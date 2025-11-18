-- Initial Schema for Standalone Agents System
-- Creates all necessary tables for behavior agents and chatbot functionality

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table (standalone authentication)
CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  full_name VARCHAR(255),
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Behavior agents table (tracks available agents)
CREATE TABLE IF NOT EXISTS behavior_agents (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  agent_key VARCHAR(50) UNIQUE NOT NULL, -- 'musk', 'jobs', 'bezos', etc.
  name VARCHAR(100) NOT NULL,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  companies TEXT[], -- Array of companies
  sectors TEXT[], -- Array of business sectors
  avatar_url VARCHAR(500),
  is_active BOOLEAN DEFAULT true,
  sort_order INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default behavior agents
INSERT INTO behavior_agents (agent_key, name, title, description, companies, sectors, avatar_url, sort_order) VALUES
('musk', 'Elon Musk', 'CEO of Tesla, SpaceX, X (Twitter)', 'First principles thinking, aggressive timelines, physics-based innovation, vertical integration strategy',
 ARRAY['Tesla', 'SpaceX', 'X (Twitter)', 'Neuralink'], ARRAY['technology', 'automotive', 'aerospace', 'social_media'],
 '/agents/elon-musk.jpg', 1),

('jobs', 'Steve Jobs', 'Co-founder of Apple', 'User experience first, simplification and design excellence, holistic innovation',
 ARRAY['Apple'], ARRAY['technology'],
 '/agents/steve-jobs.jpg', 2),

('zuckerberg', 'Mark Zuckerberg', 'CEO of Meta', 'Data-driven decision making, move fast and break things, long-term futuristic bets',
 ARRAY['Meta', 'Facebook'], ARRAY['technology', 'social_media'],
 '/agents/mark-zuckerberg.jpg', 3),

('bezos', 'Jeff Bezos', 'Founder of Amazon', 'Customer obsession, Day 1 mentality, embrace failure and experimentation',
 ARRAY['Amazon'], ARRAY['e_commerce', 'technology'],
 '/agents/jeff-bezos.jpg', 4),

('fink', 'Larry Fink', 'CEO of BlackRock', 'Long-term sustainability focus, stakeholder capitalism, risk management expertise',
 ARRAY['BlackRock'], ARRAY['finance'],
 '/agents/larry-fink.jpg', 5),

('trump', 'Donald Trump', 'Real Estate Developer & Entrepreneur', 'Aggressive negotiation, extreme anchoring, branding and marketing',
 ARRAY['Trump Organization'], ARRAY['real_estate', 'general'],
 '/agents/donald-trump.jpg', 6),

('zell', 'Sam Zell', 'Chairman of Equity Residential', 'Grave dancing - distressed opportunities, supply and demand focus, contrarian investing',
 ARRAY['Equity Residential'], ARRAY['real_estate', 'finance'],
 '/agents/sam-zell.jpg', 7),

('bren', 'Donald Bren', 'Chairman of Irvine Company', 'Quality and attention to detail, long-term vision, sustainability focus',
 ARRAY['Irvine Company'], ARRAY['real_estate'],
 '/agents/donald-bren.jpg', 8)
ON CONFLICT (agent_key) DO NOTHING;

-- Board rooms table (predefined and custom)
CREATE TABLE IF NOT EXISTS board_rooms (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE, -- NULL for predefined boards
  name VARCHAR(255) NOT NULL,
  description TEXT,
  focus_sectors TEXT[], -- Array of business sectors
  decision_style VARCHAR(50) DEFAULT 'majority', -- unanimous, majority, weighted, advisory
  consensus_threshold DECIMAL(3,2) DEFAULT 0.6,
  is_predefined BOOLEAN DEFAULT false, -- System-defined boards
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Board room members (many-to-many)
CREATE TABLE IF NOT EXISTS board_room_members (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  board_room_id UUID REFERENCES board_rooms(id) ON DELETE CASCADE,
  agent_id UUID REFERENCES behavior_agents(id) ON DELETE CASCADE,
  voting_weight DECIMAL(3,2) DEFAULT 1.0, -- For weighted voting
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(board_room_id, agent_id)
);

-- Insert predefined board rooms
INSERT INTO board_rooms (name, description, focus_sectors, decision_style, is_predefined, consensus_threshold) VALUES
('Tech Innovation Board', 'Product development, innovation, technology strategy',
 ARRAY['technology', 'e_commerce', 'social_media'], 'majority', true, 0.6),
('Investment & Finance Board', 'Investment decisions, financial strategy, capital allocation',
 ARRAY['finance', 'real_estate'], 'weighted', true, 0.6),
('Real Estate Development Board', 'Real estate strategy, development, property investment',
 ARRAY['real_estate'], 'majority', true, 0.6),
('Negotiation & Deal Making Board', 'Negotiations, partnerships, deal structuring',
 ARRAY['general'], 'advisory', true, 0.5),
('Product Strategy Board', 'Product development, UX, go-to-market',
 ARRAY['technology', 'e_commerce'], 'majority', true, 0.6),
('Growth & Scale Board', 'Scaling operations, market expansion, growth strategy',
 ARRAY['technology', 'e_commerce', 'finance'], 'majority', true, 0.6),
('Crisis Management Board', 'Crisis response, rapid decision-making, damage control',
 ARRAY['general'], 'advisory', true, 0.5),
('Executive Leadership Board', 'Comprehensive strategic decisions',
 ARRAY['technology', 'finance', 'real_estate', 'e_commerce', 'social_media'], 'weighted', true, 0.6);

-- Link agents to predefined board rooms
-- Tech Innovation Board: Musk, Jobs, Zuckerberg, Bezos
INSERT INTO board_room_members (board_room_id, agent_id, voting_weight)
SELECT br.id, ba.id, 1.0
FROM board_rooms br
CROSS JOIN behavior_agents ba
WHERE br.name = 'Tech Innovation Board'
  AND ba.agent_key IN ('musk', 'jobs', 'zuckerberg', 'bezos')
ON CONFLICT DO NOTHING;

-- Investment & Finance Board: Fink, Zell, Bren
INSERT INTO board_room_members (board_room_id, agent_id, voting_weight)
SELECT br.id, ba.id,
  CASE
    WHEN ba.agent_key = 'fink' THEN 0.4
    WHEN ba.agent_key = 'zell' THEN 0.3
    WHEN ba.agent_key = 'bren' THEN 0.3
  END
FROM board_rooms br
CROSS JOIN behavior_agents ba
WHERE br.name = 'Investment & Finance Board'
  AND ba.agent_key IN ('fink', 'zell', 'bren')
ON CONFLICT DO NOTHING;

-- Real Estate Development Board: Zell, Bren, Trump
INSERT INTO board_room_members (board_room_id, agent_id, voting_weight)
SELECT br.id, ba.id, 1.0
FROM board_rooms br
CROSS JOIN behavior_agents ba
WHERE br.name = 'Real Estate Development Board'
  AND ba.agent_key IN ('zell', 'bren', 'trump')
ON CONFLICT DO NOTHING;

-- Negotiation & Deal Making Board: Trump, Zell, Musk, Fink
INSERT INTO board_room_members (board_room_id, agent_id, voting_weight)
SELECT br.id, ba.id, 1.0
FROM board_rooms br
CROSS JOIN behavior_agents ba
WHERE br.name = 'Negotiation & Deal Making Board'
  AND ba.agent_key IN ('trump', 'zell', 'musk', 'fink')
ON CONFLICT DO NOTHING;

-- Product Strategy Board: Jobs, Zuckerberg, Bezos, Musk
INSERT INTO board_room_members (board_room_id, agent_id, voting_weight)
SELECT br.id, ba.id, 1.0
FROM board_rooms br
CROSS JOIN behavior_agents ba
WHERE br.name = 'Product Strategy Board'
  AND ba.agent_key IN ('jobs', 'zuckerberg', 'bezos', 'musk')
ON CONFLICT DO NOTHING;

-- Growth & Scale Board: Bezos, Zuckerberg, Musk, Fink
INSERT INTO board_room_members (board_room_id, agent_id, voting_weight)
SELECT br.id, ba.id, 1.0
FROM board_rooms br
CROSS JOIN behavior_agents ba
WHERE br.name = 'Growth & Scale Board'
  AND ba.agent_key IN ('bezos', 'zuckerberg', 'musk', 'fink')
ON CONFLICT DO NOTHING;

-- Crisis Management Board: Musk, Trump, Fink, Zell
INSERT INTO board_room_members (board_room_id, agent_id, voting_weight)
SELECT br.id, ba.id, 1.0
FROM board_rooms br
CROSS JOIN behavior_agents ba
WHERE br.name = 'Crisis Management Board'
  AND ba.agent_key IN ('musk', 'trump', 'fink', 'zell')
ON CONFLICT DO NOTHING;

-- Executive Leadership Board: All agents
INSERT INTO board_room_members (board_room_id, agent_id, voting_weight)
SELECT br.id, ba.id, 0.125 -- Equal weight for 8 members
FROM board_rooms br
CROSS JOIN behavior_agents ba
WHERE br.name = 'Executive Leadership Board'
ON CONFLICT DO NOTHING;

-- Chatbot conversations table
CREATE TABLE IF NOT EXISTS agent_conversations (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(255),
  context_type VARCHAR(50) NOT NULL, -- 'individual', 'board_room', 'comparison'
  selected_agents UUID[], -- Array of behavior_agents IDs
  board_room_id UUID REFERENCES board_rooms(id) ON DELETE SET NULL,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chatbot messages table
CREATE TABLE IF NOT EXISTS agent_messages (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  conversation_id UUID REFERENCES agent_conversations(id) ON DELETE CASCADE,
  role VARCHAR(20) NOT NULL, -- 'user', 'agent', 'system'
  agent_id UUID REFERENCES behavior_agents(id) ON DELETE SET NULL, -- NULL for user messages
  content TEXT NOT NULL,
  decision_context VARCHAR(50), -- From DecisionContext enum
  structured_data JSONB, -- Analysis results, decision breakdown, etc.
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User agent preferences (which agents user prefers)
CREATE TABLE IF NOT EXISTS user_agent_preferences (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  agent_id UUID REFERENCES behavior_agents(id) ON DELETE CASCADE,
  is_favorite BOOLEAN DEFAULT false,
  usage_count INTEGER DEFAULT 0,
  last_used_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(user_id, agent_id)
);

-- Agent consultation history (track all advice given)
CREATE TABLE IF NOT EXISTS agent_consultations (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  conversation_id UUID REFERENCES agent_conversations(id) ON DELETE CASCADE,
  agent_id UUID REFERENCES behavior_agents(id) ON DELETE CASCADE, -- NULL for board room
  board_room_id UUID REFERENCES board_rooms(id) ON DELETE SET NULL,
  question TEXT NOT NULL,
  decision_context VARCHAR(50),
  advice TEXT NOT NULL,
  confidence_score DECIMAL(3,2),
  success_probability DECIMAL(3,2),
  structured_response JSONB, -- Full BusinessAdvice or BoardRoomConsensus object
  user_rating INTEGER, -- 1-5 stars
  user_feedback TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_board_room_members ON board_room_members(board_room_id);
CREATE INDEX IF NOT EXISTS idx_agent_messages_conversation ON agent_messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_agent_conversations_user ON agent_conversations(user_id, is_active);
CREATE INDEX IF NOT EXISTS idx_user_preferences ON user_agent_preferences(user_id);
CREATE INDEX IF NOT EXISTS idx_consultations_user_date ON agent_consultations(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_consultations_agent_date ON agent_consultations(agent_id, created_at DESC);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$ language 'plpgsql';

-- Add triggers for updated_at
DROP TRIGGER IF EXISTS update_users_updated_at ON users;
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_behavior_agents_updated_at ON behavior_agents;
CREATE TRIGGER update_behavior_agents_updated_at BEFORE UPDATE ON behavior_agents
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_board_rooms_updated_at ON board_rooms;
CREATE TRIGGER update_board_rooms_updated_at BEFORE UPDATE ON board_rooms
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_agent_conversations_updated_at ON agent_conversations;
CREATE TRIGGER update_agent_conversations_updated_at BEFORE UPDATE ON agent_conversations
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Add comments for documentation
COMMENT ON TABLE users IS 'User accounts for agents system';
COMMENT ON TABLE behavior_agents IS 'Available behavior analysis agents (business leaders)';
COMMENT ON TABLE board_rooms IS 'Board room configurations (predefined and custom)';
COMMENT ON TABLE board_room_members IS 'Agents assigned to board rooms with voting weights';
COMMENT ON TABLE agent_conversations IS 'User chatbot conversations with agents';
COMMENT ON TABLE agent_messages IS 'Individual messages in agent conversations';
COMMENT ON TABLE user_agent_preferences IS 'User preferences and favorites for agents';
COMMENT ON TABLE agent_consultations IS 'History of all agent consultations and advice';
