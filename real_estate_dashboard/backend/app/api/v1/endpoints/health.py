"""Health Check Endpoints"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db, check_db_connection
import time

router = APIRouter()

@router.get("/")
async def health_check():
    """Basic health check."""
    return {
        "status": "healthy",
        "timestamp": time.time()
    }

@router.get("/detailed")
async def detailed_health_check(db: Session = Depends(get_db)):
    """Detailed health check with database status."""
    db_healthy = check_db_connection()
    
    return {
        "status": "healthy" if db_healthy else "degraded",
        "timestamp": time.time(),
        "components": {
            "api": "operational",
            "database": "operational" if db_healthy else "down"
        }
    }
