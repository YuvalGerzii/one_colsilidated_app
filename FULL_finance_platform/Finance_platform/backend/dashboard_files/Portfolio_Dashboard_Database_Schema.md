# Portfolio Dashboard - Database Schema & Models

## Database Schema (PostgreSQL)

### Complete SQL Schema

```sql
-- =====================================================
-- CORE ENTITIES
-- =====================================================

-- Funds table
CREATE TABLE funds (
    fund_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    fund_name VARCHAR(255) NOT NULL,
    fund_number INTEGER,
    vintage_year INTEGER NOT NULL,
    fund_size DECIMAL(15, 2) NOT NULL,
    committed_capital DECIMAL(15, 2) NOT NULL,
    drawn_capital DECIMAL(15, 2) DEFAULT 0,
    distributed_capital DECIMAL(15, 2) DEFAULT 0,
    target_irr DECIMAL(5, 4),
    fund_strategy VARCHAR(100),
    sector_focus TEXT[],
    geographic_focus TEXT[],
    fund_status VARCHAR(50) DEFAULT 'Active',
    inception_date DATE,
    close_date DATE,
    final_close_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES users(user_id),
    CONSTRAINT fund_size_positive CHECK (fund_size > 0)
);

-- Portfolio Companies table
CREATE TABLE portfolio_companies (
    company_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    fund_id UUID NOT NULL REFERENCES funds(fund_id) ON DELETE CASCADE,
    company_name VARCHAR(255) NOT NULL,
    company_legal_name VARCHAR(255),
    ticker_symbol VARCHAR(10),
    website VARCHAR(255),
    
    -- Investment details
    investment_date DATE NOT NULL,
    deal_type VARCHAR(50) NOT NULL, -- LBO, Growth, Minority, etc.
    sector VARCHAR(100) NOT NULL,
    industry VARCHAR(100),
    sub_sector VARCHAR(100),
    business_description TEXT,
    
    -- Location
    headquarters_city VARCHAR(100),
    headquarters_state VARCHAR(100),
    headquarters_country VARCHAR(100) DEFAULT 'United States',
    
    -- Financial snapshot (at entry)
    entry_revenue DECIMAL(15, 2),
    entry_ebitda DECIMAL(15, 2),
    entry_multiple DECIMAL(10, 2),
    purchase_price DECIMAL(15, 2),
    equity_invested DECIMAL(15, 2),
    debt_raised DECIMAL(15, 2),
    ownership_percentage DECIMAL(5, 4),
    
    -- Status
    company_status VARCHAR(50) DEFAULT 'Active', -- Active, Exited, Written Off
    exit_date DATE,
    exit_type VARCHAR(50), -- IPO, Strategic Sale, Secondary, etc.
    exit_proceeds DECIMAL(15, 2),
    realized_moic DECIMAL(10, 2),
    realized_irr DECIMAL(10, 4),
    
    -- Risk & Rating
    risk_rating VARCHAR(20) DEFAULT 'Medium', -- Low, Medium, High
    internal_rating VARCHAR(10), -- A, B, C, D scale
    
    -- Team
    ceo_name VARCHAR(255),
    cfo_name VARCHAR(255),
    board_members TEXT[],
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES users(user_id),
    
    CONSTRAINT ownership_valid CHECK (ownership_percentage >= 0 AND ownership_percentage <= 1),
    CONSTRAINT status_valid CHECK (company_status IN ('Active', 'Exited', 'Written Off', 'On Hold'))
);

-- Financial Metrics table (time series)
CREATE TABLE financial_metrics (
    metric_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES portfolio_companies(company_id) ON DELETE CASCADE,
    
    -- Period information
    period_date DATE NOT NULL,
    period_type VARCHAR(20) NOT NULL, -- Monthly, Quarterly, Annual, LTM
    fiscal_year INTEGER NOT NULL,
    fiscal_quarter INTEGER, -- 1-4 for quarterly, NULL for annual
    fiscal_month INTEGER, -- 1-12 for monthly, NULL otherwise
    
    -- Income Statement
    revenue DECIMAL(15, 2),
    cogs DECIMAL(15, 2),
    gross_profit DECIMAL(15, 2),
    gross_margin DECIMAL(5, 4),
    
    operating_expenses DECIMAL(15, 2),
    sales_marketing DECIMAL(15, 2),
    research_development DECIMAL(15, 2),
    general_admin DECIMAL(15, 2),
    
    ebitda DECIMAL(15, 2),
    ebitda_margin DECIMAL(5, 4),
    adjusted_ebitda DECIMAL(15, 2),
    adjusted_ebitda_margin DECIMAL(5, 4),
    
    depreciation DECIMAL(15, 2),
    amortization DECIMAL(15, 2),
    ebit DECIMAL(15, 2),
    
    interest_expense DECIMAL(15, 2),
    interest_income DECIMAL(15, 2),
    other_income DECIMAL(15, 2),
    
    ebt DECIMAL(15, 2),
    tax_expense DECIMAL(15, 2),
    tax_rate DECIMAL(5, 4),
    net_income DECIMAL(15, 2),
    net_margin DECIMAL(5, 4),
    
    -- Balance Sheet
    cash DECIMAL(15, 2),
    accounts_receivable DECIMAL(15, 2),
    inventory DECIMAL(15, 2),
    prepaid_expenses DECIMAL(15, 2),
    other_current_assets DECIMAL(15, 2),
    total_current_assets DECIMAL(15, 2),
    
    ppe_gross DECIMAL(15, 2),
    accumulated_depreciation DECIMAL(15, 2),
    ppe_net DECIMAL(15, 2),
    intangible_assets DECIMAL(15, 2),
    goodwill DECIMAL(15, 2),
    other_longterm_assets DECIMAL(15, 2),
    total_assets DECIMAL(15, 2),
    
    accounts_payable DECIMAL(15, 2),
    accrued_expenses DECIMAL(15, 2),
    current_portion_debt DECIMAL(15, 2),
    other_current_liabilities DECIMAL(15, 2),
    total_current_liabilities DECIMAL(15, 2),
    
    long_term_debt DECIMAL(15, 2),
    deferred_taxes DECIMAL(15, 2),
    other_longterm_liabilities DECIMAL(15, 2),
    total_liabilities DECIMAL(15, 2),
    
    shareholders_equity DECIMAL(15, 2),
    retained_earnings DECIMAL(15, 2),
    
    -- Cash Flow Statement
    operating_cash_flow DECIMAL(15, 2),
    capex DECIMAL(15, 2),
    investing_cash_flow DECIMAL(15, 2),
    financing_cash_flow DECIMAL(15, 2),
    net_cash_flow DECIMAL(15, 2),
    free_cash_flow DECIMAL(15, 2),
    
    -- Calculated Metrics
    working_capital DECIMAL(15, 2),
    net_working_capital DECIMAL(15, 2),
    nwc_percent_revenue DECIMAL(5, 4),
    
    -- Data source and validation
    data_source VARCHAR(100), -- Management Report, Audited Financials, etc.
    data_source_file_id UUID REFERENCES documents(document_id),
    verified BOOLEAN DEFAULT FALSE,
    verified_by UUID REFERENCES users(user_id),
    verified_at TIMESTAMP,
    
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES users(user_id),
    
    CONSTRAINT unique_company_period UNIQUE (company_id, period_date, period_type),
    CONSTRAINT valid_period_type CHECK (period_type IN ('Monthly', 'Quarterly', 'Annual', 'LTM'))
);

-- Company KPIs table (for operational metrics)
CREATE TABLE company_kpis (
    kpi_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES portfolio_companies(company_id) ON DELETE CASCADE,
    
    period_date DATE NOT NULL,
    period_type VARCHAR(20) NOT NULL,
    
    -- SaaS Metrics
    arr DECIMAL(15, 2),
    mrr DECIMAL(15, 2),
    net_revenue_retention DECIMAL(5, 4),
    gross_revenue_retention DECIMAL(5, 4),
    customer_churn_rate DECIMAL(5, 4),
    revenue_churn_rate DECIMAL(5, 4),
    
    -- Customer Metrics
    total_customers INTEGER,
    new_customers INTEGER,
    churned_customers INTEGER,
    active_customers INTEGER,
    arpu DECIMAL(15, 2), -- Average Revenue Per User
    
    -- Sales & Marketing
    cac DECIMAL(15, 2), -- Customer Acquisition Cost
    ltv DECIMAL(15, 2), -- Lifetime Value
    ltv_cac_ratio DECIMAL(10, 2),
    magic_number DECIMAL(10, 2),
    sales_efficiency DECIMAL(10, 2),
    
    -- Operational
    headcount INTEGER,
    revenue_per_employee DECIMAL(15, 2),
    gross_margin_per_employee DECIMAL(15, 2),
    
    -- Product/Tech
    monthly_active_users INTEGER,
    daily_active_users INTEGER,
    nps_score INTEGER, -- Net Promoter Score
    product_adoption_rate DECIMAL(5, 4),
    
    -- E-commerce
    gmv DECIMAL(15, 2), -- Gross Merchandise Value
    take_rate DECIMAL(5, 4),
    average_order_value DECIMAL(15, 2),
    orders INTEGER,
    
    -- Custom KPIs (JSON for flexibility)
    custom_kpis JSONB,
    
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT unique_company_kpi_period UNIQUE (company_id, period_date, period_type)
);

-- Valuations table
CREATE TABLE valuations (
    valuation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES portfolio_companies(company_id) ON DELETE CASCADE,
    
    valuation_date DATE NOT NULL,
    valuation_type VARCHAR(50) NOT NULL, -- DCF, Market Comps, Transaction Comps, LBO, Fair Value
    
    -- DCF Valuation
    dcf_enterprise_value DECIMAL(15, 2),
    dcf_equity_value DECIMAL(15, 2),
    dcf_terminal_value DECIMAL(15, 2),
    dcf_pv_terminal_value DECIMAL(15, 2),
    dcf_wacc DECIMAL(5, 4),
    dcf_terminal_growth DECIMAL(5, 4),
    dcf_projection_years INTEGER,
    
    -- Market Comparables
    comp_ev_revenue_multiple DECIMAL(10, 2),
    comp_ev_ebitda_multiple DECIMAL(10, 2),
    comp_ev_ebit_multiple DECIMAL(10, 2),
    comp_pe_ratio DECIMAL(10, 2),
    implied_ev_from_revenue DECIMAL(15, 2),
    implied_ev_from_ebitda DECIMAL(15, 2),
    
    -- Transaction Comparables
    precedent_ev_revenue DECIMAL(10, 2),
    precedent_ev_ebitda DECIMAL(10, 2),
    precedent_premium_paid DECIMAL(5, 4),
    
    -- Final Valuation
    enterprise_value DECIMAL(15, 2) NOT NULL,
    net_debt DECIMAL(15, 2),
    equity_value DECIMAL(15, 2) NOT NULL,
    
    -- Returns Metrics
    cost_basis DECIMAL(15, 2),
    unrealized_gain DECIMAL(15, 2),
    unrealized_moic DECIMAL(10, 2),
    unrealized_irr DECIMAL(10, 4),
    
    -- Valuation details
    valuation_assumptions JSONB,
    valuation_model_file_id UUID REFERENCES documents(document_id),
    
    -- Approval
    status VARCHAR(50) DEFAULT 'Draft', -- Draft, Pending, Approved, Rejected
    approved_by UUID REFERENCES users(user_id),
    approved_at TIMESTAMP,
    
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES users(user_id),
    
    CONSTRAINT valid_valuation_status CHECK (status IN ('Draft', 'Pending', 'Approved', 'Rejected'))
);

-- Due Diligence Tracker
CREATE TABLE due_diligence (
    dd_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES portfolio_companies(company_id) ON DELETE CASCADE,
    
    dd_phase VARCHAR(50) NOT NULL, -- Pre-LOI, Post-LOI, Confirmatory
    dd_start_date DATE NOT NULL,
    dd_target_end_date DATE,
    dd_actual_end_date DATE,
    
    overall_status VARCHAR(50) DEFAULT 'Not Started',
    overall_completion_pct DECIMAL(5, 4) DEFAULT 0,
    
    -- Summary stats
    total_items INTEGER DEFAULT 0,
    completed_items INTEGER DEFAULT 0,
    high_priority_open INTEGER DEFAULT 0,
    red_flags_count INTEGER DEFAULT 0,
    
    -- Final recommendation
    dd_recommendation VARCHAR(50), -- Proceed, Proceed with Conditions, Do Not Proceed
    dd_summary TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES users(user_id)
);

-- Due Diligence Items
CREATE TABLE dd_items (
    item_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dd_id UUID NOT NULL REFERENCES due_diligence(dd_id) ON DELETE CASCADE,
    
    workstream VARCHAR(100) NOT NULL, -- Financial, Commercial, Legal, Tax, etc.
    item_number VARCHAR(50),
    item_description TEXT NOT NULL,
    priority VARCHAR(20) DEFAULT 'Medium', -- Low, Medium, High, Critical
    
    assigned_to UUID REFERENCES users(user_id),
    due_date DATE,
    
    status VARCHAR(50) DEFAULT 'Not Started', -- Not Started, In Progress, Complete, Blocked
    completion_date DATE,
    
    -- Findings
    finding_summary TEXT,
    risk_level VARCHAR(20), -- None, Low, Medium, High, Critical
    value_impact DECIMAL(15, 2),
    mitigation_plan TEXT,
    
    -- Documents
    documents_received BOOLEAN DEFAULT FALSE,
    documents_reviewed BOOLEAN DEFAULT FALSE,
    
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT valid_priority CHECK (priority IN ('Low', 'Medium', 'High', 'Critical')),
    CONSTRAINT valid_status CHECK (status IN ('Not Started', 'In Progress', 'Complete', 'Blocked'))
);

-- Value Creation Initiatives
CREATE TABLE value_creation_initiatives (
    initiative_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES portfolio_companies(company_id) ON DELETE CASCADE,
    
    initiative_name VARCHAR(255) NOT NULL,
    initiative_category VARCHAR(100) NOT NULL, -- Revenue Growth, Margin Improvement, etc.
    description TEXT,
    
    owner_name VARCHAR(255),
    owner_user_id UUID REFERENCES users(user_id),
    
    -- Timeline
    start_date DATE,
    target_completion_date DATE,
    actual_completion_date DATE,
    
    -- Financials
    investment_required DECIMAL(15, 2),
    target_revenue_impact DECIMAL(15, 2),
    target_ebitda_impact DECIMAL(15, 2),
    target_completion_year INTEGER,
    
    actual_revenue_impact DECIMAL(15, 2),
    actual_ebitda_impact DECIMAL(15, 2),
    
    -- Status
    status VARCHAR(50) DEFAULT 'Planning', -- Planning, In Progress, Complete, On Hold, Cancelled
    completion_pct DECIMAL(5, 4) DEFAULT 0,
    
    -- Tracking
    milestones JSONB, -- Array of milestones with dates
    kpis JSONB, -- KPIs to track progress
    
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES users(user_id),
    
    CONSTRAINT valid_status CHECK (status IN ('Planning', 'In Progress', 'Complete', 'On Hold', 'Cancelled'))
);

-- Documents table
CREATE TABLE documents (
    document_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID REFERENCES portfolio_companies(company_id) ON DELETE CASCADE,
    fund_id UUID REFERENCES funds(fund_id) ON DELETE CASCADE,
    
    document_name VARCHAR(255) NOT NULL,
    document_type VARCHAR(100) NOT NULL, -- Financial Statement, Board Report, etc.
    document_category VARCHAR(100), -- Due Diligence, Quarterly Report, etc.
    
    file_path VARCHAR(500) NOT NULL,
    file_size_bytes BIGINT,
    file_type VARCHAR(50), -- PDF, XLSX, DOCX, etc.
    
    -- PDF Processing
    extraction_status VARCHAR(50), -- Pending, Processing, Complete, Failed
    extraction_confidence DECIMAL(5, 4),
    extracted_data JSONB,
    needs_review BOOLEAN DEFAULT FALSE,
    
    -- Metadata
    period_date DATE,
    fiscal_year INTEGER,
    fiscal_quarter INTEGER,
    
    uploaded_by UUID REFERENCES users(user_id),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT document_scope CHECK (
        (company_id IS NOT NULL AND fund_id IS NULL) OR 
        (company_id IS NULL AND fund_id IS NOT NULL)
    )
);

-- Users table
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    
    role VARCHAR(50) NOT NULL, -- Admin, Partner, Associate, Analyst, LP, Viewer
    firm_name VARCHAR(255),
    
    password_hash VARCHAR(255) NOT NULL,
    two_factor_enabled BOOLEAN DEFAULT FALSE,
    two_factor_secret VARCHAR(255),
    
    -- Access control
    funds_access UUID[], -- Array of fund_ids user can access
    companies_access UUID[], -- Array of company_ids (for portfolio company users)
    
    last_login TIMESTAMP,
    active BOOLEAN DEFAULT TRUE,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT valid_role CHECK (role IN ('Admin', 'Partner', 'Associate', 'Analyst', 'LP', 'Viewer', 'PortCo'))
);

-- Audit Log table
CREATE TABLE audit_logs (
    log_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id),
    
    action VARCHAR(100) NOT NULL, -- CREATE, UPDATE, DELETE, VIEW, EXPORT, etc.
    entity_type VARCHAR(100) NOT NULL, -- Company, Valuation, Document, etc.
    entity_id UUID NOT NULL,
    
    changes JSONB, -- Before/after values for updates
    ip_address INET,
    user_agent TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================

-- Companies
CREATE INDEX idx_companies_fund ON portfolio_companies(fund_id);
CREATE INDEX idx_companies_status ON portfolio_companies(company_status);
CREATE INDEX idx_companies_sector ON portfolio_companies(sector);
CREATE INDEX idx_companies_investment_date ON portfolio_companies(investment_date);

-- Financial Metrics
CREATE INDEX idx_metrics_company ON financial_metrics(company_id);
CREATE INDEX idx_metrics_period ON financial_metrics(period_date);
CREATE INDEX idx_metrics_company_period ON financial_metrics(company_id, period_date);

-- Valuations
CREATE INDEX idx_valuations_company ON valuations(company_id);
CREATE INDEX idx_valuations_date ON valuations(valuation_date);

-- Documents
CREATE INDEX idx_documents_company ON documents(company_id);
CREATE INDEX idx_documents_type ON documents(document_type);
CREATE INDEX idx_documents_extraction ON documents(extraction_status);

-- Audit Logs
CREATE INDEX idx_audit_user ON audit_logs(user_id);
CREATE INDEX idx_audit_entity ON audit_logs(entity_type, entity_id);
CREATE INDEX idx_audit_created ON audit_logs(created_at);

-- =====================================================
-- VIEWS FOR COMMON QUERIES
-- =====================================================

-- Portfolio Summary View
CREATE VIEW v_portfolio_summary AS
SELECT 
    pc.company_id,
    pc.company_name,
    pc.fund_id,
    f.fund_name,
    pc.sector,
    pc.investment_date,
    pc.ownership_percentage,
    
    -- Latest financials
    fm.revenue AS latest_revenue,
    fm.ebitda AS latest_ebitda,
    fm.ebitda_margin,
    fm.period_date AS latest_financials_date,
    
    -- Latest valuation
    v.equity_value AS current_equity_value,
    v.unrealized_moic,
    v.unrealized_irr,
    v.valuation_date AS latest_valuation_date,
    
    pc.company_status,
    pc.risk_rating
FROM 
    portfolio_companies pc
    JOIN funds f ON pc.fund_id = f.fund_id
    LEFT JOIN LATERAL (
        SELECT * FROM financial_metrics 
        WHERE company_id = pc.company_id 
        ORDER BY period_date DESC 
        LIMIT 1
    ) fm ON TRUE
    LEFT JOIN LATERAL (
        SELECT * FROM valuations 
        WHERE company_id = pc.company_id AND status = 'Approved'
        ORDER BY valuation_date DESC 
        LIMIT 1
    ) v ON TRUE;

-- Fund Performance View
CREATE VIEW v_fund_performance AS
SELECT 
    f.fund_id,
    f.fund_name,
    f.vintage_year,
    f.fund_size,
    f.committed_capital,
    f.drawn_capital,
    f.distributed_capital,
    
    COUNT(DISTINCT pc.company_id) AS portfolio_companies_count,
    SUM(pc.equity_invested) AS total_equity_invested,
    SUM(v.equity_value) AS total_current_value,
    SUM(v.unrealized_gain) AS total_unrealized_gain,
    
    AVG(v.unrealized_moic) AS avg_moic,
    AVG(v.unrealized_irr) AS avg_irr
FROM 
    funds f
    LEFT JOIN portfolio_companies pc ON f.fund_id = pc.fund_id
    LEFT JOIN LATERAL (
        SELECT * FROM valuations 
        WHERE company_id = pc.company_id AND status = 'Approved'
        ORDER BY valuation_date DESC 
        LIMIT 1
    ) v ON TRUE
GROUP BY 
    f.fund_id, f.fund_name, f.vintage_year, f.fund_size, 
    f.committed_capital, f.drawn_capital, f.distributed_capital;
```

---

## Python Data Models (SQLAlchemy)

```python
from sqlalchemy import Column, String, Integer, Numeric, Date, DateTime, Boolean, Text, ARRAY, JSON
from sqlalchemy.dialects.postgresql import UUID, INET, JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class Fund(Base):
    __tablename__ = 'funds'
    
    fund_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fund_name = Column(String(255), nullable=False)
    fund_number = Column(Integer)
    vintage_year = Column(Integer, nullable=False)
    fund_size = Column(Numeric(15, 2), nullable=False)
    committed_capital = Column(Numeric(15, 2), nullable=False)
    drawn_capital = Column(Numeric(15, 2), default=0)
    distributed_capital = Column(Numeric(15, 2), default=0)
    target_irr = Column(Numeric(5, 4))
    fund_strategy = Column(String(100))
    sector_focus = Column(ARRAY(Text))
    geographic_focus = Column(ARRAY(Text))
    fund_status = Column(String(50), default='Active')
    inception_date = Column(Date)
    close_date = Column(Date)
    final_close_date = Column(Date)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_by = Column(UUID(as_uuid=True))

class PortfolioCompany(Base):
    __tablename__ = 'portfolio_companies'
    
    company_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fund_id = Column(UUID(as_uuid=True), nullable=False)
    company_name = Column(String(255), nullable=False)
    company_legal_name = Column(String(255))
    ticker_symbol = Column(String(10))
    website = Column(String(255))
    
    investment_date = Column(Date, nullable=False)
    deal_type = Column(String(50), nullable=False)
    sector = Column(String(100), nullable=False)
    industry = Column(String(100))
    sub_sector = Column(String(100))
    business_description = Column(Text)
    
    headquarters_city = Column(String(100))
    headquarters_state = Column(String(100))
    headquarters_country = Column(String(100), default='United States')
    
    entry_revenue = Column(Numeric(15, 2))
    entry_ebitda = Column(Numeric(15, 2))
    entry_multiple = Column(Numeric(10, 2))
    purchase_price = Column(Numeric(15, 2))
    equity_invested = Column(Numeric(15, 2))
    debt_raised = Column(Numeric(15, 2))
    ownership_percentage = Column(Numeric(5, 4))
    
    company_status = Column(String(50), default='Active')
    exit_date = Column(Date)
    exit_type = Column(String(50))
    exit_proceeds = Column(Numeric(15, 2))
    realized_moic = Column(Numeric(10, 2))
    realized_irr = Column(Numeric(10, 4))
    
    risk_rating = Column(String(20), default='Medium')
    internal_rating = Column(String(10))
    
    ceo_name = Column(String(255))
    cfo_name = Column(String(255))
    board_members = Column(ARRAY(Text))
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_by = Column(UUID(as_uuid=True))

class FinancialMetric(Base):
    __tablename__ = 'financial_metrics'
    
    metric_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), nullable=False)
    
    period_date = Column(Date, nullable=False)
    period_type = Column(String(20), nullable=False)
    fiscal_year = Column(Integer, nullable=False)
    fiscal_quarter = Column(Integer)
    fiscal_month = Column(Integer)
    
    # Income Statement
    revenue = Column(Numeric(15, 2))
    cogs = Column(Numeric(15, 2))
    gross_profit = Column(Numeric(15, 2))
    gross_margin = Column(Numeric(5, 4))
    
    operating_expenses = Column(Numeric(15, 2))
    sales_marketing = Column(Numeric(15, 2))
    research_development = Column(Numeric(15, 2))
    general_admin = Column(Numeric(15, 2))
    
    ebitda = Column(Numeric(15, 2))
    ebitda_margin = Column(Numeric(5, 4))
    adjusted_ebitda = Column(Numeric(15, 2))
    adjusted_ebitda_margin = Column(Numeric(5, 4))
    
    depreciation = Column(Numeric(15, 2))
    amortization = Column(Numeric(15, 2))
    ebit = Column(Numeric(15, 2))
    
    interest_expense = Column(Numeric(15, 2))
    interest_income = Column(Numeric(15, 2))
    other_income = Column(Numeric(15, 2))
    
    ebt = Column(Numeric(15, 2))
    tax_expense = Column(Numeric(15, 2))
    tax_rate = Column(Numeric(5, 4))
    net_income = Column(Numeric(15, 2))
    net_margin = Column(Numeric(5, 4))
    
    # Balance Sheet
    cash = Column(Numeric(15, 2))
    accounts_receivable = Column(Numeric(15, 2))
    inventory = Column(Numeric(15, 2))
    prepaid_expenses = Column(Numeric(15, 2))
    other_current_assets = Column(Numeric(15, 2))
    total_current_assets = Column(Numeric(15, 2))
    
    ppe_gross = Column(Numeric(15, 2))
    accumulated_depreciation = Column(Numeric(15, 2))
    ppe_net = Column(Numeric(15, 2))
    intangible_assets = Column(Numeric(15, 2))
    goodwill = Column(Numeric(15, 2))
    other_longterm_assets = Column(Numeric(15, 2))
    total_assets = Column(Numeric(15, 2))
    
    accounts_payable = Column(Numeric(15, 2))
    accrued_expenses = Column(Numeric(15, 2))
    current_portion_debt = Column(Numeric(15, 2))
    other_current_liabilities = Column(Numeric(15, 2))
    total_current_liabilities = Column(Numeric(15, 2))
    
    long_term_debt = Column(Numeric(15, 2))
    deferred_taxes = Column(Numeric(15, 2))
    other_longterm_liabilities = Column(Numeric(15, 2))
    total_liabilities = Column(Numeric(15, 2))
    
    shareholders_equity = Column(Numeric(15, 2))
    retained_earnings = Column(Numeric(15, 2))
    
    # Cash Flow Statement
    operating_cash_flow = Column(Numeric(15, 2))
    capex = Column(Numeric(15, 2))
    investing_cash_flow = Column(Numeric(15, 2))
    financing_cash_flow = Column(Numeric(15, 2))
    net_cash_flow = Column(Numeric(15, 2))
    free_cash_flow = Column(Numeric(15, 2))
    
    working_capital = Column(Numeric(15, 2))
    net_working_capital = Column(Numeric(15, 2))
    nwc_percent_revenue = Column(Numeric(5, 4))
    
    data_source = Column(String(100))
    data_source_file_id = Column(UUID(as_uuid=True))
    verified = Column(Boolean, default=False)
    verified_by = Column(UUID(as_uuid=True))
    verified_at = Column(DateTime)
    
    notes = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_by = Column(UUID(as_uuid=True))

class Valuation(Base):
    __tablename__ = 'valuations'
    
    valuation_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), nullable=False)
    
    valuation_date = Column(Date, nullable=False)
    valuation_type = Column(String(50), nullable=False)
    
    # DCF
    dcf_enterprise_value = Column(Numeric(15, 2))
    dcf_equity_value = Column(Numeric(15, 2))
    dcf_terminal_value = Column(Numeric(15, 2))
    dcf_pv_terminal_value = Column(Numeric(15, 2))
    dcf_wacc = Column(Numeric(5, 4))
    dcf_terminal_growth = Column(Numeric(5, 4))
    dcf_projection_years = Column(Integer)
    
    # Comps
    comp_ev_revenue_multiple = Column(Numeric(10, 2))
    comp_ev_ebitda_multiple = Column(Numeric(10, 2))
    comp_ev_ebit_multiple = Column(Numeric(10, 2))
    comp_pe_ratio = Column(Numeric(10, 2))
    implied_ev_from_revenue = Column(Numeric(15, 2))
    implied_ev_from_ebitda = Column(Numeric(15, 2))
    
    # Final
    enterprise_value = Column(Numeric(15, 2), nullable=False)
    net_debt = Column(Numeric(15, 2))
    equity_value = Column(Numeric(15, 2), nullable=False)
    
    cost_basis = Column(Numeric(15, 2))
    unrealized_gain = Column(Numeric(15, 2))
    unrealized_moic = Column(Numeric(10, 2))
    unrealized_irr = Column(Numeric(10, 4))
    
    valuation_assumptions = Column(JSONB)
    valuation_model_file_id = Column(UUID(as_uuid=True))
    
    status = Column(String(50), default='Draft')
    approved_by = Column(UUID(as_uuid=True))
    approved_at = Column(DateTime)
    
    notes = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_by = Column(UUID(as_uuid=True))

# ... Additional models for other tables ...
```

---

## Sample API Routes (FastAPI)

```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas

app = FastAPI()

# Companies
@app.get("/api/v1/companies", response_model=List[schemas.CompanyList])
def get_companies(
    fund_id: str = None,
    status: str = "Active",
    db: Session = Depends(get_db)
):
    query = db.query(models.PortfolioCompany)
    if fund_id:
        query = query.filter(models.PortfolioCompany.fund_id == fund_id)
    if status:
        query = query.filter(models.PortfolioCompany.company_status == status)
    return query.all()

@app.post("/api/v1/companies", response_model=schemas.Company)
def create_company(
    company: schemas.CompanyCreate,
    db: Session = Depends(get_db)
):
    db_company = models.PortfolioCompany(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

@app.get("/api/v1/companies/{company_id}", response_model=schemas.CompanyDetail)
def get_company(
    company_id: str,
    db: Session = Depends(get_db)
):
    company = db.query(models.PortfolioCompany).filter(
        models.PortfolioCompany.company_id == company_id
    ).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

# Financials
@app.post("/api/v1/companies/{company_id}/financials")
def add_financials(
    company_id: str,
    financials: schemas.FinancialMetricCreate,
    db: Session = Depends(get_db)
):
    db_metric = models.FinancialMetric(
        company_id=company_id,
        **financials.dict()
    )
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric

@app.get("/api/v1/companies/{company_id}/financials")
def get_financials(
    company_id: str,
    period_type: str = "Quarterly",
    limit: int = 8,
    db: Session = Depends(get_db)
):
    metrics = db.query(models.FinancialMetric).filter(
        models.FinancialMetric.company_id == company_id,
        models.FinancialMetric.period_type == period_type
    ).order_by(models.FinancialMetric.period_date.desc()).limit(limit).all()
    return metrics

# PDF Processing
@app.post("/api/v1/documents/upload")
async def upload_document(
    file: UploadFile,
    company_id: str,
    document_type: str,
    db: Session = Depends(get_db)
):
    # Save file to S3
    file_path = await save_to_s3(file)
    
    # Create document record
    document = models.Document(
        company_id=company_id,
        document_name=file.filename,
        document_type=document_type,
        file_path=file_path,
        extraction_status='Pending'
    )
    db.add(document)
    db.commit()
    
    # Queue for extraction
    queue_for_extraction(document.document_id)
    
    return {"document_id": document.document_id, "status": "uploaded"}

@app.post("/api/v1/documents/{document_id}/extract")
async def extract_document(
    document_id: str,
    db: Session = Depends(get_db)
):
    document = db.query(models.Document).filter(
        models.Document.document_id == document_id
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Update status
    document.extraction_status = 'Processing'
    db.commit()
    
    # Run extraction (async task)
    result = await extract_financial_data(document.file_path)
    
    # Save results
    document.extracted_data = result['data']
    document.extraction_confidence = result['confidence']
    document.extraction_status = 'Complete'
    document.needs_review = result['confidence'] < 0.9
    db.commit()
    
    return result
```

---

*This provides the complete database foundation for the Portfolio Dashboard platform.*
