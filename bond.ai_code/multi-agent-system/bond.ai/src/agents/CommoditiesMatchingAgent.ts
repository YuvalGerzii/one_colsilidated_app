/**
 * Commodities Matching Agent
 * Specializes in matching suppliers with buyers for commodities, resources, and materials
 * Handles both physical commodities (raw materials) and digital commodities (data, licenses, etc.)
 */

import { Contact, Match } from '../types';

export interface CommodityProfile {
  commodityTypes: string[]; // e.g., 'metals', 'agricultural', 'energy', 'data', 'software licenses'
  role: 'supplier' | 'buyer' | 'broker' | 'both';
  specificCommodities: string[]; // e.g., 'copper', 'wheat', 'crude oil'
  volumeCapacity?: 'small' | 'medium' | 'large' | 'enterprise'; // Volume they can handle
  geographicCoverage: string[]; // Regions they operate in
  certifications?: string[]; // Quality certifications, compliance
  paymentTerms?: string[]; // Cash, credit, escrow, etc.
  minimumOrderValue?: number;
  maximumOrderValue?: number;
  deliveryCapabilities?: string[]; // FOB, CIF, DDP, etc.
  experienceYears: number;
  reliability?: 'unverified' | 'verified' | 'highly_reliable' | 'industry_leader';
  specializations?: string[]; // Organic, fair-trade, sustainable, etc.
}

export interface CommodityNeed {
  commodityType: string;
  specificCommodity: string;
  role: 'buying' | 'selling'; // What the seeker is doing
  volume: 'small' | 'medium' | 'large' | 'enterprise';
  budget?: number;
  targetRegions: string[];
  qualityRequirements?: string[]; // Certifications, standards
  urgency: 'low' | 'medium' | 'high' | 'immediate';
  paymentPreference?: string[];
  deliveryPreference?: string[];
  sustainabilityRequired?: boolean;
  longTermContract?: boolean; // One-time vs ongoing relationship
}

export class CommoditiesMatchingAgent {
  private commodityCategories: Map<string, string[]>;
  private commoditySynonyms: Map<string, string[]>;
  private regionalMarkets: Map<string, string[]>;

  constructor() {
    this.commodityCategories = this.initializeCommodityCategories();
    this.commoditySynonyms = this.initializeCommoditySynonyms();
    this.regionalMarkets = this.initializeRegionalMarkets();
  }

  /**
   * Match a commodity supplier/buyer with a need
   */
  matchCommodity(
    provider: Contact,
    need: CommodityNeed
  ): {
    score: number;
    breakdown: {
      commodityMatch: number;
      volumeCapability: number;
      geographicFit: number;
      qualityAlignment: number;
      commercialFit: number;
    };
    strengths: string[];
    concerns: string[];
    estimatedMatchType: 'perfect' | 'strong' | 'moderate' | 'weak';
    recommendation: string;
  } {
    const profile = this.extractCommodityProfile(provider);

    // Validate role compatibility
    if (!this.isRoleCompatible(profile.role, need.role)) {
      return this.generateIncompatibleResult(profile.role, need.role);
    }

    // Calculate dimensions
    const commodityMatch = this.calculateCommodityMatch(profile, need);
    const volumeCapability = this.calculateVolumeCapability(profile, need);
    const geographicFit = this.calculateGeographicFit(profile, need);
    const qualityAlignment = this.calculateQualityAlignment(profile, need);
    const commercialFit = this.calculateCommercialFit(profile, need);

    // Weighted score
    const score = (
      commodityMatch * 0.35 +
      volumeCapability * 0.25 +
      geographicFit * 0.20 +
      qualityAlignment * 0.10 +
      commercialFit * 0.10
    );

    // Analyze match
    const { strengths, concerns } = this.analyzeCommodityMatch(
      profile,
      need,
      { commodityMatch, volumeCapability, geographicFit, qualityAlignment, commercialFit }
    );

    const estimatedMatchType = this.estimateMatchType(score);
    const recommendation = this.generateRecommendation(score, strengths, concerns, profile, need);

    return {
      score,
      breakdown: {
        commodityMatch,
        volumeCapability,
        geographicFit,
        qualityAlignment,
        commercialFit,
      },
      strengths,
      concerns,
      estimatedMatchType,
      recommendation,
    };
  }

  /**
   * Check if roles are compatible
   */
  private isRoleCompatible(profileRole: string, needRole: string): boolean {
    if (profileRole === 'broker' || profileRole === 'both') {
      return true; // Brokers and both can match any need
    }

    // Buyer needs supplier, seller needs buyer
    if (needRole === 'buying' && (profileRole === 'supplier' || profileRole === 'both')) {
      return true;
    }

    if (needRole === 'selling' && (profileRole === 'buyer' || profileRole === 'both')) {
      return true;
    }

    return false;
  }

  /**
   * Generate result for incompatible roles
   */
  private generateIncompatibleResult(profileRole: string, needRole: string): any {
    return {
      score: 0,
      breakdown: {
        commodityMatch: 0,
        volumeCapability: 0,
        geographicFit: 0,
        qualityAlignment: 0,
        commercialFit: 0,
      },
      strengths: [],
      concerns: [`Role mismatch: ${profileRole} cannot fulfill ${needRole} need`],
      estimatedMatchType: 'weak' as const,
      recommendation: `This contact is a ${profileRole}, but you're looking for a ${needRole === 'buying' ? 'supplier' : 'buyer'}.`,
    };
  }

  /**
   * Calculate commodity match score
   */
  private calculateCommodityMatch(
    profile: CommodityProfile,
    need: CommodityNeed
  ): number {
    const needCommodity = need.specificCommodity.toLowerCase();
    const needType = need.commodityType.toLowerCase();

    // Check specific commodity match
    const profileCommodities = profile.specificCommodities.map(c => c.toLowerCase());

    // Direct match
    if (profileCommodities.includes(needCommodity)) {
      return 1.0;
    }

    // Synonym match
    if (this.hasCommoditySynonym(profileCommodities, needCommodity)) {
      return 0.95;
    }

    // Category match
    const profileTypes = profile.commodityTypes.map(t => t.toLowerCase());
    if (profileTypes.includes(needType)) {
      return 0.7; // Same category but different specific commodity
    }

    // Related category
    const relatedScore = this.getRelatedCommodityScore(profileTypes, needType);
    return relatedScore;
  }

  /**
   * Check for commodity synonyms
   */
  private hasCommoditySynonym(profileCommodities: string[], needed: string): boolean {
    const synonyms = this.commoditySynonyms.get(needed) || [];
    return profileCommodities.some(c => synonyms.includes(c));
  }

  /**
   * Get related commodity score
   */
  private getRelatedCommodityScore(profileTypes: string[], needType: string): number {
    const relatedCategories = new Map<string, string[]>([
      ['metals', ['minerals', 'ores', 'alloys']],
      ['energy', ['renewables', 'fossil fuels', 'power']],
      ['agricultural', ['food commodities', 'livestock', 'grains']],
      ['data', ['analytics', 'datasets', 'market data']],
    ]);

    const related = relatedCategories.get(needType) || [];

    for (const profileType of profileTypes) {
      if (related.includes(profileType)) {
        return 0.5;
      }
    }

    return 0.2;
  }

  /**
   * Calculate volume capability match
   */
  private calculateVolumeCapability(
    profile: CommodityProfile,
    need: CommodityNeed
  ): number {
    if (!profile.volumeCapacity) {
      return 0.5; // Unknown capacity
    }

    const volumeLevels = ['small', 'medium', 'large', 'enterprise'];
    const profileLevel = volumeLevels.indexOf(profile.volumeCapacity);
    const needLevel = volumeLevels.indexOf(need.volume);

    if (profileLevel === needLevel) {
      return 1.0; // Perfect match
    }

    if (profileLevel > needLevel) {
      // Provider can handle more than needed (good, but might be expensive)
      return 0.9 - ((profileLevel - needLevel) * 0.1);
    } else {
      // Provider might not be able to handle volume (bad)
      return Math.max(0.3, 0.8 - ((needLevel - profileLevel) * 0.2));
    }
  }

  /**
   * Calculate geographic fit
   */
  private calculateGeographicFit(
    profile: CommodityProfile,
    need: CommodityNeed
  ): number {
    const profileRegions = new Set(
      profile.geographicCoverage.map(r => r.toLowerCase())
    );

    const targetRegions = need.targetRegions.map(r => r.toLowerCase());

    // Direct region matches
    let matches = 0;
    for (const region of targetRegions) {
      if (profileRegions.has(region)) {
        matches++;
      }
    }

    if (matches > 0) {
      return Math.min(1.0, 0.7 + (matches / targetRegions.length) * 0.3);
    }

    // Check for regional market overlap
    const regionalOverlap = this.checkRegionalMarketOverlap(
      Array.from(profileRegions),
      targetRegions
    );

    return regionalOverlap;
  }

  /**
   * Check for regional market overlap
   */
  private checkRegionalMarketOverlap(profileRegions: string[], targetRegions: string[]): number {
    for (const target of targetRegions) {
      const marketRegions = this.regionalMarkets.get(target) || [];

      for (const profile of profileRegions) {
        if (marketRegions.includes(profile)) {
          return 0.6; // Nearby regions
        }
      }
    }

    // Check global coverage
    if (profileRegions.includes('global') || profileRegions.includes('worldwide')) {
      return 0.8;
    }

    return 0.3; // Limited geographic fit
  }

  /**
   * Calculate quality alignment
   */
  private calculateQualityAlignment(
    profile: CommodityProfile,
    need: CommodityNeed
  ): number {
    if (!need.qualityRequirements || need.qualityRequirements.length === 0) {
      return 0.7; // No specific requirements
    }

    const profileCerts = new Set(
      (profile.certifications || []).map(c => c.toLowerCase())
    );

    const profileSpecs = new Set(
      (profile.specializations || []).map(s => s.toLowerCase())
    );

    let matches = 0;
    for (const requirement of need.qualityRequirements) {
      const reqLower = requirement.toLowerCase();
      if (profileCerts.has(reqLower) || profileSpecs.has(reqLower)) {
        matches++;
      }
    }

    const matchScore = matches / need.qualityRequirements.length;

    // Sustainability bonus
    if (need.sustainabilityRequired) {
      const hasSustainability = profileSpecs.has('sustainable') ||
        profileSpecs.has('organic') ||
        profileSpecs.has('fair-trade') ||
        profileSpecs.has('green');

      if (hasSustainability) {
        return Math.min(1.0, matchScore + 0.2);
      } else {
        return matchScore * 0.7; // Penalty for missing sustainability
      }
    }

    return matchScore;
  }

  /**
   * Calculate commercial fit
   */
  private calculateCommercialFit(
    profile: CommodityProfile,
    need: CommodityNeed
  ): number {
    let score = 0.5; // Base score

    // Payment terms alignment
    if (need.paymentPreference && profile.paymentTerms) {
      const hasPaymentMatch = need.paymentPreference.some(pref =>
        profile.paymentTerms!.some(term =>
          term.toLowerCase().includes(pref.toLowerCase())
        )
      );
      if (hasPaymentMatch) {
        score += 0.2;
      }
    }

    // Delivery capabilities
    if (need.deliveryPreference && profile.deliveryCapabilities) {
      const hasDeliveryMatch = need.deliveryPreference.some(pref =>
        profile.deliveryCapabilities!.some(cap =>
          cap.toLowerCase().includes(pref.toLowerCase())
        )
      );
      if (hasDeliveryMatch) {
        score += 0.2;
      }
    }

    // Budget alignment (if specified)
    if (need.budget && profile.minimumOrderValue) {
      if (need.budget >= profile.minimumOrderValue) {
        score += 0.15;
      } else {
        score -= 0.2; // Below minimum
      }
    }

    // Reliability score
    const reliabilityBonus = {
      'industry_leader': 0.15,
      'highly_reliable': 0.10,
      'verified': 0.05,
      'unverified': 0,
    };
    score += reliabilityBonus[profile.reliability || 'unverified'];

    return Math.max(0, Math.min(1.0, score));
  }

  /**
   * Analyze commodity match
   */
  private analyzeCommodityMatch(
    profile: CommodityProfile,
    need: CommodityNeed,
    scores: any
  ): { strengths: string[]; concerns: string[] } {
    const strengths: string[] = [];
    const concerns: string[] = [];

    if (scores.commodityMatch === 1.0) {
      strengths.push(`Perfect commodity match for ${need.specificCommodity}`);
    } else if (scores.commodityMatch >= 0.7) {
      strengths.push(`Experience in ${need.commodityType} commodities`);
    } else {
      concerns.push(`Limited experience with ${need.specificCommodity}`);
    }

    if (scores.geographicFit >= 0.7) {
      strengths.push(`Strong geographic coverage in target regions`);
    } else if (scores.geographicFit < 0.5) {
      concerns.push(`Limited coverage in ${need.targetRegions.join(', ')}`);
    }

    if (scores.volumeCapability >= 0.9) {
      strengths.push(`Can handle required ${need.volume} volume`);
    } else if (scores.volumeCapability < 0.6) {
      concerns.push(`May not have capacity for ${need.volume} volume orders`);
    }

    if (profile.reliability === 'industry_leader' || profile.reliability === 'highly_reliable') {
      strengths.push(`${profile.reliability.replace('_', ' ')} reputation`);
    } else if (profile.reliability === 'unverified') {
      concerns.push(`Reliability not yet verified`);
    }

    if (need.sustainabilityRequired && scores.qualityAlignment < 0.7) {
      concerns.push(`Sustainability requirements may not be met`);
    }

    if (profile.experienceYears >= 5) {
      strengths.push(`${profile.experienceYears}+ years of commodity experience`);
    }

    return { strengths, concerns };
  }

  /**
   * Estimate match type
   */
  private estimateMatchType(score: number): 'perfect' | 'strong' | 'moderate' | 'weak' {
    if (score >= 0.85) return 'perfect';
    if (score >= 0.70) return 'strong';
    if (score >= 0.50) return 'moderate';
    return 'weak';
  }

  /**
   * Generate recommendation
   */
  private generateRecommendation(
    score: number,
    strengths: string[],
    concerns: string[],
    profile: CommodityProfile,
    need: CommodityNeed
  ): string {
    if (score >= 0.85) {
      return `Excellent match! ${strengths.join('. ')}. Strongly recommended for ${need.role === 'buying' ? 'procurement' : 'sales'} discussion.`;
    } else if (score >= 0.70) {
      return `Strong candidate. ${strengths.join('. ')}. ${concerns.length > 0 ? 'Minor concerns: ' + concerns.join(', ') : ''}`;
    } else if (score >= 0.50) {
      return `Moderate fit. ${concerns.join('. ')}. May work for smaller trial orders or with accommodations.`;
    } else {
      return `Not recommended. Significant gaps: ${concerns.join(', ')}`;
    }
  }

  /**
   * Extract commodity profile
   */
  private extractCommodityProfile(contact: Contact): CommodityProfile {
    const metadata = contact.metadata || {};
    const skills = contact.skills || [];

    return {
      commodityTypes: metadata.commodityTypes || this.inferCommodityTypes(contact),
      role: metadata.commodityRole || this.inferRole(contact),
      specificCommodities: metadata.specificCommodities || skills,
      volumeCapacity: metadata.volumeCapacity,
      geographicCoverage: metadata.geographicCoverage || [contact.location || 'Unknown'],
      certifications: metadata.certifications,
      paymentTerms: metadata.paymentTerms,
      minimumOrderValue: metadata.minimumOrderValue,
      maximumOrderValue: metadata.maximumOrderValue,
      deliveryCapabilities: metadata.deliveryCapabilities,
      experienceYears: metadata.experienceYears || this.estimateExperience(contact),
      reliability: metadata.reliability || 'unverified',
      specializations: metadata.specializations,
    };
  }

  /**
   * Infer commodity types from profile
   */
  private inferCommodityTypes(contact: Contact): string[] {
    const bio = (contact.bio || '').toLowerCase();
    const title = (contact.title || '').toLowerCase();
    const combined = bio + ' ' + title;

    const types: string[] = [];

    if (combined.match(/metal|copper|iron|steel|aluminum/)) types.push('metals');
    if (combined.match(/oil|gas|energy|coal|power/)) types.push('energy');
    if (combined.match(/wheat|corn|grain|agricultural|livestock/)) types.push('agricultural');
    if (combined.match(/data|analytics|dataset/)) types.push('data');
    if (combined.match(/software|license|saas/)) types.push('digital commodities');

    return types.length > 0 ? types : ['general'];
  }

  /**
   * Infer role from profile
   */
  private inferRole(contact: Contact): 'supplier' | 'buyer' | 'broker' | 'both' {
    const title = (contact.title || '').toLowerCase();
    const bio = (contact.bio || '').toLowerCase();

    if (title.includes('broker') || bio.includes('broker')) return 'broker';
    if (title.includes('procurement') || title.includes('buyer')) return 'buyer';
    if (title.includes('supplier') || title.includes('vendor') || title.includes('manufacturer')) return 'supplier';
    if (title.includes('trader') || title.includes('merchant')) return 'both';

    return 'supplier'; // Default
  }

  /**
   * Estimate experience
   */
  private estimateExperience(contact: Contact): number {
    const bio = (contact.bio || '').toLowerCase();

    if (bio.includes('20+ years') || bio.includes('20 years')) return 20;
    if (bio.includes('15+ years') || bio.includes('15 years')) return 15;
    if (bio.includes('10+ years') || bio.includes('10 years')) return 10;
    if (bio.includes('5+ years') || bio.includes('5 years')) return 5;

    return 3;
  }

  /**
   * Initialize commodity categories
   */
  private initializeCommodityCategories(): Map<string, string[]> {
    return new Map([
      ['metals', ['copper', 'iron', 'steel', 'aluminum', 'zinc', 'nickel', 'gold', 'silver']],
      ['energy', ['crude oil', 'natural gas', 'coal', 'electricity', 'renewable energy']],
      ['agricultural', ['wheat', 'corn', 'soybeans', 'rice', 'coffee', 'sugar', 'cotton']],
      ['livestock', ['cattle', 'hogs', 'poultry']],
      ['data', ['market data', 'consumer data', 'analytics', 'datasets', 'apis']],
      ['digital', ['software licenses', 'cloud credits', 'saas subscriptions']],
    ]);
  }

  /**
   * Initialize commodity synonyms
   */
  private initializeCommoditySynonyms(): Map<string, string[]> {
    return new Map([
      ['crude oil', ['oil', 'petroleum', 'brent crude', 'wti']],
      ['natural gas', ['gas', 'lng', 'lpg']],
      ['wheat', ['soft wheat', 'hard wheat']],
      ['corn', ['maize']],
      ['gold', ['au', 'bullion']],
      ['silver', ['ag']],
    ]);
  }

  /**
   * Initialize regional markets
   */
  private initializeRegionalMarkets(): Map<string, string[]> {
    return new Map([
      ['north america', ['usa', 'canada', 'mexico']],
      ['europe', ['eu', 'uk', 'germany', 'france', 'spain', 'italy']],
      ['asia', ['china', 'india', 'japan', 'singapore', 'south korea']],
      ['middle east', ['uae', 'saudi arabia', 'qatar', 'israel']],
      ['south america', ['brazil', 'argentina', 'chile', 'colombia']],
    ]);
  }

  /**
   * Bulk match commodities
   */
  bulkMatchCommodities(
    candidates: Contact[],
    need: CommodityNeed,
    topN: number = 10
  ): Array<{
    contact: Contact;
    matchResult: ReturnType<typeof this.matchCommodity>;
  }> {
    const results = candidates.map(candidate => ({
      contact: candidate,
      matchResult: this.matchCommodity(candidate, need),
    }));

    results.sort((a, b) => b.matchResult.score - a.matchResult.score);

    return results.slice(0, topN);
  }
}
