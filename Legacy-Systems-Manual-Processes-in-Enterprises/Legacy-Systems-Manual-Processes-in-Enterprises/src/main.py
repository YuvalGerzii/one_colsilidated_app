"""Main application entry point."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from prometheus_client import make_asgi_app

from src.core.config import get_settings
from src.core.logger import logger
from src.api import router as api_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Application lifespan handler."""
    logger.info("Starting Enterprise AI Modernization Suite...")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Debug mode: {settings.debug}")

    # Startup tasks
    logger.info("All modules initialized successfully")

    yield

    # Shutdown tasks
    logger.info("Shutting down Enterprise AI Modernization Suite...")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Comprehensive AI-driven enterprise modernization platform",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

# Add Prometheus metrics
if settings.prometheus_enabled:
    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)

# Include API router
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root() -> dict:
    """Root endpoint."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "operational",
        "environment": settings.environment,
    }


@app.get("/health")
async def health_check() -> JSONResponse:
    """Health check endpoint."""
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "version": settings.app_version,
            "modules": {
                "automation_fabric": settings.eaf_enabled,
                "legacy_migrator": settings.migrator_enabled,
                "process_miner": settings.process_miner_enabled,
                "document_os": settings.document_os_enabled,
                "governance": settings.governance_enabled,
                "company_brain": settings.company_brain_enabled,
                "hitl_hub": settings.hitl_enabled,
                "infrastructure": settings.infra_orchestrator_enabled,
                "agents": settings.agents_enabled,
                "risk_radar": settings.risk_radar_enabled,
            },
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
        workers=settings.api_workers if not settings.api_reload else 1,
        log_level=settings.log_level.lower(),
    )
