#!/usr/bin/env ts-node

/**
 * Bond.AI Stress Test Script
 *
 * Comprehensive testing with 100+ users including edge cases:
 * - Isolated users (no connections)
 * - Super connectors (100+ connections)
 * - Users with conflicting needs/offerings
 * - Incomplete profiles
 * - Rare industries/locations
 * - Extreme trust levels
 *
 * Tests all advanced agents:
 * - NetworkTraversalAgent
 * - SixDegreesAgent
 * - ConnectionStrengthAnalyzer
 * - MatchingEngine
 *
 * Documents:
 * - Performance metrics
 * - Edge case handling
 * - System flaws
 * - Improvement opportunities
 */

import { Pool } from 'pg';
import Redis from 'ioredis';
import { config } from 'dotenv';
import { generateAdvancedUsers, seedAdvancedUsers, seedAdvancedConnections, cleanAdvancedTestData } from '../server/utils/advancedSeedData';
import { NetworkTraversalAgent } from '../src/agents/NetworkTraversalAgent';
import { SixDegreesAgent } from '../src/agents/SixDegreesAgent';
import { ConnectionStrengthAnalyzer } from '../src/agents/ConnectionStrengthAnalyzer';
import { MatchingEngine } from '../src/matching/MatchingEngine';

config();

const pool = new Pool({
  host: process.env.DB_HOST || 'localhost',
  port: parseInt(process.env.DB_PORT || '5432'),
  database: process.env.DB_NAME || 'bondai',
  user: process.env.DB_USER || 'postgres',
  password: process.env.DB_PASSWORD || 'postgres'
});

const redis = new Redis({
  host: process.env.REDIS_HOST || 'localhost',
  port: parseInt(process.env.REDIS_PORT || '6379')
});

const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  green: '\x1b[32m',
  blue: '\x1b[34m',
  yellow: '\x1b[33m',
  red: '\x1b[31m',
  cyan: '\x1b[36m',
  magenta: '\x1b[35m'
};

function log(message: string, color: keyof typeof colors = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

function section(title: string) {
  log('\n' + '='.repeat(80), 'bright');
  log(title, 'bright');
  log('='.repeat(80), 'bright');
}

interface TestResult {
  testName: string;
  passed: boolean;
  duration: number;
  details?: any;
  error?: string;
}

interface Issue {
  severity: 'critical' | 'high' | 'medium' | 'low';
  category: string;
  description: string;
  impact: string;
  recommendation: string;
}

const testResults: TestResult[] = [];
const issues: Issue[] = [];

async function measureTime<T>(
  testName: string,
  fn: () => Promise<T>
): Promise<{ result: T; duration: number }> {
  const start = Date.now();
  try {
    const result = await fn();
    const duration = Date.now() - start;

    testResults.push({
      testName,
      passed: true,
      duration
    });

    return { result, duration };
  } catch (error: any) {
    const duration = Date.now() - start;

    testResults.push({
      testName,
      passed: false,
      duration,
      error: error.message
    });

    throw error;
  }
}

async function runStressTest() {
  log('\n' + '🔥 BOND.AI STRESS TEST 🔥', 'bright');
  log('Testing with 100+ users including edge cases\n', 'cyan');

  const startTime = Date.now();

  // =========================================================================
  // STEP 1: Data Generation and Seeding
  // =========================================================================
  section('Step 1: Data Generation (100 Users with Edge Cases)');

  const { result: users } = await measureTime('Generate 100 users', async () => {
    return generateAdvancedUsers(100);
  });

  log(`\n✓ Generated ${users.length} users`, 'green');
  log(`  - Isolated users: ${users.filter(u => u.connectionStrategy === 'isolated').length}`, 'cyan');
  log(`  - Super connectors: ${users.filter(u => u.connectionStrategy === 'super_connector').length}`, 'cyan');
  log(`  - Selective connectors: ${users.filter(u => u.connectionStrategy === 'selective').length}`, 'cyan');
  log(`  - Normal users: ${users.filter(u => u.connectionStrategy === 'normal').length}`, 'cyan');
  log(`  - Users with no needs: ${users.filter(u => u.needs.length === 0).length}`, 'yellow');
  log(`  - Users with no offerings: ${users.filter(u => u.offerings.length === 0).length}`, 'yellow');
  log(`  - Users with empty bio: ${users.filter(u => !u.bio).length}`, 'yellow');

  // Clean existing test data
  await cleanAdvancedTestData(pool);

  // Seed users
  const { result: userIdMap } = await measureTime('Seed 100 users to database', async () => {
    return seedAdvancedUsers(pool, users);
  });

  // Seed connections
  await measureTime('Create advanced connections', async () => {
    return seedAdvancedConnections(pool, userIdMap, users);
  });

  // =========================================================================
  // STEP 2: Network Traversal Agent Tests
  // =========================================================================
  section('Step 2: Network Traversal Agent Tests');

  const traversalAgent = new NetworkTraversalAgent(pool, redis);

  // Test 2.1: Shortest Path - Normal Case
  log('\nTest 2.1: Shortest Path (Normal Users)', 'cyan');
  const normalUsers = Array.from(userIdMap.values()).filter((_, i) => i >= 25 && i < 50);

  if (normalUsers.length >= 2) {
    const { result: shortestPath, duration } = await measureTime(
      'Find shortest path between normal users',
      async () => traversalAgent.findShortestPath(normalUsers[0], normalUsers[1])
    );

    if (shortestPath) {
      log(`  ✓ Found path with ${shortestPath.length} degrees in ${duration}ms`, 'green');
      log(`    Quality: ${(shortestPath.quality * 100).toFixed(1)}%`, 'cyan');
      log(`    Average trust: ${(shortestPath.averageTrust * 100).toFixed(1)}%`, 'cyan');
    } else {
      log(`  ⚠️  No path found between normal users`, 'yellow');
      issues.push({
        severity: 'medium',
        category: 'Network Connectivity',
        description: 'Normal users not connected',
        impact: 'Limits platform utility for typical users',
        recommendation: 'Improve connection seeding strategy or suggest connections'
      });
    }
  }

  // Test 2.2: Shortest Path - Isolated User
  log('\nTest 2.2: Shortest Path (Isolated User)', 'cyan');
  const isolatedUsers = Array.from(userIdMap.entries())
    .filter(([email]) => users.find(u => u.email === email)?.connectionStrategy === 'isolated')
    .map(([, id]) => id);

  if (isolatedUsers.length > 0 && normalUsers.length > 0) {
    const { result: isolatedPath } = await measureTime(
      'Find path to isolated user',
      async () => traversalAgent.findShortestPath(normalUsers[0], isolatedUsers[0])
    );

    if (isolatedPath === null) {
      log(`  ✓ Correctly identified isolated user (no path)`, 'green');
    } else {
      log(`  ✗ Isolated user has connections (unexpected)`, 'red');
      issues.push({
        severity: 'low',
        category: 'Data Integrity',
        description: 'Isolated user has unexpected connections',
        impact: 'Edge case not properly isolated',
        recommendation: 'Review connection seeding logic for isolated users'
      });
    }
  }

  // Test 2.3: Network Statistics
  log('\nTest 2.3: Network Statistics', 'cyan');
  const { result: networkStats, duration: statsTime } = await measureTime(
    'Calculate network statistics',
    async () => traversalAgent.getNetworkStatistics()
  );

  log(`  ✓ Calculated statistics in ${statsTime}ms`, 'green');
  log(`    Total users: ${networkStats.totalUsers}`, 'cyan');
  log(`    Total connections: ${networkStats.totalConnections}`, 'cyan');
  log(`    Average degree: ${networkStats.averageDegree.toFixed(2)}`, 'cyan');
  log(`    Network diameter: ${networkStats.diameter}`, 'cyan');
  log(`    Clustering coefficient: ${networkStats.clusteringCoefficient.toFixed(3)}`, 'cyan');
  log(`    Isolated users: ${networkStats.isolatedUsers}`, networkStats.isolatedUsers > 10 ? 'yellow' : 'cyan');

  if (networkStats.isolatedUsers > 10) {
    issues.push({
      severity: 'medium',
      category: 'Network Structure',
      description: `High number of isolated users (${networkStats.isolatedUsers})`,
      impact: 'Many users cannot access network features',
      recommendation: 'Implement onboarding flow to suggest initial connections'
    });
  }

  // Test 2.4: Bridge Nodes
  log('\nTest 2.4: Bridge Node Detection', 'cyan');
  const { result: bridgeNodes, duration: bridgeTime } = await measureTime(
    'Identify bridge nodes',
    async () => traversalAgent.findBridgeNodes(10)
  );

  log(`  ✓ Found ${bridgeNodes.length} bridge nodes in ${bridgeTime}ms`, 'green');
  bridgeNodes.slice(0, 3).forEach((node, i) => {
    log(`    ${i + 1}. ${node.name} (betweenness: ${node.betweenness.toFixed(3)}, degree: ${node.degree})`, 'cyan');
  });

  // =========================================================================
  // STEP 3: Six Degrees Agent Tests
  // =========================================================================
  section('Step 3: Six Degrees of Separation Tests');

  const sixDegreesAgent = new SixDegreesAgent(pool, redis);

  // Test 3.1: Six Degrees Verification
  log('\nTest 3.1: Six Degrees Verification (Random Pairs)', 'cyan');
  const { result: sixDegreesDemo } = await measureTime(
    'Demonstrate six degrees with 20 users',
    async () => sixDegreesAgent.demonstrateSixDegrees(20)
  );

  log(`  ✓ Tested ${sixDegreesDemo.totalPairs} pairs`, 'green');
  log(`    Connected: ${sixDegreesDemo.connectedPairs} (${((sixDegreesDemo.connectedPairs / sixDegreesDemo.totalPairs) * 100).toFixed(1)}%)`, 'cyan');
  log(`    Average degrees: ${sixDegreesDemo.averageDegrees.toFixed(2)}`, 'cyan');
  log(`    Max degrees: ${sixDegreesDemo.maxDegrees}`, 'cyan');
  log(`    Within 6 degrees: ${sixDegreesDemo.within6Degrees} (${((sixDegreesDemo.within6Degrees / Math.max(sixDegreesDemo.connectedPairs, 1)) * 100).toFixed(1)}%)`, 'cyan');
  log(`    Distribution:`, 'cyan');
  Object.entries(sixDegreesDemo.distribution).forEach(([degree, count]) => {
    log(`      ${degree} degrees: ${count} pairs`, 'cyan');
  });

  if (sixDegreesDemo.averageDegrees > 4) {
    issues.push({
      severity: 'medium',
      category: 'Network Efficiency',
      description: `Average degrees (${sixDegreesDemo.averageDegrees.toFixed(2)}) higher than typical social networks (3-4)`,
      impact: 'Users may be harder to connect',
      recommendation: 'Add more strategic connections between clusters'
    });
  }

  // Test 3.2: Super Connectors
  log('\nTest 3.2: Super Connector Identification', 'cyan');
  const { result: superConnectors } = await measureTime(
    'Find super connectors',
    async () => sixDegreesAgent.findSuperConnectors(5)
  );

  log(`  ✓ Found ${superConnectors.length} super connectors`, 'green');
  superConnectors.forEach((connector, i) => {
    log(`    ${i + 1}. ${connector.name}`, 'cyan');
    log(`       Direct connections: ${connector.directConnections}`, 'cyan');
    log(`       Network reach: ${connector.reachability.toFixed(1)}%`, 'cyan');
    log(`       Influence: ${(connector.influence * 100).toFixed(1)}%`, 'cyan');
    log(`       Role: ${connector.role}`, 'cyan');
  });

  // Test 3.3: Introduction Path
  log('\nTest 3.3: Best Introduction Path', 'cyan');
  if (normalUsers.length >= 2) {
    const { result: introPath } = await measureTime(
      'Find best introduction path',
      async () => sixDegreesAgent.findBestIntroductionPath(normalUsers[2], normalUsers[3])
    );

    if (introPath) {
      log(`  ✓ Found introduction path with ${introPath.introducers.length} introducers`, 'green');
      log(`    Success estimate: ${(introPath.estimatedSuccess * 100).toFixed(1)}%`, 'cyan');
      log(`    Recommendation: ${introPath.recommendedApproach}`, 'cyan');
    }
  }

  // =========================================================================
  // STEP 4: Connection Strength Analyzer Tests
  // =========================================================================
  section('Step 4: Connection Strength Analysis Tests');

  const strengthAnalyzer = new ConnectionStrengthAnalyzer(pool, redis);

  // Test 4.1: Centrality Metrics
  log('\nTest 4.1: Centrality Metrics (Super Connector)', 'cyan');
  if (superConnectors.length > 0) {
    const { result: centrality } = await measureTime(
      'Calculate centrality metrics',
      async () => strengthAnalyzer.calculateCentrality(superConnectors[0].userId)
    );

    log(`  ✓ Analyzed ${centrality.userName}`, 'green');
    log(`    Degree centrality: ${centrality.degreeCentrality}`, 'cyan');
    log(`    Normalized degree: ${centrality.normalizedDegree.toFixed(3)}`, 'cyan');
    log(`    Betweenness: ${centrality.betweennessCentrality.toFixed(3)}`, 'cyan');
    log(`    Eigenvector: ${centrality.eigenvectorCentrality.toFixed(3)}`, 'cyan');
    log(`    PageRank: ${centrality.pageRank.toFixed(3)}`, 'cyan');
    log(`    Closeness: ${centrality.closeness.toFixed(3)}`, 'cyan');
    log(`    Role: ${centrality.role}`, 'cyan');
  }

  // Test 4.2: Network Position
  log('\nTest 4.2: Network Position Analysis', 'cyan');
  const sampleUserIds = Array.from(userIdMap.values()).slice(0, 5);

  for (const userId of sampleUserIds.slice(0, 2)) {
    const { result: position } = await measureTime(
      `Analyze network position`,
      async () => strengthAnalyzer.analyzeNetworkPosition(userId)
    );

    log(`  ${position.userName}:`, 'cyan');
    log(`    Position: ${position.position}`, 'cyan');
    log(`    Local cluster: ${position.localClusterSize} users`, 'cyan');
    log(`    Bridging potential: ${(position.bridgingPotential * 100).toFixed(1)}%`, 'cyan');
    log(`    Structural holes: ${(position.structuralHoles * 100).toFixed(1)}%`, 'cyan');
  }

  // Test 4.3: Tie Strength Analysis
  log('\nTest 4.3: Tie Strength (Strong vs Weak Ties)', 'cyan');
  if (sampleUserIds.length >= 1) {
    const { result: strongTies } = await measureTime(
      'Find strong ties',
      async () => strengthAnalyzer.findStrongTies(sampleUserIds[0], 5)
    );

    const { result: weakTies } = await measureTime(
      'Find weak ties',
      async () => strengthAnalyzer.findWeakTies(sampleUserIds[0], 5)
    );

    log(`  Strong ties found: ${strongTies.length}`, 'green');
    strongTies.slice(0, 2).forEach(tie => {
      log(`    Score: ${(tie.score * 100).toFixed(1)}%, Type: ${tie.type}`, 'cyan');
    });

    log(`  Weak ties found: ${weakTies.length}`, 'green');
    weakTies.slice(0, 2).forEach(tie => {
      log(`    Score: ${(tie.score * 100).toFixed(1)}%, Type: ${tie.type}`, 'cyan');
    });
  }

  // =========================================================================
  // STEP 5: Edge Case Testing
  // =========================================================================
  section('Step 5: Edge Case Handling');

  // Test 5.1: Users with no needs
  log('\nTest 5.1: Matching for Users with No Needs', 'cyan');
  const noNeedsUsers = Array.from(userIdMap.entries())
    .filter(([email]) => users.find(u => u.email === email)?.needs.length === 0)
    .map(([, id]) => id);

  if (noNeedsUsers.length > 0) {
    try {
      const matchingEngine = new MatchingEngine(pool, redis);
      const { result: matches } = await measureTime(
        'Match user with no needs',
        async () => matchingEngine.findMatches(noNeedsUsers[0])
      );

      log(`  Found ${matches.length} matches for user with no needs`, matches.length > 0 ? 'green' : 'yellow');

      if (matches.length > 0) {
        log(`    System handled edge case gracefully`, 'green');
      } else {
        issues.push({
          severity: 'low',
          category: 'Matching Algorithm',
          description: 'Users with no needs get no matches',
          impact: 'Reduces engagement for users still exploring',
          recommendation: 'Consider interest-based or network-based matches as fallback'
        });
      }
    } catch (error: any) {
      log(`  ✗ Error: ${error.message}`, 'red');
      issues.push({
        severity: 'high',
        category: 'Error Handling',
        description: 'Matching fails for users with no needs',
        impact: 'System errors for incomplete profiles',
        recommendation: 'Add validation and fallback matching strategies'
      });
    }
  }

  // Test 5.2: Empty bio users
  log('\nTest 5.2: Users with Empty Bios', 'cyan');
  const emptyBioUsers = Array.from(userIdMap.entries())
    .filter(([email]) => !users.find(u => u.email === email)?.bio)
    .map(([, id]) => id);

  if (emptyBioUsers.length > 0) {
    log(`  Found ${emptyBioUsers.length} users with empty bios`, 'yellow');
    issues.push({
      severity: 'low',
      category: 'Data Quality',
      description: 'Users with incomplete profiles',
      impact: 'Lower match quality and trust signals',
      recommendation: 'Prompt users to complete profiles, use defaults for missing data'
    });
  }

  // =========================================================================
  // STEP 6: Performance Analysis
  // =========================================================================
  section('Step 6: Performance Analysis');

  const passedTests = testResults.filter(t => t.passed).length;
  const failedTests = testResults.filter(t => !t.passed).length;
  const avgDuration = testResults.reduce((sum, t) => sum + t.duration, 0) / testResults.length;

  log(`\nTest Results:`, 'cyan');
  log(`  Total tests: ${testResults.length}`, 'cyan');
  log(`  Passed: ${passedTests}`, 'green');
  log(`  Failed: ${failedTests}`, failedTests > 0 ? 'red' : 'green');
  log(`  Average duration: ${avgDuration.toFixed(0)}ms`, 'cyan');

  log(`\nSlowest tests:`, 'yellow');
  const slowestTests = [...testResults]
    .sort((a, b) => b.duration - a.duration)
    .slice(0, 5);

  slowestTests.forEach((test, i) => {
    log(`  ${i + 1}. ${test.testName}: ${test.duration}ms`, 'yellow');

    if (test.duration > 5000) {
      issues.push({
        severity: 'medium',
        category: 'Performance',
        description: `Slow operation: ${test.testName} took ${test.duration}ms`,
        impact: 'May cause timeouts or poor user experience',
        recommendation: 'Optimize algorithm, add caching, or use background processing'
      });
    }
  });

  // =========================================================================
  // STEP 7: Issues and Recommendations
  // =========================================================================
  section('Step 7: Issues and Recommendations');

  if (issues.length === 0) {
    log('\n✅ No issues found! System performing well.', 'green');
  } else {
    log(`\nFound ${issues.length} issues:\n`, 'yellow');

    const groupedIssues = {
      critical: issues.filter(i => i.severity === 'critical'),
      high: issues.filter(i => i.severity === 'high'),
      medium: issues.filter(i => i.severity === 'medium'),
      low: issues.filter(i => i.severity === 'low')
    };

    for (const [severity, severityIssues] of Object.entries(groupedIssues)) {
      if (severityIssues.length > 0) {
        log(`${severity.toUpperCase()} Severity (${severityIssues.length}):`, severity === 'critical' || severity === 'high' ? 'red' : 'yellow');

        severityIssues.forEach((issue, i) => {
          log(`\n${i + 1}. [${issue.category}] ${issue.description}`, 'cyan');
          log(`   Impact: ${issue.impact}`, 'yellow');
          log(`   Recommendation: ${issue.recommendation}`, 'green');
        });
        log('');
      }
    }
  }

  // =========================================================================
  // STEP 8: Summary
  // =========================================================================
  section('Summary');

  const totalDuration = Date.now() - startTime;

  log(`\n📊 Stress Test Complete`, 'bright');
  log(`\nExecution Time: ${(totalDuration / 1000).toFixed(2)}s`, 'cyan');
  log(`\nTest Coverage:`, 'cyan');
  log(`  ✓ Network Traversal Agent`, 'green');
  log(`  ✓ Six Degrees Agent`, 'green');
  log(`  ✓ Connection Strength Analyzer`, 'green');
  log(`  ✓ Edge Case Handling`, 'green');
  log(`  ✓ Performance Monitoring`, 'green');

  log(`\nKey Findings:`, 'cyan');
  log(`  • Network diameter: ${networkStats.diameter} degrees`, 'cyan');
  log(`  • Average path length: ${sixDegreesDemo.averageDegrees.toFixed(2)} degrees`, 'cyan');
  log(`  • Users within 6 degrees: ${((sixDegreesDemo.within6Degrees / Math.max(sixDegreesDemo.connectedPairs, 1)) * 100).toFixed(1)}%`, 'cyan');
  log(`  • Super connectors: ${superConnectors.length} identified`, 'cyan');
  log(`  • Tests passed: ${passedTests}/${testResults.length}`, passedTests === testResults.length ? 'green' : 'yellow');

  log(`\nIssue Severity Breakdown:`, 'cyan');
  log(`  Critical: ${groupedIssues.critical.length}`, groupedIssues.critical.length > 0 ? 'red' : 'green');
  log(`  High: ${groupedIssues.high.length}`, groupedIssues.high.length > 0 ? 'red' : 'green');
  log(`  Medium: ${groupedIssues.medium.length}`, groupedIssues.medium.length > 0 ? 'yellow' : 'green');
  log(`  Low: ${groupedIssues.low.length}`, 'cyan');

  if (failedTests === 0 && groupedIssues.critical.length === 0 && groupedIssues.high.length === 0) {
    log(`\n🎉 System is production-ready!`, 'green');
  } else if (groupedIssues.critical.length > 0) {
    log(`\n⚠️  Critical issues found - address before production`, 'red');
  } else {
    log(`\n✅ System stable with minor improvements needed`, 'yellow');
  }

  log('');
}

async function cleanup() {
  await pool.end();
  await redis.quit();
}

if (require.main === module) {
  runStressTest()
    .then(() => {
      cleanup();
      process.exit(0);
    })
    .catch(error => {
      console.error('Fatal error:', error);
      cleanup();
      process.exit(1);
    });
}

export { runStressTest };
