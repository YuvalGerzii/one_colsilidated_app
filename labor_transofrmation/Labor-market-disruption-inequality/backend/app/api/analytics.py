from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from pydantic import BaseModel
from app.db.database import get_db
from app.db.models import Worker, Skill, WorkerSkill, Job, JobSkill
from app.models.reskilling_advisor import ReskillingAdvisor

router = APIRouter()
reskilling_advisor = ReskillingAdvisor()

class SkillGapAnalysisRequest(BaseModel):
    worker_id: int
    target_job_id: int

class SkillGapResponse(BaseModel):
    readiness_score: float
    missing_skills: List[dict]
    skills_to_upgrade: List[dict]
    matched_skills: List[dict]
    total_estimated_weeks: int

class LearningPathRequest(BaseModel):
    worker_id: int
    target_job_id: int
    max_budget: float = 5000
    max_duration_weeks: int = 26
    online_only: bool = True

@router.post("/skill-gap", response_model=SkillGapResponse)
def analyze_skill_gap(request: SkillGapAnalysisRequest, db: Session = Depends(get_db)):
    """
    Analyze skill gap between worker's current skills and target job
    Core feature: Skill-gap analytics
    """
    # Get worker skills
    worker_skills = db.query(WorkerSkill).filter(
        WorkerSkill.worker_id == request.worker_id
    ).all()

    current_skills = [
        {
            'skill_id': ws.skill_id,
            'proficiency_level': ws.proficiency_level
        }
        for ws in worker_skills
    ]

    # Get target job skills
    job_skills = db.query(JobSkill).filter(
        JobSkill.job_id == request.target_job_id
    ).all()

    target_job_skills = [
        {
            'skill_id': js.skill_id,
            'required': js.required,
            'importance': js.importance
        }
        for js in job_skills
    ]

    # Get skill metadata
    all_skill_ids = list(set([s['skill_id'] for s in current_skills + target_job_skills]))
    skills = db.query(Skill).filter(Skill.id.in_(all_skill_ids)).all()

    skill_metadata = {
        skill.id: {
            'name': skill.name,
            'category': skill.category,
            'demand_score': skill.demand_score,
            'automation_risk': skill.automation_risk
        }
        for skill in skills
    }

    # Analyze gap
    gap_analysis = reskilling_advisor.analyze_skill_gap(
        current_skills,
        target_job_skills,
        skill_metadata
    )

    return gap_analysis

@router.post("/learning-path")
def recommend_learning_path(request: LearningPathRequest, db: Session = Depends(get_db)):
    """
    Recommend tailored reskilling pathway for worker
    Core feature: Tailored reskilling pathways
    """
    # First get skill gap analysis
    gap_request = SkillGapAnalysisRequest(
        worker_id=request.worker_id,
        target_job_id=request.target_job_id
    )
    gap_analysis = analyze_skill_gap(gap_request, db)

    # Get available training programs (mock data for now)
    # TODO: Implement actual training program database
    training_programs = [
        {
            'id': 1,
            'title': 'Python Programming Fundamentals',
            'provider': 'Coursera',
            'duration_weeks': 8,
            'cost': 399,
            'online': True,
            'target_skills': [1, 2, 3],
            'success_rate': 0.85
        },
        {
            'id': 2,
            'title': 'Data Science with Python',
            'provider': 'Udacity',
            'duration_weeks': 12,
            'cost': 799,
            'online': True,
            'target_skills': [4, 5],
            'success_rate': 0.80
        }
    ]

    worker_preferences = {
        'max_budget': request.max_budget,
        'max_duration_weeks': request.max_duration_weeks,
        'online_only': request.online_only
    }

    learning_path = reskilling_advisor.recommend_learning_path(
        gap_analysis.dict(),
        training_programs,
        worker_preferences
    )

    return learning_path

@router.get("/market-trends")
def get_market_trends(db: Session = Depends(get_db)):
    """
    Get labor market trends and insights
    Shows in-demand skills, automation risk by industry, etc.
    """
    # Top in-demand skills
    top_skills = db.query(
        Skill.name,
        Skill.demand_score,
        Skill.category
    ).order_by(
        Skill.demand_score.desc()
    ).limit(10).all()

    # Skills at risk of automation
    at_risk_skills = db.query(
        Skill.name,
        Skill.automation_risk
    ).filter(
        Skill.automation_risk > 70
    ).order_by(
        Skill.automation_risk.desc()
    ).limit(10).all()

    # Industry automation risk distribution
    industry_risks = db.query(
        Worker.current_industry,
        func.avg(Worker.risk_score).label('avg_risk')
    ).group_by(
        Worker.current_industry
    ).all()

    return {
        'top_in_demand_skills': [
            {'name': s.name, 'demand_score': s.demand_score, 'category': s.category}
            for s in top_skills
        ],
        'high_automation_risk_skills': [
            {'name': s.name, 'automation_risk': s.automation_risk}
            for s in at_risk_skills
        ],
        'industry_risk_scores': [
            {'industry': ir[0], 'avg_risk_score': float(ir[1]) if ir[1] else 0}
            for ir in industry_risks
        ]
    }

@router.get("/worker-statistics")
def get_worker_statistics(db: Session = Depends(get_db)):
    """Get aggregate statistics about workers in the system"""
    total_workers = db.query(func.count(Worker.id)).scalar()

    high_risk_count = db.query(func.count(Worker.id)).filter(
        Worker.risk_score > 60
    ).scalar()

    avg_risk = db.query(func.avg(Worker.risk_score)).scalar()

    # Workers by industry
    by_industry = db.query(
        Worker.current_industry,
        func.count(Worker.id)
    ).group_by(Worker.current_industry).all()

    return {
        'total_workers': total_workers,
        'high_risk_workers': high_risk_count,
        'average_risk_score': float(avg_risk) if avg_risk else 0,
        'workers_by_industry': [
            {'industry': i[0], 'count': i[1]}
            for i in by_industry
        ]
    }
