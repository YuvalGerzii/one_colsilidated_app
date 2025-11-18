# Multi-Agent System for Workforce Transition Platform
from .base_agent import BaseAgent, AgentResponse, AgentMessage, AgentCoordinator
from .gap_analyzer_agent import GapAnalyzerAgent
from .opportunity_agent import OpportunityDiscoveryAgent
from .learning_strategist_agent import LearningPathStrategistAgent
from .teaching_coach_agent import TeachingCoachAgent
from .career_navigator_agent import CareerNavigatorAgent

__all__ = [
    'BaseAgent',
    'AgentResponse',
    'AgentMessage',
    'AgentCoordinator',
    'GapAnalyzerAgent',
    'OpportunityDiscoveryAgent',
    'LearningPathStrategistAgent',
    'TeachingCoachAgent',
    'CareerNavigatorAgent'
]
