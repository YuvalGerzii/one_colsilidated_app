"""
Script to create database tables and populate with sample data
"""
from app.db.database import engine
from app.db.models import Base, Worker, Skill, Job, Enterprise
from app.db.models import WorkerSkill, JobSkill, TrainingProgram
from datetime import datetime, timedelta
import random

def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

def populate_sample_data():
    """Populate database with sample data for testing"""
    from sqlalchemy.orm import Session

    with Session(engine) as session:
        print("Populating sample data...")

        # Create sample skills
        skills_data = [
            {"name": "Python Programming", "category": "technical", "description": "Python development", "demand_score": 85, "automation_risk": 20},
            {"name": "Machine Learning", "category": "technical", "description": "ML algorithms", "demand_score": 90, "automation_risk": 25},
            {"name": "Data Analysis", "category": "technical", "description": "Data analysis skills", "demand_score": 80, "automation_risk": 40},
            {"name": "Cloud Computing", "category": "technical", "description": "Cloud platforms", "demand_score": 88, "automation_risk": 30},
            {"name": "Communication", "category": "soft", "description": "Communication skills", "demand_score": 75, "automation_risk": 10},
            {"name": "Leadership", "category": "soft", "description": "Team leadership", "demand_score": 70, "automation_risk": 15},
            {"name": "Data Entry", "category": "technical", "description": "Manual data entry", "demand_score": 30, "automation_risk": 95},
            {"name": "Customer Service", "category": "soft", "description": "Customer interaction", "demand_score": 60, "automation_risk": 65},
            {"name": "Project Management", "category": "domain", "description": "Project coordination", "demand_score": 78, "automation_risk": 35},
            {"name": "DevOps", "category": "technical", "description": "DevOps practices", "demand_score": 85, "automation_risk": 25},
        ]

        for skill_data in skills_data:
            skill = Skill(**skill_data)
            session.add(skill)

        session.commit()
        print(f"Created {len(skills_data)} skills")

        # Create sample workers
        workers_data = [
            {
                "email": "john.doe@example.com",
                "full_name": "John Doe",
                "hashed_password": "hashed_password",
                "current_job_title": "Data Entry Specialist",
                "current_industry": "administrative",
                "years_experience": 5,
                "education_level": "bachelor",
                "location": "New York, NY"
            },
            {
                "email": "jane.smith@example.com",
                "full_name": "Jane Smith",
                "hashed_password": "hashed_password",
                "current_job_title": "Customer Service Rep",
                "current_industry": "retail",
                "years_experience": 3,
                "education_level": "associate",
                "location": "Los Angeles, CA"
            },
            {
                "email": "mike.johnson@example.com",
                "full_name": "Mike Johnson",
                "hashed_password": "hashed_password",
                "current_job_title": "Software Developer",
                "current_industry": "technology",
                "years_experience": 7,
                "education_level": "master",
                "location": "San Francisco, CA"
            }
        ]

        for worker_data in workers_data:
            worker = Worker(**worker_data)
            session.add(worker)

        session.commit()
        print(f"Created {len(workers_data)} workers")

        # Create sample jobs
        jobs_data = [
            {
                "title": "Data Analyst",
                "company": "Tech Corp",
                "industry": "technology",
                "location": "New York, NY",
                "description": "Analyze data and create insights",
                "salary_min": 70000,
                "salary_max": 95000,
                "remote_friendly": True
            },
            {
                "title": "ML Engineer",
                "company": "AI Innovations",
                "industry": "technology",
                "location": "San Francisco, CA",
                "description": "Build ML models and deploy them",
                "salary_min": 110000,
                "salary_max": 150000,
                "remote_friendly": True
            },
            {
                "title": "Project Manager",
                "company": "Global Solutions",
                "industry": "management",
                "location": "Chicago, IL",
                "description": "Manage cross-functional projects",
                "salary_min": 80000,
                "salary_max": 110000,
                "remote_friendly": False
            }
        ]

        for job_data in jobs_data:
            job = Job(**job_data)
            session.add(job)

        session.commit()
        print(f"Created {len(jobs_data)} jobs")

        # Add skills to workers
        workers = session.query(Worker).all()
        skills = session.query(Skill).all()

        for worker in workers:
            # Randomly assign 3-5 skills to each worker
            worker_skill_count = random.randint(3, 5)
            selected_skills = random.sample(skills, worker_skill_count)

            for skill in selected_skills:
                worker_skill = WorkerSkill(
                    worker_id=worker.id,
                    skill_id=skill.id,
                    proficiency_level=random.randint(2, 5),
                    years_experience=random.randint(1, 5)
                )
                session.add(worker_skill)

        session.commit()
        print("Added skills to workers")

        # Add skills to jobs
        jobs = session.query(Job).all()

        for job in jobs:
            # Randomly assign 4-6 skills to each job
            job_skill_count = random.randint(4, 6)
            selected_skills = random.sample(skills, job_skill_count)

            for i, skill in enumerate(selected_skills):
                job_skill = JobSkill(
                    job_id=job.id,
                    skill_id=skill.id,
                    required=i < 3,  # First 3 are required
                    importance=random.randint(3, 5)
                )
                session.add(job_skill)

        session.commit()
        print("Added skills to jobs")

        # Create sample enterprise
        enterprise = Enterprise(
            company_name="Enterprise Demo Corp",
            industry="technology",
            size="large",
            subscription_tier="enterprise",
            contact_email="admin@enterprisedemo.com",
            subscription_expires=datetime.utcnow() + timedelta(days=365)
        )
        session.add(enterprise)
        session.commit()
        print("Created sample enterprise")

        # Create training programs
        training_data = [
            {
                "title": "Python for Data Science",
                "provider": "Coursera",
                "description": "Learn Python for data analysis",
                "duration_weeks": 8,
                "cost": 399,
                "online": True,
                "certification": True,
                "target_skills": [1, 3],  # Python, Data Analysis
                "success_rate": 0.85
            },
            {
                "title": "Machine Learning Bootcamp",
                "provider": "Udacity",
                "description": "Comprehensive ML training",
                "duration_weeks": 16,
                "cost": 1299,
                "online": True,
                "certification": True,
                "target_skills": [2, 3],  # ML, Data Analysis
                "success_rate": 0.80
            }
        ]

        for training in training_data:
            program = TrainingProgram(**training)
            session.add(program)

        session.commit()
        print("Created training programs")

        print("\nSample data population complete!")
        print("\nTest credentials:")
        print("Worker IDs: 1, 2, 3")
        print("Job IDs: 1, 2, 3")
        print("Enterprise ID: 1")

if __name__ == "__main__":
    create_tables()
    populate_sample_data()
