"""
Generalized Event Framework
Handles any type of extreme event with a flexible, extensible architecture
"""

from typing import Dict, List, Any, Optional, Type
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class EventCategory(Enum):
    """Categories of extreme events"""
    PHYSICAL = "physical"
    HEALTH = "health"
    SECURITY = "security"
    ECONOMIC = "economic"
    TECHNOLOGICAL = "technological"
    POLITICAL = "political"
    COMPOUND = "compound"
    UNKNOWN = "unknown"


class EventSeverity(Enum):
    """Standardized severity levels"""
    MINIMAL = 1
    MODERATE = 2
    SIGNIFICANT = 3
    SEVERE = 4
    CATASTROPHIC = 5


@dataclass
class EventCharacteristics:
    """
    Standardized characteristics for any extreme event
    """
    event_type: str
    event_subtype: Optional[str] = None
    category: EventCategory = EventCategory.UNKNOWN

    # Spatial characteristics
    geographic_scope: str = "regional"  # local, regional, national, continental, global
    affected_regions: List[str] = field(default_factory=list)
    epicenter_location: Optional[str] = None

    # Temporal characteristics
    onset_date: Optional[datetime] = None
    duration_estimate_days: int = 30
    is_ongoing: bool = True
    is_sudden_onset: bool = True

    # Impact characteristics
    severity: int = 3  # 1-5
    casualty_count: int = 0
    economic_loss_usd: float = 0
    population_affected: int = 0

    # Uncertainty and data quality
    data_quality: str = "medium"  # low, medium, high
    uncertainty_level: float = 0.5  # 0-1
    information_completeness: float = 0.7  # 0-1

    # Behavioral triggers
    fear_factor: float = 0.5  # 0-1
    anger_factor: float = 0.0  # 0-1
    uncertainty_factor: float = 0.5  # 0-1

    # Systemic characteristics
    contagion_risk: float = 0.3  # 0-1
    systemic_risk: float = 0.3  # 0-1
    cascading_potential: float = 0.3  # 0-1

    # Response characteristics
    policy_response_speed: str = "moderate"  # slow, moderate, fast
    policy_response_strength: str = "moderate"  # weak, moderate, strong
    international_coordination: bool = False

    # Market-specific
    market_sentiment_before: float = 0.5  # 0-1
    volatility_before: float = 15.0  # VIX-like
    liquidity_before: float = 1.0

    # Metadata
    similar_historical_events: List[str] = field(default_factory=list)
    unique_features: List[str] = field(default_factory=list)
    custom_attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PredictionOutput:
    """
    Standardized prediction output for any event
    """
    event_id: str
    prediction_timestamp: datetime

    # Market predictions
    market_impact_pct: float
    market_impact_confidence: float  # 0-1
    volatility_increase_pct: float

    # Time-based predictions
    immediate_impact_24h: float
    short_term_7d: float
    medium_term_30d: float
    long_term_90d: float

    # Sector predictions
    sector_winners: Dict[str, float]  # sector -> expected gain %
    sector_losers: Dict[str, float]   # sector -> expected loss %

    # Behavioral predictions
    dominant_emotion: str  # fear, anger, panic, optimism
    risk_tolerance_change: float  # -1 to 1
    herd_behavior_likelihood: float  # 0-1
    panic_buying_likelihood: float  # 0-1

    # Recovery predictions
    recovery_timeline_days: int
    recovery_shape: str  # V, U, L, W
    full_recovery_probability: float  # 0-1

    # Risk metrics
    var_95: float
    cvar_95: float
    tail_risk_score: float  # 0-10

    # Recommendations
    risk_level: str  # low, moderate, high, critical
    recommended_actions: List[str]
    opportunities: List[Dict[str, Any]]
    threats: List[Dict[str, Any]]

    # Metadata
    prediction_method: str
    model_ensemble: List[str]
    key_assumptions: List[str]


class GeneralizedEventFramework:
    """
    Framework that can handle any type of extreme event
    """

    def __init__(self):
        self.event_registry = {}  # Registry of all event types
        self.agent_registry = {}  # Registry of specialized agents
        self.prediction_history = []

    def register_event_type(self, event_type: str, characteristics: Dict):
        """
        Register a new event type with the framework

        Args:
            event_type: Name of the event type
            characteristics: Default characteristics
        """
        self.event_registry[event_type] = characteristics

    def register_agent(self, event_type: str, agent: Any):
        """
        Register a specialized agent for an event type

        Args:
            event_type: Event type this agent handles
            agent: Agent instance
        """
        self.agent_registry[event_type] = agent

    def classify_event(self, event_data: Dict) -> EventCategory:
        """
        Automatically classify an event into a category

        Args:
            event_data: Event data dictionary

        Returns:
            EventCategory enum
        """
        event_type = event_data.get('event_type', '').lower()

        # Classification rules
        if 'pandemic' in event_type or 'health' in event_type:
            return EventCategory.HEALTH
        elif 'cyber' in event_type or 'terror' in event_type:
            return EventCategory.SECURITY
        elif 'economic' in event_type or 'financial' in event_type or 'crisis' in event_type:
            return EventCategory.ECONOMIC
        elif 'climate' in event_type or 'disaster' in event_type or 'natural' in event_type:
            return EventCategory.PHYSICAL
        elif 'tech' in event_type or 'ai' in event_type or 'infrastructure' in event_type:
            return EventCategory.TECHNOLOGICAL
        elif 'war' in event_type or 'politic' in event_type or 'governance' in event_type:
            return EventCategory.POLITICAL
        elif 'compound' in event_type or 'multiple' in event_type:
            return EventCategory.COMPOUND
        else:
            return EventCategory.UNKNOWN

    def normalize_event_data(self, event_data: Dict) -> EventCharacteristics:
        """
        Convert any event data format to standardized EventCharacteristics

        Args:
            event_data: Raw event data in any format

        Returns:
            Normalized EventCharacteristics
        """
        # Extract common fields with fallbacks
        return EventCharacteristics(
            event_type=event_data.get('event_type', 'unknown'),
            event_subtype=event_data.get('event_subtype') or event_data.get('crisis_type') or event_data.get('disaster_type'),
            category=self.classify_event(event_data),

            geographic_scope=event_data.get('geographic_scope', 'regional'),
            affected_regions=event_data.get('affected_regions') or event_data.get('affected_countries') or event_data.get('countries_involved', []),
            epicenter_location=event_data.get('location') or event_data.get('epicenter'),

            duration_estimate_days=event_data.get('duration_estimate_days') or event_data.get('duration_estimate_months', 1) * 30,

            severity=event_data.get('severity', 3),
            casualty_count=event_data.get('casualties') or event_data.get('casualty_count', 0),
            economic_loss_usd=event_data.get('economic_losses_usd') or event_data.get('economic_loss_usd', 0),
            population_affected=event_data.get('population_affected', 0),

            data_quality=event_data.get('data_quality', 'medium'),

            # Behavioral factors
            fear_factor=self._calculate_fear_factor(event_data),
            anger_factor=self._calculate_anger_factor(event_data),
            uncertainty_factor=event_data.get('uncertainty_level', 0.5),

            contagion_risk=event_data.get('contagion_risk', 0.3),
            systemic_risk=event_data.get('systemic_risk_score', 0.3) / 10.0 if event_data.get('systemic_risk_score') else 0.3,

            custom_attributes=event_data
        )

    def _calculate_fear_factor(self, event_data: Dict) -> float:
        """
        Calculate fear factor from event characteristics
        """
        fear = 0.5

        # High casualties increase fear
        casualties = event_data.get('casualties', 0)
        if casualties > 1000:
            fear += 0.3
        elif casualties > 100:
            fear += 0.2
        elif casualties > 10:
            fear += 0.1

        # Unknown/novel threats increase fear
        if event_data.get('novel_threat', False):
            fear += 0.2

        # Systemic risk increases fear
        if event_data.get('systemic_risk_score', 0) > 7:
            fear += 0.2

        return min(1.0, fear)

    def _calculate_anger_factor(self, event_data: Dict) -> float:
        """
        Calculate anger factor from event characteristics
        """
        anger = 0.0

        # Perceived injustice or human cause
        if event_data.get('human_caused', False):
            anger += 0.3

        if event_data.get('preventable', False):
            anger += 0.2

        if event_data.get('inequality_impact', False):
            anger += 0.3

        return min(1.0, anger)

    def can_handle_event(self, event_type: str) -> bool:
        """
        Check if framework can handle this event type

        Args:
            event_type: Event type string

        Returns:
            True if can handle, False otherwise
        """
        # Framework can handle any event if it has a registered agent
        # or can use the generalized approach
        return event_type in self.agent_registry or True

    def get_applicable_agents(self, event_characteristics: EventCharacteristics) -> List[str]:
        """
        Determine which agents should analyze this event

        Args:
            event_characteristics: Normalized event characteristics

        Returns:
            List of applicable agent types
        """
        agents = []

        # Primary agent based on event type
        if event_characteristics.event_type in self.agent_registry:
            agents.append(event_characteristics.event_type)

        # Category-based agents
        category_map = {
            EventCategory.HEALTH: ['pandemic', 'public_health_crisis'],
            EventCategory.SECURITY: ['terrorism', 'cyber_attack'],
            EventCategory.ECONOMIC: ['economic_crisis', 'supply_chain_collapse'],
            EventCategory.PHYSICAL: ['natural_disaster', 'climate_crisis'],
            EventCategory.TECHNOLOGICAL: ['technology_disruption'],
            EventCategory.POLITICAL: ['geopolitical', 'governance_collapse']
        }

        if event_characteristics.category in category_map:
            agents.extend([a for a in category_map[event_characteristics.category] if a in self.agent_registry])

        return list(set(agents))  # Remove duplicates

    def estimate_impact_severity(self, event_characteristics: EventCharacteristics) -> int:
        """
        Estimate severity (1-5) from characteristics using generalized rules

        Args:
            event_characteristics: Event characteristics

        Returns:
            Severity score 1-5
        """
        # If severity already provided, use it
        if event_characteristics.severity:
            return event_characteristics.severity

        # Otherwise, estimate from other factors
        score = 3  # Default moderate

        # Adjust based on scope
        scope_map = {'local': -1, 'regional': 0, 'national': 0, 'continental': 1, 'global': 2}
        score += scope_map.get(event_characteristics.geographic_scope, 0)

        # Adjust based on casualties (logarithmic scale)
        if event_characteristics.casualty_count > 10000:
            score += 2
        elif event_characteristics.casualty_count > 1000:
            score += 1
        elif event_characteristics.casualty_count > 100:
            score += 0.5

        # Adjust based on economic loss (in billions)
        loss_billions = event_characteristics.economic_loss_usd / 1e9
        if loss_billions > 100:
            score += 2
        elif loss_billions > 10:
            score += 1
        elif loss_billions > 1:
            score += 0.5

        # Adjust based on systemic/contagion risk
        if event_characteristics.systemic_risk > 0.7 or event_characteristics.contagion_risk > 0.7:
            score += 1

        return max(1, min(5, int(round(score))))

    def create_standardized_prediction(
        self,
        event_characteristics: EventCharacteristics,
        analysis_results: Dict
    ) -> PredictionOutput:
        """
        Convert analysis results to standardized prediction output

        Args:
            event_characteristics: Normalized event characteristics
            analysis_results: Results from agent analysis

        Returns:
            Standardized PredictionOutput
        """
        # Extract or compute each field
        return PredictionOutput(
            event_id=f"{event_characteristics.event_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            prediction_timestamp=datetime.now(),

            market_impact_pct=analysis_results.get('market_impact', -10.0),
            market_impact_confidence=analysis_results.get('confidence', 0.7),
            volatility_increase_pct=analysis_results.get('volatility_increase', 20.0),

            immediate_impact_24h=analysis_results.get('immediate_impact', -12.0),
            short_term_7d=analysis_results.get('short_term', -10.0),
            medium_term_30d=analysis_results.get('medium_term', -7.0),
            long_term_90d=analysis_results.get('long_term', -4.0),

            sector_winners=analysis_results.get('winners', {}),
            sector_losers=analysis_results.get('losers', {}),

            dominant_emotion=self._determine_dominant_emotion(event_characteristics),
            risk_tolerance_change=self._estimate_risk_tolerance_change(event_characteristics),
            herd_behavior_likelihood=event_characteristics.uncertainty_factor,
            panic_buying_likelihood=event_characteristics.fear_factor * 0.7,

            recovery_timeline_days=analysis_results.get('recovery_days', 90),
            recovery_shape=analysis_results.get('recovery_shape', 'U'),
            full_recovery_probability=0.7,

            var_95=analysis_results.get('var_95', -15.0),
            cvar_95=analysis_results.get('cvar_95', -20.0),
            tail_risk_score=event_characteristics.severity * 2,

            risk_level=self._categorize_risk_level(event_characteristics.severity),
            recommended_actions=analysis_results.get('recommendations', []),
            opportunities=analysis_results.get('opportunities', []),
            threats=analysis_results.get('threats', []),

            prediction_method="generalized_framework",
            model_ensemble=analysis_results.get('models_used', ['generalized']),
            key_assumptions=analysis_results.get('assumptions', [])
        )

    def _determine_dominant_emotion(self, event: EventCharacteristics) -> str:
        """Determine dominant emotional response"""
        if event.fear_factor > 0.7:
            return 'fear'
        elif event.anger_factor > 0.6:
            return 'anger'
        elif event.uncertainty_factor > 0.7:
            return 'anxiety'
        else:
            return 'concern'

    def _estimate_risk_tolerance_change(self, event: EventCharacteristics) -> float:
        """Estimate change in risk tolerance (-1 to 1)"""
        # Fear decreases risk tolerance
        change = -event.fear_factor * 0.7

        # Anger can increase risk-taking
        change += event.anger_factor * 0.3

        return max(-1.0, min(1.0, change))

    def _categorize_risk_level(self, severity: int) -> str:
        """Categorize risk level from severity"""
        if severity >= 5:
            return 'catastrophic'
        elif severity >= 4:
            return 'critical'
        elif severity >= 3:
            return 'high'
        elif severity >= 2:
            return 'moderate'
        else:
            return 'low'
