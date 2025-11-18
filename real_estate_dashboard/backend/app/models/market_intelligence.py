"""
Market Intelligence Database Models

Stores data from various government APIs and scraped sources:
- Census demographics & housing
- FRED economic indicators
- HUD Fair Market Rent
- BLS employment data
- SEC EDGAR REIT data
- EPA environmental hazards
- NOAA climate risk
- Scraped property listings
"""

from datetime import datetime, date
from typing import Optional
from decimal import Decimal

from sqlalchemy import Column, Integer, String, Float, DateTime, Date, Text, Boolean, JSON, Numeric, Index
from sqlalchemy.sql import func

from app.core.database import Base


class CensusData(Base):
    """Census Bureau - Demographics & Housing Data"""
    __tablename__ = "census_data"

    id = Column(Integer, primary_key=True, index=True)

    # Geographic identifiers
    geo_level = Column(String(50), nullable=False, index=True)  # nation, state, county, msa, tract
    geo_id = Column(String(50), nullable=False, index=True)     # FIPS code or GEO ID
    geo_name = Column(String(200), nullable=False)
    state_code = Column(String(2), index=True)
    county_code = Column(String(5), index=True)

    # Time period
    year = Column(Integer, nullable=False, index=True)
    dataset = Column(String(50), nullable=False)  # acs5, acs1, dec

    # Housing metrics
    total_housing_units = Column(Integer)
    occupied_units = Column(Integer)
    vacant_units = Column(Integer)
    owner_occupied = Column(Integer)
    renter_occupied = Column(Integer)
    median_home_value = Column(Integer)
    median_gross_rent = Column(Integer)
    median_year_built = Column(Integer)

    # Demographics
    total_population = Column(Integer)
    median_age = Column(Float)
    median_household_income = Column(Integer)
    per_capita_income = Column(Integer)
    poverty_rate = Column(Float)
    unemployment_rate = Column(Float)
    bachelors_degree_pct = Column(Float)

    # Additional fields
    raw_data = Column(JSON)  # Store full response

    # Timestamps
    data_date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index('idx_census_geo_year', 'geo_level', 'geo_id', 'year'),
        Index('idx_census_state_year', 'state_code', 'year'),
    )


class FREDIndicator(Base):
    """Federal Reserve Economic Data - Time Series"""
    __tablename__ = "fred_indicators"

    id = Column(Integer, primary_key=True, index=True)

    # Series identification
    series_id = Column(String(50), nullable=False, index=True)  # e.g., HOUST, MORTGAGE30US
    series_name = Column(String(200), nullable=False)
    category = Column(String(100), index=True)  # housing, interest_rates, construction, etc.

    # Data point
    observation_date = Column(Date, nullable=False, index=True)
    value = Column(Numeric(20, 6))

    # Metadata
    frequency = Column(String(20))  # daily, monthly, quarterly, annual
    units = Column(String(100))     # percent, thousands, index
    seasonal_adjustment = Column(String(50))

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index('idx_fred_series_date', 'series_id', 'observation_date'),
    )


class HUDFairMarketRent(Base):
    """HUD Fair Market Rent Data"""
    __tablename__ = "hud_fair_market_rents"

    id = Column(Integer, primary_key=True, index=True)

    # Geographic identifiers
    fips_code = Column(String(5), nullable=False, index=True)
    county_name = Column(String(200), nullable=False)
    state_code = Column(String(2), nullable=False, index=True)
    metro_code = Column(String(10), index=True)
    metro_name = Column(String(200))

    # Time period
    fiscal_year = Column(Integer, nullable=False, index=True)

    # FMR values (monthly rents)
    fmr_0br = Column(Integer)  # Efficiency
    fmr_1br = Column(Integer)
    fmr_2br = Column(Integer)
    fmr_3br = Column(Integer)
    fmr_4br = Column(Integer)

    # Income limits (annual)
    median_family_income = Column(Integer)
    very_low_income_limit = Column(Integer)   # 50% MFI
    extremely_low_income_limit = Column(Integer)  # 30% MFI
    low_income_limit = Column(Integer)        # 80% MFI

    # Metadata
    fmr_type = Column(String(50))  # Small Area FMR, Metro FMR, etc.

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index('idx_hud_fips_year', 'fips_code', 'fiscal_year'),
        Index('idx_hud_state_year', 'state_code', 'fiscal_year'),
    )


class BLSEmployment(Base):
    """Bureau of Labor Statistics - Employment Data"""
    __tablename__ = "bls_employment"

    id = Column(Integer, primary_key=True, index=True)

    # Series identification
    series_id = Column(String(50), nullable=False, index=True)
    area_code = Column(String(20), nullable=False, index=True)  # National, state, or metro area
    area_name = Column(String(200), nullable=False)

    # Data point
    period_date = Column(Date, nullable=False, index=True)
    year = Column(Integer, nullable=False)
    period = Column(String(10), nullable=False)  # M01-M12, Q01-Q04, A01

    # Employment metrics
    unemployment_rate = Column(Numeric(5, 2))
    employment_level = Column(Integer)
    unemployment_level = Column(Integer)
    labor_force = Column(Integer)

    # Industry-specific (if available)
    industry_code = Column(String(20))
    industry_name = Column(String(200))

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index('idx_bls_area_date', 'area_code', 'period_date'),
    )


class SECREITData(Base):
    """SEC EDGAR - REIT Financial Data"""
    __tablename__ = "sec_reit_data"

    id = Column(Integer, primary_key=True, index=True)

    # Company identification
    cik = Column(String(10), nullable=False, index=True)  # Central Index Key
    company_name = Column(String(200), nullable=False)
    ticker = Column(String(10), index=True)

    # Filing information
    filing_type = Column(String(10), nullable=False)  # 10-K, 10-Q, 8-K
    filing_date = Column(Date, nullable=False, index=True)
    period_end_date = Column(Date)

    # Financial metrics (from XBRL)
    total_assets = Column(Numeric(20, 2))
    total_liabilities = Column(Numeric(20, 2))
    stockholders_equity = Column(Numeric(20, 2))
    revenues = Column(Numeric(20, 2))
    net_income = Column(Numeric(20, 2))
    funds_from_operations = Column(Numeric(20, 2))  # FFO - key REIT metric

    # Property portfolio
    number_of_properties = Column(Integer)
    total_square_footage = Column(Numeric(15, 2))
    occupancy_rate = Column(Numeric(5, 2))

    # Additional data
    raw_data = Column(JSON)  # Store full XBRL data

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index('idx_sec_cik_filing_date', 'cik', 'filing_date'),
        Index('idx_sec_ticker_date', 'ticker', 'filing_date'),
    )


class EPAEnvironmentalHazard(Base):
    """EPA - Environmental Hazards Data"""
    __tablename__ = "epa_environmental_hazards"

    id = Column(Integer, primary_key=True, index=True)

    # Site identification
    epa_id = Column(String(50), nullable=False, unique=True, index=True)
    site_name = Column(String(300), nullable=False)

    # Location
    address = Column(String(300))
    city = Column(String(100))
    state_code = Column(String(2), nullable=False, index=True)
    zip_code = Column(String(10), index=True)
    county = Column(String(100))
    latitude = Column(Numeric(10, 7))
    longitude = Column(Numeric(10, 7))

    # Hazard information
    hazard_type = Column(String(100))  # superfund, toxic_release, etc.
    status = Column(String(100))       # active, proposed, final, deleted
    npl_status = Column(String(100))   # National Priorities List status

    # Risk assessment
    contamination_level = Column(String(50))
    chemicals_present = Column(Text)
    cleanup_status = Column(String(100))

    # Dates
    discovery_date = Column(Date)
    listing_date = Column(Date)
    deletion_date = Column(Date)

    # Additional data
    raw_data = Column(JSON)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index('idx_epa_state_zip', 'state_code', 'zip_code'),
        Index('idx_epa_location', 'state_code', 'city'),
    )


class NOAAClimateData(Base):
    """NOAA - Climate & Weather Risk Data"""
    __tablename__ = "noaa_climate_data"

    id = Column(Integer, primary_key=True, index=True)

    # Station/Location
    station_id = Column(String(50), nullable=False, index=True)
    station_name = Column(String(200))
    latitude = Column(Numeric(10, 7))
    longitude = Column(Numeric(10, 7))
    elevation = Column(Numeric(10, 2))

    # Geographic area
    state_code = Column(String(2), index=True)
    county = Column(String(100))

    # Time period
    observation_date = Column(Date, nullable=False, index=True)
    data_type = Column(String(50), nullable=False)  # TMAX, TMIN, PRCP, SNOW, etc.

    # Weather data
    value = Column(Numeric(10, 2))
    units = Column(String(20))

    # Risk indicators
    extreme_event_type = Column(String(100))  # flood, hurricane, tornado, etc.
    severity_level = Column(String(20))

    # Additional data
    raw_data = Column(JSON)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index('idx_noaa_station_date', 'station_id', 'observation_date'),
        Index('idx_noaa_state_date', 'state_code', 'observation_date'),
    )


class PropertyListing(Base):
    """Scraped Property Listings from Zillow, Realtor.com, Redfin"""
    __tablename__ = "property_listings"

    id = Column(Integer, primary_key=True, index=True)

    # Source
    source = Column(String(50), nullable=False, index=True)  # zillow, realtor, redfin
    source_id = Column(String(100), index=True)  # Original listing ID
    source_url = Column(String(500))

    # Location
    address = Column(String(300))
    city = Column(String(100), index=True)
    state_code = Column(String(2), nullable=False, index=True)
    zip_code = Column(String(10), index=True)
    county = Column(String(100))
    latitude = Column(Numeric(10, 7))
    longitude = Column(Numeric(10, 7))

    # Property details
    property_type = Column(String(50), index=True)  # single_family, condo, townhouse, multi_family
    listing_type = Column(String(20), index=True)   # for_sale, for_rent, sold, pending
    status = Column(String(50))

    # Pricing
    price = Column(Numeric(15, 2))
    price_per_sqft = Column(Numeric(10, 2))
    rent_estimate = Column(Numeric(10, 2))
    hoa_fees = Column(Numeric(10, 2))
    property_tax = Column(Numeric(10, 2))

    # Property specs
    bedrooms = Column(Integer)
    bathrooms = Column(Numeric(3, 1))
    square_footage = Column(Integer)
    lot_size = Column(Numeric(12, 2))
    year_built = Column(Integer)

    # Listing dates
    listing_date = Column(Date)
    last_sold_date = Column(Date)
    last_sold_price = Column(Numeric(15, 2))
    days_on_market = Column(Integer)

    # Additional features
    description = Column(Text)
    features = Column(JSON)  # amenities, parking, etc.
    photos = Column(JSON)    # photo URLs

    # Market analysis
    estimated_value = Column(Numeric(15, 2))
    value_range_low = Column(Numeric(15, 2))
    value_range_high = Column(Numeric(15, 2))

    # Timestamps
    scraped_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index('idx_listing_state_city', 'state_code', 'city'),
        Index('idx_listing_zip_type', 'zip_code', 'property_type'),
        Index('idx_listing_price_range', 'price', 'property_type'),
    )


class MarketDataImport(Base):
    """Track data import jobs and their status"""
    __tablename__ = "market_data_imports"

    id = Column(Integer, primary_key=True, index=True)

    # Import job details
    data_source = Column(String(50), nullable=False, index=True)  # census, fred, hud, bls, etc.
    import_type = Column(String(50), nullable=False)  # full, incremental, backfill
    status = Column(String(20), nullable=False, index=True)  # pending, running, completed, failed

    # Time range
    start_date = Column(Date)
    end_date = Column(Date)

    # Results
    records_processed = Column(Integer, default=0)
    records_inserted = Column(Integer, default=0)
    records_updated = Column(Integer, default=0)
    records_failed = Column(Integer, default=0)

    # Error handling
    error_message = Column(Text)
    error_details = Column(JSON)

    # Timing
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    duration_seconds = Column(Integer)

    # Scheduling
    scheduled_by = Column(String(50))  # manual, cron, api
    next_scheduled_run = Column(DateTime(timezone=True))

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index('idx_import_source_status', 'data_source', 'status'),
        Index('idx_import_completed', 'completed_at'),
    )


class YFinanceMarketData(Base):
    """Yahoo Finance - Stock, REIT, and Index Data"""
    __tablename__ = "yfinance_market_data"

    id = Column(Integer, primary_key=True, index=True)

    # Ticker identification
    ticker = Column(String(20), nullable=False, index=True)
    company_name = Column(String(200))
    security_type = Column(String(50), index=True)  # stock, reit, etf, index

    # Price data
    current_price = Column(Numeric(20, 6))
    currency = Column(String(10))
    price_change = Column(Numeric(20, 6))
    price_change_pct = Column(Numeric(10, 4))

    # Volume and market data
    volume = Column(Integer)
    market_cap = Column(Integer)

    # Valuation metrics
    pe_ratio = Column(Numeric(10, 4))
    dividend_yield = Column(Numeric(10, 6))

    # 52-week range
    week_52_high = Column(Numeric(20, 6))
    week_52_low = Column(Numeric(20, 6))

    # Classification
    sector = Column(String(100), index=True)
    industry = Column(String(100), index=True)

    # Historical data (stored as JSON)
    historical_data = Column(JSON)  # Array of {date, open, high, low, close, volume}

    # Data period info
    data_period = Column(String(20))  # 1mo, 3mo, 1y, etc.
    data_interval = Column(String(20))  # 1d, 1wk, 1mo, etc.

    # Timestamps
    data_timestamp = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index('idx_yfinance_ticker_timestamp', 'ticker', 'data_timestamp'),
        Index('idx_yfinance_type_sector', 'security_type', 'sector'),
    )


class EconomicsAPIIndicator(Base):
    """Economics API - Macroeconomic Indicators from Trading Economics"""
    __tablename__ = "economics_api_indicators"

    id = Column(Integer, primary_key=True, index=True)

    # Country identification
    country = Column(String(100), nullable=False, index=True)
    country_code = Column(String(3), index=True)  # ISO 3-letter code

    # Indicator classification
    category = Column(String(50), nullable=False, index=True)  # overview, gdp, labour, prices, etc.
    indicator_name = Column(String(200), nullable=False)
    indicator_code = Column(String(100))

    # Indicator value
    value = Column(Numeric(20, 6))
    previous_value = Column(Numeric(20, 6))
    value_change = Column(Numeric(20, 6))
    value_change_pct = Column(Numeric(10, 4))

    # Metadata
    units = Column(String(100))  # percent, billions, index, etc.
    frequency = Column(String(50))  # monthly, quarterly, annual

    # Time period
    reference_date = Column(Date, nullable=False, index=True)
    next_release_date = Column(Date)

    # Raw data from API
    raw_data = Column(JSON)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index('idx_economic_country_category', 'country', 'category'),
        Index('idx_economic_category_date', 'category', 'reference_date'),
        Index('idx_economic_indicator', 'indicator_name', 'reference_date'),
    )


class MarketIntelligenceSnapshot(Base):
    """Comprehensive Market Intelligence Snapshot"""
    __tablename__ = "market_intelligence_snapshots"

    id = Column(Integer, primary_key=True, index=True)

    # Snapshot identification
    snapshot_date = Column(Date, nullable=False, index=True)
    snapshot_type = Column(String(50), index=True)  # daily, weekly, monthly

    # Market indices
    sp500_value = Column(Numeric(20, 6))
    sp500_change_pct = Column(Numeric(10, 4))
    dow_jones_value = Column(Numeric(20, 6))
    nasdaq_value = Column(Numeric(20, 6))
    vix_value = Column(Numeric(20, 6))

    # REIT performance
    reit_etf_vnq = Column(Numeric(20, 6))
    reit_sector_change_pct = Column(Numeric(10, 4))

    # Interest rates
    treasury_10y = Column(Numeric(10, 6))
    treasury_30y = Column(Numeric(10, 6))
    fed_funds_rate = Column(Numeric(10, 6))
    mortgage_30y = Column(Numeric(10, 6))

    # Economic indicators
    unemployment_rate = Column(Numeric(10, 4))
    inflation_rate = Column(Numeric(10, 4))
    gdp_growth_rate = Column(Numeric(10, 4))

    # Housing indicators
    home_price_index = Column(Numeric(20, 6))
    housing_starts = Column(Integer)
    building_permits = Column(Integer)

    # Comprehensive data
    full_data = Column(JSON)  # Store complete snapshot data

    # Data quality
    data_completeness_pct = Column(Numeric(5, 2))  # Percentage of data points available
    data_sources_count = Column(Integer)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index('idx_snapshot_date_type', 'snapshot_date', 'snapshot_type'),
    )
