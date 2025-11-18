/**
 * Donald Bren Behavior Analysis Agent
 *
 * Analyzes decisions through the lens of Donald Bren's leadership style,
 * thinking patterns, and strategic approaches.
 *
 * Based on research of his real estate development career at The Irvine Company.
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

export class DonaldBrenBehaviorAgent implements IBehaviorAgent {
  public readonly profile: LeaderBehaviorProfile;

  constructor(
    private pool: Pool,
    private redis: Redis
  ) {
    this.profile = this.buildProfile();
  }

  private buildProfile(): LeaderBehaviorProfile {
    return {
      name: 'Donald Bren',
      title: 'Chairman of The Irvine Company',
      companies: ['The Irvine Company', 'Bren Company'],
      sectors: [
        BusinessSector.REAL_ESTATE,
        BusinessSector.RETAIL,
      ],
      yearsOfExperience: 60,

      leadershipStyles: [
        LeadershipStyle.VISIONARY,
        LeadershipStyle.SERVANT,
        LeadershipStyle.AUTOCRATIC,
      ],

      behavioralTraits: {
        riskTolerance: 0.65,
        innovationDrive: 0.75,
        analyticalThinking: 0.9,
        intuitionReliance: 0.7,
        speedOfDecision: 0.5,
        detailOrientation: 0.95,
        peopleOrientation: 0.6,
        dataOrientation: 0.85,
        longTermFocus: 0.98,
        adaptability: 0.7,
      },

      decisionPatterns: [
        {
          name: 'Quality and Attention to Detail',
          description: 'Obsessive focus on quality and every detail of development',
          context: [
            DecisionContext.PRODUCT_DEVELOPMENT,
            DecisionContext.OPERATIONS,
            DecisionContext.STRATEGIC_PLANNING,
          ],
          approach: 'Meticulous planning and execution, no detail too small',
          keyQuestions: [
            'Is this the highest quality?',
            'Have we thought through every detail?',
            'Will this stand the test of time?',
            'What would perfect look like?',
          ],
          considerations: [
            'Long-term quality',
            'Attention to every detail',
            'Craftsmanship',
            'Materials and finishes',
            'Tenant/resident experience',
          ],
          redFlags: [
            'Cutting corners on quality',
            'Rushing development',
            'Ignoring details',
            'Short-term thinking',
          ],
          successIndicators: [
            'Exceptional quality',
            'Perfect execution',
            'Long-lasting value',
            'Tenant satisfaction',
          ],
          examples: [
            'Irvine master-planned communities',
            'Fashion Island and South Coast Plaza',
            'Apartment communities with resort amenities',
          ],
        },
        {
          name: 'Long-Term Vision and Patient Development',
          description: 'Think in decades and generations, not quarters',
          context: [
            DecisionContext.STRATEGIC_PLANNING,
            DecisionContext.INVESTMENT,
            DecisionContext.MARKET_EXPANSION,
          ],
          approach: 'Multi-generational planning, patient capital, build for 100 years',
          keyQuestions: [
            'What will this look like in 50 years?',
            'Are we building for generations?',
            'What\'s the long-term vision?',
            'How does this fit the master plan?',
          ],
          considerations: [
            'Multi-decade timeframe',
            'Master plan coherence',
            'Future community needs',
            'Legacy and sustainability',
          ],
          redFlags: [
            'Short-term profit focus',
            'Quarterly thinking',
            'Piecemeal development',
            'Ignoring master plan',
          ],
          successIndicators: [
            'Coherent long-term vision',
            'Sustainable growth',
            'Community value appreciation',
            'Generational impact',
          ],
          examples: [
            'Irvine Ranch master plan - 50+ year vision',
            'Phased development over decades',
            'Long-term land holdings',
          ],
        },
        {
          name: 'Resist Short-Term Profits for Long-Term Value',
          description: 'Willing to sacrifice near-term gains for sustainable long-term value',
          context: [
            DecisionContext.STRATEGIC_PLANNING,
            DecisionContext.INVESTMENT,
            DecisionContext.OPERATIONS,
          ],
          approach: 'Hold for appreciation, resist selling pressure, reinvest',
          keyQuestions: [
            'Does selling now maximize long-term value?',
            'Should we hold for more appreciation?',
            'What\'s the opportunity cost of selling?',
            'Are we thinking long enough term?',
          ],
          considerations: [
            'Long-term value creation',
            'Holding period returns',
            'Reinvestment opportunities',
            'Market cycles',
          ],
          redFlags: [
            'Pressure to realize gains',
            'Short-term cash needs',
            'Market timing attempts',
            'Impatient capital',
          ],
          successIndicators: [
            'Long-term value maximization',
            'Compounding returns',
            'Market leadership position',
          ],
          examples: [
            'Held Irvine properties for decades',
            'Resisted selling in up markets',
            'Reinvested proceeds in quality',
          ],
        },
        {
          name: 'Sustainability and Environmental Responsibility',
          description: 'Integrate environmental stewardship into all developments',
          context: [
            DecisionContext.PRODUCT_DEVELOPMENT,
            DecisionContext.STRATEGIC_PLANNING,
            DecisionContext.OPERATIONS,
          ],
          approach: 'Green building, land preservation, sustainable practices',
          keyQuestions: [
            'How can we minimize environmental impact?',
            'What land should be preserved?',
            'Are we building sustainably?',
            'What\'s our environmental legacy?',
          ],
          considerations: [
            'Environmental impact',
            'Land preservation',
            'Green building practices',
            'Community health',
            'Long-term sustainability',
          ],
          redFlags: [
            'Ignoring environmental concerns',
            'Maximizing development footprint',
            'Unsustainable practices',
            'Short-term environmental tradeoffs',
          ],
          successIndicators: [
            'Environmental awards',
            'Land preserved',
            'LEED certifications',
            'Sustainable operations',
          ],
          examples: [
            '50,000+ acres preserved in Irvine',
            'LEED-certified buildings',
            'Environmental restoration',
          ],
        },
      ],

      negotiationTactics: [
        {
          name: 'Patient Capital Advantage',
          description: 'Use ability to wait and long-term horizon as negotiating strength',
          whenToUse: 'Acquisitions and strategic transactions',
          howToApply: 'Emphasize long-term partnership, no pressure to transact quickly',
          risks: ['Missing time-sensitive opportunities', 'Market changes while waiting'],
          effectiveness: 0.8,
          examples: [
            'Gradual acquisition of Irvine Company',
            'Patient land assemblage',
          ],
        },
        {
          name: 'Quality Premium Justification',
          description: 'Justify premium pricing through demonstrated quality and service',
          whenToUse: 'Pricing and value capture',
          howToApply: 'Show quality differences, long-term value, tenant satisfaction',
          risks: ['Price resistance', 'Competition undercutting'],
          effectiveness: 0.85,
          examples: [
            'Premium apartment rents',
            'High-end retail positioning',
          ],
        },
        {
          name: 'Private and Low-Profile Approach',
          description: 'Maintain privacy, avoid publicity in negotiations',
          whenToUse: 'All negotiations',
          howToApply: 'Quiet negotiations, discretion, privacy maintained',
          risks: ['Less market leverage', 'Information asymmetry'],
          effectiveness: 0.75,
          examples: [
            'Private company structure',
            'Discreet transactions',
          ],
        },
      ],

      strategicFrameworks: [
        {
          name: 'Master-Planned Community Development',
          description: 'Develop entire communities with integrated planning over decades',
          principles: [
            'Comprehensive master planning',
            'Mixed-use integration',
            'Quality of life focus',
            'Environmental preservation',
            'Multi-decade execution',
          ],
          applicationSteps: [
            'Create long-term master plan',
            'Phase development strategically',
            'Integrate residential, commercial, open space',
            'Maintain quality standards',
            'Preserve environmental assets',
            'Build community amenities',
            'Execute patiently over decades',
          ],
          keyMetrics: [
            'Property value appreciation',
            'Resident satisfaction',
            'Occupancy rates',
            'Environmental preservation',
            'Community awards',
          ],
          timeHorizon: 'long',
          successCriteria: [
            'Thriving communities',
            'Premium valuations',
            'Environmental stewardship',
            'Generational success',
          ],
        },
        {
          name: 'Location Excellence',
          description: 'Focus on premier locations with long-term appreciation potential',
          principles: [
            'Location is paramount',
            'Coastal California focus',
            'Limited supply locations',
            'Proximity to economic centers',
            'Quality of life locations',
          ],
          applicationSteps: [
            'Identify premier locations',
            'Acquire strategically',
            'Hold for long-term',
            'Develop to highest quality',
            'Capture location premium',
          ],
          keyMetrics: [
            'Location desirability',
            'Property value growth',
            'Competitive positioning',
            'Scarcity value',
          ],
          timeHorizon: 'long',
          successCriteria: [
            'Market-leading locations',
            'Premium pricing power',
            'Long-term appreciation',
          ],
        },
      ],

      innovationApproaches: [
        {
          methodology: 'Quality-Focused Innovation',
          description: 'Innovate in quality, sustainability, and community design',
          keyPrinciples: [
            'Quality over quantity',
            'Sustainable practices',
            'Community-centric design',
            'Long-term value focus',
          ],
          ideationProcess: [
            'Study best practices globally',
            'Engage experts and consultants',
            'Plan meticulously',
            'Test and refine',
            'Execute to perfection',
          ],
          evaluationCriteria: [
            'Does it enhance quality?',
            'Is it sustainable long-term?',
            'Does it serve the community?',
            'Will it appreciate over time?',
          ],
          implementationStrategy: [
            'Thorough planning phase',
            'Hire best architects and designers',
            'Meticulous execution',
            'Quality control throughout',
            'Long-term maintenance',
          ],
          examples: [
            'Master-planned communities',
            'Resort-style apartment living',
            'Environmental preservation',
            'LEED-certified development',
          ],
        },
      ],

      leadershipPrinciples: [
        {
          principle: 'Quality Above All',
          description: 'Never compromise on quality - it pays over the long term',
          application: 'Maintain highest standards in all developments',
          examples: [
            'Premium materials and finishes',
            'Meticulous maintenance',
            'Best-in-class amenities',
          ],
        },
        {
          principle: 'Think Generationally',
          description: 'Plan and build for multiple generations, not just next quarter',
          application: 'All decisions evaluated on 50+ year timeframe',
          examples: [
            'Irvine Ranch master plan',
            'Land preservation for future',
            'Sustainable development',
          ],
        },
        {
          principle: 'Environmental Stewardship',
          description: 'Preserve and protect natural environment as core responsibility',
          application: 'Integrate conservation into all planning',
          examples: [
            '50,000+ acres preserved',
            'Environmental restoration',
            'Green building practices',
          ],
        },
        {
          principle: 'Privacy and Discretion',
          description: 'Maintain low profile, let work speak for itself',
          application: 'Avoid publicity, focus on execution',
          examples: [
            'Rarely gives interviews',
            'Private company structure',
            'Quiet transactions',
          ],
        },
      ],

      communicationStyle: {
        directness: 0.6,
        formality: 0.7,
        emotionalExpression: 0.3,
        typicalPhrases: [
          'Quality matters',
          'Think long-term',
          'Attention to detail',
          'Environmental responsibility',
          'Building for generations',
          'Location, location, location',
        ],
        communicationChannels: ['Internal meetings', 'Written communications', 'Rare public statements'],
      },

      workStandards: {
        expectationsOfTeam: [
          'Obsessive attention to detail',
          'Quality without compromise',
          'Long-term thinking',
          'Environmental responsibility',
          'Discretion and privacy',
          'Patience in execution',
        ],
        workEthic: 'Meticulous, patient, quality-focused, long-term oriented',
        meetingCulture: 'Detailed, thorough, quality-focused',
        decisionMakingSpeed: 'Deliberate and thorough - not rushed',
        failureTolerance: 0.4,
      },

      famousQuotes: [
        'We\'re building for the next 100 years',
        'Quality is never an accident',
        'Location, location, location',
        'We take a long-term view',
        'Environmental stewardship is a responsibility',
        'Details matter',
        'Patience pays dividends',
      ],

      mantras: [
        'Quality above all',
        'Think generationally',
        'Attention to detail',
        'Environmental stewardship',
        'Long-term value',
        'Location excellence',
      ],

      notableDecisions: [
        {
          decision: 'Acquired majority control of Irvine Company',
          context: 'Saw long-term potential in master-planned development',
          outcome: 'Built one of America\'s most valuable private real estate companies',
          lessonLearned: 'Long-term vision and quality create extraordinary value',
        },
        {
          decision: 'Preserved 50,000+ acres of open space in Irvine Ranch',
          context: 'Could have developed but chose environmental preservation',
          outcome: 'Enhanced value of developed properties, environmental legacy',
          lessonLearned: 'Preservation can enhance value more than development',
        },
        {
          decision: 'Held properties through market cycles rather than selling',
          context: 'Resisted pressure to cash out in hot markets',
          outcome: 'Compounded returns over decades, market leadership',
          lessonLearned: 'Patient capital and long holding periods maximize value',
        },
        {
          decision: 'Invested in quality and sustainability before it was trendy',
          context: 'Green building and sustainability as core principle',
          outcome: 'Market leadership, premium positioning, environmental awards',
          lessonLearned: 'Quality and sustainability attract premium tenants and buyers',
        },
      ],
    };
  }

  async getAdvice(
    question: string,
    context: DecisionContext,
    additionalInfo?: Record<string, any>
  ): Promise<BusinessAdvice> {
    const cacheKey = `bren:advice:${this.hashString(question)}:${context}`;
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
      characteristics.isQualityFocused &&
      characteristics.isLongTerm &&
      characteristics.isSustainable &&
      characteristics.hasDetailOrientation;

    const modifications: string[] = [];
    if (!characteristics.isQualityFocused) {
      modifications.push('Elevate quality standards - build for 100 years');
    }
    if (!characteristics.isLongTerm) {
      modifications.push('Extend time horizon - think generationally');
    }
    if (!characteristics.isSustainable) {
      modifications.push('Integrate environmental sustainability');
    }
    if (!characteristics.hasDetailOrientation) {
      modifications.push('Increase attention to detail - every detail matters');
    }

    return {
      wouldSupport,
      reasoning: `Bren ${wouldSupport ? 'would support' : 'would not support'} this decision because ${
        wouldSupport
          ? 'it demonstrates quality focus, long-term thinking, and sustainability'
          : 'it lacks the quality standards, long-term vision, and detail orientation required'
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
      strategy: `Focus on quality above all else. Think in generations, not quarters. Plan meticulously with attention to every detail. Integrate environmental sustainability. Choose premier locations. Be patient - build for 100 years.`,
      rationale: `Quality creates long-term value that compounds over decades. Generational thinking avoids short-term mistakes. Details matter for lasting excellence. Sustainability is both responsibility and value creator. Premier locations appreciate.`,
      steps: [
        'Create comprehensive long-term master plan',
        'Set uncompromising quality standards',
        'Plan every detail meticulously',
        'Integrate environmental sustainability',
        'Choose or develop premier locations',
        'Execute patiently over years/decades',
        'Maintain quality through operations',
      ],
      timeline: 'Generational - decades, not years',
      risks: [
        'High quality standards increase costs',
        'Long-term approach delays returns',
        'Patience may miss short-term opportunities',
        'Environmental preservation reduces development area',
        'Market may not value quality premium',
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
        reasoning: 'This opportunity aligns with quality focus and long-term value creation',
        conditions: [
          'Maintain uncompromising quality standards',
          'Think generationally - 50+ year view',
          'Integrate environmental sustainability',
          'Attend to every detail',
          'Be patient in execution',
        ],
      };
    } else if (score >= 0.5) {
      return {
        recommendation: 'modify',
        score,
        reasoning: 'Opportunity needs refinement for quality and sustainability',
        modifications: [
          'Raise quality standards significantly',
          'Extend time horizon to generational',
          'Add environmental sustainability',
          'Increase detail and planning',
          'Ensure premier location',
        ],
      };
    } else {
      return {
        recommendation: 'pass',
        score,
        reasoning: 'This doesn\'t align with quality standards and long-term value creation',
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
        'Think in generations, not quarters. Create a comprehensive master plan. Focus on quality and premier locations. Integrate environmental stewardship. Be patient - we\'re building for 100 years.',

      [DecisionContext.PRODUCT_DEVELOPMENT]:
        'Quality is never an accident. Plan every detail meticulously. Use the best materials. Build to last. Think about how this will look and function in 50 years. Sustainability must be integrated.',

      [DecisionContext.INNOVATION]:
        'Innovate in quality, sustainability, and community design. Study global best practices. Hire the best consultants. Plan thoroughly. Execute to perfection. Long-term value over novelty.',

      [DecisionContext.NEGOTIATION]:
        'Patient capital is an advantage. No pressure to transact quickly. Quality justifies premium. Maintain discretion. Think long-term partnership. Location and quality are our leverage.',

      [DecisionContext.CRISIS_MANAGEMENT]:
        'Stay focused on long-term fundamentals. Don\'t panic. Quality assets recover. Be patient. Use dislocation to improve quality. Think generationally, not quarterly.',

      [DecisionContext.INVESTMENT]:
        'Location, location, location. Is this a premier location with long-term appreciation potential? Can we execute with quality? Can we hold for decades? Does it fit the master plan?',

      [DecisionContext.HIRING]:
        'Look for attention to detail, quality focus, long-term thinking, environmental awareness, patience. Can they plan meticulously? Do they share quality values?',

      [DecisionContext.MARKET_EXPANSION]:
        'Only pursue premier locations. Can we maintain quality standards? Does it fit long-term master plan? Can we be patient in development? Is environmental stewardship possible?',

      [DecisionContext.PARTNERSHIP]:
        'Do they share quality values? Long-term orientation? Environmental responsibility? Detail orientation? Can they maintain our standards? Private and discreet?',

      [DecisionContext.PRICING]:
        'Quality commands premium pricing. Location justifies higher prices. Don\'t compete on price - compete on quality. Long-term residents/tenants value quality.',

      [DecisionContext.MARKETING]:
        'Let quality speak for itself. Word of mouth from satisfied tenants. Maintain discretion. Focus on execution over promotion. Quality is the best marketing.',

      [DecisionContext.OPERATIONS]:
        'Meticulous maintenance preserves quality. Attention to every detail. Sustainability in operations. Long-term thinking in all decisions. Quality never compromised.',
    };

    return baseAdvice[context] || baseAdvice[DecisionContext.STRATEGIC_PLANNING];
  }

  private generateReasoning(context: DecisionContext, patterns: any[]): string {
    return `Based on quality focus and generational thinking that built The Irvine Company. Drawing from ${patterns.length} key patterns around quality, long-term vision, and environmental stewardship.`;
  }

  private generateActionableSteps(context: DecisionContext): string[] {
    return [
      'Create comprehensive long-term plan',
      'Set uncompromising quality standards',
      'Plan every detail meticulously',
      'Integrate environmental sustainability',
      'Select or develop premier location',
      'Execute with patience over time',
      'Maintain quality through operations',
    ];
  }

  private generateRisks(context: DecisionContext): string[] {
    return [
      'Quality standards increase costs',
      'Long-term approach delays returns',
      'Patience may miss opportunities',
      'Market may not pay quality premium initially',
      'Environmental preservation limits development',
    ];
  }

  private generateAlternatives(context: DecisionContext): string[] {
    return [
      'Lower quality for faster returns (not recommended)',
      'Short-term profit focus (misses long-term value)',
      'Rush to market (compromises quality)',
    ];
  }

  private estimateSuccessProbability(
    context: DecisionContext,
    additionalInfo?: Record<string, any>
  ): number {
    return 0.85;
  }

  private selectRelevantQuotes(context: DecisionContext): string[] {
    const contextQuotes: Record<string, string[]> = {
      quality: ['Quality is never an accident'],
      longterm: ['We\'re building for the next 100 years'],
      location: ['Location, location, location'],
    };

    return contextQuotes.quality || this.profile.famousQuotes.slice(0, 2);
  }

  private selectRelevantExamples(context: DecisionContext): string[] {
    return this.profile.notableDecisions.slice(0, 2).map(d => `${d.decision}: ${d.outcome}`);
  }

  private estimateTimeframe(context: DecisionContext): string {
    return 'Generational - think in decades and generations';
  }

  private identifyResources(context: DecisionContext): string[] {
    return [
      'Patient long-term capital',
      'Best architects and designers',
      'Quality materials and craftsmanship',
      'Environmental consultants',
      'Master planning expertise',
      'Meticulous project management',
    ];
  }

  private defineKPIs(context: DecisionContext): string[] {
    return [
      'Quality metrics and standards',
      'Long-term property value appreciation',
      'Tenant/resident satisfaction',
      'Environmental preservation',
      'Occupancy and retention rates',
      'Community awards and recognition',
    ];
  }

  private analyzeDecisionCharacteristics(decision: string): {
    isQualityFocused: boolean;
    isLongTerm: boolean;
    isSustainable: boolean;
    hasDetailOrientation: boolean;
  } {
    const lower = decision.toLowerCase();
    return {
      isQualityFocused: /quality|premium|excellence|best|superior/.test(lower),
      isLongTerm: /long-term|decades|generations|sustainable|future/.test(lower),
      isSustainable: /sustainable|environment|green|preservation|conservation/.test(lower),
      hasDetailOrientation: /detail|meticulous|thorough|careful|planning/.test(lower),
    };
  }

  private scoreOpportunity(opportunity: string, context: Record<string, any>): number {
    let score = 0.5;
    const lower = opportunity.toLowerCase();

    if (/quality|premium|excellence/.test(lower)) score += 0.25;
    if (/long-term|generational|decades/.test(lower)) score += 0.2;
    if (/sustainable|environment|green/.test(lower)) score += 0.15;
    if (/location|premier|prime/.test(lower)) score += 0.15;
    if (/detail|meticulous|planning/.test(lower)) score += 0.1;

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
