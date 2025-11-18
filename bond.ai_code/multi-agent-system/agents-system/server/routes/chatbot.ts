import { Router, Response } from 'express';
import { Pool } from 'pg';
import Redis from 'ioredis';
import { authenticateToken, AuthRequest } from '../middleware/auth';
import { BehaviorAgentFactory } from '../../src/agents/BehaviorAgentFactory';
import { DecisionContext } from '../../src/types/BehaviorAgentTypes';

export function createChatbotRoutes(pool: Pool, redis: Redis): Router {
  const router = Router();
  const factory = new BehaviorAgentFactory(pool, redis);

  // POST /api/chatbot/conversations - Create new conversation (requires auth)
  router.post('/conversations', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const userId = req.user!.userId;
      const { title, contextType, selectedAgents, boardRoomId } = req.body;

      // Validate
      if (!contextType) {
        res.status(400).json({ success: false, error: 'contextType is required' });
        return;
      }

      // Get agent IDs if agentKeys provided
      let agentIds: string[] = [];
      if (selectedAgents && selectedAgents.length > 0) {
        const agentResult = await pool.query(
          'SELECT id FROM behavior_agents WHERE agent_key = ANY($1)',
          [selectedAgents]
        );
        agentIds = agentResult.rows.map((row) => row.id);
      }

      const result = await pool.query(
        `INSERT INTO agent_conversations (
          user_id, title, context_type, selected_agents, board_room_id
        )
        VALUES ($1, $2, $3, $4, $5)
        RETURNING id, title, context_type as "contextType",
                  selected_agents as "selectedAgents", board_room_id as "boardRoomId",
                  created_at as "createdAt"`,
        [
          userId,
          title || 'New Conversation',
          contextType,
          agentIds.length > 0 ? agentIds : null,
          boardRoomId || null,
        ]
      );

      res.status(201).json({
        success: true,
        conversation: result.rows[0],
      });
    } catch (error) {
      console.error('Error creating conversation:', error);
      res.status(500).json({ success: false, error: 'Failed to create conversation' });
    }
  });

  // GET /api/chatbot/conversations - Get user's conversations (requires auth)
  router.get('/conversations', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const userId = req.user!.userId;

      const result = await pool.query(
        `SELECT
          c.id, c.title, c.context_type as "contextType",
          c.created_at as "createdAt", c.updated_at as "updatedAt",
          c.board_room_id as "boardRoomId",
          br.name as "boardRoomName",
          (
            SELECT json_agg(json_build_object(
              'role', role,
              'content', substring(content, 1, 100),
              'createdAt', created_at
            ) ORDER BY created_at DESC)
            FROM (
              SELECT role, content, created_at
              FROM agent_messages
              WHERE conversation_id = c.id
              ORDER BY created_at DESC
              LIMIT 3
            ) recent
          ) as "recentMessages"
        FROM agent_conversations c
        LEFT JOIN board_rooms br ON c.board_room_id = br.id
        WHERE c.user_id = $1 AND c.is_active = true
        ORDER BY c.updated_at DESC
        LIMIT 50`,
        [userId]
      );

      res.json({
        success: true,
        conversations: result.rows,
      });
    } catch (error) {
      console.error('Error fetching conversations:', error);
      res.status(500).json({ success: false, error: 'Failed to fetch conversations' });
    }
  });

  // GET /api/chatbot/conversations/:id - Get specific conversation with messages (requires auth)
  router.get('/conversations/:id', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const { id } = req.params;
      const userId = req.user!.userId;

      // Get conversation
      const convResult = await pool.query(
        `SELECT
          c.id, c.title, c.context_type as "contextType",
          c.selected_agents as "selectedAgents", c.board_room_id as "boardRoomId",
          c.created_at as "createdAt",
          br.name as "boardRoomName"
        FROM agent_conversations c
        LEFT JOIN board_rooms br ON c.board_room_id = br.id
        WHERE c.id = $1 AND c.user_id = $2 AND c.is_active = true`,
        [id, userId]
      );

      if (convResult.rows.length === 0) {
        res.status(404).json({ success: false, error: 'Conversation not found' });
        return;
      }

      // Get messages
      const messagesResult = await pool.query(
        `SELECT
          m.id, m.role, m.content, m.decision_context as "decisionContext",
          m.structured_data as "structuredData", m.created_at as "createdAt",
          ba.agent_key as "agentKey", ba.name as "agentName", ba.avatar_url as "agentAvatar"
        FROM agent_messages m
        LEFT JOIN behavior_agents ba ON m.agent_id = ba.id
        WHERE m.conversation_id = $1
        ORDER BY m.created_at ASC`,
        [id]
      );

      res.json({
        success: true,
        conversation: {
          ...convResult.rows[0],
          messages: messagesResult.rows,
        },
      });
    } catch (error) {
      console.error('Error fetching conversation:', error);
      res.status(500).json({ success: false, error: 'Failed to fetch conversation' });
    }
  });

  // POST /api/chatbot/ask - Ask agents or board room (requires auth)
  router.post('/ask', authenticateToken, async (req: AuthRequest, res: Response) => {
    const client = await pool.connect();

    try {
      const userId = req.user!.userId;
      const {
        conversationId,
        question,
        agentKeys,
        boardRoomId,
        decisionContext,
      } = req.body;

      // Validation
      if (!conversationId || !question) {
        res.status(400).json({
          success: false,
          error: 'conversationId and question are required',
        });
        return;
      }

      if (!agentKeys && !boardRoomId) {
        res.status(400).json({
          success: false,
          error: 'Either agentKeys or boardRoomId must be provided',
        });
        return;
      }

      await client.query('BEGIN');

      // Save user message
      await client.query(
        `INSERT INTO agent_messages (conversation_id, role, content, decision_context)
        VALUES ($1, 'user', $2, $3)`,
        [conversationId, question, decisionContext || 'GENERAL']
      );

      const responses: any[] = [];

      if (boardRoomId) {
        // Board room consultation
        const boardResult = await client.query(
          `SELECT
            br.name, br.focus_sectors, br.decision_style, br.consensus_threshold,
            array_agg(ba.agent_key) as agent_keys
          FROM board_rooms br
          JOIN board_room_members brm ON br.id = brm.board_room_id
          JOIN behavior_agents ba ON brm.agent_id = ba.id
          WHERE br.id = $1
          GROUP BY br.id, br.name, br.focus_sectors, br.decision_style, br.consensus_threshold`,
          [boardRoomId]
        );

        if (boardResult.rows.length === 0) {
          res.status(404).json({ success: false, error: 'Board room not found' });
          return;
        }

        const boardConfig = boardResult.rows[0];
        const boardRoom = factory.createBoardRoomAgent();

        const sector = boardConfig.focus_sectors && boardConfig.focus_sectors.length > 0
          ? boardConfig.focus_sectors[0]
          : 'GENERAL';

        const consensus = await boardRoom.getBoardRoomConsensus(
          boardConfig.name,
          question,
          (decisionContext as DecisionContext) || 'GENERAL',
          sector as any
        );

        // Format response
        const content = `**${boardConfig.name} Consensus**\n\n${consensus.consensusRecommendation}\n\n**Confidence:** ${Math.round(consensus.confidenceScore * 100)}%\n\n**Action Plan:**\n${consensus.actionPlan.map((a) => `• ${a.action} (${a.priority}) - ${a.timeline}`).join('\n')}`;

        // Save agent response
        await client.query(
          `INSERT INTO agent_messages (
            conversation_id, role, content, decision_context, structured_data
          )
          VALUES ($1, 'agent', $2, $3, $4)`,
          [conversationId, content, decisionContext || 'GENERAL', JSON.stringify(consensus)]
        );

        // Save consultation
        await client.query(
          `INSERT INTO agent_consultations (
            user_id, conversation_id, board_room_id, question,
            decision_context, advice, confidence_score, structured_response
          )
          VALUES ($1, $2, $3, $4, $5, $6, $7, $8)`,
          [
            userId,
            conversationId,
            boardRoomId,
            question,
            decisionContext || 'GENERAL',
            content,
            consensus.confidenceScore,
            JSON.stringify(consensus),
          ]
        );

        responses.push({
          type: 'board_room',
          content,
          structuredData: consensus,
        });
      } else {
        // Individual agent consultations
        for (const agentKey of agentKeys) {
          const agent = factory.getAgentByName(agentKey);
          if (!agent) continue;

          const advice = await agent.getAdvice(
            question,
            (decisionContext as DecisionContext) || 'GENERAL'
          );

          // Get agent ID
          const agentResult = await client.query(
            'SELECT id FROM behavior_agents WHERE agent_key = $1',
            [agentKey]
          );
          const agentId = agentResult.rows[0]?.id;

          // Format response
          const content = `**${agent.profile.name}'s Advice**\n\n${advice.advice}\n\n**Confidence:** ${Math.round(advice.successProbability * 100)}%\n\n**Key Steps:**\n${advice.actionableSteps.map((s) => `• ${s}`).join('\n')}${advice.potentialRisks.length > 0 ? `\n\n**Risks:**\n${advice.potentialRisks.map((r) => `• ${r}`).join('\n')}` : ''}`;

          // Save agent response
          await client.query(
            `INSERT INTO agent_messages (
              conversation_id, role, agent_id, content, decision_context, structured_data
            )
            VALUES ($1, 'agent', $2, $3, $4, $5)`,
            [conversationId, agentId, content, decisionContext || 'GENERAL', JSON.stringify(advice)]
          );

          // Save consultation
          await client.query(
            `INSERT INTO agent_consultations (
              user_id, conversation_id, agent_id, question, decision_context,
              advice, confidence_score, success_probability, structured_response
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)`,
            [
              userId,
              conversationId,
              agentId,
              question,
              decisionContext || 'GENERAL',
              content,
              advice.successProbability,
              advice.successProbability,
              JSON.stringify(advice),
            ]
          );

          // Update user preferences
          await client.query(
            `INSERT INTO user_agent_preferences (user_id, agent_id, usage_count, last_used_at)
            VALUES ($1, $2, 1, NOW())
            ON CONFLICT (user_id, agent_id)
            DO UPDATE SET
              usage_count = user_agent_preferences.usage_count + 1,
              last_used_at = NOW()`,
            [userId, agentId]
          );

          responses.push({
            type: 'individual',
            agentKey,
            agentName: agent.profile.name,
            content,
            structuredData: advice,
          });
        }
      }

      // Update conversation timestamp
      await client.query(
        'UPDATE agent_conversations SET updated_at = NOW() WHERE id = $1',
        [conversationId]
      );

      await client.query('COMMIT');

      res.json({
        success: true,
        responses,
      });
    } catch (error) {
      await client.query('ROLLBACK');
      console.error('Error processing question:', error);
      res.status(500).json({ success: false, error: 'Failed to process question' });
    } finally {
      client.release();
    }
  });

  // POST /api/chatbot/rate - Rate a consultation (requires auth)
  router.post('/rate', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const userId = req.user!.userId;
      const { consultationId, rating, feedback } = req.body;

      // Validation
      if (!consultationId || !rating || rating < 1 || rating > 5) {
        res.status(400).json({
          success: false,
          error: 'Valid consultationId and rating (1-5) are required',
        });
        return;
      }

      // Update consultation
      const result = await pool.query(
        `UPDATE agent_consultations
        SET user_rating = $1, user_feedback = $2
        WHERE id = $3 AND user_id = $4
        RETURNING id`,
        [rating, feedback || null, consultationId, userId]
      );

      if (result.rows.length === 0) {
        res.status(404).json({
          success: false,
          error: 'Consultation not found',
        });
        return;
      }

      res.json({
        success: true,
        message: 'Rating submitted successfully',
      });
    } catch (error) {
      console.error('Error submitting rating:', error);
      res.status(500).json({ success: false, error: 'Failed to submit rating' });
    }
  });

  // DELETE /api/chatbot/conversations/:id - Delete conversation (requires auth)
  router.delete('/conversations/:id', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const { id } = req.params;
      const userId = req.user!.userId;

      // Soft delete
      const result = await pool.query(
        `UPDATE agent_conversations
        SET is_active = false
        WHERE id = $1 AND user_id = $2
        RETURNING id`,
        [id, userId]
      );

      if (result.rows.length === 0) {
        res.status(404).json({ success: false, error: 'Conversation not found' });
        return;
      }

      res.json({
        success: true,
        message: 'Conversation deleted successfully',
      });
    } catch (error) {
      console.error('Error deleting conversation:', error);
      res.status(500).json({ success: false, error: 'Failed to delete conversation' });
    }
  });

  return router;
}
