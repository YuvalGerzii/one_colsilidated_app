/**
 * Tier-Aware Matching Engine
 *
 * Extends pure need-based matching with tier-aware filtering and validation.
 * Prevents inappropriate cross-tier connections while allowing exceptional value propositions.
 *
 * Key Features:
 * 1. Professional tier classification
 * 2. Value proposition assessment for cross-tier requests
 * 3. Gatekeeper validation (prevents junior → CEO spam)
 * 4. Enhanced bidirectional validation
 * 5. Contextual needs analysis
 * 6. Status-aware but merit-based matching
 */

import {
  Contact,
  Match,
  EnhancedMatch,
  MatchType,
  MatchReason,
  Priority,
  MatchStatus,
  ProfessionalTier,
  IntelligenceAnalysis,
  ConnectionPath,
  BidirectionalValidation,
  ContextualAlignment,
  ValueProposition
} from '../types';
import { NetworkMapper } from '../network/NetworkMapper';
import { IntelligenceEngine } from '../intelligence/IntelligenceEngine';
import { TierClassificationAgent } from '../agents/TierClassificationAgent';
import { ValuePropositionAgent } from '../agents/ValuePropositionAgent';
import { GatekeeperAgent } from '../agents/GatekeeperAgent';
import { ContextualNeedsAgent } from '../agents/ContextualNeedsAgent';
import { EnhancedBidirectionalValidationAgent } from '../agents/EnhancedBidirectionalValidationAgent';

interface TierAwareConfig {
  enableTierFiltering: boolean;
  maxTierGapWithoutValidation: number;
  minValuePropositionForCrossTier: number;
  requireGatekeeperForExecutivePlus: boolean;
  tierWeightInMatching: number;
  minMutualityScore: number;
  minOverallScore: number;
  maxNetworkDistance: number;
}

export class TierAwareMatchingEngine {
  private networkMapper: NetworkMapper;
  private intelligenceEngine: IntelligenceEngine;
  private tierClassifier: TierClassificationAgent;
  private valuePropositionAgent: ValuePropositionAgent;
  private gatekeeperAgent: GatekeeperAgent;
  private contextualNeedsAgent: ContextualNeedsAgent;
  private bidirectionalValidator: EnhancedBidirectionalValidationAgent;
  private matches: Map<string, EnhancedMatch>;
  private config: TierAwareConfig;

  // Enhanced score weights
  private readonly SCORE_WEIGHTS = {
    mutualNeeds: 0.45,           // 45% - Mutual needs satisfaction
    valueExchange: 0.25,         // 25% - Value quality
    bidirectionalBalance: 0.15,  // 15% - Bidirectional fairness
    contextualAlignment: 0.10,   // 10% - Context compatibility
    networkDistance: 0.05        // 5% - Reachability
  };

  constructor(
    networkMapper: NetworkMapper,
    intelligenceEngine: IntelligenceEngine,
    config?: Partial<TierAwareConfig>
  ) {
    this.networkMapper = networkMapper;
    this.intelligenceEngine = intelligenceEngine;
    this.tierClassifier = new TierClassificationAgent();
    this.valuePropositionAgent = new ValuePropositionAgent();
    this.gatekeeperAgent = new GatekeeperAgent();
    this.contextualNeedsAgent = new ContextualNeedsAgent();
    this.bidirectionalValidator = new EnhancedBidirectionalValidationAgent();
    this.matches = new Map();

    this.config = {
      enableTierFiltering: config?.enableTierFiltering ?? true,
      maxTierGapWithoutValidation: config?.maxTierGapWithoutValidation ?? 2,
      minValuePropositionForCrossTier: config?.minValuePropositionForCrossTier ?? 70,
      requireGatekeeperForExecutivePlus: config?.requireGatekeeperForExecutivePlus ?? true,
      tierWeightInMatching: config?.tierWeightInMatching ?? 0.15,
      minMutualityScore: config?.minMutualityScore ?? 60,
      minOverallScore: config?.minOverallScore ?? 70,
      maxNetworkDistance: config?.maxNetworkDistance ?? 4
    };
  }

  /**
   * Find tier-aware matches for a seeker
   */
  async findMatches(
    seeker: Contact,
    candidates: Contact[],
    maxResults: number = 50
  ): Promise<EnhancedMatch[]> {
    // Classify seeker's tier
    const seekerTierProfile = await this.tierClassifier.classifyTier(seeker);
    seeker.tierProfile = seekerTierProfile;

    // Analyze seeker's contextual needs
    const seekerContextualNeeds = await this.contextualNeedsAgent.analyzeAllNeeds(seeker);
    seeker.contextualNeeds = seekerContextualNeeds;

    const potentialMatches: EnhancedMatch[] = [];

    for (const candidate of candidates) {
      try {
        // Classify candidate's tier
        const candidateTierProfile = await this.tierClassifier.classifyTier(candidate);
        candidate.tierProfile = candidateTierProfile;

        // Analyze candidate's contextual needs
        const candidateContextualNeeds = await this.contextualNeedsAgent.analyzeAllNeeds(candidate);
        candidate.contextualNeeds = candidateContextualNeeds;

        // Calculate tier gap
        const tierGap = this.tierClassifier.getTierGap(
          seekerTierProfile.tier,
          candidateTierProfile.tier
        );

        // Check if appropriate direct contact (tier filtering)
        const appropriateMatch = this.tierClassifier.isAppropriateDirectContact(
          seekerTierProfile.tier,
          candidateTierProfile.tier,
          this.config.maxTierGapWithoutValidation
        );

        // Determine if gatekeeper is required
        const requiresGatekeeper = this.requiresGatekeeperValidation(
          seekerTierProfile.tier,
          candidateTierProfile.tier,
          tierGap
        );

        // If tier filtering enabled and inappropriate, assess value proposition
        let valueProposition: ValueProposition | undefined;
        let gatekeeperPassed = true;

        if (this.config.enableTierFiltering && !appropriateMatch) {
          // Assess value proposition
          valueProposition = await this.valuePropositionAgent.assessValueProposition(
            seeker,
            candidate,
            seekerTierProfile.tier,
            candidateTierProfile.tier
          );

          // If gatekeeper required, validate
          if (requiresGatekeeper) {
            const gatekeeperValidation = await this.gatekeeperAgent.validateAccess(
              seeker,
              candidate,
              seekerTierProfile.tier,
              candidateTierProfile.tier,
              valueProposition,
              tierGap
            );

            gatekeeperPassed = gatekeeperValidation.passed;

            // Skip this match if gatekeeper rejects
            if (!gatekeeperPassed) {
              console.log(`Gatekeeper rejected ${seeker.name} → ${candidate.name}: ${gatekeeperValidation.recommendation}`);
              continue;
            }
          }
        }

        // Perform enhanced bidirectional validation
        const bidirectionalValidation = await this.bidirectionalValidator.validateWithContextualNeeds(
          seeker,
          candidate,
          seekerContextualNeeds,
          candidateContextualNeeds,
          seekerTierProfile.tier,
          candidateTierProfile.tier
        );

        // Check if passes bidirectional validation
        if (!this.bidirectionalValidator.passesValidation(bidirectionalValidation, this.config.minMutualityScore)) {
          console.log(`Bidirectional validation failed for ${seeker.name} → ${candidate.name} (mutuality: ${bidirectionalValidation.mutualityScore})`);
          continue;
        }

        // Calculate contextual alignment
        const contextualAlignment = this.calculateContextualAlignment(
          seekerContextualNeeds,
          candidateContextualNeeds,
          seeker,
          candidate
        );

        // Analyze intelligence for both
        const seekerAnalysis = await this.intelligenceEngine.analyzeContact(seeker);
        const candidateAnalysis = await this.intelligenceEngine.analyzeContact(candidate);

        // Find connection paths
        const paths = this.networkMapper.findConnectionPaths(seeker.id, candidate.id, this.config.maxNetworkDistance);
        if (paths.length === 0) {
          continue; // Skip if not reachable
        }

        // Calculate mutual needs score
        const mutualNeedsScore = this.calculateMutualNeedsScore(seeker, candidate);

        // Calculate value exchange
        const valueExchangeScore = this.calculateValueExchange(seeker, candidate);

        // Calculate network distance score
        const networkScore = this.calculateNetworkScore(paths[0].contacts.length);

        // Calculate overall score
        const overallScore =
          mutualNeedsScore * this.SCORE_WEIGHTS.mutualNeeds +
          valueExchangeScore * this.SCORE_WEIGHTS.valueExchange +
          (bidirectionalValidation.balanceRatio * 100) * this.SCORE_WEIGHTS.bidirectionalBalance +
          contextualAlignment.overallAlignment * this.SCORE_WEIGHTS.contextualAlignment +
          networkScore * this.SCORE_WEIGHTS.networkDistance;

        // Filter by minimum quality
        if (overallScore < this.config.minOverallScore) {
          continue;
        }

        // Generate match reasons
        const reasons = this.generateMatchReasons(
          seeker,
          candidate,
          bidirectionalValidation,
          contextualAlignment,
          mutualNeedsScore
        );

        // Determine priority
        const priority = this.determinePriority(
          overallScore,
          bidirectionalValidation,
          contextualAlignment,
          seekerContextualNeeds
        );

        // Create enhanced match
        const match: EnhancedMatch = {
          id: `${seeker.id}-${candidate.id}-${Date.now()}`,
          targetContact: candidate,
          sourceContact: seeker,
          matchType: this.determineMatchType(seeker, candidate),
          compatibilityScore: overallScore / 100,
          valuePotential: valueExchangeScore / 100,
          successProbability: (mutualNeedsScore / 100) * (bidirectionalValidation.balanceRatio),
          overallScore: overallScore / 100,
          connectionPaths: paths,
          shortestPath: paths[0],
          reasons,
          priority,
          timestamp: new Date(),
          status: MatchStatus.NEW,
          tierAnalysis: {
            seekerTier: seekerTierProfile.tier,
            targetTier: candidateTierProfile.tier,
            tierGap,
            appropriateMatch: appropriateMatch || gatekeeperPassed,
            requiresGatekeeper
          },
          valueProposition,
          gatekeeperValidation: requiresGatekeeper && valueProposition
            ? await this.gatekeeperAgent.validateAccess(seeker, candidate, seekerTierProfile.tier, candidateTierProfile.tier, valueProposition, tierGap)
            : undefined,
          bidirectionalValidation,
          contextualAlignment
        };

        potentialMatches.push(match);

      } catch (error) {
        console.error(`Error processing candidate ${candidate.name}:`, error);
        continue;
      }
    }

    // Sort by overall score
    potentialMatches.sort((a, b) => b.overallScore - a.overallScore);

    // Return top matches
    return potentialMatches.slice(0, maxResults);
  }

  /**
   * Determine if gatekeeper validation is required
   */
  private requiresGatekeeperValidation(
    seekerTier: ProfessionalTier,
    targetTier: ProfessionalTier,
    tierGap: number
  ): boolean {
    // Always require for large gaps
    if (tierGap > this.config.maxTierGapWithoutValidation) {
      return true;
    }

    // Require for executive and above
    if (this.config.requireGatekeeperForExecutivePlus) {
      const executiveTiers = [
        ProfessionalTier.EXECUTIVE,
        ProfessionalTier.C_LEVEL,
        ProfessionalTier.FOUNDER_CEO,
        ProfessionalTier.LUMINARY
      ];
      return executiveTiers.includes(targetTier);
    }

    return false;
  }

  /**
   * Calculate mutual needs satisfaction score
   */
  private calculateMutualNeedsScore(seeker: Contact, target: Contact): number {
    const seekerNeeds = seeker.needs || [];
    const targetNeeds = target.needs || [];
    const seekerOfferings = seeker.offerings || [];
    const targetOfferings = target.offerings || [];

    if (seekerNeeds.length === 0 && targetNeeds.length === 0) {
      return 50; // No explicit needs
    }

    let seekerSatisfaction = 0;
    let targetSatisfaction = 0;

    // How well target satisfies seeker's needs
    for (const need of seekerNeeds) {
      for (const offering of targetOfferings) {
        const similarity = this.semanticSimilarity(need.toLowerCase(), offering.toLowerCase());
        if (similarity > 0.3) {
          seekerSatisfaction += similarity * 100;
        }
      }
    }

    // How well seeker satisfies target's needs
    for (const need of targetNeeds) {
      for (const offering of seekerOfferings) {
        const similarity = this.semanticSimilarity(need.toLowerCase(), offering.toLowerCase());
        if (similarity > 0.3) {
          targetSatisfaction += similarity * 100;
        }
      }
    }

    const avgSeekerSat = seekerNeeds.length > 0 ? seekerSatisfaction / seekerNeeds.length : 50;
    const avgTargetSat = targetNeeds.length > 0 ? targetSatisfaction / targetNeeds.length : 50;

    // Mutual score is minimum (both must benefit)
    return Math.min(avgSeekerSat, avgTargetSat);
  }

  /**
   * Calculate value exchange score
   */
  private calculateValueExchange(seeker: Contact, target: Contact): number {
    let score = 50; // Base score

    // Skills complementarity
    const seekerSkills = new Set((seeker.skills || []).map(s => s.toLowerCase()));
    const targetSkills = new Set((target.skills || []).map(s => s.toLowerCase()));

    const uniqueToSeeker = [...seekerSkills].filter(s => !targetSkills.has(s)).length;
    const uniqueToTarget = [...targetSkills].filter(s => !seekerSkills.has(s)).length;

    // More unique skills = higher value exchange potential
    score += Math.min((uniqueToSeeker + uniqueToTarget) * 2, 30);

    // Industry diversity bonus
    if (seeker.industry && target.industry && seeker.industry !== target.industry) {
      score += 10;
    }

    // Both have substantial profiles
    if ((seeker.offerings || []).length > 0 && (target.offerings || []).length > 0) {
      score += 10;
    }

    return Math.min(100, score);
  }

  /**
   * Calculate contextual alignment
   */
  private calculateContextualAlignment(
    seekerNeeds: any[],
    candidateNeeds: any[],
    seeker: Contact,
    candidate: Contact
  ): ContextualAlignment {
    // If no contextual needs, use simpler alignment
    if (seekerNeeds.length === 0 && candidateNeeds.length === 0) {
      return {
        needsAlignment: 50,
        urgencyAlignment: 50,
        scopeAlignment: 50,
        resourceAlignment: 50,
        timingAlignment: 50,
        domainAlignment: 50,
        overallAlignment: 50
      };
    }

    let needsAlignment = 0;
    let urgencyAlignment = 0;
    let scopeAlignment = 0;
    let resourceAlignment = 50; // Default moderate
    let timingAlignment = 0;
    let domainAlignment = 0;

    // Calculate alignment scores
    if (seekerNeeds.length > 0 && candidateNeeds.length > 0) {
      for (const sn of seekerNeeds) {
        for (const cn of candidateNeeds) {
          needsAlignment = Math.max(needsAlignment, this.contextualNeedsAgent.calculateNeedsAlignment(sn, cn));
        }
      }
    }

    // Calculate domain alignment
    const seekerDomains = new Set(seekerNeeds.flatMap((n: any) => n.relatedDomains || []));
    const candidateDomains = new Set(candidateNeeds.flatMap((n: any) => n.relatedDomains || []));
    const candidateSkills = new Set((candidate.skills || []).map(s => s.toLowerCase()));
    const seekerSkills = new Set((seeker.skills || []).map(s => s.toLowerCase()));

    let domainMatches = 0;
    for (const domain of seekerDomains) {
      if (candidateDomains.has(domain)) domainMatches++;
    }
    domainAlignment = seekerDomains.size > 0 ? (domainMatches / seekerDomains.size) * 100 : 50;

    const overallAlignment =
      needsAlignment * 0.30 +
      urgencyAlignment * 0.15 +
      scopeAlignment * 0.15 +
      resourceAlignment * 0.15 +
      timingAlignment * 0.10 +
      domainAlignment * 0.15;

    return {
      needsAlignment,
      urgencyAlignment,
      scopeAlignment,
      resourceAlignment,
      timingAlignment,
      domainAlignment,
      overallAlignment
    };
  }

  /**
   * Calculate network distance score
   */
  private calculateNetworkScore(pathLength: number): number {
    // Closer is better
    if (pathLength === 1) return 100; // Direct connection
    if (pathLength === 2) return 90;  // 1 degree
    if (pathLength === 3) return 70;  // 2 degrees
    if (pathLength === 4) return 50;  // 3 degrees
    return 30; // 4+ degrees
  }

  /**
   * Generate match reasons
   */
  private generateMatchReasons(
    seeker: Contact,
    candidate: Contact,
    bidirectionalValidation: BidirectionalValidation,
    contextualAlignment: ContextualAlignment,
    mutualNeedsScore: number
  ): MatchReason[] {
    const reasons: MatchReason[] = [];

    // Needs satisfaction
    if (bidirectionalValidation.seekerNeeds.length > 0) {
      reasons.push({
        type: 'needs_satisfaction',
        description: `Can help with: ${bidirectionalValidation.seekerNeeds.join(', ')}`,
        score: bidirectionalValidation.seekerBenefit / 100,
        evidence: bidirectionalValidation.seekerNeeds
      });
    }

    // Mutual benefit
    if (bidirectionalValidation.targetNeeds.length > 0) {
      reasons.push({
        type: 'mutual_benefit',
        description: `You can help with: ${bidirectionalValidation.targetNeeds.join(', ')}`,
        score: bidirectionalValidation.targetBenefit / 100,
        evidence: bidirectionalValidation.targetNeeds
      });
    }

    // Contextual alignment
    if (contextualAlignment.domainAlignment > 60) {
      reasons.push({
        type: 'domain_expertise',
        description: 'Strong domain expertise alignment',
        score: contextualAlignment.domainAlignment / 100,
        evidence: ['Matching professional domains']
      });
    }

    // Balance
    if (bidirectionalValidation.balanceRatio > 0.8) {
      reasons.push({
        type: 'balanced_exchange',
        description: 'Well-balanced mutual value exchange',
        score: bidirectionalValidation.balanceRatio,
        evidence: [`Balance ratio: ${(bidirectionalValidation.balanceRatio * 100).toFixed(0)}%`]
      });
    }

    return reasons;
  }

  /**
   * Determine match priority
   */
  private determinePriority(
    overallScore: number,
    bidirectionalValidation: BidirectionalValidation,
    contextualAlignment: ContextualAlignment,
    seekerNeeds: any[]
  ): Priority {
    // Critical priority for exceptional matches with critical needs
    const hasCriticalNeeds = seekerNeeds.some(n => n.importance === 'critical' || n.urgency === 'critical');
    if (overallScore >= 85 && hasCriticalNeeds) {
      return Priority.CRITICAL;
    }

    // High priority for strong matches
    if (overallScore >= 80 || (overallScore >= 75 && bidirectionalValidation.mutualityScore >= 75)) {
      return Priority.HIGH;
    }

    // Medium priority for good matches
    if (overallScore >= 70) {
      return Priority.MEDIUM;
    }

    return Priority.LOW;
  }

  /**
   * Determine match type
   */
  private determineMatchType(seeker: Contact, candidate: Contact): MatchType {
    const seekerNeeds = (seeker.needs || []).join(' ').toLowerCase();
    const candidateOfferings = (candidate.offerings || []).join(' ').toLowerCase();

    if (seekerNeeds.match(/business|partnership|investment/)) {
      return MatchType.BUSINESS_OPPORTUNITY;
    }

    if (seekerNeeds.match(/knowledge|learn|mentor/)) {
      return MatchType.KNOWLEDGE_EXCHANGE;
    }

    if (seekerNeeds.match(/collaborate|project|work together/)) {
      return MatchType.COLLABORATION;
    }

    return MatchType.COMPLEMENTARY_NEEDS;
  }

  /**
   * Semantic similarity helper
   */
  private semanticSimilarity(text1: string, text2: string): number {
    const words1 = new Set(text1.split(/\s+/));
    const words2 = new Set(text2.split(/\s+/));

    const intersection = new Set([...words1].filter(w => words2.has(w)));
    const union = new Set([...words1, ...words2]);

    return union.size > 0 ? intersection.size / union.size : 0;
  }
}
