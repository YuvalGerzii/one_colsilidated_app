/**
 * Bond.AI API Server
 * Express + TypeScript + WebSocket
 */

import 'dotenv/config';
import express, { Request, Response, NextFunction } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';
import { createServer } from 'http';
import { Server as SocketIOServer } from 'socket.io';
import { initDatabase, getDb } from './database/connection';
import { authenticateToken, AuthRequest, rateLimit } from './auth/jwt';
import authRoutes from './routes/auth';
import registrationRoutes from './routes/registration';
// import userRoutes from './routes/users'; // TODO: Create this route file
// import matchingRoutes from './routes/matching'; // TODO: Create this route file
// import negotiationRoutes from './routes/negotiations'; // Using createNegotiationRoutes instead
// import linkedinRoutes from './routes/linkedin'; // TODO: Create this route file
import { NotificationService } from './services/NotificationService';
// TODO: Re-enable when dependencies are resolved
// import { createFilterRoutes } from './routes/filters';
// TODO: Re-enable when AdvancedNegotiationStrategies is integrated
// import { createNegotiationRoutes } from './routes/negotiations';
// TODO: Re-enable when AdvancedSearchService ES module issue is resolved
// import { createSearchRoutes } from './routes/search';
// TODO: Re-enable when dependencies are resolved
// import { createInsightsRoutes } from './routes/insights';
// TODO: Re-enable when dependencies are resolved
// import { createAnalyticsRoutes } from './routes/analytics';
import { createHealthRoutes } from './routes/health';
import { DynamicProfileService } from './services/DynamicProfileService';
import { MessagingService } from './services/MessagingService';
// TODO: Re-enable when ES module issue is resolved
// import { AdvancedSearchService } from './services/AdvancedSearchService';

const PORT = process.env.PORT || 3002;
const app = express();
const httpServer = createServer(app);

// Initialize Socket.IO
const io = new SocketIOServer(httpServer, {
  cors: {
    origin: process.env.CORS_ORIGIN || 'http://localhost:5173',
    credentials: true,
  },
});

// Initialize services
const notificationService = new NotificationService(io);
let dynamicProfileService: DynamicProfileService;
let messagingService: MessagingService;
// TODO: Re-enable when ES module issue is resolved
// let searchService: AdvancedSearchService;

// Middleware
app.use(helmet());
app.use(cors({
  origin: process.env.CORS_ORIGIN || 'http://localhost:5173',
  credentials: true,
}));
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));
app.use(morgan('combined'));

// Global rate limiting
app.use(rateLimit(1000, 60000)); // 1000 requests per minute

// Health check
app.get('/health', async (req: Request, res: Response) => {
  try {
    const db = getDb();
    const health = await db.healthCheck();
    const poolStats = db.getPoolStats();

    res.json({
      status: 'ok',
      timestamp: new Date().toISOString(),
      database: health,
      pool: poolStats,
    });
  } catch (error) {
    res.status(503).json({
      status: 'error',
      timestamp: new Date().toISOString(),
      error: 'Service unavailable',
    });
  }
});

// API Routes
app.use('/api/auth', authRoutes);
app.use('/api/registration', registrationRoutes);
// app.use('/api/users', authenticateToken, userRoutes); // TODO: Create users route
// app.use('/api/matching', authenticateToken, matchingRoutes); // TODO: Create matching route
// app.use('/api/linkedin', authenticateToken, linkedinRoutes); // TODO: Create linkedin route

// New feature routes (initialized after database connection)
// These will be registered in the start() function

// WebSocket authentication
io.use(async (socket, next) => {
  try {
    const token = socket.handshake.auth.token;
    if (!token) {
      return next(new Error('Authentication required'));
    }

    // Verify token (implement your JWT verification)
    // const payload = verifyToken(token);
    // socket.data.userId = payload.userId;

    next();
  } catch (error) {
    next(new Error('Invalid token'));
  }
});

// WebSocket connection
io.on('connection', (socket) => {
  console.log('Client connected:', socket.id);

  // Subscribe to user's notifications
  socket.on('subscribe:notifications', (userId: string) => {
    socket.join(`user:${userId}`);
    console.log(`User ${userId} subscribed to notifications`);
  });

  // Subscribe to match updates
  socket.on('subscribe:matches', (userId: string) => {
    socket.join(`matches:${userId}`);
    console.log(`User ${userId} subscribed to matches`);
  });

  // Subscribe to negotiation updates
  socket.on('subscribe:negotiation', (negotiationId: string) => {
    socket.join(`negotiation:${negotiationId}`);
    console.log(`Subscribed to negotiation ${negotiationId}`);
  });

  socket.on('disconnect', () => {
    console.log('Client disconnected:', socket.id);
  });
});

// Error handling middleware
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  console.error('Error:', err);

  if (err.name === 'UnauthorizedError') {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  if (err.name === 'ValidationError') {
    return res.status(400).json({ error: err.message });
  }

  res.status(500).json({
    error: 'Internal server error',
    message: process.env.NODE_ENV === 'development' ? err.message : undefined,
  });
});

// 404 handler
app.use((req: Request, res: Response) => {
  res.status(404).json({ error: 'Not found' });
});

// Start server
async function start() {
  try {
    // Initialize database
    console.log('Initializing database...');
    initDatabase();

    // Test database connection
    const db = getDb();
    const health = await db.healthCheck();
    console.log('Database health:', health);

    if (!health.postgres || !health.redis) {
      throw new Error('Database or Redis connection failed');
    }

    // Initialize new services with database connections
    const { pool, redis } = db;

    // Initialize dynamic profile updates service
    dynamicProfileService = new DynamicProfileService(pool, redis, io);
    console.log('Dynamic Profile Service initialized');

    // Initialize messaging service
    messagingService = new MessagingService(pool, redis, io);
    console.log('Messaging Service initialized');

    // TODO: Re-enable when ES module issue is resolved
    // // Initialize advanced search service
    // searchService = new AdvancedSearchService(pool, redis);
    // console.log('Advanced Search Service initialized');

    // // Perform initial search reindex (async, non-blocking)
    // searchService.reindexAll().catch(error => {
    //   console.error('Initial search reindex failed:', error);
    // });

    // Register new feature routes
    app.use('/api/health', createHealthRoutes(pool, redis));
    // TODO: Re-enable when dependencies are resolved
    // app.use('/api/filters', authenticateToken, createFilterRoutes(pool, redis));
    // TODO: Re-enable when AdvancedNegotiationStrategies is integrated
    // app.use('/api/negotiations', authenticateToken, createNegotiationRoutes(pool, redis));
    // TODO: Re-enable when AdvancedSearchService ES module issue is resolved
    // app.use('/api/search', authenticateToken, createSearchRoutes(pool, redis));
    // TODO: Re-enable when dependencies are resolved
    // app.use('/api/insights', authenticateToken, createInsightsRoutes(pool, redis));
    // TODO: Re-enable when dependencies are resolved
    // app.use('/api/analytics', authenticateToken, createAnalyticsRoutes(pool, redis));
    console.log('Basic routes registered successfully');

    // Start server
    httpServer.listen(PORT, () => {
      console.log(`🚀 Bond.AI API Server running on port ${PORT}`);
      console.log(`   HTTP: http://localhost:${PORT}`);
      console.log(`   WebSocket: ws://localhost:${PORT}`);
      console.log(`   Environment: ${process.env.NODE_ENV || 'development'}`);
    });
  } catch (error) {
    console.error('Failed to start server:', error);
    process.exit(1);
  }
}

// Graceful shutdown
process.on('SIGTERM', async () => {
  console.log('SIGTERM received, shutting down gracefully...');
  httpServer.close(async () => {
    const db = getDb();
    await db.close();
    console.log('Server closed');
    process.exit(0);
  });
});

process.on('SIGINT', async () => {
  console.log('SIGINT received, shutting down gracefully...');
  httpServer.close(async () => {
    const db = getDb();
    await db.close();
    console.log('Server closed');
    process.exit(0);
  });
});

// Start the server
if (require.main === module) {
  start();
}

export { app, io, notificationService };
