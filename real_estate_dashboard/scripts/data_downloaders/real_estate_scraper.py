#!/usr/bin/env python3
"""
Real Estate Property Scraper using HomeHarvest
Scrapes Zillow, Realtor.com, and Redfin WITHOUT API keys
"""

import sys
import time
import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import logging

# Check if homeharvest is installed
try:
    from homeharvest import scrape_property
    HOMEHARVEST_AVAILABLE = True
except ImportError:
    HOMEHARVEST_AVAILABLE = False
    print("⚠️  HomeHarvest not installed. Run: pip install homeharvest")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RealEstateScraper:
    """Scrape real estate properties from multiple sources"""

    def __init__(self, output_dir: str = "./scraped_data"):
        if not HOMEHARVEST_AVAILABLE:
            raise ImportError("homeharvest package not installed")

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def scrape_location(
        self,
        location: str,
        listing_type: str = "for_sale",
        past_days: Optional[int] = None,
        delay_seconds: int = 3
    ) -> pd.DataFrame:
        """
        Scrape properties for a location

        Args:
            location: ZIP code, city, or address
            listing_type: for_sale, for_rent, sold, pending
            past_days: Days of history for sold/pending
            delay_seconds: Delay between requests (default 3)

        Returns:
            DataFrame of properties
        """
        logger.info(f"Scraping {listing_type} properties in {location}")

        try:
            # Add delay to be respectful
            time.sleep(delay_seconds)

            # Scrape
            df = scrape_property(
                location=location,
                listing_type=listing_type,
                past_days=past_days
            )

            logger.info(f"✓ Found {len(df)} properties")

            return df

        except Exception as e:
            logger.error(f"Error scraping {location}: {e}")
            return pd.DataFrame()

    def scrape_multiple_locations(
        self,
        locations: List[str],
        listing_type: str = "for_sale",
        delay_seconds: int = 5
    ) -> pd.DataFrame:
        """
        Scrape multiple locations with rate limiting

        Args:
            locations: List of ZIP codes or cities
            listing_type: Type of listings to scrape
            delay_seconds: Delay between locations
        """
        all_properties = []

        logger.info(f"Scraping {len(locations)} locations...")

        for i, location in enumerate(locations, 1):
            logger.info(f"\n[{i}/{len(locations)}] {location}")

            df = self.scrape_location(
                location=location,
                listing_type=listing_type,
                delay_seconds=delay_seconds
            )

            if not df.empty:
                all_properties.append(df)

        if all_properties:
            combined = pd.concat(all_properties, ignore_index=True)
            logger.info(f"\n✓ Total properties: {len(combined)}")
            return combined
        else:
            logger.warning("No properties found")
            return pd.DataFrame()

    def scrape_comps(
        self,
        address: str,
        min_beds: Optional[int] = None,
        max_beds: Optional[int] = None,
        past_days: int = 180
    ) -> pd.DataFrame:
        """
        Scrape comparable sold properties

        Args:
            address: Subject property address
            min_beds: Minimum bedrooms
            max_beds: Maximum bedrooms
            past_days: Days of sold history (default 180)
        """
        logger.info(f"Finding comps for: {address}")

        df = self.scrape_location(
            location=address,
            listing_type="sold",
            past_days=past_days
        )

        if df.empty:
            return df

        # Filter by bedrooms
        if min_beds is not None:
            df = df[df['beds'] >= min_beds]
        if max_beds is not None:
            df = df[df['beds'] <= max_beds]

        # Sort by most recent
        if 'sold_date' in df.columns:
            df = df.sort_values('sold_date', ascending=False)

        logger.info(f"✓ Found {len(df)} comparable sales")

        return df

    def analyze_market(self, df: pd.DataFrame) -> Dict:
        """
        Analyze market statistics from scraped data
        """
        if df.empty:
            return {}

        stats = {
            'count': len(df),
            'avg_price': df['price'].mean() if 'price' in df.columns else None,
            'median_price': df['price'].median() if 'price' in df.columns else None,
            'min_price': df['price'].min() if 'price' in df.columns else None,
            'max_price': df['price'].max() if 'price' in df.columns else None,
        }

        # Price per sqft
        if 'price' in df.columns and 'sqft' in df.columns:
            df['price_per_sqft'] = df['price'] / df['sqft']
            stats['avg_price_per_sqft'] = df['price_per_sqft'].mean()
            stats['median_price_per_sqft'] = df['price_per_sqft'].median()

        # By bedrooms
        if 'beds' in df.columns:
            stats['by_bedrooms'] = df.groupby('beds')['price'].agg(['count', 'mean', 'median']).to_dict()

        return stats

    def save_results(
        self,
        df: pd.DataFrame,
        filename: str,
        format: str = 'csv'
    ) -> str:
        """
        Save scraped data to file

        Args:
            df: DataFrame to save
            filename: Output filename (without extension)
            format: csv or excel
        """
        if df.empty:
            logger.warning("No data to save")
            return None

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_filename = filename.replace(' ', '_').replace(',', '')

        if format == 'csv':
            filepath = self.output_dir / f"{safe_filename}_{timestamp}.csv"
            df.to_csv(filepath, index=False)
        elif format == 'excel':
            filepath = self.output_dir / f"{safe_filename}_{timestamp}.xlsx"
            df.to_excel(filepath, index=False)
        else:
            raise ValueError(f"Unsupported format: {format}")

        logger.info(f"✓ Saved to {filepath}")
        return str(filepath)


def main():
    """Interactive scraper"""
    if not HOMEHARVEST_AVAILABLE:
        print("\n❌ HomeHarvest not installed")
        print("Install with: pip install homeharvest")
        print("Requires Python >= 3.10")
        return

    print(f"\n🏠 Real Estate Property Scraper")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    print("\n⚠️  IMPORTANT:")
    print("  • Use responsibly and respect rate limits")
    print("  • Add delays between requests (3-5 seconds)")
    print("  • For personal/research use only")
    print("  • May violate Terms of Service - use at your own risk")
    print("="*80)

    scraper = RealEstateScraper()

    print("\n📊 Scraping Options:")
    print("  1. Scrape single location")
    print("  2. Scrape multiple locations")
    print("  3. Find comparable sales")
    print("  4. Market analysis")
    print("  0. Exit")

    while True:
        choice = input("\n👉 Enter choice: ").strip()

        if choice == '0':
            break

        elif choice == '1':
            location = input("Enter location (ZIP, city, or address): ").strip()
            listing_type = input("Listing type (for_sale/for_rent/sold/pending): ").strip() or "for_sale"

            past_days = None
            if listing_type in ['sold', 'pending']:
                days = input("Past days (default 30): ").strip()
                past_days = int(days) if days else 30

            df = scraper.scrape_location(location, listing_type, past_days)

            if not df.empty:
                print(f"\n✓ Found {len(df)} properties")
                print(f"Columns: {df.columns.tolist()}")
                print(f"\nSample:\n{df.head()}")

                save = input("\nSave results? (y/n): ")
                if save.lower() == 'y':
                    format_choice = input("Format (csv/excel): ").strip() or "csv"
                    scraper.save_results(df, location, format_choice)

        elif choice == '2':
            locations_input = input("Enter locations (comma-separated): ").strip()
            locations = [loc.strip() for loc in locations_input.split(',')]

            listing_type = input("Listing type (for_sale/for_rent/sold/pending): ").strip() or "for_sale"
            delay = input("Delay between requests (seconds, default 5): ").strip()
            delay = int(delay) if delay else 5

            df = scraper.scrape_multiple_locations(locations, listing_type, delay)

            if not df.empty:
                print(f"\n✓ Total: {len(df)} properties")
                print(f"\nSample:\n{df.head()}")

                save = input("\nSave results? (y/n): ")
                if save.lower() == 'y':
                    filename = input("Filename (without extension): ").strip() or "multi_location"
                    format_choice = input("Format (csv/excel): ").strip() or "csv"
                    scraper.save_results(df, filename, format_choice)

        elif choice == '3':
            address = input("Enter property address: ").strip()
            min_beds = input("Min bedrooms (optional): ").strip()
            max_beds = input("Max bedrooms (optional): ").strip()
            past_days = input("Past days (default 180): ").strip()

            df = scraper.scrape_comps(
                address=address,
                min_beds=int(min_beds) if min_beds else None,
                max_beds=int(max_beds) if max_beds else None,
                past_days=int(past_days) if past_days else 180
            )

            if not df.empty:
                print(f"\n✓ Found {len(df)} comparable sales")
                print(f"\nSample:\n{df.head()}")

                save = input("\nSave results? (y/n): ")
                if save.lower() == 'y':
                    scraper.save_results(df, f"comps_{address.split(',')[0]}", "csv")

        elif choice == '4':
            location = input("Enter location for market analysis: ").strip()
            listing_type = input("Listing type (for_sale/for_rent/sold): ").strip() or "for_sale"

            df = scraper.scrape_location(location, listing_type)

            if not df.empty:
                stats = scraper.analyze_market(df)

                print("\n" + "="*80)
                print("MARKET ANALYSIS")
                print("="*80)
                print(f"\nTotal Properties: {stats.get('count')}")
                print(f"\nPrice Statistics:")
                print(f"  Average:  ${stats.get('avg_price', 0):,.0f}")
                print(f"  Median:   ${stats.get('median_price', 0):,.0f}")
                print(f"  Min:      ${stats.get('min_price', 0):,.0f}")
                print(f"  Max:      ${stats.get('max_price', 0):,.0f}")

                if 'avg_price_per_sqft' in stats:
                    print(f"\nPrice per Sq Ft:")
                    print(f"  Average:  ${stats.get('avg_price_per_sqft', 0):.2f}")
                    print(f"  Median:   ${stats.get('median_price_per_sqft', 0):.2f}")

        else:
            print("❌ Invalid choice")

    print("\n✅ Done!\n")


if __name__ == "__main__":
    main()
