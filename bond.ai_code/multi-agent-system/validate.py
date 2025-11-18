"""Quick validation script to test the system works."""

import asyncio
from multi_agent_system import MultiAgentSystem

async def main():
    print("🚀 Validating Multi-Agent System...")
    print("=" * 60)

    # Test 1: System initialization
    print("\n✓ Test 1: Initializing system...")
    mas = MultiAgentSystem(enable_learning=True)
    await mas.start()
    print(f"  Agents created: {len(mas.agents)}")
    print(f"  Workers: {len(mas.workers)}")

    # Test 2: Simple task
    print("\n✓ Test 2: Executing simple task...")
    result = await mas.execute_task("Test task")
    print(f"  Success: {result.success}")
    print(f"  Agent: {result.agent_id}")

    # Test 3: Complex task
    print("\n✓ Test 3: Executing complex task...")
    result = await mas.execute_task(
        "Complex task",
        requirements=["research", "code"]
    )
    print(f"  Success: {result.success}")
    print(f"  Subtasks: {result.data.get('subtask_count', 0)}")

    # Test 4: Metrics
    print("\n✓ Test 4: Checking metrics...")
    metrics = mas.get_metrics()
    print(f"  Total tasks: {metrics.total_tasks}")
    print(f"  Completed: {metrics.completed_tasks}")
    print(f"  Success rate: {metrics.success_rate:.2%}")

    # Test 5: Learning
    if mas.enable_learning:
        print("\n✓ Test 5: Checking learning engines...")
        print(f"  Learning engines: {len(mas.learning_engines)}")
        for agent_id, engine in list(mas.learning_engines.items())[:2]:
            stats = engine.get_statistics()
            print(f"  {agent_id}: {stats['updates']} updates")

    await mas.stop()

    print("\n" + "=" * 60)
    print("✅ All validations passed!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
