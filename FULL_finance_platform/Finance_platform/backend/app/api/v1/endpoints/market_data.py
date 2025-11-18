"""
Market Data API Endpoints

Endpoints for fetching real-time market data from external APIs with database integration.
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.services.market_data_service import MarketDataService
from app.services.market_data_aggregator import MarketDataAggregator
from app.api.deps import get_db


router = APIRouter()
market_data_service = MarketDataService()
aggregator = MarketDataAggregator()


# ================================
# REQUEST/RESPONSE MODELS
# ================================

class MarketDataRequest(BaseModel):
    """Request model for market data."""
    address: str = Field(..., description="Property address")
    city: str = Field(..., description="City name")
    state: str = Field(..., description="State abbreviation (e.g., CA, NY)")
    zip_code: str = Field(..., description="ZIP code")
    property_type: str = Field(..., description="Property type (e.g., Multifamily, SFR, Office)")
    latitude: Optional[float] = Field(None, description="Latitude coordinate (optional)")
    longitude: Optional[float] = Field(None, description="Longitude coordinate (optional)")


class PropertySearchRequest(BaseModel):
    """Request model for property search."""
    query: str = Field(..., description="Search query (address, city, or ZIP code)")
    property_type: Optional[str] = Field(None, description="Filter by property type")


# ================================
# ENDPOINTS
# ================================

@router.post("/comprehensive", summary="Get comprehensive market data")
async def get_comprehensive_market_data(
    request: MarketDataRequest,
    db: Session = Depends(get_db),
    force_refresh: bool = Query(False, description="Force refresh from APIs instead of using cache")
):
    """
    Fetch comprehensive market data from all sources with database caching:
    - CoStar: Cap rates, rent comps, market trends
    - Zillow/Redfin: Property valuations and comparables
    - Census: Demographics and population trends
    - Walk Score: Walkability and amenities

    Returns aggregated data from all APIs. Data is cached in the database for 24 hours.
    Use force_refresh=true to bypass cache.
    """
    try:
        data = await market_data_service.get_comprehensive_market_data(
            db=db,
            address=request.address,
            city=request.city,
            state=request.state,
            zip_code=request.zip_code,
            property_type=request.property_type,
            latitude=request.latitude,
            longitude=request.longitude,
            force_refresh=force_refresh,
        )
        return {
            "success": True,
            "data": data,
            "cached": not force_refresh
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/investment-summary", summary="Get investment summary")
async def get_investment_summary(
    request: MarketDataRequest,
    db: Session = Depends(get_db)
):
    """
    Generate an investment summary with key metrics from all sources.

    Returns a curated summary of the most important investment metrics.
    Uses database cache when available.
    """
    try:
        summary = await market_data_service.get_investment_summary(
            db=db,
            address=request.address,
            city=request.city,
            state=request.state,
            zip_code=request.zip_code,
            property_type=request.property_type,
            latitude=request.latitude,
            longitude=request.longitude,
        )
        return {
            "success": True,
            "data": summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/costar", summary="Get CoStar market data")
async def get_costar_data(
    address: str = Query(..., description="Property address"),
    city: str = Query(..., description="City name"),
    state: str = Query(..., description="State abbreviation"),
    zip_code: str = Query(..., description="ZIP code"),
    property_type: str = Query(..., description="Property type"),
):
    """
    Fetch market data from CoStar API.

    Returns cap rates, rent comps, and market trends.
    """
    try:
        data = await aggregator.costar.get_market_data(
            address, city, state, zip_code, property_type
        )
        return {
            "success": True,
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/zillow", summary="Get Zillow property data")
async def get_zillow_data(
    address: str = Query(..., description="Property address"),
    city: str = Query(..., description="City name"),
    state: str = Query(..., description="State abbreviation"),
    zip_code: str = Query(..., description="ZIP code"),
):
    """
    Fetch property data from Zillow API.

    Returns property valuations and comparables.
    """
    try:
        data = await aggregator.zillow.get_property_data(
            address, city, state, zip_code
        )
        return {
            "success": True,
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/census", summary="Get Census demographic data")
async def get_census_data(
    city: str = Query(..., description="City name"),
    state: str = Query(..., description="State abbreviation"),
    zip_code: Optional[str] = Query(None, description="ZIP code (optional)"),
):
    """
    Fetch demographic data from Census API.

    Returns population, income, and economic data.
    """
    try:
        data = await aggregator.census.get_demographic_data(
            city, state, zip_code
        )
        return {
            "success": True,
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/walkscore", summary="Get Walk Score data")
async def get_walkscore_data(
    address: str = Query(..., description="Property address"),
    latitude: float = Query(..., description="Latitude coordinate"),
    longitude: float = Query(..., description="Longitude coordinate"),
):
    """
    Fetch walkability scores from Walk Score API.

    Returns walk score, transit score, and nearby amenities.
    """
    try:
        data = await aggregator.walkscore.get_scores(
            address, latitude, longitude
        )
        return {
            "success": True,
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/comparable-sales", summary="Get comparable sales")
async def get_comparable_sales(
    address: str = Query(..., description="Property address"),
    city: str = Query(..., description="City name"),
    state: str = Query(..., description="State abbreviation"),
    property_type: str = Query(..., description="Property type"),
    radius_miles: float = Query(1.0, description="Search radius in miles"),
):
    """
    Fetch comparable sales from CoStar.

    Returns recent comparable sales within the specified radius.
    """
    try:
        data = await aggregator.costar.get_comparable_sales(
            address, city, state, property_type, radius_miles
        )
        return {
            "success": True,
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/comparable-properties", summary="Get comparable properties")
async def get_comparable_properties(
    address: str = Query(..., description="Property address"),
    city: str = Query(..., description="City name"),
    state: str = Query(..., description="State abbreviation"),
    zip_code: str = Query(..., description="ZIP code"),
    radius_miles: float = Query(1.0, description="Search radius in miles"),
):
    """
    Fetch comparable properties from Zillow.

    Returns similar properties within the specified radius.
    """
    try:
        data = await aggregator.zillow.get_comparable_properties(
            address, city, state, zip_code, radius_miles
        )
        return {
            "success": True,
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
