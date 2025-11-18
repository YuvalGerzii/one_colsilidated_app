"""
Example: NLP, News Analysis, and Economic Event Prediction (V3.0)

This example demonstrates the new V3.0 features:
1. NLP sentiment analysis on news articles
2. Real-time news analysis and event prediction
3. Economic event analysis (recession, inflation, interest rates)
4. MCP (Model Context Protocol) integration
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from enhanced_orchestrator import EnhancedExtremeEventsOrchestrator
from nlp.sentiment_analyzer import FinancialNLPAnalyzer
from nlp.news_analyzer import RealTimeNewsAnalyzer
import json


def example_1_recession_analysis_with_news():
    """
    Example 1: Recession prediction with real-time news analysis
    """
    print("\n" + "="*80)
    print("EXAMPLE 1: RECESSION PREDICTION WITH NEWS ANALYSIS")
    print("="*80)

    # Initialize orchestrator with NLP enabled
    orchestrator = EnhancedExtremeEventsOrchestrator(
        enable_llm=False,  # Disable LLM for faster example
        enable_nlp=True    # Enable NLP and news analysis
    )

    # Simulate recent news headlines about recession
    news_items = [
        "Federal Reserve signals concern over slowing GDP growth and rising unemployment",
        "Yield curve inverts for third consecutive month, raising recession fears",
        "Consumer confidence plunges to lowest level since 2020 pandemic",
        "Manufacturing PMI drops below 50, indicating contraction in factory activity",
        "Economists warn: Multiple recession indicators flashing red",
        "Stock market crashes 5% as investors flee to safe haven assets",
        "Jobless claims surge unexpectedly, Sahm Rule threshold approached",
        "GDP contracts for second consecutive quarter, technical recession confirmed"
    ]

    # Event data for recession analysis
    recession_data = {
        'name': 'US Economic Recession 2024',
        'description': 'Potential US recession based on leading indicators',

        # Leading indicators
        'yield_curve_spread': -0.5,  # Inverted (10Y - 2Y)
        'unemployment_rate': 4.5,
        'unemployment_3month_avg': 4.2,
        'gdp_q1': -0.5,
        'gdp_q2': -0.3,
        'consumer_confidence': 75,
        'pmi': 48,

        # Additional context
        'region': 'United States',
        'affected_population': 330_000_000,
        'sectors_affected': ['all'],
        'severity': 4
    }

    # Run comprehensive analysis with news
    result = orchestrator.comprehensive_analysis(
        event_type='recession',
        event_data=recession_data,
        news_items=news_items,
        use_llm_agents=False
    )

    # Display results
    print("\n" + "-"*80)
    print("ANALYSIS RESULTS")
    print("-"*80)

    # News Analysis Results
    if result.get('news_analysis'):
        print("\n📰 NEWS ANALYSIS:")
        news_analysis = result['news_analysis']

        # Aggregate sentiment
        if 'aggregate_sentiment' in news_analysis:
            agg_sent = news_analysis['aggregate_sentiment']
            print(f"  Overall Sentiment: {agg_sent['sentiment'].upper()}")
            print(f"  Sentiment Score: {agg_sent['average_score']:.2f} (-1 to +1)")
            print(f"  Confidence: {agg_sent['average_confidence']:.1f}%")

        # Event warnings detected from news
        if result.get('event_warnings'):
            print(f"\n  ⚠️  Event Warnings Detected: {len(result['event_warnings'])}")
            for warning in result['event_warnings'][:3]:
                print(f"    • {warning.event_type}: {warning.probability:.1%} probability")
                print(f"      Severity: {warning.severity_estimate}/5")

        # Trading signals from news
        if 'trading_signals' in news_analysis:
            signals = news_analysis['trading_signals']
            print(f"\n  📊 Trading Signals from News: {len(signals)}")
            for signal in signals[:3]:
                print(f"    • {signal.signal_type.upper()}: {signal.asset_class}")
                print(f"      Strength: {signal.strength:.1%} | Rationale: {signal.rationale}")

    # Agent Analysis
    print("\n🤖 RECESSION AGENT ANALYSIS:")
    agent_analysis = result['agent_analysis']
    predictions = agent_analysis.get('predictions', {})
    print(f"  Recession Probability: {predictions.get('recession_probability', 0):.1%}")
    print(f"  Recession Phase: {predictions.get('recession_phase', 'unknown').upper()}")
    print(f"  Market Impact: {predictions.get('market_impact_pct', 0):.1f}%")

    # Synthesis
    print("\n📊 SYNTHESIS:")
    synthesis = result['synthesis']
    print(f"  Overall Sentiment: {synthesis['overall_sentiment'].upper()}")
    print(f"  Market Impact Estimate: {synthesis['market_impact_estimate']:.1f}%")
    print(f"  Severity Score: {synthesis['severity_score']}/5")

    print("\n  Key Insights:")
    for insight in synthesis['key_insights']:
        print(f"    • {insight}")

    # Market Directions
    print("\n📈 MARKET DIRECTIONS:")
    market_dirs = result['market_directions']
    print(f"  Winners ({len(market_dirs['winners'])}):")
    for winner in market_dirs['winners'][:3]:
        print(f"    + {winner['name']}: +{winner['expected_change_pct']:.0f}% ({winner['rationale']})")

    print(f"\n  Losers ({len(market_dirs['losers'])}):")
    for loser in market_dirs['losers'][:3]:
        print(f"    - {loser['name']}: {loser['expected_change_pct']:.0f}% ({loser['rationale']})")

    # Actionable Intelligence
    print("\n💡 ACTIONABLE INTELLIGENCE:")
    intel = result['actionable_intelligence']
    print(f"  Action Urgency: {intel['action_urgency']}")
    print(f"  Immediate Actions:")
    for action in intel['immediate_actions']:
        print(f"    → {action}")

    return result


def example_2_inflation_surge_analysis():
    """
    Example 2: Inflation surge with Fed rate response
    """
    print("\n\n" + "="*80)
    print("EXAMPLE 2: INFLATION SURGE AND FED RESPONSE")
    print("="*80)

    orchestrator = EnhancedExtremeEventsOrchestrator(
        enable_llm=False,
        enable_nlp=True
    )

    # News about inflation
    news_items = [
        "CPI surges to 6.5%, highest level in 40 years",
        "Federal Reserve Chairman signals aggressive rate hikes ahead",
        "Core PCE inflation remains stubbornly above Fed's 2% target",
        "Wage growth accelerates, raising fears of wage-price spiral",
        "Commodity prices spike as supply chain disruptions persist",
        "Bond market prices in 200 basis points of rate hikes this year",
        "Inflation expectations become unanchored, Fed loses credibility"
    ]

    # Inflation event data
    inflation_data = {
        'name': 'US Inflation Surge 2024',
        'description': 'High inflation forcing Fed response',

        # Inflation metrics
        'cpi': 6.5,
        'core_cpi': 5.8,
        'pce': 6.0,
        'core_pce': 5.5,
        'wage_growth': 5.2,
        'commodity_prices_change': 25.0,

        # Fed metrics
        'current_fed_rate': 2.5,
        'fed_target_rate': 5.0,

        # Context
        'region': 'United States',
        'severity': 4,
        'duration_months': 12
    }

    result = orchestrator.comprehensive_analysis(
        event_type='inflation',
        event_data=inflation_data,
        news_items=news_items,
        use_llm_agents=False
    )

    # Display key results
    print("\n" + "-"*80)
    print("ANALYSIS RESULTS")
    print("-"*80)

    # Agent predictions
    print("\n🏦 INFLATION AGENT ANALYSIS:")
    predictions = result['agent_analysis'].get('predictions', {})
    print(f"  Inflation Level: {predictions.get('inflation_level', 'unknown').upper()}")
    print(f"  Market Impact: {predictions.get('market_impact_pct', 0):.1f}%")
    print(f"  Rate Hikes Needed: {predictions.get('rate_hikes_needed', 0)}")
    print(f"  Time to Control: {predictions.get('time_to_control_months', 0)} months")

    # News sentiment
    if result.get('news_analysis', {}).get('aggregate_sentiment'):
        sent = result['news_analysis']['aggregate_sentiment']
        print(f"\n📰 News Sentiment: {sent['sentiment'].upper()} ({sent['average_score']:.2f})")

    # Market directions
    print("\n📈 INFLATION WINNERS & LOSERS:")
    print("  Winners:")
    for winner in result['market_directions']['winners'][:3]:
        print(f"    + {winner['name']}: +{winner['expected_change_pct']:.0f}%")

    print("\n  Losers:")
    for loser in result['market_directions']['losers'][:3]:
        print(f"    - {loser['name']}: {loser['expected_change_pct']:.0f}%")

    return result


def example_3_interest_rate_shock():
    """
    Example 3: Surprise interest rate change
    """
    print("\n\n" + "="*80)
    print("EXAMPLE 3: SURPRISE INTEREST RATE HIKE")
    print("="*80)

    orchestrator = EnhancedExtremeEventsOrchestrator(
        enable_llm=False,
        enable_nlp=True
    )

    news_items = [
        "BREAKING: Fed raises rates by 75 basis points, largest hike in decades",
        "Market shocked by aggressive Fed action, stocks plunge 3%",
        "Fed signals more hikes coming as inflation fight intensifies",
        "Bond yields surge across the curve following surprise hike",
        "Dollar strengthens to 20-year high after hawkish Fed decision"
    ]

    rate_change_data = {
        'name': 'Fed Emergency Rate Hike',
        'description': 'Surprise 75bp rate hike',

        'rate_change_bps': 75,  # Basis points
        'new_rate': 3.25,
        'old_rate': 2.50,
        'surprise_factor': 0.8,  # 0-1, how unexpected
        'direction': 'hike',

        # Forward guidance
        'forward_guidance': 'hawkish',
        'terminal_rate_estimate': 5.0,

        'region': 'United States',
        'severity': 3
    }

    result = orchestrator.comprehensive_analysis(
        event_type='interest_rate_change',
        event_data=rate_change_data,
        news_items=news_items,
        use_llm_agents=False
    )

    # Display results
    print("\n" + "-"*80)
    print("ANALYSIS RESULTS")
    print("-"*80)

    print("\n💵 INTEREST RATE AGENT ANALYSIS:")
    predictions = result['agent_analysis'].get('predictions', {})
    print(f"  Market Impact: {predictions.get('market_impact_pct', 0):.1f}%")
    print(f"  Surprise Multiplier: {predictions.get('surprise_multiplier', 1.0):.2f}x")

    # Sector impacts
    if 'sector_impacts' in predictions:
        print("\n  Sector Impacts:")
        for sector, impact in list(predictions['sector_impacts'].items())[:5]:
            print(f"    {sector}: {impact:+.1f}%")

    print("\n📈 Rate Hike Impact by Asset Class:")
    for winner in result['market_directions']['winners'][:2]:
        print(f"  + {winner['name']}: +{winner['expected_change_pct']:.0f}%")
    for loser in result['market_directions']['losers'][:3]:
        print(f"  - {loser['name']}: {loser['expected_change_pct']:.0f}%")

    return result


def example_4_nlp_only():
    """
    Example 4: Pure NLP analysis without full event analysis
    """
    print("\n\n" + "="*80)
    print("EXAMPLE 4: STANDALONE NLP ANALYSIS")
    print("="*80)

    # Initialize NLP components
    nlp_analyzer = FinancialNLPAnalyzer()
    news_analyzer = RealTimeNewsAnalyzer(nlp_analyzer)

    # Mixed news stream
    news_items = [
        "Stock market rallies on strong earnings, tech sector leads gains",
        "Federal Reserve warns of recession risks amid persistent inflation",
        "Banking crisis fears subside as regulators step in",
        "Unemployment rate drops to 50-year low, labor market remains tight",
        "Geopolitical tensions escalate, oil prices spike 10%",
        "Housing market crash intensifies, prices down 20% year-over-year",
        "Corporate bankruptcies surge to highest level since 2009"
    ]

    print("\n📰 ANALYZING NEWS STREAM...")
    print("-"*80)

    # Analyze each headline
    for i, headline in enumerate(news_items, 1):
        analysis = nlp_analyzer.analyze_text(headline)
        print(f"\n{i}. {headline}")
        print(f"   Sentiment: {analysis.sentiment.upper()} ({analysis.score:+.2f})")
        print(f"   Urgency: {analysis.urgency}")
        print(f"   Topics: {', '.join(analysis.topics)}")

    # Aggregate analysis
    print("\n\n" + "-"*80)
    print("AGGREGATE ANALYSIS")
    print("-"*80)

    stream_analysis = news_analyzer.analyze_news_stream(news_items)

    # Overall sentiment
    agg_sent = stream_analysis['aggregate_sentiment']
    print(f"\nOverall Sentiment: {agg_sent['sentiment'].upper()}")
    print(f"Average Score: {agg_sent['average_score']:.2f}")
    print(f"Confidence: {agg_sent['average_confidence']:.0f}%")

    # Event warnings
    warnings = stream_analysis['warnings']
    print(f"\n⚠️  Event Warnings Detected: {len(warnings)}")
    for warning in warnings:
        print(f"  • {warning.event_type.upper()}")
        print(f"    Probability: {warning.probability:.1%}")
        print(f"    Severity: {warning.severity_estimate}/5")
        print(f"    Indicators: {', '.join(warning.indicators)}")

    # Trading signals
    signals = stream_analysis['trading_signals']
    print(f"\n📊 Trading Signals: {len(signals)}")
    for signal in signals[:5]:
        print(f"  • {signal.signal_type.upper()}: {signal.asset_class}")
        print(f"    Strength: {signal.strength:.1%}")
        print(f"    Rationale: {signal.rationale}")

    return stream_analysis


def main():
    """Run all examples"""
    print("\n" + "="*80)
    print("EXTREME EVENTS PLATFORM V3.0 - NLP & ECONOMIC EVENTS EXAMPLES")
    print("="*80)

    # Run examples
    try:
        result1 = example_1_recession_analysis_with_news()
        result2 = example_2_inflation_surge_analysis()
        result3 = example_3_interest_rate_shock()
        result4 = example_4_nlp_only()

        print("\n\n" + "="*80)
        print("ALL EXAMPLES COMPLETED SUCCESSFULLY")
        print("="*80)

        print("\nV3.0 Features Demonstrated:")
        print("  ✓ NLP sentiment analysis on financial news")
        print("  ✓ Real-time event prediction from news streams")
        print("  ✓ Recession probability analysis with leading indicators")
        print("  ✓ Inflation analysis with Fed response modeling")
        print("  ✓ Interest rate shock analysis")
        print("  ✓ News-based trading signals")
        print("  ✓ Event warning system")
        print("  ✓ Integration with existing extreme events framework")

    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
