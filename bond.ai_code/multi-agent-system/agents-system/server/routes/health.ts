import { Router, Response, Request } from 'express';
import { Pool } from 'pg';
import Redis from 'ioredis';
import os from 'os';

export function createHealthRoutes(pool: Pool, redis: Redis): Router {
  const router = Router();
  const startTime = Date.now();

  // GET /api/health - Basic health check
  router.get('/', async (req: Request, res: Response) => {
    try {
      const checks = {
        status: 'healthy',
        timestamp: new Date().toISOString(),
        uptime: Math.floor((Date.now() - startTime) / 1000),
        version: process.env.npm_package_version || '2.0.0',
      };

      res.json(checks);
    } catch (error) {
      res.status(500).json({ status: 'unhealthy', error: 'Health check failed' });
    }
  });

  // GET /api/health/detailed - Detailed health check with all services
  router.get('/detailed', async (req: Request, res: Response) => {
    const checks: any = {
      status: 'healthy',
      timestamp: new Date().toISOString(),
      uptime: Math.floor((Date.now() - startTime) / 1000),
      version: process.env.npm_package_version || '2.0.0',
      environment: process.env.NODE_ENV || 'development',
      services: {},
      system: {},
    };

    let hasFailure = false;

    // Database check
    try {
      const dbStart = Date.now();
      const result = await pool.query('SELECT NOW() as time, current_database() as database');
      const dbLatency = Date.now() - dbStart;

      checks.services.database = {
        status: 'healthy',
        latency: dbLatency,
        database: result.rows[0].database,
        timestamp: result.rows[0].time,
      };
    } catch (error: any) {
      hasFailure = true;
      checks.services.database = {
        status: 'unhealthy',
        error: error.message,
      };
    }

    // Redis check
    try {
      const redisStart = Date.now();
      await redis.ping();
      const redisLatency = Date.now() - redisStart;

      const info = await redis.info('memory');
      const usedMemory = info.match(/used_memory_human:(\S+)/)?.[1] || 'unknown';

      checks.services.redis = {
        status: 'healthy',
        latency: redisLatency,
        memory: usedMemory,
      };
    } catch (error: any) {
      hasFailure = true;
      checks.services.redis = {
        status: 'unhealthy',
        error: error.message,
      };
    }

    // System metrics
    checks.system = {
      hostname: os.hostname(),
      platform: os.platform(),
      arch: os.arch(),
      nodeVersion: process.version,
      cpus: os.cpus().length,
      totalMemory: formatBytes(os.totalmem()),
      freeMemory: formatBytes(os.freemem()),
      usedMemory: formatBytes(os.totalmem() - os.freemem()),
      loadAverage: os.loadavg(),
      processMemory: {
        heapUsed: formatBytes(process.memoryUsage().heapUsed),
        heapTotal: formatBytes(process.memoryUsage().heapTotal),
        rss: formatBytes(process.memoryUsage().rss),
      },
    };

    // Overall status
    if (hasFailure) {
      checks.status = 'degraded';
    }

    res.status(hasFailure ? 503 : 200).json(checks);
  });

  // GET /api/health/ready - Readiness check (for k8s)
  router.get('/ready', async (req: Request, res: Response) => {
    try {
      // Check database
      await pool.query('SELECT 1');

      // Check Redis
      await redis.ping();

      res.json({ ready: true });
    } catch (error) {
      res.status(503).json({ ready: false, error: 'Service not ready' });
    }
  });

  // GET /api/health/live - Liveness check (for k8s)
  router.get('/live', (req: Request, res: Response) => {
    res.json({ alive: true });
  });

  // GET /api/health/metrics - Application metrics
  router.get('/metrics', async (req: Request, res: Response) => {
    try {
      // Get database metrics
      const dbMetrics = await pool.query(`
        SELECT
          (SELECT COUNT(*)::int FROM users) as total_users,
          (SELECT COUNT(*)::int FROM agent_conversations WHERE is_active = true) as active_conversations,
          (SELECT COUNT(*)::int FROM agent_consultations) as total_consultations,
          (SELECT COUNT(*)::int FROM agent_consultations WHERE created_at >= NOW() - INTERVAL '24 hours') as consultations_24h,
          (SELECT COUNT(*)::int FROM teams WHERE is_active = true) as active_teams,
          (SELECT COUNT(*)::int FROM agent_debates WHERE completed_at IS NOT NULL) as completed_debates
      `);

      // Get agent usage
      const agentUsage = await pool.query(`
        SELECT
          ba.agent_key, ba.name,
          COUNT(ac.id)::int as total_consultations,
          COUNT(CASE WHEN ac.created_at >= NOW() - INTERVAL '24 hours' THEN 1 END)::int as last_24h
        FROM behavior_agents ba
        LEFT JOIN agent_consultations ac ON ba.id = ac.agent_id
        WHERE ba.is_active = true
        GROUP BY ba.id, ba.agent_key, ba.name
        ORDER BY total_consultations DESC
      `);

      // Connection pool stats
      const poolStats = {
        totalCount: pool.totalCount,
        idleCount: pool.idleCount,
        waitingCount: pool.waitingCount,
      };

      res.json({
        success: true,
        metrics: {
          application: dbMetrics.rows[0],
          agentUsage: agentUsage.rows,
          connectionPool: poolStats,
          process: {
            uptime: process.uptime(),
            memory: process.memoryUsage(),
          },
        },
      });
    } catch (error) {
      console.error('Error getting metrics:', error);
      res.status(500).json({ success: false, error: 'Failed to get metrics' });
    }
  });

  // GET /api/health/agents - Check all agents are available
  router.get('/agents', async (req: Request, res: Response) => {
    try {
      const result = await pool.query(`
        SELECT agent_key, name, is_active
        FROM behavior_agents
        ORDER BY sort_order
      `);

      const agents = result.rows.map(agent => ({
        key: agent.agent_key,
        name: agent.name,
        status: agent.is_active ? 'available' : 'disabled',
      }));

      const allAvailable = agents.every(a => a.status === 'available');

      res.json({
        success: true,
        allAvailable,
        agents,
      });
    } catch (error) {
      console.error('Error checking agents:', error);
      res.status(500).json({ success: false, error: 'Failed to check agents' });
    }
  });

  return router;
}

// Helper function to format bytes
function formatBytes(bytes: number): string {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}
