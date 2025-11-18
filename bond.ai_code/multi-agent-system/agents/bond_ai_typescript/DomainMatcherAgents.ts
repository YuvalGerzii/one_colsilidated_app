/**
 * Domain-Specific Matcher Agents
 * Specialized agents for different types of partnerships
 * Based on 2025 AI-powered matching research and best practices
 */

import {
  DomainMatcherAgent,
  AgentType,
  AgentCapability,
  MatchingDomain,
  MatchingStrategy,
  SuccessPattern,
  UserRepresentativeAgent,
  Priority,
  NeedCategory,
  OfferingCategory
} from './types';
import { IntelligenceAnalysis } from '../types';

/**
 * Base Domain Matcher
 */
abstract class BaseDomainMatcher implements DomainMatcherAgent {
  id: string;
  type: AgentType.DOMAIN_MATCHER = AgentType.DOMAIN_MATCHER;
  name: string;
  specialization?: string;
  capabilities: AgentCapability[];
  config: any;
  domain: MatchingDomain;
  matchingStrategies: MatchingStrategy[];
  successPatterns: SuccessPattern[];

  constructor(domain: MatchingDomain, name: string) {
    this.id = `domain-matcher-${domain}`;
    this.name = name;
    this.domain = domain;
    this.capabilities = [
      AgentCapability.MATCH,
      AgentCapability.ANALYZE,
      AgentCapability.EVALUATE,
      AgentCapability.LEARN
    ];
    this.config = {};
    this.matchingStrategies = [];
    this.successPatterns = [];
  }

  /**
   * Calculate domain-specific match score
   */
  abstract calculateMatchScore(
    agent1: UserRepresentativeAgent,
    agent2: UserRepresentativeAgent
  ): number;

  /**
   * Identify match potential and rationale
   */
  abstract identifyMatchPotential(
    agent1: UserRepresentativeAgent,
    agent2: UserRepresentativeAgent
  ): {
    score: number;
    rationale: string[];
    keyFactors: string[];
    risks: string[];
  };
}

/**
 * Investor-Startup Matcher
 * Specializes in matching investors with startups
 * Implements venture capital matching best practices
 */
export class InvestorStartupMatcher extends BaseDomainMatcher {
  constructor() {
    super(MatchingDomain.INVESTOR_STARTUP, 'Investor-Startup Matcher');

    this.matchingStrategies = [
      {
        name: 'Stage-Investment Alignment',
        description: 'Match investment stage with startup stage',
        scoringFunction: 'stageAlignment',
        weights: { stage: 0.4, amount: 0.3, industry: 0.3 },
        threshold: 0.7
      },
      {
        name: 'Industry Thesis Match',
        description: 'Match investor thesis with startup industry',
        scoringFunction: 'industryThesisMatch',
        weights: { industry: 0.5, technology: 0.3, market: 0.2 },
        threshold: 0.6
      },
      {
        name: 'Traction-Capital Fit',
        description: 'Match startup traction with capital requirements',
        scoringFunction: 'tractionCapitalFit',
        weights: { traction: 0.5, capital: 0.3, timeline: 0.2 },
        threshold: 0.65
      }
    ];

    this.successPatterns = [
      {
        pattern: 'AI/ML startup seeking seed funding from AI-focused fund',
        successRate: 0.85,
        conditions: ['Industry alignment', 'Technical expertise match', 'Stage appropriateness'],
        examples: ['OpenAI + Khosla Ventures', 'Anthropic + Spark Capital']
      },
      {
        pattern: 'Enterprise SaaS with revenue seeking Series A',
        successRate: 0.78,
        conditions: ['Proven revenue model', 'Growth trajectory', 'Market size'],
        examples: ['Notion + Index Ventures', 'Figma + Sequoia']
      }
    ];
  }

  calculateMatchScore(
    agent1: UserRepresentativeAgent,
    agent2: UserRepresentativeAgent
  ): number {
    // Identify investor and startup
    const { investor, startup } = this.identifyRoles(agent1, agent2);
    if (!investor || !startup) return 0;

    let totalScore = 0;
    let totalWeight = 0;

    // Stage alignment (40%)
    const stageScore = this.calculateStageAlignment(investor, startup);
    totalScore += stageScore * 0.4;
    totalWeight += 0.4;

    // Industry alignment (25%)
    const industryScore = this.calculateIndustryAlignment(investor, startup);
    totalScore += industryScore * 0.25;
    totalWeight += 0.25;

    // Capital fit (20%)
    const capitalScore = this.calculateCapitalFit(investor, startup);
    totalScore += capitalScore * 0.2;
    totalWeight += 0.2;

    // Strategic value (15%)
    const strategicScore = this.calculateStrategicValue(investor, startup);
    totalScore += strategicScore * 0.15;
    totalWeight += 0.15;

    return totalScore / totalWeight;
  }

  identifyMatchPotential(
    agent1: UserRepresentativeAgent,
    agent2: UserRepresentativeAgent
  ): {
    score: number;
    rationale: string[];
    keyFactors: string[];
    risks: string[];
  } {
    const { investor, startup } = this.identifyRoles(agent1, agent2);
    const score = this.calculateMatchScore(agent1, agent2);

    const rationale: string[] = [];
    const keyFactors: string[] = [];
    const risks: string[] = [];

    if (investor && startup) {
      // Industry alignment
      const investorIndustries = investor.userContact.industry || '';
      const startupIndustry = startup.userContact.industry || '';

      if (investorIndustries.toLowerCase().includes(startupIndustry.toLowerCase())) {
        rationale.push('Strong industry thesis alignment');
        keyFactors.push('Industry focus match');
      }

      // Funding needs
      const fundingNeeds = startup.userProfile.needs.filter(n =>
        n.category === NeedCategory.FUNDING
      );

      const capitalOfferings = investor.userProfile.offerings.filter(o =>
        o.category === OfferingCategory.CAPITAL
      );

      if (fundingNeeds.length > 0 && capitalOfferings.length > 0) {
        rationale.push('Clear funding need meets capital availability');
        keyFactors.push('Capital requirements match');
      }

      // Strategic value beyond capital
      const strategicOfferings = investor.userProfile.offerings.filter(o =>
        o.category !== OfferingCategory.CAPITAL
      );

      if (strategicOfferings.length > 2) {
        rationale.push('Investor offers strategic value beyond capital');
        keyFactors.push('Strategic support available');
      }

      // Risks
      if (fundingNeeds.some(n => n.urgency === 'immediate')) {
        risks.push('Urgent capital need may require faster diligence timeline');
      }

      if (!startup.userProfile.offerings.some(o => o.description.toLowerCase().includes('traction'))) {
        risks.push('Limited traction visibility may require deeper validation');
      }
    }

    return { score, rationale, keyFactors, risks };
  }

  private identifyRoles(
    agent1: UserRepresentativeAgent,
    agent2: UserRepresentativeAgent
  ): { investor?: UserRepresentativeAgent; startup?: UserRepresentativeAgent } {
    let investor, startup;

    // Check if agent has capital offerings and needs deal flow
    if (agent1.userProfile.offerings.some(o => o.category === OfferingCategory.CAPITAL)) {
      investor = agent1;
      startup = agent2;
    } else if (agent2.userProfile.offerings.some(o => o.category === OfferingCategory.CAPITAL)) {
      investor = agent2;
      startup = agent1;
    }

    return { investor, startup };
  }

  private calculateStageAlignment(
    investor: UserRepresentativeAgent,
    startup: UserRepresentativeAgent
  ): number {
    // In production, would analyze actual stage data
    return 0.8;
  }

  private calculateIndustryAlignment(
    investor: UserRepresentativeAgent,
    startup: UserRepresentativeAgent
  ): number {
    const investorIndustry = investor.userContact.industry?.toLowerCase() || '';
    const startupIndustry = startup.userContact.industry?.toLowerCase() || '';

    if (investorIndustry.includes(startupIndustry) || startupIndustry.includes(investorIndustry)) {
      return 1.0;
    }

    // Partial match
    const investorWords = investorIndustry.split(' ');
    const startupWords = startupIndustry.split(' ');
    const common = investorWords.filter(w => startupWords.includes(w));

    return common.length > 0 ? 0.7 : 0.3;
  }

  private calculateCapitalFit(
    investor: UserRepresentativeAgent,
    startup: UserRepresentativeAgent
  ): number {
    // Simplified - in production would compare actual funding amounts
    const capitalOfferings = investor.userProfile.offerings.filter(o =>
      o.category === OfferingCategory.CAPITAL
    );

    const fundingNeeds = startup.userProfile.needs.filter(n =>
      n.category === NeedCategory.FUNDING
    );

    return capitalOfferings.length > 0 && fundingNeeds.length > 0 ? 0.9 : 0.3;
  }

  private calculateStrategicValue(
    investor: UserRepresentativeAgent,
    startup: UserRepresentativeAgent
  ): number {
    const strategicOfferings = investor.userProfile.offerings.filter(o =>
      o.category !== OfferingCategory.CAPITAL
    );

    return Math.min(strategicOfferings.length / 3, 1);
  }
}

/**
 * Sales-Client Matcher
 * Specializes in matching sales professionals with potential clients
 */
export class SalesClientMatcher extends BaseDomainMatcher {
  constructor() {
    super(MatchingDomain.SALES_CLIENT, 'Sales-Client Matcher');

    this.successPatterns = [
      {
        pattern: 'Enterprise sales matching with growing companies',
        successRate: 0.82,
        conditions: ['Budget availability', 'Pain point match', 'Decision maker access'],
        examples: ['Salesforce enterprise deals', 'AWS enterprise adoption']
      }
    ];
  }

  calculateMatchScore(
    agent1: UserRepresentativeAgent,
    agent2: UserRepresentativeAgent
  ): number {
    const { seller, buyer } = this.identifyRoles(agent1, agent2);
    if (!seller || !buyer) return 0;

    // Pain-solution fit (40%)
    const painSolutionScore = this.calculatePainSolutionFit(seller, buyer) * 0.4;

    // Budget alignment (30%)
    const budgetScore = this.calculateBudgetAlignment(seller, buyer) * 0.3;

    // Decision-making fit (20%)
    const decisionScore = this.calculateDecisionMakerFit(buyer) * 0.2;

    // Timing (10%)
    const timingScore = this.calculateTimingAlignment(buyer) * 0.1;

    return painSolutionScore + budgetScore + decisionScore + timingScore;
  }

  identifyMatchPotential(
    agent1: UserRepresentativeAgent,
    agent2: UserRepresentativeAgent
  ): {
    score: number;
    rationale: string[];
    keyFactors: string[];
    risks: string[];
  } {
    const score = this.calculateMatchScore(agent1, agent2);
    const { seller, buyer } = this.identifyRoles(agent1, agent2);

    const rationale: string[] = [];
    const keyFactors: string[] = [];
    const risks: string[] = [];

    if (seller && buyer) {
      // Check pain point alignment
      const buyerNeeds = buyer.userProfile.needs;
      const sellerSolutions = seller.userProfile.offerings;

      const matchedNeeds = buyerNeeds.filter(need =>
        sellerSolutions.some(solution =>
          solution.description.toLowerCase().includes(need.description.toLowerCase().split(' ')[0])
        )
      );

      if (matchedNeeds.length > 0) {
        rationale.push('Clear pain point to solution alignment');
        keyFactors.push(`${matchedNeeds.length} matched pain points`);
      }

      // Check budget
      if (buyer.userProfile.constraints.budgetConstraints) {
        keyFactors.push('Budget defined');
      } else {
        risks.push('Budget not clearly defined');
      }

      // Check decision maker level
      const title = buyer.userContact.title?.toLowerCase() || '';
      if (title.includes('ceo') || title.includes('cto') || title.includes('vp')) {
        keyFactors.push('Decision maker access');
      } else {
        risks.push('May need executive buy-in');
      }
    }

    return { score, rationale, keyFactors, risks };
  }

  private identifyRoles(
    agent1: UserRepresentativeAgent,
    agent2: UserRepresentativeAgent
  ): { seller?: UserRepresentativeAgent; buyer?: UserRepresentativeAgent } {
    let seller, buyer;

    // Seller typically has technology/service offerings
    if (agent1.userProfile.offerings.some(o =>
      o.category === OfferingCategory.TECHNOLOGY ||
      o.description.toLowerCase().includes('solution')
    )) {
      seller = agent1;
      buyer = agent2;
    } else {
      seller = agent2;
      buyer = agent1;
    }

    return { seller, buyer };
  }

  private calculatePainSolutionFit(
    seller: UserRepresentativeAgent,
    buyer: UserRepresentativeAgent
  ): number {
    const buyerNeeds = buyer.userProfile.needs;
    const sellerSolutions = seller.userProfile.offerings;

    let matches = 0;
    for (const need of buyerNeeds) {
      for (const solution of sellerSolutions) {
        if (this.solutionAddressesNeed(solution.description, need.description)) {
          matches++;
          break;
        }
      }
    }

    return buyerNeeds.length > 0 ? matches / buyerNeeds.length : 0;
  }

  private calculateBudgetAlignment(
    seller: UserRepresentativeAgent,
    buyer: UserRepresentativeAgent
  ): number {
    return buyer.userProfile.constraints.budgetConstraints ? 0.8 : 0.5;
  }

  private calculateDecisionMakerFit(buyer: UserRepresentativeAgent): number {
    const title = buyer.userContact.title?.toLowerCase() || '';
    if (title.includes('ceo') || title.includes('chief')) return 1.0;
    if (title.includes('vp') || title.includes('director')) return 0.8;
    if (title.includes('manager')) return 0.6;
    return 0.4;
  }

  private calculateTimingAlignment(buyer: UserRepresentativeAgent): number {
    const urgentNeeds = buyer.userProfile.needs.filter(n =>
      n.urgency === 'immediate' || n.urgency === 'short_term'
    );
    return urgentNeeds.length > 0 ? 1.0 : 0.6;
  }

  private solutionAddressesNeed(solution: string, need: string): boolean {
    const solutionWords = solution.toLowerCase().split(' ');
    const needWords = need.toLowerCase().split(' ');
    const common = solutionWords.filter(w => needWords.includes(w));
    return common.length >= 2;
  }
}

/**
 * Partnership Matcher
 * Specializes in strategic partnership matching
 */
export class PartnershipMatcher extends BaseDomainMatcher {
  constructor() {
    super(MatchingDomain.PARTNERSHIP, 'Strategic Partnership Matcher');

    this.successPatterns = [
      {
        pattern: 'Complementary technology partnerships',
        successRate: 0.79,
        conditions: ['Technology complementarity', 'Market synergy', 'No direct competition'],
        examples: ['Stripe + Shopify', 'Slack + Salesforce']
      },
      {
        pattern: 'Distribution partnerships',
        successRate: 0.73,
        conditions: ['Non-competing products', 'Shared customer base', 'Channel alignment'],
        examples: ['AWS + Partner Network', 'Microsoft + System Integrators']
      }
    ];
  }

  calculateMatchScore(
    agent1: UserRepresentativeAgent,
    agent2: UserRepresentativeAgent
  ): number {
    // Strategic alignment (30%)
    const strategicScore = this.calculateStrategicAlignment(agent1, agent2) * 0.3;

    // Complementarity (30%)
    const complementarityScore = this.calculateComplementarity(agent1, agent2) * 0.3;

    // Market synergy (25%)
    const marketScore = this.calculateMarketSynergy(agent1, agent2) * 0.25;

    // Resource balance (15%)
    const balanceScore = this.calculateResourceBalance(agent1, agent2) * 0.15;

    return strategicScore + complementarityScore + marketScore + balanceScore;
  }

  identifyMatchPotential(
    agent1: UserRepresentativeAgent,
    agent2: UserRepresentativeAgent
  ): {
    score: number;
    rationale: string[];
    keyFactors: string[];
    risks: string[];
  } {
    const score = this.calculateMatchScore(agent1, agent2);

    const rationale: string[] = [];
    const keyFactors: string[] = [];
    const risks: string[] = [];

    // Check goal alignment
    const goals1 = agent1.userProfile.goals;
    const goals2 = agent2.userProfile.goals;

    if (goals1.length > 0 && goals2.length > 0) {
      rationale.push('Both parties have clear strategic goals');
      keyFactors.push('Goal-driven partnership');
    }

    // Check complementarity
    const needsMatch1 = agent1.userProfile.needs.filter(need =>
      agent2.userProfile.offerings.some(offering =>
        offering.description.toLowerCase().includes(need.description.toLowerCase())
      )
    );

    const needsMatch2 = agent2.userProfile.needs.filter(need =>
      agent1.userProfile.offerings.some(offering =>
        offering.description.toLowerCase().includes(need.description.toLowerCase())
      )
    );

    if (needsMatch1.length > 0 && needsMatch2.length > 0) {
      rationale.push('Strong bilateral complementarity');
      keyFactors.push('Mutual value exchange');
    } else if (needsMatch1.length === 0 && needsMatch2.length === 0) {
      risks.push('Limited clear value exchange identified');
    } else {
      risks.push('Unbalanced value exchange may need adjustment');
    }

    // Check for competition risks
    const industry1 = agent1.userContact.industry?.toLowerCase() || '';
    const industry2 = agent2.userContact.industry?.toLowerCase() || '';

    if (industry1 === industry2) {
      risks.push('Same industry may indicate competitive overlap');
    }

    return { score, rationale, keyFactors, risks };
  }

  private calculateStrategicAlignment(
    agent1: UserRepresentativeAgent,
    agent2: UserRepresentativeAgent
  ): number {
    // Compare goals and vision
    const goals1 = agent1.userProfile.goals;
    const goals2 = agent2.userProfile.goals;

    if (goals1.length === 0 || goals2.length === 0) return 0.5;

    // Simple alignment check
    return 0.75; // Placeholder
  }

  private calculateComplementarity(
    agent1: UserRepresentativeAgent,
    agent2: UserRepresentativeAgent
  ): number {
    const offerings1 = agent1.userProfile.offerings;
    const offerings2 = agent2.userProfile.offerings;

    // Higher score if offerings don't overlap (complementary)
    const overlap = offerings1.filter(o1 =>
      offerings2.some(o2 =>
        o1.category === o2.category
      )
    );

    return 1 - (overlap.length / Math.max(offerings1.length, offerings2.length, 1));
  }

  private calculateMarketSynergy(
    agent1: UserRepresentativeAgent,
    agent2: UserRepresentativeAgent
  ): number {
    // Check if they serve similar markets but don't compete
    const industry1 = agent1.userContact.industry?.toLowerCase() || '';
    const industry2 = agent2.userContact.industry?.toLowerCase() || '';

    // Adjacent industries = good synergy
    if (industry1.includes('tech') && industry2.includes('software')) return 0.9;

    return 0.6; // Default moderate synergy
  }

  private calculateResourceBalance(
    agent1: UserRepresentativeAgent,
    agent2: UserRepresentativeAgent
  ): number {
    const offerings1Count = agent1.userProfile.offerings.length;
    const offerings2Count = agent2.userProfile.offerings.length;

    // More balanced = better
    const ratio = Math.min(offerings1Count, offerings2Count) /
                  Math.max(offerings1Count, offerings2Count, 1);

    return ratio;
  }
}

/**
 * Mentor-Mentee Matcher
 * Specializes in mentorship matching
 */
export class MentorMenteeMatcher extends BaseDomainMatcher {
  constructor() {
    super(MatchingDomain.MENTOR_MENTEE, 'Mentor-Mentee Matcher');

    this.successPatterns = [
      {
        pattern: 'Experienced executive mentoring startup founder',
        successRate: 0.88,
        conditions: ['Industry experience', 'Complementary expertise', 'Time availability'],
        examples: ['Y Combinator model', 'First Round Capital mentorship']
      }
    ];
  }

  calculateMatchScore(
    agent1: UserRepresentativeAgent,
    agent2: UserRepresentativeAgent
  ): number {
    const { mentor, mentee } = this.identifyRoles(agent1, agent2);
    if (!mentor || !mentee) return 0;

    // Experience gap (35%)
    const experienceScore = this.calculateExperienceGap(mentor, mentee) * 0.35;

    // Expertise match (30%)
    const expertiseScore = this.calculateExpertiseMatch(mentor, mentee) * 0.3;

    // Learning style fit (20%)
    const learningScore = this.calculateLearningFit(mentor, mentee) * 0.2;

    // Availability (15%)
    const availabilityScore = this.calculateAvailability(mentor) * 0.15;

    return experienceScore + expertiseScore + learningScore + availabilityScore;
  }

  identifyMatchPotential(
    agent1: UserRepresentativeAgent,
    agent2: UserRepresentativeAgent
  ): {
    score: number;
    rationale: string[];
    keyFactors: string[];
    risks: string[];
  } {
    const score = this.calculateMatchScore(agent1, agent2);
    const { mentor, mentee } = this.identifyRoles(agent1, agent2);

    const rationale: string[] = [];
    const keyFactors: string[] = [];
    const risks: string[] = [];

    if (mentor && mentee) {
      rationale.push('Mentor-mentee relationship potential identified');

      // Check expertise alignment
      const mentorExpertise = mentor.userAnalysis.profileAnalysis.expertiseAreas;
      const menteeNeeds = mentee.userProfile.needs;

      const alignedAreas = menteeNeeds.filter(need =>
        mentorExpertise.some(expertise =>
          expertise.toLowerCase().includes(need.description.toLowerCase())
        )
      );

      if (alignedAreas.length > 0) {
        keyFactors.push('Expertise-need alignment');
      }

      // Check time availability
      if (mentor.userProfile.constraints.timeAvailability &&
          mentor.userProfile.constraints.timeAvailability > 2) {
        keyFactors.push('Sufficient time availability');
      } else {
        risks.push('Limited mentor time availability');
      }
    }

    return { score, rationale, keyFactors, risks };
  }

  private identifyRoles(
    agent1: UserRepresentativeAgent,
    agent2: UserRepresentativeAgent
  ): { mentor?: UserRepresentativeAgent; mentee?: UserRepresentativeAgent } {
    // Mentor typically offers guidance/mentorship
    if (agent1.userProfile.offerings.some(o =>
      o.category === OfferingCategory.GUIDANCE ||
      o.description.toLowerCase().includes('mentor')
    )) {
      return { mentor: agent1, mentee: agent2 };
    } else if (agent2.userProfile.offerings.some(o =>
      o.category === OfferingCategory.GUIDANCE ||
      o.description.toLowerCase().includes('mentor')
    )) {
      return { mentor: agent2, mentee: agent1 };
    }

    // Otherwise use career stage
    const stage1 = agent1.userAnalysis.profileAnalysis.careerStage;
    const stage2 = agent2.userAnalysis.profileAnalysis.careerStage;

    if (stage1 === 'executive' && stage2 !== 'executive') {
      return { mentor: agent1, mentee: agent2 };
    } else if (stage2 === 'executive' && stage1 !== 'executive') {
      return { mentor: agent2, mentee: agent1 };
    }

    return {};
  }

  private calculateExperienceGap(
    mentor: UserRepresentativeAgent,
    mentee: UserRepresentativeAgent
  ): number {
    const stages: Record<string, number> = {
      'executive': 4,
      'senior': 3,
      'mid-level': 2,
      'junior': 1
    };

    const mentorStage = stages[mentor.userAnalysis.profileAnalysis.careerStage] || 2;
    const menteeStage = stages[mentee.userAnalysis.profileAnalysis.careerStage] || 2;

    const gap = mentorStage - menteeStage;

    // Ideal gap is 1-2 levels
    if (gap >= 1 && gap <= 2) return 1.0;
    if (gap >= 3) return 0.7;
    return 0.4;
  }

  private calculateExpertiseMatch(
    mentor: UserRepresentativeAgent,
    mentee: UserRepresentativeAgent
  ): number {
    const mentorExpertise = mentor.userAnalysis.profileAnalysis.expertiseAreas;
    const menteeNeeds = mentee.userProfile.needs.map(n => n.description.toLowerCase());

    let matches = 0;
    for (const expertise of mentorExpertise) {
      if (menteeNeeds.some(need => need.includes(expertise.toLowerCase()))) {
        matches++;
      }
    }

    return mentorExpertise.length > 0 ? matches / mentorExpertise.length : 0;
  }

  private calculateLearningFit(
    mentor: UserRepresentativeAgent,
    mentee: UserRepresentativeAgent
  ): number {
    // Check personality compatibility
    const mentorStyle = mentor.userAnalysis.personalityProfile.communicationStyle;
    const menteeStyle = mentee.userAnalysis.personalityProfile.communicationStyle;

    // Collaborative styles work well together
    if (mentorStyle === 'collaborative' || menteeStyle === 'collaborative') return 0.9;

    return 0.7;
  }

  private calculateAvailability(mentor: UserRepresentativeAgent): number {
    const timeAvailable = mentor.userProfile.constraints.timeAvailability || 0;

    if (timeAvailable >= 5) return 1.0;
    if (timeAvailable >= 2) return 0.8;
    if (timeAvailable >= 1) return 0.5;
    return 0.3;
  }
}

/**
 * Domain Matcher Factory
 * Creates appropriate matcher for a given domain
 */
export class DomainMatcherFactory {
  static createMatcher(domain: MatchingDomain): BaseDomainMatcher {
    switch (domain) {
      case MatchingDomain.INVESTOR_STARTUP:
        return new InvestorStartupMatcher();
      case MatchingDomain.SALES_CLIENT:
        return new SalesClientMatcher();
      case MatchingDomain.PARTNERSHIP:
        return new PartnershipMatcher();
      case MatchingDomain.MENTOR_MENTEE:
        return new MentorMenteeMatcher();
      default:
        throw new Error(`Unknown matching domain: ${domain}`);
    }
  }

  static getAllMatchers(): BaseDomainMatcher[] {
    return [
      new InvestorStartupMatcher(),
      new SalesClientMatcher(),
      new PartnershipMatcher(),
      new MentorMenteeMatcher()
    ];
  }
}
