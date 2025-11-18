"""
Freelance Workers Hub API - Performance Optimized Version

Improvements over original:
- Database integration (replaces mock data)
- Caching for frequently accessed data
- Pagination for list endpoints
- Optimized database queries with eager loading
- Comprehensive error handling
- Query optimization with indexes
"""

from fastapi import APIRouter, HTTPException, Depends, Query as QueryParam
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, asc, and_, or_, func

from ..db.database import get_db
from ..db.models import (
    FreelanceProfile, FreelanceJobPosting, FreelanceProposal,
    FreelanceContract, FreelanceReview, FreelancePortfolioItem,
    FreelanceCategory, Worker
)
from ..models.freelance_hub import FreelanceHub
from ..agents.freelance_advisor_agent import FreelanceAdvisorAgent
from ..core.cache import cached, get_cache, invalidate_cache_pattern
from ..core.pagination import paginate, create_paginated_response

router = APIRouter()

# Initialize engines
freelance_hub = FreelanceHub()
advisor_agent = FreelanceAdvisorAgent()

# ==================== REQUEST/RESPONSE MODELS ====================

class FreelanceProfileCreate(BaseModel):
    worker_id: int
    title: str = Field(..., description="Professional title (e.g., 'Python Developer')")
    bio: str = Field(..., min_length=100, max_length=1000)
    hourly_rate: float = Field(..., ge=10, le=500)
    availability_hours_weekly: int = Field(..., ge=5, le=168)
    preferred_job_types: List[str] = Field(default=["one_time", "hourly"])
    min_project_budget: float = Field(default=0)
    languages: List[str] = Field(default=["English"])

class FreelanceProfileUpdate(BaseModel):
    title: Optional[str] = None
    bio: Optional[str] = None
    hourly_rate: Optional[float] = None
    availability_hours_weekly: Optional[int] = None
    is_available: Optional[bool] = None
    preferred_job_types: Optional[List[str]] = None
    min_project_budget: Optional[float] = None

class JobPostingCreate(BaseModel):
    client_id: int
    title: str = Field(..., min_length=10, max_length=200)
    description: str = Field(..., min_length=50)
    category_id: int
    budget_type: str = Field(..., pattern="^(fixed|hourly)$")
    budget_min: float = Field(..., ge=0)
    budget_max: float = Field(..., ge=0)
    duration_estimate: str
    deadline: Optional[datetime] = None
    required_skills: List[str]
    experience_level: str = Field(default="intermediate", pattern="^(beginner|intermediate|expert)$")
    visibility: str = Field(default="public", pattern="^(public|private|invited_only)$")

class ProposalCreate(BaseModel):
    job_posting_id: int
    freelancer_id: int
    cover_letter: str = Field(..., min_length=100, max_length=2000)
    proposed_rate: float = Field(..., ge=0)
    proposed_duration: str
    delivery_date: Optional[datetime] = None

class ProposalUpdate(BaseModel):
    cover_letter: Optional[str] = None
    proposed_rate: Optional[float] = None
    proposed_duration: Optional[str] = None
    status: Optional[str] = None

class ContractCreate(BaseModel):
    job_posting_id: int
    proposal_id: int
    freelancer_id: int
    client_id: int
    agreed_rate: float
    payment_type: str = Field(..., pattern="^(fixed|hourly|milestone)$")
    total_amount: float
    milestones: Optional[List[Dict]] = None
    deadline: Optional[datetime] = None

class ContractUpdate(BaseModel):
    status: Optional[str] = None
    progress_percentage: Optional[int] = Field(None, ge=0, le=100)
    amount_paid: Optional[float] = None
    milestones: Optional[List[Dict]] = None

class ReviewCreate(BaseModel):
    contract_id: int
    freelancer_id: int
    client_id: int
    rating: float = Field(..., ge=1, le=5)
    review_text: str = Field(..., min_length=50, max_length=1000)
    quality_rating: Optional[float] = Field(None, ge=1, le=5)
    communication_rating: Optional[float] = Field(None, ge=1, le=5)
    professionalism_rating: Optional[float] = Field(None, ge=1, le=5)
    deadline_rating: Optional[float] = Field(None, ge=1, le=5)
    value_rating: Optional[float] = Field(None, ge=1, le=5)
    would_recommend: bool = True
    would_hire_again: bool = True

class PortfolioItemCreate(BaseModel):
    freelancer_id: int
    title: str
    description: str
    category: str
    tags: List[str]
    thumbnail_url: Optional[str] = None
    images: Optional[List[str]] = None
    video_url: Optional[str] = None
    live_url: Optional[str] = None
    github_url: Optional[str] = None

# ==================== HELPER FUNCTIONS ====================

def profile_to_dict(profile: FreelanceProfile) -> dict:
    """Convert FreelanceProfile ORM model to dictionary"""
    return {
        "id": profile.id,
        "worker_id": profile.worker_id,
        "title": profile.title,
        "bio": profile.bio,
        "hourly_rate": profile.hourly_rate,
        "availability_hours_weekly": profile.availability_hours_weekly,
        "rating_average": profile.rating_average,
        "total_reviews": profile.total_reviews,
        "total_jobs_completed": profile.total_jobs_completed,
        "total_earnings": profile.total_earnings,
        "success_rate": profile.success_rate,
        "response_time_hours": profile.response_time_hours,
        "verified": profile.verified,
        "top_rated": profile.top_rated,
        "badges": profile.badges or [],
        "preferred_job_types": profile.preferred_job_types or [],
        "min_project_budget": profile.min_project_budget,
        "languages": profile.languages or [],
        "is_active": profile.is_active,
        "is_available": profile.is_available,
        "created_at": profile.created_at.isoformat() if profile.created_at else None,
        "updated_at": profile.updated_at.isoformat() if profile.updated_at else None
    }

def job_to_dict(job: FreelanceJobPosting) -> dict:
    """Convert FreelanceJobPosting ORM model to dictionary"""
    return {
        "id": job.id,
        "title": job.title,
        "description": job.description,
        "category_id": job.category_id,
        "budget_type": job.budget_type,
        "budget_min": job.budget_min,
        "budget_max": job.budget_max,
        "duration_estimate": job.duration_estimate,
        "deadline": job.deadline.isoformat() if job.deadline else None,
        "required_skills": job.required_skills or [],
        "experience_level": job.experience_level,
        "status": job.status,
        "visibility": job.visibility,
        "views_count": job.views_count,
        "proposals_count": job.proposals_count,
        "posted_at": job.posted_at.isoformat() if job.posted_at else None,
        "client_id": job.client_id
    }

# ==================== PROFILE ENDPOINTS ====================

@router.post("/profile/create")
def create_freelance_profile(profile: FreelanceProfileCreate, db: Session = Depends(get_db)):
    """Create a new freelance profile for a worker"""
    try:
        # Check if worker exists
        worker = db.query(Worker).filter(Worker.id == profile.worker_id).first()
        if not worker:
            raise HTTPException(status_code=404, detail="Worker not found")

        # Check if profile already exists
        existing = db.query(FreelanceProfile).filter(
            FreelanceProfile.worker_id == profile.worker_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Freelance profile already exists for this worker")

        # Create new profile
        new_profile = FreelanceProfile(
            worker_id=profile.worker_id,
            title=profile.title,
            bio=profile.bio,
            hourly_rate=profile.hourly_rate,
            availability_hours_weekly=profile.availability_hours_weekly,
            preferred_job_types=profile.preferred_job_types,
            min_project_budget=profile.min_project_budget,
            languages=profile.languages,
            is_active=True,
            is_available=True
        )

        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)

        # Invalidate related caches
        invalidate_cache_pattern(f"freelancer_{profile.worker_id}")

        return {
            "status": "success",
            "message": "Freelance profile created successfully",
            "profile": profile_to_dict(new_profile),
            "next_steps": [
                "Add portfolio items",
                "Complete skill verification",
                "Start applying to jobs"
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create profile: {str(e)}")

@router.get("/profile/{freelancer_id}")
@cached(ttl_seconds=300, category="profile", key_prefix="freelance_")
def get_freelance_profile(freelancer_id: int, db: Session = Depends(get_db)):
    """Get freelance profile details with caching"""
    try:
        profile = db.query(FreelanceProfile).options(
            joinedload(FreelanceProfile.worker)
        ).filter(FreelanceProfile.id == freelancer_id).first()

        if not profile:
            raise HTTPException(status_code=404, detail="Freelance profile not found")

        profile_data = profile_to_dict(profile)

        # Add worker name if available
        if profile.worker:
            profile_data["name"] = profile.worker.name

        return {
            "status": "success",
            "profile": profile_data
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch profile: {str(e)}")

@router.put("/profile/{freelancer_id}")
def update_freelance_profile(
    freelancer_id: int,
    updates: FreelanceProfileUpdate,
    db: Session = Depends(get_db)
):
    """Update freelance profile"""
    try:
        profile = db.query(FreelanceProfile).filter(
            FreelanceProfile.id == freelancer_id
        ).first()

        if not profile:
            raise HTTPException(status_code=404, detail="Freelance profile not found")

        # Update fields
        update_data = updates.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(profile, field, value)

        profile.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(profile)

        # Invalidate cache
        invalidate_cache_pattern(f"freelancer_{freelancer_id}")

        return {
            "status": "success",
            "message": "Profile updated successfully",
            "updated_fields": list(update_data.keys()),
            "profile": profile_to_dict(profile)
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update profile: {str(e)}")

# ==================== JOB POSTING ENDPOINTS ====================

@router.post("/jobs/post")
def create_job_posting(job: JobPostingCreate, db: Session = Depends(get_db)):
    """Create a new freelance job posting"""
    try:
        # Validate client exists
        client = db.query(Worker).filter(Worker.id == job.client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")

        # Validate category exists
        category = db.query(FreelanceCategory).filter(
            FreelanceCategory.id == job.category_id
        ).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        # Create job posting
        new_job = FreelanceJobPosting(
            client_id=job.client_id,
            title=job.title,
            description=job.description,
            category_id=job.category_id,
            budget_type=job.budget_type,
            budget_min=job.budget_min,
            budget_max=job.budget_max,
            duration_estimate=job.duration_estimate,
            deadline=job.deadline,
            required_skills=job.required_skills,
            experience_level=job.experience_level,
            visibility=job.visibility,
            status="open"
        )

        db.add(new_job)
        db.commit()
        db.refresh(new_job)

        # Update category job count
        category.job_count = db.query(FreelanceJobPosting).filter(
            FreelanceJobPosting.category_id == job.category_id,
            FreelanceJobPosting.status == "open"
        ).count()
        db.commit()

        # Invalidate job listings cache
        invalidate_cache_pattern("jobs_search")
        invalidate_cache_pattern("marketplace_")

        return {
            "status": "success",
            "message": "Job posted successfully",
            "job_id": new_job.id,
            "job": job_to_dict(new_job)
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create job: {str(e)}")

@router.get("/jobs/search")
def search_jobs(
    category_id: Optional[int] = None,
    budget_min: Optional[float] = None,
    budget_max: Optional[float] = None,
    experience_level: Optional[str] = None,
    status: str = "open",
    page: int = QueryParam(default=1, ge=1),
    page_size: int = QueryParam(default=20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Search for freelance jobs with pagination and filtering"""
    try:
        # Build query
        query = db.query(FreelanceJobPosting).filter(
            FreelanceJobPosting.status == status
        )

        # Apply filters
        if category_id:
            query = query.filter(FreelanceJobPosting.category_id == category_id)

        if budget_min:
            query = query.filter(FreelanceJobPosting.budget_max >= budget_min)

        if budget_max:
            query = query.filter(FreelanceJobPosting.budget_min <= budget_max)

        if experience_level:
            query = query.filter(FreelanceJobPosting.experience_level == experience_level)

        # Order by most recent
        query = query.order_by(desc(FreelanceJobPosting.posted_at))

        # Paginate
        items, total_count, pagination = paginate(query, page=page, page_size=page_size)

        # Convert to dicts
        jobs = [job_to_dict(job) for job in items]

        return create_paginated_response(jobs, total_count, page, page_size)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search jobs: {str(e)}")

@router.get("/jobs/{job_id}")
@cached(ttl_seconds=60, category="jobs", key_prefix="job_")
def get_job_details(job_id: int, db: Session = Depends(get_db)):
    """Get detailed information about a job posting"""
    try:
        job = db.query(FreelanceJobPosting).options(
            joinedload(FreelanceJobPosting.category),
            joinedload(FreelanceJobPosting.client)
        ).filter(FreelanceJobPosting.id == job_id).first()

        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

        # Increment view count (async in production)
        job.views_count += 1
        db.commit()

        job_data = job_to_dict(job)

        # Add additional details
        if job.category:
            job_data["category_name"] = job.category.name

        if job.client:
            job_data["client_name"] = job.client.name

        return {
            "status": "success",
            "job": job_data
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch job: {str(e)}")

# ==================== PROPOSAL ENDPOINTS ====================

@router.post("/proposals/create")
def submit_proposal(proposal: ProposalCreate, db: Session = Depends(get_db)):
    """Submit a proposal for a job posting"""
    try:
        # Validate job exists and is open
        job = db.query(FreelanceJobPosting).filter(
            FreelanceJobPosting.id == proposal.job_posting_id,
            FreelanceJobPosting.status == "open"
        ).first()

        if not job:
            raise HTTPException(status_code=404, detail="Job not found or not accepting proposals")

        # Validate freelancer exists
        freelancer = db.query(FreelanceProfile).filter(
            FreelanceProfile.id == proposal.freelancer_id
        ).first()

        if not freelancer:
            raise HTTPException(status_code=404, detail="Freelancer profile not found")

        # Check for duplicate proposal
        existing = db.query(FreelanceProposal).filter(
            FreelanceProposal.job_posting_id == proposal.job_posting_id,
            FreelanceProposal.freelancer_id == proposal.freelancer_id,
            FreelanceProposal.status.in_(["pending", "accepted"])
        ).first()

        if existing:
            raise HTTPException(status_code=400, detail="You already have an active proposal for this job")

        # Create proposal
        new_proposal = FreelanceProposal(
            job_posting_id=proposal.job_posting_id,
            freelancer_id=proposal.freelancer_id,
            cover_letter=proposal.cover_letter,
            proposed_rate=proposal.proposed_rate,
            proposed_duration=proposal.proposed_duration,
            delivery_date=proposal.delivery_date,
            status="pending"
        )

        db.add(new_proposal)

        # Update job proposals count
        job.proposals_count += 1

        db.commit()
        db.refresh(new_proposal)

        # Invalidate caches
        invalidate_cache_pattern(f"job_{proposal.job_posting_id}")
        invalidate_cache_pattern(f"proposals_freelancer_{proposal.freelancer_id}")

        return {
            "status": "success",
            "message": "Proposal submitted successfully",
            "proposal_id": new_proposal.id,
            "submitted_at": new_proposal.submitted_at.isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to submit proposal: {str(e)}")

@router.get("/proposals/freelancer/{freelancer_id}")
def get_freelancer_proposals(
    freelancer_id: int,
    status: Optional[str] = None,
    page: int = QueryParam(default=1, ge=1),
    page_size: int = QueryParam(default=20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all proposals for a freelancer with pagination"""
    try:
        query = db.query(FreelanceProposal).options(
            joinedload(FreelanceProposal.job_posting)
        ).filter(FreelanceProposal.freelancer_id == freelancer_id)

        if status:
            query = query.filter(FreelanceProposal.status == status)

        query = query.order_by(desc(FreelanceProposal.submitted_at))

        # Paginate
        items, total_count, pagination = paginate(query, page=page, page_size=page_size)

        # Convert to dicts
        proposals = []
        for p in items:
            proposals.append({
                "id": p.id,
                "job_id": p.job_posting_id,
                "job_title": p.job_posting.title if p.job_posting else "Unknown",
                "proposed_rate": p.proposed_rate,
                "proposed_duration": p.proposed_duration,
                "status": p.status,
                "submitted_at": p.submitted_at.isoformat() if p.submitted_at else None
            })

        # Get stats
        stats = {
            "pending": db.query(FreelanceProposal).filter(
                FreelanceProposal.freelancer_id == freelancer_id,
                FreelanceProposal.status == "pending"
            ).count(),
            "accepted": db.query(FreelanceProposal).filter(
                FreelanceProposal.freelancer_id == freelancer_id,
                FreelanceProposal.status == "accepted"
            ).count(),
            "rejected": db.query(FreelanceProposal).filter(
                FreelanceProposal.freelancer_id == freelancer_id,
                FreelanceProposal.status == "rejected"
            ).count()
        }

        response = create_paginated_response(proposals, total_count, page, page_size)
        response["stats"] = stats

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch proposals: {str(e)}")

# ==================== CONTRACT ENDPOINTS ====================

@router.post("/contracts/create")
def create_contract(contract: ContractCreate, db: Session = Depends(get_db)):
    """Create a new contract (accept a proposal)"""
    try:
        # Validate proposal exists and is pending
        proposal = db.query(FreelanceProposal).filter(
            FreelanceProposal.id == contract.proposal_id,
            FreelanceProposal.status == "pending"
        ).first()

        if not proposal:
            raise HTTPException(status_code=404, detail="Proposal not found or already processed")

        # Create contract
        new_contract = FreelanceContract(
            job_posting_id=contract.job_posting_id,
            proposal_id=contract.proposal_id,
            freelancer_id=contract.freelancer_id,
            client_id=contract.client_id,
            agreed_rate=contract.agreed_rate,
            payment_type=contract.payment_type,
            total_amount=contract.total_amount,
            escrow_amount=contract.total_amount,  # Full amount in escrow
            milestones=contract.milestones,
            deadline=contract.deadline,
            status="active"
        )

        db.add(new_contract)

        # Update proposal status
        proposal.status = "accepted"

        # Update job status
        job = db.query(FreelanceJobPosting).filter(
            FreelanceJobPosting.id == contract.job_posting_id
        ).first()
        if job:
            job.status = "in_progress"
            job.started_at = datetime.utcnow()
            job.freelancer_id = contract.freelancer_id

        db.commit()
        db.refresh(new_contract)

        # Invalidate caches
        invalidate_cache_pattern(f"job_{contract.job_posting_id}")
        invalidate_cache_pattern(f"freelancer_{contract.freelancer_id}")
        invalidate_cache_pattern(f"proposals_")

        return {
            "status": "success",
            "message": "Contract created successfully",
            "contract_id": new_contract.id,
            "next_steps": [
                "Freelancer will be notified",
                "Set up milestones if applicable",
                "Establish communication channel"
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create contract: {str(e)}")

@router.get("/contracts/freelancer/{freelancer_id}")
def get_freelancer_contracts(
    freelancer_id: int,
    status: Optional[str] = None,
    page: int = QueryParam(default=1, ge=1),
    page_size: int = QueryParam(default=20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all contracts for a freelancer with pagination"""
    try:
        query = db.query(FreelanceContract).options(
            joinedload(FreelanceContract.job_posting),
            joinedload(FreelanceContract.client)
        ).filter(FreelanceContract.freelancer_id == freelancer_id)

        if status:
            query = query.filter(FreelanceContract.status == status)

        query = query.order_by(desc(FreelanceContract.started_at))

        # Paginate
        items, total_count, pagination = paginate(query, page=page, page_size=page_size)

        # Convert to dicts
        contracts = []
        for c in items:
            contracts.append({
                "id": c.id,
                "job_title": c.job_posting.title if c.job_posting else "Unknown",
                "client_name": c.client.name if c.client else "Unknown",
                "total_amount": c.total_amount,
                "payment_type": c.payment_type,
                "status": c.status,
                "progress_percentage": c.progress_percentage,
                "started_at": c.started_at.isoformat() if c.started_at else None,
                "deadline": c.deadline.isoformat() if c.deadline else None
            })

        # Calculate stats
        all_completed = db.query(FreelanceContract).filter(
            FreelanceContract.freelancer_id == freelancer_id,
            FreelanceContract.status == "completed"
        ).all()

        stats = {
            "active": db.query(FreelanceContract).filter(
                FreelanceContract.freelancer_id == freelancer_id,
                FreelanceContract.status == "active"
            ).count(),
            "completed": len(all_completed),
            "total_earned": sum(c.amount_paid for c in all_completed)
        }

        response = create_paginated_response(contracts, total_count, page, page_size)
        response["stats"] = stats

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch contracts: {str(e)}")

# ==================== DASHBOARD & ANALYTICS ====================

@router.get("/dashboard/freelancer/{freelancer_id}")
@cached(ttl_seconds=120, category="dashboard", key_prefix="freelancer_dash_")
def get_freelancer_dashboard(freelancer_id: int, db: Session = Depends(get_db)):
    """Get comprehensive freelancer dashboard data with caching"""
    try:
        # Get freelancer profile
        profile = db.query(FreelanceProfile).options(
            joinedload(FreelanceProfile.worker)
        ).filter(FreelanceProfile.id == freelancer_id).first()

        if not profile:
            raise HTTPException(status_code=404, detail="Freelancer not found")

        # Get active contracts
        active_contracts = db.query(FreelanceContract).filter(
            FreelanceContract.freelancer_id == freelancer_id,
            FreelanceContract.status == "active"
        ).count()

        # Get pending proposals
        pending_proposals = db.query(FreelanceProposal).filter(
            FreelanceProposal.freelancer_id == freelancer_id,
            FreelanceProposal.status == "pending"
        ).count()

        # Calculate this month's earnings
        from datetime import datetime, timedelta
        month_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        this_month_earnings = db.query(func.sum(FreelanceContract.amount_paid)).filter(
            FreelanceContract.freelancer_id == freelancer_id,
            FreelanceContract.completed_at >= month_start
        ).scalar() or 0

        # Get recent reviews
        recent_reviews = db.query(FreelanceReview).options(
            joinedload(FreelanceReview.client)
        ).filter(
            FreelanceReview.freelancer_id == freelancer_id
        ).order_by(desc(FreelanceReview.created_at)).limit(5).all()

        reviews_data = [{
            "id": r.id,
            "rating": r.rating,
            "review_text": r.review_text,
            "client_name": r.client.name if r.client else "Unknown",
            "created_at": r.created_at.isoformat() if r.created_at else None
        } for r in recent_reviews]

        return {
            "status": "success",
            "profile": profile_to_dict(profile),
            "metrics": {
                "total_earnings": profile.total_earnings,
                "jobs_completed": profile.total_jobs_completed,
                "success_rate": profile.success_rate,
                "avg_rating": profile.rating_average
            },
            "active_contracts": active_contracts,
            "pending_proposals": pending_proposals,
            "this_month_earnings": float(this_month_earnings),
            "recent_reviews": reviews_data
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch dashboard: {str(e)}")

@router.get("/analytics/marketplace")
@cached(ttl_seconds=300, category="marketplace", key_prefix="marketplace_analytics_")
def get_marketplace_analytics(db: Session = Depends(get_db)):
    """Get overall marketplace analytics with caching"""
    try:
        total_freelancers = db.query(FreelanceProfile).count()
        active_freelancers = db.query(FreelanceProfile).filter(
            FreelanceProfile.is_available == True
        ).count()

        total_jobs_posted = db.query(FreelanceJobPosting).count()
        open_jobs = db.query(FreelanceJobPosting).filter(
            FreelanceJobPosting.status == "open"
        ).count()

        total_earnings = db.query(func.sum(FreelanceContract.amount_paid)).scalar() or 0

        # Average hourly rate
        avg_hourly_rate = db.query(func.avg(FreelanceProfile.hourly_rate)).filter(
            FreelanceProfile.is_active == True
        ).scalar() or 0

        # Top categories
        top_categories = db.query(
            FreelanceCategory.name,
            FreelanceCategory.job_count,
            func.avg(FreelanceProfile.hourly_rate).label("avg_rate")
        ).join(
            FreelanceJobPosting, FreelanceJobPosting.category_id == FreelanceCategory.id
        ).join(
            FreelanceProfile, FreelanceJobPosting.freelancer_id == FreelanceProfile.id, isouter=True
        ).group_by(
            FreelanceCategory.id, FreelanceCategory.name, FreelanceCategory.job_count
        ).order_by(
            desc(FreelanceCategory.job_count)
        ).limit(5).all()

        categories_data = [{
            "name": cat.name,
            "job_count": cat.job_count,
            "avg_rate": float(cat.avg_rate) if cat.avg_rate else 0
        } for cat in top_categories]

        return {
            "status": "success",
            "total_freelancers": total_freelancers,
            "active_freelancers": active_freelancers,
            "total_jobs_posted": total_jobs_posted,
            "open_jobs": open_jobs,
            "total_earnings_platform": float(total_earnings),
            "avg_hourly_rate": float(avg_hourly_rate),
            "top_categories": categories_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch analytics: {str(e)}")

# ==================== CACHE MANAGEMENT ====================

@router.post("/admin/cache/clear")
def clear_cache():
    """Clear all cache (admin only - add auth in production)"""
    cache = get_cache()
    cache.clear()
    return {
        "status": "success",
        "message": "Cache cleared successfully"
    }

@router.get("/admin/cache/stats")
def get_cache_stats():
    """Get cache statistics (admin only - add auth in production)"""
    cache = get_cache()
    stats = cache.get_stats()
    return {
        "status": "success",
        "cache_stats": stats
    }
