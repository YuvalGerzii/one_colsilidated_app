-- ============================================================================
-- Market Data Schema Extension for Portfolio Dashboard
-- Integrates with Financial Datasets MCP Server
-- ============================================================================

-- Table: public_comparables
-- Stores list of public companies used as comparables for portfolio companies
CREATE TABLE IF NOT EXISTS public_comparables (
    comparable_id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL UNIQUE,
    company_name VARCHAR(255) NOT NULL,
    industry VARCHAR(100),
    sector VARCHAR(100),
    market_cap DECIMAL(20, 2),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: market_financials
-- Stores financial data for public comparables (from MCP server)
CREATE TABLE IF NOT EXISTS market_financials (
    market_financial_id SERIAL PRIMARY KEY,
    comparable_id INTEGER REFERENCES public_comparables(comparable_id) ON DELETE CASCADE,
    period_type VARCHAR(20) NOT NULL, -- 'annual', 'quarterly', 'ttm'
    period_end_date DATE NOT NULL,
    
    -- Income Statement Items
    revenue DECIMAL(20, 2),
    gross_profit DECIMAL(20, 2),
    operating_income DECIMAL(20, 2),
    ebitda DECIMAL(20, 2),
    ebit DECIMAL(20, 2),
    net_income DECIMAL(20, 2),
    
    -- Balance Sheet Items
    total_assets DECIMAL(20, 2),
    total_liabilities DECIMAL(20, 2),
    total_equity DECIMAL(20, 2),
    cash_and_equivalents DECIMAL(20, 2),
    total_debt DECIMAL(20, 2),
    
    -- Margins
    gross_margin DECIMAL(10, 4),
    operating_margin DECIMAL(10, 4),
    ebitda_margin DECIMAL(10, 4),
    net_margin DECIMAL(10, 4),
    
    -- Metadata
    data_source VARCHAR(50) DEFAULT 'mcp_financial_datasets',
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(comparable_id, period_type, period_end_date)
);

-- Table: market_prices
-- Stores historical stock prices for comparables
CREATE TABLE IF NOT EXISTS market_prices (
    price_id SERIAL PRIMARY KEY,
    comparable_id INTEGER REFERENCES public_comparables(comparable_id) ON DELETE CASCADE,
    price_date DATE NOT NULL,
    open_price DECIMAL(10, 2),
    high_price DECIMAL(10, 2),
    low_price DECIMAL(10, 2),
    close_price DECIMAL(10, 2),
    volume BIGINT,
    adjusted_close DECIMAL(10, 2),
    
    -- Metadata
    data_source VARCHAR(50) DEFAULT 'mcp_financial_datasets',
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(comparable_id, price_date)
);

-- Table: valuation_multiples
-- Stores calculated valuation multiples for comparables
CREATE TABLE IF NOT EXISTS valuation_multiples (
    multiple_id SERIAL PRIMARY KEY,
    comparable_id INTEGER REFERENCES public_comparables(comparable_id) ON DELETE CASCADE,
    as_of_date DATE NOT NULL,
    
    -- Enterprise Value Components
    market_cap DECIMAL(20, 2),
    enterprise_value DECIMAL(20, 2),
    
    -- Revenue Multiples
    ev_revenue DECIMAL(10, 2),
    price_to_sales DECIMAL(10, 2),
    
    -- EBITDA Multiples
    ev_ebitda DECIMAL(10, 2),
    price_to_ebitda DECIMAL(10, 2),
    
    -- Earnings Multiples
    pe_ratio DECIMAL(10, 2),
    peg_ratio DECIMAL(10, 2),
    
    -- Book Value Multiples
    price_to_book DECIMAL(10, 2),
    ev_to_book DECIMAL(10, 2),
    
    -- Metadata
    calculation_method VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(comparable_id, as_of_date)
);

-- Table: company_comparable_mapping
-- Maps portfolio companies to their public comparables
CREATE TABLE IF NOT EXISTS company_comparable_mapping (
    mapping_id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES companies(company_id) ON DELETE CASCADE,
    comparable_id INTEGER REFERENCES public_comparables(comparable_id) ON DELETE CASCADE,
    relevance_score DECIMAL(3, 2), -- 0.00 to 1.00
    notes TEXT,
    is_primary BOOLEAN DEFAULT FALSE, -- Flag for primary comparable
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(company_id, comparable_id)
);

-- Table: industry_benchmarks
-- Stores calculated industry benchmark statistics
CREATE TABLE IF NOT EXISTS industry_benchmarks (
    benchmark_id SERIAL PRIMARY KEY,
    industry VARCHAR(100) NOT NULL,
    sector VARCHAR(100),
    as_of_date DATE NOT NULL,
    
    -- Multiple Statistics (median, mean, min, max)
    ev_revenue_median DECIMAL(10, 2),
    ev_revenue_mean DECIMAL(10, 2),
    ev_revenue_min DECIMAL(10, 2),
    ev_revenue_max DECIMAL(10, 2),
    
    ev_ebitda_median DECIMAL(10, 2),
    ev_ebitda_mean DECIMAL(10, 2),
    ev_ebitda_min DECIMAL(10, 2),
    ev_ebitda_max DECIMAL(10, 2),
    
    pe_ratio_median DECIMAL(10, 2),
    pe_ratio_mean DECIMAL(10, 2),
    pe_ratio_min DECIMAL(10, 2),
    pe_ratio_max DECIMAL(10, 2),
    
    ebitda_margin_median DECIMAL(10, 4),
    ebitda_margin_mean DECIMAL(10, 4),
    ebitda_margin_min DECIMAL(10, 4),
    ebitda_margin_max DECIMAL(10, 4),
    
    -- Sample Size
    comparable_count INTEGER,
    
    -- Metadata
    calculation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(industry, sector, as_of_date)
);

-- Table: valuation_validation_log
-- Logs validation of portfolio company valuations against market
CREATE TABLE IF NOT EXISTS valuation_validation_log (
    validation_id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES companies(company_id) ON DELETE CASCADE,
    valuation_date DATE NOT NULL,
    
    -- Portfolio Company Metrics
    portfolio_revenue DECIMAL(20, 2),
    portfolio_ebitda DECIMAL(20, 2),
    portfolio_enterprise_value DECIMAL(20, 2),
    portfolio_ev_revenue DECIMAL(10, 2),
    portfolio_ev_ebitda DECIMAL(10, 2),
    
    -- Market Benchmark Comparison
    market_ev_revenue_median DECIMAL(10, 2),
    market_ev_ebitda_median DECIMAL(10, 2),
    ev_revenue_vs_market_pct DECIMAL(10, 2), -- % above/below market
    ev_ebitda_vs_market_pct DECIMAL(10, 2),
    
    -- Assessment
    valuation_flag VARCHAR(50), -- 'Above Market', 'At Market', 'Below Market'
    assessment_summary TEXT,
    
    -- Metadata
    validated_by VARCHAR(100),
    validated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: mcp_api_usage_log
-- Tracks API calls to Financial Datasets MCP server
CREATE TABLE IF NOT EXISTS mcp_api_usage_log (
    log_id SERIAL PRIMARY KEY,
    endpoint VARCHAR(255) NOT NULL,
    ticker VARCHAR(10),
    request_params JSONB,
    response_status INTEGER,
    response_time_ms INTEGER,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- INDEXES for Performance
-- ============================================================================

-- Comparables
CREATE INDEX idx_comparables_ticker ON public_comparables(ticker);
CREATE INDEX idx_comparables_industry ON public_comparables(industry);
CREATE INDEX idx_comparables_sector ON public_comparables(sector);

-- Market Financials
CREATE INDEX idx_market_financials_comp_id ON market_financials(comparable_id);
CREATE INDEX idx_market_financials_period ON market_financials(period_end_date);
CREATE INDEX idx_market_financials_type ON market_financials(period_type);

-- Market Prices
CREATE INDEX idx_market_prices_comp_id ON market_prices(comparable_id);
CREATE INDEX idx_market_prices_date ON market_prices(price_date);

-- Valuation Multiples
CREATE INDEX idx_valuation_multiples_comp_id ON valuation_multiples(comparable_id);
CREATE INDEX idx_valuation_multiples_date ON valuation_multiples(as_of_date);

-- Company Comparable Mapping
CREATE INDEX idx_company_comparable_company ON company_comparable_mapping(company_id);
CREATE INDEX idx_company_comparable_comparable ON company_comparable_mapping(comparable_id);
CREATE INDEX idx_company_comparable_primary ON company_comparable_mapping(company_id, is_primary) WHERE is_primary = TRUE;

-- Industry Benchmarks
CREATE INDEX idx_industry_benchmarks_industry ON industry_benchmarks(industry);
CREATE INDEX idx_industry_benchmarks_sector ON industry_benchmarks(sector);
CREATE INDEX idx_industry_benchmarks_date ON industry_benchmarks(as_of_date);

-- Valuation Validation Log
CREATE INDEX idx_validation_log_company ON valuation_validation_log(company_id);
CREATE INDEX idx_validation_log_date ON valuation_validation_log(valuation_date);

-- MCP API Log
CREATE INDEX idx_mcp_log_endpoint ON mcp_api_usage_log(endpoint);
CREATE INDEX idx_mcp_log_ticker ON mcp_api_usage_log(ticker);
CREATE INDEX idx_mcp_log_created ON mcp_api_usage_log(created_at);

-- ============================================================================
-- VIEWS for Common Queries
-- ============================================================================

-- View: Latest comparable multiples
CREATE OR REPLACE VIEW v_latest_comparable_multiples AS
SELECT 
    c.ticker,
    c.company_name,
    c.industry,
    c.sector,
    vm.as_of_date,
    vm.market_cap,
    vm.enterprise_value,
    vm.ev_revenue,
    vm.ev_ebitda,
    vm.pe_ratio
FROM public_comparables c
JOIN valuation_multiples vm ON c.comparable_id = vm.comparable_id
WHERE vm.as_of_date = (
    SELECT MAX(as_of_date) 
    FROM valuation_multiples 
    WHERE comparable_id = c.comparable_id
)
AND c.is_active = TRUE;

-- View: Company with primary comparables
CREATE OR REPLACE VIEW v_company_primary_comparables AS
SELECT 
    co.company_id,
    co.company_name AS portfolio_company,
    pc.ticker,
    pc.company_name AS comparable_company,
    pc.industry,
    pc.sector,
    ccm.relevance_score,
    vm.ev_revenue,
    vm.ev_ebitda,
    vm.pe_ratio,
    vm.as_of_date
FROM companies co
JOIN company_comparable_mapping ccm ON co.company_id = ccm.company_id
JOIN public_comparables pc ON ccm.comparable_id = pc.comparable_id
LEFT JOIN valuation_multiples vm ON pc.comparable_id = vm.comparable_id
    AND vm.as_of_date = (
        SELECT MAX(as_of_date) 
        FROM valuation_multiples 
        WHERE comparable_id = pc.comparable_id
    )
WHERE ccm.is_primary = TRUE;

-- View: Latest industry benchmarks
CREATE OR REPLACE VIEW v_latest_industry_benchmarks AS
SELECT 
    industry,
    sector,
    as_of_date,
    ev_revenue_median,
    ev_revenue_mean,
    ev_ebitda_median,
    ev_ebitda_mean,
    pe_ratio_median,
    pe_ratio_mean,
    ebitda_margin_median,
    comparable_count
FROM industry_benchmarks
WHERE as_of_date = (
    SELECT MAX(as_of_date)
    FROM industry_benchmarks ib2
    WHERE ib2.industry = industry_benchmarks.industry
)
ORDER BY industry, sector;

-- ============================================================================
-- SAMPLE DATA (Optional - for testing)
-- ============================================================================

-- Insert sample public comparables
INSERT INTO public_comparables (ticker, company_name, industry, sector, market_cap) VALUES
('AAPL', 'Apple Inc.', 'Technology Hardware', 'Technology', 2800000000000),
('MSFT', 'Microsoft Corporation', 'Software', 'Technology', 2400000000000),
('GOOGL', 'Alphabet Inc.', 'Internet Services', 'Technology', 1700000000000),
('META', 'Meta Platforms Inc.', 'Social Media', 'Technology', 900000000000),
('NVDA', 'NVIDIA Corporation', 'Semiconductors', 'Technology', 1100000000000)
ON CONFLICT (ticker) DO NOTHING;

-- ============================================================================
-- FUNCTIONS
-- ============================================================================

-- Function: Get latest multiples for a comparable
CREATE OR REPLACE FUNCTION get_latest_multiples(p_ticker VARCHAR)
RETURNS TABLE (
    ticker VARCHAR,
    as_of_date DATE,
    ev_revenue DECIMAL,
    ev_ebitda DECIMAL,
    pe_ratio DECIMAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.ticker,
        vm.as_of_date,
        vm.ev_revenue,
        vm.ev_ebitda,
        vm.pe_ratio
    FROM public_comparables c
    JOIN valuation_multiples vm ON c.comparable_id = vm.comparable_id
    WHERE c.ticker = p_ticker
    ORDER BY vm.as_of_date DESC
    LIMIT 1;
END;
$$ LANGUAGE plpgsql;

-- Function: Calculate industry benchmark
CREATE OR REPLACE FUNCTION calculate_industry_benchmark(
    p_industry VARCHAR,
    p_sector VARCHAR DEFAULT NULL
) RETURNS TABLE (
    ev_revenue_median DECIMAL,
    ev_ebitda_median DECIMAL,
    pe_ratio_median DECIMAL,
    comparable_count INTEGER
) AS $$
BEGIN
    RETURN QUERY
    WITH recent_multiples AS (
        SELECT 
            c.comparable_id,
            vm.ev_revenue,
            vm.ev_ebitda,
            vm.pe_ratio
        FROM public_comparables c
        JOIN valuation_multiples vm ON c.comparable_id = vm.comparable_id
        WHERE c.industry = p_industry
            AND (p_sector IS NULL OR c.sector = p_sector)
            AND vm.as_of_date = (
                SELECT MAX(as_of_date)
                FROM valuation_multiples
                WHERE comparable_id = c.comparable_id
            )
    )
    SELECT 
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY ev_revenue) AS ev_revenue_median,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY ev_ebitda) AS ev_ebitda_median,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY pe_ratio) AS pe_ratio_median,
        COUNT(*)::INTEGER AS comparable_count
    FROM recent_multiples;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- GRANTS (Adjust based on your user roles)
-- ============================================================================

-- GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO dashboard_user;
-- GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO dashboard_user;
-- GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO dashboard_user;
