"""
Cache utilities for official data integrations

Provides database caching layer for FHFA, Bank of Israel, and other integrations
to avoid repeated API calls and improve performance.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
import logging

from app.models.official_data import (
    HousingPriceIndex,
    ExchangeRate,
    EconomicIndicator,
    DataUpdateLog
)

logger = logging.getLogger(__name__)


class FHFADataCache:
    """Cache manager for FHFA Housing Price Index data"""

    @staticmethod
    async def save_hpi_data(
        db: Session,
        data: List[Dict[str, Any]],
        source: str = "fhfa"
    ) -> Dict[str, int]:
        """
        Save FHFA HPI data to database

        Args:
            db: Database session
            data: List of HPI records from CSV
            source: Data source identifier

        Returns:
            Dict with inserted and updated counts
        """
        inserted = 0
        updated = 0
        failed = 0

        for record in data:
            try:
                # Parse date from year and period
                year = int(record.get('year', 0))
                period = record.get('period', 'M01')

                # Determine quarter and month
                quarter = None
                month = None

                if period.startswith('M'):
                    month = int(period[1:])
                elif period.startswith('Q'):
                    quarter = int(period[1:])
                    month = quarter * 3  # Last month of quarter

                date = datetime(year, month or 1, 1)

                # Check if record exists
                existing = db.query(HousingPriceIndex).filter(
                    and_(
                        HousingPriceIndex.source == source,
                        HousingPriceIndex.geography_type == record.get('level'),
                        HousingPriceIndex.geography_code == record.get('place_id'),
                        HousingPriceIndex.year == year,
                        HousingPriceIndex.month == month
                    )
                ).first()

                # Determine seasonal adjustment
                seasonal_adjustment = record.get('index_sa') is not None

                if existing:
                    # Update existing record
                    existing.index_value = float(record.get('index_sa') or record.get('index_nsa', 0))
                    existing.index_type = record.get('hpi_flavor')
                    existing.seasonal_adjustment = seasonal_adjustment
                    existing.raw_data = record
                    existing.updated_at = datetime.now()
                    updated += 1
                else:
                    # Create new record
                    hpi = HousingPriceIndex(
                        source=source,
                        geography_type=record.get('level'),
                        geography_code=record.get('place_id'),
                        geography_name=record.get('place_name'),
                        year=year,
                        quarter=quarter,
                        month=month,
                        date=date,
                        index_value=float(record.get('index_sa') or record.get('index_nsa', 0)),
                        index_type=record.get('hpi_flavor'),
                        seasonal_adjustment=seasonal_adjustment,
                        raw_data=record
                    )
                    db.add(hpi)
                    inserted += 1

            except Exception as e:
                logger.error(f"Failed to process HPI record: {e}", exc_info=True)
                failed += 1
                continue

        try:
            db.commit()
        except Exception as e:
            logger.error(f"Failed to commit HPI data: {e}", exc_info=True)
            db.rollback()

        return {"inserted": inserted, "updated": updated, "failed": failed}

    @staticmethod
    def get_hpi_data(
        db: Session,
        geography_type: Optional[str] = None,
        geography_code: Optional[str] = None,
        place_name: Optional[str] = None,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None,
        limit: int = 1000
    ) -> List[HousingPriceIndex]:
        """
        Retrieve HPI data from database cache

        Args:
            db: Database session
            geography_type: Filter by geography type
            geography_code: Filter by geography code
            place_name: Filter by place name (partial match)
            start_year: Filter by start year
            end_year: Filter by end year
            limit: Maximum records to return

        Returns:
            List of HPI records
        """
        query = db.query(HousingPriceIndex)

        # Apply filters
        if geography_type:
            query = query.filter(HousingPriceIndex.geography_type == geography_type)
        if geography_code:
            query = query.filter(HousingPriceIndex.geography_code == geography_code)
        if place_name:
            query = query.filter(HousingPriceIndex.geography_name.ilike(f"%{place_name}%"))
        if start_year:
            query = query.filter(HousingPriceIndex.year >= start_year)
        if end_year:
            query = query.filter(HousingPriceIndex.year <= end_year)

        # Order by date descending
        query = query.order_by(desc(HousingPriceIndex.date))

        # Limit results
        return query.limit(limit).all()

    @staticmethod
    def get_cache_age(db: Session) -> Optional[datetime]:
        """Get the age of the most recent HPI data in cache"""
        latest = db.query(HousingPriceIndex).order_by(desc(HousingPriceIndex.created_at)).first()
        return latest.created_at if latest else None

    @staticmethod
    def is_cache_stale(db: Session, max_age_days: int = 30) -> bool:
        """Check if cache is stale and needs refresh"""
        cache_age = FHFADataCache.get_cache_age(db)
        if not cache_age:
            return True  # No data, needs refresh

        age = datetime.now() - cache_age.replace(tzinfo=None)
        return age.days >= max_age_days


class BankOfIsraelDataCache:
    """Cache manager for Bank of Israel data"""

    @staticmethod
    async def save_exchange_rates(
        db: Session,
        data: List[Dict[str, Any]],
        base_currency: str,
        quote_currency: str,
        source: str = "boi",
        series_code: Optional[str] = None
    ) -> Dict[str, int]:
        """
        Save exchange rate data to database

        Args:
            db: Database session
            data: List of exchange rate records
            base_currency: Base currency code
            quote_currency: Quote currency code
            source: Data source identifier
            series_code: SDMX series code

        Returns:
            Dict with inserted and updated counts
        """
        inserted = 0
        updated = 0
        failed = 0

        for record in data:
            try:
                # Parse date
                date_str = record.get('TIME_PERIOD') or record.get('DATE')
                if not date_str:
                    continue

                date = datetime.strptime(date_str, "%Y-%m-%d")

                # Get rate value
                rate_value = float(record.get('OBS_VALUE') or record.get('VALUE', 0))
                if rate_value == 0:
                    continue

                # Check if record exists
                existing = db.query(ExchangeRate).filter(
                    and_(
                        ExchangeRate.source == source,
                        ExchangeRate.base_currency == base_currency,
                        ExchangeRate.quote_currency == quote_currency,
                        ExchangeRate.date == date
                    )
                ).first()

                if existing:
                    # Update existing record
                    existing.rate = rate_value
                    existing.series_code = series_code
                    existing.raw_data = record
                    existing.updated_at = datetime.now()
                    updated += 1
                else:
                    # Create new record
                    exchange_rate = ExchangeRate(
                        source=source,
                        base_currency=base_currency,
                        quote_currency=quote_currency,
                        date=date,
                        year=date.year,
                        month=date.month,
                        day=date.day,
                        rate=rate_value,
                        series_code=series_code,
                        raw_data=record
                    )
                    db.add(exchange_rate)
                    inserted += 1

            except Exception as e:
                logger.error(f"Failed to process exchange rate record: {e}", exc_info=True)
                failed += 1
                continue

        try:
            db.commit()
        except Exception as e:
            logger.error(f"Failed to commit exchange rate data: {e}", exc_info=True)
            db.rollback()

        return {"inserted": inserted, "updated": updated, "failed": failed}

    @staticmethod
    def get_exchange_rates(
        db: Session,
        base_currency: str,
        quote_currency: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 1000
    ) -> List[ExchangeRate]:
        """
        Retrieve exchange rate data from database cache

        Args:
            db: Database session
            base_currency: Base currency code
            quote_currency: Quote currency code
            start_date: Filter by start date
            end_date: Filter by end date
            limit: Maximum records to return

        Returns:
            List of exchange rate records
        """
        query = db.query(ExchangeRate).filter(
            and_(
                ExchangeRate.base_currency == base_currency,
                ExchangeRate.quote_currency == quote_currency
            )
        )

        # Apply date filters
        if start_date:
            query = query.filter(ExchangeRate.date >= start_date)
        if end_date:
            query = query.filter(ExchangeRate.date <= end_date)

        # Order by date descending
        query = query.order_by(desc(ExchangeRate.date))

        # Limit results
        return query.limit(limit).all()

    @staticmethod
    def get_latest_rate(
        db: Session,
        base_currency: str,
        quote_currency: str
    ) -> Optional[ExchangeRate]:
        """Get the most recent exchange rate"""
        return db.query(ExchangeRate).filter(
            and_(
                ExchangeRate.base_currency == base_currency,
                ExchangeRate.quote_currency == quote_currency
            )
        ).order_by(desc(ExchangeRate.date)).first()

    @staticmethod
    def get_cache_age(
        db: Session,
        base_currency: str,
        quote_currency: str
    ) -> Optional[datetime]:
        """Get the age of the most recent rate in cache"""
        latest = BankOfIsraelDataCache.get_latest_rate(db, base_currency, quote_currency)
        return latest.date if latest else None

    @staticmethod
    def is_cache_stale(
        db: Session,
        base_currency: str,
        quote_currency: str,
        max_age_days: int = 1
    ) -> bool:
        """Check if cache is stale and needs refresh"""
        cache_age = BankOfIsraelDataCache.get_cache_age(db, base_currency, quote_currency)
        if not cache_age:
            return True  # No data, needs refresh

        age = datetime.now() - cache_age.replace(tzinfo=None)
        return age.days >= max_age_days


class DataUpdateLogger:
    """Logger for tracking data update operations"""

    @staticmethod
    def start_update(
        db: Session,
        integration_name: str,
        data_type: str,
        update_type: str = "full",
        metadata: Optional[Dict[str, Any]] = None
    ) -> DataUpdateLog:
        """Start logging a data update operation"""
        log = DataUpdateLog(
            integration_name=integration_name,
            data_type=data_type,
            update_type=update_type,
            status="started",
            started_at=datetime.now(),
            metadata=metadata or {}
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return log

    @staticmethod
    def complete_update(
        db: Session,
        log: DataUpdateLog,
        records_processed: int = 0,
        records_inserted: int = 0,
        records_updated: int = 0,
        records_failed: int = 0
    ):
        """Mark update as completed successfully"""
        log.status = "completed"
        log.completed_at = datetime.now()
        log.duration_seconds = (log.completed_at - log.started_at).total_seconds()
        log.records_processed = records_processed
        log.records_inserted = records_inserted
        log.records_updated = records_updated
        log.records_failed = records_failed
        db.commit()

    @staticmethod
    def fail_update(
        db: Session,
        log: DataUpdateLog,
        error_message: str,
        error_details: Optional[Dict[str, Any]] = None
    ):
        """Mark update as failed"""
        log.status = "failed"
        log.completed_at = datetime.now()
        log.duration_seconds = (log.completed_at - log.started_at).total_seconds()
        log.error_message = error_message
        log.error_details = error_details or {}
        db.commit()

    @staticmethod
    def get_recent_updates(
        db: Session,
        integration_name: Optional[str] = None,
        data_type: Optional[str] = None,
        limit: int = 100
    ) -> List[DataUpdateLog]:
        """Get recent update logs"""
        query = db.query(DataUpdateLog)

        if integration_name:
            query = query.filter(DataUpdateLog.integration_name == integration_name)
        if data_type:
            query = query.filter(DataUpdateLog.data_type == data_type)

        return query.order_by(desc(DataUpdateLog.started_at)).limit(limit).all()

    @staticmethod
    def get_last_successful_update(
        db: Session,
        integration_name: str,
        data_type: str
    ) -> Optional[DataUpdateLog]:
        """Get the most recent successful update"""
        return db.query(DataUpdateLog).filter(
            and_(
                DataUpdateLog.integration_name == integration_name,
                DataUpdateLog.data_type == data_type,
                DataUpdateLog.status == "completed"
            )
        ).order_by(desc(DataUpdateLog.completed_at)).first()
