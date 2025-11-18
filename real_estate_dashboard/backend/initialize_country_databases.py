#!/usr/bin/env python3
"""
Initialize Country Databases

Creates separate PostgreSQL databases for each of the 23 countries.
Each database will contain all economics tables for that specific country.

Database naming convention: economics_{country_slug}
Examples:
  - economics_united_states
  - economics_china
  - economics_japan

Usage:
    python3 initialize_country_databases.py                    # Initialize all
    python3 initialize_country_databases.py --country us       # Initialize one
    python3 initialize_country_databases.py --list             # List status
    python3 initialize_country_databases.py --drop china       # Drop database (CAUTION!)

Prerequisites:
  - PostgreSQL server running
  - DATABASE_URL configured in .env
  - Database user has CREATE DATABASE privileges
"""

import sys
import argparse
import logging
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(parent_dir))

from app.database.country_database_manager import country_db_manager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def initialize_all():
    """Initialize databases for all 23 countries"""
    results = country_db_manager.initialize_all_databases()

    # Exit code based on success
    all_success = all(results.values())
    return 0 if all_success else 1


def initialize_one(country_slug: str):
    """Initialize database for a single country"""
    country_name = country_db_manager.COUNTRY_NAMES.get(country_slug)

    if not country_name:
        print(f"❌ Unknown country: {country_slug}")
        print(f"Available countries: {', '.join(country_db_manager.COUNTRY_NAMES.keys())}")
        return 1

    print(f"\n📊 Initializing database for {country_name}...")
    success = country_db_manager.initialize_country_database(country_slug)

    if success:
        db_name = country_db_manager.get_country_db_name(country_slug)
        print(f"✅ Success! Database: {db_name}\n")
        return 0
    else:
        print(f"❌ Failed to initialize database\n")
        return 1


def list_databases():
    """List all country databases and their status"""
    print("\n" + "=" * 80)
    print("COUNTRY DATABASE STATUS")
    print("=" * 80)

    databases = country_db_manager.list_country_databases()

    existing = []
    missing = []

    for country_slug, db_name, exists in databases:
        country_name = country_db_manager.COUNTRY_NAMES[country_slug]
        status = "✅" if exists else "❌"
        print(f"{status} {country_name:20} → {db_name}")

        if exists:
            existing.append(country_name)
        else:
            missing.append(country_name)

    print("=" * 80)
    print(f"\nExisting: {len(existing)}/{len(databases)}")
    if missing:
        print(f"Missing:  {len(missing)}")
        print(f"          {', '.join(missing)}")
    print("")

    return 0


def drop_database(country_slug: str):
    """Drop a country's database (CAUTION!)"""
    country_name = country_db_manager.COUNTRY_NAMES.get(country_slug)

    if not country_name:
        print(f"❌ Unknown country: {country_slug}")
        return 1

    db_name = country_db_manager.get_country_db_name(country_slug)

    # Confirm
    print(f"\n⚠️  WARNING: This will delete ALL data for {country_name}!")
    print(f"   Database: {db_name}")
    response = input("\nType 'DELETE' to confirm: ")

    if response != "DELETE":
        print("❌ Cancelled")
        return 1

    print(f"\n🗑️  Dropping database...")
    success = country_db_manager.drop_country_database(country_slug)

    if success:
        print(f"✅ Database dropped: {db_name}\n")
        return 0
    else:
        print(f"❌ Failed to drop database\n")
        return 1


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Initialize country-specific databases for economics data'
    )

    parser.add_argument(
        '--country',
        help='Initialize database for a specific country (e.g., united-states, china)'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all country databases and their status'
    )
    parser.add_argument(
        '--drop',
        help='Drop a country database (CAUTION: deletes all data!)'
    )

    args = parser.parse_args()

    # Handle commands
    if args.list:
        return list_databases()
    elif args.drop:
        return drop_database(args.drop)
    elif args.country:
        return initialize_one(args.country)
    else:
        return initialize_all()


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n❌ Interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        sys.exit(1)
