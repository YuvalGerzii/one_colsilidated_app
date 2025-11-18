import { Pool } from 'pg';
import Redis from 'ioredis';
import { TrustPropagationAgent } from './TrustPropagationAgent';
import { TemporalAnalysisAgent } from './TemporalAnalysisAgent';

/**
 * Relationship Health Agent
 *
 * Monitors and analyzes the health of relationships in a user's network.
 *
 * Key capabilities:
 * - Relationship strength assessment
 * - Churn risk prediction
 * - Engagement level tracking
 * - Relationship lifecycle analysis
 * - Health trend monitoring
 * - Actionable recommendations for strengthening relationships
 */

export interface RelationshipHealth {
  userId1: string;
  userId2: string;
  user1Name: string;
  user2Name: string;

  overallHealth: number; // 0-100
  healthCategory: 'thriving' | 'healthy' | 'declining' | 'at_risk' | 'dormant';

  metrics: {
    trustLevel: number; // 0-1
    engagementFrequency: number; // 0-1 (how often they interact)
    responseRate: number; // 0-1
    mutuality: number; // 0-1 (bidirectional vs one-sided)
    longevity: number; // Days since connection
    recentActivity: number; // 0-1 (activity in last 30 days)
  };

  trend: {
    direction: 'improving' | 'stable' | 'declining';
    velocity: number; // Rate of change
    projection30Days: number; // Predicted health in 30 days
    projection90Days: number; // Predicted health in 90 days
  };

  risks: Array<{
    type: 'churn' | 'disengagement' | 'one_sided' | 'stale' | 'trust_erosion';
    severity: 'low' | 'medium' | 'high' | 'critical';
    probability: number; // 0-1
    description: string;
    indicators: string[];
  }>;

  opportunities: Array<{
    type: 'strengthen' | 'collaborate' | 'introduce' | 're_engage';
    priority: 'high' | 'medium' | 'low';
    description: string;
    expectedImpact: number; // 0-1
  }>;

  recommendations: Array<{
    action: string;
    priority: 'urgent' | 'high' | 'medium' | 'low';
    reasoning: string;
    timeframe: string;
    difficulty: 'easy' | 'medium' | 'hard';
  }>;

  lifecycle: {
    stage: 'new' | 'developing' | 'established' | 'mature' | 'declining' | 'dormant';
    daysSinceConnection: number;
    daysSinceLastInteraction: number;
    totalInteractions: number;
  };
}

export interface NetworkHealthSummary {
  userId: string;
  overallNetworkHealth: number; // 0-100
  totalRelationships: number;

  distribution: {
    thriving: number;
    healthy: number;
    declining: number;
    atRisk: number;
    dormant: number;
  };

  topConcerns: Array<{
    userId: string;
    userName: string;
    health: number;
    risk: string;
  }>;

  topOpportunities: Array<{
    userId: string;
    userName: string;
    opportunity: string;
    impact: number;
  }>;

  trends: {
    improving: number;
    stable: number;
    declining: number;
  };

  actionableInsights: string[];
  prioritizedRecommendations: Array<{
    targetUserId: string;
    action: string;
    priority: string;
    expectedImpact: number;
  }>;
}

export class RelationshipHealthAgent {
  // Health thresholds
  private readonly HEALTH_THRESHOLDS = {
    thriving: 80,
    healthy: 60,
    declining: 40,
    atRisk: 20,
  };

  // Churn risk factors
  private readonly CHURN_FACTORS = {
    noActivity30Days: 0.3,
    noActivity60Days: 0.6,
    noActivity90Days: 0.9,
    lowResponseRate: 0.4,
    lowMutuality: 0.3,
    trustDeclining: 0.5,
  };

  constructor(
    private pool: Pool,
    private redis: Redis,
    private trustAgent: TrustPropagationAgent,
    private temporalAgent: TemporalAnalysisAgent
  ) {}

  /**
   * Analyze health of a specific relationship
   */
  async analyzeRelationship(
    userId1: string,
    userId2: string
  ): Promise<RelationshipHealth> {
    // Check cache
    const cacheKey = `rel_health:${userId1}:${userId2}`;
    const cached = await this.redis.get(cacheKey);
    if (cached) return JSON.parse(cached);

    // Gather relationship data
    const [user1Profile, user2Profile, metrics, trustData, lifecycle] = await Promise.all([
      this.getUserProfile(userId1),
      this.getUserProfile(userId2),
      this.calculateMetrics(userId1, userId2),
      this.trustAgent.calculateTransitiveTrust(userId1, userId2),
      this.getLifecycleData(userId1, userId2),
    ]);

    // Calculate overall health
    const overallHealth = this.calculateOverallHealth(metrics);
    const healthCategory = this.categorizeHealth(overallHealth);

    // Analyze trends
    const trend = await this.analyzeTrend(userId1, userId2, overallHealth);

    // Identify risks
    const risks = this.identifyRisks(metrics, trend, lifecycle);

    // Find opportunities
    const opportunities = this.findOpportunities(metrics, lifecycle, healthCategory);

    // Generate recommendations
    const recommendations = this.generateRecommendations(risks, opportunities, metrics);

    const health: RelationshipHealth = {
      userId1,
      userId2,
      user1Name: user1Profile.name || 'Unknown',
      user2Name: user2Profile.name || 'Unknown',
      overallHealth,
      healthCategory,
      metrics,
      trend,
      risks,
      opportunities,
      recommendations,
      lifecycle,
    };

    // Cache for 15 minutes
    await this.redis.set(cacheKey, JSON.stringify(health), 'EX', 900);

    return health;
  }

  /**
   * Analyze health of all relationships for a user
   */
  async analyzeAllRelationships(userId: string): Promise<NetworkHealthSummary> {
    // Get all connections
    const connections = await this.getUserConnections(userId);

    // Analyze each relationship
    const healthAnalyses = await Promise.all(
      connections.map(connId => this.analyzeRelationship(userId, connId))
    );

    // Calculate distribution
    const distribution = {
      thriving: healthAnalyses.filter(h => h.healthCategory === 'thriving').length,
      healthy: healthAnalyses.filter(h => h.healthCategory === 'healthy').length,
      declining: healthAnalyses.filter(h => h.healthCategory === 'declining').length,
      atRisk: healthAnalyses.filter(h => h.healthCategory === 'at_risk').length,
      dormant: healthAnalyses.filter(h => h.healthCategory === 'dormant').length,
    };

    // Overall network health
    const overallNetworkHealth = healthAnalyses.length > 0
      ? Math.round(healthAnalyses.reduce((sum, h) => sum + h.overallHealth, 0) / healthAnalyses.length)
      : 0;

    // Top concerns (at-risk relationships)
    const topConcerns = healthAnalyses
      .filter(h => h.risks.length > 0)
      .sort((a, b) => a.overallHealth - b.overallHealth)
      .slice(0, 5)
      .map(h => ({
        userId: h.userId2,
        userName: h.user2Name,
        health: h.overallHealth,
        risk: h.risks[0].description,
      }));

    // Top opportunities
    const topOpportunities = healthAnalyses
      .filter(h => h.opportunities.length > 0)
      .sort((a, b) => {
        const aImpact = b.opportunities[0]?.expectedImpact || 0;
        const bImpact = a.opportunities[0]?.expectedImpact || 0;
        return aImpact - bImpact;
      })
      .slice(0, 5)
      .map(h => ({
        userId: h.userId2,
        userName: h.user2Name,
        opportunity: h.opportunities[0].description,
        impact: h.opportunities[0].expectedImpact,
      }));

    // Trends
    const trends = {
      improving: healthAnalyses.filter(h => h.trend.direction === 'improving').length,
      stable: healthAnalyses.filter(h => h.trend.direction === 'stable').length,
      declining: healthAnalyses.filter(h => h.trend.direction === 'declining').length,
    };

    // Actionable insights
    const actionableInsights = this.generateNetworkInsights(
      healthAnalyses,
      distribution,
      trends
    );

    // Prioritize recommendations across all relationships
    const allRecommendations = healthAnalyses.flatMap(h =>
      h.recommendations.map(r => ({
        targetUserId: h.userId2,
        action: r.action,
        priority: r.priority,
        expectedImpact: this.estimateImpact(r.priority),
      }))
    );

    const prioritizedRecommendations = allRecommendations
      .sort((a, b) => b.expectedImpact - a.expectedImpact)
      .slice(0, 10);

    return {
      userId,
      overallNetworkHealth,
      totalRelationships: connections.length,
      distribution,
      topConcerns,
      topOpportunities,
      trends,
      actionableInsights,
      prioritizedRecommendations,
    };
  }

  /**
   * Monitor relationships and send alerts for at-risk ones
   */
  async monitorAndAlert(userId: string): Promise<Array<{
    type: 'churn_risk' | 'engagement_drop' | 'trust_issue';
    targetUserId: string;
    severity: string;
    message: string;
  }>> {
    const summary = await this.analyzeAllRelationships(userId);
    const alerts: Array<any> = [];

    // Check for high-risk relationships
    for (const concern of summary.topConcerns) {
      if (concern.health < 30) {
        alerts.push({
          type: 'churn_risk',
          targetUserId: concern.userId,
          severity: 'high',
          message: `Relationship with ${concern.userName} is at risk: ${concern.risk}`,
        });
      }
    }

    // Check for declining trends
    if (summary.trends.declining > summary.totalRelationships * 0.3) {
      alerts.push({
        type: 'engagement_drop',
        targetUserId: userId,
        severity: 'medium',
        message: `${summary.trends.declining} relationships are declining - consider re-engagement strategy`,
      });
    }

    return alerts;
  }

  /**
   * Private helper methods
   */

  private async calculateMetrics(
    userId1: string,
    userId2: string
  ): Promise<RelationshipHealth['metrics']> {
    const [trustData, activityData] = await Promise.all([
      this.trustAgent.calculateTransitiveTrust(userId1, userId2),
      this.getActivityData(userId1, userId2),
    ]);

    return {
      trustLevel: trustData.directTrust || trustData.indirectTrust,
      engagementFrequency: activityData.frequency,
      responseRate: activityData.responseRate,
      mutuality: activityData.mutuality,
      longevity: activityData.longevity,
      recentActivity: activityData.recentActivity,
    };
  }

  private calculateOverallHealth(metrics: RelationshipHealth['metrics']): number {
    const weights = {
      trustLevel: 0.25,
      engagementFrequency: 0.20,
      responseRate: 0.15,
      mutuality: 0.15,
      recentActivity: 0.15,
      longevity: 0.10,
    };

    const normalizedLongevity = Math.min(1, metrics.longevity / 365); // Cap at 1 year

    const health =
      metrics.trustLevel * weights.trustLevel +
      metrics.engagementFrequency * weights.engagementFrequency +
      metrics.responseRate * weights.responseRate +
      metrics.mutuality * weights.mutuality +
      metrics.recentActivity * weights.recentActivity +
      normalizedLongevity * weights.longevity;

    return Math.round(health * 100);
  }

  private categorizeHealth(health: number): RelationshipHealth['healthCategory'] {
    if (health >= this.HEALTH_THRESHOLDS.thriving) return 'thriving';
    if (health >= this.HEALTH_THRESHOLDS.healthy) return 'healthy';
    if (health >= this.HEALTH_THRESHOLDS.declining) return 'declining';
    if (health >= this.HEALTH_THRESHOLDS.atRisk) return 'at_risk';
    return 'dormant';
  }

  private async analyzeTrend(
    userId1: string,
    userId2: string,
    currentHealth: number
  ): Promise<RelationshipHealth['trend']> {
    // Simplified trend analysis (would use historical data in production)
    const trend = await this.getHistoricalTrend(userId1, userId2);

    return {
      direction: trend.direction,
      velocity: trend.velocity,
      projection30Days: Math.max(0, Math.min(100, currentHealth + trend.velocity * 30)),
      projection90Days: Math.max(0, Math.min(100, currentHealth + trend.velocity * 90)),
    };
  }

  private identifyRisks(
    metrics: RelationshipHealth['metrics'],
    trend: RelationshipHealth['trend'],
    lifecycle: RelationshipHealth['lifecycle']
  ): RelationshipHealth['risks'] {
    const risks: RelationshipHealth['risks'] = [];

    // Churn risk
    if (lifecycle.daysSinceLastInteraction > 90) {
      risks.push({
        type: 'churn',
        severity: 'critical',
        probability: 0.9,
        description: 'No interaction in 90+ days - high churn risk',
        indicators: [`${lifecycle.daysSinceLastInteraction} days since last interaction`],
      });
    } else if (lifecycle.daysSinceLastInteraction > 60) {
      risks.push({
        type: 'churn',
        severity: 'high',
        probability: 0.6,
        description: 'No interaction in 60+ days',
        indicators: [`${lifecycle.daysSinceLastInteraction} days since last interaction`],
      });
    }

    // Disengagement risk
    if (metrics.recentActivity < 0.2) {
      risks.push({
        type: 'disengagement',
        severity: 'high',
        probability: 0.7,
        description: 'Very low recent activity',
        indicators: ['Minimal engagement in last 30 days'],
      });
    }

    // One-sided risk
    if (metrics.mutuality < 0.3) {
      risks.push({
        type: 'one_sided',
        severity: 'medium',
        probability: 0.5,
        description: 'Relationship appears one-sided',
        indicators: ['Low reciprocity in interactions'],
      });
    }

    // Trust erosion
    if (trend.direction === 'declining' && metrics.trustLevel < 0.5) {
      risks.push({
        type: 'trust_erosion',
        severity: 'high',
        probability: 0.6,
        description: 'Trust level declining',
        indicators: ['Downward trust trend'],
      });
    }

    return risks.sort((a, b) => {
      const severityWeight = { critical: 4, high: 3, medium: 2, low: 1 };
      return severityWeight[b.severity] - severityWeight[a.severity];
    });
  }

  private findOpportunities(
    metrics: RelationshipHealth['metrics'],
    lifecycle: RelationshipHealth['lifecycle'],
    category: RelationshipHealth['healthCategory']
  ): RelationshipHealth['opportunities'] {
    const opportunities: RelationshipHealth['opportunities'] = [];

    // Re-engagement opportunity
    if (lifecycle.daysSinceLastInteraction > 30 && lifecycle.daysSinceLastInteraction < 90) {
      opportunities.push({
        type: 're_engage',
        priority: 'high',
        description: 'Good candidate for re-engagement',
        expectedImpact: 0.7,
      });
    }

    // Strengthen opportunity
    if (category === 'healthy' && metrics.trustLevel > 0.6) {
      opportunities.push({
        type: 'strengthen',
        priority: 'medium',
        description: 'Potential to develop into strong relationship',
        expectedImpact: 0.6,
      });
    }

    // Collaboration opportunity
    if (metrics.trustLevel > 0.7 && metrics.mutuality > 0.7) {
      opportunities.push({
        type: 'collaborate',
        priority: 'high',
        description: 'Strong foundation for collaboration',
        expectedImpact: 0.8,
      });
    }

    // Introduction opportunity
    if (metrics.trustLevel > 0.8) {
      opportunities.push({
        type: 'introduce',
        priority: 'medium',
        description: 'Leverage this relationship for introductions',
        expectedImpact: 0.7,
      });
    }

    return opportunities;
  }

  private generateRecommendations(
    risks: RelationshipHealth['risks'],
    opportunities: RelationshipHealth['opportunities'],
    metrics: RelationshipHealth['metrics']
  ): RelationshipHealth['recommendations'] {
    const recommendations: RelationshipHealth['recommendations'] = [];

    // Address risks
    for (const risk of risks.slice(0, 2)) {
      if (risk.type === 'churn') {
        recommendations.push({
          action: 'Reach out with personalized message',
          priority: risk.severity === 'critical' ? 'urgent' : 'high',
          reasoning: 'Re-establish connection before relationship becomes dormant',
          timeframe: risk.severity === 'critical' ? 'This week' : 'This month',
          difficulty: 'easy',
        });
      } else if (risk.type === 'one_sided') {
        recommendations.push({
          action: 'Invite for coffee or video call',
          priority: 'medium',
          reasoning: 'Build stronger mutual engagement',
          timeframe: 'This month',
          difficulty: 'medium',
        });
      }
    }

    // Leverage opportunities
    for (const opp of opportunities.slice(0, 2)) {
      if (opp.type === 'collaborate') {
        recommendations.push({
          action: 'Propose collaboration project',
          priority: 'high',
          reasoning: 'Strong relationship foundation for collaboration',
          timeframe: 'This quarter',
          difficulty: 'medium',
        });
      } else if (opp.type === 're_engage') {
        recommendations.push({
          action: 'Share relevant article or opportunity',
          priority: 'medium',
          reasoning: 'Gentle re-engagement with value-add',
          timeframe: 'This week',
          difficulty: 'easy',
        });
      }
    }

    return recommendations.sort((a, b) => {
      const priorityWeight = { urgent: 4, high: 3, medium: 2, low: 1 };
      return priorityWeight[b.priority] - priorityWeight[a.priority];
    });
  }

  private generateNetworkInsights(
    analyses: RelationshipHealth[],
    distribution: NetworkHealthSummary['distribution'],
    trends: NetworkHealthSummary['trends']
  ): string[] {
    const insights: string[] = [];

    const totalRelationships = analyses.length;
    const atRiskPercentage = (distribution.atRisk / totalRelationships) * 100;
    const decliningPercentage = (trends.declining / totalRelationships) * 100;

    if (atRiskPercentage > 20) {
      insights.push(`${Math.round(atRiskPercentage)}% of relationships are at risk - prioritize re-engagement`);
    }

    if (decliningPercentage > 30) {
      insights.push(`${Math.round(decliningPercentage)}% of relationships are declining - review engagement strategy`);
    }

    if (distribution.thriving > totalRelationships * 0.4) {
      insights.push(`Strong network health with ${distribution.thriving} thriving relationships`);
    }

    if (distribution.dormant > totalRelationships * 0.3) {
      insights.push(`${distribution.dormant} dormant relationships - consider targeted re-activation campaign`);
    }

    return insights;
  }

  private estimateImpact(priority: string): number {
    const impacts = { urgent: 0.9, high: 0.7, medium: 0.5, low: 0.3 };
    return impacts[priority as keyof typeof impacts] || 0.5;
  }

  /**
   * Database helpers
   */

  private async getUserProfile(userId: string): Promise<any> {
    const client = await pool.connect();
    try {
      const result = await client.query(
        'SELECT id, name, email FROM users WHERE id = $1',
        [userId]
      );
      return result.rows[0] || {};
    } finally {
      client.release();
    }
  }

  private async getUserConnections(userId: string): Promise<string[]> {
    const client = await pool.connect();
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

  private async getActivityData(userId1: string, userId2: string): Promise<{
    frequency: number;
    responseRate: number;
    mutuality: number;
    longevity: number;
    recentActivity: number;
  }> {
    // Simplified - would query actual activity data
    return {
      frequency: 0.6,
      responseRate: 0.8,
      mutuality: 0.7,
      longevity: 180,
      recentActivity: 0.5,
    };
  }

  private async getLifecycleData(userId1: string, userId2: string): Promise<RelationshipHealth['lifecycle']> {
    // Simplified - would query actual connection data
    return {
      stage: 'established',
      daysSinceConnection: 180,
      daysSinceLastInteraction: 15,
      totalInteractions: 25,
    };
  }

  private async getHistoricalTrend(userId1: string, userId2: string): Promise<{
    direction: 'improving' | 'stable' | 'declining';
    velocity: number;
  }> {
    // Simplified - would analyze historical health data
    return {
      direction: 'stable',
      velocity: 0.1,
    };
  }
}
