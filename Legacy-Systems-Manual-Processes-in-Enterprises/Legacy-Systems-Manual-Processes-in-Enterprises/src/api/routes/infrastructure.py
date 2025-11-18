"""API routes for Infrastructure Orchestrator."""

from typing import List
from fastapi import APIRouter
from src.infrastructure.models import InfrastructureResource, CostOptimization

router = APIRouter()


@router.get("/resources", response_model=List[InfrastructureResource])
async def get_resources() -> List[InfrastructureResource]:
    """Get infrastructure resources."""
    return []


@router.post("/optimize/cost", response_model=CostOptimization)
async def optimize_costs() -> CostOptimization:
    """Get cost optimization recommendations."""
    return CostOptimization(
        current_cost=10000.0,
        optimized_cost=7500.0,
        savings_percent=25.0,
        actions=["Right-size instances", "Use spot instances"],
    )


@router.get("/health")
async def health_check() -> dict:
    """Health check."""
    return {"status": "healthy", "module": "infrastructure"}
