-- Advanced Search System Migration
-- Hybrid search with full-text search and semantic vectors

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS pg_trgm;  -- For fuzzy matching
CREATE EXTENSION IF NOT EXISTS vector;   -- For semantic search

-- Search index table (denormalized for performance)
CREATE TABLE IF NOT EXISTS search_index (
  id UUID NOT NULL,
  type VARCHAR(20) NOT NULL CHECK (type IN ('user', 'match', 'need', 'offering')),
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  industry VARCHAR(100),
  location_text VARCHAR(255),
  match_type VARCHAR(50),
  metadata JSONB DEFAULT '{}',
  search_vector tsvector,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

  PRIMARY KEY (id, type)
);

-- Full-text search index
CREATE INDEX idx_search_vector ON search_index USING GIN(search_vector);

-- Fuzzy matching index (pg_trgm)
CREATE INDEX idx_search_title_trgm ON search_index USING GIN(title gin_trgm_ops);
CREATE INDEX idx_search_description_trgm ON search_index USING GIN(description gin_trgm_ops);

-- Regular indexes for filtering
CREATE INDEX idx_search_type ON search_index(type);
CREATE INDEX idx_search_industry ON search_index(industry);
CREATE INDEX idx_search_location ON search_index(location_text);
CREATE INDEX idx_search_match_type ON search_index(match_type);

-- Composite index for common filters
CREATE INDEX idx_search_type_industry ON search_index(type, industry);

-- Update embeddings table to add vector index
CREATE INDEX IF NOT EXISTS idx_embeddings_vector ON embeddings
  USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);  -- Adjust based on data size

-- Index for entity lookups
CREATE INDEX IF NOT EXISTS idx_embeddings_entity ON embeddings(entity_id, entity_type);

-- Function to automatically update search_vector
CREATE OR REPLACE FUNCTION update_search_vector()
RETURNS TRIGGER AS $$
BEGIN
  NEW.search_vector = to_tsvector('english', COALESCE(NEW.title, '') || ' ' || COALESCE(NEW.description, ''));
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to update search_vector on insert/update
CREATE TRIGGER trigger_update_search_vector
BEFORE INSERT OR UPDATE ON search_index
FOR EACH ROW
EXECUTE FUNCTION update_search_vector();

-- Search analytics table
CREATE TABLE IF NOT EXISTS search_analytics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  query TEXT NOT NULL,
  search_mode VARCHAR(20) NOT NULL,
  filters JSONB,
  result_count INTEGER NOT NULL,
  response_time INTEGER NOT NULL,  -- milliseconds
  clicked_result_id UUID,
  clicked_result_type VARCHAR(20),
  timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_search_analytics_user ON search_analytics(user_id);
CREATE INDEX idx_search_analytics_timestamp ON search_analytics(timestamp DESC);
CREATE INDEX idx_search_analytics_query ON search_analytics USING GIN(to_tsvector('english', query));

-- Popular searches materialized view
CREATE MATERIALIZED VIEW IF NOT EXISTS popular_searches AS
SELECT
  query,
  COUNT(*) as search_count,
  AVG(result_count) as avg_results,
  AVG(response_time) as avg_response_time,
  COUNT(clicked_result_id) as click_count
FROM search_analytics
WHERE timestamp > NOW() - INTERVAL '30 days'
GROUP BY query
HAVING COUNT(*) >= 5
ORDER BY search_count DESC
LIMIT 100;

CREATE UNIQUE INDEX idx_popular_searches_query ON popular_searches(query);

-- Function to refresh popular searches
CREATE OR REPLACE FUNCTION refresh_popular_searches()
RETURNS void AS $$
BEGIN
  REFRESH MATERIALIZED VIEW CONCURRENTLY popular_searches;
END;
$$ LANGUAGE plpgsql;

-- Search suggestions table (for autocomplete)
CREATE TABLE IF NOT EXISTS search_suggestions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  suggestion TEXT UNIQUE NOT NULL,
  category VARCHAR(50),
  weight INTEGER DEFAULT 1,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_search_suggestions_text ON search_suggestions USING GIN(to_tsvector('english', suggestion));
CREATE INDEX idx_search_suggestions_trgm ON search_suggestions USING GIN(suggestion gin_trgm_ops);
CREATE INDEX idx_search_suggestions_category ON search_suggestions(category);

-- Function to get autocomplete suggestions
CREATE OR REPLACE FUNCTION get_search_suggestions(query_text TEXT, max_results INTEGER DEFAULT 10)
RETURNS TABLE(suggestion TEXT, category VARCHAR, score FLOAT) AS $$
BEGIN
  RETURN QUERY
  SELECT
    s.suggestion,
    s.category,
    similarity(s.suggestion, query_text) as score
  FROM search_suggestions s
  WHERE s.suggestion % query_text
  ORDER BY similarity(s.suggestion, query_text) DESC, s.weight DESC
  LIMIT max_results;
END;
$$ LANGUAGE plpgsql;

-- Indexed search history for personalization
CREATE TABLE IF NOT EXISTS user_search_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  query TEXT NOT NULL,
  filters JSONB,
  timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_user_search_history_user ON user_search_history(user_id);
CREATE INDEX idx_user_search_history_timestamp ON user_search_history(timestamp DESC);

-- Function to get personalized search suggestions
CREATE OR REPLACE FUNCTION get_personalized_suggestions(p_user_id UUID, max_results INTEGER DEFAULT 5)
RETURNS TABLE(suggestion TEXT, frequency BIGINT) AS $$
BEGIN
  RETURN QUERY
  SELECT
    query as suggestion,
    COUNT(*) as frequency
  FROM user_search_history
  WHERE user_id = p_user_id
    AND timestamp > NOW() - INTERVAL '90 days'
  GROUP BY query
  ORDER BY COUNT(*) DESC, MAX(timestamp) DESC
  LIMIT max_results;
END;
$$ LANGUAGE plpgsql;

-- Comments for documentation
COMMENT ON TABLE search_index IS 'Denormalized search index for hybrid full-text and semantic search';
COMMENT ON TABLE search_analytics IS 'Analytics and metrics for search queries';
COMMENT ON TABLE search_suggestions IS 'Autocomplete suggestions for search';
COMMENT ON TABLE user_search_history IS 'User search history for personalization';
COMMENT ON MATERIALIZED VIEW popular_searches IS 'Most popular search queries';
