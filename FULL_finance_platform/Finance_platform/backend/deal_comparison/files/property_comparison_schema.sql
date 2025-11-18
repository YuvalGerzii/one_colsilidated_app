-- =====================================================
-- PROPERTY COMPARISON TOOL - DATABASE SCHEMA
-- =====================================================
-- Purpose: Store and compare real estate deals from multiple model types
-- Supports: Multifamily, Mixed-Use, Hotel, SFR, House Flipping
-- Created: November 4, 2025

-- =====================================================
-- DROP EXISTING TABLES (for fresh install)
-- =====================================================

DROP TABLE IF EXISTS comparison_metrics CASCADE;
DROP TABLE IF EXISTS property_deals CASCADE;
DROP TABLE IF EXISTS comparison_sets CASCADE;
DROP TABLE IF EXISTS scoring_criteria CASCADE;
DROP TABLE IF EXISTS deal_scores CASCADE;

-- =====================================================
-- COMPARISON SETS (Groups of deals to compare)
-- =====================================================

CREATE TABLE comparison_sets (
    comparison_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    comparison_name VARCHAR(255) NOT NULL,
    comparison_description TEXT,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by UUID, -- References users(user_id) from main schema
    
    -- Status
    status VARCHAR(50) DEFAULT 'Draft', -- Draft, Active, Archived
    
    -- Settings
    primary_metric VARCHAR(50) DEFAULT 'levered_irr', -- Primary sort metric
    
    CONSTRAINT valid_status CHECK (status IN ('Draft', 'Active', 'Archived'))
);

-- =====================================================
-- PROPERTY DEALS (Individual deals to compare)
-- =====================================================

CREATE TABLE property_deals (
    deal_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    comparison_id UUID REFERENCES comparison_sets(comparison_id) ON DELETE CASCADE,
    
    -- Basic Info
    property_name VARCHAR(255) NOT NULL,
    property_address TEXT,
    property_type VARCHAR(50) NOT NULL, -- Multifamily, Mixed-Use, Hotel, SFR, House Flipping
    property_subtype VARCHAR(50), -- Class A/B/C, or specific strategy
    
    -- Location
    city VARCHAR(100),
    state VARCHAR(50),
    submarket VARCHAR(100),
    
    -- Size
    total_sf DECIMAL(12, 2),
    units INTEGER, -- For multifamily/hotel
    land_acres DECIMAL(10, 4),
    
    -- Source Model
    source_model_type VARCHAR(50) NOT NULL, -- Which Excel model this came from
    source_file_path TEXT,
    source_file_id UUID, -- References documents table
    import_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Key Dates
    acquisition_date DATE,
    stabilization_date DATE,
    exit_date DATE,
    hold_period_years DECIMAL(5, 2),
    
    -- Status
    deal_status VARCHAR(50) DEFAULT 'Active', -- Active, On Hold, Passed, Closed
    
    -- Notes
    deal_notes TEXT,
    strengths TEXT,
    concerns TEXT,
    
    -- Rankings (calculated)
    overall_rank INTEGER,
    risk_adjusted_rank INTEGER,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT valid_property_type CHECK (property_type IN 
        ('Multifamily', 'Mixed-Use', 'Hotel', 'SFR', 'House Flipping', 'Office', 'Retail', 'Industrial')),
    CONSTRAINT valid_deal_status CHECK (deal_status IN 
        ('Active', 'On Hold', 'Passed', 'Closed', 'Under Review'))
);

-- =====================================================
-- COMPARISON METRICS (Standardized metrics for all deals)
-- =====================================================

CREATE TABLE comparison_metrics (
    metric_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    deal_id UUID NOT NULL REFERENCES property_deals(deal_id) ON DELETE CASCADE,
    
    -- RETURNS METRICS
    levered_irr DECIMAL(8, 4), -- Levered IRR (%)
    unlevered_irr DECIMAL(8, 4), -- Unlevered IRR (%)
    equity_multiple DECIMAL(8, 4), -- MOIC
    cash_on_cash_y1 DECIMAL(8, 4), -- Year 1 Cash-on-Cash (%)
    cash_on_cash_avg DECIMAL(8, 4), -- Average Cash-on-Cash (%)
    
    -- VALUATION METRICS
    entry_cap_rate DECIMAL(6, 4), -- Entry Cap Rate (%)
    exit_cap_rate DECIMAL(6, 4), -- Exit Cap Rate (%)
    cap_rate_spread DECIMAL(6, 4), -- Exit - Entry (bps)
    
    -- OPERATIONAL METRICS
    noi_year1 DECIMAL(15, 2), -- Year 1 NOI
    noi_stabilized DECIMAL(15, 2), -- Stabilized NOI
    noi_margin DECIMAL(6, 4), -- NOI Margin (%)
    noi_per_sf DECIMAL(10, 2), -- NOI per SF (for density comparison)
    noi_per_unit DECIMAL(10, 2), -- NOI per unit (multifamily/hotel)
    
    -- DEBT METRICS
    dscr_year1 DECIMAL(8, 4), -- Debt Service Coverage Ratio Y1
    dscr_min DECIMAL(8, 4), -- Minimum DSCR across hold period
    ltv DECIMAL(6, 4), -- Loan-to-Value (%)
    debt_yield DECIMAL(6, 4), -- Debt Yield (%)
    
    -- INVESTMENT SIZE
    purchase_price DECIMAL(15, 2),
    total_project_cost DECIMAL(15, 2),
    equity_required DECIMAL(15, 2),
    debt_amount DECIMAL(15, 2),
    
    -- PER-UNIT / PER-SF METRICS
    price_per_unit DECIMAL(10, 2), -- For multifamily/hotel
    price_per_sf DECIMAL(10, 2),
    renovation_per_unit DECIMAL(10, 2),
    
    -- REVENUE METRICS
    gross_revenue_year1 DECIMAL(15, 2),
    revenue_per_sf DECIMAL(10, 2),
    revenue_per_unit DECIMAL(10, 2),
    occupancy_stabilized DECIMAL(6, 4), -- Occupancy (%)
    
    -- EXIT METRICS
    gross_exit_value DECIMAL(15, 2),
    net_exit_proceeds DECIMAL(15, 2),
    gain_on_sale DECIMAL(15, 2),
    
    -- CALCULATED SCORES (0-100)
    returns_score DECIMAL(5, 2),
    risk_score DECIMAL(5, 2),
    location_score DECIMAL(5, 2),
    operational_score DECIMAL(5, 2),
    overall_score DECIMAL(5, 2),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- SCORING CRITERIA (Weighted scoring system)
-- =====================================================

CREATE TABLE scoring_criteria (
    criteria_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    comparison_id UUID REFERENCES comparison_sets(comparison_id) ON DELETE CASCADE,
    
    -- Criteria Category
    category VARCHAR(50) NOT NULL, -- Returns, Risk, Location, Operations
    criteria_name VARCHAR(100) NOT NULL,
    criteria_description TEXT,
    
    -- Weighting
    weight DECIMAL(5, 4) NOT NULL, -- Sum of all weights should equal 1.0
    
    -- Scoring Method
    metric_field VARCHAR(100) NOT NULL, -- Which field from comparison_metrics to use
    scoring_method VARCHAR(50) DEFAULT 'linear', -- linear, threshold, inverse
    
    -- Threshold Values (for scoring)
    excellent_threshold DECIMAL(15, 4), -- Score = 100
    good_threshold DECIMAL(15, 4), -- Score = 75
    acceptable_threshold DECIMAL(15, 4), -- Score = 50
    poor_threshold DECIMAL(15, 4), -- Score = 25
    
    -- Active Status
    is_active BOOLEAN DEFAULT TRUE,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT valid_category CHECK (category IN ('Returns', 'Risk', 'Location', 'Operations', 'Other')),
    CONSTRAINT weight_between_zero_one CHECK (weight >= 0 AND weight <= 1),
    CONSTRAINT valid_scoring_method CHECK (scoring_method IN ('linear', 'threshold', 'inverse', 'boolean'))
);

-- =====================================================
-- DEAL SCORES (Historical scoring results)
-- =====================================================

CREATE TABLE deal_scores (
    score_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    deal_id UUID NOT NULL REFERENCES property_deals(deal_id) ON DELETE CASCADE,
    criteria_id UUID NOT NULL REFERENCES scoring_criteria(criteria_id) ON DELETE CASCADE,
    
    -- Score Details
    raw_value DECIMAL(15, 4), -- Actual metric value
    normalized_score DECIMAL(5, 2), -- 0-100 score
    weighted_score DECIMAL(5, 2), -- Score * Weight
    
    -- Ranking
    rank_in_category INTEGER,
    percentile DECIMAL(5, 2),
    
    scored_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================

-- Comparison Sets
CREATE INDEX idx_comparison_sets_created ON comparison_sets(created_at DESC);
CREATE INDEX idx_comparison_sets_status ON comparison_sets(status);

-- Property Deals
CREATE INDEX idx_deals_comparison ON property_deals(comparison_id);
CREATE INDEX idx_deals_type ON property_deals(property_type);
CREATE INDEX idx_deals_status ON property_deals(deal_status);
CREATE INDEX idx_deals_location ON property_deals(city, state);
CREATE INDEX idx_deals_created ON property_deals(created_at DESC);

-- Comparison Metrics
CREATE INDEX idx_metrics_deal ON comparison_metrics(deal_id);
CREATE INDEX idx_metrics_irr ON comparison_metrics(levered_irr DESC);
CREATE INDEX idx_metrics_moic ON comparison_metrics(equity_multiple DESC);
CREATE INDEX idx_metrics_overall_score ON comparison_metrics(overall_score DESC);

-- Scoring Criteria
CREATE INDEX idx_criteria_comparison ON scoring_criteria(comparison_id);
CREATE INDEX idx_criteria_active ON scoring_criteria(is_active);

-- Deal Scores
CREATE INDEX idx_scores_deal ON deal_scores(deal_id);
CREATE INDEX idx_scores_criteria ON deal_scores(criteria_id);

-- =====================================================
-- VIEWS FOR COMMON QUERIES
-- =====================================================

-- Deal Comparison Summary View
CREATE VIEW v_deal_comparison_summary AS
SELECT 
    pd.deal_id,
    pd.property_name,
    pd.property_type,
    pd.city,
    pd.state,
    
    -- Key Metrics
    cm.levered_irr,
    cm.equity_multiple,
    cm.cash_on_cash_y1,
    cm.entry_cap_rate,
    cm.exit_cap_rate,
    cm.dscr_year1,
    
    -- Investment Size
    cm.equity_required,
    cm.total_project_cost,
    
    -- Scores
    cm.overall_score,
    cm.returns_score,
    cm.risk_score,
    
    -- Rankings
    pd.overall_rank,
    pd.risk_adjusted_rank,
    
    -- Status
    pd.deal_status,
    
    cs.comparison_name
FROM 
    property_deals pd
    JOIN comparison_metrics cm ON pd.deal_id = cm.deal_id
    JOIN comparison_sets cs ON pd.comparison_id = cs.comparison_id
ORDER BY 
    cm.overall_score DESC;

-- Top Deals by IRR
CREATE VIEW v_top_deals_by_irr AS
SELECT 
    pd.property_name,
    pd.property_type,
    pd.city,
    cm.levered_irr,
    cm.equity_multiple,
    cm.equity_required,
    cm.overall_score,
    pd.deal_status
FROM 
    property_deals pd
    JOIN comparison_metrics cm ON pd.deal_id = cm.deal_id
WHERE 
    pd.deal_status = 'Active'
ORDER BY 
    cm.levered_irr DESC
LIMIT 20;

-- Risk-Adjusted Rankings
CREATE VIEW v_risk_adjusted_rankings AS
SELECT 
    pd.property_name,
    pd.property_type,
    cm.levered_irr,
    cm.dscr_year1,
    cm.ltv,
    cm.risk_score,
    -- Risk-adjusted return = IRR * (Risk Score / 100)
    (cm.levered_irr * (cm.risk_score / 100.0)) AS risk_adjusted_irr,
    cm.overall_score
FROM 
    property_deals pd
    JOIN comparison_metrics cm ON pd.deal_id = cm.deal_id
WHERE 
    pd.deal_status = 'Active'
ORDER BY 
    (cm.levered_irr * (cm.risk_score / 100.0)) DESC;

-- =====================================================
-- DEFAULT SCORING CRITERIA (Insert standard criteria)
-- =====================================================

-- This will be inserted when a new comparison is created
-- Sample criteria for a typical PE real estate comparison
/*
INSERT INTO scoring_criteria (comparison_id, category, criteria_name, weight, metric_field, scoring_method, excellent_threshold, good_threshold, acceptable_threshold, poor_threshold)
VALUES
    -- RETURNS (40% weight)
    (NULL, 'Returns', 'Levered IRR', 0.25, 'levered_irr', 'linear', 0.25, 0.20, 0.15, 0.10),
    (NULL, 'Returns', 'Equity Multiple', 0.10, 'equity_multiple', 'linear', 2.50, 2.00, 1.60, 1.30),
    (NULL, 'Returns', 'Cash-on-Cash Y1', 0.05, 'cash_on_cash_y1', 'linear', 0.12, 0.08, 0.05, 0.03),
    
    -- RISK (30% weight)
    (NULL, 'Risk', 'DSCR Y1', 0.15, 'dscr_year1', 'linear', 1.50, 1.35, 1.25, 1.15),
    (NULL, 'Risk', 'LTV', 0.10, 'ltv', 'inverse', 0.65, 0.70, 0.75, 0.80),
    (NULL, 'Risk', 'Cap Rate Spread', 0.05, 'cap_rate_spread', 'linear', 150, 100, 50, 0),
    
    -- LOCATION (20% weight)
    (NULL, 'Location', 'Submarket Quality', 0.20, 'location_score', 'linear', 90, 75, 60, 45),
    
    -- OPERATIONS (10% weight)
    (NULL, 'Operations', 'NOI Margin', 0.05, 'noi_margin', 'linear', 0.65, 0.60, 0.55, 0.50),
    (NULL, 'Operations', 'Stabilized Occupancy', 0.05, 'occupancy_stabilized', 'linear', 0.95, 0.92, 0.88, 0.85);
*/

-- =====================================================
-- COMMENTS
-- =====================================================

COMMENT ON TABLE comparison_sets IS 'Groups of property deals being compared side-by-side';
COMMENT ON TABLE property_deals IS 'Individual real estate deals with basic information';
COMMENT ON TABLE comparison_metrics IS 'Standardized financial metrics for each deal';
COMMENT ON TABLE scoring_criteria IS 'Weighted criteria for ranking deals';
COMMENT ON TABLE deal_scores IS 'Individual scores for each deal against each criterion';

COMMENT ON COLUMN comparison_metrics.levered_irr IS 'Internal Rate of Return with debt financing (%)';
COMMENT ON COLUMN comparison_metrics.equity_multiple IS 'Total cash returned / equity invested (MOIC)';
COMMENT ON COLUMN comparison_metrics.dscr_year1 IS 'Debt Service Coverage Ratio in Year 1';
COMMENT ON COLUMN comparison_metrics.noi_margin IS 'Net Operating Income / Gross Revenue (%)';
