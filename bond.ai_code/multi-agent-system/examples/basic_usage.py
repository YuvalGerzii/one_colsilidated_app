"""
Basic usage example of the Multi-Agent System.

This example demonstrates:
- System initialization
- Simple task execution
- Result retrieval
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from multi_agent_system import MultiAgentSystem


async def main():
    """Run basic usage example."""
    print("=" * 60)
    print("Multi-Agent System - Basic Usage Example")
    print("=" * 60)

    # Initialize the system
    print("\n1. Initializing Multi-Agent System...")
    mas = MultiAgentSystem(enable_learning=True)

    # Start the system
    print("2. Starting the system...")
    await mas.start()

    # Execute a simple task
    print("\n3. Executing a simple task...")
    result = await mas.execute_task(
        "Research the latest trends in artificial intelligence"
    )

    print(f"\nTask completed!")
    print(f"  Success: {result.success}")
    print(f"  Agent: {result.agent_id}")
    print(f"  Execution time: {result.execution_time:.2f}s")
    print(f"  Quality score: {result.quality_score:.2f}")
    print(f"  Data: {result.data}")

    # Execute a more complex task
    print("\n4. Executing a complex task with multiple requirements...")
    result = await mas.execute_task(
        "Create a web scraper for news articles with comprehensive testing",
        requirements=["research", "code", "test"]
    )

    print(f"\nComplex task completed!")
    print(f"  Success: {result.success}")
    print(f"  Execution time: {result.execution_time:.2f}s")
    print(f"  Subtasks processed: {result.data.get('subtask_count', 0)}")
    print(f"  Successful subtasks: {result.data.get('successful', 0)}")
    print(f"  Failed subtasks: {result.data.get('failed', 0)}")

    # Show system metrics
    print("\n5. System Metrics:")
    metrics = mas.get_metrics()
    print(f"  Total tasks: {metrics.total_tasks}")
    print(f"  Completed: {metrics.completed_tasks}")
    print(f"  Failed: {metrics.failed_tasks}")
    print(f"  Success rate: {metrics.success_rate:.2%}")

    # Show agent states
    print("\n6. Agent States:")
    states = mas.get_agent_states()
    for agent_id, state in states.items():
        print(f"  {agent_id}:")
        print(f"    Status: {state['status']}")
        print(f"    Completed tasks: {state['completed_tasks']}")
        print(f"    Performance score: {state['performance_score']:.2f}")

    # Stop the system
    print("\n7. Stopping the system...")
    await mas.stop()

    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
