#!/usr/bin/env python3
"""
HUD USER API Explorer
Explores Fair Market Rents, Income Limits, and Housing Data from HUD
"""

import requests
import json
from typing import Dict, List, Optional
from datetime import datetime


class HUDAPIExplorer:
    """Explore HUD USER API for housing data"""

    BASE_URL = "https://www.huduser.gov/hudapi/public"
    API_KEY = "YOUR_HUD_API_KEY"  # Get free key at https://www.huduser.gov/hudapi/public/register

    # State FIPS codes for reference
    STATE_FIPS = {
        '06': 'California',
        '36': 'New York',
        '48': 'Texas',
        '12': 'Florida',
        '17': 'Illinois',
        '42': 'Pennsylvania',
    }

    def __init__(self, api_key: Optional[str] = None):
        """Initialize explorer with optional API key"""
        if api_key:
            self.API_KEY = api_key

    def check_api_key(self) -> bool:
        """Verify API key is configured"""
        if self.API_KEY == "YOUR_HUD_API_KEY":
            print("\n⚠️  WARNING: Using placeholder API key")
            print("   Register for free key at: https://www.huduser.gov/hudapi/public/register")
            return False
        return True

    def get_headers(self) -> Dict:
        """Get authorization headers"""
        return {
            'Authorization': f'Bearer {self.API_KEY}',
            'Content-Type': 'application/json'
        }

    def get_fair_market_rents(self, zip_code: str, year: int = None) -> Dict:
        """
        Get Fair Market Rents for a ZIP code
        FMRs are used to determine payment standard amounts for HUD Programs
        """
        if year is None:
            year = datetime.now().year

        url = f"{self.BASE_URL}/fmr/data/{zip_code}"
        params = {'year': year}

        print(f"\n{'='*80}")
        print(f"FAIR MARKET RENTS - ZIP {zip_code} ({year})")
        print('='*80)

        if not self.check_api_key():
            return {}

        try:
            response = requests.get(url, params=params, headers=self.get_headers(), timeout=10)
            response.raise_for_status()
            data = response.json()

            if 'data' in data and 'basicdata' in data['data']:
                fmr_data = data['data']['basicdata']

                print(f"\nArea Name: {fmr_data.get('areaname', 'N/A')}")
                print(f"Metro Code: {fmr_data.get('metro_code', 'N/A')}")
                print(f"FMR Type: {fmr_data.get('fmr_type', 'N/A')}")
                print(f"\nFair Market Rents:")
                print(f"  Efficiency: ${fmr_data.get('fmr_0', 'N/A')}")
                print(f"  1-Bedroom:  ${fmr_data.get('fmr_1', 'N/A')}")
                print(f"  2-Bedroom:  ${fmr_data.get('fmr_2', 'N/A')}")
                print(f"  3-Bedroom:  ${fmr_data.get('fmr_3', 'N/A')}")
                print(f"  4-Bedroom:  ${fmr_data.get('fmr_4', 'N/A')}")

                return data['data']

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
        return {}

    def get_income_limits(self, state_code: str, year: int = None) -> Dict:
        """
        Get HUD Income Limits by state
        Income limits determine eligibility for HUD programs
        """
        if year is None:
            year = datetime.now().year

        url = f"{self.BASE_URL}/il/data/{state_code}"
        params = {'year': year}

        print(f"\n{'='*80}")
        print(f"INCOME LIMITS - {self.STATE_FIPS.get(state_code, state_code)} ({year})")
        print('='*80)

        if not self.check_api_key():
            return {}

        try:
            response = requests.get(url, params=params, headers=self.get_headers(), timeout=10)
            response.raise_for_status()
            data = response.json()

            if 'data' in data and 'incomes' in data['data']:
                print(f"\nFound {len(data['data']['incomes'])} income limit records")

                # Show first few examples
                for i, record in enumerate(data['data']['incomes'][:3]):
                    print(f"\n{record.get('areaname', 'N/A')}:")
                    print(f"  Median Family Income: ${record.get('median_family_income', 'N/A')}")
                    print(f"  Very Low Income (50% MFI): ${record.get('very_low_income_limit_1', 'N/A')} (1 person)")
                    print(f"  Low Income (80% MFI): ${record.get('low_income_limit_1', 'N/A')} (1 person)")
                    print(f"  Extremely Low (30% MFI): ${record.get('extremely_low_income_limit_1', 'N/A')} (1 person)")

                return data['data']

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
        return {}

    def get_usps_crosswalk(self, zip_code: str) -> Dict:
        """
        Get USPS ZIP Code to Census Tract crosswalk
        Maps ZIP codes to Census geographic identifiers
        """
        url = f"{self.BASE_URL}/usps"
        params = {
            'type': '1',  # Type 1: ZIP to Tract
            'query': zip_code
        }

        print(f"\n{'='*80}")
        print(f"USPS CROSSWALK - ZIP {zip_code}")
        print('='*80)

        if not self.check_api_key():
            return {}

        try:
            response = requests.get(url, params=params, headers=self.get_headers(), timeout=10)
            response.raise_for_status()
            data = response.json()

            if 'data' in data and 'results' in data['data']:
                results = data['data']['results']
                print(f"\nFound {len(results)} census tracts")

                for result in results[:5]:
                    print(f"\nTract: {result.get('tract', 'N/A')}")
                    print(f"  County: {result.get('county', 'N/A')}")
                    print(f"  Residential Ratio: {result.get('res_ratio', 'N/A')}")
                    print(f"  Business Ratio: {result.get('bus_ratio', 'N/A')}")

                return data['data']

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
        return {}

    def explore_fmr_history(self, zip_code: str, years: int = 5) -> List[Dict]:
        """Get historical Fair Market Rents"""
        current_year = datetime.now().year
        history = []

        print(f"\n{'='*80}")
        print(f"FMR HISTORICAL TRENDS - ZIP {zip_code}")
        print('='*80)

        if not self.check_api_key():
            return []

        for year in range(current_year - years, current_year + 1):
            try:
                data = self.get_fair_market_rents(zip_code, year)
                if data and 'basicdata' in data:
                    history.append({
                        'year': year,
                        'data': data['basicdata']
                    })
            except Exception as e:
                print(f"  {year}: Error - {e}")

        # Show trends
        if history:
            print(f"\n2-Bedroom FMR Trend:")
            for record in history:
                year = record['year']
                fmr_2 = record['data'].get('fmr_2', 'N/A')
                print(f"  {year}: ${fmr_2}")

        return history

    def show_available_datasets(self) -> None:
        """Display all available HUD datasets"""
        print("\n" + "=" * 80)
        print("HUD USER API - AVAILABLE DATASETS")
        print("=" * 80)

        datasets = {
            "Fair Market Rents (FMR)": {
                "endpoint": "/fmr/data/{zip}",
                "description": "Fair Market Rents used for Section 8 Housing Choice Voucher program",
                "fields": [
                    "fmr_0, fmr_1, fmr_2, fmr_3, fmr_4 (by bedroom count)",
                    "areaname, metro_code",
                    "fmr_type (40th or 50th percentile)"
                ],
                "history": "1983-present",
                "geography": "ZIP codes, counties, metropolitan areas"
            },
            "Income Limits": {
                "endpoint": "/il/data/{state}",
                "description": "Income limits for HUD programs by area",
                "fields": [
                    "median_family_income",
                    "very_low_income_limit (50% MFI)",
                    "low_income_limit (80% MFI)",
                    "extremely_low_income_limit (30% MFI)",
                    "Limits by household size (1-8 persons)"
                ],
                "history": "1998-present",
                "geography": "Metropolitan areas, counties"
            },
            "USPS Crosswalk": {
                "endpoint": "/usps",
                "description": "ZIP Code to Census geography crosswalk",
                "fields": [
                    "ZIP to Tract",
                    "ZIP to County",
                    "ZIP to CBSA",
                    "Residential/Business ratios"
                ],
                "history": "Quarterly updates",
                "geography": "All US ZIP codes"
            },
            "CHAS (Comprehensive Housing Affordability Strategy)": {
                "endpoint": "/chas",
                "description": "Housing needs and market conditions",
                "fields": [
                    "Housing problems (cost burden, overcrowding, etc.)",
                    "Income levels and housing tenure",
                    "Household demographics"
                ],
                "history": "Based on ACS 5-year estimates",
                "geography": "States, counties, places"
            }
        }

        for name, info in datasets.items():
            print(f"\n{name}")
            print(f"  Endpoint: {info['endpoint']}")
            print(f"  Description: {info['description']}")
            print(f"  Historical Data: {info['history']}")
            print(f"  Geographic Coverage: {info['geography']}")
            print(f"  Key Fields:")
            for field in info['fields']:
                print(f"    • {field}")

    def show_capabilities_summary(self) -> None:
        """Display comprehensive summary"""
        print("\n" + "=" * 80)
        print("HUD USER API - REAL ESTATE CAPABILITIES")
        print("=" * 80)

        print("\n📊 DATA SOURCES:")
        print("  • Fair Market Rents (1983-present)")
        print("  • Income Limits (1998-present)")
        print("  • USPS Geographic Crosswalks (quarterly)")
        print("  • CHAS Housing Affordability Data")

        print("\n💰 FAIR MARKET RENT DATA:")
        print("  • Rent standards by bedroom count (0-4 bedrooms)")
        print("  • Updated annually")
        print("  • ZIP code, county, and metro area level")
        print("  • 40th and 50th percentile rents")
        print("  • Used for Section 8 voucher program")

        print("\n👥 INCOME LIMIT DATA:")
        print("  • Median Family Income (MFI)")
        print("  • Very Low Income (50% MFI)")
        print("  • Low Income (80% MFI)")
        print("  • Extremely Low Income (30% MFI)")
        print("  • By household size (1-8 persons)")

        print("\n🗺️  GEOGRAPHIC TOOLS:")
        print("  • ZIP to Census Tract mapping")
        print("  • ZIP to County mapping")
        print("  • ZIP to CBSA (Metro area) mapping")
        print("  • Residential/business address ratios")

        print("\n🏡 REAL ESTATE USE CASES:")
        print("  ✓ Rent Analysis: Compare market rents to HUD FMRs")
        print("  ✓ Affordable Housing: Determine income qualification")
        print("  ✓ Market Research: Geographic crosswalks for analysis")
        print("  ✓ Subsidy Programs: Section 8 rent calculations")
        print("  ✓ Investment Screening: Identify underserved markets")
        print("  ✓ Policy Analysis: Track rent and income trends")

        print("\n" + "=" * 80)


def main():
    """Run HUD API exploration"""
    print(f"\n🔍 HUD USER API Explorer")
    print(f"📅 Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    explorer = HUDAPIExplorer()

    # Show capabilities
    explorer.show_capabilities_summary()

    # Show datasets
    print("\n\n" + "="*80)
    input("Press Enter to see available datasets...")
    explorer.show_available_datasets()

    # Check for API key
    print("\n\n" + "="*80)
    has_key = input("\nDo you have a HUD API key? (y/n): ")

    if has_key.lower() == 'y':
        api_key = input("Enter your HUD API key: ")
        explorer = HUDAPIExplorer(api_key=api_key)

        # Test Fair Market Rents
        print("\n" + "="*80)
        test_fmr = input("\nTest Fair Market Rents? (y/n): ")
        if test_fmr.lower() == 'y':
            zip_code = input("Enter ZIP code (e.g., 90210): ")
            explorer.get_fair_market_rents(zip_code)

            # Historical trend
            history = input("\nGet 5-year historical trend? (y/n): ")
            if history.lower() == 'y':
                explorer.explore_fmr_history(zip_code)

        # Test Income Limits
        print("\n" + "="*80)
        test_il = input("\nTest Income Limits? (y/n): ")
        if test_il.lower() == 'y':
            print("\nState codes: 06=CA, 36=NY, 48=TX, 12=FL")
            state_code = input("Enter state FIPS code: ")
            explorer.get_income_limits(state_code)

        # Test USPS Crosswalk
        print("\n" + "="*80)
        test_usps = input("\nTest USPS Crosswalk? (y/n): ")
        if test_usps.lower() == 'y':
            zip_code = input("Enter ZIP code: ")
            explorer.get_usps_crosswalk(zip_code)

    else:
        print("\nℹ️  Register for free API key at:")
        print("   https://www.huduser.gov/hudapi/public/register")

    print("\n✅ Exploration complete!\n")


if __name__ == "__main__":
    main()
