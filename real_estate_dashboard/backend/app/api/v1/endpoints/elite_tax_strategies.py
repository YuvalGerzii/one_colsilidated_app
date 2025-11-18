"""
API endpoints for elite tax loopholes and strategies.

These are lesser-known but 100% legal strategies that require sophisticated implementation.
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from decimal import Decimal

from app.config.elite_tax_loopholes import (
    QSBSCalculator,
    AugustaRuleCalculator,
    REPSCalculator,
    MegaBackdoorRothCalculator,
    CashBalancePlanCalculator,
    SCorpSalaryOptimizer,
    EstatePlanningCalculator,
    TaxLossHarvestingCalculator
)

router = APIRouter()


# Pydantic models for request/response validation
class QSBSRequest(BaseModel):
    acquisition_date: str = Field(..., description="YYYY-MM-DD format")
    sale_date: str = Field(..., description="YYYY-MM-DD format")
    sale_price: float = Field(..., gt=0)
    cost_basis: float = Field(..., gt=0)
    company_assets_at_issuance: float = Field(..., ge=0, le=50_000_000)
    is_qualified_business: bool = Field(True)
    acquired_at_original_issue: bool = Field(True)


class AugustaRuleRequest(BaseModel):
    rental_days: int = Field(..., ge=1, le=14)
    daily_rate: float = Field(..., gt=0)
    comparable_venue_rate: float = Field(..., gt=0)
    business_structure: str = Field("s_corp")
    business_tax_rate: float = Field(0.21, ge=0, le=1.0)
    personal_tax_rate: float = Field(0.37, ge=0, le=1.0)


class REPSRequest(BaseModel):
    real_estate_hours: int = Field(..., ge=0)
    total_work_hours: int = Field(..., gt=0)
    rental_properties: int = Field(..., ge=1)
    rental_losses: float
    w2_income: float = Field(0, ge=0)
    make_grouping_election: bool = Field(True)
    properties_material_participation: Optional[List[Dict[str, int]]] = None


class MegaBackdoorRequest(BaseModel):
    age: int = Field(..., ge=18, le=100)
    current_401k_deferrals: float = Field(..., ge=0)
    employer_match: float = Field(..., ge=0)
    plan_allows_after_tax: bool = Field(True)
    plan_allows_in_service_conversion: bool = Field(True)
    tax_year: int = Field(2024, ge=2024, le=2025)


class CashBalanceRequest(BaseModel):
    age: int = Field(..., ge=18, le=100)
    w2_compensation: float = Field(..., gt=0)
    business_net_income: float = Field(..., gt=0)
    current_401k_contribution: float = Field(0, ge=0)
    employees_count: int = Field(0, ge=0)
    target_retirement_age: int = Field(65, ge=55, le=75)


class SCorpSalaryRequest(BaseModel):
    net_business_income: float = Field(..., gt=0)
    industry: str
    years_in_business: int = Field(..., ge=0)
    business_duties: str = Field("owner_operator")
    geographic_area: str = Field("national_avg")


class GRATRequest(BaseModel):
    asset_value: float = Field(..., gt=0)
    grat_term_years: int = Field(..., ge=2, le=10)
    section_7520_rate: float = Field(0.054, ge=0, le=0.15)
    expected_appreciation_rate: float = Field(0.10, ge=0, le=1.0)
    annual_annuity_percentage: Optional[float] = None


class IDGTSLATRequest(BaseModel):
    asset_value: float = Field(..., gt=0)
    gift_tax_exemption_used: float = Field(..., ge=0)
    trust_term_years: int = Field(..., ge=1)
    expected_appreciation_rate: float = Field(0.08, ge=0, le=1.0)
    grantor_pays_income_tax: bool = Field(True)


class TaxLossHarvestingRequest(BaseModel):
    capital_gains_realized: float = Field(..., ge=0)
    available_losses: float = Field(..., ge=0)
    ordinary_income: float = Field(..., ge=0)
    holding_period: str = Field("long_term")
    has_carryforward_losses: float = Field(0, ge=0)


# Helper function to convert Decimal to float
def _convert_decimals_to_float(obj):
    """Recursively convert Decimal objects to float."""
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, dict):
        return {k: _convert_decimals_to_float(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_convert_decimals_to_float(item) for item in obj]
    return obj


@router.post("/qsbs-analysis")
async def analyze_qsbs(request: QSBSRequest) -> Dict[str, Any]:
    """
    Analyze Qualified Small Business Stock (Section 1202) for 0% capital gains.

    Returns qualification analysis and tax savings up to $10M+ exclusion.
    """
    try:
        result = QSBSCalculator.calculate_qsbs_benefit(
            acquisition_date=request.acquisition_date,
            sale_date=request.sale_date,
            sale_price=request.sale_price,
            cost_basis=request.cost_basis,
            company_assets_at_issuance=request.company_assets_at_issuance,
            is_qualified_business=request.is_qualified_business,
            acquired_at_original_issue=request.acquired_at_original_issue
        )
        return _convert_decimals_to_float(result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error analyzing QSBS: {str(e)}"
        )


@router.post("/augusta-rule")
async def calculate_augusta_rule(request: AugustaRuleRequest) -> Dict[str, Any]:
    """
    Calculate Augusta Rule (Section 280A) tax-free rental income.

    Rent your home to your business up to 14 days/year tax-free.
    """
    try:
        result = AugustaRuleCalculator.calculate_augusta_rule_benefit(
            rental_days=request.rental_days,
            daily_rate=request.daily_rate,
            comparable_venue_rate=request.comparable_venue_rate,
            business_structure=request.business_structure,
            business_tax_rate=request.business_tax_rate,
            personal_tax_rate=request.personal_tax_rate
        )
        return _convert_decimals_to_float(result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error calculating Augusta Rule: {str(e)}"
        )


@router.post("/reps-qualification")
async def calculate_reps(request: REPSRequest) -> Dict[str, Any]:
    """
    Calculate Real Estate Professional Status (REPS) qualification.

    Unlock unlimited rental losses against W-2 income. Requires 750+ hours.
    """
    try:
        result = REPSCalculator.calculate_reps_qualification(
            real_estate_hours=request.real_estate_hours,
            total_work_hours=request.total_work_hours,
            rental_properties=request.rental_properties,
            rental_losses=request.rental_losses,
            w2_income=request.w2_income,
            make_grouping_election=request.make_grouping_election,
            properties_material_participation=request.properties_material_participation
        )
        return _convert_decimals_to_float(result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error calculating REPS: {str(e)}"
        )


@router.post("/mega-backdoor-roth")
async def calculate_mega_backdoor(request: MegaBackdoorRequest) -> Dict[str, Any]:
    """
    Calculate Mega Backdoor Roth contribution capacity.

    Contribute $46K+ beyond normal 401k limits via after-tax contributions.
    """
    try:
        result = MegaBackdoorRothCalculator.calculate_mega_backdoor_roth(
            age=request.age,
            current_401k_deferrals=request.current_401k_deferrals,
            employer_match=request.employer_match,
            plan_allows_after_tax=request.plan_allows_after_tax,
            plan_allows_in_service_conversion=request.plan_allows_in_service_conversion,
            tax_year=request.tax_year
        )
        return _convert_decimals_to_float(result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error calculating Mega Backdoor Roth: {str(e)}"
        )


@router.post("/cash-balance-plan")
async def calculate_cash_balance(request: CashBalanceRequest) -> Dict[str, Any]:
    """
    Calculate Cash Balance Plan + 401k combination.

    Deduct $300K+ annually for business owners 50+.
    """
    try:
        result = CashBalancePlanCalculator.calculate_cash_balance_plan(
            age=request.age,
            w2_compensation=request.w2_compensation,
            business_net_income=request.business_net_income,
            current_401k_contribution=request.current_401k_contribution,
            employees_count=request.employees_count,
            target_retirement_age=request.target_retirement_age
        )
        return _convert_decimals_to_float(result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error calculating Cash Balance Plan: {str(e)}"
        )


@router.post("/scorp-salary-optimization")
async def optimize_scorp_salary(request: SCorpSalaryRequest) -> Dict[str, Any]:
    """
    Optimize S-Corp salary to minimize payroll taxes while staying reasonable.

    Balance between salary (payroll tax) and distributions (no payroll tax).
    """
    try:
        result = SCorpSalaryOptimizer.calculate_optimal_salary(
            net_business_income=request.net_business_income,
            industry=request.industry,
            years_in_business=request.years_in_business,
            business_duties=request.business_duties,
            geographic_area=request.geographic_area
        )
        return _convert_decimals_to_float(result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error optimizing S-Corp salary: {str(e)}"
        )


@router.post("/grat-analysis")
async def analyze_grat(request: GRATRequest) -> Dict[str, Any]:
    """
    Calculate Grantor Retained Annuity Trust (GRAT) wealth transfer.

    Zeroed-out GRAT: Transfer wealth with minimal/no gift tax.
    """
    try:
        result = EstatePlanningCalculator.calculate_grat(
            asset_value=request.asset_value,
            grat_term_years=request.grat_term_years,
            section_7520_rate=request.section_7520_rate,
            expected_appreciation_rate=request.expected_appreciation_rate,
            annual_annuity_percentage=request.annual_annuity_percentage
        )
        return _convert_decimals_to_float(result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error analyzing GRAT: {str(e)}"
        )


@router.post("/idgt-slat-analysis")
async def analyze_idgt_slat(request: IDGTSLATRequest) -> Dict[str, Any]:
    """
    Calculate IDGT/SLAT wealth transfer before 2026 exemption sunset.

    URGENT: $13.99M exemption sunsets to ~$7M on 1/1/2026.
    """
    try:
        result = EstatePlanningCalculator.calculate_idgt_slat(
            asset_value=request.asset_value,
            gift_tax_exemption_used=request.gift_tax_exemption_used,
            trust_term_years=request.trust_term_years,
            expected_appreciation_rate=request.expected_appreciation_rate,
            grantor_pays_income_tax=request.grantor_pays_income_tax
        )
        return _convert_decimals_to_float(result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error analyzing IDGT/SLAT: {str(e)}"
        )


@router.post("/tax-loss-harvesting")
async def calculate_tax_loss_harvesting(request: TaxLossHarvestingRequest) -> Dict[str, Any]:
    """
    Calculate tax loss harvesting benefits and wash sale rule compliance.

    Harvest investment losses to offset gains. Crypto has no wash sale rules.
    """
    try:
        result = TaxLossHarvestingCalculator.calculate_tax_loss_harvesting(
            capital_gains_realized=request.capital_gains_realized,
            available_losses=request.available_losses,
            ordinary_income=request.ordinary_income,
            holding_period=request.holding_period,
            has_carryforward_losses=request.has_carryforward_losses
        )
        return _convert_decimals_to_float(result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error calculating tax loss harvesting: {str(e)}"
        )
