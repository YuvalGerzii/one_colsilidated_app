"""
Orchestrator agent for coordinating worker agents.
"""

import asyncio
from typing import Any, Dict, List, Optional
from loguru import logger

from multi_agent_system.agents.base import BaseAgent
from multi_agent_system.core.types import (
    Task,
    Result,
    Message,
    MessageType,
    AgentCapability,
    TaskStatus,
)


class OrchestratorAgent(BaseAgent):
    """
    Orchestrator agent that coordinates multiple worker agents.

    Responsibilities:
    - Decompose complex tasks into subtasks
    - Delegate subtasks to appropriate worker agents
    - Coordinate parallel execution
    - Synthesize results from workers
    - Monitor progress and handle failures
    """

    def __init__(self, agent_id: str = "orchestrator", message_bus=None):
        capabilities = [
            AgentCapability("task_decomposition", "Break down complex tasks", 1.0),
            AgentCapability("delegation", "Delegate tasks to workers", 1.0),
            AgentCapability("coordination", "Coordinate multiple agents", 1.0),
            AgentCapability("synthesis", "Combine results from multiple sources", 1.0),
        ]
        super().__init__(agent_id, capabilities, message_bus)

        # Track worker agents and their capabilities
        self.workers: Dict[str, BaseAgent] = {}
        self.worker_capabilities: Dict[str, List[str]] = {}

    def register_worker(self, worker: BaseAgent) -> None:
        """
        Register a worker agent.

        Args:
            worker: Worker agent to register
        """
        self.workers[worker.agent_id] = worker
        self.worker_capabilities[worker.agent_id] = [
            cap.name for cap in worker.capabilities
        ]
        logger.info(f"Registered worker {worker.agent_id} with orchestrator")

    def unregister_worker(self, worker_id: str) -> None:
        """
        Unregister a worker agent.

        Args:
            worker_id: ID of worker to unregister
        """
        if worker_id in self.workers:
            del self.workers[worker_id]
            del self.worker_capabilities[worker_id]
            logger.info(f"Unregistered worker {worker_id}")

    async def process_task(self, task: Task) -> Result:
        """
        Process a task by orchestrating worker agents.

        Strategy:
        1. Analyze task requirements
        2. Decompose into subtasks if complex
        3. Match subtasks to capable workers
        4. Execute subtasks in parallel
        5. Synthesize results

        Args:
            task: Task to process

        Returns:
            Synthesized result
        """
        logger.info(f"Orchestrator processing task: {task.description}")

        # Step 1: Analyze task
        analysis = self._analyze_task(task)

        # Step 2: Decompose into subtasks if needed
        if analysis["complexity"] > 0.5 or len(task.requirements) > 1:
            subtasks = self._decompose_task(task)
        else:
            subtasks = [task]

        # Step 3: Delegate to workers
        delegations = self._plan_delegation(subtasks)

        if not delegations:
            logger.warning("No suitable workers found for task")
            return Result(
                task_id=task.id,
                success=False,
                error="No suitable workers available",
            )

        # Step 4: Execute in parallel
        results = await self._execute_parallel(delegations)

        # Step 5: Synthesize results
        final_result = self._synthesize_results(task, results)

        return final_result

    def _analyze_task(self, task: Task) -> Dict[str, Any]:
        """
        Analyze a task to determine complexity and requirements.

        Args:
            task: Task to analyze

        Returns:
            Analysis dictionary
        """
        # Simple analysis based on requirements and description
        complexity = len(task.requirements) / 10.0  # Normalize
        complexity = min(complexity, 1.0)

        return {
            "complexity": complexity,
            "requirement_count": len(task.requirements),
            "description_length": len(task.description),
            "needs_decomposition": complexity > 0.5,
        }

    def _decompose_task(self, task: Task) -> List[Task]:
        """
        Decompose a complex task into subtasks.

        Args:
            task: Task to decompose

        Returns:
            List of subtasks
        """
        subtasks = []

        # If task has explicit requirements, create subtask for each
        if task.requirements:
            for idx, requirement in enumerate(task.requirements):
                subtask = Task(
                    description=f"{task.description} - {requirement}",
                    requirements=[requirement],
                    context=task.context,
                    priority=task.priority,
                    parent_task_id=task.id,
                    metadata={"subtask_index": idx, "parent_task": task.id},
                )
                subtasks.append(subtask)
                task.subtasks.append(subtask.id)
        else:
            # Simple decomposition based on description keywords
            # In a real system, this would use more sophisticated NLP
            keywords = ["research", "code", "test", "analyze", "document"]
            found_keywords = [kw for kw in keywords if kw in task.description.lower()]

            if found_keywords:
                for idx, keyword in enumerate(found_keywords):
                    subtask = Task(
                        description=f"{keyword.capitalize()} for: {task.description}",
                        requirements=[keyword],
                        context=task.context,
                        priority=task.priority,
                        parent_task_id=task.id,
                        metadata={"subtask_index": idx, "focus": keyword},
                    )
                    subtasks.append(subtask)
                    task.subtasks.append(subtask.id)
            else:
                # Can't decompose, return original task
                subtasks = [task]

        logger.info(f"Decomposed task into {len(subtasks)} subtasks")
        return subtasks

    def _plan_delegation(self, subtasks: List[Task]) -> List[tuple[Task, str]]:
        """
        Plan which workers should handle which subtasks.

        Args:
            subtasks: List of subtasks to delegate

        Returns:
            List of (task, worker_id) tuples
        """
        delegations = []

        for subtask in subtasks:
            # Find best worker for this subtask
            best_worker = self._find_best_worker(subtask)

            if best_worker:
                delegations.append((subtask, best_worker))
                logger.debug(f"Delegating subtask {subtask.id} to {best_worker}")
            else:
                logger.warning(f"No suitable worker for subtask {subtask.id}")

        return delegations

    def _find_best_worker(self, task: Task) -> Optional[str]:
        """
        Find the best worker for a task based on capabilities.

        Args:
            task: Task to assign

        Returns:
            Worker ID, or None if no suitable worker
        """
        if not self.workers:
            return None

        # Score each worker based on capability match
        scores = {}

        for worker_id, capabilities in self.worker_capabilities.items():
            worker = self.workers[worker_id]

            # Skip busy workers
            if worker.state.status == "busy":
                continue

            score = 0.0

            # Match task requirements to worker capabilities
            for requirement in task.requirements:
                if requirement in capabilities:
                    # Get proficiency for this capability
                    proficiency = worker.get_capability_proficiency(requirement)
                    score += proficiency

            # Factor in worker's performance score
            score *= worker.state.performance_score

            # Penalize workers with high failure rates
            total_tasks = worker.state.completed_tasks + worker.state.failed_tasks
            if total_tasks > 0:
                success_rate = worker.state.completed_tasks / total_tasks
                score *= success_rate

            scores[worker_id] = score

        if not scores:
            # No workers available, pick any idle one
            for worker_id, worker in self.workers.items():
                if worker.state.status == "idle":
                    return worker_id
            return None

        # Return worker with highest score
        best_worker = max(scores.items(), key=lambda x: x[1])[0]
        return best_worker

    async def _execute_parallel(
        self, delegations: List[tuple[Task, str]]
    ) -> List[Result]:
        """
        Execute multiple tasks in parallel across workers.

        Args:
            delegations: List of (task, worker_id) tuples

        Returns:
            List of results
        """
        logger.info(f"Executing {len(delegations)} tasks in parallel")

        # Create coroutines for each delegation
        coroutines = []
        for task, worker_id in delegations:
            worker = self.workers[worker_id]
            coroutines.append(worker.execute_task(task))

        # Execute all in parallel
        results = await asyncio.gather(*coroutines, return_exceptions=True)

        # Convert exceptions to error results
        processed_results = []
        for idx, result in enumerate(results):
            if isinstance(result, Exception):
                task, worker_id = delegations[idx]
                processed_results.append(
                    Result(
                        task_id=task.id,
                        success=False,
                        error=str(result),
                        agent_id=worker_id,
                    )
                )
            else:
                processed_results.append(result)

        logger.info(f"Completed {len(processed_results)} parallel tasks")
        return processed_results

    def _synthesize_results(self, original_task: Task, results: List[Result]) -> Result:
        """
        Synthesize multiple results into a single result.

        Args:
            original_task: The original task
            results: List of results from subtasks

        Returns:
            Synthesized result
        """
        # Check overall success
        all_success = all(r.success for r in results)

        # Collect all data
        combined_data = {
            "subtask_count": len(results),
            "successful": sum(1 for r in results if r.success),
            "failed": sum(1 for r in results if not r.success),
            "results": [],
        }

        for result in results:
            combined_data["results"].append({
                "task_id": result.task_id,
                "success": result.success,
                "data": result.data,
                "agent_id": result.agent_id,
                "execution_time": result.execution_time,
            })

        # Calculate overall quality score
        if results:
            avg_quality = sum(r.quality_score for r in results) / len(results)
        else:
            avg_quality = 0.0

        # Calculate total execution time
        total_time = max((r.execution_time for r in results), default=0.0)

        synthesized = Result(
            task_id=original_task.id,
            success=all_success,
            data=combined_data,
            agent_id=self.agent_id,
            execution_time=total_time,
            quality_score=avg_quality,
            metadata={
                "synthesis": True,
                "subtask_count": len(results),
            },
        )

        logger.info(
            f"Synthesized {len(results)} results: "
            f"success={all_success}, quality={avg_quality:.2f}"
        )

        return synthesized

    def get_worker_status(self) -> Dict[str, Any]:
        """Get status of all workers."""
        return {
            worker_id: {
                "status": worker.state.status,
                "completed_tasks": worker.state.completed_tasks,
                "failed_tasks": worker.state.failed_tasks,
                "performance_score": worker.state.performance_score,
            }
            for worker_id, worker in self.workers.items()
        }
