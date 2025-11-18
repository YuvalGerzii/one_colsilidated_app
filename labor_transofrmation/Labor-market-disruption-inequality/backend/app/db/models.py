from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Worker(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    current_job_title = Column(String)
    current_industry = Column(String)
    years_experience = Column(Integer)
    education_level = Column(String)
    location = Column(String)
    risk_score = Column(Float, nullable=True)  # Job loss risk score
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    skills = relationship("WorkerSkill", back_populates="worker")
    applications = relationship("JobApplication", back_populates="worker")
    reskilling_paths = relationship("ReskillingPath", back_populates="worker")
    learning_activities = relationship("LearningActivity", back_populates="worker")
    portfolio_projects = relationship("PortfolioProject", back_populates="worker")
    achievements = relationship("Achievement", back_populates="worker")
    daily_progress = relationship("DailyProgress", back_populates="worker")
    learning_streak = relationship("LearningStreak", back_populates="worker", uselist=False)

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    category = Column(String)  # technical, soft, domain
    description = Column(Text)
    demand_score = Column(Float)  # Market demand (0-100)
    automation_risk = Column(Float)  # Risk of being automated (0-100)

    # Relationships
    worker_skills = relationship("WorkerSkill", back_populates="skill")
    job_skills = relationship("JobSkill", back_populates="skill")

class WorkerSkill(Base):
    __tablename__ = "worker_skills"

    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, ForeignKey("workers.id"))
    skill_id = Column(Integer, ForeignKey("skills.id"))
    proficiency_level = Column(Integer)  # 1-5 scale
    years_experience = Column(Integer)
    verified = Column(Boolean, default=False)

    # Relationships
    worker = relationship("Worker", back_populates="skills")
    skill = relationship("Skill", back_populates="worker_skills")

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    company = Column(String)
    industry = Column(String)
    location = Column(String)
    description = Column(Text)
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    remote_friendly = Column(Boolean, default=False)
    automation_resistant = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)

    # Relationships
    skills = relationship("JobSkill", back_populates="job")
    applications = relationship("JobApplication", back_populates="job")

class JobSkill(Base):
    __tablename__ = "job_skills"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    skill_id = Column(Integer, ForeignKey("skills.id"))
    required = Column(Boolean, default=True)  # Required vs preferred
    importance = Column(Integer)  # 1-5 scale

    # Relationships
    job = relationship("Job", back_populates="skills")
    skill = relationship("Skill", back_populates="job_skills")

class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, ForeignKey("workers.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    match_score = Column(Float)  # ML-computed match score
    status = Column(String)  # pending, reviewing, interview, rejected, accepted
    applied_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    worker = relationship("Worker", back_populates="applications")
    job = relationship("Job", back_populates="applications")

class TrainingProgram(Base):
    __tablename__ = "training_programs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    provider = Column(String)
    description = Column(Text)
    duration_weeks = Column(Integer)
    cost = Column(Float)
    online = Column(Boolean, default=True)
    certification = Column(Boolean, default=False)
    target_skills = Column(JSON)  # List of skill IDs
    success_rate = Column(Float)  # Historical success rate
    created_at = Column(DateTime, default=datetime.utcnow)

class ReskillingPath(Base):
    __tablename__ = "reskilling_paths"

    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, ForeignKey("workers.id"))
    target_job_title = Column(String)
    current_skill_match = Column(Float)  # % match with target
    estimated_duration_weeks = Column(Integer)
    recommended_programs = Column(JSON)  # List of training program IDs
    skill_gaps = Column(JSON)  # List of skills to acquire
    created_at = Column(DateTime, default=datetime.utcnow)
    completed = Column(Boolean, default=False)

    # Relationships
    worker = relationship("Worker", back_populates="reskilling_paths")

class Enterprise(Base):
    __tablename__ = "enterprises"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, index=True)
    industry = Column(String)
    size = Column(String)  # small, medium, large, enterprise
    subscription_tier = Column(String)  # basic, professional, enterprise
    contact_email = Column(String)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    subscription_expires = Column(DateTime, nullable=True)

# ==================== FREELANCE WORKERS HUB MODELS ====================

class FreelanceProfile(Base):
    """Extended profile for workers offering freelance services"""
    __tablename__ = "freelance_profiles"

    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, ForeignKey("workers.id"), unique=True)

    # Profile information
    title = Column(String)  # e.g., "Python Developer", "Graphic Designer"
    bio = Column(Text)
    hourly_rate = Column(Float)
    availability_hours_weekly = Column(Integer)

    # Ratings & stats
    rating_average = Column(Float, default=0.0)  # 0-5 stars
    total_reviews = Column(Integer, default=0)
    total_jobs_completed = Column(Integer, default=0)
    total_earnings = Column(Float, default=0.0)
    success_rate = Column(Float, default=0.0)  # % of completed projects
    response_time_hours = Column(Float, default=24.0)  # Average response time

    # Badges & verification
    verified = Column(Boolean, default=False)
    top_rated = Column(Boolean, default=False)  # Auto-calculated based on performance
    badges = Column(JSON, default=list)  # ["expert_python", "reliable", "fast_delivery"]

    # Preferences
    preferred_job_types = Column(JSON, default=list)  # ["one_time", "ongoing", "hourly"]
    min_project_budget = Column(Float, default=0.0)
    languages = Column(JSON, default=list)  # ["English", "Spanish"]

    # Activity
    is_active = Column(Boolean, default=True)
    is_available = Column(Boolean, default=True)
    last_active = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    worker = relationship("Worker", backref="freelance_profile")
    job_postings = relationship("FreelanceJobPosting", back_populates="freelancer", foreign_keys="FreelanceJobPosting.freelancer_id")
    proposals = relationship("FreelanceProposal", back_populates="freelancer")
    contracts = relationship("FreelanceContract", back_populates="freelancer")
    reviews_received = relationship("FreelanceReview", back_populates="freelancer", foreign_keys="FreelanceReview.freelancer_id")
    portfolio_items = relationship("FreelancePortfolioItem", back_populates="freelancer")

class FreelanceCategory(Base):
    """Categories/specializations for freelance services"""
    __tablename__ = "freelance_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)  # e.g., "Web Development", "Graphic Design"
    parent_id = Column(Integer, ForeignKey("freelance_categories.id"), nullable=True)  # For subcategories
    description = Column(Text)
    icon = Column(String)  # Icon name or emoji
    is_active = Column(Boolean, default=True)
    job_count = Column(Integer, default=0)  # Denormalized count of active jobs

    # Relationships
    parent = relationship("FreelanceCategory", remote_side=[id], backref="subcategories")
    job_postings = relationship("FreelanceJobPosting", back_populates="category")

class FreelanceJobPosting(Base):
    """Jobs posted by clients for freelancers to bid on"""
    __tablename__ = "freelance_job_postings"

    id = Column(Integer, primary_key=True, index=True)

    # Posted by (can be a regular worker or enterprise)
    client_id = Column(Integer, ForeignKey("workers.id"))
    freelancer_id = Column(Integer, ForeignKey("freelance_profiles.id"), nullable=True)  # If job is assigned

    # Job details
    title = Column(String, index=True)
    description = Column(Text)
    category_id = Column(Integer, ForeignKey("freelance_categories.id"))

    # Budget & timeline
    budget_type = Column(String)  # "fixed", "hourly"
    budget_min = Column(Float)
    budget_max = Column(Float)
    duration_estimate = Column(String)  # "1-3 days", "1-2 weeks", etc.
    deadline = Column(DateTime, nullable=True)

    # Requirements
    required_skills = Column(JSON, default=list)  # List of skill IDs or names
    experience_level = Column(String)  # "beginner", "intermediate", "expert"

    # Status
    status = Column(String, default="open")  # open, in_progress, completed, cancelled
    visibility = Column(String, default="public")  # public, private, invited_only

    # Stats
    views_count = Column(Integer, default=0)
    proposals_count = Column(Integer, default=0)

    # Timestamps
    posted_at = Column(DateTime, default=datetime.utcnow, index=True)
    expires_at = Column(DateTime, nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    client = relationship("Worker", foreign_keys=[client_id], backref="posted_jobs")
    freelancer = relationship("FreelanceProfile", back_populates="job_postings", foreign_keys=[freelancer_id])
    category = relationship("FreelanceCategory", back_populates="job_postings")
    proposals = relationship("FreelanceProposal", back_populates="job_posting")
    contract = relationship("FreelanceContract", back_populates="job_posting", uselist=False)

class FreelanceProposal(Base):
    """Proposals/bids submitted by freelancers for job postings"""
    __tablename__ = "freelance_proposals"

    id = Column(Integer, primary_key=True, index=True)
    job_posting_id = Column(Integer, ForeignKey("freelance_job_postings.id"))
    freelancer_id = Column(Integer, ForeignKey("freelance_profiles.id"))

    # Proposal details
    cover_letter = Column(Text)
    proposed_rate = Column(Float)
    proposed_duration = Column(String)
    delivery_date = Column(DateTime, nullable=True)

    # Status
    status = Column(String, default="pending")  # pending, accepted, rejected, withdrawn

    # Timestamps
    submitted_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    reviewed_at = Column(DateTime, nullable=True)

    # Relationships
    job_posting = relationship("FreelanceJobPosting", back_populates="proposals")
    freelancer = relationship("FreelanceProfile", back_populates="proposals")

class FreelanceContract(Base):
    """Active/completed contracts between clients and freelancers"""
    __tablename__ = "freelance_contracts"

    id = Column(Integer, primary_key=True, index=True)
    job_posting_id = Column(Integer, ForeignKey("freelance_job_postings.id"))
    proposal_id = Column(Integer, ForeignKey("freelance_proposals.id"))
    freelancer_id = Column(Integer, ForeignKey("freelance_profiles.id"))
    client_id = Column(Integer, ForeignKey("workers.id"))

    # Contract terms
    agreed_rate = Column(Float)
    payment_type = Column(String)  # "fixed", "hourly", "milestone"
    total_amount = Column(Float)
    escrow_amount = Column(Float, default=0.0)  # Amount held in escrow

    # Milestones (for milestone-based contracts)
    milestones = Column(JSON, default=list)  # [{"name": "...", "amount": 500, "status": "pending"}]

    # Status & progress
    status = Column(String, default="active")  # active, completed, disputed, cancelled
    progress_percentage = Column(Integer, default=0)

    # Payments
    amount_paid = Column(Float, default=0.0)
    amount_pending = Column(Float, default=0.0)

    # Timestamps
    started_at = Column(DateTime, default=datetime.utcnow)
    deadline = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    job_posting = relationship("FreelanceJobPosting", back_populates="contract")
    proposal = relationship("FreelanceProposal", backref="contract")
    freelancer = relationship("FreelanceProfile", back_populates="contracts")
    client = relationship("Worker", foreign_keys=[client_id], backref="contracts")
    messages = relationship("FreelanceMessage", back_populates="contract")
    review = relationship("FreelanceReview", back_populates="contract", uselist=False)

class FreelanceReview(Base):
    """Reviews and ratings for completed contracts"""
    __tablename__ = "freelance_reviews"

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("freelance_contracts.id"))
    freelancer_id = Column(Integer, ForeignKey("freelance_profiles.id"))
    client_id = Column(Integer, ForeignKey("workers.id"))

    # Review from client to freelancer
    rating = Column(Float)  # 1-5 stars
    review_text = Column(Text)

    # Detailed ratings (optional, 1-5 each)
    quality_rating = Column(Float, nullable=True)
    communication_rating = Column(Float, nullable=True)
    professionalism_rating = Column(Float, nullable=True)
    deadline_rating = Column(Float, nullable=True)
    value_rating = Column(Float, nullable=True)

    # Would hire again?
    would_recommend = Column(Boolean, default=True)
    would_hire_again = Column(Boolean, default=True)

    # Response from freelancer (optional)
    freelancer_response = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    response_at = Column(DateTime, nullable=True)

    # Relationships
    contract = relationship("FreelanceContract", back_populates="review")
    freelancer = relationship("FreelanceProfile", back_populates="reviews_received", foreign_keys=[freelancer_id])
    client = relationship("Worker", foreign_keys=[client_id], backref="reviews_given")

class FreelancePortfolioItem(Base):
    """Portfolio items showcased by freelancers"""
    __tablename__ = "freelance_portfolio_items"

    id = Column(Integer, primary_key=True, index=True)
    freelancer_id = Column(Integer, ForeignKey("freelance_profiles.id"))

    # Portfolio item details
    title = Column(String)
    description = Column(Text)
    category = Column(String)
    tags = Column(JSON, default=list)  # ["python", "web", "automation"]

    # Media
    thumbnail_url = Column(String, nullable=True)
    images = Column(JSON, default=list)  # List of image URLs
    video_url = Column(String, nullable=True)
    live_url = Column(String, nullable=True)
    github_url = Column(String, nullable=True)

    # Stats
    views_count = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    freelancer = relationship("FreelanceProfile", back_populates="portfolio_items")

class FreelanceMessage(Base):
    """Messages between clients and freelancers"""
    __tablename__ = "freelance_messages"

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("freelance_contracts.id"))
    sender_id = Column(Integer, ForeignKey("workers.id"))

    # Message content
    message_text = Column(Text)
    attachments = Column(JSON, default=list)  # URLs to attachments

    # Status
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime, nullable=True)

    # Timestamps
    sent_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    contract = relationship("FreelanceContract", back_populates="messages")
    sender = relationship("Worker", foreign_keys=[sender_id], backref="messages_sent")
