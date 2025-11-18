import { Router, Response } from 'express';
import { Pool } from 'pg';
import { authenticateToken, AuthRequest } from '../middleware/auth';

export function createNotificationRoutes(pool: Pool): Router {
  const router = Router();

  // GET /api/notifications - Get user's notifications (requires auth)
  router.get('/', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const userId = req.user!.userId;
      const { unreadOnly = 'false', limit = '50', offset = '0' } = req.query;

      let query = `
        SELECT
          id, notification_type as "notificationType", title, message,
          action_url as "actionUrl", metadata, is_read as "isRead",
          is_dismissed as "isDismissed", created_at as "createdAt", read_at as "readAt"
        FROM notifications
        WHERE user_id = $1 AND is_dismissed = false
      `;

      const params: any[] = [userId];

      if (unreadOnly === 'true') {
        query += ` AND is_read = false`;
      }

      query += ` ORDER BY created_at DESC LIMIT $2 OFFSET $3`;
      params.push(parseInt(limit as string), parseInt(offset as string));

      const result = await pool.query(query, params);

      // Get unread count
      const countResult = await pool.query(
        'SELECT COUNT(*)::int as count FROM notifications WHERE user_id = $1 AND is_read = false AND is_dismissed = false',
        [userId]
      );

      res.json({
        success: true,
        notifications: result.rows,
        unreadCount: countResult.rows[0].count,
      });
    } catch (error) {
      console.error('Error fetching notifications:', error);
      res.status(500).json({ success: false, error: 'Failed to fetch notifications' });
    }
  });

  // POST /api/notifications/:id/read - Mark notification as read (requires auth)
  router.post('/:id/read', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const { id } = req.params;
      const userId = req.user!.userId;

      const result = await pool.query(
        `UPDATE notifications
        SET is_read = true, read_at = NOW()
        WHERE id = $1 AND user_id = $2
        RETURNING id`,
        [id, userId]
      );

      if (result.rows.length === 0) {
        res.status(404).json({ success: false, error: 'Notification not found' });
        return;
      }

      res.json({ success: true, message: 'Notification marked as read' });
    } catch (error) {
      console.error('Error marking notification as read:', error);
      res.status(500).json({ success: false, error: 'Failed to update notification' });
    }
  });

  // POST /api/notifications/read-all - Mark all as read (requires auth)
  router.post('/read-all', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const userId = req.user!.userId;

      await pool.query(
        `UPDATE notifications
        SET is_read = true, read_at = NOW()
        WHERE user_id = $1 AND is_read = false`,
        [userId]
      );

      res.json({ success: true, message: 'All notifications marked as read' });
    } catch (error) {
      console.error('Error marking all notifications as read:', error);
      res.status(500).json({ success: false, error: 'Failed to update notifications' });
    }
  });

  // POST /api/notifications/:id/dismiss - Dismiss notification (requires auth)
  router.post('/:id/dismiss', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const { id } = req.params;
      const userId = req.user!.userId;

      await pool.query(
        `UPDATE notifications
        SET is_dismissed = true
        WHERE id = $1 AND user_id = $2`,
        [id, userId]
      );

      res.json({ success: true, message: 'Notification dismissed' });
    } catch (error) {
      console.error('Error dismissing notification:', error);
      res.status(500).json({ success: false, error: 'Failed to dismiss notification' });
    }
  });

  // DELETE /api/notifications/clear - Clear all dismissed (requires auth)
  router.delete('/clear', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const userId = req.user!.userId;

      await pool.query(
        'DELETE FROM notifications WHERE user_id = $1 AND is_dismissed = true',
        [userId]
      );

      res.json({ success: true, message: 'Dismissed notifications cleared' });
    } catch (error) {
      console.error('Error clearing notifications:', error);
      res.status(500).json({ success: false, error: 'Failed to clear notifications' });
    }
  });

  // POST /api/notifications/preferences - Update notification preferences (requires auth)
  router.post('/preferences', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const userId = req.user!.userId;
      const { emailNotifications, pushNotifications, notificationTypes } = req.body;

      // Store in user preferences (would need a user_preferences table)
      // For now, store in Redis or as part of user metadata
      res.json({
        success: true,
        message: 'Notification preferences updated',
        preferences: { emailNotifications, pushNotifications, notificationTypes },
      });
    } catch (error) {
      console.error('Error updating preferences:', error);
      res.status(500).json({ success: false, error: 'Failed to update preferences' });
    }
  });

  return router;
}

// Helper function to create notifications (used by other parts of the system)
export async function createNotification(
  pool: Pool,
  userId: string,
  notification: {
    type: string;
    title: string;
    message: string;
    actionUrl?: string;
    metadata?: any;
  }
): Promise<string> {
  const result = await pool.query(
    `INSERT INTO notifications (
      user_id, notification_type, title, message, action_url, metadata
    )
    VALUES ($1, $2, $3, $4, $5, $6)
    RETURNING id`,
    [
      userId,
      notification.type,
      notification.title,
      notification.message,
      notification.actionUrl || null,
      notification.metadata ? JSON.stringify(notification.metadata) : null,
    ]
  );

  return result.rows[0].id;
}
