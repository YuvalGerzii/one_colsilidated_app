"""Agent implementations for the multi-agent system."""

from multi_agent_system.agents.base import BaseAgent
from multi_agent_system.agents.orchestrator import OrchestratorAgent
from multi_agent_system.agents.workers import (
    ResearchAgent,
    CodeAgent,
    TestAgent,
    DataAnalystAgent,
    GeneralAgent,
    create_worker_pool,
)
from multi_agent_system.agents.specialized import (
    AdvancedDataAnalysisAgent,
    AdvancedDataScienceAgent,
    AdvancedUIDesignAgent,
    AdvancedMarketingAgent,
    AdvancedFinanceAgent,
    AdvancedManagerCEOAgent,
    create_specialized_agent_pool,
)

__all__ = [
    "BaseAgent",
    "OrchestratorAgent",
    "ResearchAgent",
    "CodeAgent",
    "TestAgent",
    "DataAnalystAgent",
    "GeneralAgent",
    "AdvancedDataAnalysisAgent",
    "AdvancedDataScienceAgent",
    "AdvancedUIDesignAgent",
    "AdvancedMarketingAgent",
    "AdvancedFinanceAgent",
    "AdvancedManagerCEOAgent",
    "create_worker_pool",
    "create_specialized_agent_pool",
]
