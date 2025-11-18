-- Enhancement Migration: Advanced Features for Agents System
-- Adds analytics, collaboration, templates, debates, webhooks, and more

-- ============================================
-- TEAM COLLABORATION
-- ============================================

-- Teams/Organizations table
CREATE TABLE IF NOT EXISTS teams (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name VARCHAR(255) NOT NULL,
  description TEXT,
  owner_id UUID REFERENCES users(id) ON DELETE CASCADE,
  subscription_tier VARCHAR(50) DEFAULT 'free', -- free, pro, enterprise
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Team members
CREATE TABLE IF NOT EXISTS team_members (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  team_id UUID REFERENCES teams(id) ON DELETE CASCADE,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  role VARCHAR(50) DEFAULT 'member', -- owner, admin, member, viewer
  permissions JSONB DEFAULT '{}', -- Custom permissions object
  joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(team_id, user_id)
);

-- Shared board rooms
ALTER TABLE board_rooms ADD COLUMN IF NOT EXISTS team_id UUID REFERENCES teams(id) ON DELETE CASCADE;
ALTER TABLE board_rooms ADD COLUMN IF NOT EXISTS is_public BOOLEAN DEFAULT false;
ALTER TABLE board_rooms ADD COLUMN IF NOT EXISTS share_token VARCHAR(100) UNIQUE;

-- Shared conversations
ALTER TABLE agent_conversations ADD COLUMN IF NOT EXISTS team_id UUID REFERENCES teams(id) ON DELETE SET NULL;
ALTER TABLE agent_conversations ADD COLUMN IF NOT EXISTS is_shared BOOLEAN DEFAULT false;

-- ============================================
-- DECISION TEMPLATES & FRAMEWORKS
-- ============================================

-- Decision templates
CREATE TABLE IF NOT EXISTS decision_templates (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  team_id UUID REFERENCES teams(id) ON DELETE CASCADE,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  category VARCHAR(100), -- strategy, investment, product, hiring, etc.
  template_data JSONB NOT NULL, -- Questions, framework, criteria
  decision_context VARCHAR(50),
  recommended_agents TEXT[], -- Array of agent keys
  recommended_board_room_id UUID REFERENCES board_rooms(id) ON DELETE SET NULL,
  usage_count INTEGER DEFAULT 0,
  is_public BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Decision instances (when template is used)
CREATE TABLE IF NOT EXISTS decision_instances (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  template_id UUID REFERENCES decision_templates(id) ON DELETE SET NULL,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  conversation_id UUID REFERENCES agent_conversations(id) ON DELETE CASCADE,
  instance_data JSONB NOT NULL, -- Filled template with actual data
  status VARCHAR(50) DEFAULT 'in_progress', -- in_progress, decided, abandoned
  final_decision TEXT,
  outcome TEXT, -- What actually happened
  success_rating INTEGER, -- 1-5 how well did it work
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- AGENT DEBATES & COMPARISONS
-- ============================================

-- Multi-agent debates
CREATE TABLE IF NOT EXISTS agent_debates (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  conversation_id UUID REFERENCES agent_conversations(id) ON DELETE CASCADE,
  topic TEXT NOT NULL,
  debate_type VARCHAR(50) DEFAULT 'roundtable', -- roundtable, adversarial, panel
  participating_agents UUID[] NOT NULL, -- Array of agent IDs
  moderator_agent_id UUID REFERENCES behavior_agents(id) ON DELETE SET NULL,
  debate_data JSONB, -- Structured debate with rounds, arguments, rebuttals
  consensus_reached BOOLEAN DEFAULT false,
  final_recommendation TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  completed_at TIMESTAMP
);

-- Debate rounds and arguments
CREATE TABLE IF NOT EXISTS debate_messages (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  debate_id UUID REFERENCES agent_debates(id) ON DELETE CASCADE,
  agent_id UUID REFERENCES behavior_agents(id) ON DELETE CASCADE,
  round_number INTEGER NOT NULL,
  message_type VARCHAR(50), -- opening, argument, rebuttal, closing
  content TEXT NOT NULL,
  references_message_id UUID REFERENCES debate_messages(id) ON DELETE SET NULL,
  supporting_data JSONB,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_debate_messages (debate_id, round_number)
);

-- Agent comparisons
CREATE TABLE IF NOT EXISTS agent_comparisons (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  conversation_id UUID REFERENCES agent_conversations(id) ON DELETE SET NULL,
  question TEXT NOT NULL,
  compared_agents UUID[] NOT NULL,
  comparison_matrix JSONB NOT NULL, -- Structured comparison data
  user_choice UUID REFERENCES behavior_agents(id) ON DELETE SET NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- ANALYTICS & INSIGHTS
-- ============================================

-- Consultation outcomes tracking
CREATE TABLE IF NOT EXISTS consultation_outcomes (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  consultation_id UUID REFERENCES agent_consultations(id) ON DELETE CASCADE,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  decision_implemented BOOLEAN DEFAULT false,
  implementation_date TIMESTAMP,
  outcome_description TEXT,
  success_level INTEGER, -- 1-5 rating
  roi_estimate DECIMAL(15,2), -- Estimated return on investment
  time_saved_hours INTEGER,
  lessons_learned TEXT,
  would_follow_again BOOLEAN,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Agent performance metrics (aggregated)
CREATE TABLE IF NOT EXISTS agent_performance_metrics (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  agent_id UUID REFERENCES behavior_agents(id) ON DELETE CASCADE,
  metric_period VARCHAR(20) DEFAULT 'daily', -- daily, weekly, monthly, all_time
  period_start TIMESTAMP NOT NULL,
  period_end TIMESTAMP NOT NULL,
  total_consultations INTEGER DEFAULT 0,
  average_rating DECIMAL(3,2),
  average_confidence DECIMAL(3,2),
  success_rate DECIMAL(3,2), -- Based on outcome tracking
  decision_contexts JSONB, -- Breakdown by context
  sector_breakdown JSONB, -- Performance by sector
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(agent_id, metric_period, period_start)
);

-- User engagement analytics
CREATE TABLE IF NOT EXISTS user_engagement_metrics (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  metric_date DATE NOT NULL,
  conversations_started INTEGER DEFAULT 0,
  questions_asked INTEGER DEFAULT 0,
  agents_consulted INTEGER DEFAULT 0,
  board_rooms_used INTEGER DEFAULT 0,
  templates_used INTEGER DEFAULT 0,
  debates_created INTEGER DEFAULT 0,
  time_spent_minutes INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(user_id, metric_date)
);

-- ============================================
-- WEBHOOKS & INTEGRATIONS
-- ============================================

-- Webhook configurations
CREATE TABLE IF NOT EXISTS webhooks (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  team_id UUID REFERENCES teams(id) ON DELETE CASCADE,
  name VARCHAR(255) NOT NULL,
  url VARCHAR(500) NOT NULL,
  secret_key VARCHAR(255) NOT NULL, -- For HMAC signature
  events TEXT[] NOT NULL, -- consultation.completed, debate.finished, etc.
  is_active BOOLEAN DEFAULT true,
  retry_count INTEGER DEFAULT 3,
  timeout_seconds INTEGER DEFAULT 30,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  last_triggered_at TIMESTAMP
);

-- Webhook delivery logs
CREATE TABLE IF NOT EXISTS webhook_deliveries (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  webhook_id UUID REFERENCES webhooks(id) ON DELETE CASCADE,
  event_type VARCHAR(100) NOT NULL,
  payload JSONB NOT NULL,
  response_status INTEGER,
  response_body TEXT,
  delivery_duration_ms INTEGER,
  success BOOLEAN DEFAULT false,
  error_message TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_webhook_deliveries (webhook_id, created_at DESC)
);

-- External integrations
CREATE TABLE IF NOT EXISTS integrations (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  team_id UUID REFERENCES teams(id) ON DELETE CASCADE,
  integration_type VARCHAR(50) NOT NULL, -- slack, teams, email, zapier, etc.
  config JSONB NOT NULL, -- API keys, settings, etc.
  is_active BOOLEAN DEFAULT true,
  last_sync_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- SCHEDULED CONSULTATIONS & AUTOMATION
-- ============================================

-- Scheduled consultations
CREATE TABLE IF NOT EXISTS scheduled_consultations (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  team_id UUID REFERENCES teams(id) ON DELETE CASCADE,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  question_template TEXT NOT NULL,
  agent_keys TEXT[],
  board_room_id UUID REFERENCES board_rooms(id) ON DELETE SET NULL,
  decision_context VARCHAR(50),
  schedule_cron VARCHAR(100), -- Cron expression
  next_run_at TIMESTAMP,
  last_run_at TIMESTAMP,
  is_active BOOLEAN DEFAULT true,
  notification_emails TEXT[],
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Scheduled consultation runs
CREATE TABLE IF NOT EXISTS scheduled_consultation_runs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  scheduled_consultation_id UUID REFERENCES scheduled_consultations(id) ON DELETE CASCADE,
  conversation_id UUID REFERENCES agent_conversations(id) ON DELETE SET NULL,
  status VARCHAR(50) DEFAULT 'pending', -- pending, running, completed, failed
  started_at TIMESTAMP,
  completed_at TIMESTAMP,
  error_message TEXT,
  result_summary JSONB,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- AUDIT LOGS & SECURITY
-- ============================================

-- Audit logs
CREATE TABLE IF NOT EXISTS audit_logs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE SET NULL,
  team_id UUID REFERENCES teams(id) ON DELETE SET NULL,
  action VARCHAR(100) NOT NULL, -- user.login, agent.consulted, board.created, etc.
  resource_type VARCHAR(50), -- user, agent, conversation, etc.
  resource_id UUID,
  ip_address INET,
  user_agent TEXT,
  metadata JSONB, -- Additional context
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_audit_logs_user (user_id, created_at DESC),
  INDEX idx_audit_logs_action (action, created_at DESC)
);

-- User sessions
CREATE TABLE IF NOT EXISTS user_sessions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  token_hash VARCHAR(255) UNIQUE NOT NULL,
  ip_address INET,
  user_agent TEXT,
  expires_at TIMESTAMP NOT NULL,
  last_activity_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_user_sessions (user_id, is_active)
);

-- ============================================
-- NOTIFICATIONS & REMINDERS
-- ============================================

-- User notifications
CREATE TABLE IF NOT EXISTS notifications (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  notification_type VARCHAR(50) NOT NULL, -- reminder, insight, update, alert
  title VARCHAR(255) NOT NULL,
  message TEXT NOT NULL,
  action_url VARCHAR(500),
  metadata JSONB,
  is_read BOOLEAN DEFAULT false,
  is_dismissed BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  read_at TIMESTAMP,
  INDEX idx_notifications_user (user_id, is_read, created_at DESC)
);

-- Follow-up reminders
CREATE TABLE IF NOT EXISTS followup_reminders (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  consultation_id UUID REFERENCES agent_consultations(id) ON DELETE CASCADE,
  decision_instance_id UUID REFERENCES decision_instances(id) ON DELETE CASCADE,
  reminder_date TIMESTAMP NOT NULL,
  reminder_type VARCHAR(50), -- outcome_check, implementation_review, etc.
  message TEXT,
  is_sent BOOLEAN DEFAULT false,
  sent_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_followup_reminders (reminder_date, is_sent)
);

-- ============================================
-- LEARNING & INTELLIGENCE
-- ============================================

-- Conversation tags (auto-generated and manual)
CREATE TABLE IF NOT EXISTS conversation_tags (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  conversation_id UUID REFERENCES agent_conversations(id) ON DELETE CASCADE,
  tag VARCHAR(100) NOT NULL,
  tag_type VARCHAR(50) DEFAULT 'auto', -- auto, manual, suggested
  confidence DECIMAL(3,2), -- For auto-generated tags
  created_by UUID REFERENCES users(id) ON DELETE SET NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(conversation_id, tag)
);

-- Industry insights and trends
CREATE TABLE IF NOT EXISTS industry_insights (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  industry VARCHAR(100) NOT NULL,
  insight_type VARCHAR(50), -- trend, pattern, recommendation
  title VARCHAR(255) NOT NULL,
  description TEXT NOT NULL,
  supporting_data JSONB,
  confidence_score DECIMAL(3,2),
  source VARCHAR(100), -- derived, manual, external
  is_active BOOLEAN DEFAULT true,
  valid_from TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  valid_until TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Agent learning feedback (improve over time)
CREATE TABLE IF NOT EXISTS agent_learning_feedback (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  agent_id UUID REFERENCES behavior_agents(id) ON DELETE CASCADE,
  consultation_id UUID REFERENCES agent_consultations(id) ON DELETE CASCADE,
  feedback_type VARCHAR(50), -- too_conservative, too_aggressive, helpful, etc.
  context_analysis JSONB, -- What was the context
  user_correction TEXT, -- What should have been said
  impact_score INTEGER, -- 1-5 how impactful this feedback is
  incorporated BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- EXPORT & REPORTING
-- ============================================

-- Report templates
CREATE TABLE IF NOT EXISTS report_templates (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  team_id UUID REFERENCES teams(id) ON DELETE CASCADE,
  name VARCHAR(255) NOT NULL,
  report_type VARCHAR(50), -- executive_summary, decision_history, agent_performance
  template_config JSONB NOT NULL,
  is_public BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Generated reports
CREATE TABLE IF NOT EXISTS generated_reports (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  template_id UUID REFERENCES report_templates(id) ON DELETE SET NULL,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  report_data JSONB NOT NULL,
  file_url VARCHAR(500), -- If exported to PDF/CSV
  date_range_start TIMESTAMP,
  date_range_end TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_generated_reports (user_id, created_at DESC)
);

-- ============================================
-- INDEXES FOR PERFORMANCE
-- ============================================

CREATE INDEX IF NOT EXISTS idx_team_members_user ON team_members(user_id);
CREATE INDEX IF NOT EXISTS idx_team_members_team ON team_members(team_id);
CREATE INDEX IF NOT EXISTS idx_decision_templates_category ON decision_templates(category);
CREATE INDEX IF NOT EXISTS idx_decision_instances_status ON decision_instances(status);
CREATE INDEX IF NOT EXISTS idx_agent_debates_completed ON agent_debates(completed_at);
CREATE INDEX IF NOT EXISTS idx_consultation_outcomes_success ON consultation_outcomes(success_level);
CREATE INDEX IF NOT EXISTS idx_webhooks_active ON webhooks(is_active);
CREATE INDEX IF NOT EXISTS idx_scheduled_consultations_next_run ON scheduled_consultations(next_run_at, is_active);
CREATE INDEX IF NOT EXISTS idx_notifications_unread ON notifications(user_id, is_read) WHERE is_read = false;
CREATE INDEX IF NOT EXISTS idx_conversation_tags_tag ON conversation_tags(tag);

-- ============================================
-- TRIGGERS
-- ============================================

-- Update updated_at on teams
DROP TRIGGER IF EXISTS update_teams_updated_at ON teams;
CREATE TRIGGER update_teams_updated_at BEFORE UPDATE ON teams
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Update updated_at on decision_templates
DROP TRIGGER IF EXISTS update_decision_templates_updated_at ON decision_templates;
CREATE TRIGGER update_decision_templates_updated_at BEFORE UPDATE ON decision_templates
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Update updated_at on decision_instances
DROP TRIGGER IF EXISTS update_decision_instances_updated_at ON decision_instances;
CREATE TRIGGER update_decision_instances_updated_at BEFORE UPDATE ON decision_instances
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Update updated_at on consultation_outcomes
DROP TRIGGER IF EXISTS update_consultation_outcomes_updated_at ON consultation_outcomes;
CREATE TRIGGER update_consultation_outcomes_updated_at BEFORE UPDATE ON consultation_outcomes
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Update updated_at on integrations
DROP TRIGGER IF EXISTS update_integrations_updated_at ON integrations;
CREATE TRIGGER update_integrations_updated_at BEFORE UPDATE ON integrations
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Update updated_at on scheduled_consultations
DROP TRIGGER IF EXISTS update_scheduled_consultations_updated_at ON scheduled_consultations;
CREATE TRIGGER update_scheduled_consultations_updated_at BEFORE UPDATE ON scheduled_consultations
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- COMMENTS
-- ============================================

COMMENT ON TABLE teams IS 'Organizations/teams for collaboration';
COMMENT ON TABLE team_members IS 'Team membership with roles and permissions';
COMMENT ON TABLE decision_templates IS 'Reusable decision-making frameworks';
COMMENT ON TABLE decision_instances IS 'Actual decisions made using templates';
COMMENT ON TABLE agent_debates IS 'Multi-agent debate sessions';
COMMENT ON TABLE debate_messages IS 'Individual arguments in debates';
COMMENT ON TABLE agent_comparisons IS 'Side-by-side agent comparisons';
COMMENT ON TABLE consultation_outcomes IS 'Real-world outcomes of following agent advice';
COMMENT ON TABLE agent_performance_metrics IS 'Aggregated performance data for agents';
COMMENT ON TABLE webhooks IS 'Webhook configurations for external integrations';
COMMENT ON TABLE webhook_deliveries IS 'Log of webhook delivery attempts';
COMMENT ON TABLE scheduled_consultations IS 'Automated recurring consultations';
COMMENT ON TABLE audit_logs IS 'Complete audit trail of all system actions';
COMMENT ON TABLE notifications IS 'User notifications and alerts';
COMMENT ON TABLE followup_reminders IS 'Scheduled follow-ups on decisions';
COMMENT ON TABLE conversation_tags IS 'Tags for organizing and searching conversations';
COMMENT ON TABLE agent_learning_feedback IS 'Feedback to improve agent responses over time';
