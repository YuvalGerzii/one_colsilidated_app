import { Pool } from 'pg';
import Redis from 'ioredis';

/**
 * Trust Propagation Agent
 *
 * Calculates transitive trust through network paths:
 * - If A trusts B (0.9) and B trusts C (0.8), what's A's trust in C?
 * - Uses path-based trust propagation
 * - Applies trust decay over distance
 * - Identifies trust clusters
 * - Detects trust anomalies
 */

export interface TransitiveTrust {
  sourceId: string;
  targetId: string;
  directTrust: number | null; // Direct connection trust if exists
  indirectTrust: number; // Calculated through paths
  confidenceLevel: number; // How confident we are in this trust score
  trustPaths: Array<{
    path: string[];
    pathTrust: number;
    pathLength: number;
  }>;
  recommendation: 'highly_trustworthy' | 'trustworthy' | 'neutral' | 'cautious' | 'unknown';
}

export interface TrustCluster {
  clusterId: string;
  members: string[];
  averageTrust: number;
  cohesion: number; // How tightly connected
  size: number;
}

export class TrustPropagationAgent {
  // Trust decay factor per hop
  private readonly DECAY_FACTOR = 0.85;
  private readonly MAX_PATH_LENGTH = 4;
  private readonly MIN_TRUST_THRESHOLD = 0.3;

  constructor(
    private pool: Pool,
    private redis: Redis
  ) {}

  /**
   * Calculate transitive trust between two users
   * Uses multiple paths and averages with decay
   */
  async calculateTransitiveTrust(
    sourceId: string,
    targetId: string
  ): Promise<TransitiveTrust> {
    const cacheKey = `trust:${sourceId}:${targetId}`;
    const cached = await this.redis.get(cacheKey);

    if (cached) {
      return JSON.parse(cached);
    }

    // Check for direct trust
    const directTrust = await this.getDirectTrust(sourceId, targetId);

    // Find all trust paths
    const trustPaths = await this.findTrustPaths(
      sourceId,
      targetId,
      this.MAX_PATH_LENGTH
    );

    if (trustPaths.length === 0 && directTrust === null) {
      return {
        sourceId,
        targetId,
        directTrust: null,
        indirectTrust: 0,
        confidenceLevel: 0,
        trustPaths: [],
        recommendation: 'unknown'
      };
    }

    // Calculate indirect trust from paths
    let totalTrust = 0;
    let totalWeight = 0;

    for (const path of trustPaths) {
      const weight = Math.pow(this.DECAY_FACTOR, path.pathLength - 1);
      totalTrust += path.pathTrust * weight;
      totalWeight += weight;
    }

    const indirectTrust = totalWeight > 0 ? totalTrust / totalWeight : 0;

    // Combine direct and indirect if both exist
    const finalTrust = directTrust !== null ?
      (directTrust * 0.7 + indirectTrust * 0.3) :
      indirectTrust;

    // Confidence based on number and quality of paths
    const confidenceLevel = this.calculateConfidence(trustPaths, directTrust !== null);

    // Generate recommendation
    const recommendation = this.getTrustRecommendation(finalTrust, confidenceLevel);

    const result = {
      sourceId,
      targetId,
      directTrust,
      indirectTrust,
      confidenceLevel,
      trustPaths: trustPaths.slice(0, 5), // Top 5 paths
      recommendation
    };

    // Cache for 30 minutes
    await this.redis.set(cacheKey, JSON.stringify(result), 'EX', 1800);

    return result;
  }

  /**
   * Find trust paths between two users using modified BFS
   */
  private async findTrustPaths(
    sourceId: string,
    targetId: string,
    maxLength: number
  ): Promise<Array<{
    path: string[];
    pathTrust: number;
    pathLength: number;
  }>> {
    const paths: Array<{
      path: string[];
      pathTrust: number;
      pathLength: number;
    }> = [];

    const queue: Array<{
      currentId: string;
      path: string[];
      trustAccumulated: number;
      visited: Set<string>;
    }> = [{
      currentId: sourceId,
      path: [sourceId],
      trustAccumulated: 1.0,
      visited: new Set([sourceId])
    }];

    while (queue.length > 0) {
      const { currentId, path, trustAccumulated, visited } = queue.shift()!;

      if (path.length > maxLength) continue;

      // Found target
      if (currentId === targetId && path.length > 1) {
        paths.push({
          path: [...path],
          pathTrust: trustAccumulated,
          pathLength: path.length
        });
        continue;
      }

      // Get neighbors with trust levels
      const neighbors = await this.getTrustedNeighbors(currentId);

      for (const { userId, trustLevel } of neighbors) {
        if (!visited.has(userId)) {
          const newVisited = new Set(visited);
          newVisited.add(userId);

          // Propagate trust with decay
          const newTrust = trustAccumulated * trustLevel;

          if (newTrust >= this.MIN_TRUST_THRESHOLD) {
            queue.push({
              currentId: userId,
              path: [...path, userId],
              trustAccumulated: newTrust,
              visited: newVisited
            });
          }
        }
      }
    }

    // Sort by trust level
    return paths.sort((a, b) => b.pathTrust - a.pathTrust);
  }

  /**
   * Calculate trust clusters using trust-based community detection
   */
  async findTrustClusters(
    minClusterSize: number = 3,
    minAverageTrust: number = 0.7
  ): Promise<TrustCluster[]> {
    const cacheKey = `trust_clusters:${minClusterSize}:${minAverageTrust}`;
    const cached = await this.redis.get(cacheKey);

    if (cached) {
      return JSON.parse(cached);
    }

    // Get all users
    const allUsers = await this.getAllUsers();

    // Build trust graph
    const trustGraph = await this.buildTrustGraph(allUsers);

    // Find clusters using trust-weighted modularity
    const clusters = this.detectTrustClusters(trustGraph, minAverageTrust);

    // Filter by size and trust level
    const filteredClusters = clusters
      .filter(c => c.size >= minClusterSize && c.averageTrust >= minAverageTrust)
      .map((c, i) => ({
        ...c,
        clusterId: `cluster_${i + 1}`
      }));

    // Cache for 20 minutes
    await this.redis.set(cacheKey, JSON.stringify(filteredClusters), 'EX', 1200);

    return filteredClusters;
  }

  /**
   * Identify trust anomalies (unusually high/low trust patterns)
   */
  async detectTrustAnomalies(userId: string): Promise<Array<{
    type: 'high_trust_low_reciprocity' | 'trust_mismatch' | 'isolated_high_trust' | 'trust_outlier';
    description: string;
    targetId?: string;
    severity: 'low' | 'medium' | 'high';
  }>> {
    const anomalies: Array<{
      type: any;
      description: string;
      targetId?: string;
      severity: 'low' | 'medium' | 'high';
    }> = [];

    const connections = await this.getUserConnections(userId);

    for (const conn of connections) {
      // Check reciprocity
      const forwardTrust = conn.trustLevel;
      const reverseTrust = await this.getDirectTrust(conn.userId, userId);

      if (reverseTrust !== null) {
        const trustDiff = Math.abs(forwardTrust - reverseTrust);

        if (forwardTrust > 0.8 && reverseTrust < 0.4) {
          anomalies.push({
            type: 'high_trust_low_reciprocity',
            description: `High trust (${forwardTrust.toFixed(2)}) not reciprocated by ${conn.userName}`,
            targetId: conn.userId,
            severity: 'medium'
          });
        } else if (trustDiff > 0.5) {
          anomalies.push({
            type: 'trust_mismatch',
            description: `Significant trust mismatch with ${conn.userName} (difference: ${trustDiff.toFixed(2)})`,
            targetId: conn.userId,
            severity: 'low'
          });
        }
      }

      // Check for outliers
      const avgTrust = connections.reduce((sum, c) => sum + c.trustLevel, 0) / connections.length;
      if (Math.abs(conn.trustLevel - avgTrust) > 0.3) {
        anomalies.push({
          type: 'trust_outlier',
          description: `${conn.userName} has unusually ${conn.trustLevel > avgTrust ? 'high' : 'low'} trust compared to network average`,
          targetId: conn.userId,
          severity: 'low'
        });
      }
    }

    return anomalies;
  }

  /**
   * Recommend trust-building actions
   */
  async recommendTrustActions(
    userId: string,
    targetId: string
  ): Promise<Array<{
    action: string;
    impact: number;
    effort: 'low' | 'medium' | 'high';
    timeframe: string;
  }>> {
    const currentTrust = await this.calculateTransitiveTrust(userId, targetId);
    const recommendations: Array<{
      action: string;
      impact: number;
      effort: 'low' | 'medium' | 'high';
      timeframe: string;
    }> = [];

    if (currentTrust.directTrust === null) {
      // No direct connection
      if (currentTrust.trustPaths.length > 0) {
        const bestPath = currentTrust.trustPaths[0];
        const introducer = bestPath.path[1]; // First intermediary
        const introducerName = await this.getUserName(introducer);

        recommendations.push({
          action: `Request introduction from ${introducerName}`,
          impact: 0.4,
          effort: 'low',
          timeframe: '1-2 weeks'
        });
      }

      recommendations.push({
        action: 'Engage on shared content/interests',
        impact: 0.3,
        effort: 'low',
        timeframe: '2-4 weeks'
      });

      recommendations.push({
        action: 'Attend same events/conferences',
        impact: 0.5,
        effort: 'medium',
        timeframe: '1-3 months'
      });
    } else {
      // Have direct connection, build trust
      if (currentTrust.directTrust < 0.5) {
        recommendations.push({
          action: 'Regular check-ins and communication',
          impact: 0.3,
          effort: 'low',
          timeframe: 'Ongoing'
        });

        recommendations.push({
          action: 'Deliver on commitments consistently',
          impact: 0.6,
          effort: 'high',
          timeframe: '3-6 months'
        });

        recommendations.push({
          action: 'Share valuable resources/introductions',
          impact: 0.4,
          effort: 'medium',
          timeframe: '1-2 months'
        });
      }
    }

    return recommendations.sort((a, b) => b.impact - a.impact);
  }

  /**
   * Helper methods
   */

  private async getDirectTrust(userId1: string, userId2: string): Promise<number | null> {
    const client = await this.pool.connect();

    try {
      const result = await client.query(`
        SELECT c.trust_level
        FROM connections c
        JOIN contacts ct ON c.contact_id = ct.id
        JOIN users u ON ct.email = u.email
        WHERE c.user_id = $1 AND u.id = $2
      `, [userId1, userId2]);

      if (result.rows.length === 0) return null;

      return parseFloat(result.rows[0].trust_level);

    } finally {
      client.release();
    }
  }

  private async getTrustedNeighbors(userId: string): Promise<Array<{
    userId: string;
    trustLevel: number;
  }>> {
    const client = await this.pool.connect();

    try {
      const result = await client.query(`
        SELECT u.id, c.trust_level
        FROM connections c
        JOIN contacts ct ON c.contact_id = ct.id
        JOIN users u ON ct.email = u.email
        WHERE c.user_id = $1 AND c.trust_level >= $2
      `, [userId, this.MIN_TRUST_THRESHOLD]);

      return result.rows.map(row => ({
        userId: row.id,
        trustLevel: parseFloat(row.trust_level)
      }));

    } finally {
      client.release();
    }
  }

  private calculateConfidence(
    paths: any[],
    hasDirect: boolean
  ): number {
    if (hasDirect && paths.length > 0) return 0.9;
    if (hasDirect) return 0.8;
    if (paths.length >= 3) return 0.7;
    if (paths.length >= 2) return 0.6;
    if (paths.length >= 1) return 0.5;
    return 0.3;
  }

  private getTrustRecommendation(
    trust: number,
    confidence: number
  ): 'highly_trustworthy' | 'trustworthy' | 'neutral' | 'cautious' | 'unknown' {
    const effectiveTrust = trust * confidence;

    if (effectiveTrust >= 0.7) return 'highly_trustworthy';
    if (effectiveTrust >= 0.5) return 'trustworthy';
    if (effectiveTrust >= 0.3) return 'neutral';
    if (effectiveTrust > 0) return 'cautious';
    return 'unknown';
  }

  private async buildTrustGraph(users: string[]): Promise<Map<string, Map<string, number>>> {
    const graph = new Map<string, Map<string, number>>();

    for (const userId of users) {
      const neighbors = await this.getTrustedNeighbors(userId);
      const edges = new Map<string, number>();

      for (const { userId: neighborId, trustLevel } of neighbors) {
        edges.set(neighborId, trustLevel);
      }

      graph.set(userId, edges);
    }

    return graph;
  }

  private detectTrustClusters(
    trustGraph: Map<string, Map<string, number>>,
    minTrust: number
  ): TrustCluster[] {
    // Simple clustering based on trust levels
    // In production, use more sophisticated algorithms like Louvain

    const clusters: TrustCluster[] = [];
    const assigned = new Set<string>();

    for (const [userId, neighbors] of trustGraph) {
      if (assigned.has(userId)) continue;

      // Start new cluster
      const cluster = new Set<string>([userId]);
      assigned.add(userId);

      // Add high-trust neighbors
      for (const [neighborId, trust] of neighbors) {
        if (trust >= minTrust && !assigned.has(neighborId)) {
          cluster.add(neighborId);
          assigned.add(neighborId);
        }
      }

      if (cluster.size >= 2) {
        // Calculate cluster metrics
        const members = Array.from(cluster);
        let totalTrust = 0;
        let edgeCount = 0;

        for (const member of members) {
          const memberNeighbors = trustGraph.get(member) || new Map();
          for (const other of members) {
            if (member !== other && memberNeighbors.has(other)) {
              totalTrust += memberNeighbors.get(other)!;
              edgeCount++;
            }
          }
        }

        const averageTrust = edgeCount > 0 ? totalTrust / edgeCount : 0;
        const maxEdges = members.length * (members.length - 1);
        const cohesion = maxEdges > 0 ? edgeCount / maxEdges : 0;

        clusters.push({
          clusterId: '',
          members,
          averageTrust,
          cohesion,
          size: members.length
        });
      }
    }

    return clusters;
  }

  private async getUserConnections(userId: string): Promise<Array<{
    userId: string;
    userName: string;
    trustLevel: number;
  }>> {
    const client = await this.pool.connect();

    try {
      const result = await client.query(`
        SELECT u.id, u.name, c.trust_level
        FROM connections c
        JOIN contacts ct ON c.contact_id = ct.id
        JOIN users u ON ct.email = u.email
        WHERE c.user_id = $1
      `, [userId]);

      return result.rows.map(row => ({
        userId: row.id,
        userName: row.name,
        trustLevel: parseFloat(row.trust_level)
      }));

    } finally {
      client.release();
    }
  }

  private async getAllUsers(): Promise<string[]> {
    const client = await this.pool.connect();

    try {
      const result = await client.query('SELECT id FROM users LIMIT 200');
      return result.rows.map(row => row.id);

    } finally {
      client.release();
    }
  }

  private async getUserName(userId: string): Promise<string> {
    const client = await this.pool.connect();

    try {
      const result = await client.query('SELECT name FROM users WHERE id = $1', [userId]);
      return result.rows[0]?.name || 'Unknown';

    } finally {
      client.release();
    }
  }
}
