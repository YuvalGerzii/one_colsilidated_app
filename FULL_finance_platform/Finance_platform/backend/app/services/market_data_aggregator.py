"""
Market Data Aggregator Service

Combines data from all external APIs into a unified market data response.
"""

from typing import Dict, List, Optional
from datetime import datetime

from app.services.costar_service import CoStarService
from app.services.zillow_service import ZillowService
from app.services.census_service import CensusService
from app.services.walkscore_service import WalkScoreService


class MarketDataAggregator:
    """
    Market Data Aggregator

    Fetches and combines data from multiple sources:
    - CoStar: Cap rates, rent comps, market trends
    - Zillow/Redfin: Property valuations and comparables
    - Census: Demographics and population trends
    - Walk Score: Walkability and amenities
    """

    def __init__(self):
        self.costar = CoStarService()
        self.zillow = ZillowService()
        self.census = CensusService()
        self.walkscore = WalkScoreService()

    async def get_comprehensive_market_data(
        self,
        address: str,
        city: str,
        state: str,
        zip_code: str,
        property_type: str,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
    ) -> Dict:
        """
        Fetch comprehensive market data from all sources.

        Args:
            address: Property address
            city: City name
            state: State abbreviation
            zip_code: ZIP code
            property_type: Property type (e.g., Multifamily, SFR, Office)
            latitude: Latitude coordinate (optional, for Walk Score)
            longitude: Longitude coordinate (optional, for Walk Score)

        Returns:
            Dictionary containing all market data
        """
        # Initialize response structure
        data = {
            "property_info": {
                "address": address,
                "city": city,
                "state": state,
                "zip_code": zip_code,
                "property_type": property_type,
                "latitude": latitude,
                "longitude": longitude,
            },
            "costar_data": {},
            "zillow_redfin_data": {},
            "census_data": {},
            "walk_score_data": {},
            "data_sources": [],
            "timestamp": datetime.utcnow().isoformat(),
        }

        # Fetch CoStar data
        try:
            costar_data = await self.costar.get_market_data(
                address, city, state, zip_code, property_type
            )
            data["costar_data"] = costar_data
            data["data_sources"].append("CoStar")
        except Exception as e:
            print(f"Error fetching CoStar data: {str(e)}")
            data["costar_data"] = {"error": str(e)}

        # Fetch Zillow/Redfin data
        try:
            zillow_data = await self.zillow.get_property_data(
                address, city, state, zip_code
            )
            redfin_data = await self.zillow.get_redfin_data(
                address, city, state, zip_code
            )
            data["zillow_redfin_data"] = {
                "zillow": zillow_data,
                "redfin": redfin_data,
            }
            data["data_sources"].extend(["Zillow", "Redfin"])
        except Exception as e:
            print(f"Error fetching Zillow/Redfin data: {str(e)}")
            data["zillow_redfin_data"] = {"error": str(e)}

        # Fetch Census data
        try:
            census_data = await self.census.get_demographic_data(
                city, state, zip_code
            )
            data["census_data"] = census_data
            data["data_sources"].append("U.S. Census Bureau")
        except Exception as e:
            print(f"Error fetching Census data: {str(e)}")
            data["census_data"] = {"error": str(e)}

        # Fetch Walk Score data (requires lat/lon)
        if latitude and longitude:
            try:
                walkscore_data = await self.walkscore.get_scores(
                    address, latitude, longitude
                )
                data["walk_score_data"] = walkscore_data
                data["data_sources"].append("Walk Score")
            except Exception as e:
                print(f"Error fetching Walk Score data: {str(e)}")
                data["walk_score_data"] = {"error": str(e)}
        else:
            data["walk_score_data"] = {
                "note": "Walk Score requires latitude and longitude coordinates"
            }

        return data

    async def get_investment_summary(
        self,
        address: str,
        city: str,
        state: str,
        zip_code: str,
        property_type: str,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
    ) -> Dict:
        """
        Generate an investment summary with key metrics from all sources.

        Args:
            address: Property address
            city: City name
            state: State abbreviation
            zip_code: ZIP code
            property_type: Property type
            latitude: Latitude coordinate
            longitude: Longitude coordinate

        Returns:
            Investment summary with key metrics
        """
        # Fetch comprehensive data
        data = await self.get_comprehensive_market_data(
            address, city, state, zip_code, property_type, latitude, longitude
        )

        # Extract key investment metrics
        costar = data.get("costar_data", {})
        zillow = data.get("zillow_redfin_data", {}).get("zillow", {})
        redfin = data.get("zillow_redfin_data", {}).get("redfin", {})
        census = data.get("census_data", {})
        walkscore = data.get("walk_score_data", {})

        summary = {
            "property_info": data["property_info"],
            "key_metrics": {
                # CoStar metrics
                "cap_rate": costar.get("cap_rate"),
                "market_trend": costar.get("market_trend"),
                "vacancy_rate": costar.get("vacancy_rate"),
                "market_rating": costar.get("market_rating"),
                # Zillow/Redfin metrics
                "property_value": zillow.get("zestimate"),
                "rent_estimate": zillow.get("rent_estimate"),
                "price_trend_30d": zillow.get("price_change_30d"),
                "days_on_market": redfin.get("days_on_market"),
                "market_hotness": redfin.get("competition_score"),
                # Census metrics
                "population": census.get("population"),
                "population_growth": census.get("population_growth"),
                "median_income": census.get("median_income"),
                "employment_rate": census.get("employment_rate"),
                # Walk Score metrics
                "walk_score": walkscore.get("walk_score"),
                "transit_score": walkscore.get("transit_score"),
                "walkability": walkscore.get("walk_score_description"),
            },
            "investment_indicators": self._calculate_investment_indicators(
                costar, zillow, census, walkscore
            ),
            "comparable_properties": zillow.get("comparable_properties", [])[:3],
            "comparable_sales": costar.get("comparable_sales", [])[:3],
            "timestamp": datetime.utcnow().isoformat(),
        }

        return summary

    def _calculate_investment_indicators(
        self,
        costar: Dict,
        zillow: Dict,
        census: Dict,
        walkscore: Dict
    ) -> Dict:
        """Calculate investment quality indicators."""
        indicators = {}

        # Market strength indicator (based on multiple factors)
        market_score = 0
        factors_checked = 0

        # CoStar market trend
        if costar.get("market_trend") == "Growing":
            market_score += 2
            factors_checked += 1
        elif costar.get("market_trend") == "Stable":
            market_score += 1
            factors_checked += 1
        elif costar.get("market_trend"):
            factors_checked += 1

        # Population growth
        pop_growth = census.get("population_growth", 0)
        if pop_growth > 5:
            market_score += 2
            factors_checked += 1
        elif pop_growth > 0:
            market_score += 1
            factors_checked += 1
        elif census.get("population_growth") is not None:
            factors_checked += 1

        # Walk score
        walk_score = walkscore.get("walk_score", 0)
        if walk_score >= 70:
            market_score += 2
            factors_checked += 1
        elif walk_score >= 50:
            market_score += 1
            factors_checked += 1
        elif walkscore.get("walk_score") is not None:
            factors_checked += 1

        # Calculate overall market strength
        if factors_checked > 0:
            market_strength = (market_score / (factors_checked * 2)) * 100
            if market_strength >= 75:
                indicators["market_strength"] = "Strong"
            elif market_strength >= 50:
                indicators["market_strength"] = "Moderate"
            else:
                indicators["market_strength"] = "Weak"
        else:
            indicators["market_strength"] = "Insufficient Data"

        # Cap rate analysis
        cap_rate = costar.get("cap_rate")
        if cap_rate:
            if cap_rate >= 7:
                indicators["cap_rate_analysis"] = "High - Good cash flow potential"
            elif cap_rate >= 5:
                indicators["cap_rate_analysis"] = "Moderate - Balanced investment"
            else:
                indicators["cap_rate_analysis"] = "Low - Appreciation-focused"

        # Demographic quality
        median_income = census.get("median_income", 0)
        if median_income >= 75000:
            indicators["demographic_quality"] = "High Income"
        elif median_income >= 50000:
            indicators["demographic_quality"] = "Middle Income"
        else:
            indicators["demographic_quality"] = "Lower Income"

        return indicators
