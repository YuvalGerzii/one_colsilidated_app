import { Pool } from 'pg';
import Redis from 'ioredis';

/**
 * Connection Strength Analyzer Agent
 *
 * Analyzes connection quality and network structure using multiple metrics:
 * - Tie Strength (strong vs weak ties)
 * - Centrality Measures (degree, betweenness, eigenvector, PageRank)
 * - Network Position Analysis
 * - Relationship Quality Scoring
 *
 * Based on social network analysis research:
 * - Degree Centrality: Number of direct connections
 * - Betweenness Centrality: Bridge nodes
 * - Eigenvector Centrality: Connected to well-connected nodes
 * - Tie strength: Time, emotional intensity, intimacy, reciprocity
 */

export interface TieStrength {
  userId1: string;
  userId2: string;
  strength: 'strong' | 'medium' | 'weak';
  score: number; // 0-1
  factors: {
    connectionStrength: number;
    trustLevel: number;
    mutuality: number; // Bidirectional connection
    frequency?: number; // Interaction frequency
  };
  type: 'strong_tie' | 'weak_tie';
  recommendation: string;
}

export interface CentralityMetrics {
  userId: string;
  userName: string;
  degreeCentrality: number; // Number of connections
  normalizedDegree: number; // 0-1 scale
  betweennessCentrality: number; // Bridge score
  eigenvectorCentrality: number; // Quality of connections
  pageRank: number; // Authority score
  closeness: number; // Average distance to others
  role: string; // Hub, Bridge, Peripheral, etc.
}

export interface NetworkPosition {
  userId: string;
  userName: string;
  position: 'core' | 'semi_peripheral' | 'peripheral' | 'isolated';
  coreDistance: number; // Steps to network core
  localClusterSize: number;
  bridgingPotential: number; // Ability to connect disparate groups
  structuralHoles: number; // Unique connections between groups
}

export interface RelationshipQuality {
  connectionId: string;
  userId1: string;
  userId2: string;
  quality: 'excellent' | 'good' | 'fair' | 'poor';
  overallScore: number;
  strengths: string[];
  weaknesses: string[];
  opportunities: string[];
  risk: 'low' | 'medium' | 'high';
}

export class ConnectionStrengthAnalyzer {
  constructor(
    private pool: Pool,
    private redis: Redis
  ) {}

  /**
   * Analyze tie strength between two users
   */
  async analyzeTieStrength(userId1: string, userId2: string): Promise<TieStrength | null> {
    const cacheKey = `tie_strength:${userId1}:${userId2}`;
    const cached = await this.redis.get(cacheKey);

    if (cached) {
      return JSON.parse(cached);
    }

    const client = await this.pool.connect();

    try {
      // Get connection in both directions
      const result = await client.query(`
        SELECT
          c1.connection_strength as strength1,
          c1.trust_level as trust1,
          c2.connection_strength as strength2,
          c2.trust_level as trust2
        FROM connections c1
        LEFT JOIN contacts ct1 ON c1.contact_id = ct1.id
        LEFT JOIN users u1 ON ct1.email = u1.email
        LEFT JOIN connections c2 ON u1.id = c2.user_id
        LEFT JOIN contacts ct2 ON c2.contact_id = ct2.id
        LEFT JOIN users u2 ON ct2.email = u2.email
        WHERE c1.user_id = $1 AND u1.id = $2
          AND (c2.id IS NULL OR u2.id = $1)
      `, [userId1, userId2]);

      if (result.rows.length === 0) {
        return null; // No connection found
      }

      const data = result.rows[0];
      const strength1 = parseFloat(data.strength1) || 0;
      const trust1 = parseFloat(data.trust1) || 0;
      const strength2 = parseFloat(data.strength2) || 0;
      const trust2 = parseFloat(data.trust2) || 0;

      // Calculate mutuality
      const mutuality = strength2 > 0 ? Math.min(strength1, strength2) / Math.max(strength1, strength2) : 0;

      // Calculate overall strength score
      const avgStrength = (strength1 + strength2) / (strength2 > 0 ? 2 : 1);
      const avgTrust = (trust1 + trust2) / (trust2 > 0 ? 2 : 1);

      const score = (
        avgStrength * 0.4 +
        avgTrust * 0.4 +
        mutuality * 0.2
      );

      // Categorize
      let strength: 'strong' | 'medium' | 'weak';
      let type: 'strong_tie' | 'weak_tie';
      let recommendation: string;

      if (score >= 0.7) {
        strength = 'strong';
        type = 'strong_tie';
        recommendation = 'Strong relationship. Ideal for close collaboration, introductions, and trust-based exchanges.';
      } else if (score >= 0.4) {
        strength = 'medium';
        type = score >= 0.5 ? 'strong_tie' : 'weak_tie';
        recommendation = 'Moderate relationship. Good for professional collaboration. Consider strengthening for deeper partnership.';
      } else {
        strength = 'weak';
        type = 'weak_tie';
        recommendation = 'Weak tie. Useful for novel information and bridging to new networks, but may require reinforcement for collaboration.';
      }

      const tieStrength: TieStrength = {
        userId1,
        userId2,
        strength,
        score,
        factors: {
          connectionStrength: avgStrength,
          trustLevel: avgTrust,
          mutuality
        },
        type,
        recommendation
      };

      // Cache for 30 minutes
      await this.redis.set(cacheKey, JSON.stringify(tieStrength), 'EX', 1800);

      return tieStrength;

    } finally {
      client.release();
    }
  }

  /**
   * Calculate centrality metrics for a user
   */
  async calculateCentrality(userId: string): Promise<CentralityMetrics> {
    const cacheKey = `centrality:${userId}`;
    const cached = await this.redis.get(cacheKey);

    if (cached) {
      return JSON.parse(cached);
    }

    const userName = await this.getUserName(userId);

    // Degree centrality
    const degreeCentrality = await this.calculateDegreeCentrality(userId);

    // Normalized degree
    const totalUsers = await this.getTotalUserCount();
    const normalizedDegree = totalUsers > 1 ? degreeCentrality / (totalUsers - 1) : 0;

    // Betweenness centrality (sample-based for performance)
    const betweennessCentrality = await this.calculateBetweennessCentrality(userId);

    // Eigenvector centrality (simplified)
    const eigenvectorCentrality = await this.calculateEigenvectorCentrality(userId);

    // PageRank (simplified)
    const pageRank = await this.calculatePageRank(userId);

    // Closeness centrality
    const closeness = await this.calculateClosenessCentrality(userId);

    // Determine role
    const role = this.determineNetworkRole({
      degreeCentrality,
      normalizedDegree,
      betweennessCentrality,
      eigenvectorCentrality
    });

    const metrics: CentralityMetrics = {
      userId,
      userName,
      degreeCentrality,
      normalizedDegree,
      betweennessCentrality,
      eigenvectorCentrality,
      pageRank,
      closeness,
      role
    };

    // Cache for 15 minutes
    await this.redis.set(cacheKey, JSON.stringify(metrics), 'EX', 900);

    return metrics;
  }

  /**
   * Analyze user's network position
   */
  async analyzeNetworkPosition(userId: string): Promise<NetworkPosition> {
    const cacheKey = `network_position:${userId}`;
    const cached = await this.redis.get(cacheKey);

    if (cached) {
      return JSON.parse(cached);
    }

    const userName = await this.getUserName(userId);

    // Get centrality metrics
    const centrality = await this.calculateCentrality(userId);

    // Determine position
    let position: 'core' | 'semi_peripheral' | 'peripheral' | 'isolated';
    if (centrality.degreeCentrality === 0) {
      position = 'isolated';
    } else if (centrality.normalizedDegree >= 0.3 && centrality.betweennessCentrality >= 0.2) {
      position = 'core';
    } else if (centrality.normalizedDegree >= 0.1 || centrality.betweennessCentrality >= 0.1) {
      position = 'semi_peripheral';
    } else {
      position = 'peripheral';
    }

    // Calculate local cluster size
    const localClusterSize = await this.calculateLocalClusterSize(userId);

    // Bridging potential (based on structural holes)
    const bridgingPotential = await this.calculateBridgingPotential(userId);

    // Structural holes
    const structuralHoles = await this.calculateStructuralHoles(userId);

    // Core distance
    const coreDistance = position === 'core' ? 0 :
                        position === 'semi_peripheral' ? 1 :
                        position === 'peripheral' ? 2 : 3;

    const networkPosition: NetworkPosition = {
      userId,
      userName,
      position,
      coreDistance,
      localClusterSize,
      bridgingPotential,
      structuralHoles
    };

    // Cache for 15 minutes
    await this.redis.set(cacheKey, JSON.stringify(networkPosition), 'EX', 900);

    return networkPosition;
  }

  /**
   * Evaluate relationship quality
   */
  async evaluateRelationshipQuality(
    userId1: string,
    userId2: string
  ): Promise<RelationshipQuality | null> {
    const tieStrength = await this.analyzeTieStrength(userId1, userId2);

    if (!tieStrength) {
      return null;
    }

    const strengths: string[] = [];
    const weaknesses: string[] = [];
    const opportunities: string[] = [];

    // Analyze strengths
    if (tieStrength.factors.connectionStrength >= 0.7) {
      strengths.push('Strong connection foundation');
    }
    if (tieStrength.factors.trustLevel >= 0.7) {
      strengths.push('High trust level');
    }
    if (tieStrength.factors.mutuality >= 0.7) {
      strengths.push('Mutual relationship (bidirectional)');
    }

    // Analyze weaknesses
    if (tieStrength.factors.connectionStrength < 0.4) {
      weaknesses.push('Low connection strength');
    }
    if (tieStrength.factors.trustLevel < 0.4) {
      weaknesses.push('Low trust level');
    }
    if (tieStrength.factors.mutuality < 0.3) {
      weaknesses.push('One-sided relationship');
    }

    // Identify opportunities
    if (tieStrength.factors.connectionStrength >= 0.5 && tieStrength.factors.trustLevel < 0.5) {
      opportunities.push('Build trust through consistent interactions');
    }
    if (tieStrength.factors.mutuality < 0.5) {
      opportunities.push('Establish reciprocal connection');
    }
    if (tieStrength.type === 'weak_tie') {
      opportunities.push('Leverage for novel information and network bridging');
    }

    // Determine quality category
    let quality: 'excellent' | 'good' | 'fair' | 'poor';
    if (tieStrength.score >= 0.8) quality = 'excellent';
    else if (tieStrength.score >= 0.6) quality = 'good';
    else if (tieStrength.score >= 0.4) quality = 'fair';
    else quality = 'poor';

    // Assess risk
    let risk: 'low' | 'medium' | 'high';
    if (tieStrength.factors.trustLevel >= 0.7 && tieStrength.factors.mutuality >= 0.6) {
      risk = 'low';
    } else if (tieStrength.factors.trustLevel >= 0.4) {
      risk = 'medium';
    } else {
      risk = 'high';
    }

    return {
      connectionId: `${userId1}-${userId2}`,
      userId1,
      userId2,
      quality,
      overallScore: tieStrength.score,
      strengths,
      weaknesses,
      opportunities,
      risk
    };
  }

  /**
   * Find weak ties (valuable for novel information)
   */
  async findWeakTies(userId: string, limit: number = 10): Promise<TieStrength[]> {
    const client = await this.pool.connect();

    try {
      const result = await client.query(`
        SELECT u.id
        FROM connections c
        JOIN contacts ct ON c.contact_id = ct.id
        JOIN users u ON ct.email = u.email
        WHERE c.user_id = $1
          AND c.connection_strength < 0.5
        ORDER BY c.connection_strength ASC
        LIMIT $2
      `, [userId, limit]);

      const weakTies = await Promise.all(
        result.rows.map(row =>
          this.analyzeTieStrength(userId, row.id)
        )
      );

      return weakTies.filter(t => t !== null) as TieStrength[];

    } finally {
      client.release();
    }
  }

  /**
   * Find strong ties (valuable for support and collaboration)
   */
  async findStrongTies(userId: string, limit: number = 10): Promise<TieStrength[]> {
    const client = await this.pool.connect();

    try {
      const result = await client.query(`
        SELECT u.id
        FROM connections c
        JOIN contacts ct ON c.contact_id = ct.id
        JOIN users u ON ct.email = u.email
        WHERE c.user_id = $1
          AND c.connection_strength >= 0.7
        ORDER BY c.connection_strength DESC
        LIMIT $2
      `, [userId, limit]);

      const strongTies = await Promise.all(
        result.rows.map(row =>
          this.analyzeTieStrength(userId, row.id)
        )
      );

      return strongTies.filter(t => t !== null) as TieStrength[];

    } finally {
      client.release();
    }
  }

  /**
   * Private helper methods
   */

  private async calculateDegreeCentrality(userId: string): Promise<number> {
    const client = await this.pool.connect();

    try {
      const result = await client.query(`
        SELECT COUNT(*) as count
        FROM connections
        WHERE user_id = $1
      `, [userId]);

      return parseInt(result.rows[0].count);

    } finally {
      client.release();
    }
  }

  private async calculateBetweennessCentrality(userId: string): Promise<number> {
    // Simplified betweenness: count of times user appears in shortest paths
    // Full calculation is computationally expensive, using approximation

    const client = await this.pool.connect();

    try {
      // Sample approach: check user's position relative to their neighbors
      const neighbors = await this.getDirectNeighbors(userId);

      if (neighbors.length < 2) {
        return 0; // Can't be a bridge with fewer than 2 neighbors
      }

      let bridgeCount = 0;
      const sampleSize = Math.min(neighbors.length, 10);

      // Check if this user bridges between their neighbors
      for (let i = 0; i < sampleSize - 1; i++) {
        for (let j = i + 1; j < sampleSize; j++) {
          // Check if neighbors are directly connected
          const directConnection = await client.query(`
            SELECT COUNT(*) as count
            FROM connections c
            JOIN contacts ct ON c.contact_id = ct.id
            JOIN users u ON ct.email = u.email
            WHERE c.user_id = $1 AND u.id = $2
          `, [neighbors[i], neighbors[j]]);

          if (parseInt(directConnection.rows[0].count) === 0) {
            bridgeCount++; // User bridges these two nodes
          }
        }
      }

      const maxBridges = (sampleSize * (sampleSize - 1)) / 2;
      return maxBridges > 0 ? bridgeCount / maxBridges : 0;

    } finally {
      client.release();
    }
  }

  private async calculateEigenvectorCentrality(userId: string): Promise<number> {
    // Simplified eigenvector: weighted sum of neighbors' degree centralities

    const neighbors = await this.getDirectNeighbors(userId);

    if (neighbors.length === 0) {
      return 0;
    }

    let weightedSum = 0;

    for (const neighborId of neighbors) {
      const neighborDegree = await this.calculateDegreeCentrality(neighborId);
      weightedSum += neighborDegree;
    }

    const totalUsers = await this.getTotalUserCount();
    const normalizedSum = totalUsers > 0 ? weightedSum / (totalUsers * neighbors.length) : 0;

    return Math.min(normalizedSum, 1);
  }

  private async calculatePageRank(userId: string): Promise<number> {
    // Simplified PageRank: based on quality and quantity of incoming connections

    const client = await this.pool.connect();

    try {
      const result = await client.query(`
        SELECT
          COUNT(*) as inbound_count,
          AVG(c.connection_strength) as avg_strength,
          AVG(c.trust_level) as avg_trust
        FROM users u
        JOIN contacts ct ON u.email = ct.email
        JOIN connections c ON ct.id = c.contact_id
        WHERE u.id = $1
      `, [userId]);

      const data = result.rows[0];
      const inboundCount = parseInt(data.inbound_count);
      const avgStrength = parseFloat(data.avg_strength) || 0;
      const avgTrust = parseFloat(data.avg_trust) || 0;

      const totalUsers = await this.getTotalUserCount();
      const normalizedCount = totalUsers > 1 ? inboundCount / (totalUsers - 1) : 0;

      return (normalizedCount * 0.5 + avgStrength * 0.25 + avgTrust * 0.25);

    } finally {
      client.release();
    }
  }

  private async calculateClosenessCentrality(userId: string): Promise<number> {
    // Average shortest path distance to all reachable nodes
    // Using sample for performance

    const sampleUsers = await this.getSampleUsers(30);
    let totalDistance = 0;
    let reachableCount = 0;

    for (const targetId of sampleUsers) {
      if (targetId === userId) continue;

      const distance = await this.getShortestPathLength(userId, targetId);
      if (distance < Infinity) {
        totalDistance += distance;
        reachableCount++;
      }
    }

    if (reachableCount === 0) {
      return 0;
    }

    const avgDistance = totalDistance / reachableCount;
    // Closeness is inverse of average distance
    return 1 / (avgDistance + 1);
  }

  private determineNetworkRole(metrics: {
    degreeCentrality: number;
    normalizedDegree: number;
    betweennessCentrality: number;
    eigenvectorCentrality: number;
  }): string {
    if (metrics.degreeCentrality >= 50 && metrics.eigenvectorCentrality >= 0.7) {
      return 'Super Hub - Highly connected to influential nodes';
    } else if (metrics.betweennessCentrality >= 0.5) {
      return 'Critical Bridge - Connects disparate network clusters';
    } else if (metrics.degreeCentrality >= 30) {
      return 'Hub - Many direct connections';
    } else if (metrics.betweennessCentrality >= 0.2) {
      return 'Bridge - Connects different groups';
    } else if (metrics.eigenvectorCentrality >= 0.6) {
      return 'Quality Connector - Connected to influential nodes';
    } else if (metrics.normalizedDegree >= 0.1) {
      return 'Active Member - Regular participation';
    } else if (metrics.degreeCentrality > 0) {
      return 'Peripheral - Few connections';
    } else {
      return 'Isolated - No connections';
    }
  }

  private async calculateLocalClusterSize(userId: string): Promise<number> {
    // Size of immediate network cluster (2-degree neighborhood)

    const firstDegree = await this.getDirectNeighbors(userId);
    const secondDegree = new Set<string>();

    for (const neighborId of firstDegree.slice(0, 20)) { // Limit for performance
      const neighborsOfNeighbor = await this.getDirectNeighbors(neighborId);
      neighborsOfNeighbor.forEach(id => {
        if (id !== userId && !firstDegree.includes(id)) {
          secondDegree.add(id);
        }
      });
    }

    return firstDegree.length + secondDegree.size;
  }

  private async calculateBridgingPotential(userId: string): Promise<number> {
    // Based on betweenness and local network structure

    const betweenness = await this.calculateBetweennessCentrality(userId);
    const structuralHoles = await this.calculateStructuralHoles(userId);

    return (betweenness * 0.6 + structuralHoles * 0.4);
  }

  private async calculateStructuralHoles(userId: string): Promise<number> {
    // Measure of non-redundant connections (connections that don't know each other)

    const neighbors = await this.getDirectNeighbors(userId);

    if (neighbors.length < 2) {
      return 0;
    }

    const sampleSize = Math.min(neighbors.length, 15);
    let nonRedundant = 0;

    for (let i = 0; i < sampleSize - 1; i++) {
      for (let j = i + 1; j < sampleSize; j++) {
        const connected = await this.areDirectlyConnected(neighbors[i], neighbors[j]);
        if (!connected) {
          nonRedundant++;
        }
      }
    }

    const maxPossible = (sampleSize * (sampleSize - 1)) / 2;
    return maxPossible > 0 ? nonRedundant / maxPossible : 0;
  }

  private async getDirectNeighbors(userId: string): Promise<string[]> {
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

  private async areDirectlyConnected(userId1: string, userId2: string): Promise<boolean> {
    const client = await this.pool.connect();

    try {
      const result = await client.query(`
        SELECT COUNT(*) as count
        FROM connections c
        JOIN contacts ct ON c.contact_id = ct.id
        JOIN users u ON ct.email = u.email
        WHERE c.user_id = $1 AND u.id = $2
      `, [userId1, userId2]);

      return parseInt(result.rows[0].count) > 0;

    } finally {
      client.release();
    }
  }

  private async getShortestPathLength(userId1: string, userId2: string): Promise<number> {
    // BFS to find shortest path length
    const queue: Array<{ userId: string; distance: number }> = [{ userId: userId1, distance: 0 }];
    const visited = new Set<string>([userId1]);

    while (queue.length > 0) {
      const { userId, distance } = queue.shift()!;

      if (userId === userId2) {
        return distance;
      }

      if (distance >= 6) continue; // Stop at 6 degrees

      const neighbors = await this.getDirectNeighbors(userId);

      for (const neighborId of neighbors) {
        if (!visited.has(neighborId)) {
          visited.add(neighborId);
          queue.push({ userId: neighborId, distance: distance + 1 });
        }
      }
    }

    return Infinity;
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

  private async getTotalUserCount(): Promise<number> {
    const cacheKey = 'total_user_count';
    const cached = await this.redis.get(cacheKey);

    if (cached) {
      return parseInt(cached);
    }

    const client = await this.pool.connect();

    try {
      const result = await client.query('SELECT COUNT(*) as count FROM users');
      const count = parseInt(result.rows[0].count);

      await this.redis.set(cacheKey, count.toString(), 'EX', 300);

      return count;

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
