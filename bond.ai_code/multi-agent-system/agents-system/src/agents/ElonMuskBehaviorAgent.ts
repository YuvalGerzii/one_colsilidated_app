/**
 * Elon Musk Behavior Analysis Agent
 *
 * Analyzes decisions through the lens of Elon Musk's leadership style,
 * thinking patterns, and strategic approaches.
 *
 * Based on research of his leadership at Tesla, SpaceX, X (Twitter), and other ventures.
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

export class ElonMuskBehaviorAgent implements IBehaviorAgent {
  public readonly profile: LeaderBehaviorProfile;

  constructor(
    private pool: Pool,
    private redis: Redis
  ) {
    this.profile = this.buildProfile();
  }

  private buildProfile(): LeaderBehaviorProfile {
    return {
      name: 'Elon Musk',
      title: 'CEO of Tesla, SpaceX, X (Twitter)',
      companies: ['Tesla', 'SpaceX', 'X (Twitter)', 'Neuralink', 'The Boring Company'],
      sectors: [
        BusinessSector.AUTOMOTIVE,
        BusinessSector.AEROSPACE,
        BusinessSector.TECHNOLOGY,
        BusinessSector.ENERGY,
        BusinessSector.SOCIAL_MEDIA,
      ],
      yearsOfExperience: 25,

      leadershipStyles: [
        LeadershipStyle.TRANSFORMATIONAL,
        LeadershipStyle.AUTOCRATIC,
        LeadershipStyle.SITUATIONAL,
        LeadershipStyle.VISIONARY,
      ],

      behavioralTraits: {
        riskTolerance: 0.95,
        innovationDrive: 1.0,
        analyticalThinking: 0.9,
        intuitionReliance: 0.7,
        speedOfDecision: 0.9,
        detailOrientation: 0.85,
        peopleOrientation: 0.4,
        dataOrientation: 0.95,
        longTermFocus: 0.95,
        adaptability: 0.9,
      },

      decisionPatterns: [
        {
          name: 'First Principles Thinking',
          description: 'Break down problems to fundamental truths and reason up from there',
          context: [
            DecisionContext.PRODUCT_DEVELOPMENT,
            DecisionContext.INNOVATION,
            DecisionContext.STRATEGIC_PLANNING,
          ],
          approach: 'Question every assumption, break down to physics and fundamental truths',
          keyQuestions: [
            'What are the fundamental physical constraints?',
            'What assumptions can we eliminate?',
            'What is physically possible vs. what is conventionally done?',
            'Can we build this from scratch more efficiently?',
          ],
          considerations: [
            'Physics and engineering fundamentals',
            'Manufacturing costs at scale',
            'Technical feasibility',
            'Long-term sustainability',
          ],
          redFlags: [
            'Accepting "because that\'s how it\'s always been done"',
            'Incremental improvements instead of revolutionary changes',
            'Following industry standards without questioning',
          ],
          successIndicators: [
            '10x improvement potential',
            'Novel approach that others dismissed',
            'Drastically reduced costs',
          ],
          examples: [
            'SpaceX reusable rockets - questioned why rockets couldn\'t be reused',
            'Tesla battery costs - broke down to material costs and rebuilt supply chain',
          ],
        },
        {
          name: 'Rapid Iteration & High Intensity',
          description: 'Move fast, iterate rapidly, demand high performance',
          context: [
            DecisionContext.PRODUCT_DEVELOPMENT,
            DecisionContext.OPERATIONS,
            DecisionContext.CRISIS_MANAGEMENT,
          ],
          approach: 'Prototype quickly, test, fail fast, iterate, demand excellence',
          keyQuestions: [
            'How can we test this today?',
            'What\'s the fastest path to validation?',
            'Are we moving fast enough?',
            'Is the team operating at maximum intensity?',
          ],
          considerations: [
            'Speed of execution',
            'Testing infrastructure',
            'Team capacity and commitment',
            'Acceptable failure modes',
          ],
          redFlags: [
            'Slow decision-making processes',
            'Excessive meetings',
            'Risk aversion',
            'Comfort with status quo',
          ],
          successIndicators: [
            'Rapid prototyping cycles',
            'Quick pivots based on data',
            'High team productivity',
          ],
          examples: [
            'Twitter/X transformation - rapid changes, high intensity demands',
            'Tesla production ramps - sleeping at factory to solve bottlenecks',
          ],
        },
        {
          name: 'Vertical Integration',
          description: 'Control critical parts of the supply chain and technology stack',
          context: [
            DecisionContext.STRATEGIC_PLANNING,
            DecisionContext.OPERATIONS,
            DecisionContext.INVESTMENT,
          ],
          approach: 'Bring critical components in-house to control quality, cost, and innovation',
          keyQuestions: [
            'Is this component critical to our mission?',
            'Can we do it better and cheaper ourselves?',
            'Does this give us a competitive advantage?',
            'Will this enable faster innovation?',
          ],
          considerations: [
            'Strategic importance',
            'Cost savings potential',
            'Innovation velocity',
            'Quality control',
          ],
          redFlags: [
            'Over-reliance on suppliers',
            'Lack of technical control',
            'Constrained by others\' timelines',
          ],
          successIndicators: [
            'Better margins',
            'Faster iteration',
            'Unique capabilities',
          ],
          examples: [
            'Tesla building battery factories',
            'SpaceX building rocket engines in-house',
          ],
        },
      ],

      negotiationTactics: [
        {
          name: 'Aggressive Deadline Setting',
          description: 'Set ambitious, seemingly impossible deadlines to drive maximum effort',
          whenToUse: 'When rallying teams for critical projects',
          howToApply: 'Set deadline that seems impossible but is technically feasible with maximum effort',
          risks: ['Team burnout', 'Quality issues if pushed too far', 'Talent attrition'],
          effectiveness: 0.8,
          examples: ['Model 3 production ramp', 'Starship development timeline'],
        },
        {
          name: 'Public Commitment',
          description: 'Make bold public statements to create accountability pressure',
          whenToUse: 'When need to galvanize team and stakeholders around ambitious goal',
          howToApply: 'Publicly announce timeline or goal before fully certain it\'s achievable',
          risks: ['Reputation damage if fail', 'Stock price volatility', 'Regulatory scrutiny'],
          effectiveness: 0.75,
          examples: ['Mars colonization timeline', 'Full Self-Driving predictions'],
        },
      ],

      strategicFrameworks: [
        {
          name: 'Mission-Driven Development',
          description: 'Organize all activities around ambitious, world-changing mission',
          principles: [
            'Make humanity multiplanetary (SpaceX)',
            'Accelerate sustainable energy transition (Tesla)',
            'Mission justifies extreme effort and risk',
            'Attract talent passionate about the mission',
          ],
          applicationSteps: [
            'Define audacious mission',
            'Break down into technical challenges',
            'Rally team around mission',
            'Make decisions that advance mission even if risky',
          ],
          keyMetrics: [
            'Progress toward mission milestones',
            'Technical breakthroughs achieved',
            'Cost reductions',
            'Scale achieved',
          ],
          timeHorizon: 'long',
          successCriteria: [
            'Technological leadership',
            'Market transformation',
            'Mission progress',
          ],
        },
      ],

      innovationApproaches: [
        {
          methodology: 'Physics-Based Innovation',
          description: 'Use physics and engineering principles to identify what\'s possible',
          keyPrinciples: [
            'Laws of physics are the only true constraints',
            'Question all conventional wisdom',
            'Optimize for physical efficiency first',
            'Build from first principles',
          ],
          ideationProcess: [
            'Identify the fundamental physics',
            'Calculate theoretical limits',
            'Design to approach theoretical limits',
            'Iterate on implementation',
          ],
          evaluationCriteria: [
            'Does it approach physical limits?',
            'Is it 10x better than alternatives?',
            'Can it scale?',
            'Does it enable the mission?',
          ],
          implementationStrategy: [
            'Build minimum viable prototype',
            'Test aggressively',
            'Iterate rapidly',
            'Scale manufacturing',
          ],
          examples: [
            'Reusable orbital rockets',
            'Electric vehicles with 300+ mile range',
            'Boring Company tunnel costs',
          ],
        },
      ],

      leadershipPrinciples: [
        {
          principle: 'Lead from the Front',
          description: 'Be on the factory floor, in the trenches, solving problems directly',
          application: 'When facing production crises, sleep at the factory and solve bottlenecks personally',
          examples: [
            'Sleeping at Tesla factory during Model 3 production hell',
            'Living at SpaceX during critical development phases',
          ],
          quotes: [
            'If you\'re not working 80 to 100 hours a week, others will beat you',
          ],
        },
        {
          principle: 'Question Authority and Conventional Wisdom',
          description: 'Don\'t accept "that\'s how it\'s done" as a valid answer',
          application: 'Challenge every process, every requirement, every assumption',
          examples: [
            'Challenging aerospace industry on reusability',
            'Challenging auto industry on electric vehicles',
          ],
        },
        {
          principle: 'Optimize for Truth, Not Comfort',
          description: 'Seek truth even when uncomfortable, make decisions based on reality',
          application: 'Fire people who don\'t meet standards, cut products that don\'t work',
          examples: [
            'Twitter layoffs to align with vision',
            'Removing features that don\'t serve users',
          ],
        },
      ],

      communicationStyle: {
        directness: 0.95,
        formality: 0.2,
        emotionalExpression: 0.5,
        typicalPhrases: [
          'This is physically possible',
          'The laws of physics are the only limit',
          'We need to move faster',
          'Question every requirement',
          'Delete, simplify, accelerate',
          'The best part is no part',
        ],
        communicationChannels: ['Twitter/X', 'All-hands meetings', 'Email', 'Factory floor discussions'],
      },

      workStandards: {
        expectationsOfTeam: [
          'Work extremely long hours when necessary',
          'Question everything',
          'Move with urgency',
          'Accept no excuses',
          'Solve problems, don\'t escalate them',
          'Be willing to fail in pursuit of breakthrough',
        ],
        workEthic: 'Extreme intensity - 80-100 hour weeks during critical phases',
        meetingCulture: 'Minimal meetings - walk out if not providing value',
        decisionMakingSpeed: 'Extremely fast - make decisions on the spot when possible',
        failureTolerance: 0.7, // High tolerance if learning and iterating
      },

      famousQuotes: [
        'When something is important enough, you do it even if the odds are not in your favor',
        'I think it\'s possible for ordinary people to choose to be extraordinary',
        'Failure is an option here. If things are not failing, you are not innovating enough',
        'The first step is to establish that something is possible; then probability will occur',
        'If you get up in the morning and think the future is going to be better, it is a bright day',
        'Persistence is very important. You should not give up unless you are forced to give up',
      ],

      mantras: [
        'First principles thinking',
        'Move fast, break things, iterate',
        'Question every requirement',
        'The best part is no part',
        'Delete, simplify, accelerate',
        'Make the impossible possible',
      ],

      notableDecisions: [
        {
          decision: 'Invested personal fortune into Tesla and SpaceX during 2008 crisis',
          context: 'Both companies near bankruptcy, could have lost everything',
          outcome: 'Both companies survived and became industry leaders',
          lessonLearned: 'When mission is critical, take maximum personal risk',
        },
        {
          decision: 'Made Tesla patents open source',
          context: 'Accelerate sustainable energy adoption',
          outcome: 'Established Tesla as industry leader, accelerated EV adoption',
          lessonLearned: 'Sometimes giving away advantages advances the larger mission',
        },
        {
          decision: 'Acquired Twitter and implemented rapid transformation',
          context: 'Believed platform needed fundamental changes',
          outcome: 'Controversial but achieved cost reduction and platform changes',
          lessonLearned: 'Rapid, decisive action can transform organizations',
        },
      ],
    };
  }

  async getAdvice(
    question: string,
    context: DecisionContext,
    additionalInfo?: Record<string, any>
  ): Promise<BusinessAdvice> {
    // Cache key
    const cacheKey = `musk:advice:${this.hashString(question)}:${context}`;
    const cached = await this.redis.get(cacheKey);
    if (cached) return JSON.parse(cached);

    // Analyze through Musk's lens
    const relevantPatterns = this.profile.decisionPatterns.filter(p =>
      p.context.includes(context)
    );

    let advice = '';
    let reasoning = '';
    const actionableSteps: string[] = [];
    const potentialRisks: string[] = [];

    // Apply first principles thinking
    advice = this.generateAdviceByContext(question, context, additionalInfo);
    reasoning = this.generateReasoning(context, relevantPatterns);
    actionableSteps.push(...this.generateActionableSteps(context));
    potentialRisks.push(...this.generateRisks(context));

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

    // Cache for 1 hour
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
    // Evaluate based on Musk's principles
    const characteristics = this.analyzeDecisionCharacteristics(decision);

    const wouldSupport =
      characteristics.isAmbitious &&
      characteristics.hasFirstPrinciples &&
      characteristics.movesFast &&
      !characteristics.isIncremental;

    const modifications: string[] = [];
    if (!characteristics.isAmbitious) {
      modifications.push('Make the goal 10x more ambitious');
    }
    if (!characteristics.hasFirstPrinciples) {
      modifications.push('Apply first principles thinking - break down to fundamental truths');
    }
    if (!characteristics.movesFast) {
      modifications.push('Accelerate timeline - ask "why not this month?"');
    }
    if (characteristics.isIncremental) {
      modifications.push('Think revolutionary, not evolutionary - aim for breakthrough');
    }

    return {
      wouldSupport,
      reasoning: `Musk ${wouldSupport ? 'would support' : 'would not support'} this decision because ${
        wouldSupport
          ? 'it aligns with first principles thinking, is ambitious, and moves fast'
          : 'it lacks the ambition and first-principles thinking required for breakthrough innovation'
      }`,
      modifications,
      confidence: wouldSupport ? 0.85 : 0.7,
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
      strategy: `Apply first principles to break down the problem, question all constraints, and develop a revolutionary solution that achieves 10x improvement`,
      rationale: `Most constraints are assumptions that can be challenged. By breaking down to fundamental physics and rebuilding from there, we can find breakthrough solutions.`,
      steps: [
        'Question every constraint - which are real vs. assumed?',
        'Break down the problem to fundamental truths',
        'Design solution from first principles',
        'Build minimum viable prototype rapidly',
        'Test and iterate with high intensity',
        'Scale manufacturing and operations',
      ],
      timeline: 'Aggressive - 6 months for prototype, 18 months to scale',
      risks: [
        'High intensity may cause team burnout',
        'Challenging assumptions may reveal real constraints',
        'Rapid iteration may have quality issues',
        'Ambitious timeline may not be met',
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
    // Evaluate based on Musk's criteria
    const score = this.scoreOpportunity(opportunity, context);

    if (score >= 0.7) {
      return {
        recommendation: 'pursue',
        score,
        reasoning: 'This opportunity aligns with first principles thinking and has potential for massive impact',
        conditions: [
          'Ensure team is committed to extreme intensity',
          'Validate physics-based feasibility',
          'Confirm this advances a meaningful mission',
        ],
      };
    } else if (score >= 0.4) {
      return {
        recommendation: 'modify',
        score,
        reasoning: 'Opportunity has potential but needs to be more ambitious',
        modifications: [
          'Increase scope and ambition',
          'Apply first principles to find 10x improvement',
          'Accelerate timeline',
          'Ensure mission alignment',
        ],
      };
    } else {
      return {
        recommendation: 'pass',
        score,
        reasoning: 'Opportunity is too incremental and doesn\'t have breakthrough potential',
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
        'Start with first principles. What are you really trying to achieve? Break it down to the fundamental physics and constraints. Then ask yourself: can we do this 10x better? Don\'t accept incremental improvements - seek revolutionary approaches.',

      [DecisionContext.PRODUCT_DEVELOPMENT]:
        'Question every requirement. Why does this part exist? The best part is no part. Delete unnecessary components, simplify what remains, then accelerate. Test rapidly, fail fast, iterate. Move with extreme urgency.',

      [DecisionContext.INNOVATION]:
        'What do the laws of physics allow? Most "impossible" things are just things no one has tried yet. Break down the problem, identify the true constraints (physics, not convention), and rebuild from there. Aim for 10x improvement, not 10%.',

      [DecisionContext.NEGOTIATION]:
        'Know your physics-based bottom line. Don\'t accept conventional terms. Be willing to walk away. Create deadline pressure. Make bold public commitments to drive urgency.',

      [DecisionContext.CRISIS_MANAGEMENT]:
        'Move to the front lines. Sleep at the factory if needed. Identify the core bottleneck and solve it personally. Make rapid decisions. Cut anything not essential. Demand maximum intensity from the team.',

      [DecisionContext.INVESTMENT]:
        'Does this advance a meaningful mission? Can it scale 100x? Is the physics favorable? Can we achieve cost parity or advantage? If yes, take the risk. Bet big on physics-based opportunities.',

      [DecisionContext.HIRING]:
        'Hire for mission alignment and exceptional ability. Can they work at extreme intensity? Do they question assumptions? Will they solve problems rather than escalate? Cultural fit with first principles thinking is critical.',

      [DecisionContext.MARKET_EXPANSION]:
        'Can we do it better than anyone else through vertical integration and first principles? Can we achieve 10x cost advantage? Don\'t expand just to expand - only if it advances the mission and we can dominate.',

      [DecisionContext.PARTNERSHIP]:
        'Does this partnership advance our mission or create dependency? Prefer vertical integration over partnerships for critical components. Partner only when it accelerates us without creating constraints.',

      [DecisionContext.PRICING]:
        'Price based on cost curve at scale, not current costs. Be willing to lose money initially if the physics and scale economics work. Use pricing to accelerate adoption of mission-critical technologies.',

      [DecisionContext.MARKETING]:
        'Let the product speak for itself. Make it so good people can\'t help but talk about it. Use bold public demonstrations. I prefer engineering budget over marketing budget.',

      [DecisionContext.OPERATIONS]:
        'Delete steps, simplify processes, accelerate everything. Eliminate all unnecessary meetings. Remove bureaucracy. Empower people to make decisions quickly. Optimize for velocity.',
    };

    return baseAdvice[context] || baseAdvice[DecisionContext.STRATEGIC_PLANNING];
  }

  private generateReasoning(context: DecisionContext, patterns: any[]): string {
    return `Based on first principles thinking and ${patterns.length} relevant decision patterns from my experience at Tesla, SpaceX, and other ventures. The key is to question all assumptions and rebuild from fundamental truths.`;
  }

  private generateActionableSteps(context: DecisionContext): string[] {
    return [
      'Break down the problem to first principles',
      'Identify and question all assumptions',
      'Calculate what physics allows',
      'Design for 10x improvement, not 10%',
      'Build rapid prototype',
      'Test with maximum intensity',
      'Iterate based on data',
      'Scale aggressively',
    ];
  }

  private generateRisks(context: DecisionContext): string[] {
    return [
      'High intensity approach may cause team burnout',
      'Ambitious timelines may not be met',
      'First principles approach may reveal harder constraints',
      'Revolutionary changes may face regulatory resistance',
      'Rapid iteration may have quality issues initially',
    ];
  }

  private generateAlternatives(context: DecisionContext): string[] {
    return [
      'Take more incremental approach (not recommended)',
      'Partner instead of building in-house (consider carefully)',
      'Extend timeline for lower risk (reduces learning velocity)',
    ];
  }

  private estimateSuccessProbability(
    context: DecisionContext,
    additionalInfo?: Record<string, any>
  ): number {
    // Musk's approaches have high variance - either breakthrough or failure
    return 0.65;
  }

  private selectRelevantQuotes(context: DecisionContext): string[] {
    const contextQuotes: Record<string, string[]> = {
      innovation: ['Failure is an option here. If things are not failing, you are not innovating enough'],
      strategic: ['The first step is to establish that something is possible; then probability will occur'],
      crisis: ['When something is important enough, you do it even if the odds are not in your favor'],
    };

    return contextQuotes.innovation || this.profile.famousQuotes.slice(0, 2);
  }

  private selectRelevantExamples(context: DecisionContext): string[] {
    return this.profile.notableDecisions.slice(0, 2).map(d => `${d.decision}: ${d.outcome}`);
  }

  private estimateTimeframe(context: DecisionContext): string {
    return 'Aggressive timeline - weeks for decisions, months for execution. Always ask "why not sooner?"';
  }

  private identifyResources(context: DecisionContext): string[] {
    return [
      'Team committed to extreme intensity',
      'Rapid prototyping capability',
      'Physics/engineering expertise',
      'Manufacturing capacity for scale',
      'Capital for aggressive investment',
    ];
  }

  private defineKPIs(context: DecisionContext): string[] {
    return [
      'Velocity of iteration',
      'Cost reduction vs. target',
      '10x improvement metrics',
      'Time to prototype',
      'Time to scale',
      'Team productivity',
    ];
  }

  private analyzeDecisionCharacteristics(decision: string): {
    isAmbitious: boolean;
    hasFirstPrinciples: boolean;
    movesFast: boolean;
    isIncremental: boolean;
  } {
    const lower = decision.toLowerCase();
    return {
      isAmbitious: /10x|revolutionary|breakthrough|transform|impossible/.test(lower),
      hasFirstPrinciples: /first principles|fundamental|physics|rethink|question/.test(lower),
      movesFast: /rapid|fast|quick|immediate|urgent|weeks/.test(lower),
      isIncremental: /improve|optimize|enhance|refine|slightly/.test(lower),
    };
  }

  private scoreOpportunity(opportunity: string, context: Record<string, any>): number {
    let score = 0.5;

    const lower = opportunity.toLowerCase();

    // Check for mission alignment
    if (/sustainable|energy|space|future|humanity/.test(lower)) score += 0.2;

    // Check for ambition
    if (/10x|revolutionary|breakthrough|transform/.test(lower)) score += 0.15;

    // Check for physics-based feasibility
    if (/physics|engineering|technical|feasible/.test(lower)) score += 0.1;

    // Check for scale potential
    if (/scale|mass|global|billion/.test(lower)) score += 0.1;

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
