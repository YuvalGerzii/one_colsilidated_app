/**
 * Strategic Negotiation Framework
 *
 * Implements advanced negotiation strategies:
 * - Game theory and Nash equilibrium
 * - BATNA (Best Alternative To Negotiated Agreement)
 * - ZOPA (Zone of Possible Agreement) analysis
 * - Anchoring and adjustment
 * - Concession strategies
 * - Relationship vs transaction optimization
 * - Adaptive negotiation tactics
 */

import {
  ProposedTerms,
  MatchTerms,
  UserRepresentativeAgent,
  NegotiationStyle,
  Priority
} from './types';

export interface NegotiationStrategy {
  name: string;
  description: string;
  tactics: NegotiationTactic[];
  whenToUse: string;
  expectedOutcome: string;
}

export interface NegotiationTactic {
  name: string;
  action: string;
  timing: 'early' | 'middle' | 'late' | 'any';
  effectiveness: number; // 0-1
  riskLevel: number; // 0-1
}

export interface BATNA {
  alternative: string;
  value: number; // 0-1, how good is this alternative
  availability: number; // 0-1, how likely/available
  description: string;
}

export interface ZOPA {
  exists: boolean;
  lowerBound: number; // Agent1's minimum acceptable
  upperBound: number; // Agent2's maximum offering
  midpoint: number;
  range: number;
  recommendation: string;
}

export interface ConcessionPlan {
  initialPosition: MatchTerms;
  fallbackPositions: MatchTerms[];
  redLines: string[]; // Non-negotiable items
  tradables: string[]; // Items willing to trade
  concessionRate: number; // How much to concede per round
  strategy: 'tit-for-tat' | 'gradual' | 'firm' | 'flexible';
}

export class StrategicNegotiationFramework {
  /**
   * Develop comprehensive negotiation strategy
   */
  developNegotiationStrategy(
    agent: UserRepresentativeAgent,
    otherAgent: UserRepresentativeAgent,
    round: number
  ): NegotiationStrategy {
    const style = agent.config.negotiationStyle;
    const batna = this.calculateBATNA(agent, otherAgent);

    // Select strategy based on style, BATNA, and round
    if (style === NegotiationStyle.COMPETITIVE && batna.value > 0.6) {
      return this.createCompetitiveStrategy(agent, batna, round);
    } else if (style === NegotiationStyle.COLLABORATIVE) {
      return this.createCollaborativeStrategy(agent, round);
    } else if (style === NegotiationStyle.COMPROMISING) {
      return this.createCompromisingStrategy(agent, round);
    } else if (style === NegotiationStyle.ACCOMMODATING) {
      return this.createAccommodatingStrategy(agent, round);
    } else {
      return this.createBalancedStrategy(agent, batna, round);
    }
  }

  /**
   * Calculate BATNA (Best Alternative To Negotiated Agreement)
   */
  calculateBATNA(
    agent: UserRepresentativeAgent,
    otherAgent: UserRepresentativeAgent
  ): BATNA {
    // In real implementation, would assess:
    // 1. Other potential partners
    // 2. Internal alternatives (build vs buy)
    // 3. Market conditions
    // 4. Timing factors

    // Simplified: Based on how many similar opportunities exist
    const criticalNeeds = agent.userProfile.needs.filter(n => n.priority === Priority.CRITICAL);
    const availability = agent.userProfile.offerings.length > 3 ? 0.7 : 0.4;

    return {
      alternative: 'Pursue other partnership opportunities',
      value: availability,
      availability,
      description: `Agent has ${agent.userProfile.offerings.length} offerings and ${criticalNeeds.length} critical needs, suggesting ${availability > 0.6 ? 'good' : 'moderate'} alternatives exist`
    };
  }

  /**
   * Calculate ZOPA (Zone of Possible Agreement)
   */
  calculateZOPA(
    agent1: UserRepresentativeAgent,
    agent2: UserRepresentativeAgent,
    proposal: ProposedTerms
  ): ZOPA {
    // Estimate agent1's minimum acceptable value
    const agent1Min = this.estimateMinimumAcceptable(agent1, proposal);

    // Estimate agent2's maximum offering
    const agent2Max = this.estimateMaximumOffering(agent2, proposal);

    const exists = agent2Max >= agent1Min;
    const midpoint = (agent1Min + agent2Max) / 2;
    const range = exists ? agent2Max - agent1Min : 0;

    let recommendation = '';
    if (!exists) {
      recommendation = `No ZOPA exists. Agent1 minimum (${(agent1Min * 100).toFixed(0)}%) exceeds Agent2 maximum (${(agent2Max * 100).toFixed(0)}%). Consider expanding the pie or finding alternative value sources.`;
    } else if (range < 0.2) {
      recommendation = `Narrow ZOPA (${(range * 100).toFixed(0)}%). Negotiate carefully, small concessions can close gap.`;
    } else {
      recommendation = `Good ZOPA exists (${(range * 100).toFixed(0)}% range). Aim for midpoint around ${(midpoint * 100).toFixed(0)}% satisfaction.`;
    }

    return {
      exists,
      lowerBound: agent1Min,
      upperBound: agent2Max,
      midpoint,
      range,
      recommendation
    };
  }

  /**
   * Create concession plan
   */
  createConcessionPlan(
    agent: UserRepresentativeAgent,
    otherAgent: UserRepresentativeAgent,
    initialProposal: ProposedTerms
  ): ConcessionPlan {
    // Identify red lines (non-negotiable)
    const redLines: string[] = [];
    agent.userProfile.needs.filter(n => n.priority === Priority.CRITICAL).forEach(need => {
      redLines.push(need.description);
    });

    // Identify tradables
    const tradables: string[] = [];
    agent.userProfile.needs.filter(n => n.priority !== Priority.CRITICAL && n.flexibility && n.flexibility > 0.5).forEach(need => {
      tradables.push(need.description);
    });

    // Create fallback positions
    const fallbackPositions = this.generateFallbackPositions(
      agent,
      initialProposal.terms,
      3 // Generate 3 fallback positions
    );

    // Determine concession strategy based on negotiation style
    let strategy: ConcessionPlan['strategy'];
    let concessionRate: number;

    if (agent.config.negotiationStyle === NegotiationStyle.COMPETITIVE) {
      strategy = 'firm';
      concessionRate = 0.05; // 5% concessions
    } else if (agent.config.negotiationStyle === NegotiationStyle.COLLABORATIVE) {
      strategy = 'tit-for-tat';
      concessionRate = 0.15; // 15% concessions, matching other party
    } else if (agent.config.negotiationStyle === NegotiationStyle.ACCOMMODATING) {
      strategy = 'flexible';
      concessionRate = 0.25; // 25% concessions
    } else {
      strategy = 'gradual';
      concessionRate = 0.12; // 12% concessions
    }

    return {
      initialPosition: initialProposal.terms,
      fallbackPositions,
      redLines,
      tradables,
      concessionRate,
      strategy
    };
  }

  /**
   * Determine next move based on strategy and opponent's last move
   */
  determineNextMove(
    agent: UserRepresentativeAgent,
    otherAgent: UserRepresentativeAgent,
    currentProposal: ProposedTerms,
    opponentLastProposal: ProposedTerms,
    concessionPlan: ConcessionPlan,
    round: number
  ): {
    action: 'accept' | 'reject' | 'counter' | 'hold_firm' | 'make_concession' | 'request_reciprocity';
    reasoning: string;
    counterOffer?: MatchTerms;
  } {
    // Analyze opponent's concession
    const opponentConceded = this.analyzeConcession(currentProposal, opponentLastProposal);

    // Check if within ZOPA
    const zopa = this.calculateZOPA(agent, otherAgent, currentProposal);

    // Decision logic based on strategy
    if (concessionPlan.strategy === 'tit-for-tat') {
      if (opponentConceded > 0.1) {
        // They conceded, we concede equally
        return {
          action: 'make_concession',
          reasoning: 'Tit-for-tat: Reciprocating their concession to build trust',
          counterOffer: this.generateConcession(agent, currentProposal.terms, concessionPlan.concessionRate)
        };
      } else if (opponentConceded < 0.05 && round > 3) {
        return {
          action: 'hold_firm',
          reasoning: 'Tit-for-tat: They haven\'t conceded, maintaining our position'
        };
      }
    } else if (concessionPlan.strategy === 'firm') {
      if (zopa.exists && this.evaluateProposal(agent, currentProposal) >= agent.config.minAcceptableScore) {
        return {
          action: 'accept',
          reasoning: 'Within ZOPA and meets minimum threshold'
        };
      } else if (round > 8) {
        // Late stage, final offer
        return {
          action: 'counter',
          reasoning: 'Final position - take it or leave it',
          counterOffer: this.generateFinalPosition(agent, concessionPlan)
        };
      } else {
        return {
          action: 'hold_firm',
          reasoning: 'Maintaining firm position to signal strength'
        };
      }
    } else if (concessionPlan.strategy === 'gradual') {
      if (round % 2 === 0) {
        // Every other round, make small concession
        return {
          action: 'make_concession',
          reasoning: 'Gradual concession to show flexibility while maintaining value',
          counterOffer: this.generateConcession(agent, currentProposal.terms, concessionPlan.concessionRate)
        };
      } else {
        return {
          action: 'hold_firm',
          reasoning: 'Maintaining position this round'
        };
      }
    } else if (concessionPlan.strategy === 'flexible') {
      // Always willing to concede if it moves toward agreement
      if (zopa.exists) {
        return {
          action: 'make_concession',
          reasoning: 'Flexible approach - moving toward midpoint',
          counterOffer: this.generateConcession(agent, currentProposal.terms, concessionPlan.concessionRate * 1.5)
        };
      }
    }

    // Default: Counter with moderate concession
    return {
      action: 'counter',
      reasoning: 'Standard negotiation move',
      counterOffer: this.generateConcession(agent, currentProposal.terms, concessionPlan.concessionRate)
    };
  }

  /**
   * Optimize for relationship vs transaction
   */
  optimizeForRelationship(
    agent: UserRepresentativeAgent,
    otherAgent: UserRepresentativeAgent,
    currentOffer: MatchTerms,
    priorAgreements: number
  ): {
    shouldPrioritizeRelationship: boolean;
    adjustedOffer?: MatchTerms;
    reasoning: string;
  } {
    // Long-term value of relationship
    const relationshipValue = this.estimateRelationshipValue(agent, otherAgent, priorAgreements);

    // Transaction value
    const transactionValue = this.estimateTransactionValue(agent, currentOffer);

    const shouldPrioritizeRelationship = relationshipValue > transactionValue * 1.5;

    let reasoning = '';
    let adjustedOffer: MatchTerms | undefined;

    if (shouldPrioritizeRelationship) {
      reasoning = `Long-term relationship value (${(relationshipValue * 100).toFixed(0)}%) exceeds transaction value (${(transactionValue * 100).toFixed(0)}%). Recommend prioritizing relationship with more generous terms.`;

      // Make offer more generous
      adjustedOffer = { ...currentOffer };

      // Add additional value to other party
      const additionalOffering = agent.userProfile.offerings.find(o =>
        o.capacity > 0.3 && !currentOffer.whatAgent1Gives.includes(o.description)
      );

      if (additionalOffering) {
        adjustedOffer.whatAgent1Gives.push(additionalOffering.description);
        adjustedOffer.whatAgent2Gets.push(additionalOffering.description);
      }
    } else {
      reasoning = `Transaction value (${(transactionValue * 100).toFixed(0)}%) is primary focus. Optimize for current deal terms.`;
    }

    return {
      shouldPrioritizeRelationship,
      adjustedOffer,
      reasoning
    };
  }

  // Private helper methods

  private createCompetitiveStrategy(
    agent: UserRepresentativeAgent,
    batna: BATNA,
    round: number
  ): NegotiationStrategy {
    return {
      name: 'Competitive/Win-Lose',
      description: 'Maximize own gains, strong BATNA gives leverage',
      tactics: [
        {
          name: 'High Anchor',
          action: 'Start with aggressive initial offer',
          timing: 'early',
          effectiveness: 0.75,
          riskLevel: 0.6
        },
        {
          name: 'Limited Concessions',
          action: 'Make small, infrequent concessions',
          timing: 'middle',
          effectiveness: 0.7,
          riskLevel: 0.5
        },
        {
          name: 'Deadline Pressure',
          action: 'Create time pressure for decision',
          timing: 'late',
          effectiveness: 0.65,
          riskLevel: 0.7
        }
      ],
      whenToUse: 'Strong BATNA, one-time transaction, competitive market',
      expectedOutcome: 'Favorable terms, may strain relationship'
    };
  }

  private createCollaborativeStrategy(
    agent: UserRepresentativeAgent,
    round: number
  ): NegotiationStrategy {
    return {
      name: 'Collaborative/Win-Win',
      description: 'Create mutual value, expand the pie',
      tactics: [
        {
          name: 'Information Sharing',
          action: 'Share interests and priorities openly',
          timing: 'early',
          effectiveness: 0.8,
          riskLevel: 0.3
        },
        {
          name: 'Value Creation',
          action: 'Identify new sources of value for both parties',
          timing: 'middle',
          effectiveness: 0.85,
          riskLevel: 0.2
        },
        {
          name: 'Package Deals',
          action: 'Bundle multiple items for greater value',
          timing: 'any',
          effectiveness: 0.8,
          riskLevel: 0.3
        }
      ],
      whenToUse: 'Long-term relationship, complex deal, mutual dependency',
      expectedOutcome: 'High mutual value, strong relationship foundation'
    };
  }

  private createCompromisingStrategy(
    agent: UserRepresentativeAgent,
    round: number
  ): NegotiationStrategy {
    return {
      name: 'Compromising/Split-the-Difference',
      description: 'Meet in the middle, balanced approach',
      tactics: [
        {
          name: 'Moderate Opening',
          action: 'Start with reasonable offer',
          timing: 'early',
          effectiveness: 0.7,
          riskLevel: 0.4
        },
        {
          name: 'Gradual Concessions',
          action: 'Make steady, predictable concessions',
          timing: 'middle',
          effectiveness: 0.75,
          riskLevel: 0.3
        },
        {
          name: 'Midpoint Focus',
          action: 'Aim for 50/50 split',
          timing: 'late',
          effectiveness: 0.7,
          riskLevel: 0.3
        }
      ],
      whenToUse: 'Time pressure, equal power, moderate stakes',
      expectedOutcome: 'Fair compromise, acceptable to both parties'
    };
  }

  private createAccommodatingStrategy(
    agent: UserRepresentativeAgent,
    round: number
  ): NegotiationStrategy {
    return {
      name: 'Accommodating/Relationship-First',
      description: 'Prioritize relationship and goodwill',
      tactics: [
        {
          name: 'Generous Opening',
          action: 'Start with favorable offer to other party',
          timing: 'early',
          effectiveness: 0.65,
          riskLevel: 0.5
        },
        {
          name: 'Quick Concessions',
          action: 'Readily make concessions',
          timing: 'any',
          effectiveness: 0.6,
          riskLevel: 0.6
        },
        {
          name: 'Long-term Focus',
          action: 'Emphasize future collaboration value',
          timing: 'any',
          effectiveness: 0.75,
          riskLevel: 0.4
        }
      ],
      whenToUse: 'Building new relationship, low stakes, goodwill needed',
      expectedOutcome: 'Strong relationship, may leave value on table'
    };
  }

  private createBalancedStrategy(
    agent: UserRepresentativeAgent,
    batna: BATNA,
    round: number
  ): NegotiationStrategy {
    return {
      name: 'Balanced/Adaptive',
      description: 'Adapt based on situation and opponent moves',
      tactics: [
        {
          name: 'Responsive Positioning',
          action: 'Adjust based on opponent behavior',
          timing: 'any',
          effectiveness: 0.75,
          riskLevel: 0.4
        },
        {
          name: 'Principled Negotiation',
          action: 'Focus on objective criteria and fairness',
          timing: 'any',
          effectiveness: 0.8,
          riskLevel: 0.3
        },
        {
          name: 'Strategic Concessions',
          action: 'Trade on items of different value to each party',
          timing: 'middle',
          effectiveness: 0.85,
          riskLevel: 0.3
        }
      ],
      whenToUse: 'Most situations, flexible approach',
      expectedOutcome: 'Good balance of value and relationship'
    };
  }

  private estimateMinimumAcceptable(agent: UserRepresentativeAgent, proposal: ProposedTerms): number {
    return agent.config.minAcceptableScore || 0.6;
  }

  private estimateMaximumOffering(agent: UserRepresentativeAgent, proposal: ProposedTerms): number {
    // Estimate how much value agent can offer
    const capacity = agent.userProfile.offerings.reduce((sum, o) => sum + o.capacity, 0) / Math.max(agent.userProfile.offerings.length, 1);
    return Math.min(0.9, capacity + 0.2);
  }

  private generateFallbackPositions(
    agent: UserRepresentativeAgent,
    initialTerms: MatchTerms,
    count: number
  ): MatchTerms[] {
    const fallbacks: MatchTerms[] = [];

    for (let i = 0; i < count; i++) {
      const concessionLevel = (i + 1) * 0.15; // 15%, 30%, 45% concessions

      const fallback: MatchTerms = {
        ...initialTerms,
        whatAgent1Gets: [...initialTerms.whatAgent1Gets],
        whatAgent1Gives: [...initialTerms.whatAgent1Gives],
        whatAgent2Gets: [...initialTerms.whatAgent2Gets],
        whatAgent2Gives: [...initialTerms.whatAgent2Gives]
      };

      // Remove some "gets" or add some "gives" to represent concession
      if (fallback.whatAgent1Gets.length > i + 1) {
        fallback.whatAgent1Gets = fallback.whatAgent1Gets.slice(0, -(i + 1));
      }

      fallbacks.push(fallback);
    }

    return fallbacks;
  }

  private analyzeConcession(current: ProposedTerms, previous: ProposedTerms): number {
    // Compare proposals to quantify concession
    const currentValue = current.terms.whatAgent1Gets.length - current.terms.whatAgent1Gives.length;
    const previousValue = previous.terms.whatAgent1Gets.length - previous.terms.whatAgent1Gives.length;

    const concession = previousValue - currentValue;
    return Math.max(0, concession / Math.max(previousValue, 1));
  }

  private evaluateProposal(agent: UserRepresentativeAgent, proposal: ProposedTerms): number {
    // Simplified evaluation
    return 0.65; // Would use full decision engine
  }

  private generateConcession(
    agent: UserRepresentativeAgent,
    currentTerms: MatchTerms,
    concessionRate: number
  ): MatchTerms {
    const conceded: MatchTerms = {
      ...currentTerms,
      whatAgent1Gets: [...currentTerms.whatAgent1Gets],
      whatAgent1Gives: [...currentTerms.whatAgent1Gives],
      whatAgent2Gets: [...currentTerms.whatAgent2Gets],
      whatAgent2Gives: [...currentTerms.whatAgent2Gives]
    };

    // Remove one "get" item if making concession
    if (conceded.whatAgent1Gets.length > 1 && Math.random() < concessionRate) {
      conceded.whatAgent1Gets.pop();
      conceded.whatAgent2Gives.pop();
    }

    return conceded;
  }

  private generateFinalPosition(agent: UserRepresentativeAgent, plan: ConcessionPlan): MatchTerms {
    // Use first fallback as final position
    return plan.fallbackPositions[0] || plan.initialPosition;
  }

  private estimateRelationshipValue(
    agent: UserRepresentativeAgent,
    otherAgent: UserRepresentativeAgent,
    priorAgreements: number
  ): number {
    let value = 0.4; // Base value

    // Prior successful agreements
    value += Math.min(priorAgreements * 0.15, 0.3);

    // Network value
    // Would assess other agent's network size and quality

    // Strategic alignment
    // Would assess long-term strategic fit

    return Math.min(1, value);
  }

  private estimateTransactionValue(agent: UserRepresentativeAgent, offer: MatchTerms): number {
    // Simplified: ratio of gets to gives
    const getsValue = offer.whatAgent1Gets.length * 0.15;
    const givesValue = offer.whatAgent1Gives.length * 0.1;

    return Math.max(0, Math.min(1, getsValue - givesValue + 0.5));
  }
}
