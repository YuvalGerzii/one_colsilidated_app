-- In-App Messaging System Migration
-- Tables for real-time messaging with scalability

-- Conversations table
CREATE TABLE IF NOT EXISTS conversations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  participants UUID[] NOT NULL,
  type VARCHAR(20) NOT NULL CHECK (type IN ('direct', 'negotiation', 'introduction')),
  match_id UUID REFERENCES match_candidates(id) ON DELETE SET NULL,
  last_message_id UUID,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_conversations_participants ON conversations USING GIN(participants);
CREATE INDEX idx_conversations_updated ON conversations(updated_at DESC);
CREATE INDEX idx_conversations_match ON conversations(match_id) WHERE match_id IS NOT NULL;

-- Messages table
CREATE TABLE IF NOT EXISTS messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
  sender_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  recipient_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  content TEXT NOT NULL,
  type VARCHAR(20) DEFAULT 'text' CHECK (type IN ('text', 'system', 'introduction', 'proposal')),
  metadata JSONB DEFAULT '{}',
  status VARCHAR(20) DEFAULT 'sent' CHECK (status IN ('sent', 'delivered', 'read')),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  delivered_at TIMESTAMP WITH TIME ZONE,
  read_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_messages_conversation ON messages(conversation_id, created_at DESC);
CREATE INDEX idx_messages_sender ON messages(sender_id);
CREATE INDEX idx_messages_recipient ON messages(recipient_id);
CREATE INDEX idx_messages_status ON messages(status) WHERE status != 'read';
CREATE INDEX idx_messages_created ON messages(created_at DESC);

-- Add foreign key for last_message_id after messages table exists
ALTER TABLE conversations
  DROP CONSTRAINT IF EXISTS fk_conversations_last_message,
  ADD CONSTRAINT fk_conversations_last_message
    FOREIGN KEY (last_message_id) REFERENCES messages(id) ON DELETE SET NULL;

-- Message reactions table
CREATE TABLE IF NOT EXISTS message_reactions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  message_id UUID NOT NULL REFERENCES messages(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  reaction VARCHAR(50) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

  UNIQUE(message_id, user_id, reaction)
);

CREATE INDEX idx_message_reactions_message ON message_reactions(message_id);
CREATE INDEX idx_message_reactions_user ON message_reactions(user_id);

-- Typing indicators (in-memory via Redis, this is for history)
CREATE TABLE IF NOT EXISTS typing_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  stopped_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_typing_history_conversation ON typing_history(conversation_id);

-- Message attachments table
CREATE TABLE IF NOT EXISTS message_attachments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  message_id UUID NOT NULL REFERENCES messages(id) ON DELETE CASCADE,
  file_name VARCHAR(255) NOT NULL,
  file_type VARCHAR(100) NOT NULL,
  file_size INTEGER NOT NULL,
  file_url TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_message_attachments_message ON message_attachments(message_id);

-- Function to update conversation's updated_at timestamp
CREATE OR REPLACE FUNCTION update_conversation_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE conversations
  SET updated_at = NOW()
  WHERE id = NEW.conversation_id;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to update conversation timestamp on new message
CREATE TRIGGER trigger_update_conversation_timestamp
AFTER INSERT ON messages
FOR EACH ROW
EXECUTE FUNCTION update_conversation_timestamp();

-- Function to update message status to delivered
CREATE OR REPLACE FUNCTION mark_message_delivered()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.status = 'delivered' AND OLD.status = 'sent' THEN
    NEW.delivered_at = NOW();
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to set delivered_at timestamp
CREATE TRIGGER trigger_mark_delivered
BEFORE UPDATE ON messages
FOR EACH ROW
WHEN (NEW.status = 'delivered' AND OLD.status = 'sent')
EXECUTE FUNCTION mark_message_delivered();

-- Function to update message status to read
CREATE OR REPLACE FUNCTION mark_message_read()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.status = 'read' AND OLD.status != 'read' THEN
    NEW.read_at = NOW();
    IF NEW.delivered_at IS NULL THEN
      NEW.delivered_at = NOW();
    END IF;
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to set read_at timestamp
CREATE TRIGGER trigger_mark_read
BEFORE UPDATE ON messages
FOR EACH ROW
WHEN (NEW.status = 'read' AND OLD.status != 'read')
EXECUTE FUNCTION mark_message_read();

-- Materialized view for conversation statistics
CREATE MATERIALIZED VIEW IF NOT EXISTS conversation_stats AS
SELECT
  c.id as conversation_id,
  COUNT(m.id) as total_messages,
  COUNT(CASE WHEN m.status = 'read' THEN 1 END) as read_messages,
  MAX(m.created_at) as last_activity,
  array_agg(DISTINCT m.sender_id) as active_participants
FROM conversations c
LEFT JOIN messages m ON c.id = m.conversation_id
GROUP BY c.id;

CREATE UNIQUE INDEX idx_conversation_stats ON conversation_stats(conversation_id);

-- Function to refresh conversation stats
CREATE OR REPLACE FUNCTION refresh_conversation_stats()
RETURNS void AS $$
BEGIN
  REFRESH MATERIALIZED VIEW CONCURRENTLY conversation_stats;
END;
$$ LANGUAGE plpgsql;

-- Comments for documentation
COMMENT ON TABLE conversations IS 'Chat conversations between users';
COMMENT ON TABLE messages IS 'Individual messages within conversations';
COMMENT ON TABLE message_reactions IS 'Emoji reactions to messages';
COMMENT ON TABLE message_attachments IS 'File attachments for messages';
COMMENT ON MATERIALIZED VIEW conversation_stats IS 'Statistics and metrics for conversations';
