import { Pool } from 'pg';
import Redis from 'ioredis';
import { ConnectionStrengthAnalyzer } from './ConnectionStrengthAnalyzer';

/**
 * Serendipity Agent
 *
 * Finds unexpected but valuable matches using "Strength of Weak Ties" theory:
 * - Weak ties provide access to novel information
 * - Bridges between different clusters are valuable
 * - Distant connections offer fresh perspectives
 * - Serendipitous matches often lead to innovation
 *
 * Based on Granovetter's "Strength of Weak Ties" (1973) and
 * recent research on innovation through diverse networks.
 */

export interface SerendipitousMatch {
  userId: string;
  targetId: string;
  serendipityScore: number; // 0-1, higher = more serendipitous
  unexpectednessScore: number; // How unexpected this match is
  potentialValue: number; // Estimated value of this match
  bridgeValue: number; // Value as a bridge to new networks
  reasons: {
    differentCluster: boolean;
    novelIndustry: boolean;
    uniqueExpertise: boolean;
    weakTieBridge: boolean;
    geographicDiversity: boolean;
    unexpectedSynergy: boolean;
  };
  insights: string[];
  recommendation: string;
}

export interface NovelOpportunity {
  type: 'weak_tie_introduction' | 'cluster_bridge' | 'industry_crossover' | 'geographic_expansion';
  targetId: string;
  targetName: string;
  opportunityScore: number;
  description: string;
  actionableSteps: string[];
}

export interface DiversityMetrics {
  industryDiversity: number; // 0-1
  geographicDiversity: number;
  expertiseDiversity: number;
  networkDiversity: number; // Based on clustering
  overallDiversity: number;
}

export class SerendipityAgent {
  private strengthAnalyzer: ConnectionStrengthAnalyzer;

  constructor(
    private pool: Pool,
    private redis: Redis
  ) {
    this.strengthAnalyzer = new ConnectionStrengthAnalyzer(pool, redis);
  }

  /**
   * Find serendipitous matches - unexpected but highly valuable
   * Uses weak tie theory: distant connections bring novel information
   */
  async findSerendipitousMatches(
    userId: string,
    limit: number = 10
  ): Promise<SerendipitousMatch[]> {
    const cacheKey = `serendipity:${userId}:${limit}`;
    const cached = await this.redis.get(cacheKey);

    if (cached) {
      return JSON.parse(cached);
    }

    // Get user's profile and current network
    const userProfile = await this.getUserProfile(userId);
    const directConnections = await this.getDirectConnections(userId);
    const closeNetwork = await this.getCloseNetwork(userId, 2); // Within 2 degrees

    // Find potential matches NOT in close network (serendipity!)
    const candidates = await this.findDistantCandidates(
      userId,
      closeNetwork,
      limit * 3 // Get more candidates to filter
    );

    // Score each candidate for serendipity
    const scoredMatches: SerendipitousMatch[] = [];

    for (const candidate of candidates) {
      const match = await this.scoreSerendipity(
        userId,
        candidate.id,
        userProfile,
        candidate,
        closeNetwork
      );

      if (match) {
        scoredMatches.push(match);
      }
    }

    // Sort by serendipity score and take top N
    const topMatches = scoredMatches
      .sort((a, b) => b.serendipityScore - a.serendipityScore)
      .slice(0, limit);

    // Cache for 30 minutes
    await this.redis.set(cacheKey, JSON.stringify(topMatches), 'EX', 1800);

    return topMatches;
  }

  /**
   * Find novel opportunities through weak ties
   */
  async findNovelOpportunities(
    userId: string,
    limit: number = 5
  ): Promise<NovelOpportunity[]> {
    const opportunities: NovelOpportunity[] = [];

    // Get weak ties
    const weakTies = await this.strengthAnalyzer.findWeakTies(userId, 20);

    // Analyze each weak tie for opportunities
    for (const tie of weakTies) {
      const targetId = tie.userId2 === userId ? tie.userId1 : tie.userId2;

      // Check what this weak tie can provide access to
      const targetNetwork = await this.getDirectConnections(targetId);
      const targetProfile = await this.getUserProfile(targetId);

      // Weak tie introduction opportunity
      if (targetNetwork.length > 10) {
        opportunities.push({
          type: 'weak_tie_introduction',
          targetId,
          targetName: targetProfile.name,
          opportunityScore: 0.7 + (targetNetwork.length / 100),
          description: `${targetProfile.name} has ${targetNetwork.length} connections in ${targetProfile.industry}, providing access to a new network`,
          actionableSteps: [
            `Reach out to ${targetProfile.name} for a coffee chat`,
            `Ask about their work in ${targetProfile.industry}`,
            `Request introductions to relevant contacts`
          ]
        });
      }

      // Industry crossover opportunity
      if (targetProfile.industry !== (await this.getUserProfile(userId)).industry) {
        opportunities.push({
          type: 'industry_crossover',
          targetId,
          targetName: targetProfile.name,
          opportunityScore: 0.75,
          description: `Cross-industry collaboration with ${targetProfile.industry} professional`,
          actionableSteps: [
            `Explore synergies between industries`,
            `Discuss potential partnerships`,
            `Share unique perspectives from your industry`
          ]
        });
      }

      // Geographic expansion
      if (targetProfile.location.country !== (await this.getUserProfile(userId)).location.country) {
        opportunities.push({
          type: 'geographic_expansion',
          targetId,
          targetName: targetProfile.name,
          opportunityScore: 0.65,
          description: `Access to ${targetProfile.location.country} market through ${targetProfile.name}`,
          actionableSteps: [
            `Learn about market dynamics in ${targetProfile.location.country}`,
            `Discuss potential expansion opportunities`,
            `Request local market insights`
          ]
        });
      }
    }

    // Sort by opportunity score
    return opportunities
      .sort((a, b) => b.opportunityScore - a.opportunityScore)
      .slice(0, limit);
  }

  /**
   * Analyze network diversity (more diversity = more serendipity potential)
   */
  async analyzeNetworkDiversity(userId: string): Promise<DiversityMetrics> {
    const cacheKey = `diversity:${userId}`;
    const cached = await this.redis.get(cacheKey);

    if (cached) {
      return JSON.parse(cached);
    }

    const connections = await this.getConnectionProfiles(userId);

    if (connections.length === 0) {
      return {
        industryDiversity: 0,
        geographicDiversity: 0,
        expertiseDiversity: 0,
        networkDiversity: 0,
        overallDiversity: 0
      };
    }

    // Industry diversity (Shannon entropy)
    const industries = connections.map(c => c.industry);
    const industryDiversity = this.calculateShannnonEntropy(industries);

    // Geographic diversity
    const countries = connections.map(c => c.location.country);
    const geographicDiversity = this.calculateShannnonEntropy(countries);

    // Expertise diversity
    const allExpertise = connections.flatMap(c => c.expertiseAreas);
    const expertiseDiversity = this.calculateShannnonEntropy(allExpertise);

    // Network diversity (based on clustering)
    const networkDiversity = await this.calculateNetworkDiversity(userId, connections);

    const overallDiversity = (
      industryDiversity * 0.3 +
      geographicDiversity * 0.25 +
      expertiseDiversity * 0.25 +
      networkDiversity * 0.2
    );

    const metrics = {
      industryDiversity,
      geographicDiversity,
      expertiseDiversity,
      networkDiversity,
      overallDiversity
    };

    // Cache for 15 minutes
    await this.redis.set(cacheKey, JSON.stringify(metrics), 'EX', 900);

    return metrics;
  }

  /**
   * Suggest connections to increase diversity
   */
  async suggestDiversityConnections(
    userId: string,
    limit: number = 5
  ): Promise<Array<{
    targetId: string;
    targetName: string;
    diversityImpact: number;
    reason: string;
  }>> {
    const currentDiversity = await this.analyzeNetworkDiversity(userId);
    const userProfile = await this.getUserProfile(userId);

    const suggestions: Array<{
      targetId: string;
      targetName: string;
      diversityImpact: number;
      reason: string;
    }> = [];

    // Find candidates from different industries
    if (currentDiversity.industryDiversity < 0.7) {
      const differentIndustry = await this.findDifferentIndustry(userId, userProfile.industry);

      for (const candidate of differentIndustry.slice(0, 2)) {
        suggestions.push({
          targetId: candidate.id,
          targetName: candidate.name,
          diversityImpact: 0.8,
          reason: `Add ${candidate.industry} perspective to your network`
        });
      }
    }

    // Find candidates from different geographies
    if (currentDiversity.geographicDiversity < 0.6) {
      const differentCountry = await this.findDifferentCountry(userId, userProfile.location.country);

      for (const candidate of differentCountry.slice(0, 2)) {
        suggestions.push({
          targetId: candidate.id,
          targetName: candidate.name,
          diversityImpact: 0.75,
          reason: `Expand geographic reach to ${candidate.location.country}`
        });
      }
    }

    // Find candidates with unique expertise
    const uniqueExpertise = await this.findUniqueExpertise(userId);
    for (const candidate of uniqueExpertise.slice(0, 2)) {
      suggestions.push({
        targetId: candidate.id,
        targetName: candidate.name,
        diversityImpact: 0.7,
        reason: `Access unique expertise: ${candidate.uniqueSkills.join(', ')}`
      });
    }

    return suggestions
      .sort((a, b) => b.diversityImpact - a.diversityImpact)
      .slice(0, limit);
  }

  /**
   * Find "bridge" users who connect disparate networks
   * These are valuable for serendipitous discoveries
   */
  async findBridgeUsers(
    userId: string,
    limit: number = 10
  ): Promise<Array<{
    bridgeId: string;
    bridgeName: string;
    bridgeScore: number;
    clustersConnected: number;
    value: string;
  }>> {
    // Use betweenness centrality to find bridges
    const allUsers = await this.getSampleUsers(100);

    const client = await this.pool.connect();

    try {
      // Find users with high betweenness and different clusters
      const result = await client.query(`
        SELECT
          u.id,
          u.name,
          u.industry,
          up.location,
          COUNT(DISTINCT c.id) as connection_count
        FROM users u
        JOIN user_profiles up ON u.id = up.user_id
        JOIN connections c ON u.id = c.user_id
        WHERE u.id != $1
        GROUP BY u.id, u.name, u.industry, up.location
        HAVING COUNT(DISTINCT c.id) > 10
        ORDER BY connection_count DESC
        LIMIT $2
      `, [userId, limit * 2]);

      const candidates = result.rows;

      // Score each as potential bridge
      const bridges = await Promise.all(
        candidates.map(async candidate => {
          // Calculate how many different clusters they connect
          const centrality = await this.strengthAnalyzer.calculateCentrality(candidate.id);

          return {
            bridgeId: candidate.id,
            bridgeName: candidate.name,
            bridgeScore: centrality.betweennessCentrality,
            clustersConnected: Math.floor(centrality.betweennessCentrality * 10) + 2,
            value: `Connects ${candidate.industry} with other industries`
          };
        })
      );

      return bridges
        .sort((a, b) => b.bridgeScore - a.bridgeScore)
        .slice(0, limit);

    } finally {
      client.release();
    }
  }

  /**
   * Private helper methods
   */

  private async scoreSerendipity(
    userId: string,
    targetId: string,
    userProfile: any,
    targetProfile: any,
    closeNetwork: Set<string>
  ): Promise<SerendipitousMatch | null> {
    // Calculate various scores
    const differentCluster = !closeNetwork.has(targetId);
    const novelIndustry = targetProfile.industry !== userProfile.industry;
    const uniqueExpertise = this.hasUniqueExpertise(
      userProfile.expertiseAreas,
      targetProfile.expertiseAreas
    );
    const geographicDiversity = targetProfile.location.country !== userProfile.location.country;

    // Check for weak tie bridge potential
    const commonConnections = await this.getCommonConnections(userId, targetId);
    const weakTieBridge = commonConnections.length > 0 && commonConnections.length < 3;

    // Check for unexpected synergies
    const unexpectedSynergy = await this.checkUnexpectedSynergy(
      userProfile,
      targetProfile
    );

    const reasons = {
      differentCluster,
      novelIndustry,
      uniqueExpertise,
      weakTieBridge,
      geographicDiversity,
      unexpectedSynergy
    };

    // Calculate scores
    const unexpectednessScore = (
      (differentCluster ? 0.25 : 0) +
      (novelIndustry ? 0.2 : 0) +
      (uniqueExpertise ? 0.2 : 0) +
      (geographicDiversity ? 0.15 : 0) +
      (unexpectedSynergy ? 0.2 : 0)
    );

    // Estimate potential value
    const potentialValue = await this.estimatePotentialValue(
      userProfile,
      targetProfile,
      reasons
    );

    // Bridge value
    const bridgeValue = weakTieBridge ? 0.8 : differentCluster ? 0.6 : 0.3;

    // Overall serendipity score
    const serendipityScore = (
      unexpectednessScore * 0.4 +
      potentialValue * 0.35 +
      bridgeValue * 0.25
    );

    // Must meet minimum threshold
    if (serendipityScore < 0.4) {
      return null;
    }

    // Generate insights
    const insights = this.generateSerendipityInsights(reasons, targetProfile);

    // Generate recommendation
    const recommendation = this.generateSerendipityRecommendation(
      serendipityScore,
      reasons,
      targetProfile
    );

    return {
      userId,
      targetId,
      serendipityScore,
      unexpectednessScore,
      potentialValue,
      bridgeValue,
      reasons,
      insights,
      recommendation
    };
  }

  private async findDistantCandidates(
    userId: string,
    closeNetwork: Set<string>,
    limit: number
  ): Promise<any[]> {
    const client = await this.pool.connect();

    try {
      // Find users NOT in close network
      const closeNetworkArray = Array.from(closeNetwork);

      const result = await client.query(`
        SELECT
          u.id,
          u.name,
          u.industry,
          up.expertise_areas,
          up.location,
          up.needs,
          up.offerings
        FROM users u
        JOIN user_profiles up ON u.id = up.user_id
        WHERE u.id != $1
        ${closeNetworkArray.length > 0 ? 'AND u.id != ALL($2)' : ''}
        ORDER BY RANDOM()
        LIMIT $3
      `, closeNetworkArray.length > 0 ? [userId, closeNetworkArray, limit] : [userId, limit]);

      return result.rows.map(row => ({
        id: row.id,
        name: row.name,
        industry: row.industry,
        expertiseAreas: row.expertise_areas,
        location: row.location,
        needs: row.needs,
        offerings: row.offerings
      }));

    } finally {
      client.release();
    }
  }

  private calculateShannnonEntropy(values: string[]): number {
    if (values.length === 0) return 0;

    // Count frequencies
    const frequencies = new Map<string, number>();
    for (const value of values) {
      frequencies.set(value, (frequencies.get(value) || 0) + 1);
    }

    // Calculate entropy
    let entropy = 0;
    const total = values.length;

    for (const count of frequencies.values()) {
      const p = count / total;
      entropy -= p * Math.log2(p);
    }

    // Normalize to 0-1
    const maxEntropy = Math.log2(frequencies.size);
    return maxEntropy > 0 ? entropy / maxEntropy : 0;
  }

  private async calculateNetworkDiversity(
    userId: string,
    connections: any[]
  ): Promise<number> {
    // Check if connections are from different clusters
    // Higher diversity = connections span multiple clusters

    if (connections.length < 2) return 0;

    // Sample connections and check how many are connected to each other
    let disconnectedPairs = 0;
    let totalPairs = 0;

    const sampleSize = Math.min(15, connections.length);
    for (let i = 0; i < sampleSize - 1; i++) {
      for (let j = i + 1; j < sampleSize; j++) {
        totalPairs++;
        const connected = await this.areConnected(connections[i].id, connections[j].id);
        if (!connected) {
          disconnectedPairs++;
        }
      }
    }

    // Higher percentage of disconnected pairs = more diversity
    return totalPairs > 0 ? disconnectedPairs / totalPairs : 0;
  }

  private hasUniqueExpertise(expertise1: string[], expertise2: string[]): boolean {
    const set1 = new Set(expertise1);
    const set2 = new Set(expertise2);

    // Check for expertise in set2 not in set1
    for (const skill of set2) {
      if (!set1.has(skill)) {
        return true;
      }
    }

    return false;
  }

  private async checkUnexpectedSynergy(
    profile1: any,
    profile2: any
  ): Promise<boolean> {
    // Check if needs of one match offerings of other (unexpected match)
    const needs1 = profile1.needs || [];
    const needs2 = profile2.needs || [];
    const offerings1 = profile1.offerings || [];
    const offerings2 = profile2.offerings || [];

    // Check for cross-matches
    for (const need of needs1) {
      for (const offering of offerings2) {
        if (this.categoriesMatch(need.category, offering.category)) {
          return true;
        }
      }
    }

    for (const need of needs2) {
      for (const offering of offerings1) {
        if (this.categoriesMatch(need.category, offering.category)) {
          return true;
        }
      }
    }

    return false;
  }

  private categoriesMatch(cat1: string, cat2: string): boolean {
    // Simple matching - could be more sophisticated
    return cat1.toLowerCase().includes(cat2.toLowerCase()) ||
           cat2.toLowerCase().includes(cat1.toLowerCase());
  }

  private async estimatePotentialValue(
    profile1: any,
    profile2: any,
    reasons: any
  ): Promise<number> {
    let value = 0.5; // Base value

    // Increase value for various factors
    if (reasons.novelIndustry) value += 0.15;
    if (reasons.uniqueExpertise) value += 0.15;
    if (reasons.unexpectedSynergy) value += 0.2;
    if (reasons.weakTieBridge) value += 0.1;

    return Math.min(value, 1.0);
  }

  private generateSerendipityInsights(reasons: any, targetProfile: any): string[] {
    const insights: string[] = [];

    if (reasons.differentCluster) {
      insights.push('From a different part of the network - brings fresh perspective');
    }

    if (reasons.novelIndustry) {
      insights.push(`${targetProfile.industry} industry perspective offers cross-pollination opportunities`);
    }

    if (reasons.uniqueExpertise) {
      insights.push('Possesses unique expertise not common in your network');
    }

    if (reasons.weakTieBridge) {
      insights.push('Weak tie connection - valuable for novel information and opportunities');
    }

    if (reasons.geographicDiversity) {
      insights.push(`Geographic diversity (${targetProfile.location.country}) expands market reach`);
    }

    if (reasons.unexpectedSynergy) {
      insights.push('Unexpected synergy detected - complementary needs and offerings');
    }

    return insights;
  }

  private generateSerendipityRecommendation(
    score: number,
    reasons: any,
    targetProfile: any
  ): string {
    if (score >= 0.8) {
      return `Highly serendipitous match! ${targetProfile.name} represents a unique opportunity ` +
             `for innovation and fresh perspectives. Strong recommendation to connect.`;
    } else if (score >= 0.6) {
      return `Good serendipity potential with ${targetProfile.name}. ` +
             `This connection could open doors to new opportunities and insights.`;
    } else {
      return `Moderately serendipitous connection. ${targetProfile.name} offers some ` +
             `novel perspectives worth exploring.`;
    }
  }

  // ... (helper methods for database queries)

  private async getUserProfile(userId: string): Promise<any> {
    const client = await this.pool.connect();

    try {
      const result = await client.query(`
        SELECT
          u.id,
          u.name,
          u.industry,
          up.expertise_areas,
          up.location,
          up.needs,
          up.offerings
        FROM users u
        JOIN user_profiles up ON u.id = up.user_id
        WHERE u.id = $1
      `, [userId]);

      const row = result.rows[0];
      return {
        id: row.id,
        name: row.name,
        industry: row.industry,
        expertiseAreas: row.expertise_areas,
        location: row.location,
        needs: row.needs,
        offerings: row.offerings
      };

    } finally {
      client.release();
    }
  }

  private async getDirectConnections(userId: string): Promise<any[]> {
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

  private async getCloseNetwork(userId: string, maxDegrees: number): Promise<Set<string>> {
    const closeNetwork = new Set<string>([userId]);
    const queue: Array<{ id: string; degree: number }> = [{ id: userId, degree: 0 }];
    const visited = new Set<string>([userId]);

    while (queue.length > 0) {
      const { id, degree } = queue.shift()!;

      if (degree >= maxDegrees) continue;

      const connections = await this.getDirectConnections(id);

      for (const connId of connections) {
        if (!visited.has(connId)) {
          visited.add(connId);
          closeNetwork.add(connId);
          queue.push({ id: connId, degree: degree + 1 });
        }
      }
    }

    return closeNetwork;
  }

  private async getConnectionProfiles(userId: string): Promise<any[]> {
    const connectionIds = await this.getDirectConnections(userId);

    return Promise.all(
      connectionIds.map(id => this.getUserProfile(id))
    );
  }

  private async getCommonConnections(userId1: string, userId2: string): Promise<string[]> {
    const connections1 = new Set(await this.getDirectConnections(userId1));
    const connections2 = await this.getDirectConnections(userId2);

    return connections2.filter(id => connections1.has(id));
  }

  private async areConnected(userId1: string, userId2: string): Promise<boolean> {
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

  private async findDifferentIndustry(userId: string, currentIndustry: string): Promise<any[]> {
    const client = await this.pool.connect();

    try {
      const result = await client.query(`
        SELECT u.id, u.name, u.industry
        FROM users u
        WHERE u.id != $1 AND u.industry != $2
        ORDER BY RANDOM()
        LIMIT 5
      `, [userId, currentIndustry]);

      return result.rows;

    } finally {
      client.release();
    }
  }

  private async findDifferentCountry(userId: string, currentCountry: string): Promise<any[]> {
    const client = await this.pool.connect();

    try {
      const result = await client.query(`
        SELECT u.id, u.name, up.location
        FROM users u
        JOIN user_profiles up ON u.id = up.user_id
        WHERE u.id != $1 AND up.location->>'country' != $2
        ORDER BY RANDOM()
        LIMIT 5
      `, [userId, currentCountry]);

      return result.rows.map(row => ({
        id: row.id,
        name: row.name,
        location: row.location
      }));

    } finally {
      client.release();
    }
  }

  private async findUniqueExpertise(userId: string): Promise<any[]> {
    const userProfile = await this.getUserProfile(userId);
    const userSkills = new Set(userProfile.expertiseAreas);

    const client = await this.pool.connect();

    try {
      const result = await client.query(`
        SELECT u.id, u.name, up.expertise_areas
        FROM users u
        JOIN user_profiles up ON u.id = up.user_id
        WHERE u.id != $1
        ORDER BY RANDOM()
        LIMIT 20
      `, [userId]);

      return result.rows
        .map(row => {
          const candidateSkills = row.expertise_areas;
          const uniqueSkills = candidateSkills.filter((skill: string) => !userSkills.has(skill));

          return {
            id: row.id,
            name: row.name,
            uniqueSkills
          };
        })
        .filter(candidate => candidate.uniqueSkills.length > 0)
        .slice(0, 5);

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
