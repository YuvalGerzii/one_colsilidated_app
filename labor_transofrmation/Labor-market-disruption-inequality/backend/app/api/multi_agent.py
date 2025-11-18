"""
Multi-Agent System API Endpoints
Expose MAS workflows, coordination, and monitoring
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime

from backend.app.core.multi_agent_system import (
    MultiAgentCoordinator,
    SharedEnvironment,
    DistributedTask,
    TaskStatus,
    MessageType
)
from backend.app.core.mas_workflows import WorkflowFactory

router = APIRouter(prefix="/mas", tags=["Multi-Agent System"])

# Global coordinator instance (in production, use dependency injection)
_coordinator: Optional[MultiAgentCoordinator] = None


def get_coordinator() -> MultiAgentCoordinator:
    """Get or create global coordinator instance"""
    global _coordinator
    if _coordinator is None:
        _coordinator = MultiAgentCoordinator()
    return _coordinator


# ===== Request/Response Models =====

class WorkflowRequest(BaseModel):
    """Base workflow request"""
    workflow_type: str = Field(..., description="career_transition, learning_consensus, market_analysis, resource_curation")
    parameters: Dict = Field(..., description="Workflow-specific parameters")


class CareerTransitionRequest(BaseModel):
    """Career transition workflow request"""
    worker_id: int
    target_role: str = Field(..., description="Target job role/title")


class LearningConsensusRequest(BaseModel):
    """Learning consensus workflow request"""
    worker_id: int
    target_skills: List[str]
    time_constraint_hours: int = Field(..., gt=0)


class MarketAnalysisRequest(BaseModel):
    """Job market analysis request"""
    industry: str
    region: str
    skills: List[str]


class ResourceCurationRequest(BaseModel):
    """Resource curation request"""
    topic: str
    difficulty_level: str = Field(..., description="beginner, intermediate, advanced, expert")
    learner_preferences: Dict = Field(default_factory=dict)


class CollaborationRequest(BaseModel):
    """Request collaboration between agents"""
    requester_id: str
    task_description: str
    required_agents: List[str]


class TaskDistributionRequest(BaseModel):
    """Distribute a task to agents"""
    task_name: str
    task_description: str
    required_capabilities: List[str]
    input_data: Dict
    priority: int = Field(default=5, ge=1, le=10)


# ===== Workflow Endpoints =====

@router.post("/workflows/career-transition")
async def start_career_transition_workflow(request: CareerTransitionRequest) -> Dict:
    """
    Start comprehensive career transition workflow

    Flow:
    1. Gap Analyzer analyzes skills gap
    2. Opportunity Scout finds matching jobs
    3. Learning Strategist creates learning path
    4. Teaching Coach prepares materials
    5. Career Navigator creates final transition plan

    All agents communicate through shared environment
    """
    coordinator = get_coordinator()

    try:
        result = WorkflowFactory.create_career_transition_workflow(
            coordinator=coordinator,
            worker_id=request.worker_id,
            target_role=request.target_role
        )
        return {
            'success': True,
            'workflow': result,
            'message': 'Career transition workflow initiated'
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/workflows/learning-consensus")
async def start_learning_consensus(request: LearningConsensusRequest) -> Dict:
    """
    Multiple agents negotiate optimal learning strategy

    Demonstrates:
    - Agent proposals and counter-proposals
    - Voting mechanism
    - Consensus building
    """
    coordinator = get_coordinator()

    try:
        result = WorkflowFactory.create_learning_consensus(
            coordinator=coordinator,
            worker_id=request.worker_id,
            target_skills=request.target_skills,
            time_hours=request.time_constraint_hours
        )
        return {
            'success': True,
            'consensus': result,
            'message': 'Learning consensus workflow initiated'
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/workflows/market-analysis")
async def start_market_analysis(request: MarketAnalysisRequest) -> Dict:
    """
    Distributed job market analysis

    Multiple agents analyze different aspects in parallel:
    - Trend analysis
    - Salary analysis
    - Skill demand
    - Competition level
    """
    coordinator = get_coordinator()

    try:
        result = WorkflowFactory.create_market_analysis(
            coordinator=coordinator,
            industry=request.industry,
            region=request.region,
            skills=request.skills
        )
        return {
            'success': True,
            'analysis': result,
            'message': 'Market analysis workflow initiated'
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/workflows/resource-curation")
async def start_resource_curation(request: ResourceCurationRequest) -> Dict:
    """
    Collaborative resource curation by multiple agents

    Agents work together to find and curate best learning resources
    """
    coordinator = get_coordinator()

    try:
        result = WorkflowFactory.create_resource_curation(
            coordinator=coordinator,
            topic=request.topic,
            difficulty=request.difficulty_level,
            preferences=request.learner_preferences
        )
        return {
            'success': True,
            'curation': result,
            'message': 'Resource curation workflow initiated'
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/workflows/{workflow_id}/progress")
async def get_workflow_progress(workflow_id: str) -> Dict:
    """Get workflow execution progress"""
    coordinator = get_coordinator()

    try:
        progress = coordinator.check_workflow_progress(workflow_id)
        return {
            'success': True,
            'progress': progress
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail="Workflow not found")


# ===== Agent Coordination Endpoints =====

@router.post("/collaboration/request")
async def request_collaboration(request: CollaborationRequest) -> Dict:
    """
    Request collaboration between multiple agents

    Returns conversation_id for tracking
    """
    coordinator = get_coordinator()

    try:
        conversation_id = coordinator.request_collaboration(
            requester_id=request.requester_id,
            task_description=request.task_description,
            required_agents=request.required_agents
        )
        return {
            'success': True,
            'conversation_id': conversation_id,
            'message': 'Collaboration request sent to agents'
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tasks/distribute")
async def distribute_task(request: TaskDistributionRequest) -> Dict:
    """
    Distribute task to best available agent

    Uses capability matching and performance scoring
    """
    coordinator = get_coordinator()

    try:
        import uuid
        task = DistributedTask(
            task_id=str(uuid.uuid4()),
            name=request.task_name,
            description=request.task_description,
            required_capabilities=request.required_capabilities,
            input_data=request.input_data,
            priority=request.priority
        )

        success = coordinator.distribute_task(task)

        if success:
            return {
                'success': True,
                'task_id': task.task_id,
                'assigned_agent': task.assigned_agent,
                'message': 'Task distributed successfully'
            }
        else:
            raise HTTPException(status_code=400, detail="No capable agents available")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tasks/{task_id}/status")
async def get_task_status(task_id: str) -> Dict:
    """Get status of a distributed task"""
    coordinator = get_coordinator()

    if task_id not in coordinator.tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    task = coordinator.tasks[task_id]
    return {
        'success': True,
        'task': {
            'task_id': task.task_id,
            'name': task.name,
            'status': task.status.value,
            'assigned_agent': task.assigned_agent,
            'created_at': task.created_at.isoformat() if task.created_at else None,
            'started_at': task.started_at.isoformat() if task.started_at else None,
            'completed_at': task.completed_at.isoformat() if task.completed_at else None,
            'result': task.result,
            'error': task.error,
        }
    }


# ===== Shared Environment Endpoints =====

@router.get("/shared-environment/knowledge/{key}")
async def read_shared_knowledge(key: str) -> Dict:
    """Read value from shared knowledge base"""
    coordinator = get_coordinator()
    value = coordinator.shared_env.read(key)

    return {
        'success': True,
        'key': key,
        'value': value,
        'exists': value is not None
    }


@router.get("/shared-environment/events")
async def get_recent_events(
    limit: int = Query(default=100, le=1000),
    event_type: Optional[str] = None
) -> Dict:
    """Get recent events from shared environment"""
    coordinator = get_coordinator()

    events = coordinator.shared_env.get_recent_events(
        limit=limit,
        event_type=event_type
    )

    return {
        'success': True,
        'events': events,
        'count': len(events)
    }


@router.get("/shared-environment/metrics")
async def get_environment_metrics() -> Dict:
    """Get shared environment metrics"""
    coordinator = get_coordinator()
    metrics = coordinator.shared_env.get_metrics()

    return {
        'success': True,
        'metrics': metrics
    }


# ===== System Status & Monitoring =====

@router.get("/status")
async def get_system_status() -> Dict:
    """Get comprehensive MAS system status"""
    coordinator = get_coordinator()

    try:
        status = coordinator.get_system_status()
        return {
            'success': True,
            'system': status
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agents")
async def list_agents() -> Dict:
    """List all registered agents"""
    coordinator = get_coordinator()

    agents = []
    for agent_id, agent in coordinator.agents.items():
        agents.append({
            'agent_id': agent_id,
            'agent_type': agent.agent_type,
            'active': agent.active,
            'capabilities': agent.capabilities,
            'mas_enabled': agent.mas_enabled,
            'performance': coordinator.performance_metrics.get(agent_id, {})
        })

    return {
        'success': True,
        'agents': agents,
        'total': len(agents)
    }


@router.get("/agents/{agent_id}")
async def get_agent_details(agent_id: str) -> Dict:
    """Get detailed agent information"""
    coordinator = get_coordinator()

    if agent_id not in coordinator.agents:
        raise HTTPException(status_code=404, detail="Agent not found")

    agent = coordinator.agents[agent_id]

    return {
        'success': True,
        'agent': {
            'agent_id': agent_id,
            'agent_type': agent.agent_type,
            'active': agent.active,
            'capabilities': agent.capabilities,
            'queued_messages': len(agent.message_queue),
            'mas_enabled': agent.mas_enabled,
            'performance': coordinator.performance_metrics.get(agent_id, {})
        }
    }


@router.get("/network/visualization")
async def get_agent_network() -> Dict:
    """
    Get agent network visualization data

    Shows:
    - Nodes (agents)
    - Edges (communication patterns)
    - Interaction weights
    """
    coordinator = get_coordinator()

    try:
        network = coordinator.visualize_agent_network()
        return {
            'success': True,
            'network': network
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str) -> Dict:
    """Get message history for a conversation"""
    coordinator = get_coordinator()

    if conversation_id not in coordinator.conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")

    messages = coordinator.conversations[conversation_id]

    return {
        'success': True,
        'conversation_id': conversation_id,
        'messages': [msg.to_dict() for msg in messages],
        'message_count': len(messages)
    }


# ===== Agent Actions =====

@router.post("/agents/{agent_id}/activate")
async def activate_agent(agent_id: str) -> Dict:
    """Activate an agent"""
    coordinator = get_coordinator()

    if agent_id not in coordinator.agents:
        raise HTTPException(status_code=404, detail="Agent not found")

    agent = coordinator.agents[agent_id]
    agent.active = True

    return {
        'success': True,
        'message': f'Agent {agent_id} activated'
    }


@router.post("/agents/{agent_id}/deactivate")
async def deactivate_agent(agent_id: str) -> Dict:
    """Deactivate an agent"""
    coordinator = get_coordinator()

    if agent_id not in coordinator.agents:
        raise HTTPException(status_code=404, detail="Agent not found")

    agent = coordinator.agents[agent_id]
    agent.active = False

    return {
        'success': True,
        'message': f'Agent {agent_id} deactivated'
    }


@router.post("/messages/process")
async def process_pending_messages(max_messages: int = Query(default=10, le=100)) -> Dict:
    """Process pending messages in the system"""
    coordinator = get_coordinator()

    try:
        coordinator.process_messages(max_messages=max_messages)
        return {
            'success': True,
            'message': f'Processed up to {max_messages} messages',
            'remaining': coordinator.message_queue.qsize()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===== Performance & Analytics =====

@router.get("/analytics/performance")
async def get_performance_analytics() -> Dict:
    """Get system-wide performance analytics"""
    coordinator = get_coordinator()

    return {
        'success': True,
        'performance': {
            'by_agent': coordinator.performance_metrics,
            'system_metrics': coordinator.shared_env.get_metrics()
        }
    }


@router.get("/analytics/collaboration-patterns")
async def get_collaboration_patterns() -> Dict:
    """Analyze collaboration patterns between agents"""
    coordinator = get_coordinator()

    # Analyze conversation patterns
    patterns = {
        'total_conversations': len(coordinator.conversations),
        'total_messages': sum(len(msgs) for msgs in coordinator.conversations.values()),
        'active_collaborations': 0,
        'most_collaborative_agents': [],
    }

    # Find most collaborative agents
    agent_message_counts = {}
    for messages in coordinator.conversations.values():
        for msg in messages:
            agent_message_counts[msg.from_agent] = agent_message_counts.get(msg.from_agent, 0) + 1

    if agent_message_counts:
        sorted_agents = sorted(agent_message_counts.items(), key=lambda x: x[1], reverse=True)
        patterns['most_collaborative_agents'] = [
            {'agent_id': agent_id, 'message_count': count}
            for agent_id, count in sorted_agents[:5]
        ]

    return {
        'success': True,
        'collaboration_patterns': patterns
    }
