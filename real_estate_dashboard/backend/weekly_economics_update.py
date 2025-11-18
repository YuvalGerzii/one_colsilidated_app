#!/usr/bin/env python3
"""
Weekly Economics Data Update Script

Runs weekly to update economic data for all countries.
Smart caching - only fetches data that's missing or older than 7 days.

Usage:
    python3 weekly_economics_update.py
    python3 weekly_economics_update.py --countries united-states,china,israel
    python3 weekly_economics_update.py --max-age-days 7 --delay 1.0
    python3 weekly_economics_update.py --force-refresh  # Force update all
"""

import os
import sys
import asyncio
import argparse
from typing import List, Optional
from datetime import datetime
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from country_data_fetcher import CountryDataFetcher
from app.models.database import SessionLocal
from app.services.economics_db_service import EconomicsDBService
from app.settings import settings


class WeeklyEconomicsUpdater:
    """Manages weekly updates for all countries"""

    # All supported countries (in priority order)
    ALL_COUNTRIES = [
        "united-states",
        "china",
        "euro-area",
        "japan",
        "germany",
        "india",
        "united-kingdom",
        "france",
        "russia",
        "canada",
        "italy",
        "brazil",
        "australia",
        "south-korea",
        "mexico",
        "spain",
        "indonesia",
        "saudi-arabia",
        "netherlands",
        "turkey",
        "switzerland",
        "taiwan",
        "poland",
    ]

    def __init__(
        self,
        api_key: Optional[str] = None,
        countries: Optional[List[str]] = None,
        max_age_days: int = 7,
        force_refresh: bool = False,
        delay: float = 0.5,
        country_delay: float = 2.0
    ):
        self.api_key = api_key or settings.ECONOMICS_API_KEY
        self.countries = countries or self.ALL_COUNTRIES
        self.max_age_days = max_age_days
        self.force_refresh = force_refresh
        self.delay = delay  # Delay between category fetches
        self.country_delay = country_delay  # Delay between countries

        self.stats = {
            'total_countries': len(self.countries),
            'countries_updated': 0,
            'countries_skipped': 0,
            'countries_failed': 0,
            'total_indicators_saved': 0,
            'total_categories_fetched': 0,
            'start_time': datetime.now(),
            'errors': []
        }

    def print_header(self):
        """Print update header"""
        print("\n" + "=" * 80)
        print(" WEEKLY ECONOMICS DATA UPDATE")
        print("=" * 80)
        print(f"\n📅 Start Time: {self.stats['start_time'].strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🌍 Countries: {self.stats['total_countries']}")
        print(f"⏱️  Max Age: {self.max_age_days} days")
        print(f"🔄 Force Refresh: {self.force_refresh}")
        print(f"⏲️  Delays: {self.delay}s between categories, {self.country_delay}s between countries")

        if not self.api_key:
            print("\n❌ ERROR: No API key configured!")
            print("   Set ECONOMICS_API_KEY in .env or pass as argument")
            return False

        print("=" * 80)
        return True

    async def update_country(self, country: str) -> bool:
        """Update data for a single country"""
        try:
            print(f"\n🌍 Processing: {country.upper()}")
            print("-" * 80)

            # Create country fetcher with shared DB session
            db = SessionLocal()
            fetcher = CountryDataFetcher(
                country=country,
                api_key=self.api_key,
                db=db,
                max_age_days=self.max_age_days,
                force_refresh=self.force_refresh
            )

            # Fetch all data
            await fetcher.fetch_all_categories(delay=self.delay)

            # Update stats
            self.stats['countries_updated'] += 1
            self.stats['total_indicators_saved'] += fetcher.stats['indicators_saved']
            self.stats['total_categories_fetched'] += fetcher.stats['categories_fetched']

            if fetcher.stats['errors']:
                self.stats['errors'].extend([
                    f"{country}: {error}" for error in fetcher.stats['errors']
                ])

            # Print mini summary
            print(f"\n✅ {country.upper()}: {fetcher.stats['indicators_saved']} indicators saved, "
                  f"{fetcher.stats['categories_fetched']} categories updated")

            db.close()
            return True

        except Exception as e:
            print(f"\n❌ {country.upper()}: Failed - {str(e)}")
            self.stats['countries_failed'] += 1
            self.stats['errors'].append(f"{country}: {str(e)}")
            return False

    async def update_all_countries(self):
        """Update all countries"""
        for i, country in enumerate(self.countries, 1):
            print(f"\n{'='*80}")
            print(f" Country {i}/{len(self.countries)}")
            print(f"{'='*80}")

            await self.update_country(country)

            # Delay between countries (except last one)
            if i < len(self.countries):
                print(f"\n⏸️  Waiting {self.country_delay}s before next country...")
                await asyncio.sleep(self.country_delay)

    def print_summary(self):
        """Print final summary"""
        end_time = datetime.now()
        duration = (end_time - self.stats['start_time']).total_seconds()

        print("\n\n" + "=" * 80)
        print(" WEEKLY UPDATE SUMMARY")
        print("=" * 80)

        print(f"\n⏱️  Total Duration: {duration/60:.1f} minutes ({duration:.0f} seconds)")
        print(f"📅 Completed: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

        print(f"\n🌍 Countries:")
        print(f"   Total: {self.stats['total_countries']}")
        print(f"   ✅ Updated: {self.stats['countries_updated']}")
        print(f"   ⏭️  Skipped: {self.stats['countries_skipped']}")
        print(f"   ❌ Failed: {self.stats['countries_failed']}")

        print(f"\n📊 Data:")
        print(f"   Categories Fetched: {self.stats['total_categories_fetched']}")
        print(f"   Indicators Saved: {self.stats['total_indicators_saved']}")

        if self.stats['errors']:
            print(f"\n⚠️  Errors ({len(self.stats['errors'])}):")
            for error in self.stats['errors'][:10]:
                print(f"   - {error}")
            if len(self.stats['errors']) > 10:
                print(f"   ... and {len(self.stats['errors']) - 10} more")
        else:
            print(f"\n✅ No errors! All countries updated successfully.")

        # Database stats
        print(f"\n💾 Database Status:")
        db = SessionLocal()
        db_service = EconomicsDBService(db)
        countries_in_db = db_service.get_countries_with_data()
        print(f"   Countries with data: {len(countries_in_db)}")

        cache_stats = db_service.get_cache_stats()
        print(f"   Cache entries: {cache_stats['total_entries']}")
        print(f"   Valid cache: {cache_stats['valid_entries']}")

        # Recent fetch logs
        recent_logs = db_service.get_fetch_logs(hours=24, limit=10)
        if recent_logs:
            success_count = sum(1 for log in recent_logs if log.status == 'success')
            print(f"\n📊 Last 24 Hours:")
            print(f"   Total fetches: {len(recent_logs)}")
            print(f"   Success rate: {(success_count/len(recent_logs)*100):.1f}%")

        db.close()

        print("\n" + "=" * 80)
        print(" ✨ Weekly update completed!")
        print("=" * 80 + "\n")

    async def run(self):
        """Run the weekly update"""
        if not self.print_header():
            return 1

        await self.update_all_countries()
        self.print_summary()

        return 0 if self.stats['countries_failed'] == 0 else 1


async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Weekly economics data update')
    parser.add_argument('--api-key', help='API key (or use ECONOMICS_API_KEY env var)')
    parser.add_argument('--countries', help='Comma-separated country slugs (default: all)')
    parser.add_argument('--max-age-days', type=int, default=7,
                       help='Max age of data before refresh (default: 7)')
    parser.add_argument('--force-refresh', action='store_true',
                       help='Force refresh all data')
    parser.add_argument('--delay', type=float, default=0.5,
                       help='Delay between category fetches (default: 0.5s)')
    parser.add_argument('--country-delay', type=float, default=2.0,
                       help='Delay between countries (default: 2.0s)')
    parser.add_argument('--test', action='store_true',
                       help='Test mode: only update first 3 countries')

    args = parser.parse_args()

    # Parse countries
    countries = None
    if args.countries:
        countries = [c.strip().lower() for c in args.countries.split(',')]
    elif args.test:
        countries = WeeklyEconomicsUpdater.ALL_COUNTRIES[:3]
        print("🧪 TEST MODE: Only updating first 3 countries")

    # Create updater
    updater = WeeklyEconomicsUpdater(
        api_key=args.api_key,
        countries=countries,
        max_age_days=args.max_age_days,
        force_refresh=args.force_refresh,
        delay=args.delay,
        country_delay=args.country_delay
    )

    # Run update
    exit_code = await updater.run()
    return exit_code


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
