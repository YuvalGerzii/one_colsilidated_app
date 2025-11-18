import { Router, Response } from 'express';
import { Pool } from 'pg';
import { authenticateToken, optionalAuth, AuthRequest } from '../middleware/auth';

export function createAgentRoutes(pool: Pool): Router {
  const router = Router();

  // GET /api/agents - Get all active behavior agents
  router.get('/', async (req, res: Response) => {
    try {
      const result = await pool.query(
        `SELECT
          id, agent_key as "agentKey", name, title, description,
          companies, sectors, avatar_url as "avatarUrl", sort_order as "sortOrder"
        FROM behavior_agents
        WHERE is_active = true
        ORDER BY sort_order ASC`
      );

      res.json({
        success: true,
        agents: result.rows,
      });
    } catch (error) {
      console.error('Error fetching agents:', error);
      res.status(500).json({ success: false, error: 'Failed to fetch agents' });
    }
  });

  // GET /api/agents/:agentKey - Get specific agent details
  router.get('/:agentKey', async (req, res: Response) => {
    try {
      const { agentKey } = req.params;

      const result = await pool.query(
        `SELECT
          id, agent_key as "agentKey", name, title, description,
          companies, sectors, avatar_url as "avatarUrl", sort_order as "sortOrder",
          created_at as "createdAt"
        FROM behavior_agents
        WHERE agent_key = $1 AND is_active = true`,
        [agentKey]
      );

      if (result.rows.length === 0) {
        res.status(404).json({ success: false, error: 'Agent not found' });
        return;
      }

      res.json({
        success: true,
        agent: result.rows[0],
      });
    } catch (error) {
      console.error('Error fetching agent:', error);
      res.status(500).json({ success: false, error: 'Failed to fetch agent' });
    }
  });

  // GET /api/agents/:agentKey/stats - Get agent statistics (requires auth)
  router.get('/:agentKey/stats', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const { agentKey } = req.params;
      const userId = req.user!.userId;

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

      // Get consultation statistics
      const statsResult = await pool.query(
        `SELECT
          COUNT(*)::int as total_consultations,
          AVG(user_rating)::numeric(3,2) as average_rating
        FROM agent_consultations
        WHERE agent_id = $1 AND user_rating IS NOT NULL`,
        [agentId]
      );

      // Get user preferences
      const prefResult = await pool.query(
        `SELECT
          is_favorite as "isFavorite",
          usage_count as "usageCount",
          last_used_at as "lastUsed"
        FROM user_agent_preferences
        WHERE user_id = $1 AND agent_id = $2`,
        [userId, agentId]
      );

      const stats = statsResult.rows[0];
      const prefs = prefResult.rows[0] || {
        isFavorite: false,
        usageCount: 0,
        lastUsed: null,
      };

      res.json({
        success: true,
        stats: {
          totalConsultations: stats.total_consultations || 0,
          averageRating: parseFloat(stats.average_rating) || null,
          isFavorite: prefs.isFavorite,
          usageCount: prefs.usageCount,
          lastUsed: prefs.lastUsed,
        },
      });
    } catch (error) {
      console.error('Error fetching agent stats:', error);
      res.status(500).json({ success: false, error: 'Failed to fetch agent statistics' });
    }
  });

  // POST /api/agents/:agentKey/favorite - Toggle favorite status (requires auth)
  router.post('/:agentKey/favorite', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const { agentKey } = req.params;
      const { isFavorite } = req.body;
      const userId = req.user!.userId;

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

      // Upsert preference
      await pool.query(
        `INSERT INTO user_agent_preferences (user_id, agent_id, is_favorite)
        VALUES ($1, $2, $3)
        ON CONFLICT (user_id, agent_id)
        DO UPDATE SET is_favorite = $3`,
        [userId, agentId, isFavorite]
      );

      res.json({
        success: true,
        message: isFavorite ? 'Agent added to favorites' : 'Agent removed from favorites',
      });
    } catch (error) {
      console.error('Error updating favorite status:', error);
      res.status(500).json({ success: false, error: 'Failed to update favorite status' });
    }
  });

  // GET /api/agents/favorites/list - Get user's favorite agents (requires auth)
  router.get('/favorites/list', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const userId = req.user!.userId;

      const result = await pool.query(
        `SELECT
          ba.id, ba.agent_key as "agentKey", ba.name, ba.title,
          ba.avatar_url as "avatarUrl", uap.usage_count as "usageCount",
          uap.last_used_at as "lastUsed"
        FROM user_agent_preferences uap
        JOIN behavior_agents ba ON uap.agent_id = ba.id
        WHERE uap.user_id = $1 AND uap.is_favorite = true
        ORDER BY uap.last_used_at DESC NULLS LAST`,
        [userId]
      );

      res.json({
        success: true,
        favorites: result.rows,
      });
    } catch (error) {
      console.error('Error fetching favorites:', error);
      res.status(500).json({ success: false, error: 'Failed to fetch favorites' });
    }
  });

  // GET /api/agents/by-sector/:sector - Get agents by business sector
  router.get('/by-sector/:sector', async (req, res: Response) => {
    try {
      const { sector } = req.params;

      const result = await pool.query(
        `SELECT
          id, agent_key as "agentKey", name, title, description,
          companies, sectors, avatar_url as "avatarUrl", sort_order as "sortOrder"
        FROM behavior_agents
        WHERE $1 = ANY(sectors) AND is_active = true
        ORDER BY sort_order ASC`,
        [sector]
      );

      res.json({
        success: true,
        sector,
        agents: result.rows,
      });
    } catch (error) {
      console.error('Error fetching agents by sector:', error);
      res.status(500).json({ success: false, error: 'Failed to fetch agents by sector' });
    }
  });

  return router;
}
