"""Models for Process Miner."""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class ProcessEvent(BaseModel):
    """Single process event."""
    id: UUID = Field(default_factory=uuid4)
    activity: str
    timestamp: datetime
    resource: str
    data: Dict[str, Any] = Field(default_factory=dict)


class ProcessMap(BaseModel):
    """Discovered process map."""
    id: UUID = Field(default_factory=uuid4)
    name: str
    activities: List[str]
    transitions: List[Dict[str, Any]]
    bottlenecks: List[str]
    frequency: int
    avg_duration_minutes: float


class WorkflowOptimization(BaseModel):
    """Optimized workflow suggestion."""
    original_process: str
    optimized_process: str
    improvements: List[str]
    estimated_time_saving_percent: float
    implementation_steps: List[str]
