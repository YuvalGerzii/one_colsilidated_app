import { Pool } from 'pg';
import Redis from 'ioredis';
import { MatchQualityAgent } from './MatchQualityAgent';
import { TrustPropagationAgent } from './TrustPropagationAgent';

/**
 * Collaboration Prediction Agent
 *
 * Predicts success probability of potential collaborations between users.
 *
 * Analyzes:
 * - Skill complementarity
 * - Communication compatibility
 * - Trust levels
 * - Historical collaboration patterns
 * - Goal alignment
 * - Availability/capacity
 * - Cultural fit
 * - Risk factors
 *
 * Provides actionable recommendations for successful collaboration.
 */

export interface CollaborationPrediction {
  user1Id: string;
  user2Id: string;
  user1Name: string;
  user2Name: string;

  overallSuccessProbability: number; // 0-100
  confidence: number; // 0-1

  factors: {
    skillComplementarity: number; // 0-1
    communicationCompatibility: number; // 0-1
    trustLevel: number; // 0-1
    goalAlignment: number; // 0-1
    culturalFit: number; // 0-1
    availabilityMatch: number; // 0-1
    historicalSuccess: number; // 0-1
  };

  strengths: Array<{
    factor: string;
    score: number;
    description: string;
  }>;

  risks: Array<{
    factor: string;
    severity: 'low' | 'medium' | 'high';
    description: string;
    mitigation: string;
  }>;

  recommendations: Array<{
    category: 'communication' | 'planning' | 'trust-building' | 'skill-development';
    priority: 'high' | 'medium' | 'low';
    action: string;
    expectedImpact: number; // 0-1
  }>;

  optimalCollaborationType: 'short_term_project' | 'long_term_partnership' | 'one_time_introduction' | 'mentorship' | 'not_recommended';
  suggestedDuration: string;
  keySuccessFactors: string[];
}

export interface CollaborationOpportunity {
  id: string;
  type: 'project' | 'introduction' | 'advisory' | 'co_creation' | 'investment';
  participants: string[];
  successProbability: number;
  potentialValue: number; // 0-100
  timeframe: string;
  requirements: string[];
  benefits: string[];
}

export interface TeamCompatibility {
  teamMembers: string[];
  overallCompatibility: number; // 0-100
  pairwiseScores: Map<string, Map<string, number>>;
  teamStrengths: string[];
  teamRisks: string[];
  recommendedRoles: Map<string, string>;
  optimalTeamSize: number;
}

export class CollaborationPredictionAgent {
  // Weights for success probability calculation
  private readonly WEIGHTS = {
    skillComplementarity: 0.25,
    communicationCompatibility: 0.15,
    trustLevel: 0.20,
    goalAlignment: 0.20,
    culturalFit: 0.10,
    availabilityMatch: 0.05,
    historicalSuccess: 0.05
  };

  constructor(
    private pool: Pool,
    private redis: Redis,
    private matchQualityAgent: MatchQualityAgent,
    private trustAgent: TrustPropagationAgent
  ) {}

  /**
   * Predict collaboration success between two users
   */
  async predictCollaboration(
    user1Id: string,
    user2Id: string
  ): Promise<CollaborationPrediction> {
    // Check cache
    const cacheKey = `collab_pred:${user1Id}:${user2Id}`;
    const cached = await this.redis.get(cacheKey);
    if (cached) return JSON.parse(cached);

    // Gather user profiles
    const [user1Profile, user2Profile] = await Promise.all([
      this.getUserProfile(user1Id),
      this.getUserProfile(user2Id)
    ]);

    // Calculate all factors
    const factors = await this.calculateFactors(user1Id, user2Id, user1Profile, user2Profile);

    // Calculate overall success probability
    const successProbability = this.calculateSuccessProbability(factors);

    // Identify strengths
    const strengths = this.identifyStrengths(factors);

    // Identify risks
    const risks = this.identifyRisks(factors, user1Profile, user2Profile);

    // Generate recommendations
    const recommendations = this.generateRecommendations(factors, risks);

    // Determine optimal collaboration type
    const optimalCollaborationType = this.determineCollaborationType(factors, successProbability);

    // Suggest duration
    const suggestedDuration = this.suggestDuration(factors, optimalCollaborationType);

    // Key success factors
    const keySuccessFactors = this.identifyKeySuccessFactors(factors, strengths);

    // Confidence based on data availability
    const confidence = this.calculateConfidence(user1Profile, user2Profile);

    const prediction: CollaborationPrediction = {
      user1Id,
      user2Id,
      user1Name: user1Profile.name || 'Unknown',
      user2Name: user2Profile.name || 'Unknown',
      overallSuccessProbability: Math.round(successProbability * 100),
      confidence,
      factors,
      strengths,
      risks,
      recommendations,
      optimalCollaborationType,
      suggestedDuration,
      keySuccessFactors
    };

    // Cache for 1 hour
    await this.redis.set(cacheKey, JSON.stringify(prediction), 'EX', 3600);

    return prediction;
  }

  /**
   * Find best collaboration opportunities for a user
   */
  async findCollaborationOpportunities(
    userId: string,
    options: {
      type?: CollaborationOpportunity['type'];
      minProbability?: number;
      limit?: number;
    } = {}
  ): Promise<CollaborationOpportunity[]> {
    const { type, minProbability = 60, limit = 10 } = options;

    // Get candidate collaborators
    const candidates = await this.getCandidateCollaborators(userId);

    // Score all candidates
    const predictions = await Promise.all(
      candidates.map(targetId => this.predictCollaboration(userId, targetId))
    );

    // Filter by minimum probability
    const filteredPredictions = predictions.filter(
      p => p.overallSuccessProbability >= minProbability
    );

    // Convert to opportunities
    const opportunities = filteredPredictions.map(pred => this.predictionToOpportunity(pred, userId));

    // Filter by type if specified
    const typeFiltered = type
      ? opportunities.filter(opp => opp.type === type)
      : opportunities;

    // Sort by potential value
    return typeFiltered
      .sort((a, b) => b.potentialValue - a.potentialValue)
      .slice(0, limit);
  }

  /**
   * Analyze team compatibility for multi-person collaborations
   */
  async analyzeTeamCompatibility(
    teamMembers: string[]
  ): Promise<TeamCompatibility> {
    if (teamMembers.length < 2) {
      throw new Error('Team must have at least 2 members');
    }

    // Calculate pairwise scores
    const pairwiseScores = new Map<string, Map<string, number>>();

    for (const member1 of teamMembers) {
      const scores = new Map<string, number>();

      for (const member2 of teamMembers) {
        if (member1 !== member2) {
          const prediction = await this.predictCollaboration(member1, member2);
          scores.set(member2, prediction.overallSuccessProbability);
        }
      }

      pairwiseScores.set(member1, scores);
    }

    // Calculate overall compatibility
    let totalScore = 0;
    let pairCount = 0;

    for (const scores of pairwiseScores.values()) {
      for (const score of scores.values()) {
        totalScore += score;
        pairCount++;
      }
    }

    const overallCompatibility = pairCount > 0 ? totalScore / pairCount : 0;

    // Identify team strengths
    const teamStrengths = await this.identifyTeamStrengths(teamMembers);

    // Identify team risks
    const teamRisks = await this.identifyTeamRisks(teamMembers, pairwiseScores);

    // Recommend roles
    const recommendedRoles = await this.recommendTeamRoles(teamMembers);

    // Optimal team size (based on compatibility degradation)
    const optimalTeamSize = this.calculateOptimalTeamSize(overallCompatibility, teamMembers.length);

    return {
      teamMembers,
      overallCompatibility: Math.round(overallCompatibility),
      pairwiseScores,
      teamStrengths,
      teamRisks,
      recommendedRoles,
      optimalTeamSize
    };
  }

  /**
   * Predict success of specific collaboration scenario
   */
  async predictScenario(
    participants: string[],
    scenario: {
      type: 'project' | 'partnership' | 'event';
      duration: 'short' | 'medium' | 'long';
      complexity: 'low' | 'medium' | 'high';
      requiredSkills: string[];
    }
  ): Promise<{
    successProbability: number;
    feasibility: number;
    recommendations: string[];
    missingSkills: string[];
    idealAdditions: Array<{ skill: string; candidateIds: string[] }>;
  }> {
    // Check if team has required skills
    const teamSkills = await this.getTeamSkills(participants);
    const missingSkills = scenario.requiredSkills.filter(
      skill => !teamSkills.includes(skill)
    );

    // Calculate base success probability
    const teamCompat = await this.analyzeTeamCompatibility(participants);
    let successProbability = teamCompat.overallCompatibility / 100;

    // Adjust for complexity
    if (scenario.complexity === 'high') {
      successProbability *= 0.8;
    } else if (scenario.complexity === 'low') {
      successProbability *= 1.1;
    }

    // Adjust for duration
    if (scenario.duration === 'long') {
      successProbability *= 0.9; // Longer = more risk
    }

    // Penalty for missing skills
    const skillCoverage = 1 - (missingSkills.length / Math.max(1, scenario.requiredSkills.length));
    successProbability *= (0.5 + skillCoverage * 0.5);

    // Feasibility
    const feasibility = skillCoverage * (teamCompat.overallCompatibility / 100);

    // Recommendations
    const recommendations: string[] = [];

    if (missingSkills.length > 0) {
      recommendations.push(`Add team members with: ${missingSkills.slice(0, 3).join(', ')}`);
    }

    if (teamCompat.overallCompatibility < 70) {
      recommendations.push('Conduct team building activities before starting');
    }

    if (scenario.complexity === 'high' && participants.length < 3) {
      recommendations.push('Consider expanding team size for complex project');
    }

    // Find ideal additions
    const idealAdditions = await this.findIdealTeamAdditions(
      participants,
      missingSkills
    );

    return {
      successProbability: Math.round(successProbability * 100),
      feasibility: Math.round(feasibility * 100),
      recommendations,
      missingSkills,
      idealAdditions
    };
  }

  /**
   * Private calculation methods
   */

  private async calculateFactors(
    user1Id: string,
    user2Id: string,
    user1Profile: any,
    user2Profile: any
  ): Promise<CollaborationPrediction['factors']> {
    // Skill complementarity
    const skillComplementarity = this.calculateSkillComplementarity(
      user1Profile,
      user2Profile
    );

    // Communication compatibility (simplified heuristic)
    const communicationCompatibility = this.calculateCommunicationCompatibility(
      user1Profile,
      user2Profile
    );

    // Trust level
    const trustData = await this.trustAgent.calculateTransitiveTrust(user1Id, user2Id);
    const trustLevel = trustData.directTrust !== null
      ? trustData.directTrust
      : trustData.indirectTrust;

    // Goal alignment
    const goalAlignment = this.calculateGoalAlignment(user1Profile, user2Profile);

    // Cultural fit (location, industry similarity)
    const culturalFit = this.calculateCulturalFit(user1Profile, user2Profile);

    // Availability match (placeholder)
    const availabilityMatch = 0.7;

    // Historical success (placeholder - would need collaboration history)
    const historicalSuccess = 0.6;

    return {
      skillComplementarity,
      communicationCompatibility,
      trustLevel,
      goalAlignment,
      culturalFit,
      availabilityMatch,
      historicalSuccess
    };
  }

  private calculateSuccessProbability(
    factors: CollaborationPrediction['factors']
  ): number {
    let probability = 0;

    probability += factors.skillComplementarity * this.WEIGHTS.skillComplementarity;
    probability += factors.communicationCompatibility * this.WEIGHTS.communicationCompatibility;
    probability += factors.trustLevel * this.WEIGHTS.trustLevel;
    probability += factors.goalAlignment * this.WEIGHTS.goalAlignment;
    probability += factors.culturalFit * this.WEIGHTS.culturalFit;
    probability += factors.availabilityMatch * this.WEIGHTS.availabilityMatch;
    probability += factors.historicalSuccess * this.WEIGHTS.historicalSuccess;

    return Math.max(0, Math.min(1, probability));
  }

  private calculateSkillComplementarity(user1Profile: any, user2Profile: any): number {
    const user1Skills = new Set(user1Profile.expertise_areas || []);
    const user2Skills = new Set(user2Profile.expertise_areas || []);

    const user1Needs = new Set(user1Profile.needs || []);
    const user2Offers = new Set(user2Profile.offers || []);

    const user2Needs = new Set(user2Profile.needs || []);
    const user1Offers = new Set(user1Profile.offers || []);

    // Count matches: user1 needs that user2 offers, and vice versa
    let matches = 0;
    let totalNeeds = Math.max(1, user1Needs.size + user2Needs.size);

    for (const need of user1Needs) {
      if (user2Offers.has(need)) matches++;
    }

    for (const need of user2Needs) {
      if (user1Offers.has(need)) matches++;
    }

    // Also value skill overlap (shared expertise)
    const skillOverlap = [...user1Skills].filter(s => user2Skills.has(s)).length;
    const sharedExpertiseBonus = Math.min(0.3, skillOverlap * 0.1);

    const complementarity = (matches / totalNeeds) + sharedExpertiseBonus;

    return Math.min(1, complementarity);
  }

  private calculateCommunicationCompatibility(user1Profile: any, user2Profile: any): number {
    // Simplified: based on industry and expertise overlap
    let score = 0.5; // Base score

    if (user1Profile.industry === user2Profile.industry) {
      score += 0.2; // Same industry = easier communication
    }

    const user1Expertise = new Set(user1Profile.expertise_areas || []);
    const user2Expertise = new Set(user2Profile.expertise_areas || []);
    const overlapCount = [...user1Expertise].filter(e => user2Expertise.has(e)).length;

    if (overlapCount > 0) {
      score += Math.min(0.3, overlapCount * 0.1);
    }

    return Math.min(1, score);
  }

  private calculateGoalAlignment(user1Profile: any, user2Profile: any): number {
    // Simplified: based on needs/offers match
    const user1Needs = new Set(user1Profile.needs || []);
    const user2Needs = new Set(user2Profile.needs || []);

    const commonNeeds = [...user1Needs].filter(n => user2Needs.has(n));

    // Having common needs = aligned goals
    const alignment = Math.min(1, commonNeeds.length * 0.25);

    return alignment > 0 ? alignment : 0.5; // Default to neutral
  }

  private calculateCulturalFit(user1Profile: any, user2Profile: any): number {
    let fit = 0.5; // Neutral base

    // Same location
    if (user1Profile.location?.country === user2Profile.location?.country) {
      fit += 0.3;
    }

    // Same industry
    if (user1Profile.industry === user2Profile.industry) {
      fit += 0.2;
    }

    return Math.min(1, fit);
  }

  private identifyStrengths(
    factors: CollaborationPrediction['factors']
  ): CollaborationPrediction['strengths'] {
    const strengths: CollaborationPrediction['strengths'] = [];

    if (factors.skillComplementarity >= 0.7) {
      strengths.push({
        factor: 'Skill Complementarity',
        score: factors.skillComplementarity,
        description: 'Strong skill match - complementary expertise and needs/offers alignment'
      });
    }

    if (factors.trustLevel >= 0.7) {
      strengths.push({
        factor: 'Trust Level',
        score: factors.trustLevel,
        description: 'High trust foundation - excellent basis for collaboration'
      });
    }

    if (factors.goalAlignment >= 0.7) {
      strengths.push({
        factor: 'Goal Alignment',
        score: factors.goalAlignment,
        description: 'Aligned objectives - working toward common goals'
      });
    }

    if (factors.communicationCompatibility >= 0.7) {
      strengths.push({
        factor: 'Communication',
        score: factors.communicationCompatibility,
        description: 'Compatible communication style - smooth interactions expected'
      });
    }

    return strengths.sort((a, b) => b.score - a.score);
  }

  private identifyRisks(
    factors: CollaborationPrediction['factors'],
    user1Profile: any,
    user2Profile: any
  ): CollaborationPrediction['risks'] {
    const risks: CollaborationPrediction['risks'] = [];

    if (factors.trustLevel < 0.4) {
      risks.push({
        factor: 'Low Trust',
        severity: 'high',
        description: 'Limited trust relationship - may affect collaboration effectiveness',
        mitigation: 'Start with small, low-risk collaboration to build trust incrementally'
      });
    }

    if (factors.skillComplementarity < 0.3) {
      risks.push({
        factor: 'Skill Mismatch',
        severity: 'medium',
        description: 'Limited skill complementarity - may not offer mutual value',
        mitigation: 'Clearly define value exchange and seek third-party additions'
      });
    }

    if (factors.communicationCompatibility < 0.4) {
      risks.push({
        factor: 'Communication Gap',
        severity: 'medium',
        description: 'Different backgrounds may lead to misunderstandings',
        mitigation: 'Establish clear communication protocols and regular check-ins'
      });
    }

    if (user1Profile.location?.country !== user2Profile.location?.country) {
      risks.push({
        factor: 'Geographic Distance',
        severity: 'low',
        description: 'Different locations may complicate coordination',
        mitigation: 'Use async communication tools and schedule overlapping hours'
      });
    }

    return risks.sort((a, b) => {
      const severityWeight = { high: 3, medium: 2, low: 1 };
      return severityWeight[b.severity] - severityWeight[a.severity];
    });
  }

  private generateRecommendations(
    factors: CollaborationPrediction['factors'],
    risks: CollaborationPrediction['risks']
  ): CollaborationPrediction['recommendations'] {
    const recommendations: CollaborationPrediction['recommendations'] = [];

    // Address each risk
    for (const risk of risks) {
      if (risk.severity === 'high' || risk.severity === 'medium') {
        if (risk.factor === 'Low Trust') {
          recommendations.push({
            category: 'trust-building',
            priority: 'high',
            action: risk.mitigation,
            expectedImpact: 0.8
          });
        } else if (risk.factor === 'Communication Gap') {
          recommendations.push({
            category: 'communication',
            priority: 'high',
            action: risk.mitigation,
            expectedImpact: 0.7
          });
        }
      }
    }

    // Always recommend planning
    recommendations.push({
      category: 'planning',
      priority: 'high',
      action: 'Create detailed collaboration plan with milestones and success metrics',
      expectedImpact: 0.6
    });

    // Leverage strengths
    if (factors.skillComplementarity >= 0.7) {
      recommendations.push({
        category: 'skill-development',
        priority: 'medium',
        action: 'Leverage complementary skills through knowledge exchange sessions',
        expectedImpact: 0.5
      });
    }

    return recommendations.sort((a, b) => {
      const priorityWeight = { high: 3, medium: 2, low: 1 };
      return priorityWeight[b.priority] - priorityWeight[a.priority];
    });
  }

  private determineCollaborationType(
    factors: CollaborationPrediction['factors'],
    probability: number
  ): CollaborationPrediction['optimalCollaborationType'] {
    if (probability < 0.4) {
      return 'not_recommended';
    }

    if (factors.trustLevel >= 0.8 && factors.goalAlignment >= 0.7) {
      return 'long_term_partnership';
    }

    if (factors.skillComplementarity >= 0.7) {
      return 'short_term_project';
    }

    if (probability >= 0.6) {
      return 'one_time_introduction';
    }

    return 'short_term_project';
  }

  private suggestDuration(
    factors: CollaborationPrediction['factors'],
    type: CollaborationPrediction['optimalCollaborationType']
  ): string {
    if (type === 'long_term_partnership') {
      return '6+ months, ongoing';
    }

    if (type === 'short_term_project') {
      return factors.trustLevel >= 0.6 ? '2-3 months' : '1-2 months';
    }

    if (type === 'one_time_introduction') {
      return 'Single meeting or introduction';
    }

    return 'Not applicable';
  }

  private identifyKeySuccessFactors(
    factors: CollaborationPrediction['factors'],
    strengths: CollaborationPrediction['strengths']
  ): string[] {
    const keyFactors: string[] = [];

    // Top strength factors
    for (const strength of strengths.slice(0, 2)) {
      keyFactors.push(strength.factor);
    }

    // Always important
    keyFactors.push('Clear communication');
    keyFactors.push('Defined goals and milestones');

    // Conditional factors
    if (factors.trustLevel < 0.6) {
      keyFactors.push('Building trust through small wins');
    }

    return keyFactors.slice(0, 5);
  }

  private calculateConfidence(user1Profile: any, user2Profile: any): number {
    let confidence = 0.7; // Base

    // More complete profiles = higher confidence
    const user1Completeness = this.profileCompleteness(user1Profile);
    const user2Completeness = this.profileCompleteness(user2Profile);

    confidence = (confidence + user1Completeness + user2Completeness) / 3;

    return Math.min(1, confidence);
  }

  private profileCompleteness(profile: any): number {
    let score = 0;
    const fields = ['name', 'industry', 'expertise_areas', 'needs', 'offers', 'location'];

    for (const field of fields) {
      if (profile[field] && (Array.isArray(profile[field]) ? profile[field].length > 0 : true)) {
        score += 1 / fields.length;
      }
    }

    return score;
  }

  private predictionToOpportunity(
    prediction: CollaborationPrediction,
    userId: string
  ): CollaborationOpportunity {
    const type: CollaborationOpportunity['type'] =
      prediction.optimalCollaborationType === 'short_term_project' ? 'project' :
      prediction.optimalCollaborationType === 'one_time_introduction' ? 'introduction' :
      prediction.optimalCollaborationType === 'long_term_partnership' ? 'co_creation' :
      'advisory';

    return {
      id: `opp_${userId}_${prediction.user2Id}_${Date.now()}`,
      type,
      participants: [userId, prediction.user2Id],
      successProbability: prediction.overallSuccessProbability,
      potentialValue: prediction.overallSuccessProbability,
      timeframe: prediction.suggestedDuration,
      requirements: prediction.keySuccessFactors,
      benefits: prediction.strengths.map(s => s.description)
    };
  }

  private async identifyTeamStrengths(teamMembers: string[]): Promise<string[]> {
    const profiles = await Promise.all(
      teamMembers.map(id => this.getUserProfile(id))
    );

    const allSkills = new Set<string>();
    profiles.forEach(p => {
      (p.expertise_areas || []).forEach((skill: string) => allSkills.add(skill));
    });

    const strengths = [`Diverse skill set: ${allSkills.size} unique expertise areas`];

    if (teamMembers.length >= 3 && teamMembers.length <= 5) {
      strengths.push('Optimal team size for collaboration');
    }

    return strengths;
  }

  private async identifyTeamRisks(
    teamMembers: string[],
    pairwiseScores: Map<string, Map<string, number>>
  ): Promise<string[]> {
    const risks: string[] = [];

    // Check for low pairwise scores
    let lowScoreCount = 0;
    for (const scores of pairwiseScores.values()) {
      for (const score of scores.values()) {
        if (score < 50) lowScoreCount++;
      }
    }

    if (lowScoreCount > teamMembers.length) {
      risks.push('Multiple low-compatibility pairs detected');
    }

    if (teamMembers.length > 7) {
      risks.push('Large team size may complicate coordination');
    }

    return risks;
  }

  private async recommendTeamRoles(teamMembers: string[]): Promise<Map<string, string>> {
    const roles = new Map<string, string>();
    const profiles = await Promise.all(
      teamMembers.map(id => this.getUserProfile(id))
    );

    // Simplified role assignment based on profile
    profiles.forEach((profile, i) => {
      const memberId = teamMembers[i];
      const expertiseCount = (profile.expertise_areas || []).length;

      if (expertiseCount >= 5) {
        roles.set(memberId, 'Technical Lead');
      } else if (i === 0) {
        roles.set(memberId, 'Project Manager');
      } else {
        roles.set(memberId, 'Team Member');
      }
    });

    return roles;
  }

  private calculateOptimalTeamSize(compatibility: number, currentSize: number): number {
    // Optimal is usually 3-5 people
    if (currentSize >= 3 && currentSize <= 5) {
      return currentSize;
    }

    if (compatibility >= 80) {
      return Math.min(5, currentSize + 1);
    }

    return Math.max(3, currentSize);
  }

  private async getTeamSkills(participants: string[]): Promise<string[]> {
    const profiles = await Promise.all(
      participants.map(id => this.getUserProfile(id))
    );

    const skills = new Set<string>();
    profiles.forEach(p => {
      (p.expertise_areas || []).forEach((skill: string) => skills.add(skill));
    });

    return Array.from(skills);
  }

  private async findIdealTeamAdditions(
    currentTeam: string[],
    missingSkills: string[]
  ): Promise<Array<{ skill: string; candidateIds: string[] }>> {
    const additions: Array<{ skill: string; candidateIds: string[] }> = [];

    for (const skill of missingSkills.slice(0, 3)) {
      const candidates = await this.findBySkill(skill);
      additions.push({
        skill,
        candidateIds: candidates.slice(0, 3)
      });
    }

    return additions;
  }

  /**
   * Database helpers
   */

  private async getUserProfile(userId: string): Promise<any> {
    const client = await this.pool.connect();
    try {
      const result = await client.query(`
        SELECT u.id, u.name, u.industry, up.expertise_areas, up.location, up.needs, up.offers
        FROM users u
        LEFT JOIN user_profiles up ON u.id = up.user_id
        WHERE u.id = $1
      `, [userId]);
      return result.rows[0] || {};
    } finally {
      client.release();
    }
  }

  private async getCandidateCollaborators(userId: string): Promise<string[]> {
    const client = await this.pool.connect();
    try {
      const result = await client.query(`
        SELECT id FROM users
        WHERE id != $1
        LIMIT 50
      `, [userId]);
      return result.rows.map(row => row.id);
    } finally {
      client.release();
    }
  }

  private async findBySkill(skill: string): Promise<string[]> {
    const client = await this.pool.connect();
    try {
      const result = await client.query(`
        SELECT user_id as id
        FROM user_profiles
        WHERE $1 = ANY(expertise_areas)
        LIMIT 10
      `, [skill]);
      return result.rows.map(row => row.id);
    } finally {
      client.release();
    }
  }
}
