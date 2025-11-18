-- ============================================================================
-- REAL ESTATE MARKET DATA SCHEMA EXTENSION
-- For Portfolio Dashboard - Real Estate Market Intelligence
-- ============================================================================

-- Table 1: market_data
-- Stores time-series market metrics (cap rates, rents, occupancy, etc.)
CREATE TABLE IF NOT EXISTS market_data (
    market_data_id SERIAL PRIMARY KEY,
    
    -- Geography
    market_name VARCHAR(100) NOT NULL, -- 'NYC' or 'Miami'
    submarket_name VARCHAR(100), -- 'Manhattan', 'Brooklyn', 'Brickell', etc.
    
    -- Property Details
    property_type VARCHAR(50) NOT NULL, -- 'multifamily', 'office', 'retail', 'hotel', 'mixed-use'
    property_class VARCHAR(10), -- 'A', 'B', 'C', NULL for aggregated data
    
    -- Metric
    metric_name VARCHAR(100) NOT NULL, -- 'cap_rate', 'rent_psf', 'occupancy_rate', etc.
    metric_value DECIMAL(15, 4), -- Numeric value
    metric_unit VARCHAR(50), -- '%', '$/SF', '$/unit', 'count', etc.
    
    -- Time Period
    period DATE NOT NULL, -- YYYY-MM-DD format (use first of month)
    
    -- Data Quality
    data_source VARCHAR(255), -- Citation/source of data
    confidence_level VARCHAR(20), -- 'high', 'medium', 'low'
    
    -- Metadata
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT valid_market CHECK (market_name IN ('NYC', 'Miami')),
    CONSTRAINT valid_property_type CHECK (property_type IN ('multifamily', 'office', 'retail', 'hotel', 'mixed-use', 'sfr', 'land')),
    CONSTRAINT valid_class CHECK (property_class IN ('A', 'B', 'C', NULL)),
    CONSTRAINT valid_confidence CHECK (confidence_level IN ('high', 'medium', 'low', NULL))
);

-- Table 2: comp_transactions
-- Stores comparable sales transactions for valuation
CREATE TABLE IF NOT EXISTS comp_transactions (
    transaction_id SERIAL PRIMARY KEY,
    
    -- Property Location
    address VARCHAR(255),
    city VARCHAR(100) NOT NULL,
    submarket VARCHAR(100),
    state VARCHAR(50) DEFAULT 'NY', -- or 'FL'
    
    -- Property Details
    property_type VARCHAR(50) NOT NULL,
    property_class VARCHAR(10),
    
    -- Transaction Details
    sale_date DATE NOT NULL,
    sale_price DECIMAL(20, 2), -- Total sale price
    
    -- Pricing Metrics
    price_per_unit DECIMAL(15, 2), -- For multifamily/hotel
    price_per_sf DECIMAL(15, 2), -- $/SF
    cap_rate DECIMAL(5, 4), -- As decimal (e.g., 0.0550 for 5.50%)
    
    -- Property Specs
    units INTEGER, -- For multifamily/hotel
    total_sf INTEGER, -- Total square footage
    year_built INTEGER,
    
    -- Transaction Parties
    buyer VARCHAR(255),
    seller VARCHAR(255),
    
    -- Additional Info
    financing_type VARCHAR(100), -- 'Cash', 'Financed', 'Assumption', etc.
    occupancy_at_sale DECIMAL(5, 4), -- As decimal (e.g., 0.92 for 92%)
    deal_type VARCHAR(100), -- 'Arms Length', 'Portfolio', 'Distressed', etc.
    
    -- Data Source
    data_source VARCHAR(255),
    source_url TEXT,
    
    -- Metadata
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 3: economic_indicators
-- Stores macroeconomic and demographic data by geography
CREATE TABLE IF NOT EXISTS economic_indicators (
    indicator_id SERIAL PRIMARY KEY,
    
    -- Geography
    geography VARCHAR(100) NOT NULL, -- 'NYC Metro', 'Miami Metro', 'Manhattan', etc.
    geography_type VARCHAR(50), -- 'Metro', 'City', 'County', 'Borough', 'State'
    
    -- Indicator
    indicator_name VARCHAR(100) NOT NULL, -- 'population', 'employment', 'median_income', etc.
    indicator_value DECIMAL(20, 4),
    indicator_unit VARCHAR(50), -- 'count', 'USD', '%', 'index', etc.
    
    -- Time Period
    period DATE NOT NULL, -- YYYY-MM-DD format
    period_type VARCHAR(20), -- 'monthly', 'quarterly', 'annual'
    
    -- Data Source
    data_source VARCHAR(255), -- 'US Census', 'BLS', 'Local Planning Dept', etc.
    
    -- Metadata
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================================

-- market_data indexes
CREATE INDEX idx_market_data_market ON market_data(market_name);
CREATE INDEX idx_market_data_submarket ON market_data(submarket_name);
CREATE INDEX idx_market_data_type ON market_data(property_type, property_class);
CREATE INDEX idx_market_data_metric ON market_data(metric_name);
CREATE INDEX idx_market_data_period ON market_data(period);
CREATE INDEX idx_market_data_composite ON market_data(market_name, property_type, metric_name, period);

-- comp_transactions indexes
CREATE INDEX idx_comp_trans_city ON comp_transactions(city);
CREATE INDEX idx_comp_trans_type ON comp_transactions(property_type, property_class);
CREATE INDEX idx_comp_trans_date ON comp_transactions(sale_date);
CREATE INDEX idx_comp_trans_price ON comp_transactions(price_per_sf, price_per_unit);

-- economic_indicators indexes
CREATE INDEX idx_econ_geography ON economic_indicators(geography);
CREATE INDEX idx_econ_indicator ON economic_indicators(indicator_name);
CREATE INDEX idx_econ_period ON economic_indicators(period);
CREATE INDEX idx_econ_composite ON economic_indicators(geography, indicator_name, period);

-- ============================================================================
-- VIEWS FOR COMMON QUERIES
-- ============================================================================

-- View: Latest Cap Rates by Market
CREATE OR REPLACE VIEW v_latest_cap_rates AS
WITH ranked_data AS (
    SELECT 
        market_name,
        submarket_name,
        property_type,
        property_class,
        metric_value AS cap_rate,
        period,
        data_source,
        ROW_NUMBER() OVER (
            PARTITION BY market_name, submarket_name, property_type, property_class 
            ORDER BY period DESC
        ) as rn
    FROM market_data
    WHERE metric_name = 'cap_rate'
        AND metric_value IS NOT NULL
)
SELECT 
    market_name,
    submarket_name,
    property_type,
    property_class,
    cap_rate,
    period AS as_of_date,
    data_source
FROM ranked_data
WHERE rn = 1
ORDER BY market_name, submarket_name, property_type, property_class;

-- View: Recent Comparable Transactions (Last 12 months)
CREATE OR REPLACE VIEW v_recent_comp_transactions AS
SELECT 
    transaction_id,
    address,
    city,
    submarket,
    property_type,
    property_class,
    sale_date,
    sale_price,
    price_per_unit,
    price_per_sf,
    cap_rate,
    units,
    total_sf,
    buyer,
    seller
FROM comp_transactions
WHERE sale_date >= CURRENT_DATE - INTERVAL '12 months'
ORDER BY sale_date DESC;

-- View: Economic Indicators Summary (Latest Values)
CREATE OR REPLACE VIEW v_latest_economic_indicators AS
WITH ranked_indicators AS (
    SELECT 
        geography,
        indicator_name,
        indicator_value,
        indicator_unit,
        period,
        data_source,
        ROW_NUMBER() OVER (
            PARTITION BY geography, indicator_name 
            ORDER BY period DESC
        ) as rn
    FROM economic_indicators
)
SELECT 
    geography,
    indicator_name,
    indicator_value,
    indicator_unit,
    period AS as_of_date,
    data_source
FROM ranked_indicators
WHERE rn = 1
ORDER BY geography, indicator_name;

-- ============================================================================
-- HELPER FUNCTIONS
-- ============================================================================

-- Function: Get Market Data for Specific Property Type
CREATE OR REPLACE FUNCTION get_market_metrics(
    p_market VARCHAR,
    p_property_type VARCHAR,
    p_metric_name VARCHAR,
    p_start_date DATE DEFAULT NULL,
    p_end_date DATE DEFAULT CURRENT_DATE
) RETURNS TABLE (
    submarket VARCHAR,
    property_class VARCHAR,
    metric_value DECIMAL,
    period DATE
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        md.submarket_name,
        md.property_class,
        md.metric_value,
        md.period
    FROM market_data md
    WHERE md.market_name = p_market
        AND md.property_type = p_property_type
        AND md.metric_name = p_metric_name
        AND (p_start_date IS NULL OR md.period >= p_start_date)
        AND md.period <= p_end_date
    ORDER BY md.period DESC, md.submarket_name, md.property_class;
END;
$$ LANGUAGE plpgsql;

-- Function: Calculate Average Cap Rate by Market
CREATE OR REPLACE FUNCTION avg_cap_rate_by_market(
    p_market VARCHAR,
    p_property_type VARCHAR DEFAULT NULL,
    p_start_date DATE DEFAULT CURRENT_DATE - INTERVAL '12 months'
) RETURNS TABLE (
    market VARCHAR,
    property_type VARCHAR,
    avg_cap_rate DECIMAL,
    min_cap_rate DECIMAL,
    max_cap_rate DECIMAL,
    data_points INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        md.market_name,
        md.property_type,
        AVG(md.metric_value) AS avg_cap_rate,
        MIN(md.metric_value) AS min_cap_rate,
        MAX(md.metric_value) AS max_cap_rate,
        COUNT(*)::INTEGER AS data_points
    FROM market_data md
    WHERE md.market_name = p_market
        AND md.metric_name = 'cap_rate'
        AND (p_property_type IS NULL OR md.property_type = p_property_type)
        AND md.period >= p_start_date
        AND md.metric_value IS NOT NULL
    GROUP BY md.market_name, md.property_type
    ORDER BY md.property_type;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- SAMPLE QUERIES
-- ============================================================================

-- Query 1: Get latest multifamily cap rates for NYC
-- SELECT * FROM v_latest_cap_rates 
-- WHERE market_name = 'NYC' AND property_type = 'multifamily';

-- Query 2: Get recent Manhattan office transactions
-- SELECT * FROM v_recent_comp_transactions
-- WHERE city = 'Manhattan' AND property_type = 'office'
-- ORDER BY sale_date DESC
-- LIMIT 10;

-- Query 3: Get population and employment trends for Miami
-- SELECT * FROM economic_indicators
-- WHERE geography = 'Miami Metro'
--   AND indicator_name IN ('population', 'employment')
-- ORDER BY period DESC;

-- Query 4: Compare cap rates between NYC and Miami for Class A multifamily
-- SELECT 
--     market_name,
--     AVG(metric_value) as avg_cap_rate,
--     COUNT(*) as data_points
-- FROM market_data
-- WHERE property_type = 'multifamily'
--   AND property_class = 'A'
--   AND metric_name = 'cap_rate'
--   AND period >= CURRENT_DATE - INTERVAL '6 months'
-- GROUP BY market_name;

-- ============================================================================
-- GRANTS (Adjust based on your user roles)
-- ============================================================================

-- Example grants (uncomment and modify as needed):
-- GRANT SELECT, INSERT, UPDATE ON market_data TO dashboard_user;
-- GRANT SELECT, INSERT, UPDATE ON comp_transactions TO dashboard_user;
-- GRANT SELECT, INSERT, UPDATE ON economic_indicators TO dashboard_user;
-- GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO dashboard_user;
-- GRANT SELECT ON ALL TABLES IN SCHEMA public TO dashboard_viewer;
