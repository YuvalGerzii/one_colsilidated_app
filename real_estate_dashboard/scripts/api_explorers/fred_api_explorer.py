#!/usr/bin/env python3
"""
FRED (Federal Reserve Economic Data) API Explorer
Explores economic and real estate indicators from the St. Louis Federal Reserve
"""

import requests
import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta


class FREDAPIExplorer:
    """Explore FRED API for real estate economic indicators"""

    BASE_URL = "https://api.stlouisfed.org/fred"
    API_KEY = "YOUR_FRED_API_KEY"  # Get free key at https://fredaccount.stlouisfed.org/apikeys

    # Key real estate series
    HOUSING_SERIES = {
        'HOUST': 'Housing Starts: Total New Privately Owned',
        'PERMIT': 'New Private Housing Units Authorized by Building Permits',
        'CSUSHPINSA': 'S&P/Case-Shiller U.S. National Home Price Index',
        'MSPUS': 'Median Sales Price of Houses Sold for the United States',
        'MSACSR': 'Monthly Supply of New Houses in the United States',
        'HSN1F': 'New One Family Houses Sold: United States',
        'USSTHPI': 'All-Transactions House Price Index for the United States',
        'COMPUTSA': 'Housing Units Under Construction',
        'TLRESCONS': 'Total Construction Spending: Residential',
    }

    MORTGAGE_SERIES = {
        'MORTGAGE30US': '30-Year Fixed Rate Mortgage Average in the United States',
        'MORTGAGE15US': '15-Year Fixed Rate Mortgage Average in the United States',
        'MORTGAGE5US': '5/1-Year Adjustable Rate Mortgage Average in the United States',
        'FEDFUNDS': 'Federal Funds Effective Rate',
        'DGS10': '10-Year Treasury Constant Maturity Rate',
        'DGS30': '30-Year Treasury Constant Maturity Rate',
    }

    COMMERCIAL_REAL_ESTATE = {
        'BOGZ1FL075035503Q': 'Commercial Real Estate Loans, All Commercial Banks',
        'TLCOMCON': 'Total Construction Spending: Commercial',
        'TLOFFCON': 'Total Construction Spending: Office',
        'TLHTLCON': 'Total Construction Spending: Lodging',
        'TLMFGCON': 'Total Construction Spending: Manufacturing',
    }

    ECONOMIC_INDICATORS = {
        'UNRATE': 'Unemployment Rate',
        'GDP': 'Gross Domestic Product',
        'CPIAUCSL': 'Consumer Price Index for All Urban Consumers: All Items',
        'PAYEMS': 'All Employees, Total Nonfarm',
        'POPTHM': 'Population',
        'PCEPILFE': 'Personal Consumption Expenditures Excluding Food and Energy (Core PCE)',
    }

    REGIONAL_HOUSING = {
        'ATNHPIUS06': 'All-Transactions House Price Index for California',
        'ATNHPIUS36': 'All-Transactions House Price Index for New York',
        'ATNHPIUS48': 'All-Transactions House Price Index for Texas',
        'ATNHPIUS12': 'All-Transactions House Price Index for Florida',
    }

    def __init__(self, api_key: Optional[str] = None):
        """Initialize explorer with optional API key"""
        if api_key:
            self.API_KEY = api_key

    def check_api_key(self) -> bool:
        """Verify API key is valid"""
        if self.API_KEY == "YOUR_FRED_API_KEY":
            print("\n⚠️  WARNING: Using placeholder API key")
            print("   Get free key at: https://fredaccount.stlouisfed.org/apikeys")
            return False
        return True

    def get_series_info(self, series_id: str) -> Dict:
        """Get metadata for a specific series"""
        url = f"{self.BASE_URL}/series"
        params = {
            'series_id': series_id,
            'api_key': self.API_KEY,
            'file_type': 'json'
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if 'seriess' in data and data['seriess']:
                series = data['seriess'][0]
                print(f"\n{series_id}:")
                print(f"  Title: {series.get('title')}")
                print(f"  Frequency: {series.get('frequency')}")
                print(f"  Units: {series.get('units')}")
                print(f"  Seasonal Adjustment: {series.get('seasonal_adjustment')}")
                print(f"  Observation Start: {series.get('observation_start')}")
                print(f"  Observation End: {series.get('observation_end')}")
                print(f"  Last Updated: {series.get('last_updated')}")
                return series

        except requests.exceptions.RequestException as e:
            print(f"Error fetching series info for {series_id}: {e}")
        return {}

    def get_series_observations(self, series_id: str, limit: int = 10) -> List[Dict]:
        """Get recent observations for a series"""
        url = f"{self.BASE_URL}/series/observations"
        params = {
            'series_id': series_id,
            'api_key': self.API_KEY,
            'file_type': 'json',
            'sort_order': 'desc',
            'limit': limit
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            observations = data.get('observations', [])
            if observations:
                print(f"\n  Recent observations ({len(observations)}):")
                for obs in observations[:5]:
                    print(f"    {obs['date']}: {obs['value']}")

            return observations

        except requests.exceptions.RequestException as e:
            print(f"Error fetching observations for {series_id}: {e}")
        return []

    def search_series(self, search_text: str, limit: int = 20) -> List[Dict]:
        """Search for series by keyword"""
        url = f"{self.BASE_URL}/series/search"
        params = {
            'search_text': search_text,
            'api_key': self.API_KEY,
            'file_type': 'json',
            'limit': limit
        }

        print(f"\n{'='*80}")
        print(f"SEARCHING: '{search_text}'")
        print('='*80)

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            series_list = data.get('seriess', [])
            print(f"\nFound {len(series_list)} series (showing {min(limit, len(series_list))})")

            for series in series_list[:limit]:
                print(f"\n{series['id']}")
                print(f"  {series['title']}")
                print(f"  Frequency: {series.get('frequency', 'N/A')}")
                print(f"  Popularity: {series.get('popularity', 'N/A')}")

            return series_list

        except requests.exceptions.RequestException as e:
            print(f"Error searching series: {e}")
        return []

    def explore_all_categories(self) -> None:
        """Explore all real estate categories"""
        print("\n" + "=" * 80)
        print("FRED API - REAL ESTATE DATA SERIES")
        print("=" * 80)

        if not self.check_api_key():
            print("\nℹ️  Showing available series without fetching data")
            self.show_all_series_list()
            return

        categories = [
            ("HOUSING MARKET INDICATORS", self.HOUSING_SERIES),
            ("MORTGAGE & INTEREST RATES", self.MORTGAGE_SERIES),
            ("COMMERCIAL REAL ESTATE", self.COMMERCIAL_REAL_ESTATE),
            ("ECONOMIC INDICATORS", self.ECONOMIC_INDICATORS),
            ("REGIONAL HOUSING INDICES", self.REGIONAL_HOUSING),
        ]

        for category_name, series_dict in categories:
            print(f"\n{'='*80}")
            print(f"{category_name}")
            print('='*80)

            for series_id, description in series_dict.items():
                print(f"\n{series_id}: {description}")
                self.get_series_info(series_id)
                self.get_series_observations(series_id, limit=5)

    def show_all_series_list(self) -> None:
        """Display all available series without API calls"""
        print("\n" + "=" * 80)
        print("📊 HOUSING MARKET INDICATORS")
        print("=" * 80)
        for series_id, desc in self.HOUSING_SERIES.items():
            print(f"  {series_id}: {desc}")

        print("\n" + "=" * 80)
        print("💰 MORTGAGE & INTEREST RATES")
        print("=" * 80)
        for series_id, desc in self.MORTGAGE_SERIES.items():
            print(f"  {series_id}: {desc}")

        print("\n" + "=" * 80)
        print("🏢 COMMERCIAL REAL ESTATE")
        print("=" * 80)
        for series_id, desc in self.COMMERCIAL_REAL_ESTATE.items():
            print(f"  {series_id}: {desc}")

        print("\n" + "=" * 80)
        print("📈 ECONOMIC INDICATORS")
        print("=" * 80)
        for series_id, desc in self.ECONOMIC_INDICATORS.items():
            print(f"  {series_id}: {desc}")

        print("\n" + "=" * 80)
        print("🗺️  REGIONAL HOUSING INDICES")
        print("=" * 80)
        for series_id, desc in self.REGIONAL_HOUSING.items():
            print(f"  {series_id}: {desc}")

    def get_time_series_data(self, series_id: str, start_date: str = None, end_date: str = None) -> Dict:
        """Get time series data for analysis"""
        url = f"{self.BASE_URL}/series/observations"

        if not start_date:
            # Default to 5 years ago
            start_date = (datetime.now() - timedelta(days=365*5)).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')

        params = {
            'series_id': series_id,
            'api_key': self.API_KEY,
            'file_type': 'json',
            'observation_start': start_date,
            'observation_end': end_date
        }

        print(f"\nFetching {series_id} from {start_date} to {end_date}...")

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            observations = data.get('observations', [])
            print(f"Retrieved {len(observations)} observations")

            return {
                'series_id': series_id,
                'start_date': start_date,
                'end_date': end_date,
                'count': len(observations),
                'data': observations
            }

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
        return {}

    def export_series_to_json(self, series_ids: List[str], output_file: str = None) -> None:
        """Export multiple series to JSON file"""
        if output_file is None:
            output_file = f"fred_data_{datetime.now().strftime('%Y%m%d')}.json"

        all_data = {}

        for series_id in series_ids:
            data = self.get_time_series_data(series_id)
            if data:
                all_data[series_id] = data

        with open(output_file, 'w') as f:
            json.dump(all_data, f, indent=2)

        print(f"\n✓ Data exported to: {output_file}")

    def show_capabilities_summary(self) -> None:
        """Display comprehensive summary"""
        print("\n" + "=" * 80)
        print("FRED API - REAL ESTATE CAPABILITIES SUMMARY")
        print("=" * 80)

        print("\n📊 DATA COVERAGE:")
        print("  • 800,000+ economic time series")
        print("  • Historical data back to 1940s (varies by series)")
        print("  • Daily, weekly, monthly, quarterly, annual frequencies")
        print("  • Free API with no rate limits")

        print("\n🏠 HOUSING MARKET DATA:")
        print("  • Housing starts and building permits")
        print("  • Home price indices (national and regional)")
        print("  • Sales prices and volumes")
        print("  • Housing supply and inventory")
        print("  • Construction spending")

        print("\n💵 FINANCIAL DATA:")
        print("  • Mortgage rates (30-year, 15-year, ARM)")
        print("  • Treasury rates")
        print("  • Federal funds rate")
        print("  • Commercial real estate loans")

        print("\n🏢 COMMERCIAL REAL ESTATE:")
        print("  • Commercial construction spending")
        print("  • Office building construction")
        print("  • Hotel/lodging construction")
        print("  • CRE loan volumes")

        print("\n📈 ECONOMIC INDICATORS:")
        print("  • GDP and economic growth")
        print("  • Employment and unemployment")
        print("  • Inflation (CPI, PCE)")
        print("  • Population growth")

        print("\n🎯 REAL ESTATE USE CASES:")
        print("  ✓ Market Forecasting: Housing starts, permits, inventory trends")
        print("  ✓ Pricing Models: Home price indices, interest rate correlations")
        print("  ✓ Investment Analysis: Economic cycles, mortgage rate impacts")
        print("  ✓ Risk Assessment: Employment trends, economic stability")
        print("  ✓ Development Planning: Construction costs, supply dynamics")

        print("\n" + "=" * 80)


def main():
    """Run FRED API exploration"""
    print(f"\n🔍 FRED API Explorer")
    print(f"📅 Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    explorer = FREDAPIExplorer()

    # Show capabilities
    explorer.show_capabilities_summary()

    # Show all available series
    print("\n\n" + "="*80)
    input("Press Enter to see all real estate series...")
    explorer.show_all_series_list()

    # Check for API key
    print("\n\n" + "="*80)
    has_key = input("\nDo you have a FRED API key? (y/n): ")

    if has_key.lower() == 'y':
        api_key = input("Enter your FRED API key: ")
        explorer = FREDAPIExplorer(api_key=api_key)

        # Explore series details
        explore = input("\nFetch detailed data for all series? (y/n): ")
        if explore.lower() == 'y':
            explorer.explore_all_categories()

        # Search capability
        search_query = input("\nEnter search term (or press Enter to skip): ")
        if search_query:
            explorer.search_series(search_query)

        # Export data
        export = input("\nExport key series to JSON? (y/n): ")
        if export.lower() == 'y':
            key_series = list(explorer.HOUSING_SERIES.keys())[:5]
            explorer.export_series_to_json(key_series)

    else:
        print("\nℹ️  Get a free API key at: https://fredaccount.stlouisfed.org/apikeys")
        print("   No registration fees, unlimited access!")

    print("\n✅ Exploration complete!\n")


if __name__ == "__main__":
    main()
