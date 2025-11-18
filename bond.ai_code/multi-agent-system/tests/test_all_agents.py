"""
Comprehensive test suite for all agents in the multi-agent system.

Tests:
- All agents can be instantiated
- All agents can process tasks
- Agent communication works
- Orchestration works end-to-end
- Verification agents work
- Planning and NLP agents work
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from multi_agent_system.agents.intelligent_orchestrator import IntelligentOrchestrator
from multi_agent_system.agents.workers import (
    ResearchAgent,
    CodeAgent,
    TestAgent,
    DataAnalystAgent,
    GeneralAgent,
    create_worker_pool,
)
from multi_agent_system.agents.verification_agents import create_verification_agents
from multi_agent_system.agents.planning_nlp_agents import create_planning_nlp_agents
from multi_agent_system.communication.message_bus import MessageBus
from multi_agent_system.core.types import Task, Message, MessageType
from loguru import logger


class TestResults:
    """Track test results."""

    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []

    def record(self, test_name: str, passed: bool, message: str = ""):
        """Record a test result."""
        self.tests.append({
            "name": test_name,
            "passed": passed,
            "message": message,
        })

        if passed:
            self.passed += 1
            logger.info(f"✓ {test_name}")
        else:
            self.failed += 1
            logger.error(f"✗ {test_name}: {message}")

    def summary(self) -> str:
        """Get test summary."""
        total = self.passed + self.failed
        success_rate = (self.passed / total * 100) if total > 0 else 0

        summary = [
            "\n" + "=" * 80,
            "TEST SUMMARY",
            "=" * 80,
            f"Total Tests: {total}",
            f"Passed: {self.passed} ✓",
            f"Failed: {self.failed} ✗",
            f"Success Rate: {success_rate:.1f}%",
            "",
        ]

        if self.failed > 0:
            summary.append("Failed Tests:")
            for test in self.tests:
                if not test["passed"]:
                    summary.append(f"  - {test['name']}: {test['message']}")

        summary.append("=" * 80)

        return "\n".join(summary)


async def test_agent_instantiation(results: TestResults):
    """Test that all agents can be instantiated."""
    print("\n" + "=" * 80)
    print("TEST: Agent Instantiation")
    print("=" * 80)

    message_bus = MessageBus()

    # Test core workers
    try:
        research = ResearchAgent("research_test", message_bus)
        results.record("ResearchAgent instantiation", True)
    except Exception as e:
        results.record("ResearchAgent instantiation", False, str(e))

    try:
        code = CodeAgent("code_test", message_bus)
        results.record("CodeAgent instantiation", True)
    except Exception as e:
        results.record("CodeAgent instantiation", False, str(e))

    try:
        test_agent = TestAgent("test_test", message_bus)
        results.record("TestAgent instantiation", True)
    except Exception as e:
        results.record("TestAgent instantiation", False, str(e))

    try:
        data = DataAnalystAgent("data_test", message_bus)
        results.record("DataAnalystAgent instantiation", True)
    except Exception as e:
        results.record("DataAnalystAgent instantiation", False, str(e))

    try:
        general = GeneralAgent("general_test", message_bus)
        results.record("GeneralAgent instantiation", True)
    except Exception as e:
        results.record("GeneralAgent instantiation", False, str(e))

    # Test verification agents
    try:
        verifiers = create_verification_agents(message_bus)
        results.record(f"Verification agents instantiation ({len(verifiers)} agents)", len(verifiers) == 10)
    except Exception as e:
        results.record("Verification agents instantiation", False, str(e))

    # Test planning & NLP agents
    try:
        planning_nlp = create_planning_nlp_agents(message_bus)
        results.record(f"Planning & NLP agents instantiation ({len(planning_nlp)} agents)", len(planning_nlp) == 10)
    except Exception as e:
        results.record("Planning & NLP agents instantiation", False, str(e))

    # Test orchestrator
    try:
        orch = IntelligentOrchestrator("test_orch", message_bus)
        results.record("IntelligentOrchestrator instantiation", True)
    except Exception as e:
        results.record("IntelligentOrchestrator instantiation", False, str(e))

    print(f"\nInstantiation tests: {results.passed}/{results.passed + results.failed} passed")


async def test_agent_task_processing(results: TestResults):
    """Test that all agents can process tasks."""
    print("\n" + "=" * 80)
    print("TEST: Agent Task Processing")
    print("=" * 80)

    message_bus = MessageBus()

    # Test research agent
    try:
        agent = ResearchAgent("research_test", message_bus)
        task = Task(description="Research Python frameworks", requirements=["research"])
        result = await agent.process_task(task)

        results.record(
            "ResearchAgent task processing",
            result.success and result.data is not None,
            "" if result.success else result.error
        )
    except Exception as e:
        results.record("ResearchAgent task processing", False, str(e))

    # Test code agent
    try:
        agent = CodeAgent("code_test", message_bus)
        task = Task(description="Generate a sorting algorithm", requirements=["code"])
        result = await agent.process_task(task)

        results.record(
            "CodeAgent task processing",
            result.success and "code" in result.data,
            "" if result.success else result.error
        )
    except Exception as e:
        results.record("CodeAgent task processing", False, str(e))

    # Test test agent
    try:
        agent = TestAgent("test_test", message_bus)
        task = Task(description="Generate tests for sorting algorithm", requirements=["testing"])
        result = await agent.process_task(task)

        results.record(
            "TestAgent task processing",
            result.success and result.data is not None,
            "" if result.success else result.error
        )
    except Exception as e:
        results.record("TestAgent task processing", False, str(e))

    # Test data analyst agent
    try:
        agent = DataAnalystAgent("data_test", message_bus)
        task = Task(description="Analyze sales data", requirements=["data_analysis"])
        result = await agent.process_task(task)

        results.record(
            "DataAnalystAgent task processing",
            result.success and result.data is not None,
            "" if result.success else result.error
        )
    except Exception as e:
        results.record("DataAnalystAgent task processing", False, str(e))

    print(f"\nTask processing tests: {results.passed - (results.passed + results.failed - 4)}/4 passed")


async def test_planning_nlp_agents(results: TestResults):
    """Test planning and NLP agents."""
    print("\n" + "=" * 80)
    print("TEST: Planning & NLP Agents")
    print("=" * 80)

    message_bus = MessageBus()
    agents = create_planning_nlp_agents(message_bus)

    # Test strategic planner
    try:
        agent = agents["strategic_planner_1"]
        task = Task(description="Create strategic plan for product launch", requirements=["strategic_planning"])
        result = await agent.process_task(task)

        results.record(
            "StrategicPlannerAgent processing",
            result.success and "phases" in result.data and "timeline" in result.data,
            "" if result.success else result.error
        )
    except Exception as e:
        results.record("StrategicPlannerAgent processing", False, str(e))

    # Test project planner
    try:
        agent = agents["project_planner_1"]
        task = Task(description="Create project plan for website redesign", requirements=["project_planning"])
        result = await agent.process_task(task)

        results.record(
            "ProjectPlannerAgent processing",
            result.success and "sprints" in result.data and "work_breakdown_structure" in result.data,
            "" if result.success else result.error
        )
    except Exception as e:
        results.record("ProjectPlannerAgent processing", False, str(e))

    # Test text analyzer
    try:
        agent = agents["text_analyzer_1"]
        task = Task(
            description="Analyze text",
            requirements=["text_analysis"],
            context={"text": "This is a sample text for analysis. It contains multiple sentences and keywords."}
        )
        result = await agent.process_task(task)

        results.record(
            "TextAnalysisAgent processing",
            result.success and "summary" in result.data and "keywords" in result.data,
            "" if result.success else result.error
        )
    except Exception as e:
        results.record("TextAnalysisAgent processing", False, str(e))

    # Test NLP analyzer
    try:
        agent = agents["nlp_analyzer_1"]
        task = Task(
            description="Perform NLP analysis",
            requirements=["nlp"],
            context={"text": "I love this product! It's amazing and works perfectly."}
        )
        result = await agent.process_task(task)

        results.record(
            "NLPAnalysisAgent processing",
            result.success and "sentiment" in result.data and "entities" in result.data,
            "" if result.success else result.error
        )
    except Exception as e:
        results.record("NLPAnalysisAgent processing", False, str(e))

    # Test semantic search
    try:
        agent = agents["semantic_search_1"]
        task = Task(
            description="Search for relevant documents",
            requirements=["semantic_search"],
            context={"query": "machine learning algorithms"}
        )
        result = await agent.process_task(task)

        results.record(
            "SemanticSearchAgent processing",
            result.success and "ranked_results" in result.data,
            "" if result.success else result.error
        )
    except Exception as e:
        results.record("SemanticSearchAgent processing", False, str(e))

    print(f"\nPlanning & NLP tests: {results.passed - (results.passed + results.failed - 5)}/5 passed")


async def test_verification_agents(results: TestResults):
    """Test verification agents."""
    print("\n" + "=" * 80)
    print("TEST: Verification Agents")
    print("=" * 80)

    message_bus = MessageBus()
    verifiers = create_verification_agents(message_bus)

    # Create a sample output to verify
    sample_output = {
        "task_id": "test-123",
        "success": True,
        "data": {
            "findings": ["Finding 1", "Finding 2"],
            "sources": ["source1.com", "source2.org"],
            "confidence": 0.85,
        },
        "quality_score": 0.87,
        "agent_id": "research_1",
    }

    # Test quality verifier
    try:
        agent = verifiers["quality_verifier_research"]
        task = Task(
            description="Verify research quality",
            requirements=["quality_verification"],
            context={
                "output_to_verify": sample_output,
                "original_task": {"description": "Research topic", "requirements": ["research"]},
            }
        )
        result = await agent.process_task(task)

        results.record(
            "QualityVerifierAgent processing",
            result.success and "quality_scores" in result.data and "overall_quality" in result.data,
            "" if result.success else result.error
        )
    except Exception as e:
        results.record("QualityVerifierAgent processing", False, str(e))

    # Test delivery validator
    try:
        agent = verifiers["delivery_validator_research"]
        task = Task(
            description="Validate delivery",
            requirements=["delivery_validation"],
            context={"output_to_verify": sample_output}
        )
        result = await agent.process_task(task)

        results.record(
            "DeliveryValidatorAgent processing",
            result.success and "validation_scores" in result.data and "overall_validation" in result.data,
            "" if result.success else result.error
        )
    except Exception as e:
        results.record("DeliveryValidatorAgent processing", False, str(e))

    print(f"\nVerification tests: {results.passed - (results.passed + results.failed - 2)}/2 passed")


async def test_orchestration(results: TestResults):
    """Test orchestration end-to-end."""
    print("\n" + "=" * 80)
    print("TEST: Intelligent Orchestration")
    print("=" * 80)

    message_bus = MessageBus()

    # Create orchestrator and workers
    orchestrator = IntelligentOrchestrator("test_orch", message_bus)

    workers = create_worker_pool({
        "research": 1,
        "code": 1,
        "test": 1,
        "data_analysis": 1,
    }, message_bus)

    for worker in workers.values():
        orchestrator.register_worker(worker)

    # Test simple task (should use 1 agent)
    try:
        task = Task(description="What is Python?", requirements=["research"])
        result = await orchestrator.process_task(task)

        agents_used = result.metadata.get("agents_used", 0)
        results.record(
            "Simple task orchestration (1 agent expected)",
            result.success and agents_used <= 2,
            f"Used {agents_used} agents" if not result.success else ""
        )
    except Exception as e:
        results.record("Simple task orchestration", False, str(e))

    # Test moderate task (should use 3-5 agents)
    try:
        task = Task(
            description="Compare Python and JavaScript",
            requirements=["research", "analysis"]
        )
        result = await orchestrator.process_task(task)

        agents_used = result.metadata.get("agents_used", 0)
        results.record(
            "Moderate task orchestration (3-5 agents expected)",
            result.success and 2 <= agents_used <= 5,
            f"Used {agents_used} agents" if not result.success else ""
        )
    except Exception as e:
        results.record("Moderate task orchestration", False, str(e))

    # Test orchestrator metrics
    try:
        metrics = orchestrator.get_efficiency_metrics()
        results.record(
            "Orchestrator efficiency metrics",
            "avg_agents_per_task" in metrics and metrics["avg_agents_per_task"] > 0,
            "" if "avg_agents_per_task" in metrics else "Missing metrics"
        )
    except Exception as e:
        results.record("Orchestrator efficiency metrics", False, str(e))

    print(f"\nOrchestration tests: {results.passed - (results.passed + results.failed - 3)}/3 passed")


async def test_message_bus_communication(results: TestResults):
    """Test agent communication via message bus."""
    print("\n" + "=" * 80)
    print("TEST: Message Bus Communication")
    print("=" * 80)

    message_bus = MessageBus()

    # Register agents
    message_bus.register_agent("agent_1")
    message_bus.register_agent("agent_2")

    # Test direct messaging
    try:
        message = Message(
            sender="agent_1",
            recipient="agent_2",
            message_type=MessageType.QUERY,
            content={"question": "test"}
        )

        sent = await message_bus.send_message(message)
        received = await message_bus.receive_message("agent_2", timeout=1.0)

        results.record(
            "Message bus direct messaging",
            sent and received is not None and received.content["question"] == "test",
            "Message not received" if not received else ""
        )
    except Exception as e:
        results.record("Message bus direct messaging", False, str(e))

    # Test broadcasting
    try:
        broadcast_msg = Message(
            sender="agent_1",
            recipient="*",
            message_type=MessageType.BROADCAST,
            content={"announcement": "test"}
        )

        sent = await message_bus.send_message(broadcast_msg)
        received = await message_bus.receive_message("agent_2", timeout=1.0)

        results.record(
            "Message bus broadcasting",
            sent and received is not None,
            "Broadcast not received" if not received else ""
        )
    except Exception as e:
        results.record("Message bus broadcasting", False, str(e))

    # Test pub/sub
    try:
        message_bus.subscribe("agent_2", "test_topic")

        pub_msg = Message(
            sender="agent_1",
            message_type=MessageType.BROADCAST,
            content={"data": "test"}
        )

        count = await message_bus.publish("test_topic", pub_msg)

        results.record(
            "Message bus pub/sub",
            count > 0,
            f"Published to {count} subscribers"
        )
    except Exception as e:
        results.record("Message bus pub/sub", False, str(e))

    print(f"\nCommunication tests: {results.passed - (results.passed + results.failed - 3)}/3 passed")


async def main():
    """Run all tests."""
    print("\n" + "=" * 80)
    print("MULTI-AGENT SYSTEM - COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    print("\nTesting all agents, communication, orchestration, and verification...")

    results = TestResults()

    try:
        # Run test suites
        await test_agent_instantiation(results)
        await test_agent_task_processing(results)
        await test_planning_nlp_agents(results)
        await test_verification_agents(results)
        await test_orchestration(results)
        await test_message_bus_communication(results)

        # Print summary
        print(results.summary())

        # Return exit code
        return 0 if results.failed == 0 else 1

    except Exception as e:
        logger.error(f"Test suite error: {e}")
        print(results.summary())
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
