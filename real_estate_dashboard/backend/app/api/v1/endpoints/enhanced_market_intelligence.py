"""
Enhanced Market Intelligence API Endpoints

Advanced market analysis features:
- Custom market creation and management
- Competitive set tracking
- Automated market updates
- Rent trend analysis
- Supply/demand modeling
- Economic indicator correlations
"""

from typing import List, Optional
from datetime import datetime, date, timedelta
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_

from app.api.deps import get_db
from app.models.enhanced_market_intelligence import (
    CustomMarket, CompetitiveProperty, RentTrendAnalysis,
    SupplyDemandAnalysis, EconomicIndicatorCorrelation,
    MarketUpdateSchedule, MarketType, UpdateFrequency
)


router = APIRouter()


# ========================================
# PYDANTIC SCHEMAS
# ========================================

class CustomMarketBase(BaseModel):
    """Base schema for custom market"""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    market_type: MarketType = MarketType.CUSTOM
    geographic_areas: Optional[dict] = None
    property_types: Optional[list] = None
    price_range_min: Optional[float] = None
    price_range_max: Optional[float] = None
    size_range_min: Optional[int] = None
    size_range_max: Optional[int] = None
    year_built_min: Optional[int] = None
    year_built_max: Optional[int] = None
    custom_criteria: Optional[dict] = None
    auto_update_enabled: bool = True
    update_frequency: UpdateFrequency = UpdateFrequency.WEEKLY


class CustomMarketCreate(CustomMarketBase):
    """Schema for creating a custom market"""
    company_id: Optional[UUID] = None
    created_by: Optional[str] = None


class CustomMarketUpdate(BaseModel):
    """Schema for updating a custom market"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    geographic_areas: Optional[dict] = None
    property_types: Optional[list] = None
    price_range_min: Optional[float] = None
    price_range_max: Optional[float] = None
    auto_update_enabled: Optional[bool] = None
    update_frequency: Optional[UpdateFrequency] = None


class CustomMarketResponse(CustomMarketBase):
    """Schema for custom market response"""
    id: UUID
    company_id: Optional[UUID]
    created_by: Optional[str]
    property_count: int
    avg_price: Optional[float]
    avg_price_per_sqft: Optional[float]
    avg_days_on_market: Optional[int]
    last_updated_at: Optional[datetime]
    next_update_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CompetitivePropertyBase(BaseModel):
    """Base schema for competitive property"""
    property_name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state_code: Optional[str] = None
    zip_code: Optional[str] = None
    property_type: Optional[str] = None
    units: Optional[int] = None
    year_built: Optional[int] = None
    square_footage: Optional[int] = None
    current_asking_rent: Optional[float] = None
    effective_rent: Optional[float] = None
    occupancy_rate: Optional[float] = None
    concessions_offered: Optional[str] = None
    amenities: Optional[dict] = None
    notes: Optional[str] = None


class CompetitivePropertyCreate(CompetitivePropertyBase):
    """Schema for creating competitive property"""
    market_id: UUID
    property_listing_id: Optional[int] = None


class CompetitivePropertyResponse(CompetitivePropertyBase):
    """Schema for competitive property response"""
    id: UUID
    market_id: UUID
    rent_per_sqft: Optional[float]
    first_tracked_date: Optional[date]
    last_data_update: Optional[datetime]
    tracking_status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RentTrendResponse(BaseModel):
    """Schema for rent trend analysis response"""
    id: UUID
    market_id: UUID
    analysis_date: date
    property_type: Optional[str]
    bedroom_count: Optional[int]
    avg_asking_rent: Optional[float]
    median_asking_rent: Optional[float]
    avg_effective_rent: Optional[float]
    avg_rent_per_sqft: Optional[float]
    mom_change_pct: Optional[float]
    yoy_change_pct: Optional[float]
    ytd_change_pct: Optional[float]
    property_count: Optional[int]
    forecast_30_days: Optional[float]
    forecast_60_days: Optional[float]
    forecast_90_days: Optional[float]
    insights: Optional[dict]
    created_at: datetime

    class Config:
        from_attributes = True


class SupplyDemandResponse(BaseModel):
    """Schema for supply/demand analysis response"""
    id: UUID
    market_id: UUID
    analysis_date: date
    property_type: Optional[str]
    total_inventory: Optional[int]
    new_construction_units: Optional[int]
    units_leased: Optional[int]
    absorption_rate: Optional[float]
    months_of_supply: Optional[float]
    avg_occupancy_rate: Optional[float]
    market_balance_score: Optional[float]
    rent_growth_rate: Optional[float]
    population_growth_rate: Optional[float]
    employment_growth_rate: Optional[float]
    supply_forecast_12mo: Optional[int]
    demand_forecast_12mo: Optional[int]
    insights: Optional[dict]
    created_at: datetime

    class Config:
        from_attributes = True


class CorrelationResponse(BaseModel):
    """Schema for economic indicator correlation response"""
    id: UUID
    market_id: UUID
    analysis_date: date
    indicator_name: str
    indicator_category: Optional[str]
    market_metric: str
    correlation_coefficient: Optional[float]
    r_squared: Optional[float]
    p_value: Optional[float]
    is_significant: Optional[bool]
    relationship_strength: Optional[str]
    relationship_direction: Optional[str]
    optimal_lag_days: Optional[int]
    interpretation: Optional[str]
    recommendations: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# ========================================
# CUSTOM MARKET ENDPOINTS
# ========================================

@router.post("/custom-markets", response_model=CustomMarketResponse, status_code=status.HTTP_201_CREATED)
async def create_custom_market(
    market_data: CustomMarketCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new custom market definition.

    - **name**: Market name
    - **market_type**: Type of market (geographic, competitive, portfolio, custom)
    - **geographic_areas**: ZIP codes, cities, MSAs to include
    - **property_types**: Property types to track
    - **price/size/year ranges**: Filtering criteria
    - **auto_update_enabled**: Enable automated updates
    - **update_frequency**: How often to update (daily, weekly, monthly, quarterly)
    """
    market = CustomMarket(**market_data.model_dump())

    # Set initial update time
    if market.auto_update_enabled:
        market.next_update_at = datetime.utcnow() + timedelta(days=1)

    db.add(market)
    db.commit()
    db.refresh(market)

    return market


@router.get("/custom-markets", response_model=List[CustomMarketResponse])
async def list_custom_markets(
    company_id: Optional[UUID] = Query(None),
    market_type: Optional[MarketType] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """
    List all custom markets with optional filtering.

    - **company_id**: Filter by company
    - **market_type**: Filter by market type
    """
    query = db.query(CustomMarket).filter(CustomMarket.deleted_at.is_(None))

    if company_id:
        query = query.filter(CustomMarket.company_id == company_id)

    if market_type:
        query = query.filter(CustomMarket.market_type == market_type)

    markets = query.order_by(CustomMarket.created_at.desc()).offset(skip).limit(limit).all()

    return markets


@router.get("/custom-markets/{market_id}", response_model=CustomMarketResponse)
async def get_custom_market(
    market_id: UUID,
    db: Session = Depends(get_db)
):
    """Get a specific custom market by ID"""
    market = db.query(CustomMarket).filter(
        CustomMarket.id == market_id,
        CustomMarket.deleted_at.is_(None)
    ).first()

    if not market:
        raise HTTPException(status_code=404, detail="Custom market not found")

    return market


@router.put("/custom-markets/{market_id}", response_model=CustomMarketResponse)
async def update_custom_market(
    market_id: UUID,
    market_data: CustomMarketUpdate,
    db: Session = Depends(get_db)
):
    """Update a custom market"""
    market = db.query(CustomMarket).filter(
        CustomMarket.id == market_id,
        CustomMarket.deleted_at.is_(None)
    ).first()

    if not market:
        raise HTTPException(status_code=404, detail="Custom market not found")

    update_data = market_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(market, field, value)

    db.commit()
    db.refresh(market)

    return market


@router.delete("/custom-markets/{market_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_custom_market(
    market_id: UUID,
    db: Session = Depends(get_db)
):
    """Delete a custom market (soft delete)"""
    market = db.query(CustomMarket).filter(
        CustomMarket.id == market_id,
        CustomMarket.deleted_at.is_(None)
    ).first()

    if not market:
        raise HTTPException(status_code=404, detail="Custom market not found")

    market.soft_delete()
    db.commit()

    return None


# ========================================
# COMPETITIVE PROPERTY ENDPOINTS
# ========================================

@router.post("/competitive-properties", response_model=CompetitivePropertyResponse, status_code=status.HTTP_201_CREATED)
async def add_competitive_property(
    property_data: CompetitivePropertyCreate,
    db: Session = Depends(get_db)
):
    """
    Add a property to track as part of competitive set.

    - Can link to existing PropertyListing or enter manually
    - Tracks rent, occupancy, concessions, amenities
    - Historical data stored for trend analysis
    """
    # Verify market exists
    market = db.query(CustomMarket).filter(CustomMarket.id == property_data.market_id).first()
    if not market:
        raise HTTPException(status_code=404, detail="Market not found")

    property_obj = CompetitiveProperty(**property_data.model_dump())
    property_obj.first_tracked_date = date.today()

    # Calculate rent per sqft if possible
    if property_obj.current_asking_rent and property_obj.square_footage:
        property_obj.rent_per_sqft = float(property_obj.current_asking_rent) / property_obj.square_footage

    db.add(property_obj)
    db.commit()
    db.refresh(property_obj)

    return property_obj


@router.get("/competitive-properties", response_model=List[CompetitivePropertyResponse])
async def list_competitive_properties(
    market_id: UUID = Query(..., description="Market ID to filter by"),
    tracking_status: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """List competitive properties for a market"""
    query = db.query(CompetitiveProperty).filter(CompetitiveProperty.market_id == market_id)

    if tracking_status:
        query = query.filter(CompetitiveProperty.tracking_status == tracking_status)

    properties = query.order_by(CompetitiveProperty.created_at.desc()).offset(skip).limit(limit).all()

    return properties


@router.put("/competitive-properties/{property_id}", response_model=CompetitivePropertyResponse)
async def update_competitive_property(
    property_id: UUID,
    property_data: CompetitivePropertyBase,
    db: Session = Depends(get_db)
):
    """Update competitive property data (manual tracking update)"""
    property_obj = db.query(CompetitiveProperty).filter(CompetitiveProperty.id == property_id).first()

    if not property_obj:
        raise HTTPException(status_code=404, detail="Property not found")

    update_data = property_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(property_obj, field, value)

    # Recalculate rent per sqft
    if property_obj.current_asking_rent and property_obj.square_footage:
        property_obj.rent_per_sqft = float(property_obj.current_asking_rent) / property_obj.square_footage

    property_obj.last_data_update = datetime.utcnow()

    db.commit()
    db.refresh(property_obj)

    return property_obj


# ========================================
# RENT TREND ANALYSIS ENDPOINTS
# ========================================

@router.get("/rent-trends", response_model=List[RentTrendResponse])
async def get_rent_trends(
    market_id: UUID = Query(..., description="Market ID"),
    property_type: Optional[str] = Query(None),
    bedroom_count: Optional[int] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """
    Get rent trend analysis for a market.

    - Historical rent changes
    - Month-over-month, year-over-year changes
    - Concessions tracking
    - Rent forecasts
    - Seasonality indicators
    """
    query = db.query(RentTrendAnalysis).filter(RentTrendAnalysis.market_id == market_id)

    if property_type:
        query = query.filter(RentTrendAnalysis.property_type == property_type)

    if bedroom_count is not None:
        query = query.filter(RentTrendAnalysis.bedroom_count == bedroom_count)

    if start_date:
        query = query.filter(RentTrendAnalysis.analysis_date >= start_date)

    if end_date:
        query = query.filter(RentTrendAnalysis.analysis_date <= end_date)

    trends = query.order_by(RentTrendAnalysis.analysis_date.desc()).offset(skip).limit(limit).all()

    return trends


@router.get("/rent-trends/latest", response_model=RentTrendResponse)
async def get_latest_rent_trend(
    market_id: UUID = Query(..., description="Market ID"),
    property_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get the most recent rent trend analysis for a market"""
    query = db.query(RentTrendAnalysis).filter(RentTrendAnalysis.market_id == market_id)

    if property_type:
        query = query.filter(RentTrendAnalysis.property_type == property_type)

    trend = query.order_by(RentTrendAnalysis.analysis_date.desc()).first()

    if not trend:
        raise HTTPException(status_code=404, detail="No rent trend data found for this market")

    return trend


# ========================================
# SUPPLY/DEMAND ANALYSIS ENDPOINTS
# ========================================

@router.get("/supply-demand", response_model=List[SupplyDemandResponse])
async def get_supply_demand_analysis(
    market_id: UUID = Query(..., description="Market ID"),
    property_type: Optional[str] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """
    Get supply/demand analysis for a market.

    - Inventory levels
    - Absorption rates
    - Months of supply
    - Construction pipeline
    - Occupancy trends
    - Market balance score
    - Population & employment correlations
    """
    query = db.query(SupplyDemandAnalysis).filter(SupplyDemandAnalysis.market_id == market_id)

    if property_type:
        query = query.filter(SupplyDemandAnalysis.property_type == property_type)

    if start_date:
        query = query.filter(SupplyDemandAnalysis.analysis_date >= start_date)

    if end_date:
        query = query.filter(SupplyDemandAnalysis.analysis_date <= end_date)

    analyses = query.order_by(SupplyDemandAnalysis.analysis_date.desc()).offset(skip).limit(limit).all()

    return analyses


@router.get("/supply-demand/latest", response_model=SupplyDemandResponse)
async def get_latest_supply_demand(
    market_id: UUID = Query(..., description="Market ID"),
    property_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get the most recent supply/demand analysis for a market"""
    query = db.query(SupplyDemandAnalysis).filter(SupplyDemandAnalysis.market_id == market_id)

    if property_type:
        query = query.filter(SupplyDemandAnalysis.property_type == property_type)

    analysis = query.order_by(SupplyDemandAnalysis.analysis_date.desc()).first()

    if not analysis:
        raise HTTPException(status_code=404, detail="No supply/demand data found for this market")

    return analysis


# ========================================
# ECONOMIC INDICATOR CORRELATION ENDPOINTS
# ========================================

@router.get("/correlations", response_model=List[CorrelationResponse])
async def get_economic_correlations(
    market_id: UUID = Query(..., description="Market ID"),
    market_metric: Optional[str] = Query(None, description="Market metric (rent, occupancy, price)"),
    indicator_category: Optional[str] = Query(None, description="Indicator category (employment, rates, housing)"),
    significant_only: bool = Query(False, description="Only show statistically significant correlations"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """
    Get correlations between economic indicators and market performance.

    - Identifies which economic factors influence the market
    - Statistical significance testing
    - Lag analysis (leading/lagging indicators)
    - Relationship strength and direction
    - Actionable insights and recommendations
    """
    query = db.query(EconomicIndicatorCorrelation).filter(
        EconomicIndicatorCorrelation.market_id == market_id
    )

    if market_metric:
        query = query.filter(EconomicIndicatorCorrelation.market_metric == market_metric)

    if indicator_category:
        query = query.filter(EconomicIndicatorCorrelation.indicator_category == indicator_category)

    if significant_only:
        query = query.filter(EconomicIndicatorCorrelation.is_significant == True)

    correlations = query.order_by(
        EconomicIndicatorCorrelation.correlation_coefficient.desc()
    ).offset(skip).limit(limit).all()

    return correlations


@router.get("/correlations/top-indicators", response_model=List[CorrelationResponse])
async def get_top_economic_indicators(
    market_id: UUID = Query(..., description="Market ID"),
    market_metric: str = Query(..., description="Market metric to analyze"),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get the top economic indicators most correlated with a specific market metric"""
    correlations = db.query(EconomicIndicatorCorrelation).filter(
        EconomicIndicatorCorrelation.market_id == market_id,
        EconomicIndicatorCorrelation.market_metric == market_metric,
        EconomicIndicatorCorrelation.is_significant == True
    ).order_by(
        func.abs(EconomicIndicatorCorrelation.correlation_coefficient).desc()
    ).limit(limit).all()

    return correlations


# ========================================
# MARKET UPDATE & AUTOMATION ENDPOINTS
# ========================================

@router.post("/markets/{market_id}/trigger-update", status_code=status.HTTP_202_ACCEPTED)
async def trigger_market_update(
    market_id: UUID,
    update_rent_trends: bool = Query(True),
    update_supply_demand: bool = Query(True),
    update_correlations: bool = Query(False),
    db: Session = Depends(get_db)
):
    """
    Manually trigger a market data update.

    This endpoint queues an update job. In production, this would:
    - Fetch latest property listing data
    - Recalculate rent trends
    - Update supply/demand metrics
    - Recalculate economic correlations (if requested)

    Returns immediately with a job ID (implementation TBD).
    """
    market = db.query(CustomMarket).filter(CustomMarket.id == market_id).first()
    if not market:
        raise HTTPException(status_code=404, detail="Market not found")

    # In production, this would queue a background job
    # For now, just update the timestamp
    market.last_updated_at = datetime.utcnow()
    market.next_update_at = datetime.utcnow() + timedelta(
        days=7 if market.update_frequency == UpdateFrequency.WEEKLY else 30
    )

    db.commit()

    return {
        "status": "accepted",
        "message": "Market update queued",
        "market_id": market_id,
        "estimated_completion": "5-10 minutes"
    }


@router.get("/markets/{market_id}/update-status")
async def get_market_update_status(
    market_id: UUID,
    db: Session = Depends(get_db)
):
    """Get the update status and schedule for a market"""
    market = db.query(CustomMarket).filter(CustomMarket.id == market_id).first()
    if not market:
        raise HTTPException(status_code=404, detail="Market not found")

    schedule = db.query(MarketUpdateSchedule).filter(
        MarketUpdateSchedule.market_id == market_id
    ).first()

    return {
        "market_id": market_id,
        "market_name": market.name,
        "auto_update_enabled": market.auto_update_enabled,
        "update_frequency": market.update_frequency,
        "last_updated_at": market.last_updated_at,
        "next_update_at": market.next_update_at,
        "schedule": {
            "total_runs": schedule.total_runs if schedule else 0,
            "successful_runs": schedule.successful_runs if schedule else 0,
            "failed_runs": schedule.failed_runs if schedule else 0,
            "last_run_status": schedule.last_run_status if schedule else None,
        } if schedule else None
    }
