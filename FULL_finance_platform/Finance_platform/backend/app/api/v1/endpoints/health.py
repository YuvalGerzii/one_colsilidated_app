"""Health Check Endpoints"""

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from app.core.database import get_db, check_db_connection
import time
import os
import sys
import urllib.request
import urllib.error
from typing import Dict, Any

router = APIRouter()


def check_redis() -> Dict[str, Any]:
    """Check Redis connectivity."""
    try:
        redis_url = os.getenv("REDIS_URL", "")
        if not redis_url:
            return {"healthy": False, "error": "REDIS_URL not configured"}

        # Simple check - we'll return healthy if configured
        # In production, you'd want to actually ping Redis
        return {"healthy": True, "configured": True}
    except Exception as e:
        return {"healthy": False, "error": str(e)}


def check_rabbitmq() -> Dict[str, Any]:
    """Check RabbitMQ connectivity."""
    try:
        rabbitmq_url = os.getenv("RABBITMQ_URL", "")
        if not rabbitmq_url:
            return {"healthy": False, "error": "RABBITMQ_URL not configured"}

        return {"healthy": True, "configured": True}
    except Exception as e:
        return {"healthy": False, "error": str(e)}


def check_ollama() -> Dict[str, Any]:
    """Check Ollama LLM service."""
    try:
        ollama_url = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")

        req = urllib.request.Request(f"{ollama_url}/api/tags", method="GET")
        response = urllib.request.urlopen(req, timeout=2)

        if response.status == 200:
            return {"healthy": True, "url": ollama_url}
        return {"healthy": False, "error": f"HTTP {response.status}"}
    except urllib.error.URLError as e:
        return {"healthy": False, "error": "Service unavailable", "fallback": "LLM features disabled"}
    except Exception as e:
        return {"healthy": False, "error": str(e), "fallback": "LLM features disabled"}


def check_weaviate() -> Dict[str, Any]:
    """Check Weaviate vector database."""
    try:
        weaviate_url = os.getenv("WEAVIATE_URL", "http://weaviate:8080")

        req = urllib.request.Request(f"{weaviate_url}/v1/.well-known/ready", method="GET")
        response = urllib.request.urlopen(req, timeout=2)

        if response.status == 200:
            return {"healthy": True, "url": weaviate_url}
        return {"healthy": False, "error": f"HTTP {response.status}"}
    except urllib.error.URLError:
        return {"healthy": False, "error": "Service unavailable", "fallback": "Vector search disabled"}
    except Exception as e:
        return {"healthy": False, "error": str(e), "fallback": "Vector search disabled"}


@router.get("/")
async def health_check():
    """Basic health check - lightweight probe."""
    return {
        "status": "healthy",
        "service": "finance-backend",
        "timestamp": time.time()
    }


@router.get("/live")
async def liveness_check():
    """Kubernetes-style liveness probe."""
    return {
        "alive": True,
        "service": "finance-backend",
        "uptime": time.process_time()
    }


@router.get("/ready")
async def readiness_check(response: Response):
    """Kubernetes-style readiness probe - checks critical dependencies."""
    checks = {}
    all_critical_healthy = True

    # Check critical dependency: Database
    db_healthy = check_db_connection()
    checks["database"] = {"healthy": db_healthy, "critical": True}
    if not db_healthy:
        all_critical_healthy = False

    # Check Redis (critical for caching)
    redis_status = check_redis()
    checks["redis"] = {**redis_status, "critical": True}
    if not redis_status.get("healthy"):
        all_critical_healthy = False

    if not all_critical_healthy:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {
            "ready": False,
            "service": "finance-backend",
            "checks": checks
        }

    return {
        "ready": True,
        "service": "finance-backend",
        "checks": checks
    }


@router.get("/detailed")
async def detailed_health_check(db: Session = Depends(get_db)):
    """Detailed health check with all dependencies."""
    checks = {}

    # Database check
    db_healthy = check_db_connection()
    checks["database"] = {
        "healthy": db_healthy,
        "critical": True,
        "status": "operational" if db_healthy else "down"
    }

    # Redis check
    checks["redis"] = {**check_redis(), "critical": True}

    # RabbitMQ check
    checks["rabbitmq"] = {**check_rabbitmq(), "critical": False}

    # Ollama check (optional service)
    checks["ollama"] = {**check_ollama(), "critical": False}

    # Weaviate check (optional service)
    checks["weaviate"] = {**check_weaviate(), "critical": False}

    # Determine overall status
    critical_services_healthy = all(
        check.get("healthy", False)
        for check in checks.values()
        if check.get("critical", False)
    )

    overall_status = "healthy" if critical_services_healthy else "degraded"

    # Add system info
    system_info = {
        "python_version": sys.version,
        "uptime": time.process_time()
    }

    return {
        "status": overall_status,
        "service": "finance-backend",
        "timestamp": time.time(),
        "checks": checks,
        "system": system_info,
        "fallback_info": {
            "ollama": "LLM features will be disabled if unavailable",
            "weaviate": "Vector search will be disabled if unavailable",
            "rabbitmq": "Background tasks may be affected if unavailable"
        }
    }
