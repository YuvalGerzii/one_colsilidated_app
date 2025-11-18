from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from app.db.database import get_db
from app.db.models import Skill, WorkerSkill

router = APIRouter()

class SkillCreate(BaseModel):
    name: str
    category: str
    description: str
    demand_score: float = 50.0
    automation_risk: float = 50.0

class SkillResponse(BaseModel):
    id: int
    name: str
    category: str
    demand_score: float
    automation_risk: float

    class Config:
        from_attributes = True

class WorkerSkillAdd(BaseModel):
    worker_id: int
    skill_id: int
    proficiency_level: int
    years_experience: int = 0

@router.post("/", response_model=SkillResponse)
def create_skill(skill: SkillCreate, db: Session = Depends(get_db)):
    """Create a new skill in the system"""
    db_skill = Skill(**skill.dict())
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill

@router.get("/", response_model=List[SkillResponse])
def list_skills(
    category: Optional[str] = None,
    min_demand: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """List all skills with optional filters"""
    query = db.query(Skill)

    if category:
        query = query.filter(Skill.category == category)

    if min_demand:
        query = query.filter(Skill.demand_score >= min_demand)

    return query.all()

@router.get("/{skill_id}", response_model=SkillResponse)
def get_skill(skill_id: int, db: Session = Depends(get_db)):
    """Get skill details"""
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill

@router.post("/worker-skill")
def add_worker_skill(worker_skill: WorkerSkillAdd, db: Session = Depends(get_db)):
    """Add a skill to a worker's profile"""
    db_worker_skill = WorkerSkill(**worker_skill.dict())
    db.add(db_worker_skill)
    db.commit()
    db.refresh(db_worker_skill)
    return {"message": "Skill added successfully", "id": db_worker_skill.id}

@router.get("/in-demand")
def get_in_demand_skills(limit: int = 20, db: Session = Depends(get_db)):
    """Get most in-demand skills"""
    skills = db.query(Skill).order_by(
        Skill.demand_score.desc()
    ).limit(limit).all()

    return {
        'in_demand_skills': [
            {
                'id': s.id,
                'name': s.name,
                'category': s.category,
                'demand_score': s.demand_score,
                'automation_risk': s.automation_risk
            }
            for s in skills
        ]
    }

@router.get("/automation-risk")
def get_automation_risk_skills(threshold: float = 60, db: Session = Depends(get_db)):
    """Get skills at high risk of automation"""
    skills = db.query(Skill).filter(
        Skill.automation_risk >= threshold
    ).order_by(
        Skill.automation_risk.desc()
    ).all()

    return {
        'high_risk_skills': [
            {
                'id': s.id,
                'name': s.name,
                'category': s.category,
                'automation_risk': s.automation_risk
            }
            for s in skills
        ]
    }
