"""Models for Agentic Operations."""

from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional, List
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class AgentType(str, Enum):
    """Agent types."""
    VENDOR_MANAGEMENT = "vendor_management"
    PROCUREMENT = "procurement"
    DOCUMENT_DRAFTING = "document_drafting"
    REPORTING = "reporting"
    CONTRACT_RENEWAL = "contract_renewal"
    RISK_ANALYSIS = "risk_analysis"
    PROJECT_MANAGEMENT = "project_management"
    INVOICE_REVIEW = "invoice_review"
    FINANCIAL_CLOSE = "financial_close"


class AgentTask(BaseModel):
    """Agent task."""
    id: UUID = Field(default_factory=uuid4)
    agent_type: AgentType
    description: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    status: str = "pending"
    result: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Agent(BaseModel):
    """Autonomous agent."""
    id: UUID = Field(default_factory=uuid4)
    type: AgentType
    name: str
    capabilities: List[str]
    active_tasks: List[UUID] = Field(default_factory=list)
