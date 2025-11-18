/**
 * Enhanced Bidirectional Validation Agent
 * Ensures mutual benefit and prevents one-sided connections
 * Validates that BOTH parties genuinely benefit from the connection
 */

import {
  Contact,
  BidirectionalValidation,
  ContextualNeedsAnalysis,
  ProfessionalTier,
  AgentType,
  AgentCapability
} from '../types';

export class EnhancedBidirectionalValidationAgent {
  private agentType = AgentType.EVALUATOR;
  private capabilities = [AgentCapability.EVALUATE, AgentCapability.ANALYZE];

  /**
   * Validate bidirectional benefit between two contacts
   */
  async validateBidirectionalBenefit(
    seeker: Contact,
    target: Contact,
    seekerTier?: ProfessionalTier,
    targetTier?: ProfessionalTier
  ): Promise<BidirectionalValidation> {
    // Calculate benefit for seeker
    const seekerBenefit = this.calculateBenefitScore(
      seeker,
      target,
      'seeker',
      seekerTier,
      targetTier
    );

    // Calculate benefit for target
    const targetBenefit = this.calculateBenefitScore(
      target,
      seeker,
      'target',
      targetTier,
      seekerTier
    );

    // Calculate mutuality score (minimum of both)
    const mutualityScore = Math.min(seekerBenefit, targetBenefit);

    // Check for imbalance
    const balanceRatio = Math.min(seekerBenefit, targetBenefit) / Math.max(seekerBenefit, targetBenefit);
    const imbalanceWarning = balanceRatio < 0.6; // More than 40% difference

    // Identify specific needs being addressed
    const seekerNeeds = this.identifyNeedsAddressed(seeker, target);
    const targetNeeds = this.identifyNeedsAddressed(target, seeker);

    return {
      seekerBenefit,
      targetBenefit,
      mutualityScore,
      imbalanceWarning,
      seekerNeeds,
      targetNeeds,
      balanceRatio
    };
  }

  /**
   * Calculate benefit score for one party
   */
  private calculateBenefitScore(
    beneficiary: Contact,
    helper: Contact,
    role: 'seeker' | 'target',
    beneficiaryTier?: ProfessionalTier,
    helperTier?: ProfessionalTier
  ): number {
    let score = 0;

    // 1. Needs satisfaction (40 points max)
    const needsSatisfaction = this.calculateNeedsSatisfaction(beneficiary, helper);
    score += needsSatisfaction * 0.4;

    // 2. Value exchange (30 points max)
    const valueExchange = this.calculateValueExchange(beneficiary, helper);
    score += valueExchange * 0.3;

    // 3. Network value (15 points max)
    const networkValue = this.calculateNetworkValue(helper, beneficiaryTier, helperTier);
    score += networkValue * 0.15;

    // 4. Knowledge/expertise value (15 points max)
    const expertiseValue = this.calculateExpertiseValue(beneficiary, helper);
    score += expertiseValue * 0.15;

    return Math.min(100, Math.round(score));
  }

  /**
   * Calculate how well helper satisfies beneficiary's needs
   */
  private calculateNeedsSatisfaction(beneficiary: Contact, helper: Contact): number {
    const beneficiaryNeeds = beneficiary.needs || [];
    const helperOfferings = helper.offerings || [];
    const helperSkills = helper.skills || [];

    if (beneficiaryNeeds.length === 0) {
      return 50; // No explicit needs, moderate score
    }

    let totalSatisfaction = 0;
    let satisfiedNeeds = 0;

    for (const need of beneficiaryNeeds) {
      const needLower = need.toLowerCase();

      // Check offerings
      for (const offering of helperOfferings) {
        const similarity = this.semanticSimilarity(needLower, offering.toLowerCase());
        if (similarity > 0.3) {
          totalSatisfaction += similarity * 100;
          satisfiedNeeds++;
          break;
        }
      }

      // Check skills if not satisfied by offerings
      if (satisfiedNeeds === 0 || satisfiedNeeds < beneficiaryNeeds.length) {
        for (const skill of helperSkills) {
          const similarity = this.semanticSimilarity(needLower, skill.toLowerCase());
          if (similarity > 0.3) {
            totalSatisfaction += similarity * 70; // Skills slightly less valuable than explicit offerings
            satisfiedNeeds++;
            break;
          }
        }
      }
    }

    if (satisfiedNeeds === 0) return 0;

    // Average satisfaction * coverage
    const avgSatisfaction = totalSatisfaction / satisfiedNeeds;
    const coverage = satisfiedNeeds / beneficiaryNeeds.length;

    return avgSatisfaction * coverage;
  }

  /**
   * Calculate value exchange potential
   */
  private calculateValueExchange(beneficiary: Contact, helper: Contact): number {
    const beneficiaryOfferings = beneficiary.offerings || [];
    const helperNeeds = helper.needs || [];

    // What can beneficiary offer in return?
    if (beneficiaryOfferings.length === 0) {
      return 30; // Limited to offer
    }

    if (helperNeeds.length === 0) {
      return 50; // Helper hasn't stated needs, assume moderate value
    }

    let exchangeValue = 0;
    let matches = 0;

    for (const helperNeed of helperNeeds) {
      for (const offering of beneficiaryOfferings) {
        const similarity = this.semanticSimilarity(
          helperNeed.toLowerCase(),
          offering.toLowerCase()
        );
        if (similarity > 0.3) {
          exchangeValue += similarity * 100;
          matches++;
        }
      }
    }

    if (matches === 0) return 20; // No clear exchange value

    return Math.min(100, (exchangeValue / matches));
  }

  /**
   * Calculate network value (value of adding this person to network)
   */
  private calculateNetworkValue(
    helper: Contact,
    beneficiaryTier?: ProfessionalTier,
    helperTier?: ProfessionalTier
  ): number {
    let value = 50; // Base network value

    // Tier-based network value
    if (helperTier && beneficiaryTier) {
      const tierOrder = [
        ProfessionalTier.ENTRY,
        ProfessionalTier.JUNIOR,
        ProfessionalTier.MID_LEVEL,
        ProfessionalTier.SENIOR,
        ProfessionalTier.EXECUTIVE,
        ProfessionalTier.C_LEVEL,
        ProfessionalTier.FOUNDER_CEO,
        ProfessionalTier.LUMINARY
      ];

      const helperIndex = tierOrder.indexOf(helperTier);
      const beneficiaryIndex = tierOrder.indexOf(beneficiaryTier);

      // Connecting with higher tier adds value
      if (helperIndex > beneficiaryIndex) {
        value += (helperIndex - beneficiaryIndex) * 8; // Up to +56
      }
    }

    // Prestigious company
    const prestigiousCompanies = ['google', 'apple', 'microsoft', 'amazon', 'meta',
                                   'tesla', 'openai', 'anthropic', 'stripe'];
    if (helper.company &&
        prestigiousCompanies.some(c => helper.company!.toLowerCase().includes(c))) {
      value += 20;
    }

    // Industry diversity
    // (Different industry can be valuable for cross-pollination)

    return Math.min(100, value);
  }

  /**
   * Calculate expertise/knowledge value
   */
  private calculateExpertiseValue(beneficiary: Contact, helper: Contact): number {
    let value = 40; // Base value

    const helperSkills = helper.skills || [];
    const beneficiarySkills = beneficiary.skills || [];

    // Unique skills helper has that beneficiary doesn't
    const uniqueSkills = helperSkills.filter(hs =>
      !beneficiarySkills.some(bs =>
        this.semanticSimilarity(hs.toLowerCase(), bs.toLowerCase()) > 0.5
      )
    );

    // More unique skills = more value
    value += Math.min(uniqueSkills.length * 5, 40);

    // Bio indicates expertise
    if (helper.bio && helper.bio.length > 200) {
      value += 10;
    }

    // Title indicates seniority/expertise
    if (helper.title) {
      const titleLower = helper.title.toLowerCase();
      if (titleLower.match(/senior|lead|principal|director|vp|chief/)) {
        value += 15;
      }
    }

    return Math.min(100, value);
  }

  /**
   * Identify specific needs being addressed
   */
  private identifyNeedsAddressed(beneficiary: Contact, helper: Contact): string[] {
    const beneficiaryNeeds = beneficiary.needs || [];
    const helperOfferings = helper.offerings || [];
    const helperSkills = helper.skills || [];

    const addressed: string[] = [];

    for (const need of beneficiaryNeeds) {
      const needLower = need.toLowerCase();

      // Check offerings
      const offeringMatch = helperOfferings.some(offering =>
        this.semanticSimilarity(needLower, offering.toLowerCase()) > 0.3
      );

      // Check skills
      const skillMatch = helperSkills.some(skill =>
        this.semanticSimilarity(needLower, skill.toLowerCase()) > 0.3
      );

      if (offeringMatch || skillMatch) {
        addressed.push(need);
      }
    }

    return addressed;
  }

  /**
   * Validate with contextual needs analysis
   */
  async validateWithContextualNeeds(
    seeker: Contact,
    target: Contact,
    seekerNeedsAnalysis: ContextualNeedsAnalysis[],
    targetNeedsAnalysis: ContextualNeedsAnalysis[],
    seekerTier?: ProfessionalTier,
    targetTier?: ProfessionalTier
  ): Promise<BidirectionalValidation> {
    // Get base validation
    const baseValidation = await this.validateBidirectionalBenefit(
      seeker,
      target,
      seekerTier,
      targetTier
    );

    // Enhance with contextual understanding
    const contextualBonus = this.calculateContextualBonus(
      seekerNeedsAnalysis,
      targetNeedsAnalysis,
      seeker,
      target
    );

    // Adjust scores
    const seekerBenefit = Math.min(100, baseValidation.seekerBenefit + contextualBonus.seekerBonus);
    const targetBenefit = Math.min(100, baseValidation.targetBenefit + contextualBonus.targetBonus);

    const mutualityScore = Math.min(seekerBenefit, targetBenefit);
    const balanceRatio = Math.min(seekerBenefit, targetBenefit) / Math.max(seekerBenefit, targetBenefit);
    const imbalanceWarning = balanceRatio < 0.6;

    return {
      seekerBenefit,
      targetBenefit,
      mutualityScore,
      imbalanceWarning,
      seekerNeeds: baseValidation.seekerNeeds,
      targetNeeds: baseValidation.targetNeeds,
      balanceRatio
    };
  }

  /**
   * Calculate bonus from contextual needs analysis
   */
  private calculateContextualBonus(
    seekerNeedsAnalysis: ContextualNeedsAnalysis[],
    targetNeedsAnalysis: ContextualNeedsAnalysis[],
    seeker: Contact,
    target: Contact
  ): { seekerBonus: number; targetBonus: number } {
    let seekerBonus = 0;
    let targetBonus = 0;

    // Check if target can help with seeker's critical/urgent needs
    for (const seekerNeed of seekerNeedsAnalysis) {
      if (seekerNeed.importance === 'critical' || seekerNeed.urgency === 'critical') {
        const targetSkills = target.skills || [];
        const targetOfferings = target.offerings || [];

        const canHelp = [...targetSkills, ...targetOfferings].some(item =>
          seekerNeed.keywords.some(kw => item.toLowerCase().includes(kw))
        );

        if (canHelp) {
          seekerBonus += 15; // Significant bonus for addressing critical needs
        }
      }
    }

    // Check if seeker can help with target's critical/urgent needs
    for (const targetNeed of targetNeedsAnalysis) {
      if (targetNeed.importance === 'critical' || targetNeed.urgency === 'critical') {
        const seekerSkills = seeker.skills || [];
        const seekerOfferings = seeker.offerings || [];

        const canHelp = [...seekerSkills, ...seekerOfferings].some(item =>
          targetNeed.keywords.some(kw => item.toLowerCase().includes(kw))
        );

        if (canHelp) {
          targetBonus += 15;
        }
      }
    }

    return {
      seekerBonus: Math.min(seekerBonus, 25),
      targetBonus: Math.min(targetBonus, 25)
    };
  }

  /**
   * Check if connection passes bidirectional validation
   */
  passesValidation(
    validation: BidirectionalValidation,
    minMutualityScore: number = 60
  ): boolean {
    // Both parties must benefit at least at the minimum level
    return (
      validation.mutualityScore >= minMutualityScore &&
      validation.seekerBenefit >= minMutualityScore &&
      validation.targetBenefit >= minMutualityScore
    );
  }

  /**
   * Get validation quality level
   */
  getValidationQuality(validation: BidirectionalValidation): string {
    const score = validation.mutualityScore;

    if (score >= 85) return 'Exceptional mutual benefit';
    if (score >= 75) return 'Strong mutual benefit';
    if (score >= 65) return 'Good mutual benefit';
    if (score >= 55) return 'Moderate mutual benefit';
    if (score >= 45) return 'Weak mutual benefit';
    return 'Insufficient mutual benefit';
  }

  /**
   * Generate validation report
   */
  generateValidationReport(validation: BidirectionalValidation): string {
    const lines: string[] = [];

    lines.push(`Bidirectional Validation Report:`);
    lines.push(`  Seeker Benefit: ${validation.seekerBenefit}/100`);
    lines.push(`  Target Benefit: ${validation.targetBenefit}/100`);
    lines.push(`  Mutuality Score: ${validation.mutualityScore}/100`);
    lines.push(`  Balance Ratio: ${(validation.balanceRatio * 100).toFixed(1)}%`);
    lines.push(`  Quality: ${this.getValidationQuality(validation)}`);

    if (validation.imbalanceWarning) {
      lines.push(`  ⚠️ WARNING: Imbalanced connection (one party benefits significantly more)`);
    }

    if (validation.seekerNeeds.length > 0) {
      lines.push(`  Seeker needs addressed: ${validation.seekerNeeds.join(', ')}`);
    } else {
      lines.push(`  ⚠️ No clear needs addressed for seeker`);
    }

    if (validation.targetNeeds.length > 0) {
      lines.push(`  Target needs addressed: ${validation.targetNeeds.join(', ')}`);
    } else {
      lines.push(`  ⚠️ No clear needs addressed for target`);
    }

    return lines.join('\n');
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
}
