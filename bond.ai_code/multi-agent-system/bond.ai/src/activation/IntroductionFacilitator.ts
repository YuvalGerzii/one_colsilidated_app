/**
 * Activation & Facilitation Module
 * Warm introduction protocols through mutual connections
 * Conversation starters and context provision
 * Relationship tracking and success measurement
 */

import {
  Match,
  Introduction,
  IntroductionStatus,
  Contact,
  IntelligenceAnalysis
} from '../types';
import { NetworkMapper } from '../network/NetworkMapper';
import { IntelligenceEngine } from '../intelligence/IntelligenceEngine';

export class IntroductionFacilitator {
  private networkMapper: NetworkMapper;
  private intelligenceEngine: IntelligenceEngine;
  private introductions: Map<string, Introduction>;
  private relationshipMetrics: Map<string, RelationshipMetrics>;

  constructor(
    networkMapper: NetworkMapper,
    intelligenceEngine: IntelligenceEngine
  ) {
    this.networkMapper = networkMapper;
    this.intelligenceEngine = intelligenceEngine;
    this.introductions = new Map();
    this.relationshipMetrics = new Map();
  }

  /**
   * Create a warm introduction for a match
   */
  async createIntroduction(match: Match): Promise<Introduction> {
    // Find the best introducer (mutual connection)
    const introducer = this.findBestIntroducer(match);

    if (!introducer) {
      throw new Error('No suitable introducer found for this match');
    }

    // Get intelligence analyses
    const sourceAnalysis = await this.intelligenceEngine.analyzeContact(match.sourceContact);
    const targetAnalysis = await this.intelligenceEngine.analyzeContact(match.targetContact);

    // Generate introduction message
    const message = this.generateIntroductionMessage(
      match,
      introducer,
      sourceAnalysis,
      targetAnalysis
    );

    // Generate conversation starters
    const conversationStarters = this.generateConversationStarters(
      match,
      sourceAnalysis,
      targetAnalysis
    );

    // Generate context
    const context = this.generateContext(match, sourceAnalysis, targetAnalysis);

    const introduction: Introduction = {
      id: `intro-${match.id}-${Date.now()}`,
      match,
      introducerContact: introducer,
      introduceeContact: match.sourceContact,
      targetContact: match.targetContact,
      message,
      conversationStarters,
      context,
      status: IntroductionStatus.DRAFT,
      createdAt: new Date()
    };

    this.introductions.set(introduction.id, introduction);

    return introduction;
  }

  /**
   * Find the best introducer from the connection path
   */
  private findBestIntroducer(match: Match): Contact | null {
    const shortestPath = match.shortestPath;

    if (shortestPath.contacts.length < 2) {
      return null; // No intermediary
    }

    // The best introducer is typically the contact closest to the source
    // with the strongest relationship to both parties
    if (shortestPath.contacts.length === 2) {
      // Direct path: source -> target (shouldn't happen in matches)
      return null;
    }

    // For 3-hop path: source -> introducer -> target
    // Return the middle contact
    const introducerIndex = 1;
    return shortestPath.contacts[introducerIndex];
  }

  /**
   * Generate personalized introduction message
   */
  private generateIntroductionMessage(
    match: Match,
    introducer: Contact,
    sourceAnalysis: IntelligenceAnalysis,
    targetAnalysis: IntelligenceAnalysis
  ): string {
    const source = match.sourceContact;
    const target = match.targetContact;

    // Get primary match reason
    const primaryReason = match.reasons[0];

    const message = `Hi ${target.name},

I wanted to introduce you to ${source.name}${source.title ? `, ${source.title}` : ''}${source.company ? ` at ${source.company}` : ''}.

I think you two would really benefit from connecting because:

${this.formatMatchReasons(match.reasons)}

${source.name} is particularly interested in ${this.getInterestSummary(sourceAnalysis)}, and I know you have expertise in ${this.getExpertiseSummary(targetAnalysis)}.

I believe there could be great synergy here, especially around ${this.getSynergyArea(match, sourceAnalysis, targetAnalysis)}.

Would you be open to a brief conversation? I'm happy to facilitate an introduction call if that's helpful.

Best regards,
${introducer.name}`;

    return message;
  }

  /**
   * Generate conversation starters
   */
  private generateConversationStarters(
    match: Match,
    sourceAnalysis: IntelligenceAnalysis,
    targetAnalysis: IntelligenceAnalysis
  ): string[] {
    const starters: string[] = [];

    // Based on match type
    if (match.matchType === 'complementary_needs') {
      starters.push(
        `I noticed you're working on ${this.getRecentActivity(targetAnalysis)}. I'd love to hear more about that.`,
        `I'm currently exploring ${this.getRecentActivity(sourceAnalysis)} and thought we might have complementary interests.`
      );
    }

    if (match.matchType === 'industry_synergy') {
      starters.push(
        `What's your take on the recent developments in ${targetAnalysis.profileAnalysis.industries[0]}?`,
        `I've been following trends in our industry and would value your perspective.`
      );
    }

    if (match.matchType === 'skill_match') {
      starters.push(
        `I saw your expertise in ${targetAnalysis.profileAnalysis.expertiseAreas[0]} and would love to learn from your experience.`,
        `I've been working with ${sourceAnalysis.profileAnalysis.expertiseAreas[0]} and thought we could share insights.`
      );
    }

    // Add mutual interest starters
    const commonInterests = this.findCommonInterests(
      match.sourceContact,
      match.targetContact
    );

    if (commonInterests.length > 0) {
      starters.push(
        `I noticed we both share an interest in ${commonInterests[0]}. How did you get started with that?`
      );
    }

    // Add generic professional starters
    starters.push(
      `What are you currently most excited about in your work?`,
      `I'd be curious to hear about the challenges you're tackling right now.`,
      `What projects are you focusing on these days?`
    );

    return starters.slice(0, 5); // Return top 5
  }

  /**
   * Generate context for the introduction
   */
  private generateContext(
    match: Match,
    sourceAnalysis: IntelligenceAnalysis,
    targetAnalysis: IntelligenceAnalysis
  ): string {
    const contextParts: string[] = [];

    contextParts.push(`Match Quality: ${(match.overallScore * 100).toFixed(0)}% compatibility`);
    contextParts.push(`Connection Strength: ${(match.shortestPath.trustScore * 100).toFixed(0)}% trust level`);
    contextParts.push(`Success Probability: ${(match.successProbability * 100).toFixed(0)}%`);

    // Add key insights
    contextParts.push('\nKey Insights:');

    for (const reason of match.reasons.slice(0, 3)) {
      contextParts.push(`• ${reason.description} (${(reason.score * 100).toFixed(0)}% match)`);
    }

    // Add complementary strengths
    contextParts.push('\nComplementary Strengths:');
    contextParts.push(`• ${match.sourceContact.name}: ${sourceAnalysis.profileAnalysis.expertiseAreas.slice(0, 3).join(', ')}`);
    contextParts.push(`• ${match.targetContact.name}: ${targetAnalysis.profileAnalysis.expertiseAreas.slice(0, 3).join(', ')}`);

    return contextParts.join('\n');
  }

  /**
   * Request approval for an introduction
   */
  async requestApproval(introductionId: string): Promise<void> {
    const intro = this.introductions.get(introductionId);
    if (!intro) {
      throw new Error('Introduction not found');
    }

    intro.status = IntroductionStatus.PENDING_APPROVAL;
  }

  /**
   * Approve and send an introduction
   */
  async approveAndSend(introductionId: string): Promise<void> {
    const intro = this.introductions.get(introductionId);
    if (!intro) {
      throw new Error('Introduction not found');
    }

    // In a real implementation, this would send the actual introduction
    // via email, LinkedIn, etc.

    intro.status = IntroductionStatus.SENT;
    intro.sentAt = new Date();

    // Initialize relationship tracking
    this.initializeRelationshipTracking(intro);
  }

  /**
   * Mark introduction as accepted
   */
  acceptIntroduction(introductionId: string): void {
    const intro = this.introductions.get(introductionId);
    if (!intro) {
      throw new Error('Introduction not found');
    }

    intro.status = IntroductionStatus.ACCEPTED;
    intro.respondedAt = new Date();
  }

  /**
   * Mark introduction as declined
   */
  declineIntroduction(introductionId: string): void {
    const intro = this.introductions.get(introductionId);
    if (!intro) {
      throw new Error('Introduction not found');
    }

    intro.status = IntroductionStatus.DECLINED;
    intro.respondedAt = new Date();
  }

  /**
   * Mark introduction as completed
   */
  completeIntroduction(introductionId: string): void {
    const intro = this.introductions.get(introductionId);
    if (!intro) {
      throw new Error('Introduction not found');
    }

    intro.status = IntroductionStatus.COMPLETED;

    // Update relationship metrics
    this.updateRelationshipMetrics(intro, 'completed');
  }

  /**
   * Initialize relationship tracking
   */
  private initializeRelationshipTracking(intro: Introduction): void {
    const key = `${intro.introduceeContact.id}-${intro.targetContact.id}`;

    this.relationshipMetrics.set(key, {
      introductionId: intro.id,
      introduceeId: intro.introduceeContact.id,
      targetId: intro.targetContact.id,
      startDate: new Date(),
      status: 'active',
      interactionCount: 0,
      lastInteraction: new Date(),
      relationshipStrength: 0.3, // Initial strength
      businessValue: 0,
      notes: []
    });
  }

  /**
   * Update relationship metrics
   */
  private updateRelationshipMetrics(
    intro: Introduction,
    event: 'completed' | 'interaction' | 'business_value'
  ): void {
    const key = `${intro.introduceeContact.id}-${intro.targetContact.id}`;
    const metrics = this.relationshipMetrics.get(key);

    if (!metrics) return;

    switch (event) {
      case 'completed':
        metrics.status = 'completed';
        metrics.relationshipStrength += 0.2;
        break;
      case 'interaction':
        metrics.interactionCount++;
        metrics.lastInteraction = new Date();
        metrics.relationshipStrength = Math.min(metrics.relationshipStrength + 0.05, 1);
        break;
      case 'business_value':
        metrics.businessValue += 1;
        metrics.relationshipStrength = Math.min(metrics.relationshipStrength + 0.1, 1);
        break;
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
    const key = `${introduceeId}-${targetId}`;
    const metrics = this.relationshipMetrics.get(key);

    if (!metrics) return;

    metrics.interactionCount++;
    metrics.lastInteraction = new Date();
    metrics.relationshipStrength = Math.min(metrics.relationshipStrength + 0.05, 1);

    if (note) {
      metrics.notes.push({
        date: new Date(),
        note
      });
    }
  }

  /**
   * Record business value
   */
  recordBusinessValue(
    introduceeId: string,
    targetId: string,
    value: number,
    note?: string
  ): void {
    const key = `${introduceeId}-${targetId}`;
    const metrics = this.relationshipMetrics.get(key);

    if (!metrics) return;

    metrics.businessValue += value;
    metrics.relationshipStrength = Math.min(metrics.relationshipStrength + 0.1, 1);

    if (note) {
      metrics.notes.push({
        date: new Date(),
        note: `Business value: $${value} - ${note}`
      });
    }
  }

  /**
   * Get relationship metrics
   */
  getRelationshipMetrics(
    introduceeId: string,
    targetId: string
  ): RelationshipMetrics | undefined {
    const key = `${introduceeId}-${targetId}`;
    return this.relationshipMetrics.get(key);
  }

  /**
   * Get introduction success metrics
   */
  getSuccessMetrics(): {
    totalIntroductions: number;
    successRate: number;
    averageResponseTime: number;
    businessValueGenerated: number;
    activeRelationships: number;
  } {
    const intros = Array.from(this.introductions.values());
    const metrics = Array.from(this.relationshipMetrics.values());

    const sentIntros = intros.filter(i => i.sentAt);
    const acceptedIntros = intros.filter(i => i.status === IntroductionStatus.ACCEPTED);

    const responseTimes = intros
      .filter(i => i.sentAt && i.respondedAt)
      .map(i => i.respondedAt!.getTime() - i.sentAt!.getTime());

    const avgResponseTime = responseTimes.length > 0
      ? responseTimes.reduce((sum, t) => sum + t, 0) / responseTimes.length / (1000 * 60 * 60 * 24)
      : 0;

    const totalBusinessValue = metrics.reduce((sum, m) => sum + m.businessValue, 0);
    const activeRelationships = metrics.filter(m => m.status === 'active').length;

    return {
      totalIntroductions: sentIntros.length,
      successRate: sentIntros.length > 0 ? acceptedIntros.length / sentIntros.length : 0,
      averageResponseTime: avgResponseTime,
      businessValueGenerated: totalBusinessValue,
      activeRelationships
    };
  }

  /**
   * Get introduction by ID
   */
  getIntroduction(introductionId: string): Introduction | undefined {
    return this.introductions.get(introductionId);
  }

  /**
   * Get all introductions
   */
  getAllIntroductions(): Introduction[] {
    return Array.from(this.introductions.values());
  }

  /**
   * Get introductions by status
   */
  getIntroductionsByStatus(status: IntroductionStatus): Introduction[] {
    return Array.from(this.introductions.values())
      .filter(i => i.status === status);
  }

  /**
   * Helper: Format match reasons
   */
  private formatMatchReasons(reasons: any[]): string {
    return reasons
      .slice(0, 3)
      .map((r, i) => `${i + 1}. ${r.description}`)
      .join('\n');
  }

  /**
   * Helper: Get interest summary
   */
  private getInterestSummary(analysis: IntelligenceAnalysis): string {
    const interests = [
      ...analysis.needsAnalysis.explicit,
      ...analysis.profileAnalysis.expertiseAreas
    ];
    return interests.slice(0, 2).join(' and ') || 'professional development';
  }

  /**
   * Helper: Get expertise summary
   */
  private getExpertiseSummary(analysis: IntelligenceAnalysis): string {
    return analysis.profileAnalysis.expertiseAreas.slice(0, 2).join(' and ') || 'this area';
  }

  /**
   * Helper: Get synergy area
   */
  private getSynergyArea(
    match: Match,
    sourceAnalysis: IntelligenceAnalysis,
    targetAnalysis: IntelligenceAnalysis
  ): string {
    if (match.reasons.length > 0) {
      return match.reasons[0].type.replace(/_/g, ' ');
    }
    return 'mutual professional development';
  }

  /**
   * Helper: Get recent activity
   */
  private getRecentActivity(analysis: IntelligenceAnalysis): string {
    if (analysis.needsAnalysis.explicit.length > 0) {
      return analysis.needsAnalysis.explicit[0];
    }
    return analysis.profileAnalysis.expertiseAreas[0] || 'your current projects';
  }

  /**
   * Helper: Find common interests
   */
  private findCommonInterests(contact1: Contact, contact2: Contact): string[] {
    const interests1 = new Set(contact1.interests || []);
    const interests2 = new Set(contact2.interests || []);

    return [...interests1].filter(i => interests2.has(i));
  }
}

interface RelationshipMetrics {
  introductionId: string;
  introduceeId: string;
  targetId: string;
  startDate: Date;
  status: 'active' | 'completed' | 'inactive';
  interactionCount: number;
  lastInteraction: Date;
  relationshipStrength: number;
  businessValue: number;
  notes: Array<{
    date: Date;
    note: string;
  }>;
}
