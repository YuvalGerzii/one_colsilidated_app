"""API routes for HITL Hub."""

from typing import List
from fastapi import APIRouter
from src.hitl_hub.models import ApprovalRequest, RiskAssessment

router = APIRouter()


@router.post("/approvals", response_model=ApprovalRequest)
async def create_approval_request(request: ApprovalRequest) -> ApprovalRequest:
    """Create approval request."""
    return request


@router.get("/approvals/pending", response_model=List[ApprovalRequest])
async def get_pending_approvals() -> List[ApprovalRequest]:
    """Get pending approvals."""
    return []


@router.post("/risk/assess", response_model=RiskAssessment)
async def assess_risk(automation_id: str) -> RiskAssessment:
    """Assess automation risk."""
    from uuid import UUID
    return RiskAssessment(
        automation_id=UUID(automation_id),
        risk_score=0.3,
        factors={"complexity": 0.2, "impact": 0.4},
        recommendation="Approve with monitoring",
    )


@router.get("/health")
async def health_check() -> dict:
    """Health check."""
    return {"status": "healthy", "module": "hitl_hub"}
