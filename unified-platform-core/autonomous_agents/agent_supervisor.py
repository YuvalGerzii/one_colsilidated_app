"""
Agent Supervisor

Oversees and coordinates multiple autonomous agents.
Provides monitoring, resource allocation, and safety controls.

Features:
- Agent lifecycle management
- Resource allocation and limits
- Cross-agent coordination
- Safety monitoring
- Performance analytics
"""

from typing import Dict, List, Any, Optional, Type
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import asyncio
import logging

from .base_autonomous_agent import (
    BaseAutonomousAgent, AgentConfig, ActionStatus, RiskLevel
)

logger = logging.getLogger(__name__)


class SupervisorAlert(Enum):
    """Types of supervisor alerts"""
    BUDGET_WARNING = "budget_warning"
    BUDGET_EXCEEDED = "budget_exceeded"
    ACTION_LIMIT_WARNING = "action_limit_warning"
    ACTION_LIMIT_EXCEEDED = "action_limit_exceeded"
    ERROR_RATE_HIGH = "error_rate_high"
    AGENT_UNRESPONSIVE = "agent_unresponsive"
    APPROVAL_REQUIRED = "approval_required"
    SAFETY_VIOLATION = "safety_violation"


@dataclass
class AgentMetrics:
    """Performance metrics for an agent"""
    agent_id: str
    total_actions: int = 0
    successful_actions: int = 0
    failed_actions: int = 0
    total_spend_usd: float = 0.0
    avg_response_time_ms: float = 0.0
    last_action_time: Optional[datetime] = None
    error_rate: float = 0.0
    uptime_percentage: float = 100.0


@dataclass
class SupervisorConfig:
    """Configuration for the agent supervisor"""
    supervisor_id: str
    name: str = "Agent Supervisor"

    # Global limits
    global_spending_limit_usd: float = 1000.0
    global_daily_action_limit: int = 10000

    # Alert thresholds
    budget_warning_threshold: float = 0.8  # 80% of budget
    error_rate_threshold: float = 0.1  # 10% error rate
    unresponsive_threshold_seconds: int = 300  # 5 minutes

    # Safety settings
    require_approval_for_high_risk: bool = True
    pause_on_repeated_failures: int = 5
    emergency_stop_enabled: bool = True


class AgentSupervisor:
    """
    Supervises and coordinates autonomous agents.

    Responsibilities:
    - Register and manage agents
    - Monitor performance and health
    - Enforce resource limits
    - Coordinate cross-agent workflows
    - Handle approvals and escalations
    """

    def __init__(self, config: SupervisorConfig):
        self.config = config
        self.agents: Dict[str, BaseAutonomousAgent] = {}
        self.metrics: Dict[str, AgentMetrics] = {}
        self.alerts: List[Dict[str, Any]] = []
        self.approval_queue: List[Dict[str, Any]] = []
        self.global_spend: float = 0.0
        self.global_actions_today: int = 0
        self.paused_agents: set = set()
        self.emergency_stop: bool = False

    def register_agent(self, agent: BaseAutonomousAgent):
        """Register an agent with the supervisor"""

        agent_id = agent.config.agent_id
        self.agents[agent_id] = agent
        self.metrics[agent_id] = AgentMetrics(agent_id=agent_id)

        logger.info(f"Registered agent: {agent_id}")

    def unregister_agent(self, agent_id: str):
        """Unregister an agent"""

        if agent_id in self.agents:
            del self.agents[agent_id]
            del self.metrics[agent_id]
            logger.info(f"Unregistered agent: {agent_id}")

    async def start_agent(
        self,
        agent_id: str,
        objective: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Start an agent with an objective"""

        if self.emergency_stop:
            return {
                "status": "blocked",
                "reason": "Emergency stop is active"
            }

        if agent_id not in self.agents:
            return {
                "status": "error",
                "reason": f"Agent {agent_id} not registered"
            }

        if agent_id in self.paused_agents:
            return {
                "status": "paused",
                "reason": f"Agent {agent_id} is paused due to repeated failures"
            }

        # Check global limits
        limit_check = await self._check_global_limits()
        if not limit_check["allowed"]:
            return {
                "status": "blocked",
                "reason": limit_check["reason"]
            }

        agent = self.agents[agent_id]

        # Run the agent
        try:
            result = await agent.run(objective, context)

            # Update metrics
            await self._update_metrics(agent_id, result)

            return {
                "status": "completed",
                "agent_id": agent_id,
                "result": result
            }

        except Exception as e:
            logger.error(f"Agent {agent_id} failed: {e}")
            await self._handle_agent_failure(agent_id, str(e))

            return {
                "status": "error",
                "agent_id": agent_id,
                "error": str(e)
            }

    async def _check_global_limits(self) -> Dict[str, Any]:
        """Check if global limits allow more actions"""

        # Check spending
        if self.global_spend >= self.config.global_spending_limit_usd:
            await self._create_alert(
                SupervisorAlert.BUDGET_EXCEEDED,
                f"Global spending limit exceeded: ${self.global_spend:.2f}"
            )
            return {
                "allowed": False,
                "reason": "Global spending limit exceeded"
            }

        # Check action count
        if self.global_actions_today >= self.config.global_daily_action_limit:
            await self._create_alert(
                SupervisorAlert.ACTION_LIMIT_EXCEEDED,
                f"Global daily action limit exceeded: {self.global_actions_today}"
            )
            return {
                "allowed": False,
                "reason": "Global daily action limit exceeded"
            }

        # Warning alerts
        if self.global_spend >= self.config.global_spending_limit_usd * self.config.budget_warning_threshold:
            await self._create_alert(
                SupervisorAlert.BUDGET_WARNING,
                f"Global spending at {(self.global_spend / self.config.global_spending_limit_usd * 100):.1f}% of limit"
            )

        return {"allowed": True}

    async def _update_metrics(
        self,
        agent_id: str,
        result: Dict[str, Any]
    ):
        """Update agent metrics after execution"""

        metrics = self.metrics[agent_id]

        # Update action counts
        actions_executed = result.get("actions_executed", 0)
        successful = result.get("successful", 0)
        failed = result.get("failed", 0)

        metrics.total_actions += actions_executed
        metrics.successful_actions += successful
        metrics.failed_actions += failed
        metrics.last_action_time = datetime.now()

        # Update spend
        spend = result.get("total_spend_usd", 0.0)
        metrics.total_spend_usd += spend
        self.global_spend += spend

        # Update global action count
        self.global_actions_today += actions_executed

        # Calculate error rate
        if metrics.total_actions > 0:
            metrics.error_rate = metrics.failed_actions / metrics.total_actions

        # Check for high error rate
        if metrics.error_rate >= self.config.error_rate_threshold:
            await self._create_alert(
                SupervisorAlert.ERROR_RATE_HIGH,
                f"Agent {agent_id} error rate: {metrics.error_rate:.1%}"
            )

    async def _handle_agent_failure(self, agent_id: str, error: str):
        """Handle agent failure"""

        metrics = self.metrics[agent_id]
        metrics.failed_actions += 1

        # Check for repeated failures
        recent_failures = metrics.failed_actions
        if recent_failures >= self.config.pause_on_repeated_failures:
            self.paused_agents.add(agent_id)
            await self._create_alert(
                SupervisorAlert.SAFETY_VIOLATION,
                f"Agent {agent_id} paused after {recent_failures} failures"
            )

    async def _create_alert(
        self,
        alert_type: SupervisorAlert,
        message: str
    ):
        """Create a supervisor alert"""

        alert = {
            "alert_id": f"alert_{datetime.now().timestamp()}",
            "type": alert_type.value,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "acknowledged": False
        }

        self.alerts.append(alert)
        logger.warning(f"Supervisor Alert: {alert_type.value} - {message}")

    async def request_approval(
        self,
        agent_id: str,
        action: Dict[str, Any],
        reason: str
    ) -> str:
        """Request human approval for an action"""

        request = {
            "request_id": f"approval_{datetime.now().timestamp()}",
            "agent_id": agent_id,
            "action": action,
            "reason": reason,
            "requested_at": datetime.now().isoformat(),
            "status": "pending"
        }

        self.approval_queue.append(request)

        await self._create_alert(
            SupervisorAlert.APPROVAL_REQUIRED,
            f"Agent {agent_id} requires approval: {reason}"
        )

        return request["request_id"]

    async def approve_request(self, request_id: str) -> bool:
        """Approve a pending request"""

        for request in self.approval_queue:
            if request["request_id"] == request_id:
                request["status"] = "approved"
                request["approved_at"] = datetime.now().isoformat()
                return True

        return False

    async def deny_request(self, request_id: str, reason: str) -> bool:
        """Deny a pending request"""

        for request in self.approval_queue:
            if request["request_id"] == request_id:
                request["status"] = "denied"
                request["denied_at"] = datetime.now().isoformat()
                request["denial_reason"] = reason
                return True

        return False

    def trigger_emergency_stop(self, reason: str):
        """Trigger emergency stop for all agents"""

        self.emergency_stop = True
        logger.critical(f"EMERGENCY STOP triggered: {reason}")

        asyncio.create_task(self._create_alert(
            SupervisorAlert.SAFETY_VIOLATION,
            f"Emergency stop: {reason}"
        ))

    def resume_operations(self):
        """Resume operations after emergency stop"""

        self.emergency_stop = False
        logger.info("Operations resumed")

    def resume_agent(self, agent_id: str):
        """Resume a paused agent"""

        if agent_id in self.paused_agents:
            self.paused_agents.remove(agent_id)
            # Reset failure count
            if agent_id in self.metrics:
                self.metrics[agent_id].failed_actions = 0
            logger.info(f"Agent {agent_id} resumed")

    async def coordinate_agents(
        self,
        agent_ids: List[str],
        workflow: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Coordinate multiple agents for a workflow"""

        results = {}

        for step in workflow.get("steps", []):
            agent_id = step.get("agent_id")
            objective = step.get("objective")
            context = step.get("context", {})

            # Add previous results to context
            context["previous_results"] = results

            if agent_id in agent_ids and agent_id in self.agents:
                result = await self.start_agent(agent_id, objective, context)
                results[step.get("step_id", agent_id)] = result

                # Check for failures
                if result.get("status") == "error":
                    if workflow.get("stop_on_failure", True):
                        break

        return {
            "workflow_id": workflow.get("id", "unknown"),
            "status": "completed",
            "results": results
        }

    def get_agent_status(self, agent_id: str) -> Dict[str, Any]:
        """Get status of a specific agent"""

        if agent_id not in self.agents:
            return {"error": f"Agent {agent_id} not found"}

        agent = self.agents[agent_id]
        metrics = self.metrics.get(agent_id, AgentMetrics(agent_id=agent_id))

        return {
            "agent_id": agent_id,
            "name": agent.config.name,
            "enabled": agent.config.enabled,
            "paused": agent_id in self.paused_agents,
            "metrics": {
                "total_actions": metrics.total_actions,
                "success_rate": (metrics.successful_actions / metrics.total_actions * 100) if metrics.total_actions > 0 else 0,
                "total_spend": metrics.total_spend_usd,
                "error_rate": metrics.error_rate
            },
            "last_action": metrics.last_action_time.isoformat() if metrics.last_action_time else None
        }

    def get_all_status(self) -> Dict[str, Any]:
        """Get status of all agents and supervisor"""

        return {
            "supervisor": {
                "id": self.config.supervisor_id,
                "emergency_stop": self.emergency_stop,
                "global_spend": self.global_spend,
                "global_actions_today": self.global_actions_today,
                "pending_approvals": len([r for r in self.approval_queue if r["status"] == "pending"]),
                "active_alerts": len([a for a in self.alerts if not a["acknowledged"]])
            },
            "agents": {
                agent_id: self.get_agent_status(agent_id)
                for agent_id in self.agents
            },
            "paused_agents": list(self.paused_agents)
        }

    def get_alerts(
        self,
        unacknowledged_only: bool = True
    ) -> List[Dict[str, Any]]:
        """Get supervisor alerts"""

        if unacknowledged_only:
            return [a for a in self.alerts if not a["acknowledged"]]
        return self.alerts

    def acknowledge_alert(self, alert_id: str):
        """Acknowledge an alert"""

        for alert in self.alerts:
            if alert["alert_id"] == alert_id:
                alert["acknowledged"] = True
                alert["acknowledged_at"] = datetime.now().isoformat()
                break

    def reset_daily_limits(self):
        """Reset daily action limits (call at midnight)"""

        self.global_actions_today = 0
        logger.info("Daily action limits reset")


# Factory function
def create_agent_supervisor(
    supervisor_id: str = "main_supervisor",
    global_spending_limit: float = 1000.0,
    global_action_limit: int = 10000
) -> AgentSupervisor:
    """Create a configured agent supervisor"""

    config = SupervisorConfig(
        supervisor_id=supervisor_id,
        global_spending_limit_usd=global_spending_limit,
        global_daily_action_limit=global_action_limit
    )

    return AgentSupervisor(config)
