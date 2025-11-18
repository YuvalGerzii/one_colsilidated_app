/**
 * Board Room Agent
 *
 * Orchestrates a "board room" of world-class business leaders to provide
 * collective wisdom, diverse perspectives, and consensus recommendations
 * on strategic decisions.
 *
 * Brings together leaders from different sectors and specializations
 * to guide company decisions, strategies, and implementations.
 */

import { Pool } from 'pg';
import Redis from 'ioredis';
import {
  IBehaviorAgent,
  BoardRoomConfig,
  BoardRoomConsensus,
  BusinessAdvice,
  DecisionContext,
  BusinessSector,
} from './BehaviorAgentTypes';

export class BoardRoomAgent {
  private configs: Map<string, BoardRoomConfig> = new Map();

  constructor(
    private pool: Pool,
    private redis: Redis
  ) {}

  /**
   * Register a pre-configured board room
   */
  registerBoardRoom(config: BoardRoomConfig): void {
    this.configs.set(config.name, config);
  }

  /**
   * Create an ad-hoc board room for a specific decision
   */
  createAdHocBoardRoom(
    name: string,
    members: IBehaviorAgent[],
    focus: BusinessSector[],
    decisionMakingStyle: 'unanimous' | 'majority' | 'weighted' | 'advisory' = 'majority'
  ): BoardRoomConfig {
    const config: BoardRoomConfig = {
      name,
      focus,
      members,
      consensusThreshold: 0.6, // 60% for majority
      decisionMakingStyle,
    };

    this.registerBoardRoom(config);
    return config;
  }

  /**
   * Get consensus advice from a board room on a business question
   */
  async getBoardRoomConsensus(
    boardRoomName: string,
    question: string,
    context: DecisionContext,
    sector: BusinessSector,
    additionalInfo?: Record<string, any>
  ): Promise<BoardRoomConsensus> {
    const config = this.configs.get(boardRoomName);
    if (!config) {
      throw new Error(`Board room '${boardRoomName}' not found`);
    }

    // Cache key
    const cacheKey = `boardroom:${boardRoomName}:${this.hashString(question)}:${context}`;
    const cached = await this.redis.get(cacheKey);
    if (cached) return JSON.parse(cached);

    // Get advice from each board member in parallel
    const advicePromises = config.members.map(async (member) => {
      const advice = await member.getAdvice(question, context, additionalInfo);
      return {
        leaderName: member.profile.name,
        advice,
      };
    });

    const adviceResults = await Promise.all(advicePromises);

    // Build map of individual advice
    const individualAdvice = new Map<string, BusinessAdvice>();
    adviceResults.forEach(({ leaderName, advice }) => {
      individualAdvice.set(leaderName, advice);
    });

    // Analyze consensus
    const consensus = this.analyzeConsensus(
      individualAdvice,
      config,
      question,
      context,
      sector
    );

    // Cache for 1 hour
    await this.redis.set(cacheKey, JSON.stringify(consensus), 'EX', 3600);

    return consensus;
  }

  /**
   * Get strategic guidance from board room
   */
  async getBoardRoomStrategicGuidance(
    boardRoomName: string,
    situation: string,
    goals: string[],
    constraints: string[]
  ): Promise<{
    consensus: string;
    individualGuidance: Map<string, any>;
    implementationRoadmap: any;
  }> {
    const config = this.configs.get(boardRoomName);
    if (!config) {
      throw new Error(`Board room '${boardRoomName}' not found`);
    }

    // Get guidance from each member
    const guidancePromises = config.members.map(async (member) => {
      const guidance = await member.getStrategicGuidance(situation, goals, constraints);
      return {
        leaderName: member.profile.name,
        guidance,
      };
    });

    const guidanceResults = await Promise.all(guidancePromises);

    const individualGuidance = new Map();
    guidanceResults.forEach(({ leaderName, guidance }) => {
      individualGuidance.set(leaderName, guidance);
    });

    // Synthesize consensus strategy
    const consensus = this.synthesizeStrategicConsensus(guidanceResults, config);

    // Build implementation roadmap
    const implementationRoadmap = this.buildImplementationRoadmap(guidanceResults);

    return {
      consensus,
      individualGuidance,
      implementationRoadmap,
    };
  }

  /**
   * Evaluate opportunity with board room
   */
  async evaluateOpportunityWithBoardRoom(
    boardRoomName: string,
    opportunity: string,
    context: Record<string, any>
  ): Promise<{
    recommendation: 'pursue' | 'pass' | 'modify';
    voteBreakdown: Map<string, any>;
    consensus: string;
    conditions?: string[];
    modifications?: string[];
  }> {
    const config = this.configs.get(boardRoomName);
    if (!config) {
      throw new Error(`Board room '${boardRoomName}' not found`);
    }

    // Get evaluations from each member
    const evaluationPromises = config.members.map(async (member) => {
      const evaluation = await member.evaluateOpportunity(opportunity, context);
      return {
        leaderName: member.profile.name,
        evaluation,
      };
    });

    const evaluationResults = await Promise.all(evaluationPromises);

    const voteBreakdown = new Map();
    const votes = { pursue: 0, pass: 0, modify: 0 };
    const allConditions: string[] = [];
    const allModifications: string[] = [];

    evaluationResults.forEach(({ leaderName, evaluation }) => {
      voteBreakdown.set(leaderName, evaluation);
      votes[evaluation.recommendation]++;

      if (evaluation.conditions) {
        allConditions.push(...evaluation.conditions);
      }
      if (evaluation.modifications) {
        allModifications.push(...evaluation.modifications);
      }
    });

    // Determine consensus recommendation
    let recommendation: 'pursue' | 'pass' | 'modify';
    if (votes.pursue > votes.pass && votes.pursue > votes.modify) {
      recommendation = 'pursue';
    } else if (votes.modify > votes.pass && votes.modify > votes.pursue) {
      recommendation = 'modify';
    } else {
      recommendation = 'pass';
    }

    // Build consensus explanation
    const consensus = this.buildOpportunityConsensus(
      evaluationResults,
      recommendation,
      votes,
      config
    );

    return {
      recommendation,
      voteBreakdown,
      consensus,
      conditions: recommendation === 'pursue' ? this.deduplicateAndPrioritize(allConditions) : undefined,
      modifications: recommendation === 'modify' ? this.deduplicateAndPrioritize(allModifications) : undefined,
    };
  }

  /**
   * Compare different approaches using board room wisdom
   */
  async compareApproaches(
    boardRoomName: string,
    approaches: Array<{ name: string; description: string }>,
    context: DecisionContext
  ): Promise<{
    ranking: Array<{ approach: string; score: number; reasoning: string }>;
    recommendation: string;
    individualRankings: Map<string, any>;
  }> {
    const config = this.configs.get(boardRoomName);
    if (!config) {
      throw new Error(`Board room '${boardRoomName}' not found`);
    }

    const individualRankings = new Map();
    const scoresByApproach = new Map<string, number[]>();

    // Initialize score arrays
    approaches.forEach(approach => {
      scoresByApproach.set(approach.name, []);
    });

    // Get each leader's perspective on each approach
    for (const member of config.members) {
      const memberRanking: any[] = [];

      for (const approach of approaches) {
        const evaluation = await member.evaluateOpportunity(
          approach.description,
          { context, name: approach.name }
        );

        memberRanking.push({
          approach: approach.name,
          score: evaluation.score,
          recommendation: evaluation.recommendation,
          reasoning: evaluation.reasoning,
        });

        scoresByApproach.get(approach.name)?.push(evaluation.score);
      }

      individualRankings.set(member.profile.name, memberRanking);
    }

    // Calculate average scores
    const ranking = approaches.map(approach => {
      const scores = scoresByApproach.get(approach.name) || [];
      const avgScore = scores.reduce((sum, score) => sum + score, 0) / scores.length;

      return {
        approach: approach.name,
        score: avgScore,
        reasoning: this.buildApproachReasoning(approach.name, individualRankings),
      };
    }).sort((a, b) => b.score - a.score);

    const recommendation = this.buildComparisonRecommendation(ranking, individualRankings);

    return {
      ranking,
      recommendation,
      individualRankings,
    };
  }

  /**
   * Get list of registered board rooms
   */
  getBoardRooms(): string[] {
    return Array.from(this.configs.keys());
  }

  /**
   * Get board room configuration
   */
  getBoardRoomConfig(name: string): BoardRoomConfig | undefined {
    return this.configs.get(name);
  }

  // Private helper methods

  private analyzeConsensus(
    individualAdvice: Map<string, BusinessAdvice>,
    config: BoardRoomConfig,
    question: string,
    context: DecisionContext,
    sector: BusinessSector
  ): BoardRoomConsensus {
    const adviceArray = Array.from(individualAdvice.values());

    // Extract common themes
    const commonThemes = this.extractCommonThemes(adviceArray);
    const divergentViews = this.extractDivergentViews(adviceArray);

    // Build consensus recommendation
    const consensusRecommendation = this.buildConsensusRecommendation(
      commonThemes,
      adviceArray,
      config
    );

    // Determine majority and minority opinions
    const { majorityOpinion, minorityOpinions } = this.identifyOpinions(
      adviceArray,
      config
    );

    // Risk assessment
    const riskAssessment = this.assessRisks(adviceArray);

    // Calculate confidence
    const confidenceScore = this.calculateConfidence(adviceArray, commonThemes);

    // Build implementation plan
    const implementationPlan = this.buildImplementationPlan(adviceArray);

    // Identify dissenting views
    const dissent = this.identifyDissent(individualAdvice, consensusRecommendation);

    return {
      question,
      context,
      sector,
      individualAdvice,
      consensusRecommendation,
      majorityOpinion,
      minorityOpinions,
      riskAssessment,
      confidenceScore,
      implementationPlan,
      dissent,
    };
  }

  private extractCommonThemes(advice: BusinessAdvice[]): string[] {
    // Simple keyword frequency analysis
    const keywordMap = new Map<string, number>();

    advice.forEach(a => {
      const words = a.advice.toLowerCase().split(/\s+/);
      words.forEach(word => {
        if (word.length > 4) { // Skip short words
          keywordMap.set(word, (keywordMap.get(word) || 0) + 1);
        }
      });
    });

    // Get most common keywords
    return Array.from(keywordMap.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .map(([word]) => word);
  }

  private extractDivergentViews(advice: BusinessAdvice[]): string[] {
    const divergent: string[] = [];

    // Find advice with significantly different success probabilities
    const avgProb = advice.reduce((sum, a) => sum + a.successProbability, 0) / advice.length;

    advice.forEach(a => {
      if (Math.abs(a.successProbability - avgProb) > 0.3) {
        divergent.push(`${a.leaderName}: ${a.advice.substring(0, 100)}...`);
      }
    });

    return divergent;
  }

  private buildConsensusRecommendation(
    themes: string[],
    advice: BusinessAdvice[],
    config: BoardRoomConfig
  ): string {
    // Aggregate the advice
    const recommendations: string[] = [];

    advice.forEach(a => {
      recommendations.push(`**${a.leaderName}**: ${a.advice}`);
    });

    return `## Board Room Consensus\n\n${recommendations.join('\n\n')}\n\n## Synthesis\n\nThe board emphasizes: ${themes.slice(0, 5).join(', ')}. Consider multiple perspectives and adapt based on your specific context.`;
  }

  private identifyOpinions(
    advice: BusinessAdvice[],
    config: BoardRoomConfig
  ): { majorityOpinion: string; minorityOpinions: string[] } {
    // Group by success probability ranges
    const high = advice.filter(a => a.successProbability > 0.7);
    const medium = advice.filter(a => a.successProbability >= 0.4 && a.successProbability <= 0.7);
    const low = advice.filter(a => a.successProbability < 0.4);

    let majorityOpinion = '';
    const minorityOpinions: string[] = [];

    if (high.length > advice.length / 2) {
      majorityOpinion = `Majority of the board (${high.length}/${advice.length}) is optimistic about this approach with high confidence in success.`;
      if (low.length > 0) {
        minorityOpinions.push(`${low.length} member(s) express significant concerns about success probability.`);
      }
    } else if (medium.length > advice.length / 2) {
      majorityOpinion = `Majority of the board (${medium.length}/${advice.length}) sees moderate potential with careful execution required.`;
    } else {
      majorityOpinion = `Board opinion is divided across different confidence levels. Consider the specific concerns of each leader.`;
    }

    return { majorityOpinion, minorityOpinions };
  }

  private assessRisks(advice: BusinessAdvice[]): {
    level: 'low' | 'medium' | 'high' | 'very_high';
    factors: string[];
  } {
    const allRisks = advice.flatMap(a => a.potentialRisks);
    const uniqueRisks = [...new Set(allRisks)];

    // Count risk mentions
    const riskCounts = new Map<string, number>();
    allRisks.forEach(risk => {
      riskCounts.set(risk, (riskCounts.get(risk) || 0) + 1);
    });

    // Get most mentioned risks
    const topRisks = Array.from(riskCounts.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .map(([risk]) => risk);

    // Determine risk level based on average success probability
    const avgSuccess = advice.reduce((sum, a) => sum + a.successProbability, 0) / advice.length;
    let level: 'low' | 'medium' | 'high' | 'very_high';

    if (avgSuccess > 0.75) level = 'low';
    else if (avgSuccess > 0.6) level = 'medium';
    else if (avgSuccess > 0.4) level = 'high';
    else level = 'very_high';

    return { level, factors: topRisks };
  }

  private calculateConfidence(advice: BusinessAdvice[], themes: string[]): number {
    // Confidence based on agreement level
    const avgSuccess = advice.reduce((sum, a) => sum + a.successProbability, 0) / advice.length;
    const variance = advice.reduce(
      (sum, a) => sum + Math.pow(a.successProbability - avgSuccess, 2),
      0
    ) / advice.length;

    // Lower variance = higher confidence
    const agreementScore = 1 - Math.min(variance * 4, 0.5);

    return avgSuccess * agreementScore;
  }

  private buildImplementationPlan(advice: BusinessAdvice[]): BoardRoomConsensus['implementationPlan'] {
    // Aggregate actionable steps from all advice
    const allSteps = advice.flatMap(a => a.actionableSteps);
    const stepGroups = this.groupSimilarSteps(allSteps);

    const phases = stepGroups.map((steps, index) => ({
      phase: `Phase ${index + 1}`,
      duration: advice[0]?.timeframe || 'To be determined',
      actions: steps,
      milestones: [`Complete ${steps.length} key actions`],
    }));

    return {
      phases,
      totalTimeline: this.aggregateTimelines(advice.map(a => a.timeframe)),
    };
  }

  private groupSimilarSteps(steps: string[]): string[][] {
    // Simple grouping - in production would use more sophisticated NLP
    const groups: string[][] = [];
    const groupSize = Math.ceil(steps.length / 3);

    for (let i = 0; i < steps.length; i += groupSize) {
      groups.push(steps.slice(i, i + groupSize));
    }

    return groups.filter(g => g.length > 0);
  }

  private aggregateTimelines(timeframes: string[]): string {
    // Extract numbers and find maximum
    const numbers = timeframes
      .map(t => parseInt(t.match(/\d+/)?.[0] || '0'))
      .filter(n => n > 0);

    if (numbers.length === 0) return 'Timeline to be determined based on scope';

    const max = Math.max(...numbers);
    return `Estimated ${max}-${max * 1.5} months for full implementation`;
  }

  private identifyDissent(
    individualAdvice: Map<string, BusinessAdvice>,
    consensus: string
  ): BoardRoomConsensus['dissent'] {
    const dissent: BoardRoomConsensus['dissent'] = [];

    individualAdvice.forEach((advice, leader) => {
      if (advice.successProbability < 0.5) {
        dissent.push({
          leader,
          concern: advice.potentialRisks.join(', '),
          alternativeView: advice.alternativeApproaches[0] || 'Consider alternative approach',
        });
      }
    });

    return dissent.length > 0 ? dissent : undefined;
  }

  private synthesizeStrategicConsensus(guidanceResults: any[], config: BoardRoomConfig): string {
    const strategies = guidanceResults.map(r =>
      `**${r.leaderName}**: ${r.guidance.strategy}\n\n*Rationale*: ${r.guidance.rationale}`
    );

    return `# Strategic Consensus\n\n${strategies.join('\n\n---\n\n')}`;
  }

  private buildImplementationRoadmap(guidanceResults: any[]): any {
    const allSteps = guidanceResults.flatMap(r => r.guidance.steps);
    const allRisks = guidanceResults.flatMap(r => r.guidance.risks);

    return {
      consolidatedSteps: [...new Set(allSteps)],
      consolidatedRisks: [...new Set(allRisks)],
      timeline: guidanceResults[0]?.guidance.timeline || 'To be determined',
    };
  }

  private buildOpportunityConsensus(
    evaluations: any[],
    recommendation: 'pursue' | 'pass' | 'modify',
    votes: any,
    config: BoardRoomConfig
  ): string {
    const total = config.members.length;
    const breakdown = `**Vote Breakdown**: Pursue: ${votes.pursue}/${total}, Modify: ${votes.modify}/${total}, Pass: ${votes.pass}/${total}`;

    const details = evaluations.map(e =>
      `- **${e.leaderName}**: ${e.evaluation.recommendation} (score: ${e.evaluation.score.toFixed(2)}) - ${e.evaluation.reasoning}`
    ).join('\n');

    return `## Board Room Recommendation: ${recommendation.toUpperCase()}\n\n${breakdown}\n\n### Individual Perspectives:\n${details}`;
  }

  private buildApproachReasoning(approach: string, rankings: Map<string, any>): string {
    const reasons: string[] = [];

    rankings.forEach((ranking, leader) => {
      const item = ranking.find((r: any) => r.approach === approach);
      if (item) {
        reasons.push(`${leader}: ${item.reasoning.substring(0, 100)}...`);
      }
    });

    return reasons.join(' | ');
  }

  private buildComparisonRecommendation(ranking: any[], individualRankings: Map<string, any>): string {
    const top = ranking[0];
    return `The board recommends **${top.approach}** with an average score of ${top.score.toFixed(2)}. This approach received the highest combined confidence from the leadership team.`;
  }

  private deduplicateAndPrioritize(items: string[]): string[] {
    const counts = new Map<string, number>();
    items.forEach(item => {
      counts.set(item, (counts.get(item) || 0) + 1);
    });

    return Array.from(counts.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .map(([item]) => item);
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
