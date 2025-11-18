import { Server as SocketIOServer, Socket } from 'socket.io';
import { Server as HTTPServer } from 'http';
import jwt from 'jsonwebtoken';
import { Pool } from 'pg';
import Redis from 'ioredis';
import { BehaviorAgentFactory } from '../src/agents/BehaviorAgentFactory';
import { DecisionContext } from '../src/agents/BehaviorAgentTypes';

interface AuthenticatedSocket extends Socket {
  userId?: string;
  email?: string;
}

interface StreamingConsultation {
  conversationId: string;
  question: string;
  agentKeys: string[];
  decisionContext: string;
}

export function createWebSocketServer(
  httpServer: HTTPServer,
  pool: Pool,
  redis: Redis
): SocketIOServer {
  const io = new SocketIOServer(httpServer, {
    cors: {
      origin: process.env.CORS_ORIGIN || 'http://localhost:3000',
      methods: ['GET', 'POST'],
      credentials: true,
    },
    pingTimeout: 60000,
    pingInterval: 25000,
  });

  const factory = new BehaviorAgentFactory(pool, redis);

  // Authentication middleware
  io.use(async (socket: AuthenticatedSocket, next) => {
    try {
      const token = socket.handshake.auth.token || socket.handshake.headers.authorization?.split(' ')[1];

      if (!token) {
        return next(new Error('Authentication required'));
      }

      const secret = process.env.JWT_SECRET || 'your-secret-key';
      const decoded = jwt.verify(token, secret) as { userId: string; email: string };

      socket.userId = decoded.userId;
      socket.email = decoded.email;

      // Track user connection
      await redis.sadd(`user:${decoded.userId}:sockets`, socket.id);
      await redis.set(`socket:${socket.id}:user`, decoded.userId);

      next();
    } catch (error) {
      next(new Error('Invalid authentication token'));
    }
  });

  // Connection handler
  io.on('connection', (socket: AuthenticatedSocket) => {
    console.log(`User ${socket.userId} connected via WebSocket`);

    // Join user's personal room
    socket.join(`user:${socket.userId}`);

    // ===========================
    // Real-time Agent Consultation
    // ===========================

    socket.on('consultation:start', async (data: StreamingConsultation) => {
      try {
        const { conversationId, question, agentKeys, decisionContext } = data;

        if (!conversationId || !question || !agentKeys || agentKeys.length === 0) {
          socket.emit('consultation:error', { error: 'Missing required fields' });
          return;
        }

        // Notify client that consultation started
        socket.emit('consultation:started', {
          conversationId,
          agentCount: agentKeys.length,
          timestamp: new Date().toISOString(),
        });

        // Process each agent
        for (let i = 0; i < agentKeys.length; i++) {
          const agentKey = agentKeys[i];
          const agent = factory.getAgentByName(agentKey);

          if (!agent) {
            socket.emit('consultation:agent:error', {
              agentKey,
              error: 'Agent not found',
            });
            continue;
          }

          // Notify client that agent is thinking
          socket.emit('consultation:agent:thinking', {
            agentKey,
            agentName: agent.profile.name,
            position: i + 1,
            total: agentKeys.length,
          });

          // Get advice
          const advice = await agent.getAdvice(
            question,
            (decisionContext as DecisionContext) || 'GENERAL'
          );

          // Get agent ID for database
          const agentResult = await pool.query(
            'SELECT id FROM behavior_agents WHERE agent_key = $1',
            [agentKey]
          );
          const agentId = agentResult.rows[0]?.id;

          // Save to database
          await pool.query(
            `INSERT INTO agent_messages (
              conversation_id, role, agent_id, content, decision_context, structured_data
            )
            VALUES ($1, 'agent', $2, $3, $4, $5)`,
            [
              conversationId,
              agentId,
              advice.advice,
              decisionContext || 'GENERAL',
              JSON.stringify(advice),
            ]
          );

          // Save consultation
          await pool.query(
            `INSERT INTO agent_consultations (
              user_id, conversation_id, agent_id, question, decision_context,
              advice, confidence_score, success_probability, structured_response
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)`,
            [
              socket.userId,
              conversationId,
              agentId,
              question,
              decisionContext || 'GENERAL',
              advice.advice,
              advice.successProbability,
              advice.successProbability,
              JSON.stringify(advice),
            ]
          );

          // Stream response to client
          socket.emit('consultation:agent:response', {
            agentKey,
            agentName: agent.profile.name,
            advice: advice.advice,
            successProbability: advice.successProbability,
            actionableSteps: advice.actionableSteps,
            potentialRisks: advice.potentialRisks,
            recommendedTimeline: advice.recommendedTimeline,
            position: i + 1,
            total: agentKeys.length,
            isLast: i === agentKeys.length - 1,
          });

          // Small delay between agents for better UX
          if (i < agentKeys.length - 1) {
            await new Promise(resolve => setTimeout(resolve, 500));
          }
        }

        // Consultation complete
        socket.emit('consultation:complete', {
          conversationId,
          agentCount: agentKeys.length,
          timestamp: new Date().toISOString(),
        });

      } catch (error: any) {
        console.error('Consultation error:', error);
        socket.emit('consultation:error', {
          error: error.message || 'Consultation failed',
        });
      }
    });

    // ===========================
    // Real-time Debate
    // ===========================

    socket.on('debate:start', async (data) => {
      try {
        const { conversationId, topic, agentKeys, rounds = 2, decisionContext } = data;

        if (!topic || !agentKeys || agentKeys.length < 2) {
          socket.emit('debate:error', { error: 'Topic and at least 2 agents required' });
          return;
        }

        socket.emit('debate:started', {
          topic,
          agentCount: agentKeys.length,
          rounds,
        });

        const agents = agentKeys.map((key: string) => ({
          key,
          agent: factory.getAgentByName(key)!,
        })).filter(a => a.agent);

        const debateHistory: any[] = [];

        for (let round = 1; round <= rounds; round++) {
          socket.emit('debate:round:start', { round, total: rounds });

          for (const { key, agent } of agents) {
            socket.emit('debate:agent:thinking', {
              agentKey: key,
              agentName: agent.profile.name,
              round,
            });

            // Build context from previous arguments
            let contextualQuestion = topic;
            if (debateHistory.length > 0) {
              const previousArgs = debateHistory
                .map(h => `${h.agentName}: ${h.summary}`)
                .join('\n');
              contextualQuestion = `${topic}\n\nPrevious arguments:\n${previousArgs}\n\nProvide your ${round === rounds ? 'closing' : 'counter-'}arguments:`;
            }

            const advice = await agent.getAdvice(
              contextualQuestion,
              (decisionContext as DecisionContext) || 'GENERAL'
            );

            const argument = {
              agentKey: key,
              agentName: agent.profile.name,
              round,
              content: advice.advice,
              summary: advice.actionableSteps[0] || advice.advice.substring(0, 100),
              confidence: advice.successProbability,
            };

            debateHistory.push(argument);

            socket.emit('debate:agent:argument', argument);

            await new Promise(resolve => setTimeout(resolve, 300));
          }

          socket.emit('debate:round:end', { round });
        }

        socket.emit('debate:complete', {
          topic,
          rounds,
          agentCount: agents.length,
          arguments: debateHistory,
        });

      } catch (error: any) {
        console.error('Debate error:', error);
        socket.emit('debate:error', { error: error.message });
      }
    });

    // ===========================
    // Typing Indicators
    // ===========================

    socket.on('typing:start', (data) => {
      const { conversationId } = data;
      socket.to(`conversation:${conversationId}`).emit('typing:user', {
        userId: socket.userId,
        conversationId,
      });
    });

    socket.on('typing:stop', (data) => {
      const { conversationId } = data;
      socket.to(`conversation:${conversationId}`).emit('typing:stopped', {
        userId: socket.userId,
        conversationId,
      });
    });

    // ===========================
    // Room Management
    // ===========================

    socket.on('conversation:join', (conversationId: string) => {
      socket.join(`conversation:${conversationId}`);
      socket.emit('conversation:joined', { conversationId });
    });

    socket.on('conversation:leave', (conversationId: string) => {
      socket.leave(`conversation:${conversationId}`);
    });

    socket.on('team:join', (teamId: string) => {
      socket.join(`team:${teamId}`);
    });

    // ===========================
    // Presence
    // ===========================

    socket.on('presence:online', async () => {
      await redis.hset(`presence:${socket.userId}`, {
        status: 'online',
        lastSeen: new Date().toISOString(),
        socketId: socket.id,
      });
      io.emit('presence:updated', {
        userId: socket.userId,
        status: 'online',
      });
    });

    socket.on('presence:away', async () => {
      await redis.hset(`presence:${socket.userId}`, {
        status: 'away',
        lastSeen: new Date().toISOString(),
      });
      io.emit('presence:updated', {
        userId: socket.userId,
        status: 'away',
      });
    });

    // ===========================
    // Disconnect
    // ===========================

    socket.on('disconnect', async () => {
      console.log(`User ${socket.userId} disconnected`);

      // Remove from tracking
      await redis.srem(`user:${socket.userId}:sockets`, socket.id);
      await redis.del(`socket:${socket.id}:user`);

      // Check if user has other connections
      const remainingSockets = await redis.scard(`user:${socket.userId}:sockets`);
      if (remainingSockets === 0) {
        await redis.hset(`presence:${socket.userId}`, {
          status: 'offline',
          lastSeen: new Date().toISOString(),
        });
        io.emit('presence:updated', {
          userId: socket.userId,
          status: 'offline',
        });
      }
    });
  });

  return io;
}

// Helper to send notifications to specific user
export async function sendUserNotification(
  io: SocketIOServer,
  userId: string,
  notification: {
    type: string;
    title: string;
    message: string;
    data?: any;
  }
): Promise<void> {
  io.to(`user:${userId}`).emit('notification', {
    ...notification,
    timestamp: new Date().toISOString(),
  });
}

// Helper to broadcast to team
export async function broadcastToTeam(
  io: SocketIOServer,
  teamId: string,
  event: string,
  data: any
): Promise<void> {
  io.to(`team:${teamId}`).emit(event, data);
}
