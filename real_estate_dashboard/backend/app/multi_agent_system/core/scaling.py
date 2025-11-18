"""
Dynamic agent scaling based on task complexity.

Implements 2025 best practices for scaling multi-agent systems.
"""

from typing import Any, Dict, List, Optional
from enum import Enum
from loguru import logger

from app.multi_agent_system.core.types import Task


class TaskComplexity(Enum):
    """Task complexity levels."""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    VERY_COMPLEX = "very_complex"


class ScalingStrategy:
    """
    Dynamic scaling strategy for multi-agent systems.

    Based on 2025 research:
    - Simple tasks: 1 agent, 3-10 tool calls
    - Direct comparisons: 2-4 agents, 10-15 calls each
    - Complex research: 10+ agents with divided responsibilities
    """

    def __init__(self):
        """Initialize scaling strategy."""
        self.complexity_thresholds = {
            TaskComplexity.SIMPLE: {
                "max_agents": 1,
                "max_tool_calls": 10,
                "min_requirements": 0,
                "max_requirements": 1,
                "description_length": 100,
            },
            TaskComplexity.MODERATE: {
                "max_agents": 4,
                "max_tool_calls": 15,
                "min_requirements": 2,
                "max_requirements": 3,
                "description_length": 300,
            },
            TaskComplexity.COMPLEX: {
                "max_agents": 8,
                "max_tool_calls": 25,
                "min_requirements": 4,
                "max_requirements": 6,
                "description_length": 600,
            },
            TaskComplexity.VERY_COMPLEX: {
                "max_agents": 15,
                "max_tool_calls": 50,
                "min_requirements": 7,
                "max_requirements": float("inf"),
                "description_length": 1000,
            },
        }

        logger.info("ScalingStrategy initialized")

    def assess_complexity(self, task: Task) -> TaskComplexity:
        """
        Assess task complexity.

        Args:
            task: Task to assess

        Returns:
            Complexity level
        """
        # Factors to consider
        requirement_count = len(task.requirements)
        description_length = len(task.description)
        subtask_count = len(task.subtasks)
        priority = task.priority

        # Calculate complexity score
        score = 0.0

        # Requirements contribute most
        score += requirement_count * 2.0

        # Description length
        if description_length > 500:
            score += 3.0
        elif description_length > 200:
            score += 1.5

        # Subtasks
        score += subtask_count * 1.5

        # High priority tasks get more resources
        if priority >= 8:
            score += 1.0

        # Context complexity
        if task.context:
            score += len(task.context) * 0.5

        # Determine complexity level
        if score <= 2:
            complexity = TaskComplexity.SIMPLE
        elif score <= 6:
            complexity = TaskComplexity.MODERATE
        elif score <= 12:
            complexity = TaskComplexity.COMPLEX
        else:
            complexity = TaskComplexity.VERY_COMPLEX

        logger.debug(
            f"Task complexity: {complexity.value} (score={score:.1f})"
        )

        return complexity

    def get_agent_allocation(
        self, task: Task, available_agents: int
    ) -> Dict[str, Any]:
        """
        Determine how many agents to allocate to a task.

        Args:
            task: Task to allocate for
            available_agents: Number of available agents

        Returns:
            Allocation recommendation
        """
        complexity = self.assess_complexity(task)
        thresholds = self.complexity_thresholds[complexity]

        # Calculate recommended agent count
        recommended_agents = min(
            thresholds["max_agents"],
            available_agents,
            max(1, len(task.requirements))  # At least 1 per requirement
        )

        # Calculate recommended tool calls per agent
        tool_calls_per_agent = thresholds["max_tool_calls"] // max(
            recommended_agents, 1
        )

        allocation = {
            "complexity": complexity.value,
            "recommended_agents": recommended_agents,
            "max_tool_calls_per_agent": tool_calls_per_agent,
            "total_estimated_calls": recommended_agents * tool_calls_per_agent,
            "parallel_execution": recommended_agents > 1,
            "estimated_speedup": min(recommended_agents, len(task.requirements)) if recommended_agents > 1 else 1.0,
        }

        logger.info(
            f"Agent allocation: {recommended_agents} agents for {complexity.value} task"
        )

        return allocation

    def should_spawn_subagent(
        self,
        current_depth: int,
        max_depth: int,
        task_complexity: TaskComplexity,
    ) -> bool:
        """
        Determine if a subagent should be spawned.

        Args:
            current_depth: Current recursion depth
            max_depth: Maximum allowed depth
            task_complexity: Complexity of the task

        Returns:
            True if subagent should be spawned
        """
        if current_depth >= max_depth:
            return False

        # More complex tasks benefit from deeper hierarchies
        depth_limits = {
            TaskComplexity.SIMPLE: 1,
            TaskComplexity.MODERATE: 2,
            TaskComplexity.COMPLEX: 3,
            TaskComplexity.VERY_COMPLEX: 4,
        }

        return current_depth < depth_limits.get(task_complexity, 2)

    def get_decomposition_strategy(
        self, task: Task
    ) -> Dict[str, Any]:
        """
        Get strategy for decomposing a task.

        Args:
            task: Task to decompose

        Returns:
            Decomposition strategy
        """
        complexity = self.assess_complexity(task)

        if complexity == TaskComplexity.SIMPLE:
            strategy = {
                "should_decompose": False,
                "decomposition_method": "none",
                "subtask_count": 1,
            }

        elif complexity == TaskComplexity.MODERATE:
            strategy = {
                "should_decompose": True,
                "decomposition_method": "requirement_based",
                "subtask_count": max(len(task.requirements), 2),
                "parallel_subtasks": True,
            }

        elif complexity == TaskComplexity.COMPLEX:
            strategy = {
                "should_decompose": True,
                "decomposition_method": "hierarchical",
                "subtask_count": max(len(task.requirements), 4),
                "parallel_subtasks": True,
                "allow_nesting": True,
                "max_nesting_depth": 2,
            }

        else:  # VERY_COMPLEX
            strategy = {
                "should_decompose": True,
                "decomposition_method": "divide_and_conquer",
                "subtask_count": max(len(task.requirements), 8),
                "parallel_subtasks": True,
                "allow_nesting": True,
                "max_nesting_depth": 3,
                "use_coordination": True,
            }

        logger.debug(
            f"Decomposition strategy: {strategy['decomposition_method']}"
        )

        return strategy


class LoadBalancer:
    """
    Load balancer for distributing tasks across agents.
    """

    def __init__(self):
        """Initialize load balancer."""
        self.agent_loads: Dict[str, float] = {}
        logger.info("LoadBalancer initialized")

    def update_load(self, agent_id: str, load: float) -> None:
        """
        Update load for an agent.

        Args:
            agent_id: Agent identifier
            load: Current load (0.0 to 1.0)
        """
        self.agent_loads[agent_id] = load

    def get_least_loaded_agent(
        self, agent_ids: List[str]
    ) -> Optional[str]:
        """
        Get the least loaded agent.

        Args:
            agent_ids: List of candidate agent IDs

        Returns:
            ID of least loaded agent, or None
        """
        if not agent_ids:
            return None

        # Filter to only those in the candidate list
        loads = {
            aid: self.agent_loads.get(aid, 0.0)
            for aid in agent_ids
        }

        if not loads:
            return agent_ids[0]

        # Return agent with minimum load
        return min(loads.items(), key=lambda x: x[1])[0]

    def distribute_tasks(
        self, tasks: List[Task], agent_ids: List[str]
    ) -> Dict[str, List[Task]]:
        """
        Distribute tasks across agents.

        Args:
            tasks: Tasks to distribute
            agent_ids: Available agents

        Returns:
            Dictionary mapping agent IDs to task lists
        """
        if not agent_ids:
            return {}

        # Sort agents by current load
        sorted_agents = sorted(
            agent_ids,
            key=lambda aid: self.agent_loads.get(aid, 0.0)
        )

        # Distribute tasks in round-robin fashion to least loaded agents
        distribution: Dict[str, List[Task]] = {aid: [] for aid in agent_ids}

        for idx, task in enumerate(tasks):
            agent_id = sorted_agents[idx % len(sorted_agents)]
            distribution[agent_id].append(task)

        logger.info(
            f"Distributed {len(tasks)} tasks across {len(agent_ids)} agents"
        )

        return distribution

    def get_load_statistics(self) -> Dict[str, Any]:
        """Get load balancing statistics."""
        if not self.agent_loads:
            return {}

        import numpy as np

        loads = list(self.agent_loads.values())

        return {
            "total_agents": len(self.agent_loads),
            "average_load": float(np.mean(loads)),
            "max_load": float(np.max(loads)),
            "min_load": float(np.min(loads)),
            "load_variance": float(np.var(loads)),
        }
