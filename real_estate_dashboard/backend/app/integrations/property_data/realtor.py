"""
Realtor.com RapidAPI Integration
Provides property listings and market data

Note: Uses RapidAPI (freemium model - limited free tier available)
Documentation: https://rapidapi.com/apidojo/api/realtor/
"""

from typing import Dict, Any, Optional
import httpx
from ..base import BaseIntegration, IntegrationConfig, IntegrationMetadata, IntegrationResponse


class RealtorIntegration(BaseIntegration):
    """
    Integration with Realtor.com API via RapidAPI
    Provides property listings, sold properties, and market data

    Note: Free tier: 500 requests/month
    """

    BASE_URL = "https://realtor.p.rapidapi.com"

    def __init__(self, config: IntegrationConfig):
        config.is_free = True  # Limited free tier
        config.requires_api_key = True  # RapidAPI key
        super().__init__(config)

    def get_metadata(self) -> IntegrationMetadata:
        return IntegrationMetadata(
            name="Realtor.com (via RapidAPI)",
            category="property_data",
            description="Property listings, sold data, and market insights from Realtor.com",
            is_free=True,
            requires_api_key=True,
            documentation_url="https://rapidapi.com/apidojo/api/realtor/",
            features=[
                "Active property listings",
                "Recently sold properties",
                "Property details",
                "Market trends by location",
                "Agent information",
                "School data"
            ]
        )

    async def test_connection(self) -> IntegrationResponse:
        """Test Realtor API connection"""
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="Realtor.com integration not configured. Requires RapidAPI key."
            )

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.BASE_URL}/locations/v2/auto-complete",
                    params={"input": "New York"},
                    headers={
                        "X-RapidAPI-Key": self.config.api_key,
                        "X-RapidAPI-Host": "realtor.p.rapidapi.com"
                    },
                    timeout=10.0
                )
                response.raise_for_status()

                return self._success_response({
                    "message": "Successfully connected to Realtor.com API",
                    "status": "connected"
                })

        except Exception as e:
            return self._handle_error(e, "Realtor.com connection test")

    async def search_properties(
        self,
        city: Optional[str] = None,
        state_code: Optional[str] = None,
        postal_code: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
        status: str = "for_sale"
    ) -> IntegrationResponse:
        """
        Search for properties

        Args:
            city: City name
            state_code: 2-letter state code
            postal_code: ZIP code
            limit: Number of results
            offset: Pagination offset
            status: "for_sale", "for_rent", or "sold"
        """
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="Realtor.com integration not configured"
            )

        try:
            params = {
                "limit": limit,
                "offset": offset,
                "status": status
            }

            if postal_code:
                params["postal_code"] = postal_code
            elif city and state_code:
                params["city"] = city
                params["state_code"] = state_code
            else:
                return IntegrationResponse(
                    success=False,
                    error="Must provide either postal_code or city+state_code"
                )

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.BASE_URL}/properties/v3/list",
                    params=params,
                    headers={
                        "X-RapidAPI-Key": self.config.api_key,
                        "X-RapidAPI-Host": "realtor.p.rapidapi.com"
                    },
                    timeout=30.0
                )
                response.raise_for_status()

                data = response.json()

                return self._success_response({
                    "properties": data.get("data", {}).get("home_search", {}).get("results", []),
                    "total": data.get("data", {}).get("home_search", {}).get("total", 0)
                })

        except Exception as e:
            return self._handle_error(e, "search_properties")

    async def get_property_details(self, property_id: str) -> IntegrationResponse:
        """
        Get detailed property information

        Args:
            property_id: Realtor.com property ID
        """
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="Realtor.com integration not configured"
            )

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.BASE_URL}/properties/v3/detail",
                    params={"property_id": property_id},
                    headers={
                        "X-RapidAPI-Key": self.config.api_key,
                        "X-RapidAPI-Host": "realtor.p.rapidapi.com"
                    },
                    timeout=10.0
                )
                response.raise_for_status()

                data = response.json()

                return self._success_response({
                    "property_details": data.get("data", {})
                })

        except Exception as e:
            return self._handle_error(e, "get_property_details")

    async def get_sold_properties(
        self,
        postal_code: str,
        limit: int = 20,
        offset: int = 0
    ) -> IntegrationResponse:
        """
        Get recently sold properties (comps)

        Args:
            postal_code: ZIP code
            limit: Number of results
            offset: Pagination offset
        """
        return await self.search_properties(
            postal_code=postal_code,
            limit=limit,
            offset=offset,
            status="sold"
        )
