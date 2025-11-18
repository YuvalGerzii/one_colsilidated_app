/**
 * Expert Developer Matching Agent
 * Specializes in matching technical talent with hiring needs
 * Focuses on skills, experience, tech stack, and cultural fit
 */

import { Contact, Match } from '../types';
import { ContextualMatchingAgent, MatchContext, ContextualGoal } from './ContextualMatchingAgent';

export interface DeveloperProfile {
  primaryLanguages: string[];
  frameworks: string[];
  experienceYears: number;
  seniority: 'junior' | 'mid' | 'senior' | 'lead' | 'principal' | 'architect';
  specializations: string[];
  previousCompanies?: string[];
  education?: string;
  certifications?: string[];
  githubActivity?: 'low' | 'medium' | 'high';
  remoteExperience?: boolean;
}

export interface DeveloperRequirement {
  mustHaveSkills: string[];
  niceToHaveSkills: string[];
  minExperienceYears: number;
  preferredSeniority: string[];
  techStack: string[];
  projectType: 'greenfield' | 'maintenance' | 'legacy_migration' | 'scaling';
  teamSize: 'solo' | 'small' | 'medium' | 'large';
  remote: boolean;
  timezone?: string;
}

export class ExpertDeveloperMatchingAgent {
  private contextAgent: ContextualMatchingAgent;
  private skillSynonyms: Map<string, string[]>;

  constructor() {
    this.contextAgent = new ContextualMatchingAgent();
    this.skillSynonyms = this.initializeSkillSynonyms();
  }

  /**
   * Match a developer with a hiring requirement
   */
  matchDeveloper(
    developer: Contact,
    requirement: DeveloperRequirement,
    baseMatch?: Match
  ): {
    score: number;
    breakdown: {
      skillsMatch: number;
      experienceMatch: number;
      techStackMatch: number;
      seniorityMatch: number;
      culturalFit: number;
    };
    strengths: string[];
    gaps: string[];
    recommendation: string;
  } {
    const developerProfile = this.extractDeveloperProfile(developer);

    // Calculate individual dimension scores
    const skillsMatch = this.calculateSkillsMatch(
      developerProfile,
      requirement
    );

    const experienceMatch = this.calculateExperienceMatch(
      developerProfile,
      requirement
    );

    const techStackMatch = this.calculateTechStackMatch(
      developerProfile,
      requirement
    );

    const seniorityMatch = this.calculateSeniorityMatch(
      developerProfile,
      requirement
    );

    const culturalFit = this.calculateCulturalFit(
      developer,
      requirement
    );

    // Weighted overall score
    const score = (
      skillsMatch * 0.35 +
      experienceMatch * 0.25 +
      techStackMatch * 0.20 +
      seniorityMatch * 0.15 +
      culturalFit * 0.05
    );

    // Generate strengths and gaps
    const { strengths, gaps } = this.analyzeStrengthsAndGaps(
      developerProfile,
      requirement,
      { skillsMatch, experienceMatch, techStackMatch, seniorityMatch, culturalFit }
    );

    // Generate recommendation
    const recommendation = this.generateRecommendation(
      score,
      strengths,
      gaps,
      requirement
    );

    return {
      score,
      breakdown: {
        skillsMatch,
        experienceMatch,
        techStackMatch,
        seniorityMatch,
        culturalFit,
      },
      strengths,
      gaps,
      recommendation,
    };
  }

  /**
   * Calculate skills match score
   */
  private calculateSkillsMatch(
    profile: DeveloperProfile,
    requirement: DeveloperRequirement
  ): number {
    const devSkills = new Set([
      ...profile.primaryLanguages,
      ...profile.frameworks,
      ...profile.specializations,
    ].map(s => s.toLowerCase()));

    // Check must-have skills
    let mustHaveMatches = 0;
    for (const skill of requirement.mustHaveSkills) {
      if (this.hasSkill(devSkills, skill)) {
        mustHaveMatches++;
      }
    }
    const mustHaveScore = requirement.mustHaveSkills.length > 0
      ? mustHaveMatches / requirement.mustHaveSkills.length
      : 1.0;

    // Check nice-to-have skills
    let niceToHaveMatches = 0;
    for (const skill of requirement.niceToHaveSkills) {
      if (this.hasSkill(devSkills, skill)) {
        niceToHaveMatches++;
      }
    }
    const niceToHaveScore = requirement.niceToHaveSkills.length > 0
      ? niceToHaveMatches / requirement.niceToHaveSkills.length
      : 0.5;

    // Weighted combination: must-have is 80%, nice-to-have is 20%
    return mustHaveScore * 0.8 + niceToHaveScore * 0.2;
  }

  /**
   * Check if developer has a skill (with synonym matching)
   */
  private hasSkill(devSkills: Set<string>, requiredSkill: string): boolean {
    const normalizedSkill = requiredSkill.toLowerCase();

    if (devSkills.has(normalizedSkill)) {
      return true;
    }

    // Check synonyms
    const synonyms = this.skillSynonyms.get(normalizedSkill) || [];
    return synonyms.some(syn => devSkills.has(syn.toLowerCase()));
  }

  /**
   * Calculate experience match score
   */
  private calculateExperienceMatch(
    profile: DeveloperProfile,
    requirement: DeveloperRequirement
  ): number {
    const yearsGap = profile.experienceYears - requirement.minExperienceYears;

    if (yearsGap < 0) {
      // Under-qualified: penalize proportionally
      return Math.max(0, 1 + (yearsGap / requirement.minExperienceYears));
    } else if (yearsGap <= 3) {
      // Perfect range
      return 1.0;
    } else {
      // Over-qualified: slight penalty for potential overqualification
      return Math.max(0.7, 1 - ((yearsGap - 3) * 0.05));
    }
  }

  /**
   * Calculate tech stack match
   */
  private calculateTechStackMatch(
    profile: DeveloperProfile,
    requirement: DeveloperRequirement
  ): number {
    const devTech = new Set([
      ...profile.primaryLanguages,
      ...profile.frameworks,
    ].map(t => t.toLowerCase()));

    let matches = 0;
    for (const tech of requirement.techStack) {
      if (this.hasSkill(devTech, tech)) {
        matches++;
      }
    }

    return requirement.techStack.length > 0
      ? matches / requirement.techStack.length
      : 0.5;
  }

  /**
   * Calculate seniority match
   */
  private calculateSeniorityMatch(
    profile: DeveloperProfile,
    requirement: DeveloperRequirement
  ): number {
    const seniorityLevels = ['junior', 'mid', 'senior', 'lead', 'principal', 'architect'];
    const devLevel = seniorityLevels.indexOf(profile.seniority);

    if (requirement.preferredSeniority.includes(profile.seniority)) {
      return 1.0;
    }

    // Find closest preferred seniority
    let minDistance = Infinity;
    for (const preferred of requirement.preferredSeniority) {
      const prefLevel = seniorityLevels.indexOf(preferred);
      const distance = Math.abs(devLevel - prefLevel);
      minDistance = Math.min(minDistance, distance);
    }

    // Score decreases by 0.15 per level difference
    return Math.max(0, 1 - (minDistance * 0.15));
  }

  /**
   * Calculate cultural fit (basic implementation)
   */
  private calculateCulturalFit(
    developer: Contact,
    requirement: DeveloperRequirement
  ): number {
    let score = 0.5; // Base score

    // Remote experience match
    if (requirement.remote && developer.metadata?.remoteExperience) {
      score += 0.3;
    }

    // Company stage match (if available)
    const devCompanies = developer.metadata?.previousCompanies || [];
    if (devCompanies.length > 0) {
      score += 0.2;
    }

    return Math.min(1.0, score);
  }

  /**
   * Analyze strengths and gaps
   */
  private analyzeStrengthsAndGaps(
    profile: DeveloperProfile,
    requirement: DeveloperRequirement,
    scores: any
  ): { strengths: string[]; gaps: string[] } {
    const strengths: string[] = [];
    const gaps: string[] = [];

    if (scores.skillsMatch >= 0.8) {
      strengths.push(`Strong skills match (${(scores.skillsMatch * 100).toFixed(0)}%)`);
    } else if (scores.skillsMatch < 0.6) {
      gaps.push(`Skills gap - missing some key requirements`);
    }

    if (scores.experienceMatch >= 0.9) {
      strengths.push(`Perfect experience level (${profile.experienceYears} years)`);
    } else if (scores.experienceMatch < 0.7) {
      if (profile.experienceYears < requirement.minExperienceYears) {
        gaps.push(`Needs ${requirement.minExperienceYears - profile.experienceYears} more years of experience`);
      } else {
        gaps.push(`May be overqualified for the role`);
      }
    }

    if (scores.techStackMatch >= 0.8) {
      strengths.push(`Excellent tech stack alignment`);
    } else if (scores.techStackMatch < 0.5) {
      gaps.push(`Limited experience with required tech stack`);
    }

    if (scores.seniorityMatch === 1.0) {
      strengths.push(`Perfect seniority match (${profile.seniority})`);
    }

    return { strengths, gaps };
  }

  /**
   * Generate hiring recommendation
   */
  private generateRecommendation(
    score: number,
    strengths: string[],
    gaps: string[],
    requirement: DeveloperRequirement
  ): string {
    if (score >= 0.85) {
      return `Excellent match! ${strengths.join('. ')}. Highly recommended for interview.`;
    } else if (score >= 0.7) {
      return `Strong candidate. ${strengths.join('. ')}. ${gaps.length > 0 ? 'Minor concerns: ' + gaps.join(', ') : ''}`;
    } else if (score >= 0.55) {
      return `Moderate match. May require additional training or mentorship. Gaps: ${gaps.join(', ')}`;
    } else {
      return `Not recommended. Significant gaps: ${gaps.join(', ')}`;
    }
  }

  /**
   * Extract developer profile from contact
   */
  private extractDeveloperProfile(contact: Contact): DeveloperProfile {
    const skills = contact.skills || [];
    const metadata = contact.metadata || {};

    // Extract from skills array
    const languages: string[] = [];
    const frameworks: string[] = [];
    const specializations: string[] = [];

    const knownLanguages = new Set([
      'javascript', 'typescript', 'python', 'java', 'c++', 'c#', 'ruby',
      'go', 'rust', 'swift', 'kotlin', 'php', 'scala', 'r'
    ]);

    const knownFrameworks = new Set([
      'react', 'vue', 'angular', 'node.js', 'express', 'django', 'flask',
      'spring', 'rails', 'laravel', 'next.js', 'nest.js', 'fastapi'
    ]);

    for (const skill of skills) {
      const lowerSkill = skill.toLowerCase();
      if (knownLanguages.has(lowerSkill)) {
        languages.push(skill);
      } else if (knownFrameworks.has(lowerSkill)) {
        frameworks.push(skill);
      } else {
        specializations.push(skill);
      }
    }

    return {
      primaryLanguages: languages,
      frameworks: frameworks,
      experienceYears: metadata.experienceYears || this.estimateExperience(contact),
      seniority: (metadata.seniority || this.estimateSeniority(contact)) as any,
      specializations: specializations,
      previousCompanies: metadata.previousCompanies,
      education: metadata.education,
      certifications: metadata.certifications,
      githubActivity: metadata.githubActivity,
      remoteExperience: metadata.remoteExperience,
    };
  }

  /**
   * Estimate experience from profile
   */
  private estimateExperience(contact: Contact): number {
    // Try to infer from bio or title
    const bio = (contact.bio || '').toLowerCase();
    const title = (contact.title || '').toLowerCase();

    if (bio.includes('10+ years') || bio.includes('10 years')) return 10;
    if (bio.includes('5+ years') || bio.includes('5 years')) return 5;
    if (title.includes('senior')) return 7;
    if (title.includes('lead') || title.includes('principal')) return 10;
    if (title.includes('junior')) return 2;

    return 3; // Default mid-level
  }

  /**
   * Estimate seniority from profile
   */
  private estimateSeniority(contact: Contact): string {
    const title = (contact.title || '').toLowerCase();

    if (title.includes('principal') || title.includes('architect')) return 'principal';
    if (title.includes('lead') || title.includes('staff')) return 'lead';
    if (title.includes('senior')) return 'senior';
    if (title.includes('junior')) return 'junior';

    return 'mid';
  }

  /**
   * Initialize skill synonyms for better matching
   */
  private initializeSkillSynonyms(): Map<string, string[]> {
    return new Map([
      ['javascript', ['js', 'ecmascript', 'es6', 'es2015']],
      ['typescript', ['ts']],
      ['react', ['reactjs', 'react.js']],
      ['node.js', ['nodejs', 'node']],
      ['vue', ['vuejs', 'vue.js']],
      ['angular', ['angularjs', 'angular.js']],
      ['machine learning', ['ml', 'ai', 'artificial intelligence']],
      ['deep learning', ['dl', 'neural networks']],
      ['devops', ['ci/cd', 'continuous integration', 'continuous deployment']],
      ['kubernetes', ['k8s']],
      ['postgresql', ['postgres', 'psql']],
      ['mongodb', ['mongo']],
    ]);
  }

  /**
   * Bulk match developers
   */
  bulkMatchDevelopers(
    candidates: Contact[],
    requirement: DeveloperRequirement,
    topN: number = 10
  ): Array<{
    contact: Contact;
    matchResult: ReturnType<typeof this.matchDeveloper>;
  }> {
    const results = candidates.map(candidate => ({
      contact: candidate,
      matchResult: this.matchDeveloper(candidate, requirement),
    }));

    // Sort by score descending
    results.sort((a, b) => b.matchResult.score - a.matchResult.score);

    return results.slice(0, topN);
  }
}
