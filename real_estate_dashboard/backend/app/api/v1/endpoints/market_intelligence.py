"""
Market Intelligence API Endpoints

This module provides REST API endpoints for market intelligence data including:
- Real-time data from integrations (with failsafe fallbacks)
- Macro indicators, local market metrics
- Competitive landscape and news aggregation
"""

from typing import List, Optional
from datetime import datetime, date
from enum import Enum

from fastapi import APIRouter, Body, Depends, HTTPException, Query, Path, status, File, UploadFile
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import io

from app.api.deps import get_db
from app.services.market_data_service import market_data_service
from app.services.cache_service import get_cache_service


router = APIRouter()

# Initialize cache service for market intelligence endpoints
cache_service = get_cache_service()


# ========================================
# REAL DATA ENDPOINTS (WITH FAILSAFES)
# ========================================

@router.get("/data/summary")
async def get_real_market_data_summary(
    location: Optional[str] = Query(None, description="Location (city, state, or ZIP code)")
):
    """
    Get comprehensive market intelligence summary with REAL DATA and failsafe fallbacks.

    **Data Sources:**
    - Employment statistics (BLS)
    - Housing market indicators (FHFA, HUD)
    - Interest rates (Bank of Israel)

    **Failsafe**: Returns mock data if all sources fail. This endpoint NEVER breaks.
    """
    return await market_data_service.get_market_intelligence_summary(location)


@router.get("/data/employment")
async def get_real_employment_data(
    area_code: str = Query("0000000", description="BLS area code (default is national)")
):
    """
    Get REAL employment statistics with automatic failover.

    **Failsafe**: Never fails, returns mock data if needed.
    """
    return await market_data_service.get_employment_data(area_code)


@router.get("/data/housing-indicators")
async def get_real_housing_indicators():
    """
    Get REAL housing market indicators with automatic failover.

    **Failsafe**: Never fails, returns mock data if needed.
    """
    return await market_data_service.get_housing_indicators()


@router.get("/data/interest-rates")
async def get_real_interest_rates():
    """
    Get REAL interest rates with automatic failover.

    **Failsafe**: Never fails, returns mock data if needed.
    """
    return await market_data_service.get_interest_rates()


@router.get("/data/health")
async def get_integration_health():
    """
    Check health status of all data integrations.

    Returns which integrations are currently active and working.
    """
    return await market_data_service.get_integration_health()


@router.get("/analysis/gentrification-score")
async def get_gentrification_score(
    location: Optional[str] = Query(None, description="Location (city, state, or ZIP code)")
):
    """
    Calculate gentrification risk score for a location (0-100).

    **Analyzes multiple indicators:**
    - Housing price growth trends (30% weight)
    - Market velocity - inventory and sales speed (25% weight)
    - Employment strength (20% weight)
    - Interest rate environment (15% weight)
    - Affordability indicators (10% weight)

    **Score Ranges:**
    - 0-25: Low gentrification risk
    - 26-50: Moderate gentrification risk
    - 51-75: High gentrification risk
    - 76-100: Very high gentrification risk

    **Returns:**
    - Overall score and risk level
    - Component scores with weights
    - Market indicators
    - Actionable recommendations
    - Data quality metrics

    **Failsafe**: Never fails, uses fallback data if needed.
    """
    return await market_data_service.calculate_gentrification_score(location)


# ========================================
# MOCK/VISUALIZATION DATA ENDPOINTS
# ========================================


# Enums

class NewsCategory(str, Enum):
    """News article categories"""
    MACRO = "Macro"
    LOCAL = "Local"
    CONSTRUCTION = "Construction"
    INVESTMENT = "Investment"
    DEMOGRAPHICS = "Demographics"


class DevelopmentStatus(str, Enum):
    """Development project status"""
    PLANNING = "Planning"
    PRE_LEASING = "Pre-Leasing"
    UNDER_CONSTRUCTION = "Under Construction"
    COMPLETED = "Completed"


# Pydantic Schemas

class MacroIndicatorResponse(BaseModel):
    """Macro economic indicators response"""
    month: str
    fed_funds_rate: float = Field(..., description="Federal Funds Rate (%)")
    mortgage_30yr: float = Field(..., description="30-Year Mortgage Rate (%)")
    mortgage_15yr: float = Field(..., description="15-Year Mortgage Rate (%)")
    cpi: float = Field(..., description="Consumer Price Index (%)")
    pce: float = Field(..., description="Personal Consumption Expenditures (%)")
    housing_inflation: float = Field(..., description="Housing Inflation (%)")
    gdp_growth: float = Field(..., description="GDP Growth (%)")
    construction_growth: float = Field(..., description="Construction Sector Growth (%)")
    residential_growth: float = Field(..., description="Residential Construction Growth (%)")


class LocalMarketMetricResponse(BaseModel):
    """Local market metrics response"""
    month: str
    job_growth_rate: float = Field(..., description="Job Growth Rate (%)")
    new_jobs: int = Field(..., description="New Jobs Created")
    population: int = Field(..., description="Total Population")
    population_growth: float = Field(..., description="Population Growth (%)")
    single_family_permits: int = Field(..., description="Single Family Building Permits")
    multifamily_permits: int = Field(..., description="Multifamily Building Permits")
    commercial_permits: int = Field(..., description="Commercial Building Permits")


class CompetitiveDevelopmentResponse(BaseModel):
    """Competitive development project response"""
    id: int
    name: str = Field(description="Project name")
    developer: str = Field(description="Developer/company name")
    project_type: str = Field(description="Project type (Multifamily, Mixed-Use, etc.)")
    units: int = Field(description="Number of units (0 for commercial)")
    status: DevelopmentStatus = Field(description="Current project status")
    completion_date: str = Field(description="Expected completion date")
    price_range: str = Field(description="Price range for units")
    location: str = Field(description="Project location")
    amenities: List[str] = Field(default_factory=list, description="List of amenities")


class NewsArticleResponse(BaseModel):
    """News article response"""
    id: int
    title: str = Field(description="Article title")
    source: str = Field(description="News source")
    publication_date: str = Field(description="Publication date (YYYY-MM-DD)")
    category: NewsCategory = Field(description="Article category")
    summary: str = Field(description="Article summary")
    url: str = Field(description="Article URL")


class MarketOverviewResponse(BaseModel):
    """Market overview with key metrics"""
    fed_funds_rate: float
    fed_funds_change: float
    inflation_cpi: float
    inflation_change: float
    job_growth: int
    job_growth_change: int
    building_permits: int
    building_permits_change: int


# API Endpoints

@router.get("/overview", response_model=MarketOverviewResponse)
def get_market_overview(
    market: str = Query("National", description="Market location"),
    db: Session = Depends(get_db),
):
    """
    Get high-level market overview with key metrics
    """
    # Mock data - replace with actual database queries
    return MarketOverviewResponse(
        fed_funds_rate=5.33,
        fed_funds_change=0.00,
        inflation_cpi=3.0,
        inflation_change=-0.3,
        job_growth=215000,
        job_growth_change=20000,
        building_permits=3430,
        building_permits_change=180,
    )


@router.get("/macro-indicators", response_model=List[MacroIndicatorResponse])
def get_macro_indicators(
    market: str = Query("National", description="Market location"),
    timeframe: str = Query("6M", description="Time period (1M, 3M, 6M, 1Y, 2Y, 5Y)"),
    db: Session = Depends(get_db),
):
    """
    Get macro economic indicators including interest rates, inflation, and GDP growth
    """
    # Mock data - replace with actual database queries or external API calls
    return [
        MacroIndicatorResponse(
            month="Jan",
            fed_funds_rate=5.33,
            mortgage_30yr=6.62,
            mortgage_15yr=5.89,
            cpi=3.1,
            pce=2.4,
            housing_inflation=4.2,
            gdp_growth=2.2,
            construction_growth=3.1,
            residential_growth=4.2,
        ),
        MacroIndicatorResponse(
            month="Feb",
            fed_funds_rate=5.33,
            mortgage_30yr=6.64,
            mortgage_15yr=5.92,
            cpi=3.2,
            pce=2.5,
            housing_inflation=4.3,
            gdp_growth=2.1,
            construction_growth=2.9,
            residential_growth=3.8,
        ),
        MacroIndicatorResponse(
            month="Mar",
            fed_funds_rate=5.33,
            mortgage_30yr=6.82,
            mortgage_15yr=6.06,
            cpi=3.5,
            pce=2.7,
            housing_inflation=4.5,
            gdp_growth=4.9,
            construction_growth=3.5,
            residential_growth=6.2,
        ),
        MacroIndicatorResponse(
            month="Apr",
            fed_funds_rate=5.33,
            mortgage_30yr=7.17,
            mortgage_15yr=6.39,
            cpi=3.4,
            pce=2.7,
            housing_inflation=4.4,
            gdp_growth=3.4,
            construction_growth=3.2,
            residential_growth=4.5,
        ),
        MacroIndicatorResponse(
            month="May",
            fed_funds_rate=5.33,
            mortgage_30yr=6.81,
            mortgage_15yr=6.07,
            cpi=3.3,
            pce=2.6,
            housing_inflation=4.3,
            gdp_growth=1.6,
            construction_growth=2.8,
            residential_growth=3.2,
        ),
        MacroIndicatorResponse(
            month="Jun",
            fed_funds_rate=5.33,
            mortgage_30yr=6.86,
            mortgage_15yr=6.10,
            cpi=3.0,
            pce=2.5,
            housing_inflation=4.1,
            gdp_growth=2.8,
            construction_growth=3.0,
            residential_growth=4.1,
        ),
    ]


@router.get("/local-metrics", response_model=List[LocalMarketMetricResponse])
def get_local_market_metrics(
    market: str = Query("National", description="Market location"),
    timeframe: str = Query("6M", description="Time period (1M, 3M, 6M, 1Y, 2Y, 5Y)"),
    db: Session = Depends(get_db),
):
    """
    Get local market metrics including job growth, population trends, and building permits
    """
    # Mock data - replace with actual database queries or external API calls
    return [
        LocalMarketMetricResponse(
            month="Jan",
            job_growth_rate=2.8,
            new_jobs=175000,
            population=8550000,
            population_growth=1.2,
            single_family_permits=850,
            multifamily_permits=1200,
            commercial_permits=320,
        ),
        LocalMarketMetricResponse(
            month="Feb",
            job_growth_rate=3.1,
            new_jobs=198000,
            population=8560000,
            population_growth=1.3,
            single_family_permits=920,
            multifamily_permits=1350,
            commercial_permits=340,
        ),
        LocalMarketMetricResponse(
            month="Mar",
            job_growth_rate=2.9,
            new_jobs=185000,
            population=8570000,
            population_growth=1.2,
            single_family_permits=1100,
            multifamily_permits=1580,
            commercial_permits=380,
        ),
        LocalMarketMetricResponse(
            month="Apr",
            job_growth_rate=3.2,
            new_jobs=210000,
            population=8580000,
            population_growth=1.4,
            single_family_permits=1050,
            multifamily_permits=1420,
            commercial_permits=360,
        ),
        LocalMarketMetricResponse(
            month="May",
            job_growth_rate=3.0,
            new_jobs=195000,
            population=8590000,
            population_growth=1.3,
            single_family_permits=1180,
            multifamily_permits=1680,
            commercial_permits=410,
        ),
        LocalMarketMetricResponse(
            month="Jun",
            job_growth_rate=3.3,
            new_jobs=215000,
            population=8600000,
            population_growth=1.5,
            single_family_permits=1250,
            multifamily_permits=1750,
            commercial_permits=430,
        ),
    ]


@router.get("/competitive-developments", response_model=List[CompetitiveDevelopmentResponse])
def get_competitive_developments(
    market: str = Query("National", description="Market location"),
    project_type: Optional[str] = Query(None, description="Filter by project type"),
    status: Optional[DevelopmentStatus] = Query(None, description="Filter by status"),
    db: Session = Depends(get_db),
):
    """
    Get competitive development projects in target markets
    """
    # Mock data - replace with actual database queries
    developments = [
        CompetitiveDevelopmentResponse(
            id=1,
            name="Riverside Towers",
            developer="Metro Development Group",
            project_type="Multifamily",
            units=245,
            status=DevelopmentStatus.UNDER_CONSTRUCTION,
            completion_date="Q4 2024",
            price_range="$450k - $850k",
            location="Downtown District",
            amenities=["Pool", "Gym", "Rooftop Deck"],
        ),
        CompetitiveDevelopmentResponse(
            id=2,
            name="Westside Commons",
            developer="Urban Living LLC",
            project_type="Mixed-Use",
            units=180,
            status=DevelopmentStatus.PRE_LEASING,
            completion_date="Q2 2024",
            price_range="$395k - $725k",
            location="West End",
            amenities=["Retail", "Co-working", "Parking"],
        ),
        CompetitiveDevelopmentResponse(
            id=3,
            name="Heritage Park Residences",
            developer="Skyline Properties",
            project_type="Luxury Condos",
            units=92,
            status=DevelopmentStatus.PLANNING,
            completion_date="Q1 2025",
            price_range="$650k - $1.2M",
            location="Historic District",
            amenities=["Concierge", "Spa", "Wine Room"],
        ),
        CompetitiveDevelopmentResponse(
            id=4,
            name="Tech Park Plaza",
            developer="Innovation Realty",
            project_type="Commercial",
            units=0,
            status=DevelopmentStatus.UNDER_CONSTRUCTION,
            completion_date="Q3 2024",
            price_range="N/A",
            location="Tech Corridor",
            amenities=["Conference Center", "Food Hall", "Green Space"],
        ),
    ]

    # Apply filters
    if project_type:
        developments = [d for d in developments if d.project_type.lower() == project_type.lower()]
    if status:
        developments = [d for d in developments if d.status == status]

    return developments


@router.get("/news", response_model=List[NewsArticleResponse])
def get_market_news(
    market: str = Query("National", description="Market location"),
    category: Optional[NewsCategory] = Query(None, description="Filter by category"),
    limit: int = Query(10, ge=1, le=50, description="Number of articles to return"),
    db: Session = Depends(get_db),
):
    """
    Get real estate news filtered by market and category
    """
    # Mock data - replace with actual database queries or news API integration
    articles = [
        NewsArticleResponse(
            id=1,
            title="Fed Signals Potential Rate Cuts in Late 2024",
            source="Wall Street Journal",
            date=date(2024, 6, 15),
            category=NewsCategory.MACRO,
            summary="Federal Reserve officials hint at possible interest rate reductions if inflation continues to cool, potentially boosting real estate markets.",
            url="#",
        ),
        NewsArticleResponse(
            id=2,
            title="Downtown Office-to-Residential Conversions Accelerate",
            source="Commercial Observer",
            date=date(2024, 6, 14),
            category=NewsCategory.LOCAL,
            summary="Three major office buildings announce conversion plans as demand for urban housing remains strong amid remote work trends.",
            url="#",
        ),
        NewsArticleResponse(
            id=3,
            title="Housing Starts Rise 15% in Metropolitan Areas",
            source="Real Estate Weekly",
            date=date(2024, 6, 13),
            category=NewsCategory.CONSTRUCTION,
            summary="New construction permits surge across major metros, signaling developer confidence despite elevated interest rates.",
            url="#",
        ),
        NewsArticleResponse(
            id=4,
            title="Multifamily Investment Volume Up 22% Year-Over-Year",
            source="CBRE Research",
            date=date(2024, 6, 12),
            category=NewsCategory.INVESTMENT,
            summary="Institutional investors return to multifamily sector as cap rates stabilize and rental demand remains robust.",
            url="#",
        ),
        NewsArticleResponse(
            id=5,
            title="Population Growth Drives Housing Demand in Sunbelt Markets",
            source="Bloomberg Real Estate",
            date=date(2024, 6, 11),
            category=NewsCategory.DEMOGRAPHICS,
            summary="Census data shows continued migration to southern and western markets, with job growth outpacing national averages.",
            url="#",
        ),
    ]

    # Apply filters
    if category:
        articles = [a for a in articles if a.category == category]

    return articles[:limit]


# ========================================
# DATABASE-BACKED ENDPOINTS (NEW)
# ========================================

@router.get("/census/demographics")
def get_census_demographics(
    state_code: Optional[str] = Query(None, description="State code (e.g., 'CA', 'NY')"),
    county_code: Optional[str] = Query(None, description="County FIPS code"),
    year: Optional[int] = Query(2023, description="Census year"),
    db: Session = Depends(get_db),
):
    """
    Get Census demographics and housing data.

    **Failsafe**: Returns mock data if database is empty.
    """
    try:
        from app.models import CensusData

        query = db.query(CensusData).filter(CensusData.year == year)

        if state_code:
            query = query.filter(CensusData.state_code == state_code)
        if county_code:
            query = query.filter(CensusData.county_code == county_code)

        results = query.limit(100).all()

        if results:
            return {
                "count": len(results),
                "data": [
                    {
                        "geo_name": r.geo_name,
                        "state_code": r.state_code,
                        "total_population": r.total_population,
                        "median_household_income": r.median_household_income,
                        "median_home_value": r.median_home_value,
                        "median_gross_rent": r.median_gross_rent,
                        "total_housing_units": r.total_housing_units,
                        "owner_occupied": r.owner_occupied,
                        "renter_occupied": r.renter_occupied,
                        "unemployment_rate": r.unemployment_rate,
                        "poverty_rate": r.poverty_rate,
                    }
                    for r in results
                ],
            }
        else:
            # Fallback mock data
            return {
                "count": 1,
                "data": [
                    {
                        "geo_name": "Sample County, CA",
                        "state_code": "CA",
                        "total_population": 500000,
                        "median_household_income": 75000,
                        "median_home_value": 650000,
                        "median_gross_rent": 2100,
                        "total_housing_units": 180000,
                        "owner_occupied": 100000,
                        "renter_occupied": 75000,
                        "unemployment_rate": 4.2,
                        "poverty_rate": 12.5,
                    }
                ],
                "note": "Mock data - no census data in database yet"
            }
    except Exception as e:
        # Fallback on any error
        return {
            "count": 0,
            "data": [],
            "error": str(e),
            "note": "Failed to load data - returning empty result"
        }


@router.get("/property-listings/search")
def search_property_listings(
    city: Optional[str] = Query(None, description="City name"),
    state_code: Optional[str] = Query(None, description="State code"),
    zip_code: Optional[str] = Query(None, description="ZIP code"),
    property_type: Optional[str] = Query(None, description="Property type"),
    listing_type: Optional[str] = Query("for_sale", description="Listing type (for_sale, for_rent)"),
    min_price: Optional[float] = Query(None, description="Minimum price"),
    max_price: Optional[float] = Query(None, description="Maximum price"),
    limit: int = Query(50, description="Max results"),
    db: Session = Depends(get_db),
):
    """
    Search property listings from scraped data.

    **Failsafe**: Returns mock data if database is empty.
    """
    try:
        from app.models import PropertyListing

        query = db.query(PropertyListing)

        if city:
            query = query.filter(PropertyListing.city.ilike(f"%{city}%"))
        if state_code:
            query = query.filter(PropertyListing.state_code == state_code)
        if zip_code:
            query = query.filter(PropertyListing.zip_code == zip_code)
        if property_type:
            query = query.filter(PropertyListing.property_type == property_type)
        if listing_type:
            query = query.filter(PropertyListing.listing_type == listing_type)
        if min_price:
            query = query.filter(PropertyListing.price >= min_price)
        if max_price:
            query = query.filter(PropertyListing.price <= max_price)

        results = query.limit(limit).all()

        if results:
            return {
                "count": len(results),
                "listings": [
                    {
                        "address": r.address,
                        "city": r.city,
                        "state_code": r.state_code,
                        "zip_code": r.zip_code,
                        "price": float(r.price) if r.price else None,
                        "bedrooms": r.bedrooms,
                        "bathrooms": float(r.bathrooms) if r.bathrooms else None,
                        "square_footage": r.square_footage,
                        "property_type": r.property_type,
                        "listing_type": r.listing_type,
                        "days_on_market": r.days_on_market,
                        "source": r.source,
                    }
                    for r in results
                ],
            }
        else:
            # Fallback mock data
            return {
                "count": 3,
                "listings": [
                    {
                        "address": "123 Main St",
                        "city": "San Francisco",
                        "state_code": "CA",
                        "zip_code": "94102",
                        "price": 1250000,
                        "bedrooms": 3,
                        "bathrooms": 2.0,
                        "square_footage": 1800,
                        "property_type": "single_family",
                        "listing_type": "for_sale",
                        "days_on_market": 15,
                        "source": "zillow",
                    },
                    {
                        "address": "456 Oak Ave",
                        "city": "San Francisco",
                        "state_code": "CA",
                        "zip_code": "94103",
                        "price": 895000,
                        "bedrooms": 2,
                        "bathrooms": 1.5,
                        "square_footage": 1200,
                        "property_type": "condo",
                        "listing_type": "for_sale",
                        "days_on_market": 8,
                        "source": "redfin",
                    },
                    {
                        "address": "789 Pine St",
                        "city": "San Francisco",
                        "state_code": "CA",
                        "zip_code": "94104",
                        "price": 4200,
                        "bedrooms": 1,
                        "bathrooms": 1.0,
                        "square_footage": 750,
                        "property_type": "apartment",
                        "listing_type": "for_rent",
                        "days_on_market": 3,
                        "source": "realtor",
                    }
                ],
                "note": "Mock data - no property listings in database yet"
            }
    except Exception as e:
        # Fallback on any error
        return {
            "count": 0,
            "listings": [],
            "error": str(e),
            "note": "Failed to load listings - returning empty result"
        }


@router.get("/fred/indicators")
def get_fred_indicators(
    series_id: Optional[str] = Query(None, description="FRED series ID (e.g., HOUST, MORTGAGE30US)"),
    category: Optional[str] = Query(None, description="Category filter"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    limit: int = Query(100, description="Max results"),
    db: Session = Depends(get_db),
):
    """
    Get FRED economic indicators.

    **Failsafe**: Returns mock data if database is empty.
    """
    try:
        from app.models import FREDIndicator
        from datetime import datetime

        query = db.query(FREDIndicator)

        if series_id:
            query = query.filter(FREDIndicator.series_id == series_id)
        if category:
            query = query.filter(FREDIndicator.category == category)
        if start_date:
            query = query.filter(FREDIndicator.observation_date >= datetime.strptime(start_date, "%Y-%m-%d").date())
        if end_date:
            query = query.filter(FREDIndicator.observation_date <= datetime.strptime(end_date, "%Y-%m-%d").date())

        results = query.order_by(FREDIndicator.observation_date.desc()).limit(limit).all()

        if results:
            return {
                "count": len(results),
                "indicators": [
                    {
                        "series_id": r.series_id,
                        "series_name": r.series_name,
                        "category": r.category,
                        "observation_date": r.observation_date.isoformat() if r.observation_date else None,
                        "value": float(r.value) if r.value else None,
                        "units": r.units,
                        "frequency": r.frequency,
                    }
                    for r in results
                ],
            }
        else:
            # Fallback mock data
            return {
                "count": 2,
                "indicators": [
                    {
                        "series_id": "MORTGAGE30US",
                        "series_name": "30-Year Fixed Rate Mortgage Average",
                        "category": "interest_rates",
                        "observation_date": "2024-06-15",
                        "value": 6.87,
                        "units": "Percent",
                        "frequency": "weekly",
                    },
                    {
                        "series_id": "HOUST",
                        "series_name": "Housing Starts: Total: New Privately Owned",
                        "category": "housing",
                        "observation_date": "2024-05-01",
                        "value": 1360,
                        "units": "Thousands of Units",
                        "frequency": "monthly",
                    },
                ],
                "note": "Mock data - no FRED data in database yet"
            }
    except Exception as e:
        # Fallback on any error
        return {
            "count": 0,
            "indicators": [],
            "error": str(e),
            "note": "Failed to load indicators - returning empty result"
        }


@router.get("/hud/fair-market-rents")
def get_hud_fair_market_rents(
    state_code: Optional[str] = Query(None, description="State code"),
    county: Optional[str] = Query(None, description="County name"),
    fiscal_year: int = Query(2024, description="HUD fiscal year"),
    limit: int = Query(100, description="Max results"),
    db: Session = Depends(get_db),
):
    """
    Get HUD Fair Market Rent data.

    **Failsafe**: Returns mock data if database is empty.
    """
    try:
        from app.models import HUDFairMarketRent

        query = db.query(HUDFairMarketRent).filter(HUDFairMarketRent.fiscal_year == fiscal_year)

        if state_code:
            query = query.filter(HUDFairMarketRent.state_code == state_code)
        if county:
            query = query.filter(HUDFairMarketRent.county_name.ilike(f"%{county}%"))

        results = query.limit(limit).all()

        if results:
            return {
                "count": len(results),
                "fmr_data": [
                    {
                        "county_name": r.county_name,
                        "state_code": r.state_code,
                        "metro_name": r.metro_name,
                        "fiscal_year": r.fiscal_year,
                        "fmr_0br": r.fmr_0br,
                        "fmr_1br": r.fmr_1br,
                        "fmr_2br": r.fmr_2br,
                        "fmr_3br": r.fmr_3br,
                        "fmr_4br": r.fmr_4br,
                        "median_family_income": r.median_family_income,
                    }
                    for r in results
                ],
            }
        else:
            # Fallback mock data
            return {
                "count": 1,
                "fmr_data": [
                    {
                        "county_name": "San Francisco County",
                        "state_code": "CA",
                        "metro_name": "San Francisco-Oakland-Hayward, CA HUD Metro FMR Area",
                        "fiscal_year": 2024,
                        "fmr_0br": 2190,
                        "fmr_1br": 2790,
                        "fmr_2br": 3620,
                        "fmr_3br": 5010,
                        "fmr_4br": 6180,
                        "median_family_income": 154500,
                    }
                ],
                "note": "Mock data - no HUD data in database yet"
            }
    except Exception as e:
        # Fallback on any error
        return {
            "count": 0,
            "fmr_data": [],
            "error": str(e),
            "note": "Failed to load FMR data - returning empty result"
        }


# ========================================
# DATA IMPORT ENDPOINTS
# ========================================

@router.post("/import/all")
def import_all_data(db: Session = Depends(get_db)):
    """
    Import sample data from all sources (Census, FRED, HUD, Property Listings).

    This endpoint populates the database with sample data for demonstration purposes.
    In production, this would be replaced with actual API calls to government data sources.
    """
    try:
        from app.services.market_data_importer import MarketDataImporter

        importer = MarketDataImporter(db)
        result = importer.import_all_sample_data()

        return {
            "success": result["success"],
            "message": "Data import completed",
            "total_inserted": result["total_inserted"],
            "total_updated": result["total_updated"],
            "details": result["details"],
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Import failed: {str(e)}",
            "error": str(e),
        }


@router.post("/import/census")
def import_census_data(db: Session = Depends(get_db)):
    """
    Import sample Census data.

    Imports demographics and housing statistics for California counties.
    """
    try:
        from app.services.market_data_importer import MarketDataImporter

        importer = MarketDataImporter(db)
        result = importer.import_sample_census_data()

        return {
            "success": result["success"],
            "message": "Census data import completed" if result["success"] else "Census data import failed",
            "records_processed": result.get("records_processed", 0),
            "records_inserted": result.get("records_inserted", 0),
            "records_updated": result.get("records_updated", 0),
            "job_id": result.get("job_id"),
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Import failed: {str(e)}",
            "error": str(e),
        }


@router.post("/import/fred")
def import_fred_data(db: Session = Depends(get_db)):
    """
    Import sample FRED economic indicators.

    Imports data including mortgage rates, housing starts, and home price indexes.
    """
    try:
        from app.services.market_data_importer import MarketDataImporter

        importer = MarketDataImporter(db)
        result = importer.import_sample_fred_data()

        return {
            "success": result["success"],
            "message": "FRED data import completed" if result["success"] else "FRED data import failed",
            "records_processed": result.get("records_processed", 0),
            "records_inserted": result.get("records_inserted", 0),
            "records_updated": result.get("records_updated", 0),
            "job_id": result.get("job_id"),
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Import failed: {str(e)}",
            "error": str(e),
        }


@router.post("/import/hud")
def import_hud_data(db: Session = Depends(get_db)):
    """
    Import sample HUD Fair Market Rent data.

    Imports rental market data for California metros.
    """
    try:
        from app.services.market_data_importer import MarketDataImporter

        importer = MarketDataImporter(db)
        result = importer.import_sample_hud_data()

        return {
            "success": result["success"],
            "message": "HUD data import completed" if result["success"] else "HUD data import failed",
            "records_processed": result.get("records_processed", 0),
            "records_inserted": result.get("records_inserted", 0),
            "records_updated": result.get("records_updated", 0),
            "job_id": result.get("job_id"),
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Import failed: {str(e)}",
            "error": str(e),
        }


@router.post("/import/property-listings")
def import_property_listings(db: Session = Depends(get_db)):
    """
    Import sample property listings.

    Imports scraped property data from various sources (Zillow, Redfin, etc.).
    """
    try:
        from app.services.market_data_importer import MarketDataImporter

        importer = MarketDataImporter(db)
        result = importer.import_sample_property_listings()

        return {
            "success": result["success"],
            "message": "Property listings import completed" if result["success"] else "Property listings import failed",
            "records_processed": result.get("records_processed", 0),
            "records_inserted": result.get("records_inserted", 0),
            "records_updated": result.get("records_updated", 0),
            "job_id": result.get("job_id"),
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Import failed: {str(e)}",
            "error": str(e),
        }


@router.get("/import/jobs")
def get_import_jobs(
    data_source: Optional[str] = Query(None, description="Filter by data source"),
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: int = Query(20, description="Max results"),
    db: Session = Depends(get_db),
):
    """
    Get import job history and status.

    Returns a list of all data import jobs with their status and metrics.
    """
    try:
        from app.models import MarketDataImport

        query = db.query(MarketDataImport)

        if data_source:
            query = query.filter(MarketDataImport.data_source == data_source)
        if status:
            query = query.filter(MarketDataImport.status == status)

        results = query.order_by(MarketDataImport.created_at.desc()).limit(limit).all()

        return {
            "count": len(results),
            "jobs": [
                {
                    "id": r.id,
                    "data_source": r.data_source,
                    "import_type": r.import_type,
                    "status": r.status,
                    "records_processed": r.records_processed,
                    "records_inserted": r.records_inserted,
                    "records_updated": r.records_updated,
                    "records_failed": r.records_failed,
                    "started_at": r.started_at.isoformat() if r.started_at else None,
                    "completed_at": r.completed_at.isoformat() if r.completed_at else None,
                    "duration_seconds": r.duration_seconds,
                    "error_message": r.error_message,
                }
                for r in results
            ],
        }
    except Exception as e:
        return {
            "count": 0,
            "jobs": [],
            "error": str(e),
        }


from functools import lru_cache
from datetime import datetime, timedelta
import statistics

# Simple in-memory cache with timestamp
_usa_economics_cache = {
    "data": None,
    "timestamp": None,
    "ttl": 3600  # 1 hour cache
}

def _get_cached_usa_data(category: Optional[str] = None):
    """Get cached USA economics data if available and fresh."""
    cache = _usa_economics_cache
    now = datetime.now()

    # Check if cache is valid
    if cache["data"] and cache["timestamp"]:
        age = (now - cache["timestamp"]).total_seconds()
        if age < cache["ttl"]:
            # Filter by category if needed
            if category:
                filtered_indicators = [
                    ind for ind in cache["data"]["indicators"]
                    if ind.get("category") == category
                ]
                return {
                    **cache["data"],
                    "indicators": filtered_indicators,
                    "total_indicators": len(filtered_indicators),
                    "cached": True,
                    "cache_age_seconds": int(age)
                }
            return {**cache["data"], "cached": True, "cache_age_seconds": int(age)}

    return None

def _update_usa_data_cache(data: dict):
    """Update the USA economics data cache."""
    _usa_economics_cache["data"] = data
    _usa_economics_cache["timestamp"] = datetime.now()

@router.get("/data/usa-economics")
async def get_usa_economic_data(
    category: Optional[str] = Query(None, description="Category filter (overview, gdp, labour, prices, health, money, trade, government, business, housing)"),
    limit: Optional[int] = Query(None, description="Limit number of indicators returned"),
    use_cache: bool = Query(True, description="Use cached data if available")
):
    """
    Get USA economic indicators from country-specific database with caching.

    Returns economic data across 10 categories with 345+ indicators including:
    - Overview: Key economic metrics (23 indicators)
    - GDP: Growth, composition, and related metrics (25 indicators)
    - Labour: Employment, unemployment, wages (63 indicators)
    - Prices: Inflation, CPI, PPI (45 indicators)
    - Health: Healthcare metrics (4 indicators)
    - Money: Interest rates, money supply (14 indicators)
    - Trade: Imports, exports, balance of trade (24 indicators)
    - Government: Debt, budget, taxes (20 indicators)
    - Business: PMI, confidence, production (91 indicators)
    - Housing: Permits, starts, prices (36 indicators)

    Cache: Data is cached for 1 hour by default. Set use_cache=false to bypass.
    """
    try:
        # Try to get from cache first
        if use_cache:
            cached_data = _get_cached_usa_data(category)
            if cached_data:
                if limit:
                    cached_data["indicators"] = cached_data["indicators"][:limit]
                    cached_data["total_indicators"] = len(cached_data["indicators"])
                return cached_data

        from app.database.country_database_manager import country_db_manager
        from app.models.economics import EconomicIndicator
        from sqlalchemy import func

        # Get session for USA database
        db = country_db_manager.get_session("united-states")

        try:
            # Build query
            query = db.query(EconomicIndicator)

            # Apply category filter if provided
            if category:
                query = query.filter(EconomicIndicator.category == category)

            # Order by most recent first
            query = query.order_by(EconomicIndicator.data_date.desc())

            # Apply limit if provided
            if limit:
                query = query.limit(limit)

            # Execute query
            indicators = query.all()

            # Get category summary
            category_counts = db.query(
                EconomicIndicator.category,
                func.count(EconomicIndicator.id).label('count')
            ).group_by(EconomicIndicator.category).all()

            # Calculate change percentages
            indicators_data = []
            for ind in indicators:
                ind_dict = {
                    "id": ind.id,
                    "category": ind.category,
                    "indicator_name": ind.indicator_name,
                    "last_value": ind.last_value,
                    "last_value_numeric": ind.last_value_numeric,
                    "previous_value": ind.previous_value,
                    "previous_value_numeric": ind.previous_value_numeric,
                    "highest_value": ind.highest_value,
                    "highest_value_numeric": ind.highest_value_numeric,
                    "lowest_value": ind.lowest_value,
                    "lowest_value_numeric": ind.lowest_value_numeric,
                    "unit": ind.unit,
                    "reference_period": ind.reference_period,
                    "data_date": ind.data_date.isoformat() if ind.data_date else None,
                }

                # Calculate change percentage
                if ind.last_value_numeric is not None and ind.previous_value_numeric is not None and ind.previous_value_numeric != 0:
                    change_percent = ((ind.last_value_numeric - ind.previous_value_numeric) / ind.previous_value_numeric) * 100
                    ind_dict["change_percent"] = round(change_percent, 2)
                    ind_dict["change_absolute"] = round(ind.last_value_numeric - ind.previous_value_numeric, 2)

                indicators_data.append(ind_dict)

            result = {
                "success": True,
                "country": "United States",
                "total_indicators": len(indicators_data),
                "category_summary": {cat: count for cat, count in category_counts},
                "indicators": indicators_data,
                "cached": False,
                "timestamp": datetime.now().isoformat()
            }

            # Update cache if no category filter (full data)
            if not category and use_cache:
                _update_usa_data_cache(result)

            return result

        finally:
            db.close()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve USA economic data: {str(e)}"
        )


@router.get("/data/usa-economics/categories")
async def get_usa_economic_categories():
    """
    Get list of available USA economic data categories with counts.
    """
    try:
        from app.database.country_database_manager import country_db_manager
        from app.models.economics import EconomicIndicator
        from sqlalchemy import func

        db = country_db_manager.get_session("united-states")

        try:
            category_counts = db.query(
                EconomicIndicator.category,
                func.count(EconomicIndicator.id).label('count'),
                func.max(EconomicIndicator.data_date).label('latest_date')
            ).group_by(EconomicIndicator.category).all()

            return {
                "success": True,
                "country": "United States",
                "categories": [
                    {
                        "category": cat,
                        "count": count,
                        "latest_update": latest.isoformat() if latest else None
                    }
                    for cat, count, latest in category_counts
                ]
            }
        finally:
            db.close()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve category list: {str(e)}"
        )


@router.get("/data/usa-economics/analysis")
async def get_usa_economic_analysis():
    """
    Get comprehensive economic analysis including trends, correlations, and key insights.
    """
    try:
        from app.database.country_database_manager import country_db_manager
        from app.models.economics import EconomicIndicator
        from sqlalchemy import func

        db = country_db_manager.get_session("united-states")

        try:
            # Get all indicators
            indicators = db.query(EconomicIndicator).all()

            # Calculate statistics by category
            category_stats = {}
            for cat in set(ind.category for ind in indicators):
                cat_indicators = [ind for ind in indicators if ind.category == cat]

                # Count indicators with positive/negative changes
                positive_changes = sum(1 for ind in cat_indicators
                                     if ind.last_value_numeric and ind.previous_value_numeric
                                     and ind.last_value_numeric > ind.previous_value_numeric)
                negative_changes = sum(1 for ind in cat_indicators
                                     if ind.last_value_numeric and ind.previous_value_numeric
                                     and ind.last_value_numeric < ind.previous_value_numeric)

                # Calculate average change percentage
                changes = []
                for ind in cat_indicators:
                    if ind.last_value_numeric and ind.previous_value_numeric and ind.previous_value_numeric != 0:
                        change = ((ind.last_value_numeric - ind.previous_value_numeric) / ind.previous_value_numeric) * 100
                        changes.append(change)

                avg_change = statistics.mean(changes) if changes else 0

                category_stats[cat] = {
                    "total_indicators": len(cat_indicators),
                    "positive_changes": positive_changes,
                    "negative_changes": negative_changes,
                    "avg_change_percent": round(avg_change, 2),
                    "trend": "bullish" if avg_change > 0 else "bearish" if avg_change < 0 else "neutral"
                }

            # Key indicators for dashboard
            key_indicators = {}
            key_names = [
                "GDP Growth Rate",
                "Unemployment Rate",
                "Inflation Rate",
                "Interest Rate",
                "Consumer Confidence",
                "Industrial Production"
            ]

            for name in key_names:
                ind = db.query(EconomicIndicator).filter(
                    EconomicIndicator.indicator_name.ilike(f"%{name}%")
                ).first()

                if ind:
                    change_percent = None
                    if ind.last_value_numeric and ind.previous_value_numeric and ind.previous_value_numeric != 0:
                        change_percent = ((ind.last_value_numeric - ind.previous_value_numeric) / ind.previous_value_numeric) * 100

                    key_indicators[name] = {
                        "value": ind.last_value,
                        "numeric_value": ind.last_value_numeric,
                        "previous": ind.previous_value,
                        "change_percent": round(change_percent, 2) if change_percent else None,
                        "unit": ind.unit,
                        "category": ind.category
                    }

            # Economic health score (0-100)
            health_scores = []

            # GDP growth (target: 2-3%)
            gdp_ind = db.query(EconomicIndicator).filter(
                EconomicIndicator.indicator_name.ilike("%GDP Growth%")
            ).first()
            if gdp_ind and gdp_ind.last_value_numeric:
                gdp_score = min(100, max(0, (gdp_ind.last_value_numeric / 3.0) * 100))
                health_scores.append(gdp_score)

            # Unemployment (target: < 5%)
            unemp_ind = db.query(EconomicIndicator).filter(
                EconomicIndicator.indicator_name.ilike("%Unemployment Rate%")
            ).first()
            if unemp_ind and unemp_ind.last_value_numeric:
                unemp_score = max(0, 100 - (unemp_ind.last_value_numeric * 10))
                health_scores.append(unemp_score)

            # Inflation (target: 2%)
            inf_ind = db.query(EconomicIndicator).filter(
                EconomicIndicator.indicator_name.ilike("%Inflation Rate%")
            ).first()
            if inf_ind and inf_ind.last_value_numeric:
                inf_score = max(0, 100 - abs(inf_ind.last_value_numeric - 2) * 20)
                health_scores.append(inf_score)

            economic_health = round(statistics.mean(health_scores), 2) if health_scores else 50

            return {
                "success": True,
                "country": "United States",
                "economic_health_score": economic_health,
                "health_rating": "strong" if economic_health > 75 else "moderate" if economic_health > 50 else "weak",
                "category_stats": category_stats,
                "key_indicators": key_indicators,
                "summary": {
                    "total_categories": len(category_stats),
                    "total_indicators": len(indicators),
                    "bullish_categories": sum(1 for s in category_stats.values() if s["trend"] == "bullish"),
                    "bearish_categories": sum(1 for s in category_stats.values() if s["trend"] == "bearish"),
                },
                "timestamp": datetime.now().isoformat()
            }

        finally:
            db.close()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate economic analysis: {str(e)}"
        )


@router.get("/data/usa-economics/trends")
async def get_usa_economic_trends(
    category: Optional[str] = Query(None, description="Filter by category")
):
    """
    Get trending economic indicators showing largest changes.
    """
    try:
        from app.database.country_database_manager import country_db_manager
        from app.models.economics import EconomicIndicator

        db = country_db_manager.get_session("united-states")

        try:
            query = db.query(EconomicIndicator)

            if category:
                query = query.filter(EconomicIndicator.category == category)

            indicators = query.all()

            # Calculate changes and sort
            trending = []
            for ind in indicators:
                if ind.last_value_numeric and ind.previous_value_numeric and ind.previous_value_numeric != 0:
                    change_percent = ((ind.last_value_numeric - ind.previous_value_numeric) / ind.previous_value_numeric) * 100
                    trending.append({
                        "indicator_name": ind.indicator_name,
                        "category": ind.category,
                        "current_value": ind.last_value,
                        "previous_value": ind.previous_value,
                        "change_percent": round(change_percent, 2),
                        "change_absolute": round(ind.last_value_numeric - ind.previous_value_numeric, 2),
                        "unit": ind.unit,
                        "reference_period": ind.reference_period
                    })

            # Sort by absolute change
            trending.sort(key=lambda x: abs(x["change_percent"]), reverse=True)

            return {
                "success": True,
                "country": "United States",
                "top_gainers": [t for t in trending if t["change_percent"] > 0][:10],
                "top_losers": [t for t in trending if t["change_percent"] < 0][:10],
                "most_volatile": trending[:20],
                "timestamp": datetime.now().isoformat()
            }

        finally:
            db.close()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve economic trends: {str(e)}"
        )


# ============================================================================
# TIME SERIES / HISTORICAL DATA ENDPOINTS
# ============================================================================

class HistoricalDataPoint(BaseModel):
    """Single historical data point"""
    date: datetime
    value: Optional[float]
    change_from_previous: Optional[float] = None
    change_percent: Optional[float] = None


class HistoricalDataResponse(BaseModel):
    """Time series data response"""
    indicator_name: str
    country: str
    category: Optional[str] = None
    unit: Optional[str] = None
    data_points: List[HistoricalDataPoint]
    count: int
    start_date: datetime
    end_date: datetime
    frequency: Optional[str] = None
    statistics: Optional[dict] = None


class MultiSeriesResponse(BaseModel):
    """Multiple time series data response"""
    series: List[HistoricalDataResponse]
    count: int
    timestamp: str


@router.get(
    "/data/usa-economics/history/{indicator_name}",
    response_model=HistoricalDataResponse,
    summary="Get historical time series for an economic indicator",
    description="Retrieve time series data for a specific USA economic indicator"
)
async def get_indicator_historical_data(
    indicator_name: str,
    start_date: Optional[date] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date (YYYY-MM-DD)"),
    limit: int = Query(365, ge=1, le=3650, description="Maximum number of data points"),
    db: Session = Depends(get_db)
):
    """
    Get historical time series data for a specific USA economic indicator.

    **Features:**
    - Date range filtering
    - Automatic statistics calculation (min, max, avg, trend)
    - Change calculations (absolute and percent)
    - Supports up to 10 years of data (3650 days)

    **Use Cases:**
    - Historical charts
    - Trend analysis
    - Forecasting inputs
    - Correlation studies
    """
    try:
        from app.services.economics_db_service import EconomicsDBService
        from app.models.economics import EconomicIndicatorHistory

        service = EconomicsDBService(db)

        # Get historical data
        history = service.get_indicator_history(
            country="United States",
            indicator_name=indicator_name,
            start_date=start_date,
            end_date=end_date,
            limit=limit
        )

        if not history:
            raise HTTPException(
                status_code=404,
                detail=f"No historical data found for indicator: {indicator_name}"
            )

        # Convert to response format
        data_points = [
            HistoricalDataPoint(
                date=h.observation_date,
                value=h.value_numeric,
                change_from_previous=h.change_from_previous,
                change_percent=h.change_percent
            )
            for h in reversed(history)  # Oldest to newest
        ]

        # Calculate statistics
        values = [dp.value for dp in data_points if dp.value is not None]
        statistics = None
        if values:
            statistics = {
                "min": min(values),
                "max": max(values),
                "avg": sum(values) / len(values),
                "latest": values[-1],
                "first": values[0],
                "total_change": values[-1] - values[0] if len(values) > 1 else 0,
                "total_change_percent": ((values[-1] - values[0]) / values[0] * 100) if len(values) > 1 and values[0] != 0 else 0,
                "data_points_count": len(values)
            }

        return HistoricalDataResponse(
            indicator_name=indicator_name,
            country="United States",
            category=history[0].category if history else None,
            unit=history[0].unit if history else None,
            data_points=data_points,
            count=len(data_points),
            start_date=data_points[0].date if data_points else datetime.now(),
            end_date=data_points[-1].date if data_points else datetime.now(),
            frequency=history[0].frequency if history else None,
            statistics=statistics
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve historical data: {str(e)}"
        )


@router.get(
    "/data/usa-economics/history/multiple",
    response_model=MultiSeriesResponse,
    summary="Get historical data for multiple indicators",
    description="Retrieve time series data for multiple USA economic indicators"
)
async def get_multiple_indicators_historical_data(
    indicator_names: List[str] = Query(..., description="List of indicator names"),
    start_date: Optional[date] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date (YYYY-MM-DD)"),
    limit: int = Query(365, ge=1, le=3650, description="Maximum number of data points per indicator"),
    db: Session = Depends(get_db)
):
    """
    Get historical time series data for multiple USA economic indicators.

    **Use Cases:**
    - Multi-line charts comparing indicators
    - Correlation analysis
    - Dashboard widgets with multiple metrics
    - Comparative trend analysis

    **Example:**
    ```
    GET /data/usa-economics/history/multiple?indicator_names=GDP&indicator_names=Unemployment%20Rate
    ```
    """
    try:
        from app.services.economics_db_service import EconomicsDBService

        service = EconomicsDBService(db)
        series_list = []

        for indicator_name in indicator_names:
            try:
                # Get historical data for this indicator
                history = service.get_indicator_history(
                    country="United States",
                    indicator_name=indicator_name,
                    start_date=start_date,
                    end_date=end_date,
                    limit=limit
                )

                if history:
                    # Convert to response format
                    data_points = [
                        HistoricalDataPoint(
                            date=h.observation_date,
                            value=h.value_numeric,
                            change_from_previous=h.change_from_previous,
                            change_percent=h.change_percent
                        )
                        for h in reversed(history)
                    ]

                    # Calculate statistics
                    values = [dp.value for dp in data_points if dp.value is not None]
                    statistics = None
                    if values:
                        statistics = {
                            "min": min(values),
                            "max": max(values),
                            "avg": sum(values) / len(values),
                            "latest": values[-1],
                            "first": values[0],
                            "total_change": values[-1] - values[0] if len(values) > 1 else 0,
                            "total_change_percent": ((values[-1] - values[0]) / values[0] * 100) if len(values) > 1 and values[0] != 0 else 0
                        }

                    series_list.append(
                        HistoricalDataResponse(
                            indicator_name=indicator_name,
                            country="United States",
                            category=history[0].category if history else None,
                            unit=history[0].unit if history else None,
                            data_points=data_points,
                            count=len(data_points),
                            start_date=data_points[0].date if data_points else datetime.now(),
                            end_date=data_points[-1].date if data_points else datetime.now(),
                            frequency=history[0].frequency if history else None,
                            statistics=statistics
                        )
                    )
            except Exception as e:
                # Skip indicators that fail, but log error
                print(f"Error fetching history for {indicator_name}: {str(e)}")
                continue

        if not series_list:
            raise HTTPException(
                status_code=404,
                detail="No historical data found for any of the requested indicators"
            )

        return MultiSeriesResponse(
            series=series_list,
            count=len(series_list),
            timestamp=datetime.now().isoformat()
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve multiple historical series: {str(e)}"
        )


@router.get(
    "/data/usa-economics/history/category/{category}",
    response_model=MultiSeriesResponse,
    summary="Get historical data for all indicators in a category",
    description="Retrieve time series data for all indicators within a specific category"
)
async def get_category_historical_data(
    category: str,
    start_date: Optional[date] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date (YYYY-MM-DD)"),
    limit: int = Query(365, ge=1, le=3650, description="Maximum number of data points per indicator"),
    max_indicators: int = Query(20, ge=1, le=50, description="Maximum number of indicators to return"),
    db: Session = Depends(get_db)
):
    """
    Get historical time series data for all indicators in a category.

    **Categories:**
    - employment
    - housing
    - inflation
    - gdp
    - interest_rates
    - consumer_spending
    - manufacturing
    - trade
    - sentiment
    - financial_markets

    **Use Cases:**
    - Category-specific dashboards
    - Sector analysis
    - Related indicator comparisons
    """
    try:
        from app.services.economics_db_service import EconomicsDBService
        from app.models.economics import EconomicIndicator

        service = EconomicsDBService(db)

        # Get all indicators in this category
        indicators = db.query(EconomicIndicator).filter(
            EconomicIndicator.country_name == "United States",
            EconomicIndicator.category == category
        ).limit(max_indicators).all()

        if not indicators:
            raise HTTPException(
                status_code=404,
                detail=f"No indicators found in category: {category}"
            )

        series_list = []

        for indicator in indicators:
            try:
                # Get historical data
                history = service.get_indicator_history(
                    country="United States",
                    indicator_name=indicator.indicator_name,
                    start_date=start_date,
                    end_date=end_date,
                    limit=limit
                )

                if history:
                    data_points = [
                        HistoricalDataPoint(
                            date=h.observation_date,
                            value=h.value_numeric,
                            change_from_previous=h.change_from_previous,
                            change_percent=h.change_percent
                        )
                        for h in reversed(history)
                    ]

                    # Calculate statistics
                    values = [dp.value for dp in data_points if dp.value is not None]
                    statistics = None
                    if values:
                        statistics = {
                            "min": min(values),
                            "max": max(values),
                            "avg": sum(values) / len(values),
                            "latest": values[-1]
                        }

                    series_list.append(
                        HistoricalDataResponse(
                            indicator_name=indicator.indicator_name,
                            country="United States",
                            category=category,
                            unit=indicator.unit,
                            data_points=data_points,
                            count=len(data_points),
                            start_date=data_points[0].date if data_points else datetime.now(),
                            end_date=data_points[-1].date if data_points else datetime.now(),
                            frequency=indicator.frequency,
                            statistics=statistics
                        )
                    )
            except Exception:
                continue

        if not series_list:
            raise HTTPException(
                status_code=404,
                detail=f"No historical data found for category: {category}"
            )

        return MultiSeriesResponse(
            series=series_list,
            count=len(series_list),
            timestamp=datetime.now().isoformat()
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve category historical data: {str(e)}"
        )


# ==================== Prophet Forecasting Endpoints ====================

class ForecastRequest(BaseModel):
    """Request model for generating forecasts"""
    forecast_periods: int = Field(365, ge=1, le=1825, description="Number of days to forecast (max 5 years)")
    historical_days: int = Field(730, ge=30, le=3650, description="Days of historical data to use (max 10 years)")
    seasonality_mode: str = Field('additive', description="Seasonality mode: 'additive' or 'multiplicative'")
    include_holidays: bool = Field(False, description="Include US holidays in the model")
    changepoint_prior_scale: float = Field(0.05, ge=0.001, le=0.5, description="Flexibility of trend changes")
    seasonality_prior_scale: float = Field(10.0, ge=0.01, le=10.0, description="Flexibility of seasonality")
    confidence_interval: float = Field(0.95, ge=0.80, le=0.99, description="Confidence interval width")


class ForecastDataPoint(BaseModel):
    """Single forecast data point"""
    date: str
    value: float
    lower_bound: float
    upper_bound: float
    is_forecast: bool
    trend: Optional[float] = None
    yearly_seasonality: Optional[float] = None


class ForecastComponentsResponse(BaseModel):
    """Forecast components (trend, seasonality)"""
    trend: Optional[List[dict]] = None
    trend_direction: Optional[str] = None
    trend_strength: Optional[float] = None
    yearly_seasonality: Optional[List[dict]] = None
    seasonality_strength: Optional[float] = None
    changepoints: Optional[List[str]] = None


class ForecastMetrics(BaseModel):
    """Forecast quality metrics"""
    mae: float
    mape: float
    rmse: float
    r_squared: float
    forecast_quality: str
    forecast_mean: float
    forecast_min: float
    forecast_max: float
    forecast_std: float
    total_change: float
    total_change_percent: float
    avg_confidence_interval_width: float


class ForecastResponse(BaseModel):
    """Complete forecast response"""
    indicator_name: str
    country: str
    forecast_start: str
    forecast_end: str
    forecast_periods: int
    historical_periods: int
    historical_start: str
    historical_end: str
    forecast: List[ForecastDataPoint]
    components: ForecastComponentsResponse
    metrics: ForecastMetrics
    parameters: dict
    timestamp: str


class MultipleForecastsResponse(BaseModel):
    """Response for multiple forecasts"""
    forecasts: List[ForecastResponse]
    count: int
    errors: List[dict]
    timestamp: str


class RecommendationItem(BaseModel):
    """Single recommendation"""
    type: str
    severity: str
    message: str


class ForecastRecommendationsResponse(BaseModel):
    """Forecast recommendations and insights"""
    recommendations: List[RecommendationItem]
    risk_level: str
    confidence: str
    key_insights: dict


@router.post(
    "/data/usa-economics/forecast/{indicator_name}",
    response_model=ForecastResponse,
    summary="Generate time-series forecast for an economic indicator",
    description="""
    Generate a Prophet-based forecast for a USA economic indicator.

    Features:
    - Configurable forecast horizon (1 day to 5 years)
    - Automatic trend and seasonality detection
    - Confidence intervals for predictions
    - Quality metrics (MAE, MAPE, RMSE, R²)
    - Component analysis (trend, yearly seasonality)
    - Changepoint detection

    Parameters:
    - forecast_periods: How many days to forecast (default: 365 = 1 year)
    - historical_days: How much historical data to use (default: 730 = 2 years)
    - seasonality_mode: 'additive' for absolute changes, 'multiplicative' for percentage changes
    - include_holidays: Add US federal holidays to the model
    - changepoint_prior_scale: Higher = more flexible trend (0.001-0.5)
    - seasonality_prior_scale: Higher = more flexible seasonality (0.01-10)
    - confidence_interval: Prediction interval width (0.80-0.99)

    Returns:
    - Historical fit and future forecast with confidence bounds
    - Trend and seasonality components
    - Quality metrics and forecast assessment
    - Model parameters used
    """
)
async def generate_forecast(
    indicator_name: str = Path(..., description="Name of the economic indicator to forecast"),
    request: ForecastRequest = Body(...),
    db: Session = Depends(get_db)
):
    """
    Generate a time-series forecast for a USA economic indicator using Prophet.

    Example indicators:
    - GDP
    - Unemployment Rate
    - Inflation Rate
    - Interest Rate
    - Housing Starts
    - Consumer Confidence
    """
    try:
        from app.services.prophet_forecasting_service import ProphetForecastingService

        service = ProphetForecastingService(db)

        result = service.generate_forecast(
            country="United States",
            indicator_name=indicator_name,
            forecast_periods=request.forecast_periods,
            historical_days=request.historical_days,
            seasonality_mode=request.seasonality_mode,
            include_holidays=request.include_holidays,
            changepoint_prior_scale=request.changepoint_prior_scale,
            seasonality_prior_scale=request.seasonality_prior_scale,
            confidence_interval=request.confidence_interval
        )

        return result

    except ImportError as e:
        raise HTTPException(
            status_code=503,
            detail={
                "error": "Prophet library not available",
                "message": str(e),
                "install_command": "pip install prophet"
            }
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid forecast parameters: {str(e)}"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating forecast for {indicator_name}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate forecast: {str(e)}"
        )


@router.post(
    "/data/usa-economics/forecast/multiple",
    response_model=MultipleForecastsResponse,
    summary="Generate forecasts for multiple economic indicators",
    description="""
    Generate Prophet-based forecasts for multiple USA economic indicators.

    Useful for:
    - Comparing future trends across indicators
    - Portfolio scenario analysis
    - Multi-factor economic projections

    Note: Failed indicators are logged in the 'errors' field and don't stop execution.
    """
)
async def generate_multiple_forecasts(
    indicator_names: List[str] = Body(..., embed=True, description="List of indicator names to forecast"),
    request: ForecastRequest = Body(...),
    db: Session = Depends(get_db)
):
    """
    Generate forecasts for multiple USA economic indicators.

    Returns successful forecasts and logs any errors.
    """
    try:
        from app.services.prophet_forecasting_service import ProphetForecastingService

        service = ProphetForecastingService(db)

        result = service.generate_multiple_forecasts(
            country="United States",
            indicator_names=indicator_names,
            forecast_periods=request.forecast_periods,
            historical_days=request.historical_days,
            seasonality_mode=request.seasonality_mode,
            include_holidays=request.include_holidays,
            changepoint_prior_scale=request.changepoint_prior_scale,
            seasonality_prior_scale=request.seasonality_prior_scale,
            confidence_interval=request.confidence_interval
        )

        return result

    except ImportError as e:
        raise HTTPException(
            status_code=503,
            detail={
                "error": "Prophet library not available",
                "message": str(e),
                "install_command": "pip install prophet"
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating multiple forecasts: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate forecasts: {str(e)}"
        )


@router.post(
    "/data/usa-economics/forecast/{indicator_name}/recommendations",
    response_model=ForecastRecommendationsResponse,
    summary="Get actionable recommendations from a forecast",
    description="""
    Generate actionable investment and risk recommendations based on a forecast.

    Analyzes:
    - Trend direction and strength
    - Volatility and uncertainty
    - Forecast quality
    - Expected changes

    Returns:
    - List of recommendations with severity levels
    - Overall risk assessment
    - Key insights summary
    """
)
async def get_forecast_recommendations(
    indicator_name: str = Path(..., description="Name of the economic indicator"),
    request: ForecastRequest = Body(...),
    db: Session = Depends(get_db)
):
    """
    Get actionable recommendations based on a forecast.

    First generates the forecast, then analyzes it for investment insights.
    """
    try:
        from app.services.prophet_forecasting_service import ProphetForecastingService

        service = ProphetForecastingService(db)

        # Generate forecast
        forecast_result = service.generate_forecast(
            country="United States",
            indicator_name=indicator_name,
            forecast_periods=request.forecast_periods,
            historical_days=request.historical_days,
            seasonality_mode=request.seasonality_mode,
            include_holidays=request.include_holidays,
            changepoint_prior_scale=request.changepoint_prior_scale,
            seasonality_prior_scale=request.seasonality_prior_scale,
            confidence_interval=request.confidence_interval
        )

        # Generate recommendations
        recommendations = service.get_forecast_recommendations(forecast_result)

        return recommendations

    except ImportError as e:
        raise HTTPException(
            status_code=503,
            detail={
                "error": "Prophet library not available",
                "message": str(e),
                "install_command": "pip install prophet"
            }
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid forecast parameters: {str(e)}"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating recommendations for {indicator_name}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate recommendations: {str(e)}"
        )


@router.get(
    "/forecast/availability",
    summary="Check Prophet forecasting availability",
    description="Check if Prophet library is installed and available for forecasting"
)
async def check_forecast_availability():
    """
    Check if Prophet forecasting is available.

    Returns installation status and version information.
    """
    try:
        from app.services.prophet_forecasting_service import check_prophet_availability

        status = check_prophet_availability()

        if not status.get("available"):
            return JSONResponse(
                status_code=503,
                content=status
            )

        return status

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "available": False,
                "message": f"Error checking Prophet availability: {str(e)}"
            }
        )


# ========================================
# DATA IMPORT/EXPORT ENDPOINTS
# ========================================

@router.post(
    "/data/usa-economics/upload",
    summary="Upload economic data from CSV/Excel",
    description="Upload economic indicators from CSV or Excel file. Supports .csv, .xlsx, .xls formats."
)
async def upload_economic_data(
    file: UploadFile = File(..., description="CSV or Excel file containing economic indicators"),
    country: str = Query("United States", description="Country for the data"),
    overwrite: bool = Query(False, description="Overwrite existing indicators with same name")
):
    """
    Upload economic indicators from CSV or Excel file.

    **Supported Formats**: .csv, .xlsx, .xls

    **Required Columns** (flexible names):
    - indicator / indicator_name / name
    - category / type / group
    - value / last_value / current
    - unit / units / measurement

    **Optional Columns**:
    - previous / previous_value
    - date / period / timestamp
    - highest / highest_value
    - lowest / lowest_value

    **Example CSV**:
    ```
    indicator,category,value,unit,previous
    GDP Growth,gdp,2.5,%,2.3
    Unemployment Rate,labour,3.8,%,3.9
    ```

    Returns summary of import operation including:
    - Number of indicators parsed
    - Number successfully saved
    - Validation errors
    - Duplicate indicators
    """
    try:
        from app.services.file_parser_service import FileParserService
        from app.database.country_database_manager import country_db_manager
        from app.models.economics import EconomicIndicator
        from sqlalchemy.exc import IntegrityError
        import logging

        logger = logging.getLogger(__name__)

        # Validate file type
        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="No filename provided"
            )

        # Parse the file
        logger.info(f"Parsing uploaded file: {file.filename}")
        indicators = FileParserService.parse_file(file)

        if not indicators:
            raise HTTPException(
                status_code=400,
                detail="No valid indicators found in file"
            )

        # Validate indicators
        validation_result = FileParserService.validate_indicators(indicators)
        if not validation_result["valid"]:
            return {
                "success": False,
                "file_name": file.filename,
                "indicators_parsed": len(indicators),
                "validation_errors": validation_result["errors"],
                "message": "File contains validation errors"
            }

        # Get database session
        country_slug = "united-states" if country == "United States" else country.lower().replace(" ", "-")
        db = country_db_manager.get_session(country_slug)

        saved_count = 0
        updated_count = 0
        skipped_count = 0
        errors = []

        try:
            for ind_data in indicators:
                try:
                    # Check if indicator already exists
                    existing = db.query(EconomicIndicator).filter(
                        EconomicIndicator.indicator_name == ind_data["indicator_name"]
                    ).first()

                    if existing:
                        if overwrite:
                            # Update existing indicator
                            for key, value in ind_data.items():
                                if key != "indicator_name" and value is not None:
                                    setattr(existing, key, value)
                            updated_count += 1
                        else:
                            skipped_count += 1
                            continue
                    else:
                        # Create new indicator
                        indicator = EconomicIndicator(**ind_data)
                        db.add(indicator)
                        saved_count += 1

                    db.commit()

                except IntegrityError as e:
                    db.rollback()
                    errors.append(f"Duplicate indicator: {ind_data.get('indicator_name', 'Unknown')}")
                    skipped_count += 1
                except Exception as e:
                    db.rollback()
                    errors.append(f"Error saving {ind_data.get('indicator_name', 'Unknown')}: {str(e)}")
                    logger.error(f"Error saving indicator: {e}")

            # Clear cache after successful import
            _usa_economics_cache.clear()

            return {
                "success": True,
                "file_name": file.filename,
                "indicators_parsed": len(indicators),
                "indicators_saved": saved_count,
                "indicators_updated": updated_count,
                "indicators_skipped": skipped_count,
                "errors": errors,
                "message": f"Successfully imported {saved_count} new indicators, updated {updated_count}, skipped {skipped_count}"
            }

        finally:
            db.close()

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading economic data: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload economic data: {str(e)}"
        )


@router.get(
    "/data/usa-economics/template",
    summary="Download template file for data import",
    description="Download CSV or Excel template file with correct column structure for importing data"
)
async def download_import_template(
    format: str = Query("csv", regex="^(csv|excel)$", description="Template format: csv or excel")
):
    """
    Download template file for importing economic data.

    **Formats**:
    - csv: Comma-separated values file
    - excel: Excel .xlsx file

    **Template includes**:
    - Column headers with examples
    - Sample data rows
    - Comments explaining each field

    Returns file download.
    """
    try:
        from app.services.file_parser_service import FileParserService

        # Generate template
        template_content = FileParserService.export_template(format)

        # Prepare response
        filename = f"economic_indicators_template.{format if format == 'csv' else 'xlsx'}"
        media_type = "text/csv" if format == "csv" else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        return StreamingResponse(
            io.BytesIO(template_content),
            media_type=media_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate template: {str(e)}"
        )


# ========================================
# GEOGRAPHIC & MARKET DATA ENDPOINTS
# ========================================

@router.get("/data/geographic-indicators")
async def get_geographic_indicators(
    geography: Optional[str] = Query(None, description="Geography name (e.g., 'Atlanta MSA', 'Manhattan')"),
    geography_type: Optional[str] = Query(None, description="Geography type (Metro, Borough, County)"),
    indicator_name: Optional[str] = Query(None, description="Indicator name filter"),
    start_date: Optional[date] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date (YYYY-MM-DD)"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """
    Get geographic economic indicators for metro areas, boroughs, and counties.

    **Data includes:**
    - Metro-level economic data (employment, GDP, income, education)
    - US National mortgage rates (2020-2024 monthly data)
    - Time-series data with period types (annual, monthly, quarterly)

    **Available Geographies:**
    - US National
    - Metro areas (Atlanta MSA, NYC, Miami, etc.)
    - Boroughs (Manhattan, Brooklyn, etc.)

    **Indicators include:**
    - Employment metrics (employment_total, unemployment_rate)
    - Income and GDP (gdp_per_capita, income_growth_rate_yoy)
    - Education (education_bachelor_degree_pct)
    - Housing (home_price_appreciation_yoy)
    - Financial markets (mortgage_30yr, mortgage_15yr, arm_5_1)
    """
    try:
        from app.scripts.import_market_intelligence_csv import GeographicEconomicIndicator

        query = db.query(GeographicEconomicIndicator)

        # Apply filters
        if geography:
            query = query.filter(GeographicEconomicIndicator.geography.ilike(f"%{geography}%"))
        if geography_type:
            query = query.filter(GeographicEconomicIndicator.geography_type == geography_type)
        if indicator_name:
            query = query.filter(GeographicEconomicIndicator.indicator_name.ilike(f"%{indicator_name}%"))
        if start_date:
            query = query.filter(GeographicEconomicIndicator.period >= start_date)
        if end_date:
            query = query.filter(GeographicEconomicIndicator.period <= end_date)

        # Order by most recent first
        query = query.order_by(GeographicEconomicIndicator.period.desc())

        # Apply limit
        results = query.limit(limit).all()

        # Get summary statistics
        total_count = db.query(GeographicEconomicIndicator).count()
        unique_geographies = db.query(GeographicEconomicIndicator.geography).distinct().count()
        unique_indicators = db.query(GeographicEconomicIndicator.indicator_name).distinct().count()

        return {
            "success": True,
            "total_records": total_count,
            "unique_geographies": unique_geographies,
            "unique_indicators": unique_indicators,
            "results_count": len(results),
            "data": [
                {
                    "id": r.id,
                    "geography": r.geography,
                    "geography_type": r.geography_type,
                    "indicator_name": r.indicator_name,
                    "indicator_value": float(r.indicator_value) if r.indicator_value else None,
                    "indicator_unit": r.indicator_unit,
                    "period": r.period.isoformat() if r.period else None,
                    "period_type": r.period_type,
                    "data_source": r.data_source,
                    "notes": r.notes,
                }
                for r in results
            ]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve geographic indicators: {str(e)}"
        )


@router.get("/data/geographic-indicators/timeseries")
async def get_geographic_timeseries(
    geography: str = Query(..., description="Geography name"),
    indicator_name: str = Query(..., description="Indicator name"),
    db: Session = Depends(get_db)
):
    """
    Get time-series data for a specific geography and indicator.

    **Use Cases:**
    - Trend charts showing indicator changes over time
    - Year-over-year comparisons
    - Seasonal analysis

    **Example:**
    - Geography: "Atlanta MSA"
    - Indicator: "employment_total"
    - Returns: All data points ordered by date
    """
    try:
        from app.scripts.import_market_intelligence_csv import GeographicEconomicIndicator

        results = db.query(GeographicEconomicIndicator).filter(
            GeographicEconomicIndicator.geography == geography,
            GeographicEconomicIndicator.indicator_name == indicator_name
        ).order_by(GeographicEconomicIndicator.period).all()

        if not results:
            raise HTTPException(
                status_code=404,
                detail=f"No data found for {geography} - {indicator_name}"
            )

        # Calculate trends
        values = [float(r.indicator_value) for r in results if r.indicator_value]
        trend_data = {
            "min": min(values) if values else None,
            "max": max(values) if values else None,
            "avg": sum(values) / len(values) if values else None,
            "latest": values[-1] if values else None,
            "first": values[0] if values else None,
            "total_change": values[-1] - values[0] if len(values) > 1 else 0,
            "total_change_percent": ((values[-1] - values[0]) / values[0] * 100) if len(values) > 1 and values[0] != 0 else 0,
        }

        return {
            "success": True,
            "geography": geography,
            "indicator_name": indicator_name,
            "unit": results[0].indicator_unit if results else None,
            "period_type": results[0].period_type if results else None,
            "data_points": len(results),
            "trends": trend_data,
            "data": [
                {
                    "period": r.period.isoformat() if r.period else None,
                    "value": float(r.indicator_value) if r.indicator_value else None,
                    "notes": r.notes,
                }
                for r in results
            ]
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve time-series data: {str(e)}"
        )


@router.get("/data/real-estate-market")
async def get_real_estate_market_data(
    market_name: Optional[str] = Query(None, description="Market name (e.g., 'National', 'NYC', 'Miami')"),
    submarket_name: Optional[str] = Query(None, description="Submarket name"),
    property_type: Optional[str] = Query(None, description="Property type (multifamily, office, retail, industrial)"),
    property_class: Optional[str] = Query(None, description="Property class (A, B, C)"),
    metric_name: Optional[str] = Query(None, description="Metric name filter"),
    start_date: Optional[date] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date (YYYY-MM-DD)"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """
    Get real estate market data including cap rates, occupancy, rents, and transaction volumes.

    **Markets covered:**
    - National
    - NYC (Manhattan, Brooklyn, Queens, Bronx, Staten Island)
    - Miami
    - Chicago
    - Los Angeles
    - And more...

    **Property Types:**
    - multifamily
    - office
    - retail
    - industrial

    **Key Metrics:**
    - occupancy_rate, vacancy_rate
    - rent_growth, rent_per_sf, rent_per_unit
    - cap_rate (capitalization rate)
    - opex_per_unit, insurance_per_unit
    - transaction_volume
    - units_under_construction
    """
    try:
        from app.scripts.import_market_intelligence_csv import RealEstateMarketData

        query = db.query(RealEstateMarketData)

        # Apply filters
        if market_name:
            query = query.filter(RealEstateMarketData.market_name.ilike(f"%{market_name}%"))
        if submarket_name:
            query = query.filter(RealEstateMarketData.submarket_name.ilike(f"%{submarket_name}%"))
        if property_type:
            query = query.filter(RealEstateMarketData.property_type == property_type)
        if property_class:
            query = query.filter(RealEstateMarketData.property_class == property_class)
        if metric_name:
            query = query.filter(RealEstateMarketData.metric_name.ilike(f"%{metric_name}%"))
        if start_date:
            query = query.filter(RealEstateMarketData.period >= start_date)
        if end_date:
            query = query.filter(RealEstateMarketData.period <= end_date)

        # Order by most recent first
        query = query.order_by(RealEstateMarketData.period.desc())

        # Apply limit
        results = query.limit(limit).all()

        # Get summary statistics
        total_count = db.query(RealEstateMarketData).count()
        unique_markets = db.query(RealEstateMarketData.market_name).distinct().count()
        unique_property_types = db.query(RealEstateMarketData.property_type).distinct().count()

        return {
            "success": True,
            "total_records": total_count,
            "unique_markets": unique_markets,
            "unique_property_types": unique_property_types,
            "results_count": len(results),
            "data": [
                {
                    "id": r.id,
                    "market_name": r.market_name,
                    "submarket_name": r.submarket_name,
                    "property_type": r.property_type,
                    "property_class": r.property_class,
                    "metric_name": r.metric_name,
                    "metric_value": float(r.metric_value) if r.metric_value else None,
                    "metric_unit": r.metric_unit,
                    "period": r.period.isoformat() if r.period else None,
                    "data_source": r.data_source,
                    "confidence_level": r.confidence_level,
                    "notes": r.notes,
                }
                for r in results
            ]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve real estate market data: {str(e)}"
        )


@router.get("/data/comparable-transactions")
async def get_comparable_transactions(
    city: Optional[str] = Query(None, description="City name (e.g., 'Manhattan', 'Miami', 'Brooklyn')"),
    state: Optional[str] = Query(None, description="State code (e.g., 'NY', 'FL')"),
    property_type: Optional[str] = Query(None, description="Property type (multifamily, office, etc.)"),
    property_class: Optional[str] = Query(None, description="Property class (A, B, C)"),
    deal_type: Optional[str] = Query(None, description="Deal type (Arms Length, Portfolio, Foreclosure, etc.)"),
    min_sale_price: Optional[float] = Query(None, description="Minimum sale price"),
    max_sale_price: Optional[float] = Query(None, description="Maximum sale price"),
    min_cap_rate: Optional[float] = Query(None, description="Minimum cap rate"),
    max_cap_rate: Optional[float] = Query(None, description="Maximum cap rate"),
    start_date: Optional[date] = Query(None, description="Start sale date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End sale date (YYYY-MM-DD)"),
    limit: int = Query(50, ge=1, le=500, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """
    Get comparable property sales transactions.

    **Markets covered:**
    - Manhattan, Brooklyn, Queens, Bronx, Staten Island (NYC)
    - Miami, Fort Lauderdale, West Palm Beach (FL)
    - Chicago, Coral Gables

    **Data includes:**
    - Sale price and date
    - Price per unit, price per SF
    - Cap rates
    - Property details (units, square footage, year built)
    - Buyer and seller information
    - Deal type (Arms Length, Portfolio, Foreclosure, etc.)

    **Transaction Types:**
    - Arms Length: Standard market transactions
    - Portfolio: Multi-property deals
    - Foreclosure: Distressed sales
    - Development Site: Land/redevelopment opportunities
    """
    try:
        from app.scripts.import_market_intelligence_csv import ComparableTransaction

        query = db.query(ComparableTransaction)

        # Apply filters
        if city:
            query = query.filter(ComparableTransaction.city.ilike(f"%{city}%"))
        if state:
            query = query.filter(ComparableTransaction.state == state)
        if property_type:
            query = query.filter(ComparableTransaction.property_type == property_type)
        if property_class:
            query = query.filter(ComparableTransaction.property_class == property_class)
        if deal_type:
            query = query.filter(ComparableTransaction.deal_type == deal_type)
        if min_sale_price:
            query = query.filter(ComparableTransaction.sale_price >= min_sale_price)
        if max_sale_price:
            query = query.filter(ComparableTransaction.sale_price <= max_sale_price)
        if min_cap_rate:
            query = query.filter(ComparableTransaction.cap_rate >= min_cap_rate)
        if max_cap_rate:
            query = query.filter(ComparableTransaction.cap_rate <= max_cap_rate)
        if start_date:
            query = query.filter(ComparableTransaction.sale_date >= start_date)
        if end_date:
            query = query.filter(ComparableTransaction.sale_date <= end_date)

        # Order by most recent sales first
        query = query.order_by(ComparableTransaction.sale_date.desc())

        # Apply limit
        results = query.limit(limit).all()

        # Get summary statistics
        total_count = db.query(ComparableTransaction).count()
        unique_cities = db.query(ComparableTransaction.city).distinct().count()

        return {
            "success": True,
            "total_transactions": total_count,
            "unique_cities": unique_cities,
            "results_count": len(results),
            "data": [
                {
                    "id": r.id,
                    "address": r.address,
                    "city": r.city,
                    "submarket": r.submarket,
                    "state": r.state,
                    "property_type": r.property_type,
                    "property_class": r.property_class,
                    "sale_date": r.sale_date.isoformat() if r.sale_date else None,
                    "sale_price": float(r.sale_price) if r.sale_price else None,
                    "price_per_unit": float(r.price_per_unit) if r.price_per_unit else None,
                    "price_per_sf": float(r.price_per_sf) if r.price_per_sf else None,
                    "cap_rate": float(r.cap_rate) if r.cap_rate else None,
                    "units": r.units,
                    "total_sf": r.total_sf,
                    "year_built": r.year_built,
                    "buyer": r.buyer,
                    "seller": r.seller,
                    "financing_type": r.financing_type,
                    "occupancy_at_sale": float(r.occupancy_at_sale) if r.occupancy_at_sale else None,
                    "deal_type": r.deal_type,
                    "data_source": r.data_source,
                    "notes": r.notes,
                    # New expanded fields
                    "zip_code": r.zip_code if hasattr(r, 'zip_code') else None,
                    "lot_size_sf": r.lot_size_sf if hasattr(r, 'lot_size_sf') else None,
                    "year_renovated": r.year_renovated if hasattr(r, 'year_renovated') else None,
                    "num_buildings": r.num_buildings if hasattr(r, 'num_buildings') else None,
                    "num_floors": r.num_floors if hasattr(r, 'num_floors') else None,
                    "parking_spaces": r.parking_spaces if hasattr(r, 'parking_spaces') else None,
                    "noi": float(r.noi) if hasattr(r, 'noi') and r.noi else None,
                    "gross_potential_rent": float(r.gross_potential_rent) if hasattr(r, 'gross_potential_rent') and r.gross_potential_rent else None,
                    "inplace_vs_market_rent_pct": float(r.inplace_vs_market_rent_pct) if hasattr(r, 'inplace_vs_market_rent_pct') and r.inplace_vs_market_rent_pct else None,
                    "buyer_type": r.buyer_type if hasattr(r, 'buyer_type') else None,
                    "seller_type": r.seller_type if hasattr(r, 'seller_type') else None,
                    "broker": r.broker if hasattr(r, 'broker') else None,
                    "ltv": float(r.ltv) if hasattr(r, 'ltv') and r.ltv else None,
                    "lender": r.lender if hasattr(r, 'lender') else None,
                    "interest_rate": float(r.interest_rate) if hasattr(r, 'interest_rate') and r.interest_rate else None,
                    "special_conditions": r.special_conditions if hasattr(r, 'special_conditions') else None,
                }
                for r in results
            ]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve comparable transactions: {str(e)}"
        )


# ========================================
# ADVANCED QUERY ENDPOINTS FOR UPLOADED DATA
# ========================================

@router.get("/data/hot-zones")
async def get_hot_zones(
    market_name: Optional[str] = Query(None, description="Filter by market name"),
    neighborhood: Optional[str] = Query(None, description="Filter by neighborhood"),
    metric_category: Optional[str] = Query(None, description="Filter by metric category"),
    min_rank: Optional[int] = Query(None, description="Minimum hot zone rank"),
    max_rank: Optional[int] = Query(None, description="Maximum hot zone rank"),
    limit: int = Query(1000, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """
    Get hot zones and emerging markets data.

    **Markets covered:**
    - New York Metro (NYC boroughs and submarkets)
    - Miami Metro
    - Other major U.S. markets

    **Metric Categories:**
    - Price & Rent Momentum
    - Population Growth
    - Employment Growth
    - Investment Activity
    - Development Pipeline
    - Rental Demand

    Returns emerging neighborhoods ranked by investment potential.
    """
    try:
        from app.scripts.import_market_intelligence_csv import HotZoneMarket

        query = db.query(HotZoneMarket)

        # Apply filters
        if market_name:
            query = query.filter(HotZoneMarket.market_name.ilike(f"%{market_name}%"))
        if neighborhood:
            query = query.filter(HotZoneMarket.neighborhood_name.ilike(f"%{neighborhood}%"))
        if metric_category:
            query = query.filter(HotZoneMarket.metric_category.ilike(f"%{metric_category}%"))
        if min_rank:
            query = query.filter(HotZoneMarket.hot_zone_rank >= min_rank)
        if max_rank:
            query = query.filter(HotZoneMarket.hot_zone_rank <= max_rank)

        # Order by rank (best opportunities first)
        query = query.order_by(HotZoneMarket.hot_zone_rank.asc())

        # Apply limit
        results = query.limit(limit).all()

        # Get summary statistics
        total_count = db.query(HotZoneMarket).count()
        unique_markets = db.query(HotZoneMarket.market_name).distinct().count()
        unique_neighborhoods = db.query(HotZoneMarket.neighborhood_name).distinct().count()

        return {
            "success": True,
            "total_hot_zones": total_count,
            "unique_markets": unique_markets,
            "unique_neighborhoods": unique_neighborhoods,
            "results_count": len(results),
            "data": [
                {
                    "id": r.id,
                    "market_name": r.market_name,
                    "neighborhood_name": r.neighborhood_name,
                    "hot_zone_rank": r.hot_zone_rank,
                    "metric_category": r.metric_category,
                    "metric_name": r.metric_name,
                    "metric_value": float(r.metric_value) if r.metric_value else None,
                    "metric_unit": r.metric_unit,
                    "period": r.period.isoformat() if r.period else None,
                    "comparison_to_city_average": r.comparison_to_city_average,
                    "data_source": r.data_source,
                    "notes": r.notes,
                }
                for r in results
            ]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve hot zones: {str(e)}"
        )


@router.get("/data/neighborhood-scores")
async def get_neighborhood_scores(
    market_name: Optional[str] = Query(None, description="Filter by market name"),
    neighborhood: Optional[str] = Query(None, description="Filter by neighborhood"),
    score_category: Optional[str] = Query(None, description="Filter by score category"),
    min_score: Optional[float] = Query(None, description="Minimum score value"),
    max_score: Optional[float] = Query(None, description="Maximum score value"),
    limit: int = Query(1000, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """
    Get neighborhood scoring and ranking analysis.

    **Score Categories:**
    - Accessibility Score (walkability, transit)
    - School Quality Score
    - Safety Score
    - Amenity Score (restaurants, parks, retail)
    - Investment Potential Score
    - Livability Score
    - Job Accessibility Score

    Scores range from 0-100, with higher scores indicating better quality.
    """
    try:
        from app.scripts.import_market_intelligence_csv import NeighborhoodScore

        query = db.query(NeighborhoodScore)

        # Apply filters
        if market_name:
            query = query.filter(NeighborhoodScore.market_name.ilike(f"%{market_name}%"))
        if neighborhood:
            query = query.filter(NeighborhoodScore.neighborhood_name.ilike(f"%{neighborhood}%"))
        if score_category:
            query = query.filter(NeighborhoodScore.score_category.ilike(f"%{score_category}%"))
        if min_score:
            query = query.filter(NeighborhoodScore.score_value >= min_score)
        if max_score:
            query = query.filter(NeighborhoodScore.score_value <= max_score)

        # Order by score (highest first)
        query = query.order_by(NeighborhoodScore.score_value.desc())

        # Apply limit
        results = query.limit(limit).all()

        # Get summary statistics
        total_count = db.query(NeighborhoodScore).count()
        unique_markets = db.query(NeighborhoodScore.market_name).distinct().count()
        unique_neighborhoods = db.query(NeighborhoodScore.neighborhood_name).distinct().count()

        return {
            "success": True,
            "total_scores": total_count,
            "unique_markets": unique_markets,
            "unique_neighborhoods": unique_neighborhoods,
            "results_count": len(results),
            "data": [
                {
                    "id": r.id,
                    "market_name": r.market_name,
                    "neighborhood_name": r.neighborhood_name,
                    "score_category": r.score_category,
                    "score_value": float(r.score_value) if r.score_value else None,
                    "rank_within_market": r.rank_within_market,
                    "rank_nationally": r.rank_nationally,
                    "period": r.period.isoformat() if r.period else None,
                    "data_source": r.data_source,
                    "notes": r.notes,
                }
                for r in results
            ]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve neighborhood scores: {str(e)}"
        )


@router.get("/analysis/comparable-transactions/insights")
async def get_transaction_insights(
    city: Optional[str] = Query(None, description="Filter by city"),
    state: Optional[str] = Query(None, description="Filter by state"),
    property_type: Optional[str] = Query(None, description="Filter by property type"),
    buyer_type: Optional[str] = Query(None, description="Filter by buyer type"),
    start_date: Optional[date] = Query(None, description="Filter sales from this date"),
    end_date: Optional[date] = Query(None, description="Filter sales until this date"),
    db: Session = Depends(get_db)
):
    """
    Get advanced insights and analytics for comparable transactions.

    **Insights include:**
    - Average sale price, price/unit, price/SF, cap rate
    - Price trends over time
    - Buyer type distribution
    - Seller type distribution
    - Financing mix
    - Deal type breakdown
    - Market velocity metrics

    Returns aggregated statistics and trends to support investment decisions.
    """
    try:
        from app.scripts.import_market_intelligence_csv import ComparableTransaction
        from sqlalchemy import func, extract

        query = db.query(ComparableTransaction)

        # Apply filters
        if city:
            query = query.filter(ComparableTransaction.city.ilike(f"%{city}%"))
        if state:
            query = query.filter(ComparableTransaction.state == state)
        if property_type:
            query = query.filter(ComparableTransaction.property_type == property_type)
        if buyer_type:
            query = query.filter(ComparableTransaction.buyer_type.ilike(f"%{buyer_type}%"))
        if start_date:
            query = query.filter(ComparableTransaction.sale_date >= start_date)
        if end_date:
            query = query.filter(ComparableTransaction.sale_date <= end_date)

        transactions = query.all()

        if not transactions:
            return {
                "success": True,
                "message": "No transactions found matching the criteria",
                "insights": None
            }

        # Calculate aggregated metrics
        total_volume = sum(float(t.sale_price) for t in transactions if t.sale_price)
        avg_price = total_volume / len([t for t in transactions if t.sale_price])

        avg_price_per_unit = sum(float(t.price_per_unit) for t in transactions if t.price_per_unit) / len([t for t in transactions if t.price_per_unit]) if any(t.price_per_unit for t in transactions) else None

        avg_price_per_sf = sum(float(t.price_per_sf) for t in transactions if t.price_per_sf) / len([t for t in transactions if t.price_per_sf]) if any(t.price_per_sf for t in transactions) else None

        avg_cap_rate = sum(float(t.cap_rate) for t in transactions if t.cap_rate) / len([t for t in transactions if t.cap_rate]) if any(t.cap_rate for t in transactions) else None

        # Buyer type distribution
        buyer_types = {}
        for t in transactions:
            if hasattr(t, 'buyer_type') and t.buyer_type:
                buyer_types[t.buyer_type] = buyer_types.get(t.buyer_type, 0) + 1

        # Seller type distribution
        seller_types = {}
        for t in transactions:
            if hasattr(t, 'seller_type') and t.seller_type:
                seller_types[t.seller_type] = seller_types.get(t.seller_type, 0) + 1

        # Deal type distribution
        deal_types = {}
        for t in transactions:
            if t.deal_type:
                deal_types[t.deal_type] = deal_types.get(t.deal_type, 0) + 1

        # Financing type distribution
        financing_types = {}
        for t in transactions:
            if t.financing_type:
                financing_types[t.financing_type] = financing_types.get(t.financing_type, 0) + 1

        # Monthly trend
        monthly_volume = {}
        for t in transactions:
            if t.sale_date:
                month_key = t.sale_date.strftime('%Y-%m')
                if month_key not in monthly_volume:
                    monthly_volume[month_key] = {"count": 0, "total_volume": 0}
                monthly_volume[month_key]["count"] += 1
                if t.sale_price:
                    monthly_volume[month_key]["total_volume"] += float(t.sale_price)

        return {
            "success": True,
            "total_transactions": len(transactions),
            "insights": {
                "pricing": {
                    "total_volume": round(total_volume, 2),
                    "average_sale_price": round(avg_price, 2),
                    "average_price_per_unit": round(avg_price_per_unit, 2) if avg_price_per_unit else None,
                    "average_price_per_sf": round(avg_price_per_sf, 2) if avg_price_per_sf else None,
                    "average_cap_rate": round(avg_cap_rate * 100, 2) if avg_cap_rate else None,
                },
                "market_participants": {
                    "buyer_types": buyer_types,
                    "seller_types": seller_types,
                },
                "transaction_characteristics": {
                    "deal_types": deal_types,
                    "financing_types": financing_types,
                },
                "trends": {
                    "monthly_volume": [
                        {
                            "month": month,
                            "transaction_count": data["count"],
                            "total_volume": round(data["total_volume"], 2),
                            "avg_price": round(data["total_volume"] / data["count"], 2) if data["count"] > 0 else 0
                        }
                        for month, data in sorted(monthly_volume.items())
                    ]
                }
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate transaction insights: {str(e)}"
        )


@router.get("/analysis/market-intelligence/trends")
async def get_market_trends(
    geography: Optional[str] = Query(None, description="Filter by geography"),
    indicator_name: Optional[str] = Query(None, description="Filter by indicator"),
    start_period: Optional[date] = Query(None, description="Start date for trend analysis"),
    end_period: Optional[date] = Query(None, description="End date for trend analysis"),
    db: Session = Depends(get_db)
):
    """
    Analyze trends in geographic and economic indicators over time.

    **Trend Metrics:**
    - Growth rates (YoY, compound annual growth)
    - Volatility measures
    - Correlation analysis
    - Leading/lagging indicator identification
    - Anomaly detection

    Helps identify investment opportunities and risk factors.
    """
    try:
        from app.scripts.import_market_intelligence_csv import GeographicEconomicIndicator
        from sqlalchemy import func

        query = db.query(GeographicEconomicIndicator)

        # Apply filters
        if geography:
            query = query.filter(GeographicEconomicIndicator.geography.ilike(f"%{geography}%"))
        if indicator_name:
            query = query.filter(GeographicEconomicIndicator.indicator_name.ilike(f"%{indicator_name}%"))
        if start_period:
            query = query.filter(GeographicEconomicIndicator.period >= start_period)
        if end_period:
            query = query.filter(GeographicEconomicIndicator.period <= end_period)

        # Order by period
        query = query.order_by(GeographicEconomicIndicator.period.asc())

        indicators = query.all()

        if not indicators:
            return {
                "success": True,
                "message": "No indicators found matching the criteria",
                "trends": None
            }

        # Group by geography and indicator
        trends_by_indicator = {}
        for ind in indicators:
            key = f"{ind.geography}_{ind.indicator_name}"
            if key not in trends_by_indicator:
                trends_by_indicator[key] = {
                    "geography": ind.geography,
                    "indicator_name": ind.indicator_name,
                    "indicator_unit": ind.indicator_unit,
                    "data_points": []
                }

            trends_by_indicator[key]["data_points"].append({
                "period": ind.period.isoformat() if ind.period else None,
                "value": float(ind.indicator_value) if ind.indicator_value else None,
            })

        # Calculate growth rates for each indicator
        for key, trend in trends_by_indicator.items():
            data_points = trend["data_points"]
            if len(data_points) >= 2:
                # Calculate YoY growth if we have at least 2 points
                first_value = data_points[0]["value"]
                last_value = data_points[-1]["value"]

                if first_value and last_value and first_value != 0:
                    total_growth = ((last_value - first_value) / first_value) * 100
                    trend["total_growth_pct"] = round(total_growth, 2)

                    # Calculate CAGR if we have date range
                    if data_points[0]["period"] and data_points[-1]["period"]:
                        from datetime import datetime
                        start = datetime.fromisoformat(data_points[0]["period"])
                        end = datetime.fromisoformat(data_points[-1]["period"])
                        years = (end - start).days / 365.25

                        if years > 0:
                            cagr = (((last_value / first_value) ** (1 / years)) - 1) * 100
                            trend["cagr_pct"] = round(cagr, 2)

        return {
            "success": True,
            "total_indicators": len(indicators),
            "unique_geographies": len(set(i.geography for i in indicators)),
            "unique_indicators": len(set(i.indicator_name for i in indicators)),
            "trends": list(trends_by_indicator.values())
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze market trends: {str(e)}"
        )


@router.post("/data/deduplicate")
async def deduplicate_data(
    table: str = Query(..., description="Table to deduplicate: 'transactions', 'hot_zones', or 'neighborhood_scores'"),
    dry_run: bool = Query(True, description="If true, only report duplicates without removing them"),
    db: Session = Depends(get_db)
):
    """
    Identify and optionally remove duplicate records from uploaded data.

    **Deduplication Logic:**
    - Comparable Transactions: Same address, city, state, sale_date, sale_price
    - Hot Zones: Same market_name, neighborhood_name, metric_category, metric_name, period
    - Neighborhood Scores: Same market_name, neighborhood_name, score_category, period

    **Dry Run Mode (default):**
    - Returns list of duplicates without deleting
    - Safe for exploratory analysis

    **Live Mode (dry_run=false):**
    - Keeps the first occurrence of each duplicate group
    - Deletes all other occurrences
    - Returns count of deleted records
    """
    try:
        from sqlalchemy import func

        if table == "transactions":
            from app.scripts.import_market_intelligence_csv import ComparableTransaction
            Model = ComparableTransaction
            group_fields = [
                ComparableTransaction.address,
                ComparableTransaction.city,
                ComparableTransaction.state,
                ComparableTransaction.sale_date,
                ComparableTransaction.sale_price
            ]
        elif table == "hot_zones":
            from app.scripts.import_market_intelligence_csv import HotZoneMarket
            Model = HotZoneMarket
            group_fields = [
                HotZoneMarket.market_name,
                HotZoneMarket.neighborhood_name,
                HotZoneMarket.metric_category,
                HotZoneMarket.metric_name,
                HotZoneMarket.period
            ]
        elif table == "neighborhood_scores":
            from app.scripts.import_market_intelligence_csv import NeighborhoodScore
            Model = NeighborhoodScore
            group_fields = [
                NeighborhoodScore.market_name,
                NeighborhoodScore.neighborhood_name,
                NeighborhoodScore.score_category,
                NeighborhoodScore.period
            ]
        else:
            raise HTTPException(
                status_code=400,
                detail="Invalid table. Must be 'transactions', 'hot_zones', or 'neighborhood_scores'"
            )

        # Find duplicate groups
        duplicate_groups = (
            db.query(*group_fields, func.count(Model.id).label('count'), func.array_agg(Model.id).label('ids'))
            .group_by(*group_fields)
            .having(func.count(Model.id) > 1)
            .all()
        )

        total_duplicates = sum(g.count - 1 for g in duplicate_groups)

        if dry_run:
            return {
                "success": True,
                "dry_run": True,
                "table": table,
                "duplicate_groups_found": len(duplicate_groups),
                "total_duplicate_records": total_duplicates,
                "duplicates": [
                    {
                        "count": g.count,
                        "ids": g.ids,
                        "key": dict(zip([f.name for f in group_fields], g[:-2]))
                    }
                    for g in duplicate_groups
                ]
            }
        else:
            # Delete duplicates (keep first, delete rest)
            deleted_count = 0
            for group in duplicate_groups:
                ids_to_delete = group.ids[1:]  # Keep first, delete rest
                db.query(Model).filter(Model.id.in_(ids_to_delete)).delete(synchronize_session=False)
                deleted_count += len(ids_to_delete)

            db.commit()

            return {
                "success": True,
                "dry_run": False,
                "table": table,
                "duplicate_groups_found": len(duplicate_groups),
                "records_deleted": deleted_count
            }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to deduplicate data: {str(e)}"
        )


@router.get("/analysis/comparable-analysis")
async def find_comparables(
    target_city: str = Query(..., description="Target property city"),
    target_state: str = Query(..., description="Target property state"),
    target_property_type: str = Query(..., description="Target property type"),
    target_units: Optional[int] = Query(None, description="Target property units"),
    target_sf: Optional[int] = Query(None, description="Target property square footage"),
    target_year_built: Optional[int] = Query(None, description="Target property year built"),
    units_tolerance: float = Query(0.25, description="Units matching tolerance (0.25 = ±25%)"),
    sf_tolerance: float = Query(0.25, description="Square footage matching tolerance"),
    year_tolerance: int = Query(10, description="Year built tolerance (±years)"),
    max_results: int = Query(10, description="Maximum number of comparables to return"),
    db: Session = Depends(get_db)
):
    """
    Find comparable property transactions for a target property.

    **Matching Criteria:**
    - Same city, state, and property type (required)
    - Similar units (within tolerance %)
    - Similar square footage (within tolerance %)
    - Similar year built (within tolerance years)
    - Recent transactions preferred

    **Returns:**
    - Ranked list of comparable transactions
    - Similarity score (0-100)
    - Suggested valuation range based on comps
    - Market insights

    Essential tool for property valuation and underwriting.
    """
    try:
        from app.scripts.import_market_intelligence_csv import ComparableTransaction

        # Query base filters (exact matches)
        query = db.query(ComparableTransaction).filter(
            ComparableTransaction.city.ilike(f"%{target_city}%"),
            ComparableTransaction.state == target_state,
            ComparableTransaction.property_type == target_property_type
        )

        # Apply fuzzy matching filters if provided
        if target_units:
            min_units = target_units * (1 - units_tolerance)
            max_units = target_units * (1 + units_tolerance)
            query = query.filter(
                ComparableTransaction.units >= min_units,
                ComparableTransaction.units <= max_units
            )

        if target_sf:
            min_sf = target_sf * (1 - sf_tolerance)
            max_sf = target_sf * (1 + sf_tolerance)
            query = query.filter(
                ComparableTransaction.total_sf >= min_sf,
                ComparableTransaction.total_sf <= max_sf
            )

        if target_year_built:
            min_year = target_year_built - year_tolerance
            max_year = target_year_built + year_tolerance
            query = query.filter(
                ComparableTransaction.year_built >= min_year,
                ComparableTransaction.year_built <= max_year
            )

        # Order by most recent sales
        query = query.order_by(ComparableTransaction.sale_date.desc())

        comparables = query.limit(max_results).all()

        if not comparables:
            return {
                "success": True,
                "message": "No comparable transactions found",
                "comparables": []
            }

        # Calculate similarity scores and valuation metrics
        results = []
        for comp in comparables:
            similarity_score = 100  # Start at perfect match

            # Reduce score based on differences
            if target_units and comp.units:
                units_diff = abs(comp.units - target_units) / target_units
                similarity_score -= min(units_diff * 50, 20)

            if target_sf and comp.total_sf:
                sf_diff = abs(comp.total_sf - target_sf) / target_sf
                similarity_score -= min(sf_diff * 50, 20)

            if target_year_built and comp.year_built:
                year_diff = abs(comp.year_built - target_year_built) / year_tolerance
                similarity_score -= min(year_diff * 10, 15)

            results.append({
                "similarity_score": round(max(similarity_score, 0), 1),
                "transaction": {
                    "id": comp.id,
                    "address": comp.address,
                    "city": comp.city,
                    "state": comp.state,
                    "sale_date": comp.sale_date.isoformat() if comp.sale_date else None,
                    "sale_price": float(comp.sale_price) if comp.sale_price else None,
                    "price_per_unit": float(comp.price_per_unit) if comp.price_per_unit else None,
                    "price_per_sf": float(comp.price_per_sf) if comp.price_per_sf else None,
                    "cap_rate": float(comp.cap_rate) if comp.cap_rate else None,
                    "units": comp.units,
                    "total_sf": comp.total_sf,
                    "year_built": comp.year_built,
                    "noi": float(comp.noi) if hasattr(comp, 'noi') and comp.noi else None,
                    "buyer_type": comp.buyer_type if hasattr(comp, 'buyer_type') else None,
                }
            })

        # Sort by similarity score
        results.sort(key=lambda x: x["similarity_score"], reverse=True)

        # Calculate valuation range
        prices_per_unit = [r["transaction"]["price_per_unit"] for r in results if r["transaction"]["price_per_unit"]]
        prices_per_sf = [r["transaction"]["price_per_sf"] for r in results if r["transaction"]["price_per_sf"]]
        cap_rates = [r["transaction"]["cap_rate"] for r in results if r["transaction"]["cap_rate"]]

        valuation_metrics = {}
        if prices_per_unit:
            valuation_metrics["avg_price_per_unit"] = round(sum(prices_per_unit) / len(prices_per_unit), 2)
            valuation_metrics["price_per_unit_range"] = [round(min(prices_per_unit), 2), round(max(prices_per_unit), 2)]

        if prices_per_sf:
            valuation_metrics["avg_price_per_sf"] = round(sum(prices_per_sf) / len(prices_per_sf), 2)
            valuation_metrics["price_per_sf_range"] = [round(min(prices_per_sf), 2), round(max(prices_per_sf), 2)]

        if cap_rates:
            valuation_metrics["avg_cap_rate"] = round((sum(cap_rates) / len(cap_rates)) * 100, 2)
            valuation_metrics["cap_rate_range"] = [round(min(cap_rates) * 100, 2), round(max(cap_rates) * 100, 2)]

        # Estimate target property value if we have units and/or SF
        estimated_value_range = None
        if target_units and prices_per_unit:
            low = target_units * min(prices_per_unit)
            high = target_units * max(prices_per_unit)
            estimated_value_range = {
                "method": "price_per_unit",
                "low": round(low, 2),
                "high": round(high, 2),
                "mid": round((low + high) / 2, 2)
            }
        elif target_sf and prices_per_sf:
            low = target_sf * min(prices_per_sf)
            high = target_sf * max(prices_per_sf)
            estimated_value_range = {
                "method": "price_per_sf",
                "low": round(low, 2),
                "high": round(high, 2),
                "mid": round((low + high) / 2, 2)
            }

        return {
            "success": True,
            "total_comparables": len(results),
            "comparables": results,
            "valuation_metrics": valuation_metrics,
            "estimated_value_range": estimated_value_range
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to find comparable transactions: {str(e)}"
        )


# ========================================
# ADDITIONAL MARKET INTELLIGENCE ENDPOINTS
# ========================================

@router.get("/data/hot-zones")
async def get_hot_zones(
    market: Optional[str] = Query(None, description="Market name filter"),
    metric_name: Optional[str] = Query(None, description="Metric name filter"),
    start_date: Optional[date] = Query(None, description="Start date"),
    end_date: Optional[date] = Query(None, description="End date"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    use_cache: bool = Query(True, description="Use cached data if available"),
    db: Session = Depends(get_db)
):
    """
    Get hot zone market data showing high-growth and emerging markets.

    **Data includes:**
    - Market growth stages and momentum
    - Investment recommendations
    - Price appreciation metrics
    - Supply/demand dynamics

    **Cache:** Data is cached for 15 minutes for better performance.
    """
    try:
        # Try cache first
        if use_cache:
            cache_key = _make_cache_key("hot_zones", market=market, metric_name=metric_name,
                                        start_date=str(start_date) if start_date else None,
                                        end_date=str(end_date) if end_date else None, limit=limit)
            cached_data = await cache_service.get(cache_key, namespace="market_intelligence", cache_type="real_estate_data")
            if cached_data:
                return {**cached_data, "cached": True}

        from app.scripts.import_market_intelligence_csv import HotZoneMarket

        query = db.query(HotZoneMarket)

        # Apply filters
        if market:
            query = query.filter(HotZoneMarket.market_name.ilike(f"%{market}%"))
        if metric_name:
            query = query.filter(HotZoneMarket.metric_name.ilike(f"%{metric_name}%"))
        if start_date:
            query = query.filter(HotZoneMarket.period >= start_date)
        if end_date:
            query = query.filter(HotZoneMarket.period <= end_date)

        # Order by hot zone rank
        query = query.order_by(HotZoneMarket.hot_zone_rank.asc().nullslast(), HotZoneMarket.period.desc())

        # Apply limit
        results = query.limit(limit).all()

        # Get summary statistics
        total_count = db.query(HotZoneMarket).count()
        unique_markets = db.query(HotZoneMarket.market_name).distinct().count()

        response_data = {
            "success": True,
            "total_records": total_count,
            "unique_markets": unique_markets,
            "results_count": len(results),
            "cached": False,
            "data": [
                {
                    "id": r.id,
                    "market": r.market_name,
                    "neighborhood": r.neighborhood_name,
                    "hot_zone_rank": r.hot_zone_rank,
                    "metric_category": r.metric_category,
                    "metric_name": r.metric_name,
                    "metric_value": float(r.metric_value) if r.metric_value else None,
                    "metric_unit": r.metric_unit,
                    "period": r.period.isoformat() if r.period else None,
                    "comparison_to_city_average": r.comparison_to_city_average,
                    "data_source": r.data_source,
                    "notes": r.notes if hasattr(r, 'notes') else None,
                }
                for r in results
            ]
        }

        # Cache the response
        if use_cache:
            await cache_service.set(cache_key, response_data, namespace="market_intelligence",
                                   cache_type="real_estate_data", ttl=900)  # 15 minutes

        return response_data

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve hot zones: {str(e)}"
        )


@router.get("/data/neighborhood-scores")
async def get_neighborhood_scores(
    market: Optional[str] = Query(None, description="Market name filter"),
    neighborhood: Optional[str] = Query(None, description="Neighborhood name filter"),
    score_type: Optional[str] = Query(None, description="Score type filter"),
    min_score: Optional[float] = Query(None, description="Minimum score value"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """
    Get neighborhood-level scoring metrics for investment analysis.

    **Data includes:**
    - Walkability and transit scores
    - Amenity density (restaurants, coffee shops, etc.)
    - Safety and crime statistics
    - School quality ratings
    - Economic indicators
    """
    try:
        from app.scripts.import_market_intelligence_csv import NeighborhoodScore

        query = db.query(NeighborhoodScore)

        # Apply filters
        if market:
            query = query.filter(NeighborhoodScore.market_name.ilike(f"%{market}%"))
        if neighborhood:
            query = query.filter(NeighborhoodScore.neighborhood_name.ilike(f"%{neighborhood}%"))
        if score_type:
            query = query.filter(NeighborhoodScore.score_category.ilike(f"%{score_type}%"))
        if min_score is not None:
            query = query.filter(NeighborhoodScore.score_value >= min_score)

        # Order by score value descending
        query = query.order_by(NeighborhoodScore.score_value.desc())

        # Apply limit
        results = query.limit(limit).all()

        # Get summary statistics
        total_count = db.query(NeighborhoodScore).count()
        unique_neighborhoods = db.query(NeighborhoodScore.neighborhood_name).distinct().count()

        return {
            "success": True,
            "total_records": total_count,
            "unique_neighborhoods": unique_neighborhoods,
            "results_count": len(results),
            "data": [
                {
                    "id": r.id,
                    "market": r.market_name,
                    "neighborhood_name": r.neighborhood_name,
                    "score_category": r.score_category,
                    "score_value": float(r.score_value) if r.score_value else None,
                    "rank_within_market": r.rank_within_market,
                    "rank_nationally": r.rank_nationally,
                    "period": r.period.isoformat() if r.period else None,
                    "data_source": r.data_source,
                    "notes": r.notes if hasattr(r, 'notes') else None,
                }
                for r in results
            ]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve neighborhood scores: {str(e)}"
        )


@router.get("/data/str-hot-neighborhoods")
async def get_str_hot_neighborhoods(
    market: Optional[str] = Query(None, description="Market name filter"),
    min_revenue: Optional[float] = Query(None, description="Minimum average annual revenue"),
    min_occupancy: Optional[float] = Query(None, description="Minimum occupancy rate (0-1)"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """
    Get Short-Term Rental (STR) hot neighborhoods for investment opportunities.

    **Data includes:**
    - Average annual revenue per listing
    - Occupancy rates
    - Neighborhood rankings
    - ADR (Average Daily Rate)
    - RevPAR (Revenue Per Available Room)
    """
    try:
        from app.scripts.import_market_intelligence_csv import STRHotNeighborhood

        query = db.query(STRHotNeighborhood)

        # Apply filters
        if market:
            query = query.filter(STRHotNeighborhood.market.ilike(f"%{market}%"))
        if min_revenue is not None:
            query = query.filter(STRHotNeighborhood.avg_annual_revenue_per_listing >= min_revenue)
        if min_occupancy is not None:
            query = query.filter(STRHotNeighborhood.avg_occupancy_rate_pct >= min_occupancy)

        # Order by revenue descending
        query = query.order_by(STRHotNeighborhood.avg_annual_revenue_per_listing.desc())

        # Apply limit
        results = query.limit(limit).all()

        # Get summary statistics
        total_count = db.query(STRHotNeighborhood).count()
        unique_markets = db.query(STRHotNeighborhood.market).distinct().count()

        return {
            "success": True,
            "total_records": total_count,
            "unique_markets": unique_markets,
            "results_count": len(results),
            "data": [
                {
                    "id": r.id,
                    "market": r.market,
                    "neighborhood_rank": r.neighborhood_rank,
                    "neighborhood_name": r.neighborhood_name,
                    "avg_annual_revenue_per_listing": float(r.avg_annual_revenue_per_listing) if r.avg_annual_revenue_per_listing else None,
                    "avg_occupancy_rate_pct": float(r.avg_occupancy_rate_pct) if r.avg_occupancy_rate_pct else None,
                    "avg_revpar": float(r.avg_revpar) if r.avg_revpar else None,
                    "growth_stage": r.growth_stage,
                    "revenue_category": r.revenue_category,
                    "analysis_date": r.analysis_date.isoformat() if r.analysis_date else None,
                    "data_source": r.data_source,
                }
                for r in results
            ]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve STR hot neighborhoods: {str(e)}"
        )


@router.get("/data/str-performance-metrics")
async def get_str_performance_metrics(
    market: Optional[str] = Query(None, description="Market name filter"),
    property_type: Optional[str] = Query(None, description="Property type filter"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """
    Get STR performance metrics by property type and market.

    **Data includes:**
    - ADR (Average Daily Rate)
    - Occupancy rates
    - RevPAR (Revenue Per Available Room)
    - Booking lead times
    - Length of stay patterns
    """
    try:
        from app.scripts.import_market_intelligence_csv import STRPerformanceMetrics

        query = db.query(STRPerformanceMetrics)

        # Apply filters
        if market:
            query = query.filter(STRPerformanceMetrics.market.ilike(f"%{market}%"))
        if property_type:
            query = query.filter(STRPerformanceMetrics.property_type.ilike(f"%{property_type}%"))

        # Order by RevPAR descending
        query = query.order_by(STRPerformanceMetrics.revpar.desc().nullslast())

        # Apply limit
        results = query.limit(limit).all()

        # Get summary statistics
        total_count = db.query(STRPerformanceMetrics).count()

        return {
            "success": True,
            "total_records": total_count,
            "results_count": len(results),
            "data": [
                {
                    "id": r.id,
                    "market": r.market,
                    "property_type": r.property_type,
                    "adr_daily": float(r.adr_daily) if r.adr_daily else None,
                    "occupancy_rate_pct": float(r.occupancy_rate_pct) if r.occupancy_rate_pct else None,
                    "revpar": float(r.revpar) if r.revpar else None,
                    "monthly_revenue_avg": float(r.monthly_revenue_avg) if r.monthly_revenue_avg else None,
                    "annual_revenue_avg": float(r.annual_revenue_avg) if r.annual_revenue_avg else None,
                    "booking_lead_time_days": r.booking_lead_time_days,
                    "avg_length_of_stay_nights": float(r.avg_length_of_stay_nights) if r.avg_length_of_stay_nights else None,
                    "review_score": float(r.review_score) if r.review_score else None,
                    "period": r.period.isoformat() if r.period else None,
                    "data_source": r.data_source,
                }
                for r in results
            ]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve STR performance metrics: {str(e)}"
        )


@router.get("/data/str-market-overview")
async def get_str_market_overview(
    market: Optional[str] = Query(None, description="Market name filter"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """
    Get STR market overview statistics.

    **Data includes:**
    - Total listing counts
    - Inventory growth rates
    - Market saturation metrics
    - Host concentration
    """
    try:
        from app.scripts.import_market_intelligence_csv import STRMarketOverview

        query = db.query(STRMarketOverview)

        # Apply filters
        if market:
            query = query.filter(STRMarketOverview.market.ilike(f"%{market}%"))

        # Order by listing count descending
        query = query.order_by(STRMarketOverview.total_str_listings.desc().nullslast())

        # Apply limit
        results = query.limit(limit).all()

        # Get summary statistics
        total_count = db.query(STRMarketOverview).count()

        return {
            "success": True,
            "total_records": total_count,
            "results_count": len(results),
            "data": [
                {
                    "id": r.id,
                    "market": r.market,
                    "total_str_listings": r.total_str_listings,
                    "active_listings_30days": r.active_listings_30days,
                    "entire_home_apt_count": r.entire_home_apt_count,
                    "entire_home_pct": float(r.entire_home_pct) if r.entire_home_pct else None,
                    "private_shared_room_count": r.private_shared_room_count,
                    "private_shared_room_pct": float(r.private_shared_room_pct) if r.private_shared_room_pct else None,
                    "str_pct_of_housing_stock": float(r.str_pct_of_housing_stock) if r.str_pct_of_housing_stock else None,
                    "inventory_growth_yoy_pct": float(r.inventory_growth_yoy_pct) if r.inventory_growth_yoy_pct else None,
                    "avg_listing_age_months": float(r.avg_listing_age_months) if r.avg_listing_age_months else None,
                    "host_concentration_10plus_pct": float(r.host_concentration_10plus_pct) if r.host_concentration_10plus_pct else None,
                    "analysis_date": r.analysis_date.isoformat() if r.analysis_date else None,
                    "data_source": r.data_source,
                }
                for r in results
            ]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve STR market overview: {str(e)}"
        )


@router.get("/data/str-regulatory-environment")
async def get_str_regulatory_environment(
    market: Optional[str] = Query(None, description="Market name filter"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """
    Get STR regulatory environment data by market.

    **Data includes:**
    - Licensing requirements
    - Permit costs and timelines
    - Occupancy limits
    - Enforcement severity
    """
    try:
        from app.scripts.import_market_intelligence_csv import STRRegulatoryEnvironment

        query = db.query(STRRegulatoryEnvironment)

        # Apply filters
        if market:
            query = query.filter(STRRegulatoryEnvironment.market.ilike(f"%{market}%"))

        # Order by market name
        query = query.order_by(STRRegulatoryEnvironment.market)

        # Apply limit
        results = query.limit(limit).all()

        # Get summary statistics
        total_count = db.query(STRRegulatoryEnvironment).count()

        return {
            "success": True,
            "total_records": total_count,
            "results_count": len(results),
            "data": [
                {
                    "id": r.id,
                    "market": r.market,
                    "regulation_type": r.regulation_type,
                    "registration_required": r.registration_required,
                    "license_permit_required": r.license_permit_required,
                    "license_cost_usd": float(r.license_cost_usd) if r.license_cost_usd else None,
                    "primary_residence_requirement": r.primary_residence_requirement,
                    "max_rental_days_per_year": r.max_rental_days_per_year,
                    "occupancy_tax_rate_pct": float(r.occupancy_tax_rate_pct) if r.occupancy_tax_rate_pct else None,
                    "platform_collects_taxes": r.platform_collects_taxes,
                    "enforcement_level": r.enforcement_level,
                    "fine_per_violation_usd": float(r.fine_per_violation_usd) if r.fine_per_violation_usd else None,
                    "effective_date": r.effective_date.isoformat() if r.effective_date else None,
                    "data_source": r.data_source,
                }
                for r in results
            ]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve STR regulatory environment: {str(e)}"
        )


@router.get("/data/zoning-districts")
async def get_zoning_districts(
    market: Optional[str] = Query(None, description="Market name filter"),
    zone_type: Optional[str] = Query(None, description="Zone type filter"),
    min_far: Optional[float] = Query(None, description="Minimum FAR (Floor Area Ratio)"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """
    Get zoning district information across markets.

    **Data includes:**
    - FAR (Floor Area Ratio) limits
    - Height restrictions
    - Parking requirements
    - Allowed uses
    """
    try:
        from app.scripts.import_market_intelligence_csv import ZoningDistrict

        query = db.query(ZoningDistrict)

        # Apply filters
        if market:
            query = query.filter(ZoningDistrict.market.ilike(f"%{market}%"))
        if zone_type:
            query = query.filter(ZoningDistrict.zone_type.ilike(f"%{zone_type}%"))
        if min_far is not None:
            query = query.filter(ZoningDistrict.max_far >= min_far)

        # Order by FAR descending
        query = query.order_by(ZoningDistrict.max_far.desc())

        # Apply limit
        results = query.limit(limit).all()

        # Get summary statistics
        total_count = db.query(ZoningDistrict).count()
        unique_markets = db.query(ZoningDistrict.market).distinct().count()

        return {
            "success": True,
            "total_records": total_count,
            "unique_markets": unique_markets,
            "results_count": len(results),
            "data": [
                {
                    "id": r.id,
                    "market": r.market,
                    "zone_code": r.zone_code,
                    "zone_type": r.zone_type,
                    "max_far": float(r.max_far) if r.max_far else None,
                    "max_height_feet": r.max_height_feet,
                    "min_lot_size_sf": r.min_lot_size_sf,
                    "parking_requirement": r.parking_requirement,
                    "setback_front_feet": r.setback_front_feet,
                    "use_restrictions": r.use_restrictions,
                    "effective_date": r.effective_date.isoformat() if r.effective_date else None,
                    "data_source": r.data_source,
                }
                for r in results
            ]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve zoning districts: {str(e)}"
        )


@router.get("/data/zoning-reforms")
async def get_zoning_reforms(
    market: Optional[str] = Query(None, description="Market name filter"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """
    Get zoning reform and regulatory change data.

    **Data includes:**
    - Reform names and descriptions
    - Implementation dates
    - Impact on development capacity (units enabled)
    - Affected areas
    """
    try:
        from app.scripts.import_market_intelligence_csv import ZoningReform

        query = db.query(ZoningReform)

        # Apply filters
        if market:
            query = query.filter(ZoningReform.market.ilike(f"%{market}%"))

        # Order by effective date descending
        query = query.order_by(ZoningReform.effective_date.desc().nullslast())

        # Apply limit
        results = query.limit(limit).all()

        # Get summary statistics
        total_count = db.query(ZoningReform).count()

        return {
            "success": True,
            "total_records": total_count,
            "results_count": len(results),
            "data": [
                {
                    "id": r.id,
                    "market": r.market,
                    "reform_name": r.reform_name,
                    "area_affected": r.area_affected,
                    "old_zoning": r.old_zoning,
                    "new_zoning": r.new_zoning,
                    "effective_date": r.effective_date.isoformat() if r.effective_date else None,
                    "units_enabled": r.units_enabled,
                    "description": r.description,
                    "data_source": r.data_source,
                }
                for r in results
            ]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve zoning reforms: {str(e)}"
        )


@router.get("/data/opportunity-zones")
async def get_opportunity_zones(
    market: Optional[str] = Query(None, description="Market name filter"),
    min_investment: Optional[float] = Query(None, description="Minimum total investment"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """
    Get Opportunity Zone investment data.

    **Data includes:**
    - OZ tract designations
    - Investment activity
    - Project counts and types
    - Tax incentive details
    """
    try:
        from app.scripts.import_market_intelligence_csv import OpportunityZone

        query = db.query(OpportunityZone)

        # Apply filters
        if market:
            query = query.filter(OpportunityZone.market.ilike(f"%{market}%"))
        if min_investment is not None:
            query = query.filter(OpportunityZone.investment_in_oz_mm >= min_investment)

        # Order by investment descending
        query = query.order_by(OpportunityZone.investment_in_oz_mm.desc().nullslast())

        # Apply limit
        results = query.limit(limit).all()

        # Get summary statistics
        total_count = db.query(OpportunityZone).count()

        return {
            "success": True,
            "total_records": total_count,
            "results_count": len(results),
            "data": [
                {
                    "id": r.id,
                    "market": r.market,
                    "num_opportunity_zones": r.num_opportunity_zones,
                    "total_acres_in_oz": float(r.total_acres_in_oz) if r.total_acres_in_oz else None,
                    "investment_in_oz_mm": float(r.investment_in_oz_mm) if r.investment_in_oz_mm else None,
                    "development_projects_in_oz": r.development_projects_in_oz,
                    "oz_residential_units": r.oz_residential_units,
                    "oz_commercial_sf": r.oz_commercial_sf,
                    "avg_cap_rate_compression_bps": r.avg_cap_rate_compression_bps,
                    "oz_designation_date": r.oz_designation_date.isoformat() if r.oz_designation_date else None,
                    "period": r.period.isoformat() if r.period else None,
                    "data_source": r.data_source,
                }
                for r in results
            ]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve opportunity zones: {str(e)}"
        )


@router.get("/data/underbuilt-parcels")
async def get_underbuilt_parcels(
    market: Optional[str] = Query(None, description="Market name filter"),
    zone_type: Optional[str] = Query(None, description="Zone type filter"),
    min_far_gap: Optional[float] = Query(None, description="Minimum FAR gap (potential vs utilized)"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """
    Get underbuilt parcel analysis for development opportunities (aggregate data by market and zone).

    **Data includes:**
    - FAR gap analysis (potential vs utilized)
    - Aggregate parcel statistics by zone
    - Estimated additional buildable SF
    - Development potential
    """
    try:
        from app.scripts.import_market_intelligence_csv import UnderbuiltParcel

        query = db.query(UnderbuiltParcel)

        # Apply filters
        if market:
            query = query.filter(UnderbuiltParcel.market.ilike(f"%{market}%"))
        if zone_type:
            query = query.filter(UnderbuiltParcel.zone_type.ilike(f"%{zone_type}%"))
        if min_far_gap is not None:
            query = query.filter(UnderbuiltParcel.far_gap >= min_far_gap)

        # Order by FAR gap descending
        query = query.order_by(UnderbuiltParcel.far_gap.desc().nullslast())

        # Apply limit
        results = query.limit(limit).all()

        # Get summary statistics
        total_count = db.query(UnderbuiltParcel).count()

        return {
            "success": True,
            "total_records": total_count,
            "results_count": len(results),
            "data": [
                {
                    "id": r.id,
                    "market": r.market,
                    "zone_type": r.zone_type,
                    "num_underbuilt_parcels": r.num_underbuilt_parcels,
                    "avg_current_far": float(r.avg_current_far) if r.avg_current_far else None,
                    "avg_max_allowed_far": float(r.avg_max_allowed_far) if r.avg_max_allowed_far else None,
                    "far_gap": float(r.far_gap) if r.far_gap else None,
                    "avg_current_height_feet": r.avg_current_height_feet,
                    "avg_max_height_feet": r.avg_max_height_feet,
                    "avg_parcel_size_sf": r.avg_parcel_size_sf,
                    "avg_parcel_size_acres": float(r.avg_parcel_size_acres) if r.avg_parcel_size_acres else None,
                    "total_additional_developable_sf": r.total_additional_developable_sf,
                    "estimated_additional_units_possible": r.estimated_additional_units_possible,
                    "analysis_date": r.analysis_date.isoformat() if r.analysis_date else None,
                    "data_source": r.data_source,
                }
                for r in results
            ]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve underbuilt parcels: {str(e)}"
        )


@router.get("/data/development-pipeline")
async def get_development_pipeline(
    market: Optional[str] = Query(None, description="Market name filter"),
    zone_type: Optional[str] = Query(None, description="Zone type filter"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """
    Get development pipeline data by market (aggregate statistics by zone).

    **Data includes:**
    - Projects under construction counts and stats
    - Permits issued year-to-date
    - Applications pending
    - Approval timelines and success rates
    """
    try:
        from app.scripts.import_market_intelligence_csv import DevelopmentPipeline

        query = db.query(DevelopmentPipeline)

        # Apply filters
        if market:
            query = query.filter(DevelopmentPipeline.market.ilike(f"%{market}%"))
        if zone_type:
            query = query.filter(DevelopmentPipeline.zone_type.ilike(f"%{zone_type}%"))

        # Order by units under construction descending
        query = query.order_by(DevelopmentPipeline.units_under_construction.desc().nullslast())

        # Apply limit
        results = query.limit(limit).all()

        # Get summary statistics
        total_count = db.query(DevelopmentPipeline).count()
        unique_markets = db.query(DevelopmentPipeline.market).distinct().count()

        return {
            "success": True,
            "total_records": total_count,
            "unique_markets": unique_markets,
            "results_count": len(results),
            "data": [
                {
                    "id": r.id,
                    "market": r.market,
                    "zone_type": r.zone_type,
                    "projects_under_construction": r.projects_under_construction,
                    "units_under_construction": r.units_under_construction,
                    "sf_under_construction": r.sf_under_construction,
                    "permits_issued_ytd_2024": r.permits_issued_ytd_2024,
                    "units_permitted_ytd": r.units_permitted_ytd,
                    "sf_permitted_ytd": r.sf_permitted_ytd,
                    "permit_value_mm": float(r.permit_value_mm) if r.permit_value_mm else None,
                    "applications_pending": r.applications_pending,
                    "avg_approval_timeline_months": float(r.avg_approval_timeline_months) if r.avg_approval_timeline_months else None,
                    "approval_success_rate_pct": float(r.approval_success_rate_pct) if r.approval_success_rate_pct else None,
                    "period": r.period.isoformat() if r.period else None,
                    "data_source": r.data_source,
                }
                for r in results
            ]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve development pipeline: {str(e)}"
        )


@router.get("/data/land-cost-economics")
async def get_land_cost_economics(
    market: Optional[str] = Query(None, description="Market name filter"),
    zone_type: Optional[str] = Query(None, description="Zone type filter"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """
    Get land cost and development economics data.

    **Data includes:**
    - Land prices per SF and per developable SF
    - Construction costs
    - Land as % of total cost
    - Pro forma yields
    """
    try:
        from app.scripts.import_market_intelligence_csv import LandCostEconomics

        query = db.query(LandCostEconomics)

        # Apply filters
        if market:
            query = query.filter(LandCostEconomics.market.ilike(f"%{market}%"))
        if zone_type:
            query = query.filter(LandCostEconomics.zone_type.ilike(f"%{zone_type}%"))

        # Order by land price descending
        query = query.order_by(LandCostEconomics.land_price_per_sf.desc().nullslast())

        # Apply limit
        results = query.limit(limit).all()

        # Get summary statistics
        total_count = db.query(LandCostEconomics).count()

        return {
            "success": True,
            "total_records": total_count,
            "results_count": len(results),
            "data": [
                {
                    "id": r.id,
                    "market": r.market,
                    "zone_type": r.zone_type,
                    "land_price_per_sf": float(r.land_price_per_sf) if r.land_price_per_sf else None,
                    "land_price_per_developable_sf": float(r.land_price_per_developable_sf) if r.land_price_per_developable_sf else None,
                    "land_as_pct_of_total_cost": float(r.land_as_pct_of_total_cost) if r.land_as_pct_of_total_cost else None,
                    "estimated_construction_cost_per_sf": float(r.estimated_construction_cost_per_sf) if r.estimated_construction_cost_per_sf else None,
                    "pro_forma_yield_on_cost_pct": float(r.pro_forma_yield_on_cost_pct) if r.pro_forma_yield_on_cost_pct else None,
                    "period": r.period.isoformat() if r.period else None,
                    "data_source": r.data_source,
                }
                for r in results
            ]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve land cost economics: {str(e)}"
        )


@router.get("/data/property-tax-assessments")
async def get_property_tax_assessments(
    market: Optional[str] = Query(None, description="Market name filter"),
    geography_type: Optional[str] = Query(None, description="Geography type filter (Metro, Borough, County)"),
    indicator_name: Optional[str] = Query(None, description="Indicator name filter"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """
    Get property tax assessment indicators across markets.

    **Data includes:**
    - Various tax-related indicators by geography
    - Market-specific tax metrics
    - Assessment data
    - Tax burden metrics
    """
    try:
        from app.scripts.import_market_intelligence_csv import PropertyTaxAssessment

        query = db.query(PropertyTaxAssessment)

        # Apply filters
        if market:
            query = query.filter(PropertyTaxAssessment.market.ilike(f"%{market}%"))
        if geography_type:
            query = query.filter(PropertyTaxAssessment.geography_type.ilike(f"%{geography_type}%"))
        if indicator_name:
            query = query.filter(PropertyTaxAssessment.indicator_name.ilike(f"%{indicator_name}%"))

        # Order by market and indicator name
        query = query.order_by(PropertyTaxAssessment.market, PropertyTaxAssessment.indicator_name)

        # Apply limit
        results = query.limit(limit).all()

        # Get summary statistics
        total_count = db.query(PropertyTaxAssessment).count()
        unique_markets = db.query(PropertyTaxAssessment.market).distinct().count()

        return {
            "success": True,
            "total_records": total_count,
            "unique_markets": unique_markets,
            "results_count": len(results),
            "data": [
                {
                    "id": r.id,
                    "market": r.market,
                    "geography_type": r.geography_type,
                    "indicator_name": r.indicator_name,
                    "indicator_value": float(r.indicator_value) if r.indicator_value else None,
                    "indicator_unit": r.indicator_unit,
                    "data_source": r.data_source,
                    "notes": r.notes if hasattr(r, 'notes') else None,
                }
                for r in results
            ]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve property tax assessments: {str(e)}"
        )


@router.get("/data/tenant-credit-quality")
async def get_tenant_credit_quality(
    tenant_name: Optional[str] = Query(None, description="Tenant name filter"),
    category: Optional[str] = Query(None, description="Category filter"),
    metric_name: Optional[str] = Query(None, description="Metric name filter"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """
    Get tenant credit quality and financial metrics data.

    **Data includes:**
    - Credit ratings (Moody's and S&P)
    - Financial metrics by tenant
    - Various performance indicators
    - Industry classifications
    """
    try:
        from app.scripts.import_market_intelligence_csv import TenantCreditQuality

        query = db.query(TenantCreditQuality)

        # Apply filters
        if tenant_name:
            query = query.filter(TenantCreditQuality.tenant_name.ilike(f"%{tenant_name}%"))
        if category:
            query = query.filter(TenantCreditQuality.category.ilike(f"%{category}%"))
        if metric_name:
            query = query.filter(TenantCreditQuality.metric_name.ilike(f"%{metric_name}%"))

        # Order by tenant name and metric name
        query = query.order_by(TenantCreditQuality.tenant_name, TenantCreditQuality.metric_name)

        # Apply limit
        results = query.limit(limit).all()

        # Get summary statistics
        total_count = db.query(TenantCreditQuality).count()
        unique_tenants = db.query(TenantCreditQuality.tenant_name).distinct().count()

        return {
            "success": True,
            "total_records": total_count,
            "unique_tenants": unique_tenants,
            "results_count": len(results),
            "data": [
                {
                    "id": r.id,
                    "tenant_name": r.tenant_name,
                    "ticker": r.ticker,
                    "category": r.category,
                    "company_name": r.company_name,
                    "moodys_rating": r.moodys_rating,
                    "sp_rating": r.sp_rating,
                    "metric_name": r.metric_name,
                    "metric_value": float(r.metric_value) if r.metric_value else None,
                    "unit": r.unit,
                    "period": r.period.isoformat() if r.period else None,
                    "data_source": r.data_source,
                    "notes": r.notes if hasattr(r, 'notes') else None,
                }
                for r in results
            ]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve tenant credit quality: {str(e)}"
        )

# ========================================
# FINANCIAL TIME-SERIES ENDPOINTS
# ========================================

@router.get("/data/financial-time-series")
async def get_financial_time_series(
    source_category: Optional[str] = Query(None, description="Source category filter (e.g., treasury_yield_curve, fed_policy_financial_conditions)"),
    indicator_name: Optional[str] = Query(None, description="Indicator name filter"),
    start_date: Optional[date] = Query(None, description="Start date filter (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date filter (YYYY-MM-DD)"),
    period_type: Optional[str] = Query(None, description="Period type filter (quarterly, monthly, daily, annual)"),
    limit: int = Query(1000, ge=1, le=5000, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """
    Get financial time-series indicator data.
    
    **Data includes 9 financial categories:**
    - Treasury Yield Curve (2020-2025)
    - Fed Policy & Financial Conditions
    - Banking Sector Health
    - Credit Markets & Fixed Income
    - Global Economic Indicators
    - Corporate Earnings & Business Confidence
    - Consumer Finance & Household Balance Sheet
    - Currency, Commodities & Construction Costs
    - Institutional Asset Allocation & Portfolio Positioning
    """
    try:
        from app.scripts.import_market_intelligence_csv import TimeSeriesIndicator
        
        query = db.query(TimeSeriesIndicator)
        
        # Apply filters
        if source_category:
            query = query.filter(TimeSeriesIndicator.source_category == source_category)
        if indicator_name:
            query = query.filter(TimeSeriesIndicator.indicator_name.ilike(f"%{indicator_name}%"))
        if start_date:
            query = query.filter(TimeSeriesIndicator.date >= start_date)
        if end_date:
            query = query.filter(TimeSeriesIndicator.date <= end_date)
        if period_type:
            query = query.filter(TimeSeriesIndicator.period_type == period_type)
        
        # Order by date descending
        query = query.order_by(TimeSeriesIndicator.date.desc())
        
        # Apply limit
        results = query.limit(limit).all()
        
        # Get summary statistics
        total_count = db.query(TimeSeriesIndicator).filter(
            TimeSeriesIndicator.source_category == source_category if source_category else True
        ).count()
        
        return {
            "success": True,
            "total_records": total_count,
            "results_count": len(results),
            "data": [
                {
                    "id": r.id,
                    "date": r.date.isoformat() if r.date else None,
                    "period_type": r.period_type,
                    "indicator_name": r.indicator_name,
                    "indicator_value": float(r.indicator_value) if r.indicator_value else None,
                    "indicator_unit": r.indicator_unit,
                    "source_category": r.source_category,
                    "data_source": r.data_source,
                    "notes": r.notes,
                }
                for r in results
            ]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve financial time-series data: {str(e)}"
        )


@router.get("/data/financial-time-series/categories")
async def get_financial_time_series_categories(
    db: Session = Depends(get_db)
):
    """Get list of available financial time-series source categories with record counts."""
    try:
        from app.scripts.import_market_intelligence_csv import TimeSeriesIndicator
        from sqlalchemy import func
        
        categories = db.query(
            TimeSeriesIndicator.source_category,
            func.count(TimeSeriesIndicator.id).label('count'),
            func.min(TimeSeriesIndicator.date).label('start_date'),
            func.max(TimeSeriesIndicator.date).label('end_date')
        ).group_by(
            TimeSeriesIndicator.source_category
        ).all()
        
        return {
            "success": True,
            "categories": [
                {
                    "source_category": cat.source_category,
                    "count": cat.count,
                    "start_date": cat.start_date.isoformat() if cat.start_date else None,
                    "end_date": cat.end_date.isoformat() if cat.end_date else None,
                }
                for cat in categories
            ]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve categories: {str(e)}"
        )


@router.get("/data/financial-time-series/indicators")
async def get_financial_time_series_indicators(
    source_category: str = Query(..., description="Source category to get indicators for"),
    db: Session = Depends(get_db)
):
    """Get list of available indicators for a specific financial time-series category."""
    try:
        from app.scripts.import_market_intelligence_csv import TimeSeriesIndicator
        from sqlalchemy import func
        
        indicators = db.query(
            TimeSeriesIndicator.indicator_name,
            func.count(TimeSeriesIndicator.id).label('count')
        ).filter(
            TimeSeriesIndicator.source_category == source_category
        ).group_by(
            TimeSeriesIndicator.indicator_name
        ).all()
        
        return {
            "success": True,
            "source_category": source_category,
            "indicators": [
                {
                    "indicator_name": ind.indicator_name,
                    "count": ind.count,
                }
                for ind in indicators
            ]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve indicators: {str(e)}"
        )


# ========================================
# STR ANALYTICS ENDPOINTS (NEW)
# ========================================

@router.get("/data/str-analytics/competitive-analysis")
async def get_str_competitive_analysis(
    city: Optional[str] = Query(None, description="City filter"),
    property_type: Optional[str] = Query(None, description="Property type filter"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """Get STR competitive analysis data including market share, pricing strategies, and competitive positioning."""
    try:
        from app.scripts.import_market_intelligence_csv import STRCompetitiveAnalysis
        
        query = db.query(STRCompetitiveAnalysis)
        
        if city:
            query = query.filter(STRCompetitiveAnalysis.city.ilike(f"%{city}%"))
        if property_type:
            query = query.filter(STRCompetitiveAnalysis.property_type == property_type)
        
        results = query.limit(limit).all()
        
        return {
            "success": True,
            "results_count": len(results),
            "data": [
                {
                    "id": r.id,
                    "city": r.city,
                    "neighborhood": r.neighborhood,
                    "property_type": r.property_type,
                    "competitor_name": r.competitor_name,
                    "market_share": float(r.market_share) if r.market_share else None,
                    "avg_daily_rate": float(r.avg_daily_rate) if r.avg_daily_rate else None,
                    "occupancy_rate": float(r.occupancy_rate) if r.occupancy_rate else None,
                    "total_units": r.total_units,
                    "competitive_position": r.competitive_position,
                    "notes": r.notes,
                }
                for r in results
            ]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve STR competitive analysis: {str(e)}"
        )


@router.get("/data/str-analytics/compliance-enforcement")
async def get_str_compliance_enforcement(
    city: Optional[str] = Query(None, description="City filter"),
    violation_type: Optional[str] = Query(None, description="Violation type filter"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """Get STR compliance and enforcement data including violations, fines, and regulatory actions."""
    try:
        from app.scripts.import_market_intelligence_csv import STRComplianceEnforcement
        
        query = db.query(STRComplianceEnforcement)
        
        if city:
            query = query.filter(STRComplianceEnforcement.city.ilike(f"%{city}%"))
        if violation_type:
            query = query.filter(STRComplianceEnforcement.violation_type.ilike(f"%{violation_type}%"))
        
        results = query.limit(limit).all()
        
        return {
            "success": True,
            "results_count": len(results),
            "data": [
                {
                    "id": r.id,
                    "city": r.city,
                    "violation_type": r.violation_type,
                    "violation_count": r.violation_count,
                    "total_fines": float(r.total_fines) if r.total_fines else None,
                    "enforcement_rate": float(r.enforcement_rate) if r.enforcement_rate else None,
                    "period": r.period.isoformat() if r.period else None,
                    "notes": r.notes,
                }
                for r in results
            ]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve STR compliance data: {str(e)}"
        )


@router.get("/data/str-analytics/guest-demographics")
async def get_str_guest_demographics(
    city: Optional[str] = Query(None, description="City filter"),
    demographic_category: Optional[str] = Query(None, description="Demographic category filter"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """Get STR guest demographics data including age groups, income levels, and travel purposes."""
    try:
        from app.scripts.import_market_intelligence_csv import STRGuestDemographics
        
        query = db.query(STRGuestDemographics)
        
        if city:
            query = query.filter(STRGuestDemographics.city.ilike(f"%{city}%"))
        if demographic_category:
            query = query.filter(STRGuestDemographics.demographic_category.ilike(f"%{demographic_category}%"))
        
        results = query.limit(limit).all()
        
        return {
            "success": True,
            "results_count": len(results),
            "data": [
                {
                    "id": r.id,
                    "city": r.city,
                    "demographic_category": r.demographic_category,
                    "demographic_value": r.demographic_value,
                    "percentage": float(r.percentage) if r.percentage else None,
                    "average_stay_length": float(r.average_stay_length) if r.average_stay_length else None,
                    "average_spend": float(r.average_spend) if r.average_spend else None,
                    "period": r.period.isoformat() if r.period else None,
                    "notes": r.notes,
                }
                for r in results
            ]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve STR guest demographics: {str(e)}"
        )


@router.get("/data/str-analytics/host-economics")
async def get_str_host_economics(
    city: Optional[str] = Query(None, description="City filter"),
    host_type: Optional[str] = Query(None, description="Host type filter (individual, professional, institutional)"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """Get STR host economics data including revenue, expenses, profitability, and operational metrics."""
    try:
        from app.scripts.import_market_intelligence_csv import STRHostEconomics
        
        query = db.query(STRHostEconomics)
        
        if city:
            query = query.filter(STRHostEconomics.city.ilike(f"%{city}%"))
        if host_type:
            query = query.filter(STRHostEconomics.host_type == host_type)
        
        results = query.limit(limit).all()
        
        return {
            "success": True,
            "results_count": len(results),
            "data": [
                {
                    "id": r.id,
                    "city": r.city,
                    "neighborhood": r.neighborhood,
                    "host_type": r.host_type,
                    "avg_annual_revenue": float(r.avg_annual_revenue) if r.avg_annual_revenue else None,
                    "avg_occupancy_rate": float(r.avg_occupancy_rate) if r.avg_occupancy_rate else None,
                    "avg_daily_rate": float(r.avg_daily_rate) if r.avg_daily_rate else None,
                    "operating_expenses_pct": float(r.operating_expenses_pct) if r.operating_expenses_pct else None,
                    "net_operating_income": float(r.net_operating_income) if r.net_operating_income else None,
                    "total_properties": r.total_properties,
                    "period": r.period.isoformat() if r.period else None,
                    "notes": r.notes,
                }
                for r in results
            ]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve STR host economics: {str(e)}"
        )


@router.get("/data/str-analytics/housing-market-impact")
async def get_str_housing_market_impact(
    city: Optional[str] = Query(None, description="City filter"),
    impact_metric: Optional[str] = Query(None, description="Impact metric filter"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """Get STR housing market impact data including effects on housing availability, prices, and neighborhood character."""
    try:
        from app.scripts.import_market_intelligence_csv import STRHousingMarketImpact
        
        query = db.query(STRHousingMarketImpact)
        
        if city:
            query = query.filter(STRHousingMarketImpact.city.ilike(f"%{city}%"))
        if impact_metric:
            query = query.filter(STRHousingMarketImpact.impact_metric.ilike(f"%{impact_metric}%"))
        
        results = query.limit(limit).all()
        
        return {
            "success": True,
            "results_count": len(results),
            "data": [
                {
                    "id": r.id,
                    "city": r.city,
                    "neighborhood": r.neighborhood,
                    "impact_metric": r.impact_metric,
                    "metric_value": float(r.metric_value) if r.metric_value else None,
                    "unit": r.unit,
                    "str_penetration_rate": float(r.str_penetration_rate) if r.str_penetration_rate else None,
                    "housing_units_converted": r.housing_units_converted,
                    "period": r.period.isoformat() if r.period else None,
                    "notes": r.notes,
                }
                for r in results
            ]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve STR housing market impact: {str(e)}"
        )


@router.get("/data/str-analytics/investment-analysis")
async def get_str_investment_analysis(
    city: Optional[str] = Query(None, description="City filter"),
    property_type: Optional[str] = Query(None, description="Property type filter"),
    min_roi: Optional[float] = Query(None, description="Minimum ROI filter"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """Get STR investment analysis data including ROI, payback periods, and investment performance metrics."""
    try:
        from app.scripts.import_market_intelligence_csv import STRInvestmentAnalysis
        
        query = db.query(STRInvestmentAnalysis)
        
        if city:
            query = query.filter(STRInvestmentAnalysis.city.ilike(f"%{city}%"))
        if property_type:
            query = query.filter(STRInvestmentAnalysis.property_type == property_type)
        if min_roi is not None:
            query = query.filter(STRInvestmentAnalysis.estimated_roi >= min_roi)
        
        results = query.limit(limit).all()
        
        return {
            "success": True,
            "results_count": len(results),
            "data": [
                {
                    "id": r.id,
                    "city": r.city,
                    "neighborhood": r.neighborhood,
                    "property_type": r.property_type,
                    "estimated_roi": float(r.estimated_roi) if r.estimated_roi else None,
                    "payback_period_years": float(r.payback_period_years) if r.payback_period_years else None,
                    "avg_annual_revenue": float(r.avg_annual_revenue) if r.avg_annual_revenue else None,
                    "initial_investment": float(r.initial_investment) if r.initial_investment else None,
                    "cap_rate": float(r.cap_rate) if r.cap_rate else None,
                    "occupancy_rate": float(r.occupancy_rate) if r.occupancy_rate else None,
                    "period": r.period.isoformat() if r.period else None,
                    "notes": r.notes,
                }
                for r in results
            ]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve STR investment analysis: {str(e)}"
        )


@router.get("/data/str-analytics/platform-performance")
async def get_str_platform_performance(
    platform_name: Optional[str] = Query(None, description="Platform name filter (Airbnb, Vrbo, etc.)"),
    city: Optional[str] = Query(None, description="City filter"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """Get STR platform performance data including listings, bookings, and revenue by platform."""
    try:
        from app.scripts.import_market_intelligence_csv import STRPlatformPerformance
        
        query = db.query(STRPlatformPerformance)
        
        if platform_name:
            query = query.filter(STRPlatformPerformance.platform_name.ilike(f"%{platform_name}%"))
        if city:
            query = query.filter(STRPlatformPerformance.city.ilike(f"%{city}%"))
        
        results = query.limit(limit).all()
        
        return {
            "success": True,
            "results_count": len(results),
            "data": [
                {
                    "id": r.id,
                    "platform_name": r.platform_name,
                    "city": r.city,
                    "total_listings": r.total_listings,
                    "active_listings": r.active_listings,
                    "market_share": float(r.market_share) if r.market_share else None,
                    "avg_booking_rate": float(r.avg_booking_rate) if r.avg_booking_rate else None,
                    "total_revenue": float(r.total_revenue) if r.total_revenue else None,
                    "period": r.period.isoformat() if r.period else None,
                    "notes": r.notes,
                }
                for r in results
            ]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve STR platform performance: {str(e)}"
        )


@router.get("/data/str-analytics/pricing-patterns")
async def get_str_pricing_patterns(
    city: Optional[str] = Query(None, description="City filter"),
    property_type: Optional[str] = Query(None, description="Property type filter"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """Get STR pricing patterns data including seasonal variations, pricing strategies, and rate optimization."""
    try:
        from app.scripts.import_market_intelligence_csv import STRPricingPatterns
        
        query = db.query(STRPricingPatterns)
        
        if city:
            query = query.filter(STRPricingPatterns.city.ilike(f"%{city}%"))
        if property_type:
            query = query.filter(STRPricingPatterns.property_type == property_type)
        
        results = query.limit(limit).all()
        
        return {
            "success": True,
            "results_count": len(results),
            "data": [
                {
                    "id": r.id,
                    "city": r.city,
                    "neighborhood": r.neighborhood,
                    "property_type": r.property_type,
                    "season": r.season,
                    "avg_daily_rate": float(r.avg_daily_rate) if r.avg_daily_rate else None,
                    "min_rate": float(r.min_rate) if r.min_rate else None,
                    "max_rate": float(r.max_rate) if r.max_rate else None,
                    "price_variation_pct": float(r.price_variation_pct) if r.price_variation_pct else None,
                    "period": r.period.isoformat() if r.period else None,
                    "notes": r.notes,
                }
                for r in results
            ]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve STR pricing patterns: {str(e)}"
        )


@router.get("/data/str-analytics/supply-demand")
async def get_str_supply_demand_dynamics(
    city: Optional[str] = Query(None, description="City filter"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """Get STR supply and demand dynamics including market balance, growth trends, and capacity utilization."""
    try:
        from app.scripts.import_market_intelligence_csv import STRSupplyDemandDynamics
        
        query = db.query(STRSupplyDemandDynamics)
        
        if city:
            query = query.filter(STRSupplyDemandDynamics.city.ilike(f"%{city}%"))
        
        results = query.limit(limit).all()
        
        return {
            "success": True,
            "results_count": len(results),
            "data": [
                {
                    "id": r.id,
                    "city": r.city,
                    "neighborhood": r.neighborhood,
                    "total_supply": r.total_supply,
                    "occupied_units": r.occupied_units,
                    "demand_index": float(r.demand_index) if r.demand_index else None,
                    "supply_growth_rate": float(r.supply_growth_rate) if r.supply_growth_rate else None,
                    "demand_growth_rate": float(r.demand_growth_rate) if r.demand_growth_rate else None,
                    "market_balance": r.market_balance,
                    "period": r.period.isoformat() if r.period else None,
                    "notes": r.notes,
                }
                for r in results
            ]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve STR supply-demand dynamics: {str(e)}"
        )


# ========================================
# ZONING & DEVELOPMENT ENDPOINTS (NEW)
# ========================================

@router.get("/data/zoning/entitled-land")
async def get_entitled_land_inventory(
    city: Optional[str] = Query(None, description="City filter"),
    zoning_designation: Optional[str] = Query(None, description="Zoning designation filter"),
    development_status: Optional[str] = Query(None, description="Development status filter"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """Get entitled land inventory data including approved but undeveloped parcels and development rights."""
    try:
        from app.scripts.import_market_intelligence_csv import EntitledLandInventory
        
        query = db.query(EntitledLandInventory)
        
        if city:
            query = query.filter(EntitledLandInventory.city.ilike(f"%{city}%"))
        if zoning_designation:
            query = query.filter(EntitledLandInventory.zoning_designation.ilike(f"%{zoning_designation}%"))
        if development_status:
            query = query.filter(EntitledLandInventory.development_status == development_status)
        
        results = query.limit(limit).all()
        
        return {
            "success": True,
            "results_count": len(results),
            "data": [
                {
                    "id": r.id,
                    "city": r.city,
                    "neighborhood": r.neighborhood,
                    "zoning_designation": r.zoning_designation,
                    "parcel_size_acres": float(r.parcel_size_acres) if r.parcel_size_acres else None,
                    "entitled_units": r.entitled_units,
                    "entitled_sq_ft": float(r.entitled_sq_ft) if r.entitled_sq_ft else None,
                    "development_status": r.development_status,
                    "approval_date": r.approval_date.isoformat() if r.approval_date else None,
                    "estimated_value": float(r.estimated_value) if r.estimated_value else None,
                    "notes": r.notes,
                }
                for r in results
            ]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve entitled land inventory: {str(e)}"
        )


@router.get("/data/zoning/future-initiatives")
async def get_future_zoning_initiatives(
    city: Optional[str] = Query(None, description="City filter"),
    initiative_type: Optional[str] = Query(None, description="Initiative type filter"),
    status: Optional[str] = Query(None, description="Status filter (proposed, under_review, approved)"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """Get future zoning initiatives data including proposed changes, upzoning plans, and policy reforms."""
    try:
        from app.scripts.import_market_intelligence_csv import FutureZoningInitiatives
        
        query = db.query(FutureZoningInitiatives)
        
        if city:
            query = query.filter(FutureZoningInitiatives.city.ilike(f"%{city}%"))
        if initiative_type:
            query = query.filter(FutureZoningInitiatives.initiative_type.ilike(f"%{initiative_type}%"))
        if status:
            query = query.filter(FutureZoningInitiatives.status == status)
        
        results = query.limit(limit).all()
        
        return {
            "success": True,
            "results_count": len(results),
            "data": [
                {
                    "id": r.id,
                    "city": r.city,
                    "neighborhood": r.neighborhood,
                    "initiative_name": r.initiative_name,
                    "initiative_type": r.initiative_type,
                    "description": r.description,
                    "status": r.status,
                    "estimated_units_added": r.estimated_units_added,
                    "proposed_date": r.proposed_date.isoformat() if r.proposed_date else None,
                    "expected_approval_date": r.expected_approval_date.isoformat() if r.expected_approval_date else None,
                    "impact_assessment": r.impact_assessment,
                    "notes": r.notes,
                }
                for r in results
            ]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve future zoning initiatives: {str(e)}"
        )


@router.get("/data/zoning/regulatory-barriers")
async def get_regulatory_barriers(
    city: Optional[str] = Query(None, description="City filter"),
    barrier_type: Optional[str] = Query(None, description="Barrier type filter"),
    severity: Optional[str] = Query(None, description="Severity filter (low, medium, high)"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """Get regulatory barriers data including zoning restrictions, permitting challenges, and development obstacles."""
    try:
        from app.scripts.import_market_intelligence_csv import RegulatoryBarriers
        
        query = db.query(RegulatoryBarriers)
        
        if city:
            query = query.filter(RegulatoryBarriers.city.ilike(f"%{city}%"))
        if barrier_type:
            query = query.filter(RegulatoryBarriers.barrier_type.ilike(f"%{barrier_type}%"))
        if severity:
            query = query.filter(RegulatoryBarriers.severity == severity)
        
        results = query.limit(limit).all()
        
        return {
            "success": True,
            "results_count": len(results),
            "data": [
                {
                    "id": r.id,
                    "city": r.city,
                    "neighborhood": r.neighborhood,
                    "barrier_type": r.barrier_type,
                    "description": r.description,
                    "severity": r.severity,
                    "estimated_cost_impact": float(r.estimated_cost_impact) if r.estimated_cost_impact else None,
                    "estimated_time_delay_months": float(r.estimated_time_delay_months) if r.estimated_time_delay_months else None,
                    "affected_development_types": r.affected_development_types,
                    "notes": r.notes,
                }
                for r in results
            ]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve regulatory barriers: {str(e)}"
        )


@router.get("/data/zoning/tod")
async def get_transit_oriented_development(
    city: Optional[str] = Query(None, description="City filter"),
    transit_type: Optional[str] = Query(None, description="Transit type filter (subway, light_rail, bus_rapid_transit)"),
    development_status: Optional[str] = Query(None, description="Development status filter"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """Get Transit-Oriented Development (TOD) data including projects near transit hubs and density bonuses."""
    try:
        from app.scripts.import_market_intelligence_csv import TransitOrientedDevelopment
        
        query = db.query(TransitOrientedDevelopment)
        
        if city:
            query = query.filter(TransitOrientedDevelopment.city.ilike(f"%{city}%"))
        if transit_type:
            query = query.filter(TransitOrientedDevelopment.transit_type == transit_type)
        if development_status:
            query = query.filter(TransitOrientedDevelopment.development_status == development_status)
        
        results = query.limit(limit).all()
        
        return {
            "success": True,
            "results_count": len(results),
            "data": [
                {
                    "id": r.id,
                    "city": r.city,
                    "neighborhood": r.neighborhood,
                    "transit_station": r.transit_station,
                    "transit_type": r.transit_type,
                    "distance_to_transit_feet": float(r.distance_to_transit_feet) if r.distance_to_transit_feet else None,
                    "project_name": r.project_name,
                    "total_units": r.total_units,
                    "density_bonus_units": r.density_bonus_units,
                    "development_status": r.development_status,
                    "estimated_completion": r.estimated_completion.isoformat() if r.estimated_completion else None,
                    "tod_incentives": r.tod_incentives,
                    "notes": r.notes,
                }
                for r in results
            ]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve TOD data: {str(e)}"
        )


@router.get("/data/zoning/master-metrics")
async def get_zoning_master_metrics(
    city: Optional[str] = Query(None, description="City filter"),
    metric_category: Optional[str] = Query(None, description="Metric category filter"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """Get zoning master metrics data including comprehensive zoning statistics and trends."""
    try:
        from app.scripts.import_market_intelligence_csv import ZoningMasterMetrics
        
        query = db.query(ZoningMasterMetrics)
        
        if city:
            query = query.filter(ZoningMasterMetrics.city.ilike(f"%{city}%"))
        if metric_category:
            query = query.filter(ZoningMasterMetrics.metric_category.ilike(f"%{metric_category}%"))
        
        results = query.limit(limit).all()
        
        return {
            "success": True,
            "results_count": len(results),
            "data": [
                {
                    "id": r.id,
                    "city": r.city,
                    "metric_category": r.metric_category,
                    "metric_name": r.metric_name,
                    "metric_value": float(r.metric_value) if r.metric_value else None,
                    "unit": r.unit,
                    "period": r.period.isoformat() if r.period else None,
                    "year_over_year_change": float(r.year_over_year_change) if r.year_over_year_change else None,
                    "notes": r.notes,
                }
                for r in results
            ]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve zoning master metrics: {str(e)}"
        )

