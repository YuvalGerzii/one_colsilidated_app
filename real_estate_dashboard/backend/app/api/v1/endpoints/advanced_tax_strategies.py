"""
API endpoints for advanced tax strategy calculators.

These endpoints provide sophisticated tax planning calculations for high net worth individuals
and businesses. All strategies require professional implementation.
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from decimal import Decimal

from app.config.advanced_calculators import (
    Section179BonusOptimizer,
    DSTAnalyzer,
    CaptiveInsuranceCalculator,
    CRTCalculator,
    OilGasInvestmentCalculator
)
from app.config.tax_shelters_and_structures import (
    TaxShelterEvaluator,
    ShelfCompanyAnalyzer,
    InternationalTaxPlanner
)

router = APIRouter()


# Pydantic models for request/response validation
class Section179Request(BaseModel):
    asset_purchases: List[Dict[str, Any]] = Field(..., description="List of assets with cost, name, class_life")
    business_income: float = Field(..., gt=0, description="Taxable income before depreciation")
    tax_year: int = Field(2024, ge=2024, le=2027)
    state_bonus_conformity: bool = Field(True, description="Does state conform to bonus depreciation?")


class DSTRequest(BaseModel):
    relinquished_property_value: float = Field(..., gt=0)
    debt_on_relinquished: float = Field(..., ge=0)
    capital_gains_rate: float = Field(0.20, ge=0, le=0.40)
    depreciation_recapture_rate: float = Field(0.25)
    dst_properties: Optional[List[Dict[str, Any]]] = None


class CaptiveInsuranceRequest(BaseModel):
    annual_premium: float = Field(..., gt=0, le=3_000_000)
    operating_company_revenue: float = Field(..., gt=0)
    loss_ratio_5yr: float = Field(..., ge=0, le=1.0, description="Claims/Premiums over 5 years")
    has_financing_arrangement: bool = Field(False, description="Loans/guarantees back to insured?")


class CRTRequest(BaseModel):
    asset_value: float = Field(..., gt=0)
    cost_basis: float = Field(..., ge=0)
    annual_payout_rate: float = Field(0.05, ge=0.05, le=0.50, description="5-50% annual payout")
    term_years: int = Field(0, ge=0, le=20, description="0 for lifetime, max 20 years")
    beneficiary_age: int = Field(..., ge=1, le=120)
    is_unitrust: bool = Field(True, description="True for CRUT, False for CRAT")
    section_7520_rate: float = Field(0.054, ge=0, le=0.15, description="Current IRS 7520 rate")


class OilGasRequest(BaseModel):
    investment_amount: float = Field(..., gt=0)
    idc_percentage: float = Field(0.75, ge=0, le=1.0)
    tangible_percentage: float = Field(0.15, ge=0, le=1.0)
    working_interest: bool = Field(True, description="Working vs Royalty interest")
    income_phase: float = Field(0.85, ge=0, le=1.0)


class TaxShelterRequest(BaseModel):
    strategy_name: str
    investment_amount: float = Field(..., gt=0)
    expected_deduction: float = Field(..., ge=0)
    expected_loss: float = Field(..., ge=0)
    years_to_breakeven: int = Field(..., ge=1)
    has_economic_substance: bool
    has_business_purpose: bool
    promoter_fees_pct: float = Field(..., ge=0, le=1.0)
    involves_tax_haven: bool = Field(False)


class ShelfCompanyRequest(BaseModel):
    purchase_price: float = Field(..., gt=0)
    company_age_years: int = Field(..., ge=1)
    has_credit_history: bool
    intended_use: str
    formation_state: str = Field("delaware")


class InternationalRequest(BaseModel):
    us_business_income: float = Field(..., ge=0)
    foreign_operations_income: float = Field(..., gt=0)
    has_real_foreign_operations: bool
    employees_abroad: int = Field(..., ge=0)
    target_country: str = Field("ireland")


# Helper function to convert Decimal to float for JSON serialization
def _convert_decimals_to_float(obj):
    """Recursively convert Decimal objects to float."""
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, dict):
        return {k: _convert_decimals_to_float(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_convert_decimals_to_float(item) for item in obj]
    return obj


@router.post("/section-179-optimizer")
async def optimize_section_179(request: Section179Request) -> Dict[str, Any]:
    """
    Optimize between Section 179 and Bonus Depreciation for maximum tax benefit.

    Returns detailed strategy comparison with recommendations.
    """
    try:
        result = Section179BonusOptimizer.optimize_depreciation(
            asset_purchases=request.asset_purchases,
            business_income=request.business_income,
            tax_year=request.tax_year,
            state_bonus_conformity=request.state_bonus_conformity
        )
        return _convert_decimals_to_float(result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error calculating Section 179 optimization: {str(e)}"
        )


@router.post("/dst-1031-analysis")
async def analyze_dst(request: DSTRequest) -> Dict[str, Any]:
    """
    Analyze Delaware Statutory Trust (DST) for 1031 exchange.

    Returns DST investment analysis with tax deferral calculations.
    """
    try:
        result = DSTAnalyzer.analyze_dst_investment(
            relinquished_property_value=request.relinquished_property_value,
            debt_on_relinquished=request.debt_on_relinquished,
            capital_gains_rate=request.capital_gains_rate,
            depreciation_recapture_rate=request.depreciation_recapture_rate,
            dst_properties=request.dst_properties
        )
        return _convert_decimals_to_float(result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error analyzing DST: {str(e)}"
        )


@router.post("/captive-insurance-feasibility")
async def calculate_captive_feasibility(request: CaptiveInsuranceRequest) -> Dict[str, Any]:
    """
    Calculate 831(b) micro-captive insurance feasibility and IRS risk.

    WARNING: Under intense IRS scrutiny. Listed transaction if meets criteria.
    """
    try:
        result = CaptiveInsuranceCalculator.calculate_831b_feasibility(
            annual_premium=request.annual_premium,
            operating_company_revenue=request.operating_company_revenue,
            loss_ratio_5yr=request.loss_ratio_5yr,
            has_financing_arrangement=request.has_financing_arrangement
        )
        return _convert_decimals_to_float(result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error calculating captive insurance feasibility: {str(e)}"
        )


@router.post("/charitable-remainder-trust")
async def calculate_crt(request: CRTRequest) -> Dict[str, Any]:
    """
    Calculate Charitable Remainder Trust (CRT/CRUT) benefits.

    Returns tax deferral, income stream, and charitable deduction analysis.
    """
    try:
        result = CRTCalculator.calculate_crt_benefits(
            asset_value=request.asset_value,
            cost_basis=request.cost_basis,
            annual_payout_rate=request.annual_payout_rate,
            term_years=request.term_years,
            beneficiary_age=request.beneficiary_age,
            is_unitrust=request.is_unitrust,
            section_7520_rate=request.section_7520_rate
        )
        return _convert_decimals_to_float(result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error calculating CRT benefits: {str(e)}"
        )


@router.post("/oil-gas-investment")
async def calculate_oil_gas(request: OilGasRequest) -> Dict[str, Any]:
    """
    Calculate oil & gas investment tax benefits.

    Returns IDC deductions, depletion allowance, and tax savings analysis.
    """
    try:
        result = OilGasInvestmentCalculator.calculate_oil_gas_benefits(
            investment_amount=request.investment_amount,
            idc_percentage=request.idc_percentage,
            tangible_percentage=request.tangible_percentage,
            working_interest=request.working_interest,
            income_phase=request.income_phase
        )
        return _convert_decimals_to_float(result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error calculating oil & gas benefits: {str(e)}"
        )


@router.post("/tax-shelter-evaluation")
async def evaluate_tax_shelter(request: TaxShelterRequest) -> Dict[str, Any]:
    """
    Evaluate tax shelter strategy for legitimacy and IRS risk.

    Returns risk score, economic substance analysis, and potential penalties.
    """
    try:
        result = TaxShelterEvaluator.evaluate_tax_shelter(
            strategy_name=request.strategy_name,
            investment_amount=request.investment_amount,
            expected_deduction=request.expected_deduction,
            expected_loss=request.expected_loss,
            years_to_breakeven=request.years_to_breakeven,
            has_economic_substance=request.has_economic_substance,
            has_business_purpose=request.has_business_purpose,
            promoter_fees_pct=request.promoter_fees_pct,
            involves_tax_haven=request.involves_tax_haven
        )
        return _convert_decimals_to_float(result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error evaluating tax shelter: {str(e)}"
        )


@router.get("/tax-shelter-comparison")
async def compare_legitimate_shelters() -> Dict[str, Any]:
    """
    Compare legitimate tax shelter strategies with risk/reward profiles.
    """
    try:
        result = TaxShelterEvaluator.compare_legitimate_shelters()
        return _convert_decimals_to_float(result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error comparing tax shelters: {str(e)}"
        )


@router.post("/shelf-company-analysis")
async def analyze_shelf_company(request: ShelfCompanyRequest) -> Dict[str, Any]:
    """
    Analyze shelf company (aged corporation) for risks and benefits.

    Returns legitimacy analysis and compliance requirements.
    """
    try:
        result = ShelfCompanyAnalyzer.analyze_shelf_company(
            purchase_price=request.purchase_price,
            company_age_years=request.company_age_years,
            has_credit_history=request.has_credit_history,
            intended_use=request.intended_use,
            formation_state=request.formation_state
        )
        return _convert_decimals_to_float(result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error analyzing shelf company: {str(e)}"
        )


@router.get("/shelf-company-states")
async def get_formation_states() -> Dict[str, Any]:
    """
    Get comparison of business-friendly formation states.
    """
    try:
        return ShelfCompanyAnalyzer.FORMATION_STATES
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error retrieving formation states: {str(e)}"
        )


@router.post("/international-tax-planning")
async def analyze_international_structure(request: InternationalRequest) -> Dict[str, Any]:
    """
    Analyze international tax planning structure (LEGAL implementations only).

    Requires real economic substance. Returns GILTI, FTC, and compliance analysis.
    """
    try:
        result = InternationalTaxPlanner.analyze_international_structure(
            us_business_income=request.us_business_income,
            foreign_operations_income=request.foreign_operations_income,
            has_real_foreign_operations=request.has_real_foreign_operations,
            employees_abroad=request.employees_abroad,
            target_country=request.target_country
        )
        return _convert_decimals_to_float(result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error analyzing international structure: {str(e)}"
        )


@router.get("/international-jurisdictions")
async def get_tax_treaty_countries() -> Dict[str, Any]:
    """
    Get comparison of international tax jurisdictions with treaty benefits.
    """
    try:
        return InternationalTaxPlanner.TAX_TREATY_COUNTRIES
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error retrieving jurisdictions: {str(e)}"
        )
