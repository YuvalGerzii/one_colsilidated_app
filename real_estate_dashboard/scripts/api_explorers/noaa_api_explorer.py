#!/usr/bin/env python3
"""
NOAA Climate Data API Explorer
Explores weather, climate, and flood risk data
"""

import requests
import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta


class NOAAAPIExplorer:
    """Explore NOAA Climate Data API for weather and climate risk"""

    BASE_URL = "https://www.ncdc.noaa.gov/cdo-web/api/v2"
    API_KEY = "YOUR_NOAA_API_KEY"  # Get free key at https://www.ncdc.noaa.gov/cdo-web/token

    # Available datasets
    DATASETS = {
        'GHCND': 'Global Historical Climatology Network - Daily',
        'GSOM': 'Global Summary of the Month',
        'GSOY': 'Global Summary of the Year',
        'NEXRAD2': 'Weather Radar (Level II)',
        'NEXRAD3': 'Weather Radar (Level III)',
        'NORMAL_ANN': 'Normals Annual/Seasonal',
        'NORMAL_MLY': 'Normals Monthly',
        'PRECIP_15': 'Precipitation 15 Minute',
        'PRECIP_HLY': 'Precipitation Hourly',
    }

    # Common data types
    DATA_TYPES = {
        'PRCP': 'Precipitation (mm or inches)',
        'SNOW': 'Snowfall (mm)',
        'SNWD': 'Snow depth (mm)',
        'TMAX': 'Maximum temperature',
        'TMIN': 'Minimum temperature',
        'TAVG': 'Average temperature',
        'AWND': 'Average wind speed',
        'WSF2': 'Fastest 2-minute wind speed',
        'WT01': 'Fog, ice fog, or freezing fog',
        'WT03': 'Thunder',
        'WT04': 'Ice pellets, sleet, snow pellets',
        'WT05': 'Hail',
        'WT08': 'Smoke or haze',
    }

    def __init__(self, api_key: Optional[str] = None):
        """Initialize NOAA API explorer"""
        if api_key:
            self.API_KEY = api_key

    def check_api_key(self) -> bool:
        """Verify API key is configured"""
        if self.API_KEY == "YOUR_NOAA_API_KEY":
            print("\n⚠️  WARNING: Using placeholder API key")
            print("   Get free key at: https://www.ncdc.noaa.gov/cdo-web/token")
            print("\n   API Limits:")
            print("   • 5 requests per second")
            print("   • 10,000 requests per day")
            return False
        return True

    def get_headers(self) -> Dict:
        """Get API headers with token"""
        return {
            'token': self.API_KEY
        }

    def get_datasets(self) -> List[Dict]:
        """Get all available datasets"""
        url = f"{self.BASE_URL}/datasets"

        print(f"\n{'='*80}")
        print(f"AVAILABLE NOAA DATASETS")
        print('='*80)

        if not self.check_api_key():
            print("\nDataset IDs (requires API key to fetch details):")
            for dataset_id, name in self.DATASETS.items():
                print(f"  {dataset_id}: {name}")
            return []

        try:
            response = requests.get(url, headers=self.get_headers(), timeout=10)
            response.raise_for_status()
            data = response.json()

            datasets = data.get('results', [])
            print(f"\nFound {len(datasets)} datasets")

            for dataset in datasets:
                print(f"\n{dataset.get('id', 'N/A')}")
                print(f"  Name: {dataset.get('name', 'N/A')}")
                print(f"  Coverage: {dataset.get('mindate', 'N/A')} to {dataset.get('maxdate', 'N/A')}")

            return datasets

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return []

    def search_locations(self, location_category: str = "CITY",
                        limit: int = 10, offset: int = 0) -> List[Dict]:
        """
        Search for locations
        Categories: CITY, ST (state), CNTRY (country), ZIP
        """
        url = f"{self.BASE_URL}/locations"
        params = {
            'locationcategoryid': location_category,
            'limit': limit,
            'offset': offset
        }

        print(f"\n{'='*80}")
        print(f"LOCATIONS - {location_category}")
        print('='*80)

        if not self.check_api_key():
            return []

        try:
            response = requests.get(url, params=params, headers=self.get_headers(), timeout=10)
            response.raise_for_status()
            data = response.json()

            locations = data.get('results', [])
            print(f"\nFound {len(locations)} locations")

            for loc in locations[:limit]:
                print(f"\n{loc.get('id', 'N/A')}: {loc.get('name', 'N/A')}")
                print(f"  Coverage: {loc.get('mindate', 'N/A')} to {loc.get('maxdate', 'N/A')}")

            return locations

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return []

    def get_weather_stations(self, location_id: str = None, limit: int = 10) -> List[Dict]:
        """Get weather stations, optionally filtered by location"""
        url = f"{self.BASE_URL}/stations"
        params = {
            'limit': limit
        }

        if location_id:
            params['locationid'] = location_id

        print(f"\n{'='*80}")
        print(f"WEATHER STATIONS")
        print('='*80)

        if not self.check_api_key():
            return []

        try:
            response = requests.get(url, params=params, headers=self.get_headers(), timeout=10)
            response.raise_for_status()
            data = response.json()

            stations = data.get('results', [])
            print(f"\nFound {len(stations)} stations")

            for station in stations:
                print(f"\n{station.get('id', 'N/A')}: {station.get('name', 'N/A')}")
                print(f"  Location: {station.get('latitude', 'N/A')}, {station.get('longitude', 'N/A')}")
                print(f"  Elevation: {station.get('elevation', 'N/A')} m")
                print(f"  Coverage: {station.get('mindate', 'N/A')} to {station.get('maxdate', 'N/A')}")

            return stations

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return []

    def get_climate_data(self, dataset_id: str = 'GHCND', location_id: str = None,
                        start_date: str = None, end_date: str = None,
                        limit: int = 25) -> List[Dict]:
        """
        Get climate data observations
        """
        if not start_date:
            start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')

        url = f"{self.BASE_URL}/data"
        params = {
            'datasetid': dataset_id,
            'startdate': start_date,
            'enddate': end_date,
            'limit': limit,
            'units': 'standard'  # Use standard units
        }

        if location_id:
            params['locationid'] = location_id

        print(f"\n{'='*80}")
        print(f"CLIMATE DATA: {dataset_id}")
        print('='*80)
        print(f"Period: {start_date} to {end_date}")

        if not self.check_api_key():
            return []

        try:
            response = requests.get(url, params=params, headers=self.get_headers(), timeout=10)
            response.raise_for_status()
            data = response.json()

            observations = data.get('results', [])
            print(f"\n✓ Retrieved {len(observations)} observations")

            # Show sample data
            for obs in observations[:5]:
                print(f"\n{obs.get('date', 'N/A')} - {obs.get('datatype', 'N/A')}")
                print(f"  Station: {obs.get('station', 'N/A')}")
                print(f"  Value: {obs.get('value', 'N/A')}")

            return observations

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return []

    def show_data_types(self) -> None:
        """Display common data types"""
        print("\n" + "=" * 80)
        print("📊 COMMON CLIMATE DATA TYPES")
        print("=" * 80)

        print("\nTemperature:")
        print("  TMAX, TMIN, TAVG - Maximum, Minimum, Average temperature")

        print("\nPrecipitation:")
        print("  PRCP - Precipitation")
        print("  SNOW - Snowfall")
        print("  SNWD - Snow depth")

        print("\nWind:")
        print("  AWND - Average wind speed")
        print("  WSF2 - Fastest 2-minute wind speed")

        print("\nWeather Events:")
        print("  WT01 - Fog")
        print("  WT03 - Thunder")
        print("  WT04 - Ice pellets/sleet")
        print("  WT05 - Hail")
        print("  WT08 - Smoke/haze")

    def show_capabilities_summary(self) -> None:
        """Display comprehensive summary"""
        print("\n" + "=" * 80)
        print("NOAA CLIMATE DATA API - REAL ESTATE CAPABILITIES")
        print("=" * 80)

        print("\n📊 DATA COVERAGE:")
        print("  • Global weather and climate data")
        print("  • Historical data back to 1763 (varies by location)")
        print("  • Daily, monthly, annual summaries")
        print("  • Real-time weather observations")

        print("\n🌡️  CLIMATE DATA:")
        print("  • Temperature (min, max, average)")
        print("  • Precipitation and snowfall")
        print("  • Wind speed and direction")
        print("  • Severe weather events")
        print("  • Climate normals (30-year averages)")

        print("\n🌪️  EXTREME WEATHER:")
        print("  • Storm events database (1950+)")
        print("  • Floods, hurricanes, tornadoes")
        print("  • Damage assessments")
        print("  • Event locations and tracks")

        print("\n📍 GEOGRAPHIC COVERAGE:")
        print("  • Weather stations worldwide")
        print("  • Location by city, state, ZIP, country")
        print("  • Coordinate-based searches")
        print("  • Station metadata (lat/long, elevation)")

        print("\n⚡ API CHARACTERISTICS:")
        print("  • Free API key required")
        print("  • Rate limit: 5 requests/second")
        print("  • Daily limit: 10,000 requests")
        print("  • JSON format responses")

        print("\n🎯 REAL ESTATE USE CASES:")
        print("  ✓ Climate Risk Assessment: Historical flood/storm frequency")
        print("  ✓ Insurance Underwriting: Weather event history")
        print("  ✓ Development Planning: Flood zones, extreme weather")
        print("  ✓ Property Valuation: Climate-related risks")
        print("  ✓ Long-term Investment: Climate change impacts")
        print("  ✓ Due Diligence: Weather pattern analysis")

        print("\n📈 CLIMATE RISK METRICS:")
        print("  • Flood frequency and severity")
        print("  • Hurricane/tornado exposure")
        print("  • Extreme temperature events")
        print("  • Precipitation trends")
        print("  • Sea level rise (coastal areas)")

        print("\n" + "=" * 80)


def main():
    """Run NOAA API exploration"""
    print(f"\n🔍 NOAA Climate Data API Explorer")
    print(f"📅 Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    explorer = NOAAAPIExplorer()

    # Show capabilities
    explorer.show_capabilities_summary()

    # Show data types
    print("\n\n" + "="*80)
    input("Press Enter to see common data types...")
    explorer.show_data_types()

    # Check for API key
    print("\n\n" + "="*80)
    has_key = input("\nDo you have a NOAA API key? (y/n): ")

    if has_key.lower() == 'y':
        api_key = input("Enter your NOAA API key: ")
        explorer = NOAAAPIExplorer(api_key=api_key)

        # Get datasets
        print("\n" + "="*80)
        datasets = input("\nFetch available datasets? (y/n): ")
        if datasets.lower() == 'y':
            explorer.get_datasets()

        # Search locations
        print("\n" + "="*80)
        locations = input("\nSearch locations? (y/n): ")
        if locations.lower() == 'y':
            category = input("Category (CITY/ST/ZIP): ")
            explorer.search_locations(category.upper())

        # Get weather stations
        print("\n" + "="*80)
        stations = input("\nGet weather stations? (y/n): ")
        if stations.lower() == 'y':
            explorer.get_weather_stations()

        # Get climate data
        print("\n" + "="*80)
        climate = input("\nGet climate data sample? (y/n): ")
        if climate.lower() == 'y':
            explorer.get_climate_data()

    else:
        print("\nℹ️  Request free API token at:")
        print("   https://www.ncdc.noaa.gov/cdo-web/token")
        print("   Token will be emailed to you immediately")

    print("\n✅ Exploration complete!\n")
    print("ℹ️  Additional NOAA resources:")
    print("   • Storm Events Database: https://www.ncdc.noaa.gov/stormevents/")
    print("   • Climate Data Online: https://www.ncdc.noaa.gov/cdo-web/")


if __name__ == "__main__":
    main()
