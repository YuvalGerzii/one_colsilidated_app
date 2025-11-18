#!/usr/bin/env python3
"""
Comprehensive test runner for Portfolio Dashboard.

Runs all test suites with formatted output and summary.
"""

import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str) -> None:
    """Print formatted section header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 80}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}  {text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 80}{Colors.RESET}\n")


def print_separator() -> None:
    """Print separator line."""
    print(f"{Colors.BLUE}{'-' * 70}{Colors.RESET}")


def run_test_suite(name: str, path: str, markers: str = None) -> Tuple[bool, str]:
    """
    Run a test suite and return success status and output.
    
    Args:
        name: Test suite name
        path: Path to test file or directory
        markers: Pytest markers to filter tests
    
    Returns:
        Tuple of (success: bool, output: str)
    """
    cmd = ["pytest", path, "-v"]
    
    if markers:
        cmd.extend(["-m", markers])
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        success = result.returncode == 0
        output = result.stdout + result.stderr
        
        return success, output
    
    except subprocess.TimeoutExpired:
        return False, "Test suite timed out after 5 minutes"
    
    except Exception as e:
        return False, f"Error running tests: {str(e)}"


def extract_test_stats(output: str) -> Dict[str, int]:
    """Extract test statistics from pytest output."""
    stats = {
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "total": 0
    }
    
    # Look for pytest summary line like "5 passed in 0.23s"
    for line in output.split('\n'):
        if " passed" in line or " failed" in line:
            parts = line.split()
            for i, part in enumerate(parts):
                if i + 1 < len(parts):
                    if parts[i + 1] == "passed":
                        stats["passed"] = int(part)
                    elif parts[i + 1] == "failed":
                        stats["failed"] = int(part)
                    elif parts[i + 1] == "skipped":
                        stats["skipped"] = int(part)
    
    stats["total"] = stats["passed"] + stats["failed"] + stats["skipped"]
    
    return stats


def print_test_result(name: str, success: bool, stats: Dict[str, int]) -> None:
    """Print formatted test result."""
    if success:
        status = f"{Colors.GREEN}✓ PASSED{Colors.RESET}"
    else:
        status = f"{Colors.RED}✗ FAILED{Colors.RESET}"
    
    print(f"{status} {name}")
    
    if stats["total"] > 0:
        print(f"  Tests: {stats['passed']} passed, {stats['failed']} failed, "
              f"{stats['skipped']} skipped ({stats['total']} total)")


def main():
    """Main test runner."""
    print_header("PORTFOLIO DASHBOARD - COMPREHENSIVE TEST SUITE")
    
    # Define test suites
    test_suites = [
        {
            "name": "1. Unit Tests - CRUD Operations",
            "path": "tests/unit/test_crud.py",
            "markers": "unit"
        },
        {
            "name": "2. Integration Tests - Core API Endpoints",
            "path": "tests/integration/test_api_endpoints.py",
            "markers": "integration and not slow"
        },
        {
            "name": "3. Integration Tests - Service Endpoints",
            "path": "tests/integration/test_service_endpoints.py",
            "markers": "service and not slow"
        },
        {
            "name": "4. Performance Tests",
            "path": "tests/",
            "markers": "performance"
        },
        {
            "name": "5. All Tests (Quick Run)",
            "path": "tests/",
            "markers": "not slow"
        }
    ]
    
    results: List[Dict] = []
    
    # Run each test suite
    for suite in test_suites:
        print_separator()
        print(f"\n{Colors.BOLD}Running: {suite['name']}{Colors.RESET}\n")
        
        success, output = run_test_suite(
            name=suite['name'],
            path=suite['path'],
            markers=suite.get('markers')
        )
        
        stats = extract_test_stats(output)
        
        # Store result
        results.append({
            "name": suite['name'],
            "success": success,
            "stats": stats
        })
        
        # Print result
        print_test_result(suite['name'], success, stats)
        
        # Print failures if any
        if not success and stats["failed"] > 0:
            print(f"\n{Colors.RED}Failed tests output:{Colors.RESET}")
            # Show only the last 50 lines to avoid clutter
            lines = output.split('\n')
            for line in lines[-50:]:
                if "FAILED" in line or "ERROR" in line:
                    print(f"  {line}")
    
    # Print summary
    print_header("TEST SUMMARY")
    
    total_suites = len(results)
    passed_suites = sum(1 for r in results if r["success"])
    failed_suites = total_suites - passed_suites
    
    total_tests = sum(r["stats"]["total"] for r in results)
    passed_tests = sum(r["stats"]["passed"] for r in results)
    failed_tests = sum(r["stats"]["failed"] for r in results)
    skipped_tests = sum(r["stats"]["skipped"] for r in results)
    
    print(f"Test Suites: {passed_suites}/{total_suites} passed "
          f"({(passed_suites/total_suites*100):.1f}%)")
    print(f"Tests:       {passed_tests} passed, {failed_tests} failed, "
          f"{skipped_tests} skipped ({total_tests} total)")
    
    print_separator()
    
    if failed_suites == 0:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ ALL TEST SUITES PASSED!{Colors.RESET}\n")
        return 0
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}✗ {failed_suites} TEST SUITE(S) FAILED{Colors.RESET}\n")
        
        # List failed suites
        print("Failed suites:")
        for result in results:
            if not result["success"]:
                print(f"  - {result['name']}")
        
        print()
        return 1


if __name__ == "__main__":
    sys.exit(main())
