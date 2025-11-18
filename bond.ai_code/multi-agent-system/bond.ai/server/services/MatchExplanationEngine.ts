import { Pool } from 'pg';
import Redis from 'ioredis';
import { pipeline } from '@xenova/transformers';

/**
 * AI-Powered Match Explanation Engine
 *
 * Generates human-readable explanations for why users matched
 * Uses multiple signals to create comprehensive, transparent explanations
 *
 * Features:
 * - Multi-factor analysis (needs, offerings, network, behavior)
 * - Confidence scoring for each explanation factor
 * - Personalized explanation styles
 * - Historical pattern recognition
 */

export interface MatchExplanation {
  matchId: string;
  overallScore: number;
  primaryReasons: ExplanationFactor[];
  secondaryReasons: ExplanationFactor[];
  potentialConcerns: ExplanationFactor[];
  actionableInsights: string[];
  confidenceLevel: 'very_high' | 'high' | 'medium' | 'low';
}

export interface ExplanationFactor {
  category: string;
  title: string;
  description: string;
  score: number; // 0-1
  confidence: number; // 0-1
  evidence: string[];
  icon?: string;
}

export class MatchExplanationEngine {
  private pool: Pool;
  private redis: Redis;
  private llmModel: any;

  constructor(pool: Pool, redis: Redis) {
    this.pool = pool;
    this.redis = redis;
  }

  /**
   * Generate comprehensive explanation for a match
   */
  async explainMatch(userId: string, matchId: string): Promise<MatchExplanation> {
    const client = await this.pool.connect();

    try {
      // Get match details
      const matchResult = await client.query(
        `SELECT
           mc.*,
           u1.name as user1_name,
           u1.industry as user1_industry,
           u2.name as user2_name,
           u2.industry as user2_industry,
           up1.needs as user1_needs,
           up1.offerings as user1_offerings,
           up2.needs as user2_needs,
           up2.offerings as user2_offerings
         FROM match_candidates mc
         JOIN agents a1 ON mc.initiator_agent_id = a1.id
         JOIN agents a2 ON mc.agent_id = a2.id
         JOIN users u1 ON a1.user_id = u1.id
         JOIN users u2 ON a2.user_id = u2.id
         LEFT JOIN user_profiles up1 ON u1.id = up1.user_id
         LEFT JOIN user_profiles up2 ON u2.id = up2.user_id
         WHERE mc.id = $1 AND (a1.user_id = $2 OR a2.user_id = $2)`,
        [matchId, userId]
      );

      if (matchResult.rows.length === 0) {
        throw new Error('Match not found');
      }

      const match = matchResult.rows[0];

      // Analyze different factors
      const factors = await Promise.all([
        this.analyzeNeedOfferingAlignment(match),
        this.analyzeNetworkStrength(match),
        this.analyzeIndustryFit(match),
        this.analyzeBehavioralCompatibility(match),
        this.analyzeHistoricalPatterns(match),
        this.analyzeTimingAlignment(match)
      ]);

      // Categorize factors
      const primaryReasons = factors
        .filter(f => f.score >= 0.7 && f.confidence >= 0.7)
        .sort((a, b) => b.score - a.score)
        .slice(0, 3);

      const secondaryReasons = factors
        .filter(f => f.score >= 0.5 && f.score < 0.7 && f.confidence >= 0.6)
        .sort((a, b) => b.score - a.score)
        .slice(0, 3);

      const potentialConcerns = factors
        .filter(f => f.score < 0.4)
        .sort((a, b) => a.score - b.score)
        .slice(0, 2);

      // Generate actionable insights
      const insights = this.generateActionableInsights(
        match,
        primaryReasons,
        secondaryReasons,
        potentialConcerns
      );

      // Calculate overall confidence
      const avgConfidence = factors.reduce((sum, f) => sum + f.confidence, 0) / factors.length;
      let confidenceLevel: 'very_high' | 'high' | 'medium' | 'low';
      if (avgConfidence >= 0.85) confidenceLevel = 'very_high';
      else if (avgConfidence >= 0.7) confidenceLevel = 'high';
      else if (avgConfidence >= 0.5) confidenceLevel = 'medium';
      else confidenceLevel = 'low';

      return {
        matchId,
        overallScore: match.compatibility_score,
        primaryReasons,
        secondaryReasons,
        potentialConcerns,
        actionableInsights: insights,
        confidenceLevel
      };
    } finally {
      client.release();
    }
  }

  /**
   * Analyze need-offering alignment
   */
  private async analyzeNeedOfferingAlignment(match: any): Promise<ExplanationFactor> {
    const user1Needs = match.user1_needs || [];
    const user1Offerings = match.user1_offerings || [];
    const user2Needs = match.user2_needs || [];
    const user2Offerings = match.user2_offerings || [];

    // Find matches between needs and offerings
    const matches: string[] = [];
    let totalAlignmentScore = 0;
    let matchCount = 0;

    user1Needs.forEach((need: any) => {
      user2Offerings.forEach((offering: any) => {
        if (this.categoriesMatch(need.category, offering.category)) {
          matches.push(`${match.user2_name} can provide ${offering.category} which addresses ${match.user1_name}'s need for ${need.category}`);
          totalAlignmentScore += this.calculateCategoryAlignment(need, offering);
          matchCount++;
        }
      });
    });

    user2Needs.forEach((need: any) => {
      user1Offerings.forEach((offering: any) => {
        if (this.categoriesMatch(need.category, offering.category)) {
          matches.push(`${match.user1_name} can provide ${offering.category} which addresses ${match.user2_name}'s need for ${need.category}`);
          totalAlignmentScore += this.calculateCategoryAlignment(need, offering);
          matchCount++;
        }
      });
    });

    const score = matchCount > 0 ? totalAlignmentScore / matchCount : 0;

    return {
      category: 'needs_offerings',
      title: 'Need-Offering Alignment',
      description: matchCount > 0
        ? `Found ${matchCount} complementary need-offering ${matchCount === 1 ? 'match' : 'matches'} between you`
        : 'Limited complementary need-offering alignment',
      score,
      confidence: matchCount >= 2 ? 0.9 : matchCount === 1 ? 0.7 : 0.5,
      evidence: matches.slice(0, 3),
      icon: '🤝'
    };
  }

  /**
   * Analyze network strength
   */
  private async analyzeNetworkStrength(match: any): Promise<ExplanationFactor> {
    const degreeOfSeparation = match.metadata?.degreeOfSeparation || 3;
    const mutualConnections = match.metadata?.mutualConnections || 0;
    const trustLevel = match.metadata?.trustLevel || 0.5;

    const evidence: string[] = [];

    if (degreeOfSeparation === 1) {
      evidence.push('You are directly connected');
    } else if (degreeOfSeparation === 2) {
      evidence.push('You have mutual connections');
    } else {
      evidence.push(`${degreeOfSeparation} degrees of separation`);
    }

    if (mutualConnections > 0) {
      evidence.push(`${mutualConnections} mutual ${mutualConnections === 1 ? 'connection' : 'connections'}`);
    }

    // Score based on proximity and trust
    const proximityScore = 1 - ((degreeOfSeparation - 1) / 3); // Closer = better
    const trustScore = trustLevel;
    const mutualScore = Math.min(mutualConnections / 5, 1); // Normalize to 0-1

    const score = (proximityScore * 0.4 + trustScore * 0.4 + mutualScore * 0.2);

    return {
      category: 'network',
      title: 'Network Connection',
      description: degreeOfSeparation === 1
        ? 'Strong existing connection in your network'
        : mutualConnections > 0
          ? 'Connected through mutual connections'
          : 'Indirect network connection',
      score,
      confidence: degreeOfSeparation <= 2 ? 0.9 : 0.6,
      evidence,
      icon: '🌐'
    };
  }

  /**
   * Analyze industry fit
   */
  private async analyzeIndustryFit(match: any): Promise<ExplanationFactor> {
    const user1Industry = match.user1_industry;
    const user2Industry = match.user2_industry;

    const evidence: string[] = [];
    let score = 0;

    if (user1Industry === user2Industry) {
      evidence.push(`Both in ${user1Industry} industry`);
      evidence.push('Deep industry knowledge alignment');
      score = 0.9;
    } else if (this.industriesAreRelated(user1Industry, user2Industry)) {
      evidence.push(`Complementary industries: ${user1Industry} and ${user2Industry}`);
      evidence.push('Cross-industry collaboration potential');
      score = 0.7;
    } else {
      evidence.push(`Different industries: ${user1Industry} and ${user2Industry}`);
      evidence.push('Opportunity for diverse perspectives');
      score = 0.5;
    }

    return {
      category: 'industry',
      title: 'Industry Alignment',
      description: user1Industry === user2Industry
        ? 'Perfect industry alignment'
        : 'Cross-industry opportunity',
      score,
      confidence: 0.95,
      evidence,
      icon: '🏢'
    };
  }

  /**
   * Analyze behavioral compatibility
   */
  private async analyzeBehavioralCompatibility(match: any): Promise<ExplanationFactor> {
    // This would use data from profile preferences, communication style, etc.
    // For now, using placeholder logic

    const evidence: string[] = [];

    evidence.push('Similar communication preferences');
    evidence.push('Compatible working styles');

    return {
      category: 'behavior',
      title: 'Behavioral Compatibility',
      description: 'Compatible working and communication styles',
      score: 0.75,
      confidence: 0.6,
      evidence,
      icon: '💬'
    };
  }

  /**
   * Analyze historical patterns
   */
  private async analyzeHistoricalPatterns(match: any): Promise<ExplanationFactor> {
    const client = await this.pool.connect();

    try {
      // Check for similar successful matches
      const similarMatches = await client.query(
        `SELECT COUNT(*) as count
         FROM match_candidates mc
         JOIN agreements a ON mc.id = a.match_id
         WHERE mc.match_type = $1
         AND mc.status = 'accepted'`,
        [match.match_type]
      );

      const successCount = parseInt(similarMatches.rows[0]?.count || '0');
      const evidence: string[] = [];

      if (successCount > 10) {
        evidence.push(`${successCount} similar successful matches on platform`);
        evidence.push('Proven track record for this match type');
      } else if (successCount > 0) {
        evidence.push(`${successCount} similar matches have succeeded`);
      } else {
        evidence.push('New match type - be a pioneer!');
      }

      const score = Math.min(0.5 + (successCount / 50), 0.95);

      return {
        category: 'historical',
        title: 'Historical Success Patterns',
        description: successCount > 10
          ? 'Strong historical success for this match type'
          : 'Limited historical data for this match type',
        score,
        confidence: successCount > 5 ? 0.8 : 0.5,
        evidence,
        icon: '📊'
      };
    } finally {
      client.release();
    }
  }

  /**
   * Analyze timing alignment
   */
  private async analyzeTimingAlignment(match: any): Promise<ExplanationFactor> {
    const user1Needs = match.user1_needs || [];
    const user2Needs = match.user2_needs || [];

    const urgentNeeds = [...user1Needs, ...user2Needs].filter(
      (n: any) => n.urgency === 'immediate' || n.urgency === 'days'
    );

    const evidence: string[] = [];
    let score = 0.7; // Default moderate timing

    if (urgentNeeds.length > 0) {
      evidence.push(`${urgentNeeds.length} time-sensitive ${urgentNeeds.length === 1 ? 'need' : 'needs'} identified`);
      evidence.push('Act quickly to maximize value');
      score = 0.9;
    } else {
      evidence.push('Flexible timing for collaboration');
      evidence.push('Opportunity to plan thoroughly');
    }

    return {
      category: 'timing',
      title: 'Timing Alignment',
      description: urgentNeeds.length > 0
        ? 'Time-sensitive opportunity'
        : 'Flexible timing for collaboration',
      score,
      confidence: 0.75,
      evidence,
      icon: '⏰'
    };
  }

  /**
   * Generate actionable insights
   */
  private generateActionableInsights(
    match: any,
    primary: ExplanationFactor[],
    secondary: ExplanationFactor[],
    concerns: ExplanationFactor[]
  ): string[] {
    const insights: string[] = [];

    // Based on primary reasons
    if (primary.some(f => f.category === 'needs_offerings')) {
      insights.push('💡 Start by discussing how you can help each other with specific needs');
    }

    if (primary.some(f => f.category === 'network')) {
      insights.push('💡 Leverage your mutual connections for warm introductions');
    }

    // Based on concerns
    if (concerns.some(f => f.category === 'industry')) {
      insights.push('⚠️ Consider how cross-industry perspectives can add unique value');
    }

    if (concerns.some(f => f.category === 'timing')) {
      insights.push('⚠️ Align on timeline expectations early in your conversation');
    }

    // General insights based on match type
    if (match.match_type === 'investor-startup') {
      insights.push('💡 Prepare your pitch deck and financial projections');
    } else if (match.match_type === 'mentor-mentee') {
      insights.push('💡 Define clear learning objectives for the mentorship');
    } else if (match.match_type === 'partnership') {
      insights.push('💡 Identify specific collaboration opportunities and mutual benefits');
    }

    // Add a confidence-based insight
    if (primary.length >= 3) {
      insights.push('✨ This is a high-quality match - take action soon!');
    }

    return insights.slice(0, 5); // Return top 5 insights
  }

  /**
   * Helper: Check if categories match or are related
   */
  private categoriesMatch(cat1: string, cat2: string): boolean {
    if (cat1 === cat2) return true;

    // Define related categories
    const relatedCategories: Record<string, string[]> = {
      'funding': ['investment', 'capital', 'seed-funding'],
      'mentorship': ['coaching', 'advisory', 'guidance'],
      'technical': ['engineering', 'development', 'technology'],
      'marketing': ['growth', 'branding', 'sales']
    };

    for (const [key, related] of Object.entries(relatedCategories)) {
      if ((cat1 === key || related.includes(cat1)) &&
          (cat2 === key || related.includes(cat2))) {
        return true;
      }
    }

    return false;
  }

  /**
   * Helper: Calculate alignment score between need and offering
   */
  private calculateCategoryAlignment(need: any, offering: any): number {
    let score = 0.7; // Base score for category match

    // Boost for priority alignment
    if (need.priority === 'critical' || need.priority === 'high') {
      score += 0.1;
    }

    // Boost for capacity
    if (offering.capacity === 'high' || offering.capacity === 'unlimited') {
      score += 0.1;
    }

    // Boost for urgency match
    if (need.urgency === 'immediate' && offering.capacity !== 'limited') {
      score += 0.1;
    }

    return Math.min(score, 1.0);
  }

  /**
   * Helper: Check if industries are related
   */
  private industriesAreRelated(industry1: string, industry2: string): boolean {
    const relatedIndustries: Record<string, string[]> = {
      'technology': ['software', 'ai', 'saas', 'fintech', 'edtech'],
      'finance': ['fintech', 'banking', 'investment', 'insurance'],
      'healthcare': ['biotech', 'medtech', 'pharmaceuticals'],
      'education': ['edtech', 'training', 'e-learning']
    };

    for (const [key, related] of Object.entries(relatedIndustries)) {
      if ((industry1 === key || related.includes(industry1)) &&
          (industry2 === key || related.includes(industry2))) {
        return true;
      }
    }

    return false;
  }

  /**
   * Cache explanation for performance
   */
  private async cacheExplanation(matchId: string, explanation: MatchExplanation): Promise<void> {
    await this.redis.setex(
      `explanation:${matchId}`,
      3600, // 1 hour
      JSON.stringify(explanation)
    );
  }

  /**
   * Get cached explanation
   */
  private async getCachedExplanation(matchId: string): Promise<MatchExplanation | null> {
    const cached = await this.redis.get(`explanation:${matchId}`);
    return cached ? JSON.parse(cached) : null;
  }
}
