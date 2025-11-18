/**
 * Dynamic Matching Strategy Selector
 *
 * Intelligently analyzes ANY type of request and dynamically selects/combines
 * matching strategies without relying on predefined scenarios.
 *
 * Key Features:
 * - Semantic request analysis and intent extraction
 * - Dynamic weight adjustment based on request context
 * - Multi-dimensional matching with adaptive strategies
 * - Strategy combination and optimization
 * - Confidence scoring and explanation generation
 */

import { Contact, Match } from '../types';
import { IntelligenceEngine } from '../intelligence/IntelligenceEngine';

export interface MatchingRequest {
  seeker: Contact;
  query?: string; // Natural language query (optional)
  constraints?: {
    industries?: string[];
    locations?: string[];
    experienceRange?: { min: number; max: number };
    maxResults?: number;
    minConfidence?: number;
  };
  context?: {
    urgency?: 'low' | 'medium' | 'high' | 'immediate';
    relationship?: 'one-time' | 'ongoing' | 'long-term';
    formality?: 'casual' | 'professional' | 'formal';
  };
}

export interface MatchingStrategy {
  name: string;
  weight: number;
  dimensions: string[];
  scoringFunction: (seeker: Contact, candidate: Contact) => number;
  confidence: number;
}

export interface DynamicMatchResult {
  candidate: Contact;
  score: number;
  confidence: number;
  strategies: Array<{
    name: string;
    contribution: number;
    dimensions: string[];
  }>;
  explanations: string[];
  matchType: string;
}

export class DynamicMatchingStrategySelector {
  private intelligenceEngine: IntelligenceEngine;
  private semanticAnalyzer: SemanticRequestAnalyzer;
  private weightingAgent: AdaptiveWeightingAgent;
  private intentClassifier: IntentClassificationAgent;

  constructor(intelligenceEngine: IntelligenceEngine) {
    this.intelligenceEngine = intelligenceEngine;
    this.semanticAnalyzer = new SemanticRequestAnalyzer();
    this.weightingAgent = new AdaptiveWeightingAgent();
    this.intentClassifier = new IntentClassificationAgent();
  }

  /**
   * Main entry point: Analyze request and find best matches dynamically
   */
  async findMatches(
    request: MatchingRequest,
    candidates: Contact[]
  ): Promise<DynamicMatchResult[]> {
    // Step 1: Analyze the request semantically
    const requestAnalysis = await this.semanticAnalyzer.analyze(request);

    // Step 2: Classify intent and extract requirements
    const intent = await this.intentClassifier.classify(requestAnalysis);

    // Step 3: Dynamically select and combine strategies
    const strategies = await this.selectStrategies(requestAnalysis, intent);

    // Step 4: Calculate adaptive weights based on context
    const weights = this.weightingAgent.calculateWeights(requestAnalysis, intent, strategies);

    // Step 5: Score all candidates using combined strategies
    const results = await this.scoreAllCandidates(
      request.seeker,
      candidates,
      strategies,
      weights,
      requestAnalysis
    );

    // Step 6: Filter by constraints and confidence
    const filtered = this.applyConstraints(results, request.constraints || {});

    // Step 7: Sort and limit results
    const sorted = filtered.sort((a, b) => b.score - a.score);
    const limit = request.constraints?.maxResults || 20;

    return sorted.slice(0, limit);
  }

  /**
   * Dynamically select matching strategies based on request analysis
   */
  private async selectStrategies(
    requestAnalysis: RequestAnalysis,
    intent: IntentClassification
  ): Promise<MatchingStrategy[]> {
    const strategies: MatchingStrategy[] = [];

    // Always include needs-based matching (core strategy)
    strategies.push(this.createNeedsMatchingStrategy());

    // Add strategies based on detected dimensions
    if (requestAnalysis.hasTechnicalRequirements) {
      strategies.push(this.createSkillsMatchingStrategy());
    }

    if (requestAnalysis.hasIndustryFocus) {
      strategies.push(this.createIndustryAlignmentStrategy());
    }

    if (requestAnalysis.hasExperienceRequirements) {
      strategies.push(this.createExperienceMatchingStrategy());
    }

    if (requestAnalysis.hasGeographicPreference) {
      strategies.push(this.createGeographicMatchingStrategy());
    }

    if (requestAnalysis.hasNetworkImportance) {
      strategies.push(this.createNetworkAccessStrategy());
    }

    if (requestAnalysis.hasQualityRequirements) {
      strategies.push(this.createQualityMatchingStrategy());
    }

    // Intent-based strategies
    if (intent.type === 'resource_acquisition') {
      strategies.push(this.createResourceAvailabilityStrategy());
    }

    if (intent.type === 'knowledge_seeking') {
      strategies.push(this.createExpertiseComplementarityStrategy());
    }

    if (intent.type === 'collaboration') {
      strategies.push(this.createComplementarityStrategy());
    }

    if (intent.type === 'transaction') {
      strategies.push(this.createCommercialFitStrategy());
    }

    // Always add personality/cultural fit for relationship-based matches
    if (intent.relationshipOriented) {
      strategies.push(this.createPersonalityFitStrategy());
    }

    return strategies;
  }

  /**
   * Score all candidates using combined strategies
   */
  private async scoreAllCandidates(
    seeker: Contact,
    candidates: Contact[],
    strategies: MatchingStrategy[],
    weights: Map<string, number>,
    requestAnalysis: RequestAnalysis
  ): Promise<DynamicMatchResult[]> {
    const results: DynamicMatchResult[] = [];

    for (const candidate of candidates) {
      const result = await this.scoreCandidate(
        seeker,
        candidate,
        strategies,
        weights,
        requestAnalysis
      );
      results.push(result);
    }

    return results;
  }

  /**
   * Score a single candidate using all strategies
   */
  private async scoreCandidate(
    seeker: Contact,
    candidate: Contact,
    strategies: MatchingStrategy[],
    weights: Map<string, number>,
    requestAnalysis: RequestAnalysis
  ): Promise<DynamicMatchResult> {
    let totalScore = 0;
    let totalWeight = 0;
    const strategyResults: Array<{
      name: string;
      contribution: number;
      dimensions: string[];
    }> = [];

    // Apply each strategy
    for (const strategy of strategies) {
      const strategyScore = strategy.scoringFunction(seeker, candidate);
      const weight = weights.get(strategy.name) || strategy.weight;
      const contribution = strategyScore * weight;

      totalScore += contribution;
      totalWeight += weight;

      strategyResults.push({
        name: strategy.name,
        contribution,
        dimensions: strategy.dimensions
      });
    }

    // Normalize score
    const finalScore = totalWeight > 0 ? totalScore / totalWeight : 0;

    // Calculate confidence based on data completeness
    const confidence = this.calculateConfidence(seeker, candidate, strategies);

    // Generate explanations
    const explanations = this.generateExplanations(
      strategyResults,
      seeker,
      candidate,
      requestAnalysis
    );

    // Determine match type
    const matchType = this.determineMatchType(finalScore, strategyResults);

    return {
      candidate,
      score: finalScore,
      confidence,
      strategies: strategyResults.sort((a, b) => b.contribution - a.contribution),
      explanations,
      matchType
    };
  }

  /**
   * Strategy Creation Methods
   */

  private createNeedsMatchingStrategy(): MatchingStrategy {
    return {
      name: 'Needs-Based Matching',
      weight: 0.40,
      dimensions: ['needs', 'offerings'],
      scoringFunction: (seeker, candidate) => {
        const seekerNeeds = new Set((seeker.needs || []).map(n => n.toLowerCase()));
        const candidateOfferings = new Set((candidate.offerings || []).map(o => o.toLowerCase()));
        const candidateNeeds = new Set((candidate.needs || []).map(n => n.toLowerCase()));
        const seekerOfferings = new Set((seeker.offerings || []).map(o => o.toLowerCase()));

        let matches = 0;
        let total = seekerNeeds.size + candidateNeeds.size;

        if (total === 0) return 0.5; // Neutral if no needs/offerings defined

        // Bidirectional matching
        for (const need of seekerNeeds) {
          if (this.matchesAny(need, Array.from(candidateOfferings))) {
            matches++;
          }
        }

        for (const need of candidateNeeds) {
          if (this.matchesAny(need, Array.from(seekerOfferings))) {
            matches++;
          }
        }

        return total > 0 ? matches / total : 0.5;
      },
      confidence: 0.85
    };
  }

  private createSkillsMatchingStrategy(): MatchingStrategy {
    return {
      name: 'Skills & Expertise Matching',
      weight: 0.25,
      dimensions: ['skills', 'expertise'],
      scoringFunction: (seeker, candidate) => {
        const seekerSkills = new Set((seeker.skills || []).map(s => s.toLowerCase()));
        const candidateSkills = new Set((candidate.skills || []).map(s => s.toLowerCase()));

        // Check if seeker needs skills that candidate has
        const seekerNeeds = new Set((seeker.needs || []).map(n => n.toLowerCase()));
        let skillMatches = 0;

        for (const need of seekerNeeds) {
          for (const skill of candidateSkills) {
            if (this.semanticMatch(need, skill)) {
              skillMatches++;
            }
          }
        }

        // Also check complementary skills
        const commonSkills = [...seekerSkills].filter(s => candidateSkills.has(s));
        const complementaryScore = 1 - (commonSkills.length / Math.max(seekerSkills.size, 1));

        // Combine: 70% need-based, 30% complementary
        return (skillMatches / Math.max(seekerNeeds.size, 1)) * 0.7 + complementaryScore * 0.3;
      },
      confidence: 0.80
    };
  }

  private createIndustryAlignmentStrategy(): MatchingStrategy {
    return {
      name: 'Industry Alignment',
      weight: 0.15,
      dimensions: ['industry'],
      scoringFunction: (seeker, candidate) => {
        if (!seeker.industry || !candidate.industry) return 0.5;

        const seekerInd = seeker.industry.toLowerCase();
        const candInd = candidate.industry.toLowerCase();

        if (seekerInd === candInd) return 1.0;
        if (this.areRelatedIndustries(seekerInd, candInd)) return 0.7;

        return 0.3;
      },
      confidence: 0.90
    };
  }

  private createExperienceMatchingStrategy(): MatchingStrategy {
    return {
      name: 'Experience Level Matching',
      weight: 0.15,
      dimensions: ['experience', 'seniority'],
      scoringFunction: (seeker, candidate) => {
        const seekerExp = this.extractExperienceLevel(seeker);
        const candidateExp = this.extractExperienceLevel(candidate);

        const diff = Math.abs(seekerExp - candidateExp);

        // Complementary experience (3-10 years difference) is good for mentorship
        if (diff >= 3 && diff <= 10) return 0.9;

        // Similar experience is good for peer collaboration
        if (diff <= 2) return 0.85;

        // Large gap might still work for certain scenarios
        return Math.max(0.3, 1 - (diff * 0.05));
      },
      confidence: 0.70
    };
  }

  private createGeographicMatchingStrategy(): MatchingStrategy {
    return {
      name: 'Geographic Proximity',
      weight: 0.10,
      dimensions: ['location', 'geography'],
      scoringFunction: (seeker, candidate) => {
        if (!seeker.location || !candidate.location) return 0.5;

        const seekerLoc = seeker.location.toLowerCase();
        const candLoc = candidate.location.toLowerCase();

        if (seekerLoc === candLoc) return 1.0;

        // Same city
        if (seekerLoc.split(',')[0] === candLoc.split(',')[0]) return 0.9;

        // Same state/country
        if (this.sameRegion(seekerLoc, candLoc)) return 0.6;

        return 0.3;
      },
      confidence: 0.75
    };
  }

  private createNetworkAccessStrategy(): MatchingStrategy {
    return {
      name: 'Network Access & Influence',
      weight: 0.20,
      dimensions: ['network', 'influence'],
      scoringFunction: (seeker, candidate) => {
        const candidateInfluence = candidate.metadata?.networkInfluence || 'medium';
        const candidateConnections = candidate.metadata?.connectionsCount || 100;

        let score = 0.5;

        // Influence level
        if (candidateInfluence === 'expert') score += 0.3;
        else if (candidateInfluence === 'high') score += 0.2;
        else if (candidateInfluence === 'medium') score += 0.1;

        // Network size
        if (candidateConnections > 500) score += 0.2;
        else if (candidateConnections > 200) score += 0.1;

        return Math.min(1.0, score);
      },
      confidence: 0.65
    };
  }

  private createQualityMatchingStrategy(): MatchingStrategy {
    return {
      name: 'Profile Quality & Reliability',
      weight: 0.10,
      dimensions: ['quality', 'verification'],
      scoringFunction: (seeker, candidate) => {
        let score = 0.5;

        if (candidate.metadata?.verified) score += 0.2;
        if (candidate.metadata?.profileQuality && candidate.metadata.profileQuality > 0.7) score += 0.15;
        if (candidate.metadata?.recommendationsCount && candidate.metadata.recommendationsCount > 3) score += 0.15;

        return Math.min(1.0, score);
      },
      confidence: 0.80
    };
  }

  private createResourceAvailabilityStrategy(): MatchingStrategy {
    return {
      name: 'Resource Availability',
      weight: 0.15,
      dimensions: ['availability', 'capacity'],
      scoringFunction: (seeker, candidate) => {
        const availability = candidate.metadata?.availability || 'unknown';
        const lastActive = candidate.metadata?.lastActive;

        let score = 0.5;

        if (availability === 'immediate') score = 0.9;
        else if (availability === 'available') score = 0.7;

        if (lastActive) {
          const daysSince = this.getDaysSince(lastActive);
          if (daysSince < 7) score += 0.1;
        }

        return Math.min(1.0, score);
      },
      confidence: 0.70
    };
  }

  private createExpertiseComplementarityStrategy(): MatchingStrategy {
    return {
      name: 'Expertise Complementarity',
      weight: 0.25,
      dimensions: ['expertise', 'knowledge'],
      scoringFunction: (seeker, candidate) => {
        const seekerSkills = new Set((seeker.skills || []).map(s => s.toLowerCase()));
        const candidateSkills = new Set((candidate.skills || []).map(s => s.toLowerCase()));

        const allSkills = new Set([...seekerSkills, ...candidateSkills]);
        const overlap = [...seekerSkills].filter(s => candidateSkills.has(s)).length;

        // High complementarity = low overlap but relevant skills
        const complementarity = 1 - (overlap / Math.max(allSkills.size, 1));

        return complementarity;
      },
      confidence: 0.75
    };
  }

  private createComplementarityStrategy(): MatchingStrategy {
    return {
      name: 'Overall Complementarity',
      weight: 0.20,
      dimensions: ['skills', 'offerings', 'strengths'],
      scoringFunction: (seeker, candidate) => {
        // Combines skill complementarity with offerings complementarity
        const skillComp = this.createExpertiseComplementarityStrategy().scoringFunction(seeker, candidate);

        const seekerOfferings = new Set((seeker.offerings || []).map(o => o.toLowerCase()));
        const candidateOfferings = new Set((candidate.offerings || []).map(o => o.toLowerCase()));
        const allOfferings = new Set([...seekerOfferings, ...candidateOfferings]);
        const offerOverlap = [...seekerOfferings].filter(o => candidateOfferings.has(o)).length;
        const offerComp = allOfferings.size > 0 ? 1 - (offerOverlap / allOfferings.size) : 0.5;

        return (skillComp + offerComp) / 2;
      },
      confidence: 0.75
    };
  }

  private createCommercialFitStrategy(): MatchingStrategy {
    return {
      name: 'Commercial Fit',
      weight: 0.20,
      dimensions: ['budget', 'pricing', 'terms'],
      scoringFunction: (seeker, candidate) => {
        // Simplified - in real implementation would check budget alignment,
        // payment terms, pricing expectations, etc.
        let score = 0.6; // Default moderate fit

        // Check if both have commercial intent
        const seekerCommercial = (seeker.offerings || []).some(o =>
          o.toLowerCase().includes('purchase') || o.toLowerCase().includes('buy')
        );
        const candidateCommercial = (candidate.offerings || []).some(o =>
          o.toLowerCase().includes('sell') || o.toLowerCase().includes('service')
        );

        if (seekerCommercial && candidateCommercial) score = 0.8;

        return score;
      },
      confidence: 0.60
    };
  }

  private createPersonalityFitStrategy(): MatchingStrategy {
    return {
      name: 'Personality & Cultural Fit',
      weight: 0.15,
      dimensions: ['personality', 'culture', 'values'],
      scoringFunction: (seeker, candidate) => {
        // Simplified - in real implementation would use personality analysis
        // from IntelligenceEngine
        return 0.7; // Default moderate fit
      },
      confidence: 0.65
    };
  }

  /**
   * Helper Methods
   */

  private matchesAny(term: string, items: string[]): boolean {
    return items.some(item =>
      item.includes(term) || term.includes(item) || this.semanticMatch(term, item)
    );
  }

  private semanticMatch(term1: string, term2: string): boolean {
    // Simple semantic matching - can be enhanced with NLP
    const synonyms: Record<string, string[]> = {
      'developer': ['engineer', 'programmer', 'coder', 'software developer'],
      'funding': ['investment', 'capital', 'financing', 'money'],
      'mentor': ['advisor', 'coach', 'guide'],
      'partner': ['collaboration', 'partnership', 'ally'],
    };

    for (const [key, syns] of Object.entries(synonyms)) {
      if ((term1.includes(key) || syns.some(s => term1.includes(s))) &&
          (term2.includes(key) || syns.some(s => term2.includes(s)))) {
        return true;
      }
    }

    return false;
  }

  private areRelatedIndustries(ind1: string, ind2: string): boolean {
    const related: Record<string, string[]> = {
      'technology': ['software', 'saas', 'it', 'tech'],
      'finance': ['fintech', 'banking', 'investment'],
      'healthcare': ['healthtech', 'medical', 'biotech'],
    };

    for (const [key, rels] of Object.entries(related)) {
      if ((ind1.includes(key) || rels.some(r => ind1.includes(r))) &&
          (ind2.includes(key) || rels.some(r => ind2.includes(r)))) {
        return true;
      }
    }

    return false;
  }

  private extractExperienceLevel(contact: Contact): number {
    return contact.metadata?.experienceYears || 5;
  }

  private sameRegion(loc1: string, loc2: string): boolean {
    const parts1 = loc1.split(',').map(p => p.trim());
    const parts2 = loc2.split(',').map(p => p.trim());

    return parts1.length > 1 && parts2.length > 1 && parts1[1] === parts2[1];
  }

  private getDaysSince(dateString: string): number {
    const date = new Date(dateString);
    const now = new Date();
    return Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24));
  }

  private calculateConfidence(
    seeker: Contact,
    candidate: Contact,
    strategies: MatchingStrategy[]
  ): number {
    // Confidence based on data completeness
    let dataPoints = 0;
    let totalPossible = 10;

    if (seeker.needs && seeker.needs.length > 0) dataPoints++;
    if (seeker.offerings && seeker.offerings.length > 0) dataPoints++;
    if (seeker.skills && seeker.skills.length > 0) dataPoints++;
    if (seeker.industry) dataPoints++;
    if (seeker.location) dataPoints++;

    if (candidate.needs && candidate.needs.length > 0) dataPoints++;
    if (candidate.offerings && candidate.offerings.length > 0) dataPoints++;
    if (candidate.skills && candidate.skills.length > 0) dataPoints++;
    if (candidate.industry) dataPoints++;
    if (candidate.location) dataPoints++;

    const dataCompleteness = dataPoints / totalPossible;

    // Average strategy confidence
    const avgStrategyConfidence = strategies.reduce((sum, s) => sum + s.confidence, 0) / strategies.length;

    return (dataCompleteness * 0.6) + (avgStrategyConfidence * 0.4);
  }

  private generateExplanations(
    strategyResults: Array<{ name: string; contribution: number; dimensions: string[] }>,
    seeker: Contact,
    candidate: Contact,
    requestAnalysis: RequestAnalysis
  ): string[] {
    const explanations: string[] = [];

    // Top 3 contributing strategies
    const topStrategies = strategyResults
      .sort((a, b) => b.contribution - a.contribution)
      .slice(0, 3);

    for (const strategy of topStrategies) {
      if (strategy.contribution > 0.1) {
        explanations.push(`${strategy.name}: ${(strategy.contribution * 100).toFixed(1)}% contribution`);
      }
    }

    return explanations;
  }

  private determineMatchType(
    score: number,
    strategyResults: Array<{ name: string; contribution: number }>
  ): string {
    if (score >= 0.8) return 'Excellent Match';
    if (score >= 0.65) return 'Strong Match';
    if (score >= 0.5) return 'Good Match';
    if (score >= 0.35) return 'Moderate Match';
    return 'Weak Match';
  }

  private applyConstraints(
    results: DynamicMatchResult[],
    constraints: MatchingRequest['constraints']
  ): DynamicMatchResult[] {
    let filtered = results;

    if (constraints.industries && constraints.industries.length > 0) {
      filtered = filtered.filter(r =>
        constraints.industries!.some(ind =>
          r.candidate.industry?.toLowerCase().includes(ind.toLowerCase())
        )
      );
    }

    if (constraints.locations && constraints.locations.length > 0) {
      filtered = filtered.filter(r =>
        constraints.locations!.some(loc =>
          r.candidate.location?.toLowerCase().includes(loc.toLowerCase())
        )
      );
    }

    if (constraints.minConfidence) {
      filtered = filtered.filter(r => r.confidence >= constraints.minConfidence!);
    }

    return filtered;
  }
}

/**
 * Supporting Classes
 */

interface RequestAnalysis {
  hasTechnicalRequirements: boolean;
  hasIndustryFocus: boolean;
  hasExperienceRequirements: boolean;
  hasGeographicPreference: boolean;
  hasNetworkImportance: boolean;
  hasQualityRequirements: boolean;
  extractedTerms: string[];
  confidence: number;
}

class SemanticRequestAnalyzer {
  async analyze(request: MatchingRequest): Promise<RequestAnalysis> {
    const needs = request.seeker.needs || [];
    const offerings = request.seeker.offerings || [];
    const skills = request.seeker.skills || [];
    const query = request.query || '';

    const allText = [...needs, ...offerings, ...skills, query].join(' ').toLowerCase();

    return {
      hasTechnicalRequirements: this.hasTechnical(allText),
      hasIndustryFocus: !!request.seeker.industry,
      hasExperienceRequirements: this.hasExperience(allText),
      hasGeographicPreference: !!request.seeker.location || !!request.constraints?.locations,
      hasNetworkImportance: this.hasNetwork(allText),
      hasQualityRequirements: this.hasQuality(allText),
      extractedTerms: this.extractKeyTerms(allText),
      confidence: 0.8
    };
  }

  private hasTechnical(text: string): boolean {
    const techKeywords = ['developer', 'engineer', 'programming', 'software', 'technical', 'code', 'design', 'data'];
    return techKeywords.some(k => text.includes(k));
  }

  private hasExperience(text: string): boolean {
    const expKeywords = ['senior', 'junior', 'experienced', 'years', 'expert', 'novice'];
    return expKeywords.some(k => text.includes(k));
  }

  private hasNetwork(text: string): boolean {
    const networkKeywords = ['network', 'connections', 'introduction', 'access', 'influence'];
    return networkKeywords.some(k => text.includes(k));
  }

  private hasQuality(text: string): boolean {
    const qualityKeywords = ['verified', 'certified', 'reputable', 'trusted', 'experienced'];
    return qualityKeywords.some(k => text.includes(k));
  }

  private extractKeyTerms(text: string): string[] {
    // Simple extraction - can be enhanced with NLP
    return text.split(/\s+/).filter(term => term.length > 3);
  }
}

interface IntentClassification {
  type: 'resource_acquisition' | 'knowledge_seeking' | 'collaboration' | 'transaction' | 'networking' | 'general';
  relationshipOriented: boolean;
  confidence: number;
}

class IntentClassificationAgent {
  async classify(analysis: RequestAnalysis): Promise<IntentClassification> {
    // Classify based on extracted terms and patterns
    const terms = analysis.extractedTerms.join(' ');

    if (terms.includes('hire') || terms.includes('recruit') || terms.includes('talent')) {
      return { type: 'resource_acquisition', relationshipOriented: true, confidence: 0.85 };
    }

    if (terms.includes('mentor') || terms.includes('learn') || terms.includes('advice')) {
      return { type: 'knowledge_seeking', relationshipOriented: true, confidence: 0.80 };
    }

    if (terms.includes('partner') || terms.includes('collaborate') || terms.includes('cofounder')) {
      return { type: 'collaboration', relationshipOriented: true, confidence: 0.85 };
    }

    if (terms.includes('buy') || terms.includes('sell') || terms.includes('supplier')) {
      return { type: 'transaction', relationshipOriented: false, confidence: 0.75 };
    }

    if (terms.includes('network') || terms.includes('connection') || terms.includes('introduction')) {
      return { type: 'networking', relationshipOriented: true, confidence: 0.80 };
    }

    return { type: 'general', relationshipOriented: true, confidence: 0.60 };
  }
}

class AdaptiveWeightingAgent {
  calculateWeights(
    analysis: RequestAnalysis,
    intent: IntentClassification,
    strategies: MatchingStrategy[]
  ): Map<string, number> {
    const weights = new Map<string, number>();

    for (const strategy of strategies) {
      let weight = strategy.weight;

      // Adjust based on intent
      if (intent.type === 'resource_acquisition' && strategy.name.includes('Availability')) {
        weight *= 1.5;
      }

      if (intent.type === 'knowledge_seeking' && strategy.name.includes('Expertise')) {
        weight *= 1.4;
      }

      if (intent.type === 'collaboration' && strategy.name.includes('Complementarity')) {
        weight *= 1.3;
      }

      // Adjust based on data availability
      if (analysis.hasTechnicalRequirements && strategy.name.includes('Skills')) {
        weight *= 1.2;
      }

      weights.set(strategy.name, weight);
    }

    return weights;
  }
}

export { SemanticRequestAnalyzer, IntentClassificationAgent, AdaptiveWeightingAgent };
