/**
 * Gatekeeper Agent
 * Validates cross-tier access requests and prevents inappropriate connections
 * Ensures juniors don't spam executives unless they have exceptional value
 */

import {
  Contact,
  ProfessionalTier,
  ValueProposition,
  GatekeeperValidation,
  CrossTierAccessRequest,
  AgentType,
  AgentCapability
} from '../types';

export class GatekeeperAgent {
  private agentType = AgentType.EVALUATOR;
  private capabilities = [AgentCapability.EVALUATE, AgentCapability.ANALYZE];

  /**
   * Validate a cross-tier access request
   */
  async validateAccess(
    requester: Contact,
    target: Contact,
    requesterTier: ProfessionalTier,
    targetTier: ProfessionalTier,
    valueProposition: ValueProposition,
    tierGap: number
  ): Promise<GatekeeperValidation> {
    // Determine required threshold based on tier gap
    const requiredThreshold = this.calculateRequiredThreshold(
      requesterTier,
      targetTier,
      tierGap
    );

    // Perform comprehensive checks
    const checks = {
      valuePropositionStrength: valueProposition.strength,
      specificity: valueProposition.specificity,
      relevance: this.assessRelevance(valueProposition, target),
      professionalism: this.assessProfessionalism(requester, valueProposition),
      mutualBenefit: this.assessMutualBenefit(requester, target, valueProposition),
      verification: valueProposition.verifiability
    };

    // Calculate overall gatekeeper score
    const score = this.calculateGatekeeperScore(checks, tierGap);

    // Determine if request passes
    const passed = score >= requiredThreshold;

    // Generate recommendation and warnings
    const recommendation = this.generateRecommendation(
      passed,
      score,
      requiredThreshold,
      checks,
      tierGap,
      requesterTier,
      targetTier
    );

    const warnings = this.generateWarnings(checks, tierGap, requesterTier, targetTier);

    return {
      passed,
      score,
      checks,
      requiredThreshold,
      recommendation,
      warnings
    };
  }

  /**
   * Calculate required threshold based on tier gap
   * Larger gaps require higher scores
   */
  private calculateRequiredThreshold(
    requesterTier: ProfessionalTier,
    targetTier: ProfessionalTier,
    tierGap: number
  ): number {
    const baselines = {
      // Same tier or down: very low bar
      0: 40,
      // 1 tier up: moderate bar
      1: 55,
      // 2 tiers up: higher bar
      2: 65,
      // 3 tiers up: high bar (e.g., Junior -> Executive)
      3: 75,
      // 4 tiers up: very high bar (e.g., Junior -> C-Level)
      4: 82,
      // 5+ tiers up: exceptional value required (e.g., Entry -> Founder/CEO)
      5: 88,
      6: 92,
      7: 95
    };

    let threshold = baselines[Math.min(tierGap, 7)] || 95;

    // Extra strict for Luminary targets
    if (targetTier === ProfessionalTier.LUMINARY) {
      threshold = Math.max(threshold, 90);
    }

    // Extra strict for C-Level and Founder/CEO
    if (targetTier === ProfessionalTier.C_LEVEL || targetTier === ProfessionalTier.FOUNDER_CEO) {
      threshold = Math.max(threshold, 80);
    }

    // Slightly more lenient if requester is at least Senior
    if (requesterTier === ProfessionalTier.SENIOR ||
        requesterTier === ProfessionalTier.EXECUTIVE) {
      threshold -= 5;
    }

    return Math.max(40, Math.min(95, threshold));
  }

  /**
   * Assess relevance of value proposition to target's needs
   */
  private assessRelevance(valueProposition: ValueProposition, target: Contact): number {
    let score = 50; // Base score

    // Check if target needs are addressed
    const needsAddressed = valueProposition.needsAddressed.length;
    if (needsAddressed > 0) {
      score += Math.min(needsAddressed * 15, 40);
    }

    // Check target's explicit needs
    const targetNeeds = target.needs || [];
    if (targetNeeds.length === 0) {
      // No explicit needs, harder to be relevant
      score -= 10;
    } else {
      // High relevance if multiple needs addressed
      const coverage = needsAddressed / targetNeeds.length;
      score += coverage * 20;
    }

    // Timeliness bonus
    if (valueProposition.timeliness > 70) {
      score += 10;
    }

    return Math.max(0, Math.min(100, score));
  }

  /**
   * Assess professionalism of approach
   */
  private assessProfessionalism(requester: Contact, valueProposition: ValueProposition): number {
    let score = 60; // Base moderate score

    // Complete profile indicates professionalism
    const profileCompleteness = this.calculateProfileCompleteness(requester);
    score += profileCompleteness * 0.2; // Up to +20

    // Verified social profiles
    if (requester.socialProfiles?.linkedin) score += 10;
    if (requester.company) score += 5;
    if (requester.title) score += 5;

    // Description quality
    const descLength = valueProposition.description.length;
    if (descLength < 50) {
      score -= 15; // Too brief, unprofessional
    } else if (descLength > 200 && descLength < 800) {
      score += 10; // Well-detailed
    } else if (descLength > 1000) {
      score -= 5; // Too verbose
    }

    // Check for spam indicators
    if (this.hasSpamIndicators(valueProposition.description)) {
      score -= 30;
    }

    // Specificity indicates effort and professionalism
    score += (valueProposition.specificity - 50) * 0.3;

    return Math.max(0, Math.min(100, score));
  }

  /**
   * Assess mutual benefit (not one-sided)
   */
  private assessMutualBenefit(
    requester: Contact,
    target: Contact,
    valueProposition: ValueProposition
  ): number {
    let score = 50; // Base score

    // Check if requester offers something target needs
    const targetNeeds = target.needs || [];
    const requesterOfferings = requester.offerings || [];

    let matchCount = 0;
    for (const need of targetNeeds) {
      for (const offering of requesterOfferings) {
        if (this.semanticSimilarity(need.toLowerCase(), offering.toLowerCase()) > 0.3) {
          matchCount++;
        }
      }
    }

    if (matchCount > 0) {
      score += Math.min(matchCount * 20, 40);
    }

    // Value proposition category bonus
    const mutualCategories = ['business_opportunity', 'collaboration', 'expertise_exchange'];
    if (mutualCategories.includes(valueProposition.category)) {
      score += 10;
    }

    // One-sided categories penalty
    const oneSidedCategories = ['career_opportunity', 'introduction'];
    if (oneSidedCategories.includes(valueProposition.category)) {
      score -= 15;
    }

    // Description indicates mutual benefit
    const description = valueProposition.description.toLowerCase();
    if (description.match(/mutual|both|together|collaboration|partnership/)) {
      score += 15;
    }

    // One-sided language penalty
    if (description.match(/\b(i need|help me|looking for|seeking|want)\b/) &&
        !description.match(/\b(i offer|i can help|i provide|i bring)\b/)) {
      score -= 20;
    }

    return Math.max(0, Math.min(100, score));
  }

  /**
   * Calculate overall gatekeeper score
   */
  private calculateGatekeeperScore(
    checks: GatekeeperValidation['checks'],
    tierGap: number
  ): number {
    // Weights vary based on tier gap
    const baseWeights = {
      valuePropositionStrength: 0.30,
      specificity: 0.15,
      relevance: 0.25,
      professionalism: 0.10,
      mutualBenefit: 0.10,
      verification: 0.10
    };

    // Adjust weights for large tier gaps
    if (tierGap >= 4) {
      // Value proposition strength becomes critical
      baseWeights.valuePropositionStrength = 0.40;
      baseWeights.relevance = 0.30;
      baseWeights.verification = 0.15;
      baseWeights.mutualBenefit = 0.10;
      baseWeights.specificity = 0.05;
      baseWeights.professionalism = 0.00; // Assumed if you got this far
    } else if (tierGap >= 2) {
      baseWeights.valuePropositionStrength = 0.35;
      baseWeights.relevance = 0.25;
      baseWeights.verification = 0.12;
    }

    const score =
      checks.valuePropositionStrength * baseWeights.valuePropositionStrength +
      checks.specificity * baseWeights.specificity +
      checks.relevance * baseWeights.relevance +
      checks.professionalism * baseWeights.professionalism +
      checks.mutualBenefit * baseWeights.mutualBenefit +
      checks.verification * baseWeights.verification;

    return Math.round(score);
  }

  /**
   * Generate recommendation message
   */
  private generateRecommendation(
    passed: boolean,
    score: number,
    requiredThreshold: number,
    checks: GatekeeperValidation['checks'],
    tierGap: number,
    requesterTier: ProfessionalTier,
    targetTier: ProfessionalTier
  ): string {
    if (passed) {
      if (score >= requiredThreshold + 10) {
        return `STRONGLY APPROVED: Excellent value proposition (${score}/100). This connection has high potential for mutual benefit.`;
      } else {
        return `APPROVED: Value proposition meets requirements (${score}/${requiredThreshold}). Connection is appropriate.`;
      }
    } else {
      const gap = requiredThreshold - score;

      if (gap <= 5) {
        return `BORDERLINE: Score is ${score}/${requiredThreshold}. Consider strengthening the value proposition, particularly: ${this.identifyWeakestAspects(checks).join(', ')}.`;
      } else if (gap <= 15) {
        return `NOT RECOMMENDED: Score is ${score}/${requiredThreshold}. The tier gap (${tierGap} levels) requires a stronger value proposition. Focus on: ${this.identifyWeakestAspects(checks).join(', ')}.`;
      } else {
        return `REJECTED: Score is ${score}/${requiredThreshold}. This connection is not appropriate. A ${requesterTier} contacting a ${targetTier} requires exceptional value. Consider: 1) Building credibility first, 2) Getting a warm introduction, 3) Connecting with someone closer to your tier.`;
      }
    }
  }

  /**
   * Generate warning messages
   */
  private generateWarnings(
    checks: GatekeeperValidation['checks'],
    tierGap: number,
    requesterTier: ProfessionalTier,
    targetTier: ProfessionalTier
  ): string[] {
    const warnings: string[] = [];

    // Low value proposition
    if (checks.valuePropositionStrength < 50) {
      warnings.push('⚠️ Value proposition is weak. Be more specific about what you can offer.');
    }

    // Low specificity
    if (checks.specificity < 40) {
      warnings.push('⚠️ Value proposition is too vague. Include concrete details, metrics, or examples.');
    }

    // Low relevance
    if (checks.relevance < 50) {
      warnings.push('⚠️ Value proposition may not be relevant to target\'s needs. Research their priorities.');
    }

    // Low professionalism
    if (checks.professionalism < 50) {
      warnings.push('⚠️ Approach lacks professionalism. Complete your profile and craft a thoughtful message.');
    }

    // One-sided benefit
    if (checks.mutualBenefit < 40) {
      warnings.push('⚠️ Connection appears one-sided. Emphasize mutual benefits, not just what you need.');
    }

    // Low verification
    if (checks.verification < 50) {
      warnings.push('⚠️ Claims are difficult to verify. Add evidence or credentials to build trust.');
    }

    // Large tier gap warning
    if (tierGap >= 4) {
      warnings.push(`⚠️ Large tier gap (${tierGap} levels). Consider getting a warm introduction or connecting with intermediaries first.`);
    }

    // Executive protection
    if (targetTier === ProfessionalTier.C_LEVEL ||
        targetTier === ProfessionalTier.FOUNDER_CEO ||
        targetTier === ProfessionalTier.LUMINARY) {
      warnings.push('⚠️ Contacting a senior executive. Ensure your value proposition is exceptional and relevant.');
    }

    return warnings;
  }

  /**
   * Identify weakest aspects of the submission
   */
  private identifyWeakestAspects(checks: GatekeeperValidation['checks']): string[] {
    const aspects = [
      { name: 'value proposition strength', score: checks.valuePropositionStrength },
      { name: 'specificity', score: checks.specificity },
      { name: 'relevance to target', score: checks.relevance },
      { name: 'professionalism', score: checks.professionalism },
      { name: 'mutual benefit', score: checks.mutualBenefit },
      { name: 'verifiability', score: checks.verification }
    ];

    // Sort by score ascending
    aspects.sort((a, b) => a.score - b.score);

    // Return bottom 2-3
    return aspects.slice(0, 3).map(a => a.name);
  }

  /**
   * Calculate profile completeness
   */
  private calculateProfileCompleteness(contact: Contact): number {
    let score = 0;
    const fields = [
      contact.name,
      contact.email,
      contact.company,
      contact.title,
      contact.bio,
      contact.industry,
      contact.location
    ];

    score += fields.filter(f => f && f.length > 0).length * 10; // 70 max

    if (contact.skills && contact.skills.length > 0) score += 10;
    if (contact.needs && contact.needs.length > 0) score += 5;
    if (contact.offerings && contact.offerings.length > 0) score += 10;
    if (contact.socialProfiles?.linkedin) score += 5;

    return Math.min(100, score);
  }

  /**
   * Check for spam indicators
   */
  private hasSpamIndicators(text: string): boolean {
    const spamPatterns = [
      /click here/i,
      /limited time offer/i,
      /act now/i,
      /guaranteed/i,
      /make money fast/i,
      /work from home/i,
      /\$\$\$/,
      /!!!{2,}/,
      /FREE!!!/i
    ];

    return spamPatterns.some(pattern => pattern.test(text));
  }

  /**
   * Simple semantic similarity
   */
  private semanticSimilarity(text1: string, text2: string): number {
    const words1 = new Set(text1.split(/\s+/));
    const words2 = new Set(text2.split(/\s+/));

    const intersection = new Set([...words1].filter(w => words2.has(w)));
    const union = new Set([...words1, ...words2]);

    return union.size > 0 ? intersection.size / union.size : 0;
  }

  /**
   * Create a full cross-tier access request evaluation
   */
  async evaluateCrossTierRequest(
    requester: Contact,
    target: Contact,
    requesterTier: ProfessionalTier,
    targetTier: ProfessionalTier,
    tierGap: number,
    valueProposition: ValueProposition
  ): Promise<CrossTierAccessRequest> {
    const gatekeeperValidation = await this.validateAccess(
      requester,
      target,
      requesterTier,
      targetTier,
      valueProposition,
      tierGap
    );

    return {
      requester,
      target,
      requesterTier,
      targetTier,
      tierGap,
      valueProposition,
      gatekeeperValidation,
      approved: gatekeeperValidation.passed,
      reason: gatekeeperValidation.recommendation
    };
  }
}
