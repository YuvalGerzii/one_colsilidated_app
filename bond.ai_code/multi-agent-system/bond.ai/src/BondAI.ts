/**
 * Bond.AI - Main Coordinator
 * AI-Powered Connection Intelligence Platform
 *
 * Orchestrates all components:
 * - Network Mapping
 * - Intelligence Analysis
 * - Smart Matching
 * - Introduction Facilitation
 */

import { NetworkMapper } from './network/NetworkMapper';
import { IntelligenceEngine } from './intelligence/IntelligenceEngine';
import { MatchingEngine } from './matching/MatchingEngine';
import { IntroductionFacilitator } from './activation/IntroductionFacilitator';
import {
  Contact,
  Connection,
  Match,
  Introduction,
  BondAIConfig,
  NetworkSource,
  MatchStatus,
  IntroductionStatus,
  Priority
} from './types';

export class BondAI {
  private networkMapper: NetworkMapper;
  private intelligenceEngine: IntelligenceEngine;
  private matchingEngine: MatchingEngine;
  private introductionFacilitator: IntroductionFacilitator;
  private config: BondAIConfig;
  private userId: string;

  constructor(userId: string, config?: Partial<BondAIConfig>) {
    this.userId = userId;
    this.config = this.initializeConfig(config);

    // Initialize all components
    this.networkMapper = new NetworkMapper(userId);
    this.intelligenceEngine = new IntelligenceEngine(this.config.intelligenceConfig);
    this.matchingEngine = new MatchingEngine(
      this.networkMapper,
      this.intelligenceEngine,
      {
        minCompatibilityScore: this.config.minCompatibilityScore,
        minSuccessProbability: 0.5,
        enabledMatchTypes: this.config.enabledMatchTypes,
        priorityWeights: this.config.priorityWeights
      }
    );
    this.introductionFacilitator = new IntroductionFacilitator(
      this.networkMapper,
      this.intelligenceEngine
    );
  }

  /**
   * Initialize configuration with defaults
   */
  private initializeConfig(config?: Partial<BondAIConfig>): BondAIConfig {
    return {
      maxDegreeOfSeparation: config?.maxDegreeOfSeparation ?? 3,
      minRelationshipStrength: config?.minRelationshipStrength ?? 0.3,
      minCompatibilityScore: config?.minCompatibilityScore ?? 0.6,
      enabledMatchTypes: config?.enabledMatchTypes ?? [
        'complementary_needs',
        'skill_match',
        'industry_synergy',
        'mutual_interest',
        'business_opportunity',
        'knowledge_exchange',
        'collaboration'
      ] as any,
      priorityWeights: config?.priorityWeights ?? {
        valuePotential: 0.35,
        successProbability: 0.25,
        trustLevel: 0.25,
        timing: 0.15
      },
      intelligenceConfig: config?.intelligenceConfig ?? {
        enableNeedsInference: true,
        enablePersonalityAnalysis: true,
        enableBehavioralPrediction: true
      }
    };
  }

  // ==========================================
  // Network Building & Management
  // ==========================================

  /**
   * Import contacts from a source
   */
  async importContacts(source: NetworkSource): Promise<{
    contactsImported: number;
    connectionsCreated: number;
  }> {
    return await this.networkMapper.importFromSource(source);
  }

  /**
   * Add a contact manually
   */
  addContact(contact: Contact): void {
    this.networkMapper.addContact(contact);
  }

  /**
   * Add a connection between contacts
   */
  addConnection(connection: Connection): void {
    this.networkMapper.addConnection(connection);
  }

  /**
   * Get network statistics
   */
  getNetworkStats(): any {
    return this.networkMapper.getNetworkStats();
  }

  /**
   * Build complete network graph
   */
  buildNetwork(): void {
    this.networkMapper.buildNetworkGraph(this.config.maxDegreeOfSeparation);
  }

  /**
   * Get contacts by degree of separation
   */
  getContactsByDegree(degree: number): Contact[] {
    return this.networkMapper.getContactsByDegree(degree);
  }

  /**
   * Get all contacts
   */
  getAllContacts(): Contact[] {
    return this.networkMapper.getAllContacts();
  }

  /**
   * Get contact by ID
   */
  getContact(contactId: string): Contact | undefined {
    return this.networkMapper.getContact(contactId);
  }

  // ==========================================
  // Intelligence & Analysis
  // ==========================================

  /**
   * Analyze a contact's profile
   */
  async analyzeContact(contactId: string): Promise<any> {
    const contact = this.networkMapper.getContact(contactId);
    if (!contact) {
      throw new Error('Contact not found');
    }

    return await this.intelligenceEngine.analyzeContact(contact);
  }

  /**
   * Calculate compatibility between two contacts
   */
  async calculateCompatibility(contact1Id: string, contact2Id: string): Promise<any> {
    const contact1 = this.networkMapper.getContact(contact1Id);
    const contact2 = this.networkMapper.getContact(contact2Id);

    if (!contact1 || !contact2) {
      throw new Error('One or both contacts not found');
    }

    const analysis1 = await this.intelligenceEngine.analyzeContact(contact1);
    const analysis2 = await this.intelligenceEngine.analyzeContact(contact2);

    return this.intelligenceEngine.calculateCompatibility(
      contact1,
      analysis1,
      contact2,
      analysis2
    );
  }

  // ==========================================
  // Smart Matching
  // ==========================================

  /**
   * Find all matches in the network
   */
  async discoverMatches(): Promise<Match[]> {
    return await this.matchingEngine.findAllMatches();
  }

  /**
   * Find matches for a specific contact
   */
  async findMatchesFor(contactId: string): Promise<Match[]> {
    const contact = this.networkMapper.getContact(contactId);
    if (!contact) {
      throw new Error('Contact not found');
    }

    return await this.matchingEngine.findMatches(contact);
  }

  /**
   * Get top priority matches
   */
  getTopMatches(limit: number = 10): Match[] {
    return this.matchingEngine.getTopMatches(limit);
  }

  /**
   * Get matches by priority level
   */
  getMatchesByPriority(priority: Priority): Match[] {
    return this.matchingEngine.getMatchesByPriority(priority);
  }

  /**
   * Get matches by status
   */
  getMatchesByStatus(status: MatchStatus): Match[] {
    return this.matchingEngine.getMatchesByStatus(status);
  }

  /**
   * Get critical matches (highest value opportunities)
   */
  getCriticalMatches(): Match[] {
    return this.getMatchesByPriority(Priority.CRITICAL);
  }

  /**
   * Update match status
   */
  updateMatchStatus(matchId: string, status: MatchStatus): void {
    this.matchingEngine.updateMatchStatus(matchId, status);
  }

  // ==========================================
  // Introduction & Facilitation
  // ==========================================

  /**
   * Create an introduction for a match
   */
  async createIntroduction(matchId: string): Promise<Introduction> {
    const match = this.matchingEngine.getMatch(matchId);
    if (!match) {
      throw new Error('Match not found');
    }

    const introduction = await this.introductionFacilitator.createIntroduction(match);

    // Update match status
    this.matchingEngine.updateMatchStatus(matchId, MatchStatus.INTRODUCTION_REQUESTED);

    return introduction;
  }

  /**
   * Request approval for an introduction
   */
  async requestIntroductionApproval(introductionId: string): Promise<void> {
    await this.introductionFacilitator.requestApproval(introductionId);
  }

  /**
   * Approve and send an introduction
   */
  async sendIntroduction(introductionId: string): Promise<void> {
    await this.introductionFacilitator.approveAndSend(introductionId);

    // Update related match status
    const intro = this.introductionFacilitator.getIntroduction(introductionId);
    if (intro) {
      this.matchingEngine.updateMatchStatus(
        intro.match.id,
        MatchStatus.INTRODUCTION_MADE
      );
    }
  }

  /**
   * Accept an introduction
   */
  acceptIntroduction(introductionId: string): void {
    this.introductionFacilitator.acceptIntroduction(introductionId);

    // Update match status
    const intro = this.introductionFacilitator.getIntroduction(introductionId);
    if (intro) {
      this.matchingEngine.updateMatchStatus(intro.match.id, MatchStatus.ENGAGED);
    }
  }

  /**
   * Decline an introduction
   */
  declineIntroduction(introductionId: string): void {
    this.introductionFacilitator.declineIntroduction(introductionId);
  }

  /**
   * Complete an introduction
   */
  completeIntroduction(introductionId: string): void {
    this.introductionFacilitator.completeIntroduction(introductionId);

    // Update match status
    const intro = this.introductionFacilitator.getIntroduction(introductionId);
    if (intro) {
      this.matchingEngine.updateMatchStatus(intro.match.id, MatchStatus.COMPLETED);
    }
  }

  /**
   * Record an interaction
   */
  recordInteraction(
    introduceeId: string,
    targetId: string,
    note?: string
  ): void {
    this.introductionFacilitator.recordInteraction(introduceeId, targetId, note);
  }

  /**
   * Record business value from a relationship
   */
  recordBusinessValue(
    introduceeId: string,
    targetId: string,
    value: number,
    note?: string
  ): void {
    this.introductionFacilitator.recordBusinessValue(
      introduceeId,
      targetId,
      value,
      note
    );
  }

  /**
   * Get relationship metrics
   */
  getRelationshipMetrics(introduceeId: string, targetId: string): any {
    return this.introductionFacilitator.getRelationshipMetrics(
      introduceeId,
      targetId
    );
  }

  /**
   * Get introductions by status
   */
  getIntroductionsByStatus(status: IntroductionStatus): Introduction[] {
    return this.introductionFacilitator.getIntroductionsByStatus(status);
  }

  /**
   * Get all introductions
   */
  getAllIntroductions(): Introduction[] {
    return this.introductionFacilitator.getAllIntroductions();
  }

  // ==========================================
  // Analytics & Reporting
  // ==========================================

  /**
   * Get comprehensive platform analytics
   */
  getAnalytics(): {
    network: any;
    matches: any;
    introductions: any;
  } {
    const networkStats = this.networkMapper.getNetworkStats();
    const matches = this.matchingEngine.getAllMatches();
    const introStats = this.introductionFacilitator.getSuccessMetrics();

    return {
      network: {
        ...networkStats,
        reach: this.calculateNetworkReach()
      },
      matches: {
        total: matches.length,
        byPriority: {
          critical: this.getMatchesByPriority(Priority.CRITICAL).length,
          high: this.getMatchesByPriority(Priority.HIGH).length,
          medium: this.getMatchesByPriority(Priority.MEDIUM).length,
          low: this.getMatchesByPriority(Priority.LOW).length
        },
        byStatus: {
          new: this.getMatchesByStatus(MatchStatus.NEW).length,
          reviewed: this.getMatchesByStatus(MatchStatus.REVIEWED).length,
          introductionRequested: this.getMatchesByStatus(MatchStatus.INTRODUCTION_REQUESTED).length,
          introductionMade: this.getMatchesByStatus(MatchStatus.INTRODUCTION_MADE).length,
          engaged: this.getMatchesByStatus(MatchStatus.ENGAGED).length,
          completed: this.getMatchesByStatus(MatchStatus.COMPLETED).length
        },
        averageCompatibility: this.calculateAverageCompatibility(matches),
        totalValuePotential: this.calculateTotalValuePotential(matches)
      },
      introductions: introStats
    };
  }

  /**
   * Get ROI metrics
   */
  getROI(): {
    totalIntroductions: number;
    successfulConnections: number;
    businessValueGenerated: number;
    averageValuePerIntroduction: number;
    networkGrowthRate: number;
  } {
    const introStats = this.introductionFacilitator.getSuccessMetrics();

    return {
      totalIntroductions: introStats.totalIntroductions,
      successfulConnections: Math.floor(
        introStats.totalIntroductions * introStats.successRate
      ),
      businessValueGenerated: introStats.businessValueGenerated,
      averageValuePerIntroduction:
        introStats.totalIntroductions > 0
          ? introStats.businessValueGenerated / introStats.totalIntroductions
          : 0,
      networkGrowthRate: this.calculateNetworkGrowthRate()
    };
  }

  /**
   * Get dashboard summary
   */
  getDashboard(): {
    networkSize: number;
    totalReach: number;
    activeMatches: number;
    criticalOpportunities: number;
    pendingIntroductions: number;
    activeRelationships: number;
    businessValue: number;
  } {
    const networkStats = this.networkMapper.getNetworkStats();
    const introStats = this.introductionFacilitator.getSuccessMetrics();

    return {
      networkSize: networkStats.totalContacts,
      totalReach: this.calculateNetworkReach(),
      activeMatches: this.getMatchesByStatus(MatchStatus.NEW).length,
      criticalOpportunities: this.getMatchesByPriority(Priority.CRITICAL).length,
      pendingIntroductions: this.getIntroductionsByStatus(
        IntroductionStatus.PENDING_APPROVAL
      ).length,
      activeRelationships: introStats.activeRelationships,
      businessValue: introStats.businessValueGenerated
    };
  }

  // ==========================================
  // Helper Methods
  // ==========================================

  /**
   * Calculate total network reach
   */
  private calculateNetworkReach(): number {
    const stats = this.networkMapper.getNetworkStats();
    return Object.values(stats.contactsByDegree).reduce(
      (sum: number, count: number) => sum + count,
      0
    );
  }

  /**
   * Calculate average compatibility across matches
   */
  private calculateAverageCompatibility(matches: Match[]): number {
    if (matches.length === 0) return 0;

    const total = matches.reduce((sum, m) => sum + m.compatibilityScore, 0);
    return total / matches.length;
  }

  /**
   * Calculate total value potential
   */
  private calculateTotalValuePotential(matches: Match[]): number {
    return matches.reduce((sum, m) => sum + m.valuePotential, 0);
  }

  /**
   * Calculate network growth rate
   */
  private calculateNetworkGrowthRate(): number {
    // Placeholder - would calculate based on historical data
    return 0.15; // 15% growth
  }

  /**
   * Get configuration
   */
  getConfig(): BondAIConfig {
    return { ...this.config };
  }

  /**
   * Update configuration
   */
  updateConfig(config: Partial<BondAIConfig>): void {
    this.config = { ...this.config, ...config };

    // Update component configs
    // Note: In production, would need to reinitialize components or update their configs
  }
}

// Export main class and types
export * from './types';
export { NetworkMapper } from './network/NetworkMapper';
export { IntelligenceEngine } from './intelligence/IntelligenceEngine';
export { MatchingEngine } from './matching/MatchingEngine';
export { IntroductionFacilitator } from './activation/IntroductionFacilitator';
