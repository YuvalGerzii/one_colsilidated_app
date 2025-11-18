/**
 * Reinforcement Learning Agent Service
 * Implements Q-Learning for negotiation strategy optimization
 */

import { getDb } from '../database/connection';
import crypto from 'crypto';

export interface NegotiationState {
  currentRound: number;
  proposalScore: number;
  otherAgentStyle: string;
  needsSatisfaction: number;
  givingCost: number;
  trustLevel: number;
}

export enum NegotiationAction {
  ACCEPT = 'accept',
  COUNTER_AGGRESSIVE = 'counter_aggressive',
  COUNTER_MODERATE = 'counter_moderate',
  COUNTER_ACCOMMODATING = 'counter_accommodating',
  REQUEST_CLARIFICATION = 'request_clarification',
  ADD_SWEETENER = 'add_sweetener',
  REJECT = 'reject',
}

export interface RLConfig {
  learningRate: number; // α (alpha)
  discountFactor: number; // γ (gamma)
  explorationRate: number; // ε (epsilon)
  explorationDecay: number;
  minExplorationRate: number;
}

export class RLAgentService {
  private agentId: string;
  private config: RLConfig;
  private qTable: Map<string, Map<NegotiationAction, number>>;

  constructor(
    agentId: string,
    config: Partial<RLConfig> = {}
  ) {
    this.agentId = agentId;
    this.config = {
      learningRate: config.learningRate ?? 0.1,
      discountFactor: config.discountFactor ?? 0.95,
      explorationRate: config.explorationRate ?? 0.2,
      explorationDecay: config.explorationDecay ?? 0.995,
      minExplorationRate: config.minExplorationRate ?? 0.01,
    };
    this.qTable = new Map();
  }

  /**
   * Initialize Q-table from database
   */
  async initialize(): Promise<void> {
    const db = getDb();

    // Load Q-values from database
    const qValues = await db.queryMany<{
      state_hash: string;
      action: string;
      q_value: number;
    }>(
      'SELECT state_hash, action, q_value FROM rl_q_values WHERE agent_id = $1',
      [this.agentId]
    );

    // Populate Q-table
    qValues.forEach((row) => {
      if (!this.qTable.has(row.state_hash)) {
        this.qTable.set(row.state_hash, new Map());
      }
      this.qTable
        .get(row.state_hash)!
        .set(row.action as NegotiationAction, row.q_value);
    });

    console.log(`Loaded ${qValues.length} Q-values for agent ${this.agentId}`);
  }

  /**
   * Hash state for lookup
   */
  private hashState(state: NegotiationState): string {
    // Discretize continuous values
    const discretized = {
      round: Math.floor(state.currentRound),
      score: Math.floor(state.proposalScore * 10) / 10,
      style: state.otherAgentStyle,
      needs: Math.floor(state.needsSatisfaction * 10) / 10,
      cost: Math.floor(state.givingCost * 10) / 10,
      trust: Math.floor(state.trustLevel * 10) / 10,
    };

    // Create hash
    const stateString = JSON.stringify(discretized);
    return crypto.createHash('sha256').update(stateString).digest('hex').substring(0, 16);
  }

  /**
   * Get Q-value for state-action pair
   */
  private getQValue(stateHash: string, action: NegotiationAction): number {
    if (!this.qTable.has(stateHash)) {
      return 0; // Initial Q-value
    }

    const actions = this.qTable.get(stateHash)!;
    return actions.get(action) ?? 0;
  }

  /**
   * Set Q-value for state-action pair
   */
  private setQValue(
    stateHash: string,
    action: NegotiationAction,
    value: number
  ): void {
    if (!this.qTable.has(stateHash)) {
      this.qTable.set(stateHash, new Map());
    }

    this.qTable.get(stateHash)!.set(action, value);
  }

  /**
   * Select action using epsilon-greedy policy
   */
  selectAction(state: NegotiationState): NegotiationAction {
    const stateHash = this.hashState(state);

    // Exploration: random action
    if (Math.random() < this.config.explorationRate) {
      const actions = Object.values(NegotiationAction);
      return actions[Math.floor(Math.random() * actions.length)];
    }

    // Exploitation: best action
    return this.getBestAction(stateHash);
  }

  /**
   * Get best action for state
   */
  private getBestAction(stateHash: string): NegotiationAction {
    const actions = Object.values(NegotiationAction);
    let bestAction = actions[0];
    let bestValue = this.getQValue(stateHash, bestAction);

    for (const action of actions) {
      const value = this.getQValue(stateHash, action);
      if (value > bestValue) {
        bestValue = value;
        bestAction = action;
      }
    }

    return bestAction;
  }

  /**
   * Get maximum Q-value for state
   */
  private getMaxQValue(stateHash: string): number {
    const actions = Object.values(NegotiationAction);
    let maxValue = this.getQValue(stateHash, actions[0]);

    for (const action of actions) {
      const value = this.getQValue(stateHash, action);
      if (value > maxValue) {
        maxValue = value;
      }
    }

    return maxValue;
  }

  /**
   * Update Q-value using Q-learning algorithm
   * Q(s,a) = Q(s,a) + α[r + γ max Q(s',a') - Q(s,a)]
   */
  async learn(
    state: NegotiationState,
    action: NegotiationAction,
    reward: number,
    nextState: NegotiationState
  ): Promise<void> {
    const stateHash = this.hashState(state);
    const nextStateHash = this.hashState(nextState);

    // Current Q-value
    const currentQ = this.getQValue(stateHash, action);

    // Maximum Q-value for next state
    const maxNextQ = this.getMaxQValue(nextStateHash);

    // Q-learning update
    const newQ =
      currentQ +
      this.config.learningRate *
        (reward + this.config.discountFactor * maxNextQ - currentQ);

    // Update Q-table
    this.setQValue(stateHash, action, newQ);

    // Persist to database (async, don't wait)
    this.persistQValue(stateHash, action, newQ).catch((err) =>
      console.error('Failed to persist Q-value:', err)
    );

    // Decay exploration rate
    this.config.explorationRate = Math.max(
      this.config.minExplorationRate,
      this.config.explorationRate * this.config.explorationDecay
    );
  }

  /**
   * Persist Q-value to database
   */
  private async persistQValue(
    stateHash: string,
    action: NegotiationAction,
    qValue: number
  ): Promise<void> {
    const db = getDb();

    await db.query(
      `INSERT INTO rl_q_values (agent_id, state_hash, action, q_value, visits, updated_at)
       VALUES ($1, $2, $3, $4, 1, NOW())
       ON CONFLICT (agent_id, state_hash, action)
       DO UPDATE SET
         q_value = $4,
         visits = rl_q_values.visits + 1,
         updated_at = NOW()`,
      [this.agentId, stateHash, action, qValue]
    );
  }

  /**
   * Calculate reward based on negotiation outcome
   */
  static calculateReward(outcome: {
    success: boolean;
    mutualBenefit?: number;
    proposalAccepted?: boolean;
    negotiationFailed?: boolean;
  }): number {
    if (outcome.success && outcome.mutualBenefit) {
      // Agreement reached with high mutual benefit
      if (outcome.mutualBenefit >= 0.8) {
        return 100;
      } else if (outcome.mutualBenefit >= 0.6) {
        return 50;
      } else {
        return 30;
      }
    }

    if (outcome.proposalAccepted) {
      // Proposal accepted
      return 20;
    }

    if (outcome.negotiationFailed) {
      // Negotiation failed
      return -50;
    }

    // Proposal rejected
    return -10;
  }

  /**
   * Get agent statistics
   */
  async getStatistics(): Promise<{
    totalStates: number;
    totalActions: number;
    avgQValue: number;
    explorationRate: number;
    topActions: Array<{ action: string; avgQValue: number }>;
  }> {
    const db = getDb();

    const stats = await db.queryOne<{
      total_states: number;
      total_actions: number;
      avg_q_value: number;
    }>(
      `SELECT
        COUNT(DISTINCT state_hash) as total_states,
        COUNT(*) as total_actions,
        AVG(q_value) as avg_q_value
       FROM rl_q_values
       WHERE agent_id = $1`,
      [this.agentId]
    );

    const topActions = await db.queryMany<{
      action: string;
      avg_q_value: number;
    }>(
      `SELECT
        action,
        AVG(q_value) as avg_q_value
       FROM rl_q_values
       WHERE agent_id = $1
       GROUP BY action
       ORDER BY avg_q_value DESC
       LIMIT 5`,
      [this.agentId]
    );

    return {
      totalStates: stats?.total_states || 0,
      totalActions: stats?.total_actions || 0,
      avgQValue: stats?.avg_q_value || 0,
      explorationRate: this.config.explorationRate,
      topActions: topActions.map((row) => ({
        action: row.action,
        avgQValue: row.avg_q_value,
      })),
    };
  }

  /**
   * Export Q-table for analysis
   */
  exportQTable(): Array<{
    stateHash: string;
    action: NegotiationAction;
    qValue: number;
  }> {
    const exported: Array<{
      stateHash: string;
      action: NegotiationAction;
      qValue: number;
    }> = [];

    this.qTable.forEach((actions, stateHash) => {
      actions.forEach((qValue, action) => {
        exported.push({ stateHash, action, qValue });
      });
    });

    return exported;
  }

  /**
   * Reset learning (for testing)
   */
  async reset(): Promise<void> {
    const db = getDb();

    await db.query('DELETE FROM rl_q_values WHERE agent_id = $1', [this.agentId]);

    this.qTable.clear();
    this.config.explorationRate = 0.2; // Reset to initial
  }
}

/**
 * RL Agent Manager
 * Manages multiple RL agents
 */
export class RLAgentManager {
  private agents: Map<string, RLAgentService> = new Map();

  /**
   * Get or create RL agent for user
   */
  async getAgent(agentId: string): Promise<RLAgentService> {
    if (this.agents.has(agentId)) {
      return this.agents.get(agentId)!;
    }

    const agent = new RLAgentService(agentId);
    await agent.initialize();
    this.agents.set(agentId, agent);

    return agent;
  }

  /**
   * Get statistics for all agents
   */
  async getAllStatistics(): Promise<
    Array<{
      agentId: string;
      stats: Awaited<ReturnType<RLAgentService['getStatistics']>>;
    }>
  > {
    const results = [];

    for (const [agentId, agent] of this.agents.entries()) {
      const stats = await agent.getStatistics();
      results.push({ agentId, stats });
    }

    return results;
  }
}

// Singleton instance
let rlManagerInstance: RLAgentManager | null = null;

/**
 * Get RL agent manager
 */
export function getRLAgentManager(): RLAgentManager {
  if (!rlManagerInstance) {
    rlManagerInstance = new RLAgentManager();
  }
  return rlManagerInstance;
}
