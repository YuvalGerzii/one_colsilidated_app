/**
 * Bond.AI - Connection Intelligence Platform
 * Core Type Definitions
 */

export interface Contact {
  id: string;
  name: string;
  email?: string;
  phone?: string;
  company?: string;
  title?: string;
  industry?: string;
  location?: string;
  bio?: string;
  interests?: string[];
  skills?: string[];
  needs?: string[];
  offerings?: string[];
  socialProfiles?: {
    linkedin?: string;
    twitter?: string;
    github?: string;
    website?: string;
  };
  tierProfile?: TierProfile; // Professional tier information
  contextualNeeds?: ContextualNeedsAnalysis[]; // Enhanced needs with context
  metadata?: Record<string, any>;
}

export interface Connection {
  id: string;
  fromContactId: string;
  toContactId: string;
  relationshipType: RelationshipType;
  strength: number; // 0-1, indicating relationship strength
  lastInteraction?: Date;
  interactionFrequency?: number; // interactions per month
  trustLevel?: number; // 0-1, calculated trust score
  metadata?: Record<string, any>;
}

export enum RelationshipType {
  COLLEAGUE = 'colleague',
  CLIENT = 'client',
  VENDOR = 'vendor',
  PARTNER = 'partner',
  FRIEND = 'friend',
  ACQUAINTANCE = 'acquaintance',
  MENTOR = 'mentor',
  MENTEE = 'mentee',
  OTHER = 'other'
}

export interface NetworkGraph {
  contacts: Map<string, Contact>;
  connections: Map<string, Connection>;
  degreeMap: Map<string, number>; // contactId -> degree of separation from user
}

export interface ConnectionPath {
  contacts: Contact[];
  connections: Connection[];
  totalStrength: number;
  trustScore: number;
}

export interface Match {
  id: string;
  targetContact: Contact;
  sourceContact: Contact; // the user or their connection
  matchType: MatchType;
  compatibilityScore: number; // 0-1
  valuePotential: number; // 0-1
  successProbability: number; // 0-1
  overallScore: number; // weighted combination
  connectionPaths: ConnectionPath[];
  shortestPath: ConnectionPath;
  reasons: MatchReason[];
  priority: Priority;
  timestamp: Date;
  status: MatchStatus;
  metadata?: Record<string, any>;
}

export enum MatchType {
  COMPLEMENTARY_NEEDS = 'complementary_needs',
  SKILL_MATCH = 'skill_match',
  INDUSTRY_SYNERGY = 'industry_synergy',
  MUTUAL_INTEREST = 'mutual_interest',
  BUSINESS_OPPORTUNITY = 'business_opportunity',
  KNOWLEDGE_EXCHANGE = 'knowledge_exchange',
  COLLABORATION = 'collaboration'
}

export interface MatchReason {
  type: string;
  description: string;
  score: number;
  evidence: string[];
}

export enum Priority {
  CRITICAL = 'critical',
  HIGH = 'high',
  MEDIUM = 'medium',
  LOW = 'low'
}

export enum MatchStatus {
  NEW = 'new',
  REVIEWED = 'reviewed',
  INTRODUCTION_REQUESTED = 'introduction_requested',
  INTRODUCTION_MADE = 'introduction_made',
  ENGAGED = 'engaged',
  COMPLETED = 'completed',
  DISMISSED = 'dismissed'
}

export interface Introduction {
  id: string;
  match: Match;
  introducerContact: Contact;
  introduceeContact: Contact;
  targetContact: Contact;
  message: string;
  conversationStarters: string[];
  context: string;
  status: IntroductionStatus;
  createdAt: Date;
  sentAt?: Date;
  respondedAt?: Date;
  metadata?: Record<string, any>;
}

export enum IntroductionStatus {
  DRAFT = 'draft',
  PENDING_APPROVAL = 'pending_approval',
  SENT = 'sent',
  ACCEPTED = 'accepted',
  DECLINED = 'declined',
  COMPLETED = 'completed'
}

export interface NetworkSource {
  type: SourceType;
  credentials?: any;
  config?: any;
}

export enum SourceType {
  LINKEDIN = 'linkedin',
  GMAIL = 'gmail',
  OUTLOOK = 'outlook',
  TWITTER = 'twitter',
  SALESFORCE = 'salesforce',
  CSV = 'csv',
  MANUAL = 'manual'
}

export interface IntelligenceAnalysis {
  contactId: string;
  profileAnalysis: {
    industries: string[];
    expertiseAreas: string[];
    careerStage: string;
    influenceScore: number;
  };
  needsAnalysis: {
    explicit: string[]; // stated needs
    implicit: string[]; // inferred needs
    confidence: number;
  };
  offeringsAnalysis: {
    explicit: string[]; // stated offerings
    implicit: string[]; // inferred capabilities
    confidence: number;
  };
  personalityProfile: {
    traits: Record<string, number>;
    communicationStyle: string;
    decisionMakingStyle: string;
  };
  behavioralInsights: {
    responsiveness: number;
    collaborationStyle: string;
    preferredChannels: string[];
  };
  timestamp: Date;
}

/**
 * Professional Tier System
 * Defines hierarchical levels for status-aware matching
 */
export enum ProfessionalTier {
  ENTRY = 'entry',           // Students, interns, junior employees (0-2 years)
  JUNIOR = 'junior',         // Early career professionals (2-5 years)
  MID_LEVEL = 'mid_level',   // Experienced professionals (5-10 years)
  SENIOR = 'senior',         // Senior professionals, team leads (10-15 years)
  EXECUTIVE = 'executive',   // Directors, VPs (15+ years)
  C_LEVEL = 'c_level',       // C-suite executives (CTO, CFO, COO, etc.)
  FOUNDER_CEO = 'founder_ceo', // Founders, CEOs
  LUMINARY = 'luminary'      // Industry leaders, famous experts, thought leaders
}

export interface TierProfile {
  tier: ProfessionalTier;
  tierScore: number; // 0-100, composite score for tier placement
  careerYears: number;
  seniorityLevel: number; // 1-10 scale
  influenceMetrics: {
    networkSize: number;
    followerCount: number;
    publicationsCount: number;
    speakingEngagements: number;
    awardsRecognitions: number;
    mediaPresence: number;
  };
  achievementScore: number; // 0-100, based on verifiable achievements
  industryAuthority: number; // 0-100, domain expertise recognition
  organizationLevel: number; // 1-10, position in organizational hierarchy
  verified: boolean; // Whether tier has been verified
  verificationSources: string[]; // LinkedIn, company website, press, etc.
}

export interface ValueProposition {
  id: string;
  proposer: string; // Contact ID
  target: string; // Contact ID
  strength: number; // 0-100, how strong is the value proposition
  category: ValuePropositionCategory;
  description: string;
  specificity: number; // 0-100, how specific and concrete
  verifiability: number; // 0-100, how verifiable the claims are
  evidence: string[]; // Supporting evidence
  needsAddressed: string[]; // Which target needs this addresses
  uniqueness: number; // 0-100, how unique/differentiated
  timeliness: number; // 0-100, how timely/urgent
  validated: boolean;
  validationTimestamp?: Date;
}

export enum ValuePropositionCategory {
  BUSINESS_OPPORTUNITY = 'business_opportunity', // Partnership, sales, investment
  EXPERTISE_EXCHANGE = 'expertise_exchange',     // Knowledge sharing, mentorship
  PROBLEM_SOLVING = 'problem_solving',          // Specific problem they can solve
  INTRODUCTION = 'introduction',                // Valuable introduction they can make
  RESOURCE_ACCESS = 'resource_access',          // Access to resources, tools, network
  CAREER_OPPORTUNITY = 'career_opportunity',    // Job, project, collaboration
  INNOVATION = 'innovation',                    // Novel idea, technology, approach
  MARKET_ACCESS = 'market_access'              // Access to new markets/customers
}

export interface CrossTierAccessRequest {
  requester: Contact;
  target: Contact;
  requesterTier: ProfessionalTier;
  targetTier: ProfessionalTier;
  tierGap: number; // Numeric difference in tier levels
  valueProposition: ValueProposition;
  gatekeeperValidation: GatekeeperValidation;
  approved: boolean;
  reason: string;
}

export interface GatekeeperValidation {
  passed: boolean;
  score: number; // 0-100, overall gatekeeper score
  checks: {
    valuePropositionStrength: number; // Must be high for large tier gaps
    specificity: number; // Vague requests rejected
    relevance: number; // How relevant to target's needs
    professionalism: number; // Quality of approach
    mutualBenefit: number; // Both parties benefit
    verification: number; // Evidence strength
  };
  requiredThreshold: number; // Based on tier gap
  recommendation: string;
  warnings: string[];
}

export interface ContextualNeedsAnalysis {
  needId: string;
  needDescription: string;
  urgency: UrgencyLevel;
  importance: ImportanceLevel;
  complexity: ComplexityLevel;
  scope: ScopeLevel;
  timeHorizon: TimeHorizon;
  resourceRequirements: ResourceRequirements;
  successCriteria: string[];
  semanticEmbedding?: number[]; // Vector representation for semantic matching
  keywords: string[];
  relatedDomains: string[];
  preferredHelperTier: ProfessionalTier[]; // What tier(s) can best help
}

export enum UrgencyLevel {
  CRITICAL = 'critical',   // Immediate action needed
  HIGH = 'high',          // Within days
  MEDIUM = 'medium',      // Within weeks
  LOW = 'low'            // Within months
}

export enum ImportanceLevel {
  CRITICAL = 'critical',   // Mission-critical, business survival
  HIGH = 'high',          // Major impact on success
  MEDIUM = 'medium',      // Meaningful but not critical
  LOW = 'low'            // Nice to have
}

export enum ComplexityLevel {
  SIMPLE = 'simple',       // Straightforward, single-dimension
  MODERATE = 'moderate',   // Multiple factors, some expertise needed
  COMPLEX = 'complex',     // Multi-dimensional, requires expertise
  HIGHLY_COMPLEX = 'highly_complex' // Requires deep expertise, multiple specialists
}

export enum ScopeLevel {
  TACTICAL = 'tactical',       // Single task/question
  OPERATIONAL = 'operational', // Department/team level
  STRATEGIC = 'strategic',     // Organization-wide
  TRANSFORMATIONAL = 'transformational' // Industry/ecosystem level
}

export enum TimeHorizon {
  IMMEDIATE = 'immediate',     // < 1 week
  SHORT_TERM = 'short_term',   // 1-4 weeks
  MEDIUM_TERM = 'medium_term', // 1-3 months
  LONG_TERM = 'long_term'     // 3+ months
}

export interface ResourceRequirements {
  timeCommitment: string; // e.g., "30 minutes", "ongoing mentorship"
  financialInvestment?: string;
  expertise: string[];
  networkAccess?: string[];
  otherResources?: string[];
}

export interface EnhancedMatch extends Match {
  tierAnalysis: {
    seekerTier: ProfessionalTier;
    targetTier: ProfessionalTier;
    tierGap: number;
    appropriateMatch: boolean;
    requiresGatekeeper: boolean;
  };
  valueProposition?: ValueProposition;
  gatekeeperValidation?: GatekeeperValidation;
  bidirectionalValidation: BidirectionalValidation;
  contextualAlignment: ContextualAlignment;
}

export interface BidirectionalValidation {
  seekerBenefit: number; // 0-100, how much seeker benefits
  targetBenefit: number; // 0-100, how much target benefits
  mutualityScore: number; // min(seekerBenefit, targetBenefit)
  imbalanceWarning: boolean; // true if one-sided
  seekerNeeds: string[]; // Needs being addressed for seeker
  targetNeeds: string[]; // Needs being addressed for target
  balanceRatio: number; // ratio of benefit (should be close to 1.0)
}

export interface ContextualAlignment {
  needsAlignment: number; // 0-100, how well needs/offerings align
  urgencyAlignment: number; // 0-100, urgency compatibility
  scopeAlignment: number; // 0-100, scope compatibility
  resourceAlignment: number; // 0-100, resource availability match
  timingAlignment: number; // 0-100, timing compatibility
  domainAlignment: number; // 0-100, domain expertise match
  overallAlignment: number; // weighted average
}

export interface BondAIConfig {
  maxDegreeOfSeparation: number;
  minRelationshipStrength: number;
  minCompatibilityScore: number;
  enabledMatchTypes: MatchType[];
  priorityWeights: {
    valuePotential: number;
    successProbability: number;
    trustLevel: number;
    timing: number;
  };
  intelligenceConfig: {
    enableNeedsInference: boolean;
    enablePersonalityAnalysis: boolean;
    enableBehavioralPrediction: boolean;
  };
  tierConfig: {
    enableTierFiltering: boolean;
    maxTierGapWithoutValidation: number; // e.g., 2 = can contact 2 tiers up without special validation
    minValuePropositionForCrossTier: number; // 0-100, minimum VP strength
    requireGatekeeperForExecutivePlus: boolean; // Require validation for Executive+
    tierWeightInMatching: number; // 0-1, how much tier affects matching
  };
}
