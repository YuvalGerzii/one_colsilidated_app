import { Router } from 'express';
import { Pool } from 'pg';
import Redis from 'ioredis';
import { MatchQualityAgent } from '../../src/agents/MatchQualityAgent';
import { SixDegreesAgent } from '../../src/agents/SixDegreesAgent';
import { TrustPropagationAgent } from '../../src/agents/TrustPropagationAgent';
import { SerendipityAgent } from '../../src/agents/SerendipityAgent';
import { CommunityDetectionAgent } from '../../src/agents/CommunityDetectionAgent';
import { ConnectionStrengthAnalyzer } from '../../src/agents/ConnectionStrengthAnalyzer';
import { NetworkTraversalAgent } from '../../src/agents/NetworkTraversalAgent';
import { OptimizedNetworkCalculations } from '../../src/agents/OptimizedNetworkCalculations';

const router = Router();

let matchQualityAgent: MatchQualityAgent;

export function initializeMatchQualityRoutes(pool: Pool, redis: Redis) {
  const traversalAgent = new NetworkTraversalAgent(pool, redis);
  const optimizedCalc = new OptimizedNetworkCalculations(pool, redis);
  const sixDegreesAgent = new SixDegreesAgent(pool, redis, traversalAgent);
  const trustAgent = new TrustPropagationAgent(pool, redis);
  const serendipityAgent = new SerendipityAgent(pool, redis, traversalAgent, optimizedCalc);
  const communityAgent = new CommunityDetectionAgent(pool, redis);
  const strengthAnalyzer = new ConnectionStrengthAnalyzer(pool, redis, optimizedCalc);

  matchQualityAgent = new MatchQualityAgent(
    pool,
    redis,
    sixDegreesAgent,
    trustAgent,
    serendipityAgent,
    communityAgent,
    strengthAnalyzer
  );
}

/**
 * GET /api/match-quality/:targetId
 * Calculate match quality between authenticated user and target user
 */
router.get('/:targetId', async (req, res) => {
  try {
    const userId = (req as any).user?.id;
    if (!userId) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    const { targetId } = req.params;
    const { useCache = 'true', includeExplanation = 'true' } = req.query;

    const matchScore = await matchQualityAgent.calculateMatchQuality(userId, targetId, {
      useCache: useCache === 'true',
      includeExplanation: includeExplanation === 'true'
    });

    res.json({
      success: true,
      match: matchScore
    });
  } catch (error: any) {
    console.error('Error calculating match quality:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to calculate match quality',
      message: error.message
    });
  }
});

/**
 * POST /api/match-quality/compare
 * Compare match quality between two users (bidirectional)
 */
router.post('/compare', async (req, res) => {
  try {
    const userId = (req as any).user?.id;
    if (!userId) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    const { targetId } = req.body;

    if (!targetId) {
      return res.status(400).json({ error: 'targetId is required' });
    }

    const comparison = await matchQualityAgent.compareMatchMutuality(userId, targetId);

    res.json({
      success: true,
      comparison
    });
  } catch (error: any) {
    console.error('Error comparing match mutuality:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to compare match mutuality',
      message: error.message
    });
  }
});

/**
 * GET /api/match-quality/best-matches
 * Find best matches for authenticated user
 */
router.get('/best-matches', async (req, res) => {
  try {
    const userId = (req as any).user?.id;
    if (!userId) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    const {
      limit = 20,
      minScore = 50,
      excludeExisting = 'true',
      diversityWeight = 0.3
    } = req.query;

    const matches = await matchQualityAgent.findBestMatches(userId, {
      limit: parseInt(limit as string),
      minScore: parseInt(minScore as string),
      excludeExisting: excludeExisting === 'true',
      diversityWeight: parseFloat(diversityWeight as string)
    });

    res.json({
      success: true,
      count: matches.length,
      matches
    });
  } catch (error: any) {
    console.error('Error finding best matches:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to find best matches',
      message: error.message
    });
  }
});

/**
 * POST /api/match-quality/batch
 * Calculate match quality for multiple targets at once
 */
router.post('/batch', async (req, res) => {
  try {
    const userId = (req as any).user?.id;
    if (!userId) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    const { targetIds } = req.body;

    if (!Array.isArray(targetIds) || targetIds.length === 0) {
      return res.status(400).json({ error: 'targetIds array is required' });
    }

    if (targetIds.length > 50) {
      return res.status(400).json({ error: 'Maximum 50 targets allowed per batch' });
    }

    const scoreMap = await matchQualityAgent.batchCalculateScores(userId, targetIds);

    // Convert map to array for JSON response
    const scores = Array.from(scoreMap.entries()).map(([targetId, score]) => ({
      targetId,
      ...score
    }));

    res.json({
      success: true,
      count: scores.length,
      scores
    });
  } catch (error: any) {
    console.error('Error calculating batch scores:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to calculate batch scores',
      message: error.message
    });
  }
});

export default router;
