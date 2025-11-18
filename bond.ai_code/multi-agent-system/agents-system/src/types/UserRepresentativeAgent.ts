/**
 * User Representative Agent
 * Autonomous agent that represents a user in agent-to-agent negotiations
 * Knows what the user needs and offers, negotiates on their behalf
 */

import {
  UserRepresentativeAgent as IUserRepresentativeAgent,
  AgentType,
  AgentCapability,
  UserProfile,
  UserNeed,
  UserOffering,
  NegotiationStyle,
  ConversationMessage,
  MessageType,
  ProposedTerms,
  MatchTerms,
  Position,
  NegotiationPoint,
  Benefit,
  MutualBenefit,
  NegotiationRecord,
  Priority,
  Urgency
} from './types';
import { Contact, IntelligenceAnalysis } from '../types';

export class UserRepresentativeAgent implements IUserRepresentativeAgent {
  id: string;
  type: AgentType.USER_REPRESENTATIVE = AgentType.USER_REPRESENTATIVE;
  name: string;
  specialization?: string;
  capabilities: AgentCapability[];
  config: any;

  userId: string;
  userContact: Contact;
  userAnalysis: IntelligenceAnalysis;
  userProfile: UserProfile;
  negotiationHistory: NegotiationRecord[];

  constructor(
    userId: string,
    userContact: Contact,
    userAnalysis: IntelligenceAnalysis,
    userProfile: UserProfile,
    config?: {
      negotiationStyle?: NegotiationStyle;
      riskTolerance?: number;
      minAcceptableScore?: number;
    }
  ) {
    this.id = `agent-${userId}`;
    this.name = `${userContact.name}'s Representative`;
    this.userId = userId;
    this.userContact = userContact;
    this.userAnalysis = userAnalysis;
    this.userProfile = userProfile;
    this.negotiationHistory = [];

    this.capabilities = [
      AgentCapability.NEGOTIATE,
      AgentCapability.ANALYZE,
      AgentCapability.EVALUATE,
      AgentCapability.LEARN
    ];

    this.config = {
      negotiationStyle: config?.negotiationStyle || this.determineNegotiationStyle(),
      riskTolerance: config?.riskTolerance ?? 0.5,
      minAcceptableScore: config?.minAcceptableScore ?? 0.6,
      learningEnabled: true
    };
  }

  /**
   * Generate introduction message for another agent
   */
  generateIntroduction(otherAgent: IUserRepresentativeAgent): ConversationMessage {
    const content = this.craftIntroductionMessage(otherAgent);

    return {
      id: `msg-${Date.now()}-intro`,
      from: this.id,
      to: otherAgent.id,
      timestamp: new Date(),
      messageType: MessageType.INTRODUCTION,
      content,
      sentiment: 0.7
    };
  }

  /**
   * Craft personalized introduction message
   */
  private craftIntroductionMessage(otherAgent: IUserRepresentativeAgent): string {
    const userName = this.userContact.name;
    const userTitle = this.userContact.title || 'Professional';
    const userCompany = this.userContact.company || '';

    const otherName = otherAgent.userContact.name;

    // Identify top needs and offerings
    const topNeeds = this.userProfile.needs
      .filter(n => n.priority === Priority.CRITICAL || n.priority === Priority.HIGH)
      .slice(0, 2);

    const topOfferings = this.userProfile.offerings
      .filter(o => o.capacity > 0.5)
      .slice(0, 2);

    let message = `Hello! I'm representing ${userName}, ${userTitle}`;
    if (userCompany) message += ` at ${userCompany}`;
    message += `.

I'm reaching out on behalf of ${userName} to explore potential synergies with ${otherName}.

**What ${userName} is looking for:**
${topNeeds.map(n => `• ${n.description} (${n.priority} priority)`).join('\n')}

**What ${userName} can offer:**
${topOfferings.map(o => `• ${o.description}`).join('\n')}

I'd like to discuss how we might create mutual value. What are your thoughts on a potential collaboration?`;

    return message;
  }

  /**
   * Analyze incoming proposal and decide response
   */
  analyzeProposal(proposal: ProposedTerms): {
    shouldAccept: boolean;
    score: number;
    concerns: string[];
    counterOffer?: MatchTerms;
    rationale: string;
  } {
    // Calculate how well the proposal meets user needs
    const needsSatisfactionScore = this.calculateNeedsSatisfaction(proposal.terms);

    // Calculate value of what user must give up
    const givingCostScore = this.calculateGivingCost(proposal.terms);

    // Calculate overall value
    const overallScore = this.calculateProposalScore(
      needsSatisfactionScore,
      givingCostScore,
      proposal.terms
    );

    // Identify concerns
    const concerns = this.identifyConcerns(proposal.terms);

    // Decide if acceptable
    const shouldAccept =
      overallScore >= this.config.minAcceptableScore &&
      concerns.length === 0;

    // Generate counter offer if not accepting
    let counterOffer: MatchTerms | undefined;
    let rationale: string;

    if (!shouldAccept && overallScore > this.config.minAcceptableScore * 0.7) {
      // Close enough to counter-offer
      counterOffer = this.generateCounterOffer(proposal.terms, concerns);
      rationale = `The proposal is interesting but has some concerns: ${concerns.join(', ')}. I've prepared a counter-offer that addresses these issues.`;
    } else if (shouldAccept) {
      rationale = `This proposal aligns well with ${this.userContact.name}'s needs and offers fair value exchange. I recommend acceptance.`;
    } else {
      rationale = `Unfortunately, this proposal doesn't meet ${this.userContact.name}'s minimum requirements. The value exchange is not sufficient (score: ${(overallScore * 100).toFixed(0)}%, minimum: ${(this.config.minAcceptableScore * 100).toFixed(0)}%).`;
    }

    return {
      shouldAccept,
      score: overallScore,
      concerns,
      counterOffer,
      rationale
    };
  }

  /**
   * Calculate how well proposal satisfies user needs
   */
  private calculateNeedsSatisfaction(terms: MatchTerms): number {
    const userGets = terms.whatAgent1Gets; // Assuming this agent is agent1
    const criticalNeeds = this.userProfile.needs.filter(n =>
      n.priority === Priority.CRITICAL
    );
    const highNeeds = this.userProfile.needs.filter(n =>
      n.priority === Priority.HIGH
    );

    let satisfiedCritical = 0;
    let satisfiedHigh = 0;

    for (const item of userGets) {
      for (const need of criticalNeeds) {
        if (this.matchesNeed(item, need)) {
          satisfiedCritical++;
          break;
        }
      }
      for (const need of highNeeds) {
        if (this.matchesNeed(item, need)) {
          satisfiedHigh++;
          break;
        }
      }
    }

    const criticalSatisfaction = criticalNeeds.length > 0
      ? satisfiedCritical / criticalNeeds.length
      : 1;
    const highSatisfaction = highNeeds.length > 0
      ? satisfiedHigh / highNeeds.length
      : 1;

    // Critical needs are weighted 2x
    return (criticalSatisfaction * 0.7 + highSatisfaction * 0.3);
  }

  /**
   * Calculate cost of what user gives
   */
  private calculateGivingCost(terms: MatchTerms): number {
    const userGives = terms.whatAgent1Gives;
    let totalCost = 0;

    for (const item of userGives) {
      const offering = this.findMatchingOffering(item);
      if (offering) {
        // Higher capacity = lower cost (more available to give)
        const cost = 1 - offering.capacity;
        totalCost += cost;
      } else {
        // Unknown item = high cost
        totalCost += 0.8;
      }
    }

    // Normalize
    return userGives.length > 0 ? totalCost / userGives.length : 0;
  }

  /**
   * Calculate overall proposal score
   */
  private calculateProposalScore(
    needsSatisfaction: number,
    givingCost: number,
    terms: MatchTerms
  ): number {
    // Benefits should outweigh costs
    const benefit = needsSatisfaction;
    const cost = givingCost;

    // Apply negotiation style
    let score: number;

    switch (this.config.negotiationStyle) {
      case NegotiationStyle.COLLABORATIVE:
        // Win-win focused - good if both sides benefit
        score = benefit * 0.6 - cost * 0.4;
        break;

      case NegotiationStyle.COMPETITIVE:
        // Maximize own benefit
        score = benefit * 0.8 - cost * 0.2;
        break;

      case NegotiationStyle.ACCOMMODATING:
        // Relationship focused - lower cost concern
        score = benefit * 0.5 - cost * 0.5;
        break;

      case NegotiationStyle.COMPROMISING:
        // Balanced
        score = benefit * 0.5 - cost * 0.5;
        break;

      default:
        score = benefit - cost;
    }

    // Apply risk tolerance
    if (this.config.riskTolerance < 0.5) {
      // Risk averse - penalize uncertainty
      score *= 0.9;
    }

    return Math.max(0, Math.min(1, score));
  }

  /**
   * Identify concerns with proposal
   */
  private identifyConcerns(terms: MatchTerms): string[] {
    const concerns: string[] = [];

    // Check if critical needs are met
    const criticalNeeds = this.userProfile.needs.filter(n =>
      n.priority === Priority.CRITICAL
    );

    for (const need of criticalNeeds) {
      const isMet = terms.whatAgent1Gets.some(item =>
        this.matchesNeed(item, need)
      );
      if (!isMet) {
        concerns.push(`Critical need not addressed: ${need.description}`);
      }
    }

    // Check constraints
    if (this.userProfile.constraints.budgetConstraints) {
      const { min, max } = this.userProfile.constraints.budgetConstraints;
      // Simple check - would need more context in real implementation
      if (max && terms.whatAgent1Gives.some(item => item.toLowerCase().includes('funding'))) {
        concerns.push('Budget constraints may be exceeded');
      }
    }

    // Check deal breakers
    if (this.userProfile.preferences.dealBreakers) {
      for (const dealBreaker of this.userProfile.preferences.dealBreakers) {
        if (terms.whatAgent1Gives.some(item =>
          item.toLowerCase().includes(dealBreaker.toLowerCase())
        )) {
          concerns.push(`Deal breaker identified: ${dealBreaker}`);
        }
      }
    }

    return concerns;
  }

  /**
   * Generate counter offer addressing concerns
   */
  private generateCounterOffer(
    originalTerms: MatchTerms,
    concerns: string[]
  ): MatchTerms {
    const counterOffer: MatchTerms = {
      whatAgent1Gives: [...originalTerms.whatAgent1Gives],
      whatAgent1Gets: [...originalTerms.whatAgent1Gets],
      whatAgent2Gives: [...originalTerms.whatAgent2Gives],
      whatAgent2Gets: [...originalTerms.whatAgent2Gets],
      conditions: [...(originalTerms.conditions || [])],
      timeline: originalTerms.timeline,
      successMetrics: originalTerms.successMetrics
    };

    // Add unmet critical needs to what agent1 gets
    const criticalNeeds = this.userProfile.needs.filter(n =>
      n.priority === Priority.CRITICAL
    );

    for (const need of criticalNeeds) {
      const isMet = originalTerms.whatAgent1Gets.some(item =>
        this.matchesNeed(item, need)
      );
      if (!isMet) {
        counterOffer.whatAgent1Gets.push(need.description);
        // Add corresponding item to what agent2 gets (balanced exchange)
        const additionalOffering = this.userProfile.offerings.find(o =>
          o.capacity > 0.3
        );
        if (additionalOffering) {
          counterOffer.whatAgent1Gives.push(additionalOffering.description);
        }
      }
    }

    // Add conditions to address constraints
    if (concerns.some(c => c.includes('budget'))) {
      counterOffer.conditions = counterOffer.conditions || [];
      counterOffer.conditions.push('Payment terms to be structured within budget constraints');
    }

    return counterOffer;
  }

  /**
   * Create initial proposal based on compatibility
   */
  createProposal(otherAgent: IUserRepresentativeAgent): ProposedTerms {
    const matchedNeeds = this.findMatchedNeeds(otherAgent);
    const balancedTerms = this.createBalancedTerms(matchedNeeds, otherAgent);

    return {
      id: `proposal-${Date.now()}`,
      proposedBy: this.id,
      timestamp: new Date(),
      terms: balancedTerms,
      rationale: this.explainProposal(balancedTerms, matchedNeeds),
      status: 'proposed' as any
    };
  }

  /**
   * Find matched needs between users
   */
  private findMatchedNeeds(otherAgent: IUserRepresentativeAgent): {
    myNeedTheirOffering: Array<{ need: UserNeed; offering: UserOffering }>;
    theirNeedMyOffering: Array<{ need: UserNeed; offering: UserOffering }>;
  } {
    const matches = {
      myNeedTheirOffering: [] as Array<{ need: UserNeed; offering: UserOffering }>,
      theirNeedMyOffering: [] as Array<{ need: UserNeed; offering: UserOffering }>
    };

    // My needs matched with their offerings
    for (const myNeed of this.userProfile.needs) {
      for (const theirOffering of otherAgent.userProfile.offerings) {
        if (this.needMatchesOffering(myNeed, theirOffering)) {
          matches.myNeedTheirOffering.push({ need: myNeed, offering: theirOffering });
        }
      }
    }

    // Their needs matched with my offerings
    for (const theirNeed of otherAgent.userProfile.needs) {
      for (const myOffering of this.userProfile.offerings) {
        if (this.needMatchesOffering(theirNeed, myOffering)) {
          matches.theirNeedMyOffering.push({ need: theirNeed, offering: myOffering });
        }
      }
    }

    return matches;
  }

  /**
   * Create balanced terms from matched needs
   */
  private createBalancedTerms(
    matches: any,
    otherAgent: IUserRepresentativeAgent
  ): MatchTerms {
    const terms: MatchTerms = {
      whatAgent1Gives: [],
      whatAgent1Gets: [],
      whatAgent2Gives: [],
      whatAgent2Gets: [],
      conditions: [],
      successMetrics: []
    };

    // What I give (my offerings) = What they get
    const myOfferings = matches.theirNeedMyOffering.map((m: any) => m.offering.description);
    terms.whatAgent1Gives = myOfferings;
    terms.whatAgent2Gets = myOfferings;

    // What they give (their offerings) = What I get
    const theirOfferings = matches.myNeedTheirOffering.map((m: any) => m.offering.description);
    terms.whatAgent2Gives = theirOfferings;
    terms.whatAgent1Gets = theirOfferings;

    // Add conditions
    terms.conditions = [
      'Mutual confidentiality agreement',
      'Regular progress check-ins',
      'Clear success metrics to be defined'
    ];

    // Add success metrics based on goals
    if (this.userProfile.goals.length > 0) {
      terms.successMetrics = this.userProfile.goals
        .slice(0, 2)
        .map(g => g.successCriteria[0] || g.description);
    }

    // Set timeline based on urgency
    const urgentNeeds = this.userProfile.needs.filter(n =>
      n.urgency === Urgency.IMMEDIATE || n.urgency === Urgency.SHORT_TERM
    );
    terms.timeline = urgentNeeds.length > 0
      ? 'Short-term (within 1-2 months)'
      : 'Medium-term (3-6 months)';

    return terms;
  }

  /**
   * Explain why this proposal makes sense
   */
  private explainProposal(terms: MatchTerms, matches: any): string {
    let explanation = `This proposal is designed to create mutual value:\n\n`;

    explanation += `**For ${this.userContact.name}:**\n`;
    explanation += `Addresses ${matches.myNeedTheirOffering.length} critical need(s) by receiving:\n`;
    terms.whatAgent1Gets.slice(0, 3).forEach(item => {
      explanation += `  • ${item}\n`;
    });

    explanation += `\n**In exchange, ${this.userContact.name} provides:**\n`;
    terms.whatAgent1Gives.slice(0, 3).forEach(item => {
      explanation += `  • ${item}\n`;
    });

    explanation += `\nThis creates a balanced, win-win partnership opportunity.`;

    return explanation;
  }

  /**
   * Determine negotiation style from user profile and analysis
   */
  private determineNegotiationStyle(): NegotiationStyle {
    // Analyze personality traits
    const traits = this.userAnalysis.personalityProfile.traits;

    if (traits.agreeableness > 0.7) {
      return NegotiationStyle.COLLABORATIVE;
    } else if (traits.extraversion > 0.7 && traits.agreeableness < 0.5) {
      return NegotiationStyle.COMPETITIVE;
    } else if (traits.agreeableness > 0.6 && traits.conscientiousness > 0.6) {
      return NegotiationStyle.ACCOMMODATING;
    } else {
      return NegotiationStyle.COMPROMISING;
    }
  }

  /**
   * Check if need matches offering
   */
  private needMatchesOffering(need: UserNeed, offering: UserOffering): boolean {
    // Simple keyword matching - in production would use more sophisticated NLP
    const needKeywords = need.description.toLowerCase().split(' ');
    const offeringKeywords = offering.description.toLowerCase().split(' ');

    const commonWords = needKeywords.filter(word =>
      offeringKeywords.some(oWord => oWord.includes(word) || word.includes(oWord))
    );

    return commonWords.length >= 2;
  }

  /**
   * Check if item matches need
   */
  private matchesNeed(item: string, need: UserNeed): boolean {
    return item.toLowerCase().includes(need.description.toLowerCase()) ||
           need.description.toLowerCase().includes(item.toLowerCase());
  }

  /**
   * Find matching offering for an item
   */
  private findMatchingOffering(item: string): UserOffering | undefined {
    return this.userProfile.offerings.find(offering =>
      item.toLowerCase().includes(offering.description.toLowerCase()) ||
      offering.description.toLowerCase().includes(item.toLowerCase())
    );
  }

  /**
   * Record negotiation for learning
   */
  recordNegotiation(record: NegotiationRecord): void {
    this.negotiationHistory.push(record);

    if (this.config.learningEnabled) {
      this.learnFromNegotiation(record);
    }
  }

  /**
   * Learn from past negotiations
   */
  private learnFromNegotiation(record: NegotiationRecord): void {
    // Adjust risk tolerance based on outcomes
    if (record.outcome === 'agreement_reached' && record.agreement) {
      // Successful negotiation - maintain or slightly increase risk tolerance
      this.config.riskTolerance = Math.min(
        this.config.riskTolerance + 0.05,
        1
      );
    } else if (record.outcome === 'no_agreement') {
      // Failed negotiation - become slightly more conservative
      this.config.riskTolerance = Math.max(
        this.config.riskTolerance - 0.05,
        0
      );
    }
  }
}
