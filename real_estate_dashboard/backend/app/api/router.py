"""
API Router - Main API route aggregation
"""

from fastapi import APIRouter

from app.api.v1.endpoints import (
    health,
    property_management,
    real_estate_tools,
    companies,
    users,  # ✅ NEW - User management
    deals,  # ✅ NEW - Multi-type deal management
    accounting,
    tax_calculators,
    advanced_tax_strategies,
    elite_tax_strategies,
    crm,
    market_intelligence,
    enhanced_market_intelligence,
    yfinance_economics,  # ✅ NEW - YFinance & Economics API integration
    integrations,
    official_data,
    # ml_analytics,  # TEMPORARILY DISABLED: Requires sentence-transformers
    auth,
    saved_calculations,
    fund_management,
    financial_models,
    debt_management,
    reports,
    project_tracking,
    # legal_services,  # DISABLED: UUID vs integer type mismatch - file removed
    enhanced_legal,  # ✅ Active - uses UUID foreign keys
    pdf_extraction,
    compliance_audit,
    internal_legal_services,
    model_templates,
    portfolio_analytics,
    interactive_dashboards,
    llm,  # ✅ NEW - Local LLM integration
    markitdown,  # ✅ NEW - MarkItDown document conversion
    sensitivity_analysis,  # ✅ NEW - Sensitivity analysis for financial models
    deal_analysis,  # ✅ NEW - Deal analysis framework
    predictive_analytics,  # ✅ NEW - ML-powered predictive analytics
    ai_chatbot,  # ✅ NEW - AI chatbot with multi-agent system
    zillow_data,  # ✅ NEW - Zillow property data scraping with background tasks
)

api_router = APIRouter()

# Health check endpoint
api_router.include_router(
    health.router,
    tags=["health"]
)

# Authentication endpoints
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["authentication"]
)

# Saved Calculations endpoints (replaces localStorage)
api_router.include_router(
    saved_calculations.router,
    prefix="/calculations",
    tags=["calculations"]
)

# Third-Party Integrations endpoints
api_router.include_router(
    integrations.router,
    prefix="/integrations",
    tags=["integrations"]
)

# Official Government Data endpoints
api_router.include_router(
    official_data.router,
    prefix="/integrations/official-data",
    tags=["official-data"]
)

# Company Management endpoints
api_router.include_router(
    companies.router,
    prefix="/companies",
    tags=["companies"]
)

# User Management endpoints
api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users", "user-management"]
)

# Deal Management endpoints (Multi-type: real estate, acquisitions, shares, commodities)
api_router.include_router(
    deals.router,
    prefix="/deals",
    tags=["deals", "transactions", "pipeline"]
)

# Accounting endpoints
api_router.include_router(
    accounting.router,
    prefix="/accounting",
    tags=["accounting", "financial", "tax-benefits"]
)

# Tax Calculator endpoints
api_router.include_router(
    tax_calculators.router,
    prefix="/tax-calculators",
    tags=["tax-calculators", "planning-tools"]
)

# Advanced Tax Strategy endpoints
api_router.include_router(
    advanced_tax_strategies.router,
    prefix="/advanced-tax",
    tags=["advanced-tax-strategies", "tax-shelters", "international-tax"]
)

# Elite Tax Loopholes & Strategies endpoints
api_router.include_router(
    elite_tax_strategies.router,
    prefix="/elite-tax",
    tags=["elite-tax-loopholes", "qsbs", "augusta-rule", "reps", "estate-planning"]
)

# Property Management endpoints
api_router.include_router(
    property_management.router,
    prefix="/property-management",
    tags=["property-management"]
)

# Real Estate Tools endpoints
api_router.include_router(
    real_estate_tools.router,
    prefix="/real-estate",
    tags=["real-estate-tools"]
)

# Sensitivity Analysis endpoints (FREE - No API keys required)
api_router.include_router(
    sensitivity_analysis.router,
    prefix="/sensitivity-analysis",
    tags=["sensitivity-analysis", "financial-modeling", "risk-analysis"]
)

# Deal Analysis endpoints (FREE - No API keys required)
api_router.include_router(
    deal_analysis.router,
    prefix="/deal-analysis",
    tags=["deal-analysis", "investment-analysis", "deal-scoring"]
)

# CRM endpoints
api_router.include_router(
    crm.router,
    prefix="/crm",
    tags=["crm"]
)

# Market Intelligence endpoints (with failsafe fallbacks)
api_router.include_router(
    market_intelligence.router,
    prefix="/market-intelligence",
    tags=["market-intelligence"]
)

# Enhanced Market Intelligence endpoints (Custom markets, competitive analysis)
api_router.include_router(
    enhanced_market_intelligence.router,
    prefix="/market-intelligence/enhanced",
    tags=["market-intelligence-enhanced", "custom-markets", "competitive-analysis"]
)

# YFinance & Economics API endpoints (Stock data, REITs, Market Indices, Economic Indicators)
api_router.include_router(
    yfinance_economics.router,
    prefix="/market-intelligence",
    tags=["yfinance", "economics-api", "stock-data", "reits", "economic-indicators"]
)

# ML & AI Analytics endpoints (TEMPORARILY DISABLED)
# api_router.include_router(
#     ml_analytics.router,
#     prefix="/ml-analytics",
#     tags=["ml-analytics", "ai", "predictive-analytics"]
# )

# Fund Management endpoints (PE/VC funds)
api_router.include_router(
    fund_management.router,
    prefix="/fund-management",
    tags=["fund-management"]
)

# Financial Models endpoints (DCF, LBO)
api_router.include_router(
    financial_models.router,
    prefix="/financial-models",
    tags=["financial-models"]
)

# Debt Management endpoints (Loan tracking, DSCR, refinancing analysis)
api_router.include_router(
    debt_management.router,
    prefix="/debt-management",
    tags=["debt-management"]
)

# Report Generation endpoints (Investment memos, quarterly reports, etc.)
api_router.include_router(
    reports.router,
    prefix="/reports",
    tags=["reports", "documents"]
)

# Project Tracking endpoints (Task management, project tracking)
api_router.include_router(
    project_tracking.router,
    prefix="/project-tracking",
    tags=["project-tracking", "tasks", "projects"]
)

# Legal Services endpoints (Legal docs, compliance, risk assessment)
# DISABLED: UUID vs integer type mismatch issues
# api_router.include_router(
#     legal_services.router,
#     prefix="/legal-services",
#     tags=["legal-services", "compliance", "legal"]
# )

# Enhanced Legal Services endpoints (AI, automation, clause library)
# Note: Uses models with UUID foreign keys
api_router.include_router(
    enhanced_legal.router,
    prefix="/legal-services/enhanced",
    tags=["legal-services-enhanced", "ai-legal", "automation"]
)

# Compliance and Audit endpoints (Regulatory, KYC/AML, Audit prep)
api_router.include_router(
    compliance_audit.router,
    prefix="/compliance-audit",
    tags=["compliance", "audit", "regulatory"]
)

# PDF Extraction endpoints (Financial document extraction and analysis)
api_router.include_router(
    pdf_extraction.router,
    prefix="/pdf-extraction",
    tags=["pdf-extraction", "documents", "ai"]
)

# Internal Legal Services endpoints (No external APIs - fully self-contained)
api_router.include_router(
    internal_legal_services.router,
    prefix="/internal-legal",
    tags=["internal-legal", "templates", "clause-analysis", "risk-scoring", "checklists", "deadlines"]
)

# Model Templates & Presets endpoints (Smart templates, cloning, comparison)
api_router.include_router(
    model_templates.router,
    prefix="/templates",
    tags=["templates", "presets", "model-management"]
)

# Portfolio Analytics endpoints (Performance tracking, IRR, risk metrics, cash flow projections)
api_router.include_router(
    portfolio_analytics.router,
    prefix="/portfolio-analytics",
    tags=["portfolio-analytics", "performance", "risk-metrics"]
)

# Interactive Dashboards endpoints (Dashboard builder, custom KPIs, benchmarks, performance attribution)
api_router.include_router(
    interactive_dashboards.router,
    prefix="/dashboards",
    tags=["dashboards", "widgets", "kpis", "benchmarks"]
)

# LLM endpoints (Local language model features - text generation, summarization, property descriptions)
api_router.include_router(
    llm.router,
    prefix="/llm",
    tags=["llm", "ai", "text-generation"]
)

# MarkItDown endpoints (Document-to-markdown conversion for multi-format documents)
api_router.include_router(
    markitdown.router,
    prefix="/markitdown",
    tags=["markitdown", "document-conversion", "markdown", "ai"]
)

# Predictive Analytics endpoints (ML models for price prediction, rent forecasting, risk/opportunity scoring)
api_router.include_router(
    predictive_analytics.router,
    tags=["predictive-analytics", "machine-learning", "forecasting", "ai"]
)

# AI Chatbot endpoints (Multi-agent system for real estate assistance with REST and WebSocket support)
api_router.include_router(
    ai_chatbot.router,
    prefix="/ai-chatbot",
    tags=["ai-chatbot", "multi-agent", "assistant", "conversational-ai"]
)

# Zillow Property Data endpoints (Web scraping with background tasks - no API key required)
api_router.include_router(
    zillow_data.router,
    prefix="/zillow",
    tags=["zillow", "property-data", "scraping", "real-estate"]
)
