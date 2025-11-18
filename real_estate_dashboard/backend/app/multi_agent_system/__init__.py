"""
Multi-Agent System with Reinforcement Learning

A fully functional, locally-running multi-agent system with reinforcement learning capabilities.
"""

from app.multi_agent_system.core.system import MultiAgentSystem
from app.multi_agent_system.agents.base import BaseAgent
from app.multi_agent_system.agents.orchestrator import OrchestratorAgent
from app.multi_agent_system.core.types import Task, Result, Message, AgentCapability

__version__ = "0.1.0"
__author__ = "Multi-Agent System Team"

__all__ = [
    "MultiAgentSystem",
    "BaseAgent",
    "OrchestratorAgent",
    "Task",
    "Result",
    "Message",
    "AgentCapability",
]
