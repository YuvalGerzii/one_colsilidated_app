import { Router, Response } from 'express';
import { Pool } from 'pg';
import { authenticateToken, AuthRequest } from '../middleware/auth';

export function createSearchRoutes(pool: Pool): Router {
  const router = Router();

  // GET /api/search - Universal search across all content (requires auth)
  router.get('/', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const userId = req.user!.userId;
      const { q, type, limit = '20' } = req.query;

      if (!q || (q as string).length < 2) {
        res.status(400).json({ success: false, error: 'Search query must be at least 2 characters' });
        return;
      }

      const searchTerm = `%${(q as string).toLowerCase()}%`;
      const limitNum = Math.min(parseInt(limit as string), 100);
      const results: any = {};

      // Search based on type or all
      const searchTypes = type ? [type as string] : ['conversations', 'consultations', 'agents', 'templates', 'debates'];

      // Search conversations
      if (searchTypes.includes('conversations')) {
        const convResult = await pool.query(
          `SELECT
            ac.id, ac.title, ac.context_type as "contextType",
            ac.created_at as "createdAt",
            'conversation' as type
          FROM agent_conversations ac
          WHERE ac.user_id = $1
            AND ac.is_active = true
            AND LOWER(ac.title) LIKE $2
          ORDER BY ac.updated_at DESC
          LIMIT $3`,
          [userId, searchTerm, limitNum]
        );
        results.conversations = convResult.rows;
      }

      // Search consultations/messages
      if (searchTypes.includes('consultations')) {
        const consultResult = await pool.query(
          `SELECT
            ac.id, ac.question, ac.advice,
            ac.decision_context as "decisionContext",
            ac.created_at as "createdAt",
            ba.name as "agentName", ba.agent_key as "agentKey",
            'consultation' as type
          FROM agent_consultations ac
          JOIN behavior_agents ba ON ac.agent_id = ba.id
          WHERE ac.user_id = $1
            AND (LOWER(ac.question) LIKE $2 OR LOWER(ac.advice) LIKE $2)
          ORDER BY ac.created_at DESC
          LIMIT $3`,
          [userId, searchTerm, limitNum]
        );
        results.consultations = consultResult.rows;
      }

      // Search agents
      if (searchTypes.includes('agents')) {
        const agentResult = await pool.query(
          `SELECT
            id, agent_key as "agentKey", name, title, description,
            sectors, avatar_url as "avatarUrl",
            'agent' as type
          FROM behavior_agents
          WHERE is_active = true
            AND (
              LOWER(name) LIKE $1
              OR LOWER(title) LIKE $1
              OR LOWER(description) LIKE $1
              OR EXISTS (SELECT 1 FROM unnest(sectors) s WHERE LOWER(s) LIKE $1)
            )
          ORDER BY sort_order ASC
          LIMIT $2`,
          [searchTerm, limitNum]
        );
        results.agents = agentResult.rows;
      }

      // Search templates
      if (searchTypes.includes('templates')) {
        const templateResult = await pool.query(
          `SELECT
            id, name, description, category,
            decision_context as "decisionContext",
            'template' as type
          FROM decision_templates
          WHERE (is_public = true OR user_id = $1)
            AND (
              LOWER(name) LIKE $2
              OR LOWER(description) LIKE $2
              OR LOWER(category) LIKE $2
            )
          ORDER BY usage_count DESC
          LIMIT $3`,
          [userId, searchTerm, limitNum]
        );
        results.templates = templateResult.rows;
      }

      // Search debates
      if (searchTypes.includes('debates')) {
        const debateResult = await pool.query(
          `SELECT
            ad.id, ad.topic, ad.debate_type as "debateType",
            ad.consensus_reached as "consensusReached",
            ad.created_at as "createdAt",
            'debate' as type
          FROM agent_debates ad
          JOIN agent_conversations ac ON ad.conversation_id = ac.id
          WHERE ac.user_id = $1
            AND LOWER(ad.topic) LIKE $2
          ORDER BY ad.created_at DESC
          LIMIT $3`,
          [userId, searchTerm, limitNum]
        );
        results.debates = debateResult.rows;
      }

      // Calculate totals
      const totals = Object.entries(results).reduce((acc, [key, value]) => {
        acc[key] = (value as any[]).length;
        acc.total += (value as any[]).length;
        return acc;
      }, { total: 0 } as any);

      res.json({
        success: true,
        query: q,
        totals,
        results,
      });
    } catch (error) {
      console.error('Error searching:', error);
      res.status(500).json({ success: false, error: 'Search failed' });
    }
  });

  // GET /api/search/suggestions - Get search suggestions (requires auth)
  router.get('/suggestions', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const userId = req.user!.userId;
      const { q } = req.query;

      if (!q || (q as string).length < 2) {
        res.json({ success: true, suggestions: [] });
        return;
      }

      const searchTerm = `${(q as string).toLowerCase()}%`;

      // Get recent searches and matching items
      const suggestions: string[] = [];

      // Recent conversation titles
      const convResult = await pool.query(
        `SELECT DISTINCT title
        FROM agent_conversations
        WHERE user_id = $1 AND LOWER(title) LIKE $2
        LIMIT 5`,
        [userId, searchTerm]
      );
      convResult.rows.forEach(r => suggestions.push(r.title));

      // Agent names
      const agentResult = await pool.query(
        `SELECT name
        FROM behavior_agents
        WHERE is_active = true AND LOWER(name) LIKE $1
        LIMIT 3`,
        [searchTerm]
      );
      agentResult.rows.forEach(r => suggestions.push(r.name));

      // Template names
      const templateResult = await pool.query(
        `SELECT name
        FROM decision_templates
        WHERE (is_public = true OR user_id = $1) AND LOWER(name) LIKE $2
        LIMIT 3`,
        [userId, searchTerm]
      );
      templateResult.rows.forEach(r => suggestions.push(r.name));

      // Remove duplicates
      const uniqueSuggestions = [...new Set(suggestions)].slice(0, 10);

      res.json({
        success: true,
        suggestions: uniqueSuggestions,
      });
    } catch (error) {
      console.error('Error getting suggestions:', error);
      res.status(500).json({ success: false, error: 'Failed to get suggestions' });
    }
  });

  // GET /api/search/recent - Get recent searches (requires auth)
  router.get('/recent', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const userId = req.user!.userId;

      // Get recently accessed conversations
      const recentResult = await pool.query(
        `SELECT
          ac.id, ac.title, ac.context_type as "contextType",
          ac.updated_at as "lastAccessed"
        FROM agent_conversations ac
        WHERE ac.user_id = $1 AND ac.is_active = true
        ORDER BY ac.updated_at DESC
        LIMIT 10`,
        [userId]
      );

      // Get frequently used agents
      const frequentAgentsResult = await pool.query(
        `SELECT
          ba.agent_key as "agentKey", ba.name, ba.avatar_url as "avatarUrl",
          COUNT(*)::int as usage_count
        FROM agent_consultations ac
        JOIN behavior_agents ba ON ac.agent_id = ba.id
        WHERE ac.user_id = $1
          AND ac.created_at >= NOW() - INTERVAL '30 days'
        GROUP BY ba.id, ba.agent_key, ba.name, ba.avatar_url
        ORDER BY usage_count DESC
        LIMIT 5`,
        [userId]
      );

      res.json({
        success: true,
        recentConversations: recentResult.rows,
        frequentAgents: frequentAgentsResult.rows,
      });
    } catch (error) {
      console.error('Error getting recent items:', error);
      res.status(500).json({ success: false, error: 'Failed to get recent items' });
    }
  });

  // POST /api/search/advanced - Advanced search with filters (requires auth)
  router.post('/advanced', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const userId = req.user!.userId;
      const {
        query,
        agents,
        contexts,
        dateFrom,
        dateTo,
        minRating,
        hasOutcome,
        limit = 50,
      } = req.body;

      let sql = `
        SELECT
          ac.id, ac.question, ac.advice,
          ac.decision_context as "decisionContext",
          ac.user_rating as "rating",
          ac.confidence_score as "confidence",
          ac.created_at as "createdAt",
          ba.name as "agentName", ba.agent_key as "agentKey",
          EXISTS (
            SELECT 1 FROM consultation_outcomes co WHERE co.consultation_id = ac.id
          ) as "hasOutcome"
        FROM agent_consultations ac
        JOIN behavior_agents ba ON ac.agent_id = ba.id
        WHERE ac.user_id = $1
      `;

      const params: any[] = [userId];
      let paramIndex = 2;

      if (query && query.length >= 2) {
        sql += ` AND (LOWER(ac.question) LIKE $${paramIndex} OR LOWER(ac.advice) LIKE $${paramIndex})`;
        params.push(`%${query.toLowerCase()}%`);
        paramIndex++;
      }

      if (agents && agents.length > 0) {
        sql += ` AND ba.agent_key = ANY($${paramIndex})`;
        params.push(agents);
        paramIndex++;
      }

      if (contexts && contexts.length > 0) {
        sql += ` AND ac.decision_context = ANY($${paramIndex})`;
        params.push(contexts);
        paramIndex++;
      }

      if (dateFrom) {
        sql += ` AND ac.created_at >= $${paramIndex}`;
        params.push(dateFrom);
        paramIndex++;
      }

      if (dateTo) {
        sql += ` AND ac.created_at <= $${paramIndex}`;
        params.push(dateTo);
        paramIndex++;
      }

      if (minRating) {
        sql += ` AND ac.user_rating >= $${paramIndex}`;
        params.push(minRating);
        paramIndex++;
      }

      if (hasOutcome === true) {
        sql += ` AND EXISTS (SELECT 1 FROM consultation_outcomes co WHERE co.consultation_id = ac.id)`;
      } else if (hasOutcome === false) {
        sql += ` AND NOT EXISTS (SELECT 1 FROM consultation_outcomes co WHERE co.consultation_id = ac.id)`;
      }

      sql += ` ORDER BY ac.created_at DESC LIMIT $${paramIndex}`;
      params.push(Math.min(limit, 100));

      const result = await pool.query(sql, params);

      res.json({
        success: true,
        count: result.rows.length,
        results: result.rows,
      });
    } catch (error) {
      console.error('Error in advanced search:', error);
      res.status(500).json({ success: false, error: 'Advanced search failed' });
    }
  });

  return router;
}
