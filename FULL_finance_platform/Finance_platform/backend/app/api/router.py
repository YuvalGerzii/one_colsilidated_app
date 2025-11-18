"""
API Router Configuration

This module aggregates all API endpoints into a single router.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import (
    finance_models,
    health,
    market_data,
    real_estate_tools,
    property_management,
    monitoring,
    companies,
    funds,
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
    market_data.router,
    prefix="/market-data",
    tags=["Market Data 📈"]
)

api_router.include_router(
    real_estate_tools.router,
    prefix="/real-estate",
    tags=["Real Estate Models"]
)

api_router.include_router(
    finance_models.router,
    prefix="/finance",
    tags=["Corporate Finance Models"]
)

api_router.include_router(
    property_management.router,
    prefix="/property-management",
    tags=["Property Management 🏢"]
)

api_router.include_router(
    monitoring.router,
    tags=["Monitoring & Debug 🔧"]
)

api_router.include_router(
    companies.router,
    prefix="/companies",
    tags=["Portfolio Companies 💼"]
)

api_router.include_router(
    funds.router,
    prefix="/funds",
    tags=["Funds 💰"]
)

# TODO: Add other endpoint routers as they are implemented
# - financials
# - models
# - pdf
# - reports
# - dashboard


__all__ = ["api_router"]
