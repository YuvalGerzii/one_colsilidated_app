/**
 * Notification Service
 * Real-time notifications via WebSocket
 */

import { Server as SocketIOServer } from 'socket.io';
import { getDb } from '../database/connection';

export interface Notification {
  id?: string;
  userId: string;
  type: NotificationType;
  title: string;
  message: string;
  data?: any;
  priority?: 'low' | 'medium' | 'high' | 'critical';
  read?: boolean;
  createdAt?: Date;
}

export enum NotificationType {
  NEW_MATCH = 'new_match',
  NEGOTIATION_STARTED = 'negotiation_started',
  NEGOTIATION_UPDATE = 'negotiation_update',
  PROPOSAL_RECEIVED = 'proposal_received',
  AGREEMENT_REACHED = 'agreement_reached',
  INTRODUCTION_REQUESTED = 'introduction_requested',
  NETWORK_UPDATE = 'network_update',
  SYSTEM = 'system',
}

export class NotificationService {
  private io: SocketIOServer;

  constructor(io: SocketIOServer) {
    this.io = io;
  }

  /**
   * Send notification to user
   */
  async notify(notification: Notification): Promise<void> {
    const db = getDb();

    // Store in database
    const result = await db.queryOne<{ id: string }>(
      `INSERT INTO notifications (user_id, type, title, message, data, priority, created_at)
       VALUES ($1, $2, $3, $4, $5, $6, NOW())
       RETURNING id`,
      [
        notification.userId,
        notification.type,
        notification.title,
        notification.message,
        JSON.stringify(notification.data || {}),
        notification.priority || 'medium',
      ]
    );

    const notificationWithId = {
      ...notification,
      id: result?.id,
      createdAt: new Date(),
    };

    // Send via WebSocket
    this.io.to(`user:${notification.userId}`).emit('notification', notificationWithId);

    // Also cache in Redis for quick access
    await db.setCacheJSON(
      `notification:${result?.id}`,
      notificationWithId,
      86400 // 24 hours
    );
  }

  /**
   * Notify about new match
   */
  async notifyNewMatch(userId: string, match: any): Promise<void> {
    await this.notify({
      userId,
      type: NotificationType.NEW_MATCH,
      title: '🎯 New Match Found!',
      message: `Perfect match with ${match.agent2.userContact.name} (${(match.overallScore * 100).toFixed(0)}% compatibility)`,
      data: { matchId: match.id, match },
      priority: match.priority === 'critical' ? 'critical' : 'high',
    });
  }

  /**
   * Notify about negotiation update
   */
  async notifyNegotiationUpdate(
    userId: string,
    negotiationId: string,
    update: {
      type: 'started' | 'proposal' | 'counter' | 'agreement' | 'failed';
      message: string;
      data?: any;
    }
  ): Promise<void> {
    const typeMap = {
      started: NotificationType.NEGOTIATION_STARTED,
      proposal: NotificationType.PROPOSAL_RECEIVED,
      counter: NotificationType.NEGOTIATION_UPDATE,
      agreement: NotificationType.AGREEMENT_REACHED,
      failed: NotificationType.NEGOTIATION_UPDATE,
    };

    const priorityMap = {
      started: 'high' as const,
      proposal: 'high' as const,
      counter: 'medium' as const,
      agreement: 'critical' as const,
      failed: 'medium' as const,
    };

    await this.notify({
      userId,
      type: typeMap[update.type],
      title: this.getNegotiationTitle(update.type),
      message: update.message,
      data: { negotiationId, ...update.data },
      priority: priorityMap[update.type],
    });

    // Also emit to negotiation room
    this.io.to(`negotiation:${negotiationId}`).emit('negotiation_update', {
      type: update.type,
      message: update.message,
      data: update.data,
      timestamp: new Date(),
    });
  }

  /**
   * Get negotiation notification title
   */
  private getNegotiationTitle(type: string): string {
    const titles = {
      started: '🤝 Negotiation Started',
      proposal: '📋 New Proposal Received',
      counter: '💬 Counter-Proposal Received',
      agreement: '✅ Agreement Reached!',
      failed: '❌ Negotiation Ended',
    };
    return titles[type as keyof typeof titles] || 'Negotiation Update';
  }

  /**
   * Broadcast system notification to all users
   */
  async broadcast(notification: Omit<Notification, 'userId'>): Promise<void> {
    this.io.emit('notification', {
      ...notification,
      type: NotificationType.SYSTEM,
      createdAt: new Date(),
    });
  }

  /**
   * Get unread notifications for user
   */
  async getUnread(userId: string, limit: number = 50): Promise<Notification[]> {
    const db = getDb();

    const notifications = await db.queryMany<Notification>(
      `SELECT id, user_id, type, title, message, data, priority, read, created_at
       FROM notifications
       WHERE user_id = $1 AND read = false
       ORDER BY created_at DESC
       LIMIT $2`,
      [userId, limit]
    );

    return notifications;
  }

  /**
   * Get all notifications for user
   */
  async getNotifications(
    userId: string,
    options: {
      limit?: number;
      offset?: number;
      unreadOnly?: boolean;
    } = {}
  ): Promise<{ notifications: Notification[]; total: number }> {
    const db = getDb();
    const { limit = 50, offset = 0, unreadOnly = false } = options;

    const whereClause = unreadOnly
      ? 'WHERE user_id = $1 AND read = false'
      : 'WHERE user_id = $1';

    const notifications = await db.queryMany<Notification>(
      `SELECT id, user_id, type, title, message, data, priority, read, created_at
       FROM notifications
       ${whereClause}
       ORDER BY created_at DESC
       LIMIT $2 OFFSET $3`,
      [userId, limit, offset]
    );

    const totalResult = await db.queryOne<{ count: number }>(
      `SELECT COUNT(*) as count FROM notifications ${whereClause}`,
      [userId]
    );

    return {
      notifications,
      total: totalResult?.count || 0,
    };
  }

  /**
   * Mark notification as read
   */
  async markAsRead(notificationId: string): Promise<void> {
    const db = getDb();

    await db.query(
      `UPDATE notifications
       SET read = true, read_at = NOW()
       WHERE id = $1`,
      [notificationId]
    );
  }

  /**
   * Mark all notifications as read for user
   */
  async markAllAsRead(userId: string): Promise<void> {
    const db = getDb();

    await db.query(
      `UPDATE notifications
       SET read = true, read_at = NOW()
       WHERE user_id = $1 AND read = false`,
      [userId]
    );
  }

  /**
   * Delete notification
   */
  async deleteNotification(notificationId: string): Promise<void> {
    const db = getDb();

    await db.query('DELETE FROM notifications WHERE id = $1', [notificationId]);
    await db.deleteCache(`notification:${notificationId}`);
  }

  /**
   * Delete old notifications (cleanup task)
   */
  async deleteOldNotifications(daysOld: number = 30): Promise<number> {
    const db = getDb();

    const result = await db.query(
      `DELETE FROM notifications
       WHERE created_at < NOW() - INTERVAL '${daysOld} days'`,
      []
    );

    return result.rowCount || 0;
  }

  /**
   * Get notification statistics
   */
  async getStats(userId: string): Promise<{
    total: number;
    unread: number;
    byType: Record<string, number>;
    byPriority: Record<string, number>;
  }> {
    const db = getDb();

    const stats = await db.queryOne<{
      total: number;
      unread: number;
    }>(
      `SELECT
        COUNT(*) as total,
        COUNT(*) FILTER (WHERE read = false) as unread
       FROM notifications
       WHERE user_id = $1`,
      [userId]
    );

    const byType = await db.queryMany<{ type: string; count: number }>(
      `SELECT type, COUNT(*) as count
       FROM notifications
       WHERE user_id = $1
       GROUP BY type`,
      [userId]
    );

    const byPriority = await db.queryMany<{ priority: string; count: number }>(
      `SELECT priority, COUNT(*) as count
       FROM notifications
       WHERE user_id = $1
       GROUP BY priority`,
      [userId]
    );

    return {
      total: stats?.total || 0,
      unread: stats?.unread || 0,
      byType: byType.reduce(
        (acc, row) => {
          acc[row.type] = row.count;
          return acc;
        },
        {} as Record<string, number>
      ),
      byPriority: byPriority.reduce(
        (acc, row) => {
          acc[row.priority] = row.count;
          return acc;
        },
        {} as Record<string, number>
      ),
    };
  }
}
