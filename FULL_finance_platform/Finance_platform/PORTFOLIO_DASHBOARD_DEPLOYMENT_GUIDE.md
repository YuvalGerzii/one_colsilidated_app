# Portfolio Dashboard - Complete Deployment Guide

## 🎯 Overview

This guide provides step-by-step instructions to deploy the Portfolio Dashboard platform from scratch. The platform centralizes management of 10-100+ portfolio companies with automated Excel model generation, PDF data extraction, and real-time KPI dashboards.

**Tech Stack:**
- **Backend**: Python 3.11+ + FastAPI + PostgreSQL
- **Frontend**: React 18 + TypeScript + Material-UI
- **Excel**: openpyxl (formula preservation)
- **PDF**: pdfplumber + GPT-4 Vision API
- **Deployment**: Docker + AWS (or local)

**Estimated Setup Time**: 2-4 hours

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Structure](#project-structure)
3. [Database Setup](#database-setup)
4. [Backend Setup](#backend-setup)
5. [Frontend Setup](#frontend-setup)
6. [Docker Deployment](#docker-deployment)
7. [AWS Deployment](#aws-deployment)
8. [Development with Claude Code/Cursor](#development-with-claude-codecursor)
9. [Testing & Validation](#testing--validation)
10. [Troubleshooting](#troubleshooting)

---

## 1. Prerequisites

### Required Software

```bash
# Check versions
python --version        # 3.11 or higher
node --version          # 16 or higher
npm --version           # 8 or higher
psql --version          # PostgreSQL 14 or higher
docker --version        # 20 or higher (optional)
git --version           # 2.30 or higher
```

### Installation Commands

**macOS (Homebrew)**:
```bash
brew install python@3.11 node postgresql@14 docker
```

**Ubuntu/Debian**:
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv nodejs npm postgresql-14 docker.io
```

**Windows**:
- Python: https://www.python.org/downloads/
- Node.js: https://nodejs.org/
- PostgreSQL: https://www.postgresql.org/download/windows/
- Docker Desktop: https://www.docker.com/products/docker-desktop

### API Keys Required

1. **OpenAI API Key** (for PDF extraction)
   - Sign up: https://platform.openai.com/
   - Cost: ~$20/month for 100 portfolio companies

2. **Financial Datasets API Key** (optional, for market data)
   - Sign up: https://financialdatasets.ai/
   - Free tier: 100 requests/day

---

## 2. Project Structure

Create the following directory structure:

```
portfolio-dashboard/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── auth.py
│   │   ├── config.py
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── companies.py
│   │   │   ├── financials.py
│   │   │   ├── models.py
│   │   │   ├── pdf.py
│   │   │   └── dashboards.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── pdf_extractor.py
│   │   │   ├── model_generator.py
│   │   │   └── excel_builder.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── validators.py
│   ├── tests/
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── types/
│   │   ├── App.tsx
│   │   └── index.tsx
│   ├── package.json
│   ├── tsconfig.json
│   └── Dockerfile
├── database/
│   ├── init/
│   │   ├── 01_schema.sql
│   │   ├── 02_seed_data.sql
│   │   └── 03_indexes.sql
│   └── migrations/
├── docker-compose.yml
├── .gitignore
└── README.md
```

### Quick Setup Script

```bash
#!/bin/bash
# setup_project.sh

echo "Creating Portfolio Dashboard project structure..."

mkdir -p portfolio-dashboard/{backend/{app/{routers,services,utils},tests},frontend/src/{components,pages,services,types},database/{init,migrations}}

cd portfolio-dashboard

# Create placeholder files
touch backend/app/__init__.py
touch backend/requirements.txt
touch backend/.env.example
touch frontend/package.json
touch docker-compose.yml
touch .gitignore

echo "✅ Project structure created!"
echo "📂 Location: $(pwd)"
```

---

## 3. Database Setup

### 3.1 Install PostgreSQL

**Verify installation:**
```bash
psql --version
# Expected: psql (PostgreSQL) 14.x or higher
```

### 3.2 Create Database

```bash
# Start PostgreSQL service
# macOS: brew services start postgresql@14
# Linux: sudo systemctl start postgresql
# Windows: Start from Services panel

# Connect as postgres user
sudo -u postgres psql

# Or on Windows: psql -U postgres
```

**In the PostgreSQL prompt:**
```sql
-- Create database
CREATE DATABASE portfolio_dashboard;

-- Create user
CREATE USER portfolio_user WITH ENCRYPTED PASSWORD 'change_this_password_123!';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE portfolio_dashboard TO portfolio_user;

-- Connect to the database
\c portfolio_dashboard

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO portfolio_user;

-- Exit
\q
```

### 3.3 Initialize Schema

Create `database/init/01_schema.sql`:

```sql
-- ============================================================================
-- PORTFOLIO DASHBOARD - DATABASE SCHEMA
-- ============================================================================
-- Based on: Portfolio_Dashboard_Database_Schema.md
-- Version: 1.0.0
-- Date: November 2025
-- ============================================================================

-- Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm"; -- For text search

-- ============================================================================
-- TABLE 1: Funds
-- ============================================================================
CREATE TABLE funds (
    fund_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fund_name VARCHAR(255) NOT NULL UNIQUE,
    vintage_year INTEGER NOT NULL,
    fund_size DECIMAL(18,2) NOT NULL,
    committed_capital DECIMAL(18,2) NOT NULL DEFAULT 0,
    drawn_capital DECIMAL(18,2) DEFAULT 0,
    fund_strategy VARCHAR(100),
    target_irr DECIMAL(5,2),
    fund_status VARCHAR(50) DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE funds IS 'Private equity funds managed by the firm';

-- ============================================================================
-- TABLE 2: Portfolio Companies
-- ============================================================================
CREATE TABLE portfolio_companies (
    company_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fund_id UUID NOT NULL REFERENCES funds(fund_id) ON DELETE CASCADE,
    company_name VARCHAR(255) NOT NULL,
    sector VARCHAR(100),
    industry VARCHAR(100),
    geography VARCHAR(100),
    investment_date DATE NOT NULL,
    purchase_price DECIMAL(18,2),
    equity_invested DECIMAL(18,2),
    debt_raised DECIMAL(18,2) DEFAULT 0,
    ownership_percentage DECIMAL(5,2),
    board_seats INTEGER DEFAULT 0,
    company_status VARCHAR(50) DEFAULT 'Active',
    exit_date DATE,
    exit_value DECIMAL(18,2),
    exit_multiple DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT unique_company_fund UNIQUE(company_name, fund_id)
);

COMMENT ON TABLE portfolio_companies IS 'Portfolio companies within each fund';
CREATE INDEX idx_companies_fund ON portfolio_companies(fund_id);
CREATE INDEX idx_companies_status ON portfolio_companies(company_status);
CREATE INDEX idx_companies_sector ON portfolio_companies(sector);

-- ============================================================================
-- TABLE 3: Financial Metrics (Time Series)
-- ============================================================================
CREATE TABLE financial_metrics (
    metric_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID NOT NULL REFERENCES portfolio_companies(company_id) ON DELETE CASCADE,
    period_date DATE NOT NULL,
    period_type VARCHAR(20) CHECK (period_type IN ('Annual', 'Quarterly', 'Monthly')),
    fiscal_year INTEGER NOT NULL,
    fiscal_quarter INTEGER CHECK (fiscal_quarter BETWEEN 1 AND 4),
    
    -- Income Statement
    revenue DECIMAL(18,2),
    gross_profit DECIMAL(18,2),
    operating_expenses DECIMAL(18,2),
    ebitda DECIMAL(18,2),
    ebit DECIMAL(18,2),
    interest_expense DECIMAL(18,2),
    taxes DECIMAL(18,2),
    net_income DECIMAL(18,2),
    
    -- Cash Flow Statement
    operating_cash_flow DECIMAL(18,2),
    capex DECIMAL(18,2),
    free_cash_flow DECIMAL(18,2),
    
    -- Balance Sheet
    cash DECIMAL(18,2),
    accounts_receivable DECIMAL(18,2),
    inventory DECIMAL(18,2),
    total_assets DECIMAL(18,2),
    total_liabilities DECIMAL(18,2),
    total_debt DECIMAL(18,2),
    shareholders_equity DECIMAL(18,2),
    
    -- Metrics
    gross_margin DECIMAL(5,2),
    ebitda_margin DECIMAL(5,2),
    net_margin DECIMAL(5,2),
    roa DECIMAL(5,2),
    roe DECIMAL(5,2),
    debt_to_equity DECIMAL(5,2),
    
    data_source VARCHAR(100) DEFAULT 'Manual Entry',
    confidence_score DECIMAL(3,2), -- For AI-extracted data
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT unique_company_period UNIQUE(company_id, period_date, period_type)
);

COMMENT ON TABLE financial_metrics IS 'Time-series financial data for portfolio companies';
CREATE INDEX idx_metrics_company ON financial_metrics(company_id);
CREATE INDEX idx_metrics_date ON financial_metrics(period_date DESC);
CREATE INDEX idx_metrics_year ON financial_metrics(fiscal_year DESC);

-- ============================================================================
-- TABLE 4: Company KPIs
-- ============================================================================
CREATE TABLE company_kpis (
    kpi_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID NOT NULL REFERENCES portfolio_companies(company_id) ON DELETE CASCADE,
    period_date DATE NOT NULL,
    
    -- Operational KPIs
    employees INTEGER,
    customers INTEGER,
    customer_churn_rate DECIMAL(5,2),
    nps_score DECIMAL(5,2),
    arr DECIMAL(18,2), -- Annual Recurring Revenue
    mrr DECIMAL(18,2), -- Monthly Recurring Revenue
    
    -- Unit Economics
    cac DECIMAL(10,2), -- Customer Acquisition Cost
    ltv DECIMAL(10,2), -- Lifetime Value
    ltv_cac_ratio DECIMAL(5,2),
    
    -- Custom KPIs (JSON for flexibility)
    custom_kpis JSONB,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT unique_company_kpi_period UNIQUE(company_id, period_date)
);

CREATE INDEX idx_kpis_company ON company_kpis(company_id);
CREATE INDEX idx_kpis_date ON company_kpis(period_date DESC);

-- ============================================================================
-- TABLE 5: Valuations
-- ============================================================================
CREATE TABLE valuations (
    valuation_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID NOT NULL REFERENCES portfolio_companies(company_id) ON DELETE CASCADE,
    valuation_date DATE NOT NULL,
    valuation_type VARCHAR(50) CHECK (valuation_type IN ('Fair Value', 'Transaction', 'Model')),
    
    enterprise_value DECIMAL(18,2),
    equity_value DECIMAL(18,2),
    implied_multiple DECIMAL(5,2),
    
    -- Methodology
    method_used VARCHAR(100),
    discount_rate DECIMAL(5,2),
    terminal_growth_rate DECIMAL(5,2),
    comparable_companies TEXT,
    
    -- Model files
    model_file_path VARCHAR(500),
    model_version VARCHAR(50),
    
    notes TEXT,
    created_by UUID,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_valuations_company ON valuations(company_id);
CREATE INDEX idx_valuations_date ON valuations(valuation_date DESC);

-- ============================================================================
-- TABLE 6: Generated Models
-- ============================================================================
CREATE TABLE generated_models (
    model_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID NOT NULL REFERENCES portfolio_companies(company_id) ON DELETE CASCADE,
    model_type VARCHAR(50) NOT NULL CHECK (model_type IN ('DCF', 'LBO', 'Merger', 'DD_Tracker', 'QoE')),
    scenario_name VARCHAR(255) NOT NULL DEFAULT 'Base Case',
    
    -- Model Metadata
    model_version VARCHAR(50),
    template_version VARCHAR(50),
    file_path VARCHAR(500),
    file_size_bytes BIGINT,
    
    -- Model Inputs (stored as JSON for flexibility)
    input_parameters JSONB NOT NULL,
    
    -- Model Outputs
    output_metrics JSONB,
    
    -- Status
    generation_status VARCHAR(50) DEFAULT 'Pending' CHECK (generation_status IN ('Pending', 'Processing', 'Complete', 'Failed')),
    error_message TEXT,
    
    generated_by UUID,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_accessed TIMESTAMP,
    
    CONSTRAINT unique_company_model_scenario UNIQUE(company_id, model_type, scenario_name)
);

CREATE INDEX idx_models_company ON generated_models(company_id);
CREATE INDEX idx_models_type ON generated_models(model_type);
CREATE INDEX idx_models_status ON generated_models(generation_status);

-- ============================================================================
-- TABLE 7: Documents
-- ============================================================================
CREATE TABLE documents (
    document_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID REFERENCES portfolio_companies(company_id) ON DELETE CASCADE,
    fund_id UUID REFERENCES funds(fund_id) ON DELETE CASCADE,
    
    document_name VARCHAR(255) NOT NULL,
    document_type VARCHAR(100),
    file_path VARCHAR(500) NOT NULL,
    file_size_bytes BIGINT,
    mime_type VARCHAR(100),
    
    -- PDF Extraction
    extraction_status VARCHAR(50) CHECK (extraction_status IN ('Pending', 'Processing', 'Complete', 'Failed', 'Not Applicable')),
    extracted_data JSONB,
    confidence_score DECIMAL(3,2),
    
    -- Metadata
    fiscal_period DATE,
    tags TEXT[],
    notes TEXT,
    
    uploaded_by UUID,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CHECK (company_id IS NOT NULL OR fund_id IS NOT NULL)
);

CREATE INDEX idx_documents_company ON documents(company_id);
CREATE INDEX idx_documents_fund ON documents(fund_id);
CREATE INDEX idx_documents_type ON documents(document_type);
CREATE INDEX idx_documents_status ON documents(extraction_status);

-- ============================================================================
-- TABLE 8: Users
-- ============================================================================
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    role VARCHAR(50) DEFAULT 'Analyst' CHECK (role IN ('Admin', 'Partner', 'Principal', 'Associate', 'Analyst', 'LP')),
    
    -- Access Control
    fund_access UUID[] DEFAULT '{}', -- Array of fund_ids user can access
    is_active BOOLEAN DEFAULT true,
    last_login TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);

-- ============================================================================
-- TABLE 9: Audit Log
-- ============================================================================
CREATE TABLE audit_log (
    log_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id),
    action VARCHAR(100) NOT NULL,
    table_name VARCHAR(100),
    record_id UUID,
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_user ON audit_log(user_id);
CREATE INDEX idx_audit_table ON audit_log(table_name);
CREATE INDEX idx_audit_timestamp ON audit_log(timestamp DESC);

-- ============================================================================
-- TABLE 10: Due Diligence Tracker
-- ============================================================================
CREATE TABLE dd_tracker (
    dd_item_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID NOT NULL REFERENCES portfolio_companies(company_id) ON DELETE CASCADE,
    category VARCHAR(100) NOT NULL,
    subcategory VARCHAR(100),
    item_name VARCHAR(255) NOT NULL,
    description TEXT,
    
    -- Status
    status VARCHAR(50) DEFAULT 'Not Started' CHECK (status IN ('Not Started', 'In Progress', 'Complete', 'N/A')),
    priority VARCHAR(20) CHECK (priority IN ('Critical', 'High', 'Medium', 'Low')),
    
    -- Ownership
    assigned_to UUID REFERENCES users(user_id),
    due_date DATE,
    completed_date DATE,
    
    -- Documents
    document_ids UUID[],
    notes TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_dd_company ON dd_tracker(company_id);
CREATE INDEX idx_dd_status ON dd_tracker(status);
CREATE INDEX idx_dd_priority ON dd_tracker(priority);

-- ============================================================================
-- TABLE 11: Value Creation Initiatives
-- ============================================================================
CREATE TABLE value_creation (
    initiative_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID NOT NULL REFERENCES portfolio_companies(company_id) ON DELETE CASCADE,
    initiative_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    description TEXT,
    
    -- Targets
    target_metric VARCHAR(100),
    baseline_value DECIMAL(18,2),
    target_value DECIMAL(18,2),
    current_value DECIMAL(18,2),
    
    -- Timeline
    start_date DATE,
    target_date DATE,
    status VARCHAR(50) DEFAULT 'Planning' CHECK (status IN ('Planning', 'In Progress', 'Complete', 'On Hold', 'Cancelled')),
    
    -- Investment
    capex_required DECIMAL(18,2),
    opex_required DECIMAL(18,2),
    expected_ebitda_impact DECIMAL(18,2),
    
    -- Ownership
    owner UUID REFERENCES users(user_id),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_vc_company ON value_creation(company_id);
CREATE INDEX idx_vc_status ON value_creation(status);

-- ============================================================================
-- TABLE 12: Market Data (from MCP integration)
-- ============================================================================
CREATE TABLE market_data (
    data_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ticker VARCHAR(20) NOT NULL,
    data_date DATE NOT NULL,
    
    -- Price Data
    open_price DECIMAL(10,2),
    high_price DECIMAL(10,2),
    low_price DECIMAL(10,2),
    close_price DECIMAL(10,2),
    volume BIGINT,
    market_cap DECIMAL(18,2),
    
    -- Financial Data
    revenue DECIMAL(18,2),
    ebitda DECIMAL(18,2),
    net_income DECIMAL(18,2),
    total_assets DECIMAL(18,2),
    total_debt DECIMAL(18,2),
    
    -- Multiples
    ev_revenue DECIMAL(5,2),
    ev_ebitda DECIMAL(5,2),
    pe_ratio DECIMAL(5,2),
    
    data_source VARCHAR(100) DEFAULT 'Financial Datasets API',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT unique_ticker_date UNIQUE(ticker, data_date)
);

CREATE INDEX idx_market_ticker ON market_data(ticker);
CREATE INDEX idx_market_date ON market_data(data_date DESC);

-- ============================================================================
-- TABLE 13: Public Comparables
-- ============================================================================
CREATE TABLE public_comparables (
    comp_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID REFERENCES portfolio_companies(company_id) ON DELETE CASCADE,
    ticker VARCHAR(20) NOT NULL,
    company_name VARCHAR(255),
    sector VARCHAR(100),
    is_active BOOLEAN DEFAULT true,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_comps_company ON public_comparables(company_id);
CREATE INDEX idx_comps_ticker ON public_comparables(ticker);

-- ============================================================================
-- VIEWS
-- ============================================================================

-- View: Latest Financials per Company
CREATE VIEW v_latest_financials AS
SELECT DISTINCT ON (company_id)
    fm.*,
    pc.company_name,
    pc.fund_id
FROM financial_metrics fm
JOIN portfolio_companies pc ON fm.company_id = pc.company_id
ORDER BY company_id, period_date DESC;

-- View: Portfolio Summary
CREATE VIEW v_portfolio_summary AS
SELECT 
    f.fund_id,
    f.fund_name,
    COUNT(DISTINCT pc.company_id) as total_companies,
    COUNT(DISTINCT CASE WHEN pc.company_status = 'Active' THEN pc.company_id END) as active_companies,
    SUM(pc.equity_invested) as total_invested,
    SUM(CASE WHEN pc.exit_value IS NOT NULL THEN pc.exit_value ELSE 
        COALESCE(v.equity_value, pc.equity_invested) END) as total_value,
    SUM(COALESCE(lf.ebitda, 0)) as total_ebitda
FROM funds f
LEFT JOIN portfolio_companies pc ON f.fund_id = pc.fund_id
LEFT JOIN valuations v ON pc.company_id = v.company_id AND v.valuation_date = (
    SELECT MAX(valuation_date) FROM valuations WHERE company_id = pc.company_id
)
LEFT JOIN v_latest_financials lf ON pc.company_id = lf.company_id
GROUP BY f.fund_id, f.fund_name;

-- ============================================================================
-- FUNCTIONS
-- ============================================================================

-- Function: Update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for updated_at
CREATE TRIGGER update_funds_updated_at BEFORE UPDATE ON funds
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_companies_updated_at BEFORE UPDATE ON portfolio_companies
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_financials_updated_at BEFORE UPDATE ON financial_metrics
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- PERMISSIONS
-- ============================================================================

-- Grant permissions to portfolio_user
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO portfolio_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO portfolio_user;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO portfolio_user;

-- ============================================================================
-- COMPLETE
-- ============================================================================
```

**Apply the schema:**
```bash
psql -U portfolio_user -d portfolio_dashboard -f database/init/01_schema.sql
```

**Verify tables:**
```bash
psql -U portfolio_user -d portfolio_dashboard -c "\dt"
```

Expected output: 13 tables created

---

## 4. Backend Setup

### 4.1 Create Python Environment

```bash
cd portfolio-dashboard/backend

# Create virtual environment
python3.11 -m venv venv

# Activate it
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# Verify
which python  # Should point to venv/bin/python
```

### 4.2 Create requirements.txt

```txt
# FastAPI Framework
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-multipart==0.0.6

# Database
sqlalchemy==2.0.25
psycopg2-binary==2.9.9
alembic==1.13.1

# Authentication
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0

# Data Validation
pydantic==2.5.3
pydantic-settings==2.1.0

# Excel Processing
openpyxl==3.1.2
xlsxwriter==3.1.9

# PDF Processing
pdfplumber==0.10.3
PyPDF2==3.0.1
pdf2image==1.16.3
pytesseract==0.3.10

# AI / ML
openai==1.10.0

# Date/Time
python-dateutil==2.8.2

# HTTP Requests
httpx==0.26.0
requests==2.31.0

# Testing
pytest==7.4.4
pytest-asyncio==0.23.3

# Utilities
python-slugify==8.0.1
tenacity==8.2.3  # Retry logic
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

### 4.3 Environment Configuration

Create `backend/.env`:

```bash
# Database
DATABASE_URL=postgresql://portfolio_user:change_this_password_123!@localhost:5432/portfolio_dashboard

# Security
SECRET_KEY=your-secret-key-generate-with-openssl-rand-hex-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI API
OPENAI_API_KEY=sk-your-openai-api-key-here

# Financial Datasets API (optional)
FINANCIAL_DATASETS_API_KEY=your-api-key-here

# File Storage
UPLOAD_DIR=/var/uploads/portfolio_dashboard
MAX_UPLOAD_SIZE_MB=50

# Environment
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=INFO

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Redis (optional, for caching)
REDIS_URL=redis://localhost:6379/0
```

**Generate SECRET_KEY:**
```bash
openssl rand -hex 32
```

### 4.4 Create Backend Code

**File: `backend/app/config.py`**

```python
from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # APIs
    OPENAI_API_KEY: str
    FINANCIAL_DATASETS_API_KEY: str = ""
    
    # File Storage
    UPLOAD_DIR: str = "/var/uploads/portfolio_dashboard"
    MAX_UPLOAD_SIZE_MB: int = 50
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()

# Create upload directory
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
```

**File: `backend/app/database.py`**

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=settings.DEBUG
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**File: `backend/app/models.py`** (Sample - based on schema)

```python
from sqlalchemy import Column, String, Integer, Numeric, Date, DateTime, Boolean, Text, ARRAY, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from .database import Base

class Fund(Base):
    __tablename__ = "funds"
    
    fund_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fund_name = Column(String(255), nullable=False, unique=True)
    vintage_year = Column(Integer, nullable=False)
    fund_size = Column(Numeric(18, 2), nullable=False)
    committed_capital = Column(Numeric(18, 2), default=0)
    drawn_capital = Column(Numeric(18, 2), default=0)
    fund_strategy = Column(String(100))
    target_irr = Column(Numeric(5, 2))
    fund_status = Column(String(50), default='Active')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class PortfolioCompany(Base):
    __tablename__ = "portfolio_companies"
    
    company_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fund_id = Column(UUID(as_uuid=True), nullable=False)
    company_name = Column(String(255), nullable=False)
    sector = Column(String(100))
    industry = Column(String(100))
    geography = Column(String(100))
    investment_date = Column(Date, nullable=False)
    purchase_price = Column(Numeric(18, 2))
    equity_invested = Column(Numeric(18, 2))
    debt_raised = Column(Numeric(18, 2), default=0)
    ownership_percentage = Column(Numeric(5, 2))
    board_seats = Column(Integer, default=0)
    company_status = Column(String(50), default='Active')
    exit_date = Column(Date)
    exit_value = Column(Numeric(18, 2))
    exit_multiple = Column(Numeric(5, 2))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class FinancialMetric(Base):
    __tablename__ = "financial_metrics"
    
    metric_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), nullable=False)
    period_date = Column(Date, nullable=False)
    period_type = Column(String(20))
    fiscal_year = Column(Integer, nullable=False)
    fiscal_quarter = Column(Integer)
    
    # Income Statement
    revenue = Column(Numeric(18, 2))
    gross_profit = Column(Numeric(18, 2))
    operating_expenses = Column(Numeric(18, 2))
    ebitda = Column(Numeric(18, 2))
    ebit = Column(Numeric(18, 2))
    interest_expense = Column(Numeric(18, 2))
    taxes = Column(Numeric(18, 2))
    net_income = Column(Numeric(18, 2))
    
    # Cash Flow
    operating_cash_flow = Column(Numeric(18, 2))
    capex = Column(Numeric(18, 2))
    free_cash_flow = Column(Numeric(18, 2))
    
    # Balance Sheet
    cash = Column(Numeric(18, 2))
    accounts_receivable = Column(Numeric(18, 2))
    inventory = Column(Numeric(18, 2))
    total_assets = Column(Numeric(18, 2))
    total_liabilities = Column(Numeric(18, 2))
    total_debt = Column(Numeric(18, 2))
    shareholders_equity = Column(Numeric(18, 2))
    
    # Ratios
    gross_margin = Column(Numeric(5, 2))
    ebitda_margin = Column(Numeric(5, 2))
    net_margin = Column(Numeric(5, 2))
    roa = Column(Numeric(5, 2))
    roe = Column(Numeric(5, 2))
    debt_to_equity = Column(Numeric(5, 2))
    
    data_source = Column(String(100), default='Manual Entry')
    confidence_score = Column(Numeric(3, 2))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class User(Base):
    __tablename__ = "users"
    
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    role = Column(String(50), default='Analyst')
    fund_access = Column(ARRAY(UUID(as_uuid=True)), default=[])
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

**File: `backend/app/main.py`**

```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .config import settings
from .database import engine, Base
import logging

# Configure logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Portfolio Dashboard API",
    description="Private Equity Portfolio Management Platform",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health Check
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "version": "1.0.0"
    }

# Root
@app.get("/")
def read_root():
    return {
        "message": "Portfolio Dashboard API",
        "docs": "/api/docs",
        "health": "/health"
    }

# TODO: Include routers
# from .routers import companies, financials, models, pdf, dashboards
# app.include_router(companies.router, prefix="/api/v1", tags=["companies"])
# app.include_router(financials.router, prefix="/api/v1", tags=["financials"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
```

### 4.5 Run the Backend

```bash
# Make sure you're in backend/ with venv activated

# Run with uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or run directly
python -m app.main
```

**Test it:**
```bash
curl http://localhost:8000/health
# Expected: {"status":"healthy","environment":"development","version":"1.0.0"}

# View API docs:
open http://localhost:8000/api/docs
```

---

## 5. Frontend Setup

### 5.1 Create React App

```bash
cd portfolio-dashboard/frontend

# Create React app with TypeScript
npx create-react-app . --template typescript

# Or use Vite (faster)
npm create vite@latest . -- --template react-ts
```

### 5.2 Install Dependencies

```bash
npm install @mui/material @emotion/react @emotion/styled @mui/icons-material
npm install axios react-router-dom
npm install recharts  # For charts
npm install date-fns  # Date utilities
npm install @tanstack/react-query  # Data fetching

# Dev dependencies
npm install --save-dev @types/node
```

### 5.3 Configure TypeScript

**File: `frontend/tsconfig.json`**

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,

    /* Bundler mode */
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",

    /* Linting */
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    
    /* Path aliases */
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

### 5.4 Create API Service

**File: `frontend/src/services/api.ts`**

```typescript
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor (add auth token)
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor (handle errors)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Redirect to login
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;

// Type Definitions
export interface Fund {
  fund_id: string;
  fund_name: string;
  vintage_year: number;
  fund_size: number;
  committed_capital: number;
  drawn_capital: number;
  fund_strategy?: string;
  target_irr?: number;
  fund_status: string;
}

export interface Company {
  company_id: string;
  fund_id: string;
  company_name: string;
  sector: string;
  industry?: string;
  geography?: string;
  investment_date: string;
  purchase_price?: number;
  equity_invested?: number;
  ownership_percentage?: number;
  company_status: string;
}

export interface FinancialMetric {
  metric_id: string;
  company_id: string;
  period_date: string;
  period_type: string;
  fiscal_year: number;
  fiscal_quarter?: number;
  revenue?: number;
  ebitda?: number;
  net_income?: number;
  // ... other fields
}

// API Functions
export const getFunds = () => api.get<Fund[]>('/funds');
export const getCompanies = (fundId?: string) => 
  api.get<Company[]>('/companies', { params: { fund_id: fundId } });
export const getCompany = (id: string) => api.get<Company>(`/companies/${id}`);
export const getFinancials = (companyId: string) => 
  api.get<FinancialMetric[]>(`/companies/${companyId}/financials`);
```

### 5.5 Run Frontend

```bash
npm start
# Opens http://localhost:3000
```

---

## 6. Docker Deployment

### 6.1 Backend Dockerfile

**File: `backend/Dockerfile`**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 6.2 Frontend Dockerfile

**File: `frontend/Dockerfile`**

```dockerfile
# Build stage
FROM node:18-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine

COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

**File: `frontend/nginx.conf`**

```nginx
server {
    listen 80;
    server_name _;

    root /usr/share/nginx/html;
    index index.html;

    # SPA routing
    location / {
        try_files $uri $uri/ /index.html;
    }

    # API proxy (optional)
    location /api/ {
        proxy_pass http://backend:8000/api/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
}
```

### 6.3 Docker Compose

**File: `docker-compose.yml`**

```yaml
version: '3.8'

services:
  # PostgreSQL Database
  db:
    image: postgres:14-alpine
    container_name: portfolio_db
    environment:
      POSTGRES_DB: portfolio_dashboard
      POSTGRES_USER: portfolio_user
      POSTGRES_PASSWORD: change_this_password_123!
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/init:/docker-entrypoint-initdb.d
    networks:
      - portfolio_network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U portfolio_user -d portfolio_dashboard"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Backend API
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: portfolio_backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://portfolio_user:change_this_password_123!@db:5432/portfolio_dashboard
      SECRET_KEY: ${SECRET_KEY}
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      ENVIRONMENT: production
      DEBUG: "False"
    volumes:
      - ./backend:/app
      - uploads:/var/uploads/portfolio_dashboard
    depends_on:
      db:
        condition: service_healthy
    networks:
      - portfolio_network
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  # Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: portfolio_frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
    networks:
      - portfolio_network

  # Redis (optional, for caching)
  redis:
    image: redis:7-alpine
    container_name: portfolio_redis
    ports:
      - "6379:6379"
    networks:
      - portfolio_network

volumes:
  postgres_data:
  uploads:

networks:
  portfolio_network:
    driver: bridge
```

### 6.4 Run with Docker

```bash
# Create .env file in project root
cat > .env << 'EOF'
SECRET_KEY=your-generated-secret-key-here
OPENAI_API_KEY=sk-your-openai-key-here
FINANCIAL_DATASETS_API_KEY=your-optional-key-here
EOF

# Build and start all services
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes data)
docker-compose down -v
```

**Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api/docs
- Database: localhost:5432

---

## 7. AWS Deployment

### 7.1 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                       AWS Cloud                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐      ┌──────────────┐               │
│  │   Route 53   │─────▶│     ALB      │               │
│  │     DNS      │      │Load Balancer │               │
│  └──────────────┘      └──────┬───────┘               │
│                                │                        │
│                    ┌───────────┴────────────┐          │
│                    │                        │          │
│            ┌───────▼─────┐          ┌──────▼──────┐   │
│            │ ECS Fargate │          │ ECS Fargate │   │
│            │  Frontend   │          │  Backend    │   │
│            │   (React)   │          │  (FastAPI)  │   │
│            └─────────────┘          └──────┬──────┘   │
│                                             │          │
│                                     ┌───────▼────────┐ │
│                                     │   RDS Postgres │ │
│                                     │   (Multi-AZ)   │ │
│                                     └────────────────┘ │
│                                                         │
│  ┌──────────────┐      ┌──────────────┐               │
│  │      S3      │      │ ElastiCache  │               │
│  │   (Files)    │      │   (Redis)    │               │
│  └──────────────┘      └──────────────┘               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 7.2 AWS Setup Script

**File: `deploy/aws-setup.sh`**

```bash
#!/bin/bash

# AWS Portfolio Dashboard Deployment Script
# Prerequisites: AWS CLI configured with appropriate permissions

set -e

# Configuration
AWS_REGION="us-east-1"
PROJECT_NAME="portfolio-dashboard"
ENVIRONMENT="production"

echo "🚀 Starting AWS deployment for Portfolio Dashboard..."
echo "Region: $AWS_REGION"
echo "Environment: $ENVIRONMENT"

# 1. Create VPC and Networking
echo "📡 Creating VPC..."
VPC_ID=$(aws ec2 create-vpc \
  --cidr-block 10.0.0.0/16 \
  --tag-specifications "ResourceType=vpc,Tags=[{Key=Name,Value=$PROJECT_NAME-vpc}]" \
  --query 'Vpc.VpcId' \
  --output text \
  --region $AWS_REGION)

echo "✅ VPC created: $VPC_ID"

# Enable DNS hostnames
aws ec2 modify-vpc-attribute \
  --vpc-id $VPC_ID \
  --enable-dns-hostnames \
  --region $AWS_REGION

# 2. Create Subnets
echo "🌐 Creating subnets..."

# Public Subnet 1
PUBLIC_SUBNET_1=$(aws ec2 create-subnet \
  --vpc-id $VPC_ID \
  --cidr-block 10.0.1.0/24 \
  --availability-zone ${AWS_REGION}a \
  --tag-specifications "ResourceType=subnet,Tags=[{Key=Name,Value=$PROJECT_NAME-public-1}]" \
  --query 'Subnet.SubnetId' \
  --output text \
  --region $AWS_REGION)

# Public Subnet 2
PUBLIC_SUBNET_2=$(aws ec2 create-subnet \
  --vpc-id $VPC_ID \
  --cidr-block 10.0.2.0/24 \
  --availability-zone ${AWS_REGION}b \
  --tag-specifications "ResourceType=subnet,Tags=[{Key=Name,Value=$PROJECT_NAME-public-2}]" \
  --query 'Subnet.SubnetId' \
  --output text \
  --region $AWS_REGION)

# Private Subnet 1
PRIVATE_SUBNET_1=$(aws ec2 create-subnet \
  --vpc-id $VPC_ID \
  --cidr-block 10.0.10.0/24 \
  --availability-zone ${AWS_REGION}a \
  --tag-specifications "ResourceType=subnet,Tags=[{Key=Name,Value=$PROJECT_NAME-private-1}]" \
  --query 'Subnet.SubnetId' \
  --output text \
  --region $AWS_REGION)

# Private Subnet 2
PRIVATE_SUBNET_2=$(aws ec2 create-subnet \
  --vpc-id $VPC_ID \
  --cidr-block 10.0.11.0/24 \
  --availability-zone ${AWS_REGION}b \
  --tag-specifications "ResourceType=subnet,Tags=[{Key=Name,Value=$PROJECT_NAME-private-2}]" \
  --query 'Subnet.SubnetId' \
  --output text \
  --region $AWS_REGION)

echo "✅ Subnets created"

# 3. Create Internet Gateway
echo "🌍 Creating Internet Gateway..."
IGW_ID=$(aws ec2 create-internet-gateway \
  --tag-specifications "ResourceType=internet-gateway,Tags=[{Key=Name,Value=$PROJECT_NAME-igw}]" \
  --query 'InternetGateway.InternetGatewayId' \
  --output text \
  --region $AWS_REGION)

aws ec2 attach-internet-gateway \
  --vpc-id $VPC_ID \
  --internet-gateway-id $IGW_ID \
  --region $AWS_REGION

echo "✅ Internet Gateway created: $IGW_ID"

# 4. Create RDS PostgreSQL
echo "🗄️  Creating RDS PostgreSQL instance..."

# Create DB Subnet Group
aws rds create-db-subnet-group \
  --db-subnet-group-name $PROJECT_NAME-db-subnet \
  --db-subnet-group-description "Portfolio Dashboard DB Subnet Group" \
  --subnet-ids $PRIVATE_SUBNET_1 $PRIVATE_SUBNET_2 \
  --region $AWS_REGION

# Create Security Group for RDS
RDS_SG=$(aws ec2 create-security-group \
  --group-name $PROJECT_NAME-rds-sg \
  --description "Security group for Portfolio Dashboard RDS" \
  --vpc-id $VPC_ID \
  --query 'GroupId' \
  --output text \
  --region $AWS_REGION)

# Allow PostgreSQL access from private subnets
aws ec2 authorize-security-group-ingress \
  --group-id $RDS_SG \
  --protocol tcp \
  --port 5432 \
  --cidr 10.0.0.0/16 \
  --region $AWS_REGION

# Create RDS instance
aws rds create-db-instance \
  --db-instance-identifier $PROJECT_NAME-db \
  --db-instance-class db.t3.medium \
  --engine postgres \
  --engine-version 14.7 \
  --master-username portfolioadmin \
  --master-user-password "ChangeThisPassword123!" \
  --allocated-storage 100 \
  --storage-type gp3 \
  --vpc-security-group-ids $RDS_SG \
  --db-subnet-group-name $PROJECT_NAME-db-subnet \
  --backup-retention-period 7 \
  --multi-az \
  --publicly-accessible false \
  --region $AWS_REGION

echo "✅ RDS instance creation initiated (will take 5-10 minutes)"

# 5. Create S3 Bucket for file storage
echo "📦 Creating S3 bucket..."

S3_BUCKET="${PROJECT_NAME}-files-${AWS_ACCOUNT_ID}"
aws s3 mb s3://$S3_BUCKET --region $AWS_REGION

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket $S3_BUCKET \
  --versioning-configuration Status=Enabled \
  --region $AWS_REGION

# Enable encryption
aws s3api put-bucket-encryption \
  --bucket $S3_BUCKET \
  --server-side-encryption-configuration '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}' \
  --region $AWS_REGION

echo "✅ S3 bucket created: $S3_BUCKET"

# 6. Create ECR Repositories
echo "🐳 Creating ECR repositories..."

aws ecr create-repository \
  --repository-name $PROJECT_NAME/backend \
  --region $AWS_REGION

aws ecr create-repository \
  --repository-name $PROJECT_NAME/frontend \
  --region $AWS_REGION

echo "✅ ECR repositories created"

# 7. Create ECS Cluster
echo "☁️  Creating ECS cluster..."

aws ecs create-cluster \
  --cluster-name $PROJECT_NAME-cluster \
  --region $AWS_REGION

echo "✅ ECS cluster created"

echo ""
echo "🎉 AWS infrastructure setup complete!"
echo ""
echo "Next steps:"
echo "1. Wait for RDS instance to be available (~10 minutes)"
echo "2. Build and push Docker images to ECR"
echo "3. Create ECS task definitions and services"
echo "4. Configure ALB and target groups"
echo "5. Set up Route 53 DNS"
echo ""
echo "Resources created:"
echo "  VPC ID: $VPC_ID"
echo "  Public Subnets: $PUBLIC_SUBNET_1, $PUBLIC_SUBNET_2"
echo "  Private Subnets: $PRIVATE_SUBNET_1, $PRIVATE_SUBNET_2"
echo "  RDS Security Group: $RDS_SG"
echo "  S3 Bucket: $S3_BUCKET"
```

### 7.3 Deploy Docker Images to ECR

```bash
# Get ECR login command
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Build and tag backend
cd backend
docker build -t portfolio-dashboard/backend .
docker tag portfolio-dashboard/backend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/portfolio-dashboard/backend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/portfolio-dashboard/backend:latest

# Build and tag frontend
cd ../frontend
docker build -t portfolio-dashboard/frontend .
docker tag portfolio-dashboard/frontend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/portfolio-dashboard/frontend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/portfolio-dashboard/frontend:latest
```

---

## 8. Development with Claude Code/Cursor

### 8.1 Clone Project

```bash
# Clone repository
git clone <your-repo-url> portfolio-dashboard
cd portfolio-dashboard
```

### 8.2 Open in Claude Code

**Using Claude Code CLI:**
```bash
# Install Claude Code
npm install -g @anthropic-ai/claude-code

# Initialize in project
claude-code init

# Start Claude Code session
claude-code start
```

**Tell Claude Code:**
```
I'm working on a Portfolio Dashboard platform. The project structure is:
- backend/ - Python FastAPI backend
- frontend/ - React TypeScript frontend
- database/ - PostgreSQL schema and migrations

Current task: [describe what you want to build]

Reference these project files:
- Portfolio_Dashboard_Implementation_Plan.md
- Portfolio_Dashboard_Database_Schema.md
- DCF_Model_Comprehensive.xlsx (and other Excel models)
```

### 8.3 Open in Cursor

1. Download Cursor: https://cursor.sh/
2. Open project folder in Cursor
3. Enable Claude integration in settings
4. Use `Cmd/Ctrl + K` to chat with Claude

**Example prompts:**
```
"Create a FastAPI router for portfolio companies with CRUD operations based on the schema in database/init/01_schema.sql"

"Build a React component for displaying company financials with a chart using Recharts"

"Write a PDF extraction service that uses pdfplumber to extract financial tables and validates against the database schema"
```

### 8.4 VS Code Dev Containers (Alternative)

**File: `.devcontainer/devcontainer.json`**

```json
{
  "name": "Portfolio Dashboard Dev",
  "dockerComposeFile": "../docker-compose.yml",
  "service": "backend",
  "workspaceFolder": "/app",
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "ms-azuretools.vscode-docker"
      ],
      "settings": {
        "python.defaultInterpreterPath": "/usr/local/bin/python",
        "python.linting.enabled": true,
        "python.linting.pylintEnabled": true,
        "python.formatting.provider": "black",
        "editor.formatOnSave": true
      }
    }
  },
  "postCreateCommand": "pip install -r requirements.txt"
}
```

---

## 9. Testing & Validation

### 9.1 Backend Tests

```bash
cd backend

# Install test dependencies
pip install pytest pytest-asyncio pytest-cov httpx

# Run tests
pytest

# With coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_companies.py -v
```

**Sample test file: `backend/tests/test_companies.py`**

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

# Test database
SQLALCHEMY_DATABASE_URL = "postgresql://portfolio_user:password@localhost:5432/portfolio_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_create_fund():
    response = client.post(
        "/api/v1/funds",
        json={
            "fund_name": "Test Fund I",
            "vintage_year": 2024,
            "fund_size": 100000000,
            "committed_capital": 80000000,
            "fund_strategy": "Buyout"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["fund_name"] == "Test Fund I"
    assert "fund_id" in data

# More tests...
```

### 9.2 Frontend Tests

```bash
cd frontend

# Install test dependencies
npm install --save-dev @testing-library/react @testing-library/jest-dom

# Run tests
npm test

# With coverage
npm test -- --coverage
```

### 9.3 Integration Tests

**Test database connection:**
```bash
psql -U portfolio_user -d portfolio_dashboard -c "SELECT COUNT(*) FROM funds"
```

**Test API endpoints:**
```bash
# Health check
curl http://localhost:8000/health

# Create fund
curl -X POST http://localhost:8000/api/v1/funds \
  -H "Content-Type: application/json" \
  -d '{
    "fund_name": "Test Fund I",
    "vintage_year": 2024,
    "fund_size": 100000000,
    "committed_capital": 80000000
  }'

# Get funds
curl http://localhost:8000/api/v1/funds
```

**Test Excel model generation:**
```python
# backend/tests/test_model_generation.py
from app.services.model_generator import DCFModelGenerator

def test_dcf_model_generation():
    generator = DCFModelGenerator()
    
    # Test data
    company_data = {
        "company_name": "Test Company",
        "revenue": 10000000,
        "ebitda": 2000000,
        # ... more inputs
    }
    
    # Generate model
    excel_path = generator.generate(company_data)
    
    # Verify file exists
    assert os.path.exists(excel_path)
    
    # Load and verify formulas
    from openpyxl import load_workbook
    wb = load_workbook(excel_path)
    ws = wb['DCF Model']
    
    # Check that formulas are preserved (not just values)
    assert ws['E10'].value.startswith('=')  # Should be a formula
    
    print(f"✅ DCF model generated successfully: {excel_path}")
```

---

## 10. Troubleshooting

### Common Issues

#### Database Connection Errors

**Problem:** `psycopg2.OperationalError: could not connect to server`

**Solution:**
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql  # Linux
brew services list  # macOS

# Check connection manually
psql -U portfolio_user -d portfolio_dashboard -h localhost

# Verify .env DATABASE_URL is correct
cat backend/.env | grep DATABASE_URL
```

#### Port Already in Use

**Problem:** `Error: Address already in use (port 8000)`

**Solution:**
```bash
# Find process using port
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill the process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

#### Docker Build Fails

**Problem:** Docker build error with dependencies

**Solution:**
```bash
# Clear Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache

# Check Docker daemon is running
docker info
```

#### OpenAI API Errors

**Problem:** `openai.error.AuthenticationError: Incorrect API key`

**Solution:**
```bash
# Verify API key is set
echo $OPENAI_API_KEY

# Test API key directly
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# Update .env file
nano backend/.env
# OPENAI_API_KEY=sk-your-actual-key-here
```

#### Frontend Can't Connect to Backend

**Problem:** CORS error or connection refused

**Solution:**
```bash
# Check backend is running
curl http://localhost:8000/health

# Verify CORS_ORIGINS in backend/.env
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Check frontend API URL
cat frontend/.env
# REACT_APP_API_URL=http://localhost:8000/api/v1
```

#### Excel Model Formulas Lost

**Problem:** Generated Excel files have values instead of formulas

**Solution:**
```python
# Use openpyxl with data_only=False
from openpyxl import load_workbook

# WRONG:
wb = load_workbook('template.xlsx', data_only=True)  # ❌ Evaluates formulas

# CORRECT:
wb = load_workbook('template.xlsx', data_only=False)  # ✅ Preserves formulas
```

---

## 📚 Additional Resources

### Project Documentation
- **Implementation Plan**: `/mnt/project/Portfolio_Dashboard_Implementation_Plan.md`
- **Database Schema**: `/mnt/project/Portfolio_Dashboard_Database_Schema.md`
- **Quick Start Guide**: `/mnt/project/Portfolio_Dashboard_Quick_Start.md`
- **Model Guides**: `/mnt/project/*_MODEL_GUIDE.md`

### External Documentation
- **FastAPI**: https://fastapi.tiangolo.com/
- **React**: https://react.dev/
- **PostgreSQL**: https://www.postgresql.org/docs/
- **Docker**: https://docs.docker.com/
- **AWS ECS**: https://docs.aws.amazon.com/ecs/
- **openpyxl**: https://openpyxl.readthedocs.io/

### Support
- GitHub Issues: [Create issue for bugs/features]
- Documentation: Check `/mnt/project/` files
- Claude Code: Use for development assistance

---

## ✅ Deployment Checklist

Before going to production:

### Security
- [ ] Change all default passwords
- [ ] Generate strong SECRET_KEY
- [ ] Enable HTTPS/SSL certificates
- [ ] Configure firewall rules
- [ ] Set up VPN for database access
- [ ] Enable AWS GuardDuty
- [ ] Configure WAF rules

### Performance
- [ ] Set up database indexes
- [ ] Configure Redis caching
- [ ] Enable CloudFront CDN
- [ ] Set up auto-scaling policies
- [ ] Configure RDS performance insights

### Monitoring
- [ ] Set up CloudWatch alarms
- [ ] Configure application logging
- [ ] Enable RDS monitoring
- [ ] Set up error tracking (Sentry)
- [ ] Configure uptime monitoring

### Backup & DR
- [ ] Verify automated RDS backups
- [ ] Test backup restoration
- [ ] Set up S3 versioning
- [ ] Document disaster recovery plan
- [ ] Schedule backup tests

### Documentation
- [ ] Update API documentation
- [ ] Create user guides
- [ ] Document deployment process
- [ ] Write runbooks for common issues
- [ ] Update architecture diagrams

---

## 🎉 Success!

You've successfully set up the Portfolio Dashboard platform! 

**Next steps:**
1. **Customize**: Adapt the code to your firm's specific needs
2. **Integrate**: Connect your existing Excel models  
3. **Test**: Load sample data and generate models
4. **Train**: Onboard your team
5. **Launch**: Start with 1-2 portfolio companies, then scale

**Estimated time savings:** 70-80% reduction in manual data entry and model building time.

**Questions?** Check the project documentation in `/mnt/project/` or use Claude Code for development assistance.

---

*Last Updated: November 2025*
*Version: 1.0.0*
*Author: Claude (Anthropic)*
