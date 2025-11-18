"""
Progress Tracking Models
Tracks learning progress, job applications, portfolio projects, and achievements
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class LearningActivity(Base):
    """Track individual learning activities"""
    __tablename__ = "learning_activities"

    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, ForeignKey("workers.id"))
    skill = Column(String, nullable=False)
    activity_type = Column(String)  # course, practice, project, reading
    status = Column(String, default="in_progress")  # in_progress, completed, abandoned
    difficulty = Column(String)  # easy, medium, hard
    score = Column(Float)  # 0-100
    time_spent_minutes = Column(Integer, default=0)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text, nullable=True)
    metadata = Column(JSON, nullable=True)  # Additional activity-specific data

    worker = relationship("Worker", back_populates="learning_activities")


class JobApplication(Base):
    """Track job applications"""
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, ForeignKey("workers.id"))
    company = Column(String, nullable=False)
    position = Column(String, nullable=False)
    job_url = Column(String, nullable=True)
    status = Column(String, default="applied")  # applied, screening, interview, offer, rejected, accepted, withdrawn
    application_date = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    salary_range_min = Column(Integer, nullable=True)
    salary_range_max = Column(Integer, nullable=True)
    location = Column(String, nullable=True)
    remote = Column(Boolean, default=False)
    source = Column(String, nullable=True)  # linkedin, indeed, referral, company_site, hidden_market
    priority = Column(String, default="medium")  # low, medium, high
    notes = Column(Text, nullable=True)
    interview_dates = Column(JSON, nullable=True)  # Array of interview dates
    contact_info = Column(JSON, nullable=True)  # Recruiter/hiring manager info
    match_score = Column(Float, nullable=True)  # AI-calculated match score

    worker = relationship("Worker", back_populates="job_applications")


class PortfolioProject(Base):
    """Track portfolio projects"""
    __tablename__ = "portfolio_projects"

    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, ForeignKey("workers.id"))
    title = Column(String, nullable=False)
    description = Column(Text)
    skills_demonstrated = Column(JSON)  # Array of skills
    project_url = Column(String, nullable=True)
    github_url = Column(String, nullable=True)
    status = Column(String, default="planned")  # planned, in_progress, completed
    difficulty = Column(String)  # beginner, intermediate, advanced
    impact_score = Column(Float, nullable=True)  # How impressive is this project
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text, nullable=True)
    metrics = Column(JSON, nullable=True)  # Project-specific metrics

    worker = relationship("Worker", back_populates="portfolio_projects")


class Achievement(Base):
    """Track achievements and badges"""
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, ForeignKey("workers.id"))
    achievement_type = Column(String, nullable=False)  # skill_mastery, streak, project_complete, job_landed, etc.
    title = Column(String, nullable=False)
    description = Column(String)
    badge_icon = Column(String)  # Icon name or URL
    points = Column(Integer, default=0)
    unlocked_at = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON, nullable=True)

    worker = relationship("Worker", back_populates="achievements")


class DailyProgress(Base):
    """Track daily progress metrics"""
    __tablename__ = "daily_progress"

    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, ForeignKey("workers.id"))
    date = Column(DateTime, nullable=False)
    activities_completed = Column(Integer, default=0)
    time_spent_minutes = Column(Integer, default=0)
    skills_practiced = Column(JSON)  # Array of skills practiced
    applications_sent = Column(Integer, default=0)
    projects_worked_on = Column(Integer, default=0)
    overall_score = Column(Float, default=0.0)
    notes = Column(Text, nullable=True)

    worker = relationship("Worker", back_populates="daily_progress")


class LearningStreak(Base):
    """Track learning streaks"""
    __tablename__ = "learning_streaks"

    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, ForeignKey("workers.id"), unique=True)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_activity_date = Column(DateTime, nullable=True)
    total_days_active = Column(Integer, default=0)
    streak_milestones = Column(JSON, nullable=True)  # Array of milestone dates

    worker = relationship("Worker", back_populates="learning_streak")
