#!/usr/bin/env python3
"""
Weekly Update Script for Australia

Automatically updates economic data for Australia.
Runs weekly to fetch new data and update existing records.

This script:
- Fetches data from all 11 categories (overview, gdp, labour, prices, etc.)
- Only updates data that's older than 7 days (smart caching)
- Stores all data in the database for Australia
- Logs all operations for monitoring

Usage:
    python3 update_australia.py
    python3 update_australia.py --force-refresh  # Force update all
    python3 update_australia.py --max-age-days 3  # Update if older than 3 days

Manual Run:
    cd /home/user/real_estate_dashboard/backend
    python3 country_scripts/update_australia.py

Cron Setup (run every Sunday at 2 AM):
    0 2 * * 0 cd /home/user/real_estate_dashboard/backend && python3 country_scripts/update_australia.py >> logs/australia_update.log 2>&1
"""

import os
import sys
import asyncio

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from country_data_fetcher import CountryDataFetcher
import argparse


async def main():
    """Update Australia economic data"""
    parser = argparse.ArgumentParser(description='Update Australia economic data')
    parser.add_argument('--api-key', help='API key (or use ECONOMICS_API_KEY env var)')
    parser.add_argument('--max-age-days', type=int, default=7,
                       help='Max age of data before refresh (default: 7 days)')
    parser.add_argument('--force-refresh', action='store_true',
                       help='Force refresh all data regardless of age')
    parser.add_argument('--delay', type=float, default=0.5,
                       help='Delay between API calls in seconds (default: 0.5)')

    args = parser.parse_args()

    # Get API key
    api_key = args.api_key or os.getenv('ECONOMICS_API_KEY')

    if not api_key:
        print("❌ ERROR: No API key configured!")
        print("   Set ECONOMICS_API_KEY in .env or pass --api-key argument")
        return 1

    # Create fetcher for Australia
    fetcher = CountryDataFetcher(
        country="australia",
        api_key=api_key,
        max_age_days=args.max_age_days,
        force_refresh=args.force_refresh
    )

    # Fetch all categories
    await fetcher.fetch_all_categories(delay=args.delay)

    # Print summary
    fetcher.print_summary()

    # Return exit code based on errors
    return 0 if not fetcher.stats['errors'] else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
