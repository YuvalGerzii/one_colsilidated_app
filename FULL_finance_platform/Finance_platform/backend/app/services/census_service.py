"""
Census API Integration Service

Provides demographics, population growth, and economic data.
"""

import os
from typing import Dict, Optional
from datetime import datetime
import httpx


class CensusService:
    """
    U.S. Census Bureau API Integration

    Fetches demographic and economic data including:
    - Population and growth trends
    - Median income
    - Employment rates
    - Education levels
    - Age distribution
    """

    def __init__(self):
        self.api_key = os.getenv("CENSUS_API_KEY", "")
        self.base_url = "https://api.census.gov/data"
        self.timeout = 30.0

    async def get_demographic_data(
        self,
        city: str,
        state: str,
        zip_code: Optional[str] = None
    ) -> Dict:
        """
        Fetch demographic data from Census API.

        Args:
            city: City name
            state: State abbreviation
            zip_code: ZIP code (optional, for more specific data)

        Returns:
            Dictionary containing demographic data
        """
        # NOTE: This is a mock implementation. Replace with actual Census API calls.
        # Census API is free and doesn't require authentication for basic data.
        # API documentation: https://www.census.gov/data/developers/data-sets.html

        if not self.api_key:
            return self._get_mock_data(city, state, zip_code)

        try:
            # Example: American Community Survey 5-Year Data
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/2021/acs/acs5",
                    params={
                        "get": "NAME,B01003_001E,B19013_001E,B23025_005E",  # Population, Median Income, Employed
                        "for": f"place:{city}",
                        "in": f"state:{state}",
                        "key": self.api_key,
                    }
                )
                response.raise_for_status()
                return self._parse_census_response(response.json())
        except Exception as e:
            print(f"Census API error: {str(e)}")
            return self._get_mock_data(city, state, zip_code)

    def _parse_census_response(self, data: list) -> Dict:
        """Parse Census API response into a structured format."""
        if len(data) < 2:
            return {}

        headers = data[0]
        values = data[1]

        return {
            "population": int(values[headers.index("B01003_001E")]) if "B01003_001E" in headers else None,
            "median_income": float(values[headers.index("B19013_001E")]) if "B19013_001E" in headers else None,
            "employed": int(values[headers.index("B23025_005E")]) if "B23025_005E" in headers else None,
        }

    def _get_mock_data(self, city: str, state: str, zip_code: Optional[str]) -> Dict:
        """Generate mock Census data for development/testing."""
        import random

        # Population based on city (rough estimates)
        city_pop_ranges = {
            "small": (10000, 50000),
            "medium": (50000, 200000),
            "large": (200000, 1000000),
            "metro": (1000000, 5000000),
        }

        # Random city size
        city_size = random.choice(list(city_pop_ranges.keys()))
        pop_range = city_pop_ranges[city_size]
        population = random.randint(*pop_range)

        return {
            "population": population,
            "median_income": random.randint(35000, 120000),
            "population_growth": round(random.uniform(-2.0, 15.0), 2),  # 5-year growth %
            "employment_rate": round(random.uniform(88.0, 97.0), 1),
            "age_median": round(random.uniform(28.0, 45.0), 1),
            "education_bachelor_plus": round(random.uniform(20.0, 60.0), 1),  # % with bachelor's or higher
            "demographics": {
                "white": round(random.uniform(40.0, 80.0), 1),
                "black": round(random.uniform(5.0, 30.0), 1),
                "hispanic": round(random.uniform(5.0, 40.0), 1),
                "asian": round(random.uniform(2.0, 20.0), 1),
                "other": round(random.uniform(2.0, 10.0), 1),
            },
            "housing": {
                "median_home_value": random.randint(150000, 800000),
                "median_rent": random.randint(800, 3000),
                "homeownership_rate": round(random.uniform(45.0, 75.0), 1),
            },
            "economic": {
                "unemployment_rate": round(random.uniform(3.0, 8.0), 1),
                "poverty_rate": round(random.uniform(8.0, 25.0), 1),
                "median_household_income": random.randint(35000, 120000),
            },
            "source": "U.S. Census Bureau (Mock Data)",
            "timestamp": datetime.utcnow().isoformat(),
        }

    async def get_population_trends(
        self,
        city: str,
        state: str
    ) -> Dict:
        """
        Fetch population growth trends.

        Args:
            city: City name
            state: State abbreviation

        Returns:
            Population trend data
        """
        data = await self.get_demographic_data(city, state)
        return {
            "current_population": data.get("population"),
            "population_growth_5yr": data.get("population_growth"),
            "median_age": data.get("age_median"),
        }

    async def get_economic_indicators(
        self,
        city: str,
        state: str
    ) -> Dict:
        """
        Fetch economic indicators.

        Args:
            city: City name
            state: State abbreviation

        Returns:
            Economic indicator data
        """
        data = await self.get_demographic_data(city, state)
        return {
            "median_income": data.get("median_income"),
            "employment_rate": data.get("employment_rate"),
            "economic_data": data.get("economic", {}),
            "housing_data": data.get("housing", {}),
        }
