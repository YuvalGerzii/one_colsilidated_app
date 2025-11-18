"""
Shared environment for multi-agent interaction.

The shared environment allows agents to:
- Share resources and information
- Interact with common objects
- Compete for resources
- Collaborate on shared goals
- Observe each other's actions
"""

import asyncio
from typing import Any, Dict, List, Optional, Set, Callable
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
from loguru import logger
import uuid


class ResourceType(Enum):
    """Types of resources in the environment."""
    COMPUTATIONAL = "computational"
    DATA = "data"
    KNOWLEDGE = "knowledge"
    TOOL = "tool"
    MEMORY = "memory"


class AccessMode(Enum):
    """Resource access modes."""
    SHARED = "shared"  # Multiple agents can access simultaneously
    EXCLUSIVE = "exclusive"  # Only one agent at a time
    READ_ONLY = "read_only"  # Read-only access


@dataclass
class Resource:
    """A resource in the shared environment."""
    id: str
    name: str
    resource_type: ResourceType
    access_mode: AccessMode
    capacity: int = 1  # How many agents can use it simultaneously
    data: Any = None
    owner: Optional[str] = None  # Agent that created/owns the resource
    current_users: Set[str] = field(default_factory=set)
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EnvironmentEvent:
    """An event in the environment that agents can observe."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str = ""
    source_agent: Optional[str] = None
    target_agent: Optional[str] = None
    resource_id: Optional[str] = None
    data: Any = None
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


class SharedEnvironment:
    """
    Shared environment where agents can interact.

    Features:
    - Resource management (create, access, release)
    - Event broadcasting (agents can observe environment changes)
    - State sharing (common knowledge base)
    - Competition mechanisms (resource contention)
    - Collaboration support (shared workspaces)
    """

    def __init__(self, name: str = "default"):
        """
        Initialize the shared environment.

        Args:
            name: Name of the environment
        """
        self.name = name

        # Resources in the environment
        self.resources: Dict[str, Resource] = {}

        # Shared state/knowledge base
        self.shared_state: Dict[str, Any] = {}

        # Event history
        self.events: List[EnvironmentEvent] = []
        self.max_events = 10000

        # Agent registry
        self.registered_agents: Set[str] = set()

        # Event subscribers: event_type -> set of agent_ids
        self.event_subscribers: Dict[str, Set[str]] = {}

        # Locks for resource access
        self.resource_locks: Dict[str, asyncio.Lock] = {}

        # Environment statistics
        self.stats = {
            "total_resources_created": 0,
            "total_resource_accesses": 0,
            "total_events": 0,
            "total_conflicts": 0,
        }

        logger.info(f"SharedEnvironment '{name}' initialized")

    def register_agent(self, agent_id: str) -> None:
        """
        Register an agent with the environment.

        Args:
            agent_id: ID of the agent to register
        """
        self.registered_agents.add(agent_id)
        logger.info(f"Agent {agent_id} registered with environment '{self.name}'")

        # Emit event
        event = EnvironmentEvent(
            event_type="agent_joined",
            source_agent=agent_id,
            data={"agent_id": agent_id}
        )
        self._emit_event(event)

    def unregister_agent(self, agent_id: str) -> None:
        """
        Unregister an agent from the environment.

        Args:
            agent_id: ID of the agent to unregister
        """
        self.registered_agents.discard(agent_id)

        # Release all resources held by this agent
        for resource in self.resources.values():
            resource.current_users.discard(agent_id)

        # Remove from event subscriptions
        for subscribers in self.event_subscribers.values():
            subscribers.discard(agent_id)

        logger.info(f"Agent {agent_id} unregistered from environment '{self.name}'")

        # Emit event
        event = EnvironmentEvent(
            event_type="agent_left",
            source_agent=agent_id,
            data={"agent_id": agent_id}
        )
        self._emit_event(event)

    async def create_resource(
        self,
        name: str,
        resource_type: ResourceType,
        access_mode: AccessMode,
        data: Any = None,
        owner: Optional[str] = None,
        capacity: int = 1,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Create a new resource in the environment.

        Args:
            name: Name of the resource
            resource_type: Type of resource
            access_mode: How the resource can be accessed
            data: Initial data for the resource
            owner: Agent that owns the resource
            capacity: How many agents can use it simultaneously
            metadata: Additional metadata

        Returns:
            Resource ID
        """
        resource_id = str(uuid.uuid4())

        resource = Resource(
            id=resource_id,
            name=name,
            resource_type=resource_type,
            access_mode=access_mode,
            capacity=capacity,
            data=data,
            owner=owner,
            metadata=metadata or {}
        )

        self.resources[resource_id] = resource
        self.resource_locks[resource_id] = asyncio.Lock()
        self.stats["total_resources_created"] += 1

        logger.info(f"Resource '{name}' created by {owner} (type={resource_type.value}, mode={access_mode.value})")

        # Emit event
        event = EnvironmentEvent(
            event_type="resource_created",
            source_agent=owner,
            resource_id=resource_id,
            data={
                "name": name,
                "type": resource_type.value,
                "access_mode": access_mode.value
            }
        )
        self._emit_event(event)

        return resource_id

    async def request_resource(
        self,
        resource_id: str,
        agent_id: str,
        timeout: float = 10.0
    ) -> bool:
        """
        Request access to a resource.

        Args:
            resource_id: ID of the resource
            agent_id: ID of the requesting agent
            timeout: Maximum time to wait for access

        Returns:
            True if access was granted, False otherwise
        """
        if resource_id not in self.resources:
            logger.warning(f"Resource {resource_id} not found")
            return False

        resource = self.resources[resource_id]

        # Check if agent is registered
        if agent_id not in self.registered_agents:
            logger.warning(f"Agent {agent_id} not registered in environment")
            return False

        # Handle different access modes
        if resource.access_mode == AccessMode.READ_ONLY:
            # Read-only resources are always accessible
            resource.current_users.add(agent_id)
            self.stats["total_resource_accesses"] += 1

            event = EnvironmentEvent(
                event_type="resource_accessed",
                source_agent=agent_id,
                resource_id=resource_id,
                data={"access_mode": "read_only"}
            )
            self._emit_event(event)

            return True

        elif resource.access_mode == AccessMode.SHARED:
            # Shared resources can be accessed up to capacity
            if len(resource.current_users) < resource.capacity:
                resource.current_users.add(agent_id)
                self.stats["total_resource_accesses"] += 1

                event = EnvironmentEvent(
                    event_type="resource_accessed",
                    source_agent=agent_id,
                    resource_id=resource_id,
                    data={"access_mode": "shared", "current_users": len(resource.current_users)}
                )
                self._emit_event(event)

                return True
            else:
                # Resource at capacity, need to wait
                logger.info(f"Resource {resource.name} at capacity, agent {agent_id} waiting...")
                self.stats["total_conflicts"] += 1

                # Try to acquire with timeout
                try:
                    async with asyncio.timeout(timeout):
                        while len(resource.current_users) >= resource.capacity:
                            await asyncio.sleep(0.1)

                        resource.current_users.add(agent_id)
                        self.stats["total_resource_accesses"] += 1
                        return True
                except asyncio.TimeoutError:
                    logger.warning(f"Agent {agent_id} timed out waiting for resource {resource.name}")
                    return False

        elif resource.access_mode == AccessMode.EXCLUSIVE:
            # Exclusive access requires a lock
            lock = self.resource_locks[resource_id]

            try:
                async with asyncio.timeout(timeout):
                    acquired = await lock.acquire()
                    if acquired:
                        resource.current_users.add(agent_id)
                        self.stats["total_resource_accesses"] += 1

                        event = EnvironmentEvent(
                            event_type="resource_accessed",
                            source_agent=agent_id,
                            resource_id=resource_id,
                            data={"access_mode": "exclusive"}
                        )
                        self._emit_event(event)

                        return True
            except asyncio.TimeoutError:
                logger.warning(f"Agent {agent_id} timed out waiting for exclusive access to {resource.name}")
                self.stats["total_conflicts"] += 1
                return False

        return False

    async def release_resource(
        self,
        resource_id: str,
        agent_id: str
    ) -> bool:
        """
        Release a resource.

        Args:
            resource_id: ID of the resource
            agent_id: ID of the agent releasing it

        Returns:
            True if successfully released
        """
        if resource_id not in self.resources:
            logger.warning(f"Resource {resource_id} not found")
            return False

        resource = self.resources[resource_id]

        if agent_id not in resource.current_users:
            logger.warning(f"Agent {agent_id} is not using resource {resource.name}")
            return False

        resource.current_users.discard(agent_id)

        # Release lock for exclusive resources
        if resource.access_mode == AccessMode.EXCLUSIVE:
            lock = self.resource_locks[resource_id]
            if lock.locked():
                lock.release()

        logger.debug(f"Agent {agent_id} released resource {resource.name}")

        # Emit event
        event = EnvironmentEvent(
            event_type="resource_released",
            source_agent=agent_id,
            resource_id=resource_id,
            data={"remaining_users": len(resource.current_users)}
        )
        self._emit_event(event)

        return True

    def get_resource(self, resource_id: str) -> Optional[Resource]:
        """Get a resource by ID."""
        return self.resources.get(resource_id)

    def get_resource_data(self, resource_id: str) -> Optional[Any]:
        """Get the data from a resource."""
        resource = self.resources.get(resource_id)
        return resource.data if resource else None

    def update_resource_data(
        self,
        resource_id: str,
        data: Any,
        agent_id: str
    ) -> bool:
        """
        Update resource data.

        Args:
            resource_id: ID of the resource
            data: New data
            agent_id: Agent updating the data

        Returns:
            True if updated successfully
        """
        if resource_id not in self.resources:
            return False

        resource = self.resources[resource_id]

        # Check if agent has access
        if agent_id not in resource.current_users and resource.access_mode != AccessMode.READ_ONLY:
            logger.warning(f"Agent {agent_id} doesn't have access to resource {resource.name}")
            return False

        resource.data = data

        # Emit event
        event = EnvironmentEvent(
            event_type="resource_updated",
            source_agent=agent_id,
            resource_id=resource_id,
            data={"size": len(str(data)) if data else 0}
        )
        self._emit_event(event)

        return True

    def set_shared_state(self, key: str, value: Any, agent_id: str) -> None:
        """
        Set a value in the shared state.

        Args:
            key: State key
            value: State value
            agent_id: Agent setting the state
        """
        self.shared_state[key] = value

        # Emit event
        event = EnvironmentEvent(
            event_type="state_updated",
            source_agent=agent_id,
            data={"key": key, "value_type": type(value).__name__}
        )
        self._emit_event(event)

    def get_shared_state(self, key: str) -> Optional[Any]:
        """Get a value from the shared state."""
        return self.shared_state.get(key)

    def subscribe_to_events(self, agent_id: str, event_type: str) -> None:
        """
        Subscribe an agent to specific events.

        Args:
            agent_id: ID of the agent
            event_type: Type of event to subscribe to
        """
        if event_type not in self.event_subscribers:
            self.event_subscribers[event_type] = set()

        self.event_subscribers[event_type].add(agent_id)
        logger.debug(f"Agent {agent_id} subscribed to events of type '{event_type}'")

    def unsubscribe_from_events(self, agent_id: str, event_type: str) -> None:
        """
        Unsubscribe an agent from events.

        Args:
            agent_id: ID of the agent
            event_type: Type of event to unsubscribe from
        """
        if event_type in self.event_subscribers:
            self.event_subscribers[event_type].discard(agent_id)

    def _emit_event(self, event: EnvironmentEvent) -> None:
        """
        Emit an event to the environment.

        Args:
            event: The event to emit
        """
        self.events.append(event)
        self.stats["total_events"] += 1

        # Trim event history if needed
        if len(self.events) > self.max_events:
            self.events = self.events[-self.max_events:]

        logger.debug(f"Event emitted: {event.event_type} from {event.source_agent}")

    def get_events(
        self,
        agent_id: Optional[str] = None,
        event_type: Optional[str] = None,
        limit: int = 100
    ) -> List[EnvironmentEvent]:
        """
        Get events from the environment.

        Args:
            agent_id: Filter by agent
            event_type: Filter by event type
            limit: Maximum number of events to return

        Returns:
            List of events
        """
        filtered = self.events

        if agent_id:
            filtered = [e for e in filtered if e.source_agent == agent_id or e.target_agent == agent_id]

        if event_type:
            filtered = [e for e in filtered if e.event_type == event_type]

        return filtered[-limit:]

    def get_environment_state(self) -> Dict[str, Any]:
        """Get the current state of the environment."""
        return {
            "name": self.name,
            "registered_agents": len(self.registered_agents),
            "total_resources": len(self.resources),
            "resources_in_use": sum(1 for r in self.resources.values() if r.current_users),
            "shared_state_keys": len(self.shared_state),
            "total_events": len(self.events),
            "statistics": self.stats,
            "resources": [
                {
                    "id": r.id,
                    "name": r.name,
                    "type": r.resource_type.value,
                    "access_mode": r.access_mode.value,
                    "current_users": len(r.current_users),
                    "capacity": r.capacity,
                    "owner": r.owner
                }
                for r in self.resources.values()
            ]
        }

    def list_resources(
        self,
        resource_type: Optional[ResourceType] = None,
        available_only: bool = False
    ) -> List[Dict[str, Any]]:
        """
        List resources in the environment.

        Args:
            resource_type: Filter by resource type
            available_only: Only show available resources

        Returns:
            List of resource information
        """
        resources = self.resources.values()

        if resource_type:
            resources = [r for r in resources if r.resource_type == resource_type]

        if available_only:
            resources = [r for r in resources if len(r.current_users) < r.capacity]

        return [
            {
                "id": r.id,
                "name": r.name,
                "type": r.resource_type.value,
                "access_mode": r.access_mode.value,
                "current_users": len(r.current_users),
                "capacity": r.capacity,
                "available": len(r.current_users) < r.capacity,
                "owner": r.owner
            }
            for r in resources
        ]
