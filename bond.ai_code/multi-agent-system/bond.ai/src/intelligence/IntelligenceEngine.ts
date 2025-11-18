/**
 * Intelligence Layer Module
 * AI analyzes profiles, interests, needs, and business activities
 * Pattern recognition identifies complementary matches
 * Behavioral algorithms predict relationship success probability
 */

import { Contact, IntelligenceAnalysis } from '../types';

export class IntelligenceEngine {
  private analysisCache: Map<string, IntelligenceAnalysis>;
  private config: {
    enableNeedsInference: boolean;
    enablePersonalityAnalysis: boolean;
    enableBehavioralPrediction: boolean;
  };

  constructor(config?: {
    enableNeedsInference?: boolean;
    enablePersonalityAnalysis?: boolean;
    enableBehavioralPrediction?: boolean;
  }) {
    this.analysisCache = new Map();
    this.config = {
      enableNeedsInference: config?.enableNeedsInference ?? true,
      enablePersonalityAnalysis: config?.enablePersonalityAnalysis ?? true,
      enableBehavioralPrediction: config?.enableBehavioralPrediction ?? true
    };
  }

  /**
   * Perform comprehensive intelligence analysis on a contact
   */
  async analyzeContact(contact: Contact): Promise<IntelligenceAnalysis> {
    // Check cache first
    const cached = this.analysisCache.get(contact.id);
    if (cached && this.isCacheValid(cached)) {
      return cached;
    }

    const analysis: IntelligenceAnalysis = {
      contactId: contact.id,
      profileAnalysis: await this.analyzeProfile(contact),
      needsAnalysis: await this.analyzeNeeds(contact),
      offeringsAnalysis: await this.analyzeOfferings(contact),
      personalityProfile: await this.analyzePersonality(contact),
      behavioralInsights: await this.analyzeBehavior(contact),
      timestamp: new Date()
    };

    this.analysisCache.set(contact.id, analysis);
    return analysis;
  }

  /**
   * Analyze contact profile to extract industries, expertise, career stage
   */
  private async analyzeProfile(contact: Contact): Promise<{
    industries: string[];
    expertiseAreas: string[];
    careerStage: string;
    influenceScore: number;
  }> {
    const industries = contact.industry ? [contact.industry] : [];

    // Extract expertise from skills and bio
    const expertiseAreas = new Set<string>(contact.skills || []);

    if (contact.bio) {
      // Simple keyword extraction for expertise
      const expertiseKeywords = this.extractExpertiseKeywords(contact.bio);
      expertiseKeywords.forEach(k => expertiseAreas.add(k));
    }

    // Determine career stage based on title and experience
    const careerStage = this.determineCareerStage(contact);

    // Calculate influence score based on various factors
    const influenceScore = this.calculateInfluenceScore(contact);

    return {
      industries,
      expertiseAreas: Array.from(expertiseAreas),
      careerStage,
      influenceScore
    };
  }

  /**
   * Analyze and infer needs from contact profile
   */
  private async analyzeNeeds(contact: Contact): Promise<{
    explicit: string[];
    implicit: string[];
    confidence: number;
  }> {
    const explicit = contact.needs || [];
    const implicit: string[] = [];

    if (this.config.enableNeedsInference) {
      // Infer needs based on title, company, and industry
      const inferredNeeds = this.inferNeeds(contact);
      implicit.push(...inferredNeeds);
    }

    return {
      explicit,
      implicit,
      confidence: explicit.length > 0 ? 0.9 : 0.6
    };
  }

  /**
   * Analyze offerings and capabilities
   */
  private async analyzeOfferings(contact: Contact): Promise<{
    explicit: string[];
    implicit: string[];
    confidence: number;
  }> {
    const explicit = contact.offerings || [];
    const implicit: string[] = [];

    // Infer offerings from skills and expertise
    if (contact.skills) {
      implicit.push(...contact.skills.map(s => `${s} expertise`));
    }

    return {
      explicit,
      implicit,
      confidence: explicit.length > 0 ? 0.9 : 0.7
    };
  }

  /**
   * Analyze personality traits from profile data
   */
  private async analyzePersonality(contact: Contact): Promise<{
    traits: Record<string, number>;
    communicationStyle: string;
    decisionMakingStyle: string;
  }> {
    if (!this.config.enablePersonalityAnalysis) {
      return {
        traits: {},
        communicationStyle: 'unknown',
        decisionMakingStyle: 'unknown'
      };
    }

    // Analyze bio and other text for personality indicators
    const traits = this.extractPersonalityTraits(contact);
    const communicationStyle = this.determineCommunicationStyle(contact);
    const decisionMakingStyle = this.determineDecisionMakingStyle(contact);

    return {
      traits,
      communicationStyle,
      decisionMakingStyle
    };
  }

  /**
   * Analyze behavioral patterns
   */
  private async analyzeBehavior(contact: Contact): Promise<{
    responsiveness: number;
    collaborationStyle: string;
    preferredChannels: string[];
  }> {
    if (!this.config.enableBehavioralPrediction) {
      return {
        responsiveness: 0.5,
        collaborationStyle: 'unknown',
        preferredChannels: []
      };
    }

    // Determine responsiveness from available data
    const responsiveness = this.estimateResponsiveness(contact);

    // Determine collaboration style
    const collaborationStyle = this.determineCollaborationStyle(contact);

    // Identify preferred communication channels
    const preferredChannels = this.identifyPreferredChannels(contact);

    return {
      responsiveness,
      collaborationStyle,
      preferredChannels
    };
  }

  /**
   * Calculate compatibility score between two contacts
   */
  calculateCompatibility(
    contact1: Contact,
    analysis1: IntelligenceAnalysis,
    contact2: Contact,
    analysis2: IntelligenceAnalysis
  ): {
    score: number;
    dimensions: {
      industryAlignment: number;
      needsMatch: number;
      personalityFit: number;
      expertiseComplementarity: number;
    };
  } {
    const industryAlignment = this.calculateIndustryAlignment(analysis1, analysis2);
    const needsMatch = this.calculateNeedsMatch(analysis1, analysis2);
    const personalityFit = this.calculatePersonalityFit(analysis1, analysis2);
    const expertiseComplementarity = this.calculateExpertiseComplementarity(analysis1, analysis2);

    const score = (
      industryAlignment * 0.2 +
      needsMatch * 0.4 +
      personalityFit * 0.2 +
      expertiseComplementarity * 0.2
    );

    return {
      score,
      dimensions: {
        industryAlignment,
        needsMatch,
        personalityFit,
        expertiseComplementarity
      }
    };
  }

  /**
   * Predict relationship success probability
   */
  predictSuccessProbability(
    contact1: Contact,
    analysis1: IntelligenceAnalysis,
    contact2: Contact,
    analysis2: IntelligenceAnalysis,
    connectionStrength: number
  ): number {
    const compatibility = this.calculateCompatibility(contact1, analysis1, contact2, analysis2);

    // Factors influencing success
    const responsivenessFactor = (
      analysis1.behavioralInsights.responsiveness +
      analysis2.behavioralInsights.responsiveness
    ) / 2;

    const connectionFactor = connectionStrength;

    // Weighted combination
    const probability = (
      compatibility.score * 0.5 +
      responsivenessFactor * 0.2 +
      connectionFactor * 0.3
    );

    return Math.min(Math.max(probability, 0), 1);
  }

  /**
   * Helper: Extract expertise keywords from bio
   */
  private extractExpertiseKeywords(bio: string): string[] {
    const keywords: string[] = [];
    const expertisePatterns = [
      /expert in ([\w\s]+)/gi,
      /specialized in ([\w\s]+)/gi,
      /focused on ([\w\s]+)/gi,
      /experienced with ([\w\s]+)/gi
    ];

    for (const pattern of expertisePatterns) {
      const matches = bio.matchAll(pattern);
      for (const match of matches) {
        keywords.push(match[1].trim().toLowerCase());
      }
    }

    return keywords;
  }

  /**
   * Helper: Determine career stage
   */
  private determineCareerStage(contact: Contact): string {
    const title = contact.title?.toLowerCase() || '';

    if (title.includes('chief') || title.includes('president') || title.includes('vp')) {
      return 'executive';
    } else if (title.includes('director') || title.includes('head of')) {
      return 'senior';
    } else if (title.includes('manager') || title.includes('lead')) {
      return 'mid-level';
    } else if (title.includes('senior')) {
      return 'senior';
    } else if (title.includes('junior') || title.includes('associate')) {
      return 'junior';
    }

    return 'mid-level';
  }

  /**
   * Helper: Calculate influence score
   */
  private calculateInfluenceScore(contact: Contact): number {
    let score = 0.5;

    // Adjust based on title
    const careerStage = this.determineCareerStage(contact);
    const stageMultipliers: Record<string, number> = {
      'executive': 1.5,
      'senior': 1.2,
      'mid-level': 1.0,
      'junior': 0.8
    };
    score *= stageMultipliers[careerStage] || 1.0;

    // Adjust based on skills count (proxy for expertise breadth)
    if (contact.skills && contact.skills.length > 5) {
      score *= 1.2;
    }

    return Math.min(score, 1);
  }

  /**
   * Helper: Infer needs based on contact profile
   */
  private inferNeeds(contact: Contact): string[] {
    const needs: string[] = [];
    const careerStage = this.determineCareerStage(contact);

    // Career stage-based needs
    if (careerStage === 'executive') {
      needs.push('strategic partnerships', 'board connections', 'investment opportunities');
    } else if (careerStage === 'junior') {
      needs.push('mentorship', 'skill development', 'networking');
    }

    // Industry-based needs
    if (contact.industry?.toLowerCase().includes('startup')) {
      needs.push('funding', 'talent acquisition', 'market expansion');
    }

    return needs;
  }

  /**
   * Helper: Extract personality traits
   */
  private extractPersonalityTraits(contact: Contact): Record<string, number> {
    const traits: Record<string, number> = {
      openness: 0.5,
      conscientiousness: 0.5,
      extraversion: 0.5,
      agreeableness: 0.5,
      neuroticism: 0.5
    };

    // Simple bio analysis
    if (contact.bio) {
      const bio = contact.bio.toLowerCase();

      if (bio.includes('innovative') || bio.includes('creative')) {
        traits.openness += 0.2;
      }
      if (bio.includes('organized') || bio.includes('detail')) {
        traits.conscientiousness += 0.2;
      }
      if (bio.includes('leadership') || bio.includes('team')) {
        traits.extraversion += 0.2;
      }
      if (bio.includes('collaborative') || bio.includes('supportive')) {
        traits.agreeableness += 0.2;
      }
    }

    // Normalize
    for (const key in traits) {
      traits[key] = Math.min(Math.max(traits[key], 0), 1);
    }

    return traits;
  }

  /**
   * Helper: Determine communication style
   */
  private determineCommunicationStyle(contact: Contact): string {
    if (contact.bio) {
      const bio = contact.bio.toLowerCase();
      if (bio.includes('direct') || bio.includes('concise')) return 'direct';
      if (bio.includes('collaborative') || bio.includes('discussion')) return 'collaborative';
      if (bio.includes('analytical') || bio.includes('data-driven')) return 'analytical';
    }
    return 'balanced';
  }

  /**
   * Helper: Determine decision-making style
   */
  private determineDecisionMakingStyle(contact: Contact): string {
    const careerStage = this.determineCareerStage(contact);

    if (careerStage === 'executive') return 'strategic';
    if (contact.bio?.toLowerCase().includes('data')) return 'analytical';
    if (contact.bio?.toLowerCase().includes('intuitive')) return 'intuitive';

    return 'balanced';
  }

  /**
   * Helper: Estimate responsiveness
   */
  private estimateResponsiveness(contact: Contact): number {
    // Default middle value
    let score = 0.5;

    // Adjust based on available social profiles (indicates active online presence)
    const profileCount = Object.keys(contact.socialProfiles || {}).length;
    score += profileCount * 0.1;

    return Math.min(score, 1);
  }

  /**
   * Helper: Determine collaboration style
   */
  private determineCollaborationStyle(contact: Contact): string {
    if (contact.bio) {
      const bio = contact.bio.toLowerCase();
      if (bio.includes('independent')) return 'independent';
      if (bio.includes('team player') || bio.includes('collaborative')) return 'collaborative';
      if (bio.includes('leader')) return 'leadership';
    }
    return 'flexible';
  }

  /**
   * Helper: Identify preferred channels
   */
  private identifyPreferredChannels(contact: Contact): string[] {
    const channels: string[] = [];

    if (contact.email) channels.push('email');
    if (contact.phone) channels.push('phone');
    if (contact.socialProfiles?.linkedin) channels.push('linkedin');
    if (contact.socialProfiles?.twitter) channels.push('twitter');

    return channels;
  }

  /**
   * Helper: Calculate industry alignment
   */
  private calculateIndustryAlignment(
    analysis1: IntelligenceAnalysis,
    analysis2: IntelligenceAnalysis
  ): number {
    const industries1 = new Set(analysis1.profileAnalysis.industries);
    const industries2 = new Set(analysis2.profileAnalysis.industries);

    const intersection = new Set([...industries1].filter(x => industries2.has(x)));
    const union = new Set([...industries1, ...industries2]);

    return union.size > 0 ? intersection.size / union.size : 0;
  }

  /**
   * Helper: Calculate needs match (complementary)
   */
  private calculateNeedsMatch(
    analysis1: IntelligenceAnalysis,
    analysis2: IntelligenceAnalysis
  ): number {
    const needs1 = new Set([
      ...analysis1.needsAnalysis.explicit,
      ...analysis1.needsAnalysis.implicit
    ]);
    const offerings2 = new Set([
      ...analysis2.offeringsAnalysis.explicit,
      ...analysis2.offeringsAnalysis.implicit
    ]);

    const needs2 = new Set([
      ...analysis2.needsAnalysis.explicit,
      ...analysis2.needsAnalysis.implicit
    ]);
    const offerings1 = new Set([
      ...analysis1.offeringsAnalysis.explicit,
      ...analysis1.offeringsAnalysis.implicit
    ]);

    // Check how many needs of contact1 are met by offerings of contact2 and vice versa
    let matchCount = 0;
    let totalNeeds = needs1.size + needs2.size;

    for (const need of needs1) {
      for (const offering of offerings2) {
        if (this.termsMatch(need, offering)) {
          matchCount++;
          break;
        }
      }
    }

    for (const need of needs2) {
      for (const offering of offerings1) {
        if (this.termsMatch(need, offering)) {
          matchCount++;
          break;
        }
      }
    }

    return totalNeeds > 0 ? matchCount / totalNeeds : 0;
  }

  /**
   * Helper: Calculate personality fit
   */
  private calculatePersonalityFit(
    analysis1: IntelligenceAnalysis,
    analysis2: IntelligenceAnalysis
  ): number {
    const traits1 = analysis1.personalityProfile.traits;
    const traits2 = analysis2.personalityProfile.traits;

    if (Object.keys(traits1).length === 0 || Object.keys(traits2).length === 0) {
      return 0.5; // neutral if no data
    }

    // Calculate similarity using normalized difference
    const traitKeys = Object.keys(traits1);
    const differences = traitKeys.map(key => {
      const val1 = traits1[key] || 0.5;
      const val2 = traits2[key] || 0.5;
      return Math.abs(val1 - val2);
    });

    const avgDifference = differences.reduce((sum, d) => sum + d, 0) / differences.length;

    // Convert difference to similarity (lower difference = higher fit)
    return 1 - avgDifference;
  }

  /**
   * Helper: Calculate expertise complementarity
   */
  private calculateExpertiseComplementarity(
    analysis1: IntelligenceAnalysis,
    analysis2: IntelligenceAnalysis
  ): number {
    const expertise1 = new Set(analysis1.profileAnalysis.expertiseAreas);
    const expertise2 = new Set(analysis2.profileAnalysis.expertiseAreas);

    // Complementarity: how different yet relevant the expertise is
    const overlap = new Set([...expertise1].filter(x => expertise2.has(x)));
    const total = new Set([...expertise1, ...expertise2]);

    // Some overlap is good (common ground), but complete overlap is less complementary
    const overlapRatio = total.size > 0 ? overlap.size / total.size : 0;

    // Optimal is around 30-50% overlap
    if (overlapRatio >= 0.3 && overlapRatio <= 0.5) {
      return 1.0;
    } else if (overlapRatio < 0.3) {
      return 0.5 + overlapRatio;
    } else {
      return 1.5 - overlapRatio;
    }
  }

  /**
   * Helper: Check if two terms match (fuzzy)
   */
  private termsMatch(term1: string, term2: string): boolean {
    const t1 = term1.toLowerCase().trim();
    const t2 = term2.toLowerCase().trim();

    // Exact match
    if (t1 === t2) return true;

    // Substring match
    if (t1.includes(t2) || t2.includes(t1)) return true;

    // Word overlap
    const words1 = t1.split(/\s+/);
    const words2 = t2.split(/\s+/);
    const commonWords = words1.filter(w => words2.includes(w));

    return commonWords.length >= Math.min(words1.length, words2.length) / 2;
  }

  /**
   * Helper: Check if cache is valid (24 hours)
   */
  private isCacheValid(analysis: IntelligenceAnalysis): boolean {
    const cacheAge = Date.now() - analysis.timestamp.getTime();
    const maxAge = 24 * 60 * 60 * 1000; // 24 hours
    return cacheAge < maxAge;
  }

  /**
   * Clear analysis cache
   */
  clearCache(): void {
    this.analysisCache.clear();
  }

  /**
   * Get cached analysis
   */
  getCachedAnalysis(contactId: string): IntelligenceAnalysis | undefined {
    return this.analysisCache.get(contactId);
  }
}
