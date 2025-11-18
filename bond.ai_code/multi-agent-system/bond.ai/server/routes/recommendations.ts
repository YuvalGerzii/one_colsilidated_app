import { Router } from 'express';
import { Pool } from 'pg';
import Redis from 'ioredis';
import { RecommendationEngine } from '../../src/agents/RecommendationEngine';
import { MatchQualityAgent } from '../../src/agents/MatchQualityAgent';
import { SixDegreesAgent } from '../../src/agents/SixDegreesAgent';
import { TrustPropagationAgent } from '../../src/agents/TrustPropagationAgent';
import { SerendipityAgent } from '../../src/agents/SerendipityAgent';
import { CommunityDetectionAgent } from '../../src/agents/CommunityDetectionAgent';
import { ConnectionStrengthAnalyzer } from '../../src/agents/ConnectionStrengthAnalyzer';
import { NetworkTraversalAgent } from '../../src/agents/NetworkTraversalAgent';
import { OptimizedNetworkCalculations } from '../../src/agents/OptimizedNetworkCalculations';

const router = Router();

// Initialize agents (would be done in app initialization in production)
let recommendationEngine: RecommendationEngine;

export function initializeRecommendationRoutes(pool: Pool, redis: Redis) {
  const traversalAgent = new NetworkTraversalAgent(pool, redis);
  const optimizedCalc = new OptimizedNetworkCalculations(pool, redis);
  const sixDegreesAgent = new SixDegreesAgent(pool, redis, traversalAgent);
  const trustAgent = new TrustPropagationAgent(pool, redis);
  const serendipityAgent = new SerendipityAgent(pool, redis, traversalAgent, optimizedCalc);
  const communityAgent = new CommunityDetectionAgent(pool, redis);
  const strengthAnalyzer = new ConnectionStrengthAnalyzer(pool, redis, optimizedCalc);
  const matchQualityAgent = new MatchQualityAgent(
    pool,
    redis,
    sixDegreesAgent,
    trustAgent,
    serendipityAgent,
    communityAgent,
    strengthAnalyzer
  );

  recommendationEngine = new RecommendationEngine(
    pool,
    redis,
    matchQualityAgent,
    sixDegreesAgent,
    trustAgent,
    serendipityAgent,
    communityAgent,
    strengthAnalyzer
  );
}

/**
 * GET /api/recommendations
 * Get personalized recommendations for authenticated user
 */
router.get('/', async (req, res) => {
  try {
    const userId = (req as any).user?.id;
    if (!userId) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    const {
      limit = 10,
      includeIntroductions = 'true',
      includeGapFill = 'true',
      includeDiversity = 'true',
      minScore = 60
    } = req.query;

    const recommendations = await recommendationEngine.getRecommendations(userId, {
      limit: parseInt(limit as string),
      includeIntroductions: includeIntroductions === 'true',
      includeGapFill: includeGapFill === 'true',
      includeDiversity: includeDiversity === 'true',
      minScore: parseInt(minScore as string)
    });

    res.json({
      success: true,
      count: recommendations.length,
      recommendations
    });
  } catch (error: any) {
    console.error('Error fetching recommendations:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch recommendations',
      message: error.message
    });
  }
});

/**
 * GET /api/recommendations/network-gaps
 * Analyze network gaps for authenticated user
 */
router.get('/network-gaps', async (req, res) => {
  try {
    const userId = (req as any).user?.id;
    if (!userId) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    const gapAnalysis = await recommendationEngine.analyzeNetworkGaps(userId);

    res.json({
      success: true,
      analysis: gapAnalysis
    });
  } catch (error: any) {
    console.error('Error analyzing network gaps:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to analyze network gaps',
      message: error.message
    });
  }
});

/**
 * GET /api/recommendations/weekly-digest
 * Get weekly digest for authenticated user
 */
router.get('/weekly-digest', async (req, res) => {
  try {
    const userId = (req as any).user?.id;
    if (!userId) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    const weekStart = req.query.weekStart
      ? new Date(req.query.weekStart as string)
      : new Date();

    const digest = await recommendationEngine.generateWeeklyDigest(userId, weekStart);

    res.json({
      success: true,
      digest
    });
  } catch (error: any) {
    console.error('Error generating weekly digest:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to generate weekly digest',
      message: error.message
    });
  }
});

/**
 * POST /api/recommendations/goal
 * Get recommendations based on specific goal
 */
router.post('/goal', async (req, res) => {
  try {
    const userId = (req as any).user?.id;
    if (!userId) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    const { goalType, targetIndustry, targetExpertise, targetCommunity, customDescription, timeframe } = req.body;

    if (!goalType) {
      return res.status(400).json({ error: 'goalType is required' });
    }

    const recommendations = await recommendationEngine.getGoalRecommendations(userId, {
      goalType,
      targetIndustry,
      targetExpertise,
      targetCommunity,
      customDescription,
      timeframe
    });

    res.json({
      success: true,
      count: recommendations.length,
      recommendations
    });
  } catch (error: any) {
    console.error('Error generating goal recommendations:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to generate goal recommendations',
      message: error.message
    });
  }
});

export default router;
