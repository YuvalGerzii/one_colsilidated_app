import { Pool } from 'pg';
import Redis from 'ioredis';
import { MatchQualityAgent, MatchScore } from './MatchQualityAgent';
import { SixDegreesAgent } from './SixDegreesAgent';
import { TrustPropagationAgent } from './TrustPropagationAgent';
import { SerendipityAgent } from './SerendipityAgent';
import { CommunityDetectionAgent } from './CommunityDetectionAgent';
import { ConnectionStrengthAnalyzer } from './ConnectionStrengthAnalyzer';

/**
 * Recommendation Engine
 *
 * Orchestrates all agents to provide strategic, personalized connection recommendations.
 *
 * Key capabilities:
 * - Personalized match recommendations
 * - Strategic network gap analysis
 * - Introduction path suggestions
 * - Network diversification recommendations
 * - Weekly digest generation
 * - Goal-oriented recommendations
 */

export interface Recommendation {
  id: string;
  type: 'match' | 'introduction' | 'gap_fill' | 'diversify' | 'strengthen' | 'strategic';
  priority: 'high' | 'medium' | 'low';
  targetUserId: string;
  targetName: string;
  score: number; // 0-100
  confidence: number; // 0-1

  title: string;
  description: string;
  reasoning: string[];

  actionSteps: Array<{
    step: number;
    action: string;
    difficulty: 'easy' | 'medium' | 'hard';
    estimatedTime: string;
  }>;

  expectedOutcomes: string[];
  potentialRisks: string[];

  timeframe: string; // "This week", "This month", etc.
  expiresAt?: Date;
}

export interface NetworkGapAnalysis {
  userId: string;
  overallHealth: number; // 0-100
  gaps: Array<{
    type: 'industry' | 'geography' | 'expertise' | 'role' | 'community';
    description: string;
    severity: 'critical' | 'important' | 'minor';
    recommendations: string[];
  }>;
  strengths: string[];
  opportunities: string[];
}

export interface WeeklyDigest {
  userId: string;
  weekStart: Date;
  weekEnd: Date;

  topRecommendations: Recommendation[];
  networkInsights: {
    newConnections: number;
    networkGrowth: number; // percentage
    trustIncreases: Array<{ userId: string; userName: string; increase: number }>;
    communityChanges: string[];
  };
  activitySummary: {
    connectionsReached: number;
    introductionsMade: number;
    opportunitiesEngaged: number;
  };
  nextWeekFocus: string[];
}

export interface StrategicGoal {
  goalType: 'expand_industry' | 'build_expertise' | 'increase_centrality' | 'join_community' | 'custom';
  targetIndustry?: string;
  targetExpertise?: string;
  targetCommunity?: string;
  customDescription?: string;
  timeframe: 'week' | 'month' | 'quarter' | 'year';
}

export class RecommendationEngine {
  constructor(
    private pool: Pool,
    private redis: Redis,
    private matchQualityAgent: MatchQualityAgent,
    private sixDegreesAgent: SixDegreesAgent,
    private trustAgent: TrustPropagationAgent,
    private serendipityAgent: SerendipityAgent,
    private communityAgent: CommunityDetectionAgent,
    private strengthAnalyzer: ConnectionStrengthAnalyzer
  ) {}

  /**
   * Get personalized recommendations for a user
   */
  async getRecommendations(
    userId: string,
    options: {
      limit?: number;
      includeIntroductions?: boolean;
      includeGapFill?: boolean;
      includeDiversity?: boolean;
      minScore?: number;
    } = {}
  ): Promise<Recommendation[]> {
    const {
      limit = 10,
      includeIntroductions = true,
      includeGapFill = true,
      includeDiversity = true,
      minScore = 60
    } = options;

    const allRecommendations: Recommendation[] = [];

    // 1. Best matches (always included)
    const matchRecommendations = await this.generateMatchRecommendations(
      userId,
      Math.ceil(limit * 0.4),
      minScore
    );
    allRecommendations.push(...matchRecommendations);

    // 2. Introduction opportunities
    if (includeIntroductions) {
      const introRecommendations = await this.generateIntroductionRecommendations(
        userId,
        Math.ceil(limit * 0.2)
      );
      allRecommendations.push(...introRecommendations);
    }

    // 3. Gap filling
    if (includeGapFill) {
      const gapRecommendations = await this.generateGapFillingRecommendations(
        userId,
        Math.ceil(limit * 0.2)
      );
      allRecommendations.push(...gapRecommendations);
    }

    // 4. Diversity & serendipity
    if (includeDiversity) {
      const diversityRecommendations = await this.generateDiversityRecommendations(
        userId,
        Math.ceil(limit * 0.2)
      );
      allRecommendations.push(...diversityRecommendations);
    }

    // Sort by priority and score
    const priorityWeight = { high: 3, medium: 2, low: 1 };
    allRecommendations.sort((a, b) => {
      const priorityDiff = priorityWeight[b.priority] - priorityWeight[a.priority];
      if (priorityDiff !== 0) return priorityDiff;
      return b.score - a.score;
    });

    return allRecommendations.slice(0, limit);
  }

  /**
   * Analyze network gaps and provide improvement suggestions
   */
  async analyzeNetworkGaps(userId: string): Promise<NetworkGapAnalysis> {
    const [
      userProfile,
      connections,
      communityData,
      centralityData,
      diversityData
    ] = await Promise.all([
      this.getUserProfile(userId),
      this.getUserConnections(userId),
      this.communityAgent.analyzeCommunityOverlap(userId),
      this.strengthAnalyzer.calculateCentrality(userId),
      this.serendipityAgent.analyzeNetworkDiversity(userId)
    ]);

    const gaps: NetworkGapAnalysis['gaps'] = [];
    const strengths: string[] = [];
    const opportunities: string[] = [];

    // Analyze industry diversity
    const industries = await this.getConnectionIndustries(userId);
    if (industries.size < 3) {
      gaps.push({
        type: 'industry',
        description: `Limited industry diversity (${industries.size} industries)`,
        severity: 'important',
        recommendations: [
          'Connect with professionals in complementary industries',
          'Attend cross-industry networking events',
          'Explore adjacent market opportunities'
        ]
      });
    } else {
      strengths.push(`Strong industry diversity (${industries.size} industries)`);
    }

    // Analyze geographic diversity
    const countries = await this.getConnectionCountries(userId);
    if (countries.size < 2) {
      gaps.push({
        type: 'geography',
        description: 'Limited geographic reach',
        severity: 'minor',
        recommendations: [
          'Connect with international professionals',
          'Join global communities',
          'Attend virtual international events'
        ]
      });
    } else {
      strengths.push(`Global network across ${countries.size} countries`);
    }

    // Analyze expertise gaps
    const expertiseGaps = await this.findExpertiseGaps(userId);
    if (expertiseGaps.length > 0) {
      gaps.push({
        type: 'expertise',
        description: `Missing expertise areas: ${expertiseGaps.slice(0, 3).join(', ')}`,
        severity: 'important',
        recommendations: [
          `Connect with experts in ${expertiseGaps[0]}`,
          'Diversify skill network',
          'Build relationships with complementary skill sets'
        ]
      });
    }

    // Community analysis
    if (communityData.role === 'isolated') {
      gaps.push({
        type: 'community',
        description: 'Not integrated into any community',
        severity: 'critical',
        recommendations: [
          'Join relevant professional communities',
          'Engage with industry groups',
          'Attend community events'
        ]
      });
    } else if (communityData.role === 'core_member') {
      strengths.push(`Core member of ${communityData.primaryCommunity}`);
    } else if (communityData.role === 'bridge') {
      strengths.push('Strategic bridge between communities');
      opportunities.push('Leverage bridge position for introductions');
    }

    // Centrality analysis
    if (centralityData.degreeCentrality < 0.1) {
      gaps.push({
        type: 'role',
        description: 'Low network centrality - limited influence',
        severity: 'important',
        recommendations: [
          'Increase number of quality connections',
          'Engage more actively with network',
          'Position yourself as a connector'
        ]
      });
    } else if (centralityData.betweenness > 0.3) {
      strengths.push('High betweenness centrality - key connector');
      opportunities.push('Monetize connector role through introductions');
    }

    // Calculate overall health
    const healthFactors = [
      industries.size >= 3 ? 25 : (industries.size * 8),
      countries.size >= 3 ? 20 : (countries.size * 7),
      expertiseGaps.length === 0 ? 20 : Math.max(0, 20 - expertiseGaps.length * 5),
      communityData.role !== 'isolated' ? 20 : 0,
      centralityData.degreeCentrality * 100 * 0.15
    ];
    const overallHealth = Math.round(healthFactors.reduce((sum, val) => sum + val, 0));

    return {
      userId,
      overallHealth,
      gaps,
      strengths,
      opportunities
    };
  }

  /**
   * Generate weekly digest for user
   */
  async generateWeeklyDigest(
    userId: string,
    weekStart: Date = new Date()
  ): Promise<WeeklyDigest> {
    const weekEnd = new Date(weekStart);
    weekEnd.setDate(weekEnd.getDate() + 7);

    // Get top recommendations
    const topRecommendations = await this.getRecommendations(userId, {
      limit: 5,
      minScore: 65
    });

    // Network insights (would need historical data tracking)
    const networkInsights = {
      newConnections: 0, // TODO: Track from activity log
      networkGrowth: 0,
      trustIncreases: [],
      communityChanges: []
    };

    // Activity summary
    const activitySummary = {
      connectionsReached: 0,
      introductionsMade: 0,
      opportunitiesEngaged: 0
    };

    // Next week focus
    const gapAnalysis = await this.analyzeNetworkGaps(userId);
    const nextWeekFocus = gapAnalysis.gaps
      .filter(g => g.severity === 'critical' || g.severity === 'important')
      .slice(0, 3)
      .map(g => g.recommendations[0]);

    return {
      userId,
      weekStart,
      weekEnd,
      topRecommendations,
      networkInsights,
      activitySummary,
      nextWeekFocus
    };
  }

  /**
   * Get goal-oriented recommendations
   */
  async getGoalRecommendations(
    userId: string,
    goal: StrategicGoal
  ): Promise<Recommendation[]> {
    const recommendations: Recommendation[] = [];

    switch (goal.goalType) {
      case 'expand_industry':
        if (goal.targetIndustry) {
          const industryRecs = await this.generateIndustryExpansionRecs(
            userId,
            goal.targetIndustry
          );
          recommendations.push(...industryRecs);
        }
        break;

      case 'build_expertise':
        if (goal.targetExpertise) {
          const expertiseRecs = await this.generateExpertiseRecs(
            userId,
            goal.targetExpertise
          );
          recommendations.push(...expertiseRecs);
        }
        break;

      case 'increase_centrality':
        const centralityRecs = await this.generateCentralityRecs(userId);
        recommendations.push(...centralityRecs);
        break;

      case 'join_community':
        const communityRecs = await this.generateCommunityJoinRecs(userId);
        recommendations.push(...communityRecs);
        break;
    }

    return recommendations;
  }

  /**
   * Private recommendation generation methods
   */

  private async generateMatchRecommendations(
    userId: string,
    limit: number,
    minScore: number
  ): Promise<Recommendation[]> {
    const matches = await this.matchQualityAgent.findBestMatches(userId, {
      limit: limit * 2,
      minScore,
      excludeExisting: true,
      diversityWeight: 0.2
    });

    return Promise.all(
      matches.slice(0, limit).map(match => this.matchToRecommendation(match, 'match'))
    );
  }

  private async generateIntroductionRecommendations(
    userId: string,
    limit: number
  ): Promise<Recommendation[]> {
    // Find users at 2-3 degrees who would be valuable
    const candidates = await this.findIntroductionCandidates(userId);
    const scored = await this.matchQualityAgent.batchCalculateScores(
      userId,
      candidates.slice(0, 20)
    );

    const recommendations: Recommendation[] = [];

    for (const [targetId, match] of scored) {
      if (match.features.networkDistance >= 2 && match.features.networkDistance <= 3) {
        const rec = await this.matchToRecommendation(match, 'introduction');
        recommendations.push(rec);
      }
    }

    return recommendations.slice(0, limit);
  }

  private async generateGapFillingRecommendations(
    userId: string,
    limit: number
  ): Promise<Recommendation[]> {
    const gapAnalysis = await this.analyzeNetworkGaps(userId);
    const recommendations: Recommendation[] = [];

    // For each critical/important gap, find candidates who fill it
    for (const gap of gapAnalysis.gaps) {
      if (gap.severity === 'critical' || gap.severity === 'important') {
        const gapFillers = await this.findGapFillers(userId, gap);

        for (const targetId of gapFillers.slice(0, 2)) {
          const match = await this.matchQualityAgent.calculateMatchQuality(userId, targetId);
          const rec = await this.matchToRecommendation(match, 'gap_fill');
          rec.description = `Fills ${gap.type} gap: ${gap.description}`;
          recommendations.push(rec);
        }
      }
    }

    return recommendations.slice(0, limit);
  }

  private async generateDiversityRecommendations(
    userId: string,
    limit: number
  ): Promise<Recommendation[]> {
    const serendipityMatches = await this.serendipityAgent.findSerendipitousMatches(
      userId,
      limit * 2
    );

    const recommendations: Recommendation[] = [];

    for (const sMatch of serendipityMatches.slice(0, limit)) {
      const match = await this.matchQualityAgent.calculateMatchQuality(userId, sMatch.targetId);
      const rec = await this.matchToRecommendation(match, 'diversify');
      rec.description = `Serendipitous match: ${sMatch.insight}`;
      rec.reasoning.unshift(...sMatch.reasons.map(r => r.description));
      recommendations.push(rec);
    }

    return recommendations;
  }

  /**
   * Goal-specific recommendation generators
   */

  private async generateIndustryExpansionRecs(
    userId: string,
    targetIndustry: string
  ): Promise<Recommendation[]> {
    const candidates = await this.findByIndustry(targetIndustry);
    const scored = await this.matchQualityAgent.batchCalculateScores(
      userId,
      candidates.slice(0, 20)
    );

    const recommendations: Recommendation[] = [];

    for (const [targetId, match] of scored) {
      if (match.overallScore >= 55) {
        const rec = await this.matchToRecommendation(match, 'strategic');
        rec.title = `Expand into ${targetIndustry}`;
        rec.description = `Strategic connection in ${targetIndustry} industry`;
        recommendations.push(rec);
      }
    }

    return recommendations.slice(0, 5);
  }

  private async generateExpertiseRecs(
    userId: string,
    targetExpertise: string
  ): Promise<Recommendation[]> {
    const candidates = await this.findByExpertise(targetExpertise);
    const scored = await this.matchQualityAgent.batchCalculateScores(
      userId,
      candidates.slice(0, 20)
    );

    const recommendations: Recommendation[] = [];

    for (const [targetId, match] of scored) {
      if (match.overallScore >= 50) {
        const rec = await this.matchToRecommendation(match, 'strategic');
        rec.title = `Build ${targetExpertise} expertise`;
        rec.description = `Connect with ${targetExpertise} expert`;
        recommendations.push(rec);
      }
    }

    return recommendations.slice(0, 5);
  }

  private async generateCentralityRecs(userId: string): Promise<Recommendation[]> {
    const superConnectors = await this.sixDegreesAgent.findSuperConnectors(10);
    const scored = await this.matchQualityAgent.batchCalculateScores(
      userId,
      superConnectors.map(sc => sc.userId)
    );

    const recommendations: Recommendation[] = [];

    for (const [targetId, match] of scored) {
      const rec = await this.matchToRecommendation(match, 'strategic');
      rec.title = 'Increase network centrality';
      rec.description = 'Connect with highly influential network member';
      recommendations.push(rec);
    }

    return recommendations.slice(0, 5);
  }

  private async generateCommunityJoinRecs(userId: string): Promise<Recommendation[]> {
    const communityData = await this.communityAgent.recommendCommunityActions(userId);
    const recommendations: Recommendation[] = [];

    for (const action of communityData) {
      if (action.type === 'join_community' && action.targetCommunity) {
        const community = await this.getCommunity(action.targetCommunity);
        const centralMember = community?.centralMembers[0];

        if (centralMember) {
          const match = await this.matchQualityAgent.calculateMatchQuality(
            userId,
            centralMember.userId
          );

          const rec = await this.matchToRecommendation(match, 'strategic');
          rec.title = `Join ${community.name}`;
          rec.description = action.reasoning;
          rec.actionSteps = action.actionableSteps.map((step, i) => ({
            step: i + 1,
            action: step,
            difficulty: 'medium' as const,
            estimatedTime: '1-2 weeks'
          }));
          recommendations.push(rec);
        }
      }
    }

    return recommendations;
  }

  /**
   * Helper: Convert match to recommendation
   */

  private async matchToRecommendation(
    match: MatchScore,
    type: Recommendation['type']
  ): Promise<Recommendation> {
    const targetProfile = await this.getUserProfile(match.targetId);

    const priority: 'high' | 'medium' | 'low' =
      match.overallScore >= 80 ? 'high' :
      match.overallScore >= 65 ? 'medium' : 'low';

    const actionSteps: Recommendation['actionSteps'] = [];

    if (match.features.commonConnections > 0) {
      actionSteps.push({
        step: 1,
        action: `Request introduction through mutual connection`,
        difficulty: 'easy',
        estimatedTime: '1-3 days'
      });
    } else if (match.features.networkDistance <= 3) {
      actionSteps.push({
        step: 1,
        action: `Find introduction path (${match.features.networkDistance} degrees)`,
        difficulty: 'medium',
        estimatedTime: '1-2 weeks'
      });
    } else {
      actionSteps.push({
        step: 1,
        action: 'Send direct connection request with personalized message',
        difficulty: 'medium',
        estimatedTime: '1 week'
      });
    }

    actionSteps.push({
      step: 2,
      action: 'Schedule introductory call',
      difficulty: 'easy',
      estimatedTime: '1 week'
    });

    actionSteps.push({
      step: 3,
      action: 'Explore collaboration opportunities',
      difficulty: 'medium',
      estimatedTime: '2-4 weeks'
    });

    return {
      id: `rec_${match.userId}_${match.targetId}_${Date.now()}`,
      type,
      priority,
      targetUserId: match.targetId,
      targetName: targetProfile.name || 'Unknown',
      score: match.overallScore,
      confidence: match.confidence,
      title: `Connect with ${targetProfile.name}`,
      description: `${targetProfile.industry || 'Professional'} with ${match.overallScore}% match`,
      reasoning: match.topReasons.map(r => r.explanation),
      actionSteps,
      expectedOutcomes: match.recommendations,
      potentialRisks: match.warnings,
      timeframe: priority === 'high' ? 'This week' : priority === 'medium' ? 'This month' : 'This quarter',
      expiresAt: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000) // 30 days
    };
  }

  /**
   * Database helpers
   */

  private async getUserProfile(userId: string): Promise<any> {
    const client = await this.pool.connect();
    try {
      const result = await client.query(`
        SELECT u.id, u.name, u.industry, up.expertise_areas, up.location
        FROM users u
        LEFT JOIN user_profiles up ON u.id = up.user_id
        WHERE u.id = $1
      `, [userId]);
      return result.rows[0] || {};
    } finally {
      client.release();
    }
  }

  private async getUserConnections(userId: string): Promise<string[]> {
    const client = await this.pool.connect();
    try {
      const result = await client.query(`
        SELECT u.id
        FROM connections c
        JOIN contacts ct ON c.contact_id = ct.id
        JOIN users u ON ct.email = u.email
        WHERE c.user_id = $1
      `, [userId]);
      return result.rows.map(row => row.id);
    } finally {
      client.release();
    }
  }

  private async getConnectionIndustries(userId: string): Promise<Set<string>> {
    const client = await this.pool.connect();
    try {
      const result = await client.query(`
        SELECT DISTINCT u.industry
        FROM connections c
        JOIN contacts ct ON c.contact_id = ct.id
        JOIN users u ON ct.email = u.email
        WHERE c.user_id = $1 AND u.industry IS NOT NULL
      `, [userId]);
      return new Set(result.rows.map(row => row.industry));
    } finally {
      client.release();
    }
  }

  private async getConnectionCountries(userId: string): Promise<Set<string>> {
    const client = await this.pool.connect();
    try {
      const result = await client.query(`
        SELECT DISTINCT (up.location->>'country') as country
        FROM connections c
        JOIN contacts ct ON c.contact_id = ct.id
        JOIN users u ON ct.email = u.email
        JOIN user_profiles up ON u.id = up.user_id
        WHERE c.user_id = $1 AND up.location IS NOT NULL
      `, [userId]);
      return new Set(result.rows.map(row => row.country).filter(Boolean));
    } finally {
      client.release();
    }
  }

  private async findExpertiseGaps(userId: string): Promise<string[]> {
    // Simplified: Find common expertise areas user doesn't have
    const client = await this.pool.connect();
    try {
      const result = await client.query(`
        SELECT DISTINCT unnest(expertise_areas) as expertise
        FROM user_profiles
        WHERE user_id != $1
        LIMIT 50
      `, [userId]);

      const userProfile = await this.getUserProfile(userId);
      const userExpertise = new Set(userProfile.expertise_areas || []);

      return result.rows
        .map(row => row.expertise)
        .filter(exp => !userExpertise.has(exp))
        .slice(0, 10);
    } finally {
      client.release();
    }
  }

  private async findIntroductionCandidates(userId: string): Promise<string[]> {
    // Users at 2-3 degrees
    const client = await this.pool.connect();
    try {
      const result = await client.query(`
        SELECT DISTINCT u2.id
        FROM connections c1
        JOIN contacts ct1 ON c1.contact_id = ct1.id
        JOIN users u1 ON ct1.email = u1.email
        JOIN connections c2 ON c2.user_id = u1.id
        JOIN contacts ct2 ON c2.contact_id = ct2.id
        JOIN users u2 ON ct2.email = u2.email
        WHERE c1.user_id = $1
        AND u2.id != $1
        AND u2.id NOT IN (
          SELECT u.id
          FROM connections c
          JOIN contacts ct ON c.contact_id = ct.id
          JOIN users u ON ct.email = u.email
          WHERE c.user_id = $1
        )
        LIMIT 50
      `, [userId]);
      return result.rows.map(row => row.id);
    } finally {
      client.release();
    }
  }

  private async findGapFillers(
    userId: string,
    gap: NetworkGapAnalysis['gaps'][0]
  ): Promise<string[]> {
    const client = await this.pool.connect();
    try {
      let query = '';
      let params: any[] = [userId];

      switch (gap.type) {
        case 'industry':
          // Find users in different industries
          const userProfile = await this.getUserProfile(userId);
          query = `
            SELECT id FROM users
            WHERE industry != $2 AND id != $1
            LIMIT 20
          `;
          params.push(userProfile.industry);
          break;

        case 'geography':
          query = `
            SELECT u.id
            FROM users u
            JOIN user_profiles up ON u.id = up.user_id
            WHERE u.id != $1
            AND (up.location->>'country') != (
              SELECT location->>'country'
              FROM user_profiles
              WHERE user_id = $1
            )
            LIMIT 20
          `;
          break;

        case 'expertise':
          query = `
            SELECT user_id as id
            FROM user_profiles
            WHERE user_id != $1
            LIMIT 20
          `;
          break;

        default:
          query = 'SELECT id FROM users WHERE id != $1 LIMIT 20';
      }

      const result = await client.query(query, params);
      return result.rows.map(row => row.id);
    } finally {
      client.release();
    }
  }

  private async findByIndustry(industry: string): Promise<string[]> {
    const client = await this.pool.connect();
    try {
      const result = await client.query(
        'SELECT id FROM users WHERE industry = $1 LIMIT 30',
        [industry]
      );
      return result.rows.map(row => row.id);
    } finally {
      client.release();
    }
  }

  private async findByExpertise(expertise: string): Promise<string[]> {
    const client = await this.pool.connect();
    try {
      const result = await client.query(`
        SELECT user_id as id
        FROM user_profiles
        WHERE $1 = ANY(expertise_areas)
        LIMIT 30
      `, [expertise]);
      return result.rows.map(row => row.id);
    } finally {
      client.release();
    }
  }

  private async getCommunity(communityId: string): Promise<any> {
    const structure = await this.communityAgent.detectCommunities();
    return structure.communities.find(c => c.communityId === communityId);
  }
}
