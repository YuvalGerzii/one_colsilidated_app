"""
Unit tests for CRUD operations.

Tests database operations directly without HTTP layer.
Covers all models: Fund, Company, FinancialMetric, Valuation, KPI.
"""

import pytest
from datetime import date, datetime
from decimal import Decimal
from sqlalchemy.orm import Session

try:
    from app.models import (
        Fund, Company, FinancialMetric, Valuation, KPI,
        ModelTemplate, GeneratedModel, PDFDocument
    )
    from app.crud import fund, company, financial_metric, valuation, kpi
except ImportError:
    # Mock for standalone testing
    fund = company = financial_metric = valuation = kpi = None
    Fund = Company = FinancialMetric = Valuation = KPI = None


# ============================================================================
# FUND CRUD TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.database
class TestFundCRUD:
    """Test CRUD operations for Fund model."""
    
    def test_create_fund(self, db_session: Session):
        """Test creating a new fund."""
        fund_data = {
            "name": "Test Fund III",
            "vintage_year": 2024,
            "fund_size": Decimal("1000000000.00"),
            "target_irr": 25.0,
            "target_moic": 3.0,
            "status": "Active"
        }
        
        new_fund = Fund(**fund_data)
        db_session.add(new_fund)
        db_session.commit()
        db_session.refresh(new_fund)
        
        assert new_fund.fund_id is not None
        assert new_fund.name == "Test Fund III"
        assert new_fund.fund_size == Decimal("1000000000.00")
        assert new_fund.status == "Active"
    
    def test_read_fund(self, db_session: Session, sample_fund: Fund):
        """Test reading a fund by ID."""
        retrieved_fund = db_session.query(Fund).filter(
            Fund.fund_id == sample_fund.fund_id
        ).first()
        
        assert retrieved_fund is not None
        assert retrieved_fund.fund_id == sample_fund.fund_id
        assert retrieved_fund.name == sample_fund.name
    
    def test_update_fund(self, db_session: Session, sample_fund: Fund):
        """Test updating fund attributes."""
        sample_fund.status = "Closed"
        sample_fund.fund_size = Decimal("600000000.00")
        db_session.commit()
        db_session.refresh(sample_fund)
        
        assert sample_fund.status == "Closed"
        assert sample_fund.fund_size == Decimal("600000000.00")
    
    def test_delete_fund(self, db_session: Session, sample_fund: Fund):
        """Test deleting a fund."""
        fund_id = sample_fund.fund_id
        db_session.delete(sample_fund)
        db_session.commit()
        
        deleted_fund = db_session.query(Fund).filter(
            Fund.fund_id == fund_id
        ).first()
        
        assert deleted_fund is None
    
    def test_list_funds(self, db_session: Session, sample_fund: Fund):
        """Test listing all funds."""
        funds = db_session.query(Fund).all()
        
        assert len(funds) >= 1
        assert sample_fund in funds


# ============================================================================
# COMPANY CRUD TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.database
class TestCompanyCRUD:
    """Test CRUD operations for Company model."""
    
    def test_create_company(self, db_session: Session, sample_fund: Fund):
        """Test creating a new company."""
        company_data = {
            "fund_id": sample_fund.fund_id,
            "company_name": "Test Company",
            "sector": "Healthcare",
            "investment_date": date(2024, 1, 1),
            "initial_investment": Decimal("50000000.00"),
            "current_ownership_pct": 75.0,
            "status": "Active"
        }
        
        new_company = Company(**company_data)
        db_session.add(new_company)
        db_session.commit()
        db_session.refresh(new_company)
        
        assert new_company.company_id is not None
        assert new_company.company_name == "Test Company"
        assert new_company.fund_id == sample_fund.fund_id
    
    def test_read_company(self, db_session: Session, sample_company: Company):
        """Test reading a company by ID."""
        retrieved_company = db_session.query(Company).filter(
            Company.company_id == sample_company.company_id
        ).first()
        
        assert retrieved_company is not None
        assert retrieved_company.company_id == sample_company.company_id
        assert retrieved_company.company_name == sample_company.company_name
    
    def test_update_company(self, db_session: Session, sample_company: Company):
        """Test updating company attributes."""
        sample_company.status = "Under LOI"
        sample_company.current_ownership_pct = 70.0
        db_session.commit()
        db_session.refresh(sample_company)
        
        assert sample_company.status == "Under LOI"
        assert sample_company.current_ownership_pct == 70.0
    
    def test_delete_company(self, db_session: Session, sample_company: Company):
        """Test soft deleting a company."""
        company_id = sample_company.company_id
        sample_company.status = "Exited"
        db_session.commit()
        
        company = db_session.query(Company).filter(
            Company.company_id == company_id
        ).first()
        
        assert company.status == "Exited"
    
    def test_filter_by_fund(self, db_session: Session, sample_company: Company, sample_fund: Fund):
        """Test filtering companies by fund."""
        companies = db_session.query(Company).filter(
            Company.fund_id == sample_fund.fund_id
        ).all()
        
        assert len(companies) >= 1
        assert sample_company in companies
    
    def test_filter_by_sector(self, db_session: Session, sample_company: Company):
        """Test filtering companies by sector."""
        companies = db_session.query(Company).filter(
            Company.sector == "Technology"
        ).all()
        
        assert len(companies) >= 1
        assert all(c.sector == "Technology" for c in companies)
    
    def test_filter_by_status(self, db_session: Session, sample_company: Company):
        """Test filtering companies by status."""
        companies = db_session.query(Company).filter(
            Company.status == "Active"
        ).all()
        
        assert len(companies) >= 1
        assert all(c.status == "Active" for c in companies)


# ============================================================================
# FINANCIAL METRIC CRUD TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.database
class TestFinancialMetricCRUD:
    """Test CRUD operations for FinancialMetric model."""
    
    def test_create_financial_metric(self, db_session: Session, sample_company: Company):
        """Test creating a financial metric."""
        metric_data = {
            "company_id": sample_company.company_id,
            "period_end_date": date(2024, 12, 31),
            "period_type": "Annual",
            "period_name": "FY 2024",
            "revenue": Decimal("100000000.00"),
            "ebitda": Decimal("20000000.00"),
            "net_income": Decimal("15000000.00")
        }
        
        new_metric = FinancialMetric(**metric_data)
        db_session.add(new_metric)
        db_session.commit()
        db_session.refresh(new_metric)
        
        assert new_metric.metric_id is not None
        assert new_metric.company_id == sample_company.company_id
        assert new_metric.revenue == Decimal("100000000.00")
    
    def test_read_financial_metrics(
        self, 
        db_session: Session, 
        sample_company: Company,
        sample_financials: list
    ):
        """Test reading financial metrics for a company."""
        metrics = db_session.query(FinancialMetric).filter(
            FinancialMetric.company_id == sample_company.company_id
        ).all()
        
        assert len(metrics) >= 4
        assert all(m.company_id == sample_company.company_id for m in metrics)
    
    def test_filter_by_period_type(
        self, 
        db_session: Session,
        sample_company: Company,
        sample_financials: list
    ):
        """Test filtering metrics by period type."""
        metrics = db_session.query(FinancialMetric).filter(
            FinancialMetric.company_id == sample_company.company_id,
            FinancialMetric.period_type == "Quarterly"
        ).all()
        
        assert len(metrics) >= 4
        assert all(m.period_type == "Quarterly" for m in metrics)
    
    def test_order_by_date(
        self, 
        db_session: Session,
        sample_company: Company,
        sample_financials: list
    ):
        """Test ordering metrics by date."""
        metrics = db_session.query(FinancialMetric).filter(
            FinancialMetric.company_id == sample_company.company_id
        ).order_by(FinancialMetric.period_end_date.desc()).all()
        
        assert len(metrics) >= 4
        # Verify descending order
        for i in range(len(metrics) - 1):
            assert metrics[i].period_end_date >= metrics[i + 1].period_end_date
    
    def test_calculate_growth_rate(
        self, 
        db_session: Session,
        sample_financials: list
    ):
        """Test calculating revenue growth rate."""
        metrics = sorted(sample_financials, key=lambda x: x.period_end_date)
        
        if len(metrics) >= 2:
            q1_revenue = float(metrics[0].revenue)
            q2_revenue = float(metrics[1].revenue)
            growth_rate = ((q2_revenue - q1_revenue) / q1_revenue) * 100
            
            assert growth_rate > 0  # Revenue should be growing
            assert growth_rate < 50  # Reasonable quarterly growth


# ============================================================================
# VALUATION CRUD TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.database
class TestValuationCRUD:
    """Test CRUD operations for Valuation model."""
    
    def test_create_valuation(self, db_session: Session, sample_company: Company):
        """Test creating a valuation."""
        valuation_data = {
            "company_id": sample_company.company_id,
            "valuation_date": date(2024, 12, 31),
            "valuation_type": "Comparable Companies",
            "enterprise_value": Decimal("200000000.00"),
            "equity_value": Decimal("180000000.00"),
            "ebitda_multiple": Decimal("15.0"),
            "status": "Draft"
        }
        
        new_valuation = Valuation(**valuation_data)
        db_session.add(new_valuation)
        db_session.commit()
        db_session.refresh(new_valuation)
        
        assert new_valuation.valuation_id is not None
        assert new_valuation.valuation_type == "Comparable Companies"
        assert new_valuation.enterprise_value == Decimal("200000000.00")
    
    def test_read_latest_valuation(
        self, 
        db_session: Session,
        sample_company: Company,
        sample_valuation: Valuation
    ):
        """Test reading the latest valuation."""
        latest = db_session.query(Valuation).filter(
            Valuation.company_id == sample_company.company_id
        ).order_by(Valuation.valuation_date.desc()).first()
        
        assert latest is not None
        assert latest.valuation_id == sample_valuation.valuation_id
    
    def test_update_valuation_status(
        self, 
        db_session: Session,
        sample_valuation: Valuation
    ):
        """Test updating valuation status."""
        sample_valuation.status = "Approved"
        db_session.commit()
        db_session.refresh(sample_valuation)
        
        assert sample_valuation.status == "Approved"
    
    def test_filter_by_valuation_type(
        self, 
        db_session: Session,
        sample_company: Company,
        sample_valuation: Valuation
    ):
        """Test filtering valuations by type."""
        valuations = db_session.query(Valuation).filter(
            Valuation.company_id == sample_company.company_id,
            Valuation.valuation_type == "DCF"
        ).all()
        
        assert len(valuations) >= 1
        assert all(v.valuation_type == "DCF" for v in valuations)


# ============================================================================
# KPI CRUD TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.database
class TestKPICRUD:
    """Test CRUD operations for KPI model."""
    
    def test_create_kpi(self, db_session: Session, sample_company: Company):
        """Test creating a KPI."""
        kpi_data = {
            "company_id": sample_company.company_id,
            "period_end_date": date(2024, 12, 31),
            "period_type": "Quarterly",
            "period_name": "Q4 2024",
            "kpi_category": "Sales",
            "kpi_name": "Monthly Recurring Revenue",
            "kpi_value": Decimal("5000000.00"),
            "target_value": Decimal("6000000.00"),
            "unit": "USD"
        }
        
        new_kpi = KPI(**kpi_data)
        db_session.add(new_kpi)
        db_session.commit()
        db_session.refresh(new_kpi)
        
        assert new_kpi.kpi_id is not None
        assert new_kpi.kpi_name == "Monthly Recurring Revenue"
        assert new_kpi.kpi_value == Decimal("5000000.00")
    
    def test_read_kpis(
        self, 
        db_session: Session,
        sample_company: Company,
        sample_kpis: list
    ):
        """Test reading KPIs for a company."""
        kpis = db_session.query(KPI).filter(
            KPI.company_id == sample_company.company_id
        ).all()
        
        assert len(kpis) >= 4
        assert all(k.company_id == sample_company.company_id for k in kpis)
    
    def test_filter_kpis_by_quarter(
        self, 
        db_session: Session,
        sample_company: Company,
        sample_kpis: list
    ):
        """Test filtering KPIs by quarter."""
        kpis = db_session.query(KPI).filter(
            KPI.company_id == sample_company.company_id,
            KPI.period_name.like("%Q4%")
        ).all()
        
        assert len(kpis) >= 1
        assert all("Q4" in k.period_name for k in kpis)
    
    def test_filter_kpis_by_category(
        self, 
        db_session: Session,
        sample_company: Company,
        sample_kpis: list
    ):
        """Test filtering KPIs by category."""
        kpis = db_session.query(KPI).filter(
            KPI.company_id == sample_company.company_id,
            KPI.kpi_category == "Customer"
        ).all()
        
        assert len(kpis) >= 1
        assert all(k.kpi_category == "Customer" for k in kpis)


# ============================================================================
# RELATIONSHIP TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.database
class TestRelationships:
    """Test model relationships."""
    
    def test_fund_to_companies(
        self, 
        db_session: Session,
        sample_fund: Fund,
        sample_company: Company
    ):
        """Test Fund -> Companies relationship."""
        fund_with_companies = db_session.query(Fund).filter(
            Fund.fund_id == sample_fund.fund_id
        ).first()
        
        # Access companies through relationship
        companies = fund_with_companies.companies
        assert len(companies) >= 1
        assert sample_company in companies
    
    def test_company_to_financials(
        self, 
        db_session: Session,
        sample_company: Company,
        sample_financials: list
    ):
        """Test Company -> FinancialMetrics relationship."""
        company_with_financials = db_session.query(Company).filter(
            Company.company_id == sample_company.company_id
        ).first()
        
        # Access financials through relationship
        financials = company_with_financials.financial_metrics
        assert len(financials) >= 4
    
    def test_company_to_valuations(
        self, 
        db_session: Session,
        sample_company: Company,
        sample_valuation: Valuation
    ):
        """Test Company -> Valuations relationship."""
        company_with_valuations = db_session.query(Company).filter(
            Company.company_id == sample_company.company_id
        ).first()
        
        # Access valuations through relationship
        valuations = company_with_valuations.valuations
        assert len(valuations) >= 1
        assert sample_valuation in valuations
    
    def test_company_to_kpis(
        self, 
        db_session: Session,
        sample_company: Company,
        sample_kpis: list
    ):
        """Test Company -> KPIs relationship."""
        company_with_kpis = db_session.query(Company).filter(
            Company.company_id == sample_company.company_id
        ).first()
        
        # Access KPIs through relationship
        kpis = company_with_kpis.kpis
        assert len(kpis) >= 4


# ============================================================================
# PERFORMANCE TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.performance
class TestPerformance:
    """Test query performance."""
    
    def test_bulk_insert(self, db_session: Session, sample_fund: Fund):
        """Test bulk inserting companies."""
        companies = [
            Company(
                fund_id=sample_fund.fund_id,
                company_name=f"Company {i}",
                sector="Technology",
                investment_date=date(2024, 1, 1),
                initial_investment=Decimal("10000000.00"),
                status="Active"
            )
            for i in range(50)
        ]
        
        db_session.bulk_save_objects(companies)
        db_session.commit()
        
        count = db_session.query(Company).filter(
            Company.fund_id == sample_fund.fund_id
        ).count()
        
        assert count >= 50
    
    def test_paginated_query(self, db_session: Session, multiple_companies: list):
        """Test pagination performance."""
        page_size = 2
        page_1 = db_session.query(Company).limit(page_size).offset(0).all()
        page_2 = db_session.query(Company).limit(page_size).offset(page_size).all()
        
        assert len(page_1) == page_size
        assert len(page_2) == page_size
        assert page_1[0].company_id != page_2[0].company_id
    
    @pytest.mark.slow
    def test_complex_join_query(
        self, 
        db_session: Session,
        complete_company_data: dict
    ):
        """Test complex JOIN query performance."""
        results = db_session.query(
            Company.company_name,
            FinancialMetric.revenue,
            Valuation.enterprise_value
        ).join(
            FinancialMetric, Company.company_id == FinancialMetric.company_id
        ).join(
            Valuation, Company.company_id == Valuation.company_id
        ).filter(
            Company.status == "Active"
        ).all()
        
        assert len(results) >= 1
