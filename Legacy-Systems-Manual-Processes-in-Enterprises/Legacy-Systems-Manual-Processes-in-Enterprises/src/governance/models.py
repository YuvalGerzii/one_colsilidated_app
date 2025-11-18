"""Models for Governance."""

from datetime import datetime
from typing import List, Dict, Any
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class ComplianceStandard(BaseModel):
    """Compliance standard."""
    id: UUID = Field(default_factory=uuid4)
    name: str
    requirements: List[str]
    controls: List[str]


class ComplianceCheck(BaseModel):
    """Compliance check result."""
    standard: str
    status: str
    compliant: bool
    issues: List[str]
    evidence: List[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AuditTrail(BaseModel):
    """Audit trail entry."""
    id: UUID = Field(default_factory=uuid4)
    action: str
    user: str
    timestamp: datetime
    reasoning: str
    data: Dict[str, Any]
