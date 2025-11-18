/**
 * Bond.AI Enhanced - Main Coordinator with Agent-to-Agent Matching
 * Integrates traditional matching with advanced agent-based negotiation
 */

import { BondAI } from './BondAI';
import { MultiAgentCoordinator, AgentMatchCandidate } from './agents/MultiAgentCoordinator';
import { UserProfile, Agreement, NegotiationOutcome } from './agents/types';
import { Contact, BondAIConfig } from './types';

/**
 * Enhanced Bond.AI with Agent-Based Matching
 */
export class BondAI_Enhanced extends BondAI {
  private agentCoordinator: MultiAgentCoordinator;

  constructor(userId: string, config?: Partial<BondAIConfig>) {
    super(userId, config);

    // Initialize agent coordinator
    this.agentCoordinator = new MultiAgentCoordinator(
      (this as any).intelligenceEngine
    );
  }

  /**
   * Register user with their needs and offerings for agent-based matching
   */
  async registerUserForAgentMatching(
    userId: string,
    contact: Contact,
    userProfile: UserProfile
  ): Promise<void> {
    // Add contact to network
    this.addContact(contact);

    // Register with agent coordinator
    await this.agentCoordinator.registerUser(userId, contact, userProfile);

    console.log(`✓ User ${contact.name} registered for agent-based matching`);
  }

  /**
   * Find matches using agent-to-agent approach
   */
  async findAgentBasedMatches(userId: string): Promise<AgentMatchCandidate[]> {
    return await this.agentCoordinator.findAgentMatches(userId);
  }

  /**
   * Run complete agent-based matching process
   * This is where agents talk to each other and negotiate matches
   */
  async runAgentBasedMatching(
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
    return await this.agentCoordinator.runCompleteMatchingProcess(
      userId,
      maxNegotiations
    );
  }

  /**
   * Negotiate specific match using agent-to-agent conversation
   */
  async negotiateMatch(candidate: AgentMatchCandidate): Promise<NegotiationOutcome> {
    return await this.agentCoordinator.negotiateMatch(candidate);
  }

  /**
   * Get agent-based match history
   */
  getAgentMatchHistory(userId: string): AgentMatchCandidate[] {
    return this.agentCoordinator.getMatchHistory(userId);
  }

  /**
   * Get agreements history
   */
  getAgreements(userId: string): Agreement[] {
    return this.agentCoordinator.getAgreementHistory(userId);
  }

  /**
   * Get all platform agreements
   */
  getAllAgreements(): Agreement[] {
    return this.agentCoordinator.getAllAgreements();
  }

  /**
   * Get enhanced analytics including agent-based matching
   */
  getEnhancedAnalytics() {
    const baseAnalytics = this.getAnalytics();
    const agentStats = this.agentCoordinator.getPlatformStatistics();

    return {
      ...baseAnalytics,
      agentBased: {
        totalUsers: agentStats.totalUsers,
        totalMatches: agentStats.totalMatches,
        totalNegotiations: agentStats.totalNegotiations,
        totalAgreements: agentStats.totalAgreements,
        successRate: agentStats.successRate,
        averageMatchScore: agentStats.averageMatchScore,
        agreementsByDomain: agentStats.agreementsByDomain
      }
    };
  }

  /**
   * Get top performing users
   */
  getTopPerformers(limit: number = 5) {
    return this.agentCoordinator.getTopPerformers(limit);
  }
}

// Export enhanced version
export default BondAI_Enhanced;
