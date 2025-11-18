"""
Economics Database Service

Handles database operations for economic data storage and retrieval.
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, or_
from sqlalchemy.exc import IntegrityError

from app.models.economics import (
    CountryEconomicOverview,
    EconomicIndicator,
    EconomicIndicatorHistory,
    EconomicDataFetchLog,
    EconomicCacheMetadata,
)
from app.services.economics_data_parser import EconomicsDataParser

logger = logging.getLogger(__name__)


class EconomicsDBService:
    """Service for economics data database operations"""

    def __init__(self, db: Session):
        self.db = db
        self.parser = EconomicsDataParser()

    # ============================================================================
    # Country Overview Operations
    # ============================================================================

    def save_country_overview(self, data: List[Dict]) -> int:
        """
        Save countries overview data to database

        Returns number of records saved
        """
        try:
            parsed_data = self.parser.parse_countries_overview(data)
            saved_count = 0

            for country_data in parsed_data:
                try:
                    # Add country code
                    country_data['country_code'] = self.parser.extract_country_code(
                        country_data['country_name']
                    )

                    # Create or update record
                    overview = CountryEconomicOverview(**country_data)
                    self.db.add(overview)
                    self.db.commit()
                    saved_count += 1
                except IntegrityError:
                    # Record already exists for this date, update it
                    self.db.rollback()
                    existing = self.db.query(CountryEconomicOverview).filter(
                        and_(
                            CountryEconomicOverview.country_name == country_data['country_name'],
                            CountryEconomicOverview.data_date == country_data['data_date']
                        )
                    ).first()

                    if existing:
                        for key, value in country_data.items():
                            setattr(existing, key, value)
                        existing.updated_at = datetime.now()
                        self.db.commit()
                        saved_count += 1
                except Exception as e:
                    logger.error(f"Error saving country overview: {str(e)}")
                    self.db.rollback()
                    continue

            return saved_count
        except Exception as e:
            logger.error(f"Error in save_country_overview: {str(e)}")
            self.db.rollback()
            return 0

    def get_country_overview(
        self,
        country_name: Optional[str] = None,
        limit: int = 100
    ) -> List[CountryEconomicOverview]:
        """Get country overview data from database"""
        query = self.db.query(CountryEconomicOverview)

        if country_name:
            query = query.filter(CountryEconomicOverview.country_name == country_name)

        return query.order_by(desc(CountryEconomicOverview.data_date)).limit(limit).all()

    def get_latest_country_overview(self, country_name: str) -> Optional[CountryEconomicOverview]:
        """Get most recent overview for a specific country"""
        return self.db.query(CountryEconomicOverview).filter(
            CountryEconomicOverview.country_name == country_name
        ).order_by(desc(CountryEconomicOverview.data_date)).first()

    # ============================================================================
    # Economic Indicators Operations
    # ============================================================================

    def save_economic_indicators(
        self,
        data: List[Dict],
        country: str,
        category: str
    ) -> int:
        """
        Save economic indicators to database

        Returns number of records saved
        """
        try:
            parsed_data = self.parser.parse_economic_indicators(data, country, category)
            saved_count = 0

            for indicator_data in parsed_data:
                try:
                    # Validate data
                    if not self.parser.validate_indicator_data(indicator_data):
                        logger.warning(f"Invalid indicator data: {indicator_data}")
                        continue

                    # Create or update indicator
                    indicator = EconomicIndicator(**indicator_data)
                    self.db.add(indicator)
                    self.db.commit()
                    saved_count += 1

                    # Also save to history
                    history_data = self.parser.parse_indicator_for_history(
                        indicator_data['raw_data'],
                        country,
                        category
                    )
                    if history_data:
                        self._save_indicator_history(history_data)

                except IntegrityError:
                    # Record exists, update it
                    self.db.rollback()
                    existing = self.db.query(EconomicIndicator).filter(
                        and_(
                            EconomicIndicator.country_name == indicator_data['country_name'],
                            EconomicIndicator.category == indicator_data['category'],
                            EconomicIndicator.indicator_name == indicator_data['indicator_name'],
                            EconomicIndicator.reference_period == indicator_data['reference_period']
                        )
                    ).first()

                    if existing:
                        for key, value in indicator_data.items():
                            if key != 'id':
                                setattr(existing, key, value)
                        existing.updated_at = datetime.now()
                        self.db.commit()
                        saved_count += 1
                except Exception as e:
                    logger.error(f"Error saving indicator {indicator_data.get('indicator_name')}: {str(e)}")
                    self.db.rollback()
                    continue

            return saved_count
        except Exception as e:
            logger.error(f"Error in save_economic_indicators: {str(e)}")
            self.db.rollback()
            return 0

    def _save_indicator_history(self, history_data: Dict) -> bool:
        """Save indicator history point"""
        try:
            history = EconomicIndicatorHistory(**history_data)
            self.db.add(history)
            self.db.commit()
            return True
        except IntegrityError:
            # History point already exists
            self.db.rollback()
            return False
        except Exception as e:
            logger.error(f"Error saving indicator history: {str(e)}")
            self.db.rollback()
            return False

    def get_economic_indicators(
        self,
        country: Optional[str] = None,
        category: Optional[str] = None,
        indicator_name: Optional[str] = None,
        limit: int = 100
    ) -> List[EconomicIndicator]:
        """Get economic indicators from database"""
        query = self.db.query(EconomicIndicator)

        if country:
            query = query.filter(EconomicIndicator.country_name == country)
        if category:
            query = query.filter(EconomicIndicator.category == category)
        if indicator_name:
            query = query.filter(EconomicIndicator.indicator_name.ilike(f"%{indicator_name}%"))

        return query.order_by(desc(EconomicIndicator.data_date)).limit(limit).all()

    def get_indicator_history(
        self,
        country: str,
        indicator_name: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 365
    ) -> List[EconomicIndicatorHistory]:
        """Get historical time series for an indicator"""
        query = self.db.query(EconomicIndicatorHistory).filter(
            and_(
                EconomicIndicatorHistory.country_name == country,
                EconomicIndicatorHistory.indicator_name == indicator_name
            )
        )

        if start_date:
            query = query.filter(EconomicIndicatorHistory.observation_date >= start_date)
        if end_date:
            query = query.filter(EconomicIndicatorHistory.observation_date <= end_date)

        return query.order_by(desc(EconomicIndicatorHistory.observation_date)).limit(limit).all()

    # ============================================================================
    # Fetch Log Operations
    # ============================================================================

    def log_fetch(
        self,
        endpoint: str,
        country: Optional[str] = None,
        category: Optional[str] = None,
        status: str = "success",
        records_fetched: int = 0,
        records_stored: int = 0,
        response_time_ms: Optional[int] = None,
        cache_hit: Optional[str] = None,
        error_message: Optional[str] = None,
        error_details: Optional[Dict] = None,
        triggered_by: str = "api"
    ) -> EconomicDataFetchLog:
        """Log an API fetch operation"""
        try:
            log_entry = EconomicDataFetchLog(
                endpoint=endpoint,
                country=country,
                category=category,
                status=status,
                records_fetched=records_fetched,
                records_stored=records_stored,
                response_time_ms=response_time_ms,
                cache_hit=cache_hit,
                error_message=error_message,
                error_details=error_details,
                triggered_by=triggered_by
            )
            self.db.add(log_entry)
            self.db.commit()
            return log_entry
        except Exception as e:
            logger.error(f"Error logging fetch: {str(e)}")
            self.db.rollback()
            return None

    def get_fetch_logs(
        self,
        country: Optional[str] = None,
        status: Optional[str] = None,
        hours: int = 24,
        limit: int = 100
    ) -> List[EconomicDataFetchLog]:
        """Get recent fetch logs"""
        query = self.db.query(EconomicDataFetchLog)

        cutoff_time = datetime.now() - timedelta(hours=hours)
        query = query.filter(EconomicDataFetchLog.fetch_timestamp >= cutoff_time)

        if country:
            query = query.filter(EconomicDataFetchLog.country == country)
        if status:
            query = query.filter(EconomicDataFetchLog.status == status)

        return query.order_by(desc(EconomicDataFetchLog.fetch_timestamp)).limit(limit).all()

    # ============================================================================
    # Cache Metadata Operations
    # ============================================================================

    def update_cache_metadata(
        self,
        cache_key: str,
        country: Optional[str] = None,
        category: Optional[str] = None,
        record_count: int = 0,
        ttl_seconds: int = 3600
    ) -> EconomicCacheMetadata:
        """Update or create cache metadata"""
        try:
            metadata = self.db.query(EconomicCacheMetadata).filter(
                EconomicCacheMetadata.cache_key == cache_key
            ).first()

            now = datetime.now()
            expires_at = now + timedelta(seconds=ttl_seconds)

            if metadata:
                # Update existing
                metadata.last_fetched = now
                metadata.last_accessed = now
                metadata.access_count += 1
                metadata.record_count = record_count
                metadata.expires_at = expires_at
                metadata.ttl_seconds = ttl_seconds
                metadata.updated_at = now
            else:
                # Create new
                metadata = EconomicCacheMetadata(
                    cache_key=cache_key,
                    country=country,
                    category=category,
                    last_fetched=now,
                    last_accessed=now,
                    access_count=1,
                    record_count=record_count,
                    expires_at=expires_at,
                    ttl_seconds=ttl_seconds
                )
                self.db.add(metadata)

            self.db.commit()
            return metadata
        except Exception as e:
            logger.error(f"Error updating cache metadata: {str(e)}")
            self.db.rollback()
            return None

    def is_cache_valid(self, cache_key: str) -> bool:
        """Check if cache is still valid"""
        metadata = self.db.query(EconomicCacheMetadata).filter(
            EconomicCacheMetadata.cache_key == cache_key
        ).first()

        if not metadata:
            return False

        return metadata.expires_at > datetime.now()

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_entries = self.db.query(EconomicCacheMetadata).count()
        expired_entries = self.db.query(EconomicCacheMetadata).filter(
            EconomicCacheMetadata.expires_at < datetime.now()
        ).count()

        return {
            'total_entries': total_entries,
            'valid_entries': total_entries - expired_entries,
            'expired_entries': expired_entries,
            'hit_rate': self._calculate_hit_rate(),
        }

    def _calculate_hit_rate(self) -> float:
        """Calculate cache hit rate from fetch logs"""
        recent_logs = self.get_fetch_logs(hours=24, limit=1000)
        if not recent_logs:
            return 0.0

        cache_hits = sum(1 for log in recent_logs if log.cache_hit == 'hit')
        return (cache_hits / len(recent_logs)) * 100

    # ============================================================================
    # Cleanup Operations
    # ============================================================================

    def cleanup_expired_cache(self) -> int:
        """Remove expired cache metadata"""
        try:
            deleted = self.db.query(EconomicCacheMetadata).filter(
                EconomicCacheMetadata.expires_at < datetime.now()
            ).delete()
            self.db.commit()
            return deleted
        except Exception as e:
            logger.error(f"Error cleaning up cache: {str(e)}")
            self.db.rollback()
            return 0

    def cleanup_old_fetch_logs(self, days: int = 30) -> int:
        """Remove fetch logs older than specified days"""
        try:
            cutoff = datetime.now() - timedelta(days=days)
            deleted = self.db.query(EconomicDataFetchLog).filter(
                EconomicDataFetchLog.fetch_timestamp < cutoff
            ).delete()
            self.db.commit()
            return deleted
        except Exception as e:
            logger.error(f"Error cleaning up fetch logs: {str(e)}")
            self.db.rollback()
            return 0

    # ============================================================================
    # Query/Analytics Methods
    # ============================================================================

    def get_countries_with_data(self) -> List[str]:
        """Get list of countries that have data in the database"""
        results = self.db.query(CountryEconomicOverview.country_name).distinct().all()
        return [r[0] for r in results]

    def get_available_categories(self, country: Optional[str] = None) -> List[str]:
        """Get list of available indicator categories"""
        query = self.db.query(EconomicIndicator.category).distinct()

        if country:
            query = query.filter(EconomicIndicator.country_name == country)

        results = query.all()
        return [r[0] for r in results]

    def get_data_freshness(self, country: str) -> Dict[str, Any]:
        """Get data freshness information for a country"""
        latest_overview = self.get_latest_country_overview(country)

        latest_indicators = {}
        for category in self.get_available_categories(country):
            latest = self.db.query(EconomicIndicator).filter(
                and_(
                    EconomicIndicator.country_name == country,
                    EconomicIndicator.category == category
                )
            ).order_by(desc(EconomicIndicator.data_date)).first()

            if latest:
                latest_indicators[category] = latest.data_date

        return {
            'country': country,
            'overview_last_updated': latest_overview.data_date if latest_overview else None,
            'categories_last_updated': latest_indicators,
            'overall_freshness': min(latest_indicators.values()) if latest_indicators else None
        }
