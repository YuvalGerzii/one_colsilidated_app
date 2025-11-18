# Bond.AI Tier-Based Matching System 🎯

## Overview

This document describes the comprehensive tier-based matching system implemented in Bond.AI. The system prevents inappropriate cross-tier connections (e.g., junior developers spamming CEOs) while allowing exceptional value propositions to break through.

## Table of Contents

1. [Professional Tier System](#professional-tier-system)
2. [New Agents](#new-agents)
3. [Tier-Aware Matching Engine](#tier-aware-matching-engine)
4. [Gatekeeper System](#gatekeeper-system)
5. [Enhanced Features](#enhanced-features)
6. [Database Schema](#database-schema)
7. [Usage Examples](#usage-examples)
8. [Configuration](#configuration)

---

## Professional Tier System

### Tier Levels

The system classifies professionals into 8 tiers:

| Tier | Description | Typical Roles | Experience |
|------|-------------|---------------|------------|
| **ENTRY** | Students, interns, junior employees | Intern, Trainee | 0-2 years |
| **JUNIOR** | Early career professionals | Junior Developer, Associate | 2-5 years |
| **MID_LEVEL** | Experienced professionals | Developer, Engineer, Specialist | 5-10 years |
| **SENIOR** | Senior professionals, team leads | Senior Engineer, Team Lead | 10-15 years |
| **EXECUTIVE** | Directors, VPs | Director, VP | 15+ years |
| **C_LEVEL** | C-suite executives | CTO, CFO, COO, CMO | 15+ years |
| **FOUNDER_CEO** | Founders, CEOs | Founder, CEO, President | Varies |
| **LUMINARY** | Industry leaders, famous experts | Thought Leaders, Industry Icons | Varies |

### Tier Classification Factors

Each tier is determined by a composite score (0-100) based on:

1. **Career Years** (15% weight)
   - Extracted from bio or inferred from title
   - Normalized to 0-100 scale

2. **Seniority Level** (25% weight)
   - 1-10 scale based on job title
   - Keywords: intern, junior, senior, lead, director, VP, C-level

3. **Influence Metrics** (20% weight)
   - Network size
   - Follower count
   - Publications count
   - Speaking engagements
   - Awards & recognitions
   - Media presence

4. **Achievement Score** (20% weight)
   - Company prestige
   - Education (MBA, PhD, etc.)
   - Patents, publications
   - Leadership experience
   - Quantifiable accomplishments

5. **Industry Authority** (10% weight)
   - Thought leadership indicators
   - Public presence
   - Industry recognition

6. **Organization Level** (10% weight)
   - Position in organizational hierarchy
   - 1-10 scale from intern to CEO

### Tier Verification

Tiers are verified using multiple sources:

- ✅ **LinkedIn Profile** - Most reliable
- ✅ **Corporate Email** - Domain verification
- ✅ **Company Website** - Public profile
- ✅ **GitHub** - For technical roles
- ✅ **Social Media** - Additional validation

---

## New Agents

### 1. TierClassificationAgent

**Purpose**: Automatically classifies contacts into professional tiers

**Key Methods**:
```typescript
async classifyTier(contact: Contact): Promise<TierProfile>
getTierGap(tier1: ProfessionalTier, tier2: ProfessionalTier): number
isAppropriateDirectContact(seekerTier, targetTier, maxGap): boolean
```

**Features**:
- Analyzes career years from bio/title
- Calculates seniority from job title
- Extracts influence metrics from profile
- Verifies tier using multiple sources
- Returns comprehensive TierProfile

**Location**: `src/agents/TierClassificationAgent.ts`

---

### 2. ValuePropositionAgent

**Purpose**: Assesses the strength and quality of value propositions for cross-tier connections

**Key Dimensions** (0-100 scores):

- **Strength**: Overall value proposition quality
- **Specificity**: How concrete and detailed
- **Verifiability**: How verifiable the claims are
- **Uniqueness**: How unique/differentiated
- **Timeliness**: How timely/urgent

**Categories**:
- `BUSINESS_OPPORTUNITY` - Partnership, investment, sales
- `EXPERTISE_EXCHANGE` - Knowledge sharing, mentorship
- `PROBLEM_SOLVING` - Specific problem they can solve
- `INTRODUCTION` - Valuable introduction they can make
- `RESOURCE_ACCESS` - Access to resources, tools, network
- `CAREER_OPPORTUNITY` - Job, project, collaboration
- `INNOVATION` - Novel idea, technology, approach
- `MARKET_ACCESS` - Access to new markets/customers

**Example**:
```typescript
const valueProposition = await valuePropositionAgent.assessValueProposition(
  seeker,       // Junior developer
  target,       // CEO
  ProfessionalTier.JUNIOR,
  ProfessionalTier.FOUNDER_CEO,
  "I've built an AI system that can reduce your customer churn by 30%"
);

// Result:
// strength: 85/100 (specific, quantified, relevant)
// specificity: 90/100 (concrete numbers, clear benefit)
// verifiability: 70/100 (needs proof, but plausible)
// category: BUSINESS_OPPORTUNITY
```

**Location**: `src/agents/ValuePropositionAgent.ts`

---

### 3. GatekeeperAgent

**Purpose**: Validates cross-tier access requests and prevents spam

**Validation Checks** (0-100 scores):

1. **Value Proposition Strength** - Must be exceptional for large gaps
2. **Specificity** - Vague requests rejected
3. **Relevance** - How relevant to target's needs
4. **Professionalism** - Quality of approach
5. **Mutual Benefit** - Both parties benefit (not one-sided)
6. **Verification** - Evidence strength

**Required Thresholds by Tier Gap**:

| Tier Gap | Required Score | Example |
|----------|----------------|---------|
| 0 (same tier) | 40 | Mid-level → Mid-level |
| 1 tier | 55 | Mid-level → Senior |
| 2 tiers | 65 | Junior → Senior |
| 3 tiers | 75 | Junior → Executive |
| 4 tiers | 82 | Junior → C-Level |
| 5+ tiers | 88+ | Entry → CEO |

**Special Rules**:
- ⚠️ Extra strict for **Luminary** targets (min 90)
- ⚠️ Extra strict for **C-Level/Founder** (min 80)
- ✅ More lenient if requester is Senior+ (-5 points)

**Rejection Examples**:

```typescript
// ❌ REJECTED: Vague, one-sided
Gatekeeper Score: 45/88 (Entry → Founder_CEO)
"I'm a CS student looking for mentorship and career advice"
Issues: Low specificity (30), low mutual benefit (25), no value to target

// ✅ APPROVED: Strong value, specific, mutual benefit
Gatekeeper Score: 92/88 (Entry → Founder_CEO)
"I've identified a critical security vulnerability in your authentication system
that could expose 50K user accounts. I have a detailed report and proposed fix."
```

**Location**: `src/agents/GatekeeperAgent.ts`

---

### 4. ContextualNeedsAgent

**Purpose**: Deep analysis of needs with full context understanding

**Analyzes 6 Dimensions**:

1. **Urgency**: CRITICAL | HIGH | MEDIUM | LOW
   - Extracted from: "urgent", "asap", "deadline", etc.

2. **Importance**: CRITICAL | HIGH | MEDIUM | LOW
   - Extracted from: "mission-critical", "survival", "strategic"

3. **Complexity**: HIGHLY_COMPLEX | COMPLEX | MODERATE | SIMPLE
   - Based on technical depth, multi-dimensionality

4. **Scope**: TRANSFORMATIONAL | STRATEGIC | OPERATIONAL | TACTICAL
   - Company-wide vs. single task

5. **Time Horizon**: IMMEDIATE | SHORT_TERM | MEDIUM_TERM | LONG_TERM
   - < 1 week to 3+ months

6. **Resource Requirements**:
   - Time commitment
   - Financial investment
   - Expertise needed
   - Network access

**Preferred Helper Tier Calculation**:

```typescript
// Example: Highly complex, transformational, critical importance
preferredHelperTier: [
  ProfessionalTier.EXECUTIVE,
  ProfessionalTier.C_LEVEL,
  ProfessionalTier.FOUNDER_CEO
]

// Example: Simple, tactical, low importance
preferredHelperTier: [
  ProfessionalTier.MID_LEVEL,
  ProfessionalTier.SENIOR
]
```

**Location**: `src/agents/ContextualNeedsAgent.ts`

---

### 5. EnhancedBidirectionalValidationAgent

**Purpose**: Ensures **BOTH** parties genuinely benefit from the connection

**Validation Scores** (0-100):

- **Seeker Benefit**: How much the seeker benefits
- **Target Benefit**: How much the target benefits
- **Mutuality Score**: `min(seekerBenefit, targetBenefit)` - Both must benefit
- **Balance Ratio**: `min/max` - Should be close to 1.0

**Imbalance Warning**: Triggered if `balanceRatio < 0.6` (>40% difference)

**Benefit Calculation** (4 factors):

1. **Needs Satisfaction** (40%) - How well helper satisfies needs
2. **Value Exchange** (30%) - What can beneficiary offer in return
3. **Network Value** (15%) - Value of adding to network
4. **Expertise Value** (15%) - Knowledge/skills gained

**Example Results**:

```typescript
// ✅ GOOD: Balanced mutual benefit
{
  seekerBenefit: 78,
  targetBenefit: 72,
  mutualityScore: 72,
  balanceRatio: 0.92,
  imbalanceWarning: false
}

// ⚠️ WARNING: One-sided
{
  seekerBenefit: 85,
  targetBenefit: 42,
  mutualityScore: 42,
  balanceRatio: 0.49,
  imbalanceWarning: true  // Seeker benefits 2x more
}
```

**Location**: `src/agents/EnhancedBidirectionalValidationAgent.ts`

---

## Tier-Aware Matching Engine

### Architecture

The `TierAwareMatchingEngine` orchestrates all agents for intelligent matching:

```
                    ┌─────────────────────────────────┐
                    │  TierAwareMatchingEngine        │
                    └─────────────────────────────────┘
                                  │
         ┌────────────────────────┼────────────────────────┐
         │                        │                        │
    ┌────▼────┐          ┌────────▼─────────┐      ┌──────▼──────┐
    │  Tier   │          │  Value           │      │  Gatekeeper │
    │Classify │          │  Proposition     │      │   Agent     │
    └────┬────┘          └────────┬─────────┘      └──────┬──────┘
         │                        │                        │
         └────────────────────────┼────────────────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │  Contextual Needs Agent   │
                    └─────────────┬─────────────┘
                                  │
              ┌───────────────────▼───────────────────┐
              │  Bidirectional Validation Agent       │
              └───────────────────┬───────────────────┘
                                  │
                         ┌────────▼────────┐
                         │  Enhanced Match │
                         └─────────────────┘
```

### Matching Flow

1. **Tier Classification**
   ```typescript
   seekerTierProfile = await tierClassifier.classifyTier(seeker);
   candidateTierProfile = await tierClassifier.classifyTier(candidate);
   tierGap = tierClassifier.getTierGap(seekerTier, candidateTier);
   ```

2. **Tier Filtering**
   ```typescript
   appropriateMatch = tierClassifier.isAppropriateDirectContact(
     seekerTier,
     candidateTier,
     maxTierGapWithoutValidation // e.g., 2
   );
   ```

3. **Value Proposition Assessment** (if inappropriate tier gap)
   ```typescript
   valueProposition = await valuePropositionAgent.assessValueProposition(
     seeker, candidate, seekerTier, candidateTier
   );
   ```

4. **Gatekeeper Validation** (if required)
   ```typescript
   gatekeeperValidation = await gatekeeperAgent.validateAccess(
     seeker, candidate, seekerTier, candidateTier, valueProposition, tierGap
   );

   if (!gatekeeperValidation.passed) {
     // REJECT match
     continue;
   }
   ```

5. **Contextual Needs Analysis**
   ```typescript
   seekerContextualNeeds = await contextualNeedsAgent.analyzeAllNeeds(seeker);
   candidateContextualNeeds = await contextualNeedsAgent.analyzeAllNeeds(candidate);
   ```

6. **Bidirectional Validation**
   ```typescript
   bidirectionalValidation = await bidirectionalValidator.validateWithContextualNeeds(
     seeker, candidate, seekerContextualNeeds, candidateContextualNeeds
   );

   if (bidirectionalValidation.mutualityScore < 60) {
     // REJECT - insufficient mutual benefit
     continue;
   }
   ```

7. **Contextual Alignment**
   ```typescript
   contextualAlignment = calculateContextualAlignment(
     seekerContextualNeeds,
     candidateContextualNeeds
   );
   ```

8. **Final Score Calculation**
   ```typescript
   overallScore =
     mutualNeedsScore * 0.45 +           // 45%
     valueExchangeScore * 0.25 +         // 25%
     balanceRatio * 100 * 0.15 +         // 15%
     contextualAlignment * 0.10 +        // 10%
     networkScore * 0.05;                // 5%
   ```

9. **Quality Filtering**
   ```typescript
   if (overallScore < minOverallScore) {
     // REJECT - quality too low
     continue;
   }
   ```

### Enhanced Match Output

```typescript
interface EnhancedMatch {
  // Standard match fields
  targetContact: Contact;
  sourceContact: Contact;
  overallScore: number;

  // NEW: Tier analysis
  tierAnalysis: {
    seekerTier: ProfessionalTier;
    targetTier: ProfessionalTier;
    tierGap: number;
    appropriateMatch: boolean;
    requiresGatekeeper: boolean;
  };

  // NEW: Value proposition (if cross-tier)
  valueProposition?: ValueProposition;

  // NEW: Gatekeeper results (if applicable)
  gatekeeperValidation?: GatekeeperValidation;

  // NEW: Bidirectional validation
  bidirectionalValidation: {
    seekerBenefit: number;
    targetBenefit: number;
    mutualityScore: number;
    balanceRatio: number;
    imbalanceWarning: boolean;
    seekerNeeds: string[];
    targetNeeds: string[];
  };

  // NEW: Contextual alignment
  contextualAlignment: {
    needsAlignment: number;
    urgencyAlignment: number;
    scopeAlignment: number;
    resourceAlignment: number;
    timingAlignment: number;
    domainAlignment: number;
    overallAlignment: number;
  };
}
```

**Location**: `src/matching/TierAwareMatchingEngine.ts`

---

## Gatekeeper System

### How It Works

The gatekeeper system prevents inappropriate cross-tier spam while allowing exceptional value to break through.

### Decision Matrix

```
┌─────────────┬──────────────────────────────────────────────────────┐
│ Tier Gap    │ Gatekeeper Decision Logic                            │
├─────────────┼──────────────────────────────────────────────────────┤
│ 0-1 tiers   │ ✅ ALLOW - Peers or close colleagues                 │
│ 2 tiers     │ ⚖️ MODERATE - Check value proposition (score ≥ 65)  │
│ 3 tiers     │ ⚠️ STRICT - Requires good value (score ≥ 75)        │
│ 4 tiers     │ 🚨 VERY STRICT - Exceptional value (score ≥ 82)     │
│ 5+ tiers    │ 🔒 EXTREMELY STRICT - Outstanding value (score ≥ 88)│
└─────────────┴──────────────────────────────────────────────────────┘
```

### Real-World Examples

#### ✅ **APPROVED**: Entry → Founder_CEO (Score: 92/88)

**Requester**: CS Student at State University
**Target**: CEO of Fortune 500 Tech Company
**Tier Gap**: 7 levels

**Value Proposition**:
```
"I discovered a critical zero-day vulnerability in your mobile app's
payment processing system affecting 10M+ users. I have a detailed
security audit, proof-of-concept exploit, and proposed patches.
This could prevent a potential $50M+ breach."
```

**Gatekeeper Analysis**:
- ✅ VP Strength: 95 (Critical business impact)
- ✅ Specificity: 92 (Quantified, detailed)
- ✅ Relevance: 98 (Addresses critical security need)
- ✅ Professionalism: 85 (Thorough, evidence-based)
- ✅ Mutual Benefit: 70 (Protects company, establishes credibility)
- ✅ Verification: 80 (Can be verified via security team)

**Recommendation**: "STRONGLY APPROVED - This connection has exceptional value and addresses a critical business need."

---

#### ⚠️ **BORDERLINE**: Junior → Executive (Score: 73/75)

**Requester**: Junior Product Manager (3 years exp)
**Target**: VP of Product at SaaS Company
**Tier Gap**: 3 levels

**Value Proposition**:
```
"I've analyzed your product roadmap and identified a $2M revenue
opportunity in the SMB segment. I have market research, competitive
analysis, and a go-to-market strategy based on my previous
experience launching similar products."
```

**Gatekeeper Analysis**:
- ✅ VP Strength: 75 (Good quantified opportunity)
- ⚠️ Specificity: 70 (Solid but could be more detailed)
- ✅ Relevance: 80 (Addresses growth objectives)
- ✅ Professionalism: 72 (Well-structured)
- ⚠️ Mutual Benefit: 65 (Mostly one-way)
- ✅ Verification: 70 (Claims are verifiable)

**Recommendation**: "BORDERLINE - Consider strengthening mutual benefit and specificity. Perhaps offer to collaborate on a pilot project rather than just presenting ideas."

---

#### ❌ **REJECTED**: Entry → C_Level (Score: 48/88)

**Requester**: Recent College Graduate
**Target**: CTO of Tech Startup
**Tier Gap**: 6 levels

**Value Proposition**:
```
"I'm passionate about technology and really want to learn from
experienced leaders like you. I'd love to grab coffee and hear
about your journey and get career advice."
```

**Gatekeeper Analysis**:
- ❌ VP Strength: 30 (No value to target)
- ❌ Specificity: 35 (Extremely vague)
- ❌ Relevance: 25 (No connection to target's needs)
- ⚠️ Professionalism: 60 (Polite but generic)
- ❌ Mutual Benefit: 15 (Purely one-sided)
- ❌ Verification: 40 (No verifiable claims)

**Recommendation**: "REJECTED - This is purely one-sided. A 0-year professional contacting a CTO requires exceptional value. Consider:
1. Building credibility first (projects, experience)
2. Getting a warm introduction through mutual connections
3. Connecting with someone closer to your tier (Senior Engineer, Engineering Manager)
4. Demonstrating specific value you can provide"

**Warnings**:
- ⚠️ Value proposition is weak
- ⚠️ Value proposition is too vague
- ⚠️ Connection appears one-sided
- ⚠️ Large tier gap (6 levels)
- ⚠️ Contacting a senior executive - ensure exceptional value

---

## Enhanced Features

### 1. Advanced NLP & Context Understanding

**Before** (Basic keyword matching):
```typescript
// Simple keyword overlap
needsSatisfaction = calculateKeywordOverlap(seeker.needs, target.offerings);
```

**After** (Contextual semantic matching):
```typescript
// Deep contextual analysis
const contextualNeed = {
  description: "Need to scale our infrastructure",
  urgency: "CRITICAL",
  importance: "CRITICAL",
  complexity: "HIGHLY_COMPLEX",
  scope: "STRATEGIC",
  timeHorizon: "IMMEDIATE",
  preferredHelperTier: [ProfessionalTier.SENIOR, ProfessionalTier.EXECUTIVE],
  resourceRequirements: {
    timeCommitment: "Full-time for 3 months",
    expertise: ["cloud architecture", "kubernetes", "distributed systems"]
  }
};
```

### 2. Bidirectional Verification

**Before** (One-way matching):
```typescript
// Only checked if target can help seeker
score = calculateMatch(seeker, target);
```

**After** (Two-way validation):
```typescript
// BOTH must benefit
bidirectionalValidation = {
  seekerBenefit: 78,    // Target helps seeker
  targetBenefit: 72,    // Seeker helps target
  mutualityScore: 72,   // min(78, 72) - both must win
  balanceRatio: 0.92,   // 72/78 - balanced exchange
  imbalanceWarning: false
};

// Reject if either party doesn't benefit enough
if (seekerBenefit < 60 || targetBenefit < 60) {
  REJECT();
}
```

### 3. Status Bias Prevention

**Before** (Status bonuses):
```typescript
// Old system gave bonuses for status
if (contact.title.includes("CEO")) score += 0.15;  // +15%
if (followers > 10000) score += 0.20;  // +20%
```

**After** (Merit-based with tier awareness):
```typescript
// NO status bonuses in score
// But tier-aware filtering prevents spam
if (tierGap > 2 && !exceptionalValueProposition) {
  REJECT();  // Can't contact CEO without exceptional value
}
```

### 4. Value Proposition Categories

The system recognizes 8 types of value:

1. **Business Opportunity** (Highest weight for cross-tier)
   - Partnership proposals
   - Investment opportunities
   - Revenue-generating ideas

2. **Innovation**
   - Novel technology
   - Patents
   - Breakthrough approaches

3. **Market Access**
   - Customer introductions
   - Distribution channels
   - Network effects

4. **Problem Solving**
   - Specific solutions to known problems
   - Bug fixes
   - Process improvements

5. **Resource Access**
   - Tools, platforms, infrastructure
   - Talent pools
   - Special resources

6. **Career Opportunity**
   - Job offers
   - Project opportunities
   - Collaborations

7. **Introduction**
   - Connecting to valuable contacts
   - Warm introductions

8. **Expertise Exchange**
   - Knowledge sharing
   - Mentorship
   - Learning

---

## Database Schema

### New Tables

#### 1. `tier_profiles`
Stores professional tier classification for all contacts.

```sql
CREATE TABLE tier_profiles (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  tier VARCHAR(50) NOT NULL,  -- entry, junior, ..., luminary
  tier_score INTEGER NOT NULL,  -- 0-100
  career_years INTEGER,
  seniority_level INTEGER,  -- 1-10

  -- Influence metrics
  network_size INTEGER,
  follower_count INTEGER,
  publications_count INTEGER,
  speaking_engagements INTEGER,
  awards_recognitions INTEGER,

  -- Verification
  verified BOOLEAN,
  verification_sources TEXT[]
);
```

#### 2. `value_propositions`
Value propositions assessed for cross-tier requests.

```sql
CREATE TABLE value_propositions (
  id UUID PRIMARY KEY,
  proposer_id UUID REFERENCES users(id),
  target_id UUID REFERENCES users(id),
  category VARCHAR(50),  -- business_opportunity, innovation, etc.
  description TEXT,

  -- Assessment scores (0-100)
  strength INTEGER,
  specificity INTEGER,
  verifiability INTEGER,
  uniqueness INTEGER,
  timeliness INTEGER,

  evidence TEXT[],
  needs_addressed TEXT[],
  validated BOOLEAN
);
```

#### 3. `cross_tier_requests`
Gatekeeper validation results.

```sql
CREATE TABLE cross_tier_requests (
  id UUID PRIMARY KEY,
  requester_id UUID,
  target_id UUID,
  tier_gap INTEGER,

  -- Gatekeeper results
  gatekeeper_passed BOOLEAN,
  gatekeeper_score INTEGER,  -- 0-100
  required_threshold INTEGER,

  -- Individual check scores
  vp_strength_score INTEGER,
  specificity_score INTEGER,
  relevance_score INTEGER,
  professionalism_score INTEGER,
  mutual_benefit_score INTEGER,

  approved BOOLEAN,
  recommendation TEXT,
  warnings TEXT[]
);
```

#### 4. `contextual_needs`
Enhanced needs with deep context.

```sql
CREATE TABLE contextual_needs (
  id UUID PRIMARY KEY,
  user_id UUID,
  need_description TEXT,

  -- Contextual dimensions
  urgency VARCHAR(50),  -- critical, high, medium, low
  importance VARCHAR(50),
  complexity VARCHAR(50),
  scope VARCHAR(50),
  time_horizon VARCHAR(50),

  -- Analysis
  keywords TEXT[],
  related_domains TEXT[],
  preferred_helper_tiers TEXT[],
  embedding VECTOR(384)  -- BERT embeddings
);
```

#### 5. `enhanced_matches`
Tier-aware matches with full validation.

```sql
CREATE TABLE enhanced_matches (
  id UUID PRIMARY KEY,
  seeker_id UUID,
  target_id UUID,

  -- Tier analysis
  seeker_tier VARCHAR(50),
  target_tier VARCHAR(50),
  tier_gap INTEGER,
  appropriate_match BOOLEAN,
  requires_gatekeeper BOOLEAN,

  -- Validation scores
  seeker_benefit INTEGER,  -- 0-100
  target_benefit INTEGER,
  mutuality_score INTEGER,
  balance_ratio DECIMAL(3,2),

  -- Contextual alignment
  needs_alignment INTEGER,
  urgency_alignment INTEGER,
  domain_alignment INTEGER,
  overall_alignment INTEGER,

  -- Match details
  overall_score DECIMAL(3,2),
  priority VARCHAR(50),
  status VARCHAR(50)
);
```

---

## Usage Examples

### Example 1: Basic Tier-Aware Matching

```typescript
import { TierAwareMatchingEngine } from './matching/TierAwareMatchingEngine';

// Initialize engine
const matchingEngine = new TierAwareMatchingEngine(
  networkMapper,
  intelligenceEngine,
  {
    enableTierFiltering: true,
    maxTierGapWithoutValidation: 2,  // Can contact 2 tiers up freely
    minValuePropositionForCrossTier: 70,  // Need 70+ VP score for larger gaps
    requireGatekeeperForExecutivePlus: true,
    minMutualityScore: 60,  // Both parties must benefit ≥60
    minOverallScore: 70  // Minimum overall match quality
  }
);

// Find matches
const seeker = {
  id: '123',
  name: 'Alice (Junior Developer)',
  title: 'Junior Software Engineer',
  company: 'Startup Inc',
  needs: ['mentorship in system design', 'career guidance'],
  offerings: ['frontend development', 'React expertise'],
  // ... other fields
};

const candidates = [...]; // Array of potential matches

const matches = await matchingEngine.findMatches(seeker, candidates, 50);

// Results
matches.forEach(match => {
  console.log(`
    Match: ${match.targetContact.name}
    Overall Score: ${(match.overallScore * 100).toFixed(0)}%
    Tier: ${match.tierAnalysis.seekerTier} → ${match.tierAnalysis.targetTier}
    Tier Gap: ${match.tierAnalysis.tierGap}

    Bidirectional Validation:
      - Seeker Benefit: ${match.bidirectionalValidation.seekerBenefit}/100
      - Target Benefit: ${match.bidirectionalValidation.targetBenefit}/100
      - Mutuality: ${match.bidirectionalValidation.mutualityScore}/100
      - Balance: ${(match.bidirectionalValidation.balanceRatio * 100).toFixed(0)}%

    ${match.tierAnalysis.requiresGatekeeper ?
      `Gatekeeper: ${match.gatekeeperValidation?.passed ? 'APPROVED' : 'REJECTED'}
       Score: ${match.gatekeeperValidation?.score}/${match.gatekeeperValidation?.requiredThreshold}
       ${match.gatekeeperValidation?.recommendation}`
      : 'Gatekeeper: Not required'}

    Reasons:
    ${match.reasons.map(r => `  - ${r.description}`).join('\n')}
  `);
});
```

### Example 2: Cross-Tier Request with Value Proposition

```typescript
// Junior developer wants to contact CEO
const seeker = {
  tier: ProfessionalTier.JUNIOR,
  name: 'Bob',
  title: 'Junior Developer',
  // ...
};

const target = {
  tier: ProfessionalTier.FOUNDER_CEO,
  name: 'Jane Smith',
  title: 'CEO',
  company: 'BigTech Corp',
  needs: ['reduce infrastructure costs', 'improve system reliability'],
  // ...
};

// Assess value proposition
const vp = await valuePropositionAgent.assessValueProposition(
  seeker,
  target,
  ProfessionalTier.JUNIOR,
  ProfessionalTier.FOUNDER_CEO,
  `I've analyzed your cloud infrastructure and identified opportunities to
   reduce costs by $500K/year (30% savings) through optimization of your
   Kubernetes clusters. I have a detailed cost analysis and implementation
   plan based on my experience optimizing similar systems at my current company.`
);

console.log('Value Proposition Assessment:', {
  strength: vp.strength,  // 88/100 - Strong quantified value
  specificity: vp.specificity,  // 85/100 - Concrete numbers and plan
  category: vp.category,  // BUSINESS_OPPORTUNITY
  needsAddressed: vp.needsAddressed,  // ['reduce infrastructure costs']
});

// Gatekeeper validation
const tierGap = 7;  // Junior to CEO
const gatekeeperResult = await gatekeeperAgent.validateAccess(
  seeker,
  target,
  ProfessionalTier.JUNIOR,
  ProfessionalTier.FOUNDER_CEO,
  vp,
  tierGap
);

if (gatekeeperResult.passed) {
  console.log('✅ Gatekeeper APPROVED');
  console.log('Recommendation:', gatekeeperResult.recommendation);
  // Proceed with connection
} else {
  console.log('❌ Gatekeeper REJECTED');
  console.log('Recommendation:', gatekeeperResult.recommendation);
  console.log('Warnings:', gatekeeperResult.warnings);
  // Connection blocked
}
```

### Example 3: Contextual Needs Analysis

```typescript
const contextualNeedsAgent = new ContextualNeedsAgent();

const analysis = await contextualNeedsAgent.analyzeNeed(
  "Need urgent help scaling our database - we're hitting performance limits and expect 10x growth in 2 months",
  contact
);

console.log('Contextual Analysis:', {
  urgency: analysis.urgency,  // CRITICAL
  importance: analysis.importance,  // HIGH
  complexity: analysis.complexity,  // COMPLEX
  scope: analysis.scope,  // OPERATIONAL
  timeHorizon: analysis.timeHorizon,  // SHORT_TERM
  preferredHelperTier: analysis.preferredHelperTier,  // [SENIOR, EXECUTIVE]
  resourceRequirements: {
    timeCommitment: '2-3 months',
    expertise: ['database architecture', 'scaling', 'performance optimization']
  }
});

// This helps match with appropriate tier
// Entry/Junior would be rejected (insufficient expertise)
// Senior/Executive would be preferred (right level for complexity)
```

---

## Configuration

### Tier System Configuration

```typescript
interface TierAwareConfig {
  // Enable/disable tier filtering
  enableTierFiltering: boolean;  // default: true

  // Maximum tier gap without special validation
  // e.g., 2 = can contact up to 2 tiers higher freely
  maxTierGapWithoutValidation: number;  // default: 2

  // Minimum value proposition score for cross-tier
  // 0-100 scale
  minValuePropositionForCrossTier: number;  // default: 70

  // Require gatekeeper for Executive and above
  requireGatekeeperForExecutivePlus: boolean;  // default: true

  // How much tier affects matching score (0-1)
  tierWeightInMatching: number;  // default: 0.15

  // Minimum mutuality score for bidirectional validation
  minMutualityScore: number;  // default: 60

  // Minimum overall match score
  minOverallScore: number;  // default: 70

  // Maximum network distance (degrees of separation)
  maxNetworkDistance: number;  // default: 4
}
```

### Recommended Configurations

#### **Strict Mode** (Protect executives from spam)
```typescript
{
  enableTierFiltering: true,
  maxTierGapWithoutValidation: 1,  // Only 1 tier up
  minValuePropositionForCrossTier: 80,  // High bar
  requireGatekeeperForExecutivePlus: true,
  minMutualityScore: 70,  // Strong mutual benefit required
  minOverallScore: 75  // High quality only
}
```

#### **Moderate Mode** (Balance accessibility and quality)
```typescript
{
  enableTierFiltering: true,
  maxTierGapWithoutValidation: 2,  // 2 tiers up
  minValuePropositionForCrossTier: 70,  // Moderate bar
  requireGatekeeperForExecutivePlus: true,
  minMutualityScore: 60,  // Moderate mutual benefit
  minOverallScore: 70  // Good quality
}
```

#### **Permissive Mode** (Encourage connections, light filtering)
```typescript
{
  enableTierFiltering: true,
  maxTierGapWithoutValidation: 3,  // 3 tiers up
  minValuePropositionForCrossTier: 60,  // Lower bar
  requireGatekeeperForExecutivePlus: true,  // Still protect top tiers
  minMutualityScore: 55,  // More lenient
  minOverallScore: 65  // More matches
}
```

#### **Disabled Mode** (Traditional matching, no tier filtering)
```typescript
{
  enableTierFiltering: false,  // No tier filtering
  maxTierGapWithoutValidation: 999,
  minValuePropositionForCrossTier: 0,
  requireGatekeeperForExecutivePlus: false,
  minMutualityScore: 50,
  minOverallScore: 60
}
```

---

## Performance Considerations

### Tier Classification Caching

Tier classification is expensive. Cache results:

```typescript
// Cache tier profiles for 7 days
const tierCache = new Map<string, { profile: TierProfile, timestamp: number }>();
const CACHE_TTL = 7 * 24 * 60 * 60 * 1000;  // 7 days

async function getCachedTierProfile(contact: Contact): Promise<TierProfile> {
  const cached = tierCache.get(contact.id);
  if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
    return cached.profile;
  }

  const profile = await tierClassifier.classifyTier(contact);
  tierCache.set(contact.id, { profile, timestamp: Date.now() });
  return profile;
}
```

### Batch Processing

Process candidates in parallel:

```typescript
const matches = await Promise.all(
  candidates.map(async candidate => {
    try {
      return await evaluateMatch(seeker, candidate);
    } catch (error) {
      console.error(`Error processing ${candidate.name}:`, error);
      return null;
    }
  })
).then(results => results.filter(r => r !== null));
```

### Database Indexing

Key indexes for performance:

```sql
-- Tier lookups
CREATE INDEX idx_tier_profiles_user_id ON tier_profiles(user_id);
CREATE INDEX idx_tier_profiles_tier ON tier_profiles(tier);

-- Match queries
CREATE INDEX idx_enhanced_matches_seeker_id ON enhanced_matches(seeker_id);
CREATE INDEX idx_enhanced_matches_status ON enhanced_matches(status);
CREATE INDEX idx_enhanced_matches_overall_score ON enhanced_matches(overall_score DESC);

-- Gatekeeper lookups
CREATE INDEX idx_cross_tier_approved ON cross_tier_requests(approved);
CREATE INDEX idx_cross_tier_gatekeeper_passed ON cross_tier_requests(gatekeeper_passed);
```

---

## Future Enhancements

### 1. Machine Learning Tier Classification

Train ML model on verified profiles:

```typescript
// Use historical data to improve tier classification
const tierModel = await trainTierClassifier({
  features: ['title', 'company', 'bio', 'yearsExperience', 'skillCount'],
  labels: verifiedTierProfiles.map(p => p.tier)
});
```

### 2. Dynamic Threshold Adjustment

Adjust gatekeeper thresholds based on success rates:

```typescript
// Lower threshold if too many good matches are being rejected
// Raise threshold if too much spam gets through
const dynamicThreshold = calculateOptimalThreshold({
  acceptanceRate: 0.15,  // Target 15% approval rate
  falsePositiveRate: 0.05  // Max 5% spam
});
```

### 3. Reputation System

Track connection outcomes to build reputation:

```typescript
interface Reputation {
  connectionSuccessRate: number;  // % of connections that led to value
  responseRate: number;  // % of messages that got responses
  valueDelivered: number;  // Avg value rating from connections
  spamReports: number;  // # of spam reports
}

// Adjust gatekeeper threshold based on reputation
if (requester.reputation.connectionSuccessRate > 0.8) {
  requiredThreshold -= 10;  // Lower bar for proven track record
}
```

### 4. Semantic Embeddings

Use BERT embeddings for deeper needs matching:

```typescript
// Generate embeddings for needs and offerings
const needEmbedding = await bertModel.encode(need.description);
const offeringEmbedding = await bertModel.encode(offering.description);

// Calculate semantic similarity
const similarity = cosineSimilarity(needEmbedding, offeringEmbedding);
```

---

## Summary

The Bond.AI tier-based matching system provides:

✅ **Intelligent Tier Classification** - Automatic professional tier detection
✅ **Status Bias Prevention** - Merit-based matching, not title-based
✅ **Gatekeeper Protection** - Prevents executive spam while allowing exceptional value
✅ **Bidirectional Validation** - Ensures both parties benefit
✅ **Contextual Understanding** - Deep analysis of need urgency, importance, complexity
✅ **Value Proposition Assessment** - Quantifies the strength of cross-tier requests
✅ **Advanced NLP** - Semantic matching beyond keyword overlap
✅ **Configurable Strictness** - Adjust filtering based on use case

**Result**: High-quality connections that respect professional hierarchies while rewarding genuine value.

---

## Questions?

For technical questions or support:
- Review the source code in `src/agents/` and `src/matching/`
- Check the database schema in `database/schema.sql`
- Examine test cases for usage examples

For feature requests or bugs:
- Open an issue with detailed description
- Include example scenarios
- Suggest improvements to thresholds or algorithms
