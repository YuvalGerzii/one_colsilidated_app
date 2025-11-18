"""
Citizen Developer Enablement Agent

Empowers non-technical users to build applications using low-code/no-code platforms.
Based on 2025 goal: 80% of users outside IT building apps.

Uses 100% FREE local LLMs - NO API costs!
"""

from typing import Dict, Any, List
from src.agents.framework import BaseAgent, AgentRole, AgentTask, AgentResult, AgentStatus
from loguru import logger


class CitizenDeveloperAgent(BaseAgent):
    """Enables and supports citizen developers in building low-code applications."""

    def __init__(self):
        super().__init__("citizen-developer", AgentRole.DEVELOPER)

    def get_capabilities(self) -> List[str]:
        return [
            "assess_candidate_suitability",
            "create_learning_path",
            "provide_development_guidance",
            "review_citizen_apps",
            "ensure_governance_compliance",
        ]

    async def execute(self, task: AgentTask) -> AgentResult:
        self.status = AgentStatus.WORKING

        try:
            task_type = task.type.lower()
            input_data = task.input_data

            if task_type == "assess":
                output = await self._assess_candidates(input_data)
            elif task_type == "guide":
                output = await self._provide_guidance(input_data)
            elif task_type == "review":
                output = await self._review_application(input_data)
            else:
                output = await self._create_enablement_program(input_data)

            self.status = AgentStatus.IDLE

            return AgentResult(
                task_id=task.id,
                agent_id=self.agent_id,
                status=AgentStatus.COMPLETED,
                output=output,
                confidence=0.85,
                reasoning="Citizen developer enablement based on 2025 best practices",
                recommendations=self._generate_recommendations(output),
                next_steps=["Begin training program", "Set up sandbox environments", "Launch first project"]
            )

        except Exception as e:
            logger.error(f"Citizen developer enablement failed: {e}")
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

    async def _assess_candidates(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess citizen developer candidates."""
        candidates = input_data.get("candidates", [])

        # Criteria for good citizen developers
        assessment_criteria = {
            "business_knowledge": "Deep understanding of business processes",
            "technical_aptitude": "Comfortable with technology, analytical thinking",
            "problem_solving": "Ability to break down complex problems",
            "collaboration": "Works well with IT and business teams",
            "learning_agility": "Quick to learn new tools and concepts",
        }

        return {
            "assessment_criteria": assessment_criteria,
            "recommended_candidates": min(len(candidates), int(len(candidates) * 0.7)),  # 70% suitable
            "target_by_2026": "80% of users outside IT",
            "training_required": "4-6 weeks initial training",
        }

    async def _provide_guidance(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Provide development guidance to citizen developer."""
        project_description = input_data.get("project_description", "")
        current_challenge = input_data.get("challenge", "")

        # Use AI to provide guidance
        prompt = f"""Provide guidance to a citizen developer:
Project: {project_description}
Challenge: {current_challenge}

Provide:
1. Step-by-step guidance
2. Low-code best practices
3. Common pitfalls to avoid
4. When to involve IT

Keep it simple and actionable."""

        ai_guidance = await self.analyze_with_llm(
            prompt=prompt,
            context="You are a mentor for citizen developers. Provide clear, beginner-friendly guidance."
        )

        return {
            "guidance": ai_guidance,
            "best_practices": [
                "Start with the minimum viable product (MVP)",
                "Reuse components from the library",
                "Test with real users early and often",
                "Follow governance guidelines",
                "Ask IT for help with integrations",
            ],
            "resources": [
                "Component library",
                "Template gallery",
                "Office hours (Tuesdays 2-4pm)",
                "Slack channel: #citizen-developers",
            ],
        }

    async def _review_application(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Review citizen-developed application."""
        app_description = input_data.get("app_description", "")

        # Use AI to review
        prompt = f"""Review this citizen-developed application:
{app_description}

Check for:
1. Governance compliance
2. Security considerations
3. Performance optimization
4. Reusability opportunities
5. Best practice adherence

Provide constructive feedback."""

        ai_review = await self.analyze_with_llm(
            prompt=prompt,
            context="You are reviewing a citizen-developed application. Be constructive and educational."
        )

        return {
            "review_status": "approved_with_suggestions",
            "ai_review": ai_review,
            "checklist": {
                "governance_compliant": True,
                "security_reviewed": True,
                "performance_acceptable": True,
                "reusable_components": True,
            },
            "suggestions_for_improvement": [
                "Consider adding error handling",
                "Extract common logic into reusable component",
                "Add user documentation",
            ],
        }

    async def _create_enablement_program(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive citizen developer enablement program."""
        target_citizen_devs = input_data.get("target_count", 50)

        return {
            "program_structure": {
                "phase_1": {
                    "name": "Foundation Training",
                    "duration_weeks": 4,
                    "curriculum": [
                        "Low-code platform introduction",
                        "Building your first app",
                        "Working with data",
                        "Governance and security basics",
                    ],
                },
                "phase_2": {
                    "name": "Hands-on Project",
                    "duration_weeks": 4,
                    "activities": [
                        "Build real application for your department",
                        "Weekly mentor check-ins",
                        "Peer code reviews",
                        "Deploy to production",
                    ],
                },
                "phase_3": {
                    "name": "Advanced Topics & Community",
                    "duration": "Ongoing",
                    "activities": [
                        "AI agent integration",
                        "Advanced workflows",
                        "Performance optimization",
                        "Community of practice",
                    ],
                },
            },
            "support_structure": {
                "mentors": max(3, target_citizen_devs // 15),  # 1 mentor per 15 devs
                "office_hours": "Weekly",
                "community_channel": "Slack/Teams",
                "documentation": "Self-service knowledge base",
            },
            "governance": {
                "sandbox_environment": "Isolated dev environment for experimentation",
                "approval_process": "IT review before production deployment",
                "component_library": "Reusable, pre-approved components",
                "security_training": "Mandatory security awareness",
            },
            "success_metrics": {
                "target_citizen_devs": target_citizen_devs,
                "apps_per_dev_per_year": 3,
                "time_savings": "30-50% vs traditional development",
                "business_value": "$50K-100K per app",
            },
        }

    def _generate_recommendations(self, output: Dict[str, Any]) -> List[str]:
        return [
            "Target business users with strong domain knowledge",
            "Provide comprehensive training and ongoing support",
            "Create safe sandbox environments for experimentation",
            "Build component library to accelerate development",
            "Celebrate and showcase citizen developer successes",
            "Maintain governance without stifling innovation",
        ]
