"""
Israeli Data.gov Integration - FREE
Access to Israeli government open data

Based on CKAN API used by data.gov.il
Documentation: https://data.gov.il
"""

from typing import Dict, Any, Optional, List
import httpx
from ..base import BaseIntegration, IntegrationConfig, IntegrationMetadata, IntegrationResponse


class DataGovILIntegration(BaseIntegration):
    """
    Integration with Israeli Data.gov CKAN API
    FREE - No API key required

    Provides access to Israeli government datasets
    """

    BASE_URL = "https://data.gov.il/api/3/action"

    def __init__(self, config: IntegrationConfig):
        config.is_free = True
        config.requires_api_key = False
        super().__init__(config)

    def get_metadata(self) -> IntegrationMetadata:
        return IntegrationMetadata(
            name="Data.gov.il (Israel)",
            category="official_data",
            description="Israeli government open data portal",
            is_free=True,
            requires_api_key=False,
            documentation_url="https://data.gov.il",
            features=[
                "Search Israeli government datasets",
                "Property and land registry data",
                "Economic indicators",
                "Municipal data",
                "Infrastructure information",
                "Real estate permits and approvals",
                "Hebrew and English data"
            ]
        )

    async def test_connection(self) -> IntegrationResponse:
        """Test Israeli Data.gov API connection"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.BASE_URL}/package_list",
                    params={"limit": 5},
                    timeout=10.0
                )
                response.raise_for_status()
                data = response.json()

                if data.get("success"):
                    return self._success_response({
                        "message": "Successfully connected to Data.gov.il API",
                        "sample_datasets": data.get("result", [])[:5]
                    })
                else:
                    return IntegrationResponse(
                        success=False,
                        error="Data.gov.il API returned unsuccessful response"
                    )

        except Exception as e:
            return self._handle_error(e, "Data.gov.il connection test")

    async def search_datasets(
        self,
        query: str,
        limit: int = 20,
        offset: int = 0
    ) -> IntegrationResponse:
        """
        Search for datasets on Data.gov.il

        Args:
            query: Search query (supports Hebrew and English)
            limit: Number of results
            offset: Pagination offset
        """
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="Data.gov.il integration not available"
            )

        try:
            params = {
                "q": query,
                "rows": min(limit, 1000),
                "start": offset
            }

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.BASE_URL}/package_search",
                    params=params,
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()

                if data.get("success"):
                    result = data.get("result", {})
                    return self._success_response({
                        "datasets": result.get("results", []),
                        "total_count": result.get("count", 0),
                        "query": query
                    })
                else:
                    return IntegrationResponse(
                        success=False,
                        error=data.get("error", {}).get("message", "Unknown error")
                    )

        except Exception as e:
            return self._handle_error(e, "search_datasets")

    async def get_dataset(self, dataset_id: str) -> IntegrationResponse:
        """Get detailed information about a specific dataset"""
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="Data.gov.il integration not available"
            )

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.BASE_URL}/package_show",
                    params={"id": dataset_id},
                    timeout=10.0
                )
                response.raise_for_status()
                data = response.json()

                if data.get("success"):
                    return self._success_response({
                        "dataset": data.get("result", {})
                    })
                else:
                    return IntegrationResponse(
                        success=False,
                        error=data.get("error", {}).get("message", "Dataset not found")
                    )

        except Exception as e:
            return self._handle_error(e, "get_dataset")

    async def get_real_estate_datasets(self, limit: int = 50) -> IntegrationResponse:
        """Get datasets related to real estate and property"""
        # Search in both Hebrew and English
        return await self.search_datasets(
            query="נדל״ן OR real estate OR property OR מקרקעין",
            limit=limit
        )

    async def list_tags(self) -> IntegrationResponse:
        """List all available tags"""
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="Data.gov.il integration not available"
            )

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.BASE_URL}/tag_list",
                    timeout=10.0
                )
                response.raise_for_status()
                data = response.json()

                if data.get("success"):
                    return self._success_response({
                        "tags": data.get("result", [])
                    })
                else:
                    return IntegrationResponse(
                        success=False,
                        error="Failed to fetch tags"
                    )

        except Exception as e:
            return self._handle_error(e, "list_tags")

    async def list_licenses(self) -> IntegrationResponse:
        """List all available data licenses"""
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="Data.gov.il integration not available"
            )

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.BASE_URL}/license_list",
                    timeout=10.0
                )
                response.raise_for_status()
                data = response.json()

                if data.get("success"):
                    return self._success_response({
                        "licenses": data.get("result", [])
                    })
                else:
                    return IntegrationResponse(
                        success=False,
                        error="Failed to fetch licenses"
                    )

        except Exception as e:
            return self._handle_error(e, "list_licenses")
