"""
ATTOM Data Solutions Integration
Provides comprehensive property data (Zillow alternative with API access)

Note: ATTOM offers a free trial, then requires paid subscription
Documentation: https://api.developer.attomdata.com/
"""

from typing import Dict, Any, Optional
import httpx
from ..base import BaseIntegration, IntegrationConfig, IntegrationMetadata, IntegrationResponse


class AttomDataIntegration(BaseIntegration):
    """
    Integration with ATTOM Data Solutions API
    Provides property data, AVMs, sales comps, and more

    Note: Free trial available, then paid plans starting at $49/month
    """

    BASE_URL = "https://api.gateway.attomdata.com/propertyapi/v1.0.0"

    def __init__(self, config: IntegrationConfig):
        config.is_free = False  # Free trial, then paid
        config.requires_api_key = True
        super().__init__(config)

    def get_metadata(self) -> IntegrationMetadata:
        return IntegrationMetadata(
            name="ATTOM Data Solutions",
            category="property_data",
            description="Comprehensive property data including AVMs, sales history, and detailed property characteristics",
            is_free=False,
            requires_api_key=True,
            documentation_url="https://api.developer.attomdata.com/",
            features=[
                "Property details and characteristics",
                "Automated Valuation Models (AVM)",
                "Sales history and comparables",
                "Property ownership information",
                "Tax assessor data",
                "Foreclosure and pre-foreclosure data",
                "School and neighborhood information"
            ]
        )

    async def test_connection(self) -> IntegrationResponse:
        """Test ATTOM API connection"""
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="ATTOM Data integration not configured. This is a paid service."
            )

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.BASE_URL}/property/basicprofile",
                    params={"address1": "123 Main St", "address2": "New York, NY"},
                    headers={"apikey": self.config.api_key},
                    timeout=10.0
                )
                response.raise_for_status()

                return self._success_response({
                    "message": "Successfully connected to ATTOM Data API",
                    "status": "connected"
                })

        except Exception as e:
            return self._handle_error(e, "ATTOM connection test")

    async def get_property_details(
        self,
        address: Optional[str] = None,
        apn: Optional[str] = None,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None
    ) -> IntegrationResponse:
        """
        Get detailed property information

        Args:
            address: Full street address
            apn: Assessor's Parcel Number
            latitude: Latitude coordinate
            longitude: Longitude coordinate
        """
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="ATTOM Data integration not configured"
            )

        try:
            params = {}

            if address:
                # Split address into components
                parts = address.split(",")
                if len(parts) >= 2:
                    params["address1"] = parts[0].strip()
                    params["address2"] = ",".join(parts[1:]).strip()
            elif apn:
                params["apn"] = apn
            elif latitude and longitude:
                params["latitude"] = str(latitude)
                params["longitude"] = str(longitude)
            else:
                return IntegrationResponse(
                    success=False,
                    error="Must provide either address, APN, or coordinates"
                )

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.BASE_URL}/property/expandedprofile",
                    params=params,
                    headers={"apikey": self.config.api_key},
                    timeout=30.0
                )
                response.raise_for_status()

                data = response.json()

                return self._success_response({
                    "property_details": data
                })

        except Exception as e:
            return self._handle_error(e, "get_property_details")

    async def get_avm(
        self,
        address: Optional[str] = None,
        apn: Optional[str] = None
    ) -> IntegrationResponse:
        """
        Get Automated Valuation Model (property value estimate)

        Args:
            address: Full street address
            apn: Assessor's Parcel Number
        """
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="ATTOM Data integration not configured"
            )

        try:
            params = {}

            if address:
                parts = address.split(",")
                if len(parts) >= 2:
                    params["address1"] = parts[0].strip()
                    params["address2"] = ",".join(parts[1:]).strip()
            elif apn:
                params["apn"] = apn
            else:
                return IntegrationResponse(
                    success=False,
                    error="Must provide either address or APN"
                )

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.BASE_URL}/property/avm",
                    params=params,
                    headers={"apikey": self.config.api_key},
                    timeout=10.0
                )
                response.raise_for_status()

                data = response.json()

                return self._success_response({
                    "avm_data": data
                })

        except Exception as e:
            return self._handle_error(e, "get_avm")

    async def get_sales_comps(
        self,
        address: Optional[str] = None,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        radius: float = 1.0
    ) -> IntegrationResponse:
        """
        Get comparable sales (comps)

        Args:
            address: Full street address
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            radius: Search radius in miles
        """
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="ATTOM Data integration not configured"
            )

        try:
            params = {"radius": str(radius)}

            if address:
                parts = address.split(",")
                if len(parts) >= 2:
                    params["address1"] = parts[0].strip()
                    params["address2"] = ",".join(parts[1:]).strip()
            elif latitude and longitude:
                params["latitude"] = str(latitude)
                params["longitude"] = str(longitude)
            else:
                return IntegrationResponse(
                    success=False,
                    error="Must provide either address or coordinates"
                )

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.BASE_URL}/salescomparable/detail",
                    params=params,
                    headers={"apikey": self.config.api_key},
                    timeout=30.0
                )
                response.raise_for_status()

                data = response.json()

                return self._success_response({
                    "comparable_sales": data
                })

        except Exception as e:
            return self._handle_error(e, "get_sales_comps")
