import { Pool } from 'pg';
import Redis from 'ioredis';
import { SixDegreesAgent } from './SixDegreesAgent';
import { TrustPropagationAgent } from './TrustPropagationAgent';
import { SerendipityAgent } from './SerendipityAgent';
import { CommunityDetectionAgent } from './CommunityDetectionAgent';
import { ConnectionStrengthAnalyzer } from './ConnectionStrengthAnalyzer';

/**
 * Match Quality Agent
 *
 * Comprehensive match scoring system that combines multiple signals:
 * - Network distance and reachability
 * - Trust propagation scores
 * - Serendipity potential
 * - Community alignment
 * - Connection strength
 * - Strategic value
 * - ML-ready feature vectors
 *
 * Produces actionable match recommendations with confidence scores
 * and explanations for each recommendation.
 */

export interface MatchFeatures {
  // Network topology features
  networkDistance: number; // 0-6 (degrees of separation)
  hasDirectConnection: boolean;
  commonConnections: number;

  // Trust features
  directTrust: number | null; // 0-1 or null
  indirectTrust: number; // 0-1
  trustConfidence: number; // 0-1

  // Serendipity features
  serendipityScore: number; // 0-1
  unexpectedness: number; // 0-1
  novelty: number; // 0-1

  // Community features
  sameCommunity: boolean;
  communityOverlap: number; // 0-1
  bridgePotential: number; // 0-1

  // Profile alignment features
  industryMatch: number; // 0-1
  expertiseOverlap: number; // 0-1
  needsOffersAlignment: number; // 0-1
  geographicDistance: number; // 0-1 (normalized)

  // Strategic features
  centralityDifference: number; // -1 to 1
  mutualBenefit: number; // 0-1
  networkEfficiency: number; // 0-1

  // Meta features
  dataCompleteness: number; // 0-1
  calculationConfidence: number; // 0-1
}

export interface MatchScore {
  userId: string;
  targetId: string;
  overallScore: number; // 0-100
  confidence: number; // 0-1
  category: 'excellent' | 'good' | 'moderate' | 'weak' | 'poor';
  features: MatchFeatures;

  // Explanation
  topReasons: Array<{
    factor: string;
    contribution: number;
    explanation: string;
  }>;

  warnings: string[];
  recommendations: string[];

  // ML-ready
  featureVector: number[];
  featureNames: string[];
}

export interface MatchComparison {
  user1: string;
  user2: string;
  score1to2: MatchScore;
  score2to1: MatchScore;
  mutuality: number; // How symmetric the match is
  recommendation: 'highly_mutual' | 'asymmetric' | 'one_sided' | 'weak_both';
}

export class MatchQualityAgent {
  // Feature weights (can be tuned via ML)
  private readonly WEIGHTS = {
    networkDistance: 0.10,
    trust: 0.20,
    serendipity: 0.15,
    community: 0.10,
    profileAlignment: 0.25,
    strategic: 0.15,
    meta: 0.05
  };

  // Sub-weights for profile alignment
  private readonly PROFILE_WEIGHTS = {
    industry: 0.2,
    expertise: 0.3,
    needsOffers: 0.4,
    geography: 0.1
  };

  constructor(
    private pool: Pool,
    private redis: Redis,
    private sixDegreesAgent: SixDegreesAgent,
    private trustAgent: TrustPropagationAgent,
    private serendipityAgent: SerendipityAgent,
    private communityAgent: CommunityDetectionAgent,
    private strengthAnalyzer: ConnectionStrengthAnalyzer
  ) {}

  /**
   * Calculate comprehensive match quality score
   */
  async calculateMatchQuality(
    userId: string,
    targetId: string,
    options: {
      useCache?: boolean;
      includeExplanation?: boolean;
    } = {}
  ): Promise<MatchScore> {
    const { useCache = true, includeExplanation = true } = options;

    // Check cache
    if (useCache) {
      const cacheKey = `match_quality:${userId}:${targetId}`;
      const cached = await this.redis.get(cacheKey);
      if (cached) return JSON.parse(cached);
    }

    // Gather features from all agents in parallel
    const [
      networkData,
      trustData,
      serendipityData,
      communityData,
      profileData,
      centralityData
    ] = await Promise.all([
      this.gatherNetworkFeatures(userId, targetId),
      this.gatherTrustFeatures(userId, targetId),
      this.gatherSerendipityFeatures(userId, targetId),
      this.gatherCommunityFeatures(userId, targetId),
      this.gatherProfileFeatures(userId, targetId),
      this.gatherStrategicFeatures(userId, targetId)
    ]);

    // Combine into feature object
    const features: MatchFeatures = {
      ...networkData,
      ...trustData,
      ...serendipityData,
      ...communityData,
      ...profileData,
      ...centralityData,
      dataCompleteness: this.calculateDataCompleteness({
        ...networkData,
        ...trustData,
        ...serendipityData,
        ...communityData,
        ...profileData,
        ...centralityData
      }),
      calculationConfidence: 0.85 // Will be refined
    };

    // Calculate weighted score
    const { score, confidence, contributions } = this.calculateWeightedScore(features);

    // Categorize
    const category = this.categorizeScore(score);

    // Generate explanation
    const topReasons = includeExplanation
      ? this.generateTopReasons(contributions, features)
      : [];

    const warnings = this.generateWarnings(features);
    const recommendations = this.generateRecommendations(features);

    // Create ML-ready feature vector
    const { featureVector, featureNames } = this.createFeatureVector(features);

    const matchScore: MatchScore = {
      userId,
      targetId,
      overallScore: Math.round(score * 100),
      confidence,
      category,
      features,
      topReasons,
      warnings,
      recommendations,
      featureVector,
      featureNames
    };

    // Cache for 15 minutes
    const cacheKey = `match_quality:${userId}:${targetId}`;
    await this.redis.set(cacheKey, JSON.stringify(matchScore), 'EX', 900);

    return matchScore;
  }

  /**
   * Compare match quality in both directions
   */
  async compareMatchMutuality(
    user1: string,
    user2: string
  ): Promise<MatchComparison> {
    const [score1to2, score2to1] = await Promise.all([
      this.calculateMatchQuality(user1, user2),
      this.calculateMatchQuality(user2, user1)
    ]);

    // Calculate mutuality
    const scoreDiff = Math.abs(score1to2.overallScore - score2to1.overallScore);
    const avgScore = (score1to2.overallScore + score2to1.overallScore) / 2;

    const mutuality = 1 - (scoreDiff / 100);

    // Determine recommendation
    let recommendation: 'highly_mutual' | 'asymmetric' | 'one_sided' | 'weak_both';

    if (avgScore >= 70 && mutuality >= 0.8) {
      recommendation = 'highly_mutual';
    } else if (avgScore >= 50 && mutuality < 0.6) {
      recommendation = 'asymmetric';
    } else if (Math.max(score1to2.overallScore, score2to1.overallScore) >= 60 &&
               Math.min(score1to2.overallScore, score2to1.overallScore) <= 40) {
      recommendation = 'one_sided';
    } else {
      recommendation = 'weak_both';
    }

    return {
      user1,
      user2,
      score1to2,
      score2to1,
      mutuality,
      recommendation
    };
  }

  /**
   * Find best matches for a user across the network
   */
  async findBestMatches(
    userId: string,
    options: {
      limit?: number;
      minScore?: number;
      excludeExisting?: boolean;
      diversityWeight?: number;
    } = {}
  ): Promise<MatchScore[]> {
    const {
      limit = 20,
      minScore = 50,
      excludeExisting = true,
      diversityWeight = 0.3
    } = options;

    // Get candidate users
    const candidates = await this.getCandidateUsers(userId, excludeExisting);

    // Score all candidates in batches
    const batchSize = 10;
    const scores: MatchScore[] = [];

    for (let i = 0; i < candidates.length; i += batchSize) {
      const batch = candidates.slice(i, i + batchSize);
      const batchScores = await Promise.all(
        batch.map(targetId => this.calculateMatchQuality(userId, targetId))
      );
      scores.push(...batchScores);
    }

    // Filter by minimum score
    let filteredScores = scores.filter(s => s.overallScore >= minScore);

    // Apply diversity boosting if requested
    if (diversityWeight > 0) {
      filteredScores = this.applyDiversityBoost(filteredScores, diversityWeight);
    }

    // Sort and limit
    return filteredScores
      .sort((a, b) => b.overallScore - a.overallScore)
      .slice(0, limit);
  }

  /**
   * Batch scoring for recommendations
   */
  async batchCalculateScores(
    userId: string,
    targetIds: string[]
  ): Promise<Map<string, MatchScore>> {
    const scores = await Promise.all(
      targetIds.map(targetId => this.calculateMatchQuality(userId, targetId))
    );

    const scoreMap = new Map<string, MatchScore>();
    scores.forEach(score => scoreMap.set(score.targetId, score));

    return scoreMap;
  }

  /**
   * Feature gathering methods
   */

  private async gatherNetworkFeatures(
    userId: string,
    targetId: string
  ): Promise<Partial<MatchFeatures>> {
    try {
      const sixDegreesResult = await this.sixDegreesAgent.verifySixDegrees(userId, targetId);
      const commonConnections = await this.getCommonConnections(userId, targetId);

      return {
        networkDistance: sixDegreesResult.degrees,
        hasDirectConnection: sixDegreesResult.degrees === 1,
        commonConnections: commonConnections.length
      };
    } catch (error) {
      return {
        networkDistance: 6,
        hasDirectConnection: false,
        commonConnections: 0
      };
    }
  }

  private async gatherTrustFeatures(
    userId: string,
    targetId: string
  ): Promise<Partial<MatchFeatures>> {
    try {
      const trustResult = await this.trustAgent.calculateTransitiveTrust(userId, targetId);

      return {
        directTrust: trustResult.directTrust,
        indirectTrust: trustResult.indirectTrust,
        trustConfidence: trustResult.confidenceLevel
      };
    } catch (error) {
      return {
        directTrust: null,
        indirectTrust: 0,
        trustConfidence: 0
      };
    }
  }

  private async gatherSerendipityFeatures(
    userId: string,
    targetId: string
  ): Promise<Partial<MatchFeatures>> {
    try {
      const serendipityMatches = await this.serendipityAgent.findSerendipitousMatches(userId, 50);
      const targetMatch = serendipityMatches.find(m => m.targetId === targetId);

      if (targetMatch) {
        return {
          serendipityScore: targetMatch.serendipityScore,
          unexpectedness: targetMatch.unexpectednessScore,
          novelty: targetMatch.bridgeValue
        };
      }

      return {
        serendipityScore: 0,
        unexpectedness: 0,
        novelty: 0
      };
    } catch (error) {
      return {
        serendipityScore: 0,
        unexpectedness: 0,
        novelty: 0
      };
    }
  }

  private async gatherCommunityFeatures(
    userId: string,
    targetId: string
  ): Promise<Partial<MatchFeatures>> {
    try {
      const structure = await this.communityAgent.detectCommunities();

      const userCommunity = structure.communities.find(c => c.members.includes(userId));
      const targetCommunity = structure.communities.find(c => c.members.includes(targetId));

      const sameCommunity = userCommunity?.communityId === targetCommunity?.communityId;

      // Check if either is a bridge
      const userBridge = structure.intercommunityBridges.find(b => b.userId === userId);
      const targetBridge = structure.intercommunityBridges.find(b => b.userId === targetId);

      const bridgePotential = (userBridge || targetBridge) ? 0.8 : 0.2;

      const communityOverlap = sameCommunity ? 1.0 :
        (userBridge && targetBridge) ? 0.5 : 0.0;

      return {
        sameCommunity,
        communityOverlap,
        bridgePotential
      };
    } catch (error) {
      return {
        sameCommunity: false,
        communityOverlap: 0,
        bridgePotential: 0
      };
    }
  }

  private async gatherProfileFeatures(
    userId: string,
    targetId: string
  ): Promise<Partial<MatchFeatures>> {
    const [userProfile, targetProfile] = await Promise.all([
      this.getUserProfile(userId),
      this.getUserProfile(targetId)
    ]);

    // Industry match
    const industryMatch = userProfile.industry === targetProfile.industry ? 1.0 : 0.0;

    // Expertise overlap
    const userExpertise = new Set(userProfile.expertiseAreas || []);
    const targetExpertise = new Set(targetProfile.expertiseAreas || []);
    const expertiseIntersection = new Set(
      [...userExpertise].filter(x => targetExpertise.has(x))
    );
    const expertiseOverlap = userExpertise.size > 0
      ? expertiseIntersection.size / userExpertise.size
      : 0;

    // Needs/offers alignment
    const userNeeds = new Set(userProfile.needs || []);
    const targetOffers = new Set(targetProfile.offers || []);
    const needsOffersMatch = new Set(
      [...userNeeds].filter(x => targetOffers.has(x))
    );
    const needsOffersAlignment = userNeeds.size > 0
      ? needsOffersMatch.size / userNeeds.size
      : 0;

    // Geographic distance (simplified)
    const geographicDistance = userProfile.location?.country === targetProfile.location?.country
      ? 0.0 : 0.5;

    return {
      industryMatch,
      expertiseOverlap,
      needsOffersAlignment,
      geographicDistance
    };
  }

  private async gatherStrategicFeatures(
    userId: string,
    targetId: string
  ): Promise<Partial<MatchFeatures>> {
    try {
      const [userCentrality, targetCentrality] = await Promise.all([
        this.strengthAnalyzer.calculateCentrality(userId),
        this.strengthAnalyzer.calculateCentrality(targetId)
      ]);

      const centralityDifference = (
        (userCentrality.pageRank - targetCentrality.pageRank) /
        Math.max(userCentrality.pageRank, targetCentrality.pageRank)
      );

      // Network efficiency: connecting different network positions is valuable
      const networkEfficiency = Math.abs(centralityDifference) > 0.3 ? 0.8 : 0.5;

      // Mutual benefit (simplified heuristic)
      const mutualBenefit = 0.7;

      return {
        centralityDifference,
        mutualBenefit,
        networkEfficiency
      };
    } catch (error) {
      return {
        centralityDifference: 0,
        mutualBenefit: 0.5,
        networkEfficiency: 0.5
      };
    }
  }

  /**
   * Scoring calculation
   */

  private calculateWeightedScore(features: MatchFeatures): {
    score: number;
    confidence: number;
    contributions: Map<string, number>;
  } {
    const contributions = new Map<string, number>();

    // Network distance (inverse - closer is better)
    const networkScore = features.hasDirectConnection ? 1.0 :
      Math.max(0, 1 - (features.networkDistance / 6));
    contributions.set('network', networkScore * this.WEIGHTS.networkDistance);

    // Trust
    const trustScore = features.directTrust !== null
      ? features.directTrust * 0.7 + features.indirectTrust * 0.3
      : features.indirectTrust;
    contributions.set('trust', trustScore * this.WEIGHTS.trust);

    // Serendipity
    const serendipityScore = features.serendipityScore;
    contributions.set('serendipity', serendipityScore * this.WEIGHTS.serendipity);

    // Community
    const communityScore = (
      (features.sameCommunity ? 0.5 : 0) +
      features.communityOverlap * 0.3 +
      features.bridgePotential * 0.2
    );
    contributions.set('community', communityScore * this.WEIGHTS.community);

    // Profile alignment (weighted sub-components)
    const profileScore = (
      features.industryMatch * this.PROFILE_WEIGHTS.industry +
      features.expertiseOverlap * this.PROFILE_WEIGHTS.expertise +
      features.needsOffersAlignment * this.PROFILE_WEIGHTS.needsOffers +
      (1 - features.geographicDistance) * this.PROFILE_WEIGHTS.geography
    );
    contributions.set('profile', profileScore * this.WEIGHTS.profileAlignment);

    // Strategic
    const strategicScore = (
      features.mutualBenefit * 0.5 +
      features.networkEfficiency * 0.5
    );
    contributions.set('strategic', strategicScore * this.WEIGHTS.strategic);

    // Meta
    const metaScore = features.dataCompleteness;
    contributions.set('meta', metaScore * this.WEIGHTS.meta);

    // Total score
    const totalScore = Array.from(contributions.values()).reduce((sum, val) => sum + val, 0);

    // Confidence based on data completeness and trust confidence
    const confidence = (
      features.dataCompleteness * 0.7 +
      features.trustConfidence * 0.3
    );

    return { score: totalScore, confidence, contributions };
  }

  private calculateDataCompleteness(features: Partial<MatchFeatures>): number {
    const fields = [
      'networkDistance',
      'directTrust',
      'indirectTrust',
      'serendipityScore',
      'sameCommunity',
      'industryMatch',
      'expertiseOverlap',
      'needsOffersAlignment',
      'centralityDifference'
    ];

    let completedFields = 0;
    for (const field of fields) {
      if (features[field as keyof typeof features] !== undefined &&
          features[field as keyof typeof features] !== null) {
        completedFields++;
      }
    }

    return completedFields / fields.length;
  }

  private categorizeScore(score: number): 'excellent' | 'good' | 'moderate' | 'weak' | 'poor' {
    if (score >= 0.8) return 'excellent';
    if (score >= 0.65) return 'good';
    if (score >= 0.5) return 'moderate';
    if (score >= 0.3) return 'weak';
    return 'poor';
  }

  /**
   * Explanation generation
   */

  private generateTopReasons(
    contributions: Map<string, number>,
    features: MatchFeatures
  ): Array<{ factor: string; contribution: number; explanation: string }> {
    const reasons: Array<{ factor: string; contribution: number; explanation: string }> = [];

    // Network
    if (contributions.get('network')! > 0.05) {
      reasons.push({
        factor: 'Network Distance',
        contribution: contributions.get('network')!,
        explanation: features.hasDirectConnection
          ? 'Direct connection exists'
          : `Connected within ${features.networkDistance} degrees`
      });
    }

    // Trust
    if (contributions.get('trust')! > 0.05) {
      reasons.push({
        factor: 'Trust',
        contribution: contributions.get('trust')!,
        explanation: features.directTrust !== null
          ? `Direct trust: ${(features.directTrust * 100).toFixed(0)}%`
          : `Indirect trust via ${features.trustConfidence > 0.7 ? 'reliable' : 'uncertain'} paths`
      });
    }

    // Profile alignment
    if (contributions.get('profile')! > 0.05) {
      const reasons_parts = [];
      if (features.industryMatch > 0) reasons_parts.push('same industry');
      if (features.expertiseOverlap > 0.3) reasons_parts.push('overlapping expertise');
      if (features.needsOffersAlignment > 0.3) reasons_parts.push('complementary needs/offers');

      reasons.push({
        factor: 'Profile Alignment',
        contribution: contributions.get('profile')!,
        explanation: reasons_parts.join(', ') || 'Some profile overlap'
      });
    }

    // Serendipity
    if (contributions.get('serendipity')! > 0.05) {
      reasons.push({
        factor: 'Serendipity',
        contribution: contributions.get('serendipity')!,
        explanation: 'Unexpected but valuable connection opportunity'
      });
    }

    return reasons.sort((a, b) => b.contribution - a.contribution).slice(0, 5);
  }

  private generateWarnings(features: MatchFeatures): string[] {
    const warnings: string[] = [];

    if (features.networkDistance >= 5) {
      warnings.push('Very distant in network - may be hard to reach');
    }

    if (features.trustConfidence < 0.4) {
      warnings.push('Low trust confidence - limited trust data available');
    }

    if (features.dataCompleteness < 0.6) {
      warnings.push('Incomplete profile data - score may be inaccurate');
    }

    if (features.geographicDistance > 0.7) {
      warnings.push('Significant geographic distance');
    }

    return warnings;
  }

  private generateRecommendations(features: MatchFeatures): string[] {
    const recommendations: string[] = [];

    if (features.commonConnections > 0) {
      recommendations.push(`Request introduction through ${features.commonConnections} mutual connection(s)`);
    }

    if (features.serendipityScore > 0.6) {
      recommendations.push('High serendipity potential - explore unexpected synergies');
    }

    if (features.bridgePotential > 0.6) {
      recommendations.push('Bridge to new network clusters - strategic connection');
    }

    if (features.needsOffersAlignment > 0.5) {
      recommendations.push('Strong needs/offers match - immediate collaboration potential');
    }

    return recommendations;
  }

  /**
   * ML feature vector creation
   */

  private createFeatureVector(features: MatchFeatures): {
    featureVector: number[];
    featureNames: string[];
  } {
    const featureNames = [
      'networkDistance',
      'hasDirectConnection',
      'commonConnections',
      'directTrust',
      'indirectTrust',
      'trustConfidence',
      'serendipityScore',
      'unexpectedness',
      'novelty',
      'sameCommunity',
      'communityOverlap',
      'bridgePotential',
      'industryMatch',
      'expertiseOverlap',
      'needsOffersAlignment',
      'geographicDistance',
      'centralityDifference',
      'mutualBenefit',
      'networkEfficiency',
      'dataCompleteness'
    ];

    const featureVector = featureNames.map(name => {
      const value = features[name as keyof MatchFeatures];

      if (typeof value === 'boolean') return value ? 1 : 0;
      if (typeof value === 'number') return value;
      if (value === null) return 0;
      return 0;
    });

    return { featureVector, featureNames };
  }

  /**
   * Helper methods
   */

  private applyDiversityBoost(
    scores: MatchScore[],
    diversityWeight: number
  ): MatchScore[] {
    // Boost scores for diverse matches (different industries, communities, etc.)
    return scores.map(score => {
      let diversityBonus = 0;

      if (!score.features.sameCommunity) diversityBonus += 0.1;
      if (score.features.industryMatch < 0.5) diversityBonus += 0.1;
      if (score.features.serendipityScore > 0.5) diversityBonus += 0.15;

      const boostedScore = score.overallScore + (diversityBonus * 100 * diversityWeight);

      return {
        ...score,
        overallScore: Math.min(100, Math.round(boostedScore))
      };
    });
  }

  private async getCandidateUsers(
    userId: string,
    excludeExisting: boolean
  ): Promise<string[]> {
    const client = await this.pool.connect();

    try {
      let query = 'SELECT id FROM users WHERE id != $1';
      const params: any[] = [userId];

      if (excludeExisting) {
        query += ` AND id NOT IN (
          SELECT u.id
          FROM connections c
          JOIN contacts ct ON c.contact_id = ct.id
          JOIN users u ON ct.email = u.email
          WHERE c.user_id = $2
        )`;
        params.push(userId);
      }

      query += ' LIMIT 100';

      const result = await client.query(query, params);
      return result.rows.map(row => row.id);

    } finally {
      client.release();
    }
  }

  private async getCommonConnections(
    userId1: string,
    userId2: string
  ): Promise<string[]> {
    const client = await this.pool.connect();

    try {
      const result = await client.query(`
        SELECT DISTINCT u.id
        FROM connections c1
        JOIN contacts ct1 ON c1.contact_id = ct1.id
        JOIN users u ON ct1.email = u.email
        WHERE c1.user_id = $1
        AND u.id IN (
          SELECT u2.id
          FROM connections c2
          JOIN contacts ct2 ON c2.contact_id = ct2.id
          JOIN users u2 ON ct2.email = u2.email
          WHERE c2.user_id = $2
        )
      `, [userId1, userId2]);

      return result.rows.map(row => row.id);

    } finally {
      client.release();
    }
  }

  private async getUserProfile(userId: string): Promise<any> {
    const client = await this.pool.connect();

    try {
      const result = await client.query(`
        SELECT
          u.id,
          u.name,
          u.industry,
          up.expertise_areas,
          up.location,
          up.needs,
          up.offers
        FROM users u
        LEFT JOIN user_profiles up ON u.id = up.user_id
        WHERE u.id = $1
      `, [userId]);

      return result.rows[0] || {};

    } finally {
      client.release();
    }
  }
}
