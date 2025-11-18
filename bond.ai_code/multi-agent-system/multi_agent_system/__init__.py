"""
Multi-Agent System with Reinforcement Learning

A fully functional, locally-running multi-agent system with reinforcement learning capabilities.
"""

from multi_agent_system.core.system import MultiAgentSystem
from multi_agent_system.agents.base import BaseAgent
from multi_agent_system.agents.orchestrator import OrchestratorAgent
from multi_agent_system.core.types import Task, Result, Message, AgentCapability

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
