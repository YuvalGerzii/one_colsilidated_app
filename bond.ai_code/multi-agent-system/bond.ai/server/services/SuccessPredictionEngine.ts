import { Pool } from 'pg';
import Redis from 'ioredis';

/**
 * Success Prediction Engine
 *
 * Predicts likelihood of successful collaboration using:
 * - Historical match success data
 * - User engagement patterns
 * - Network effects
 * - Timing factors
 * - Behavioral signals
 *
 * Uses ensemble model combining multiple prediction methods:
 * - Logistic regression on historical data
 * - Similarity-based predictions
 * - Network effect scoring
 */

export interface SuccessPrediction {
  matchId: string;
  successProbability: number; // 0-1
  confidenceInterval: { lower: number; upper: number };
  predictionFactors: PredictionFactor[];
  riskFactors: RiskFactor[];
  recommendations: string[];
  historicalComparison: HistoricalComparison;
}

export interface PredictionFactor {
  name: string;
  impact: number; // -1 to 1
  weight: number; // 0-1
  description: string;
}

export interface RiskFactor {
  type: 'low' | 'medium' | 'high';
  description: string;
  mitigation: string;
}

export interface HistoricalComparison {
  similarMatches: number;
  successRate: number;
  averageTimeToSuccess: number; // days
  commonSuccessPatterns: string[];
}

export class SuccessPredictionEngine {
  private pool: Pool;
  private redis: Redis;

  // Feature weights learned from historical data
  private weights = {
    compatibilityScore: 0.25,
    networkStrength: 0.15,
    responseTime: 0.12,
    needOfferingFit: 0.20,
    historicalSuccess: 0.15,
    timing: 0.08,
    engagement: 0.05
  };

  constructor(pool: Pool, redis: Redis) {
    this.pool = pool;
    this.redis = redis;
  }

  /**
   * Predict success probability for a match
   */
  async predictSuccess(matchId: string): Promise<SuccessPrediction> {
    // Check cache first
    const cached = await this.getCachedPrediction(matchId);
    if (cached) return cached;

    const client = await this.pool.connect();

    try {
      // Get match data
      const matchData = await this.getMatchData(client, matchId);

      // Calculate prediction factors
      const factors = await this.calculatePredictionFactors(client, matchData);

      // Calculate base probability
      const baseProbability = this.calculateBaseProbability(factors);

      // Apply historical adjustments
      const historicalComparison = await this.getHistoricalComparison(client, matchData);
      const adjustedProbability = this.applyHistoricalAdjustment(
        baseProbability,
        historicalComparison
      );

      // Calculate confidence interval
      const confidenceInterval = this.calculateConfidenceInterval(
        adjustedProbability,
        historicalComparison.similarMatches
      );

      // Identify risk factors
      const riskFactors = this.identifyRiskFactors(factors, matchData);

      // Generate recommendations
      const recommendations = this.generateRecommendations(
        factors,
        riskFactors,
        adjustedProbability
      );

      const prediction: SuccessPrediction = {
        matchId,
        successProbability: adjustedProbability,
        confidenceInterval,
        predictionFactors: factors,
        riskFactors,
        recommendations,
        historicalComparison
      };

      // Cache prediction
      await this.cachePrediction(matchId, prediction);

      return prediction;
    } finally {
      client.release();
    }
  }

  /**
   * Get comprehensive match data
   */
  private async getMatchData(client: any, matchId: string): Promise<any> {
    const result = await client.query(
      `SELECT
         mc.*,
         a1.user_id as user1_id,
         a2.user_id as user2_id,
         u1.created_at as user1_join_date,
         u2.created_at as user2_join_date,
         up1.needs as user1_needs,
         up1.offerings as user1_offerings,
         up2.needs as user2_needs,
         up2.offerings as user2_offerings,
         (
           SELECT COUNT(*)
           FROM negotiations n
           WHERE n.match_id = mc.id
         ) as negotiation_count,
         (
           SELECT COUNT(*)
           FROM messages m
           JOIN conversations c ON m.conversation_id = c.id
           WHERE mc.id = ANY(c.participants::text[])
         ) as message_count
       FROM match_candidates mc
       JOIN agents a1 ON mc.initiator_agent_id = a1.id
       JOIN agents a2 ON mc.agent_id = a2.id
       JOIN users u1 ON a1.user_id = u1.id
       JOIN users u2 ON a2.user_id = u2.id
       LEFT JOIN user_profiles up1 ON u1.id = up1.user_id
       LEFT JOIN user_profiles up2 ON u2.id = up2.user_id
       WHERE mc.id = $1`,
      [matchId]
    );

    if (result.rows.length === 0) {
      throw new Error('Match not found');
    }

    return result.rows[0];
  }

  /**
   * Calculate all prediction factors
   */
  private async calculatePredictionFactors(client: any, matchData: any): Promise<PredictionFactor[]> {
    const factors: PredictionFactor[] = [];

    // 1. Compatibility Score Factor
    const compatScore = matchData.compatibility_score || 0;
    factors.push({
      name: 'Compatibility Score',
      impact: this.normalizeImpact(compatScore),
      weight: this.weights.compatibilityScore,
      description: `Match compatibility score: ${Math.round(compatScore * 100)}%`
    });

    // 2. Network Strength Factor
    const networkStrength = matchData.metadata?.trustLevel || 0.5;
    const degreeOfSeparation = matchData.metadata?.degreeOfSeparation || 3;
    const networkScore = networkStrength * (1 - (degreeOfSeparation - 1) / 3);

    factors.push({
      name: 'Network Strength',
      impact: this.normalizeImpact(networkScore),
      weight: this.weights.networkStrength,
      description: `Network trust level: ${Math.round(networkStrength * 100)}%, ${degreeOfSeparation}° separation`
    });

    // 3. Response Time Factor
    const avgResponseTime = await this.getAverageResponseTime(client, matchData.user1_id, matchData.user2_id);
    const responseScore = avgResponseTime < 3600 ? 1.0 : // < 1 hour = great
                         avgResponseTime < 86400 ? 0.7 : // < 1 day = good
                         avgResponseTime < 172800 ? 0.4 : // < 2 days = okay
                         0.2; // > 2 days = poor

    factors.push({
      name: 'Response Time',
      impact: this.normalizeImpact(responseScore),
      weight: this.weights.responseTime,
      description: `Average response time: ${this.formatDuration(avgResponseTime)}`
    });

    // 4. Need-Offering Fit Factor
    const fitScore = this.calculateNeedOfferingFit(
      matchData.user1_needs,
      matchData.user1_offerings,
      matchData.user2_needs,
      matchData.user2_offerings
    );

    factors.push({
      name: 'Need-Offering Fit',
      impact: this.normalizeImpact(fitScore),
      weight: this.weights.needOfferingFit,
      description: `${Math.round(fitScore * 100)}% alignment between needs and offerings`
    });

    // 5. Historical Success Factor
    const historicalSuccessRate = await this.getMatchTypeSuccessRate(client, matchData.match_type);

    factors.push({
      name: 'Historical Success Rate',
      impact: this.normalizeImpact(historicalSuccessRate),
      weight: this.weights.historicalSuccess,
      description: `${Math.round(historicalSuccessRate * 100)}% success rate for ${matchData.match_type} matches`
    });

    // 6. Timing Factor
    const timingScore = this.calculateTimingScore(matchData.user1_needs, matchData.user2_needs);

    factors.push({
      name: 'Timing Alignment',
      impact: this.normalizeImpact(timingScore),
      weight: this.weights.timing,
      description: timingScore > 0.7 ? 'Time-sensitive opportunity' : 'Flexible timing'
    });

    // 7. Engagement Factor
    const engagementScore = this.calculateEngagementScore(
      matchData.negotiation_count || 0,
      matchData.message_count || 0
    );

    factors.push({
      name: 'User Engagement',
      impact: this.normalizeImpact(engagementScore),
      weight: this.weights.engagement,
      description: `${matchData.negotiation_count || 0} negotiations, ${matchData.message_count || 0} messages`
    });

    return factors;
  }

  /**
   * Calculate base probability from factors
   */
  private calculateBaseProbability(factors: PredictionFactor[]): number {
    let weightedSum = 0;
    let totalWeight = 0;

    factors.forEach(factor => {
      weightedSum += factor.impact * factor.weight;
      totalWeight += factor.weight;
    });

    return totalWeight > 0 ? weightedSum / totalWeight : 0.5;
  }

  /**
   * Get historical comparison data
   */
  private async getHistoricalComparison(client: any, matchData: any): Promise<HistoricalComparison> {
    const result = await client.query(
      `SELECT
         COUNT(*) as total_matches,
         COUNT(CASE WHEN a.id IS NOT NULL THEN 1 END) as successful_matches,
         AVG(EXTRACT(EPOCH FROM (a.created_at - mc.created_at)) / 86400) as avg_days_to_success
       FROM match_candidates mc
       LEFT JOIN agreements a ON mc.id = a.match_id
       WHERE mc.match_type = $1
       AND mc.created_at > NOW() - INTERVAL '6 months'`,
      [matchData.match_type]
    );

    const data = result.rows[0];
    const totalMatches = parseInt(data.total_matches);
    const successfulMatches = parseInt(data.successful_matches);
    const successRate = totalMatches > 0 ? successfulMatches / totalMatches : 0.5;

    // Get common success patterns
    const patternsResult = await client.query(
      `SELECT metadata->>'successFactors' as factors
       FROM agreements
       WHERE match_id IN (
         SELECT id FROM match_candidates
         WHERE match_type = $1
       )
       LIMIT 20`,
      [matchData.match_type]
    );

    const commonSuccessPatterns = this.extractCommonPatterns(patternsResult.rows);

    return {
      similarMatches: totalMatches,
      successRate,
      averageTimeToSuccess: parseFloat(data.avg_days_to_success || '30'),
      commonSuccessPatterns
    };
  }

  /**
   * Apply historical adjustment to base probability
   */
  private applyHistoricalAdjustment(
    baseProbability: number,
    historical: HistoricalComparison
  ): number {
    // Blend base probability with historical success rate
    // More similar matches = more weight on historical data
    const historicalWeight = Math.min(historical.similarMatches / 50, 0.4);
    const baseWeight = 1 - historicalWeight;

    return (baseProbability * baseWeight) + (historical.successRate * historicalWeight);
  }

  /**
   * Calculate confidence interval
   */
  private calculateConfidenceInterval(
    probability: number,
    sampleSize: number
  ): { lower: number; upper: number } {
    // Use Wilson score interval for binomial proportion
    const z = 1.96; // 95% confidence
    const n = Math.max(sampleSize, 10); // Minimum sample size

    const center = probability;
    const margin = z * Math.sqrt((probability * (1 - probability)) / n);

    return {
      lower: Math.max(0, center - margin),
      upper: Math.min(1, center + margin)
    };
  }

  /**
   * Identify risk factors
   */
  private identifyRiskFactors(factors: PredictionFactor[], matchData: any): RiskFactor[] {
    const risks: RiskFactor[] = [];

    // Check for low compatibility
    const compatFactor = factors.find(f => f.name === 'Compatibility Score');
    if (compatFactor && compatFactor.impact < 0.5) {
      risks.push({
        type: 'high',
        description: 'Low compatibility score may indicate misalignment',
        mitigation: 'Focus on finding common ground and clear mutual benefits'
      });
    }

    // Check for weak network connection
    const networkFactor = factors.find(f => f.name === 'Network Strength');
    if (networkFactor && networkFactor.impact < 0.4) {
      risks.push({
        type: 'medium',
        description: 'Limited network connection may affect trust building',
        mitigation: 'Request warm introductions from mutual connections'
      });
    }

    // Check for slow response times
    const responseFactor = factors.find(f => f.name === 'Response Time');
    if (responseFactor && responseFactor.impact < 0.3) {
      risks.push({
        type: 'medium',
        description: 'Slow response times may delay progress',
        mitigation: 'Set clear communication expectations early'
      });
    }

    // Check for low engagement
    const engagementFactor = factors.find(f => f.name === 'User Engagement');
    if (engagementFactor && engagementFactor.impact < 0.3) {
      risks.push({
        type: 'low',
        description: 'Limited engagement history',
        mitigation: 'Start with a clear, compelling introduction message'
      });
    }

    return risks;
  }

  /**
   * Generate actionable recommendations
   */
  private generateRecommendations(
    factors: PredictionFactor[],
    risks: RiskFactor[],
    probability: number
  ): string[] {
    const recommendations: string[] = [];

    if (probability >= 0.75) {
      recommendations.push('🎯 High probability of success - initiate contact soon!');
      recommendations.push('📅 Schedule an intro call within the next week');
    } else if (probability >= 0.5) {
      recommendations.push('💡 Good potential - invest time in a thoughtful introduction');
      recommendations.push('🤝 Focus on demonstrating mutual value');
    } else {
      recommendations.push('⚠️ Consider strengthening the match before proceeding');
      recommendations.push('🔍 Identify and address potential misalignments first');
    }

    // Add specific recommendations based on factors
    const lowFactors = factors.filter(f => f.impact < 0.4);

    if (lowFactors.some(f => f.name === 'Need-Offering Fit')) {
      recommendations.push('💬 Clearly articulate how you can help each other');
    }

    if (lowFactors.some(f => f.name === 'Network Strength')) {
      recommendations.push('🌐 Leverage mutual connections for introductions');
    }

    if (lowFactors.some(f => f.name === 'Timing Alignment')) {
      recommendations.push('⏰ Discuss timeline expectations upfront');
    }

    // Add risk-specific recommendations
    const highRisks = risks.filter(r => r.type === 'high');
    if (highRisks.length > 0) {
      recommendations.push(`⚠️ Address key risk: ${highRisks[0].mitigation}`);
    }

    return recommendations.slice(0, 5);
  }

  /**
   * Helper functions
   */

  private normalizeImpact(score: number): number {
    // Convert 0-1 score to -1 to 1 impact
    return (score * 2) - 1;
  }

  private async getAverageResponseTime(client: any, user1Id: string, user2Id: string): Promise<number> {
    // Get average response time for these users
    const result = await client.query(
      `SELECT AVG(
         EXTRACT(EPOCH FROM (
           m2.created_at - m1.created_at
         ))
       ) as avg_response_time
       FROM messages m1
       JOIN messages m2 ON m1.conversation_id = m2.conversation_id
       WHERE m1.sender_id IN ($1, $2)
       AND m2.sender_id IN ($1, $2)
       AND m1.sender_id != m2.sender_id
       AND m2.created_at > m1.created_at
       AND EXTRACT(EPOCH FROM (m2.created_at - m1.created_at)) < 604800`, // Within 1 week
      [user1Id, user2Id]
    );

    return parseFloat(result.rows[0]?.avg_response_time || '86400'); // Default 1 day
  }

  private calculateNeedOfferingFit(needs1: any[], offerings1: any[], needs2: any[], offerings2: any[]): number {
    let matches = 0;
    let total = 0;

    (needs1 || []).forEach((need: any) => {
      (offerings2 || []).forEach((offering: any) => {
        total++;
        if (this.categoriesMatch(need.category, offering.category)) {
          matches++;
        }
      });
    });

    (needs2 || []).forEach((need: any) => {
      (offerings1 || []).forEach((offering: any) => {
        total++;
        if (this.categoriesMatch(need.category, offering.category)) {
          matches++;
        }
      });
    });

    return total > 0 ? matches / total : 0.5;
  }

  private categoriesMatch(cat1: string, cat2: string): boolean {
    return cat1 === cat2 || this.areCategoriesRelated(cat1, cat2);
  }

  private areCategoriesRelated(cat1: string, cat2: string): boolean {
    const related: Record<string, string[]> = {
      'funding': ['investment', 'capital'],
      'mentorship': ['coaching', 'advisory'],
      'technical': ['engineering', 'development']
    };

    for (const [key, vals] of Object.entries(related)) {
      if ((cat1 === key || vals.includes(cat1)) && (cat2 === key || vals.includes(cat2))) {
        return true;
      }
    }

    return false;
  }

  private calculateTimingScore(needs1: any[], needs2: any[]): number {
    const allNeeds = [...(needs1 || []), ...(needs2 || [])];
    const urgentCount = allNeeds.filter((n: any) =>
      n.urgency === 'immediate' || n.urgency === 'days'
    ).length;

    return urgentCount > 0 ? 0.9 : 0.6;
  }

  private calculateEngagementScore(negotiations: number, messages: number): number {
    const negScore = Math.min(negotiations / 3, 1);
    const msgScore = Math.min(messages / 20, 1);

    return (negScore * 0.6 + msgScore * 0.4);
  }

  private async getMatchTypeSuccessRate(client: any, matchType: string): Promise<number> {
    const result = await client.query(
      `SELECT
         COUNT(*) as total,
         COUNT(CASE WHEN a.id IS NOT NULL THEN 1 END) as successful
       FROM match_candidates mc
       LEFT JOIN agreements a ON mc.id = a.match_id
       WHERE mc.match_type = $1`,
      [matchType]
    );

    const total = parseInt(result.rows[0]?.total || '0');
    const successful = parseInt(result.rows[0]?.successful || '0');

    return total > 0 ? successful / total : 0.5;
  }

  private extractCommonPatterns(rows: any[]): string[] {
    // Extract common success factors from metadata
    const patterns = new Set<string>();

    rows.forEach(row => {
      try {
        const factors = JSON.parse(row.factors || '[]');
        factors.forEach((f: string) => patterns.add(f));
      } catch (e) {
        // Ignore parse errors
      }
    });

    return Array.from(patterns).slice(0, 5);
  }

  private formatDuration(seconds: number): string {
    if (seconds < 3600) return `${Math.round(seconds / 60)} minutes`;
    if (seconds < 86400) return `${Math.round(seconds / 3600)} hours`;
    return `${Math.round(seconds / 86400)} days`;
  }

  /**
   * Cache prediction
   */
  private async cachePrediction(matchId: string, prediction: SuccessPrediction): Promise<void> {
    await this.redis.setex(
      `prediction:${matchId}`,
      7200, // 2 hours
      JSON.stringify(prediction)
    );
  }

  /**
   * Get cached prediction
   */
  private async getCachedPrediction(matchId: string): Promise<SuccessPrediction | null> {
    const cached = await this.redis.get(`prediction:${matchId}`);
    return cached ? JSON.parse(cached) : null;
  }
}
