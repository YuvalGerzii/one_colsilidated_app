"""
Economics Database Models

Stores macroeconomic data from Sugra AI Economics API:
- Country overviews
- Economic indicators (GDP, labour, prices, housing, etc.)
- Time series data with historical tracking
"""

from sqlalchemy import Column, Integer, Float, String, JSON, DateTime, Text, Index, UniqueConstraint
from sqlalchemy.sql import func
from app.models.database import Base, TimestampMixin, UUIDMixin


class CountryEconomicOverview(Base, UUIDMixin, TimestampMixin):
    """Country-level economic overview snapshot."""

    __tablename__ = "economics_country_overview"

    # Country identification
    country_name = Column(String(100), nullable=False, index=True, comment="Country name")
    country_code = Column(String(10), nullable=True, index=True, comment="ISO country code")

    # Economic snapshot metrics
    gdp = Column(Float, nullable=True, comment="GDP in billions USD")
    gdp_growth = Column(Float, nullable=True, comment="GDP growth rate %")
    inflation_rate = Column(Float, nullable=True, comment="Inflation rate %")
    interest_rate = Column(Float, nullable=True, comment="Interest rate %")
    unemployment_rate = Column(Float, nullable=True, comment="Unemployment/Jobless rate %")
    population = Column(Float, nullable=True, comment="Population in millions")

    # Fiscal metrics
    current_account = Column(Float, nullable=True, comment="Current account % of GDP")
    debt_to_gdp = Column(Float, nullable=True, comment="Debt to GDP ratio %")
    government_budget = Column(Float, nullable=True, comment="Government budget % of GDP")

    # Metadata
    data_date = Column(DateTime, nullable=True, index=True, comment="Date of the data snapshot")
    data_source = Column(String(50), default="economics-api", comment="Data source identifier")
    raw_data = Column(JSON, nullable=True, comment="Raw API response")

    __table_args__ = (
        Index('ix_country_date', 'country_name', 'data_date'),
        UniqueConstraint('country_name', 'data_date', name='uq_country_overview_snapshot'),
    )


class EconomicIndicator(Base, UUIDMixin, TimestampMixin):
    """Individual economic indicator data point."""

    __tablename__ = "economics_indicators"

    # Identification
    country_name = Column(String(100), nullable=False, index=True, comment="Country name")
    category = Column(String(50), nullable=False, index=True, comment="Indicator category (gdp, labour, housing, etc.)")
    indicator_name = Column(String(255), nullable=False, index=True, comment="Specific indicator name")

    # Values
    last_value = Column(String(50), nullable=True, comment="Latest value (as string to handle formats)")
    last_value_numeric = Column(Float, nullable=True, comment="Latest value as number")
    previous_value = Column(String(50), nullable=True, comment="Previous value")
    previous_value_numeric = Column(Float, nullable=True, comment="Previous value as number")
    highest_value = Column(String(50), nullable=True, comment="Historical highest value")
    highest_value_numeric = Column(Float, nullable=True, comment="Historical highest as number")
    lowest_value = Column(String(50), nullable=True, comment="Historical lowest value")
    lowest_value_numeric = Column(Float, nullable=True, comment="Historical lowest as number")

    # Metadata
    unit = Column(String(100), nullable=True, comment="Unit of measurement")
    frequency = Column(String(50), nullable=True, comment="Update frequency (monthly, quarterly, etc.)")
    reference_period = Column(String(50), nullable=True, comment="Reference period (e.g., Nov/25)")
    data_date = Column(DateTime, nullable=True, index=True, comment="Date of the data")
    source = Column(String(255), nullable=True, comment="Data source/provider")

    # Raw data
    raw_data = Column(JSON, nullable=True, comment="Raw API response for this indicator")
    data_source_api = Column(String(50), default="economics-api", comment="API source")

    __table_args__ = (
        Index('ix_country_category_indicator', 'country_name', 'category', 'indicator_name'),
        Index('ix_category_date', 'category', 'data_date'),
        UniqueConstraint('country_name', 'category', 'indicator_name', 'reference_period',
                        name='uq_indicator_snapshot'),
    )


class EconomicIndicatorHistory(Base, UUIDMixin, TimestampMixin):
    """Time series history for economic indicators."""

    __tablename__ = "economics_indicator_history"

    # Link to indicator
    country_name = Column(String(100), nullable=False, index=True)
    category = Column(String(50), nullable=False, index=True)
    indicator_name = Column(String(255), nullable=False, index=True)

    # Time series data
    observation_date = Column(DateTime, nullable=False, index=True, comment="Date of observation")
    value = Column(String(50), nullable=True, comment="Value as string")
    value_numeric = Column(Float, nullable=True, comment="Value as number")
    unit = Column(String(100), nullable=True)

    # Change metrics
    change_from_previous = Column(Float, nullable=True, comment="Change from previous period")
    change_percent = Column(Float, nullable=True, comment="Percent change from previous")

    # Metadata
    frequency = Column(String(50), nullable=True)
    source = Column(String(255), nullable=True)
    data_source_api = Column(String(50), default="economics-api")

    __table_args__ = (
        Index('ix_history_country_indicator_date', 'country_name', 'indicator_name', 'observation_date'),
        Index('ix_history_category_date', 'category', 'observation_date'),
        UniqueConstraint('country_name', 'indicator_name', 'observation_date',
                        name='uq_indicator_history_point'),
    )


class EconomicDataFetchLog(Base, UUIDMixin, TimestampMixin):
    """Log of API data fetches for monitoring and debugging."""

    __tablename__ = "economics_fetch_log"

    # Fetch details
    endpoint = Column(String(255), nullable=False, comment="API endpoint called")
    country = Column(String(100), nullable=True, index=True)
    category = Column(String(50), nullable=True, index=True)

    # Status
    status = Column(String(20), nullable=False, comment="success, failed, partial")
    records_fetched = Column(Integer, default=0, comment="Number of records fetched")
    records_stored = Column(Integer, default=0, comment="Number of records stored in DB")

    # Performance
    response_time_ms = Column(Integer, nullable=True, comment="API response time in ms")
    cache_hit = Column(String(20), nullable=True, comment="Whether cache was hit")

    # Error tracking
    error_message = Column(Text, nullable=True, comment="Error message if failed")
    error_details = Column(JSON, nullable=True, comment="Detailed error information")

    # Metadata
    fetch_timestamp = Column(DateTime, server_default=func.now(), index=True)
    triggered_by = Column(String(100), nullable=True, comment="What triggered the fetch (cron, api, manual)")

    __table_args__ = (
        Index('ix_fetch_log_timestamp', 'fetch_timestamp'),
        Index('ix_fetch_log_status', 'status', 'fetch_timestamp'),
    )


class EconomicCacheMetadata(Base, UUIDMixin, TimestampMixin):
    """Metadata about cached economic data."""

    __tablename__ = "economics_cache_metadata"

    # Cache key details
    cache_key = Column(String(255), nullable=False, unique=True, index=True)
    country = Column(String(100), nullable=True, index=True)
    category = Column(String(50), nullable=True, index=True)

    # Cache status
    last_fetched = Column(DateTime, nullable=True, comment="When data was last fetched from API")
    last_accessed = Column(DateTime, nullable=True, comment="When cache was last accessed")
    access_count = Column(Integer, default=0, comment="Number of times accessed")

    # Data info
    record_count = Column(Integer, default=0, comment="Number of records in cache")
    data_quality = Column(String(20), nullable=True, comment="Quality indicator (complete, partial, stale)")

    # TTL
    expires_at = Column(DateTime, nullable=True, comment="When cache expires")
    ttl_seconds = Column(Integer, default=3600, comment="TTL in seconds")

    __table_args__ = (
        Index('ix_cache_expires', 'expires_at'),
        Index('ix_cache_country_category', 'country', 'category'),
    )
