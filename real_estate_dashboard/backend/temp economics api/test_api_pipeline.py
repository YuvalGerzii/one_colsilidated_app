#!/usr/bin/env python3
"""
Economics API Test Script

Tests API connectivity, data fetching, and database storage.
Verifies the entire data pipeline works correctly.
"""

import sys
import os
import asyncio
import json
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(parent_dir))

import requests
from datetime import datetime


def test_api_connectivity(api_key: str = None):
    """Test basic API connectivity"""
    print("\n" + "=" * 80)
    print("TESTING API CONNECTIVITY")
    print("=" * 80 + "\n")

    base_url = "https://api.sugra.ai"

    # Test endpoints
    test_endpoints = [
        ("Countries List", f"{base_url}/v1/economics/countries"),
        ("US Overview", f"{base_url}/v1/economics/united-states/overview"),
        ("US GDP", f"{base_url}/v1/economics/united-states/gdp"),
    ]

    headers = {}
    if api_key and api_key != "your_api_key_here":
        headers['x-api-key'] = api_key
        print(f"✅ Using API key: {api_key[:8]}..." if len(api_key) > 8 else api_key)
    else:
        print("⚠️  No API key provided - testing without authentication")
        print("   (Get your API key from https://sugra.ai)")

    print()

    results = {}

    for name, url in test_endpoints:
        print(f"Testing: {name}")
        print(f"URL: {url}")

        try:
            response = requests.get(url, headers=headers, timeout=10)

            print(f"Status Code: {response.status_code}")

            if response.status_code == 200:
                data = response.json()

                if isinstance(data, list):
                    print(f"✅ SUCCESS - Received {len(data)} items")
                    if data:
                        print(f"   Sample item keys: {list(data[0].keys())[:5]}")
                        results[name] = {
                            "success": True,
                            "items": len(data),
                            "sample": data[0] if data else None
                        }
                elif isinstance(data, dict):
                    print(f"✅ SUCCESS - Received data object")
                    print(f"   Keys: {list(data.keys())[:10]}")
                    results[name] = {
                        "success": True,
                        "data": data
                    }
                else:
                    print(f"⚠️  Unexpected data type: {type(data)}")
                    results[name] = {"success": False, "reason": "Unexpected data type"}

            elif response.status_code == 401:
                print(f"❌ AUTHENTICATION FAILED")
                print(f"   You need a valid API key from https://sugra.ai")
                results[name] = {"success": False, "reason": "Authentication required"}

            elif response.status_code == 403:
                print(f"❌ ACCESS FORBIDDEN")
                print(f"   API key may be invalid or lacks permissions")
                results[name] = {"success": False, "reason": "Access forbidden"}

            elif response.status_code == 429:
                print(f"❌ RATE LIMIT EXCEEDED")
                print(f"   Too many requests - wait before retrying")
                results[name] = {"success": False, "reason": "Rate limited"}

            else:
                print(f"❌ REQUEST FAILED")
                print(f"   Response: {response.text[:200]}")
                results[name] = {"success": False, "reason": f"HTTP {response.status_code}"}

        except requests.exceptions.Timeout:
            print(f"❌ TIMEOUT - Request took too long")
            results[name] = {"success": False, "reason": "Timeout"}

        except requests.exceptions.ConnectionError:
            print(f"❌ CONNECTION ERROR - Cannot reach API")
            results[name] = {"success": False, "reason": "Connection error"}

        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            results[name] = {"success": False, "reason": str(e)}

        print()

    return results


def test_data_parsing(api_key: str = None):
    """Test data parsing from API response"""
    print("\n" + "=" * 80)
    print("TESTING DATA PARSING")
    print("=" * 80 + "\n")

    if not api_key or api_key == "your_api_key_here":
        print("⚠️  Skipping - API key required for this test")
        return None

    url = "https://api.sugra.ai/v1/economics/united-states/housing"
    headers = {'x-api-key': api_key}

    try:
        print(f"Fetching housing data for United States...")
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Received {len(data)} housing indicators\n")

            # Parse and display sample indicators
            print("Sample Indicators:")
            print("-" * 80)

            for i, indicator in enumerate(data[:5]):  # Show first 5
                name = indicator.get('Country Indicator', 'Unknown')
                last = indicator.get('Last', 'N/A')
                previous = indicator.get('Previous', 'N/A')
                unit = indicator.get('Unit', '')

                print(f"{i+1}. {name}")
                print(f"   Last: {last} {unit}")
                print(f"   Previous: {previous} {unit}")
                print()

            return {"success": True, "data": data}

        else:
            print(f"❌ Failed with status {response.status_code}")
            return {"success": False, "status": response.status_code}

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {"success": False, "error": str(e)}


def test_database_storage(api_key: str = None):
    """Test storing data in database"""
    print("\n" + "=" * 80)
    print("TESTING DATABASE STORAGE")
    print("=" * 80 + "\n")

    if not api_key or api_key == "your_api_key_here":
        print("⚠️  Skipping - API key required for this test")
        return None

    try:
        from app.database.country_database_manager import country_db_manager
        from app.services.economics_db_service import EconomicsDBService
        from app.services.economics_api_service import EconomicsAPIService
        from app.services.economics_data_parser import EconomicsDataParser

        print("1. Checking if United States database exists...")

        # Check if database exists
        databases = country_db_manager.list_country_databases()
        us_db_exists = any(slug == "united-states" and exists for slug, _, exists in databases)

        if not us_db_exists:
            print("   Creating United States database...")
            success = country_db_manager.initialize_country_database("united-states")
            if success:
                print("   ✅ Database created successfully")
            else:
                print("   ❌ Failed to create database")
                return {"success": False, "reason": "Database creation failed"}
        else:
            print("   ✅ Database already exists")

        print("\n2. Fetching data from API...")

        api_service = EconomicsAPIService(api_key=api_key)

        # Fetch overview data
        overview_data = api_service.get_country_overview("united-states")

        if not overview_data:
            print("   ❌ No data received from API")
            return {"success": False, "reason": "No API data"}

        print(f"   ✅ Received overview data with {len(overview_data)} items")

        print("\n3. Parsing data...")

        parser = EconomicsDataParser()
        parsed_overview = parser.parse_country_overview(overview_data, "United States")

        print(f"   ✅ Parsed overview data")

        print("\n4. Saving to database...")

        db = country_db_manager.get_session("united-states")
        db_service = EconomicsDBService(db)

        # Save overview
        db_service.save_country_overview("United States", parsed_overview)
        print(f"   ✅ Saved overview to database")

        # Fetch and save one category (GDP)
        print("\n5. Fetching and saving GDP indicators...")
        gdp_data = api_service.get_indicators("united-states", "gdp")

        if gdp_data:
            parsed_indicators = parser.parse_indicators(gdp_data, "United States", "gdp")
            db_service.save_economic_indicators("United States", "gdp", parsed_indicators)
            print(f"   ✅ Saved {len(parsed_indicators)} GDP indicators")
        else:
            print("   ⚠️  No GDP data available")

        print("\n6. Verifying data in database...")

        # Query back from database
        indicators = db_service.get_economic_indicators(
            country="United States",
            category="gdp",
            limit=5
        )

        if indicators:
            print(f"   ✅ Successfully retrieved {len(indicators)} indicators from database")
            print("\n   Sample indicators:")
            for ind in indicators[:3]:
                print(f"   - {ind.indicator_name}: {ind.last_value}")
        else:
            print("   ⚠️  No indicators found in database")

        return {
            "success": True,
            "overview_items": len(overview_data),
            "gdp_indicators": len(parsed_indicators) if gdp_data else 0,
            "database_indicators": len(indicators)
        }

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}


def test_analysis_tools(api_key: str = None):
    """Test analysis tools with real data"""
    print("\n" + "=" * 80)
    print("TESTING ANALYSIS TOOLS")
    print("=" * 80 + "\n")

    try:
        from app.database.country_database_manager import country_db_manager
        from app.services.economics_db_service import EconomicsDBService
        from app.services.economic_analyzer import EconomicAnalyzer

        # Check if we have data
        db = country_db_manager.get_session("united-states")
        db_service = EconomicsDBService(db)

        indicators = db_service.get_economic_indicators(
            country="United States",
            category="gdp",
            limit=1
        )

        if not indicators:
            print("⚠️  No data in database - run data fetch test first")
            return {"success": False, "reason": "No data"}

        print("1. Testing Economic Analyzer...")

        analyzer = EconomicAnalyzer(db_service)

        # Analyze a single indicator
        indicator = indicators[0]

        interpretation = analyzer.interpret_indicator(
            indicator.indicator_name,
            indicator.last_value_numeric,
        )

        print(f"   ✅ Analyzed indicator: {interpretation['indicator']}")
        print(f"   Classification: {interpretation['classification']}")
        print(f"   Signal: {interpretation.get('signal', 'unknown')}")

        print("\n2. Testing Country Analysis...")

        analysis = analyzer.analyze_country("United States")

        if "summary" in analysis:
            print(f"   ✅ Health Score: {analysis['summary'].get('health_score', 'N/A')}/100")
            print(f"   Leading Indicators: {analysis['summary'].get('leading_count', 0)}")
            print(f"   Coincident Indicators: {analysis['summary'].get('coincident_count', 0)}")
            print(f"   Lagging Indicators: {analysis['summary'].get('lagging_count', 0)}")

        return {"success": True, "analysis": analysis}

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}


def main():
    """Main test runner"""
    print("\n" + "🔬" * 40)
    print("ECONOMICS API & DATA PIPELINE TEST SUITE")
    print("🔬" * 40)

    # Get API key from environment or command line
    api_key = os.getenv("ECONOMICS_API_KEY")

    if len(sys.argv) > 1:
        api_key = sys.argv[1]

    if not api_key or api_key == "your_api_key_here":
        print("\n⚠️  WARNING: No valid API key provided")
        print("   Many tests will be skipped")
        print("\nTo run full tests:")
        print("   python3 test_api_pipeline.py YOUR_API_KEY")
        print("\nOr set in environment:")
        print("   export ECONOMICS_API_KEY=your_key")
        print("   python3 test_api_pipeline.py")
    else:
        print(f"\n✅ Using API key: {api_key[:8]}...")

    # Run tests
    results = {}

    # Test 1: API Connectivity
    results['connectivity'] = test_api_connectivity(api_key)

    # Test 2: Data Parsing
    results['parsing'] = test_data_parsing(api_key)

    # Test 3: Database Storage
    results['database'] = test_database_storage(api_key)

    # Test 4: Analysis Tools
    results['analysis'] = test_analysis_tools(api_key)

    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80 + "\n")

    all_success = True

    for test_name, result in results.items():
        if result is None:
            print(f"⚠️  {test_name.upper()}: Skipped (API key required)")
        elif result.get('success'):
            print(f"✅ {test_name.upper()}: Passed")
        else:
            print(f"❌ {test_name.upper()}: Failed - {result.get('reason', result.get('error', 'Unknown'))}")
            all_success = False

    print("\n" + "=" * 80)

    if all_success and api_key and api_key != "your_api_key_here":
        print("🎉 ALL TESTS PASSED!")
        print("\nYour economics data pipeline is working correctly!")
        print("\nNext steps:")
        print("  1. Run: python3 initialize_country_databases.py")
        print("  2. Run: python3 country_scripts/update_united_states.py")
        print("  3. Run: python3 analyze_economics.py analyze united-states")
    elif api_key and api_key != "your_api_key_here":
        print("⚠️  SOME TESTS FAILED")
        print("\nCheck the errors above and fix any issues.")
    else:
        print("ℹ️  TESTS INCOMPLETE")
        print("\nProvide a valid API key to run full test suite:")
        print("  python3 test_api_pipeline.py YOUR_API_KEY")

    print("=" * 80 + "\n")

    return 0 if all_success else 1


if __name__ == "__main__":
    sys.exit(main())
