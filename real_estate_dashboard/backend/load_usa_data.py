#!/usr/bin/env python3
"""
Load USA Economic Data Directly to Database

Script to parse and store provided USA economic data for multiple categories.
"""

import sys
import json
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(parent_dir))

from app.database.country_database_manager import country_db_manager
from app.services.economics_db_service import EconomicsDBService
from app.services.economics_data_parser import EconomicsDataParser


def load_category_data(category: str, data: list, db_service: EconomicsDBService):
    """Load data for a specific category"""
    print(f"\n{'=' * 80}")
    print(f"LOADING USA {category.upper()} DATA")
    print('=' * 80 + '\n')

    # Parse data
    print(f"1. Parsing {category} data...")
    parser = EconomicsDataParser()

    # All categories use the same data format with Related, Last, Previous, etc.
    parsed_data = parser.parse_economic_indicators(data, "United States", category)

    print(f"   ✅ Parsed {len(parsed_data)} indicators")

    # Show sample
    print(f"\n   Sample {category} indicators:")
    for ind in parsed_data[:3]:
        print(f"   - {ind['indicator_name']}: {ind['last_value']}")

    # Save to database
    print(f"\n2. Saving to database...")
    # save_economic_indicators expects raw data, not parsed data
    # It will parse the data itself
    db_service.save_economic_indicators(data, "United States", category)

    print(f"   ✅ Saved {len(parsed_data)} {category} indicators to database")

    # Verify
    print(f"\n3. Verifying data in database...")
    indicators = db_service.get_economic_indicators(
        country="United States",
        category=category,
        limit=5
    )

    if indicators:
        print(f"   ✅ Successfully retrieved {len(indicators)} indicators from database")
        print(f"\n   Sample retrieved {category} indicators:")
        for ind in indicators[:3]:
            print(f"   - {ind.indicator_name}: {ind.last_value}")
        return True
    else:
        print(f"   ⚠️  No indicators found in database")
        return False


def main():
    """Main function"""

    # Check/create database first
    print("\n" + "=" * 80)
    print("INITIALIZING USA DATABASE")
    print("=" * 80 + "\n")

    print("1. Checking United States database...")
    databases = country_db_manager.list_country_databases()
    us_db_exists = any(slug == "united-states" and exists for slug, _, exists in databases)

    if not us_db_exists:
        print("   Creating United States database...")
        success = country_db_manager.initialize_country_database("united-states")
        if success:
            print("   ✅ Database created successfully")
        else:
            print("   ❌ Failed to create database")
            return 1
    else:
        print("   ✅ Database already exists")

    # Get database session
    db = country_db_manager.get_session("united-states")
    db_service = EconomicsDBService(db)

    # DATA TO LOAD
    # ============

    # Overview Data
    usa_overview = [
        {"Highest": "165", "Last": "99.21", "Lowest": "70.7", "Previous": "99.5", "Reference": "Nov/25", "Related": "Currency", "Unit": ""},
        {"Highest": "6922", "Last": "6826", "Lowest": "4.4", "Previous": "6851", "Reference": "Nov/25", "Related": "Stock Market", "Unit": "points"},
        {"Highest": "34.9", "Last": "3.8", "Lowest": "-28", "Previous": "-0.6", "Reference": "Jun/25", "Related": "GDP Growth Rate", "Unit": "percent"},
        {"Highest": "13.4", "Last": "2.1", "Lowest": "-7.4", "Previous": "2", "Reference": "Jun/25", "Related": "GDP Annual Growth Rate", "Unit": "percent"},
        {"Highest": "14.9", "Last": "4.3", "Lowest": "2.5", "Previous": "4.2", "Reference": "Aug/25", "Related": "Unemployment Rate", "Unit": "percent"},
        {"Highest": "4631", "Last": "22", "Lowest": "-20471", "Previous": "79", "Reference": "Aug/25", "Related": "Non Farm Payrolls", "Unit": "Thousand"},
        {"Highest": "23.7", "Last": "3", "Lowest": "-15.8", "Previous": "2.9", "Reference": "Sep/25", "Related": "Inflation Rate", "Unit": "percent"},
        {"Highest": "2", "Last": "0.3", "Lowest": "-1.8", "Previous": "0.4", "Reference": "Sep/25", "Related": "Inflation Rate MoM", "Unit": "percent"},
        {"Highest": "20", "Last": "4", "Lowest": "0.25", "Previous": "4.25", "Reference": "Oct/25", "Related": "Interest Rate", "Unit": "percent"},
        {"Highest": "1.95", "Last": "-78.31", "Lowest": "-136", "Previous": "-59.09", "Reference": "Jul/25", "Related": "Balance of Trade", "Unit": "USD Billion"},
        {"Highest": "9.96", "Last": "-251", "Lowest": "-440", "Previous": "-440", "Reference": "Jun/25", "Related": "Current Account", "Unit": "USD Billion"},
        {"Highest": "0.2", "Last": "-3.9", "Lowest": "-6", "Previous": "-3.3", "Reference": "Dec/24", "Related": "Current Account to GDP", "Unit": "percent of GDP"},
        {"Highest": "126", "Last": "124", "Lowest": "31.8", "Previous": "122", "Reference": "Dec/24", "Related": "Government Debt to GDP", "Unit": "percent of GDP"},
        {"Highest": "4.5", "Last": "-6.4", "Lowest": "-14.7", "Previous": "-6.2", "Reference": "Dec/24", "Related": "Government Budget", "Unit": "percent of GDP"},
        {"Highest": "77.5", "Last": "48.7", "Lowest": "29.4", "Previous": "49.1", "Reference": "Oct/25", "Related": "Business Confidence", "Unit": "points"},
        {"Highest": "63.4", "Last": "52.5", "Lowest": "36.1", "Previous": "52", "Reference": "Oct/25", "Related": "Manufacturing PMI", "Unit": "points"},
        {"Highest": "67.6", "Last": "52.4", "Lowest": "37.8", "Previous": "50", "Reference": "Oct/25", "Related": "Non Manufacturing PMI", "Unit": "points"},
        {"Highest": "70.4", "Last": "54.8", "Lowest": "26.7", "Previous": "54.2", "Reference": "Oct/25", "Related": "Services PMI", "Unit": "points"},
        {"Highest": "111", "Last": "50.3", "Lowest": "50", "Previous": "53.6", "Reference": "Nov/25", "Related": "Consumer Confidence", "Unit": "points"},
        {"Highest": "19.3", "Last": "0.6", "Lowest": "-14.4", "Previous": "0.6", "Reference": "Aug/25", "Related": "Retail Sales MoM", "Unit": "percent"},
        {"Highest": "2419", "Last": "1330", "Lowest": "513", "Previous": "1362", "Reference": "Aug/25", "Related": "Building Permits", "Unit": "Thousand"},
        {"Highest": "52.8", "Last": "21", "Lowest": "1", "Previous": "21", "Reference": "Dec/25", "Related": "Corporate Tax Rate", "Unit": "percent"},
        {"Highest": "39.6", "Last": "37", "Lowest": "35", "Previous": "37", "Reference": "Dec/25", "Related": "Personal Income Tax Rate", "Unit": "percent"}
    ]

    # GDP Data
    usa_gdp = [
        {"Highest": "34.9", "Last": "3.8", "Lowest": "-28", "Previous": "-0.6", "Reference": "Jun/25", "Related": "GDP Growth Rate", "Unit": "percent"},
        {"Highest": "13.4", "Last": "2.1", "Lowest": "-7.4", "Previous": "2", "Reference": "Jun/25", "Related": "GDP Annual Growth Rate", "Unit": "percent"},
        {"Highest": "29185", "Last": "29185", "Lowest": "542", "Previous": "27721", "Reference": "Dec/24", "Related": "GDP", "Unit": "USD Billion"},
        {"Highest": "23771", "Last": "23771", "Lowest": "2172", "Previous": "23548", "Reference": "Jun/25", "Related": "GDP Constant Prices", "Unit": "USD Billion"},
        {"Highest": "23774", "Last": "23774", "Lowest": "2187", "Previous": "23567", "Reference": "Jun/25", "Related": "Gross National Product", "Unit": "USD Billion"},
        {"Highest": "4380", "Last": "4380", "Lowest": "1216", "Previous": "4334", "Reference": "Jun/25", "Related": "Gross Fixed Capital Formation", "Unit": "USD Billion"},
        {"Highest": "66683", "Last": "66683", "Lowest": "18854", "Previous": "65505", "Reference": "Dec/24", "Related": "GDP per Capita", "Unit": "USD"},
        {"Highest": "75492", "Last": "75492", "Lowest": "43742", "Previous": "74159", "Reference": "Dec/24", "Related": "GDP per Capita PPP", "Unit": "USD"},
        {"Highest": "18.9", "Last": "2.8", "Lowest": "-12.9", "Previous": "2.9", "Reference": "Dec/24", "Related": "Full Year GDP Growth", "Unit": "percent"},
        {"Highest": "24.95", "Last": "1.68", "Lowest": "-21.62", "Previous": "0.42", "Reference": "Jun/25", "Related": "GDP Growth Contribution Consumer Spending", "Unit": "percentage points"},
        {"Highest": "4.86", "Last": "-0.2", "Lowest": "-8.71", "Previous": "0.02", "Reference": "Jun/25", "Related": "GDP Growth Contribution Exports", "Unit": "percentage points"},
        {"Highest": "10.01", "Last": "-0.01", "Lowest": "-3.25", "Previous": "-0.17", "Reference": "Jun/25", "Related": "GDP Growth Contribution Government", "Unit": "percentage points"},
        {"Highest": "9.45", "Last": "5.03", "Lowest": "-7.36", "Previous": "-4.7", "Reference": "Jun/25", "Related": "GDP Growth Contribution Imports", "Unit": "percentage points"},
        {"Highest": "14.11", "Last": "-2.66", "Lowest": "-11.57", "Previous": "3.79", "Reference": "Jun/25", "Related": "GDP Growth Contribution Investment", "Unit": "percentage points"},
        {"Highest": "25.2", "Last": "7.5", "Lowest": "-24.6", "Previous": "-3.2", "Reference": "Jun/25", "Related": "GDP Sales QoQ", "Unit": "percent"},
        {"Highest": "40.6", "Last": "2.5", "Lowest": "-30.4", "Previous": "0.6", "Reference": "Jun/25", "Related": "Real Consumer Spending", "Unit": "percent"},
        {"Highest": "10.56", "Last": "2.22", "Lowest": "-8.12", "Previous": "2", "Reference": "Nov/25", "Related": "Weekly Economic Index", "Unit": "percent"},
        {"Highest": "210", "Last": "196", "Lowest": "136", "Previous": "196", "Reference": "Jun/25", "Related": "GDP from Agriculture", "Unit": "USD Billion"},
        {"Highest": "946", "Last": "891", "Lowest": "640", "Previous": "882", "Reference": "Jun/25", "Related": "GDP from Construction", "Unit": "USD Billion"},
        {"Highest": "2405", "Last": "2405", "Lowest": "1808", "Previous": "2338", "Reference": "Jun/25", "Related": "GDP from Manufacturing", "Unit": "USD Billion"},
        {"Highest": "372", "Last": "366", "Lowest": "153", "Previous": "343", "Reference": "Jun/25", "Related": "GDP from Mining", "Unit": "USD Billion"},
        {"Highest": "2624", "Last": "2603", "Lowest": "2355", "Previous": "2624", "Reference": "Jun/25", "Related": "GDP from Public Administration", "Unit": "USD Billion"},
        {"Highest": "17306", "Last": "17306", "Lowest": "10485", "Previous": "17156", "Reference": "Jun/25", "Related": "GDP from Services", "Unit": "USD Billion"},
        {"Highest": "747", "Last": "744", "Lowest": "475", "Previous": "735", "Reference": "Jun/25", "Related": "GDP from Transport", "Unit": "USD Billion"},
        {"Highest": "367", "Last": "341", "Lowest": "238", "Previous": "355", "Reference": "Jun/25", "Related": "GDP from Utilities", "Unit": "USD Billion"}
    ]

    # Labour Data (64 indicators - COMPLETE)
    usa_labour = [
        {"Highest": "14.9", "Last": "4.3", "Lowest": "2.5", "Previous": "4.2", "Reference": "Aug/25", "Related": "Unemployment Rate", "Unit": "percent"},
        {"Highest": "4631", "Last": "22", "Lowest": "-20471", "Previous": "79", "Reference": "Aug/25", "Related": "Non Farm Payrolls", "Unit": "Thousand"},
        {"Highest": "486", "Last": "-16", "Lowest": "-918", "Previous": "2", "Reference": "Aug/25", "Related": "Government Payrolls", "Unit": "Thousand"},
        {"Highest": "4612", "Last": "38", "Lowest": "-19553", "Previous": "77", "Reference": "Aug/25", "Related": "Nonfarm Payrolls Private", "Unit": "Thousand"},
        {"Highest": "655", "Last": "-12", "Lowest": "-1715", "Previous": "-2", "Reference": "Aug/25", "Related": "Manufacturing Payrolls", "Unit": "Thousand"},
        {"Highest": "6137", "Last": "218", "Lowest": "162", "Previous": "232", "Reference": "Sep/25", "Related": "Initial Jobless Claims", "Unit": "Thousand"},
        {"Highest": "23130", "Last": "1926", "Lowest": "988", "Previous": "1928", "Reference": "Sep/25", "Related": "Continuing Jobless Claims", "Unit": "Thousand"},
        {"Highest": "1247", "Last": "42", "Lowest": "-6094", "Previous": "-29", "Reference": "Oct/25", "Related": "ADP Employment Change", "Unit": "Thousand"},
        {"Highest": "163969", "Last": "163394", "Lowest": "57172", "Previous": "163106", "Reference": "Aug/25", "Related": "Employed Persons", "Unit": "Thousand"},
        {"Highest": "23239", "Last": "7384", "Lowest": "1596", "Previous": "7236", "Reference": "Aug/25", "Related": "Unemployed Persons", "Unit": "Thousand"},
        {"Highest": "4.5", "Last": "0.3", "Lowest": "-1.1", "Previous": "0.3", "Reference": "Aug/25", "Related": "Average Hourly Earnings", "Unit": "percent"},
        {"Highest": "35", "Last": "34.2", "Lowest": "33.7", "Previous": "34.2", "Reference": "Aug/25", "Related": "Average Weekly Hours", "Unit": "Hours"},
        {"Highest": "67.3", "Last": "62.3", "Lowest": "58.1", "Previous": "62.2", "Reference": "Aug/25", "Related": "Labor Force Participation Rate", "Unit": "percent"},
        {"Highest": "4.4", "Last": "1.13", "Lowest": "0.08", "Previous": "1.07", "Reference": "Aug/25", "Related": "Long Term Unemployment Rate", "Unit": "percent"},
        {"Highest": "28.5", "Last": "10.5", "Lowest": "4.8", "Previous": "10", "Reference": "Aug/25", "Related": "Youth Unemployment Rate", "Unit": "percent"},
        {"Highest": "124", "Last": "124", "Lowest": "14.98", "Previous": "123", "Reference": "Jun/25", "Related": "Labour Costs", "Unit": "points"},
        {"Highest": "116", "Last": "116", "Lowest": "22.07", "Previous": "115", "Reference": "Jun/25", "Related": "Productivity", "Unit": "points"},
        {"Highest": "12588", "Last": "7235", "Lowest": "2157", "Previous": "7779", "Reference": "Aug/25", "Related": "Job Vacancies", "Unit": "Thousand"},
        {"Highest": "12134", "Last": "7227", "Lowest": "2232", "Previous": "7208", "Reference": "Aug/25", "Related": "Job Offers", "Unit": "Thousand"},
        {"Highest": "671129", "Last": "153074", "Lowest": "14875", "Previous": "54064", "Reference": "Oct/25", "Related": "Challenger Job Cuts", "Unit": "Persons"},
        {"Highest": "31.46", "Last": "31.46", "Lowest": "2.5", "Previous": "31.34", "Reference": "Aug/25", "Related": "Wages", "Unit": "USD/Hour"},
        {"Highest": "7.25", "Last": "7.25", "Lowest": "0.25", "Previous": "7.25", "Reference": "Dec/25", "Related": "Minimum Wages", "Unit": "USD/Hour"},
        {"Highest": "15.54", "Last": "4.86", "Lowest": "-6.12", "Previous": "5.16", "Reference": "Aug/25", "Related": "Wage Growth", "Unit": "percent"},
        {"Highest": "29.03", "Last": "29.03", "Lowest": "0.48", "Previous": "29.01", "Reference": "Aug/25", "Related": "Wages in Manufacturing", "Unit": "USD/Hour"},
        {"Highest": "2", "Last": "0.9", "Lowest": "0.2", "Previous": "0.9", "Reference": "Jun/25", "Related": "Employment Cost Index", "Unit": "percent"},
        {"Highest": "341", "Last": "341", "Lowest": "76.09", "Previous": "339", "Reference": "Dec/24", "Related": "Population", "Unit": "Million"},
        {"Highest": "66.83", "Last": "66.83", "Lowest": "66", "Previous": "66.67", "Reference": "Dec/25", "Related": "Retirement Age Women", "Unit": "Years"},
        {"Highest": "66.83", "Last": "66.83", "Lowest": "66", "Previous": "66.67", "Reference": "Dec/25", "Related": "Retirement Age Men", "Unit": "Years"},
        {"Highest": "14.25", "Last": "-11.25", "Lowest": "-11.25", "Previous": "14.25", "Reference": "Oct/25", "Related": "ADP Employment Change Weekly", "Unit": "Thousand"},
        {"Highest": "84211", "Last": "82933", "Lowest": "55093", "Previous": "82078", "Reference": "Dec/24", "Related": "Average Annual Wages", "Unit": "USD"},
        {"Highest": "8.1", "Last": "3.7", "Lowest": "0.6", "Previous": "3.9", "Reference": "Aug/25", "Related": "Average Hourly Earnings YoY", "Unit": "percent"},
        {"Highest": "57.97", "Last": "44.81", "Lowest": "17.91", "Previous": "45.13", "Reference": "Oct/25", "Related": "Chicago Fed Hiring Rate", "Unit": "percent"},
        {"Highest": "3.98", "Last": "2.1", "Lowest": "1.92", "Previous": "2.09", "Reference": "Oct/25", "Related": "Chicago Fed Layoffs Rate", "Unit": "percent"},
        {"Highest": "482", "Last": "-7", "Lowest": "-1019", "Previous": "-1", "Reference": "Aug/25", "Related": "Construction Payrolls", "Unit": "Thousand"},
        {"Highest": "77716", "Last": "8168", "Lowest": "218", "Previous": "7863", "Reference": "Sep/25", "Related": "Continued Jobless Claims - Federal Workers", "Unit": "People"},
        {"Highest": "3", "Last": "2.6", "Lowest": "1.6", "Previous": "2.4", "Reference": "Oct/25", "Related": "Earnings Growth Expectations", "Unit": "percent"},
        {"Highest": "2.7", "Last": "0.7", "Lowest": "0.1", "Previous": "1.2", "Reference": "Jun/25", "Related": "Employment Cost Index Benefits", "Unit": "percent"},
        {"Highest": "1.6", "Last": "1", "Lowest": "0.2", "Previous": "0.8", "Reference": "Jun/25", "Related": "Employment Cost Index Wages", "Unit": "percent"},
        {"Highest": "432", "Last": "-15", "Lowest": "-240", "Previous": "-10", "Reference": "Aug/25", "Related": "Federal Government Payrolls", "Unit": "Thousand"},
        {"Highest": "50", "Last": "-3", "Lowest": "-265", "Previous": "9", "Reference": "Aug/25", "Related": "Financial Activities Payrolls", "Unit": "Thousand"},
        {"Highest": "6911", "Last": "6911", "Lowest": "2225", "Previous": "6676", "Reference": "Dec/24", "Related": "Gross Average Monthly Wages", "Unit": "USD at Current Exchange Rates"},
        {"Highest": "372", "Last": "30.6", "Lowest": "-1516", "Previous": "51.3", "Reference": "Aug/25", "Related": "Health Care Payrolls", "Unit": "Thousand"},
        {"Highest": "939790", "Last": "283138", "Lowest": "1494", "Previous": "117313", "Reference": "Oct/25", "Related": "Hiring Plans Announcements", "Unit": "Persons"},
        {"Highest": "606", "Last": "-5", "Lowest": "-586", "Previous": "-7", "Reference": "Aug/25", "Related": "Information Payrolls", "Unit": "Thousand"},
        {"Highest": "13516", "Last": "1725", "Lowest": "1287", "Previous": "1787", "Reference": "Aug/25", "Related": "Job Layoffs and Discharges", "Unit": "Thousand"},
        {"Highest": "4499", "Last": "3091", "Lowest": "1555", "Previous": "3166", "Reference": "Aug/25", "Related": "Job Quits", "Unit": "Thousand"},
        {"Highest": "3", "Last": "1.9", "Lowest": "1.2", "Previous": "2", "Reference": "Aug/25", "Related": "Job Quits Rate", "Unit": "Percent"},
        {"Highest": "71442", "Last": "635", "Lowest": "24", "Previous": "572", "Reference": "Sep/25", "Related": "Jobless Claims - Federal Workers", "Unit": "People"},
        {"Highest": "1830", "Last": "28", "Lowest": "-7439", "Previous": "6", "Reference": "Aug/25", "Related": "Leisure and Hospitality Payrolls", "Unit": "Thousand"},
        {"Highest": "155", "Last": "-5.5", "Lowest": "-141", "Previous": "-4.1", "Reference": "Aug/25", "Related": "Mining and Energy Payrolls", "Unit": "Thousand"},
        {"Highest": "20.9", "Last": "3.3", "Lowest": "-11.7", "Previous": "-1.8", "Reference": "Jun/25", "Related": "Nonfarm Productivity QoQ", "Unit": "percent"},
        {"Highest": "358", "Last": "-17", "Lowest": "-2165", "Previous": "-10", "Reference": "Aug/25", "Related": "Professional and Business Services Payrolls", "Unit": "Thousand"},
        {"Highest": "821", "Last": "10.5", "Lowest": "-2186", "Previous": "7.2", "Reference": "Aug/25", "Related": "Retail Trade Payrolls", "Unit": "Thousand"},
        {"Highest": "111", "Last": "16.2", "Lowest": "-655", "Previous": "20.3", "Reference": "Aug/25", "Related": "Social Assistance Payrolls", "Unit": "Thousand"},
        {"Highest": "179", "Last": "3.6", "Lowest": "-514", "Previous": "6.3", "Reference": "Aug/25", "Related": "Transportation and Warehousing Payrolls", "Unit": "Thousand"},
        {"Highest": "23", "Last": "8.1", "Lowest": "6.5", "Previous": "7.9", "Reference": "Aug/25", "Related": "U6 Unemployment Rate", "Unit": "percent"},
        {"Highest": "50.9", "Last": "42.5", "Lowest": "30.7", "Previous": "41.1", "Reference": "Oct/25", "Related": "Unemployment Expectations", "Unit": "percent"},
        {"Highest": "27.3", "Last": "1", "Lowest": "-14.3", "Previous": "6.9", "Reference": "Jun/25", "Related": "Unit Labour Costs QoQ", "Unit": "percent"},
        {"Highest": "41", "Last": "-11.7", "Lowest": "-390", "Previous": "-8.3", "Reference": "Aug/25", "Related": "Wholesale Trade Payrolls", "Unit": "Thousand"},
        {"Highest": "64.7", "Last": "59.6", "Lowest": "51.2", "Previous": "59.6", "Reference": "Aug/25", "Related": "Employment Rate", "Unit": "percent"},
        {"Highest": "135896", "Last": "134480", "Lowest": "64640", "Previous": "134837", "Reference": "Aug/25", "Related": "Full Time Employment", "Unit": "Thousand"},
        {"Highest": "5288", "Last": "238", "Lowest": "179", "Previous": "240", "Reference": "Sep/25", "Related": "Jobless Claims 4-week Average", "Unit": "Thousand"},
        {"Highest": "29034", "Last": "29034", "Lowest": "10086", "Previous": "28437", "Reference": "Aug/25", "Related": "Part Time Employment", "Unit": "Thousand"}
    ]

    # Prices Data (46 indicators - COMPLETE)
    usa_prices = [
        {"Highest": "23.7", "Last": "3", "Lowest": "-15.8", "Previous": "2.9", "Reference": "Sep/25", "Related": "Inflation Rate", "Unit": "percent"},
        {"Highest": "2", "Last": "0.3", "Lowest": "-1.8", "Previous": "0.4", "Reference": "Sep/25", "Related": "Inflation Rate MoM", "Unit": "percent"},
        {"Highest": "325", "Last": "325", "Lowest": "23.5", "Previous": "324", "Reference": "Sep/25", "Related": "Consumer Price Index CPI", "Unit": "points"},
        {"Highest": "331", "Last": "331", "Lowest": "28.5", "Previous": "330", "Reference": "Sep/25", "Related": "Core Consumer Prices", "Unit": "points"},
        {"Highest": "13.6", "Last": "3", "Lowest": "0", "Previous": "3.1", "Reference": "Sep/25", "Related": "Core Inflation Rate", "Unit": "percent"},
        {"Highest": "128", "Last": "128", "Lowest": "11.14", "Previous": "128", "Reference": "Jun/25", "Related": "GDP Deflator", "Unit": "points"},
        {"Highest": "149", "Last": "149", "Lowest": "100", "Previous": "149", "Reference": "Aug/25", "Related": "Producer Prices", "Unit": "points"},
        {"Highest": "19.57", "Last": "2.6", "Lowest": "-6.86", "Previous": "3.1", "Reference": "Aug/25", "Related": "Producer Prices Change", "Unit": "percent"},
        {"Highest": "167", "Last": "153", "Lowest": "82.4", "Previous": "153", "Reference": "Aug/25", "Related": "Export Prices", "Unit": "points"},
        {"Highest": "148", "Last": "141", "Lowest": "75", "Previous": "141", "Reference": "Aug/25", "Related": "Import Prices", "Unit": "points"},
        {"Highest": "36.7", "Last": "3.1", "Lowest": "-34.3", "Previous": "3.2", "Reference": "Sep/25", "Related": "Food Inflation", "Unit": "percent"},
        {"Highest": "1.42", "Last": "0.2", "Lowest": "-0.5", "Previous": "0.3", "Reference": "Sep/25", "Related": "Core Inflation Rate MoM", "Unit": "percent"},
        {"Highest": "10.22", "Last": "2.91", "Lowest": "0.63", "Previous": "2.85", "Reference": "Aug/25", "Related": "Core PCE Price Index Annual Change", "Unit": "percent"},
        {"Highest": "1", "Last": "0.2", "Lowest": "-0.6", "Previous": "0.2", "Reference": "Aug/25", "Related": "Core PCE Price Index MoM", "Unit": "percent"},
        {"Highest": "11.9", "Last": "2.6", "Lowest": "-0.8", "Previous": "3.3", "Reference": "Jun/25", "Related": "Core PCE Prices QoQ", "Unit": "percent"},
        {"Highest": "1.2", "Last": "-0.1", "Lowest": "-0.4", "Previous": "0.7", "Reference": "Aug/25", "Related": "Core Producer Prices MoM", "Unit": "percent"},
        {"Highest": "9.7", "Last": "2.8", "Lowest": "0.2", "Previous": "3.4", "Reference": "Aug/25", "Related": "Core Producer Prices YoY", "Unit": "percent"},
        {"Highest": "324", "Last": "324", "Lowest": "21.48", "Previous": "323", "Reference": "Sep/25", "Related": "CPI seasonally adjusted", "Unit": "points"},
        {"Highest": "47.13", "Last": "2.8", "Lowest": "-28.09", "Previous": "0.2", "Reference": "Sep/25", "Related": "Energy Inflation", "Unit": "Percent"},
        {"Highest": "3.9", "Last": "0.3", "Lowest": "-3.7", "Previous": "0.3", "Reference": "Aug/25", "Related": "Export Prices MoM", "Unit": "percent"},
        {"Highest": "18.6", "Last": "3.4", "Lowest": "-11.8", "Previous": "2.2", "Reference": "Aug/25", "Related": "Export Prices YoY", "Unit": "percent"},
        {"Highest": "3.4", "Last": "0.3", "Lowest": "-7.4", "Previous": "0.2", "Reference": "Aug/25", "Related": "Import Prices MoM", "Unit": "percent"},
        {"Highest": "21.4", "Last": "0", "Lowest": "-19.1", "Previous": "-0.2", "Reference": "Aug/25", "Related": "Import Prices YoY", "Unit": "percent"},
        {"Highest": "4.2", "Last": "3", "Lowest": "2.3", "Previous": "3", "Reference": "Oct/25", "Related": "Inflation Expectations 3Y", "Unit": "percent"},
        {"Highest": "3", "Last": "3", "Lowest": "2", "Previous": "3", "Reference": "Oct/25", "Related": "Inflation Expectations 5Y", "Unit": "percent"},
        {"Highest": "9.7", "Last": "3.6", "Lowest": "2.2", "Previous": "3.9", "Reference": "Nov/25", "Related": "Michigan 5 Year Inflation Expectations", "Unit": "percent"},
        {"Highest": "10.4", "Last": "4.7", "Lowest": "0.4", "Previous": "4.6", "Reference": "Nov/25", "Related": "Michigan Inflation Expectations", "Unit": "percent"},
        {"Highest": "11.6", "Last": "2.74", "Lowest": "-1.47", "Previous": "2.6", "Reference": "Aug/25", "Related": "PCE Price Index Annual Change", "Unit": "percent"},
        {"Highest": "1.2", "Last": "0.3", "Lowest": "-1.2", "Previous": "0.2", "Reference": "Aug/25", "Related": "PCE Price Index Monthly Change", "Unit": "percent"},
        {"Highest": "13.3", "Last": "2.1", "Lowest": "-6.2", "Previous": "3.4", "Reference": "Jun/25", "Related": "PCE Prices QoQ", "Unit": "percent"},
        {"Highest": "137", "Last": "137", "Lowest": "100", "Previous": "136", "Reference": "Aug/25", "Related": "PPI Ex Food Energy and Trade Services", "Unit": "points"},
        {"Highest": "0.9", "Last": "0.3", "Lowest": "-0.8", "Previous": "0.6", "Reference": "Aug/25", "Related": "PPI Ex Food Energy and Trade Services MoM", "Unit": "percent"},
        {"Highest": "7.1", "Last": "2.8", "Lowest": "-0.2", "Previous": "2.7", "Reference": "Aug/25", "Related": "PPI Ex Food Energy and Trade Services YoY", "Unit": "percent"},
        {"Highest": "1.7", "Last": "-0.1", "Lowest": "-1.2", "Previous": "0.7", "Reference": "Aug/25", "Related": "Producer Price Inflation MoM", "Unit": "percent"},
        {"Highest": "20.85", "Last": "3.6", "Lowest": "-0.73", "Previous": "3.6", "Reference": "Sep/25", "Related": "Rent Inflation", "Unit": "percent"},
        {"Highest": "18.09", "Last": "3.6", "Lowest": "0.57", "Previous": "3.8", "Reference": "Sep/25", "Related": "Services Inflation", "Unit": "Percent"},
        {"Highest": "127", "Last": "127", "Lowest": "15.5", "Previous": "126", "Reference": "Aug/25", "Related": "Core PCE Price Index", "Unit": "points"},
        {"Highest": "148", "Last": "148", "Lowest": "99.9", "Previous": "148", "Reference": "Aug/25", "Related": "Core Producer Prices", "Unit": "points"},
        {"Highest": "10.9", "Last": "2.4", "Lowest": "0.3", "Previous": "2.5", "Reference": "Sep/25", "Related": "CPI Core Core", "Unit": "percent"},
        {"Highest": "350", "Last": "350", "Lowest": "30.5", "Previous": "349", "Reference": "Sep/25", "Related": "CPI Housing Utilities", "Unit": "points"},
        {"Highest": "7", "Last": "3.5", "Lowest": "0.5", "Previous": "3.6", "Reference": "Sep/25", "Related": "CPI Median", "Unit": "percent"},
        {"Highest": "285", "Last": "274", "Lowest": "22.3", "Previous": "274", "Reference": "Sep/25", "Related": "CPI Transportation", "Unit": "points"},
        {"Highest": "7.2", "Last": "3.2", "Lowest": "0.7", "Previous": "3.3", "Reference": "Sep/25", "Related": "CPI Trimmed-Mean", "Unit": "percent"},
        {"Highest": "6.8", "Last": "3.2", "Lowest": "2.33", "Previous": "3.4", "Reference": "Oct/25", "Related": "Inflation Expectations", "Unit": "percent"},
        {"Highest": "127", "Last": "127", "Lowest": "15.16", "Previous": "127", "Reference": "Aug/25", "Related": "PCE Price Index", "Unit": "points"}
    ]

    # Health Data (4 indicators - COMPLETE)
    usa_health = [
        {"Highest": "9.18", "Last": "2.75", "Lowest": "2.75", "Previous": "2.77", "Reference": "Dec/22", "Related": "Hospital Beds", "Unit": "per 1000 people"},
        {"Highest": "30.65", "Last": "18.36", "Lowest": "17.13", "Previous": "18.46", "Reference": "Dec/22", "Related": "Hospitals", "Unit": "per one million people"},
        {"Highest": "2.77", "Last": "2.77", "Lowest": "2.27", "Previous": "2.74", "Reference": "Dec/19", "Related": "Medical Doctors", "Unit": "per 1000 people"},
        {"Highest": "12.71", "Last": "12.71", "Lowest": "10.1", "Previous": "12.36", "Reference": "Dec/24", "Related": "Nurses", "Unit": "per 1000 people"}
    ]

    # Money Data (14 indicators - COMPLETE)
    usa_money = [
        {"Highest": "20", "Last": "4", "Lowest": "0.25", "Previous": "4.25", "Reference": "Oct/25", "Related": "Interest Rate", "Unit": "percent"},
        {"Highest": "6413100", "Last": "5478000", "Lowest": "48400", "Previous": "5686100", "Reference": "Sep/25", "Related": "Money Supply M0", "Unit": "USD Million"},
        {"Highest": "20727", "Last": "18913", "Lowest": "139", "Previous": "18836", "Reference": "Sep/25", "Related": "Money Supply M1", "Unit": "USD Billion"},
        {"Highest": "22212", "Last": "22212", "Lowest": "287", "Previous": "22108", "Reference": "Sep/25", "Related": "Money Supply M2", "Unit": "USD Billion"},
        {"Highest": "24535", "Last": "24347", "Lowest": "698", "Previous": "24378", "Reference": "Oct/25", "Related": "Banks Balance Sheet", "Unit": "USD Billion"},
        {"Highest": "8965487", "Last": "6572732", "Lowest": "712809", "Previous": "6587034", "Reference": "Nov/25", "Related": "Central Bank Balance Sheet", "Unit": "USD Million"},
        {"Highest": "54933", "Last": "39205", "Lowest": "0", "Previous": "39161", "Reference": "Sep/25", "Related": "Foreign Exchange Reserves", "Unit": "USD Million"},
        {"Highest": "3034", "Last": "2695", "Lowest": "11.29", "Previous": "2686", "Reference": "Sep/25", "Related": "Loans to Private Sector", "Unit": "USD Billion"},
        {"Highest": "22.36", "Last": "3.87", "Lowest": "0.04", "Previous": "3.87", "Reference": "Nov/25", "Related": "Effective Federal Funds Rate", "Unit": "percent"},
        {"Highest": "29360", "Last": "6785", "Lowest": "6785", "Previous": "6785", "Reference": "Nov/25", "Related": "Fed Capital Account Surplus", "Unit": "USD Million"},
        {"Highest": "17.43", "Last": "3.89", "Lowest": "-1.41", "Previous": "3.92", "Reference": "Oct/25", "Related": "Proxy Funds Rate", "Unit": "percent"},
        {"Highest": "5.4", "Last": "3.98", "Lowest": "0", "Previous": "3.95", "Reference": "Nov/25", "Related": "Secured Overnight Financing Rate", "Unit": "percent"},
        {"Highest": "175162", "Last": "58200", "Lowest": "-310793", "Previous": "-5100", "Reference": "Jul/25", "Related": "Foreign Bond Investment", "Unit": "USD Million"},
        {"Highest": "158", "Last": "142", "Lowest": "100", "Previous": "148", "Reference": "Dec/24", "Related": "Private Debt to GDP", "Unit": "percent"}
    ]

    # Trade Data (24 indicators - COMPLETE)
    usa_trade = [
        {"Highest": "1.95", "Last": "-78.31", "Lowest": "-136", "Previous": "-59.09", "Reference": "Jul/25", "Related": "Balance of Trade", "Unit": "USD Billion"},
        {"Highest": "9.96", "Last": "-251", "Lowest": "-440", "Previous": "-440", "Reference": "Jun/25", "Related": "Current Account", "Unit": "USD Billion"},
        {"Highest": "0.2", "Last": "-3.9", "Lowest": "-6", "Previous": "-3.3", "Reference": "Dec/24", "Related": "Current Account to GDP", "Unit": "percent of GDP"},
        {"Highest": "292", "Last": "280", "Lowest": "0.77", "Previous": "280", "Reference": "Jul/25", "Related": "Exports", "Unit": "USD Billion"},
        {"Highest": "420", "Last": "359", "Lowest": "0.58", "Previous": "339", "Reference": "Jul/25", "Related": "Imports", "Unit": "USD Billion"},
        {"Highest": "28604291", "Last": "28604291", "Lowest": "6570168", "Previous": "28097015", "Reference": "Jun/25", "Related": "External Debt", "Unit": "USD Million"},
        {"Highest": "165", "Last": "109", "Lowest": "89.99", "Previous": "109", "Reference": "Jun/25", "Related": "Terms of Trade", "Unit": "points"},
        {"Highest": "398900", "Last": "2100", "Lowest": "-194622", "Previous": "92100", "Reference": "Jul/25", "Related": "Capital Flows", "Unit": "USD Million"},
        {"Highest": "82453", "Last": "82453", "Lowest": "-9988", "Previous": "64346", "Reference": "Jun/25", "Related": "Foreign Direct Investment", "Unit": "USD Million"},
        {"Highest": "266800", "Last": "49200", "Lowest": "-134889", "Previous": "151000", "Reference": "Jul/25", "Related": "Net Long-term TIC Flows", "Unit": "USD Million"},
        {"Highest": "8149", "Last": "8133", "Lowest": "8133", "Previous": "8133", "Reference": "Sep/25", "Related": "Gold Reserves", "Unit": "Tonnes"},
        {"Highest": "13794", "Last": "13794", "Lowest": "1097", "Previous": "13708", "Reference": "Aug/25", "Related": "Crude Oil Production", "Unit": "BBL/D/1K"},
        {"Highest": "143", "Last": "131", "Lowest": "11.4", "Previous": "127", "Reference": "Jul/25", "Related": "Auto Exports", "Unit": "Thousand"},
        {"Highest": "3.03", "Last": "-270", "Lowest": "-466", "Previous": "-466", "Reference": "Jun/25", "Related": "Current Account Goods", "Unit": "USD Billion"},
        {"Highest": "80.29", "Last": "79.59", "Lowest": "-0.52", "Previous": "80.29", "Reference": "Jun/25", "Related": "Current Account Services", "Unit": "USD Billion"},
        {"Highest": "190082", "Last": "176074", "Lowest": "35404", "Previous": "178371", "Reference": "Aug/25", "Related": "Goods Exports", "Unit": "USD Million"},
        {"Highest": "344592", "Last": "261615", "Lowest": "41371", "Previous": "281211", "Reference": "Aug/25", "Related": "Goods Imports", "Unit": "USD Million"},
        {"Highest": "13651", "Last": "13651", "Lowest": "3813", "Previous": "13644", "Reference": "Oct/25", "Related": "Weekly Crude Oil Production", "Unit": "Thousand Barrels Per Day"},
        {"Highest": "1492", "Last": "-85541", "Lowest": "-161951", "Previous": "-102840", "Reference": "Aug/25", "Related": "Goods Trade Balance", "Unit": "USD Million"},
        {"Highest": "11664", "Last": "7626", "Lowest": "0", "Previous": "7614", "Reference": "Jul/25", "Related": "Oil Exports", "Unit": "USD Million"},
        {"Highest": "7.39", "Last": "3.52", "Lowest": "3.52", "Previous": "4.14", "Reference": "Dec/24", "Related": "Terrorism Index", "Unit": "Points"},
        {"Highest": "21896", "Last": "20626", "Lowest": "3721", "Previous": "20913", "Reference": "Jul/25", "Related": "Tourism Revenues", "Unit": "USD Million"},
        {"Highest": "8418370", "Last": "6275257", "Lowest": "248486", "Previous": "5278944", "Reference": "Jul/25", "Related": "Tourist Arrivals", "Unit": ""},
        {"Highest": "15883", "Last": "13512", "Lowest": "1388", "Previous": "11102", "Reference": "Dec/24", "Related": "Weapons Sales", "Unit": "SIPRI TIV Million"}
    ]

    # Government Data (20 indicators - COMPLETE)
    usa_government = [
        {"Highest": "126", "Last": "124", "Lowest": "31.8", "Previous": "122", "Reference": "Dec/24", "Related": "Government Debt to GDP", "Unit": "percent of GDP"},
        {"Highest": "4.5", "Last": "-6.4", "Lowest": "-14.7", "Previous": "-6.2", "Reference": "Dec/24", "Related": "Government Budget", "Unit": "percent of GDP"},
        {"Highest": "308215", "Last": "197950", "Lowest": "-864074", "Previous": "-344792", "Reference": "Sep/25", "Related": "Government Budget Value", "Unit": "USD Million"},
        {"Highest": "4004", "Last": "3993", "Lowest": "556", "Previous": "3994", "Reference": "Jun/25", "Related": "Government Spending", "Unit": "USD Billion"},
        {"Highest": "863644", "Last": "543663", "Lowest": "33111", "Previous": "344315", "Reference": "Sep/25", "Related": "Government Revenues", "Unit": "USD Million"},
        {"Highest": "38040094", "Last": "38040094", "Lowest": "60000", "Previous": "37637553", "Reference": "Oct/25", "Related": "Government Debt", "Unit": "USD Million"},
        {"Highest": "1104903", "Last": "345713", "Lowest": "3842", "Previous": "689107", "Reference": "Sep/25", "Related": "Fiscal Expenditure", "Unit": "USD Million"},
        {"Highest": "892904", "Last": "892904", "Lowest": "24616", "Previous": "498861", "Reference": "Dec/24", "Related": "Asylum Applications", "Unit": "Persons"},
        {"Highest": "78", "Last": "65", "Lowest": "65", "Previous": "69", "Reference": "Dec/24", "Related": "Corruption Index", "Unit": "Points"},
        {"Highest": "28", "Last": "28", "Lowest": "14", "Previous": "24", "Reference": "Dec/24", "Related": "Corruption Rank", "Unit": ""},
        {"Highest": "", "Last": "97", "Lowest": "", "Previous": "", "Reference": "Nov/25", "Related": "Credit Rating", "Unit": ""},
        {"Highest": "47.01", "Last": "39.7", "Lowest": "6.55", "Previous": "34.38", "Reference": "Dec/24", "Related": "Government Spending to GDP", "Unit": "percent of GDP"},
        {"Highest": "997309", "Last": "997309", "Lowest": "14088", "Previous": "916015", "Reference": "Dec/24", "Related": "Military Expenditure", "Unit": "USD Million"},
        {"Highest": "52.8", "Last": "21", "Lowest": "1", "Previous": "21", "Reference": "Dec/25", "Related": "Corporate Tax Rate", "Unit": "percent"},
        {"Highest": "39.6", "Last": "37", "Lowest": "35", "Previous": "37", "Reference": "Dec/25", "Related": "Personal Income Tax Rate", "Unit": "percent"},
        {"Highest": "0", "Last": "0", "Lowest": "0", "Previous": "0", "Reference": "Dec/25", "Related": "Sales Tax Rate", "Unit": "percent"},
        {"Highest": "16.75", "Last": "15.3", "Lowest": "15.3", "Previous": "15.3", "Reference": "Dec/25", "Related": "Social Security Rate", "Unit": "percent"},
        {"Highest": "10.1", "Last": "7.65", "Lowest": "7.65", "Previous": "7.65", "Reference": "Dec/25", "Related": "Social Security Rate For Companies", "Unit": "percent"},
        {"Highest": "7.65", "Last": "7.65", "Lowest": "6.65", "Previous": "7.65", "Reference": "Dec/25", "Related": "Social Security Rate For Employees", "Unit": "percent"},
        {"Highest": "30", "Last": "30", "Lowest": "30", "Previous": "30", "Reference": "Dec/25", "Related": "Withholding Tax Rate", "Unit": "percent"}
    ]

    # Business Data (96 indicators - COMPLETE)
    usa_business = [
        {"Highest": "77.5", "Last": "48.7", "Lowest": "29.4", "Previous": "49.1", "Reference": "Oct/25", "Related": "Business Confidence", "Unit": "points"},
        {"Highest": "63.4", "Last": "52.5", "Lowest": "36.1", "Previous": "52", "Reference": "Oct/25", "Related": "Manufacturing PMI", "Unit": "points"},
        {"Highest": "67.6", "Last": "52.4", "Lowest": "37.8", "Previous": "50", "Reference": "Oct/25", "Related": "Non Manufacturing PMI", "Unit": "points"},
        {"Highest": "70.4", "Last": "54.8", "Lowest": "26.7", "Previous": "54.2", "Reference": "Oct/25", "Related": "Services PMI", "Unit": "points"},
        {"Highest": "68.7", "Last": "54.6", "Lowest": "27", "Previous": "53.9", "Reference": "Oct/25", "Related": "Composite PMI", "Unit": "points"},
        {"Highest": "62", "Last": "0.9", "Lowest": "-33.7", "Previous": "1.3", "Reference": "Aug/25", "Related": "Industrial Production", "Unit": "percent"},
        {"Highest": "16.6", "Last": "0.1", "Lowest": "-13.2", "Previous": "-0.4", "Reference": "Aug/25", "Related": "Industrial Production Mom", "Unit": "percent"},
        {"Highest": "67.9", "Last": "0.9", "Lowest": "-39.4", "Previous": "1.3", "Reference": "Aug/25", "Related": "Manufacturing Production", "Unit": "percent"},
        {"Highest": "89.4", "Last": "77.4", "Lowest": "64.7", "Previous": "77.4", "Reference": "Aug/25", "Related": "Capacity Utilization", "Unit": "percent"},
        {"Highest": "26.4", "Last": "2.9", "Lowest": "-21.2", "Previous": "-2.7", "Reference": "Aug/25", "Related": "Durable Goods Orders", "Unit": "percent"},
        {"Highest": "29.3", "Last": "1.9", "Lowest": "-22.2", "Previous": "-2.3", "Reference": "Aug/25", "Related": "Durable Goods Orders Ex Defense", "Unit": "percent"},
        {"Highest": "6.3", "Last": "0.4", "Lowest": "-10.2", "Previous": "1", "Reference": "Aug/25", "Related": "Durable Goods Orders Ex Transportation", "Unit": "percent"},
        {"Highest": "5.3", "Last": "0.6", "Lowest": "-9.2", "Previous": "0.4", "Reference": "Jul/25", "Related": "Factory Orders Ex Transportation", "Unit": "percent"},
        {"Highest": "12", "Last": "-1.3", "Lowest": "-14", "Previous": "-4.8", "Reference": "Jul/25", "Related": "Factory Orders", "Unit": "percent"},
        {"Highest": "642533", "Last": "603629", "Lowest": "223500", "Previous": "611471", "Reference": "Jul/25", "Related": "New Orders", "Unit": "USD Million"},
        {"Highest": "2.5", "Last": "0.2", "Lowest": "-2.4", "Previous": "0.2", "Reference": "Jul/25", "Related": "Business Inventories", "Unit": "percent"},
        {"Highest": "227", "Last": "-18.3", "Lowest": "-261", "Previous": "172", "Reference": "Jun/25", "Related": "Changes in Inventories", "Unit": "USD Billion"},
        {"Highest": "2.8", "Last": "-0.2", "Lowest": "-1.9", "Previous": "0", "Reference": "Aug/25", "Related": "Wholesale Inventories", "Unit": "percent"},
        {"Highest": "82446", "Last": "23043", "Lowest": "12748", "Previous": "23309", "Reference": "Jun/25", "Related": "Bankruptcies", "Unit": "Companies"},
        {"Highest": "3271", "Last": "3259", "Lowest": "9.96", "Previous": "3252", "Reference": "Jun/25", "Related": "Corporate Profits", "Unit": "USD Billion"},
        {"Highest": "109", "Last": "98.2", "Lowest": "80.1", "Previous": "98.8", "Reference": "Oct/25", "Related": "NFIB Business Optimism Index", "Unit": "points"},
        {"Highest": "6.31", "Last": "-0.12", "Lowest": "-18.19", "Previous": "-0.28", "Reference": "Aug/25", "Related": "Chicago Fed National Activity Index", "Unit": "points"},
        {"Highest": "47.9", "Last": "-5", "Lowest": "-74.4", "Previous": "-8.7", "Reference": "Oct/25", "Related": "Dallas Fed Manufacturing Index", "Unit": "points"},
        {"Highest": "39", "Last": "10.7", "Lowest": "-79.9", "Previous": "-8.7", "Reference": "Oct/25", "Related": "NY Empire State Manufacturing Index", "Unit": "points"},
        {"Highest": "58.5", "Last": "-12.8", "Lowest": "-60.5", "Previous": "23.2", "Reference": "Oct/25", "Related": "Philadelphia Fed Manufacturing Index", "Unit": "points"},
        {"Highest": "27", "Last": "-4", "Lowest": "-54", "Previous": "-17", "Reference": "Oct/25", "Related": "Richmond Fed Manufacturing Index", "Unit": "points"},
        {"Highest": "81", "Last": "43.8", "Lowest": "20.7", "Previous": "40.6", "Reference": "Oct/25", "Related": "Chicago PMI", "Unit": "points"},
        {"Highest": "13.89", "Last": "11.04", "Lowest": "0.09", "Previous": "10.42", "Reference": "Aug/25", "Related": "Car Production", "Unit": "Million Units"},
        {"Highest": "1213", "Last": "241", "Lowest": "166", "Previous": "222", "Reference": "Aug/25", "Related": "Car Registrations", "Unit": "Thousand"},
        {"Highest": "21.71", "Last": "15.3", "Lowest": "8.59", "Previous": "16.4", "Reference": "Oct/25", "Related": "Total Vehicle Sales", "Unit": "Million"},
        {"Highest": "118", "Last": "98.4", "Lowest": "25.9", "Previous": "98.9", "Reference": "Aug/25", "Related": "Leading Economic Index", "Unit": "points"},
        {"Highest": "6.65", "Last": "6.65", "Lowest": "2.58", "Previous": "6.5", "Reference": "Oct/25", "Related": "Car Loan Delinquency", "Unit": "percent"},
        {"Highest": "1.97", "Last": "-0.07", "Lowest": "-8.96", "Previous": "-0.1", "Reference": "Aug/25", "Related": "CFNAI Employment Index", "Unit": "points"},
        {"Highest": "1.01", "Last": "-0.03", "Lowest": "-1.27", "Previous": "0.02", "Reference": "Aug/25", "Related": "CFNAI Personal Consumption and Housing Index", "Unit": "points"},
        {"Highest": "2.48", "Last": "-0.02", "Lowest": "-5.7", "Previous": "-0.17", "Reference": "Aug/25", "Related": "CFNAI Production Index", "Unit": "percent"},
        {"Highest": "1.37", "Last": "0", "Lowest": "-2.26", "Previous": "-0.02", "Reference": "Aug/25", "Related": "CFNAI Sales Orders and Inventories Index", "Unit": "percent"},
        {"Highest": "148", "Last": "148", "Lowest": "44.91", "Previous": "148", "Reference": "Aug/25", "Related": "Coincident Index", "Unit": "points"},
        {"Highest": "104", "Last": "100", "Lowest": "92.84", "Previous": "100", "Reference": "Oct/25", "Related": "Composite Leading Indicator", "Unit": "points"},
        {"Highest": "31.8", "Last": "2", "Lowest": "-50.2", "Previous": "-3.4", "Reference": "Oct/25", "Related": "Dallas Fed Manufacturing Employment Index", "Unit": "points"},
        {"Highest": "38.6", "Last": "-1.7", "Lowest": "-71.1", "Previous": "-2.6", "Reference": "Oct/25", "Related": "Dallas Fed Manufacturing New Orders Index", "Unit": "points"},
        {"Highest": "83.8", "Last": "33.4", "Lowest": "-47.8", "Previous": "43.4", "Reference": "Oct/25", "Related": "Dallas Fed Manufacturing Prices Paid Index", "Unit": "points"},
        {"Highest": "48.6", "Last": "5.2", "Lowest": "-55.5", "Previous": "5.2", "Reference": "Oct/25", "Related": "Dallas Fed Manufacturing Production Index", "Unit": "points"},
        {"Highest": "47.5", "Last": "5.8", "Lowest": "-58.5", "Previous": "6.7", "Reference": "Oct/25", "Related": "Dallas Fed Manufacturing Shipments Index", "Unit": "points"},
        {"Highest": "43.2", "Last": "-9.4", "Lowest": "-83", "Previous": "-5.6", "Reference": "Oct/25", "Related": "Dallas Fed Services Index", "Unit": "points"},
        {"Highest": "38.8", "Last": "-6.4", "Lowest": "-66.8", "Previous": "-2.4", "Reference": "Oct/25", "Related": "Dallas Fed Services Revenues Index", "Unit": "points"},
        {"Highest": "70.6", "Last": "47.9", "Lowest": "23.4", "Previous": "46.2", "Reference": "Oct/25", "Related": "ISM Manufacturing Backlog of Orders", "Unit": "points"},
        {"Highest": "73.7", "Last": "46", "Lowest": "27.8", "Previous": "45.3", "Reference": "Oct/25", "Related": "ISM Manufacturing Employment", "Unit": "points"},
        {"Highest": "57", "Last": "45.8", "Lowest": "42.3", "Previous": "47.7", "Reference": "Oct/25", "Related": "ISM Manufacturing Inventories", "Unit": "points"},
        {"Highest": "82.6", "Last": "49.4", "Lowest": "24.2", "Previous": "48.9", "Reference": "Oct/25", "Related": "ISM Manufacturing New Orders", "Unit": "points"},
        {"Highest": "92.1", "Last": "58", "Lowest": "17.1", "Previous": "61.9", "Reference": "Oct/25", "Related": "ISM Manufacturing Prices", "Unit": "points"},
        {"Highest": "84", "Last": "48.2", "Lowest": "27.4", "Previous": "51", "Reference": "Oct/25", "Related": "ISM Manufacturing Production", "Unit": "points"},
        {"Highest": "78.8", "Last": "54.2", "Lowest": "43.5", "Previous": "52.6", "Reference": "Oct/25", "Related": "ISM Manufacturing Supplier Deliveries", "Unit": "points"},
        {"Highest": "70.4", "Last": "54.3", "Lowest": "26.1", "Previous": "49.9", "Reference": "Oct/25", "Related": "ISM Non Manufacturing Business Activity", "Unit": "points"},
        {"Highest": "60.3", "Last": "48.2", "Lowest": "29.3", "Previous": "47.2", "Reference": "Oct/25", "Related": "ISM Non Manufacturing Employment", "Unit": "points"},
        {"Highest": "69.2", "Last": "56.2", "Lowest": "33", "Previous": "50.4", "Reference": "Oct/25", "Related": "ISM Non Manufacturing New Orders", "Unit": "points"},
        {"Highest": "84.5", "Last": "70", "Lowest": "36.1", "Previous": "69.4", "Reference": "Oct/25", "Related": "ISM Non Manufacturing Prices", "Unit": "points"},
        {"Highest": "31", "Last": "6", "Lowest": "-30", "Previous": "4", "Reference": "Oct/25", "Related": "Kansas Fed Composite Index", "Unit": "points"},
        {"Highest": "35", "Last": "1", "Lowest": "-38", "Previous": "7", "Reference": "Oct/25", "Related": "Kansas Fed Employment Index", "Unit": "points"},
        {"Highest": "40", "Last": "1", "Lowest": "-60", "Previous": "2", "Reference": "Oct/25", "Related": "Kansas Fed New Orders Index", "Unit": "points"},
        {"Highest": "85", "Last": "41", "Lowest": "-33", "Previous": "40", "Reference": "Oct/25", "Related": "Kansas Fed Prices Paid Index", "Unit": "points"},
        {"Highest": "40", "Last": "15", "Lowest": "-62", "Previous": "7", "Reference": "Oct/25", "Related": "Kansas Fed Shipments Index", "Unit": "points"},
        {"Highest": "17.3", "Last": "0.2", "Lowest": "-15.4", "Previous": "-0.1", "Reference": "Aug/25", "Related": "Manufacturing Production MoM", "Unit": "Percent"},
        {"Highest": "9.5", "Last": "0.6", "Lowest": "-10.8", "Previous": "0.8", "Reference": "Aug/25", "Related": "Non Defense Capital Goods Orders Ex Aircraft", "Unit": "percent"},
        {"Highest": "23.9", "Last": "6.2", "Lowest": "-54", "Previous": "-1.2", "Reference": "Oct/25", "Related": "NY Empire State Employment Index", "Unit": "points"},
        {"Highest": "42", "Last": "3.7", "Lowest": "-69.1", "Previous": "-19.6", "Reference": "Oct/25", "Related": "NY Empire State New Orders Index", "Unit": "points"},
        {"Highest": "86.4", "Last": "52.4", "Lowest": "-18.2", "Previous": "46.1", "Reference": "Oct/25", "Related": "NY Empire State Prices Paid Index", "Unit": "points"},
        {"Highest": "49.6", "Last": "14.4", "Lowest": "-70.9", "Previous": "-17.3", "Reference": "Oct/25", "Related": "NY Empire State Shipments Index", "Unit": "points"},
        {"Highest": "43.2", "Last": "-23.6", "Lowest": "-76.5", "Previous": "-19.4", "Reference": "Oct/25", "Related": "NY Fed Services Activity Index", "Unit": "points"},
        {"Highest": "91", "Last": "36.2", "Lowest": "-39.7", "Previous": "31.5", "Reference": "Oct/25", "Related": "Philly Fed Business Conditions", "Unit": "points"},
        {"Highest": "51.1", "Last": "25.2", "Lowest": "-18.7", "Previous": "12.5", "Reference": "Oct/25", "Related": "Philly Fed CAPEX Index", "Unit": "points"},
        {"Highest": "41.1", "Last": "4.6", "Lowest": "-51.8", "Previous": "5.6", "Reference": "Oct/25", "Related": "Philly Fed Employment", "Unit": "points"},
        {"Highest": "56.2", "Last": "18.2", "Lowest": "-70.4", "Previous": "12.4", "Reference": "Oct/25", "Related": "Philly Fed New Orders", "Unit": "points"},
        {"Highest": "91.1", "Last": "49.2", "Lowest": "-35.5", "Previous": "46.8", "Reference": "Oct/25", "Related": "Philly Fed Prices Paid", "Unit": "points"},
        {"Highest": "97.3", "Last": "95.33", "Lowest": "66.9", "Previous": "90.04", "Reference": "Dec/25", "Related": "Prospective Plantings Corn", "Unit": "Million Acres"},
        {"Highest": "16.2", "Last": "9.87", "Lowest": "8.81", "Previous": "10.67", "Reference": "Dec/25", "Related": "Prospective Plantings Cotton", "Unit": "Million Acres"},
        {"Highest": "90.96", "Last": "83.5", "Lowest": "32", "Previous": "86.51", "Reference": "Dec/25", "Related": "Prospective Plantings Soy", "Unit": "Million Acres"},
        {"Highest": "77.55", "Last": "45.35", "Lowest": "11.6", "Previous": "47.5", "Reference": "Dec/25", "Related": "Prospective Plantings Wheat", "Unit": "Million Acres"},
        {"Highest": "3.8", "Last": "0.3", "Lowest": "-2.1", "Previous": "0.2", "Reference": "Aug/25", "Related": "Retail Inventories Ex Autos", "Unit": "percent"},
        {"Highest": "36", "Last": "4", "Lowest": "-71", "Previous": "-20", "Reference": "Oct/25", "Related": "Richmond Fed Manufacturing Shipments", "Unit": "points"},
        {"Highest": "33", "Last": "4", "Lowest": "-87", "Previous": "1", "Reference": "Oct/25", "Related": "Richmond Fed Services Index", "Unit": "points"},
        {"Highest": "12.52", "Last": "1.53", "Lowest": "1.24", "Previous": "4.64", "Reference": "Sep/25", "Related": "Grain Stocks Corn", "Unit": "Billion Bushels"},
        {"Highest": "3.74", "Last": "0.32", "Lowest": "0.09", "Previous": "1.01", "Reference": "Sep/25", "Related": "Grain Stocks Soy", "Unit": "Billion Bushels"},
        {"Highest": "2.53", "Last": "2.12", "Lowest": "0.58", "Previous": "0.85", "Reference": "Sep/25", "Related": "Grain Stocks Wheat", "Unit": "Billion Bushels"},
        {"Highest": "37", "Last": "15", "Lowest": "-65", "Previous": "4", "Reference": "Oct/25", "Related": "Kansas Fed Manufacturing Index", "Unit": "points"},
        {"Highest": "91", "Last": "73.2", "Lowest": "55.8", "Previous": "75.5", "Reference": "Oct/25", "Related": "LMI Inventory Costs", "Unit": "points"},
        {"Highest": "76.2", "Last": "57.4", "Lowest": "45.4", "Previous": "57.4", "Reference": "Oct/25", "Related": "LMI Logistics Managers Index", "Unit": "points"},
        {"Highest": "73.6", "Last": "64.6", "Lowest": "49.6", "Previous": "59.6", "Reference": "Oct/25", "Related": "LMI Logistics Managers Index Future", "Unit": "points"},
        {"Highest": "95.81", "Last": "61.7", "Lowest": "27.9", "Previous": "54.2", "Reference": "Oct/25", "Related": "LMI Transportation Prices", "Unit": "points"},
        {"Highest": "90.5", "Last": "67.7", "Lowest": "58.97", "Previous": "66", "Reference": "Oct/25", "Related": "LMI Warehouse Prices", "Unit": "points"},
        {"Highest": "108", "Last": "1", "Lowest": "-28.8", "Previous": "1.4", "Reference": "Aug/25", "Related": "Mining Production", "Unit": "percent"},
        {"Highest": "11951", "Last": "6900", "Lowest": "3799", "Previous": "7200", "Reference": "Sep/25", "Related": "Steel Production", "Unit": "Thousand Tonnes"}
    ]

    # Consumer Data (30 indicators - NOTE: provided in previous session but not accessible after summary)
    # This category was received but needs to be re-provided
    usa_consumer = []

    # Housing Data (36 indicators - COMPLETE)
    usa_housing = [
        {"Highest": "2419", "Last": "1330", "Lowest": "513", "Previous": "1362", "Reference": "Aug/25", "Related": "Building Permits", "Unit": "Thousand"},
        {"Highest": "2494", "Last": "1307", "Lowest": "478", "Previous": "1429", "Reference": "Aug/25", "Related": "Housing Starts", "Unit": "Thousand units"},
        {"Highest": "1389", "Last": "800", "Lowest": "270", "Previous": "664", "Reference": "Aug/25", "Related": "New Home Sales", "Unit": "Thousand units"},
        {"Highest": "52.4", "Last": "-0.9", "Lowest": "-36.8", "Previous": "3.8", "Reference": "Sep/25", "Related": "Pending Home Sales", "Unit": "percent"},
        {"Highest": "7250", "Last": "4060", "Lowest": "1370", "Previous": "4000", "Reference": "Sep/25", "Related": "Existing Home Sales", "Unit": "Thousand"},
        {"Highest": "5.9", "Last": "-0.1", "Lowest": "-4.8", "Previous": "-0.4", "Reference": "Jul/25", "Related": "Construction Spending", "Unit": "percent"},
        {"Highest": "437", "Last": "435", "Lowest": "100", "Previous": "434", "Reference": "Aug/25", "Related": "Housing Index", "Unit": "points"},
        {"Highest": "90", "Last": "37", "Lowest": "8", "Previous": "32", "Reference": "Oct/25", "Related": "Nahb Housing Market Index", "Unit": "points"},
        {"Highest": "10.56", "Last": "6.34", "Lowest": "2.85", "Previous": "6.31", "Reference": "Nov/25", "Related": "Mortgage Rate", "Unit": "percent"},
        {"Highest": "112", "Last": "0.6", "Lowest": "-40.5", "Previous": "-1.9", "Reference": "Nov/25", "Related": "Mortgage Applications", "Unit": "percent"},
        {"Highest": "8.89", "Last": "5.5", "Lowest": "2.1", "Previous": "5.41", "Reference": "Nov/25", "Related": "15 Year Mortgage Rate", "Unit": "percent"},
        {"Highest": "18.63", "Last": "6.22", "Lowest": "2.65", "Previous": "6.17", "Reference": "Nov/25", "Related": "30 Year Mortgage Rate", "Unit": "percent"},
        {"Highest": "568700", "Last": "534100", "Lowest": "39500", "Previous": "478200", "Reference": "Aug/25", "Related": "Average House Prices", "Unit": "USD"},
        {"Highest": "460", "Last": "379", "Lowest": "98.5", "Previous": "374", "Reference": "Sep/25", "Related": "Average Mortgage Size", "Unit": "Thousand USD"},
        {"Highest": "33.9", "Last": "-2.3", "Lowest": "-24", "Previous": "-2.2", "Reference": "Aug/25", "Related": "Building Permits MoM", "Unit": "percent"},
        {"Highest": "3.1", "Last": "-0.6", "Lowest": "-2.8", "Previous": "-0.3", "Reference": "Aug/25", "Related": "Case Shiller Home Price Index MoM", "Unit": "percent"},
        {"Highest": "21.3", "Last": "1.6", "Lowest": "-19", "Previous": "1.8", "Reference": "Aug/25", "Related": "Case Shiller Home Price Index YoY", "Unit": "percent"},
        {"Highest": "22.4", "Last": "1.5", "Lowest": "-22.5", "Previous": "-0.2", "Reference": "Sep/25", "Related": "Existing Home Sales MoM", "Unit": "percent"},
        {"Highest": "1.8", "Last": "0.4", "Lowest": "-1.8", "Previous": "0", "Reference": "Aug/25", "Related": "House Price Index MoM", "Unit": "percent"},
        {"Highest": "19.1", "Last": "2.3", "Lowest": "-10.5", "Previous": "2.4", "Reference": "Aug/25", "Related": "House Price Index YoY", "Unit": "percent"},
        {"Highest": "29.3", "Last": "-8.5", "Lowest": "-26.4", "Previous": "3.4", "Reference": "Aug/25", "Related": "Housing Starts MoM", "Unit": "percent"},
        {"Highest": "1000", "Last": "403", "Lowest": "53", "Previous": "453", "Reference": "Aug/25", "Related": "Housing Starts Multi Family", "Unit": "Thousand units"},
        {"Highest": "1823", "Last": "890", "Lowest": "353", "Previous": "957", "Reference": "Aug/25", "Related": "Housing Starts Single Family", "Unit": "Thousand units"},
        {"Highest": "1857", "Last": "334", "Lowest": "64.2", "Previous": "332", "Reference": "Nov/25", "Related": "MBA Mortgage Market Index", "Unit": "points"},
        {"Highest": "9978", "Last": "1248", "Lowest": "59", "Previous": "1291", "Reference": "Nov/25", "Related": "MBA Mortgage Refinance Index", "Unit": "points"},
        {"Highest": "529", "Last": "173", "Lowest": "53.5", "Previous": "163", "Reference": "Nov/25", "Related": "MBA Purchase Index", "Unit": "points"},
        {"Highest": "1218", "Last": "512", "Lowest": "286", "Previous": "458", "Reference": "Sep/25", "Related": "Mortgage Originations", "Unit": "Billion USD"},
        {"Highest": "330", "Last": "327", "Lowest": "25.42", "Previous": "326", "Reference": "Aug/25", "Related": "National Home Price Index", "Unit": "points"},
        {"Highest": "31.2", "Last": "20.5", "Lowest": "-33.6", "Previous": "-1.8", "Reference": "Aug/25", "Related": "New Home Sales MoM", "Unit": "percent"},
        {"Highest": "40.5", "Last": "0", "Lowest": "-30.3", "Previous": "4.2", "Reference": "Sep/25", "Related": "Pending Home Sales MoM", "Unit": "percent"},
        {"Highest": "4040", "Last": "1550", "Lowest": "860", "Previous": "1530", "Reference": "Sep/25", "Related": "Total Housing Inventory", "Unit": "Thousands"},
        {"Highest": "343", "Last": "340", "Lowest": "100", "Previous": "342", "Reference": "Aug/25", "Related": "Case Shiller Home Price Index", "Unit": "points"},
        {"Highest": "69.2", "Last": "65", "Lowest": "62.9", "Previous": "65.1", "Reference": "Jun/25", "Related": "Home Ownership Rate", "Unit": "percent"},
        {"Highest": "432700", "Last": "415200", "Lowest": "19700", "Previous": "422600", "Reference": "Sep/25", "Related": "Single Family Home Prices", "Unit": "USD"},
        {"Highest": "140", "Last": "134", "Lowest": "88.72", "Previous": "133", "Reference": "Dec/24", "Related": "Price to Rent Ratio", "Unit": ""},
        {"Highest": "18.4", "Last": "1.66", "Lowest": "-16.84", "Previous": "2.45", "Reference": "Jun/25", "Related": "Residential Property Prices", "Unit": "Percent"}
    ]

    # Load all 10 available categories
    # Note: consumer category (30 indicators) still needs to be provided
    categories_data = [
        ("overview", usa_overview),
        ("gdp", usa_gdp),
        ("labour", usa_labour),
        ("prices", usa_prices),
        ("health", usa_health),
        ("money", usa_money),
        ("trade", usa_trade),
        ("government", usa_government),
        ("business", usa_business),
        ("housing", usa_housing)
    ]

    results = {}
    for category, data in categories_data:
        try:
            success = load_category_data(category, data, db_service)
            results[category] = success
        except Exception as e:
            print(f"\n❌ Error loading {category}: {str(e)}")
            import traceback
            traceback.print_exc()
            results[category] = False

    # Summary
    print("\n" + "=" * 80)
    print("LOADING SUMMARY")
    print("=" * 80 + "\n")

    all_success = True
    for category, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{status}: {category.upper()}")
        if not success:
            all_success = False

    print("\n" + "=" * 80)

    if all_success:
        print("✅ ALL DATA LOADED SUCCESSFULLY!")
        print("\nYou can now run analysis commands like:")
        print("  python3 analyze_economics.py analyze united-states")
        print("  python3 analyze_economics.py indices united-states")
        print("  python3 analyze_economics.py risk united-states --type recession")
        print("  python3 analyze_economics.py calc mortgage --loan_amount 500000 --rate 7.0")
        return 0
    else:
        print("⚠️  SOME DATA FAILED TO LOAD")
        print("\nCheck the errors above and retry.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
