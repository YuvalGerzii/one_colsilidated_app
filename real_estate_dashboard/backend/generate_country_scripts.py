#!/usr/bin/env python3
"""
Generate Individual Country Update Scripts

Creates a separate script for each country that can be run independently.
Each script updates data for that specific country only.

Usage:
    python3 generate_country_scripts.py
    python3 generate_country_scripts.py --output-dir country_scripts/
"""

import os
import argparse
from pathlib import Path


COUNTRIES = {
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


def generate_country_script(country_slug: str, country_name: str) -> str:
    """Generate script content for a specific country"""
    return f'''#!/usr/bin/env python3
"""
Weekly Update Script for {country_name}

Automatically updates economic data for {country_name}.
Runs weekly to fetch new data and update existing records.

This script:
- Fetches data from all 11 categories (overview, gdp, labour, prices, etc.)
- Only updates data that's older than 7 days (smart caching)
- Stores all data in the database for {country_name}
- Logs all operations for monitoring

Usage:
    python3 update_{country_slug.replace("-", "_")}.py
    python3 update_{country_slug.replace("-", "_")}.py --force-refresh  # Force update all
    python3 update_{country_slug.replace("-", "_")}.py --max-age-days 3  # Update if older than 3 days

Manual Run:
    cd /home/user/real_estate_dashboard/backend
    python3 country_scripts/update_{country_slug.replace("-", "_")}.py

Cron Setup (run every Sunday at 2 AM):
    0 2 * * 0 cd /home/user/real_estate_dashboard/backend && python3 country_scripts/update_{country_slug.replace("-", "_")}.py >> logs/{country_slug}_update.log 2>&1
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
    """Update {country_name} economic data"""
    parser = argparse.ArgumentParser(description='Update {country_name} economic data')
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

    # Create fetcher for {country_name}
    fetcher = CountryDataFetcher(
        country="{country_slug}",
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
'''


def generate_all_scripts(output_dir: str = "country_scripts"):
    """Generate scripts for all countries"""
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    print(f"Generating country update scripts in: {output_path.absolute()}")
    print("=" * 80)

    created_scripts = []

    for country_slug, country_name in COUNTRIES.items():
        script_name = f"update_{country_slug.replace('-', '_')}.py"
        script_path = output_path / script_name

        # Generate script content
        content = generate_country_script(country_slug, country_name)

        # Write script
        with open(script_path, 'w') as f:
            f.write(content)

        # Make executable
        os.chmod(script_path, 0o755)

        created_scripts.append((country_name, script_name))
        print(f"✓ Created: {script_name}")

    print("=" * 80)
    print(f"\n✅ Generated {len(created_scripts)} country update scripts")

    # Create a master README
    readme_content = f"""# Country Update Scripts

This directory contains individual update scripts for each country.

## Generated Scripts

"""
    for country_name, script_name in sorted(created_scripts):
        readme_content += f"- `{script_name}` - Updates data for **{country_name}**\n"

    readme_content += """
## Usage

### Run a Single Country Update

```bash
cd /home/user/real_estate_dashboard/backend
python3 country_scripts/update_united_states.py
```

### Run with Options

```bash
# Force refresh all data
python3 country_scripts/update_china.py --force-refresh

# Only update if data is older than 3 days
python3 country_scripts/update_japan.py --max-age-days 3

# With custom delay to avoid rate limiting
python3 country_scripts/update_germany.py --delay 1.0
```

### Set Up Cron Job for a Country

Add to crontab:
```bash
# Update United States data every Sunday at 2 AM
0 2 * * 0 cd /home/user/real_estate_dashboard/backend && python3 country_scripts/update_united_states.py >> logs/united_states_update.log 2>&1

# Update China data every Monday at 3 AM
0 3 * * 1 cd /home/user/real_estate_dashboard/backend && python3 country_scripts/update_china.py >> logs/china_update.log 2>&1
```

## Features

Each script:
- ✅ Fetches all 11 economic categories
- ✅ Smart caching - only updates stale data (>7 days old)
- ✅ Stores in database with country-specific tables
- ✅ Logs all operations
- ✅ Reports errors and statistics
- ✅ Can be run via cron or manually

## Database Storage

All data is stored in PostgreSQL tables:
- `economics_country_overview` - Country snapshots
- `economics_indicators` - Individual indicators by category
- `economics_indicator_history` - Time-series data

Filter by country name in queries:
```python
from app.services.economics_db_service import EconomicsDBService
from app.models.database import SessionLocal

db = SessionLocal()
service = EconomicsDBService(db)

# Get United States housing data
us_housing = service.get_economic_indicators(
    country="United States",
    category="housing"
)
```

## Monitoring

View logs:
```bash
# View recent updates
tail -f logs/united_states_update.log

# Check all country logs
tail -f logs/*_update.log
```

Query database for freshness:
```python
freshness = service.get_data_freshness("United States")
print(f"Last updated: {{freshness['overview_last_updated']}}")
```

---

Generated by: `generate_country_scripts.py`
"""

    readme_path = output_path / "README.md"
    with open(readme_path, 'w') as f:
        f.write(readme_content)

    print(f"\n📄 Created README: {readme_path}")

    # Create a run_all.sh script
    run_all_content = """#!/bin/bash
#
# Run all country update scripts
#
# Usage: ./run_all.sh
# With delay: ./run_all.sh 5  # 5 second delay between countries

DELAY=${1:-2}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Running all country updates with ${DELAY}s delay between countries..."
echo ""

"""
    for country_name, script_name in sorted(created_scripts):
        run_all_content += f"""echo "Updating {country_name}..."
python3 "$SCRIPT_DIR/{script_name}"
sleep $DELAY
echo ""
"""

    run_all_content += """
echo "All country updates completed!"
"""

    run_all_path = output_path / "run_all.sh"
    with open(run_all_path, 'w') as f:
        f.write(run_all_content)
    os.chmod(run_all_path, 0o755)

    print(f"📄 Created run_all.sh: {run_all_path}")
    print("\nTo run all countries: ./country_scripts/run_all.sh")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Generate country update scripts')
    parser.add_argument('--output-dir', default='country_scripts',
                       help='Output directory for scripts (default: country_scripts)')

    args = parser.parse_args()

    generate_all_scripts(args.output_dir)


if __name__ == "__main__":
    main()
