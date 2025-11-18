import { Pool } from 'pg';
import Redis from 'ioredis';

/**
 * Temporal Analysis Agent
 *
 * Tracks and analyzes network evolution over time:
 * - Connection growth patterns
 * - Trust evolution
 * - Centrality trends
 * - Community dynamics
 * - Relationship strength changes
 * - Predictive analytics
 * - Network health metrics
 *
 * Provides insights into how networks change and predicts future states.
 */

export interface NetworkSnapshot {
  timestamp: Date;
  userId: string;
  metrics: {
    totalConnections: number;
    averageTrustLevel: number;
    degreeCentrality: number;
    betweennessCentrality: number;
    pageRank: number;
    clusteringCoefficient: number;
    communityCount: number;
    networkDensity: number;
  };
}

export interface NetworkTrend {
  metric: string;
  timeframe: 'week' | 'month' | 'quarter' | 'year';
  startDate: Date;
  endDate: Date;
  startValue: number;
  endValue: number;
  change: number;
  percentageChange: number;
  trend: 'increasing' | 'decreasing' | 'stable';
  velocity: number; // Rate of change
  acceleration: number; // Change in rate of change
}

export interface ConnectionEvolution {
  userId1: string;
  userId2: string;
  firstConnected: Date;
  history: Array<{
    timestamp: Date;
    trustLevel: number;
    interactionCount: number;
    lastInteraction: Date;
  }>;
  overallTrend: 'strengthening' | 'weakening' | 'stable';
  predictions: {
    futureStrength30Days: number;
    futureStrength90Days: number;
    churnRisk: number; // 0-1
  };
}

export interface CommunityEvolution {
  communityId: string;
  formation: {
    detectedAt: Date;
    initialSize: number;
    foundingMembers: string[];
  };
  growth: Array<{
    timestamp: Date;
    size: number;
    density: number;
    modularity: number;
    newMembers: string[];
    departedMembers: string[];
  }>;
  predictions: {
    expectedSize30Days: number;
    growthRate: number;
    stabilityScore: number; // 0-1
    splitRisk: number; // 0-1
  };
}

export interface UserTrajectory {
  userId: string;
  userName: string;
  startDate: Date;
  milestones: Array<{
    date: Date;
    type: 'joined' | 'connection_milestone' | 'community_joined' | 'became_super_connector' | 'became_bridge';
    description: string;
    significance: 'low' | 'medium' | 'high';
  }>;
  growthPhases: Array<{
    startDate: Date;
    endDate: Date;
    phase: 'rapid_growth' | 'steady_growth' | 'plateau' | 'decline';
    avgConnectionsPerWeek: number;
  }>;
  currentPhase: 'rapid_growth' | 'steady_growth' | 'plateau' | 'decline';
  predictions: {
    expectedConnections30Days: number;
    expectedConnections90Days: number;
    likelyNextMilestone: string;
    engagementRisk: number; // 0-1
  };
}

export interface NetworkHealthReport {
  timestamp: Date;
  overallHealth: number; // 0-100
  indicators: {
    growthRate: number;
    churnRate: number;
    avgConnectionStrength: number;
    communityStability: number;
    trustLevels: number;
    engagement: number;
  };
  trends: {
    healthTrend: 'improving' | 'declining' | 'stable';
    concernAreas: string[];
    strengths: string[];
  };
  recommendations: string[];
}

export class TemporalAnalysisAgent {
  private readonly SNAPSHOT_INTERVAL_HOURS = 24;

  constructor(
    private pool: Pool,
    private redis: Redis
  ) {}

  /**
   * Capture current network snapshot for a user
   */
  async captureSnapshot(userId: string): Promise<NetworkSnapshot> {
    const metrics = await this.calculateCurrentMetrics(userId);

    const snapshot: NetworkSnapshot = {
      timestamp: new Date(),
      userId,
      metrics
    };

    // Store in database
    await this.storeSnapshot(snapshot);

    // Cache latest
    await this.redis.set(
      `snapshot:latest:${userId}`,
      JSON.stringify(snapshot),
      'EX',
      86400
    );

    return snapshot;
  }

  /**
   * Analyze trends for a user over time
   */
  async analyzeTrends(
    userId: string,
    timeframe: 'week' | 'month' | 'quarter' | 'year'
  ): Promise<NetworkTrend[]> {
    const endDate = new Date();
    const startDate = this.getStartDate(endDate, timeframe);

    const snapshots = await this.getSnapshots(userId, startDate, endDate);

    if (snapshots.length < 2) {
      return []; // Not enough data
    }

    const trends: NetworkTrend[] = [];
    const metrics = [
      'totalConnections',
      'averageTrustLevel',
      'degreeCentrality',
      'betweennessCentrality',
      'pageRank',
      'clusteringCoefficient'
    ];

    for (const metric of metrics) {
      const trend = this.calculateTrend(snapshots, metric, timeframe, startDate, endDate);
      trends.push(trend);
    }

    return trends;
  }

  /**
   * Track connection evolution over time
   */
  async trackConnectionEvolution(
    userId1: string,
    userId2: string
  ): Promise<ConnectionEvolution | null> {
    const history = await this.getConnectionHistory(userId1, userId2);

    if (history.length === 0) {
      return null;
    }

    // Determine overall trend
    const recentHistory = history.slice(-5);
    const olderHistory = history.slice(0, Math.min(5, history.length - 5));

    let overallTrend: 'strengthening' | 'weakening' | 'stable' = 'stable';

    if (recentHistory.length > 0 && olderHistory.length > 0) {
      const recentAvg = recentHistory.reduce((sum, h) => sum + h.trustLevel, 0) / recentHistory.length;
      const olderAvg = olderHistory.reduce((sum, h) => sum + h.trustLevel, 0) / olderHistory.length;

      if (recentAvg > olderAvg + 0.1) {
        overallTrend = 'strengthening';
      } else if (recentAvg < olderAvg - 0.1) {
        overallTrend = 'weakening';
      }
    }

    // Predict future strength
    const predictions = this.predictConnectionStrength(history);

    return {
      userId1,
      userId2,
      firstConnected: history[0].timestamp,
      history,
      overallTrend,
      predictions
    };
  }

  /**
   * Track community evolution
   */
  async trackCommunityEvolution(communityId: string): Promise<CommunityEvolution | null> {
    const growthHistory = await this.getCommunityHistory(communityId);

    if (growthHistory.length === 0) {
      return null;
    }

    const formation = {
      detectedAt: growthHistory[0].timestamp,
      initialSize: growthHistory[0].size,
      foundingMembers: growthHistory[0].newMembers
    };

    // Predict future
    const predictions = this.predictCommunityGrowth(growthHistory);

    return {
      communityId,
      formation,
      growth: growthHistory,
      predictions
    };
  }

  /**
   * Analyze user trajectory and growth patterns
   */
  async analyzeUserTrajectory(userId: string): Promise<UserTrajectory> {
    const startDate = await this.getUserJoinDate(userId);
    const snapshots = await this.getSnapshots(userId, startDate, new Date());

    // Identify milestones
    const milestones = this.identifyMilestones(snapshots);

    // Identify growth phases
    const growthPhases = this.identifyGrowthPhases(snapshots);

    // Current phase
    const currentPhase = growthPhases.length > 0
      ? growthPhases[growthPhases.length - 1].phase
      : 'steady_growth';

    // Predictions
    const predictions = this.predictUserGrowth(snapshots);

    const userProfile = await this.getUserProfile(userId);

    return {
      userId,
      userName: userProfile.name || 'Unknown',
      startDate,
      milestones,
      growthPhases,
      currentPhase,
      predictions
    };
  }

  /**
   * Generate network health report
   */
  async generateHealthReport(userId: string): Promise<NetworkHealthReport> {
    const snapshot = await this.captureSnapshot(userId);
    const trends = await this.analyzeTrends(userId, 'month');

    // Calculate health indicators
    const indicators = {
      growthRate: this.getGrowthRate(trends),
      churnRate: 0, // TODO: Calculate from departed connections
      avgConnectionStrength: snapshot.metrics.averageTrustLevel,
      communityStability: snapshot.metrics.clusteringCoefficient,
      trustLevels: snapshot.metrics.averageTrustLevel,
      engagement: this.calculateEngagement(snapshot)
    };

    // Overall health (weighted average)
    const overallHealth = Math.round(
      indicators.growthRate * 20 +
      (1 - indicators.churnRate) * 15 +
      indicators.avgConnectionStrength * 25 +
      indicators.communityStability * 20 +
      indicators.trustLevels * 15 +
      indicators.engagement * 5
    );

    // Determine health trend
    const connectionTrend = trends.find(t => t.metric === 'totalConnections');
    const healthTrend: 'improving' | 'declining' | 'stable' =
      connectionTrend && connectionTrend.trend === 'increasing' ? 'improving' :
      connectionTrend && connectionTrend.trend === 'decreasing' ? 'declining' :
      'stable';

    // Identify concerns and strengths
    const concernAreas: string[] = [];
    const strengths: string[] = [];

    if (indicators.growthRate < 0.3) {
      concernAreas.push('Low growth rate - network expansion needed');
    } else if (indicators.growthRate > 0.7) {
      strengths.push('Strong network growth');
    }

    if (indicators.avgConnectionStrength < 0.5) {
      concernAreas.push('Weak connection strength - trust building needed');
    } else if (indicators.avgConnectionStrength > 0.7) {
      strengths.push('High-quality connections');
    }

    if (indicators.communityStability < 0.3) {
      concernAreas.push('Low community integration');
    } else if (indicators.communityStability > 0.6) {
      strengths.push('Well-integrated in communities');
    }

    // Generate recommendations
    const recommendations: string[] = [];

    if (concernAreas.length > 0) {
      concernAreas.forEach(concern => {
        if (concern.includes('growth')) {
          recommendations.push('Focus on expanding network through introductions');
        } else if (concern.includes('trust')) {
          recommendations.push('Strengthen existing relationships before expanding');
        } else if (concern.includes('community')) {
          recommendations.push('Engage more actively with network communities');
        }
      });
    }

    return {
      timestamp: new Date(),
      overallHealth,
      indicators,
      trends: {
        healthTrend,
        concernAreas,
        strengths
      },
      recommendations
    };
  }

  /**
   * Compare two time periods
   */
  async compareTimePeriods(
    userId: string,
    period1Start: Date,
    period1End: Date,
    period2Start: Date,
    period2End: Date
  ): Promise<{
    period1: NetworkSnapshot;
    period2: NetworkSnapshot;
    changes: Map<string, {
      absolute: number;
      percentage: number;
      direction: 'increased' | 'decreased' | 'unchanged';
    }>;
  }> {
    const [snapshots1, snapshots2] = await Promise.all([
      this.getSnapshots(userId, period1Start, period1End),
      this.getSnapshots(userId, period2Start, period2End)
    ]);

    const period1Snapshot = this.aggregateSnapshots(snapshots1);
    const period2Snapshot = this.aggregateSnapshots(snapshots2);

    const changes = new Map<string, any>();

    const metrics = Object.keys(period1Snapshot.metrics) as Array<keyof NetworkSnapshot['metrics']>;

    for (const metric of metrics) {
      const val1 = period1Snapshot.metrics[metric];
      const val2 = period2Snapshot.metrics[metric];

      const absolute = val2 - val1;
      const percentage = val1 !== 0 ? (absolute / val1) * 100 : 0;

      const direction =
        Math.abs(absolute) < 0.01 ? 'unchanged' :
        absolute > 0 ? 'increased' : 'decreased';

      changes.set(metric, { absolute, percentage, direction });
    }

    return {
      period1: period1Snapshot,
      period2: period2Snapshot,
      changes
    };
  }

  /**
   * Private helper methods
   */

  private async calculateCurrentMetrics(userId: string): Promise<NetworkSnapshot['metrics']> {
    const client = await this.pool.connect();

    try {
      // Total connections
      const connResult = await client.query(`
        SELECT COUNT(*) as count
        FROM connections
        WHERE user_id = $1
      `, [userId]);
      const totalConnections = parseInt(connResult.rows[0]?.count || '0');

      // Average trust level
      const trustResult = await client.query(`
        SELECT AVG(trust_level) as avg_trust
        FROM connections
        WHERE user_id = $1
      `, [userId]);
      const averageTrustLevel = parseFloat(trustResult.rows[0]?.avg_trust || '0');

      // Simplified centrality metrics (would use actual algorithms in production)
      const degreeCentrality = totalConnections / 100; // Normalized
      const betweennessCentrality = 0.5; // Placeholder
      const pageRank = 0.5; // Placeholder
      const clusteringCoefficient = 0.5; // Placeholder
      const communityCount = 1; // Placeholder
      const networkDensity = 0.5; // Placeholder

      return {
        totalConnections,
        averageTrustLevel,
        degreeCentrality,
        betweennessCentrality,
        pageRank,
        clusteringCoefficient,
        communityCount,
        networkDensity
      };

    } finally {
      client.release();
    }
  }

  private async storeSnapshot(snapshot: NetworkSnapshot): Promise<void> {
    const client = await this.pool.connect();

    try {
      await client.query(`
        INSERT INTO network_snapshots (
          user_id, timestamp, total_connections, avg_trust_level,
          degree_centrality, betweenness_centrality, page_rank,
          clustering_coefficient, community_count, network_density
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
        ON CONFLICT (user_id, timestamp) DO UPDATE SET
          total_connections = EXCLUDED.total_connections,
          avg_trust_level = EXCLUDED.avg_trust_level
      `, [
        snapshot.userId,
        snapshot.timestamp,
        snapshot.metrics.totalConnections,
        snapshot.metrics.averageTrustLevel,
        snapshot.metrics.degreeCentrality,
        snapshot.metrics.betweennessCentrality,
        snapshot.metrics.pageRank,
        snapshot.metrics.clusteringCoefficient,
        snapshot.metrics.communityCount,
        snapshot.metrics.networkDensity
      ]);
    } catch (error) {
      // Table might not exist yet - that's ok
      console.log('Snapshot storage skipped:', error);
    } finally {
      client.release();
    }
  }

  private async getSnapshots(
    userId: string,
    startDate: Date,
    endDate: Date
  ): Promise<NetworkSnapshot[]> {
    const client = await this.pool.connect();

    try {
      const result = await client.query(`
        SELECT *
        FROM network_snapshots
        WHERE user_id = $1
        AND timestamp >= $2
        AND timestamp <= $3
        ORDER BY timestamp ASC
      `, [userId, startDate, endDate]);

      return result.rows.map(row => ({
        timestamp: row.timestamp,
        userId: row.user_id,
        metrics: {
          totalConnections: row.total_connections,
          averageTrustLevel: parseFloat(row.avg_trust_level),
          degreeCentrality: parseFloat(row.degree_centrality),
          betweennessCentrality: parseFloat(row.betweenness_centrality),
          pageRank: parseFloat(row.page_rank),
          clusteringCoefficient: parseFloat(row.clustering_coefficient),
          communityCount: row.community_count,
          networkDensity: parseFloat(row.network_density)
        }
      }));
    } catch (error) {
      // Return empty if table doesn't exist
      return [];
    } finally {
      client.release();
    }
  }

  private calculateTrend(
    snapshots: NetworkSnapshot[],
    metric: string,
    timeframe: 'week' | 'month' | 'quarter' | 'year',
    startDate: Date,
    endDate: Date
  ): NetworkTrend {
    const startSnapshot = snapshots[0];
    const endSnapshot = snapshots[snapshots.length - 1];

    const startValue = (startSnapshot.metrics as any)[metric] || 0;
    const endValue = (endSnapshot.metrics as any)[metric] || 0;

    const change = endValue - startValue;
    const percentageChange = startValue !== 0 ? (change / startValue) * 100 : 0;

    const trend: 'increasing' | 'decreasing' | 'stable' =
      Math.abs(percentageChange) < 5 ? 'stable' :
      percentageChange > 0 ? 'increasing' : 'decreasing';

    // Calculate velocity (rate of change per day)
    const daysDiff = Math.max(1, (endDate.getTime() - startDate.getTime()) / (1000 * 60 * 60 * 24));
    const velocity = change / daysDiff;

    // Calculate acceleration (simplified)
    const midPoint = Math.floor(snapshots.length / 2);
    const midSnapshot = snapshots[midPoint];
    const midValue = (midSnapshot?.metrics as any)[metric] || startValue;

    const firstHalfVelocity = (midValue - startValue) / (daysDiff / 2);
    const secondHalfVelocity = (endValue - midValue) / (daysDiff / 2);
    const acceleration = secondHalfVelocity - firstHalfVelocity;

    return {
      metric,
      timeframe,
      startDate,
      endDate,
      startValue,
      endValue,
      change,
      percentageChange,
      trend,
      velocity,
      acceleration
    };
  }

  private getStartDate(endDate: Date, timeframe: 'week' | 'month' | 'quarter' | 'year'): Date {
    const start = new Date(endDate);

    switch (timeframe) {
      case 'week':
        start.setDate(start.getDate() - 7);
        break;
      case 'month':
        start.setMonth(start.getMonth() - 1);
        break;
      case 'quarter':
        start.setMonth(start.getMonth() - 3);
        break;
      case 'year':
        start.setFullYear(start.getFullYear() - 1);
        break;
    }

    return start;
  }

  private async getConnectionHistory(
    userId1: string,
    userId2: string
  ): Promise<ConnectionEvolution['history']> {
    // Placeholder - would query connection_history table
    return [];
  }

  private predictConnectionStrength(
    history: ConnectionEvolution['history']
  ): ConnectionEvolution['predictions'] {
    if (history.length === 0) {
      return {
        futureStrength30Days: 0,
        futureStrength90Days: 0,
        churnRisk: 1
      };
    }

    const recentTrust = history[history.length - 1].trustLevel;
    const trend = history.length > 1
      ? recentTrust - history[history.length - 2].trustLevel
      : 0;

    return {
      futureStrength30Days: Math.max(0, Math.min(1, recentTrust + trend * 0.5)),
      futureStrength90Days: Math.max(0, Math.min(1, recentTrust + trend * 1.5)),
      churnRisk: recentTrust < 0.3 ? 0.7 : recentTrust < 0.5 ? 0.4 : 0.1
    };
  }

  private async getCommunityHistory(communityId: string): Promise<CommunityEvolution['growth']> {
    // Placeholder - would query community_history table
    return [];
  }

  private predictCommunityGrowth(
    growthHistory: CommunityEvolution['growth']
  ): CommunityEvolution['predictions'] {
    if (growthHistory.length === 0) {
      return {
        expectedSize30Days: 0,
        growthRate: 0,
        stabilityScore: 0,
        splitRisk: 0
      };
    }

    const current = growthHistory[growthHistory.length - 1];
    const growthRate = growthHistory.length > 1
      ? (current.size - growthHistory[0].size) / growthHistory.length
      : 0;

    return {
      expectedSize30Days: Math.round(current.size + growthRate * 30),
      growthRate,
      stabilityScore: current.density,
      splitRisk: current.size > 50 ? 0.6 : 0.2
    };
  }

  private identifyMilestones(snapshots: NetworkSnapshot[]): UserTrajectory['milestones'] {
    const milestones: UserTrajectory['milestones'] = [];

    for (let i = 0; i < snapshots.length; i++) {
      const snapshot = snapshots[i];

      // Connection milestones
      if (snapshot.metrics.totalConnections === 10 ||
          snapshot.metrics.totalConnections === 50 ||
          snapshot.metrics.totalConnections === 100) {
        milestones.push({
          date: snapshot.timestamp,
          type: 'connection_milestone',
          description: `Reached ${snapshot.metrics.totalConnections} connections`,
          significance: snapshot.metrics.totalConnections >= 100 ? 'high' : 'medium'
        });
      }

      // Super connector
      if (snapshot.metrics.degreeCentrality > 0.8) {
        milestones.push({
          date: snapshot.timestamp,
          type: 'became_super_connector',
          description: 'Became a super connector',
          significance: 'high'
        });
      }
    }

    return milestones;
  }

  private identifyGrowthPhases(snapshots: NetworkSnapshot[]): UserTrajectory['growthPhases'] {
    // Simplified implementation
    if (snapshots.length < 4) return [];

    const phases: UserTrajectory['growthPhases'] = [];
    let currentPhase: UserTrajectory['growthPhases'][0]['phase'] = 'steady_growth';

    const startSnapshot = snapshots[0];
    const endSnapshot = snapshots[snapshots.length - 1];

    const totalGrowth = endSnapshot.metrics.totalConnections - startSnapshot.metrics.totalConnections;
    const weeksDiff = Math.max(1, (endSnapshot.timestamp.getTime() - startSnapshot.timestamp.getTime()) / (1000 * 60 * 60 * 24 * 7));
    const avgConnectionsPerWeek = totalGrowth / weeksDiff;

    if (avgConnectionsPerWeek > 5) {
      currentPhase = 'rapid_growth';
    } else if (avgConnectionsPerWeek > 1) {
      currentPhase = 'steady_growth';
    } else if (avgConnectionsPerWeek < 0) {
      currentPhase = 'decline';
    } else {
      currentPhase = 'plateau';
    }

    phases.push({
      startDate: startSnapshot.timestamp,
      endDate: endSnapshot.timestamp,
      phase: currentPhase,
      avgConnectionsPerWeek
    });

    return phases;
  }

  private predictUserGrowth(snapshots: NetworkSnapshot[]): UserTrajectory['predictions'] {
    if (snapshots.length < 2) {
      return {
        expectedConnections30Days: 0,
        expectedConnections90Days: 0,
        likelyNextMilestone: 'Build first connections',
        engagementRisk: 0.5
      };
    }

    const current = snapshots[snapshots.length - 1];
    const previous = snapshots[snapshots.length - 2];

    const growth = current.metrics.totalConnections - previous.metrics.totalConnections;
    const daysDiff = (current.timestamp.getTime() - previous.timestamp.getTime()) / (1000 * 60 * 60 * 24);
    const dailyGrowth = growth / daysDiff;

    return {
      expectedConnections30Days: Math.round(current.metrics.totalConnections + dailyGrowth * 30),
      expectedConnections90Days: Math.round(current.metrics.totalConnections + dailyGrowth * 90),
      likelyNextMilestone: current.metrics.totalConnections < 10 ? 'Reach 10 connections' :
                           current.metrics.totalConnections < 50 ? 'Reach 50 connections' :
                           'Become super connector',
      engagementRisk: dailyGrowth < 0.1 ? 0.7 : dailyGrowth < 0.5 ? 0.3 : 0.1
    };
  }

  private getGrowthRate(trends: NetworkTrend[]): number {
    const connectionTrend = trends.find(t => t.metric === 'totalConnections');
    if (!connectionTrend) return 0.5;

    // Normalize to 0-1 based on percentage change
    return Math.max(0, Math.min(1, (connectionTrend.percentageChange + 50) / 100));
  }

  private calculateEngagement(snapshot: NetworkSnapshot): number {
    // Simplified: based on average trust level as proxy
    return snapshot.metrics.averageTrustLevel;
  }

  private aggregateSnapshots(snapshots: NetworkSnapshot[]): NetworkSnapshot {
    if (snapshots.length === 0) {
      return {
        timestamp: new Date(),
        userId: '',
        metrics: {
          totalConnections: 0,
          averageTrustLevel: 0,
          degreeCentrality: 0,
          betweennessCentrality: 0,
          pageRank: 0,
          clusteringCoefficient: 0,
          communityCount: 0,
          networkDensity: 0
        }
      };
    }

    const avgMetrics: NetworkSnapshot['metrics'] = {
      totalConnections: 0,
      averageTrustLevel: 0,
      degreeCentrality: 0,
      betweennessCentrality: 0,
      pageRank: 0,
      clusteringCoefficient: 0,
      communityCount: 0,
      networkDensity: 0
    };

    for (const snapshot of snapshots) {
      avgMetrics.totalConnections += snapshot.metrics.totalConnections;
      avgMetrics.averageTrustLevel += snapshot.metrics.averageTrustLevel;
      avgMetrics.degreeCentrality += snapshot.metrics.degreeCentrality;
      avgMetrics.betweennessCentrality += snapshot.metrics.betweennessCentrality;
      avgMetrics.pageRank += snapshot.metrics.pageRank;
      avgMetrics.clusteringCoefficient += snapshot.metrics.clusteringCoefficient;
      avgMetrics.communityCount += snapshot.metrics.communityCount;
      avgMetrics.networkDensity += snapshot.metrics.networkDensity;
    }

    const count = snapshots.length;
    Object.keys(avgMetrics).forEach(key => {
      (avgMetrics as any)[key] /= count;
    });

    return {
      timestamp: snapshots[snapshots.length - 1].timestamp,
      userId: snapshots[0].userId,
      metrics: avgMetrics
    };
  }

  private async getUserJoinDate(userId: string): Promise<Date> {
    const client = await this.pool.connect();
    try {
      const result = await client.query(
        'SELECT created_at FROM users WHERE id = $1',
        [userId]
      );
      return result.rows[0]?.created_at || new Date();
    } finally {
      client.release();
    }
  }

  private async getUserProfile(userId: string): Promise<any> {
    const client = await this.pool.connect();
    try {
      const result = await client.query(
        'SELECT name FROM users WHERE id = $1',
        [userId]
      );
      return result.rows[0] || {};
    } finally {
      client.release();
    }
  }
}
