#!/usr/bin/env python3
"""
Bulk Economics Data Fetcher

Fetches economic data from all endpoints and stores in database.
Runs all categories for all countries and populates the database.

Usage:
    python3 bulk_fetch_economics_data.py [API_KEY]
    python3 bulk_fetch_economics_data.py --countries US,IL,CN
    python3 bulk_fetch_economics_data.py --categories gdp,labour,housing
"""

import os
import sys
import asyncio
import argparse
from typing import List, Optional
from datetime import datetime
import time

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.models.database import SessionLocal
from app.services.economics_api_service import EconomicsAPIService
from app.services.economics_db_service import EconomicsDBService
from app.settings import settings


class BulkEconomicsFetcher:
    """Bulk fetcher for economics data"""

    # All supported countries (can expand this list)
    ALL_COUNTRIES = [
        "united-states", "china", "japan", "germany", "united-kingdom",
        "france", "india", "italy", "brazil", "canada", "russia",
        "south-korea", "spain", "mexico", "indonesia", "saudi-arabia",
        "netherlands", "turkey", "switzerland", "taiwan", "poland",
        "australia", "israel", "euro-area"
    ]

    # All categories
    ALL_CATEGORIES = [
        "overview", "gdp", "labour", "prices", "money", "trade",
        "government", "business", "consumer", "housing"
    ]

    def __init__(self, api_key: Optional[str] = None, db: Optional[Session] = None):
        self.api_key = api_key or settings.ECONOMICS_API_KEY
        self.api_service = EconomicsAPIService(api_key=self.api_key)
        self.db = db or SessionLocal()
        self.db_service = EconomicsDBService(self.db)
        self.stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'total_records_saved': 0,
            'errors': [],
            'start_time': datetime.now()
        }

    def print_header(self, title: str):
        """Print formatted header"""
        print("\n" + "=" * 80)
        print(f" {title}")
        print("=" * 80)

    async def fetch_countries_overview(self) -> dict:
        """Fetch and store countries overview"""
        self.print_header("Fetching Countries Overview")

        try:
            start_time = time.time()
            result = await self.api_service.get_countries_overview(use_cache=False)
            response_time = int((time.time() - start_time) * 1000)

            self.stats['total_requests'] += 1

            if 'error' in result:
                print(f"❌ Error fetching countries overview: {result['error']}")
                self.stats['failed_requests'] += 1
                self.db_service.log_fetch(
                    endpoint="/v1/economics/countries-overview",
                    status="failed",
                    response_time_ms=response_time,
                    error_message=result['error']
                )
                return result

            # Save to database
            if 'countries' in result and isinstance(result['countries'], list):
                saved = self.db_service.save_country_overview(result['countries'])
                self.stats['successful_requests'] += 1
                self.stats['total_records_saved'] += saved
                print(f"✅ Fetched and saved {saved} countries")

                # Log fetch
                self.db_service.log_fetch(
                    endpoint="/v1/economics/countries-overview",
                    status="success",
                    records_fetched=len(result['countries']),
                    records_stored=saved,
                    response_time_ms=response_time,
                    triggered_by="bulk_fetch"
                )
            else:
                print(f"⚠️  Unexpected response format")
                self.stats['failed_requests'] += 1

            return result

        except Exception as e:
            print(f"❌ Error: {str(e)}")
            self.stats['failed_requests'] += 1
            self.stats['errors'].append(f"Countries overview: {str(e)}")
            return {'error': str(e)}

    async def fetch_country_indicators(
        self,
        country: str,
        category: str,
        delay: float = 0.5
    ) -> dict:
        """Fetch and store indicators for a country and category"""
        try:
            # Add delay to avoid rate limiting
            await asyncio.sleep(delay)

            start_time = time.time()
            result = await self.api_service.get_economic_indicator(
                country, category, use_cache=False
            )
            response_time = int((time.time() - start_time) * 1000)

            self.stats['total_requests'] += 1

            if 'error' in result:
                print(f"  ❌ {country}/{category}: {result['error']}")
                self.stats['failed_requests'] += 1
                self.db_service.log_fetch(
                    endpoint=f"/v1/economics/{country}/{category}",
                    country=country,
                    category=category,
                    status="failed",
                    response_time_ms=response_time,
                    error_message=result['error'],
                    triggered_by="bulk_fetch"
                )
                return result

            # Save to database
            if 'data' in result and isinstance(result['data'], list):
                saved = self.db_service.save_economic_indicators(
                    result['data'], country, category
                )
                self.stats['successful_requests'] += 1
                self.stats['total_records_saved'] += saved
                print(f"  ✅ {country}/{category}: {saved} indicators saved")

                # Log fetch
                self.db_service.log_fetch(
                    endpoint=f"/v1/economics/{country}/{category}",
                    country=country,
                    category=category,
                    status="success",
                    records_fetched=len(result['data']),
                    records_stored=saved,
                    response_time_ms=response_time,
                    triggered_by="bulk_fetch"
                )
            else:
                print(f"  ⚠️  {country}/{category}: Unexpected format")
                self.stats['failed_requests'] += 1

            return result

        except Exception as e:
            print(f"  ❌ {country}/{category}: {str(e)}")
            self.stats['failed_requests'] += 1
            self.stats['errors'].append(f"{country}/{category}: {str(e)}")
            return {'error': str(e)}

    async def fetch_all_countries_data(
        self,
        countries: Optional[List[str]] = None,
        categories: Optional[List[str]] = None,
        delay: float = 0.5
    ):
        """Fetch data for all countries and categories"""
        countries = countries or self.ALL_COUNTRIES
        categories = categories or self.ALL_CATEGORIES

        self.print_header(f"Fetching Data for {len(countries)} Countries, {len(categories)} Categories")

        for country in countries:
            print(f"\n📍 {country.upper()}")

            for category in categories:
                await self.fetch_country_indicators(country, category, delay=delay)

            # Small delay between countries
            await asyncio.sleep(1)

    async def run_full_fetch(
        self,
        countries: Optional[List[str]] = None,
        categories: Optional[List[str]] = None,
        include_overview: bool = True,
        delay: float = 0.5
    ):
        """Run complete data fetch"""
        self.print_header("BULK ECONOMICS DATA FETCH")
        print(f"\nAPI Key: {'✓ Configured' if self.api_key else '✗ Not configured'}")
        print(f"Start Time: {self.stats['start_time'].isoformat()}")
        print(f"Countries: {len(countries) if countries else len(self.ALL_COUNTRIES)}")
        print(f"Categories: {len(categories) if categories else len(self.ALL_CATEGORIES)}")

        if not self.api_key:
            print("\n❌ ERROR: No API key configured!")
            print("   Set ECONOMICS_API_KEY in .env or pass as argument")
            return

        # Step 1: Fetch countries overview
        if include_overview:
            await self.fetch_countries_overview()
            await asyncio.sleep(2)  # Delay before starting country-specific fetches

        # Step 2: Fetch country-specific data
        await self.fetch_all_countries_data(countries, categories, delay=delay)

        # Print summary
        self.print_summary()

    def print_summary(self):
        """Print fetch summary"""
        end_time = datetime.now()
        duration = (end_time - self.stats['start_time']).total_seconds()

        self.print_header("FETCH SUMMARY")

        print(f"\n⏱️  Duration: {duration:.1f} seconds")
        print(f"📊 Total Requests: {self.stats['total_requests']}")
        print(f"✅ Successful: {self.stats['successful_requests']}")
        print(f"❌ Failed: {self.stats['failed_requests']}")
        print(f"💾 Records Saved: {self.stats['total_records_saved']}")

        if self.stats['failed_requests'] > 0:
            success_rate = (self.stats['successful_requests'] / self.stats['total_requests']) * 100
            print(f"📈 Success Rate: {success_rate:.1f}%")

        if self.stats['errors']:
            print(f"\n⚠️  Errors ({len(self.stats['errors'])}):")
            for error in self.stats['errors'][:10]:  # Show first 10 errors
                print(f"   - {error}")
            if len(self.stats['errors']) > 10:
                print(f"   ... and {len(self.stats['errors']) - 10} more")

        # Database stats
        print(f"\n📂 Database Statistics:")
        countries_with_data = self.db_service.get_countries_with_data()
        print(f"   Countries in DB: {len(countries_with_data)}")

        cache_stats = self.db_service.get_cache_stats()
        print(f"   Cache Entries: {cache_stats['total_entries']}")
        print(f"   Valid Cache: {cache_stats['valid_entries']}")

        print(f"\n✨ Fetch completed at {end_time.isoformat()}")


async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Bulk fetch economics data')
    parser.add_argument('api_key', nargs='?', help='API key (or use ECONOMICS_API_KEY env var)')
    parser.add_argument('--countries', help='Comma-separated country codes (e.g., united-states,israel)')
    parser.add_argument('--categories', help='Comma-separated categories (e.g., gdp,labour,housing)')
    parser.add_argument('--skip-overview', action='store_true', help='Skip countries overview fetch')
    parser.add_argument('--delay', type=float, default=0.5, help='Delay between requests in seconds')

    args = parser.parse_args()

    # Get API key
    api_key = args.api_key or os.getenv('ECONOMICS_API_KEY')

    # Parse countries and categories
    countries = None
    if args.countries:
        countries = [c.strip().lower() for c in args.countries.split(',')]

    categories = None
    if args.categories:
        categories = [c.strip().lower() for c in args.categories.split(',')]

    # Run fetch
    fetcher = BulkEconomicsFetcher(api_key=api_key)
    await fetcher.run_full_fetch(
        countries=countries,
        categories=categories,
        include_overview=not args.skip_overview,
        delay=args.delay
    )


if __name__ == "__main__":
    asyncio.run(main())
