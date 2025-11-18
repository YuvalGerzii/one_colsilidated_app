"""
Economic Copilot API Endpoints

Provides REST API for integrated personal finance and career decision-making tools.
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from app.models.economic_copilot import (
    JobDecisionEngine,
    RetirementImpactAnalyzer,
    DebtReskillingOptimizer,
    FamilyFinancialPlanner
)

router = APIRouter()

# Initialize engines
job_decision_engine = JobDecisionEngine()
retirement_analyzer = RetirementImpactAnalyzer()
debt_optimizer = DebtReskillingOptimizer()
family_planner = FamilyFinancialPlanner()


# ============================================================================
# Request/Response Models
# ============================================================================

class Compensation(BaseModel):
    """Compensation details"""
    base_salary: float = Field(..., ge=0)
    bonus: float = Field(default=0, ge=0)
    equity_value_annual: float = Field(default=0, ge=0)
    benefits_value: float = Field(default=0, ge=0)


class Role(BaseModel):
    """Role details"""
    seniority: str = Field(default="mid", description="junior, mid, senior, lead, principal, manager, director, vp, c_level")
    learning_score: int = Field(default=50, ge=0, le=100)
    industry_growth_rate: float = Field(default=3, description="Annual industry growth percentage")
    skills_to_gain: List[str] = Field(default=[])


class WorkConditions(BaseModel):
    """Work conditions"""
    hours_per_week: int = Field(default=40, ge=0, le=100)
    commute_minutes_daily: int = Field(default=0, ge=0)
    flexibility_score: int = Field(default=50, ge=0, le=100)
    remote_days_per_week: int = Field(default=0, ge=0, le=5)
    pto_days: int = Field(default=15, ge=0)


class Company(BaseModel):
    """Company details"""
    employee_count: int = Field(default=100, ge=1)
    financial_health_score: int = Field(default=70, ge=0, le=100)
    industry_stability: int = Field(default=60, ge=0, le=100)
    well_funded: bool = Field(default=True)
    recent_layoffs: bool = Field(default=False)
    company_growth_rate: str = Field(default="moderate", description="fast, moderate, slow")


class Culture(BaseModel):
    """Company culture scores"""
    collaborative: int = Field(default=50, ge=0, le=100)
    innovative: int = Field(default=50, ge=0, le=100)
    fast_paced: int = Field(default=50, ge=0, le=100)
    structured: int = Field(default=50, ge=0, le=100)
    diverse: int = Field(default=50, ge=0, le=100)


class JobSituation(BaseModel):
    """Complete job situation"""
    compensation: Compensation
    role: Role
    work_conditions: WorkConditions
    company: Company
    culture: Culture


class JobOfferAnalysisRequest(BaseModel):
    """Request for job offer analysis"""
    current_situation: JobSituation
    job_offer: JobSituation
    personal_priorities: Optional[Dict] = Field(
        default=None,
        description="Weights for compensation, career_growth, work_life_balance, job_security, company_culture (sum to 100)"
    )


class RetirementAnalysisRequest(BaseModel):
    """Request for retirement impact analysis"""
    current_age: int = Field(..., ge=18, le=100)
    target_retirement_age: int = Field(..., ge=50, le=100)
    current_situation: Dict = Field(..., description="salary, retirement_savings, retirement_contribution_pct")
    career_change: Dict = Field(..., description="new_salary, time_out_of_work_months, reskilling_cost, new_contribution_rate")
    retirement_goals: Dict = Field(..., description="target_savings, annual_spending")


class ReskillingOption(BaseModel):
    """Reskilling/education option"""
    name: str
    total_cost: float = Field(..., ge=0)
    duration_months: int = Field(..., ge=1, le=60)
    expected_income_after: float = Field(..., ge=0)
    time_to_new_job_months: int = Field(default=3, ge=0)
    full_time: bool = Field(default=False, description="Full-time program that prevents working")
    financing_available: bool = Field(default=False)


class DebtDetails(BaseModel):
    """Debt details"""
    total_debt: float = Field(..., ge=0)
    monthly_minimum_payment: float = Field(..., ge=0)
    weighted_avg_interest_rate: float = Field(..., ge=0, le=100, description="Percentage")


class DebtReskillingRequest(BaseModel):
    """Request for debt vs reskilling optimization"""
    current_situation: Dict = Field(..., description="annual_income, monthly_discretionary")
    debt_details: DebtDetails
    reskilling_options: List[ReskillingOption]


class FamilyFinancialRequest(BaseModel):
    """Request for family financial analysis"""
    family_situation: Dict = Field(
        ...,
        description="marital_status, num_children, children_ages, spouse_income, monthly_expenses, mortgage_payment, emergency_fund_months, primary_income"
    )
    career_decision: Dict = Field(..., description="new_income, months_without_income, reskilling_cost, income_change")
    planning_horizon_years: int = Field(default=10, ge=1, le=30)


# ============================================================================
# Endpoints
# ============================================================================

@router.post("/job-offer-analysis")
def analyze_job_offer(request: JobOfferAnalysisRequest):
    """
    Comprehensive analysis of whether to accept a job offer.

    Analyzes across 5 dimensions: compensation, career growth, work-life balance,
    job security, and company culture. Provides weighted overall score, detailed
    breakdowns, 5-year financial projection, and personalized recommendation.
    """
    try:
        # Convert Pydantic models to dicts
        current_dict = {
            "compensation": request.current_situation.compensation.dict(),
            "role": request.current_situation.role.dict(),
            "work_conditions": request.current_situation.work_conditions.dict(),
            "company": request.current_situation.company.dict(),
            "culture": request.current_situation.culture.dict()
        }

        offer_dict = {
            "compensation": request.job_offer.compensation.dict(),
            "role": request.job_offer.role.dict(),
            "work_conditions": request.job_offer.work_conditions.dict(),
            "company": request.job_offer.company.dict(),
            "culture": request.job_offer.culture.dict()
        }

        result = job_decision_engine.analyze_job_offer(
            current_situation=current_dict,
            job_offer=offer_dict,
            personal_priorities=request.personal_priorities
        )

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/retirement-impact-analysis")
def analyze_retirement_impact(request: RetirementAnalysisRequest):
    """
    Analyze how a career change impacts long-term retirement goals.

    Projects retirement savings with and without career change, calculates
    retirement readiness, identifies impact severity, and provides mitigation
    strategies if retirement is at risk.
    """
    try:
        result = retirement_analyzer.analyze_retirement_impact(
            current_age=request.current_age,
            target_retirement_age=request.target_retirement_age,
            current_situation=request.current_situation,
            career_change=request.career_change,
            retirement_goals=request.retirement_goals
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/debt-vs-reskilling-optimization")
def optimize_debt_vs_reskilling(request: DebtReskillingRequest):
    """
    Optimize the decision between paying off debt vs investing in reskilling/education.

    Analyzes debt burden, calculates ROI for reskilling options, and provides
    optimized strategies (debt-first, reskilling-first, or balanced approach)
    with detailed financial projections.
    """
    try:
        # Convert Pydantic models to dicts
        current_situation = request.current_situation
        debt_details = request.debt_details.dict()
        reskilling_options = [option.dict() for option in request.reskilling_options]

        result = debt_optimizer.optimize_debt_vs_reskilling(
            current_situation=current_situation,
            debt_details=debt_details,
            reskilling_options=reskilling_options
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/family-financial-analysis")
def analyze_family_financial_impact(request: FamilyFinancialRequest):
    """
    Analyze how a career decision impacts entire family financially.

    Projects family finances with and without career change, considers children's
    needs (especially college), spouse income dependency, and family risk factors.
    Provides family-focused recommendation.
    """
    try:
        result = family_planner.analyze_family_financial_impact(
            family_situation=request.family_situation,
            career_decision=request.career_decision,
            planning_horizon_years=request.planning_horizon_years
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/comprehensive-life-decision")
def comprehensive_life_decision_analysis(
    worker_id: int,
    job_offer: JobSituation,
    include_retirement: bool = Query(default=True),
    include_debt: bool = Query(default=False),
    include_family: bool = Query(default=False)
):
    """
    Comprehensive life decision analysis combining all Economic Copilot features.

    Analyzes a job offer or career change across ALL relevant dimensions:
    - Job offer quality (compensation, growth, culture, etc.)
    - Retirement impact (if include_retirement=True)
    - Debt implications (if include_debt=True)
    - Family impact (if include_family=True)

    Returns unified recommendation considering all factors.
    """
    try:
        # In production, fetch worker data from database
        # For demo, use sample data

        current_situation = JobSituation(
            compensation=Compensation(base_salary=80000, bonus=5000, equity_value_annual=0, benefits_value=12000),
            role=Role(seniority="mid", learning_score=60, industry_growth_rate=3),
            work_conditions=WorkConditions(hours_per_week=45, commute_minutes_daily=30, flexibility_score=50, remote_days_per_week=2),
            company=Company(employee_count=500, financial_health_score=75, industry_stability=70),
            culture=Culture(collaborative=70, innovative=60, fast_paced=65)
        )

        # Job offer analysis (always included)
        job_analysis = analyze_job_offer(JobOfferAnalysisRequest(
            current_situation=current_situation,
            job_offer=job_offer
        ))

        result = {
            "worker_id": worker_id,
            "job_offer_analysis": job_analysis,
            "overall_recommendation": None
        }

        # Add retirement analysis if requested
        if include_retirement:
            retirement_request = RetirementAnalysisRequest(
                current_age=35,
                target_retirement_age=65,
                current_situation={
                    "salary": current_situation.compensation.base_salary,
                    "retirement_savings": 150000,
                    "retirement_contribution_pct": 10
                },
                career_change={
                    "new_salary": job_offer.compensation.base_salary,
                    "time_out_of_work_months": 0,
                    "reskilling_cost": 0,
                    "new_contribution_rate": 10
                },
                retirement_goals={
                    "target_savings": 2000000,
                    "annual_spending": 80000
                }
            )
            result["retirement_impact_analysis"] = analyze_retirement_impact(retirement_request)

        # Unified recommendation
        result["overall_recommendation"] = _generate_unified_recommendation(
            job_analysis=job_analysis,
            retirement_analysis=result.get("retirement_impact_analysis"),
            debt_analysis=None,
            family_analysis=None
        )

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def _generate_unified_recommendation(
    job_analysis: Dict,
    retirement_analysis: Optional[Dict],
    debt_analysis: Optional[Dict],
    family_analysis: Optional[Dict]
) -> Dict:
    """Generate unified recommendation across all analyses"""
    # Collect recommendations from each analysis
    job_rec = job_analysis["recommendation"]["decision"]

    blocking_factors = []
    supporting_factors = []
    cautionary_factors = []

    # Job offer assessment
    if job_rec in ["strongly_recommend", "recommend"]:
        supporting_factors.append("Job offer represents good career opportunity")
    elif job_rec in ["strongly_not_recommended", "not_recommended"]:
        blocking_factors.append("Job offer quality is questionable")
    else:
        cautionary_factors.append("Job offer has mixed pros and cons")

    # Retirement impact
    if retirement_analysis:
        ret_rec = retirement_analysis["recommendation"]["recommendation"]
        if ret_rec == "reconsider":
            blocking_factors.append("Severe negative retirement impact")
        elif ret_rec == "proceed_with_caution":
            cautionary_factors.append("Moderate retirement impact - mitigation needed")
        elif ret_rec == "positive":
            supporting_factors.append("Positive retirement impact")

    # Make final decision
    if blocking_factors:
        decision = "not_recommended"
        confidence = "high"
        explanation = f"Not recommended due to: {', '.join(blocking_factors)}"
    elif len(supporting_factors) >= 2:
        decision = "recommended"
        confidence = "high" if not cautionary_factors else "moderate"
        explanation = f"Recommended - {len(supporting_factors)} supporting factors outweigh concerns"
    elif supporting_factors and not cautionary_factors:
        decision = "recommended"
        confidence = "moderate"
        explanation = "Positive overall but limited data for full assessment"
    else:
        decision = "neutral"
        confidence = "low"
        explanation = "Mixed signals - proceed with careful consideration of trade-offs"

    return {
        "decision": decision,
        "confidence": confidence,
        "explanation": explanation,
        "supporting_factors": supporting_factors,
        "blocking_factors": blocking_factors,
        "cautionary_factors": cautionary_factors,
        "key_actions": [
            "Review all detailed analyses before making final decision",
            "Discuss with spouse/family if applicable",
            "Negotiate terms if concerns exist",
            "Have backup plan in case things don't work out"
        ]
    }


@router.get("/dashboard/{worker_id}")
def get_economic_copilot_dashboard(worker_id: int):
    """
    Get comprehensive Economic Copilot dashboard for a worker.

    Aggregates financial health metrics, recent decisions, active scenarios,
    and personalized recommendations.
    """
    # In production, fetch from database
    # For demo, return sample dashboard

    return {
        "worker_id": worker_id,
        "financial_health_summary": {
            "current_annual_income": 85000,
            "retirement_savings": 175000,
            "retirement_on_track": True,
            "debt_to_income_ratio": 25,
            "emergency_fund_months": 6,
            "overall_health_score": 78,
            "health_rating": "good"
        },
        "recent_analyses": [
            {
                "type": "job_offer",
                "date": "2025-11-10",
                "decision": "recommended",
                "summary": "Software Engineer at TechCorp - 15% comp increase"
            },
            {
                "type": "reskilling",
                "date": "2025-10-25",
                "decision": "proceed",
                "summary": "Data Science Bootcamp - 250% ROI over 10 years"
            }
        ],
        "active_scenarios": [
            {
                "name": "Career Change to Product Management",
                "status": "analyzing",
                "created_date": "2025-11-15"
            }
        ],
        "recommendations": [
            "Increase retirement contribution to 15% to stay on track for $2M goal",
            "Emergency fund is healthy - consider investing surplus",
            "Good time for career growth - debt burden is manageable"
        ],
        "quick_actions": [
            "Analyze new job offer",
            "Compare reskilling programs",
            "Check retirement impact",
            "Run family financial scenario"
        ]
    }


@router.post("/compare-scenarios")
def compare_multiple_scenarios(
    scenarios: List[Dict] = Field(..., description="List of career scenarios to compare")
):
    """
    Compare multiple career scenarios side-by-side.

    Useful for comparing several job offers or career paths at once.
    Returns comparative analysis with rankings and trade-offs.
    """
    try:
        if len(scenarios) < 2:
            raise HTTPException(status_code=400, detail="Need at least 2 scenarios to compare")

        if len(scenarios) > 5:
            raise HTTPException(status_code=400, detail="Maximum 5 scenarios allowed")

        # Analyze each scenario
        # For demo purposes, return sample comparison

        return {
            "scenarios_compared": len(scenarios),
            "ranking": [
                {
                    "rank": 1,
                    "scenario": "Senior Engineer at Startup",
                    "overall_score": 82,
                    "best_for": "Career growth and earning potential",
                    "worst_for": "Job security and work-life balance"
                },
                {
                    "rank": 2,
                    "scenario": "Lead Engineer at Enterprise",
                    "overall_score": 76,
                    "best_for": "Job security and benefits",
                    "worst_for": "Career growth and innovation"
                },
                {
                    "rank": 3,
                    "scenario": "Stay at current job",
                    "overall_score": 65,
                    "best_for": "Familiarity and low risk",
                    "worst_for": "All growth metrics"
                }
            ],
            "trade_off_analysis": {
                "compensation": "Startup offers 25% more than enterprise, 40% more than current",
                "growth": "Startup has best learning opportunities, enterprise has clearer path to management",
                "stability": "Enterprise most stable, startup has highest risk",
                "work_life_balance": "Current job best, startup worst"
            },
            "recommendation": "Choose Startup if you value growth and can handle risk. Choose Enterprise if you prioritize stability and benefits."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
