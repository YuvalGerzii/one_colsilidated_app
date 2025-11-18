import { Router, Response } from 'express';
import { Pool } from 'pg';
import crypto from 'crypto';
import { authenticateToken, AuthRequest } from '../middleware/auth';

export function createWebhookRoutes(pool: Pool): Router {
  const router = Router();

  // POST /api/webhooks - Create webhook (requires auth)
  router.post('/', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const userId = req.user!.userId;
      const { name, url, events, teamId, retryCount = 3, timeoutSeconds = 30 } = req.body;

      if (!name || !url || !events || events.length === 0) {
        res.status(400).json({
          success: false,
          error: 'Name, url, and events are required',
        });
        return;
      }

      // Generate secret key for webhook signatures
      const secretKey = crypto.randomBytes(32).toString('hex');

      const result = await pool.query(
        `INSERT INTO webhooks (
          user_id, team_id, name, url, secret_key, events, retry_count, timeout_seconds
        )
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        RETURNING id, name, url, events, is_active as "isActive", created_at as "createdAt"`,
        [userId, teamId || null, name, url, secretKey, events, retryCount, timeoutSeconds]
      );

      res.status(201).json({
        success: true,
        webhook: {
          ...result.rows[0],
          secretKey, // Only returned once during creation
        },
      });
    } catch (error) {
      console.error('Error creating webhook:', error);
      res.status(500).json({ success: false, error: 'Failed to create webhook' });
    }
  });

  // GET /api/webhooks - Get user's webhooks (requires auth)
  router.get('/', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const userId = req.user!.userId;

      const result = await pool.query(
        `SELECT
          id, name, url, events, is_active as "isActive",
          retry_count as "retryCount", timeout_seconds as "timeoutSeconds",
          created_at as "createdAt", last_triggered_at as "lastTriggeredAt"
        FROM webhooks
        WHERE user_id = $1 OR team_id IN (
          SELECT team_id FROM team_members WHERE user_id = $1
        )
        ORDER BY created_at DESC`,
        [userId]
      );

      res.json({
        success: true,
        webhooks: result.rows,
      });
    } catch (error) {
      console.error('Error fetching webhooks:', error);
      res.status(500).json({ success: false, error: 'Failed to fetch webhooks' });
    }
  });

  // GET /api/webhooks/:id - Get webhook details (requires auth)
  router.get('/:id', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const { id } = req.params;
      const userId = req.user!.userId;

      const result = await pool.query(
        `SELECT
          w.id, w.name, w.url, w.events, w.is_active as "isActive",
          w.retry_count as "retryCount", w.timeout_seconds as "timeoutSeconds",
          w.created_at as "createdAt", w.last_triggered_at as "lastTriggeredAt"
        FROM webhooks w
        WHERE w.id = $1 AND (
          w.user_id = $2 OR w.team_id IN (
            SELECT team_id FROM team_members WHERE user_id = $2
          )
        )`,
        [id, userId]
      );

      if (result.rows.length === 0) {
        res.status(404).json({ success: false, error: 'Webhook not found' });
        return;
      }

      // Get recent deliveries
      const deliveriesResult = await pool.query(
        `SELECT
          id, event_type as "eventType", response_status as "responseStatus",
          delivery_duration_ms as "deliveryDurationMs", success,
          error_message as "errorMessage", created_at as "createdAt"
        FROM webhook_deliveries
        WHERE webhook_id = $1
        ORDER BY created_at DESC
        LIMIT 20`,
        [id]
      );

      res.json({
        success: true,
        webhook: result.rows[0],
        recentDeliveries: deliveriesResult.rows,
      });
    } catch (error) {
      console.error('Error fetching webhook:', error);
      res.status(500).json({ success: false, error: 'Failed to fetch webhook' });
    }
  });

  // PUT /api/webhooks/:id - Update webhook (requires auth)
  router.put('/:id', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const { id } = req.params;
      const userId = req.user!.userId;
      const { name, url, events, isActive, retryCount, timeoutSeconds } = req.body;

      const result = await pool.query(
        `UPDATE webhooks
        SET name = COALESCE($1, name),
            url = COALESCE($2, url),
            events = COALESCE($3, events),
            is_active = COALESCE($4, is_active),
            retry_count = COALESCE($5, retry_count),
            timeout_seconds = COALESCE($6, timeout_seconds)
        WHERE id = $7 AND (
          user_id = $8 OR team_id IN (
            SELECT team_id FROM team_members WHERE user_id = $8 AND role IN ('owner', 'admin')
          )
        )
        RETURNING id, name, url, events, is_active as "isActive"`,
        [name, url, events, isActive, retryCount, timeoutSeconds, id, userId]
      );

      if (result.rows.length === 0) {
        res.status(404).json({ success: false, error: 'Webhook not found or access denied' });
        return;
      }

      res.json({
        success: true,
        webhook: result.rows[0],
      });
    } catch (error) {
      console.error('Error updating webhook:', error);
      res.status(500).json({ success: false, error: 'Failed to update webhook' });
    }
  });

  // DELETE /api/webhooks/:id - Delete webhook (requires auth)
  router.delete('/:id', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const { id } = req.params;
      const userId = req.user!.userId;

      const result = await pool.query(
        `DELETE FROM webhooks
        WHERE id = $1 AND (
          user_id = $2 OR team_id IN (
            SELECT team_id FROM team_members WHERE user_id = $2 AND role IN ('owner', 'admin')
          )
        )
        RETURNING id`,
        [id, userId]
      );

      if (result.rows.length === 0) {
        res.status(404).json({ success: false, error: 'Webhook not found or access denied' });
        return;
      }

      res.json({
        success: true,
        message: 'Webhook deleted successfully',
      });
    } catch (error) {
      console.error('Error deleting webhook:', error);
      res.status(500).json({ success: false, error: 'Failed to delete webhook' });
    }
  });

  // POST /api/webhooks/:id/test - Test webhook (requires auth)
  router.post('/:id/test', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const { id } = req.params;
      const userId = req.user!.userId;

      // Get webhook
      const webhookResult = await pool.query(
        `SELECT id, url, secret_key, timeout_seconds
        FROM webhooks
        WHERE id = $1 AND (
          user_id = $2 OR team_id IN (
            SELECT team_id FROM team_members WHERE user_id = $2
          )
        )`,
        [id, userId]
      );

      if (webhookResult.rows.length === 0) {
        res.status(404).json({ success: false, error: 'Webhook not found' });
        return;
      }

      const webhook = webhookResult.rows[0];

      // Test payload
      const testPayload = {
        event: 'webhook.test',
        timestamp: new Date().toISOString(),
        data: {
          message: 'This is a test webhook delivery',
        },
      };

      // Send test request
      const startTime = Date.now();
      try {
        const signature = createWebhookSignature(testPayload, webhook.secret_key);

        const response = await fetch(webhook.url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Webhook-Signature': signature,
            'User-Agent': 'Agents-System-Webhook/1.0',
          },
          body: JSON.stringify(testPayload),
          signal: AbortSignal.timeout(webhook.timeout_seconds * 1000),
        });

        const duration = Date.now() - startTime;
        const responseBody = await response.text();

        // Log delivery
        await pool.query(
          `INSERT INTO webhook_deliveries (
            webhook_id, event_type, payload, response_status,
            response_body, delivery_duration_ms, success
          )
          VALUES ($1, $2, $3, $4, $5, $6, $7)`,
          [
            id,
            'webhook.test',
            JSON.stringify(testPayload),
            response.status,
            responseBody,
            duration,
            response.ok,
          ]
        );

        res.json({
          success: true,
          testResult: {
            status: response.status,
            duration,
            success: response.ok,
            response: responseBody.substring(0, 500), // Limit response size
          },
        });
      } catch (error: any) {
        const duration = Date.now() - startTime;

        // Log failed delivery
        await pool.query(
          `INSERT INTO webhook_deliveries (
            webhook_id, event_type, payload, delivery_duration_ms,
            success, error_message
          )
          VALUES ($1, $2, $3, $4, false, $5)`,
          [
            id,
            'webhook.test',
            JSON.stringify(testPayload),
            duration,
            error.message,
          ]
        );

        res.status(500).json({
          success: false,
          error: 'Webhook delivery failed',
          details: error.message,
        });
      }
    } catch (error) {
      console.error('Error testing webhook:', error);
      res.status(500).json({ success: false, error: 'Failed to test webhook' });
    }
  });

  return router;
}

// Helper function to create webhook signature
function createWebhookSignature(payload: any, secret: string): string {
  const hmac = crypto.createHmac('sha256', secret);
  hmac.update(JSON.stringify(payload));
  return hmac.digest('hex');
}

// Utility function to trigger webhooks (used by other parts of the system)
export async function triggerWebhooks(
  pool: Pool,
  eventType: string,
  userId: string,
  payload: any
): Promise<void> {
  try {
    // Get active webhooks for this event type
    const webhooks = await pool.query(
      `SELECT id, url, secret_key, retry_count, timeout_seconds
      FROM webhooks
      WHERE (user_id = $1 OR team_id IN (
        SELECT team_id FROM team_members WHERE user_id = $1
      ))
      AND is_active = true
      AND $2 = ANY(events)`,
      [userId, eventType]
    );

    // Trigger each webhook asynchronously
    for (const webhook of webhooks.rows) {
      triggerWebhookAsync(pool, webhook, eventType, payload);
    }
  } catch (error) {
    console.error('Error triggering webhooks:', error);
  }
}

// Async webhook trigger (doesn't block)
async function triggerWebhookAsync(
  pool: Pool,
  webhook: any,
  eventType: string,
  payload: any
): Promise<void> {
  const fullPayload = {
    event: eventType,
    timestamp: new Date().toISOString(),
    data: payload,
  };

  let attempt = 0;
  const maxAttempts = webhook.retry_count + 1;

  while (attempt < maxAttempts) {
    attempt++;
    const startTime = Date.now();

    try {
      const signature = createWebhookSignature(fullPayload, webhook.secret_key);

      const response = await fetch(webhook.url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Webhook-Signature': signature,
          'User-Agent': 'Agents-System-Webhook/1.0',
        },
        body: JSON.stringify(fullPayload),
        signal: AbortSignal.timeout(webhook.timeout_seconds * 1000),
      });

      const duration = Date.now() - startTime;
      const responseBody = await response.text();

      // Log delivery
      await pool.query(
        `INSERT INTO webhook_deliveries (
          webhook_id, event_type, payload, response_status,
          response_body, delivery_duration_ms, success
        )
        VALUES ($1, $2, $3, $4, $5, $6, $7)`,
        [
          webhook.id,
          eventType,
          JSON.stringify(fullPayload),
          response.status,
          responseBody.substring(0, 1000),
          duration,
          response.ok,
        ]
      );

      // Update last triggered time
      await pool.query(
        'UPDATE webhooks SET last_triggered_at = NOW() WHERE id = $1',
        [webhook.id]
      );

      if (response.ok) {
        break; // Success, no need to retry
      }

      // If not ok and retries remain, wait before retrying
      if (attempt < maxAttempts) {
        await new Promise((resolve) => setTimeout(resolve, 1000 * attempt));
      }
    } catch (error: any) {
      const duration = Date.now() - startTime;

      // Log failed delivery
      await pool.query(
        `INSERT INTO webhook_deliveries (
          webhook_id, event_type, payload, delivery_duration_ms,
          success, error_message
        )
        VALUES ($1, $2, $3, $4, false, $5)`,
        [
          webhook.id,
          eventType,
          JSON.stringify(fullPayload),
          duration,
          error.message,
        ]
      );

      // If retries remain, wait before retrying
      if (attempt < maxAttempts) {
        await new Promise((resolve) => setTimeout(resolve, 1000 * attempt));
      }
    }
  }
}
