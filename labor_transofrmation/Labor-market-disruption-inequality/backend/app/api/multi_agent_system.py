"""
Multi-Agent System API

Endpoints for interacting with the distributed multi-agent orchestration system
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

from ..agents.multi_agent_orchestrator import (
    create_freelance_multi_agent_system,
    TaskPriority,
    AgentRole,
    MultiAgentOrchestrator
)

router = APIRouter()

# Global orchestrator instance (in production, use dependency injection)
orchestrator, agents = create_freelance_multi_agent_system()


# ==================== REQUEST MODELS ====================

class TaskPriorityModel(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class AgentRoleModel(str, Enum):
    PROFILE_OPTIMIZER = "profile_optimizer"
    JOB_MATCHER = "job_matcher"
    PRICING_STRATEGIST = "pricing_strategist"
    PROPOSAL_WRITER = "proposal_writer"
    MARKET_ANALYST = "market_analyst"
    CAREER_PLANNER = "career_planner"
    COMPETITION_ANALYZER = "competition_analyzer"
    NEGOTIATION_ADVISOR = "negotiation_advisor"


class CollaborativeTaskRequest(BaseModel):
    task_type: str = Field(..., description="Type of collaborative task")
    description: str = Field(..., description="Task description")
    required_agents: List[AgentRoleModel] = Field(..., description="Required agent roles")
    input_data: Dict[str, Any] = Field(..., description="Input data for task")
    priority: TaskPriorityModel = Field(default=TaskPriorityModel.MEDIUM, description="Task priority")


class FreelancerOptimizationRequest(BaseModel):
    freelancer_id: int
    profile_data: Dict
    optimization_goals: List[str] = Field(
        default=["increase_visibility", "optimize_pricing", "improve_job_matching"]
    )


class JobApplicationRequest(BaseModel):
    freelancer_id: int
    freelancer_profile: Dict
    target_categories: List[str] = Field(default=["web_development", "data_analysis"])
    max_jobs: int = Field(default=5, ge=1, le=20)


class CareerGrowthRequest(BaseModel):
    freelancer_id: int
    current_stats: Dict
    goals: Dict
    timeframe_months: int = Field(default=12, ge=3, le=36)


# ==================== ENDPOINTS ====================

@router.post("/collaborative-task/create")
def create_collaborative_task(request: CollaborativeTaskRequest):
    """
    Create a collaborative task that requires multiple agents to work together

    This endpoint demonstrates distributed task allocation and agent coordination
    """
    try:
        # Convert enum models to actual enums
        priority = TaskPriority[request.priority.value]
        required_agents = [AgentRole(role.value) for role in request.required_agents]

        task = orchestrator.create_collaborative_task(
            task_type=request.task_type,
            description=request.description,
            required_agents=required_agents,
            input_data=request.input_data,
            priority=priority
        )

        return {
            "status": "success",
            "task_id": task.task_id,
            "task_type": task.task_type,
            "description": task.description,
            "required_agents": [r.value for r in task.required_agents],
            "priority": task.priority.name,
            "message": "Collaborative task created successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/collaborative-task/{task_id}/execute")
def execute_collaborative_task(task_id: str):
    """
    Execute a collaborative task with distributed agent coordination

    This demonstrates:
    - Task decomposition
    - Competitive bidding among agents
    - Inter-agent communication
    - Collective intelligence emergence
    """
    try:
        task = orchestrator.active_tasks.get(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        result = orchestrator.execute_collaborative_task(task)

        return {
            "status": "success",
            "task_id": task_id,
            "execution_result": result,
            "agents_involved": result.get('agents_involved', []),
            "collective_recommendation": result.get('collective_recommendation', {}),
            "confidence": result.get('confidence', 0),
            "message": "Task executed successfully with multi-agent collaboration"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/optimize-freelancer/multi-agent")
def optimize_freelancer_multi_agent(request: FreelancerOptimizationRequest):
    """
    Comprehensive freelancer optimization using multiple cooperating agents

    Agents involved:
    - Profile Optimizer: Enhances profile content
    - Pricing Strategist: Optimizes rates
    - Market Analyst: Analyzes positioning

    They communicate and coordinate to provide unified recommendations
    """
    try:
        task = orchestrator.create_collaborative_task(
            task_type="optimize_freelancer_profile",
            description=f"Comprehensive optimization for freelancer {request.freelancer_id}",
            required_agents=[
                AgentRole.PROFILE_OPTIMIZER,
                AgentRole.PRICING_STRATEGIST,
                AgentRole.MARKET_ANALYST
            ],
            input_data={
                'freelancer_id': request.freelancer_id,
                'profile_data': request.profile_data,
                'goals': request.optimization_goals
            },
            priority=TaskPriority.HIGH
        )

        result = orchestrator.execute_collaborative_task(task)

        return {
            "status": "success",
            "freelancer_id": request.freelancer_id,
            "optimization_results": result['collective_recommendation'],
            "agents_consulted": result['agents_involved'],
            "confidence": result['confidence'],
            "implementation_priority": result['collective_recommendation'].get('priority_actions', []),
            "estimated_impact": result['collective_recommendation'].get('estimated_impact', ''),
            "message": "Multi-agent optimization completed successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/find-and-apply-jobs/multi-agent")
def find_and_apply_jobs_multi_agent(request: JobApplicationRequest):
    """
    Find jobs and prepare applications using coordinated agents

    Workflow:
    1. Job Matcher finds opportunities
    2. Competition Analyzer evaluates each job
    3. Proposal Writer creates customized proposals

    Agents share information through the shared environment
    """
    try:
        task = orchestrator.create_collaborative_task(
            task_type="find_and_apply_jobs",
            description=f"Find and prepare job applications for freelancer {request.freelancer_id}",
            required_agents=[
                AgentRole.JOB_MATCHER,
                AgentRole.COMPETITION_ANALYZER,
                AgentRole.PROPOSAL_WRITER
            ],
            input_data={
                'freelancer_id': request.freelancer_id,
                'profile': request.freelancer_profile,
                'categories': request.target_categories,
                'max_jobs': request.max_jobs
            },
            priority=TaskPriority.MEDIUM
        )

        result = orchestrator.execute_collaborative_task(task)

        return {
            "status": "success",
            "freelancer_id": request.freelancer_id,
            "recommended_jobs": result['collective_recommendation'].get('recommended_jobs', []),
            "competition_insights": result['collective_recommendation'].get('competition_insights', {}),
            "ready_proposals": result['collective_recommendation'].get('ready_proposals', []),
            "success_probability": result['collective_recommendation'].get('success_probability', 0),
            "application_strategy": result['collective_recommendation'].get('application_strategy', {}),
            "agents_involved": result['agents_involved'],
            "message": "Job discovery and application preparation completed"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/career-growth-plan/multi-agent")
def create_career_growth_plan_multi_agent(request: CareerGrowthRequest):
    """
    Create comprehensive career growth plan using multiple expert agents

    Agents collaborate to synthesize:
    - Market trends and opportunities
    - Pricing evolution strategy
    - Long-term career milestones

    Demonstrates collective intelligence beyond individual agent capabilities
    """
    try:
        task = orchestrator.create_collaborative_task(
            task_type="career_growth_plan",
            description=f"Create {request.timeframe_months}-month career plan for freelancer {request.freelancer_id}",
            required_agents=[
                AgentRole.MARKET_ANALYST,
                AgentRole.PRICING_STRATEGIST,
                AgentRole.CAREER_PLANNER
            ],
            input_data={
                'freelancer_id': request.freelancer_id,
                'current_stats': request.current_stats,
                'goals': request.goals,
                'timeframe_months': request.timeframe_months
            },
            priority=TaskPriority.HIGH
        )

        result = orchestrator.execute_collaborative_task(task)

        return {
            "status": "success",
            "freelancer_id": request.freelancer_id,
            "timeframe_months": request.timeframe_months,
            "market_trends": result['collective_recommendation'].get('market_trends', []),
            "pricing_roadmap": result['collective_recommendation'].get('pricing_roadmap', []),
            "career_milestones": result['collective_recommendation'].get('career_milestones', []),
            "integrated_plan": result['collective_recommendation'].get('integrated_plan', {}),
            "risk_factors": result['collective_recommendation'].get('risk_factors', []),
            "success_indicators": result['collective_recommendation'].get('success_indicators', {}),
            "confidence": result['confidence'],
            "message": "Comprehensive career growth plan created by multi-agent collaboration"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/system/intelligence")
def get_system_intelligence():
    """
    Get emergent intelligence from the multi-agent system

    Shows collective intelligence that emerges from agent interactions:
    - Collaboration patterns
    - Emergent behaviors
    - System-wide performance
    - Knowledge accumulation
    """
    try:
        intelligence = orchestrator.get_system_intelligence()

        return {
            "status": "success",
            "system_intelligence": intelligence,
            "insights": [
                f"System has completed {intelligence['total_tasks_completed']} collaborative tasks",
                f"Average agent performance: {intelligence['avg_agent_performance']:.1f}/100",
                f"Collective knowledge base contains {intelligence['collective_knowledge_items']} insights",
                f"Agents have exchanged {intelligence['total_messages_exchanged']} messages"
            ],
            "emergent_patterns": intelligence.get('emergent_patterns', []),
            "message": "Collective intelligence analysis complete"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agents/status")
def get_all_agents_status():
    """
    Get status of all agents in the system

    Shows individual agent performance and current state
    """
    try:
        agents_status = []

        for agent_id, agent in agents.items():
            status = {
                "agent_id": agent.agent_id,
                "role": agent.role.value,
                "active": agent.active,
                "performance_score": agent.performance_score,
                "capabilities": agent.capabilities,
                "current_task": agent.current_task,
                "completed_tasks_count": len(agent.completed_tasks)
            }
            agents_status.append(status)

        return {
            "status": "success",
            "total_agents": len(agents_status),
            "active_agents": len([a for a in agents_status if a['active']]),
            "agents": agents_status,
            "message": "Agent status retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/communication/message-bus")
def get_message_bus():
    """
    View inter-agent communication messages

    Shows how agents communicate and coordinate
    """
    try:
        messages = orchestrator.environment.message_bus[-50:]  # Last 50 messages

        message_summary = {
            "total_messages": len(orchestrator.environment.message_bus),
            "recent_messages": [
                {
                    "from": msg.get('from_agent'),
                    "to": msg.get('to_agent'),
                    "type": msg.get('message_type'),
                    "timestamp": msg.get('timestamp').isoformat() if msg.get('timestamp') else None,
                    "read": msg.get('read', False)
                }
                for msg in messages
            ]
        }

        # Analyze message patterns
        message_types = {}
        for msg in orchestrator.environment.message_bus:
            msg_type = msg.get('message_type', 'unknown')
            message_types[msg_type] = message_types.get(msg_type, 0) + 1

        return {
            "status": "success",
            "summary": message_summary,
            "message_type_distribution": message_types,
            "message": "Message bus data retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/collaboration/patterns")
def get_collaboration_patterns():
    """
    Analyze agent collaboration patterns

    Shows which agents work best together
    """
    try:
        intelligence = orchestrator.get_system_intelligence()

        patterns = {
            "most_effective_collaborations": intelligence.get('most_effective_collaborations', []),
            "total_collaborative_tasks": len(orchestrator.task_history),
            "success_rate": intelligence.get('success_rate', 0),
            "insights": [
                "Profile Optimizer + Pricing Strategist = Strong synergy",
                "Job Matcher + Competition Analyzer = Better job selection",
                "Market Analyst provides context that improves all other agents' decisions"
            ]
        }

        return {
            "status": "success",
            "collaboration_patterns": patterns,
            "message": "Collaboration patterns analyzed successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/knowledge-base/shared")
def get_shared_knowledge_base():
    """
    Access the shared knowledge base

    Shows collective knowledge accumulated by all agents
    """
    try:
        kb = orchestrator.environment.knowledge_base

        knowledge_items = []
        for key, value in list(kb.items())[:50]:  # First 50 items
            knowledge_items.append({
                "key": key,
                "value": value.get('value'),
                "timestamp": value.get('timestamp').isoformat() if value.get('timestamp') else None,
                "contributors": value.get('contributors', [])
            })

        return {
            "status": "success",
            "total_knowledge_items": len(kb),
            "recent_knowledge": knowledge_items,
            "categories": list(set(key.split('_')[0] for key in kb.keys() if '_' in key)),
            "message": "Shared knowledge base accessed successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/agent/{agent_id}/send-message")
def send_agent_message(agent_id: str, to_agent: str, message_type: str, payload: Dict):
    """
    Send a message from one agent to another

    Demonstrates inter-agent communication
    """
    try:
        if agent_id not in agents:
            raise HTTPException(status_code=404, detail="Sender agent not found")

        agent = agents[agent_id]
        agent.send_message(to_agent, message_type, payload)

        return {
            "status": "success",
            "from_agent": agent_id,
            "to_agent": to_agent,
            "message_type": message_type,
            "message": "Message sent successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tasks/history")
def get_task_history(limit: int = 20):
    """
    Get history of completed collaborative tasks

    Shows system learning and improvement over time
    """
    try:
        tasks = orchestrator.task_history[-limit:]

        task_summaries = []
        for task in tasks:
            task_summaries.append({
                "task_id": task.task_id,
                "task_type": task.task_type,
                "description": task.description,
                "agents_involved": task.assigned_agents,
                "coordinator": task.coordinator_agent,
                "status": task.status,
                "created_at": task.created_at.isoformat(),
                "subtasks_count": len(task.subtasks)
            })

        return {
            "status": "success",
            "total_tasks": len(orchestrator.task_history),
            "recent_tasks": task_summaries,
            "message": "Task history retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/demo/complete-workflow")
def demo_complete_workflow():
    """
    Demonstration of a complete multi-agent workflow

    This endpoint shows all aspects of the multi-agent system:
    1. Task creation
    2. Agent bidding and selection
    3. Task decomposition
    4. Distributed execution
    5. Inter-agent communication
    6. Collective intelligence emergence
    """
    try:
        # Create a comprehensive optimization task
        task = orchestrator.create_collaborative_task(
            task_type="optimize_freelancer_profile",
            description="Complete freelancer optimization demo",
            required_agents=[
                AgentRole.PROFILE_OPTIMIZER,
                AgentRole.PRICING_STRATEGIST,
                AgentRole.MARKET_ANALYST
            ],
            input_data={
                'freelancer_id': 999,
                'profile_data': {
                    'bio': 'Developer with 5 years experience',
                    'hourly_rate': 50,
                    'skills': ['python', 'react'],
                    'portfolio_items': 2
                }
            },
            priority=TaskPriority.HIGH
        )

        # Execute the task
        result = orchestrator.execute_collaborative_task(task)

        # Get system intelligence
        intelligence = orchestrator.get_system_intelligence()

        return {
            "status": "success",
            "demo_results": {
                "task_creation": {
                    "task_id": task.task_id,
                    "agents_required": [r.value for r in task.required_agents]
                },
                "agent_bidding": {
                    "message": "Agents competed for task based on expertise and workload",
                    "selected_agents": result['agents_involved']
                },
                "task_decomposition": {
                    "subtasks_created": len(task.subtasks),
                    "message": "Task broken down into specialized subtasks"
                },
                "distributed_execution": {
                    "coordinator": result.get('coordinator'),
                    "message": "Agents executed subtasks in parallel with coordination"
                },
                "inter_agent_communication": {
                    "total_messages": intelligence['total_messages_exchanged'],
                    "message": "Agents communicated through shared environment"
                },
                "collective_intelligence": {
                    "recommendation": result['collective_recommendation'],
                    "confidence": result['confidence'],
                    "emergent_patterns": intelligence.get('emergent_patterns', [])
                }
            },
            "message": "Complete multi-agent workflow demonstration successful"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
