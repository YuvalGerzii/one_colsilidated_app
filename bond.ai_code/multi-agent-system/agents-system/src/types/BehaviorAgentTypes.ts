/**
 * Behavior Analysis Agent Types
 *
 * Agents that analyze and emulate the behavior patterns, thinking, and strategies
 * of world-class business leaders to guide decision-making.
 */

import { Pool } from 'pg';
import Redis from 'ioredis';

/**
 * Business sectors and domains
 */
export enum BusinessSector {
  TECHNOLOGY = 'technology',
  FINANCE = 'finance',
  REAL_ESTATE = 'real_estate',
  E_COMMERCE = 'e_commerce',
  SOCIAL_MEDIA = 'social_media',
  AUTOMOTIVE = 'automotive',
  AEROSPACE = 'aerospace',
  ENERGY = 'energy',
  RETAIL = 'retail',
  GENERAL = 'general'
}

/**
 * Decision-making contexts
 */
export enum DecisionContext {
  STRATEGIC_PLANNING = 'strategic_planning',
  PRODUCT_DEVELOPMENT = 'product_development',
  NEGOTIATION = 'negotiation',
  INVESTMENT = 'investment',
  CRISIS_MANAGEMENT = 'crisis_management',
  INNOVATION = 'innovation',
  MARKET_EXPANSION = 'market_expansion',
  HIRING = 'hiring',
  PARTNERSHIP = 'partnership',
  PRICING = 'pricing',
  MARKETING = 'marketing',
  OPERATIONS = 'operations'
}

/**
 * Leadership styles
 */
export enum LeadershipStyle {
  TRANSFORMATIONAL = 'transformational',
  AUTOCRATIC = 'autocratic',
  VISIONARY = 'visionary',
  DEMOCRATIC = 'democratic',
  SITUATIONAL = 'situational',
  SERVANT = 'servant',
  TRANSACTIONAL = 'transactional'
}

/**
 * Core behavioral traits
 */
export interface BehavioralTraits {
  riskTolerance: number; // 0-1 scale
  innovationDrive: number; // 0-1 scale
  analyticalThinking: number; // 0-1 scale
  intuitionReliance: number; // 0-1 scale
  speedOfDecision: number; // 0-1 scale (0=slow, 1=very fast)
  detailOrientation: number; // 0-1 scale
  peopleOrientation: number; // 0-1 scale
  dataOrientation: number; // 0-1 scale
  longTermFocus: number; // 0-1 scale (0=short-term, 1=long-term)
  adaptability: number; // 0-1 scale
}

/**
 * Decision-making pattern
 */
export interface DecisionPattern {
  name: string;
  description: string;
  context: DecisionContext[];
  approach: string;
  keyQuestions: string[];
  considerations: string[];
  redFlags: string[];
  successIndicators: string[];
  examples: string[];
}

/**
 * Negotiation tactics
 */
export interface NegotiationTactic {
  name: string;
  description: string;
  whenToUse: string;
  howToApply: string;
  risks: string[];
  effectiveness: number; // 0-1
  examples: string[];
}

/**
 * Strategic framework
 */
export interface StrategicFramework {
  name: string;
  description: string;
  principles: string[];
  applicationSteps: string[];
  keyMetrics: string[];
  timeHorizon: 'short' | 'medium' | 'long';
  successCriteria: string[];
}

/**
 * Innovation approach
 */
export interface InnovationApproach {
  methodology: string;
  description: string;
  keyPrinciples: string[];
  ideationProcess: string[];
  evaluationCriteria: string[];
  implementationStrategy: string[];
  examples: string[];
}

/**
 * Leadership principle
 */
export interface LeadershipPrinciple {
  principle: string;
  description: string;
  application: string;
  examples: string[];
  quotes?: string[];
}

/**
 * Business advice response
 */
export interface BusinessAdvice {
  question: string;
  context: DecisionContext;
  leaderName: string;
  advice: string;
  reasoning: string;
  alternativeApproaches: string[];
  potentialRisks: string[];
  successProbability: number; // 0-1
  keyQuotes?: string[];
  historicalExamples: string[];
  actionableSteps: string[];
  timeframe: string;
  resourcesNeeded: string[];
  kpis: string[];
}

/**
 * Board room consensus
 */
export interface BoardRoomConsensus {
  question: string;
  context: DecisionContext;
  sector: BusinessSector;
  individualAdvice: Map<string, BusinessAdvice>;
  consensusRecommendation: string;
  majorityOpinion: string;
  minorityOpinions: string[];
  riskAssessment: {
    level: 'low' | 'medium' | 'high' | 'very_high';
    factors: string[];
  };
  confidenceScore: number; // 0-1
  implementationPlan: {
    phases: Array<{
      phase: string;
      duration: string;
      actions: string[];
      milestones: string[];
    }>;
    totalTimeline: string;
    budget?: string;
    team?: string[];
  };
  dissent?: Array<{
    leader: string;
    concern: string;
    alternativeView: string;
  }>;
}

/**
 * Behavior profile for a business leader
 */
export interface LeaderBehaviorProfile {
  name: string;
  title: string;
  companies: string[];
  sectors: BusinessSector[];
  yearsOfExperience: number;

  // Core characteristics
  leadershipStyles: LeadershipStyle[];
  behavioralTraits: BehavioralTraits;

  // Patterns and approaches
  decisionPatterns: DecisionPattern[];
  negotiationTactics: NegotiationTactic[];
  strategicFrameworks: StrategicFramework[];
  innovationApproaches: InnovationApproach[];
  leadershipPrinciples: LeadershipPrinciple[];

  // Communication style
  communicationStyle: {
    directness: number; // 0-1
    formality: number; // 0-1
    emotionalExpression: number; // 0-1
    typicalPhrases: string[];
    communicationChannels: string[];
  };

  // Work standards
  workStandards: {
    expectationsOfTeam: string[];
    workEthic: string;
    meetingCulture: string;
    decisionMakingSpeed: string;
    failureTolerance: number; // 0-1
  };

  // Notable quotes and mantras
  famousQuotes: string[];
  mantras: string[];

  // Historical decisions and outcomes
  notableDecisions: Array<{
    decision: string;
    context: string;
    outcome: string;
    lessonLearned: string;
  }>;
}

/**
 * Base interface for behavior agents
 */
export interface IBehaviorAgent {
  profile: LeaderBehaviorProfile;

  /**
   * Get advice on a business decision
   */
  getAdvice(
    question: string,
    context: DecisionContext,
    additionalInfo?: Record<string, any>
  ): Promise<BusinessAdvice>;

  /**
   * Analyze a decision through this leader's lens
   */
  analyzeDecision(
    decision: string,
    context: DecisionContext,
    outcomes?: string[]
  ): Promise<{
    wouldSupport: boolean;
    reasoning: string;
    modifications: string[];
    confidence: number;
  }>;

  /**
   * Get strategic guidance
   */
  getStrategicGuidance(
    situation: string,
    goals: string[],
    constraints: string[]
  ): Promise<{
    strategy: string;
    rationale: string;
    steps: string[];
    timeline: string;
    risks: string[];
  }>;

  /**
   * Evaluate an opportunity
   */
  evaluateOpportunity(
    opportunity: string,
    context: Record<string, any>
  ): Promise<{
    recommendation: 'pursue' | 'pass' | 'modify';
    score: number; // 0-1
    reasoning: string;
    conditions?: string[];
    modifications?: string[];
  }>;
}

/**
 * Board room configuration
 */
export interface BoardRoomConfig {
  name: string;
  focus: BusinessSector[];
  members: IBehaviorAgent[];
  consensusThreshold: number; // 0-1, percentage needed for consensus
  votingWeights?: Map<string, number>; // Optional weighted voting
  decisionMakingStyle: 'unanimous' | 'majority' | 'weighted' | 'advisory';
}
