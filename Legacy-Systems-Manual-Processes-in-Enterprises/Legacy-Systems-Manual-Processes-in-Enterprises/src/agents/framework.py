"""
Intelligent Agent Framework
Base classes and interfaces for specialized AI agents
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Any, List, Optional
from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from loguru import logger

from src.core.llm import get_local_llm


class AgentRole(str, Enum):
    """Agent role types."""
    DISCOVERY = "discovery"
    ASSESSMENT = "assessment"
    ANALYSIS = "analysis"
    PLANNING = "planning"
    EXECUTION = "execution"
    MONITORING = "monitoring"
    ADVISORY = "advisory"
    DEVELOPER = "developer"  # For low-code/citizen dev agents
    ORCHESTRATOR = "orchestrator"  # For coordinating multiple agents


class AgentStatus(str, Enum):
    """Agent execution status."""
    IDLE = "idle"
    THINKING = "thinking"
    WORKING = "working"
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"


class AgentTask(BaseModel):
    """Task for an agent to execute."""
    id: str = Field(default_factory=lambda: str(uuid4()))
    type: str
    description: str
    input_data: Dict[str, Any] = Field(default_factory=dict)
    assigned_to: Optional[str] = None  # Specific agent ID
    priority: int = 5
    dependencies: List[str] = Field(default_factory=list)  # Task IDs this depends on
    delegate_to: Optional[str] = None  # Agent can delegate to another
    parent_task_id: Optional[str] = None  # For hierarchical tasks
    created_at: datetime = Field(default_factory=datetime.utcnow)


class AgentResult(BaseModel):
    """Result from agent execution."""
    task_id: str
    agent_id: str
    status: AgentStatus
    output: Dict[str, Any] = Field(default_factory=dict)
    confidence: float = 1.0
    reasoning: str = ""
    recommendations: List[str] = Field(default_factory=list)
    next_steps: List[str] = Field(default_factory=list)
    delegated_tasks: List[str] = Field(default_factory=list)  # Tasks delegated to other agents
    completed_at: datetime = Field(default_factory=datetime.utcnow)


class BaseAgent(ABC):
    """
    Base class for all intelligent agents.

    Each agent has:
    - A specific role and expertise
    - Ability to analyze and reason using local LLM
    - Structured output format
    - Collaboration capabilities
    """

    def __init__(self, agent_id: str, role: AgentRole):
        """Initialize agent."""
        self.agent_id = agent_id
        self.role = role
        self.status = AgentStatus.IDLE
        self.llm = get_local_llm()
        self.memory: List[Dict[str, Any]] = []

        logger.info(f"Initialized {self.__class__.__name__} (ID: {agent_id}, Role: {role})")

    @abstractmethod
    async def execute(self, task: AgentTask) -> AgentResult:
        """
        Execute a task.

        Args:
            task: Task to execute

        Returns:
            AgentResult: Execution result
        """
        pass

    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Get list of agent capabilities."""
        pass

    async def analyze_with_llm(
        self,
        prompt: str,
        context: Optional[str] = None,
        max_tokens: int = 2000,
    ) -> str:
        """
        Use local LLM to analyze and reason.

        Args:
            prompt: Analysis prompt
            context: Optional context information
            max_tokens: Maximum tokens to generate

        Returns:
            str: LLM response
        """
        messages = []

        if context:
            messages.append({
                "role": "system",
                "content": f"You are a {self.role} agent. {context}"
            })

        messages.append({
            "role": "user",
            "content": prompt
        })

        self.status = AgentStatus.THINKING

        try:
            response = await self.llm.chat_completion(
                messages=messages,
                temperature=0.3,  # Lower temperature for more focused analysis
                max_tokens=max_tokens,
            )

            self.status = AgentStatus.IDLE
            return response

        except Exception as e:
            logger.error(f"LLM analysis failed for {self.agent_id}: {e}")
            self.status = AgentStatus.FAILED
            raise

    def remember(self, key: str, value: Any) -> None:
        """Store information in agent memory."""
        self.memory.append({
            "timestamp": datetime.utcnow(),
            "key": key,
            "value": value,
        })

    def recall(self, key: str) -> Optional[Any]:
        """Recall information from memory."""
        for item in reversed(self.memory):
            if item["key"] == key:
                return item["value"]
        return None

    def get_context_summary(self) -> str:
        """Get summary of agent's memory/context."""
        if not self.memory:
            return "No prior context."

        recent = self.memory[-5:]  # Last 5 items
        summary = "\n".join([
            f"- {item['key']}: {str(item['value'])[:100]}"
            for item in recent
        ])
        return f"Recent context:\n{summary}"


class AgentOrchestrator:
    """
    Advanced Multi-Agent Orchestrator (2025)

    Coordinates multiple agents with support for:
    - Hierarchical delegation
    - Agent-to-agent communication
    - Event-driven coordination
    - Intelligent task routing
    - Parallel and sequential workflows

    Based on 2025 research: 58% of business functions use AI agents managing processes.
    """

    def __init__(self):
        """Initialize orchestrator."""
        self.agents: Dict[str, BaseAgent] = {}
        self.task_queue: List[AgentTask] = []
        self.task_results: Dict[str, AgentResult] = {}  # Changed from UUID to str
        self.agent_messages: Dict[str, List[Dict[str, Any]]] = {}  # Agent-to-agent messages

        logger.info("Advanced Multi-Agent Orchestrator initialized (2025)")

    def register_agent(self, agent: BaseAgent) -> None:
        """Register an agent with the orchestrator."""
        self.agents[agent.agent_id] = agent
        logger.info(f"Registered agent: {agent.agent_id} ({agent.role})")

    async def execute_workflow(
        self,
        workflow_name: str,
        tasks: List[AgentTask],
    ) -> List[AgentResult]:
        """
        Execute a workflow with multiple tasks.

        Args:
            workflow_name: Name of the workflow
            tasks: List of tasks to execute

        Returns:
            List[AgentResult]: Results from all tasks
        """
        logger.info(f"Starting workflow: {workflow_name} ({len(tasks)} tasks)")

        results = []

        for task in tasks:
            # Find appropriate agent for task
            agent = self._find_agent_for_task(task)

            if not agent:
                logger.warning(f"No agent found for task: {task.type}")
                continue

            # Execute task
            logger.info(f"Assigning task {task.id} to agent {agent.agent_id}")
            result = await agent.execute(task)

            results.append(result)
            self.results[result.task_id] = result

        logger.info(f"Workflow {workflow_name} completed with {len(results)} results")
        return results

    def _find_agent_for_task(self, task: AgentTask) -> Optional[BaseAgent]:
        """Find best agent for a task."""
        # Simple matching based on task type
        for agent in self.agents.values():
            capabilities = agent.get_capabilities()
            if any(cap in task.type for cap in capabilities):
                return agent

        return None

    async def collaborate(
        self,
        lead_agent: str,
        supporting_agents: List[str],
        task: AgentTask,
    ) -> AgentResult:
        """
        Multiple agents collaborate on a task.

        Args:
            lead_agent: ID of lead agent
            supporting_agents: IDs of supporting agents
            task: Task to execute

        Returns:
            AgentResult: Aggregated result
        """
        logger.info(f"Collaboration: {lead_agent} leading with {len(supporting_agents)} supporting agents")

        # Supporting agents provide input
        supporting_results = []
        for agent_id in supporting_agents:
            agent = self.agents.get(agent_id)
            if agent:
                result = await agent.execute(task)
                supporting_results.append(result)

        # Lead agent synthesizes
        lead = self.agents.get(lead_agent)
        if lead:
            # Add supporting results to task input
            task.input_data["supporting_analysis"] = [
                r.output for r in supporting_results
            ]

            final_result = await lead.execute(task)
            return final_result

        raise ValueError(f"Lead agent {lead_agent} not found")

    def get_all_capabilities(self) -> Dict[str, List[str]]:
        """Get capabilities of all registered agents."""
        return {
            agent_id: agent.get_capabilities()
            for agent_id, agent in self.agents.items()
        }

    # ========================================================================
    # ENHANCED MULTI-AGENT COORDINATION (2025)
    # ========================================================================

    async def execute_task(self, task: AgentTask) -> AgentResult:
        """
        Execute a single task with intelligent agent selection.

        Supports:
        - Automatic agent selection based on capabilities
        - Task delegation
        - Dependency resolution
        """
        logger.info(f"Executing task {task.id}: {task.description}")

        # Check dependencies
        if task.dependencies:
            await self._wait_for_dependencies(task.dependencies)

        # Find or use assigned agent
        if task.assigned_to:
            agent = self.agents.get(task.assigned_to)
            if not agent:
                raise ValueError(f"Assigned agent {task.assigned_to} not found")
        else:
            agent = self._find_agent_for_task(task)
            if not agent:
                raise ValueError(f"No suitable agent found for task type: {task.type}")

        # Execute task
        logger.info(f"Agent {agent.agent_id} executing task {task.id}")
        result = await agent.execute(task)

        # Store result
        self.task_results[task.id] = result

        # Handle delegation
        if result.delegated_tasks:
            await self._handle_delegated_tasks(result.delegated_tasks)

        return result

    async def execute_parallel_workflow(
        self,
        tasks: List[AgentTask],
        aggregate_results: bool = True
    ) -> List[AgentResult]:
        """
        Execute multiple tasks in parallel.

        Based on 2025 patterns for parallel agent execution.
        """
        import asyncio

        logger.info(f"Executing {len(tasks)} tasks in parallel")

        # Execute all tasks concurrently
        results = await asyncio.gather(
            *[self.execute_task(task) for task in tasks],
            return_exceptions=True
        )

        # Filter out exceptions
        valid_results = [r for r in results if isinstance(r, AgentResult)]

        logger.info(f"Parallel execution completed: {len(valid_results)}/{len(tasks)} succeeded")

        return valid_results

    async def execute_sequential_workflow(
        self,
        tasks: List[AgentTask],
        pass_context: bool = True
    ) -> List[AgentResult]:
        """
        Execute tasks sequentially, optionally passing context between them.

        Each agent can see results from previous agents.
        """
        logger.info(f"Executing {len(tasks)} tasks sequentially")

        results = []

        for i, task in enumerate(tasks):
            # Inject previous results as context
            if pass_context and results:
                task.input_data["previous_results"] = [
                    {
                        "agent": r.agent_id,
                        "output": r.output,
                        "recommendations": r.recommendations,
                    }
                    for r in results
                ]

            result = await self.execute_task(task)
            results.append(result)

            logger.info(f"Sequential step {i+1}/{len(tasks)} completed by {result.agent_id}")

        return results

    async def delegate_task(
        self,
        from_agent: str,
        to_agent: str,
        task: AgentTask
    ) -> AgentResult:
        """
        Hierarchical delegation: One agent delegates task to another.

        Based on 2025 multi-agent orchestration patterns.
        """
        logger.info(f"Agent {from_agent} delegating task to {to_agent}")

        task.assigned_to = to_agent
        task.parent_task_id = task.id

        result = await self.execute_task(task)

        # Notify original agent
        await self.send_message(to_agent, from_agent, {
            "type": "task_completed",
            "task_id": task.id,
            "result": result.output
        })

        return result

    async def send_message(
        self,
        from_agent: str,
        to_agent: str,
        message: Dict[str, Any]
    ) -> None:
        """
        Agent-to-agent communication.

        Enables agents to share information and coordinate.
        """
        if to_agent not in self.agent_messages:
            self.agent_messages[to_agent] = []

        self.agent_messages[to_agent].append({
            "from": from_agent,
            "timestamp": datetime.utcnow(),
            "message": message
        })

        logger.info(f"Message sent: {from_agent} -> {to_agent}")

    async def get_messages(self, agent_id: str) -> List[Dict[str, Any]]:
        """Get messages for an agent."""
        return self.agent_messages.get(agent_id, [])

    async def execute_conditional_workflow(
        self,
        condition_task: AgentTask,
        if_true_tasks: List[AgentTask],
        if_false_tasks: List[AgentTask]
    ) -> List[AgentResult]:
        """
        Execute conditional workflow based on agent decision.

        Pattern: IF condition THEN tasks_a ELSE tasks_b
        """
        logger.info("Executing conditional workflow")

        # Execute condition task
        condition_result = await self.execute_task(condition_task)

        # Determine which path to take
        condition_met = condition_result.output.get("condition_met", False)

        if condition_met:
            logger.info("Condition TRUE - executing if_true branch")
            return await self.execute_sequential_workflow(if_true_tasks)
        else:
            logger.info("Condition FALSE - executing if_false branch")
            return await self.execute_sequential_workflow(if_false_tasks)

    async def execute_hub_spoke_workflow(
        self,
        hub_agent_id: str,
        spoke_tasks: List[AgentTask],
        synthesize: bool = True
    ) -> AgentResult:
        """
        Hub-and-spoke pattern: Multiple agents feed into central coordinator.

        Based on 2025 multi-agent orchestration patterns (IBM watsonx style).
        """
        logger.info(f"Hub-spoke workflow: {hub_agent_id} coordinating {len(spoke_tasks)} spokes")

        # Execute all spoke tasks in parallel
        spoke_results = await self.execute_parallel_workflow(spoke_tasks)

        if not synthesize:
            return spoke_results

        # Hub agent synthesizes results
        hub_agent = self.agents.get(hub_agent_id)
        if not hub_agent:
            raise ValueError(f"Hub agent {hub_agent_id} not found")

        synthesis_task = AgentTask(
            id=f"synthesis-{uuid4()}",
            type="synthesize",
            description="Synthesize results from spoke agents",
            input_data={
                "spoke_results": [
                    {
                        "agent": r.agent_id,
                        "output": r.output,
                        "confidence": r.confidence,
                        "recommendations": r.recommendations,
                    }
                    for r in spoke_results
                ]
            },
            assigned_to=hub_agent_id,
        )

        final_result = await self.execute_task(synthesis_task)

        logger.info(f"Hub-spoke synthesis completed by {hub_agent_id}")

        return final_result

    async def _wait_for_dependencies(self, dependency_ids: List[str]) -> None:
        """Wait for dependency tasks to complete."""
        import asyncio

        logger.info(f"Waiting for {len(dependency_ids)} dependencies")

        # Poll for completion (simple implementation)
        max_wait = 300  # 5 minutes
        elapsed = 0

        while elapsed < max_wait:
            all_complete = all(
                dep_id in self.task_results and
                self.task_results[dep_id].status == AgentStatus.COMPLETED
                for dep_id in dependency_ids
            )

            if all_complete:
                logger.info("All dependencies completed")
                return

            await asyncio.sleep(1)
            elapsed += 1

        raise TimeoutError(f"Dependencies not completed within {max_wait} seconds")

    async def _handle_delegated_tasks(self, delegated_task_ids: List[str]) -> None:
        """Handle tasks that were delegated."""
        # In a full implementation, this would execute delegated tasks
        # For now, just log
        logger.info(f"Handling {len(delegated_task_ids)} delegated tasks")

    def get_workflow_status(self) -> Dict[str, Any]:
        """Get status of all tasks and agents."""
        return {
            "total_agents": len(self.agents),
            "total_tasks": len(self.task_results),
            "completed_tasks": sum(
                1 for r in self.task_results.values()
                if r.status == AgentStatus.COMPLETED
            ),
            "failed_tasks": sum(
                1 for r in self.task_results.values()
                if r.status == AgentStatus.FAILED
            ),
            "agent_statuses": {
                agent_id: agent.status.value
                for agent_id, agent in self.agents.items()
            },
            "pending_messages": {
                agent_id: len(messages)
                for agent_id, messages in self.agent_messages.items()
            },
        }
