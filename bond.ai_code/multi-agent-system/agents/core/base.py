"""
Base agent class for all agents in the system.
"""

import asyncio
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime
from loguru import logger

from multi_agent_system.core.types import (
    Task,
    Result,
    Message,
    MessageType,
    AgentCapability,
    AgentState,
    Experience,
    TaskStatus,
)
from multi_agent_system.communication.message_bus import MessageBus


class BaseAgent(ABC):
    """
    Base class for all agents in the multi-agent system.

    All agents must implement the process_task method.
    """

    def __init__(
        self,
        agent_id: str,
        capabilities: List[AgentCapability],
        message_bus: Optional[MessageBus] = None,
    ):
        """
        Initialize the agent.

        Args:
            agent_id: Unique identifier for the agent
            capabilities: List of capabilities this agent has
            message_bus: Message bus for communication
        """
        self.agent_id = agent_id
        self.capabilities = capabilities
        self.message_bus = message_bus

        # Agent state
        self.state = AgentState(
            agent_id=agent_id,
            capabilities=capabilities,
            status="idle",
        )

        # Task management
        self.current_task: Optional[Task] = None
        self.task_queue: asyncio.Queue = asyncio.Queue()

        # Learning
        self.experiences: List[Experience] = []

        # Tools (to be injected)
        self.tools: Dict[str, Any] = {}

        # Running flag
        self.running = False

        logger.info(f"Agent {agent_id} initialized with {len(capabilities)} capabilities")

    async def start(self) -> None:
        """Start the agent's main loop."""
        self.running = True

        if self.message_bus:
            self.message_bus.register_agent(self.agent_id)

        logger.info(f"Agent {self.agent_id} started")

        # Start message processing loop
        asyncio.create_task(self._message_loop())

    async def stop(self) -> None:
        """Stop the agent."""
        self.running = False

        if self.message_bus:
            self.message_bus.unregister_agent(self.agent_id)

        logger.info(f"Agent {self.agent_id} stopped")

    @abstractmethod
    async def process_task(self, task: Task) -> Result:
        """
        Process a task. Must be implemented by subclasses.

        Args:
            task: The task to process

        Returns:
            The result of processing the task
        """
        pass

    async def execute_task(self, task: Task) -> Result:
        """
        Execute a task with proper state management and learning.

        Args:
            task: The task to execute

        Returns:
            The result of the task
        """
        start_time = datetime.now()
        self.current_task = task
        self.state.status = "busy"
        self.state.current_task = task.id

        task.status = TaskStatus.IN_PROGRESS
        task.started_at = start_time
        task.assigned_to = self.agent_id

        # Capture initial state for learning
        initial_state = self._capture_state(task)

        try:
            # Process the task
            logger.info(f"Agent {self.agent_id} processing task {task.id}")
            result = await self.process_task(task)

            # Update task status
            task.status = TaskStatus.COMPLETED if result.success else TaskStatus.FAILED
            task.completed_at = datetime.now()

            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds()
            result.execution_time = execution_time
            result.agent_id = self.agent_id

            # Update agent state
            if result.success:
                self.state.completed_tasks += 1
            else:
                self.state.failed_tasks += 1

            # Update average execution time
            total_tasks = self.state.completed_tasks + self.state.failed_tasks
            self.state.average_execution_time = (
                self.state.average_execution_time * (total_tasks - 1)
                + execution_time
            ) / total_tasks

            # Capture final state and create experience for learning
            final_state = self._capture_state(task)
            reward = self._calculate_reward(result)

            experience = Experience(
                agent_id=self.agent_id,
                state=initial_state,
                action=task.description[:100],  # Truncate for storage
                reward=reward,
                next_state=final_state,
                done=True,
                metadata={
                    "task_id": task.id,
                    "execution_time": execution_time,
                    "quality_score": result.quality_score,
                },
            )
            self.experiences.append(experience)

            logger.info(
                f"Agent {self.agent_id} completed task {task.id} "
                f"(success={result.success}, time={execution_time:.2f}s, reward={reward:.2f})"
            )

            return result

        except Exception as e:
            logger.error(f"Agent {self.agent_id} error processing task {task.id}: {e}")

            task.status = TaskStatus.FAILED
            task.completed_at = datetime.now()
            self.state.failed_tasks += 1

            result = Result(
                task_id=task.id,
                success=False,
                error=str(e),
                agent_id=self.agent_id,
                execution_time=(datetime.now() - start_time).total_seconds(),
            )

            # Create negative experience
            final_state = self._capture_state(task)
            experience = Experience(
                agent_id=self.agent_id,
                state=initial_state,
                action=task.description[:100],
                reward=-0.5,  # Negative reward for failure
                next_state=final_state,
                done=True,
                metadata={"task_id": task.id, "error": str(e)},
            )
            self.experiences.append(experience)

            return result

        finally:
            self.current_task = None
            self.state.status = "idle"
            self.state.current_task = None
            self.state.last_active = datetime.now()

    async def send_message(self, message: Message) -> bool:
        """
        Send a message to another agent.

        Args:
            message: The message to send

        Returns:
            True if message was sent successfully
        """
        if not self.message_bus:
            logger.warning(f"Agent {self.agent_id} has no message bus")
            return False

        message.sender = self.agent_id
        return await self.message_bus.send_message(message)

    async def receive_message(self, timeout: Optional[float] = None) -> Optional[Message]:
        """
        Receive a message.

        Args:
            timeout: Maximum time to wait for a message

        Returns:
            The received message, or None if timeout
        """
        if not self.message_bus:
            logger.warning(f"Agent {self.agent_id} has no message bus")
            return None

        return await self.message_bus.receive_message(self.agent_id, timeout)

    async def send_and_wait_response(
        self, message: Message, timeout: float = 30.0
    ) -> Optional[Message]:
        """
        Send a message and wait for a response.

        Args:
            message: The message to send
            timeout: Maximum time to wait for response

        Returns:
            The response message, or None if timeout
        """
        if not self.message_bus:
            logger.warning(f"Agent {self.agent_id} has no message bus")
            return None

        message.sender = self.agent_id
        return await self.message_bus.send_and_wait_response(message, timeout)

    async def broadcast_message(self, content: Any, message_type: MessageType = MessageType.BROADCAST) -> bool:
        """
        Broadcast a message to all agents.

        Args:
            content: The content to broadcast
            message_type: Type of message

        Returns:
            True if broadcast was successful
        """
        message = Message(
            sender=self.agent_id,
            recipient="*",
            message_type=message_type,
            content=content,
        )
        return await self.send_message(message)

    async def _message_loop(self) -> None:
        """Background loop for processing incoming messages."""
        while self.running:
            try:
                message = await self.receive_message(timeout=1.0)
                if message:
                    await self._handle_message(message)
            except Exception as e:
                logger.error(f"Agent {self.agent_id} message loop error: {e}")

    async def _handle_message(self, message: Message) -> None:
        """
        Handle an incoming message.

        Args:
            message: The message to handle
        """
        logger.debug(f"Agent {self.agent_id} handling message {message.id} from {message.sender}")

        if message.message_type == MessageType.TASK_ASSIGNMENT:
            # Add task to queue
            task = message.content
            if isinstance(task, Task):
                await self.task_queue.put(task)

        elif message.message_type == MessageType.QUERY:
            # Handle query and send response
            response = await self._handle_query(message.content)
            response_msg = Message(
                sender=self.agent_id,
                recipient=message.sender,
                message_type=MessageType.RESPONSE,
                content=response,
            )
            await self.message_bus.send_response(message.id, response_msg)

        # Subclasses can override to handle other message types

    async def _handle_query(self, query: Any) -> Any:
        """
        Handle a query from another agent.

        Args:
            query: The query content

        Returns:
            The response
        """
        # Default implementation - can be overridden by subclasses
        return {"status": "received", "agent_id": self.agent_id}

    def has_capability(self, capability_name: str) -> bool:
        """
        Check if the agent has a specific capability.

        Args:
            capability_name: Name of the capability to check

        Returns:
            True if the agent has the capability
        """
        return any(cap.name == capability_name for cap in self.capabilities)

    def get_capability_proficiency(self, capability_name: str) -> float:
        """
        Get the proficiency level for a capability.

        Args:
            capability_name: Name of the capability

        Returns:
            Proficiency level (0.0 to 1.0), or 0.0 if not found
        """
        for cap in self.capabilities:
            if cap.name == capability_name:
                return cap.proficiency
        return 0.0

    def add_tool(self, tool_name: str, tool: Any) -> None:
        """
        Add a tool to the agent.

        Args:
            tool_name: Name of the tool
            tool: The tool object
        """
        self.tools[tool_name] = tool
        logger.debug(f"Agent {self.agent_id} added tool: {tool_name}")

    def _capture_state(self, task: Task) -> Dict[str, Any]:
        """
        Capture the current state for learning.

        Args:
            task: Current task

        Returns:
            State dictionary
        """
        return {
            "agent_performance": self.state.performance_score,
            "completed_tasks": self.state.completed_tasks,
            "failed_tasks": self.state.failed_tasks,
            "average_time": self.state.average_execution_time,
            "task_priority": task.priority,
            "task_requirements": len(task.requirements),
        }

    def _calculate_reward(self, result: Result) -> float:
        """
        Calculate reward for a task result.

        Args:
            result: The task result

        Returns:
            Reward value
        """
        if not result.success:
            return -0.5

        # Base reward for completion
        reward = 1.0

        # Quality bonus
        reward += result.quality_score * 0.5

        # Efficiency bonus (faster is better, within reason)
        if result.execution_time > 0:
            # Bonus for tasks completed quickly
            # Assuming average task should take around 10 seconds
            if result.execution_time < 10:
                reward += 0.2

        return reward

    def get_experiences(self) -> List[Experience]:
        """Get all experiences for learning."""
        return self.experiences

    def clear_experiences(self) -> None:
        """Clear experience buffer."""
        self.experiences = []

    def get_state(self) -> AgentState:
        """Get current agent state."""
        return self.state

    def to_dict(self) -> Dict[str, Any]:
        """Convert agent to dictionary representation."""
        return {
            "agent_id": self.agent_id,
            "capabilities": [cap.name for cap in self.capabilities],
            "state": self.state.to_dict(),
            "current_task": self.current_task.id if self.current_task else None,
            "experience_count": len(self.experiences),
        }
