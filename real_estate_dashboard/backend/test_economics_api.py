#!/usr/bin/env python3
"""
Test Script for Economics API Integration

This script tests all economics API endpoints using both direct HTTP calls
and the EconomicsAPIService wrapper.

Usage:
    python test_economics_api.py [API_KEY]

If API_KEY is not provided, it will use the value from .env file.
"""

import os
import sys
import json
import asyncio
import http.client
from typing import Dict, Any, Optional
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.economics_api_service import EconomicsAPIService
from app.settings import settings


class EconomicsAPITester:
    """Test class for Economics API endpoints"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.ECONOMICS_API_KEY
        self.base_url = settings.ECONOMICS_API_BASE_URL
        self.service = EconomicsAPIService(api_key=self.api_key)
        self.results = []

    def print_header(self, title: str):
        """Print formatted header"""
        print("\n" + "=" * 80)
        print(f" {title}")
        print("=" * 80)

    def print_result(self, test_name: str, success: bool, data: Any = None, error: str = None):
        """Print test result"""
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"\n{status} - {test_name}")

        if error:
            print(f"  Error: {error}")
        elif data:
            if isinstance(data, dict):
                if "error" in data:
                    print(f"  API Error: {data['error']}")
                else:
                    print(f"  Response keys: {list(data.keys())}")
                    if "data" in data and isinstance(data["data"], list):
                        print(f"  Data records: {len(data['data'])}")
                    elif "countries" in data and isinstance(data["countries"], list):
                        print(f"  Countries: {len(data['countries'])}")

        self.results.append({
            "test": test_name,
            "success": success,
            "error": error,
            "timestamp": datetime.now().isoformat()
        })

    def test_direct_http_call(self, endpoint: str, params: Dict[str, str] = None) -> Dict[str, Any]:
        """Test direct HTTP call using http.client (like the user's example)"""
        try:
            # Parse the base URL
            from urllib.parse import urlparse
            parsed = urlparse(self.base_url)

            conn = http.client.HTTPSConnection(parsed.netloc)

            # Build the full path with query parameters
            path = endpoint
            if params:
                query_string = "&".join([f"{k}={v}" for k, v in params.items()])
                path = f"{endpoint}?{query_string}"

            headers = {}
            if self.api_key:
                headers['x-api-key'] = self.api_key

            conn.request("GET", path, "", headers)
            res = conn.getresponse()
            data = res.read()

            if res.status != 200:
                return {
                    "error": f"HTTP {res.status}: {res.reason}",
                    "response": data.decode("utf-8")
                }

            return json.loads(data.decode("utf-8"))

        except Exception as e:
            return {"error": str(e)}

    async def test_countries_overview(self):
        """Test 1: Get Economic Countries Indicators"""
        self.print_header("Test 1: Countries Overview")

        # Test with direct HTTP call (like user's example)
        print("\n1a) Direct HTTP call:")
        data = self.test_direct_http_call("/v1/economics/countries-overview", {"country": "null"})
        success = "error" not in data and isinstance(data, list)
        self.print_result("Direct HTTP - Countries Overview", success, data if not success else {"data": data})

        if success and len(data) > 0:
            print(f"\nSample data (first country):")
            print(json.dumps(data[0], indent=2))

        # Test with service wrapper
        print("\n1b) Service wrapper call:")
        try:
            result = await self.service.get_countries_overview(use_cache=False)
            success = "error" not in result
            self.print_result("Service - Countries Overview", success, result)
        except Exception as e:
            self.print_result("Service - Countries Overview", False, error=str(e))

    async def test_country_specific_overview(self, country: str = "United States"):
        """Test 2: Get specific country overview"""
        self.print_header(f"Test 2: {country} Overview")

        try:
            # Using service
            country_slug = country.lower().replace(" ", "-")
            result = await self.service.get_country_overview(country_slug, use_cache=False)
            success = "error" not in result
            self.print_result(f"{country} Overview", success, result)

            if success and "data" in result:
                print(f"\nSample data:")
                print(json.dumps(result["data"][:2] if isinstance(result["data"], list) else result["data"], indent=2))

        except Exception as e:
            self.print_result(f"{country} Overview", False, error=str(e))

    async def test_gdp_indicators(self, country: str = "United States"):
        """Test 3: Get Economics GDP Indicators"""
        self.print_header(f"Test 3: GDP Indicators - {country}")

        try:
            country_slug = country.lower().replace(" ", "-")
            result = await self.service.get_gdp_data(country_slug, use_cache=False)
            success = "error" not in result
            self.print_result(f"GDP Data - {country}", success, result)

            if success and "data" in result:
                print(f"\nSample GDP data:")
                data_sample = result["data"][:3] if isinstance(result["data"], list) else result["data"]
                print(json.dumps(data_sample, indent=2))

        except Exception as e:
            self.print_result(f"GDP Data - {country}", False, error=str(e))

    async def test_labour_indicators(self, country: str = "United States"):
        """Test 4: Get Economics Labour Indicators"""
        self.print_header(f"Test 4: Labour Indicators - {country}")

        try:
            country_slug = country.lower().replace(" ", "-")
            result = await self.service.get_labour_data(country_slug, use_cache=False)
            success = "error" not in result
            self.print_result(f"Labour Data - {country}", success, result)

            if success and "data" in result:
                print(f"\nSample Labour data:")
                data_sample = result["data"][:3] if isinstance(result["data"], list) else result["data"]
                print(json.dumps(data_sample, indent=2))

        except Exception as e:
            self.print_result(f"Labour Data - {country}", False, error=str(e))

    async def test_prices_indicators(self, country: str = "United States"):
        """Test 5: Get Economics Prices Indicators"""
        self.print_header(f"Test 5: Prices/Inflation Indicators - {country}")

        try:
            country_slug = country.lower().replace(" ", "-")
            result = await self.service.get_inflation_data(country_slug, use_cache=False)
            success = "error" not in result
            self.print_result(f"Prices Data - {country}", success, result)

            if success and "data" in result:
                print(f"\nSample Prices data:")
                data_sample = result["data"][:3] if isinstance(result["data"], list) else result["data"]
                print(json.dumps(data_sample, indent=2))

        except Exception as e:
            self.print_result(f"Prices Data - {country}", False, error=str(e))

    async def test_money_indicators(self, country: str = "United States"):
        """Test 6: Get Economics Money Indicators"""
        self.print_header(f"Test 6: Money/Interest Rate Indicators - {country}")

        try:
            country_slug = country.lower().replace(" ", "-")
            result = await self.service.get_interest_rates(country_slug, use_cache=False)
            success = "error" not in result
            self.print_result(f"Money Data - {country}", success, result)

            if success and "data" in result:
                print(f"\nSample Money data:")
                data_sample = result["data"][:3] if isinstance(result["data"], list) else result["data"]
                print(json.dumps(data_sample, indent=2))

        except Exception as e:
            self.print_result(f"Money Data - {country}", False, error=str(e))

    async def test_trade_indicators(self, country: str = "United States"):
        """Test 7: Get Economics Trade Indicators"""
        self.print_header(f"Test 7: Trade Indicators - {country}")

        try:
            country_slug = country.lower().replace(" ", "-")
            result = await self.service.get_trade_data(country_slug, use_cache=False)
            success = "error" not in result
            self.print_result(f"Trade Data - {country}", success, result)

            if success and "data" in result:
                print(f"\nSample Trade data:")
                data_sample = result["data"][:3] if isinstance(result["data"], list) else result["data"]
                print(json.dumps(data_sample, indent=2))

        except Exception as e:
            self.print_result(f"Trade Data - {country}", False, error=str(e))

    async def test_housing_indicators(self, country: str = "United States"):
        """Test 8: Get Economics Housing Indicators"""
        self.print_header(f"Test 8: Housing Indicators - {country}")

        try:
            country_slug = country.lower().replace(" ", "-")
            result = await self.service.get_housing_data(country_slug, use_cache=False)
            success = "error" not in result
            self.print_result(f"Housing Data - {country}", success, result)

            if success and "data" in result:
                print(f"\nSample Housing data:")
                data_sample = result["data"][:3] if isinstance(result["data"], list) else result["data"]
                print(json.dumps(data_sample, indent=2))

        except Exception as e:
            self.print_result(f"Housing Data - {country}", False, error=str(e))

    async def test_all_categories(self, country: str = "United States"):
        """Test all economic indicator categories for a country"""
        categories = ["overview", "gdp", "labour", "prices", "money", "trade", "housing", "government", "business", "consumer"]

        self.print_header(f"Test 9: All Categories - {country}")

        country_slug = country.lower().replace(" ", "-")

        for category in categories:
            try:
                if category == "overview":
                    result = await self.service.get_country_overview(country_slug, use_cache=False)
                else:
                    result = await self.service.get_economic_indicator(country_slug, category, use_cache=False)

                success = "error" not in result
                self.print_result(f"{category.capitalize()} - {country}", success, result)

            except Exception as e:
                self.print_result(f"{category.capitalize()} - {country}", False, error=str(e))

    async def test_compare_countries(self):
        """Test 10: Compare multiple countries"""
        self.print_header("Test 10: Compare Countries")

        try:
            countries = ["united-states", "china", "japan", "germany"]
            result = await self.service.compare_countries(countries, use_cache=False)
            success = "error" not in result
            self.print_result("Compare Countries", success, result)

            if success and "comparison" in result:
                print(f"\nCountries compared: {', '.join(countries)}")

        except Exception as e:
            self.print_result("Compare Countries", False, error=str(e))

    async def test_market_intelligence_summary(self):
        """Test 11: Get comprehensive market intelligence summary"""
        self.print_header("Test 11: Market Intelligence Summary")

        try:
            result = await self.service.get_market_intelligence_summary(use_cache=False)
            success = "error" not in result
            self.print_result("Market Intelligence Summary", success, result)

            if success and "countries" in result:
                print(f"\nCountries in summary: {len(result['countries'])}")

        except Exception as e:
            self.print_result("Market Intelligence Summary", False, error=str(e))

    def print_summary(self):
        """Print test summary"""
        self.print_header("Test Summary")

        total = len(self.results)
        passed = sum(1 for r in self.results if r["success"])
        failed = total - passed

        print(f"\nTotal Tests: {total}")
        print(f"Passed: {passed} (✓)")
        print(f"Failed: {failed} (✗)")
        print(f"Success Rate: {(passed/total*100):.1f}%")

        if failed > 0:
            print("\nFailed Tests:")
            for r in self.results:
                if not r["success"]:
                    print(f"  - {r['test']}: {r.get('error', 'Unknown error')}")

    async def run_all_tests(self):
        """Run all tests"""
        print("\n" + "=" * 80)
        print(" ECONOMICS API INTEGRATION TEST SUITE")
        print("=" * 80)
        print(f"\nBase URL: {self.base_url}")
        print(f"API Key: {'✓ Configured' if self.api_key else '✗ Not configured'}")
        print(f"Timestamp: {datetime.now().isoformat()}")

        if not self.api_key:
            print("\n⚠️  WARNING: No API key configured. Some tests may fail.")
            print("   Set ECONOMICS_API_KEY in .env or pass as argument.")

        # Run all tests
        await self.test_countries_overview()
        await self.test_country_specific_overview("United States")
        await self.test_gdp_indicators("United States")
        await self.test_labour_indicators("United States")
        await self.test_prices_indicators("United States")
        await self.test_money_indicators("United States")
        await self.test_trade_indicators("United States")
        await self.test_housing_indicators("United States")
        await self.test_all_categories("Israel")
        await self.test_compare_countries()
        await self.test_market_intelligence_summary()

        # Print summary
        self.print_summary()

        # Save results to file
        results_file = "economics_api_test_results.json"
        with open(results_file, "w") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "total_tests": len(self.results),
                "passed": sum(1 for r in self.results if r["success"]),
                "failed": sum(1 for r in self.results if not r["success"]),
                "results": self.results
            }, f, indent=2)

        print(f"\n📄 Detailed results saved to: {results_file}")


async def main():
    """Main entry point"""
    # Get API key from command line or environment
    api_key = sys.argv[1] if len(sys.argv) > 1 else None

    if not api_key:
        # Try to load from .env
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("ECONOMICS_API_KEY")

    # Run tests
    tester = EconomicsAPITester(api_key=api_key)
    await tester.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())
