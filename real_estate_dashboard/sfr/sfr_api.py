"""
Single-Family Rental API Endpoints
===================================

REST API for SFR property analysis integrated with Portfolio Dashboard

Endpoints:
- POST /api/sfr/analyze - Analyze new property
- GET /api/sfr/properties/{property_id} - Get property details
- GET /api/sfr/properties/{property_id}/cashflows - Get cash flow projections
- GET /api/sfr/properties/{property_id}/scenarios - Get exit scenarios
- GET /api/sfr/portfolio/summary - Get portfolio metrics
- GET /api/sfr/portfolio/top-performers - Get best properties

Author: Financial Modeling AI
Date: November 2025
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime
from decimal import Decimal
import os

from sfr_analysis_service import (
    SFRAnalysisService,
    SFRProperty,
    SFRFinancing
)

# Initialize FastAPI app
app = FastAPI(
    title="Single-Family Rental Analysis API",
    description="REST API for analyzing mortgage-financed rental properties",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
DB_CONNECTION = os.getenv(
    "DATABASE_URL",
    "dbname=portfolio_dashboard user=admin password=secure123 host=localhost"
)


# ============================================================================
# PYDANTIC MODELS (Request/Response)
# ============================================================================

class PropertyRequest(BaseModel):
    """Request model for property analysis"""
    
    # Company/Fund
    company_id: int
    fund_id: Optional[int] = None
    
    # Property identification
    property_name: str = Field(..., description="Property address or name")
    address: str
    city: str
    state: str
    zip_code: str
    
    # Property details
    square_feet: int = Field(..., gt=0)
    bedrooms: int = Field(..., ge=0)
    bathrooms: float = Field(..., ge=0)
    year_built: Optional[int] = None
    
    # Acquisition
    purchase_price: float = Field(..., gt=0, description="Purchase price in dollars")
    closing_costs: float = Field(default=0, ge=0)
    renovation_budget: float = Field(default=0, ge=0)
    acquisition_date: Optional[date] = None
    
    # Rental
    monthly_rent: float = Field(..., gt=0, description="Expected monthly rent")
    market_rent: Optional[float] = None
    vacancy_rate: float = Field(default=5.0, ge=0, le=100, description="Vacancy rate %")
    
    # Growth assumptions
    annual_rent_growth: float = Field(default=3.0, description="Rent growth %")
    annual_expense_growth: float = Field(default=2.0, description="Expense growth %")
    annual_appreciation: float = Field(default=4.0, description="Property appreciation %")
    
    # Monthly expenses
    property_tax_monthly: float = Field(..., ge=0)
    insurance_monthly: float = Field(..., ge=0)
    hoa_monthly: float = Field(default=0, ge=0)
    utilities_monthly: float = Field(default=0, ge=0)
    management_fee_pct: float = Field(default=10.0, ge=0, le=100)
    maintenance_reserve_monthly: float = Field(..., ge=0)
    capex_reserve_monthly: float = Field(..., ge=0)
    
    # Financing
    down_payment_pct: float = Field(..., gt=0, le=100, description="Down payment %")
    interest_rate: float = Field(..., gt=0, le=20, description="Annual interest rate %")
    loan_term_years: int = Field(default=30, description="Loan term in years")
    loan_type: str = Field(default="Conventional")
    
    # Strategy
    investment_strategy: str = Field(default="Buy & Hold")
    hold_period_years: int = Field(default=10, ge=1, le=50)
    
    class Config:
        json_schema_extra = {
            "example": {
                "company_id": 1,
                "fund_id": 1,
                "property_name": "123 Main Street",
                "address": "123 Main Street",
                "city": "Austin",
                "state": "TX",
                "zip_code": "78701",
                "square_feet": 1500,
                "bedrooms": 3,
                "bathrooms": 2.0,
                "year_built": 2015,
                "purchase_price": 150000,
                "closing_costs": 3000,
                "renovation_budget": 45000,
                "monthly_rent": 2450,
                "vacancy_rate": 5.0,
                "property_tax_monthly": 350,
                "insurance_monthly": 125,
                "maintenance_reserve_monthly": 200,
                "capex_reserve_monthly": 150,
                "down_payment_pct": 25.0,
                "interest_rate": 7.5,
                "loan_term_years": 30,
                "investment_strategy": "Buy & Hold"
            }
        }


class PropertyResponse(BaseModel):
    """Response model for property analysis"""
    property_id: int
    status: str
    summary: dict
    scenarios: List[dict]
    
    class Config:
        json_schema_extra = {
            "example": {
                "property_id": 42,
                "status": "SUCCESS",
                "summary": {
                    "investment_decision": "BUY",
                    "cash_on_cash_return": 15.5,
                    "ten_year_irr": 18.2,
                    "monthly_cash_flow": 206.00,
                    "cap_rate": 7.9,
                    "dscr": 1.27
                },
                "scenarios": [
                    {
                        "scenario_name": "Hold 10 Years",
                        "irr": 18.2,
                        "equity_multiple": 4.42
                    }
                ]
            }
        }


class PortfolioSummaryResponse(BaseModel):
    """Response model for portfolio summary"""
    fund_name: str
    total_properties: int
    total_invested: float
    total_annual_rent: float
    avg_cash_on_cash: float
    avg_irr: float
    portfolio_yield: float
    avg_dscr: float


# ============================================================================
# DEPENDENCIES
# ============================================================================

def get_sfr_service() -> SFRAnalysisService:
    """Dependency injection for SFR service"""
    return SFRAnalysisService(DB_CONNECTION)


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """API health check"""
    return {
        "service": "SFR Analysis API",
        "status": "operational",
        "version": "1.0.0",
        "endpoints": {
            "analyze": "POST /api/sfr/analyze",
            "properties": "GET /api/sfr/properties/{property_id}",
            "cash_flows": "GET /api/sfr/properties/{property_id}/cashflows",
            "scenarios": "GET /api/sfr/properties/{property_id}/scenarios",
            "portfolio": "GET /api/sfr/portfolio/summary",
            "top_performers": "GET /api/sfr/portfolio/top-performers"
        }
    }


@app.post("/api/sfr/analyze", response_model=PropertyResponse)
async def analyze_property(
    request: PropertyRequest,
    service: SFRAnalysisService = Depends(get_sfr_service)
):
    """
    Analyze a single-family rental property with mortgage financing
    
    Calculates:
    - Monthly cash flows for 10 years
    - IRR, Cash-on-Cash Return, Cap Rate, DSCR
    - Exit scenarios (Flip, BRRRR, Hold 10yr, Hold Forever)
    - Investment recommendation
    
    Returns:
    - property_id for future reference
    - Summary metrics
    - Exit scenarios
    """
    try:
        # Calculate derived values
        total_acquisition = (
            request.purchase_price + 
            request.closing_costs + 
            request.renovation_budget
        )
        
        down_payment_amount = request.purchase_price * (request.down_payment_pct / 100)
        loan_amount = request.purchase_price - down_payment_amount
        ltv = (loan_amount / request.purchase_price) * 100
        
        total_cash_invested = (
            down_payment_amount + 
            request.closing_costs + 
            request.renovation_budget
        )
        
        # Create property object
        property = SFRProperty(
            company_id=request.company_id,
            fund_id=request.fund_id,
            property_name=request.property_name,
            address=request.address,
            city=request.city,
            state=request.state,
            zip_code=request.zip_code,
            square_feet=request.square_feet,
            bedrooms=request.bedrooms,
            bathrooms=Decimal(str(request.bathrooms)),
            year_built=request.year_built,
            purchase_price=Decimal(str(request.purchase_price)),
            closing_costs=Decimal(str(request.closing_costs)),
            renovation_budget=Decimal(str(request.renovation_budget)),
            total_acquisition_cost=Decimal(str(total_acquisition)),
            acquisition_date=request.acquisition_date or date.today(),
            monthly_rent=Decimal(str(request.monthly_rent)),
            market_rent=Decimal(str(request.market_rent)) if request.market_rent else None,
            vacancy_rate=Decimal(str(request.vacancy_rate)),
            annual_rent_growth=Decimal(str(request.annual_rent_growth)),
            annual_expense_growth=Decimal(str(request.annual_expense_growth)),
            annual_appreciation=Decimal(str(request.annual_appreciation)),
            property_tax_monthly=Decimal(str(request.property_tax_monthly)),
            insurance_monthly=Decimal(str(request.insurance_monthly)),
            hoa_monthly=Decimal(str(request.hoa_monthly)),
            utilities_monthly=Decimal(str(request.utilities_monthly)),
            management_fee_pct=Decimal(str(request.management_fee_pct)),
            maintenance_reserve_monthly=Decimal(str(request.maintenance_reserve_monthly)),
            capex_reserve_monthly=Decimal(str(request.capex_reserve_monthly)),
            investment_strategy=request.investment_strategy,
            hold_period_years=request.hold_period_years,
            status="Analysis"
        )
        
        # Create financing object
        financing = SFRFinancing(
            down_payment=Decimal(str(down_payment_amount)),
            closing_costs_cash=Decimal(str(request.closing_costs)),
            renovation_cash=Decimal(str(request.renovation_budget)),
            total_cash_invested=Decimal(str(total_cash_invested)),
            loan_amount=Decimal(str(loan_amount)),
            loan_type=request.loan_type,
            interest_rate=Decimal(str(request.interest_rate)),
            loan_term_months=request.loan_term_years * 12,
            ltv_ratio=Decimal(str(ltv))
        )
        
        # Run analysis
        result = service.run_complete_analysis(property, financing)
        
        if result['status'] == 'SUCCESS':
            # Convert Decimals to floats for JSON response
            summary = {k: (float(v) if isinstance(v, Decimal) else v) 
                      for k, v in result['summary'].items()}
            
            scenarios = []
            for scenario in result['scenarios']:
                scenarios.append({
                    k: (float(v) if isinstance(v, Decimal) else v)
                    for k, v in scenario.items()
                })
            
            return PropertyResponse(
                property_id=result['property_id'],
                status="SUCCESS",
                summary=summary,
                scenarios=scenarios
            )
        else:
            raise HTTPException(status_code=500, detail=result['error'])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/sfr/properties/{property_id}")
async def get_property_details(
    property_id: int,
    service: SFRAnalysisService = Depends(get_sfr_service)
):
    """Get complete property details including summary and scenarios"""
    try:
        with service.get_connection() as conn:
            with conn.cursor() as cur:
                # Get property
                cur.execute("""
                    SELECT p.*, f.*, s.*
                    FROM sfr_properties p
                    JOIN sfr_financing f ON p.property_id = f.property_id
                    LEFT JOIN sfr_analysis_summary s ON p.property_id = s.property_id
                    WHERE p.property_id = %s
                    ORDER BY s.analysis_date DESC
                    LIMIT 1
                """, (property_id,))
                
                result = cur.fetchone()
                
                if not result:
                    raise HTTPException(status_code=404, detail="Property not found")
                
                # Convert Decimals to floats
                return {k: (float(v) if isinstance(v, Decimal) else v) 
                       for k, v in dict(result).items()}
                
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/sfr/properties/{property_id}/cashflows")
async def get_cash_flows(
    property_id: int,
    year: Optional[int] = None,
    service: SFRAnalysisService = Depends(get_sfr_service)
):
    """
    Get monthly cash flow projections
    
    Query params:
    - year: Filter by specific year (1-10)
    """
    try:
        with service.get_connection() as conn:
            with conn.cursor() as cur:
                if year:
                    cur.execute("""
                        SELECT * FROM sfr_cash_flows
                        WHERE property_id = %s AND year_number = %s
                        ORDER BY month_number
                    """, (property_id, year))
                else:
                    cur.execute("""
                        SELECT * FROM sfr_cash_flows
                        WHERE property_id = %s
                        ORDER BY year_number, month_number
                    """, (property_id,))
                
                results = cur.fetchall()
                
                if not results:
                    raise HTTPException(status_code=404, detail="Cash flows not found")
                
                # Convert Decimals to floats
                return [
                    {k: (float(v) if isinstance(v, Decimal) else v) 
                     for k, v in dict(row).items()}
                    for row in results
                ]
                
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/sfr/properties/{property_id}/scenarios")
async def get_exit_scenarios(
    property_id: int,
    service: SFRAnalysisService = Depends(get_sfr_service)
):
    """Get exit scenario analysis (Flip, BRRRR, Hold 10yr, Hold Forever)"""
    try:
        with service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT * FROM sfr_scenarios
                    WHERE property_id = %s
                    ORDER BY 
                        CASE scenario_type
                            WHEN 'Flip' THEN 1
                            WHEN 'BRRRR' THEN 2
                            WHEN 'Hold' THEN 3
                            WHEN 'Hold Forever' THEN 4
                        END
                """, (property_id,))
                
                results = cur.fetchall()
                
                if not results:
                    raise HTTPException(status_code=404, detail="Scenarios not found")
                
                # Convert Decimals to floats
                return [
                    {k: (float(v) if isinstance(v, Decimal) else v) 
                     for k, v in dict(row).items()}
                    for row in results
                ]
                
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/sfr/portfolio/summary", response_model=PortfolioSummaryResponse)
async def get_portfolio_summary(
    fund_id: Optional[int] = None,
    service: SFRAnalysisService = Depends(get_sfr_service)
):
    """
    Get portfolio-level summary metrics
    
    Query params:
    - fund_id: Filter by specific fund (optional)
    """
    try:
        result = service.get_portfolio_summary(fund_id)
        
        if not result:
            raise HTTPException(status_code=404, detail="Portfolio data not found")
        
        # Convert Decimals to floats
        return {k: (float(v) if isinstance(v, Decimal) else v) 
               for k, v in dict(result).items()}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/sfr/portfolio/top-performers")
async def get_top_performers(
    limit: int = 10,
    service: SFRAnalysisService = Depends(get_sfr_service)
):
    """
    Get best performing properties by IRR
    
    Query params:
    - limit: Number of properties to return (default: 10, max: 50)
    """
    try:
        if limit > 50:
            limit = 50
        
        results = service.get_top_performers(limit)
        
        # Convert Decimals to floats
        return [
            {k: (float(v) if isinstance(v, Decimal) else v) 
             for k, v in dict(row).items()}
            for row in results
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/sfr/portfolio/at-risk")
async def get_properties_at_risk(
    service: SFRAnalysisService = Depends(get_sfr_service)
):
    """Get properties that need attention (negative CF, low DSCR, high vacancy risk)"""
    try:
        with service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM vw_sfr_properties_at_risk")
                results = cur.fetchall()
                
                # Convert Decimals to floats
                return [
                    {k: (float(v) if isinstance(v, Decimal) else v) 
                     for k, v in dict(row).items()}
                    for row in results
                ]
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "sfr_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
