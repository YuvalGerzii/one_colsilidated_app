# Extreme Events Platform - Usage Guide

## Overview

This platform provides comprehensive analysis and prediction of market reactions to extreme events including:
- **Pandemics** (COVID-19, SARS, etc.)
- **Terrorism** (9/11, bombings, etc.)
- **Natural Disasters** (hurricanes, earthquakes, floods)
- **Economic Crises** (2008 financial crisis, etc.)
- **Geopolitical Events** (wars, sanctions, etc.)

## Quick Start

### Basic Usage

```python
from extreme_events_platform import ExtremeEventsOrchestrator

# Initialize the platform
orchestrator = ExtremeEventsOrchestrator()

# Define an event
event_data = {
    'disease_name': 'Novel Virus',
    'r0': 3.0,
    'mortality_rate': 0.01,
    'affected_countries': ['USA', 'Europe'],
    'vaccine_availability': False,
    'geographic_scope': 'global'
}

# Analyze the event
result = orchestrator.analyze_event('pandemic', event_data)

# Access key results
print(f"Predicted Impact: {result['ensemble_predictions']['ensemble_prediction']}%")
print(f"Risk Level: {result['risk_summary']['overall_risk_level']}")
print(f"Recovery Time: {result['risk_summary']['estimated_recovery_days']} days")
```

## Event Types and Required Parameters

### 1. Pandemic Events

```python
pandemic_event = {
    'disease_name': str,              # Name of disease
    'r0': float,                      # Basic reproduction number (1-10)
    'mortality_rate': float,          # Mortality rate (0-1)
    'affected_countries': List[str],  # List of affected countries
    'containment_measures': List[str], # ['lockdown', 'travel_ban', etc.]
    'healthcare_capacity': str,       # 'low', 'medium', 'high'
    'vaccine_availability': bool,     # Vaccine available?
    'geographic_scope': str,          # 'local', 'regional', 'national', 'global'
    'data_quality': str              # 'low', 'medium', 'high'
}

result = orchestrator.analyze_event('pandemic', pandemic_event)
```

### 2. Terrorism Events

```python
terrorism_event = {
    'attack_type': str,         # 'bombing', 'shooting', 'cyber_attack', etc.
    'casualties': int,          # Number of casualties
    'target_type': str,         # 'civilian', 'financial', 'infrastructure', etc.
    'location': str,            # Location of attack
    'economic_center': bool,    # Is it a major economic center?
    'symbolic_value': int,      # Symbolic importance (1-5)
    'claimed_by': str,          # Organization claiming responsibility
    'follow_up_threat': bool,   # Is there ongoing threat?
    'geographic_scope': str,    # 'local', 'regional', 'national'
    'data_quality': str        # 'low', 'medium', 'high'
}

result = orchestrator.analyze_event('terrorism', terrorism_event)
```

### 3. Natural Disaster Events

```python
disaster_event = {
    'disaster_type': str,                    # 'hurricane', 'earthquake', 'flood', etc.
    'magnitude': float,                      # Magnitude (Richter, Category, etc.)
    'affected_area_sq_km': float,           # Affected area
    'population_affected': int,             # Number of people affected
    'infrastructure_damage': str,           # 'minimal', 'moderate', 'severe', 'catastrophic'
    'economic_losses_usd': float,          # Economic losses in USD
    'insurance_coverage': float,            # Coverage ratio (0-1)
    'location': str,                        # Location
    'industrial_facilities_affected': List[str],  # ['port', 'refinery', etc.]
    'geographic_scope': str,               # 'local', 'regional', 'national'
    'data_quality': str                    # 'low', 'medium', 'high'
}

result = orchestrator.analyze_event('natural_disaster', disaster_event)
```

### 4. Economic Crisis Events

```python
crisis_event = {
    'crisis_type': str,                  # 'banking_crisis', 'sovereign_debt', etc.
    'affected_institutions': List[str],  # List of affected institutions
    'systemic_risk_score': float,       # Systemic risk (0-10)
    'credit_market_stress': str,        # 'low', 'medium', 'high', 'severe'
    'contagion_risk': float,            # Contagion probability (0-1)
    'central_bank_response': str,       # 'none', 'moderate', 'aggressive'
    'fiscal_stimulus': float,           # Stimulus amount in USD
    'unemployment_increase': float,     # Percentage point increase
    'gdp_contraction': float,          # GDP contraction percentage
    'geographic_scope': str,           # 'regional', 'national', 'continental', 'global'
    'data_quality': str               # 'low', 'medium', 'high'
}

result = orchestrator.analyze_event('economic_crisis', crisis_event)
```

### 5. Geopolitical Events

```python
geopolitical_event = {
    'event_subtype': str,                    # 'war', 'sanctions', 'trade_war', etc.
    'countries_involved': List[str],        # Countries involved
    'economic_powerhouses_involved': bool,  # Major economies involved?
    'nuclear_powers_involved': bool,        # Nuclear powers involved?
    'escalation_potential': float,          # Escalation risk (0-10)
    'resource_access_impact': str,          # 'oil, gas, minerals, food'
    'trade_route_disruption': bool,        # Trade routes affected?
    'duration_estimate_months': int,       # Expected duration
    'alliance_implications': List[str],    # Affected alliances
    'geographic_scope': str,              # 'regional', 'continental', 'global'
    'data_quality': str                   # 'low', 'medium', 'high'
}

result = orchestrator.analyze_event('geopolitical', geopolitical_event)
```

## Understanding Results

### Analysis Result Structure

```python
{
    'analysis_id': str,                    # Unique analysis ID
    'timestamp': str,                      # ISO format timestamp
    'event_type': str,                     # Type of event analyzed
    'event_data': Dict,                    # Original event data

    'agent_analysis': {                    # Specialized agent analysis
        'severity_assessment': int,        # Severity score (1-5)
        'predictions': Dict,               # Agent-specific predictions
        'sectoral_impact': Dict,          # Impact by sector
        'historical_comparisons': List    # Similar historical events
    },

    'ml_predictions': {                    # ML model predictions
        'predicted_impact': float,         # Predicted impact %
        'confidence_interval_95': Dict,   # Confidence bounds
        'feature_importance': Dict        # Feature contributions
    },

    'ensemble_predictions': {              # Ensemble of multiple models
        'ensemble_prediction': float,      # Combined prediction
        'individual_predictions': Dict,   # Individual model results
        'model_agreement': float          # Agreement score (0-1)
    },

    'confidence_metrics': {                # Prediction confidence
        'overall_confidence': float,       # Overall confidence %
        'confidence_level': str           # 'low', 'medium', 'high'
    },

    'time_series_forecast': {              # Time-based predictions
        'time_series_predictions': List,  # Day-by-day predictions
        'full_recovery_day': int,         # Recovery timeline
        'peak_impact_day': int           # Day of maximum impact
    },

    'risk_summary': {                      # Executive summary
        'overall_risk_level': str,        # 'low', 'moderate', 'high', 'critical'
        'severity_score': int,            # Severity (1-5)
        'predicted_market_impact_pct': float,  # Market impact %
        'estimated_recovery_days': int,   # Recovery time
        'key_risks': List[str],          # List of key risks
        'immediate_actions_required': bool
    },

    'recommendations': List[Dict]          # Actionable recommendations
}
```

### Key Metrics Explained

**VaR (Value at Risk)**: Maximum expected loss at given confidence level
- VaR 95%: Loss exceeded only 5% of the time
- VaR 99%: Loss exceeded only 1% of the time

**CVaR (Conditional VaR)**: Expected loss when VaR threshold is exceeded
- Always worse than VaR
- Represents "tail risk"

**Severity Score**: 1-5 scale
- 1: Minor impact
- 2: Moderate impact
- 3: Significant impact
- 4: Severe impact
- 5: Catastrophic impact

**Risk Level**:
- **Low**: Limited market impact, quick recovery
- **Moderate**: Noticeable impact, manageable recovery
- **High**: Major market disruption, extended recovery
- **Critical**: Severe market disruption, prolonged recovery

## Advanced Usage

### Scenario Comparison

Compare multiple scenarios to identify worst-case:

```python
scenarios = [
    {
        'name': 'Scenario 1',
        'event_type': 'pandemic',
        'event_data': {...}
    },
    {
        'name': 'Scenario 2',
        'event_type': 'economic_crisis',
        'event_data': {...}
    }
]

comparison = orchestrator.compare_scenarios(scenarios)
print(f"Most severe: {comparison['most_severe']['scenario_name']}")
```

### Export Reports

Export analysis to file:

```python
# JSON export
orchestrator.export_report(result, format='json', filepath='analysis.json')

# Text export
orchestrator.export_report(result, format='text', filepath='analysis.txt')
```

### Time Series Forecasting

Access day-by-day predictions:

```python
time_series = result['time_series_forecast']
for day in time_series['time_series_predictions']:
    print(f"Day {day['day']}: {day['predicted_impact']}%")
```

## Best Practices

1. **Data Quality**: Always specify `data_quality`. Higher quality = better predictions

2. **Historical Context**: Include similar past events for better accuracy

3. **Multiple Models**: Use ensemble predictions for robustness

4. **Confidence Levels**: Check confidence metrics before acting on predictions

5. **Scenario Analysis**: Run multiple scenarios to understand range of outcomes

6. **Regular Updates**: Re-analyze as new information becomes available

## Example Scenarios

See `examples/example_usage.py` for complete working examples of:
- Pandemic analysis (COVID-like scenario)
- Terrorism analysis (Major attack scenario)
- Natural disaster analysis (Hurricane scenario)
- Economic crisis analysis (Banking crisis scenario)
- Geopolitical analysis (Conflict scenario)
- Multi-scenario comparison

Run examples:
```bash
cd extreme_events_platform
python examples/example_usage.py
```

## Research References

This platform is based on:
- **Extreme Value Theory**: For tail risk modeling
- **Black Swan Theory** (Taleb): Framework for rare high-impact events
- **Machine Learning**: Neural networks, SVMs for pattern recognition
- **Economic Impact Models**: Multi-factor impact assessment
- **Historical Crisis Analysis**: 2008 crisis, COVID-19, 9/11, etc.

## Support

For issues or questions:
1. Review this guide
2. Check example scripts
3. Refer to README.md for methodology
4. Review configuration in `config/config.py`
