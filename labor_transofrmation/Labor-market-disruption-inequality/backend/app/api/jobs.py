from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from app.db.database import get_db
from app.db.models import Job, JobSkill, Worker, WorkerSkill
from app.models.matcher import WorkerJobMatcher

router = APIRouter()
matcher = WorkerJobMatcher()

class JobCreate(BaseModel):
    title: str
    company: str
    industry: str
    location: str
    description: str
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    remote_friendly: bool = False

class JobResponse(BaseModel):
    id: int
    title: str
    company: str
    industry: str
    location: str
    salary_min: Optional[int]
    salary_max: Optional[int]
    remote_friendly: bool

    class Config:
        from_attributes = True

class MatchRequest(BaseModel):
    worker_id: int
    top_n: int = 10

@router.post("/", response_model=JobResponse)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    """Create a new job posting"""
    db_job = Job(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@router.get("/", response_model=List[JobResponse])
def list_jobs(
    skip: int = 0,
    limit: int = 20,
    industry: Optional[str] = None,
    remote_only: bool = False,
    db: Session = Depends(get_db)
):
    """List available job postings with filters"""
    query = db.query(Job)

    if industry:
        query = query.filter(Job.industry == industry)

    if remote_only:
        query = query.filter(Job.remote_friendly == True)

    jobs = query.offset(skip).limit(limit).all()
    return jobs

@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    """Get job details"""
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.post("/match")
def match_jobs_for_worker(request: MatchRequest, db: Session = Depends(get_db)):
    """
    Match jobs to a worker based on skills, location, and preferences
    Core feature: Matching displaced workers with new opportunities
    """
    # Get worker
    worker = db.query(Worker).filter(Worker.id == request.worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    # Get worker skills
    worker_skills_db = db.query(WorkerSkill).filter(
        WorkerSkill.worker_id == request.worker_id
    ).all()

    worker_skills = [
        {
            'skill_id': ws.skill_id,
            'proficiency_level': ws.proficiency_level
        }
        for ws in worker_skills_db
    ]

    # Get all active jobs
    jobs = db.query(Job).filter(
        Job.expires_at == None
    ).all() or db.query(Job).all()

    # Get skills for each job
    jobs_skills = {}
    for job in jobs:
        job_skills_db = db.query(JobSkill).filter(
            JobSkill.job_id == job.id
        ).all()
        jobs_skills[job.id] = [
            {
                'skill_id': js.skill_id,
                'required': js.required,
                'importance': js.importance
            }
            for js in job_skills_db
        ]

    # Convert worker to dict
    worker_dict = {
        'location': worker.location,
        'years_experience': worker.years_experience,
        'expected_salary': None  # TODO: Add to worker model
    }

    # Convert jobs to list of dicts
    jobs_list = [
        {
            'id': job.id,
            'title': job.title,
            'company': job.company,
            'location': job.location,
            'remote_friendly': job.remote_friendly,
            'salary_min': job.salary_min,
            'salary_max': job.salary_max,
            'required_experience': 0  # TODO: Add to job model
        }
        for job in jobs
    ]

    # Get ranked matches
    matches = matcher.rank_jobs_for_worker(
        worker_dict,
        worker_skills,
        jobs_list,
        jobs_skills,
        request.top_n
    )

    return {
        'worker_id': request.worker_id,
        'total_jobs_analyzed': len(jobs),
        'top_matches': matches
    }

@router.get("/{job_id}/match/{worker_id}")
def match_specific_job(job_id: int, worker_id: int, db: Session = Depends(get_db)):
    """Get detailed match analysis for a specific job and worker"""
    # Get worker
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    # Get job
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Get skills
    worker_skills = db.query(WorkerSkill).filter(
        WorkerSkill.worker_id == worker_id
    ).all()

    job_skills = db.query(JobSkill).filter(
        JobSkill.job_id == job_id
    ).all()

    worker_skills_list = [
        {'skill_id': ws.skill_id, 'proficiency_level': ws.proficiency_level}
        for ws in worker_skills
    ]

    job_skills_list = [
        {'skill_id': js.skill_id, 'required': js.required, 'importance': js.importance}
        for js in job_skills
    ]

    # Get match
    worker_dict = {
        'location': worker.location,
        'years_experience': worker.years_experience,
        'expected_salary': None
    }

    job_dict = {
        'id': job.id,
        'title': job.title,
        'location': job.location,
        'remote_friendly': job.remote_friendly,
        'salary_min': job.salary_min,
        'salary_max': job.salary_max,
        'required_experience': 0
    }

    match_result = matcher.match_worker_to_job(
        worker_dict,
        job_dict,
        worker_skills_list,
        job_skills_list
    )

    return {
        'job': job_dict,
        'worker_id': worker_id,
        'match_analysis': match_result
    }
