/**
 * Larry Fink Behavior Analysis Agent
 *
 * Analyzes decisions through the lens of Larry Fink's leadership style,
 * thinking patterns, and strategic approaches.
 *
 * Based on research of his leadership at BlackRock.
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

export class LarryFinkBehaviorAgent implements IBehaviorAgent {
  public readonly profile: LeaderBehaviorProfile;

  constructor(
    private pool: Pool,
    private redis: Redis
  ) {
    this.profile = this.buildProfile();
  }

  private buildProfile(): LeaderBehaviorProfile {
    return {
      name: 'Larry Fink',
      title: 'CEO and Chairman of BlackRock',
      companies: ['BlackRock', 'First Boston'],
      sectors: [
        BusinessSector.FINANCE,
        BusinessSector.TECHNOLOGY,
        BusinessSector.GENERAL,
      ],
      yearsOfExperience: 45,

      leadershipStyles: [
        LeadershipStyle.TRANSFORMATIONAL,
        LeadershipStyle.VISIONARY,
        LeadershipStyle.SERVANT,
      ],

      behavioralTraits: {
        riskTolerance: 0.7,
        innovationDrive: 0.8,
        analyticalThinking: 0.95,
        intuitionReliance: 0.5,
        speedOfDecision: 0.6,
        detailOrientation: 0.85,
        peopleOrientation: 0.7,
        dataOrientation: 0.9,
        longTermFocus: 0.95,
        adaptability: 0.75,
      },

      decisionPatterns: [
        {
          name: 'Long-Term Sustainability Focus',
          description: 'Prioritize long-term value creation and sustainability over short-term gains',
          context: [
            DecisionContext.STRATEGIC_PLANNING,
            DecisionContext.INVESTMENT,
            DecisionContext.OPERATIONS,
          ],
          approach: 'Evaluate decisions through lens of long-term sustainability and stakeholder value',
          keyQuestions: [
            'What are the long-term implications?',
            'Is this sustainable?',
            'How does this impact all stakeholders?',
            'What\'s the 10-year view?',
          ],
          considerations: [
            'Environmental impact',
            'Social responsibility',
            'Governance quality',
            'Long-term value creation',
            'Stakeholder alignment',
          ],
          redFlags: [
            'Short-term profit maximization',
            'Ignoring stakeholder impacts',
            'Unsustainable practices',
            'Poor governance',
          ],
          successIndicators: [
            'Long-term value creation',
            'Stakeholder satisfaction',
            'Sustainable practices',
            'Strong governance',
          ],
          examples: [
            'Annual CEO letters on sustainability',
            'ESG integration in investment process',
            'Climate risk focus',
          ],
        },
        {
          name: 'Stakeholder Capitalism',
          description: 'Consider all stakeholders, not just shareholders',
          context: [
            DecisionContext.STRATEGIC_PLANNING,
            DecisionContext.OPERATIONS,
            DecisionContext.INVESTMENT,
          ],
          approach: 'Balance interests of shareholders, employees, customers, communities, environment',
          keyQuestions: [
            'Who are all the stakeholders?',
            'How does this impact each group?',
            'Are we creating shared value?',
            'What\'s the societal impact?',
          ],
          considerations: [
            'Employee welfare',
            'Community impact',
            'Environmental stewardship',
            'Customer value',
            'Shareholder returns',
          ],
          redFlags: [
            'Shareholder-only focus',
            'Ignoring externalities',
            'Short-term extraction',
            'Stakeholder conflicts',
          ],
          successIndicators: [
            'Stakeholder alignment',
            'Shared value creation',
            'Positive societal impact',
          ],
          examples: [
            'Corporate governance advocacy',
            'Climate change initiatives',
            'Diversity and inclusion focus',
          ],
        },
        {
          name: 'Risk Management Excellence',
          description: 'Deep focus on understanding and managing risk',
          context: [
            DecisionContext.INVESTMENT,
            DecisionContext.STRATEGIC_PLANNING,
            DecisionContext.CRISIS_MANAGEMENT,
          ],
          approach: 'Rigorous risk analysis, scenario planning, stress testing',
          keyQuestions: [
            'What are the risks?',
            'What could go wrong?',
            'Are we properly hedged?',
            'What\'s the downside?',
          ],
          considerations: [
            'Risk-return tradeoffs',
            'Tail risks',
            'Correlation risks',
            'Systemic risks',
          ],
          redFlags: [
            'Ignoring risks',
            'Inadequate hedging',
            'Poor risk measurement',
            'Excessive concentration',
          ],
          successIndicators: [
            'Risk-adjusted returns',
            'Proper diversification',
            'Resilience in crises',
          ],
          examples: [
            'Built BlackRock on risk management (Aladdin platform)',
            'Mortgage crisis navigation',
            'Risk analytics leadership',
          ],
        },
        {
          name: 'Investing Ahead of Structural Trends',
          description: 'Identify and invest in long-term structural growth trends',
          context: [
            DecisionContext.INVESTMENT,
            DecisionContext.STRATEGIC_PLANNING,
            DecisionContext.INNOVATION,
          ],
          approach: 'Identify mega-trends, position ahead of the curve',
          keyQuestions: [
            'What are the structural trends?',
            'Where is the world going?',
            'What will matter in 10 years?',
            'How do demographics drive this?',
          ],
          considerations: [
            'Demographic shifts',
            'Technological change',
            'Climate transition',
            'Geopolitical trends',
          ],
          redFlags: [
            'Following short-term fads',
            'Ignoring structural changes',
            'Fighting mega-trends',
          ],
          successIndicators: [
            'Early positioning in trends',
            'Long-term outperformance',
            'Market leadership',
          ],
          examples: [
            'ETF revolution - built iShares',
            'Private markets expansion',
            'Technology and infrastructure focus',
            'Climate investment',
          ],
        },
      ],

      negotiationTactics: [
        {
          name: 'Relationship-Based Persuasion',
          description: 'Build long-term relationships and influence through thought leadership',
          whenToUse: 'Building strategic partnerships and influencing policy',
          howToApply: 'Share insights, build trust, demonstrate expertise, think long-term',
          risks: ['Slow process', 'Requires patience', 'May not yield immediate results'],
          effectiveness: 0.85,
          examples: [
            'Annual CEO letters influencing corporate behavior',
            'Engagement with portfolio companies on governance',
          ],
        },
        {
          name: 'Data-Driven Advocacy',
          description: 'Use rigorous analysis and data to support positions',
          whenToUse: 'Making investment cases and strategic recommendations',
          howToApply: 'Present comprehensive analysis, quantify impacts, show scenarios',
          risks: ['Analysis paralysis', 'Missing qualitative factors'],
          effectiveness: 0.9,
          examples: [
            'Climate risk analysis',
            'Investment research',
            'Risk assessments',
          ],
        },
        {
          name: 'Stewardship Engagement',
          description: 'Use fiduciary position to engage companies on long-term value',
          whenToUse: 'Influencing portfolio companies',
          howToApply: 'Engage as long-term owner, focus on governance and sustainability',
          risks: ['Relationship strain', 'Slow change', 'Pushback'],
          effectiveness: 0.8,
          examples: [
            'Board engagement on ESG',
            'Climate transition advocacy',
            'Governance improvements',
          ],
        },
      ],

      strategicFrameworks: [
        {
          name: 'Democratization of Investing',
          description: 'Make sophisticated investment strategies accessible to all investors',
          principles: [
            'Lower costs through technology and scale',
            'Accessible products (ETFs, target-date funds)',
            'Education and transparency',
            'Fiduciary responsibility',
          ],
          applicationSteps: [
            'Identify institutional-quality strategies',
            'Productize for retail access',
            'Use technology to lower costs',
            'Educate investors',
            'Scale for efficiency',
          ],
          keyMetrics: [
            'Cost reduction',
            'Retail accessibility',
            'Assets under management',
            'Client outcomes',
          ],
          timeHorizon: 'long',
          successCriteria: [
            'Broad investor access',
            'Lower costs',
            'Better outcomes',
          ],
        },
        {
          name: 'Platform and Technology Leadership',
          description: 'Build technology platforms that create competitive advantage',
          principles: [
            'Technology as core competency',
            'Data and analytics advantage',
            'Platform effects',
            'Continuous innovation',
          ],
          applicationSteps: [
            'Invest in technology infrastructure',
            'Build proprietary platforms (Aladdin)',
            'Leverage data and analytics',
            'Create network effects',
            'License to others',
          ],
          keyMetrics: [
            'Platform adoption',
            'Technology ROI',
            'Data assets',
            'Innovation metrics',
          ],
          timeHorizon: 'long',
          successCriteria: [
            'Technology leadership',
            'Platform dominance',
            'Competitive moat',
          ],
        },
      ],

      innovationApproaches: [
        {
          methodology: 'Structural Trend Identification',
          description: 'Identify and capitalize on long-term structural changes',
          keyPrinciples: [
            'Look 10+ years ahead',
            'Identify demographic and technological shifts',
            'Position ahead of trends',
            'Build for long-term',
          ],
          ideationProcess: [
            'Analyze demographic trends',
            'Study technological changes',
            'Assess climate and environmental shifts',
            'Identify investment implications',
            'Build products and strategies',
          ],
          evaluationCriteria: [
            'Is this a structural trend?',
            'What\'s the 10-year view?',
            'Can we position ahead?',
            'Is it sustainable?',
          ],
          implementationStrategy: [
            'Early positioning',
            'Long-term commitment',
            'Build capabilities',
            'Educate market',
            'Scale over time',
          ],
          examples: [
            'ETF revolution and iShares',
            'Private markets expansion',
            'Climate investing',
            'Technology infrastructure',
          ],
        },
      ],

      leadershipPrinciples: [
        {
          principle: 'Purpose and Profit',
          description: 'Companies must serve a purpose beyond profit to succeed long-term',
          application: 'Evaluate all decisions through lens of purpose and stakeholder value',
          examples: [
            'Annual letters on corporate purpose',
            'ESG integration',
            'Stakeholder capitalism advocacy',
          ],
          quotes: [
            'Profits are in no way inconsistent with purpose – in fact, profits and purpose are inextricably linked',
          ],
        },
        {
          principle: 'Long-Term Thinking',
          description: 'Focus on long-term value creation, resist short-term pressures',
          application: 'Make decisions with 10+ year horizon, build for sustainability',
          examples: [
            'Long-term investment strategies',
            'Infrastructure building',
            'Climate transition planning',
          ],
        },
        {
          principle: 'Fiduciary Responsibility',
          description: 'Act in the best long-term interests of clients',
          application: 'Client outcomes above short-term profits, transparency, stewardship',
          examples: [
            'Client-first culture',
            'Engagement with companies',
            'Fee reduction through scale',
          ],
        },
      ],

      communicationStyle: {
        directness: 0.75,
        formality: 0.7,
        emotionalExpression: 0.5,
        typicalPhrases: [
          'Long-term value creation',
          'Stakeholder capitalism',
          'Climate risk is investment risk',
          'Purpose and profit',
          'Fiduciary responsibility',
          'Structural trends',
        ],
        communicationChannels: ['Annual CEO letters', 'Client communications', 'Public statements', 'Industry events'],
      },

      workStandards: {
        expectationsOfTeam: [
          'Client-first mentality',
          'Long-term thinking',
          'Rigorous analysis',
          'Risk awareness',
          'Ethical behavior',
          'Continuous learning',
        ],
        workEthic: 'Analytical rigor, long-term focus, client service',
        meetingCulture: 'Data-driven discussions, strategic focus',
        decisionMakingSpeed: 'Deliberate, thorough, not rushed',
        failureTolerance: 0.5,
      },

      famousQuotes: [
        'Profits are in no way inconsistent with purpose – in fact, profits and purpose are inextricably linked',
        'Climate risk is investment risk',
        'We focus on sustainability not because we\'re environmentalists, but because we are capitalists',
        'Purpose is the engine of long-term profitability',
        'Every company and every industry will be transformed by the transition to a net zero world',
        'Without a sense of purpose, no company can achieve its full potential',
      ],

      mantras: [
        'Long-term value creation',
        'Stakeholder capitalism',
        'Risk management first',
        'Purpose drives profit',
        'Invest ahead of trends',
        'Fiduciary responsibility',
      ],

      notableDecisions: [
        {
          decision: 'Built Aladdin risk management platform',
          context: 'Recognized technology and risk management as core competency',
          outcome: 'Competitive advantage, licensed to others, BlackRock foundation',
          lessonLearned: 'Technology and risk management create lasting competitive advantage',
        },
        {
          decision: 'Acquired Barclays Global Investors (iShares) for $13.5B in 2009',
          context: 'ETF revolution was structural trend',
          outcome: 'iShares became dominant ETF platform, transformed BlackRock',
          lessonLearned: 'Invest ahead of structural trends even when expensive',
        },
        {
          decision: 'Made climate and sustainability central to investment approach',
          context: 'Recognized climate as systemic financial risk',
          outcome: 'Industry leadership, client alignment, risk management',
          lessonLearned: 'Sustainability is financial imperative, not just values',
        },
        {
          decision: 'Expanded into private markets and alternatives',
          context: 'Identified structural shift in institutional portfolios',
          outcome: 'Major growth driver, client diversification',
          lessonLearned: 'Follow client needs and structural portfolio shifts',
        },
      ],
    };
  }

  async getAdvice(
    question: string,
    context: DecisionContext,
    additionalInfo?: Record<string, any>
  ): Promise<BusinessAdvice> {
    const cacheKey = `fink:advice:${this.hashString(question)}:${context}`;
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
      characteristics.isLongTerm &&
      characteristics.isSustainable &&
      characteristics.considersStakeholders &&
      characteristics.isRiskAware;

    const modifications: string[] = [];
    if (!characteristics.isLongTerm) {
      modifications.push('Extend time horizon - think 10+ years');
    }
    if (!characteristics.isSustainable) {
      modifications.push('Incorporate sustainability and ESG factors');
    }
    if (!characteristics.considersStakeholders) {
      modifications.push('Consider all stakeholders, not just shareholders');
    }
    if (!characteristics.isRiskAware) {
      modifications.push('Conduct thorough risk analysis and scenario planning');
    }

    return {
      wouldSupport,
      reasoning: `Fink ${wouldSupport ? 'would support' : 'would not support'} this decision because ${
        wouldSupport
          ? 'it focuses on long-term value, sustainability, and stakeholder interests with proper risk management'
          : 'it lacks the long-term focus, sustainability perspective, and stakeholder consideration needed'
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
      strategy: `Take a long-term view focused on sustainable value creation for all stakeholders. Identify structural trends and position ahead of them. Use rigorous risk management. Build technology and platform advantages. Serve a purpose beyond profit.`,
      rationale: `Long-term sustainable value creation benefits all stakeholders and delivers superior returns. Structural trends drive decades of growth. Risk management preserves capital. Purpose attracts talent and clients.`,
      steps: [
        'Define purpose and stakeholder value creation',
        'Identify relevant structural trends',
        'Conduct comprehensive risk analysis',
        'Develop long-term strategic plan',
        'Build technology and platform capabilities',
        'Engage stakeholders transparently',
        'Measure and report on long-term metrics',
      ],
      timeline: 'Long-term - years to decades, with near-term milestones',
      risks: [
        'Short-term performance pressures',
        'Stakeholder conflicts',
        'Trend identification errors',
        'Risk model limitations',
        'Technology investment requirements',
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
        reasoning: 'This opportunity aligns with long-term value creation and sustainable growth',
        conditions: [
          'Conduct thorough risk analysis',
          'Ensure stakeholder alignment',
          'Verify sustainability',
          'Build for long-term',
        ],
      };
    } else if (score >= 0.5) {
      return {
        recommendation: 'modify',
        score,
        reasoning: 'Opportunity has potential but needs refinement for sustainability',
        modifications: [
          'Extend time horizon',
          'Incorporate ESG factors',
          'Improve risk management',
          'Align with structural trends',
        ],
      };
    } else {
      return {
        recommendation: 'pass',
        score,
        reasoning: 'This opportunity doesn\'t align with long-term sustainable value creation',
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
        'Think long-term - what matters in 10 years? Identify structural trends and position ahead. Consider all stakeholders. Build sustainable competitive advantages through technology and platforms. Purpose drives long-term profitability.',

      [DecisionContext.PRODUCT_DEVELOPMENT]:
        'Build for long-term client needs. Use technology for scale and accessibility. Focus on democratization. Ensure sustainability. Rigorous risk management from start.',

      [DecisionContext.INNOVATION]:
        'Identify structural trends - demographic, technological, environmental. Position ahead of the curve. Build capabilities for long-term. Technology and platforms create sustainable advantage.',

      [DecisionContext.NEGOTIATION]:
        'Build long-term relationships. Use data and analysis to support positions. Think win-win for all stakeholders. Consider fiduciary responsibilities. Sustainability matters.',

      [DecisionContext.CRISIS_MANAGEMENT]:
        'Rigorous risk analysis. Scenario planning. Stress test assumptions. Protect long-term value. Communicate transparently with stakeholders. Learn and improve systems.',

      [DecisionContext.INVESTMENT]:
        'What are the structural trends? Is this sustainable long-term? Risk-adjusted returns. Stakeholder impacts. Climate and ESG factors. 10-year view.',

      [DecisionContext.HIRING]:
        'Client-first mentality. Long-term thinking. Analytical rigor. Risk awareness. Ethical foundation. Continuous learning. Cultural fit with purpose.',

      [DecisionContext.MARKET_EXPANSION]:
        'Is this a structural trend or fad? Can we build sustainable advantage? What are stakeholder implications? Risk-adjusted opportunity. Long-term client needs.',

      [DecisionContext.PARTNERSHIP]:
        'Long-term alignment. Stakeholder value creation. Technology and platform synergies. Risk considerations. Purpose alignment.',

      [DecisionContext.PRICING]:
        'Fair value for long-term relationship. Use scale and technology to lower costs. Democratization principle. Client outcomes focus.',

      [DecisionContext.MARKETING]:
        'Thought leadership. Educational approach. Transparency. Long-term relationship building. Purpose and values communication.',

      [DecisionContext.OPERATIONS]:
        'Technology and platform leverage. Risk management integration. Client service excellence. Sustainable practices. Continuous improvement.',
    };

    return baseAdvice[context] || baseAdvice[DecisionContext.STRATEGIC_PLANNING];
  }

  private generateReasoning(context: DecisionContext, patterns: any[]): string {
    return `Based on long-term value creation and stakeholder capitalism principles that built BlackRock. Drawing from ${patterns.length} key patterns around sustainability, risk management, and structural trends.`;
  }

  private generateActionableSteps(context: DecisionContext): string[] {
    return [
      'Identify long-term structural trends',
      'Analyze all stakeholder impacts',
      'Conduct comprehensive risk assessment',
      'Develop sustainable approach',
      'Build technology and platform capabilities',
      'Create measurement framework',
      'Communicate transparently',
    ];
  }

  private generateRisks(context: DecisionContext): string[] {
    return [
      'Short-term performance pressures',
      'Structural trend misidentification',
      'Stakeholder conflicts',
      'Technology investment needs',
      'Regulatory changes',
    ];
  }

  private generateAlternatives(context: DecisionContext): string[] {
    return [
      'Short-term profit maximization (not recommended)',
      'Shareholder-only focus (incomplete)',
      'Ignore sustainability (risky)',
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
      sustainability: ['Climate risk is investment risk', 'Purpose drives profit'],
      longterm: ['Purpose is the engine of long-term profitability'],
    };

    return contextQuotes.sustainability || this.profile.famousQuotes.slice(0, 2);
  }

  private selectRelevantExamples(context: DecisionContext): string[] {
    return this.profile.notableDecisions.slice(0, 2).map(d => `${d.decision}: ${d.outcome}`);
  }

  private estimateTimeframe(context: DecisionContext): string {
    return 'Long-term horizon - years to decades with near-term milestones';
  }

  private identifyResources(context: DecisionContext): string[] {
    return [
      'Analytical capabilities',
      'Risk management systems',
      'Technology platforms',
      'Long-term capital',
      'Stakeholder engagement',
    ];
  }

  private defineKPIs(context: DecisionContext): string[] {
    return [
      'Long-term value creation',
      'Risk-adjusted returns',
      'Stakeholder satisfaction',
      'Sustainability metrics',
      'Client outcomes',
      'Platform adoption',
    ];
  }

  private analyzeDecisionCharacteristics(decision: string): {
    isLongTerm: boolean;
    isSustainable: boolean;
    considersStakeholders: boolean;
    isRiskAware: boolean;
  } {
    const lower = decision.toLowerCase();
    return {
      isLongTerm: /long-term|decade|sustainable|structural/.test(lower),
      isSustainable: /sustainable|esg|climate|environment|social/.test(lower),
      considersStakeholders: /stakeholder|community|employee|social|purpose/.test(lower),
      isRiskAware: /risk|hedge|diversif|scenario|stress/.test(lower),
    };
  }

  private scoreOpportunity(opportunity: string, context: Record<string, any>): number {
    let score = 0.5;
    const lower = opportunity.toLowerCase();

    if (/long-term|structural|trend/.test(lower)) score += 0.2;
    if (/sustainable|esg|climate/.test(lower)) score += 0.15;
    if (/stakeholder|purpose/.test(lower)) score += 0.1;
    if (/risk|diversif/.test(lower)) score += 0.1;
    if (/technology|platform/.test(lower)) score += 0.1;

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
