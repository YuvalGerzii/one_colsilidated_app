#!/usr/bin/env python3
"""
Test All Economics API Endpoints

Tests all 11 categories to verify complete API coverage.
Based on the exact endpoint list provided.

Usage:
    python3 test_all_endpoints.py API_KEY
"""

import http.client
import json
import sys


def test_endpoint(category: str, api_key: str, country: str = "United-States"):
    """Test a specific endpoint"""
    try:
        conn = http.client.HTTPSConnection("api.sugra.ai")

        if category == "overview":
            endpoint = f"/v1/economics/{country}/overview?Related=null"
        else:
            endpoint = f"/v1/economics/{country}/{category}"

        headers = {'x-api-key': api_key}

        conn.request("GET", endpoint, '', headers)
        res = conn.getresponse()
        data = res.read()

        if res.status == 200:
            parsed = json.loads(data.decode("utf-8"))
            indicator_count = len(parsed) if isinstance(parsed, list) else 0
            print(f"  ✓ {category:12} - {indicator_count:3} indicators")
            return True, indicator_count
        else:
            print(f"  ✗ {category:12} - HTTP {res.status}")
            return False, 0

    except Exception as e:
        print(f"  ✗ {category:12} - Error: {str(e)}")
        return False, 0


def main():
    """Main test function"""
    if len(sys.argv) < 2:
        print("Usage: python3 test_all_endpoints.py API_KEY")
        sys.exit(1)

    api_key = sys.argv[1]
    country = sys.argv[2] if len(sys.argv) > 2 else "United-States"

    print("\n" + "=" * 80)
    print(f" TESTING ALL ECONOMICS API ENDPOINTS - {country}")
    print("=" * 80)

    # All 11 categories from the API documentation
    categories = [
        "overview",
        "gdp",
        "labour",
        "prices",
        "health",
        "money",
        "trade",
        "government",
        "business",
        "consumer",
        "housing",
    ]

    print(f"\nTesting {len(categories)} categories:")
    print("-" * 80)

    results = []
    total_indicators = 0

    for category in categories:
        success, count = test_endpoint(category, api_key, country)
        results.append(success)
        total_indicators += count

    # Summary
    print("\n" + "=" * 80)
    print(" SUMMARY")
    print("=" * 80)
    successful = sum(results)
    failed = len(results) - successful

    print(f"\nCategories Tested: {len(categories)}")
    print(f"✓ Successful: {successful}")
    print(f"✗ Failed: {failed}")
    print(f"📊 Total Indicators: {total_indicators}")

    if failed == 0:
        print("\n🎉 All endpoints working! Complete API coverage verified.")
    else:
        print(f"\n⚠️  {failed} endpoint(s) failed. Check API key or endpoint availability.")

    print("=" * 80 + "\n")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
