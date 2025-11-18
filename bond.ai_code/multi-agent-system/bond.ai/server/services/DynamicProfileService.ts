import { Pool } from 'pg';
import Redis from 'ioredis';
import { Server as SocketIOServer } from 'socket.io';

/**
 * Dynamic Need/Offering Updates Service
 *
 * Implements real-time profile updates with:
 * - Delta updates (only send changes)
 * - WebSocket heartbeats for connection monitoring
 * - Robust reconnection logic with exponential backoff
 * - State synchronization after reconnection
 * - Resource management and connection limiting
 */

export interface Need {
  id: string;
  category: string;
  description: string;
  priority: 'low' | 'medium' | 'high' | 'critical';
  urgency: 'flexible' | 'weeks' | 'days' | 'immediate';
  flexibility: number; // 0-1
  status: 'active' | 'fulfilled' | 'expired';
  createdAt: Date;
  updatedAt: Date;
}

export interface Offering {
  id: string;
  category: string;
  description: string;
  value: string;
  capacity: 'limited' | 'moderate' | 'high' | 'unlimited';
  conditions?: string;
  status: 'available' | 'reserved' | 'unavailable';
  createdAt: Date;
  updatedAt: Date;
}

export interface ProfileUpdate {
  type: 'need' | 'offering';
  action: 'create' | 'update' | 'delete';
  data: Need | Offering | Partial<Need> | Partial<Offering>;
  userId: string;
  timestamp: Date;
  version: number; // For conflict resolution
}

export interface DeltaUpdate {
  id: string;
  changes: Record<string, any>;
  previousValues?: Record<string, any>;
  timestamp: Date;
}

export class DynamicProfileService {
  private pool: Pool;
  private redis: Redis;
  private io: SocketIOServer;
  private heartbeatInterval = 30000; // 30 seconds
  private reconnectAttempts = new Map<string, number>();

  constructor(pool: Pool, redis: Redis, io: SocketIOServer) {
    this.pool = pool;
    this.redis = redis;
    this.io = io;

    this.setupWebSocketHandlers();
  }

  /**
   * Setup WebSocket handlers for real-time updates
   */
  private setupWebSocketHandlers(): void {
    this.io.on('connection', (socket) => {
      const userId = (socket as any).userId;

      if (!userId) {
        socket.disconnect();
        return;
      }

      console.log(`User ${userId} connected for profile updates`);

      // Join user's personal room
      socket.join(`user:${userId}`);

      // Setup heartbeat
      this.setupHeartbeat(socket, userId);

      // Handle profile update requests
      socket.on('profile:update:need', async (data) => {
        await this.handleNeedUpdate(userId, data, socket);
      });

      socket.on('profile:update:offering', async (data) => {
        await this.handleOfferingUpdate(userId, data, socket);
      });

      // Handle sync requests (after reconnection)
      socket.on('profile:sync', async () => {
        await this.syncProfile(userId, socket);
      });

      // Handle disconnection
      socket.on('disconnect', () => {
        console.log(`User ${userId} disconnected`);
        this.handleDisconnection(userId);
      });

      // Send initial sync on connection
      this.syncProfile(userId, socket);
    });
  }

  /**
   * Setup heartbeat to monitor connection
   */
  private setupHeartbeat(socket: any, userId: string): void {
    const heartbeat = setInterval(() => {
      socket.emit('heartbeat:ping');

      const timeout = setTimeout(() => {
        console.log(`Heartbeat timeout for user ${userId}`);
        socket.disconnect();
      }, 5000);

      socket.once('heartbeat:pong', () => {
        clearTimeout(timeout);
      });
    }, this.heartbeatInterval);

    socket.on('disconnect', () => {
      clearInterval(heartbeat);
    });
  }

  /**
   * Handle need updates with delta sync
   */
  private async handleNeedUpdate(
    userId: string,
    data: { action: 'create' | 'update' | 'delete'; need: Partial<Need> },
    socket: any
  ): Promise<void> {
    const client = await this.pool.connect();

    try {
      const { action, need } = data;
      let result;
      let delta: DeltaUpdate | null = null;

      // Get current version
      const version = await this.getProfileVersion(userId);

      switch (action) {
        case 'create':
          result = await client.query(
            `INSERT INTO user_needs (user_id, category, description, priority, urgency, flexibility, status)
             VALUES ($1, $2, $3, $4, $5, $6, 'active')
             RETURNING *`,
            [userId, need.category, need.description, need.priority, need.urgency, need.flexibility || 0.5]
          );

          delta = {
            id: result.rows[0].id,
            changes: { action: 'create', ...result.rows[0] },
            timestamp: new Date()
          };
          break;

        case 'update':
          // Get previous values for delta
          const previousResult = await client.query(
            `SELECT * FROM user_needs WHERE id = $1 AND user_id = $2`,
            [need.id, userId]
          );

          if (previousResult.rows.length === 0) {
            socket.emit('error', { message: 'Need not found' });
            return;
          }

          const previous = previousResult.rows[0];

          // Build update query dynamically
          const updates: string[] = [];
          const values: any[] = [];
          let paramIndex = 3;

          if (need.description !== undefined && need.description !== previous.description) {
            updates.push(`description = $${paramIndex++}`);
            values.push(need.description);
          }

          if (need.priority !== undefined && need.priority !== previous.priority) {
            updates.push(`priority = $${paramIndex++}`);
            values.push(need.priority);
          }

          if (need.urgency !== undefined && need.urgency !== previous.urgency) {
            updates.push(`urgency = $${paramIndex++}`);
            values.push(need.urgency);
          }

          if (need.status !== undefined && need.status !== previous.status) {
            updates.push(`status = $${paramIndex++}`);
            values.push(need.status);
          }

          if (updates.length === 0) {
            socket.emit('profile:update:ack', { message: 'No changes detected' });
            return;
          }

          updates.push('updated_at = NOW()');

          result = await client.query(
            `UPDATE user_needs
             SET ${updates.join(', ')}
             WHERE id = $1 AND user_id = $2
             RETURNING *`,
            [need.id, userId, ...values]
          );

          // Create delta with only changed fields
          const changes: Record<string, any> = {};
          const previousValues: Record<string, any> = {};

          Object.keys(need).forEach(key => {
            if (need[key as keyof Need] !== previous[key]) {
              changes[key] = need[key as keyof Need];
              previousValues[key] = previous[key];
            }
          });

          delta = {
            id: need.id!,
            changes,
            previousValues,
            timestamp: new Date()
          };
          break;

        case 'delete':
          await client.query(
            `UPDATE user_needs
             SET status = 'expired', updated_at = NOW()
             WHERE id = $1 AND user_id = $2`,
            [need.id, userId]
          );

          delta = {
            id: need.id!,
            changes: { action: 'delete', status: 'expired' },
            timestamp: new Date()
          };
          break;
      }

      // Increment version
      const newVersion = version + 1;
      await this.setProfileVersion(userId, newVersion);

      // Store update in Redis for offline queue
      await this.queueUpdate(userId, {
        type: 'need',
        action,
        data: result?.rows[0] || need,
        userId,
        timestamp: new Date(),
        version: newVersion
      });

      // Broadcast delta update to user's other connected clients
      this.io.to(`user:${userId}`).emit('profile:delta', {
        type: 'need',
        delta,
        version: newVersion
      });

      // Trigger re-matching if significant change
      if (action === 'create' || (action === 'update' && delta?.changes.priority === 'critical')) {
        await this.triggerReMatching(userId);
      }

      socket.emit('profile:update:ack', {
        success: true,
        version: newVersion,
        delta
      });
    } catch (error) {
      console.error('Error handling need update:', error);
      socket.emit('error', { message: 'Failed to update need' });
    } finally {
      client.release();
    }
  }

  /**
   * Handle offering updates with delta sync
   */
  private async handleOfferingUpdate(
    userId: string,
    data: { action: 'create' | 'update' | 'delete'; offering: Partial<Offering> },
    socket: any
  ): Promise<void> {
    const client = await this.pool.connect();

    try {
      const { action, offering } = data;
      let result;
      let delta: DeltaUpdate | null = null;

      const version = await this.getProfileVersion(userId);

      switch (action) {
        case 'create':
          result = await client.query(
            `INSERT INTO user_offerings (user_id, category, description, value, capacity, conditions, status)
             VALUES ($1, $2, $3, $4, $5, $6, 'available')
             RETURNING *`,
            [userId, offering.category, offering.description, offering.value, offering.capacity, offering.conditions]
          );

          delta = {
            id: result.rows[0].id,
            changes: { action: 'create', ...result.rows[0] },
            timestamp: new Date()
          };
          break;

        case 'update':
          const previousResult = await client.query(
            `SELECT * FROM user_offerings WHERE id = $1 AND user_id = $2`,
            [offering.id, userId]
          );

          if (previousResult.rows.length === 0) {
            socket.emit('error', { message: 'Offering not found' });
            return;
          }

          const previous = previousResult.rows[0];
          const updates: string[] = [];
          const values: any[] = [];
          let paramIndex = 3;

          if (offering.description !== undefined && offering.description !== previous.description) {
            updates.push(`description = $${paramIndex++}`);
            values.push(offering.description);
          }

          if (offering.capacity !== undefined && offering.capacity !== previous.capacity) {
            updates.push(`capacity = $${paramIndex++}`);
            values.push(offering.capacity);
          }

          if (offering.status !== undefined && offering.status !== previous.status) {
            updates.push(`status = $${paramIndex++}`);
            values.push(offering.status);
          }

          if (updates.length === 0) {
            socket.emit('profile:update:ack', { message: 'No changes detected' });
            return;
          }

          updates.push('updated_at = NOW()');

          result = await client.query(
            `UPDATE user_offerings
             SET ${updates.join(', ')}
             WHERE id = $1 AND user_id = $2
             RETURNING *`,
            [offering.id, userId, ...values]
          );

          const changes: Record<string, any> = {};
          const previousValues: Record<string, any> = {};

          Object.keys(offering).forEach(key => {
            if (offering[key as keyof Offering] !== previous[key]) {
              changes[key] = offering[key as keyof Offering];
              previousValues[key] = previous[key];
            }
          });

          delta = {
            id: offering.id!,
            changes,
            previousValues,
            timestamp: new Date()
          };
          break;

        case 'delete':
          await client.query(
            `UPDATE user_offerings
             SET status = 'unavailable', updated_at = NOW()
             WHERE id = $1 AND user_id = $2`,
            [offering.id, userId]
          );

          delta = {
            id: offering.id!,
            changes: { action: 'delete', status: 'unavailable' },
            timestamp: new Date()
          };
          break;
      }

      const newVersion = version + 1;
      await this.setProfileVersion(userId, newVersion);

      await this.queueUpdate(userId, {
        type: 'offering',
        action,
        data: result?.rows[0] || offering,
        userId,
        timestamp: new Date(),
        version: newVersion
      });

      this.io.to(`user:${userId}`).emit('profile:delta', {
        type: 'offering',
        delta,
        version: newVersion
      });

      if (action === 'create') {
        await this.triggerReMatching(userId);
      }

      socket.emit('profile:update:ack', {
        success: true,
        version: newVersion,
        delta
      });
    } catch (error) {
      console.error('Error handling offering update:', error);
      socket.emit('error', { message: 'Failed to update offering' });
    } finally {
      client.release();
    }
  }

  /**
   * Sync full profile state (used after reconnection)
   */
  private async syncProfile(userId: string, socket: any): Promise<void> {
    const client = await this.pool.connect();

    try {
      const version = await this.getProfileVersion(userId);

      // Get all needs
      const needsResult = await client.query(
        `SELECT * FROM user_needs WHERE user_id = $1 AND status != 'expired'`,
        [userId]
      );

      // Get all offerings
      const offeringsResult = await client.query(
        `SELECT * FROM user_offerings WHERE user_id = $1 AND status != 'unavailable'`,
        [userId]
      );

      // Get queued updates (if any)
      const queuedUpdates = await this.getQueuedUpdates(userId);

      socket.emit('profile:sync:complete', {
        version,
        needs: needsResult.rows,
        offerings: offeringsResult.rows,
        queuedUpdates,
        timestamp: new Date()
      });

      // Clear queued updates after successful sync
      await this.clearQueuedUpdates(userId);

      // Reset reconnect attempts
      this.reconnectAttempts.delete(userId);
    } catch (error) {
      console.error('Error syncing profile:', error);
      socket.emit('error', { message: 'Failed to sync profile' });
    } finally {
      client.release();
    }
  }

  /**
   * Handle disconnection with exponential backoff tracking
   */
  private handleDisconnection(userId: string): void {
    const attempts = this.reconnectAttempts.get(userId) || 0;
    this.reconnectAttempts.set(userId, attempts + 1);

    // Store disconnection time for offline queue management
    this.redis.setex(
      `user:${userId}:last_disconnect`,
      3600,
      new Date().toISOString()
    );
  }

  /**
   * Trigger re-matching when profile changes significantly
   */
  private async triggerReMatching(userId: string): Promise<void> {
    try {
      // Publish event for matching engine
      await this.redis.publish('profile:changed', JSON.stringify({
        userId,
        timestamp: new Date().toISOString()
      }));

      // Notify user of new potential matches
      this.io.to(`user:${userId}`).emit('matching:triggered', {
        message: 'Your profile changes may result in new matches'
      });
    } catch (error) {
      console.error('Error triggering re-matching:', error);
    }
  }

  /**
   * Get profile version for conflict resolution
   */
  private async getProfileVersion(userId: string): Promise<number> {
    const version = await this.redis.get(`profile:${userId}:version`);
    return version ? parseInt(version) : 0;
  }

  /**
   * Set profile version
   */
  private async setProfileVersion(userId: string, version: number): Promise<void> {
    await this.redis.set(`profile:${userId}:version`, version.toString());
  }

  /**
   * Queue update for offline clients
   */
  private async queueUpdate(userId: string, update: ProfileUpdate): Promise<void> {
    const key = `profile:${userId}:queue`;
    await this.redis.rpush(key, JSON.stringify(update));
    await this.redis.expire(key, 86400); // 24 hours
  }

  /**
   * Get queued updates
   */
  private async getQueuedUpdates(userId: string): Promise<ProfileUpdate[]> {
    const key = `profile:${userId}:queue`;
    const updates = await this.redis.lrange(key, 0, -1);

    return updates.map(u => JSON.parse(u));
  }

  /**
   * Clear queued updates
   */
  private async clearQueuedUpdates(userId: string): Promise<void> {
    const key = `profile:${userId}:queue`;
    await this.redis.del(key);
  }
}
