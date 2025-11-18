/**
 * Utility Helper Functions
 *
 * Common helper functions used across the Bond.AI platform
 */

import { Pool } from 'pg';
import Redis from 'ioredis';

/**
 * Retry a function with exponential backoff
 */
export async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  options: {
    maxRetries?: number;
    initialDelay?: number;
    maxDelay?: number;
    backoffMultiplier?: number;
  } = {}
): Promise<T> {
  const {
    maxRetries = 3,
    initialDelay = 1000,
    maxDelay = 10000,
    backoffMultiplier = 2
  } = options;

  let lastError: Error;
  let delay = initialDelay;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error: any) {
      lastError = error;

      if (attempt < maxRetries) {
        console.log(`Attempt ${attempt + 1} failed, retrying in ${delay}ms...`);
        await sleep(delay);
        delay = Math.min(delay * backoffMultiplier, maxDelay);
      }
    }
  }

  throw lastError!;
}

/**
 * Sleep for a specified duration
 */
export function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Batch process an array in chunks
 */
export async function batchProcess<T, R>(
  items: T[],
  batchSize: number,
  processor: (batch: T[]) => Promise<R[]>
): Promise<R[]> {
  const results: R[] = [];

  for (let i = 0; i < items.length; i += batchSize) {
    const batch = items.slice(i, i + batchSize);
    const batchResults = await processor(batch);
    results.push(...batchResults);
  }

  return results;
}

/**
 * Debounce a function
 */
export function debounce<T extends (...args: any[]) => any>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void {
  let timeoutId: NodeJS.Timeout;

  return function(this: any, ...args: Parameters<T>) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn.apply(this, args), delay);
  };
}

/**
 * Throttle a function
 */
export function throttle<T extends (...args: any[]) => any>(
  fn: T,
  interval: number
): (...args: Parameters<T>) => void {
  let lastCall = 0;

  return function(this: any, ...args: Parameters<T>) {
    const now = Date.now();

    if (now - lastCall >= interval) {
      lastCall = now;
      fn.apply(this, args);
    }
  };
}

/**
 * Generate a random ID
 */
export function generateId(length: number = 16): string {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';

  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }

  return result;
}

/**
 * Calculate percentage
 */
export function percentage(value: number, total: number, decimals: number = 2): number {
  if (total === 0) return 0;
  return parseFloat(((value / total) * 100).toFixed(decimals));
}

/**
 * Clamp a value between min and max
 */
export function clamp(value: number, min: number, max: number): number {
  return Math.min(Math.max(value, min), max);
}

/**
 * Check if value is within range
 */
export function inRange(value: number, min: number, max: number): boolean {
  return value >= min && value <= max;
}

/**
 * Round to decimal places
 */
export function round(value: number, decimals: number = 2): number {
  const multiplier = Math.pow(10, decimals);
  return Math.round(value * multiplier) / multiplier;
}

/**
 * Format number with commas
 */
export function formatNumber(value: number): string {
  return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

/**
 * Parse time range string (e.g., '7d', '30d', '1y')
 */
export function parseTimeRange(range: string): { start: Date; end: Date } {
  const end = new Date();
  const start = new Date();

  const match = range.match(/^(\d+)([hdwmy])$/);
  if (!match) {
    throw new Error(`Invalid time range format: ${range}`);
  }

  const [, value, unit] = match;
  const amount = parseInt(value);

  switch (unit) {
    case 'h': // hours
      start.setHours(start.getHours() - amount);
      break;
    case 'd': // days
      start.setDate(start.getDate() - amount);
      break;
    case 'w': // weeks
      start.setDate(start.getDate() - (amount * 7));
      break;
    case 'm': // months
      start.setMonth(start.getMonth() - amount);
      break;
    case 'y': // years
      start.setFullYear(start.getFullYear() - amount);
      break;
  }

  return { start, end };
}

/**
 * Safe JSON parse with fallback
 */
export function safeJSONParse<T>(json: string, fallback: T): T {
  try {
    return JSON.parse(json);
  } catch {
    return fallback;
  }
}

/**
 * Deep clone an object
 */
export function deepClone<T>(obj: T): T {
  return JSON.parse(JSON.stringify(obj));
}

/**
 * Chunk an array into smaller arrays
 */
export function chunk<T>(array: T[], size: number): T[][] {
  const chunks: T[][] = [];

  for (let i = 0; i < array.length; i += size) {
    chunks.push(array.slice(i, i + size));
  }

  return chunks;
}

/**
 * Get unique values from array
 */
export function unique<T>(array: T[]): T[] {
  return Array.from(new Set(array));
}

/**
 * Group array by key
 */
export function groupBy<T>(
  array: T[],
  keyFn: (item: T) => string | number
): Record<string | number, T[]> {
  return array.reduce((acc, item) => {
    const key = keyFn(item);
    if (!acc[key]) {
      acc[key] = [];
    }
    acc[key].push(item);
    return acc;
  }, {} as Record<string | number, T[]>);
}

/**
 * Cache result of async function with TTL
 */
export function createCachedFunction<T extends (...args: any[]) => Promise<any>>(
  fn: T,
  redis: Redis,
  keyPrefix: string,
  ttlSeconds: number = 300
): T {
  return (async (...args: Parameters<T>) => {
    const cacheKey = `${keyPrefix}:${JSON.stringify(args)}`;

    // Try to get from cache
    const cached = await redis.get(cacheKey);
    if (cached) {
      return JSON.parse(cached);
    }

    // Execute function
    const result = await fn(...args);

    // Store in cache
    await redis.set(cacheKey, JSON.stringify(result), 'EX', ttlSeconds);

    return result;
  }) as T;
}

/**
 * Execute database query with connection retry
 */
export async function queryWithRetry(
  pool: Pool,
  query: string,
  params?: any[]
): Promise<any> {
  return retryWithBackoff(
    async () => {
      const client = await pool.connect();
      try {
        return await client.query(query, params);
      } finally {
        client.release();
      }
    },
    { maxRetries: 3, initialDelay: 500 }
  );
}

/**
 * Create a transaction wrapper
 */
export async function withTransaction<T>(
  pool: Pool,
  callback: (client: any) => Promise<T>
): Promise<T> {
  const client = await pool.connect();

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
 * Validate email format
 */
export function isValidEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

/**
 * Sanitize string for SQL LIKE query
 */
export function sanitizeLikeQuery(input: string): string {
  return input.replace(/[%_]/g, '\\$&');
}

/**
 * Calculate Levenshtein distance (string similarity)
 */
export function levenshteinDistance(str1: string, str2: string): number {
  const matrix: number[][] = [];

  for (let i = 0; i <= str2.length; i++) {
    matrix[i] = [i];
  }

  for (let j = 0; j <= str1.length; j++) {
    matrix[0][j] = j;
  }

  for (let i = 1; i <= str2.length; i++) {
    for (let j = 1; j <= str1.length; j++) {
      if (str2.charAt(i - 1) === str1.charAt(j - 1)) {
        matrix[i][j] = matrix[i - 1][j - 1];
      } else {
        matrix[i][j] = Math.min(
          matrix[i - 1][j - 1] + 1, // substitution
          matrix[i][j - 1] + 1,     // insertion
          matrix[i - 1][j] + 1      // deletion
        );
      }
    }
  }

  return matrix[str2.length][str1.length];
}

/**
 * Calculate string similarity (0-1 scale)
 */
export function stringSimilarity(str1: string, str2: string): number {
  const distance = levenshteinDistance(str1.toLowerCase(), str2.toLowerCase());
  const maxLength = Math.max(str1.length, str2.length);

  if (maxLength === 0) return 1;

  return 1 - (distance / maxLength);
}

/**
 * Async map with concurrency limit
 */
export async function asyncMap<T, R>(
  items: T[],
  mapper: (item: T, index: number) => Promise<R>,
  concurrency: number = 5
): Promise<R[]> {
  const results: R[] = [];
  const executing: Promise<void>[] = [];

  for (let i = 0; i < items.length; i++) {
    const promise = mapper(items[i], i).then(result => {
      results[i] = result;
    });

    executing.push(promise);

    if (executing.length >= concurrency) {
      await Promise.race(executing);
      executing.splice(executing.findIndex(p => p === promise), 1);
    }
  }

  await Promise.all(executing);
  return results;
}

/**
 * Rate limiter
 */
export class RateLimiter {
  private requests: number[] = [];

  constructor(
    private maxRequests: number,
    private windowMs: number
  ) {}

  async acquire(): Promise<void> {
    const now = Date.now();

    // Remove old requests outside the window
    this.requests = this.requests.filter(time => now - time < this.windowMs);

    if (this.requests.length >= this.maxRequests) {
      const oldestRequest = this.requests[0];
      const waitTime = this.windowMs - (now - oldestRequest);
      await sleep(waitTime);
      return this.acquire();
    }

    this.requests.push(now);
  }
}

/**
 * Measure execution time
 */
export async function measureTime<T>(
  label: string,
  fn: () => Promise<T>
): Promise<{ result: T; duration: number }> {
  const start = Date.now();
  const result = await fn();
  const duration = Date.now() - start;

  console.log(`${label} took ${duration}ms`);

  return { result, duration };
}
