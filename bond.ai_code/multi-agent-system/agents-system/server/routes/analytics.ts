import { Router, Response } from 'express';
import { Pool } from 'pg';
import { authenticateToken, AuthRequest } from '../middleware/auth';

export function createAnalyticsRoutes(pool: Pool): Router {
  const router = Router();

  // GET /api/analytics/dashboard - Get overview dashboard data (requires auth)
  router.get('/dashboard', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const userId = req.user!.userId;
      const { period = '30' } = req.query; // days

      // Get user statistics
      const statsResult = await pool.query(
        `SELECT
          COUNT(DISTINCT ac.id) as total_conversations,
          COUNT(DISTINCT cons.id) as total_consultations,
          COUNT(DISTINCT di.id) as decisions_made,
          AVG(cons.user_rating)::numeric(3,2) as avg_rating,
          COUNT(DISTINCT DATE(cons.created_at)) as active_days
        FROM users u
        LEFT JOIN agent_conversations ac ON u.id = ac.user_id
          AND ac.created_at >= NOW() - INTERVAL '${parseInt(period as string)} days'
        LEFT JOIN agent_consultations cons ON u.id = cons.user_id
          AND cons.created_at >= NOW() - INTERVAL '${parseInt(period as string)} days'
        LEFT JOIN decision_instances di ON u.id = di.user_id
          AND di.created_at >= NOW() - INTERVAL '${parseInt(period as string)} days'
        WHERE u.id = $1`,
        [userId]
      );

      // Get consultation breakdown by decision context
      const contextBreakdown = await pool.query(
        `SELECT
          decision_context,
          COUNT(*)::int as count,
          AVG(user_rating)::numeric(3,2) as avg_rating
        FROM agent_consultations
        WHERE user_id = $1
          AND created_at >= NOW() - INTERVAL '${parseInt(period as string)} days'
        GROUP BY decision_context
        ORDER BY count DESC`,
        [userId]
      );

      // Get top agents used
      const topAgents = await pool.query(
        `SELECT
          ba.agent_key as "agentKey",
          ba.name,
          ba.avatar_url as "avatarUrl",
          COUNT(*)::int as consultations,
          AVG(ac.user_rating)::numeric(3,2) as avg_rating
        FROM agent_consultations ac
        JOIN behavior_agents ba ON ac.agent_id = ba.id
        WHERE ac.user_id = $1
          AND ac.created_at >= NOW() - INTERVAL '${parseInt(period as string)} days'
        GROUP BY ba.id, ba.agent_key, ba.name, ba.avatar_url
        ORDER BY consultations DESC
        LIMIT 5`,
        [userId]
      );

      // Get activity timeline
      const activityTimeline = await pool.query(
        `SELECT
          DATE(created_at) as date,
          COUNT(*)::int as consultations
        FROM agent_consultations
        WHERE user_id = $1
          AND created_at >= NOW() - INTERVAL '${parseInt(period as string)} days'
        GROUP BY DATE(created_at)
        ORDER BY date ASC`,
        [userId]
      );

      // Get outcome success rate
      const outcomeStats = await pool.query(
        `SELECT
          COUNT(*)::int as total_outcomes,
          AVG(success_level)::numeric(3,2) as avg_success,
          SUM(roi_estimate)::numeric(15,2) as total_roi,
          AVG(roi_estimate)::numeric(15,2) as avg_roi,
          COUNT(CASE WHEN decision_implemented THEN 1 END)::int as implemented_count
        FROM consultation_outcomes
        WHERE user_id = $1
          AND created_at >= NOW() - INTERVAL '${parseInt(period as string)} days'`,
        [userId]
      );

      res.json({
        success: true,
        period: `${period} days`,
        overview: statsResult.rows[0],
        contextBreakdown: contextBreakdown.rows,
        topAgents: topAgents.rows,
        activityTimeline: activityTimeline.rows,
        outcomes: outcomeStats.rows[0],
      });
    } catch (error) {
      console.error('Error fetching dashboard analytics:', error);
      res.status(500).json({ success: false, error: 'Failed to fetch analytics' });
    }
  });

  // GET /api/analytics/agents - Get agent performance metrics
  router.get('/agents', async (req, res: Response) => {
    try {
      const { period = '30' } = req.query;

      const result = await pool.query(
        `SELECT
          ba.id,
          ba.agent_key as "agentKey",
          ba.name,
          ba.title,
          ba.avatar_url as "avatarUrl",
          ba.sectors,
          COUNT(DISTINCT ac.id)::int as total_consultations,
          AVG(ac.user_rating)::numeric(3,2) as avg_rating,
          AVG(ac.confidence_score)::numeric(3,2) as avg_confidence,
          COUNT(DISTINCT co.id)::int as outcomes_tracked,
          AVG(co.success_level)::numeric(3,2) as avg_success_level,
          AVG(co.roi_estimate)::numeric(15,2) as avg_roi
        FROM behavior_agents ba
        LEFT JOIN agent_consultations ac ON ba.id = ac.agent_id
          AND ac.created_at >= NOW() - INTERVAL '${parseInt(period as string)} days'
        LEFT JOIN consultation_outcomes co ON ac.id = co.consultation_id
        WHERE ba.is_active = true
        GROUP BY ba.id, ba.agent_key, ba.name, ba.title, ba.avatar_url, ba.sectors
        ORDER BY total_consultations DESC`,
        []
      );

      res.json({
        success: true,
        period: `${period} days`,
        agents: result.rows,
      });
    } catch (error) {
      console.error('Error fetching agent analytics:', error);
      res.status(500).json({ success: false, error: 'Failed to fetch agent analytics' });
    }
  });

  // GET /api/analytics/agents/:agentKey - Get detailed agent analytics
  router.get('/agents/:agentKey', async (req, res: Response) => {
    try {
      const { agentKey } = req.params;
      const { period = '90' } = req.query;

      // Get agent ID
      const agentResult = await pool.query(
        'SELECT id FROM behavior_agents WHERE agent_key = $1',
        [agentKey]
      );

      if (agentResult.rows.length === 0) {
        res.status(404).json({ success: false, error: 'Agent not found' });
        return;
      }

      const agentId = agentResult.rows[0].id;

      // Overall metrics
      const metricsResult = await pool.query(
        `SELECT
          COUNT(DISTINCT ac.id)::int as total_consultations,
          AVG(ac.user_rating)::numeric(3,2) as avg_rating,
          AVG(ac.confidence_score)::numeric(3,2) as avg_confidence,
          AVG(ac.success_probability)::numeric(3,2) as avg_success_prob,
          COUNT(DISTINCT ac.user_id)::int as unique_users
        FROM agent_consultations ac
        WHERE ac.agent_id = $1
          AND ac.created_at >= NOW() - INTERVAL '${parseInt(period as string)} days'`,
        [agentId]
      );

      // Context breakdown
      const contextResult = await pool.query(
        `SELECT
          decision_context,
          COUNT(*)::int as consultations,
          AVG(user_rating)::numeric(3,2) as avg_rating,
          AVG(confidence_score)::numeric(3,2) as avg_confidence
        FROM agent_consultations
        WHERE agent_id = $1
          AND created_at >= NOW() - INTERVAL '${parseInt(period as string)} days'
        GROUP BY decision_context
        ORDER BY consultations DESC`,
        [agentId]
      );

      // Outcome tracking
      const outcomeResult = await pool.query(
        `SELECT
          COUNT(*)::int as total_outcomes,
          AVG(success_level)::numeric(3,2) as avg_success,
          SUM(roi_estimate)::numeric(15,2) as total_roi,
          COUNT(CASE WHEN decision_implemented THEN 1 END)::int as implemented,
          COUNT(CASE WHEN would_follow_again THEN 1 END)::int as would_follow_again
        FROM consultation_outcomes co
        JOIN agent_consultations ac ON co.consultation_id = ac.id
        WHERE ac.agent_id = $1
          AND co.created_at >= NOW() - INTERVAL '${parseInt(period as string)} days'`,
        [agentId]
      );

      // Timeline
      const timelineResult = await pool.query(
        `SELECT
          DATE(created_at) as date,
          COUNT(*)::int as consultations,
          AVG(user_rating)::numeric(3,2) as avg_rating
        FROM agent_consultations
        WHERE agent_id = $1
          AND created_at >= NOW() - INTERVAL '${parseInt(period as string)} days'
        GROUP BY DATE(created_at)
        ORDER BY date ASC`,
        [agentId]
      );

      // Top questions/topics
      const topicsResult = await pool.query(
        `SELECT
          decision_context,
          question,
          user_rating,
          confidence_score,
          created_at
        FROM agent_consultations
        WHERE agent_id = $1
          AND user_rating >= 4
          AND created_at >= NOW() - INTERVAL '${parseInt(period as string)} days'
        ORDER BY user_rating DESC, confidence_score DESC
        LIMIT 10`,
        [agentId]
      );

      res.json({
        success: true,
        agentKey,
        period: `${period} days`,
        metrics: metricsResult.rows[0],
        contextBreakdown: contextResult.rows,
        outcomes: outcomeResult.rows[0],
        timeline: timelineResult.rows,
        topQuestions: topicsResult.rows,
      });
    } catch (error) {
      console.error('Error fetching detailed agent analytics:', error);
      res.status(500).json({ success: false, error: 'Failed to fetch agent analytics' });
    }
  });

  // GET /api/analytics/decisions - Get decision analytics (requires auth)
  router.get('/decisions', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const userId = req.user!.userId;
      const { period = '90' } = req.query;

      // Decision instances summary
      const summaryResult = await pool.query(
        `SELECT
          COUNT(*)::int as total_decisions,
          COUNT(CASE WHEN status = 'decided' THEN 1 END)::int as completed,
          COUNT(CASE WHEN status = 'in_progress' THEN 1 END)::int as in_progress,
          COUNT(CASE WHEN status = 'abandoned' THEN 1 END)::int as abandoned,
          AVG(success_rating)::numeric(3,2) as avg_success_rating
        FROM decision_instances
        WHERE user_id = $1
          AND created_at >= NOW() - INTERVAL '${parseInt(period as string)} days'`,
        [userId]
      );

      // Decisions by template
      const templateResult = await pool.query(
        `SELECT
          dt.name as template_name,
          dt.category,
          COUNT(di.id)::int as usage_count,
          AVG(di.success_rating)::numeric(3,2) as avg_success
        FROM decision_instances di
        JOIN decision_templates dt ON di.template_id = dt.id
        WHERE di.user_id = $1
          AND di.created_at >= NOW() - INTERVAL '${parseInt(period as string)} days'
        GROUP BY dt.id, dt.name, dt.category
        ORDER BY usage_count DESC`,
        [userId]
      );

      // Timeline
      const timelineResult = await pool.query(
        `SELECT
          DATE(created_at) as date,
          COUNT(*)::int as decisions_made,
          COUNT(CASE WHEN status = 'decided' THEN 1 END)::int as completed
        FROM decision_instances
        WHERE user_id = $1
          AND created_at >= NOW() - INTERVAL '${parseInt(period as string)} days'
        GROUP BY DATE(created_at)
        ORDER BY date ASC`,
        [userId]
      );

      res.json({
        success: true,
        period: `${period} days`,
        summary: summaryResult.rows[0],
        byTemplate: templateResult.rows,
        timeline: timelineResult.rows,
      });
    } catch (error) {
      console.error('Error fetching decision analytics:', error);
      res.status(500).json({ success: false, error: 'Failed to fetch decision analytics' });
    }
  });

  // GET /api/analytics/insights - Get AI-generated insights (requires auth)
  router.get('/insights', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const userId = req.user!.userId;

      // Get user patterns
      const patternsResult = await pool.query(
        `SELECT
          decision_context,
          COUNT(*)::int as frequency,
          AVG(user_rating)::numeric(3,2) as avg_rating
        FROM agent_consultations
        WHERE user_id = $1
          AND created_at >= NOW() - INTERVAL '90 days'
        GROUP BY decision_context
        HAVING COUNT(*) >= 3
        ORDER BY frequency DESC
        LIMIT 5`,
        [userId]
      );

      // Get success patterns
      const successResult = await pool.query(
        `SELECT
          ac.decision_context,
          ba.name as best_agent,
          COUNT(*)::int as consultations,
          AVG(co.success_level)::numeric(3,2) as success_rate
        FROM consultation_outcomes co
        JOIN agent_consultations ac ON co.consultation_id = ac.id
        JOIN behavior_agents ba ON ac.agent_id = ba.id
        WHERE ac.user_id = $1
          AND co.success_level >= 4
        GROUP BY ac.decision_context, ba.name
        ORDER BY success_rate DESC, consultations DESC
        LIMIT 5`,
        [userId]
      );

      // Get improvement opportunities
      const improvementResult = await pool.query(
        `SELECT
          decision_context,
          COUNT(*)::int as consultations,
          AVG(user_rating)::numeric(3,2) as avg_rating
        FROM agent_consultations
        WHERE user_id = $1
          AND created_at >= NOW() - INTERVAL '90 days'
        GROUP BY decision_context
        HAVING AVG(user_rating) < 3.5
        ORDER BY consultations DESC
        LIMIT 3`,
        [userId]
      );

      // Generate insights
      const insights = [];

      // Pattern insights
      if (patternsResult.rows.length > 0) {
        const topPattern = patternsResult.rows[0];
        insights.push({
          type: 'pattern',
          title: 'Your Primary Focus Area',
          message: `You frequently consult on ${topPattern.decision_context} decisions (${topPattern.frequency} times in the last 90 days). Your average satisfaction is ${topPattern.avg_rating}/5.`,
          priority: 'medium',
        });
      }

      // Success insights
      if (successResult.rows.length > 0) {
        const bestMatch = successResult.rows[0];
        insights.push({
          type: 'recommendation',
          title: 'Winning Combination',
          message: `${bestMatch.best_agent} provides the best guidance for ${bestMatch.decision_context} decisions with a ${Math.round(parseFloat(bestMatch.success_rate) * 100)}% success rate.`,
          priority: 'high',
        });
      }

      // Improvement opportunities
      if (improvementResult.rows.length > 0) {
        const needsImprovement = improvementResult.rows[0];
        insights.push({
          type: 'opportunity',
          title: 'Room for Improvement',
          message: `Consider trying different agents or board rooms for ${needsImprovement.decision_context} decisions. Current satisfaction is ${needsImprovement.avg_rating}/5.`,
          priority: 'medium',
        });
      }

      // Industry insights
      const industryInsights = await pool.query(
        `SELECT
          title,
          description,
          confidence_score
        FROM industry_insights
        WHERE is_active = true
          AND (valid_until IS NULL OR valid_until > NOW())
        ORDER BY confidence_score DESC
        LIMIT 3`
      );

      res.json({
        success: true,
        personalInsights: insights,
        industryInsights: industryInsights.rows,
        userPatterns: patternsResult.rows,
      });
    } catch (error) {
      console.error('Error generating insights:', error);
      res.status(500).json({ success: false, error: 'Failed to generate insights' });
    }
  });

  // GET /api/analytics/export - Export analytics data (requires auth)
  router.get('/export', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const userId = req.user!.userId;
      const { format = 'json', period = '90' } = req.query;

      // Get comprehensive data
      const consultations = await pool.query(
        `SELECT
          ac.id,
          ac.question,
          ac.decision_context,
          ac.advice,
          ac.confidence_score,
          ac.user_rating,
          ac.created_at,
          ba.name as agent_name,
          co.decision_implemented,
          co.success_level,
          co.roi_estimate
        FROM agent_consultations ac
        JOIN behavior_agents ba ON ac.agent_id = ba.id
        LEFT JOIN consultation_outcomes co ON ac.id = co.consultation_id
        WHERE ac.user_id = $1
          AND ac.created_at >= NOW() - INTERVAL '${parseInt(period as string)} days'
        ORDER BY ac.created_at DESC`,
        [userId]
      );

      if (format === 'csv') {
        // Convert to CSV
        const header = Object.keys(consultations.rows[0] || {}).join(',');
        const rows = consultations.rows.map(row =>
          Object.values(row).map(v => `"${v}"`).join(',')
        );
        const csv = [header, ...rows].join('\n');

        res.setHeader('Content-Type', 'text/csv');
        res.setHeader('Content-Disposition', `attachment; filename=analytics_${period}days.csv`);
        res.send(csv);
      } else {
        // Return JSON
        res.json({
          success: true,
          period: `${period} days`,
          exportDate: new Date().toISOString(),
          data: consultations.rows,
        });
      }
    } catch (error) {
      console.error('Error exporting analytics:', error);
      res.status(500).json({ success: false, error: 'Failed to export analytics' });
    }
  });

  return router;
}
