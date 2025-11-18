-- Bond.AI Database Schema
-- PostgreSQL 14+

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255) NOT NULL,
  password_hash VARCHAR(255),
  industry VARCHAR(100),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  last_login TIMESTAMP,
  is_active BOOLEAN DEFAULT true,
  verification_token VARCHAR(255),
  verified BOOLEAN DEFAULT false
);

-- User profiles table
CREATE TABLE IF NOT EXISTS user_profiles (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  bio TEXT,
  job_title VARCHAR(255),
  company VARCHAR(255),
  linkedin_url VARCHAR(500),
  twitter_url VARCHAR(500),
  website_url VARCHAR(500),
  location JSONB, -- {city, country, latitude, longitude}
  expertise_areas TEXT[], -- Array of skills
  needs TEXT[], -- What they're looking for
  offers TEXT[], -- What they can offer
  years_experience INTEGER,
  education JSONB[], -- Array of education objects
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(user_id)
);

-- Contacts table (imported contacts)
CREATE TABLE IF NOT EXISTS contacts (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  email VARCHAR(255) NOT NULL,
  name VARCHAR(255),
  company VARCHAR(255),
  job_title VARCHAR(255),
  source VARCHAR(50), -- 'linkedin', 'gmail', 'manual', etc.
  imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  metadata JSONB
);

-- Connections table (relationships between users)
CREATE TABLE IF NOT EXISTS connections (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  contact_id UUID REFERENCES contacts(id) ON DELETE CASCADE,
  strength DECIMAL(3,2) DEFAULT 0.5, -- 0.0 to 1.0
  trust_level DECIMAL(3,2) DEFAULT 0.5, -- 0.0 to 1.0
  last_interaction TIMESTAMP,
  interaction_count INTEGER DEFAULT 0,
  notes TEXT,
  tags TEXT[],
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(user_id, contact_id)
);

-- Messages table (conversations)
CREATE TABLE IF NOT EXISTS messages (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  sender_id UUID REFERENCES users(id) ON DELETE CASCADE,
  recipient_id UUID REFERENCES users(id) ON DELETE CASCADE,
  subject VARCHAR(500),
  body TEXT NOT NULL,
  sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  read_at TIMESTAMP,
  thread_id UUID, -- For conversation threading
  metadata JSONB, -- intent, sentiment, etc.
  is_introduction BOOLEAN DEFAULT false
);

-- Introductions table
CREATE TABLE IF NOT EXISTS introductions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  introducer_id UUID REFERENCES users(id) ON DELETE CASCADE,
  person1_id UUID REFERENCES users(id) ON DELETE CASCADE,
  person2_id UUID REFERENCES users(id) ON DELETE CASCADE,
  message_id UUID REFERENCES messages(id),
  status VARCHAR(50) DEFAULT 'pending', -- pending, accepted, declined, completed
  person1_accepted BOOLEAN,
  person2_accepted BOOLEAN,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  accepted_at TIMESTAMP,
  completed_at TIMESTAMP,
  outcome TEXT,
  metadata JSONB
);

-- Network snapshots table (for temporal analysis)
CREATE TABLE IF NOT EXISTS network_snapshots (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  total_connections INTEGER NOT NULL,
  avg_trust_level DECIMAL(3,2),
  degree_centrality DECIMAL(5,4),
  betweenness_centrality DECIMAL(5,4),
  page_rank DECIMAL(5,4),
  clustering_coefficient DECIMAL(5,4),
  community_count INTEGER,
  network_density DECIMAL(5,4),
  UNIQUE(user_id, timestamp)
);

-- Opportunities table
CREATE TABLE IF NOT EXISTS opportunities (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  type VARCHAR(50) NOT NULL, -- collaboration, introduction, hiring, investment, etc.
  title VARCHAR(255) NOT NULL,
  description TEXT,
  target_user_ids UUID[], -- Array of involved users
  score INTEGER, -- 0-100
  confidence DECIMAL(3,2), -- 0-1
  status VARCHAR(50) DEFAULT 'active', -- active, pursued, completed, dismissed
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  expires_at TIMESTAMP,
  metadata JSONB -- reasoning, next_steps, etc.
);

-- Relationship health history
CREATE TABLE IF NOT EXISTS relationship_health_history (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  target_user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  health_score INTEGER NOT NULL, -- 0-100
  category VARCHAR(50) NOT NULL, -- thriving, healthy, declining, at_risk, dormant
  metrics JSONB NOT NULL, -- trust, engagement, etc.
  risks JSONB, -- Array of risk objects
  opportunities JSONB, -- Array of opportunity objects
  recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Activity log
CREATE TABLE IF NOT EXISTS activity_log (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  activity_type VARCHAR(100) NOT NULL,
  entity_type VARCHAR(50), -- user, message, connection, etc.
  entity_id UUID,
  metadata JSONB,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_industry ON users(industry);
CREATE INDEX IF NOT EXISTS idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_contacts_user_id ON contacts(user_id);
CREATE INDEX IF NOT EXISTS idx_contacts_email ON contacts(email);
CREATE INDEX IF NOT EXISTS idx_connections_user_id ON connections(user_id);
CREATE INDEX IF NOT EXISTS idx_connections_contact_id ON connections(contact_id);
CREATE INDEX IF NOT EXISTS idx_messages_sender_id ON messages(sender_id);
CREATE INDEX IF NOT EXISTS idx_messages_recipient_id ON messages(recipient_id);
CREATE INDEX IF NOT EXISTS idx_messages_thread_id ON messages(thread_id);
CREATE INDEX IF NOT EXISTS idx_introductions_introducer_id ON introductions(introducer_id);
CREATE INDEX IF NOT EXISTS idx_network_snapshots_user_timestamp ON network_snapshots(user_id, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_opportunities_user_id ON opportunities(user_id);
CREATE INDEX IF NOT EXISTS idx_opportunities_status ON opportunities(status);
CREATE INDEX IF NOT EXISTS idx_relationship_health_user_id ON relationship_health_history(user_id);
CREATE INDEX IF NOT EXISTS idx_activity_log_user_id ON activity_log(user_id);
CREATE INDEX IF NOT EXISTS idx_activity_log_created_at ON activity_log(created_at DESC);

-- GIN indexes for array and JSONB columns
CREATE INDEX IF NOT EXISTS idx_user_profiles_expertise_areas ON user_profiles USING GIN(expertise_areas);
CREATE INDEX IF NOT EXISTS idx_user_profiles_needs ON user_profiles USING GIN(needs);
CREATE INDEX IF NOT EXISTS idx_user_profiles_offers ON user_profiles USING GIN(offers);
CREATE INDEX IF NOT EXISTS idx_user_profiles_location ON user_profiles USING GIN(location);

-- Updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply updated_at triggers
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_profiles_updated_at BEFORE UPDATE ON user_profiles
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_connections_updated_at BEFORE UPDATE ON connections
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_opportunities_updated_at BEFORE UPDATE ON opportunities
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- TIER SYSTEM SCHEMA ADDITIONS
-- Professional tier classification and cross-tier validation
-- ============================================================================

-- Professional tier profiles
CREATE TABLE IF NOT EXISTS tier_profiles (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  contact_id UUID REFERENCES contacts(id) ON DELETE CASCADE,
  tier VARCHAR(50) NOT NULL, -- entry, junior, mid_level, senior, executive, c_level, founder_ceo, luminary
  tier_score INTEGER NOT NULL, -- 0-100
  career_years INTEGER,
  seniority_level INTEGER, -- 1-10
  achievement_score INTEGER, -- 0-100
  industry_authority INTEGER, -- 0-100
  organization_level INTEGER, -- 1-10
  
  -- Influence metrics
  network_size INTEGER DEFAULT 0,
  follower_count INTEGER DEFAULT 0,
  publications_count INTEGER DEFAULT 0,
  speaking_engagements INTEGER DEFAULT 0,
  awards_recognitions INTEGER DEFAULT 0,
  media_presence INTEGER DEFAULT 0,
  
  -- Verification
  verified BOOLEAN DEFAULT false,
  verification_sources TEXT[], -- linkedin, company_profile, corporate_email, etc.
  verified_at TIMESTAMP,
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  CONSTRAINT check_tier_score CHECK (tier_score >= 0 AND tier_score <= 100),
  CONSTRAINT check_seniority_level CHECK (seniority_level >= 1 AND seniority_level <= 10),
  CONSTRAINT check_org_level CHECK (organization_level >= 1 AND organization_level <= 10)
);

-- Value propositions
CREATE TABLE IF NOT EXISTS value_propositions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  proposer_id UUID REFERENCES users(id) ON DELETE CASCADE,
  target_id UUID REFERENCES users(id) ON DELETE CASCADE,
  
  category VARCHAR(50) NOT NULL, -- business_opportunity, expertise_exchange, problem_solving, etc.
  description TEXT NOT NULL,
  
  -- Assessment scores (0-100)
  strength INTEGER NOT NULL,
  specificity INTEGER NOT NULL,
  verifiability INTEGER NOT NULL,
  uniqueness INTEGER NOT NULL,
  timeliness INTEGER NOT NULL,
  
  evidence TEXT[], -- Supporting evidence
  needs_addressed TEXT[], -- Which target needs this addresses
  
  validated BOOLEAN DEFAULT false,
  validated_at TIMESTAMP,
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  CONSTRAINT check_strength CHECK (strength >= 0 AND strength <= 100),
  CONSTRAINT check_specificity CHECK (specificity >= 0 AND specificity <= 100)
);

-- Cross-tier access requests
CREATE TABLE IF NOT EXISTS cross_tier_requests (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  requester_id UUID REFERENCES users(id) ON DELETE CASCADE,
  target_id UUID REFERENCES users(id) ON DELETE CASCADE,
  value_proposition_id UUID REFERENCES value_propositions(id),
  
  requester_tier VARCHAR(50) NOT NULL,
  target_tier VARCHAR(50) NOT NULL,
  tier_gap INTEGER NOT NULL,
  
  -- Gatekeeper validation results
  gatekeeper_passed BOOLEAN NOT NULL,
  gatekeeper_score INTEGER NOT NULL, -- 0-100
  required_threshold INTEGER NOT NULL, -- 0-100
  
  -- Individual check scores (0-100)
  vp_strength_score INTEGER,
  specificity_score INTEGER,
  relevance_score INTEGER,
  professionalism_score INTEGER,
  mutual_benefit_score INTEGER,
  verification_score INTEGER,
  
  recommendation TEXT,
  warnings TEXT[],
  
  approved BOOLEAN NOT NULL,
  approval_reason TEXT,
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  CONSTRAINT check_tier_gap CHECK (tier_gap >= 0),
  CONSTRAINT check_gatekeeper_score CHECK (gatekeeper_score >= 0 AND gatekeeper_score <= 100)
);

-- Contextual needs analysis
CREATE TABLE IF NOT EXISTS contextual_needs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  contact_id UUID REFERENCES contacts(id) ON DELETE CASCADE,
  
  need_description TEXT NOT NULL,
  
  -- Contextual dimensions
  urgency VARCHAR(50) NOT NULL, -- critical, high, medium, low
  importance VARCHAR(50) NOT NULL, -- critical, high, medium, low
  complexity VARCHAR(50) NOT NULL, -- highly_complex, complex, moderate, simple
  scope VARCHAR(50) NOT NULL, -- transformational, strategic, operational, tactical
  time_horizon VARCHAR(50) NOT NULL, -- immediate, short_term, medium_term, long_term
  
  -- Resource requirements
  time_commitment TEXT,
  financial_investment TEXT,
  required_expertise TEXT[],
  network_access TEXT[],
  
  -- Analysis results
  success_criteria TEXT[],
  keywords TEXT[],
  related_domains TEXT[],
  preferred_helper_tiers TEXT[], -- Which tiers can best help
  
  -- Semantic embedding for advanced matching
  embedding VECTOR(384), -- For BERT embeddings (requires pgvector extension)
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Enhanced matches with tier awareness
CREATE TABLE IF NOT EXISTS enhanced_matches (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  seeker_id UUID REFERENCES users(id) ON DELETE CASCADE,
  target_id UUID REFERENCES users(id) ON DELETE CASCADE,
  
  -- Tier analysis
  seeker_tier VARCHAR(50) NOT NULL,
  target_tier VARCHAR(50) NOT NULL,
  tier_gap INTEGER NOT NULL,
  appropriate_match BOOLEAN NOT NULL,
  requires_gatekeeper BOOLEAN NOT NULL,
  
  -- Value proposition (if cross-tier)
  value_proposition_id UUID REFERENCES value_propositions(id),
  
  -- Validation scores (0-100)
  seeker_benefit INTEGER NOT NULL,
  target_benefit INTEGER NOT NULL,
  mutuality_score INTEGER NOT NULL,
  balance_ratio DECIMAL(3,2) NOT NULL,
  imbalance_warning BOOLEAN DEFAULT false,
  
  -- Contextual alignment (0-100)
  needs_alignment INTEGER,
  urgency_alignment INTEGER,
  scope_alignment INTEGER,
  resource_alignment INTEGER,
  timing_alignment INTEGER,
  domain_alignment INTEGER,
  overall_alignment INTEGER,
  
  -- Match scores
  compatibility_score DECIMAL(3,2) NOT NULL,
  value_potential DECIMAL(3,2) NOT NULL,
  success_probability DECIMAL(3,2) NOT NULL,
  overall_score DECIMAL(3,2) NOT NULL,
  
  -- Match details
  match_type VARCHAR(50) NOT NULL,
  priority VARCHAR(50) NOT NULL, -- critical, high, medium, low
  status VARCHAR(50) DEFAULT 'new',
  
  seeker_needs_addressed TEXT[],
  target_needs_addressed TEXT[],
  match_reasons JSONB, -- Array of match reason objects
  
  shortest_path_length INTEGER,
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  dismissed_at TIMESTAMP,
  
  CONSTRAINT check_tier_gap_matches CHECK (tier_gap >= 0),
  CONSTRAINT check_mutuality_score CHECK (mutuality_score >= 0 AND mutuality_score <= 100),
  CONSTRAINT check_balance_ratio CHECK (balance_ratio >= 0 AND balance_ratio <= 1)
);

-- Indexes for tier tables
CREATE INDEX IF NOT EXISTS idx_tier_profiles_user_id ON tier_profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_tier_profiles_contact_id ON tier_profiles(contact_id);
CREATE INDEX IF NOT EXISTS idx_tier_profiles_tier ON tier_profiles(tier);
CREATE INDEX IF NOT EXISTS idx_tier_profiles_verified ON tier_profiles(verified);

CREATE INDEX IF NOT EXISTS idx_value_props_proposer_id ON value_propositions(proposer_id);
CREATE INDEX IF NOT EXISTS idx_value_props_target_id ON value_propositions(target_id);
CREATE INDEX IF NOT EXISTS idx_value_props_category ON value_propositions(category);
CREATE INDEX IF NOT EXISTS idx_value_props_validated ON value_propositions(validated);

CREATE INDEX IF NOT EXISTS idx_cross_tier_requester_id ON cross_tier_requests(requester_id);
CREATE INDEX IF NOT EXISTS idx_cross_tier_target_id ON cross_tier_requests(target_id);
CREATE INDEX IF NOT EXISTS idx_cross_tier_approved ON cross_tier_requests(approved);
CREATE INDEX IF NOT EXISTS idx_cross_tier_gatekeeper_passed ON cross_tier_requests(gatekeeper_passed);

CREATE INDEX IF NOT EXISTS idx_contextual_needs_user_id ON contextual_needs(user_id);
CREATE INDEX IF NOT EXISTS idx_contextual_needs_contact_id ON contextual_needs(contact_id);
CREATE INDEX IF NOT EXISTS idx_contextual_needs_urgency ON contextual_needs(urgency);
CREATE INDEX IF NOT EXISTS idx_contextual_needs_importance ON contextual_needs(importance);

CREATE INDEX IF NOT EXISTS idx_enhanced_matches_seeker_id ON enhanced_matches(seeker_id);
CREATE INDEX IF NOT EXISTS idx_enhanced_matches_target_id ON enhanced_matches(target_id);
CREATE INDEX IF NOT EXISTS idx_enhanced_matches_status ON enhanced_matches(status);
CREATE INDEX IF NOT EXISTS idx_enhanced_matches_priority ON enhanced_matches(priority);
CREATE INDEX IF NOT EXISTS idx_enhanced_matches_overall_score ON enhanced_matches(overall_score DESC);
CREATE INDEX IF NOT EXISTS idx_enhanced_matches_tier_gap ON enhanced_matches(tier_gap);

-- GIN indexes for array columns
CREATE INDEX IF NOT EXISTS idx_contextual_needs_keywords ON contextual_needs USING GIN(keywords);
CREATE INDEX IF NOT EXISTS idx_contextual_needs_domains ON contextual_needs USING GIN(related_domains);
CREATE INDEX IF NOT EXISTS idx_enhanced_matches_seeker_needs ON enhanced_matches USING GIN(seeker_needs_addressed);
CREATE INDEX IF NOT EXISTS idx_enhanced_matches_target_needs ON enhanced_matches USING GIN(target_needs_addressed);

-- Apply updated_at triggers
CREATE TRIGGER update_tier_profiles_updated_at BEFORE UPDATE ON tier_profiles
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_value_propositions_updated_at BEFORE UPDATE ON value_propositions
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_contextual_needs_updated_at BEFORE UPDATE ON contextual_needs
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_enhanced_matches_updated_at BEFORE UPDATE ON enhanced_matches
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Comments for documentation
COMMENT ON TABLE tier_profiles IS 'Professional tier classification for users and contacts based on career stage, influence, and achievements';
COMMENT ON TABLE value_propositions IS 'Value propositions from seekers to targets, assessed for strength and relevance';
COMMENT ON TABLE cross_tier_requests IS 'Cross-tier access requests with gatekeeper validation results';
COMMENT ON TABLE contextual_needs IS 'Enhanced needs analysis with contextual understanding of urgency, importance, complexity, and scope';
COMMENT ON TABLE enhanced_matches IS 'Tier-aware matches with bidirectional validation and contextual alignment';

COMMENT ON COLUMN tier_profiles.tier IS 'Professional tier: entry, junior, mid_level, senior, executive, c_level, founder_ceo, luminary';
COMMENT ON COLUMN contextual_needs.embedding IS 'BERT semantic embedding vector (384 dimensions) for advanced semantic matching';
COMMENT ON COLUMN enhanced_matches.mutuality_score IS 'Minimum of seeker_benefit and target_benefit - both must benefit';
COMMENT ON COLUMN enhanced_matches.balance_ratio IS 'Ratio of min to max benefit - should be close to 1.0 for balanced exchange';
