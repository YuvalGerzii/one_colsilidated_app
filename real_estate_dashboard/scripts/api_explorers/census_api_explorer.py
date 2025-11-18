#!/usr/bin/env python3
"""
US Census Bureau API Explorer
Explores available datasets, variables, and fields relevant to real estate analysis
"""

import requests
import json
from typing import Dict, List, Optional
from datetime import datetime


class CensusAPIExplorer:
    """Explore US Census Bureau API for real estate data"""

    BASE_URL = "https://api.census.gov/data"

    # API key - replace with actual key or set as environment variable
    API_KEY = "YOUR_CENSUS_API_KEY"

    # Key real estate related variable groups
    HOUSING_VARIABLES = {
        'B25001_001E': 'Total Housing Units',
        'B25002_002E': 'Occupied Housing Units',
        'B25002_003E': 'Vacant Housing Units',
        'B25003_001E': 'Tenure Total',
        'B25003_002E': 'Owner Occupied',
        'B25003_003E': 'Renter Occupied',
        'B25077_001E': 'Median Home Value',
        'B25064_001E': 'Median Gross Rent',
        'B25034_001E': 'Year Structure Built',
        'B25024_001E': 'Units in Structure',
        'B25035_001E': 'Median Year Structure Built',
        'B25037_001E': 'Median Year Householder Moved In',
    }

    DEMOGRAPHIC_VARIABLES = {
        'B01003_001E': 'Total Population',
        'B01002_001E': 'Median Age',
        'B19013_001E': 'Median Household Income',
        'B19301_001E': 'Per Capita Income',
        'B17001_002E': 'Population Below Poverty Level',
        'B23025_005E': 'Unemployment',
        'B15003_022E': 'Bachelor\'s Degree',
        'B15003_023E': 'Master\'s Degree',
    }

    ECONOMIC_VARIABLES = {
        'B08303_001E': 'Travel Time to Work',
        'B08303_013E': 'Travel Time 60+ Minutes',
        'B25091_001E': 'Mortgage Status',
        'B25092_001E': 'Median Selected Monthly Owner Costs',
        'B25070_001E': 'Gross Rent as % of Household Income',
    }

    def __init__(self, api_key: Optional[str] = None):
        """Initialize explorer with optional API key"""
        if api_key:
            self.API_KEY = api_key

    def get_available_datasets(self) -> Dict:
        """Get list of all available Census datasets"""
        url = f"{self.BASE_URL}.json"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            print("=" * 80)
            print("AVAILABLE CENSUS DATASETS")
            print("=" * 80)

            # Filter for relevant datasets
            relevant = []
            for dataset in data.get('dataset', []):
                title = dataset.get('title', '')
                if any(keyword in title.lower() for keyword in
                       ['acs', 'american community', 'housing', 'economic']):
                    relevant.append(dataset)
                    print(f"\n{dataset.get('title')}")
                    print(f"  Identifier: {dataset.get('identifier')}")
                    print(f"  Description: {dataset.get('description', 'N/A')[:200]}")

            return relevant

        except requests.exceptions.RequestException as e:
            print(f"Error fetching datasets: {e}")
            return {}

    def get_acs5_variables(self, year: int = 2023) -> Dict:
        """Get all variables available in ACS 5-year survey"""
        url = f"{self.BASE_URL}/{year}/acs/acs5/variables.json"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            variables = response.json().get('variables', {})

            print("\n" + "=" * 80)
            print(f"ACS 5-YEAR VARIABLES ({year})")
            print("=" * 80)

            # Categorize variables
            housing_vars = {}
            demographic_vars = {}
            economic_vars = {}

            for var_code, var_info in variables.items():
                label = var_info.get('label', '').lower()

                if any(keyword in label for keyword in
                       ['housing', 'tenure', 'rent', 'value', 'units', 'rooms']):
                    housing_vars[var_code] = var_info.get('label')

                elif any(keyword in label for keyword in
                         ['income', 'poverty', 'employment', 'earnings', 'wage']):
                    economic_vars[var_code] = var_info.get('label')

                elif any(keyword in label for keyword in
                         ['population', 'age', 'household', 'family']):
                    demographic_vars[var_code] = var_info.get('label')

            print(f"\nTotal Variables: {len(variables)}")
            print(f"Housing Related: {len(housing_vars)}")
            print(f"Economic Related: {len(economic_vars)}")
            print(f"Demographic Related: {len(demographic_vars)}")

            # Show sample housing variables
            print("\nSample Housing Variables:")
            for i, (code, label) in enumerate(list(housing_vars.items())[:20]):
                print(f"  {code}: {label}")

            return {
                'housing': housing_vars,
                'economic': economic_vars,
                'demographic': demographic_vars
            }

        except requests.exceptions.RequestException as e:
            print(f"Error fetching variables: {e}")
            return {}

    def explore_geography_levels(self, year: int = 2023) -> None:
        """Show available geographic levels"""
        url = f"{self.BASE_URL}/{year}/acs/acs5/geography.json"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            geographies = response.json()

            print("\n" + "=" * 80)
            print("AVAILABLE GEOGRAPHIC LEVELS")
            print("=" * 80)

            for geo in geographies.get('fips', []):
                print(f"\n{geo.get('name')}")
                print(f"  Geolevels: {', '.join(geo.get('geoLevelDisplay', []))}")

        except requests.exceptions.RequestException as e:
            print(f"Error fetching geographies: {e}")

    def get_real_estate_data_sample(self, state_fips: str = "06", year: int = 2023) -> Dict:
        """
        Get sample real estate data for a state
        Default: California (FIPS 06)
        """
        # Combine all relevant variables
        variables = {**self.HOUSING_VARIABLES, **self.DEMOGRAPHIC_VARIABLES, **self.ECONOMIC_VARIABLES}
        var_codes = ','.join(['NAME'] + list(variables.keys()))

        url = f"{self.BASE_URL}/{year}/acs/acs5"
        params = {
            'get': var_codes,
            'for': 'county:*',
            'in': f'state:{state_fips}',
            'key': self.API_KEY
        }

        print("\n" + "=" * 80)
        print(f"SAMPLE DATA EXTRACTION - State FIPS: {state_fips}")
        print("=" * 80)
        print(f"\nEndpoint: {url}")
        print(f"Parameters: {params}")

        if self.API_KEY == "YOUR_CENSUS_API_KEY":
            print("\n⚠️  WARNING: Using placeholder API key. Get real key at:")
            print("   https://api.census.gov/data/key_signup.html")
            return {}

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Parse results
            headers = data[0]
            rows = data[1:]

            print(f"\nRetrieved {len(rows)} counties")
            print(f"\nFields returned: {len(headers)}")
            print(f"Headers: {headers[:5]}...")

            # Show first county as example
            if rows:
                print("\nSample County Data:")
                example = dict(zip(headers, rows[0]))
                for key, value in list(example.items())[:10]:
                    var_name = variables.get(key, key)
                    print(f"  {var_name}: {value}")

            return {
                'headers': headers,
                'data': rows,
                'variable_map': variables
            }

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return {}

    def export_variable_catalog(self, year: int = 2023, output_file: str = None) -> None:
        """Export comprehensive variable catalog to JSON"""
        if output_file is None:
            output_file = f"census_variables_{year}.json"

        url = f"{self.BASE_URL}/{year}/acs/acs5/variables.json"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            variables = response.json()

            with open(output_file, 'w') as f:
                json.dump(variables, f, indent=2)

            print(f"\n✓ Variable catalog exported to: {output_file}")

        except Exception as e:
            print(f"Error exporting catalog: {e}")

    def show_real_estate_summary(self) -> None:
        """Display comprehensive summary of real estate capabilities"""
        print("\n" + "=" * 80)
        print("CENSUS API - REAL ESTATE DATA CAPABILITIES")
        print("=" * 80)

        print("\n📊 KEY HOUSING METRICS:")
        for code, desc in self.HOUSING_VARIABLES.items():
            print(f"  {code}: {desc}")

        print("\n👥 DEMOGRAPHIC INDICATORS:")
        for code, desc in self.DEMOGRAPHIC_VARIABLES.items():
            print(f"  {code}: {desc}")

        print("\n💰 ECONOMIC INDICATORS:")
        for code, desc in self.ECONOMIC_VARIABLES.items():
            print(f"  {code}: {desc}")

        print("\n📈 AVAILABLE DATASETS:")
        print("  • ACS 5-Year (2009-2023): Most geographic detail")
        print("  • ACS 1-Year (2005-2024): Most current, large areas only")
        print("  • ACS 1-Year Supplemental (2014-2023): Medium populations")

        print("\n🗺️  GEOGRAPHIC LEVELS:")
        print("  • Nation")
        print("  • States")
        print("  • Counties")
        print("  • Metropolitan Statistical Areas (MSAs)")
        print("  • Places (Cities)")
        print("  • ZIP Code Tabulation Areas (ZCTAs)")
        print("  • Census Tracts")
        print("  • Block Groups")

        print("\n🏡 REAL ESTATE USE CASES:")
        print("  ✓ Market Analysis: Demographics, income, population trends")
        print("  ✓ Property Valuation: Comparable housing values and rents")
        print("  ✓ Investment Decisions: Economic indicators, employment")
        print("  ✓ Risk Assessment: Vacancy rates, tenure patterns")
        print("  ✓ Development Planning: Housing needs, demographic projections")

        print("\n" + "=" * 80)


def main():
    """Run comprehensive Census API exploration"""
    print(f"\n🔍 Census API Explorer")
    print(f"📅 Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    explorer = CensusAPIExplorer()

    # Show capabilities summary
    explorer.show_real_estate_summary()

    # Get available datasets
    print("\n\n" + "="*80)
    input("Press Enter to fetch available datasets...")
    explorer.get_available_datasets()

    # Get ACS 5-year variables
    print("\n\n" + "="*80)
    input("Press Enter to fetch ACS 5-Year variables...")
    explorer.get_acs5_variables(year=2023)

    # Show geography levels
    print("\n\n" + "="*80)
    input("Press Enter to fetch geography levels...")
    explorer.explore_geography_levels(year=2023)

    # Export variable catalog
    print("\n\n" + "="*80)
    export = input("Export full variable catalog to JSON? (y/n): ")
    if export.lower() == 'y':
        explorer.export_variable_catalog(year=2023)

    # Sample data extraction
    print("\n\n" + "="*80)
    print("\nNote: Actual data extraction requires API key")
    print("Get free key at: https://api.census.gov/data/key_signup.html")

    try_sample = input("\nTry sample data extraction? (requires API key) (y/n): ")
    if try_sample.lower() == 'y':
        api_key = input("Enter your Census API key (or press Enter to skip): ")
        if api_key:
            explorer = CensusAPIExplorer(api_key=api_key)
            explorer.get_real_estate_data_sample(state_fips="06", year=2023)

    print("\n✅ Exploration complete!\n")


if __name__ == "__main__":
    main()
