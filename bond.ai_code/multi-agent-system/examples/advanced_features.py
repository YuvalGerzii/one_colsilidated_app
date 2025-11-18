"""
Advanced features demonstration.

Showcases enhancements based on 2025 best practices:
- Semantic memory with context retrieval
- Model Context Protocol (MCP) patterns
- Policy gradient learning with human feedback
- Observability and monitoring
- Dynamic scaling and resilience
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from multi_agent_system import MultiAgentSystem
from multi_agent_system.memory.semantic_memory import SemanticMemory
from multi_agent_system.core.context_protocol import (
    ContextProtocol,
    ContextType,
    ContextScope,
)
from multi_agent_system.learning.policy_gradient import PolicyGradientEngine
from multi_agent_system.observability.monitor import SystemMonitor, EventType
from multi_agent_system.core.scaling import ScalingStrategy, TaskComplexity
from multi_agent_system.core.resilience import ResilientExecutor, RetryStrategy


async def demo_semantic_memory():
    """Demonstrate semantic memory with context-aware retrieval."""
    print("\n" + "=" * 60)
    print("1. SEMANTIC MEMORY DEMONSTRATION")
    print("=" * 60)

    memory = SemanticMemory(agent_id="demo_agent", embedding_dim=384)

    # Store some memories
    print("\nStoring memories...")
    memory.store(
        "ml_research_2024",
        "Research on transformer architectures and attention mechanisms",
        context={"domain": "AI", "year": 2024},
        importance=0.9,
    )

    memory.store(
        "python_optimization",
        "Optimizing Python code with async/await and multiprocessing",
        context={"domain": "Engineering", "language": "Python"},
        importance=0.7,
    )

    memory.store(
        "distributed_systems",
        "Building scalable distributed systems with microservices",
        context={"domain": "Engineering", "type": "Architecture"},
        importance=0.8,
    )

    # Semantic retrieval
    print("\nRetrieving memories semantically...")
    query = "machine learning and AI algorithms"
    results = memory.retrieve_by_similarity(query, top_k=3)

    for key, content, score in results:
        print(f"  [{score:.3f}] {key}: {str(content)[:60]}...")

    # Context-aware retrieval
    print("\nContext-aware retrieval...")
    context = {"domain": "Engineering"}
    results = memory.retrieve_contextual(
        "optimization techniques", context, top_k=2
    )

    for key, content, relevance in results:
        print(f"  [{relevance:.3f}] {key}: {str(content)[:60]}...")

    stats = memory.get_statistics()
    print(f"\nMemory stats: {stats['current_memories']} memories stored")


async def demo_context_protocol():
    """Demonstrate Model Context Protocol (MCP) patterns."""
    print("\n" + "=" * 60)
    print("2. CONTEXT PROTOCOL DEMONSTRATION")
    print("=" * 60)

    protocol = ContextProtocol(max_contexts=100)

    # Store contexts at different scopes
    print("\nStoring contexts...")

    # Private context for specific agent
    protocol.store_context(
        agent_id="agent_1",
        context_type=ContextType.TASK,
        content={"current_task": "research", "progress": 0.5},
        scope=ContextScope.PRIVATE,
        importance=0.8,
    )

    # Shared context for team
    protocol.store_context(
        agent_id="agent_1",
        context_type=ContextType.DOMAIN,
        content={"domain": "AI/ML", "expertise_level": "advanced"},
        scope=ContextScope.SHARED,
        importance=0.9,
    )

    # Global system context
    protocol.store_context(
        agent_id="system",
        context_type=ContextType.SYSTEM,
        content={"version": "2.0", "features": ["semantic_memory", "mcp"]},
        scope=ContextScope.GLOBAL,
        importance=1.0,
    )

    # Retrieve relevant context
    print("\nRetrieving relevant context...")
    contexts = protocol.retrieve_relevant_context(
        agent_id="agent_1",
        query="machine learning tasks",
        top_k=3,
    )

    for entry in contexts:
        print(
            f"  [{entry.relevance_score:.2f}] {entry.type.value} "
            f"({entry.scope.value}): {entry.content}"
        )

    stats = protocol.get_statistics()
    print(f"\nContext stats: {stats['total_contexts']} total contexts")


async def demo_policy_gradient():
    """Demonstrate policy gradient learning with human feedback."""
    print("\n" + "=" * 60)
    print("3. POLICY GRADIENT LEARNING DEMONSTRATION")
    print("=" * 60)

    engine = PolicyGradientEngine(
        agent_id="learner",
        learning_rate=0.01,
        discount_factor=0.95,
    )

    print("\nTraining with policy gradient...")

    # Simulate a simple environment
    for episode in range(5):
        state = {"position": 0, "goal": 10}
        available_actions = ["move_forward", "move_backward", "stay"]

        # Collect episode experience
        for step in range(10):
            # Select action using policy
            action = engine.select_action(state, available_actions)

            # Simulate environment
            next_state = state.copy()
            if action == "move_forward":
                next_state["position"] += 1
                reward = 1.0 if next_state["position"] == state["goal"] else 0.1
            elif action == "move_backward":
                next_state["position"] -= 1
                reward = -0.1
            else:  # stay
                reward = 0.0

            # Store experience
            from multi_agent_system.core.types import Experience

            exp = Experience(
                agent_id="learner",
                state=state,
                action=action,
                reward=reward,
                next_state=next_state,
                done=(next_state["position"] == state["goal"]),
            )
            engine.add_experience(exp)

            state = next_state

            if exp.done:
                break

        # Update policy at end of episode
        metrics = engine.end_episode()
        print(
            f"  Episode {episode + 1}: Return={metrics.get('episode_return', 0):.2f}, "
            f"Entropy={metrics.get('entropy', 0):.3f}"
        )

    # Add human feedback
    print("\nAdding human feedback...")
    engine.add_human_feedback(
        state={"position": 5, "goal": 10},
        action="move_forward",
        preference=1.0,  # Positive feedback
    )

    stats = engine.get_statistics()
    print(
        f"\nLearning stats: {stats['episodes']} episodes, "
        f"{stats['updates']} updates, "
        f"avg reward={stats['average_reward']:.2f}"
    )


async def demo_monitoring():
    """Demonstrate observability and monitoring."""
    print("\n" + "=" * 60)
    print("4. MONITORING & OBSERVABILITY DEMONSTRATION")
    print("=" * 60)

    monitor = SystemMonitor(retention_hours=1)

    print("\nSimulating traced operations...")

    # Trace a distributed task
    trace_id = "trace_001"

    # Orchestrator span
    monitor.start_span(
        trace_id=trace_id,
        span_id="span_orchestrator",
        parent_span_id=None,
        agent_id="orchestrator",
        event_type=EventType.TASK_START,
        metadata={"task": "complex_analysis"},
    )

    # Worker spans (parallel)
    for i in range(3):
        worker_span_id = f"span_worker_{i}"
        monitor.start_span(
            trace_id=trace_id,
            span_id=worker_span_id,
            parent_span_id="span_orchestrator",
            agent_id=f"worker_{i}",
            event_type=EventType.TASK_START,
            metadata={"subtask": f"subtask_{i}"},
        )

        # Simulate work
        await asyncio.sleep(0.1)

        # End worker span
        monitor.end_span(worker_span_id, success=True)

    # End orchestrator span
    monitor.end_span("span_orchestrator", success=True)

    # Record some metrics
    monitor.record_metric("task_duration_ms", 150.5)
    monitor.record_metric("queue_size", 5)

    # Get trace
    print("\nTrace events:")
    events = monitor.get_trace(trace_id)
    for event in events:
        print(
            f"  {event.agent_id} - {event.event_type.value} "
            f"({event.duration_ms:.2f}ms)"
        )

    # Get system metrics
    print("\nSystem metrics:")
    metrics = monitor.get_system_metrics()
    for key, value in metrics.items():
        print(f"  {key}: {value}")

    # Performance report
    print("\n" + monitor.get_performance_report())


async def demo_scaling():
    """Demonstrate dynamic agent scaling."""
    print("\n" + "=" * 60)
    print("5. DYNAMIC SCALING DEMONSTRATION")
    print("=" * 60)

    strategy = ScalingStrategy()

    # Test different complexity tasks
    from multi_agent_system.core.types import Task

    tasks = [
        Task(description="Simple fact retrieval", requirements=["research"]),
        Task(
            description="Comprehensive analysis of ML algorithms",
            requirements=["research", "analyze", "document"],
        ),
        Task(
            description="Build distributed system with microservices, testing, documentation, and deployment",
            requirements=[
                "research",
                "code",
                "test",
                "document",
                "deploy",
                "monitor",
                "optimize",
            ],
        ),
    ]

    for task in tasks:
        complexity = strategy.assess_complexity(task)
        allocation = strategy.get_agent_allocation(task, available_agents=10)

        print(f"\nTask: {task.description[:50]}...")
        print(f"  Complexity: {complexity.value}")
        print(f"  Recommended agents: {allocation['recommended_agents']}")
        print(f"  Tool calls per agent: {allocation['max_tool_calls_per_agent']}")
        print(f"  Parallel execution: {allocation['parallel_execution']}")
        print(f"  Estimated speedup: {allocation['estimated_speedup']:.1f}x")


async def demo_resilience():
    """Demonstrate error recovery and resilience."""
    print("\n" + "=" * 60)
    print("6. RESILIENCE & ERROR RECOVERY DEMONSTRATION")
    print("=" * 60)

    executor = ResilientExecutor(max_retries=3, initial_delay=0.1)

    # Test retry mechanism
    print("\nTesting retry with exponential backoff...")
    attempt_count = [0]

    async def flaky_operation():
        attempt_count[0] += 1
        print(f"  Attempt {attempt_count[0]}...")
        if attempt_count[0] < 3:
            raise Exception("Temporary failure")
        return "Success!"

    try:
        result = await executor.execute_with_retry(
            flaky_operation, retry_strategy=RetryStrategy.EXPONENTIAL_BACKOFF
        )
        print(f"  Result: {result}")
    except Exception as e:
        print(f"  Failed: {e}")

    # Test circuit breaker
    print("\nTesting circuit breaker...")

    failure_count = [0]

    async def unstable_operation():
        failure_count[0] += 1
        if failure_count[0] <= 5:  # Fail first 5 times
            raise Exception("Service unavailable")
        return "Success!"

    for i in range(8):
        try:
            result = await executor.execute_with_circuit_breaker(
                "external_service", unstable_operation
            )
            print(f"  Call {i + 1}: {result}")
        except Exception as e:
            print(f"  Call {i + 1}: Failed - {str(e)[:50]}")

        await asyncio.sleep(0.05)

    # Test fallback
    print("\nTesting fallback mechanism...")

    async def primary_operation():
        raise Exception("Primary failed")

    async def fallback_operation():
        return "Fallback result"

    result = await executor.execute_with_fallback(
        primary_operation, fallback_operation
    )
    print(f"  Result: {result}")


async def main():
    """Run all advanced feature demos."""
    print("\n" + "=" * 60)
    print("MULTI-AGENT SYSTEM - ADVANCED FEATURES (2025)")
    print("=" * 60)

    await demo_semantic_memory()
    await demo_context_protocol()
    await demo_policy_gradient()
    await demo_monitoring()
    await demo_scaling()
    await demo_resilience()

    print("\n" + "=" * 60)
    print("All advanced features demonstrated successfully!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
