"""
Human Behavior Predictor
Predicts how people will react to extreme events based on behavioral economics
"""

from typing import Dict, List, Tuple
import numpy as np
from dataclasses import dataclass


@dataclass
class BehavioralPrediction:
    """Prediction of human behavioral responses"""
    dominant_emotion: str
    emotion_intensity: float  # 0-1
    behavioral_patterns: List[str]
    risk_tolerance_change: float  # -1 to 1
    time_horizon_shift: str
    social_behaviors: List[str]
    economic_behaviors: List[str]
    confidence_score: float


class HumanBehaviorPredictor:
    """
    Predicts human psychological and behavioral responses to extreme events
    Based on behavioral economics and crisis psychology research
    """

    def __init__(self):
        self.emotion_thresholds = {
            'fear': 0.6,
            'anger': 0.5,
            'panic': 0.8,
            'anxiety': 0.5,
            'optimism': 0.4
        }

    def predict_behavior(self, event_data: Dict) -> BehavioralPrediction:
        """
        Predict comprehensive behavioral response

        Args:
            event_data: Event characteristics

        Returns:
            BehavioralPrediction with all behavioral aspects
        """
        # Determine emotional response
        dominant_emotion, intensity = self._analyze_emotional_response(event_data)

        # Predict behavioral patterns
        patterns = self._predict_behavioral_patterns(dominant_emotion, intensity, event_data)

        # Risk tolerance changes
        risk_change = self._predict_risk_tolerance_change(dominant_emotion, intensity)

        # Time horizon shift
        time_horizon = self._predict_time_horizon(dominant_emotion, intensity)

        # Social behaviors
        social = self._predict_social_behaviors(dominant_emotion, event_data)

        # Economic behaviors
        economic = self._predict_economic_behaviors(dominant_emotion, event_data)

        return BehavioralPrediction(
            dominant_emotion=dominant_emotion,
            emotion_intensity=intensity,
            behavioral_patterns=patterns,
            risk_tolerance_change=risk_change,
            time_horizon_shift=time_horizon,
            social_behaviors=social,
            economic_behaviors=economic,
            confidence_score=0.75
        )

    def _analyze_emotional_response(self, event_data: Dict) -> Tuple[str, float]:
        """
        Determine dominant emotional response and its intensity

        Returns:
            (emotion_name, intensity)
        """
        # Calculate emotion scores
        fear_score = self._calculate_fear(event_data)
        anger_score = self._calculate_anger(event_data)
        panic_score = self._calculate_panic(event_data)
        anxiety_score = self._calculate_anxiety(event_data)

        # Find dominant emotion
        emotions = {
            'fear': fear_score,
            'anger': anger_score,
            'panic': panic_score,
            'anxiety': anxiety_score
        }

        dominant = max(emotions.items(), key=lambda x: x[1])
        return dominant[0], dominant[1]

    def _calculate_fear(self, event_data: Dict) -> float:
        """Calculate fear response intensity"""
        fear = 0.5  # Base level

        # High casualties
        casualties = event_data.get('casualties', 0) or event_data.get('casualty_count', 0)
        if casualties > 1000:
            fear += 0.3
        elif casualties > 100:
            fear += 0.2

        # Unknown/novel threat
        if event_data.get('novel_threat', False) or event_data.get('vaccine_availability', True) == False:
            fear += 0.2

        # Systemic risk
        systemic = event_data.get('systemic_risk_score', 0) or event_data.get('systemic_risk', 0)
        if systemic > 7 or systemic > 0.7:
            fear += 0.25

        # Personal threat
        if event_data.get('geographic_scope') == 'global':
            fear += 0.15

        # Existential risk
        if event_data.get('nuclear_powers_involved', False) or event_data.get('event_type') == 'space_event':
            fear += 0.3

        return min(1.0, fear)

    def _calculate_anger(self, event_data: Dict) -> float:
        """Calculate anger response intensity"""
        anger = 0.0

        # Human-caused events trigger anger
        event_type = event_data.get('event_type', '')
        if event_type in ['terrorism', 'cyber_attack', 'economic_crisis', 'governance_collapse']:
            anger += 0.3

        # Preventable events
        if event_data.get('preventable', False):
            anger += 0.25

        # Inequality/injustice
        if event_data.get('inequality_impact', False):
            anger += 0.3

        # Corruption or negligence
        if 'corruption' in event_data.get('causes', []) or 'negligence' in event_data.get('causes', []):
            anger += 0.35

        # Failed policy response
        if event_data.get('policy_response', '') == 'none' or event_data.get('central_bank_response') == 'none':
            anger += 0.2

        return min(1.0, anger)

    def _calculate_panic(self, event_data: Dict) -> float:
        """Calculate panic response intensity"""
        panic = 0.0

        # Sudden onset
        if event_data.get('is_sudden_onset', True):
            panic += 0.2

        # Supply disruption
        if 'supply' in event_data.get('event_type', '').lower():
            panic += 0.3

        # Essential resources threatened
        if event_data.get('resource_access_impact') or event_data.get('event_type') == 'resource_crisis':
            panic += 0.35

        # Market crash
        market_impact = event_data.get('market_impact', 0)
        if market_impact < -20:
            panic += 0.3
        elif market_impact < -10:
            panic += 0.2

        # High uncertainty
        uncertainty = event_data.get('uncertainty_level', 0.5) or event_data.get('uncertainty_factor', 0.5)
        panic += uncertainty * 0.4

        return min(1.0, panic)

    def _calculate_anxiety(self, event_data: Dict) -> float:
        """Calculate anxiety response intensity"""
        anxiety = 0.3  # Base level

        # Duration matters for anxiety
        duration = event_data.get('duration_estimate_months', 1) or event_data.get('duration_estimate_days', 30) / 30
        if duration > 12:
            anxiety += 0.3
        elif duration > 6:
            anxiety += 0.2

        # Uncertainty
        uncertainty = event_data.get('uncertainty_level', 0.5)
        anxiety += uncertainty * 0.3

        # Ongoing threat
        if event_data.get('is_ongoing', True) or event_data.get('follow_up_threat', False):
            anxiety += 0.2

        return min(1.0, anxiety)

    def _predict_behavioral_patterns(self, emotion: str, intensity: float, event_data: Dict) -> List[str]:
        """Predict specific behavioral patterns"""
        patterns = []

        if emotion == 'fear' and intensity > 0.6:
            patterns.extend([
                'flight_to_safety',
                'defensive_positioning',
                'information_seeking',
                'social_withdrawal',
                'precautionary_saving'
            ])

        if emotion == 'anger' and intensity > 0.5:
            patterns.extend([
                'risk_taking',
                'contrarian_behavior',
                'protest_actions',
                'boycotts',
                'social_activism'
            ])

        if emotion == 'panic' and intensity > 0.7:
            patterns.extend([
                'panic_buying',
                'panic_selling',
                'hoarding',
                'herd_behavior',
                'irrational_decision_making'
            ])

        if emotion == 'anxiety' and intensity > 0.6:
            patterns.extend([
                'hypervigilance',
                'excessive_checking',
                'rumination',
                'indecision',
                'paralysis_by_analysis'
            ])

        # Add herd behavior if uncertainty is high
        if event_data.get('uncertainty_level', 0.5) > 0.7:
            patterns.append('herd_mentality')

        return patterns

    def _predict_risk_tolerance_change(self, emotion: str, intensity: float) -> float:
        """
        Predict change in risk tolerance

        Returns:
            Value from -1 (very risk averse) to 1 (very risk seeking)
        """
        # Fear decreases risk tolerance
        if emotion == 'fear':
            return -0.7 * intensity

        # Anger can increase risk taking
        elif emotion == 'anger':
            return 0.3 * intensity

        # Panic dramatically decreases risk tolerance
        elif emotion == 'panic':
            return -0.9 * intensity

        # Anxiety moderately decreases risk tolerance
        elif emotion == 'anxiety':
            return -0.5 * intensity

        else:
            return -0.3  # Default: slightly risk averse

    def _predict_time_horizon(self, emotion: str, intensity: float) -> str:
        """Predict shift in time horizon for decision making"""
        if emotion == 'panic' and intensity > 0.7:
            return 'immediate'  # Seconds to minutes
        elif emotion == 'fear' and intensity > 0.6:
            return 'very_short'  # Hours to days
        elif emotion == 'anxiety':
            return 'short'  # Days to weeks
        elif emotion == 'anger':
            return 'medium'  # Weeks to months
        else:
            return 'normal'  # Months to years

    def _predict_social_behaviors(self, emotion: str, event_data: Dict) -> List[str]:
        """Predict social behaviors"""
        behaviors = []

        if emotion == 'fear':
            behaviors.extend([
                'seeking_social_support',
                'following_authority',
                'conformity_increase',
                'trust_in_experts'
            ])

        elif emotion == 'anger':
            behaviors.extend([
                'protest_organization',
                'social_media_activism',
                'group_solidarity',
                'authority_questioning'
            ])

        elif emotion == 'panic':
            behaviors.extend([
                'competitive_behavior',
                'social_distancing',
                'every_person_for_themselves',
                'breakdown_of_norms'
            ])

        # Check for social unrest triggers
        if event_data.get('event_type') in ['social_unrest', 'governance_collapse']:
            behaviors.append('mass_mobilization')

        return behaviors

    def _predict_economic_behaviors(self, emotion: str, event_data: Dict) -> List[str]:
        """Predict economic behaviors"""
        behaviors = []

        if emotion == 'fear':
            behaviors.extend([
                'increase_savings',
                'reduce_discretionary_spending',
                'buy_defensive_stocks',
                'sell_risky_assets',
                'buy_gold_and_safe_havens',
                'delay_major_purchases'
            ])

        elif emotion == 'anger':
            behaviors.extend([
                'boycott_products',
                'switch_brands',
                'support_alternatives',
                'punish_perceived_wrongdoers'
            ])

        elif emotion == 'panic':
            behaviors.extend([
                'bulk_buying',
                'stockpiling_essentials',
                'bank_runs',
                'currency_flight',
                'asset_liquidation'
            ])

        # Market-specific behaviors
        market_impact = abs(event_data.get('market_impact', 0))
        if market_impact > 15:
            behaviors.append('stop_loss_triggering')
            behaviors.append('margin_calls')

        return behaviors

    def predict_crowd_psychology(self, event_data: Dict, population_size: int = 1000000) -> Dict:
        """
        Predict crowd/mass psychology dynamics

        Args:
            event_data: Event characteristics
            population_size: Size of affected population

        Returns:
            Dictionary with crowd psychology metrics
        """
        behavior_pred = self.predict_behavior(event_data)

        # Calculate social contagion potential
        uncertainty = event_data.get('uncertainty_level', 0.5)
        social_media_era = 0.9  # High connectivity in modern era

        contagion_rate = uncertainty * social_media_era * behavior_pred.emotion_intensity

        # Estimate cascading behavior
        herd_threshold = 0.3  # 30% of people need to act before others follow
        panic_threshold = 0.6  # 60% for panic cascade

        # Estimate behavioral cascade timing
        if behavior_pred.emotion_intensity > panic_threshold:
            cascade_hours = 2  # Very fast (panic)
        elif behavior_pred.emotion_intensity > herd_threshold:
            cascade_hours = 24  # Fast (herd behavior)
        else:
            cascade_hours = 168  # Slow (1 week)

        return {
            'contagion_rate': contagion_rate,
            'herd_behavior_probability': min(1.0, contagion_rate * 1.2),
            'panic_cascade_probability': min(1.0, contagion_rate * 0.8) if behavior_pred.dominant_emotion == 'panic' else 0.3,
            'cascade_speed_hours': cascade_hours,
            'affected_population_pct': min(100, contagion_rate * 100),
            'social_amplification_factor': 1 + (social_media_era * behavior_pred.emotion_intensity),
            'information_seeking_surge': uncertainty * 10,  # 10x normal at max uncertainty
            'misinformation_vulnerability': uncertainty * behavior_pred.emotion_intensity
        }

    def predict_market_participation(self, event_data: Dict) -> Dict:
        """
        Predict changes in market participation behavior

        Args:
            event_data: Event characteristics

        Returns:
            Dictionary with market participation predictions
        """
        behavior_pred = self.predict_behavior(event_data)

        # Base participation change
        participation_change = 0

        if behavior_pred.dominant_emotion == 'fear':
            participation_change = -0.3  # 30% reduction
        elif behavior_pred.dominant_emotion == 'panic':
            participation_change = -0.5  # 50% reduction (or spike then drop)
        elif behavior_pred.dominant_emotion == 'anger':
            participation_change = 0.1  # 10% increase (contrarian activity)

        # Volatility effect
        volatility_impact = abs(event_data.get('market_impact', 10)) / 50  # Normalize

        return {
            'retail_participation_change': participation_change,
            'institutional_participation_change': participation_change * 0.5,  # Less volatile
            'trading_volume_change': participation_change + volatility_impact,
            'options_activity_change': volatility_impact * 2,  # Options spike
            'short_selling_change': abs(participation_change) * 1.5 if participation_change < 0 else 0,
            'risk_off_flow': -participation_change if participation_change < 0 else 0,
            'cash_holdings_change': -participation_change * 0.8  # Inverse of participation
        }
