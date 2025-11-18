#!/usr/bin/env python3
"""
BLS (Bureau of Labor Statistics) API Explorer
Explores employment, wages, CPI, and construction data
"""

import requests
import json
from typing import Dict, List, Optional
from datetime import datetime


class BLSAPIExplorer:
    """Explore BLS API for employment and economic data"""

    BASE_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
    API_KEY = "YOUR_BLS_API_KEY"  # Register at https://data.bls.gov/registrationEngine/

    # Key series IDs for real estate
    HOUSING_CPI_SERIES = {
        'CUUR0000SAH1': 'CPI - Housing',
        'CUUR0000SEHA': 'CPI - Rent of primary residence',
        'CUUR0000SAH21': 'CPI - Household furnishings and operations',
        'CUUR0000SEHC': 'CPI - Owners\' equivalent rent of residences',
        'CUUR0000SEHC01': 'CPI - Owners\' equivalent rent of primary residence',
    }

    CONSTRUCTION_EMPLOYMENT = {
        'CEU2023600001': 'Construction - All employees',
        'CEU2023620001': 'Construction - Residential building',
        'CEU2023630001': 'Construction - Nonresidential building',
        'CEU2000000001': 'Construction - Total private',
        'CES2000000001': 'Construction - All employees, thousands',
    }

    CONSTRUCTION_PPI = {
        'WPUSI012011': 'PPI - New office building construction',
        'WPUSI012012': 'PPI - New warehouse construction',
        'PCU23611-23611-': 'PPI - Residential building construction',
        'PCU236116236116': 'PPI - New single-family housing construction',
        'PCU236118236118': 'PPI - Residential remodelers',
    }

    REAL_ESTATE_SERVICES = {
        'CEU6553100001': 'Real estate - All employees',
        'CEU6553110001': 'Lessors of real estate - All employees',
        'CES6553100001': 'Real estate - All employees, thousands',
    }

    WAGES_EARNINGS = {
        'CEU2000000003': 'Construction - Average hourly earnings',
        'CEU6553100003': 'Real estate - Average hourly earnings',
        'CEU0000000003': 'Total private - Average hourly earnings',
    }

    def __init__(self, api_key: Optional[str] = None):
        """Initialize explorer with optional API key"""
        if api_key:
            self.API_KEY = api_key

    def check_api_key(self) -> bool:
        """Verify API key is configured"""
        if self.API_KEY == "YOUR_BLS_API_KEY":
            print("\n⚠️  WARNING: Using placeholder API key")
            print("   Register at: https://data.bls.gov/registrationEngine/")
            print("\n   V2 API Benefits:")
            print("   • 500 queries/day (vs 25 unregistered)")
            print("   • 50 series/query (vs 25 unregistered)")
            print("   • 20 years/query (vs 10 unregistered)")
            return False
        return True

    def get_series_data(self, series_ids: List[str], start_year: int = None,
                       end_year: int = None, show_data: bool = True) -> Dict:
        """
        Fetch data for one or more series
        V2 API allows up to 50 series per request
        """
        if start_year is None:
            start_year = datetime.now().year - 5
        if end_year is None:
            end_year = datetime.now().year

        payload = {
            'seriesid': series_ids,
            'startyear': str(start_year),
            'endyear': str(end_year),
        }

        if self.check_api_key():
            payload['registrationkey'] = self.API_KEY

        print(f"\n{'='*80}")
        print(f"FETCHING BLS DATA: {len(series_ids)} series ({start_year}-{end_year})")
        print('='*80)

        try:
            headers = {'Content-Type': 'application/json'}
            response = requests.post(self.BASE_URL, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()

            if data['status'] == 'REQUEST_SUCCEEDED':
                print(f"\n✓ Request successful")
                results = data.get('Results', {})
                series_data = results.get('series', [])

                print(f"Retrieved {len(series_data)} series")

                if show_data:
                    for series in series_data:
                        series_id = series['seriesID']
                        print(f"\n{series_id}:")

                        observations = series.get('data', [])
                        print(f"  Observations: {len(observations)}")

                        # Show most recent values
                        for obs in observations[:5]:
                            period = obs.get('period')
                            year = obs.get('year')
                            value = obs.get('value')
                            footnotes = obs.get('footnotes', [])

                            period_name = self.parse_period(period)
                            print(f"    {year} {period_name}: {value}")

                            if footnotes:
                                for fn in footnotes:
                                    if fn.get('text'):
                                        print(f"      Note: {fn['text']}")

                return data

            else:
                print(f"\n✗ Request failed: {data.get('message', 'Unknown error')}")
                return data

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
        return {}

    def parse_period(self, period_code: str) -> str:
        """Parse BLS period code to readable format"""
        if period_code.startswith('M'):
            month_num = int(period_code[1:])
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            return months[month_num - 1] if 1 <= month_num <= 12 else period_code
        elif period_code.startswith('Q'):
            return f"Q{period_code[1:]}"
        elif period_code == 'A01':
            return 'Annual'
        return period_code

    def explore_housing_cpi(self) -> None:
        """Explore housing-related CPI series"""
        print("\n" + "=" * 80)
        print("📊 HOUSING CPI (Consumer Price Index)")
        print("=" * 80)

        print("\nAvailable Series:")
        for series_id, desc in self.HOUSING_CPI_SERIES.items():
            print(f"  {series_id}: {desc}")

        if not self.check_api_key():
            return

        proceed = input("\nFetch data? (y/n): ")
        if proceed.lower() == 'y':
            series_list = list(self.HOUSING_CPI_SERIES.keys())
            self.get_series_data(series_list)

    def explore_construction_employment(self) -> None:
        """Explore construction employment series"""
        print("\n" + "=" * 80)
        print("👷 CONSTRUCTION EMPLOYMENT")
        print("=" * 80)

        print("\nAvailable Series:")
        for series_id, desc in self.CONSTRUCTION_EMPLOYMENT.items():
            print(f"  {series_id}: {desc}")

        if not self.check_api_key():
            return

        proceed = input("\nFetch data? (y/n): ")
        if proceed.lower() == 'y':
            series_list = list(self.CONSTRUCTION_EMPLOYMENT.keys())
            self.get_series_data(series_list)

    def explore_construction_ppi(self) -> None:
        """Explore construction Producer Price Index"""
        print("\n" + "=" * 80)
        print("🏗️  CONSTRUCTION PPI (Producer Price Index)")
        print("=" * 80)

        print("\nAvailable Series:")
        for series_id, desc in self.CONSTRUCTION_PPI.items():
            print(f"  {series_id}: {desc}")

        if not self.check_api_key():
            return

        proceed = input("\nFetch data? (y/n): ")
        if proceed.lower() == 'y':
            series_list = list(self.CONSTRUCTION_PPI.keys())
            self.get_series_data(series_list)

    def show_series_id_format(self) -> None:
        """Explain BLS series ID format"""
        print("\n" + "=" * 80)
        print("📖 BLS SERIES ID FORMAT GUIDE")
        print("=" * 80)

        print("\nCPI Series ID Format: CUUR0000SA0")
        print("  CU = CPI for All Urban Consumers (CPI-U)")
        print("  U = Not seasonally adjusted")
        print("  R = Regular monthly publication")
        print("  0000 = U.S. city average")
        print("  SA0 = All items")

        print("\nCES Series ID Format: CEU2023600001")
        print("  CES = Current Employment Statistics")
        print("  20 = Industry code (Construction)")
        print("  236 = Detailed industry (Construction of buildings)")
        print("  00001 = Data type (All employees, in thousands)")

        print("\nCommon Data Type Codes:")
        print("  00001 = All employees")
        print("  00003 = Average hourly earnings")
        print("  00006 = Average weekly hours")
        print("  00011 = Average weekly earnings")

    def show_capabilities_summary(self) -> None:
        """Display comprehensive summary"""
        print("\n" + "=" * 80)
        print("BLS API - REAL ESTATE CAPABILITIES")
        print("=" * 80)

        print("\n📊 DATA COVERAGE:")
        print("  • Employment and unemployment data")
        print("  • Wages and earnings by industry")
        print("  • Consumer Price Index (CPI)")
        print("  • Producer Price Index (PPI)")
        print("  • Historical data (varies by series, often 20+ years)")

        print("\n🏠 HOUSING-RELATED DATA:")
        print("  • Housing component of CPI")
        print("  • Rent of primary residence")
        print("  • Owners' equivalent rent")
        print("  • Household furnishings and operations")

        print("\n🏗️  CONSTRUCTION DATA:")
        print("  • Construction employment by sector")
        print("  • Construction wages and earnings")
        print("  • Construction material costs (PPI)")
        print("  • Building construction prices")

        print("\n🏢 REAL ESTATE INDUSTRY:")
        print("  • Real estate employment")
        print("  • Real estate wages")
        print("  • Property management employment")

        print("\n💰 API LIMITS:")
        print("  Unregistered (V1):")
        print("    • 25 queries/day")
        print("    • 25 series/query")
        print("    • 10 years/query")
        print("  Registered (V2):")
        print("    • 500 queries/day")
        print("    • 50 series/query")
        print("    • 20 years/query")

        print("\n🎯 REAL ESTATE USE CASES:")
        print("  ✓ Cost Analysis: Track construction material and labor costs")
        print("  ✓ Rent Trends: Monitor rental price inflation")
        print("  ✓ Employment: Construction and real estate job trends")
        print("  ✓ Operating Expenses: Utilities, maintenance cost inflation")
        print("  ✓ Investment Analysis: Inflation-adjusted valuations")

        print("\n" + "=" * 80)

    def export_all_series_ids(self, output_file: str = None) -> None:
        """Export all real estate series IDs to JSON"""
        if output_file is None:
            output_file = f"bls_series_ids_{datetime.now().strftime('%Y%m%d')}.json"

        all_series = {
            'housing_cpi': self.HOUSING_CPI_SERIES,
            'construction_employment': self.CONSTRUCTION_EMPLOYMENT,
            'construction_ppi': self.CONSTRUCTION_PPI,
            'real_estate_services': self.REAL_ESTATE_SERVICES,
            'wages_earnings': self.WAGES_EARNINGS,
        }

        with open(output_file, 'w') as f:
            json.dump(all_series, f, indent=2)

        print(f"\n✓ Series IDs exported to: {output_file}")


def main():
    """Run BLS API exploration"""
    print(f"\n🔍 BLS API Explorer")
    print(f"📅 Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    explorer = BLSAPIExplorer()

    # Show capabilities
    explorer.show_capabilities_summary()

    # Show series ID format
    print("\n\n" + "="*80)
    input("Press Enter to see Series ID format guide...")
    explorer.show_series_id_format()

    # Explore categories
    print("\n\n" + "="*80)
    input("Press Enter to explore Housing CPI...")
    explorer.explore_housing_cpi()

    print("\n\n" + "="*80)
    input("Press Enter to explore Construction Employment...")
    explorer.explore_construction_employment()

    print("\n\n" + "="*80)
    input("Press Enter to explore Construction PPI...")
    explorer.explore_construction_ppi()

    # Export series IDs
    print("\n\n" + "="*80)
    export = input("\nExport all series IDs to JSON? (y/n): ")
    if export.lower() == 'y':
        explorer.export_all_series_ids()

    # Test with API key
    print("\n\n" + "="*80)
    has_key = input("\nDo you have a BLS API key for full access? (y/n): ")
    if has_key.lower() == 'y':
        api_key = input("Enter your BLS API key: ")
        explorer = BLSAPIExplorer(api_key=api_key)

        # Test request
        print("\nTesting API with key...")
        test_series = ['CUUR0000SAH1', 'CEU2023600001']
        explorer.get_series_data(test_series, start_year=2020)

    else:
        print("\nℹ️  Register for free API key at:")
        print("   https://data.bls.gov/registrationEngine/")

    print("\n✅ Exploration complete!\n")


if __name__ == "__main__":
    main()
