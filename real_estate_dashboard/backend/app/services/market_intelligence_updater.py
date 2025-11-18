"""
Daily Market Intelligence Data Updater

Fetches market data from multiple sources, stores in database, and creates
daily snapshots with comprehensive fallback mechanisms.

Run this script daily (recommended: 6 PM EST after market close)
"""

import logging
import asyncio
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Any, Tuple
from decimal import Decimal
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.market_intelligence import (
    YFinanceMarketData,
    EconomicIndicator,
    MarketIntelligenceSnapshot,
    MarketDataImport
)
from app.services.yfinance_service import YFinanceService
from app.services.economics_api_service import EconomicsAPIService
from app.services.cache_service import CacheService
from app.services.market_analytics_service import MarketAnalyticsService

logger = logging.getLogger(__name__)


class MarketIntelligenceUpdater:
    """
    Comprehensive market intelligence data updater with fallback mechanisms
    """

    def __init__(self, db: Session):
        self.db = db
        self.yfinance = YFinanceService()
        self.economics = EconomicsAPIService()
        self.cache = CacheService()
        self.analytics = MarketAnalyticsService(db)

        # Track update status
        self.status = {
            "started_at": datetime.now(),
            "completed_at": None,
            "total_success": 0,
            "total_failures": 0,
            "sources_success": [],
            "sources_failed": [],
            "errors": [],
            "trends_calculated": 0,
            "correlations_calculated": 0,
            "insights_generated": 0,
        }

    async def run_daily_update(self) -> Dict[str, Any]:
        """
        Main entry point for daily market intelligence update

        Returns:
            Dict with update status and statistics
        """
        logger.info("=" * 80)
        logger.info("Starting Daily Market Intelligence Update")
        logger.info("=" * 80)

        try:
            # Phase 1: Fetch YFinance Data (REITs, Indices, Rates)
            logger.info("Phase 1: Fetching YFinance market data...")
            yfinance_success = await self._update_yfinance_data()

            # Phase 2: Fetch Economics API Data
            logger.info("Phase 2: Fetching Economics API data...")
            economics_success = await self._update_economics_data()

            # Phase 3: Create Daily Snapshot
            logger.info("Phase 3: Creating daily snapshot...")
            snapshot_success = await self._create_daily_snapshot()

            # Phase 4: Calculate Trends (NEW - Analytics)
            logger.info("Phase 4: Calculating market trends...")
            trends_calculated = await self._calculate_trends()
            self.status["trends_calculated"] = trends_calculated

            # Phase 5: Calculate Correlations (NEW - Analytics)
            logger.info("Phase 5: Calculating market correlations...")
            correlations_calculated = await self._calculate_correlations()
            self.status["correlations_calculated"] = correlations_calculated

            # Phase 6: Generate Insights (NEW - Analytics)
            logger.info("Phase 6: Generating market insights...")
            insights_generated = await self._generate_insights()
            self.status["insights_generated"] = insights_generated

            # Phase 7: Cleanup old data
            logger.info("Phase 7: Cleaning up old data...")
            await self._cleanup_old_data()

            # Finalize status
            self.status["completed_at"] = datetime.now()
            duration = (self.status["completed_at"] - self.status["started_at"]).total_seconds()

            logger.info("=" * 80)
            logger.info(f"Update Complete in {duration:.2f} seconds")
            logger.info(f"✅ Successful: {self.status['total_success']}")
            logger.info(f"❌ Failed: {self.status['total_failures']}")
            logger.info(f"Sources Success: {', '.join(self.status['sources_success'])}")
            if self.status['sources_failed']:
                logger.warning(f"Sources Failed: {', '.join(self.status['sources_failed'])}")
            logger.info(f"\n📊 Analytics:")
            logger.info(f"  • Trends calculated: {self.status['trends_calculated']}")
            logger.info(f"  • Correlations calculated: {self.status['correlations_calculated']}")
            logger.info(f"  • Insights generated: {self.status['insights_generated']}")
            logger.info("=" * 80)

            return self.status

        except Exception as e:
            logger.error(f"Critical error in daily update: {str(e)}", exc_info=True)
            self.status["completed_at"] = datetime.now()
            self.status["errors"].append(f"Critical: {str(e)}")
            return self.status

    async def _update_yfinance_data(self) -> bool:
        """
        Update YFinance market data with fallbacks

        Returns:
            True if successful, False otherwise
        """
        success_count = 0

        try:
            # 1. Update Market Indices
            logger.info("  → Fetching market indices...")
            indices_result = await self._fetch_with_fallback(
                self.yfinance.get_market_indices,
                "market_indices"
            )
            if indices_result:
                success_count += await self._save_yfinance_data(
                    indices_result.get("indices", []),
                    "index"
                )

            # 2. Update REITs
            logger.info("  → Fetching REIT data...")
            reits_result = await self._fetch_with_fallback(
                self.yfinance.get_reit_data,
                "reits"
            )
            if reits_result:
                success_count += await self._save_yfinance_data(
                    reits_result.get("reits", []),
                    "reit"
                )

            # 3. Update Treasury Rates
            logger.info("  → Fetching treasury rates...")
            rates_result = await self._fetch_with_fallback(
                self.yfinance.get_treasury_rates,
                "treasury_rates"
            )
            if rates_result:
                success_count += await self._save_yfinance_data(
                    rates_result.get("rates", []),
                    "rate"
                )

            logger.info(f"  ✅ YFinance: Saved {success_count} records")
            self.status["total_success"] += success_count
            self.status["sources_success"].append("YFinance")

            # Log import record
            await self._log_import("yfinance", "success", success_count, 0)

            return True

        except Exception as e:
            logger.error(f"  ❌ YFinance update failed: {str(e)}")
            self.status["total_failures"] += 1
            self.status["sources_failed"].append("YFinance")
            self.status["errors"].append(f"YFinance: {str(e)}")

            await self._log_import("yfinance", "failed", 0, 0, str(e))
            return False

    async def _update_economics_data(self) -> bool:
        """
        Update Economics API data with fallbacks

        Returns:
            True if successful, False otherwise
        """
        success_count = 0

        try:
            # Key countries for real estate intelligence
            countries = ["united-states", "israel"]
            categories = ["housing", "labour", "prices", "gdp"]

            for country in countries:
                for category in categories:
                    logger.info(f"  → Fetching {country} {category} data...")

                    result = await self._fetch_with_fallback(
                        lambda: self.economics.get_economic_indicator(country, category, use_cache=False),
                        f"economics_{country}_{category}"
                    )

                    if result and "data" in result:
                        count = await self._save_economic_data(result, country, category)
                        success_count += count

            logger.info(f"  ✅ Economics API: Saved {success_count} indicators")
            self.status["total_success"] += success_count
            self.status["sources_success"].append("Economics API")

            await self._log_import("economics_api", "success", success_count, 0)

            return True

        except Exception as e:
            logger.error(f"  ❌ Economics API update failed: {str(e)}")
            self.status["total_failures"] += 1
            self.status["sources_failed"].append("Economics API")
            self.status["errors"].append(f"Economics API: {str(e)}")

            await self._log_import("economics_api", "failed", 0, 0, str(e))
            return False

    async def _fetch_with_fallback(
        self,
        fetch_func: callable,
        cache_key: str,
        max_retries: int = 3
    ) -> Optional[Dict[str, Any]]:
        """
        Fetch data with fallback to cache and retries

        Args:
            fetch_func: Function to call for data
            cache_key: Key for caching
            max_retries: Maximum retry attempts

        Returns:
            Data dict or None if all attempts fail
        """
        last_error = None

        # Try primary fetch with retries
        for attempt in range(max_retries):
            try:
                result = await fetch_func(use_cache=False)

                if result and not result.get("error"):
                    # Success - cache and return
                    await self.cache.set(f"daily_update:{cache_key}", result, ttl=86400)
                    return result

                last_error = result.get("error") if result else "No data returned"

                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    logger.warning(f"    Attempt {attempt + 1} failed, retrying in {wait_time}s...")
                    await asyncio.sleep(wait_time)

            except Exception as e:
                last_error = str(e)
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    logger.warning(f"    Attempt {attempt + 1} error: {e}, retrying in {wait_time}s...")
                    await asyncio.sleep(wait_time)

        # All retries failed - try cache fallback
        logger.warning(f"    All retries failed: {last_error}")
        logger.info(f"    Attempting cache fallback for {cache_key}...")

        cached = await self.cache.get(f"daily_update:{cache_key}")
        if cached:
            logger.info(f"    ⚠️  Using cached data from {cached.get('timestamp', 'unknown')}")
            return cached

        # Try yesterday's database data as last resort
        logger.warning(f"    No cache available, attempting database fallback...")
        db_data = await self._get_yesterday_data(cache_key)
        if db_data:
            logger.info(f"    ⚠️  Using yesterday's database data")
            return db_data

        logger.error(f"    ❌ All fallback attempts failed for {cache_key}")
        return None

    async def _save_yfinance_data(
        self,
        data_items: List[Dict],
        security_type: str
    ) -> int:
        """Save YFinance data to database"""
        saved_count = 0

        for item in data_items:
            try:
                # Determine ticker
                ticker = item.get("ticker") or item.get("symbol")
                if not ticker:
                    continue

                # Check if record exists for today
                existing = self.db.query(YFinanceMarketData).filter(
                    YFinanceMarketData.ticker == ticker,
                    YFinanceMarketData.data_timestamp >= datetime.now().replace(hour=0, minute=0, second=0)
                ).first()

                if existing:
                    # Update existing record
                    existing.current_price = self._to_decimal(item.get("current_price") or item.get("value") or item.get("rate"))
                    existing.price_change = self._to_decimal(item.get("change") or item.get("price_change"))
                    existing.price_change_pct = self._to_decimal(item.get("change_pct") or item.get("price_change_pct"))
                    existing.volume = item.get("volume")
                    existing.market_cap = item.get("market_cap")
                    existing.updated_at = datetime.now()
                else:
                    # Create new record
                    record = YFinanceMarketData(
                        ticker=ticker,
                        company_name=item.get("company_name") or item.get("name"),
                        security_type=security_type,
                        current_price=self._to_decimal(item.get("current_price") or item.get("value") or item.get("rate")),
                        currency=item.get("currency", "USD"),
                        price_change=self._to_decimal(item.get("change") or item.get("price_change")),
                        price_change_pct=self._to_decimal(item.get("change_pct") or item.get("price_change_pct")),
                        volume=item.get("volume"),
                        market_cap=item.get("market_cap"),
                        pe_ratio=self._to_decimal(item.get("pe_ratio")),
                        dividend_yield=self._to_decimal(item.get("dividend_yield")),
                        week_52_high=self._to_decimal(item.get("52_week_high")),
                        week_52_low=self._to_decimal(item.get("52_week_low")),
                        sector=item.get("sector"),
                        industry=item.get("industry"),
                        historical_data=item.get("history"),
                        data_period=item.get("period"),
                        data_interval=item.get("interval"),
                        data_timestamp=datetime.now()
                    )
                    self.db.add(record)

                saved_count += 1

            except Exception as e:
                logger.error(f"    Error saving {ticker}: {str(e)}")
                continue

        self.db.commit()
        return saved_count

    async def _save_economic_data(
        self,
        result: Dict,
        country: str,
        category: str
    ) -> int:
        """Save economic indicator data to database"""
        saved_count = 0

        try:
            data = result.get("data", {})
            if not data:
                return 0

            # Handle different data structures from Economics API
            indicators = []

            if isinstance(data, list):
                indicators = data
            elif isinstance(data, dict):
                # Convert dict to list of indicators
                for key, value in data.items():
                    if isinstance(value, dict):
                        value["indicator_name"] = key
                        indicators.append(value)
                    else:
                        indicators.append({
                            "indicator_name": key,
                            "value": value
                        })

            for indicator_data in indicators:
                try:
                    indicator_name = indicator_data.get("indicator_name") or indicator_data.get("name", "Unknown")

                    # Check if record exists for today
                    existing = self.db.query(EconomicIndicator).filter(
                        EconomicIndicator.country == country,
                        EconomicIndicator.category == category,
                        EconomicIndicator.indicator_name == indicator_name,
                        EconomicIndicator.reference_date >= date.today()
                    ).first()

                    value = indicator_data.get("value") or indicator_data.get("latest_value")

                    if existing:
                        # Update existing
                        existing.value = self._to_decimal(value)
                        existing.previous_value = self._to_decimal(indicator_data.get("previous_value"))
                        existing.raw_data = indicator_data
                        existing.updated_at = datetime.now()
                    else:
                        # Create new
                        record = EconomicIndicator(
                            country=country,
                            category=category,
                            indicator_name=indicator_name,
                            value=self._to_decimal(value),
                            previous_value=self._to_decimal(indicator_data.get("previous_value")),
                            units=indicator_data.get("units"),
                            frequency=indicator_data.get("frequency"),
                            reference_date=date.today(),
                            raw_data=indicator_data
                        )
                        self.db.add(record)

                    saved_count += 1

                except Exception as e:
                    logger.error(f"    Error saving indicator {indicator_name}: {str(e)}")
                    continue

            self.db.commit()

        except Exception as e:
            logger.error(f"    Error processing economic data: {str(e)}")

        return saved_count

    async def _create_daily_snapshot(self) -> bool:
        """
        Create comprehensive daily market intelligence snapshot

        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info("  → Creating daily snapshot...")

            # Get today's data
            today = date.today()

            # Check if snapshot already exists
            existing = self.db.query(MarketIntelligenceSnapshot).filter(
                MarketIntelligenceSnapshot.snapshot_date == today,
                MarketIntelligenceSnapshot.snapshot_type == "daily"
            ).first()

            # Gather data
            indices = await self._get_latest_indices()
            reits = await self._get_latest_reits()
            rates = await self._get_latest_rates()
            economic = await self._get_latest_economic()

            # Calculate data completeness
            total_fields = 15
            available_fields = sum([
                1 if indices.get("sp500_value") else 0,
                1 if indices.get("dow_jones_value") else 0,
                1 if indices.get("nasdaq_value") else 0,
                1 if indices.get("vix_value") else 0,
                1 if reits.get("reit_etf_vnq") else 0,
                1 if rates.get("treasury_10y") else 0,
                1 if rates.get("treasury_30y") else 0,
                1 if economic.get("unemployment_rate") else 0,
                1 if economic.get("inflation_rate") else 0,
                1 if economic.get("gdp_growth_rate") else 0,
                1 if economic.get("home_price_index") else 0,
                1 if economic.get("housing_starts") else 0,
                1 if economic.get("building_permits") else 0,
                1 if rates.get("fed_funds_rate") else 0,
                1 if rates.get("mortgage_30y") else 0,
            ])

            completeness = (available_fields / total_fields) * 100

            # Create full_data dict
            full_data = {
                "indices": indices,
                "reits": reits,
                "rates": rates,
                "economic": economic,
                "snapshot_date": today.isoformat(),
                "completeness_pct": completeness,
            }

            if existing:
                # Update existing snapshot
                existing.sp500_value = indices.get("sp500_value")
                existing.sp500_change_pct = indices.get("sp500_change_pct")
                existing.dow_jones_value = indices.get("dow_jones_value")
                existing.nasdaq_value = indices.get("nasdaq_value")
                existing.vix_value = indices.get("vix_value")
                existing.reit_etf_vnq = reits.get("reit_etf_vnq")
                existing.reit_sector_change_pct = reits.get("reit_sector_change_pct")
                existing.treasury_10y = rates.get("treasury_10y")
                existing.treasury_30y = rates.get("treasury_30y")
                existing.fed_funds_rate = rates.get("fed_funds_rate")
                existing.mortgage_30y = rates.get("mortgage_30y")
                existing.unemployment_rate = economic.get("unemployment_rate")
                existing.inflation_rate = economic.get("inflation_rate")
                existing.gdp_growth_rate = economic.get("gdp_growth_rate")
                existing.home_price_index = economic.get("home_price_index")
                existing.housing_starts = economic.get("housing_starts")
                existing.building_permits = economic.get("building_permits")
                existing.full_data = full_data
                existing.data_completeness_pct = self._to_decimal(completeness)
                existing.data_sources_count = len(self.status["sources_success"])
                existing.updated_at = datetime.now()

                logger.info(f"  ✅ Updated existing snapshot ({completeness:.1f}% complete)")
            else:
                # Create new snapshot
                snapshot = MarketIntelligenceSnapshot(
                    snapshot_date=today,
                    snapshot_type="daily",
                    sp500_value=indices.get("sp500_value"),
                    sp500_change_pct=indices.get("sp500_change_pct"),
                    dow_jones_value=indices.get("dow_jones_value"),
                    nasdaq_value=indices.get("nasdaq_value"),
                    vix_value=indices.get("vix_value"),
                    reit_etf_vnq=reits.get("reit_etf_vnq"),
                    reit_sector_change_pct=reits.get("reit_sector_change_pct"),
                    treasury_10y=rates.get("treasury_10y"),
                    treasury_30y=rates.get("treasury_30y"),
                    fed_funds_rate=rates.get("fed_funds_rate"),
                    mortgage_30y=rates.get("mortgage_30y"),
                    unemployment_rate=economic.get("unemployment_rate"),
                    inflation_rate=economic.get("inflation_rate"),
                    gdp_growth_rate=economic.get("gdp_growth_rate"),
                    home_price_index=economic.get("home_price_index"),
                    housing_starts=economic.get("housing_starts"),
                    building_permits=economic.get("building_permits"),
                    full_data=full_data,
                    data_completeness_pct=self._to_decimal(completeness),
                    data_sources_count=len(self.status["sources_success"])
                )
                self.db.add(snapshot)

                logger.info(f"  ✅ Created new snapshot ({completeness:.1f}% complete)")

            self.db.commit()
            return True

        except Exception as e:
            logger.error(f"  ❌ Failed to create snapshot: {str(e)}")
            return False

    async def _get_latest_indices(self) -> Dict:
        """Get latest market indices from database"""
        indices = {}

        try:
            sp500 = self.db.query(YFinanceMarketData).filter(
                YFinanceMarketData.ticker == "^GSPC",
                YFinanceMarketData.data_timestamp >= datetime.now() - timedelta(days=1)
            ).order_by(YFinanceMarketData.data_timestamp.desc()).first()

            if sp500:
                indices["sp500_value"] = sp500.current_price
                indices["sp500_change_pct"] = sp500.price_change_pct

            dow = self.db.query(YFinanceMarketData).filter(
                YFinanceMarketData.ticker == "^DJI",
                YFinanceMarketData.data_timestamp >= datetime.now() - timedelta(days=1)
            ).order_by(YFinanceMarketData.data_timestamp.desc()).first()

            if dow:
                indices["dow_jones_value"] = dow.current_price

            nasdaq = self.db.query(YFinanceMarketData).filter(
                YFinanceMarketData.ticker == "^IXIC",
                YFinanceMarketData.data_timestamp >= datetime.now() - timedelta(days=1)
            ).order_by(YFinanceMarketData.data_timestamp.desc()).first()

            if nasdaq:
                indices["nasdaq_value"] = nasdaq.current_price

            vix = self.db.query(YFinanceMarketData).filter(
                YFinanceMarketData.ticker == "^VIX",
                YFinanceMarketData.data_timestamp >= datetime.now() - timedelta(days=1)
            ).order_by(YFinanceMarketData.data_timestamp.desc()).first()

            if vix:
                indices["vix_value"] = vix.current_price

        except Exception as e:
            logger.error(f"Error getting indices: {str(e)}")

        return indices

    async def _get_latest_reits(self) -> Dict:
        """Get latest REIT data from database"""
        reits = {}

        try:
            vnq = self.db.query(YFinanceMarketData).filter(
                YFinanceMarketData.ticker == "VNQ",
                YFinanceMarketData.data_timestamp >= datetime.now() - timedelta(days=1)
            ).order_by(YFinanceMarketData.data_timestamp.desc()).first()

            if vnq:
                reits["reit_etf_vnq"] = vnq.current_price
                reits["reit_sector_change_pct"] = vnq.price_change_pct

        except Exception as e:
            logger.error(f"Error getting REITs: {str(e)}")

        return reits

    async def _get_latest_rates(self) -> Dict:
        """Get latest rates from database"""
        rates = {}

        try:
            tnx = self.db.query(YFinanceMarketData).filter(
                YFinanceMarketData.ticker == "^TNX",
                YFinanceMarketData.data_timestamp >= datetime.now() - timedelta(days=1)
            ).order_by(YFinanceMarketData.data_timestamp.desc()).first()

            if tnx:
                rates["treasury_10y"] = tnx.current_price

            tyx = self.db.query(YFinanceMarketData).filter(
                YFinanceMarketData.ticker == "^TYX",
                YFinanceMarketData.data_timestamp >= datetime.now() - timedelta(days=1)
            ).order_by(YFinanceMarketData.data_timestamp.desc()).first()

            if tyx:
                rates["treasury_30y"] = tyx.current_price

        except Exception as e:
            logger.error(f"Error getting rates: {str(e)}")

        return rates

    async def _get_latest_economic(self) -> Dict:
        """Get latest economic indicators from database"""
        economic = {}

        try:
            # This would query economic indicators from database
            # For now, return empty dict as we just started collecting
            pass

        except Exception as e:
            logger.error(f"Error getting economic data: {str(e)}")

        return economic

    async def _get_yesterday_data(self, cache_key: str) -> Optional[Dict]:
        """Get yesterday's data from database as fallback"""
        # This would query yesterday's snapshot from database
        # Return None for now
        return None

    async def _cleanup_old_data(self):
        """Remove data older than retention period"""
        try:
            # Keep 90 days of daily data
            cutoff_date = datetime.now() - timedelta(days=90)

            deleted_yfinance = self.db.query(YFinanceMarketData).filter(
                YFinanceMarketData.created_at < cutoff_date
            ).delete()

            deleted_economic = self.db.query(EconomicIndicator).filter(
                EconomicIndicator.created_at < cutoff_date
            ).delete()

            # Keep 180 days of snapshots
            snapshot_cutoff = datetime.now() - timedelta(days=180)
            deleted_snapshots = self.db.query(MarketIntelligenceSnapshot).filter(
                MarketIntelligenceSnapshot.created_at < snapshot_cutoff
            ).delete()

            self.db.commit()

            logger.info(f"  ✅ Cleaned up {deleted_yfinance + deleted_economic + deleted_snapshots} old records")

        except Exception as e:
            logger.error(f"  ⚠️  Cleanup error: {str(e)}")

    async def _log_import(
        self,
        source: str,
        status: str,
        records_created: int,
        records_updated: int,
        error_msg: str = None
    ):
        """Log import job to database"""
        try:
            import_log = MarketDataImport(
                data_source=source,
                import_type="daily_update",
                status=status,
                records_created=records_created,
                records_updated=records_updated,
                started_at=self.status["started_at"],
                completed_at=datetime.now(),
                error_message=error_msg
            )
            self.db.add(import_log)
            self.db.commit()

        except Exception as e:
            logger.error(f"Error logging import: {str(e)}")

    async def _calculate_trends(self) -> int:
        """
        Calculate trends for all tracked indicators

        Returns:
            Number of trends calculated
        """
        trends_count = 0

        try:
            # Get unique tickers from recent YFinance data
            recent_tickers = self.db.query(YFinanceMarketData.ticker, YFinanceMarketData.security_type).filter(
                YFinanceMarketData.data_timestamp >= datetime.now() - timedelta(days=1)
            ).distinct().all()

            logger.info(f"  → Calculating trends for {len(recent_tickers)} indicators...")

            for ticker, sec_type in recent_tickers:
                try:
                    trend = await self.analytics.calculate_trends(
                        ticker=ticker,
                        indicator_type=sec_type or 'stock'
                    )
                    if trend:
                        trends_count += 1
                except Exception as e:
                    logger.warning(f"    Failed to calculate trend for {ticker}: {str(e)}")
                    continue

            logger.info(f"  ✅ Calculated {trends_count} market trends")

        except Exception as e:
            logger.error(f"  ❌ Trend calculation failed: {str(e)}")

        return trends_count

    async def _calculate_correlations(self) -> int:
        """
        Calculate correlations between key market indicators

        Returns:
            Number of correlations calculated
        """
        correlations_count = 0

        try:
            # Define key correlation pairs to track
            correlation_pairs = [
                # REITs vs Interest Rates
                ('VNQ', 'reit', '^TNX', 'rate'),  # VNQ vs 10Y Treasury
                ('IYR', 'reit', '^TYX', 'rate'),  # IYR vs 30Y Treasury

                # REITs vs Market Indices
                ('VNQ', 'reit', '^GSPC', 'index'),  # VNQ vs S&P 500
                ('XLRE', 'reit', '^GSPC', 'index'),  # XLRE vs S&P 500

                # Interest Rate Spreads
                ('^TNX', 'rate', '^TYX', 'rate'),  # 10Y vs 30Y spread

                # REITs correlation
                ('VNQ', 'reit', 'IYR', 'reit'),  # VNQ vs IYR
            ]

            logger.info(f"  → Calculating {len(correlation_pairs)} correlation pairs...")

            for symbol1, type1, symbol2, type2 in correlation_pairs:
                try:
                    correlation = await self.analytics.calculate_correlation(
                        symbol1=symbol1,
                        type1=type1,
                        symbol2=symbol2,
                        type2=type2,
                        period_days=90
                    )
                    if correlation:
                        correlations_count += 1
                except Exception as e:
                    logger.warning(f"    Failed to calculate correlation {symbol1}-{symbol2}: {str(e)}")
                    continue

            logger.info(f"  ✅ Calculated {correlations_count} market correlations")

        except Exception as e:
            logger.error(f"  ❌ Correlation calculation failed: {str(e)}")

        return correlations_count

    async def _generate_insights(self) -> int:
        """
        Generate actionable market insights

        Returns:
            Number of insights generated
        """
        insights_count = 0

        try:
            logger.info(f"  → Generating market insights...")

            insights = await self.analytics.generate_insights()
            insights_count = len(insights)

            if insights_count > 0:
                # Save insights to database
                for insight in insights:
                    self.db.add(insight)

                self.db.commit()
                logger.info(f"  ✅ Generated {insights_count} market insights")
            else:
                logger.info(f"  ℹ️  No new insights generated")

        except Exception as e:
            logger.error(f"  ❌ Insight generation failed: {str(e)}")

        return insights_count

    @staticmethod
    def _to_decimal(value: Any) -> Optional[Decimal]:
        """Convert value to Decimal safely"""
        if value is None:
            return None
        try:
            return Decimal(str(value))
        except:
            return None


# ============================================================================
# Standalone execution
# ============================================================================

async def run_daily_update():
    """Run daily update as standalone script"""
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Get database session
    db = next(get_db())

    try:
        updater = MarketIntelligenceUpdater(db)
        result = await updater.run_daily_update()

        # Print summary
        print("\n" + "=" * 80)
        print("DAILY UPDATE SUMMARY")
        print("=" * 80)
        print(f"Started:  {result['started_at']}")
        print(f"Finished: {result['completed_at']}")
        print(f"Duration: {(result['completed_at'] - result['started_at']).total_seconds():.2f}s")
        print(f"\n✅ Success: {result['total_success']}")
        print(f"❌ Failures: {result['total_failures']}")
        print(f"\nSources Success: {', '.join(result['sources_success']) or 'None'}")
        if result['sources_failed']:
            print(f"Sources Failed: {', '.join(result['sources_failed'])}")
        if result['errors']:
            print(f"\nErrors:")
            for error in result['errors']:
                print(f"  - {error}")
        print("=" * 80 + "\n")

        return result

    finally:
        db.close()


if __name__ == "__main__":
    # Run the update
    asyncio.run(run_daily_update())
