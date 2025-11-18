/**
 * UI/UX Designer Matching Agent
 * Specializes in matching design talent with creative and product needs
 * Focuses on design skills, portfolio, tools, and aesthetic alignment
 */

import { Contact, Match } from '../types';

export interface DesignerProfile {
  designDisciplines: string[]; // UI, UX, Product Design, Visual Design, etc.
  toolProficiency: string[]; // Figma, Sketch, Adobe XD, etc.
  experienceYears: number;
  seniority: 'junior' | 'mid' | 'senior' | 'lead' | 'principal';
  specializations: string[]; // Mobile, Web, Desktop, B2B, B2C, etc.
  portfolioQuality?: 'exceptional' | 'strong' | 'good' | 'developing';
  designSystem Experience?: boolean;
  researchSkills?: 'expert' | 'intermediate' | 'basic' | 'none';
  frontendSkills?: string[]; // HTML, CSS, React, etc.
  previousProducts?: string[];
  industryExperience?: string[];
}

export interface DesignerRequirement {
  primaryDiscipline: 'ui' | 'ux' | 'product' | 'visual' | 'brand' | 'motion';
  requiredTools: string[];
  preferredTools: string[];
  minExperienceYears: number;
  preferredSeniority: string[];
  projectType: 'web' | 'mobile' | 'desktop' | 'multi-platform';
  productStage: 'mvp' | 'growth' | 'scale' | 'redesign';
  needsResearch: boolean;
  needsFrontendSkills: boolean;
  designSystemRequired: boolean;
  aestheticStyle?: 'minimal' | 'modern' | 'playful' | 'corporate' | 'luxury';
  industry?: string;
}

export class UIDesignerMatchingAgent {
  private toolCategories: Map<string, string[]>;
  private disciplineHierarchy: Map<string, number>;

  constructor() {
    this.toolCategories = this.initializeToolCategories();
    this.disciplineHierarchy = this.initializeDisciplineHierarchy();
  }

  /**
   * Match a designer with a hiring requirement
   */
  matchDesigner(
    designer: Contact,
    requirement: DesignerRequirement
  ): {
    score: number;
    breakdown: {
      disciplineMatch: number;
      toolProficiency: number;
      experienceMatch: number;
      specialization: number;
      portfolioFit: number;
    };
    strengths: string[];
    concerns: string[];
    recommendation: string;
  } {
    const designerProfile = this.extractDesignerProfile(designer);

    // Calculate dimension scores
    const disciplineMatch = this.calculateDisciplineMatch(
      designerProfile,
      requirement
    );

    const toolProficiency = this.calculateToolProficiency(
      designerProfile,
      requirement
    );

    const experienceMatch = this.calculateExperienceMatch(
      designerProfile,
      requirement
    );

    const specialization = this.calculateSpecializationMatch(
      designerProfile,
      requirement
    );

    const portfolioFit = this.calculatePortfolioFit(
      designerProfile,
      requirement
    );

    // Weighted overall score
    const score = (
      disciplineMatch * 0.30 +
      toolProficiency * 0.25 +
      experienceMatch * 0.20 +
      specialization * 0.15 +
      portfolioFit * 0.10
    );

    // Generate analysis
    const { strengths, concerns } = this.analyzeDesigner(
      designerProfile,
      requirement,
      { disciplineMatch, toolProficiency, experienceMatch, specialization, portfolioFit }
    );

    const recommendation = this.generateRecommendation(score, strengths, concerns);

    return {
      score,
      breakdown: {
        disciplineMatch,
        toolProficiency,
        experienceMatch,
        specialization,
        portfolioFit,
      },
      strengths,
      concerns,
      recommendation,
    };
  }

  /**
   * Calculate discipline match
   */
  private calculateDisciplineMatch(
    profile: DesignerProfile,
    requirement: DesignerRequirement
  ): number {
    const disciplines = profile.designDisciplines.map(d => d.toLowerCase());

    // Direct match
    if (disciplines.includes(requirement.primaryDiscipline.toLowerCase())) {
      return 1.0;
    }

    // Related disciplines
    const relatedScore = this.getRelatedDisciplineScore(
      disciplines,
      requirement.primaryDiscipline
    );

    return relatedScore;
  }

  /**
   * Get score for related disciplines
   */
  private getRelatedDisciplineScore(
    designerDisciplines: string[],
    requiredDiscipline: string
  ): number {
    const relationships = new Map<string, Map<string, number>>([
      ['product', new Map([
        ['ux', 0.9],
        ['ui', 0.8],
        ['visual', 0.6],
      ])],
      ['ux', new Map([
        ['product', 0.9],
        ['ui', 0.7],
      ])],
      ['ui', new Map([
        ['product', 0.8],
        ['ux', 0.7],
        ['visual', 0.8],
      ])],
      ['visual', new Map([
        ['ui', 0.8],
        ['brand', 0.7],
      ])],
    ]);

    const required = requiredDiscipline.toLowerCase();
    const relatedScores = relationships.get(required);

    if (!relatedScores) return 0.5;

    for (const discipline of designerDisciplines) {
      const score = relatedScores.get(discipline);
      if (score) return score;
    }

    return 0.4; // Some design experience, but not closely related
  }

  /**
   * Calculate tool proficiency match
   */
  private calculateToolProficiency(
    profile: DesignerProfile,
    requirement: DesignerRequirement
  ): number {
    const designerTools = new Set(
      profile.toolProficiency.map(t => t.toLowerCase())
    );

    // Required tools score
    let requiredMatches = 0;
    for (const tool of requirement.requiredTools) {
      if (this.hasToolOrEquivalent(designerTools, tool)) {
        requiredMatches++;
      }
    }

    const requiredScore = requirement.requiredTools.length > 0
      ? requiredMatches / requirement.requiredTools.length
      : 1.0;

    // Preferred tools score
    let preferredMatches = 0;
    for (const tool of requirement.preferredTools) {
      if (this.hasToolOrEquivalent(designerTools, tool)) {
        preferredMatches++;
      }
    }

    const preferredScore = requirement.preferredTools.length > 0
      ? preferredMatches / requirement.preferredTools.length
      : 0.5;

    // Required tools are 75%, preferred are 25%
    return requiredScore * 0.75 + preferredScore * 0.25;
  }

  /**
   * Check if designer has tool or equivalent
   */
  private hasToolOrEquivalent(designerTools: Set<string>, requiredTool: string): boolean {
    const normalized = requiredTool.toLowerCase();

    if (designerTools.has(normalized)) {
      return true;
    }

    // Check for equivalent tools
    const category = this.getToolCategory(normalized);
    if (category) {
      const equivalents = this.toolCategories.get(category) || [];
      return equivalents.some(tool => designerTools.has(tool.toLowerCase()));
    }

    return false;
  }

  /**
   * Get tool category
   */
  private getToolCategory(tool: string): string | null {
    for (const [category, tools] of this.toolCategories.entries()) {
      if (tools.some(t => t.toLowerCase() === tool.toLowerCase())) {
        return category;
      }
    }
    return null;
  }

  /**
   * Calculate experience match
   */
  private calculateExperienceMatch(
    profile: DesignerProfile,
    requirement: DesignerRequirement
  ): number {
    const yearsGap = profile.experienceYears - requirement.minExperienceYears;

    if (yearsGap < 0) {
      // Under-qualified
      return Math.max(0, 1 + (yearsGap / requirement.minExperienceYears));
    } else if (yearsGap <= 2) {
      // Perfect range
      return 1.0;
    } else {
      // Over-qualified (less penalty than dev roles)
      return Math.max(0.8, 1 - ((yearsGap - 2) * 0.03));
    }
  }

  /**
   * Calculate specialization match
   */
  private calculateSpecializationMatch(
    profile: DesignerProfile,
    requirement: DesignerRequirement
  ): number {
    let score = 0.5;

    // Project type match
    const projectTypes = profile.specializations.map(s => s.toLowerCase());
    if (projectTypes.includes(requirement.projectType)) {
      score += 0.2;
    }

    // Research skills match
    if (requirement.needsResearch) {
      if (profile.researchSkills === 'expert') score += 0.2;
      else if (profile.researchSkills === 'intermediate') score += 0.1;
      else score -= 0.1;
    } else {
      score += 0.1;
    }

    // Frontend skills match
    if (requirement.needsFrontendSkills) {
      if (profile.frontendSkills && profile.frontendSkills.length > 0) {
        score += 0.15;
      } else {
        score -= 0.1;
      }
    } else {
      score += 0.05;
    }

    // Design system experience
    if (requirement.designSystemRequired) {
      if (profile.designSystemExperience) {
        score += 0.15;
      } else {
        score -= 0.15;
      }
    }

    return Math.max(0, Math.min(1.0, score));
  }

  /**
   * Calculate portfolio fit
   */
  private calculatePortfolioFit(
    profile: DesignerProfile,
    requirement: DesignerRequirement
  ): number {
    let score = 0.5;

    // Portfolio quality
    if (profile.portfolioQuality === 'exceptional') score = 1.0;
    else if (profile.portfolioQuality === 'strong') score = 0.85;
    else if (profile.portfolioQuality === 'good') score = 0.7;
    else if (profile.portfolioQuality === 'developing') score = 0.5;

    // Industry experience match
    if (requirement.industry && profile.industryExperience) {
      const hasIndustry = profile.industryExperience.some(
        ind => ind.toLowerCase().includes(requirement.industry!.toLowerCase())
      );
      if (hasIndustry) {
        score = Math.min(1.0, score + 0.15);
      }
    }

    return score;
  }

  /**
   * Analyze designer strengths and concerns
   */
  private analyzeDesigner(
    profile: DesignerProfile,
    requirement: DesignerRequirement,
    scores: any
  ): { strengths: string[]; concerns: string[] } {
    const strengths: string[] = [];
    const concerns: string[] = [];

    if (scores.disciplineMatch >= 0.9) {
      strengths.push(`Expert in ${requirement.primaryDiscipline} design`);
    } else if (scores.disciplineMatch < 0.6) {
      concerns.push(`Limited experience in ${requirement.primaryDiscipline} design`);
    }

    if (scores.toolProficiency >= 0.8) {
      strengths.push(`Proficient in required tools`);
    } else if (scores.toolProficiency < 0.6) {
      concerns.push(`May need training on required design tools`);
    }

    if (profile.portfolioQuality === 'exceptional' || profile.portfolioQuality === 'strong') {
      strengths.push(`${profile.portfolioQuality} portfolio quality`);
    }

    if (requirement.designSystemRequired && !profile.designSystemExperience) {
      concerns.push(`No design system experience`);
    }

    if (requirement.needsResearch && profile.researchSkills === 'none') {
      concerns.push(`Limited UX research capabilities`);
    }

    if (profile.experienceYears >= requirement.minExperienceYears + 3) {
      strengths.push(`${profile.experienceYears} years of design experience`);
    }

    return { strengths, concerns };
  }

  /**
   * Generate recommendation
   */
  private generateRecommendation(
    score: number,
    strengths: string[],
    concerns: string[]
  ): string {
    if (score >= 0.8) {
      return `Excellent designer match! ${strengths.join('. ')}. Strongly recommended for portfolio review.`;
    } else if (score >= 0.65) {
      return `Good candidate. ${strengths.join('. ')}. ${concerns.length > 0 ? 'Note: ' + concerns.join(', ') : ''}`;
    } else if (score >= 0.5) {
      return `Moderate fit. Concerns: ${concerns.join(', ')}. Consider if strong portfolio demonstrates capability.`;
    } else {
      return `Not recommended. Significant gaps: ${concerns.join(', ')}`;
    }
  }

  /**
   * Extract designer profile from contact
   */
  private extractDesignerProfile(contact: Contact): DesignerProfile {
    const skills = contact.skills || [];
    const metadata = contact.metadata || {};

    const disciplines: string[] = [];
    const tools: string[] = [];
    const specializations: string[] = [];

    const knownDisciplines = new Set([
      'ui', 'ux', 'product design', 'visual design', 'brand design',
      'motion design', 'interaction design', 'graphic design'
    ]);

    const knownTools = new Set([
      'figma', 'sketch', 'adobe xd', 'photoshop', 'illustrator',
      'after effects', 'principle', 'framer', 'invision', 'zeplin'
    ]);

    for (const skill of skills) {
      const lowerSkill = skill.toLowerCase();
      if (knownDisciplines.has(lowerSkill)) {
        disciplines.push(skill);
      } else if (knownTools.has(lowerSkill)) {
        tools.push(skill);
      } else {
        specializations.push(skill);
      }
    }

    return {
      designDisciplines: disciplines,
      toolProficiency: tools,
      experienceYears: metadata.experienceYears || this.estimateExperience(contact),
      seniority: (metadata.seniority || this.estimateSeniority(contact)) as any,
      specializations: specializations,
      portfolioQuality: metadata.portfolioQuality,
      designSystemExperience: metadata.designSystemExperience,
      researchSkills: metadata.researchSkills,
      frontendSkills: metadata.frontendSkills,
      previousProducts: metadata.previousProducts,
      industryExperience: metadata.industryExperience,
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
    if (title.includes('senior')) return 6;
    if (title.includes('lead') || title.includes('principal')) return 8;
    if (title.includes('junior')) return 2;

    return 3;
  }

  /**
   * Estimate seniority
   */
  private estimateSeniority(contact: Contact): string {
    const title = (contact.title || '').toLowerCase();

    if (title.includes('principal') || title.includes('director')) return 'principal';
    if (title.includes('lead') || title.includes('head')) return 'lead';
    if (title.includes('senior')) return 'senior';
    if (title.includes('junior')) return 'junior';

    return 'mid';
  }

  /**
   * Initialize tool categories and equivalents
   */
  private initializeToolCategories(): Map<string, string[]> {
    return new Map([
      ['design_tool', ['Figma', 'Sketch', 'Adobe XD', 'Framer']],
      ['prototyping', ['Figma', 'Framer', 'Principle', 'ProtoPie', 'InVision']],
      ['graphics', ['Photoshop', 'Illustrator', 'Affinity Designer']],
      ['motion', ['After Effects', 'Principle', 'Lottie']],
      ['collaboration', ['Figma', 'InVision', 'Zeplin', 'Abstract']],
    ]);
  }

  /**
   * Initialize discipline hierarchy
   */
  private initializeDisciplineHierarchy(): Map<string, number> {
    return new Map([
      ['product', 5],
      ['ux', 4],
      ['ui', 3],
      ['visual', 2],
      ['brand', 1],
    ]);
  }

  /**
   * Bulk match designers
   */
  bulkMatchDesigners(
    candidates: Contact[],
    requirement: DesignerRequirement,
    topN: number = 10
  ): Array<{
    contact: Contact;
    matchResult: ReturnType<typeof this.matchDesigner>;
  }> {
    const results = candidates.map(candidate => ({
      contact: candidate,
      matchResult: this.matchDesigner(candidate, requirement),
    }));

    results.sort((a, b) => b.matchResult.score - a.matchResult.score);

    return results.slice(0, topN);
  }
}
