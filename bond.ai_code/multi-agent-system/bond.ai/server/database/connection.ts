/**
 * Database Connection Manager
 * PostgreSQL connection using pg library
 */

import { Pool, PoolClient, QueryResult } from 'pg';
import Redis from 'ioredis';

interface DatabaseConfig {
  host: string;
  port: number;
  database: string;
  user: string;
  password: string;
  max?: number;
  idleTimeoutMillis?: number;
  connectionTimeoutMillis?: number;
}

interface RedisConfig {
  host: string;
  port: number;
  password?: string;
  db?: number;
}

/**
 * Database connection pool
 */
export class Database {
  private pool: Pool;
  private redis: Redis;
  private static instance: Database;

  private constructor(dbConfig: DatabaseConfig, redisConfig: RedisConfig) {
    // PostgreSQL connection pool
    this.pool = new Pool({
      host: dbConfig.host,
      port: dbConfig.port,
      database: dbConfig.database,
      user: dbConfig.user,
      password: dbConfig.password,
      max: dbConfig.max || 20,
      idleTimeoutMillis: dbConfig.idleTimeoutMillis || 30000,
      connectionTimeoutMillis: dbConfig.connectionTimeoutMillis || 10000,
    });

    // Redis connection
    this.redis = new Redis({
      host: redisConfig.host,
      port: redisConfig.port,
      password: redisConfig.password,
      db: redisConfig.db || 0,
      retryStrategy: (times) => {
        const delay = Math.min(times * 50, 2000);
        return delay;
      },
    });

    this.setupEventHandlers();
  }

  /**
   * Get singleton instance
   */
  static getInstance(dbConfig?: DatabaseConfig, redisConfig?: RedisConfig): Database {
    if (!Database.instance) {
      if (!dbConfig || !redisConfig) {
        throw new Error('Database and Redis config required for first initialization');
      }
      Database.instance = new Database(dbConfig, redisConfig);
    }
    return Database.instance;
  }

  /**
   * Setup event handlers
   */
  private setupEventHandlers(): void {
    this.pool.on('error', (err) => {
      console.error('Unexpected error on idle client', err);
    });

    this.pool.on('connect', () => {
      console.log('PostgreSQL client connected');
    });

    this.redis.on('error', (err) => {
      console.error('Redis connection error:', err);
    });

    this.redis.on('connect', () => {
      console.log('Redis client connected');
    });
  }

  /**
   * Execute query
   */
  async query<T = any>(text: string, params?: any[]): Promise<QueryResult<T>> {
    const start = Date.now();
    const result = await this.pool.query<T>(text, params);
    const duration = Date.now() - start;

    if (duration > 1000) {
      console.warn('Slow query detected:', { text, duration });
    }

    return result;
  }

  /**
   * Execute query with single row result
   */
  async queryOne<T = any>(text: string, params?: any[]): Promise<T | null> {
    const result = await this.query<T>(text, params);
    return result.rows[0] || null;
  }

  /**
   * Execute query with multiple rows result
   */
  async queryMany<T = any>(text: string, params?: any[]): Promise<T[]> {
    const result = await this.query<T>(text, params);
    return result.rows;
  }

  /**
   * Get client for transaction
   */
  async getClient(): Promise<PoolClient> {
    return await this.pool.connect();
  }

  /**
   * Execute transaction
   */
  async transaction<T>(callback: (client: PoolClient) => Promise<T>): Promise<T> {
    const client = await this.getClient();

    try {
      await client.query('BEGIN');
      const result = await callback(client);
      await client.query('COMMIT');
      return result;
    } catch (error) {
      await client.query('ROLLBACK');
      throw error;
    } finally {
      client.release();
    }
  }

  /**
   * Cache helpers
   */
  async getCache(key: string): Promise<string | null> {
    return await this.redis.get(key);
  }

  async getCacheJSON<T>(key: string): Promise<T | null> {
    const data = await this.redis.get(key);
    return data ? JSON.parse(data) : null;
  }

  async setCache(key: string, value: string, ttlSeconds?: number): Promise<void> {
    if (ttlSeconds) {
      await this.redis.setex(key, ttlSeconds, value);
    } else {
      await this.redis.set(key, value);
    }
  }

  async setCacheJSON<T>(key: string, value: T, ttlSeconds?: number): Promise<void> {
    await this.setCache(key, JSON.stringify(value), ttlSeconds);
  }

  async deleteCache(key: string): Promise<void> {
    await this.redis.del(key);
  }

  async deleteCachePattern(pattern: string): Promise<void> {
    const keys = await this.redis.keys(pattern);
    if (keys.length > 0) {
      await this.redis.del(...keys);
    }
  }

  /**
   * Close connections
   */
  async close(): Promise<void> {
    await this.pool.end();
    await this.redis.quit();
  }

  /**
   * Health check
   */
  async healthCheck(): Promise<{ postgres: boolean; redis: boolean }> {
    let postgresHealthy = false;
    let redisHealthy = false;

    try {
      await this.query('SELECT 1');
      postgresHealthy = true;
    } catch (error) {
      console.error('PostgreSQL health check failed:', error);
    }

    try {
      await this.redis.ping();
      redisHealthy = true;
    } catch (error) {
      console.error('Redis health check failed:', error);
    }

    return { postgres: postgresHealthy, redis: redisHealthy };
  }

  /**
   * Get pool stats
   */
  getPoolStats() {
    return {
      totalCount: this.pool.totalCount,
      idleCount: this.pool.idleCount,
      waitingCount: this.pool.waitingCount,
    };
  }
}

/**
 * Initialize database
 */
export function initDatabase(dbConfig?: DatabaseConfig, redisConfig?: RedisConfig): Database {
  const defaultDbConfig: DatabaseConfig = {
    host: process.env.DB_HOST || 'localhost',
    port: parseInt(process.env.DB_PORT || '5432'),
    database: process.env.DB_NAME || 'bondai',
    user: process.env.DB_USER || 'bondai_user',
    password: process.env.DB_PASSWORD || 'bondai_password',
    max: parseInt(process.env.DB_POOL_MAX || '20'),
  };

  const defaultRedisConfig: RedisConfig = {
    host: process.env.REDIS_HOST || 'localhost',
    port: parseInt(process.env.REDIS_PORT || '6379'),
    password: process.env.REDIS_PASSWORD,
    db: parseInt(process.env.REDIS_DB || '0'),
  };

  return Database.getInstance(
    dbConfig || defaultDbConfig,
    redisConfig || defaultRedisConfig
  );
}

// Export singleton getter
export const getDb = () => Database.getInstance();
