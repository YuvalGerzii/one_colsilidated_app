-- Add Matching Preferences for Advanced Algorithm
-- These fields help the matching algorithm make better connections

ALTER TABLE user_registration_data
-- Urgency and Timeline
ADD COLUMN IF NOT EXISTS urgency VARCHAR(20),
ADD COLUMN IF NOT EXISTS timeline VARCHAR(20),
ADD COLUMN IF NOT EXISTS relationship_type VARCHAR(20),

-- Communication and Working Style
ADD COLUMN IF NOT EXISTS communication_style TEXT[],
ADD COLUMN IF NOT EXISTS working_style TEXT[],

-- Geographic and Industry Preferences
ADD COLUMN IF NOT EXISTS geographic_preference VARCHAR(30),
ADD COLUMN IF NOT EXISTS preferred_industries TEXT[],

-- Budget and Deal Breakers
ADD COLUMN IF NOT EXISTS budget_range VARCHAR(50),
ADD COLUMN IF NOT EXISTS deal_breakers TEXT,

-- Success and Challenges
ADD COLUMN IF NOT EXISTS success_criteria TEXT,
ADD COLUMN IF NOT EXISTS specific_challenges TEXT,
ADD COLUMN IF NOT EXISTS past_collaboration_experience TEXT;

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_user_registration_urgency ON user_registration_data(urgency);
CREATE INDEX IF NOT EXISTS idx_user_registration_timeline ON user_registration_data(timeline);
CREATE INDEX IF NOT EXISTS idx_user_registration_relationship_type ON user_registration_data(relationship_type);
CREATE INDEX IF NOT EXISTS idx_user_registration_geographic_pref ON user_registration_data(geographic_preference);
CREATE INDEX IF NOT EXISTS idx_user_registration_communication_style ON user_registration_data USING gin(communication_style);
CREATE INDEX IF NOT EXISTS idx_user_registration_working_style ON user_registration_data USING gin(working_style);
CREATE INDEX IF NOT EXISTS idx_user_registration_preferred_industries ON user_registration_data USING gin(preferred_industries);

-- Add comments for documentation
COMMENT ON COLUMN user_registration_data.urgency IS 'How urgent is the user''s need (immediate, high, medium, low)';
COMMENT ON COLUMN user_registration_data.timeline IS 'Expected duration of engagement (1-week, 1-month, 3-months, 6-months, ongoing)';
COMMENT ON COLUMN user_registration_data.relationship_type IS 'Type of relationship sought (one-time, short-term, long-term, ongoing)';
COMMENT ON COLUMN user_registration_data.communication_style IS 'Preferred communication methods (email, video, phone, etc.)';
COMMENT ON COLUMN user_registration_data.working_style IS 'User''s working style preferences (structured, flexible, collaborative, etc.)';
COMMENT ON COLUMN user_registration_data.geographic_preference IS 'Geographic preference for connections (local, regional, national, global, remote-first)';
COMMENT ON COLUMN user_registration_data.preferred_industries IS 'Specific industries the user wants to connect with';
COMMENT ON COLUMN user_registration_data.budget_range IS 'Budget or investment willingness';
COMMENT ON COLUMN user_registration_data.deal_breakers IS 'Absolute requirements or non-negotiables';
COMMENT ON COLUMN user_registration_data.success_criteria IS 'What success looks like for this connection';
COMMENT ON COLUMN user_registration_data.specific_challenges IS 'Specific problems the user is trying to solve';
COMMENT ON COLUMN user_registration_data.past_collaboration_experience IS 'Past collaboration experiences and learnings';
