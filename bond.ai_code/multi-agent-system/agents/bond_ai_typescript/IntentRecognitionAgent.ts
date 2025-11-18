import { Pool } from 'pg';
import Redis from 'ioredis';

/**
 * Intent Recognition Agent
 *
 * Analyzes user messages and actions to detect intent and provide
 * contextual assistance.
 *
 * Key capabilities:
 * - Intent classification (seeking, offering, introducing, etc.)
 * - Entity extraction (people, skills, industries, etc.)
 * - Sentiment analysis
 * - Urgency detection
 * - Action recommendation based on intent
 */

export interface DetectedIntent {
  userId: string;
  message: string;
  primaryIntent: IntentType;
  confidence: number; // 0-1
  secondaryIntents: Array<{ type: IntentType; confidence: number }>;

  entities: {
    people: string[]; // Mentioned names
    skills: string[]; // Mentioned skills/expertise
    industries: string[]; // Mentioned industries
    locations: string[]; // Mentioned locations
    companies: string[]; // Mentioned companies
    actions: string[]; // Action words
  };

  sentiment: {
    polarity: 'positive' | 'neutral' | 'negative';
    score: number; // -1 to 1
    emotions: Array<{ emotion: string; intensity: number }>;
  };

  urgency: {
    level: 'low' | 'medium' | 'high' | 'urgent';
    score: number; // 0-1
    indicators: string[];
  };

  suggestedActions: Array<{
    action: string;
    priority: 'high' | 'medium' | 'low';
    reasoning: string;
  }>;

  contextualData: {
    timeOfDay: string;
    dayOfWeek: string;
    userActivity: string; // Recent activity pattern
    networkContext: string; // Current network state
  };
}

export type IntentType =
  | 'seeking_connection' // Looking to connect with someone
  | 'offering_help' // Offering expertise/help
  | 'requesting_introduction' // Asking for intro
  | 'providing_introduction' // Making an intro
  | 'seeking_collaboration' // Looking for collaborators
  | 'sharing_opportunity' // Sharing job/opportunity
  | 'asking_question' // Seeking information
  | 'expressing_gratitude' // Thanking someone
  | 'scheduling_meeting' // Setting up a meeting
  | 'following_up' // Following up on previous conversation
  | 'networking_casual' // Casual networking
  | 'seeking_advice' // Asking for advice
  | 'offering_opportunity' // Offering job/project
  | 'exploring' // Just browsing/exploring
  | 'unknown'; // Cannot determine

export interface IntentPattern {
  pattern: RegExp;
  intent: IntentType;
  weight: number;
  entities?: string[];
}

export class IntentRecognitionAgent {
  // Intent patterns (simplified - would use ML in production)
  private readonly INTENT_PATTERNS: IntentPattern[] = [
    // Seeking connection
    { pattern: /looking for|seeking|need to connect|want to meet/i, intent: 'seeking_connection', weight: 0.9 },
    { pattern: /know anyone who|can you introduce|introduction to/i, intent: 'requesting_introduction', weight: 0.95 },

    // Offering
    { pattern: /i can help|happy to|offering|available to/i, intent: 'offering_help', weight: 0.85 },
    { pattern: /let me introduce|want to connect you|should meet/i, intent: 'providing_introduction', weight: 0.9 },

    // Collaboration
    { pattern: /looking for partner|collaborate on|work together|co-founder/i, intent: 'seeking_collaboration', weight: 0.9 },
    { pattern: /project opportunity|collaboration|partnership/i, intent: 'seeking_collaboration', weight: 0.7 },

    // Opportunities
    { pattern: /job opening|hiring|position available|opportunity at/i, intent: 'sharing_opportunity', weight: 0.85 },
    { pattern: /interested in role|apply for|career opportunity/i, intent: 'offering_opportunity', weight: 0.8 },

    // Communication
    { pattern: /thank you|thanks|appreciate|grateful/i, intent: 'expressing_gratitude', weight: 0.9 },
    { pattern: /schedule|meeting|call|coffee|lunch/i, intent: 'scheduling_meeting', weight: 0.85 },
    { pattern: /following up|circling back|checking in/i, intent: 'following_up', weight: 0.8 },

    // Questions
    { pattern: /what do you think|advice on|your opinion|how should/i, intent: 'seeking_advice', weight: 0.85 },
    { pattern: /\?/, intent: 'asking_question', weight: 0.5 },
  ];

  // Urgency indicators
  private readonly URGENCY_INDICATORS: Array<{ pattern: RegExp; score: number }> = [
    { pattern: /asap|urgent|immediately|right away/i, score: 1.0 },
    { pattern: /soon|quickly|fast|rapid/i, score: 0.8 },
    { pattern: /this week|by friday|deadline/i, score: 0.7 },
    { pattern: /when you can|no rush|whenever/i, score: 0.2 },
  ];

  // Sentiment keywords (simplified)
  private readonly SENTIMENT_KEYWORDS = {
    positive: ['great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'perfect', 'awesome'],
    negative: ['bad', 'terrible', 'awful', 'hate', 'worst', 'disappointed', 'frustrated', 'annoyed'],
  };

  constructor(
    private pool: Pool,
    private redis: Redis
  ) {}

  /**
   * Detect intent from a user message
   */
  async detectIntent(userId: string, message: string): Promise<DetectedIntent> {
    // Check cache
    const cacheKey = `intent:${userId}:${this.hashMessage(message)}`;
    const cached = await this.redis.get(cacheKey);
    if (cached) return JSON.parse(cached);

    // Extract entities
    const entities = this.extractEntities(message);

    // Detect intent
    const { primaryIntent, confidence, secondaryIntents } = this.classifyIntent(message, entities);

    // Analyze sentiment
    const sentiment = this.analyzeSentiment(message);

    // Detect urgency
    const urgency = this.detectUrgency(message);

    // Get contextual data
    const contextualData = await this.getContextualData(userId);

    // Generate suggested actions
    const suggestedActions = await this.generateSuggestedActions(
      userId,
      primaryIntent,
      entities,
      urgency,
      contextualData
    );

    const result: DetectedIntent = {
      userId,
      message,
      primaryIntent,
      confidence,
      secondaryIntents,
      entities,
      sentiment,
      urgency,
      suggestedActions,
      contextualData,
    };

    // Cache for 1 hour
    await this.redis.set(cacheKey, JSON.stringify(result), 'EX', 3600);

    return result;
  }

  /**
   * Batch detect intents for multiple messages
   */
  async detectIntentBatch(
    userId: string,
    messages: string[]
  ): Promise<DetectedIntent[]> {
    return Promise.all(messages.map(msg => this.detectIntent(userId, msg)));
  }

  /**
   * Analyze conversation flow to detect evolving intent
   */
  async analyzeConversationFlow(
    userId: string,
    messages: Array<{ sender: string; message: string; timestamp: Date }>
  ): Promise<{
    overallIntent: IntentType;
    intentEvolution: Array<{ timestamp: Date; intent: IntentType }>;
    conversationStage: 'opening' | 'exploration' | 'negotiation' | 'closing';
    nextLikelyIntent: IntentType;
    recommendations: string[];
  }> {
    const intents = await Promise.all(
      messages.map(async (msg) => ({
        timestamp: msg.timestamp,
        intent: (await this.detectIntent(userId, msg.message)).primaryIntent,
      }))
    );

    // Determine overall intent (most frequent)
    const intentCounts = new Map<IntentType, number>();
    intents.forEach(({ intent }) => {
      intentCounts.set(intent, (intentCounts.get(intent) || 0) + 1);
    });

    const overallIntent = Array.from(intentCounts.entries())
      .sort((a, b) => b[1] - a[1])[0][0];

    // Determine conversation stage
    const messageCount = messages.length;
    let conversationStage: 'opening' | 'exploration' | 'negotiation' | 'closing';

    if (messageCount <= 2) {
      conversationStage = 'opening';
    } else if (messageCount <= 5) {
      conversationStage = 'exploration';
    } else if (messageCount <= 10) {
      conversationStage = 'negotiation';
    } else {
      conversationStage = 'closing';
    }

    // Predict next intent based on pattern
    const recentIntents = intents.slice(-3).map(i => i.intent);
    const nextLikelyIntent = this.predictNextIntent(recentIntents, conversationStage);

    // Generate recommendations
    const recommendations = this.generateConversationRecommendations(
      overallIntent,
      conversationStage,
      nextLikelyIntent
    );

    return {
      overallIntent,
      intentEvolution: intents,
      conversationStage,
      nextLikelyIntent,
      recommendations,
    };
  }

  /**
   * Private helper methods
   */

  private extractEntities(message: string): DetectedIntent['entities'] {
    // Simplified entity extraction (would use NER in production)
    const entities: DetectedIntent['entities'] = {
      people: [],
      skills: [],
      industries: [],
      locations: [],
      companies: [],
      actions: [],
    };

    // Extract capitalized words (potential names/companies)
    const capitalizedWords = message.match(/\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b/g) || [];
    entities.people = capitalizedWords.slice(0, 3); // Assume first few are people

    // Extract skills (simple keyword matching)
    const skillKeywords = ['AI', 'ML', 'Python', 'JavaScript', 'React', 'Design', 'Marketing', 'Sales'];
    entities.skills = skillKeywords.filter(skill =>
      message.toLowerCase().includes(skill.toLowerCase())
    );

    // Extract industries
    const industryKeywords = ['tech', 'finance', 'healthcare', 'education', 'retail', 'manufacturing'];
    entities.industries = industryKeywords.filter(industry =>
      message.toLowerCase().includes(industry)
    );

    // Extract action verbs
    const actionWords = message.match(/\b(connect|meet|introduce|collaborate|work|help|share|find)\b/gi) || [];
    entities.actions = [...new Set(actionWords.map(w => w.toLowerCase()))];

    return entities;
  }

  private classifyIntent(
    message: string,
    entities: DetectedIntent['entities']
  ): {
    primaryIntent: IntentType;
    confidence: number;
    secondaryIntents: Array<{ type: IntentType; confidence: number }>;
  } {
    const scores = new Map<IntentType, number>();

    // Score based on patterns
    for (const pattern of this.INTENT_PATTERNS) {
      if (pattern.pattern.test(message)) {
        const currentScore = scores.get(pattern.intent) || 0;
        scores.set(pattern.intent, currentScore + pattern.weight);
      }
    }

    // Boost scores based on entities
    if (entities.actions.includes('introduce') || entities.actions.includes('connect')) {
      scores.set('requesting_introduction', (scores.get('requesting_introduction') || 0) + 0.3);
    }

    if (entities.skills.length > 0 && entities.actions.includes('help')) {
      scores.set('offering_help', (scores.get('offering_help') || 0) + 0.2);
    }

    // Sort by score
    const sortedIntents = Array.from(scores.entries())
      .sort((a, b) => b[1] - a[1]);

    if (sortedIntents.length === 0) {
      return {
        primaryIntent: 'unknown',
        confidence: 0.1,
        secondaryIntents: [],
      };
    }

    const maxScore = sortedIntents[0][1];
    const normalizedConfidence = Math.min(1, maxScore / 2); // Normalize to 0-1

    return {
      primaryIntent: sortedIntents[0][0],
      confidence: normalizedConfidence,
      secondaryIntents: sortedIntents.slice(1, 3).map(([type, score]) => ({
        type,
        confidence: Math.min(1, score / 2),
      })),
    };
  }

  private analyzeSentiment(message: string): DetectedIntent['sentiment'] {
    let score = 0;
    const messageLower = message.toLowerCase();

    // Count positive and negative words
    let positiveCount = 0;
    let negativeCount = 0;

    for (const word of this.SENTIMENT_KEYWORDS.positive) {
      if (messageLower.includes(word)) positiveCount++;
    }

    for (const word of this.SENTIMENT_KEYWORDS.negative) {
      if (messageLower.includes(word)) negativeCount++;
    }

    score = (positiveCount - negativeCount) / Math.max(1, positiveCount + negativeCount);

    // Determine polarity
    let polarity: 'positive' | 'neutral' | 'negative';
    if (score > 0.2) polarity = 'positive';
    else if (score < -0.2) polarity = 'negative';
    else polarity = 'neutral';

    // Detect emotions (simplified)
    const emotions: Array<{ emotion: string; intensity: number }> = [];

    if (messageLower.includes('excit')) emotions.push({ emotion: 'excitement', intensity: 0.8 });
    if (messageLower.includes('thank')) emotions.push({ emotion: 'gratitude', intensity: 0.9 });
    if (messageLower.includes('sorry')) emotions.push({ emotion: 'regret', intensity: 0.7 });
    if (messageLower.includes('frustrat')) emotions.push({ emotion: 'frustration', intensity: 0.8 });

    return { polarity, score, emotions };
  }

  private detectUrgency(message: string): DetectedIntent['urgency'] {
    let maxScore = 0;
    const indicators: string[] = [];

    for (const { pattern, score } of this.URGENCY_INDICATORS) {
      if (pattern.test(message)) {
        maxScore = Math.max(maxScore, score);
        indicators.push(pattern.source);
      }
    }

    let level: 'low' | 'medium' | 'high' | 'urgent';
    if (maxScore >= 0.9) level = 'urgent';
    else if (maxScore >= 0.7) level = 'high';
    else if (maxScore >= 0.4) level = 'medium';
    else level = 'low';

    return { level, score: maxScore, indicators };
  }

  private async getContextualData(userId: string): Promise<DetectedIntent['contextualData']> {
    const now = new Date();

    return {
      timeOfDay: this.getTimeOfDay(now),
      dayOfWeek: now.toLocaleDateString('en-US', { weekday: 'long' }),
      userActivity: 'active', // Would fetch from activity log
      networkContext: 'growing', // Would fetch from temporal analysis
    };
  }

  private getTimeOfDay(date: Date): string {
    const hour = date.getHours();
    if (hour < 6) return 'late night';
    if (hour < 12) return 'morning';
    if (hour < 17) return 'afternoon';
    if (hour < 21) return 'evening';
    return 'night';
  }

  private async generateSuggestedActions(
    userId: string,
    primaryIntent: IntentType,
    entities: DetectedIntent['entities'],
    urgency: DetectedIntent['urgency'],
    context: DetectedIntent['contextualData']
  ): Promise<DetectedIntent['suggestedActions']> {
    const actions: DetectedIntent['suggestedActions'] = [];

    switch (primaryIntent) {
      case 'seeking_connection':
        actions.push({
          action: 'Search for matches in the specified area',
          priority: urgency.level === 'urgent' ? 'high' : 'medium',
          reasoning: 'User is actively looking to connect',
        });
        if (entities.skills.length > 0) {
          actions.push({
            action: `Find users with expertise in: ${entities.skills.join(', ')}`,
            priority: 'high',
            reasoning: 'Specific skills mentioned',
          });
        }
        break;

      case 'requesting_introduction':
        actions.push({
          action: 'Identify mutual connections who can make introduction',
          priority: 'high',
          reasoning: 'User explicitly requested introduction',
        });
        actions.push({
          action: 'Suggest introduction template',
          priority: 'medium',
          reasoning: 'Help user craft effective introduction request',
        });
        break;

      case 'seeking_collaboration':
        actions.push({
          action: 'Find potential collaborators based on skills and goals',
          priority: 'high',
          reasoning: 'User is looking for collaboration partners',
        });
        actions.push({
          action: 'Analyze collaboration compatibility',
          priority: 'medium',
          reasoning: 'Predict success probability',
        });
        break;

      case 'scheduling_meeting':
        actions.push({
          action: 'Check calendar availability',
          priority: 'high',
          reasoning: 'User wants to schedule a meeting',
        });
        actions.push({
          action: 'Suggest optimal meeting times',
          priority: 'medium',
          reasoning: 'Streamline scheduling process',
        });
        break;

      case 'following_up':
        actions.push({
          action: 'Retrieve conversation history',
          priority: 'high',
          reasoning: 'User is following up on previous conversation',
        });
        actions.push({
          action: 'Suggest follow-up message template',
          priority: 'medium',
          reasoning: 'Help maintain relationship momentum',
        });
        break;

      default:
        actions.push({
          action: 'Provide general networking suggestions',
          priority: 'low',
          reasoning: 'Intent unclear - offer general assistance',
        });
    }

    return actions;
  }

  private predictNextIntent(
    recentIntents: IntentType[],
    stage: 'opening' | 'exploration' | 'negotiation' | 'closing'
  ): IntentType {
    // Simplified prediction logic
    if (stage === 'opening') return 'asking_question';
    if (stage === 'exploration') return 'seeking_collaboration';
    if (stage === 'negotiation') return 'scheduling_meeting';
    return 'expressing_gratitude';
  }

  private generateConversationRecommendations(
    overallIntent: IntentType,
    stage: string,
    nextIntent: IntentType
  ): string[] {
    const recommendations: string[] = [];

    if (stage === 'opening') {
      recommendations.push('Build rapport with personal connection');
      recommendations.push('Ask open-ended questions');
    } else if (stage === 'exploration') {
      recommendations.push('Share relevant experiences');
      recommendations.push('Explore mutual interests');
    } else if (stage === 'negotiation') {
      recommendations.push('Propose specific next steps');
      recommendations.push('Set clear expectations');
    } else {
      recommendations.push('Express gratitude');
      recommendations.push('Confirm action items');
    }

    return recommendations;
  }

  private hashMessage(message: string): string {
    // Simple hash for caching
    let hash = 0;
    for (let i = 0; i < message.length; i++) {
      const char = message.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash;
    }
    return hash.toString(36);
  }
}
