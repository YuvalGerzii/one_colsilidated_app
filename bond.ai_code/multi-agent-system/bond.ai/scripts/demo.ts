#!/usr/bin/env ts-node

/**
 * Bond.AI Platform Demo Script
 *
 * Comprehensive demonstration of the platform with 50 users:
 * 1. Seeds 50 diverse users with realistic profiles
 * 2. Creates network connections
 * 3. Runs intelligent matching
 * 4. Initiates negotiations
 * 5. Generates introductions
 * 6. Sends messages
 * 7. Shows analytics and insights
 */

import { Pool } from 'pg';
import Redis from 'ioredis';
import { config } from 'dotenv';
import { generateUsers, seedUsers, seedConnections, cleanSeedData } from '../server/utils/seedData';
import { MatchingEngine } from '../src/matching/MatchingEngine';
import { MultiAgentCoordinator } from '../src/agents/MultiAgentCoordinator';
import { MatchExplanationEngine } from '../server/services/MatchExplanationEngine';
import { SuccessPredictionEngine } from '../server/services/SuccessPredictionEngine';
import { IntroductionGenerator } from '../server/services/IntroductionGenerator';
import { AnalyticsDashboardService } from '../server/services/AnalyticsDashboard';

// Load environment variables
config();

// Database connection
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

// Color codes for console output
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  green: '\x1b[32m',
  blue: '\x1b[34m',
  yellow: '\x1b[33m',
  cyan: '\x1b[36m',
  magenta: '\x1b[35m'
};

function log(message: string, color: keyof typeof colors = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

function logSection(title: string) {
  console.log('\n' + '='.repeat(80));
  log(title, 'bright');
  console.log('='.repeat(80) + '\n');
}

async function runDemo() {
  try {
    logSection('🚀 BOND.AI PLATFORM DEMO');

    // Step 1: Clean and seed data
    logSection('Step 1: Seeding Database with 50 Users');
    await cleanSeedData(pool);

    const users = generateUsers(50);
    log(`Generated ${users.length} diverse users`, 'green');

    const userIdMap = await seedUsers(pool, users);
    log(`✓ Created ${userIdMap.size} users in database`, 'green');

    await seedConnections(pool, userIdMap);
    log('✓ Created network connections', 'green');

    // Step 2: Run matching
    logSection('Step 2: Running Intelligent Matching');

    const matchingEngine = new MatchingEngine({
      maxDegreeOfSeparation: 3,
      minRelationshipStrength: 0.3,
      minCompatibilityScore: 0.6,
      enabledMatchTypes: ['all'],
      priorityWeights: {
        valuePotential: 0.35,
        successProbability: 0.25,
        trustLevel: 0.25,
        timing: 0.15
      }
    });

    const client = await pool.connect();
    try {
      // Get all users
      const usersResult = await client.query(
        `SELECT u.id, u.name, u.email, up.needs, up.offerings
         FROM users u
         JOIN user_profiles up ON u.id = up.user_id
         WHERE u.email LIKE '%@bondai-demo.com'
         LIMIT 10` // Match first 10 users for demo
      );

      let totalMatches = 0;

      for (const user of usersResult.rows) {
        log(`\nFinding matches for ${user.name}...`, 'cyan');

        // Get user's connections
        const connectionsResult = await client.query(
          `SELECT c.name, c.email, conn.trust_level, conn.connection_strength
           FROM connections conn
           JOIN contacts c ON conn.contact_id = c.id
           WHERE conn.user_id = $1`,
          [user.id]
        );

        const contacts = connectionsResult.rows.map(c => ({
          name: c.name,
          email: c.email,
          skills: [],
          needs: [],
          offerings: []
        }));

        // Find matches
        const matches = await matchingEngine.findMatches(
          { ...user, connections: [] },
          contacts,
          []
        );

        log(`  Found ${matches.length} potential matches`, 'green');

        // Store top matches in database
        for (const match of matches.slice(0, 5)) {
          // Get agent IDs
          const agentResult = await client.query(
            `SELECT a1.id as initiator_id, a2.id as target_id
             FROM agents a1
             CROSS JOIN agents a2
             JOIN users u1 ON a1.user_id = u1.id
             JOIN users u2 ON a2.user_id = u2.id
             WHERE u1.id = $1
             AND u2.email = $2`,
            [user.id, match.contact.email]
          );

          if (agentResult.rows.length > 0) {
            const { initiator_id, target_id } = agentResult.rows[0];

            await client.query(
              `INSERT INTO match_candidates (
                initiator_agent_id, agent_id, compatibility_score,
                match_type, match_reasons, status, metadata
              )
              VALUES ($1, $2, $3, $4, $5, 'active', $6)
              ON CONFLICT DO NOTHING`,
              [
                initiator_id,
                target_id,
                match.score,
                match.type,
                JSON.stringify(match.reasons),
                JSON.stringify({
                  trustLevel: 0.5 + Math.random() * 0.4,
                  degreeOfSeparation: 1 + Math.floor(Math.random() * 2)
                })
              ]
            );

            totalMatches++;
          }
        }

        if (matches.length > 0) {
          log(`  Top match: ${matches[0].contact.name} (${(matches[0].score * 100).toFixed(1)}% compatible)`, 'yellow');
        }
      }

      log(`\n✓ Created ${totalMatches} high-quality matches`, 'green');

    } finally {
      client.release();
    }

    // Step 3: Generate explanations and predictions
    logSection('Step 3: AI-Powered Insights');

    const explanationEngine = new MatchExplanationEngine(pool, redis);
    const predictionEngine = new SuccessPredictionEngine(pool, redis);
    const introGenerator = new IntroductionGenerator(pool, redis);

    // Get some matches to analyze
    const matchesResult = await pool.query(
      `SELECT mc.id, mc.compatibility_score,
              u1.name as user1_name, u2.name as user2_name
       FROM match_candidates mc
       JOIN agents a1 ON mc.initiator_agent_id = a1.id
       JOIN agents a2 ON mc.agent_id = a2.id
       JOIN users u1 ON a1.user_id = u1.id
       JOIN users u2 ON a2.user_id = u2.id
       WHERE u1.email LIKE '%@bondai-demo.com'
       ORDER BY mc.compatibility_score DESC
       LIMIT 5`
    );

    for (const match of matchesResult.rows) {
      log(`\nAnalyzing match: ${match.user1_name} ↔ ${match.user2_name}`, 'cyan');

      // Get user ID for match
      const userResult = await pool.query(
        `SELECT a.user_id
         FROM match_candidates mc
         JOIN agents a ON mc.initiator_agent_id = a.id
         WHERE mc.id = $1`,
        [match.id]
      );

      const userId = userResult.rows[0]?.user_id;

      if (userId) {
        try {
          // Generate explanation
          const explanation = await explanationEngine.explainMatch(userId, match.id);
          log(`  Primary reasons: ${explanation.primaryReasons.length}`, 'green');
          if (explanation.primaryReasons.length > 0) {
            log(`    - ${explanation.primaryReasons[0].title}: ${explanation.primaryReasons[0].description}`, 'yellow');
          }

          // Generate prediction
          const prediction = await predictionEngine.predictSuccess(match.id);
          log(`  Success probability: ${(prediction.successProbability * 100).toFixed(1)}%`, 'green');
          log(`  Confidence: ${prediction.confidenceInterval.lower.toFixed(2)} - ${prediction.confidenceInterval.upper.toFixed(2)}`, 'green');

          if (prediction.recommendations.length > 0) {
            log(`  Recommendation: ${prediction.recommendations[0]}`, 'yellow');
          }

          // Generate introduction
          const intro = await introGenerator.generateIntroduction(userId, match.id, 'professional');
          log(`  Generated introduction: "${intro.subject}"`, 'green');

        } catch (error: any) {
          log(`  Error analyzing match: ${error.message}`, 'yellow');
        }
      }
    }

    // Step 4: Start negotiations
    logSection('Step 4: Starting Automated Negotiations');

    const coordinator = new MultiAgentCoordinator();

    // Start 5 negotiations
    const negotiationsStarted = [];

    for (const match of matchesResult.rows.slice(0, 5)) {
      try {
        log(`\nStarting negotiation: ${match.user1_name} ↔ ${match.user2_name}`, 'cyan');

        // Get agents
        const agentsResult = await pool.query(
          `SELECT a1.id as initiator_id, a2.id as target_id
           FROM match_candidates mc
           JOIN agents a1 ON mc.initiator_agent_id = a1.id
           JOIN agents a2 ON mc.agent_id = a2.id
           WHERE mc.id = $1`,
          [match.id]
        );

        if (agentsResult.rows.length > 0) {
          const { initiator_id, target_id } = agentsResult.rows[0];

          // Create negotiation
          const negotiationResult = await pool.query(
            `INSERT INTO negotiations (
              match_id, initiator_agent_id, target_agent_id,
              status, conversation_history, metadata
            )
            VALUES ($1, $2, $3, 'active', '[]'::jsonb, $4)
            RETURNING id`,
            [
              match.id,
              initiator_id,
              target_id,
              JSON.stringify({
                strategy: 'Tit-for-Tat with Forgiveness',
                startedAt: new Date().toISOString()
              })
            ]
          );

          const negotiationId = negotiationResult.rows[0].id;
          negotiationsStarted.push(negotiationId);

          log(`  ✓ Started negotiation ${negotiationId}`, 'green');
        }
      } catch (error: any) {
        log(`  Error starting negotiation: ${error.message}`, 'yellow');
      }
    }

    log(`\n✓ Started ${negotiationsStarted.length} negotiations`, 'green');

    // Step 5: Create some conversations
    logSection('Step 5: Creating Conversations');

    let conversationsCreated = 0;

    for (const match of matchesResult.rows.slice(0, 3)) {
      try {
        // Get user IDs
        const usersResult = await pool.query(
          `SELECT a1.user_id as user1_id, a2.user_id as user2_id
           FROM match_candidates mc
           JOIN agents a1 ON mc.initiator_agent_id = a1.id
           JOIN agents a2 ON mc.agent_id = a2.id
           WHERE mc.id = $1`,
          [match.id]
        );

        if (usersResult.rows.length > 0) {
          const { user1_id, user2_id } = usersResult.rows[0];

          // Create conversation
          const convResult = await pool.query(
            `INSERT INTO conversations (participants, type, match_id)
             VALUES ($1, 'introduction', $2)
             RETURNING id`,
            [[user1_id, user2_id], match.id]
          );

          const conversationId = convResult.rows[0].id;

          // Send introduction message
          await pool.query(
            `INSERT INTO messages (
              conversation_id, sender_id, recipient_id, content, type, status
            )
            VALUES ($1, $2, $3, $4, 'introduction', 'sent')`,
            [
              conversationId,
              user1_id,
              user2_id,
              `Hi! I'm ${match.user1_name}. Bond.AI matched us based on our complementary needs and offerings. I'd love to explore potential collaboration opportunities.`
            ]
          );

          conversationsCreated++;
          log(`Created conversation: ${match.user1_name} → ${match.user2_name}`, 'green');
        }
      } catch (error: any) {
        log(`Error creating conversation: ${error.message}`, 'yellow');
      }
    }

    log(`\n✓ Created ${conversationsCreated} conversations`, 'green');

    // Step 6: Show analytics
    logSection('Step 6: Platform Analytics');

    const analyticsService = new AnalyticsDashboardService(pool, redis);

    // Get a user for analytics
    const analyticsUserResult = await pool.query(
      `SELECT id FROM users WHERE email LIKE '%@bondai-demo.com' LIMIT 1`
    );

    if (analyticsUserResult.rows.length > 0) {
      const userId = analyticsUserResult.rows[0].id;

      try {
        const metrics = await analyticsService.getDashboardMetrics(userId, '30d');

        log('Dashboard Metrics:', 'bright');
        log(`  Total Matches: ${metrics.overview.totalMatches}`, 'cyan');
        log(`  Active Negotiations: ${metrics.overview.activeNegotiations}`, 'cyan');
        log(`  Network Size: ${metrics.overview.networkSize}`, 'cyan');
        log(`  Average Match Score: ${(metrics.overview.averageMatchScore * 100).toFixed(1)}%`, 'cyan');

        if (Object.keys(metrics.matches.byType).length > 0) {
          log('\n  Matches by Type:', 'bright');
          Object.entries(metrics.matches.byType).forEach(([type, count]) => {
            log(`    ${type}: ${count}`, 'yellow');
          });
        }
      } catch (error: any) {
        log(`Error getting analytics: ${error.message}`, 'yellow');
      }
    }

    // Step 7: Summary
    logSection('📊 Demo Summary');

    const summaryResult = await pool.query(
      `SELECT
         (SELECT COUNT(*) FROM users WHERE email LIKE '%@bondai-demo.com') as users,
         (SELECT COUNT(*) FROM match_candidates mc
          JOIN agents a ON mc.initiator_agent_id = a.id
          JOIN users u ON a.user_id = u.id
          WHERE u.email LIKE '%@bondai-demo.com') as matches,
         (SELECT COUNT(*) FROM negotiations n
          JOIN agents a ON n.initiator_agent_id = a.id
          JOIN users u ON a.user_id = u.id
          WHERE u.email LIKE '%@bondai-demo.com') as negotiations,
         (SELECT COUNT(*) FROM conversations c
          WHERE EXISTS (
            SELECT 1 FROM users u
            WHERE u.id = ANY(c.participants)
            AND u.email LIKE '%@bondai-demo.com'
          )) as conversations,
         (SELECT COUNT(*) FROM messages m
          JOIN users u ON m.sender_id = u.id
          WHERE u.email LIKE '%@bondai-demo.com') as messages,
         (SELECT COUNT(*) FROM connections conn
          JOIN users u ON conn.user_id = u.id
          WHERE u.email LIKE '%@bondai-demo.com') as connections`
    );

    const summary = summaryResult.rows[0];

    log(`✅ Users Created: ${summary.users}`, 'green');
    log(`✅ Matches Found: ${summary.matches}`, 'green');
    log(`✅ Negotiations Started: ${summary.negotiations}`, 'green');
    log(`✅ Conversations Created: ${summary.conversations}`, 'green');
    log(`✅ Messages Sent: ${summary.messages}`, 'green');
    log(`✅ Network Connections: ${summary.connections}`, 'green');

    log('\n🎉 Demo completed successfully!', 'bright');
    log('\nYou can now:', 'cyan');
    log('  1. Login with any demo user (password: Demo@1234)', 'yellow');
    log('  2. View matches and insights', 'yellow');
    log('  3. Check analytics dashboard', 'yellow');
    log('  4. Send messages and start negotiations', 'yellow');

    log('\nSample login credentials:', 'cyan');
    const sampleUsers = users.slice(0, 3);
    sampleUsers.forEach(u => {
      log(`  Email: ${u.email} | Password: Demo@1234`, 'yellow');
    });

  } catch (error) {
    console.error('\n❌ Demo failed:', error);
    throw error;
  } finally {
    await pool.end();
    await redis.quit();
  }
}

// Run the demo
if (require.main === module) {
  runDemo().catch(error => {
    console.error('Fatal error:', error);
    process.exit(1);
  });
}

export { runDemo };
