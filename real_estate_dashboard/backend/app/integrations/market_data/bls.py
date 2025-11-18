"""
Bureau of Labor Statistics (BLS) Integration - FREE
Provides employment and economic data
"""

from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import httpx
from ..base import BaseIntegration, IntegrationConfig, IntegrationMetadata, IntegrationResponse


class BLSIntegration(BaseIntegration):
    """
    Integration with Bureau of Labor Statistics API
    FREE - API key optional but recommended (increases daily limits from 25 to 500 queries)
    Documentation: https://www.bls.gov/developers/
    """

    BASE_URL = "https://api.bls.gov/publicAPI/v2"

    def __init__(self, config: IntegrationConfig):
        config.is_free = True
        config.requires_api_key = False  # Optional
        super().__init__(config)

    def get_metadata(self) -> IntegrationMetadata:
        return IntegrationMetadata(
            name="Bureau of Labor Statistics",
            category="market_data",
            description="Access employment, unemployment, and economic indicators",
            is_free=True,
            requires_api_key=False,
            documentation_url="https://www.bls.gov/developers/",
            features=[
                "Unemployment rates by area",
                "Employment statistics",
                "Consumer Price Index (CPI)",
                "Producer Price Index (PPI)",
                "Average hourly earnings",
                "Job growth metrics"
            ]
        )

    async def test_connection(self) -> IntegrationResponse:
        """Test BLS API connection"""
        try:
            # Test with national unemployment rate (Series ID: LNS14000000)
            result = await self.get_series_data(["LNS14000000"], limit=1)
            if result.success:
                return self._success_response({
                    "message": "Successfully connected to BLS API",
                    "sample_data": result.data
                })
            return result
        except Exception as e:
            return self._handle_error(e, "BLS connection test")

    async def get_series_data(
        self,
        series_ids: List[str],
        start_year: Optional[int] = None,
        end_year: Optional[int] = None,
        limit: Optional[int] = None
    ) -> IntegrationResponse:
        """
        Get time series data from BLS

        Args:
            series_ids: List of BLS series IDs
            start_year: Start year for data
            end_year: End year for data
            limit: Limit number of results
        """
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="BLS integration not available"
            )

        try:
            # Default to last 3 years if not specified
            if not end_year:
                end_year = datetime.now().year
            if not start_year:
                start_year = end_year - 3

            payload = {
                "seriesid": series_ids,
                "startyear": str(start_year),
                "endyear": str(end_year),
            }

            if self.config.api_key:
                payload["registrationkey"] = self.config.api_key

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.BASE_URL}/timeseries/data/",
                    json=payload,
                    timeout=30.0
                )
                response.raise_for_status()

                result = response.json()

                if result.get("status") == "REQUEST_SUCCEEDED":
                    series_data = result.get("Results", {}).get("series", [])

                    # Format the data
                    formatted_data = {}
                    for series in series_data:
                        series_id = series["seriesID"]
                        data_points = series.get("data", [])

                        if limit:
                            data_points = data_points[:limit]

                        formatted_data[series_id] = [
                            {
                                "year": point.get("year"),
                                "period": point.get("period"),
                                "period_name": point.get("periodName"),
                                "value": point.get("value"),
                                "footnotes": point.get("footnotes", [])
                            }
                            for point in data_points
                        ]

                    return self._success_response({
                        "series_data": formatted_data,
                        "message": result.get("message", [])
                    })
                else:
                    return IntegrationResponse(
                        success=False,
                        error=f"BLS API error: {result.get('message', ['Unknown error'])}"
                    )

        except Exception as e:
            return self._handle_error(e, "get_series_data")

    async def get_unemployment_rate(self, area_code: str = "0000000") -> IntegrationResponse:
        """
        Get unemployment rate for an area

        Args:
            area_code: BLS area code (default is national)
                      Format: LAUMT[ST][AREA]0000000000000003
                      National: 0000000
        """
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="BLS integration not available"
            )

        try:
            # Construct series ID for unemployment rate
            if area_code == "0000000":
                # National unemployment rate
                series_id = "LNS14000000"
            else:
                # Local area unemployment rate
                series_id = f"LAUMT{area_code}0000000003"

            result = await self.get_series_data([series_id], limit=12)  # Last 12 months

            return result

        except Exception as e:
            return self._handle_error(e, "get_unemployment_rate")

    async def get_cpi(self) -> IntegrationResponse:
        """Get Consumer Price Index (All Urban Consumers)"""
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="BLS integration not available"
            )

        try:
            # CPI-U: All items in U.S. city average
            series_id = "CUSR0000SA0"
            result = await self.get_series_data([series_id], limit=12)

            return result

        except Exception as e:
            return self._handle_error(e, "get_cpi")

    async def get_employment_stats(self, area_code: str = "0000000") -> IntegrationResponse:
        """
        Get employment statistics for an area

        Returns unemployment rate, employment level, and labor force data
        """
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="BLS integration not available"
            )

        try:
            if area_code == "0000000":
                # National series IDs
                series_ids = [
                    "LNS14000000",  # Unemployment rate
                    "LNS12000000",  # Employment level
                    "LNS11000000",  # Labor force
                ]
            else:
                series_ids = [
                    f"LAUMT{area_code}0000000003",  # Unemployment rate
                    f"LAUMT{area_code}0000000005",  # Employment
                    f"LAUMT{area_code}0000000006",  # Labor force
                ]

            result = await self.get_series_data(series_ids, limit=12)

            return result

        except Exception as e:
            return self._handle_error(e, "get_employment_stats")
