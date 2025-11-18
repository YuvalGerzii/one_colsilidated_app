"""
Distributed coordination for multi-agent systems.

Features:
- Peer-to-peer task allocation
- Leader election (Bully algorithm, Raft-inspired)
- Distributed consensus
- Load balancing
- Fault tolerance
"""

import asyncio
from typing import Any, Dict, List, Optional, Set, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
from loguru import logger
import uuid
import random


class AgentRole(Enum):
    """Roles in distributed coordination."""
    FOLLOWER = "follower"
    CANDIDATE = "candidate"
    LEADER = "leader"


class CoordinationStrategy(Enum):
    """Strategies for task allocation."""
    ROUND_ROBIN = "round_robin"
    LOAD_BASED = "load_based"
    CAPABILITY_BASED = "capability_based"
    AUCTION_BASED = "auction_based"


@dataclass
class CoordinationState:
    """State of an agent in the coordination system."""
    agent_id: str
    role: AgentRole = AgentRole.FOLLOWER
    current_leader: Optional[str] = None
    term: int = 0  # Election term
    voted_for: Optional[str] = None
    last_heartbeat: datetime = field(default_factory=datetime.now)
    is_alive: bool = True
    workload: int = 0  # Current number of tasks
    capabilities: Set[str] = field(default_factory=set)
    priority: int = 0  # For leader election (higher is better)


class DistributedCoordinator:
    """
    Distributed coordination system for agents.

    Implements distributed algorithms for:
    - Leader election without central authority
    - Peer-to-peer task allocation
    - Consensus building
    - Fault tolerance and recovery
    """

    def __init__(
        self,
        election_timeout: float = 5.0,
        heartbeat_interval: float = 1.0,
        strategy: CoordinationStrategy = CoordinationStrategy.CAPABILITY_BASED
    ):
        """
        Initialize the distributed coordinator.

        Args:
            election_timeout: Time before starting new election
            heartbeat_interval: Interval for leader heartbeats
            strategy: Task allocation strategy
        """
        self.election_timeout = election_timeout
        self.heartbeat_interval = heartbeat_interval
        self.strategy = strategy

        # Agent states
        self.agents: Dict[str, CoordinationState] = {}

        # Task queue
        self.pending_tasks: List[Dict[str, Any]] = []

        # Coordination metrics
        self.metrics = {
            "total_elections": 0,
            "total_tasks_allocated": 0,
            "leader_changes": 0,
            "failed_agents": 0,
        }

        # Running flag
        self.running = False

        # Round-robin counter
        self._round_robin_index = 0

        logger.info(f"DistributedCoordinator initialized (strategy={strategy.value})")

    async def start(self) -> None:
        """Start the distributed coordinator."""
        self.running = True

        # Start background tasks
        asyncio.create_task(self._monitor_heartbeats())
        asyncio.create_task(self._process_task_queue())

        logger.info("DistributedCoordinator started")

    async def stop(self) -> None:
        """Stop the distributed coordinator."""
        self.running = False
        logger.info("DistributedCoordinator stopped")

    def register_agent(
        self,
        agent_id: str,
        capabilities: Set[str],
        priority: int = 0
    ) -> None:
        """
        Register an agent for distributed coordination.

        Args:
            agent_id: ID of the agent
            capabilities: Set of agent capabilities
            priority: Priority for leader election
        """
        state = CoordinationState(
            agent_id=agent_id,
            capabilities=capabilities,
            priority=priority
        )

        self.agents[agent_id] = state

        logger.info(f"Agent {agent_id} registered for coordination (priority={priority})")

        # If no leader exists, trigger election
        if not self._get_current_leader():
            asyncio.create_task(self._trigger_election())

    def unregister_agent(self, agent_id: str) -> None:
        """
        Unregister an agent.

        Args:
            agent_id: ID of the agent
        """
        if agent_id in self.agents:
            state = self.agents[agent_id]
            state.is_alive = False

            # If this was the leader, trigger new election
            if state.role == AgentRole.LEADER:
                logger.warning(f"Leader {agent_id} unregistered, triggering election")
                asyncio.create_task(self._trigger_election())

            del self.agents[agent_id]
            self.metrics["failed_agents"] += 1

            logger.info(f"Agent {agent_id} unregistered from coordination")

    async def submit_task(
        self,
        task: Dict[str, Any],
        required_capabilities: Optional[Set[str]] = None
    ) -> Optional[str]:
        """
        Submit a task for distributed allocation.

        Args:
            task: Task to allocate
            required_capabilities: Required capabilities for the task

        Returns:
            ID of agent assigned to task, or None if no suitable agent
        """
        task_info = {
            "id": task.get("id", str(uuid.uuid4())),
            "task": task,
            "required_capabilities": required_capabilities or set(),
            "submitted_at": datetime.now(),
        }

        # Try immediate allocation
        assigned_agent = await self._allocate_task(task_info)

        if assigned_agent:
            self.metrics["total_tasks_allocated"] += 1
            logger.info(f"Task {task_info['id']} allocated to {assigned_agent}")
            return assigned_agent
        else:
            # Queue for later
            self.pending_tasks.append(task_info)
            logger.info(f"Task {task_info['id']} queued (no suitable agent available)")
            return None

    async def _allocate_task(self, task_info: Dict[str, Any]) -> Optional[str]:
        """
        Allocate a task to an agent based on strategy.

        Args:
            task_info: Task information

        Returns:
            ID of assigned agent, or None
        """
        required_caps = task_info["required_capabilities"]

        # Filter capable agents
        capable_agents = [
            agent_id
            for agent_id, state in self.agents.items()
            if state.is_alive and required_caps.issubset(state.capabilities)
        ]

        if not capable_agents:
            return None

        # Apply allocation strategy
        if self.strategy == CoordinationStrategy.ROUND_ROBIN:
            assigned = capable_agents[self._round_robin_index % len(capable_agents)]
            self._round_robin_index += 1
            self.agents[assigned].workload += 1
            return assigned

        elif self.strategy == CoordinationStrategy.LOAD_BASED:
            # Assign to agent with lowest workload
            assigned = min(
                capable_agents,
                key=lambda aid: self.agents[aid].workload
            )
            self.agents[assigned].workload += 1
            return assigned

        elif self.strategy == CoordinationStrategy.CAPABILITY_BASED:
            # Assign to most capable agent (most capabilities)
            assigned = max(
                capable_agents,
                key=lambda aid: len(self.agents[aid].capabilities)
            )
            self.agents[assigned].workload += 1
            return assigned

        elif self.strategy == CoordinationStrategy.AUCTION_BASED:
            # Simple auction: agent with lowest workload "bids" lowest
            assigned = min(
                capable_agents,
                key=lambda aid: self.agents[aid].workload
            )
            self.agents[assigned].workload += 1
            return assigned

        return None

    async def _trigger_election(self) -> None:
        """Trigger a leader election (Bully algorithm variant)."""
        if not self.agents:
            return

        self.metrics["total_elections"] += 1

        logger.info("Starting leader election...")

        # Reset all agents to follower
        for state in self.agents.values():
            if state.role == AgentRole.LEADER:
                logger.info(f"Demoting current leader {state.agent_id}")
            state.role = AgentRole.FOLLOWER
            state.voted_for = None

        # Increment term
        current_term = max(
            (state.term for state in self.agents.values()),
            default=0
        ) + 1

        for state in self.agents.values():
            state.term = current_term

        # Bully algorithm: agent with highest priority becomes leader
        # In case of tie, use agent_id as tiebreaker
        candidates = [
            (state.priority, state.agent_id)
            for state in self.agents.values()
            if state.is_alive
        ]

        if not candidates:
            logger.warning("No alive agents for election")
            return

        # Sort by priority (descending), then by agent_id
        candidates.sort(reverse=True)
        winner_priority, winner_id = candidates[0]

        # Set the leader
        if winner_id in self.agents:
            self.agents[winner_id].role = AgentRole.LEADER
            self.agents[winner_id].current_leader = winner_id

            # Update all other agents
            for agent_id, state in self.agents.items():
                if agent_id != winner_id:
                    state.current_leader = winner_id

            self.metrics["leader_changes"] += 1

            logger.info(
                f"Election complete: {winner_id} elected as leader "
                f"(term={current_term}, priority={winner_priority})"
            )

            # Start sending heartbeats
            asyncio.create_task(self._send_heartbeats(winner_id))

    async def _send_heartbeats(self, leader_id: str) -> None:
        """
        Send periodic heartbeats from the leader.

        Args:
            leader_id: ID of the leader
        """
        while self.running and leader_id in self.agents:
            state = self.agents[leader_id]

            # Check if still leader
            if state.role != AgentRole.LEADER:
                break

            # Update heartbeat timestamp
            state.last_heartbeat = datetime.now()

            # Send heartbeat to all followers (in real system, would use message bus)
            for agent_id, agent_state in self.agents.items():
                if agent_id != leader_id and agent_state.is_alive:
                    agent_state.last_heartbeat = datetime.now()
                    agent_state.current_leader = leader_id

            await asyncio.sleep(self.heartbeat_interval)

    async def _monitor_heartbeats(self) -> None:
        """Monitor heartbeats and detect leader failures."""
        while self.running:
            await asyncio.sleep(self.heartbeat_interval)

            current_leader = self._get_current_leader()

            if current_leader:
                leader_state = self.agents[current_leader]
                time_since_heartbeat = (
                    datetime.now() - leader_state.last_heartbeat
                ).total_seconds()

                # Check if leader has timed out
                if time_since_heartbeat > self.election_timeout:
                    logger.warning(
                        f"Leader {current_leader} heartbeat timeout "
                        f"({time_since_heartbeat:.1f}s), triggering election"
                    )
                    await self._trigger_election()

            else:
                # No leader, trigger election
                if self.agents:  # Only if there are agents
                    logger.info("No leader detected, triggering election")
                    await self._trigger_election()

    async def _process_task_queue(self) -> None:
        """Process pending tasks."""
        while self.running:
            await asyncio.sleep(0.5)

            if not self.pending_tasks:
                continue

            # Try to allocate pending tasks
            allocated_tasks = []

            for task_info in self.pending_tasks:
                assigned = await self._allocate_task(task_info)

                if assigned:
                    self.metrics["total_tasks_allocated"] += 1
                    logger.info(f"Queued task {task_info['id']} allocated to {assigned}")
                    allocated_tasks.append(task_info)

            # Remove allocated tasks from queue
            for task_info in allocated_tasks:
                self.pending_tasks.remove(task_info)

    def _get_current_leader(self) -> Optional[str]:
        """Get the current leader agent ID."""
        for agent_id, state in self.agents.items():
            if state.role == AgentRole.LEADER and state.is_alive:
                return agent_id
        return None

    def get_leader(self) -> Optional[str]:
        """Get the current leader (public method)."""
        return self._get_current_leader()

    def report_task_completed(self, agent_id: str) -> None:
        """
        Report that an agent completed a task.

        Args:
            agent_id: ID of the agent
        """
        if agent_id in self.agents:
            self.agents[agent_id].workload = max(0, self.agents[agent_id].workload - 1)

    def get_coordination_state(self) -> Dict[str, Any]:
        """Get the current coordination state."""
        leader = self._get_current_leader()

        return {
            "current_leader": leader,
            "total_agents": len(self.agents),
            "alive_agents": sum(1 for s in self.agents.values() if s.is_alive),
            "pending_tasks": len(self.pending_tasks),
            "strategy": self.strategy.value,
            "metrics": self.metrics,
            "agents": [
                {
                    "id": agent_id,
                    "role": state.role.value,
                    "workload": state.workload,
                    "is_alive": state.is_alive,
                    "priority": state.priority,
                    "capabilities": list(state.capabilities),
                }
                for agent_id, state in self.agents.items()
            ]
        }

    def get_agent_state(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get state of a specific agent."""
        if agent_id not in self.agents:
            return None

        state = self.agents[agent_id]

        return {
            "id": agent_id,
            "role": state.role.value,
            "current_leader": state.current_leader,
            "term": state.term,
            "workload": state.workload,
            "is_alive": state.is_alive,
            "priority": state.priority,
            "capabilities": list(state.capabilities),
            "last_heartbeat": state.last_heartbeat.isoformat(),
        }
