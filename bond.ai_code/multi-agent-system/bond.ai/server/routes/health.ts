import express from 'express';
import { Pool } from 'pg';
import Redis from 'ioredis';

/**
 * Health Check API Routes
 *
 * Provides comprehensive system health information:
 * - Basic health status
 * - Detailed component diagnostics
 * - Database schema validation
 * - Service status checks
 */

export function createHealthRoutes(pool: Pool, redis: Redis): express.Router {
  const router = express.Router();

  /**
   * GET /api/health
   * Basic health check - lightweight
   */
  router.get('/', async (req, res) => {
    try {
      // Quick database ping
      const dbStart = Date.now();
      await pool.query('SELECT 1');
      const dbLatency = Date.now() - dbStart;

      // Quick Redis ping
      const redisStart = Date.now();
      await redis.ping();
      const redisLatency = Date.now() - redisStart;

      res.json({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        uptime: process.uptime(),
        database: {
          postgres: true,
          latency: dbLatency
        },
        cache: {
          redis: true,
          latency: redisLatency
        },
        memory: {
          used: process.memoryUsage().heapUsed,
          total: process.memoryUsage().heapTotal,
          external: process.memoryUsage().external
        }
      });
    } catch (error: any) {
      res.status(503).json({
        status: 'unhealthy',
        timestamp: new Date().toISOString(),
        error: error.message
      });
    }
  });

  /**
   * GET /api/health/detailed
   * Comprehensive health diagnostics
   */
  router.get('/detailed', async (req, res) => {
    try {
      const checks = {
        database: await checkDatabase(pool),
        redis: await checkRedis(redis),
        tables: await checkTables(pool),
        extensions: await checkExtensions(pool),
        indices: await checkIndices(pool)
      };

      const allHealthy = Object.values(checks).every(check =>
        typeof check === 'object' && 'healthy' in check ? check.healthy : true
      );

      res.status(allHealthy ? 200 : 503).json({
        status: allHealthy ? 'healthy' : 'degraded',
        timestamp: new Date().toISOString(),
        checks,
        system: {
          uptime: process.uptime(),
          memory: process.memoryUsage(),
          cpu: process.cpuUsage(),
          nodeVersion: process.version,
          platform: process.platform
        }
      });
    } catch (error: any) {
      res.status(503).json({
        status: 'error',
        timestamp: new Date().toISOString(),
        error: error.message
      });
    }
  });

  /**
   * GET /api/health/ready
   * Kubernetes-style readiness probe
   */
  router.get('/ready', async (req, res) => {
    try {
      // Check critical dependencies
      await pool.query('SELECT 1');
      await redis.ping();

      // Check required tables exist
      const requiredTables = ['users', 'user_profiles', 'agents', 'match_candidates'];
      for (const table of requiredTables) {
        const result = await pool.query(
          `SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_name = $1
          )`,
          [table]
        );

        if (!result.rows[0].exists) {
          throw new Error(`Required table '${table}' not found`);
        }
      }

      res.status(200).json({ ready: true });
    } catch (error: any) {
      res.status(503).json({ ready: false, error: error.message });
    }
  });

  /**
   * GET /api/health/live
   * Kubernetes-style liveness probe
   */
  router.get('/live', (req, res) => {
    // Server is alive if it can respond to this request
    res.status(200).json({ alive: true });
  });

  return router;
}

/**
 * Check PostgreSQL database health
 */
async function checkDatabase(pool: Pool): Promise<any> {
  try {
    const start = Date.now();
    const result = await pool.query('SELECT NOW(), version()');
    const latency = Date.now() - start;

    // Get connection pool stats
    const poolStats = {
      total: pool.totalCount,
      idle: pool.idleCount,
      waiting: pool.waitingCount
    };

    return {
      healthy: true,
      latency,
      version: result.rows[0].version,
      serverTime: result.rows[0].now,
      pool: poolStats
    };
  } catch (error: any) {
    return {
      healthy: false,
      error: error.message
    };
  }
}

/**
 * Check Redis health
 */
async function checkRedis(redis: Redis): Promise<any> {
  try {
    const start = Date.now();
    await redis.ping();
    const latency = Date.now() - start;

    // Get Redis info
    const info = await redis.info();
    const lines = info.split('\r\n');
    const version = lines.find(l => l.startsWith('redis_version:'))?.split(':')[1];
    const connectedClients = lines.find(l => l.startsWith('connected_clients:'))?.split(':')[1];
    const usedMemory = lines.find(l => l.startsWith('used_memory_human:'))?.split(':')[1];

    // Test set/get
    const testKey = `health_check_${Date.now()}`;
    await redis.set(testKey, 'test', 'EX', 10);
    const testValue = await redis.get(testKey);
    await redis.del(testKey);

    return {
      healthy: true,
      latency,
      version,
      connectedClients: parseInt(connectedClients || '0'),
      memory: usedMemory,
      readWrite: testValue === 'test'
    };
  } catch (error: any) {
    return {
      healthy: false,
      error: error.message
    };
  }
}

/**
 * Check database tables exist
 */
async function checkTables(pool: Pool): Promise<any> {
  try {
    const requiredTables = [
      'users', 'user_profiles', 'agents', 'match_candidates',
      'negotiations', 'agreements', 'conversations', 'messages',
      'connections', 'contacts', 'embeddings', 'search_index',
      'user_needs', 'user_offerings', 'filter_preferences'
    ];

    const existingTables = [];
    const missingTables = [];

    for (const table of requiredTables) {
      const result = await pool.query(
        `SELECT EXISTS (
          SELECT FROM information_schema.tables
          WHERE table_name = $1
        )`,
        [table]
      );

      if (result.rows[0].exists) {
        existingTables.push(table);
      } else {
        missingTables.push(table);
      }
    }

    return {
      healthy: missingTables.length === 0,
      total: requiredTables.length,
      existing: existingTables.length,
      missing: missingTables.length > 0 ? missingTables : undefined
    };
  } catch (error: any) {
    return {
      healthy: false,
      error: error.message
    };
  }
}

/**
 * Check PostgreSQL extensions
 */
async function checkExtensions(pool: Pool): Promise<any> {
  try {
    const requiredExtensions = ['pg_trgm', 'vector'];
    const installedExtensions = [];
    const missingExtensions = [];

    for (const ext of requiredExtensions) {
      const result = await pool.query(
        `SELECT EXISTS (
          SELECT FROM pg_extension
          WHERE extname = $1
        )`,
        [ext]
      );

      if (result.rows[0].exists) {
        installedExtensions.push(ext);
      } else {
        missingExtensions.push(ext);
      }
    }

    return {
      healthy: missingExtensions.length === 0,
      installed: installedExtensions,
      missing: missingExtensions.length > 0 ? missingExtensions : undefined
    };
  } catch (error: any) {
    return {
      healthy: false,
      error: error.message
    };
  }
}

/**
 * Check database indices for performance
 */
async function checkIndices(pool: Pool): Promise<any> {
  try {
    const result = await pool.query(`
      SELECT
        schemaname,
        tablename,
        indexname,
        indexdef
      FROM pg_indexes
      WHERE schemaname = 'public'
      ORDER BY tablename, indexname
    `);

    const indices = result.rows.reduce((acc: any, row: any) => {
      if (!acc[row.tablename]) {
        acc[row.tablename] = [];
      }
      acc[row.tablename].push(row.indexname);
      return acc;
    }, {});

    return {
      healthy: true,
      totalIndices: result.rows.length,
      byTable: indices
    };
  } catch (error: any) {
    return {
      healthy: false,
      error: error.message
    };
  }
}
