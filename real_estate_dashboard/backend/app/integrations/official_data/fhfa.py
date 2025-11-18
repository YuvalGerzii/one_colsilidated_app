"""
FHFA (Federal Housing Finance Agency) Integration - FREE
Access to US housing price index and mortgage data

Documentation: https://www.fhfa.gov/DataTools/Downloads
CSV Download: https://www.fhfa.gov/hpi/download/monthly/hpi_master.csv
"""

from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import httpx
import csv
import io
from sqlalchemy.orm import Session
from ..base import BaseIntegration, IntegrationConfig, IntegrationMetadata, IntegrationResponse
from ..cache_utils import FHFADataCache, DataUpdateLogger
from ..retry_utils import retry_async, STANDARD_RETRY


class FHFAIntegration(BaseIntegration):
    """
    Integration with FHFA (Federal Housing Finance Agency)
    FREE - No API key required

    Provides access to House Price Index (HPI) and mortgage market data
    Downloads and parses CSV data directly from FHFA
    """

    BASE_URL = "https://www.fhfa.gov"
    HPI_CSV_URL = "https://www.fhfa.gov/hpi/download/monthly/hpi_master.csv"
    HPI_DATA_URL = f"{BASE_URL}/data/hpi"

    def __init__(self, config: IntegrationConfig):
        config.is_free = True
        config.requires_api_key = False
        super().__init__(config)

    def get_metadata(self) -> IntegrationMetadata:
        return IntegrationMetadata(
            name="FHFA (Federal Housing Finance Agency)",
            category="official_data",
            description="US house price index and mortgage finance data - CSV downloads with real-time parsing",
            is_free=True,
            requires_api_key=False,
            documentation_url="https://www.fhfa.gov/data/hpi",
            features=[
                "House Price Index (HPI) - national, state, metro, ZIP",
                "Purchase-Only HPI",
                "All-Transactions HPI",
                "Distress-Free HPI",
                "Historical price trends from 1991",
                "Monthly updates",
                "Real-time CSV parsing",
                "Seasonally adjusted and non-seasonally adjusted data"
            ]
        )

    async def test_connection(self) -> IntegrationResponse:
        """Test FHFA CSV download"""
        try:
            async def _fetch_test_data():
                async with httpx.AsyncClient(follow_redirects=True) as client:
                    # Test by downloading first few lines of CSV
                    response = await client.get(
                        self.HPI_CSV_URL,
                        timeout=15.0,
                        headers={
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                        }
                    )
                    response.raise_for_status()
                    return response.text

            # Use retry logic for network resilience
            csv_text = await retry_async(
                _fetch_test_data,
                config=STANDARD_RETRY,
                operation_name="FHFA connection test"
            )

            # Parse first few lines to verify format
            lines = csv_text.split('\n')[:3]

            if len(lines) >= 2 and 'hpi_type' in lines[0]:
                return self._success_response({
                    "message": "Successfully connected to FHFA HPI data",
                    "status": "operational",
                    "csv_url": self.HPI_CSV_URL,
                    "sample_header": lines[0],
                    "data_available": True
                })
            else:
                return IntegrationResponse(
                    success=False,
                    error="CSV format unexpected"
                )

        except httpx.HTTPStatusError as e:
            return IntegrationResponse(
                success=False,
                error=f"FHFA returned status {e.response.status_code}"
            )
        except Exception as e:
            return self._handle_error(e, "FHFA connection test")

    async def download_hpi_data(
        self,
        geography_type: Optional[str] = None,
        place_name: Optional[str] = None,
        limit: int = 100
    ) -> IntegrationResponse:
        """
        Download and parse FHFA House Price Index CSV data

        Args:
            geography_type: Filter by level (USA, State, CBSA, ZIP5, etc.)
            place_name: Filter by place name (e.g., "California", "Los Angeles")
            limit: Maximum number of records to return
        """
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="FHFA integration not available"
            )

        try:
            async def _fetch_csv_data():
                async with httpx.AsyncClient(follow_redirects=True) as client:
                    response = await client.get(
                        self.HPI_CSV_URL,
                        timeout=60.0,  # CSV file is large
                        headers={
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                        }
                    )
                    response.raise_for_status()
                    return response.text

            # Use retry logic for network resilience
            csv_text = await retry_async(
                _fetch_csv_data,
                config=STANDARD_RETRY,
                operation_name="FHFA HPI CSV download"
            )

            # Parse CSV
            csv_file = io.StringIO(csv_text)
            reader = csv.DictReader(csv_file)

            # Filter and collect data
            data = []
            for row in reader:
                # Apply filters
                if geography_type and row.get('level') != geography_type:
                    continue
                if place_name and place_name.lower() not in row.get('place_name', '').lower():
                    continue

                data.append({
                    'hpi_type': row.get('hpi_type'),
                    'hpi_flavor': row.get('hpi_flavor'),
                    'frequency': row.get('frequency'),
                    'level': row.get('level'),
                    'place_name': row.get('place_name'),
                    'place_id': row.get('place_id'),
                    'year': row.get('yr'),
                    'period': row.get('period'),
                    'index_nsa': row.get('index_nsa'),
                    'index_sa': row.get('index_sa')
                })

                if len(data) >= limit:
                    break

            return self._success_response({
                    "data": data,
                    "count": len(data),
                    "filters": {
                        "geography_type": geography_type,
                        "place_name": place_name
                    },
                    "source": "FHFA HPI Master CSV",
                    "download_url": self.HPI_CSV_URL
                })

        except httpx.HTTPStatusError as e:
            return IntegrationResponse(
                success=False,
                error=f"Failed to download HPI data: HTTP {e.response.status_code}"
            )
        except Exception as e:
            return self._handle_error(e, "download_hpi_data")

    async def get_house_price_index(
        self,
        geography_type: str = "USA",
        place_name: Optional[str] = None,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None,
        db: Optional[Session] = None,
        use_cache: bool = True
    ) -> IntegrationResponse:
        """
        Get House Price Index (HPI) data for specific geography

        With caching: Checks database cache first, downloads if stale

        Args:
            geography_type: "USA", "State", "CBSA", "ZIP5"
            place_name: Name of place (e.g., "California", "Los Angeles-Long Beach-Anaheim, CA")
            start_year: Start year (default: last 5 years)
            end_year: End year (default: current year)
            db: Database session for caching
            use_cache: Whether to use database cache
        """
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="FHFA integration not available"
            )

        try:
            # Set default date range
            if not end_year:
                end_year = datetime.now().year
            if not start_year:
                start_year = end_year - 5

            # Try cache first if enabled
            if db and use_cache:
                cache_stale = FHFADataCache.is_cache_stale(db, max_age_days=30)

                if not cache_stale:
                    # Get from cache
                    cached_records = FHFADataCache.get_hpi_data(
                        db,
                        geography_type=geography_type,
                        place_name=place_name,
                        start_year=start_year,
                        end_year=end_year,
                        limit=1000
                    )

                    if cached_records:
                        # Convert ORM objects to dict
                        data = [{
                            'hpi_type': r.index_type,
                            'level': r.geography_type,
                            'place_name': r.geography_name,
                            'place_id': r.geography_code,
                            'year': str(r.year),
                            'period': f"M{r.month:02d}" if r.month else f"Q{r.quarter}",
                            'index_sa': str(r.index_value),
                            'index_nsa': str(r.index_value)
                        } for r in cached_records]

                        return self._success_response({
                            "geography_type": geography_type,
                            "place_name": place_name,
                            "data": data,
                            "count": len(data),
                            "year_range": f"{start_year}-{end_year}",
                            "source": "FHFA HPI Database Cache",
                            "cached": True
                        })

            # Download fresh data
            result = await self.download_hpi_data(
                geography_type=geography_type,
                place_name=place_name,
                limit=1000
            )

            if not result.success:
                return result

            # Further filter by year
            filtered_data = [
                record for record in result.data.get('data', [])
                if start_year <= int(record.get('year', 0)) <= end_year
            ]

            # Save to cache if db available
            if db and filtered_data:
                await FHFADataCache.save_hpi_data(db, filtered_data)

            return self._success_response({
                "geography_type": geography_type,
                "place_name": place_name,
                "data": filtered_data,
                "count": len(filtered_data),
                "year_range": f"{start_year}-{end_year}",
                "source": "FHFA HPI Master CSV",
                "cached": False
            })

        except Exception as e:
            return self._handle_error(e, "get_house_price_index")

    async def get_state_hpi(
        self,
        state_name: str,
        start_year: Optional[int] = None,
        db: Optional[Session] = None
    ) -> IntegrationResponse:
        """
        Get House Price Index for a specific state

        Args:
            state_name: State name (e.g., "California", "New York", "Texas")
            start_year: Start year (default: last 5 years)
            db: Database session for caching
        """
        return await self.get_house_price_index(
            geography_type="State",
            place_name=state_name,
            start_year=start_year,
            db=db
        )

    async def get_metro_hpi(
        self,
        metro_name: str,
        start_year: Optional[int] = None,
        db: Optional[Session] = None
    ) -> IntegrationResponse:
        """
        Get House Price Index for a metropolitan area

        Args:
            metro_name: Metro area name (e.g., "Los Angeles", "New York", "San Francisco")
            start_year: Start year (default: last 5 years)
            db: Database session for caching
        """
        return await self.get_house_price_index(
            geography_type="CBSA",
            place_name=metro_name,
            start_year=start_year,
            db=db
        )

    async def get_national_hpi(
        self,
        start_year: Optional[int] = None,
        db: Optional[Session] = None
    ) -> IntegrationResponse:
        """
        Get National House Price Index

        Args:
            start_year: Start year (default: last 5 years)
            db: Database session for caching
        """
        return await self.get_house_price_index(
            geography_type="USA",
            start_year=start_year,
            db=db
        )

    async def search_places(
        self,
        query: str,
        geography_type: Optional[str] = None
    ) -> IntegrationResponse:
        """
        Search for available places in HPI data

        Args:
            query: Search query (e.g., "Los Angeles", "California")
            geography_type: Filter by geography level
        """
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="FHFA integration not available"
            )

        try:
            # Download sample data to find matching places
            result = await self.download_hpi_data(
                geography_type=geography_type,
                place_name=query,
                limit=50
            )

            if not result.success:
                return result

            # Extract unique places
            places = {}
            for record in result.data.get('data', []):
                place_key = f"{record['place_name']}|{record['level']}"
                if place_key not in places:
                    places[place_key] = {
                        'place_name': record['place_name'],
                        'place_id': record['place_id'],
                        'level': record['level']
                    }

            places_list = list(places.values())

            return self._success_response({
                "query": query,
                "places": places_list,
                "count": len(places_list),
                "geography_filter": geography_type
            })

        except Exception as e:
            return self._handle_error(e, "search_places")

    async def get_latest_data(
        self,
        geography_type: str = "USA",
        limit: int = 10
    ) -> IntegrationResponse:
        """
        Get latest HPI data points

        Args:
            geography_type: Geography level to filter
            limit: Number of results
        """
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="FHFA integration not available"
            )

        try:
            # Download recent data
            current_year = datetime.now().year
            result = await self.get_house_price_index(
                geography_type=geography_type,
                start_year=current_year - 1,
                end_year=current_year
            )

            if not result.success:
                return result

            # Sort by year and period, take latest
            data = result.data.get('data', [])
            data_sorted = sorted(
                data,
                key=lambda x: (int(x.get('year', 0)), int(x.get('period', 0).replace('M', ''))),
                reverse=True
            )[:limit]

            return self._success_response({
                "latest_data": data_sorted,
                "count": len(data_sorted),
                "geography_type": geography_type
            })

        except Exception as e:
            return self._handle_error(e, "get_latest_data")

    async def get_download_info(self) -> IntegrationResponse:
        """Get information about available CSV downloads"""
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="FHFA integration not available"
            )

        try:
            return self._success_response({
                "message": "FHFA HPI Direct CSV Download",
                "csv_url": self.HPI_CSV_URL,
                "data_portal": self.HPI_DATA_URL,
                "geography_levels": [
                    "USA - National level",
                    "State - State level (50 states)",
                    "CBSA - Metropolitan areas (~400 metros)",
                    "ZIP5 - ZIP code level (where available)"
                ],
                "data_fields": [
                    "hpi_type - Type of index (traditional, etc.)",
                    "hpi_flavor - Purchase-only, All-transactions, Distress-free",
                    "frequency - Monthly, Quarterly, Annual",
                    "level - Geographic level",
                    "place_name - Name of geographic area",
                    "place_id - Unique identifier",
                    "yr - Year",
                    "period - Month/Quarter (M01-M12, Q1-Q4)",
                    "index_nsa - Not seasonally adjusted index",
                    "index_sa - Seasonally adjusted index"
                ],
                "update_frequency": "Monthly",
                "historical_coverage": "1991 to present",
                "note": "CSV file is ~20MB, contains complete historical data"
            })

        except Exception as e:
            return self._handle_error(e, "get_download_info")
