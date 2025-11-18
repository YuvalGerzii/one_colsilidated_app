import { Router } from 'express';
import { Pool } from 'pg';
import Redis from 'ioredis';
import { CommunityDetectionAgent } from '../../src/agents/CommunityDetectionAgent';
import { TemporalAnalysisAgent } from '../../src/agents/TemporalAnalysisAgent';

const router = Router();

let communityAgent: CommunityDetectionAgent;
let temporalAgent: TemporalAnalysisAgent;

export function initializeNetworkAnalysisRoutes(pool: Pool, redis: Redis) {
  communityAgent = new CommunityDetectionAgent(pool, redis);
  temporalAgent = new TemporalAnalysisAgent(pool, redis);
}

/**
 * GET /api/network-analysis/communities
 * Detect communities in the network
 */
router.get('/communities', async (req, res) => {
  try {
    const userId = (req as any).user?.id;
    if (!userId) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    const { minCommunitySize = 3 } = req.query;

    const structure = await communityAgent.detectCommunities(
      parseInt(minCommunitySize as string)
    );

    res.json({
      success: true,
      structure
    });
  } catch (error: any) {
    console.error('Error detecting communities:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to detect communities',
      message: error.message
    });
  }
});

/**
 * GET /api/network-analysis/communities/user/:userId
 * Get community information for a specific user
 */
router.get('/communities/user/:userId', async (req, res) => {
  try {
    const requestingUserId = (req as any).user?.id;
    if (!requestingUserId) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    const { userId } = req.params;

    const overlap = await communityAgent.analyzeCommunityOverlap(userId);

    res.json({
      success: true,
      overlap
    });
  } catch (error: any) {
    console.error('Error analyzing community overlap:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to analyze community overlap',
      message: error.message
    });
  }
});

/**
 * GET /api/network-analysis/communities/recommendations
 * Get community-related recommendations for user
 */
router.get('/communities/recommendations', async (req, res) => {
  try {
    const userId = (req as any).user?.id;
    if (!userId) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    const recommendations = await communityAgent.recommendCommunityActions(userId);

    res.json({
      success: true,
      recommendations
    });
  } catch (error: any) {
    console.error('Error generating community recommendations:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to generate community recommendations',
      message: error.message
    });
  }
});

/**
 * GET /api/network-analysis/temporal/snapshot
 * Capture current network snapshot for user
 */
router.get('/temporal/snapshot', async (req, res) => {
  try {
    const userId = (req as any).user?.id;
    if (!userId) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    const snapshot = await temporalAgent.captureSnapshot(userId);

    res.json({
      success: true,
      snapshot
    });
  } catch (error: any) {
    console.error('Error capturing snapshot:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to capture snapshot',
      message: error.message
    });
  }
});

/**
 * GET /api/network-analysis/temporal/trends
 * Analyze network trends over time
 */
router.get('/temporal/trends', async (req, res) => {
  try {
    const userId = (req as any).user?.id;
    if (!userId) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    const { timeframe = 'month' } = req.query;

    if (!['week', 'month', 'quarter', 'year'].includes(timeframe as string)) {
      return res.status(400).json({ error: 'Invalid timeframe' });
    }

    const trends = await temporalAgent.analyzeTrends(
      userId,
      timeframe as 'week' | 'month' | 'quarter' | 'year'
    );

    res.json({
      success: true,
      timeframe,
      trends
    });
  } catch (error: any) {
    console.error('Error analyzing trends:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to analyze trends',
      message: error.message
    });
  }
});

/**
 * GET /api/network-analysis/temporal/trajectory
 * Analyze user's network trajectory
 */
router.get('/temporal/trajectory', async (req, res) => {
  try {
    const userId = (req as any).user?.id;
    if (!userId) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    const trajectory = await temporalAgent.analyzeUserTrajectory(userId);

    res.json({
      success: true,
      trajectory
    });
  } catch (error: any) {
    console.error('Error analyzing trajectory:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to analyze trajectory',
      message: error.message
    });
  }
});

/**
 * GET /api/network-analysis/temporal/health
 * Generate network health report
 */
router.get('/temporal/health', async (req, res) => {
  try {
    const userId = (req as any).user?.id;
    if (!userId) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    const healthReport = await temporalAgent.generateHealthReport(userId);

    res.json({
      success: true,
      report: healthReport
    });
  } catch (error: any) {
    console.error('Error generating health report:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to generate health report',
      message: error.message
    });
  }
});

/**
 * POST /api/network-analysis/temporal/compare
 * Compare two time periods
 */
router.post('/temporal/compare', async (req, res) => {
  try {
    const userId = (req as any).user?.id;
    if (!userId) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    const { period1Start, period1End, period2Start, period2End } = req.body;

    if (!period1Start || !period1End || !period2Start || !period2End) {
      return res.status(400).json({ error: 'All period dates are required' });
    }

    const comparison = await temporalAgent.compareTimePeriods(
      userId,
      new Date(period1Start),
      new Date(period1End),
      new Date(period2Start),
      new Date(period2End)
    );

    res.json({
      success: true,
      comparison
    });
  } catch (error: any) {
    console.error('Error comparing periods:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to compare periods',
      message: error.message
    });
  }
});

export default router;
