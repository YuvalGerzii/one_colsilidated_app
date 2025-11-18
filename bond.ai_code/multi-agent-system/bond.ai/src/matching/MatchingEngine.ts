/**
 * Smart Matching Engine
 * Real-time opportunity alerts when matches emerge
 * Multi-dimensional compatibility scoring
 * Prioritization based on value potential and trust level
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

export class MatchingEngine {
  private networkMapper: NetworkMapper;
  private intelligenceEngine: IntelligenceEngine;
  private matches: Map<string, Match>;
  private config: {
    minCompatibilityScore: number;
    minSuccessProbability: number;
    enabledMatchTypes: Set<MatchType>;
    priorityWeights: {
      valuePotential: number;
      successProbability: number;
      trustLevel: number;
      timing: number;
    };
  };

  constructor(
    networkMapper: NetworkMapper,
    intelligenceEngine: IntelligenceEngine,
    config?: {
      minCompatibilityScore?: number;
      minSuccessProbability?: number;
      enabledMatchTypes?: MatchType[];
      priorityWeights?: {
        valuePotential: number;
        successProbability: number;
        trustLevel: number;
        timing: number;
      };
    }
  ) {
    this.networkMapper = networkMapper;
    this.intelligenceEngine = intelligenceEngine;
    this.matches = new Map();
    this.config = {
      minCompatibilityScore: config?.minCompatibilityScore ?? 0.6,
      minSuccessProbability: config?.minSuccessProbability ?? 0.5,
      enabledMatchTypes: new Set(config?.enabledMatchTypes ?? Object.values(MatchType)),
      priorityWeights: config?.priorityWeights ?? {
        valuePotential: 0.35,
        successProbability: 0.25,
        trustLevel: 0.25,
        timing: 0.15
      }
    };
  }

  /**
   * Find all potential matches for a contact
   */
  async findMatches(sourceContact: Contact): Promise<Match[]> {
    const sourceAnalysis = await this.intelligenceEngine.analyzeContact(sourceContact);
    const allContacts = this.networkMapper.getAllContacts();
    const potentialMatches: Match[] = [];

    for (const targetContact of allContacts) {
      // Skip self
      if (targetContact.id === sourceContact.id) continue;

      // Check if already connected directly
      const directConnections = this.networkMapper.getDirectContacts(sourceContact.id);
      if (directConnections.some(c => c.id === targetContact.id)) continue;

      const match = await this.evaluateMatch(sourceContact, sourceAnalysis, targetContact);

      if (match && this.meetsThresholds(match)) {
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
   * Evaluate a potential match between two contacts
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
      3
    );

    if (connectionPaths.length === 0) {
      return null; // No connection path found
    }

    const shortestPath = connectionPaths[0];

    // Calculate compatibility
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

    // Determine match types and reasons
    const { matchTypes, reasons } = this.identifyMatchTypesAndReasons(
      sourceContact,
      sourceAnalysis,
      targetContact,
      targetAnalysis,
      compatibility
    );

    if (matchTypes.length === 0) {
      return null; // No valid match types
    }

    // Calculate value potential
    const valuePotential = this.calculateValuePotential(
      sourceContact,
      sourceAnalysis,
      targetContact,
      targetAnalysis,
      matchTypes
    );

    // Calculate overall score
    const overallScore = this.calculateOverallScore(
      compatibility.score,
      valuePotential,
      successProbability,
      shortestPath.trustScore
    );

    // Determine priority
    const priority = this.determinePriority(overallScore, valuePotential, matchTypes);

    const match: Match = {
      id: `${sourceContact.id}-${targetContact.id}-${Date.now()}`,
      sourceContact,
      targetContact,
      matchType: matchTypes[0], // Primary match type
      compatibilityScore: compatibility.score,
      valuePotential,
      successProbability,
      overallScore,
      connectionPaths,
      shortestPath,
      reasons,
      priority,
      timestamp: new Date(),
      status: MatchStatus.NEW
    };

    return match;
  }

  /**
   * Identify match types and reasons
   */
  private identifyMatchTypesAndReasons(
    sourceContact: Contact,
    sourceAnalysis: IntelligenceAnalysis,
    targetContact: Contact,
    targetAnalysis: IntelligenceAnalysis,
    compatibility: any
  ): {
    matchTypes: MatchType[];
    reasons: MatchReason[];
  } {
    const matchTypes: MatchType[] = [];
    const reasons: MatchReason[] = [];

    // Complementary needs matching
    const needsScore = compatibility.dimensions.needsMatch;
    if (needsScore > 0.5 && this.config.enabledMatchTypes.has(MatchType.COMPLEMENTARY_NEEDS)) {
      matchTypes.push(MatchType.COMPLEMENTARY_NEEDS);
      reasons.push({
        type: 'complementary_needs',
        description: 'Complementary needs and offerings alignment',
        score: needsScore,
        evidence: this.getComplementaryNeedsEvidence(sourceAnalysis, targetAnalysis)
      });
    }

    // Skill matching
    const expertiseScore = compatibility.dimensions.expertiseComplementarity;
    if (expertiseScore > 0.6 && this.config.enabledMatchTypes.has(MatchType.SKILL_MATCH)) {
      matchTypes.push(MatchType.SKILL_MATCH);
      reasons.push({
        type: 'skill_match',
        description: 'Complementary expertise areas',
        score: expertiseScore,
        evidence: this.getExpertiseEvidence(sourceAnalysis, targetAnalysis)
      });
    }

    // Industry synergy
    const industryScore = compatibility.dimensions.industryAlignment;
    if (industryScore > 0.5 && this.config.enabledMatchTypes.has(MatchType.INDUSTRY_SYNERGY)) {
      matchTypes.push(MatchType.INDUSTRY_SYNERGY);
      reasons.push({
        type: 'industry_synergy',
        description: 'Aligned industry interests',
        score: industryScore,
        evidence: this.getIndustryEvidence(sourceAnalysis, targetAnalysis)
      });
    }

    // Mutual interests
    const interestScore = this.calculateInterestOverlap(sourceContact, targetContact);
    if (interestScore > 0.4 && this.config.enabledMatchTypes.has(MatchType.MUTUAL_INTEREST)) {
      matchTypes.push(MatchType.MUTUAL_INTEREST);
      reasons.push({
        type: 'mutual_interest',
        description: 'Shared interests and passions',
        score: interestScore,
        evidence: this.getInterestEvidence(sourceContact, targetContact)
      });
    }

    // Business opportunity
    if (this.detectBusinessOpportunity(sourceAnalysis, targetAnalysis) &&
        this.config.enabledMatchTypes.has(MatchType.BUSINESS_OPPORTUNITY)) {
      matchTypes.push(MatchType.BUSINESS_OPPORTUNITY);
      reasons.push({
        type: 'business_opportunity',
        description: 'Potential business collaboration opportunity',
        score: 0.8,
        evidence: ['Career stages and industries suggest partnership potential']
      });
    }

    return { matchTypes, reasons };
  }

  /**
   * Calculate value potential
   */
  private calculateValuePotential(
    sourceContact: Contact,
    sourceAnalysis: IntelligenceAnalysis,
    targetContact: Contact,
    targetAnalysis: IntelligenceAnalysis,
    matchTypes: MatchType[]
  ): number {
    let value = 0.5;

    // Adjust based on match types
    if (matchTypes.includes(MatchType.BUSINESS_OPPORTUNITY)) value += 0.2;
    if (matchTypes.includes(MatchType.COMPLEMENTARY_NEEDS)) value += 0.15;
    if (matchTypes.includes(MatchType.SKILL_MATCH)) value += 0.1;

    // Adjust based on influence scores
    const avgInfluence = (
      sourceAnalysis.profileAnalysis.influenceScore +
      targetAnalysis.profileAnalysis.influenceScore
    ) / 2;
    value += avgInfluence * 0.2;

    // Adjust based on career stages
    if (sourceAnalysis.profileAnalysis.careerStage === 'executive' ||
        targetAnalysis.profileAnalysis.careerStage === 'executive') {
      value += 0.15;
    }

    return Math.min(value, 1);
  }

  /**
   * Calculate overall match score
   */
  private calculateOverallScore(
    compatibilityScore: number,
    valuePotential: number,
    successProbability: number,
    trustLevel: number
  ): number {
    const weights = this.config.priorityWeights;

    const score = (
      valuePotential * weights.valuePotential +
      successProbability * weights.successProbability +
      trustLevel * weights.trustLevel +
      compatibilityScore * weights.timing
    );

    return Math.min(Math.max(score, 0), 1);
  }

  /**
   * Determine match priority
   */
  private determinePriority(
    overallScore: number,
    valuePotential: number,
    matchTypes: MatchType[]
  ): Priority {
    // Critical: High value business opportunities with high overall score
    if (overallScore > 0.8 && valuePotential > 0.8 &&
        matchTypes.includes(MatchType.BUSINESS_OPPORTUNITY)) {
      return Priority.CRITICAL;
    }

    // High: High overall score
    if (overallScore > 0.75) {
      return Priority.HIGH;
    }

    // Medium: Good overall score
    if (overallScore > 0.6) {
      return Priority.MEDIUM;
    }

    // Low: Acceptable score
    return Priority.LOW;
  }

  /**
   * Check if match meets thresholds
   */
  private meetsThresholds(match: Match): boolean {
    return (
      match.compatibilityScore >= this.config.minCompatibilityScore &&
      match.successProbability >= this.config.minSuccessProbability
    );
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
   * Helper: Get complementary needs evidence
   */
  private getComplementaryNeedsEvidence(
    analysis1: IntelligenceAnalysis,
    analysis2: IntelligenceAnalysis
  ): string[] {
    const evidence: string[] = [];

    const needs1 = [...analysis1.needsAnalysis.explicit, ...analysis1.needsAnalysis.implicit];
    const offerings2 = [...analysis2.offeringsAnalysis.explicit, ...analysis2.offeringsAnalysis.implicit];

    for (const need of needs1.slice(0, 3)) {
      for (const offering of offerings2) {
        if (need.toLowerCase().includes(offering.toLowerCase()) ||
            offering.toLowerCase().includes(need.toLowerCase())) {
          evidence.push(`Need "${need}" matches offering "${offering}"`);
          break;
        }
      }
    }

    return evidence;
  }

  /**
   * Helper: Get expertise evidence
   */
  private getExpertiseEvidence(
    analysis1: IntelligenceAnalysis,
    analysis2: IntelligenceAnalysis
  ): string[] {
    const expertise1 = analysis1.profileAnalysis.expertiseAreas;
    const expertise2 = analysis2.profileAnalysis.expertiseAreas;

    const overlap = expertise1.filter(e1 => expertise2.includes(e1));
    const unique = [...expertise1, ...expertise2].filter(e =>
      !overlap.includes(e)
    );

    return [
      `Common expertise: ${overlap.slice(0, 3).join(', ')}`,
      `Complementary skills: ${unique.slice(0, 3).join(', ')}`
    ];
  }

  /**
   * Helper: Get industry evidence
   */
  private getIndustryEvidence(
    analysis1: IntelligenceAnalysis,
    analysis2: IntelligenceAnalysis
  ): string[] {
    const industries1 = analysis1.profileAnalysis.industries;
    const industries2 = analysis2.profileAnalysis.industries;

    const common = industries1.filter(i => industries2.includes(i));

    return common.length > 0
      ? [`Shared industries: ${common.join(', ')}`]
      : ['Related industry sectors'];
  }

  /**
   * Helper: Calculate interest overlap
   */
  private calculateInterestOverlap(contact1: Contact, contact2: Contact): number {
    const interests1 = new Set(contact1.interests || []);
    const interests2 = new Set(contact2.interests || []);

    if (interests1.size === 0 || interests2.size === 0) return 0;

    const intersection = new Set([...interests1].filter(x => interests2.has(x)));
    const union = new Set([...interests1, ...interests2]);

    return intersection.size / union.size;
  }

  /**
   * Helper: Get interest evidence
   */
  private getInterestEvidence(contact1: Contact, contact2: Contact): string[] {
    const interests1 = new Set(contact1.interests || []);
    const interests2 = new Set(contact2.interests || []);

    const common = [...interests1].filter(i => interests2.has(i));

    return common.length > 0
      ? [`Shared interests: ${common.slice(0, 3).join(', ')}`]
      : [];
  }

  /**
   * Helper: Detect business opportunity
   */
  private detectBusinessOpportunity(
    analysis1: IntelligenceAnalysis,
    analysis2: IntelligenceAnalysis
  ): boolean {
    // Simple heuristic: executive + complementary needs = opportunity
    const hasExecutive = (
      analysis1.profileAnalysis.careerStage === 'executive' ||
      analysis2.profileAnalysis.careerStage === 'executive'
    );

    const hasNeeds = (
      analysis1.needsAnalysis.explicit.length > 0 ||
      analysis2.needsAnalysis.explicit.length > 0
    );

    return hasExecutive && hasNeeds;
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
   * Get matches by status
   */
  getMatchesByStatus(status: MatchStatus): Match[] {
    return Array.from(this.matches.values())
      .filter(m => m.status === status);
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
   * Get top matches
   */
  getTopMatches(limit: number = 10): Match[] {
    return Array.from(this.matches.values())
      .sort((a, b) => b.overallScore - a.overallScore)
      .slice(0, limit);
  }
}
