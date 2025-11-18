/**
 * Value Proposition Agent
 * Assesses the strength and quality of value propositions for cross-tier connections
 */

import {
  Contact,
  ValueProposition,
  ValuePropositionCategory,
  ProfessionalTier,
  AgentType,
  AgentCapability
} from '../types';
import { v4 as uuidv4 } from 'uuid';

export class ValuePropositionAgent {
  private agentType = AgentType.EVALUATOR;
  private capabilities = [AgentCapability.EVALUATE, AgentCapability.ANALYZE];

  /**
   * Assess value proposition from seeker to target
   */
  async assessValueProposition(
    seeker: Contact,
    target: Contact,
    seekerTier: ProfessionalTier,
    targetTier: ProfessionalTier,
    proposedValue?: string
  ): Promise<ValueProposition> {
    // Extract or infer value proposition
    const category = this.categorizeValueProposition(seeker, target, proposedValue);
    const description = proposedValue || this.inferValueProposition(seeker, target);

    // Assess various dimensions
    const strength = this.calculateStrength(seeker, target, category, description, seekerTier, targetTier);
    const specificity = this.assessSpecificity(description);
    const verifiability = this.assessVerifiability(seeker, description);
    const uniqueness = this.assessUniqueness(seeker, target, description);
    const timeliness = this.assessTimeliness(description, target);
    const needsAddressed = this.identifyNeedsAddressed(target, description);
    const evidence = this.extractEvidence(seeker, description);

    return {
      id: uuidv4(),
      proposer: seeker.id,
      target: target.id,
      strength,
      category,
      description,
      specificity,
      verifiability,
      evidence,
      needsAddressed,
      uniqueness,
      timeliness,
      validated: strength >= 70, // Auto-validate if strong enough
      validationTimestamp: new Date()
    };
  }

  /**
   * Categorize the type of value proposition
   */
  private categorizeValueProposition(
    seeker: Contact,
    target: Contact,
    proposedValue?: string
  ): ValuePropositionCategory {
    const text = (proposedValue || seeker.bio || '').toLowerCase();
    const seekerOfferings = (seeker.offerings || []).join(' ').toLowerCase();
    const targetNeeds = (target.needs || []).join(' ').toLowerCase();

    // Business opportunity keywords
    if (text.match(/partnership|investment|funding|revenue|sales|deal|contract|acquisition/) ||
        seekerOfferings.match(/capital|funding|investment/)) {
      return ValuePropositionCategory.BUSINESS_OPPORTUNITY;
    }

    // Innovation keywords
    if (text.match(/innovation|patent|technology|breakthrough|novel|cutting-edge|revolutionary/)) {
      return ValuePropositionCategory.INNOVATION;
    }

    // Market access
    if (text.match(/market access|customers|distribution|channel|network effect/)) {
      return ValuePropositionCategory.MARKET_ACCESS;
    }

    // Problem solving
    if (text.match(/solve|solution|fix|address|resolve/) || targetNeeds.length > 0) {
      return ValuePropositionCategory.PROBLEM_SOLVING;
    }

    // Resource access
    if (text.match(/access to|resources|tools|platform|infrastructure/)) {
      return ValuePropositionCategory.RESOURCE_ACCESS;
    }

    // Career opportunity
    if (text.match(/hiring|job|position|opportunity|role|join our team/)) {
      return ValuePropositionCategory.CAREER_OPPORTUNITY;
    }

    // Introduction
    if (text.match(/introduce|connect you with|know someone/)) {
      return ValuePropositionCategory.INTRODUCTION;
    }

    // Default to expertise exchange
    return ValuePropositionCategory.EXPERTISE_EXCHANGE;
  }

  /**
   * Infer value proposition based on seeker's offerings and target's needs
   */
  private inferValueProposition(seeker: Contact, target: Contact): string {
    const seekerOfferings = seeker.offerings || [];
    const targetNeeds = target.needs || [];

    // Find overlaps
    const overlaps = seekerOfferings.filter(offering =>
      targetNeeds.some(need =>
        this.semanticSimilarity(offering.toLowerCase(), need.toLowerCase()) > 0.5
      )
    );

    if (overlaps.length > 0) {
      return `I can help with ${overlaps.slice(0, 2).join(' and ')}`;
    }

    // Use seeker's primary offerings
    if (seekerOfferings.length > 0) {
      return `I offer expertise in ${seekerOfferings.slice(0, 2).join(' and ')}`;
    }

    // Fallback to skills
    if (seeker.skills && seeker.skills.length > 0) {
      return `I have skills in ${seeker.skills.slice(0, 3).join(', ')}`;
    }

    return 'Mutual professional growth and knowledge exchange';
  }

  /**
   * Calculate overall value proposition strength (0-100)
   */
  private calculateStrength(
    seeker: Contact,
    target: Contact,
    category: ValuePropositionCategory,
    description: string,
    seekerTier: ProfessionalTier,
    targetTier: ProfessionalTier
  ): number {
    let strength = 50; // Base score

    // Category-based bonuses
    const categoryWeights = {
      [ValuePropositionCategory.BUSINESS_OPPORTUNITY]: 30,
      [ValuePropositionCategory.INNOVATION]: 25,
      [ValuePropositionCategory.MARKET_ACCESS]: 25,
      [ValuePropositionCategory.PROBLEM_SOLVING]: 20,
      [ValuePropositionCategory.RESOURCE_ACCESS]: 15,
      [ValuePropositionCategory.CAREER_OPPORTUNITY]: 20,
      [ValuePropositionCategory.INTRODUCTION]: 15,
      [ValuePropositionCategory.EXPERTISE_EXCHANGE]: 10
    };

    strength += categoryWeights[category] || 0;

    // Needs alignment bonus
    const needsAlignment = this.calculateNeedsAlignment(seeker, target);
    strength += needsAlignment * 0.3; // Up to +30

    // Tier-appropriate bonus/penalty
    const tierAppropriatenesss = this.assessTierAppropriateness(seekerTier, targetTier, category);
    strength *= tierAppropriatenesss;

    // Specificity of offering
    const specificity = this.assessSpecificity(description);
    strength += (specificity - 50) * 0.2; // Adjust based on specificity

    // Seeker credibility
    const credibility = this.assessSeekerCredibility(seeker, seekerTier);
    strength += credibility * 0.2; // Up to +20

    return Math.max(0, Math.min(100, Math.round(strength)));
  }

  /**
   * Assess how specific and concrete the value proposition is
   */
  private assessSpecificity(description: string): number {
    let score = 30; // Base low score for vague

    // Length indicates detail
    const wordCount = description.split(/\s+/).length;
    if (wordCount > 50) score += 20;
    else if (wordCount > 30) score += 15;
    else if (wordCount > 15) score += 10;

    // Specific numbers/metrics
    if (description.match(/\d+%|\$\d+|[0-9,]+\s*(users|customers|revenue)/i)) {
      score += 25;
    }

    // Concrete nouns vs vague terms
    const concreteTerms = description.match(/product|platform|system|process|methodology|framework|tool/gi);
    if (concreteTerms && concreteTerms.length > 0) {
      score += Math.min(concreteTerms.length * 5, 20);
    }

    // Penalty for vague buzzwords
    const vagueTerms = description.match(/synergy|leverage|innovative|cutting-edge|world-class|best-in-class/gi);
    if (vagueTerms && vagueTerms.length > 2) {
      score -= 10;
    }

    // Specific action verbs
    const actionVerbs = description.match(/\b(build|create|develop|implement|deploy|launch|scale|optimize)\b/gi);
    if (actionVerbs && actionVerbs.length > 0) {
      score += 10;
    }

    return Math.max(0, Math.min(100, score));
  }

  /**
   * Assess how verifiable the claims are
   */
  private assessVerifiability(seeker: Contact, description: string): number {
    let score = 40; // Base score

    // LinkedIn profile available
    if (seeker.socialProfiles?.linkedin) {
      score += 15;
    }

    // Company email (not personal)
    if (seeker.email && !seeker.email.match(/@(gmail|yahoo|hotmail|outlook)/i)) {
      score += 15;
    }

    // Specific company mentioned
    if (seeker.company) {
      score += 10;
    }

    // Quantifiable claims
    const quantifiableClaims = description.match(/\d+%|\$\d+M|\d+\s*years?|[0-9,]+\s*(users|customers)/gi);
    if (quantifiableClaims) {
      score += Math.min(quantifiableClaims.length * 10, 20);
    }

    // References to verifiable entities
    if (description.match(/published|patented|certified|awarded|featured in/i)) {
      score += 20;
    }

    // Website/portfolio mentioned
    if (seeker.socialProfiles?.website || seeker.socialProfiles?.github) {
      score += 10;
    }

    return Math.max(0, Math.min(100, score));
  }

  /**
   * Assess uniqueness of the value proposition
   */
  private assessUniqueness(seeker: Contact, target: Contact, description: string): number {
    let score = 50; // Base middling score

    // Unique skills or rare expertise
    const rareSkills = ['AI safety', 'quantum computing', 'genomics', 'space tech', 'fusion energy'];
    const seekerSkills = (seeker.skills || []).join(' ').toLowerCase();
    if (rareSkills.some(skill => seekerSkills.includes(skill.toLowerCase()))) {
      score += 20;
    }

    // Proprietary technology/IP
    if (description.match(/proprietary|patent|exclusive|unique|first-of-its-kind/i)) {
      score += 15;
    }

    // Rare combination of skills
    if (seeker.skills && seeker.skills.length >= 5) {
      score += 10;
    }

    // Novel approach
    if (description.match(/novel|innovative|breakthrough|pioneering|first to/i)) {
      score += 10;
    }

    // Access to hard-to-reach network/resources
    if (description.match(/exclusive access|rare opportunity|limited availability/i)) {
      score += 15;
    }

    return Math.max(0, Math.min(100, score));
  }

  /**
   * Assess timeliness and urgency
   */
  private assessTimeliness(description: string, target: Contact): number {
    let score = 50; // Base score

    // Urgency indicators
    if (description.match(/urgent|immediate|asap|time-sensitive|deadline/i)) {
      score += 20;
    }

    // Market timing
    if (description.match(/trending|hot market|growing demand|emerging/i)) {
      score += 15;
    }

    // Alignment with target's current needs
    const targetNeeds = (target.needs || []).join(' ').toLowerCase();
    if (targetNeeds.length > 0) {
      const descLower = description.toLowerCase();
      const hasRelevance = target.needs?.some(need =>
        this.semanticSimilarity(descLower, need.toLowerCase()) > 0.4
      );
      if (hasRelevance) {
        score += 25;
      }
    }

    return Math.max(0, Math.min(100, score));
  }

  /**
   * Identify which of target's needs are addressed
   */
  private identifyNeedsAddressed(target: Contact, description: string): string[] {
    const targetNeeds = target.needs || [];
    const addressed: string[] = [];

    const descLower = description.toLowerCase();

    for (const need of targetNeeds) {
      const similarity = this.semanticSimilarity(descLower, need.toLowerCase());
      if (similarity > 0.3) {
        addressed.push(need);
      }
    }

    return addressed;
  }

  /**
   * Extract evidence supporting the value proposition
   */
  private extractEvidence(seeker: Contact, description: string): string[] {
    const evidence: string[] = [];

    if (seeker.company) {
      evidence.push(`Works at ${seeker.company}`);
    }

    if (seeker.title) {
      evidence.push(`Title: ${seeker.title}`);
    }

    if (seeker.skills && seeker.skills.length > 0) {
      evidence.push(`Skills: ${seeker.skills.slice(0, 5).join(', ')}`);
    }

    // Extract quantifiable claims from description
    const metrics = description.match(/\d+%|\$\d+[KMB]?|\d+[KMB]?\s*(users|customers|revenue)/gi);
    if (metrics) {
      evidence.push(...metrics);
    }

    if (seeker.socialProfiles?.linkedin) {
      evidence.push('Verified LinkedIn profile');
    }

    return evidence;
  }

  /**
   * Calculate needs alignment between seeker's offerings and target's needs
   */
  private calculateNeedsAlignment(seeker: Contact, target: Contact): number {
    const seekerOfferings = seeker.offerings || [];
    const targetNeeds = target.needs || [];

    if (targetNeeds.length === 0) return 30; // Default moderate alignment

    let totalSimilarity = 0;
    let matches = 0;

    for (const need of targetNeeds) {
      const needLower = need.toLowerCase();
      for (const offering of seekerOfferings) {
        const similarity = this.semanticSimilarity(needLower, offering.toLowerCase());
        if (similarity > 0.3) {
          totalSimilarity += similarity;
          matches++;
        }
      }
    }

    if (matches === 0) return 0;

    // Average similarity * coverage percentage
    const avgSimilarity = totalSimilarity / matches;
    const coverage = Math.min(matches / targetNeeds.length, 1);

    return (avgSimilarity * 70 + coverage * 30);
  }

  /**
   * Assess if value proposition is appropriate for the tier gap
   */
  private assessTierAppropriateness(
    seekerTier: ProfessionalTier,
    targetTier: ProfessionalTier,
    category: ValuePropositionCategory
  ): number {
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

    const seekerIndex = tierOrder.indexOf(seekerTier);
    const targetIndex = tierOrder.indexOf(targetTier);
    const tierGap = targetIndex - seekerIndex;

    if (tierGap <= 0) return 1.0; // Same tier or contacting down is always appropriate

    // High-value categories are more appropriate for large gaps
    const highValueCategories = [
      ValuePropositionCategory.BUSINESS_OPPORTUNITY,
      ValuePropositionCategory.INNOVATION,
      ValuePropositionCategory.MARKET_ACCESS
    ];

    const isHighValue = highValueCategories.includes(category);

    // Calculate appropriateness multiplier
    if (tierGap === 1) return 1.0; // 1 tier up is fine
    if (tierGap === 2) return isHighValue ? 1.0 : 0.9;
    if (tierGap === 3) return isHighValue ? 0.95 : 0.7;
    if (tierGap === 4) return isHighValue ? 0.9 : 0.5;
    if (tierGap >= 5) return isHighValue ? 0.8 : 0.3; // Large gap requires exceptional value

    return 1.0;
  }

  /**
   * Assess seeker's credibility
   */
  private assessSeekerCredibility(seeker: Contact, tier: ProfessionalTier): number {
    let score = 50; // Base score

    // Tier-based credibility
    const tierScores = {
      [ProfessionalTier.ENTRY]: 30,
      [ProfessionalTier.JUNIOR]: 40,
      [ProfessionalTier.MID_LEVEL]: 50,
      [ProfessionalTier.SENIOR]: 65,
      [ProfessionalTier.EXECUTIVE]: 75,
      [ProfessionalTier.C_LEVEL]: 85,
      [ProfessionalTier.FOUNDER_CEO]: 90,
      [ProfessionalTier.LUMINARY]: 95
    };

    score = tierScores[tier] || 50;

    // Verified profiles add credibility
    if (seeker.socialProfiles?.linkedin) score += 10;
    if (seeker.company) score += 5;
    if (seeker.email && !seeker.email.match(/@(gmail|yahoo)/i)) score += 5;

    return Math.min(100, score);
  }

  /**
   * Simple semantic similarity based on word overlap
   */
  private semanticSimilarity(text1: string, text2: string): number {
    const words1 = new Set(text1.toLowerCase().split(/\s+/));
    const words2 = new Set(text2.toLowerCase().split(/\s+/));

    const intersection = new Set([...words1].filter(w => words2.has(w)));
    const union = new Set([...words1, ...words2]);

    return intersection.size / union.size;
  }
}
