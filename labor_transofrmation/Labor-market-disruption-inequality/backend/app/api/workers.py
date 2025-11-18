from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel, EmailStr
from app.db.database import get_db
from app.db.models import Worker, WorkerSkill
from app.models.risk_predictor import JobLossRiskPredictor

router = APIRouter()
risk_predictor = JobLossRiskPredictor()

# Pydantic models
class WorkerCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    current_job_title: str
    current_industry: str
    years_experience: int
    education_level: str
    location: str

class WorkerResponse(BaseModel):
    id: int
    email: str
    full_name: str
    current_job_title: str
    current_industry: str
    years_experience: int
    risk_score: float | None

    class Config:
        from_attributes = True

class RiskAssessmentResponse(BaseModel):
    worker_id: int
    risk_score: float
    risk_level: str
    confidence: float
    factors: List[dict]

@router.post("/", response_model=WorkerResponse)
def create_worker(worker: WorkerCreate, db: Session = Depends(get_db)):
    """Register a new worker"""
    # Check if email exists
    existing = db.query(Worker).filter(Worker.email == worker.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create worker (in production, hash the password properly)
    db_worker = Worker(
        email=worker.email,
        full_name=worker.full_name,
        hashed_password=f"hashed_{worker.password}",  # TODO: Proper hashing
        current_job_title=worker.current_job_title,
        current_industry=worker.current_industry,
        years_experience=worker.years_experience,
        education_level=worker.education_level,
        location=worker.location
    )

    db.add(db_worker)
    db.commit()
    db.refresh(db_worker)

    return db_worker

@router.get("/{worker_id}", response_model=WorkerResponse)
def get_worker(worker_id: int, db: Session = Depends(get_db)):
    """Get worker profile"""
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    return worker

@router.get("/{worker_id}/risk-assessment", response_model=RiskAssessmentResponse)
def assess_risk(worker_id: int, db: Session = Depends(get_db)):
    """
    Assess job loss risk for a worker
    Uses ML model to predict automation/displacement risk
    """
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    # Get worker skills
    worker_skills = db.query(WorkerSkill).filter(
        WorkerSkill.worker_id == worker_id
    ).all()

    # Calculate average skill metrics
    skill_demand_avg = 50  # TODO: Calculate from actual skill data
    skill_automation_risk_avg = 50  # TODO: Calculate from actual skill data
    skill_diversity_score = len(worker_skills)

    # Prepare worker data
    worker_data = {
        'years_experience': worker.years_experience,
        'education_level': worker.education_level,
        'current_industry': worker.current_industry,
        'skill_demand_avg': skill_demand_avg,
        'skill_automation_risk_avg': skill_automation_risk_avg,
        'skill_diversity_score': skill_diversity_score,
        'recent_skill_acquisition': 0,  # TODO: Track this
        'age_category': 2,  # TODO: Add age to worker model
        'remote_capability': 0.5  # TODO: Add remote capability assessment
    }

    # Get risk prediction
    risk_result = risk_predictor.predict_risk(worker_data)

    # Update worker record
    worker.risk_score = risk_result['risk_score']
    db.commit()

    return {
        'worker_id': worker_id,
        **risk_result
    }

@router.get("/{worker_id}/profile")
def get_worker_profile(worker_id: int, db: Session = Depends(get_db)):
    """Get complete worker profile with skills and applications"""
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    skills = db.query(WorkerSkill).filter(
        WorkerSkill.worker_id == worker_id
    ).all()

    return {
        'worker': worker,
        'skills': skills,
        'risk_score': worker.risk_score,
        'applications_count': len(worker.applications)
    }
