"""
Labor Market Data Products

High-value data products from the Labor platform:
- Skill Demand Forecasts: Predict in-demand skills
- Salary Intelligence: Compensation benchmarking
- Workforce Analytics: Hiring trends and talent flow

Revenue Potential: $15M ARR
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class SkillCategory(Enum):
    TECHNICAL = "technical"
    BUSINESS = "business"
    CREATIVE = "creative"
    LEADERSHIP = "leadership"
    DATA = "data"
    CLOUD = "cloud"
    SECURITY = "security"


class IndustryType(Enum):
    TECHNOLOGY = "technology"
    FINANCE = "finance"
    HEALTHCARE = "healthcare"
    MANUFACTURING = "manufacturing"
    RETAIL = "retail"
    CONSULTING = "consulting"


@dataclass
class SkillForecast:
    """Skill demand forecast"""
    skill_name: str
    category: SkillCategory
    timestamp: datetime

    # Current metrics
    current_demand: int  # Job postings
    current_supply: int  # Professionals with skill
    supply_demand_ratio: float

    # Forecasts
    demand_growth_12m: float
    demand_growth_36m: float

    # Compensation
    salary_premium: float  # % above base
    avg_salary: float

    # Related skills
    complementary_skills: List[str]
    emerging_variants: List[str]

    # Confidence
    confidence: float


@dataclass
class SalaryBenchmark:
    """Salary benchmark data"""
    role: str
    location: str
    experience_level: str
    timestamp: datetime

    # Salary data
    percentile_25: float
    percentile_50: float
    percentile_75: float
    percentile_90: float

    # Components
    base_salary: float
    total_comp: float
    bonus_pct: float
    equity_value: float

    # Factors
    industry_premium: Dict[str, float]
    company_size_premium: Dict[str, float]
    remote_adjustment: float

    # Trends
    yoy_change: float
    market_trend: str


@dataclass
class WorkforceInsight:
    """Workforce analytics insight"""
    insight_id: str
    timestamp: datetime
    insight_type: str

    # Content
    title: str
    description: str
    data_points: Dict[str, Any]

    # Impact
    affected_roles: List[str]
    affected_industries: List[str]

    # Recommendations
    actions: List[str]
    confidence: float


class SkillDemandForecastsAPI:
    """
    API for skill demand predictions.

    Features:
    - 12-36 month demand forecasts
    - Supply/demand ratios
    - Salary premiums
    - Learning path recommendations

    Pricing:
    - Starter: 50 queries/month, $99/mo
    - Professional: 500 queries/month, $499/mo
    - Enterprise: Unlimited + custom models, $2,499/mo
    """

    def __init__(self):
        self.forecasts: Dict[str, SkillForecast] = {}

    async def get_skill_forecast(
        self,
        skill: str,
        category: Optional[SkillCategory] = None
    ) -> SkillForecast:
        """Get demand forecast for a skill"""

        # Simulated forecast data
        forecast = SkillForecast(
            skill_name=skill,
            category=category or SkillCategory.TECHNICAL,
            timestamp=datetime.now(),
            current_demand=15000,  # Job postings
            current_supply=8000,   # Available professionals
            supply_demand_ratio=0.53,
            demand_growth_12m=0.25,
            demand_growth_36m=0.85,
            salary_premium=0.18,
            avg_salary=145000,
            complementary_skills=[
                "Python", "Cloud Architecture", "Data Engineering"
            ],
            emerging_variants=[
                f"{skill} for LLMs",
                f"Applied {skill}"
            ],
            confidence=0.82
        )

        self.forecasts[skill.lower()] = forecast
        return forecast

    async def get_trending_skills(
        self,
        category: Optional[SkillCategory] = None,
        limit: int = 20
    ) -> List[SkillForecast]:
        """Get trending skills by demand growth"""

        # Simulated trending skills
        trending = [
            ("Machine Learning", SkillCategory.DATA, 0.35),
            ("Kubernetes", SkillCategory.CLOUD, 0.30),
            ("Rust", SkillCategory.TECHNICAL, 0.28),
            ("LLM Engineering", SkillCategory.DATA, 0.45),
            ("Zero Trust Security", SkillCategory.SECURITY, 0.25),
            ("Product Management", SkillCategory.BUSINESS, 0.20),
            ("Data Engineering", SkillCategory.DATA, 0.32),
            ("React Native", SkillCategory.TECHNICAL, 0.18),
            ("Terraform", SkillCategory.CLOUD, 0.22),
            ("GraphQL", SkillCategory.TECHNICAL, 0.15)
        ]

        results = []
        for skill, cat, growth in trending:
            if category and cat != category:
                continue

            forecast = await self.get_skill_forecast(skill, cat)
            forecast.demand_growth_12m = growth
            results.append(forecast)

            if len(results) >= limit:
                break

        return results

    async def get_skill_gaps(
        self,
        current_skills: List[str],
        target_role: str
    ) -> Dict[str, Any]:
        """Identify skill gaps for a target role"""

        # Simulated gap analysis
        role_requirements = {
            "data_scientist": ["Python", "ML", "Statistics", "SQL", "Visualization"],
            "devops_engineer": ["Kubernetes", "CI/CD", "Terraform", "Linux", "Python"],
            "product_manager": ["Strategy", "Analytics", "Communication", "Agile", "SQL"]
        }

        required = role_requirements.get(target_role.lower().replace(" ", "_"), [])
        current_lower = [s.lower() for s in current_skills]

        gaps = [s for s in required if s.lower() not in current_lower]

        return {
            "target_role": target_role,
            "required_skills": required,
            "current_skills": current_skills,
            "gaps": gaps,
            "gap_count": len(gaps),
            "readiness_score": (len(required) - len(gaps)) / len(required) if required else 1.0,
            "recommended_learning_path": [
                {
                    "skill": gap,
                    "priority": "high" if i < 2 else "medium",
                    "estimated_time_weeks": 4 + (i * 2)
                }
                for i, gap in enumerate(gaps)
            ]
        }


class SalaryIntelligenceAPI:
    """
    API for compensation benchmarking.

    Features:
    - Role-specific salary data
    - Location adjustments
    - Total compensation breakdown
    - Industry premiums

    Pricing:
    - Professional: $299/mo
    - Enterprise: $1,499/mo with API access
    """

    def __init__(self):
        self.benchmarks: List[SalaryBenchmark] = []

    async def get_salary_benchmark(
        self,
        role: str,
        location: str = "United States",
        experience_years: int = 5,
        industry: Optional[str] = None
    ) -> SalaryBenchmark:
        """Get salary benchmark for a role"""

        # Base salaries by experience
        base_by_experience = {
            1: 75000,
            3: 95000,
            5: 125000,
            7: 150000,
            10: 180000
        }

        # Get closest experience level
        closest_exp = min(base_by_experience.keys(),
                         key=lambda x: abs(x - experience_years))
        base = base_by_experience[closest_exp]

        # Role multiplier
        role_multipliers = {
            "software engineer": 1.0,
            "data scientist": 1.1,
            "product manager": 1.05,
            "engineering manager": 1.3,
            "devops engineer": 1.02
        }
        multiplier = role_multipliers.get(role.lower(), 1.0)

        base_salary = base * multiplier

        benchmark = SalaryBenchmark(
            role=role,
            location=location,
            experience_level=f"{experience_years} years",
            timestamp=datetime.now(),
            percentile_25=base_salary * 0.85,
            percentile_50=base_salary,
            percentile_75=base_salary * 1.15,
            percentile_90=base_salary * 1.35,
            base_salary=base_salary,
            total_comp=base_salary * 1.25,  # Include bonus/equity
            bonus_pct=0.15,
            equity_value=base_salary * 0.10,
            industry_premium={
                "technology": 0.15,
                "finance": 0.20,
                "healthcare": 0.05,
                "retail": -0.10
            },
            company_size_premium={
                "startup": 0.05,
                "mid_size": 0.0,
                "enterprise": 0.08,
                "faang": 0.30
            },
            remote_adjustment=-0.05,
            yoy_change=0.045,
            market_trend="up"
        )

        self.benchmarks.append(benchmark)
        return benchmark

    async def compare_offers(
        self,
        offers: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Compare multiple job offers"""

        analyzed = []

        for offer in offers:
            total_value = (
                offer.get("base", 0) +
                offer.get("bonus", 0) +
                offer.get("equity_annual", 0) +
                offer.get("benefits_value", 0)
            )

            analyzed.append({
                "company": offer.get("company", "Unknown"),
                "total_annual_value": total_value,
                "base_salary": offer.get("base", 0),
                "bonus": offer.get("bonus", 0),
                "equity": offer.get("equity_annual", 0),
                "growth_potential": offer.get("growth_score", 0.5)
            })

        # Rank by total value
        analyzed.sort(key=lambda x: x["total_annual_value"], reverse=True)

        return {
            "offers_analyzed": len(offers),
            "ranked_offers": analyzed,
            "recommendation": analyzed[0]["company"] if analyzed else None,
            "analysis_notes": [
                "Consider equity vesting schedules",
                "Factor in career growth potential",
                "Compare benefits packages"
            ]
        }


class WorkforceAnalyticsAPI:
    """
    API for workforce and hiring analytics.

    Features:
    - Hiring trends by industry
    - Talent flow patterns
    - Workforce composition
    - Automation impact

    Pricing:
    - Enterprise: $2,999/mo
    - Custom research: Starting at $10,000
    """

    def __init__(self):
        self.insights: List[WorkforceInsight] = []

    async def get_hiring_trends(
        self,
        industry: IndustryType,
        months: int = 6
    ) -> Dict[str, Any]:
        """Get hiring trends for an industry"""

        return {
            "industry": industry.value,
            "period_months": months,
            "metrics": {
                "total_postings": 125000,
                "posting_growth": 0.15,
                "time_to_fill_days": 42,
                "offer_acceptance_rate": 0.72
            },
            "top_roles": [
                {"role": "Software Engineer", "postings": 25000, "growth": 0.20},
                {"role": "Data Scientist", "postings": 12000, "growth": 0.35},
                {"role": "Product Manager", "postings": 8000, "growth": 0.18}
            ],
            "top_skills": [
                {"skill": "Python", "demand_index": 95},
                {"skill": "AWS", "demand_index": 88},
                {"skill": "React", "demand_index": 82}
            ],
            "salary_trends": {
                "median_change": 0.05,
                "top_25_change": 0.08
            }
        }

    async def get_talent_flow(
        self,
        from_industry: Optional[str] = None,
        to_industry: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get talent flow patterns between industries"""

        return {
            "period": "Last 12 months",
            "flows": [
                {
                    "from": "Consulting",
                    "to": "Technology",
                    "volume": 15000,
                    "common_roles": ["Product Manager", "Data Analyst"]
                },
                {
                    "from": "Finance",
                    "to": "Fintech",
                    "volume": 12000,
                    "common_roles": ["Quant", "Risk Analyst"]
                },
                {
                    "from": "Technology",
                    "to": "Startups",
                    "volume": 8000,
                    "common_roles": ["Senior Engineer", "Tech Lead"]
                }
            ],
            "net_gainers": ["Technology", "Healthcare Tech"],
            "net_losers": ["Retail", "Traditional Banking"]
        }

    async def get_automation_impact(
        self,
        role: str
    ) -> Dict[str, Any]:
        """Get automation impact assessment for a role"""

        # Simulated automation risk scores
        risk_scores = {
            "data entry clerk": 0.85,
            "truck driver": 0.70,
            "accountant": 0.45,
            "software engineer": 0.15,
            "nurse": 0.10,
            "therapist": 0.05
        }

        risk = risk_scores.get(role.lower(), 0.30)

        return {
            "role": role,
            "automation_risk": risk,
            "risk_level": "high" if risk > 0.6 else "medium" if risk > 0.3 else "low",
            "timeline_years": 5 if risk > 0.6 else 10 if risk > 0.3 else 15,
            "tasks_at_risk": [
                "Repetitive data processing",
                "Standard reporting",
                "Basic analysis"
            ],
            "skills_to_develop": [
                "Critical thinking",
                "Creative problem solving",
                "Stakeholder management",
                "AI/ML tool proficiency"
            ],
            "adjacent_roles": [
                "AI/ML Specialist",
                "Process Optimizer",
                "Human-AI Collaboration Manager"
            ]
        }


# FastAPI Router
def create_labor_data_products_router():
    """Create FastAPI router for labor data products"""

    from fastapi import APIRouter, Query

    router = APIRouter(
        prefix="/data-products/labor",
        tags=["labor-data-products"]
    )

    skills_api = SkillDemandForecastsAPI()
    salary_api = SalaryIntelligenceAPI()
    workforce_api = WorkforceAnalyticsAPI()

    @router.get("/skills/{skill}")
    async def get_skill_forecast(skill: str):
        """Get skill demand forecast"""
        return await skills_api.get_skill_forecast(skill)

    @router.get("/skills/trending")
    async def get_trending(
        limit: int = Query(20, le=50)
    ):
        """Get trending skills"""
        return await skills_api.get_trending_skills(limit=limit)

    @router.get("/salary/{role}")
    async def get_salary(
        role: str,
        location: str = "United States",
        years: int = Query(5, ge=0, le=30)
    ):
        """Get salary benchmark"""
        return await salary_api.get_salary_benchmark(
            role=role,
            location=location,
            experience_years=years
        )

    @router.get("/workforce/hiring/{industry}")
    async def get_hiring(
        industry: str,
        months: int = Query(6, le=24)
    ):
        """Get hiring trends"""
        return await workforce_api.get_hiring_trends(
            IndustryType(industry),
            months
        )

    @router.get("/workforce/automation/{role}")
    async def get_automation(role: str):
        """Get automation impact assessment"""
        return await workforce_api.get_automation_impact(role)

    return router
