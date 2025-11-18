/**
 * Improved Pure Need-Based Matching Engine
 *
 * Focuses PURELY on complementary needs and mutual value exchange.
 * Eliminates status biases, influence scoring, and forced connections.
 *
 * Key Principles:
 * 1. Both parties must have needs satisfied (bidirectional matching)
 * 2. No bonuses for titles, influence, or status
 * 3. Higher quality thresholds
 * 4. Semantic need/offering matching
 * 5. Balanced value exchange
 */

import {
  Contact,
  Match,
  MatchType,
  MatchReason,
  Priority,
  MatchStatus,
  IntelligenceAnalysis,
  ConnectionPath
} from '../types';
import { NetworkMapper } from '../network/NetworkMapper';
import { IntelligenceEngine } from '../intelligence/IntelligenceEngine';

interface MutualNeedSatisfaction {
  userAScore: number;      // How well A's needs are met by B
  userBScore: number;      // How well B's needs are met by A
  mutuality: number;       // Minimum of both (both must benefit)
  balance: number;         // How balanced the exchange is
  userAMatches: Array<{ need: string; offering: string; score: number }>;
  userBMatches: Array<{ need: string; offering: string; score: number }>;
}

interface ValueExchange {
  aToB: number;           // Value A provides to B
  bToA: number;           // Value B provides to A
  mutual: number;         // Average mutual value
  fairness: number;       // How fair/balanced is the exchange
}

interface MatchQualityMetrics {
  hasBidirectionalNeeds: boolean;
  hasSubstantiveReasons: boolean;
  meetsCriticalNeeds: boolean;
  isBalanced: boolean;
  qualityScore: number;
}

export class ImprovedMatchingEngine {
  private networkMapper: NetworkMapper;
  private intelligenceEngine: IntelligenceEngine;
  private matches: Map<string, Match>;
  private config: {
    minMutualNeedScore: number;
    minBidirectionalScore: number;
    minOverallScore: number;
    requireSubstantiveReasons: boolean;
    requireBidirectional: boolean;
    maxNetworkDistance: number;
  };

  // Pure need-based weights (NO status biases)
  private readonly SCORE_WEIGHTS = {
    mutualNeeds: 0.50,        // 50% - Both parties' needs satisfaction
    valueExchange: 0.30,      // 30% - Quality of value exchanged
    balance: 0.15,            // 15% - Fairness/balance of exchange
    networkDistance: 0.05     // 5% - Reachability (minimal weight)
  };

  constructor(
    networkMapper: NetworkMapper,
    intelligenceEngine: IntelligenceEngine,
    config?: {
      minMutualNeedScore?: number;
      minBidirectionalScore?: number;
      minOverallScore?: number;
      requireSubstantiveReasons?: boolean;
      requireBidirectional?: boolean;
      maxNetworkDistance?: number;
    }
  ) {
    this.networkMapper = networkMapper;
    this.intelligenceEngine = intelligenceEngine;
    this.matches = new Map();
    this.config = {
      minMutualNeedScore: config?.minMutualNeedScore ?? 0.5,
      minBidirectionalScore: config?.minBidirectionalScore ?? 0.6,
      minOverallScore: config?.minOverallScore ?? 0.70,  // Raised from 0.6
      requireSubstantiveReasons: config?.requireSubstantiveReasons ?? true,
      requireBidirectional: config?.requireBidirectional ?? true,
      maxNetworkDistance: config?.maxNetworkDistance ?? 4  // Closer connections
    };
  }

  /**
   * Find all pure need-based matches for a contact
   */
  async findMatches(sourceContact: Contact): Promise<Match[]> {
    const sourceAnalysis = await this.intelligenceEngine.analyzeContact(sourceContact);
    const allContacts = this.networkMapper.getAllContacts();
    const potentialMatches: Match[] = [];

    for (const targetContact of allContacts) {
      // Skip self
      if (targetContact.id === sourceContact.id) continue;

      // Skip if already directly connected
      const directConnections = this.networkMapper.getDirectContacts(sourceContact.id);
      if (directConnections.some(c => c.id === targetContact.id)) continue;

      const match = await this.evaluateMatch(sourceContact, sourceAnalysis, targetContact);

      if (match && this.meetsQualityThresholds(match)) {
        potentialMatches.push(match);
      }
    }

    // Sort by overall score
    potentialMatches.sort((a, b) => b.overallScore - a.overallScore);

    // Store matches
    potentialMatches.forEach(m => this.matches.set(m.id, m));

    return potentialMatches;
  }

  /**
   * Find matches for all contacts in the network
   */
  async findAllMatches(): Promise<Match[]> {
    const allContacts = this.networkMapper.getAllContacts();
    const allMatches: Match[] = [];

    for (const contact of allContacts) {
      const matches = await this.findMatches(contact);
      allMatches.push(...matches);
    }

    // Remove duplicates (A->B and B->A are the same match)
    const uniqueMatches = this.deduplicateMatches(allMatches);

    return uniqueMatches.sort((a, b) => b.overallScore - a.overallScore);
  }

  /**
   * Evaluate a potential match using pure need-based criteria
   */
  private async evaluateMatch(
    sourceContact: Contact,
    sourceAnalysis: IntelligenceAnalysis,
    targetContact: Contact
  ): Promise<Match | null> {
    const targetAnalysis = await this.intelligenceEngine.analyzeContact(targetContact);

    // Find connection paths
    const connectionPaths = this.networkMapper.findConnectionPaths(
      sourceContact.id,
      targetContact.id,
      this.config.maxNetworkDistance
    );

    if (connectionPaths.length === 0) {
      return null; // No reachable connection path
    }

    const shortestPath = connectionPaths[0];

    // Calculate mutual need satisfaction (CORE METRIC)
    const mutualNeeds = this.calculateMutualNeedSatisfaction(
      sourceContact,
      sourceAnalysis,
      targetContact,
      targetAnalysis
    );

    // Early exit if needs aren't mutually satisfied
    if (mutualNeeds.mutuality < this.config.minMutualNeedScore) {
      return null;
    }

    // Calculate value exchange
    const valueExchange = this.calculateValueExchange(
      sourceContact,
      sourceAnalysis,
      targetContact,
      targetAnalysis,
      mutualNeeds
    );

    // Calculate overall score (pure need-based)
    const overallScore = this.calculatePureNeedBasedScore(
      mutualNeeds,
      valueExchange,
      shortestPath.totalStrength
    );

    // Determine match types and reasons (without bias)
    const { matchTypes, reasons } = this.identifyPureMatchReasons(
      sourceContact,
      sourceAnalysis,
      targetContact,
      targetAnalysis,
      mutualNeeds
    );

    if (matchTypes.length === 0) {
      return null;
    }

    // Calculate compatibility for backward compatibility
    const compatibility = this.intelligenceEngine.calculateCompatibility(
      sourceContact,
      sourceAnalysis,
      targetContact,
      targetAnalysis
    );

    // Calculate success probability
    const successProbability = this.intelligenceEngine.predictSuccessProbability(
      sourceContact,
      sourceAnalysis,
      targetContact,
      targetAnalysis,
      shortestPath.totalStrength
    );

    // Determine priority based on mutual benefit (not status)
    const priority = this.determinePureNeedBasedPriority(
      mutualNeeds,
      valueExchange,
      matchTypes
    );

    const match: Match = {
      id: `${sourceContact.id}-${targetContact.id}-${Date.now()}`,
      sourceContact,
      targetContact,
      matchType: matchTypes[0],
      compatibilityScore: compatibility.score,
      valuePotential: valueExchange.mutual,  // Pure value, no status bonus
      successProbability,
      overallScore,
      connectionPaths,
      shortestPath,
      reasons,
      priority,
      timestamp: new Date(),
      status: MatchStatus.NEW,
      // Additional metadata for transparency
      metadata: {
        mutualNeedsScore: mutualNeeds.mutuality,
        balanceScore: mutualNeeds.balance,
        bidirectional: mutualNeeds.mutuality >= this.config.minBidirectionalScore,
        userABenefit: mutualNeeds.userAScore,
        userBBenefit: mutualNeeds.userBScore
      }
    };

    return match;
  }

  /**
   * Calculate mutual need satisfaction (CORE PURE METRIC)
   * Both parties must have needs satisfied for a high score
   */
  private calculateMutualNeedSatisfaction(
    userA: Contact,
    analysisA: IntelligenceAnalysis,
    userB: Contact,
    analysisB: IntelligenceAnalysis
  ): MutualNeedSatisfaction {
    // A's needs vs B's offerings
    const aMatches = this.matchNeedsToOfferings(
      analysisA.needsAnalysis,
      analysisB.offeringsAnalysis
    );

    // B's needs vs A's offerings
    const bMatches = this.matchNeedsToOfferings(
      analysisB.needsAnalysis,
      analysisA.offeringsAnalysis
    );

    // Calculate scores
    const userAScore = this.calculateNeedSatisfactionScore(aMatches, analysisA.needsAnalysis);
    const userBScore = this.calculateNeedSatisfactionScore(bMatches, analysisB.needsAnalysis);

    // Mutuality = minimum (both must benefit)
    const mutuality = Math.min(userAScore, userBScore);

    // Balance = how even the exchange is (1 = perfectly balanced)
    const balance = 1 - Math.abs(userAScore - userBScore);

    return {
      userAScore,
      userBScore,
      mutuality,
      balance,
      userAMatches: aMatches,
      userBMatches: bMatches
    };
  }

  /**
   * Match needs to offerings using semantic similarity
   */
  private matchNeedsToOfferings(
    needsAnalysis: IntelligenceAnalysis['needsAnalysis'],
    offeringsAnalysis: IntelligenceAnalysis['offeringsAnalysis']
  ): Array<{ need: string; offering: string; score: number }> {
    const matches: Array<{ need: string; offering: string; score: number }> = [];

    const allNeeds = [
      ...needsAnalysis.explicit,
      ...needsAnalysis.implicit.slice(0, 3) // Include top implicit needs
    ];

    const allOfferings = [
      ...offeringsAnalysis.explicit,
      ...offeringsAnalysis.implicit.slice(0, 3)
    ];

    for (const need of allNeeds) {
      for (const offering of allOfferings) {
        const score = this.calculateSemanticSimilarity(need, offering);

        if (score > 0.3) {  // Threshold for considering a match
          matches.push({ need, offering, score });
        }
      }
    }

    return matches;
  }

  /**
   * Calculate semantic similarity between need and offering
   * (Simplified - in production would use NLP/embeddings)
   */
  private calculateSemanticSimilarity(need: string, offering: string): number {
    const needLower = need.toLowerCase();
    const offeringLower = offering.toLowerCase();

    // Extract key words
    const needWords = needLower.split(/\s+/).filter(w => w.length > 3);
    const offeringWords = offeringLower.split(/\s+/).filter(w => w.length > 3);

    if (needWords.length === 0 || offeringWords.length === 0) return 0;

    // Calculate word overlap
    let matchCount = 0;
    let totalWeight = 0;

    for (const needWord of needWords) {
      for (const offeringWord of offeringWords) {
        if (needWord === offeringWord) {
          matchCount += 1;
          totalWeight += 1;
        } else if (needWord.includes(offeringWord) || offeringWord.includes(needWord)) {
          matchCount += 0.5;
          totalWeight += 0.5;
        }
      }
    }

    // Normalize by total words
    const score = totalWeight / Math.max(needWords.length, offeringWords.length);

    // Exact phrase match bonus
    if (needLower.includes(offeringLower) || offeringLower.includes(needLower)) {
      return Math.min(1.0, score + 0.3);
    }

    return Math.min(1.0, score);
  }

  /**
   * Calculate need satisfaction score from matches
   */
  private calculateNeedSatisfactionScore(
    matches: Array<{ need: string; offering: string; score: number }>,
    needsAnalysis: IntelligenceAnalysis['needsAnalysis']
  ): number {
    if (matches.length === 0) return 0;

    const totalNeeds = needsAnalysis.explicit.length + Math.min(3, needsAnalysis.implicit.length);

    if (totalNeeds === 0) return 0;

    // Weight explicit needs more heavily
    const explicitNeeds = new Set(needsAnalysis.explicit);
    let satisfiedExplicit = 0;
    let satisfiedImplicit = 0;

    const needsSatisfied = new Set<string>();

    for (const match of matches) {
      needsSatisfied.add(match.need);

      if (explicitNeeds.has(match.need)) {
        satisfiedExplicit += match.score;
      } else {
        satisfiedImplicit += match.score;
      }
    }

    // Weighted score: 70% explicit, 30% implicit
    const explicitScore = needsAnalysis.explicit.length > 0
      ? satisfiedExplicit / needsAnalysis.explicit.length
      : 0;

    const implicitScore = needsAnalysis.implicit.length > 0
      ? satisfiedImplicit / Math.min(3, needsAnalysis.implicit.length)
      : 0;

    return (explicitScore * 0.7 + implicitScore * 0.3);
  }

  /**
   * Calculate value exchange (NO STATUS BIASES)
   */
  private calculateValueExchange(
    userA: Contact,
    analysisA: IntelligenceAnalysis,
    userB: Contact,
    analysisB: IntelligenceAnalysis,
    mutualNeeds: MutualNeedSatisfaction
  ): ValueExchange {
    // Value A provides to B
    const aToB = mutualNeeds.userBScore;  // How well A satisfies B's needs

    // Value B provides to A
    const bToA = mutualNeeds.userAScore;  // How well B satisfies A's needs

    // Mutual value (average)
    const mutual = (aToB + bToA) / 2;

    // Fairness (how balanced)
    const fairness = 1 - Math.abs(aToB - bToA);

    return {
      aToB,
      bToA,
      mutual,
      fairness
    };
  }

  /**
   * Calculate pure need-based score (NO BIASES)
   */
  private calculatePureNeedBasedScore(
    mutualNeeds: MutualNeedSatisfaction,
    valueExchange: ValueExchange,
    networkTrustScore: number
  ): number {
    const score = (
      mutualNeeds.mutuality * this.SCORE_WEIGHTS.mutualNeeds +
      valueExchange.mutual * this.SCORE_WEIGHTS.valueExchange +
      mutualNeeds.balance * this.SCORE_WEIGHTS.balance +
      networkTrustScore * this.SCORE_WEIGHTS.networkDistance
    );

    return Math.min(Math.max(score, 0), 1);
  }

  /**
   * Identify pure match reasons (without status bias)
   */
  private identifyPureMatchReasons(
    sourceContact: Contact,
    sourceAnalysis: IntelligenceAnalysis,
    targetContact: Contact,
    targetAnalysis: IntelligenceAnalysis,
    mutualNeeds: MutualNeedSatisfaction
  ): {
    matchTypes: MatchType[];
    reasons: MatchReason[];
  } {
    const matchTypes: MatchType[] = [];
    const reasons: MatchReason[] = [];

    // PURE complementary needs matching
    if (mutualNeeds.mutuality > 0.5) {
      matchTypes.push(MatchType.COMPLEMENTARY_NEEDS);

      const evidenceA = mutualNeeds.userAMatches.slice(0, 3).map(m =>
        `${sourceContact.name} needs "${m.need}", ${targetContact.name} offers "${m.offering}"`
      );

      const evidenceB = mutualNeeds.userBMatches.slice(0, 3).map(m =>
        `${targetContact.name} needs "${m.need}", ${sourceContact.name} offers "${m.offering}"`
      );

      reasons.push({
        type: 'complementary_needs',
        description: 'Strong mutual needs and offerings alignment',
        score: mutualNeeds.mutuality,
        evidence: [...evidenceA, ...evidenceB]
      });
    }

    // Skill matching (only if complementary)
    const compatibility = this.intelligenceEngine.calculateCompatibility(
      sourceContact,
      sourceAnalysis,
      targetContact,
      targetAnalysis
    );

    const expertiseScore = compatibility.dimensions.expertiseComplementarity;
    if (expertiseScore > 0.6) {
      matchTypes.push(MatchType.SKILL_MATCH);
      reasons.push({
        type: 'skill_match',
        description: 'Complementary expertise areas',
        score: expertiseScore,
        evidence: [`Expertise complementarity score: ${(expertiseScore * 100).toFixed(0)}%`]
      });
    }

    // Industry synergy (only as supporting reason)
    const industryScore = compatibility.dimensions.industryAlignment;
    if (industryScore > 0.7) {
      matchTypes.push(MatchType.INDUSTRY_SYNERGY);
      reasons.push({
        type: 'industry_synergy',
        description: 'Aligned industry interests',
        score: industryScore,
        evidence: [`Both operate in ${sourceContact.industry || 'related'} industry`]
      });
    }

    // Business opportunity (ONLY if mutual needs are met)
    if (mutualNeeds.mutuality > 0.6 &&
        mutualNeeds.userAMatches.length > 0 &&
        mutualNeeds.userBMatches.length > 0) {
      matchTypes.push(MatchType.BUSINESS_OPPORTUNITY);
      reasons.push({
        type: 'business_opportunity',
        description: 'Verified mutual business opportunity',
        score: mutualNeeds.mutuality,
        evidence: [
          `Mutual needs satisfaction: ${(mutualNeeds.mutuality * 100).toFixed(0)}%`,
          `Balance score: ${(mutualNeeds.balance * 100).toFixed(0)}%`
        ]
      });
    }

    return { matchTypes, reasons };
  }

  /**
   * Determine priority based on mutual benefit (NOT status)
   */
  private determinePureNeedBasedPriority(
    mutualNeeds: MutualNeedSatisfaction,
    valueExchange: ValueExchange,
    matchTypes: MatchType[]
  ): Priority {
    // Critical: High mutual satisfaction + high balance
    if (mutualNeeds.mutuality > 0.8 && mutualNeeds.balance > 0.8) {
      return Priority.CRITICAL;
    }

    // High: Good mutual satisfaction
    if (mutualNeeds.mutuality > 0.7) {
      return Priority.HIGH;
    }

    // Medium: Decent satisfaction
    if (mutualNeeds.mutuality > 0.6) {
      return Priority.MEDIUM;
    }

    // Low: Meets minimum threshold
    return Priority.LOW;
  }

  /**
   * Check if match meets quality thresholds
   */
  private meetsQualityThresholds(match: Match): boolean {
    const metrics = this.calculateQualityMetrics(match);

    // Must meet overall score threshold
    if (match.overallScore < this.config.minOverallScore) {
      return false;
    }

    // Must be bidirectional if required
    if (this.config.requireBidirectional && !metrics.hasBidirectionalNeeds) {
      return false;
    }

    // Must have substantive reasons if required
    if (this.config.requireSubstantiveReasons && !metrics.hasSubstantiveReasons) {
      return false;
    }

    // Must meet critical needs
    if (!metrics.meetsCriticalNeeds) {
      return false;
    }

    return true;
  }

  /**
   * Calculate quality metrics for a match
   */
  private calculateQualityMetrics(match: Match): MatchQualityMetrics {
    const metadata = match.metadata as any;

    const hasBidirectionalNeeds = metadata?.bidirectional ?? false;

    const substantiveTypes = ['complementary_needs', 'skill_match', 'business_opportunity'];
    const hasSubstantiveReasons = match.reasons.some(r =>
      substantiveTypes.includes(r.type) && r.score > 0.5
    );

    // Check if critical needs are addressed
    const meetsCriticalNeeds = match.reasons.some(r =>
      r.type === 'complementary_needs' && r.score > 0.6
    );

    const isBalanced = metadata?.balanceScore > 0.6;

    const qualityScore = (
      (hasBidirectionalNeeds ? 0.3 : 0) +
      (hasSubstantiveReasons ? 0.3 : 0) +
      (meetsCriticalNeeds ? 0.3 : 0) +
      (isBalanced ? 0.1 : 0)
    );

    return {
      hasBidirectionalNeeds,
      hasSubstantiveReasons,
      meetsCriticalNeeds,
      isBalanced,
      qualityScore
    };
  }

  /**
   * Deduplicate matches (A->B and B->A are the same)
   */
  private deduplicateMatches(matches: Match[]): Match[] {
    const seen = new Set<string>();
    const unique: Match[] = [];

    for (const match of matches) {
      const key1 = `${match.sourceContact.id}-${match.targetContact.id}`;
      const key2 = `${match.targetContact.id}-${match.sourceContact.id}`;

      if (!seen.has(key1) && !seen.has(key2)) {
        seen.add(key1);
        unique.push(match);
      }
    }

    return unique;
  }

  /**
   * Get match by ID
   */
  getMatch(matchId: string): Match | undefined {
    return this.matches.get(matchId);
  }

  /**
   * Get all matches
   */
  getAllMatches(): Match[] {
    return Array.from(this.matches.values());
  }

  /**
   * Get matches by priority
   */
  getMatchesByPriority(priority: Priority): Match[] {
    return Array.from(this.matches.values())
      .filter(m => m.priority === priority)
      .sort((a, b) => b.overallScore - a.overallScore);
  }

  /**
   * Get top matches
   */
  getTopMatches(limit: number = 10): Match[] {
    return Array.from(this.matches.values())
      .sort((a, b) => b.overallScore - a.overallScore)
      .slice(0, limit);
  }

  /**
   * Update match status
   */
  updateMatchStatus(matchId: string, status: MatchStatus): void {
    const match = this.matches.get(matchId);
    if (match) {
      match.status = status;
    }
  }

  /**
   * Get matches by status
   */
  getMatchesByStatus(status: MatchStatus): Match[] {
    return Array.from(this.matches.values())
      .filter(m => m.status === status);
  }
}
