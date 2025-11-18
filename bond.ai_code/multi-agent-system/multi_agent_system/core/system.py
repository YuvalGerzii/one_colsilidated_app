"""
Main Multi-Agent System controller.

Integrates all components into a cohesive system.
"""

import asyncio
import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional
from loguru import logger

from multi_agent_system.core.types import Task, Result, SystemMetrics
from multi_agent_system.agents.base import BaseAgent
from multi_agent_system.agents.orchestrator import OrchestratorAgent
from multi_agent_system.agents.workers import create_worker_pool
from multi_agent_system.communication.message_bus import MessageBus
from multi_agent_system.memory.memory_manager import MemoryManager
from multi_agent_system.learning.q_learning import QLearningEngine
from multi_agent_system.tools.base_tool import ToolRegistry


class MultiAgentSystem:
    """
    Main Multi-Agent System with Reinforcement Learning.

    Features:
    - Orchestrator-worker pattern
    - Parallel task execution
    - Reinforcement learning
    - Memory management
    - Tool integration
    """

    def __init__(
        self,
        config_path: Optional[str] = None,
        enable_learning: bool = True,
    ):
        """
        Initialize the multi-agent system.

        Args:
            config_path: Path to configuration file
            enable_learning: Enable reinforcement learning
        """
        # Load configuration
        self.config = self._load_config(config_path)

        # Initialize components
        self.message_bus = MessageBus(
            max_queue_size=self.config["communication"]["message_queue_size"],
        )

        self.tool_registry = ToolRegistry()

        # Initialize orchestrator
        self.orchestrator = OrchestratorAgent(message_bus=self.message_bus)

        # Initialize workers
        worker_types = {
            wtype["name"]: wtype["max_instances"]
            for wtype in self.config["agents"]["worker_types"]
        }
        self.workers = create_worker_pool(worker_types, self.message_bus)

        # Register workers with orchestrator
        for worker in self.workers.values():
            self.orchestrator.register_worker(worker)

        # All agents (orchestrator + workers)
        self.agents: Dict[str, BaseAgent] = {
            self.orchestrator.agent_id: self.orchestrator,
            **self.workers,
        }

        # Initialize memory for each agent
        self.memories: Dict[str, MemoryManager] = {}
        for agent_id in self.agents:
            self.memories[agent_id] = MemoryManager(
                agent_id=agent_id,
                short_term_size=self.config["memory"]["short_term_size"],
                long_term_path=self.config["memory"]["long_term_path"],
                consolidation_threshold=self.config["memory"]["consolidation_threshold"],
            )

        # Initialize learning engines if enabled
        self.enable_learning = enable_learning and self.config["learning"]["enabled"]
        self.learning_engines: Dict[str, QLearningEngine] = {}

        if self.enable_learning:
            for agent_id in self.agents:
                self.learning_engines[agent_id] = QLearningEngine(
                    agent_id=agent_id,
                    learning_rate=self.config["learning"]["learning_rate"],
                    discount_factor=self.config["learning"]["discount_factor"],
                    exploration_rate=self.config["learning"]["exploration_rate"],
                    exploration_decay=self.config["learning"]["exploration_decay"],
                    min_exploration_rate=self.config["learning"]["min_exploration_rate"],
                    replay_buffer_size=self.config["learning"]["replay_buffer_size"],
                )

        # System state
        self.running = False
        self.metrics = SystemMetrics()

        # Task tracking
        self.tasks: Dict[str, Task] = {}
        self.results: Dict[str, Result] = {}

        logger.info(
            f"MultiAgentSystem initialized with {len(self.workers)} workers, "
            f"learning={'enabled' if self.enable_learning else 'disabled'}"
        )

    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load configuration from file or use defaults."""
        default_config_path = Path(__file__).parent.parent.parent / "config.yaml"

        if config_path:
            path = Path(config_path)
        elif default_config_path.exists():
            path = default_config_path
        else:
            # Use default configuration
            return self._get_default_config()

        try:
            with open(path, "r") as f:
                config = yaml.safe_load(f)
            logger.info(f"Loaded configuration from {path}")
            return config
        except Exception as e:
            logger.warning(f"Failed to load config from {path}: {e}, using defaults")
            return self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "system": {
                "max_agents": 10,
                "parallel_execution": True,
                "timeout": 300,
            },
            "learning": {
                "enabled": True,
                "learning_rate": 0.1,
                "discount_factor": 0.95,
                "exploration_rate": 0.2,
                "exploration_decay": 0.995,
                "min_exploration_rate": 0.01,
                "batch_size": 32,
                "replay_buffer_size": 10000,
            },
            "memory": {
                "short_term_size": 1000,
                "long_term_path": "./data/memory",
                "consolidation_threshold": 0.7,
            },
            "communication": {
                "message_queue_size": 1000,
            },
            "agents": {
                "worker_types": [
                    {"name": "researcher", "max_instances": 2},
                    {"name": "coder", "max_instances": 2},
                    {"name": "tester", "max_instances": 1},
                    {"name": "data_analyst", "max_instances": 1},
                ],
            },
        }

    async def start(self) -> None:
        """Start the multi-agent system."""
        if self.running:
            logger.warning("System already running")
            return

        self.running = True

        # Start all agents
        for agent in self.agents.values():
            await agent.start()

        logger.info("Multi-Agent System started")

    async def stop(self) -> None:
        """Stop the multi-agent system."""
        if not self.running:
            return

        self.running = False

        # Stop all agents
        for agent in self.agents.values():
            await agent.stop()

        logger.info("Multi-Agent System stopped")

    async def execute_task(self, task_description: str, **kwargs) -> Result:
        """
        Execute a task using the multi-agent system.

        Args:
            task_description: Description of the task to execute
            **kwargs: Additional task parameters

        Returns:
            Task execution result
        """
        # Create task
        task = Task(
            description=task_description,
            requirements=kwargs.get("requirements", []),
            context=kwargs.get("context", {}),
            priority=kwargs.get("priority", 1),
        )

        self.tasks[task.id] = task
        self.metrics.total_tasks += 1

        logger.info(f"Executing task: {task.description}")

        # Execute task through orchestrator
        result = await self.orchestrator.execute_task(task)

        self.results[task.id] = result

        # Update metrics
        if result.success:
            self.metrics.completed_tasks += 1
        else:
            self.metrics.failed_tasks += 1

        self.metrics.success_rate = (
            self.metrics.completed_tasks / self.metrics.total_tasks
        )

        # Collect experiences and train if learning is enabled
        if self.enable_learning:
            await self._learn_from_execution(task, result)

        logger.info(
            f"Task completed: success={result.success}, "
            f"time={result.execution_time:.2f}s"
        )

        return result

    async def _learn_from_execution(self, task: Task, result: Result) -> None:
        """
        Learn from task execution.

        Args:
            task: The executed task
            result: The result of execution
        """
        # Collect experiences from all agents
        for agent in self.agents.values():
            experiences = agent.get_experiences()

            if experiences:
                # Add to learning engine replay buffer
                learning_engine = self.learning_engines[agent.agent_id]

                for exp in experiences:
                    learning_engine.add_experience(exp)

                # Train from replay buffer
                if len(learning_engine.replay_buffer) >= self.config["learning"]["batch_size"]:
                    learning_engine.train_from_replay(
                        batch_size=self.config["learning"]["batch_size"]
                    )

                # Clear agent experiences
                agent.clear_experiences()

    def add_agent(
        self,
        name: str,
        capabilities: List[str],
        agent_class: Optional[type] = None,
    ) -> str:
        """
        Add a new agent to the system.

        Args:
            name: Name/ID for the agent
            capabilities: List of capability names
            agent_class: Custom agent class (optional)

        Returns:
            Agent ID
        """
        from multi_agent_system.core.types import AgentCapability
        from multi_agent_system.agents.workers import GeneralAgent

        # Create capabilities
        caps = [AgentCapability(cap, f"{cap} capability") for cap in capabilities]

        # Create agent
        if agent_class:
            agent = agent_class(agent_id=name, message_bus=self.message_bus)
        else:
            agent = GeneralAgent(agent_id=name, message_bus=self.message_bus)
            agent.capabilities = caps

        # Add to system
        self.agents[name] = agent
        self.workers[name] = agent
        self.orchestrator.register_worker(agent)

        # Add memory
        self.memories[name] = MemoryManager(
            agent_id=name,
            short_term_size=self.config["memory"]["short_term_size"],
        )

        # Add learning engine if enabled
        if self.enable_learning:
            self.learning_engines[name] = QLearningEngine(agent_id=name)

        # Start agent if system is running
        if self.running:
            asyncio.create_task(agent.start())

        logger.info(f"Added agent: {name}")
        return name

    def add_custom_agent(self, agent: BaseAgent) -> None:
        """
        Add a custom agent instance.

        Args:
            agent: Agent instance to add
        """
        agent.message_bus = self.message_bus

        self.agents[agent.agent_id] = agent
        self.workers[agent.agent_id] = agent
        self.orchestrator.register_worker(agent)

        # Add memory and learning
        self.memories[agent.agent_id] = MemoryManager(agent_id=agent.agent_id)

        if self.enable_learning:
            self.learning_engines[agent.agent_id] = QLearningEngine(
                agent_id=agent.agent_id
            )

        if self.running:
            asyncio.create_task(agent.start())

        logger.info(f"Added custom agent: {agent.agent_id}")

    def save_policies(self, path: str) -> None:
        """
        Save learned policies for all agents.

        Args:
            path: Directory to save policies
        """
        if not self.enable_learning:
            logger.warning("Learning is disabled, no policies to save")
            return

        save_path = Path(path)
        save_path.mkdir(parents=True, exist_ok=True)

        for agent_id, engine in self.learning_engines.items():
            agent_path = save_path / f"{agent_id}_policy.pkl"
            engine.save_model(str(agent_path))

        logger.info(f"Saved policies for {len(self.learning_engines)} agents to {path}")

    def load_policies(self, path: str) -> None:
        """
        Load learned policies for all agents.

        Args:
            path: Directory to load policies from
        """
        if not self.enable_learning:
            logger.warning("Learning is disabled, cannot load policies")
            return

        load_path = Path(path)

        if not load_path.exists():
            logger.warning(f"Policy path does not exist: {path}")
            return

        for agent_id, engine in self.learning_engines.items():
            agent_path = load_path / f"{agent_id}_policy.pkl"
            if agent_path.exists():
                engine.load_model(str(agent_path))

        logger.info(f"Loaded policies from {path}")

    def get_metrics(self) -> SystemMetrics:
        """Get system metrics."""
        self.metrics.active_agents = sum(
            1 for agent in self.agents.values() if agent.state.status != "idle"
        )

        return self.metrics

    def get_agent_states(self) -> Dict[str, Any]:
        """Get state of all agents."""
        return {
            agent_id: agent.state.to_dict()
            for agent_id, agent in self.agents.items()
        }

    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        return {
            "running": self.running,
            "metrics": self.metrics.to_dict(),
            "agents": self.get_agent_states(),
            "learning_enabled": self.enable_learning,
            "learning_stats": {
                agent_id: engine.get_statistics()
                for agent_id, engine in self.learning_engines.items()
            } if self.enable_learning else {},
        }
