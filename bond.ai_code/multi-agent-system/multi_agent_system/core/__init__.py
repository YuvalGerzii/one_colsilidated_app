"""Core module for multi-agent system."""

from multi_agent_system.core.system import MultiAgentSystem
from multi_agent_system.core.types import (
    Task,
    Result,
    Message,
    AgentCapability,
    TaskStatus,
    MessageType,
    Experience,
)
from multi_agent_system.core.context_protocol import ContextProtocol, ContextType, ContextScope
from multi_agent_system.core.scaling import ScalingStrategy, TaskComplexity, LoadBalancer
from multi_agent_system.core.resilience import ResilientExecutor, RetryStrategy, CircuitBreaker

__all__ = [
    "MultiAgentSystem",
    "Task",
    "Result",
    "Message",
    "AgentCapability",
    "TaskStatus",
    "MessageType",
    "Experience",
    "ContextProtocol",
    "ContextType",
    "ContextScope",
    "ScalingStrategy",
    "TaskComplexity",
    "LoadBalancer",
    "ResilientExecutor",
    "RetryStrategy",
    "CircuitBreaker",
]
