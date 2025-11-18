"""
Market Data Model

Stores market data from various sources (CoStar, Zillow, Census, Walk Score)
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.database import Base


class MarketData(Base):
    """
    Market Data Model

    Stores aggregated market data from multiple sources for property analysis.
    """
    __tablename__ = "market_data"

    id = Column(Integer, primary_key=True, index=True)

    # Location Information
    address = Column(String(500), nullable=False)
    city = Column(String(200), nullable=False)
    state = Column(String(100), nullable=False)
    zip_code = Column(String(20), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    # Property Type
    property_type = Column(String(100), nullable=False)  # SFR, Multifamily, Commercial, etc.

    # CoStar Data
    costar_cap_rate = Column(Float, nullable=True)
    costar_avg_rent_psf = Column(Float, nullable=True)
    costar_market_trend = Column(String(50), nullable=True)  # Growing, Stable, Declining
    costar_vacancy_rate = Column(Float, nullable=True)
    costar_comparable_sales = Column(JSON, nullable=True)  # List of comparable sales
    costar_market_rating = Column(String(20), nullable=True)  # A, B, C, D

    # Zillow/Redfin Data
    zillow_estimate = Column(Float, nullable=True)
    zillow_rent_estimate = Column(Float, nullable=True)
    zillow_price_sqft = Column(Float, nullable=True)
    zillow_price_change_30d = Column(Float, nullable=True)  # Percentage
    zillow_comparable_properties = Column(JSON, nullable=True)
    redfin_hot_homes_rank = Column(Integer, nullable=True)
    redfin_days_on_market = Column(Integer, nullable=True)

    # Census Data
    census_population = Column(Integer, nullable=True)
    census_median_income = Column(Float, nullable=True)
    census_population_growth = Column(Float, nullable=True)  # Percentage over 5 years
    census_employment_rate = Column(Float, nullable=True)
    census_age_median = Column(Float, nullable=True)
    census_education_bachelor_plus = Column(Float, nullable=True)  # Percentage
    census_demographics = Column(JSON, nullable=True)

    # Walk Score Data
    walk_score = Column(Integer, nullable=True)  # 0-100
    transit_score = Column(Integer, nullable=True)  # 0-100
    bike_score = Column(Integer, nullable=True)  # 0-100
    walk_score_description = Column(String(100), nullable=True)
    nearby_amenities = Column(JSON, nullable=True)  # List of nearby amenities

    # Metadata
    data_sources = Column(JSON, nullable=True)  # Track which sources provided data
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to company/property (optional) - DISABLED temporarily
    # TODO: Fix foreign key to reference portfolio_companies.id with UUID type
    # company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=True)
    # company = relationship("Company", back_populates="market_data")

    # Indexes for faster queries
    __table_args__ = (
        Index('idx_market_data_location', 'city', 'state', 'zip_code'),
        Index('idx_market_data_property_type', 'property_type'),
        Index('idx_market_data_created_at', 'created_at'),
    )

    def __repr__(self):
        return f"<MarketData(id={self.id}, address='{self.address}', city='{self.city}')>"

    def to_dict(self):
        """Convert market data to dictionary."""
        return {
            "id": self.id,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "zip_code": self.zip_code,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "property_type": self.property_type,
            "costar_data": {
                "cap_rate": self.costar_cap_rate,
                "avg_rent_psf": self.costar_avg_rent_psf,
                "market_trend": self.costar_market_trend,
                "vacancy_rate": self.costar_vacancy_rate,
                "comparable_sales": self.costar_comparable_sales,
                "market_rating": self.costar_market_rating,
            },
            "zillow_redfin_data": {
                "zillow_estimate": self.zillow_estimate,
                "rent_estimate": self.zillow_rent_estimate,
                "price_sqft": self.zillow_price_sqft,
                "price_change_30d": self.zillow_price_change_30d,
                "comparable_properties": self.zillow_comparable_properties,
                "redfin_hot_homes_rank": self.redfin_hot_homes_rank,
                "days_on_market": self.redfin_days_on_market,
            },
            "census_data": {
                "population": self.census_population,
                "median_income": self.census_median_income,
                "population_growth": self.census_population_growth,
                "employment_rate": self.census_employment_rate,
                "age_median": self.census_age_median,
                "education_bachelor_plus": self.census_education_bachelor_plus,
                "demographics": self.census_demographics,
            },
            "walk_score_data": {
                "walk_score": self.walk_score,
                "transit_score": self.transit_score,
                "bike_score": self.bike_score,
                "description": self.walk_score_description,
                "nearby_amenities": self.nearby_amenities,
            },
            "data_sources": self.data_sources,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
