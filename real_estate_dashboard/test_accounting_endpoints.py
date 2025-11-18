#!/usr/bin/env python3
"""
Test script to verify accounting API endpoints functionality
"""

import requests
import json

BASE_URL = "http://localhost:8001/api/v1"

def test_endpoint(name, method, url, data=None):
    """Test a single endpoint"""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"{'='*60}")

    try:
        if method == "POST":
            response = requests.post(url, json=data, timeout=10)
        else:
            response = requests.get(url, timeout=10)

        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            print("✅ SUCCESS")
            result = response.json()
            print(f"Response keys: {list(result.keys())}")
            return True
        else:
            print(f"❌ FAILED")
            print(f"Response: {response.text[:500]}")
            return False

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def main():
    print("\n" + "="*60)
    print(" ACCOUNTING API ENDPOINTS FUNCTIONAL TEST")
    print("="*60)

    results = {}

    # Test 1: Entity Comparison
    results['Entity Comparison'] = test_endpoint(
        "Entity Comparison Calculator",
        "POST",
        f"{BASE_URL}/tax-calculators/entity-comparison",
        {
            "net_income": 150000,
            "reasonable_salary": 60000,
            "state_tax_rate": 5.0,
            "filing_status": "married"
        }
    )

    # Test 2: Cost Segregation
    results['Cost Segregation'] = test_endpoint(
        "Cost Segregation & Depreciation Calculator",
        "POST",
        f"{BASE_URL}/tax-calculators/cost-segregation",
        {
            "building_cost": 500000,
            "land_cost": 200000,
            "property_type": "commercial"
        }
    )

    # Test 3: Compliance Calendar
    results['Compliance Calendar'] = test_endpoint(
        "Tax Compliance Calendar",
        "GET",
        f"{BASE_URL}/tax-calculators/compliance-calendar/2024"
    )

    # Test 4: Audit Risk Assessment
    results['Audit Risk'] = test_endpoint(
        "IRS Audit Risk Assessment",
        "POST",
        f"{BASE_URL}/tax-calculators/audit-risk",
        {
            "income": 150000,
            "business_type": "consulting",
            "deductions": {
                "meals_entertainment": 5000,
                "travel": 10000,
                "vehicle": 8000
            },
            "filing_status": "married",
            "has_schedule_c": True,
            "has_rental_properties": 2,
            "claims_reps": False,
            "has_foreign_accounts": False,
            "large_charitable": 5000,
            "home_office": True,
            "large_losses": 0
        }
    )

    # Summary
    print("\n" + "="*60)
    print(" TEST SUMMARY")
    print("="*60)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name:30} {status}")

    print(f"\n{'='*60}")
    print(f"Results: {passed}/{total} tests passed")
    print(f"{'='*60}\n")

    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
