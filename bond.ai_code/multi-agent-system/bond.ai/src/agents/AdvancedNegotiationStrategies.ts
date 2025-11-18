/**
 * Advanced Multi-Agent Negotiation Strategies
 *
 * Implements sophisticated negotiation strategies based on 2025 best practices:
 * - Five dimensions: Actors, Types, Structures, Strategies, Coordination
 * - Communication paradigms: memory-based, report-based, role-based, graph-based
 * - Dynamic adaptation using reinforcement learning and game theory
 * - "Nice" strategies for better outcomes
 * - Risk mitigation through multi-model coordination
 */

import { UserRepresentativeAgent, AgentConversation, NegotiationPoint, ProposedTerms } from './types';

/**
 * Communication Paradigms for Agent Coordination
 */
export enum CommunicationParadigm {
  MEMORY_BASED = 'memory_based',       // Shared knowledge repository
  REPORT_BASED = 'report_based',       // Status updates and reports
  ASSEMBLY_LINE = 'assembly_line',     // Sequential processing
  ROLE_BASED = 'role_based',           // Professional role assignments
  GRAPH_BASED = 'graph_based'          // Graph-structured workflows
}

/**
 * Negotiation Architecture Structures
 */
export enum NegotiationStructure {
  PEER_TO_PEER = 'peer_to_peer',         // Direct 1-on-1 negotiation
  CENTRALIZED = 'centralized',           // Central mediator
  DISTRIBUTED = 'distributed',           // Multiple parallel negotiations
  HIERARCHICAL = 'hierarchical'          // Tiered decision making
}

/**
 * Collaboration Types
 */
export enum CollaborationType {
  COOPERATION = 'cooperation',           // Win-win collaboration
  COMPETITION = 'competition',           // Win-lose competition
  COOPETITION = 'coopetition'           // Mixed cooperation and competition
}

/**
 * Advanced Negotiation Strategy
 */
export interface AdvancedStrategy {
  name: string;
  description: string;
  paradigm: CommunicationParadigm;
  structure: NegotiationStructure;
  collaborationType: CollaborationType;

  // Strategy parameters
  nicenessFactor: number;              // 0-1: How "nice" the strategy is
  adaptabilityFactor: number;          // 0-1: How much it adapts to opponent
  riskTolerance: number;               // 0-1: Risk acceptance level

  // Game theory parameters
  cooperationThreshold: number;        // When to cooperate vs compete
  reciprocityFactor: number;          // How much to mirror opponent

  // Learning parameters
  learningRate: number;                // How fast to adapt
  explorationRate: number;             // Exploration vs exploitation
}

/**
 * Predefined Advanced Strategies
 */
export class NegotiationStrategies {
  /**
   * Tit-for-Tat with Forgiveness (Nice strategy)
   * Highly effective based on game theory research
   */
  static TIT_FOR_TAT_FORGIVING: AdvancedStrategy = {
    name: 'Tit-for-Tat with Forgiveness',
    description: 'Cooperates first, then mirrors opponent but occasionally forgives defections',
    paradigm: CommunicationParadigm.MEMORY_BASED,
    structure: NegotiationStructure.PEER_TO_PEER,
    collaborationType: CollaborationType.COOPERATION,
    nicenessFactor: 0.85,
    adaptabilityFactor: 0.9,
    riskTolerance: 0.6,
    cooperationThreshold: 0.7,
    reciprocityFactor: 0.8,
    learningRate: 0.3,
    explorationRate: 0.2
  };

  /**
   * Generous Tit-for-Tat (Very nice strategy)
   * Occasionally cooperates even after defection
   */
  static GENEROUS_TIT_FOR_TAT: AdvancedStrategy = {
    name: 'Generous Tit-for-Tat',
    description: 'Like Tit-for-Tat but more forgiving, occasionally cooperates after defection',
    paradigm: CommunicationParadigm.MEMORY_BASED,
    structure: NegotiationStructure.PEER_TO_PEER,
    collaborationType: CollaborationType.COOPERATION,
    nicenessFactor: 0.95,
    adaptabilityFactor: 0.85,
    riskTolerance: 0.7,
    cooperationThreshold: 0.8,
    reciprocityFactor: 0.7,
    learningRate: 0.25,
    explorationRate: 0.15
  };

  /**
   * Pavlov Strategy (Win-Stay, Lose-Shift)
   * Repeats if successful, changes if not
   */
  static PAVLOV: AdvancedStrategy = {
    name: 'Pavlov',
    description: 'Win-Stay, Lose-Shift: Repeats successful actions, changes after failure',
    paradigm: CommunicationParadigm.REPORT_BASED,
    structure: NegotiationStructure.PEER_TO_PEER,
    collaborationType: CollaborationType.COOPETITION,
    nicenessFactor: 0.7,
    adaptabilityFactor: 0.95,
    riskTolerance: 0.5,
    cooperationThreshold: 0.6,
    reciprocityFactor: 0.6,
    learningRate: 0.4,
    explorationRate: 0.3
  };

  /**
   * Gradual Strategy
   * Increases retaliation gradually, quick to forgive
   */
  static GRADUAL: AdvancedStrategy = {
    name: 'Gradual',
    description: 'Escalates retaliation gradually but is quick to forgive and cooperate',
    paradigm: CommunicationParadigm.MEMORY_BASED,
    structure: NegotiationStructure.PEER_TO_PEER,
    collaborationType: CollaborationType.COOPERATION,
    nicenessFactor: 0.8,
    adaptabilityFactor: 0.9,
    riskTolerance: 0.5,
    cooperationThreshold: 0.75,
    reciprocityFactor: 0.85,
    learningRate: 0.35,
    explorationRate: 0.2
  };

  /**
   * Adaptive Strategy with Reinforcement Learning
   * Uses Q-learning to optimize strategy over time
   */
  static ADAPTIVE_RL: AdvancedStrategy = {
    name: 'Adaptive RL',
    description: 'Uses reinforcement learning to adapt strategy based on outcomes',
    paradigm: CommunicationParadigm.GRAPH_BASED,
    structure: NegotiationStructure.DISTRIBUTED,
    collaborationType: CollaborationType.COOPETITION,
    nicenessFactor: 0.75,
    adaptabilityFactor: 0.98,
    riskTolerance: 0.6,
    cooperationThreshold: 0.65,
    reciprocityFactor: 0.75,
    learningRate: 0.5,
    explorationRate: 0.4
  };

  /**
   * Cooperative Multi-Agent Strategy
   * Optimized for multi-party negotiations
   */
  static COOPERATIVE_MULTI_AGENT: AdvancedStrategy = {
    name: 'Cooperative Multi-Agent',
    description: 'Designed for multi-party negotiations with coalition building',
    paradigm: CommunicationParadigm.ROLE_BASED,
    structure: NegotiationStructure.DISTRIBUTED,
    collaborationType: CollaborationType.COOPERATION,
    nicenessFactor: 0.9,
    adaptabilityFactor: 0.85,
    riskTolerance: 0.55,
    cooperationThreshold: 0.85,
    reciprocityFactor: 0.8,
    learningRate: 0.3,
    explorationRate: 0.25
  };

  /**
   * Competitive Bargaining Strategy
   * For competitive negotiations with stakes
   */
  static COMPETITIVE_BARGAINING: AdvancedStrategy = {
    name: 'Competitive Bargaining',
    description: 'Competitive approach for high-stakes negotiations',
    paradigm: CommunicationParadigm.REPORT_BASED,
    structure: NegotiationStructure.CENTRALIZED,
    collaborationType: CollaborationType.COMPETITION,
    nicenessFactor: 0.4,
    adaptabilityFactor: 0.7,
    riskTolerance: 0.8,
    cooperationThreshold: 0.4,
    reciprocityFactor: 0.5,
    learningRate: 0.35,
    explorationRate: 0.3
  };

  /**
   * Get all available strategies
   */
  static getAllStrategies(): AdvancedStrategy[] {
    return [
      this.TIT_FOR_TAT_FORGIVING,
      this.GENEROUS_TIT_FOR_TAT,
      this.PAVLOV,
      this.GRADUAL,
      this.ADAPTIVE_RL,
      this.COOPERATIVE_MULTI_AGENT,
      this.COMPETITIVE_BARGAINING
    ];
  }

  /**
   * Select optimal strategy based on context
   */
  static selectOptimalStrategy(
    opponentHistory: AgentConversation[],
    matchType: string,
    trustLevel: number
  ): AdvancedStrategy {
    // High trust + cooperation domain → Nice strategies
    if (trustLevel > 0.7 && ['mentor-mentee', 'collaboration', 'partnership'].includes(matchType)) {
      return this.GENEROUS_TIT_FOR_TAT;
    }

    // Investment/competitive domain → Adaptive or competitive
    if (['investor-startup', 'supplier-buyer'].includes(matchType)) {
      return trustLevel > 0.6 ? this.ADAPTIVE_RL : this.COMPETITIVE_BARGAINING;
    }

    // Multi-party potential → Cooperative multi-agent
    if (matchType === 'collaboration' || matchType === 'partnership') {
      return this.COOPERATIVE_MULTI_AGENT;
    }

    // Uncertain opponent → Gradual escalation
    if (opponentHistory.length < 3) {
      return this.GRADUAL;
    }

    // Analyze opponent's cooperativeness
    const cooperationRate = this.analyzeCooperation(opponentHistory);

    if (cooperationRate > 0.7) {
      return this.TIT_FOR_TAT_FORGIVING;
    } else if (cooperationRate > 0.4) {
      return this.PAVLOV;
    } else {
      return this.ADAPTIVE_RL;
    }
  }

  /**
   * Analyze opponent's cooperation rate from history
   */
  private static analyzeCooperation(history: AgentConversation[]): number {
    if (history.length === 0) return 0.5;

    let cooperativeActions = 0;

    history.forEach(conversation => {
      // Analyze conversation for cooperative signals
      const message = conversation.message.toLowerCase();

      if (message.includes('agree') || message.includes('accept') ||
          message.includes('collaborate') || message.includes('mutual')) {
        cooperativeActions++;
      }
    });

    return cooperativeActions / history.length;
  }
}

/**
 * Strategy Executor - Implements the selected strategy
 */
export class StrategyExecutor {
  private strategy: AdvancedStrategy;
  private conversationHistory: AgentConversation[] = [];
  private qValues: Map<string, number> = new Map(); // For RL strategies

  constructor(strategy: AdvancedStrategy) {
    this.strategy = strategy;
  }

  /**
   * Decide next action based on strategy
   */
  decideAction(
    currentProposal: ProposedTerms,
    opponentLastAction: 'cooperate' | 'defect' | null,
    round: number
  ): 'accept' | 'counter' | 'reject' {
    const { name, nicenessFactor, adaptabilityFactor, cooperationThreshold } = this.strategy;

    // First round - nice strategies cooperate
    if (round === 1) {
      return nicenessFactor > 0.6 ? 'accept' : 'counter';
    }

    // Reinforcement Learning strategies use Q-values
    if (name === 'Adaptive RL') {
      return this.rlDecision(currentProposal);
    }

    // Tit-for-Tat strategies
    if (name.includes('Tit-for-Tat')) {
      if (opponentLastAction === 'cooperate') {
        return 'accept';
      } else if (opponentLastAction === 'defect') {
        // Forgiveness factor
        const forgive = Math.random() < (nicenessFactor - 0.5) * 2;
        return forgive ? 'counter' : 'reject';
      }
    }

    // Pavlov (Win-Stay, Lose-Shift)
    if (name === 'Pavlov') {
      const lastOutcome = this.getLastOutcome();
      if (lastOutcome === 'win') {
        return 'accept'; // Stay with winning strategy
      } else {
        return 'counter'; // Shift strategy
      }
    }

    // Gradual strategy
    if (name === 'Gradual') {
      const defectionCount = this.countRecentDefections(3);
      if (defectionCount === 0) {
        return 'accept';
      } else if (defectionCount <= 2) {
        return 'counter';
      } else {
        return 'reject';
      }
    }

    // Default: evaluate proposal score
    const proposalScore = this.evaluateProposal(currentProposal);

    if (proposalScore >= cooperationThreshold) {
      return 'accept';
    } else if (proposalScore >= 0.4) {
      return 'counter';
    } else {
      return 'reject';
    }
  }

  /**
   * Reinforcement Learning decision using Q-values
   */
  private rlDecision(proposal: ProposedTerms): 'accept' | 'counter' | 'reject' {
    const state = this.getCurrentState(proposal);
    const actions: ('accept' | 'counter' | 'reject')[] = ['accept', 'counter', 'reject'];

    // Epsilon-greedy exploration
    if (Math.random() < this.strategy.explorationRate) {
      return actions[Math.floor(Math.random() * actions.length)];
    }

    // Exploit: choose action with highest Q-value
    let bestAction: 'accept' | 'counter' | 'reject' = 'counter';
    let bestValue = -Infinity;

    actions.forEach(action => {
      const key = `${state}-${action}`;
      const qValue = this.qValues.get(key) || 0;

      if (qValue > bestValue) {
        bestValue = qValue;
        bestAction = action;
      }
    });

    return bestAction;
  }

  /**
   * Update Q-values after action (for RL strategies)
   */
  updateQValue(
    state: string,
    action: string,
    reward: number,
    nextState: string
  ): void {
    const currentQ = this.qValues.get(`${state}-${action}`) || 0;

    // Get max Q-value for next state
    const nextActions = ['accept', 'counter', 'reject'];
    const maxNextQ = Math.max(
      ...nextActions.map(a => this.qValues.get(`${nextState}-${a}`) || 0)
    );

    // Q-learning update rule
    const newQ = currentQ + this.strategy.learningRate * (
      reward + 0.9 * maxNextQ - currentQ
    );

    this.qValues.set(`${state}-${action}`, newQ);
  }

  /**
   * Get current state representation
   */
  private getCurrentState(proposal: ProposedTerms): string {
    const round = this.conversationHistory.length;
    const proposalScore = this.evaluateProposal(proposal);
    const scoreCategory = proposalScore > 0.7 ? 'high' : proposalScore > 0.4 ? 'medium' : 'low';

    return `r${round}-${scoreCategory}`;
  }

  /**
   * Evaluate proposal quality
   */
  private evaluateProposal(proposal: ProposedTerms): number {
    // Simple heuristic: ratio of what we get vs what we give
    const givingValue = proposal.whatTheyGive?.length || 0;
    const gettingValue = proposal.whatTheyGet?.length || 0;

    if (gettingValue === 0) return 0;

    return Math.min(givingValue / (gettingValue + givingValue), 1);
  }

  /**
   * Get outcome of last action
   */
  private getLastOutcome(): 'win' | 'lose' | 'neutral' {
    if (this.conversationHistory.length === 0) return 'neutral';

    const lastConv = this.conversationHistory[this.conversationHistory.length - 1];

    // Check if last proposal was accepted or beneficial
    if (lastConv.message.toLowerCase().includes('accept') ||
        lastConv.message.toLowerCase().includes('agree')) {
      return 'win';
    } else if (lastConv.message.toLowerCase().includes('reject')) {
      return 'lose';
    }

    return 'neutral';
  }

  /**
   * Count recent defections in conversation history
   */
  private countRecentDefections(lookback: number): number {
    const recent = this.conversationHistory.slice(-lookback);

    return recent.filter(conv =>
      conv.message.toLowerCase().includes('reject') ||
      conv.message.toLowerCase().includes('cannot accept')
    ).length;
  }

  /**
   * Add conversation to history
   */
  addToHistory(conversation: AgentConversation): void {
    this.conversationHistory.push(conversation);
  }

  /**
   * Get strategy info
   */
  getStrategy(): AdvancedStrategy {
    return this.strategy;
  }

  /**
   * Get conversation history
   */
  getHistory(): AgentConversation[] {
    return this.conversationHistory;
  }
}

/**
 * Multi-Model Coordination for Risk Mitigation
 * Uses multiple strategy models and aggregates decisions
 */
export class MultiModelCoordinator {
  private executors: StrategyExecutor[] = [];

  constructor(strategies: AdvancedStrategy[]) {
    this.executors = strategies.map(s => new StrategyExecutor(s));
  }

  /**
   * Get consensus decision from multiple models
   */
  getConsensusDecision(
    proposal: ProposedTerms,
    opponentLastAction: 'cooperate' | 'defect' | null,
    round: number
  ): 'accept' | 'counter' | 'reject' {
    const decisions = this.executors.map(executor =>
      executor.decideAction(proposal, opponentLastAction, round)
    );

    // Count votes
    const votes = {
      accept: decisions.filter(d => d === 'accept').length,
      counter: decisions.filter(d => d === 'counter').length,
      reject: decisions.filter(d => d === 'reject').length
    };

    // Return majority decision
    if (votes.accept > votes.counter && votes.accept > votes.reject) {
      return 'accept';
    } else if (votes.counter > votes.reject) {
      return 'counter';
    } else {
      return 'reject';
    }
  }

  /**
   * Get confidence score for decision (agreement among models)
   */
  getConfidence(
    proposal: ProposedTerms,
    opponentLastAction: 'cooperate' | 'defect' | null,
    round: number
  ): number {
    const decisions = this.executors.map(executor =>
      executor.decideAction(proposal, opponentLastAction, round)
    );

    const maxVotes = Math.max(
      decisions.filter(d => d === 'accept').length,
      decisions.filter(d => d === 'counter').length,
      decisions.filter(d => d === 'reject').length
    );

    return maxVotes / decisions.length;
  }
}
