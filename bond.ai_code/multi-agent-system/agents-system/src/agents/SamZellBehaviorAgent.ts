/**
 * Sam Zell Behavior Analysis Agent
 *
 * Analyzes decisions through the lens of Sam Zell's leadership style,
 * thinking patterns, and strategic approaches.
 *
 * Based on research of his real estate and investment career.
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

export class SamZellBehaviorAgent implements IBehaviorAgent {
  public readonly profile: LeaderBehaviorProfile;

  constructor(
    private pool: Pool,
    private redis: Redis
  ) {
    this.profile = this.buildProfile();
  }

  private buildProfile(): LeaderBehaviorProfile {
    return {
      name: 'Sam Zell',
      title: 'Real Estate Investor and "Grave Dancer"',
      companies: ['Equity Group Investments', 'Equity Residential', 'Equity Office', 'Tribune Company'],
      sectors: [
        BusinessSector.REAL_ESTATE,
        BusinessSector.FINANCE,
        BusinessSector.GENERAL,
      ],
      yearsOfExperience: 55,

      leadershipStyles: [
        LeadershipStyle.VISIONARY,
        LeadershipStyle.AUTOCRATIC,
      ],

      behavioralTraits: {
        riskTolerance: 0.85,
        innovationDrive: 0.75,
        analyticalThinking: 0.9,
        intuitionReliance: 0.8,
        speedOfDecision: 0.75,
        detailOrientation: 0.85,
        peopleOrientation: 0.5,
        dataOrientation: 0.85,
        longTermFocus: 0.85,
        adaptability: 0.9,
      },

      decisionPatterns: [
        {
          name: 'Grave Dancing - Distressed Opportunities',
          description: 'Profit from distressed assets and market dislocations',
          context: [
            DecisionContext.INVESTMENT,
            DecisionContext.STRATEGIC_PLANNING,
            DecisionContext.CRISIS_MANAGEMENT,
          ],
          approach: 'Buy when others are forced to sell, profit from distress',
          keyQuestions: [
            'Why is this distressed?',
            'What\'s the intrinsic value?',
            'What\'s the distressed seller\'s timeline?',
            'How can we profit from dislocation?',
          ],
          considerations: [
            'Fundamental value vs. market price',
            'Seller distress factors',
            'Market timing',
            'Recovery potential',
          ],
          redFlags: [
            'Paying market prices',
            'Following the crowd',
            'Ignoring fundamental value',
            'Missing distressed opportunities',
          ],
          successIndicators: [
            'Bought at significant discount',
            'Fundamental value intact',
            'Market recovery potential',
            'Seller desperation',
          ],
          examples: [
            'S&L crisis - bought distressed properties',
            'Equity Office sale at market peak',
            'Distressed real estate in downturns',
          ],
        },
        {
          name: 'Supply and Demand Focus',
          description: 'Relentless focus on supply and demand fundamentals',
          context: [
            DecisionContext.INVESTMENT,
            DecisionContext.MARKET_EXPANSION,
            DecisionContext.STRATEGIC_PLANNING,
          ],
          approach: 'Analyze supply/demand dynamics, invest where supply constrained',
          keyQuestions: [
            'What\'s the supply situation?',
            'Is demand sustainable?',
            'Can new supply come online?',
            'What are the barriers to entry?',
          ],
          considerations: [
            'Current supply levels',
            'Demand drivers',
            'New supply pipeline',
            'Zoning and regulatory barriers',
          ],
          redFlags: [
            'Oversupply risk',
            'Weak demand fundamentals',
            'Easy to replicate',
            'No barriers to entry',
          ],
          successIndicators: [
            'Supply constrained',
            'Strong demand',
            'High barriers to entry',
            'Pricing power',
          ],
          examples: [
            'Apartments in supply-constrained markets',
            'Avoided office glut markets',
            'Focused on barrier-protected locations',
          ],
        },
        {
          name: 'Contrarian Investing',
          description: 'Go against the crowd, profit from being early or different',
          context: [
            DecisionContext.INVESTMENT,
            DecisionContext.STRATEGIC_PLANNING,
            DecisionContext.MARKET_EXPANSION,
          ],
          approach: 'When everyone zigs, zag - find opportunity in unpopular assets',
          keyQuestions: [
            'What is everyone avoiding?',
            'Why is this unpopular?',
            'What do we see that others don\'t?',
            'Are we too early or are we wrong?',
          ],
          considerations: [
            'Market sentiment',
            'Fundamental value',
            'Timing',
            'Risk of being early',
          ],
          redFlags: [
            'Following trends',
            'Buying at peaks',
            'Ignoring fundamentals',
            'Momentum investing',
          ],
          successIndicators: [
            'Out of consensus',
            'Fundamentals support thesis',
            'Patience for market to recognize',
          ],
          examples: [
            'Created REIT structure when novel',
            'Sold Equity Office at peak',
            'Bought distressed when others fled',
          ],
        },
        {
          name: 'Patience and Flexibility',
          description: 'Wait for right opportunity, be flexible in execution',
          context: [
            DecisionContext.INVESTMENT,
            DecisionContext.NEGOTIATION,
            DecisionContext.STRATEGIC_PLANNING,
          ],
          approach: 'Don\'t force deals, wait for opportunity, adapt to circumstances',
          keyQuestions: [
            'Are we forcing this?',
            'Can we wait for better opportunity?',
            'What\'s changed that requires adaptation?',
            'Is this the right time?',
          ],
          considerations: [
            'Opportunity cost',
            'Market timing',
            'Alternative options',
            'Changing circumstances',
          ],
          redFlags: [
            'Desperate to deploy capital',
            'Forcing deals',
            'Rigid thinking',
            'Ignoring market signals',
          ],
          successIndicators: [
            'Waited for opportunity',
            'Adapted to changes',
            'Disciplined pricing',
          ],
          examples: [
            'Held cash during bubbles',
            'Patient capital deployment',
            'Flexible deal structures',
          ],
        },
      ],

      negotiationTactics: [
        {
          name: 'Exploit Seller Distress',
          description: 'Use seller\'s weakness and timeline pressure to negotiate better terms',
          whenToUse: 'Distressed asset acquisitions',
          howToApply: 'Understand seller motivations, timeline, use patience as weapon',
          risks: ['Reputation as vulture', 'Relationship damage', 'Ethical concerns'],
          effectiveness: 0.85,
          examples: [
            'Distressed property negotiations',
            'Forced seller situations',
          ],
        },
        {
          name: 'Supply/Demand Leverage',
          description: 'Use market dynamics knowledge to strengthen negotiating position',
          whenToUse: 'Any real estate or asset negotiation',
          howToApply: 'Demonstrate superior market knowledge, use data on supply/demand',
          risks: ['Overconfidence', 'Market shifts'],
          effectiveness: 0.8,
          examples: [
            'Pricing negotiations based on market data',
            'Timing based on supply pipeline',
          ],
        },
        {
          name: 'Walk-Away Discipline',
          description: 'Willingness to walk away if price or terms not right',
          whenToUse: 'All negotiations',
          howToApply: 'Set discipline on pricing, don\'t chase deals, have alternatives',
          risks: ['Missing opportunities', 'Reputation for being difficult'],
          effectiveness: 0.9,
          examples: [
            'Passed on overpriced deals',
            'Discipline through cycles',
          ],
        },
      ],

      strategicFrameworks: [
        {
          name: 'Liquidity Event Strategy',
          description: 'Build with exit in mind, create liquidity for value realization',
          principles: [
            'Create liquid investment vehicles (REITs)',
            'Build to sell at right time',
            'Recognize market peaks',
            'Monetize when valuations high',
          ],
          applicationSteps: [
            'Structure for eventual liquidity',
            'Build institutional-quality assets',
            'Monitor market valuations',
            'Exit when price is right',
            'Recycle capital to new opportunities',
          ],
          keyMetrics: [
            'Exit multiples',
            'Market valuations',
            'Comparable transactions',
            'IRR on exits',
          ],
          timeHorizon: 'medium',
          successCriteria: [
            'Successful exits at peak valuations',
            'Capital recycled profitably',
            'Liquidity created',
          ],
        },
        {
          name: 'REIT Pioneering',
          description: 'Use REIT structure for scale, liquidity, and tax advantages',
          principles: [
            'Public markets provide liquidity',
            'Scale advantages in real estate',
            'Tax-efficient structure',
            'Access to capital markets',
          ],
          applicationSteps: [
            'Build portfolio of similar assets',
            'Create REIT structure',
            'Go public for liquidity',
            'Use currency for acquisitions',
            'Manage for total return',
          ],
          keyMetrics: [
            'FFO growth',
            'NAV per share',
            'Dividend yield',
            'Stock performance',
          ],
          timeHorizon: 'long',
          successCriteria: [
            'Market-leading REIT',
            'Strong shareholder returns',
            'Efficient capital structure',
          ],
        },
      ],

      innovationApproaches: [
        {
          methodology: 'Fundamentals-Based Innovation',
          description: 'Innovate in structure and approach while respecting supply/demand fundamentals',
          keyPrinciples: [
            'Structure innovation (REITs)',
            'Market timing innovation',
            'Respect fundamentals always',
            'Look where others don\'t',
          ],
          ideationProcess: [
            'Identify market inefficiency',
            'Understand why it exists',
            'Design innovative approach',
            'Validate with fundamentals',
            'Execute contrarian strategy',
          ],
          evaluationCriteria: [
            'Do fundamentals support it?',
            'Is market mispricing this?',
            'Can we profit from dislocation?',
            'What\'s the risk?',
          ],
          implementationStrategy: [
            'Start with deep research',
            'Be patient for opportunity',
            'Execute with discipline',
            'Exit when overvalued',
          ],
          examples: [
            'REIT structure innovation',
            'Distressed investing approach',
            'Market timing excellence',
          ],
        },
      ],

      leadershipPrinciples: [
        {
          principle: 'Focus on Fundamentals',
          description: 'Supply and demand are the only things that matter',
          application: 'Every decision analyzed through supply/demand lens',
          examples: [
            'Apartment investing in supply-constrained markets',
            'Avoiding oversupplied markets',
          ],
          quotes: [
            'Supply and demand is all that matters',
          ],
        },
        {
          principle: 'Be Contrarian',
          description: 'Profit comes from being different and right',
          application: 'Go against crowd when fundamentals support it',
          examples: [
            'Grave dancing in downturns',
            'Selling at peaks',
          ],
          quotes: [
            'If everyone is going left, look right',
          ],
        },
        {
          principle: 'Discipline Over Activity',
          description: 'Better to do nothing than to do something stupid',
          application: 'Patient capital, waiting for right opportunities',
          examples: [
            'Holding cash in bubbles',
            'Walking away from bad deals',
          ],
        },
      ],

      communicationStyle: {
        directness: 0.95,
        formality: 0.2,
        emotionalExpression: 0.6,
        typicalPhrases: [
          'Supply and demand',
          'Grave dancing',
          'Where\'s the puck going?',
          'Be patient',
          'Focus on fundamentals',
          'Don\'t confuse liquidity with value',
        ],
        communicationChannels: ['Direct conversations', 'Interviews', 'Investor meetings', 'Public speaking'],
      },

      workStandards: {
        expectationsOfTeam: [
          'Understand supply and demand',
          'Think independently',
          'Be contrarian when right',
          'Disciplined execution',
          'Know when to walk away',
        ],
        workEthic: 'Analytical rigor, patience, contrarian thinking',
        meetingCulture: 'Direct, focused on fundamentals',
        decisionMakingSpeed: 'Deliberate when needed, decisive when opportunity clear',
        failureTolerance: 0.6,
      },

      famousQuotes: [
        'If everyone is going left, look right',
        'Supply and demand is all that matters',
        'Be curious, not judgmental',
        'When the puck is moving right, skate left',
        'Real estate is a commodity business',
        'Failure is part of success - the key is to learn',
        'If you don\'t have a competitive advantage, don\'t compete',
      ],

      mantras: [
        'Supply and demand',
        'Grave dancing',
        'Be contrarian',
        'Focus on fundamentals',
        'Patient capital',
        'Know when to sell',
      ],

      notableDecisions: [
        {
          decision: 'Pioneered apartment REITs with Equity Residential',
          context: 'Created new structure for real estate investing',
          outcome: 'Built massive apartment empire, liquidity for investors',
          lessonLearned: 'Innovation in structure can create enormous value',
        },
        {
          decision: 'Sold Equity Office for $39B at market peak in 2007',
          context: 'Office market at all-time highs, recognized bubble',
          outcome: 'Perfectly timed exit before crash, buyer lost billions',
          lessonLearned: 'Know when to sell - market timing matters enormously',
        },
        {
          decision: 'Built fortune through distressed real estate investing',
          context: 'S&L crisis, real estate downturns',
          outcome: 'Massive profits from "grave dancing"',
          lessonLearned: 'Profit from others\' distress - buy when others forced to sell',
        },
        {
          decision: 'Tribune Company acquisition (one that didn\'t work)',
          context: 'Bought newspaper company at wrong time',
          outcome: 'Bankruptcy, major loss',
          lessonLearned: 'Even experts make mistakes - stick to your competence',
        },
      ],
    };
  }

  async getAdvice(
    question: string,
    context: DecisionContext,
    additionalInfo?: Record<string, any>
  ): Promise<BusinessAdvice> {
    const cacheKey = `zell:advice:${this.hashString(question)}:${context}`;
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
      characteristics.isFundamentBased &&
      characteristics.isContrarian &&
      characteristics.hasPatience &&
      !characteristics.isFollowingCrowd;

    const modifications: string[] = [];
    if (!characteristics.isFundamentBased) {
      modifications.push('Focus on supply and demand fundamentals');
    }
    if (!characteristics.isContrarian) {
      modifications.push('Look for contrarian angle - what is everyone missing?');
    }
    if (!characteristics.hasPatience) {
      modifications.push('Be more patient - wait for right opportunity');
    }
    if (characteristics.isFollowingCrowd) {
      modifications.push('Don\'t follow the crowd - look where others aren\'t');
    }

    return {
      wouldSupport,
      reasoning: `Zell ${wouldSupport ? 'would support' : 'would not support'} this decision because ${
        wouldSupport
          ? 'it\'s based on fundamentals, contrarian, and shows patience'
          : 'it lacks focus on fundamentals, contrarian thinking, or shows herd mentality'
      }`,
      modifications,
      confidence: wouldSupport ? 0.8 : 0.75,
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
      strategy: `Focus on supply and demand fundamentals. Be contrarian - look where others aren't. Be patient for the right opportunity. Look for distressed situations. Know when to sell. Don't confuse liquidity with value.`,
      rationale: `Supply and demand drive everything. Profits come from being different and right. Patience allows you to wait for opportunity. Distress creates mispricing. Knowing when to sell is as important as knowing when to buy.`,
      steps: [
        'Analyze supply and demand fundamentals deeply',
        'Identify contrarian opportunities',
        'Look for distressed situations',
        'Be patient - don\'t force deals',
        'Execute with discipline when opportunity appears',
        'Plan exit from beginning',
        'Monitor for selling opportunities',
      ],
      timeline: 'Patient capital - wait for opportunity, hold through cycles',
      risks: [
        'Being too contrarian and wrong',
        'Missing opportunities through patience',
        'Market timing errors',
        'Distressed assets may not recover',
        'Exit timing challenges',
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
        reasoning: 'This opportunity aligns with fundamental supply/demand analysis and contrarian positioning',
        conditions: [
          'Verify supply and demand fundamentals',
          'Ensure contrarian positioning supported by data',
          'Have patience for full cycle',
          'Plan exit strategy',
        ],
      };
    } else if (score >= 0.5) {
      return {
        recommendation: 'modify',
        score,
        reasoning: 'Opportunity needs refinement to align with fundamentals',
        modifications: [
          'Strengthen fundamental analysis',
          'Find contrarian angle',
          'Add discipline on pricing',
          'Define clear exit strategy',
        ],
      };
    } else {
      return {
        recommendation: 'pass',
        score,
        reasoning: 'This doesn\'t align with fundamental investing or shows herd mentality',
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
        'Focus on supply and demand - that\'s all that matters. Be contrarian. Where is everyone going? Go the other way if fundamentals support it. Be patient. Know when to sell.',

      [DecisionContext.PRODUCT_DEVELOPMENT]:
        'What do supply and demand fundamentals say? Is there real demand? How much supply exists or can come online? Don\'t build what everyone else is building.',

      [DecisionContext.INNOVATION]:
        'Innovate in structure and approach, not necessarily product. REITs were structural innovation. Look for market inefficiencies and innovative ways to exploit them.',

      [DecisionContext.NEGOTIATION]:
        'Understand the other side\'s distress and timeline. Be patient. Use superior market knowledge. Walk away if price isn\'t right. Discipline beats activity.',

      [DecisionContext.CRISIS_MANAGEMENT]:
        'Crisis creates opportunity. This is when grave dancing happens. Look for distressed assets. Understand what\'s being forced. Have patience and capital ready.',

      [DecisionContext.INVESTMENT]:
        'What are supply and demand fundamentals? Why is this mispriced? Are we being contrarian? Is there distress we can exploit? What\'s the exit? Can we be patient?',

      [DecisionContext.HIRING]:
        'Do they understand fundamentals? Can they think independently? Are they contrarian when warranted? Do they have discipline? Will they challenge assumptions?',

      [DecisionContext.MARKET_EXPANSION]:
        'What\'s the supply situation? Is demand sustainable? Barriers to entry? Are we early or just different? Can we profit from being contrarian here?',

      [DecisionContext.PARTNERSHIP]:
        'Does this give us better access to supply or demand? What\'s their distress level if any? Can we maintain independence? What are real fundamentals?',

      [DecisionContext.PRICING]:
        'What do supply and demand say? What are comparable transactions? Are we in a bubble? Don\'t confuse liquidity with value. Be disciplined.',

      [DecisionContext.MARKETING]:
        'In commodity businesses, fundamentals matter more than marketing. Focus resources on understanding supply and demand, not advertising.',

      [DecisionContext.OPERATIONS]:
        'Operational excellence in commodity business means cost discipline and efficiency. Don\'t try to differentiate a commodity - just execute better.',
    };

    return baseAdvice[context] || baseAdvice[DecisionContext.STRATEGIC_PLANNING];
  }

  private generateReasoning(context: DecisionContext, patterns: any[]): string {
    return `Based on supply/demand fundamentals and contrarian investing that built multi-billion dollar real estate empire. Drawing from ${patterns.length} key patterns around grave dancing, fundamentals, and patient capital.`;
  }

  private generateActionableSteps(context: DecisionContext): string[] {
    return [
      'Analyze supply and demand fundamentals',
      'Identify contrarian opportunities',
      'Look for distressed situations',
      'Be patient for right pricing',
      'Execute with discipline',
      'Plan exit strategy',
      'Monitor market for selling opportunity',
    ];
  }

  private generateRisks(context: DecisionContext): string[] {
    return [
      'Contrarian position may be wrong',
      'Patience may cause missed opportunities',
      'Market timing risk',
      'Distress may not create opportunity',
      'Exit timing challenges',
    ];
  }

  private generateAlternatives(context: DecisionContext): string[] {
    return [
      'Follow the crowd (not recommended)',
      'Ignore fundamentals (dangerous)',
      'Force deals without patience (costly)',
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
      contrarian: ['If everyone is going left, look right'],
      fundamentals: ['Supply and demand is all that matters'],
    };

    return contextQuotes.fundamentals || this.profile.famousQuotes.slice(0, 2);
  }

  private selectRelevantExamples(context: DecisionContext): string[] {
    return this.profile.notableDecisions.slice(0, 2).map(d => `${d.decision}: ${d.outcome}`);
  }

  private estimateTimeframe(context: DecisionContext): string {
    return 'Patient capital - wait for opportunity, hold through cycles';
  }

  private identifyResources(context: DecisionContext): string[] {
    return [
      'Market research capabilities',
      'Supply/demand analysis',
      'Patient capital',
      'Deal discipline',
      'Exit planning',
    ];
  }

  private defineKPIs(context: DecisionContext): string[] {
    return [
      'Supply/demand ratios',
      'Entry pricing vs fundamentals',
      'IRR on investments',
      'Exit timing and multiples',
      'Contrarian position validation',
    ];
  }

  private analyzeDecisionCharacteristics(decision: string): {
    isFundamentBased: boolean;
    isContrarian: boolean;
    hasPatience: boolean;
    isFollowingCrowd: boolean;
  } {
    const lower = decision.toLowerCase();
    return {
      isFundamentBased: /supply|demand|fundamental|analysis|market/.test(lower),
      isContrarian: /contrarian|different|against|unconventional/.test(lower),
      hasPatience: /patient|wait|discipline|timing/.test(lower),
      isFollowingCrowd: /trend|popular|everyone|consensus/.test(lower),
    };
  }

  private scoreOpportunity(opportunity: string, context: Record<string, any>): number {
    let score = 0.5;
    const lower = opportunity.toLowerCase();

    if (/supply|demand|fundamental/.test(lower)) score += 0.25;
    if (/contrarian|distressed|mispriced/.test(lower)) score += 0.2;
    if (/patient|disciplined|timing/.test(lower)) score += 0.1;
    if (/exit|liquidity/.test(lower)) score += 0.1;
    if (/trend|popular|consensus/.test(lower)) score -= 0.2;

    return Math.max(0, Math.min(1, score));
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
