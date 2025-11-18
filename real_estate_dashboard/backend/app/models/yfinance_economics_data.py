"""
YFinance and Economics API Data Models

Models for storing market intelligence data from Yahoo Finance and Economics API.
Enables historical tracking, trend analysis, and offline access to global market data.
"""

from datetime import datetime, date
from sqlalchemy import Column, String, Numeric, Date, DateTime, Text, Index, Boolean
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app.models.database import Base, UUIDMixin, TimestampMixin


class MarketIndex(Base, UUIDMixin, TimestampMixin):
    """
    Market indices from Yahoo Finance (S&P 500, NASDAQ, DOW, etc.)

    Tracks major stock market indices for trend analysis and market sentiment
    """
    __tablename__ = "market_indices"

    # Index Details
    symbol = Column(String(20), nullable=False, index=True)  # ^GSPC, ^IXIC, ^DJI, etc.
    name = Column(String(200), nullable=False)  # S&P 500, NASDAQ Composite, etc.

    # Price Data
    current_value = Column(Numeric(15, 2))  # Current index value
    open_value = Column(Numeric(15, 2))  # Opening value
    high_value = Column(Numeric(15, 2))  # Daily high
    low_value = Column(Numeric(15, 2))  # Daily low
    previous_close = Column(Numeric(15, 2))  # Previous closing value

    # Changes
    price_change = Column(Numeric(15, 2))  # Absolute change
    price_change_pct = Column(Numeric(10, 4))  # Percentage change

    # Volume
    volume = Column(Numeric(20, 0))  # Trading volume

    # Metadata
    data_date = Column(Date, nullable=False, index=True)  # Date of this data
    currency = Column(String(10), default="USD")
    market = Column(String(50))  # US, International, etc.
    source = Column(String(50), default="yfinance")
    raw_data = Column(JSONB)  # Original data from yfinance
    notes = Column(Text)

    __table_args__ = (
        Index('idx_market_index_symbol_date', 'symbol', 'data_date'),
    )


class REITData(Base, UUIDMixin, TimestampMixin):
    """
    Real Estate Investment Trust (REIT) data from Yahoo Finance

    Tracks REIT performance, dividends, and market metrics
    """
    __tablename__ = "reit_data"

    # REIT Details
    ticker = Column(String(20), nullable=False, index=True)  # VNQ, O, VICI, etc.
    company_name = Column(String(300))  # Full company name
    sector = Column(String(100))  # Residential, Retail, Office, Industrial, etc.

    # Price Data
    current_price = Column(Numeric(15, 2))  # Current share price
    day_high = Column(Numeric(15, 2))  # Daily high
    day_low = Column(Numeric(15, 2))  # Daily low
    previous_close = Column(Numeric(15, 2))  # Previous close

    # Changes
    price_change = Column(Numeric(15, 2))  # Absolute change
    price_change_pct = Column(Numeric(10, 4))  # Percentage change

    # Dividend Information
    dividend_yield = Column(Numeric(8, 4))  # Dividend yield as decimal (0.05 = 5%)
    annual_dividend = Column(Numeric(15, 2))  # Annual dividend per share
    dividend_date = Column(Date)  # Next/last dividend date
    ex_dividend_date = Column(Date)  # Ex-dividend date
    payout_ratio = Column(Numeric(8, 4))  # Payout ratio

    # Market Metrics
    market_cap = Column(Numeric(20, 0))  # Market capitalization
    volume = Column(Numeric(20, 0))  # Trading volume
    average_volume = Column(Numeric(20, 0))  # Average volume
    pe_ratio = Column(Numeric(10, 2))  # Price-to-earnings ratio
    beta = Column(Numeric(10, 4))  # Beta (volatility measure)

    # Performance
    week_52_high = Column(Numeric(15, 2))  # 52-week high
    week_52_low = Column(Numeric(15, 2))  # 52-week low
    ytd_return = Column(Numeric(10, 4))  # Year-to-date return

    # Metadata
    data_date = Column(Date, nullable=False, index=True)
    currency = Column(String(10), default="USD")
    exchange = Column(String(50))  # NYSE, NASDAQ, etc.
    source = Column(String(50), default="yfinance")
    is_active = Column(Boolean, default=True)  # Whether still tracking
    raw_data = Column(JSONB)
    notes = Column(Text)

    __table_args__ = (
        Index('idx_reit_ticker_date', 'ticker', 'data_date'),
        Index('idx_reit_sector', 'sector'),
    )


class TreasuryRate(Base, UUIDMixin, TimestampMixin):
    """
    US Treasury rates and yields from Yahoo Finance

    Tracks treasury bond yields for interest rate analysis
    """
    __tablename__ = "treasury_rates"

    # Treasury Details
    symbol = Column(String(20), nullable=False, index=True)  # ^IRX, ^FVX, ^TNX, ^TYX
    name = Column(String(200))  # 13 Week, 5 Year, 10 Year, 30 Year
    maturity = Column(String(50))  # 3-month, 2-year, 10-year, etc.

    # Rate Data
    rate = Column(Numeric(8, 4), nullable=False)  # Yield as percentage
    previous_rate = Column(Numeric(8, 4))  # Previous rate
    rate_change = Column(Numeric(8, 4))  # Absolute change
    rate_change_pct = Column(Numeric(10, 4))  # Percentage change

    # Historical Context
    week_52_high = Column(Numeric(8, 4))  # 52-week high
    week_52_low = Column(Numeric(8, 4))  # 52-week low

    # Metadata
    data_date = Column(Date, nullable=False, index=True)
    source = Column(String(50), default="yfinance")
    raw_data = Column(JSONB)
    notes = Column(Text)

    __table_args__ = (
        Index('idx_treasury_symbol_date', 'symbol', 'data_date'),
    )


class StockData(Base, UUIDMixin, TimestampMixin):
    """
    Individual stock data from Yahoo Finance

    Tracks stock performance for companies relevant to real estate
    """
    __tablename__ = "stock_data"

    # Stock Details
    ticker = Column(String(20), nullable=False, index=True)
    company_name = Column(String(300))
    sector = Column(String(100))  # Real Estate, Financials, Construction, etc.
    industry = Column(String(100))  # More specific industry

    # Price Data
    current_price = Column(Numeric(15, 2))
    open_price = Column(Numeric(15, 2))
    high_price = Column(Numeric(15, 2))
    low_price = Column(Numeric(15, 2))
    previous_close = Column(Numeric(15, 2))

    # Changes
    price_change = Column(Numeric(15, 2))
    price_change_pct = Column(Numeric(10, 4))

    # Volume & Metrics
    volume = Column(Numeric(20, 0))
    market_cap = Column(Numeric(20, 0))
    pe_ratio = Column(Numeric(10, 2))
    dividend_yield = Column(Numeric(8, 4))
    beta = Column(Numeric(10, 4))

    # Metadata
    data_date = Column(Date, nullable=False, index=True)
    currency = Column(String(10), default="USD")
    exchange = Column(String(50))
    source = Column(String(50), default="yfinance")
    is_tracked = Column(Boolean, default=True)
    raw_data = Column(JSONB)
    notes = Column(Text)

    __table_args__ = (
        Index('idx_stock_ticker_date', 'ticker', 'data_date'),
        Index('idx_stock_sector', 'sector'),
    )


class GlobalEconomicIndicator(Base, UUIDMixin, TimestampMixin):
    """
    Economic indicators from Economics API (Trading Economics)

    Tracks GDP, employment, inflation, housing data for multiple countries
    """
    __tablename__ = "global_economic_indicators"

    # Location
    country = Column(String(100), nullable=False, index=True)  # united-states, israel, etc.
    country_code = Column(String(10))  # ISO country code

    # Indicator Details
    category = Column(String(100), nullable=False, index=True)  # gdp, labour, housing, prices, etc.
    indicator_name = Column(String(300), nullable=False)  # GDP Growth Rate, Unemployment Rate, etc.
    indicator_code = Column(String(100))  # Unique identifier from API

    # Value Data
    value = Column(Numeric(20, 4))  # The indicator value
    previous_value = Column(Numeric(20, 4))  # Previous period value
    change = Column(Numeric(20, 4))  # Absolute change
    change_pct = Column(Numeric(10, 4))  # Percentage change

    # Context
    forecast = Column(Numeric(20, 4))  # Forecasted value
    unit = Column(String(50))  # percent, billion USD, thousands, etc.
    frequency = Column(String(50))  # Monthly, Quarterly, Annually

    # Time Period
    data_date = Column(Date, nullable=False, index=True)
    period = Column(String(50))  # Q1 2024, Jan 2024, etc.

    # Metadata
    source = Column(String(50), default="economics-api")
    source_organization = Column(String(200))  # BLS, Census, Trading Economics, etc.
    last_updated = Column(DateTime)
    raw_data = Column(JSONB)
    notes = Column(Text)

    __table_args__ = (
        Index('idx_global_economic_country_category', 'country', 'category', 'data_date'),
        Index('idx_global_economic_indicator', 'indicator_name', 'data_date'),
    )


class MarketIntelligenceFetchLog(Base, UUIDMixin, TimestampMixin):
    """
    Log of market intelligence data fetch operations

    Tracks success/failure of YFinance and Economics API data fetches
    """
    __tablename__ = "market_intelligence_fetch_log"

    # Fetch Details
    fetch_timestamp = Column(DateTime, nullable=False, index=True, default=datetime.utcnow)
    data_source = Column(String(100), nullable=False)  # yfinance, economics-api
    data_type = Column(String(100), nullable=False)  # market_indices, reits, treasury, economic_indicators
    endpoint = Column(String(300))  # API endpoint used

    # Status
    status = Column(String(20), nullable=False)  # success, partial, failed
    records_fetched = Column(Numeric(10, 0), default=0)
    records_saved = Column(Numeric(10, 0), default=0)
    records_updated = Column(Numeric(10, 0), default=0)

    # Error Handling
    has_errors = Column(Boolean, default=False)
    error_message = Column(Text)
    error_details = Column(JSONB)
    retry_count = Column(Numeric(5, 0), default=0)
    max_retries = Column(Numeric(5, 0), default=3)

    # Performance
    duration_seconds = Column(Numeric(10, 3))
    cache_hit = Column(Boolean, default=False)
    cache_ttl = Column(Numeric(10, 0))  # Cache TTL in seconds

    # Request Details
    request_params = Column(JSONB)  # Parameters used in the request
    response_summary = Column(JSONB)  # Summary of response

    # Metadata
    user_id = Column(UUID(as_uuid=True), nullable=True)  # If user-initiated
    automated = Column(Boolean, default=True)  # Whether scheduled or manual
    fetch_metadata = Column(JSONB)

    __table_args__ = (
        Index('idx_fetch_log_source_type', 'data_source', 'data_type', 'fetch_timestamp'),
        Index('idx_fetch_log_status', 'status', 'fetch_timestamp'),
    )


class CountryFilter(Base, UUIDMixin, TimestampMixin):
    """
    User preferences for country/region filters

    Stores which countries/regions users want to track
    """
    __tablename__ = "country_filters"

    # User Association
    user_id = Column(UUID(as_uuid=True), nullable=True, index=True)  # Null = global default
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=True)

    # Filter Details
    country = Column(String(100), nullable=False)  # united-states, israel, etc.
    country_code = Column(String(10))
    country_display_name = Column(String(200))  # United States, Israel, etc.

    # US-Specific Filters
    state = Column(String(100))  # For US data filtering
    state_code = Column(String(10))  # CA, NY, TX, etc.
    metro_area = Column(String(200))  # Metropolitan areas

    # Priority & Display
    is_primary = Column(Boolean, default=False)  # Primary country for dashboard
    display_order = Column(Numeric(5, 0), default=0)  # Order in UI
    is_active = Column(Boolean, default=True)

    # Data Categories to Track
    track_economic_indicators = Column(Boolean, default=True)
    track_housing_data = Column(Boolean, default=True)
    track_employment_data = Column(Boolean, default=True)
    track_interest_rates = Column(Boolean, default=True)

    # Preferences
    preferences = Column(JSONB)  # Additional user preferences
    notes = Column(Text)

    __table_args__ = (
        Index('idx_country_filter_user', 'user_id', 'country'),
        Index('idx_country_filter_company', 'company_id', 'country'),
    )


# Export all models
__all__ = [
    "MarketIndex",
    "REITData",
    "TreasuryRate",
    "StockData",
    "GlobalEconomicIndicator",
    "MarketIntelligenceFetchLog",
    "CountryFilter",
]
