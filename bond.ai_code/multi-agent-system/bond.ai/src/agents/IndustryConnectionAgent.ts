/**
 * Industry Connection Agent
 * Specializes in finding connections to specific industries, sectors, or companies
 * Focuses on network access, influence, and relationship strength
 */

import { Contact, Match } from '../types';

export interface IndustryConnectionProfile {
  industries: string[];
  companies: string[]; // Current and previous companies
  positions: string[]; // Current and previous titles
  networkInfluence: 'low' | 'medium' | 'high' | 'expert';
  yearsInIndustry: number;
  boardPositions?: string[];
  advisoryRoles?: string[];
  investorIn?: string[]; // If they're an investor
  speaksAt?: string[]; // Conferences, events
  publishedWork?: string[]; // Articles, books, research
  professionalGroups?: string[]; // Industry associations
  geographicReach?: string[]; // Regions/countries they have connections in
}

export interface IndustryConnectionNeed {
  targetIndustry: string;
  targetCompanies?: string[]; // Specific companies to connect to
  targetRoles?: string[]; // Types of people to connect with
  purpose: 'fundraising' | 'partnership' | 'sales' | 'hiring' | 'market_entry' | 'advisory';
  geographicPreference?: string[];
  urgency: 'low' | 'medium' | 'high';
  relationshipDepth: 'introduction' | 'warm_connection' | 'deep_relationship';
}

export class IndustryConnectionAgent {
  private industryHierarchy: Map<string, string[]>;
  private companyToIndustry: Map<string, string>;

  constructor() {
    this.industryHierarchy = this.initializeIndustryHierarchy();
    this.companyToIndustry = this.initializeCompanyToIndustry();
  }

  /**
   * Match a connector with an industry connection need
   */
  matchIndustryConnection(
    connector: Contact,
    need: IndustryConnectionNeed
  ): {
    score: number;
    breakdown: {
      industryAccess: number;
      companyAccess: number;
      networkStrength: number;
      influenceLevel: number;
      purposeAlignment: number;
    };
    connectionPaths: string[];
    estimatedIntroQuality: 'cold' | 'warm' | 'hot';
    recommendation: string;
  } {
    const profile = this.extractIndustryProfile(connector);

    // Calculate dimensions
    const industryAccess = this.calculateIndustryAccess(profile, need);
    const companyAccess = this.calculateCompanyAccess(profile, need);
    const networkStrength = this.calculateNetworkStrength(profile, need);
    const influenceLevel = this.calculateInfluenceLevel(profile, need);
    const purposeAlignment = this.calculatePurposeAlignment(profile, need);

    // Weighted score
    const score = (
      industryAccess * 0.30 +
      companyAccess * 0.25 +
      networkStrength * 0.25 +
      influenceLevel * 0.15 +
      purposeAlignment * 0.05
    );

    // Analyze connection paths
    const connectionPaths = this.identifyConnectionPaths(profile, need);

    // Estimate intro quality
    const estimatedIntroQuality = this.estimateIntroductionQuality(
      score,
      profile,
      need
    );

    // Generate recommendation
    const recommendation = this.generateRecommendation(
      score,
      profile,
      need,
      connectionPaths,
      estimatedIntroQuality
    );

    return {
      score,
      breakdown: {
        industryAccess,
        companyAccess,
        networkStrength,
        influenceLevel,
        purposeAlignment,
      },
      connectionPaths,
      estimatedIntroQuality,
      recommendation,
    };
  }

  /**
   * Calculate industry access score
   */
  private calculateIndustryAccess(
    profile: IndustryConnectionProfile,
    need: IndustryConnectionNeed
  ): number {
    const targetIndustry = need.targetIndustry.toLowerCase();
    const connectorIndustries = profile.industries.map(i => i.toLowerCase());

    // Direct industry match
    if (connectorIndustries.includes(targetIndustry)) {
      // Boost for years in industry
      const yearBoost = Math.min(0.2, profile.yearsInIndustry * 0.02);
      return Math.min(1.0, 0.8 + yearBoost);
    }

    // Related industry match
    const relatedScore = this.getRelatedIndustryAccess(
      connectorIndustries,
      targetIndustry
    );

    return relatedScore;
  }

  /**
   * Get related industry access score
   */
  private getRelatedIndustryAccess(connectorIndustries: string[], target: string): number {
    const relatedIndustries = this.industryHierarchy.get(target) || [];

    for (const industry of connectorIndustries) {
      if (relatedIndustries.includes(industry)) {
        return 0.6; // Related industry access
      }
    }

    return connectorIndustries.length > 0 ? 0.3 : 0.1;
  }

  /**
   * Calculate company access score
   */
  private calculateCompanyAccess(
    profile: IndustryConnectionProfile,
    need: IndustryConnectionNeed
  ): number {
    if (!need.targetCompanies || need.targetCompanies.length === 0) {
      return 0.5; // Not specified, neutral score
    }

    const connectorCompanies = new Set(
      profile.companies.map(c => c.toLowerCase())
    );

    const targetCompanies = need.targetCompanies.map(c => c.toLowerCase());

    // Direct company match (current or previous)
    for (const target of targetCompanies) {
      if (connectorCompanies.has(target)) {
        return 1.0; // Direct insider access
      }
    }

    // Check if connector's companies are in same industry
    let sameIndustryCount = 0;
    for (const company of profile.companies) {
      const industry = this.companyToIndustry.get(company.toLowerCase());
      if (industry && industry === need.targetIndustry.toLowerCase()) {
        sameIndustryCount++;
      }
    }

    if (sameIndustryCount > 0) {
      return 0.6 + (sameIndustryCount * 0.1); // Likely has connections
    }

    return 0.3; // Limited company access
  }

  /**
   * Calculate network strength
   */
  private calculateNetworkStrength(
    profile: IndustryConnectionProfile,
    need: IndustryConnectionNeed
  ): number {
    let score = 0.3; // Base score

    // Network influence
    const influenceScores = {
      'expert': 0.40,
      'high': 0.30,
      'medium': 0.15,
      'low': 0.05,
    };
    score += influenceScores[profile.networkInfluence];

    // Board positions
    if (profile.boardPositions && profile.boardPositions.length > 0) {
      score += Math.min(0.15, profile.boardPositions.length * 0.05);
    }

    // Advisory roles
    if (profile.advisoryRoles && profile.advisoryRoles.length > 0) {
      score += Math.min(0.10, profile.advisoryRoles.length * 0.03);
    }

    // Professional groups
    if (profile.professionalGroups && profile.professionalGroups.length > 0) {
      score += Math.min(0.10, profile.professionalGroups.length * 0.02);
    }

    // Geographic reach match
    if (need.geographicPreference && profile.geographicReach) {
      const hasGeoMatch = need.geographicPreference.some(geo =>
        profile.geographicReach!.some(reach =>
          reach.toLowerCase().includes(geo.toLowerCase())
        )
      );
      if (hasGeoMatch) {
        score += 0.10;
      }
    }

    return Math.min(1.0, score);
  }

  /**
   * Calculate influence level
   */
  private calculateInfluenceLevel(
    profile: IndustryConnectionProfile,
    need: IndustryConnectionNeed
  ): number {
    let score = 0.4;

    // Speaking engagements
    if (profile.speaksAt && profile.speaksAt.length > 0) {
      score += Math.min(0.20, profile.speaksAt.length * 0.04);
    }

    // Published work
    if (profile.publishedWork && profile.publishedWork.length > 0) {
      score += Math.min(0.20, profile.publishedWork.length * 0.05);
    }

    // Investor status
    if (profile.investorIn && profile.investorIn.length > 0) {
      score += 0.20;
    }

    // Network influence already factored in network strength
    // but double-weight for high influence individuals
    if (profile.networkInfluence === 'expert') {
      score += 0.15;
    } else if (profile.networkInfluence === 'high') {
      score += 0.10;
    }

    return Math.min(1.0, score);
  }

  /**
   * Calculate purpose alignment
   */
  private calculatePurposeAlignment(
    profile: IndustryConnectionProfile,
    need: IndustryConnectionNeed
  ): number {
    const purposeMatches: Record<string, string[]> = {
      'fundraising': ['investor', 'vc', 'angel', 'board', 'advisor'],
      'partnership': ['business development', 'partner', 'alliance', 'executive'],
      'sales': ['sales', 'business development', 'account', 'customer'],
      'hiring': ['recruiter', 'hr', 'talent', 'hiring'],
      'market_entry': ['executive', 'strategy', 'business development', 'advisor'],
      'advisory': ['advisor', 'consultant', 'board', 'mentor'],
    };

    const relevantKeywords = purposeMatches[need.purpose] || [];
    const positions = profile.positions.map(p => p.toLowerCase()).join(' ');

    let matches = 0;
    for (const keyword of relevantKeywords) {
      if (positions.includes(keyword)) {
        matches++;
      }
    }

    // Special boost for investors if purpose is fundraising
    if (need.purpose === 'fundraising' && profile.investorIn && profile.investorIn.length > 0) {
      return 1.0;
    }

    return matches > 0 ? Math.min(1.0, 0.5 + (matches * 0.2)) : 0.4;
  }

  /**
   * Identify potential connection paths
   */
  private identifyConnectionPaths(
    profile: IndustryConnectionProfile,
    need: IndustryConnectionNeed
  ): string[] {
    const paths: string[] = [];

    // Direct company connection
    if (need.targetCompanies) {
      for (const company of need.targetCompanies) {
        if (profile.companies.some(c => c.toLowerCase() === company.toLowerCase())) {
          paths.push(`Direct: Former/current employee at ${company}`);
        }
      }
    }

    // Board/advisory connections
    if (profile.boardPositions && profile.boardPositions.length > 0) {
      paths.push(`Board: Board member at ${profile.boardPositions.length} companies in related sectors`);
    }

    // Investor connections
    if (profile.investorIn && profile.investorIn.length > 0) {
      paths.push(`Investor: Active investor in ${need.targetIndustry} sector`);
    }

    // Industry groups
    if (profile.professionalGroups && profile.professionalGroups.length > 0) {
      paths.push(`Professional Networks: Member of ${profile.professionalGroups.length} industry associations`);
    }

    // Speaking/thought leadership
    if (profile.speaksAt && profile.speaksAt.length > 0) {
      paths.push(`Thought Leader: Speaker at industry events`);
    }

    // Geographic connections
    if (need.geographicPreference && profile.geographicReach) {
      const matches = need.geographicPreference.filter(geo =>
        profile.geographicReach!.some(reach =>
          reach.toLowerCase().includes(geo.toLowerCase())
        )
      );
      if (matches.length > 0) {
        paths.push(`Geographic: Strong network in ${matches.join(', ')}`);
      }
    }

    if (paths.length === 0) {
      paths.push(`Indirect: Industry experience may provide relevant connections`);
    }

    return paths;
  }

  /**
   * Estimate introduction quality
   */
  private estimateIntroductionQuality(
    score: number,
    profile: IndustryConnectionProfile,
    need: IndustryConnectionNeed
  ): 'cold' | 'warm' | 'hot' {
    // Direct company match = hot
    if (need.targetCompanies) {
      for (const company of need.targetCompanies) {
        if (profile.companies.some(c => c.toLowerCase() === company.toLowerCase())) {
          return 'hot';
        }
      }
    }

    // High score + strong network = warm to hot
    if (score >= 0.75 && profile.networkInfluence === 'high' || profile.networkInfluence === 'expert') {
      return 'hot';
    }

    if (score >= 0.6) {
      return 'warm';
    }

    if (score >= 0.4) {
      return 'warm';
    }

    return 'cold';
  }

  /**
   * Generate recommendation
   */
  private generateRecommendation(
    score: number,
    profile: IndustryConnectionProfile,
    need: IndustryConnectionNeed,
    paths: string[],
    introQuality: string
  ): string {
    if (score >= 0.75) {
      return `Excellent connector! ${introQuality === 'hot' ? 'Direct' : 'Strong'} connection to ${need.targetIndustry}. ` +
        `Connection paths: ${paths.slice(0, 2).join('; ')}. Highly recommended for ${introQuality} introduction.`;
    } else if (score >= 0.6) {
      return `Good connector. ${paths[0]}. Can likely provide ${introQuality} introduction to ${need.targetIndustry}.`;
    } else if (score >= 0.45) {
      return `Moderate fit. May have indirect connections through ${paths[0]}. Consider as backup option.`;
    } else {
      return `Limited access to ${need.targetIndustry}. May not be able to provide strong introduction.`;
    }
  }

  /**
   * Extract industry connection profile
   */
  private extractIndustryProfile(contact: Contact): IndustryConnectionProfile {
    const metadata = contact.metadata || {};

    return {
      industries: metadata.industries || this.inferIndustries(contact),
      companies: metadata.companies || [contact.company || ''].filter(Boolean),
      positions: metadata.positions || [contact.title || ''].filter(Boolean),
      networkInfluence: metadata.networkInfluence || this.estimateNetworkInfluence(contact),
      yearsInIndustry: metadata.yearsInIndustry || this.estimateYearsInIndustry(contact),
      boardPositions: metadata.boardPositions,
      advisoryRoles: metadata.advisoryRoles,
      investorIn: metadata.investorIn,
      speaksAt: metadata.speaksAt,
      publishedWork: metadata.publishedWork,
      professionalGroups: metadata.professionalGroups,
      geographicReach: metadata.geographicReach || [contact.location || ''].filter(Boolean),
    };
  }

  /**
   * Infer industries from profile
   */
  private inferIndustries(contact: Contact): string[] {
    const industries: string[] = [];
    const bio = (contact.bio || '').toLowerCase();
    const title = (contact.title || '').toLowerCase();

    const industryKeywords = new Map([
      ['tech', ['software', 'saas', 'technology', 'ai', 'ml', 'cloud']],
      ['finance', ['fintech', 'banking', 'investment', 'venture capital', 'private equity']],
      ['healthcare', ['healthtech', 'medical', 'biotech', 'pharma', 'clinical']],
      ['ecommerce', ['retail', 'marketplace', 'consumer', 'dtc']],
      ['education', ['edtech', 'learning', 'training', 'university']],
    ]);

    for (const [industry, keywords] of industryKeywords) {
      if (keywords.some(keyword => bio.includes(keyword) || title.includes(keyword))) {
        industries.push(industry);
      }
    }

    return industries.length > 0 ? industries : ['general'];
  }

  /**
   * Estimate network influence
   */
  private estimateNetworkInfluence(contact: Contact): 'low' | 'medium' | 'high' | 'expert' {
    const title = (contact.title || '').toLowerCase();
    const bio = (contact.bio || '').toLowerCase();

    if (title.includes('ceo') || title.includes('founder') || title.includes('partner')) {
      return 'high';
    }

    if (title.includes('vp') || title.includes('director')) {
      return 'medium';
    }

    if (bio.includes('speaker') || bio.includes('author') || bio.includes('board')) {
      return 'high';
    }

    return 'medium';
  }

  /**
   * Estimate years in industry
   */
  private estimateYearsInIndustry(contact: Contact): number {
    const bio = (contact.bio || '').toLowerCase();

    if (bio.includes('20+ years') || bio.includes('20 years')) return 20;
    if (bio.includes('15+ years') || bio.includes('15 years')) return 15;
    if (bio.includes('10+ years') || bio.includes('10 years')) return 10;
    if (bio.includes('5+ years') || bio.includes('5 years')) return 5;

    return 5; // Default
  }

  /**
   * Initialize industry hierarchy
   */
  private initializeIndustryHierarchy(): Map<string, string[]> {
    return new Map([
      ['tech', ['software', 'saas', 'ai', 'cloud', 'cybersecurity', 'data']],
      ['fintech', ['finance', 'banking', 'payments', 'lending', 'insurance']],
      ['healthtech', ['healthcare', 'biotech', 'pharma', 'medical devices', 'diagnostics']],
      ['ecommerce', ['retail', 'marketplace', 'consumer goods', 'dtc', 'logistics']],
      ['edtech', ['education', 'training', 'e-learning', 'corporate learning']],
    ]);
  }

  /**
   * Initialize company to industry mapping (sample)
   */
  private initializeCompanyToIndustry(): Map<string, string> {
    return new Map([
      // Tech
      ['google', 'tech'],
      ['microsoft', 'tech'],
      ['amazon', 'tech'],
      ['meta', 'tech'],
      // Finance
      ['goldman sachs', 'finance'],
      ['jpmorgan', 'finance'],
      ['stripe', 'fintech'],
      // Add more as needed
    ]);
  }

  /**
   * Bulk match industry connections
   */
  bulkMatchIndustryConnections(
    candidates: Contact[],
    need: IndustryConnectionNeed,
    topN: number = 10
  ): Array<{
    contact: Contact;
    matchResult: ReturnType<typeof this.matchIndustryConnection>;
  }> {
    const results = candidates.map(candidate => ({
      contact: candidate,
      matchResult: this.matchIndustryConnection(candidate, need),
    }));

    results.sort((a, b) => b.matchResult.score - a.matchResult.score);

    return results.slice(0, topN);
  }
}
