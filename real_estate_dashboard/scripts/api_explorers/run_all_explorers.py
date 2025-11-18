#!/usr/bin/env python3
"""
Master Script - Run All API Explorers
Provides interactive menu to explore all data source APIs
"""

import sys
from datetime import datetime


class MasterExplorer:
    """Interactive menu for all API explorers"""

    EXPLORERS = {
        '1': {
            'name': 'Census Bureau API',
            'module': 'census_api_explorer',
            'description': 'Demographics, housing, and economic data',
            'cost': 'FREE',
            'key_required': True
        },
        '2': {
            'name': 'FRED API',
            'module': 'fred_api_explorer',
            'description': 'Federal Reserve economic indicators',
            'cost': 'FREE',
            'key_required': True
        },
        '3': {
            'name': 'HUD USER API',
            'module': 'hud_api_explorer',
            'description': 'Fair Market Rents and income limits',
            'cost': 'FREE',
            'key_required': True
        },
        '4': {
            'name': 'BLS API',
            'module': 'bls_api_explorer',
            'description': 'Employment, wages, and CPI data',
            'cost': 'FREE',
            'key_required': True
        },
        '5': {
            'name': 'SEC EDGAR API',
            'module': 'sec_edgar_api_explorer',
            'description': 'REIT and company filings',
            'cost': 'FREE',
            'key_required': False
        },
        '6': {
            'name': 'EPA Envirofacts API',
            'module': 'epa_api_explorer',
            'description': 'Environmental hazards and Superfund sites',
            'cost': 'FREE',
            'key_required': False
        },
        '7': {
            'name': 'NOAA Climate API',
            'module': 'noaa_api_explorer',
            'description': 'Weather and climate risk data',
            'cost': 'FREE',
            'key_required': True
        }
    }

    def show_menu(self):
        """Display interactive menu"""
        print("\n" + "=" * 80)
        print(" " * 20 + "🏠 REAL ESTATE DATA SOURCE EXPLORERS")
        print("=" * 80)
        print(f"\n📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        print("\n" + "=" * 80)
        print("AVAILABLE EXPLORERS")
        print("=" * 80)

        for key, explorer in self.EXPLORERS.items():
            key_status = "🔑 Key Required" if explorer['key_required'] else "✓ No Key Needed"
            print(f"\n[{key}] {explorer['name']}")
            print(f"    {explorer['description']}")
            print(f"    Cost: {explorer['cost']} | {key_status}")

        print("\n[0] Exit")
        print("\n" + "=" * 80)

    def run_explorer(self, choice):
        """Run selected explorer"""
        if choice == '0':
            print("\n👋 Goodbye!\n")
            sys.exit(0)

        if choice not in self.EXPLORERS:
            print("\n❌ Invalid choice. Please try again.")
            return

        explorer = self.EXPLORERS[choice]
        module_name = explorer['module']

        print("\n" + "=" * 80)
        print(f"LAUNCHING: {explorer['name']}")
        print("=" * 80)

        try:
            # Import and run the explorer
            module = __import__(module_name)
            module.main()
        except ImportError as e:
            print(f"\n❌ Error: Could not import {module_name}")
            print(f"   Make sure all explorer scripts are in the same directory.")
            print(f"   Details: {e}")
        except Exception as e:
            print(f"\n❌ Error running explorer: {e}")

    def show_summary(self):
        """Show summary of all data sources"""
        print("\n" + "=" * 80)
        print("📊 DATA SOURCE SUMMARY")
        print("=" * 80)

        print("\n🏛️  GOVERNMENT APIS (FREE):")
        print("  • Census Bureau - Demographics, housing, economic data")
        print("  • FRED - 800,000+ economic time series")
        print("  • HUD - Fair market rents, income limits")
        print("  • BLS - Employment, wages, CPI")
        print("  • SEC EDGAR - REIT and company filings")
        print("  • EPA - Environmental hazards")
        print("  • NOAA - Climate and weather data")

        print("\n💰 ALL APIS ARE FREE!")
        print("  Most require simple registration for API key")
        print("  No credit card needed")
        print("  Generous rate limits")

        print("\n📈 REAL ESTATE USE CASES:")
        print("  ✓ Market Analysis - Demographics, economic indicators")
        print("  ✓ Property Valuation - Comparable data, market trends")
        print("  ✓ Risk Assessment - Environmental, climate, economic risks")
        print("  ✓ Investment Analysis - REIT performance, market cycles")
        print("  ✓ Development Planning - Housing needs, demographics")

        print("\n" + "=" * 80)

    def show_api_key_help(self):
        """Show where to get API keys"""
        print("\n" + "=" * 80)
        print("🔑 API KEY REGISTRATION LINKS")
        print("=" * 80)

        print("\nCensus Bureau:")
        print("  https://api.census.gov/data/key_signup.html")

        print("\nFRED (Federal Reserve):")
        print("  https://fredaccount.stlouisfed.org/apikeys")

        print("\nHUD USER:")
        print("  https://www.huduser.gov/hudapi/public/register")

        print("\nBLS (Bureau of Labor Statistics):")
        print("  https://data.bls.gov/registrationEngine/")

        print("\nNOAA Climate Data:")
        print("  https://www.ncdc.noaa.gov/cdo-web/token")

        print("\nSEC EDGAR:")
        print("  No API key required!")

        print("\nEPA Envirofacts:")
        print("  No API key required!")

        print("\n💡 TIP: Sign up for all keys at once - they're all free!")
        print("        Most are emailed to you immediately")

        print("\n" + "=" * 80)

    def run(self):
        """Main interactive loop"""
        print("\n" + "🔍" * 40)
        print(" " * 20 + "REAL ESTATE DATA SOURCE EXPLORER")
        print("🔍" * 40)

        while True:
            self.show_menu()

            choice = input("\n👉 Enter your choice: ").strip()

            if choice == '0':
                print("\n👋 Goodbye!\n")
                break
            elif choice == 's':
                self.show_summary()
            elif choice == 'k':
                self.show_api_key_help()
            elif choice in self.EXPLORERS:
                self.run_explorer(choice)
            else:
                print("\n❌ Invalid choice. Please try again.")

            input("\n\nPress Enter to return to menu...")


def show_quick_start():
    """Show quick start guide"""
    print("\n" + "=" * 80)
    print("🚀 QUICK START GUIDE")
    print("=" * 80)

    print("\n1️⃣  CHOOSE AN EXPLORER")
    print("   Select from the menu to explore a specific API")

    print("\n2️⃣  GET API KEYS (Optional)")
    print("   Most explorers work without keys in demo mode")
    print("   For full access, register for free API keys")

    print("\n3️⃣  RUN THE EXPLORER")
    print("   Follow interactive prompts")
    print("   View available data and endpoints")
    print("   Test sample queries")

    print("\n4️⃣  REVIEW DOCUMENTATION")
    print("   Check /docs/API_RESEARCH_DATA_SOURCES.md for detailed info")
    print("   Read /docs/INTEGRATION_RECOMMENDATIONS.md for implementation guide")

    print("\n5️⃣  INTEGRATE INTO YOUR APP")
    print("   Use exploration scripts as reference")
    print("   Follow integration recommendations")
    print("   Extend existing integration framework")

    print("\n" + "=" * 80)


def main():
    """Run master explorer"""
    show_quick_start()

    explorer = MasterExplorer()

    # Check if specific explorer requested via command line
    if len(sys.argv) > 1:
        choice = sys.argv[1]
        explorer.run_explorer(choice)
    else:
        explorer.run()


if __name__ == "__main__":
    main()
