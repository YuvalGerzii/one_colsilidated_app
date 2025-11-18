"""Automated comparable properties pulling service from public APIs."""

from typing import List, Dict, Any, Optional
import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import requests

from app.models.crm import Comp, Deal
from app.settings import settings
from app.integrations.property_data.attom import AttomDataIntegration
from app.integrations.property_data.realtor import RealtorIntegration
from app.integrations.base import IntegrationConfig

logger = logging.getLogger(__name__)


class CompPullingService:
    """Service for automatically pulling comparable properties from public APIs."""

    def __init__(self):
        """Initialize comp pulling service."""
        # Initialize API clients if configured
        self.attom_client = None
        self.realtor_client = None

        attom_key = getattr(settings, 'ATTOM_API_KEY', None)
        if attom_key:
            try:
                config = IntegrationConfig(api_key=attom_key, is_active=True)
                self.attom_client = AttomDataIntegration(config=config)
            except Exception as e:
                logger.warning(f"Failed to initialize ATTOM client: {e}")

        realtor_key = getattr(settings, 'REALTOR_API_KEY', None)
        if realtor_key:
            try:
                config = IntegrationConfig(api_key=realtor_key, is_active=True)
                self.realtor_client = RealtorIntegration(config=config)
            except Exception as e:
                logger.warning(f"Failed to initialize Realtor client: {e}")

    def pull_comps_for_deal(
        self,
        db: Session,
        deal: Deal,
        radius_miles: float = 3.0,
        max_results: int = 20,
        time_period_days: int = 365,
    ) -> List[Comp]:
        """
        Automatically pull comparable properties for a deal.

        Args:
            db: Database session
            deal: Deal object to find comps for
            radius_miles: Search radius in miles
            max_results: Maximum number of comps to return
            time_period_days: Only include sales from last N days

        Returns:
            List of Comp objects created
        """
        comps_created = []

        # Pull from ATTOM if available
        if self.attom_client:
            try:
                attom_comps = self._pull_from_attom(
                    deal=deal,
                    radius_miles=radius_miles,
                    max_results=max_results,
                    time_period_days=time_period_days,
                )
                for comp_data in attom_comps:
                    comp = self._create_comp_from_data(db, comp_data, 'ATTOM')
                    if comp:
                        comps_created.append(comp)
            except Exception as e:
                logger.error(f"Error pulling comps from ATTOM: {e}")

        # Pull from Realtor.com if available
        if self.realtor_client and len(comps_created) < max_results:
            try:
                realtor_comps = self._pull_from_realtor(
                    deal=deal,
                    radius_miles=radius_miles,
                    max_results=max_results - len(comps_created),
                    time_period_days=time_period_days,
                )
                for comp_data in realtor_comps:
                    comp = self._create_comp_from_data(db, comp_data, 'Realtor.com')
                    if comp:
                        comps_created.append(comp)
            except Exception as e:
                logger.error(f"Error pulling comps from Realtor: {e}")

        # Pull from public records (example: county records, if available)
        if len(comps_created) < max_results:
            try:
                public_comps = self._pull_from_public_records(
                    deal=deal,
                    radius_miles=radius_miles,
                    max_results=max_results - len(comps_created),
                    time_period_days=time_period_days,
                )
                for comp_data in public_comps:
                    comp = self._create_comp_from_data(db, comp_data, 'Public Records')
                    if comp:
                        comps_created.append(comp)
            except Exception as e:
                logger.error(f"Error pulling comps from public records: {e}")

        db.commit()
        logger.info(f"Pulled {len(comps_created)} comps for deal {deal.id}")

        return comps_created

    def _pull_from_attom(
        self,
        deal: Deal,
        radius_miles: float,
        max_results: int,
        time_period_days: int,
    ) -> List[Dict[str, Any]]:
        """Pull comps from ATTOM Data API."""
        if not self.attom_client:
            return []

        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=time_period_days)

        # Build search criteria
        criteria = {
            'property_type': deal.property_type,
            'market': deal.market,
            'min_sale_date': start_date.strftime('%Y-%m-%d'),
            'max_sale_date': end_date.strftime('%Y-%m-%d'),
            'radius_miles': radius_miles,
            'limit': max_results,
        }

        if deal.property_address:
            criteria['address'] = deal.property_address

        # Search for comparable sales
        try:
            results = self.attom_client.search_sales(**criteria)
            return self._normalize_attom_results(results)
        except Exception as e:
            logger.error(f"ATTOM API error: {e}")
            return []

    def _pull_from_realtor(
        self,
        deal: Deal,
        radius_miles: float,
        max_results: int,
        time_period_days: int,
    ) -> List[Dict[str, Any]]:
        """Pull comps from Realtor.com API."""
        if not self.realtor_client:
            return []

        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=time_period_days)

        # Build search criteria
        criteria = {
            'property_type': deal.property_type,
            'city': deal.market,
            'min_sale_date': start_date.strftime('%Y-%m-%d'),
            'max_sale_date': end_date.strftime('%Y-%m-%d'),
            'radius': radius_miles,
            'limit': max_results,
            'status': 'sold',
        }

        # Search for comparable sales
        try:
            results = self.realtor_client.search_properties(**criteria)
            return self._normalize_realtor_results(results)
        except Exception as e:
            logger.error(f"Realtor API error: {e}")
            return []

    def _pull_from_public_records(
        self,
        deal: Deal,
        radius_miles: float,
        max_results: int,
        time_period_days: int,
    ) -> List[Dict[str, Any]]:
        """
        Pull comps from public records APIs.

        This is a placeholder for integration with county/state public records.
        Could integrate with:
        - County assessor databases
        - State property records
        - MLS feeds (if available)
        """
        # Placeholder - would integrate with specific public records APIs
        # For now, return empty list
        return []

    def _normalize_attom_results(self, results: List[Dict]) -> List[Dict[str, Any]]:
        """Normalize ATTOM API results to standard format."""
        normalized = []

        for result in results:
            try:
                normalized.append({
                    'property_name': result.get('address', {}).get('oneLine', 'Unknown'),
                    'property_address': result.get('address', {}).get('oneLine'),
                    'property_type': result.get('summary', {}).get('proptype'),
                    'market': result.get('address', {}).get('locality'),
                    'submarket': result.get('address', {}).get('countrySubd'),
                    'sale_date': result.get('sale', {}).get('saleTransDate'),
                    'sale_price': result.get('sale', {}).get('amount'),
                    'units': result.get('building', {}).get('rooms', {}).get('beds'),
                    'square_feet': result.get('building', {}).get('size', {}).get('universalsize'),
                    'year_built': result.get('summary', {}).get('yearbuilt'),
                    'buyer': result.get('sale', {}).get('buyer', {}).get('name1full'),
                    'seller': result.get('sale', {}).get('seller', {}).get('name1full'),
                    'data_source': 'ATTOM',
                    'verified': 1,
                    'verified_date': datetime.now().date(),
                    'confidence': 5,
                })
            except Exception as e:
                logger.error(f"Error normalizing ATTOM result: {e}")

        return normalized

    def _normalize_realtor_results(self, results: List[Dict]) -> List[Dict[str, Any]]:
        """Normalize Realtor.com API results to standard format."""
        normalized = []

        for result in results:
            try:
                normalized.append({
                    'property_name': result.get('address', {}).get('line', 'Unknown'),
                    'property_address': f"{result.get('address', {}).get('line')}, {result.get('address', {}).get('city')}, {result.get('address', {}).get('state')}",
                    'property_type': result.get('prop_type'),
                    'market': result.get('address', {}).get('city'),
                    'submarket': result.get('address', {}).get('neighborhood_name'),
                    'sale_date': result.get('last_sold_date'),
                    'sale_price': result.get('last_sold_price'),
                    'units': result.get('beds'),
                    'square_feet': result.get('sqft'),
                    'year_built': result.get('year_built'),
                    'data_source': 'Realtor.com',
                    'verified': 1,
                    'verified_date': datetime.now().date(),
                    'confidence': 4,
                })
            except Exception as e:
                logger.error(f"Error normalizing Realtor result: {e}")

        return normalized

    def _create_comp_from_data(
        self,
        db: Session,
        data: Dict[str, Any],
        source: str
    ) -> Optional[Comp]:
        """Create a Comp object from normalized data."""
        try:
            # Calculate metrics
            sale_price = data.get('sale_price')
            units = data.get('units')
            square_feet = data.get('square_feet')

            price_per_unit = None
            if sale_price and units and units > 0:
                price_per_unit = sale_price / units

            price_per_sf = None
            if sale_price and square_feet and square_feet > 0:
                price_per_sf = sale_price / square_feet

            # Parse sale date
            sale_date = None
            if data.get('sale_date'):
                try:
                    if isinstance(data['sale_date'], str):
                        sale_date = datetime.strptime(data['sale_date'], '%Y-%m-%d').date()
                    else:
                        sale_date = data['sale_date']
                except:
                    pass

            # Create comp
            comp = Comp(
                property_name=data.get('property_name', 'Unknown'),
                property_address=data.get('property_address'),
                property_type=data.get('property_type'),
                market=data.get('market'),
                submarket=data.get('submarket'),
                sale_date=sale_date,
                sale_price=sale_price,
                price_per_unit=price_per_unit,
                price_per_sf=price_per_sf,
                units=units,
                square_feet=square_feet,
                year_built=data.get('year_built'),
                year_renovated=data.get('year_renovated'),
                buyer=data.get('buyer'),
                seller=data.get('seller'),
                data_source=source,
                notes=f"Auto-pulled from {source}",
                confidence=data.get('confidence', 3),
                verified=data.get('verified', 0),
                verified_date=data.get('verified_date'),
            )

            db.add(comp)
            return comp

        except Exception as e:
            logger.error(f"Error creating comp from data: {e}")
            return None

    def pull_comps_by_criteria(
        self,
        db: Session,
        property_type: str,
        market: str,
        radius_miles: float = 5.0,
        max_results: int = 50,
        time_period_days: int = 365,
    ) -> List[Comp]:
        """
        Pull comps by specific criteria (not tied to a deal).

        Args:
            db: Database session
            property_type: Type of property
            market: Market/city
            radius_miles: Search radius
            max_results: Maximum results
            time_period_days: Time period for sales

        Returns:
            List of Comp objects
        """
        # Create a temporary deal-like object for search
        temp_deal = Deal(
            property_name=f"Search in {market}",
            property_type=property_type,
            market=market,
        )

        return self.pull_comps_for_deal(
            db=db,
            deal=temp_deal,
            radius_miles=radius_miles,
            max_results=max_results,
            time_period_days=time_period_days,
        )


# Global comp pulling service instance
comp_pulling_service = CompPullingService()
