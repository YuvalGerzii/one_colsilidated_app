/**
 * Steve Jobs Behavior Analysis Agent
 *
 * Analyzes decisions through the lens of Steve Jobs' leadership style,
 * thinking patterns, and strategic approaches.
 *
 * Based on research of his leadership at Apple, NeXT, and Pixar.
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

export class SteveJobsBehaviorAgent implements IBehaviorAgent {
  public readonly profile: LeaderBehaviorProfile;

  constructor(
    private pool: Pool,
    private redis: Redis
  ) {
    this.profile = this.buildProfile();
  }

  private buildProfile(): LeaderBehaviorProfile {
    return {
      name: 'Steve Jobs',
      title: 'Co-founder and CEO of Apple',
      companies: ['Apple', 'NeXT', 'Pixar'],
      sectors: [
        BusinessSector.TECHNOLOGY,
        BusinessSector.RETAIL,
        BusinessSector.GENERAL,
      ],
      yearsOfExperience: 35,

      leadershipStyles: [
        LeadershipStyle.VISIONARY,
        LeadershipStyle.TRANSFORMATIONAL,
        LeadershipStyle.AUTOCRATIC,
      ],

      behavioralTraits: {
        riskTolerance: 0.8,
        innovationDrive: 1.0,
        analyticalThinking: 0.75,
        intuitionReliance: 0.85,
        speedOfDecision: 0.8,
        detailOrientation: 0.95,
        peopleOrientation: 0.5,
        dataOrientation: 0.6,
        longTermFocus: 0.9,
        adaptability: 0.7,
      },

      decisionPatterns: [
        {
          name: 'User Experience First',
          description: 'Obsessive focus on simplicity, design, and user experience above all else',
          context: [
            DecisionContext.PRODUCT_DEVELOPMENT,
            DecisionContext.STRATEGIC_PLANNING,
            DecisionContext.INNOVATION,
          ],
          approach: 'Start with the user experience and work backward to the technology',
          keyQuestions: [
            'How does this make the user feel?',
            'Is this simple enough?',
            'Does this create magic?',
            'Would I want to use this?',
          ],
          considerations: [
            'Emotional connection with product',
            'Simplicity and elegance',
            'Integration of hardware and software',
            'Attention to every detail',
          ],
          redFlags: [
            'Complexity for complexity\'s sake',
            'Following what competitors do',
            'Compromising on design',
            'Adding features users don\'t need',
          ],
          successIndicators: [
            'Users develop emotional connection',
            'Product feels magical',
            'Design is iconic',
            'Simplicity achieved',
          ],
          examples: [
            'iPhone - eliminated keyboard for pure touchscreen',
            'iPod - 1000 songs in your pocket',
            'Mac - computer as appliance',
          ],
        },
        {
          name: 'Making Unexpected Connections',
          description: 'Connect seemingly unrelated fields to create breakthrough innovations',
          context: [
            DecisionContext.INNOVATION,
            DecisionContext.PRODUCT_DEVELOPMENT,
            DecisionContext.STRATEGIC_PLANNING,
          ],
          approach: 'Draw inspiration from art, humanities, and diverse fields',
          keyQuestions: [
            'What can we learn from other industries?',
            'How does art inform technology?',
            'What unexpected combinations create value?',
          ],
          considerations: [
            'Intersection of technology and liberal arts',
            'Aesthetics and functionality',
            'Cultural trends',
            'Historical precedents',
          ],
          redFlags: [
            'Narrow technical focus',
            'Ignoring design and aesthetics',
            'Pure engineering mindset',
          ],
          successIndicators: [
            'Novel combinations',
            'Beautiful products',
            'Cultural resonance',
          ],
          examples: [
            'Calligraphy class influenced Mac typography',
            'Zen Buddhism influenced product simplicity',
            'Bauhaus design principles in Apple products',
          ],
        },
        {
          name: 'Simplification - The Best Part is No Part',
          description: 'Relentlessly eliminate until only the essential remains',
          context: [
            DecisionContext.PRODUCT_DEVELOPMENT,
            DecisionContext.OPERATIONS,
            DecisionContext.STRATEGIC_PLANNING,
          ],
          approach: 'Remove features, buttons, options until reaching perfect simplicity',
          keyQuestions: [
            'What can we remove?',
            'Is this absolutely necessary?',
            'Can we make this simpler?',
            'What\'s the essence of this product?',
          ],
          considerations: [
            'Core functionality vs. feature bloat',
            'User confusion from complexity',
            'Manufacturing simplification',
            'Support and maintenance costs',
          ],
          redFlags: [
            'Adding features to match competitors',
            'Complexity creep',
            'Multiple ways to do the same thing',
            'Cluttered interfaces',
          ],
          successIndicators: [
            'Intuitive without manual',
            'Fewer parts, lower costs',
            'Elegant solutions',
            'Clear value proposition',
          ],
          examples: [
            'iPhone - one button',
            'iPod - simple scroll wheel',
            'Mac - no startup disk selection needed',
          ],
        },
        {
          name: 'Go-to-Market Before Product',
          description: 'Think about positioning, story, and market strategy before building',
          context: [
            DecisionContext.PRODUCT_DEVELOPMENT,
            DecisionContext.MARKETING,
            DecisionContext.STRATEGIC_PLANNING,
          ],
          approach: 'Define the narrative and market positioning early, let it guide development',
          keyQuestions: [
            'What\'s the story we\'re telling?',
            'How do we position this?',
            'What\'s the one-sentence description?',
            'How do we create desire?',
          ],
          considerations: [
            'Market positioning',
            'Brand narrative',
            'Competitive differentiation',
            'Customer perception',
          ],
          redFlags: [
            'Building without clear positioning',
            'Unclear value proposition',
            'Confusing messaging',
          ],
          successIndicators: [
            'Clear, compelling narrative',
            'Strong differentiation',
            'Creates desire before launch',
          ],
          examples: [
            'iPod - "1000 songs in your pocket"',
            'iPhone - "An iPod, a phone, an internet communicator"',
            'Mac - "The computer for the rest of us"',
          ],
        },
      ],

      negotiationTactics: [
        {
          name: 'Power of Saying No',
          description: 'Say no to almost everything to maintain focus on what matters',
          whenToUse: 'When facing feature requests, partnerships, or opportunities that distract',
          howToApply: 'Be ruthless about focus - say no to good ideas to focus on great ones',
          risks: ['Missing opportunities', 'Alienating partners', 'Market gaps'],
          effectiveness: 0.9,
          examples: [
            'Killed multiple product lines when returning to Apple',
            'Said no to licensing Mac OS widely',
            'Rejected phone with keyboard',
          ],
        },
        {
          name: 'Reality Distortion Field',
          description: 'Convince team that impossible deadlines and goals are achievable',
          whenToUse: 'When need to inspire team to achieve extraordinary results',
          howToApply: 'Set seemingly impossible goals with absolute conviction they\'re possible',
          risks: ['Team burnout', 'Credibility if consistently missed', 'Quality issues'],
          effectiveness: 0.75,
          examples: [
            'Original Mac timeline',
            'iPhone development schedule',
            'Retail store launch pace',
          ],
        },
        {
          name: 'Perfectionist Demands',
          description: 'Demand perfection in every detail, no matter how small',
          whenToUse: 'Throughout product development and operations',
          howToApply: 'Scrutinize every detail, reject anything less than perfect',
          risks: ['Delays', 'Team frustration', 'Increased costs'],
          effectiveness: 0.85,
          examples: [
            'iPhone screen - rejected multiple versions',
            'Store design - obsessed over every material',
            'Product packaging - art form',
          ],
        },
      ],

      strategicFrameworks: [
        {
          name: 'Holistic Innovation',
          description: 'Integrate product, business model, retail, advertising into coherent whole',
          principles: [
            'Control entire customer experience',
            'Hardware and software integration',
            'Retail as extension of product',
            'Marketing tells the story',
            'Ecosystem over individual products',
          ],
          applicationSteps: [
            'Design product with integration in mind',
            'Create business model that enhances experience',
            'Build retail that showcases products properly',
            'Craft advertising that tells emotional story',
            'Ensure all parts work together seamlessly',
          ],
          keyMetrics: [
            'Customer satisfaction',
            'Brand loyalty',
            'Ecosystem lock-in',
            'Retail experience metrics',
            'Product margins',
          ],
          timeHorizon: 'long',
          successCriteria: [
            'Seamless customer experience',
            'Strong ecosystem',
            'Premium pricing power',
            'Market leadership',
          ],
        },
        {
          name: 'Iconoclastic Thinking',
          description: 'Challenge conventional wisdom and industry norms',
          principles: [
            'Question everything the industry accepts',
            'Be willing to be different',
            'Think different',
            'Create new categories',
          ],
          applicationSteps: [
            'Identify industry assumptions',
            'Question each one',
            'Imagine ideal solution without constraints',
            'Build toward that vision',
          ],
          keyMetrics: [
            'Differentiation from competitors',
            'Category creation',
            'Industry disruption',
          ],
          timeHorizon: 'long',
          successCriteria: [
            'Changed industry paradigm',
            'Created new category',
            'Competitors following',
          ],
        },
      ],

      innovationApproaches: [
        {
          methodology: 'Technology Meets Liberal Arts',
          description: 'Combine technology with humanities to create products people love',
          keyPrinciples: [
            'Technology alone is not enough',
            'Design is how it works, not just how it looks',
            'Connect with customers emotionally',
            'Make technology accessible and delightful',
          ],
          ideationProcess: [
            'Start with customer need and desire',
            'Consider emotional and aesthetic dimensions',
            'Apply technology to serve human needs',
            'Iterate until product is magical',
          ],
          evaluationCriteria: [
            'Does it create joy?',
            'Is it simple to use?',
            'Is it beautiful?',
            'Does it integrate seamlessly?',
          ],
          implementationStrategy: [
            'Form small, elite teams',
            'Iterate obsessively',
            'Maintain secrecy until launch',
            'Control entire experience',
          ],
          examples: [
            'iPod - technology meets music',
            'iPhone - computer meets phone meets design',
            'iPad - technology meets publishing',
          ],
        },
      ],

      leadershipPrinciples: [
        {
          principle: 'Focus and Simplicity',
          description: 'Deciding what not to do is as important as deciding what to do',
          application: 'Cut product lines, features, and initiatives ruthlessly to maintain focus',
          examples: [
            'Reduced Apple product line from dozens to four quadrants',
            'Said no to many good ideas',
          ],
          quotes: [
            'Focus is about saying no',
            'Simple can be harder than complex',
          ],
        },
        {
          principle: 'Insane Attention to Detail',
          description: 'Care about every detail, even ones customers never see',
          application: 'Review every aspect of product, from internal components to packaging',
          examples: [
            'Insisted on perfect internal cable routing',
            'Obsessed over box opening experience',
            'Scrutinized every pixel',
          ],
          quotes: [
            'Details matter, it\'s worth waiting to get it right',
          ],
        },
        {
          principle: 'Integration Over Openness',
          description: 'Control the full stack to ensure perfect user experience',
          application: 'Build integrated hardware and software, control ecosystem',
          examples: [
            'Mac OS only on Apple hardware',
            'iPhone iOS integration',
            'Apple ecosystem',
          ],
        },
      ],

      communicationStyle: {
        directness: 0.95,
        formality: 0.3,
        emotionalExpression: 0.7,
        typicalPhrases: [
          'This is shit',
          'Insanely great',
          'One more thing...',
          'It just works',
          'Think different',
          'Make a dent in the universe',
        ],
        communicationChannels: ['Product keynotes', 'One-on-ones', 'Design reviews', 'Public presentations'],
      },

      workStandards: {
        expectationsOfTeam: [
          'A players only',
          'Perfectionism in every detail',
          'Total commitment',
          'Willingness to be challenged',
          'No compromises on quality',
        ],
        workEthic: 'Intense focus on product excellence, long hours, high standards',
        meetingCulture: 'Small teams, focused discussions, design reviews, frank feedback',
        decisionMakingSpeed: 'Fast on vision, slow on details until perfect',
        failureTolerance: 0.4,
      },

      famousQuotes: [
        'Stay hungry, stay foolish',
        'People don\'t know what they want until you show them',
        'Design is not just what it looks like and feels like. Design is how it works',
        'Innovation distinguishes between a leader and a follower',
        'Quality is more important than quantity. One home run is better than two doubles',
        'The only way to do great work is to love what you do',
        'Simple can be harder than complex: You have to work hard to get your thinking clean to make it simple',
      ],

      mantras: [
        'Think different',
        'The best part is no part',
        'Insanely great',
        'Stay hungry, stay foolish',
        'Focus and simplicity',
        'It just works',
      ],

      notableDecisions: [
        {
          decision: 'Eliminated most of Apple product line in 1997',
          context: 'Apple was bleeding money with too many products',
          outcome: 'Return to profitability, renewed focus, paved way for iMac',
          lessonLearned: 'Focus and simplicity can save a company',
        },
        {
          decision: 'Built Apple Retail Stores',
          context: 'Conventional wisdom said computer companies shouldn\'t do retail',
          outcome: 'Most successful retail per square foot in the world',
          lessonLearned: 'Control customer experience end-to-end',
        },
        {
          decision: 'iPhone without physical keyboard',
          context: 'All smartphones had keyboards, considered essential',
          outcome: 'Revolutionized mobile computing, dominant design',
          lessonLearned: 'Trust your vision even when everyone disagrees',
        },
        {
          decision: 'Acquired NeXT, returned to Apple',
          context: 'Apple was failing, NeXT had superior OS',
          outcome: 'NeXT OS became Mac OS X, Jobs led Apple renaissance',
          lessonLearned: 'Sometimes you need to go back to move forward',
        },
      ],
    };
  }

  async getAdvice(
    question: string,
    context: DecisionContext,
    additionalInfo?: Record<string, any>
  ): Promise<BusinessAdvice> {
    const cacheKey = `jobs:advice:${this.hashString(question)}:${context}`;
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
      characteristics.isSimple &&
      characteristics.isDesignFocused &&
      characteristics.hasUserFocus &&
      !characteristics.isCompromise;

    const modifications: string[] = [];
    if (!characteristics.isSimple) {
      modifications.push('Simplify ruthlessly - remove everything non-essential');
    }
    if (!characteristics.isDesignFocused) {
      modifications.push('Elevate design - make it beautiful and intuitive');
    }
    if (!characteristics.hasUserFocus) {
      modifications.push('Start with user experience, work backward to technology');
    }
    if (characteristics.isCompromise) {
      modifications.push('Don\'t compromise - find a way to achieve the ideal');
    }

    return {
      wouldSupport,
      reasoning: `Jobs ${wouldSupport ? 'would support' : 'would not support'} this decision because ${
        wouldSupport
          ? 'it emphasizes simplicity, design excellence, and user experience'
          : 'it lacks the focus on simplicity and design that creates insanely great products'
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
      strategy: `Focus on creating an insanely great product with perfect user experience. Say no to everything that doesn't serve this goal. Design the complete customer journey, from product to retail to marketing.`,
      rationale: `The only way to win is to create products people love. This requires focus, simplicity, and attention to every detail. Don't settle for good - make it insanely great.`,
      steps: [
        'Define the ideal user experience - start here, not with technology',
        'Eliminate all non-essential features and complexity',
        'Design for simplicity and beauty',
        'Iterate until every detail is perfect',
        'Control the entire customer experience',
        'Tell a compelling story',
        'Launch with excellence',
      ],
      timeline: 'Take the time to get it right - months to years for perfect execution',
      risks: [
        'Perfectionism may delay launch',
        'High standards may frustrate team',
        'Focus may miss adjacent opportunities',
        'Integration strategy requires significant investment',
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
        reasoning: 'This opportunity aligns with creating insanely great products that customers will love',
        conditions: [
          'Must maintain complete control over user experience',
          'Design excellence is non-negotiable',
          'Say no to feature creep',
          'Take time to perfect every detail',
        ],
      };
    } else if (score >= 0.5) {
      return {
        recommendation: 'modify',
        score,
        reasoning: 'Opportunity has potential but needs refinement for excellence',
        modifications: [
          'Simplify to the essence',
          'Elevate design to create emotional connection',
          'Focus on fewer things done better',
          'Ensure we can control the full experience',
        ],
      };
    } else {
      return {
        recommendation: 'pass',
        score,
        reasoning: 'This doesn\'t align with creating products people will love - focus on what matters',
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
        'Focus is about saying no. Cut everything that doesn\'t contribute to creating insanely great products. Decide what NOT to do. Think holistically - product, retail, marketing must work as one.',

      [DecisionContext.PRODUCT_DEVELOPMENT]:
        'Start with the customer experience and work backward to the technology. Make it simple, beautiful, and magical. The best part is no part. Design is how it works, not just how it looks. Don\'t ship until it\'s insanely great.',

      [DecisionContext.INNOVATION]:
        'Make unexpected connections. Technology alone is not enough - marry it with liberal arts. Look for what customers will love before they know they want it. Don\'t ask customers what they want - show them what\'s possible.',

      [DecisionContext.NEGOTIATION]:
        'Say no to almost everything. Focus is power. Don\'t compromise on what matters. If it doesn\'t serve the vision of creating the best product, decline.',

      [DecisionContext.CRISIS_MANAGEMENT]:
        'Cut to the core. What matters most? Focus all energy there. Eliminate distractions ruthlessly. Get back to making insanely great products.',

      [DecisionContext.INVESTMENT]:
        'Does this help us create products people will love? Can we control the experience? Will this let us make something insanely great? If not, say no.',

      [DecisionContext.HIRING]:
        'Only A players. They want to work with other A players. B and C players hire worse. Insist on excellence. Can they handle brutal honesty? Will they make the product better?',

      [DecisionContext.MARKET_EXPANSION]:
        'Only expand if we can deliver the same insanely great experience. Don\'t dilute the brand. Better to say no than to do it poorly. Control the customer experience completely.',

      [DecisionContext.PARTNERSHIP]:
        'Partnerships often mean compromise. Can we do it ourselves better? Do we control the experience? If it requires compromising our vision, probably no.',

      [DecisionContext.PRICING]:
        'Charge what the product is worth. Premium products command premium prices. Don\'t compete on price - compete on insanely great products. Price for the value created.',

      [DecisionContext.MARKETING]:
        'Tell a simple, emotional story. Show, don\'t tell. The product is the hero. Create desire. One clear message. Make people feel something. Less is more.',

      [DecisionContext.OPERATIONS]:
        'Simplify operations to enable perfect products. Remove bureaucracy. Small teams. Fast decisions. Everything serves product excellence.',
    };

    return baseAdvice[context] || baseAdvice[DecisionContext.STRATEGIC_PLANNING];
  }

  private generateReasoning(context: DecisionContext, patterns: any[]): string {
    return `Based on the principles of focus, simplicity, and design excellence that drove Apple's success. Drawing from ${patterns.length} key decision patterns around user experience and holistic innovation.`;
  }

  private generateActionableSteps(context: DecisionContext): string[] {
    return [
      'Define the ideal user experience',
      'Simplify ruthlessly - remove all non-essential elements',
      'Design for beauty and intuition',
      'Perfect every detail',
      'Ensure complete integration',
      'Craft the narrative',
      'Don\'t ship until it\'s insanely great',
    ];
  }

  private generateRisks(context: DecisionContext): string[] {
    return [
      'Perfectionism may cause delays',
      'High standards may create team friction',
      'Saying no may miss some opportunities',
      'Control strategy requires significant investment',
      'Design focus may increase costs',
    ];
  }

  private generateAlternatives(context: DecisionContext): string[] {
    return [
      'Ship faster with less polish (not recommended)',
      'Add more features to match competitors (dilutes focus)',
      'Partner instead of controlling experience (compromises quality)',
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
      product: ['Design is not just what it looks like. Design is how it works'],
      innovation: ['People don\'t know what they want until you show them'],
      focus: ['Focus is about saying no'],
    };

    return contextQuotes.product || this.profile.famousQuotes.slice(0, 2);
  }

  private selectRelevantExamples(context: DecisionContext): string[] {
    return this.profile.notableDecisions.slice(0, 2).map(d => `${d.decision}: ${d.outcome}`);
  }

  private estimateTimeframe(context: DecisionContext): string {
    return 'Take the time needed for excellence - don\'t rush perfection';
  }

  private identifyResources(context: DecisionContext): string[] {
    return [
      'A player talent only',
      'Design and engineering excellence',
      'Complete control over experience',
      'Time to perfect details',
      'Resources for integration',
    ];
  }

  private defineKPIs(context: DecisionContext): string[] {
    return [
      'Customer satisfaction and delight',
      'Design awards and recognition',
      'Product simplicity metrics',
      'Brand loyalty',
      'Premium pricing power',
      'Market leadership position',
    ];
  }

  private analyzeDecisionCharacteristics(decision: string): {
    isSimple: boolean;
    isDesignFocused: boolean;
    hasUserFocus: boolean;
    isCompromise: boolean;
  } {
    const lower = decision.toLowerCase();
    return {
      isSimple: /simple|streamline|focus|essential|minimal/.test(lower),
      isDesignFocused: /design|beautiful|elegant|intuitive|experience/.test(lower),
      hasUserFocus: /user|customer|people|experience|delight/.test(lower),
      isCompromise: /compromise|settle|good enough|acceptable/.test(lower),
    };
  }

  private scoreOpportunity(opportunity: string, context: Record<string, any>): number {
    let score = 0.5;
    const lower = opportunity.toLowerCase();

    if (/design|beautiful|elegant|user experience/.test(lower)) score += 0.2;
    if (/simple|focus|essential/.test(lower)) score += 0.15;
    if (/innovative|creative|breakthrough/.test(lower)) score += 0.1;
    if (/control|integrate|ecosystem/.test(lower)) score += 0.1;
    if (/compromise|complex|feature/.test(lower)) score -= 0.2;

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
