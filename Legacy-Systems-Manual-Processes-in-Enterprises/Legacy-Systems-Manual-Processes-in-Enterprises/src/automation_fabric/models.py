"""Data models for Enterprise Automation Fabric."""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class WorkflowStatus(str, Enum):
    """Workflow execution status."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


class ActionType(str, Enum):
    """Types of automation actions."""

    CLICK = "click"
    TYPE = "type"
    READ = "read"
    NAVIGATE = "navigate"
    WAIT = "wait"
    EXTRACT = "extract"
    VALIDATE = "validate"
    API_CALL = "api_call"


class AutomationAction(BaseModel):
    """Single automation action."""

    action_type: ActionType
    target: str
    value: Optional[str] = None
    timeout: int = 30
    retry_count: int = 3
    metadata: Dict[str, Any] = Field(default_factory=dict)


class WorkflowDefinition(BaseModel):
    """Workflow definition."""

    id: UUID = Field(default_factory=uuid4)
    name: str
    description: Optional[str] = None
    actions: List[AutomationAction]
    frequency: Optional[str] = None  # cron expression
    enabled: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class WorkflowExecution(BaseModel):
    """Workflow execution record."""

    id: UUID = Field(default_factory=uuid4)
    workflow_id: UUID
    status: WorkflowStatus = WorkflowStatus.PENDING
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    logs: List[str] = Field(default_factory=list)


class PatternRecognitionResult(BaseModel):
    """Result of pattern recognition analysis."""

    pattern_id: UUID = Field(default_factory=uuid4)
    pattern_name: str
    frequency: int
    confidence: float
    suggested_workflow: WorkflowDefinition
    detected_at: datetime = Field(default_factory=datetime.utcnow)


class APIEmulationConfig(BaseModel):
    """Configuration for API emulation."""

    system_id: str
    base_url: str
    authentication: Dict[str, Any]
    endpoints: List[Dict[str, Any]]
    rate_limit: Optional[int] = None
    timeout: int = 30
