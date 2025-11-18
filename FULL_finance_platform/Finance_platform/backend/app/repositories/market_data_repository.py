"""
Market Data Repository

Handles database operations for market data.
"""

from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.market_data import MarketData


class MarketDataRepository:
    """Repository for market data database operations."""

    @staticmethod
    def create(db: Session, market_data: dict) -> MarketData:
        """
        Create a new market data entry.

        Args:
            db: Database session
            market_data: Dictionary containing market data fields

        Returns:
            Created MarketData object
        """
        db_market_data = MarketData(**market_data)
        db.add(db_market_data)
        db.commit()
        db.refresh(db_market_data)
        return db_market_data

    @staticmethod
    def get_by_id(db: Session, market_data_id: int) -> Optional[MarketData]:
        """Get market data by ID."""
        return db.query(MarketData).filter(MarketData.id == market_data_id).first()

    @staticmethod
    def get_by_address(
        db: Session,
        address: str,
        city: str,
        state: str,
        zip_code: str
    ) -> Optional[MarketData]:
        """Get market data by property address."""
        return db.query(MarketData).filter(
            MarketData.address == address,
            MarketData.city == city,
            MarketData.state == state,
            MarketData.zip_code == zip_code
        ).order_by(desc(MarketData.last_updated)).first()

    @staticmethod
    def get_by_company(db: Session, company_id: int) -> List[MarketData]:
        """Get all market data for a company."""
        return db.query(MarketData).filter(
            MarketData.company_id == company_id
        ).order_by(desc(MarketData.last_updated)).all()

    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[MarketData]:
        """Get all market data entries with pagination."""
        return db.query(MarketData).order_by(
            desc(MarketData.last_updated)
        ).offset(skip).limit(limit).all()

    @staticmethod
    def update(
        db: Session,
        market_data_id: int,
        updates: dict
    ) -> Optional[MarketData]:
        """Update market data entry."""
        db_market_data = MarketDataRepository.get_by_id(db, market_data_id)
        if db_market_data:
            for key, value in updates.items():
                if hasattr(db_market_data, key):
                    setattr(db_market_data, key, value)
            db_market_data.last_updated = datetime.utcnow()
            db.commit()
            db.refresh(db_market_data)
        return db_market_data

    @staticmethod
    def delete(db: Session, market_data_id: int) -> bool:
        """Delete market data entry."""
        db_market_data = MarketDataRepository.get_by_id(db, market_data_id)
        if db_market_data:
            db.delete(db_market_data)
            db.commit()
            return True
        return False

    @staticmethod
    def get_or_create(
        db: Session,
        address: str,
        city: str,
        state: str,
        zip_code: str,
        property_type: str,
        market_data: dict,
        company_id: Optional[int] = None
    ) -> MarketData:
        """
        Get existing market data or create new entry.

        If data exists and is less than 24 hours old, return existing.
        Otherwise, create new entry.
        """
        existing = MarketDataRepository.get_by_address(db, address, city, state, zip_code)

        # Check if data is fresh (less than 24 hours old)
        if existing:
            time_diff = datetime.utcnow() - existing.last_updated
            if time_diff.total_seconds() < 86400:  # 24 hours
                return existing

            # Update existing entry
            return MarketDataRepository.update(db, existing.id, market_data)

        # Create new entry
        market_data_obj = {
            "address": address,
            "city": city,
            "state": state,
            "zip_code": zip_code,
            "property_type": property_type,
            "company_id": company_id,
            **market_data
        }
        return MarketDataRepository.create(db, market_data_obj)

    @staticmethod
    def search_by_location(
        db: Session,
        city: Optional[str] = None,
        state: Optional[str] = None,
        zip_code: Optional[str] = None,
        property_type: Optional[str] = None
    ) -> List[MarketData]:
        """Search market data by location criteria."""
        query = db.query(MarketData)

        if city:
            query = query.filter(MarketData.city.ilike(f"%{city}%"))
        if state:
            query = query.filter(MarketData.state == state)
        if zip_code:
            query = query.filter(MarketData.zip_code == zip_code)
        if property_type:
            query = query.filter(MarketData.property_type == property_type)

        return query.order_by(desc(MarketData.last_updated)).all()
