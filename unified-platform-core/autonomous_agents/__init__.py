"""
Autonomous AI Agents Framework

Agents that can execute real-world actions without human intervention:
- Trading Execution Agent: Execute arbitrage trades
- Outreach Agent: Send personalized emails/messages
- Property Scout Agent: Find deals matching criteria
- Job Application Agent: Auto-apply to positions
- Document Processing Agent: Extract and classify documents

Safety Features:
- Configurable human-in-the-loop checkpoints
- Spending/action limits
- Rollback capabilities
- Audit logging
"""

__version__ = "1.0.0"

from .base_autonomous_agent import (
    BaseAutonomousAgent,
    AgentAction,
    ActionResult,
    AgentConfig,
    ActionType,
    ActionStatus,
    RiskLevel
)
from .trading_execution_agent import TradingExecutionAgent, create_trading_agent
from .outreach_agent import OutreachAgent, create_outreach_agent
from .property_scout_agent import PropertyScoutAgent, create_property_scout_agent
from .job_application_agent import JobApplicationAgent, create_job_application_agent
from .agent_supervisor import AgentSupervisor, create_agent_supervisor

__all__ = [
    "BaseAutonomousAgent",
    "AgentAction",
    "ActionResult",
    "AgentConfig",
    "ActionType",
    "ActionStatus",
    "RiskLevel",
    "TradingExecutionAgent",
    "create_trading_agent",
    "OutreachAgent",
    "create_outreach_agent",
    "PropertyScoutAgent",
    "create_property_scout_agent",
    "JobApplicationAgent",
    "create_job_application_agent",
    "AgentSupervisor",
    "create_agent_supervisor"
]
