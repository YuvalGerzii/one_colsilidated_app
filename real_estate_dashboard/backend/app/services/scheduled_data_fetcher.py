"""
Scheduled Data Fetcher Service

Fetches market data from integrations on a scheduled basis.
Runs daily to keep market intelligence data fresh and historical.
"""

import logging
import asyncio
from datetime import datetime, date, timedelta
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.integrations.manager import integration_manager
from app.models.market_data import (
    EmploymentData,
    HousingIndicators,
    InterestRates,
    EconomicIndicators,
    MarketDataFetchLog,
)
from app.integrations.cache_utils import FHFADataCache, BankOfIsraelDataCache, DataUpdateLogger

logger = logging.getLogger(__name__)


class ScheduledDataFetcher:
    """
    Fetches market data from integrations and saves to database

    Designed to run daily via cron or APScheduler
    """

    def __init__(self):
        self.db: Optional[Session] = None

    def _get_db(self) -> Session:
        """Get database session"""
        if self.db is None:
            self.db = SessionLocal()
        return self.db

    def _close_db(self):
        """Close database session"""
        if self.db:
            self.db.close()
            self.db = None

    def _log_fetch(
        self,
        data_source: str,
        data_type: str,
        success: str,
        records_fetched: int = 0,
        records_saved: int = 0,
        error_message: Optional[str] = None,
        duration_seconds: float = 0.0,
        retry_count: int = 0,
        metadata: Optional[Dict] = None
    ):
        """Log data fetch operation to database"""
        try:
            db = self._get_db()

            fetch_log = MarketDataFetchLog(
                fetch_date=datetime.utcnow(),
                data_source=data_source,
                data_type=data_type,
                success=success,
                records_fetched=records_fetched,
                records_saved=records_saved,
                error_message=error_message,
                retry_count=retry_count,
                duration_seconds=duration_seconds,
                fetch_metadata=metadata or {}
            )

            db.add(fetch_log)
            db.commit()

        except Exception as e:
            logger.error(f"Failed to log fetch operation: {e}")
            if self.db:
                self.db.rollback()

    async def fetch_employment_data(self, area_code: str = "0000000") -> Dict[str, Any]:
        """
        Fetch employment data from BLS and save to database

        Returns summary of fetch operation
        """
        start_time = datetime.utcnow()
        data_source = "bls"
        data_type = "employment"

        try:
            logger.info(f"Fetching employment data for area {area_code}...")

            # Get BLS integration
            bls = integration_manager.get("bls")
            if not bls or not bls.is_available:
                error_msg = "BLS integration not available"
                logger.warning(error_msg)
                self._log_fetch(data_source, data_type, "failed", error_message=error_msg)
                return {"success": False, "error": error_msg}

            # Fetch data with retry
            result = await bls._retry_with_exponential_backoff(
                lambda: bls.get_employment_stats(area_code),
                max_retries=3,
                operation_name="BLS employment data fetch"
            )

            if not result.success or not result.data:
                error_msg = result.error or "No data returned"
                logger.warning(f"Failed to fetch employment data: {error_msg}")
                duration = (datetime.utcnow() - start_time).total_seconds()
                self._log_fetch(data_source, data_type, "failed", error_message=error_msg, duration_seconds=duration)
                return {"success": False, "error": error_msg}

            # Parse and save to database
            db = self._get_db()
            series_data = result.data.get("series_data", {})

            records_saved = 0
            today = date.today()

            # Extract unemployment rate
            unemployment_series_id = f"LAUMT{area_code}0000000003" if area_code != "0000000" else "LNS14000000"
            if unemployment_series_id in series_data:
                unemployment_data = series_data[unemployment_series_id]
                if unemployment_data and len(unemployment_data) > 0:
                    latest = unemployment_data[0]

                    # Check if we already have today's data
                    existing = db.query(EmploymentData).filter(
                        EmploymentData.area_code == area_code,
                        EmploymentData.data_date == today
                    ).first()

                    if not existing:
                        employment_record = EmploymentData(
                            area_code=area_code,
                            area_name="National" if area_code == "0000000" else f"Area {area_code}",
                            unemployment_rate=float(latest.get("value", 0)),
                            data_date=today,
                            source="bls",
                            series_data=series_data,
                            notes=f"Fetched from BLS on {datetime.utcnow().isoformat()}"
                        )

                        db.add(employment_record)
                        db.commit()
                        records_saved += 1
                        logger.info(f"Saved employment data for {area_code}")

            duration = (datetime.utcnow() - start_time).total_seconds()
            self._log_fetch(
                data_source,
                data_type,
                "success" if records_saved > 0 else "partial",
                records_fetched=len(series_data),
                records_saved=records_saved,
                duration_seconds=duration
            )

            return {
                "success": True,
                "records_saved": records_saved,
                "duration_seconds": duration
            }

        except Exception as e:
            logger.error(f"Error fetching employment data: {e}", exc_info=True)
            duration = (datetime.utcnow() - start_time).total_seconds()
            self._log_fetch(data_source, data_type, "failed", error_message=str(e), duration_seconds=duration)
            return {"success": False, "error": str(e)}

    async def fetch_cpi_data(self) -> Dict[str, Any]:
        """
        Fetch Consumer Price Index (CPI) data from BLS

        Returns summary of fetch operation
        """
        start_time = datetime.utcnow()
        data_source = "bls"
        data_type = "cpi"

        try:
            logger.info("Fetching CPI data...")

            bls = integration_manager.get("bls")
            if not bls or not bls.is_available:
                error_msg = "BLS integration not available"
                logger.warning(error_msg)
                self._log_fetch(data_source, data_type, "failed", error_message=error_msg)
                return {"success": False, "error": error_msg}

            # Fetch data with retry
            result = await bls._retry_with_exponential_backoff(
                lambda: bls.get_cpi(),
                max_retries=3,
                operation_name="BLS CPI data fetch"
            )

            if not result.success or not result.data:
                error_msg = result.error or "No data returned"
                duration = (datetime.utcnow() - start_time).total_seconds()
                self._log_fetch(data_source, data_type, "failed", error_message=error_msg, duration_seconds=duration)
                return {"success": False, "error": error_msg}

            # Save to database
            db = self._get_db()
            series_data = result.data.get("series_data", {})

            records_saved = 0
            today = date.today()

            # CPI series ID
            cpi_series_id = "CUSR0000SA0"
            if cpi_series_id in series_data:
                cpi_data = series_data[cpi_series_id]
                if cpi_data and len(cpi_data) > 0:
                    latest = cpi_data[0]

                    # Check if we already have today's data
                    existing = db.query(EconomicIndicators).filter(
                        EconomicIndicators.data_date == today,
                        EconomicIndicators.geography == "US"
                    ).first()

                    if not existing:
                        econ_record = EconomicIndicators(
                            data_date=today,
                            geography="US",
                            cpi_all_items=float(latest.get("value", 0)),
                            source="bls",
                            raw_data=series_data,
                            notes=f"Fetched from BLS on {datetime.utcnow().isoformat()}"
                        )

                        db.add(econ_record)
                        db.commit()
                        records_saved += 1
                        logger.info("Saved CPI data")

            duration = (datetime.utcnow() - start_time).total_seconds()
            self._log_fetch(
                data_source,
                data_type,
                "success" if records_saved > 0 else "partial",
                records_fetched=len(series_data),
                records_saved=records_saved,
                duration_seconds=duration
            )

            return {
                "success": True,
                "records_saved": records_saved,
                "duration_seconds": duration
            }

        except Exception as e:
            logger.error(f"Error fetching CPI data: {e}", exc_info=True)
            duration = (datetime.utcnow() - start_time).total_seconds()
            self._log_fetch(data_source, data_type, "failed", error_message=str(e), duration_seconds=duration)
            return {"success": False, "error": str(e)}

    async def fetch_fhfa_hpi_data(self) -> Dict[str, Any]:
        """
        Fetch FHFA House Price Index data and save to database

        Updates national, state, and metro-level HPI data monthly
        Returns summary of fetch operation
        """
        start_time = datetime.utcnow()
        data_source = "fhfa"
        data_type = "hpi"

        try:
            logger.info("Fetching FHFA HPI data...")

            # Get FHFA integration
            fhfa = integration_manager.get("fhfa")
            if not fhfa or not fhfa.is_available:
                error_msg = "FHFA integration not available"
                logger.warning(error_msg)
                return {"success": False, "error": error_msg}

            db = self._get_db()

            # Start update log
            update_log = DataUpdateLogger.start_update(
                db,
                integration_name="fhfa",
                data_type="hpi",
                update_type="monthly",
                metadata={"fetch_date": start_time.isoformat()}
            )

            try:
                # Fetch national HPI (last 2 years to capture updates)
                current_year = datetime.now().year
                result = await fhfa.get_house_price_index(
                    geography_type="USA",
                    start_year=current_year - 2,
                    end_year=current_year,
                    db=db,
                    use_cache=False  # Force fresh download
                )

                if not result.success:
                    error_msg = result.error or "Failed to fetch HPI data"
                    logger.warning(f"FHFA fetch failed: {error_msg}")
                    DataUpdateLogger.fail_update(db, update_log, error_msg)
                    duration = (datetime.utcnow() - start_time).total_seconds()
                    return {"success": False, "error": error_msg, "duration_seconds": duration}

                # Data is automatically cached by the integration
                records_count = result.data.get('count', 0)

                # Complete update log
                DataUpdateLogger.complete_update(
                    db,
                    update_log,
                    records_processed=records_count,
                    records_inserted=records_count,
                    records_updated=0
                )

                duration = (datetime.utcnow() - start_time).total_seconds()
                logger.info(f"FHFA HPI data fetch completed: {records_count} records in {duration:.2f}s")

                return {
                    "success": True,
                    "records_saved": records_count,
                    "duration_seconds": duration,
                    "cached": result.data.get('cached', False)
                }

            except Exception as e:
                logger.error(f"Error during FHFA fetch: {e}", exc_info=True)
                DataUpdateLogger.fail_update(db, update_log, str(e))
                raise

        except Exception as e:
            logger.error(f"Error fetching FHFA HPI data: {e}", exc_info=True)
            duration = (datetime.utcnow() - start_time).total_seconds()
            return {"success": False, "error": str(e), "duration_seconds": duration}

    async def fetch_bank_of_israel_exchange_rates(self) -> Dict[str, Any]:
        """
        Fetch Bank of Israel exchange rates and save to database

        Updates daily exchange rates for major currencies (USD, EUR, GBP)
        Returns summary of fetch operation
        """
        start_time = datetime.utcnow()
        data_source = "bank_of_israel"
        data_type = "exchange_rates"

        try:
            logger.info("Fetching Bank of Israel exchange rates...")

            # Get Bank of Israel integration
            boi = integration_manager.get("bank_of_israel")
            if not boi or not boi.is_available:
                error_msg = "Bank of Israel integration not available"
                logger.warning(error_msg)
                return {"success": False, "error": error_msg}

            db = self._get_db()

            # Start update log
            update_log = DataUpdateLogger.start_update(
                db,
                integration_name="bank_of_israel",
                data_type="exchange_rates",
                update_type="daily",
                metadata={"fetch_date": start_time.isoformat()}
            )

            try:
                # Fetch latest exchange rates for major currencies
                currencies = ['USD', 'EUR', 'GBP', 'JPY', 'CHF']
                total_records = 0
                failed_currencies = []

                for currency in currencies:
                    try:
                        # Fetch last 7 days to capture any missed updates
                        end_date = datetime.now()
                        start_date = end_date - timedelta(days=7)

                        result = await boi.get_exchange_rate(
                            currency=currency,
                            start_date=start_date.strftime("%Y-%m-%d"),
                            end_date=end_date.strftime("%Y-%m-%d"),
                            db=db,
                            use_cache=False  # Force fresh download
                        )

                        if result.success:
                            count = result.data.get('count', 0)
                            total_records += count
                            logger.info(f"Fetched {count} {currency}/ILS exchange rates")
                        else:
                            failed_currencies.append(f"{currency}: {result.error}")
                            logger.warning(f"Failed to fetch {currency} rates: {result.error}")

                    except Exception as e:
                        failed_currencies.append(f"{currency}: {str(e)}")
                        logger.error(f"Error fetching {currency} rates: {e}", exc_info=True)

                # Complete update log
                DataUpdateLogger.complete_update(
                    db,
                    update_log,
                    records_processed=total_records,
                    records_inserted=total_records,
                    records_updated=0,
                    records_failed=len(failed_currencies)
                )

                duration = (datetime.utcnow() - start_time).total_seconds()
                logger.info(f"Bank of Israel exchange rate fetch completed: {total_records} records in {duration:.2f}s")

                return {
                    "success": True,
                    "records_saved": total_records,
                    "duration_seconds": duration,
                    "failed_currencies": failed_currencies if failed_currencies else None
                }

            except Exception as e:
                logger.error(f"Error during Bank of Israel fetch: {e}", exc_info=True)
                DataUpdateLogger.fail_update(db, update_log, str(e))
                raise

        except Exception as e:
            logger.error(f"Error fetching Bank of Israel exchange rates: {e}", exc_info=True)
            duration = (datetime.utcnow() - start_time).total_seconds()
            return {"success": False, "error": str(e), "duration_seconds": duration}

    async def fetch_bank_of_israel_cpi(self) -> Dict[str, Any]:
        """
        Fetch Bank of Israel CPI data and save to database

        Updates monthly CPI data
        Returns summary of fetch operation
        """
        start_time = datetime.utcnow()
        data_source = "bank_of_israel"
        data_type = "cpi"

        try:
            logger.info("Fetching Bank of Israel CPI data...")

            # Get Bank of Israel integration
            boi = integration_manager.get("bank_of_israel")
            if not boi or not boi.is_available:
                error_msg = "Bank of Israel integration not available"
                logger.warning(error_msg)
                return {"success": False, "error": error_msg}

            db = self._get_db()

            # Start update log
            update_log = DataUpdateLogger.start_update(
                db,
                integration_name="bank_of_israel",
                data_type="cpi",
                update_type="monthly",
                metadata={"fetch_date": start_time.isoformat()}
            )

            try:
                # Fetch last 12 months of CPI data
                end_date = datetime.now()
                start_date = end_date - timedelta(days=365)

                result = await boi.get_cpi(
                    start_date=start_date.strftime("%Y-%m-%d"),
                    end_date=end_date.strftime("%Y-%m-%d"),
                    db=db,
                    use_cache=False  # Force fresh download
                )

                if not result.success:
                    error_msg = result.error or "Failed to fetch CPI data"
                    logger.warning(f"BOI CPI fetch failed: {error_msg}")
                    DataUpdateLogger.fail_update(db, update_log, error_msg)
                    duration = (datetime.utcnow() - start_time).total_seconds()
                    return {"success": False, "error": error_msg, "duration_seconds": duration}

                records_count = result.data.get('count', 0)

                # Complete update log
                DataUpdateLogger.complete_update(
                    db,
                    update_log,
                    records_processed=records_count,
                    records_inserted=records_count,
                    records_updated=0
                )

                duration = (datetime.utcnow() - start_time).total_seconds()
                logger.info(f"BOI CPI data fetch completed: {records_count} records in {duration:.2f}s")

                return {
                    "success": True,
                    "records_saved": records_count,
                    "duration_seconds": duration,
                    "cached": result.data.get('cached', False)
                }

            except Exception as e:
                logger.error(f"Error during BOI CPI fetch: {e}", exc_info=True)
                DataUpdateLogger.fail_update(db, update_log, str(e))
                raise

        except Exception as e:
            logger.error(f"Error fetching BOI CPI data: {e}", exc_info=True)
            duration = (datetime.utcnow() - start_time).total_seconds()
            return {"success": False, "error": str(e), "duration_seconds": duration}

    async def fetch_bank_of_israel_interest_rate(self) -> Dict[str, Any]:
        """
        Fetch Bank of Israel interest rate data and save to database

        Updates monthly interest rate data
        Returns summary of fetch operation
        """
        start_time = datetime.utcnow()
        data_source = "bank_of_israel"
        data_type = "interest_rate"

        try:
            logger.info("Fetching Bank of Israel interest rate data...")

            # Get Bank of Israel integration
            boi = integration_manager.get("bank_of_israel")
            if not boi or not boi.is_available:
                error_msg = "Bank of Israel integration not available"
                logger.warning(error_msg)
                return {"success": False, "error": error_msg}

            db = self._get_db()

            # Start update log
            update_log = DataUpdateLogger.start_update(
                db,
                integration_name="bank_of_israel",
                data_type="interest_rate",
                update_type="monthly",
                metadata={"fetch_date": start_time.isoformat()}
            )

            try:
                # Fetch last 24 months of interest rate data
                end_date = datetime.now()
                start_date = end_date - timedelta(days=730)

                result = await boi.get_interest_rate(
                    start_date=start_date.strftime("%Y-%m-%d"),
                    end_date=end_date.strftime("%Y-%m-%d"),
                    db=db,
                    use_cache=False  # Force fresh download
                )

                if not result.success:
                    error_msg = result.error or "Failed to fetch interest rate data"
                    logger.warning(f"BOI interest rate fetch failed: {error_msg}")
                    DataUpdateLogger.fail_update(db, update_log, error_msg)
                    duration = (datetime.utcnow() - start_time).total_seconds()
                    return {"success": False, "error": error_msg, "duration_seconds": duration}

                records_count = result.data.get('count', 0)

                # Complete update log
                DataUpdateLogger.complete_update(
                    db,
                    update_log,
                    records_processed=records_count,
                    records_inserted=records_count,
                    records_updated=0
                )

                duration = (datetime.utcnow() - start_time).total_seconds()
                logger.info(f"BOI interest rate data fetch completed: {records_count} records in {duration:.2f}s")

                return {
                    "success": True,
                    "records_saved": records_count,
                    "duration_seconds": duration,
                    "cached": result.data.get('cached', False)
                }

            except Exception as e:
                logger.error(f"Error during BOI interest rate fetch: {e}", exc_info=True)
                DataUpdateLogger.fail_update(db, update_log, str(e))
                raise

        except Exception as e:
            logger.error(f"Error fetching BOI interest rate data: {e}", exc_info=True)
            duration = (datetime.utcnow() - start_time).total_seconds()
            return {"success": False, "error": str(e), "duration_seconds": duration}

    async def fetch_all_data(self) -> Dict[str, Any]:
        """
        Fetch all market data from available sources

        This is the main entry point for scheduled daily fetching
        """
        logger.info("=" * 80)
        logger.info("Starting scheduled market data fetch...")
        logger.info("=" * 80)

        overall_start = datetime.utcnow()
        results = {}

        try:
            # Fetch employment data (national)
            employment_result = await self.fetch_employment_data("0000000")
            results["employment_national"] = employment_result

            # Fetch CPI data
            cpi_result = await self.fetch_cpi_data()
            results["cpi"] = cpi_result

            # Fetch Bank of Israel exchange rates (daily)
            boi_result = await self.fetch_bank_of_israel_exchange_rates()
            results["bank_of_israel_exchange_rates"] = boi_result

            # Fetch Bank of Israel CPI (monthly)
            boi_cpi_result = await self.fetch_bank_of_israel_cpi()
            results["bank_of_israel_cpi"] = boi_cpi_result

            # Fetch Bank of Israel interest rate (monthly)
            boi_ir_result = await self.fetch_bank_of_israel_interest_rate()
            results["bank_of_israel_interest_rate"] = boi_ir_result

            # Fetch FHFA HPI data (monthly - checks cache staleness internally)
            fhfa_result = await self.fetch_fhfa_hpi_data()
            results["fhfa_hpi"] = fhfa_result

            # Calculate summary
            total_records = sum(r.get("records_saved", 0) for r in results.values())
            successful_fetches = sum(1 for r in results.values() if r.get("success", False))
            total_fetches = len(results)

            overall_duration = (datetime.utcnow() - overall_start).total_seconds()

            logger.info("=" * 80)
            logger.info(f"Scheduled data fetch completed in {overall_duration:.2f}s")
            logger.info(f"Successful fetches: {successful_fetches}/{total_fetches}")
            logger.info(f"Total records saved: {total_records}")
            logger.info("=" * 80)

            return {
                "success": True,
                "total_records_saved": total_records,
                "successful_fetches": successful_fetches,
                "total_fetches": total_fetches,
                "duration_seconds": overall_duration,
                "results": results
            }

        except Exception as e:
            logger.error(f"Error in scheduled data fetch: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "results": results
            }
        finally:
            self._close_db()


# Global instance
scheduled_data_fetcher = ScheduledDataFetcher()


async def run_daily_fetch():
    """
    Main function to run daily data fetch

    Can be called from:
    - APScheduler (recommended)
    - Cron job
    - Manual trigger via API endpoint
    """
    return await scheduled_data_fetcher.fetch_all_data()


if __name__ == "__main__":
    # Allow running this script directly for testing
    import sys
    sys.path.insert(0, "/Users/yuvalgerzi/Documents/personal projects/real_estate_dashboard/backend")

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    asyncio.run(run_daily_fetch())
