/**
 * Mark Zuckerberg Behavior Analysis Agent
 *
 * Analyzes decisions through the lens of Mark Zuckerberg's leadership style,
 * thinking patterns, and strategic approaches.
 *
 * Based on research of his leadership at Facebook/Meta.
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

export class MarkZuckerbergBehaviorAgent implements IBehaviorAgent {
  public readonly profile: LeaderBehaviorProfile;

  constructor(
    private pool: Pool,
    private redis: Redis
  ) {
    this.profile = this.buildProfile();
  }

  private buildProfile(): LeaderBehaviorProfile {
    return {
      name: 'Mark Zuckerberg',
      title: 'CEO and Co-founder of Meta (Facebook)',
      companies: ['Meta', 'Facebook', 'Instagram', 'WhatsApp'],
      sectors: [
        BusinessSector.SOCIAL_MEDIA,
        BusinessSector.TECHNOLOGY,
        BusinessSector.GENERAL,
      ],
      yearsOfExperience: 20,

      leadershipStyles: [
        LeadershipStyle.VISIONARY,
        LeadershipStyle.DEMOCRATIC,
        LeadershipStyle.TRANSFORMATIONAL,
      ],

      behavioralTraits: {
        riskTolerance: 0.85,
        innovationDrive: 0.9,
        analyticalThinking: 0.9,
        intuitionReliance: 0.6,
        speedOfDecision: 0.95,
        detailOrientation: 0.75,
        peopleOrientation: 0.6,
        dataOrientation: 0.95,
        longTermFocus: 0.95,
        adaptability: 0.85,
      },

      decisionPatterns: [
        {
          name: 'Data-Driven Decision Making',
          description: 'Let data and metrics guide all decisions, A/B test everything',
          context: [
            DecisionContext.PRODUCT_DEVELOPMENT,
            DecisionContext.STRATEGIC_PLANNING,
            DecisionContext.MARKETING,
          ],
          approach: 'Measure, test, analyze, iterate based on data',
          keyQuestions: [
            'What does the data say?',
            'How can we test this?',
            'What are the metrics?',
            'What does user behavior show?',
          ],
          considerations: [
            'User engagement metrics',
            'A/B test results',
            'Growth analytics',
            'Behavioral data',
          ],
          redFlags: [
            'Decisions based on gut feeling alone',
            'Not measuring outcomes',
            'Ignoring user data',
            'No experimentation framework',
          ],
          successIndicators: [
            'Measurable improvements',
            'Data-validated hypotheses',
            'Optimized user engagement',
          ],
          examples: [
            'News Feed algorithm - constantly A/B tested',
            'Feature rollouts - data-driven decisions',
            'Product changes - measured impact on engagement',
          ],
        },
        {
          name: 'Move Fast and Break Things',
          description: 'Prioritize speed and iteration over perfection',
          context: [
            DecisionContext.PRODUCT_DEVELOPMENT,
            DecisionContext.INNOVATION,
            DecisionContext.OPERATIONS,
          ],
          approach: 'Ship quickly, learn from mistakes, iterate rapidly',
          keyQuestions: [
            'Can we ship this faster?',
            'What\'s the minimum we need to test?',
            'How quickly can we iterate?',
            'Are we moving fast enough?',
          ],
          considerations: [
            'Speed to market',
            'Learning velocity',
            'Iteration cycles',
            'Acceptable failure modes',
          ],
          redFlags: [
            'Over-planning before action',
            'Waiting for perfection',
            'Slow iteration cycles',
            'Risk paralysis',
          ],
          successIndicators: [
            'Rapid feature deployment',
            'Quick learning cycles',
            'Fast pivots when needed',
          ],
          examples: [
            'Facebook platform launched quickly, refined over time',
            'Mobile transition - fast iteration',
            'Acquired Instagram and WhatsApp, integrated quickly',
          ],
        },
        {
          name: 'Long-Term Futuristic Bets',
          description: 'Make bold bets on future technology trends, even if years away',
          context: [
            DecisionContext.STRATEGIC_PLANNING,
            DecisionContext.INVESTMENT,
            DecisionContext.INNOVATION,
          ],
          approach: 'Identify long-term trends, invest heavily even if unprofitable initially',
          keyQuestions: [
            'Where is the world going?',
            'What will matter in 10 years?',
            'Are we building for the future?',
            'What\'s the next platform?',
          ],
          considerations: [
            'Long-term technology trends',
            'Platform shifts',
            'Future user behaviors',
            'Strategic positioning',
          ],
          redFlags: [
            'Only focusing on current revenue',
            'Ignoring emerging platforms',
            'Short-term thinking',
            'Missing paradigm shifts',
          ],
          successIndicators: [
            'Early position in new platforms',
            'Long-term strategic advantage',
            'Future-proof positioning',
          ],
          examples: [
            'Metaverse investment - $10B+ annually despite losses',
            'VR/AR bet with Oculus acquisition',
            'AI infrastructure massive investment',
          ],
        },
        {
          name: 'Reflexive Product Iteration',
          description: 'Continuous cycle of hypothesize, prototype, measure, adapt',
          context: [
            DecisionContext.PRODUCT_DEVELOPMENT,
            DecisionContext.INNOVATION,
            DecisionContext.OPERATIONS,
          ],
          approach: 'Build-measure-learn loops at high velocity',
          keyQuestions: [
            'What\'s our hypothesis?',
            'How do we test it?',
            'What did we learn?',
            'How do we adapt?',
          ],
          considerations: [
            'Hypothesis clarity',
            'Measurement framework',
            'Learning capture',
            'Adaptation speed',
          ],
          redFlags: [
            'Building without hypothesis',
            'Not measuring results',
            'Slow adaptation',
            'Ignoring feedback',
          ],
          successIndicators: [
            'Rapid iteration',
            'Data-informed changes',
            'Continuous improvement',
          ],
          examples: [
            'News Feed continuous evolution',
            'Ads platform optimization',
            'Mobile app improvements',
          ],
        },
      ],

      negotiationTactics: [
        {
          name: 'Aggressive Acquisition Strategy',
          description: 'Move quickly to acquire potential competitors or complementary products',
          whenToUse: 'When identifying threats or strategic opportunities',
          howToApply: 'Act fast, pay premium if necessary to secure strategic position',
          risks: ['Overpaying', 'Integration challenges', 'Regulatory scrutiny'],
          effectiveness: 0.85,
          examples: [
            'Instagram for $1B (seemed expensive, now seen as bargain)',
            'WhatsApp for $19B',
            'Oculus for $2B',
          ],
        },
        {
          name: 'Engineering-First Culture',
          description: 'Prioritize engineering and product over other functions',
          whenToUse: 'Building culture and making organizational decisions',
          howToApply: 'Give engineers autonomy, flat hierarchy, product-centric',
          risks: ['Neglecting other functions', 'Communication issues', 'Business gaps'],
          effectiveness: 0.8,
          examples: [
            'Hackathons as core culture',
            'Engineers ship directly to production',
            'Flat organizational structure',
          ],
        },
        {
          name: 'Radical Transparency with Data',
          description: 'Share metrics widely internally to drive aligned decisions',
          whenToUse: 'Building data-driven culture',
          howToApply: 'Make all metrics accessible, encourage data-driven debates',
          risks: ['Information overload', 'Misinterpretation', 'Leaks'],
          effectiveness: 0.75,
          examples: [
            'Internal dashboards for all',
            'Open access to metrics',
            'Data-driven debates encouraged',
          ],
        },
      ],

      strategicFrameworks: [
        {
          name: 'Speed is King',
          description: 'Execute faster than competitors, iterate to win',
          principles: [
            'Ship early and often',
            'Learn from real user data',
            'Iterate faster than competitors',
            'Speed compounds over time',
          ],
          applicationSteps: [
            'Define minimum viable test',
            'Ship to subset of users',
            'Measure results',
            'Iterate based on data',
            'Repeat cycle rapidly',
          ],
          keyMetrics: [
            'Time to ship',
            'Iteration velocity',
            'Learning rate',
            'Feature deployment frequency',
          ],
          timeHorizon: 'short',
          successCriteria: [
            'Faster than competitors',
            'Continuous learning',
            'Market leadership',
          ],
        },
        {
          name: 'Connect the World',
          description: 'Mission-driven focus on connecting everyone globally',
          principles: [
            'Growth at scale',
            'Global reach',
            'Network effects',
            'Accessibility for all',
          ],
          applicationSteps: [
            'Remove barriers to access',
            'Optimize for emerging markets',
            'Build network effects',
            'Scale infrastructure',
          ],
          keyMetrics: [
            'Daily active users',
            'Global penetration',
            'Engagement metrics',
            'Network density',
          ],
          timeHorizon: 'long',
          successCriteria: [
            'Billions of users',
            'Global presence',
            'Strong network effects',
          ],
        },
      ],

      innovationApproaches: [
        {
          methodology: 'Data-Driven Experimentation',
          description: 'Use A/B testing and data analysis to drive all innovation',
          keyPrinciples: [
            'Test everything',
            'Let data decide',
            'Measure impact rigorously',
            'Scale what works',
          ],
          ideationProcess: [
            'Generate hypotheses',
            'Design experiments',
            'Run A/B tests',
            'Analyze results',
            'Scale winners',
          ],
          evaluationCriteria: [
            'Statistically significant results?',
            'Positive impact on key metrics?',
            'Scalable?',
            'Aligned with mission?',
          ],
          implementationStrategy: [
            'Start with small user percentage',
            'Measure carefully',
            'Iterate based on data',
            'Roll out gradually',
            'Monitor at scale',
          ],
          examples: [
            'News Feed ranking algorithms',
            'Ad targeting optimization',
            'User interface improvements',
          ],
        },
      ],

      leadershipPrinciples: [
        {
          principle: 'Focus on Impact',
          description: 'Measure success by impact created, not hours worked',
          application: 'Set clear goals, measure outcomes, give autonomy',
          examples: [
            'No 1:1s with reports - focus on impact not process',
            'Outcome-oriented management',
          ],
          quotes: [
            'Move fast and break things',
            'Done is better than perfect',
          ],
        },
        {
          principle: 'Be Bold',
          description: 'Take risks, make big bets, don\'t play it safe',
          application: 'Invest heavily in future trends even if current losses',
          examples: [
            'Metaverse bet - billions in losses for future positioning',
            'Mobile pivot - bet the company',
          ],
        },
        {
          principle: 'Build Social Value',
          description: 'Mission is to connect world and build community',
          application: 'Make decisions that increase connectivity and community',
          examples: [
            'Free internet initiatives',
            'Safety features',
            'Community building tools',
          ],
        },
      ],

      communicationStyle: {
        directness: 0.7,
        formality: 0.3,
        emotionalExpression: 0.4,
        typicalPhrases: [
          'Move fast',
          'What does the data say?',
          'The journey is 1% finished',
          'Done is better than perfect',
          'Focus on impact',
          'Connect the world',
        ],
        communicationChannels: ['All-hands', 'Internal posts', 'Public posts', 'Product demos'],
      },

      workStandards: {
        expectationsOfTeam: [
          'Data-driven decisions',
          'Move fast and iterate',
          'Focus on impact',
          'Think long-term',
          'Be bold',
        ],
        workEthic: 'High output, focus on results over process',
        meetingCulture: 'Minimal - no 1:1s, focus on shipping',
        decisionMakingSpeed: 'Very fast - bias toward action',
        failureTolerance: 0.8,
      },

      famousQuotes: [
        'Move fast and break things',
        'Done is better than perfect',
        'Ideas don\'t come out fully formed. They only become clear as you work on them',
        'The biggest risk is not taking any risk',
        'The question isn\'t, "What do we want to know about people?" It\'s, "What do people want to tell about themselves?"',
        'I think a simple rule of business is, if you do the things that are easier first, then you can actually make a lot of progress',
      ],

      mantras: [
        'Move fast',
        'Be bold',
        'Focus on impact',
        'Connect the world',
        'Build for the long term',
        'Data over opinions',
      ],

      notableDecisions: [
        {
          decision: 'Acquired Instagram for $1 billion in 2012',
          context: 'Instagram was small but growing fast, seen as potential threat',
          outcome: 'Now worth $100B+, strategic acquisition that neutralized competitor',
          lessonLearned: 'Move fast on strategic acquisitions, don\'t hesitate on price',
        },
        {
          decision: 'Pivoted entire company to mobile in 2012',
          context: 'Facebook was desktop-first, mobile was threatening the business',
          outcome: 'Became mobile-first company, now majority of revenue from mobile',
          lessonLearned: 'Recognize platform shifts early and bet the company',
        },
        {
          decision: 'Rebranded to Meta and invested $10B+ annually in metaverse',
          context: 'Betting on next platform shift to VR/AR',
          outcome: 'TBD - long-term bet with current losses',
          lessonLearned: 'Make bold long-term bets even if near-term pain',
        },
        {
          decision: 'Massive AI infrastructure investment in 2024',
          context: 'AI becoming critical, needed massive compute',
          outcome: 'Building leading AI capabilities',
          lessonLearned: 'Invest aggressively in strategic technologies',
        },
      ],
    };
  }

  async getAdvice(
    question: string,
    context: DecisionContext,
    additionalInfo?: Record<string, any>
  ): Promise<BusinessAdvice> {
    const cacheKey = `zuckerberg:advice:${this.hashString(question)}:${context}`;
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
      characteristics.isDataDriven &&
      characteristics.isFast &&
      characteristics.isLongTerm &&
      !characteristics.isRiskAverse;

    const modifications: string[] = [];
    if (!characteristics.isDataDriven) {
      modifications.push('Add measurement framework and A/B testing');
    }
    if (!characteristics.isFast) {
      modifications.push('Accelerate - ship faster and iterate');
    }
    if (!characteristics.isLongTerm) {
      modifications.push('Think bigger - what does this enable in 10 years?');
    }
    if (characteristics.isRiskAverse) {
      modifications.push('Be bolder - the biggest risk is not taking any risk');
    }

    return {
      wouldSupport,
      reasoning: `Zuckerberg ${wouldSupport ? 'would support' : 'would not support'} this decision because ${
        wouldSupport
          ? 'it\'s data-driven, moves fast, and takes a long-term view'
          : 'it lacks the speed, data orientation, and boldness needed for impact'
      }`,
      modifications,
      confidence: wouldSupport ? 0.8 : 0.7,
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
      strategy: `Move fast with data-driven iteration. Ship quickly to learn from real users, measure everything, and iterate based on data. Make bold long-term bets while optimizing short-term execution.`,
      rationale: `Speed and data create competitive advantage. The faster you learn, the faster you win. Combine this with bold long-term vision to build sustainable leadership.`,
      steps: [
        'Define hypothesis and key metrics',
        'Build minimum viable test',
        'Ship to subset of users',
        'Measure and analyze data',
        'Iterate based on learnings',
        'Scale what works',
        'Make long-term strategic bets in parallel',
      ],
      timeline: 'Days to weeks for iteration cycles, years for strategic bets',
      risks: [
        'Moving too fast may create technical debt',
        'Data may not capture everything',
        'Long-term bets may not pay off',
        'Iteration may lack strategic direction',
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

    if (score >= 0.7) {
      return {
        recommendation: 'pursue',
        score,
        reasoning: 'This opportunity aligns with data-driven, fast-moving, long-term strategic thinking',
        conditions: [
          'Establish clear metrics and measurement',
          'Move fast with iteration cycles',
          'Consider long-term strategic implications',
          'Be bold in execution',
        ],
      };
    } else if (score >= 0.4) {
      return {
        recommendation: 'modify',
        score,
        reasoning: 'Opportunity has potential but needs refinement',
        modifications: [
          'Add data-driven framework',
          'Accelerate timeline',
          'Think bigger and longer-term',
          'Increase boldness of bet',
        ],
      };
    } else {
      return {
        recommendation: 'pass',
        score,
        reasoning: 'This opportunity doesn\'t align with high-impact, data-driven, long-term strategy',
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
        'Think long-term while moving fast short-term. What matters in 10 years? Make bold bets on the future. Identify platform shifts early. Be willing to invest heavily even if current losses.',

      [DecisionContext.PRODUCT_DEVELOPMENT]:
        'Ship fast, measure everything, iterate based on data. A/B test all changes. Done is better than perfect. Build-measure-learn cycles at high velocity. Let user data guide decisions.',

      [DecisionContext.INNOVATION]:
        'Move fast and break things. Test hypotheses quickly. Let data validate ideas. Be bold in trying new things. Learn from failures fast. Iterate toward success.',

      [DecisionContext.NEGOTIATION]:
        'Move quickly on strategic opportunities. Don\'t hesitate on price if strategically important. Think long-term value. Consider acquisition of threats early.',

      [DecisionContext.CRISIS_MANAGEMENT]:
        'Move fast, use data to understand the problem, iterate solutions quickly. Don\'t overthink - ship and learn. Adapt based on real-time data.',

      [DecisionContext.INVESTMENT]:
        'Make bold long-term bets. Don\'t worry about near-term profitability if strategic. Invest heavily in future platforms. Think 10 years out.',

      [DecisionContext.HIRING]:
        'Hire engineers and builders. Look for impact over credentials. Culture fit with move-fast mentality. Can they thrive with autonomy?',

      [DecisionContext.MARKET_EXPANSION]:
        'Expand fast, measure results, optimize based on data. Think global from day one. Build network effects. Focus on user growth.',

      [DecisionContext.PARTNERSHIP]:
        'Prefer acquisition to partnership if strategic. Partner where it accelerates learning or reach. Maintain control of core platform.',

      [DecisionContext.PRICING]:
        'Optimize based on data and A/B testing. Consider long-term user acquisition over short-term revenue. Build network effects first.',

      [DecisionContext.MARKETING]:
        'Let product speak for itself. Growth through virality and network effects. Measure and optimize all channels. Data-driven allocation.',

      [DecisionContext.OPERATIONS]:
        'Flat hierarchy, engineering-first. Minimize process. Fast decisions. No 1:1s - focus on impact. Data transparency.',
    };

    return baseAdvice[context] || baseAdvice[DecisionContext.STRATEGIC_PLANNING];
  }

  private generateReasoning(context: DecisionContext, patterns: any[]): string {
    return `Based on data-driven, fast-moving principles that built Facebook/Meta. Drawing from ${patterns.length} key decision patterns around speed, experimentation, and long-term thinking.`;
  }

  private generateActionableSteps(context: DecisionContext): string[] {
    return [
      'Define clear hypothesis and metrics',
      'Build minimum test quickly',
      'Ship to users and gather data',
      'Analyze results rigorously',
      'Iterate based on learnings',
      'Scale what works',
      'Think about long-term implications',
    ];
  }

  private generateRisks(context: DecisionContext): string[] {
    return [
      'Moving too fast may create issues',
      'Over-reliance on data may miss context',
      'Long-term bets may not pay off',
      'Rapid iteration may cause instability',
      'Bold bets require significant capital',
    ];
  }

  private generateAlternatives(context: DecisionContext): string[] {
    return [
      'Move slower with more planning (not recommended)',
      'Rely on intuition over data (risky)',
      'Focus only on short-term (misses strategic opportunities)',
    ];
  }

  private estimateSuccessProbability(
    context: DecisionContext,
    additionalInfo?: Record<string, any>
  ): number {
    return 0.75;
  }

  private selectRelevantQuotes(context: DecisionContext): string[] {
    const contextQuotes: Record<string, string[]> = {
      speed: ['Move fast and break things', 'Done is better than perfect'],
      innovation: ['The biggest risk is not taking any risk'],
      data: ['What does the data say?'],
    };

    return contextQuotes.speed || this.profile.famousQuotes.slice(0, 2);
  }

  private selectRelevantExamples(context: DecisionContext): string[] {
    return this.profile.notableDecisions.slice(0, 2).map(d => `${d.decision}: ${d.outcome}`);
  }

  private estimateTimeframe(context: DecisionContext): string {
    return 'Fast iteration in days/weeks, long-term bets over years';
  }

  private identifyResources(context: DecisionContext): string[] {
    return [
      'Engineering talent',
      'Data infrastructure',
      'A/B testing framework',
      'Analytics capability',
      'Capital for long-term bets',
    ];
  }

  private defineKPIs(context: DecisionContext): string[] {
    return [
      'User growth (DAU/MAU)',
      'Engagement metrics',
      'Iteration velocity',
      'Time to ship',
      'A/B test win rate',
      'Long-term strategic positioning',
    ];
  }

  private analyzeDecisionCharacteristics(decision: string): {
    isDataDriven: boolean;
    isFast: boolean;
    isLongTerm: boolean;
    isRiskAverse: boolean;
  } {
    const lower = decision.toLowerCase();
    return {
      isDataDriven: /data|measure|test|metrics|analytics|a\/b/.test(lower),
      isFast: /fast|quick|rapid|immediate|ship|iterate/.test(lower),
      isLongTerm: /long-term|future|strategic|years|platform/.test(lower),
      isRiskAverse: /safe|cautious|conservative|avoid risk/.test(lower),
    };
  }

  private scoreOpportunity(opportunity: string, context: Record<string, any>): number {
    let score = 0.5;
    const lower = opportunity.toLowerCase();

    if (/data|measure|analytics/.test(lower)) score += 0.15;
    if (/fast|quick|iterate/.test(lower)) score += 0.15;
    if (/long-term|future|platform/.test(lower)) score += 0.15;
    if (/scale|growth|network/.test(lower)) score += 0.1;
    if (/bold|aggressive/.test(lower)) score += 0.1;

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
