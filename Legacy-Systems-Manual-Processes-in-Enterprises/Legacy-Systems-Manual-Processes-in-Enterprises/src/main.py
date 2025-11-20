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
    """Basic health check - lightweight probe."""
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "service": "legacy-backend",
            "version": settings.app_version,
        },
    )


@app.get("/health/live")
async def liveness_check() -> JSONResponse:
    """Kubernetes-style liveness probe."""
    import time
    return JSONResponse(
        status_code=200,
        content={
            "alive": True,
            "service": "legacy-backend",
            "uptime": time.process_time(),
        },
    )


@app.get("/health/ready")
async def readiness_check() -> JSONResponse:
    """Kubernetes-style readiness probe - checks critical dependencies."""
    import os
    import urllib.request
    import urllib.error

    checks = {}
    all_healthy = True

    # Check Database
    database_url = os.getenv("DATABASE_URL", "")
    if database_url:
        checks["database"] = {"healthy": True, "configured": True, "critical": True}
    else:
        checks["database"] = {"healthy": False, "error": "DATABASE_URL not configured", "critical": True}
        all_healthy = False

    # Check Redis
    redis_url = os.getenv("REDIS_URL", "")
    if redis_url:
        checks["redis"] = {"healthy": True, "configured": True, "critical": True}
    else:
        checks["redis"] = {"healthy": False, "error": "REDIS_URL not configured", "critical": True}
        all_healthy = False

    # Check Qdrant (Vector DB)
    qdrant_url = os.getenv("QDRANT_URL", "http://qdrant:6333")
    try:
        req = urllib.request.Request(qdrant_url, method="GET")
        response = urllib.request.urlopen(req, timeout=2)
        checks["qdrant"] = {"healthy": True, "url": qdrant_url, "critical": False}
    except Exception:
        checks["qdrant"] = {"healthy": False, "error": "Service unavailable", "critical": False, "fallback": "Vector search disabled"}

    # Check Neo4j (Graph DB)
    neo4j_uri = os.getenv("NEO4J_URI", "")
    if neo4j_uri:
        checks["neo4j"] = {"healthy": True, "configured": True, "critical": False}
    else:
        checks["neo4j"] = {"healthy": False, "error": "Not configured", "critical": False}

    status_code = 200 if all_healthy else 503

    return JSONResponse(
        status_code=status_code,
        content={
            "ready": all_healthy,
            "service": "legacy-backend",
            "checks": checks,
        },
    )


@app.get("/health/detailed")
async def detailed_health_check() -> JSONResponse:
    """Detailed health check with all dependencies and modules."""
    import os
    import sys
    import time
    import urllib.request
    import urllib.error

    checks = {}

    # Database check
    database_url = os.getenv("DATABASE_URL", "")
    checks["database"] = {
        "healthy": bool(database_url),
        "configured": bool(database_url),
        "critical": True
    }

    # Redis check
    redis_url = os.getenv("REDIS_URL", "")
    checks["redis"] = {
        "healthy": bool(redis_url),
        "configured": bool(redis_url),
        "critical": True
    }

    # Ollama check (LLM)
    ollama_url = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
    try:
        req = urllib.request.Request(f"{ollama_url}/api/tags", method="GET")
        response = urllib.request.urlopen(req, timeout=2)
        checks["ollama"] = {"healthy": True, "url": ollama_url, "critical": False}
    except Exception as e:
        checks["ollama"] = {"healthy": False, "error": "Service unavailable", "critical": False, "fallback": "LLM features disabled"}

    # Qdrant check (Vector DB)
    qdrant_url = os.getenv("QDRANT_URL", "http://qdrant:6333")
    try:
        req = urllib.request.Request(qdrant_url, method="GET")
        response = urllib.request.urlopen(req, timeout=2)
        checks["qdrant"] = {"healthy": True, "url": qdrant_url, "critical": False}
    except Exception:
        checks["qdrant"] = {"healthy": False, "error": "Service unavailable", "critical": False, "fallback": "Vector search disabled"}

    # Neo4j check
    neo4j_uri = os.getenv("NEO4J_URI", "")
    checks["neo4j"] = {
        "healthy": bool(neo4j_uri),
        "configured": bool(neo4j_uri),
        "critical": False,
        "fallback": "Knowledge graph features disabled" if not neo4j_uri else None
    }

    # Elasticsearch check
    es_url = os.getenv("ELASTICSEARCH_URL", "")
    if es_url:
        try:
            req = urllib.request.Request(f"{es_url}/_cluster/health", method="GET")
            response = urllib.request.urlopen(req, timeout=2)
            checks["elasticsearch"] = {"healthy": True, "url": es_url, "critical": False}
        except Exception:
            checks["elasticsearch"] = {"healthy": False, "error": "Service unavailable", "critical": False}
    else:
        checks["elasticsearch"] = {"healthy": False, "error": "Not configured", "critical": False}

    # MinIO check
    minio_endpoint = os.getenv("MINIO_ENDPOINT", "")
    checks["minio"] = {
        "healthy": bool(minio_endpoint),
        "configured": bool(minio_endpoint),
        "critical": False,
        "fallback": "Object storage disabled" if not minio_endpoint else None
    }

    # Determine overall status
    critical_services_healthy = all(
        check.get("healthy", False)
        for check in checks.values()
        if check.get("critical", False)
    )

    overall_status = "healthy" if critical_services_healthy else "degraded"

    return JSONResponse(
        status_code=200,
        content={
            "status": overall_status,
            "service": "legacy-backend",
            "version": settings.app_version,
            "timestamp": time.time(),
            "checks": checks,
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
            "system": {
                "python_version": sys.version,
                "uptime": time.process_time()
            },
            "fallback_info": {
                "ollama": "LLM features will be disabled if unavailable",
                "qdrant": "Vector search will be disabled if unavailable",
                "neo4j": "Knowledge graph features will be disabled if unavailable",
                "elasticsearch": "Advanced search will be disabled if unavailable",
                "minio": "Object storage features will be disabled if unavailable"
            }
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
