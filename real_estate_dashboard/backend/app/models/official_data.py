"""
Database models for official government data storage
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class OfficialDataset(Base):
    """Stores metadata about official government datasets"""
    __tablename__ = "official_datasets"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(100), nullable=False, index=True)  # datagov_us, datagov_il, etc.
    dataset_id = Column(String(255), nullable=False, index=True)  # External dataset ID
    name = Column(String(500), nullable=False)
    title = Column(String(500))
    description = Column(Text)

    # Organization/Publisher info
    organization = Column(String(255))
    publisher = Column(String(255))

    # Tags and categories
    tags = Column(JSON)  # List of tags
    categories = Column(JSON)  # List of categories

    # Metadata
    license_title = Column(String(255))
    license_url = Column(String(500))
    metadata_created = Column(DateTime)
    metadata_modified = Column(DateTime)

    # Resources
    resource_count = Column(Integer, default=0)
    resources = Column(JSON)  # List of resource objects

    # URLs
    dataset_url = Column(String(500))
    api_url = Column(String(500))

    # Additional data
    extras = Column(JSON)  # Additional metadata

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    records = relationship("OfficialDataRecord", back_populates="dataset", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<OfficialDataset(source={self.source}, name={self.name})>"


class OfficialDataRecord(Base):
    """Stores actual data records from official sources"""
    __tablename__ = "official_data_records"

    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer, ForeignKey("official_datasets.id", ondelete="CASCADE"), nullable=False, index=True)

    # Record identification
    record_id = Column(String(255), index=True)  # External record ID if available

    # Data type indicators
    data_type = Column(String(100), index=True)  # housing, economic, demographic, etc.
    category = Column(String(100), index=True)

    # Geographic info
    country = Column(String(2), index=True)  # ISO country code
    state = Column(String(100), index=True)
    county = Column(String(100), index=True)
    city = Column(String(100), index=True)
    zip_code = Column(String(20), index=True)
    metro_area = Column(String(255))

    # Temporal info
    data_year = Column(Integer, index=True)
    data_quarter = Column(Integer)
    data_month = Column(Integer)
    data_date = Column(DateTime)
    period_start = Column(DateTime)
    period_end = Column(DateTime)

    # Numeric data
    value = Column(Float)
    value_type = Column(String(100))  # index, rate, percentage, count, etc.

    # Full data payload
    data = Column(JSON)  # Complete data object

    # Metadata
    source_url = Column(String(500))
    notes = Column(Text)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    dataset = relationship("OfficialDataset", back_populates="records")

    def __repr__(self):
        return f"<OfficialDataRecord(type={self.data_type}, location={self.state or self.country})>"


class HousingPriceIndex(Base):
    """Stores housing price index data (FHFA, etc.)"""
    __tablename__ = "housing_price_indexes"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(50), nullable=False, index=True)  # fhfa, fred, etc.

    # Geographic scope
    geography_type = Column(String(50), nullable=False, index=True)  # national, state, metro, zip
    geography_code = Column(String(100), index=True)  # State code, metro area code, ZIP, etc.
    geography_name = Column(String(255))

    # Temporal info
    year = Column(Integer, nullable=False, index=True)
    quarter = Column(Integer)
    month = Column(Integer)
    date = Column(DateTime, index=True)

    # Index values
    index_value = Column(Float, nullable=False)
    index_type = Column(String(100))  # purchase-only, all-transactions, distress-free

    # Change metrics
    quarterly_change = Column(Float)  # Percentage
    annual_change = Column(Float)  # Percentage
    since_peak_change = Column(Float)  # Percentage from peak

    # Additional data
    base_period = Column(String(50))  # Base period for index (e.g., "2000 Q1 = 100")
    seasonal_adjustment = Column(Boolean, default=False)

    # Raw data
    raw_data = Column(JSON)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<HousingPriceIndex(type={self.geography_type}, code={self.geography_code}, date={self.date})>"


class EconomicIndicator(Base):
    """Stores economic indicators from central banks and government sources"""
    __tablename__ = "economic_indicators"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(50), nullable=False, index=True)  # boi, fred, bls, etc.
    country = Column(String(2), nullable=False, index=True)  # ISO country code

    # Indicator info
    indicator_code = Column(String(100), nullable=False, index=True)
    indicator_name = Column(String(255), nullable=False)
    indicator_type = Column(String(100), index=True)  # interest_rate, cpi, gdp, unemployment, etc.

    # Temporal info
    year = Column(Integer, nullable=False, index=True)
    quarter = Column(Integer)
    month = Column(Integer)
    date = Column(DateTime, index=True)

    # Value
    value = Column(Float, nullable=False)
    value_unit = Column(String(50))  # percentage, index, billions, etc.

    # Change metrics
    month_over_month_change = Column(Float)
    year_over_year_change = Column(Float)

    # Metadata
    seasonal_adjustment = Column(Boolean, default=False)
    revision_status = Column(String(50))  # preliminary, revised, final

    # Raw data
    raw_data = Column(JSON)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<EconomicIndicator(country={self.country}, type={self.indicator_type}, date={self.date})>"


class FairMarketRent(Base):
    """Stores HUD Fair Market Rent data"""
    __tablename__ = "fair_market_rents"

    id = Column(Integer, primary_key=True, index=True)

    # Geographic info
    zip_code = Column(String(10), index=True)
    county = Column(String(100), index=True)
    county_code = Column(String(10))
    metro_code = Column(String(10), index=True)
    metro_name = Column(String(255))
    state = Column(String(2), index=True)

    # Year
    year = Column(Integer, nullable=False, index=True)

    # FMR values by bedroom count
    efficiency = Column(Float)  # Studio/efficiency
    one_bedroom = Column(Float)
    two_bedroom = Column(Float)
    three_bedroom = Column(Float)
    four_bedroom = Column(Float)

    # Additional data
    percentile = Column(Integer, default=40)  # Usually 40th or 50th percentile
    small_area_fmr = Column(Boolean, default=False)  # ZIP code level vs county level

    # Raw data
    raw_data = Column(JSON)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<FairMarketRent(zip={self.zip_code}, year={self.year})>"


class ExchangeRate(Base):
    """Stores exchange rate data from central banks"""
    __tablename__ = "exchange_rates"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(50), nullable=False, index=True)  # boi, ecb, etc.

    # Currency pair
    base_currency = Column(String(3), nullable=False, index=True)  # ILS, USD, EUR
    quote_currency = Column(String(3), nullable=False, index=True)  # USD, EUR, ILS

    # Date
    date = Column(DateTime, nullable=False, index=True)
    year = Column(Integer, nullable=False, index=True)
    month = Column(Integer, nullable=False, index=True)
    day = Column(Integer, nullable=False)

    # Rate value
    rate = Column(Float, nullable=False)
    rate_type = Column(String(50), default='representative')  # representative, spot, average

    # Series identification
    series_code = Column(String(100), index=True)  # SDMX series code

    # Change metrics
    daily_change = Column(Float)
    daily_change_pct = Column(Float)

    # Raw data from API
    raw_data = Column(JSON)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<ExchangeRate({self.base_currency}/{self.quote_currency}={self.rate}, date={self.date})>"


class DataUpdateLog(Base):
    """Tracks data update operations for scheduled tasks"""
    __tablename__ = "data_update_logs"

    id = Column(Integer, primary_key=True, index=True)

    # Update identification
    integration_name = Column(String(100), nullable=False, index=True)  # fhfa, bank_of_israel, etc.
    data_type = Column(String(100), nullable=False, index=True)  # hpi, exchange_rate, cpi, etc.
    update_type = Column(String(50), nullable=False)  # full, incremental, backfill

    # Status
    status = Column(String(50), nullable=False, index=True)  # started, completed, failed

    # Metrics
    records_processed = Column(Integer, default=0)
    records_inserted = Column(Integer, default=0)
    records_updated = Column(Integer, default=0)
    records_failed = Column(Integer, default=0)

    # Timing
    started_at = Column(DateTime(timezone=True), nullable=False)
    completed_at = Column(DateTime(timezone=True))
    duration_seconds = Column(Float)

    # Error details
    error_message = Column(Text)
    error_details = Column(JSON)

    # Additional metadata
    update_metadata = Column(JSON)  # Date ranges, parameters, etc.

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<DataUpdateLog({self.integration_name}, {self.data_type}, {self.status})>"
