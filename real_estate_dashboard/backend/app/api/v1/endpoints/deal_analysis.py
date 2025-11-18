"""
Deal Analysis API Endpoints

REST API for comprehensive real estate deal analysis.
100% FREE - No API keys required. All calculations performed locally.
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.services.deal_analysis_service import DealAnalysisService

router = APIRouter()
deal_service = DealAnalysisService()


# ========================================
# REQUEST/RESPONSE MODELS
# ========================================

class DealInputs(BaseModel):
    """Deal parameters for analysis"""
    purchase_price: float = Field(..., description="Purchase price of property")
    annual_income: float = Field(..., description="Annual gross income")
    annual_expenses: float = Field(..., description="Annual operating expenses")
    down_payment_pct: float = Field(20, description="Down payment percentage")
    interest_rate: float = Field(6.5, description="Loan interest rate")
    loan_term_years: int = Field(30, description="Loan term in years")
    closing_costs: Optional[float] = Field(None, description="Closing costs (defaults to 3% of purchase price)")
    rehab_costs: float = Field(0, description="Renovation/rehab costs")
    vacancy_rate: float = Field(5, description="Vacancy rate percentage")
    location_quality: float = Field(7, description="Location quality score (1-10)")
    market_growth_rate: float = Field(2, description="Annual market growth rate %")


class InvestorCriteria(BaseModel):
    """Investor's minimum requirements"""
    min_cap_rate: Optional[float] = None
    min_cash_on_cash: Optional[float] = None
    min_dscr: Optional[float] = None
    max_down_payment_pct: Optional[float] = None


class DealAnalysisRequest(BaseModel):
    """Request for deal analysis"""
    deal_inputs: DealInputs
    property_type: str = Field("multifamily", description="Property type: multifamily, single_family, commercial, fix_and_flip")
    investor_criteria: Optional[InvestorCriteria] = None


class MultiDealComparisonRequest(BaseModel):
    """Request for comparing multiple deals"""
    deals: List[Dict[str, Any]]


class BreakEvenRequest(BaseModel):
    """Request for break-even occupancy analysis"""
    annual_income: float
    annual_expenses: float
    annual_debt_service: float
    current_occupancy: float = 95


# ========================================
# ENDPOINTS
# ========================================

@router.post("/analyze")
async def analyze_deal(request: DealAnalysisRequest):
    """
    Perform comprehensive deal analysis

    **Analyzes a real estate investment deal and provides:**
    - Overall deal score (0-100)
    - Rating and recommendation
    - Financial, risk, and market scores
    - Key investment metrics (Cap Rate, Cash-on-Cash, DSCR)
    - Strengths and weaknesses
    - Investor criteria check

    **100% FREE - No API keys required. All calculations done locally.**

    **Scoring System:**
    - 80-100: Excellent (Strong Buy)
    - 70-79: Good (Buy)
    - 60-69: Fair (Consider)
    - 50-59: Below Average (Proceed with Caution)
    - 0-49: Poor (Pass)
    """
    try:
        # Convert Pydantic models to dicts
        deal_inputs_dict = request.deal_inputs.dict()

        # If closing_costs not provided, calculate it
        if deal_inputs_dict.get("closing_costs") is None:
            deal_inputs_dict["closing_costs"] = deal_inputs_dict["purchase_price"] * 0.03

        investor_criteria_dict = request.investor_criteria.dict() if request.investor_criteria else {}

        result = deal_service.analyze_deal(
            deal_inputs=deal_inputs_dict,
            property_type=request.property_type,
            investor_criteria=investor_criteria_dict
        )

        return {
            "success": True,
            "data": result,
            "property_type": request.property_type
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Deal analysis failed: {str(e)}"
        )


@router.post("/compare")
async def compare_deals(request: MultiDealComparisonRequest):
    """
    Compare multiple deals side-by-side

    **Compares multiple real estate deals and provides:**
    - Best deal identification
    - Statistical analysis (averages, ranges)
    - Rankings by overall score
    - Key metrics comparison

    **Use this to:**
    - Compare multiple opportunities
    - Identify the best deal
    - See how deals stack up against each other

    **100% FREE - No API keys required.**
    """
    try:
        result = deal_service.compare_deals(request.deals)

        return {
            "success": True,
            "data": result
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Deal comparison failed: {str(e)}"
        )


@router.post("/break-even")
async def calculate_break_even(request: BreakEvenRequest):
    """
    Calculate break-even occupancy rate

    **Calculates the minimum occupancy needed to cover expenses and debt service.**

    Provides:
    - Break-even occupancy percentage
    - Safety margin from current occupancy
    - Risk level assessment
    - Monthly cushion amount

    **Critical for:**
    - Understanding downside risk
    - Stress testing vacancy scenarios
    - Loan qualification (lenders look at this)
    - Risk management

    **100% FREE - No API keys required.**
    """
    try:
        result = deal_service.calculate_break_even_occupancy(
            annual_income=request.annual_income,
            annual_expenses=request.annual_expenses,
            annual_debt_service=request.annual_debt_service,
            current_occupancy=request.current_occupancy
        )

        return {
            "success": True,
            "data": result
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Break-even calculation failed: {str(e)}"
        )


@router.get("/templates/{property_type}")
async def get_deal_template(property_type: str):
    """
    Get sample deal template with realistic values

    **Property Types:**
    - multifamily
    - single_family
    - commercial
    - fix_and_flip

    **Returns sample values to help you get started with analysis.**

    **100% FREE - No API keys required.**
    """
    templates = {
        "multifamily": {
            "deal_inputs": {
                "purchase_price": 1000000,
                "annual_income": 120000,
                "annual_expenses": 45000,
                "down_payment_pct": 25,
                "interest_rate": 6.5,
                "loan_term_years": 30,
                "rehab_costs": 50000,
                "vacancy_rate": 5,
                "location_quality": 8,
                "market_growth_rate": 3
            },
            "property_type": "multifamily",
            "investor_criteria": {
                "min_cap_rate": 6.0,
                "min_cash_on_cash": 10.0,
                "min_dscr": 1.25,
                "max_down_payment_pct": 30
            }
        },
        "single_family": {
            "deal_inputs": {
                "purchase_price": 350000,
                "annual_income": 30000,
                "annual_expenses": 8000,
                "down_payment_pct": 20,
                "interest_rate": 7.0,
                "loan_term_years": 30,
                "rehab_costs": 15000,
                "vacancy_rate": 5,
                "location_quality": 7,
                "market_growth_rate": 2.5
            },
            "property_type": "single_family",
            "investor_criteria": {
                "min_cap_rate": 5.0,
                "min_cash_on_cash": 8.0,
                "min_dscr": 1.2,
                "max_down_payment_pct": 25
            }
        },
        "commercial": {
            "deal_inputs": {
                "purchase_price": 2000000,
                "annual_income": 200000,
                "annual_expenses": 60000,
                "down_payment_pct": 30,
                "interest_rate": 6.0,
                "loan_term_years": 25,
                "rehab_costs": 100000,
                "vacancy_rate": 10,
                "location_quality": 8,
                "market_growth_rate": 2
            },
            "property_type": "commercial",
            "investor_criteria": {
                "min_cap_rate": 7.0,
                "min_cash_on_cash": 12.0,
                "min_dscr": 1.3,
                "max_down_payment_pct": 35
            }
        },
        "fix_and_flip": {
            "deal_inputs": {
                "purchase_price": 250000,
                "annual_income": 0,  # Not applicable for flip
                "annual_expenses": 18000,  # Holding costs (6 months * $3k/month)
                "down_payment_pct": 20,
                "interest_rate": 8.0,
                "loan_term_years": 1,
                "rehab_costs": 75000,
                "vacancy_rate": 0,
                "location_quality": 7,
                "market_growth_rate": 3
            },
            "property_type": "fix_and_flip",
            "notes": "Fix & flip deals require different analysis - ARV and sale timeline are critical factors"
        }
    }

    if property_type not in templates:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template not found. Available types: {', '.join(templates.keys())}"
        )

    return {
        "success": True,
        "property_type": property_type,
        "template": templates[property_type]
    }


@router.post("/quick-score")
async def quick_score(
    cap_rate: float,
    cash_on_cash: float,
    dscr: float,
    property_type: str = "multifamily"
):
    """
    Quick deal scoring based on key metrics only

    **Fast analysis when you only have basic metrics.**

    Requires just 3 key numbers:
    - Cap Rate
    - Cash-on-Cash Return
    - DSCR (Debt Service Coverage Ratio)

    **100% FREE - No API keys required.**
    """
    try:
        # Use internal scoring methods
        financial_score = deal_service._calculate_financial_score(
            cap_rate, cash_on_cash, dscr, property_type
        )

        # Simple overall score (primarily financial)
        overall_score = financial_score * 0.9 + 10  # Add 10 base points

        if overall_score >= 80:
            rating = "Excellent"
            emoji = "🟢"
        elif overall_score >= 70:
            rating = "Good"
            emoji = "🟢"
        elif overall_score >= 60:
            rating = "Fair"
            emoji = "🟡"
        elif overall_score >= 50:
            rating = "Below Average"
            emoji = "🟡"
        else:
            rating = "Poor"
            emoji = "🔴"

        strengths = deal_service._identify_strengths(
            cap_rate, cash_on_cash, dscr, property_type
        )

        weaknesses = deal_service._identify_weaknesses(
            cap_rate, cash_on_cash, dscr, property_type
        )

        return {
            "success": True,
            "data": {
                "overall_score": round(overall_score, 1),
                "rating": rating,
                "emoji": emoji,
                "metrics": {
                    "cap_rate": cap_rate,
                    "cash_on_cash": cash_on_cash,
                    "dscr": dscr
                },
                "strengths": strengths,
                "weaknesses": weaknesses,
                "property_type": property_type
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Quick score failed: {str(e)}"
        )
