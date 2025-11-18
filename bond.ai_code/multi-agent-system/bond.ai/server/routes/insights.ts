import express from 'express';
import { Pool } from 'pg';
import Redis from 'ioredis';
import { authenticate } from '../auth/jwt';
import { MatchExplanationEngine } from '../services/MatchExplanationEngine';
import { SuccessPredictionEngine } from '../services/SuccessPredictionEngine';
import { IntroductionGenerator } from '../services/IntroductionGenerator';

/**
 * AI Insights API Routes
 *
 * Provides endpoints for:
 * - Match explanations
 * - Success predictions
 * - Automated introduction generation
 */

export function createInsightsRoutes(pool: Pool, redis: Redis): express.Router {
  const router = express.Router();

  const explanationEngine = new MatchExplanationEngine(pool, redis);
  const predictionEngine = new SuccessPredictionEngine(pool, redis);
  const introGenerator = new IntroductionGenerator(pool, redis);

  /**
   * GET /api/insights/match/:id/explanation
   * Get AI-generated explanation for why a match occurred
   */
  router.get('/match/:id/explanation', authenticate, async (req, res) => {
    try {
      const userId = req.user!.id;
      const { id: matchId } = req.params;

      const explanation = await explanationEngine.explainMatch(userId, matchId);

      res.json({
        success: true,
        explanation
      });
    } catch (error) {
      console.error('Error generating match explanation:', error);
      res.status(500).json({ error: 'Failed to generate explanation' });
    }
  });

  /**
   * GET /api/insights/match/:id/prediction
   * Get success probability prediction for a match
   */
  router.get('/match/:id/prediction', authenticate, async (req, res) => {
    try {
      const { id: matchId } = req.params;

      const prediction = await predictionEngine.predictSuccess(matchId);

      res.json({
        success: true,
        prediction
      });
    } catch (error) {
      console.error('Error generating prediction:', error);
      res.status(500).json({ error: 'Failed to generate prediction' });
    }
  });

  /**
   * POST /api/insights/match/:id/introduction
   * Generate personalized introduction for a match
   */
  router.post('/match/:id/introduction', authenticate, async (req, res) => {
    try {
      const userId = req.user!.id;
      const { id: matchId } = req.params;
      const { tone = 'professional' } = req.body;

      const introduction = await introGenerator.generateIntroduction(userId, matchId, tone);

      res.json({
        success: true,
        introduction
      });
    } catch (error) {
      console.error('Error generating introduction:', error);
      res.status(500).json({ error: 'Failed to generate introduction' });
    }
  });

  /**
   * POST /api/insights/match/:id/send-introduction
   * Generate and send introduction in one action
   */
  router.post('/match/:id/send-introduction', authenticate, async (req, res) => {
    try {
      const userId = req.user!.id;
      const { id: matchId } = req.params;
      const { tone = 'professional', customizations } = req.body;

      // Generate introduction
      const introduction = await introGenerator.generateIntroduction(userId, matchId, tone);

      // Get match details for recipient
      const client = await pool.connect();
      try {
        const matchResult = await client.query(
          `SELECT
             mc.*,
             a1.user_id as user1_id,
             a2.user_id as user2_id
           FROM match_candidates mc
           JOIN agents a1 ON mc.initiator_agent_id = a1.id
           JOIN agents a2 ON mc.agent_id = a2.id
           WHERE mc.id = $1 AND (a1.user_id = $2 OR a2.user_id = $2)`,
          [matchId, userId]
        );

        if (matchResult.rows.length === 0) {
          return res.status(404).json({ error: 'Match not found' });
        }

        const match = matchResult.rows[0];
        const recipientId = match.user1_id === userId ? match.user2_id : match.user1_id;

        // Create conversation if doesn't exist
        const convResult = await client.query(
          `INSERT INTO conversations (participants, type, match_id)
           VALUES ($1, 'introduction', $2)
           ON CONFLICT DO NOTHING
           RETURNING id`,
          [[userId, recipientId], matchId]
        );

        let conversationId = convResult.rows[0]?.id;

        if (!conversationId) {
          // Conversation already exists
          const existingConv = await client.query(
            `SELECT id FROM conversations
             WHERE $1 = ANY(participants) AND $2 = ANY(participants)`,
            [userId, recipientId]
          );

          conversationId = existingConv.rows[0]?.id;
        }

        // Apply customizations if provided
        let finalBody = introduction.body;
        if (customizations?.additionalNotes) {
          finalBody += `\n\nP.S. ${customizations.additionalNotes}`;
        }

        // Send introduction message
        await client.query(
          `INSERT INTO messages (conversation_id, sender_id, recipient_id, content, type)
           VALUES ($1, $2, $3, $4, 'introduction')`,
          [conversationId, userId, recipientId, finalBody]
        );

        res.json({
          success: true,
          message: 'Introduction sent successfully',
          introduction,
          conversationId
        });
      } finally {
        client.release();
      }
    } catch (error) {
      console.error('Error sending introduction:', error);
      res.status(500).json({ error: 'Failed to send introduction' });
    }
  });

  /**
   * GET /api/insights/user/recommendations
   * Get personalized recommendations for the user
   */
  router.get('/user/recommendations', authenticate, async (req, res) => {
    try {
      const userId = req.user!.id;

      const client = await pool.connect();
      try {
        // Get top matches that haven't been contacted
        const matches = await client.query(
          `SELECT
             mc.id,
             mc.compatibility_score,
             mc.match_type,
             u.name as match_name
           FROM match_candidates mc
           JOIN agents a1 ON mc.initiator_agent_id = a1.id
           JOIN agents a2 ON mc.agent_id = a2.id
           JOIN users u ON a2.user_id = u.id
           WHERE a1.user_id = $1
           AND mc.status = 'active'
           AND NOT EXISTS (
             SELECT 1 FROM conversations c
             WHERE mc.id::text = ANY(c.participants::text[])
           )
           ORDER BY mc.compatibility_score DESC
           LIMIT 5`,
          [userId]
        );

        // Get predictions for each match
        const recommendations = await Promise.all(
          matches.rows.map(async (match) => {
            const prediction = await predictionEngine.predictSuccess(match.id);

            return {
              matchId: match.id,
              matchName: match.match_name,
              matchType: match.match_type,
              compatibilityScore: match.compatibility_score,
              successProbability: prediction.successProbability,
              recommendation: prediction.recommendations[0],
              priority: prediction.successProbability > 0.75 ? 'high' :
                       prediction.successProbability > 0.5 ? 'medium' : 'low'
            };
          })
        );

        // Sort by success probability
        recommendations.sort((a, b) => b.successProbability - a.successProbability);

        res.json({
          success: true,
          recommendations
        });
      } finally {
        client.release();
      }
    } catch (error) {
      console.error('Error getting recommendations:', error);
      res.status(500).json({ error: 'Failed to get recommendations' });
    }
  });

  /**
   * GET /api/insights/match/:id/complete
   * Get complete insights package (explanation + prediction + introduction)
   */
  router.get('/match/:id/complete', authenticate, async (req, res) => {
    try {
      const userId = req.user!.id;
      const { id: matchId } = req.params;

      // Get all insights in parallel
      const [explanation, prediction, introduction] = await Promise.all([
        explanationEngine.explainMatch(userId, matchId),
        predictionEngine.predictSuccess(matchId),
        introGenerator.generateIntroduction(userId, matchId)
      ]);

      res.json({
        success: true,
        insights: {
          explanation,
          prediction,
          introduction
        }
      });
    } catch (error) {
      console.error('Error getting complete insights:', error);
      res.status(500).json({ error: 'Failed to get insights' });
    }
  });

  return router;
}
