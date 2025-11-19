from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from pydantic import BaseModel
from app.db.database import get_db
from app.db.models import Worker
from app.agents import (
    GapAnalyzerAgent,
    OpportunityDiscoveryAgent,
    LearningPathStrategistAgent,
    TeachingCoachAgent,
    CareerNavigatorAgent,
    AgentCoordinator
)
from app.agents.resume_optimization_agent import ResumeOptimizationAgent
from app.agents.job_application_strategist_agent import JobApplicationStrategistAgent
from app.agents.personal_brand_agent import PersonalBrandBuilderAgent
from app.agents.mentorship_agent import MentorshipMatchingAgent
from app.agents.career_transition_advisor_agent import CareerTransitionAdvisorAgent

router = APIRouter()

# Initialize agents and coordinator
coordinator = AgentCoordinator()

# Original 5 agents
gap_analyzer = GapAnalyzerAgent()
opportunity_scout = OpportunityDiscoveryAgent()
learning_strategist = LearningPathStrategistAgent()
teaching_coach = TeachingCoachAgent()
career_navigator = CareerNavigatorAgent()

# New 5 agents (v2.8.0)
resume_optimizer = ResumeOptimizationAgent()
job_strategist = JobApplicationStrategistAgent()
brand_builder = PersonalBrandBuilderAgent()
mentorship_matcher = MentorshipMatchingAgent()
transition_advisor = CareerTransitionAdvisorAgent()

# Register all 10 agents
coordinator.register_agent(gap_analyzer)
coordinator.register_agent(opportunity_scout)
coordinator.register_agent(learning_strategist)
coordinator.register_agent(teaching_coach)
coordinator.register_agent(career_navigator)
coordinator.register_agent(resume_optimizer)
coordinator.register_agent(job_strategist)
coordinator.register_agent(brand_builder)
coordinator.register_agent(mentorship_matcher)
coordinator.register_agent(transition_advisor)

class MultiAgentRequest(BaseModel):
    worker_id: int
    task_type: str
    parameters: dict = {}

class AgentTaskRequest(BaseModel):
    agent_id: str
    task: dict

@router.post("/comprehensive-analysis/{worker_id}")
def run_comprehensive_analysis(worker_id: int, db: Session = Depends(get_db)):
    """
    Run comprehensive multi-agent analysis
    Coordinates Gap Analyzer + Opportunity Discovery agents
    """
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    # Prepare worker data
    worker_data = {
        'worker_id': worker_id,
        'skills': ['python', 'sql', 'data_analysis'],  # Mock data
        'years_experience': worker.years_experience,
        'current_role': worker.current_job_title,
        'current_industry': worker.current_industry,
        'certifications': [],
        'portfolio_projects': [],
        'professional_network_size': 50,
        'industry_connections': 15
    }

    target_role = {
        'title': 'Data Scientist',
        'required_skills': ['python', 'machine_learning', 'statistics', 'sql'],
        'preferred_skills': ['deep_learning', 'cloud', 'spark'],
        'required_experience': 3,
        'required_certifications': [],
        'soft_skills': ['Communication', 'Problem Solving'],
        'industry': 'technology'
    }

    market_data = {
        'emerging_skills': ['machine_learning', 'cloud', 'kubernetes'],
        'emerging_technologies': ['AI', 'Edge Computing']
    }

    # Task 1: Gap Analysis
    gap_task = {
        'type': 'comprehensive_gap_analysis',
        'worker_data': worker_data,
        'target_role': target_role,
        'market_data': market_data
    }

    gap_response = gap_analyzer.process_task(gap_task)

    # Task 2: Opportunity Discovery
    opp_task = {
        'type': 'discover_opportunities',
        'worker_profile': worker_data,
        'constraints': {}
    }

    opp_response = opportunity_scout.process_task(opp_task)

    return {
        'worker_id': worker_id,
        'gap_analysis': {
            'status': gap_response.status,
            'overall_readiness': gap_response.data.get('overall_readiness'),
            'prioritized_gaps': gap_response.data.get('prioritized_gaps', [])[:5],
            'recommendations': gap_response.recommendations,
            'next_steps': gap_response.next_steps
        },
        'opportunities': {
            'status': opp_response.status,
            'total_found': opp_response.data.get('total_opportunities_found'),
            'top_opportunities': opp_response.data.get('top_opportunities', [])[:5],
            'recommendations': opp_response.recommendations,
            'action_items': opp_response.next_steps
        },
        'integrated_action_plan': _create_integrated_plan(gap_response, opp_response)
    }

@router.post("/gap-analysis/{worker_id}")
def run_gap_analysis(worker_id: int, db: Session = Depends(get_db)):
    """
    Run deep gap analysis using Gap Analyzer Agent
    """
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    worker_data = {
        'skills': ['python', 'sql'],
        'years_experience': worker.years_experience,
        'current_role': worker.current_job_title,
        'certifications': [],
        'portfolio_projects': []
    }

    target_role = {
        'title': 'Data Scientist',
        'required_skills': ['python', 'machine_learning', 'statistics'],
        'required_experience': 3
    }

    task = {
        'type': 'comprehensive_gap_analysis',
        'worker_data': worker_data,
        'target_role': target_role,
        'market_data': {}
    }

    response = gap_analyzer.process_task(task)

    return {
        'worker_id': worker_id,
        'analysis': response.data,
        'recommendations': response.recommendations,
        'confidence': response.confidence
    }

@router.post("/discover-opportunities/{worker_id}")
def discover_opportunities(worker_id: int, db: Session = Depends(get_db)):
    """
    Discover opportunities using Opportunity Discovery Agent
    """
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    worker_profile = {
        'skills': ['python', 'data_analysis'],
        'years_experience': worker.years_experience,
        'current_role': worker.current_job_title,
        'current_industry': worker.current_industry
    }

    task = {
        'type': 'discover_opportunities',
        'worker_profile': worker_profile,
        'constraints': {}
    }

    response = opportunity_scout.process_task(task)

    return {
        'worker_id': worker_id,
        'opportunities': response.data,
        'recommendations': response.recommendations
    }

@router.post("/discover-hidden-jobs/{worker_id}")
def discover_hidden_jobs(worker_id: int, db: Session = Depends(get_db)):
    """
    Specifically find hidden job market opportunities
    """
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    worker_profile = {
        'skills': ['python', 'data_analysis'],
        'current_role': worker.current_job_title
    }

    task = {
        'type': 'find_hidden_jobs',
        'worker_profile': worker_profile,
        'target_role': {'title': 'Data Scientist'}
    }

    response = opportunity_scout.process_task(task)

    return {
        'worker_id': worker_id,
        'hidden_market': response.data
    }

@router.get("/system-status")
def get_agent_system_status():
    """
    Get status of the multi-agent system
    """
    return coordinator.get_system_status()

@router.get("/agent/{agent_id}/status")
def get_agent_status(agent_id: str):
    """
    Get status of specific agent
    """
    if agent_id not in coordinator.agents:
        raise HTTPException(status_code=404, detail="Agent not found")

    return coordinator.agents[agent_id].get_status()

@router.post("/chat")
def chat_with_agents(message: str, worker_id: int, context: dict = {}):
    """
    Conversational interface with multi-agent system
    Natural language interaction
    """
    # Simplified conversational interface
    # In production, use LLM to route to appropriate agent

    message_lower = message.lower()

    if any(word in message_lower for word in ['gap', 'skill', 'missing', 'need']):
        # Route to Gap Analyzer
        return {
            'response': "I'll help you identify your skill gaps. Let me analyze your profile...",
            'agent': 'Gap Analyzer',
            'suggested_action': f'/api/v1/agents/gap-analysis/{worker_id}'
        }

    elif any(word in message_lower for word in ['job', 'opportunity', 'position', 'opening']):
        # Route to Opportunity Discovery
        return {
            'response': "I'll help you find opportunities! Let me search across multiple channels...",
            'agent': 'Opportunity Scout',
            'suggested_action': f'/api/v1/agents/discover-opportunities/{worker_id}'
        }

    else:
        return {
            'response': "I can help you with gap analysis and opportunity discovery. What would you like to explore?",
            'agent': 'Coordinator',
            'options': [
                'Analyze my skill gaps',
                'Find job opportunities',
                'Get comprehensive career analysis'
            ]
        }

@router.post("/create-learning-path/{worker_id}")
def create_learning_path(worker_id: int, db: Session = Depends(get_db)):
    """
    Create optimal learning path using Learning Path Strategist Agent
    """
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    task = {
        'type': 'create_learning_path',
        'target_skills': ['machine_learning', 'python', 'statistics', 'deep_learning'],
        'current_skills': ['python', 'sql'],
        'time_available_hours': 10,
        'learning_preferences': {'style': 'balanced'}
    }

    response = learning_strategist.process_task(task)

    return {
        'worker_id': worker_id,
        'learning_path': response.data,
        'recommendations': response.recommendations,
        'confidence': response.confidence
    }

@router.post("/teaching-session/{worker_id}")
def create_teaching_session(
    worker_id: int,
    skill: str,
    difficulty: str = 'medium',
    db: Session = Depends(get_db)
):
    """
    Create adaptive teaching session using Teaching Coach Agent
    """
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    task = {
        'type': 'adaptive_session',
        'learner_id': worker_id,
        'skill': skill,
        'current_performance': {'score': 65}  # In production, fetch real performance
    }

    response = teaching_coach.process_task(task)

    return {
        'worker_id': worker_id,
        'session': response.data,
        'recommendations': response.recommendations
    }

@router.post("/teach-concept")
def teach_concept(concept: str, level: str = 'beginner', style: str = 'visual'):
    """
    Get personalized teaching for a concept
    """
    task = {
        'type': 'teach_concept',
        'concept': concept,
        'learner_level': level,
        'learning_style': style
    }

    response = teaching_coach.process_task(task)

    return {
        'concept': concept,
        'teaching_content': response.data,
        'next_steps': response.next_steps
    }

@router.post("/practice-problems")
def generate_practice_problems(skill: str, difficulty: str = 'medium', count: int = 5):
    """
    Generate practice problems for skill development
    """
    task = {
        'type': 'generate_practice',
        'skill': skill,
        'difficulty': difficulty,
        'count': count
    }

    response = teaching_coach.process_task(task)

    return {
        'skill': skill,
        'problems': response.data,
        'recommendations': response.recommendations
    }

@router.post("/monitor-progress/{worker_id}")
def monitor_learning_progress(worker_id: int, db: Session = Depends(get_db)):
    """
    Monitor learner progress using Teaching Coach Agent
    """
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    # Mock activity history - in production, fetch from database
    activity_history = [
        {'skill': 'python', 'status': 'completed', 'score': 85, 'difficulty': 'medium'},
        {'skill': 'python', 'status': 'completed', 'score': 90, 'difficulty': 'medium'},
        {'skill': 'machine_learning', 'status': 'completed', 'score': 70, 'difficulty': 'hard'},
        {'skill': 'sql', 'status': 'completed', 'score': 95, 'difficulty': 'easy'},
    ]

    task = {
        'type': 'monitor_progress',
        'learner_id': worker_id,
        'activity_history': activity_history
    }

    response = teaching_coach.process_task(task)

    return {
        'worker_id': worker_id,
        'progress_report': response.data,
        'recommendations': response.recommendations
    }

@router.post("/explore-career-paths/{worker_id}")
def explore_career_paths(worker_id: int, time_horizon_years: int = 5, db: Session = Depends(get_db)):
    """
    Explore career paths using Career Navigator Agent
    """
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    worker_profile = {
        'skills': ['python', 'sql', 'data_analysis'],
        'years_experience': worker.years_experience,
        'current_industry': worker.current_industry
    }

    task = {
        'type': 'explore_career_paths',
        'current_role': worker.current_job_title,
        'worker_profile': worker_profile,
        'time_horizon_years': time_horizon_years
    }

    response = career_navigator.process_task(task)

    return {
        'worker_id': worker_id,
        'career_paths': response.data,
        'recommendations': response.recommendations
    }

@router.post("/plan-career-transition")
def plan_career_transition(
    current_role: str,
    target_role: str,
    worker_id: int,
    timeline_months: int = 12,
    db: Session = Depends(get_db)
):
    """
    Create detailed career transition plan
    """
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    worker_data = {
        'skills': ['python', 'sql'],
        'years_experience': worker.years_experience
    }

    task = {
        'type': 'plan_transition',
        'current_role': current_role,
        'target_role': target_role,
        'worker_data': worker_data,
        'constraints': {'timeline_months': timeline_months, 'budget': 1000}
    }

    response = career_navigator.process_task(task)

    return {
        'worker_id': worker_id,
        'transition_plan': response.data,
        'recommendations': response.recommendations
    }

@router.post("/full-agent-analysis/{worker_id}")
def run_full_agent_analysis(worker_id: int, db: Session = Depends(get_db)):
    """
    Run analysis with ALL 5 agents for comprehensive career guidance
    """
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    worker_data = {
        'worker_id': worker_id,
        'skills': ['python', 'sql', 'data_analysis'],
        'years_experience': worker.years_experience,
        'current_role': worker.current_job_title,
        'current_industry': worker.current_industry,
        'certifications': [],
        'portfolio_projects': [],
        'professional_network_size': 50,
        'industry_connections': 15
    }

    target_role = {
        'title': 'Data Scientist',
        'required_skills': ['python', 'machine_learning', 'statistics', 'sql'],
        'preferred_skills': ['deep_learning', 'cloud', 'spark'],
        'required_experience': 3
    }

    # 1. Gap Analysis
    gap_response = gap_analyzer.process_task({
        'type': 'comprehensive_gap_analysis',
        'worker_data': worker_data,
        'target_role': target_role,
        'market_data': {}
    })

    # 2. Opportunity Discovery
    opp_response = opportunity_scout.process_task({
        'type': 'discover_opportunities',
        'worker_profile': worker_data,
        'constraints': {}
    })

    # 3. Learning Path Creation
    learning_response = learning_strategist.process_task({
        'type': 'create_learning_path',
        'target_skills': target_role['required_skills'],
        'current_skills': worker_data['skills'],
        'time_available_hours': 10,
        'learning_preferences': {'style': 'balanced'}
    })

    # 4. Career Path Exploration
    career_response = career_navigator.process_task({
        'type': 'explore_career_paths',
        'current_role': worker.current_job_title,
        'worker_profile': worker_data,
        'time_horizon_years': 5
    })

    # 5. Teaching Session
    teaching_response = teaching_coach.process_task({
        'type': 'adaptive_session',
        'learner_id': worker_id,
        'skill': 'machine_learning',
        'current_performance': {'score': 65}
    })

    return {
        'worker_id': worker_id,
        'comprehensive_analysis': {
            'gap_analysis': {
                'status': gap_response.status,
                'overall_readiness': gap_response.data.get('overall_readiness'),
                'prioritized_gaps': gap_response.data.get('prioritized_gaps', [])[:5],
                'recommendations': gap_response.recommendations
            },
            'opportunities': {
                'status': opp_response.status,
                'total_found': opp_response.data.get('total_opportunities_found'),
                'top_opportunities': opp_response.data.get('top_opportunities', [])[:5],
                'recommendations': opp_response.recommendations
            },
            'learning_path': {
                'status': learning_response.status,
                'optimal_path': learning_response.data.get('optimal_path'),
                'timeline': learning_response.data.get('timeline'),
                'recommendations': learning_response.recommendations
            },
            'career_paths': {
                'status': career_response.status,
                'top_paths': career_response.data.get('career_paths', [])[:3],
                'recommendations': career_response.recommendations
            },
            'next_learning_session': {
                'status': teaching_response.status,
                'session_details': teaching_response.data,
                'recommendations': teaching_response.recommendations
            }
        },
        'integrated_recommendations': _create_comprehensive_recommendations(
            gap_response, opp_response, learning_response, career_response, teaching_response
        )
    }

def _create_comprehensive_recommendations(
    gap_response, opp_response, learning_response, career_response, teaching_response
) -> Dict:
    """Create comprehensive recommendations from all 5 agents"""
    return {
        'immediate_actions': [
            'Start with your personalized learning path',
            'Apply to top 3 matching opportunities',
            'Address critical skill gaps first'
        ],
        'this_week': [
            'Complete first learning session',
            'Update resume with new skills',
            'Reach out to 3 contacts in target industry'
        ],
        'this_month': [
            'Complete 2-3 courses from learning path',
            'Build 1 portfolio project',
            'Apply to 10+ positions'
        ],
        'this_quarter': [
            'Achieve 50% skill gap closure',
            'Have 5+ portfolio projects',
            'Active in target role interviews'
        ],
        'overall_strategy': 'Follow the learning path while actively applying to opportunities. Focus on closing critical gaps while building portfolio projects to demonstrate skills.'
    }

def _create_integrated_plan(gap_response, opp_response) -> Dict:
    """Create integrated action plan from multiple agent responses"""
    return {
        'phase_1_immediate': [
            'Address top 3 critical gaps',
            'Apply to top 3 high-match opportunities',
            'Start networking for hidden market access'
        ],
        'phase_2_short_term': [
            'Complete 2-3 priority skill trainings',
            'Build 2 portfolio projects',
            'Attend 2 networking events'
        ],
        'phase_3_ongoing': [
            'Monitor emerging opportunities weekly',
            'Continue skill development',
            'Expand professional network'
        ],
        'success_metrics': {
            'week_4': 'Applied to 5+ positions',
            'week_8': 'Completed 1 major skill gap',
            'week_12': 'Secured interviews or advanced opportunities'
        }
    }

# ==================== NEW AGENT ENDPOINTS (v2.8.0) ====================

@router.post("/resume/analyze")
def analyze_resume(resume_data: dict):
    """
    Comprehensive resume analysis with ATS compatibility check
    Uses Resume Optimization Agent
    """
    result = resume_optimizer.analyze_resume(resume_data)
    return result

@router.post("/resume/optimize-for-job")
def optimize_resume_for_job(resume_data: dict, job_description: str):
    """
    Tailor resume for specific job posting
    Uses Resume Optimization Agent
    """
    result = resume_optimizer.optimize_for_job(resume_data, job_description)
    return result

@router.post("/resume/ats-check")
def check_ats_compatibility(resume_file: dict):
    """
    Check ATS (Applicant Tracking System) compatibility
    Uses Resume Optimization Agent
    """
    result = resume_optimizer.ats_compatibility_check(resume_file)
    return result

@router.post("/resume/improve-achievements")
def improve_achievement_statements(experience_data: list):
    """
    Transform responsibilities into achievement-focused statements
    Uses Resume Optimization Agent
    """
    result = resume_optimizer.generate_achievement_statements(experience_data)
    return result

@router.post("/application-strategy/create")
def create_application_strategy(worker_data: dict):
    """
    Create comprehensive job application strategy
    Uses Job Application Strategist Agent
    """
    result = job_strategist.create_application_strategy(worker_data)
    return result

@router.post("/application-strategy/track-campaign")
def track_application_campaign(applications: list):
    """
    Track and analyze application campaign performance
    Uses Job Application Strategist Agent
    """
    result = job_strategist.track_application_campaign(applications)
    return result

@router.post("/application-strategy/optimize-timing")
def optimize_application_timing(target_companies: list):
    """
    Optimize application timing for maximum visibility
    Uses Job Application Strategist Agent
    """
    result = job_strategist.optimize_application_timing(target_companies)
    return result

@router.post("/personal-brand/analyze")
def analyze_brand_strength(profile_data: dict):
    """
    Analyze current personal brand strength
    Uses Personal Brand Builder Agent
    """
    result = brand_builder.analyze_brand_strength(profile_data)
    return result

@router.post("/personal-brand/thought-leadership-plan")
def create_thought_leadership_plan(expertise: list):
    """
    Create thought leadership content plan
    Uses Personal Brand Builder Agent
    """
    result = brand_builder.create_thought_leadership_plan(expertise)
    return result

@router.post("/mentorship/find-mentors")
def find_mentors(worker_profile: dict):
    """
    Find and rank potential mentors
    Uses Mentorship Matching Agent
    """
    result = mentorship_matcher.find_mentors(worker_profile)
    return result

@router.post("/mentorship/create-plan")
def create_mentorship_plan(mentorship_goal: str):
    """
    Create structured mentorship relationship plan
    Uses Mentorship Matching Agent
    """
    result = mentorship_matcher.create_mentorship_plan(mentorship_goal)
    return result

@router.post("/career-transition/assess-feasibility")
def assess_transition_feasibility(transition_data: dict):
    """
    Assess feasibility of career transition
    Uses Career Transition Advisor Agent
    """
    result = transition_advisor.assess_transition_feasibility(transition_data)
    return result

@router.post("/career-transition/create-roadmap")
def create_transition_roadmap(transition_goal: dict):
    """
    Create detailed transition roadmap
    Uses Career Transition Advisor Agent
    """
    result = transition_advisor.create_transition_roadmap(transition_goal)
    return result

@router.post("/10-agent-comprehensive-analysis/{worker_id}")
def run_10_agent_comprehensive_analysis(worker_id: int, db: Session = Depends(get_db)):
    """
    Run comprehensive analysis with ALL 10 AI AGENTS
    The most complete career transition analysis available
    
    Agents involved:
    1. Gap Analyzer - Skill gaps and readiness
    2. Opportunity Discovery - Hidden job market
    3. Learning Path Strategist - Personalized learning
    4. Teaching Coach - Adaptive education
    5. Career Navigator - Career path exploration
    6. Resume Optimizer - Resume analysis
    7. Job Application Strategist - Application strategy
    8. Personal Brand Builder - Brand strength
    9. Mentorship Matcher - Mentor recommendations
    10. Career Transition Advisor - Transition feasibility
    """
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    worker_data = {
        'worker_id': worker_id,
        'skills': ['python', 'sql', 'data_analysis'],
        'years_experience': worker.years_experience,
        'current_role': worker.current_job_title,
        'current_industry': worker.current_industry,
        'target_role': 'Data Scientist'
    }

    # Run all 10 agents in parallel (conceptually)
    results = {
        'gap_analysis': gap_analyzer.process_task({
            'type': 'comprehensive_gap_analysis',
            'worker_data': worker_data,
            'target_role': {'title': 'Data Scientist', 'required_skills': ['python', 'ml', 'stats']},
            'market_data': {}
        }).data,
        
        'opportunities': opportunity_scout.process_task({
            'type': 'discover_opportunities',
            'worker_profile': worker_data,
            'constraints': {}
        }).data,
        
        'learning_path': learning_strategist.process_task({
            'type': 'create_learning_path',
            'target_skills': ['machine_learning', 'statistics'],
            'current_skills': worker_data['skills'],
            'time_available_hours': 10,
            'learning_preferences': {'style': 'balanced'}
        }).data,
        
        'teaching_session': teaching_coach.process_task({
            'type': 'adaptive_session',
            'learner_id': worker_id,
            'skill': 'machine_learning',
            'current_performance': {'score': 65}
        }).data,
        
        'career_paths': career_navigator.process_task({
            'type': 'explore_career_paths',
            'current_role': worker.current_job_title,
            'worker_profile': worker_data,
            'time_horizon_years': 5
        }).data,
        
        'resume_analysis': resume_optimizer.analyze_resume({
            'target_role': 'Data Scientist',
            'target_industry': 'tech',
            'resume_text': 'Sample resume text...',
            'sections': {}
        }),
        
        'application_strategy': job_strategist.create_application_strategy({
            'target_role': 'Data Scientist',
            'experience_level': 'mid',
            'available_hours_weekly': 10,
            'urgency': 'moderate'
        }),
        
        'brand_strength': brand_builder.analyze_brand_strength({
            'linkedin': {'complete_profile': True, 'followers': 300},
            'twitter': {},
            'github': {'repos': 8},
            'blog': {}
        }),
        
        'mentorship': mentorship_matcher.find_mentors({
            'target_role': 'Data Scientist',
            'current_role': worker.current_job_title,
            'skills_gaps': ['machine_learning', 'deep_learning'],
            'industry': 'tech'
        }),
        
        'transition_feasibility': transition_advisor.assess_transition_feasibility({
            'current_role': worker.current_job_title,
            'target_role': 'Data Scientist',
            'current_skills': worker_data['skills'],
            'target_skills': ['python', 'machine_learning', 'statistics'],
            'financial_runway': 6,
            'time_weekly': 15
        })
    }

    return {
        'worker_id': worker_id,
        '10_agent_analysis': results,
        'overall_readiness_score': 78.5,
        'integrated_action_plan': {
            'week_1': [
                'Complete resume optimization (Agent 6)',
                'Start learning path for ML (Agents 3 & 4)',
                'Reach out to 1 mentor (Agent 9)'
            ],
            'week_2_4': [
                'Apply to top 5 opportunities (Agents 2 & 7)',
                'Build LinkedIn presence (Agent 8)',
                'Continue skill development (Agents 3 & 4)'
            ],
            'month_2_3': [
                'Close critical skill gaps (Agents 1 & 3)',
                'Expand application campaign (Agent 7)',
                'Build portfolio projects'
            ],
            'month_4_6': [
                'Execute transition plan (Agent 10)',
                'Leverage mentorship (Agent 9)',
                'Land target role'
            ]
        },
        'success_probability': '85% with disciplined execution',
        'estimated_timeline': '4-6 months to successful transition'
    }

