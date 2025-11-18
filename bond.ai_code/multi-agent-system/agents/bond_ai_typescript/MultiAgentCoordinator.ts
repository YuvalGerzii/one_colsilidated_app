/**
 * Multi-Agent Coordinator
 * Orchestrates the entire agent-to-agent matching process
 * Coordinates domain matchers, user agents, and negotiations
 */

import { UserRepresentativeAgent } from './UserRepresentativeAgent';
import { NegotiationFacilitator } from './NegotiationFacilitator';
import { DomainMatcherFactory } from './DomainMatcherAgents';
import {
  UserRepresentativeAgent as IUserRepresentativeAgent,
  MatchingDomain,
  AgentConversation,
  NegotiationOutcome,
  Agreement,
  UserProfile
} from './types';
import { Contact, IntelligenceAnalysis } from '../types';
import { IntelligenceEngine } from '../intelligence/IntelligenceEngine';

/**
 * Agent Match Candidate
 */
export interface AgentMatchCandidate {
  agent1: UserRepresentativeAgent;
  agent2: UserRepresentativeAgent;
  domain: MatchingDomain;
  domainScore: number;
  overallScore: number;
  rationale: string[];
  keyFactors: string[];
  risks: string[];
  recommended: boolean;
}

/**
 * Multi-Agent Coordinator
 * Orchestrates agent-based matching and negotiation
 */
export class MultiAgentCoordinator {
  private userAgents: Map<string, UserRepresentativeAgent>;
  private negotiationFacilitator: NegotiationFacilitator;
  private intelligenceEngine: IntelligenceEngine;
  private domainMatchers: Map<MatchingDomain, any>;
  private matchHistory: Map<string, AgentMatchCandidate[]>;
  private agreementHistory: Map<string, Agreement[]>;

  constructor(intelligenceEngine: IntelligenceEngine) {
    this.userAgents = new Map();
    this.negotiationFacilitator = new NegotiationFacilitator();
    this.intelligenceEngine = intelligenceEngine;
    this.domainMatchers = new Map();
    this.matchHistory = new Map();
    this.agreementHistory = new Map();

    // Initialize all domain matchers
    const matchers = DomainMatcherFactory.getAllMatchers();
    matchers.forEach(matcher => {
      this.domainMatchers.set(matcher.domain, matcher);
    });
  }

  /**
   * Register a user and create their representative agent
   */
  async registerUser(
    userId: string,
    contact: Contact,
    userProfile: UserProfile
  ): Promise<UserRepresentativeAgent> {
    // Get intelligence analysis
    const analysis = await this.intelligenceEngine.analyzeContact(contact);

    // Create user representative agent
    const agent = new UserRepresentativeAgent(
      userId,
      contact,
      analysis,
      userProfile
    );

    this.userAgents.set(userId, agent);

    console.log(`✓ Registered user ${contact.name} with agent ${agent.id}`);

    return agent;
  }

  /**
   * Find all potential matches for a user using agent-based approach
   */
  async findAgentMatches(userId: string): Promise<AgentMatchCandidate[]> {
    const userAgent = this.userAgents.get(userId);
    if (!userAgent) {
      throw new Error('User agent not found. Please register user first.');
    }

    const candidates: AgentMatchCandidate[] = [];

    // Check against all other users
    for (const [otherUserId, otherAgent] of this.userAgents.entries()) {
      if (otherUserId === userId) continue;

      // Try all domain matchers to find best fit
      const domainResults = await this.evaluateAllDomains(userAgent, otherAgent);

      if (domainResults.length > 0) {
        // Take best domain match
        const best = domainResults.reduce((a, b) =>
          a.overallScore > b.overallScore ? a : b
        );

        candidates.push(best);
      }
    }

    // Sort by overall score
    candidates.sort((a, b) => b.overallScore - a.overallScore);

    // Store in history
    this.matchHistory.set(userId, candidates);

    return candidates;
  }

  /**
   * Evaluate a pair of agents across all domain matchers
   */
  private async evaluateAllDomains(
    agent1: UserRepresentativeAgent,
    agent2: UserRepresentativeAgent
  ): Promise<AgentMatchCandidate[]> {
    const results: AgentMatchCandidate[] = [];

    for (const [domain, matcher] of this.domainMatchers.entries()) {
      const domainScore = matcher.calculateMatchScore(agent1, agent2);

      // Only consider if domain score is meaningful
      if (domainScore >= 0.5) {
        const potential = matcher.identifyMatchPotential(agent1, agent2);

        // Calculate overall score combining domain score and general compatibility
        const compatibility = await this.calculateGeneralCompatibility(agent1, agent2);
        const overallScore = (domainScore * 0.6 + compatibility * 0.4);

        const candidate: AgentMatchCandidate = {
          agent1,
          agent2,
          domain,
          domainScore,
          overallScore,
          rationale: potential.rationale,
          keyFactors: potential.keyFactors,
          risks: potential.risks,
          recommended: overallScore >= 0.7
        };

        results.push(candidate);
      }
    }

    return results;
  }

  /**
   * Calculate general compatibility between agents
   */
  private async calculateGeneralCompatibility(
    agent1: UserRepresentativeAgent,
    agent2: UserRepresentativeAgent
  ): Promise<number> {
    return this.intelligenceEngine.calculateCompatibility(
      agent1.userContact,
      agent1.userAnalysis,
      agent2.userContact,
      agent2.userAnalysis
    ).score;
  }

  /**
   * Initiate agent-to-agent negotiation for a match candidate
   */
  async negotiateMatch(candidate: AgentMatchCandidate): Promise<NegotiationOutcome> {
    console.log(`\n${'='.repeat(80)}`);
    console.log(`INITIATING AGENT-TO-AGENT NEGOTIATION`);
    console.log(`Domain: ${candidate.domain}`);
    console.log(`Participants: ${candidate.agent1.name} ⟷ ${candidate.agent2.name}`);
    console.log(`Pre-negotiation Score: ${(candidate.overallScore * 100).toFixed(0)}%`);
    console.log(`${'='.repeat(80)}\n`);

    const outcome = await this.negotiationFacilitator.conductNegotiation(
      candidate.agent1,
      candidate.agent2
    );

    // Store agreement if successful
    if (outcome.success && outcome.agreement) {
      const userId1 = candidate.agent1.userId;
      const userId2 = candidate.agent2.userId;

      if (!this.agreementHistory.has(userId1)) {
        this.agreementHistory.set(userId1, []);
      }
      if (!this.agreementHistory.has(userId2)) {
        this.agreementHistory.set(userId2, []);
      }

      this.agreementHistory.get(userId1)!.push(outcome.agreement);
      this.agreementHistory.get(userId2)!.push(outcome.agreement);
    }

    return outcome;
  }

  /**
   * Run complete matching process for a user
   * 1. Find candidates
   * 2. Rank by domain + compatibility
   * 3. Conduct negotiations with top candidates
   * 4. Return successful agreements
   */
  async runCompleteMatchingProcess(
    userId: string,
    maxNegotiations: number = 3
  ): Promise<{
    candidates: AgentMatchCandidate[];
    negotiations: Array<{
      candidate: AgentMatchCandidate;
      outcome: NegotiationOutcome;
    }>;
    agreements: Agreement[];
  }> {
    console.log(`\n${'█'.repeat(80)}`);
    console.log(`COMPLETE MATCHING PROCESS FOR USER: ${userId}`);
    console.log(`${'█'.repeat(80)}\n`);

    // Step 1: Find candidates
    console.log('Step 1: Finding match candidates...');
    const candidates = await this.findAgentMatches(userId);
    console.log(`✓ Found ${candidates.length} potential matches\n`);

    // Step 2: Select top candidates for negotiation
    const topCandidates = candidates
      .filter(c => c.recommended)
      .slice(0, maxNegotiations);

    console.log(`Step 2: Selected ${topCandidates.length} top candidates for negotiation\n`);

    // Step 3: Conduct negotiations
    console.log('Step 3: Conducting agent-to-agent negotiations...\n');
    const negotiations: Array<{
      candidate: AgentMatchCandidate;
      outcome: NegotiationOutcome;
    }> = [];

    for (const candidate of topCandidates) {
      const outcome = await this.negotiateMatch(candidate);
      negotiations.push({ candidate, outcome });

      // Small delay between negotiations
      await this.sleep(100);
    }

    // Step 4: Collect successful agreements
    const agreements = negotiations
      .filter(n => n.outcome.success)
      .map(n => n.outcome.agreement!)
      .filter(a => a !== undefined);

    console.log(`\n${'█'.repeat(80)}`);
    console.log(`MATCHING PROCESS COMPLETE`);
    console.log(`Total Candidates: ${candidates.length}`);
    console.log(`Negotiations Conducted: ${negotiations.length}`);
    console.log(`Successful Agreements: ${agreements.length}`);
    console.log(`Success Rate: ${negotiations.length > 0 ? (agreements.length / negotiations.length * 100).toFixed(0) : 0}%`);
    console.log(`${'█'.repeat(80)}\n`);

    return {
      candidates,
      negotiations,
      agreements
    };
  }

  /**
   * Get user agent
   */
  getUserAgent(userId: string): UserRepresentativeAgent | undefined {
    return this.userAgents.get(userId);
  }

  /**
   * Get all user agents
   */
  getAllUserAgents(): UserRepresentativeAgent[] {
    return Array.from(this.userAgents.values());
  }

  /**
   * Get match history for user
   */
  getMatchHistory(userId: string): AgentMatchCandidate[] {
    return this.matchHistory.get(userId) || [];
  }

  /**
   * Get agreement history for user
   */
  getAgreementHistory(userId: string): Agreement[] {
    return this.agreementHistory.get(userId) || [];
  }

  /**
   * Get all agreements
   */
  getAllAgreements(): Agreement[] {
    const all: Agreement[] = [];
    for (const agreements of this.agreementHistory.values()) {
      all.push(...agreements);
    }

    // Deduplicate
    const unique = Array.from(new Set(all.map(a => a.id)))
      .map(id => all.find(a => a.id === id)!);

    return unique;
  }

  /**
   * Get platform statistics
   */
  getPlatformStatistics(): {
    totalUsers: number;
    totalMatches: number;
    totalNegotiations: number;
    totalAgreements: number;
    successRate: number;
    averageMatchScore: number;
    agreementsByDomain: Record<string, number>;
  } {
    const totalUsers = this.userAgents.size;

    const allMatches = Array.from(this.matchHistory.values())
      .reduce((acc, matches) => acc + matches.length, 0);

    const conversations = this.negotiationFacilitator.getAllConversations();
    const totalNegotiations = conversations.length;

    const allAgreements = this.getAllAgreements();
    const totalAgreements = allAgreements.length;

    const successRate = this.negotiationFacilitator.getSuccessRate();

    const allCandidates = Array.from(this.matchHistory.values()).flat();
    const averageMatchScore = allCandidates.length > 0
      ? allCandidates.reduce((sum, c) => sum + c.overallScore, 0) / allCandidates.length
      : 0;

    const agreementsByDomain: Record<string, number> = {};
    for (const candidate of allCandidates) {
      agreementsByDomain[candidate.domain] = (agreementsByDomain[candidate.domain] || 0) + 1;
    }

    return {
      totalUsers,
      totalMatches: allMatches,
      totalNegotiations,
      totalAgreements,
      successRate,
      averageMatchScore,
      agreementsByDomain
    };
  }

  /**
   * Get top performers (users with most successful agreements)
   */
  getTopPerformers(limit: number = 5): Array<{
    userId: string;
    userName: string;
    agreementCount: number;
    averageSatisfaction: number;
  }> {
    const performers: Array<{
      userId: string;
      userName: string;
      agreementCount: number;
      averageSatisfaction: number;
    }> = [];

    for (const [userId, agent] of this.userAgents.entries()) {
      const agreements = this.agreementHistory.get(userId) || [];
      if (agreements.length > 0) {
        const avgSatisfaction = agreements.reduce((sum, agreement) => {
          const benefit = agreement.agent1.userId === userId
            ? agreement.mutualBenefit.agent1Benefits
            : agreement.mutualBenefit.agent2Benefits;

          const satisfaction = benefit.reduce((s, b) => s + b.estimatedValue, 0) / benefit.length;
          return sum + satisfaction;
        }, 0) / agreements.length;

        performers.push({
          userId,
          userName: agent.userContact.name,
          agreementCount: agreements.length,
          averageSatisfaction: avgSatisfaction
        });
      }
    }

    return performers
      .sort((a, b) => b.agreementCount - a.agreementCount)
      .slice(0, limit);
  }

  /**
   * Utility: Sleep for ms
   */
  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
