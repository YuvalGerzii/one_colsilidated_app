#!/usr/bin/env python3
"""
Simple Direct HTTP Test for Economics API

This script tests the Economics API using direct HTTP calls without
requiring the full application dependencies.

Usage:
    python3 test_economics_api_direct.py API_KEY
"""

import sys
import json
import http.client
from urllib.parse import urlparse


def test_api_call(api_key: str, endpoint: str, params: dict = None):
    """Make a direct HTTP call to the Economics API"""
    try:
        base_url = "https://api.sugra.ai"
        parsed = urlparse(base_url)

        conn = http.client.HTTPSConnection(parsed.netloc)

        # Build path with query parameters
        path = endpoint
        if params:
            query_string = "&".join([f"{k}={v}" for k, v in params.items()])
            path = f"{endpoint}?{query_string}"

        # Set headers
        headers = {'x-api-key': api_key}

        print(f"\n{'='*80}")
        print(f"Testing: {endpoint}")
        print(f"Full URL: {base_url}{path}")
        print(f"{'='*80}")

        # Make request
        conn.request("GET", path, "", headers)
        res = conn.getresponse()
        data = res.read()

        print(f"Status: {res.status} {res.reason}")

        if res.status == 200:
            parsed_data = json.loads(data.decode("utf-8"))
            print(f"✓ SUCCESS")
            print(f"\nResponse (first 2 items):")
            if isinstance(parsed_data, list):
                print(json.dumps(parsed_data[:2], indent=2))
            else:
                print(json.dumps(parsed_data, indent=2))
            return True
        else:
            print(f"✗ FAILED")
            print(f"Response: {data.decode('utf-8')}")
            return False

    except Exception as e:
        print(f"✗ ERROR: {str(e)}")
        return False


def main():
    """Main test function"""
    if len(sys.argv) < 2:
        print("Usage: python3 test_economics_api_direct.py API_KEY")
        print("\nExample:")
        print("  python3 test_economics_api_direct.py ABCD314159")
        sys.exit(1)

    api_key = sys.argv[1]

    print("\n" + "="*80)
    print(" ECONOMICS API DIRECT HTTP TEST")
    print("="*80)
    print(f"\nAPI Key: {api_key[:10]}..." if len(api_key) > 10 else f"\nAPI Key: {api_key}")

    results = []

    # Test 1: Countries Overview (like user's example)
    results.append(
        test_api_call(api_key, "/v1/economics/countries-overview", {"country": "null"})
    )

    # Test 2: United States Overview
    results.append(
        test_api_call(api_key, "/v1/economics/united-states/overview")
    )

    # Test 3: United States GDP
    results.append(
        test_api_call(api_key, "/v1/economics/united-states/gdp")
    )

    # Test 4: United States Labour
    results.append(
        test_api_call(api_key, "/v1/economics/united-states/labour")
    )

    # Test 5: United States Prices
    results.append(
        test_api_call(api_key, "/v1/economics/united-states/prices")
    )

    # Test 6: United States Housing
    results.append(
        test_api_call(api_key, "/v1/economics/united-states/housing")
    )

    # Test 7: United States Money
    results.append(
        test_api_call(api_key, "/v1/economics/united-states/money")
    )

    # Test 8: United States Trade
    results.append(
        test_api_call(api_key, "/v1/economics/united-states/trade")
    )

    # Test 9: United States Government
    results.append(
        test_api_call(api_key, "/v1/economics/united-states/government")
    )

    # Test 10: United States Business
    results.append(
        test_api_call(api_key, "/v1/economics/united-states/business")
    )

    # Test 11: United States Consumer
    results.append(
        test_api_call(api_key, "/v1/economics/united-states/consumer")
    )

    # Test 12: Israel Housing
    results.append(
        test_api_call(api_key, "/v1/economics/israel/housing")
    )

    # Summary
    print(f"\n{'='*80}")
    print(" TEST SUMMARY")
    print(f"{'='*80}")
    total = len(results)
    passed = sum(results)
    failed = total - passed
    print(f"\nTotal Tests: {total}")
    print(f"Passed: {passed} ✓")
    print(f"Failed: {failed} ✗")
    print(f"Success Rate: {(passed/total*100):.1f}%")

    if passed == total:
        print("\n🎉 All tests passed! The Economics API is working correctly.")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Check your API key or endpoint configuration.")


if __name__ == "__main__":
    main()
