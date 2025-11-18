"""
Market Data Service with Database Integration

Provides market data from external APIs and stores results in the database.
"""

from typing import Dict, Optional
from sqlalchemy.orm import Session

from app.services.market_data_aggregator import MarketDataAggregator
from app.repositories.market_data_repository import MarketDataRepository


class MarketDataService:
    """
    Market Data Service with Database Integration

    Fetches data from external APIs and stores/retrieves from database.
    """

    def __init__(self):
        self.aggregator = MarketDataAggregator()
        self.repository = MarketDataRepository()

    async def get_comprehensive_market_data(
        self,
        db: Session,
        address: str,
        city: str,
        state: str,
        zip_code: str,
        property_type: str,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        company_id: Optional[int] = None,
        force_refresh: bool = False,
    ) -> Dict:
        """
        Get comprehensive market data from all sources.

        Args:
            db: Database session
            address: Property address
            city: City name
            state: State abbreviation
            zip_code: ZIP code
            property_type: Property type
            latitude: Latitude (optional)
            longitude: Longitude (optional)
            company_id: Associated company ID (optional)
            force_refresh: Force fetch from APIs instead of using cached data

        Returns:
            Comprehensive market data
        """
        # Check if we have recent data in the database (unless force refresh)
        if not force_refresh:
            existing_data = self.repository.get_by_address(db, address, city, state, zip_code)
            if existing_data:
                # Return cached data if less than 24 hours old
                from datetime import datetime
                time_diff = datetime.utcnow() - existing_data.last_updated
                if time_diff.total_seconds() < 86400:  # 24 hours
                    return existing_data.to_dict()

        # Fetch fresh data from external APIs
        api_data = await self.aggregator.get_comprehensive_market_data(
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            property_type=property_type,
            latitude=latitude,
            longitude=longitude,
        )

        # Parse and prepare data for database
        db_data = self._parse_api_data_for_db(api_data)

        # Store/update in database
        try:
            market_data_entry = self.repository.get_or_create(
                db=db,
                address=address,
                city=city,
                state=state,
                zip_code=zip_code,
                property_type=property_type,
                market_data=db_data,
                company_id=company_id,
            )
            return market_data_entry.to_dict()
        except Exception as e:
            # If database write fails, still return API data
            print(f"Warning: Failed to save to database: {str(e)}")
            return api_data

    async def get_investment_summary(
        self,
        db: Session,
        address: str,
        city: str,
        state: str,
        zip_code: str,
        property_type: str,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        company_id: Optional[int] = None,
    ) -> Dict:
        """
        Get investment summary with key metrics.

        Args:
            db: Database session
            address: Property address
            city: City name
            state: State abbreviation
            zip_code: ZIP code
            property_type: Property type
            latitude: Latitude (optional)
            longitude: Longitude (optional)
            company_id: Associated company ID (optional)

        Returns:
            Investment summary
        """
        # Get comprehensive data (will use cache if available)
        comprehensive_data = await self.get_comprehensive_market_data(
            db=db,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            property_type=property_type,
            latitude=latitude,
            longitude=longitude,
            company_id=company_id,
        )

        # Generate investment summary from comprehensive data
        return await self.aggregator.get_investment_summary(
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            property_type=property_type,
            latitude=latitude,
            longitude=longitude,
        )

    def _parse_api_data_for_db(self, api_data: Dict) -> Dict:
        """
        Parse API response data for database storage.

        Args:
            api_data: Raw API response data

        Returns:
            Dictionary formatted for database storage
        """
        costar = api_data.get("costar_data", {})
        zillow_redfin = api_data.get("zillow_redfin_data", {})
        zillow = zillow_redfin.get("zillow", {})
        redfin = zillow_redfin.get("redfin", {})
        census = api_data.get("census_data", {})
        walkscore = api_data.get("walk_score_data", {})
        property_info = api_data.get("property_info", {})

        return {
            # Location
            "latitude": property_info.get("latitude"),
            "longitude": property_info.get("longitude"),

            # CoStar data
            "costar_cap_rate": costar.get("cap_rate"),
            "costar_avg_rent_psf": costar.get("avg_rent_psf"),
            "costar_market_trend": costar.get("market_trend"),
            "costar_vacancy_rate": costar.get("vacancy_rate"),
            "costar_comparable_sales": costar.get("comparable_sales"),
            "costar_market_rating": costar.get("market_rating"),

            # Zillow/Redfin data
            "zillow_estimate": zillow.get("zestimate"),
            "zillow_rent_estimate": zillow.get("rent_estimate"),
            "zillow_price_sqft": zillow.get("price_sqft"),
            "zillow_price_change_30d": zillow.get("price_change_30d"),
            "zillow_comparable_properties": zillow.get("comparable_properties"),
            "redfin_hot_homes_rank": redfin.get("hot_homes_rank"),
            "redfin_days_on_market": redfin.get("days_on_market"),

            # Census data
            "census_population": census.get("population"),
            "census_median_income": census.get("median_income"),
            "census_population_growth": census.get("population_growth"),
            "census_employment_rate": census.get("employment_rate"),
            "census_age_median": census.get("age_median"),
            "census_education_bachelor_plus": census.get("education_bachelor_plus"),
            "census_demographics": census.get("demographics"),

            # Walk Score data
            "walk_score": walkscore.get("walk_score"),
            "transit_score": walkscore.get("transit_score"),
            "bike_score": walkscore.get("bike_score"),
            "walk_score_description": walkscore.get("walk_score_description"),
            "nearby_amenities": walkscore.get("nearby_amenities"),

            # Metadata
            "data_sources": api_data.get("data_sources", []),
        }

    def get_market_data_by_company(
        self,
        db: Session,
        company_id: int
    ) -> list:
        """
        Get all market data for a specific company.

        Args:
            db: Database session
            company_id: Company ID

        Returns:
            List of market data entries
        """
        market_data_entries = self.repository.get_by_company(db, company_id)
        return [entry.to_dict() for entry in market_data_entries]

    def search_market_data(
        self,
        db: Session,
        city: Optional[str] = None,
        state: Optional[str] = None,
        zip_code: Optional[str] = None,
        property_type: Optional[str] = None,
    ) -> list:
        """
        Search market data by location criteria.

        Args:
            db: Database session
            city: City name (optional)
            state: State abbreviation (optional)
            zip_code: ZIP code (optional)
            property_type: Property type (optional)

        Returns:
            List of matching market data entries
        """
        market_data_entries = self.repository.search_by_location(
            db=db,
            city=city,
            state=state,
            zip_code=zip_code,
            property_type=property_type,
        )
        return [entry.to_dict() for entry in market_data_entries]
