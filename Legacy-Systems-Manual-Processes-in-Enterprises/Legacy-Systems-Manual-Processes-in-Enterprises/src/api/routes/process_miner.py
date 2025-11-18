"""API routes for Process Miner."""

from fastapi import APIRouter
from src.process_miner.models import ProcessMap, WorkflowOptimization

router = APIRouter()


@router.post("/mine", response_model=ProcessMap)
async def mine_processes(events: list) -> ProcessMap:
    """Mine business processes from events."""
    return ProcessMap(
        name="Discovered Process",
        activities=["Start", "Review", "Approve", "End"],
        transitions=[],
        bottlenecks=["Manual Review"],
        frequency=100,
        avg_duration_minutes=45.5,
    )


@router.post("/optimize", response_model=WorkflowOptimization)
async def optimize_workflow(process_map: ProcessMap) -> WorkflowOptimization:
    """Optimize a discovered workflow."""
    return WorkflowOptimization(
        original_process=process_map.name,
        optimized_process="Automated Process",
        improvements=["Remove manual approval step", "Parallel processing"],
        estimated_time_saving_percent=35.0,
        implementation_steps=["Implement AI approval", "Deploy automation"],
    )


@router.get("/health")
async def health_check() -> dict:
    """Health check."""
    return {"status": "healthy", "module": "process_miner"}
