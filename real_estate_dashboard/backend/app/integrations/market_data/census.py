"""
U.S. Census Bureau Integration - FREE
Provides demographic and housing data
"""

from typing import Dict, Any, Optional, List
import httpx
from ..base import BaseIntegration, IntegrationConfig, IntegrationMetadata, IntegrationResponse


class CensusBureauIntegration(BaseIntegration):
    """
    Integration with U.S. Census Bureau API
    FREE - No API key required for basic usage
    Documentation: https://www.census.gov/data/developers/data-sets.html
    """

    BASE_URL = "https://api.census.gov/data"

    def __init__(self, config: IntegrationConfig):
        # Census API is free but API key increases rate limits
        config.is_free = True
        config.requires_api_key = False  # Optional, but recommended
        super().__init__(config)

    def get_metadata(self) -> IntegrationMetadata:
        return IntegrationMetadata(
            name="U.S. Census Bureau",
            category="market_data",
            description="Access demographic, housing, and economic data from U.S. Census Bureau",
            is_free=True,
            requires_api_key=False,
            documentation_url="https://www.census.gov/data/developers.html",
            features=[
                "Population demographics by location",
                "Housing statistics",
                "Income and poverty data",
                "Business and economic data",
                "Geographic data (ZIP codes, counties, etc.)"
            ]
        )

    async def test_connection(self) -> IntegrationResponse:
        """Test Census API connection"""
        try:
            async with httpx.AsyncClient() as client:
                # Test with a simple population query for the US
                params = {
                    "get": "NAME,POP",
                    "for": "state:*"
                }
                if self.config.api_key:
                    params["key"] = self.config.api_key

                response = await client.get(
                    f"{self.BASE_URL}/2021/pep/population",
                    params=params,
                    timeout=10.0
                )
                response.raise_for_status()

                return self._success_response({
                    "message": "Successfully connected to Census Bureau API",
                    "sample_data": response.json()[:3]  # Return first 3 rows
                })
        except Exception as e:
            return self._handle_error(e, "Census Bureau connection test")

    async def get_demographics(
        self,
        geography: str = "zip code tabulation area",
        geo_ids: Optional[List[str]] = None,
        variables: Optional[List[str]] = None
    ) -> IntegrationResponse:
        """
        Get demographic data for specific geography

        Args:
            geography: Geographic level (e.g., "zip code tabulation area", "county", "state")
            geo_ids: List of geographic IDs (e.g., ZIP codes, county FIPS codes)
            variables: List of variable codes to retrieve
        """
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="Census Bureau integration not available"
            )

        try:
            # Default variables for real estate analysis
            if variables is None:
                variables = [
                    "NAME",  # Geographic name
                    "B01003_001E",  # Total population
                    "B19013_001E",  # Median household income
                    "B25077_001E",  # Median home value
                    "B25064_001E",  # Median gross rent
                ]

            async with httpx.AsyncClient() as client:
                params = {
                    "get": ",".join(variables),
                }

                # Build geography parameter
                if geo_ids:
                    params["for"] = f"{geography}:{','.join(geo_ids)}"
                else:
                    params["for"] = f"{geography}:*"

                if self.config.api_key:
                    params["key"] = self.config.api_key

                response = await client.get(
                    f"{self.BASE_URL}/2021/acs/acs5",  # American Community Survey 5-year
                    params=params,
                    timeout=30.0
                )
                response.raise_for_status()

                data = response.json()
                headers = data[0]
                rows = data[1:]

                # Convert to dict format
                formatted_data = [
                    dict(zip(headers, row)) for row in rows
                ]

                return self._success_response({
                    "demographics": formatted_data,
                    "total_count": len(formatted_data)
                })

        except Exception as e:
            return self._handle_error(e, "get_demographics")

    async def get_housing_stats(self, zip_code: str) -> IntegrationResponse:
        """Get housing statistics for a ZIP code"""
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="Census Bureau integration not available"
            )

        try:
            variables = [
                "NAME",
                "B25001_001E",  # Total housing units
                "B25002_002E",  # Occupied housing units
                "B25002_003E",  # Vacant housing units
                "B25003_002E",  # Owner-occupied units
                "B25003_003E",  # Renter-occupied units
                "B25077_001E",  # Median home value
                "B25064_001E",  # Median gross rent
            ]

            async with httpx.AsyncClient() as client:
                params = {
                    "get": ",".join(variables),
                    "for": f"zip code tabulation area:{zip_code}",
                }

                if self.config.api_key:
                    params["key"] = self.config.api_key

                response = await client.get(
                    f"{self.BASE_URL}/2021/acs/acs5",
                    params=params,
                    timeout=10.0
                )
                response.raise_for_status()

                data = response.json()
                if len(data) > 1:
                    headers = data[0]
                    values = data[1]
                    result = dict(zip(headers, values))

                    return self._success_response({
                        "zip_code": zip_code,
                        "housing_stats": result
                    })
                else:
                    return self._success_response({
                        "zip_code": zip_code,
                        "housing_stats": None,
                        "message": "No data found for this ZIP code"
                    })

        except Exception as e:
            return self._handle_error(e, "get_housing_stats")
