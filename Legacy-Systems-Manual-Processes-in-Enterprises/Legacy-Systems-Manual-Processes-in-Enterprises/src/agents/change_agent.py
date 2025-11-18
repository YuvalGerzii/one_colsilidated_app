"""
Change Management Agent

Manages organizational change during digital transformation.
Handles stakeholder communication, training, and adoption tracking.

Uses 100% FREE local LLMs - NO API costs!
"""

from typing import Dict, Any, List
from src.agents.framework import BaseAgent, AgentRole, AgentTask, AgentResult, AgentStatus
from loguru import logger


class ChangeManagementAgent(BaseAgent):
    """Manages organizational change and adoption during transformation."""

    def __init__(self):
        super().__init__("change-management", AgentRole.ADVISORY)

    def get_capabilities(self) -> List[str]:
        return [
            "assess_change_impact",
            "create_communication_plan",
            "design_training_program",
            "track_adoption_metrics",
            "manage_resistance",
        ]

    async def execute(self, task: AgentTask) -> AgentResult:
        self.status = AgentStatus.WORKING

        try:
            input_data = task.input_data
            change_scope = input_data.get("change_scope", "digital_transformation")
            affected_users = input_data.get("affected_users", 100)
            departments = input_data.get("departments", [])

            # Assess impact
            impact_assessment = await self._assess_impact(change_scope, affected_users, departments)

            # Create communication plan
            comm_plan = self._create_communication_plan(impact_assessment)

            # Design training
            training_plan = self._design_training(affected_users)

            # Adoption strategy
            adoption_strategy = await self._create_adoption_strategy(impact_assessment)

            output = {
                "impact_assessment": impact_assessment,
                "communication_plan": comm_plan,
                "training_plan": training_plan,
                "adoption_strategy": adoption_strategy,
            }

            self.status = AgentStatus.IDLE

            return AgentResult(
                task_id=task.id,
                agent_id=self.agent_id,
                status=AgentStatus.COMPLETED,
                output=output,
                confidence=0.85,
                reasoning="Change management plan based on enterprise transformation best practices",
                recommendations=self._generate_recommendations(output),
                next_steps=["Secure executive sponsorship", "Launch communication campaign", "Begin training"]
            )

        except Exception as e:
            logger.error(f"Change management failed: {e}")
            self.status = AgentStatus.IDLE
            return AgentResult(
                task_id=task.id,
                agent_id=self.agent_id,
                status=AgentStatus.FAILED,
                output={"error": str(e)},
                confidence=0.0,
                reasoning=f"Failed: {e}",
                recommendations=[],
                next_steps=[]
            )

    async def _assess_impact(self, scope: str, users: int, departments: List) -> Dict[str, Any]:
        """Assess change impact."""
        # Use AI to assess impact
        prompt = f"""Assess organizational change impact for:
Scope: {scope}
Affected Users: {users}
Departments: {departments}

Analyze:
1. Change magnitude (low/medium/high)
2. Key stakeholder groups
3. Potential resistance points
4. Success factors"""

        ai_assessment = await self.analyze_with_llm(prompt=prompt, context="You are a change management expert.")

        return {
            "change_magnitude": "high" if users > 100 else "medium",
            "affected_users": users,
            "departments": departments or ["All"],
            "resistance_level": "medium",
            "ai_assessment": ai_assessment,
        }

    def _create_communication_plan(self, assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Create communication plan."""
        return {
            "channels": ["Email", "Town Halls", "Slack/Teams", "Intranet"],
            "frequency": "Weekly updates during rollout",
            "key_messages": [
                "Why we're transforming (business drivers)",
                "What's changing (new tools and processes)",
                "How it benefits you (WIIFM - What's In It For Me)",
                "Support available (training, help desk)",
            ],
            "timeline": {
                "week_-2": "Pre-announcement to leadership",
                "week_0": "Official kickoff announcement",
                "week_1_8": "Weekly progress updates",
                "week_8+": "Monthly optimization updates",
            }
        }

    def _design_training(self, users: int) -> Dict[str, Any]:
        """Design training program."""
        return {
            "delivery_methods": ["Self-paced online", "Live workshops", "Office hours"],
            "duration_hours_per_user": 8,
            "cohort_size": 20,
            "number_of_cohorts": (users + 19) // 20,
            "timeline_weeks": ((users + 19) // 20) * 2,
            "certification": "Citizen Developer Certified",
        }

    async def _create_adoption_strategy(self, assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Create adoption strategy."""
        return {
            "champions_program": {
                "identify": "5-10% of users as champions",
                "train_early": "Train champions before general rollout",
                "support_role": "Champions provide peer support",
            },
            "adoption_metrics": [
                "Active users (target: 80% within 3 months)",
                "Process automation rate (target: 50% of manual tasks)",
                "User satisfaction (target: >75%)",
                "Time savings (target: 30% improvement)",
            ],
            "incentives": [
                "Gamification (leaderboards, badges)",
                "Recognition program",
                "Innovation challenges",
            ],
        }

    def _generate_recommendations(self, output: Dict[str, Any]) -> List[str]:
        return [
            "Secure visible executive sponsorship",
            "Launch champions program early",
            "Communicate benefits clearly (WIIFM)",
            "Provide multiple training formats",
            "Celebrate early wins publicly",
            "Monitor adoption metrics weekly",
        ]
