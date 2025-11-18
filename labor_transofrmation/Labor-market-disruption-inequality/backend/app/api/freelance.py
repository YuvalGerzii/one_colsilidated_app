"""
Freelance Workers Hub API

REST API endpoints for the freelance platform including:
- Profile management
- Job posting and discovery
- Proposal submission
- Contract management
- Reviews and ratings
- AI-powered advisory
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

from ..models.freelance_hub import FreelanceHub
from ..agents.freelance_advisor_agent import FreelanceAdvisorAgent

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

# ==================== PROFILE ENDPOINTS ====================

@router.post("/profile/create")
def create_freelance_profile(profile: FreelanceProfileCreate):
    """Create a new freelance profile for a worker"""
    try:
        # In a real implementation, this would save to database
        return {
            "status": "success",
            "message": "Freelance profile created successfully",
            "profile": profile.dict(),
            "next_steps": [
                "Add portfolio items",
                "Complete skill verification",
                "Start applying to jobs"
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/profile/{freelancer_id}")
def get_freelance_profile(freelancer_id: int):
    """Get freelance profile details"""
    # Mock data - in real implementation, fetch from database
    return {
        "id": freelancer_id,
        "name": "Sample Freelancer",
        "title": "Full-Stack Developer",
        "bio": "Experienced developer with 5+ years in web development...",
        "hourly_rate": 75,
        "rating_average": 4.8,
        "total_jobs_completed": 45,
        "success_rate": 96,
        "badges": ["top_rated", "reliable_delivery"],
        "is_available": True
    }

@router.put("/profile/{freelancer_id}")
def update_freelance_profile(freelancer_id: int, updates: FreelanceProfileUpdate):
    """Update freelance profile"""
    try:
        return {
            "status": "success",
            "message": "Profile updated successfully",
            "updated_fields": [k for k, v in updates.dict(exclude_unset=True).items()]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/profile/{freelancer_id}/optimize")
def optimize_profile(freelancer_id: int):
    """Get AI-powered profile optimization recommendations"""
    try:
        # Mock freelancer data
        freelancer = {
            "id": freelancer_id,
            "bio": "Developer",
            "hourly_rate": 50,
            "skills": ["python", "javascript"],
            "portfolio_items": [],
            "is_available": True
        }

        # Use advisor agent to analyze and optimize
        response = advisor_agent.process_task({
            "type": "optimize_profile",
            "freelancer": freelancer,
            "market_data": {}
        })

        return {
            "status": "success",
            "optimization": response.data,
            "confidence": response.confidence,
            "recommendations": response.recommendations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== JOB POSTING ENDPOINTS ====================

@router.post("/jobs/post")
def create_job_posting(job: JobPostingCreate):
    """Create a new freelance job posting"""
    try:
        return {
            "status": "success",
            "message": "Job posted successfully",
            "job_id": 12345,
            "job": job.dict(),
            "estimated_reach": "50-100 qualified freelancers",
            "expected_proposals": "10-20 within 48 hours"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/jobs/search")
def search_jobs(
    category: Optional[str] = None,
    budget_min: Optional[float] = None,
    budget_max: Optional[float] = None,
    experience_level: Optional[str] = None,
    status: str = "open",
    limit: int = 20
):
    """Search for freelance jobs"""
    # Mock job data
    jobs = [
        {
            "id": 1,
            "title": "Build a responsive landing page",
            "description": "Need a modern landing page for our startup...",
            "category": "web_development",
            "budget_type": "fixed",
            "budget_max": 500,
            "experience_level": "intermediate",
            "proposals_count": 8,
            "posted_at": datetime.utcnow().isoformat()
        }
    ]

    return {
        "status": "success",
        "total_results": len(jobs),
        "jobs": jobs,
        "filters_applied": {
            "category": category,
            "budget_range": f"${budget_min}-${budget_max}" if budget_min else "any",
            "experience_level": experience_level or "any"
        }
    }

@router.get("/jobs/{job_id}")
def get_job_details(job_id: int):
    """Get detailed information about a job posting"""
    return {
        "id": job_id,
        "title": "Build a responsive landing page",
        "description": "Need a modern landing page for our startup with React...",
        "category": "web_development",
        "budget_type": "fixed",
        "budget_max": 500,
        "budget_min": 300,
        "required_skills": ["react", "css", "responsive_design"],
        "experience_level": "intermediate",
        "status": "open",
        "client_name": "TechStartup Inc.",
        "proposals_count": 8,
        "views_count": 156,
        "posted_at": datetime.utcnow().isoformat()
    }

@router.post("/jobs/{job_id}/recommend-freelancers")
def recommend_freelancers_for_job(job_id: int):
    """Get recommended freelancers for a job posting"""
    try:
        # Mock data
        job_posting = {
            "id": job_id,
            "title": "Build landing page",
            "required_skills": ["react", "css"],
            "budget_max": 500,
            "budget_min": 300,
            "experience_level": "intermediate"
        }

        freelancers = [
            {
                "id": 1,
                "name": "John Doe",
                "hourly_rate": 60,
                "rating_average": 4.8,
                "skills": ["react", "css", "javascript"],
                "total_jobs_completed": 45,
                "success_rate": 96,
                "is_available": True,
                "response_time_hours": 6,
                "badges": ["top_rated"]
            }
        ]

        matches = freelance_hub.match_freelancers_to_job(job_posting, freelancers)

        return {
            "status": "success",
            "job_id": job_id,
            "total_matches": len(matches),
            "top_matches": matches[:10],
            "recommendations": [
                "Review top 5 candidates carefully",
                "Consider inviting top matches directly",
                "Look for verified badges and high ratings"
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== PROPOSAL ENDPOINTS ====================

@router.post("/proposals/create")
def submit_proposal(proposal: ProposalCreate):
    """Submit a proposal for a job posting"""
    try:
        return {
            "status": "success",
            "message": "Proposal submitted successfully",
            "proposal_id": 789,
            "proposal": proposal.dict(),
            "estimated_response_time": "24-48 hours",
            "tips": [
                "Client typically responds within 2 days",
                "Follow up if no response after 5 days",
                "Be ready to answer questions quickly"
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/proposals/freelancer/{freelancer_id}")
def get_freelancer_proposals(
    freelancer_id: int,
    status: Optional[str] = None,
    limit: int = 20
):
    """Get all proposals for a freelancer"""
    # Mock proposal data
    proposals = [
        {
            "id": 1,
            "job_title": "Build landing page",
            "proposed_rate": 400,
            "status": "pending",
            "submitted_at": datetime.utcnow().isoformat(),
            "job_id": 123
        }
    ]

    return {
        "status": "success",
        "freelancer_id": freelancer_id,
        "total_proposals": len(proposals),
        "proposals": proposals,
        "stats": {
            "pending": 5,
            "accepted": 2,
            "rejected": 3
        }
    }

@router.post("/proposals/{proposal_id}/generate-template")
def generate_proposal_template(proposal_id: int, freelancer_id: int, job_id: int):
    """Generate AI-powered proposal template"""
    try:
        # Mock data
        freelancer = {
            "id": freelancer_id,
            "name": "John Doe",
            "hourly_rate": 75,
            "rating_average": 4.8,
            "total_jobs_completed": 45,
            "skills": ["react", "python", "css"]
        }

        job_posting = {
            "id": job_id,
            "title": "Build responsive landing page",
            "required_skills": ["react", "css"],
            "budget_type": "fixed",
            "budget_max": 500
        }

        template = freelance_hub.generate_proposal_template(freelancer, job_posting)

        return {
            "status": "success",
            "template": template,
            "personalization_tips": [
                "Mention specific details from job description",
                "Include relevant portfolio links",
                "Address client's pain points"
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/proposals/{proposal_id}")
def update_proposal(proposal_id: int, updates: ProposalUpdate):
    """Update an existing proposal"""
    try:
        return {
            "status": "success",
            "message": "Proposal updated successfully",
            "proposal_id": proposal_id
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ==================== CONTRACT ENDPOINTS ====================

@router.post("/contracts/create")
def create_contract(contract: ContractCreate):
    """Create a new contract (accept a proposal)"""
    try:
        return {
            "status": "success",
            "message": "Contract created successfully",
            "contract_id": 456,
            "contract": contract.dict(),
            "next_steps": [
                "Freelancer will be notified",
                "Set up milestones if applicable",
                "Establish communication channel"
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/contracts/freelancer/{freelancer_id}")
def get_freelancer_contracts(
    freelancer_id: int,
    status: Optional[str] = None,
    limit: int = 20
):
    """Get all contracts for a freelancer"""
    contracts = [
        {
            "id": 1,
            "job_title": "Landing page development",
            "client_name": "TechStartup Inc.",
            "total_amount": 450,
            "payment_type": "fixed",
            "status": "active",
            "progress_percentage": 60,
            "started_at": datetime.utcnow().isoformat(),
            "deadline": (datetime.utcnow()).isoformat()
        }
    ]

    return {
        "status": "success",
        "freelancer_id": freelancer_id,
        "total_contracts": len(contracts),
        "contracts": contracts,
        "stats": {
            "active": 2,
            "completed": 15,
            "total_earned": 12500
        }
    }

@router.put("/contracts/{contract_id}")
def update_contract(contract_id: int, updates: ContractUpdate):
    """Update contract status or progress"""
    try:
        return {
            "status": "success",
            "message": "Contract updated successfully",
            "contract_id": contract_id,
            "updates": updates.dict(exclude_unset=True)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/contracts/{contract_id}/complete")
def complete_contract(contract_id: int):
    """Mark contract as completed"""
    try:
        return {
            "status": "success",
            "message": "Contract completed successfully",
            "contract_id": contract_id,
            "next_steps": [
                "Request client review",
                "Add to portfolio if notable",
                "Invoice for final payment"
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ==================== REVIEW ENDPOINTS ====================

@router.post("/reviews/create")
def submit_review(review: ReviewCreate):
    """Submit a review for a completed contract"""
    try:
        return {
            "status": "success",
            "message": "Review submitted successfully",
            "review_id": 321,
            "review": review.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/reviews/freelancer/{freelancer_id}")
def get_freelancer_reviews(freelancer_id: int, limit: int = 20):
    """Get all reviews for a freelancer"""
    reviews = [
        {
            "id": 1,
            "rating": 5.0,
            "review_text": "Excellent work! Delivered ahead of schedule.",
            "quality_rating": 5.0,
            "communication_rating": 5.0,
            "client_name": "TechStartup Inc.",
            "created_at": datetime.utcnow().isoformat()
        }
    ]

    return {
        "status": "success",
        "freelancer_id": freelancer_id,
        "total_reviews": len(reviews),
        "reviews": reviews,
        "summary": {
            "average_rating": 4.8,
            "total_reviews": 42,
            "5_star": 35,
            "4_star": 5,
            "3_star": 2
        }
    }

# ==================== PORTFOLIO ENDPOINTS ====================

@router.post("/portfolio/create")
def create_portfolio_item(item: PortfolioItemCreate):
    """Add a portfolio item"""
    try:
        return {
            "status": "success",
            "message": "Portfolio item added successfully",
            "item_id": 999,
            "item": item.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/portfolio/freelancer/{freelancer_id}")
def get_freelancer_portfolio(freelancer_id: int):
    """Get all portfolio items for a freelancer"""
    portfolio = [
        {
            "id": 1,
            "title": "E-commerce Website Redesign",
            "description": "Complete redesign of an e-commerce platform...",
            "category": "web_development",
            "tags": ["react", "ecommerce", "ui/ux"],
            "thumbnail_url": "https://example.com/thumb.jpg",
            "views_count": 234,
            "likes_count": 12
        }
    ]

    return {
        "status": "success",
        "freelancer_id": freelancer_id,
        "total_items": len(portfolio),
        "portfolio": portfolio
    }

# ==================== AI ADVISORY ENDPOINTS ====================

@router.post("/advisor/job-recommendations/{freelancer_id}")
def get_job_recommendations(freelancer_id: int, limit: int = 10):
    """Get AI-powered job recommendations for a freelancer"""
    try:
        # Mock data
        freelancer = {
            "id": freelancer_id,
            "hourly_rate": 75,
            "skills": ["python", "react", "nodejs"],
            "is_available": True,
            "min_project_budget": 200
        }

        available_jobs = [
            {
                "id": 1,
                "title": "Python automation script",
                "required_skills": ["python"],
                "budget_max": 300,
                "status": "open",
                "proposals_count": 5,
                "deadline": datetime.utcnow(),
                "client_name": "Corp Inc."
            }
        ]

        recommendations = freelance_hub.recommend_jobs_for_freelancer(
            freelancer,
            available_jobs,
            limit
        )

        # Use advisor for strategic insights
        response = advisor_agent.process_task({
            "type": "recommend_jobs",
            "freelancer": freelancer,
            "available_jobs": available_jobs,
            "limit": limit
        })

        return {
            "status": "success",
            "recommendations": recommendations,
            "strategic_insights": response.data,
            "next_steps": response.next_steps
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/advisor/pricing-optimization/{freelancer_id}")
def optimize_pricing(freelancer_id: int):
    """Get AI-powered pricing optimization recommendations"""
    try:
        # Mock data
        freelancer = {
            "id": freelancer_id,
            "hourly_rate": 50,
            "rating_average": 4.7,
            "total_jobs_completed": 30,
            "success_rate": 94,
            "primary_category": "web_development"
        }

        contracts = []  # Would fetch from DB

        response = advisor_agent.process_task({
            "type": "optimize_pricing",
            "freelancer": freelancer,
            "market_data": {},
            "contracts": contracts
        })

        return {
            "status": "success",
            "pricing_analysis": response.data,
            "confidence": response.confidence,
            "recommendations": response.recommendations,
            "next_steps": response.next_steps
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/advisor/analyze-competition/{job_id}")
def analyze_job_competition(job_id: int, freelancer_id: int):
    """Analyze competition for a specific job"""
    try:
        # Mock data
        job_posting = {
            "id": job_id,
            "title": "Build landing page",
            "budget_max": 500
        }

        proposals = []  # Would fetch existing proposals

        freelancer = {
            "id": freelancer_id,
            "hourly_rate": 75,
            "rating_average": 4.8,
            "total_jobs_completed": 45
        }

        response = advisor_agent.process_task({
            "type": "analyze_competition",
            "job_posting": job_posting,
            "proposals": proposals,
            "freelancer": freelancer
        })

        return {
            "status": "success",
            "competition_analysis": response.data,
            "win_probability": response.data.get("win_probability", 0.5),
            "strategy": response.data.get("competitive_strategy", {}),
            "next_steps": response.next_steps
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/advisor/growth-strategy/{freelancer_id}")
def get_growth_strategy(freelancer_id: int, annual_income_goal: Optional[float] = None):
    """Get long-term freelance career growth strategy"""
    try:
        # Mock data
        freelancer = {
            "id": freelancer_id,
            "hourly_rate": 75,
            "rating_average": 4.6,
            "total_jobs_completed": 25
        }

        contracts = []  # Would fetch from DB

        response = advisor_agent.process_task({
            "type": "growth_strategy",
            "freelancer": freelancer,
            "contracts": contracts,
            "goals": {
                "annual_income": annual_income_goal or 100000
            }
        })

        return {
            "status": "success",
            "growth_plan": response.data,
            "confidence": response.confidence,
            "recommendations": response.recommendations,
            "next_steps": response.next_steps
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== DASHBOARD & ANALYTICS ====================

@router.get("/dashboard/freelancer/{freelancer_id}")
def get_freelancer_dashboard(freelancer_id: int):
    """Get comprehensive freelancer dashboard data"""
    try:
        # Mock data
        freelancer = {
            "id": freelancer_id,
            "name": "John Doe",
            "title": "Full-Stack Developer",
            "hourly_rate": 75,
            "rating_average": 4.8,
            "total_jobs_completed": 45,
            "total_earnings": 32500,
            "success_rate": 96,
            "badges": ["top_rated", "reliable_delivery"],
            "is_available": True
        }

        contracts = []  # Would fetch active contracts

        metrics = freelance_hub.calculate_freelancer_metrics(freelancer_id, contracts)

        return {
            "status": "success",
            "profile": freelancer,
            "metrics": metrics,
            "active_contracts": 2,
            "pending_proposals": 3,
            "this_month_earnings": 2800,
            "average_monthly_earnings": 2100,
            "recent_reviews": [],
            "notifications": [
                {"type": "proposal_viewed", "message": "Client viewed your proposal", "time": "2 hours ago"},
                {"type": "new_job_match", "message": "3 new jobs match your profile", "time": "5 hours ago"}
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dashboard/client/{client_id}")
def get_client_dashboard(client_id: int):
    """Get comprehensive client dashboard data"""
    return {
        "status": "success",
        "active_jobs": 2,
        "active_contracts": 1,
        "total_spent": 5600,
        "avg_project_cost": 800,
        "favorite_freelancers": [],
        "recent_hires": []
    }

@router.get("/analytics/marketplace")
def get_marketplace_analytics():
    """Get overall marketplace analytics"""
    return {
        "status": "success",
        "total_freelancers": 1250,
        "active_freelancers": 890,
        "total_jobs_posted": 3400,
        "open_jobs": 245,
        "total_earnings_platform": 2450000,
        "avg_hourly_rate": 68,
        "top_categories": [
            {"name": "Web Development", "job_count": 120, "avg_rate": 75},
            {"name": "Graphic Design", "job_count": 85, "avg_rate": 60},
            {"name": "Writing", "job_count": 70, "avg_rate": 50}
        ],
        "trending_skills": ["react", "python", "figma", "seo", "nodejs"]
    }
