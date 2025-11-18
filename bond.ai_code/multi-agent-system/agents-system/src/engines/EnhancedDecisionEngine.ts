/**
 * Enhanced Decision-Making Engine
 *
 * Advanced decision-making for agent negotiations with:
 * - Multi-criteria decision analysis (MCDA)
 * - Strategic reasoning and game theory
 * - Risk-adjusted valuations
 * - Alternative generation
 * - Decision trees and scenario analysis
 * - Integration with behavior analysis agents for strategic insights
 */

import {
  ProposedTerms,
  MatchTerms,
  UserRepresentativeAgent,
  UserNeed,
  UserOffering,
  Priority,
  Urgency,
  NegotiationStyle
} from './types';
import { IBehaviorAgent, DecisionContext } from './BehaviorAgentTypes';

export interface DecisionAnalysis {
  shouldAccept: boolean;
  confidence: number; // 0-1
  overallScore: number; // 0-1
  multiCriteriaScores: {
    needsSatisfaction: number;
    costEfficiency: number;
    riskLevel: number;
    strategicAlignment: number;
    timingOptimality: number;
    relationshipValue: number;
  };
  concerns: string[];
  strengths: string[];
  alternativeActions: AlternativeAction[];
  strategicRecommendation: string;
  scenarioAnalysis: ScenarioOutcome[];
  behaviorInsights?: string[]; // From behavior analysis agents
}

export interface AlternativeAction {
  action: 'accept' | 'reject' | 'counter' | 'request_clarification' | 'propose_alternative';
  description: string;
  expectedOutcome: string;
  probability: number; // Probability of success
  expectedValue: number; // Expected utility
  counterOffer?: MatchTerms;
}

export interface ScenarioOutcome {
  scenario: string;
  probability: number;
  outcome: string;
  value: number;
}

export interface DecisionContext {
  negotiationRound: number;
  previousOffers: ProposedTerms[];
  deadlineProximity?: number; // 0-1, how close to deadline
  competitiveAlternatives?: number; // Other options available
  relationshipHistory?: number; // Prior successful agreements
}

export class EnhancedDecisionEngine {
  /**
   * Analyze proposal using multi-criteria decision analysis
   */
  async analyzeProposalAdvanced(
    agent: UserRepresentativeAgent,
    otherAgent: UserRepresentativeAgent,
    proposal: ProposedTerms,
    context: DecisionContext,
    behaviorAdvisors?: IBehaviorAgent[]
  ): Promise<DecisionAnalysis> {
    // Multi-criteria scoring
    const multiCriteriaScores = this.calculateMultiCriteriaScores(
      agent,
      otherAgent,
      proposal,
      context
    );

    // Calculate weighted overall score
    const overallScore = this.calculateWeightedScore(multiCriteriaScores, agent.config);

    // Identify concerns and strengths
    const concerns = this.identifyDetailedConcerns(agent, proposal, multiCriteriaScores);
    const strengths = this.identifyStrengths(agent, proposal, multiCriteriaScores);

    // Generate alternative actions
    const alternativeActions = await this.generateAlternatives(
      agent,
      otherAgent,
      proposal,
      multiCriteriaScores,
      context
    );

    // Scenario analysis
    const scenarioAnalysis = this.performScenarioAnalysis(
      agent,
      proposal,
      alternativeActions,
      context
    );

    // Strategic recommendation
    const strategicRecommendation = this.generateStrategicRecommendation(
      multiCriteriaScores,
      alternativeActions,
      scenarioAnalysis,
      agent.config
    );

    // Get behavior insights if advisors provided
    let behaviorInsights: string[] | undefined;
    if (behaviorAdvisors && behaviorAdvisors.length > 0) {
      behaviorInsights = await this.getBehaviorInsights(
        behaviorAdvisors,
        proposal,
        agent,
        context
      );
    }

    // Decision with confidence
    const { shouldAccept, confidence } = this.makeDecision(
      overallScore,
      multiCriteriaScores,
      alternativeActions,
      agent.config,
      context
    );

    return {
      shouldAccept,
      confidence,
      overallScore,
      multiCriteriaScores,
      concerns,
      strengths,
      alternativeActions,
      strategicRecommendation,
      scenarioAnalysis,
      behaviorInsights
    };
  }

  /**
   * Calculate multi-criteria scores
   */
  private calculateMultiCriteriaScores(
    agent: UserRepresentativeAgent,
    otherAgent: UserRepresentativeAgent,
    proposal: ProposedTerms,
    context: DecisionContext
  ): DecisionAnalysis['multiCriteriaScores'] {
    return {
      needsSatisfaction: this.scoreNeedsSatisfaction(agent, proposal),
      costEfficiency: this.scoreCostEfficiency(agent, proposal),
      riskLevel: this.scoreRiskLevel(agent, proposal, context),
      strategicAlignment: this.scoreStrategicAlignment(agent, proposal),
      timingOptimality: this.scoreTimingOptimality(agent, proposal, context),
      relationshipValue: this.scoreRelationshipValue(agent, otherAgent, context)
    };
  }

  /**
   * Score how well proposal satisfies needs
   */
  private scoreNeedsSatisfaction(agent: UserRepresentativeAgent, proposal: ProposedTerms): number {
    const needs = agent.userProfile.needs;
    const gets = proposal.terms.whatAgent1Gets;

    let totalWeight = 0;
    let satisfiedWeight = 0;

    for (const need of needs) {
      const weight = this.priorityToWeight(need.priority);
      totalWeight += weight;

      // Check if need is satisfied
      const isSatisfied = gets.some(item =>
        this.matchesNeed(item, need) || this.partiallyMatchesNeed(item, need)
      );

      if (isSatisfied) {
        // Check quality of satisfaction
        const matchQuality = this.assessMatchQuality(gets, need);
        satisfiedWeight += weight * matchQuality;
      }
    }

    return totalWeight > 0 ? satisfiedWeight / totalWeight : 0;
  }

  /**
   * Score cost efficiency
   */
  private scoreCostEfficiency(agent: UserRepresentativeAgent, proposal: ProposedTerms): number {
    const gives = proposal.terms.whatAgent1Gives;
    const gets = proposal.terms.whatAgent1Gets;

    // Calculate what we give (cost)
    let costScore = 0;
    for (const item of gives) {
      const offering = agent.userProfile.offerings.find(o =>
        this.matchesOffering(item, o)
      );

      if (offering) {
        // Higher capacity = lower cost
        costScore += (1 - offering.capacity) * 0.5;
      } else {
        // Unknown item = higher cost
        costScore += 0.8;
      }
    }

    const avgCost = gives.length > 0 ? costScore / gives.length : 0;

    // Calculate value received
    const valueReceived = this.scoreNeedsSatisfaction(agent, proposal);

    // Cost efficiency = value/cost ratio
    if (avgCost === 0) return valueReceived;

    const efficiency = valueReceived / Math.max(avgCost, 0.1);

    return Math.min(1, efficiency);
  }

  /**
   * Score risk level (lower is better)
   */
  private scoreRiskLevel(
    agent: UserRepresentativeAgent,
    proposal: ProposedTerms,
    context: DecisionContext
  ): number {
    let risk = 0;

    // Commitment risk
    const commitmentSize = proposal.terms.whatAgent1Gives.length;
    risk += Math.min(commitmentSize * 0.1, 0.3);

    // Uncertainty risk
    if (!proposal.terms.timeline) risk += 0.1;
    if (!proposal.terms.successMetrics || proposal.terms.successMetrics.length === 0) risk += 0.15;
    if (!proposal.terms.conditions || proposal.terms.conditions.length === 0) risk += 0.1;

    // Novelty risk (no prior relationship)
    if (!context.relationshipHistory || context.relationshipHistory === 0) {
      risk += 0.2;
    }

    // Deal breaker risk
    const dealBreakers = agent.userProfile.preferences.dealBreakers || [];
    for (const dealBreaker of dealBreakers) {
      if (proposal.terms.whatAgent1Gives.some(item =>
        item.toLowerCase().includes(dealBreaker.toLowerCase())
      )) {
        risk += 0.4; // Major risk
      }
    }

    // Constraint violations
    if (this.violatesConstraints(agent, proposal)) {
      risk += 0.3;
    }

    return Math.max(0, 1 - Math.min(risk, 1)); // Invert so higher is better
  }

  /**
   * Score strategic alignment
   */
  private scoreStrategicAlignment(agent: UserRepresentativeAgent, proposal: ProposedTerms): number {
    let alignment = 0.5; // Baseline

    const goals = agent.userProfile.goals;

    // Check alignment with goals
    for (const goal of goals) {
      const contributesToGoal = proposal.terms.whatAgent1Gets.some(item =>
        goal.successCriteria.some(criteria =>
          item.toLowerCase().includes(criteria.toLowerCase()) ||
          criteria.toLowerCase().includes(item.toLowerCase())
        )
      );

      if (contributesToGoal) {
        const urgencyWeight = this.urgencyToWeight(goal.timeframe);
        alignment += urgencyWeight * 0.3;
      }
    }

    // Check industry alignment
    const preferredIndustries = agent.userProfile.preferences.preferredIndustries || [];
    // Would need other agent's industry info for full check

    return Math.min(1, alignment);
  }

  /**
   * Score timing optimality
   */
  private scoreTimingOptimality(
    agent: UserRepresentativeAgent,
    proposal: ProposedTerms,
    context: DecisionContext
  ): number {
    let timingScore = 0.7; // Baseline

    // Check if timeline matches urgent needs
    const urgentNeeds = agent.userProfile.needs.filter(n =>
      n.urgency === Urgency.IMMEDIATE || n.urgency === Urgency.SHORT_TERM
    );

    if (urgentNeeds.length > 0) {
      const timelineStr = proposal.terms.timeline?.toLowerCase() || '';
      if (timelineStr.includes('immediate') || timelineStr.includes('short')) {
        timingScore += 0.2;
      } else if (timelineStr.includes('long')) {
        timingScore -= 0.2;
      }
    }

    // Deadline pressure
    if (context.deadlineProximity && context.deadlineProximity > 0.7) {
      timingScore += 0.15; // Pressure to decide
    }

    // Competitive alternatives
    if (context.competitiveAlternatives && context.competitiveAlternatives > 2) {
      timingScore -= 0.1; // Can afford to wait
    }

    return Math.max(0, Math.min(1, timingScore));
  }

  /**
   * Score relationship value
   */
  private scoreRelationshipValue(
    agent: UserRepresentativeAgent,
    otherAgent: UserRepresentativeAgent,
    context: DecisionContext
  ): number {
    let relationshipValue = 0.5;

    // Prior successful agreements
    if (context.relationshipHistory) {
      relationshipValue += Math.min(context.relationshipHistory * 0.15, 0.3);
    }

    // Network value (if other agent is well-connected)
    // Would need network analysis data

    // Reputation value
    // Would need reputation score

    return Math.min(1, relationshipValue);
  }

  /**
   * Calculate weighted overall score
   */
  private calculateWeightedScore(
    scores: DecisionAnalysis['multiCriteriaScores'],
    config: any
  ): number {
    // Default weights
    const defaultWeights = {
      needsSatisfaction: 0.30,
      costEfficiency: 0.20,
      riskLevel: 0.15,
      strategicAlignment: 0.15,
      timingOptimality: 0.10,
      relationshipValue: 0.10
    };

    // Adjust weights based on negotiation style
    const weights = { ...defaultWeights };

    if (config.negotiationStyle === NegotiationStyle.COMPETITIVE) {
      weights.needsSatisfaction = 0.35;
      weights.costEfficiency = 0.25;
      weights.relationshipValue = 0.05;
    } else if (config.negotiationStyle === NegotiationStyle.COLLABORATIVE) {
      weights.relationshipValue = 0.20;
      weights.strategicAlignment = 0.20;
      weights.costEfficiency = 0.15;
    } else if (config.negotiationStyle === NegotiationStyle.ACCOMMODATING) {
      weights.relationshipValue = 0.25;
      weights.needsSatisfaction = 0.25;
      weights.riskLevel = 0.10;
    }

    // Adjust for risk tolerance
    if (config.riskTolerance < 0.5) {
      weights.riskLevel *= 1.5; // Risk-averse
      // Renormalize
      const sum = Object.values(weights).reduce((a, b) => a + b, 0);
      Object.keys(weights).forEach(key => {
        weights[key as keyof typeof weights] /= sum;
      });
    }

    // Calculate weighted score
    return (
      scores.needsSatisfaction * weights.needsSatisfaction +
      scores.costEfficiency * weights.costEfficiency +
      scores.riskLevel * weights.riskLevel +
      scores.strategicAlignment * weights.strategicAlignment +
      scores.timingOptimality * weights.timingOptimality +
      scores.relationshipValue * weights.relationshipValue
    );
  }

  /**
   * Identify detailed concerns
   */
  private identifyDetailedConcerns(
    agent: UserRepresentativeAgent,
    proposal: ProposedTerms,
    scores: DecisionAnalysis['multiCriteriaScores']
  ): string[] {
    const concerns: string[] = [];

    if (scores.needsSatisfaction < 0.6) {
      const unsatisfiedNeeds = agent.userProfile.needs
        .filter(n => n.priority === Priority.CRITICAL || n.priority === Priority.HIGH)
        .filter(need =>
          !proposal.terms.whatAgent1Gets.some(item => this.matchesNeed(item, need))
        );

      unsatisfiedNeeds.forEach(need => {
        concerns.push(`Critical need not addressed: ${need.description}`);
      });
    }

    if (scores.costEfficiency < 0.5) {
      concerns.push('Cost-benefit ratio is unfavorable - giving too much relative to value received');
    }

    if (scores.riskLevel < 0.6) {
      concerns.push('Risk level is higher than acceptable threshold');

      if (this.violatesConstraints(agent, proposal)) {
        concerns.push('Proposal violates budget or operational constraints');
      }
    }

    if (scores.strategicAlignment < 0.5) {
      concerns.push('Proposal does not align well with strategic objectives');
    }

    if (scores.timingOptimality < 0.5) {
      concerns.push('Timeline does not match urgency of needs');
    }

    // Check deal breakers
    const dealBreakers = agent.userProfile.preferences.dealBreakers || [];
    for (const dealBreaker of dealBreakers) {
      if (proposal.terms.whatAgent1Gives.some(item =>
        item.toLowerCase().includes(dealBreaker.toLowerCase())
      )) {
        concerns.push(`Deal breaker identified: ${dealBreaker}`);
      }
    }

    return concerns;
  }

  /**
   * Identify strengths
   */
  private identifyStrengths(
    agent: UserRepresentativeAgent,
    proposal: ProposedTerms,
    scores: DecisionAnalysis['multiCriteriaScores']
  ): string[] {
    const strengths: string[] = [];

    if (scores.needsSatisfaction > 0.7) {
      strengths.push('Excellently addresses core needs');
    }

    if (scores.costEfficiency > 0.7) {
      strengths.push('Highly cost-effective value exchange');
    }

    if (scores.riskLevel > 0.7) {
      strengths.push('Low-risk opportunity with clear terms');
    }

    if (scores.strategicAlignment > 0.7) {
      strengths.push('Strong alignment with strategic goals');
    }

    if (scores.timingOptimality > 0.7) {
      strengths.push('Timeline matches current priorities perfectly');
    }

    if (scores.relationshipValue > 0.7) {
      strengths.push('Valuable relationship and network benefits');
    }

    // Check must-haves
    const mustHaves = agent.userProfile.preferences.mustHaves || [];
    const satisfiedMustHaves = mustHaves.filter(mustHave =>
      proposal.terms.whatAgent1Gets.some(item =>
        item.toLowerCase().includes(mustHave.toLowerCase())
      )
    );

    if (satisfiedMustHaves.length > 0) {
      strengths.push(`Satisfies must-have requirements: ${satisfiedMustHaves.join(', ')}`);
    }

    return strengths;
  }

  /**
   * Generate alternative actions
   */
  private async generateAlternatives(
    agent: UserRepresentativeAgent,
    otherAgent: UserRepresentativeAgent,
    proposal: ProposedTerms,
    scores: DecisionAnalysis['multiCriteriaScores'],
    context: DecisionContext
  ): Promise<AlternativeAction[]> {
    const alternatives: AlternativeAction[] = [];

    // Option 1: Accept as-is
    const acceptValue = scores.needsSatisfaction * 0.5 + scores.costEfficiency * 0.3 + scores.riskLevel * 0.2;
    alternatives.push({
      action: 'accept',
      description: 'Accept current proposal without modifications',
      expectedOutcome: 'Immediate agreement, move to implementation',
      probability: acceptValue > 0.7 ? 0.9 : 0.7,
      expectedValue: acceptValue
    });

    // Option 2: Reject
    const rejectValue = 1 - acceptValue;
    alternatives.push({
      action: 'reject',
      description: 'Decline proposal and end negotiations',
      expectedOutcome: 'No agreement, preserve resources for other opportunities',
      probability: 0.95,
      expectedValue: rejectValue * 0.3 // Rejection has value if proposal is bad
    });

    // Option 3: Counter-offer
    if (scores.needsSatisfaction > 0.4 && scores.needsSatisfaction < 0.8) {
      const counterOffer = this.generateCounterOffer(agent, otherAgent, proposal, scores);
      const counterValue = acceptValue * 1.2; // Potential to improve

      alternatives.push({
        action: 'counter',
        description: 'Propose adjusted terms addressing key concerns',
        expectedOutcome: 'Continued negotiation with improved terms',
        probability: 0.6,
        expectedValue: counterValue * 0.6, // Discounted by probability
        counterOffer
      });
    }

    // Option 4: Request clarification
    if (scores.riskLevel < 0.6) {
      alternatives.push({
        action: 'request_clarification',
        description: 'Request more information before deciding',
        expectedOutcome: 'Better information for decision-making',
        probability: 0.8,
        expectedValue: acceptValue * 0.9 // Slightly lower due to delay
      });
    }

    // Option 5: Propose alternative structure
    if (scores.strategicAlignment < 0.6 && scores.needsSatisfaction > 0.5) {
      alternatives.push({
        action: 'propose_alternative',
        description: 'Suggest entirely different collaboration structure',
        expectedOutcome: 'Explore new win-win frameworks',
        probability: 0.5,
        expectedValue: acceptValue * 1.3 // Higher potential but riskier
      });
    }

    // Sort by expected value
    alternatives.sort((a, b) => b.expectedValue - a.expectedValue);

    return alternatives;
  }

  /**
   * Generate improved counter-offer
   */
  private generateCounterOffer(
    agent: UserRepresentativeAgent,
    otherAgent: UserRepresentativeAgent,
    proposal: ProposedTerms,
    scores: DecisionAnalysis['multiCriteriaScores']
  ): MatchTerms {
    const counter: MatchTerms = {
      whatAgent1Gives: [...proposal.terms.whatAgent1Gives],
      whatAgent1Gets: [...proposal.terms.whatAgent1Gets],
      whatAgent2Gives: [...proposal.terms.whatAgent2Gives],
      whatAgent2Gets: [...proposal.terms.whatAgent2Gets],
      conditions: [...(proposal.terms.conditions || [])],
      timeline: proposal.terms.timeline,
      successMetrics: proposal.terms.successMetrics
    };

    // Add unsatisfied critical needs
    if (scores.needsSatisfaction < 0.7) {
      const criticalNeeds = agent.userProfile.needs
        .filter(n => n.priority === Priority.CRITICAL)
        .filter(need => !proposal.terms.whatAgent1Gets.some(item => this.matchesNeed(item, need)));

      criticalNeeds.forEach(need => {
        counter.whatAgent1Gets.push(need.description);
        // Balance by adding something we can give
        const additionalOffering = agent.userProfile.offerings.find(o => o.capacity > 0.4);
        if (additionalOffering && !counter.whatAgent1Gives.includes(additionalOffering.description)) {
          counter.whatAgent1Gives.push(additionalOffering.description);
          counter.whatAgent2Gets.push(additionalOffering.description);
        }
      });
    }

    // Reduce commitments if cost-efficiency is low
    if (scores.costEfficiency < 0.5 && counter.whatAgent1Gives.length > 2) {
      // Remove least valuable giving item
      counter.whatAgent1Gives = counter.whatAgent1Gives.slice(0, -1);
      counter.whatAgent2Gets = counter.whatAgent2Gets.slice(0, -1);
    }

    // Add risk mitigation conditions
    if (scores.riskLevel < 0.6) {
      if (!counter.conditions) counter.conditions = [];
      counter.conditions.push('Phased implementation with milestone reviews');
      counter.conditions.push('Clear termination clauses for both parties');
      counter.conditions.push('Regular progress reporting and adjustments');
    }

    return counter;
  }

  /**
   * Perform scenario analysis
   */
  private performScenarioAnalysis(
    agent: UserRepresentativeAgent,
    proposal: ProposedTerms,
    alternatives: AlternativeAction[],
    context: DecisionContext
  ): ScenarioOutcome[] {
    const scenarios: ScenarioOutcome[] = [];

    // Best case scenario
    scenarios.push({
      scenario: 'Best Case: Partnership exceeds expectations',
      probability: 0.25,
      outcome: 'All objectives achieved, relationship strengthens, new opportunities emerge',
      value: 1.0
    });

    // Expected case
    scenarios.push({
      scenario: 'Expected Case: Partnership meets core objectives',
      probability: 0.50,
      outcome: 'Primary needs satisfied, stable collaboration',
      value: alternatives.find(a => a.action === 'accept')?.expectedValue || 0.7
    });

    // Worst case
    scenarios.push({
      scenario: 'Worst Case: Partnership underperforms or fails',
      probability: 0.15,
      outcome: 'Objectives not met, resources wasted, relationship strained',
      value: 0.2
    });

    // No deal scenario
    scenarios.push({
      scenario: 'No Deal: Reject and pursue alternatives',
      probability: 0.10,
      outcome: 'Resources preserved, opportunity cost of lost partnership',
      value: alternatives.find(a => a.action === 'reject')?.expectedValue || 0.3
    });

    return scenarios;
  }

  /**
   * Generate strategic recommendation
   */
  private generateStrategicRecommendation(
    scores: DecisionAnalysis['multiCriteriaScores'],
    alternatives: AlternativeAction[],
    scenarios: ScenarioOutcome[],
    config: any
  ): string {
    const bestAlternative = alternatives[0];
    const avgScore = Object.values(scores).reduce((a, b) => a + b, 0) / Object.keys(scores).length;

    let recommendation = '';

    if (bestAlternative.action === 'accept' && avgScore > 0.7) {
      recommendation = `**Strong Recommendation to Accept**: This proposal scores highly across all criteria (${(avgScore * 100).toFixed(0)}% average). The risk-reward profile is favorable, and this aligns well with strategic objectives. Recommend proceeding with acceptance.`;
    } else if (bestAlternative.action === 'counter' && avgScore > 0.5) {
      recommendation = `**Recommendation to Counter**: The proposal shows promise (${(avgScore * 100).toFixed(0)}% score) but has addressable concerns. A counter-offer can improve terms while maintaining momentum. Key areas to improve: `;

      if (scores.needsSatisfaction < 0.7) recommendation += 'needs satisfaction, ';
      if (scores.costEfficiency < 0.6) recommendation += 'cost-efficiency, ';
      if (scores.riskLevel < 0.6) recommendation += 'risk mitigation';

      recommendation += `. Expected improvement: ${((bestAlternative.expectedValue - avgScore) * 100).toFixed(0)}%.`;
    } else if (bestAlternative.action === 'reject') {
      recommendation = `**Recommendation to Decline**: This proposal does not meet minimum requirements (${(avgScore * 100).toFixed(0)}% score vs ${(config.minAcceptableScore * 100).toFixed(0)}% threshold). The risk-reward profile is unfavorable. Recommend declining politely and preserving resources for better opportunities.`;
    } else if (bestAlternative.action === 'request_clarification') {
      recommendation = `**Recommendation to Seek Clarification**: The proposal has potential but contains significant uncertainties. Before deciding, request clarification on key points to reduce risk and improve decision confidence.`;
    } else {
      recommendation = `**Recommendation to Explore Alternatives**: Consider proposing an entirely different collaboration structure that better aligns with strategic objectives.`;
    }

    // Add scenario insights
    const expectedScenarioValue = scenarios.reduce((sum, s) => sum + s.probability * s.value, 0);
    recommendation += `\n\n**Expected Value Analysis**: Based on scenario analysis, the expected value is ${(expectedScenarioValue * 100).toFixed(0)}%.`;

    return recommendation;
  }

  /**
   * Make final decision with confidence
   */
  private makeDecision(
    overallScore: number,
    scores: DecisionAnalysis['multiCriteriaScores'],
    alternatives: AlternativeAction[],
    config: any,
    context: DecisionContext
  ): { shouldAccept: boolean; confidence: number } {
    const bestAlternative = alternatives[0];

    let shouldAccept = false;
    let confidence = 0.5;

    // Decision logic
    if (bestAlternative.action === 'accept' && overallScore >= config.minAcceptableScore) {
      shouldAccept = true;
      confidence = Math.min(0.95, overallScore + 0.1);
    } else {
      shouldAccept = false;
      confidence = Math.min(0.9, 1 - overallScore + 0.1);
    }

    // Adjust confidence based on variance in criteria scores
    const scoresArray = Object.values(scores);
    const avgScore = scoresArray.reduce((a, b) => a + b, 0) / scoresArray.length;
    const variance = scoresArray.reduce((sum, score) => sum + Math.pow(score - avgScore, 2), 0) / scoresArray.length;

    // High variance = lower confidence
    confidence *= (1 - variance * 0.3);

    // Deadline pressure affects confidence
    if (context.deadlineProximity && context.deadlineProximity > 0.8) {
      confidence *= 0.9; // Less time to analyze = slightly lower confidence
    }

    // Prior relationship increases confidence
    if (context.relationshipHistory && context.relationshipHistory > 2) {
      confidence = Math.min(0.95, confidence + 0.1);
    }

    return { shouldAccept, confidence: Math.max(0.1, Math.min(0.95, confidence)) };
  }

  /**
   * Get insights from behavior analysis agents
   */
  private async getBehaviorInsights(
    advisors: IBehaviorAgent[],
    proposal: ProposedTerms,
    agent: UserRepresentativeAgent,
    context: DecisionContext
  ): Promise<string[]> {
    const insights: string[] = [];

    // Sample 2-3 advisors for insights
    const selectedAdvisors = advisors.slice(0, Math.min(3, advisors.length));

    for (const advisor of selectedAdvisors) {
      try {
        const advice = await advisor.analyzeDecision(
          `Proposal: ${proposal.rationale}`,
          DecisionContext.NEGOTIATION,
          proposal.terms.whatAgent1Gets
        );

        insights.push(
          `${advisor.profile.name}: ${advice.reasoning}${advice.modifications.length > 0 ? ' Suggests: ' + advice.modifications[0] : ''}`
        );
      } catch (error) {
        // Silently skip if advisor fails
      }
    }

    return insights;
  }

  // Helper methods

  private priorityToWeight(priority: Priority): number {
    return {
      [Priority.CRITICAL]: 1.0,
      [Priority.HIGH]: 0.7,
      [Priority.MEDIUM]: 0.5,
      [Priority.LOW]: 0.3
    }[priority] || 0.5;
  }

  private urgencyToWeight(urgency: Urgency): number {
    return {
      [Urgency.IMMEDIATE]: 1.0,
      [Urgency.SHORT_TERM]: 0.8,
      [Urgency.MEDIUM_TERM]: 0.5,
      [Urgency.LONG_TERM]: 0.3
    }[urgency] || 0.5;
  }

  private matchesNeed(item: string, need: UserNeed): boolean {
    const itemLower = item.toLowerCase();
    const needLower = need.description.toLowerCase();
    return itemLower.includes(needLower) || needLower.includes(itemLower);
  }

  private partiallyMatchesNeed(item: string, need: UserNeed): boolean {
    const itemWords = item.toLowerCase().split(' ');
    const needWords = need.description.toLowerCase().split(' ');
    const commonWords = itemWords.filter(w => needWords.some(nw => nw.includes(w) || w.includes(nw)));
    return commonWords.length >= 2;
  }

  private matchesOffering(item: string, offering: UserOffering): boolean {
    const itemLower = item.toLowerCase();
    const offeringLower = offering.description.toLowerCase();
    return itemLower.includes(offeringLower) || offeringLower.includes(itemLower);
  }

  private assessMatchQuality(gets: string[], need: UserNeed): number {
    // How well does the match satisfy the need?
    let quality = 0.5;

    const matchingItems = gets.filter(item => this.matchesNeed(item, need));

    if (matchingItems.length > 0) {
      quality = 0.8;

      // Check if quantifiable
      if (need.quantifiable) {
        // Would need to parse quantities from items
        quality += 0.2;
      }
    }

    return Math.min(1, quality);
  }

  private violatesConstraints(agent: UserRepresentativeAgent, proposal: ProposedTerms): boolean {
    const constraints = agent.userProfile.constraints;

    // Check budget
    if (constraints.budgetConstraints) {
      // Would need monetary value parsing
    }

    // Check time availability
    if (constraints.timeAvailability) {
      // Would need time commitment parsing
    }

    // Check geographic constraints
    if (constraints.geographicConstraints && constraints.geographicConstraints.length > 0) {
      // Would need location parsing from proposal
    }

    return false; // Simplified
  }
}
