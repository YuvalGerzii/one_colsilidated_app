"""
Gig Economy & Hybrid Labor Integration API Endpoints

Provides REST API for gig matching, income stabilization, benefits calculation,
and hybrid work optimization.
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from app.models.gig_economy import GigEconomyEngine, GigBenefitsCalculator, HybridWorkOptimizer

router = APIRouter()

# Initialize engines
gig_engine = GigEconomyEngine()
benefits_calculator = GigBenefitsCalculator()
hybrid_optimizer = HybridWorkOptimizer()


# ============================================================================
# Request/Response Models
# ============================================================================

class SkillMatchRequest(BaseModel):
    """Request for matching skills to gig opportunities"""
    worker_skills: List[str] = Field(..., description="List of worker skills")
    availability_hours_weekly: int = Field(..., description="Hours available per week", ge=5, le=80)
    income_target_monthly: float = Field(..., description="Target monthly income", ge=0)
    preferences: Optional[Dict] = Field(default=None, description="Optional preferences (remote_only, etc.)")


class IncomeSource(BaseModel):
    """Income source for stabilization planning"""
    name: str
    monthly_avg: float = Field(..., ge=0)
    volatility: str = Field(..., description="low, medium, or high")


class IncomeStabilizationRequest(BaseModel):
    """Request for income stabilization plan"""
    current_income_sources: List[IncomeSource]
    monthly_expenses: float = Field(..., ge=0)
    emergency_fund_months: int = Field(default=6, ge=3, le=12)
    risk_tolerance: str = Field(default="moderate", description="low, moderate, or high")


class CurrentGig(BaseModel):
    """Current gig engagement"""
    name: str
    platform: str
    hours_per_month: float = Field(..., ge=0)
    income_per_month: float = Field(..., ge=0)


class PortfolioOptimizationRequest(BaseModel):
    """Request for gig portfolio optimization"""
    worker_id: int
    current_gigs: List[CurrentGig]
    available_hours_weekly: int = Field(..., ge=5, le=80)
    target_monthly_income: float = Field(..., ge=0)


class BenefitsCalculationRequest(BaseModel):
    """Request for benefits calculation"""
    annual_gig_income: float = Field(..., ge=0)
    state: str = Field(default="CA", description="State for tax calculations")
    age: int = Field(..., ge=18, le=100)
    dependents: int = Field(default=0, ge=0, le=10)
    retirement_contribution_pct: float = Field(default=10.0, ge=0, le=100)


class W2Job(BaseModel):
    """W2 job details for hybrid optimization"""
    hours_per_week: int = Field(..., ge=0, le=80)
    monthly_income: float = Field(..., ge=0)
    flexibility: str = Field(default="low", description="low, medium, or high")


class GigOpportunity(BaseModel):
    """Gig opportunity for hybrid optimization"""
    name: str
    hours_per_week: float = Field(..., ge=0)
    weekly_income: float = Field(..., ge=0)
    hourly_rate: float = Field(..., ge=0)
    flexibility_score: int = Field(default=50, ge=0, le=100)
    skill_value: int = Field(default=50, ge=0, le=100)


class HybridScheduleRequest(BaseModel):
    """Request for hybrid schedule optimization"""
    w2_job: W2Job
    gig_opportunities: List[GigOpportunity]
    weekly_hours_available: int = Field(..., ge=20, le=100)
    optimization_goal: str = Field(default="max_income", description="max_income, work_life_balance, or skill_building")


# ============================================================================
# Endpoints
# ============================================================================

@router.post("/match-skills-to-gigs")
def match_skills_to_gigs(request: SkillMatchRequest):
    """
    Match worker skills to gig opportunities across multiple platforms.

    Returns matched opportunities with earning potential, platform recommendations,
    and income optimization strategy.
    """
    try:
        result = gig_engine.match_skills_to_gigs(
            worker_skills=request.worker_skills,
            availability_hours_weekly=request.availability_hours_weekly,
            income_target_monthly=request.income_target_monthly,
            preferences=request.preferences
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/income-stabilization-plan")
def create_income_stabilization_plan(request: IncomeStabilizationRequest):
    """
    Create income stabilization plan for gig workers with multiple income streams.

    Analyzes income diversification, volatility, and provides recommendations
    for building stable income with emergency fund targets.
    """
    try:
        # Convert Pydantic models to dicts for engine
        income_sources = [source.dict() for source in request.current_income_sources]

        result = gig_engine.calculate_income_stabilization_plan(
            current_income_sources=income_sources,
            monthly_expenses=request.monthly_expenses,
            emergency_fund_months=request.emergency_fund_months,
            risk_tolerance=request.risk_tolerance
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/portfolio-optimization")
def optimize_gig_portfolio(request: PortfolioOptimizationRequest):
    """
    Analyze current gig portfolio and suggest optimizations.

    Identifies low-performing gigs, unused hours, and provides action plan
    for maximizing income with available time.
    """
    try:
        # Convert Pydantic models to dicts
        current_gigs = [gig.dict() for gig in request.current_gigs]

        result = gig_engine.optimize_gig_portfolio(
            worker_id=request.worker_id,
            current_gigs=current_gigs,
            available_hours_weekly=request.available_hours_weekly,
            target_monthly_income=request.target_monthly_income
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/benefits-calculator")
def calculate_benefits_package(request: BenefitsCalculationRequest):
    """
    Calculate comprehensive benefits package costs for gig workers.

    Includes health insurance, retirement, taxes, disability/life insurance.
    Provides W2 equivalent salary comparison and recommendations.
    """
    try:
        result = benefits_calculator.calculate_benefits_package(
            annual_gig_income=request.annual_gig_income,
            state=request.state,
            age=request.age,
            dependents=request.dependents,
            retirement_contribution_pct=request.retirement_contribution_pct
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/hybrid-schedule-optimizer")
def optimize_hybrid_schedule(request: HybridScheduleRequest):
    """
    Optimize work schedule combining W2 and gig work.

    Balances income goals with burnout risk, provides sustainability scoring,
    and recommends optimal gig selection based on optimization goal.
    """
    try:
        # Convert Pydantic models to dicts
        w2_job = request.w2_job.dict()
        gig_opportunities = [gig.dict() for gig in request.gig_opportunities]

        result = hybrid_optimizer.optimize_hybrid_schedule(
            w2_job=w2_job,
            gig_opportunities=gig_opportunities,
            weekly_hours_available=request.weekly_hours_available,
            optimization_goal=request.optimization_goal
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/gig-platforms")
def get_gig_platforms():
    """
    Get list of supported gig platforms with details.

    Returns platform information including categories, fees, and volume.
    """
    return {
        "platforms": gig_engine.gig_platforms,
        "total_platforms": len(gig_engine.gig_platforms),
        "categories": list(set(p["category"] for p in gig_engine.gig_platforms.values()))
    }


@router.get("/skill-gig-mapping")
def get_skill_gig_mapping():
    """
    Get mapping of skills to gig platforms.

    Returns which platforms are best for each skill.
    """
    return {
        "skill_mappings": gig_engine.skill_gig_map,
        "total_skills": len(gig_engine.skill_gig_map)
    }


@router.get("/dashboard/{worker_id}")
def get_gig_dashboard(worker_id: int):
    """
    Get comprehensive gig economy dashboard for a worker.

    Aggregates key metrics, recommendations, and quick actions.
    """
    # In production, fetch from database
    # For demo, return sample dashboard

    return {
        "worker_id": worker_id,
        "gig_summary": {
            "active_platforms": 3,
            "active_gigs": 5,
            "monthly_income": 3250.00,
            "hours_per_month": 80,
            "average_hourly_rate": 40.63
        },
        "income_streams": [
            {"source": "Upwork - Web Development", "monthly": 1500, "volatility": "medium"},
            {"source": "Fiverr - Graphic Design", "monthly": 950, "volatility": "high"},
            {"source": "Part-time W2", "monthly": 800, "volatility": "low"}
        ],
        "stability_metrics": {
            "diversification_score": 68,
            "income_stability_score": 72,
            "burnout_risk": "moderate"
        },
        "quick_actions": [
            "Review 2 low-performing gigs",
            "Apply to Toptal for higher rates",
            "Set up Solo 401(k)",
            "Calculate quarterly taxes"
        ],
        "next_steps": [
            "Optimize portfolio to hit $4000/month target",
            "Add retainer client for stable base income",
            "Increase hourly rate on top platform by 20%"
        ]
    }


@router.post("/compare-gig-vs-w2")
def compare_gig_vs_w2(
    gig_annual_income: float = Query(..., ge=0),
    w2_annual_salary: float = Query(..., ge=0),
    age: int = Query(..., ge=18, le=100),
    state: str = Query(default="CA")
):
    """
    Compare total compensation between gig work and W2 employment.

    Accounts for benefits, taxes, and provides comprehensive comparison.
    """
    try:
        # Calculate gig total cost
        gig_benefits = benefits_calculator.calculate_benefits_package(
            annual_gig_income=gig_annual_income,
            state=state,
            age=age,
            dependents=0,
            retirement_contribution_pct=10.0
        )

        # Simplified W2 calculation (employer pays ~30% benefits)
        w2_employer_benefits = w2_annual_salary * 0.30
        w2_total_compensation = w2_annual_salary + w2_employer_benefits

        # W2 taxes (simplified - just income tax, not SE tax)
        w2_federal_tax = gig_benefits["taxes"]["federal_income_tax"] * 0.85  # Roughly less than gig
        w2_fica = w2_annual_salary * 0.0765
        w2_state_tax = gig_benefits["taxes"]["state_income_tax"]
        w2_total_tax = w2_federal_tax + w2_fica + w2_state_tax

        w2_net = w2_annual_salary - w2_total_tax
        gig_net = gig_benefits["summary"]["net_annual_income"]

        return {
            "gig_work": {
                "gross_income": gig_annual_income,
                "total_taxes": gig_benefits["summary"]["total_taxes"],
                "benefits_cost": gig_benefits["summary"]["total_benefits_cost"],
                "net_income": gig_net,
                "effective_hourly_rate": gig_benefits["summary"]["effective_hourly_rate"]
            },
            "w2_employment": {
                "salary": w2_annual_salary,
                "employer_benefits_value": round(w2_employer_benefits, 2),
                "total_compensation": round(w2_total_compensation, 2),
                "total_taxes": round(w2_total_tax, 2),
                "net_income": round(w2_net, 2),
                "effective_hourly_rate": round(w2_net / 2080, 2)
            },
            "comparison": {
                "net_income_difference": round(gig_net - w2_net, 2),
                "gig_premium_required_pct": round((gig_annual_income - w2_annual_salary) / w2_annual_salary * 100, 1),
                "recommendation": "Gig work is better" if gig_net > w2_net else "W2 is better" if w2_net > gig_net else "Roughly equivalent",
                "analysis": self._generate_comparison_analysis(gig_net, w2_net, gig_annual_income, w2_annual_salary)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def _generate_comparison_analysis(gig_net: float, w2_net: float, gig_gross: float, w2_gross: float) -> str:
    """Generate comparison analysis text"""
    diff = gig_net - w2_net
    diff_pct = abs(diff) / w2_net * 100 if w2_net > 0 else 0

    if abs(diff) < 5000:
        return f"Net income is roughly equivalent (within ${abs(diff):,.0f}). Consider non-financial factors like flexibility, benefits, job security."
    elif gig_net > w2_net:
        return f"Gig work provides ${diff:,.0f} ({diff_pct:.1f}%) more in net income, but requires self-management of benefits and irregular income."
    else:
        return f"W2 employment provides ${abs(diff):,.0f} ({diff_pct:.1f}%) more in net income, plus job security and employer-managed benefits."


@router.post("/income-gap-analysis")
def analyze_income_gap(
    current_monthly_income: float = Query(..., ge=0),
    target_monthly_income: float = Query(..., ge=0),
    current_hours_weekly: int = Query(..., ge=0, le=80),
    max_hours_weekly: int = Query(..., ge=0, le=100)
):
    """
    Analyze gap between current and target income, suggest strategies to close it.

    Provides specific recommendations for increasing income through gigs.
    """
    gap = target_monthly_income - current_monthly_income
    gap_pct = gap / current_monthly_income * 100 if current_monthly_income > 0 else float('inf')

    available_hours = max_hours_weekly - current_hours_weekly
    current_hourly = (current_monthly_income / (current_hours_weekly * 4.33)) if current_hours_weekly > 0 else 0

    # Strategies to close gap
    strategies = []

    # Strategy 1: Increase hours at current rate
    if available_hours > 0:
        hours_needed = gap / current_hourly if current_hourly > 0 else 0
        monthly_hours_needed = hours_needed
        weekly_hours_needed = monthly_hours_needed / 4.33

        if weekly_hours_needed <= available_hours:
            strategies.append({
                "strategy": "Add gig hours at current hourly rate",
                "hours_to_add_weekly": round(weekly_hours_needed, 1),
                "feasibility": "achievable",
                "timeline": "immediate"
            })

    # Strategy 2: Increase hourly rate
    target_hourly = (target_monthly_income / (current_hours_weekly * 4.33)) if current_hours_weekly > 0 else 0
    rate_increase_needed = target_hourly - current_hourly
    rate_increase_pct = (rate_increase_needed / current_hourly * 100) if current_hourly > 0 else 0

    if rate_increase_pct > 0 and rate_increase_pct < 50:
        strategies.append({
            "strategy": "Increase hourly rate through upskilling or negotiation",
            "rate_increase_needed": round(rate_increase_needed, 2),
            "rate_increase_pct": round(rate_increase_pct, 1),
            "feasibility": "achievable" if rate_increase_pct < 30 else "challenging",
            "timeline": "3-6 months"
        })

    # Strategy 3: Combination approach
    if available_hours > 5:
        # Add some hours + modest rate increase
        combo_hours_add = min(available_hours, 15)
        combo_hours_total = current_hours_weekly + combo_hours_add
        combo_hourly_needed = target_monthly_income / (combo_hours_total * 4.33)
        combo_rate_increase = combo_hourly_needed - current_hourly
        combo_rate_increase_pct = (combo_rate_increase / current_hourly * 100) if current_hourly > 0 else 0

        if combo_rate_increase_pct > 0 and combo_rate_increase_pct < 30:
            strategies.append({
                "strategy": "Combination: Add hours + modest rate increase",
                "hours_to_add_weekly": combo_hours_add,
                "rate_increase_pct": round(combo_rate_increase_pct, 1),
                "feasibility": "achievable",
                "timeline": "1-3 months"
            })

    return {
        "gap_analysis": {
            "current_monthly_income": current_monthly_income,
            "target_monthly_income": target_monthly_income,
            "income_gap": round(gap, 2),
            "gap_percentage": round(gap_pct, 1),
            "current_hourly_rate": round(current_hourly, 2),
            "available_hours_weekly": available_hours
        },
        "strategies_to_close_gap": strategies,
        "recommendations": [
            "Focus on high-value skills that command $50+/hr rates" if current_hourly < 50 else "Maintain premium positioning",
            "Build portfolio of work to justify rate increases",
            "Diversify income streams to reduce dependency on single source",
            "Consider passive income streams (courses, templates, affiliate) to scale beyond hours"
        ],
        "feasibility_assessment": "achievable" if gap_pct < 50 else "challenging" if gap_pct < 100 else "requires_major_changes"
    }
