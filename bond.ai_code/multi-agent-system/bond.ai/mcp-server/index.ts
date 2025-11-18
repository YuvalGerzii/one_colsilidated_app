#!/usr/bin/env node

/**
 * Bond.AI MCP Server
 *
 * Model Context Protocol server that provides rich context about users,
 * networks, recommendations, and relationships to AI assistants.
 *
 * Capabilities:
 * - User profile and network data
 * - Real-time recommendation generation
 * - Network analysis and insights
 * - Collaboration predictions
 * - Introduction assistance
 * - Conversation context management
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListResourcesRequestSchema,
  ListToolsRequestSchema,
  ReadResourceRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { Pool } from 'pg';
import Redis from 'ioredis';

// Import agents
import { RecommendationEngine } from '../src/agents/RecommendationEngine';
import { MatchQualityAgent } from '../src/agents/MatchQualityAgent';
import { CollaborationPredictionAgent } from '../src/agents/CollaborationPredictionAgent';
import { CommunityDetectionAgent } from '../src/agents/CommunityDetectionAgent';
import { TemporalAnalysisAgent } from '../src/agents/TemporalAnalysisAgent';
import { IntentRecognitionAgent } from '../src/agents/IntentRecognitionAgent';
import { RelationshipHealthAgent } from '../src/agents/RelationshipHealthAgent';
import { OpportunityDetectionAgent } from '../src/agents/OpportunityDetectionAgent';
import { ConversationIntelligenceAgent } from '../src/agents/ConversationIntelligenceAgent';
import { NetworkIntelligenceAgent } from '../src/agents/NetworkIntelligenceAgent';
import { IntroductionOrchestrationAgent } from '../src/agents/IntroductionOrchestrationAgent';

// Initialize database and Redis
const pool = new Pool({
  connectionString: process.env.DATABASE_URL || 'postgresql://localhost:5432/bondai',
});

const redis = new Redis(process.env.REDIS_URL || 'redis://localhost:6379');

// Initialize all agents
const agents = initializeAgents(pool, redis);

function initializeAgents(pool: Pool, redis: Redis) {
  // Initialize base agents (from previous phases)
  const networkTraversal = new (require('../src/agents/NetworkTraversalAgent').NetworkTraversalAgent)(pool, redis);
  const optimizedCalc = new (require('../src/agents/OptimizedNetworkCalculations').OptimizedNetworkCalculations)(pool, redis);
  const sixDegrees = new (require('../src/agents/SixDegreesAgent').SixDegreesAgent)(pool, redis, networkTraversal);
  const trust = new (require('../src/agents/TrustPropagationAgent').TrustPropagationAgent)(pool, redis);
  const serendipity = new (require('../src/agents/SerendipityAgent').SerendipityAgent)(pool, redis, networkTraversal, optimizedCalc);
  const community = new CommunityDetectionAgent(pool, redis);
  const strength = new (require('../src/agents/ConnectionStrengthAnalyzer').ConnectionStrengthAnalyzer)(pool, redis, optimizedCalc);

  const matchQuality = new MatchQualityAgent(pool, redis, sixDegrees, trust, serendipity, community, strength);
  const collaboration = new CollaborationPredictionAgent(pool, redis, matchQuality, trust);
  const recommendation = new RecommendationEngine(pool, redis, matchQuality, sixDegrees, trust, serendipity, community, strength);
  const temporal = new TemporalAnalysisAgent(pool, redis);

  // Initialize new specialized agents
  const intentRecognition = new IntentRecognitionAgent(pool, redis);
  const relationshipHealth = new RelationshipHealthAgent(pool, redis, trust, temporal);
  const opportunityDetection = new OpportunityDetectionAgent(pool, redis, matchQuality, community, serendipity);
  const conversationIntelligence = new ConversationIntelligenceAgent(pool, redis, intentRecognition);
  const networkIntelligence = new NetworkIntelligenceAgent(pool, redis, community, temporal, strength);
  const introductionOrchestration = new IntroductionOrchestrationAgent(pool, redis, matchQuality, trust, conversationIntelligence);

  return {
    recommendation,
    matchQuality,
    collaboration,
    community,
    temporal,
    intentRecognition,
    relationshipHealth,
    opportunityDetection,
    conversationIntelligence,
    networkIntelligence,
    introductionOrchestration,
  };
}

// Create MCP server
const server = new Server(
  {
    name: 'bond-ai-mcp-server',
    version: '1.0.0',
  },
  {
    capabilities: {
      resources: {},
      tools: {},
    },
  }
);

/**
 * Resource Handlers
 * Provide read-only access to Bond.AI data
 */
server.setRequestHandler(ListResourcesRequestSchema, async () => {
  return {
    resources: [
      {
        uri: 'bondai://user/{userId}/profile',
        name: 'User Profile',
        description: 'Complete user profile including bio, expertise, needs, and offers',
        mimeType: 'application/json',
      },
      {
        uri: 'bondai://user/{userId}/network',
        name: 'User Network',
        description: 'User\'s connections, trust levels, and relationship strengths',
        mimeType: 'application/json',
      },
      {
        uri: 'bondai://user/{userId}/recommendations',
        name: 'User Recommendations',
        description: 'Personalized connection recommendations',
        mimeType: 'application/json',
      },
      {
        uri: 'bondai://user/{userId}/communities',
        name: 'User Communities',
        description: 'Communities the user belongs to and their roles',
        mimeType: 'application/json',
      },
      {
        uri: 'bondai://user/{userId}/trajectory',
        name: 'User Trajectory',
        description: 'Network growth history and predictions',
        mimeType: 'application/json',
      },
      {
        uri: 'bondai://user/{userId}/health',
        name: 'Network Health',
        description: 'Current network health metrics and recommendations',
        mimeType: 'application/json',
      },
      {
        uri: 'bondai://user/{userId}/opportunities',
        name: 'Opportunities',
        description: 'Detected collaboration and introduction opportunities',
        mimeType: 'application/json',
      },
      {
        uri: 'bondai://match/{userId}/{targetId}',
        name: 'Match Analysis',
        description: 'Detailed match quality analysis between two users',
        mimeType: 'application/json',
      },
      {
        uri: 'bondai://conversation/{userId}/context',
        name: 'Conversation Context',
        description: 'Recent conversations and their context',
        mimeType: 'application/json',
      },
    ],
  };
});

server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const uri = request.params.uri;
  const parts = uri.replace('bondai://', '').split('/');

  try {
    if (parts[0] === 'user') {
      const userId = parts[1];
      const resource = parts[2];

      switch (resource) {
        case 'profile':
          return await getUserProfile(userId);
        case 'network':
          return await getUserNetwork(userId);
        case 'recommendations':
          return await getUserRecommendations(userId);
        case 'communities':
          return await getUserCommunities(userId);
        case 'trajectory':
          return await getUserTrajectory(userId);
        case 'health':
          return await getNetworkHealth(userId);
        case 'opportunities':
          return await getOpportunities(userId);
        default:
          throw new Error(`Unknown resource: ${resource}`);
      }
    } else if (parts[0] === 'match') {
      const userId = parts[1];
      const targetId = parts[2];
      return await getMatchAnalysis(userId, targetId);
    } else if (parts[0] === 'conversation') {
      const userId = parts[1];
      return await getConversationContext(userId);
    }

    throw new Error(`Unknown resource type: ${parts[0]}`);
  } catch (error: any) {
    return {
      contents: [{
        uri,
        mimeType: 'application/json',
        text: JSON.stringify({ error: error.message }),
      }],
    };
  }
});

/**
 * Tool Handlers
 * Provide interactive capabilities
 */
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'get_recommendations',
        description: 'Get personalized connection recommendations for a user',
        inputSchema: {
          type: 'object',
          properties: {
            userId: { type: 'string', description: 'User ID' },
            limit: { type: 'number', description: 'Number of recommendations', default: 10 },
            minScore: { type: 'number', description: 'Minimum match score (0-100)', default: 60 },
          },
          required: ['userId'],
        },
      },
      {
        name: 'analyze_match',
        description: 'Analyze match quality between two users',
        inputSchema: {
          type: 'object',
          properties: {
            userId: { type: 'string', description: 'First user ID' },
            targetId: { type: 'string', description: 'Second user ID' },
          },
          required: ['userId', 'targetId'],
        },
      },
      {
        name: 'predict_collaboration',
        description: 'Predict collaboration success between two users',
        inputSchema: {
          type: 'object',
          properties: {
            userId: { type: 'string', description: 'First user ID' },
            targetId: { type: 'string', description: 'Second user ID' },
          },
          required: ['userId', 'targetId'],
        },
      },
      {
        name: 'detect_intent',
        description: 'Detect user intent from a message',
        inputSchema: {
          type: 'object',
          properties: {
            userId: { type: 'string', description: 'User ID' },
            message: { type: 'string', description: 'User message' },
          },
          required: ['userId', 'message'],
        },
      },
      {
        name: 'generate_introduction',
        description: 'Generate a personalized introduction email',
        inputSchema: {
          type: 'object',
          properties: {
            introducerId: { type: 'string', description: 'Person making introduction' },
            person1Id: { type: 'string', description: 'First person to introduce' },
            person2Id: { type: 'string', description: 'Second person to introduce' },
            context: { type: 'string', description: 'Optional context for introduction' },
          },
          required: ['introducerId', 'person1Id', 'person2Id'],
        },
      },
      {
        name: 'detect_opportunities',
        description: 'Detect collaboration opportunities in user network',
        inputSchema: {
          type: 'object',
          properties: {
            userId: { type: 'string', description: 'User ID' },
            type: {
              type: 'string',
              enum: ['collaboration', 'introduction', 'hiring', 'investment', 'all'],
              description: 'Type of opportunity to detect',
            },
          },
          required: ['userId'],
        },
      },
      {
        name: 'analyze_relationship_health',
        description: 'Analyze health of relationships in user network',
        inputSchema: {
          type: 'object',
          properties: {
            userId: { type: 'string', description: 'User ID' },
            targetId: { type: 'string', description: 'Optional specific connection to analyze' },
          },
          required: ['userId'],
        },
      },
      {
        name: 'get_network_insights',
        description: 'Get intelligent insights about user network',
        inputSchema: {
          type: 'object',
          properties: {
            userId: { type: 'string', description: 'User ID' },
            insightType: {
              type: 'string',
              enum: ['gaps', 'opportunities', 'risks', 'strengths', 'all'],
              description: 'Type of insights to generate',
            },
          },
          required: ['userId'],
        },
      },
      {
        name: 'suggest_next_action',
        description: 'Suggest the next best action for user networking',
        inputSchema: {
          type: 'object',
          properties: {
            userId: { type: 'string', description: 'User ID' },
            goal: { type: 'string', description: 'Optional specific goal' },
          },
          required: ['userId'],
        },
      },
      {
        name: 'analyze_conversation',
        description: 'Analyze a conversation for insights and suggestions',
        inputSchema: {
          type: 'object',
          properties: {
            userId: { type: 'string', description: 'User ID' },
            conversationId: { type: 'string', description: 'Conversation ID' },
            messages: {
              type: 'array',
              items: { type: 'object' },
              description: 'Conversation messages',
            },
          },
          required: ['userId', 'messages'],
        },
      },
    ],
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case 'get_recommendations':
        return await handleGetRecommendations(args as any);

      case 'analyze_match':
        return await handleAnalyzeMatch(args as any);

      case 'predict_collaboration':
        return await handlePredictCollaboration(args as any);

      case 'detect_intent':
        return await handleDetectIntent(args as any);

      case 'generate_introduction':
        return await handleGenerateIntroduction(args as any);

      case 'detect_opportunities':
        return await handleDetectOpportunities(args as any);

      case 'analyze_relationship_health':
        return await handleAnalyzeRelationshipHealth(args as any);

      case 'get_network_insights':
        return await handleGetNetworkInsights(args as any);

      case 'suggest_next_action':
        return await handleSuggestNextAction(args as any);

      case 'analyze_conversation':
        return await handleAnalyzeConversation(args as any);

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error: any) {
    return {
      content: [{ type: 'text', text: `Error: ${error.message}` }],
      isError: true,
    };
  }
});

/**
 * Resource Implementation Functions
 */

async function getUserProfile(userId: string) {
  const client = await pool.connect();
  try {
    const result = await client.query(`
      SELECT
        u.id, u.name, u.email, u.industry, u.created_at,
        up.bio, up.expertise_areas, up.needs, up.offers,
        up.location, up.linkedin_url, up.company, up.job_title
      FROM users u
      LEFT JOIN user_profiles up ON u.id = up.user_id
      WHERE u.id = $1
    `, [userId]);

    return {
      contents: [{
        uri: `bondai://user/${userId}/profile`,
        mimeType: 'application/json',
        text: JSON.stringify(result.rows[0] || {}, null, 2),
      }],
    };
  } finally {
    client.release();
  }
}

async function getUserNetwork(userId: string) {
  const data = await agents.networkIntelligence.analyzeNetwork(userId);
  return {
    contents: [{
      uri: `bondai://user/${userId}/network`,
      mimeType: 'application/json',
      text: JSON.stringify(data, null, 2),
    }],
  };
}

async function getUserRecommendations(userId: string) {
  const recommendations = await agents.recommendation.getRecommendations(userId, { limit: 10 });
  return {
    contents: [{
      uri: `bondai://user/${userId}/recommendations`,
      mimeType: 'application/json',
      text: JSON.stringify(recommendations, null, 2),
    }],
  };
}

async function getUserCommunities(userId: string) {
  const overlap = await agents.community.analyzeCommunityOverlap(userId);
  return {
    contents: [{
      uri: `bondai://user/${userId}/communities`,
      mimeType: 'application/json',
      text: JSON.stringify(overlap, null, 2),
    }],
  };
}

async function getUserTrajectory(userId: string) {
  const trajectory = await agents.temporal.analyzeUserTrajectory(userId);
  return {
    contents: [{
      uri: `bondai://user/${userId}/trajectory`,
      mimeType: 'application/json',
      text: JSON.stringify(trajectory, null, 2),
    }],
  };
}

async function getNetworkHealth(userId: string) {
  const health = await agents.temporal.generateHealthReport(userId);
  return {
    contents: [{
      uri: `bondai://user/${userId}/health`,
      mimeType: 'application/json',
      text: JSON.stringify(health, null, 2),
    }],
  };
}

async function getOpportunities(userId: string) {
  const opportunities = await agents.opportunityDetection.detectOpportunities(userId);
  return {
    contents: [{
      uri: `bondai://user/${userId}/opportunities`,
      mimeType: 'application/json',
      text: JSON.stringify(opportunities, null, 2),
    }],
  };
}

async function getMatchAnalysis(userId: string, targetId: string) {
  const match = await agents.matchQuality.calculateMatchQuality(userId, targetId);
  return {
    contents: [{
      uri: `bondai://match/${userId}/${targetId}`,
      mimeType: 'application/json',
      text: JSON.stringify(match, null, 2),
    }],
  };
}

async function getConversationContext(userId: string) {
  const context = await agents.conversationIntelligence.getContext(userId);
  return {
    contents: [{
      uri: `bondai://conversation/${userId}/context`,
      mimeType: 'application/json',
      text: JSON.stringify(context, null, 2),
    }],
  };
}

/**
 * Tool Implementation Functions
 */

async function handleGetRecommendations(args: { userId: string; limit?: number; minScore?: number }) {
  const recommendations = await agents.recommendation.getRecommendations(args.userId, {
    limit: args.limit || 10,
    minScore: args.minScore || 60,
  });

  return {
    content: [{ type: 'text', text: JSON.stringify(recommendations, null, 2) }],
  };
}

async function handleAnalyzeMatch(args: { userId: string; targetId: string }) {
  const match = await agents.matchQuality.calculateMatchQuality(args.userId, args.targetId);
  return {
    content: [{ type: 'text', text: JSON.stringify(match, null, 2) }],
  };
}

async function handlePredictCollaboration(args: { userId: string; targetId: string }) {
  const prediction = await agents.collaboration.predictCollaboration(args.userId, args.targetId);
  return {
    content: [{ type: 'text', text: JSON.stringify(prediction, null, 2) }],
  };
}

async function handleDetectIntent(args: { userId: string; message: string }) {
  const intent = await agents.intentRecognition.detectIntent(args.userId, args.message);
  return {
    content: [{ type: 'text', text: JSON.stringify(intent, null, 2) }],
  };
}

async function handleGenerateIntroduction(args: {
  introducerId: string;
  person1Id: string;
  person2Id: string;
  context?: string;
}) {
  const intro = await agents.introductionOrchestration.generateIntroduction(
    args.introducerId,
    args.person1Id,
    args.person2Id,
    args.context
  );
  return {
    content: [{ type: 'text', text: JSON.stringify(intro, null, 2) }],
  };
}

async function handleDetectOpportunities(args: { userId: string; type?: string }) {
  const opportunities = await agents.opportunityDetection.detectOpportunities(
    args.userId,
    args.type as any
  );
  return {
    content: [{ type: 'text', text: JSON.stringify(opportunities, null, 2) }],
  };
}

async function handleAnalyzeRelationshipHealth(args: { userId: string; targetId?: string }) {
  const health = args.targetId
    ? await agents.relationshipHealth.analyzeRelationship(args.userId, args.targetId)
    : await agents.relationshipHealth.analyzeAllRelationships(args.userId);
  return {
    content: [{ type: 'text', text: JSON.stringify(health, null, 2) }],
  };
}

async function handleGetNetworkInsights(args: { userId: string; insightType: string }) {
  const insights = await agents.networkIntelligence.generateInsights(
    args.userId,
    args.insightType as any
  );
  return {
    content: [{ type: 'text', text: JSON.stringify(insights, null, 2) }],
  };
}

async function handleSuggestNextAction(args: { userId: string; goal?: string }) {
  const action = await agents.networkIntelligence.suggestNextAction(args.userId, args.goal);
  return {
    content: [{ type: 'text', text: JSON.stringify(action, null, 2) }],
  };
}

async function handleAnalyzeConversation(args: {
  userId: string;
  conversationId?: string;
  messages: any[];
}) {
  const analysis = await agents.conversationIntelligence.analyzeConversation(
    args.userId,
    args.messages
  );
  return {
    content: [{ type: 'text', text: JSON.stringify(analysis, null, 2) }],
  };
}

/**
 * Start the server
 */
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('Bond.AI MCP Server running on stdio');
}

main().catch((error) => {
  console.error('Fatal error in main():', error);
  process.exit(1);
});
