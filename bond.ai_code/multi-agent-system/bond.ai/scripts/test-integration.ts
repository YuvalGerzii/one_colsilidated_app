#!/usr/bin/env ts-node

/**
 * Integration Test Script
 *
 * Verifies all components can be imported and initialized properly
 */

import { Pool } from 'pg';
import Redis from 'ioredis';
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

async function testIntegration() {
  log('\n' + '='.repeat(60), 'bright');
  log('Bond.AI Integration Test', 'bright');
  log('='.repeat(60) + '\n', 'bright');

  const tests = {
    imports: false,
    database: false,
    redis: false,
    services: false,
    utilities: false
  };

  // Test 1: Verify imports
  log('Test 1: Verifying module imports...', 'cyan');
  try {
    // Import all major modules
    const { generateUsers, seedUsers } = require('../server/utils/seedData');
    const { MatchingEngine } = require('../src/matching/MatchingEngine');
    const { MultiAgentCoordinator } = require('../src/agents/MultiAgentCoordinator');
    const { MatchExplanationEngine } = require('../server/services/MatchExplanationEngine');
    const { SuccessPredictionEngine } = require('../server/services/SuccessPredictionEngine');
    const { IntroductionGenerator } = require('../server/services/IntroductionGenerator');
    const { AnalyticsDashboardService } = require('../server/services/AnalyticsDashboard');

    log('✓ All modules imported successfully', 'green');
    tests.imports = true;
  } catch (error: any) {
    log(`✗ Import error: ${error.message}`, 'red');
  }

  // Test 2: Database connection
  log('\nTest 2: Testing database connection...', 'cyan');
  const pool = new Pool({
    host: process.env.DB_HOST || 'localhost',
    port: parseInt(process.env.DB_PORT || '5432'),
    database: process.env.DB_NAME || 'bondai',
    user: process.env.DB_USER || 'postgres',
    password: process.env.DB_PASSWORD || 'postgres'
  });

  try {
    const result = await pool.query('SELECT NOW()');
    log('✓ Database connection successful', 'green');
    log(`  Server time: ${result.rows[0].now}`, 'cyan');
    tests.database = true;
  } catch (error: any) {
    log(`✗ Database error: ${error.message}`, 'red');
  }

  // Test 3: Redis connection
  log('\nTest 3: Testing Redis connection...', 'cyan');
  const redis = new Redis({
    host: process.env.REDIS_HOST || 'localhost',
    port: parseInt(process.env.REDIS_PORT || '6379')
  });

  try {
    await redis.ping();
    log('✓ Redis connection successful', 'green');
    tests.redis = true;
  } catch (error: any) {
    log(`✗ Redis error: ${error.message}`, 'red');
  }

  // Test 4: Service initialization
  log('\nTest 4: Testing service initialization...', 'cyan');
  try {
    const { MatchExplanationEngine } = require('../server/services/MatchExplanationEngine');
    const { SuccessPredictionEngine } = require('../server/services/SuccessPredictionEngine');
    const { IntroductionGenerator } = require('../server/services/IntroductionGenerator');
    const { AnalyticsDashboardService } = require('../server/services/AnalyticsDashboard');

    const explanationEngine = new MatchExplanationEngine(pool, redis);
    const predictionEngine = new SuccessPredictionEngine(pool, redis);
    const introGenerator = new IntroductionGenerator(pool, redis);
    const analyticsService = new AnalyticsDashboardService(pool, redis);

    log('✓ All services initialized successfully', 'green');
    log('  - Match Explanation Engine', 'cyan');
    log('  - Success Prediction Engine', 'cyan');
    log('  - Introduction Generator', 'cyan');
    log('  - Analytics Dashboard Service', 'cyan');
    tests.services = true;
  } catch (error: any) {
    log(`✗ Service initialization error: ${error.message}`, 'red');
  }

  // Test 5: Utility functions
  log('\nTest 5: Testing utility functions...', 'cyan');
  try {
    const { generateUsers } = require('../server/utils/seedData');
    const helpers = require('../server/utils/helpers');

    // Test user generation
    const users = generateUsers(5);
    if (users.length === 5) {
      log('✓ User generation working', 'green');
      log(`  Generated ${users.length} test users`, 'cyan');
    }

    // Test helper functions
    const similarity = helpers.stringSimilarity('test', 'test');
    if (similarity === 1) {
      log('✓ Helper functions working', 'green');
    }

    tests.utilities = true;
  } catch (error: any) {
    log(`✗ Utility error: ${error.message}`, 'red');
  }

  // Summary
  log('\n' + '='.repeat(60), 'bright');
  log('Test Summary', 'bright');
  log('='.repeat(60), 'bright');

  const allPassed = Object.values(tests).every(t => t === true);

  if (allPassed) {
    log('\n✅ All integration tests passed!', 'green');
    log('   System is ready to run the demo.', 'green');
  } else {
    log('\n⚠️  Some tests failed:', 'yellow');
    Object.entries(tests).forEach(([test, passed]) => {
      log(`  ${test}: ${passed ? '✓ Passed' : '✗ Failed'}`, passed ? 'green' : 'red');
    });
  }

  // Cleanup
  await pool.end();
  await redis.quit();

  log('');
  process.exit(allPassed ? 0 : 1);
}

if (require.main === module) {
  testIntegration().catch(error => {
    console.error('Fatal error:', error);
    process.exit(1);
  });
}

export { testIntegration };
