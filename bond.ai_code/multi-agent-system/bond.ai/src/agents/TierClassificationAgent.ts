/**
 * Tier Classification Agent
 * Determines professional tier based on profile analysis
 */

import {
  Contact,
  ProfessionalTier,
  TierProfile,
  AgentType,
  AgentCapability
} from '../types';

export class TierClassificationAgent {
  private agentType = AgentType.ANALYZER;
  private capabilities = [AgentCapability.ANALYZE, AgentCapability.EVALUATE];

  /**
   * Classify a contact into appropriate professional tier
   */
  async classifyTier(contact: Contact): Promise<TierProfile> {
    const careerYears = this.estimateCareerYears(contact);
    const seniorityLevel = this.calculateSeniorityLevel(contact);
    const influenceMetrics = await this.analyzeInfluenceMetrics(contact);
    const achievementScore = this.calculateAchievementScore(contact);
    const industryAuthority = this.assessIndustryAuthority(contact);
    const organizationLevel = this.determineOrganizationLevel(contact);

    // Calculate composite tier score
    const tierScore = this.calculateTierScore({
      careerYears,
      seniorityLevel,
      influenceMetrics,
      achievementScore,
      industryAuthority,
      organizationLevel
    });

    // Determine tier based on multiple factors
    const tier = this.determineTier({
      careerYears,
      seniorityLevel,
      tierScore,
      title: contact.title,
      company: contact.company,
      influenceMetrics
    });

    // Verify tier based on available evidence
    const { verified, verificationSources } = await this.verifyTier(contact, tier);

    return {
      tier,
      tierScore,
      careerYears,
      seniorityLevel,
      influenceMetrics,
      achievementScore,
      industryAuthority,
      organizationLevel,
      verified,
      verificationSources
    };
  }

  /**
   * Estimate career years from profile information
   */
  private estimateCareerYears(contact: Contact): number {
    const title = contact.title?.toLowerCase() || '';
    const bio = contact.bio?.toLowerCase() || '';

    // Extract years from explicit mentions
    const yearsMatch = bio.match(/(\d+)\+?\s*years?\s*(of\s*)?(experience|in)/i);
    if (yearsMatch) {
      return parseInt(yearsMatch[1]);
    }

    // Infer from title keywords
    if (title.includes('intern') || title.includes('student')) return 0;
    if (title.includes('junior') || title.includes('associate')) return 2;
    if (title.includes('senior') && !title.includes('director') && !title.includes('vp')) return 10;
    if (title.includes('lead') || title.includes('principal')) return 8;
    if (title.includes('director')) return 12;
    if (title.includes('vp') || title.includes('vice president')) return 15;
    if (title.includes('cto') || title.includes('cfo') || title.includes('coo')) return 18;
    if (title.includes('ceo') || title.includes('founder')) return 20;

    // Default estimate based on title presence
    return contact.title ? 5 : 3;
  }

  /**
   * Calculate seniority level (1-10 scale)
   */
  private calculateSeniorityLevel(contact: Contact): number {
    const title = contact.title?.toLowerCase() || '';

    const seniorityKeywords = [
      { patterns: ['intern', 'trainee'], score: 1 },
      { patterns: ['junior', 'associate', 'analyst'], score: 2 },
      { patterns: ['developer', 'engineer', 'specialist'], score: 4 },
      { patterns: ['senior', 'staff'], score: 6 },
      { patterns: ['lead', 'principal', 'architect'], score: 7 },
      { patterns: ['manager', 'head of'], score: 8 },
      { patterns: ['director'], score: 9 },
      { patterns: ['vp', 'vice president', 'c-level', 'cto', 'cfo', 'coo'], score: 10 },
      { patterns: ['ceo', 'founder', 'president'], score: 10 }
    ];

    for (const { patterns, score } of seniorityKeywords) {
      if (patterns.some(pattern => title.includes(pattern))) {
        return score;
      }
    }

    return 5; // Default mid-level
  }

  /**
   * Analyze influence metrics from social profiles and bio
   */
  private async analyzeInfluenceMetrics(contact: Contact): Promise<TierProfile['influenceMetrics']> {
    const bio = contact.bio || '';
    const metrics = {
      networkSize: 0,
      followerCount: 0,
      publicationsCount: 0,
      speakingEngagements: 0,
      awardsRecognitions: 0,
      mediaPresence: 0
    };

    // Extract follower counts from bio
    const followerMatch = bio.match(/(\d+)[kK]?\+?\s*(followers?|connections?)/i);
    if (followerMatch) {
      const count = parseInt(followerMatch[1]);
      metrics.followerCount = followerMatch[0].includes('k') || followerMatch[0].includes('K')
        ? count * 1000
        : count;
    }

    // Look for publication indicators
    if (bio.match(/author|published|papers?|articles?|books?/i)) {
      metrics.publicationsCount = 5; // Placeholder
    }

    // Look for speaking indicators
    if (bio.match(/speaker|keynote|conference|ted|talks?/i)) {
      metrics.speakingEngagements = 3; // Placeholder
    }

    // Look for awards/recognition
    if (bio.match(/award|recognized|forbes|fortune|top \d+/i)) {
      metrics.awardsRecognitions = 1;
    }

    // Look for media presence
    if (bio.match(/featured|interviewed|quoted|press|media/i)) {
      metrics.mediaPresence = 1;
    }

    return metrics;
  }

  /**
   * Calculate achievement score based on verifiable accomplishments
   */
  private calculateAchievementScore(contact: Contact): number {
    let score = 0;
    const bio = contact.bio?.toLowerCase() || '';
    const company = contact.company?.toLowerCase() || '';

    // Company prestige
    const prestigiousCompanies = ['google', 'apple', 'microsoft', 'amazon', 'meta', 'facebook',
                                   'tesla', 'spacex', 'openai', 'anthropic', 'stripe'];
    if (prestigiousCompanies.some(c => company.includes(c))) {
      score += 20;
    }

    // Education indicators (MBA, PhD, etc.)
    if (bio.match(/mba|phd|doctorate|stanford|mit|harvard|oxford|cambridge/i)) {
      score += 15;
    }

    // Achievements mentioned
    if (bio.match(/founded|built|scaled|grew|\$\d+m|\$\d+b/i)) {
      score += 20;
    }

    // Patents, publications
    if (bio.match(/patent|published|research/i)) {
      score += 10;
    }

    // Awards
    if (bio.match(/award|winner|recipient|recognized/i)) {
      score += 15;
    }

    // Leadership experience
    if (bio.match(/led team|managed|director|head of/i)) {
      score += 10;
    }

    // Industry expertise
    if (contact.skills && contact.skills.length > 10) {
      score += 10;
    }

    return Math.min(score, 100);
  }

  /**
   * Assess industry authority
   */
  private assessIndustryAuthority(contact: Contact): number {
    let authority = 0;
    const bio = contact.bio?.toLowerCase() || '';
    const title = contact.title?.toLowerCase() || '';

    // Thought leader indicators
    if (bio.match(/thought leader|expert|authority|pioneer|innovator/i)) {
      authority += 30;
    }

    // Public presence
    if (bio.match(/speaker|author|blogger|influencer|creator/i)) {
      authority += 20;
    }

    // Executive titles
    if (title.match(/chief|vp|director|president|founder/i)) {
      authority += 25;
    }

    // Industry recognition
    if (bio.match(/award|recognized|top \d+|forbes|fortune/i)) {
      authority += 25;
    }

    return Math.min(authority, 100);
  }

  /**
   * Determine position in organizational hierarchy (1-10)
   */
  private determineOrganizationLevel(contact: Contact): number {
    const title = contact.title?.toLowerCase() || '';

    const levels = [
      { patterns: ['intern', 'trainee'], level: 1 },
      { patterns: ['junior', 'associate'], level: 2 },
      { patterns: ['analyst', 'specialist', 'coordinator'], level: 3 },
      { patterns: ['developer', 'engineer', 'consultant'], level: 4 },
      { patterns: ['senior'], level: 5 },
      { patterns: ['lead', 'staff', 'principal'], level: 6 },
      { patterns: ['manager'], level: 7 },
      { patterns: ['senior manager', 'head of'], level: 8 },
      { patterns: ['director'], level: 8 },
      { patterns: ['senior director', 'vp', 'vice president'], level: 9 },
      { patterns: ['svp', 'evp', 'cto', 'cfo', 'coo', 'cmo'], level: 10 },
      { patterns: ['ceo', 'president', 'founder'], level: 10 }
    ];

    for (let i = levels.length - 1; i >= 0; i--) {
      const { patterns, level } = levels[i];
      if (patterns.some(pattern => title.includes(pattern))) {
        return level;
      }
    }

    return 5; // Default mid-level
  }

  /**
   * Calculate composite tier score
   */
  private calculateTierScore(factors: {
    careerYears: number;
    seniorityLevel: number;
    influenceMetrics: TierProfile['influenceMetrics'];
    achievementScore: number;
    industryAuthority: number;
    organizationLevel: number;
  }): number {
    const weights = {
      careerYears: 0.15,
      seniorityLevel: 0.25,
      influence: 0.20,
      achievements: 0.20,
      authority: 0.10,
      organization: 0.10
    };

    // Normalize career years to 0-100 (20+ years = 100)
    const normalizedYears = Math.min((factors.careerYears / 20) * 100, 100);

    // Normalize seniority level (1-10 to 0-100)
    const normalizedSeniority = (factors.seniorityLevel / 10) * 100;

    // Normalize organization level (1-10 to 0-100)
    const normalizedOrg = (factors.organizationLevel / 10) * 100;

    // Calculate influence score
    const influenceScore = Math.min(
      (factors.influenceMetrics.followerCount / 10000) * 30 +
      factors.influenceMetrics.publicationsCount * 10 +
      factors.influenceMetrics.speakingEngagements * 10 +
      factors.influenceMetrics.awardsRecognitions * 20 +
      factors.influenceMetrics.mediaPresence * 10,
      100
    );

    const tierScore =
      normalizedYears * weights.careerYears +
      normalizedSeniority * weights.seniorityLevel +
      influenceScore * weights.influence +
      factors.achievementScore * weights.achievements +
      factors.industryAuthority * weights.authority +
      normalizedOrg * weights.organization;

    return Math.round(tierScore);
  }

  /**
   * Determine final tier classification
   */
  private determineTier(factors: {
    careerYears: number;
    seniorityLevel: number;
    tierScore: number;
    title?: string;
    company?: string;
    influenceMetrics: TierProfile['influenceMetrics'];
  }): ProfessionalTier {
    const { careerYears, seniorityLevel, tierScore, title } = factors;
    const titleLower = title?.toLowerCase() || '';

    // Luminary tier - industry leaders with exceptional influence
    if (tierScore >= 90 ||
        (factors.influenceMetrics.followerCount > 100000) ||
        titleLower.match(/chief executive|founder & ceo/) && factors.influenceMetrics.awardsRecognitions > 0) {
      return ProfessionalTier.LUMINARY;
    }

    // Founder/CEO tier
    if (titleLower.includes('founder') ||
        (titleLower.includes('ceo') && !titleLower.includes('assistant'))) {
      return ProfessionalTier.FOUNDER_CEO;
    }

    // C-Level tier
    if (titleLower.match(/\bcto\b|\bcfo\b|\bcoo\b|\bcmo\b|\bcpo\b|\bchief\b/) ||
        tierScore >= 80) {
      return ProfessionalTier.C_LEVEL;
    }

    // Executive tier
    if (titleLower.match(/\bvp\b|vice president|director/) ||
        (careerYears >= 15 && seniorityLevel >= 8) ||
        tierScore >= 70) {
      return ProfessionalTier.EXECUTIVE;
    }

    // Senior tier
    if (titleLower.includes('senior') ||
        titleLower.match(/\blead\b|\bprincipal\b|\bstaff\b/) ||
        (careerYears >= 10 && seniorityLevel >= 6) ||
        tierScore >= 60) {
      return ProfessionalTier.SENIOR;
    }

    // Mid-level tier
    if ((careerYears >= 5 && seniorityLevel >= 4) ||
        tierScore >= 45) {
      return ProfessionalTier.MID_LEVEL;
    }

    // Junior tier
    if (titleLower.match(/junior|associate|analyst/) ||
        (careerYears >= 2 && careerYears < 5) ||
        tierScore >= 30) {
      return ProfessionalTier.JUNIOR;
    }

    // Entry tier
    return ProfessionalTier.ENTRY;
  }

  /**
   * Verify tier classification based on available evidence
   */
  private async verifyTier(contact: Contact, tier: ProfessionalTier): Promise<{
    verified: boolean;
    verificationSources: string[];
  }> {
    const sources: string[] = [];
    let verified = false;

    // LinkedIn verification
    if (contact.socialProfiles?.linkedin) {
      sources.push('linkedin');
      verified = true; // Would actually verify via LinkedIn API
    }

    // Company website verification
    if (contact.company && contact.title) {
      sources.push('company_profile');
    }

    // Email domain verification (corporate email)
    if (contact.email && !contact.email.includes('gmail') && !contact.email.includes('yahoo')) {
      sources.push('corporate_email');
    }

    // GitHub verification for tech roles
    if (contact.socialProfiles?.github) {
      sources.push('github');
    }

    // Verification confidence
    verified = sources.length >= 2;

    return { verified, verificationSources: sources };
  }

  /**
   * Get tier gap between two tiers (numeric difference)
   */
  getTierGap(tier1: ProfessionalTier, tier2: ProfessionalTier): number {
    const tierOrder = [
      ProfessionalTier.ENTRY,
      ProfessionalTier.JUNIOR,
      ProfessionalTier.MID_LEVEL,
      ProfessionalTier.SENIOR,
      ProfessionalTier.EXECUTIVE,
      ProfessionalTier.C_LEVEL,
      ProfessionalTier.FOUNDER_CEO,
      ProfessionalTier.LUMINARY
    ];

    const index1 = tierOrder.indexOf(tier1);
    const index2 = tierOrder.indexOf(tier2);

    return Math.abs(index1 - index2);
  }

  /**
   * Check if tier gap is appropriate for direct contact
   */
  isAppropriateDirectContact(
    seekerTier: ProfessionalTier,
    targetTier: ProfessionalTier,
    maxGapWithoutValidation: number = 2
  ): boolean {
    const gap = this.getTierGap(seekerTier, targetTier);

    // Can always contact same tier or lower
    const tierOrder = [
      ProfessionalTier.ENTRY,
      ProfessionalTier.JUNIOR,
      ProfessionalTier.MID_LEVEL,
      ProfessionalTier.SENIOR,
      ProfessionalTier.EXECUTIVE,
      ProfessionalTier.C_LEVEL,
      ProfessionalTier.FOUNDER_CEO,
      ProfessionalTier.LUMINARY
    ];

    const seekerIndex = tierOrder.indexOf(seekerTier);
    const targetIndex = tierOrder.indexOf(targetTier);

    if (targetIndex <= seekerIndex) {
      return true; // Can always contact same or lower tier
    }

    // Check gap for upward contact
    return gap <= maxGapWithoutValidation;
  }
}
