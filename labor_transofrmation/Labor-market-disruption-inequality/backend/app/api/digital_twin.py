from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from app.db.database import get_db
from app.models.digital_twin import WorkforceDigitalTwin

router = APIRouter()
digital_twin = WorkforceDigitalTwin()

class MarketInitRequest(BaseModel):
    total_jobs: int
    total_workers: int
    unemployment_rate: float
    avg_salary: float
    skills_demand: dict
    occupation_health: dict
    automation_index: float

class SimulationRequest(BaseModel):
    time_horizon_months: int = 12
    automation_adoption_rate: float = 0.05

class DisplacementRequest(BaseModel):
    occupation: str
    time_horizon_months: int = 18

class ScenarioRequest(BaseModel):
    adoption_percentage: float
    affected_occupations: List[str]
    time_horizon_months: int = 24

class RegionHeatmapRequest(BaseModel):
    regions: List[str]
    market_data_by_region: dict

@router.post("/initialize")
def initialize_digital_twin(request: MarketInitRequest):
    """
    Initialize Digital Twin with current market data
    """
    digital_twin.initialize_from_data(request.dict())

    return {
        "status": "initialized",
        "timestamp": digital_twin.current_state.timestamp.isoformat(),
        "message": "Digital Twin successfully initialized with market data"
    }

@router.post("/simulate")
def simulate_market(request: SimulationRequest):
    """
    Simulate market dynamics over time
    Real-time AI simulation of labor market evolution
    """
    simulations = digital_twin.simulate_market_dynamics(
        time_horizon_months=request.time_horizon_months,
        automation_adoption_rate=request.automation_adoption_rate
    )

    return {
        "time_horizon_months": request.time_horizon_months,
        "automation_rate": request.automation_adoption_rate,
        "simulations": [
            {
                "month": i,
                "timestamp": sim.timestamp.isoformat(),
                "total_jobs": sim.total_jobs,
                "unemployment_rate": sim.unemployment_rate,
                "avg_salary": sim.avg_salary,
                "automation_index": sim.automation_index
            }
            for i, sim in enumerate(simulations)
        ],
        "insights": {
            "projected_job_loss": simulations[0].total_jobs - simulations[-1].total_jobs if simulations else 0,
            "unemployment_delta": simulations[-1].unemployment_rate - simulations[0].unemployment_rate if simulations else 0
        }
    }

@router.post("/displacement-prediction")
def predict_displacement(request: DisplacementRequest):
    """
    Predict displacement probability for specific occupation
    Core Digital Twin feature
    """
    prediction = digital_twin.predict_occupation_displacement(
        occupation=request.occupation,
        time_horizon_months=request.time_horizon_months
    )

    return prediction

@router.post("/scenario-modeling")
def model_scenario(request: ScenarioRequest):
    """
    Model "what-if" automation scenarios
    Example: "If 50% of companies adopt automation, what jobs vanish next?"
    """
    results = digital_twin.model_automation_scenario(
        adoption_percentage=request.adoption_percentage,
        affected_occupations=request.affected_occupations,
        time_horizon_months=request.time_horizon_months
    )

    return results

@router.get("/macro-risk-index")
def get_macro_risk_index():
    """
    Get monthly updated macro AI job-risk index
    Overall market health indicator (0-100)
    """
    # Mock market data - in production, fetch from real sources
    market_data = {
        'automation_adoption': 45,
        'job_vacancy_rate': 65,
        'skill_mismatch': 55,
        'unemployment_trend': 35,
        'tech_disruption': 60
    }

    risk_index = digital_twin.calculate_macro_job_risk_index(market_data)

    return risk_index

@router.post("/region-heatmap")
def generate_region_heatmap(request: RegionHeatmapRequest):
    """
    Generate region-level risk heatmap
    Geographical visualization of automation risk
    """
    heatmap = digital_twin.generate_region_risk_heatmap(
        regions=request.regions,
        market_data_by_region=request.market_data_by_region
    )

    return heatmap

@router.post("/predictive-alert")
def get_predictive_alert(occupation: str, location: str, time_horizon: int = 18):
    """
    Generate predictive alert for worker
    Example: "30% of bookkeeping tasks automated in 18 months in your field"
    """
    alert = digital_twin.generate_predictive_alert(
        occupation=occupation,
        worker_location=location,
        time_horizon_months=time_horizon
    )

    return alert

@router.get("/government-dashboard")
def get_government_dashboard():
    """
    Government dashboard with comprehensive labor market insights
    """
    # Mock data for demonstration
    regions = ['California', 'Texas', 'New York', 'Florida', 'Illinois']

    market_data_by_region = {
        'California': {
            'industries': ['Technology', 'Entertainment', 'Agriculture'],
            'unemployment': 4.5,
            'automation_adoption': 55,
            'total_workers': 19000000,
            'industry_automation_exposure': 60
        },
        'Texas': {
            'industries': ['Energy', 'Manufacturing', 'Technology'],
            'unemployment': 3.8,
            'automation_adoption': 45,
            'total_workers': 14000000,
            'industry_automation_exposure': 50
        },
        'New York': {
            'industries': ['Finance', 'Media', 'Healthcare'],
            'unemployment': 4.2,
            'automation_adoption': 60,
            'total_workers': 9500000,
            'industry_automation_exposure': 65
        },
        'Florida': {
            'industries': ['Tourism', 'Healthcare', 'Retail'],
            'unemployment': 3.5,
            'automation_adoption': 40,
            'total_workers': 10000000,
            'industry_automation_exposure': 55
        },
        'Illinois': {
            'industries': ['Manufacturing', 'Finance', 'Agriculture'],
            'unemployment': 4.8,
            'automation_adoption': 50,
            'total_workers': 6200000,
            'industry_automation_exposure': 58
        }
    }

    # Get comprehensive data
    heatmap = digital_twin.generate_region_risk_heatmap(regions, market_data_by_region)

    macro_risk = digital_twin.calculate_macro_job_risk_index({
        'automation_adoption': 50,
        'job_vacancy_rate': 60,
        'skill_mismatch': 50,
        'unemployment_trend': 40,
        'tech_disruption': 55
    })

    # Top threatened occupations nationally
    high_risk_occupations = [
        {'occupation': 'Retail Salesperson', 'workers': 4500000, 'displacement_risk': 75},
        {'occupation': 'Office Clerk', 'workers': 2800000, 'displacement_risk': 80},
        {'occupation': 'Customer Service Rep', 'workers': 2700000, 'displacement_risk': 70},
        {'occupation': 'Data Entry', 'workers': 1200000, 'displacement_risk': 95},
        {'occupation': 'Cashier', 'workers': 3600000, 'displacement_risk': 85}
    ]

    return {
        'macro_risk_index': macro_risk,
        'region_heatmap': heatmap,
        'high_risk_occupations': high_risk_occupations,
        'total_workers_at_risk': sum(market_data_by_region[r]['total_workers'] * (heatmap['regions'][i]['risk_score'] / 100)
                                      for i, r in enumerate(regions)),
        'policy_recommendations': [
            'Accelerate nationwide reskilling programs',
            'Invest in automation-resistant sectors',
            'Strengthen safety net for displaced workers',
            'Incentivize hiring in high-growth sectors'
        ]
    }

@router.get("/employer-dashboard/{industry}")
def get_employer_dashboard(industry: str):
    """
    Employer-specific dashboard with industry insights
    """
    # Industry-specific automation data
    industry_data = {
        'retail': {'automation_pressure': 75, 'talent_shortage': 45},
        'technology': {'automation_pressure': 35, 'talent_shortage': 80},
        'manufacturing': {'automation_pressure': 80, 'talent_shortage': 60},
        'healthcare': {'automation_pressure': 30, 'talent_shortage': 85},
        'finance': {'automation_pressure': 65, 'talent_shortage': 55}
    }

    data = industry_data.get(industry.lower(), {'automation_pressure': 50, 'talent_shortage': 50})

    return {
        'industry': industry,
        'automation_pressure': data['automation_pressure'],
        'talent_shortage_index': data['talent_shortage'],
        'recommended_actions': [
            f"Prepare for {data['automation_pressure']}% automation pressure",
            'Invest in workforce reskilling programs',
            'Partner with training providers',
            'Focus on automation-complementary roles'
        ],
        'hiring_forecast': {
            'next_quarter': 'Moderate growth',
            'automation_impact': f"{data['automation_pressure']}% of roles affected",
            'critical_skills': ['AI/ML', 'Data Analysis', 'Automation']
        }
    }
