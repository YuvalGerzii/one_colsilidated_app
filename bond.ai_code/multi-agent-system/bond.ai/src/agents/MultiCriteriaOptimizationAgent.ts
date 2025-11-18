/**
 * Multi-Criteria Optimization Agent
 *
 * Handles complex matching scenarios with multiple, potentially conflicting objectives.
 * Uses advanced optimization techniques to find Pareto-optimal solutions.
 *
 * Key Features:
 * - Multi-objective optimization
 * - Constraint satisfaction
 * - Trade-off analysis
 * - Pareto frontier identification
 * - Diversity optimization
 */

import { Contact } from '../types';

export interface OptimizationObjective {
  name: string;
  weight: number;
  minimize: boolean; // false = maximize
  evaluator: (seeker: Contact, candidate: Contact) => number;
}

export interface OptimizationConstraint {
  name: string;
  type: 'hard' | 'soft';
  validator: (candidate: Contact) => boolean | number; // boolean for hard, 0-1 for soft
  penalty?: number; // for soft constraints
}

export interface OptimizationResult {
  candidate: Contact;
  objectiveScores: Map<string, number>;
  overallScore: number;
  constraintViolations: string[];
  paretoOptimal: boolean;
  tradeoffs: string[];
}

export interface DiversityConfig {
  diversityWeight: number;
  diversityDimensions: string[]; // e.g., 'industry', 'location', 'experience'
}

export class MultiCriteriaOptimizationAgent {
  /**
   * Find optimal matches considering multiple objectives and constraints
   */
  async optimizeMatches(
    seeker: Contact,
    candidates: Contact[],
    objectives: OptimizationObjective[],
    constraints: OptimizationConstraint[],
    options?: {
      maxResults?: number;
      diversityConfig?: DiversityConfig;
      paretoOnly?: boolean;
    }
  ): Promise<OptimizationResult[]> {
    // Step 1: Filter by hard constraints
    const feasibleCandidates = this.filterByHardConstraints(candidates, constraints);

    if (feasibleCandidates.length === 0) {
      console.warn('No candidates satisfy hard constraints');
      return [];
    }

    // Step 2: Evaluate all objectives for each candidate
    const evaluatedCandidates = feasibleCandidates.map(candidate => {
      const objectiveScores = new Map<string, number>();

      for (const objective of objectives) {
        const score = objective.evaluator(seeker, candidate);
        objectiveScores.set(objective.name, score);
      }

      return { candidate, objectiveScores };
    });

    // Step 3: Apply soft constraints
    const withSoftConstraints = this.applySoftConstraints(
      evaluatedCandidates,
      constraints,
      objectives
    );

    // Step 4: Calculate weighted overall scores
    const withOverallScores = withSoftConstraints.map(item => {
      const overallScore = this.calculateWeightedScore(item.objectiveScores, objectives);
      return { ...item, overallScore };
    });

    // Step 5: Identify Pareto-optimal solutions
    const paretoResults = this.identifyParetoFrontier(withOverallScores, objectives);

    // Step 6: Generate trade-off analysis
    const withTradeoffs = paretoResults.map(result => ({
      ...result,
      tradeoffs: this.analyzeTradeoffs(result, objectives),
      constraintViolations: this.checkSoftConstraintViolations(result.candidate, constraints)
    }));

    // Step 7: Apply diversity if requested
    let finalResults = withTradeoffs;
    if (options?.diversityConfig) {
      finalResults = this.applyDiversityOptimization(
        withTradeoffs,
        seeker,
        options.diversityConfig
      );
    }

    // Step 8: Filter to Pareto-optimal if requested
    if (options?.paretoOnly) {
      finalResults = finalResults.filter(r => r.paretoOptimal);
    }

    // Step 9: Sort and limit
    finalResults.sort((a, b) => b.overallScore - a.overallScore);

    const maxResults = options?.maxResults || 20;
    return finalResults.slice(0, maxResults);
  }

  /**
   * Create standard optimization objectives
   */
  createStandardObjectives(): OptimizationObjective[] {
    return [
      {
        name: 'Needs Match',
        weight: 0.35,
        minimize: false,
        evaluator: (seeker, candidate) => this.evaluateNeedsMatch(seeker, candidate)
      },
      {
        name: 'Skills Complementarity',
        weight: 0.25,
        minimize: false,
        evaluator: (seeker, candidate) => this.evaluateSkillsComplementarity(seeker, candidate)
      },
      {
        name: 'Experience Alignment',
        weight: 0.15,
        minimize: false,
        evaluator: (seeker, candidate) => this.evaluateExperienceAlignment(seeker, candidate)
      },
      {
        name: 'Geographic Proximity',
        weight: 0.10,
        minimize: false,
        evaluator: (seeker, candidate) => this.evaluateGeographicProximity(seeker, candidate)
      },
      {
        name: 'Response Time',
        weight: 0.10,
        minimize: true, // Lower is better
        evaluator: (seeker, candidate) => this.evaluateResponseTime(candidate)
      },
      {
        name: 'Profile Quality',
        weight: 0.05,
        minimize: false,
        evaluator: (seeker, candidate) => this.evaluateProfileQuality(candidate)
      }
    ];
  }

  /**
   * Create standard constraints
   */
  createStandardConstraints(requirements: any): OptimizationConstraint[] {
    const constraints: OptimizationConstraint[] = [];

    // Hard constraints
    if (requirements.requiredSkills && requirements.requiredSkills.length > 0) {
      constraints.push({
        name: 'Required Skills',
        type: 'hard',
        validator: (candidate) => {
          const candidateSkills = new Set((candidate.skills || []).map(s => s.toLowerCase()));
          return requirements.requiredSkills.every((skill: string) =>
            candidateSkills.has(skill.toLowerCase())
          );
        }
      });
    }

    if (requirements.requiredIndustries && requirements.requiredIndustries.length > 0) {
      constraints.push({
        name: 'Industry Match',
        type: 'hard',
        validator: (candidate) => {
          return requirements.requiredIndustries.some((ind: string) =>
            candidate.industry?.toLowerCase().includes(ind.toLowerCase())
          );
        }
      });
    }

    if (requirements.minExperience) {
      constraints.push({
        name: 'Minimum Experience',
        type: 'hard',
        validator: (candidate) => {
          const exp = candidate.metadata?.experienceYears || 0;
          return exp >= requirements.minExperience;
        }
      });
    }

    // Soft constraints
    if (requirements.preferredLocations && requirements.preferredLocations.length > 0) {
      constraints.push({
        name: 'Preferred Location',
        type: 'soft',
        validator: (candidate) => {
          if (!candidate.location) return 0;

          const matches = requirements.preferredLocations.some((loc: string) =>
            candidate.location!.toLowerCase().includes(loc.toLowerCase())
          );
          return matches ? 1 : 0.3;
        },
        penalty: 0.2
      });
    }

    if (requirements.preferredCompanySize) {
      constraints.push({
        name: 'Company Size Preference',
        type: 'soft',
        validator: (candidate) => {
          const companySize = candidate.metadata?.companySize || 'unknown';
          return companySize === requirements.preferredCompanySize ? 1 : 0.5;
        },
        penalty: 0.1
      });
    }

    return constraints;
  }

  /**
   * Filter by hard constraints
   */
  private filterByHardConstraints(
    candidates: Contact[],
    constraints: OptimizationConstraint[]
  ): Contact[] {
    const hardConstraints = constraints.filter(c => c.type === 'hard');

    return candidates.filter(candidate => {
      return hardConstraints.every(constraint => {
        const result = constraint.validator(candidate);
        return typeof result === 'boolean' ? result : result > 0.5;
      });
    });
  }

  /**
   * Apply soft constraints
   */
  private applySoftConstraints(
    evaluated: Array<{ candidate: Contact; objectiveScores: Map<string, number> }>,
    constraints: OptimizationConstraint[],
    objectives: OptimizationObjective[]
  ): Array<{ candidate: Contact; objectiveScores: Map<string, number> }> {
    const softConstraints = constraints.filter(c => c.type === 'soft');

    return evaluated.map(item => {
      const adjustedScores = new Map(item.objectiveScores);

      // Apply penalties for soft constraint violations
      for (const constraint of softConstraints) {
        const satisfaction = constraint.validator(item.candidate);
        const satisfactionScore = typeof satisfaction === 'boolean'
          ? (satisfaction ? 1 : 0)
          : satisfaction;

        if (satisfactionScore < 1 && constraint.penalty) {
          // Reduce all objective scores proportionally
          for (const [objName, score] of adjustedScores.entries()) {
            const penalized = score * (1 - constraint.penalty * (1 - satisfactionScore));
            adjustedScores.set(objName, penalized);
          }
        }
      }

      return {
        ...item,
        objectiveScores: adjustedScores
      };
    });
  }

  /**
   * Calculate weighted overall score
   */
  private calculateWeightedScore(
    objectiveScores: Map<string, number>,
    objectives: OptimizationObjective[]
  ): number {
    let totalScore = 0;
    let totalWeight = 0;

    for (const objective of objectives) {
      const score = objectiveScores.get(objective.name) || 0;
      const normalizedScore = objective.minimize ? (1 - score) : score;

      totalScore += normalizedScore * objective.weight;
      totalWeight += objective.weight;
    }

    return totalWeight > 0 ? totalScore / totalWeight : 0;
  }

  /**
   * Identify Pareto-optimal solutions
   *
   * A solution is Pareto-optimal if no other solution is better in all objectives
   */
  private identifyParetoFrontier(
    results: Array<{ candidate: Contact; objectiveScores: Map<string, number>; overallScore: number }>,
    objectives: OptimizationObjective[]
  ): OptimizationResult[] {
    const paretoResults: OptimizationResult[] = [];

    for (const result of results) {
      let isDominated = false;

      // Check if this result is dominated by any other result
      for (const other of results) {
        if (result === other) continue;

        let betterInAll = true;
        let betterInSome = false;

        // Compare all objectives
        for (const objective of objectives) {
          const resultScore = result.objectiveScores.get(objective.name) || 0;
          const otherScore = other.objectiveScores.get(objective.name) || 0;

          if (objective.minimize) {
            if (otherScore >= resultScore) {
              betterInAll = false;
            }
            if (otherScore < resultScore) {
              betterInSome = true;
            }
          } else {
            if (otherScore <= resultScore) {
              betterInAll = false;
            }
            if (otherScore > resultScore) {
              betterInSome = true;
            }
          }
        }

        // If another solution is better or equal in all objectives and better in some,
        // then this result is dominated
        if (betterInAll || (betterInSome && !betterInAll === false)) {
          isDominated = true;
          break;
        }
      }

      paretoResults.push({
        candidate: result.candidate,
        objectiveScores: result.objectiveScores,
        overallScore: result.overallScore,
        constraintViolations: [],
        paretoOptimal: !isDominated,
        tradeoffs: []
      });
    }

    return paretoResults;
  }

  /**
   * Analyze trade-offs for a solution
   */
  private analyzeTradeoffs(
    result: OptimizationResult,
    objectives: OptimizationObjective[]
  ): string[] {
    const tradeoffs: string[] = [];

    // Find objectives where this solution is strong/weak
    const scores: Array<{ name: string; score: number; weight: number }> = [];

    for (const objective of objectives) {
      const score = result.objectiveScores.get(objective.name) || 0;
      scores.push({ name: objective.name, score, weight: objective.weight });
    }

    scores.sort((a, b) => b.score - a.score);

    const strong = scores.slice(0, 2);
    const weak = scores.slice(-2).reverse();

    if (strong.length > 0) {
      tradeoffs.push(`Strong in: ${strong.map(s => `${s.name} (${(s.score * 100).toFixed(0)}%)`).join(', ')}`);
    }

    if (weak.length > 0 && weak[0].score < 0.5) {
      tradeoffs.push(`Weaker in: ${weak.map(s => `${s.name} (${(s.score * 100).toFixed(0)}%)`).join(', ')}`);
    }

    return tradeoffs;
  }

  /**
   * Check soft constraint violations
   */
  private checkSoftConstraintViolations(
    candidate: Contact,
    constraints: OptimizationConstraint[]
  ): string[] {
    const violations: string[] = [];

    for (const constraint of constraints) {
      if (constraint.type === 'soft') {
        const satisfaction = constraint.validator(candidate);
        const satisfactionScore = typeof satisfaction === 'boolean'
          ? (satisfaction ? 1 : 0)
          : satisfaction;

        if (satisfactionScore < 0.7) {
          violations.push(`${constraint.name}: ${(satisfactionScore * 100).toFixed(0)}% satisfied`);
        }
      }
    }

    return violations;
  }

  /**
   * Apply diversity optimization
   */
  private applyDiversityOptimization(
    results: OptimizationResult[],
    seeker: Contact,
    config: DiversityConfig
  ): OptimizationResult[] {
    // Track diversity across specified dimensions
    const selected: OptimizationResult[] = [];
    const diversityTracker = new Map<string, Set<string>>();

    for (const dimension of config.diversityDimensions) {
      diversityTracker.set(dimension, new Set());
    }

    // Sort by score first
    const sorted = [...results].sort((a, b) => b.overallScore - a.overallScore);

    for (const result of sorted) {
      // Calculate diversity bonus
      let diversityBonus = 0;

      for (const dimension of config.diversityDimensions) {
        const value = this.getDimensionValue(result.candidate, dimension);
        const existing = diversityTracker.get(dimension)!;

        if (!existing.has(value)) {
          diversityBonus += 0.1; // Bonus for new dimension value
          existing.add(value);
        }
      }

      // Apply diversity bonus
      const boostedScore = result.overallScore * (1 + diversityBonus * config.diversityWeight);

      selected.push({
        ...result,
        overallScore: boostedScore
      });
    }

    return selected.sort((a, b) => b.overallScore - a.overallScore);
  }

  /**
   * Get dimension value for diversity tracking
   */
  private getDimensionValue(candidate: Contact, dimension: string): string {
    switch (dimension) {
      case 'industry':
        return candidate.industry || 'unknown';
      case 'location':
        return candidate.location?.split(',')[0] || 'unknown';
      case 'experience':
        const exp = candidate.metadata?.experienceYears || 5;
        if (exp < 3) return 'junior';
        if (exp < 7) return 'mid';
        if (exp < 15) return 'senior';
        return 'expert';
      case 'company_size':
        return candidate.metadata?.companySize || 'unknown';
      default:
        return 'unknown';
    }
  }

  /**
   * Objective evaluators
   */

  private evaluateNeedsMatch(seeker: Contact, candidate: Contact): number {
    const seekerNeeds = new Set((seeker.needs || []).map(n => n.toLowerCase()));
    const candidateOfferings = new Set((candidate.offerings || []).map(o => o.toLowerCase()));

    if (seekerNeeds.size === 0) return 0.5;

    let matches = 0;
    for (const need of seekerNeeds) {
      for (const offering of candidateOfferings) {
        if (offering.includes(need) || need.includes(offering)) {
          matches++;
          break;
        }
      }
    }

    return matches / seekerNeeds.size;
  }

  private evaluateSkillsComplementarity(seeker: Contact, candidate: Contact): number {
    const seekerSkills = new Set((seeker.skills || []).map(s => s.toLowerCase()));
    const candidateSkills = new Set((candidate.skills || []).map(s => s.toLowerCase()));

    if (seekerSkills.size === 0 && candidateSkills.size === 0) return 0.5;

    const allSkills = new Set([...seekerSkills, ...candidateSkills]);
    const overlap = [...seekerSkills].filter(s => candidateSkills.has(s)).length;

    // High complementarity = low overlap but many total skills
    return 1 - (overlap / Math.max(allSkills.size, 1));
  }

  private evaluateExperienceAlignment(seeker: Contact, candidate: Contact): number {
    const seekerExp = seeker.metadata?.experienceYears || 5;
    const candidateExp = candidate.metadata?.experienceYears || 5;

    const diff = Math.abs(seekerExp - candidateExp);

    // 3-10 years difference is good for mentorship
    if (diff >= 3 && diff <= 10) return 0.9;

    // Similar experience is good for peers
    if (diff <= 2) return 0.85;

    return Math.max(0.3, 1 - (diff * 0.05));
  }

  private evaluateGeographicProximity(seeker: Contact, candidate: Contact): number {
    if (!seeker.location || !candidate.location) return 0.5;

    const seekerLoc = seeker.location.toLowerCase();
    const candLoc = candidate.location.toLowerCase();

    if (seekerLoc === candLoc) return 1.0;

    // Same city
    if (seekerLoc.split(',')[0] === candLoc.split(',')[0]) return 0.85;

    // Same region
    if (seekerLoc.split(',').pop() === candLoc.split(',').pop()) return 0.6;

    return 0.3;
  }

  private evaluateResponseTime(candidate: Contact): number {
    // Lower is better (minimize objective)
    const responseRate = candidate.metadata?.responseRate || 0.5;
    const lastActive = candidate.metadata?.lastActive;

    if (!lastActive) return 0.5;

    const daysSince = this.getDaysSince(lastActive);
    const recencyScore = daysSince < 7 ? 0.1 : daysSince < 30 ? 0.3 : 0.7;

    // Combine: 70% response rate, 30% recency
    return (1 - responseRate) * 0.7 + recencyScore * 0.3;
  }

  private evaluateProfileQuality(candidate: Contact): number {
    let score = 0.3;

    if (candidate.bio && candidate.bio.length > 100) score += 0.2;
    if (candidate.skills && candidate.skills.length >= 3) score += 0.15;
    if (candidate.metadata?.verified) score += 0.2;
    if (candidate.metadata?.profileQuality) {
      score += candidate.metadata.profileQuality * 0.15;
    }

    return Math.min(1.0, score);
  }

  private getDaysSince(dateString: string): number {
    const date = new Date(dateString);
    const now = new Date();
    return Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24));
  }
}
