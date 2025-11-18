"""
Enhanced Platform Example
Demonstrates new features: behavior prediction, market directions, multi-agent LLM
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from enhanced_orchestrator import EnhancedExtremeEventsOrchestrator


def print_section(title):
    """Print formatted section header"""
    print("\n" + "="*80)
    print(f"{title:^80}")
    print("="*80 + "\n")


def example_cyber_attack_analysis():
    """Example: Cyber attack analysis with enhanced features"""
    print_section("ENHANCED EXAMPLE: CYBER ATTACK ANALYSIS")

    orchestrator = EnhancedExtremeEventsOrchestrator(enable_llm=False)  # Set to True if Ollama installed

    # Define cyber attack event
    cyber_event = {
        'attack_type': 'infrastructure_hack',
        'target_sector': 'finance',
        'affected_companies': ['Major Bank A', 'Payment Processor B', 'Exchange C'],
        'data_compromised': True,
        'systems_down': True,
        'ransom_amount_usd': 50e6,
        'recovery_time_estimate_hours': 72,
        'attribution': 'nation-state',
        'cascading_effects': True,
        'geographic_scope': 'national',
        'severity': 4,
        'data_quality': 'high'
    }

    # Run comprehensive analysis
    result = orchestrator.comprehensive_analysis('cyber_attack', cyber_event, use_llm_agents=False)

    # Display results
    print("\n" + "-"*80)
    print("1. NORMALIZED EVENT CHARACTERISTICS")
    print("-"*80)
    event_norm = result['normalized_event']
    print(f"Event Category: {event_norm['category']}")
    print(f"Severity: {event_norm['severity']}/5")
    print(f"Fear Factor: {event_norm['fear_factor']:.2f}")
    print(f"Anger Factor: {event_norm['anger_factor']:.2f}")
    print(f"Uncertainty Factor: {event_norm['uncertainty_factor']:.2f}")

    print("\n" + "-"*80)
    print("2. HUMAN BEHAVIOR PREDICTIONS")
    print("-"*80)
    behavior = result['human_behavior']['individual_behavior']
    print(f"Dominant Emotion: {behavior['dominant_emotion'].upper()}")
    print(f"Emotion Intensity: {behavior['emotion_intensity']:.0%}")
    print(f"Risk Tolerance Change: {behavior['risk_tolerance_change']:.2f}")
    print(f"Time Horizon Shift: {behavior['time_horizon_shift']}")
    print("\nBehavioral Patterns:")
    for pattern in behavior['behavioral_patterns'][:5]:
        print(f"  • {pattern}")

    print("\n" + "-"*80)
    print("3. CROWD PSYCHOLOGY")
    print("-"*80)
    crowd = result['human_behavior']['crowd_psychology']
    print(f"Herd Behavior Probability: {crowd['herd_behavior_probability']:.0%}")
    print(f"Panic Cascade Probability: {crowd['panic_cascade_probability']:.0%}")
    print(f"Cascade Speed: {crowd['cascade_speed_hours']} hours")
    print(f"Social Amplification Factor: {crowd['social_amplification_factor']:.2f}x")

    print("\n" + "-"*80)
    print("4. MARKET DIRECTIONS - WINNERS")
    print("-"*80)
    for winner in result['market_directions']['winners'][:5]:
        print(f"✓ {winner['name']:30} +{winner['expected_change_pct']:>6.1f}%  ({winner['rationale']})")

    print("\n" + "-"*80)
    print("5. MARKET DIRECTIONS - LOSERS")
    print("-"*80)
    for loser in result['market_directions']['losers'][:5]:
        print(f"✗ {loser['name']:30} {loser['expected_change_pct']:>6.1f}%  ({loser['rationale']})")

    print("\n" + "-"*80)
    print("6. TRADING OPPORTUNITIES")
    print("-"*80)
    for i, opp in enumerate(result['trading_opportunities'][:5], 1):
        print(f"\n{i}. {opp['type'].upper()}: {opp['asset']}")
        print(f"   Expected Return: {opp['expected_return']:.1f}%")
        print(f"   Confidence: {opp['confidence']:.0%}")
        print(f"   Risk Level: {opp['risk_level']}")
        print(f"   Rationale: {opp['rationale']}")

    print("\n" + "-"*80)
    print("7. HEDGING STRATEGIES")
    print("-"*80)
    for i, hedge in enumerate(result['hedging_strategies'], 1):
        print(f"\n{i}. {hedge['strategy']}")
        print(f"   Allocation: {hedge['allocation']}")
        print(f"   Effectiveness: {hedge['effectiveness']}")
        print(f"   Rationale: {hedge['rationale']}")

    print("\n" + "-"*80)
    print("8. ACTIONABLE INTELLIGENCE")
    print("-"*80)
    intel = result['actionable_intelligence']
    print(f"Action Urgency: {intel['action_urgency']}")
    print("\nImmediate Actions:")
    for action in intel['immediate_actions']:
        print(f"  → {action}")

    print("\nMonitoring Priorities:")
    for priority in intel['monitoring_priorities']:
        print(f"  • {priority}")

    # Export summary
    print("\n" + "-"*80)
    print("9. EXECUTIVE SUMMARY")
    print("-"*80)
    summary = orchestrator.export_comprehensive_report(result, format='summary')
    print(summary)


def example_compound_event():
    """Example: Compound event (multiple simultaneous crises)"""
    print_section("ENHANCED EXAMPLE: COMPOUND EVENT (POLYCRISIS)")

    orchestrator = EnhancedExtremeEventsOrchestrator(enable_llm=False)

    # Define compound event: Pandemic + Economic Crisis + Supply Chain Collapse
    compound_event = {
        'primary_events': ['pandemic', 'economic_crisis', 'supply_chain_collapse'],
        'event_details': [
            {'type': 'pandemic', 'severity': 4},
            {'type': 'economic_crisis', 'severity': 5},
            {'type': 'supply_chain', 'severity': 4}
        ],
        'interaction_type': 'reinforcing',  # Events amplify each other
        'total_severity': 5,
        'systemic_stress': 0.9,
        'geographic_scope': 'global',
        'data_quality': 'medium'
    }

    result = orchestrator.comprehensive_analysis('compound_event', compound_event, use_llm_agents=False)

    print("SYNTHESIS:")
    synthesis = result['synthesis']
    print(f"Overall Sentiment: {synthesis['overall_sentiment'].upper()}")
    print(f"Market Impact Estimate: {synthesis['market_impact_estimate']:.1f}%")
    print(f"Severity: {synthesis['severity_score']}/5")

    print("\nKEY INSIGHTS:")
    for insight in synthesis['key_insights']:
        print(f"  • {insight}")

    print("\nCOMPONENTS USED:")
    for component in synthesis['components_used']:
        if component:
            print(f"  ✓ {component}")


def example_climate_crisis():
    """Example: Climate crisis analysis"""
    print_section("ENHANCED EXAMPLE: CLIMATE CRISIS")

    orchestrator = EnhancedExtremeEventsOrchestrator(enable_llm=False)

    climate_event = {
        'crisis_type': 'extreme_heat',
        'temperature_anomaly': 2.5,  # +2.5°C
        'duration_months': 18,
        'affected_regions': ['Europe', 'North America', 'Asia'],
        'agricultural_impact': 'severe',
        'infrastructure_risk': 'high',
        'migration_pressure': True,
        'tipping_point_risk': True,
        'geographic_scope': 'global',
        'severity': 4,
        'data_quality': 'high'
    }

    result = orchestrator.comprehensive_analysis('climate_crisis', climate_event, use_llm_agents=False)

    print("MARKET DIRECTIONS:")
    print("\nWINNERS (Green Transition):")
    for winner in result['market_directions']['winners'][:4]:
        print(f"  + {winner['name']:25} {winner['expected_change_pct']:>5.1f}%")

    print("\nLOSERS (Stranded Assets):")
    for loser in result['market_directions']['losers'][:4]:
        print(f"  - {loser['name']:25} {loser['expected_change_pct']:>5.1f}%")

    print("\nHUMAN BEHAVIOR:")
    behavior = result['human_behavior']['individual_behavior']
    print(f"  Dominant Emotion: {behavior['dominant_emotion']}")
    print(f"  Risk Tolerance Change: {behavior['risk_tolerance_change']:.2f}")


def example_comparison_of_events():
    """Compare multiple event types"""
    print_section("ENHANCED EXAMPLE: MULTI-EVENT COMPARISON")

    orchestrator = EnhancedExtremeEventsOrchestrator(enable_llm=False)

    events = [
        ('cyber_attack', {'attack_type': 'ransomware', 'target_sector': 'healthcare', 'severity': 3}),
        ('climate_crisis', {'crisis_type': 'drought', 'duration_months': 12, 'severity': 3}),
        ('pandemic', {'r0': 2.5, 'mortality_rate': 0.01, 'vaccine_availability': False, 'severity': 4}),
    ]

    results = []
    for event_type, event_data in events:
        event_data['data_quality'] = 'medium'
        event_data['geographic_scope'] = 'regional'
        result = orchestrator.comprehensive_analysis(event_type, event_data, use_llm_agents=False)
        results.append({
            'event_type': event_type,
            'market_impact': result['synthesis']['market_impact_estimate'],
            'severity': result['synthesis']['severity_score'],
            'dominant_emotion': result['human_behavior']['individual_behavior']['dominant_emotion'],
            'top_winner': result['market_directions']['winners'][0]['name'] if result['market_directions']['winners'] else 'N/A',
            'top_loser': result['market_directions']['losers'][0]['name'] if result['market_directions']['losers'] else 'N/A'
        })

    print(f"{'Event Type':<20} {'Impact':>8} {'Severity':>10} {'Emotion':>12} {'Top Winner':>20} {'Top Loser':>20}")
    print("-"*100)
    for r in results:
        print(f"{r['event_type']:<20} {r['market_impact']:>7.1f}% {r['severity']:>9}/5 {r['dominant_emotion']:>12} {r['top_winner']:>20} {r['top_loser']:>20}")


def main():
    """Run all enhanced examples"""
    print("\n" + "#"*80)
    print("#" + " "*78 + "#")
    print("#" + "EXTREME EVENTS PLATFORM - ENHANCED VERSION 2.0".center(78) + "#")
    print("#" + "Demonstrating: Behavior Prediction, Market Directions, Multi-Agent AI".center(78) + "#")
    print("#" + " "*78 + "#")
    print("#"*80)

    # Run examples
    example_cyber_attack_analysis()
    print("\n" + "*"*80 + "\n")

    example_compound_event()
    print("\n" + "*"*80 + "\n")

    example_climate_crisis()
    print("\n" + "*"*80 + "\n")

    example_comparison_of_events()

    print("\n" + "#"*80)
    print("#" + " "*78 + "#")
    print("#" + "ALL ENHANCED EXAMPLES COMPLETED".center(78) + "#")
    print("#" + " "*78 + "#")
    print("#"*80 + "\n")


if __name__ == "__main__":
    main()
