from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from app.db.database import get_db
from app.db.models import Enterprise, Worker, Job

router = APIRouter()

class EnterpriseCreate(BaseModel):
    company_name: str
    industry: str
    size: str
    subscription_tier: str
    contact_email: EmailStr

class EnterpriseResponse(BaseModel):
    id: int
    company_name: str
    industry: str
    size: str
    subscription_tier: str
    active: bool

    class Config:
        from_attributes = True

class WorkforceDashboardResponse(BaseModel):
    total_employees: int
    high_risk_employees: int
    avg_risk_score: float
    skills_gap_summary: dict
    recommended_training: List[dict]

@router.post("/", response_model=EnterpriseResponse)
def create_enterprise(enterprise: EnterpriseCreate, db: Session = Depends(get_db)):
    """
    Register new enterprise customer
    Core feature: Enterprise subscription for HR
    """
    # Set subscription expiration based on tier
    subscription_duration = {
        'basic': 30,
        'professional': 90,
        'enterprise': 365
    }

    days = subscription_duration.get(enterprise.subscription_tier, 30)

    db_enterprise = Enterprise(
        **enterprise.dict(),
        subscription_expires=datetime.utcnow() + timedelta(days=days)
    )

    db.add(db_enterprise)
    db.commit()
    db.refresh(db_enterprise)

    return db_enterprise

@router.get("/{enterprise_id}", response_model=EnterpriseResponse)
def get_enterprise(enterprise_id: int, db: Session = Depends(get_db)):
    """Get enterprise details"""
    enterprise = db.query(Enterprise).filter(Enterprise.id == enterprise_id).first()
    if not enterprise:
        raise HTTPException(status_code=404, detail="Enterprise not found")
    return enterprise

@router.get("/{enterprise_id}/dashboard")
def get_workforce_dashboard(enterprise_id: int, db: Session = Depends(get_db)):
    """
    Get comprehensive workforce analytics dashboard
    Shows risk assessment, skills gaps, and training recommendations
    """
    # Verify enterprise exists
    enterprise = db.query(Enterprise).filter(Enterprise.id == enterprise_id).first()
    if not enterprise:
        raise HTTPException(status_code=404, detail="Enterprise not found")

    # Get workforce statistics (filtering by industry for demo)
    workers = db.query(Worker).filter(
        Worker.current_industry == enterprise.industry
    ).all()

    total_employees = len(workers)

    high_risk_count = len([w for w in workers if w.risk_score and w.risk_score > 60])

    avg_risk = sum([w.risk_score or 0 for w in workers]) / total_employees if total_employees > 0 else 0

    # Risk distribution
    risk_distribution = {
        'low': len([w for w in workers if w.risk_score and w.risk_score < 30]),
        'medium': len([w for w in workers if w.risk_score and 30 <= w.risk_score < 60]),
        'high': len([w for w in workers if w.risk_score and w.risk_score >= 60])
    }

    # Top skills gaps (mock data)
    skills_gap_summary = {
        'most_common_gaps': [
            {'skill': 'Machine Learning', 'workers_lacking': int(total_employees * 0.7)},
            {'skill': 'Cloud Computing', 'workers_lacking': int(total_employees * 0.6)},
            {'skill': 'Data Analysis', 'workers_lacking': int(total_employees * 0.5)}
        ],
        'critical_gaps': [
            {'skill': 'Cybersecurity', 'urgency': 'high'},
            {'skill': 'AI/ML', 'urgency': 'high'}
        ]
    }

    # Recommended training programs
    recommended_training = [
        {
            'program': 'Cloud Architecture Certification',
            'target_employees': int(total_employees * 0.4),
            'estimated_cost': 500 * int(total_employees * 0.4),
            'roi_score': 8.5
        },
        {
            'program': 'Data Science Bootcamp',
            'target_employees': int(total_employees * 0.3),
            'estimated_cost': 1200 * int(total_employees * 0.3),
            'roi_score': 9.0
        }
    ]

    return {
        'enterprise_id': enterprise_id,
        'company_name': enterprise.company_name,
        'total_employees': total_employees,
        'high_risk_employees': high_risk_count,
        'avg_risk_score': round(avg_risk, 2),
        'risk_distribution': risk_distribution,
        'skills_gap_summary': skills_gap_summary,
        'recommended_training': recommended_training,
        'subscription_tier': enterprise.subscription_tier,
        'subscription_expires': enterprise.subscription_expires
    }

@router.get("/{enterprise_id}/workforce-planning")
def get_workforce_planning(enterprise_id: int, db: Session = Depends(get_db)):
    """
    Strategic workforce planning insights
    Predict future skill needs and automation impact
    """
    enterprise = db.query(Enterprise).filter(Enterprise.id == enterprise_id).first()
    if not enterprise:
        raise HTTPException(status_code=404, detail="Enterprise not found")

    # Mock workforce planning data
    return {
        'automation_impact_forecast': {
            'next_12_months': {
                'jobs_at_risk': 150,
                'automation_potential': 0.35
            },
            'next_24_months': {
                'jobs_at_risk': 280,
                'automation_potential': 0.52
            }
        },
        'emerging_skill_needs': [
            {'skill': 'AI/ML Engineering', 'demand_growth': '+125%'},
            {'skill': 'Cloud Architecture', 'demand_growth': '+95%'},
            {'skill': 'DevOps', 'demand_growth': '+80%'}
        ],
        'reskilling_priorities': [
            {
                'from_role': 'Data Entry Specialist',
                'to_role': 'Data Analyst',
                'affected_employees': 45,
                'reskilling_duration_weeks': 16
            },
            {
                'from_role': 'Manual QA Tester',
                'to_role': 'Automation Test Engineer',
                'affected_employees': 30,
                'reskilling_duration_weeks': 12
            }
        ]
    }

@router.post("/{enterprise_id}/bulk-assessment")
def bulk_risk_assessment(enterprise_id: int, worker_ids: List[int], db: Session = Depends(get_db)):
    """Run risk assessment for multiple workers"""
    # This would trigger risk assessment for all specified workers
    # For now, return a summary
    return {
        'enterprise_id': enterprise_id,
        'workers_assessed': len(worker_ids),
        'status': 'Assessment queued',
        'estimated_completion': '5 minutes'
    }
