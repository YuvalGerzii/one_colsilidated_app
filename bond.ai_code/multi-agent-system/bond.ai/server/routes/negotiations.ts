import express from 'express';
import { Pool } from 'pg';
import Redis from 'ioredis';
import { authenticate } from '../auth/jwt';
// TODO: Re-enable when AdvancedNegotiationStrategies is properly integrated
// import { NegotiationStrategies, StrategyExecutor, MultiModelCoordinator } from '../../src/agents/AdvancedNegotiationStrategies';

/**
 * Advanced Negotiation Strategies API Routes
 *
 * Provides endpoints for:
 * - Selecting and managing negotiation strategies
 * - Starting negotiations with specific strategies
 * - Tracking negotiation performance
 * - Getting strategy recommendations
 */

export function createNegotiationRoutes(pool: Pool, redis: Redis): express.Router {
  const router = express.Router();

  /**
   * GET /api/negotiations/strategies
   * Get all available negotiation strategies
   */
  router.get('/strategies', authenticate, async (req, res) => {
    try {
      const strategies = NegotiationStrategies.getAllStrategies();

      res.json({
        success: true,
        strategies,
        count: strategies.length
      });
    } catch (error) {
      console.error('Error getting strategies:', error);
      res.status(500).json({ error: 'Failed to get strategies' });
    }
  });

  /**
   * POST /api/negotiations/strategies/recommend
   * Get recommended strategy based on context
   */
  router.post('/strategies/recommend', authenticate, async (req, res) => {
    try {
      const userId = req.user!.id;
      const { matchId, matchType } = req.body;

      if (!matchId || !matchType) {
        return res.status(400).json({ error: 'Match ID and type required' });
      }

      const client = await pool.connect();

      try {
        // Get opponent's negotiation history
        const historyResult = await client.query(
          `SELECT n.conversation_history, mc.metadata
           FROM negotiations n
           JOIN match_candidates mc ON n.match_id = mc.id
           WHERE mc.id = $1`,
          [matchId]
        );

        const opponentHistory = historyResult.rows[0]?.conversation_history || [];
        const trustLevel = historyResult.rows[0]?.metadata?.trustLevel || 0.5;

        // Get recommended strategy
        const strategy = NegotiationStrategies.selectOptimalStrategy(
          opponentHistory,
          matchType,
          trustLevel
        );

        res.json({
          success: true,
          recommendedStrategy: strategy,
          reason: `Selected based on match type (${matchType}) and trust level (${Math.round(trustLevel * 100)}%)`
        });
      } finally {
        client.release();
      }
    } catch (error) {
      console.error('Error recommending strategy:', error);
      res.status(500).json({ error: 'Failed to recommend strategy' });
    }
  });

  /**
   * POST /api/negotiations/start
   * Start a negotiation with a specific strategy
   */
  router.post('/start', authenticate, async (req, res) => {
    try {
      const userId = req.user!.id;
      const { matchId, strategyName, useMultiModel = false } = req.body;

      if (!matchId) {
        return res.status(400).json({ error: 'Match ID required' });
      }

      const client = await pool.connect();

      try {
        // Get match details
        const matchResult = await client.query(
          `SELECT mc.*, a1.user_id as initiator_user_id, a2.user_id as target_user_id
           FROM match_candidates mc
           JOIN agents a1 ON mc.initiator_agent_id = a1.id
           JOIN agents a2 ON mc.agent_id = a2.id
           WHERE mc.id = $1 AND a1.user_id = $2`,
          [matchId, userId]
        );

        if (matchResult.rows.length === 0) {
          return res.status(404).json({ error: 'Match not found' });
        }

        const match = matchResult.rows[0];

        // Get or create strategy
        let strategy;
        if (strategyName) {
          const allStrategies = NegotiationStrategies.getAllStrategies();
          strategy = allStrategies.find(s => s.name === strategyName);

          if (!strategy) {
            return res.status(400).json({ error: 'Invalid strategy name' });
          }
        } else {
          // Auto-select optimal strategy
          strategy = NegotiationStrategies.selectOptimalStrategy(
            [],
            match.match_type,
            match.metadata?.trustLevel || 0.5
          );
        }

        // Create negotiation record
        const negotiationResult = await client.query(
          `INSERT INTO negotiations (
            match_id,
            initiator_agent_id,
            target_agent_id,
            status,
            metadata
          )
          VALUES ($1, $2, $3, 'active', $4)
          RETURNING *`,
          [
            matchId,
            match.initiator_agent_id,
            match.agent_id,
            JSON.stringify({
              strategy: strategy.name,
              useMultiModel,
              startedAt: new Date().toISOString()
            })
          ]
        );

        const negotiation = negotiationResult.rows[0];

        // Store strategy configuration in Redis
        await redis.setex(
          `negotiation:${negotiation.id}:strategy`,
          3600 * 24, // 24 hours
          JSON.stringify({
            strategy,
            useMultiModel,
            executor: useMultiModel ? 'multi-model' : 'single'
          })
        );

        res.json({
          success: true,
          negotiation,
          strategy,
          message: 'Negotiation started with ' + strategy.name
        });
      } finally {
        client.release();
      }
    } catch (error) {
      console.error('Error starting negotiation:', error);
      res.status(500).json({ error: 'Failed to start negotiation' });
    }
  });

  /**
   * POST /api/negotiations/:id/action
   * Take an action in an ongoing negotiation
   */
  router.post('/:id/action', authenticate, async (req, res) => {
    try {
      const userId = req.user!.id;
      const { id } = req.params;
      const { proposal, opponentLastAction } = req.body;

      if (!proposal) {
        return res.status(400).json({ error: 'Proposal required' });
      }

      // Get strategy from Redis
      const strategyData = await redis.get(`negotiation:${id}:strategy`);

      if (!strategyData) {
        return res.status(404).json({ error: 'Negotiation strategy not found' });
      }

      const { strategy, useMultiModel } = JSON.parse(strategyData);

      const client = await pool.connect();

      try {
        // Get negotiation details
        const negotiationResult = await client.query(
          `SELECT n.*, a.user_id
           FROM negotiations n
           JOIN agents a ON n.initiator_agent_id = a.id
           WHERE n.id = $1 AND a.user_id = $2`,
          [id, userId]
        );

        if (negotiationResult.rows.length === 0) {
          return res.status(404).json({ error: 'Negotiation not found' });
        }

        const negotiation = negotiationResult.rows[0];
        const round = (negotiation.conversation_history || []).length + 1;

        // Decide action using strategy
        let decision;
        let confidence = 1.0;

        if (useMultiModel) {
          // Use multi-model coordination for risk mitigation
          const strategies = [
            NegotiationStrategies.TIT_FOR_TAT_FORGIVING,
            NegotiationStrategies.GENEROUS_TIT_FOR_TAT,
            NegotiationStrategies.ADAPTIVE_RL
          ];

          const coordinator = new MultiModelCoordinator(strategies);
          decision = coordinator.getConsensusDecision(proposal, opponentLastAction, round);
          confidence = coordinator.getConfidence(proposal, opponentLastAction, round);
        } else {
          // Use single strategy
          const executor = new StrategyExecutor(strategy);
          decision = executor.decideAction(proposal, opponentLastAction, round);
        }

        // Update negotiation with decision
        await client.query(
          `UPDATE negotiations
           SET conversation_history = conversation_history || $1::jsonb,
               updated_at = NOW()
           WHERE id = $2`,
          [
            JSON.stringify([{
              round,
              timestamp: new Date().toISOString(),
              speaker: 'initiator',
              action: decision,
              proposal,
              confidence
            }]),
            id
          ]
        );

        res.json({
          success: true,
          decision,
          confidence,
          round,
          strategy: strategy.name,
          message: `Strategy recommends: ${decision}`
        });
      } finally {
        client.release();
      }
    } catch (error) {
      console.error('Error processing negotiation action:', error);
      res.status(500).json({ error: 'Failed to process action' });
    }
  });

  /**
   * GET /api/negotiations/:id/performance
   * Get performance metrics for a negotiation
   */
  router.get('/:id/performance', authenticate, async (req, res) => {
    try {
      const userId = req.user!.id;
      const { id } = req.params;

      const client = await pool.connect();

      try {
        const result = await client.query(
          `SELECT
             n.*,
             COUNT(CASE WHEN ch->>'action' = 'accept' THEN 1 END) as accept_count,
             COUNT(CASE WHEN ch->>'action' = 'counter' THEN 1 END) as counter_count,
             COUNT(CASE WHEN ch->>'action' = 'reject' THEN 1 END) as reject_count,
             AVG((ch->>'confidence')::float) as avg_confidence
           FROM negotiations n
           CROSS JOIN LATERAL jsonb_array_elements(n.conversation_history) AS ch
           JOIN agents a ON n.initiator_agent_id = a.id
           WHERE n.id = $1 AND a.user_id = $2
           GROUP BY n.id`,
          [id, userId]
        );

        if (result.rows.length === 0) {
          return res.status(404).json({ error: 'Negotiation not found' });
        }

        const performance = result.rows[0];

        res.json({
          success: true,
          performance: {
            negotiationId: id,
            status: performance.status,
            totalRounds: performance.accept_count + performance.counter_count + performance.reject_count,
            acceptCount: performance.accept_count,
            counterCount: performance.counter_count,
            rejectCount: performance.reject_count,
            avgConfidence: performance.avg_confidence,
            startedAt: performance.created_at,
            lastUpdated: performance.updated_at
          }
        });
      } finally {
        client.release();
      }
    } catch (error) {
      console.error('Error getting negotiation performance:', error);
      res.status(500).json({ error: 'Failed to get performance' });
    }
  });

  /**
   * GET /api/negotiations/user/stats
   * Get overall negotiation statistics for the user
   */
  router.get('/user/stats', authenticate, async (req, res) => {
    try {
      const userId = req.user!.id;

      const client = await pool.connect();

      try {
        const result = await client.query(
          `SELECT
             COUNT(*) as total_negotiations,
             COUNT(CASE WHEN n.status = 'completed' THEN 1 END) as completed,
             COUNT(CASE WHEN n.status = 'active' THEN 1 END) as active,
             COUNT(CASE WHEN EXISTS (
               SELECT 1 FROM agreements
               WHERE negotiation_id = n.id
             ) THEN 1 END) as successful_agreements,
             AVG(jsonb_array_length(n.conversation_history)) as avg_rounds
           FROM negotiations n
           JOIN agents a ON n.initiator_agent_id = a.id
           WHERE a.user_id = $1`,
          [userId]
        );

        const stats = result.rows[0];

        res.json({
          success: true,
          stats: {
            totalNegotiations: parseInt(stats.total_negotiations),
            completed: parseInt(stats.completed),
            active: parseInt(stats.active),
            successfulAgreements: parseInt(stats.successful_agreements),
            successRate: stats.total_negotiations > 0
              ? (stats.successful_agreements / stats.total_negotiations * 100).toFixed(1)
              : 0,
            avgRoundsPerNegotiation: stats.avg_rounds ? parseFloat(stats.avg_rounds).toFixed(1) : 0
          }
        });
      } finally {
        client.release();
      }
    } catch (error) {
      console.error('Error getting user stats:', error);
      res.status(500).json({ error: 'Failed to get user stats' });
    }
  });

  return router;
}
