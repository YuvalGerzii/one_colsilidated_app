"""
Main Orchestrator for Extreme Events Platform
Coordinates agents, models, and predictions
"""

from typing import Dict, List, Optional
from datetime import datetime
import json

from .agents import (
    PandemicAgent,
    TerrorismAgent,
    NaturalDisasterAgent,
    EconomicCrisisAgent,
    GeopoliticalAgent
)
from .models import ExtremeValueTheoryModel, MLExtremeEventPredictor
from .config.config import EVENT_TYPES, IMPACT_SEVERITY_LEVELS


class ExtremeEventsOrchestrator:
    """
    Main orchestrator that coordinates all extreme event analysis and prediction
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the orchestrator

        Args:
            config: Optional configuration dictionary
        """
        from .config import config as default_config

        self.config = config or default_config
        self.agents = self._initialize_agents()
        self.evt_model = ExtremeValueTheoryModel(self.config)
        self.ml_predictor = MLExtremeEventPredictor(self.config)
        self.analysis_history = []

    def _initialize_agents(self) -> Dict:
        """
        Initialize all specialized agents

        Returns:
            Dictionary of agents by event type
        """
        return {
            'pandemic': PandemicAgent(self.config),
            'terrorism': TerrorismAgent(self.config),
            'natural_disaster': NaturalDisasterAgent(self.config),
            'economic_crisis': EconomicCrisisAgent(self.config),
            'geopolitical': GeopoliticalAgent(self.config)
        }

    def analyze_event(self, event_type: str, event_data: Dict) -> Dict:
        """
        Comprehensive analysis of an extreme event

        Args:
            event_type: Type of event (pandemic, terrorism, etc.)
            event_data: Event details

        Returns:
            Comprehensive analysis report
        """
        if event_type not in self.agents:
            raise ValueError(f"Unknown event type: {event_type}. Available: {list(self.agents.keys())}")

        print(f"\n{'='*80}")
        print(f"EXTREME EVENT ANALYSIS: {event_type.upper()}")
        print(f"{'='*80}\n")

        # Get appropriate agent
        agent = self.agents[event_type]

        # Run agent analysis
        print(f"Running {event_type} agent analysis...")
        agent_report = agent.analyze_event(event_data)

        # Run ML predictions
        print(f"Running machine learning predictions...")
        event_data['event_type'] = event_type
        ml_predictions = self.ml_predictor.predict_market_impact(
            event_data,
            historical_data=agent_report.get('historical_comparisons', [])
        )

        # Generate ensemble prediction
        ensemble = self.ml_predictor.ensemble_prediction(event_data)

        # Calculate confidence metrics
        confidence_metrics = self.ml_predictor.calculate_confidence_metrics(event_data)

        # Time series prediction
        time_series = self.ml_predictor.predict_time_series(event_data, days_ahead=180)

        # Compile comprehensive report
        comprehensive_report = {
            'analysis_id': f"{event_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'event_data': event_data,
            'agent_analysis': agent_report,
            'ml_predictions': ml_predictions,
            'ensemble_predictions': ensemble,
            'confidence_metrics': confidence_metrics,
            'time_series_forecast': time_series,
            'risk_summary': self._generate_risk_summary(agent_report, ensemble),
            'recommendations': self._generate_recommendations(agent_report, confidence_metrics)
        }

        # Store in history
        self.analysis_history.append(comprehensive_report)

        print(f"\n{'='*80}")
        print(f"ANALYSIS COMPLETE")
        print(f"{'='*80}\n")

        return comprehensive_report

    def _generate_risk_summary(self, agent_report: Dict, ensemble: Dict) -> Dict:
        """
        Generate executive risk summary

        Args:
            agent_report: Agent analysis report
            ensemble: Ensemble predictions

        Returns:
            Risk summary
        """
        severity = agent_report.get('severity_assessment', 3)
        predicted_impact = ensemble['ensemble_prediction']

        risk_level = 'low'
        if severity >= 4 or predicted_impact <= -20:
            risk_level = 'critical'
        elif severity >= 3 or predicted_impact <= -10:
            risk_level = 'high'
        elif severity >= 2 or predicted_impact <= -5:
            risk_level = 'moderate'

        return {
            'overall_risk_level': risk_level,
            'severity_score': severity,
            'predicted_market_impact_pct': predicted_impact,
            'estimated_recovery_days': agent_report.get('estimated_recovery_days', 90),
            'key_risks': self._identify_key_risks(agent_report),
            'immediate_actions_required': risk_level in ['critical', 'high']
        }

    def _identify_key_risks(self, agent_report: Dict) -> List[str]:
        """
        Identify key risks from analysis

        Args:
            agent_report: Agent analysis report

        Returns:
            List of key risks
        """
        risks = []

        severity = agent_report.get('severity_assessment', 3)
        if severity >= 4:
            risks.append("Severe market disruption expected")

        predictions = agent_report.get('predictions', {}).get('market_predictions', {})
        if predictions.get('overall_market_impact', 0) <= -15:
            risks.append("Major portfolio losses likely")

        if agent_report.get('predictions', {}).get('volatility_increase', 0) > 30:
            risks.append("Extreme volatility spike expected")

        # Event-specific risks
        event_type = agent_report.get('event_type', '')

        if event_type == 'pandemic':
            if agent_report.get('predictions', {}).get('healthcare_system_stress', '') == 'critical':
                risks.append("Healthcare system collapse risk")

        elif event_type == 'economic_crisis':
            if agent_report.get('predictions', {}).get('systemic_risk_assessment', {}).get('risk_level', '') == 'critical':
                risks.append("Systemic financial collapse risk")

        elif event_type == 'geopolitical':
            if agent_report.get('predictions', {}).get('escalation_risk_assessment', {}).get('risk_level', '') == 'critical':
                risks.append("Military escalation risk")

        if not risks:
            risks.append("Manageable risk level")

        return risks

    def _generate_recommendations(self, agent_report: Dict, confidence_metrics: Dict) -> List[Dict]:
        """
        Generate actionable recommendations

        Args:
            agent_report: Agent analysis report
            confidence_metrics: Confidence metrics

        Returns:
            List of recommendations
        """
        recommendations = []

        severity = agent_report.get('severity_assessment', 3)
        confidence = confidence_metrics.get('overall_confidence', 50)

        # Portfolio management recommendations
        if severity >= 4:
            recommendations.append({
                'category': 'Portfolio Management',
                'priority': 'critical',
                'action': 'Reduce equity exposure and increase cash positions',
                'rationale': 'Severe market disruption expected'
            })
        elif severity >= 3:
            recommendations.append({
                'category': 'Portfolio Management',
                'priority': 'high',
                'action': 'Increase defensive positioning and hedge key exposures',
                'rationale': 'Significant market volatility expected'
            })

        # Risk management recommendations
        recommendations.append({
            'category': 'Risk Management',
            'priority': 'high',
            'action': 'Update VaR models and stress test portfolios',
            'rationale': 'Tail risk event requiring enhanced risk monitoring'
        })

        # Sector-specific recommendations
        sectoral_impact = agent_report.get('predictions', {}).get('sectoral_impact', {})
        if sectoral_impact:
            worst_sector = min(sectoral_impact.items(), key=lambda x: x[1])
            best_sector = max(sectoral_impact.items(), key=lambda x: x[1])

            recommendations.append({
                'category': 'Sector Allocation',
                'priority': 'medium',
                'action': f'Reduce {worst_sector[0]} exposure, consider {best_sector[0]} overweight',
                'rationale': f'{worst_sector[0]} highly vulnerable to this event type'
            })

        # Monitoring recommendations
        if confidence < 60:
            recommendations.append({
                'category': 'Monitoring',
                'priority': 'high',
                'action': 'Increase monitoring frequency due to prediction uncertainty',
                'rationale': f'Confidence level: {confidence}% - requires closer observation'
            })

        return recommendations

    def compare_scenarios(self, scenarios: List[Dict]) -> Dict:
        """
        Compare multiple scenarios

        Args:
            scenarios: List of scenario dictionaries with event_type and event_data

        Returns:
            Comparative analysis
        """
        results = []

        for scenario in scenarios:
            event_type = scenario['event_type']
            event_data = scenario['event_data']

            analysis = self.analyze_event(event_type, event_data)
            results.append({
                'scenario_name': scenario.get('name', f'{event_type}_scenario'),
                'event_type': event_type,
                'severity': analysis['agent_analysis']['severity_assessment'],
                'predicted_impact': analysis['ensemble_predictions']['ensemble_prediction'],
                'risk_level': analysis['risk_summary']['overall_risk_level'],
                'recovery_days': analysis['risk_summary']['estimated_recovery_days']
            })

        # Sort by severity
        results.sort(key=lambda x: x['severity'], reverse=True)

        return {
            'scenario_comparison': results,
            'most_severe': results[0] if results else None,
            'least_severe': results[-1] if results else None,
            'analysis_date': datetime.now().isoformat()
        }

    def export_report(self, analysis_result: Dict, format: str = 'json', filepath: str = None) -> str:
        """
        Export analysis report

        Args:
            analysis_result: Analysis result dictionary
            format: Export format ('json', 'text')
            filepath: Optional filepath to save

        Returns:
            Formatted report string
        """
        if format == 'json':
            report = json.dumps(analysis_result, indent=2)
        elif format == 'text':
            report = self._format_text_report(analysis_result)
        else:
            raise ValueError(f"Unknown format: {format}")

        if filepath:
            with open(filepath, 'w') as f:
                f.write(report)
            print(f"Report saved to: {filepath}")

        return report

    def _format_text_report(self, analysis: Dict) -> str:
        """
        Format analysis as readable text report

        Args:
            analysis: Analysis result dictionary

        Returns:
            Formatted text report
        """
        report = []
        report.append("="*80)
        report.append("EXTREME EVENT ANALYSIS REPORT")
        report.append("="*80)
        report.append(f"\nAnalysis ID: {analysis['analysis_id']}")
        report.append(f"Timestamp: {analysis['timestamp']}")
        report.append(f"Event Type: {analysis['event_type'].upper()}\n")

        # Risk Summary
        risk = analysis['risk_summary']
        report.append("\n" + "-"*80)
        report.append("RISK SUMMARY")
        report.append("-"*80)
        report.append(f"Overall Risk Level: {risk['overall_risk_level'].upper()}")
        report.append(f"Severity Score: {risk['severity_score']}/5")
        report.append(f"Predicted Market Impact: {risk['predicted_market_impact_pct']}%")
        report.append(f"Estimated Recovery Time: {risk['estimated_recovery_days']} days")
        report.append(f"\nKey Risks:")
        for r in risk['key_risks']:
            report.append(f"  - {r}")

        # Predictions
        report.append("\n" + "-"*80)
        report.append("PREDICTIONS")
        report.append("-"*80)
        ensemble = analysis['ensemble_predictions']
        report.append(f"Ensemble Prediction: {ensemble['ensemble_prediction']}%")
        report.append(f"Model Agreement: {ensemble['model_agreement']*100:.1f}%")

        # Confidence
        confidence = analysis['confidence_metrics']
        report.append(f"\nPrediction Confidence: {confidence['overall_confidence']}% ({confidence['confidence_level']})")

        # Recommendations
        report.append("\n" + "-"*80)
        report.append("RECOMMENDATIONS")
        report.append("-"*80)
        for rec in analysis['recommendations']:
            report.append(f"\n[{rec['priority'].upper()}] {rec['category']}")
            report.append(f"Action: {rec['action']}")
            report.append(f"Rationale: {rec['rationale']}")

        report.append("\n" + "="*80)

        return "\n".join(report)

    def get_analysis_history(self) -> List[Dict]:
        """
        Get history of all analyses

        Returns:
            List of analysis results
        """
        return self.analysis_history
