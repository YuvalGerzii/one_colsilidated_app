import { Pool } from 'pg';
import Redis from 'ioredis';

/**
 * Network Traversal Agent
 *
 * Implements advanced graph traversal algorithms for:
 * - Shortest path discovery (BFS)
 * - All paths within N degrees
 * - Path quality scoring
 * - Route optimization
 *
 * Based on research:
 * - Breadth-First Search for unweighted shortest paths
 * - Maintains "previous" node tracking for path reconstruction
 * - Optimized for social network graphs
 */

export interface PathNode {
  userId: string;
  name: string;
  connectionStrength?: number;
  trustLevel?: number;
  degreeOfSeparation: number;
}

export interface ConnectionPath {
  path: PathNode[];
  length: number;
  totalStrength: number;
  averageTrust: number;
  weakestLink: number;
  quality: number; // Overall path quality score
}

export interface NetworkStatistics {
  totalUsers: number;
  totalConnections: number;
  averageDegree: number;
  clusteringCoefficient: number;
  diameter: number; // Maximum shortest path length
  isolatedUsers: number;
}

export class NetworkTraversalAgent {
  constructor(
    private pool: Pool,
    private redis: Redis
  ) {}

  /**
   * Find shortest path between two users using BFS
   * Returns null if no path exists
   */
  async findShortestPath(
    sourceUserId: string,
    targetUserId: string
  ): Promise<ConnectionPath | null> {
    const cacheKey = `shortest_path:${sourceUserId}:${targetUserId}`;

    // Check cache
    const cached = await this.redis.get(cacheKey);
    if (cached) {
      return JSON.parse(cached);
    }

    // BFS implementation
    const queue: string[] = [sourceUserId];
    const visited = new Set<string>([sourceUserId]);
    const previous = new Map<string, { userId: string; strength: number; trust: number }>();

    while (queue.length > 0) {
      const currentUserId = queue.shift()!;

      // Found target
      if (currentUserId === targetUserId) {
        const path = await this.reconstructPath(sourceUserId, targetUserId, previous);

        // Cache result for 1 hour
        await this.redis.set(cacheKey, JSON.stringify(path), 'EX', 3600);

        return path;
      }

      // Get all connections for current user
      const connections = await this.getDirectConnections(currentUserId);

      for (const connection of connections) {
        if (!visited.has(connection.userId)) {
          visited.add(connection.userId);
          queue.push(connection.userId);
          previous.set(connection.userId, {
            userId: currentUserId,
            strength: connection.connectionStrength,
            trust: connection.trustLevel
          });
        }
      }
    }

    // No path found
    return null;
  }

  /**
   * Find all paths within N degrees of separation
   */
  async findAllPathsWithinDegrees(
    userId: string,
    maxDegrees: number = 6
  ): Promise<Map<string, ConnectionPath>> {
    const paths = new Map<string, ConnectionPath>();
    const queue: Array<{ userId: string; depth: number; path: PathNode[] }> = [
      {
        userId,
        depth: 0,
        path: [{
          userId,
          name: await this.getUserName(userId),
          degreeOfSeparation: 0
        }]
      }
    ];
    const visited = new Set<string>([userId]);

    while (queue.length > 0) {
      const current = queue.shift()!;

      // Skip if beyond max degrees
      if (current.depth >= maxDegrees) {
        continue;
      }

      // Get connections
      const connections = await this.getDirectConnections(current.userId);

      for (const connection of connections) {
        if (!visited.has(connection.userId)) {
          visited.add(connection.userId);

          const newPath: PathNode[] = [
            ...current.path,
            {
              userId: connection.userId,
              name: connection.name,
              connectionStrength: connection.connectionStrength,
              trustLevel: connection.trustLevel,
              degreeOfSeparation: current.depth + 1
            }
          ];

          // Calculate path metrics
          const pathMetrics = this.calculatePathMetrics(newPath);

          paths.set(connection.userId, {
            path: newPath,
            length: newPath.length - 1,
            ...pathMetrics
          });

          // Continue BFS
          queue.push({
            userId: connection.userId,
            depth: current.depth + 1,
            path: newPath
          });
        }
      }
    }

    return paths;
  }

  /**
   * Find multiple paths between two users (alternative routes)
   */
  async findAlternativePaths(
    sourceUserId: string,
    targetUserId: string,
    maxPaths: number = 5,
    maxLength: number = 6
  ): Promise<ConnectionPath[]> {
    const paths: ConnectionPath[] = [];
    const explored = new Set<string>();

    // Use modified BFS to find multiple paths
    const queue: Array<{
      currentUser: string;
      path: PathNode[];
      visited: Set<string>;
    }> = [{
      currentUser: sourceUserId,
      path: [{
        userId: sourceUserId,
        name: await this.getUserName(sourceUserId),
        degreeOfSeparation: 0
      }],
      visited: new Set([sourceUserId])
    }];

    while (queue.length > 0 && paths.length < maxPaths) {
      const { currentUser, path, visited } = queue.shift()!;

      // Skip if path too long
      if (path.length > maxLength) {
        continue;
      }

      // Found target
      if (currentUser === targetUserId) {
        const pathMetrics = this.calculatePathMetrics(path);
        paths.push({
          path,
          length: path.length - 1,
          ...pathMetrics
        });
        continue;
      }

      // Get connections
      const connections = await this.getDirectConnections(currentUser);

      for (const connection of connections) {
        if (!visited.has(connection.userId)) {
          const newVisited = new Set(visited);
          newVisited.add(connection.userId);

          const newPath = [
            ...path,
            {
              userId: connection.userId,
              name: connection.name,
              connectionStrength: connection.connectionStrength,
              trustLevel: connection.trustLevel,
              degreeOfSeparation: path.length
            }
          ];

          queue.push({
            currentUser: connection.userId,
            path: newPath,
            visited: newVisited
          });
        }
      }
    }

    // Sort by quality
    return paths.sort((a, b) => b.quality - a.quality);
  }

  /**
   * Calculate network diameter (longest shortest path)
   */
  async calculateNetworkDiameter(sampleSize: number = 100): Promise<number> {
    // Sample random users
    const users = await this.getSampleUsers(sampleSize);
    let maxDistance = 0;

    for (let i = 0; i < users.length - 1; i++) {
      for (let j = i + 1; j < users.length; j++) {
        const path = await this.findShortestPath(users[i], users[j]);
        if (path) {
          maxDistance = Math.max(maxDistance, path.length);
        }
      }
    }

    return maxDistance;
  }

  /**
   * Get network statistics
   */
  async getNetworkStatistics(): Promise<NetworkStatistics> {
    const cacheKey = 'network_statistics';
    const cached = await this.redis.get(cacheKey);

    if (cached) {
      return JSON.parse(cached);
    }

    const client = await this.pool.connect();

    try {
      // Total users
      const totalUsersResult = await client.query('SELECT COUNT(*) as count FROM users');
      const totalUsers = parseInt(totalUsersResult.rows[0].count);

      // Total connections
      const totalConnectionsResult = await client.query('SELECT COUNT(*) as count FROM connections');
      const totalConnections = parseInt(totalConnectionsResult.rows[0].count);

      // Average degree
      const averageDegree = totalUsers > 0 ? (totalConnections * 2) / totalUsers : 0;

      // Isolated users (no connections)
      const isolatedUsersResult = await client.query(`
        SELECT COUNT(DISTINCT u.id) as count
        FROM users u
        LEFT JOIN connections c ON u.id = c.user_id
        WHERE c.id IS NULL
      `);
      const isolatedUsers = parseInt(isolatedUsersResult.rows[0].count);

      // Clustering coefficient (sample-based)
      const clusteringCoefficient = await this.calculateClusteringCoefficient();

      // Network diameter (sample-based)
      const diameter = await this.calculateNetworkDiameter(50);

      const stats = {
        totalUsers,
        totalConnections,
        averageDegree,
        clusteringCoefficient,
        diameter,
        isolatedUsers
      };

      // Cache for 5 minutes
      await this.redis.set(cacheKey, JSON.stringify(stats), 'EX', 300);

      return stats;

    } finally {
      client.release();
    }
  }

  /**
   * Find bridge nodes (nodes that connect different clusters)
   * Uses betweenness centrality
   */
  async findBridgeNodes(topN: number = 10): Promise<Array<{
    userId: string;
    name: string;
    betweenness: number;
    degree: number;
  }>> {
    const cacheKey = `bridge_nodes:${topN}`;
    const cached = await this.redis.get(cacheKey);

    if (cached) {
      return JSON.parse(cached);
    }

    // Calculate betweenness centrality for sample of users
    const users = await this.getSampleUsers(100);
    const betweenness = new Map<string, number>();

    // Initialize
    for (const userId of users) {
      betweenness.set(userId, 0);
    }

    // Calculate betweenness for each pair
    for (let i = 0; i < users.length - 1; i++) {
      for (let j = i + 1; j < users.length; j++) {
        const paths = await this.findAlternativePaths(users[i], users[j], 3, 6);

        if (paths.length > 0) {
          // Count how many shortest paths go through each node
          const shortestLength = paths[0].length;
          const shortestPaths = paths.filter(p => p.length === shortestLength);

          for (const path of shortestPaths) {
            for (let k = 1; k < path.path.length - 1; k++) {
              const nodeId = path.path[k].userId;
              betweenness.set(nodeId, (betweenness.get(nodeId) || 0) + 1 / shortestPaths.length);
            }
          }
        }
      }
    }

    // Get top N
    const sorted = Array.from(betweenness.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, topN);

    const result = await Promise.all(
      sorted.map(async ([userId, betweennessValue]) => {
        const connections = await this.getDirectConnections(userId);
        return {
          userId,
          name: await this.getUserName(userId),
          betweenness: betweennessValue,
          degree: connections.length
        };
      })
    );

    // Cache for 10 minutes
    await this.redis.set(cacheKey, JSON.stringify(result), 'EX', 600);

    return result;
  }

  /**
   * Private helper methods
   */

  private async reconstructPath(
    sourceUserId: string,
    targetUserId: string,
    previous: Map<string, { userId: string; strength: number; trust: number }>
  ): Promise<ConnectionPath> {
    const path: PathNode[] = [];
    let current = targetUserId;
    let degree = 0;

    // Build path backwards
    const reversePath: PathNode[] = [];
    while (current !== sourceUserId) {
      const prev = previous.get(current);
      if (!prev) break;

      reversePath.push({
        userId: current,
        name: await this.getUserName(current),
        connectionStrength: prev.strength,
        trustLevel: prev.trust,
        degreeOfSeparation: degree++
      });

      current = prev.userId;
    }

    // Add source
    reversePath.push({
      userId: sourceUserId,
      name: await this.getUserName(sourceUserId),
      degreeOfSeparation: degree
    });

    // Reverse to get forward path
    const forwardPath = reversePath.reverse();

    // Calculate metrics
    const metrics = this.calculatePathMetrics(forwardPath);

    return {
      path: forwardPath,
      length: forwardPath.length - 1,
      ...metrics
    };
  }

  private calculatePathMetrics(path: PathNode[]): {
    totalStrength: number;
    averageTrust: number;
    weakestLink: number;
    quality: number;
  } {
    let totalStrength = 0;
    let totalTrust = 0;
    let weakestLink = 1.0;
    let validConnections = 0;

    for (const node of path) {
      if (node.connectionStrength !== undefined) {
        totalStrength += node.connectionStrength;
        validConnections++;
      }
      if (node.trustLevel !== undefined) {
        totalTrust += node.trustLevel;
        weakestLink = Math.min(weakestLink, node.trustLevel);
      }
    }

    const averageTrust = validConnections > 0 ? totalTrust / validConnections : 0;

    // Quality score: combination of strength, trust, and brevity
    const quality = (
      (totalStrength / Math.max(validConnections, 1)) * 0.3 +
      averageTrust * 0.4 +
      weakestLink * 0.2 +
      (1 / (path.length + 1)) * 0.1
    );

    return {
      totalStrength,
      averageTrust,
      weakestLink,
      quality
    };
  }

  private async getDirectConnections(userId: string): Promise<Array<{
    userId: string;
    name: string;
    connectionStrength: number;
    trustLevel: number;
  }>> {
    const cacheKey = `connections:${userId}`;
    const cached = await this.redis.get(cacheKey);

    if (cached) {
      return JSON.parse(cached);
    }

    const client = await this.pool.connect();

    try {
      const result = await client.query(`
        SELECT
          u.id as user_id,
          u.name,
          c.connection_strength,
          c.trust_level
        FROM connections c
        JOIN contacts ct ON c.contact_id = ct.id
        JOIN users u ON ct.email = u.email
        WHERE c.user_id = $1
      `, [userId]);

      const connections = result.rows.map(row => ({
        userId: row.user_id,
        name: row.name,
        connectionStrength: parseFloat(row.connection_strength),
        trustLevel: parseFloat(row.trust_level)
      }));

      // Cache for 5 minutes
      await this.redis.set(cacheKey, JSON.stringify(connections), 'EX', 300);

      return connections;

    } finally {
      client.release();
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

  private async calculateClusteringCoefficient(): Promise<number> {
    // Sample-based clustering coefficient calculation
    const sampleUsers = await this.getSampleUsers(50);
    let totalCoefficient = 0;
    let validUsers = 0;

    for (const userId of sampleUsers) {
      const neighbors = await this.getDirectConnections(userId);

      if (neighbors.length < 2) {
        continue; // Need at least 2 neighbors
      }

      let connectedPairs = 0;
      const possiblePairs = (neighbors.length * (neighbors.length - 1)) / 2;

      // Check how many neighbors are connected to each other
      for (let i = 0; i < neighbors.length - 1; i++) {
        for (let j = i + 1; j < neighbors.length; j++) {
          const path = await this.findShortestPath(neighbors[i].userId, neighbors[j].userId);
          if (path && path.length === 1) {
            connectedPairs++;
          }
        }
      }

      totalCoefficient += connectedPairs / possiblePairs;
      validUsers++;
    }

    return validUsers > 0 ? totalCoefficient / validUsers : 0;
  }
}
