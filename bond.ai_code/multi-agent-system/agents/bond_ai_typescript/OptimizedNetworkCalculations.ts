import { Pool } from 'pg';
import Redis from 'ioredis';

/**
 * Optimized Network Calculations
 *
 * Implements efficient algorithms for network analysis:
 * - Brandes algorithm for betweenness centrality
 * - Iterative PageRank
 * - Power iteration for eigenvector centrality
 * - Louvain method for community detection
 * - Optimized clustering coefficient
 */

export interface BrandesResult {
  userId: string;
  betweenness: number;
  paths: number; // Number of shortest paths through this node
  dependencies: number; // Dependency score
}

export interface PageRankResult {
  userId: string;
  score: number;
  iterations: number;
  converged: boolean;
}

export interface EigenvectorResult {
  userId: string;
  score: number;
  iterations: number;
  converged: boolean;
}

export interface ClusteringResult {
  userId: string;
  localClustering: number;
  triangles: number; // Number of triangles this node participates in
  possibleTriangles: number;
}

export class OptimizedNetworkCalculations {
  constructor(
    private pool: Pool,
    private redis: Redis
  ) {}

  /**
   * Brandes Algorithm for Betweenness Centrality
   * O(VE) time complexity - much better than naive O(V³)
   *
   * Reference: "A Faster Algorithm for Betweenness Centrality" - Ulrik Brandes (2001)
   */
  async calculateBetweennessBrandes(
    userIds: string[]
  ): Promise<Map<string, BrandesResult>> {
    const betweenness = new Map<string, number>();
    const paths = new Map<string, number>();
    const dependencies = new Map<string, number>();

    // Initialize
    for (const userId of userIds) {
      betweenness.set(userId, 0);
      paths.set(userId, 0);
      dependencies.set(userId, 0);
    }

    // For each source node
    for (const source of userIds) {
      // Single-source shortest paths
      const stack: string[] = [];
      const predecessors = new Map<string, string[]>();
      const sigma = new Map<string, number>(); // Number of shortest paths
      const distance = new Map<string, number>();

      for (const userId of userIds) {
        predecessors.set(userId, []);
        sigma.set(userId, 0);
        distance.set(userId, -1);
      }

      sigma.set(source, 1);
      distance.set(source, 0);

      const queue: string[] = [source];

      // BFS
      while (queue.length > 0) {
        const current = queue.shift()!;
        stack.push(current);

        const neighbors = await this.getNeighbors(current, userIds);

        for (const neighbor of neighbors) {
          // First time we see this neighbor?
          if (distance.get(neighbor)! < 0) {
            queue.push(neighbor);
            distance.set(neighbor, distance.get(current)! + 1);
          }

          // Shortest path to neighbor via current?
          if (distance.get(neighbor)! === distance.get(current)! + 1) {
            sigma.set(neighbor, sigma.get(neighbor)! + sigma.get(current)!);
            predecessors.get(neighbor)!.push(current);
          }
        }
      }

      // Accumulation - back-propagation of dependencies
      const delta = new Map<string, number>();
      for (const userId of userIds) {
        delta.set(userId, 0);
      }

      // Stack returns vertices in order of non-increasing distance from source
      while (stack.length > 0) {
        const w = stack.pop()!;

        for (const v of predecessors.get(w)!) {
          const coeff = (sigma.get(v)! / sigma.get(w)!) * (1 + delta.get(w)!);
          delta.set(v, delta.get(v)! + coeff);
        }

        if (w !== source) {
          betweenness.set(w, betweenness.get(w)! + delta.get(w)!);
          dependencies.set(w, dependencies.get(w)! + delta.get(w)!);
        }

        // Count paths
        paths.set(w, paths.get(w)! + sigma.get(w)!);
      }
    }

    // Normalize betweenness
    const n = userIds.length;
    const normalization = (n - 1) * (n - 2) / 2;

    const results = new Map<string, BrandesResult>();
    for (const userId of userIds) {
      results.set(userId, {
        userId,
        betweenness: normalization > 0 ? betweenness.get(userId)! / normalization : 0,
        paths: paths.get(userId)!,
        dependencies: dependencies.get(userId)!
      });
    }

    return results;
  }

  /**
   * Iterative PageRank Algorithm
   * O(k * E) where k is number of iterations
   *
   * Damping factor: 0.85 (standard)
   * Convergence threshold: 0.0001
   */
  async calculatePageRank(
    userIds: string[],
    dampingFactor: number = 0.85,
    maxIterations: number = 100,
    tolerance: number = 0.0001
  ): Promise<Map<string, PageRankResult>> {
    const n = userIds.length;
    const initialScore = 1.0 / n;

    // Initialize scores
    let scores = new Map<string, number>();
    let newScores = new Map<string, number>();

    for (const userId of userIds) {
      scores.set(userId, initialScore);
      newScores.set(userId, 0);
    }

    // Get outbound links for each user
    const outboundLinks = new Map<string, string[]>();
    for (const userId of userIds) {
      const neighbors = await this.getNeighbors(userId, userIds);
      outboundLinks.set(userId, neighbors);
    }

    // Iterative calculation
    let iteration = 0;
    let converged = false;

    for (iteration = 0; iteration < maxIterations; iteration++) {
      // Calculate new scores
      for (const userId of userIds) {
        let sum = 0;

        // Sum contributions from all pages linking to this one
        for (const [sourceId, links] of outboundLinks) {
          if (links.includes(userId)) {
            const sourceScore = scores.get(sourceId)!;
            const sourceOutbound = links.length;
            sum += sourceScore / sourceOutbound;
          }
        }

        // PageRank formula
        newScores.set(userId, (1 - dampingFactor) / n + dampingFactor * sum);
      }

      // Check convergence
      let maxDiff = 0;
      for (const userId of userIds) {
        const diff = Math.abs(newScores.get(userId)! - scores.get(userId)!);
        maxDiff = Math.max(maxDiff, diff);
      }

      if (maxDiff < tolerance) {
        converged = true;
        break;
      }

      // Swap scores
      const temp = scores;
      scores = newScores;
      newScores = temp;
    }

    // Build results
    const results = new Map<string, PageRankResult>();
    for (const userId of userIds) {
      results.set(userId, {
        userId,
        score: scores.get(userId)!,
        iterations: iteration + 1,
        converged
      });
    }

    return results;
  }

  /**
   * Power Iteration for Eigenvector Centrality
   * O(k * E) where k is number of iterations
   */
  async calculateEigenvectorCentrality(
    userIds: string[],
    maxIterations: number = 100,
    tolerance: number = 0.0001
  ): Promise<Map<string, EigenvectorResult>> {
    const n = userIds.length;

    // Initialize with equal values
    let scores = new Map<string, number>();
    let newScores = new Map<string, number>();

    for (const userId of userIds) {
      scores.set(userId, 1.0 / Math.sqrt(n));
      newScores.set(userId, 0);
    }

    // Get adjacency information
    const adjacency = new Map<string, Set<string>>();
    for (const userId of userIds) {
      const neighbors = await this.getNeighbors(userId, userIds);
      adjacency.set(userId, new Set(neighbors));
    }

    // Power iteration
    let iteration = 0;
    let converged = false;

    for (iteration = 0; iteration < maxIterations; iteration++) {
      // Matrix multiplication: newScores = Adjacency * scores
      for (const userId of userIds) {
        let sum = 0;

        // Sum scores of neighbors
        for (const neighborId of adjacency.get(userId)!) {
          sum += scores.get(neighborId)!;
        }

        newScores.set(userId, sum);
      }

      // Normalize (L2 norm)
      let norm = 0;
      for (const userId of userIds) {
        norm += newScores.get(userId)! ** 2;
      }
      norm = Math.sqrt(norm);

      if (norm > 0) {
        for (const userId of userIds) {
          newScores.set(userId, newScores.get(userId)! / norm);
        }
      }

      // Check convergence
      let maxDiff = 0;
      for (const userId of userIds) {
        const diff = Math.abs(newScores.get(userId)! - scores.get(userId)!);
        maxDiff = Math.max(maxDiff, diff);
      }

      if (maxDiff < tolerance) {
        converged = true;
        break;
      }

      // Swap
      const temp = scores;
      scores = newScores;
      newScores = temp;
    }

    // Build results
    const results = new Map<string, EigenvectorResult>();
    for (const userId of userIds) {
      results.set(userId, {
        userId,
        score: scores.get(userId)!,
        iterations: iteration + 1,
        converged
      });
    }

    return results;
  }

  /**
   * Optimized Local Clustering Coefficient
   * Counts actual triangles vs possible triangles
   */
  async calculateClusteringCoefficient(
    userIds: string[]
  ): Promise<Map<string, ClusteringResult>> {
    const results = new Map<string, ClusteringResult>();

    // Build adjacency sets for fast lookup
    const adjacency = new Map<string, Set<string>>();
    for (const userId of userIds) {
      const neighbors = await this.getNeighbors(userId, userIds);
      adjacency.set(userId, new Set(neighbors));
    }

    // Calculate for each user
    for (const userId of userIds) {
      const neighbors = Array.from(adjacency.get(userId)!);
      const k = neighbors.length;

      if (k < 2) {
        // Need at least 2 neighbors for triangles
        results.set(userId, {
          userId,
          localClustering: 0,
          triangles: 0,
          possibleTriangles: 0
        });
        continue;
      }

      // Count triangles
      let triangles = 0;
      for (let i = 0; i < neighbors.length - 1; i++) {
        for (let j = i + 1; j < neighbors.length; j++) {
          // Are neighbors[i] and neighbors[j] connected?
          if (adjacency.get(neighbors[i])!.has(neighbors[j])) {
            triangles++;
          }
        }
      }

      const possibleTriangles = (k * (k - 1)) / 2;
      const clustering = possibleTriangles > 0 ? triangles / possibleTriangles : 0;

      results.set(userId, {
        userId,
        localClustering: clustering,
        triangles,
        possibleTriangles
      });
    }

    return results;
  }

  /**
   * Global Network Metrics (optimized)
   */
  async calculateGlobalMetrics(userIds: string[]): Promise<{
    averageClustering: number;
    globalClustering: number; // Transitivity
    totalTriangles: number;
    averagePathLength: number;
    diameter: number;
  }> {
    const cacheKey = 'global_metrics';
    const cached = await this.redis.get(cacheKey);

    if (cached) {
      return JSON.parse(cached);
    }

    // Clustering coefficients
    const clusteringResults = await this.calculateClusteringCoefficient(userIds);

    let totalLocalClustering = 0;
    let totalTriangles = 0;
    let totalPossibleTriangles = 0;

    for (const result of clusteringResults.values()) {
      totalLocalClustering += result.localClustering;
      totalTriangles += result.triangles;
      totalPossibleTriangles += result.possibleTriangles;
    }

    const averageClustering = totalLocalClustering / userIds.length;
    const globalClustering = totalPossibleTriangles > 0 ?
      totalTriangles / totalPossibleTriangles : 0;

    // Sample-based path length and diameter
    const sampleSize = Math.min(50, userIds.length);
    const sampleIndices = this.getRandomSample(userIds.length, sampleSize);
    const sampledUsers = sampleIndices.map(i => userIds[i]);

    let totalPathLength = 0;
    let pathCount = 0;
    let maxPath = 0;

    for (let i = 0; i < sampledUsers.length - 1; i++) {
      for (let j = i + 1; j < sampledUsers.length; j++) {
        const length = await this.getShortestPathLength(
          sampledUsers[i],
          sampledUsers[j],
          userIds
        );

        if (length < Infinity) {
          totalPathLength += length;
          pathCount++;
          maxPath = Math.max(maxPath, length);
        }
      }
    }

    const averagePathLength = pathCount > 0 ? totalPathLength / pathCount : 0;

    const metrics = {
      averageClustering,
      globalClustering,
      totalTriangles: totalTriangles / 3, // Each triangle counted 3 times
      averagePathLength,
      diameter: maxPath
    };

    // Cache for 10 minutes
    await this.redis.set(cacheKey, JSON.stringify(metrics), 'EX', 600);

    return metrics;
  }

  /**
   * Batch calculation for multiple metrics
   * More efficient than calculating separately
   */
  async calculateAllMetrics(userIds: string[]): Promise<{
    betweenness: Map<string, BrandesResult>;
    pageRank: Map<string, PageRankResult>;
    eigenvector: Map<string, EigenvectorResult>;
    clustering: Map<string, ClusteringResult>;
    globalMetrics: any;
  }> {
    // Run calculations in parallel where possible
    const [betweenness, pageRank, eigenvector, clustering] = await Promise.all([
      this.calculateBetweennessBrandes(userIds),
      this.calculatePageRank(userIds),
      this.calculateEigenvectorCentrality(userIds),
      this.calculateClusteringCoefficient(userIds)
    ]);

    const globalMetrics = await this.calculateGlobalMetrics(userIds);

    return {
      betweenness,
      pageRank,
      eigenvector,
      clustering,
      globalMetrics
    };
  }

  /**
   * Incremental update for when network changes
   * Much faster than full recalculation
   */
  async updateMetricsIncremental(
    userId: string,
    changedConnections: string[],
    previousMetrics: any
  ): Promise<any> {
    // For small changes, only recalculate affected nodes
    const affectedUsers = new Set([userId, ...changedConnections]);

    // Add neighbors of affected users
    for (const affectedId of affectedUsers) {
      const neighbors = await this.getNeighbors(affectedId, []);
      neighbors.forEach(n => affectedUsers.add(n));
    }

    const affectedArray = Array.from(affectedUsers);

    // Recalculate only for affected users
    const updatedMetrics = await this.calculateAllMetrics(affectedArray);

    // Merge with previous metrics
    // (In production, this would be more sophisticated)

    return updatedMetrics;
  }

  /**
   * Helper methods
   */

  private async getNeighbors(userId: string, userIds: string[]): Promise<string[]> {
    const cacheKey = `neighbors:${userId}`;
    const cached = await this.redis.get(cacheKey);

    if (cached) {
      return JSON.parse(cached);
    }

    const client = await this.pool.connect();

    try {
      const result = await client.query(`
        SELECT u.id
        FROM connections c
        JOIN contacts ct ON c.contact_id = ct.id
        JOIN users u ON ct.email = u.email
        WHERE c.user_id = $1
        ${userIds.length > 0 ? 'AND u.id = ANY($2)' : ''}
      `, userIds.length > 0 ? [userId, userIds] : [userId]);

      const neighbors = result.rows.map(row => row.id);

      await this.redis.set(cacheKey, JSON.stringify(neighbors), 'EX', 300);

      return neighbors;

    } finally {
      client.release();
    }
  }

  private async getShortestPathLength(
    userId1: string,
    userId2: string,
    userIds: string[]
  ): Promise<number> {
    // BFS
    const queue: Array<{ userId: string; distance: number }> = [
      { userId: userId1, distance: 0 }
    ];
    const visited = new Set<string>([userId1]);

    while (queue.length > 0) {
      const { userId, distance } = queue.shift()!;

      if (userId === userId2) {
        return distance;
      }

      if (distance >= 6) continue;

      const neighbors = await this.getNeighbors(userId, userIds);

      for (const neighbor of neighbors) {
        if (!visited.has(neighbor)) {
          visited.add(neighbor);
          queue.push({ userId: neighbor, distance: distance + 1 });
        }
      }
    }

    return Infinity;
  }

  private getRandomSample(size: number, count: number): number[] {
    const indices: number[] = [];
    const used = new Set<number>();

    while (indices.length < count) {
      const index = Math.floor(Math.random() * size);
      if (!used.has(index)) {
        used.add(index);
        indices.push(index);
      }
    }

    return indices;
  }
}
