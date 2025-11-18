"""
Base Autonomous Agent

Abstract base class for all autonomous agents that can execute real-world actions.
Includes safety controls, audit logging, and human-in-the-loop checkpoints.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import asyncio
import logging
import uuid

logger = logging.getLogger(__name__)


class ActionType(Enum):
    """Types of actions agents can take"""
    EXECUTE_TRADE = "execute_trade"
    SEND_EMAIL = "send_email"
    SEND_MESSAGE = "send_message"
    SUBMIT_APPLICATION = "submit_application"
    CREATE_DOCUMENT = "create_document"
    MAKE_API_CALL = "make_api_call"
    UPDATE_DATABASE = "update_database"
    SCHEDULE_MEETING = "schedule_meeting"
    PROCESS_PAYMENT = "process_payment"


class ActionStatus(Enum):
    """Status of an action"""
    PENDING = "pending"
    APPROVED = "approved"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"
    REQUIRES_APPROVAL = "requires_approval"


class RiskLevel(Enum):
    """Risk level of an action"""
    LOW = "low"           # Auto-execute
    MEDIUM = "medium"     # Log and execute
    HIGH = "high"         # Require approval
    CRITICAL = "critical" # Require multi-party approval


@dataclass
class AgentAction:
    """Represents an action to be executed"""
    action_id: str
    action_type: ActionType
    description: str
    parameters: Dict[str, Any]
    risk_level: RiskLevel
    estimated_impact: Dict[str, Any]
    rollback_steps: List[str]
    requires_approval: bool = False
    approval_reason: Optional[str] = None
    deadline: Optional[datetime] = None
    dependencies: List[str] = field(default_factory=list)


@dataclass
class ActionResult:
    """Result of an executed action"""
    action_id: str
    status: ActionStatus
    result: Any
    error: Optional[str] = None
    execution_time_ms: int = 0
    side_effects: List[str] = field(default_factory=list)
    rollback_available: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentConfig:
    """Configuration for autonomous agent behavior"""
    agent_id: str
    name: str
    max_concurrent_actions: int = 5
    action_timeout_seconds: int = 60
    auto_approve_risk_levels: List[RiskLevel] = field(
        default_factory=lambda: [RiskLevel.LOW]
    )
    spending_limit_usd: float = 1000.0
    daily_action_limit: int = 100
    require_human_approval_above: float = 500.0
    enabled: bool = True
    dry_run: bool = False  # If True, don't execute, just simulate


class BaseAutonomousAgent(ABC):
    """
    Base class for autonomous agents.

    Provides:
    - Action planning and execution
    - Safety controls and limits
    - Audit logging
    - Human-in-the-loop checkpoints
    - Rollback capabilities
    """

    def __init__(self, config: AgentConfig):
        self.config = config
        self.action_history: List[ActionResult] = []
        self.pending_actions: Dict[str, AgentAction] = {}
        self.daily_spend: float = 0.0
        self.daily_action_count: int = 0
        self._approval_callbacks: List[Callable] = []
        self._execution_lock = asyncio.Lock()

    @abstractmethod
    async def plan_actions(
        self,
        objective: str,
        context: Dict[str, Any]
    ) -> List[AgentAction]:
        """
        Plan actions needed to achieve an objective.

        Returns list of actions in execution order.
        """
        pass

    @abstractmethod
    async def execute_action(
        self,
        action: AgentAction
    ) -> ActionResult:
        """
        Execute a single action.

        Must be implemented by each specific agent.
        """
        pass

    @abstractmethod
    async def rollback_action(
        self,
        action_id: str
    ) -> bool:
        """
        Rollback a previously executed action.

        Returns True if rollback successful.
        """
        pass

    async def run(
        self,
        objective: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Main entry point to run the agent.

        Plans and executes all necessary actions.
        """

        if not self.config.enabled:
            return {"status": "disabled", "message": "Agent is disabled"}

        logger.info(f"Agent {self.config.name} starting with objective: {objective}")

        # Plan actions
        actions = await self.plan_actions(objective, context)

        if not actions:
            return {"status": "no_actions", "message": "No actions planned"}

        # Validate all actions
        validation_results = await self._validate_actions(actions)
        if not all(v["valid"] for v in validation_results):
            return {
                "status": "validation_failed",
                "validation": validation_results
            }

        # Check for actions requiring approval
        actions_needing_approval = [
            a for a in actions
            if self._requires_approval(a)
        ]

        if actions_needing_approval:
            # Queue for approval
            for action in actions_needing_approval:
                self.pending_actions[action.action_id] = action
                await self._request_approval(action)

            return {
                "status": "pending_approval",
                "pending_actions": [a.action_id for a in actions_needing_approval]
            }

        # Execute all actions
        results = await self._execute_actions(actions)

        return {
            "status": "completed",
            "results": results,
            "summary": self._generate_summary(results)
        }

    async def _validate_actions(
        self,
        actions: List[AgentAction]
    ) -> List[Dict[str, Any]]:
        """Validate all planned actions"""

        results = []

        for action in actions:
            validation = {"action_id": action.action_id, "valid": True, "errors": []}

            # Check daily limits
            if self.daily_action_count >= self.config.daily_action_limit:
                validation["valid"] = False
                validation["errors"].append("Daily action limit reached")

            # Check spending limits
            estimated_cost = action.estimated_impact.get("cost_usd", 0)
            if self.daily_spend + estimated_cost > self.config.spending_limit_usd:
                validation["valid"] = False
                validation["errors"].append(
                    f"Would exceed spending limit: ${self.daily_spend + estimated_cost} > ${self.config.spending_limit_usd}"
                )

            # Check dependencies
            for dep_id in action.dependencies:
                if dep_id not in [a.action_id for a in actions]:
                    validation["valid"] = False
                    validation["errors"].append(f"Missing dependency: {dep_id}")

            results.append(validation)

        return results

    def _requires_approval(self, action: AgentAction) -> bool:
        """Determine if an action requires human approval"""

        # Explicit approval required
        if action.requires_approval:
            return True

        # Risk level check
        if action.risk_level not in self.config.auto_approve_risk_levels:
            return True

        # Cost threshold
        cost = action.estimated_impact.get("cost_usd", 0)
        if cost > self.config.require_human_approval_above:
            return True

        return False

    async def _request_approval(self, action: AgentAction):
        """Request approval for an action"""

        logger.info(f"Requesting approval for action {action.action_id}: {action.description}")

        # Notify approval callbacks
        for callback in self._approval_callbacks:
            try:
                await callback(action)
            except Exception as e:
                logger.error(f"Approval callback error: {e}")

    async def approve_action(self, action_id: str) -> ActionResult:
        """Approve and execute a pending action"""

        if action_id not in self.pending_actions:
            return ActionResult(
                action_id=action_id,
                status=ActionStatus.FAILED,
                result=None,
                error="Action not found in pending queue"
            )

        action = self.pending_actions.pop(action_id)
        return await self._execute_single_action(action)

    async def reject_action(self, action_id: str, reason: str) -> bool:
        """Reject a pending action"""

        if action_id in self.pending_actions:
            action = self.pending_actions.pop(action_id)
            logger.info(f"Action {action_id} rejected: {reason}")
            return True
        return False

    async def _execute_actions(
        self,
        actions: List[AgentAction]
    ) -> List[ActionResult]:
        """Execute a list of actions in order"""

        results = []

        for action in actions:
            # Check dependencies
            for dep_id in action.dependencies:
                dep_results = [r for r in results if r.action_id == dep_id]
                if not dep_results or dep_results[0].status != ActionStatus.COMPLETED:
                    results.append(ActionResult(
                        action_id=action.action_id,
                        status=ActionStatus.FAILED,
                        result=None,
                        error=f"Dependency {dep_id} not completed"
                    ))
                    continue

            # Execute action
            result = await self._execute_single_action(action)
            results.append(result)

            # Stop on failure (configurable)
            if result.status == ActionStatus.FAILED:
                logger.error(f"Action {action.action_id} failed: {result.error}")
                break

        return results

    async def _execute_single_action(
        self,
        action: AgentAction
    ) -> ActionResult:
        """Execute a single action with safety controls"""

        async with self._execution_lock:
            start_time = datetime.now()

            # Check if dry run
            if self.config.dry_run:
                logger.info(f"[DRY RUN] Would execute: {action.description}")
                return ActionResult(
                    action_id=action.action_id,
                    status=ActionStatus.COMPLETED,
                    result={"dry_run": True, "action": action.description},
                    execution_time_ms=0
                )

            try:
                # Execute with timeout
                result = await asyncio.wait_for(
                    self.execute_action(action),
                    timeout=self.config.action_timeout_seconds
                )

                # Update counters
                self.daily_action_count += 1
                cost = action.estimated_impact.get("cost_usd", 0)
                self.daily_spend += cost

                # Log to history
                self.action_history.append(result)

                execution_time = int(
                    (datetime.now() - start_time).total_seconds() * 1000
                )
                result.execution_time_ms = execution_time

                logger.info(
                    f"Action {action.action_id} completed in {execution_time}ms"
                )

                return result

            except asyncio.TimeoutError:
                return ActionResult(
                    action_id=action.action_id,
                    status=ActionStatus.FAILED,
                    result=None,
                    error=f"Action timed out after {self.config.action_timeout_seconds}s"
                )
            except Exception as e:
                logger.error(f"Action execution error: {e}")
                return ActionResult(
                    action_id=action.action_id,
                    status=ActionStatus.FAILED,
                    result=None,
                    error=str(e)
                )

    def _generate_summary(self, results: List[ActionResult]) -> Dict[str, Any]:
        """Generate execution summary"""

        completed = len([r for r in results if r.status == ActionStatus.COMPLETED])
        failed = len([r for r in results if r.status == ActionStatus.FAILED])
        total_time = sum(r.execution_time_ms for r in results)

        return {
            "total_actions": len(results),
            "completed": completed,
            "failed": failed,
            "success_rate": completed / len(results) if results else 0,
            "total_execution_time_ms": total_time,
            "daily_spend": self.daily_spend,
            "daily_action_count": self.daily_action_count
        }

    def register_approval_callback(self, callback: Callable):
        """Register a callback for approval requests"""
        self._approval_callbacks.append(callback)

    def get_action_history(
        self,
        limit: int = 100,
        status_filter: Optional[ActionStatus] = None
    ) -> List[ActionResult]:
        """Get action history with optional filtering"""

        history = self.action_history

        if status_filter:
            history = [a for a in history if a.status == status_filter]

        return history[-limit:]

    def reset_daily_limits(self):
        """Reset daily counters (call at midnight)"""
        self.daily_spend = 0.0
        self.daily_action_count = 0
        logger.info(f"Agent {self.config.name} daily limits reset")

    @staticmethod
    def create_action_id() -> str:
        """Generate a unique action ID"""
        return f"action_{uuid.uuid4().hex[:12]}"
