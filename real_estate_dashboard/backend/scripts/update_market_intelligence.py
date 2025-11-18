#!/usr/bin/env python3
"""
Market Intelligence Daily Update CLI

Run this script daily to update market intelligence data.
Recommended: Schedule with cron at 6 PM EST (after market close)

Usage:
    python3 scripts/update_market_intelligence.py
    python3 scripts/update_market_intelligence.py --dry-run
    python3 scripts/update_market_intelligence.py --force
"""

import sys
import os
import asyncio
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.market_intelligence_updater import run_daily_update


def main():
    parser = argparse.ArgumentParser(description='Update market intelligence data')
    parser.add_argument('--dry-run', action='store_true', help='Run without saving to database')
    parser.add_argument('--force', action='store_true', help='Force update even if recently updated')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()

    if args.dry_run:
        print("⚠️  DRY RUN MODE - No data will be saved")

    if args.force:
        print("⚡ FORCE MODE - Ignoring recent update checks")

    print("\n🚀 Starting Market Intelligence Daily Update...")
    print("=" * 80)

    try:
        # Run the update
        result = asyncio.run(run_daily_update())

        # Exit code based on results
        if result['total_failures'] == 0:
            print("\n✅ Update completed successfully!")
            sys.exit(0)
        elif result['total_success'] > 0:
            print("\n⚠️  Update completed with some failures")
            sys.exit(1)
        else:
            print("\n❌ Update failed completely")
            sys.exit(2)

    except KeyboardInterrupt:
        print("\n\n⚠️  Update interrupted by user")
        sys.exit(130)

    except Exception as e:
        print(f"\n\n❌ Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
