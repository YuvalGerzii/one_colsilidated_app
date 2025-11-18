import { Router, Response } from 'express';
import { Pool } from 'pg';
import Redis from 'ioredis';
import { authenticateToken, AuthRequest } from '../middleware/auth';
import { BehaviorAgentFactory } from '../../src/agents/BehaviorAgentFactory';
import { DecisionContext } from '../../src/types/BehaviorAgentTypes';

export function createDebateRoutes(pool: Pool, redis: Redis): Router {
  const router = Router();
  const factory = new BehaviorAgentFactory(pool, redis);

  // POST /api/debates - Create and run an agent debate (requires auth)
  router.post('/', authenticateToken, async (req: AuthRequest, res: Response) => {
    const client = await pool.connect();

    try {
      const userId = req.user!.userId;
      const {
        conversationId,
        topic,
        debateType = 'roundtable',
        agentKeys,
        decisionContext = 'GENERAL',
        rounds = 2,
      } = req.body;

      // Validation
      if (!topic || !agentKeys || agentKeys.length < 2) {
        res.status(400).json({
          success: false,
          error: 'Topic and at least 2 agents are required',
        });
        return;
      }

      if (agentKeys.length > 6) {
        res.status(400).json({
          success: false,
          error: 'Maximum 6 agents allowed in a debate',
        });
        return;
      }

      await client.query('BEGIN');

      // Get agent IDs
      const agentsResult = await client.query(
        `SELECT id, agent_key FROM behavior_agents WHERE agent_key = ANY($1)`,
        [agentKeys]
      );

      if (agentsResult.rows.length !== agentKeys.length) {
        res.status(404).json({ success: false, error: 'One or more agents not found' });
        return;
      }

      const agentIds = agentsResult.rows.map((r) => r.id);
      const agents = agentKeys.map((key: string) => factory.getAgentByName(key)!);

      // Create debate record
      const debateResult = await client.query(
        `INSERT INTO agent_debates (
          conversation_id, topic, debate_type, participating_agents
        )
        VALUES ($1, $2, $3, $4)
        RETURNING id, created_at as "createdAt"`,
        [conversationId, topic, debateType, agentIds]
      );

      const debateId = debateResult.rows[0].id;

      // Run the debate
      const debateData: any = {
        topic,
        type: debateType,
        rounds: [],
      };

      for (let round = 1; round <= rounds; round++) {
        const roundData: any = {
          roundNumber: round,
          arguments: [],
        };

        // Each agent provides their perspective
        for (let i = 0; i < agents.length; i++) {
          const agent = agents[i];
          const agentId = agentsResult.rows[i].id;

          // Build context from previous rounds
          let contextualQuestion = topic;
          if (round > 1) {
            const previousArguments = debateData.rounds
              .flatMap((r: any) => r.arguments)
              .map((a: any) => `${a.agentName}: ${a.summary}`)
              .join('\n');

            contextualQuestion = `${topic}\n\nPrevious perspectives:\n${previousArguments}\n\nProvide your counter-arguments and additional insights:`;
          }

          // Get agent's position
          const advice = await agent.getAdvice(
            contextualQuestion,
            decisionContext as DecisionContext
          );

          // Save debate message
          const messageType = round === 1 ? 'opening' : round === rounds ? 'closing' : 'argument';

          await client.query(
            `INSERT INTO debate_messages (
              debate_id, agent_id, round_number, message_type, content, supporting_data
            )
            VALUES ($1, $2, $3, $4, $5, $6)`,
            [
              debateId,
              agentId,
              round,
              messageType,
              advice.advice,
              JSON.stringify({
                actionableSteps: advice.actionableSteps,
                potentialRisks: advice.potentialRisks,
                successProbability: advice.successProbability,
              }),
            ]
          );

          roundData.arguments.push({
            agentKey: agentKeys[i],
            agentName: agent.profile.name,
            position: advice.advice,
            summary: advice.actionableSteps[0] || 'No summary available',
            confidence: advice.successProbability,
            risks: advice.potentialRisks,
          });
        }

        debateData.rounds.push(roundData);
      }

      // Analyze consensus
      const allAdvices = debateData.rounds.flatMap((r: any) =>
        r.arguments.map((a: any) => a.position)
      );

      // Simple consensus detection (look for common themes)
      const commonThemes = this.extractCommonThemes(allAdvices);
      const consensusReached = commonThemes.length > 0;

      // Generate final recommendation
      const finalRecommendation = this.generateFinalRecommendation(debateData, consensusReached);

      // Update debate record
      await client.query(
        `UPDATE agent_debates
        SET debate_data = $1, consensus_reached = $2, final_recommendation = $3, completed_at = NOW()
        WHERE id = $4`,
        [JSON.stringify(debateData), consensusReached, finalRecommendation, debateId]
      );

      await client.query('COMMIT');

      res.status(201).json({
        success: true,
        debate: {
          id: debateId,
          topic,
          type: debateType,
          rounds: debateData.rounds,
          consensusReached,
          finalRecommendation,
          commonThemes,
          createdAt: debateResult.rows[0].createdAt,
        },
      });
    } catch (error) {
      await client.query('ROLLBACK');
      console.error('Error creating debate:', error);
      res.status(500).json({ success: false, error: 'Failed to create debate' });
    } finally {
      client.release();
    }
  });

  // Helper method to extract common themes
  (router as any).extractCommonThemes = function (advices: string[]): string[] {
    const themes: string[] = [];
    const commonKeywords = [
      'innovation',
      'customer',
      'market',
      'risk',
      'growth',
      'efficiency',
      'quality',
      'speed',
      'data',
      'team',
      'investment',
      'timing',
    ];

    // Count keyword occurrences
    const keywordCounts: { [key: string]: number } = {};
    commonKeywords.forEach((keyword) => {
      const count = advices.filter((advice) =>
        advice.toLowerCase().includes(keyword)
      ).length;
      if (count >= advices.length / 2) {
        // If mentioned by at least half the agents
        keywordCounts[keyword] = count;
      }
    });

    // Return top themes
    return Object.entries(keywordCounts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 3)
      .map(([keyword]) => keyword);
  };

  // Helper method to generate final recommendation
  (router as any).generateFinalRecommendation = function (
    debateData: any,
    consensusReached: boolean
  ): string {
    if (consensusReached) {
      return `After ${debateData.rounds.length} rounds of debate, the panel reached consensus. The collective recommendation emphasizes the importance of balanced execution considering multiple perspectives.`;
    } else {
      return `After ${debateData.rounds.length} rounds of debate, the agents presented diverse viewpoints. Consider the trade-offs between different approaches and choose based on your specific context and priorities.`;
    }
  };

  // GET /api/debates - Get user's debates (requires auth)
  router.get('/', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const userId = req.user!.userId;

      const result = await pool.query(
        `SELECT
          ad.id, ad.topic, ad.debate_type as "debateType",
          ad.consensus_reached as "consensusReached",
          ad.final_recommendation as "finalRecommendation",
          ad.created_at as "createdAt", ad.completed_at as "completedAt",
          ac.id as "conversationId",
          ac.title as "conversationTitle",
          array_agg(ba.name) as "participatingAgents"
        FROM agent_debates ad
        JOIN agent_conversations ac ON ad.conversation_id = ac.id
        LEFT JOIN LATERAL unnest(ad.participating_agents) WITH ORDINALITY AS agent_id ON true
        LEFT JOIN behavior_agents ba ON ba.id = agent_id
        WHERE ac.user_id = $1
        GROUP BY ad.id, ac.id
        ORDER BY ad.created_at DESC
        LIMIT 50`,
        [userId]
      );

      res.json({
        success: true,
        debates: result.rows,
      });
    } catch (error) {
      console.error('Error fetching debates:', error);
      res.status(500).json({ success: false, error: 'Failed to fetch debates' });
    }
  });

  // GET /api/debates/:id - Get specific debate details (requires auth)
  router.get('/:id', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const { id } = req.params;
      const userId = req.user!.userId;

      // Get debate with full details
      const debateResult = await pool.query(
        `SELECT
          ad.id, ad.topic, ad.debate_type as "debateType",
          ad.participating_agents as "participatingAgentIds",
          ad.debate_data as "debateData",
          ad.consensus_reached as "consensusReached",
          ad.final_recommendation as "finalRecommendation",
          ad.created_at as "createdAt", ad.completed_at as "completedAt"
        FROM agent_debates ad
        JOIN agent_conversations ac ON ad.conversation_id = ac.id
        WHERE ad.id = $1 AND ac.user_id = $2`,
        [id, userId]
      );

      if (debateResult.rows.length === 0) {
        res.status(404).json({ success: false, error: 'Debate not found' });
        return;
      }

      // Get all debate messages
      const messagesResult = await pool.query(
        `SELECT
          dm.id, dm.round_number as "roundNumber",
          dm.message_type as "messageType", dm.content,
          dm.supporting_data as "supportingData",
          dm.created_at as "createdAt",
          ba.agent_key as "agentKey", ba.name as "agentName",
          ba.avatar_url as "avatarUrl"
        FROM debate_messages dm
        JOIN behavior_agents ba ON dm.agent_id = ba.id
        WHERE dm.debate_id = $1
        ORDER BY dm.round_number ASC, dm.created_at ASC`,
        [id]
      );

      res.json({
        success: true,
        debate: {
          ...debateResult.rows[0],
          messages: messagesResult.rows,
        },
      });
    } catch (error) {
      console.error('Error fetching debate details:', error);
      res.status(500).json({ success: false, error: 'Failed to fetch debate details' });
    }
  });

  // POST /api/debates/:id/compare - Compare agent positions (requires auth)
  router.post('/:id/compare', authenticateToken, async (req: AuthRequest, res: Response) => {
    try {
      const { id } = req.params;
      const userId = req.user!.userId;
      const { agentKeys } = req.body;

      if (!agentKeys || agentKeys.length !== 2) {
        res.status(400).json({ success: false, error: 'Exactly 2 agents required for comparison' });
        return;
      }

      // Get debate messages for these agents
      const result = await pool.query(
        `SELECT
          dm.round_number as "roundNumber",
          dm.message_type as "messageType",
          dm.content,
          dm.supporting_data as "supportingData",
          ba.agent_key as "agentKey",
          ba.name as "agentName"
        FROM debate_messages dm
        JOIN behavior_agents ba ON dm.agent_id = ba.id
        JOIN agent_debates ad ON dm.debate_id = ad.id
        JOIN agent_conversations ac ON ad.conversation_id = ac.id
        WHERE dm.debate_id = $1
          AND ba.agent_key = ANY($2)
          AND ac.user_id = $3
        ORDER BY dm.round_number ASC, ba.agent_key ASC`,
        [id, agentKeys, userId]
      );

      // Group by agent
      const comparison: any = {
        [agentKeys[0]]: [],
        [agentKeys[1]]: [],
      };

      result.rows.forEach((row) => {
        comparison[row.agentKey].push({
          round: row.roundNumber,
          type: row.messageType,
          content: row.content,
          supportingData: row.supportingData,
        });
      });

      // Generate comparison matrix
      const comparisonMatrix = {
        similarities: this.findSimilarities(
          comparison[agentKeys[0]],
          comparison[agentKeys[1]]
        ),
        differences: this.findDifferences(
          comparison[agentKeys[0]],
          comparison[agentKeys[1]]
        ),
      };

      // Save comparison
      const agentIds = await pool.query(
        'SELECT id FROM behavior_agents WHERE agent_key = ANY($1)',
        [agentKeys]
      );

      await pool.query(
        `INSERT INTO agent_comparisons (
          user_id, question, compared_agents, comparison_matrix
        )
        VALUES ($1, $2, $3, $4)`,
        [
          userId,
          `Debate comparison: ${agentKeys.join(' vs ')}`,
          agentIds.rows.map((r) => r.id),
          JSON.stringify(comparisonMatrix),
        ]
      );

      res.json({
        success: true,
        comparison: {
          agents: agentKeys,
          positions: comparison,
          analysis: comparisonMatrix,
        },
      });
    } catch (error) {
      console.error('Error comparing agents:', error);
      res.status(500).json({ success: false, error: 'Failed to compare agents' });
    }
  });

  // Helper methods for comparison
  (router as any).findSimilarities = function (agent1Positions: any[], agent2Positions: any[]): string[] {
    // Simplified similarity detection
    const similarities: string[] = [];
    const keywords = ['focus', 'prioritize', 'important', 'key', 'essential'];

    keywords.forEach((keyword) => {
      const in1 = agent1Positions.some((p) => p.content.toLowerCase().includes(keyword));
      const in2 = agent2Positions.some((p) => p.content.toLowerCase().includes(keyword));
      if (in1 && in2) {
        similarities.push(`Both emphasize the importance of ${keyword}`);
      }
    });

    return similarities;
  };

  (router as any).findDifferences = function (agent1Positions: any[], agent2Positions: any[]): string[] {
    // Simplified difference detection
    return [
      'Different approaches to risk management',
      'Varied perspectives on timeline and execution',
      'Divergent views on resource allocation',
    ];
  };

  return router;
}
