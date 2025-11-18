-- Bond.AI Database Schema
-- PostgreSQL 14+

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);

-- Contacts table
CREATE TABLE contacts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(50),
    company VARCHAR(255),
    title VARCHAR(255),
    industry VARCHAR(255),
    location VARCHAR(255),
    bio TEXT,
    skills TEXT[],
    interests TEXT[],
    social_profiles JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    source VARCHAR(50), -- 'linkedin', 'manual', 'csv', etc.
    external_id VARCHAR(255), -- ID from source system
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_contacts_user_id ON contacts(user_id);
CREATE INDEX idx_contacts_industry ON contacts(industry);
CREATE INDEX idx_contacts_company ON contacts(company);
CREATE INDEX idx_contacts_source ON contacts(source);
CREATE INDEX idx_contacts_external_id ON contacts(external_id);

-- Connections table (relationships between contacts)
CREATE TABLE connections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    from_contact_id UUID REFERENCES contacts(id) ON DELETE CASCADE,
    to_contact_id UUID REFERENCES contacts(id) ON DELETE CASCADE,
    relationship_type VARCHAR(50),
    strength DECIMAL(3,2) DEFAULT 0.5 CHECK (strength >= 0 AND strength <= 1),
    trust_level DECIMAL(3,2) DEFAULT 0.5 CHECK (trust_level >= 0 AND trust_level <= 1),
    interaction_frequency INTEGER DEFAULT 0,
    last_interaction TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_connections_user_id ON connections(user_id);
CREATE INDEX idx_connections_from_contact ON connections(from_contact_id);
CREATE INDEX idx_connections_to_contact ON connections(to_contact_id);
CREATE INDEX idx_connections_strength ON connections(strength);

-- User profiles (for agent-based matching)
CREATE TABLE user_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE UNIQUE,
    needs JSONB DEFAULT '[]'::jsonb,
    offerings JSONB DEFAULT '[]'::jsonb,
    preferences JSONB DEFAULT '{}'::jsonb,
    constraints JSONB DEFAULT '{}'::jsonb,
    goals JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_user_profiles_user_id ON user_profiles(user_id);

-- Agents table
CREATE TABLE agents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE UNIQUE,
    agent_type VARCHAR(50) DEFAULT 'user_representative',
    config JSONB DEFAULT '{}'::jsonb,
    learning_data JSONB DEFAULT '{}'::jsonb,
    negotiation_history JSONB DEFAULT '[]'::jsonb,
    performance_metrics JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_agents_user_id ON agents(user_id);
CREATE INDEX idx_agents_type ON agents(agent_type);

-- Match candidates table
CREATE TABLE match_candidates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    agent1_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    agent2_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    domain VARCHAR(50),
    domain_score DECIMAL(3,2),
    overall_score DECIMAL(3,2),
    rationale TEXT[],
    key_factors TEXT[],
    risks TEXT[],
    recommended BOOLEAN DEFAULT false,
    status VARCHAR(50) DEFAULT 'new',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_match_candidates_user_id ON match_candidates(user_id);
CREATE INDEX idx_match_candidates_agent1 ON match_candidates(agent1_id);
CREATE INDEX idx_match_candidates_agent2 ON match_candidates(agent2_id);
CREATE INDEX idx_match_candidates_overall_score ON match_candidates(overall_score);
CREATE INDEX idx_match_candidates_status ON match_candidates(status);

-- Negotiations table
CREATE TABLE negotiations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    match_candidate_id UUID REFERENCES match_candidates(id) ON DELETE CASCADE,
    agent1_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    agent2_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'initiated',
    messages JSONB DEFAULT '[]'::jsonb,
    proposed_terms JSONB DEFAULT '[]'::jsonb,
    negotiation_points JSONB DEFAULT '[]'::jsonb,
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    duration_ms INTEGER,
    rounds_count INTEGER DEFAULT 0,
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_negotiations_match_candidate ON negotiations(match_candidate_id);
CREATE INDEX idx_negotiations_status ON negotiations(status);
CREATE INDEX idx_negotiations_started_at ON negotiations(started_at);

-- Agreements table
CREATE TABLE agreements (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    negotiation_id UUID REFERENCES negotiations(id) ON DELETE CASCADE,
    agent1_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    agent2_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    final_terms JSONB NOT NULL,
    compatibility_score DECIMAL(3,2),
    mutual_benefit JSONB,
    agreed_at TIMESTAMP DEFAULT NOW(),
    next_steps TEXT[],
    follow_up_schedule VARCHAR(255),
    status VARCHAR(50) DEFAULT 'active',
    business_value DECIMAL(15,2) DEFAULT 0,
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_agreements_negotiation_id ON agreements(negotiation_id);
CREATE INDEX idx_agreements_agent1 ON agreements(agent1_id);
CREATE INDEX idx_agreements_agent2 ON agreements(agent2_id);
CREATE INDEX idx_agreements_agreed_at ON agreements(agreed_at);
CREATE INDEX idx_agreements_status ON agreements(status);

-- Intelligence analysis cache
CREATE TABLE intelligence_cache (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    contact_id UUID REFERENCES contacts(id) ON DELETE CASCADE UNIQUE,
    analysis JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP DEFAULT NOW() + INTERVAL '24 hours'
);

CREATE INDEX idx_intelligence_cache_contact_id ON intelligence_cache(contact_id);
CREATE INDEX idx_intelligence_cache_expires_at ON intelligence_cache(expires_at);

-- Embeddings table (for semantic matching)
CREATE TABLE embeddings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_type VARCHAR(50) NOT NULL, -- 'need', 'offering', 'contact', etc.
    entity_id UUID NOT NULL,
    text TEXT NOT NULL,
    embedding VECTOR(384), -- Using pgvector extension
    model VARCHAR(100) DEFAULT 'all-MiniLM-L6-v2',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Note: Requires pgvector extension
-- CREATE EXTENSION IF NOT EXISTS vector;
CREATE INDEX idx_embeddings_entity ON embeddings(entity_type, entity_id);

-- OAuth tokens table
CREATE TABLE oauth_tokens (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    provider VARCHAR(50) NOT NULL, -- 'linkedin', 'google', etc.
    access_token TEXT NOT NULL,
    refresh_token TEXT,
    token_type VARCHAR(50),
    expires_at TIMESTAMP,
    scope TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_oauth_tokens_user_id ON oauth_tokens(user_id);
CREATE INDEX idx_oauth_tokens_provider ON oauth_tokens(provider);

-- Activity log table
CREATE TABLE activity_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50),
    entity_id UUID,
    details JSONB DEFAULT '{}'::jsonb,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_activity_log_user_id ON activity_log(user_id);
CREATE INDEX idx_activity_log_action ON activity_log(action);
CREATE INDEX idx_activity_log_created_at ON activity_log(created_at);

-- Notifications table
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL, -- 'new_match', 'negotiation_update', 'agreement_reached', etc.
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    data JSONB DEFAULT '{}'::jsonb,
    read BOOLEAN DEFAULT false,
    priority VARCHAR(20) DEFAULT 'medium', -- 'low', 'medium', 'high', 'critical'
    created_at TIMESTAMP DEFAULT NOW(),
    read_at TIMESTAMP
);

CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_notifications_read ON notifications(read);
CREATE INDEX idx_notifications_priority ON notifications(priority);
CREATE INDEX idx_notifications_created_at ON notifications(created_at);

-- RL (Reinforcement Learning) Q-Table
CREATE TABLE rl_q_values (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    state_hash VARCHAR(64) NOT NULL, -- Hash of state
    action VARCHAR(100) NOT NULL,
    q_value DECIMAL(10,6) DEFAULT 0,
    visits INTEGER DEFAULT 0,
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_rl_q_values_agent_id ON rl_q_values(agent_id);
CREATE INDEX idx_rl_q_values_state_action ON rl_q_values(state_hash, action);

-- Performance metrics table
CREATE TABLE performance_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    metric_type VARCHAR(50) NOT NULL, -- 'negotiation', 'match', 'agreement', etc.
    metric_name VARCHAR(100) NOT NULL,
    value DECIMAL(15,6),
    dimensions JSONB DEFAULT '{}'::jsonb,
    timestamp TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_performance_metrics_type ON performance_metrics(metric_type);
CREATE INDEX idx_performance_metrics_name ON performance_metrics(metric_name);
CREATE INDEX idx_performance_metrics_timestamp ON performance_metrics(timestamp);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply updated_at trigger to relevant tables
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_contacts_updated_at BEFORE UPDATE ON contacts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_connections_updated_at BEFORE UPDATE ON connections
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_profiles_updated_at BEFORE UPDATE ON user_profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_agents_updated_at BEFORE UPDATE ON agents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_match_candidates_updated_at BEFORE UPDATE ON match_candidates
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_oauth_tokens_updated_at BEFORE UPDATE ON oauth_tokens
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Views for analytics

-- Network statistics view
CREATE VIEW network_stats AS
SELECT
    u.id as user_id,
    u.name,
    COUNT(DISTINCT c.id) as total_contacts,
    COUNT(DISTINCT conn.id) as total_connections,
    AVG(conn.strength) as avg_connection_strength,
    COUNT(DISTINCT mc.id) as total_matches,
    COUNT(DISTINCT a.id) as total_agreements
FROM users u
LEFT JOIN contacts c ON c.user_id = u.id
LEFT JOIN connections conn ON conn.user_id = u.id
LEFT JOIN match_candidates mc ON mc.user_id = u.id
LEFT JOIN agreements a ON a.agent1_id IN (SELECT id FROM agents WHERE user_id = u.id)
GROUP BY u.id, u.name;

-- Platform metrics view
CREATE VIEW platform_metrics AS
SELECT
    COUNT(DISTINCT u.id) as total_users,
    COUNT(DISTINCT c.id) as total_contacts,
    COUNT(DISTINCT conn.id) as total_connections,
    COUNT(DISTINCT mc.id) as total_matches,
    COUNT(DISTINCT n.id) as total_negotiations,
    COUNT(DISTINCT a.id) as total_agreements,
    ROUND(
        COUNT(DISTINCT CASE WHEN n.status = 'agreement_reached' THEN n.id END)::DECIMAL /
        NULLIF(COUNT(DISTINCT n.id), 0) * 100,
        2
    ) as success_rate,
    AVG(mc.overall_score) as avg_match_score
FROM users u
LEFT JOIN contacts c ON c.user_id = u.id
LEFT JOIN connections conn ON conn.user_id = u.id
LEFT JOIN match_candidates mc ON mc.user_id = u.id
LEFT JOIN negotiations n ON n.match_candidate_id = mc.id
LEFT JOIN agreements a ON a.negotiation_id = n.id;

-- Grant permissions (adjust as needed)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO bondai_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO bondai_user;
