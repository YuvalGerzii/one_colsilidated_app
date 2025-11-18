"""
Enhanced Market Intelligence Models

Advanced market analysis features:
- Custom market definitions
- Competitive set tracking
- Automated market updates
- Rent trend analysis
- Supply/demand modeling
- Economic indicator correlations
"""

from datetime import datetime, date
from typing import Optional
from decimal import Decimal

from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Date, Text,
    Boolean, JSON, Numeric, ForeignKey, Index, Enum as SQLEnum
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base
from app.models.database import UUIDMixin, TimestampMixin, SoftDeleteMixin


class MarketType(str, enum.Enum):
    """Types of custom markets"""
    GEOGRAPHIC = "geographic"  # ZIP code, city, MSA
    COMPETITIVE = "competitive"  # Competitive set
    PORTFOLIO = "portfolio"  # User's properties
    CUSTOM = "custom"  # Custom definition


class UpdateFrequency(str, enum.Enum):
    """Frequency for automated updates"""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"


class CustomMarket(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    User-defined custom markets for analysis.

    Allows users to create custom market definitions based on:
    - Geographic areas (ZIP codes, cities, MSAs)
    - Property types and characteristics
    - Custom criteria
    """
    __tablename__ = "custom_markets"

    # Basic Information
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    market_type = Column(SQLEnum(MarketType), nullable=False, default=MarketType.CUSTOM)

    # User/Company association
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=True, index=True)
    created_by = Column(String(200))

    # Market Definition
    geographic_areas = Column(JSON)  # List of ZIP codes, cities, counties, MSAs
    property_types = Column(JSON)  # Property types to include

    # Criteria filters
    price_range_min = Column(Numeric(15, 2))
    price_range_max = Column(Numeric(15, 2))
    size_range_min = Column(Integer)  # sqft
    size_range_max = Column(Integer)  # sqft
    year_built_min = Column(Integer)
    year_built_max = Column(Integer)

    # Custom criteria (JSON for flexibility)
    custom_criteria = Column(JSON)

    # Automation
    auto_update_enabled = Column(Boolean, default=True)
    update_frequency = Column(SQLEnum(UpdateFrequency), default=UpdateFrequency.WEEKLY)
    last_updated_at = Column(DateTime(timezone=True))
    next_update_at = Column(DateTime(timezone=True))

    # Statistics (cached for performance)
    property_count = Column(Integer, default=0)
    avg_price = Column(Numeric(15, 2))
    avg_price_per_sqft = Column(Numeric(10, 2))
    avg_days_on_market = Column(Integer)

    # Relationships
    competitive_properties = relationship(
        "CompetitiveProperty",
        back_populates="market",
        cascade="all, delete-orphan"
    )

    rent_trends = relationship(
        "RentTrendAnalysis",
        back_populates="market",
        cascade="all, delete-orphan"
    )

    supply_demand_analyses = relationship(
        "SupplyDemandAnalysis",
        back_populates="market",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index('idx_custom_market_company', 'company_id', 'deleted_at'),
        Index('idx_custom_market_type', 'market_type'),
    )


class CompetitiveProperty(Base, UUIDMixin, TimestampMixin):
    """
    Properties tracked as part of competitive set analysis.

    Links to PropertyListing for data, adds custom tracking.
    """
    __tablename__ = "competitive_properties"

    # Market association
    market_id = Column(UUID(as_uuid=True), ForeignKey("custom_markets.id"), nullable=False, index=True)
    market = relationship("CustomMarket", back_populates="competitive_properties")

    # Property identification (could link to PropertyListing or be manual entry)
    property_listing_id = Column(Integer, ForeignKey("property_listings.id"), nullable=True)

    # Manual entry fields (if not from PropertyListing)
    property_name = Column(String(300))
    address = Column(String(300))
    city = Column(String(100))
    state_code = Column(String(2))
    zip_code = Column(String(10), index=True)

    # Property details
    property_type = Column(String(50))
    units = Column(Integer)
    year_built = Column(Integer)
    square_footage = Column(Integer)

    # Pricing data
    current_asking_rent = Column(Numeric(10, 2))
    effective_rent = Column(Numeric(10, 2))  # After concessions
    rent_per_sqft = Column(Numeric(10, 2))

    # Occupancy & performance
    occupancy_rate = Column(Numeric(5, 2))
    concessions_offered = Column(Text)
    amenities = Column(JSON)

    # Tracking
    first_tracked_date = Column(Date)
    last_data_update = Column(DateTime(timezone=True))
    tracking_status = Column(String(50), default="active")  # active, inactive, sold

    # Historical data points (for trend analysis)
    historical_data = Column(JSON)

    # Notes
    notes = Column(Text)
    competitive_advantages = Column(Text)
    competitive_disadvantages = Column(Text)

    __table_args__ = (
        Index('idx_comp_prop_market', 'market_id', 'tracking_status'),
        Index('idx_comp_prop_zip', 'zip_code'),
    )


class RentTrendAnalysis(Base, UUIDMixin, TimestampMixin):
    """
    Rent trend analysis for custom markets.

    Tracks historical rent changes, seasonality, and forecasts.
    """
    __tablename__ = "rent_trend_analyses"

    # Market association
    market_id = Column(UUID(as_uuid=True), ForeignKey("custom_markets.id"), nullable=False, index=True)
    market = relationship("CustomMarket", back_populates="rent_trends")

    # Time period
    analysis_date = Column(Date, nullable=False, index=True)
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)

    # Property type segment (optional)
    property_type = Column(String(50), index=True)
    bedroom_count = Column(Integer)  # null = all

    # Rent statistics
    avg_asking_rent = Column(Numeric(10, 2))
    median_asking_rent = Column(Numeric(10, 2))
    avg_effective_rent = Column(Numeric(10, 2))
    avg_rent_per_sqft = Column(Numeric(10, 2))

    # Percentiles
    rent_25th_percentile = Column(Numeric(10, 2))
    rent_75th_percentile = Column(Numeric(10, 2))
    rent_90th_percentile = Column(Numeric(10, 2))

    # Change metrics
    mom_change_pct = Column(Numeric(5, 2))  # Month-over-month
    yoy_change_pct = Column(Numeric(5, 2))  # Year-over-year
    ytd_change_pct = Column(Numeric(5, 2))  # Year-to-date

    # Sample size
    property_count = Column(Integer)
    active_listings_count = Column(Integer)

    # Concessions
    avg_concession_value = Column(Numeric(10, 2))
    pct_with_concessions = Column(Numeric(5, 2))

    # Forecast (if generated)
    forecast_30_days = Column(Numeric(10, 2))
    forecast_60_days = Column(Numeric(10, 2))
    forecast_90_days = Column(Numeric(10, 2))
    forecast_confidence = Column(Numeric(5, 2))

    # Seasonality
    seasonal_index = Column(Numeric(5, 2))  # 100 = average, >100 = above average

    # Additional insights
    insights = Column(JSON)  # Flexible storage for analysis insights

    __table_args__ = (
        Index('idx_rent_trend_market_date', 'market_id', 'analysis_date'),
        Index('idx_rent_trend_property_type', 'property_type', 'bedroom_count'),
    )


class SupplyDemandAnalysis(Base, UUIDMixin, TimestampMixin):
    """
    Supply and demand modeling for markets.

    Analyzes inventory levels, absorption rates, and demand signals.
    """
    __tablename__ = "supply_demand_analyses"

    # Market association
    market_id = Column(UUID(as_uuid=True), ForeignKey("custom_markets.id"), nullable=False, index=True)
    market = relationship("CustomMarket", back_populates="supply_demand_analyses")

    # Time period
    analysis_date = Column(Date, nullable=False, index=True)
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)

    # Property type segment
    property_type = Column(String(50), index=True)

    # Supply metrics
    total_inventory = Column(Integer)
    new_construction_units = Column(Integer)
    units_under_construction = Column(Integer)
    planned_units = Column(Integer)

    # Listing activity
    new_listings = Column(Integer)
    delisted_units = Column(Integer)
    avg_days_on_market = Column(Integer)

    # Demand metrics
    units_leased = Column(Integer)
    lease_applications = Column(Integer)
    showing_requests = Column(Integer)

    # Absorption
    absorption_rate = Column(Numeric(10, 2))  # Units per month
    months_of_supply = Column(Numeric(5, 2))  # Months at current absorption rate

    # Occupancy
    avg_occupancy_rate = Column(Numeric(5, 2))
    occupancy_change_mom = Column(Numeric(5, 2))

    # Price pressure indicators
    rent_growth_rate = Column(Numeric(5, 2))
    concession_rate = Column(Numeric(5, 2))  # % of properties offering concessions
    price_cuts_count = Column(Integer)
    price_increases_count = Column(Integer)

    # Market balance score (-100 to +100)
    # Negative = oversupply, Positive = undersupply
    market_balance_score = Column(Numeric(6, 2))

    # Population & employment (from Census/BLS integration)
    population_growth_rate = Column(Numeric(5, 2))
    employment_growth_rate = Column(Numeric(5, 2))
    unemployment_rate = Column(Numeric(5, 2))

    # Forecast
    supply_forecast_12mo = Column(Integer)
    demand_forecast_12mo = Column(Integer)

    # Analysis details
    methodology = Column(String(100))
    confidence_level = Column(Numeric(5, 2))
    data_quality_score = Column(Numeric(5, 2))

    # Insights
    insights = Column(JSON)

    __table_args__ = (
        Index('idx_supply_demand_market_date', 'market_id', 'analysis_date'),
        Index('idx_supply_demand_type', 'property_type'),
    )


class EconomicIndicatorCorrelation(Base, UUIDMixin, TimestampMixin):
    """
    Correlations between economic indicators and market performance.

    Helps identify which economic factors most influence local markets.
    """
    __tablename__ = "economic_indicator_correlations"

    # Market association
    market_id = Column(UUID(as_uuid=True), ForeignKey("custom_markets.id"), nullable=False, index=True)

    # Analysis metadata
    analysis_date = Column(Date, nullable=False, index=True)
    lookback_period_days = Column(Integer, nullable=False)  # Period analyzed

    # Indicator identification
    indicator_source = Column(String(50), nullable=False)  # FRED, BLS, Census, etc.
    indicator_id = Column(String(100), nullable=False)  # Series ID or metric name
    indicator_name = Column(String(200), nullable=False)
    indicator_category = Column(String(50))  # employment, rates, housing, etc.

    # Market metric being correlated
    market_metric = Column(String(100), nullable=False)  # rent, occupancy, price, etc.

    # Correlation statistics
    correlation_coefficient = Column(Numeric(5, 4))  # Pearson correlation (-1 to 1)
    r_squared = Column(Numeric(5, 4))  # Coefficient of determination
    p_value = Column(Numeric(10, 8))  # Statistical significance
    is_significant = Column(Boolean)  # p < 0.05

    # Relationship characteristics
    relationship_strength = Column(String(20))  # weak, moderate, strong
    relationship_direction = Column(String(20))  # positive, negative, none

    # Lag analysis (does indicator lead/lag market metric?)
    optimal_lag_days = Column(Integer)  # Best correlation at this lag
    lag_correlation = Column(Numeric(5, 4))  # Correlation at optimal lag

    # Time period details
    data_points_count = Column(Integer)
    period_start = Column(Date)
    period_end = Column(Date)

    # Additional statistics
    indicator_mean = Column(Numeric(20, 6))
    indicator_std_dev = Column(Numeric(20, 6))
    market_metric_mean = Column(Numeric(20, 6))
    market_metric_std_dev = Column(Numeric(20, 6))

    # Insights
    interpretation = Column(Text)
    recommendations = Column(Text)

    __table_args__ = (
        Index('idx_econ_corr_market_date', 'market_id', 'analysis_date'),
        Index('idx_econ_corr_indicator', 'indicator_source', 'indicator_id'),
        Index('idx_econ_corr_significance', 'is_significant', 'correlation_coefficient'),
    )


class MarketUpdateSchedule(Base, UUIDMixin, TimestampMixin):
    """
    Automated market update scheduling and tracking.
    """
    __tablename__ = "market_update_schedules"

    # Market association
    market_id = Column(UUID(as_uuid=True), ForeignKey("custom_markets.id"), nullable=False, index=True)

    # Schedule configuration
    is_enabled = Column(Boolean, default=True)
    update_frequency = Column(SQLEnum(UpdateFrequency), nullable=False)

    # Update scope
    update_competitive_data = Column(Boolean, default=True)
    update_rent_trends = Column(Boolean, default=True)
    update_supply_demand = Column(Boolean, default=True)
    update_correlations = Column(Boolean, default=False)  # More expensive

    # Timing
    last_run_at = Column(DateTime(timezone=True))
    next_run_at = Column(DateTime(timezone=True), index=True)

    # Execution tracking
    total_runs = Column(Integer, default=0)
    successful_runs = Column(Integer, default=0)
    failed_runs = Column(Integer, default=0)
    last_run_duration_seconds = Column(Integer)

    # Last run results
    last_run_status = Column(String(50))  # success, failed, partial
    last_run_error = Column(Text)
    last_run_records_updated = Column(Integer)

    # Notifications
    notify_on_completion = Column(Boolean, default=False)
    notify_on_failure = Column(Boolean, default=True)
    notification_email = Column(String(200))

    __table_args__ = (
        Index('idx_update_schedule_next_run', 'is_enabled', 'next_run_at'),
    )
