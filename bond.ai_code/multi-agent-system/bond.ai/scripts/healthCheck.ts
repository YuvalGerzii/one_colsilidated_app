#!/usr/bin/env ts-node

/**
 * Bond.AI Health Check Script
 *
 * Verifies all system components are working:
 * - Database connectivity
 * - Redis connectivity
 * - API endpoints
 * - Services initialization
 */

import { Pool } from 'pg';
import Redis from 'ioredis';
import axios from 'axios';
import { config } from 'dotenv';

config();

const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  cyan: '\x1b[36m',
  bright: '\x1b[1m'
};

function log(message: string, color: keyof typeof colors = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

async function checkDatabase(): Promise<boolean> {
  const pool = new Pool({
    host: process.env.DB_HOST || 'localhost',
    port: parseInt(process.env.DB_PORT || '5432'),
    database: process.env.DB_NAME || 'bondai',
    user: process.env.DB_USER || 'postgres',
    password: process.env.DB_PASSWORD || 'postgres'
  });

  try {
    const result = await pool.query('SELECT NOW()');
    log('✓ PostgreSQL connected', 'green');

    // Check required tables
    const tables = [
      'users', 'user_profiles', 'agents', 'match_candidates',
      'negotiations', 'agreements', 'conversations', 'messages',
      'connections', 'contacts', 'embeddings', 'search_index'
    ];

    for (const table of tables) {
      const tableResult = await pool.query(
        `SELECT EXISTS (
           SELECT FROM information_schema.tables
           WHERE table_name = $1
         )`,
        [table]
      );

      if (tableResult.rows[0].exists) {
        log(`  ✓ Table '${table}' exists`, 'green');
      } else {
        log(`  ✗ Table '${table}' missing`, 'red');
        return false;
      }
    }

    await pool.end();
    return true;
  } catch (error: any) {
    log(`✗ PostgreSQL error: ${error.message}`, 'red');
    await pool.end();
    return false;
  }
}

async function checkRedis(): Promise<boolean> {
  const redis = new Redis({
    host: process.env.REDIS_HOST || 'localhost',
    port: parseInt(process.env.REDIS_PORT || '6379')
  });

  try {
    await redis.ping();
    log('✓ Redis connected', 'green');

    // Test set/get
    await redis.set('health_check', 'ok');
    const value = await redis.get('health_check');

    if (value === 'ok') {
      log('  ✓ Redis read/write working', 'green');
    } else {
      log('  ✗ Redis read/write failed', 'red');
      return false;
    }

    await redis.del('health_check');
    await redis.quit();
    return true;
  } catch (error: any) {
    log(`✗ Redis error: ${error.message}`, 'red');
    await redis.quit();
    return false;
  }
}

async function checkAPI(): Promise<boolean> {
  const baseUrl = process.env.API_URL || 'http://localhost:3000';

  try {
    // Check health endpoint
    const healthResponse = await axios.get(`${baseUrl}/health`);

    if (healthResponse.status === 200) {
      log('✓ API server responding', 'green');
      log(`  Status: ${healthResponse.data.status}`, 'cyan');

      if (healthResponse.data.database) {
        log(`  Database: ${healthResponse.data.database.postgres ? 'OK' : 'Error'}`, 'cyan');
        log(`  Redis: ${healthResponse.data.database.redis ? 'OK' : 'Error'}`, 'cyan');
      }
    } else {
      log(`✗ API server returned status ${healthResponse.status}`, 'red');
      return false;
    }

    return true;
  } catch (error: any) {
    if (error.code === 'ECONNREFUSED') {
      log('✗ API server not running', 'red');
      log('  Start with: npm run dev', 'yellow');
    } else {
      log(`✗ API error: ${error.message}`, 'red');
    }
    return false;
  }
}

async function checkExtensions(): Promise<boolean> {
  const pool = new Pool({
    host: process.env.DB_HOST || 'localhost',
    port: parseInt(process.env.DB_PORT || '5432'),
    database: process.env.DB_NAME || 'bondai',
    user: process.env.DB_USER || 'postgres',
    password: process.env.DB_PASSWORD || 'postgres'
  });

  try {
    const extensions = ['pg_trgm', 'vector'];

    for (const ext of extensions) {
      const result = await pool.query(
        `SELECT EXISTS (
           SELECT FROM pg_extension
           WHERE extname = $1
         )`,
        [ext]
      );

      if (result.rows[0].exists) {
        log(`  ✓ Extension '${ext}' installed`, 'green');
      } else {
        log(`  ✗ Extension '${ext}' missing`, 'red');
        log(`    Install with: CREATE EXTENSION IF NOT EXISTS ${ext};`, 'yellow');
        return false;
      }
    }

    await pool.end();
    return true;
  } catch (error: any) {
    log(`✗ Extension check error: ${error.message}`, 'red');
    await pool.end();
    return false;
  }
}

async function runHealthCheck() {
  log('\n' + '='.repeat(60), 'bright');
  log('Bond.AI Health Check', 'bright');
  log('='.repeat(60) + '\n', 'bright');

  const results = {
    database: false,
    redis: false,
    api: false,
    extensions: false
  };

  log('Checking PostgreSQL...', 'cyan');
  results.database = await checkDatabase();

  log('\nChecking PostgreSQL Extensions...', 'cyan');
  results.extensions = await checkExtensions();

  log('\nChecking Redis...', 'cyan');
  results.redis = await checkRedis();

  log('\nChecking API Server...', 'cyan');
  results.api = await checkAPI();

  // Summary
  log('\n' + '='.repeat(60), 'bright');
  log('Health Check Summary', 'bright');
  log('='.repeat(60), 'bright');

  const allPassed = Object.values(results).every(r => r === true);

  if (allPassed) {
    log('\n✅ All checks passed! System is healthy.', 'green');
  } else {
    log('\n⚠️  Some checks failed:', 'yellow');

    Object.entries(results).forEach(([component, passed]) => {
      log(`  ${component}: ${passed ? '✓ OK' : '✗ Failed'}`, passed ? 'green' : 'red');
    });

    log('\nPlease fix the issues above before running the system.', 'yellow');
  }

  log('');
  process.exit(allPassed ? 0 : 1);
}

if (require.main === module) {
  runHealthCheck().catch(error => {
    console.error('Fatal error:', error);
    process.exit(1);
  });
}

export { runHealthCheck };
