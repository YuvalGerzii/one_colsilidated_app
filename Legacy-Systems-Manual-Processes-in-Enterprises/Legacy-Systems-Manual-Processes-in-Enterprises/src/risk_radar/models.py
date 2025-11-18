"""Models for Risk Radar."""

from datetime import datetime
from enum import Enum
from typing import Dict, Any, List
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    """Risk severity levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class RiskAlert(BaseModel):
    """Risk alert."""
    id: UUID = Field(default_factory=uuid4)
    title: str
    description: str
    level: RiskLevel
    category: str
    detected_at: datetime = Field(default_factory=datetime.utcnow)
    affected_systems: List[str] = Field(default_factory=list)
    recommended_actions: List[str] = Field(default_factory=list)


class AnomalyDetection(BaseModel):
    """Anomaly detection result."""
    anomaly_score: float
    is_anomalous: bool
    details: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class CompliancePrediction(BaseModel):
    """Compliance failure prediction."""
    regulation: str
    failure_probability: float
    risk_factors: List[str]
    mitigation_steps: List[str]
