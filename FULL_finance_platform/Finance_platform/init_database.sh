#!/bin/bash

#######################################################################
# Portfolio Dashboard - Database Initialization Script
#######################################################################
#
# This script initializes the PostgreSQL database for Portfolio Dashboard
# It creates:
# - Database and user (if not exists)
# - All tables with proper relationships
# - Indexes for performance
# - Sample data (optional)
#
# Prerequisites:
# - PostgreSQL 14+ running
# - Sufficient permissions to create databases
#
# Usage:
#   bash init_database.sh
#
#######################################################################

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

echo "======================================================================="
echo "  Portfolio Dashboard - Database Initialization"
echo "======================================================================="
echo ""

# Database configuration
DB_NAME="portfolio_dashboard"
DB_USER="portfolio_user"
DB_PASSWORD="password"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

log_info "Database: $DB_NAME"
log_info "User: $DB_USER"
echo ""

# Check PostgreSQL is running
log_info "Checking PostgreSQL status..."
if ! pg_isready &> /dev/null; then
    log_error "PostgreSQL is not running. Please start it first."
    exit 1
fi
log_success "PostgreSQL is running"
echo ""

# Create database and user if not exists
log_info "Setting up database and user..."
psql -U postgres -tc "SELECT 1 FROM pg_roles WHERE rolname = '$DB_USER'" | grep -q 1 || \
    psql -U postgres -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'" | grep -q 1 || \
    psql -U postgres -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
log_success "Database and user ready"
echo ""

# Create schema SQL
log_info "Creating database schema..."

# Create a temporary SQL file with the schema
cat > /tmp/portfolio_schema.sql << 'EOF'
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table (must be created first due to foreign keys)
CREATE TABLE IF NOT EXISTS users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    role VARCHAR(50) NOT NULL DEFAULT 'Analyst',
    firm_name VARCHAR(255),
    password_hash VARCHAR(255) NOT NULL,
    two_factor_enabled BOOLEAN DEFAULT FALSE,
    two_factor_secret VARCHAR(255),
    funds_access UUID[],
    companies_access UUID[],
    last_login TIMESTAMP,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_role CHECK (role IN ('Admin', 'Partner', 'Associate', 'Analyst', 'LP', 'Viewer', 'PortCo'))
);

-- Funds table
CREATE TABLE IF NOT EXISTS funds (
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
CREATE TABLE IF NOT EXISTS portfolio_companies (
    company_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    fund_id UUID NOT NULL REFERENCES funds(fund_id) ON DELETE CASCADE,
    company_name VARCHAR(255) NOT NULL,
    company_legal_name VARCHAR(255),
    ticker_symbol VARCHAR(10),
    website VARCHAR(255),
    investment_date DATE NOT NULL,
    deal_type VARCHAR(50) NOT NULL,
    sector VARCHAR(100) NOT NULL,
    industry VARCHAR(100),
    sub_sector VARCHAR(100),
    business_description TEXT,
    headquarters_city VARCHAR(100),
    headquarters_state VARCHAR(100),
    headquarters_country VARCHAR(100) DEFAULT 'United States',
    entry_revenue DECIMAL(15, 2),
    entry_ebitda DECIMAL(15, 2),
    entry_multiple DECIMAL(10, 2),
    purchase_price DECIMAL(15, 2),
    equity_invested DECIMAL(15, 2),
    debt_raised DECIMAL(15, 2),
    ownership_percentage DECIMAL(5, 4),
    company_status VARCHAR(50) DEFAULT 'Active',
    exit_date DATE,
    exit_type VARCHAR(50),
    exit_proceeds DECIMAL(15, 2),
    realized_moic DECIMAL(10, 2),
    realized_irr DECIMAL(10, 4),
    risk_rating VARCHAR(20) DEFAULT 'Medium',
    internal_rating VARCHAR(10),
    ceo_name VARCHAR(255),
    cfo_name VARCHAR(255),
    board_members TEXT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES users(user_id),
    CONSTRAINT ownership_valid CHECK (ownership_percentage >= 0 AND ownership_percentage <= 1),
    CONSTRAINT status_valid CHECK (company_status IN ('Active', 'Exited', 'Written Off', 'On Hold'))
);

-- Documents table
CREATE TABLE IF NOT EXISTS documents (
    document_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID REFERENCES portfolio_companies(company_id) ON DELETE CASCADE,
    fund_id UUID REFERENCES funds(fund_id) ON DELETE CASCADE,
    document_name VARCHAR(255) NOT NULL,
    document_type VARCHAR(100) NOT NULL,
    document_category VARCHAR(100),
    file_path VARCHAR(500) NOT NULL,
    file_size_bytes BIGINT,
    file_type VARCHAR(50),
    extraction_status VARCHAR(50),
    extraction_confidence DECIMAL(5, 4),
    extracted_data JSONB,
    needs_review BOOLEAN DEFAULT FALSE,
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

-- Financial Metrics table
CREATE TABLE IF NOT EXISTS financial_metrics (
    metric_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES portfolio_companies(company_id) ON DELETE CASCADE,
    period_date DATE NOT NULL,
    period_type VARCHAR(20) NOT NULL,
    fiscal_year INTEGER NOT NULL,
    fiscal_quarter INTEGER,
    fiscal_month INTEGER,
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
    operating_cash_flow DECIMAL(15, 2),
    capex DECIMAL(15, 2),
    investing_cash_flow DECIMAL(15, 2),
    financing_cash_flow DECIMAL(15, 2),
    net_cash_flow DECIMAL(15, 2),
    free_cash_flow DECIMAL(15, 2),
    working_capital DECIMAL(15, 2),
    net_working_capital DECIMAL(15, 2),
    nwc_percent_revenue DECIMAL(5, 4),
    data_source VARCHAR(100),
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

-- Company KPIs table
CREATE TABLE IF NOT EXISTS company_kpis (
    kpi_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES portfolio_companies(company_id) ON DELETE CASCADE,
    period_date DATE NOT NULL,
    period_type VARCHAR(20) NOT NULL,
    arr DECIMAL(15, 2),
    mrr DECIMAL(15, 2),
    net_revenue_retention DECIMAL(5, 4),
    gross_revenue_retention DECIMAL(5, 4),
    customer_churn_rate DECIMAL(5, 4),
    revenue_churn_rate DECIMAL(5, 4),
    total_customers INTEGER,
    new_customers INTEGER,
    churned_customers INTEGER,
    active_customers INTEGER,
    arpu DECIMAL(15, 2),
    cac DECIMAL(15, 2),
    ltv DECIMAL(15, 2),
    ltv_cac_ratio DECIMAL(10, 2),
    magic_number DECIMAL(10, 2),
    sales_efficiency DECIMAL(10, 2),
    headcount INTEGER,
    revenue_per_employee DECIMAL(15, 2),
    gross_margin_per_employee DECIMAL(15, 2),
    monthly_active_users INTEGER,
    daily_active_users INTEGER,
    nps_score INTEGER,
    product_adoption_rate DECIMAL(5, 4),
    gmv DECIMAL(15, 2),
    take_rate DECIMAL(5, 4),
    average_order_value DECIMAL(15, 2),
    orders INTEGER,
    custom_kpis JSONB,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_company_kpi_period UNIQUE (company_id, period_date, period_type)
);

-- Valuations table
CREATE TABLE IF NOT EXISTS valuations (
    valuation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES portfolio_companies(company_id) ON DELETE CASCADE,
    valuation_date DATE NOT NULL,
    valuation_type VARCHAR(50) NOT NULL,
    dcf_enterprise_value DECIMAL(15, 2),
    dcf_equity_value DECIMAL(15, 2),
    dcf_terminal_value DECIMAL(15, 2),
    dcf_pv_terminal_value DECIMAL(15, 2),
    dcf_wacc DECIMAL(5, 4),
    dcf_terminal_growth DECIMAL(5, 4),
    dcf_projection_years INTEGER,
    comp_ev_revenue_multiple DECIMAL(10, 2),
    comp_ev_ebitda_multiple DECIMAL(10, 2),
    comp_ev_ebit_multiple DECIMAL(10, 2),
    comp_pe_ratio DECIMAL(10, 2),
    implied_ev_from_revenue DECIMAL(15, 2),
    implied_ev_from_ebitda DECIMAL(15, 2),
    precedent_ev_revenue DECIMAL(10, 2),
    precedent_ev_ebitda DECIMAL(10, 2),
    precedent_premium_paid DECIMAL(5, 4),
    enterprise_value DECIMAL(15, 2) NOT NULL,
    net_debt DECIMAL(15, 2),
    equity_value DECIMAL(15, 2) NOT NULL,
    cost_basis DECIMAL(15, 2),
    unrealized_gain DECIMAL(15, 2),
    unrealized_moic DECIMAL(10, 2),
    unrealized_irr DECIMAL(10, 4),
    valuation_assumptions JSONB,
    valuation_model_file_id UUID REFERENCES documents(document_id),
    status VARCHAR(50) DEFAULT 'Draft',
    approved_by UUID REFERENCES users(user_id),
    approved_at TIMESTAMP,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES users(user_id),
    CONSTRAINT valid_valuation_status CHECK (status IN ('Draft', 'Pending', 'Approved', 'Rejected'))
);

-- Due Diligence table
CREATE TABLE IF NOT EXISTS due_diligence (
    dd_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES portfolio_companies(company_id) ON DELETE CASCADE,
    dd_phase VARCHAR(50) NOT NULL,
    dd_start_date DATE NOT NULL,
    dd_target_end_date DATE,
    dd_actual_end_date DATE,
    overall_status VARCHAR(50) DEFAULT 'Not Started',
    overall_completion_pct DECIMAL(5, 4) DEFAULT 0,
    total_items INTEGER DEFAULT 0,
    completed_items INTEGER DEFAULT 0,
    high_priority_open INTEGER DEFAULT 0,
    red_flags_count INTEGER DEFAULT 0,
    dd_recommendation VARCHAR(50),
    dd_summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES users(user_id)
);

-- Value Creation Initiatives table
CREATE TABLE IF NOT EXISTS value_creation_initiatives (
    initiative_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES portfolio_companies(company_id) ON DELETE CASCADE,
    initiative_name VARCHAR(255) NOT NULL,
    initiative_category VARCHAR(100) NOT NULL,
    description TEXT,
    owner_name VARCHAR(255),
    owner_user_id UUID REFERENCES users(user_id),
    start_date DATE,
    target_completion_date DATE,
    actual_completion_date DATE,
    investment_required DECIMAL(15, 2),
    target_revenue_impact DECIMAL(15, 2),
    target_ebitda_impact DECIMAL(15, 2),
    target_completion_year INTEGER,
    actual_revenue_impact DECIMAL(15, 2),
    actual_ebitda_impact DECIMAL(15, 2),
    status VARCHAR(50) DEFAULT 'Planning',
    completion_pct DECIMAL(5, 4) DEFAULT 0,
    milestones JSONB,
    kpis JSONB,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES users(user_id),
    CONSTRAINT valid_status CHECK (status IN ('Planning', 'In Progress', 'Complete', 'On Hold', 'Cancelled'))
);

-- Audit Log table
CREATE TABLE IF NOT EXISTS audit_logs (
    log_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id),
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(100) NOT NULL,
    entity_id UUID NOT NULL,
    changes JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_companies_fund ON portfolio_companies(fund_id);
CREATE INDEX IF NOT EXISTS idx_companies_status ON portfolio_companies(company_status);
CREATE INDEX IF NOT EXISTS idx_companies_sector ON portfolio_companies(sector);
CREATE INDEX IF NOT EXISTS idx_companies_investment_date ON portfolio_companies(investment_date);

CREATE INDEX IF NOT EXISTS idx_financials_company ON financial_metrics(company_id);
CREATE INDEX IF NOT EXISTS idx_financials_period ON financial_metrics(period_date);
CREATE INDEX IF NOT EXISTS idx_financials_company_period ON financial_metrics(company_id, period_date);

CREATE INDEX IF NOT EXISTS idx_kpis_company ON company_kpis(company_id);
CREATE INDEX IF NOT EXISTS idx_kpis_period ON company_kpis(period_date);

CREATE INDEX IF NOT EXISTS idx_valuations_company ON valuations(company_id);
CREATE INDEX IF NOT EXISTS idx_valuations_date ON valuations(valuation_date);

CREATE INDEX IF NOT EXISTS idx_documents_company ON documents(company_id);
CREATE INDEX IF NOT EXISTS idx_documents_fund ON documents(fund_id);
CREATE INDEX IF NOT EXISTS idx_documents_type ON documents(document_type);

CREATE INDEX IF NOT EXISTS idx_audit_user ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_entity ON audit_logs(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_audit_created ON audit_logs(created_at);

EOF

# Execute the schema
psql -U postgres -d $DB_NAME -f /tmp/portfolio_schema.sql
rm /tmp/portfolio_schema.sql

log_success "Database schema created successfully"
echo ""

# Verify tables
log_info "Verifying tables..."
TABLE_COUNT=$(psql -U postgres -d $DB_NAME -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE';")
log_success "$TABLE_COUNT tables created"
echo ""

echo "======================================================================="
echo "  Database Initialization Complete!"
echo "======================================================================="
echo ""
echo "Database: $DB_NAME"
echo "User: $DB_USER"
echo "Tables: $TABLE_COUNT"
echo ""
echo "Connection string:"
echo "  postgresql://$DB_USER:$DB_PASSWORD@localhost:5432/$DB_NAME"
echo ""
echo "To connect:"
echo "  psql -U $DB_USER -d $DB_NAME"
echo ""
echo "======================================================================="
