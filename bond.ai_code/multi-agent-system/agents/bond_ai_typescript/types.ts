/**
 * Agent System Type Definitions
 * Multi-agent negotiation framework for Bond.AI
 */

import { Contact, IntelligenceAnalysis, Match } from '../types';

/**
 * Base Agent Interface
 */
export interface Agent {
  id: string;
  type: AgentType;
  name: string;
  specialization?: string;
  capabilities: AgentCapability[];
  config: AgentConfig;
}

/**
 * Agent Types
 */
export enum AgentType {
  USER_REPRESENTATIVE = 'user_representative',
  DOMAIN_MATCHER = 'domain_matcher',
  NEGOTIATOR = 'negotiator',
  EVALUATOR = 'evaluator',
  COORDINATOR = 'coordinator',
  ANALYZER = 'analyzer'
}

/**
 * Agent Capabilities
 */
export enum AgentCapability {
  NEGOTIATE = 'negotiate',
  ANALYZE = 'analyze',
  MATCH = 'match',
  EVALUATE = 'evaluate',
  COORDINATE = 'coordinate',
  LEARN = 'learn',
  RECOMMEND = 'recommend'
}

/**
 * Agent Configuration
 */
export interface AgentConfig {
  negotiationStyle?: NegotiationStyle;
  riskTolerance?: number; // 0-1
  minAcceptableScore?: number; // 0-1
  priorityWeights?: Record<string, number>;
  learningEnabled?: boolean;
}

/**
 * Negotiation Styles
 */
export enum NegotiationStyle {
  COLLABORATIVE = 'collaborative',     // Win-win focused
  COMPETITIVE = 'competitive',         // Win-lose focused
  ACCOMMODATING = 'accommodating',     // Relationship focused
  COMPROMISING = 'compromising',       // Middle-ground focused
  AVOIDING = 'avoiding'                // Conflict avoidant
}

/**
 * User Representative Agent
 * Represents a user in agent-to-agent negotiations
 */
export interface UserRepresentativeAgent extends Agent {
  type: AgentType.USER_REPRESENTATIVE;
  userId: string;
  userContact: Contact;
  userAnalysis: IntelligenceAnalysis;
  userProfile: UserProfile;
  negotiationHistory: NegotiationRecord[];
}

/**
 * User Profile (from registration)
 */
export interface UserProfile {
  needs: UserNeed[];
  offerings: UserOffering[];
  preferences: UserPreferences;
  constraints: UserConstraints;
  goals: UserGoal[];
}

/**
 * User Need
 */
export interface UserNeed {
  id: string;
  category: NeedCategory;
  description: string;
  priority: Priority;
  urgency: Urgency;
  flexibility: number; // 0-1, how flexible on this need
  quantifiable?: {
    metric: string;
    min?: number;
    max?: number;
    target?: number;
  };
}

/**
 * User Offering
 */
export interface UserOffering {
  id: string;
  category: OfferingCategory;
  description: string;
  value: OfferingValue;
  capacity: number; // 0-1, how much can offer
  conditions?: string[];
}

/**
 * Need Categories
 */
export enum NeedCategory {
  FUNDING = 'funding',
  TALENT = 'talent',
  TECHNOLOGY = 'technology',
  MARKET_ACCESS = 'market_access',
  EXPERTISE = 'expertise',
  CUSTOMERS = 'customers',
  PARTNERSHIPS = 'partnerships',
  MENTORSHIP = 'mentorship',
  RESOURCES = 'resources',
  NETWORK = 'network'
}

/**
 * Offering Categories
 */
export enum OfferingCategory {
  CAPITAL = 'capital',
  SKILLS = 'skills',
  TECHNOLOGY = 'technology',
  DISTRIBUTION = 'distribution',
  KNOWLEDGE = 'knowledge',
  CLIENTS = 'clients',
  COLLABORATION = 'collaboration',
  GUIDANCE = 'guidance',
  ASSETS = 'assets',
  CONNECTIONS = 'connections'
}

/**
 * Priority Levels
 */
export enum Priority {
  CRITICAL = 'critical',
  HIGH = 'high',
  MEDIUM = 'medium',
  LOW = 'low'
}

/**
 * Urgency Levels
 */
export enum Urgency {
  IMMEDIATE = 'immediate',     // Within days
  SHORT_TERM = 'short_term',   // Within weeks
  MEDIUM_TERM = 'medium_term', // Within months
  LONG_TERM = 'long_term'      // Beyond months
}

/**
 * Offering Value
 */
export interface OfferingValue {
  type: ValueType;
  estimated?: number;
  range?: { min: number; max: number };
  unit?: string;
}

/**
 * Value Types
 */
export enum ValueType {
  MONETARY = 'monetary',
  TIME = 'time',
  EXPERTISE = 'expertise',
  ACCESS = 'access',
  STRATEGIC = 'strategic'
}

/**
 * User Preferences
 */
export interface UserPreferences {
  preferredIndustries?: string[];
  preferredCompanySizes?: CompanySize[];
  preferredLocations?: string[];
  preferredRelationshipTypes?: string[];
  dealBreakers?: string[];
  mustHaves?: string[];
}

/**
 * Company Sizes
 */
export enum CompanySize {
  SOLO = 'solo',
  STARTUP = 'startup',
  SMALL = 'small',
  MEDIUM = 'medium',
  LARGE = 'large',
  ENTERPRISE = 'enterprise'
}

/**
 * User Constraints
 */
export interface UserConstraints {
  timeAvailability?: number; // hours per week
  budgetConstraints?: { min?: number; max?: number };
  geographicConstraints?: string[];
  legalConstraints?: string[];
  exclusivityRequirements?: string[];
}

/**
 * User Goals
 */
export interface UserGoal {
  id: string;
  description: string;
  timeframe: Urgency;
  successCriteria: string[];
  metrics?: GoalMetric[];
}

/**
 * Goal Metrics
 */
export interface GoalMetric {
  name: string;
  target: number;
  current?: number;
  unit: string;
}

/**
 * Agent-to-Agent Conversation
 */
export interface AgentConversation {
  id: string;
  agent1: UserRepresentativeAgent;
  agent2: UserRepresentativeAgent;
  facilitator?: Agent;
  status: ConversationStatus;
  messages: ConversationMessage[];
  negotiationPoints: NegotiationPoint[];
  proposedTerms: ProposedTerms[];
  finalAgreement?: Agreement;
  startedAt: Date;
  completedAt?: Date;
  metadata?: Record<string, any>;
}

/**
 * Conversation Status
 */
export enum ConversationStatus {
  INITIATED = 'initiated',
  IN_PROGRESS = 'in_progress',
  AGREEMENT_REACHED = 'agreement_reached',
  NO_AGREEMENT = 'no_agreement',
  PAUSED = 'paused',
  CANCELLED = 'cancelled'
}

/**
 * Conversation Message
 */
export interface ConversationMessage {
  id: string;
  from: string; // agent id
  to: string; // agent id
  timestamp: Date;
  messageType: MessageType;
  content: string;
  structuredData?: any;
  sentiment?: number; // -1 to 1
}

/**
 * Message Types
 */
export enum MessageType {
  INTRODUCTION = 'introduction',
  PROPOSAL = 'proposal',
  COUNTER_PROPOSAL = 'counter_proposal',
  QUESTION = 'question',
  ANSWER = 'answer',
  CLARIFICATION = 'clarification',
  ACCEPTANCE = 'acceptance',
  REJECTION = 'rejection',
  NEGOTIATION = 'negotiation',
  AGREEMENT = 'agreement'
}

/**
 * Negotiation Point
 */
export interface NegotiationPoint {
  id: string;
  topic: string;
  agent1Position: Position;
  agent2Position: Position;
  status: NegotiationPointStatus;
  resolution?: Resolution;
}

/**
 * Position
 */
export interface Position {
  statement: string;
  importance: number; // 0-1
  flexibility: number; // 0-1
  justification?: string;
}

/**
 * Negotiation Point Status
 */
export enum NegotiationPointStatus {
  OPEN = 'open',
  UNDER_DISCUSSION = 'under_discussion',
  AGREED = 'agreed',
  DEADLOCKED = 'deadlocked',
  DEFERRED = 'deferred'
}

/**
 * Resolution
 */
export interface Resolution {
  agreed: boolean;
  finalTerms?: string;
  compromise?: string;
  satisfactionScore: { agent1: number; agent2: number };
}

/**
 * Proposed Terms
 */
export interface ProposedTerms {
  id: string;
  proposedBy: string; // agent id
  timestamp: Date;
  terms: MatchTerms;
  rationale: string;
  status: TermsStatus;
  response?: TermsResponse;
}

/**
 * Match Terms
 */
export interface MatchTerms {
  whatAgent1Gives: string[];
  whatAgent1Gets: string[];
  whatAgent2Gives: string[];
  whatAgent2Gets: string[];
  conditions?: string[];
  timeline?: string;
  successMetrics?: string[];
}

/**
 * Terms Status
 */
export enum TermsStatus {
  PROPOSED = 'proposed',
  ACCEPTED = 'accepted',
  REJECTED = 'rejected',
  COUNTER_OFFERED = 'counter_offered',
  WITHDRAWN = 'withdrawn'
}

/**
 * Terms Response
 */
export interface TermsResponse {
  accepted: boolean;
  concerns?: string[];
  counterOffer?: MatchTerms;
  feedback: string;
  timestamp: Date;
}

/**
 * Agreement
 */
export interface Agreement {
  id: string;
  conversationId: string;
  agent1: UserRepresentativeAgent;
  agent2: UserRepresentativeAgent;
  finalTerms: MatchTerms;
  compatibilityScore: number;
  mutualBenefit: MutualBenefit;
  agreedAt: Date;
  nextSteps: string[];
  followUpSchedule?: string;
}

/**
 * Mutual Benefit
 */
export interface MutualBenefit {
  agent1Benefits: Benefit[];
  agent2Benefits: Benefit[];
  overallScore: number;
  balanceScore: number; // How balanced the benefits are
}

/**
 * Benefit
 */
export interface Benefit {
  category: string;
  description: string;
  estimatedValue: number; // 0-1 normalized
  timeToRealize: Urgency;
}

/**
 * Negotiation Record
 */
export interface NegotiationRecord {
  conversationId: string;
  otherAgentId: string;
  outcome: ConversationStatus;
  agreement?: Agreement;
  duration: number; // milliseconds
  messagesExchanged: number;
  learnings: string[];
  timestamp: Date;
}

/**
 * Domain Matcher Agent
 * Specialized agent for specific domains (e.g., investor-startup matching)
 */
export interface DomainMatcherAgent extends Agent {
  type: AgentType.DOMAIN_MATCHER;
  domain: MatchingDomain;
  matchingStrategies: MatchingStrategy[];
  successPatterns: SuccessPattern[];
}

/**
 * Matching Domains
 */
export enum MatchingDomain {
  INVESTOR_STARTUP = 'investor_startup',
  SALES_CLIENT = 'sales_client',
  PARTNERSHIP = 'partnership',
  TALENT_ACQUISITION = 'talent_acquisition',
  MENTOR_MENTEE = 'mentor_mentee',
  SUPPLIER_BUYER = 'supplier_buyer',
  COLLABORATION = 'collaboration'
}

/**
 * Matching Strategy
 */
export interface MatchingStrategy {
  name: string;
  description: string;
  scoringFunction: string; // reference to function
  weights: Record<string, number>;
  threshold: number;
}

/**
 * Success Pattern
 */
export interface SuccessPattern {
  pattern: string;
  successRate: number;
  conditions: string[];
  examples: string[];
}

/**
 * Negotiation Outcome
 */
export interface NegotiationOutcome {
  success: boolean;
  agreement?: Agreement;
  reason?: string;
  improvementSuggestions?: string[];
  metrics: {
    duration: number;
    messagesExchanged: number;
    proposalsConsidered: number;
    compatibilityScore: number;
    satisfactionScore: { agent1: number; agent2: number };
  };
}
