"""Models for HITL Hub."""

from datetime import datetime
from typing import Dict, Any, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class ApprovalRequest(BaseModel):
    """Approval request."""
    id: UUID = Field(default_factory=uuid4)
    task_id: UUID
    description: str
    ai_recommendation: str
    ai_confidence: float
    human_decision: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = None


class RiskAssessment(BaseModel):
    """Risk assessment for automation."""
    automation_id: UUID
    risk_score: float
    factors: Dict[str, float]
    recommendation: str
