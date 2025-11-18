/**
 * Marketing Manager Matching Agent
 * Specializes in matching marketing talent with growth and brand needs
 * Focuses on channels, campaigns, metrics, and strategic thinking
 */

import { Contact, Match } from '../types';

export interface MarketingProfile {
  channels: string[]; // SEO, SEM, Social, Content, Email, etc.
  campaignExperience: string[]; // Launch, Growth, Brand Awareness, etc.
  industryExperience: string[];
  experienceYears: number;
  seniority: 'coordinator' | 'specialist' | 'manager' | 'senior_manager' | 'director' | 'vp';
  budgetManaged?: 'small' | 'medium' | 'large' | 'enterprise'; // <100K, 100K-500K, 500K-2M, >2M
  teamSize?: number;
  metricsExpertise: string[]; // CAC, LTV, ROAS, etc.
  tools: string[]; // Google Analytics, HubSpot, Salesforce, etc.
  specializations: string[]; // B2B, B2C, SaaS, eCommerce, etc.
  growthAchievements?: string[];
}

export interface MarketingRequirement {
  primaryObjective: 'brand_awareness' | 'lead_generation' | 'customer_acquisition' | 'retention' | 'product_launch';
  requiredChannels: string[];
  preferredChannels: string[];
  industry: string;
  companyStage: 'pre-launch' | 'startup' | 'growth' | 'scale' | 'enterprise';
  budget: 'small' | 'medium' | 'large' | 'enterprise';
  teamLeadership: boolean; // Will they manage a team?
  minExperienceYears: number;
  preferredSeniority: string[];
  analyticsRequired: boolean;
  contentCreation: boolean; // Hands-on content vs strategic only
  paidMediaExperience: boolean;
  B2BorB2C: 'b2b' | 'b2c' | 'both';
}

export class MarketingManagerMatchingAgent {
  private channelCategories: Map<string, string[]>;
  private metricsByObjective: Map<string, string[]>;

  constructor() {
    this.channelCategories = this.initializeChannelCategories();
    this.metricsByObjective = this.initializeMetricsByObjective();
  }

  /**
   * Match a marketer with a requirement
   */
  matchMarketer(
    marketer: Contact,
    requirement: MarketingRequirement
  ): {
    score: number;
    breakdown: {
      channelExpertise: number;
      industryFit: number;
      objectiveAlignment: number;
      experienceMatch: number;
      strategicCapability: number;
    };
    strengths: string[];
    gaps: string[];
    recommendation: string;
  } {
    const profile = this.extractMarketingProfile(marketer);

    // Calculate dimensions
    const channelExpertise = this.calculateChannelExpertise(profile, requirement);
    const industryFit = this.calculateIndustryFit(profile, requirement);
    const objectiveAlignment = this.calculateObjectiveAlignment(profile, requirement);
    const experienceMatch = this.calculateExperienceMatch(profile, requirement);
    const strategicCapability = this.calculateStrategicCapability(profile, requirement);

    // Weighted score
    const score = (
      channelExpertise * 0.30 +
      objectiveAlignment * 0.25 +
      experienceMatch * 0.20 +
      industryFit * 0.15 +
      strategicCapability * 0.10
    );

    const { strengths, gaps } = this.analyzeMarketer(
      profile,
      requirement,
      { channelExpertise, industryFit, objectiveAlignment, experienceMatch, strategicCapability }
    );

    const recommendation = this.generateRecommendation(score, strengths, gaps, requirement);

    return {
      score,
      breakdown: {
        channelExpertise,
        industryFit,
        objectiveAlignment,
        experienceMatch,
        strategicCapability,
      },
      strengths,
      gaps,
      recommendation,
    };
  }

  /**
   * Calculate channel expertise match
   */
  private calculateChannelExpertise(
    profile: MarketingProfile,
    requirement: MarketingRequirement
  ): number {
    const marketerChannels = new Set(
      profile.channels.map(c => c.toLowerCase())
    );

    // Required channels
    let requiredMatches = 0;
    for (const channel of requirement.requiredChannels) {
      if (this.hasChannelOrEquivalent(marketerChannels, channel)) {
        requiredMatches++;
      }
    }

    const requiredScore = requirement.requiredChannels.length > 0
      ? requiredMatches / requirement.requiredChannels.length
      : 1.0;

    // Preferred channels
    let preferredMatches = 0;
    for (const channel of requirement.preferredChannels) {
      if (this.hasChannelOrEquivalent(marketerChannels, channel)) {
        preferredMatches++;
      }
    }

    const preferredScore = requirement.preferredChannels.length > 0
      ? preferredMatches / requirement.preferredChannels.length
      : 0.5;

    return requiredScore * 0.80 + preferredScore * 0.20;
  }

  /**
   * Check if marketer has channel or equivalent
   */
  private hasChannelOrEquivalent(marketerChannels: Set<string>, required: string): boolean {
    const normalized = required.toLowerCase();

    if (marketerChannels.has(normalized)) {
      return true;
    }

    // Check for equivalent channels
    const category = this.getChannelCategory(normalized);
    if (category) {
      const equivalents = this.channelCategories.get(category) || [];
      return equivalents.some(ch => marketerChannels.has(ch.toLowerCase()));
    }

    return false;
  }

  /**
   * Get channel category
   */
  private getChannelCategory(channel: string): string | null {
    for (const [category, channels] of this.channelCategories.entries()) {
      if (channels.some(c => c.toLowerCase() === channel.toLowerCase())) {
        return category;
      }
    }
    return null;
  }

  /**
   * Calculate industry fit
   */
  private calculateIndustryFit(
    profile: MarketingProfile,
    requirement: MarketingRequirement
  ): number {
    const industries = profile.industryExperience.map(i => i.toLowerCase());
    const requiredIndustry = requirement.industry.toLowerCase();

    // Direct match
    if (industries.includes(requiredIndustry)) {
      return 1.0;
    }

    // Related industry match
    const relatedScore = this.getRelatedIndustryScore(industries, requiredIndustry);

    // B2B/B2C match
    const b2bMatch = this.calculateB2BMatch(profile, requirement);

    return relatedScore * 0.6 + b2bMatch * 0.4;
  }

  /**
   * Get related industry score
   */
  private getRelatedIndustryScore(marketerIndustries: string[], required: string): number {
    const relatedIndustries = new Map<string, string[]>([
      ['saas', ['software', 'tech', 'cloud', 'enterprise software']],
      ['ecommerce', ['retail', 'marketplace', 'consumer goods']],
      ['fintech', ['finance', 'banking', 'insurance', 'payments']],
      ['healthtech', ['healthcare', 'medical', 'biotech', 'pharma']],
      ['edtech', ['education', 'training', 'learning']],
    ]);

    const related = relatedIndustries.get(required) || [];

    for (const industry of marketerIndustries) {
      if (related.includes(industry)) {
        return 0.7; // Related industry experience
      }
    }

    return marketerIndustries.length > 0 ? 0.4 : 0.2;
  }

  /**
   * Calculate B2B/B2C match
   */
  private calculateB2BMatch(
    profile: MarketingProfile,
    requirement: MarketingRequirement
  ): number {
    const specializations = profile.specializations.map(s => s.toLowerCase());

    if (requirement.B2BorB2C === 'both') {
      return specializations.includes('b2b') || specializations.includes('b2c') ? 1.0 : 0.5;
    }

    if (specializations.includes(requirement.B2BorB2C.toLowerCase())) {
      return 1.0;
    }

    // Opposite type
    const opposite = requirement.B2BorB2C === 'b2b' ? 'b2c' : 'b2b';
    if (specializations.includes(opposite)) {
      return 0.5; // Some transferable skills
    }

    return 0.6; // Unknown, neutral
  }

  /**
   * Calculate objective alignment
   */
  private calculateObjectiveAlignment(
    profile: MarketingProfile,
    requirement: MarketingRequirement
  ): number {
    const campaigns = profile.campaignExperience.map(c => c.toLowerCase());
    const objective = requirement.primaryObjective.toLowerCase();

    // Direct campaign experience match
    if (campaigns.includes(objective)) {
      return 1.0;
    }

    // Check relevant metrics knowledge
    const relevantMetrics = this.metricsByObjective.get(objective) || [];
    const marketerMetrics = profile.metricsExpertise.map(m => m.toLowerCase());

    let metricMatches = 0;
    for (const metric of relevantMetrics) {
      if (marketerMetrics.includes(metric.toLowerCase())) {
        metricMatches++;
      }
    }

    const metricScore = relevantMetrics.length > 0
      ? metricMatches / relevantMetrics.length
      : 0.5;

    // Check if any campaign experience is relevant
    const hasRelevantExperience = this.hasRelevantCampaignExperience(
      campaigns,
      objective
    );

    if (hasRelevantExperience) {
      return 0.7 + (metricScore * 0.3);
    }

    return metricScore * 0.6;
  }

  /**
   * Check for relevant campaign experience
   */
  private hasRelevantCampaignExperience(campaigns: string[], objective: string): boolean {
    const relevantCampaigns = new Map<string, string[]>([
      ['lead_generation', ['demand generation', 'inbound', 'conversion']],
      ['customer_acquisition', ['growth', 'paid acquisition', 'performance marketing']],
      ['brand_awareness', ['brand', 'content marketing', 'social media']],
      ['retention', ['lifecycle marketing', 'email marketing', 'crm']],
      ['product_launch', ['go-to-market', 'launch', 'gtm']],
    ]);

    const relevant = relevantCampaigns.get(objective) || [];

    return campaigns.some(campaign =>
      relevant.some(rel => campaign.includes(rel))
    );
  }

  /**
   * Calculate experience match
   */
  private calculateExperienceMatch(
    profile: MarketingProfile,
    requirement: MarketingRequirement
  ): number {
    const yearsGap = profile.experienceYears - requirement.minExperienceYears;

    if (yearsGap < 0) {
      return Math.max(0, 1 + (yearsGap / requirement.minExperienceYears));
    } else if (yearsGap <= 3) {
      return 1.0;
    } else {
      return Math.max(0.75, 1 - ((yearsGap - 3) * 0.04));
    }
  }

  /**
   * Calculate strategic capability
   */
  private calculateStrategicCapability(
    profile: MarketingProfile,
    requirement: MarketingRequirement
  ): number {
    let score = 0.5;

    // Budget management
    if (requirement.budget === 'large' || requirement.budget === 'enterprise') {
      if (profile.budgetManaged === 'large' || profile.budgetManaged === 'enterprise') {
        score += 0.25;
      } else if (profile.budgetManaged === 'medium') {
        score += 0.10;
      }
    }

    // Team leadership
    if (requirement.teamLeadership) {
      if (profile.teamSize && profile.teamSize > 0) {
        score += 0.20;
      } else {
        score -= 0.15;
      }
    }

    // Analytics
    if (requirement.analyticsRequired) {
      if (profile.metricsExpertise.length >= 3) {
        score += 0.15;
      } else if (profile.metricsExpertise.length > 0) {
        score += 0.05;
      }
    }

    return Math.max(0, Math.min(1.0, score));
  }

  /**
   * Analyze marketer
   */
  private analyzeMarketer(
    profile: MarketingProfile,
    requirement: MarketingRequirement,
    scores: any
  ): { strengths: string[]; gaps: string[] } {
    const strengths: string[] = [];
    const gaps: string[] = [];

    if (scores.channelExpertise >= 0.8) {
      strengths.push(`Strong expertise in required marketing channels`);
    } else if (scores.channelExpertise < 0.6) {
      gaps.push(`Limited experience with required channels`);
    }

    if (scores.industryFit >= 0.8) {
      strengths.push(`Proven ${requirement.industry} industry experience`);
    } else if (scores.industryFit < 0.5) {
      gaps.push(`No direct ${requirement.industry} industry experience`);
    }

    if (scores.objectiveAlignment >= 0.8) {
      strengths.push(`Track record in ${requirement.primaryObjective.replace('_', ' ')}`);
    }

    if (requirement.teamLeadership && profile.teamSize && profile.teamSize > 3) {
      strengths.push(`Experienced team leader (managed ${profile.teamSize}+ people)`);
    }

    if (requirement.teamLeadership && (!profile.teamSize || profile.teamSize === 0)) {
      gaps.push(`No team management experience`);
    }

    if (requirement.analyticsRequired && profile.metricsExpertise.length < 2) {
      gaps.push(`Limited analytics and metrics expertise`);
    }

    if (profile.growthAchievements && profile.growthAchievements.length > 0) {
      strengths.push(`Documented growth achievements`);
    }

    return { strengths, gaps };
  }

  /**
   * Generate recommendation
   */
  private generateRecommendation(
    score: number,
    strengths: string[],
    gaps: string[],
    requirement: MarketingRequirement
  ): string {
    if (score >= 0.8) {
      return `Excellent marketing match! ${strengths.join('. ')}. Highly recommended for interview.`;
    } else if (score >= 0.65) {
      return `Strong candidate. ${strengths.join('. ')}. ${gaps.length > 0 ? 'Minor concerns: ' + gaps.join(', ') : ''}`;
    } else if (score >= 0.5) {
      return `Moderate fit. Has potential but gaps exist: ${gaps.join(', ')}`;
    } else {
      return `Not recommended for this role. Significant gaps: ${gaps.join(', ')}`;
    }
  }

  /**
   * Extract marketing profile
   */
  private extractMarketingProfile(contact: Contact): MarketingProfile {
    const skills = contact.skills || [];
    const metadata = contact.metadata || {};

    const channels: string[] = [];
    const campaigns: string[] = [];
    const industries: string[] = [];
    const metrics: string[] = [];
    const tools: string[] = [];
    const specializations: string[] = [];

    const knownChannels = new Set([
      'seo', 'sem', 'ppc', 'social media', 'content marketing', 'email marketing',
      'influencer marketing', 'affiliate marketing', 'display advertising'
    ]);

    const knownMetrics = new Set([
      'cac', 'ltv', 'roas', 'ctr', 'conversion rate', 'engagement rate',
      'roi', 'mrr', 'arr', 'churn rate'
    ]);

    const knownTools = new Set([
      'google analytics', 'hubspot', 'salesforce', 'marketo', 'mailchimp',
      'hootsuite', 'buffer', 'semrush', 'ahrefs', 'google ads'
    ]);

    for (const skill of skills) {
      const lowerSkill = skill.toLowerCase();
      if (knownChannels.has(lowerSkill)) {
        channels.push(skill);
      } else if (knownMetrics.has(lowerSkill)) {
        metrics.push(skill);
      } else if (knownTools.has(lowerSkill)) {
        tools.push(skill);
      } else {
        specializations.push(skill);
      }
    }

    return {
      channels,
      campaignExperience: metadata.campaignExperience || campaigns,
      industryExperience: metadata.industryExperience || industries,
      experienceYears: metadata.experienceYears || this.estimateExperience(contact),
      seniority: (metadata.seniority || this.estimateSeniority(contact)) as any,
      budgetManaged: metadata.budgetManaged,
      teamSize: metadata.teamSize,
      metricsExpertise: metrics,
      tools,
      specializations,
      growthAchievements: metadata.growthAchievements,
    };
  }

  /**
   * Estimate experience
   */
  private estimateExperience(contact: Contact): number {
    const bio = (contact.bio || '').toLowerCase();
    const title = (contact.title || '').toLowerCase();

    if (bio.includes('10+ years') || bio.includes('10 years')) return 10;
    if (bio.includes('5+ years') || bio.includes('5 years')) return 5;
    if (title.includes('senior') || title.includes('director')) return 7;
    if (title.includes('vp') || title.includes('head of')) return 10;
    if (title.includes('manager')) return 4;

    return 3;
  }

  /**
   * Estimate seniority
   */
  private estimateSeniority(contact: Contact): string {
    const title = (contact.title || '').toLowerCase();

    if (title.includes('vp') || title.includes('cmo')) return 'vp';
    if (title.includes('director') || title.includes('head of')) return 'director';
    if (title.includes('senior manager')) return 'senior_manager';
    if (title.includes('manager')) return 'manager';
    if (title.includes('specialist')) return 'specialist';

    return 'coordinator';
  }

  /**
   * Initialize channel categories
   */
  private initializeChannelCategories(): Map<string, string[]> {
    return new Map([
      ['paid_search', ['SEM', 'PPC', 'Google Ads', 'Bing Ads']],
      ['organic_search', ['SEO', 'Content Marketing', 'Technical SEO']],
      ['social', ['Social Media', 'Facebook Ads', 'LinkedIn Ads', 'Instagram', 'TikTok']],
      ['email', ['Email Marketing', 'Marketing Automation', 'Lifecycle Marketing']],
      ['content', ['Content Marketing', 'Blog', 'Video Marketing', 'Podcast']],
    ]);
  }

  /**
   * Initialize metrics by objective
   */
  private initializeMetricsByObjective(): Map<string, string[]> {
    return new Map([
      ['lead_generation', ['MQL', 'SQL', 'Conversion Rate', 'CPL', 'Lead Quality']],
      ['customer_acquisition', ['CAC', 'LTV', 'ROAS', 'Conversion Rate', 'Payback Period']],
      ['brand_awareness', ['Reach', 'Impressions', 'Engagement Rate', 'Brand Recall', 'Share of Voice']],
      ['retention', ['Churn Rate', 'Retention Rate', 'LTV', 'NPS', 'Customer Satisfaction']],
      ['product_launch', ['Adoption Rate', 'Market Penetration', 'Launch Velocity', 'PR Mentions']],
    ]);
  }

  /**
   * Bulk match marketers
   */
  bulkMatchMarketers(
    candidates: Contact[],
    requirement: MarketingRequirement,
    topN: number = 10
  ): Array<{
    contact: Contact;
    matchResult: ReturnType<typeof this.matchMarketer>;
  }> {
    const results = candidates.map(candidate => ({
      contact: candidate,
      matchResult: this.matchMarketer(candidate, requirement),
    }));

    results.sort((a, b) => b.matchResult.score - a.matchResult.score);

    return results.slice(0, topN);
  }
}
