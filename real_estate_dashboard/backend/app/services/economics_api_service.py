"""
Economics API Service for Market Intelligence

Provides comprehensive macroeconomic data integration using the Sugra AI Economics API.
Includes GDP, employment, inflation, trade, and other economic indicators for countries worldwide.
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
import requests
from app.services.cache_service import CacheService
from app.settings import settings

logger = logging.getLogger(__name__)


class EconomicsAPIService:
    """Service for fetching macroeconomic data from Sugra AI Economics API"""

    # Default API base URL (from settings)
    DEFAULT_BASE_URL = settings.ECONOMICS_API_BASE_URL

    # Key countries for real estate market intelligence
    KEY_COUNTRIES = [
        "united-states",
        "israel",
        "united-kingdom",
        "canada",
        "australia",
        "germany",
        "france",
        "japan",
        "china",
    ]

    # Economic categories available from the API
    CATEGORIES = [
        "overview",      # Currency, stock market, GDP growth, unemployment, inflation
        "gdp",          # Growth rates, per capita, sectoral breakdowns
        "labour",       # Unemployment, payrolls, wages, job claims
        "prices",       # Inflation, CPI, producer prices, deflators
        "health",       # Healthcare costs, insurance, life expectancy
        "money",        # Interest rates, money supply, central bank metrics
        "trade",        # Balance of trade, exports/imports, FDI, reserves
        "government",   # Debt, budget, spending, tax rates
        "business",     # PMI, industrial production, inventories, confidence
        "consumer",     # Retail sales, confidence, spending, debt levels
        "housing",      # Starts, permits, prices, mortgage rates
    ]

    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.base_url = base_url or self.DEFAULT_BASE_URL
        self.api_key = api_key or settings.ECONOMICS_API_KEY
        self.cache = CacheService()
        self.cache_ttl = 3600  # 1 hour (economic data changes less frequently)
        self.timeout = 10  # 10 seconds timeout for API calls

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with API key"""
        headers = {}
        if self.api_key:
            headers['x-api-key'] = self.api_key
        return headers

    async def get_country_overview(
        self,
        country: str,
        related: Optional[str] = None,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Get economic overview for a country

        Args:
            country: Country name (e.g., "united-states", "israel")
            related: Optional filter for related indicators (e.g., "Inflation Rate")
            use_cache: Whether to use cached data

        Returns:
            Dict with country economic overview data
        """
        cache_key = f"economics:overview:{country}:{related or 'all'}"

        if use_cache:
            cached = await self.cache.get(cache_key)
            if cached:
                return cached

        try:
            url = f"{self.base_url}/v1/economics/{country}/overview"
            params = {"Related": related} if related else {}
            headers = self._get_headers()

            response = requests.get(url, params=params, headers=headers, timeout=self.timeout)
            response.raise_for_status()

            data = response.json()

            result = {
                "country": country,
                "category": "overview",
                "data": data,
                "timestamp": datetime.now().isoformat(),
                "data_source": "economics-api",
            }

            await self.cache.set(cache_key, result, ttl=self.cache_ttl)
            return result

        except requests.RequestException as e:
            logger.error(f"Error fetching country overview for {country}: {str(e)}")
            return {
                "country": country,
                "category": "overview",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "data_source": "economics-api",
            }

    async def get_economic_indicator(
        self,
        country: str,
        category: str,
        related: Optional[str] = None,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Get specific economic indicator data for a country

        Args:
            country: Country name
            category: Economic category (gdp, labour, prices, money, trade, etc.)
            related: Optional filter for related indicators
            use_cache: Whether to use cached data

        Returns:
            Dict with economic indicator data
        """
        if category not in self.CATEGORIES:
            return {
                "error": f"Invalid category. Must be one of: {', '.join(self.CATEGORIES)}",
                "timestamp": datetime.now().isoformat(),
            }

        cache_key = f"economics:{category}:{country}:{related or 'all'}"

        if use_cache:
            cached = await self.cache.get(cache_key)
            if cached:
                return cached

        try:
            url = f"{self.base_url}/v1/economics/{country}/{category}"
            params = {"Related": related} if related else {}
            headers = self._get_headers()

            response = requests.get(url, params=params, headers=headers, timeout=self.timeout)
            response.raise_for_status()

            data = response.json()

            result = {
                "country": country,
                "category": category,
                "data": data,
                "timestamp": datetime.now().isoformat(),
                "data_source": "economics-api",
            }

            await self.cache.set(cache_key, result, ttl=self.cache_ttl)
            return result

        except requests.RequestException as e:
            logger.error(f"Error fetching {category} data for {country}: {str(e)}")
            return {
                "country": country,
                "category": category,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "data_source": "economics-api",
            }

    async def get_gdp_data(
        self,
        country: str,
        related: Optional[str] = None,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """Get GDP data for a country"""
        return await self.get_economic_indicator(country, "gdp", related, use_cache)

    async def get_labour_data(
        self,
        country: str,
        related: Optional[str] = None,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """Get labour/employment data for a country"""
        return await self.get_economic_indicator(country, "labour", related, use_cache)

    async def get_inflation_data(
        self,
        country: str,
        related: Optional[str] = None,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """Get inflation and price data for a country"""
        return await self.get_economic_indicator(country, "prices", related, use_cache)

    async def get_housing_data(
        self,
        country: str,
        related: Optional[str] = None,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """Get housing market data for a country"""
        return await self.get_economic_indicator(country, "housing", related, use_cache)

    async def get_interest_rates(
        self,
        country: str,
        related: Optional[str] = None,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """Get interest rate and monetary data for a country"""
        return await self.get_economic_indicator(country, "money", related, use_cache)

    async def get_trade_data(
        self,
        country: str,
        related: Optional[str] = None,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """Get trade and balance of payments data for a country"""
        return await self.get_economic_indicator(country, "trade", related, use_cache)

    async def get_economic_calendar(
        self,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Get economic calendar with upcoming events

        Args:
            use_cache: Whether to use cached data

        Returns:
            Dict with economic calendar data
        """
        cache_key = "economics:calendar"

        if use_cache:
            cached = await self.cache.get(cache_key)
            if cached:
                return cached

        try:
            url = f"{self.base_url}/v1/economic-calendar"
            headers = self._get_headers()

            response = requests.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()

            data = response.json()

            result = {
                "calendar": data,
                "timestamp": datetime.now().isoformat(),
                "data_source": "economics-api",
            }

            await self.cache.set(cache_key, result, ttl=1800)  # 30 minutes cache
            return result

        except requests.RequestException as e:
            logger.error(f"Error fetching economic calendar: {str(e)}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "data_source": "economics-api",
            }

    async def get_countries_overview(
        self,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Get overview data for all countries

        Args:
            use_cache: Whether to use cached data

        Returns:
            Dict with all countries overview data
        """
        cache_key = "economics:countries:all"

        if use_cache:
            cached = await self.cache.get(cache_key)
            if cached:
                return cached

        try:
            url = f"{self.base_url}/v1/economics/countries-overview"
            params = {"country": "null"}  # Required parameter to get all countries
            headers = self._get_headers()

            response = requests.get(url, params=params, headers=headers, timeout=self.timeout)
            response.raise_for_status()

            data = response.json()

            result = {
                "countries": data,
                "count": len(data) if isinstance(data, list) else None,
                "timestamp": datetime.now().isoformat(),
                "data_source": "economics-api",
            }

            await self.cache.set(cache_key, result, ttl=self.cache_ttl)
            return result

        except requests.RequestException as e:
            logger.error(f"Error fetching countries overview: {str(e)}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "data_source": "economics-api",
            }

    async def get_market_intelligence_summary(
        self,
        countries: Optional[List[str]] = None,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Get comprehensive economic summary for key countries

        Args:
            countries: List of countries to fetch data for (default: KEY_COUNTRIES)
            use_cache: Whether to use cached data

        Returns:
            Dict with comprehensive economic data for multiple countries
        """
        countries = countries or self.KEY_COUNTRIES
        cache_key = f"economics:summary:{':'.join(countries)}"

        if use_cache:
            cached = await self.cache.get(cache_key)
            if cached:
                return cached

        try:
            country_data = []

            for country in countries:
                # Fetch key indicators for each country
                overview = await self.get_country_overview(country, use_cache=use_cache)
                gdp = await self.get_gdp_data(country, use_cache=use_cache)
                labour = await self.get_labour_data(country, use_cache=use_cache)
                housing = await self.get_housing_data(country, use_cache=use_cache)

                country_summary = {
                    "country": country,
                    "overview": overview.get("data", {}),
                    "gdp": gdp.get("data", {}),
                    "labour": labour.get("data", {}),
                    "housing": housing.get("data", {}),
                    "has_errors": any([
                        "error" in overview,
                        "error" in gdp,
                        "error" in labour,
                        "error" in housing,
                    ]),
                }

                country_data.append(country_summary)

            result = {
                "countries": country_data,
                "count": len(country_data),
                "timestamp": datetime.now().isoformat(),
                "data_source": "economics-api",
            }

            await self.cache.set(cache_key, result, ttl=self.cache_ttl)
            return result

        except Exception as e:
            logger.error(f"Error fetching market intelligence summary: {str(e)}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "data_source": "economics-api",
            }

    async def get_us_housing_indicators(
        self,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Get US-specific housing market indicators

        Args:
            use_cache: Whether to use cached data

        Returns:
            Dict with US housing market indicators
        """
        return await self.get_housing_data("united-states", use_cache=use_cache)

    async def get_israel_housing_indicators(
        self,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Get Israel-specific housing market indicators

        Args:
            use_cache: Whether to use cached data

        Returns:
            Dict with Israel housing market indicators
        """
        return await self.get_housing_data("israel", use_cache=use_cache)

    async def compare_countries(
        self,
        countries: List[str],
        indicators: Optional[List[str]] = None,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Compare economic indicators across multiple countries

        Args:
            countries: List of countries to compare
            indicators: List of indicators to compare (default: overview, gdp, labour, housing)
            use_cache: Whether to use cached data

        Returns:
            Dict with comparison data
        """
        indicators = indicators or ["overview", "gdp", "labour", "housing"]
        cache_key = f"economics:compare:{':'.join(countries)}:{':'.join(indicators)}"

        if use_cache:
            cached = await self.cache.get(cache_key)
            if cached:
                return cached

        try:
            comparison_data = {}

            for country in countries:
                country_indicators = {}

                for indicator in indicators:
                    if indicator == "overview":
                        data = await self.get_country_overview(country, use_cache=use_cache)
                    else:
                        data = await self.get_economic_indicator(country, indicator, use_cache=use_cache)

                    country_indicators[indicator] = data.get("data", {})

                comparison_data[country] = country_indicators

            result = {
                "comparison": comparison_data,
                "countries": countries,
                "indicators": indicators,
                "timestamp": datetime.now().isoformat(),
                "data_source": "economics-api",
            }

            await self.cache.set(cache_key, result, ttl=self.cache_ttl)
            return result

        except Exception as e:
            logger.error(f"Error comparing countries: {str(e)}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "data_source": "economics-api",
            }
