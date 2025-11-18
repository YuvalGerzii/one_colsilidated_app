"""
Tax Calculator API Endpoints

Provides REST API endpoints for various tax calculation tools.
"""

from typing import Dict, Any, Optional
from decimal import Decimal

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.config.tax_calculators import (
    DepreciationCalculator,
    EntityStructureCalculator,
    AMTCalculator,
    RetirementOptimizer
)
from app.config.audit_risk_compliance import (
    AuditRiskAssessment,
    ComplianceCalendar
)


router = APIRouter()


# ============================================================================
# Pydantic Schemas
# ============================================================================

class CostSegregationRequest(BaseModel):
    """Request for cost segregation analysis"""
    building_cost: float = Field(..., description="Total building cost (excluding land)")
    land_cost: float = Field(..., description="Land value")
    property_type: str = Field("commercial", description="'residential' or 'commercial'")


class EntityComparisonRequest(BaseModel):
    """Request for entity structure comparison"""
    net_income: float = Field(..., description="Annual net business income")
    reasonable_salary: Optional[float] = Field(None, description="Reasonable salary for S-Corp (default 40%)")
    state_tax_rate: float = Field(5.0, description="State income tax rate percentage")
    filing_status: str = Field("married", description="'single' or 'married'")


class AMTRequest(BaseModel):
    """Request for AMT calculation"""
    regular_taxable_income: float = Field(..., description="Regular taxable income")
    adjustments: Dict[str, float] = Field(
        default_factory=dict,
        description="AMT adjustments (e.g., {'state_tax': 10000, 'property_tax': 5000})"
    )
    filing_status: str = Field("married", description="'single', 'married', or 'head_of_household'")


class RetirementOptimizerRequest(BaseModel):
    """Request for retirement contribution optimization"""
    age: int = Field(..., description="Age of taxpayer")
    w2_income: float = Field(0, description="W-2 wage income")
    self_employment_income: float = Field(0, description="Self-employment income")
    spouse_income: float = Field(0, description="Spouse's income")
    has_hdhp: bool = Field(False, description="Covered by High Deductible Health Plan")


class AuditRiskRequest(BaseModel):
    """Request for audit risk assessment"""
    income: float = Field(..., description="Total income")
    business_type: str = Field("consulting", description="Type of business")
    deductions: Dict[str, float] = Field(default_factory=dict, description="Deductions by category")
    filing_status: str = Field("married", description="Filing status")
    has_schedule_c: bool = Field(False, description="Has Schedule C business")
    has_rental_properties: int = Field(0, description="Number of rental properties")
    claims_reps: bool = Field(False, description="Claims real estate professional status")
    has_foreign_accounts: bool = Field(False, description="Has foreign bank accounts")
    large_charitable: float = Field(0, description="Charitable contributions")
    home_office: bool = Field(False, description="Claims home office deduction")
    large_losses: float = Field(0, description="Business losses claimed")


# ============================================================================
# API Endpoints
# ============================================================================

@router.post("/cost-segregation")
async def calculate_cost_segregation(request: CostSegregationRequest) -> Dict[str, Any]:
    """
    Calculate cost segregation analysis

    Returns detailed breakdown of property components with accelerated depreciation
    potential and estimated tax savings.
    """
    try:
        result = DepreciationCalculator.cost_segregation_analysis(
            building_cost=Decimal(str(request.building_cost)),
            land_cost=Decimal(str(request.land_cost)),
            property_type=request.property_type
        )

        # Convert Decimal to float for JSON serialization
        return _convert_decimals_to_float(result)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error calculating cost segregation: {str(e)}"
        )


@router.post("/entity-comparison")
async def compare_entity_structures(request: EntityComparisonRequest) -> Dict[str, Any]:
    """
    Compare tax implications of LLC, S-Corp, and C-Corp

    Analyzes total tax burden under each structure and provides
    recommendations based on income level.
    """
    try:
        reasonable_salary = None
        if request.reasonable_salary:
            reasonable_salary = Decimal(str(request.reasonable_salary))

        result = EntityStructureCalculator.compare_structures(
            net_income=Decimal(str(request.net_income)),
            reasonable_salary=reasonable_salary,
            state_tax_rate=Decimal(str(request.state_tax_rate)),
            filing_status=request.filing_status
        )

        return _convert_decimals_to_float(result)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error comparing entity structures: {str(e)}"
        )


@router.post("/amt-calculator")
async def calculate_amt(request: AMTRequest) -> Dict[str, Any]:
    """
    Calculate Alternative Minimum Tax exposure

    Determines if taxpayer is subject to AMT and calculates the amount.
    """
    try:
        # Convert adjustments to Decimal
        adjustments = {
            key: Decimal(str(value))
            for key, value in request.adjustments.items()
        }

        result = AMTCalculator.calculate_amt(
            regular_taxable_income=Decimal(str(request.regular_taxable_income)),
            adjustments=adjustments,
            filing_status=request.filing_status
        )

        return _convert_decimals_to_float(result)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error calculating AMT: {str(e)}"
        )


@router.post("/retirement-optimizer")
async def optimize_retirement_contributions(request: RetirementOptimizerRequest) -> Dict[str, Any]:
    """
    Calculate maximum retirement contributions across all vehicles

    Analyzes 401(k), IRA, Solo 401(k), HSA, and other retirement savings options
    to maximize tax-advantaged contributions.
    """
    try:
        result = RetirementOptimizer.maximize_contributions(
            age=request.age,
            w2_income=Decimal(str(request.w2_income)),
            self_employment_income=Decimal(str(request.self_employment_income)),
            spouse_income=Decimal(str(request.spouse_income)),
            has_hdhp=request.has_hdhp
        )

        return _convert_decimals_to_float(result)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error optimizing retirement contributions: {str(e)}"
        )


@router.get("/depreciation-schedule/{cost}/{years}/{method}")
async def get_depreciation_schedule(
    cost: float,
    years: int = 27,
    method: str = "residential"
) -> Dict[str, Any]:
    """
    Get complete depreciation schedule for property

    Args:
        cost: Depreciable basis
        years: Number of years to calculate (default 27 for residential)
        method: 'residential' (27.5 years) or 'commercial' (39 years)

    Returns:
        Year-by-year depreciation schedule
    """
    try:
        cost_decimal = Decimal(str(cost))
        schedule = []

        max_years = 28 if method == 'residential' else 40

        for year in range(1, min(years + 1, max_years + 1)):
            if method == 'residential':
                annual_depr = DepreciationCalculator.macrs_gds_residential(cost_decimal, year)
            else:
                annual_depr = DepreciationCalculator.macrs_gds_commercial(cost_decimal, year)

            schedule.append({
                'year': year,
                'depreciation': float(annual_depr),
                'accumulated': float(sum(s['depreciation'] for s in schedule) + float(annual_depr)),
                'remaining_basis': float(cost_decimal - sum(s['depreciation'] for s in schedule) - float(annual_depr))
            })

        return {
            'cost': cost,
            'method': method,
            'total_years': max_years,
            'schedule': schedule
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error generating depreciation schedule: {str(e)}"
        )


@router.post("/audit-risk")
async def assess_audit_risk(request: AuditRiskRequest) -> Dict[str, Any]:
    """
    Assess IRS audit risk based on tax return characteristics

    Analyzes red flags and provides risk score with recommendations.
    """
    try:
        deductions = {key: Decimal(str(value)) for key, value in request.deductions.items()}

        result = AuditRiskAssessment.assess_risk(
            income=Decimal(str(request.income)),
            business_type=request.business_type,
            deductions=deductions,
            filing_status=request.filing_status,
            has_schedule_c=request.has_schedule_c,
            has_rental_properties=request.has_rental_properties,
            claims_reps=request.claims_reps,
            has_foreign_accounts=request.has_foreign_accounts,
            large_charitable=Decimal(str(request.large_charitable)),
            home_office=request.home_office,
            large_losses=Decimal(str(request.large_losses))
        )

        return result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error assessing audit risk: {str(e)}"
        )


@router.get("/compliance-calendar/{year}")
async def get_compliance_calendar(year: int = 2025) -> Dict[str, Any]:
    """
    Get full compliance calendar for the year with all tax deadlines
    """
    try:
        calendar = ComplianceCalendar.get_annual_calendar(year)
        return {
            'year': year,
            'calendar': calendar
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error generating compliance calendar: {str(e)}"
        )


@router.get("/compliance-calendar/upcoming/{days}")
async def get_upcoming_deadlines(days: int = 90) -> Dict[str, Any]:
    """
    Get upcoming tax deadlines for next N days
    """
    try:
        deadlines = ComplianceCalendar.get_upcoming_deadlines(days)
        return {
            'days_ahead': days,
            'total_upcoming': len(deadlines),
            'deadlines': deadlines
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error getting upcoming deadlines: {str(e)}"
        )


# ============================================================================
# Helper Functions
# ============================================================================

def _convert_decimals_to_float(obj):
    """Recursively convert Decimal objects to float for JSON serialization"""
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, dict):
        return {key: _convert_decimals_to_float(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [_convert_decimals_to_float(item) for item in obj]
    else:
        return obj
