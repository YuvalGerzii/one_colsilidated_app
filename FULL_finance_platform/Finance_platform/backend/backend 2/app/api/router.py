"""
API Router Configuration

This module aggregates all API endpoints into a single router.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import (
    health,
    funds,
    companies,
    financials,
    models,
    pdf,
    reports,
    dashboard,
)

# Create main API router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(
    health.router,
    prefix="/health",
    tags=["Health Check"]
)

api_router.include_router(
    funds.router,
    prefix="/funds",
    tags=["Funds"]
)

api_router.include_router(
    companies.router,
    prefix="/companies",
    tags=["Portfolio Companies"]
)

api_router.include_router(
    financials.router,
    prefix="/financials",
    tags=["Financial Metrics"]
)

api_router.include_router(
    models.router,
    prefix="/models",
    tags=["Model Generation"]
)

api_router.include_router(
    pdf.router,
    prefix="/pdf",
    tags=["PDF Extraction"]
)

api_router.include_router(
    reports.router,
    prefix="/reports",
    tags=["Reports"]
)

api_router.include_router(
    dashboard.router,
    prefix="/dashboard",
    tags=["Dashboard"]
)


__all__ = ["api_router"]
