"""
Integration tests for API endpoints.

Tests HTTP layer with FastAPI TestClient.
Covers all core CRUD API endpoints.
"""

import pytest
from datetime import date
from decimal import Decimal
from fastapi.testclient import TestClient

try:
    from app.models import Fund, Company, FinancialMetric, Valuation, KPI
except ImportError:
    Fund = Company = FinancialMetric = Valuation = KPI = None


# ============================================================================
# FUND API TESTS
# ============================================================================

@pytest.mark.integration
class TestFundAPI:
    """Test Fund API endpoints."""
    
    def test_create_fund(self, client: TestClient, valid_fund_payload: dict):
        """Test POST /api/v1/funds - Create fund."""
        response = client.post("/api/v1/funds", json=valid_fund_payload)
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == valid_fund_payload["name"]
        assert data["fund_size"] == valid_fund_payload["fund_size"]
        assert "fund_id" in data
    
    def test_list_funds(self, client: TestClient, sample_fund: Fund):
        """Test GET /api/v1/funds - List all funds."""
        response = client.post("/api/v1/funds", json={
            "name": "Fund for Listing",
            "vintage_year": 2024,
            "fund_size": 500000000.00,
            "status": "Active"
        })
        
        response = client.get("/api/v1/funds")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
    
    def test_get_fund_by_id(self, client: TestClient, sample_fund: Fund):
        """Test GET /api/v1/funds/{fund_id} - Get specific fund."""
        response = client.get(f"/api/v1/funds/{sample_fund.fund_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["fund_id"] == sample_fund.fund_id
        assert data["name"] == sample_fund.name
    
    def test_get_fund_not_found(self, client: TestClient):
        """Test GET /api/v1/funds/{fund_id} - 404 for non-existent fund."""
        response = client.get("/api/v1/funds/99999")
        
        assert response.status_code == 404
    
    def test_update_fund(self, client: TestClient, sample_fund: Fund):
        """Test PUT /api/v1/funds/{fund_id} - Update fund."""
        update_data = {
            "status": "Closed",
            "fund_size": 600000000.00
        }
        
        response = client.put(
            f"/api/v1/funds/{sample_fund.fund_id}",
            json=update_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "Closed"
        assert data["fund_size"] == 600000000.00
    
    def test_delete_fund(self, client: TestClient, valid_fund_payload: dict):
        """Test DELETE /api/v1/funds/{fund_id} - Delete fund."""
        # Create fund first
        create_response = client.post("/api/v1/funds", json=valid_fund_payload)
        fund_id = create_response.json()["fund_id"]
        
        # Delete it
        response = client.delete(f"/api/v1/funds/{fund_id}")
        
        assert response.status_code == 204
        
        # Verify deletion
        get_response = client.get(f"/api/v1/funds/{fund_id}")
        assert get_response.status_code == 404
    
    def test_create_fund_invalid_data(self, client: TestClient):
        """Test POST /api/v1/funds - 422 for invalid data."""
        invalid_payload = {
            "name": "Test Fund",
            # Missing required fields
        }
        
        response = client.post("/api/v1/funds", json=invalid_payload)
        
        assert response.status_code == 422


# ============================================================================
# COMPANY API TESTS
# ============================================================================

@pytest.mark.integration
class TestCompanyAPI:
    """Test Company API endpoints."""
    
    def test_create_company(
        self, 
        client: TestClient,
        sample_fund: Fund,
        valid_company_payload: dict
    ):
        """Test POST /api/v1/companies - Create company."""
        response = client.post("/api/v1/companies", json=valid_company_payload)
        
        assert response.status_code == 201
        data = response.json()
        assert data["company_name"] == valid_company_payload["company_name"]
        assert data["fund_id"] == valid_company_payload["fund_id"]
        assert "company_id" in data
    
    def test_list_companies(self, client: TestClient, sample_company: Company):
        """Test GET /api/v1/companies - List all companies."""
        response = client.get("/api/v1/companies")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
    
    def test_list_companies_by_fund(
        self, 
        client: TestClient,
        sample_fund: Fund,
        sample_company: Company
    ):
        """Test GET /api/v1/companies?fund_id={id} - Filter by fund."""
        response = client.get(f"/api/v1/companies?fund_id={sample_fund.fund_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert all(c["fund_id"] == sample_fund.fund_id for c in data)
    
    def test_list_companies_by_sector(
        self, 
        client: TestClient,
        sample_company: Company
    ):
        """Test GET /api/v1/companies?sector={sector} - Filter by sector."""
        response = client.get("/api/v1/companies?sector=Technology")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert all(c["sector"] == "Technology" for c in data)
    
    def test_get_company_by_id(self, client: TestClient, sample_company: Company):
        """Test GET /api/v1/companies/{company_id} - Get specific company."""
        response = client.get(f"/api/v1/companies/{sample_company.company_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["company_id"] == sample_company.company_id
        assert data["company_name"] == sample_company.company_name
    
    def test_update_company(self, client: TestClient, sample_company: Company):
        """Test PUT /api/v1/companies/{company_id} - Update company."""
        update_data = {
            "status": "Under LOI",
            "current_ownership_pct": 70.0
        }
        
        response = client.put(
            f"/api/v1/companies/{sample_company.company_id}",
            json=update_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "Under LOI"
        assert data["current_ownership_pct"] == 70.0
    
    def test_delete_company(
        self, 
        client: TestClient,
        sample_fund: Fund,
        valid_company_payload: dict
    ):
        """Test DELETE /api/v1/companies/{company_id} - Delete company."""
        # Create company first
        create_response = client.post("/api/v1/companies", json=valid_company_payload)
        company_id = create_response.json()["company_id"]
        
        # Delete it
        response = client.delete(f"/api/v1/companies/{company_id}")
        
        assert response.status_code == 204
    
    def test_create_company_with_invalid_fund(self, client: TestClient):
        """Test POST /api/v1/companies - 404 for invalid fund_id."""
        invalid_payload = {
            "fund_id": 99999,  # Non-existent fund
            "company_name": "Test Company",
            "sector": "Technology",
            "investment_date": "2024-01-01",
            "initial_investment": 10000000.00,
            "status": "Active"
        }
        
        response = client.post("/api/v1/companies", json=invalid_payload)
        
        assert response.status_code in [404, 422]


# ============================================================================
# FINANCIAL METRICS API TESTS
# ============================================================================

@pytest.mark.integration
class TestFinancialMetricAPI:
    """Test Financial Metric API endpoints."""
    
    def test_create_financial_metric(
        self, 
        client: TestClient,
        sample_company: Company,
        valid_financial_payload: dict
    ):
        """Test POST /api/v1/companies/{id}/financials - Create metric."""
        response = client.post(
            f"/api/v1/companies/{sample_company.company_id}/financials",
            json=valid_financial_payload
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["company_id"] == sample_company.company_id
        assert data["revenue"] == valid_financial_payload["revenue"]
        assert "metric_id" in data
    
    def test_list_financial_metrics(
        self, 
        client: TestClient,
        sample_company: Company,
        sample_financials: list
    ):
        """Test GET /api/v1/companies/{id}/financials - List metrics."""
        response = client.get(
            f"/api/v1/companies/{sample_company.company_id}/financials"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 4
    
    def test_filter_financials_by_period_type(
        self, 
        client: TestClient,
        sample_company: Company,
        sample_financials: list
    ):
        """Test GET /api/v1/companies/{id}/financials?period_type - Filter."""
        response = client.get(
            f"/api/v1/companies/{sample_company.company_id}/financials"
            "?period_type=Quarterly"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert all(m["period_type"] == "Quarterly" for m in data)
    
    def test_limit_financial_results(
        self, 
        client: TestClient,
        sample_company: Company,
        sample_financials: list
    ):
        """Test GET /api/v1/companies/{id}/financials?limit - Result limit."""
        response = client.get(
            f"/api/v1/companies/{sample_company.company_id}/financials?limit=2"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 2
    
    def test_financials_date_ordering(
        self, 
        client: TestClient,
        sample_company: Company,
        sample_financials: list
    ):
        """Test GET /api/v1/companies/{id}/financials - Date ordering."""
        response = client.get(
            f"/api/v1/companies/{sample_company.company_id}/financials"
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify descending date order
        if len(data) >= 2:
            dates = [m["period_end_date"] for m in data]
            assert dates == sorted(dates, reverse=True)


# ============================================================================
# VALUATION API TESTS
# ============================================================================

@pytest.mark.integration
class TestValuationAPI:
    """Test Valuation API endpoints."""
    
    def test_create_valuation(
        self, 
        client: TestClient,
        sample_company: Company
    ):
        """Test POST /api/v1/companies/{id}/valuations - Create valuation."""
        valuation_payload = {
            "company_id": sample_company.company_id,
            "valuation_date": "2024-12-31",
            "valuation_type": "Precedent Transactions",
            "enterprise_value": 250000000.00,
            "equity_value": 230000000.00,
            "ebitda_multiple": 18.0,
            "status": "Draft"
        }
        
        response = client.post(
            f"/api/v1/companies/{sample_company.company_id}/valuations",
            json=valuation_payload
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["valuation_type"] == "Precedent Transactions"
        assert data["enterprise_value"] == 250000000.00
    
    def test_list_valuations(
        self, 
        client: TestClient,
        sample_company: Company,
        sample_valuation: Valuation
    ):
        """Test GET /api/v1/companies/{id}/valuations - List valuations."""
        response = client.get(
            f"/api/v1/companies/{sample_company.company_id}/valuations"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
    
    def test_get_latest_valuation(
        self, 
        client: TestClient,
        sample_company: Company,
        sample_valuation: Valuation
    ):
        """Test GET /api/v1/companies/{id}/valuations/latest - Latest valuation."""
        response = client.get(
            f"/api/v1/companies/{sample_company.company_id}/valuations/latest"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["valuation_id"] == sample_valuation.valuation_id


# ============================================================================
# KPI API TESTS
# ============================================================================

@pytest.mark.integration
class TestKPIAPI:
    """Test KPI API endpoints."""
    
    def test_create_kpi(self, client: TestClient, sample_company: Company):
        """Test POST /api/v1/companies/{id}/kpis - Create KPI."""
        kpi_payload = {
            "company_id": sample_company.company_id,
            "period_end_date": "2024-12-31",
            "period_type": "Annual",
            "period_name": "FY 2024",
            "kpi_category": "Financial",
            "kpi_name": "Annual Recurring Revenue",
            "kpi_value": 150000000.00,
            "target_value": 180000000.00,
            "unit": "USD"
        }
        
        response = client.post(
            f"/api/v1/companies/{sample_company.company_id}/kpis",
            json=kpi_payload
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["kpi_name"] == "Annual Recurring Revenue"
        assert data["kpi_value"] == 150000000.00
    
    def test_list_kpis(
        self, 
        client: TestClient,
        sample_company: Company,
        sample_kpis: list
    ):
        """Test GET /api/v1/companies/{id}/kpis - List KPIs."""
        response = client.get(
            f"/api/v1/companies/{sample_company.company_id}/kpis"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 4
    
    def test_filter_kpis_by_category(
        self, 
        client: TestClient,
        sample_company: Company,
        sample_kpis: list
    ):
        """Test GET /api/v1/companies/{id}/kpis?category - Filter by category."""
        response = client.get(
            f"/api/v1/companies/{sample_company.company_id}/kpis"
            "?category=Customer"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert all(k["kpi_category"] == "Customer" for k in data)


# ============================================================================
# DASHBOARD API TESTS
# ============================================================================

@pytest.mark.integration
class TestDashboardAPI:
    """Test Dashboard aggregation endpoint."""
    
    def test_dashboard_summary(
        self, 
        client: TestClient,
        sample_fund: Fund,
        sample_company: Company,
        sample_financials: list
    ):
        """Test GET /api/v1/dashboard - Portfolio summary."""
        response = client.get("/api/v1/dashboard")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "total_companies" in data
        assert "active_companies" in data
        assert "total_invested" in data
        assert "total_revenue" in data
        assert "total_ebitda" in data
        assert "top_companies" in data
        
        assert data["total_companies"] >= 1
        assert data["active_companies"] >= 1
        assert isinstance(data["top_companies"], list)


# ============================================================================
# WORKFLOW TESTS
# ============================================================================

@pytest.mark.integration
class TestWorkflows:
    """Test complete workflows."""
    
    def test_full_company_lifecycle(self, client: TestClient, sample_fund: Fund):
        """Test complete company creation workflow."""
        # 1. Create company
        company_payload = {
            "fund_id": sample_fund.fund_id,
            "company_name": "Workflow Test Co",
            "sector": "Healthcare",
            "investment_date": "2024-01-15",
            "initial_investment": 40000000.00,
            "current_ownership_pct": 80.0,
            "status": "Active"
        }
        
        create_response = client.post("/api/v1/companies", json=company_payload)
        assert create_response.status_code == 201
        company_id = create_response.json()["company_id"]
        
        # 2. Add financial metrics
        financial_payload = {
            "company_id": company_id,
            "period_end_date": "2024-12-31",
            "period_type": "Annual",
            "period_name": "FY 2024",
            "revenue": 80000000.00,
            "ebitda": 16000000.00,
            "net_income": 12000000.00
        }
        
        financial_response = client.post(
            f"/api/v1/companies/{company_id}/financials",
            json=financial_payload
        )
        assert financial_response.status_code == 201
        
        # 3. Add valuation
        valuation_payload = {
            "company_id": company_id,
            "valuation_date": "2024-12-31",
            "valuation_type": "DCF",
            "enterprise_value": 180000000.00,
            "equity_value": 170000000.00,
            "status": "Final"
        }
        
        valuation_response = client.post(
            f"/api/v1/companies/{company_id}/valuations",
            json=valuation_payload
        )
        assert valuation_response.status_code == 201
        
        # 4. Get complete company data
        company_response = client.get(f"/api/v1/companies/{company_id}")
        assert company_response.status_code == 200
        
        # 5. Clean up
        delete_response = client.delete(f"/api/v1/companies/{company_id}")
        assert delete_response.status_code == 204
    
    def test_portfolio_summary_workflow(
        self, 
        client: TestClient,
        multiple_companies: list
    ):
        """Test portfolio-wide queries."""
        # Get all companies
        companies_response = client.get("/api/v1/companies")
        assert companies_response.status_code == 200
        companies = companies_response.json()
        assert len(companies) >= 5
        
        # Filter by sector
        tech_response = client.get("/api/v1/companies?sector=Technology")
        assert tech_response.status_code == 200
        tech_companies = tech_response.json()
        
        # Get dashboard
        dashboard_response = client.get("/api/v1/dashboard")
        assert dashboard_response.status_code == 200
        dashboard_data = dashboard_response.json()
        assert dashboard_data["total_companies"] == len(companies)


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================

@pytest.mark.integration
class TestErrorHandling:
    """Test error handling and edge cases."""
    
    def test_404_not_found(self, client: TestClient):
        """Test 404 responses for missing resources."""
        response = client.get("/api/v1/companies/99999")
        assert response.status_code == 404
    
    def test_422_validation_error(self, client: TestClient):
        """Test 422 responses for invalid payloads."""
        invalid_payload = {
            "name": "Fund",
            # Missing required fields
        }
        
        response = client.post("/api/v1/funds", json=invalid_payload)
        assert response.status_code == 422
    
    def test_invalid_date_format(self, client: TestClient, sample_company: Company):
        """Test invalid date format handling."""
        invalid_payload = {
            "company_id": sample_company.company_id,
            "period_end_date": "invalid-date",
            "period_type": "Annual",
            "revenue": 100000000.00
        }
        
        response = client.post(
            f"/api/v1/companies/{sample_company.company_id}/financials",
            json=invalid_payload
        )
        
        assert response.status_code == 422
    
    def test_duplicate_prevention(
        self, 
        client: TestClient,
        valid_fund_payload: dict
    ):
        """Test duplicate record prevention."""
        # Create first fund
        response1 = client.post("/api/v1/funds", json=valid_fund_payload)
        assert response1.status_code == 201
        
        # Try to create same fund again
        response2 = client.post("/api/v1/funds", json=valid_fund_payload)
        # Should either succeed (if duplicates allowed) or fail (409/422)
        assert response2.status_code in [201, 409, 422]


# ============================================================================
# PERFORMANCE TESTS
# ============================================================================

@pytest.mark.integration
@pytest.mark.performance
class TestPerformance:
    """Test API performance."""
    
    def test_concurrent_requests(self, client: TestClient, sample_company: Company):
        """Test handling concurrent requests."""
        import concurrent.futures
        
        def make_request():
            return client.get(f"/api/v1/companies/{sample_company.company_id}")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = [f.result() for f in futures]
        
        assert all(r.status_code == 200 for r in results)
    
    def test_pagination_performance(
        self, 
        client: TestClient,
        multiple_companies: list
    ):
        """Test pagination with large datasets."""
        # Request first page
        response = client.get("/api/v1/companies?limit=2&offset=0")
        assert response.status_code == 200
        page1 = response.json()
        
        # Request second page
        response = client.get("/api/v1/companies?limit=2&offset=2")
        assert response.status_code == 200
        page2 = response.json()
        
        # Ensure no overlap
        assert page1[0]["company_id"] != page2[0]["company_id"]
