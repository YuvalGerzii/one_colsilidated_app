"""
Market Data Models

Models for storing market intelligence data from various sources.
Enables historical tracking and offline access to market indicators.
"""

from datetime import datetime, date
from sqlalchemy import Column, String, Numeric, Date, DateTime, Text, Index
from sqlalchemy.dialects.postgresql import JSONB

from app.models.database import Base, UUIDMixin, TimestampMixin


class EmploymentData(Base, UUIDMixin, TimestampMixin):
    """
    Employment statistics from BLS and other sources

    Tracks unemployment rates, labor force, and employment levels
    """
    __tablename__ = "employment_data"

    # Location
    area_code = Column(String(50), nullable=False, index=True)  # BLS area code
    area_name = Column(String(200))  # Human-readable area name

    # Employment Metrics
    unemployment_rate = Column(Numeric(5, 2))  # Percentage
    labor_force = Column(Numeric(20, 0))  # Total labor force
    employed = Column(Numeric(20, 0))  # Number employed
    unemployed = Column(Numeric(20, 0))  # Number unemployed

    # Additional Metrics
    labor_force_participation_rate = Column(Numeric(5, 2))  # Percentage
    employment_population_ratio = Column(Numeric(5, 2))  # Percentage

    # Metadata
    data_date = Column(Date, nullable=False, index=True)  # Date this data represents
    source = Column(String(100))  # Data source (bls, manual, etc.)
    series_data = Column(JSONB)  # Original series data from API
    notes = Column(Text)

    # Create composite index for faster queries
    __table_args__ = (
        Index('idx_employment_area_date', 'area_code', 'data_date'),
    )


class HousingIndicators(Base, UUIDMixin, TimestampMixin):
    """
    Housing market indicators from FHFA, HUD, and other sources

    Tracks house prices, supply, and market conditions
    """
    __tablename__ = "housing_indicators"

    # Location
    geography_type = Column(String(50), nullable=False)  # national, state, metro, zip
    geography_code = Column(String(50), nullable=False, index=True)  # State code, ZIP, CBSA, etc.
    geography_name = Column(String(200))  # Human-readable name

    # House Price Index
    house_price_index = Column(Numeric(10, 2))  # HPI value
    hpi_year_over_year_change = Column(Numeric(5, 2))  # YoY % change
    hpi_quarter_over_quarter_change = Column(Numeric(5, 2))  # QoQ % change

    # Pricing
    median_sale_price = Column(Numeric(15, 2))  # Median sale price
    median_list_price = Column(Numeric(15, 2))  # Median list price
    average_sale_price = Column(Numeric(15, 2))  # Average sale price

    # Market Conditions
    months_supply = Column(Numeric(5, 2))  # Months of inventory
    inventory_count = Column(Numeric(10, 0))  # Number of homes for sale
    days_on_market = Column(Numeric(10, 1))  # Average days on market

    # Fair Market Rents (from HUD)
    fmr_efficiency = Column(Numeric(10, 2))  # Studio/efficiency FMR
    fmr_1br = Column(Numeric(10, 2))  # 1 bedroom FMR
    fmr_2br = Column(Numeric(10, 2))  # 2 bedroom FMR
    fmr_3br = Column(Numeric(10, 2))  # 3 bedroom FMR
    fmr_4br = Column(Numeric(10, 2))  # 4 bedroom FMR

    # Metadata
    data_date = Column(Date, nullable=False, index=True)
    source = Column(String(100))  # fhfa, hud, realtor, etc.
    raw_data = Column(JSONB)  # Original data from API
    notes = Column(Text)

    __table_args__ = (
        Index('idx_housing_geography_date', 'geography_type', 'geography_code', 'data_date'),
    )


class InterestRates(Base, UUIDMixin, TimestampMixin):
    """
    Interest rates from various sources

    Tracks mortgage rates, treasury yields, and central bank rates
    """
    __tablename__ = "interest_rates"

    # Date
    data_date = Column(Date, nullable=False, index=True)

    # US Rates
    federal_funds_rate = Column(Numeric(5, 3))  # Fed funds rate
    prime_rate = Column(Numeric(5, 3))  # Prime lending rate
    discount_rate = Column(Numeric(5, 3))  # Fed discount window rate

    # Mortgage Rates
    mortgage_30y_fixed = Column(Numeric(5, 3))  # 30-year fixed mortgage
    mortgage_15y_fixed = Column(Numeric(5, 3))  # 15-year fixed mortgage
    mortgage_5y_arm = Column(Numeric(5, 3))  # 5-year ARM
    mortgage_jumbo = Column(Numeric(5, 3))  # Jumbo mortgage rate

    # Treasury Yields
    treasury_1m = Column(Numeric(5, 3))  # 1-month treasury
    treasury_3m = Column(Numeric(5, 3))  # 3-month treasury
    treasury_6m = Column(Numeric(5, 3))  # 6-month treasury
    treasury_1y = Column(Numeric(5, 3))  # 1-year treasury
    treasury_2y = Column(Numeric(5, 3))  # 2-year treasury
    treasury_5y = Column(Numeric(5, 3))  # 5-year treasury
    treasury_10y = Column(Numeric(5, 3))  # 10-year treasury
    treasury_30y = Column(Numeric(5, 3))  # 30-year treasury

    # International Rates (from Bank of Israel, etc.)
    israel_base_rate = Column(Numeric(5, 3))  # Bank of Israel base rate

    # Metadata
    source = Column(String(100))  # fred, bank_of_israel, treasury, etc.
    raw_data = Column(JSONB)  # Original data from API
    notes = Column(Text)


class EconomicIndicators(Base, UUIDMixin, TimestampMixin):
    """
    Economic indicators (CPI, PPI, GDP, etc.)

    Tracks inflation, economic growth, and other macro indicators
    """
    __tablename__ = "real_estate_economic_indicators"

    # Date
    data_date = Column(Date, nullable=False, index=True)
    geography = Column(String(100), default="US")  # Country/region

    # Inflation Indicators
    cpi_all_items = Column(Numeric(10, 4))  # Consumer Price Index
    cpi_year_over_year = Column(Numeric(5, 2))  # CPI YoY % change
    cpi_core = Column(Numeric(10, 4))  # Core CPI (ex food & energy)
    ppi = Column(Numeric(10, 4))  # Producer Price Index
    pce = Column(Numeric(10, 4))  # Personal Consumption Expenditures
    housing_cpi = Column(Numeric(10, 4))  # Housing component of CPI

    # Growth Indicators
    gdp_real = Column(Numeric(15, 2))  # Real GDP (billions)
    gdp_growth_rate = Column(Numeric(5, 2))  # GDP growth rate (%)
    construction_spending = Column(Numeric(15, 2))  # Construction spending (billions)
    residential_construction = Column(Numeric(15, 2))  # Residential construction (billions)

    # Building Permits
    building_permits_total = Column(Numeric(10, 0))  # Total building permits
    building_permits_single_family = Column(Numeric(10, 0))
    building_permits_multi_family = Column(Numeric(10, 0))
    housing_starts = Column(Numeric(10, 0))  # Housing starts
    housing_completions = Column(Numeric(10, 0))  # Housing completions

    # Metadata
    source = Column(String(100))  # bls, fred, census, etc.
    raw_data = Column(JSONB)
    notes = Column(Text)


class MarketDataFetchLog(Base, UUIDMixin, TimestampMixin):
    """
    Log of market data fetch operations

    Tracks success/failure of scheduled data fetches for monitoring
    """
    __tablename__ = "market_data_fetch_log"

    # Fetch Details
    fetch_date = Column(DateTime, nullable=False, index=True)
    data_source = Column(String(100), nullable=False)  # bls, fhfa, hud, etc.
    data_type = Column(String(100), nullable=False)  # employment, housing, rates, etc.

    # Status
    success = Column(String(20), nullable=False)  # success, partial, failed
    records_fetched = Column(Numeric(10, 0), default=0)
    records_saved = Column(Numeric(10, 0), default=0)

    # Error Handling
    error_message = Column(Text)
    retry_count = Column(Numeric(5, 0), default=0)

    # Performance
    duration_seconds = Column(Numeric(10, 3))  # How long the fetch took

    # Metadata
    fetch_metadata = Column(JSONB)  # Additional details about the fetch


# Export all models
__all__ = [
    "EmploymentData",
    "HousingIndicators",
    "InterestRates",
    "EconomicIndicators",
    "MarketDataFetchLog",
]
