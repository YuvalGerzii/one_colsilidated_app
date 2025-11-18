"""
Career Tools API
Unified API for mental health, networking, salary negotiation, interview prep, skills verification
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, List, Any, Optional
from pydantic import BaseModel

from app.models.mental_health import MentalHealthSystem
from app.models.networking_intelligence import NetworkingIntelligence
from app.models.salary_negotiation import SalaryNegotiationCoach
from app.models.interview_prep import InterviewPreparationSystem
from app.models.skills_certification import SkillsCertificationTracker


router = APIRouter()

# Initialize systems
mental_health = MentalHealthSystem()
networking = NetworkingIntelligence()
salary_coach = SalaryNegotiationCoach()
interview_prep = InterviewPreparationSystem()
skills_tracker = SkillsCertificationTracker()


# ==================== MENTAL HEALTH ENDPOINTS ====================

class BurnoutAssessmentRequest(BaseModel):
    work_hours_weekly: float = 40
    recent_rejections: int = 0
    months_unemployed: int = 0
    emergency_fund_months: float = 3
    debt_to_income_ratio: float = 0.3
    social_support_score: int = 5
    sleep_hours_avg: float = 7
    exercise_days_weekly: int = 3


@router.post("/mental-health/burnout-assessment")
async def assess_burnout_risk(data: BurnoutAssessmentRequest):
    """
    Assess burnout risk with comprehensive analysis
    """
    result = mental_health.assess_burnout_risk(data.dict())
    return result


@router.post("/mental-health/stress-assessment")
async def assess_stress_level(stress_indicators: Dict[str, bool]):
    """
    Assess current stress level based on indicators
    """
    result = mental_health.stress_level_assessment(stress_indicators)
    return result


class WorkLifeBalanceRequest(BaseModel):
    work_hours_weekly: float = 40
    job_search_hours_weekly: float = 0
    learning_hours_weekly: float = 0
    family_hours_weekly: float = 0
    personal_hours_weekly: float = 0
    sleep_hours_weekly: float = 49


@router.post("/mental-health/work-life-balance")
async def analyze_work_life_balance(data: WorkLifeBalanceRequest):
    """
    Analyze work-life balance and get recommendations
    """
    result = mental_health.work_life_balance_score(data.dict())
    return result


@router.post("/mental-health/wellness-checkin/{worker_id}")
async def wellness_check_in(
    worker_id: int,
    mood_score: int = Query(..., ge=1, le=10),
    energy_level: int = Query(..., ge=1, le=10),
    notes: Optional[str] = None
):
    """
    Daily/weekly wellness check-in
    """
    result = mental_health.wellness_check_in(worker_id, mood_score, energy_level, notes)
    return result


# ==================== NETWORKING ENDPOINTS ====================

class NetworkAnalysisRequest(BaseModel):
    connections: List[Dict[str, Any]]
    target_industry: str
    target_role: str
    current_role: str


@router.post("/networking/analyze-network")
async def analyze_network(data: NetworkAnalysisRequest):
    """
    Comprehensive network analysis with gaps and recommendations
    """
    result = networking.analyze_network(data.dict())
    return result


class ConnectionValueRequest(BaseModel):
    connection: Dict[str, Any]
    target_industry: str
    target_role: str


@router.post("/networking/connection-value")
async def calculate_connection_value(data: ConnectionValueRequest):
    """
    Calculate strategic value of a specific connection
    """
    result = networking.connection_value_score(
        data.connection, data.target_industry, data.target_role
    )
    return result


class NetworkingEventsRequest(BaseModel):
    target_industry: str
    target_role: str
    location: str = ""
    weekly_networking_hours: float = 2


@router.post("/networking/event-recommendations")
async def get_networking_events(data: NetworkingEventsRequest):
    """
    Get personalized networking event recommendations
    """
    result = networking.networking_event_recommendations(data.dict())
    return result


class LinkedInAuditRequest(BaseModel):
    has_photo: bool = False
    headline: str = ""
    about: str = ""
    experience_count: int = 0
    experiences_with_bullets: int = 0
    skills_count: int = 0
    recommendations_count: int = 0
    posts_per_month: int = 0
    has_custom_url: bool = False
    certifications_count: int = 0


@router.post("/networking/linkedin-audit")
async def audit_linkedin_profile(data: LinkedInAuditRequest):
    """
    Audit LinkedIn profile and get optimization recommendations
    """
    result = networking.linkedin_optimization_audit(data.dict())
    return result


# ==================== SALARY NEGOTIATION ENDPOINTS ====================

class OfferAnalysisRequest(BaseModel):
    base_salary: float
    bonus_target: float = 0
    equity_value: float = 0
    role: str
    industry: str = "tech"
    location: str = ""
    years_experience: int = 0
    competing_offers: bool = False
    currently_employed: bool = True
    unique_skills: List[str] = []
    market_demand: str = "moderate"
    company_urgency: str = "normal"
    interview_feedback: str = "good"


@router.post("/salary/analyze-offer")
async def analyze_job_offer(data: OfferAnalysisRequest):
    """
    Analyze job offer and get negotiation strategies
    """
    result = salary_coach.analyze_offer(data.dict())
    return result


class CounterOfferRequest(BaseModel):
    current_offer: Dict[str, Any]
    target_comp: float
    leverage_level: str


@router.post("/salary/generate-counteroffer")
async def generate_counteroffer(data: CounterOfferRequest):
    """
    Generate structured counteroffer with justification
    """
    result = salary_coach.generate_counteroffer(
        data.current_offer, data.target_comp, data.leverage_level
    )
    return result


@router.post("/salary/benefits-negotiation")
async def get_benefits_guide(offer_data: Dict[str, Any]):
    """
    Get benefits negotiation guide
    """
    result = salary_coach.benefits_negotiation_guide(offer_data)
    return result


@router.post("/salary/leverage-assessment")
async def assess_leverage(situation: Dict[str, Any]):
    """
    Assess negotiation leverage
    """
    result = salary_coach.leverage_assessment(situation)
    return result


# ==================== INTERVIEW PREP ENDPOINTS ====================

class MockInterviewRequest(BaseModel):
    interview_type: str = "behavioral"
    role: str = "software_engineer"
    difficulty: str = "medium"
    duration_minutes: int = 60


@router.post("/interview/generate-mock")
async def create_mock_interview(data: MockInterviewRequest):
    """
    Generate personalized mock interview
    """
    result = interview_prep.generate_mock_interview(data.dict())
    return result


class InterviewEvaluationRequest(BaseModel):
    interview_type: str
    responses: List[Dict[str, Any]]
    technical_accuracy_score: int = 7
    communication_score: int = 7
    problem_solving_score: int = 7
    confidence_score: int = 7
    enthusiasm_score: int = 7


@router.post("/interview/evaluate-performance")
async def evaluate_interview(data: InterviewEvaluationRequest):
    """
    Evaluate mock interview performance
    """
    result = interview_prep.evaluate_interview_performance(data.dict())
    return result


class QuestionBankRequest(BaseModel):
    interview_type: str = "behavioral"
    role: str = ""
    difficulty: str = "medium"
    company_type: str = ""


@router.post("/interview/question-bank")
async def get_question_bank(data: QuestionBankRequest):
    """
    Get curated question bank
    """
    result = interview_prep.get_question_bank(data.dict())
    return result


class AnswerCoachingRequest(BaseModel):
    question: str
    user_answer: str
    interview_type: str


@router.post("/interview/coach-answer")
async def coach_answer(data: AnswerCoachingRequest):
    """
    Get coaching on interview answer
    """
    result = interview_prep.coach_answer(
        data.question, data.user_answer, data.interview_type
    )
    return result


@router.get("/interview/company-prep/{company_name}")
async def get_company_prep(company_name: str, role: str = Query(...)):
    """
    Get company-specific interview preparation
    """
    result = interview_prep.company_specific_prep(company_name, role)
    return result


@router.get("/interview/progress/{worker_id}")
async def track_interview_progress(worker_id: int):
    """
    Track interview preparation progress
    """
    result = interview_prep.track_interview_progress(worker_id)
    return result


# ==================== SKILLS & CERTIFICATION ENDPOINTS ====================

class SkillInventoryRequest(BaseModel):
    skills: List[Dict[str, Any]]
    target_role: str = ""


@router.post("/skills/inventory")
async def track_skills(data: SkillInventoryRequest):
    """
    Track comprehensive skill inventory
    """
    result = skills_tracker.track_skill_inventory(data.dict())
    return result


class CertificationRecommendationRequest(BaseModel):
    target_role: str = "software_engineer"
    field: str = "software_engineering"
    current_salary: float = 100000
    certification_budget: float = 1000
    available_study_hours_weekly: float = 10


@router.post("/skills/certification-recommendations")
async def recommend_certifications(data: CertificationRecommendationRequest):
    """
    Get personalized certification recommendations
    """
    result = skills_tracker.recommend_certifications(data.dict())
    return result


class SkillVerificationRequest(BaseModel):
    skill_name: str
    verification_type: str = "self_assessment"
    current_level: str = "intermediate"
    verification_status: str = "unverified"


@router.post("/skills/verify")
async def verify_skill(data: SkillVerificationRequest):
    """
    Initiate skill verification process
    """
    result = skills_tracker.verify_skill(data.dict())
    return result


class SkillGapRequest(BaseModel):
    current_skills: List[str]
    target_role: str


@router.post("/skills/gap-validation")
async def validate_skill_gaps(data: SkillGapRequest):
    """
    Validate skill gaps for target role
    """
    result = skills_tracker.skill_gap_validation(data.current_skills, data.target_role)
    return result


# ==================== COMBINED ENDPOINTS ====================

@router.get("/career-readiness/{worker_id}")
async def get_career_readiness_dashboard(worker_id: int):
    """
    Comprehensive career readiness dashboard combining all systems
    """
    # This would aggregate data from all systems
    return {
        "worker_id": worker_id,
        "overall_readiness_score": 78.5,
        "readiness_breakdown": {
            "mental_wellbeing": 85,
            "network_strength": 72,
            "interview_readiness": 80,
            "skills_verification": 75,
            "salary_negotiation_prep": 70
        },
        "top_priorities": [
            "Verify your top 3 skills with certifications",
            "Expand network in target industry (currently 12 connections)",
            "Complete 2 more mock interviews",
            "Review salary negotiation strategies"
        ],
        "next_actions": {
            "this_week": [
                "Take AWS certification exam (scheduled)",
                "Reach out to 10 connections in target industry",
                "Complete 1 behavioral mock interview"
            ],
            "this_month": [
                "Earn 2 professional certifications",
                "Attend 2 networking events",
                "Practice 20 interview questions",
                "Analyze 3 job offers using salary coach"
            ]
        }
    }


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "career-tools-api"}
