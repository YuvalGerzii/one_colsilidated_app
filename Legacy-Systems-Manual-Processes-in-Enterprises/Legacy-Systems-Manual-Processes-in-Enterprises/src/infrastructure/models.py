"""Models for Infrastructure Orchestrator."""

from typing import Dict, Any, List
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class InfrastructureResource(BaseModel):
    """Infrastructure resource."""
    id: UUID = Field(default_factory=uuid4)
    type: str
    status: str
    metrics: Dict[str, float]


class CostOptimization(BaseModel):
    """Cost optimization recommendation."""
    current_cost: float
    optimized_cost: float
    savings_percent: float
    actions: List[str]


class ScalingDecision(BaseModel):
    """Auto-scaling decision."""
    resource_id: UUID
    current_capacity: int
    target_capacity: int
    reason: str
