"""
Pytest configuration and fixtures for Portfolio Dashboard tests.

This module provides:
- Database fixtures with in-memory SQLite
- FastAPI test client with dependency overrides
- Sample data factories for testing
- Reusable test data fixtures
"""

import pytest
from datetime import datetime, date
from decimal import Decimal
from typing import Generator, Dict, Any
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

# Import your app modules (adjust paths as needed)
try:
    from app.database import Base, get_db
    from app.main import app
    from app.models import (
        Fund, Company, FinancialMetric, Valuation,
        KPI, ModelTemplate, GeneratedModel, PDFDocument,
        ValueCreationInitiative, CompanyContact
    )
except ImportError:
    # Mock imports for standalone testing
    class Base:
        metadata = type('obj', (object,), {'create_all': lambda *args: None})()
    
    def get_db():
        yield None
    
    app = None
    Fund = Company = FinancialMetric = Valuation = None
    KPI = ModelTemplate = GeneratedModel = PDFDocument = None
    ValueCreationInitiative = CompanyContact = None


# ============================================================================
# DATABASE FIXTURES
# ============================================================================

@pytest.fixture(scope="function")
def db_engine():
    """
    Create an in-memory SQLite database engine for testing.
    
    Uses StaticPool to ensure the same connection is reused,
    preventing the in-memory database from being destroyed.
    """
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(db_engine) -> Generator[Session, None, None]:
    """
    Provide a SQLAlchemy session for each test function.
    
    Automatically rolls back changes after each test to ensure isolation.
    """
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = SessionLocal()
    
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture(scope="function")
def client(db_session: Session) -> TestClient:
    """
    Provide a FastAPI TestClient with database dependency override.
    
    Overrides the get_db dependency to use the test database session.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


# ============================================================================
# SAMPLE DATA FACTORIES
# ============================================================================

@pytest.fixture
def sample_fund(db_session: Session) -> Fund:
    """Create a sample fund for testing."""
    fund = Fund(
        name="Test Growth Fund I",
        vintage_year=2022,
        fund_size=500000000.00,  # $500M
        target_irr=20.0,
        target_moic=2.5,
        management_fee_pct=2.0,
        carried_interest_pct=20.0,
        investment_period_years=5,
        fund_life_years=10,
        status="Active"
    )
    db_session.add(fund)
    db_session.commit()
    db_session.refresh(fund)
    return fund


@pytest.fixture
def sample_company(db_session: Session, sample_fund: Fund) -> Company:
    """Create a sample company for testing."""
    company = Company(
        fund_id=sample_fund.fund_id,
        company_name="TechCo Solutions Inc.",
        sector="Technology",
        industry="SaaS",
        investment_date=date(2023, 3, 15),
        initial_investment=25000000.00,  # $25M
        current_ownership_pct=65.0,
        investment_stage="Growth",
        headquarters_location="San Francisco, CA",
        website="https://techco.example.com",
        description="Leading B2B SaaS platform for workflow automation",
        status="Active"
    )
    db_session.add(company)
    db_session.commit()
    db_session.refresh(company)
    return company


@pytest.fixture
def sample_financials(db_session: Session, sample_company: Company) -> list[FinancialMetric]:
    """Create 4 quarters of financial metrics for testing."""
    financials = []
    
    quarters = [
        (date(2024, 3, 31), "Q1", 15000000, 3000000, 2000000),
        (date(2024, 6, 30), "Q2", 16500000, 3300000, 2200000),
        (date(2024, 9, 30), "Q3", 18000000, 3600000, 2400000),
        (date(2024, 12, 31), "Q4", 20000000, 4000000, 2600000),
    ]
    
    for period_end, period_name, revenue, ebitda, net_income in quarters:
        metric = FinancialMetric(
            company_id=sample_company.company_id,
            period_end_date=period_end,
            period_type="Quarterly",
            period_name=f"2024 {period_name}",
            revenue=Decimal(revenue),
            cogs=Decimal(revenue * 0.3),
            gross_profit=Decimal(revenue * 0.7),
            operating_expenses=Decimal(revenue * 0.5),
            ebitda=Decimal(ebitda),
            depreciation=Decimal(200000),
            ebit=Decimal(ebitda - 200000),
            interest_expense=Decimal(100000),
            taxes=Decimal((ebitda - 300000) * 0.25),
            net_income=Decimal(net_income),
            total_assets=Decimal(50000000),
            total_liabilities=Decimal(20000000),
            total_equity=Decimal(30000000),
            cash=Decimal(10000000),
            accounts_receivable=Decimal(5000000),
            inventory=Decimal(2000000),
            ppe=Decimal(15000000),
            accounts_payable=Decimal(3000000),
            debt_current=Decimal(2000000),
            debt_longterm=Decimal(10000000)
        )
        db_session.add(metric)
        financials.append(metric)
    
    db_session.commit()
    for f in financials:
        db_session.refresh(f)
    
    return financials


@pytest.fixture
def sample_valuation(db_session: Session, sample_company: Company) -> Valuation:
    """Create a sample valuation for testing."""
    valuation = Valuation(
        company_id=sample_company.company_id,
        valuation_date=date(2024, 12, 31),
        valuation_type="DCF",
        enterprise_value=Decimal(150000000),
        equity_value=Decimal(140000000),
        revenue_multiple=Decimal(7.5),
        ebitda_multiple=Decimal(12.5),
        wacc=Decimal(10.5),
        terminal_growth_rate=Decimal(2.5),
        assumptions={"revenue_growth": [15, 12, 10, 8, 6]},
        status="Final"
    )
    db_session.add(valuation)
    db_session.commit()
    db_session.refresh(valuation)
    return valuation


@pytest.fixture
def sample_kpis(db_session: Session, sample_company: Company) -> list[KPI]:
    """Create 4 quarters of KPIs for testing."""
    kpis = []
    
    quarters = [
        (date(2024, 3, 31), "Q1", 1500, 85, 125000),
        (date(2024, 6, 30), "Q2", 1650, 87, 130000),
        (date(2024, 9, 30), "Q3", 1800, 88, 135000),
        (date(2024, 12, 31), "Q4", 2000, 90, 140000),
    ]
    
    for period_end, period_name, customers, nps, arr in quarters:
        kpi = KPI(
            company_id=sample_company.company_id,
            period_end_date=period_end,
            period_type="Quarterly",
            period_name=f"2024 {period_name}",
            kpi_category="Customer",
            kpi_name="Total Customers",
            kpi_value=Decimal(customers),
            target_value=Decimal(customers * 1.1),
            unit="count",
            kpi_data={
                "customers": customers,
                "nps_score": nps,
                "arr": arr,
                "churn_rate": 5.0
            }
        )
        db_session.add(kpi)
        kpis.append(kpi)
    
    db_session.commit()
    for k in kpis:
        db_session.refresh(k)
    
    return kpis


@pytest.fixture
def complete_company_data(
    db_session: Session,
    sample_company: Company,
    sample_financials: list[FinancialMetric],
    sample_valuation: Valuation,
    sample_kpis: list[KPI]
) -> Dict[str, Any]:
    """Provide a complete company with all related data."""
    return {
        "company": sample_company,
        "financials": sample_financials,
        "valuation": sample_valuation,
        "kpis": sample_kpis
    }


@pytest.fixture
def multiple_companies(db_session: Session, sample_fund: Fund) -> list[Company]:
    """Create 5 companies for batch testing."""
    companies = []
    
    company_data = [
        ("Alpha Tech", "Technology", 20000000),
        ("Beta Health", "Healthcare", 30000000),
        ("Gamma Finance", "Financial Services", 25000000),
        ("Delta Retail", "Consumer", 15000000),
        ("Epsilon Energy", "Energy", 35000000),
    ]
    
    for name, sector, investment in company_data:
        company = Company(
            fund_id=sample_fund.fund_id,
            company_name=name,
            sector=sector,
            investment_date=date(2023, 6, 1),
            initial_investment=Decimal(investment),
            current_ownership_pct=55.0,
            status="Active"
        )
        db_session.add(company)
        companies.append(company)
    
    db_session.commit()
    for c in companies:
        db_session.refresh(c)
    
    return companies


# ============================================================================
# REQUEST PAYLOAD FIXTURES
# ============================================================================

@pytest.fixture
def valid_fund_payload() -> Dict[str, Any]:
    """Provide a valid fund creation payload."""
    return {
        "name": "New Fund II",
        "vintage_year": 2024,
        "fund_size": 750000000.00,
        "target_irr": 22.0,
        "target_moic": 3.0,
        "management_fee_pct": 2.0,
        "carried_interest_pct": 20.0,
        "investment_period_years": 5,
        "fund_life_years": 10,
        "status": "Fundraising"
    }


@pytest.fixture
def valid_company_payload(sample_fund: Fund) -> Dict[str, Any]:
    """Provide a valid company creation payload."""
    return {
        "fund_id": sample_fund.fund_id,
        "company_name": "NewCo Inc.",
        "sector": "Technology",
        "industry": "Cloud Infrastructure",
        "investment_date": "2024-01-15",
        "initial_investment": 30000000.00,
        "current_ownership_pct": 70.0,
        "investment_stage": "Early Growth",
        "headquarters_location": "Austin, TX",
        "website": "https://newco.example.com",
        "description": "Cloud infrastructure provider",
        "status": "Active"
    }


@pytest.fixture
def valid_financial_payload(sample_company: Company) -> Dict[str, Any]:
    """Provide a valid financial metrics payload."""
    return {
        "company_id": sample_company.company_id,
        "period_end_date": "2024-12-31",
        "period_type": "Annual",
        "period_name": "FY 2024",
        "revenue": 75000000.00,
        "cogs": 22500000.00,
        "gross_profit": 52500000.00,
        "operating_expenses": 37500000.00,
        "ebitda": 15000000.00,
        "depreciation": 800000.00,
        "ebit": 14200000.00,
        "interest_expense": 400000.00,
        "taxes": 3450000.00,
        "net_income": 10350000.00,
        "total_assets": 60000000.00,
        "total_liabilities": 25000000.00,
        "total_equity": 35000000.00,
        "cash": 12000000.00
    }


# ============================================================================
# UTILITY FIXTURES
# ============================================================================

@pytest.fixture
def api_headers() -> Dict[str, str]:
    """Provide standard API request headers."""
    return {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }


@pytest.fixture(autouse=True)
def reset_db_state(db_session: Session):
    """Automatically reset database state between tests."""
    yield
    # Cleanup happens automatically via session rollback in db_session fixture
