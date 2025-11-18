"""
Base Agent class for extreme event analysis
All specialized agents inherit from this base class
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from datetime import datetime
import numpy as np


class BaseExtremeEventAgent(ABC):
    """
    Abstract base class for all extreme event analysis agents
    """

    def __init__(self, event_type: str, config: Dict):
        """
        Initialize the base agent

        Args:
            event_type: Type of extreme event (pandemic, terrorism, etc.)
            config: Configuration dictionary
        """
        self.event_type = event_type
        self.config = config
        self.analysis_timestamp = None
        self.historical_data = []
        self.predictions = {}

    @abstractmethod
    def analyze_event(self, event_data: Dict) -> Dict:
        """
        Analyze a specific extreme event

        Args:
            event_data: Dictionary containing event details

        Returns:
            Dictionary with analysis results
        """
        pass

    @abstractmethod
    def predict_market_impact(self, event_data: Dict) -> Dict:
        """
        Predict market impact of the event

        Args:
            event_data: Dictionary containing event details

        Returns:
            Dictionary with market impact predictions
        """
        pass

    @abstractmethod
    def assess_severity(self, event_data: Dict) -> int:
        """
        Assess the severity of the event (1-5 scale)

        Args:
            event_data: Dictionary containing event details

        Returns:
            Severity score (1-5)
        """
        pass

    def calculate_shock_decay(self, days_since_event: int) -> float:
        """
        Calculate how market shock decays over time
        Uses exponential decay model based on research

        Args:
            days_since_event: Number of days since the event

        Returns:
            Decay factor (0-1)
        """
        # Initial shock (days 0-5): 100% impact
        if days_since_event <= 5:
            return 1.0

        # Acute phase (days 6-30): exponential decay
        elif days_since_event <= 30:
            return np.exp(-0.1 * (days_since_event - 5))

        # Recovery phase (months 1-6): slower decay
        elif days_since_event <= 180:
            return 0.4 * np.exp(-0.01 * (days_since_event - 30))

        # Long-term (6+ months): residual effects
        else:
            return 0.1 * np.exp(-0.005 * (days_since_event - 180))

    def calculate_market_immunity(self, similar_events_count: int) -> float:
        """
        Calculate market immunity based on previous similar events
        Markets develop immunity to repeated shocks

        Args:
            similar_events_count: Number of similar events in recent history

        Returns:
            Immunity factor (0-1, where 1 = full immunity)
        """
        if similar_events_count == 0:
            return 0.0

        # Diminishing returns: each subsequent event has less impact
        return 1 - (1 / (1 + 0.3 * similar_events_count))

    def assess_sector_impact(self, sectors: List[str], base_impact: float) -> Dict[str, float]:
        """
        Calculate impact on different market sectors

        Args:
            sectors: List of sector names
            base_impact: Base market impact (percentage)

        Returns:
            Dictionary mapping sectors to impact percentages
        """
        from ..config.config import SECTOR_SENSITIVITY

        sector_impacts = {}
        for sector in sectors:
            if sector in SECTOR_SENSITIVITY:
                sensitivity = SECTOR_SENSITIVITY[sector].get(self.event_type, 1.0)
                sector_impacts[sector] = base_impact * sensitivity
            else:
                sector_impacts[sector] = base_impact

        return sector_impacts

    def calculate_regional_multiplier(self, geographic_scope: str) -> float:
        """
        Calculate regional impact multiplier

        Args:
            geographic_scope: Scope of event (local, regional, national, etc.)

        Returns:
            Multiplier value
        """
        from ..config.config import REGIONAL_MULTIPLIERS
        return REGIONAL_MULTIPLIERS.get(geographic_scope.lower(), 1.0)

    def estimate_recovery_time(self, severity: int, geographic_scope: str) -> int:
        """
        Estimate market recovery time in days

        Args:
            severity: Event severity (1-5)
            geographic_scope: Geographic scope of event

        Returns:
            Estimated recovery time in days
        """
        from ..config.config import EVENT_TYPES

        base_recovery = EVENT_TYPES[self.event_type]['recovery_time_months'] * 30
        severity_factor = severity / 3.0  # Normalize to average severity
        regional_factor = self.calculate_regional_multiplier(geographic_scope)

        return int(base_recovery * severity_factor * (regional_factor / 5.0))

    def generate_confidence_score(self, data_quality: str, model_agreement: float) -> float:
        """
        Generate confidence score for predictions

        Args:
            data_quality: Quality of input data (high, medium, low)
            model_agreement: Agreement between different models (0-1)

        Returns:
            Confidence score (0-100)
        """
        quality_scores = {'high': 0.9, 'medium': 0.7, 'low': 0.5}
        base_confidence = quality_scores.get(data_quality.lower(), 0.5)

        return int((base_confidence * 0.6 + model_agreement * 0.4) * 100)

    def compile_analysis_report(self, event_data: Dict, predictions: Dict) -> Dict:
        """
        Compile comprehensive analysis report

        Args:
            event_data: Original event data
            predictions: Prediction results

        Returns:
            Complete analysis report
        """
        return {
            'event_type': self.event_type,
            'analysis_timestamp': datetime.now().isoformat(),
            'event_data': event_data,
            'severity_assessment': self.assess_severity(event_data),
            'predictions': predictions,
            'confidence_score': self.generate_confidence_score(
                event_data.get('data_quality', 'medium'),
                predictions.get('model_agreement', 0.7)
            ),
            'estimated_recovery_days': self.estimate_recovery_time(
                self.assess_severity(event_data),
                event_data.get('geographic_scope', 'regional')
            ),
            'agent_name': self.__class__.__name__
        }

    def get_historical_comparisons(self, event_data: Dict) -> List[Dict]:
        """
        Find and compare with similar historical events

        Args:
            event_data: Current event data

        Returns:
            List of similar historical events with outcomes
        """
        # This would interface with historical database
        # For now, return placeholder
        from ..config.config import EVENT_TYPES

        examples = EVENT_TYPES[self.event_type]['historical_examples']
        return [
            {
                'name': example,
                'similarity_score': 0.75,
                'market_impact': EVENT_TYPES[self.event_type]['avg_market_impact'],
                'recovery_time_days': EVENT_TYPES[self.event_type]['recovery_time_months'] * 30
            }
            for example in examples[:3]
        ]
