import express, { Application } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import compression from 'compression';
import morgan from 'morgan';
import rateLimit from 'express-rate-limit';
import { createServer } from 'http';
import dotenv from 'dotenv';

// Configuration
import { pool, testConnection, closePool } from '../config/database';
import { redis, testRedisConnection, closeRedis } from '../config/redis';

// Middleware
import { errorHandler, notFoundHandler } from './middleware/errorHandler';
import { createAuditMiddleware } from './middleware/audit';

// Routes
import { createAuthRoutes } from './routes/auth';
import { createAgentRoutes } from './routes/agents';
import { createBoardRoomRoutes } from './routes/boardrooms';
import { createChatbotRoutes } from './routes/chatbot';
import { createAnalyticsRoutes } from './routes/analytics';
import { createTeamRoutes } from './routes/teams';
import { createTemplateRoutes } from './routes/templates';
import { createDebateRoutes } from './routes/debates';
import { createOutcomeRoutes } from './routes/outcomes';
import { createWebhookRoutes } from './routes/webhooks';
import { createNotificationRoutes } from './routes/notifications';
import { createReportRoutes } from './routes/reports';
import { createSearchRoutes } from './routes/search';
import { createRecommendationRoutes } from './routes/recommendations';
import { createHealthRoutes } from './routes/health';

// WebSocket
import { createWebSocketServer } from './websocket';

// Load environment variables
dotenv.config();

const app: Application = express();
const httpServer = createServer(app);
const PORT = process.env.PORT || 4000;
const NODE_ENV = process.env.NODE_ENV || 'development';

// ======================
// Middleware Setup
// ======================

// Security
app.use(helmet());

// CORS
const corsOptions = {
  origin: process.env.CORS_ORIGIN || 'http://localhost:3000',
  credentials: true,
};
app.use(cors(corsOptions));

// Body parsing
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Compression
app.use(compression());

// Logging
if (NODE_ENV === 'development') {
  app.use(morgan('dev'));
} else {
  app.use(morgan('combined'));
}

// Rate limiting
const limiter = rateLimit({
  windowMs: parseInt(process.env.RATE_LIMIT_WINDOW_MS || '900000', 10),
  max: parseInt(process.env.RATE_LIMIT_MAX_REQUESTS || '100', 10),
  message: { success: false, error: 'Too many requests, please try again later' },
  standardHeaders: true,
  legacyHeaders: false,
});
app.use('/api/', limiter);

// Audit logging (after auth is processed)
app.use(createAuditMiddleware(pool));

// ======================
// Routes
// ======================

// Health checks (no auth required)
app.use('/api/health', createHealthRoutes(pool, redis));

// Root health check
app.get('/health', (req, res) => {
  res.json({
    success: true,
    status: 'healthy',
    timestamp: new Date().toISOString(),
    environment: NODE_ENV,
  });
});

// Core API routes
app.use('/api/auth', createAuthRoutes(pool));
app.use('/api/agents', createAgentRoutes(pool));
app.use('/api/boardrooms', createBoardRoomRoutes(pool));
app.use('/api/chatbot', createChatbotRoutes(pool, redis));

// Enhanced API routes
app.use('/api/analytics', createAnalyticsRoutes(pool));
app.use('/api/teams', createTeamRoutes(pool));
app.use('/api/templates', createTemplateRoutes(pool));
app.use('/api/debates', createDebateRoutes(pool, redis));
app.use('/api/outcomes', createOutcomeRoutes(pool));
app.use('/api/webhooks', createWebhookRoutes(pool));
app.use('/api/notifications', createNotificationRoutes(pool));
app.use('/api/reports', createReportRoutes(pool));
app.use('/api/search', createSearchRoutes(pool));
app.use('/api/recommendations', createRecommendationRoutes(pool, redis));

// Root route - API info
app.get('/', (req, res) => {
  res.json({
    success: true,
    message: 'Agents System API v2.0',
    version: '2.0.0',
    documentation: '/api/docs',
    health: '/api/health',
    endpoints: {
      // Core
      auth: '/api/auth',
      agents: '/api/agents',
      boardrooms: '/api/boardrooms',
      chatbot: '/api/chatbot',
      // Enhanced
      analytics: '/api/analytics',
      teams: '/api/teams',
      templates: '/api/templates',
      debates: '/api/debates',
      outcomes: '/api/outcomes',
      webhooks: '/api/webhooks',
      notifications: '/api/notifications',
      reports: '/api/reports',
      search: '/api/search',
      recommendations: '/api/recommendations',
      health: '/api/health',
    },
    features: [
      'Behavior Analysis Agents (8 business leaders)',
      'Board Rooms (8 predefined + custom)',
      'Real-time WebSocket Support',
      'Multi-Agent Debates',
      'Decision Templates (6 pre-built)',
      'Analytics & Insights',
      'Team Collaboration',
      'Outcome Tracking',
      'Webhooks & Integrations',
      'Universal Search',
      'Agent Recommendations',
      'Report Generation',
    ],
  });
});

// ======================
// Error Handling
// ======================

app.use(notFoundHandler);
app.use(errorHandler);

// ======================
// WebSocket Server
// ======================

const io = createWebSocketServer(httpServer, pool, redis);

// ======================
// Server Startup
// ======================

async function startServer(): Promise<void> {
  try {
    console.log('🚀 Starting Agents System Server v2.0...');
    console.log(`📍 Environment: ${NODE_ENV}`);
    console.log(`📍 Port: ${PORT}`);
    console.log('');

    // Test database connection
    const dbConnected = await testConnection();
    if (!dbConnected) {
      throw new Error('Failed to connect to database');
    }

    // Test Redis connection
    const redisConnected = await testRedisConnection();
    if (!redisConnected) {
      console.warn('⚠️  Redis connection failed - caching will be disabled');
    }

    // Start server
    httpServer.listen(PORT, () => {
      console.log('');
      console.log('✅ Agents System Server v2.0 is running');
      console.log(`📡 HTTP API: http://localhost:${PORT}`);
      console.log(`📡 WebSocket: ws://localhost:${PORT}`);
      console.log(`📡 Health: http://localhost:${PORT}/health`);
      console.log('');
      console.log('Core Endpoints:');
      console.log(`  - Auth:            /api/auth`);
      console.log(`  - Agents:          /api/agents`);
      console.log(`  - Board Rooms:     /api/boardrooms`);
      console.log(`  - Chatbot:         /api/chatbot`);
      console.log('');
      console.log('Enhanced Endpoints:');
      console.log(`  - Analytics:       /api/analytics`);
      console.log(`  - Teams:           /api/teams`);
      console.log(`  - Templates:       /api/templates`);
      console.log(`  - Debates:         /api/debates`);
      console.log(`  - Outcomes:        /api/outcomes`);
      console.log(`  - Webhooks:        /api/webhooks`);
      console.log(`  - Notifications:   /api/notifications`);
      console.log(`  - Reports:         /api/reports`);
      console.log(`  - Search:          /api/search`);
      console.log(`  - Recommendations: /api/recommendations`);
      console.log(`  - Health:          /api/health`);
      console.log('');
    });
  } catch (error) {
    console.error('❌ Failed to start server:', error);
    process.exit(1);
  }
}

// ======================
// Graceful Shutdown
// ======================

async function gracefulShutdown(signal: string): Promise<void> {
  console.log(`\n${signal} received. Starting graceful shutdown...`);

  try {
    // Close WebSocket connections
    io.close(() => {
      console.log('WebSocket server closed');
    });

    // Close database pool
    await closePool();

    // Close Redis
    await closeRedis();

    console.log('✅ Graceful shutdown completed');
    process.exit(0);
  } catch (error) {
    console.error('❌ Error during shutdown:', error);
    process.exit(1);
  }
}

process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
process.on('SIGINT', () => gracefulShutdown('SIGINT'));

// Handle unhandled promise rejections
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
});

// Start the server
if (require.main === module) {
  startServer();
}

export default app;
export { io };
