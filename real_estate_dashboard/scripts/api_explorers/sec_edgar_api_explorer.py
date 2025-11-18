#!/usr/bin/env python3
"""
SEC EDGAR API Explorer
Explores company filings, REIT data, and XBRL financial data
"""

import requests
import json
from typing import Dict, List, Optional
from datetime import datetime
import time


class SECEdgarAPIExplorer:
    """Explore SEC EDGAR API for REIT and real estate company data"""

    BASE_URL = "https://data.sec.gov"
    SUBMISSIONS_URL = f"{BASE_URL}/submissions"
    COMPANY_FACTS_URL = f"{BASE_URL}/api/xbrl/companyfacts"
    COMPANY_CONCEPT_URL = f"{BASE_URL}/api/xbrl/companyconcept"
    FRAMES_URL = f"{BASE_URL}/api/xbrl/frames"

    # User-Agent is REQUIRED by SEC (Fair Access rules)
    HEADERS = {
        'User-Agent': 'Real Estate Dashboard Research Tool info@example.com',
        'Accept-Encoding': 'gzip, deflate',
        'Host': 'data.sec.gov'
    }

    # Major REITs for demonstration (CIK numbers)
    SAMPLE_REITS = {
        '0000879101': 'Simon Property Group',
        '0000906107': 'Public Storage',
        '0001043121': 'Prologis Inc',
        '0000908311': 'Equity Residential',
        '0000746210': 'AvalonBay Communities',
        '0001060578': 'Welltower Inc',
        '0001045450': 'Boston Properties',
    }

    # Key XBRL concepts for real estate
    REAL_ESTATE_CONCEPTS = {
        'RealEstateInvestmentPropertyNet': 'Net investment in real estate',
        'RealEstateInvestmentPropertyAtCost': 'Real estate at cost',
        'Revenues': 'Total revenues',
        'RealEstateRevenue': 'Real estate revenue',
        'DepreciationAndAmortization': 'Depreciation and amortization',
        'LongTermDebt': 'Long-term debt',
        'Assets': 'Total assets',
        'StockholdersEquity': 'Stockholders equity',
        'NetIncomeLoss': 'Net income/loss',
        'CashAndCashEquivalentsAtCarryingValue': 'Cash and equivalents',
    }

    # Common SEC filing types
    FILING_TYPES = {
        '10-K': 'Annual Report',
        '10-Q': 'Quarterly Report',
        '8-K': 'Current Report (major events)',
        'S-11': 'REIT Registration Statement',
        'DEF 14A': 'Proxy Statement',
        '13F-HR': 'Institutional Investment Manager Holdings',
        '4': 'Insider Trading',
        '3': 'Initial Statement of Beneficial Ownership',
    }

    def __init__(self):
        """Initialize SEC EDGAR explorer"""
        # SEC recommends max 10 requests/second
        self.rate_limit_delay = 0.1

    def _make_request(self, url: str) -> Dict:
        """Make rate-limited request to SEC API"""
        time.sleep(self.rate_limit_delay)

        try:
            response = requests.get(url, headers=self.HEADERS, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return {}

    def get_company_submissions(self, cik: str) -> Dict:
        """
        Get all submissions (filings) for a company
        CIK must be 10 digits with leading zeros
        """
        # Format CIK with leading zeros
        cik_formatted = cik.zfill(10)
        url = f"{self.SUBMISSIONS_URL}/CIK{cik_formatted}.json"

        print(f"\n{'='*80}")
        print(f"COMPANY SUBMISSIONS - CIK {cik_formatted}")
        print('='*80)

        data = self._make_request(url)

        if data:
            print(f"\nCompany: {data.get('name', 'N/A')}")
            print(f"SIC: {data.get('sic', 'N/A')} - {data.get('sicDescription', 'N/A')}")
            print(f"Fiscal Year End: {data.get('fiscalYearEnd', 'N/A')}")
            print(f"State of Incorporation: {data.get('stateOfIncorporation', 'N/A')}")
            print(f"Business Address: {data.get('addresses', {}).get('business', {})}")

            # Show recent filings
            filings = data.get('filings', {}).get('recent', {})
            if filings:
                print(f"\nRecent Filings:")
                for i in range(min(10, len(filings.get('form', [])))):
                    form = filings['form'][i]
                    filing_date = filings['filingDate'][i]
                    primary_doc = filings['primaryDocument'][i]
                    acc_number = filings['accessionNumber'][i]

                    print(f"\n  {form} - {filing_date}")
                    print(f"    Accession: {acc_number}")
                    print(f"    Document: {primary_doc}")

        return data

    def get_company_facts(self, cik: str) -> Dict:
        """
        Get all XBRL facts (financial data) for a company
        Returns all reported concepts across all periods
        """
        cik_formatted = cik.zfill(10)
        url = f"{self.COMPANY_FACTS_URL}/CIK{cik_formatted}.json"

        print(f"\n{'='*80}")
        print(f"COMPANY FACTS - CIK {cik_formatted}")
        print('='*80)

        data = self._make_request(url)

        if data:
            print(f"\nCompany: {data.get('entityName', 'N/A')}")
            print(f"CIK: {data.get('cik', 'N/A')}")

            facts = data.get('facts', {})
            us_gaap = facts.get('us-gaap', {})
            dei = facts.get('dei', {})

            print(f"\nUS-GAAP Concepts: {len(us_gaap)}")
            print(f"DEI Concepts: {len(dei)}")

            # Show some real estate relevant concepts
            print("\nSample Real Estate Concepts Found:")
            for concept, description in self.REAL_ESTATE_CONCEPTS.items():
                if concept in us_gaap:
                    concept_data = us_gaap[concept]
                    print(f"\n  {concept}:")
                    print(f"    Description: {concept_data.get('description', description)}")
                    print(f"    Label: {concept_data.get('label', 'N/A')}")

                    # Show most recent value
                    units = concept_data.get('units', {})
                    for unit_type, values in units.items():
                        if values:
                            latest = sorted(values, key=lambda x: x.get('end', ''), reverse=True)[0]
                            print(f"    Latest ({unit_type}): {latest.get('val', 'N/A')} as of {latest.get('end', 'N/A')}")
                            break

        return data

    def get_company_concept(self, cik: str, concept: str) -> Dict:
        """
        Get specific XBRL concept for a company
        Shows all historical values for one concept
        """
        cik_formatted = cik.zfill(10)
        url = f"{self.COMPANY_CONCEPT_URL}/CIK{cik_formatted}/us-gaap/{concept}.json"

        print(f"\n{'='*80}")
        print(f"CONCEPT: {concept} - CIK {cik_formatted}")
        print('='*80)

        data = self._make_request(url)

        if data:
            print(f"\nCompany: {data.get('entityName', 'N/A')}")
            print(f"Concept: {data.get('tag', 'N/A')}")
            print(f"Label: {data.get('label', 'N/A')}")
            print(f"Description: {data.get('description', 'N/A')}")

            units = data.get('units', {})
            for unit_type, values in units.items():
                print(f"\nUnit: {unit_type}")
                print(f"Total Values: {len(values)}")

                # Show recent values
                recent = sorted(values, key=lambda x: x.get('end', ''), reverse=True)[:5]
                for val in recent:
                    print(f"  {val.get('end', 'N/A')}: {val.get('val', 'N/A'):,} "
                          f"({val.get('form', 'N/A')} - {val.get('fy', 'N/A')} {val.get('fp', 'N/A')})")

        return data

    def explore_reit_data(self) -> None:
        """Explore sample REIT data"""
        print("\n" + "=" * 80)
        print("🏢 EXPLORING MAJOR REITS")
        print("=" * 80)

        print("\nSample REITs:")
        for cik, name in list(self.SAMPLE_REITS.items())[:3]:
            print(f"\n{name} (CIK: {cik})")

            # Get company info
            self.get_company_submissions(cik)

            # Ask to continue
            proceed = input(f"\nGet XBRL facts for {name}? (y/n): ")
            if proceed.lower() == 'y':
                self.get_company_facts(cik)

    def show_filing_types(self) -> None:
        """Display common SEC filing types"""
        print("\n" + "=" * 80)
        print("📄 COMMON SEC FILING TYPES")
        print("=" * 80)

        for form, description in self.FILING_TYPES.items():
            print(f"\n{form}: {description}")

    def show_capabilities_summary(self) -> None:
        """Display comprehensive summary"""
        print("\n" + "=" * 80)
        print("SEC EDGAR API - REAL ESTATE CAPABILITIES")
        print("=" * 80)

        print("\n📊 DATA SOURCES:")
        print("  • Company submissions (all SEC filings)")
        print("  • XBRL financial data (structured)")
        print("  • Historical filings back to 1994")
        print("  • Real-time filing updates")

        print("\n🏢 AVAILABLE APIs:")
        print("  • Submissions API: All filings by company")
        print("  • Company Facts API: All XBRL data for company")
        print("  • Company Concept API: Single concept historical data")
        print("  • Frames API: Cross-company comparisons")

        print("\n💰 KEY FILING TYPES:")
        for form, desc in list(self.FILING_TYPES.items())[:5]:
            print(f"  • {form}: {desc}")

        print("\n🏗️  REAL ESTATE XBRL CONCEPTS:")
        for concept, desc in list(self.REAL_ESTATE_CONCEPTS.items())[:5]:
            print(f"  • {concept}: {desc}")

        print("\n⚡ API CHARACTERISTICS:")
        print("  • No API key required")
        print("  • Rate limit: 10 requests/second")
        print("  • User-Agent header REQUIRED")
        print("  • JSON format responses")

        print("\n🎯 REAL ESTATE USE CASES:")
        print("  ✓ REIT Analysis: Financial performance, property values")
        print("  ✓ Competitor Intelligence: Monitor competitor filings")
        print("  ✓ Market Research: Commercial real estate sector trends")
        print("  ✓ Due Diligence: Detailed financial statements")
        print("  ✓ Insider Trading: Track insider transactions (Form 4)")
        print("  ✓ Ownership: Institutional holdings (13F)")

        print("\n⚠️  IMPORTANT:")
        print("  • Must include identifying User-Agent header")
        print("  • Respect Fair Access guidelines")
        print("  • CIK numbers must be 10 digits with leading zeros")

        print("\n" + "=" * 80)


def main():
    """Run SEC EDGAR API exploration"""
    print(f"\n🔍 SEC EDGAR API Explorer")
    print(f"📅 Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    explorer = SECEdgarAPIExplorer()

    # Show capabilities
    explorer.show_capabilities_summary()

    # Show filing types
    print("\n\n" + "="*80)
    input("Press Enter to see filing types...")
    explorer.show_filing_types()

    # Explore REITs
    print("\n\n" + "="*80)
    explore = input("\nExplore sample REIT data? (y/n): ")
    if explore.lower() == 'y':
        explorer.explore_reit_data()

    # Custom CIK lookup
    print("\n\n" + "="*80)
    custom = input("\nLookup custom company by CIK? (y/n): ")
    if custom.lower() == 'y':
        cik = input("Enter CIK (e.g., 0000879101 for Simon Property): ")
        explorer.get_company_submissions(cik)

        facts = input("\nGet XBRL facts for this company? (y/n): ")
        if facts.lower() == 'y':
            explorer.get_company_facts(cik)

    print("\n✅ Exploration complete!\n")
    print("ℹ️  Note: SEC provides bulk data downloads at:")
    print("   https://www.sec.gov/dera/data/financial-statement-data-sets.html")


if __name__ == "__main__":
    main()
