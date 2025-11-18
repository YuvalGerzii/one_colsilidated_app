-- Dynamic Profile Updates Migration
-- Tables for real-time need/offering management

-- User needs table
CREATE TABLE IF NOT EXISTS user_needs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  category VARCHAR(100) NOT NULL,
  description TEXT NOT NULL,
  priority VARCHAR(20) NOT NULL CHECK (priority IN ('low', 'medium', 'high', 'critical')),
  urgency VARCHAR(20) NOT NULL CHECK (urgency IN ('flexible', 'weeks', 'days', 'immediate')),
  flexibility FLOAT DEFAULT 0.5 CHECK (flexibility >= 0 AND flexibility <= 1),
  status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'fulfilled', 'expired')),
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_user_needs_user_id ON user_needs(user_id);
CREATE INDEX idx_user_needs_status ON user_needs(status) WHERE status = 'active';
CREATE INDEX idx_user_needs_category ON user_needs(category);
CREATE INDEX idx_user_needs_priority ON user_needs(priority);

-- User offerings table
CREATE TABLE IF NOT EXISTS user_offerings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  category VARCHAR(100) NOT NULL,
  description TEXT NOT NULL,
  value TEXT NOT NULL,
  capacity VARCHAR(20) NOT NULL CHECK (capacity IN ('limited', 'moderate', 'high', 'unlimited')),
  conditions TEXT,
  status VARCHAR(20) DEFAULT 'available' CHECK (status IN ('available', 'reserved', 'unavailable')),
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_user_offerings_user_id ON user_offerings(user_id);
CREATE INDEX idx_user_offerings_status ON user_offerings(status) WHERE status = 'available';
CREATE INDEX idx_user_offerings_category ON user_offerings(category);

-- Profile update history for audit trail
CREATE TABLE IF NOT EXISTS profile_update_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  update_type VARCHAR(20) NOT NULL CHECK (update_type IN ('need', 'offering')),
  action VARCHAR(20) NOT NULL CHECK (action IN ('create', 'update', 'delete')),
  item_id UUID NOT NULL,
  changes JSONB NOT NULL,
  previous_values JSONB,
  version INTEGER NOT NULL,
  timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_profile_history_user_id ON profile_update_history(user_id);
CREATE INDEX idx_profile_history_timestamp ON profile_update_history(timestamp DESC);
CREATE INDEX idx_profile_history_item ON profile_update_history(item_id);

-- Comments for documentation
COMMENT ON TABLE user_needs IS 'User needs with real-time update support';
COMMENT ON TABLE user_offerings IS 'User offerings with real-time update support';
COMMENT ON TABLE profile_update_history IS 'Audit trail for profile changes';
