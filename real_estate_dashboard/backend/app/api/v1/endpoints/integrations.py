"""
Third-Party Integrations API Endpoints
"""

from typing import Dict, Any, Optional, List
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.integrations.manager import integration_manager

router = APIRouter()


# ====================================
# REQUEST/RESPONSE MODELS
# ====================================

class IntegrationStatusResponse(BaseModel):
    """Integration status response"""
    integrations: Dict[str, Dict[str, Any]]
    total_count: int
    active_count: int
    categories: Dict[str, int]


class TestConnectionResponse(BaseModel):
    """Test connection response"""
    integration: str
    success: bool
    message: Optional[str] = None
    error: Optional[str] = None


class MarketDataRequest(BaseModel):
    """Request for market data"""
    zip_code: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None


class PropertySearchRequest(BaseModel):
    """Request for property search"""
    address: Optional[str] = None
    city: Optional[str] = None
    state_code: Optional[str] = None
    postal_code: Optional[str] = None
    limit: int = 20


# ====================================
# GENERAL INTEGRATION ENDPOINTS
# ====================================

@router.get("/status", response_model=IntegrationStatusResponse)
async def get_integrations_status():
    """
    Get status of all integrations

    Returns information about which integrations are configured and available.
    """
    summary = integration_manager.get_status_summary()

    # Count by category
    categories = {}
    for info in summary.values():
        category = info["category"]
        categories[category] = categories.get(category, 0) + 1

    active_count = sum(1 for v in summary.values() if v["available"])

    return IntegrationStatusResponse(
        integrations=summary,
        total_count=len(summary),
        active_count=active_count,
        categories=categories
    )


@router.get("/test/{integration_key}")
async def test_integration_connection(integration_key: str):
    """
    Test connection to a specific integration

    Args:
        integration_key: Integration identifier (e.g., 'census', 'fred', 'slack')
    """
    integration = integration_manager.get(integration_key)

    if not integration:
        raise HTTPException(
            status_code=404,
            detail=f"Integration '{integration_key}' not found"
        )

    if not integration.is_available:
        return TestConnectionResponse(
            integration=integration_key,
            success=False,
            error=f"Integration not configured or not available (Status: {integration.status.value})"
        )

    result = await integration.test_connection()

    return TestConnectionResponse(
        integration=integration_key,
        success=result.success,
        message=result.data.get("message") if result.data else None,
        error=result.error
    )


@router.get("/test-all")
async def test_all_integrations():
    """Test connection to all configured integrations"""
    results = await integration_manager.test_all()

    return {
        "results": {
            key: {
                "success": result.success,
                "message": result.data.get("message") if result.data else None,
                "error": result.error
            }
            for key, result in results.items()
        },
        "total": len(results),
        "successful": sum(1 for r in results.values() if r.success)
    }


@router.get("/metadata/{integration_key}")
async def get_integration_metadata(integration_key: str):
    """Get metadata about a specific integration"""
    integration = integration_manager.get(integration_key)

    if not integration:
        raise HTTPException(
            status_code=404,
            detail=f"Integration '{integration_key}' not found"
        )

    metadata = integration.get_metadata()

    return {
        "metadata": metadata.dict(),
        "status": integration.status.value,
        "available": integration.is_available
    }


# ====================================
# MARKET DATA ENDPOINTS
# ====================================

@router.get("/market-data/census/demographics")
async def get_census_demographics(
    zip_code: Optional[str] = Query(None, description="ZIP code"),
    state: Optional[str] = Query(None, description="State FIPS code"),
    county: Optional[str] = Query(None, description="County FIPS code")
):
    """
    Get demographic data from Census Bureau

    Requires Census Bureau integration to be configured.
    """
    census = integration_manager.get("census")

    if not census or not census.is_available:
        raise HTTPException(
            status_code=503,
            detail="Census Bureau integration not available"
        )

    if zip_code:
        result = await census.get_housing_stats(zip_code)
    else:
        # Get general demographics
        result = await census.get_demographics()

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    return result.data


@router.get("/market-data/bls/unemployment")
async def get_unemployment_rate(
    area_code: str = Query("0000000", description="BLS area code (default is national)")
):
    """
    Get unemployment rate from Bureau of Labor Statistics

    Args:
        area_code: BLS area code (default is national rate)
    """
    bls = integration_manager.get("bls")

    if not bls or not bls.is_available:
        raise HTTPException(
            status_code=503,
            detail="BLS integration not available"
        )

    result = await bls.get_unemployment_rate(area_code)

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    return result.data


@router.get("/market-data/bls/employment")
async def get_employment_stats(
    area_code: str = Query("0000000", description="BLS area code")
):
    """Get employment statistics from BLS"""
    bls = integration_manager.get("bls")

    if not bls or not bls.is_available:
        raise HTTPException(
            status_code=503,
            detail="BLS integration not available"
        )

    result = await bls.get_employment_stats(area_code)

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    return result.data


@router.get("/market-data/fred/mortgage-rates")
async def get_mortgage_rates(
    rate_type: str = Query("30Y", description="30Y or 15Y")
):
    """Get current mortgage rates from FRED"""
    fred = integration_manager.get("fred")

    if not fred or not fred.is_available:
        raise HTTPException(
            status_code=503,
            detail="FRED integration not available. Configure FRED_API_KEY in your environment."
        )

    result = await fred.get_mortgage_rates(rate_type)

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    return result.data


@router.get("/market-data/fred/housing-indicators")
async def get_housing_indicators():
    """Get key housing market indicators from FRED"""
    fred = integration_manager.get("fred")

    if not fred or not fred.is_available:
        raise HTTPException(
            status_code=503,
            detail="FRED integration not available"
        )

    result = await fred.get_housing_indicators()

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    return result.data


@router.get("/market-data/fred/interest-rates")
async def get_interest_rates():
    """Get key interest rates from FRED"""
    fred = integration_manager.get("fred")

    if not fred or not fred.is_available:
        raise HTTPException(
            status_code=503,
            detail="FRED integration not available"
        )

    result = await fred.get_interest_rates()

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    return result.data


# ====================================
# PROPERTY DATA ENDPOINTS
# ====================================

@router.get("/property-data/attom/details")
async def get_attom_property_details(
    address: Optional[str] = Query(None, description="Full street address")
):
    """
    Get property details from ATTOM Data

    Requires paid ATTOM Data subscription.
    """
    attom = integration_manager.get("attom")

    if not attom or not attom.is_available:
        raise HTTPException(
            status_code=503,
            detail="ATTOM Data integration not available. This is a paid service."
        )

    if not address:
        raise HTTPException(status_code=400, detail="Address is required")

    result = await attom.get_property_details(address=address)

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    return result.data


@router.get("/property-data/realtor/search")
async def search_realtor_properties(
    postal_code: Optional[str] = Query(None),
    city: Optional[str] = Query(None),
    state_code: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    status: str = Query("for_sale", description="for_sale, for_rent, or sold")
):
    """
    Search properties on Realtor.com

    Requires RapidAPI key for Realtor.com API.
    Free tier: 500 requests/month
    """
    realtor = integration_manager.get("realtor")

    if not realtor or not realtor.is_available:
        raise HTTPException(
            status_code=503,
            detail="Realtor.com integration not available"
        )

    result = await realtor.search_properties(
        postal_code=postal_code,
        city=city,
        state_code=state_code,
        limit=limit,
        status=status
    )

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    return result.data


# ====================================
# NOTIFICATION ENDPOINTS
# ====================================

@router.post("/notifications/slack/send")
async def send_slack_notification(
    channel: str,
    message: str
):
    """
    Send a message to Slack

    Requires Slack bot token to be configured.
    """
    slack = integration_manager.get("slack")

    if not slack or not slack.is_available:
        raise HTTPException(
            status_code=503,
            detail="Slack integration not available"
        )

    result = await slack.send_message(channel=channel, text=message)

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    return result.data


@router.post("/notifications/slack/deal")
async def send_slack_deal_notification(
    channel: str,
    deal_name: str,
    deal_type: str,
    amount: float,
    status: str
):
    """Send a formatted deal notification to Slack"""
    slack = integration_manager.get("slack")

    if not slack or not slack.is_available:
        raise HTTPException(
            status_code=503,
            detail="Slack integration not available"
        )

    result = await slack.send_deal_notification(
        channel=channel,
        deal_name=deal_name,
        deal_type=deal_type,
        amount=amount,
        status=status
    )

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    return result.data
