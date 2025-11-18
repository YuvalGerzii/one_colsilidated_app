-- ============================================================================
-- SINGLE-FAMILY RENTAL (SFR) ANALYSIS SCHEMA
-- Portfolio Dashboard Integration
-- ============================================================================
--
-- Extends the portfolio_companies schema to support mortgage-financed
-- rental property investments with comprehensive return analysis
--
-- Tables:
--   1. sfr_properties - Property master records
--   2. sfr_financing - Mortgage and debt details
--   3. sfr_cash_flows - 10-year monthly projections
--   4. sfr_scenarios - Exit strategy analysis (Flip, BRRRR, Hold)
--   5. sfr_analysis_summary - Key metrics and returns
-- ============================================================================

-- ============================================================================
-- TABLE 1: SFR Properties
-- ============================================================================
CREATE TABLE IF NOT EXISTS sfr_properties (
    property_id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES portfolio_companies(company_id) ON DELETE CASCADE,
    fund_id INTEGER REFERENCES funds(fund_id),
    
    -- Property identification
    property_name VARCHAR(255) NOT NULL,
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(50),
    zip_code VARCHAR(20),
    
    -- Property details
    square_feet INTEGER NOT NULL,
    bedrooms INTEGER,
    bathrooms DECIMAL(3,1), -- e.g., 2.5 for 2 full + 1 half bath
    lot_size_sqft INTEGER,
    year_built INTEGER,
    property_type VARCHAR(50) DEFAULT 'Single Family', -- 'Single Family', 'Condo', 'Townhouse'
    
    -- Acquisition details
    purchase_price DECIMAL(15,2) NOT NULL,
    closing_costs DECIMAL(15,2),
    renovation_budget DECIMAL(15,2) DEFAULT 0,
    total_acquisition_cost DECIMAL(15,2) NOT NULL, -- purchase + closing + renovation
    acquisition_date DATE,
    
    -- After Repair Value (ARV)
    arv_estimate DECIMAL(15,2), -- Appraised value after renovation
    arv_date DATE,
    
    -- Rental analysis
    monthly_rent DECIMAL(10,2) NOT NULL,
    market_rent DECIMAL(10,2),
    security_deposit DECIMAL(10,2),
    pet_deposit DECIMAL(10,2),
    
    -- Operating assumptions
    vacancy_rate DECIMAL(5,2) DEFAULT 5.00, -- Percentage
    annual_rent_growth DECIMAL(5,2) DEFAULT 3.00, -- Percentage
    annual_expense_growth DECIMAL(5,2) DEFAULT 2.00, -- Percentage
    annual_appreciation DECIMAL(5,2) DEFAULT 4.00, -- Percentage
    
    -- Operating expenses (monthly)
    property_tax_monthly DECIMAL(10,2) NOT NULL,
    insurance_monthly DECIMAL(10,2) NOT NULL,
    hoa_monthly DECIMAL(10,2) DEFAULT 0,
    utilities_monthly DECIMAL(10,2) DEFAULT 0,
    management_fee_pct DECIMAL(5,2) DEFAULT 10.00, -- % of gross rent
    maintenance_reserve_monthly DECIMAL(10,2) NOT NULL,
    capex_reserve_monthly DECIMAL(10,2) NOT NULL,
    
    -- Investment strategy
    investment_strategy VARCHAR(50), -- 'Buy & Hold', 'BRRRR', 'Flip', 'House Hack'
    hold_period_years INTEGER DEFAULT 10,
    
    -- Status tracking
    status VARCHAR(50) DEFAULT 'Analysis', -- 'Analysis', 'Under Contract', 'Owned', 'Renovating', 'Rented', 'Sold'
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100),
    
    -- Indexes
    INDEX idx_sfr_property_company (company_id),
    INDEX idx_sfr_property_fund (fund_id),
    INDEX idx_sfr_property_status (status),
    INDEX idx_sfr_property_city (city, state)
);


-- ============================================================================
-- TABLE 2: SFR Financing
-- ============================================================================
CREATE TABLE IF NOT EXISTS sfr_financing (
    financing_id SERIAL PRIMARY KEY,
    property_id INTEGER REFERENCES sfr_properties(property_id) ON DELETE CASCADE,
    
    -- Equity investment
    down_payment DECIMAL(15,2) NOT NULL,
    closing_costs_cash DECIMAL(15,2) NOT NULL,
    renovation_cash DECIMAL(15,2) DEFAULT 0,
    total_cash_invested DECIMAL(15,2) NOT NULL,
    
    -- Initial mortgage (acquisition)
    loan_amount DECIMAL(15,2) NOT NULL,
    loan_type VARCHAR(50), -- 'Conventional', 'FHA', 'VA', 'Portfolio', 'Hard Money'
    interest_rate DECIMAL(6,3) NOT NULL, -- e.g., 7.500 for 7.5%
    loan_term_months INTEGER NOT NULL, -- 360 for 30-year
    monthly_payment DECIMAL(10,2) NOT NULL,
    ltv_ratio DECIMAL(5,2) NOT NULL, -- Loan-to-Value %
    
    -- Points and fees
    origination_points DECIMAL(5,2) DEFAULT 0,
    origination_fees DECIMAL(10,2) DEFAULT 0,
    
    -- Refinance details (for BRRRR strategy)
    refinance_date DATE,
    refinance_loan_amount DECIMAL(15,2),
    refinance_rate DECIMAL(6,3),
    refinance_term_months INTEGER,
    refinance_monthly_payment DECIMAL(10,2),
    refinance_ltv DECIMAL(5,2),
    cash_out_amount DECIMAL(15,2), -- Cash pulled out in refi
    
    -- Lender information
    lender_name VARCHAR(255),
    loan_number VARCHAR(100),
    loan_origination_date DATE,
    loan_maturity_date DATE,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_sfr_financing_property (property_id),
    INDEX idx_sfr_financing_lender (lender_name)
);


-- ============================================================================
-- TABLE 3: SFR Cash Flows (10-Year Projections)
-- ============================================================================
CREATE TABLE IF NOT EXISTS sfr_cash_flows (
    cash_flow_id SERIAL PRIMARY KEY,
    property_id INTEGER REFERENCES sfr_properties(property_id) ON DELETE CASCADE,
    
    -- Time period
    year_number INTEGER NOT NULL, -- 1 to 10
    month_number INTEGER NOT NULL, -- 1 to 12
    period_date DATE NOT NULL,
    
    -- Income
    gross_scheduled_income DECIMAL(10,2), -- Monthly rent * units
    vacancy_loss DECIMAL(10,2), -- vacancy_rate * GSI
    effective_gross_income DECIMAL(10,2), -- GSI - vacancy
    other_income DECIMAL(10,2) DEFAULT 0, -- Pet fees, laundry, parking
    total_income DECIMAL(10,2),
    
    -- Operating expenses
    property_tax DECIMAL(10,2),
    insurance DECIMAL(10,2),
    hoa_fees DECIMAL(10,2),
    utilities DECIMAL(10,2),
    management_fee DECIMAL(10,2),
    maintenance_repairs DECIMAL(10,2),
    capex_reserve DECIMAL(10,2),
    total_operating_expenses DECIMAL(10,2),
    
    -- Net Operating Income
    noi DECIMAL(10,2), -- Total Income - Operating Expenses
    
    -- Debt service
    mortgage_payment DECIMAL(10,2),
    mortgage_interest DECIMAL(10,2),
    mortgage_principal DECIMAL(10,2),
    
    -- Cash flow
    net_cash_flow DECIMAL(10,2), -- NOI - Debt Service
    cumulative_cash_flow DECIMAL(15,2),
    
    -- Property value
    property_value DECIMAL(15,2), -- Appreciated value
    loan_balance DECIMAL(15,2), -- Remaining mortgage
    equity DECIMAL(15,2), -- property_value - loan_balance
    
    -- Metrics
    cash_on_cash_return DECIMAL(8,4), -- Annual CF / Cash Invested
    cap_rate DECIMAL(6,3), -- NOI / Property Value
    dscr DECIMAL(6,3), -- NOI / Debt Service (Debt Service Coverage Ratio)
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(property_id, year_number, month_number),
    INDEX idx_sfr_cashflow_property (property_id),
    INDEX idx_sfr_cashflow_date (period_date),
    INDEX idx_sfr_cashflow_year (year_number)
);


-- ============================================================================
-- TABLE 4: SFR Exit Scenarios
-- ============================================================================
CREATE TABLE IF NOT EXISTS sfr_scenarios (
    scenario_id SERIAL PRIMARY KEY,
    property_id INTEGER REFERENCES sfr_properties(property_id) ON DELETE CASCADE,
    
    -- Scenario details
    scenario_name VARCHAR(100) NOT NULL, -- 'Flip', 'BRRRR', 'Hold 10 Years', 'Hold Forever'
    scenario_type VARCHAR(50) NOT NULL,
    
    -- Exit assumptions
    exit_year INTEGER, -- NULL for 'Hold Forever'
    exit_month INTEGER,
    exit_property_value DECIMAL(15,2),
    
    -- Sale details (for Flip/Hold strategies)
    sale_price DECIMAL(15,2),
    selling_costs_pct DECIMAL(5,2) DEFAULT 6.00, -- Agent commission
    selling_costs_amount DECIMAL(15,2),
    loan_payoff DECIMAL(15,2),
    net_sale_proceeds DECIMAL(15,2), -- sale_price - costs - loan_payoff
    
    -- Returns
    total_cash_flow DECIMAL(15,2), -- Sum of all monthly CF
    total_return DECIMAL(15,2), -- CF + net sale proceeds
    irr DECIMAL(8,4), -- Internal Rate of Return (%)
    equity_multiple DECIMAL(6,3), -- Total Return / Cash Invested
    average_annual_return DECIMAL(8,4), -- Annualized return
    
    -- Tax impact (simplified)
    capital_gains DECIMAL(15,2),
    depreciation_recapture DECIMAL(15,2),
    estimated_tax DECIMAL(15,2),
    after_tax_return DECIMAL(15,2),
    
    -- BRRRR-specific metrics
    cash_out_refinance_amount DECIMAL(15,2),
    capital_recycled DECIMAL(15,2), -- How much $ can be redeployed
    infinite_roi BOOLEAN DEFAULT FALSE, -- All capital recovered
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(property_id, scenario_name),
    INDEX idx_sfr_scenario_property (property_id),
    INDEX idx_sfr_scenario_type (scenario_type)
);


-- ============================================================================
-- TABLE 5: SFR Analysis Summary (Dashboard KPIs)
-- ============================================================================
CREATE TABLE IF NOT EXISTS sfr_analysis_summary (
    analysis_id SERIAL PRIMARY KEY,
    property_id INTEGER REFERENCES sfr_properties(property_id) ON DELETE CASCADE,
    analysis_date DATE NOT NULL DEFAULT CURRENT_DATE,
    
    -- Property snapshot
    current_value DECIMAL(15,2),
    purchase_price DECIMAL(15,2),
    total_invested DECIMAL(15,2),
    
    -- Current performance
    monthly_rent DECIMAL(10,2),
    monthly_expenses DECIMAL(10,2),
    monthly_mortgage DECIMAL(10,2),
    monthly_cash_flow DECIMAL(10,2),
    
    -- Key metrics
    cash_on_cash_return DECIMAL(8,4), -- Year 1 %
    ten_year_irr DECIMAL(8,4), -- Best-case hold scenario
    cap_rate DECIMAL(6,3),
    dscr DECIMAL(6,3),
    ltv DECIMAL(5,2),
    
    -- Screening metrics
    one_percent_rule_pass BOOLEAN, -- Rent >= 1% of purchase price
    fifty_percent_rule_pass BOOLEAN, -- Operating expenses <= 50% of rent
    break_even_rent DECIMAL(10,2), -- Minimum rent to cover all costs
    
    -- Market comparison
    market_rent DECIMAL(10,2),
    rent_premium_pct DECIMAL(6,2), -- (Actual - Market) / Market
    price_per_sqft DECIMAL(10,2),
    market_price_per_sqft DECIMAL(10,2),
    
    -- Risk assessment
    vacancy_break_even DECIMAL(5,2), -- Max vacancy before negative CF
    interest_rate_sensitivity DECIMAL(5,2), -- % rate increase to break even
    worst_case_scenario_irr DECIMAL(8,4), -- Conservative assumptions
    
    -- Tax benefits
    annual_depreciation DECIMAL(10,2), -- IRS depreciation deduction
    estimated_tax_savings DECIMAL(10,2),
    after_tax_irr DECIMAL(8,4),
    
    -- Portfolio context
    portfolio_rank INTEGER, -- Rank among all properties in fund
    peer_avg_irr DECIMAL(8,4), -- Average IRR of similar properties
    
    -- Investment decision
    investment_decision VARCHAR(50), -- 'STRONG BUY', 'BUY', 'PASS', 'SELL'
    decision_rationale TEXT,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100),
    
    UNIQUE(property_id, analysis_date),
    INDEX idx_sfr_summary_property (property_id),
    INDEX idx_sfr_summary_date (analysis_date),
    INDEX idx_sfr_summary_decision (investment_decision)
);


-- ============================================================================
-- VIEWS FOR DASHBOARD
-- ============================================================================

-- Portfolio-level summary
CREATE OR REPLACE VIEW vw_sfr_portfolio_summary AS
SELECT 
    f.fund_name,
    COUNT(DISTINCT sp.property_id) as total_properties,
    SUM(sp.total_acquisition_cost) as total_invested,
    SUM(sp.monthly_rent * 12) as total_annual_rent,
    AVG(sas.cash_on_cash_return) as avg_cash_on_cash,
    AVG(sas.ten_year_irr) as avg_irr,
    SUM(sp.monthly_rent * 12) / SUM(sp.total_acquisition_cost) as portfolio_yield,
    SUM(CASE WHEN sas.one_percent_rule_pass THEN 1 ELSE 0 END) as properties_passing_1pct_rule,
    AVG(sas.dscr) as avg_dscr
FROM sfr_properties sp
JOIN funds f ON sp.fund_id = f.fund_id
LEFT JOIN sfr_analysis_summary sas ON sp.property_id = sas.property_id
WHERE sp.status IN ('Owned', 'Rented')
GROUP BY f.fund_id, f.fund_name;


-- Best performing properties
CREATE OR REPLACE VIEW vw_sfr_top_performers AS
SELECT 
    sp.property_id,
    sp.property_name,
    sp.address,
    sp.city,
    sp.state,
    sp.total_acquisition_cost,
    sp.monthly_rent,
    sas.cash_on_cash_return,
    sas.ten_year_irr,
    sas.cap_rate,
    sas.investment_decision,
    RANK() OVER (ORDER BY sas.ten_year_irr DESC) as performance_rank
FROM sfr_properties sp
JOIN sfr_analysis_summary sas ON sp.property_id = sas.property_id
WHERE sp.status IN ('Owned', 'Rented', 'Analysis')
ORDER BY sas.ten_year_irr DESC
LIMIT 20;


-- Properties needing attention
CREATE OR REPLACE VIEW vw_sfr_properties_at_risk AS
SELECT 
    sp.property_id,
    sp.property_name,
    sp.city,
    sp.state,
    sp.status,
    sas.monthly_cash_flow,
    sas.dscr,
    sas.vacancy_break_even,
    CASE 
        WHEN sas.monthly_cash_flow < 0 THEN 'NEGATIVE CASH FLOW'
        WHEN sas.dscr < 1.25 THEN 'LOW DSCR'
        WHEN sas.vacancy_break_even < 10 THEN 'HIGH VACANCY RISK'
        ELSE 'MONITOR'
    END as risk_category
FROM sfr_properties sp
JOIN sfr_analysis_summary sas ON sp.property_id = sas.property_id
WHERE sp.status IN ('Owned', 'Rented')
  AND (sas.monthly_cash_flow < 100 OR sas.dscr < 1.25 OR sas.vacancy_break_even < 10);


-- ============================================================================
-- HELPER FUNCTIONS
-- ============================================================================

-- Calculate monthly mortgage payment
CREATE OR REPLACE FUNCTION calculate_mortgage_payment(
    loan_amount DECIMAL,
    annual_rate DECIMAL,
    term_months INTEGER
)
RETURNS DECIMAL AS $$
DECLARE
    monthly_rate DECIMAL;
    payment DECIMAL;
BEGIN
    monthly_rate := annual_rate / 100 / 12;
    
    IF monthly_rate = 0 THEN
        RETURN loan_amount / term_months;
    END IF;
    
    payment := loan_amount * (monthly_rate * POWER(1 + monthly_rate, term_months)) / 
               (POWER(1 + monthly_rate, term_months) - 1);
    
    RETURN ROUND(payment, 2);
END;
$$ LANGUAGE plpgsql;


-- Calculate Cash-on-Cash return
CREATE OR REPLACE FUNCTION calculate_cash_on_cash(
    annual_cash_flow DECIMAL,
    total_cash_invested DECIMAL
)
RETURNS DECIMAL AS $$
BEGIN
    IF total_cash_invested = 0 THEN
        RETURN 0;
    END IF;
    
    RETURN ROUND((annual_cash_flow / total_cash_invested * 100), 4);
END;
$$ LANGUAGE plpgsql;


-- Calculate Cap Rate
CREATE OR REPLACE FUNCTION calculate_cap_rate(
    annual_noi DECIMAL,
    property_value DECIMAL
)
RETURNS DECIMAL AS $$
BEGIN
    IF property_value = 0 THEN
        RETURN 0;
    END IF;
    
    RETURN ROUND((annual_noi / property_value * 100), 3);
END;
$$ LANGUAGE plpgsql;


-- ============================================================================
-- SAMPLE DATA INSERT
-- ============================================================================
-- Example: 3BR/2BA house with mortgage financing

-- INSERT INTO sfr_properties (
--     company_id, fund_id, property_name, address, city, state, zip_code,
--     square_feet, bedrooms, bathrooms, year_built,
--     purchase_price, closing_costs, renovation_budget, total_acquisition_cost,
--     monthly_rent, vacancy_rate,
--     property_tax_monthly, insurance_monthly, maintenance_reserve_monthly, capex_reserve_monthly,
--     investment_strategy, hold_period_years, status
-- ) VALUES (
--     1, 1, '123 Main Street', '123 Main Street', 'Austin', 'TX', '78701',
--     1500, 3, 2.0, 2015,
--     150000, 3000, 45000, 198000,
--     2450, 5.00,
--     350, 125, 200, 150,
--     'Buy & Hold', 10, 'Analysis'
-- );


-- ============================================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================================
CREATE INDEX IF NOT EXISTS idx_sfr_property_acquisition_date ON sfr_properties(acquisition_date);
CREATE INDEX IF NOT EXISTS idx_sfr_cashflow_composite ON sfr_cash_flows(property_id, year_number, month_number);
CREATE INDEX IF NOT EXISTS idx_sfr_summary_irr ON sfr_analysis_summary(ten_year_irr DESC);

-- ============================================================================
-- PERMISSIONS
-- ============================================================================
-- Grant appropriate permissions to application role
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO portfolio_app_role;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO portfolio_app_role;
-- GRANT SELECT ON vw_sfr_portfolio_summary TO portfolio_app_role;
-- GRANT SELECT ON vw_sfr_top_performers TO portfolio_app_role;
-- GRANT SELECT ON vw_sfr_properties_at_risk TO portfolio_app_role;

