/**
 * Advanced Conversation Intelligence System
 *
 * Enhances agent-to-agent conversations with:
 * - Natural language generation
 * - Strategic communication
 * - Persuasion techniques
 * - Context-aware messaging
 * - Relationship building
 * - Argumentation and framing
 */

import {
  ConversationMessage,
  MessageType,
  ProposedTerms,
  UserRepresentativeAgent,
  NegotiationStyle,
  Position,
  Priority
} from './types';

export interface ConversationContext {
  negotiationStage: 'opening' | 'exploration' | 'proposal' | 'negotiation' | 'closing';
  relationshipLevel: 'initial' | 'building' | 'established' | 'strong';
  tensionLevel: number; // 0-1, how contentious the negotiation is
  progressDirection: 'converging' | 'diverging' | 'stalled';
  roundNumber: number;
  priorAgreements: number; // With this agent
}

export interface MessageStrategy {
  primaryGoal: 'build_rapport' | 'persuade' | 'clarify' | 'concede' | 'stand_firm' | 'explore';
  tone: 'friendly' | 'professional' | 'assertive' | 'collaborative' | 'cautious';
  framingApproach: 'win-win' | 'value_creation' | 'problem_solving' | 'opportunity_focused';
  persuasionTechniques: PersuasionTechnique[];
}

export interface PersuasionTechnique {
  name: string;
  description: string;
  whenToUse: string;
  example: string;
}

export class ConversationIntelligenceEngine {
  /**
   * Generate strategic, natural language message
   */
  generateStrategicMessage(
    agent: UserRepresentativeAgent,
    recipient: UserRepresentativeAgent,
    messageType: MessageType,
    context: ConversationContext,
    content: {
      proposal?: ProposedTerms;
      concerns?: string[];
      points?: string[];
      previousMessage?: ConversationMessage;
    }
  ): ConversationMessage {
    const strategy = this.determineMessageStrategy(agent, recipient, context, messageType);
    const messageContent = this.craftStrategicMessage(
      agent,
      recipient,
      messageType,
      context,
      strategy,
      content
    );

    return {
      id: `msg-${Date.now()}-${messageType}`,
      from: agent.id,
      to: recipient.id,
      timestamp: new Date(),
      messageType,
      content: messageContent,
      sentiment: this.calculateMessageSentiment(strategy, context),
      structuredData: {
        strategy,
        context
      }
    };
  }

  /**
   * Determine optimal message strategy
   */
  private determineMessageStrategy(
    agent: UserRepresentativeAgent,
    recipient: UserRepresentativeAgent,
    context: ConversationContext,
    messageType: MessageType
  ): MessageStrategy {
    const strategy: MessageStrategy = {
      primaryGoal: 'build_rapport',
      tone: 'professional',
      framingApproach: 'win-win',
      persuasionTechniques: []
    };

    // Determine primary goal based on stage and message type
    switch (context.negotiationStage) {
      case 'opening':
        strategy.primaryGoal = 'build_rapport';
        strategy.tone = 'friendly';
        break;

      case 'exploration':
        strategy.primaryGoal = 'explore';
        strategy.tone = 'collaborative';
        break;

      case 'proposal':
      case 'negotiation':
        if (messageType === MessageType.PROPOSAL) {
          strategy.primaryGoal = 'persuade';
          strategy.tone = 'professional';
        } else if (messageType === MessageType.COUNTER_PROPOSAL) {
          strategy.primaryGoal = context.tensionLevel > 0.6 ? 'stand_firm' : 'persuade';
          strategy.tone = context.tensionLevel > 0.6 ? 'assertive' : 'collaborative';
        } else if (messageType === MessageType.QUESTION || messageType === MessageType.CLARIFICATION) {
          strategy.primaryGoal = 'clarify';
          strategy.tone = 'professional';
        }
        break;

      case 'closing':
        strategy.primaryGoal = context.progressDirection === 'converging' ? 'concede' : 'stand_firm';
        strategy.tone = 'professional';
        break;
    }

    // Adjust based on negotiation style
    strategy.persuasionTechniques = this.selectPersuasionTechniques(
      agent.config.negotiationStyle,
      strategy.primaryGoal,
      context
    );

    // Adjust framing based on relationship
    if (context.relationshipLevel === 'strong' || context.priorAgreements > 0) {
      strategy.framingApproach = 'win-win';
    } else if (agent.config.negotiationStyle === NegotiationStyle.COLLABORATIVE) {
      strategy.framingApproach = 'value_creation';
    }

    return strategy;
  }

  /**
   * Select appropriate persuasion techniques
   */
  private selectPersuasionTechniques(
    negotiationStyle: NegotiationStyle,
    goal: MessageStrategy['primaryGoal'],
    context: ConversationContext
  ): PersuasionTechnique[] {
    const techniques: PersuasionTechnique[] = [];

    const allTechniques: Record<string, PersuasionTechnique> = {
      reciprocity: {
        name: 'Reciprocity',
        description: 'Offer something valuable first to create obligation',
        whenToUse: 'When building rapport or making initial proposals',
        example: 'We\'re prepared to commit our resources first to demonstrate good faith'
      },
      scarcity: {
        name: 'Scarcity',
        description: 'Emphasize limited availability or time-sensitivity',
        whenToUse: 'When you have unique offerings or urgent timeline',
        example: 'This opportunity is time-sensitive given our current capacity'
      },
      socialProof: {
        name: 'Social Proof',
        description: 'Reference similar successful partnerships',
        whenToUse: 'When you have relevant track record',
        example: 'We\'ve successfully partnered with similar organizations'
      },
      authority: {
        name: 'Authority',
        description: 'Demonstrate expertise and credibility',
        whenToUse: 'When your expertise is relevant',
        example: 'With our 10 years of experience in this domain...'
      },
      consistency: {
        name: 'Consistency',
        description: 'Reference previous agreements or stated positions',
        whenToUse: 'When building on prior commitments',
        example: 'As we discussed earlier, this aligns with your stated goals'
      },
      liking: {
        name: 'Liking',
        description: 'Find common ground and build rapport',
        whenToUse: 'Early stages of negotiation',
        example: 'We share similar values around innovation and quality'
      },
      anchoringBias: {
        name: 'Anchoring',
        description: 'Set initial reference point strategically',
        whenToUse: 'When making first proposal',
        example: 'Starting from industry standard benchmarks'
      },
      framing: {
        name: 'Framing',
        description: 'Present information in favorable context',
        whenToUse: 'When presenting proposals or counters',
        example: 'This represents a 30% improvement over current state'
      },
      contrastEffect: {
        name: 'Contrast Effect',
        description: 'Compare to less attractive alternatives',
        whenToUse: 'When positioning your offer',
        example: 'Compared to building this in-house, our partnership offers...'
      },
      futureVision: {
        name: 'Future Vision',
        description: 'Paint picture of successful future outcome',
        whenToUse: 'When building excitement and commitment',
        example: 'Imagine where we could be 12 months from now'
      }
    };

    // Select techniques based on style and goal
    if (goal === 'build_rapport') {
      techniques.push(allTechniques.liking, allTechniques.consistency);
    } else if (goal === 'persuade') {
      techniques.push(allTechniques.reciprocity, allTechniques.framing, allTechniques.futureVision);
      if (negotiationStyle === NegotiationStyle.COMPETITIVE) {
        techniques.push(allTechniques.scarcity, allTechniques.anchoringBias);
      } else {
        techniques.push(allTechniques.socialProof, allTechniques.authority);
      }
    } else if (goal === 'explore') {
      techniques.push(allTechniques.liking, allTechniques.socialProof);
    } else if (goal === 'stand_firm') {
      techniques.push(allTechniques.authority, allTechniques.consistency, allTechniques.contrastEffect);
    } else if (goal === 'concede') {
      techniques.push(allTechniques.reciprocity, allTechniques.futureVision);
    }

    return techniques.slice(0, 2); // Use 1-2 techniques per message
  }

  /**
   * Craft strategic message content
   */
  private craftStrategicMessage(
    agent: UserRepresentativeAgent,
    recipient: UserRepresentativeAgent,
    messageType: MessageType,
    context: ConversationContext,
    strategy: MessageStrategy,
    content: any
  ): string {
    let message = '';

    // Opening based on relationship level and tone
    message += this.craftOpening(agent, recipient, context, strategy);

    // Main content based on message type
    switch (messageType) {
      case MessageType.INTRODUCTION:
        message += this.craftIntroductionContent(agent, recipient, strategy);
        break;

      case MessageType.PROPOSAL:
        message += this.craftProposalContent(agent, recipient, content.proposal, strategy, context);
        break;

      case MessageType.COUNTER_PROPOSAL:
        message += this.craftCounterProposalContent(agent, recipient, content.proposal, content.concerns, strategy, context);
        break;

      case MessageType.QUESTION:
        message += this.craftQuestionContent(agent, recipient, content.points, strategy);
        break;

      case MessageType.ANSWER:
        message += this.craftAnswerContent(agent, recipient, content.points, content.previousMessage, strategy);
        break;

      case MessageType.CLARIFICATION:
        message += this.craftClarificationContent(agent, recipient, content.points, strategy);
        break;

      case MessageType.ACCEPTANCE:
        message += this.craftAcceptanceContent(agent, recipient, content.proposal, strategy, context);
        break;

      case MessageType.REJECTION:
        message += this.craftRejectionContent(agent, recipient, content.concerns, strategy);
        break;

      case MessageType.NEGOTIATION:
        message += this.craftNegotiationContent(agent, recipient, content, strategy, context);
        break;
    }

    // Closing based on strategy
    message += this.craftClosing(agent, recipient, context, strategy);

    return message;
  }

  /**
   * Craft contextual opening
   */
  private craftOpening(
    agent: UserRepresentativeAgent,
    recipient: UserRepresentativeAgent,
    context: ConversationContext,
    strategy: MessageStrategy
  ): string {
    const recipientName = recipient.userContact.name.split(' ')[0]; // First name

    if (context.relationshipLevel === 'initial') {
      if (strategy.tone === 'friendly') {
        return `Hi ${recipientName},\n\n`;
      } else {
        return `Hello ${recipientName},\n\n`;
      }
    } else if (context.relationshipLevel === 'building') {
      return `${recipientName},\n\n`;
    } else if (context.priorAgreements > 0) {
      return `${recipientName},\n\nGreat to be working together again. `;
    } else {
      return `${recipientName},\n\n`;
    }
  }

  /**
   * Craft introduction content
   */
  private craftIntroductionContent(
    agent: UserRepresentativeAgent,
    recipient: UserRepresentativeAgent,
    strategy: MessageStrategy
  ): string {
    const userName = agent.userContact.name;
    const userTitle = agent.userContact.title || 'Professional';
    const userCompany = agent.userContact.company || '';

    let content = `I'm reaching out on behalf of ${userName}${userCompany ? `, ${userTitle} at ${userCompany}` : `, ${userTitle}`}. `;

    // Find common ground (liking technique)
    if (strategy.persuasionTechniques.some(t => t.name === 'Liking')) {
      const commonInterests = this.findCommonInterests(agent, recipient);
      if (commonInterests.length > 0) {
        content += `I noticed we share some common interests, particularly around ${commonInterests[0]}. `;
      }
    }

    // Value proposition
    content += `I believe there's significant potential for collaboration between our organizations.\n\n`;

    // Strategic framing of needs
    const topNeeds = agent.userProfile.needs
      .filter(n => n.priority === Priority.CRITICAL || n.priority === Priority.HIGH)
      .slice(0, 2);

    content += `**${userName}'s current focus:**\n`;
    topNeeds.forEach(need => {
      content += `• ${this.frameNeedPositively(need.description)}\n`;
    });

    // Strategic framing of offerings
    const topOfferings = agent.userProfile.offerings
      .filter(o => o.capacity > 0.5)
      .slice(0, 2);

    content += `\n**What ${userName} brings to the table:**\n`;
    topOfferings.forEach(offering => {
      content += `• ${this.frameOfferingCompellingly(offering.description)}\n`;
    });

    return content;
  }

  /**
   * Craft proposal content
   */
  private craftProposalContent(
    agent: UserRepresentativeAgent,
    recipient: UserRepresentativeAgent,
    proposal: ProposedTerms,
    strategy: MessageStrategy,
    context: ConversationContext
  ): string {
    let content = '';

    // Strategic opening based on framing approach
    if (strategy.framingApproach === 'win-win') {
      content += `I've put together a proposal that I believe creates significant value for both of us.\n\n`;
    } else if (strategy.framingApproach === 'value_creation') {
      content += `I see an opportunity to create something greater than the sum of its parts. Here's how:\n\n`;
    } else if (strategy.framingApproach === 'opportunity_focused') {
      content += `This is a unique opportunity that aligns perfectly with both our objectives:\n\n`;
    } else {
      content += `Here's a proposal that addresses the challenges we both face:\n\n`;
    }

    // Present the proposal with strategic framing
    content += `**The Partnership Framework:**\n\n`;

    // Frame what they get first (reciprocity)
    content += `**For ${recipient.userContact.name}:**\n`;
    content += `You would receive:\n`;
    proposal.terms.whatAgent2Gets.forEach(item => {
      content += `✓ ${this.frameBenefitCompellingly(item)}\n`;
    });

    content += `\n**For ${agent.userContact.name}:**\n`;
    content += `We would receive:\n`;
    proposal.terms.whatAgent1Gets.forEach(item => {
      content += `✓ ${this.frameBenefitCompellingly(item)}\n`;
    });

    // Future vision technique
    if (strategy.persuasionTechniques.some(t => t.name === 'Future Vision')) {
      content += `\n**The Opportunity:**\n`;
      content += `Imagine where this partnership could take us in 12 months – ${this.createVisionStatement(proposal.terms)}\n`;
    }

    // Conditions presented as mutual commitments
    if (proposal.terms.conditions && proposal.terms.conditions.length > 0) {
      content += `\n**Mutual Commitments:**\n`;
      proposal.terms.conditions.slice(0, 3).forEach(condition => {
        content += `• ${condition}\n`;
      });
    }

    // Timeline with urgency
    if (proposal.terms.timeline) {
      if (strategy.persuasionTechniques.some(t => t.name === 'Scarcity')) {
        content += `\n**Timeline:** ${proposal.terms.timeline} (optimal window for both organizations)\n`;
      } else {
        content += `\n**Proposed Timeline:** ${proposal.terms.timeline}\n`;
      }
    }

    return content;
  }

  /**
   * Craft counter-proposal content
   */
  private craftCounterProposalContent(
    agent: UserRepresentativeAgent,
    recipient: UserRepresentativeAgent,
    proposal: ProposedTerms,
    concerns: string[] | undefined,
    strategy: MessageStrategy,
    context: ConversationContext
  ): string {
    let content = '';

    // Acknowledge the original proposal positively
    content += `Thank you for your proposal. I appreciate the thought you've put into this. `;

    if (strategy.tone === 'collaborative') {
      content += `I see a lot of potential here, and I'd like to build on your ideas with some adjustments that could make this even more valuable for both parties.\n\n`;
    } else if (strategy.tone === 'assertive') {
      content += `However, there are some key points we need to address to make this work for ${agent.userContact.name}.\n\n`;
    } else {
      content += `I've reviewed it carefully and have some thoughts on how we can align this more closely with both our needs.\n\n`;
    }

    // Address concerns diplomatically
    if (concerns && concerns.length > 0) {
      content += `**Key Considerations:**\n`;
      concerns.forEach(concern => {
        content += `• ${this.frameConcernConstructively(concern)}\n`;
      });
      content += `\n`;
    }

    // Present counter-proposal
    content += `**Revised Framework:**\n\n`;

    // Emphasize what stays the same (consistency technique)
    content += `I'm pleased to maintain several elements from your original proposal, including the core value exchange. `;

    content += `Here's the adjusted structure:\n\n`;

    // Rest of proposal similar to craftProposalContent but with adjustments highlighted
    content += `**Enhanced Value for ${recipient.userContact.name}:**\n`;
    proposal.terms.whatAgent2Gets.forEach(item => {
      content += `✓ ${item}\n`;
    });

    content += `\n**Adjusted Requirements for ${agent.userContact.name}:**\n`;
    proposal.terms.whatAgent1Gets.forEach(item => {
      content += `✓ ${item}\n`;
    });

    return content;
  }

  /**
   * Craft acceptance content
   */
  private craftAcceptanceContent(
    agent: UserRepresentativeAgent,
    recipient: UserRepresentativeAgent,
    proposal: ProposedTerms,
    strategy: MessageStrategy,
    context: ConversationContext
  ): string {
    let content = '';

    // Enthusiastic acceptance
    content += `Excellent! I'm pleased to accept this proposal on behalf of ${agent.userContact.name}. `;

    // Reinforce the value
    content += `This partnership framework creates significant value for both organizations and aligns perfectly with our strategic objectives.\n\n`;

    // Future vision
    content += `**Next Steps:**\n`;
    content += `I'm excited to move forward. I suggest we:\n`;
    content += `1. Schedule a kickoff meeting within the next week\n`;
    content += `2. Define detailed implementation milestones\n`;
    content += `3. Establish regular communication channels\n`;
    content += `4. Set up success metrics and tracking\n\n`;

    content += `I'm looking forward to a successful partnership. `;

    return content;
  }

  /**
   * Craft rejection content (diplomatic)
   */
  private craftRejectionContent(
    agent: UserRepresentativeAgent,
    recipient: UserRepresentativeAgent,
    concerns: string[] | undefined,
    strategy: MessageStrategy
  ): string {
    let content = '';

    // Polite opening
    content += `I've given your proposal careful consideration. While I appreciate the effort and see merit in your approach, `;
    content += `I don't believe we can move forward with the current framework given ${agent.userContact.name}'s requirements and constraints.\n\n`;

    // Explain reasoning
    if (concerns && concerns.length > 0) {
      content += `**Key Gaps:**\n`;
      concerns.forEach(concern => {
        content += `• ${concern}\n`;
      });
      content += `\n`;
    }

    // Leave door open
    content += `That said, I believe there's still potential for collaboration in the future. `;
    content += `Perhaps we could revisit this when circumstances align better, or explore alternative structures.\n\n`;

    content += `Thank you for your time and consideration.`;

    return content;
  }

  /**
   * Craft question content
   */
  private craftQuestionContent(
    agent: UserRepresentativeAgent,
    recipient: UserRepresentativeAgent,
    points: string[],
    strategy: MessageStrategy
  ): string {
    let content = '';

    content += `To better understand how we can create the most value, I have a few questions:\n\n`;

    points.forEach((point, idx) => {
      content += `${idx + 1}. ${point}\n`;
    });

    content += `\nYour insights on these points would be very helpful.`;

    return content;
  }

  /**
   * Craft answer content
   */
  private craftAnswerContent(
    agent: UserRepresentativeAgent,
    recipient: UserRepresentativeAgent,
    points: string[],
    previousMessage: ConversationMessage | undefined,
    strategy: MessageStrategy
  ): string {
    let content = '';

    content += `Great questions. Here are my thoughts:\n\n`;

    points.forEach((point, idx) => {
      content += `**Q${idx + 1}:** ${point}\n\n`;
    });

    return content;
  }

  /**
   * Craft clarification content
   */
  private craftClarificationContent(
    agent: UserRepresentativeAgent,
    recipient: UserRepresentativeAgent,
    points: string[],
    strategy: MessageStrategy
  ): string {
    let content = '';

    content += `I'd like to clarify a few points to ensure we're aligned:\n\n`;

    points.forEach((point, idx) => {
      content += `• ${point}\n`;
    });

    content += `\nPlease let me know if you need any additional information.`;

    return content;
  }

  /**
   * Craft negotiation content
   */
  private craftNegotiationContent(
    agent: UserRepresentativeAgent,
    recipient: UserRepresentativeAgent,
    content: any,
    strategy: MessageStrategy,
    context: ConversationContext
  ): string {
    let message = '';

    if (context.progressDirection === 'converging') {
      message += `I'm encouraged by the progress we're making. We're close to alignment on most points.\n\n`;
    } else if (context.progressDirection === 'stalled') {
      message += `It seems we've hit a bit of an impasse. Let's try to find creative solutions.\n\n`;
    } else {
      message += `I understand we have different perspectives on some points. Let's work through these systematically.\n\n`;
    }

    return message;
  }

  /**
   * Craft closing
   */
  private craftClosing(
    agent: UserRepresentativeAgent,
    recipient: UserRepresentativeAgent,
    context: ConversationContext,
    strategy: MessageStrategy
  ): string {
    if (strategy.tone === 'friendly') {
      return `\n\nLooking forward to your thoughts!\n\nBest regards,\n${agent.userContact.name}`;
    } else if (strategy.tone === 'collaborative') {
      return `\n\nI'm confident we can find a mutually beneficial path forward.\n\nBest regards,\n${agent.userContact.name}`;
    } else if (strategy.tone === 'assertive') {
      return `\n\nI believe these adjustments are essential for a successful partnership.\n\nBest regards,\n${agent.userContact.name}`;
    } else {
      return `\n\nI look forward to your response.\n\nBest regards,\n${agent.userContact.name}`;
    }
  }

  // Helper methods

  private findCommonInterests(agent1: UserRepresentativeAgent, agent2: UserRepresentativeAgent): string[] {
    const interests: string[] = [];
    // Simple implementation - could be much more sophisticated
    const agent1Industries = agent1.userProfile.preferences.preferredIndustries || [];
    const agent2Industries = agent2.userProfile.preferences.preferredIndustries || [];

    const common = agent1Industries.filter(i => agent2Industries.includes(i));
    return common;
  }

  private frameNeedPositively(need: string): string {
    // Reframe needs as goals/aspirations
    return need.replace(/need|want|require/gi, match => {
      if (match.toLowerCase() === 'need') return 'seeking';
      if (match.toLowerCase() === 'want') return 'pursuing';
      if (match.toLowerCase() === 'require') return 'targeting';
      return match;
    });
  }

  private frameOfferingCompellingly(offering: string): string {
    // Add power words
    const powerWords = ['proven', 'innovative', 'comprehensive', 'strategic', 'world-class'];
    const randomPower = powerWords[Math.floor(Math.random() * powerWords.length)];

    if (!offering.toLowerCase().includes(randomPower)) {
      return `${randomPower.charAt(0).toUpperCase() + randomPower.slice(1)} ${offering}`;
    }
    return offering;
  }

  private frameBenefitCompellingly(benefit: string): string {
    // Emphasize value and outcomes
    return benefit;
  }

  private createVisionStatement(terms: any): string {
    return `both organizations achieving their strategic goals through this partnership, with measurable impact and sustained growth`;
  }

  private frameConcernConstructively(concern: string): string {
    // Reframe concerns as opportunities for improvement
    return concern.replace(/concern|problem|issue/gi, 'consideration')
      .replace(/not|don't|doesn't/gi, '')
      .trim();
  }

  private calculateMessageSentiment(strategy: MessageStrategy, context: ConversationContext): number {
    let sentiment = 0.5;

    if (strategy.tone === 'friendly') sentiment = 0.8;
    else if (strategy.tone === 'collaborative') sentiment = 0.7;
    else if (strategy.tone === 'professional') sentiment = 0.6;
    else if (strategy.tone === 'assertive') sentiment = 0.4;
    else if (strategy.tone === 'cautious') sentiment = 0.5;

    // Adjust based on tension
    sentiment -= context.tensionLevel * 0.2;

    return Math.max(0, Math.min(1, sentiment));
  }

  /**
   * Analyze conversation to update context
   */
  updateConversationContext(
    context: ConversationContext,
    latestMessage: ConversationMessage,
    latestProposal?: ProposedTerms,
    previousProposal?: ProposedTerms
  ): ConversationContext {
    const updated = { ...context };

    // Update round number
    if (latestMessage.messageType === MessageType.PROPOSAL ||
        latestMessage.messageType === MessageType.COUNTER_PROPOSAL) {
      updated.roundNumber++;
    }

    // Update negotiation stage
    if (context.roundNumber <= 2) {
      updated.negotiationStage = 'opening';
    } else if (context.roundNumber <= 4) {
      updated.negotiationStage = 'exploration';
    } else if (context.roundNumber <= 8) {
      updated.negotiationStage = 'negotiation';
    } else {
      updated.negotiationStage = 'closing';
    }

    // Update relationship level
    if (context.roundNumber > 5) {
      updated.relationshipLevel = 'building';
    }
    if (context.roundNumber > 10 || context.priorAgreements > 0) {
      updated.relationshipLevel = 'established';
    }

    // Update progress direction
    if (latestProposal && previousProposal) {
      // Compare proposals to see if converging
      const similarity = this.calculateProposalSimilarity(latestProposal, previousProposal);
      if (similarity > 0.7) {
        updated.progressDirection = 'converging';
        updated.tensionLevel = Math.max(0, updated.tensionLevel - 0.1);
      } else if (similarity < 0.4) {
        updated.progressDirection = 'diverging';
        updated.tensionLevel = Math.min(1, updated.tensionLevel + 0.1);
      } else {
        updated.progressDirection = 'stalled';
      }
    }

    // Update tension based on sentiment
    if (latestMessage.sentiment !== undefined) {
      if (latestMessage.sentiment < 0.4) {
        updated.tensionLevel = Math.min(1, updated.tensionLevel + 0.15);
      } else if (latestMessage.sentiment > 0.7) {
        updated.tensionLevel = Math.max(0, updated.tensionLevel - 0.1);
      }
    }

    return updated;
  }

  private calculateProposalSimilarity(proposal1: ProposedTerms, proposal2: ProposedTerms): number {
    // Simple Jaccard similarity on terms
    const set1 = new Set([
      ...proposal1.terms.whatAgent1Gets,
      ...proposal1.terms.whatAgent1Gives
    ]);
    const set2 = new Set([
      ...proposal2.terms.whatAgent1Gets,
      ...proposal2.terms.whatAgent1Gives
    ]);

    const intersection = new Set([...set1].filter(x => set2.has(x)));
    const union = new Set([...set1, ...set2]);

    return intersection.size / union.size;
  }

  /**
   * Create initial conversation context
   */
  createInitialContext(priorAgreements: number = 0): ConversationContext {
    return {
      negotiationStage: 'opening',
      relationshipLevel: priorAgreements > 0 ? 'building' : 'initial',
      tensionLevel: 0.3, // Start with some healthy tension
      progressDirection: 'converging',
      roundNumber: 0,
      priorAgreements
    };
  }
}
