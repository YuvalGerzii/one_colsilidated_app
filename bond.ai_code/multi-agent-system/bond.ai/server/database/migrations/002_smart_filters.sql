-- Smart Match Filters & Preferences Migration
-- Implements storage for user filter preferences and ML-based suggestions

-- Filter preferences table
CREATE TABLE IF NOT EXISTS filter_preferences (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  name VARCHAR(100) NOT NULL DEFAULT 'default',
  criteria JSONB NOT NULL,
  auto_apply BOOLEAN DEFAULT true,
  save_as_default BOOLEAN DEFAULT false,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

  UNIQUE(user_id, name)
);

CREATE INDEX idx_filter_preferences_user_id ON filter_preferences(user_id);
CREATE INDEX idx_filter_preferences_active ON filter_preferences(is_active) WHERE is_active = true;
CREATE INDEX idx_filter_preferences_criteria ON filter_preferences USING GIN(criteria);

-- Filter usage log for ML learning
CREATE TABLE IF NOT EXISTS filter_usage_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  criteria JSONB NOT NULL,
  result_count INTEGER NOT NULL,
  timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_filter_usage_user_id ON filter_usage_log(user_id);
CREATE INDEX idx_filter_usage_timestamp ON filter_usage_log(timestamp DESC);
CREATE INDEX idx_filter_usage_criteria ON filter_usage_log USING GIN(criteria);

-- Saved filter sets (for quick access)
CREATE TABLE IF NOT EXISTS saved_filters (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  name VARCHAR(100) NOT NULL,
  description TEXT,
  criteria JSONB NOT NULL,
  usage_count INTEGER DEFAULT 0,
  last_used_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

  UNIQUE(user_id, name)
);

CREATE INDEX idx_saved_filters_user_id ON saved_filters(user_id);
CREATE INDEX idx_saved_filters_last_used ON saved_filters(last_used_at DESC);

-- Filter suggestions cache (for performance)
CREATE TABLE IF NOT EXISTS filter_suggestions_cache (
  user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
  suggestions JSONB NOT NULL,
  generated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  expires_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() + INTERVAL '24 hours'
);

CREATE INDEX idx_filter_suggestions_expires ON filter_suggestions_cache(expires_at);

-- Materialized view for filter analytics
CREATE MATERIALIZED VIEW IF NOT EXISTS filter_analytics AS
SELECT
  fu.user_id,
  COUNT(*) as total_searches,
  AVG(fu.result_count) as avg_results,
  jsonb_object_agg(
    filter_key,
    filter_value
  ) FILTER (WHERE filter_key IS NOT NULL) as common_filters
FROM filter_usage_log fu
CROSS JOIN LATERAL jsonb_each(fu.criteria) AS filters(filter_key, filter_value)
WHERE fu.timestamp > NOW() - INTERVAL '30 days'
GROUP BY fu.user_id;

CREATE UNIQUE INDEX idx_filter_analytics_user ON filter_analytics(user_id);

-- Function to refresh filter analytics
CREATE OR REPLACE FUNCTION refresh_filter_analytics()
RETURNS void AS $$
BEGIN
  REFRESH MATERIALIZED VIEW CONCURRENTLY filter_analytics;
END;
$$ LANGUAGE plpgsql;

-- Comments for documentation
COMMENT ON TABLE filter_preferences IS 'Stores user filter preferences with auto-apply and ML-based suggestions';
COMMENT ON TABLE filter_usage_log IS 'Tracks filter usage patterns for machine learning recommendations';
COMMENT ON TABLE saved_filters IS 'User-created named filter sets for quick access';
COMMENT ON TABLE filter_suggestions_cache IS 'Cached ML-generated filter suggestions for performance';
COMMENT ON MATERIALIZED VIEW filter_analytics IS 'Analytics on user filter usage patterns';
