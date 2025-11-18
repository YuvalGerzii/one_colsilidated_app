import { Router, Response } from 'express';
import { Pool } from 'pg';
import { authenticateToken, AuthRequest } from '../middleware/auth';

export function createOutcomeRoutes(pool: Pool): Router {
  const router = Router();

  // POST /api/outcomes - Report consultation outcome (requires auth)
  router.post('/', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const userId = req.user!.userId;
      const {
        consultationId,
        decisionImplemented,
        implementationDate,
        outcomeDescription,
        successLevel,
        roiEstimate,
        timeSavedHours,
        lessonsLearned,
        wouldFollowAgain,
      } = req.body;

      if (!consultationId) {
        res.status(400).json({ success: false, error: 'consultationId is required' });
        return;
      }

      // Verify consultation belongs to user
      const consultationCheck = await pool.query(
        'SELECT id FROM agent_consultations WHERE id = $1 AND user_id = $2',
        [consultationId, userId]
      );

      if (consultationCheck.rows.length === 0) {
        res.status(404).json({ success: false, error: 'Consultation not found' });
        return;
      }

      const result = await pool.query(
        `INSERT INTO consultation_outcomes (
          consultation_id, user_id, decision_implemented, implementation_date,
          outcome_description, success_level, roi_estimate, time_saved_hours,
          lessons_learned, would_follow_again
        )
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
        RETURNING id, decision_implemented as "decisionImplemented",
                  success_level as "successLevel", created_at as "createdAt"`,
        [
          consultationId,
          userId,
          decisionImplemented || false,
          implementationDate || null,
          outcomeDescription || null,
          successLevel || null,
          roiEstimate || null,
          timeSavedHours || null,
          lessonsLearned || null,
          wouldFollowAgain || null,
        ]
      );

      res.status(201).json({
        success: true,
        outcome: result.rows[0],
      });
    } catch (error) {
      console.error('Error reporting outcome:', error);
      res.status(500).json({ success: false, error: 'Failed to report outcome' });
    }
  });

  // GET /api/outcomes - Get user's consultation outcomes (requires auth)
  router.get('/', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const userId = req.user!.userId;
      const { period = '90' } = req.query;

      const result = await pool.query(
        `SELECT
          co.id, co.decision_implemented as "decisionImplemented",
          co.implementation_date as "implementationDate",
          co.outcome_description as "outcomeDescription",
          co.success_level as "successLevel",
          co.roi_estimate as "roiEstimate",
          co.time_saved_hours as "timeSavedHours",
          co.would_follow_again as "wouldFollowAgain",
          co.created_at as "createdAt",
          ac.question,
          ac.decision_context as "decisionContext",
          ba.name as "agentName",
          ba.agent_key as "agentKey",
          ba.avatar_url as "avatarUrl"
        FROM consultation_outcomes co
        JOIN agent_consultations ac ON co.consultation_id = ac.id
        JOIN behavior_agents ba ON ac.agent_id = ba.id
        WHERE co.user_id = $1
          AND co.created_at >= NOW() - INTERVAL '${parseInt(period as string)} days'
        ORDER BY co.created_at DESC`,
        [userId]
      );

      // Calculate aggregates
      const aggregates = await pool.query(
        `SELECT
          COUNT(*)::int as total_outcomes,
          AVG(success_level)::numeric(3,2) as avg_success,
          SUM(roi_estimate)::numeric(15,2) as total_roi,
          AVG(roi_estimate)::numeric(15,2) as avg_roi,
          SUM(time_saved_hours)::int as total_time_saved,
          COUNT(CASE WHEN decision_implemented THEN 1 END)::int as implemented_count,
          COUNT(CASE WHEN would_follow_again THEN 1 END)::int as would_follow_again_count
        FROM consultation_outcomes
        WHERE user_id = $1
          AND created_at >= NOW() - INTERVAL '${parseInt(period as string)} days'`,
        [userId]
      );

      res.json({
        success: true,
        outcomes: result.rows,
        aggregates: aggregates.rows[0],
      });
    } catch (error) {
      console.error('Error fetching outcomes:', error);
      res.status(500).json({ success: false, error: 'Failed to fetch outcomes' });
    }
  });

  // GET /api/outcomes/:id - Get specific outcome (requires auth)
  router.get('/:id', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const { id } = req.params;
      const userId = req.user!.userId;

      const result = await pool.query(
        `SELECT
          co.id, co.decision_implemented as "decisionImplemented",
          co.implementation_date as "implementationDate",
          co.outcome_description as "outcomeDescription",
          co.success_level as "successLevel",
          co.roi_estimate as "roiEstimate",
          co.time_saved_hours as "timeSavedHours",
          co.lessons_learned as "lessonsLearned",
          co.would_follow_again as "wouldFollowAgain",
          co.created_at as "createdAt",
          ac.id as "consultationId",
          ac.question,
          ac.advice,
          ac.decision_context as "decisionContext",
          ac.confidence_score as "confidenceScore",
          ba.name as "agentName",
          ba.agent_key as "agentKey"
        FROM consultation_outcomes co
        JOIN agent_consultations ac ON co.consultation_id = ac.id
        JOIN behavior_agents ba ON ac.agent_id = ba.id
        WHERE co.id = $1 AND co.user_id = $2`,
        [id, userId]
      );

      if (result.rows.length === 0) {
        res.status(404).json({ success: false, error: 'Outcome not found' });
        return;
      }

      res.json({
        success: true,
        outcome: result.rows[0],
      });
    } catch (error) {
      console.error('Error fetching outcome:', error);
      res.status(500).json({ success: false, error: 'Failed to fetch outcome' });
    }
  });

  // PUT /api/outcomes/:id - Update outcome (requires auth)
  router.put('/:id', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const { id } = req.params;
      const userId = req.user!.userId;
      const {
        decisionImplemented,
        implementationDate,
        outcomeDescription,
        successLevel,
        roiEstimate,
        timeSavedHours,
        lessonsLearned,
        wouldFollowAgain,
      } = req.body;

      const result = await pool.query(
        `UPDATE consultation_outcomes
        SET decision_implemented = COALESCE($1, decision_implemented),
            implementation_date = COALESCE($2, implementation_date),
            outcome_description = COALESCE($3, outcome_description),
            success_level = COALESCE($4, success_level),
            roi_estimate = COALESCE($5, roi_estimate),
            time_saved_hours = COALESCE($6, time_saved_hours),
            lessons_learned = COALESCE($7, lessons_learned),
            would_follow_again = COALESCE($8, would_follow_again)
        WHERE id = $9 AND user_id = $10
        RETURNING id, success_level as "successLevel", updated_at as "updatedAt"`,
        [
          decisionImplemented,
          implementationDate,
          outcomeDescription,
          successLevel,
          roiEstimate,
          timeSavedHours,
          lessonsLearned,
          wouldFollowAgain,
          id,
          userId,
        ]
      );

      if (result.rows.length === 0) {
        res.status(404).json({ success: false, error: 'Outcome not found' });
        return;
      }

      res.json({
        success: true,
        outcome: result.rows[0],
      });
    } catch (error) {
      console.error('Error updating outcome:', error);
      res.status(500).json({ success: false, error: 'Failed to update outcome' });
    }
  });

  // DELETE /api/outcomes/:id - Delete outcome (requires auth)
  router.delete('/:id', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const { id } = req.params;
      const userId = req.user!.userId;

      const result = await pool.query(
        'DELETE FROM consultation_outcomes WHERE id = $1 AND user_id = $2 RETURNING id',
        [id, userId]
      );

      if (result.rows.length === 0) {
        res.status(404).json({ success: false, error: 'Outcome not found' });
        return;
      }

      res.json({
        success: true,
        message: 'Outcome deleted successfully',
      });
    } catch (error) {
      console.error('Error deleting outcome:', error);
      res.status(500).json({ success: false, error: 'Failed to delete outcome' });
    }
  });

  // GET /api/outcomes/stats/summary - Get outcome statistics (requires auth)
  router.get('/stats/summary', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const userId = req.user!.userId;
      const { period = '90' } = req.query;

      // Overall stats
      const overallStats = await pool.query(
        `SELECT
          COUNT(*)::int as total_outcomes,
          AVG(success_level)::numeric(3,2) as avg_success,
          SUM(roi_estimate)::numeric(15,2) as total_roi,
          AVG(roi_estimate)::numeric(15,2) as avg_roi,
          SUM(time_saved_hours)::int as total_time_saved,
          COUNT(CASE WHEN decision_implemented THEN 1 END)::decimal /
            NULLIF(COUNT(*), 0) as implementation_rate,
          COUNT(CASE WHEN would_follow_again THEN 1 END)::decimal /
            NULLIF(COUNT(*), 0) as would_follow_again_rate
        FROM consultation_outcomes
        WHERE user_id = $1
          AND created_at >= NOW() - INTERVAL '${parseInt(period as string)} days'`,
        [userId]
      );

      // By agent
      const byAgent = await pool.query(
        `SELECT
          ba.name as agent_name,
          ba.agent_key as "agentKey",
          COUNT(*)::int as outcomes_count,
          AVG(co.success_level)::numeric(3,2) as avg_success,
          SUM(co.roi_estimate)::numeric(15,2) as total_roi
        FROM consultation_outcomes co
        JOIN agent_consultations ac ON co.consultation_id = ac.id
        JOIN behavior_agents ba ON ac.agent_id = ba.id
        WHERE co.user_id = $1
          AND co.created_at >= NOW() - INTERVAL '${parseInt(period as string)} days'
        GROUP BY ba.id, ba.name, ba.agent_key
        ORDER BY avg_success DESC NULLS LAST`,
        [userId]
      );

      // By decision context
      const byContext = await pool.query(
        `SELECT
          ac.decision_context,
          COUNT(*)::int as outcomes_count,
          AVG(co.success_level)::numeric(3,2) as avg_success,
          SUM(co.roi_estimate)::numeric(15,2) as total_roi
        FROM consultation_outcomes co
        JOIN agent_consultations ac ON co.consultation_id = ac.id
        WHERE co.user_id = $1
          AND co.created_at >= NOW() - INTERVAL '${parseInt(period as string)} days'
        GROUP BY ac.decision_context
        ORDER BY outcomes_count DESC`,
        [userId]
      );

      // Success distribution
      const successDistribution = await pool.query(
        `SELECT
          success_level,
          COUNT(*)::int as count
        FROM consultation_outcomes
        WHERE user_id = $1
          AND success_level IS NOT NULL
          AND created_at >= NOW() - INTERVAL '${parseInt(period as string)} days'
        GROUP BY success_level
        ORDER BY success_level ASC`,
        [userId]
      );

      res.json({
        success: true,
        period: `${period} days`,
        overall: overallStats.rows[0],
        byAgent: byAgent.rows,
        byContext: byContext.rows,
        successDistribution: successDistribution.rows,
      });
    } catch (error) {
      console.error('Error fetching outcome stats:', error);
      res.status(500).json({ success: false, error: 'Failed to fetch outcome statistics' });
    }
  });

  return router;
}
