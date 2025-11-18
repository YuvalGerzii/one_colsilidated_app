#!/usr/bin/env python3
"""
EPA Envirofacts API Explorer
Explores environmental hazards, Superfund sites, and property risk data
"""

import requests
import json
from typing import Dict, List, Optional
from datetime import datetime


class EPAAPIExplorer:
    """Explore EPA Envirofacts API for environmental risk data"""

    BASE_URL = "https://data.epa.gov/efservice"

    # No API key required for EPA Envirofacts

    # Available data models
    DATA_MODELS = {
        'SEMS': 'Superfund Enterprise Management System',
        'TRI': 'Toxic Release Inventory',
        'AQS': 'Air Quality System',
        'SDWIS': 'Safe Drinking Water Information System',
        'RAD': 'Radiation Information',
        'GHG': 'Greenhouse Gas Reporting',
    }

    # SEMS (Superfund) key fields
    SEMS_FIELDS = [
        'SITE_ID', 'SITE_NAME', 'ADDRESS', 'CITY', 'STATE', 'ZIP_CODE',
        'LATITUDE', 'LONGITUDE', 'NPL_STATUS', 'LISTING_DATE',
        'FEDERAL_FACILITY', 'SITE_LISTING_NARRATIVE'
    ]

    def __init__(self):
        """Initialize EPA API explorer"""
        pass

    def search_superfund_sites(self, state: str = None, city: str = None,
                               zip_code: str = None, limit: int = 10) -> List[Dict]:
        """
        Search for Superfund sites by location
        Returns sites from SEMS database
        """
        print(f"\n{'='*80}")
        print(f"SUPERFUND SITES SEARCH")
        print('='*80)

        # Build query URL
        query_parts = []

        if state:
            query_parts.append(f"STATE/{state}")
        if city:
            query_parts.append(f"CITY/{city}")
        if zip_code:
            query_parts.append(f"ZIP_CODE/{zip_code}")

        query = '/'.join(query_parts) if query_parts else ''
        url = f"{self.BASE_URL}/SEMS/{query}/ROWS/0:{limit}/JSON"

        print(f"\nQuery URL: {url}")
        print(f"Filters: State={state}, City={city}, ZIP={zip_code}")

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            if isinstance(data, list):
                print(f"\n✓ Found {len(data)} Superfund sites")

                for i, site in enumerate(data[:limit], 1):
                    print(f"\n{i}. {site.get('SITE_NAME', 'N/A')}")
                    print(f"   Address: {site.get('ADDRESS', 'N/A')}, "
                          f"{site.get('CITY', 'N/A')}, {site.get('STATE', 'N/A')} "
                          f"{site.get('ZIP_CODE', 'N/A')}")
                    print(f"   Site ID: {site.get('SITE_ID', 'N/A')}")
                    print(f"   NPL Status: {site.get('NPL_STATUS', 'N/A')}")
                    print(f"   Listing Date: {site.get('LISTING_DATE', 'N/A')}")

                    if site.get('LATITUDE') and site.get('LONGITUDE'):
                        print(f"   Coordinates: {site.get('LATITUDE')}, {site.get('LONGITUDE')}")

                return data
            else:
                print("\n✗ No sites found or unexpected response format")
                return []

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return []

    def get_site_details(self, site_id: str) -> Dict:
        """Get detailed information for a specific Superfund site"""
        url = f"{self.BASE_URL}/SEMS/SITE_ID/{site_id}/JSON"

        print(f"\n{'='*80}")
        print(f"SITE DETAILS - {site_id}")
        print('='*80)

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            if isinstance(data, list) and data:
                site = data[0]

                print(f"\nSite Name: {site.get('SITE_NAME', 'N/A')}")
                print(f"Site ID: {site.get('SITE_ID', 'N/A')}")
                print(f"\nLocation:")
                print(f"  Address: {site.get('ADDRESS', 'N/A')}")
                print(f"  City: {site.get('CITY', 'N/A')}")
                print(f"  State: {site.get('STATE', 'N/A')}")
                print(f"  ZIP: {site.get('ZIP_CODE', 'N/A')}")
                print(f"  County: {site.get('COUNTY', 'N/A')}")

                if site.get('LATITUDE') and site.get('LONGITUDE'):
                    print(f"\nCoordinates: {site.get('LATITUDE')}, {site.get('LONGITUDE')}")

                print(f"\nStatus:")
                print(f"  NPL Status: {site.get('NPL_STATUS', 'N/A')}")
                print(f"  Listing Date: {site.get('LISTING_DATE', 'N/A')}")
                print(f"  Federal Facility: {site.get('FEDERAL_FACILITY', 'N/A')}")

                if site.get('SITE_LISTING_NARRATIVE'):
                    print(f"\nDescription:")
                    print(f"  {site.get('SITE_LISTING_NARRATIVE')[:500]}")

                return site

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return {}

    def search_toxic_release_inventory(self, state: str, limit: int = 10) -> List[Dict]:
        """
        Search TRI (Toxic Release Inventory) facilities
        Shows chemical releases from industrial facilities
        """
        url = f"{self.BASE_URL}/TRI_FACILITY/STATE_ABBR/{state}/ROWS/0:{limit}/JSON"

        print(f"\n{'='*80}")
        print(f"TOXIC RELEASE INVENTORY - {state}")
        print('='*80)

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            if isinstance(data, list):
                print(f"\n✓ Found {len(data)} TRI facilities")

                for i, facility in enumerate(data[:limit], 1):
                    print(f"\n{i}. {facility.get('FACILITY_NAME', 'N/A')}")
                    print(f"   Location: {facility.get('CITY_NAME', 'N/A')}, {state}")
                    print(f"   TRI ID: {facility.get('TRI_FACILITY_ID', 'N/A')}")

                return data

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return []

    def search_by_coordinates(self, latitude: float, longitude: float,
                             radius_miles: float = 5) -> None:
        """
        Search for environmental sites near coordinates
        Note: EPA API doesn't directly support radius search,
        this is a conceptual example
        """
        print(f"\n{'='*80}")
        print(f"COORDINATE SEARCH (Conceptual)")
        print('='*80)
        print(f"\nLocation: {latitude}, {longitude}")
        print(f"Radius: {radius_miles} miles")
        print("\nNote: EPA Envirofacts API does not directly support radius search.")
        print("For geographic searches, you would need to:")
        print("  1. Query by state/county/ZIP")
        print("  2. Filter results by distance calculation")
        print("  3. Use EPA's FRS (Facility Registry Service) with geospatial features")

    def show_available_models(self) -> None:
        """Display all available EPA data models"""
        print("\n" + "=" * 80)
        print("📊 EPA ENVIROFACTS DATA MODELS")
        print("=" * 80)

        for model, description in self.DATA_MODELS.items():
            print(f"\n{model}: {description}")

        print("\n" + "=" * 80)
        print("SUPERFUND (SEMS) FIELDS")
        print("=" * 80)

        print("\nAvailable Fields:")
        for field in self.SEMS_FIELDS:
            print(f"  • {field}")

    def show_query_examples(self) -> None:
        """Show example API queries"""
        print("\n" + "=" * 80)
        print("📖 EPA API QUERY EXAMPLES")
        print("=" * 80)

        examples = [
            {
                "description": "Get all Superfund sites in California",
                "url": f"{self.BASE_URL}/SEMS/STATE/CA/JSON"
            },
            {
                "description": "Get sites in specific ZIP code",
                "url": f"{self.BASE_URL}/SEMS/ZIP_CODE/90210/JSON"
            },
            {
                "description": "Get site by ID",
                "url": f"{self.BASE_URL}/SEMS/SITE_ID/0100091/JSON"
            },
            {
                "description": "Get TRI facilities in Texas",
                "url": f"{self.BASE_URL}/TRI_FACILITY/STATE_ABBR/TX/ROWS/0:10/JSON"
            },
            {
                "description": "Get drinking water violations in ZIP",
                "url": f"{self.BASE_URL}/SDWIS_VIOLATION/ZIP_CODE/10001/JSON"
            }
        ]

        for example in examples:
            print(f"\n{example['description']}:")
            print(f"  {example['url']}")

    def show_capabilities_summary(self) -> None:
        """Display comprehensive summary"""
        print("\n" + "=" * 80)
        print("EPA ENVIROFACTS API - REAL ESTATE CAPABILITIES")
        print("=" * 80)

        print("\n📊 DATA SOURCES:")
        print("  • Superfund Sites (SEMS)")
        print("  • Toxic Release Inventory (TRI)")
        print("  • Air Quality System (AQS)")
        print("  • Safe Drinking Water (SDWIS)")
        print("  • Radiation Information (RAD)")
        print("  • Greenhouse Gas Reporting (GHG)")

        print("\n🏭 SUPERFUND SITES (SEMS):")
        print("  • National Priorities List (NPL) sites")
        print("  • Site location and status")
        print("  • Contamination narrative")
        print("  • Cleanup progress")
        print("  • Federal facilities")

        print("\n☢️  TOXIC RELEASE INVENTORY:")
        print("  • Industrial facility locations")
        print("  • Chemical releases by facility")
        print("  • Release quantities and types")
        print("  • Historical release data")

        print("\n💧 DRINKING WATER DATA:")
        print("  • Public water system violations")
        print("  • Water quality issues")
        print("  • Contaminant levels")

        print("\n⚡ API CHARACTERISTICS:")
        print("  • No API key required")
        print("  • RESTful JSON API")
        print("  • Free and public access")
        print("  • Multiple output formats (JSON, XML, CSV)")

        print("\n🎯 REAL ESTATE USE CASES:")
        print("  ✓ Environmental Due Diligence: Check proximity to Superfund sites")
        print("  ✓ Risk Assessment: Identify environmental hazards")
        print("  ✓ Disclosure Requirements: Environmental issues affecting value")
        print("  ✓ Development Planning: Avoid contaminated areas")
        print("  ✓ Property Valuation: Factor in environmental liabilities")
        print("  ✓ Health & Safety: Water quality, air quality concerns")

        print("\n📍 GEOGRAPHIC SEARCH:")
        print("  • Search by state, city, county, ZIP code")
        print("  • Coordinate data available (lat/long)")
        print("  • Can calculate distance from properties")

        print("\n⚠️  LIMITATIONS:")
        print("  • No built-in radius/distance search")
        print("  • Must filter results client-side for proximity")
        print("  • Some fields may be incomplete")

        print("\n" + "=" * 80)


def main():
    """Run EPA API exploration"""
    print(f"\n🔍 EPA Envirofacts API Explorer")
    print(f"📅 Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    explorer = EPAAPIExplorer()

    # Show capabilities
    explorer.show_capabilities_summary()

    # Show data models
    print("\n\n" + "="*80)
    input("Press Enter to see available data models...")
    explorer.show_available_models()

    # Show query examples
    print("\n\n" + "="*80)
    input("Press Enter to see query examples...")
    explorer.show_query_examples()

    # Search Superfund sites
    print("\n\n" + "="*80)
    search = input("\nSearch for Superfund sites? (y/n): ")
    if search.lower() == 'y':
        state = input("Enter state code (e.g., CA, NY, TX): ")
        explorer.search_superfund_sites(state=state.upper(), limit=5)

        # Get site details
        details = input("\nGet details for a specific site? (y/n): ")
        if details.lower() == 'y':
            site_id = input("Enter Site ID: ")
            explorer.get_site_details(site_id)

    # Search TRI
    print("\n\n" + "="*80)
    tri_search = input("\nSearch Toxic Release Inventory? (y/n): ")
    if tri_search.lower() == 'y':
        state = input("Enter state code: ")
        explorer.search_toxic_release_inventory(state.upper())

    print("\n✅ Exploration complete!\n")
    print("ℹ️  For more information visit:")
    print("   https://www.epa.gov/enviro/envirofacts-data-service-api")


if __name__ == "__main__":
    main()
