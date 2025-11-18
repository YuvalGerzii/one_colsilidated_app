import { Router, Response } from 'express';
import { Pool } from 'pg';
import { authenticateToken, AuthRequest } from '../middleware/auth';

export function createTemplateRoutes(pool: Pool): Router {
  const router = Router();

  // GET /api/templates - Get available decision templates
  router.get('/', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const userId = req.user!.userId;
      const { category } = req.query;

      let query = `
        SELECT
          id, name, description, category, decision_context as "decisionContext",
          recommended_agents as "recommendedAgents", template_data as "templateData",
          usage_count as "usageCount", is_public as "isPublic",
          created_at as "createdAt"
        FROM decision_templates
        WHERE (is_public = true OR user_id = $1)
          AND (team_id IS NULL OR team_id IN (
            SELECT team_id FROM team_members WHERE user_id = $1
          ))
      `;

      const params = [userId];

      if (category) {
        query += ` AND category = $2`;
        params.push(category as string);
      }

      query += ` ORDER BY usage_count DESC, created_at DESC`;

      const result = await pool.query(query, params);

      res.json({
        success: true,
        templates: result.rows,
      });
    } catch (error) {
      console.error('Error fetching templates:', error);
      res.status(500).json({ success: false, error: 'Failed to fetch templates' });
    }
  });

  // GET /api/templates/:id - Get specific template
  router.get('/:id', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const { id } = req.params;
      const userId = req.user!.userId;

      const result = await pool.query(
        `SELECT
          dt.id, dt.name, dt.description, dt.category,
          dt.decision_context as "decisionContext",
          dt.recommended_agents as "recommendedAgents",
          dt.recommended_board_room_id as "recommendedBoardRoomId",
          dt.template_data as "templateData",
          dt.usage_count as "usageCount",
          dt.is_public as "isPublic",
          dt.created_at as "createdAt",
          br.name as "recommendedBoardRoomName"
        FROM decision_templates dt
        LEFT JOIN board_rooms br ON dt.recommended_board_room_id = br.id
        WHERE dt.id = $1
          AND (dt.is_public = true OR dt.user_id = $2)`,
        [id, userId]
      );

      if (result.rows.length === 0) {
        res.status(404).json({ success: false, error: 'Template not found' });
        return;
      }

      res.json({
        success: true,
        template: result.rows[0],
      });
    } catch (error) {
      console.error('Error fetching template:', error);
      res.status(500).json({ success: false, error: 'Failed to fetch template' });
    }
  });

  // POST /api/templates - Create custom template (requires auth)
  router.post('/', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const userId = req.user!.userId;
      const {
        name,
        description,
        category,
        decisionContext,
        recommendedAgents,
        recommendedBoardRoomId,
        templateData,
        isPublic = false,
        teamId,
      } = req.body;

      // Validation
      if (!name || !templateData) {
        res.status(400).json({ success: false, error: 'Name and templateData are required' });
        return;
      }

      const result = await pool.query(
        `INSERT INTO decision_templates (
          user_id, team_id, name, description, category, decision_context,
          recommended_agents, recommended_board_room_id, template_data, is_public
        )
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
        RETURNING id, name, description, category, created_at as "createdAt"`,
        [
          userId,
          teamId || null,
          name,
          description || null,
          category || null,
          decisionContext || null,
          recommendedAgents || null,
          recommendedBoardRoomId || null,
          JSON.stringify(templateData),
          isPublic,
        ]
      );

      res.status(201).json({
        success: true,
        template: result.rows[0],
      });
    } catch (error) {
      console.error('Error creating template:', error);
      res.status(500).json({ success: false, error: 'Failed to create template' });
    }
  });

  // PUT /api/templates/:id - Update template (requires auth)
  router.put('/:id', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const { id } = req.params;
      const userId = req.user!.userId;
      const {
        name,
        description,
        category,
        decisionContext,
        recommendedAgents,
        recommendedBoardRoomId,
        templateData,
        isPublic,
      } = req.body;

      // Check ownership
      const ownerCheck = await pool.query(
        'SELECT id FROM decision_templates WHERE id = $1 AND user_id = $2',
        [id, userId]
      );

      if (ownerCheck.rows.length === 0) {
        res.status(404).json({ success: false, error: 'Template not found or access denied' });
        return;
      }

      const result = await pool.query(
        `UPDATE decision_templates
        SET name = COALESCE($1, name),
            description = COALESCE($2, description),
            category = COALESCE($3, category),
            decision_context = COALESCE($4, decision_context),
            recommended_agents = COALESCE($5, recommended_agents),
            recommended_board_room_id = COALESCE($6, recommended_board_room_id),
            template_data = COALESCE($7, template_data),
            is_public = COALESCE($8, is_public)
        WHERE id = $9 AND user_id = $10
        RETURNING id, name, description, category, updated_at as "updatedAt"`,
        [
          name,
          description,
          category,
          decisionContext,
          recommendedAgents,
          recommendedBoardRoomId,
          templateData ? JSON.stringify(templateData) : null,
          isPublic,
          id,
          userId,
        ]
      );

      res.json({
        success: true,
        template: result.rows[0],
      });
    } catch (error) {
      console.error('Error updating template:', error);
      res.status(500).json({ success: false, error: 'Failed to update template' });
    }
  });

  // DELETE /api/templates/:id - Delete template (requires auth)
  router.delete('/:id', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const { id } = req.params;
      const userId = req.user!.userId;

      const result = await pool.query(
        'DELETE FROM decision_templates WHERE id = $1 AND user_id = $2 RETURNING id',
        [id, userId]
      );

      if (result.rows.length === 0) {
        res.status(404).json({ success: false, error: 'Template not found or access denied' });
        return;
      }

      res.json({
        success: true,
        message: 'Template deleted successfully',
      });
    } catch (error) {
      console.error('Error deleting template:', error);
      res.status(500).json({ success: false, error: 'Failed to delete template' });
    }
  });

  // POST /api/templates/:id/use - Use a template to create decision instance (requires auth)
  router.post('/:id/use', authenticateToken, async (req: AuthRequest, res: Response) => {
    const client = await pool.connect();

    try {
      const { id } = req.params;
      const userId = req.user!.userId;
      const { instanceData, conversationId } = req.body;

      if (!instanceData) {
        res.status(400).json({ success: false, error: 'instanceData is required' });
        return;
      }

      // Get template
      const templateResult = await client.query(
        'SELECT * FROM decision_templates WHERE id = $1',
        [id]
      );

      if (templateResult.rows.length === 0) {
        res.status(404).json({ success: false, error: 'Template not found' });
        return;
      }

      await client.query('BEGIN');

      // Create decision instance
      const instanceResult = await client.query(
        `INSERT INTO decision_instances (
          template_id, user_id, conversation_id, instance_data, status
        )
        VALUES ($1, $2, $3, $4, 'in_progress')
        RETURNING id, status, created_at as "createdAt"`,
        [id, userId, conversationId || null, JSON.stringify(instanceData)]
      );

      // Increment template usage
      await client.query(
        'UPDATE decision_templates SET usage_count = usage_count + 1 WHERE id = $1',
        [id]
      );

      await client.query('COMMIT');

      res.status(201).json({
        success: true,
        decisionInstance: {
          ...instanceResult.rows[0],
          template: templateResult.rows[0],
        },
      });
    } catch (error) {
      await client.query('ROLLBACK');
      console.error('Error using template:', error);
      res.status(500).json({ success: false, error: 'Failed to use template' });
    } finally {
      client.release();
    }
  });

  // GET /api/templates/instances - Get user's decision instances (requires auth)
  router.get('/instances/my', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const userId = req.user!.userId;
      const { status } = req.query;

      let query = `
        SELECT
          di.id, di.instance_data as "instanceData", di.status,
          di.final_decision as "finalDecision", di.outcome,
          di.success_rating as "successRating", di.created_at as "createdAt",
          dt.name as "templateName", dt.category
        FROM decision_instances di
        LEFT JOIN decision_templates dt ON di.template_id = dt.id
        WHERE di.user_id = $1
      `;

      const params = [userId];

      if (status) {
        query += ` AND di.status = $2`;
        params.push(status as string);
      }

      query += ` ORDER BY di.created_at DESC`;

      const result = await pool.query(query, params);

      res.json({
        success: true,
        instances: result.rows,
      });
    } catch (error) {
      console.error('Error fetching decision instances:', error);
      res.status(500).json({ success: false, error: 'Failed to fetch decision instances' });
    }
  });

  // PUT /api/templates/instances/:id - Update decision instance (requires auth)
  router.put('/instances/:id', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const { id } = req.params;
      const userId = req.user!.userId;
      const { status, finalDecision, outcome, successRating } = req.body;

      const result = await pool.query(
        `UPDATE decision_instances
        SET status = COALESCE($1, status),
            final_decision = COALESCE($2, final_decision),
            outcome = COALESCE($3, outcome),
            success_rating = COALESCE($4, success_rating)
        WHERE id = $5 AND user_id = $6
        RETURNING id, status, final_decision as "finalDecision", outcome, success_rating as "successRating"`,
        [status, finalDecision, outcome, successRating, id, userId]
      );

      if (result.rows.length === 0) {
        res.status(404).json({ success: false, error: 'Decision instance not found' });
        return;
      }

      res.json({
        success: true,
        instance: result.rows[0],
      });
    } catch (error) {
      console.error('Error updating decision instance:', error);
      res.status(500).json({ success: false, error: 'Failed to update decision instance' });
    }
  });

  return router;
}
