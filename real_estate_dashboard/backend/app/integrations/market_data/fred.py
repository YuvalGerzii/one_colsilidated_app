"""
Federal Reserve Economic Data (FRED) Integration - FREE with API key
Provides economic indicators and financial data
"""

from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import httpx
from ..base import BaseIntegration, IntegrationConfig, IntegrationMetadata, IntegrationResponse


class FREDIntegration(BaseIntegration):
    """
    Integration with FRED API (Federal Reserve Bank of St. Louis)
    FREE - Requires free API key
    Documentation: https://fred.stlouisfed.org/docs/api/
    """

    BASE_URL = "https://api.stlouisfed.org/fred"

    def __init__(self, config: IntegrationConfig):
        config.is_free = True
        config.requires_api_key = True  # Free API key required
        super().__init__(config)

    def get_metadata(self) -> IntegrationMetadata:
        return IntegrationMetadata(
            name="Federal Reserve Economic Data (FRED)",
            category="market_data",
            description="Access economic data from the Federal Reserve",
            is_free=True,
            requires_api_key=True,
            documentation_url="https://fred.stlouisfed.org/docs/api/",
            features=[
                "Interest rates and treasury yields",
                "GDP and economic growth metrics",
                "Housing market indicators",
                "Inflation data",
                "Mortgage rates",
                "Commodity prices",
                "Over 800,000+ economic time series"
            ]
        )

    async def test_connection(self) -> IntegrationResponse:
        """Test FRED API connection"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.BASE_URL}/series",
                    params={
                        "series_id": "GDP",
                        "api_key": self.config.api_key,
                        "file_type": "json"
                    },
                    timeout=10.0
                )
                response.raise_for_status()

                data = response.json()
                if "seriess" in data:
                    return self._success_response({
                        "message": "Successfully connected to FRED API",
                        "sample_data": data["seriess"][0]
                    })
                else:
                    return IntegrationResponse(
                        success=False,
                        error="Unexpected response from FRED API"
                    )

        except Exception as e:
            return self._handle_error(e, "FRED connection test")

    async def get_series_data(
        self,
        series_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: Optional[int] = None
    ) -> IntegrationResponse:
        """
        Get time series data from FRED

        Args:
            series_id: FRED series ID (e.g., "MORTGAGE30US" for 30-year mortgage rate)
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            limit: Limit number of observations
        """
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="FRED integration not available. Please configure FRED_API_KEY in your environment."
            )

        try:
            params = {
                "series_id": series_id,
                "api_key": self.config.api_key,
                "file_type": "json"
            }

            if start_date:
                params["observation_start"] = start_date
            if end_date:
                params["observation_end"] = end_date
            if limit:
                params["limit"] = limit

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.BASE_URL}/series/observations",
                    params=params,
                    timeout=30.0
                )
                response.raise_for_status()

                data = response.json()

                if "observations" in data:
                    return self._success_response({
                        "series_id": series_id,
                        "observations": data["observations"],
                        "count": len(data["observations"])
                    })
                else:
                    return IntegrationResponse(
                        success=False,
                        error=f"No observations found for series {series_id}"
                    )

        except Exception as e:
            return self._handle_error(e, "get_series_data")

    async def get_mortgage_rates(self, rate_type: str = "30Y") -> IntegrationResponse:
        """
        Get mortgage rate data

        Args:
            rate_type: "30Y" for 30-year, "15Y" for 15-year
        """
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="FRED integration not available"
            )

        try:
            series_map = {
                "30Y": "MORTGAGE30US",
                "15Y": "MORTGAGE15US",
            }

            series_id = series_map.get(rate_type, "MORTGAGE30US")

            # Get last year of data
            end_date = datetime.now()
            start_date = end_date - timedelta(days=365)

            result = await self.get_series_data(
                series_id=series_id,
                start_date=start_date.strftime("%Y-%m-%d"),
                end_date=end_date.strftime("%Y-%m-%d")
            )

            return result

        except Exception as e:
            return self._handle_error(e, "get_mortgage_rates")

    async def get_housing_indicators(self) -> IntegrationResponse:
        """Get key housing market indicators"""
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="FRED integration not available"
            )

        try:
            # Key housing series IDs
            series_ids = {
                "home_price_index": "CSUSHPISA",  # S&P Case-Shiller Home Price Index
                "housing_starts": "HOUST",  # Housing Starts
                "building_permits": "PERMIT",  # Building Permits
                "existing_home_sales": "EXHOSLUSM495S",  # Existing Home Sales
                "median_sales_price": "MSPUS",  # Median Sales Price
            }

            results = {}
            async with httpx.AsyncClient() as client:
                for indicator, series_id in series_ids.items():
                    try:
                        response = await client.get(
                            f"{self.BASE_URL}/series/observations",
                            params={
                                "series_id": series_id,
                                "api_key": self.config.api_key,
                                "file_type": "json",
                                "limit": 12,  # Last 12 observations
                                "sort_order": "desc"
                            },
                            timeout=10.0
                        )
                        response.raise_for_status()

                        data = response.json()
                        if "observations" in data:
                            results[indicator] = {
                                "series_id": series_id,
                                "latest_value": data["observations"][0] if data["observations"] else None,
                                "observations": data["observations"]
                            }
                    except Exception as e:
                        self.logger.warning(f"Failed to fetch {indicator}: {e}")
                        results[indicator] = {"error": str(e)}

            return self._success_response({
                "housing_indicators": results
            })

        except Exception as e:
            return self._handle_error(e, "get_housing_indicators")

    async def get_interest_rates(self) -> IntegrationResponse:
        """Get key interest rate data"""
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="FRED integration not available"
            )

        try:
            series_ids = {
                "federal_funds_rate": "DFF",
                "10_year_treasury": "DGS10",
                "30_year_mortgage": "MORTGAGE30US",
                "prime_rate": "DPRIME",
            }

            results = {}
            async with httpx.AsyncClient() as client:
                for rate_name, series_id in series_ids.items():
                    try:
                        response = await client.get(
                            f"{self.BASE_URL}/series/observations",
                            params={
                                "series_id": series_id,
                                "api_key": self.config.api_key,
                                "file_type": "json",
                                "limit": 30,
                                "sort_order": "desc"
                            },
                            timeout=10.0
                        )
                        response.raise_for_status()

                        data = response.json()
                        if "observations" in data:
                            results[rate_name] = {
                                "series_id": series_id,
                                "current": data["observations"][0] if data["observations"] else None,
                                "historical": data["observations"]
                            }
                    except Exception as e:
                        self.logger.warning(f"Failed to fetch {rate_name}: {e}")
                        results[rate_name] = {"error": str(e)}

            return self._success_response({
                "interest_rates": results
            })

        except Exception as e:
            return self._handle_error(e, "get_interest_rates")

    async def search_series(self, search_text: str, limit: int = 10) -> IntegrationResponse:
        """
        Search for FRED series

        Args:
            search_text: Search query
            limit: Number of results to return
        """
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="FRED integration not available"
            )

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.BASE_URL}/series/search",
                    params={
                        "search_text": search_text,
                        "api_key": self.config.api_key,
                        "file_type": "json",
                        "limit": limit
                    },
                    timeout=10.0
                )
                response.raise_for_status()

                data = response.json()

                if "seriess" in data:
                    return self._success_response({
                        "search_query": search_text,
                        "results": data["seriess"],
                        "count": len(data["seriess"])
                    })
                else:
                    return self._success_response({
                        "search_query": search_text,
                        "results": [],
                        "count": 0
                    })

        except Exception as e:
            return self._handle_error(e, "search_series")
