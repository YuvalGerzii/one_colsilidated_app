import { Router } from 'express';
import { Pool } from 'pg';
import Redis from 'ioredis';
import { CollaborationPredictionAgent } from '../../src/agents/CollaborationPredictionAgent';
import { MatchQualityAgent } from '../../src/agents/MatchQualityAgent';
import { TrustPropagationAgent } from '../../src/agents/TrustPropagationAgent';
import { SixDegreesAgent } from '../../src/agents/SixDegreesAgent';
import { SerendipityAgent } from '../../src/agents/SerendipityAgent';
import { CommunityDetectionAgent } from '../../src/agents/CommunityDetectionAgent';
import { ConnectionStrengthAnalyzer } from '../../src/agents/ConnectionStrengthAnalyzer';
import { NetworkTraversalAgent } from '../../src/agents/NetworkTraversalAgent';
import { OptimizedNetworkCalculations } from '../../src/agents/OptimizedNetworkCalculations';

const router = Router();

let collaborationAgent: CollaborationPredictionAgent;

export function initializeCollaborationRoutes(pool: Pool, redis: Redis) {
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

  collaborationAgent = new CollaborationPredictionAgent(
    pool,
    redis,
    matchQualityAgent,
    trustAgent
  );
}

/**
 * POST /api/collaboration/predict
 * Predict collaboration success between two users
 */
router.post('/predict', async (req, res) => {
  try {
    const userId = (req as any).user?.id;
    if (!userId) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    const { targetId } = req.body;

    if (!targetId) {
      return res.status(400).json({ error: 'targetId is required' });
    }

    const prediction = await collaborationAgent.predictCollaboration(userId, targetId);

    res.json({
      success: true,
      prediction
    });
  } catch (error: any) {
    console.error('Error predicting collaboration:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to predict collaboration',
      message: error.message
    });
  }
});

/**
 * GET /api/collaboration/opportunities
 * Find collaboration opportunities for authenticated user
 */
router.get('/opportunities', async (req, res) => {
  try {
    const userId = (req as any).user?.id;
    if (!userId) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    const {
      type,
      minProbability = 60,
      limit = 10
    } = req.query;

    const validTypes = ['project', 'introduction', 'advisory', 'co_creation', 'investment'];
    if (type && !validTypes.includes(type as string)) {
      return res.status(400).json({ error: 'Invalid opportunity type' });
    }

    const opportunities = await collaborationAgent.findCollaborationOpportunities(userId, {
      type: type as any,
      minProbability: parseInt(minProbability as string),
      limit: parseInt(limit as string)
    });

    res.json({
      success: true,
      count: opportunities.length,
      opportunities
    });
  } catch (error: any) {
    console.error('Error finding collaboration opportunities:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to find collaboration opportunities',
      message: error.message
    });
  }
});

/**
 * POST /api/collaboration/team-compatibility
 * Analyze compatibility for a team of users
 */
router.post('/team-compatibility', async (req, res) => {
  try {
    const userId = (req as any).user?.id;
    if (!userId) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    const { teamMembers } = req.body;

    if (!Array.isArray(teamMembers) || teamMembers.length < 2) {
      return res.status(400).json({ error: 'teamMembers array with at least 2 members is required' });
    }

    if (teamMembers.length > 10) {
      return res.status(400).json({ error: 'Maximum 10 team members allowed' });
    }

    // Ensure authenticated user is in the team
    if (!teamMembers.includes(userId)) {
      teamMembers.push(userId);
    }

    const compatibility = await collaborationAgent.analyzeTeamCompatibility(teamMembers);

    // Convert nested maps to objects for JSON response
    const pairwiseScoresObj: any = {};
    compatibility.pairwiseScores.forEach((scores, user1) => {
      const scoresObj: any = {};
      scores.forEach((score, user2) => {
        scoresObj[user2] = score;
      });
      pairwiseScoresObj[user1] = scoresObj;
    });

    const recommendedRolesObj: any = {};
    compatibility.recommendedRoles.forEach((role, userId) => {
      recommendedRolesObj[userId] = role;
    });

    res.json({
      success: true,
      compatibility: {
        ...compatibility,
        pairwiseScores: pairwiseScoresObj,
        recommendedRoles: recommendedRolesObj
      }
    });
  } catch (error: any) {
    console.error('Error analyzing team compatibility:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to analyze team compatibility',
      message: error.message
    });
  }
});

/**
 * POST /api/collaboration/predict-scenario
 * Predict success of a specific collaboration scenario
 */
router.post('/predict-scenario', async (req, res) => {
  try {
    const userId = (req as any).user?.id;
    if (!userId) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    const { participants, scenario } = req.body;

    if (!Array.isArray(participants) || participants.length < 2) {
      return res.status(400).json({ error: 'participants array with at least 2 members is required' });
    }

    if (!scenario || !scenario.type || !scenario.duration || !scenario.complexity || !Array.isArray(scenario.requiredSkills)) {
      return res.status(400).json({
        error: 'scenario object with type, duration, complexity, and requiredSkills is required'
      });
    }

    // Ensure authenticated user is in participants
    if (!participants.includes(userId)) {
      participants.push(userId);
    }

    const prediction = await collaborationAgent.predictScenario(participants, scenario);

    res.json({
      success: true,
      prediction
    });
  } catch (error: any) {
    console.error('Error predicting scenario:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to predict scenario',
      message: error.message
    });
  }
});

export default router;
