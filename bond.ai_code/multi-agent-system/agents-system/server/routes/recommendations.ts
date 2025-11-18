import { Router, Response } from 'express';
import { Pool } from 'pg';
import Redis from 'ioredis';
import { authenticateToken, AuthRequest } from '../middleware/auth';

export function createRecommendationRoutes(pool: Pool, redis: Redis): Router {
  const router = Router();

  // GET /api/recommendations/agents - Get agent recommendations for question (requires auth)
  router.get('/agents', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const userId = req.user!.userId;
      const { question, context } = req.query;

      if (!question) {
        res.status(400).json({ success: false, error: 'Question is required' });
        return;
      }

      const recommendations: any[] = [];
      const questionLower = (question as string).toLowerCase();

      // Keyword-based context detection
      const contextKeywords: Record<string, string[]> = {
        'STRATEGIC_PLANNING': ['strategy', 'long-term', 'vision', 'roadmap', 'plan'],
        'PRODUCT_DEVELOPMENT': ['product', 'feature', 'launch', 'build', 'develop', 'design'],
        'ACQUISITION': ['acquire', 'buy', 'merger', 'acquisition', 'm&a'],
        'INVESTMENT': ['invest', 'funding', 'capital', 'roi', 'return'],
        'NEGOTIATION': ['negotiate', 'deal', 'contract', 'terms', 'agreement'],
        'TEAM_BUILDING': ['hire', 'team', 'talent', 'recruit', 'culture'],
        'CRISIS_MANAGEMENT': ['crisis', 'urgent', 'emergency', 'problem', 'issue'],
        'MARKET_EXPANSION': ['market', 'expand', 'growth', 'scale', 'international'],
        'FINANCIAL_PLANNING': ['budget', 'finance', 'cost', 'revenue', 'profit'],
        'RISK_ASSESSMENT': ['risk', 'assess', 'evaluate', 'danger', 'threat'],
      };

      // Detect context from question
      let detectedContext = context as string || 'GENERAL';
      if (!context) {
        for (const [ctx, keywords] of Object.entries(contextKeywords)) {
          if (keywords.some(kw => questionLower.includes(kw))) {
            detectedContext = ctx;
            break;
          }
        }
      }

      // Agent specializations
      const agentSpecializations: Record<string, { contexts: string[]; keywords: string[] }> = {
        'musk': {
          contexts: ['STRATEGIC_PLANNING', 'PRODUCT_DEVELOPMENT', 'INNOVATION'],
          keywords: ['innovation', 'technology', 'disrupt', 'physics', 'space', 'electric', 'ai'],
        },
        'jobs': {
          contexts: ['PRODUCT_DEVELOPMENT', 'STRATEGIC_PLANNING'],
          keywords: ['design', 'user', 'experience', 'simplicity', 'product', 'quality'],
        },
        'bezos': {
          contexts: ['MARKET_EXPANSION', 'STRATEGIC_PLANNING', 'PRODUCT_DEVELOPMENT'],
          keywords: ['customer', 'scale', 'growth', 'ecommerce', 'logistics', 'data'],
        },
        'zuckerberg': {
          contexts: ['PRODUCT_DEVELOPMENT', 'MARKET_EXPANSION', 'STRATEGIC_PLANNING'],
          keywords: ['social', 'network', 'growth', 'data', 'platform', 'metaverse'],
        },
        'fink': {
          contexts: ['INVESTMENT', 'FINANCIAL_PLANNING', 'RISK_ASSESSMENT'],
          keywords: ['investment', 'portfolio', 'risk', 'sustainable', 'long-term', 'capital'],
        },
        'trump': {
          contexts: ['NEGOTIATION', 'REAL_ESTATE'],
          keywords: ['negotiate', 'deal', 'brand', 'real estate', 'media', 'marketing'],
        },
        'zell': {
          contexts: ['INVESTMENT', 'RISK_ASSESSMENT', 'ACQUISITION'],
          keywords: ['distressed', 'value', 'contrarian', 'real estate', 'opportunity'],
        },
        'bren': {
          contexts: ['STRATEGIC_PLANNING', 'REAL_ESTATE'],
          keywords: ['quality', 'long-term', 'sustainability', 'development', 'vision'],
        },
      };

      // Score each agent
      const agentScores: { key: string; score: number; reasons: string[] }[] = [];

      for (const [agentKey, specialization] of Object.entries(agentSpecializations)) {
        let score = 0;
        const reasons: string[] = [];

        // Context match
        if (specialization.contexts.includes(detectedContext)) {
          score += 30;
          reasons.push(`Specializes in ${detectedContext.toLowerCase().replace('_', ' ')}`);
        }

        // Keyword match
        const matchedKeywords = specialization.keywords.filter(kw => questionLower.includes(kw));
        if (matchedKeywords.length > 0) {
          score += matchedKeywords.length * 15;
          reasons.push(`Keywords: ${matchedKeywords.join(', ')}`);
        }

        agentScores.push({ key: agentKey, score, reasons });
      }

      // Get user's historical success with agents
      const historyResult = await pool.query(
        `SELECT
          ba.agent_key,
          COUNT(*)::int as consultations,
          AVG(ac.user_rating)::numeric(3,2) as avg_rating,
          AVG(co.success_level)::numeric(3,2) as avg_success
        FROM agent_consultations ac
        JOIN behavior_agents ba ON ac.agent_id = ba.id
        LEFT JOIN consultation_outcomes co ON ac.id = co.consultation_id
        WHERE ac.user_id = $1
          AND ac.decision_context = $2
        GROUP BY ba.agent_key`,
        [userId, detectedContext]
      );

      // Adjust scores based on history
      for (const history of historyResult.rows) {
        const agentScore = agentScores.find(a => a.key === history.agent_key);
        if (agentScore) {
          if (history.avg_success && parseFloat(history.avg_success) >= 4) {
            agentScore.score += 20;
            agentScore.reasons.push(`High success rate in similar decisions (${history.avg_success}/5)`);
          }
          if (history.avg_rating && parseFloat(history.avg_rating) >= 4) {
            agentScore.score += 10;
            agentScore.reasons.push(`Highly rated by you (${history.avg_rating}/5)`);
          }
        }
      }

      // Sort by score and get top agents
      agentScores.sort((a, b) => b.score - a.score);
      const topAgents = agentScores.slice(0, 4);

      // Get full agent details
      const agentKeys = topAgents.map(a => a.key);
      const agentsResult = await pool.query(
        `SELECT
          agent_key as "agentKey", name, title, avatar_url as "avatarUrl", sectors
        FROM behavior_agents
        WHERE agent_key = ANY($1)`,
        [agentKeys]
      );

      // Combine results
      for (const agent of agentsResult.rows) {
        const scoreInfo = topAgents.find(a => a.key === agent.agentKey);
        recommendations.push({
          ...agent,
          score: scoreInfo?.score || 0,
          reasons: scoreInfo?.reasons || [],
        });
      }

      // Sort recommendations by score
      recommendations.sort((a, b) => b.score - a.score);

      res.json({
        success: true,
        question,
        detectedContext,
        recommendations,
      });
    } catch (error) {
      console.error('Error getting agent recommendations:', error);
      res.status(500).json({ success: false, error: 'Failed to get recommendations' });
    }
  });

  // GET /api/recommendations/templates - Get template recommendations (requires auth)
  router.get('/templates', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const userId = req.user!.userId;
      const { question, context } = req.query;

      // Find templates matching the context or keywords
      const result = await pool.query(
        `SELECT
          id, name, description, category,
          decision_context as "decisionContext",
          recommended_agents as "recommendedAgents",
          usage_count as "usageCount"
        FROM decision_templates
        WHERE (is_public = true OR user_id = $1)
          AND ($2::text IS NULL OR decision_context = $2)
        ORDER BY usage_count DESC
        LIMIT 5`,
        [userId, context || null]
      );

      res.json({
        success: true,
        templates: result.rows,
      });
    } catch (error) {
      console.error('Error getting template recommendations:', error);
      res.status(500).json({ success: false, error: 'Failed to get recommendations' });
    }
  });

  // GET /api/recommendations/board-rooms - Get board room recommendations (requires auth)
  router.get('/board-rooms', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const userId = req.user!.userId;
      const { question, sector } = req.query;

      const result = await pool.query(
        `SELECT
          br.id, br.name, br.description,
          br.focus_sectors as "focusSectors",
          br.decision_style as "decisionStyle",
          array_agg(ba.name) as "memberNames"
        FROM board_rooms br
        JOIN board_room_members brm ON br.id = brm.board_room_id
        JOIN behavior_agents ba ON brm.agent_id = ba.id
        WHERE br.is_predefined = true AND br.is_active = true
          AND ($1::text IS NULL OR $1 = ANY(br.focus_sectors))
        GROUP BY br.id
        ORDER BY br.name`,
        [sector || null]
      );

      res.json({
        success: true,
        boardRooms: result.rows,
      });
    } catch (error) {
      console.error('Error getting board room recommendations:', error);
      res.status(500).json({ success: false, error: 'Failed to get recommendations' });
    }
  });

  // GET /api/recommendations/follow-up - Get follow-up recommendations (requires auth)
  router.get('/follow-up', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const userId = req.user!.userId;

      // Find consultations without outcomes that are old enough
      const pendingOutcomes = await pool.query(
        `SELECT
          ac.id as "consultationId",
          ac.question,
          ac.created_at as "consultedAt",
          ba.name as "agentName",
          ac.decision_context as "decisionContext"
        FROM agent_consultations ac
        JOIN behavior_agents ba ON ac.agent_id = ba.id
        WHERE ac.user_id = $1
          AND ac.created_at <= NOW() - INTERVAL '7 days'
          AND NOT EXISTS (
            SELECT 1 FROM consultation_outcomes co WHERE co.consultation_id = ac.id
          )
        ORDER BY ac.created_at DESC
        LIMIT 10`,
        [userId]
      );

      // Find decisions without final decision
      const pendingDecisions = await pool.query(
        `SELECT
          di.id as "decisionId",
          dt.name as "templateName",
          di.created_at as "startedAt"
        FROM decision_instances di
        LEFT JOIN decision_templates dt ON di.template_id = dt.id
        WHERE di.user_id = $1
          AND di.status = 'in_progress'
          AND di.created_at <= NOW() - INTERVAL '3 days'
        ORDER BY di.created_at DESC
        LIMIT 5`,
        [userId]
      );

      res.json({
        success: true,
        followUps: {
          pendingOutcomes: pendingOutcomes.rows,
          pendingDecisions: pendingDecisions.rows,
        },
      });
    } catch (error) {
      console.error('Error getting follow-up recommendations:', error);
      res.status(500).json({ success: false, error: 'Failed to get follow-up recommendations' });
    }
  });

  return router;
}
