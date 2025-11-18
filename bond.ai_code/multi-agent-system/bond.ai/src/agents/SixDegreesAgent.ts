import { Pool } from 'pg';
import Redis from 'ioredis';
import { NetworkTraversalAgent, ConnectionPath, PathNode } from './NetworkTraversalAgent';

/**
 * Six Degrees Agent
 *
 * Specialized agent for demonstrating and utilizing the "Six Degrees of Separation" theory:
 * - Verifies if two people are connected within 6 degrees
 * - Finds the most influential connectors
 * - Suggests optimal introduction paths
 * - Analyzes network reachability
 *
 * Theory: Most people are connected through at most 6 intermediaries
 * Research shows modern social networks often have even smaller degrees (3-4)
 */

export interface SixDegreesResult {
  connected: boolean;
  degrees: number;
  path: ConnectionPath | null;
  alternativePaths?: ConnectionPath[];
  connectorNodes?: PathNode[];
  insight: string;
}

export interface IntroductionPath {
  path: ConnectionPath;
  introducers: Array<{
    userId: string;
    name: string;
    influence: number; // How influential this person is
    willingnessToIntroduce: number; // Based on relationship strength
  }>;
  recommendedApproach: string;
  estimatedSuccess: number;
}

export interface NetworkReachability {
  userId: string;
  userName: string;
  reachableWithin6Degrees: number;
  percentageOfNetwork: number;
  averageDegreesToReach: number;
  unreachableUsers: number;
  strongConnections: number; // Within 2 degrees
  weakConnections: number; // 3-6 degrees
}

export class SixDegreesAgent {
  private traversalAgent: NetworkTraversalAgent;

  constructor(
    private pool: Pool,
    private redis: Redis
  ) {
    this.traversalAgent = new NetworkTraversalAgent(pool, redis);
  }

  /**
   * Check if two users are connected within six degrees
   */
  async verifySixDegrees(
    sourceUserId: string,
    targetUserId: string
  ): Promise<SixDegreesResult> {
    const cacheKey = `six_degrees:${sourceUserId}:${targetUserId}`;
    const cached = await this.redis.get(cacheKey);

    if (cached) {
      return JSON.parse(cached);
    }

    // Find shortest path
    const shortestPath = await this.traversalAgent.findShortestPath(sourceUserId, targetUserId);

    if (!shortestPath) {
      const result: SixDegreesResult = {
        connected: false,
        degrees: Infinity,
        path: null,
        insight: 'No connection found. These users are in separate network clusters.'
      };

      await this.redis.set(cacheKey, JSON.stringify(result), 'EX', 3600);
      return result;
    }

    const degrees = shortestPath.length;
    const connected = degrees <= 6;

    // Get alternative paths
    const alternativePaths = await this.traversalAgent.findAlternativePaths(
      sourceUserId,
      targetUserId,
      3,
      6
    );

    // Extract connector nodes (nodes that appear in multiple paths)
    const connectorNodes = this.identifyConnectorNodes(alternativePaths);

    let insight = '';
    if (degrees === 1) {
      insight = 'Direct connection! These users are already connected.';
    } else if (degrees === 2) {
      insight = `Connected through one mutual contact (${shortestPath.path[1].name}). Strong potential for introduction.`;
    } else if (degrees <= 3) {
      insight = `Connected within ${degrees} degrees through ${degrees - 1} intermediaries. Good chance of successful introduction.`;
    } else if (degrees <= 6) {
      insight = `Connected within ${degrees} degrees. Demonstrates the "six degrees of separation" principle. Introduction possible but may require more effort.`;
    } else {
      insight = `Connected, but requires ${degrees} intermediaries. Beyond typical six-degree range. Consider finding alternative paths.`;
    }

    const result: SixDegreesResult = {
      connected,
      degrees,
      path: shortestPath,
      alternativePaths: alternativePaths.slice(1, 3), // Top 2 alternatives
      connectorNodes,
      insight
    };

    // Cache for 1 hour
    await this.redis.set(cacheKey, JSON.stringify(result), 'EX', 3600);

    return result;
  }

  /**
   * Find the best introduction path with recommended approach
   */
  async findBestIntroductionPath(
    sourceUserId: string,
    targetUserId: string
  ): Promise<IntroductionPath | null> {
    const sixDegrees = await this.verifySixDegrees(sourceUserId, targetUserId);

    if (!sixDegrees.connected || !sixDegrees.path) {
      return null;
    }

    // Get all paths within reasonable length
    const allPaths = await this.traversalAgent.findAlternativePaths(
      sourceUserId,
      targetUserId,
      5,
      6
    );

    if (allPaths.length === 0) {
      return null;
    }

    // Score each path for introduction potential
    const scoredPaths = await Promise.all(
      allPaths.map(async path => ({
        path,
        score: await this.scoreIntroductionPath(path)
      }))
    );

    // Get best path
    scoredPaths.sort((a, b) => b.score - a.score);
    const bestPath = scoredPaths[0].path;

    // Identify introducers (all intermediaries)
    const introducers = [];
    for (let i = 1; i < bestPath.path.length - 1; i++) {
      const node = bestPath.path[i];
      const influence = await this.calculateUserInfluence(node.userId);
      const prevNode = bestPath.path[i - 1];
      const nextNode = bestPath.path[i + 1];

      introducers.push({
        userId: node.userId,
        name: node.name,
        influence,
        willingnessToIntroduce: (node.trustLevel || 0.5) * (node.connectionStrength || 0.5)
      });
    }

    // Generate recommendation
    const recommendedApproach = this.generateIntroductionRecommendation(bestPath, introducers);

    // Estimate success probability
    const estimatedSuccess = scoredPaths[0].score;

    return {
      path: bestPath,
      introducers,
      recommendedApproach,
      estimatedSuccess
    };
  }

  /**
   * Analyze network reachability for a user
   */
  async analyzeNetworkReachability(userId: string): Promise<NetworkReachability> {
    const cacheKey = `reachability:${userId}`;
    const cached = await this.redis.get(cacheKey);

    if (cached) {
      return JSON.parse(cached);
    }

    // Get all users within 6 degrees
    const allPaths = await this.traversalAgent.findAllPathsWithinDegrees(userId, 6);

    let totalDegrees = 0;
    let strongConnections = 0; // 1-2 degrees
    let weakConnections = 0; // 3-6 degrees

    for (const [targetUserId, path] of allPaths) {
      const degrees = path.length;
      totalDegrees += degrees;

      if (degrees <= 2) {
        strongConnections++;
      } else {
        weakConnections++;
      }
    }

    const reachableCount = allPaths.size;

    // Get total network size
    const client = await this.pool.connect();
    let totalUsers = 0;

    try {
      const result = await client.query('SELECT COUNT(*) as count FROM users');
      totalUsers = parseInt(result.rows[0].count);
    } finally {
      client.release();
    }

    const unreachableUsers = Math.max(0, totalUsers - reachableCount - 1); // -1 for self
    const percentageOfNetwork = totalUsers > 1 ? (reachableCount / (totalUsers - 1)) * 100 : 0;
    const averageDegreesToReach = reachableCount > 0 ? totalDegrees / reachableCount : 0;

    const userName = await this.getUserName(userId);

    const reachability: NetworkReachability = {
      userId,
      userName,
      reachableWithin6Degrees: reachableCount,
      percentageOfNetwork,
      averageDegreesToReach,
      unreachableUsers,
      strongConnections,
      weakConnections
    };

    // Cache for 10 minutes
    await this.redis.set(cacheKey, JSON.stringify(reachability), 'EX', 600);

    return reachability;
  }

  /**
   * Find the most connected people (super connectors)
   * These are key to six degrees of separation
   */
  async findSuperConnectors(topN: number = 10): Promise<Array<{
    userId: string;
    name: string;
    directConnections: number;
    reachability: number; // % of network reachable within 3 degrees
    influence: number;
    role: string;
  }>> {
    const cacheKey = `super_connectors:${topN}`;
    const cached = await this.redis.get(cacheKey);

    if (cached) {
      return JSON.parse(cached);
    }

    const client = await this.pool.connect();

    try {
      // Get users with most direct connections
      const result = await client.query(`
        SELECT
          u.id,
          u.name,
          COUNT(c.id) as connection_count
        FROM users u
        JOIN connections c ON u.id = c.user_id
        GROUP BY u.id, u.name
        ORDER BY connection_count DESC
        LIMIT $1
      `, [topN * 2]); // Get 2x to analyze further

      const candidates = result.rows;

      // Analyze each candidate
      const analyzed = await Promise.all(
        candidates.map(async candidate => {
          const reachability = await this.analyzeNetworkReachability(candidate.id);
          const influence = await this.calculateUserInfluence(candidate.id);

          return {
            userId: candidate.id,
            name: candidate.name,
            directConnections: parseInt(candidate.connection_count),
            reachability: reachability.percentageOfNetwork,
            influence,
            role: this.categorizeConnectorRole(
              parseInt(candidate.connection_count),
              reachability.percentageOfNetwork,
              influence
            )
          };
        })
      );

      // Sort by combination of factors
      analyzed.sort((a, b) => {
        const scoreA = a.directConnections * 0.3 + a.reachability * 0.4 + a.influence * 0.3;
        const scoreB = b.directConnections * 0.3 + b.reachability * 0.4 + b.influence * 0.3;
        return scoreB - scoreA;
      });

      const result_connectors = analyzed.slice(0, topN);

      // Cache for 15 minutes
      await this.redis.set(cacheKey, JSON.stringify(result_connectors), 'EX', 900);

      return result_connectors;

    } finally {
      client.release();
    }
  }

  /**
   * Demonstrate six degrees by finding paths between random users
   */
  async demonstrateSixDegrees(sampleSize: number = 20): Promise<{
    totalPairs: number;
    connectedPairs: number;
    averageDegrees: number;
    maxDegrees: number;
    within6Degrees: number;
    distribution: Record<number, number>; // degree -> count
    examples: SixDegreesResult[];
  }> {
    const users = await this.getSampleUsers(sampleSize);
    const results: SixDegreesResult[] = [];
    const distribution: Record<number, number> = {};
    let totalDegrees = 0;
    let maxDegrees = 0;
    let connectedPairs = 0;
    let within6Degrees = 0;

    // Test pairs
    for (let i = 0; i < users.length - 1; i++) {
      for (let j = i + 1; j < Math.min(i + 5, users.length); j++) { // Limit to avoid too many pairs
        const result = await this.verifySixDegrees(users[i], users[j]);
        results.push(result);

        if (result.connected) {
          connectedPairs++;
          totalDegrees += result.degrees;
          maxDegrees = Math.max(maxDegrees, result.degrees);

          distribution[result.degrees] = (distribution[result.degrees] || 0) + 1;

          if (result.degrees <= 6) {
            within6Degrees++;
          }
        }
      }
    }

    const totalPairs = results.length;
    const averageDegrees = connectedPairs > 0 ? totalDegrees / connectedPairs : 0;

    // Get interesting examples
    const examples = results
      .filter(r => r.connected)
      .sort((a, b) => a.degrees - b.degrees)
      .slice(0, 5);

    return {
      totalPairs,
      connectedPairs,
      averageDegrees,
      maxDegrees,
      within6Degrees,
      distribution,
      examples
    };
  }

  /**
   * Private helper methods
   */

  private identifyConnectorNodes(paths: ConnectionPath[]): PathNode[] {
    const nodeFrequency = new Map<string, { node: PathNode; count: number }>();

    // Count how often each node appears
    for (const path of paths) {
      for (let i = 1; i < path.path.length - 1; i++) { // Exclude source and target
        const node = path.path[i];
        const existing = nodeFrequency.get(node.userId);

        if (existing) {
          existing.count++;
        } else {
          nodeFrequency.set(node.userId, { node, count: 1 });
        }
      }
    }

    // Return nodes that appear in multiple paths
    return Array.from(nodeFrequency.values())
      .filter(({ count }) => count > 1)
      .sort((a, b) => b.count - a.count)
      .map(({ node }) => node)
      .slice(0, 5); // Top 5 connectors
  }

  private async scoreIntroductionPath(path: ConnectionPath): Promise<number> {
    // Score based on:
    // - Path length (shorter is better)
    // - Connection strength (stronger is better)
    // - Trust levels (higher is better)
    // - Influence of intermediaries (higher is better)

    const lengthScore = 1 / (path.length + 1); // 0-1, shorter is better
    const strengthScore = path.totalStrength / Math.max(path.length, 1); // Average strength
    const trustScore = path.averageTrust;

    // Calculate influence of intermediaries
    let totalInfluence = 0;
    for (let i = 1; i < path.path.length - 1; i++) {
      const influence = await this.calculateUserInfluence(path.path[i].userId);
      totalInfluence += influence;
    }
    const avgInfluence = path.length > 1 ? totalInfluence / (path.length - 1) : 0;

    // Weighted combination
    return (
      lengthScore * 0.3 +
      strengthScore * 0.25 +
      trustScore * 0.25 +
      avgInfluence * 0.2
    );
  }

  private async calculateUserInfluence(userId: string): Promise<number> {
    // Influence based on:
    // - Number of connections (degree centrality)
    // - Quality of connections
    // - Activity level

    const client = await this.pool.connect();

    try {
      const result = await client.query(`
        SELECT
          COUNT(*) as connection_count,
          AVG(connection_strength) as avg_strength,
          AVG(trust_level) as avg_trust
        FROM connections
        WHERE user_id = $1
      `, [userId]);

      const data = result.rows[0];
      const connectionCount = parseInt(data.connection_count);
      const avgStrength = parseFloat(data.avg_strength) || 0;
      const avgTrust = parseFloat(data.avg_trust) || 0;

      // Normalize connection count (assume max 100)
      const normalizedCount = Math.min(connectionCount / 100, 1);

      return (normalizedCount * 0.4 + avgStrength * 0.3 + avgTrust * 0.3);

    } finally {
      client.release();
    }
  }

  private generateIntroductionRecommendation(
    path: ConnectionPath,
    introducers: Array<{ name: string; influence: number; willingnessToIntroduce: number }>
  ): string {
    if (path.length === 1) {
      return 'Direct connection - no introduction needed.';
    }

    if (path.length === 2) {
      return `Ask ${introducers[0].name} to introduce you. With a ${(introducers[0].willingnessToIntroduce * 100).toFixed(0)}% likelihood of willingness, a direct request is recommended.`;
    }

    // Multi-hop introduction
    const primaryIntroducer = introducers[0];
    const secondaryIntroducer = introducers[1];

    if (primaryIntroducer.influence > 0.7 && primaryIntroducer.willingnessToIntroduce > 0.7) {
      return `Recommended approach: Ask ${primaryIntroducer.name} (highly influential connector) to facilitate the introduction through their network. High probability of success.`;
    }

    return `Recommended approach: Chain introduction through ${introducers.length} intermediaries. ` +
           `Start with ${primaryIntroducer.name}, who can connect you to ${secondaryIntroducer.name}. ` +
           `Be transparent about your intent and value proposition at each step.`;
  }

  private categorizeConnectorRole(
    directConnections: number,
    reachability: number,
    influence: number
  ): string {
    if (directConnections > 50 && reachability > 70) {
      return 'Super Connector - Hub';
    } else if (influence > 0.7 && reachability > 60) {
      return 'Influential Bridge';
    } else if (directConnections > 30) {
      return 'Active Networker';
    } else if (reachability > 50) {
      return 'Network Bridge';
    } else {
      return 'Regular Connector';
    }
  }

  private async getUserName(userId: string): Promise<string> {
    const cacheKey = `user_name:${userId}`;
    const cached = await this.redis.get(cacheKey);

    if (cached) {
      return cached;
    }

    const client = await this.pool.connect();

    try {
      const result = await client.query('SELECT name FROM users WHERE id = $1', [userId]);
      const name = result.rows[0]?.name || 'Unknown';

      await this.redis.set(cacheKey, name, 'EX', 3600);

      return name;

    } finally {
      client.release();
    }
  }

  private async getSampleUsers(count: number): Promise<string[]> {
    const client = await this.pool.connect();

    try {
      const result = await client.query(`
        SELECT id FROM users
        ORDER BY RANDOM()
        LIMIT $1
      `, [count]);

      return result.rows.map(row => row.id);

    } finally {
      client.release();
    }
  }
}
