"""
API Router - Main API route aggregation
"""

from fastapi import APIRouter

from app.api.v1.endpoints import health, property_management, real_estate_tools

api_router = APIRouter()

# Health check endpoint
api_router.include_router(
    health.router,
    tags=["health"]
)

# Property Management endpoints
api_router.include_router(
    property_management.router,
    prefix="/property-management",
    tags=["property-management"]
)

# Real Estate Tools endpoints
api_router.include_router(
    real_estate_tools.router,
    prefix="/real-estate",
    tags=["real-estate-tools"]
)
