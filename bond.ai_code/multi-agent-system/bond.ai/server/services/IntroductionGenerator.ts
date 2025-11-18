import { Pool } from 'pg';
import Redis from 'ioredis';

/**
 * Automated Introduction Generation Service
 *
 * Generates personalized, contextual introductions using:
 * - Match explanation insights
 * - User profile analysis
 * - Success prediction factors
 * - Industry-specific templates
 * - Tone matching
 */

export interface GeneratedIntroduction {
  subject: string;
  body: string;
  tone: 'professional' | 'friendly' | 'casual' | 'formal';
  keyPoints: string[];
  callToAction: string;
  alternatives: {
    subject: string;
    body: string;
  }[];
}

export class IntroductionGenerator {
  private pool: Pool;
  private redis: Redis;

  constructor(pool: Pool, redis: Redis) {
    this.pool = pool;
    this.redis = redis;
  }

  /**
   * Generate personalized introduction
   */
  async generateIntroduction(
    userId: string,
    matchId: string,
    tone: 'professional' | 'friendly' | 'casual' | 'formal' = 'professional'
  ): Promise<GeneratedIntroduction> {
    const client = await this.pool.connect();

    try {
      // Get match and user data
      const matchData = await client.query(
        `SELECT
           mc.*,
           u1.name as sender_name,
           u1.industry as sender_industry,
           u2.name as recipient_name,
           u2.industry as recipient_industry,
           up1.needs as sender_needs,
           up1.offerings as sender_offerings,
           up2.needs as recipient_needs,
           up2.offerings as recipient_offerings
         FROM match_candidates mc
         JOIN agents a1 ON mc.initiator_agent_id = a1.id
         JOIN agents a2 ON mc.agent_id = a2.id
         JOIN users u1 ON a1.user_id = u1.id
         JOIN users u2 ON a2.user_id = u2.id
         LEFT JOIN user_profiles up1 ON u1.id = up1.user_id
         LEFT JOIN user_profiles up2 ON u2.id = up2.user_id
         WHERE mc.id = $1 AND (a1.user_id = $2 OR a2.user_id = $2)`,
        [matchId, userId]
      );

      if (matchData.rows.length === 0) {
        throw new Error('Match not found');
      }

      const match = matchData.rows[0];
      const isSender = match.sender_name;
      const senderName = isSender ? match.sender_name : match.recipient_name;
      const recipientName = isSender ? match.recipient_name : match.sender_name;
      const senderNeeds = isSender ? match.sender_needs : match.recipient_needs;
      const senderOfferings = isSender ? match.sender_offerings : match.recipient_offerings;
      const recipientNeeds = isSender ? match.recipient_needs : match.sender_needs;
      const recipientOfferings = isSender ? match.recipient_offerings : match.sender_offerings;

      // Generate subject line
      const subject = this.generateSubject(match, recipientName, tone);

      // Generate body
      const body = this.generateBody(
        match,
        senderName,
        recipientName,
        senderNeeds,
        senderOfferings,
        recipientNeeds,
        recipientOfferings,
        tone
      );

      // Extract key points
      const keyPoints = this.extractKeyPoints(
        senderNeeds,
        senderOfferings,
        recipientNeeds,
        recipientOfferings
      );

      // Generate call to action
      const callToAction = this.generateCallToAction(match, tone);

      // Generate alternatives
      const alternatives = this.generateAlternatives(
        match,
        senderName,
        recipientName,
        senderNeeds,
        senderOfferings,
        recipientNeeds,
        recipientOfferings
      );

      return {
        subject,
        body,
        tone,
        keyPoints,
        callToAction,
        alternatives
      };
    } finally {
      client.release();
    }
  }

  /**
   * Generate subject line
   */
  private generateSubject(match: any, recipientName: string, tone: string): string {
    const matchType = match.match_type;

    const templates: Record<string, string[]> = {
      'investor-startup': [
        `Exploring ${matchType.replace('-', ' ')} opportunity`,
        `Investment opportunity that caught my eye`,
        `Let's discuss a potential partnership`
      ],
      'mentor-mentee': [
        `Seeking your guidance in ${match.recipient_industry}`,
        `Would love to learn from your experience`,
        `Mentorship opportunity`
      ],
      'partnership': [
        `Potential collaboration opportunity`,
        `Let's explore working together`,
        `Partnership proposal`
      ],
      'default': [
        `Introduction via Bond.AI`,
        `Let's connect`,
        `Mutual interest in collaboration`
      ]
    };

    const options = templates[matchType] || templates['default'];

    if (tone === 'formal') {
      return `Re: ${options[0]}`;
    } else if (tone === 'casual') {
      return `Hey ${recipientName} - ${options[1]}`;
    } else {
      return options[0];
    }
  }

  /**
   * Generate introduction body
   */
  private generateBody(
    match: any,
    senderName: string,
    recipientName: string,
    senderNeeds: any[],
    senderOfferings: any[],
    recipientNeeds: any[],
    recipientOfferings: any[],
    tone: string
  ): string {
    const greeting = this.getGreeting(recipientName, tone);
    const intro = this.getIntroduction(senderName, match, tone);
    const valueProposition = this.getValueProposition(
      senderNeeds,
      senderOfferings,
      recipientNeeds,
      recipientOfferings,
      match,
      tone
    );
    const closing = this.getClosing(tone);

    return `${greeting}\n\n${intro}\n\n${valueProposition}\n\n${closing}`;
  }

  /**
   * Get greeting based on tone
   */
  private getGreeting(recipientName: string, tone: string): string {
    switch (tone) {
      case 'formal':
        return `Dear ${recipientName},`;
      case 'casual':
        return `Hey ${recipientName}!`;
      case 'friendly':
        return `Hi ${recipientName},`;
      default:
        return `Hello ${recipientName},`;
    }
  }

  /**
   * Get introduction paragraph
   */
  private getIntroduction(senderName: string, match: any, tone: string): string {
    const matchType = match.match_type.replace('-', ' ');
    const score = Math.round(match.compatibility_score * 100);

    if (tone === 'formal') {
      return `I hope this message finds you well. My name is ${senderName}, and I came across your profile on Bond.AI. Our match score of ${score}% suggests we have significant alignment, particularly in the area of ${matchType}.`;
    } else if (tone === 'casual') {
      return `I'm ${senderName}. Bond.AI matched us with a ${score}% compatibility score - pretty impressive! Looks like we're both interested in ${matchType}.`;
    } else {
      return `My name is ${senderName}. Bond.AI connected us based on a ${score}% compatibility match, especially around ${matchType}. I thought it would be worth reaching out.`;
    }
  }

  /**
   * Get value proposition
   */
  private getValueProposition(
    senderNeeds: any[],
    senderOfferings: any[],
    recipientNeeds: any[],
    recipientOfferings: any[],
    match: any,
    tone: string
  ): string {
    // Find complementary matches
    const matches: string[] = [];

    (senderNeeds || []).forEach((need: any) => {
      (recipientOfferings || []).forEach((offering: any) => {
        if (this.categoriesMatch(need.category, offering.category)) {
          matches.push({
            type: 'recipient_helps_sender',
            need: need.category,
            offering: offering.category,
            description: need.description
          } as any);
        }
      });
    });

    (recipientNeeds || []).forEach((need: any) => {
      (senderOfferings || []).forEach((offering: any) => {
        if (this.categoriesMatch(need.category, offering.category)) {
          matches.push({
            type: 'sender_helps_recipient',
            need: need.category,
            offering: offering.category,
            description: need.description
          } as any);
        }
      });
    });

    if (matches.length === 0) {
      return `I believe there could be interesting synergies between our work, and I'd love to explore potential collaboration opportunities.`;
    }

    const match1 = matches[0] as any;

    if (match1.type === 'recipient_helps_sender') {
      return `I noticed you have experience with ${match1.offering}, which aligns perfectly with a current need I have: ${match1.description}. ${matches.length > 1 ? `Additionally, I see several other areas where we could collaborate.` : ''}`;
    } else {
      return `I saw that you're looking for ${match1.need}. I have significant experience in this area and would be happy to discuss how I might be able to help. ${matches.length > 1 ? `I also noticed several other potential collaboration opportunities.` : ''}`;
    }
  }

  /**
   * Get closing
   */
  private getClosing(tone: string): string {
    if (tone === 'formal') {
      return `I would appreciate the opportunity to schedule a brief call to discuss this further at your convenience.\n\nBest regards`;
    } else if (tone === 'casual') {
      return `Let me know if you're interested in chatting - I'm pretty flexible on timing.\n\nCheers`;
    } else {
      return `Would you be open to a quick call to explore this further? Happy to work around your schedule.\n\nBest`;
    }
  }

  /**
   * Extract key points
   */
  private extractKeyPoints(
    senderNeeds: any[],
    senderOfferings: any[],
    recipientNeeds: any[],
    recipientOfferings: any[]
  ): string[] {
    const points: string[] = [];

    // Match needs with offerings
    (senderNeeds || []).forEach((need: any) => {
      (recipientOfferings || []).forEach((offering: any) => {
        if (this.categoriesMatch(need.category, offering.category)) {
          points.push(`They can help you with: ${need.category}`);
        }
      });
    });

    (recipientNeeds || []).forEach((need: any) => {
      (senderOfferings || []).forEach((offering: any) => {
        if (this.categoriesMatch(need.category, offering.category)) {
          points.push(`You can help them with: ${need.category}`);
        }
      });
    });

    return points.slice(0, 5);
  }

  /**
   * Generate call to action
   */
  private generateCallToAction(match: any, tone: string): string {
    const matchType = match.match_type;

    const ctas: Record<string, string> = {
      'investor-startup': 'Schedule a pitch meeting',
      'mentor-mentee': 'Set up an introductory coffee chat',
      'partnership': 'Explore collaboration opportunities',
      'talent-acquisition': 'Discuss the opportunity',
      'default': 'Schedule a brief call'
    };

    return ctas[matchType] || ctas['default'];
  }

  /**
   * Generate alternative versions
   */
  private generateAlternatives(
    match: any,
    senderName: string,
    recipientName: string,
    senderNeeds: any[],
    senderOfferings: any[],
    recipientNeeds: any[],
    recipientOfferings: any[]
  ): { subject: string; body: string }[] {
    const alternatives: { subject: string; body: string }[] = [];

    // Alternative 1: More direct
    alternatives.push({
      subject: `Quick question about ${match.match_type.replace('-', ' ')}`,
      body: `Hi ${recipientName},\n\nI'm reaching out because Bond.AI matched us based on mutual interests in ${match.match_type.replace('-', ' ')}. I'd love to explore if there's a fit.\n\nAre you available for a 15-minute call this week?\n\nBest,\n${senderName}`
    });

    // Alternative 2: More detailed
    const detailedValue = this.getDetailedValueProposition(
      senderNeeds,
      senderOfferings,
      recipientNeeds,
      recipientOfferings
    );

    alternatives.push({
      subject: `Collaboration opportunity - Bond.AI match`,
      body: `Hello ${recipientName},\n\nI'm ${senderName}. We were matched on Bond.AI with a high compatibility score.\n\n${detailedValue}\n\nIf this resonates, I'd love to schedule a call to discuss further.\n\nLooking forward to connecting,\n${senderName}`
    });

    return alternatives;
  }

  /**
   * Get detailed value proposition
   */
  private getDetailedValueProposition(
    senderNeeds: any[],
    senderOfferings: any[],
    recipientNeeds: any[],
    recipientOfferings: any[]
  ): string {
    const parts: string[] = [];

    if (senderOfferings && senderOfferings.length > 0) {
      parts.push(`I bring: ${senderOfferings.map((o: any) => o.category).slice(0, 3).join(', ')}`);
    }

    if (senderNeeds && senderNeeds.length > 0) {
      parts.push(`I'm looking for: ${senderNeeds.map((n: any) => n.category).slice(0, 3).join(', ')}`);
    }

    return parts.join('\n');
  }

  /**
   * Helper: Check if categories match
   */
  private categoriesMatch(cat1: string, cat2: string): boolean {
    if (cat1 === cat2) return true;

    const related: Record<string, string[]> = {
      'funding': ['investment', 'capital'],
      'mentorship': ['coaching', 'advisory'],
      'technical': ['engineering', 'development']
    };

    for (const [key, vals] of Object.entries(related)) {
      if ((cat1 === key || vals.includes(cat1)) && (cat2 === key || vals.includes(cat2))) {
        return true;
      }
    }

    return false;
  }
}
