"""
Modernization Advisor Agent
Recommends modernization strategies and creates transition plans
"""

from typing import Dict, Any, List
from datetime import datetime, timedelta

from loguru import logger

from src.agents.framework import BaseAgent, AgentRole, AgentTask, AgentResult, AgentStatus


class ModernizationAdvisor(BaseAgent):
    """
    Advises on modernization strategies and creates detailed plans.

    Capabilities:
    - Evaluate modernization options
    - Recommend technology stacks
    - Create phased migration plans
    - Estimate costs and timelines
    - Identify risks and mitigations
    - Suggest training needs
    """

    def __init__(self, agent_id: str = "modernization-advisor"):
        """Initialize modernization advisor."""
        super().__init__(agent_id, AgentRole.ADVISORY)

        self.technology_recommendations = {
            "cobol": {
                "languages": ["Java", "Python", "C#"],
                "frameworks": ["Spring Boot", "Django", ".NET Core"],
                "strategy": "strangler_fig",
            },
            "vb6": {
                "languages": ["C#", "Python"],
                "frameworks": [".NET Core", "FastAPI"],
                "strategy": "rewrite",
            },
            "asp_classic": {
                "languages": ["C#", "JavaScript/TypeScript"],
                "frameworks": ["ASP.NET Core", "Next.js"],
                "strategy": "parallel_run",
            },
            "perl": {
                "languages": ["Python", "Go"],
                "frameworks": ["FastAPI", "Gin"],
                "strategy": "rewrite",
            },
        }

    def get_capabilities(self) -> List[str]:
        """Get agent capabilities."""
        return [
            "recommend_stack",
            "create_roadmap",
            "estimate_effort",
            "identify_risks",
            "plan_training",
            "suggest_architecture",
        ]

    async def execute(self, task: AgentTask) -> AgentResult:
        """Execute modernization advisory task."""
        self.status = AgentStatus.WORKING

        try:
            advice = await self._create_modernization_plan(task.input_data)

            result = AgentResult(
                task_id=task.id,
                agent_id=self.agent_id,
                status=AgentStatus.COMPLETED,
                output=advice,
                confidence=0.9,
                reasoning="Comprehensive modernization plan created",
                recommendations=advice.get("recommendations", []),
                next_steps=advice.get("roadmap", {}).get("phases", []),
            )

            self.status = AgentStatus.IDLE
            return result

        except Exception as e:
            logger.error(f"Modernization planning failed: {e}")
            self.status = AgentStatus.FAILED

            return AgentResult(
                task_id=task.id,
                agent_id=self.agent_id,
                status=AgentStatus.FAILED,
                output={"error": str(e)},
            )

    async def _create_modernization_plan(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive modernization plan."""

        legacy_tech = input_data.get("legacy_technologies", {})
        system_size = input_data.get("total_lines", 10000)
        team_size = input_data.get("team_size", 5)
        budget = input_data.get("budget", 500000)

        plan = {
            "approach": "",
            "recommended_stack": {},
            "roadmap": {},
            "cost_estimate": {},
            "risks": [],
            "recommendations": [],
            "success_metrics": [],
        }

        # Determine approach based on system characteristics
        plan["approach"] = self._determine_approach(legacy_tech, system_size)

        # Recommend technology stack
        plan["recommended_stack"] = self._recommend_stack(legacy_tech)

        # Create phased roadmap
        plan["roadmap"] = self._create_roadmap(system_size, team_size, plan["approach"])

        # Estimate costs
        plan["cost_estimate"] = self._estimate_costs(system_size, team_size, plan["roadmap"])

        # Identify risks
        plan["risks"] = self._identify_risks(plan["approach"], system_size)

        # AI-powered strategic advice
        ai_advice = await self._ai_modernization_advice(input_data, plan)
        plan["ai_strategy"] = ai_advice

        # Generate recommendations
        plan["recommendations"] = self._generate_modernization_recommendations(plan)

        # Define success metrics
        plan["success_metrics"] = self._define_success_metrics()

        return plan

    def _determine_approach(
        self,
        legacy_tech: Dict[str, Any],
        system_size: int,
    ) -> str:
        """Determine best modernization approach."""

        # Factors: risk tolerance, system size, complexity, business criticality

        if system_size > 1000000:  # > 1M lines
            return "strangler_fig"  # Incremental replacement
        elif system_size > 100000:  # > 100K lines
            return "parallel_run"  # Build new alongside old
        else:
            return "big_bang"  # Complete rewrite

    def _recommend_stack(self, legacy_tech: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend modern technology stack."""

        stack = {
            "backend": {
                "language": "Python",
                "framework": "FastAPI",
                "rationale": "Modern, high performance, excellent AI/ML integration",
            },
            "frontend": {
                "language": "TypeScript",
                "framework": "React",
                "rationale": "Type-safe, component-based, large ecosystem",
            },
            "database": {
                "primary": "PostgreSQL",
                "cache": "Redis",
                "rationale": "Mature, scalable, feature-rich",
            },
            "infrastructure": {
                "container": "Docker",
                "orchestration": "Kubernetes",
                "ci_cd": "GitHub Actions",
                "rationale": "Industry standard, cloud-native",
            },
            "ai_integration": {
                "llm": "Ollama (Local)",
                "vector_db": "Qdrant",
                "rationale": "100% free, on-premises, no API costs",
            },
        }

        # Adjust based on legacy tech
        dominant_legacy = max(legacy_tech, key=legacy_tech.get, default=None)
        if dominant_legacy in self.technology_recommendations:
            recommendations = self.technology_recommendations[dominant_legacy]
            stack["backend"]["alternatives"] = recommendations["languages"]
            stack["backend"]["framework_options"] = recommendations["frameworks"]

        return stack

    def _create_roadmap(self, system_size: int, team_size: int, approach: str) -> Dict[str, Any]:
        """Create phased modernization roadmap."""

        # Estimate duration
        base_weeks = system_size / 1000  # 1 week per 1000 lines
        adjusted_weeks = base_weeks / team_size
        duration_months = int(adjusted_weeks / 4)

        phases = []

        # Phase 1: Planning & Setup
        phases.append({
            "name": "Phase 1: Foundation",
            "duration_weeks": min(4, duration_months * 4 * 0.15),
            "objectives": [
                "Set up development environment",
                "Choose and learn new tech stack",
                "Create architecture documentation",
                "Set up CI/CD pipeline",
                "Establish coding standards",
            ],
            "deliverables": [
                "Architecture diagram",
                "Development environment",
                "CI/CD pipeline",
                "Coding guidelines",
            ],
        })

        # Phase 2: Core Migration
        phases.append({
            "name": "Phase 2: Core Migration",
            "duration_weeks": duration_months * 4 * 0.50,
            "objectives": [
                "Migrate critical business logic",
                "Build data migration scripts",
                "Implement core APIs",
                "Set up monitoring",
            ],
            "deliverables": [
                "Core functionality in new stack",
                "Data migration tools",
                "API documentation",
                "Monitoring dashboard",
            ],
        })

        # Phase 3: Feature Parity
        phases.append({
            "name": "Phase 3: Feature Completion",
            "duration_weeks": duration_months * 4 * 0.25,
            "objectives": [
                "Complete remaining features",
                "Performance optimization",
                "Security hardening",
                "User acceptance testing",
            ],
            "deliverables": [
                "Complete feature set",
                "Performance benchmarks",
                "Security audit report",
                "UAT signoff",
            ],
        })

        # Phase 4: Deployment & Cutover
        phases.append({
            "name": "Phase 4: Go-Live",
            "duration_weeks": duration_months * 4 * 0.10,
            "objectives": [
                "Production deployment",
                "Data cutover",
                "User training",
                "Decommission legacy system",
            ],
            "deliverables": [
                "Production system",
                "Training materials",
                "Decommission plan",
                "Post-mortem documentation",
            ],
        })

        return {
            "total_duration_months": duration_months,
            "total_duration_weeks": duration_months * 4,
            "phases": phases,
            "milestones": self._define_milestones(phases),
        }

    def _estimate_costs(
        self,
        system_size: int,
        team_size: int,
        roadmap: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Estimate modernization costs."""

        duration_months = roadmap["total_duration_months"]
        avg_developer_salary = 150000  # Annual
        monthly_rate = avg_developer_salary / 12

        costs = {
            "labor": {
                "developers": team_size * monthly_rate * duration_months,
                "architects": 1 * (monthly_rate * 1.5) * (duration_months * 0.5),  # Part-time
                "qa": (team_size / 2) * monthly_rate * (duration_months * 0.75),
                "project_manager": 1 * monthly_rate * duration_months,
            },
            "infrastructure": {
                "development": 500 * duration_months,
                "staging": 1000 * duration_months,
                "production": 2000 * duration_months,
            },
            "tools": {
                "licenses": 100 * team_size * duration_months,
                "training": 5000 * team_size,
                "ci_cd": 500 * duration_months,
            },
            "contingency": 0,  # Will calculate
        }

        # Calculate totals
        labor_total = sum(costs["labor"].values())
        infra_total = sum(costs["infrastructure"].values())
        tools_total = sum(costs["tools"].values())

        subtotal = labor_total + infra_total + tools_total
        costs["contingency"] = subtotal * 0.20  # 20% buffer

        costs["total"] = subtotal + costs["contingency"]
        costs["monthly_average"] = costs["total"] / duration_months

        return costs

    def _identify_risks(self, approach: str, system_size: int) -> List[Dict[str, Any]]:
        """Identify modernization risks."""

        risks = [
            {
                "category": "Technical",
                "risk": "Data migration complexity",
                "probability": "medium",
                "impact": "high",
                "mitigation": "Extensive testing, dry runs, rollback plan",
            },
            {
                "category": "Business",
                "risk": "Feature gaps in new system",
                "probability": "medium",
                "impact": "high",
                "mitigation": "Detailed requirements gathering, UAT before cutover",
            },
            {
                "category": "Team",
                "risk": "Learning curve with new tech",
                "probability": "high",
                "impact": "medium",
                "mitigation": "Training program, pair programming, documentation",
            },
            {
                "category": "Schedule",
                "risk": "Timeline overruns",
                "probability": "high",
                "impact": "high",
                "mitigation": "Phased approach, regular reviews, contingency buffer",
            },
        ]

        if approach == "big_bang":
            risks.append({
                "category": "Technical",
                "risk": "Big bang deployment failure",
                "probability": "medium",
                "impact": "critical",
                "mitigation": "Comprehensive testing, rehearsals, quick rollback capability",
            })

        if system_size > 500000:
            risks.append({
                "category": "Technical",
                "risk": "Unknown dependencies in large codebase",
                "probability": "high",
                "impact": "high",
                "mitigation": "Thorough discovery phase, dependency mapping",
            })

        return risks

    def _define_milestones(self, phases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Define key milestones."""

        milestones = []
        week_counter = 0

        for i, phase in enumerate(phases, 1):
            week_counter += phase["duration_weeks"]

            milestones.append({
                "number": i,
                "name": f"{phase['name']} Complete",
                "week": int(week_counter),
                "success_criteria": phase["deliverables"],
            })

        return milestones

    async def _ai_modernization_advice(
        self,
        input_data: Dict[str, Any],
        plan: Dict[str, Any],
    ) -> str:
        """Get AI-powered strategic advice."""

        prompt = f"""Provide modernization strategy advice:

Current situation:
- Legacy tech: {input_data.get('legacy_technologies', {})}
- System size: {input_data.get('total_lines', 0):,} lines
- Team size: {input_data.get('team_size', 0)} developers
- Budget: ${input_data.get('budget', 0):,}

Proposed plan:
- Approach: {plan['approach']}
- Duration: {plan['roadmap']['total_duration_months']} months
- Estimated cost: ${plan['cost_estimate']['total']:,.0f}

Provide strategic advice on:
1. Biggest challenge and how to overcome it
2. Critical success factor
3. One thing to avoid
4. Quick win opportunity

Keep under 200 words."""

        response = await self.analyze_with_llm(
            prompt,
            context="You are a digital transformation expert advising on modernization.",
        )

        return response

    def _generate_modernization_recommendations(self, plan: Dict[str, Any]) -> List[str]:
        """Generate specific recommendations."""

        recommendations = []

        # Based on approach
        if plan["approach"] == "strangler_fig":
            recommendations.append("✓ Strangler Fig pattern chosen - start with high-value, low-risk components")
            recommendations.append("Implement feature toggles for gradual rollout")

        elif plan["approach"] == "big_bang":
            recommendations.append("⚠️ Big Bang approach - ensure extensive testing and rollback procedures")
            recommendations.append("Consider pilot deployment to subset of users first")

        # Cost-related
        total_cost = plan["cost_estimate"]["total"]
        if total_cost > 1000000:
            recommendations.append(f"Large investment (${total_cost:,.0f}) - ensure executive sponsorship and regular stakeholder updates")

        # Duration-related
        duration = plan["roadmap"]["total_duration_months"]
        if duration > 12:
            recommendations.append(f"Long project ({duration} months) - maintain momentum with regular releases")

        # Risk-related
        critical_risks = [r for r in plan["risks"] if r["impact"] == "critical"]
        if critical_risks:
            recommendations.append("🔴 Critical risks identified - create detailed mitigation plans before starting")

        # General best practices
        recommendations.extend([
            "Use LOCAL LLMs for AI features - no ongoing API costs!",
            "Set up automated testing from day 1",
            "Document architectural decisions (ADRs)",
            "Plan for parallel running period",
            "Create comprehensive rollback procedures",
        ])

        return recommendations

    def _define_success_metrics(self) -> List[Dict[str, Any]]:
        """Define success metrics for modernization."""

        return [
            {
                "metric": "Feature Parity",
                "target": "100% of legacy features replicated",
                "measurement": "Feature checklist completion",
            },
            {
                "metric": "Performance",
                "target": "50% faster than legacy system",
                "measurement": "Response time benchmarks",
            },
            {
                "metric": "Quality",
                "target": "90% test coverage",
                "measurement": "Code coverage reports",
            },
            {
                "metric": "User Satisfaction",
                "target": "80% positive feedback",
                "measurement": "User surveys",
            },
            {
                "metric": "Cost",
                "target": "Within 10% of budget",
                "measurement": "Actual vs budgeted spend",
            },
            {
                "metric": "Timeline",
                "target": "Within 10% of schedule",
                "measurement": "Actual vs planned dates",
            },
            {
                "metric": "Defects",
                "target": "<5 critical bugs in first month",
                "measurement": "Bug tracking system",
            },
        ]
