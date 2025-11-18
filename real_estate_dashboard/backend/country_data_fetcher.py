#!/usr/bin/env python3
"""
Country Economics Data Fetcher

Fetches and updates economic data for a specific country.
Includes smart caching - only fetches data that's missing or stale.

Usage:
    python3 country_data_fetcher.py united-states YOUR_API_KEY
    python3 country_data_fetcher.py china --max-age-days 7
    python3 country_data_fetcher.py israel --force-refresh
"""

import os
import sys
import asyncio
import argparse
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import time

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.database.country_database_manager import country_db_manager
from app.services.economics_api_service import EconomicsAPIService
from app.services.economics_db_service import EconomicsDBService
from app.settings import settings


class CountryDataFetcher:
    """Smart fetcher for a single country's economic data"""

    # All categories to fetch
    ALL_CATEGORIES = [
        "overview", "gdp", "labour", "prices", "health", "money", "trade",
        "government", "business", "consumer", "housing"
    ]

    # Country name mapping (API format to display name)
    COUNTRY_NAMES = {
        "united-states": "United States",
        "china": "China",
        "euro-area": "Euro Area",
        "japan": "Japan",
        "germany": "Germany",
        "india": "India",
        "united-kingdom": "United Kingdom",
        "france": "France",
        "russia": "Russia",
        "canada": "Canada",
        "italy": "Italy",
        "brazil": "Brazil",
        "australia": "Australia",
        "south-korea": "South Korea",
        "mexico": "Mexico",
        "spain": "Spain",
        "indonesia": "Indonesia",
        "saudi-arabia": "Saudi Arabia",
        "netherlands": "Netherlands",
        "turkey": "Turkey",
        "switzerland": "Switzerland",
        "taiwan": "Taiwan",
        "poland": "Poland",
    }

    def __init__(
        self,
        country: str,
        api_key: Optional[str] = None,
        db: Optional[Session] = None,
        max_age_days: int = 7,
        force_refresh: bool = False
    ):
        self.country = country.lower()
        self.country_display = self.COUNTRY_NAMES.get(self.country, country.title())
        self.api_key = api_key or settings.ECONOMICS_API_KEY
        self.api_service = EconomicsAPIService(api_key=self.api_key)

        # Use country-specific database
        if db:
            self.db = db
        else:
            # Get database session for this specific country
            self.db = country_db_manager.get_session(self.country)

        self.db_service = EconomicsDBService(self.db)
        self.max_age_days = max_age_days
        self.force_refresh = force_refresh

        self.stats = {
            'country': self.country,
            'categories_checked': 0,
            'categories_fetched': 0,
            'categories_skipped': 0,
            'indicators_saved': 0,
            'errors': [],
            'start_time': datetime.now()
        }

    def _should_fetch_category(self, category: str) -> bool:
        """Check if we need to fetch this category"""
        if self.force_refresh:
            return True

        # Check if we have recent data for this category
        indicators = self.db_service.get_economic_indicators(
            country=self.country_display,
            category=category,
            limit=1
        )

        if not indicators:
            # No data exists, need to fetch
            return True

        # Check data age
        latest = indicators[0]
        if latest.data_date:
            age = datetime.now() - latest.data_date
            if age.days > self.max_age_days:
                return True  # Data is stale

        return False  # Data is fresh, skip

    async def fetch_overview(self) -> Dict[str, Any]:
        """Fetch country overview (countries-overview endpoint)"""
        try:
            print(f"  📊 Checking overview data...")

            # For overview, check country_overview table
            latest = self.db_service.get_latest_country_overview(self.country_display)

            should_fetch = self.force_refresh
            if not should_fetch and latest:
                age = datetime.now() - latest.data_date
                should_fetch = age.days > self.max_age_days
            elif not latest:
                should_fetch = True

            if not should_fetch:
                print(f"    ✓ Overview data is fresh (last updated: {latest.data_date.date()})")
                self.stats['categories_skipped'] += 1
                return {'status': 'skipped', 'reason': 'data_fresh'}

            # Fetch from API
            print(f"    → Fetching overview from API...")
            start_time = time.time()
            result = await self.api_service.get_countries_overview(use_cache=False)
            response_time = int((time.time() - start_time) * 1000)

            if 'error' in result:
                print(f"    ✗ Error: {result['error']}")
                self.stats['errors'].append(f"overview: {result['error']}")
                return result

            # Find our country in the response
            country_data = None
            if 'countries' in result:
                for c in result['countries']:
                    if c.get('Country') == self.country_display:
                        country_data = [c]
                        break

            if not country_data:
                print(f"    ⚠ Country not found in overview response")
                return {'status': 'not_found'}

            # Save to database
            saved = self.db_service.save_country_overview(country_data)
            self.stats['categories_fetched'] += 1
            self.stats['indicators_saved'] += saved

            # Log fetch
            self.db_service.log_fetch(
                endpoint="/v1/economics/countries-overview",
                country=self.country,
                category="overview",
                status="success",
                records_fetched=1,
                records_stored=saved,
                response_time_ms=response_time,
                triggered_by="weekly_update"
            )

            print(f"    ✓ Saved {saved} overview record(s)")
            return {'status': 'success', 'saved': saved}

        except Exception as e:
            print(f"    ✗ Error: {str(e)}")
            self.stats['errors'].append(f"overview: {str(e)}")
            return {'status': 'error', 'error': str(e)}

    async def fetch_category(self, category: str, delay: float = 0.5) -> Dict[str, Any]:
        """Fetch data for a specific category"""
        try:
            self.stats['categories_checked'] += 1
            print(f"  📈 Checking {category} data...")

            # Check if we need to fetch
            if not self._should_fetch_category(category):
                print(f"    ✓ {category.capitalize()} data is fresh, skipping")
                self.stats['categories_skipped'] += 1
                return {'status': 'skipped', 'reason': 'data_fresh'}

            # Add delay to avoid rate limiting
            await asyncio.sleep(delay)

            # Fetch from API
            print(f"    → Fetching {category} from API...")
            start_time = time.time()
            result = await self.api_service.get_economic_indicator(
                self.country, category, use_cache=False
            )
            response_time = int((time.time() - start_time) * 1000)

            if 'error' in result:
                print(f"    ✗ Error: {result['error']}")
                self.stats['errors'].append(f"{category}: {result['error']}")

                # Log failed fetch
                self.db_service.log_fetch(
                    endpoint=f"/v1/economics/{self.country}/{category}",
                    country=self.country,
                    category=category,
                    status="failed",
                    response_time_ms=response_time,
                    error_message=result['error'],
                    triggered_by="weekly_update"
                )
                return result

            # Save to database
            if 'data' in result and isinstance(result['data'], list):
                saved = self.db_service.save_economic_indicators(
                    result['data'], self.country_display, category
                )
                self.stats['categories_fetched'] += 1
                self.stats['indicators_saved'] += saved

                # Log successful fetch
                self.db_service.log_fetch(
                    endpoint=f"/v1/economics/{self.country}/{category}",
                    country=self.country,
                    category=category,
                    status="success",
                    records_fetched=len(result['data']),
                    records_stored=saved,
                    response_time_ms=response_time,
                    triggered_by="weekly_update"
                )

                print(f"    ✓ Saved {saved} {category} indicator(s)")
                return {'status': 'success', 'saved': saved}
            else:
                print(f"    ⚠ Unexpected response format")
                return {'status': 'unexpected_format'}

        except Exception as e:
            print(f"    ✗ Error: {str(e)}")
            self.stats['errors'].append(f"{category}: {str(e)}")
            return {'status': 'error', 'error': str(e)}

    async def fetch_all_categories(self, delay: float = 0.5):
        """Fetch all categories for the country"""
        print(f"\n{'='*80}")
        print(f" Updating Data: {self.country_display.upper()}")
        print(f"{'='*80}")
        print(f"Max Age: {self.max_age_days} days")
        print(f"Force Refresh: {self.force_refresh}")
        print(f"{'='*80}\n")

        # Fetch overview first
        await self.fetch_overview()

        # Fetch all categories
        for category in self.ALL_CATEGORIES:
            await self.fetch_category(category, delay=delay)

    def print_summary(self):
        """Print fetch summary"""
        end_time = datetime.now()
        duration = (end_time - self.stats['start_time']).total_seconds()

        print(f"\n{'='*80}")
        print(f" SUMMARY: {self.country_display.upper()}")
        print(f"{'='*80}")
        print(f"⏱️  Duration: {duration:.1f} seconds")
        print(f"📊 Categories Checked: {self.stats['categories_checked']}")
        print(f"⬇️  Categories Fetched: {self.stats['categories_fetched']}")
        print(f"⏭️  Categories Skipped: {self.stats['categories_skipped']} (data was fresh)")
        print(f"💾 Indicators Saved: {self.stats['indicators_saved']}")

        if self.stats['errors']:
            print(f"\n⚠️  Errors ({len(self.stats['errors'])}):")
            for error in self.stats['errors'][:5]:
                print(f"   - {error}")
            if len(self.stats['errors']) > 5:
                print(f"   ... and {len(self.stats['errors']) - 5} more")
        else:
            print(f"\n✅ No errors!")

        # Data freshness check
        freshness = self.db_service.get_data_freshness(self.country_display)
        if freshness['overview_last_updated']:
            print(f"\n📅 Data Freshness:")
            print(f"   Overview: {freshness['overview_last_updated'].date()}")
            if freshness['categories_last_updated']:
                for cat, date in list(freshness['categories_last_updated'].items())[:5]:
                    print(f"   {cat.capitalize()}: {date.date()}")


async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Fetch economics data for a country')
    parser.add_argument('country', help='Country slug (e.g., united-states, china)')
    parser.add_argument('api_key', nargs='?', help='API key (or use ECONOMICS_API_KEY env var)')
    parser.add_argument('--max-age-days', type=int, default=7,
                       help='Max age of data in days before refresh (default: 7)')
    parser.add_argument('--force-refresh', action='store_true',
                       help='Force refresh all data regardless of age')
    parser.add_argument('--delay', type=float, default=0.5,
                       help='Delay between API calls in seconds (default: 0.5)')

    args = parser.parse_args()

    # Get API key
    api_key = args.api_key or os.getenv('ECONOMICS_API_KEY')

    if not api_key:
        print("❌ ERROR: No API key provided!")
        print("   Usage: python3 country_data_fetcher.py COUNTRY API_KEY")
        print("   Or set ECONOMICS_API_KEY environment variable")
        return 1

    # Create fetcher
    fetcher = CountryDataFetcher(
        country=args.country,
        api_key=api_key,
        max_age_days=args.max_age_days,
        force_refresh=args.force_refresh
    )

    # Check if country is valid
    if fetcher.country not in fetcher.COUNTRY_NAMES:
        print(f"⚠️  Warning: '{args.country}' not in standard country list")
        print(f"   Proceeding anyway with display name: {fetcher.country_display}")

    # Fetch all data
    await fetcher.fetch_all_categories(delay=args.delay)

    # Print summary
    fetcher.print_summary()

    return 0 if not fetcher.stats['errors'] else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
