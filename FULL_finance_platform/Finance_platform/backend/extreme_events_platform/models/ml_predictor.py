"""
Machine Learning Predictor for Extreme Events
Implements neural networks and other ML models for event impact prediction
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta


class MLExtremeEventPredictor:
    """
    Machine Learning-based predictor for extreme event impacts
    Uses ensemble of models for robust predictions
    """

    def __init__(self, config: Dict):
        """
        Initialize ML predictor

        Args:
            config: Configuration dictionary with ML parameters
        """
        self.config = config
        self.models = {}
        self.feature_importance = {}
        self.training_history = []

    def extract_features(self, event_data: Dict, historical_data: Optional[List] = None) -> np.ndarray:
        """
        Extract features from event data for ML prediction

        Args:
            event_data: Current event data
            historical_data: Historical similar events

        Returns:
            Feature vector
        """
        features = []

        # Event characteristics
        features.append(event_data.get('severity', 3))
        features.append(event_data.get('duration_estimate', 30) / 365)  # Normalize to years

        # Geographic scope encoding
        scope_encoding = {'local': 1, 'regional': 2, 'national': 3, 'continental': 4, 'global': 5}
        features.append(scope_encoding.get(event_data.get('geographic_scope', 'regional'), 2))

        # Economic indicators
        features.append(event_data.get('gdp_impact', 0))
        features.append(event_data.get('market_volatility_current', 15))

        # Market conditions
        features.append(event_data.get('market_sentiment', 50) / 100)  # Normalize to 0-1
        features.append(event_data.get('liquidity_index', 1.0))

        # Historical similarity
        if historical_data:
            avg_historical_impact = np.mean([h.get('market_impact', 0) for h in historical_data])
            features.append(avg_historical_impact)
            features.append(len(historical_data))  # Number of similar events
        else:
            features.append(0)
            features.append(0)

        # Time-based features
        current_date = datetime.now()
        features.append(current_date.month / 12)  # Seasonality
        features.append(current_date.weekday() / 7)  # Day of week effect

        # Policy response
        response_encoding = {'none': 0, 'minimal': 1, 'moderate': 2, 'aggressive': 3}
        features.append(response_encoding.get(event_data.get('policy_response', 'moderate'), 2))

        return np.array(features)

    def predict_market_impact(self, event_data: Dict, historical_data: Optional[List] = None) -> Dict:
        """
        Predict market impact using ML models

        Args:
            event_data: Event details
            historical_data: Similar historical events

        Returns:
            Predictions with confidence intervals
        """
        features = self.extract_features(event_data, historical_data)

        # Since we don't have trained models, use rule-based predictions
        # In production, this would use actual trained models
        base_prediction = self._rule_based_prediction(event_data, features)

        # Add uncertainty based on data quality
        data_quality = event_data.get('data_quality', 'medium')
        uncertainty_factors = {'high': 0.1, 'medium': 0.2, 'low': 0.3}
        uncertainty = uncertainty_factors.get(data_quality, 0.2)

        lower_bound = base_prediction * (1 - uncertainty)
        upper_bound = base_prediction * (1 + uncertainty)

        return {
            'predicted_impact': round(base_prediction, 2),
            'confidence_interval_95': {
                'lower': round(lower_bound, 2),
                'upper': round(upper_bound, 2)
            },
            'uncertainty_level': uncertainty,
            'feature_importance': self._calculate_feature_importance(features),
            'model_confidence': round((1 - uncertainty) * 100, 1)
        }

    def _rule_based_prediction(self, event_data: Dict, features: np.ndarray) -> float:
        """
        Rule-based prediction (placeholder for actual ML model)

        Args:
            event_data: Event details
            features: Extracted features

        Returns:
            Predicted market impact percentage
        """
        severity = features[0]
        duration_years = features[1]
        scope = features[2]

        # Base impact from severity
        base_impact = -5.0 * severity

        # Duration adjustment
        duration_factor = 1.0 + (duration_years * 0.5)

        # Geographic scope multiplier
        scope_multiplier = scope / 3.0

        # Policy response mitigation
        policy_response = features[10]
        policy_mitigation = 1.0 - (policy_response * 0.1)

        total_impact = base_impact * duration_factor * scope_multiplier * policy_mitigation

        return total_impact

    def _calculate_feature_importance(self, features: np.ndarray) -> Dict:
        """
        Calculate feature importance scores

        Args:
            features: Feature vector

        Returns:
            Dictionary of feature importances
        """
        feature_names = [
            'severity', 'duration', 'geographic_scope', 'gdp_impact',
            'volatility', 'market_sentiment', 'liquidity', 'historical_impact',
            'similar_events_count', 'month', 'weekday', 'policy_response'
        ]

        # Simplified importance based on feature magnitudes
        importances = np.abs(features) / (np.sum(np.abs(features)) + 1e-6)

        return {
            name: round(float(imp * 100), 2)
            for name, imp in zip(feature_names, importances)
        }

    def predict_time_series(self, event_data: Dict, days_ahead: int = 90) -> Dict:
        """
        Predict market impact over time

        Args:
            event_data: Event details
            days_ahead: Number of days to predict

        Returns:
            Time series predictions
        """
        initial_impact = self.predict_market_impact(event_data)['predicted_impact']

        # Model decay over time
        time_points = np.arange(0, days_ahead)

        # Exponential decay with recovery
        decay_rate = 0.02
        recovery_start = days_ahead * 0.3

        predictions = []
        for t in time_points:
            if t < recovery_start:
                # Initial decay phase
                impact = initial_impact * np.exp(-decay_rate * t)
            else:
                # Recovery phase
                recovery_factor = (t - recovery_start) / (days_ahead - recovery_start)
                impact = initial_impact * np.exp(-decay_rate * recovery_start) * (1 - recovery_factor * 0.7)

            predictions.append({
                'day': int(t),
                'predicted_impact': round(float(impact), 2)
            })

        return {
            'time_series_predictions': predictions,
            'full_recovery_day': int(days_ahead),
            'peak_impact_day': 0,
            'recovery_start_day': int(recovery_start)
        }

    def predict_sector_specific_impact(self, event_data: Dict, sectors: List[str]) -> Dict:
        """
        Predict impact on specific market sectors

        Args:
            event_data: Event details
            sectors: List of sector names

        Returns:
            Sector-specific predictions
        """
        from ..config.config import SECTOR_SENSITIVITY

        event_type = event_data.get('event_type', 'pandemic')
        base_impact = self.predict_market_impact(event_data)['predicted_impact']

        sector_predictions = {}
        for sector in sectors:
            if sector in SECTOR_SENSITIVITY:
                sensitivity = SECTOR_SENSITIVITY[sector].get(event_type, 1.0)
                sector_impact = base_impact * sensitivity

                # Add sector-specific factors
                sector_volatility = sensitivity * 10  # Approximate volatility increase

                sector_predictions[sector] = {
                    'predicted_impact_pct': round(sector_impact, 2),
                    'sensitivity_factor': sensitivity,
                    'expected_volatility_increase': round(sector_volatility, 2),
                    'recovery_time_estimate_days': int(90 * sensitivity)
                }

        return sector_predictions

    def ensemble_prediction(self, event_data: Dict, methods: List[str] = None) -> Dict:
        """
        Generate ensemble prediction from multiple methods

        Args:
            event_data: Event details
            methods: List of methods to ensemble

        Returns:
            Ensemble prediction with individual model outputs
        """
        if methods is None:
            methods = ['ml', 'historical_avg', 'regression']

        predictions = []

        # ML prediction
        if 'ml' in methods:
            ml_pred = self.predict_market_impact(event_data)
            predictions.append(ml_pred['predicted_impact'])

        # Historical average (if available)
        if 'historical_avg' in methods:
            historical_data = event_data.get('historical_comparisons', [])
            if historical_data:
                hist_avg = np.mean([h.get('market_impact', 0) for h in historical_data])
            else:
                hist_avg = -10.0  # Default estimate
            predictions.append(hist_avg)

        # Simple regression based on severity
        if 'regression' in methods:
            severity = event_data.get('severity', 3)
            regression_pred = -8.0 * (severity / 3.0)
            predictions.append(regression_pred)

        # Ensemble: weighted average
        weights = [0.5, 0.3, 0.2][:len(predictions)]
        weights = np.array(weights) / np.sum(weights)  # Normalize

        ensemble_pred = np.average(predictions, weights=weights)
        std_dev = np.std(predictions)

        return {
            'ensemble_prediction': round(float(ensemble_pred), 2),
            'individual_predictions': {
                method: round(float(pred), 2)
                for method, pred in zip(methods, predictions)
            },
            'prediction_std_dev': round(float(std_dev), 2),
            'model_agreement': round(float(1 - (std_dev / (abs(ensemble_pred) + 1e-6))), 2)
        }

    def calculate_confidence_metrics(self, event_data: Dict) -> Dict:
        """
        Calculate various confidence metrics for predictions

        Args:
            event_data: Event details

        Returns:
            Confidence metrics
        """
        # Data quality assessment
        data_quality = event_data.get('data_quality', 'medium')
        quality_scores = {'high': 0.9, 'medium': 0.7, 'low': 0.5}
        data_score = quality_scores.get(data_quality, 0.7)

        # Historical similarity
        historical = event_data.get('historical_comparisons', [])
        similarity_score = min(1.0, len(historical) * 0.2) if historical else 0.3

        # Model agreement
        ensemble = self.ensemble_prediction(event_data)
        agreement_score = ensemble['model_agreement']

        # Overall confidence
        overall_confidence = (data_score * 0.4 + similarity_score * 0.3 + agreement_score * 0.3)

        return {
            'overall_confidence': round(overall_confidence * 100, 1),
            'data_quality_score': round(data_score * 100, 1),
            'historical_similarity_score': round(similarity_score * 100, 1),
            'model_agreement_score': round(agreement_score * 100, 1),
            'confidence_level': 'high' if overall_confidence > 0.7 else 'medium' if overall_confidence > 0.5 else 'low'
        }
