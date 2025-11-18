"""API routes and endpoints."""

from fastapi import APIRouter

from src.api.routes import (
    automation_fabric,
    legacy_migrator,
    process_miner,
    document_os,
    governance,
    company_brain,
    hitl_hub,
    infrastructure,
    agents,
    risk_radar,
    llm_monitoring,
)

router = APIRouter()

# Include all module routers
router.include_router(automation_fabric.router, prefix="/automation", tags=["Automation Fabric"])
router.include_router(legacy_migrator.router, prefix="/migration", tags=["Legacy Migrator"])
router.include_router(process_miner.router, prefix="/process", tags=["Process Miner"])
router.include_router(document_os.router, prefix="/documents", tags=["Document OS"])
router.include_router(governance.router, prefix="/governance", tags=["Governance"])
router.include_router(company_brain.router, prefix="/brain", tags=["Company Brain"])
router.include_router(hitl_hub.router, prefix="/hitl", tags=["Human-in-the-Loop"])
router.include_router(infrastructure.router, prefix="/infrastructure", tags=["Infrastructure"])
router.include_router(agents.router, prefix="/agents", tags=["Agents"])
router.include_router(risk_radar.router, prefix="/risk", tags=["Risk Radar"])
router.include_router(llm_monitoring.router, prefix="/llm", tags=["LLM Monitoring"])
