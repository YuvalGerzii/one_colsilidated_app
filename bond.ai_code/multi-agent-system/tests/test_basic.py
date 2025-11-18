"""
Basic tests for the Multi-Agent System.
"""

import asyncio
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from multi_agent_system import MultiAgentSystem, Task, AgentCapability


@pytest.mark.asyncio
async def test_system_initialization():
    """Test that system initializes correctly."""
    mas = MultiAgentSystem(enable_learning=False)
    await mas.start()

    assert mas.running is True
    assert len(mas.agents) > 0
    assert mas.orchestrator is not None

    await mas.stop()
    assert mas.running is False


@pytest.mark.asyncio
async def test_simple_task_execution():
    """Test executing a simple task."""
    mas = MultiAgentSystem(enable_learning=False)
    await mas.start()

    result = await mas.execute_task("Test task")

    assert result is not None
    assert result.success is True
    assert result.task_id is not None

    await mas.stop()


@pytest.mark.asyncio
async def test_complex_task_with_requirements():
    """Test executing a complex task with requirements."""
    mas = MultiAgentSystem(enable_learning=False)
    await mas.start()

    result = await mas.execute_task(
        "Complex task with multiple requirements",
        requirements=["research", "code", "test"]
    )

    assert result is not None
    assert result.success is True
    assert result.data is not None
    assert "subtask_count" in result.data

    await mas.stop()


@pytest.mark.asyncio
async def test_add_custom_agent():
    """Test adding a custom agent."""
    mas = MultiAgentSystem(enable_learning=False)
    await mas.start()

    initial_count = len(mas.agents)

    # Add a new agent
    agent_id = mas.add_agent(
        "custom_agent",
        capabilities=["custom_capability"]
    )

    assert agent_id == "custom_agent"
    assert len(mas.agents) == initial_count + 1
    assert "custom_agent" in mas.agents

    await mas.stop()


@pytest.mark.asyncio
async def test_system_metrics():
    """Test system metrics tracking."""
    mas = MultiAgentSystem(enable_learning=False)
    await mas.start()

    # Execute some tasks
    await mas.execute_task("Task 1")
    await mas.execute_task("Task 2")

    metrics = mas.get_metrics()

    assert metrics.total_tasks == 2
    assert metrics.completed_tasks >= 0
    assert metrics.success_rate >= 0.0

    await mas.stop()


def test_task_creation():
    """Test task creation."""
    task = Task(
        description="Test task",
        requirements=["req1", "req2"],
        priority=5
    )

    assert task.description == "Test task"
    assert len(task.requirements) == 2
    assert task.priority == 5
    assert task.id is not None


if __name__ == "__main__":
    # Run tests
    print("Running basic tests...")

    asyncio.run(test_system_initialization())
    print("✓ System initialization test passed")

    asyncio.run(test_simple_task_execution())
    print("✓ Simple task execution test passed")

    asyncio.run(test_complex_task_with_requirements())
    print("✓ Complex task execution test passed")

    asyncio.run(test_add_custom_agent())
    print("✓ Add custom agent test passed")

    asyncio.run(test_system_metrics())
    print("✓ System metrics test passed")

    test_task_creation()
    print("✓ Task creation test passed")

    print("\n✅ All tests passed!")
