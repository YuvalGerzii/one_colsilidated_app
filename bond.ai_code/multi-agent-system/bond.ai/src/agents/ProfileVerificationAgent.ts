/**
 * Profile Verification Agent
 * Verifies and scores contact profile authenticity, completeness, and quality
 * Helps identify high-quality, trustworthy contacts for matching
 */

import { Contact } from '../types';

export interface VerificationScore {
  overall: number; // 0-1
  completeness: number;
  authenticity: number;
  activityLevel: number;
  socialProof: number;
  detailedScores: {
    hasProfilePhoto: boolean;
    hasCompleteBio: boolean;
    hasWorkHistory: boolean;
    hasEducation: boolean;
    hasSkills: boolean;
    hasVerifiedEmail: boolean;
    hasVerifiedPhone: boolean;
    hasSocialLinks: boolean;
    hasRecommendations: boolean;
    hasRecentActivity: boolean;
  };
  risks: string[];
  strengths: string[];
  verificationLevel: 'unverified' | 'basic' | 'verified' | 'premium';
}

export class ProfileVerificationAgent {
  private suspiciousPatterns: RegExp[];
  private qualityIndicators: Map<string, number>;

  constructor() {
    this.suspiciousPatterns = this.initializeSuspiciousPatterns();
    this.qualityIndicators = this.initializeQualityIndicators();
  }

  /**
   * Verify a contact profile
   */
  verifyProfile(contact: Contact): VerificationScore {
    const completeness = this.calculateCompleteness(contact);
    const authenticity = this.calculateAuthenticity(contact);
    const activityLevel = this.calculateActivityLevel(contact);
    const socialProof = this.calculateSocialProof(contact);

    const overall = (
      completeness * 0.30 +
      authenticity * 0.35 +
      activityLevel * 0.20 +
      socialProof * 0.15
    );

    const detailedScores = this.getDetailedScores(contact);
    const { risks, strengths } = this.analyzeProfile(contact, {
      completeness,
      authenticity,
      activityLevel,
      socialProof,
    });

    const verificationLevel = this.determineVerificationLevel(overall, detailedScores);

    return {
      overall,
      completeness,
      authenticity,
      activityLevel,
      socialProof,
      detailedScores,
      risks,
      strengths,
      verificationLevel,
    };
  }

  /**
   * Calculate profile completeness
   */
  private calculateCompleteness(contact: Contact): number {
    let score = 0;
    let maxScore = 10;

    // Basic fields (40% of completeness)
    if (contact.name && contact.name.trim().length > 0) score += 1;
    if (contact.email && contact.email.trim().length > 0) score += 1;
    if (contact.bio && contact.bio.trim().length > 50) score += 1;
    if (contact.title && contact.title.trim().length > 0) score += 1;

    // Professional information (40% of completeness)
    if (contact.company && contact.company.trim().length > 0) score += 1;
    if (contact.skills && contact.skills.length >= 3) score += 1;
    if (contact.industry && contact.industry.trim().length > 0) score += 1;
    if (contact.location && contact.location.trim().length > 0) score += 1;

    // Additional information (20% of completeness)
    if (contact.metadata?.education) score += 0.5;
    if (contact.metadata?.workHistory && contact.metadata.workHistory.length > 0) score += 0.5;
    if (contact.metadata?.socialLinks && Object.keys(contact.metadata.socialLinks).length > 0) score += 0.5;
    if (contact.metadata?.certifications && contact.metadata.certifications.length > 0) score += 0.5;

    return score / maxScore;
  }

  /**
   * Calculate profile authenticity
   */
  private calculateAuthenticity(contact: Contact): number {
    let score = 0.5; // Start at neutral
    let flags = 0; // Suspicious flags

    // Check for suspicious patterns
    if (this.hasSuspiciousPatterns(contact)) {
      flags++;
      score -= 0.2;
    }

    // Check email validity
    if (contact.email && this.isValidEmail(contact.email)) {
      score += 0.1;
    } else if (contact.email) {
      flags++;
      score -= 0.1;
    }

    // Check name validity
    if (contact.name && this.isValidName(contact.name)) {
      score += 0.1;
    } else {
      flags++;
      score -= 0.15;
    }

    // Check bio quality
    if (contact.bio && contact.bio.length > 100) {
      score += 0.1;
      if (!this.hasGenericBio(contact.bio)) {
        score += 0.1;
      }
    }

    // Check for verification badges
    if (contact.metadata?.verified) {
      score += 0.2;
    }

    // Check for professional consistency
    if (this.isProfessionallyConsistent(contact)) {
      score += 0.15;
    }

    // Check activity timestamps
    if (contact.metadata?.lastActive) {
      const daysSinceActive = this.getDaysSince(contact.metadata.lastActive);
      if (daysSinceActive < 30) {
        score += 0.1;
      }
    }

    return Math.max(0, Math.min(1.0, score));
  }

  /**
   * Calculate activity level
   */
  private calculateActivityLevel(contact: Contact): number {
    let score = 0.3; // Base score

    // Recent activity
    if (contact.metadata?.lastActive) {
      const daysSinceActive = this.getDaysSince(contact.metadata.lastActive);
      if (daysSinceActive < 7) score += 0.3;
      else if (daysSinceActive < 30) score += 0.2;
      else if (daysSinceActive < 90) score += 0.1;
    }

    // Connection activity
    if (contact.metadata?.connectionsCount) {
      const connections = contact.metadata.connectionsCount;
      if (connections > 500) score += 0.2;
      else if (connections > 100) score += 0.15;
      else if (connections > 20) score += 0.1;
    }

    // Content activity
    if (contact.metadata?.postsCount) {
      const posts = contact.metadata.postsCount;
      if (posts > 50) score += 0.15;
      else if (posts > 10) score += 0.1;
      else if (posts > 0) score += 0.05;
    }

    // Response rate
    if (contact.metadata?.responseRate) {
      score += contact.metadata.responseRate * 0.15;
    }

    return Math.min(1.0, score);
  }

  /**
   * Calculate social proof
   */
  private calculateSocialProof(contact: Contact): number {
    let score = 0.2; // Base score

    // Recommendations/endorsements
    if (contact.metadata?.recommendationsCount) {
      const recs = contact.metadata.recommendationsCount;
      score += Math.min(0.25, recs * 0.05);
    }

    // Skill endorsements
    if (contact.metadata?.skillEndorsements) {
      const endorsements = Object.values(contact.metadata.skillEndorsements).reduce(
        (sum: number, val: any) => sum + (typeof val === 'number' ? val : 0),
        0
      );
      score += Math.min(0.20, endorsements * 0.01);
    }

    // Mutual connections
    if (contact.metadata?.mutualConnectionsCount) {
      const mutual = contact.metadata.mutualConnectionsCount;
      score += Math.min(0.20, mutual * 0.02);
    }

    // Professional memberships
    if (contact.metadata?.professionalGroups) {
      score += Math.min(0.15, contact.metadata.professionalGroups.length * 0.03);
    }

    // Published work / public presence
    if (contact.metadata?.publishedWork && contact.metadata.publishedWork.length > 0) {
      score += 0.10;
    }

    // Speaking engagements
    if (contact.metadata?.speaksAt && contact.metadata.speaksAt.length > 0) {
      score += 0.10;
    }

    return Math.min(1.0, score);
  }

  /**
   * Get detailed verification scores
   */
  private getDetailedScores(contact: Contact): VerificationScore['detailedScores'] {
    return {
      hasProfilePhoto: !!(contact.metadata?.profilePhoto || contact.metadata?.avatarUrl),
      hasCompleteBio: !!(contact.bio && contact.bio.length > 100),
      hasWorkHistory: !!(contact.metadata?.workHistory && contact.metadata.workHistory.length > 0),
      hasEducation: !!contact.metadata?.education,
      hasSkills: !!(contact.skills && contact.skills.length >= 3),
      hasVerifiedEmail: !!(contact.metadata?.emailVerified || contact.metadata?.verified),
      hasVerifiedPhone: !!contact.metadata?.phoneVerified,
      hasSocialLinks: !!(contact.metadata?.socialLinks && Object.keys(contact.metadata.socialLinks).length > 0),
      hasRecommendations: !!(contact.metadata?.recommendationsCount && contact.metadata.recommendationsCount > 0),
      hasRecentActivity: !!(contact.metadata?.lastActive && this.getDaysSince(contact.metadata.lastActive) < 30),
    };
  }

  /**
   * Analyze profile for risks and strengths
   */
  private analyzeProfile(
    contact: Contact,
    scores: any
  ): { risks: string[]; strengths: string[] } {
    const risks: string[] = [];
    const strengths: string[] = [];

    // Risks
    if (scores.authenticity < 0.5) {
      risks.push('Low authenticity score - profile may be incomplete or fake');
    }

    if (scores.completeness < 0.4) {
      risks.push('Incomplete profile - missing critical information');
    }

    if (scores.activityLevel < 0.3) {
      risks.push('Low activity level - user may be inactive');
    }

    if (!contact.email || !this.isValidEmail(contact.email)) {
      risks.push('Invalid or missing email address');
    }

    if (this.hasSuspiciousPatterns(contact)) {
      risks.push('Profile contains suspicious patterns');
    }

    if (scores.socialProof < 0.2) {
      risks.push('Limited social proof - no recommendations or connections');
    }

    // Strengths
    if (scores.completeness >= 0.8) {
      strengths.push('Comprehensive profile with detailed information');
    }

    if (scores.authenticity >= 0.8) {
      strengths.push('High authenticity - verified and credible profile');
    }

    if (scores.activityLevel >= 0.7) {
      strengths.push('Active user with recent engagement');
    }

    if (scores.socialProof >= 0.6) {
      strengths.push('Strong social proof with recommendations and connections');
    }

    if (contact.metadata?.verified) {
      strengths.push('Verified profile');
    }

    if (contact.metadata?.connectionsCount && contact.metadata.connectionsCount > 500) {
      strengths.push(`Extensive network (${contact.metadata.connectionsCount}+ connections)`);
    }

    return { risks, strengths };
  }

  /**
   * Determine verification level
   */
  private determineVerificationLevel(
    overall: number,
    detailed: VerificationScore['detailedScores']
  ): 'unverified' | 'basic' | 'verified' | 'premium' {
    const verifiedCount = Object.values(detailed).filter(Boolean).length;

    if (overall >= 0.80 && verifiedCount >= 8) {
      return 'premium';
    } else if (overall >= 0.65 && verifiedCount >= 6) {
      return 'verified';
    } else if (overall >= 0.45 && verifiedCount >= 4) {
      return 'basic';
    } else {
      return 'unverified';
    }
  }

  /**
   * Check for suspicious patterns
   */
  private hasSuspiciousPatterns(contact: Contact): boolean {
    const textToCheck = [
      contact.name || '',
      contact.bio || '',
      contact.title || '',
      contact.company || '',
    ].join(' ');

    return this.suspiciousPatterns.some(pattern => pattern.test(textToCheck));
  }

  /**
   * Validate email format
   */
  private isValidEmail(email: string): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  /**
   * Validate name
   */
  private isValidName(name: string): boolean {
    // Check for minimum length and no suspicious characters
    if (name.length < 2 || name.length > 100) return false;

    // Should have at least one letter
    if (!/[a-zA-Z]/.test(name)) return false;

    // Shouldn't be all numbers
    if (/^\d+$/.test(name)) return false;

    // Shouldn't have excessive special characters
    const specialCharCount = (name.match(/[^a-zA-Z0-9\s\-\.]/g) || []).length;
    if (specialCharCount > 3) return false;

    return true;
  }

  /**
   * Check if bio is generic/template
   */
  private hasGenericBio(bio: string): boolean {
    const genericPhrases = [
      'passionate about',
      'results-oriented professional',
      'proven track record',
      'team player',
      'looking for opportunities',
    ];

    const lowerBio = bio.toLowerCase();
    const matchCount = genericPhrases.filter(phrase => lowerBio.includes(phrase)).length;

    return matchCount >= 3; // Too many generic phrases
  }

  /**
   * Check professional consistency
   */
  private isProfessionallyConsistent(contact: Contact): boolean {
    // Check if title matches industry
    // Check if skills match title
    // This is a simplified check

    if (!contact.title || !contact.industry) return false;

    const title = contact.title.toLowerCase();
    const industry = contact.industry.toLowerCase();

    // Simple consistency checks
    if (title.includes('engineer') && !industry.includes('tech') && !industry.includes('engineering')) {
      return false;
    }

    if (title.includes('doctor') && !industry.includes('health') && !industry.includes('medical')) {
      return false;
    }

    return true;
  }

  /**
   * Get days since a date
   */
  private getDaysSince(dateString: string): number {
    const date = new Date(dateString);
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    return Math.floor(diff / (1000 * 60 * 60 * 24));
  }

  /**
   * Initialize suspicious patterns
   */
  private initializeSuspiciousPatterns(): RegExp[] {
    return [
      /\b(click here|buy now|limited time|act now)\b/i,
      /\b(crypto|bitcoin|trading|investment opportunity)\b/i,
      /[^\x00-\x7F]{20,}/, // Excessive non-ASCII characters
      /(.)\1{5,}/, // Character repeated 5+ times
      /https?:\/\/[^\s]+/gi, // Multiple URLs (more than 3 is suspicious)
    ];
  }

  /**
   * Initialize quality indicators
   */
  private initializeQualityIndicators(): Map<string, number> {
    return new Map([
      ['verified_email', 0.15],
      ['verified_phone', 0.10],
      ['complete_profile', 0.20],
      ['recommendations', 0.15],
      ['recent_activity', 0.15],
      ['social_proof', 0.10],
      ['professional_network', 0.15],
    ]);
  }

  /**
   * Batch verify profiles
   */
  batchVerifyProfiles(contacts: Contact[]): Map<string, VerificationScore> {
    const results = new Map<string, VerificationScore>();

    for (const contact of contacts) {
      results.set(contact.id, this.verifyProfile(contact));
    }

    return results;
  }

  /**
   * Filter contacts by verification level
   */
  filterByVerificationLevel(
    contacts: Contact[],
    minLevel: 'basic' | 'verified' | 'premium'
  ): Contact[] {
    const levelOrder = ['unverified', 'basic', 'verified', 'premium'];
    const minLevelIndex = levelOrder.indexOf(minLevel);

    return contacts.filter(contact => {
      const score = this.verifyProfile(contact);
      const contactLevelIndex = levelOrder.indexOf(score.verificationLevel);
      return contactLevelIndex >= minLevelIndex;
    });
  }
}
