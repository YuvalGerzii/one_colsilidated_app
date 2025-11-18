"""
Reinforcement learning example.

This example demonstrates:
- Training the system through multiple episodes
- Policy improvement over time
- Saving and loading learned policies
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from multi_agent_system import MultiAgentSystem


async def main():
    """Run reinforcement learning example."""
    print("=" * 60)
    print("Multi-Agent System - Reinforcement Learning Example")
    print("=" * 60)

    # Initialize system with learning enabled
    print("\n1. Initializing system with RL enabled...")
    mas = MultiAgentSystem(enable_learning=True)
    await mas.start()

    # Training episodes
    num_episodes = 10
    print(f"\n2. Training for {num_episodes} episodes...")

    tasks = [
        "Research machine learning algorithms",
        "Implement a sorting algorithm",
        "Test the implementation with edge cases",
        "Analyze performance data",
        "Research and code a binary search tree",
        "Create unit tests for authentication module",
        "Analyze user behavior patterns",
        "Research database optimization techniques",
        "Implement caching mechanism",
        "Test API endpoints thoroughly",
    ]

    for episode in range(num_episodes):
        print(f"\n--- Episode {episode + 1}/{num_episodes} ---")

        # Execute a task
        task = tasks[episode % len(tasks)]
        result = await mas.execute_task(task)

        print(f"Task: {task}")
        print(f"Success: {result.success}, Time: {result.execution_time:.2f}s")

        # Show learning progress
        if mas.enable_learning:
            orchestrator_engine = mas.learning_engines.get("orchestrator")
            if orchestrator_engine:
                stats = orchestrator_engine.get_statistics()
                print(f"Learning stats:")
                print(f"  Exploration rate: {stats['exploration_rate']:.4f}")
                print(f"  Average reward: {stats['average_reward']:.4f}")
                print(f"  Q-table size: {stats['q_table_size']}")

    # Show final metrics
    print("\n3. Final System Metrics:")
    metrics = mas.get_metrics()
    print(f"  Total tasks: {metrics.total_tasks}")
    print(f"  Success rate: {metrics.success_rate:.2%}")
    print(f"  Average task time: {metrics.average_task_time:.2f}s")

    # Save learned policies
    print("\n4. Saving learned policies...")
    mas.save_policies("./models")
    print("  Policies saved to ./models/")

    # Demonstrate loading policies
    print("\n5. Creating new system and loading policies...")
    mas2 = MultiAgentSystem(enable_learning=True)
    await mas2.start()
    mas2.load_policies("./models")
    print("  Policies loaded successfully!")

    # Test with loaded policies
    print("\n6. Testing with loaded policies...")
    result = await mas2.execute_task("Research and implement a hash table")
    print(f"  Success: {result.success}")
    print(f"  Time: {result.execution_time:.2f}s")

    # Cleanup
    await mas.stop()
    await mas2.stop()

    print("\n" + "=" * 60)
    print("Reinforcement learning example completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
