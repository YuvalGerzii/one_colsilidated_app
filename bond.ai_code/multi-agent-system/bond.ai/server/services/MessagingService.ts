import { Pool } from 'pg';
import Redis from 'ioredis';
import { Server as SocketIOServer } from 'socket.io';

/**
 * In-App Messaging Service
 *
 * Implements enterprise-grade messaging with:
 * - Redis Pub/Sub for horizontal scaling across multiple servers
 * - WebSocket singleton pattern for connection management
 * - Message batching and backpressure control
 * - Persistent message storage with offline queue
 * - Read receipts and typing indicators
 * - Message threading and reactions
 */

export interface Message {
  id: string;
  conversationId: string;
  senderId: string;
  recipientId: string;
  content: string;
  type: 'text' | 'system' | 'introduction' | 'proposal';
  metadata?: {
    replyToId?: string;
    attachments?: string[];
    mentionedUsers?: string[];
  };
  status: 'sent' | 'delivered' | 'read';
  createdAt: Date;
  deliveredAt?: Date;
  readAt?: Date;
}

export interface Conversation {
  id: string;
  participants: string[];
  type: 'direct' | 'negotiation' | 'introduction';
  matchId?: string;
  lastMessage?: Message;
  unreadCount: Record<string, number>;
  createdAt: Date;
  updatedAt: Date;
}

export interface TypingIndicator {
  conversationId: string;
  userId: string;
  isTyping: boolean;
  timestamp: Date;
}

export class MessagingService {
  private pool: Pool;
  private redis: Redis;
  private redisSub: Redis;  // Separate Redis client for pub/sub
  private io: SocketIOServer;

  private messageBatchSize = 50;
  private batchInterval = 1000; // 1 second
  private messageBatches = new Map<string, Message[]>();

  constructor(pool: Pool, redis: Redis, io: SocketIOServer) {
    this.pool = pool;
    this.redis = redis;
    this.io = io;

    // Create separate Redis client for subscriptions
    this.redisSub = redis.duplicate();

    this.setupWebSocketHandlers();
    this.setupRedisPubSub();
    this.setupBatchProcessing();
  }

  /**
   * Setup Redis Pub/Sub for multi-server scaling
   */
  private setupRedisPubSub(): void {
    this.redisSub.subscribe('messages:new', 'messages:delivered', 'messages:read', 'typing:indicator');

    this.redisSub.on('message', (channel, message) => {
      const data = JSON.parse(message);

      switch (channel) {
        case 'messages:new':
          this.handleNewMessageBroadcast(data);
          break;

        case 'messages:delivered':
          this.handleDeliveryReceipt(data);
          break;

        case 'messages:read':
          this.handleReadReceipt(data);
          break;

        case 'typing:indicator':
          this.handleTypingIndicator(data);
          break;
      }
    });
  }

  /**
   * Setup WebSocket handlers
   */
  private setupWebSocketHandlers(): void {
    this.io.on('connection', (socket) => {
      const userId = (socket as any).userId;

      if (!userId) {
        socket.disconnect();
        return;
      }

      console.log(`User ${userId} connected to messaging`);

      // Join user's personal room
      socket.join(`user:${userId}`);

      // Join all conversation rooms
      this.joinUserConversations(userId, socket);

      // Handle message sending
      socket.on('message:send', async (data) => {
        await this.handleSendMessage(userId, data, socket);
      });

      // Handle typing indicators
      socket.on('typing:start', (data) => {
        this.handleTypingStart(userId, data.conversationId);
      });

      socket.on('typing:stop', (data) => {
        this.handleTypingStop(userId, data.conversationId);
      });

      // Handle message read receipts
      socket.on('message:read', async (data) => {
        await this.handleMessageRead(userId, data.messageId);
      });

      // Handle conversation sync
      socket.on('conversations:sync', async () => {
        await this.syncConversations(userId, socket);
      });

      // Handle message history request
      socket.on('messages:history', async (data) => {
        await this.getMessageHistory(userId, data.conversationId, data.limit, data.before, socket);
      });

      socket.on('disconnect', () => {
        console.log(`User ${userId} disconnected from messaging`);
      });
    });
  }

  /**
   * Join all conversations for a user
   */
  private async joinUserConversations(userId: string, socket: any): Promise<void> {
    const client = await this.pool.connect();

    try {
      const result = await client.query(
        `SELECT id FROM conversations
         WHERE $1 = ANY(participants)`,
        [userId]
      );

      result.rows.forEach(row => {
        socket.join(`conversation:${row.id}`);
      });
    } finally {
      client.release();
    }
  }

  /**
   * Handle sending a message with batching
   */
  private async handleSendMessage(
    senderId: string,
    data: { conversationId?: string; recipientId: string; content: string; type?: string; metadata?: any },
    socket: any
  ): Promise<void> {
    const client = await this.pool.connect();

    try {
      let conversationId = data.conversationId;

      // Create conversation if it doesn't exist
      if (!conversationId) {
        const convResult = await client.query(
          `INSERT INTO conversations (participants, type)
           VALUES ($1, 'direct')
           RETURNING id`,
          [[senderId, data.recipientId]]
        );

        conversationId = convResult.rows[0].id;

        // Make both users join the conversation room
        this.io.to(`user:${senderId}`).socketsJoin(`conversation:${conversationId}`);
        this.io.to(`user:${data.recipientId}`).socketsJoin(`conversation:${conversationId}`);
      }

      // Insert message
      const messageResult = await client.query(
        `INSERT INTO messages (conversation_id, sender_id, recipient_id, content, type, metadata, status)
         VALUES ($1, $2, $3, $4, $5, $6, 'sent')
         RETURNING *`,
        [conversationId, senderId, data.recipientId, data.content, data.type || 'text', JSON.stringify(data.metadata || {})]
      );

      const message: Message = {
        id: messageResult.rows[0].id,
        conversationId,
        senderId,
        recipientId: data.recipientId,
        content: data.content,
        type: data.type as any || 'text',
        metadata: data.metadata,
        status: 'sent',
        createdAt: messageResult.rows[0].created_at
      };

      // Update conversation's last message
      await client.query(
        `UPDATE conversations
         SET last_message_id = $1,
             updated_at = NOW()
         WHERE id = $2`,
        [message.id, conversationId]
      );

      // Increment unread count for recipient
      await this.incrementUnreadCount(conversationId, data.recipientId);

      // Add to batch for processing
      this.addToBatch(conversationId, message);

      // Publish to Redis for multi-server support
      await this.redis.publish('messages:new', JSON.stringify({
        message,
        conversationId
      }));

      // Send acknowledgment to sender
      socket.emit('message:sent', {
        tempId: data.metadata?.tempId,  // For optimistic UI updates
        message
      });

      // Store in offline queue if recipient is offline
      const isOnline = await this.isUserOnline(data.recipientId);
      if (!isOnline) {
        await this.addToOfflineQueue(data.recipientId, message);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      socket.emit('error', { message: 'Failed to send message' });
    } finally {
      client.release();
    }
  }

  /**
   * Add message to batch for processing
   */
  private addToBatch(conversationId: string, message: Message): void {
    if (!this.messageBatches.has(conversationId)) {
      this.messageBatches.set(conversationId, []);
    }

    const batch = this.messageBatches.get(conversationId)!;
    batch.push(message);

    // Process immediately if batch is full
    if (batch.length >= this.messageBatchSize) {
      this.processBatch(conversationId);
    }
  }

  /**
   * Setup batch processing at intervals
   */
  private setupBatchProcessing(): void {
    setInterval(() => {
      this.messageBatches.forEach((batch, conversationId) => {
        if (batch.length > 0) {
          this.processBatch(conversationId);
        }
      });
    }, this.batchInterval);
  }

  /**
   * Process message batch
   */
  private processBatch(conversationId: string): void {
    const batch = this.messageBatches.get(conversationId);

    if (!batch || batch.length === 0) {
      return;
    }

    // Broadcast batch to conversation room
    this.io.to(`conversation:${conversationId}`).emit('messages:batch', {
      conversationId,
      messages: batch
    });

    // Clear batch
    this.messageBatches.set(conversationId, []);
  }

  /**
   * Handle new message broadcast from Redis
   */
  private handleNewMessageBroadcast(data: { message: Message; conversationId: string }): void {
    const { message, conversationId } = data;

    // Emit to conversation room
    this.io.to(`conversation:${conversationId}`).emit('message:new', message);

    // Emit to recipient's personal room for notifications
    this.io.to(`user:${message.recipientId}`).emit('notification:message', {
      type: 'new_message',
      message,
      conversationId
    });
  }

  /**
   * Handle typing indicator
   */
  private handleTypingStart(userId: string, conversationId: string): void {
    const indicator: TypingIndicator = {
      conversationId,
      userId,
      isTyping: true,
      timestamp: new Date()
    };

    // Publish to Redis
    this.redis.publish('typing:indicator', JSON.stringify(indicator));

    // Broadcast to conversation (except sender)
    this.io.to(`conversation:${conversationId}`).except(`user:${userId}`).emit('typing:update', indicator);
  }

  /**
   * Handle typing stop
   */
  private handleTypingStop(userId: string, conversationId: string): void {
    const indicator: TypingIndicator = {
      conversationId,
      userId,
      isTyping: false,
      timestamp: new Date()
    };

    this.redis.publish('typing:indicator', JSON.stringify(indicator));
    this.io.to(`conversation:${conversationId}`).except(`user:${userId}`).emit('typing:update', indicator);
  }

  /**
   * Handle typing indicator broadcast
   */
  private handleTypingIndicator(indicator: TypingIndicator): void {
    this.io.to(`conversation:${indicator.conversationId}`)
      .except(`user:${indicator.userId}`)
      .emit('typing:update', indicator);
  }

  /**
   * Handle message read receipt
   */
  private async handleMessageRead(userId: string, messageId: string): Promise<void> {
    const client = await this.pool.connect();

    try {
      // Update message status
      const result = await client.query(
        `UPDATE messages
         SET status = 'read', read_at = NOW()
         WHERE id = $1 AND recipient_id = $2 AND status != 'read'
         RETURNING conversation_id, sender_id`,
        [messageId, userId]
      );

      if (result.rows.length > 0) {
        const { conversation_id, sender_id } = result.rows[0];

        // Decrement unread count
        await this.decrementUnreadCount(conversation_id, userId);

        // Publish read receipt
        await this.redis.publish('messages:read', JSON.stringify({
          messageId,
          conversationId: conversation_id,
          readBy: userId,
          readAt: new Date()
        }));

        // Notify sender
        this.io.to(`user:${sender_id}`).emit('message:read', {
          messageId,
          conversationId: conversation_id,
          readBy: userId,
          readAt: new Date()
        });
      }
    } finally {
      client.release();
    }
  }

  /**
   * Handle read receipt broadcast
   */
  private handleReadReceipt(data: { messageId: string; conversationId: string; readBy: string; readAt: Date }): void {
    this.io.to(`conversation:${data.conversationId}`).emit('message:read', data);
  }

  /**
   * Handle delivery receipt broadcast
   */
  private handleDeliveryReceipt(data: { messageId: string; deliveredTo: string; deliveredAt: Date }): void {
    this.io.to(`user:${data.deliveredTo}`).emit('message:delivered', data);
  }

  /**
   * Sync conversations for a user
   */
  private async syncConversations(userId: string, socket: any): Promise<void> {
    const client = await this.pool.connect();

    try {
      const result = await client.query(
        `SELECT
           c.*,
           m.content as last_message_content,
           m.created_at as last_message_time,
           m.sender_id as last_message_sender,
           (
             SELECT COUNT(*)
             FROM messages
             WHERE conversation_id = c.id
               AND recipient_id = $1
               AND status != 'read'
           ) as unread_count
         FROM conversations c
         LEFT JOIN messages m ON c.last_message_id = m.id
         WHERE $1 = ANY(c.participants)
         ORDER BY c.updated_at DESC`,
        [userId]
      );

      const conversations = result.rows;

      socket.emit('conversations:synced', {
        conversations,
        timestamp: new Date()
      });
    } finally {
      client.release();
    }
  }

  /**
   * Get message history for a conversation
   */
  private async getMessageHistory(
    userId: string,
    conversationId: string,
    limit: number = 50,
    before?: string,
    socket?: any
  ): Promise<void> {
    const client = await this.pool.connect();

    try {
      // Verify user is participant
      const accessCheck = await client.query(
        `SELECT 1 FROM conversations
         WHERE id = $1 AND $2 = ANY(participants)`,
        [conversationId, userId]
      );

      if (accessCheck.rows.length === 0) {
        socket?.emit('error', { message: 'Access denied' });
        return;
      }

      // Get messages
      let query = `
        SELECT * FROM messages
        WHERE conversation_id = $1
      `;

      const params: any[] = [conversationId];

      if (before) {
        query += ` AND created_at < (SELECT created_at FROM messages WHERE id = $2)`;
        params.push(before);
      }

      query += ` ORDER BY created_at DESC LIMIT $${params.length + 1}`;
      params.push(limit);

      const result = await client.query(query, params);

      socket?.emit('messages:history', {
        conversationId,
        messages: result.rows.reverse(),
        hasMore: result.rows.length === limit
      });
    } finally {
      client.release();
    }
  }

  /**
   * Check if user is online
   */
  private async isUserOnline(userId: string): Promise<boolean> {
    const sockets = await this.io.in(`user:${userId}`).fetchSockets();
    return sockets.length > 0;
  }

  /**
   * Add message to offline queue
   */
  private async addToOfflineQueue(userId: string, message: Message): Promise<void> {
    const key = `offline:${userId}:messages`;
    await this.redis.rpush(key, JSON.stringify(message));
    await this.redis.expire(key, 86400 * 7); // 7 days
  }

  /**
   * Increment unread count
   */
  private async incrementUnreadCount(conversationId: string, userId: string): Promise<void> {
    const key = `unread:${conversationId}:${userId}`;
    await this.redis.incr(key);
  }

  /**
   * Decrement unread count
   */
  private async decrementUnreadCount(conversationId: string, userId: string): Promise<void> {
    const key = `unread:${conversationId}:${userId}`;
    await this.redis.decr(key);
  }
}
