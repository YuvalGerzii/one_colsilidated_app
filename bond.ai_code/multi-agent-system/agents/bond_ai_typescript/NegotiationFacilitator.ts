/**
 * Negotiation Facilitator
 * Coordinates agent-to-agent conversations and negotiations
 * Ensures fair, productive discussions between user representative agents
 */

import {
  AgentConversation,
  ConversationStatus,
  ConversationMessage,
  MessageType,
  ProposedTerms,
  Agreement,
  MutualBenefit,
  Benefit,
  NegotiationPoint,
  NegotiationPointStatus,
  Position,
  Resolution,
  NegotiationOutcome,
  UserRepresentativeAgent,
  TermsStatus
} from './types';

export class NegotiationFacilitator {
  private conversations: Map<string, AgentConversation>;
  private config: {
    maxRounds: number;
    timeoutMinutes: number;
    minMutualBenefit: number;
  };

  constructor(config?: {
    maxRounds?: number;
    timeoutMinutes?: number;
    minMutualBenefit?: number;
  }) {
    this.conversations = new Map();
    this.config = {
      maxRounds: config?.maxRounds ?? 10,
      timeoutMinutes: config?.timeoutMinutes ?? 30,
      minMutualBenefit: config?.minMutualBenefit ?? 0.6
    };
  }

  /**
   * Initiate a conversation between two user representative agents
   */
  async initiateConversation(
    agent1: UserRepresentativeAgent,
    agent2: UserRepresentativeAgent
  ): Promise<AgentConversation> {
    const conversationId = `conv-${agent1.id}-${agent2.id}-${Date.now()}`;

    const conversation: AgentConversation = {
      id: conversationId,
      agent1,
      agent2,
      status: ConversationStatus.INITIATED,
      messages: [],
      negotiationPoints: [],
      proposedTerms: [],
      startedAt: new Date()
    };

    this.conversations.set(conversationId, conversation);

    // Start with introductions
    const intro1 = agent1.generateIntroduction(agent2);
    const intro2 = agent2.generateIntroduction(agent1);

    conversation.messages.push(intro1, intro2);
    conversation.status = ConversationStatus.IN_PROGRESS;

    return conversation;
  }

  /**
   * Conduct full negotiation between two agents
   */
  async conductNegotiation(
    agent1: UserRepresentativeAgent,
    agent2: UserRepresentativeAgent
  ): Promise<NegotiationOutcome> {
    console.log(`\n🤝 Starting negotiation between ${agent1.name} and ${agent2.name}\n`);

    const conversation = await this.initiateConversation(agent1, agent2);
    const startTime = Date.now();

    // Phase 1: Initial proposal
    console.log('Phase 1: Initial Proposal Generation');
    const initialProposal = agent1.createProposal(agent2);
    initialProposal.timestamp = new Date();
    conversation.proposedTerms.push(initialProposal);

    this.logMessage(`${agent1.name} proposes:`, initialProposal.rationale);

    // Phase 2: Evaluation and response
    console.log('\nPhase 2: Proposal Evaluation');
    const evaluation = agent2.analyzeProposal(initialProposal);

    this.logMessage(
      `${agent2.name} evaluates:`,
      `Score: ${(evaluation.score * 100).toFixed(0)}%, Should Accept: ${evaluation.shouldAccept}`
    );

    if (evaluation.shouldAccept) {
      // Agreement reached on first proposal!
      console.log('\n✅ Agreement reached on first proposal!');
      return await this.finalizeAgreement(conversation, initialProposal, startTime);
    }

    // Phase 3: Negotiation rounds
    console.log('\nPhase 3: Negotiation Rounds');
    let currentProposal = initialProposal;
    let rounds = 0;

    while (rounds < this.config.maxRounds) {
      rounds++;
      console.log(`\n--- Round ${rounds} ---`);

      // Agent 2 counter-offers or rejects
      if (evaluation.counterOffer) {
        const counterProposal: ProposedTerms = {
          id: `proposal-${Date.now()}`,
          proposedBy: agent2.id,
          timestamp: new Date(),
          terms: evaluation.counterOffer,
          rationale: evaluation.rationale,
          status: TermsStatus.PROPOSED
        };

        conversation.proposedTerms.push(counterProposal);
        this.logMessage(`${agent2.name} counter-offers:`, counterProposal.rationale);

        // Agent 1 evaluates counter-offer
        const counterEvaluation = agent1.analyzeProposal(counterProposal);
        this.logMessage(
          `${agent1.name} evaluates counter:`,
          `Score: ${(counterEvaluation.score * 100).toFixed(0)}%`
        );

        if (counterEvaluation.shouldAccept) {
          console.log('\n✅ Agreement reached on counter-offer!');
          return await this.finalizeAgreement(conversation, counterProposal, startTime);
        }

        // Check if we're getting closer
        if (counterEvaluation.score > evaluation.score) {
          console.log('📈 Progress: Proposals converging...');

          // Try to find middle ground
          const compromiseProposal = this.generateCompromise(
            currentProposal,
            counterProposal,
            agent1,
            agent2
          );

          if (compromiseProposal) {
            conversation.proposedTerms.push(compromiseProposal);
            this.logMessage('🤝 Facilitator suggests compromise', compromiseProposal.rationale);

            // Both agents evaluate compromise
            const agent1Eval = agent1.analyzeProposal(compromiseProposal);
            const agent2Eval = agent2.analyzeProposal(compromiseProposal);

            if (agent1Eval.shouldAccept && agent2Eval.shouldAccept) {
              console.log('\n✅ Agreement reached on compromise!');
              return await this.finalizeAgreement(conversation, compromiseProposal, startTime);
            }
          }
        }

        currentProposal = counterProposal;
        evaluation = counterEvaluation;
      } else {
        // No counter-offer means rejection
        console.log('\n❌ No agreement possible - rejected without counter');
        break;
      }

      // Check timeout
      if (Date.now() - startTime > this.config.timeoutMinutes * 60 * 1000) {
        console.log('\n⏱️ Negotiation timeout');
        break;
      }
    }

    // No agreement reached
    conversation.status = ConversationStatus.NO_AGREEMENT;
    const duration = Date.now() - startTime;

    console.log('\n❌ Negotiation concluded without agreement');

    return {
      success: false,
      reason: rounds >= this.config.maxRounds
        ? 'Maximum negotiation rounds exceeded'
        : 'No mutually acceptable terms found',
      improvementSuggestions: this.generateImprovementSuggestions(conversation),
      metrics: {
        duration,
        messagesExchanged: conversation.messages.length,
        proposalsConsidered: conversation.proposedTerms.length,
        compatibilityScore: evaluation.score,
        satisfactionScore: { agent1: 0, agent2: evaluation.score }
      }
    };
  }

  /**
   * Finalize agreement and create agreement object
   */
  private async finalizeAgreement(
    conversation: AgentConversation,
    acceptedProposal: ProposedTerms,
    startTime: number
  ): Promise<NegotiationOutcome> {
    const mutualBenefit = this.calculateMutualBenefit(
      acceptedProposal,
      conversation.agent1,
      conversation.agent2
    );

    const agreement: Agreement = {
      id: `agreement-${conversation.id}`,
      conversationId: conversation.id,
      agent1: conversation.agent1,
      agent2: conversation.agent2,
      finalTerms: acceptedProposal.terms,
      compatibilityScore: mutualBenefit.overallScore,
      mutualBenefit,
      agreedAt: new Date(),
      nextSteps: this.generateNextSteps(acceptedProposal.terms),
      followUpSchedule: 'Weekly check-ins for first month'
    };

    conversation.finalAgreement = agreement;
    conversation.status = ConversationStatus.AGREEMENT_REACHED;
    conversation.completedAt = new Date();

    const duration = Date.now() - startTime;

    // Record in agent histories
    conversation.agent1.recordNegotiation({
      conversationId: conversation.id,
      otherAgentId: conversation.agent2.id,
      outcome: ConversationStatus.AGREEMENT_REACHED,
      agreement,
      duration,
      messagesExchanged: conversation.messages.length,
      learnings: ['Successful negotiation', `Mutual benefit: ${(mutualBenefit.overallScore * 100).toFixed(0)}%`],
      timestamp: new Date()
    });

    conversation.agent2.recordNegotiation({
      conversationId: conversation.id,
      otherAgentId: conversation.agent1.id,
      outcome: ConversationStatus.AGREEMENT_REACHED,
      agreement,
      duration,
      messagesExchanged: conversation.messages.length,
      learnings: ['Successful negotiation', `Mutual benefit: ${(mutualBenefit.overallScore * 100).toFixed(0)}%`],
      timestamp: new Date()
    });

    return {
      success: true,
      agreement,
      metrics: {
        duration,
        messagesExchanged: conversation.messages.length,
        proposalsConsidered: conversation.proposedTerms.length,
        compatibilityScore: mutualBenefit.overallScore,
        satisfactionScore: {
          agent1: this.calculateSatisfaction(agreement, conversation.agent1),
          agent2: this.calculateSatisfaction(agreement, conversation.agent2)
        }
      }
    };
  }

  /**
   * Calculate mutual benefit from proposal
   */
  private calculateMutualBenefit(
    proposal: ProposedTerms,
    agent1: UserRepresentativeAgent,
    agent2: UserRepresentativeAgent
  ): MutualBenefit {
    const agent1Benefits = this.calculateBenefits(
      proposal.terms.whatAgent1Gets,
      agent1
    );
    const agent2Benefits = this.calculateBenefits(
      proposal.terms.whatAgent2Gets,
      agent2
    );

    const agent1Score = agent1Benefits.reduce((sum, b) => sum + b.estimatedValue, 0) / Math.max(agent1Benefits.length, 1);
    const agent2Score = agent2Benefits.reduce((sum, b) => sum + b.estimatedValue, 0) / Math.max(agent2Benefits.length, 1);

    const overallScore = (agent1Score + agent2Score) / 2;
    const balanceScore = 1 - Math.abs(agent1Score - agent2Score); // Higher = more balanced

    return {
      agent1Benefits,
      agent2Benefits,
      overallScore,
      balanceScore
    };
  }

  /**
   * Calculate benefits for an agent
   */
  private calculateBenefits(items: string[], agent: UserRepresentativeAgent): Benefit[] {
    const benefits: Benefit[] = [];

    for (const item of items) {
      // Find matching need
      const matchingNeed = agent.userProfile.needs.find(need =>
        item.toLowerCase().includes(need.description.toLowerCase()) ||
        need.description.toLowerCase().includes(item.toLowerCase())
      );

      if (matchingNeed) {
        benefits.push({
          category: matchingNeed.category,
          description: item,
          estimatedValue: this.priorityToValue(matchingNeed.priority),
          timeToRealize: matchingNeed.urgency
        });
      } else {
        // Unknown benefit - assign moderate value
        benefits.push({
          category: 'other',
          description: item,
          estimatedValue: 0.5,
          timeToRealize: 'medium_term' as any
        });
      }
    }

    return benefits;
  }

  /**
   * Convert priority to numeric value
   */
  private priorityToValue(priority: string): number {
    const values: Record<string, number> = {
      critical: 1.0,
      high: 0.8,
      medium: 0.6,
      low: 0.4
    };
    return values[priority] || 0.5;
  }

  /**
   * Generate compromise proposal
   */
  private generateCompromise(
    proposal1: ProposedTerms,
    proposal2: ProposedTerms,
    agent1: UserRepresentativeAgent,
    agent2: UserRepresentativeAgent
  ): ProposedTerms | null {
    // Find common ground
    const commonGets1 = proposal1.terms.whatAgent1Gets.filter(item =>
      proposal2.terms.whatAgent1Gets.some(item2 =>
        item.toLowerCase() === item2.toLowerCase()
      )
    );

    const commonGets2 = proposal1.terms.whatAgent2Gets.filter(item =>
      proposal2.terms.whatAgent2Gets.some(item2 =>
        item.toLowerCase() === item2.toLowerCase()
      )
    );

    // If no common ground, can't compromise
    if (commonGets1.length === 0 && commonGets2.length === 0) {
      return null;
    }

    // Combine unique items from both proposals
    const combinedGets1 = [
      ...new Set([...proposal1.terms.whatAgent1Gets, ...proposal2.terms.whatAgent1Gets])
    ];
    const combinedGets2 = [
      ...new Set([...proposal1.terms.whatAgent2Gets, ...proposal2.terms.whatAgent2Gets])
    ];

    const combinedGives1 = [
      ...new Set([...proposal1.terms.whatAgent1Gives, ...proposal2.terms.whatAgent1Gives])
    ];
    const combinedGives2 = [
      ...new Set([...proposal1.terms.whatAgent2Gives, ...proposal2.terms.whatAgent2Gives])
    ];

    return {
      id: `compromise-${Date.now()}`,
      proposedBy: 'facilitator',
      timestamp: new Date(),
      terms: {
        whatAgent1Gets: combinedGets1,
        whatAgent1Gives: combinedGives1,
        whatAgent2Gets: combinedGets2,
        whatAgent2Gives: combinedGives2,
        conditions: [
          ...(proposal1.terms.conditions || []),
          ...(proposal2.terms.conditions || [])
        ],
        timeline: proposal1.terms.timeline,
        successMetrics: [
          ...(proposal1.terms.successMetrics || []),
          ...(proposal2.terms.successMetrics || [])
        ]
      },
      rationale: 'Compromise proposal combining elements from both parties to find mutual ground',
      status: TermsStatus.PROPOSED
    };
  }

  /**
   * Calculate satisfaction for an agent
   */
  private calculateSatisfaction(agreement: Agreement, agent: UserRepresentativeAgent): number {
    const benefits = agent.id === agreement.agent1.id
      ? agreement.mutualBenefit.agent1Benefits
      : agreement.mutualBenefit.agent2Benefits;

    const totalValue = benefits.reduce((sum, b) => sum + b.estimatedValue, 0);
    return benefits.length > 0 ? totalValue / benefits.length : 0.5;
  }

  /**
   * Generate next steps from terms
   */
  private generateNextSteps(terms: any): string[] {
    return [
      'Schedule kickoff meeting to align on objectives',
      'Define detailed timeline and milestones',
      'Set up communication channels and regular check-ins',
      'Establish success metrics and tracking methods',
      'Begin implementation of agreed terms'
    ];
  }

  /**
   * Generate improvement suggestions
   */
  private generateImprovementSuggestions(conversation: AgentConversation): string[] {
    const suggestions: string[] = [];

    if (conversation.proposedTerms.length < 3) {
      suggestions.push('More negotiation rounds could help find common ground');
    }

    if (conversation.messages.length < 5) {
      suggestions.push('More communication between parties might reveal hidden opportunities');
    }

    suggestions.push('Consider adjusting priorities or flexibility on key needs');
    suggestions.push('Explore alternative value exchange structures');

    return suggestions;
  }

  /**
   * Log formatted message
   */
  private logMessage(title: string, content: string): void {
    console.log(`\n${title}`);
    console.log(content);
  }

  /**
   * Get conversation by ID
   */
  getConversation(conversationId: string): AgentConversation | undefined {
    return this.conversations.get(conversationId);
  }

  /**
   * Get all conversations
   */
  getAllConversations(): AgentConversation[] {
    return Array.from(this.conversations.values());
  }

  /**
   * Get conversations by status
   */
  getConversationsByStatus(status: ConversationStatus): AgentConversation[] {
    return Array.from(this.conversations.values())
      .filter(c => c.status === status);
  }

  /**
   * Get success rate
   */
  getSuccessRate(): number {
    const total = this.conversations.size;
    if (total === 0) return 0;

    const successful = Array.from(this.conversations.values())
      .filter(c => c.status === ConversationStatus.AGREEMENT_REACHED)
      .length;

    return successful / total;
  }

  /**
   * Get average negotiation duration
   */
  getAverageNegotiationDuration(): number {
    const completed = Array.from(this.conversations.values())
      .filter(c => c.completedAt);

    if (completed.length === 0) return 0;

    const totalDuration = completed.reduce((sum, c) => {
      return sum + (c.completedAt!.getTime() - c.startedAt.getTime());
    }, 0);

    return totalDuration / completed.length;
  }
}
