from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from app.db.database import get_db
from app.db.models import Worker, WorkerSkill, Job
from app.models.skill_graph import SkillGraphGenerator
from app.models.reskilling_autopilot import ReskillingAutopilot
from app.models.career_simulator import CareerSimulator

router = APIRouter()
skill_graph_gen = SkillGraphGenerator()
autopilot = ReskillingAutopilot()
career_sim = CareerSimulator()

class SkillGraphRequest(BaseModel):
    worker_id: int

class PRPRequest(BaseModel):
    worker_id: int
    target_role_id: int
    hours_per_week: int = 10
    max_budget: float = 5000

class PRPAdaptRequest(BaseModel):
    worker_id: int
    progress_data: dict
    market_updates: dict

class CareerSimRequest(BaseModel):
    career_path: str
    worker_id: int
    time_horizon_years: int = 10

class CareerCompareRequest(BaseModel):
    worker_id: int
    career_options: List[str]
    time_horizon_years: int = 10

@router.post("/skill-graph")
def generate_skill_graph(request: SkillGraphRequest, db: Session = Depends(get_db)):
    """
    Generate intelligent skill graph from worker's experience
    Converts experience into network of skills with relationships
    """
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
            'skill_name': f"Skill_{ws.skill_id}",  # Would fetch from Skill table
            'proficiency_level': ws.proficiency_level,
            'years_experience': ws.years_experience,
            'market_demand': 70  # Mock data
        }
        for ws in worker_skills_db
    ]

    # Mock job history
    job_history = [
        {'title': worker.current_job_title, 'years': worker.years_experience}
    ]

    worker_experience = {
        'years_total': worker.years_experience,
        'current_role': worker.current_job_title,
        'industry': worker.current_industry
    }

    # Generate graph
    skill_graph = skill_graph_gen.generate_skill_graph(
        worker_experience,
        worker_skills,
        job_history
    )

    return {
        'worker_id': request.worker_id,
        'skill_graph': skill_graph,
        'visualization_url': f'/viz/skill-graph/{request.worker_id}'  # Could link to graph visualization
    }

@router.post("/personal-reskilling-plan")
def create_personal_reskilling_plan(request: PRPRequest, db: Session = Depends(get_db)):
    """
    Auto-generate Personal Reskilling Plan (PRP)
    AI Reskilling Autopilot core feature
    """
    worker = db.query(Worker).filter(Worker.id == request.worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    # Get skill graph first
    graph_request = SkillGraphRequest(worker_id=request.worker_id)
    skill_graph_response = generate_skill_graph(graph_request, db)
    skill_graph = skill_graph_response['skill_graph']

    # Mock target role
    target_role = {
        'title': 'Data Scientist',
        'required_skills': [
            {'name': 'Python', 'required_proficiency': 80, 'priority': 'high'},
            {'name': 'Machine Learning', 'required_proficiency': 75, 'priority': 'high'},
            {'name': 'Statistics', 'required_proficiency': 70, 'priority': 'medium'},
            {'name': 'SQL', 'required_proficiency': 65, 'priority': 'medium'}
        ]
    }

    # Mock market trends
    market_trends = {
        'skills_demand': {
            'Python': 90,
            'Machine Learning': 95,
            'Statistics': 80,
            'SQL': 75
        }
    }

    learning_preferences = {
        'hours_per_week': request.hours_per_week,
        'max_budget': request.max_budget,
        'online_only': True
    }

    # Generate PRP
    prp = autopilot.generate_personal_reskilling_plan(
        worker_id=request.worker_id,
        skill_graph=skill_graph,
        target_role=target_role,
        market_trends=market_trends,
        learning_preferences=learning_preferences
    )

    return {
        'worker_id': request.worker_id,
        'target_role': prp.target_role,
        'current_readiness': prp.current_readiness,
        'target_readiness': prp.target_readiness,
        'estimated_completion_weeks': prp.estimated_completion_weeks,
        'learning_modules': prp.learning_modules,
        'weekly_schedule': prp.weekly_schedule,
        'adaptation_triggers': prp.adaptation_triggers,
        'last_updated': prp.last_updated.isoformat(),
        'next_steps': [
            'Start with Week 1 modules',
            'Complete daily micro-lessons (5 min each)',
            'Work on practice projects',
            'Check in weekly for plan adaptation'
        ]
    }

@router.post("/adapt-plan")
def adapt_reskilling_plan(request: PRPAdaptRequest):
    """
    Adapt PRP based on weekly progress
    Updates plan dynamically based on learner performance and market changes
    """
    # In production, fetch existing PRP from database
    # For now, create mock PRP
    from app.models.reskilling_autopilot import PersonalReskillingPlan

    mock_prp = PersonalReskillingPlan(
        worker_id=request.worker_id,
        target_role='Data Scientist',
        current_readiness=45.0,
        target_readiness=85.0,
        estimated_completion_weeks=20,
        learning_modules=[],
        weekly_schedule=[],
        adaptation_triggers=[],
        last_updated=datetime.now()
    )

    # Adapt plan
    adapted_prp = autopilot.adapt_plan_weekly(
        current_plan=mock_prp,
        progress_data=request.progress_data,
        market_updates=request.market_updates
    )

    return {
        'adapted': True,
        'reason': 'Plan adapted based on progress and market changes',
        'changes_made': [
            'Adjusted module difficulty',
            'Reprioritized skills based on market demand',
            'Updated completion timeline'
        ],
        'updated_plan': {
            'estimated_completion_weeks': adapted_prp.estimated_completion_weeks,
            'weekly_schedule': adapted_prp.weekly_schedule,
            'last_updated': adapted_prp.last_updated.isoformat()
        }
    }

@router.get("/todays-lesson/{worker_id}")
def get_todays_lesson(worker_id: int):
    """
    Get today's micro-lessons (5-minute learning units)
    Integrated micro-learning feature
    """
    # Mock PRP
    from app.models.reskilling_autopilot import PersonalReskillingPlan

    mock_prp = PersonalReskillingPlan(
        worker_id=worker_id,
        target_role='Data Scientist',
        current_readiness=45.0,
        target_readiness=85.0,
        estimated_completion_weeks=20,
        learning_modules=[
            {
                'module_id': 'module_1',
                'skill_target': 'Python',
                'lessons': [
                    {
                        'lesson_id': 'python_1',
                        'title': 'Python Basics',
                        'duration_minutes': 5,
                        'difficulty': 'beginner',
                        'content': 'Learn Python fundamentals',
                        'practice_exercises': [
                            {'type': 'code', 'question': 'Write a function...'}
                        ]
                    }
                ]
            }
        ],
        weekly_schedule=[
            {
                'week': 1,
                'modules': [{'module_id': 'module_1', 'hours': 10}]
            }
        ],
        adaptation_triggers=[],
        last_updated=datetime.now()
    )

    day_of_week = datetime.now().weekday()

    lesson_plan = autopilot.get_todays_lesson(mock_prp, day_of_week)

    return lesson_plan

@router.get("/ai-tutor/{skill}")
def get_ai_tutor(skill: str, question: str):
    """
    AI tutor for technical subjects
    Provides explanations and guidance
    """
    # Mock AI tutor response (in production, integrate with LLM)
    tutor_response = {
        'skill': skill,
        'question': question,
        'answer': f"Here's how to understand {skill}: [Detailed explanation would come from LLM]",
        'examples': [
            f"Example 1 for {skill}",
            f"Example 2 for {skill}"
        ],
        'practice_problems': [
            f"Try this: Problem 1 for {skill}",
            f"Try this: Problem 2 for {skill}"
        ],
        'additional_resources': [
            f"Resource 1 about {skill}",
            f"Resource 2 about {skill}"
        ]
    }

    return tutor_response

@router.post("/simulate-career")
def simulate_career(request: CareerSimRequest, db: Session = Depends(get_db)):
    """
    Simulate career path with projections
    "What if you become X? Income curve? Burnout? Growth?"
    """
    worker = db.query(Worker).filter(Worker.id == request.worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    worker_profile = {
        'skill_score': 60,  # Mock
        'current_role': worker.current_job_title,
        'years_experience': worker.years_experience
    }

    # Run simulation
    simulation = career_sim.simulate_career_path(
        career_path=request.career_path,
        worker_profile=worker_profile,
        time_horizon_years=request.time_horizon_years
    )

    return {
        'career_path': simulation.career_path,
        'time_horizon_years': simulation.time_horizon_years,
        'income_projection': simulation.income_projection,
        'burnout_curve': simulation.burnout_curve,
        'growth_trajectory': simulation.growth_trajectory,
        'skill_evolution': simulation.skill_evolution,
        'market_value_projection': simulation.market_value_projection,
        'life_satisfaction': simulation.life_satisfaction,
        'summary': simulation.summary_metrics
    }

@router.post("/compare-careers")
def compare_career_paths(request: CareerCompareRequest, db: Session = Depends(get_db)):
    """
    Compare multiple career paths side-by-side
    Helps make informed career decisions
    """
    worker = db.query(Worker).filter(Worker.id == request.worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    worker_profile = {
        'skill_score': 60,
        'current_role': worker.current_job_title,
        'years_experience': worker.years_experience
    }

    # Compare careers
    comparison = career_sim.compare_career_paths(
        worker_profile=worker_profile,
        career_options=request.career_options,
        time_horizon=request.time_horizon_years
    )

    return comparison

@router.get("/skill-market-value/{skill_name}")
def get_skill_market_value_projection(skill_name: str, years: int = 5):
    """
    Project market value of specific skill over time
    Helps prioritize which skills to learn
    """
    # Mock projection (in production, use market data)
    projection = []

    base_value = 75  # Starting market value

    for year in range(years + 1):
        # Different skills have different trajectories
        if 'machine_learning' in skill_name.lower() or 'ai' in skill_name.lower():
            growth_rate = 0.15  # High growth
        elif 'cloud' in skill_name.lower() or 'devops' in skill_name.lower():
            growth_rate = 0.12
        elif 'data' in skill_name.lower():
            growth_rate = 0.10
        else:
            growth_rate = 0.05  # Moderate growth

        value = base_value * ((1 + growth_rate) ** year)

        projection.append({
            'year': year,
            'market_value': round(min(100, value), 2),
            'salary_premium': round(value * 1000, 2),  # $ premium
            'demand_level': 'Very High' if value > 90 else 'High' if value > 70 else 'Moderate'
        })

    return {
        'skill_name': skill_name,
        'projection_years': years,
        'projection': projection,
        'recommendation': 'High priority - Strong growth trajectory' if growth_rate > 0.1 else 'Moderate priority'
    }
