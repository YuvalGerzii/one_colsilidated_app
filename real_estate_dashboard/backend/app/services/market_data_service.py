"""
Market Intelligence Data Fetching Service

This service provides failsafe data fetching from multiple sources with:
- Automatic fallbacks to working integrations
- Error handling that never breaks the app
- Mock/cached data when all sources fail
- Retry logic with exponential backoff
- Enhanced caching with Redis support
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import asyncio

from app.integrations.manager import integration_manager
from app.services.cache_service import get_cache_service

logger = logging.getLogger(__name__)


class MarketDataService:
    """
    Failsafe market data service with automatic fallbacks and enhanced caching
    """

    def __init__(self):
        self.cache = get_cache_service()

    async def get_employment_data(self, area_code: str = "0000000") -> Dict[str, Any]:
        """
        Get employment statistics with failsafe fallback

        Attempts:
        1. BLS (Bureau of Labor Statistics)
        2. Cached data
        3. Mock data (as last resort)
        """
        cache_key = f"employment_{area_code}"

        # Check cache first
        cached_data = await self.cache.get(cache_key, namespace="market_data", cache_type="market_data")
        if cached_data:
            return cached_data

        # Try BLS integration
        bls = integration_manager.get("bls")
        if bls and bls.is_available:
            try:
                result = await bls.get_employment_stats(area_code)
                if result.success and result.data:
                    await self.cache.set(cache_key, result.data, namespace="market_data", cache_type="market_data")
                    return result.data
            except Exception as e:
                logger.warning(f"BLS integration failed: {e}")

        # Return mock data as fallback
        logger.info("Returning mock employment data (all sources unavailable)")
        mock_data = {
            "area_code": area_code,
            "unemployment_rate": 3.8,
            "labor_force": 163000000,
            "employed": 156940000,
            "unemployed": 6060000,
            "last_updated": datetime.utcnow().isoformat(),
            "source": "mock_data",
            "note": "Real data unavailable - using mock data"
        }
        return mock_data

    async def get_housing_indicators(self) -> Dict[str, Any]:
        """
        Get housing market indicators with fallback

        Attempts:
        1. FHFA (Federal Housing Finance Agency)
        2. HUD (Housing and Urban Development)
        3. Cached data
        4. Mock data
        """
        cache_key = "housing_indicators"

        # Check cache
        cached_data = await self.cache.get(cache_key, namespace="market_data", cache_type="real_estate_data")
        if cached_data:
            return cached_data

        # Try FHFA first
        fhfa = integration_manager.get("fhfa")
        if fhfa and fhfa.is_available:
            try:
                result = await fhfa.get_house_price_index()
                if result.success and result.data:
                    await self.cache.set(cache_key, result.data, namespace="market_data", cache_type="real_estate_data")
                    return result.data
            except Exception as e:
                logger.warning(f"FHFA integration failed: {e}")

        # Try HUD as fallback
        hud = integration_manager.get("hud")
        if hud and hud.is_available:
            try:
                result = await hud.get_fair_market_rent("00000")  # National data
                if result.success and result.data:
                    await self.cache.set(cache_key, result.data, namespace="market_data", cache_type="real_estate_data")
                    return result.data
            except Exception as e:
                logger.warning(f"HUD integration failed: {e}")

        # Return mock data
        logger.info("Returning mock housing indicators (all sources unavailable)")
        mock_data = {
            "house_price_index": 298.5,
            "year_over_year_change": 5.2,
            "median_sale_price": 385000,
            "median_list_price": 395000,
            "months_supply": 3.1,
            "last_updated": datetime.utcnow().isoformat(),
            "source": "mock_data",
            "note": "Real data unavailable - using mock data"
        }
        return mock_data

    async def get_interest_rates(self) -> Dict[str, Any]:
        """
        Get interest rates with fallback

        Attempts:
        1. Bank of Israel (for international rates)
        2. Cached data
        3. Mock data
        """
        cache_key = "interest_rates"

        # Check cache
        cached_data = await self.cache.get(cache_key, namespace="market_data", cache_type="economic_indicators")
        if cached_data:
            return cached_data

        # Try Bank of Israel
        boi = integration_manager.get("bank_of_israel")
        if boi and boi.is_available:
            try:
                result = await boi.get_interest_rate()
                if result.success and result.data:
                    await self.cache.set(cache_key, result.data, namespace="market_data", cache_type="economic_indicators")
                    return result.data
            except Exception as e:
                logger.warning(f"Bank of Israel integration failed: {e}")

        # Return mock data
        logger.info("Returning mock interest rates (all sources unavailable)")
        mock_data = {
            "federal_funds_rate": 5.33,
            "prime_rate": 8.50,
            "mortgage_30y": 7.08,
            "mortgage_15y": 6.35,
            "treasury_10y": 4.57,
            "last_updated": datetime.utcnow().isoformat(),
            "source": "mock_data",
            "note": "Real data unavailable - using mock data"
        }
        return mock_data

    async def get_market_intelligence_summary(
        self,
        location: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get comprehensive market intelligence summary with all failsafes

        This aggregates data from multiple sources with proper error handling.
        Will never fail - returns mock data if all sources are unavailable.
        """
        logger.info(f"Fetching market intelligence summary for location: {location or 'national'}")

        # Fetch all data sources in parallel
        try:
            employment, housing, rates = await asyncio.gather(
                self.get_employment_data(),
                self.get_housing_indicators(),
                self.get_interest_rates(),
                return_exceptions=True
            )

            # Handle exceptions from gather
            if isinstance(employment, Exception):
                logger.error(f"Employment data error: {employment}")
                employment = {"error": str(employment), "source": "error"}

            if isinstance(housing, Exception):
                logger.error(f"Housing data error: {housing}")
                housing = {"error": str(housing), "source": "error"}

            if isinstance(rates, Exception):
                logger.error(f"Interest rates error: {rates}")
                rates = {"error": str(rates), "source": "error"}

        except Exception as e:
            logger.error(f"Failed to fetch market intelligence: {e}")
            # Return minimal mock data
            return {
                "employment": {"error": "unavailable"},
                "housing": {"error": "unavailable"},
                "interest_rates": {"error": "unavailable"},
                "location": location,
                "timestamp": datetime.utcnow().isoformat(),
                "status": "error",
                "message": "Market data temporarily unavailable"
            }

        # Get list of active integrations
        active_integrations = integration_manager.get_available()

        return {
            "employment": employment,
            "housing_market": housing,
            "interest_rates": rates,
            "location": location or "national",
            "timestamp": datetime.utcnow().isoformat(),
            "active_data_sources": len(active_integrations),
            "data_sources": list(active_integrations.keys()),
            "status": "success"
        }

    async def get_integration_health(self) -> Dict[str, Any]:
        """
        Check health of all integrations

        Returns status of each integration for monitoring
        """
        status_summary = integration_manager.get_status_summary()

        health = {
            "total_integrations": len(status_summary),
            "active_integrations": sum(1 for v in status_summary.values() if v["available"]),
            "integrations": status_summary,
            "timestamp": datetime.utcnow().isoformat(),
            "overall_health": "healthy" if sum(1 for v in status_summary.values() if v["available"]) > 0 else "degraded"
        }

        return health

    async def calculate_gentrification_score(
        self,
        location: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Calculate gentrification risk score for a location (0-100)

        Analyzes multiple indicators:
        - Housing price growth trends
        - Employment and income changes
        - Market velocity (days on market, inventory)
        - Interest rate environment
        - Comparative regional metrics

        Score Ranges:
        - 0-25: Low gentrification risk
        - 26-50: Moderate gentrification risk
        - 51-75: High gentrification risk
        - 76-100: Very high gentrification risk
        """
        logger.info(f"Calculating gentrification score for location: {location or 'national'}")

        # Fetch market data in parallel
        try:
            employment, housing, rates = await asyncio.gather(
                self.get_employment_data(),
                self.get_housing_indicators(),
                self.get_interest_rates(),
                return_exceptions=True
            )

            # Handle exceptions
            if isinstance(employment, Exception):
                logger.warning(f"Employment data unavailable: {employment}")
                employment = {"unemployment_rate": 4.0, "source": "fallback"}

            if isinstance(housing, Exception):
                logger.warning(f"Housing data unavailable: {housing}")
                housing = {"year_over_year_change": 3.0, "months_supply": 4.0, "source": "fallback"}

            if isinstance(rates, Exception):
                logger.warning(f"Interest rates unavailable: {rates}")
                rates = {"mortgage_30y": 7.0, "source": "fallback"}

        except Exception as e:
            logger.error(f"Failed to fetch data for gentrification score: {e}")
            return {
                "score": 50,
                "risk_level": "unknown",
                "confidence": "low",
                "error": "Insufficient data to calculate accurate score",
                "timestamp": datetime.utcnow().isoformat()
            }

        # Calculate component scores (0-100 each)
        scores = {}

        # 1. Housing Price Growth Score (30% weight)
        # Rapid price growth indicates gentrification pressure
        price_growth = housing.get("year_over_year_change", 3.0)
        if price_growth > 10:
            scores["price_growth"] = 100
        elif price_growth > 7:
            scores["price_growth"] = 80
        elif price_growth > 5:
            scores["price_growth"] = 60
        elif price_growth > 3:
            scores["price_growth"] = 40
        else:
            scores["price_growth"] = 20

        # 2. Market Velocity Score (25% weight)
        # Low inventory and quick sales indicate hot market
        months_supply = housing.get("months_supply", 4.0)
        if months_supply < 2:
            scores["market_velocity"] = 100
        elif months_supply < 3:
            scores["market_velocity"] = 80
        elif months_supply < 4:
            scores["market_velocity"] = 60
        elif months_supply < 6:
            scores["market_velocity"] = 40
        else:
            scores["market_velocity"] = 20

        # 3. Employment Strength Score (20% weight)
        # Low unemployment can drive gentrification
        unemployment = employment.get("unemployment_rate", 4.0)
        if unemployment < 3:
            scores["employment"] = 90
        elif unemployment < 4:
            scores["employment"] = 70
        elif unemployment < 5:
            scores["employment"] = 50
        elif unemployment < 6:
            scores["employment"] = 30
        else:
            scores["employment"] = 10

        # 4. Interest Rate Environment Score (15% weight)
        # Lower rates accelerate gentrification
        mortgage_rate = rates.get("mortgage_30y", 7.0)
        if mortgage_rate < 4:
            scores["interest_rates"] = 90
        elif mortgage_rate < 5:
            scores["interest_rates"] = 70
        elif mortgage_rate < 6:
            scores["interest_rates"] = 50
        elif mortgage_rate < 7:
            scores["interest_rates"] = 30
        else:
            scores["interest_rates"] = 10

        # 5. Price-to-Income Indicator (10% weight)
        # Higher price points relative to market suggest gentrification
        median_price = housing.get("median_sale_price", 385000)
        if median_price > 500000:
            scores["affordability"] = 80
        elif median_price > 400000:
            scores["affordability"] = 60
        elif median_price > 300000:
            scores["affordability"] = 40
        elif median_price > 200000:
            scores["affordability"] = 20
        else:
            scores["affordability"] = 10

        # Calculate weighted average
        weights = {
            "price_growth": 0.30,
            "market_velocity": 0.25,
            "employment": 0.20,
            "interest_rates": 0.15,
            "affordability": 0.10
        }

        total_score = sum(scores[key] * weights[key] for key in scores.keys())
        total_score = round(total_score, 1)

        # Determine risk level
        if total_score >= 76:
            risk_level = "very_high"
            risk_description = "Very High Gentrification Risk"
            recommendation = "Area shows strong gentrification indicators. Expect rapid price appreciation and demographic shifts."
        elif total_score >= 51:
            risk_level = "high"
            risk_description = "High Gentrification Risk"
            recommendation = "Area demonstrates significant gentrification pressure. Monitor for accelerating price growth."
        elif total_score >= 26:
            risk_level = "moderate"
            risk_description = "Moderate Gentrification Risk"
            recommendation = "Area shows moderate gentrification indicators. Stable growth expected."
        else:
            risk_level = "low"
            risk_description = "Low Gentrification Risk"
            recommendation = "Area exhibits minimal gentrification pressure. Traditional market dynamics likely."

        # Determine confidence based on data sources
        data_sources_available = sum(1 for data in [employment, housing, rates]
                                    if data.get("source") not in ["fallback", "mock_data", "error"])
        if data_sources_available >= 2:
            confidence = "high"
        elif data_sources_available == 1:
            confidence = "medium"
        else:
            confidence = "low"

        return {
            "score": total_score,
            "risk_level": risk_level,
            "risk_description": risk_description,
            "recommendation": recommendation,
            "confidence": confidence,
            "component_scores": {
                "price_growth": {
                    "score": scores["price_growth"],
                    "weight": "30%",
                    "value": f"{price_growth}%",
                    "indicator": "Year-over-year housing price change"
                },
                "market_velocity": {
                    "score": scores["market_velocity"],
                    "weight": "25%",
                    "value": f"{months_supply} months",
                    "indicator": "Housing inventory supply"
                },
                "employment": {
                    "score": scores["employment"],
                    "weight": "20%",
                    "value": f"{unemployment}%",
                    "indicator": "Unemployment rate"
                },
                "interest_rates": {
                    "score": scores["interest_rates"],
                    "weight": "15%",
                    "value": f"{mortgage_rate}%",
                    "indicator": "30-year mortgage rate"
                },
                "affordability": {
                    "score": scores["affordability"],
                    "weight": "10%",
                    "value": f"${median_price:,}",
                    "indicator": "Median home price"
                }
            },
            "market_indicators": {
                "price_growth_yoy": price_growth,
                "months_supply": months_supply,
                "unemployment_rate": unemployment,
                "mortgage_rate_30y": mortgage_rate,
                "median_price": median_price
            },
            "location": location or "national",
            "timestamp": datetime.utcnow().isoformat(),
            "data_quality": {
                "sources_available": data_sources_available,
                "confidence_level": confidence,
                "employment_source": employment.get("source", "unknown"),
                "housing_source": housing.get("source", "unknown"),
                "rates_source": rates.get("source", "unknown")
            }
        }


# Global service instance
market_data_service = MarketDataService()
