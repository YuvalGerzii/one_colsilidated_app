"""
Message bus for agent communication.

Implements an asynchronous, event-driven message passing system for agents.
"""

import asyncio
from collections import defaultdict, deque
from typing import Callable, Dict, List, Optional, Set
from datetime import datetime, timedelta
from loguru import logger

from app.multi_agent_system.core.types import Message, MessageType


class MessageBus:
    """
    Asynchronous message bus for agent communication.

    Supports:
    - Direct messaging (point-to-point)
    - Broadcasting (one-to-many)
    - Priority queues
    - Message history
    - Pub/Sub pattern
    """

    def __init__(self, max_queue_size: int = 1000, history_size: int = 10000):
        """
        Initialize the message bus.

        Args:
            max_queue_size: Maximum size of each agent's message queue
            history_size: Maximum number of messages to keep in history
        """
        self.max_queue_size = max_queue_size
        self.history_size = history_size

        # Agent message queues: agent_id -> priority queue
        self.queues: Dict[str, asyncio.PriorityQueue] = {}

        # Subscribers for pub/sub: topic -> set of agent_ids
        self.subscribers: Dict[str, Set[str]] = defaultdict(set)

        # Message history for debugging/learning
        self.history: deque = deque(maxlen=history_size)

        # Pending responses: message_id -> future
        self.pending_responses: Dict[str, asyncio.Future] = {}

        # Statistics
        self.stats = {
            "total_messages": 0,
            "broadcasts": 0,
            "direct_messages": 0,
            "dropped_messages": 0,
        }

        logger.info("MessageBus initialized")

    def register_agent(self, agent_id: str) -> None:
        """
        Register an agent with the message bus.

        Args:
            agent_id: Unique identifier for the agent
        """
        if agent_id not in self.queues:
            self.queues[agent_id] = asyncio.PriorityQueue(maxsize=self.max_queue_size)
            logger.debug(f"Agent {agent_id} registered with message bus")

    def unregister_agent(self, agent_id: str) -> None:
        """
        Unregister an agent from the message bus.

        Args:
            agent_id: Unique identifier for the agent
        """
        if agent_id in self.queues:
            del self.queues[agent_id]
            # Remove from all subscriptions
            for topic_subscribers in self.subscribers.values():
                topic_subscribers.discard(agent_id)
            logger.debug(f"Agent {agent_id} unregistered from message bus")

    async def send_message(self, message: Message) -> bool:
        """
        Send a message to one or more agents.

        Args:
            message: The message to send

        Returns:
            True if message was successfully queued, False otherwise
        """
        self.stats["total_messages"] += 1
        self.history.append(message)

        # Check if message has expired
        if self._is_expired(message):
            logger.warning(f"Message {message.id} expired before delivery")
            return False

        # Broadcast message
        if not message.recipient or message.recipient == "*":
            return await self._broadcast_message(message)

        # Direct message
        return await self._send_direct_message(message)

    async def _send_direct_message(self, message: Message) -> bool:
        """Send a message to a specific agent."""
        self.stats["direct_messages"] += 1

        if message.recipient not in self.queues:
            logger.warning(f"Recipient {message.recipient} not registered")
            self.stats["dropped_messages"] += 1
            return False

        try:
            # Use negative priority for higher priority messages (min heap)
            priority = -message.priority
            await asyncio.wait_for(
                self.queues[message.recipient].put((priority, message)),
                timeout=1.0,
            )
            logger.debug(f"Message {message.id} sent to {message.recipient}")
            return True
        except asyncio.TimeoutError:
            logger.warning(f"Queue full for agent {message.recipient}")
            self.stats["dropped_messages"] += 1
            return False

    async def _broadcast_message(self, message: Message) -> bool:
        """Broadcast a message to all registered agents."""
        self.stats["broadcasts"] += 1

        sent_count = 0
        for agent_id in self.queues.keys():
            if agent_id != message.sender:  # Don't send to self
                msg_copy = Message(
                    sender=message.sender,
                    recipient=agent_id,
                    message_type=message.message_type,
                    content=message.content,
                    priority=message.priority,
                    metadata=message.metadata,
                )
                if await self._send_direct_message(msg_copy):
                    sent_count += 1

        logger.debug(f"Broadcast message {message.id} sent to {sent_count} agents")
        return sent_count > 0

    async def receive_message(
        self, agent_id: str, timeout: Optional[float] = None
    ) -> Optional[Message]:
        """
        Receive a message for an agent.

        Args:
            agent_id: ID of the agent receiving the message
            timeout: Maximum time to wait for a message (None = wait forever)

        Returns:
            The received message, or None if timeout occurred
        """
        if agent_id not in self.queues:
            logger.warning(f"Agent {agent_id} not registered")
            return None

        try:
            if timeout:
                priority, message = await asyncio.wait_for(
                    self.queues[agent_id].get(), timeout=timeout
                )
            else:
                priority, message = await self.queues[agent_id].get()

            # Check if message has expired
            if self._is_expired(message):
                logger.debug(f"Expired message {message.id} discarded")
                return await self.receive_message(agent_id, timeout)

            logger.debug(f"Agent {agent_id} received message {message.id}")
            return message

        except asyncio.TimeoutError:
            return None

    async def send_and_wait_response(
        self, message: Message, timeout: float = 30.0
    ) -> Optional[Message]:
        """
        Send a message and wait for a response.

        Args:
            message: The message to send
            timeout: Maximum time to wait for response

        Returns:
            The response message, or None if timeout occurred
        """
        message.requires_response = True

        # Create a future for the response
        response_future = asyncio.Future()
        self.pending_responses[message.id] = response_future

        # Send the message
        if not await self.send_message(message):
            del self.pending_responses[message.id]
            return None

        try:
            # Wait for the response
            response = await asyncio.wait_for(response_future, timeout=timeout)
            return response
        except asyncio.TimeoutError:
            logger.warning(f"Timeout waiting for response to message {message.id}")
            del self.pending_responses[message.id]
            return None

    async def send_response(self, original_message_id: str, response: Message) -> bool:
        """
        Send a response to a message.

        Args:
            original_message_id: ID of the message being responded to
            response: The response message

        Returns:
            True if response was delivered
        """
        response.in_response_to = original_message_id

        # If there's a pending future, resolve it
        if original_message_id in self.pending_responses:
            future = self.pending_responses.pop(original_message_id)
            if not future.done():
                future.set_result(response)
            return True

        # Otherwise, send as a normal message
        return await self.send_message(response)

    def subscribe(self, agent_id: str, topic: str) -> None:
        """
        Subscribe an agent to a topic.

        Args:
            agent_id: ID of the subscribing agent
            topic: Topic to subscribe to
        """
        self.subscribers[topic].add(agent_id)
        logger.debug(f"Agent {agent_id} subscribed to topic '{topic}'")

    def unsubscribe(self, agent_id: str, topic: str) -> None:
        """
        Unsubscribe an agent from a topic.

        Args:
            agent_id: ID of the agent
            topic: Topic to unsubscribe from
        """
        self.subscribers[topic].discard(agent_id)
        logger.debug(f"Agent {agent_id} unsubscribed from topic '{topic}'")

    async def publish(self, topic: str, message: Message) -> int:
        """
        Publish a message to a topic.

        Args:
            topic: The topic to publish to
            message: The message to publish

        Returns:
            Number of subscribers that received the message
        """
        if topic not in self.subscribers or not self.subscribers[topic]:
            logger.debug(f"No subscribers for topic '{topic}'")
            return 0

        sent_count = 0
        for agent_id in self.subscribers[topic]:
            msg_copy = Message(
                sender=message.sender,
                recipient=agent_id,
                message_type=message.message_type,
                content=message.content,
                priority=message.priority,
                metadata={**message.metadata, "topic": topic},
            )
            if await self._send_direct_message(msg_copy):
                sent_count += 1

        logger.debug(f"Published message to topic '{topic}': {sent_count} recipients")
        return sent_count

    def get_message_history(
        self, agent_id: Optional[str] = None, limit: int = 100
    ) -> List[Message]:
        """
        Get message history.

        Args:
            agent_id: Filter by agent ID (sender or recipient)
            limit: Maximum number of messages to return

        Returns:
            List of messages
        """
        if agent_id:
            filtered = [
                msg
                for msg in self.history
                if msg.sender == agent_id or msg.recipient == agent_id
            ]
            return list(filtered)[-limit:]
        return list(self.history)[-limit:]

    def get_statistics(self) -> Dict:
        """Get message bus statistics."""
        return {
            **self.stats,
            "registered_agents": len(self.queues),
            "total_topics": len(self.subscribers),
            "history_size": len(self.history),
            "pending_responses": len(self.pending_responses),
        }

    def _is_expired(self, message: Message) -> bool:
        """Check if a message has expired based on TTL."""
        if message.ttl <= 0:
            return False
        age = (datetime.now() - message.timestamp).total_seconds()
        return age > message.ttl

    async def clear_expired_messages(self) -> int:
        """
        Clear expired messages from all queues.

        Returns:
            Number of messages cleared
        """
        # This is a simplified implementation
        # In production, you'd want a background task for this
        cleared = 0
        for agent_id, queue in self.queues.items():
            # Can't easily remove from asyncio.PriorityQueue
            # Would need a custom implementation for full cleanup
            pass
        return cleared
