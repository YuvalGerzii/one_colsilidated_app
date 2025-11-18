-- Enhanced Registration Migration
-- Add comprehensive user registration fields

-- Add new columns to users table for detailed registration
ALTER TABLE users ADD COLUMN IF NOT EXISTS full_name VARCHAR(255);
ALTER TABLE users ADD COLUMN IF NOT EXISTS phone_number VARCHAR(50);
ALTER TABLE users ADD COLUMN IF NOT EXISTS country VARCHAR(100);
ALTER TABLE users ADD COLUMN IF NOT EXISTS city VARCHAR(100);
ALTER TABLE users ADD COLUMN IF NOT EXISTS timezone VARCHAR(100);
ALTER TABLE users ADD COLUMN IF NOT EXISTS preferred_language VARCHAR(10) DEFAULT 'en';
ALTER TABLE users ADD COLUMN IF NOT EXISTS avatar_url VARCHAR(500);
ALTER TABLE users ADD COLUMN IF NOT EXISTS onboarding_completed BOOLEAN DEFAULT false;
ALTER TABLE users ADD COLUMN IF NOT EXISTS profile_completion_percentage INTEGER DEFAULT 0;

-- Add comprehensive profile fields
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS skills JSONB DEFAULT '[]'::jsonb; -- Array of skill objects with proficiency
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS interests JSONB DEFAULT '[]'::jsonb; -- Professional interests
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS looking_for TEXT[]; -- What they're seeking (mentorship, partnership, etc.)
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS can_help_with TEXT[]; -- What they can offer
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS industry_sectors TEXT[]; -- Industries they work in
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS company_size VARCHAR(50); -- Startup, SMB, Enterprise
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS availability VARCHAR(50); -- How much time they can dedicate
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS communication_style VARCHAR(50); -- Direct, Collaborative, etc.
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS goals JSONB DEFAULT '[]'::jsonb; -- Short-term and long-term goals
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS certifications JSONB DEFAULT '[]'::jsonb; -- Professional certifications
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS languages JSONB DEFAULT '[]'::jsonb; -- Languages spoken with proficiency level
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS preferred_connection_types TEXT[]; -- Types of connections they prefer
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS achievements TEXT[]; -- Notable achievements
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS current_projects JSONB DEFAULT '[]'::jsonb; -- Current projects/initiatives

-- Create detailed registration data table for analytics
CREATE TABLE IF NOT EXISTS user_registration_data (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,

  -- Personal Information
  full_name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  phone_number VARCHAR(50),
  date_of_birth DATE,
  gender VARCHAR(50),

  -- Location
  country VARCHAR(100),
  city VARCHAR(100),
  state_province VARCHAR(100),
  postal_code VARCHAR(20),
  timezone VARCHAR(100),

  -- Professional Information
  current_job_title VARCHAR(255),
  current_company VARCHAR(255),
  industry VARCHAR(100),
  years_of_experience INTEGER,
  company_size VARCHAR(50),
  employment_type VARCHAR(50), -- Full-time, Freelance, Entrepreneur, etc.

  -- Skills and Expertise (JSONB for flexibility)
  technical_skills JSONB DEFAULT '[]'::jsonb, -- [{skill: 'Python', level: 'Expert', years: 5}]
  soft_skills JSONB DEFAULT '[]'::jsonb, -- [{skill: 'Leadership', level: 'Advanced'}]
  domain_expertise TEXT[], -- Areas of expertise

  -- Professional Goals
  looking_for TEXT[], -- What they want (mentorship, co-founder, investors, etc.)
  can_offer TEXT[], -- What they provide (mentorship, skills, connections, etc.)
  professional_goals TEXT,
  time_commitment VARCHAR(50), -- How much time they can dedicate

  -- Preferences
  preferred_communication_styles TEXT[], -- Email, Video, In-person, etc.
  preferred_meeting_times VARCHAR(100),
  willing_to_travel BOOLEAN DEFAULT false,
  remote_preference VARCHAR(50), -- Remote, Hybrid, In-person

  -- Background
  education JSONB DEFAULT '[]'::jsonb, -- [{degree, institution, year, field}]
  certifications JSONB DEFAULT '[]'::jsonb, -- [{name, issuer, year, url}]
  languages JSONB DEFAULT '[]'::jsonb, -- [{language, proficiency}]

  -- Additional Information
  bio TEXT,
  website_url VARCHAR(500),
  linkedin_url VARCHAR(500),
  twitter_url VARCHAR(500),
  github_url VARCHAR(500),
  portfolio_url VARCHAR(500),

  -- Metadata
  registration_source VARCHAR(100), -- Web, Mobile, Referral, etc.
  referral_code VARCHAR(100),
  marketing_consent BOOLEAN DEFAULT false,
  terms_accepted BOOLEAN DEFAULT true,
  privacy_accepted BOOLEAN DEFAULT true,

  -- Timestamps
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  completed_at TIMESTAMP,

  UNIQUE(user_id)
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_user_registration_email ON user_registration_data(email);
CREATE INDEX IF NOT EXISTS idx_user_registration_industry ON user_registration_data(industry);
CREATE INDEX IF NOT EXISTS idx_user_registration_location ON user_registration_data(country, city);
CREATE INDEX IF NOT EXISTS idx_user_registration_looking_for ON user_registration_data USING gin(looking_for);
CREATE INDEX IF NOT EXISTS idx_user_registration_can_offer ON user_registration_data USING gin(can_offer);
CREATE INDEX IF NOT EXISTS idx_user_registration_skills ON user_registration_data USING gin(technical_skills);
CREATE INDEX IF NOT EXISTS idx_user_registration_created ON user_registration_data(created_at);

-- Create trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_user_registration_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER user_registration_updated_at
  BEFORE UPDATE ON user_registration_data
  FOR EACH ROW
  EXECUTE FUNCTION update_user_registration_updated_at();

-- Create view for easy access to complete user profiles
CREATE OR REPLACE VIEW complete_user_profiles AS
SELECT
  u.id as user_id,
  u.email,
  u.full_name,
  u.industry,
  u.created_at as user_created_at,
  u.is_active,
  u.onboarding_completed,
  u.profile_completion_percentage,
  up.bio,
  up.job_title,
  up.company,
  up.skills,
  up.interests,
  up.looking_for,
  up.can_help_with,
  urd.current_job_title,
  urd.years_of_experience,
  urd.technical_skills,
  urd.soft_skills,
  urd.professional_goals,
  urd.linkedin_url,
  urd.portfolio_url
FROM users u
LEFT JOIN user_profiles up ON u.id = up.user_id
LEFT JOIN user_registration_data urd ON u.id = urd.user_id;

-- Add comments for documentation
COMMENT ON TABLE user_registration_data IS 'Comprehensive user registration data including skills, preferences, and professional information';
COMMENT ON COLUMN user_registration_data.technical_skills IS 'JSON array of technical skills with proficiency levels and experience';
COMMENT ON COLUMN user_registration_data.looking_for IS 'Array of what the user is seeking (mentorship, partnerships, etc.)';
COMMENT ON COLUMN user_registration_data.can_offer IS 'Array of what the user can provide to others';
