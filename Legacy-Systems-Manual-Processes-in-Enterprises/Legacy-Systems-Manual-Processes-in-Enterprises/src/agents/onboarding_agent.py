"""
Onboarding Orchestrator Agent

Guides enterprises through digital transformation and modernization onboarding.
Based on 2025 best practices for low-code transformation and AI adoption.

Uses 100% FREE local LLMs - NO API costs!
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

from src.agents.framework import (
    BaseAgent,
    AgentRole,
    AgentTask,
    AgentResult,
    AgentStatus,
)
from src.core.llm import get_local_llm
from loguru import logger


class OnboardingOrchestratorAgent(BaseAgent):
    """
    Orchestrates digital transformation onboarding and guides enterprises
    through modernization journey.

    Based on 2025 research:
    - 89% of CIOs consider agent-based AI a strategic priority
    - 70% of new enterprise apps built with low-code/no-code by 2025
    - 81% of companies consider low-code strategically important
    - 87% report solid returns from AI investments
    """

    def __init__(self):
        super().__init__("onboarding-orchestrator", AgentRole.ADVISORY)

        # Transformation phases based on 2025 best practices
        self.transformation_phases = {
            "assessment": {
                "name": "Assessment & Discovery",
                "duration_weeks": 2,
                "activities": [
                    "Assess current technology landscape",
                    "Identify pain points and bottlenecks",
                    "Map stakeholder requirements",
                    "Evaluate team capabilities",
                    "Analyze budget and resources",
                ],
            },
            "strategy": {
                "name": "Strategy & Planning",
                "duration_weeks": 3,
                "activities": [
                    "Define transformation vision and goals",
                    "Select low-code/no-code platforms",
                    "Design governance framework",
                    "Create fusion team structure",
                    "Develop pilot project roadmap",
                ],
            },
            "enablement": {
                "name": "Team Enablement",
                "duration_weeks": 4,
                "activities": [
                    "Train citizen developers",
                    "Establish development sandboxes",
                    "Define security and compliance standards",
                    "Create reusable component library",
                    "Set up monitoring and analytics",
                ],
            },
            "pilot": {
                "name": "Pilot Projects",
                "duration_weeks": 8,
                "activities": [
                    "Launch 2-3 pilot projects",
                    "Implement AI agent workflows",
                    "Test integration patterns",
                    "Gather feedback and iterate",
                    "Measure ROI and success metrics",
                ],
            },
            "scale": {
                "name": "Scale & Optimize",
                "duration_weeks": 12,
                "activities": [
                    "Roll out to additional departments",
                    "Optimize multi-agent orchestration",
                    "Expand component library",
                    "Refine governance processes",
                    "Continuous improvement cycles",
                ],
            },
        }

        # Low-code platform recommendations (2025)
        self.platform_recommendations = {
            "enterprise": {
                "primary": "Salesforce Agentforce",
                "alternatives": ["Microsoft Power Platform", "ServiceNow"],
                "strengths": "Enterprise-grade, 10/10 performance, ROI in 2 weeks",
            },
            "mid_market": {
                "primary": "Microsoft Power Platform",
                "alternatives": ["OutSystems", "Mendix"],
                "strengths": "30-50% faster response times, Azure integration",
            },
            "startup": {
                "primary": "Bubble.io",
                "alternatives": ["Webflow", "Adalo"],
                "strengths": "Cost-effective, rapid prototyping, visual development",
            },
            "process_automation": {
                "primary": "IBM watsonx Orchestrate",
                "alternatives": ["UiPath", "Automation Anywhere"],
                "strengths": "Multi-agent orchestration, intelligent routing",
            },
        }

    def get_capabilities(self) -> List[str]:
        """Return agent capabilities."""
        return [
            "transformation_assessment",
            "onboarding_roadmap",
            "platform_selection",
            "team_enablement_plan",
            "pilot_project_design",
            "roi_tracking",
            "change_management",
            "citizen_developer_training",
            "governance_framework",
            "multi_agent_orchestration",
        ]

    async def execute(self, task: AgentTask) -> AgentResult:
        """Execute onboarding orchestration task."""
        self.status = AgentStatus.WORKING

        try:
            task_type = task.type.lower()

            if task_type == "assess":
                output = await self._assess_readiness(task.input_data)
            elif task_type == "plan":
                output = await self._create_onboarding_plan(task.input_data)
            elif task_type == "recommend":
                output = await self._recommend_platforms(task.input_data)
            elif task_type == "enable":
                output = await self._create_enablement_plan(task.input_data)
            else:
                # Default: comprehensive onboarding
                output = await self._comprehensive_onboarding(task.input_data)

            # Generate AI-powered insights
            ai_insights = await self._ai_onboarding_strategy(output)
            output["ai_insights"] = ai_insights

            # Generate recommendations
            recommendations = self._generate_recommendations(output)

            self.status = AgentStatus.IDLE

            return AgentResult(
                task_id=task.id,
                agent_id=self.agent_id,
                status=AgentStatus.COMPLETED,
                output=output,
                confidence=0.9,
                reasoning=f"Onboarding assessment based on 2025 best practices and AI analysis",
                recommendations=recommendations,
                next_steps=self._generate_next_steps(output),
            )

        except Exception as e:
            logger.error(f"Onboarding orchestration failed: {e}")
            self.status = AgentStatus.IDLE

            return AgentResult(
                task_id=task.id,
                agent_id=self.agent_id,
                status=AgentStatus.FAILED,
                output={"error": str(e)},
                confidence=0.0,
                reasoning=f"Failed to complete onboarding orchestration: {e}",
                recommendations=["Review error logs", "Retry with valid input data"],
                next_steps=[],
            )

    async def _assess_readiness(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess organization's readiness for digital transformation.

        Based on 2025 research:
        - 70% of enterprises use low-code/no-code
        - 89% of CIOs prioritize agentic AI
        - 60% of multi-agent systems fail to scale without proper planning
        """
        company_size = input_data.get("company_size", "medium")
        current_tech_stack = input_data.get("current_tech_stack", [])
        budget = input_data.get("budget", 0)
        team_size = input_data.get("team_size", 10)
        it_maturity = input_data.get("it_maturity", "medium")  # low/medium/high

        # Calculate readiness scores
        readiness_scores = {}

        # Technical readiness (0-10)
        tech_score = 5.0
        if "cloud" in str(current_tech_stack).lower():
            tech_score += 2
        if "api" in str(current_tech_stack).lower():
            tech_score += 1
        if it_maturity == "high":
            tech_score += 2
        elif it_maturity == "low":
            tech_score -= 2

        readiness_scores["technical"] = min(10, max(0, tech_score))

        # Organizational readiness (0-10)
        org_score = 6.0
        if team_size >= 50:
            org_score += 2
        elif team_size < 10:
            org_score -= 1

        if company_size == "enterprise":
            org_score += 1
        elif company_size == "startup":
            org_score += 2  # More agile

        readiness_scores["organizational"] = min(10, max(0, org_score))

        # Financial readiness (0-10)
        fin_score = 5.0
        if budget >= 500000:
            fin_score += 3
        elif budget >= 100000:
            fin_score += 2
        elif budget < 50000:
            fin_score -= 2

        readiness_scores["financial"] = min(10, max(0, fin_score))

        # Overall readiness
        overall_readiness = sum(readiness_scores.values()) / len(readiness_scores)

        # Determine readiness level
        if overall_readiness >= 8:
            readiness_level = "high"
            timeframe = "3-6 months"
        elif overall_readiness >= 6:
            readiness_level = "medium"
            timeframe = "6-12 months"
        else:
            readiness_level = "low"
            timeframe = "12-18 months"

        # Identify gaps
        gaps = []
        if readiness_scores["technical"] < 6:
            gaps.append({
                "area": "Technical Infrastructure",
                "severity": "high",
                "description": "Need to modernize technical stack and implement APIs",
                "solution": "Adopt cloud-first strategy and API-driven architecture",
            })

        if readiness_scores["organizational"] < 6:
            gaps.append({
                "area": "Organizational Structure",
                "severity": "medium",
                "description": "Team needs to grow or reorganize for transformation",
                "solution": "Build fusion teams (IT + business) and upskill staff",
            })

        if readiness_scores["financial"] < 5:
            gaps.append({
                "area": "Budget",
                "severity": "high",
                "description": "Insufficient budget for comprehensive transformation",
                "solution": "Start with pilot projects to demonstrate ROI, then expand",
            })

        # Quick wins
        quick_wins = [
            {
                "initiative": "Automate 1-2 manual processes with low-code",
                "effort": "low",
                "impact": "medium",
                "timeframe": "2-4 weeks",
                "expected_roi": "15-25%",
            },
            {
                "initiative": "Deploy AI agent for customer service",
                "effort": "medium",
                "impact": "high",
                "timeframe": "4-6 weeks",
                "expected_roi": "30-50% faster response times",
            },
            {
                "initiative": "Create citizen developer training program",
                "effort": "medium",
                "impact": "high",
                "timeframe": "6-8 weeks",
                "expected_roi": "3x developer productivity by 2026",
            },
        ]

        return {
            "readiness_level": readiness_level,
            "overall_score": round(overall_readiness, 1),
            "scores": readiness_scores,
            "estimated_timeframe": timeframe,
            "gaps": gaps,
            "quick_wins": quick_wins,
            "industry_benchmarks": {
                "average_low_code_adoption": "70%",
                "average_ai_agent_adoption": "29%",
                "planned_adoption_2025": "44%",
                "projected_roi": "25-45% margin improvement",
            },
        }

    async def _create_onboarding_plan(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive onboarding roadmap."""
        readiness_level = input_data.get("readiness_level", "medium")
        company_size = input_data.get("company_size", "medium")
        priorities = input_data.get("priorities", ["automation", "ai_agents"])

        # Customize phases based on readiness
        phases = []
        total_duration_weeks = 0

        for phase_key, phase_info in self.transformation_phases.items():
            # Adjust duration based on readiness
            duration = phase_info["duration_weeks"]
            if readiness_level == "high":
                duration = int(duration * 0.75)  # 25% faster
            elif readiness_level == "low":
                duration = int(duration * 1.5)  # 50% slower

            phases.append({
                "id": phase_key,
                "name": phase_info["name"],
                "duration_weeks": duration,
                "start_week": total_duration_weeks,
                "end_week": total_duration_weeks + duration,
                "activities": phase_info["activities"],
                "deliverables": self._get_phase_deliverables(phase_key),
                "success_criteria": self._get_phase_success_criteria(phase_key),
            })

            total_duration_weeks += duration

        # Resource requirements
        resources = {
            "team": {
                "transformation_lead": 1,
                "architects": 2 if company_size == "enterprise" else 1,
                "citizen_developers": 5,
                "it_developers": 3,
                "change_managers": 1,
            },
            "tools": [
                "Low-code/no-code platform subscription",
                "AI agent orchestration platform",
                "Training and enablement materials",
                "Sandbox environments",
                "Monitoring and analytics tools",
            ],
            "estimated_budget": self._estimate_budget(company_size, total_duration_weeks),
        }

        # Milestones
        milestones = [
            {
                "name": "Transformation Strategy Approved",
                "week": phases[1]["end_week"],
                "critical": True,
            },
            {
                "name": "First Citizen Developer Certified",
                "week": phases[2]["end_week"],
                "critical": True,
            },
            {
                "name": "First Pilot Project Live",
                "week": phases[3]["end_week"],
                "critical": True,
            },
            {
                "name": "ROI Demonstrated",
                "week": phases[3]["end_week"] + 4,
                "critical": True,
            },
            {
                "name": "Scale to 5 Departments",
                "week": phases[4]["end_week"],
                "critical": False,
            },
        ]

        return {
            "total_duration_weeks": total_duration_weeks,
            "total_duration_months": round(total_duration_weeks / 4, 1),
            "phases": phases,
            "resources": resources,
            "milestones": milestones,
            "success_metrics": {
                "development_speed": "80% faster app development",
                "citizen_developer_adoption": "80% of users outside IT by 2026",
                "roi_timeframe": "2-8 weeks for first wins",
                "cost_reduction": "34% reduction in app development cost",
                "time_to_market": "38% improvement",
            },
        }

    async def _recommend_platforms(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend low-code/no-code and AI platforms based on 2025 research."""
        company_size = input_data.get("company_size", "medium")
        use_cases = input_data.get("use_cases", ["automation"])
        budget = input_data.get("budget", 100000)

        # Map company size to platform category
        category_map = {
            "enterprise": "enterprise",
            "large": "enterprise",
            "medium": "mid_market",
            "small": "mid_market",
            "startup": "startup",
        }

        category = category_map.get(company_size, "mid_market")

        # Primary platform recommendation
        primary = self.platform_recommendations.get(category, self.platform_recommendations["mid_market"])

        # Additional specialized platforms
        specialized_platforms = []

        if "process_automation" in use_cases or "workflow" in use_cases:
            specialized_platforms.append(self.platform_recommendations["process_automation"])

        # AI agent platforms (2025 leaders)
        ai_platforms = [
            {
                "name": "Salesforce Agentforce",
                "score": "10/10",
                "roi": "2 weeks",
                "best_for": "Enterprise CRM automation",
                "pricing": "Enterprise",
            },
            {
                "name": "Microsoft Copilot Agents",
                "score": "9/10",
                "roi": "4 weeks",
                "best_for": "Office 365 integration, 30-50% faster responses",
                "pricing": "Per-user",
            },
            {
                "name": "IBM watsonx Orchestrate",
                "score": "9/10",
                "roi": "6 weeks",
                "best_for": "Multi-agent orchestration, process automation",
                "pricing": "Enterprise",
            },
        ]

        # Local/open-source options (FREE!)
        open_source_options = [
            {
                "name": "Ollama + LangGraph",
                "cost": "$0",
                "best_for": "Custom AI agents, 100% local, no API costs",
                "limitations": "Requires technical setup",
            },
            {
                "name": "CrewAI",
                "cost": "$0",
                "best_for": "Multi-agent orchestration, role-based agents",
                "limitations": "Need to manage infrastructure",
            },
            {
                "name": "n8n (self-hosted)",
                "cost": "$0",
                "best_for": "Workflow automation, visual builder",
                "limitations": "Self-hosting required",
            },
        ]

        # Implementation strategy
        implementation_strategy = {
            "phase_1": {
                "name": "Foundation (Weeks 1-4)",
                "platforms": [primary["primary"]],
                "focus": "Core automation and citizen developer enablement",
            },
            "phase_2": {
                "name": "AI Augmentation (Weeks 5-12)",
                "platforms": [ai_platforms[0]["name"]],
                "focus": "Deploy AI agents for customer service and internal ops",
            },
            "phase_3": {
                "name": "Scale (Weeks 13+)",
                "platforms": ["Multi-platform integration"],
                "focus": "Enterprise-wide rollout and optimization",
            },
        }

        return {
            "primary_recommendation": primary,
            "specialized_platforms": specialized_platforms,
            "ai_agent_platforms": ai_platforms,
            "open_source_options": open_source_options,
            "implementation_strategy": implementation_strategy,
            "total_cost_estimate": {
                "year_1": budget * 0.8,
                "year_2": budget * 0.5,
                "ongoing_annual": budget * 0.3,
            },
            "expected_roi": {
                "time_to_first_value": "2-8 weeks",
                "development_speed_improvement": "80%",
                "cost_reduction": "34%",
                "margin_improvement": "25-45%",
            },
        }

    async def _create_enablement_plan(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create team enablement and training plan."""
        team_size = input_data.get("team_size", 20)
        it_maturity = input_data.get("it_maturity", "medium")

        # Training tracks based on 2025 best practices
        training_tracks = {
            "citizen_developers": {
                "target_audience": "Business users (80% of users by 2026)",
                "duration_weeks": 4,
                "curriculum": [
                    "Low-code platform fundamentals",
                    "Visual app builder training",
                    "Data modeling basics",
                    "API integration concepts",
                    "Testing and deployment",
                    "Governance and security",
                ],
                "certification": "Citizen Developer Certified",
                "expected_outcome": "Build simple apps independently",
            },
            "fusion_developers": {
                "target_audience": "IT + Business collaboration",
                "duration_weeks": 6,
                "curriculum": [
                    "Advanced low-code development",
                    "AI agent configuration",
                    "Multi-agent orchestration",
                    "Custom code extensions",
                    "Integration patterns",
                    "Performance optimization",
                ],
                "certification": "Fusion Developer Certified",
                "expected_outcome": "Build complex, integrated solutions",
            },
            "ai_agent_builders": {
                "target_audience": "Technical leads and architects",
                "duration_weeks": 8,
                "curriculum": [
                    "Agentic AI fundamentals",
                    "Multi-agent system design",
                    "Orchestration patterns",
                    "LLM integration (local + cloud)",
                    "Agent monitoring and optimization",
                    "Security and compliance",
                ],
                "certification": "AI Agent Architect",
                "expected_outcome": "Design enterprise multi-agent systems",
            },
        }

        # Calculate team allocation
        target_citizen_devs = int(team_size * 0.6)  # 60% become citizen developers
        target_fusion_devs = int(team_size * 0.3)   # 30% fusion developers
        target_ai_builders = max(2, int(team_size * 0.1))  # 10% AI specialists

        enablement_plan = {
            "tracks": training_tracks,
            "team_allocation": {
                "citizen_developers": target_citizen_devs,
                "fusion_developers": target_fusion_devs,
                "ai_agent_builders": target_ai_builders,
            },
            "timeline": {
                "week_1_4": "Citizen developer training cohort 1",
                "week_5_8": "Citizen developer cohort 2 + Fusion dev cohort 1",
                "week_9_16": "AI agent builder training + Advanced workshops",
            },
            "resources": {
                "training_platform": "Recommended LMS or platform-native",
                "sandbox_environments": target_citizen_devs,
                "mentors_needed": max(3, team_size // 10),
                "estimated_cost": team_size * 1500,  # $1,500 per person
            },
        }

        return enablement_plan

    async def _comprehensive_onboarding(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive end-to-end onboarding plan."""
        # Run all assessments
        readiness = await self._assess_readiness(input_data)

        # Create plans based on readiness
        input_with_readiness = {**input_data, "readiness_level": readiness["readiness_level"]}
        onboarding_plan = await self._create_onboarding_plan(input_with_readiness)
        platform_recs = await self._recommend_platforms(input_data)
        enablement_plan = await self._create_enablement_plan(input_data)

        return {
            "readiness_assessment": readiness,
            "onboarding_roadmap": onboarding_plan,
            "platform_recommendations": platform_recs,
            "enablement_plan": enablement_plan,
            "summary": {
                "readiness_level": readiness["readiness_level"],
                "estimated_duration_months": onboarding_plan["total_duration_months"],
                "primary_platform": platform_recs["primary_recommendation"]["primary"],
                "team_to_train": sum(enablement_plan["team_allocation"].values()),
                "quick_win_timeframe": "2-4 weeks",
            },
        }

    async def _ai_onboarding_strategy(self, analysis: Dict[str, Any]) -> str:
        """Use local LLM to generate strategic insights."""
        prompt = f"""As a digital transformation advisor, provide strategic insights for this organization's transformation:

Readiness Level: {analysis.get('readiness_assessment', {}).get('readiness_level', 'N/A')}
Key Gaps: {analysis.get('readiness_assessment', {}).get('gaps', [])}

Based on 2025 industry trends:
- 70% of enterprises using low-code/no-code
- 89% of CIOs prioritizing agentic AI
- 87% seeing solid ROI from AI investments
- Average ROI timeframe: 2-8 weeks

Provide 3-5 strategic recommendations for successful transformation.
Focus on: risk mitigation, quick wins, team enablement, and scaling strategy.
"""

        response = await self.analyze_with_llm(
            prompt=prompt,
            context="You are an expert in enterprise digital transformation and 2025 low-code/AI adoption strategies.",
        )

        return response

    def _generate_recommendations(self, output: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []

        # Based on readiness
        readiness = output.get("readiness_assessment", {})
        if readiness.get("readiness_level") == "low":
            recommendations.append("Start with 1-2 pilot projects to build confidence and demonstrate ROI")
            recommendations.append("Invest in team enablement before scaling")

        # Based on gaps
        gaps = readiness.get("gaps", [])
        for gap in gaps[:3]:
            recommendations.append(f"{gap['area']}: {gap['solution']}")

        # General best practices
        recommendations.extend([
            "Establish fusion teams (IT + business) from day 1",
            "Use local LLMs (Ollama) to minimize AI costs - $0 vs $3-5K/month",
            "Target 80% of users outside IT as citizen developers by 2026",
            "Measure ROI weekly during pilot phase",
            "Create reusable component library to accelerate development",
        ])

        return recommendations[:8]

    def _generate_next_steps(self, output: Dict[str, Any]) -> List[str]:
        """Generate next steps."""
        return [
            "Review readiness assessment with stakeholders",
            "Secure executive sponsorship and budget",
            "Select pilot projects (2-3 high-impact, low-complexity)",
            "Identify first cohort of citizen developers",
            "Set up sandbox environments for experimentation",
            "Schedule transformation kickoff meeting",
        ]

    def _get_phase_deliverables(self, phase_key: str) -> List[str]:
        """Get deliverables for each phase."""
        deliverables_map = {
            "assessment": [
                "Current state assessment report",
                "Stakeholder requirements document",
                "Technology gap analysis",
            ],
            "strategy": [
                "Transformation strategy document",
                "Platform selection rationale",
                "Governance framework v1.0",
                "Pilot project charters",
            ],
            "enablement": [
                "Training curriculum and materials",
                "Sandbox environments",
                "Component library v1.0",
                "Security and compliance guidelines",
            ],
            "pilot": [
                "2-3 pilot applications live",
                "ROI metrics and dashboard",
                "Lessons learned report",
                "Scaling plan",
            ],
            "scale": [
                "Enterprise rollout plan",
                "Expanded component library",
                "Governance playbook",
                "Continuous improvement framework",
            ],
        }
        return deliverables_map.get(phase_key, [])

    def _get_phase_success_criteria(self, phase_key: str) -> List[str]:
        """Get success criteria for each phase."""
        criteria_map = {
            "assessment": [
                "100% stakeholder interviews completed",
                "Technology gaps identified and prioritized",
            ],
            "strategy": [
                "Executive approval obtained",
                "Platform licenses procured",
                "Governance framework approved",
            ],
            "enablement": [
                "First cohort trained and certified",
                "Sandbox environments operational",
                "Security standards in place",
            ],
            "pilot": [
                "All pilot projects deployed",
                "Positive ROI demonstrated",
                "User satisfaction >80%",
            ],
            "scale": [
                "5+ departments onboarded",
                "50+ citizen developers active",
                "Cost savings targets met",
            ],
        }
        return criteria_map.get(phase_key, [])

    def _estimate_budget(self, company_size: str, duration_weeks: int) -> Dict[str, float]:
        """Estimate budget for transformation."""
        # Base on company size
        base_cost_map = {
            "enterprise": 500000,
            "large": 300000,
            "medium": 150000,
            "small": 75000,
            "startup": 30000,
        }

        base_cost = base_cost_map.get(company_size, 150000)

        return {
            "platform_licenses": base_cost * 0.3,
            "training_enablement": base_cost * 0.2,
            "consulting_support": base_cost * 0.25,
            "infrastructure": base_cost * 0.15,
            "contingency": base_cost * 0.10,
            "total": base_cost,
        }
