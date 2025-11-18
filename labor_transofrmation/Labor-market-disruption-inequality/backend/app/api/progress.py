"""
Progress Tracking API
Tracks learning activities, portfolio projects, job applications, and achievements
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime, timedelta
from app.db.database import get_db
from app.db.models import Worker

# Import progress models (these will be added to models.py)
from app.models.progress_tracking import (
    LearningActivity,
    JobApplication,
    PortfolioProject,
    Achievement,
    DailyProgress,
    LearningStreak
)

router = APIRouter()


class LearningActivityCreate(BaseModel):
    skill: str
    activity_type: str
    difficulty: str = "medium"
    time_spent_minutes: int = 0
    notes: Optional[str] = None


class JobApplicationCreate(BaseModel):
    company: str
    position: str
    job_url: Optional[str] = None
    salary_range_min: Optional[int] = None
    salary_range_max: Optional[int] = None
    location: Optional[str] = None
    remote: bool = False
    source: Optional[str] = None
    priority: str = "medium"
    notes: Optional[str] = None


class PortfolioProjectCreate(BaseModel):
    title: str
    description: str
    skills_demonstrated: List[str]
    project_url: Optional[str] = None
    github_url: Optional[str] = None
    difficulty: str = "intermediate"


class JobApplicationUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None
    priority: Optional[str] = None
    interview_dates: Optional[List[str]] = None


@router.get("/dashboard/{worker_id}")
def get_progress_dashboard(worker_id: int, db: Session = Depends(get_db)):
    """
    Get comprehensive progress dashboard
    """
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    # Get learning streak
    streak = db.query(LearningStreak).filter(LearningStreak.worker_id == worker_id).first()
    if not streak:
        streak = LearningStreak(worker_id=worker_id, current_streak=0, longest_streak=0)
        db.add(streak)
        db.commit()
        db.refresh(streak)

    # Recent learning activities
    recent_activities = db.query(LearningActivity).filter(
        LearningActivity.worker_id == worker_id
    ).order_by(LearningActivity.created_at.desc()).limit(10).all()

    # Job applications summary
    total_applications = db.query(func.count(JobApplication.id)).filter(
        JobApplication.worker_id == worker_id
    ).scalar()

    applications_by_status = db.query(
        JobApplication.status,
        func.count(JobApplication.id)
    ).filter(
        JobApplication.worker_id == worker_id
    ).group_by(JobApplication.status).all()

    # Portfolio projects
    portfolio_projects = db.query(PortfolioProject).filter(
        PortfolioProject.worker_id == worker_id
    ).order_by(PortfolioProject.created_at.desc()).all()

    # Achievements
    achievements = db.query(Achievement).filter(
        Achievement.worker_id == worker_id
    ).order_by(Achievement.unlocked_at.desc()).limit(5).all()

    # Calculate weekly progress
    week_ago = datetime.utcnow() - timedelta(days=7)
    weekly_activities = db.query(LearningActivity).filter(
        LearningActivity.worker_id == worker_id,
        LearningActivity.created_at >= week_ago
    ).all()

    weekly_time = sum(a.time_spent_minutes for a in weekly_activities)
    weekly_completed = len([a for a in weekly_activities if a.status == "completed"])

    # Recent applications
    recent_applications = db.query(JobApplication).filter(
        JobApplication.worker_id == worker_id
    ).order_by(JobApplication.application_date.desc()).limit(5).all()

    # Calculate overall progress score
    progress_score = _calculate_progress_score(
        len(recent_activities),
        streak.current_streak,
        total_applications,
        len(portfolio_projects),
        len(achievements)
    )

    return {
        "worker_id": worker_id,
        "progress_score": progress_score,
        "learning_streak": {
            "current": streak.current_streak,
            "longest": streak.longest_streak,
            "total_days_active": streak.total_days_active,
            "last_activity": streak.last_activity_date
        },
        "this_week": {
            "activities_completed": weekly_completed,
            "total_activities": len(weekly_activities),
            "time_spent_hours": round(weekly_time / 60, 1),
            "applications_sent": len([a for a in recent_applications if a.application_date >= week_ago])
        },
        "job_search": {
            "total_applications": total_applications,
            "by_status": {status: count for status, count in applications_by_status},
            "recent_applications": [
                {
                    "id": app.id,
                    "company": app.company,
                    "position": app.position,
                    "status": app.status,
                    "applied_date": app.application_date,
                    "priority": app.priority
                } for app in recent_applications
            ]
        },
        "portfolio": {
            "total_projects": len(portfolio_projects),
            "completed": len([p for p in portfolio_projects if p.status == "completed"]),
            "in_progress": len([p for p in portfolio_projects if p.status == "in_progress"]),
            "projects": [
                {
                    "id": p.id,
                    "title": p.title,
                    "status": p.status,
                    "skills": p.skills_demonstrated,
                    "github_url": p.github_url
                } for p in portfolio_projects[:5]
            ]
        },
        "achievements": {
            "total": len(achievements),
            "recent": [
                {
                    "title": a.title,
                    "description": a.description,
                    "badge_icon": a.badge_icon,
                    "points": a.points,
                    "unlocked_at": a.unlocked_at
                } for a in achievements
            ]
        },
        "recent_activities": [
            {
                "id": a.id,
                "skill": a.skill,
                "activity_type": a.activity_type,
                "status": a.status,
                "score": a.score,
                "time_spent_minutes": a.time_spent_minutes,
                "created_at": a.created_at
            } for a in recent_activities
        ],
        "recommendations": _generate_dashboard_recommendations(
            streak.current_streak,
            total_applications,
            len(portfolio_projects),
            weekly_completed
        )
    }


@router.post("/learning-activity/{worker_id}")
def log_learning_activity(
    worker_id: int,
    activity: LearningActivityCreate,
    db: Session = Depends(get_db)
):
    """Log a learning activity and update streak"""
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    # Create activity
    new_activity = LearningActivity(
        worker_id=worker_id,
        skill=activity.skill,
        activity_type=activity.activity_type,
        difficulty=activity.difficulty,
        time_spent_minutes=activity.time_spent_minutes,
        status="completed",
        notes=activity.notes,
        completed_at=datetime.utcnow()
    )
    db.add(new_activity)

    # Update streak
    streak = db.query(LearningStreak).filter(LearningStreak.worker_id == worker_id).first()
    if not streak:
        streak = LearningStreak(worker_id=worker_id)
        db.add(streak)

    today = datetime.utcnow().date()
    if streak.last_activity_date:
        last_date = streak.last_activity_date.date()
        if today == last_date:
            # Same day, no streak change
            pass
        elif today == last_date + timedelta(days=1):
            # Consecutive day
            streak.current_streak += 1
            streak.longest_streak = max(streak.longest_streak, streak.current_streak)
        else:
            # Streak broken
            streak.current_streak = 1
    else:
        streak.current_streak = 1

    streak.last_activity_date = datetime.utcnow()
    streak.total_days_active += 1

    # Check for achievements
    achievements = _check_achievements(worker_id, streak, db)

    db.commit()

    return {
        "activity_id": new_activity.id,
        "streak": {
            "current": streak.current_streak,
            "longest": streak.longest_streak
        },
        "new_achievements": achievements,
        "message": "Activity logged successfully"
    }


@router.post("/job-application/{worker_id}")
def create_job_application(
    worker_id: int,
    application: JobApplicationCreate,
    db: Session = Depends(get_db)
):
    """Create a new job application"""
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    new_application = JobApplication(
        worker_id=worker_id,
        company=application.company,
        position=application.position,
        job_url=application.job_url,
        salary_range_min=application.salary_range_min,
        salary_range_max=application.salary_range_max,
        location=application.location,
        remote=application.remote,
        source=application.source,
        priority=application.priority,
        notes=application.notes,
        status="applied"
    )
    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return {
        "application_id": new_application.id,
        "company": new_application.company,
        "position": new_application.position,
        "status": new_application.status,
        "message": "Application tracked successfully"
    }


@router.patch("/job-application/{application_id}")
def update_job_application(
    application_id: int,
    update: JobApplicationUpdate,
    db: Session = Depends(get_db)
):
    """Update job application status"""
    application = db.query(JobApplication).filter(JobApplication.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    if update.status:
        application.status = update.status
    if update.notes:
        application.notes = update.notes
    if update.priority:
        application.priority = update.priority
    if update.interview_dates:
        application.interview_dates = update.interview_dates

    application.last_updated = datetime.utcnow()

    # Check for achievements
    if update.status == "offer":
        achievement = Achievement(
            worker_id=application.worker_id,
            achievement_type="job_offer",
            title="Job Offer Received!",
            description=f"Received offer from {application.company}",
            badge_icon="celebration",
            points=500
        )
        db.add(achievement)

    db.commit()

    return {
        "application_id": application.id,
        "status": application.status,
        "message": "Application updated successfully"
    }


@router.get("/job-applications/{worker_id}")
def get_job_applications(
    worker_id: int,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all job applications for a worker"""
    query = db.query(JobApplication).filter(JobApplication.worker_id == worker_id)

    if status:
        query = query.filter(JobApplication.status == status)

    applications = query.order_by(JobApplication.application_date.desc()).all()

    return {
        "total": len(applications),
        "applications": [
            {
                "id": app.id,
                "company": app.company,
                "position": app.position,
                "status": app.status,
                "application_date": app.application_date,
                "last_updated": app.last_updated,
                "priority": app.priority,
                "salary_range": f"${app.salary_range_min}-${app.salary_range_max}" if app.salary_range_min else None,
                "location": app.location,
                "remote": app.remote,
                "source": app.source,
                "notes": app.notes
            } for app in applications
        ]
    }


@router.post("/portfolio-project/{worker_id}")
def create_portfolio_project(
    worker_id: int,
    project: PortfolioProjectCreate,
    db: Session = Depends(get_db)
):
    """Create a new portfolio project"""
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    new_project = PortfolioProject(
        worker_id=worker_id,
        title=project.title,
        description=project.description,
        skills_demonstrated=project.skills_demonstrated,
        project_url=project.project_url,
        github_url=project.github_url,
        difficulty=project.difficulty,
        status="in_progress",
        started_at=datetime.utcnow()
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return {
        "project_id": new_project.id,
        "title": new_project.title,
        "status": new_project.status,
        "message": "Project created successfully"
    }


@router.patch("/portfolio-project/{project_id}/complete")
def complete_portfolio_project(project_id: int, db: Session = Depends(get_db)):
    """Mark a portfolio project as completed"""
    project = db.query(PortfolioProject).filter(PortfolioProject.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project.status = "completed"
    project.completed_at = datetime.utcnow()

    # Add achievement
    achievement = Achievement(
        worker_id=project.worker_id,
        achievement_type="project_complete",
        title="Project Completed!",
        description=f"Completed {project.title}",
        badge_icon="rocket",
        points=100
    )
    db.add(achievement)

    db.commit()

    return {
        "project_id": project.id,
        "title": project.title,
        "status": project.status,
        "message": "Project marked as completed"
    }


@router.get("/portfolio-recommendations/{worker_id}")
def get_portfolio_recommendations(worker_id: int, db: Session = Depends(get_db)):
    """
    Get AI-recommended portfolio projects based on worker's goals
    """
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    # Get current skills and gaps (simplified - in production, fetch from gap analyzer)
    current_skills = ["python", "sql"]
    target_skills = ["machine_learning", "deep_learning", "cloud"]

    recommendations = _generate_project_recommendations(current_skills, target_skills)

    return {
        "worker_id": worker_id,
        "recommendations": recommendations,
        "total_recommended": len(recommendations)
    }


@router.get("/achievements/{worker_id}")
def get_achievements(worker_id: int, db: Session = Depends(get_db)):
    """Get all achievements for a worker"""
    achievements = db.query(Achievement).filter(
        Achievement.worker_id == worker_id
    ).order_by(Achievement.unlocked_at.desc()).all()

    total_points = sum(a.points for a in achievements)

    # Calculate level
    level = _calculate_level(total_points)

    return {
        "total_achievements": len(achievements),
        "total_points": total_points,
        "level": level,
        "next_level_points": (level + 1) * 1000,
        "achievements": [
            {
                "title": a.title,
                "description": a.description,
                "badge_icon": a.badge_icon,
                "points": a.points,
                "type": a.achievement_type,
                "unlocked_at": a.unlocked_at
            } for a in achievements
        ],
        "available_achievements": _get_available_achievements()
    }


def _calculate_progress_score(
    activities: int,
    streak: int,
    applications: int,
    projects: int,
    achievements: int
) -> int:
    """Calculate overall progress score"""
    score = 0
    score += min(activities * 2, 30)  # Up to 30 points for activities
    score += min(streak * 3, 30)  # Up to 30 points for streak
    score += min(applications * 2, 20)  # Up to 20 points for applications
    score += min(projects * 5, 15)  # Up to 15 points for projects
    score += min(achievements * 1, 5)  # Up to 5 points for achievements
    return min(score, 100)


def _generate_dashboard_recommendations(
    streak: int,
    applications: int,
    projects: int,
    weekly_completed: int
) -> List[str]:
    """Generate personalized recommendations"""
    recommendations = []

    if streak == 0:
        recommendations.append("Start your learning streak today! Complete one activity.")
    elif streak < 7:
        recommendations.append(f"Great! {7 - streak} more days to reach a 1-week streak!")
    else:
        recommendations.append(f"Amazing {streak}-day streak! Keep it going!")

    if applications < 5:
        recommendations.append("Apply to at least 5 positions to increase your chances")
    elif applications < 20:
        recommendations.append("Good progress! Aim for 20+ applications for better odds")

    if projects == 0:
        recommendations.append("Start building your first portfolio project")
    elif projects < 3:
        recommendations.append("Add more projects to strengthen your portfolio (target: 3-5)")

    if weekly_completed < 3:
        recommendations.append("Try to complete at least 3-5 learning activities per week")

    return recommendations


def _check_achievements(worker_id: int, streak: LearningStreak, db: Session) -> List[Dict]:
    """Check and unlock achievements"""
    new_achievements = []

    # Streak milestones
    if streak.current_streak == 7:
        achievement = Achievement(
            worker_id=worker_id,
            achievement_type="streak",
            title="7-Day Warrior",
            description="Completed 7 consecutive days of learning",
            badge_icon="fire",
            points=50
        )
        db.add(achievement)
        new_achievements.append({"title": achievement.title, "points": achievement.points})

    elif streak.current_streak == 30:
        achievement = Achievement(
            worker_id=worker_id,
            achievement_type="streak",
            title="Monthly Master",
            description="Completed 30 consecutive days of learning",
            badge_icon="trophy",
            points=200
        )
        db.add(achievement)
        new_achievements.append({"title": achievement.title, "points": achievement.points})

    return new_achievements


def _generate_project_recommendations(
    current_skills: List[str],
    target_skills: List[str]
) -> List[Dict]:
    """Generate portfolio project recommendations"""
    project_templates = {
        "machine_learning": [
            {
                "title": "House Price Prediction Model",
                "description": "Build an ML model to predict house prices using regression",
                "difficulty": "beginner",
                "skills_required": ["python", "pandas", "scikit-learn"],
                "estimated_hours": 10,
                "impact_score": 7.5,
                "instructions": [
                    "Get dataset from Kaggle",
                    "Perform exploratory data analysis",
                    "Engineer features",
                    "Train multiple models (Linear Regression, Random Forest)",
                    "Evaluate and compare results",
                    "Deploy to Streamlit"
                ]
            },
            {
                "title": "Image Classification with CNNs",
                "description": "Build a convolutional neural network to classify images",
                "difficulty": "intermediate",
                "skills_required": ["python", "tensorflow", "keras"],
                "estimated_hours": 20,
                "impact_score": 8.5,
                "instructions": [
                    "Choose dataset (CIFAR-10, ImageNet subset)",
                    "Build CNN architecture",
                    "Implement data augmentation",
                    "Train and tune hyperparameters",
                    "Visualize results and confusion matrix",
                    "Create web demo"
                ]
            }
        ],
        "web_development": [
            {
                "title": "Full-Stack Todo App",
                "description": "Build a complete todo application with React and Node.js",
                "difficulty": "intermediate",
                "skills_required": ["react", "node.js", "mongodb"],
                "estimated_hours": 25,
                "impact_score": 8.0,
                "instructions": [
                    "Set up React frontend",
                    "Create Node.js/Express backend",
                    "Implement CRUD operations",
                    "Add user authentication",
                    "Deploy to Heroku/Vercel"
                ]
            }
        ],
        "data_science": [
            {
                "title": "Sales Dashboard with Analytics",
                "description": "Build an interactive dashboard analyzing sales data",
                "difficulty": "beginner",
                "skills_required": ["python", "pandas", "plotly"],
                "estimated_hours": 12,
                "impact_score": 7.0,
                "instructions": [
                    "Load and clean sales data",
                    "Calculate key metrics (revenue, growth, trends)",
                    "Create visualizations",
                    "Build interactive Dash/Streamlit app",
                    "Add filters and date ranges"
                ]
            }
        ]
    }

    recommendations = []

    for skill in target_skills:
        if skill in project_templates:
            recommendations.extend(project_templates[skill])

    # Default recommendations
    if not recommendations:
        recommendations = [
            {
                "title": "Personal Portfolio Website",
                "description": "Build your own portfolio site to showcase projects",
                "difficulty": "beginner",
                "skills_required": ["html", "css", "javascript"],
                "estimated_hours": 8,
                "impact_score": 6.0,
                "instructions": [
                    "Design layout and structure",
                    "Create sections: About, Projects, Skills, Contact",
                    "Make responsive for mobile",
                    "Deploy to GitHub Pages or Netlify"
                ]
            }
        ]

    return recommendations[:5]  # Return top 5


def _calculate_level(total_points: int) -> int:
    """Calculate level based on total points"""
    return total_points // 1000 + 1


def _get_available_achievements() -> List[Dict]:
    """Get list of all available achievements"""
    return [
        {"title": "First Steps", "description": "Complete first learning activity", "points": 10},
        {"title": "7-Day Warrior", "description": "7 day learning streak", "points": 50},
        {"title": "Monthly Master", "description": "30 day learning streak", "points": 200},
        {"title": "Project Pioneer", "description": "Complete first portfolio project", "points": 100},
        {"title": "Application Pro", "description": "Submit 10 job applications", "points": 75},
        {"title": "Interview Ready", "description": "Schedule first interview", "points": 150},
        {"title": "Offer Champion", "description": "Receive job offer", "points": 500},
        {"title": "Skill Master", "description": "Master 5 skills", "points": 250},
    ]
