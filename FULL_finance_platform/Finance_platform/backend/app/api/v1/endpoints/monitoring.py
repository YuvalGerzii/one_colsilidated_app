"""
Monitoring and Debugging Endpoints
Provides system health, metrics, and debugging information
"""

import os
import sys
import psutil
import time
from datetime import datetime
from typing import Dict, List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.database import get_db
from app.config import settings

router = APIRouter(prefix="/monitoring", tags=["monitoring"])


@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """
    Comprehensive health check endpoint.

    Returns system status including:
    - API status
    - Database connectivity
    - System resources
    - Configuration
    """
    health_data = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "checks": {}
    }

    # API Check
    health_data["checks"]["api"] = {
        "status": "up",
        "message": "API is responding"
    }

    # Database Check
    try:
        db.execute(text("SELECT 1"))
        health_data["checks"]["database"] = {
            "status": "up",
            "message": "Database is accessible"
        }
    except Exception as e:
        health_data["status"] = "degraded"
        health_data["checks"]["database"] = {
            "status": "down",
            "message": f"Database error: {str(e)}"
        }

    # System Resources
    try:
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        health_data["checks"]["resources"] = {
            "status": "up",
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "memory_percent": memory.percent,
            "memory_available_mb": memory.available // (1024 * 1024),
            "disk_percent": disk.percent,
            "disk_free_gb": disk.free // (1024 ** 3)
        }
    except Exception as e:
        health_data["checks"]["resources"] = {
            "status": "unknown",
            "message": f"Could not get system resources: {str(e)}"
        }

    return health_data


@router.get("/metrics")
async def get_metrics(db: Session = Depends(get_db)):
    """
    Get application metrics.

    Returns:
    - Database table counts
    - System metrics
    - Application statistics
    """
    metrics = {
        "timestamp": datetime.utcnow().isoformat(),
        "database": {},
        "system": {},
        "application": {}
    }

    # Database table counts
    try:
        tables = [
            "funds", "portfolio_companies", "financial_metrics",
            "company_kpis", "valuations", "documents", "users",
            "market_data", "comp_transactions", "economic_indicators"
        ]

        for table in tables:
            try:
                result = db.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.scalar()
                metrics["database"][table] = count
            except:
                metrics["database"][table] = "N/A"

    except Exception as e:
        metrics["database"]["error"] = str(e)

    # System metrics
    try:
        process = psutil.Process()
        metrics["system"] = {
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "memory_percent": psutil.virtual_memory().percent,
            "process_memory_mb": process.memory_info().rss // (1024 * 1024),
            "process_cpu_percent": process.cpu_percent(interval=0.1),
            "disk_usage_percent": psutil.disk_usage('/').percent,
            "boot_time": datetime.fromtimestamp(psutil.boot_time()).isoformat()
        }
    except Exception as e:
        metrics["system"]["error"] = str(e)

    # Application metrics
    metrics["application"] = {
        "python_version": sys.version,
        "environment": settings.ENVIRONMENT,
        "debug_mode": settings.DEBUG,
        "version": settings.APP_VERSION
    }

    return metrics


@router.get("/info")
async def get_system_info():
    """
    Get detailed system information (debug mode only).

    Returns:
    - Environment variables (sanitized)
    - System information
    - Configuration
    """
    if not settings.DEBUG:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This endpoint is only available in debug mode"
        )

    info = {
        "system": {
            "platform": sys.platform,
            "python_version": sys.version,
            "python_implementation": sys.implementation.name,
        },
        "process": {
            "pid": os.getpid(),
            "cwd": os.getcwd(),
            "user": os.environ.get("USER", "unknown"),
        },
        "configuration": {
            "app_name": settings.APP_NAME,
            "app_version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT,
            "debug": settings.DEBUG,
            "api_prefix": settings.API_V1_PREFIX,
            "cors_origins": settings.get_cors_origins(),
        },
        "database": {
            "url": settings.DATABASE_URL.split("@")[-1] if hasattr(settings, 'DATABASE_URL') else "N/A",  # Hide credentials
            "pool_size": getattr(settings, 'DB_POOL_SIZE', "N/A"),
        }
    }

    # Add safe environment variables
    safe_env_vars = [
        "ENVIRONMENT", "DEBUG", "APP_NAME", "APP_VERSION",
        "LOG_LEVEL", "WORKERS"
    ]
    info["environment"] = {
        key: os.environ.get(key, "N/A")
        for key in safe_env_vars
    }

    return info


@router.get("/database/tables")
async def list_database_tables(db: Session = Depends(get_db)):
    """
    List all tables in the database with row counts.
    """
    try:
        # Get all table names
        result = db.execute(text("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name
        """))

        tables = []
        for row in result:
            table_name = row[0]
            try:
                count_result = db.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                count = count_result.scalar()
                tables.append({
                    "name": table_name,
                    "rows": count
                })
            except:
                tables.append({
                    "name": table_name,
                    "rows": "N/A"
                })

        return {
            "tables": tables,
            "total_tables": len(tables)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching tables: {str(e)}"
        )


@router.get("/logs/recent")
async def get_recent_logs(lines: int = 50):
    """
    Get recent application logs (debug mode only).

    Args:
        lines: Number of lines to return (default: 50, max: 500)
    """
    if not settings.DEBUG:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This endpoint is only available in debug mode"
        )

    lines = min(lines, 500)  # Cap at 500 lines

    log_file = getattr(settings, 'LOG_FILE_PATH', './logs/app.log')

    try:
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                all_lines = f.readlines()
                recent_lines = all_lines[-lines:]
                return {
                    "lines": recent_lines,
                    "count": len(recent_lines),
                    "total_lines": len(all_lines)
                }
        else:
            return {
                "message": f"Log file not found: {log_file}",
                "lines": [],
                "count": 0
            }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error reading logs: {str(e)}"
        )


@router.post("/cache/clear")
async def clear_cache():
    """
    Clear application cache (if using Redis).

    Note: Implementation depends on your caching strategy.
    """
    if not settings.DEBUG:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This endpoint is only available in debug mode"
        )

    # TODO: Implement cache clearing logic
    # Example:
    # redis_client.flushdb()

    return {
        "message": "Cache clearing not yet implemented",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/performance/summary")
async def get_performance_summary():
    """
    Get application performance summary.
    """
    try:
        process = psutil.Process()

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "uptime_seconds": time.time() - process.create_time(),
            "cpu": {
                "process_percent": process.cpu_percent(interval=0.1),
                "system_percent": psutil.cpu_percent(interval=0.1),
                "cpu_count": psutil.cpu_count()
            },
            "memory": {
                "process_mb": process.memory_info().rss // (1024 * 1024),
                "process_percent": process.memory_percent(),
                "system_percent": psutil.virtual_memory().percent,
                "system_available_mb": psutil.virtual_memory().available // (1024 * 1024)
            },
            "disk": {
                "usage_percent": psutil.disk_usage('/').percent,
                "free_gb": psutil.disk_usage('/').free // (1024 ** 3)
            },
            "network": {
                "connections": len(process.connections())
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting performance data: {str(e)}"
        )
