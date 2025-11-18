"""
Example: Creating and executing an automation workflow
"""

import asyncio
from uuid import uuid4

from src.automation_fabric.models import (
    WorkflowDefinition,
    AutomationAction,
    ActionType,
)
from src.automation_fabric.engine import AutomationEngine


async def main():
    """Example workflow automation."""

    # Define a workflow for legacy system automation
    workflow = WorkflowDefinition(
        name="Daily Report Generation",
        description="Automate daily report generation from legacy ERP",
        actions=[
            AutomationAction(
                action_type=ActionType.NAVIGATE,
                target="https://legacy-erp.example.com/login",
            ),
            AutomationAction(
                action_type=ActionType.TYPE,
                target="#username",
                value="admin",
            ),
            AutomationAction(
                action_type=ActionType.TYPE,
                target="#password",
                value="password123",
            ),
            AutomationAction(
                action_type=ActionType.CLICK,
                target="#login-button",
            ),
            AutomationAction(
                action_type=ActionType.NAVIGATE,
                target="https://legacy-erp.example.com/reports",
            ),
            AutomationAction(
                action_type=ActionType.CLICK,
                target="#generate-report",
            ),
            AutomationAction(
                action_type=ActionType.EXTRACT,
                target=".report-data",
            ),
        ],
    )

    # Execute workflow
    engine = AutomationEngine()
    await engine.initialize()

    print(f"Executing workflow: {workflow.name}")
    execution = await engine.execute_workflow(workflow)

    print(f"Workflow status: {execution.status}")
    print(f"Execution logs: {execution.logs}")

    await engine.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
