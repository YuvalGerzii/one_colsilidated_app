/**
 * Context Understanding Agent
 *
 * Deeply understands the broader context of matching requests including:
 * - Temporal context (timing, urgency, market conditions)
 * - Social context (relationship dynamics, cultural factors)
 * - Economic context (market trends, economic indicators)
 * - Strategic context (long-term goals, organizational objectives)
 *
 * This agent helps the system make more intelligent decisions by considering
 * factors beyond just profile matching.
 */

import { Contact } from '../types';

export interface MatchingContext {
  temporal: TemporalContext;
  social: SocialContext;
  economic: EconomicContext;
  strategic: StrategicContext;
  environmental: EnvironmentalContext;
}

export interface TemporalContext {
  urgency: 'immediate' | 'high' | 'medium' | 'low';
  timeHorizon: 'short' | 'medium' | 'long';
  seasonality: string | null;
  marketTiming: 'early' | 'peak' | 'late' | 'unknown';
  optimalTiming: boolean;
}

export interface SocialContext {
  relationshipType: 'transactional' | 'collaborative' | 'mentorship' | 'peer' | 'hierarchical';
  culturalConsiderations: string[];
  communicationStyle: 'formal' | 'casual' | 'technical' | 'mixed';
  trustLevel: 'cold' | 'warm' | 'hot';
  networkDynamics: 'closed' | 'open' | 'semi-open';
}

export interface EconomicContext {
  marketConditions: 'bull' | 'bear' | 'stable' | 'volatile';
  budgetConstraints: 'tight' | 'moderate' | 'flexible' | 'unlimited';
  valueExchange: 'monetary' | 'non-monetary' | 'mixed';
  competitivePressure: 'high' | 'medium' | 'low';
}

export interface StrategicContext {
  primaryGoal: string;
  secondaryGoals: string[];
  riskTolerance: 'conservative' | 'moderate' | 'aggressive';
  growthStage: 'ideation' | 'startup' | 'growth' | 'scale' | 'mature';
  strategicPriority: 'speed' | 'quality' | 'cost' | 'innovation';
}

export interface EnvironmentalContext {
  industryTrends: string[];
  competitiveLandscape: string;
  regulatoryEnvironment: 'strict' | 'moderate' | 'flexible';
  technologicalChange: 'rapid' | 'moderate' | 'slow';
}

export class ContextUnderstandingAgent {
  /**
   * Analyze and understand the full context of a matching request
   */
  async analyzeContext(
    seeker: Contact,
    query?: string,
    metadata?: any
  ): Promise<MatchingContext> {
    const temporal = await this.analyzeTemporalContext(seeker, query, metadata);
    const social = await this.analyzeSocialContext(seeker, query, metadata);
    const economic = await this.analyzeEconomicContext(seeker, query, metadata);
    const strategic = await this.analyzeStrategicContext(seeker, query, metadata);
    const environmental = await this.analyzeEnvironmentalContext(seeker, metadata);

    return {
      temporal,
      social,
      economic,
      strategic,
      environmental
    };
  }

  /**
   * Analyze temporal context
   */
  private async analyzeTemporalContext(
    seeker: Contact,
    query?: string,
    metadata?: any
  ): Promise<TemporalContext> {
    const urgencyKeywords = {
      immediate: ['asap', 'urgent', 'immediately', 'right now', 'emergency'],
      high: ['soon', 'quick', 'fast', 'this week', 'pressing'],
      medium: ['upcoming', 'planned', 'next month'],
      low: ['eventually', 'when possible', 'future']
    };

    let urgency: TemporalContext['urgency'] = 'medium';
    const text = (query || '').toLowerCase() + ' ' + (seeker.bio || '').toLowerCase();

    for (const [level, keywords] of Object.entries(urgencyKeywords)) {
      if (keywords.some(k => text.includes(k))) {
        urgency = level as TemporalContext['urgency'];
        break;
      }
    }

    // Determine time horizon based on needs and offerings
    const needs = (seeker.needs || []).join(' ').toLowerCase();
    const isLongTerm = needs.includes('partner') || needs.includes('cofounder') || needs.includes('mentor');
    const isShortTerm = needs.includes('consult') || needs.includes('advice') || needs.includes('one-time');

    const timeHorizon: TemporalContext['timeHorizon'] =
      isLongTerm ? 'long' : isShortTerm ? 'short' : 'medium';

    return {
      urgency,
      timeHorizon,
      seasonality: this.detectSeasonality(seeker),
      marketTiming: this.assessMarketTiming(seeker),
      optimalTiming: urgency !== 'immediate' // Immediate requests may not have optimal timing
    };
  }

  /**
   * Analyze social context
   */
  private async analyzeSocialContext(
    seeker: Contact,
    query?: string,
    metadata?: any
  ): Promise<SocialContext> {
    const needs = (seeker.needs || []).join(' ').toLowerCase();
    const offerings = (seeker.offerings || []).join(' ').toLowerCase();

    // Determine relationship type
    let relationshipType: SocialContext['relationshipType'] = 'collaborative';

    if (needs.includes('mentor') || needs.includes('advisor')) {
      relationshipType = 'mentorship';
    } else if (needs.includes('buy') || needs.includes('sell') || offerings.includes('purchase')) {
      relationshipType = 'transactional';
    } else if (seeker.title?.toLowerCase().includes('ceo') || seeker.title?.toLowerCase().includes('director')) {
      relationshipType = 'hierarchical';
    } else if (needs.includes('peer') || needs.includes('colleague')) {
      relationshipType = 'peer';
    }

    // Determine communication style
    const bio = (seeker.bio || '').toLowerCase();
    const isFormal = bio.includes('professional') || bio.includes('executive');
    const isTechnical = bio.includes('engineer') || bio.includes('developer') || bio.includes('technical');

    const communicationStyle: SocialContext['communicationStyle'] =
      isFormal ? 'formal' : isTechnical ? 'technical' : 'casual';

    // Assess trust level (based on existing connections)
    const trustLevel: SocialContext['trustLevel'] =
      metadata?.hasMutualConnections ? 'warm' :
      metadata?.hasReferences ? 'warm' : 'cold';

    return {
      relationshipType,
      culturalConsiderations: this.identifyCulturalFactors(seeker),
      communicationStyle,
      trustLevel,
      networkDynamics: 'semi-open'
    };
  }

  /**
   * Analyze economic context
   */
  private async analyzeEconomicContext(
    seeker: Contact,
    query?: string,
    metadata?: any
  ): Promise<EconomicContext> {
    const offerings = (seeker.offerings || []).join(' ').toLowerCase();
    const needs = (seeker.needs || []).join(' ').toLowerCase();

    // Determine value exchange type
    const hasMonetaryTerms = offerings.includes('payment') || offerings.includes('salary') ||
                             offerings.includes('equity') || needs.includes('funding');

    const valueExchange: EconomicContext['valueExchange'] =
      hasMonetaryTerms ? 'monetary' : 'non-monetary';

    // Assess budget constraints based on company stage
    const title = (seeker.title || '').toLowerCase();
    const isStartup = title.includes('founder') || metadata?.companyStage === 'startup';
    const isEnterprise = metadata?.companyStage === 'enterprise';

    const budgetConstraints: EconomicContext['budgetConstraints'] =
      isStartup ? 'tight' :
      isEnterprise ? 'flexible' : 'moderate';

    return {
      marketConditions: 'stable', // Could be enhanced with real market data
      budgetConstraints,
      valueExchange,
      competitivePressure: this.assessCompetitivePressure(seeker)
    };
  }

  /**
   * Analyze strategic context
   */
  private async analyzeStrategicContext(
    seeker: Contact,
    query?: string,
    metadata?: any
  ): Promise<StrategicContext> {
    const needs = (seeker.needs || []).join(' ').toLowerCase();

    // Determine primary goal
    let primaryGoal = 'networking';
    if (needs.includes('funding')) primaryGoal = 'raise capital';
    else if (needs.includes('hire') || needs.includes('talent')) primaryGoal = 'build team';
    else if (needs.includes('customer')) primaryGoal = 'acquire customers';
    else if (needs.includes('partner')) primaryGoal = 'form partnerships';

    // Determine growth stage
    const title = (seeker.title || '').toLowerCase();
    let growthStage: StrategicContext['growthStage'] = 'growth';

    if (title.includes('founder') && !metadata?.companyAge) {
      growthStage = 'startup';
    } else if (metadata?.companyStage) {
      growthStage = metadata.companyStage;
    }

    // Determine strategic priority
    const priorityKeywords = {
      speed: ['fast', 'quick', 'rapid', 'accelerate'],
      quality: ['best', 'top', 'excellent', 'premium', 'high-quality'],
      cost: ['affordable', 'cheap', 'cost-effective', 'budget'],
      innovation: ['innovative', 'cutting-edge', 'novel', 'breakthrough']
    };

    let strategicPriority: StrategicContext['strategicPriority'] = 'quality';
    const text = needs + ' ' + (seeker.bio || '').toLowerCase();

    for (const [priority, keywords] of Object.entries(priorityKeywords)) {
      if (keywords.some(k => text.includes(k))) {
        strategicPriority = priority as StrategicContext['strategicPriority'];
        break;
      }
    }

    return {
      primaryGoal,
      secondaryGoals: [],
      riskTolerance: growthStage === 'startup' ? 'aggressive' : 'moderate',
      growthStage,
      strategicPriority
    };
  }

  /**
   * Analyze environmental context
   */
  private async analyzeEnvironmentalContext(
    seeker: Contact,
    metadata?: any
  ): Promise<EnvironmentalContext> {
    const industry = seeker.industry || '';

    // Identify industry trends (simplified - could integrate with real trend data)
    const trendMap: Record<string, string[]> = {
      'Technology': ['AI/ML', 'Cloud Computing', 'Cybersecurity'],
      'Finance': ['FinTech', 'Crypto', 'Digital Banking'],
      'Healthcare': ['Telemedicine', 'AI Diagnostics', 'Personalized Medicine']
    };

    const industryTrends = trendMap[industry] || ['Digital Transformation'];

    // Assess technological change rate
    const techIndustries = ['Technology', 'Software', 'AI', 'Data'];
    const technologicalChange: EnvironmentalContext['technologicalChange'] =
      techIndustries.some(ti => industry.includes(ti)) ? 'rapid' : 'moderate';

    return {
      industryTrends,
      competitiveLandscape: 'competitive',
      regulatoryEnvironment: 'moderate',
      technologicalChange
    };
  }

  /**
   * Helper methods
   */

  private detectSeasonality(seeker: Contact): string | null {
    // Simplified seasonality detection
    const industry = (seeker.industry || '').toLowerCase();

    if (industry.includes('retail') || industry.includes('ecommerce')) {
      return 'Q4 peak (holidays)';
    }
    if (industry.includes('education')) {
      return 'Fall/Spring academic cycles';
    }

    return null;
  }

  private assessMarketTiming(seeker: Contact): 'early' | 'peak' | 'late' | 'unknown' {
    // Simplified market timing assessment
    return 'unknown'; // Would integrate with market data in production
  }

  private identifyCulturalFactors(seeker: Contact): string[] {
    const factors: string[] = [];
    const location = seeker.location || '';

    // Geographic cultural considerations
    if (location.includes('Asia') || location.includes('Japan') || location.includes('China')) {
      factors.push('Hierarchical communication');
    }
    if (location.includes('Europe')) {
      factors.push('Direct communication preferred');
    }
    if (location.includes('US') || location.includes('Silicon Valley')) {
      factors.push('Informal startup culture');
    }

    return factors;
  }

  private assessCompetitivePressure(seeker: Contact): 'high' | 'medium' | 'low' {
    const industry = (seeker.industry || '').toLowerCase();
    const title = (seeker.title || '').toLowerCase();

    // High competition industries/roles
    const highCompetition = ['technology', 'software', 'ai', 'startup'];
    if (highCompetition.some(hc => industry.includes(hc))) {
      return 'high';
    }

    if (title.includes('sales') || title.includes('business development')) {
      return 'high';
    }

    return 'medium';
  }

  /**
   * Generate context-aware recommendations
   */
  generateContextualRecommendations(context: MatchingContext): string[] {
    const recommendations: string[] = [];

    // Temporal recommendations
    if (context.temporal.urgency === 'immediate') {
      recommendations.push('Focus on immediately available candidates with high response rates');
    } else if (context.temporal.timeHorizon === 'long') {
      recommendations.push('Prioritize cultural fit and long-term compatibility');
    }

    // Social recommendations
    if (context.social.trustLevel === 'cold') {
      recommendations.push('Seek warm introductions through mutual connections');
    }

    if (context.social.relationshipType === 'mentorship') {
      recommendations.push('Look for experience differential of 5-10 years');
    }

    // Economic recommendations
    if (context.economic.budgetConstraints === 'tight') {
      recommendations.push('Consider non-monetary value exchange (equity, networking, etc.)');
    }

    // Strategic recommendations
    if (context.strategic.strategicPriority === 'speed') {
      recommendations.push('Prioritize availability and responsiveness over perfect fit');
    } else if (context.strategic.strategicPriority === 'quality') {
      recommendations.push('Be selective - wait for high-quality matches');
    }

    return recommendations;
  }
}
