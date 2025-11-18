"""
Data.gov US Integration - FREE
Access to US government open data catalog

Based on CKAN API used by Data.gov
Documentation: https://catalog.data.gov/dataset
API Docs: https://www.data.gov/developers/apis
"""

from typing import Dict, Any, Optional, List
import httpx
from ..base import BaseIntegration, IntegrationConfig, IntegrationMetadata, IntegrationResponse


class DataGovUSIntegration(BaseIntegration):
    """
    Integration with US Data.gov CKAN API
    FREE - No API key required

    Provides access to 300,000+ datasets from federal, state, and local governments
    """

    BASE_URL = "https://catalog.data.gov/api/3/action"

    def __init__(self, config: IntegrationConfig):
        config.is_free = True
        config.requires_api_key = False
        super().__init__(config)

    def get_metadata(self) -> IntegrationMetadata:
        return IntegrationMetadata(
            name="Data.gov (US)",
            category="official_data",
            description="US government open data catalog with 300,000+ datasets",
            is_free=True,
            requires_api_key=False,
            documentation_url="https://www.data.gov/developers/apis",
            features=[
                "Search 300,000+ government datasets",
                "Federal real property data",
                "Housing and urban development data",
                "Economic indicators",
                "State and local government data",
                "Real estate and property records",
                "Downloadable datasets in multiple formats"
            ]
        )

    async def test_connection(self) -> IntegrationResponse:
        """Test Data.gov API connection"""
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
                        "message": "Successfully connected to Data.gov API",
                        "sample_datasets": data.get("result", [])[:5]
                    })
                else:
                    return IntegrationResponse(
                        success=False,
                        error="Data.gov API returned unsuccessful response"
                    )

        except Exception as e:
            return self._handle_error(e, "Data.gov connection test")

    async def search_datasets(
        self,
        query: str,
        tags: Optional[List[str]] = None,
        limit: int = 20,
        offset: int = 0
    ) -> IntegrationResponse:
        """
        Search for datasets on Data.gov

        Args:
            query: Search query (e.g., "real estate", "housing")
            tags: Filter by tags (e.g., ["real-estate", "housing"])
            limit: Number of results (max 1000)
            offset: Pagination offset
        """
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="Data.gov integration not available"
            )

        try:
            # Build search query
            fq_parts = []
            if tags:
                tag_filter = " OR ".join([f'tags:"{tag}"' for tag in tags])
                fq_parts.append(f"({tag_filter})")

            params = {
                "q": query,
                "rows": min(limit, 1000),
                "start": offset
            }

            if fq_parts:
                params["fq"] = " AND ".join(fq_parts)

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
                        "query": query,
                        "tags": tags
                    })
                else:
                    return IntegrationResponse(
                        success=False,
                        error=data.get("error", {}).get("message", "Unknown error")
                    )

        except Exception as e:
            return self._handle_error(e, "search_datasets")

    async def get_dataset(self, dataset_id: str) -> IntegrationResponse:
        """
        Get detailed information about a specific dataset

        Args:
            dataset_id: Dataset identifier or name
        """
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="Data.gov integration not available"
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
        """Get datasets related to real estate and housing"""
        return await self.search_datasets(
            query="real estate OR housing OR property",
            tags=["real-estate", "housing", "property"],
            limit=limit
        )

    async def get_federal_property_data(self) -> IntegrationResponse:
        """Get federal real property datasets"""
        return await self.search_datasets(
            query="federal real property",
            limit=20
        )

    async def list_organizations(self, limit: int = 100) -> IntegrationResponse:
        """List government organizations that publish data"""
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="Data.gov integration not available"
            )

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.BASE_URL}/organization_list",
                    params={"all_fields": True, "limit": limit},
                    timeout=10.0
                )
                response.raise_for_status()
                data = response.json()

                if data.get("success"):
                    return self._success_response({
                        "organizations": data.get("result", [])
                    })
                else:
                    return IntegrationResponse(
                        success=False,
                        error="Failed to fetch organizations"
                    )

        except Exception as e:
            return self._handle_error(e, "list_organizations")

    async def download_dataset_resource(
        self,
        resource_url: str
    ) -> IntegrationResponse:
        """
        Download a dataset resource file

        Note: This returns the URL for download. Actual file download should be
        handled separately to avoid memory issues with large files.

        Args:
            resource_url: URL of the resource to download
        """
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="Data.gov integration not available"
            )

        try:
            # Validate URL
            if not resource_url.startswith(('http://', 'https://')):
                return IntegrationResponse(
                    success=False,
                    error="Invalid resource URL"
                )

            return self._success_response({
                "download_url": resource_url,
                "message": "Use this URL to download the dataset resource",
                "note": "Large files should be downloaded in chunks"
            })

        except Exception as e:
            return self._handle_error(e, "download_dataset_resource")
