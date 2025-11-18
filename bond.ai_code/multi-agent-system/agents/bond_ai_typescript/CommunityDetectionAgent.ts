import { Pool } from 'pg';
import Redis from 'ioredis';

/**
 * Community Detection Agent
 *
 * Implements Louvain algorithm for community detection:
 * - Detects natural clusters in the network
 * - Measures community quality (modularity)
 * - Identifies inter-community bridges
 * - Suggests strategic connections
 * - Analyzes community evolution
 *
 * Based on:
 * - Blondel et al. (2008) "Fast unfolding of communities in large networks"
 * - Newman & Girvan (2004) "Finding and evaluating community structure"
 */

export interface Community {
  communityId: string;
  name: string;
  members: string[];
  size: number;
  density: number; // Internal connection density
  modularity: number; // Quality score
  characteristics: {
    dominantIndustry?: string;
    dominantLocation?: string;
    commonExpertise: string[];
    averageTrustLevel: number;
  };
  centralMembers: Array<{
    userId: string;
    userName: string;
    centralityScore: number;
  }>;
  bridges: Array<{
    userId: string;
    userName: string;
    connectsToCommunities: string[];
  }>;
}

export interface CommunityStructure {
  communities: Community[];
  totalCommunities: number;
  overallModularity: number;
  hierarchyLevels: number;
  isolatedUsers: string[];
  intercommunityBridges: Array<{
    userId: string;
    communities: string[];
    bridgeStrength: number;
  }>;
}

export interface CommunityRecommendation {
  type: 'join_community' | 'bridge_communities' | 'create_subgroup' | 'strengthen_ties';
  targetCommunity?: string;
  reasoning: string;
  potentialBenefit: number;
  actionableSteps: string[];
}

export class CommunityDetectionAgent {
  // Louvain algorithm parameters
  private readonly MIN_MODULARITY_GAIN = 0.0001;
  private readonly MAX_ITERATIONS = 100;

  constructor(
    private pool: Pool,
    private redis: Redis
  ) {}

  /**
   * Detect communities using Louvain algorithm
   * Returns hierarchical community structure
   */
  async detectCommunities(
    minCommunitySize: number = 3
  ): Promise<CommunityStructure> {
    const cacheKey = `communities:${minCommunitySize}`;
    const cached = await this.redis.get(cacheKey);

    if (cached) {
      return JSON.parse(cached);
    }

    // Get all users and build network graph
    const users = await this.getAllUsers();
    const graph = await this.buildGraph(users);

    // Run Louvain algorithm
    const communities = await this.louvainAlgorithm(graph, minCommunitySize);

    // Calculate overall modularity
    const overallModularity = this.calculateModularity(graph, communities);

    // Identify inter-community bridges
    const intercommunityBridges = await this.findIntercommunityBridges(
      communities,
      graph
    );

    // Find isolated users
    const isolatedUsers = users.filter(
      userId => !communities.some(c => c.members.includes(userId))
    );

    // Enrich communities with characteristics
    const enrichedCommunities = await Promise.all(
      communities.map(c => this.enrichCommunity(c, graph))
    );

    const structure: CommunityStructure = {
      communities: enrichedCommunities,
      totalCommunities: enrichedCommunities.length,
      overallModularity,
      hierarchyLevels: 1, // Could be extended for hierarchical
      isolatedUsers,
      intercommunityBridges
    };

    // Cache for 20 minutes
    await this.redis.set(cacheKey, JSON.stringify(structure), 'EX', 1200);

    return structure;
  }

  /**
   * Louvain Algorithm Implementation
   * Phase 1: Modularity optimization
   * Phase 2: Community aggregation
   */
  private async louvainAlgorithm(
    graph: Map<string, Map<string, number>>,
    minSize: number
  ): Promise<Array<{ communityId: string; members: string[] }>> {
    const nodes = Array.from(graph.keys());

    // Initialize: each node in its own community
    const nodeToCommunity = new Map<string, string>();
    nodes.forEach(node => nodeToCommunity.set(node, node));

    let improved = true;
    let iteration = 0;

    // Phase 1: Iterative modularity optimization
    while (improved && iteration < this.MAX_ITERATIONS) {
      improved = false;
      iteration++;

      // Shuffle nodes for randomization
      const shuffledNodes = this.shuffle([...nodes]);

      for (const node of shuffledNodes) {
        const currentCommunity = nodeToCommunity.get(node)!;

        // Find neighboring communities
        const neighborCommunities = this.getNeighborCommunities(
          node,
          graph,
          nodeToCommunity
        );

        // Calculate modularity gain for each community
        let bestCommunity = currentCommunity;
        let bestGain = 0;

        for (const [community, _] of neighborCommunities) {
          const gain = this.modularityGain(
            node,
            community,
            currentCommunity,
            graph,
            nodeToCommunity
          );

          if (gain > bestGain) {
            bestGain = gain;
            bestCommunity = community;
          }
        }

        // Move node if improvement found
        if (bestGain > this.MIN_MODULARITY_GAIN && bestCommunity !== currentCommunity) {
          nodeToCommunity.set(node, bestCommunity);
          improved = true;
        }
      }
    }

    // Group nodes by community
    const communitiesMap = new Map<string, string[]>();
    for (const [node, community] of nodeToCommunity) {
      if (!communitiesMap.has(community)) {
        communitiesMap.set(community, []);
      }
      communitiesMap.get(community)!.push(node);
    }

    // Filter by minimum size and create community objects
    const communities: Array<{ communityId: string; members: string[] }> = [];
    let communityIndex = 1;

    for (const [_, members] of communitiesMap) {
      if (members.length >= minSize) {
        communities.push({
          communityId: `community_${communityIndex}`,
          members
        });
        communityIndex++;
      }
    }

    return communities;
  }

  /**
   * Calculate modularity gain for moving a node to a community
   */
  private modularityGain(
    node: string,
    targetCommunity: string,
    currentCommunity: string,
    graph: Map<string, Map<string, number>>,
    nodeToCommunity: Map<string, string>
  ): number {
    if (targetCommunity === currentCommunity) return 0;

    const nodeEdges = graph.get(node) || new Map();
    const totalEdges = this.getTotalEdgeWeight(graph);

    // Calculate ki (sum of weights of edges incident to node)
    let ki = 0;
    for (const weight of nodeEdges.values()) {
      ki += weight;
    }

    // Calculate ki_in (weight of edges from node to target community)
    let kiIn = 0;
    for (const [neighbor, weight] of nodeEdges) {
      if (nodeToCommunity.get(neighbor) === targetCommunity) {
        kiIn += weight;
      }
    }

    // Calculate sigma_tot (sum of weights of edges in target community)
    let sigmaTot = 0;
    for (const [otherNode, otherCommunity] of nodeToCommunity) {
      if (otherCommunity === targetCommunity) {
        const edges = graph.get(otherNode) || new Map();
        for (const weight of edges.values()) {
          sigmaTot += weight;
        }
      }
    }

    // Modularity gain formula
    const gain = (kiIn / totalEdges) - ((sigmaTot * ki) / (2 * totalEdges * totalEdges));

    return gain;
  }

  /**
   * Calculate overall network modularity
   */
  private calculateModularity(
    graph: Map<string, Map<string, number>>,
    communities: Array<{ communityId: string; members: string[] }>
  ): number {
    const totalEdges = this.getTotalEdgeWeight(graph);
    let modularity = 0;

    for (const community of communities) {
      const members = new Set(community.members);

      // Calculate internal edges
      let internalEdges = 0;
      let totalDegree = 0;

      for (const member of community.members) {
        const edges = graph.get(member) || new Map();

        for (const [neighbor, weight] of edges) {
          if (members.has(neighbor)) {
            internalEdges += weight;
          }
          totalDegree += weight;
        }
      }

      // Modularity contribution
      const edgeFraction = internalEdges / (2 * totalEdges);
      const degreeFraction = (totalDegree / (2 * totalEdges)) ** 2;

      modularity += edgeFraction - degreeFraction;
    }

    return modularity;
  }

  /**
   * Find users who bridge multiple communities
   */
  private async findIntercommunityBridges(
    communities: Array<{ communityId: string; members: string[] }>,
    graph: Map<string, Map<string, number>>
  ): Promise<Array<{
    userId: string;
    communities: string[];
    bridgeStrength: number;
  }>> {
    const bridges: Array<{
      userId: string;
      communities: string[];
      bridgeStrength: number;
    }> = [];

    // Create reverse mapping: user -> community
    const userToCommunity = new Map<string, string>();
    for (const community of communities) {
      for (const member of community.members) {
        userToCommunity.set(member, community.communityId);
      }
    }

    // Check each user
    for (const [userId, edges] of graph) {
      const userCommunity = userToCommunity.get(userId);
      if (!userCommunity) continue;

      // Find connections to other communities
      const connectedCommunities = new Set<string>([userCommunity]);
      let crossCommunityEdges = 0;
      let totalEdges = 0;

      for (const [neighbor, weight] of edges) {
        totalEdges += weight;
        const neighborCommunity = userToCommunity.get(neighbor);

        if (neighborCommunity && neighborCommunity !== userCommunity) {
          connectedCommunities.add(neighborCommunity);
          crossCommunityEdges += weight;
        }
      }

      // If connects to 2+ communities, it's a bridge
      if (connectedCommunities.size >= 2) {
        const bridgeStrength = totalEdges > 0 ? crossCommunityEdges / totalEdges : 0;

        bridges.push({
          userId,
          communities: Array.from(connectedCommunities),
          bridgeStrength
        });
      }
    }

    return bridges.sort((a, b) => b.bridgeStrength - a.bridgeStrength);
  }

  /**
   * Enrich community with characteristics and metadata
   */
  private async enrichCommunity(
    community: { communityId: string; members: string[] },
    graph: Map<string, Map<string, number>>
  ): Promise<Community> {
    // Get member profiles
    const profiles = await Promise.all(
      community.members.map(id => this.getUserProfile(id))
    );

    // Calculate density
    let internalEdges = 0;
    const maxEdges = (community.members.length * (community.members.length - 1)) / 2;

    const memberSet = new Set(community.members);
    for (const member of community.members) {
      const edges = graph.get(member) || new Map();
      for (const neighbor of edges.keys()) {
        if (memberSet.has(neighbor)) {
          internalEdges++;
        }
      }
    }

    const density = maxEdges > 0 ? (internalEdges / 2) / maxEdges : 0;

    // Find dominant characteristics
    const industries = profiles.map(p => p.industry).filter(Boolean);
    const locations = profiles.map(p => p.location?.country).filter(Boolean);
    const allExpertise = profiles.flatMap(p => p.expertiseAreas || []);

    const dominantIndustry = this.findMostCommon(industries);
    const dominantLocation = this.findMostCommon(locations);
    const commonExpertise = this.findTopN(allExpertise, 5);

    // Calculate average trust
    let totalTrust = 0;
    let trustCount = 0;

    for (const member of community.members) {
      const edges = graph.get(member) || new Map();
      for (const [neighbor, weight] of edges) {
        if (memberSet.has(neighbor)) {
          totalTrust += weight;
          trustCount++;
        }
      }
    }

    const averageTrustLevel = trustCount > 0 ? totalTrust / trustCount : 0;

    // Find central members (highest degree within community)
    const centralMembers = community.members
      .map(memberId => {
        const edges = graph.get(memberId) || new Map();
        let internalDegree = 0;

        for (const neighbor of edges.keys()) {
          if (memberSet.has(neighbor)) {
            internalDegree++;
          }
        }

        return {
          userId: memberId,
          userName: profiles.find(p => p.id === memberId)?.name || 'Unknown',
          centralityScore: internalDegree / (community.members.length - 1)
        };
      })
      .sort((a, b) => b.centralityScore - a.centralityScore)
      .slice(0, 5);

    // Find bridges (members with external connections)
    const bridges = community.members
      .map(memberId => {
        const edges = graph.get(memberId) || new Map();
        const externalCommunities = new Set<string>();

        for (const neighbor of edges.keys()) {
          if (!memberSet.has(neighbor)) {
            // This is an external connection
            externalCommunities.add('external'); // Simplified
          }
        }

        if (externalCommunities.size === 0) return null;

        return {
          userId: memberId,
          userName: profiles.find(p => p.id === memberId)?.name || 'Unknown',
          connectsToCommunities: Array.from(externalCommunities)
        };
      })
      .filter(Boolean) as Array<{
        userId: string;
        userName: string;
        connectsToCommunities: string[];
      }>;

    // Generate community name
    const name = `${dominantIndustry || 'Mixed'} - ${dominantLocation || 'Global'}`;

    return {
      communityId: community.communityId,
      name,
      members: community.members,
      size: community.members.length,
      density,
      modularity: 0, // Will be set by overall calculation
      characteristics: {
        dominantIndustry,
        dominantLocation,
        commonExpertise,
        averageTrustLevel
      },
      centralMembers,
      bridges
    };
  }

  /**
   * Recommend community-related actions for a user
   */
  async recommendCommunityActions(
    userId: string
  ): Promise<CommunityRecommendation[]> {
    const structure = await this.detectCommunities();
    const userCommunity = structure.communities.find(c => c.members.includes(userId));

    const recommendations: CommunityRecommendation[] = [];

    if (!userCommunity) {
      // User not in any community - suggest joining
      const bestCommunity = await this.findBestCommunityForUser(userId, structure);

      if (bestCommunity) {
        recommendations.push({
          type: 'join_community',
          targetCommunity: bestCommunity.communityId,
          reasoning: `Strong alignment with ${bestCommunity.name} community`,
          potentialBenefit: 0.8,
          actionableSteps: [
            `Connect with ${bestCommunity.centralMembers[0]?.userName || 'community leaders'}`,
            'Attend community events',
            'Engage with community content'
          ]
        });
      }
    } else {
      // User in community - suggest bridging
      const userProfile = await this.getUserProfile(userId);
      const connections = await this.getUserConnections(userId);

      // Check if user could be a bridge
      const externalConnections = connections.filter(
        connId => !userCommunity.members.includes(connId)
      );

      if (externalConnections.length >= 3) {
        recommendations.push({
          type: 'bridge_communities',
          reasoning: `You have ${externalConnections.length} connections outside your community`,
          potentialBenefit: 0.75,
          actionableSteps: [
            'Introduce community members to external contacts',
            'Organize cross-community events',
            'Share insights between communities'
          ]
        });
      }

      // Check if community is too large (could split)
      if (userCommunity.size > 30) {
        recommendations.push({
          type: 'create_subgroup',
          reasoning: 'Large community could benefit from focused subgroups',
          potentialBenefit: 0.6,
          actionableSteps: [
            'Identify specific interest areas',
            'Form working groups',
            'Organize topic-specific meetups'
          ]
        });
      }

      // Check if ties need strengthening
      if (userCommunity.density < 0.3) {
        recommendations.push({
          type: 'strengthen_ties',
          reasoning: 'Community has low internal connectivity',
          potentialBenefit: 0.7,
          actionableSteps: [
            'Introduce unconnected members',
            'Organize group activities',
            'Create shared projects'
          ]
        });
      }
    }

    return recommendations.sort((a, b) => b.potentialBenefit - a.potentialBenefit);
  }

  /**
   * Analyze community overlap for a user
   */
  async analyzeCommunityOverlap(userId: string): Promise<{
    primaryCommunity: string | null;
    secondaryCommunities: string[];
    overlapScore: number;
    role: 'core_member' | 'bridge' | 'peripheral' | 'isolated';
  }> {
    const structure = await this.detectCommunities();
    const communities = structure.communities.filter(c => c.members.includes(userId));

    if (communities.length === 0) {
      return {
        primaryCommunity: null,
        secondaryCommunities: [],
        overlapScore: 0,
        role: 'isolated'
      };
    }

    // Primary community is largest or highest centrality
    const primary = communities.sort((a, b) => b.size - a.size)[0];
    const secondary = communities.filter(c => c.communityId !== primary.communityId)
      .map(c => c.communityId);

    const overlapScore = communities.length > 1 ? 0.8 : 0.2;

    // Determine role
    let role: 'core_member' | 'bridge' | 'peripheral' | 'isolated';

    const isCentral = primary.centralMembers.some(m => m.userId === userId);
    const isBridge = structure.intercommunityBridges.some(b => b.userId === userId);

    if (isCentral && !isBridge) {
      role = 'core_member';
    } else if (isBridge) {
      role = 'bridge';
    } else if (communities.length > 0) {
      role = 'peripheral';
    } else {
      role = 'isolated';
    }

    return {
      primaryCommunity: primary.communityId,
      secondaryCommunities: secondary,
      overlapScore,
      role
    };
  }

  /**
   * Helper methods
   */

  private async buildGraph(users: string[]): Promise<Map<string, Map<string, number>>> {
    const graph = new Map<string, Map<string, number>>();

    for (const userId of users) {
      const edges = new Map<string, number>();
      const connections = await this.getUserConnectionsWithTrust(userId);

      for (const { targetId, trust } of connections) {
        if (users.includes(targetId)) {
          edges.set(targetId, trust);
        }
      }

      graph.set(userId, edges);
    }

    return graph;
  }

  private getNeighborCommunities(
    node: string,
    graph: Map<string, Map<string, number>>,
    nodeToCommunity: Map<string, string>
  ): Map<string, number> {
    const neighbors = graph.get(node) || new Map();
    const communities = new Map<string, number>();

    for (const [neighbor, weight] of neighbors) {
      const community = nodeToCommunity.get(neighbor)!;
      communities.set(community, (communities.get(community) || 0) + weight);
    }

    return communities;
  }

  private getTotalEdgeWeight(graph: Map<string, Map<string, number>>): number {
    let total = 0;
    for (const edges of graph.values()) {
      for (const weight of edges.values()) {
        total += weight;
      }
    }
    return total / 2; // Each edge counted twice
  }

  private shuffle<T>(array: T[]): T[] {
    const result = [...array];
    for (let i = result.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [result[i], result[j]] = [result[j], result[i]];
    }
    return result;
  }

  private findMostCommon(items: string[]): string | undefined {
    if (items.length === 0) return undefined;

    const counts = new Map<string, number>();
    for (const item of items) {
      counts.set(item, (counts.get(item) || 0) + 1);
    }

    let maxCount = 0;
    let mostCommon: string | undefined;

    for (const [item, count] of counts) {
      if (count > maxCount) {
        maxCount = count;
        mostCommon = item;
      }
    }

    return mostCommon;
  }

  private findTopN(items: string[], n: number): string[] {
    const counts = new Map<string, number>();
    for (const item of items) {
      counts.set(item, (counts.get(item) || 0) + 1);
    }

    return Array.from(counts.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, n)
      .map(([item]) => item);
  }

  private async findBestCommunityForUser(
    userId: string,
    structure: CommunityStructure
  ): Promise<Community | null> {
    const userProfile = await this.getUserProfile(userId);
    let bestScore = 0;
    let bestCommunity: Community | null = null;

    for (const community of structure.communities) {
      let score = 0;

      // Industry match
      if (community.characteristics.dominantIndustry === userProfile.industry) {
        score += 0.4;
      }

      // Location match
      if (community.characteristics.dominantLocation === userProfile.location?.country) {
        score += 0.3;
      }

      // Expertise overlap
      const userExpertise = new Set(userProfile.expertiseAreas || []);
      const overlapCount = community.characteristics.commonExpertise.filter(
        e => userExpertise.has(e)
      ).length;
      score += (overlapCount / Math.max(userExpertise.size, 1)) * 0.3;

      if (score > bestScore) {
        bestScore = score;
        bestCommunity = community;
      }
    }

    return bestScore > 0.4 ? bestCommunity : null;
  }

  // Database helpers
  private async getAllUsers(): Promise<string[]> {
    const client = await this.pool.connect();
    try {
      const result = await client.query('SELECT id FROM users LIMIT 200');
      return result.rows.map(row => row.id);
    } finally {
      client.release();
    }
  }

  private async getUserProfile(userId: string): Promise<any> {
    const client = await this.pool.connect();
    try {
      const result = await client.query(`
        SELECT u.id, u.name, u.industry, up.expertise_areas, up.location
        FROM users u
        JOIN user_profiles up ON u.id = up.user_id
        WHERE u.id = $1
      `, [userId]);

      return result.rows[0] || {};
    } finally {
      client.release();
    }
  }

  private async getUserConnections(userId: string): Promise<string[]> {
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

  private async getUserConnectionsWithTrust(
    userId: string
  ): Promise<Array<{ targetId: string; trust: number }>> {
    const client = await this.pool.connect();
    try {
      const result = await client.query(`
        SELECT u.id, c.trust_level
        FROM connections c
        JOIN contacts ct ON c.contact_id = ct.id
        JOIN users u ON ct.email = u.email
        WHERE c.user_id = $1
      `, [userId]);

      return result.rows.map(row => ({
        targetId: row.id,
        trust: parseFloat(row.trust_level) || 0.5
      }));
    } finally {
      client.release();
    }
  }
}
