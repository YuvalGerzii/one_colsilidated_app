"""
Intelligent orchestrator with selective agent involvement.

Based on Anthropic's multi-agent research best practices:
- Dynamically scales effort based on task complexity
- Involves only relevant agents
- Provides detailed, clear instructions to agents
- Tracks token usage and efficiency
- Supports parallel execution with proper coordination
"""

import asyncio
from typing import Any, Dict, List, Optional, Set, Tuple
from loguru import logger
from datetime import datetime
import re

from multi_agent_system.agents.base import BaseAgent
from multi_agent_system.core.types import (
    Task,
    Result,
    Message,
    MessageType,
    AgentCapability,
    TaskStatus,
)


class TaskComplexity:
    """Analyze task complexity to determine agent involvement."""

    @staticmethod
    def analyze(task: Task) -> Dict[str, Any]:
        """
        Analyze task complexity.

        Returns:
            Dictionary with complexity metrics
        """
        description = task.description.lower()

        # Count indicators of complexity
        complexity_indicators = {
            "comparison": len(re.findall(r'\bcompare|versus|vs\b', description)),
            "analysis": len(re.findall(r'\banalyze|examine|evaluate|assess\b', description)),
            "research": len(re.findall(r'\bresearch|investigate|study|explore\b', description)),
            "multiple_topics": len(re.findall(r'\band|or|also|additionally\b', description)),
            "depth": len(re.findall(r'\bdetailed|comprehensive|thorough|in-depth\b', description)),
        }

        total_indicators = sum(complexity_indicators.values())
        num_requirements = len(task.requirements)
        description_length = len(description.split())

        # Calculate complexity score (0-1)
        complexity_score = min(
            (total_indicators * 0.2 + num_requirements * 0.1 + description_length / 200) / 3,
            1.0
        )

        # Determine task type
        task_type = "simple"
        if complexity_score < 0.3:
            task_type = "simple"  # 1-2 agents
        elif complexity_score < 0.6:
            task_type = "moderate"  # 3-5 agents
        else:
            task_type = "complex"  # 6+ agents

        return {
            "score": complexity_score,
            "type": task_type,
            "indicators": complexity_indicators,
            "estimated_agents": TaskComplexity._estimate_agent_count(complexity_score),
            "parallel_potential": complexity_indicators["comparison"] + complexity_indicators["multiple_topics"]
        }

    @staticmethod
    def _estimate_agent_count(complexity_score: float) -> int:
        """Estimate number of agents needed based on complexity."""
        if complexity_score < 0.3:
            return 1
        elif complexity_score < 0.6:
            return 3
        else:
            return max(6, min(int(complexity_score * 15), 12))


class AgentSelector:
    """Intelligently select agents based on task requirements."""

    def __init__(self, workers: Dict[str, BaseAgent]):
        """
        Initialize the agent selector.

        Args:
            workers: Available worker agents
        """
        self.workers = workers
        self._build_capability_index()

    def _build_capability_index(self) -> None:
        """Build an index of capabilities to agents."""
        self.capability_index: Dict[str, List[str]] = {}

        for worker_id, worker in self.workers.items():
            for capability in worker.capabilities:
                cap_name = capability.name
                if cap_name not in self.capability_index:
                    self.capability_index[cap_name] = []
                self.capability_index[cap_name].append(worker_id)

    def select_agents(
        self,
        task: Task,
        complexity_analysis: Dict[str, Any]
    ) -> List[Tuple[str, float]]:
        """
        Select relevant agents for a task.

        Args:
            task: The task to assign
            complexity_analysis: Complexity analysis results

        Returns:
            List of (agent_id, relevance_score) tuples
        """
        candidates: Dict[str, float] = {}

        # Score agents based on capability match
        for requirement in task.requirements:
            if requirement in self.capability_index:
                for agent_id in self.capability_index[requirement]:
                    if agent_id not in candidates:
                        candidates[agent_id] = 0.0

                    worker = self.workers[agent_id]
                    proficiency = worker.get_capability_proficiency(requirement)
                    candidates[agent_id] += proficiency

        # If no specific requirements, use keyword matching
        if not candidates:
            candidates = self._match_by_keywords(task)

        # Factor in agent performance
        for agent_id in candidates:
            worker = self.workers[agent_id]
            performance_score = worker.state.performance_score
            candidates[agent_id] *= performance_score

        # Sort by relevance score
        sorted_candidates = sorted(
            candidates.items(),
            key=lambda x: x[1],
            reverse=True
        )

        # Limit based on complexity
        max_agents = complexity_analysis["estimated_agents"]

        return sorted_candidates[:max_agents]

    def _match_by_keywords(self, task: Task) -> Dict[str, float]:
        """Match agents to task based on keyword analysis."""
        description_lower = task.description.lower()
        candidates: Dict[str, float] = {}

        # Keyword to capability mapping
        keyword_map = {
            "research": ["research", "web_search", "information_gathering"],
            "code": ["code_generation", "debugging", "refactoring"],
            "test": ["testing", "qa", "validation"],
            "analyze": ["data_analysis", "pattern_recognition", "statistical_analysis"],
            "write": ["documentation", "content_creation"],
            "data": ["data_processing", "data_analysis"],
        }

        for keyword, capabilities in keyword_map.items():
            if keyword in description_lower:
                for capability in capabilities:
                    if capability in self.capability_index:
                        for agent_id in self.capability_index[capability]:
                            if agent_id not in candidates:
                                candidates[agent_id] = 0.0
                            candidates[agent_id] += 0.5

        return candidates


class IntelligentOrchestrator(BaseAgent):
    """
    Intelligent orchestrator that selectively involves agents.

    Key improvements:
    - Analyzes task complexity before delegating
    - Only involves relevant agents
    - Provides detailed, clear instructions
    - Tracks efficiency metrics
    - Optimizes for token usage
    """

    def __init__(self, agent_id: str = "intelligent_orchestrator", message_bus=None):
        capabilities = [
            AgentCapability("task_analysis", "Analyze task complexity", 1.0),
            AgentCapability("agent_selection", "Select relevant agents", 1.0),
            AgentCapability("instruction_generation", "Generate clear instructions", 1.0),
            AgentCapability("result_synthesis", "Synthesize results", 1.0),
        ]
        super().__init__(agent_id, capabilities, message_bus)

        # Track workers
        self.workers: Dict[str, BaseAgent] = {}
        self.agent_selector: Optional[AgentSelector] = None

        # Efficiency metrics
        self.metrics = {
            "total_tasks": 0,
            "simple_tasks": 0,
            "moderate_tasks": 0,
            "complex_tasks": 0,
            "agents_involved_total": 0,
            "avg_agents_per_task": 0.0,
            "token_savings": 0,  # Estimated
        }

        logger.info("IntelligentOrchestrator initialized")

    def register_worker(self, worker: BaseAgent) -> None:
        """
        Register a worker agent.

        Args:
            worker: Worker agent to register
        """
        self.workers[worker.agent_id] = worker

        # Rebuild agent selector
        self.agent_selector = AgentSelector(self.workers)

        logger.info(f"Registered worker {worker.agent_id}")

    async def process_task(self, task: Task) -> Result:
        """
        Process a task with intelligent agent selection.

        Strategy:
        1. Analyze task complexity
        2. Select only relevant agents
        3. Generate detailed instructions for each agent
        4. Execute in parallel
        5. Synthesize results

        Args:
            task: Task to process

        Returns:
            Synthesized result
        """
        start_time = datetime.now()

        logger.info(f"IntelligentOrchestrator analyzing task: {task.description}")

        # Step 1: Analyze complexity
        complexity_analysis = TaskComplexity.analyze(task)

        logger.info(
            f"Task complexity: {complexity_analysis['type']} "
            f"(score={complexity_analysis['score']:.2f}, "
            f"estimated_agents={complexity_analysis['estimated_agents']})"
        )

        # Step 2: Select relevant agents
        if not self.agent_selector:
            logger.error("No agent selector available")
            return Result(
                task_id=task.id,
                success=False,
                error="No workers registered",
            )

        selected_agents = self.agent_selector.select_agents(task, complexity_analysis)

        if not selected_agents:
            logger.warning("No suitable agents found")
            return Result(
                task_id=task.id,
                success=False,
                error="No suitable agents available",
            )

        logger.info(
            f"Selected {len(selected_agents)} agents: "
            f"{[aid for aid, _ in selected_agents]}"
        )

        # Step 3: Decompose task and generate detailed instructions
        subtasks = self._create_detailed_subtasks(
            task,
            selected_agents,
            complexity_analysis
        )

        # Step 4: Execute in parallel
        results = await self._execute_parallel(subtasks)

        # Step 5: Synthesize results
        final_result = self._synthesize_results(task, results, complexity_analysis)

        # Update metrics
        self._update_metrics(complexity_analysis, len(selected_agents))

        execution_time = (datetime.now() - start_time).total_seconds()
        final_result.execution_time = execution_time

        logger.info(
            f"Task completed in {execution_time:.2f}s with "
            f"{len(selected_agents)} agents"
        )

        return final_result

    def _create_detailed_subtasks(
        self,
        task: Task,
        selected_agents: List[Tuple[str, float]],
        complexity_analysis: Dict[str, Any]
    ) -> List[Tuple[Task, str]]:
        """
        Create detailed subtasks with clear instructions.

        Based on Anthropic's best practice: detailed instructions prevent
        duplication and improve quality.

        Args:
            task: Original task
            selected_agents: Selected agents with relevance scores
            complexity_analysis: Complexity analysis

        Returns:
            List of (subtask, agent_id) tuples
        """
        subtasks = []

        if complexity_analysis["type"] == "simple":
            # For simple tasks, assign to best agent
            agent_id, _ = selected_agents[0]
            subtask = self._create_subtask(
                task,
                agent_id,
                index=0,
                total=1,
                focus="Complete the entire task"
            )
            subtasks.append((subtask, agent_id))

        elif complexity_analysis["type"] == "moderate":
            # For moderate tasks, divide by requirements
            if task.requirements:
                for idx, requirement in enumerate(task.requirements):
                    if idx < len(selected_agents):
                        agent_id, _ = selected_agents[idx]
                        subtask = self._create_subtask(
                            task,
                            agent_id,
                            index=idx,
                            total=len(task.requirements),
                            focus=f"Focus on {requirement}"
                        )
                        subtasks.append((subtask, agent_id))
            else:
                # Divide by capability
                for idx, (agent_id, _) in enumerate(selected_agents):
                    worker = self.workers[agent_id]
                    primary_cap = worker.capabilities[0].name if worker.capabilities else "general"
                    subtask = self._create_subtask(
                        task,
                        agent_id,
                        index=idx,
                        total=len(selected_agents),
                        focus=f"Apply {primary_cap} to this task"
                    )
                    subtasks.append((subtask, agent_id))

        else:  # complex
            # For complex tasks, create specialized subtasks
            subtasks = self._decompose_complex_task(
                task,
                selected_agents,
                complexity_analysis
            )

        return subtasks

    def _create_subtask(
        self,
        parent_task: Task,
        agent_id: str,
        index: int,
        total: int,
        focus: str
    ) -> Task:
        """
        Create a detailed subtask with clear instructions.

        Includes:
        - Objective clarity
        - Output format specification
        - Task boundaries
        - Context from parent task
        """
        worker = self.workers[agent_id]

        # Generate detailed description
        detailed_description = f"""
SUBTASK {index + 1} of {total}

OBJECTIVE: {focus}

PARENT TASK: {parent_task.description}

YOUR ROLE: {worker.capabilities[0].name if worker.capabilities else 'general worker'}

SPECIFIC INSTRUCTIONS:
1. {focus}
2. Use your specialized capabilities: {', '.join(c.name for c in worker.capabilities[:3])}
3. Provide specific, actionable outputs
4. Include confidence scores and quality metrics

OUTPUT FORMAT:
- Structured data with clear labels
- Include sources/reasoning where applicable
- Mark any uncertainties

BOUNDARIES:
- Focus only on: {focus}
- Do not overlap with other subtasks
- Time limit: Optimize for quality within reasonable time
        """.strip()

        subtask = Task(
            description=detailed_description,
            requirements=[focus],
            context={
                **parent_task.context,
                "subtask_index": index,
                "total_subtasks": total,
                "focus_area": focus,
                "assigned_agent": agent_id,
            },
            priority=parent_task.priority,
            parent_task_id=parent_task.id,
            metadata={
                "orchestrator_type": "intelligent",
                "instruction_quality": "detailed",
            },
        )

        parent_task.subtasks.append(subtask.id)

        return subtask

    def _decompose_complex_task(
        self,
        task: Task,
        selected_agents: List[Tuple[str, float]],
        complexity_analysis: Dict[str, Any]
    ) -> List[Tuple[Task, str]]:
        """Decompose complex tasks into parallel work streams."""
        subtasks = []

        # Identify parallel work streams
        description_lower = task.description.lower()

        work_streams = []

        # Check for comparison tasks
        if complexity_analysis["indicators"]["comparison"] > 0:
            work_streams.extend([
                "Research first option",
                "Research second option",
                "Comparative analysis",
            ])
        # Check for multi-aspect research
        elif complexity_analysis["indicators"]["research"] > 0:
            work_streams.extend([
                "Background research and context",
                "Current state analysis",
                "Future trends and implications",
            ])
        # Default: divide by capability
        else:
            for agent_id, _ in selected_agents:
                worker = self.workers[agent_id]
                primary_cap = worker.capabilities[0].name if worker.capabilities else "general"
                work_streams.append(f"Apply {primary_cap}")

        # Create subtasks for each work stream
        for idx, focus in enumerate(work_streams):
            if idx < len(selected_agents):
                agent_id, _ = selected_agents[idx]
                subtask = self._create_subtask(
                    task,
                    agent_id,
                    index=idx,
                    total=len(work_streams),
                    focus=focus
                )
                subtasks.append((subtask, agent_id))

        return subtasks

    async def _execute_parallel(
        self,
        delegations: List[Tuple[Task, str]]
    ) -> List[Result]:
        """
        Execute tasks in parallel with proper error handling.

        Args:
            delegations: List of (task, worker_id) tuples

        Returns:
            List of results
        """
        logger.info(f"Executing {len(delegations)} subtasks in parallel")

        # Create coroutines
        coroutines = []
        for subtask, worker_id in delegations:
            worker = self.workers[worker_id]
            coroutines.append(worker.execute_task(subtask))

        # Execute in parallel
        results = await asyncio.gather(*coroutines, return_exceptions=True)

        # Process results
        processed_results = []
        for idx, result in enumerate(results):
            if isinstance(result, Exception):
                subtask, worker_id = delegations[idx]
                logger.error(f"Subtask {subtask.id} failed: {result}")
                processed_results.append(
                    Result(
                        task_id=subtask.id,
                        success=False,
                        error=str(result),
                        agent_id=worker_id,
                    )
                )
            else:
                processed_results.append(result)

        successful = sum(1 for r in processed_results if r.success)
        logger.info(f"Parallel execution complete: {successful}/{len(processed_results)} successful")

        return processed_results

    def _synthesize_results(
        self,
        original_task: Task,
        results: List[Result],
        complexity_analysis: Dict[str, Any]
    ) -> Result:
        """
        Synthesize results with quality assessment.

        Args:
            original_task: Original task
            results: Results from subtasks
            complexity_analysis: Complexity analysis

        Returns:
            Synthesized result
        """
        all_success = all(r.success for r in results)

        # Collect data
        combined_data = {
            "complexity_type": complexity_analysis["type"],
            "complexity_score": complexity_analysis["score"],
            "agents_involved": len(results),
            "successful_subtasks": sum(1 for r in results if r.success),
            "failed_subtasks": sum(1 for r in results if not r.success),
            "subtask_results": [],
        }

        for result in results:
            combined_data["subtask_results"].append({
                "task_id": result.task_id,
                "agent_id": result.agent_id,
                "success": result.success,
                "quality_score": result.quality_score,
                "execution_time": result.execution_time,
                "data": result.data,
            })

        # Calculate metrics
        if results:
            avg_quality = sum(r.quality_score for r in results) / len(results)
            max_time = max(r.execution_time for r in results)
        else:
            avg_quality = 0.0
            max_time = 0.0

        # Estimate token savings
        # Compared to involving all agents, we saved tokens
        total_agents = len(self.workers)
        agents_used = len(results)
        estimated_savings = (total_agents - agents_used) * 0.15  # Rough estimate

        synthesized = Result(
            task_id=original_task.id,
            success=all_success,
            data=combined_data,
            agent_id=self.agent_id,
            execution_time=max_time,
            quality_score=avg_quality,
            metadata={
                "orchestration_type": "intelligent",
                "agents_used": agents_used,
                "agents_available": total_agents,
                "efficiency_ratio": agents_used / total_agents if total_agents > 0 else 0,
                "estimated_token_savings": f"{estimated_savings:.1%}",
            },
        )

        logger.info(
            f"Synthesis complete: quality={avg_quality:.2f}, "
            f"efficiency={agents_used}/{total_agents} agents"
        )

        return synthesized

    def _update_metrics(self, complexity_analysis: Dict[str, Any], agents_used: int) -> None:
        """Update orchestrator metrics."""
        self.metrics["total_tasks"] += 1
        self.metrics["agents_involved_total"] += agents_used

        if complexity_analysis["type"] == "simple":
            self.metrics["simple_tasks"] += 1
        elif complexity_analysis["type"] == "moderate":
            self.metrics["moderate_tasks"] += 1
        else:
            self.metrics["complex_tasks"] += 1

        self.metrics["avg_agents_per_task"] = (
            self.metrics["agents_involved_total"] / self.metrics["total_tasks"]
        )

        # Estimate token savings (compared to always using all agents)
        total_agents = len(self.workers)
        if total_agents > 0:
            saved_agents = total_agents - agents_used
            self.metrics["token_savings"] += saved_agents

    def get_efficiency_metrics(self) -> Dict[str, Any]:
        """Get efficiency and performance metrics."""
        return {
            **self.metrics,
            "total_workers": len(self.workers),
            "worker_utilization": (
                self.metrics["avg_agents_per_task"] / len(self.workers)
                if self.workers else 0
            ),
        }

    def get_worker_status(self) -> Dict[str, Any]:
        """Get status of all workers."""
        return {
            worker_id: {
                "status": worker.state.status,
                "completed_tasks": worker.state.completed_tasks,
                "failed_tasks": worker.state.failed_tasks,
                "performance_score": worker.state.performance_score,
                "capabilities": [c.name for c in worker.capabilities],
            }
            for worker_id, worker in self.workers.items()
        }
