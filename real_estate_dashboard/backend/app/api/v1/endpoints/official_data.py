"""
Official Government Data API Endpoints
"""

from typing import Dict, Any, Optional, List
from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.integrations.manager import integration_manager
from app.core.database import get_db

router = APIRouter()


# ====================================
# DATA.GOV US ENDPOINTS
# ====================================

@router.get("/datagov-us/search")
async def search_us_datasets(
    query: str = Query(..., description="Search query"),
    tags: Optional[str] = Query(None, description="Comma-separated tags"),
    limit: int = Query(20, ge=1, le=1000)
):
    """
    Search US Data.gov datasets

    Examples:
    - `/official-data/datagov-us/search?query=real estate`
    - `/official-data/datagov-us/search?query=housing&tags=real-estate,housing`
    """
    integration = integration_manager.get("datagov_us")

    if not integration or not integration.is_available:
        raise HTTPException(
            status_code=503,
            detail="Data.gov US integration not available"
        )

    tag_list = tags.split(",") if tags else None

    result = await integration.search_datasets(
        query=query,
        tags=tag_list,
        limit=limit
    )

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    return result.data


@router.get("/datagov-us/dataset/{dataset_id}")
async def get_us_dataset(dataset_id: str):
    """Get detailed information about a US Data.gov dataset"""
    integration = integration_manager.get("datagov_us")

    if not integration or not integration.is_available:
        raise HTTPException(
            status_code=503,
            detail="Data.gov US integration not available"
        )

    result = await integration.get_dataset(dataset_id)

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    return result.data


@router.get("/datagov-us/real-estate")
async def get_us_real_estate_datasets(limit: int = Query(50, ge=1, le=1000)):
    """Get real estate and housing datasets from Data.gov"""
    integration = integration_manager.get("datagov_us")

    if not integration or not integration.is_available:
        raise HTTPException(
            status_code=503,
            detail="Data.gov US integration not available"
        )

    result = await integration.get_real_estate_datasets(limit=limit)

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    return result.data


@router.get("/datagov-us/organizations")
async def list_us_organizations(limit: int = Query(100, ge=1, le=1000)):
    """List US government organizations publishing data"""
    integration = integration_manager.get("datagov_us")

    if not integration or not integration.is_available:
        raise HTTPException(
            status_code=503,
            detail="Data.gov US integration not available"
        )

    result = await integration.list_organizations(limit=limit)

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    return result.data


# ====================================
# DATA.GOV ISRAEL ENDPOINTS
# ====================================

@router.get("/datagov-il/search")
async def search_israeli_datasets(
    query: str = Query(..., description="Search query (Hebrew or English)"),
    limit: int = Query(20, ge=1, le=1000)
):
    """
    Search Israeli Data.gov datasets

    Supports both Hebrew and English queries
    """
    integration = integration_manager.get("datagov_il")

    if not integration or not integration.is_available:
        raise HTTPException(
            status_code=503,
            detail="Data.gov IL integration not available"
        )

    result = await integration.search_datasets(query=query, limit=limit)

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    return result.data


@router.get("/datagov-il/dataset/{dataset_id}")
async def get_israeli_dataset(dataset_id: str):
    """Get detailed information about an Israeli Data.gov dataset"""
    integration = integration_manager.get("datagov_il")

    if not integration or not integration.is_available:
        raise HTTPException(
            status_code=503,
            detail="Data.gov IL integration not available"
        )

    result = await integration.get_dataset(dataset_id)

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    return result.data


@router.get("/datagov-il/real-estate")
async def get_israeli_real_estate_datasets(limit: int = Query(50, ge=1, le=1000)):
    """Get real estate and property datasets from Israeli Data.gov"""
    integration = integration_manager.get("datagov_il")

    if not integration or not integration.is_available:
        raise HTTPException(
            status_code=503,
            detail="Data.gov IL integration not available"
        )

    result = await integration.get_real_estate_datasets(limit=limit)

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    return result.data


@router.get("/datagov-il/tags")
async def list_israeli_tags():
    """List all available tags from Israeli Data.gov"""
    integration = integration_manager.get("datagov_il")

    if not integration or not integration.is_available:
        raise HTTPException(
            status_code=503,
            detail="Data.gov IL integration not available"
        )

    result = await integration.list_tags()

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    return result.data


# ====================================
# BANK OF ISRAEL ENDPOINTS
# ====================================

@router.get("/bank-of-israel/interest-rate")
async def get_israel_interest_rate(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Get Bank of Israel interest rate with database caching"""
    integration = integration_manager.get("bank_of_israel")

    if not integration or not integration.is_available:
        raise HTTPException(
            status_code=503,
            detail="Bank of Israel integration not available"
        )

    result = await integration.get_interest_rate(
        start_date=start_date,
        end_date=end_date,
        db=db
    )

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    return result.data


@router.get("/bank-of-israel/cpi")
async def get_israel_cpi(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Get Israeli Consumer Price Index (CPI) data with database caching"""
    integration = integration_manager.get("bank_of_israel")

    if not integration or not integration.is_available:
        raise HTTPException(
            status_code=503,
            detail="Bank of Israel integration not available"
        )

    result = await integration.get_cpi(
        start_date=start_date,
        end_date=end_date,
        db=db
    )

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    return result.data


@router.get("/bank-of-israel/housing-price-index")
async def get_israel_housing_price_index():
    """Get Israeli housing price index"""
    integration = integration_manager.get("bank_of_israel")

    if not integration or not integration.is_available:
        raise HTTPException(
            status_code=503,
            detail="Bank of Israel integration not available"
        )

    result = await integration.get_housing_price_index()

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    return result.data


@router.get("/bank-of-israel/exchange-rate/{currency}")
async def get_israel_exchange_rate(
    currency: str,
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Get exchange rate history for a currency vs ILS from Bank of Israel SDMX API"""
    integration = integration_manager.get("bank_of_israel")

    if not integration or not integration.is_available:
        raise HTTPException(
            status_code=503,
            detail="Bank of Israel integration not available"
        )

    result = await integration.get_exchange_rate(
        currency=currency.upper(),
        start_date=start_date,
        end_date=end_date,
        db=db
    )

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    return result.data


@router.get("/bank-of-israel/exchange-rates/latest")
async def get_israel_latest_exchange_rates(
    currencies: Optional[str] = Query(None, description="Comma-separated currency codes (USD,EUR,GBP)"),
    db: Session = Depends(get_db)
):
    """Get latest exchange rates for multiple currencies from Bank of Israel"""
    integration = integration_manager.get("bank_of_israel")

    if not integration or not integration.is_available:
        raise HTTPException(
            status_code=503,
            detail="Bank of Israel integration not available"
        )

    currency_list = currencies.split(",") if currencies else None

    result = await integration.get_latest_exchange_rates(
        currencies=currency_list,
        db=db
    )

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    return result.data


# ====================================
# HUD ENDPOINTS
# ====================================

@router.get("/hud/fair-market-rent")
async def get_fair_market_rent(
    zip_code: str = Query(..., description="5-digit ZIP code"),
    year: Optional[int] = Query(None, description="Year")
):
    """Get HUD Fair Market Rent for a ZIP code"""
    integration = integration_manager.get("hud")

    if not integration or not integration.is_available:
        raise HTTPException(
            status_code=503,
            detail="HUD integration not available"
        )

    result = await integration.get_fair_market_rent(zip_code=zip_code, year=year)

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    return result.data


@router.get("/hud/income-limits")
async def get_income_limits(
    state_code: str = Query(..., description="2-letter state code"),
    county: Optional[str] = Query(None, description="County name"),
    year: Optional[int] = Query(None, description="Year")
):
    """Get HUD Area Median Income and income limits"""
    integration = integration_manager.get("hud")

    if not integration or not integration.is_available:
        raise HTTPException(
            status_code=503,
            detail="HUD integration not available"
        )

    result = await integration.get_income_limits(
        state_code=state_code,
        county=county,
        year=year
    )

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    return result.data


@router.get("/hud/public-housing")
async def get_public_housing_data(state: Optional[str] = Query(None, description="State code")):
    """Get public housing statistics"""
    integration = integration_manager.get("hud")

    if not integration or not integration.is_available:
        raise HTTPException(
            status_code=503,
            detail="HUD integration not available"
        )

    result = await integration.get_public_housing_data(state=state)

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    return result.data


# ====================================
# FHFA ENDPOINTS
# ====================================

@router.get("/fhfa/house-price-index")
async def get_house_price_index(
    geography_type: str = Query("USA", description="USA, State, CBSA, or ZIP5"),
    place_name: Optional[str] = Query(None, description="Place name (e.g., California, Los Angeles)"),
    start_year: Optional[int] = Query(None, description="Start year"),
    end_year: Optional[int] = Query(None, description="End year"),
    db: Session = Depends(get_db)
):
    """Get FHFA House Price Index data from CSV download"""
    integration = integration_manager.get("fhfa")

    if not integration or not integration.is_available:
        raise HTTPException(
            status_code=503,
            detail="FHFA integration not available"
        )

    result = await integration.get_house_price_index(
        geography_type=geography_type,
        place_name=place_name,
        start_year=start_year,
        end_year=end_year,
        db=db
    )

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    return result.data


@router.get("/fhfa/state-hpi/{state_name}")
async def get_state_house_price_index(
    state_name: str,
    start_year: Optional[int] = Query(None, description="Start year"),
    db: Session = Depends(get_db)
):
    """Get state-level House Price Index with actual data"""
    integration = integration_manager.get("fhfa")

    if not integration or not integration.is_available:
        raise HTTPException(
            status_code=503,
            detail="FHFA integration not available"
        )

    result = await integration.get_state_hpi(
        state_name=state_name,
        start_year=start_year,
        db=db
    )

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    return result.data


@router.get("/fhfa/metro-hpi/{metro_name}")
async def get_metro_house_price_index(
    metro_name: str,
    start_year: Optional[int] = Query(None, description="Start year"),
    db: Session = Depends(get_db)
):
    """Get metro area House Price Index with actual data"""
    integration = integration_manager.get("fhfa")

    if not integration or not integration.is_available:
        raise HTTPException(
            status_code=503,
            detail="FHFA integration not available"
        )

    result = await integration.get_metro_hpi(
        metro_name=metro_name,
        start_year=start_year,
        db=db
    )

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    return result.data


@router.get("/fhfa/national-hpi")
async def get_national_house_price_index(
    start_year: Optional[int] = Query(None, description="Start year"),
    db: Session = Depends(get_db)
):
    """Get national House Price Index with actual data"""
    integration = integration_manager.get("fhfa")

    if not integration or not integration.is_available:
        raise HTTPException(
            status_code=503,
            detail="FHFA integration not available"
        )

    result = await integration.get_national_hpi(
        start_year=start_year,
        db=db
    )

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    return result.data


@router.get("/fhfa/search-places")
async def search_fhfa_places(
    query: str = Query(..., description="Search query (e.g., Los Angeles, California)"),
    geography_type: Optional[str] = Query(None, description="Filter by level (USA, State, CBSA, ZIP5)")
):
    """Search for available places in FHFA HPI data"""
    integration = integration_manager.get("fhfa")

    if not integration or not integration.is_available:
        raise HTTPException(
            status_code=503,
            detail="FHFA integration not available"
        )

    result = await integration.search_places(
        query=query,
        geography_type=geography_type
    )

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    return result.data


@router.get("/fhfa/latest-data")
async def get_fhfa_latest_data(
    geography_type: str = Query("USA", description="Geography level"),
    limit: int = Query(10, ge=1, le=100, description="Number of results")
):
    """Get latest FHFA HPI data points"""
    integration = integration_manager.get("fhfa")

    if not integration or not integration.is_available:
        raise HTTPException(
            status_code=503,
            detail="FHFA integration not available"
        )

    result = await integration.get_latest_data(
        geography_type=geography_type,
        limit=limit
    )

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    return result.data


@router.get("/fhfa/download-info")
async def get_fhfa_download_info():
    """Get information about FHFA CSV downloads and data format"""
    integration = integration_manager.get("fhfa")

    if not integration or not integration.is_available:
        raise HTTPException(
            status_code=503,
            detail="FHFA integration not available"
        )

    result = await integration.get_download_info()

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    return result.data
