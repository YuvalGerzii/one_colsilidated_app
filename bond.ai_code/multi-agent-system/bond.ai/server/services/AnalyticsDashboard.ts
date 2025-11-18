import { Pool } from 'pg';
import Redis from 'ioredis';

/**
 * Comprehensive Analytics Dashboard Service
 *
 * Provides detailed metrics and insights including:
 * - Match statistics and trends
 * - Negotiation performance
 * - Network growth
 * - Engagement metrics
 * - Success rates
 * - Comparative analytics
 */

export interface DashboardMetrics {
  overview: OverviewMetrics;
  matches: MatchMetrics;
  negotiations: NegotiationMetrics;
  network: NetworkMetrics;
  engagement: EngagementMetrics;
  success: SuccessMetrics;
  trends: TrendData[];
}

export interface OverviewMetrics {
  totalMatches: number;
  activeNegotiations: number;
  successfulAgreements: number;
  networkSize: number;
  responseRate: number;
  averageMatchScore: number;
}

export interface MatchMetrics {
  byType: Record<string, number>;
  byScore: {
    high: number; // >= 0.8
    medium: number; // 0.5-0.8
    low: number; // < 0.5
  };
  recentMatches: {
    date: Date;
    count: number;
  }[];
  topMatchedUsers: {
    name: string;
    score: number;
    matchType: string;
  }[];
}

export interface NegotiationMetrics {
  total: number;
  active: number;
  completed: number;
  successRate: number;
  averageRounds: number;
  averageDuration: number; // hours
  byStrategy: Record<string, number>;
  outcomeDistribution: Record<string, number>;
}

export interface NetworkMetrics {
  totalConnections: number;
  directConnections: number;
  secondDegree: number;
  thirdDegree: number;
  mutualConnections: number;
  averageTrustScore: number;
  strongestConnections: {
    name: string;
    trustScore: number;
    connectionStrength: number;
  }[];
  growthRate: number; // % per month
}

export interface EngagementMetrics {
  messagesExchanged: number;
  averageResponseTime: number; // seconds
  activeConversations: number;
  profileViews: number;
  searchQueries: number;
  clickThroughRate: number;
}

export interface SuccessMetrics {
  overallSuccessRate: number;
  successByMatchType: Record<string, number>;
  averageTimeToSuccess: number; // days
  mostSuccessfulStrategies: {
    strategy: string;
    successRate: number;
    count: number;
  }[];
  comparisonToPlatformAverage: {
    yourRate: number;
    platformRate: number;
    percentile: number;
  };
}

export interface TrendData {
  date: Date;
  matches: number;
  negotiations: number;
  agreements: number;
  networkGrowth: number;
}

export class AnalyticsDashboardService {
  private pool: Pool;
  private redis: Redis;

  constructor(pool: Pool, redis: Redis) {
    this.pool = pool;
    this.redis = redis;
  }

  /**
   * Get complete dashboard metrics for a user
   */
  async getDashboardMetrics(userId: string, timeRange: '7d' | '30d' | '90d' | '1y' = '30d'): Promise<DashboardMetrics> {
    // Check cache
    const cacheKey = `analytics:${userId}:${timeRange}`;
    const cached = await this.redis.get(cacheKey);
    if (cached) {
      return JSON.parse(cached);
    }

    const client = await this.pool.connect();

    try {
      const [overview, matches, negotiations, network, engagement, success, trends] = await Promise.all([
        this.getOverviewMetrics(client, userId, timeRange),
        this.getMatchMetrics(client, userId, timeRange),
        this.getNegotiationMetrics(client, userId, timeRange),
        this.getNetworkMetrics(client, userId),
        this.getEngagementMetrics(client, userId, timeRange),
        this.getSuccessMetrics(client, userId, timeRange),
        this.getTrendData(client, userId, timeRange)
      ]);

      const metrics: DashboardMetrics = {
        overview,
        matches,
        negotiations,
        network,
        engagement,
        success,
        trends
      };

      // Cache for 1 hour
      await this.redis.setex(cacheKey, 3600, JSON.stringify(metrics));

      return metrics;
    } finally {
      client.release();
    }
  }

  /**
   * Get overview metrics
   */
  private async getOverviewMetrics(client: any, userId: string, timeRange: string): Promise<OverviewMetrics> {
    const interval = this.getTimeInterval(timeRange);

    const result = await client.query(
      `SELECT
         (SELECT COUNT(*) FROM match_candidates mc
          JOIN agents a ON mc.initiator_agent_id = a.id
          WHERE a.user_id = $1 AND mc.created_at > NOW() - $2::INTERVAL) as total_matches,
         (SELECT COUNT(*) FROM negotiations n
          JOIN agents a ON n.initiator_agent_id = a.id
          WHERE a.user_id = $1 AND n.status = 'active') as active_negotiations,
         (SELECT COUNT(*) FROM agreements ag
          JOIN negotiations n ON ag.negotiation_id = n.id
          JOIN agents a ON n.initiator_agent_id = a.id
          WHERE a.user_id = $1 AND ag.created_at > NOW() - $2::INTERVAL) as successful_agreements,
         (SELECT COUNT(*) FROM connections c WHERE c.user_id = $1) as network_size,
         (SELECT AVG(compatibility_score) FROM match_candidates mc
          JOIN agents a ON mc.initiator_agent_id = a.id
          WHERE a.user_id = $1 AND mc.created_at > NOW() - $2::INTERVAL) as avg_match_score`,
      [userId, interval]
    );

    const data = result.rows[0];

    // Calculate response rate
    const responseResult = await client.query(
      `SELECT
         COUNT(DISTINCT m1.conversation_id) as responded,
         COUNT(DISTINCT m2.conversation_id) as total
       FROM messages m1
       JOIN messages m2 ON m1.conversation_id = m2.conversation_id
       WHERE m2.sender_id = $1
       AND m1.sender_id != $1
       AND m1.created_at > m2.created_at
       AND m1.created_at < m2.created_at + INTERVAL '48 hours'`,
      [userId]
    );

    const responseData = responseResult.rows[0];
    const responseRate = responseData.total > 0 ? responseData.responded / responseData.total : 0;

    return {
      totalMatches: parseInt(data.total_matches),
      activeNegotiations: parseInt(data.active_negotiations),
      successfulAgreements: parseInt(data.successful_agreements),
      networkSize: parseInt(data.network_size),
      responseRate,
      averageMatchScore: parseFloat(data.avg_match_score || '0')
    };
  }

  /**
   * Get match metrics
   */
  private async getMatchMetrics(client: any, userId: string, timeRange: string): Promise<MatchMetrics> {
    const interval = this.getTimeInterval(timeRange);

    // Match counts by type
    const byTypeResult = await client.query(
      `SELECT match_type, COUNT(*) as count
       FROM match_candidates mc
       JOIN agents a ON mc.initiator_agent_id = a.id
       WHERE a.user_id = $1 AND mc.created_at > NOW() - $2::INTERVAL
       GROUP BY match_type`,
      [userId, interval]
    );

    const byType: Record<string, number> = {};
    byTypeResult.rows.forEach(row => {
      byType[row.match_type] = parseInt(row.count);
    });

    // Match counts by score
    const byScoreResult = await client.query(
      `SELECT
         COUNT(CASE WHEN compatibility_score >= 0.8 THEN 1 END) as high,
         COUNT(CASE WHEN compatibility_score >= 0.5 AND compatibility_score < 0.8 THEN 1 END) as medium,
         COUNT(CASE WHEN compatibility_score < 0.5 THEN 1 END) as low
       FROM match_candidates mc
       JOIN agents a ON mc.initiator_agent_id = a.id
       WHERE a.user_id = $1 AND mc.created_at > NOW() - $2::INTERVAL`,
      [userId, interval]
    );

    const scoreData = byScoreResult.rows[0];
    const byScore = {
      high: parseInt(scoreData.high),
      medium: parseInt(scoreData.medium),
      low: parseInt(scoreData.low)
    };

    // Recent matches (daily counts)
    const recentResult = await client.query(
      `SELECT DATE(created_at) as date, COUNT(*) as count
       FROM match_candidates mc
       JOIN agents a ON mc.initiator_agent_id = a.id
       WHERE a.user_id = $1 AND mc.created_at > NOW() - $2::INTERVAL
       GROUP BY DATE(created_at)
       ORDER BY DATE(created_at)`,
      [userId, interval]
    );

    const recentMatches = recentResult.rows.map(row => ({
      date: new Date(row.date),
      count: parseInt(row.count)
    }));

    // Top matched users
    const topResult = await client.query(
      `SELECT u.name, mc.compatibility_score as score, mc.match_type
       FROM match_candidates mc
       JOIN agents a1 ON mc.initiator_agent_id = a1.id
       JOIN agents a2 ON mc.agent_id = a2.id
       JOIN users u ON a2.user_id = u.id
       WHERE a1.user_id = $1 AND mc.created_at > NOW() - $2::INTERVAL
       ORDER BY mc.compatibility_score DESC
       LIMIT 10`,
      [userId, interval]
    );

    const topMatchedUsers = topResult.rows.map(row => ({
      name: row.name,
      score: parseFloat(row.score),
      matchType: row.match_type
    }));

    return {
      byType,
      byScore,
      recentMatches,
      topMatchedUsers
    };
  }

  /**
   * Get negotiation metrics
   */
  private async getNegotiationMetrics(client: any, userId: string, timeRange: string): Promise<NegotiationMetrics> {
    const interval = this.getTimeInterval(timeRange);

    const result = await client.query(
      `SELECT
         COUNT(*) as total,
         COUNT(CASE WHEN status = 'active' THEN 1 END) as active,
         COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed,
         AVG(jsonb_array_length(conversation_history)) as avg_rounds,
         AVG(EXTRACT(EPOCH FROM (updated_at - created_at)) / 3600) as avg_duration
       FROM negotiations n
       JOIN agents a ON n.initiator_agent_id = a.id
       WHERE a.user_id = $1 AND n.created_at > NOW() - $2::INTERVAL`,
      [userId, interval]
    );

    const data = result.rows[0];
    const total = parseInt(data.total);
    const completed = parseInt(data.completed);
    const successRate = total > 0 ? completed / total : 0;

    // By strategy
    const strategyResult = await client.query(
      `SELECT metadata->>'strategy' as strategy, COUNT(*) as count
       FROM negotiations n
       JOIN agents a ON n.initiator_agent_id = a.id
       WHERE a.user_id = $1 AND n.created_at > NOW() - $2::INTERVAL
       AND metadata->>'strategy' IS NOT NULL
       GROUP BY metadata->>'strategy'`,
      [userId, interval]
    );

    const byStrategy: Record<string, number> = {};
    strategyResult.rows.forEach(row => {
      if (row.strategy) {
        byStrategy[row.strategy] = parseInt(row.count);
      }
    });

    // Outcome distribution
    const outcomeResult = await client.query(
      `SELECT status, COUNT(*) as count
       FROM negotiations n
       JOIN agents a ON n.initiator_agent_id = a.id
       WHERE a.user_id = $1 AND n.created_at > NOW() - $2::INTERVAL
       GROUP BY status`,
      [userId, interval]
    );

    const outcomeDistribution: Record<string, number> = {};
    outcomeResult.rows.forEach(row => {
      outcomeDistribution[row.status] = parseInt(row.count);
    });

    return {
      total,
      active: parseInt(data.active),
      completed,
      successRate,
      averageRounds: parseFloat(data.avg_rounds || '0'),
      averageDuration: parseFloat(data.avg_duration || '0'),
      byStrategy,
      outcomeDistribution
    };
  }

  /**
   * Get network metrics
   */
  private async getNetworkMetrics(client: any, userId: string): Promise<NetworkMetrics> {
    const result = await client.query(
      `SELECT
         COUNT(*) as total,
         COUNT(CASE WHEN degree_of_separation = 1 THEN 1 END) as direct,
         COUNT(CASE WHEN degree_of_separation = 2 THEN 1 END) as second_degree,
         COUNT(CASE WHEN degree_of_separation = 3 THEN 1 END) as third_degree,
         AVG(trust_level) as avg_trust
       FROM connections
       WHERE user_id = $1`,
      [userId]
    );

    const data = result.rows[0];

    // Strongest connections
    const strongestResult = await client.query(
      `SELECT c.name, conn.trust_level, conn.connection_strength
       FROM connections conn
       JOIN contacts c ON conn.contact_id = c.id
       WHERE conn.user_id = $1
       ORDER BY conn.connection_strength DESC
       LIMIT 10`,
      [userId]
    );

    const strongestConnections = strongestResult.rows.map(row => ({
      name: row.name,
      trustScore: parseFloat(row.trust_level),
      connectionStrength: parseFloat(row.connection_strength)
    }));

    // Growth rate (compare last 30 days to previous 30 days)
    const growthResult = await client.query(
      `SELECT
         COUNT(CASE WHEN created_at > NOW() - INTERVAL '30 days' THEN 1 END) as recent,
         COUNT(CASE WHEN created_at BETWEEN NOW() - INTERVAL '60 days' AND NOW() - INTERVAL '30 days' THEN 1 END) as previous
       FROM connections
       WHERE user_id = $1`,
      [userId]
    );

    const growthData = growthResult.rows[0];
    const recent = parseInt(growthData.recent);
    const previous = parseInt(growthData.previous);
    const growthRate = previous > 0 ? ((recent - previous) / previous) * 100 : 0;

    return {
      totalConnections: parseInt(data.total),
      directConnections: parseInt(data.direct),
      secondDegree: parseInt(data.second_degree),
      thirdDegree: parseInt(data.third_degree),
      mutualConnections: 0, // TODO: Calculate
      averageTrustScore: parseFloat(data.avg_trust || '0.5'),
      strongestConnections,
      growthRate
    };
  }

  /**
   * Get engagement metrics
   */
  private async getEngagementMetrics(client: any, userId: string, timeRange: string): Promise<EngagementMetrics> {
    const interval = this.getTimeInterval(timeRange);

    const result = await client.query(
      `SELECT
         (SELECT COUNT(*) FROM messages m
          WHERE m.sender_id = $1 AND m.created_at > NOW() - $2::INTERVAL) as messages,
         (SELECT COUNT(DISTINCT conversation_id) FROM messages m
          WHERE (m.sender_id = $1 OR m.recipient_id = $1)
          AND EXISTS (
            SELECT 1 FROM messages m2
            WHERE m2.conversation_id = m.conversation_id
            AND m2.created_at > NOW() - INTERVAL '7 days'
          )) as active_conversations,
         (SELECT COUNT(*) FROM search_analytics
          WHERE user_id = $1 AND timestamp > NOW() - $2::INTERVAL) as searches,
         (SELECT COUNT(*) FROM search_analytics
          WHERE user_id = $1
          AND clicked_result_id IS NOT NULL
          AND timestamp > NOW() - $2::INTERVAL) as clicks`,
      [userId, interval]
    );

    const data = result.rows[0];
    const searches = parseInt(data.searches);
    const clicks = parseInt(data.clicks);
    const clickThroughRate = searches > 0 ? clicks / searches : 0;

    // Average response time
    const responseTimeResult = await client.query(
      `SELECT AVG(
         EXTRACT(EPOCH FROM (m2.created_at - m1.created_at))
       ) as avg_response_time
       FROM messages m1
       JOIN messages m2 ON m1.conversation_id = m2.conversation_id
       WHERE m1.recipient_id = $1
       AND m2.sender_id = $1
       AND m2.created_at > m1.created_at
       AND EXTRACT(EPOCH FROM (m2.created_at - m1.created_at)) < 604800
       AND m1.created_at > NOW() - $2::INTERVAL`,
      [userId, interval]
    );

    return {
      messagesExchanged: parseInt(data.messages),
      averageResponseTime: parseFloat(responseTimeResult.rows[0]?.avg_response_time || '0'),
      activeConversations: parseInt(data.active_conversations),
      profileViews: 0, // TODO: Implement
      searchQueries: searches,
      clickThroughRate
    };
  }

  /**
   * Get success metrics
   */
  private async getSuccessMetrics(client: any, userId: string, timeRange: string): Promise<SuccessMetrics> {
    const interval = this.getTimeInterval(timeRange);

    // Overall success rate
    const overallResult = await client.query(
      `SELECT
         COUNT(DISTINCT mc.id) as total_matches,
         COUNT(DISTINCT ag.id) as successful_agreements
       FROM match_candidates mc
       JOIN agents a ON mc.initiator_agent_id = a.id
       LEFT JOIN negotiations n ON mc.id = n.match_id
       LEFT JOIN agreements ag ON n.id = ag.negotiation_id
       WHERE a.user_id = $1 AND mc.created_at > NOW() - $2::INTERVAL`,
      [userId, interval]
    );

    const overall = overallResult.rows[0];
    const totalMatches = parseInt(overall.total_matches);
    const successfulAgreements = parseInt(overall.successful_agreements);
    const overallSuccessRate = totalMatches > 0 ? successfulAgreements / totalMatches : 0;

    // Success by match type
    const byTypeResult = await client.query(
      `SELECT
         mc.match_type,
         COUNT(DISTINCT mc.id) as total,
         COUNT(DISTINCT ag.id) as successful
       FROM match_candidates mc
       JOIN agents a ON mc.initiator_agent_id = a.id
       LEFT JOIN negotiations n ON mc.id = n.match_id
       LEFT JOIN agreements ag ON n.id = ag.negotiation_id
       WHERE a.user_id = $1 AND mc.created_at > NOW() - $2::INTERVAL
       GROUP BY mc.match_type`,
      [userId, interval]
    );

    const successByMatchType: Record<string, number> = {};
    byTypeResult.rows.forEach(row => {
      const total = parseInt(row.total);
      const successful = parseInt(row.successful);
      successByMatchType[row.match_type] = total > 0 ? successful / total : 0;
    });

    // Average time to success
    const timeToSuccessResult = await client.query(
      `SELECT AVG(
         EXTRACT(EPOCH FROM (ag.created_at - mc.created_at)) / 86400
       ) as avg_days
       FROM match_candidates mc
       JOIN agents a ON mc.initiator_agent_id = a.id
       JOIN negotiations n ON mc.id = n.match_id
       JOIN agreements ag ON n.id = ag.negotiation_id
       WHERE a.user_id = $1 AND mc.created_at > NOW() - $2::INTERVAL`,
      [userId, interval]
    );

    const averageTimeToSuccess = parseFloat(timeToSuccessResult.rows[0]?.avg_days || '0');

    // Most successful strategies
    const strategiesResult = await client.query(
      `SELECT
         n.metadata->>'strategy' as strategy,
         COUNT(*) as total,
         COUNT(ag.id) as successful
       FROM negotiations n
       JOIN agents a ON n.initiator_agent_id = a.id
       LEFT JOIN agreements ag ON n.id = ag.negotiation_id
       WHERE a.user_id = $1
       AND n.created_at > NOW() - $2::INTERVAL
       AND n.metadata->>'strategy' IS NOT NULL
       GROUP BY n.metadata->>'strategy'
       ORDER BY COUNT(ag.id)::float / COUNT(*)::float DESC
       LIMIT 5`,
      [userId, interval]
    );

    const mostSuccessfulStrategies = strategiesResult.rows.map(row => ({
      strategy: row.strategy,
      successRate: parseInt(row.total) > 0 ? parseInt(row.successful) / parseInt(row.total) : 0,
      count: parseInt(row.total)
    }));

    // Comparison to platform average
    const platformResult = await client.query(
      `SELECT
         COUNT(DISTINCT mc.id) as total_matches,
         COUNT(DISTINCT ag.id) as successful_agreements
       FROM match_candidates mc
       LEFT JOIN negotiations n ON mc.id = n.match_id
       LEFT JOIN agreements ag ON n.id = ag.negotiation_id
       WHERE mc.created_at > NOW() - $2::INTERVAL`,
      [userId, interval]
    );

    const platform = platformResult.rows[0];
    const platformTotal = parseInt(platform.total_matches);
    const platformSuccessful = parseInt(platform.successful_agreements);
    const platformRate = platformTotal > 0 ? platformSuccessful / platformTotal : 0;

    // Calculate percentile
    const percentileResult = await client.query(
      `SELECT percentile_cont(0.5) WITHIN GROUP (ORDER BY success_rate) as median
       FROM (
         SELECT
           COUNT(DISTINCT ag.id)::float / NULLIF(COUNT(DISTINCT mc.id), 0) as success_rate
         FROM match_candidates mc
         JOIN agents a ON mc.initiator_agent_id = a.id
         LEFT JOIN negotiations n ON mc.id = n.match_id
         LEFT JOIN agreements ag ON n.id = ag.negotiation_id
         WHERE mc.created_at > NOW() - $1::INTERVAL
         GROUP BY a.user_id
         HAVING COUNT(DISTINCT mc.id) >= 5
       ) rates`,
      [interval]
    );

    const medianRate = parseFloat(percentileResult.rows[0]?.median || '0.5');
    const percentile = overallSuccessRate >= medianRate ?
      50 + ((overallSuccessRate - medianRate) / (1 - medianRate) * 50) :
      (overallSuccessRate / medianRate * 50);

    return {
      overallSuccessRate,
      successByMatchType,
      averageTimeToSuccess,
      mostSuccessfulStrategies,
      comparisonToPlatformAverage: {
        yourRate: overallSuccessRate,
        platformRate,
        percentile
      }
    };
  }

  /**
   * Get trend data
   */
  private async getTrendData(client: any, userId: string, timeRange: string): Promise<TrendData[]> {
    const interval = this.getTimeInterval(timeRange);

    const result = await client.query(
      `SELECT
         date_series.date,
         COALESCE(match_counts.count, 0) as matches,
         COALESCE(negotiation_counts.count, 0) as negotiations,
         COALESCE(agreement_counts.count, 0) as agreements,
         COALESCE(network_growth.count, 0) as network_growth
       FROM generate_series(
         NOW() - $1::INTERVAL,
         NOW(),
         '1 day'::interval
       ) as date_series(date)
       LEFT JOIN (
         SELECT DATE(created_at) as date, COUNT(*) as count
         FROM match_candidates mc
         JOIN agents a ON mc.initiator_agent_id = a.id
         WHERE a.user_id = $2
         GROUP BY DATE(created_at)
       ) match_counts ON date_series.date = match_counts.date
       LEFT JOIN (
         SELECT DATE(created_at) as date, COUNT(*) as count
         FROM negotiations n
         JOIN agents a ON n.initiator_agent_id = a.id
         WHERE a.user_id = $2
         GROUP BY DATE(created_at)
       ) negotiation_counts ON date_series.date = negotiation_counts.date
       LEFT JOIN (
         SELECT DATE(created_at) as date, COUNT(*) as count
         FROM agreements ag
         JOIN negotiations n ON ag.negotiation_id = n.id
         JOIN agents a ON n.initiator_agent_id = a.id
         WHERE a.user_id = $2
         GROUP BY DATE(created_at)
       ) agreement_counts ON date_series.date = agreement_counts.date
       LEFT JOIN (
         SELECT DATE(created_at) as date, COUNT(*) as count
         FROM connections
         WHERE user_id = $2
         GROUP BY DATE(created_at)
       ) network_growth ON date_series.date = network_growth.date
       ORDER BY date_series.date`,
      [interval, userId]
    );

    return result.rows.map(row => ({
      date: new Date(row.date),
      matches: parseInt(row.matches),
      negotiations: parseInt(row.negotiations),
      agreements: parseInt(row.agreements),
      networkGrowth: parseInt(row.network_growth)
    }));
  }

  /**
   * Helper: Get time interval string
   */
  private getTimeInterval(timeRange: string): string {
    switch (timeRange) {
      case '7d': return '7 days';
      case '30d': return '30 days';
      case '90d': return '90 days';
      case '1y': return '1 year';
      default: return '30 days';
    }
  }
}
