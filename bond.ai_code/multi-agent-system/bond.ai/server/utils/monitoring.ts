/**
 * System Monitoring and Logging Utilities
 *
 * Provides comprehensive monitoring, metrics tracking, and logging capabilities
 */

import { Pool } from 'pg';
import Redis from 'ioredis';

export interface SystemMetrics {
  timestamp: Date;
  cpu: NodeJS.CpuUsage;
  memory: NodeJS.MemoryUsage;
  uptime: number;
  eventLoop: {
    delay: number;
  };
}

export interface DatabaseMetrics {
  poolSize: number;
  idleConnections: number;
  waitingClients: number;
  queryCount: number;
  avgQueryTime: number;
  slowQueries: number;
}

export interface CacheMetrics {
  hits: number;
  misses: number;
  hitRate: number;
  memoryUsed: number;
  keyCount: number;
}

/**
 * System Metrics Collector
 */
export class MetricsCollector {
  private queryMetrics: Map<string, { count: number; totalTime: number; slowCount: number }> = new Map();
  private cacheStats = { hits: 0, misses: 0 };

  constructor(
    private pool: Pool,
    private redis: Redis
  ) {
    this.startCollecting();
  }

  /**
   * Get current system metrics
   */
  getSystemMetrics(): SystemMetrics {
    return {
      timestamp: new Date(),
      cpu: process.cpuUsage(),
      memory: process.memoryUsage(),
      uptime: process.uptime(),
      eventLoop: {
        delay: this.measureEventLoopDelay()
      }
    };
  }

  /**
   * Get database metrics
   */
  async getDatabaseMetrics(): Promise<DatabaseMetrics> {
    const poolStats = {
      poolSize: this.pool.totalCount,
      idleConnections: this.pool.idleCount,
      waitingClients: this.pool.waitingCount
    };

    let totalQueries = 0;
    let totalTime = 0;
    let slowQueries = 0;

    for (const [, metrics] of this.queryMetrics) {
      totalQueries += metrics.count;
      totalTime += metrics.totalTime;
      slowQueries += metrics.slowCount;
    }

    return {
      ...poolStats,
      queryCount: totalQueries,
      avgQueryTime: totalQueries > 0 ? totalTime / totalQueries : 0,
      slowQueries
    };
  }

  /**
   * Get cache metrics
   */
  async getCacheMetrics(): Promise<CacheMetrics> {
    const info = await this.redis.info('stats');
    const lines = info.split('\r\n');

    const keyspaceHits = parseInt(
      lines.find(l => l.startsWith('keyspace_hits:'))?.split(':')[1] || '0'
    );
    const keyspaceMisses = parseInt(
      lines.find(l => l.startsWith('keyspace_misses:'))?.split(':')[1] || '0'
    );
    const usedMemory = parseInt(
      lines.find(l => l.startsWith('used_memory:'))?.split(':')[1] || '0'
    );

    const dbInfo = await this.redis.info('keyspace');
    const dbLines = dbInfo.split('\r\n');
    const db0Line = dbLines.find(l => l.startsWith('db0:'));
    const keyCount = db0Line
      ? parseInt(db0Line.match(/keys=(\d+)/)?.[1] || '0')
      : 0;

    const total = keyspaceHits + keyspaceMisses;
    const hitRate = total > 0 ? keyspaceHits / total : 0;

    return {
      hits: keyspaceHits,
      misses: keyspaceMisses,
      hitRate,
      memoryUsed: usedMemory,
      keyCount
    };
  }

  /**
   * Record query execution
   */
  recordQuery(query: string, duration: number, slow: boolean = false): void {
    const normalized = this.normalizeQuery(query);

    if (!this.queryMetrics.has(normalized)) {
      this.queryMetrics.set(normalized, { count: 0, totalTime: 0, slowCount: 0 });
    }

    const metrics = this.queryMetrics.get(normalized)!;
    metrics.count++;
    metrics.totalTime += duration;
    if (slow) {
      metrics.slowCount++;
    }
  }

  /**
   * Record cache hit/miss
   */
  recordCacheHit(hit: boolean): void {
    if (hit) {
      this.cacheStats.hits++;
    } else {
      this.cacheStats.misses++;
    }
  }

  /**
   * Get all metrics summary
   */
  async getAllMetrics(): Promise<{
    system: SystemMetrics;
    database: DatabaseMetrics;
    cache: CacheMetrics;
  }> {
    return {
      system: this.getSystemMetrics(),
      database: await this.getDatabaseMetrics(),
      cache: await this.getCacheMetrics()
    };
  }

  /**
   * Reset metrics
   */
  resetMetrics(): void {
    this.queryMetrics.clear();
    this.cacheStats = { hits: 0, misses: 0 };
  }

  /**
   * Measure event loop delay
   */
  private measureEventLoopDelay(): number {
    const start = process.hrtime.bigint();
    setImmediate(() => {
      const end = process.hrtime.bigint();
      return Number(end - start) / 1e6; // Convert to milliseconds
    });
    return 0; // Placeholder
  }

  /**
   * Normalize SQL query for grouping
   */
  private normalizeQuery(query: string): string {
    // Remove values, keep structure
    return query
      .replace(/\$\d+/g, '$?')
      .replace(/\d+/g, '?')
      .replace(/\s+/g, ' ')
      .trim()
      .substring(0, 100);
  }

  /**
   * Start collecting metrics periodically
   */
  private startCollecting(): void {
    // Log metrics every 60 seconds
    setInterval(() => {
      this.logMetricsSummary();
    }, 60000);
  }

  /**
   * Log metrics summary
   */
  private async logMetricsSummary(): Promise<void> {
    try {
      const metrics = await this.getAllMetrics();

      console.log('\n=== System Metrics ===');
      console.log(`Memory: ${Math.round(metrics.system.memory.heapUsed / 1024 / 1024)}MB / ${Math.round(metrics.system.memory.heapTotal / 1024 / 1024)}MB`);
      console.log(`Uptime: ${Math.round(metrics.system.uptime / 60)} minutes`);

      console.log('\n=== Database Metrics ===');
      console.log(`Pool: ${metrics.database.poolSize} total, ${metrics.database.idleConnections} idle, ${metrics.database.waitingClients} waiting`);
      console.log(`Queries: ${metrics.database.queryCount} total, ${metrics.database.avgQueryTime.toFixed(2)}ms avg, ${metrics.database.slowQueries} slow`);

      console.log('\n=== Cache Metrics ===');
      console.log(`Hit Rate: ${(metrics.cache.hitRate * 100).toFixed(2)}%`);
      console.log(`Keys: ${metrics.cache.keyCount}, Memory: ${Math.round(metrics.cache.memoryUsed / 1024 / 1024)}MB`);
      console.log('=====================\n');
    } catch (error) {
      console.error('Error logging metrics:', error);
    }
  }
}

/**
 * Structured Logger
 */
export enum LogLevel {
  DEBUG = 'DEBUG',
  INFO = 'INFO',
  WARN = 'WARN',
  ERROR = 'ERROR',
  FATAL = 'FATAL'
}

export interface LogEntry {
  timestamp: string;
  level: LogLevel;
  message: string;
  context?: any;
  error?: any;
}

export class Logger {
  constructor(
    private serviceName: string,
    private minLevel: LogLevel = LogLevel.INFO
  ) {}

  debug(message: string, context?: any): void {
    this.log(LogLevel.DEBUG, message, context);
  }

  info(message: string, context?: any): void {
    this.log(LogLevel.INFO, message, context);
  }

  warn(message: string, context?: any): void {
    this.log(LogLevel.WARN, message, context);
  }

  error(message: string, error?: any, context?: any): void {
    this.log(LogLevel.ERROR, message, { ...context, error });
  }

  fatal(message: string, error?: any, context?: any): void {
    this.log(LogLevel.FATAL, message, { ...context, error });
  }

  private log(level: LogLevel, message: string, context?: any): void {
    if (!this.shouldLog(level)) {
      return;
    }

    const entry: LogEntry = {
      timestamp: new Date().toISOString(),
      level,
      message: `[${this.serviceName}] ${message}`,
      context
    };

    const formatted = this.formatEntry(entry);

    switch (level) {
      case LogLevel.DEBUG:
      case LogLevel.INFO:
        console.log(formatted);
        break;
      case LogLevel.WARN:
        console.warn(formatted);
        break;
      case LogLevel.ERROR:
      case LogLevel.FATAL:
        console.error(formatted);
        break;
    }
  }

  private shouldLog(level: LogLevel): boolean {
    const levels = [LogLevel.DEBUG, LogLevel.INFO, LogLevel.WARN, LogLevel.ERROR, LogLevel.FATAL];
    const minIndex = levels.indexOf(this.minLevel);
    const currentIndex = levels.indexOf(level);
    return currentIndex >= minIndex;
  }

  private formatEntry(entry: LogEntry): string {
    const base = `${entry.timestamp} [${entry.level}] ${entry.message}`;

    if (entry.context) {
      return `${base}\n${JSON.stringify(entry.context, null, 2)}`;
    }

    return base;
  }
}

/**
 * Performance Monitor
 */
export class PerformanceMonitor {
  private measurements: Map<string, number[]> = new Map();

  /**
   * Start measuring an operation
   */
  start(operation: string): () => void {
    const startTime = Date.now();

    return () => {
      const duration = Date.now() - startTime;
      this.record(operation, duration);
    };
  }

  /**
   * Record a measurement
   */
  record(operation: string, duration: number): void {
    if (!this.measurements.has(operation)) {
      this.measurements.set(operation, []);
    }

    const measurements = this.measurements.get(operation)!;
    measurements.push(duration);

    // Keep only last 100 measurements
    if (measurements.length > 100) {
      measurements.shift();
    }
  }

  /**
   * Get statistics for an operation
   */
  getStats(operation: string): {
    count: number;
    min: number;
    max: number;
    avg: number;
    p50: number;
    p95: number;
    p99: number;
  } | null {
    const measurements = this.measurements.get(operation);
    if (!measurements || measurements.length === 0) {
      return null;
    }

    const sorted = [...measurements].sort((a, b) => a - b);
    const count = sorted.length;

    return {
      count,
      min: sorted[0],
      max: sorted[count - 1],
      avg: sorted.reduce((a, b) => a + b, 0) / count,
      p50: sorted[Math.floor(count * 0.5)],
      p95: sorted[Math.floor(count * 0.95)],
      p99: sorted[Math.floor(count * 0.99)]
    };
  }

  /**
   * Get all statistics
   */
  getAllStats(): Record<string, any> {
    const stats: Record<string, any> = {};

    for (const operation of this.measurements.keys()) {
      stats[operation] = this.getStats(operation);
    }

    return stats;
  }

  /**
   * Clear measurements
   */
  clear(): void {
    this.measurements.clear();
  }
}

/**
 * Alert Manager
 */
export interface Alert {
  id: string;
  severity: 'info' | 'warning' | 'critical';
  title: string;
  message: string;
  timestamp: Date;
  resolved: boolean;
}

export class AlertManager {
  private alerts: Alert[] = [];
  private subscribers: ((alert: Alert) => void)[] = [];

  /**
   * Create an alert
   */
  alert(
    severity: 'info' | 'warning' | 'critical',
    title: string,
    message: string
  ): Alert {
    const alert: Alert = {
      id: `alert_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      severity,
      title,
      message,
      timestamp: new Date(),
      resolved: false
    };

    this.alerts.push(alert);

    // Notify subscribers
    this.subscribers.forEach(subscriber => subscriber(alert));

    // Auto-resolve info alerts after 1 minute
    if (severity === 'info') {
      setTimeout(() => this.resolve(alert.id), 60000);
    }

    return alert;
  }

  /**
   * Resolve an alert
   */
  resolve(alertId: string): void {
    const alert = this.alerts.find(a => a.id === alertId);
    if (alert) {
      alert.resolved = true;
    }
  }

  /**
   * Get active alerts
   */
  getActiveAlerts(): Alert[] {
    return this.alerts.filter(a => !a.resolved);
  }

  /**
   * Subscribe to alerts
   */
  subscribe(callback: (alert: Alert) => void): () => void {
    this.subscribers.push(callback);

    // Return unsubscribe function
    return () => {
      const index = this.subscribers.indexOf(callback);
      if (index > -1) {
        this.subscribers.splice(index, 1);
      }
    };
  }

  /**
   * Clear resolved alerts
   */
  clearResolved(): void {
    this.alerts = this.alerts.filter(a => !a.resolved);
  }
}

/**
 * Create monitoring singleton
 */
let monitoringInstance: {
  metricsCollector: MetricsCollector;
  logger: Logger;
  performanceMonitor: PerformanceMonitor;
  alertManager: AlertManager;
} | null = null;

export function initializeMonitoring(pool: Pool, redis: Redis) {
  if (!monitoringInstance) {
    monitoringInstance = {
      metricsCollector: new MetricsCollector(pool, redis),
      logger: new Logger('BondAI'),
      performanceMonitor: new PerformanceMonitor(),
      alertManager: new AlertManager()
    };

    // Set up alert handlers
    monitoringInstance.alertManager.subscribe(alert => {
      if (alert.severity === 'critical') {
        console.error(`🚨 CRITICAL ALERT: ${alert.title} - ${alert.message}`);
      } else if (alert.severity === 'warning') {
        console.warn(`⚠️  WARNING: ${alert.title} - ${alert.message}`);
      } else {
        console.log(`ℹ️  INFO: ${alert.title} - ${alert.message}`);
      }
    });
  }

  return monitoringInstance;
}

export function getMonitoring() {
  if (!monitoringInstance) {
    throw new Error('Monitoring not initialized. Call initializeMonitoring() first.');
  }
  return monitoringInstance;
}
