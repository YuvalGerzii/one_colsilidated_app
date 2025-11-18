import { Request, Response, NextFunction } from 'express';
import { Pool } from 'pg';
import { AuthRequest } from './auth';

// Middleware factory for audit logging
export function createAuditMiddleware(pool: Pool) {
  return async function auditMiddleware(
    req: AuthRequest,
    res: Response,
    next: NextFunction
  ): Promise<void> {
    // Store original end function
    const originalEnd = res.end;
    const startTime = Date.now();

    // Override end to capture response
    (res as any).end = function (chunk: any, ...args: any[]) {
      const duration = Date.now() - startTime;

      // Only log significant actions (not GET requests for static resources)
      const shouldLog =
        req.method !== 'GET' ||
        req.path.includes('/api/') && (
          req.path.includes('/ask') ||
          req.path.includes('/debates') ||
          req.path.includes('/outcomes') ||
          req.path.includes('/decisions')
        );

      if (shouldLog && req.user?.userId) {
        // Log asynchronously to not block response
        logAuditEntry(pool, {
          userId: req.user.userId,
          action: `${req.method} ${req.path}`,
          resourceType: extractResourceType(req.path),
          resourceId: extractResourceId(req),
          ipAddress: req.ip || req.socket.remoteAddress,
          userAgent: req.get('user-agent'),
          metadata: {
            method: req.method,
            path: req.path,
            query: req.query,
            statusCode: res.statusCode,
            duration,
          },
        }).catch(err => console.error('Audit log error:', err));
      }

      // Call original end
      return originalEnd.call(this, chunk, ...args);
    };

    next();
  };
}

// Log audit entry to database
async function logAuditEntry(
  pool: Pool,
  entry: {
    userId: string;
    teamId?: string;
    action: string;
    resourceType?: string;
    resourceId?: string;
    ipAddress?: string;
    userAgent?: string;
    metadata?: any;
  }
): Promise<void> {
  await pool.query(
    `INSERT INTO audit_logs (
      user_id, team_id, action, resource_type, resource_id,
      ip_address, user_agent, metadata
    )
    VALUES ($1, $2, $3, $4, $5, $6::inet, $7, $8)`,
    [
      entry.userId,
      entry.teamId || null,
      entry.action,
      entry.resourceType || null,
      entry.resourceId || null,
      entry.ipAddress || null,
      entry.userAgent || null,
      entry.metadata ? JSON.stringify(entry.metadata) : null,
    ]
  );
}

// Extract resource type from path
function extractResourceType(path: string): string | null {
  const segments = path.split('/').filter(Boolean);

  // Find the API resource segment
  const apiIndex = segments.indexOf('api');
  if (apiIndex !== -1 && segments[apiIndex + 1]) {
    return segments[apiIndex + 1];
  }

  // Fallback to first meaningful segment
  return segments[0] || null;
}

// Extract resource ID from request
function extractResourceId(req: Request): string | null {
  // Check params first
  if (req.params.id) return req.params.id;
  if (req.params.agentKey) return req.params.agentKey;
  if (req.params.memberId) return req.params.memberId;

  // Check body for common ID fields
  if (req.body) {
    if (req.body.conversationId) return req.body.conversationId;
    if (req.body.consultationId) return req.body.consultationId;
    if (req.body.templateId) return req.body.templateId;
  }

  return null;
}

// Manual audit logging function for custom events
export async function logAuditEvent(
  pool: Pool,
  userId: string,
  action: string,
  resourceType?: string,
  resourceId?: string,
  metadata?: any
): Promise<void> {
  await pool.query(
    `INSERT INTO audit_logs (user_id, action, resource_type, resource_id, metadata)
    VALUES ($1, $2, $3, $4, $5)`,
    [userId, action, resourceType, resourceId, metadata ? JSON.stringify(metadata) : null]
  );
}

// Get audit logs for user
export async function getAuditLogs(
  pool: Pool,
  options: {
    userId?: string;
    teamId?: string;
    action?: string;
    resourceType?: string;
    startDate?: string;
    endDate?: string;
    limit?: number;
    offset?: number;
  }
): Promise<any[]> {
  let query = `
    SELECT
      id, user_id as "userId", team_id as "teamId", action,
      resource_type as "resourceType", resource_id as "resourceId",
      ip_address as "ipAddress", user_agent as "userAgent",
      metadata, created_at as "createdAt"
    FROM audit_logs
    WHERE 1=1
  `;

  const params: any[] = [];
  let paramIndex = 1;

  if (options.userId) {
    query += ` AND user_id = $${paramIndex}`;
    params.push(options.userId);
    paramIndex++;
  }

  if (options.teamId) {
    query += ` AND team_id = $${paramIndex}`;
    params.push(options.teamId);
    paramIndex++;
  }

  if (options.action) {
    query += ` AND action LIKE $${paramIndex}`;
    params.push(`%${options.action}%`);
    paramIndex++;
  }

  if (options.resourceType) {
    query += ` AND resource_type = $${paramIndex}`;
    params.push(options.resourceType);
    paramIndex++;
  }

  if (options.startDate) {
    query += ` AND created_at >= $${paramIndex}`;
    params.push(options.startDate);
    paramIndex++;
  }

  if (options.endDate) {
    query += ` AND created_at <= $${paramIndex}`;
    params.push(options.endDate);
    paramIndex++;
  }

  query += ` ORDER BY created_at DESC`;

  if (options.limit) {
    query += ` LIMIT $${paramIndex}`;
    params.push(options.limit);
    paramIndex++;
  }

  if (options.offset) {
    query += ` OFFSET $${paramIndex}`;
    params.push(options.offset);
  }

  const result = await pool.query(query, params);
  return result.rows;
}
