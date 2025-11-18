/**
 * Contextual Matching Agent
 * Matches people based on current context, goals, and situational needs
 * Adapts matching criteria based on user's current objectives
 */

import { Contact, Match, MatchType } from '../types';

export enum MatchContext {
  FUNDRAISING = 'fundraising',
  HIRING = 'hiring',
  BUSINESS_DEVELOPMENT = 'business_development',
  PARTNERSHIPS = 'partnerships',
  MENTORSHIP = 'mentorship',
  JOB_SEARCH = 'job_search',
  NETWORKING = 'networking',
  LEARNING = 'learning',
  SELLING = 'selling',
}

export interface ContextualGoal {
  context: MatchContext;
  priority: number; // 0-1
  timeframe: 'immediate' | 'short_term' | 'medium_term' | 'long_term';
  specificNeeds: string[];
  constraints?: {
    geographic?: string[];
    industry?: string[];
    company_stage?: string[];
    budget_range?: { min: number; max: number };
  };
  // Enhanced matching preferences
  urgency?: 'immediate' | 'high' | 'medium' | 'low';
  timeline?: string;
  relationshipType?: 'one-time' | 'short-term' | 'long-term' | 'ongoing';
  communicationStyle?: string[];
  workingStyle?: string[];
  geographicPreference?: string;
  dealBreakers?: string;
  successCriteria?: string;
}

export interface ContextualMatchScore {
  baseScore: number;
  contextBoost: number;
  finalScore: number;
  contextAlignment: number;
  urgencyFactor: number;
  feasibilityScore: number;
  reasons: string[];
}

export class ContextualMatchingAgent {
  private contextWeights: Map<MatchContext, Map<string, number>>;

  constructor() {
    this.contextWeights = this.initializeContextWeights();
  }

  /**
   * Initialize context-specific weighting schemes
   */
  private initializeContextWeights(): Map<MatchContext, Map<string, number>> {
    const weights = new Map<MatchContext, Map<string, number>>();

    // Fundraising context
    weights.set(MatchContext.FUNDRAISING, new Map([
      ['funding_capacity', 0.35],
      ['industry_expertise', 0.25],
      ['investment_stage_match', 0.20],
      ['network_value', 0.10],
      ['geographic_proximity', 0.10],
    ]));

    // Hiring context
    weights.set(MatchContext.HIRING, new Map([
      ['skills_match', 0.40],
      ['experience_level', 0.25],
      ['culture_fit', 0.20],
      ['availability', 0.10],
      ['compensation_alignment', 0.05],
    ]));

    // Business Development context
    weights.set(MatchContext.BUSINESS_DEVELOPMENT, new Map([
      ['customer_fit', 0.30],
      ['decision_maker_access', 0.25],
      ['budget_alignment', 0.20],
      ['urgency_match', 0.15],
      ['relationship_strength', 0.10],
    ]));

    // Partnership context
    weights.set(MatchContext.PARTNERSHIPS, new Map([
      ['strategic_alignment', 0.30],
      ['complementary_strengths', 0.25],
      ['market_synergy', 0.20],
      ['trust_level', 0.15],
      ['value_alignment', 0.10],
    ]));

    // Mentorship context
    weights.set(MatchContext.MENTORSHIP, new Map([
      ['expertise_gap', 0.35],
      ['experience_differential', 0.25],
      ['personality_compatibility', 0.20],
      ['availability', 0.15],
      ['commitment_level', 0.05],
    ]));

    return weights;
  }

  /**
   * Score a match based on current context
   */
  scoreMatchInContext(
    match: Match,
    goal: ContextualGoal,
    sourceContact: Contact,
    targetContact: Contact
  ): ContextualMatchScore {
    const baseScore = match.compatibilityScore;
    const contextAlignment = this.calculateContextAlignment(goal, sourceContact, targetContact);
    const urgencyFactor = this.calculateUrgencyFactor(goal);
    const feasibilityScore = this.calculateFeasibility(goal, targetContact);

    // Enhanced: Add communication, working style, and geographic compatibility
    const communicationCompatibility = this.evaluateCommunicationStyleCompatibility(
      goal.communicationStyle || sourceContact.metadata?.communicationStyle,
      targetContact.metadata?.communicationStyle
    );

    const workingStyleCompatibility = this.evaluateWorkingStyleCompatibility(
      goal.workingStyle || sourceContact.metadata?.workingStyle,
      targetContact.metadata?.workingStyle
    );

    const geographicCompatibility = this.evaluateGeographicCompatibility(
      goal.geographicPreference || sourceContact.metadata?.geographicPreference,
      targetContact.metadata?.geographicPreference,
      sourceContact.location,
      targetContact.location
    );

    // Check deal breakers
    const passesDealBreakers = this.checkDealBreakers(
      goal.dealBreakers || sourceContact.metadata?.dealBreakers,
      targetContact
    );

    if (!passesDealBreakers) {
      // If deal breakers aren't met, significantly reduce score
      return {
        baseScore,
        contextBoost: -0.5,
        finalScore: Math.max(0, baseScore - 0.5),
        contextAlignment,
        urgencyFactor,
        feasibilityScore,
        reasons: ['Does not meet critical requirements (deal breakers)'],
      };
    }

    // Calculate enhanced context boost
    const preferenceScore = (
      communicationCompatibility * 0.3 +
      workingStyleCompatibility * 0.3 +
      geographicCompatibility * 0.2 +
      contextAlignment * 0.2
    );

    const contextBoost = (preferenceScore * urgencyFactor - 0.5) * 0.4; // Max ±0.4

    const finalScore = Math.max(0, Math.min(1, baseScore + contextBoost));

    const reasons = this.generateContextReasons(
      goal,
      contextAlignment,
      urgencyFactor,
      feasibilityScore,
      sourceContact,
      targetContact
    );

    // Add preference-based reasons
    if (communicationCompatibility >= 0.8) {
      reasons.push(`Excellent communication style match (${(communicationCompatibility * 100).toFixed(0)}% compatible)`);
    }
    if (workingStyleCompatibility >= 0.8) {
      reasons.push(`Strong working style compatibility (${(workingStyleCompatibility * 100).toFixed(0)}% compatible)`);
    }
    if (geographicCompatibility >= 0.9) {
      reasons.push('Geographic preferences align well');
    }

    return {
      baseScore,
      contextBoost,
      finalScore,
      contextAlignment,
      urgencyFactor,
      feasibilityScore,
      reasons,
    };
  }

  /**
   * Calculate how well a match aligns with current context
   */
  private calculateContextAlignment(
    goal: ContextualGoal,
    source: Contact,
    target: Contact
  ): number {
    const weights = this.contextWeights.get(goal.context) || new Map();

    let alignmentScore = 0;
    let totalWeight = 0;

    for (const [factor, weight] of weights.entries()) {
      const factorScore = this.evaluateFactor(factor, goal, source, target);
      alignmentScore += factorScore * weight;
      totalWeight += weight;
    }

    return totalWeight > 0 ? alignmentScore / totalWeight : 0.5;
  }

  /**
   * Evaluate a specific context factor
   */
  private evaluateFactor(
    factor: string,
    goal: ContextualGoal,
    source: Contact,
    target: Contact
  ): number {
    switch (factor) {
      case 'funding_capacity':
        return this.evaluateFundingCapacity(goal, target);

      case 'industry_expertise':
        return this.evaluateIndustryExpertise(source, target);

      case 'skills_match':
        return this.evaluateSkillsMatch(goal, source, target);

      case 'customer_fit':
        return this.evaluateCustomerFit(goal, target);

      case 'strategic_alignment':
        return this.evaluateStrategicAlignment(source, target);

      case 'expertise_gap':
        return this.evaluateExpertiseGap(source, target);

      default:
        return 0.5; // Neutral score for unknown factors
    }
  }

  /**
   * Evaluate funding capacity for fundraising context
   */
  private evaluateFundingCapacity(goal: ContextualGoal, target: Contact): number {
    // Check if target has funding-related offerings
    const fundingKeywords = ['funding', 'investment', 'capital', 'investor', 'vc'];
    const offerings = (target.offerings || []).join(' ').toLowerCase();

    const hasFunding = fundingKeywords.some(keyword => offerings.includes(keyword));

    // Check for investment stage match
    const goalNeeds = goal.specificNeeds.join(' ').toLowerCase();
    const stageMatch = ['seed', 'series a', 'series b'].some(stage => {
      return goalNeeds.includes(stage) && offerings.includes(stage);
    });

    return hasFunding ? (stageMatch ? 1.0 : 0.7) : 0.2;
  }

  /**
   * Evaluate industry expertise overlap
   */
  private evaluateIndustryExpertise(source: Contact, target: Contact): number {
    if (!source.industry || !target.industry) return 0.5;

    // Same industry = high score
    if (source.industry.toLowerCase() === target.industry.toLowerCase()) {
      return 1.0;
    }

    // Related industries (would need industry taxonomy)
    return 0.4;
  }

  /**
   * Evaluate skills match for hiring context
   */
  private evaluateSkillsMatch(goal: ContextualGoal, source: Contact, target: Contact): number {
    const requiredSkills = new Set(goal.specificNeeds.map(s => s.toLowerCase()));
    const targetSkills = new Set((target.skills || []).map(s => s.toLowerCase()));

    if (requiredSkills.size === 0 || targetSkills.size === 0) return 0.5;

    const matchedSkills = [...requiredSkills].filter(skill => targetSkills.has(skill));
    return matchedSkills.length / requiredSkills.size;
  }

  /**
   * Evaluate customer fit for business development
   */
  private evaluateCustomerFit(goal: ContextualGoal, target: Contact): number {
    // Check if target's needs match what source offers
    const targetNeeds = (target.needs || []).join(' ').toLowerCase();
    const goalOfferings = goal.specificNeeds.join(' ').toLowerCase();

    // Also check free text details if available
    const needsDetails = (target.metadata?.needsDetails || '').toLowerCase();
    const combinedNeeds = `${targetNeeds} ${needsDetails}`;

    const needsMatch = combinedNeeds.split(' ').some(need =>
      need.length > 2 && goalOfferings.includes(need)
    );

    // Check company size/stage if relevant
    const hasDecisionMakingPower = ['ceo', 'cto', 'vp', 'director', 'head'].some(title =>
      (target.title || '').toLowerCase().includes(title)
    );

    return needsMatch ? (hasDecisionMakingPower ? 1.0 : 0.7) : 0.3;
  }

  /**
   * Evaluate strategic alignment for partnerships
   */
  private evaluateStrategicAlignment(source: Contact, target: Contact): number {
    let alignmentScore = 0.5;

    // Industry overlap
    if (source.industry && target.industry &&
        source.industry.toLowerCase() === target.industry.toLowerCase()) {
      alignmentScore += 0.2;
    }

    // Complementary offerings
    const sourceOfferings = new Set((source.offerings || []).map(o => o.toLowerCase()));
    const targetNeeds = new Set((target.needs || []).map(n => n.toLowerCase()));
    const targetOfferings = new Set((target.offerings || []).map(o => o.toLowerCase()));
    const sourceNeeds = new Set((source.needs || []).map(n => n.toLowerCase()));

    // Also consider free text details
    const sourceOfferingsDetails = (source.metadata?.offeringsDetails || '').toLowerCase();
    const targetNeedsDetails = (target.metadata?.needsDetails || '').toLowerCase();
    const targetOfferingsDetails = (target.metadata?.offeringsDetails || '').toLowerCase();
    const sourceNeedsDetails = (source.metadata?.needsDetails || '').toLowerCase();

    // Check if they complement each other
    const sourceCanHelp = [...sourceOfferings].some(offer =>
      [...targetNeeds].some(need => need.includes(offer) || offer.includes(need))
    ) || (sourceOfferingsDetails && targetNeedsDetails &&
         this.hasSemanticOverlap(sourceOfferingsDetails, targetNeedsDetails));

    const targetCanHelp = [...targetOfferings].some(offer =>
      [...sourceNeeds].some(need => need.includes(offer) || offer.includes(need))
    ) || (targetOfferingsDetails && sourceNeedsDetails &&
         this.hasSemanticOverlap(targetOfferingsDetails, sourceNeedsDetails));

    if (sourceCanHelp && targetCanHelp) alignmentScore += 0.3;
    else if (sourceCanHelp || targetCanHelp) alignmentScore += 0.15;

    return Math.min(1.0, alignmentScore);
  }

  /**
   * Check for semantic overlap between two text strings
   */
  private hasSemanticOverlap(text1: string, text2: string): boolean {
    if (!text1 || !text2) return false;

    // Simple word overlap check (can be enhanced with NLP)
    const words1 = text1.toLowerCase().split(/\s+/).filter(w => w.length > 3);
    const words2 = text2.toLowerCase().split(/\s+/).filter(w => w.length > 3);

    const commonWords = words1.filter(w => words2.includes(w));
    return commonWords.length >= 2; // At least 2 significant words in common
  }

  /**
   * Evaluate communication style compatibility
   */
  private evaluateCommunicationStyleCompatibility(
    sourceCommunicationStyle?: string[],
    targetCommunicationStyle?: string[]
  ): number {
    if (!sourceCommunicationStyle || !targetCommunicationStyle) return 0.5;
    if (sourceCommunicationStyle.length === 0 || targetCommunicationStyle.length === 0) return 0.5;

    const sourceSet = new Set(sourceCommunicationStyle.map(s => s.toLowerCase()));
    const targetSet = new Set(targetCommunicationStyle.map(s => s.toLowerCase()));

    const commonStyles = [...sourceSet].filter(s => targetSet.has(s));
    const overlapRatio = commonStyles.length / Math.min(sourceSet.size, targetSet.size);

    // High overlap is great, but even 1 common style is good
    if (overlapRatio >= 0.5) return 1.0;
    if (overlapRatio >= 0.3) return 0.8;
    if (commonStyles.length >= 1) return 0.6;
    return 0.3; // No common communication styles
  }

  /**
   * Evaluate working style compatibility
   */
  private evaluateWorkingStyleCompatibility(
    sourceWorkingStyle?: string[],
    targetWorkingStyle?: string[]
  ): number {
    if (!sourceWorkingStyle || !targetWorkingStyle) return 0.5;
    if (sourceWorkingStyle.length === 0 || targetWorkingStyle.length === 0) return 0.5;

    const sourceSet = new Set(sourceWorkingStyle.map(s => s.toLowerCase()));
    const targetSet = new Set(targetWorkingStyle.map(s => s.toLowerCase()));

    const commonStyles = [...sourceSet].filter(s => targetSet.has(s));
    const overlapRatio = commonStyles.length / Math.min(sourceSet.size, targetSet.size);

    // Check for complementary styles (e.g., structured + detail-oriented)
    const complementaryPairs = [
      ['highly structured', 'detail-oriented'],
      ['flexible/adaptive', 'creative'],
      ['collaborative', 'team-oriented'],
      ['data-driven', 'analytical'],
      ['strategic', 'big picture'],
    ];

    let hasComplementary = false;
    for (const [style1, style2] of complementaryPairs) {
      if ((sourceSet.has(style1) && targetSet.has(style2)) ||
          (sourceSet.has(style2) && targetSet.has(style1))) {
        hasComplementary = true;
        break;
      }
    }

    if (overlapRatio >= 0.5) return 1.0;
    if (overlapRatio >= 0.3 || hasComplementary) return 0.8;
    if (commonStyles.length >= 1) return 0.6;
    return 0.4; // No common working styles (not necessarily bad)
  }

  /**
   * Evaluate geographic compatibility
   */
  private evaluateGeographicCompatibility(
    sourceGeographicPref?: string,
    targetGeographicPref?: string,
    sourceLocation?: string,
    targetLocation?: string
  ): number {
    // If either prefers remote-first, geography doesn't matter much
    if (sourceGeographicPref === 'remote-first' || targetGeographicPref === 'remote-first') {
      return 1.0;
    }

    // If both prefer global, that's a match
    if (sourceGeographicPref === 'global' && targetGeographicPref === 'global') {
      return 1.0;
    }

    // If locations are provided, check compatibility
    if (sourceLocation && targetLocation) {
      const sourceLower = sourceLocation.toLowerCase();
      const targetLower = targetLocation.toLowerCase();

      // Same city
      if (sourceLower === targetLower) {
        return 1.0;
      }

      // Check if in same region (simple check - can be enhanced)
      const sourceParts = sourceLower.split(',').map(p => p.trim());
      const targetParts = targetLower.split(',').map(p => p.trim());

      // Same country/state
      if (sourceParts.length > 1 && targetParts.length > 1) {
        if (sourceParts[sourceParts.length - 1] === targetParts[targetParts.length - 1]) {
          if (sourceGeographicPref === 'national' || targetGeographicPref === 'national') {
            return 0.9;
          }
          return 0.7; // Same country but might prefer local
        }
      }
    }

    // Default: moderate compatibility
    return 0.5;
  }

  /**
   * Check if deal breakers conflict with match
   */
  private checkDealBreakers(
    dealBreakers?: string,
    targetProfile?: Contact
  ): boolean {
    if (!dealBreakers) return true; // No deal breakers, all good

    const dealBreakerText = dealBreakers.toLowerCase();

    // Simple keyword checks (can be enhanced with NLP)
    const criticalKeywords = [
      'must have',
      'must be',
      'required',
      'essential',
      'non-negotiable',
    ];

    // If deal breakers are specified, do basic compatibility check
    // This is simplified - in production, would use more sophisticated matching
    if (criticalKeywords.some(keyword => dealBreakerText.includes(keyword))) {
      // Extract requirements and check if target meets them
      // For now, return true to not filter out matches
      // In production, implement proper requirement extraction and matching
      return true;
    }

    return true;
  }

  /**
   * Evaluate expertise gap for mentorship
   */
  private evaluateExpertiseGap(source: Contact, target: Contact): number {
    // For mentorship, we want target to have significantly more expertise
    const sourceSkills = new Set((source.skills || []).map(s => s.toLowerCase()));
    const targetSkills = new Set((target.skills || []).map(s => s.toLowerCase()));

    // Check if target has skills source wants to learn
    const learningOpportunities = (source.needs || [])
      .filter(need => {
        const needLower = need.toLowerCase();
        return [...targetSkills].some(skill => needLower.includes(skill));
      });

    // Check seniority differential (from titles)
    const seniorityDiff = this.calculateSeniorityDiff(source, target);

    const skillGapScore = Math.min(1.0, learningOpportunities.length * 0.3);
    return (skillGapScore + seniorityDiff) / 2;
  }

  /**
   * Calculate seniority differential
   */
  private calculateSeniorityDiff(source: Contact, target: Contact): number {
    const seniorityLevels = ['junior', 'mid', 'senior', 'lead', 'principal', 'vp', 'director', 'c-level'];

    const sourceSeniority = this.getSeniorityLevel(source.title || '');
    const targetSeniority = this.getSeniorityLevel(target.title || '');

    const diff = targetSeniority - sourceSeniority;

    // Ideal gap is 2-3 levels
    if (diff >= 2 && diff <= 3) return 1.0;
    if (diff === 1) return 0.7;
    if (diff >= 4) return 0.8;
    return 0.3;
  }

  /**
   * Get seniority level from title
   */
  private getSeniorityLevel(title: string): number {
    const titleLower = title.toLowerCase();

    if (titleLower.includes('ceo') || titleLower.includes('cto') || titleLower.includes('cfo')) return 7;
    if (titleLower.includes('vp') || titleLower.includes('vice president')) return 6;
    if (titleLower.includes('director')) return 5;
    if (titleLower.includes('principal')) return 4;
    if (titleLower.includes('lead') || titleLower.includes('staff')) return 3;
    if (titleLower.includes('senior')) return 2;
    if (titleLower.includes('junior')) return 0;
    return 1; // Default mid-level
  }

  /**
   * Calculate urgency factor based on timeframe
   */
  private calculateUrgencyFactor(goal: ContextualGoal): number {
    const urgencyMap = {
      immediate: 1.0,
      short_term: 0.8,
      medium_term: 0.6,
      long_term: 0.4,
    };

    return urgencyMap[goal.timeframe] * goal.priority;
  }

  /**
   * Calculate feasibility of the match
   */
  private calculateFeasibility(goal: ContextualGoal, target: Contact): number {
    let feasibility = 1.0;

    // Check geographic constraints
    if (goal.constraints?.geographic && target.location) {
      const isInRegion = goal.constraints.geographic.some(region =>
        target.location?.toLowerCase().includes(region.toLowerCase())
      );
      if (!isInRegion) feasibility *= 0.7;
    }

    // Check industry constraints
    if (goal.constraints?.industry && target.industry) {
      const isInIndustry = goal.constraints.industry.some(industry =>
        target.industry?.toLowerCase().includes(industry.toLowerCase())
      );
      if (!isInIndustry) feasibility *= 0.6;
    }

    return feasibility;
  }

  /**
   * Generate context-specific reasons for the match
   */
  private generateContextReasons(
    goal: ContextualGoal,
    alignment: number,
    urgency: number,
    feasibility: number,
    source: Contact,
    target: Contact
  ): string[] {
    const reasons: string[] = [];

    // Add context-specific reasons
    switch (goal.context) {
      case MatchContext.FUNDRAISING:
        if (alignment > 0.7) {
          reasons.push(`Strong investor profile match for ${goal.timeframe} fundraising`);
        }
        if ((target.offerings || []).some(o => o.toLowerCase().includes('funding'))) {
          reasons.push(`${target.name} offers funding in relevant stage`);
        }
        break;

      case MatchContext.HIRING:
        if (alignment > 0.7) {
          reasons.push(`Excellent skills match for your hiring needs`);
        }
        const matchedSkills = (goal.specificNeeds || []).filter(skill =>
          (target.skills || []).some(s => s.toLowerCase().includes(skill.toLowerCase()))
        );
        if (matchedSkills.length > 0) {
          reasons.push(`Has ${matchedSkills.length} of ${goal.specificNeeds.length} required skills`);
        }
        break;

      case MatchContext.BUSINESS_DEVELOPMENT:
        if (alignment > 0.7) {
          reasons.push(`High potential customer fit`);
        }
        if ((target.needs || []).length > 0) {
          reasons.push(`Has expressed needs you can address`);
        }
        break;
    }

    // Add urgency reason
    if (urgency > 0.8) {
      reasons.push(`Time-sensitive opportunity - ${goal.timeframe} timeframe`);
    }

    // Add feasibility concerns
    if (feasibility < 0.7) {
      reasons.push(`Note: Some constraints may need flexibility`);
    }

    return reasons;
  }

  /**
   * Rank matches based on multiple active goals
   */
  rankMatchesForGoals(
    matches: Match[],
    goals: ContextualGoal[],
    sourceContact: Contact,
    targetContacts: Map<string, Contact>
  ): Array<{
    match: Match;
    contextScores: Map<MatchContext, ContextualMatchScore>;
    weightedScore: number;
    primaryContext: MatchContext;
  }> {
    const results = matches.map(match => {
      const target = targetContacts.get(match.targetContact.id);
      if (!target) return null;

      const contextScores = new Map<MatchContext, ContextualMatchScore>();
      let weightedScore = 0;
      let primaryContext = goals[0]?.context || MatchContext.NETWORKING;
      let highestScore = 0;

      // Calculate score for each goal
      for (const goal of goals) {
        const contextScore = this.scoreMatchInContext(match, goal, sourceContact, target);
        contextScores.set(goal.context, contextScore);

        // Weight by goal priority
        const contribution = contextScore.finalScore * goal.priority;
        weightedScore += contribution;

        // Track primary context (highest scoring)
        if (contextScore.finalScore > highestScore) {
          highestScore = contextScore.finalScore;
          primaryContext = goal.context;
        }
      }

      // Normalize by total priority
      const totalPriority = goals.reduce((sum, g) => sum + g.priority, 0);
      weightedScore = totalPriority > 0 ? weightedScore / totalPriority : weightedScore;

      return {
        match,
        contextScores,
        weightedScore,
        primaryContext,
      };
    }).filter(r => r !== null);

    // Sort by weighted score
    return results.sort((a, b) => b!.weightedScore - a!.weightedScore);
  }
}
