"""
Extreme Events Market Prediction Platform - Enhanced Version

A comprehensive platform for predicting and analyzing market reactions to extreme events.

Features:
- 13+ event types including pandemic, terrorism, cyber attacks, climate crisis, etc.
- Generalized event handling framework
- Human behavior prediction based on behavioral economics
- Market direction prediction (winners/losers)
- Free LLM-based multi-agent analysis system
- Comprehensive forecasting and risk analysis

Version 2.0 - Enhanced with Multi-Agent AI
"""

# Main orchestrators
from .orchestrator import ExtremeEventsOrchestrator
from .enhanced_orchestrator import EnhancedExtremeEventsOrchestrator

# Core frameworks
from .core.generalized_framework import GeneralizedEventFramework, EventCharacteristics
from .behavioral.human_behavior_predictor import HumanBehaviorPredictor
from .market.direction_predictor import MarketDirectionPredictor
from .multi_agent.multi_agent_orchestrator import MultiAgentOrchestrator

# Original agents
from .agents import (
    PandemicAgent,
    TerrorismAgent,
    NaturalDisasterAgent,
    EconomicCrisisAgent,
    GeopoliticalAgent
)

# New agents
from .agents.cyber_attack_agent import CyberAttackAgent
from .agents.climate_crisis_agent import ClimateCrisisAgent
from .agents.compound_event_agent import CompoundEventAgent

# Models
from .models import ExtremeValueTheoryModel, MLExtremeEventPredictor

__version__ = '2.0.0'

__all__ = [
    # Main orchestrators
    'ExtremeEventsOrchestrator',
    'EnhancedExtremeEventsOrchestrator',

    # Core frameworks
    'GeneralizedEventFramework',
    'EventCharacteristics',
    'HumanBehaviorPredictor',
    'MarketDirectionPredictor',
    'MultiAgentOrchestrator',

    # Original agents
    'PandemicAgent',
    'TerrorismAgent',
    'NaturalDisasterAgent',
    'EconomicCrisisAgent',
    'GeopoliticalAgent',

    # New agents
    'CyberAttackAgent',
    'ClimateCrisisAgent',
    'CompoundEventAgent',

    # Models
    'ExtremeValueTheoryModel',
    'MLExtremeEventPredictor'
]


# Quick start helper
def quick_analysis(event_type: str, event_data: dict) -> dict:
    """
    Quick analysis helper function

    Example:
        >>> result = quick_analysis('pandemic', {'severity': 4, 'r0': 3.5})
        >>> print(result['synthesis']['market_impact_estimate'])
    """
    orchestrator = EnhancedExtremeEventsOrchestrator(enable_llm=False)
    return orchestrator.comprehensive_analysis(event_type, event_data, use_llm_agents=False)
