#!/usr/bin/env python3
"""
Zillow Mortgage Rates API Client

Fetches current mortgage rates from Zillow's API endpoints.
Supports various loan types, terms, and criteria filtering.

Usage:
    python zillow_mortgage_rates.py
    python zillow_mortgage_rates.py --loan-amount 300000 --credit-score 740

API Endpoints:
    - https://mortgageapi.zillow.com/api/getRates
    - https://mortgageapi.zillow.com/api/getCurrentRates
"""

import os
import sys
import json
import logging
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict


# Configuration
API_BASE_URL = "https://mortgageapi.zillow.com/api"
DEFAULT_STORAGE_PATH = Path(__file__).parent.parent / "storage" / "zillow"


@dataclass
class LoanCriteria:
    """Loan criteria for rate queries."""
    loan_amount: int = 300000
    loan_to_value: float = 80.0  # LTV percentage
    credit_score: int = 740
    state_abbreviation: str = "CA"
    loan_purpose: str = "Purchase"  # Purchase, Refinance
    property_type: str = "SingleFamily"  # SingleFamily, Condo, Townhouse, MultiFamily
    occupancy: str = "Primary"  # Primary, Secondary, Investment
    points: float = 0.0
    is_first_time_buyer: bool = False


class ZillowMortgageRatesClient:
    """Client for fetching Zillow mortgage rate data."""

    def __init__(self, storage_path: Optional[Path] = None):
        self.storage_path = Path(storage_path) if storage_path else DEFAULT_STORAGE_PATH
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Origin': 'https://www.zillow.com',
            'Referer': 'https://www.zillow.com/mortgage-rates/'
        })

        # Setup logging
        self._setup_logging()

        # Ensure storage directory exists
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def _setup_logging(self):
        """Configure logging."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler(sys.stdout)]
        )
        self.logger = logging.getLogger(__name__)

    def get_rates(self, criteria: Optional[LoanCriteria] = None) -> Dict[str, Any]:
        """
        Get mortgage rates based on loan criteria.

        Args:
            criteria: LoanCriteria object with loan parameters.
                     If None, uses default criteria.

        Returns:
            Dictionary containing rate data.
        """
        if criteria is None:
            criteria = LoanCriteria()

        endpoint = f"{API_BASE_URL}/getRates"

        # Build request payload
        payload = {
            "loanAmount": criteria.loan_amount,
            "ltv": criteria.loan_to_value,
            "creditScoreRange": self._get_credit_score_range(criteria.credit_score),
            "stateAbbreviation": criteria.state_abbreviation,
            "loanPurpose": criteria.loan_purpose,
            "propertyType": criteria.property_type,
            "occupancy": criteria.occupancy,
            "points": criteria.points,
            "isFirstTimeBuyer": criteria.is_first_time_buyer,
            "programs": [
                "Fixed30Year",
                "Fixed15Year",
                "ARM5",
                "ARM7",
                "FHA30Year",
                "VA30Year",
                "Jumbo30Year"
            ]
        }

        self.logger.info(f"Fetching rates for {criteria.state_abbreviation}, "
                        f"${criteria.loan_amount:,} loan, {criteria.credit_score} credit score")

        try:
            response = self.session.post(endpoint, json=payload, timeout=30)

            if response.status_code == 200:
                data = response.json()
                self.logger.info("Successfully fetched mortgage rates")
                return {
                    "status": "success",
                    "timestamp": datetime.now().isoformat(),
                    "criteria": asdict(criteria),
                    "rates": data
                }
            else:
                self.logger.error(f"API returned status {response.status_code}")
                return {
                    "status": "error",
                    "timestamp": datetime.now().isoformat(),
                    "error": f"HTTP {response.status_code}",
                    "response_text": response.text[:500]
                }

        except Exception as e:
            self.logger.error(f"Error fetching rates: {str(e)}")
            return {
                "status": "error",
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }

    def get_current_rates(self) -> Dict[str, Any]:
        """
        Get current national average mortgage rates.

        Returns:
            Dictionary containing current rate averages.
        """
        endpoint = f"{API_BASE_URL}/getCurrentRates"

        self.logger.info("Fetching current national average rates")

        try:
            response = self.session.get(endpoint, timeout=30)

            if response.status_code == 200:
                data = response.json()
                self.logger.info("Successfully fetched current rates")
                return {
                    "status": "success",
                    "timestamp": datetime.now().isoformat(),
                    "rates": data
                }
            else:
                self.logger.error(f"API returned status {response.status_code}")
                return {
                    "status": "error",
                    "timestamp": datetime.now().isoformat(),
                    "error": f"HTTP {response.status_code}",
                    "response_text": response.text[:500]
                }

        except Exception as e:
            self.logger.error(f"Error fetching current rates: {str(e)}")
            return {
                "status": "error",
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }

    def get_rates_by_state(self, states: List[str], criteria: Optional[LoanCriteria] = None) -> Dict[str, Any]:
        """
        Get mortgage rates for multiple states.

        Args:
            states: List of state abbreviations.
            criteria: Base loan criteria (state will be overridden).

        Returns:
            Dictionary containing rates by state.
        """
        if criteria is None:
            criteria = LoanCriteria()

        results = {}

        for state in states:
            state_criteria = LoanCriteria(
                loan_amount=criteria.loan_amount,
                loan_to_value=criteria.loan_to_value,
                credit_score=criteria.credit_score,
                state_abbreviation=state,
                loan_purpose=criteria.loan_purpose,
                property_type=criteria.property_type,
                occupancy=criteria.occupancy,
                points=criteria.points,
                is_first_time_buyer=criteria.is_first_time_buyer
            )

            result = self.get_rates(state_criteria)
            results[state] = result

        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "states": results
        }

    def get_rate_comparison(self, loan_amounts: List[int], credit_scores: List[int]) -> Dict[str, Any]:
        """
        Compare rates across different loan amounts and credit scores.

        Args:
            loan_amounts: List of loan amounts to compare.
            credit_scores: List of credit scores to compare.

        Returns:
            Dictionary containing rate comparison matrix.
        """
        results = []

        for amount in loan_amounts:
            for score in credit_scores:
                criteria = LoanCriteria(
                    loan_amount=amount,
                    credit_score=score
                )
                result = self.get_rates(criteria)

                if result["status"] == "success":
                    results.append({
                        "loan_amount": amount,
                        "credit_score": score,
                        "rates": result.get("rates", {})
                    })

        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "comparison": results
        }

    def _get_credit_score_range(self, score: int) -> str:
        """Convert numeric credit score to Zillow's range format."""
        if score >= 760:
            return "760+"
        elif score >= 740:
            return "740-759"
        elif score >= 720:
            return "720-739"
        elif score >= 700:
            return "700-719"
        elif score >= 680:
            return "680-699"
        elif score >= 660:
            return "660-679"
        elif score >= 640:
            return "640-659"
        elif score >= 620:
            return "620-639"
        else:
            return "Below620"

    def save_rates(self, data: Dict[str, Any], filename: str = "mortgage_rates.json") -> str:
        """
        Save rate data to storage.

        Args:
            data: Rate data to save.
            filename: Output filename.

        Returns:
            Path to saved file.
        """
        file_path = self.storage_path / filename

        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)

        self.logger.info(f"Saved rates to {file_path}")
        return str(file_path)

    def fetch_and_save_daily_rates(self) -> Dict[str, Any]:
        """
        Fetch current rates and save with timestamp.

        Returns:
            Dictionary with fetch results and file path.
        """
        # Get current rates
        current_rates = self.get_current_rates()

        # Get rates for common scenarios
        scenarios = [
            LoanCriteria(loan_amount=300000, credit_score=740, state_abbreviation="CA"),
            LoanCriteria(loan_amount=500000, credit_score=760, state_abbreviation="NY"),
            LoanCriteria(loan_amount=250000, credit_score=700, state_abbreviation="TX"),
        ]

        scenario_rates = []
        for i, criteria in enumerate(scenarios):
            result = self.get_rates(criteria)
            scenario_rates.append({
                "scenario": i + 1,
                "criteria": asdict(criteria),
                "result": result
            })

        # Combine all data
        combined_data = {
            "fetch_timestamp": datetime.now().isoformat(),
            "current_national_rates": current_rates,
            "scenario_rates": scenario_rates
        }

        # Save with date in filename
        date_str = datetime.now().strftime("%Y%m%d")
        filename = f"mortgage_rates_{date_str}.json"
        file_path = self.save_rates(combined_data, filename)

        return {
            "status": "success",
            "file_path": file_path,
            "data": combined_data
        }


def format_rate_output(data: Dict[str, Any]) -> str:
    """Format rate data for display."""
    output = []
    output.append("\n" + "="*60)
    output.append("ZILLOW MORTGAGE RATES")
    output.append("="*60)

    if data.get("status") == "success":
        output.append(f"Timestamp: {data.get('timestamp', 'N/A')}")

        rates = data.get("rates", {})
        if rates:
            output.append("\nCurrent Rates:")
            output.append("-"*40)

            # Handle different response structures
            if isinstance(rates, dict):
                for program, rate_data in rates.items():
                    if isinstance(rate_data, dict):
                        rate = rate_data.get("rate", rate_data.get("apr", "N/A"))
                        output.append(f"  {program}: {rate}%")
                    else:
                        output.append(f"  {program}: {rate_data}")
            elif isinstance(rates, list):
                for item in rates:
                    program = item.get("program", "Unknown")
                    rate = item.get("rate", item.get("apr", "N/A"))
                    output.append(f"  {program}: {rate}%")
    else:
        output.append(f"Error: {data.get('error', 'Unknown error')}")

    output.append("="*60 + "\n")
    return "\n".join(output)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Fetch Zillow mortgage rates")
    parser.add_argument(
        "--storage",
        type=str,
        help="Storage directory path",
        default=str(DEFAULT_STORAGE_PATH)
    )
    parser.add_argument(
        "--loan-amount",
        type=int,
        default=300000,
        help="Loan amount in dollars"
    )
    parser.add_argument(
        "--credit-score",
        type=int,
        default=740,
        help="Credit score"
    )
    parser.add_argument(
        "--state",
        type=str,
        default="CA",
        help="State abbreviation"
    )
    parser.add_argument(
        "--ltv",
        type=float,
        default=80.0,
        help="Loan-to-value ratio"
    )
    parser.add_argument(
        "--current-only",
        action="store_true",
        help="Fetch only current national averages"
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help="Save results to storage"
    )
    parser.add_argument(
        "--daily-fetch",
        action="store_true",
        help="Run daily fetch and save routine"
    )

    args = parser.parse_args()

    # Initialize client
    client = ZillowMortgageRatesClient(storage_path=Path(args.storage))

    if args.daily_fetch:
        # Run daily fetch routine
        result = client.fetch_and_save_daily_rates()
        print(f"\nDaily rates fetched and saved to: {result['file_path']}")

    elif args.current_only:
        # Get current national rates
        result = client.get_current_rates()
        print(format_rate_output(result))

        if args.save:
            client.save_rates(result, "current_rates.json")

    else:
        # Get rates with custom criteria
        criteria = LoanCriteria(
            loan_amount=args.loan_amount,
            credit_score=args.credit_score,
            state_abbreviation=args.state,
            loan_to_value=args.ltv
        )

        result = client.get_rates(criteria)
        print(format_rate_output(result))

        if args.save:
            date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            client.save_rates(result, f"rates_{date_str}.json")

    print("\nNote: If API returns 403, Zillow may require additional authentication.")
    print("Consider using their official developer portal for API access.")
