"""
Example Usage of Extreme Events Platform
Demonstrates how to analyze different types of extreme events
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orchestrator import ExtremeEventsOrchestrator


def example_pandemic_analysis():
    """
    Example: Analyzing a pandemic event
    """
    print("\n" + "="*80)
    print("EXAMPLE 1: PANDEMIC ANALYSIS")
    print("="*80)

    orchestrator = ExtremeEventsOrchestrator()

    # Define pandemic event
    pandemic_event = {
        'disease_name': 'Novel Coronavirus',
        'r0': 3.5,  # High transmission rate
        'mortality_rate': 0.02,  # 2% mortality
        'affected_countries': ['USA', 'China', 'Europe', 'India', 'Brazil'],
        'containment_measures': ['lockdown', 'travel_ban', 'social_distancing', 'mask_mandate'],
        'healthcare_capacity': 'medium',
        'vaccine_availability': False,
        'geographic_scope': 'global',
        'data_quality': 'high'
    }

    # Run analysis
    result = orchestrator.analyze_event('pandemic', pandemic_event)

    # Print key results
    print("\n" + "-"*80)
    print("KEY RESULTS")
    print("-"*80)
    print(f"Severity: {result['agent_analysis']['severity_assessment']}/5")
    print(f"Predicted Market Impact: {result['ensemble_predictions']['ensemble_prediction']}%")
    print(f"Risk Level: {result['risk_summary']['overall_risk_level'].upper()}")
    print(f"Recovery Time: {result['risk_summary']['estimated_recovery_days']} days")
    print(f"Confidence: {result['confidence_metrics']['overall_confidence']}%")

    print("\nTop Recommendations:")
    for i, rec in enumerate(result['recommendations'][:3], 1):
        print(f"\n{i}. [{rec['priority'].upper()}] {rec['category']}")
        print(f"   {rec['action']}")

    return result


def example_terrorism_analysis():
    """
    Example: Analyzing a terrorism event
    """
    print("\n" + "="*80)
    print("EXAMPLE 2: TERRORISM ANALYSIS")
    print("="*80)

    orchestrator = ExtremeEventsOrchestrator()

    # Define terrorism event
    terrorism_event = {
        'attack_type': 'bombing',
        'casualties': 150,
        'target_type': 'financial',
        'location': 'New York City',
        'economic_center': True,
        'symbolic_value': 5,
        'claimed_by': 'Unknown',
        'follow_up_threat': True,
        'geographic_scope': 'national',
        'data_quality': 'medium'
    }

    # Run analysis
    result = orchestrator.analyze_event('terrorism', terrorism_event)

    print("\n" + "-"*80)
    print("KEY RESULTS")
    print("-"*80)
    print(f"Severity: {result['agent_analysis']['severity_assessment']}/5")
    print(f"Predicted Market Impact: {result['ensemble_predictions']['ensemble_prediction']}%")
    print(f"Immediate Impact (24h): {result['agent_analysis']['predictions']['market_predictions']['immediate_impact_24h']}%")
    print(f"Risk Level: {result['risk_summary']['overall_risk_level'].upper()}")

    return result


def example_natural_disaster_analysis():
    """
    Example: Analyzing a natural disaster
    """
    print("\n" + "="*80)
    print("EXAMPLE 3: NATURAL DISASTER ANALYSIS")
    print("="*80)

    orchestrator = ExtremeEventsOrchestrator()

    # Define natural disaster event
    disaster_event = {
        'disaster_type': 'hurricane',
        'magnitude': 5.0,  # Category 5
        'affected_area_sq_km': 50000,
        'population_affected': 2000000,
        'infrastructure_damage': 'severe',
        'economic_losses_usd': 75e9,  # $75 billion
        'insurance_coverage': 0.6,
        'location': 'Florida Gulf Coast',
        'industrial_facilities_affected': ['port', 'refinery', 'airport'],
        'geographic_scope': 'regional',
        'data_quality': 'high'
    }

    # Run analysis
    result = orchestrator.analyze_event('natural_disaster', disaster_event)

    print("\n" + "-"*80)
    print("KEY RESULTS")
    print("-"*80)
    print(f"Severity: {result['agent_analysis']['severity_assessment']}/5")
    print(f"Predicted Market Impact: {result['ensemble_predictions']['ensemble_prediction']}%")
    print(f"Infrastructure Damage: {disaster_event['infrastructure_damage']}")
    print(f"Economic Losses: ${disaster_event['economic_losses_usd']/1e9:.1f}B")

    # Reconstruction opportunities
    recon = result['agent_analysis']['predictions'].get('reconstruction_opportunities', [])
    if recon:
        print("\nReconstruction Opportunities:")
        for opp in recon[:3]:
            print(f"  - {opp['sector']}: {opp['opportunity_level']} opportunity, "
                  f"+{opp['estimated_benefit_pct']}% potential benefit")

    return result


def example_economic_crisis_analysis():
    """
    Example: Analyzing an economic crisis
    """
    print("\n" + "="*80)
    print("EXAMPLE 4: ECONOMIC CRISIS ANALYSIS")
    print("="*80)

    orchestrator = ExtremeEventsOrchestrator()

    # Define economic crisis event
    crisis_event = {
        'crisis_type': 'banking_crisis',
        'affected_institutions': ['Major Bank A', 'Investment Bank B', 'Insurance Giant C'],
        'systemic_risk_score': 8.5,
        'credit_market_stress': 'severe',
        'contagion_risk': 0.75,
        'central_bank_response': 'aggressive',
        'fiscal_stimulus': 2e12,  # $2 trillion
        'unemployment_increase': 5.0,
        'gdp_contraction': -8.0,
        'geographic_scope': 'continental',
        'data_quality': 'medium'
    }

    # Run analysis
    result = orchestrator.analyze_event('economic_crisis', crisis_event)

    print("\n" + "-"*80)
    print("KEY RESULTS")
    print("-"*80)
    print(f"Severity: {result['agent_analysis']['severity_assessment']}/5")
    print(f"Predicted Market Impact: {result['ensemble_predictions']['ensemble_prediction']}%")
    print(f"Systemic Risk: {crisis_event['systemic_risk_score']}/10")
    print(f"Contagion Risk: {crisis_event['contagion_risk']*100:.0f}%")

    # Recovery scenarios
    scenarios = result['agent_analysis']['predictions'].get('recovery_scenarios', [])
    if scenarios:
        print("\nRecovery Scenarios (by probability):")
        for scenario in scenarios[:3]:
            print(f"  - {scenario['name']}: {scenario['probability']*100:.0f}% probability, "
                  f"{scenario['timeline_months']} months")

    return result


def example_geopolitical_analysis():
    """
    Example: Analyzing a geopolitical event
    """
    print("\n" + "="*80)
    print("EXAMPLE 5: GEOPOLITICAL EVENT ANALYSIS")
    print("="*80)

    orchestrator = ExtremeEventsOrchestrator()

    # Define geopolitical event
    geopolitical_event = {
        'event_subtype': 'war',
        'countries_involved': ['Country A', 'Country B'],
        'economic_powerhouses_involved': True,
        'nuclear_powers_involved': True,
        'escalation_potential': 7.5,
        'resource_access_impact': 'oil, gas, minerals',
        'trade_route_disruption': True,
        'duration_estimate_months': 18,
        'alliance_implications': ['NATO', 'Regional Defense Pacts'],
        'geographic_scope': 'continental',
        'data_quality': 'medium'
    }

    # Run analysis
    result = orchestrator.analyze_event('geopolitical', geopolitical_event)

    print("\n" + "-"*80)
    print("KEY RESULTS")
    print("-"*80)
    print(f"Severity: {result['agent_analysis']['severity_assessment']}/5")
    print(f"Predicted Market Impact: {result['ensemble_predictions']['ensemble_prediction']}%")
    print(f"Escalation Risk: {geopolitical_event['escalation_potential']}/10")
    print(f"Nuclear Powers Involved: {'Yes' if geopolitical_event['nuclear_powers_involved'] else 'No'}")

    # Resource impacts
    resource_impacts = result['agent_analysis']['predictions'].get('resource_market_impact', {})
    affected = resource_impacts.get('resource_details', [])
    if affected:
        print("\nResource Market Impacts:")
        for res in affected:
            print(f"  - {res['resource']}: +{res['price_impact_estimate_pct']:.1f}% price impact")

    return result


def example_scenario_comparison():
    """
    Example: Comparing multiple scenarios
    """
    print("\n" + "="*80)
    print("EXAMPLE 6: SCENARIO COMPARISON")
    print("="*80)

    orchestrator = ExtremeEventsOrchestrator()

    scenarios = [
        {
            'name': 'Mild Pandemic',
            'event_type': 'pandemic',
            'event_data': {
                'r0': 2.0,
                'mortality_rate': 0.005,
                'affected_countries': ['Region1'],
                'vaccine_availability': True,
                'geographic_scope': 'regional',
                'containment_measures': ['social_distancing'],
                'data_quality': 'high'
            }
        },
        {
            'name': 'Major Terrorism',
            'event_type': 'terrorism',
            'event_data': {
                'attack_type': 'bombing',
                'casualties': 200,
                'economic_center': True,
                'symbolic_value': 5,
                'follow_up_threat': False,
                'geographic_scope': 'national',
                'target_type': 'financial',
                'data_quality': 'medium'
            }
        },
        {
            'name': 'Regional Conflict',
            'event_type': 'geopolitical',
            'event_data': {
                'event_subtype': 'war',
                'escalation_potential': 5.0,
                'nuclear_powers_involved': False,
                'economic_powerhouses_involved': False,
                'countries_involved': ['Country X', 'Country Y'],
                'geographic_scope': 'regional',
                'resource_access_impact': 'oil',
                'trade_route_disruption': False,
                'data_quality': 'medium'
            }
        }
    ]

    comparison = orchestrator.compare_scenarios(scenarios)

    print("\n" + "-"*80)
    print("SCENARIO COMPARISON RESULTS")
    print("-"*80)

    for i, scenario in enumerate(comparison['scenario_comparison'], 1):
        print(f"\n{i}. {scenario['scenario_name']}")
        print(f"   Event Type: {scenario['event_type']}")
        print(f"   Severity: {scenario['severity']}/5")
        print(f"   Predicted Impact: {scenario['predicted_impact']}%")
        print(f"   Risk Level: {scenario['risk_level'].upper()}")
        print(f"   Recovery Time: {scenario['recovery_days']} days")

    print(f"\nMost Severe: {comparison['most_severe']['scenario_name']}")
    print(f"Least Severe: {comparison['least_severe']['scenario_name']}")

    return comparison


def main():
    """
    Run all examples
    """
    print("\n" + "#"*80)
    print("EXTREME EVENTS PLATFORM - EXAMPLE USAGE")
    print("#"*80)

    # Run examples
    example_pandemic_analysis()
    print("\n" + "*"*80 + "\n")

    example_terrorism_analysis()
    print("\n" + "*"*80 + "\n")

    example_natural_disaster_analysis()
    print("\n" + "*"*80 + "\n")

    example_economic_crisis_analysis()
    print("\n" + "*"*80 + "\n")

    example_geopolitical_analysis()
    print("\n" + "*"*80 + "\n")

    example_scenario_comparison()

    print("\n" + "#"*80)
    print("ALL EXAMPLES COMPLETED")
    print("#"*80 + "\n")


if __name__ == "__main__":
    main()
