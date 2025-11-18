"""
Core types and data models for the multi-agent system.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
import uuid


class TaskStatus(Enum):
    """Status of a task."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class MessageType(Enum):
    """Type of message between agents."""
    TASK_ASSIGNMENT = "task_assignment"
    TASK_RESULT = "task_result"
    QUERY = "query"
    RESPONSE = "response"
    BROADCAST = "broadcast"
    ACKNOWLEDGMENT = "acknowledgment"
    ERROR = "error"


class AgentRole(Enum):
    """Role of an agent in the system."""
    ORCHESTRATOR = "orchestrator"
    WORKER = "worker"
    SPECIALIST = "specialist"


@dataclass
class AgentCapability:
    """Capability that an agent possesses."""
    name: str
    description: str = ""
    proficiency: float = 1.0  # 0.0 to 1.0

    def __str__(self):
        return self.name


@dataclass
class Task:
    """A task to be executed by an agent."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    description: str = ""
    requirements: List[str] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    priority: int = 1  # Higher is more important
    deadline: Optional[datetime] = None
    status: TaskStatus = TaskStatus.PENDING
    assigned_to: Optional[str] = None
    parent_task_id: Optional[str] = None
    subtasks: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary."""
        return {
            "id": self.id,
            "description": self.description,
            "requirements": self.requirements,
            "context": self.context,
            "priority": self.priority,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "status": self.status.value,
            "assigned_to": self.assigned_to,
            "parent_task_id": self.parent_task_id,
            "subtasks": self.subtasks,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "metadata": self.metadata,
        }


@dataclass
class Result:
    """Result of a task execution."""
    task_id: str
    success: bool
    data: Any = None
    error: Optional[str] = None
    agent_id: str = ""
    execution_time: float = 0.0  # seconds
    quality_score: float = 0.0  # 0.0 to 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            "task_id": self.task_id,
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "agent_id": self.agent_id,
            "execution_time": self.execution_time,
            "quality_score": self.quality_score,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class Message:
    """Message passed between agents."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    sender: str = ""
    recipient: str = ""  # Empty string means broadcast
    message_type: MessageType = MessageType.QUERY
    content: Any = None
    priority: int = 1
    requires_response: bool = False
    in_response_to: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    ttl: int = 300  # Time to live in seconds
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary."""
        return {
            "id": self.id,
            "sender": self.sender,
            "recipient": self.recipient,
            "message_type": self.message_type.value,
            "content": self.content,
            "priority": self.priority,
            "requires_response": self.requires_response,
            "in_response_to": self.in_response_to,
            "timestamp": self.timestamp.isoformat(),
            "ttl": self.ttl,
            "metadata": self.metadata,
        }


@dataclass
class Experience:
    """An experience for reinforcement learning."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    agent_id: str = ""
    state: Dict[str, Any] = field(default_factory=dict)
    action: str = ""
    reward: float = 0.0
    next_state: Dict[str, Any] = field(default_factory=dict)
    done: bool = False
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert experience to dictionary."""
        return {
            "id": self.id,
            "agent_id": self.agent_id,
            "state": self.state,
            "action": self.action,
            "reward": self.reward,
            "next_state": self.next_state,
            "done": self.done,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }


@dataclass
class AgentState:
    """Current state of an agent."""
    agent_id: str
    status: str = "idle"  # idle, busy, error
    current_task: Optional[str] = None
    completed_tasks: int = 0
    failed_tasks: int = 0
    average_execution_time: float = 0.0
    last_active: datetime = field(default_factory=datetime.now)
    capabilities: List[AgentCapability] = field(default_factory=list)
    performance_score: float = 1.0  # Updated through RL
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert agent state to dictionary."""
        return {
            "agent_id": self.agent_id,
            "status": self.status,
            "current_task": self.current_task,
            "completed_tasks": self.completed_tasks,
            "failed_tasks": self.failed_tasks,
            "average_execution_time": self.average_execution_time,
            "last_active": self.last_active.isoformat(),
            "capabilities": [c.name for c in self.capabilities],
            "performance_score": self.performance_score,
            "metadata": self.metadata,
        }


@dataclass
class SystemMetrics:
    """Metrics for the entire system."""
    total_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    active_agents: int = 0
    average_task_time: float = 0.0
    success_rate: float = 0.0
    total_rewards: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary."""
        return {
            "total_tasks": self.total_tasks,
            "completed_tasks": self.completed_tasks,
            "failed_tasks": self.failed_tasks,
            "active_agents": self.active_agents,
            "average_task_time": self.average_task_time,
            "success_rate": self.success_rate,
            "total_rewards": self.total_rewards,
            "timestamp": self.timestamp.isoformat(),
        }
