"""
Bank of Israel Integration - FREE
Access to Israeli economic and statistical data via SDMX API

Documentation: https://www.boi.org.il/en/economic-roles/statistics/
SDMX API: https://edge.boi.org.il/FusionEdgeServer/sdmx/v2/
Series Database: https://edge.boi.gov.il/
"""

from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import httpx
import xml.etree.ElementTree as ET
from sqlalchemy.orm import Session
from ..base import BaseIntegration, IntegrationConfig, IntegrationMetadata, IntegrationResponse
from ..cache_utils import BankOfIsraelDataCache, DataUpdateLogger
from ..retry_utils import retry_async, STANDARD_RETRY


class BankOfIsraelIntegration(BaseIntegration):
    """
    Integration with Bank of Israel Statistical Data via SDMX API
    FREE - No API key required

    Provides access to economic indicators, CPI, interest rates, exchange rates and more
    Uses SDMX 2.0 REST API for data access
    """

    BASE_URL = "https://edge.boi.org.il"
    SDMX_API_URL = "https://edge.boi.org.il/FusionEdgeServer/sdmx/v2"
    DATAFLOW_BASE = f"{SDMX_API_URL}/data/dataflow/BOI.STATISTICS"

    # Common series codes
    SERIES_CODES = {
        # Exchange Rates (EXR)
        'USD_ILS': 'RER_USD_ILS',  # US Dollar to ILS
        'EUR_ILS': 'RER_EUR_ILS',  # Euro to ILS
        'GBP_ILS': 'RER_GBP_ILS',  # British Pound to ILS
        'JPY_ILS': 'RER_JPY_ILS',  # Japanese Yen to ILS
        'CHF_ILS': 'RER_CHF_ILS',  # Swiss Franc to ILS

        # Interest Rates
        'INTEREST_RATE': 'INTEREST_RATE_BOI',  # Bank of Israel interest rate

        # CPI
        'CPI_TOTAL': 'CPI_TOTAL',  # Consumer Price Index
        'CPI_HOUSING': 'CPI_HOUSING',  # CPI for housing
    }

    def __init__(self, config: IntegrationConfig):
        config.is_free = True
        config.requires_api_key = False
        super().__init__(config)

    def get_metadata(self) -> IntegrationMetadata:
        return IntegrationMetadata(
            name="Bank of Israel",
            category="official_data",
            description="Israeli central bank economic and statistical data via SDMX API",
            is_free=True,
            requires_api_key=False,
            documentation_url="https://www.boi.org.il/en/economic-roles/statistics/",
            features=[
                "Exchange rates (USD, EUR, GBP, JPY, CHF, etc.)",
                "Representative exchange rates",
                "Bank of Israel interest rate",
                "Consumer Price Index (CPI)",
                "Housing price index",
                "Economic indicators",
                "GDP data",
                "Employment statistics",
                "Balance of payments",
                "SDMX 2.0 REST API access"
            ]
        )

    async def test_connection(self) -> IntegrationResponse:
        """Test Bank of Israel SDMX API connection"""
        try:
            # Test by fetching USD/ILS exchange rate
            result = await self.get_exchange_rate('USD')

            if result.success:
                return self._success_response({
                    "message": "Successfully connected to Bank of Israel SDMX API",
                    "status": "operational",
                    "api_url": self.SDMX_API_URL,
                    "sample_data": result.data.get('data', [])[:1] if result.data.get('data') else []
                })
            else:
                return result

        except Exception as e:
            return self._handle_error(e, "Bank of Israel connection test")

    async def get_sdmx_data(
        self,
        dataflow_id: str,
        series_code: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        format: str = "csv"
    ) -> IntegrationResponse:
        """Fetch data from Bank of Israel SDMX API"""
        if not self.is_available:
            return IntegrationResponse(success=False, error="Integration not available")

        try:
            url = f"{self.DATAFLOW_BASE}/{dataflow_id}/1.0/{series_code}"
            params = {"format": format}
            if start_date:
                params["startPeriod"] = start_date
            if end_date:
                params["endPeriod"] = end_date

            async def _fetch_sdmx_data():
                async with httpx.AsyncClient(follow_redirects=True) as client:
                    response = await client.get(url, params=params, timeout=30.0, headers={"User-Agent": "Mozilla/5.0"})
                    response.raise_for_status()
                    return response.text

            # Use retry logic for network resilience
            response_text = await retry_async(
                _fetch_sdmx_data,
                config=STANDARD_RETRY,
                operation_name=f"Bank of Israel SDMX {dataflow_id}/{series_code}"
            )

            if format == "csv":
                lines = response_text.strip().split('\n')
                if len(lines) < 2:
                    return IntegrationResponse(success=False, error="No data returned")

                headers = lines[0].split(',')
                data = [dict(zip(headers, line.split(','))) for line in lines[1:] if len(line.split(',')) == len(headers)]

                return self._success_response({"data": data, "count": len(data), "dataflow": dataflow_id, "series": series_code})
            else:
                return self._success_response({"data": response_text, "format": format})

        except Exception as e:
            return self._handle_error(e, "get_sdmx_data")

    async def get_exchange_rate(
        self,
        currency: str = "USD",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        db: Optional[Session] = None,
        use_cache: bool = True
    ) -> IntegrationResponse:
        """
        Get exchange rate for currency vs ILS

        With caching: Checks database cache first, fetches from API if stale

        Args:
            currency: Currency code (USD, EUR, GBP, etc.)
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            db: Database session for caching
            use_cache: Whether to use database cache
        """
        if not self.is_available:
            return IntegrationResponse(success=False, error="Integration not available")

        try:
            series_code = self.SERIES_CODES.get(f"{currency}_ILS", f"RER_{currency}_ILS")

            # Parse dates
            if not end_date:
                end_date_obj = datetime.now()
                end_date = end_date_obj.strftime("%Y-%m-%d")
            else:
                end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")

            if not start_date:
                start_date_obj = end_date_obj - timedelta(days=30)
                start_date = start_date_obj.strftime("%Y-%m-%d")
            else:
                start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")

            # Try cache first if enabled
            if db and use_cache:
                cache_stale = BankOfIsraelDataCache.is_cache_stale(db, currency, "ILS", max_age_days=1)

                if not cache_stale:
                    # Get from cache
                    cached_rates = BankOfIsraelDataCache.get_exchange_rates(
                        db,
                        base_currency=currency,
                        quote_currency="ILS",
                        start_date=start_date_obj,
                        end_date=end_date_obj,
                        limit=1000
                    )

                    if cached_rates:
                        # Convert ORM objects to dict
                        data = [{
                            'TIME_PERIOD': r.date.strftime("%Y-%m-%d"),
                            'OBS_VALUE': str(r.rate),
                            'SERIES': r.series_code,
                            'DATAFLOW': 'BOI.STATISTICS:EXR(1.0)'
                        } for r in cached_rates]

                        return self._success_response({
                            "currency": currency,
                            "base_currency": "ILS",
                            "data": data,
                            "count": len(data),
                            "date_range": f"{start_date} to {end_date}",
                            "source": "Bank of Israel Database Cache",
                            "cached": True
                        })

            # Fetch from API
            result = await self.get_sdmx_data("EXR", series_code, start_date, end_date, "csv")

            if result.success:
                # Save to cache if db available
                if db and result.data.get('data'):
                    await BankOfIsraelDataCache.save_exchange_rates(
                        db,
                        result.data['data'],
                        base_currency=currency,
                        quote_currency="ILS",
                        series_code=series_code
                    )

                return self._success_response({
                    "currency": currency,
                    "base_currency": "ILS",
                    "data": result.data.get('data', []),
                    "count": result.data.get('count', 0),
                    "date_range": f"{start_date} to {end_date}",
                    "source": "Bank of Israel SDMX API",
                    "cached": False
                })
            return result

        except Exception as e:
            return self._handle_error(e, "get_exchange_rate")

    async def get_latest_exchange_rates(
        self,
        currencies: Optional[List[str]] = None,
        db: Optional[Session] = None
    ) -> IntegrationResponse:
        """
        Get latest exchange rates for multiple currencies

        Args:
            currencies: List of currency codes (default: USD, EUR, GBP)
            db: Database session for caching
        """
        if not currencies:
            currencies = ['USD', 'EUR', 'GBP']

        rates, errors = {}, []
        for currency in currencies:
            # Try cache first if db available
            if db:
                latest_rate = BankOfIsraelDataCache.get_latest_rate(db, currency, "ILS")
                if latest_rate:
                    # Check if rate is recent (within last 2 days)
                    age = datetime.now() - latest_rate.date.replace(tzinfo=None)
                    if age.days < 2:
                        rates[currency] = {
                            'rate': str(latest_rate.rate),
                            'date': latest_rate.date.strftime("%Y-%m-%d"),
                            'cached': True
                        }
                        continue

            # Fetch from API if not in cache or stale
            result = await self.get_exchange_rate(currency, db=db)
            if result.success and result.data.get('data'):
                latest = result.data['data'][-1]
                rates[currency] = {
                    'rate': latest.get('OBS_VALUE', latest.get('VALUE')),
                    'date': latest.get('TIME_PERIOD', latest.get('DATE')),
                    'cached': result.data.get('cached', False)
                }
            else:
                errors.append(f"{currency}: {result.error}")

        if rates:
            return self._success_response({"rates": rates, "errors": errors if errors else None})
        return IntegrationResponse(success=False, error=f"Failed to fetch rates. Errors: {errors}")

    async def get_cpi(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        db: Optional[Session] = None,
        use_cache: bool = True
    ) -> IntegrationResponse:
        """
        Get Consumer Price Index (CPI) data from Bank of Israel

        With caching: Checks database cache first, fetches from API if stale

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            db: Database session for caching
            use_cache: Whether to use database cache
        """
        if not self.is_available:
            return IntegrationResponse(success=False, error="Integration not available")

        try:
            # Parse dates
            if not end_date:
                end_date_obj = datetime.now()
                end_date = end_date_obj.strftime("%Y-%m-%d")
            else:
                end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")

            if not start_date:
                # Default to last 12 months for CPI
                start_date_obj = end_date_obj - timedelta(days=365)
                start_date = start_date_obj.strftime("%Y-%m-%d")
            else:
                start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")

            # Try cache first if enabled and db available
            if db and use_cache:
                # Check if we have recent CPI data in EconomicIndicator table
                from app.models.official_data import EconomicIndicator
                from sqlalchemy import and_, desc

                cached_cpi = db.query(EconomicIndicator).filter(
                    and_(
                        EconomicIndicator.source == "boi",
                        EconomicIndicator.country == "IL",
                        EconomicIndicator.indicator_type == "cpi",
                        EconomicIndicator.date >= start_date_obj,
                        EconomicIndicator.date <= end_date_obj
                    )
                ).order_by(desc(EconomicIndicator.date)).all()

                if cached_cpi:
                    # Check if cache is recent (less than 30 days old)
                    latest_record = cached_cpi[0]
                    age = datetime.now() - latest_record.created_at.replace(tzinfo=None)

                    if age.days < 30:
                        data = [{
                            'TIME_PERIOD': r.date.strftime("%Y-%m-%d"),
                            'OBS_VALUE': str(r.value),
                            'INDICATOR': r.indicator_code,
                            'DATAFLOW': 'BOI.STATISTICS:CPI(1.0)'
                        } for r in cached_cpi]

                        return self._success_response({
                            "indicator": "CPI",
                            "country": "IL",
                            "data": data,
                            "count": len(data),
                            "date_range": f"{start_date} to {end_date}",
                            "source": "Bank of Israel Database Cache",
                            "cached": True
                        })

            # Fetch from API - try CPI dataflow
            # BOI CPI series code from their SDMX API
            result = await self.get_sdmx_data("CPI", "M.IL.N.CPI.CPI.IDX", start_date, end_date, "csv")

            if result.success and result.data.get('data'):
                # Save to cache if db available
                if db:
                    from app.models.official_data import EconomicIndicator

                    for record in result.data['data']:
                        try:
                            date_str = record.get('TIME_PERIOD') or record.get('DATE')
                            if not date_str:
                                continue

                            record_date = datetime.strptime(date_str, "%Y-%m-%d")
                            value = float(record.get('OBS_VALUE') or record.get('VALUE', 0))

                            # Check if exists
                            existing = db.query(EconomicIndicator).filter(
                                and_(
                                    EconomicIndicator.source == "boi",
                                    EconomicIndicator.country == "IL",
                                    EconomicIndicator.indicator_type == "cpi",
                                    EconomicIndicator.date == record_date
                                )
                            ).first()

                            if not existing:
                                indicator = EconomicIndicator(
                                    source="boi",
                                    country="IL",
                                    indicator_code="M.IL.N.CPI.CPI.IDX",
                                    indicator_name="Consumer Price Index",
                                    indicator_type="cpi",
                                    year=record_date.year,
                                    month=record_date.month,
                                    date=record_date,
                                    value=value,
                                    value_unit="index",
                                    raw_data=record
                                )
                                db.add(indicator)
                        except Exception as e:
                            continue

                    try:
                        db.commit()
                    except Exception as e:
                        db.rollback()

                return self._success_response({
                    "indicator": "CPI",
                    "country": "IL",
                    "data": result.data.get('data', []),
                    "count": result.data.get('count', 0),
                    "date_range": f"{start_date} to {end_date}",
                    "source": "Bank of Israel SDMX API",
                    "cached": False
                })

            return result

        except Exception as e:
            return self._handle_error(e, "get_cpi")

    async def get_interest_rate(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        db: Optional[Session] = None,
        use_cache: bool = True
    ) -> IntegrationResponse:
        """
        Get Bank of Israel interest rate data

        With caching: Checks database cache first, fetches from API if stale

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            db: Database session for caching
            use_cache: Whether to use database cache
        """
        if not self.is_available:
            return IntegrationResponse(success=False, error="Integration not available")

        try:
            # Parse dates
            if not end_date:
                end_date_obj = datetime.now()
                end_date = end_date_obj.strftime("%Y-%m-%d")
            else:
                end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")

            if not start_date:
                # Default to last 24 months for interest rates
                start_date_obj = end_date_obj - timedelta(days=730)
                start_date = start_date_obj.strftime("%Y-%m-%d")
            else:
                start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")

            # Try cache first if enabled and db available
            if db and use_cache:
                from app.models.official_data import EconomicIndicator
                from sqlalchemy import and_, desc

                cached_rates = db.query(EconomicIndicator).filter(
                    and_(
                        EconomicIndicator.source == "boi",
                        EconomicIndicator.country == "IL",
                        EconomicIndicator.indicator_type == "interest_rate",
                        EconomicIndicator.date >= start_date_obj,
                        EconomicIndicator.date <= end_date_obj
                    )
                ).order_by(desc(EconomicIndicator.date)).all()

                if cached_rates:
                    # Check if cache is recent (less than 7 days old)
                    latest_record = cached_rates[0]
                    age = datetime.now() - latest_record.created_at.replace(tzinfo=None)

                    if age.days < 7:
                        data = [{
                            'TIME_PERIOD': r.date.strftime("%Y-%m-%d"),
                            'OBS_VALUE': str(r.value),
                            'INDICATOR': r.indicator_code,
                            'DATAFLOW': 'BOI.STATISTICS:IR(1.0)'
                        } for r in cached_rates]

                        return self._success_response({
                            "indicator": "Interest Rate",
                            "country": "IL",
                            "data": data,
                            "count": len(data),
                            "date_range": f"{start_date} to {end_date}",
                            "source": "Bank of Israel Database Cache",
                            "cached": True
                        })

            # Fetch from API - BOI interest rate series code
            result = await self.get_sdmx_data("IR", "M.IL.N.BOI_IR.INT", start_date, end_date, "csv")

            if result.success and result.data.get('data'):
                # Save to cache if db available
                if db:
                    from app.models.official_data import EconomicIndicator

                    for record in result.data['data']:
                        try:
                            date_str = record.get('TIME_PERIOD') or record.get('DATE')
                            if not date_str:
                                continue

                            record_date = datetime.strptime(date_str, "%Y-%m-%d")
                            value = float(record.get('OBS_VALUE') or record.get('VALUE', 0))

                            # Check if exists
                            existing = db.query(EconomicIndicator).filter(
                                and_(
                                    EconomicIndicator.source == "boi",
                                    EconomicIndicator.country == "IL",
                                    EconomicIndicator.indicator_type == "interest_rate",
                                    EconomicIndicator.date == record_date
                                )
                            ).first()

                            if not existing:
                                indicator = EconomicIndicator(
                                    source="boi",
                                    country="IL",
                                    indicator_code="M.IL.N.BOI_IR.INT",
                                    indicator_name="Bank of Israel Interest Rate",
                                    indicator_type="interest_rate",
                                    year=record_date.year,
                                    month=record_date.month,
                                    date=record_date,
                                    value=value,
                                    value_unit="percentage",
                                    raw_data=record
                                )
                                db.add(indicator)
                        except Exception as e:
                            continue

                    try:
                        db.commit()
                    except Exception as e:
                        db.rollback()

                return self._success_response({
                    "indicator": "Interest Rate",
                    "country": "IL",
                    "data": result.data.get('data', []),
                    "count": result.data.get('count', 0),
                    "date_range": f"{start_date} to {end_date}",
                    "source": "Bank of Israel SDMX API",
                    "cached": False
                })

            return result

        except Exception as e:
            return self._handle_error(e, "get_interest_rate")
