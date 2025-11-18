"""API routes for Enterprise Automation Fabric."""

from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.automation_fabric.models import (
    WorkflowDefinition,
    WorkflowExecution,
    APIEmulationConfig,
)
from src.automation_fabric.engine import AutomationEngine, APIEmulator
from src.core.logger import logger

router = APIRouter()
automation_engine = AutomationEngine()
api_emulator = APIEmulator()


@router.post("/workflows", response_model=WorkflowDefinition)
async def create_workflow(workflow: WorkflowDefinition) -> WorkflowDefinition:
    """Create a new automation workflow."""
    logger.info(f"Creating workflow: {workflow.name}")
    return workflow


@router.post("/workflows/{workflow_id}/execute", response_model=WorkflowExecution)
async def execute_workflow(
    workflow_id: UUID, workflow: WorkflowDefinition
) -> WorkflowExecution:
    """Execute a workflow."""
    try:
        execution = await automation_engine.execute_workflow(workflow)
        return execution
    except Exception as e:
        logger.error(f"Workflow execution failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/workflows/{workflow_id}/executions", response_model=List[WorkflowExecution])
async def get_workflow_executions(workflow_id: UUID) -> List[WorkflowExecution]:
    """Get execution history for a workflow."""
    executions = [
        exec for exec in automation_engine.executions.values()
        if exec.workflow_id == workflow_id
    ]
    return executions


@router.post("/api-emulation", response_model=dict)
async def create_api_emulation(config: APIEmulationConfig) -> dict:
    """Create an API emulation for a legacy system."""
    logger.info(f"Creating API emulation for system: {config.system_id}")
    return {"status": "created", "system_id": config.system_id}


@router.get("/health")
async def health_check() -> dict:
    """Health check for automation fabric."""
    return {"status": "healthy", "module": "automation_fabric"}
