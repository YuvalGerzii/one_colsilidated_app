import { Router, Response } from 'express';
import { Pool } from 'pg';
import { authenticateToken, AuthRequest } from '../middleware/auth';

export function createReportRoutes(pool: Pool): Router {
  const router = Router();

  // GET /api/reports/templates - Get available report templates
  router.get('/templates', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const userId = req.user!.userId;

      const result = await pool.query(
        `SELECT
          id, name, report_type as "reportType",
          template_config as "templateConfig", is_public as "isPublic",
          created_at as "createdAt"
        FROM report_templates
        WHERE is_public = true OR user_id = $1
        ORDER BY name ASC`,
        [userId]
      );

      res.json({
        success: true,
        templates: result.rows,
      });
    } catch (error) {
      console.error('Error fetching report templates:', error);
      res.status(500).json({ success: false, error: 'Failed to fetch templates' });
    }
  });

  // POST /api/reports/generate - Generate a report (requires auth)
  router.post('/generate', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const userId = req.user!.userId;
      const { templateId, reportType, dateRangeStart, dateRangeEnd, options = {} } = req.body;

      if (!reportType) {
        res.status(400).json({ success: false, error: 'reportType is required' });
        return;
      }

      let reportData: any = {};
      const startDate = dateRangeStart || new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString();
      const endDate = dateRangeEnd || new Date().toISOString();

      switch (reportType) {
        case 'executive_summary':
          reportData = await generateExecutiveSummary(pool, userId, startDate, endDate);
          break;
        case 'agent_performance':
          reportData = await generateAgentPerformanceReport(pool, userId, startDate, endDate);
          break;
        case 'decision_history':
          reportData = await generateDecisionHistoryReport(pool, userId, startDate, endDate);
          break;
        case 'roi_analysis':
          reportData = await generateROIAnalysisReport(pool, userId, startDate, endDate);
          break;
        case 'team_activity':
          reportData = await generateTeamActivityReport(pool, userId, startDate, endDate, options.teamId);
          break;
        default:
          res.status(400).json({ success: false, error: 'Unknown report type' });
          return;
      }

      // Save generated report
      const result = await pool.query(
        `INSERT INTO generated_reports (
          template_id, user_id, report_data, date_range_start, date_range_end
        )
        VALUES ($1, $2, $3, $4, $5)
        RETURNING id, created_at as "createdAt"`,
        [templateId || null, userId, JSON.stringify(reportData), startDate, endDate]
      );

      res.json({
        success: true,
        report: {
          id: result.rows[0].id,
          type: reportType,
          dateRange: { start: startDate, end: endDate },
          createdAt: result.rows[0].createdAt,
          data: reportData,
        },
      });
    } catch (error) {
      console.error('Error generating report:', error);
      res.status(500).json({ success: false, error: 'Failed to generate report' });
    }
  });

  // GET /api/reports - Get user's generated reports (requires auth)
  router.get('/', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const userId = req.user!.userId;
      const { limit = '20' } = req.query;

      const result = await pool.query(
        `SELECT
          gr.id, gr.report_data as "reportData",
          gr.date_range_start as "dateRangeStart",
          gr.date_range_end as "dateRangeEnd",
          gr.created_at as "createdAt",
          rt.name as "templateName", rt.report_type as "reportType"
        FROM generated_reports gr
        LEFT JOIN report_templates rt ON gr.template_id = rt.id
        WHERE gr.user_id = $1
        ORDER BY gr.created_at DESC
        LIMIT $2`,
        [userId, parseInt(limit as string)]
      );

      res.json({
        success: true,
        reports: result.rows,
      });
    } catch (error) {
      console.error('Error fetching reports:', error);
      res.status(500).json({ success: false, error: 'Failed to fetch reports' });
    }
  });

  // GET /api/reports/:id - Get specific report (requires auth)
  router.get('/:id', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const { id } = req.params;
      const userId = req.user!.userId;

      const result = await pool.query(
        `SELECT
          gr.id, gr.report_data as "reportData",
          gr.date_range_start as "dateRangeStart",
          gr.date_range_end as "dateRangeEnd",
          gr.created_at as "createdAt",
          rt.name as "templateName", rt.report_type as "reportType"
        FROM generated_reports gr
        LEFT JOIN report_templates rt ON gr.template_id = rt.id
        WHERE gr.id = $1 AND gr.user_id = $2`,
        [id, userId]
      );

      if (result.rows.length === 0) {
        res.status(404).json({ success: false, error: 'Report not found' });
        return;
      }

      res.json({
        success: true,
        report: result.rows[0],
      });
    } catch (error) {
      console.error('Error fetching report:', error);
      res.status(500).json({ success: false, error: 'Failed to fetch report' });
    }
  });

  // DELETE /api/reports/:id - Delete report (requires auth)
  router.delete('/:id', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const { id } = req.params;
      const userId = req.user!.userId;

      const result = await pool.query(
        'DELETE FROM generated_reports WHERE id = $1 AND user_id = $2 RETURNING id',
        [id, userId]
      );

      if (result.rows.length === 0) {
        res.status(404).json({ success: false, error: 'Report not found' });
        return;
      }

      res.json({ success: true, message: 'Report deleted' });
    } catch (error) {
      console.error('Error deleting report:', error);
      res.status(500).json({ success: false, error: 'Failed to delete report' });
    }
  });

  return router;
}

// Report generation functions
async function generateExecutiveSummary(
  pool: Pool,
  userId: string,
  startDate: string,
  endDate: string
): Promise<any> {
  // Overview metrics
  const overviewResult = await pool.query(
    `SELECT
      COUNT(DISTINCT ac.id)::int as total_consultations,
      COUNT(DISTINCT conv.id)::int as conversations,
      COUNT(DISTINCT di.id)::int as decisions_made,
      AVG(ac.user_rating)::numeric(3,2) as avg_satisfaction
    FROM users u
    LEFT JOIN agent_consultations ac ON u.id = ac.user_id
      AND ac.created_at BETWEEN $2 AND $3
    LEFT JOIN agent_conversations conv ON u.id = conv.user_id
      AND conv.created_at BETWEEN $2 AND $3
    LEFT JOIN decision_instances di ON u.id = di.user_id
      AND di.created_at BETWEEN $2 AND $3
    WHERE u.id = $1`,
    [userId, startDate, endDate]
  );

  // Top agents
  const topAgentsResult = await pool.query(
    `SELECT
      ba.name, ba.agent_key as "agentKey",
      COUNT(*)::int as consultations,
      AVG(ac.user_rating)::numeric(3,2) as avg_rating
    FROM agent_consultations ac
    JOIN behavior_agents ba ON ac.agent_id = ba.id
    WHERE ac.user_id = $1 AND ac.created_at BETWEEN $2 AND $3
    GROUP BY ba.id, ba.name, ba.agent_key
    ORDER BY consultations DESC
    LIMIT 5`,
    [userId, startDate, endDate]
  );

  // Outcomes summary
  const outcomesResult = await pool.query(
    `SELECT
      COUNT(*)::int as tracked_outcomes,
      AVG(success_level)::numeric(3,2) as avg_success,
      SUM(roi_estimate)::numeric(15,2) as total_roi,
      COUNT(CASE WHEN would_follow_again THEN 1 END)::int as would_follow_again
    FROM consultation_outcomes
    WHERE user_id = $1 AND created_at BETWEEN $2 AND $3`,
    [userId, startDate, endDate]
  );

  // Key decisions
  const decisionsResult = await pool.query(
    `SELECT
      dt.name as template_name,
      di.final_decision,
      di.success_rating,
      di.created_at
    FROM decision_instances di
    LEFT JOIN decision_templates dt ON di.template_id = dt.id
    WHERE di.user_id = $1
      AND di.created_at BETWEEN $2 AND $3
      AND di.status = 'decided'
    ORDER BY di.created_at DESC
    LIMIT 10`,
    [userId, startDate, endDate]
  );

  return {
    overview: overviewResult.rows[0],
    topAgents: topAgentsResult.rows,
    outcomes: outcomesResult.rows[0],
    keyDecisions: decisionsResult.rows,
    generatedAt: new Date().toISOString(),
  };
}

async function generateAgentPerformanceReport(
  pool: Pool,
  userId: string,
  startDate: string,
  endDate: string
): Promise<any> {
  const result = await pool.query(
    `SELECT
      ba.name, ba.agent_key as "agentKey", ba.title, ba.sectors,
      COUNT(ac.id)::int as total_consultations,
      AVG(ac.user_rating)::numeric(3,2) as avg_rating,
      AVG(ac.confidence_score)::numeric(3,2) as avg_confidence,
      COUNT(DISTINCT ac.decision_context) as contexts_used,
      AVG(co.success_level)::numeric(3,2) as avg_outcome_success,
      SUM(co.roi_estimate)::numeric(15,2) as total_roi
    FROM behavior_agents ba
    LEFT JOIN agent_consultations ac ON ba.id = ac.agent_id
      AND ac.user_id = $1
      AND ac.created_at BETWEEN $2 AND $3
    LEFT JOIN consultation_outcomes co ON ac.id = co.consultation_id
    WHERE ba.is_active = true
    GROUP BY ba.id, ba.name, ba.agent_key, ba.title, ba.sectors
    ORDER BY total_consultations DESC`,
    [userId, startDate, endDate]
  );

  return {
    agents: result.rows,
    generatedAt: new Date().toISOString(),
  };
}

async function generateDecisionHistoryReport(
  pool: Pool,
  userId: string,
  startDate: string,
  endDate: string
): Promise<any> {
  const decisionsResult = await pool.query(
    `SELECT
      di.id, di.status, di.final_decision, di.outcome,
      di.success_rating, di.created_at,
      dt.name as template_name, dt.category
    FROM decision_instances di
    LEFT JOIN decision_templates dt ON di.template_id = dt.id
    WHERE di.user_id = $1 AND di.created_at BETWEEN $2 AND $3
    ORDER BY di.created_at DESC`,
    [userId, startDate, endDate]
  );

  const summaryResult = await pool.query(
    `SELECT
      COUNT(*)::int as total,
      COUNT(CASE WHEN status = 'decided' THEN 1 END)::int as completed,
      COUNT(CASE WHEN status = 'in_progress' THEN 1 END)::int as in_progress,
      AVG(success_rating)::numeric(3,2) as avg_success
    FROM decision_instances
    WHERE user_id = $1 AND created_at BETWEEN $2 AND $3`,
    [userId, startDate, endDate]
  );

  return {
    summary: summaryResult.rows[0],
    decisions: decisionsResult.rows,
    generatedAt: new Date().toISOString(),
  };
}

async function generateROIAnalysisReport(
  pool: Pool,
  userId: string,
  startDate: string,
  endDate: string
): Promise<any> {
  // Overall ROI
  const overallResult = await pool.query(
    `SELECT
      COUNT(*)::int as tracked_outcomes,
      SUM(roi_estimate)::numeric(15,2) as total_roi,
      AVG(roi_estimate)::numeric(15,2) as avg_roi,
      SUM(time_saved_hours)::int as total_time_saved
    FROM consultation_outcomes
    WHERE user_id = $1 AND created_at BETWEEN $2 AND $3`,
    [userId, startDate, endDate]
  );

  // ROI by agent
  const byAgentResult = await pool.query(
    `SELECT
      ba.name, ba.agent_key as "agentKey",
      COUNT(co.id)::int as outcomes,
      SUM(co.roi_estimate)::numeric(15,2) as total_roi,
      AVG(co.roi_estimate)::numeric(15,2) as avg_roi
    FROM consultation_outcomes co
    JOIN agent_consultations ac ON co.consultation_id = ac.id
    JOIN behavior_agents ba ON ac.agent_id = ba.id
    WHERE co.user_id = $1 AND co.created_at BETWEEN $2 AND $3
    GROUP BY ba.id, ba.name, ba.agent_key
    ORDER BY total_roi DESC NULLS LAST`,
    [userId, startDate, endDate]
  );

  // ROI by context
  const byContextResult = await pool.query(
    `SELECT
      ac.decision_context,
      COUNT(co.id)::int as outcomes,
      SUM(co.roi_estimate)::numeric(15,2) as total_roi,
      AVG(co.roi_estimate)::numeric(15,2) as avg_roi
    FROM consultation_outcomes co
    JOIN agent_consultations ac ON co.consultation_id = ac.id
    WHERE co.user_id = $1 AND co.created_at BETWEEN $2 AND $3
    GROUP BY ac.decision_context
    ORDER BY total_roi DESC NULLS LAST`,
    [userId, startDate, endDate]
  );

  return {
    overall: overallResult.rows[0],
    byAgent: byAgentResult.rows,
    byContext: byContextResult.rows,
    generatedAt: new Date().toISOString(),
  };
}

async function generateTeamActivityReport(
  pool: Pool,
  userId: string,
  startDate: string,
  endDate: string,
  teamId?: string
): Promise<any> {
  if (!teamId) {
    return { error: 'Team ID required for team activity report' };
  }

  // Verify membership
  const memberCheck = await pool.query(
    'SELECT role FROM team_members WHERE team_id = $1 AND user_id = $2',
    [teamId, userId]
  );

  if (memberCheck.rows.length === 0) {
    return { error: 'Not a member of this team' };
  }

  // Team consultations
  const consultationsResult = await pool.query(
    `SELECT
      u.email, u.full_name,
      COUNT(ac.id)::int as consultations,
      AVG(ac.user_rating)::numeric(3,2) as avg_rating
    FROM team_members tm
    JOIN users u ON tm.user_id = u.id
    LEFT JOIN agent_consultations ac ON u.id = ac.user_id
      AND ac.created_at BETWEEN $2 AND $3
    WHERE tm.team_id = $1
    GROUP BY u.id, u.email, u.full_name
    ORDER BY consultations DESC`,
    [teamId, startDate, endDate]
  );

  // Shared resources
  const sharedResult = await pool.query(
    `SELECT
      COUNT(DISTINCT br.id)::int as shared_board_rooms,
      COUNT(DISTINCT ac.id)::int as shared_conversations
    FROM board_rooms br
    LEFT JOIN agent_conversations ac ON ac.team_id = $1
      AND ac.created_at BETWEEN $2 AND $3
    WHERE br.team_id = $1`,
    [teamId, startDate, endDate]
  );

  return {
    memberActivity: consultationsResult.rows,
    sharedResources: sharedResult.rows[0],
    generatedAt: new Date().toISOString(),
  };
}
