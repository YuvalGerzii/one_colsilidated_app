/**
 * Jeff Bezos Behavior Analysis Agent
 *
 * Analyzes decisions through the lens of Jeff Bezos' leadership style,
 * thinking patterns, and strategic approaches.
 *
 * Based on research of his leadership at Amazon and Blue Origin.
 */

import { Pool } from 'pg';
import Redis from 'ioredis';
import {
  IBehaviorAgent,
  LeaderBehaviorProfile,
  BusinessAdvice,
  DecisionContext,
  BusinessSector,
  LeadershipStyle,
  BehavioralTraits,
} from './BehaviorAgentTypes';

export class JeffBezosBehaviorAgent implements IBehaviorAgent {
  public readonly profile: LeaderBehaviorProfile;

  constructor(
    private pool: Pool,
    private redis: Redis
  ) {
    this.profile = this.buildProfile();
  }

  private buildProfile(): LeaderBehaviorProfile {
    return {
      name: 'Jeff Bezos',
      title: 'Founder and Executive Chairman of Amazon',
      companies: ['Amazon', 'Blue Origin', 'The Washington Post'],
      sectors: [
        BusinessSector.E_COMMERCE,
        BusinessSector.TECHNOLOGY,
        BusinessSector.AEROSPACE,
        BusinessSector.RETAIL,
      ],
      yearsOfExperience: 30,

      leadershipStyles: [
        LeadershipStyle.TRANSFORMATIONAL,
        LeadershipStyle.VISIONARY,
        LeadershipStyle.AUTOCRATIC,
      ],

      behavioralTraits: {
        riskTolerance: 0.9,
        innovationDrive: 0.95,
        analyticalThinking: 0.95,
        intuitionReliance: 0.7,
        speedOfDecision: 0.8,
        detailOrientation: 0.9,
        peopleOrientation: 0.5,
        dataOrientation: 0.95,
        longTermFocus: 0.95,
        adaptability: 0.85,
      },

      decisionPatterns: [
        {
          name: 'Customer Obsession',
          description: 'Start with customer and work backwards, obsess over customer experience',
          context: [
            DecisionContext.STRATEGIC_PLANNING,
            DecisionContext.PRODUCT_DEVELOPMENT,
            DecisionContext.OPERATIONS,
          ],
          approach: 'Begin with customer needs, work backward to solution',
          keyQuestions: [
            'What does the customer need?',
            'How does this improve customer experience?',
            'Are we truly customer-centric?',
            'What would delight the customer?',
          ],
          considerations: [
            'Customer pain points',
            'Long-term customer value',
            'Customer experience metrics',
            'Customer feedback loops',
          ],
          redFlags: [
            'Competitor-focused decisions',
            'Technology-first approach',
            'Ignoring customer feedback',
            'Short-term profit over customer value',
          ],
          successIndicators: [
            'Improved customer satisfaction',
            'Increased customer lifetime value',
            'Customer obsession demonstrated',
            'Long-term loyalty',
          ],
          examples: [
            'Free shipping through Prime',
            'One-click ordering',
            'Customer reviews',
            'Easy returns',
          ],
        },
        {
          name: 'Long-Term Thinking',
          description: 'Think in decades, not quarters; invest for long-term dominance',
          context: [
            DecisionContext.STRATEGIC_PLANNING,
            DecisionContext.INVESTMENT,
            DecisionContext.INNOVATION,
          ],
          approach: 'Make decisions with 5-10 year horizon, sacrifice short-term for long-term',
          keyQuestions: [
            'What matters in 5-10 years?',
            'Are we building for the future?',
            'What compounds over time?',
            'What creates long-term moats?',
          ],
          considerations: [
            'Long-term competitive advantages',
            'Compound effects',
            'Market position in 10 years',
            'Infrastructure investments',
          ],
          redFlags: [
            'Quarterly earnings focus',
            'Short-term profit maximization',
            'Missing long-term trends',
            'Under-investing in future',
          ],
          successIndicators: [
            'Market leadership',
            'Sustainable advantages',
            'Long-term growth',
            'Infrastructure moats',
          ],
          examples: [
            'AWS - invested heavily before profitable',
            'Fulfillment centers - massive capital before payoff',
            'Prime - long-term loyalty play',
          ],
        },
        {
          name: 'Embrace Failure and Experimentation',
          description: 'Experiment constantly, accept failure as essential for innovation',
          context: [
            DecisionContext.INNOVATION,
            DecisionContext.PRODUCT_DEVELOPMENT,
            DecisionContext.STRATEGIC_PLANNING,
          ],
          approach: 'Run many experiments, fail fast, scale winners, learn from failures',
          keyQuestions: [
            'What can we test?',
            'What did we learn from failure?',
            'Are we experimenting enough?',
            'What\'s the potential upside?',
          ],
          considerations: [
            'Experiment design',
            'Failure tolerance',
            'Learning capture',
            'Scaling criteria',
          ],
          redFlags: [
            'Fear of failure',
            'Not experimenting',
            'Punishing failures',
            'Risk aversion',
          ],
          successIndicators: [
            'High experiment velocity',
            'Learning from failures',
            'Occasional big wins',
            'Innovation culture',
          ],
          examples: [
            'Fire Phone - failed but learned',
            'AWS - experiment that became huge',
            'Marketplace - third-party sellers',
          ],
        },
        {
          name: 'High Standards and Operational Excellence',
          description: 'Maintain impossibly high standards, operational rigor, data-driven',
          context: [
            DecisionContext.OPERATIONS,
            DecisionContext.HIRING,
            DecisionContext.PRODUCT_DEVELOPMENT,
          ],
          approach: 'Set high bars, measure everything, continuous improvement, no compromises',
          keyQuestions: [
            'Are our standards high enough?',
            'What does world-class look like?',
            'What are we measuring?',
            'How do we improve?',
          ],
          considerations: [
            'Quality standards',
            'Operational metrics',
            'Efficiency opportunities',
            'Excellence benchmarks',
          ],
          redFlags: [
            'Lowering standards',
            'Accepting mediocrity',
            'Not measuring',
            'Complacency',
          ],
          successIndicators: [
            'World-class operations',
            'Continuous improvement',
            'High quality',
            'Efficient execution',
          ],
          examples: [
            'Two-day Prime shipping',
            'Fulfillment center automation',
            'Hiring bar raisers',
          ],
        },
      ],

      negotiationTactics: [
        {
          name: 'Long-Term Value Focus',
          description: 'Negotiate for long-term value, not short-term wins',
          whenToUse: 'Strategic partnerships and supplier relationships',
          howToApply: 'Emphasize long-term partnership, scale benefits, win-win',
          risks: ['Short-term costs', 'Requires patience', 'Trust needed'],
          effectiveness: 0.85,
          examples: [
            'Supplier relationships - volume commitments',
            'Partner ecosystems',
          ],
        },
        {
          name: 'Data-Driven Negotiation',
          description: 'Use comprehensive data and analysis in all negotiations',
          whenToUse: 'Any negotiation context',
          howToApply: 'Present detailed metrics, cost structures, market data',
          risks: ['Data overload', 'Analysis paralysis'],
          effectiveness: 0.9,
          examples: [
            'Pricing negotiations with data',
            'Investment decisions backed by metrics',
          ],
        },
        {
          name: 'High Standards Requirement',
          description: 'Require partners and suppliers to meet Amazon-level standards',
          whenToUse: 'Vendor selection and partnerships',
          howToApply: 'Clear standards, rigorous evaluation, no compromises',
          risks: ['Limited partner pool', 'Relationship strain'],
          effectiveness: 0.8,
          examples: [
            'Vendor performance requirements',
            'Quality standards enforcement',
          ],
        },
      ],

      strategicFrameworks: [
        {
          name: 'Day 1 Mentality',
          description: 'Always operate like a startup - maintain urgency and customer focus',
          principles: [
            'Customer obsession',
            'Resist proxies (process over outcomes)',
            'Embrace external trends',
            'High-velocity decision making',
          ],
          applicationSteps: [
            'Stay focused on customers, not competitors',
            'Avoid process bureaucracy',
            'Adopt new technologies and trends quickly',
            'Make reversible decisions quickly (Type 2)',
            'Make irreversible decisions carefully (Type 1)',
          ],
          keyMetrics: [
            'Customer satisfaction',
            'Decision velocity',
            'Innovation rate',
            'Bureaucracy metrics',
          ],
          timeHorizon: 'long',
          successCriteria: [
            'Maintained startup mentality',
            'Customer-centric culture',
            'Fast decision making',
            'Continuous innovation',
          ],
        },
        {
          name: 'Flywheel Effect',
          description: 'Build virtuous cycles where success compounds',
          principles: [
            'Lower costs enable lower prices',
            'Lower prices drive more customers',
            'More customers attract sellers',
            'More sellers improve selection',
            'Better selection drives more customers',
          ],
          applicationSteps: [
            'Identify key elements of flywheel',
            'Invest to spin flywheel faster',
            'Measure flywheel metrics',
            'Optimize each component',
            'Let momentum compound',
          ],
          keyMetrics: [
            'Customer growth',
            'Seller growth',
            'Selection expansion',
            'Cost reduction',
          ],
          timeHorizon: 'long',
          successCriteria: [
            'Self-reinforcing growth',
            'Market leadership',
            'Sustainable advantages',
          ],
        },
      ],

      innovationApproaches: [
        {
          methodology: 'Working Backwards',
          description: 'Start with customer press release, work backward to product',
          keyPrinciples: [
            'Customer-centric from start',
            'Define customer benefit first',
            'Work backward to solution',
            'Write press release before building',
          ],
          ideationProcess: [
            'Write customer-facing press release',
            'Define customer problem and solution',
            'Write FAQ anticipating questions',
            'Work backward to technical requirements',
            'Build and iterate',
          ],
          evaluationCriteria: [
            'Does customer benefit jump out?',
            'Is the problem important?',
            'Is the solution compelling?',
            'Can we build this?',
          ],
          implementationStrategy: [
            'Get approval on press release first',
            'Build minimum viable product',
            'Test with customers',
            'Iterate based on feedback',
            'Scale if successful',
          ],
          examples: [
            'Kindle - started with press release',
            'AWS - customer needs first',
            'Prime - customer value proposition',
          ],
        },
      ],

      leadershipPrinciples: [
        {
          principle: 'Customer Obsession',
          description: 'Leaders start with the customer and work backwards',
          application: 'Every decision begins with customer impact analysis',
          examples: [
            'Free returns',
            'Prime shipping',
            'Customer reviews',
          ],
          quotes: [
            'The most important single thing is to focus obsessively on the customer',
          ],
        },
        {
          principle: 'Invent and Simplify',
          description: 'Leaders expect and require innovation from their teams',
          application: 'Constantly seeking new ways to simplify and innovate',
          examples: [
            'One-click ordering',
            'AWS services',
            'Alexa',
          ],
        },
        {
          principle: 'Bias for Action',
          description: 'Speed matters in business. Many decisions are reversible.',
          application: 'Make reversible decisions quickly, irreversible ones carefully',
          examples: [
            'Type 1 vs Type 2 decisions',
            'Experiment velocity',
          ],
        },
        {
          principle: 'Frugality',
          description: 'Accomplish more with less. Constraints breed resourcefulness.',
          application: 'Avoid wasteful spending, maximize customer value',
          examples: [
            'Door desk tradition',
            'Lean operations',
          ],
        },
      ],

      communicationStyle: {
        directness: 0.85,
        formality: 0.6,
        emotionalExpression: 0.4,
        typicalPhrases: [
          'Working backwards from the customer',
          'Day 1',
          'High standards',
          'Think long-term',
          'Be stubborn on vision, flexible on details',
          'It\'s always Day 1',
        ],
        communicationChannels: ['Six-page memos', 'Annual shareholder letters', 'All-hands', 'Written narratives'],
      },

      workStandards: {
        expectationsOfTeam: [
          'Customer obsession',
          'Ownership mentality',
          'High standards',
          'Think big',
          'Bias for action',
          'Dive deep into details',
          'Deliver results',
        ],
        workEthic: 'High standards, long-term focus, data-driven, customer-centric',
        meetingCulture: 'Six-page memos, silent reading, data-driven discussions',
        decisionMakingSpeed: 'Fast on reversible decisions, careful on irreversible',
        failureTolerance: 0.8,
      },

      famousQuotes: [
        'Your margin is my opportunity',
        'We\'re willing to be misunderstood for long periods of time',
        'If you double the number of experiments you do per year, you\'re going to double your inventiveness',
        'It\'s always Day 1',
        'The most important single thing is to focus obsessively on the customer',
        'We see our customers as invited guests to a party, and we are the hosts',
        'Life\'s too short to hang out with people who aren\'t resourceful',
      ],

      mantras: [
        'Customer obsession',
        'Day 1',
        'Think long-term',
        'Invent and simplify',
        'High standards',
        'Bias for action',
      ],

      notableDecisions: [
        {
          decision: 'Built AWS and offered infrastructure as a service',
          context: 'Amazon had built internal infrastructure, saw opportunity to offer externally',
          outcome: 'AWS became $80B+ business, cloud computing leader',
          lessonLearned: 'Internal capabilities can become external businesses',
        },
        {
          decision: 'Created Amazon Prime with free two-day shipping',
          context: 'High upfront cost, uncertain payoff, but customer value clear',
          outcome: 'Over 200M members, loyalty engine, massive value creation',
          lessonLearned: 'Invest in long-term customer loyalty even with short-term costs',
        },
        {
          decision: 'Opened platform to third-party sellers',
          context: 'Risk of competition on own platform',
          outcome: 'Marketplace became majority of sales, flywheel accelerated',
          lessonLearned: 'Sometimes helping competitors helps you more',
        },
        {
          decision: 'Invested billions in fulfillment centers before profitability',
          context: 'Wall Street pressured for profits',
          outcome: 'Created sustainable competitive advantage',
          lessonLearned: 'Think in decades, not quarters',
        },
      ],
    };
  }

  async getAdvice(
    question: string,
    context: DecisionContext,
    additionalInfo?: Record<string, any>
  ): Promise<BusinessAdvice> {
    const cacheKey = `bezos:advice:${this.hashString(question)}:${context}`;
    const cached = await this.redis.get(cacheKey);
    if (cached) return JSON.parse(cached);

    const relevantPatterns = this.profile.decisionPatterns.filter(p =>
      p.context.includes(context)
    );

    const advice = this.generateAdviceByContext(question, context, additionalInfo);
    const reasoning = this.generateReasoning(context, relevantPatterns);
    const actionableSteps = this.generateActionableSteps(context);
    const potentialRisks = this.generateRisks(context);

    const result: BusinessAdvice = {
      question,
      context,
      leaderName: this.profile.name,
      advice,
      reasoning,
      alternativeApproaches: this.generateAlternatives(context),
      potentialRisks,
      successProbability: this.estimateSuccessProbability(context, additionalInfo),
      keyQuotes: this.selectRelevantQuotes(context),
      historicalExamples: this.selectRelevantExamples(context),
      actionableSteps,
      timeframe: this.estimateTimeframe(context),
      resourcesNeeded: this.identifyResources(context),
      kpis: this.defineKPIs(context),
    };

    await this.redis.set(cacheKey, JSON.stringify(result), 'EX', 3600);
    return result;
  }

  async analyzeDecision(
    decision: string,
    context: DecisionContext,
    outcomes?: string[]
  ): Promise<{
    wouldSupport: boolean;
    reasoning: string;
    modifications: string[];
    confidence: number;
  }> {
    const characteristics = this.analyzeDecisionCharacteristics(decision);

    const wouldSupport =
      characteristics.isCustomerFocused &&
      characteristics.isLongTerm &&
      characteristics.isDataDriven &&
      characteristics.hasHighStandards;

    const modifications: string[] = [];
    if (!characteristics.isCustomerFocused) {
      modifications.push('Start with the customer - work backwards from customer needs');
    }
    if (!characteristics.isLongTerm) {
      modifications.push('Extend time horizon - think in years, not quarters');
    }
    if (!characteristics.isDataDriven) {
      modifications.push('Add rigorous data analysis and metrics');
    }
    if (!characteristics.hasHighStandards) {
      modifications.push('Raise the bar - what does world-class look like?');
    }

    return {
      wouldSupport,
      reasoning: `Bezos ${wouldSupport ? 'would support' : 'would not support'} this decision because ${
        wouldSupport
          ? 'it demonstrates customer obsession, long-term thinking, and high standards'
          : 'it lacks the customer focus, long-term perspective, and rigor Amazon requires'
      }`,
      modifications,
      confidence: wouldSupport ? 0.85 : 0.75,
    };
  }

  async getStrategicGuidance(
    situation: string,
    goals: string[],
    constraints: string[]
  ): Promise<{
    strategy: string;
    rationale: string;
    steps: string[];
    timeline: string;
    risks: string[];
  }> {
    return {
      strategy: `Start with the customer and work backwards. Think long-term - what matters in 5-10 years? Maintain Day 1 mentality. Build flywheels. Experiment constantly. Hold impossibly high standards. Be data-driven and customer-obsessed.`,
      rationale: `Customer obsession and long-term thinking create sustainable advantages. High standards and experimentation drive innovation. Flywheels create compounding returns. Day 1 mentality prevents complacency.`,
      steps: [
        'Define ideal customer outcome - write press release',
        'Work backwards to solution',
        'Set high standards for execution',
        'Build measurements and metrics',
        'Experiment and iterate rapidly',
        'Think about flywheel effects',
        'Invest for long-term even if short-term pain',
      ],
      timeline: 'Think in years and decades, execute with urgency',
      risks: [
        'Short-term profitability pressure',
        'High standards may slow execution',
        'Experiments may fail',
        'Long-term bets may not pay off',
        'Customer obsession may increase costs',
      ],
    };
  }

  async evaluateOpportunity(
    opportunity: string,
    context: Record<string, any>
  ): Promise<{
    recommendation: 'pursue' | 'pass' | 'modify';
    score: number;
    reasoning: string;
    conditions?: string[];
    modifications?: string[];
  }> {
    const score = this.scoreOpportunity(opportunity, context);

    if (score >= 0.75) {
      return {
        recommendation: 'pursue',
        score,
        reasoning: 'This opportunity aligns with customer obsession and long-term value creation',
        conditions: [
          'Start with customer needs',
          'Think 5-10 years out',
          'Set high standards',
          'Measure rigorously',
          'Be willing to experiment and fail',
        ],
      };
    } else if (score >= 0.5) {
      return {
        recommendation: 'modify',
        score,
        reasoning: 'Opportunity has potential but needs refinement',
        modifications: [
          'Strengthen customer value proposition',
          'Extend time horizon',
          'Raise quality standards',
          'Add more experimentation',
          'Consider flywheel effects',
        ],
      };
    } else {
      return {
        recommendation: 'pass',
        score,
        reasoning: 'This doesn\'t align with customer obsession and long-term thinking',
      };
    }
  }

  // Private helper methods

  private generateAdviceByContext(
    question: string,
    context: DecisionContext,
    additionalInfo?: Record<string, any>
  ): string {
    const baseAdvice: Record<DecisionContext, string> = {
      [DecisionContext.STRATEGIC_PLANNING]:
        'Start with the customer. Think 5-10 years out, not quarters. Build flywheels where success compounds. It\'s always Day 1 - maintain startup urgency. Be willing to be misunderstood for long periods.',

      [DecisionContext.PRODUCT_DEVELOPMENT]:
        'Work backwards from the customer. Write the press release first. What would delight customers? Set impossibly high standards. Measure everything. Experiment constantly. Bias for action on reversible decisions.',

      [DecisionContext.INNOVATION]:
        'Experiment at high velocity. Accept that most will fail. Learn from failures. Scale the winners. Look for 10x opportunities. Customer needs guide innovation, not technology.',

      [DecisionContext.NEGOTIATION]:
        'Think long-term partnership, not transaction. Use data extensively. Maintain high standards. Focus on customer value creation. Be willing to walk away if standards not met.',

      [DecisionContext.CRISIS_MANAGEMENT]:
        'Maintain Day 1 mentality. Focus on customers first. Use data to understand the problem. Make reversible decisions quickly. Hold high standards even under pressure.',

      [DecisionContext.INVESTMENT]:
        'Does this benefit customers long-term? Can we build a moat? What\'s the 10-year view? Are we willing to be misunderstood? Can we experiment to validate?',

      [DecisionContext.HIRING]:
        'Raise the bar with every hire. Look for customer obsession, ownership, high standards, think big mentality. Would you admire this person? Will they raise the team\'s effectiveness?',

      [DecisionContext.MARKET_EXPANSION]:
        'What do customers need? Can we be customer-obsessed there? Can we build long-term advantages? What\'s the flywheel? Are we thinking big enough?',

      [DecisionContext.PARTNERSHIP]:
        'Does this serve customers better? Long-term strategic fit? Do they meet our standards? Can we measure the value? Is this reversible?',

      [DecisionContext.PRICING]:
        'Your margin is my opportunity. Focus on customer value. Lower prices drive flywheel. Long-term volume over short-term margin. Be customer-centric.',

      [DecisionContext.MARKETING]:
        'Let customers be the marketing through great experiences. Word of mouth is powerful. Focus resources on improving customer experience over advertising.',

      [DecisionContext.OPERATIONS]:
        'Impossibly high standards. Measure everything. Continuous improvement. Operational excellence enables customer obsession. Frugality breeds resourcefulness.',
    };

    return baseAdvice[context] || baseAdvice[DecisionContext.STRATEGIC_PLANNING];
  }

  private generateReasoning(context: DecisionContext, patterns: any[]): string {
    return `Based on customer obsession and long-term thinking that built Amazon. Drawing from ${patterns.length} key patterns around customer focus, experimentation, and operational excellence.`;
  }

  private generateActionableSteps(context: DecisionContext): string[] {
    return [
      'Define customer outcome - write press release',
      'Work backwards to solution',
      'Set high standards and metrics',
      'Design experiments to test',
      'Measure results rigorously',
      'Iterate based on data',
      'Scale what works',
    ];
  }

  private generateRisks(context: DecisionContext): string[] {
    return [
      'Short-term profitability pressure',
      'Experiments may fail',
      'High standards may slow execution',
      'Long-term bets uncertain',
      'Customer obsession may increase costs',
    ];
  }

  private generateAlternatives(context: DecisionContext): string[] {
    return [
      'Competitor-focused strategy (not recommended)',
      'Short-term profit focus (misses big opportunities)',
      'Lower standards for speed (compromises long-term)',
    ];
  }

  private estimateSuccessProbability(
    context: DecisionContext,
    additionalInfo?: Record<string, any>
  ): number {
    return 0.8;
  }

  private selectRelevantQuotes(context: DecisionContext): string[] {
    const contextQuotes: Record<string, string[]> = {
      customer: ['The most important single thing is to focus obsessively on the customer'],
      innovation: ['If you double the experiments, you double inventiveness'],
      longterm: ['We\'re willing to be misunderstood for long periods of time'],
    };

    return contextQuotes.customer || this.profile.famousQuotes.slice(0, 2);
  }

  private selectRelevantExamples(context: DecisionContext): string[] {
    return this.profile.notableDecisions.slice(0, 2).map(d => `${d.decision}: ${d.outcome}`);
  }

  private estimateTimeframe(context: DecisionContext): string {
    return 'Think in years and decades, execute with Day 1 urgency';
  }

  private identifyResources(context: DecisionContext): string[] {
    return [
      'Customer insights and data',
      'High-caliber talent',
      'Experimentation infrastructure',
      'Measurement systems',
      'Long-term capital',
    ];
  }

  private defineKPIs(context: DecisionContext): string[] {
    return [
      'Customer satisfaction metrics',
      'Long-term customer value',
      'Experiment velocity',
      'Innovation rate',
      'Operational excellence metrics',
      'Flywheel acceleration',
    ];
  }

  private analyzeDecisionCharacteristics(decision: string): {
    isCustomerFocused: boolean;
    isLongTerm: boolean;
    isDataDriven: boolean;
    hasHighStandards: boolean;
  } {
    const lower = decision.toLowerCase();
    return {
      isCustomerFocused: /customer|user|client|experience/.test(lower),
      isLongTerm: /long-term|years|decade|sustainable|future/.test(lower),
      isDataDriven: /data|measure|metric|analytics|test/.test(lower),
      hasHighStandards: /excellence|quality|high standard|world-class/.test(lower),
    };
  }

  private scoreOpportunity(opportunity: string, context: Record<string, any>): number {
    let score = 0.5;
    const lower = opportunity.toLowerCase();

    if (/customer|user|experience/.test(lower)) score += 0.25;
    if (/long-term|sustainable|future/.test(lower)) score += 0.2;
    if (/data|measure|experiment/.test(lower)) score += 0.1;
    if (/innovation|invent/.test(lower)) score += 0.1;
    if (/flywheel|compound/.test(lower)) score += 0.1;

    return Math.min(1, score);
  }

  private hashString(str: string): string {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = (hash << 5) - hash + char;
      hash = hash & hash;
    }
    return hash.toString(36);
  }
}
