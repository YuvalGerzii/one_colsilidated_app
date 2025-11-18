"""
Import Market Intelligence CSV Files

Imports three types of market intelligence data:
1. Geographic economic indicators (NYC, Miami metro data)
2. Real estate market data (cap rates, rents, vacancy)
3. Comparable property transactions

Usage:
    python -m app.scripts.import_market_intelligence_csv
"""

import sys
import logging
import csv
from pathlib import Path
from datetime import datetime, date
from decimal import Decimal
from typing import List, Dict, Any, Optional

from sqlalchemy import Column, Integer, String, Float, DateTime, Date, Text, Numeric, JSON, Index
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.core.database import Base, engine, SessionLocal

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ========================================
# DATABASE MODELS
# ========================================

class GeographicEconomicIndicator(Base):
    """Geographic economic indicators for metro areas"""
    __tablename__ = "geographic_economic_indicators"

    id = Column(Integer, primary_key=True, index=True)

    # Geographic info
    geography = Column(String(100), nullable=False, index=True)
    geography_type = Column(String(50), nullable=False, index=True)  # Metro, Borough, County

    # Indicator info
    indicator_name = Column(String(200), nullable=False, index=True)
    indicator_value = Column(Numeric(20, 6), nullable=False)
    indicator_unit = Column(String(50), nullable=False)

    # Time period
    period = Column(Date, nullable=True, index=True)
    period_type = Column(String(50))  # annual, monthly, daily, 5-year, 10-year

    # Metadata
    data_source = Column(String(200))
    notes = Column(Text)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index('idx_geo_indicator', 'geography', 'indicator_name', 'period'),
    )


class RealEstateMarketData(Base):
    """Real estate market metrics by market, submarket, and property type"""
    __tablename__ = "real_estate_market_data"

    id = Column(Integer, primary_key=True, index=True)

    # Location info
    market_name = Column(String(100), nullable=False, index=True)
    submarket_name = Column(String(100), index=True)

    # Property info
    property_type = Column(String(50), nullable=False, index=True)
    property_class = Column(String(50), index=True)  # A, B, C, Full Service, Limited Service, etc.

    # Metric info
    metric_name = Column(String(200), nullable=False, index=True)
    metric_value = Column(Numeric(20, 6), nullable=False)
    metric_unit = Column(String(50), nullable=False)

    # Time period
    period = Column(Date, nullable=False, index=True)

    # Metadata
    data_source = Column(String(200))
    confidence_level = Column(String(20))  # high, medium, low
    notes = Column(Text)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index('idx_market_metric', 'market_name', 'property_type', 'metric_name', 'period'),
    )


class ComparableTransaction(Base):
    """Comparable property sales transactions"""
    __tablename__ = "comparable_transactions"

    id = Column(Integer, primary_key=True, index=True)

    # Property location
    address = Column(String(300))
    city = Column(String(100), nullable=False, index=True)
    submarket = Column(String(100), index=True)
    state = Column(String(2), nullable=False, index=True)
    zip_code = Column(String(10), index=True)

    # Property info
    property_type = Column(String(50), nullable=False, index=True)
    property_class = Column(String(50), index=True)  # A, B, C, Full Service, Limited Service, etc.

    # Sale info
    sale_date = Column(Date, nullable=False, index=True)
    sale_price = Column(Numeric(20, 2))
    price_per_unit = Column(Numeric(15, 2))
    price_per_sf = Column(Numeric(10, 2))
    cap_rate = Column(Numeric(5, 4))

    # Property details
    units = Column(Integer)
    total_sf = Column(Integer)
    lot_size_sf = Column(Integer)
    year_built = Column(Integer)
    year_renovated = Column(Integer)
    num_buildings = Column(Integer)
    num_floors = Column(Integer)
    parking_spaces = Column(Integer)

    # Financial details
    noi = Column(Numeric(20, 2))
    gross_potential_rent = Column(Numeric(20, 2))
    occupancy_at_sale = Column(Numeric(5, 4))
    inplace_vs_market_rent_pct = Column(Numeric(5, 2))  # Percentages like 51.7

    # Transaction details
    buyer = Column(String(200))
    buyer_type = Column(String(100))
    seller = Column(String(200))
    seller_type = Column(String(100))
    broker = Column(String(200))
    financing_type = Column(String(50))
    ltv = Column(Numeric(5, 4))
    lender = Column(String(200))
    interest_rate = Column(Numeric(5, 4))
    deal_type = Column(String(50), index=True)  # Arms Length, Foreclosure, Portfolio, etc.
    special_conditions = Column(String(200))

    # Metadata
    data_source = Column(String(200))
    source_url = Column(Text)
    notes = Column(Text)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index('idx_comp_trans', 'city', 'property_type', 'sale_date'),
    )


class HotZoneMarket(Base):
    """Hot zones and emerging markets analysis"""
    __tablename__ = "hot_zone_markets"

    id = Column(Integer, primary_key=True, index=True)

    # Location info
    market_name = Column(String(200), nullable=False, index=True)
    neighborhood_name = Column(String(200), nullable=False, index=True)
    hot_zone_rank = Column(Integer, index=True)

    # Metric info
    metric_category = Column(String(100), nullable=False, index=True)
    metric_name = Column(String(200), nullable=False, index=True)
    metric_value = Column(Numeric(20, 6), nullable=True)
    metric_unit = Column(String(50), nullable=False)

    # Time period
    period = Column(Date, nullable=True, index=True)

    # Comparison
    comparison_to_city_average = Column(String(50))

    # Metadata
    data_source = Column(String(200))
    notes = Column(Text)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index('idx_hot_zone', 'market_name', 'neighborhood_name', 'hot_zone_rank'),
    )


class NeighborhoodScore(Base):
    """Neighborhood scoring and ranking analysis"""
    __tablename__ = "neighborhood_scores"

    id = Column(Integer, primary_key=True, index=True)

    # Location info
    market_name = Column(String(200), nullable=False, index=True)
    neighborhood_name = Column(String(200), nullable=False, index=True)

    # Score info
    score_category = Column(String(100), nullable=False, index=True)
    score_value = Column(Numeric(10, 4), nullable=False)
    rank_within_market = Column(Integer)
    rank_nationally = Column(Integer)

    # Time period
    period = Column(Date, nullable=True, index=True)

    # Metadata
    data_source = Column(String(200))
    notes = Column(Text)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index('idx_neighborhood_score', 'market_name', 'neighborhood_name', 'score_category'),
    )


# ========================================
# STR (SHORT-TERM RENTAL) MODELS
# ========================================

class STRHotNeighborhood(Base):
    """STR hot neighborhoods for investment"""
    __tablename__ = "str_hot_neighborhoods"

    id = Column(Integer, primary_key=True, index=True)
    market = Column(String(100), nullable=False, index=True)
    neighborhood_rank = Column(Integer, index=True)
    neighborhood_name = Column(String(200), nullable=False, index=True)
    avg_annual_revenue_per_listing = Column(Numeric(15, 2))
    avg_occupancy_rate_pct = Column(Numeric(5, 2))  # Changed from (5,4) to (5,2) to support values like 72.0
    avg_revpar = Column(Numeric(10, 2))
    growth_stage = Column(String(50), index=True)
    revenue_category = Column(String(50), index=True)
    data_source = Column(String(200))
    analysis_date = Column(Date, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index('idx_str_hot_neighborhood', 'market', 'neighborhood_rank'),
    )


class STRPerformanceMetrics(Base):
    """STR performance metrics by property type"""
    __tablename__ = "str_performance_metrics"

    id = Column(Integer, primary_key=True, index=True)
    market = Column(String(100), nullable=False, index=True)
    property_type = Column(String(50), nullable=False, index=True)
    adr_daily = Column(Numeric(10, 2))
    occupancy_rate_pct = Column(Numeric(5, 2))  # Percentages like 51.7
    revpar = Column(Numeric(10, 2))
    monthly_revenue_avg = Column(Numeric(15, 2))
    annual_revenue_avg = Column(Numeric(15, 2))
    booking_lead_time_days = Column(Integer)
    avg_length_of_stay_nights = Column(Numeric(5, 2))
    review_score = Column(Numeric(3, 2))
    data_source = Column(String(200))
    period = Column(Date, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index('idx_str_performance', 'market', 'property_type', 'period'),
    )


class STRMarketOverview(Base):
    """STR market overview and statistics"""
    __tablename__ = "str_market_overview"

    id = Column(Integer, primary_key=True, index=True)
    market = Column(String(100), nullable=False, index=True)
    total_str_listings = Column(Integer)
    active_listings_30days = Column(Integer)
    entire_home_apt_count = Column(Integer)
    entire_home_pct = Column(Numeric(5, 2))  # Percentages like 51.7
    private_shared_room_count = Column(Integer)
    private_shared_room_pct = Column(Numeric(5, 2))  # Percentages like 51.7
    str_pct_of_housing_stock = Column(Numeric(5, 2))  # Percentages like 51.7
    inventory_growth_yoy_pct = Column(Numeric(5, 2))  # Percentages like 51.7
    avg_listing_age_months = Column(Numeric(5, 2))
    host_concentration_10plus_pct = Column(Numeric(5, 2))  # Percentages like 51.7
    data_source = Column(String(200))
    analysis_date = Column(Date, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class STRRegulatoryEnvironment(Base):
    """STR regulatory environment by market"""
    __tablename__ = "str_regulatory_environment"

    id = Column(Integer, primary_key=True, index=True)
    market = Column(String(100), nullable=False, index=True)
    regulation_type = Column(String(100), index=True)
    registration_required = Column(String(10))
    license_permit_required = Column(String(10))
    license_cost_usd = Column(Numeric(10, 2))
    primary_residence_requirement = Column(String(10))
    max_rental_days_per_year = Column(Integer)
    occupancy_tax_rate_pct = Column(Numeric(5, 2))  # Percentages like 51.7
    platform_collects_taxes = Column(String(10))
    enforcement_level = Column(String(50), index=True)
    fine_per_violation_usd = Column(Numeric(10, 2))
    data_source = Column(String(200))
    effective_date = Column(Date, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


# ========================================
# ZONING MODELS
# ========================================

class ZoningDistrict(Base):
    """Zoning districts inventory"""
    __tablename__ = "zoning_districts"

    id = Column(Integer, primary_key=True, index=True)
    market = Column(String(100), nullable=False, index=True)
    zone_type = Column(String(100), nullable=False, index=True)
    zone_code = Column(String(50), index=True)
    max_far = Column(Numeric(5, 2))
    max_height_feet = Column(Integer)
    min_lot_size_sf = Column(Integer)
    parking_requirement = Column(String(200))
    setback_front_feet = Column(Integer)
    use_restrictions = Column(Text)
    data_source = Column(String(200))
    effective_date = Column(Date, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index('idx_zoning_district', 'market', 'zone_type', 'zone_code'),
    )


class ZoningReform(Base):
    """Zoning changes and reforms"""
    __tablename__ = "zoning_reforms"

    id = Column(Integer, primary_key=True, index=True)
    market = Column(String(100), nullable=False, index=True)
    reform_name = Column(String(200), nullable=False)
    area_affected = Column(String(200))
    old_zoning = Column(String(100))
    new_zoning = Column(String(100))
    effective_date = Column(Date, index=True)
    units_enabled = Column(Integer)
    description = Column(Text)
    data_source = Column(String(200))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class OpportunityZone(Base):
    """Opportunity zones data"""
    __tablename__ = "opportunity_zones"

    id = Column(Integer, primary_key=True, index=True)
    market = Column(String(100), nullable=False, index=True)
    num_opportunity_zones = Column(Integer)
    total_acres_in_oz = Column(Numeric(15, 2))
    investment_in_oz_mm = Column(Numeric(15, 2))
    development_projects_in_oz = Column(Integer)
    oz_residential_units = Column(Integer)
    oz_commercial_sf = Column(Integer)
    avg_cap_rate_compression_bps = Column(Integer)
    oz_designation_date = Column(Date)
    data_source = Column(String(200))
    period = Column(Date, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class UnderbuiltParcel(Base):
    """Underbuilt parcels analysis"""
    __tablename__ = "underbuilt_parcels"

    id = Column(Integer, primary_key=True, index=True)
    market = Column(String(100), nullable=False, index=True)
    zone_type = Column(String(100), index=True)
    num_underbuilt_parcels = Column(Integer)
    avg_current_far = Column(Numeric(5, 2))
    avg_max_allowed_far = Column(Numeric(5, 2))
    far_gap = Column(Numeric(5, 2))
    avg_current_height_feet = Column(Integer)
    avg_max_height_feet = Column(Integer)
    avg_parcel_size_sf = Column(Integer)
    avg_parcel_size_acres = Column(Numeric(10, 2))
    total_additional_developable_sf = Column(Integer)
    estimated_additional_units_possible = Column(Integer)
    data_source = Column(String(200))
    analysis_date = Column(Date, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


# ========================================
# DEVELOPMENT/LAND MODELS
# ========================================

class DevelopmentPipeline(Base):
    """Development pipeline by zone"""
    __tablename__ = "development_pipeline"

    id = Column(Integer, primary_key=True, index=True)
    market = Column(String(100), nullable=False, index=True)
    zone_type = Column(String(100), index=True)
    projects_under_construction = Column(Integer)
    units_under_construction = Column(Integer)
    sf_under_construction = Column(Integer)
    permits_issued_ytd_2024 = Column(Integer)
    units_permitted_ytd = Column(Integer)
    sf_permitted_ytd = Column(Integer)
    permit_value_mm = Column(Numeric(15, 2))
    applications_pending = Column(Integer)
    avg_approval_timeline_months = Column(Numeric(5, 2))
    approval_success_rate_pct = Column(Numeric(5, 2))  # Percentages like 51.7
    data_source = Column(String(200))
    period = Column(Date, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class LandCostEconomics(Base):
    """Land costs and economics"""
    __tablename__ = "land_cost_economics"

    id = Column(Integer, primary_key=True, index=True)
    market = Column(String(100), nullable=False, index=True)
    zone_type = Column(String(100), index=True)
    land_price_per_sf = Column(Numeric(10, 2))
    land_price_per_developable_sf = Column(Numeric(10, 2))
    land_as_pct_of_total_cost = Column(Numeric(5, 2))  # Percentages like 51.7
    estimated_construction_cost_per_sf = Column(Numeric(10, 2))
    pro_forma_yield_on_cost_pct = Column(Numeric(5, 2))  # Percentages like 51.7
    data_source = Column(String(200))
    period = Column(Date, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


# ========================================
# OTHER MODELS
# ========================================

class PropertyTaxAssessment(Base):
    """Property tax assessments across 15 markets"""
    __tablename__ = "property_tax_assessments"

    id = Column(Integer, primary_key=True, index=True)
    market = Column(String(100), nullable=False, index=True)
    geography_type = Column(String(50), index=True)
    indicator_name = Column(String(200), nullable=False, index=True)
    indicator_value = Column(Numeric(20, 6))
    indicator_unit = Column(String(50))
    data_source = Column(String(200))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class TenantCreditQuality(Base):
    """Tenant credit quality and performance"""
    __tablename__ = "tenant_credit_quality"

    id = Column(Integer, primary_key=True, index=True)
    tenant_name = Column(String(200), nullable=False, index=True)
    ticker = Column(String(20), index=True)
    category = Column(String(100), index=True)
    company_name = Column(String(200))
    moodys_rating = Column(String(10))
    sp_rating = Column(String(10))
    metric_name = Column(String(200), nullable=False, index=True)
    metric_value = Column(Numeric(20, 6))
    unit = Column(String(50))
    data_source = Column(String(200))
    period = Column(Date, index=True)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index('idx_tenant_credit', 'tenant_name', 'metric_name', 'period'),
    )


# ========================================
# FINANCIAL MARKETS TIME-SERIES MODELS
# ========================================

class TimeSeriesIndicator(Base):
    """Unified time-series indicator model for financial/economic data"""
    __tablename__ = "time_series_indicators"

    id = Column(Integer, primary_key=True, index=True)

    # Time period
    date = Column(Date, nullable=True, index=True)  # Nullable for quarterly data without specific dates
    period_type = Column(String(50), index=True)  # quarterly, monthly, daily, annual

    # Indicator info
    indicator_name = Column(String(200), nullable=False, index=True)
    indicator_value = Column(Numeric(20, 6))
    indicator_unit = Column(String(50))

    # Source category (to differentiate which CSV this came from)
    source_category = Column(String(100), nullable=False, index=True)

    # Metadata
    data_source = Column(String(200))
    notes = Column(Text)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index('idx_timeseries', 'date', 'indicator_name', 'source_category'),
    )


# ========================================
# STR DEEP DIVE MODELS
# ========================================

class STRCompetitiveAnalysis(Base):
    """STR vs LTR competitive analysis"""
    __tablename__ = "str_competitive_analysis"

    id = Column(Integer, primary_key=True, index=True)
    market = Column(String(200), nullable=False, index=True)
    str_adr_daily = Column(Numeric(10, 2))
    str_monthly_equivalent_adr_x30 = Column(Numeric(15, 2))
    ltr_monthly_rent = Column(Numeric(15, 2))
    str_adr_vs_ltr_difference = Column(Numeric(15, 2))
    str_profitability_advantage = Column(Numeric(15, 2))
    breakeven_occupancy_rate_pct = Column(Numeric(5, 2))
    str_implied_cap_rate_pct = Column(Numeric(5, 2))
    ltr_implied_cap_rate_pct = Column(Numeric(5, 2))
    cap_rate_advantage_basis_points = Column(Numeric(10, 2))
    data_source = Column(String(200))
    period = Column(String(50), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class STRComplianceEnforcement(Base):
    """STR compliance and enforcement metrics"""
    __tablename__ = "str_compliance_enforcement"

    id = Column(Integer, primary_key=True, index=True)
    market = Column(String(200), nullable=False, index=True)
    regulation_type = Column(String(100))
    enforcement_level = Column(String(50), index=True)
    violations_issued = Column(Integer)
    fines_collected_usd = Column(Numeric(15, 2))
    avg_fine_per_violation_usd = Column(Numeric(10, 2))
    compliance_rate_pct = Column(Numeric(5, 2))
    registered_hosts_count = Column(Integer)
    unregistered_hosts_count = Column(Integer)
    platform_cooperation_level = Column(String(50))
    data_source = Column(String(200))
    period = Column(Date, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class STRGuestDemographics(Base):
    """STR guest demographics and behavior"""
    __tablename__ = "str_guest_demographics"

    id = Column(Integer, primary_key=True, index=True)
    market = Column(String(200), nullable=False, index=True)
    guest_origin = Column(String(100), index=True)  # domestic, international
    avg_group_size = Column(Numeric(5, 2))
    avg_age_range = Column(String(50))
    purpose_of_visit = Column(String(100), index=True)  # leisure, business
    avg_booking_value_usd = Column(Numeric(10, 2))
    avg_length_of_stay_nights = Column(Numeric(5, 2))
    repeat_guest_rate_pct = Column(Numeric(5, 2))
    review_participation_rate_pct = Column(Numeric(5, 2))
    avg_review_score = Column(Numeric(3, 2))
    data_source = Column(String(200))
    period = Column(Date, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class STRHostEconomics(Base):
    """STR host economics and profitability"""
    __tablename__ = "str_host_economics"

    id = Column(Integer, primary_key=True, index=True)
    market = Column(String(200), nullable=False, index=True)
    host_type = Column(String(100), index=True)  # individual, professional, corporate
    avg_annual_revenue_per_listing = Column(Numeric(15, 2))
    avg_monthly_revenue_per_listing = Column(Numeric(15, 2))
    avg_occupancy_rate_pct = Column(Numeric(5, 2))
    avg_nightly_rate = Column(Numeric(10, 2))
    operating_expenses_pct_of_revenue = Column(Numeric(5, 2))
    platform_fees_pct = Column(Numeric(5, 2))
    cleaning_fees_avg = Column(Numeric(10, 2))
    estimated_net_margin_pct = Column(Numeric(5, 2))
    time_to_profitability_months = Column(Integer)
    data_source = Column(String(200))
    period = Column(Date, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class STRHousingMarketImpact(Base):
    """STR impact on housing market"""
    __tablename__ = "str_housing_market_impact"

    id = Column(Integer, primary_key=True, index=True)
    market = Column(String(200), nullable=False, index=True)
    str_listings_count = Column(Integer)
    str_pct_of_housing_stock = Column(Numeric(5, 2))
    ltr_units_lost_to_str = Column(Integer)
    estimated_rent_increase_pct = Column(Numeric(5, 2))
    estimated_home_price_increase_pct = Column(Numeric(5, 2))
    neighborhoods_most_impacted = Column(Text)
    housing_affordability_index_change = Column(Numeric(10, 2))
    vacancy_rate_ltr_pct = Column(Numeric(5, 2))
    vacancy_rate_str_pct = Column(Numeric(5, 2))
    data_source = Column(String(200))
    period = Column(Date, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class STRInvestmentAnalysis(Base):
    """STR investment returns and metrics"""
    __tablename__ = "str_investment_analysis"

    id = Column(Integer, primary_key=True, index=True)
    market = Column(String(200), nullable=False, index=True)
    property_type = Column(String(100), index=True)
    avg_acquisition_cost = Column(Numeric(15, 2))
    avg_renovation_cost = Column(Numeric(15, 2))
    total_upfront_investment = Column(Numeric(15, 2))
    annual_gross_revenue = Column(Numeric(15, 2))
    annual_net_operating_income = Column(Numeric(15, 2))
    cash_on_cash_return_pct = Column(Numeric(5, 2))
    cap_rate_pct = Column(Numeric(5, 2))
    payback_period_years = Column(Numeric(5, 2))
    irr_5year_pct = Column(Numeric(5, 2))
    appreciation_rate_annual_pct = Column(Numeric(5, 2))
    data_source = Column(String(200))
    period = Column(Date, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class STRPlatformPerformance(Base):
    """STR platform performance metrics"""
    __tablename__ = "str_platform_performance"

    id = Column(Integer, primary_key=True, index=True)
    market = Column(String(200), nullable=False, index=True)
    platform_name = Column(String(100), nullable=False, index=True)
    market_share_pct = Column(Numeric(5, 2))
    total_listings = Column(Integer)
    active_listings = Column(Integer)
    avg_adr = Column(Numeric(10, 2))
    avg_occupancy_rate_pct = Column(Numeric(5, 2))
    booking_volume = Column(Integer)
    gross_booking_value_usd = Column(Numeric(20, 2))
    commission_rate_pct = Column(Numeric(5, 2))
    host_retention_rate_pct = Column(Numeric(5, 2))
    guest_satisfaction_score = Column(Numeric(3, 2))
    data_source = Column(String(200))
    period = Column(Date, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class STRPricingPatterns(Base):
    """STR pricing patterns and dynamics"""
    __tablename__ = "str_pricing_patterns"

    id = Column(Integer, primary_key=True, index=True)
    market = Column(String(200), nullable=False, index=True)
    property_type = Column(String(100), index=True)
    season = Column(String(50), index=True)  # peak, shoulder, off-peak
    avg_nightly_rate = Column(Numeric(10, 2))
    min_nightly_rate = Column(Numeric(10, 2))
    max_nightly_rate = Column(Numeric(10, 2))
    weekend_premium_pct = Column(Numeric(5, 2))
    holiday_premium_pct = Column(Numeric(5, 2))
    special_event_premium_pct = Column(Numeric(5, 2))
    last_minute_discount_pct = Column(Numeric(5, 2))
    early_booking_discount_pct = Column(Numeric(5, 2))
    dynamic_pricing_adoption_pct = Column(Numeric(5, 2))
    data_source = Column(String(200))
    period = Column(Date, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class STRSupplyDemandDynamics(Base):
    """STR supply and demand dynamics"""
    __tablename__ = "str_supply_demand_dynamics"

    id = Column(Integer, primary_key=True, index=True)
    market = Column(String(200), nullable=False, index=True)
    total_supply_units = Column(Integer)
    new_listings_mtd = Column(Integer)
    delisted_units_mtd = Column(Integer)
    net_supply_change_mtd = Column(Integer)
    supply_growth_rate_yoy_pct = Column(Numeric(5, 2))
    total_demand_bookings = Column(Integer)
    demand_growth_rate_yoy_pct = Column(Numeric(5, 2))
    supply_demand_ratio = Column(Numeric(10, 2))
    market_saturation_level = Column(String(50), index=True)  # undersupplied, balanced, oversupplied
    projected_supply_12m = Column(Integer)
    projected_demand_12m = Column(Integer)
    data_source = Column(String(200))
    period = Column(Date, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


# ========================================
# ADVANCED ZONING/DEVELOPMENT MODELS
# ========================================

class EntitledLandInventory(Base):
    """Entitled but unbuilt land inventory"""
    __tablename__ = "entitled_land_inventory"

    id = Column(Integer, primary_key=True, index=True)
    market = Column(String(200), nullable=False, index=True)
    project_name = Column(String(300))
    zone_type = Column(String(100), index=True)
    entitled_units = Column(Integer)
    entitled_sf = Column(Integer)
    project_type = Column(String(100), index=True)  # residential, mixed-use, commercial
    approval_date = Column(Date)
    years_since_approval = Column(Numeric(5, 2))
    estimated_land_value_mm = Column(Numeric(15, 2))
    estimated_built_value_mm = Column(Numeric(15, 2))
    development_status = Column(String(100), index=True)  # shovel-ready, planned, stalled
    constraints = Column(Text)
    data_source = Column(String(200))
    period = Column(Date, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class FutureZoningInitiatives(Base):
    """Future zoning initiatives and proposals"""
    __tablename__ = "future_zoning_initiatives"

    id = Column(Integer, primary_key=True, index=True)
    market = Column(String(200), nullable=False, index=True)
    initiative_name = Column(String(300), nullable=False)
    initiative_type = Column(String(100), index=True)  # upzoning, rezoning, overlay
    area_affected_acres = Column(Numeric(15, 2))
    neighborhoods_affected = Column(Text)
    current_zoning = Column(String(100))
    proposed_zoning = Column(String(100))
    estimated_new_units_enabled = Column(Integer)
    estimated_new_sf_enabled = Column(Integer)
    proposal_date = Column(Date)
    expected_approval_date = Column(Date)
    approval_likelihood = Column(String(50), index=True)  # high, medium, low
    political_support_level = Column(String(50))
    data_source = Column(String(200))
    period = Column(Date, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class RegulatoryBarriers(Base):
    """Regulatory barriers to development"""
    __tablename__ = "regulatory_barriers"

    id = Column(Integer, primary_key=True, index=True)
    market = Column(String(200), nullable=False, index=True)
    barrier_type = Column(String(100), nullable=False, index=True)  # permitting, environmental, zoning
    barrier_description = Column(Text)
    affected_project_types = Column(String(200))
    avg_delay_months = Column(Numeric(5, 2))
    avg_additional_cost_pct = Column(Numeric(5, 2))
    projects_impacted_annually = Column(Integer)
    severity_rating = Column(String(50), index=True)  # low, medium, high, critical
    potential_reform_status = Column(String(100))
    estimated_units_blocked_annually = Column(Integer)
    economic_impact_mm = Column(Numeric(15, 2))
    data_source = Column(String(200))
    period = Column(Date, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class TransitOrientedDevelopment(Base):
    """Transit-oriented development opportunities"""
    __tablename__ = "transit_oriented_development"

    id = Column(Integer, primary_key=True, index=True)
    market = Column(String(200), nullable=False, index=True)
    tod_zone_name = Column(String(300), nullable=False, index=True)
    transit_type = Column(String(100), index=True)  # metro, light rail, bus rapid transit
    station_name = Column(String(200))
    distance_to_station_feet = Column(Integer)
    current_zoning = Column(String(100))
    tod_zoning_designation = Column(String(100))
    max_far_allowed = Column(Numeric(5, 2))
    max_height_feet = Column(Integer)
    parking_reduction_pct = Column(Numeric(5, 2))
    density_bonus_pct = Column(Numeric(5, 2))
    developable_acres = Column(Numeric(15, 2))
    estimated_units_capacity = Column(Integer)
    estimated_sf_capacity = Column(Integer)
    development_pipeline_units = Column(Integer)
    utilization_rate_pct = Column(Numeric(5, 2))
    data_source = Column(String(200))
    period = Column(Date, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ZoningMasterMetrics(Base):
    """Zoning master metrics summary"""
    __tablename__ = "zoning_master_metrics"

    id = Column(Integer, primary_key=True, index=True)
    market = Column(String(200), nullable=False, index=True)
    metric_name = Column(String(200), nullable=False, index=True)
    metric_value = Column(Numeric(20, 6))
    metric_unit = Column(String(50))
    metric_category = Column(String(100), index=True)  # capacity, utilization, reform, barriers
    benchmark_value = Column(Numeric(20, 6))
    variance_from_benchmark_pct = Column(Numeric(5, 2))
    trend_direction = Column(String(50))  # improving, stable, declining
    data_source = Column(String(200))
    notes = Column(Text)
    period = Column(Date, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


# ========================================
# IMPORT FUNCTIONS
# ========================================

def parse_date(date_str: str) -> Optional[date]:
    """Parse date string into date object"""
    if not date_str or date_str.strip() == '':
        return None

    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except:
            logger.warning(f"Could not parse date: {date_str}")
            return None


def parse_numeric(value_str: str) -> Optional[Decimal]:
    """Parse numeric string into Decimal"""
    if not value_str or value_str.strip() == '':
        return None

    try:
        # Remove commas and convert
        clean_value = value_str.replace(',', '')
        return Decimal(clean_value)
    except:
        logger.warning(f"Could not parse numeric: {value_str}")
        return None


def parse_int(value_str: str) -> Optional[int]:
    """Parse integer string into int, handling decimal notation"""
    if not value_str or value_str.strip() == '':
        return None

    try:
        # Convert to float first to handle decimal strings like "323.0"
        return int(float(value_str.replace(',', '')))
    except:
        logger.warning(f"Could not parse integer: {value_str}")
        return None


def import_geographic_indicators(csv_path: Path, session: Session) -> int:
    """Import geographic economic indicators from CSV"""
    logger.info(f"Importing geographic indicators from {csv_path}")

    count = 0
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            try:
                indicator = GeographicEconomicIndicator(
                    geography=row['geography'],
                    geography_type=row['geography_type'],
                    indicator_name=row['indicator_name'],
                    indicator_value=parse_numeric(row['indicator_value']),
                    indicator_unit=row['indicator_unit'],
                    period=parse_date(row['period']),
                    period_type=row.get('period_type', ''),
                    data_source=row.get('data_source', ''),
                    notes=row.get('notes', '')
                )

                session.add(indicator)
                count += 1

                if count % 100 == 0:
                    session.commit()
                    logger.info(f"Imported {count} geographic indicators...")

            except Exception as e:
                logger.error(f"Error importing row: {row}. Error: {e}")
                session.rollback()
                continue

        session.commit()

    logger.info(f"✅ Imported {count} geographic indicators")
    return count


def import_market_data(csv_path: Path, session: Session) -> int:
    """Import real estate market data from CSV"""
    logger.info(f"Importing market data from {csv_path}")

    count = 0
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            try:
                market_data = RealEstateMarketData(
                    market_name=row['market_name'],
                    submarket_name=row.get('submarket_name', ''),
                    property_type=row['property_type'],
                    property_class=row.get('property_class', ''),
                    metric_name=row['metric_name'],
                    metric_value=parse_numeric(row['metric_value']),
                    metric_unit=row['metric_unit'],
                    period=parse_date(row['period']),
                    data_source=row.get('data_source', ''),
                    confidence_level=row.get('confidence_level', ''),
                    notes=row.get('notes', '')
                )

                session.add(market_data)
                count += 1

                if count % 100 == 0:
                    session.commit()
                    logger.info(f"Imported {count} market data points...")

            except Exception as e:
                logger.error(f"Error importing row: {row}. Error: {e}")
                session.rollback()
                continue

        session.commit()

    logger.info(f"✅ Imported {count} market data points")
    return count


def import_comparable_transactions(csv_path: Path, session: Session) -> int:
    """Import comparable transactions from CSV"""
    logger.info(f"Importing comparable transactions from {csv_path}")

    count = 0
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            try:
                transaction = ComparableTransaction(
                    address=row.get('address', ''),
                    city=row['city'],
                    submarket=row.get('submarket', ''),
                    state=row['state'],
                    zip_code=row.get('zip_code', ''),
                    property_type=row['property_type'],
                    property_class=row.get('property_class', ''),
                    sale_date=parse_date(row['sale_date']),
                    sale_price=parse_numeric(row.get('sale_price', '')),
                    price_per_unit=parse_numeric(row.get('price_per_unit', '')),
                    price_per_sf=parse_numeric(row.get('price_per_sf', '')),
                    cap_rate=parse_numeric(row.get('cap_rate', '')),
                    units=parse_int(row.get('units', '')),
                    total_sf=parse_int(row.get('total_sf', '')),
                    lot_size_sf=parse_int(row.get('lot_size_sf', '')),
                    year_built=parse_int(row.get('year_built', '')),
                    year_renovated=parse_int(row.get('year_renovated', '')),
                    num_buildings=parse_int(row.get('num_buildings', '')),
                    num_floors=parse_int(row.get('num_floors', '')),
                    parking_spaces=parse_int(row.get('parking_spaces', '')),
                    noi=parse_numeric(row.get('noi', '')),
                    gross_potential_rent=parse_numeric(row.get('gross_potential_rent', '')),
                    occupancy_at_sale=parse_numeric(row.get('occupancy_at_sale', '')),
                    inplace_vs_market_rent_pct=parse_numeric(row.get('inplace_vs_market_rent_pct', '')),
                    buyer=row.get('buyer', ''),
                    buyer_type=row.get('buyer_type', ''),
                    seller=row.get('seller', ''),
                    seller_type=row.get('seller_type', ''),
                    broker=row.get('broker', ''),
                    financing_type=row.get('financing_type', ''),
                    ltv=parse_numeric(row.get('ltv', '')),
                    lender=row.get('lender', ''),
                    interest_rate=parse_numeric(row.get('interest_rate', '')),
                    deal_type=row.get('deal_type', ''),
                    special_conditions=row.get('special_conditions', ''),
                    data_source=row.get('data_source', ''),
                    source_url=row.get('source_url', ''),
                    notes=row.get('notes', '')
                )

                session.add(transaction)
                count += 1

                if count % 100 == 0:
                    session.commit()
                    logger.info(f"Imported {count} transactions...")

            except Exception as e:
                logger.error(f"Error importing row: {row}. Error: {e}")
                session.rollback()
                continue

        session.commit()

    logger.info(f"✅ Imported {count} transactions")
    return count


def import_hot_zones(csv_path: Path, session: Session) -> int:
    """Import hot zones and emerging markets from CSV"""
    logger.info(f"Importing hot zones from {csv_path}")

    count = 0
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            try:
                hot_zone = HotZoneMarket(
                    market_name=row['market_name'],
                    neighborhood_name=row['neighborhood_name'],
                    hot_zone_rank=parse_int(row.get('hot_zone_rank', '')),
                    metric_category=row['metric_category'],
                    metric_name=row['metric_name'],
                    metric_value=parse_numeric(row['metric_value']),
                    metric_unit=row['metric_unit'],
                    period=parse_date(row['period']),
                    comparison_to_city_average=row.get('comparison_to_city_average', ''),
                    data_source=row.get('data_source', ''),
                    notes=row.get('notes', '')
                )

                session.add(hot_zone)
                count += 1

                if count % 100 == 0:
                    session.commit()
                    logger.info(f"Imported {count} hot zone records...")

            except Exception as e:
                logger.error(f"Error importing row: {row}. Error: {e}")
                session.rollback()
                continue

        session.commit()

    logger.info(f"✅ Imported {count} hot zone records")
    return count


def import_neighborhood_scores(csv_path: Path, session: Session) -> int:
    """Import neighborhood scoring analysis from CSV"""
    logger.info(f"Importing neighborhood scores from {csv_path}")

    count = 0
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            try:
                score = NeighborhoodScore(
                    market_name=row['market_name'],
                    neighborhood_name=row['neighborhood_name'],
                    score_category=row['score_category'],
                    score_value=parse_numeric(row['score_value']),
                    rank_within_market=parse_int(row.get('rank_within_market', '')),
                    rank_nationally=parse_int(row.get('rank_nationally', '')),
                    period=parse_date(row['period']),
                    data_source=row.get('data_source', ''),
                    notes=row.get('notes', '')
                )

                session.add(score)
                count += 1

                if count % 100 == 0:
                    session.commit()
                    logger.info(f"Imported {count} neighborhood score records...")

            except Exception as e:
                logger.error(f"Error importing row: {row}. Error: {e}")
                session.rollback()
                continue

        session.commit()

    logger.info(f"✅ Imported {count} neighborhood score records")
    return count


# ========================================
# NEW IMPORT FUNCTIONS
# ========================================

def import_str_hot_neighborhoods(csv_path: Path, session: Session) -> int:
    """Import STR hot neighborhoods from CSV"""
    logger.info(f"Importing STR hot neighborhoods from {csv_path}")
    count = 0
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                record = STRHotNeighborhood(
                    market=row['market'],
                    neighborhood_rank=parse_int(row.get('neighborhood_rank', '')),
                    neighborhood_name=row['neighborhood_name'],
                    avg_annual_revenue_per_listing=parse_numeric(row.get('avg_annual_revenue_per_listing', '')),
                    avg_occupancy_rate_pct=parse_numeric(row.get('avg_occupancy_rate_pct', '')),
                    avg_revpar=parse_numeric(row.get('avg_revpar', '')),
                    growth_stage=row.get('growth_stage', ''),
                    revenue_category=row.get('revenue_category', ''),
                    data_source=row.get('data_source', ''),
                    analysis_date=parse_date(row.get('analysis_date', ''))
                )
                session.add(record)
                count += 1
                if count % 100 == 0:
                    session.commit()
                    logger.info(f"Imported {count} STR hot neighborhood records...")
            except Exception as e:
                logger.error(f"Error importing row: {row}. Error: {e}")
                session.rollback()
                continue
        session.commit()
    logger.info(f"✅ Imported {count} STR hot neighborhood records")
    return count


def import_str_performance_metrics(csv_path: Path, session: Session) -> int:
    """Import STR performance metrics from CSV"""
    logger.info(f"Importing STR performance metrics from {csv_path}")
    count = 0
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                record = STRPerformanceMetrics(
                    market=row['market'],
                    property_type=row['property_type'],
                    adr_daily=parse_numeric(row.get('adr_daily', '')),
                    occupancy_rate_pct=parse_numeric(row.get('occupancy_rate_pct', '')),
                    revpar=parse_numeric(row.get('revpar', '')),
                    monthly_revenue_avg=parse_numeric(row.get('monthly_revenue_avg', '')),
                    annual_revenue_avg=parse_numeric(row.get('annual_revenue_avg', '')),
                    booking_lead_time_days=parse_int(row.get('booking_lead_time_days', '')),
                    avg_length_of_stay_nights=parse_numeric(row.get('avg_length_of_stay_nights', '')),
                    review_score=parse_numeric(row.get('review_score', '')),
                    data_source=row.get('data_source', ''),
                    period=parse_date(row.get('period', ''))
                )
                session.add(record)
                count += 1
                if count % 100 == 0:
                    session.commit()
                    logger.info(f"Imported {count} STR performance metric records...")
            except Exception as e:
                logger.error(f"Error importing row: {row}. Error: {e}")
                session.rollback()
                continue
        session.commit()
    logger.info(f"✅ Imported {count} STR performance metric records")
    return count


def import_str_market_overview(csv_path: Path, session: Session) -> int:
    """Import STR market overview from CSV"""
    logger.info(f"Importing STR market overview from {csv_path}")
    count = 0
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                record = STRMarketOverview(
                    market=row['market'],
                    total_str_listings=parse_int(row.get('total_str_listings', '')),
                    active_listings_30days=parse_int(row.get('active_listings_30days', '')),
                    entire_home_apt_count=parse_int(row.get('entire_home_apt_count', '')),
                    entire_home_pct=parse_numeric(row.get('entire_home_pct', '')),
                    private_shared_room_count=parse_int(row.get('private_shared_room_count', '')),
                    private_shared_room_pct=parse_numeric(row.get('private_shared_room_pct', '')),
                    str_pct_of_housing_stock=parse_numeric(row.get('str_pct_of_housing_stock', '')),
                    inventory_growth_yoy_pct=parse_numeric(row.get('inventory_growth_yoy_pct', '')),
                    avg_listing_age_months=parse_numeric(row.get('avg_listing_age_months', '')),
                    host_concentration_10plus_pct=parse_numeric(row.get('host_concentration_10plus_pct', '')),
                    data_source=row.get('data_source', ''),
                    analysis_date=parse_date(row.get('analysis_date', ''))
                )
                session.add(record)
                count += 1
                if count % 100 == 0:
                    session.commit()
                    logger.info(f"Imported {count} STR market overview records...")
            except Exception as e:
                logger.error(f"Error importing row: {row}. Error: {e}")
                session.rollback()
                continue
        session.commit()
    logger.info(f"✅ Imported {count} STR market overview records")
    return count


def import_str_regulatory_environment(csv_path: Path, session: Session) -> int:
    """Import STR regulatory environment from CSV"""
    logger.info(f"Importing STR regulatory environment from {csv_path}")
    count = 0
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                record = STRRegulatoryEnvironment(
                    market=row['market'],
                    regulation_type=row.get('regulation_type', ''),
                    registration_required=row.get('registration_required', ''),
                    license_permit_required=row.get('license_permit_required', ''),
                    license_cost_usd=parse_numeric(row.get('license_cost_usd', '')),
                    primary_residence_requirement=row.get('primary_residence_requirement', ''),
                    max_rental_days_per_year=parse_int(row.get('max_rental_days_per_year', '')),
                    occupancy_tax_rate_pct=parse_numeric(row.get('occupancy_tax_rate_pct', '')),
                    platform_collects_taxes=row.get('platform_collects_taxes', ''),
                    enforcement_level=row.get('enforcement_level', ''),
                    fine_per_violation_usd=parse_numeric(row.get('fine_per_violation_usd', '')),
                    data_source=row.get('data_source', ''),
                    effective_date=parse_date(row.get('effective_date', ''))
                )
                session.add(record)
                count += 1
                if count % 100 == 0:
                    session.commit()
                    logger.info(f"Imported {count} STR regulatory records...")
            except Exception as e:
                logger.error(f"Error importing row: {row}. Error: {e}")
                session.rollback()
                continue
        session.commit()
    logger.info(f"✅ Imported {count} STR regulatory records")
    return count


def import_zoning_districts(csv_path: Path, session: Session) -> int:
    """Import zoning districts from CSV"""
    logger.info(f"Importing zoning districts from {csv_path}")
    count = 0
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                record = ZoningDistrict(
                    market=row['market'],
                    zone_type=row['zone_type'],
                    zone_code=row.get('zone_code', ''),
                    max_far=parse_numeric(row.get('max_far', '')),
                    max_height_feet=parse_int(row.get('max_height_feet', '')),
                    min_lot_size_sf=parse_int(row.get('min_lot_size_sf', '')),
                    parking_requirement=row.get('parking_requirement', ''),
                    setback_front_feet=parse_int(row.get('setback_front_feet', '')),
                    use_restrictions=row.get('use_restrictions', ''),
                    data_source=row.get('data_source', ''),
                    effective_date=parse_date(row.get('effective_date', ''))
                )
                session.add(record)
                count += 1
                if count % 100 == 0:
                    session.commit()
                    logger.info(f"Imported {count} zoning district records...")
            except Exception as e:
                logger.error(f"Error importing row: {row}. Error: {e}")
                session.rollback()
                continue
        session.commit()
    logger.info(f"✅ Imported {count} zoning district records")
    return count


def import_zoning_reforms(csv_path: Path, session: Session) -> int:
    """Import zoning reforms from CSV"""
    logger.info(f"Importing zoning reforms from {csv_path}")
    count = 0
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                record = ZoningReform(
                    market=row['market'],
                    reform_name=row['reform_name'],
                    area_affected=row.get('area_affected', ''),
                    old_zoning=row.get('old_zoning', ''),
                    new_zoning=row.get('new_zoning', ''),
                    effective_date=parse_date(row.get('effective_date', '')),
                    units_enabled=parse_int(row.get('units_enabled', '')),
                    description=row.get('description', ''),
                    data_source=row.get('data_source', '')
                )
                session.add(record)
                count += 1
                if count % 100 == 0:
                    session.commit()
                    logger.info(f"Imported {count} zoning reform records...")
            except Exception as e:
                logger.error(f"Error importing row: {row}. Error: {e}")
                session.rollback()
                continue
        session.commit()
    logger.info(f"✅ Imported {count} zoning reform records")
    return count


def import_opportunity_zones(csv_path: Path, session: Session) -> int:
    """Import opportunity zones from CSV"""
    logger.info(f"Importing opportunity zones from {csv_path}")
    count = 0
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                record = OpportunityZone(
                    market=row['market'],
                    num_opportunity_zones=parse_int(row.get('num_opportunity_zones', '')),
                    total_acres_in_oz=parse_numeric(row.get('total_acres_in_oz', '')),
                    investment_in_oz_mm=parse_numeric(row.get('investment_in_oz_mm', '')),
                    development_projects_in_oz=parse_int(row.get('development_projects_in_oz', '')),
                    oz_residential_units=parse_int(row.get('oz_residential_units', '')),
                    oz_commercial_sf=parse_int(row.get('oz_commercial_sf', '')),
                    avg_cap_rate_compression_bps=parse_int(row.get('avg_cap_rate_compression_bps', '')),
                    oz_designation_date=parse_date(row.get('oz_designation_date', '')),
                    data_source=row.get('data_source', ''),
                    period=parse_date(row.get('period', ''))
                )
                session.add(record)
                count += 1
                if count % 100 == 0:
                    session.commit()
                    logger.info(f"Imported {count} opportunity zone records...")
            except Exception as e:
                logger.error(f"Error importing row: {row}. Error: {e}")
                session.rollback()
                continue
        session.commit()
    logger.info(f"✅ Imported {count} opportunity zone records")
    return count


def import_underbuilt_parcels(csv_path: Path, session: Session) -> int:
    """Import underbuilt parcels from CSV"""
    logger.info(f"Importing underbuilt parcels from {csv_path}")
    count = 0
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                record = UnderbuiltParcel(
                    market=row['market'],
                    zone_type=row.get('zone_type', ''),
                    num_underbuilt_parcels=parse_int(row.get('num_underbuilt_parcels', '')),
                    avg_current_far=parse_numeric(row.get('avg_current_far', '')),
                    avg_max_allowed_far=parse_numeric(row.get('avg_max_allowed_far', '')),
                    far_gap=parse_numeric(row.get('far_gap', '')),
                    avg_current_height_feet=parse_int(row.get('avg_current_height_feet', '')),
                    avg_max_height_feet=parse_int(row.get('avg_max_height_feet', '')),
                    avg_parcel_size_sf=parse_int(row.get('avg_parcel_size_sf', '')),
                    avg_parcel_size_acres=parse_numeric(row.get('avg_parcel_size_acres', '')),
                    total_additional_developable_sf=parse_int(row.get('total_additional_developable_sf', '')),
                    estimated_additional_units_possible=parse_int(row.get('estimated_additional_units_possible', '')),
                    data_source=row.get('data_source', ''),
                    analysis_date=parse_date(row.get('analysis_date', ''))
                )
                session.add(record)
                count += 1
                if count % 100 == 0:
                    session.commit()
                    logger.info(f"Imported {count} underbuilt parcel records...")
            except Exception as e:
                logger.error(f"Error importing row: {row}. Error: {e}")
                session.rollback()
                continue
        session.commit()
    logger.info(f"✅ Imported {count} underbuilt parcel records")
    return count


def import_development_pipeline(csv_path: Path, session: Session) -> int:
    """Import development pipeline from CSV"""
    logger.info(f"Importing development pipeline from {csv_path}")
    count = 0
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                record = DevelopmentPipeline(
                    market=row['market'],
                    zone_type=row.get('zone_type', ''),
                    projects_under_construction=parse_int(row.get('projects_under_construction', '')),
                    units_under_construction=parse_int(row.get('units_under_construction', '')),
                    sf_under_construction=parse_int(row.get('sf_under_construction', '')),
                    permits_issued_ytd_2024=parse_int(row.get('permits_issued_ytd_2024', '')),
                    units_permitted_ytd=parse_int(row.get('units_permitted_ytd', '')),
                    sf_permitted_ytd=parse_int(row.get('sf_permitted_ytd', '')),
                    permit_value_mm=parse_numeric(row.get('permit_value_mm', '')),
                    applications_pending=parse_int(row.get('applications_pending', '')),
                    avg_approval_timeline_months=parse_numeric(row.get('avg_approval_timeline_months', '')),
                    approval_success_rate_pct=parse_numeric(row.get('approval_success_rate_pct', '')),
                    data_source=row.get('data_source', ''),
                    period=parse_date(row.get('period', ''))
                )
                session.add(record)
                count += 1
                if count % 100 == 0:
                    session.commit()
                    logger.info(f"Imported {count} development pipeline records...")
            except Exception as e:
                logger.error(f"Error importing row: {row}. Error: {e}")
                session.rollback()
                continue
        session.commit()
    logger.info(f"✅ Imported {count} development pipeline records")
    return count


def import_land_cost_economics(csv_path: Path, session: Session) -> int:
    """Import land cost economics from CSV"""
    logger.info(f"Importing land cost economics from {csv_path}")
    count = 0
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                record = LandCostEconomics(
                    market=row['market'],
                    zone_type=row.get('zone_type', ''),
                    land_price_per_sf=parse_numeric(row.get('land_price_per_sf', '')),
                    land_price_per_developable_sf=parse_numeric(row.get('land_price_per_developable_sf', '')),
                    land_as_pct_of_total_cost=parse_numeric(row.get('land_as_pct_of_total_cost', '')),
                    estimated_construction_cost_per_sf=parse_numeric(row.get('estimated_construction_cost_per_sf', '')),
                    pro_forma_yield_on_cost_pct=parse_numeric(row.get('pro_forma_yield_on_cost_pct', '')),
                    data_source=row.get('data_source', ''),
                    period=parse_date(row.get('period', ''))
                )
                session.add(record)
                count += 1
                if count % 100 == 0:
                    session.commit()
                    logger.info(f"Imported {count} land cost economics records...")
            except Exception as e:
                logger.error(f"Error importing row: {row}. Error: {e}")
                session.rollback()
                continue
        session.commit()
    logger.info(f"✅ Imported {count} land cost economics records")
    return count


def import_property_tax_assessments(csv_path: Path, session: Session) -> int:
    """Import property tax assessments from CSV"""
    logger.info(f"Importing property tax assessments from {csv_path}")
    count = 0
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                record = PropertyTaxAssessment(
                    market=row['market'],
                    geography_type=row.get('geography_type', ''),
                    indicator_name=row['indicator_name'],
                    indicator_value=parse_numeric(row.get('indicator_value', '')),
                    indicator_unit=row.get('indicator_unit', ''),
                    data_source=row.get('data_source', ''),
                    notes=row.get('notes', '')
                )
                session.add(record)
                count += 1
                if count % 100 == 0:
                    session.commit()
                    logger.info(f"Imported {count} property tax assessment records...")
            except Exception as e:
                logger.error(f"Error importing row: {row}. Error: {e}")
                session.rollback()
                continue
        session.commit()
    logger.info(f"✅ Imported {count} property tax assessment records")
    return count


def import_tenant_credit_quality(csv_path: Path, session: Session) -> int:
    """Import tenant credit quality from CSV"""
    logger.info(f"Importing tenant credit quality from {csv_path}")
    count = 0
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                record = TenantCreditQuality(
                    tenant_name=row['tenant_name'],
                    ticker=row.get('ticker', ''),
                    category=row.get('category', ''),
                    company_name=row.get('company_name', ''),
                    moodys_rating=row.get('moodys_rating', ''),
                    sp_rating=row.get('sp_rating', ''),
                    metric_name=row['metric_name'],
                    metric_value=parse_numeric(row.get('metric_value', '')),
                    unit=row.get('unit', ''),
                    data_source=row.get('data_source', ''),
                    period=parse_date(row.get('period', '')),
                    notes=row.get('notes', '')
                )
                session.add(record)
                count += 1
                if count % 100 == 0:
                    session.commit()
                    logger.info(f"Imported {count} tenant credit quality records...")
            except Exception as e:
                logger.error(f"Error importing row: {row}. Error: {e}")
                session.rollback()
                continue
        session.commit()
    logger.info(f"✅ Imported {count} tenant credit quality records")
    return count


# ========================================
# NEW CSV IMPORT FUNCTIONS
# ========================================

def import_time_series_indicators(csv_path: Path, session: Session, source_category: str) -> int:
    """Import time-series indicators from CSV (unified for all financial time-series data)"""
    logger.info(f"Importing time-series indicators from {csv_path} (category: {source_category})")
    count = 0
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                record = TimeSeriesIndicator(
                    date=parse_date(row['date']),
                    period_type=row.get('period_type', ''),
                    indicator_name=row['indicator_name'],
                    indicator_value=parse_numeric(row.get('indicator_value', '')),
                    indicator_unit=row.get('indicator_unit', ''),
                    source_category=source_category,
                    data_source=row.get('data_source', ''),
                    notes=row.get('notes', '')
                )
                session.add(record)
                count += 1
                if count % 100 == 0:
                    session.commit()
                    logger.info(f"Imported {count} time-series records...")
            except Exception as e:
                logger.error(f"Error importing row: {row}. Error: {e}")
                session.rollback()
                continue
        session.commit()
    logger.info(f"✅ Imported {count} time-series records for {source_category}")
    return count


def import_str_competitive_analysis(csv_path: Path, session: Session) -> int:
    """Import STR competitive analysis from CSV"""
    logger.info(f"Importing STR competitive analysis from {csv_path}")
    count = 0
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                record = STRCompetitiveAnalysis(
                    market=row['market'],
                    str_adr_daily=parse_numeric(row.get('str_adr_daily', '')),
                    str_monthly_equivalent_adr_x30=parse_numeric(row.get('str_monthly_equivalent_adr_x30', '')),
                    ltr_monthly_rent=parse_numeric(row.get('ltr_monthly_rent', '')),
                    str_adr_vs_ltr_difference=parse_numeric(row.get('str_adr_vs_ltr_difference', '')),
                    str_profitability_advantage=parse_numeric(row.get('str_profitability_advantage', '')),
                    breakeven_occupancy_rate_pct=parse_numeric(row.get('breakeven_occupancy_rate_pct', '')),
                    str_implied_cap_rate_pct=parse_numeric(row.get('str_implied_cap_rate_pct', '')),
                    ltr_implied_cap_rate_pct=parse_numeric(row.get('ltr_implied_cap_rate_pct', '')),
                    cap_rate_advantage_basis_points=parse_numeric(row.get('cap_rate_advantage_basis_points', '')),
                    data_source=row.get('data_source', ''),
                    period=row.get('period', '')
                )
                session.add(record)
                count += 1
                if count % 100 == 0:
                    session.commit()
                    logger.info(f"Imported {count} STR competitive analysis records...")
            except Exception as e:
                logger.error(f"Error importing row: {row}. Error: {e}")
                session.rollback()
                continue
        session.commit()
    logger.info(f"✅ Imported {count} STR competitive analysis records")
    return count


def import_str_compliance_enforcement(csv_path: Path, session: Session) -> int:
    """Import STR compliance enforcement from CSV"""
    logger.info(f"Importing STR compliance enforcement from {csv_path}")
    count = 0
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                record = STRComplianceEnforcement(
                    market=row['market'],
                    regulation_type=row.get('regulation_type', ''),
                    enforcement_level=row.get('enforcement_level', ''),
                    violations_issued=parse_int(row.get('violations_issued', '')),
                    fines_collected_usd=parse_numeric(row.get('fines_collected_usd', '')),
                    avg_fine_per_violation_usd=parse_numeric(row.get('avg_fine_per_violation_usd', '')),
                    compliance_rate_pct=parse_numeric(row.get('compliance_rate_pct', '')),
                    registered_hosts_count=parse_int(row.get('registered_hosts_count', '')),
                    unregistered_hosts_count=parse_int(row.get('unregistered_hosts_count', '')),
                    platform_cooperation_level=row.get('platform_cooperation_level', ''),
                    data_source=row.get('data_source', ''),
                    period=parse_date(row.get('period', ''))
                )
                session.add(record)
                count += 1
                if count % 100 == 0:
                    session.commit()
                    logger.info(f"Imported {count} STR compliance enforcement records...")
            except Exception as e:
                logger.error(f"Error importing row: {row}. Error: {e}")
                session.rollback()
                continue
        session.commit()
    logger.info(f"✅ Imported {count} STR compliance enforcement records")
    return count


def import_str_guest_demographics(csv_path: Path, session: Session) -> int:
    """Import STR guest demographics from CSV"""
    logger.info(f"Importing STR guest demographics from {csv_path}")
    count = 0
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                record = STRGuestDemographics(
                    market=row['market'],
                    guest_origin=row.get('guest_origin', ''),
                    avg_group_size=parse_numeric(row.get('avg_group_size', '')),
                    avg_age_range=row.get('avg_age_range', ''),
                    purpose_of_visit=row.get('purpose_of_visit', ''),
                    avg_booking_value_usd=parse_numeric(row.get('avg_booking_value_usd', '')),
                    avg_length_of_stay_nights=parse_numeric(row.get('avg_length_of_stay_nights', '')),
                    repeat_guest_rate_pct=parse_numeric(row.get('repeat_guest_rate_pct', '')),
                    review_participation_rate_pct=parse_numeric(row.get('review_participation_rate_pct', '')),
                    avg_review_score=parse_numeric(row.get('avg_review_score', '')),
                    data_source=row.get('data_source', ''),
                    period=parse_date(row.get('period', ''))
                )
                session.add(record)
                count += 1
                if count % 100 == 0:
                    session.commit()
                    logger.info(f"Imported {count} STR guest demographics records...")
            except Exception as e:
                logger.error(f"Error importing row: {row}. Error: {e}")
                session.rollback()
                continue
        session.commit()
    logger.info(f"✅ Imported {count} STR guest demographics records")
    return count


def import_str_host_economics(csv_path: Path, session: Session) -> int:
    """Import STR host economics from CSV"""
    logger.info(f"Importing STR host economics from {csv_path}")
    count = 0
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                record = STRHostEconomics(
                    market=row['market'],
                    host_type=row.get('host_type', ''),
                    avg_annual_revenue_per_listing=parse_numeric(row.get('avg_annual_revenue_per_listing', '')),
                    avg_monthly_revenue_per_listing=parse_numeric(row.get('avg_monthly_revenue_per_listing', '')),
                    avg_occupancy_rate_pct=parse_numeric(row.get('avg_occupancy_rate_pct', '')),
                    avg_nightly_rate=parse_numeric(row.get('avg_nightly_rate', '')),
                    operating_expenses_pct_of_revenue=parse_numeric(row.get('operating_expenses_pct_of_revenue', '')),
                    platform_fees_pct=parse_numeric(row.get('platform_fees_pct', '')),
                    cleaning_fees_avg=parse_numeric(row.get('cleaning_fees_avg', '')),
                    estimated_net_margin_pct=parse_numeric(row.get('estimated_net_margin_pct', '')),
                    time_to_profitability_months=parse_int(row.get('time_to_profitability_months', '')),
                    data_source=row.get('data_source', ''),
                    period=parse_date(row.get('period', ''))
                )
                session.add(record)
                count += 1
                if count % 100 == 0:
                    session.commit()
                    logger.info(f"Imported {count} STR host economics records...")
            except Exception as e:
                logger.error(f"Error importing row: {row}. Error: {e}")
                session.rollback()
                continue
        session.commit()
    logger.info(f"✅ Imported {count} STR host economics records")
    return count


def import_str_housing_market_impact(csv_path: Path, session: Session) -> int:
    """Import STR housing market impact from CSV"""
    logger.info(f"Importing STR housing market impact from {csv_path}")
    count = 0
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                record = STRHousingMarketImpact(
                    market=row['market'],
                    str_listings_count=parse_int(row.get('str_listings_count', '')),
                    str_pct_of_housing_stock=parse_numeric(row.get('str_pct_of_housing_stock', '')),
                    ltr_units_lost_to_str=parse_int(row.get('ltr_units_lost_to_str', '')),
                    estimated_rent_increase_pct=parse_numeric(row.get('estimated_rent_increase_pct', '')),
                    estimated_home_price_increase_pct=parse_numeric(row.get('estimated_home_price_increase_pct', '')),
                    neighborhoods_most_impacted=row.get('neighborhoods_most_impacted', ''),
                    housing_affordability_index_change=parse_numeric(row.get('housing_affordability_index_change', '')),
                    vacancy_rate_ltr_pct=parse_numeric(row.get('vacancy_rate_ltr_pct', '')),
                    vacancy_rate_str_pct=parse_numeric(row.get('vacancy_rate_str_pct', '')),
                    data_source=row.get('data_source', ''),
                    period=parse_date(row.get('period', ''))
                )
                session.add(record)
                count += 1
                if count % 100 == 0:
                    session.commit()
                    logger.info(f"Imported {count} STR housing market impact records...")
            except Exception as e:
                logger.error(f"Error importing row: {row}. Error: {e}")
                session.rollback()
                continue
        session.commit()
    logger.info(f"✅ Imported {count} STR housing market impact records")
    return count


def import_str_investment_analysis(csv_path: Path, session: Session) -> int:
    """Import STR investment analysis from CSV"""
    logger.info(f"Importing STR investment analysis from {csv_path}")
    count = 0
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                record = STRInvestmentAnalysis(
                    market=row['market'],
                    property_type=row.get('property_type', ''),
                    avg_acquisition_cost=parse_numeric(row.get('avg_acquisition_cost', '')),
                    avg_renovation_cost=parse_numeric(row.get('avg_renovation_cost', '')),
                    total_upfront_investment=parse_numeric(row.get('total_upfront_investment', '')),
                    annual_gross_revenue=parse_numeric(row.get('annual_gross_revenue', '')),
                    annual_net_operating_income=parse_numeric(row.get('annual_net_operating_income', '')),
                    cash_on_cash_return_pct=parse_numeric(row.get('cash_on_cash_return_pct', '')),
                    cap_rate_pct=parse_numeric(row.get('cap_rate_pct', '')),
                    payback_period_years=parse_numeric(row.get('payback_period_years', '')),
                    irr_5year_pct=parse_numeric(row.get('irr_5year_pct', '')),
                    appreciation_rate_annual_pct=parse_numeric(row.get('appreciation_rate_annual_pct', '')),
                    data_source=row.get('data_source', ''),
                    period=parse_date(row.get('period', ''))
                )
                session.add(record)
                count += 1
                if count % 100 == 0:
                    session.commit()
                    logger.info(f"Imported {count} STR investment analysis records...")
            except Exception as e:
                logger.error(f"Error importing row: {row}. Error: {e}")
                session.rollback()
                continue
        session.commit()
    logger.info(f"✅ Imported {count} STR investment analysis records")
    return count


def import_str_platform_performance(csv_path: Path, session: Session) -> int:
    """Import STR platform performance from CSV"""
    logger.info(f"Importing STR platform performance from {csv_path}")
    count = 0
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                record = STRPlatformPerformance(
                    market=row['market'],
                    platform_name=row['platform_name'],
                    market_share_pct=parse_numeric(row.get('market_share_pct', '')),
                    total_listings=parse_int(row.get('total_listings', '')),
                    active_listings=parse_int(row.get('active_listings', '')),
                    avg_adr=parse_numeric(row.get('avg_adr', '')),
                    avg_occupancy_rate_pct=parse_numeric(row.get('avg_occupancy_rate_pct', '')),
                    booking_volume=parse_int(row.get('booking_volume', '')),
                    gross_booking_value_usd=parse_numeric(row.get('gross_booking_value_usd', '')),
                    commission_rate_pct=parse_numeric(row.get('commission_rate_pct', '')),
                    host_retention_rate_pct=parse_numeric(row.get('host_retention_rate_pct', '')),
                    guest_satisfaction_score=parse_numeric(row.get('guest_satisfaction_score', '')),
                    data_source=row.get('data_source', ''),
                    period=parse_date(row.get('period', ''))
                )
                session.add(record)
                count += 1
                if count % 100 == 0:
                    session.commit()
                    logger.info(f"Imported {count} STR platform performance records...")
            except Exception as e:
                logger.error(f"Error importing row: {row}. Error: {e}")
                session.rollback()
                continue
        session.commit()
    logger.info(f"✅ Imported {count} STR platform performance records")
    return count


def import_str_pricing_patterns(csv_path: Path, session: Session) -> int:
    """Import STR pricing patterns from CSV"""
    logger.info(f"Importing STR pricing patterns from {csv_path}")
    count = 0
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                record = STRPricingPatterns(
                    market=row['market'],
                    property_type=row.get('property_type', ''),
                    season=row.get('season', ''),
                    avg_nightly_rate=parse_numeric(row.get('avg_nightly_rate', '')),
                    min_nightly_rate=parse_numeric(row.get('min_nightly_rate', '')),
                    max_nightly_rate=parse_numeric(row.get('max_nightly_rate', '')),
                    weekend_premium_pct=parse_numeric(row.get('weekend_premium_pct', '')),
                    holiday_premium_pct=parse_numeric(row.get('holiday_premium_pct', '')),
                    special_event_premium_pct=parse_numeric(row.get('special_event_premium_pct', '')),
                    last_minute_discount_pct=parse_numeric(row.get('last_minute_discount_pct', '')),
                    early_booking_discount_pct=parse_numeric(row.get('early_booking_discount_pct', '')),
                    dynamic_pricing_adoption_pct=parse_numeric(row.get('dynamic_pricing_adoption_pct', '')),
                    data_source=row.get('data_source', ''),
                    period=parse_date(row.get('period', ''))
                )
                session.add(record)
                count += 1
                if count % 100 == 0:
                    session.commit()
                    logger.info(f"Imported {count} STR pricing patterns records...")
            except Exception as e:
                logger.error(f"Error importing row: {row}. Error: {e}")
                session.rollback()
                continue
        session.commit()
    logger.info(f"✅ Imported {count} STR pricing patterns records")
    return count


def import_str_supply_demand_dynamics(csv_path: Path, session: Session) -> int:
    """Import STR supply demand dynamics from CSV"""
    logger.info(f"Importing STR supply demand dynamics from {csv_path}")
    count = 0
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                record = STRSupplyDemandDynamics(
                    market=row['market'],
                    total_supply_units=parse_int(row.get('total_supply_units', '')),
                    new_listings_mtd=parse_int(row.get('new_listings_mtd', '')),
                    delisted_units_mtd=parse_int(row.get('delisted_units_mtd', '')),
                    net_supply_change_mtd=parse_int(row.get('net_supply_change_mtd', '')),
                    supply_growth_rate_yoy_pct=parse_numeric(row.get('supply_growth_rate_yoy_pct', '')),
                    total_demand_bookings=parse_int(row.get('total_demand_bookings', '')),
                    demand_growth_rate_yoy_pct=parse_numeric(row.get('demand_growth_rate_yoy_pct', '')),
                    supply_demand_ratio=parse_numeric(row.get('supply_demand_ratio', '')),
                    market_saturation_level=row.get('market_saturation_level', ''),
                    projected_supply_12m=parse_int(row.get('projected_supply_12m', '')),
                    projected_demand_12m=parse_int(row.get('projected_demand_12m', '')),
                    data_source=row.get('data_source', ''),
                    period=parse_date(row.get('period', ''))
                )
                session.add(record)
                count += 1
                if count % 100 == 0:
                    session.commit()
                    logger.info(f"Imported {count} STR supply demand dynamics records...")
            except Exception as e:
                logger.error(f"Error importing row: {row}. Error: {e}")
                session.rollback()
                continue
        session.commit()
    logger.info(f"✅ Imported {count} STR supply demand dynamics records")
    return count


def import_entitled_land_inventory(csv_path: Path, session: Session) -> int:
    """Import entitled land inventory from CSV"""
    logger.info(f"Importing entitled land inventory from {csv_path}")
    count = 0
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                record = EntitledLandInventory(
                    market=row['market'],
                    project_name=row.get('project_name', ''),
                    zone_type=row.get('zone_type', ''),
                    entitled_units=parse_int(row.get('entitled_units', '')),
                    entitled_sf=parse_int(row.get('entitled_sf', '')),
                    project_type=row.get('project_type', ''),
                    approval_date=parse_date(row.get('approval_date', '')),
                    years_since_approval=parse_numeric(row.get('years_since_approval', '')),
                    estimated_land_value_mm=parse_numeric(row.get('estimated_land_value_mm', '')),
                    estimated_built_value_mm=parse_numeric(row.get('estimated_built_value_mm', '')),
                    development_status=row.get('development_status', ''),
                    constraints=row.get('constraints', ''),
                    data_source=row.get('data_source', ''),
                    period=parse_date(row.get('period', ''))
                )
                session.add(record)
                count += 1
                if count % 100 == 0:
                    session.commit()
                    logger.info(f"Imported {count} entitled land inventory records...")
            except Exception as e:
                logger.error(f"Error importing row: {row}. Error: {e}")
                session.rollback()
                continue
        session.commit()
    logger.info(f"✅ Imported {count} entitled land inventory records")
    return count


def import_future_zoning_initiatives(csv_path: Path, session: Session) -> int:
    """Import future zoning initiatives from CSV"""
    logger.info(f"Importing future zoning initiatives from {csv_path}")
    count = 0
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                record = FutureZoningInitiatives(
                    market=row['market'],
                    initiative_name=row['initiative_name'],
                    initiative_type=row.get('initiative_type', ''),
                    area_affected_acres=parse_numeric(row.get('area_affected_acres', '')),
                    neighborhoods_affected=row.get('neighborhoods_affected', ''),
                    current_zoning=row.get('current_zoning', ''),
                    proposed_zoning=row.get('proposed_zoning', ''),
                    estimated_new_units_enabled=parse_int(row.get('estimated_new_units_enabled', '')),
                    estimated_new_sf_enabled=parse_int(row.get('estimated_new_sf_enabled', '')),
                    proposal_date=parse_date(row.get('proposal_date', '')),
                    expected_approval_date=parse_date(row.get('expected_approval_date', '')),
                    approval_likelihood=row.get('approval_likelihood', ''),
                    political_support_level=row.get('political_support_level', ''),
                    data_source=row.get('data_source', ''),
                    period=parse_date(row.get('period', ''))
                )
                session.add(record)
                count += 1
                if count % 100 == 0:
                    session.commit()
                    logger.info(f"Imported {count} future zoning initiatives records...")
            except Exception as e:
                logger.error(f"Error importing row: {row}. Error: {e}")
                session.rollback()
                continue
        session.commit()
    logger.info(f"✅ Imported {count} future zoning initiatives records")
    return count


def import_regulatory_barriers(csv_path: Path, session: Session) -> int:
    """Import regulatory barriers from CSV"""
    logger.info(f"Importing regulatory barriers from {csv_path}")
    count = 0
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                record = RegulatoryBarriers(
                    market=row['market'],
                    barrier_type=row['barrier_type'],
                    barrier_description=row.get('barrier_description', ''),
                    affected_project_types=row.get('affected_project_types', ''),
                    avg_delay_months=parse_numeric(row.get('avg_delay_months', '')),
                    avg_additional_cost_pct=parse_numeric(row.get('avg_additional_cost_pct', '')),
                    projects_impacted_annually=parse_int(row.get('projects_impacted_annually', '')),
                    severity_rating=row.get('severity_rating', ''),
                    potential_reform_status=row.get('potential_reform_status', ''),
                    estimated_units_blocked_annually=parse_int(row.get('estimated_units_blocked_annually', '')),
                    economic_impact_mm=parse_numeric(row.get('economic_impact_mm', '')),
                    data_source=row.get('data_source', ''),
                    period=parse_date(row.get('period', ''))
                )
                session.add(record)
                count += 1
                if count % 100 == 0:
                    session.commit()
                    logger.info(f"Imported {count} regulatory barriers records...")
            except Exception as e:
                logger.error(f"Error importing row: {row}. Error: {e}")
                session.rollback()
                continue
        session.commit()
    logger.info(f"✅ Imported {count} regulatory barriers records")
    return count


def import_transit_oriented_development(csv_path: Path, session: Session) -> int:
    """Import transit oriented development from CSV"""
    logger.info(f"Importing transit oriented development from {csv_path}")
    count = 0
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                record = TransitOrientedDevelopment(
                    market=row['market'],
                    tod_zone_name=row['tod_zone_name'],
                    transit_type=row.get('transit_type', ''),
                    station_name=row.get('station_name', ''),
                    distance_to_station_feet=parse_int(row.get('distance_to_station_feet', '')),
                    current_zoning=row.get('current_zoning', ''),
                    tod_zoning_designation=row.get('tod_zoning_designation', ''),
                    max_far_allowed=parse_numeric(row.get('max_far_allowed', '')),
                    max_height_feet=parse_int(row.get('max_height_feet', '')),
                    parking_reduction_pct=parse_numeric(row.get('parking_reduction_pct', '')),
                    density_bonus_pct=parse_numeric(row.get('density_bonus_pct', '')),
                    developable_acres=parse_numeric(row.get('developable_acres', '')),
                    estimated_units_capacity=parse_int(row.get('estimated_units_capacity', '')),
                    estimated_sf_capacity=parse_int(row.get('estimated_sf_capacity', '')),
                    development_pipeline_units=parse_int(row.get('development_pipeline_units', '')),
                    utilization_rate_pct=parse_numeric(row.get('utilization_rate_pct', '')),
                    data_source=row.get('data_source', ''),
                    period=parse_date(row.get('period', ''))
                )
                session.add(record)
                count += 1
                if count % 100 == 0:
                    session.commit()
                    logger.info(f"Imported {count} transit oriented development records...")
            except Exception as e:
                logger.error(f"Error importing row: {row}. Error: {e}")
                session.rollback()
                continue
        session.commit()
    logger.info(f"✅ Imported {count} transit oriented development records")
    return count


def import_zoning_master_metrics(csv_path: Path, session: Session) -> int:
    """Import zoning master metrics from CSV"""
    logger.info(f"Importing zoning master metrics from {csv_path}")
    count = 0
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                record = ZoningMasterMetrics(
                    market=row['market'],
                    metric_name=row['metric_name'],
                    metric_value=parse_numeric(row.get('metric_value', '')),
                    metric_unit=row.get('metric_unit', ''),
                    metric_category=row.get('metric_category', ''),
                    benchmark_value=parse_numeric(row.get('benchmark_value', '')),
                    variance_from_benchmark_pct=parse_numeric(row.get('variance_from_benchmark_pct', '')),
                    trend_direction=row.get('trend_direction', ''),
                    data_source=row.get('data_source', ''),
                    notes=row.get('notes', ''),
                    period=parse_date(row.get('period', ''))
                )
                session.add(record)
                count += 1
                if count % 100 == 0:
                    session.commit()
                    logger.info(f"Imported {count} zoning master metrics records...")
            except Exception as e:
                logger.error(f"Error importing row: {row}. Error: {e}")
                session.rollback()
                continue
        session.commit()
    logger.info(f"✅ Imported {count} zoning master metrics records")
    return count


def main():
    """Main execution function"""
    try:
        # Create tables
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)

        # Create session
        session = SessionLocal()

        try:
            # CSV file paths
            project_root = Path(__file__).parent.parent.parent.parent
            uploads_dir = project_root / "storage" / "uploads"

            # Import each CSV file
            total_imported = 0

            # 1. Geographic economic indicators - Original file
            geo_indicators_path = uploads_dir / "economic_indicators.csv"
            if geo_indicators_path.exists():
                count = import_geographic_indicators(geo_indicators_path, session)
                total_imported += count
            else:
                logger.warning(f"File not found: {geo_indicators_path}")

            # 2. Geographic economic indicators - Expanded 2024 (metro-level data)
            geo_indicators_expanded_path = uploads_dir / "economic_indicators_expanded_2024.csv"
            if geo_indicators_expanded_path.exists():
                count = import_geographic_indicators(geo_indicators_expanded_path, session)
                total_imported += count
            else:
                logger.warning(f"File not found: {geo_indicators_expanded_path}")

            # 3. Financial markets 2020-2024 (mortgage rates - goes to same table)
            financial_markets_path = uploads_dir / "financial_markets_2020_2024.csv"
            if financial_markets_path.exists():
                count = import_geographic_indicators(financial_markets_path, session)
                total_imported += count
            else:
                logger.warning(f"File not found: {financial_markets_path}")

            # 4. Real estate market data - Original file
            market_data_path = uploads_dir / "market_data.csv"
            if market_data_path.exists():
                count = import_market_data(market_data_path, session)
                total_imported += count
            else:
                logger.warning(f"File not found: {market_data_path}")

            # 5. Real estate market data - Expanded 2024 (national metrics)
            market_data_expanded_path = uploads_dir / "market_data_expanded_2024.csv"
            if market_data_expanded_path.exists():
                count = import_market_data(market_data_expanded_path, session)
                total_imported += count
            else:
                logger.warning(f"File not found: {market_data_expanded_path}")

            # 6. Comparable transactions - Original file
            comp_trans_path = uploads_dir / "comp_transactions.csv"
            if comp_trans_path.exists():
                count = import_comparable_transactions(comp_trans_path, session)
                total_imported += count
            else:
                logger.warning(f"File not found: {comp_trans_path}")

            # 7. Comparable transactions - Expanded 2023-2024
            comp_trans_expanded_path = uploads_dir / "comp_transactions_expanded_2023_2024.csv"
            if comp_trans_expanded_path.exists():
                count = import_comparable_transactions(comp_trans_expanded_path, session)
                total_imported += count
            else:
                logger.warning(f"File not found: {comp_trans_expanded_path}")

            # 8. Institutional capital flows (goes to geographic indicators table)
            institutional_flows_path = uploads_dir / "institutional_capital_flows_2020_2024.csv"
            if institutional_flows_path.exists():
                count = import_geographic_indicators(institutional_flows_path, session)
                total_imported += count
            else:
                logger.warning(f"File not found: {institutional_flows_path}")

            # 9. Hot zones and emerging markets
            hot_zones_path = uploads_dir / "hot_zones_emerging_markets_2024_2025.csv"
            if hot_zones_path.exists():
                count = import_hot_zones(hot_zones_path, session)
                total_imported += count
            else:
                logger.warning(f"File not found: {hot_zones_path}")

            # 10. Neighborhood scoring analysis
            neighborhood_scores_path = uploads_dir / "neighborhood_scoring_analysis_2024.csv"
            if neighborhood_scores_path.exists():
                count = import_neighborhood_scores(neighborhood_scores_path, session)
                total_imported += count
            else:
                logger.warning(f"File not found: {neighborhood_scores_path}")

            # 11. Expanded neighborhoods (NYC, Miami, Chicago, LA)
            expanded_neighborhoods_path = uploads_dir / "expanded_neighborhoods_NYC_Miami_Chicago_LA.csv"
            if expanded_neighborhoods_path.exists():
                count = import_neighborhood_scores(expanded_neighborhoods_path, session)
                total_imported += count
            else:
                logger.warning(f"File not found: {expanded_neighborhoods_path}")

            # ========================================
            # STR (SHORT-TERM RENTAL) DATA
            # ========================================

            # 12. STR Hot Neighborhoods Investment
            str_hot_path = uploads_dir / "str_hot_neighborhoods_investment.csv"
            if str_hot_path.exists():
                count = import_str_hot_neighborhoods(str_hot_path, session)
                total_imported += count
            else:
                logger.warning(f"File not found: {str_hot_path}")

            # 13. STR Performance Metrics by Type
            str_performance_path = uploads_dir / "str_performance_metrics_by_type.csv"
            if str_performance_path.exists():
                count = import_str_performance_metrics(str_performance_path, session)
                total_imported += count
            else:
                logger.warning(f"File not found: {str_performance_path}")

            # 14. STR Market Overview
            str_market_overview_path = uploads_dir / "str_market_overview.csv"
            if str_market_overview_path.exists():
                count = import_str_market_overview(str_market_overview_path, session)
                total_imported += count
            else:
                logger.warning(f"File not found: {str_market_overview_path}")

            # 15. STR Regulatory Environment
            str_regulatory_path = uploads_dir / "str_regulatory_environment.csv"
            if str_regulatory_path.exists():
                count = import_str_regulatory_environment(str_regulatory_path, session)
                total_imported += count
            else:
                logger.warning(f"File not found: {str_regulatory_path}")

            # ========================================
            # ZONING DATA
            # ========================================

            # 16. Zoning Districts Inventory
            zoning_districts_path = uploads_dir / "zoning_districts_inventory.csv"
            if zoning_districts_path.exists():
                count = import_zoning_districts(zoning_districts_path, session)
                total_imported += count
            else:
                logger.warning(f"File not found: {zoning_districts_path}")

            # 17. Zoning Changes and Reforms
            zoning_reforms_path = uploads_dir / "zoning_changes_reforms.csv"
            if zoning_reforms_path.exists():
                count = import_zoning_reforms(zoning_reforms_path, session)
                total_imported += count
            else:
                logger.warning(f"File not found: {zoning_reforms_path}")

            # 18. Opportunity Zones
            opportunity_zones_path = uploads_dir / "opportunity_zones.csv"
            if opportunity_zones_path.exists():
                count = import_opportunity_zones(opportunity_zones_path, session)
                total_imported += count
            else:
                logger.warning(f"File not found: {opportunity_zones_path}")

            # 19. Underbuilt Parcels Analysis
            underbuilt_parcels_path = uploads_dir / "underbuilt_parcels_analysis.csv"
            if underbuilt_parcels_path.exists():
                count = import_underbuilt_parcels(underbuilt_parcels_path, session)
                total_imported += count
            else:
                logger.warning(f"File not found: {underbuilt_parcels_path}")

            # ========================================
            # DEVELOPMENT/LAND DATA
            # ========================================

            # 20. Development Pipeline by Zone
            development_pipeline_path = uploads_dir / "development_pipeline_by_zone.csv"
            if development_pipeline_path.exists():
                count = import_development_pipeline(development_pipeline_path, session)
                total_imported += count
            else:
                logger.warning(f"File not found: {development_pipeline_path}")

            # 21. Land Costs Economics
            land_costs_path = uploads_dir / "land_costs_economics.csv"
            if land_costs_path.exists():
                count = import_land_cost_economics(land_costs_path, session)
                total_imported += count
            else:
                logger.warning(f"File not found: {land_costs_path}")

            # ========================================
            # OTHER DATA
            # ========================================

            # 22. Property Tax Assessments (15 markets)
            property_tax_path = uploads_dir / "property_tax_assessment_15_markets.csv"
            if property_tax_path.exists():
                count = import_property_tax_assessments(property_tax_path, session)
                total_imported += count
            else:
                logger.warning(f"File not found: {property_tax_path}")

            # 23. Tenant Credit Quality Performance
            tenant_credit_path = uploads_dir / "tenant_credit_quality_performance_2024.csv"
            if tenant_credit_path.exists():
                count = import_tenant_credit_quality(tenant_credit_path, session)
                total_imported += count
            else:
                logger.warning(f"File not found: {tenant_credit_path}")

            # ========================================
            # NEW CSV FILES - FINANCIAL TIME-SERIES
            # ========================================

            # 24. Treasury Yield Curve (2020-2025)
            treasury_yield_path = uploads_dir / "treasury_yield_curve_2020_2025.csv"
            if treasury_yield_path.exists():
                count = import_time_series_indicators(treasury_yield_path, session, "treasury_yield_curve")
                total_imported += count
            else:
                logger.warning(f"File not found: {treasury_yield_path}")

            # 25. Fed Policy & Financial Conditions (2020-2025)
            fed_policy_path = uploads_dir / "fed_policy_financial_conditions_2020_2025.csv"
            if fed_policy_path.exists():
                count = import_time_series_indicators(fed_policy_path, session, "fed_policy_financial_conditions")
                total_imported += count
            else:
                logger.warning(f"File not found: {fed_policy_path}")

            # 26. Banking Sector Health (2020-2025)
            banking_path = uploads_dir / "banking_sector_health_2020_2025.csv"
            if banking_path.exists():
                count = import_time_series_indicators(banking_path, session, "banking_sector_health")
                total_imported += count
            else:
                logger.warning(f"File not found: {banking_path}")

            # 27. Credit Markets & Fixed Income (2020-2025)
            credit_markets_path = uploads_dir / "credit_markets_fixed_income_2020_2025.csv"
            if credit_markets_path.exists():
                count = import_time_series_indicators(credit_markets_path, session, "credit_markets_fixed_income")
                total_imported += count
            else:
                logger.warning(f"File not found: {credit_markets_path}")

            # 28. Global Economic Indicators (2020-2025)
            global_econ_path = uploads_dir / "global_economic_indicators_2020_2025.csv"
            if global_econ_path.exists():
                count = import_time_series_indicators(global_econ_path, session, "global_economic_indicators")
                total_imported += count
            else:
                logger.warning(f"File not found: {global_econ_path}")

            # 29. Corporate Earnings & Business Confidence (2020-2025)
            corporate_earnings_path = uploads_dir / "corporate_earnings_business_confidence_2020_2025.csv"
            if corporate_earnings_path.exists():
                count = import_time_series_indicators(corporate_earnings_path, session, "corporate_earnings_business_confidence")
                total_imported += count
            else:
                logger.warning(f"File not found: {corporate_earnings_path}")

            # 30. Consumer Finance & Household Balance Sheet (2020-2025)
            consumer_finance_path = uploads_dir / "consumer_finance_household_balance_sheet_2020_2025.csv"
            if consumer_finance_path.exists():
                count = import_time_series_indicators(consumer_finance_path, session, "consumer_finance_household_balance_sheet")
                total_imported += count
            else:
                logger.warning(f"File not found: {consumer_finance_path}")

            # 31. Currency, Commodities & Construction Costs (2020-2025)
            currency_commodities_path = uploads_dir / "currency_commodities_construction_costs_2020_2025.csv"
            if currency_commodities_path.exists():
                count = import_time_series_indicators(currency_commodities_path, session, "currency_commodities_construction_costs")
                total_imported += count
            else:
                logger.warning(f"File not found: {currency_commodities_path}")

            # 32. Institutional Asset Allocation & Portfolio Positioning (2020-2025)
            institutional_asset_path = uploads_dir / "institutional_asset_allocation_portfolio_positioning_2020_2025.csv"
            if institutional_asset_path.exists():
                count = import_time_series_indicators(institutional_asset_path, session, "institutional_asset_allocation_portfolio_positioning")
                total_imported += count
            else:
                logger.warning(f"File not found: {institutional_asset_path}")

            # ========================================
            # NEW CSV FILES - STR DEEP DIVE
            # ========================================

            # 33. STR Competitive Analysis
            str_competitive_path = uploads_dir / "str_competitive_analysis.csv"
            if str_competitive_path.exists():
                count = import_str_competitive_analysis(str_competitive_path, session)
                total_imported += count
            else:
                logger.warning(f"File not found: {str_competitive_path}")

            # 34. STR Compliance Enforcement
            str_compliance_path = uploads_dir / "str_compliance_enforcement.csv"
            if str_compliance_path.exists():
                count = import_str_compliance_enforcement(str_compliance_path, session)
                total_imported += count
            else:
                logger.warning(f"File not found: {str_compliance_path}")

            # 35. STR Guest Demographics
            str_guest_path = uploads_dir / "str_guest_demographics.csv"
            if str_guest_path.exists():
                count = import_str_guest_demographics(str_guest_path, session)
                total_imported += count
            else:
                logger.warning(f"File not found: {str_guest_path}")

            # 36. STR Host Economics
            str_host_path = uploads_dir / "str_host_economics.csv"
            if str_host_path.exists():
                count = import_str_host_economics(str_host_path, session)
                total_imported += count
            else:
                logger.warning(f"File not found: {str_host_path}")

            # 37. STR Housing Market Impact
            str_housing_path = uploads_dir / "str_housing_market_impact.csv"
            if str_housing_path.exists():
                count = import_str_housing_market_impact(str_housing_path, session)
                total_imported += count
            else:
                logger.warning(f"File not found: {str_housing_path}")

            # 38. STR Investment Analysis
            str_investment_path = uploads_dir / "str_investment_analysis.csv"
            if str_investment_path.exists():
                count = import_str_investment_analysis(str_investment_path, session)
                total_imported += count
            else:
                logger.warning(f"File not found: {str_investment_path}")

            # 39. STR Platform Performance
            str_platform_path = uploads_dir / "str_platform_performance.csv"
            if str_platform_path.exists():
                count = import_str_platform_performance(str_platform_path, session)
                total_imported += count
            else:
                logger.warning(f"File not found: {str_platform_path}")

            # 40. STR Pricing Patterns
            str_pricing_path = uploads_dir / "str_pricing_patterns.csv"
            if str_pricing_path.exists():
                count = import_str_pricing_patterns(str_pricing_path, session)
                total_imported += count
            else:
                logger.warning(f"File not found: {str_pricing_path}")

            # 41. STR Supply Demand Dynamics
            str_supply_demand_path = uploads_dir / "str_supply_demand_dynamics.csv"
            if str_supply_demand_path.exists():
                count = import_str_supply_demand_dynamics(str_supply_demand_path, session)
                total_imported += count
            else:
                logger.warning(f"File not found: {str_supply_demand_path}")

            # ========================================
            # NEW CSV FILES - ADVANCED ZONING/DEVELOPMENT
            # ========================================

            # 42. Entitled Land Inventory
            entitled_land_path = uploads_dir / "entitled_land_inventory.csv"
            if entitled_land_path.exists():
                count = import_entitled_land_inventory(entitled_land_path, session)
                total_imported += count
            else:
                logger.warning(f"File not found: {entitled_land_path}")

            # 43. Future Zoning Initiatives
            future_zoning_path = uploads_dir / "future_zoning_initiatives.csv"
            if future_zoning_path.exists():
                count = import_future_zoning_initiatives(future_zoning_path, session)
                total_imported += count
            else:
                logger.warning(f"File not found: {future_zoning_path}")

            # 44. Regulatory Barriers
            regulatory_barriers_path = uploads_dir / "regulatory_barriers.csv"
            if regulatory_barriers_path.exists():
                count = import_regulatory_barriers(regulatory_barriers_path, session)
                total_imported += count
            else:
                logger.warning(f"File not found: {regulatory_barriers_path}")

            # 45. Transit Oriented Development
            tod_path = uploads_dir / "transit_oriented_development.csv"
            if tod_path.exists():
                count = import_transit_oriented_development(tod_path, session)
                total_imported += count
            else:
                logger.warning(f"File not found: {tod_path}")

            # 46. Zoning Master Metrics Summary
            zoning_master_path = uploads_dir / "zoning_master_metrics_summary.csv"
            if zoning_master_path.exists():
                count = import_zoning_master_metrics(zoning_master_path, session)
                total_imported += count
            else:
                logger.warning(f"File not found: {zoning_master_path}")

            logger.info(f"\n{'='*60}")
            logger.info(f"✅ Import completed successfully!")
            logger.info(f"Total records imported: {total_imported}")
            logger.info(f"{'='*60}\n")

            sys.exit(0)

        finally:
            session.close()

    except Exception as e:
        logger.error(f"❌ Import failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
