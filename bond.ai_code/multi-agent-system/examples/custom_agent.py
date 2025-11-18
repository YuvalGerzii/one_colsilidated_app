"""
Custom agent example.

This example demonstrates:
- Creating custom agent types
- Adding custom agents to the system
- Specialized processing logic
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from multi_agent_system import MultiAgentSystem, BaseAgent, AgentCapability
from multi_agent_system.core.types import Task, Result


class SecurityAgent(BaseAgent):
    """
    Custom agent specialized in security analysis.
    """

    def __init__(self, agent_id: str = "security_1", message_bus=None):
        capabilities = [
            AgentCapability("security_analysis", "Analyze security vulnerabilities", 0.95),
            AgentCapability("penetration_testing", "Perform security testing", 0.9),
            AgentCapability("compliance_check", "Check security compliance", 0.85),
        ]
        super().__init__(agent_id, capabilities, message_bus)

    async def process_task(self, task: Task) -> Result:
        """Process security-related tasks."""
        print(f"🔒 {self.agent_id} performing security analysis...")

        # Simulate security analysis
        await asyncio.sleep(0.5)  # Simulate processing time

        security_report = {
            "task": task.description,
            "vulnerabilities_found": [
                "SQL Injection risk in login form",
                "Missing CSRF protection",
                "Weak password policy",
            ],
            "severity": "Medium",
            "recommendations": [
                "Implement parameterized queries",
                "Add CSRF tokens",
                "Enforce strong password requirements",
            ],
            "compliance_status": "Requires attention",
        }

        return Result(
            task_id=task.id,
            success=True,
            data=security_report,
            agent_id=self.agent_id,
            quality_score=0.9,
        )


class DocumentationAgent(BaseAgent):
    """
    Custom agent specialized in documentation.
    """

    def __init__(self, agent_id: str = "doc_writer_1", message_bus=None):
        capabilities = [
            AgentCapability("documentation", "Create comprehensive documentation", 0.9),
            AgentCapability("technical_writing", "Write technical content", 0.85),
        ]
        super().__init__(agent_id, capabilities, message_bus)

    async def process_task(self, task: Task) -> Result:
        """Process documentation tasks."""
        print(f"📝 {self.agent_id} creating documentation...")

        await asyncio.sleep(0.3)

        documentation = {
            "task": task.description,
            "sections": [
                "Overview",
                "Installation",
                "Usage",
                "API Reference",
                "Examples",
                "Troubleshooting",
            ],
            "format": "Markdown",
            "word_count": 2500,
            "quality": "Production-ready",
        }

        return Result(
            task_id=task.id,
            success=True,
            data=documentation,
            agent_id=self.agent_id,
            quality_score=0.88,
        )


async def main():
    """Run custom agent example."""
    print("=" * 60)
    print("Multi-Agent System - Custom Agent Example")
    print("=" * 60)

    # Initialize system
    print("\n1. Initializing system...")
    mas = MultiAgentSystem(enable_learning=False)
    await mas.start()

    # Create and add custom agents
    print("\n2. Adding custom agents...")

    security_agent = SecurityAgent()
    doc_agent = DocumentationAgent()

    mas.add_custom_agent(security_agent)
    mas.add_custom_agent(doc_agent)

    print(f"  Added: {security_agent.agent_id}")
    print(f"  Added: {doc_agent.agent_id}")

    # Execute tasks that will use custom agents
    print("\n3. Executing security analysis task...")
    result = await mas.execute_task(
        "Perform security audit of the authentication system",
        requirements=["security_analysis"]
    )

    print(f"\nSecurity Analysis Results:")
    print(f"  Success: {result.success}")
    if result.data:
        data = result.data.get('results', [{}])[0].get('data', {})
        print(f"  Vulnerabilities: {len(data.get('vulnerabilities_found', []))}")
        print(f"  Severity: {data.get('severity', 'N/A')}")

    print("\n4. Executing documentation task...")
    result = await mas.execute_task(
        "Create comprehensive API documentation",
        requirements=["documentation"]
    )

    print(f"\nDocumentation Results:")
    print(f"  Success: {result.success}")
    if result.data:
        data = result.data.get('results', [{}])[0].get('data', {})
        print(f"  Sections: {len(data.get('sections', []))}")
        print(f"  Format: {data.get('format', 'N/A')}")
        print(f"  Word count: {data.get('word_count', 0)}")

    # Show all agents
    print("\n5. All agents in the system:")
    for agent_id, state in mas.get_agent_states().items():
        print(f"  {agent_id}: {state['status']}")

    await mas.stop()

    print("\n" + "=" * 60)
    print("Custom agent example completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
