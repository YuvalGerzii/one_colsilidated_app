#!/usr/bin/env python3
"""
Economics Analysis CLI Tool

Comprehensive economic analysis and calculators.

Usage Examples:
    # Core Analysis
    python3 analyze_economics.py analyze united-states
    python3 analyze_economics.py compare united-states china japan --indicator "GDP Growth Rate"
    python3 analyze_economics.py housing united-states
    python3 analyze_economics.py trends united-states "GDP Growth Rate"
    python3 analyze_economics.py correlate united-states "House Prices" "GDP Growth Rate"

    # Composite Indices
    python3 analyze_economics.py indices united-states
    python3 analyze_economics.py indices united-states --type misery

    # Financial Calculators
    python3 analyze_economics.py calc mortgage --loan_amount 300000 --rate 6.5
    python3 analyze_economics.py calc affordability --income 100000 --down_payment 60000
    python3 analyze_economics.py calc rent_vs_buy --home_price 400000 --rent 2000

    # Risk Assessments
    python3 analyze_economics.py risk united-states
    python3 analyze_economics.py risk united-states --type recession

    # Advanced Economic Models
    python3 analyze_economics.py models united-states taylor
    python3 analyze_economics.py models united-states phillips
    python3 analyze_economics.py models united-states okun
"""

import sys
import os
import asyncio
import argparse
import json
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(parent_dir))

from app.database.country_database_manager import country_db_manager
from app.services.economics_db_service import EconomicsDBService
from app.services.economic_analyzer import EconomicAnalyzer
from app.services.country_comparator import CountryComparator
from app.services.trend_analyzer import TrendAnalyzer
from app.services.correlation_analyzer import CorrelationAnalyzer
from app.services.housing_market_analyzer import HousingMarketAnalyzer
from app.services.composite_indices import CompositeIndicesCalculator
from app.services.financial_calculators import FinancialCalculators
from app.services.inflation_calculator import InflationCalculator
from app.services.risk_calculators import RiskCalculators
from app.services.advanced_models import AdvancedEconomicModels


def print_section(title: str):
    """Print formatted section header"""
    print("\n" + "=" * 80)
    print(f" {title}")
    print("=" * 80 + "\n")


def print_json(data: dict, indent: int = 2):
    """Print formatted JSON"""
    print(json.dumps(data, indent=indent, default=str))


def analyze_country(country_slug: str, output_format: str = "text"):
    """Analyze a country's economic indicators"""
    print_section(f"Economic Analysis: {country_slug.replace('-', ' ').title()}")

    # Get database and services
    db = country_db_manager.get_session(country_slug)
    db_service = EconomicsDBService(db)
    analyzer = EconomicAnalyzer(db_service)

    country_name = country_db_manager.COUNTRY_NAMES.get(country_slug, country_slug)

    # Perform analysis
    analysis = analyzer.analyze_country(country_name)

    if output_format == "json":
        print_json(analysis)
        return

    # Text output
    print(f"📊 Country: {analysis['country']}")
    print(f"📅 Analysis Date: {analysis['analysis_date']}")

    # Summary
    print_section("Summary")
    summary = analysis.get("summary", {})
    print(f"Overall Health: {summary.get('overall_health', 'unknown').upper()}")
    print(f"Health Score: {summary.get('health_score', 0)}/100")
    print(f"Total Indicators: {summary.get('total_indicators_analyzed', 0)}")
    print(f"  • Leading: {summary.get('leading_count', 0)}")
    print(f"  • Coincident: {summary.get('coincident_count', 0)}")
    print(f"  • Lagging: {summary.get('lagging_count', 0)}")
    print(f"\n{summary.get('message', '')}")

    # Top indicators by category
    print_section("Key Indicators by Type")

    print("📈 LEADING INDICATORS (Predict 6-12 months ahead):")
    for ind in analysis.get("leading_indicators", [])[:5]:
        signal = ind.get("signal", "neutral")
        emoji = "📈" if signal in ["very_positive", "positive"] else "📉" if signal in ["very_negative", "negative"] else "➡️"
        print(f"  {emoji} {ind['indicator']}: {ind['current_value']:.2f}")

    print("\n⚡ COINCIDENT INDICATORS (Reflect current conditions):")
    for ind in analysis.get("coincident_indicators", [])[:5]:
        signal = ind.get("signal", "neutral")
        emoji = "📈" if signal in ["very_positive", "positive"] else "📉" if signal in ["very_negative", "negative"] else "➡️"
        print(f"  {emoji} {ind['indicator']}: {ind['current_value']:.2f}")

    print("\n📊 LAGGING INDICATORS (Confirm trends):")
    for ind in analysis.get("lagging_indicators", [])[:5]:
        signal = ind.get("signal", "neutral")
        emoji = "📈" if signal in ["very_positive", "positive"] else "📉" if signal in ["very_negative", "negative"] else "➡️"
        print(f"  {emoji} {ind['indicator']}: {ind['current_value']:.2f}")


def compare_countries(
    country_slugs: list,
    indicator_name: str,
    category: str = "gdp"
):
    """Compare countries on a specific indicator"""
    countries = [
        country_db_manager.COUNTRY_NAMES.get(slug, slug)
        for slug in country_slugs
    ]

    print_section(f"Country Comparison: {indicator_name}")

    comparator = CountryComparator()
    comparison = comparator.compare_indicator(countries, indicator_name, category)

    print(f"Indicator: {comparison['indicator']}")
    print(f"Category: {comparison['category']}\n")

    # Rankings
    rankings = comparison.get("rankings", {})
    if rankings and "ranked_list" in rankings:
        print("📊 RANKINGS:")
        for ranked in rankings["ranked_list"]:
            print(f"  #{ranked['rank']} {ranked['country']:20} - {ranked['value']:.2f}")

        print(f"\n📈 Highest: {rankings['highest']['country']} ({rankings['highest']['value']:.2f})")
        print(f"📉 Lowest: {rankings['lowest']['country']} ({rankings['lowest']['value']:.2f})")
        print(f"📊 Average: {rankings['average']:.2f}")
        print(f"📊 Spread: {rankings['spread_pct']:.1f}%")

    # Insights
    print("\n💡 INSIGHTS:")
    for insight in comparison.get("insights", []):
        print(f"  • {insight}")


def analyze_housing(country_slug: str):
    """Analyze housing market for a country"""
    country_name = country_db_manager.COUNTRY_NAMES.get(country_slug, country_slug)

    print_section(f"Housing Market Analysis: {country_name}")

    db = country_db_manager.get_session(country_slug)
    db_service = EconomicsDBService(db)
    housing_analyzer = HousingMarketAnalyzer(db_service)

    analysis = housing_analyzer.analyze_housing_market(country_name)

    if "error" in analysis:
        print(f"❌ Error: {analysis['error']}")
        return

    # Market Health
    print(f"🏠 Market Health Score: {analysis['market_health_score']}/100\n")

    # Market Cycle
    cycle = analysis.get("market_cycle", {})
    print(f"📊 Market Cycle: {cycle.get('phase', 'unknown').upper()}")
    print(f"   {cycle.get('interpretation', '')}\n")

    # Affordability
    affordability = analysis.get("affordability", {})
    if affordability and "metrics" in affordability:
        print("💰 AFFORDABILITY:")
        metrics = affordability["metrics"]

        if "price_to_income_ratio" in metrics:
            print(f"  Price-to-Income Ratio: {metrics['price_to_income_ratio']:.1f}x")
            print(f"  Affordability Level: {affordability.get('level', 'unknown').upper()}")

        if "payment_to_income_pct" in metrics:
            print(f"  Monthly Payment Burden: {metrics['payment_to_income_pct']:.1f}% of income")
            print(f"  Burden Level: {metrics.get('burden_level', 'unknown').upper()}")

        if "mortgage_rate" in metrics:
            print(f"  30-Year Mortgage Rate: {metrics['mortgage_rate']:.2f}%")

        print(f"\n  {affordability.get('interpretation', '')}\n")

    # Momentum
    momentum = analysis.get("market_momentum", {})
    if momentum:
        print("📈 MARKET MOMENTUM:")
        print(f"  Overall Momentum: {momentum.get('overall_momentum', 'unknown').upper()}")
        print(f"  Momentum Score: {momentum.get('momentum_score', 0)}/100\n")

        for name, data in momentum.get("indicators", {}).items():
            print(f"  • {name}: {data.get('trend', 'unknown')} (score: {data.get('momentum_score', 0)})")

    # Key Insights
    print("\n💡 KEY INSIGHTS:")
    for insight in analysis.get("key_insights", []):
        print(f"  {insight}")

    # Recommendations
    print("\n📋 RECOMMENDATIONS:")
    for rec in analysis.get("recommendations", []):
        print(f"  • {rec}")


def analyze_trends(country_slug: str, indicator_name: str):
    """Analyze trends for an indicator"""
    country_name = country_db_manager.COUNTRY_NAMES.get(country_slug, country_slug)

    print_section(f"Trend Analysis: {indicator_name} - {country_name}")

    db = country_db_manager.get_session(country_slug)
    db_service = EconomicsDBService(db)
    trend_analyzer = TrendAnalyzer(db_service)

    analysis = trend_analyzer.analyze_trend(country_name, indicator_name, periods=12)

    if "error" in analysis:
        print(f"❌ Error: {analysis['error']}")
        return

    print(f"Indicator: {analysis['indicator']}")
    print(f"Periods Analyzed: {analysis['periods_analyzed']}")
    print(f"Current Value: {analysis['current_value']:.2f}\n")

    # Statistics
    stats = analysis.get("statistics", {})
    print("📊 STATISTICS:")
    print(f"  Mean: {stats.get('mean', 0):.2f}")
    print(f"  Median: {stats.get('median', 0):.2f}")
    print(f"  Std Dev: {stats.get('std_dev', 0):.2f}")
    print(f"  Range: {stats.get('min', 0):.2f} - {stats.get('max', 0):.2f}\n")

    # Trend
    trend = analysis.get("trend", {})
    print("📈 TREND:")
    print(f"  Direction: {trend.get('direction', 'unknown').upper()}")
    print(f"  Strength: {trend.get('strength', 'unknown').upper()}")
    print(f"  Confidence: {trend.get('confidence', 0):.1f}%\n")

    # Growth Rates
    growth = analysis.get("growth_rates", {})
    if growth:
        print("📊 GROWTH RATES:")
        for rate_type, value in growth.items():
            print(f"  {rate_type.replace('_', ' ').title()}: {value:+.2f}%")
        print()

    # Volatility
    volatility = analysis.get("volatility", {})
    if volatility and "classification" in volatility:
        print("📊 VOLATILITY:")
        print(f"  Classification: {volatility.get('classification', 'unknown').upper()}")
        print(f"  Avg Absolute Change: {volatility.get('average_absolute_change', 0):.2f}%\n")

    # Interpretation
    print("💡 INTERPRETATION:")
    print(f"  {analysis.get('interpretation', '')}")

    # Forecast
    forecast = analysis.get("forecast", {})
    if forecast:
        print("\n🔮 FORECAST (Simple Trend-Based):")
        print(f"  Next {forecast.get('periods_ahead', 0)} periods: {forecast.get('forecasted_values', [])}")
        print(f"  ⚠️  {forecast.get('warning', '')}")


def analyze_correlation(
    country_slug: str,
    indicator_x: str,
    indicator_y: str
):
    """Analyze correlation between two indicators"""
    country_name = country_db_manager.COUNTRY_NAMES.get(country_slug, country_slug)

    print_section(f"Correlation Analysis: {country_name}")

    db = country_db_manager.get_session(country_slug)
    db_service = EconomicsDBService(db)
    corr_analyzer = CorrelationAnalyzer(db_service)

    analysis = corr_analyzer.analyze_correlation(
        country_name,
        indicator_x,
        indicator_y,
        periods=12
    )

    if "error" in analysis:
        print(f"❌ Error: {analysis['error']}")
        return

    print(f"Indicator X: {analysis['indicator_x']}")
    print(f"Indicator Y: {analysis['indicator_y']}")
    print(f"Data Points: {analysis['data_points']}\n")

    print("📊 CORRELATION:")
    print(f"  Coefficient: {analysis['correlation_coefficient']:.3f}")
    print(f"  Strength: {analysis['correlation_strength'].upper()}")
    print(f"  Relationship: {analysis['relationship'].upper()}\n")

    if "theoretical_expectation" in analysis:
        print(f"📚 Theory: Expected {analysis['theoretical_expectation']} correlation")
        matches = "✅" if analysis.get("matches_theory") else "⚠️"
        print(f"   {matches} Matches theory: {analysis.get('matches_theory')}\n")

    print("💡 INTERPRETATION:")
    print(f"  {analysis.get('interpretation', '')}")


def calculate_indices(country_slug: str, index_type: str = "all"):
    """Calculate composite economic indices"""
    country_name = country_db_manager.COUNTRY_NAMES.get(country_slug, country_slug)

    db = country_db_manager.get_session(country_slug)
    db_service = EconomicsDBService(db)
    calc = CompositeIndicesCalculator(db_service)

    if index_type == "misery" or index_type == "all":
        print_section(f"Misery Index: {country_name}")
        result = calc.calculate_misery_index(country_name)
        if "error" not in result:
            print(f"{result['emoji']} Misery Index: {result['misery_index']}")
            print(f"Level: {result['level'].upper()}")
            print(f"  Unemployment: {result['components']['unemployment_rate']}%")
            print(f"  Inflation: {result['components']['inflation_rate']}%")
            print(f"\n{result['interpretation']}")

    if index_type == "stability" or index_type == "all":
        print_section(f"Economic Stability Index: {country_name}")
        result = calc.calculate_economic_stability_index(country_name)
        if "error" not in result:
            print(f"{result['emoji']} Stability Index: {result['stability_index']}/100")
            print(f"Level: {result['level'].upper()}")
            print(f"\nComponents:")
            for name, data in result['components'].items():
                print(f"  {name}: {data['score']}/100 (weight: {data['weight']*100:.0f}%)")
            print(f"\n{result['interpretation']}")

    if index_type == "stress" or index_type == "all":
        print_section(f"Consumer Stress Index: {country_name}")
        result = calc.calculate_consumer_stress_index(country_name)
        if "error" not in result:
            print(f"{result['emoji']} Consumer Stress: {result['consumer_stress_index']}/100")
            print(f"Level: {result['level'].upper()}")
            print(f"\n{result['interpretation']}")


def financial_calculator(calc_type: str, **kwargs):
    """Run financial calculators"""
    print_section(f"{calc_type.replace('_', ' ').title()} Calculator")

    if calc_type == "mortgage":
        loan_amount = float(kwargs.get('loan_amount', 300000))
        rate = float(kwargs.get('rate', 6.5))
        years = int(kwargs.get('years', 30))

        result = FinancialCalculators.calculate_mortgage_payment(loan_amount, rate, years)

        print(f"Loan Amount: ${result['loan_amount']:,.0f}")
        print(f"Interest Rate: {result['annual_rate']}%")
        print(f"Term: {result['loan_term_years']} years")
        print(f"\n💰 Monthly Payment: ${result['monthly_payment']:,.2f}")
        print(f"Total Paid: ${result['total_paid']:,.0f}")
        print(f"Total Interest: ${result['total_interest']:,.0f} ({result['interest_as_percentage']}% of loan)")

    elif calc_type == "affordability":
        income = float(kwargs.get('income', 100000))
        down_payment = float(kwargs.get('down_payment', 60000))
        rate = float(kwargs.get('rate', 6.5))

        result = FinancialCalculators.calculate_affordability(income, down_payment=down_payment, interest_rate=rate)

        print(f"Annual Income: ${result['annual_income']:,.0f}")
        print(f"Down Payment: ${result['down_payment']:,.0f}")
        print(f"\n🏠 Maximum Home Price: ${result['max_home_price']:,.0f}")
        print(f"Maximum Loan: ${result['max_loan_amount']:,.0f}")
        print(f"\nMonthly Payment: ${result['monthly_payment_breakdown']['total_housing_payment']:,.0f}")
        print(f"Front-End Ratio: {result['ratios']['front_end_ratio']}%")
        print(f"\n{result['interpretation']}")

    elif calc_type == "rent_vs_buy":
        home_price = float(kwargs.get('home_price', 400000))
        down_payment = float(kwargs.get('down_payment', 80000))
        rate = float(kwargs.get('rate', 6.5))
        rent = float(kwargs.get('rent', 2000))

        result = FinancialCalculators.calculate_rent_vs_buy(home_price, down_payment, rate, rent, years=10)

        print(f"Home Price: ${result['initial_costs']['total_initial_investment']:,.0f}")
        print(f"Monthly Rent: ${rent:,.0f}")
        print(f"\nAfter 10 years:")
        print(f"  Buying: Net position ${result['buying_summary']['net_position']:,.0f}")
        print(f"  Renting: Net position ${result['renting_summary']['net_position']:,.0f}")
        print(f"\n✅ {result['recommendation']}")


def risk_assessment(country_slug: str, risk_type: str = "all"):
    """Calculate risk assessments"""
    country_name = country_db_manager.COUNTRY_NAMES.get(country_slug, country_slug)

    db = country_db_manager.get_session(country_slug)
    db_service = EconomicsDBService(db)
    calc = RiskCalculators(db_service)

    if risk_type == "recession" or risk_type == "all":
        print_section(f"Recession Probability: {country_name}")
        result = calc.calculate_recession_probability(country_name)
        if "error" not in result:
            print(f"{result['emoji']} Recession Probability: {result['recession_probability']}%")
            print(f"Risk Level: {result['risk_level'].upper()}")
            print(f"Risk Score: {result['risk_score']}/{result['max_score']}")
            print(f"\n📋 Risk Factors:")
            for factor in result['risk_factors']:
                print(f"  {factor}")
            print(f"\n💡 {result['interpretation']}")
            print(f"📌 {result['recommendation']}")

    if risk_type == "bubble" or risk_type == "all":
        print_section(f"Housing Bubble Risk: {country_name}")
        result = calc.calculate_housing_bubble_risk(country_name)
        if "error" not in result:
            print(f"{result['emoji']} Bubble Risk Score: {result['bubble_risk_score']}%")
            print(f"Risk Level: {result['risk_level'].upper()}")
            print(f"\n📋 Risk Factors:")
            for factor in result['risk_factors']:
                print(f"  {factor}")
            print(f"\n💡 {result['interpretation']}")
            print(f"📌 {result['recommendation']}")

    if risk_type == "inflation" or risk_type == "all":
        print_section(f"Inflation Risk: {country_name}")
        result = calc.calculate_inflation_risk(country_name)
        if "error" not in result:
            print(f"{result['emoji']} Inflation Risk: {result['inflation_risk_score']}/100")
            print(f"Current Inflation: {result['current_inflation']}%")
            print(f"\n📋 Risk Factors:")
            for factor in result['risk_factors']:
                print(f"  {factor}")
            print(f"\n💡 {result['interpretation']}")


def economic_models(country_slug: str, model_type: str):
    """Calculate advanced economic models"""
    country_name = country_db_manager.COUNTRY_NAMES.get(country_slug, country_slug)

    db = country_db_manager.get_session(country_slug)
    db_service = EconomicsDBService(db)
    calc = AdvancedEconomicModels(db_service)

    if model_type == "taylor":
        print_section(f"Taylor Rule: {country_name}")
        result = calc.calculate_taylor_rule(country_name)
        if "error" not in result:
            print(f"{result['results']['emoji']} Taylor Rule Rate: {result['results']['taylor_rule_rate']}%")
            if result['results']['actual_policy_rate']:
                print(f"Actual Policy Rate: {result['results']['actual_policy_rate']}%")
                print(f"Deviation: {result['results']['rate_deviation']:+.2f}pp")
            print(f"Policy Stance: {result['results']['policy_stance'].upper()}")
            print(f"\n💡 {result['interpretation']}")
            print(f"📌 {result['recommendation']}")

    elif model_type == "phillips":
        print_section(f"Phillips Curve: {country_name}")
        result = calc.analyze_phillips_curve(country_name)
        if "error" not in result:
            print(f"Correlation: {result['correlation']:.3f}")
            print(f"Relationship: {result['relationship'].upper()}")
            print(f"Matches Theory: {'✅ Yes' if result['matches_theory'] else '⚠️ No'}")
            print(f"\nCurrent:")
            print(f"  Unemployment: {result['current_conditions']['unemployment']}%")
            print(f"  Inflation: {result['current_conditions']['inflation']}%")
            print(f"\n💡 {result['interpretation']}")
            print(f"📌 {result['policy_implications']}")

    elif model_type == "okun":
        print_section(f"Okun's Law: {country_name}")
        result = calc.calculate_okuns_law(country_name)
        if "error" not in result:
            print(f"Correlation: {result['correlation']:.3f}")
            print(f"Okun Coefficient: {result['okun_coefficient']:.2f}")
            print(f"Relationship: {result['relationship_strength'].upper()}")
            print(f"Matches Theory: {'✅ Yes' if result['matches_theory'] else '⚠️ No'}")
            print(f"\n💡 {result['interpretation']}")
            print(f"📌 {result['implication']}")

    elif model_type == "output_gap":
        print_section(f"Output Gap: {country_name}")
        result = calc.calculate_output_gap(country_name)
        if "error" not in result:
            print(f"{result['results']['emoji']} Output Gap: {result['results']['output_gap']:+.2f}pp")
            print(f"Actual Growth: {result['inputs']['actual_growth']}%")
            print(f"Potential Growth: {result['inputs']['potential_growth']}%")
            print(f"Status: {result['results']['status'].upper()}")
            print(f"\n💡 {result['interpretation']}")
            print(f"📌 {result['policy_implication']}")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description='Economics Analysis CLI Tool')
    subparsers = parser.add_subparsers(dest='command', help='Analysis command')

    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze a country')
    analyze_parser.add_argument('country', help='Country slug (e.g., united-states)')
    analyze_parser.add_argument('--format', choices=['text', 'json'], default='text')

    # Compare command
    compare_parser = subparsers.add_parser('compare', help='Compare countries')
    compare_parser.add_argument('countries', nargs='+', help='Country slugs')
    compare_parser.add_argument('--indicator', required=True, help='Indicator name')
    compare_parser.add_argument('--category', default='gdp', help='Category')

    # Housing command
    housing_parser = subparsers.add_parser('housing', help='Analyze housing market')
    housing_parser.add_argument('country', help='Country slug')

    # Trends command
    trends_parser = subparsers.add_parser('trends', help='Analyze trends')
    trends_parser.add_argument('country', help='Country slug')
    trends_parser.add_argument('indicator', help='Indicator name')

    # Correlation command
    corr_parser = subparsers.add_parser('correlate', help='Analyze correlation')
    corr_parser.add_argument('country', help='Country slug')
    corr_parser.add_argument('indicator_x', help='First indicator')
    corr_parser.add_argument('indicator_y', help='Second indicator')

    # Indices command
    indices_parser = subparsers.add_parser('indices', help='Calculate composite indices')
    indices_parser.add_argument('country', help='Country slug')
    indices_parser.add_argument('--type', choices=['all', 'misery', 'stability', 'stress'], default='all', help='Index type')

    # Calculator command
    calc_parser = subparsers.add_parser('calc', help='Financial calculators')
    calc_parser.add_argument('calc_type', choices=['mortgage', 'affordability', 'rent_vs_buy'], help='Calculator type')
    calc_parser.add_argument('--loan_amount', type=float, help='Loan amount')
    calc_parser.add_argument('--rate', type=float, help='Interest rate')
    calc_parser.add_argument('--years', type=int, help='Loan term years')
    calc_parser.add_argument('--income', type=float, help='Annual income')
    calc_parser.add_argument('--down_payment', type=float, help='Down payment')
    calc_parser.add_argument('--home_price', type=float, help='Home price')
    calc_parser.add_argument('--rent', type=float, help='Monthly rent')

    # Risk command
    risk_parser = subparsers.add_parser('risk', help='Risk assessments')
    risk_parser.add_argument('country', help='Country slug')
    risk_parser.add_argument('--type', choices=['all', 'recession', 'bubble', 'inflation'], default='all', help='Risk type')

    # Models command
    models_parser = subparsers.add_parser('models', help='Advanced economic models')
    models_parser.add_argument('country', help='Country slug')
    models_parser.add_argument('model_type', choices=['taylor', 'phillips', 'okun', 'output_gap'], help='Model type')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    try:
        if args.command == 'analyze':
            analyze_country(args.country, args.format)
        elif args.command == 'compare':
            compare_countries(args.countries, args.indicator, args.category)
        elif args.command == 'housing':
            analyze_housing(args.country)
        elif args.command == 'trends':
            analyze_trends(args.country, args.indicator)
        elif args.command == 'correlate':
            analyze_correlation(args.country, args.indicator_x, args.indicator_y)
        elif args.command == 'indices':
            calculate_indices(args.country, args.type)
        elif args.command == 'calc':
            kwargs = {k: v for k, v in vars(args).items() if v is not None and k != 'calc_type'}
            financial_calculator(args.calc_type, **kwargs)
        elif args.command == 'risk':
            risk_assessment(args.country, args.type)
        elif args.command == 'models':
            economic_models(args.country, args.model_type)

        return 0

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
