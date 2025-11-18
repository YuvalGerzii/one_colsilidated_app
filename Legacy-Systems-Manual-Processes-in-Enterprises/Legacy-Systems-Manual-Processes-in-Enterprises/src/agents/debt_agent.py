"""
Technical Debt Analyzer Agent
Identifies, quantifies, and prioritizes technical debt
"""

from typing import Dict, Any, List
from datetime import datetime, timedelta

from loguru import logger

from src.agents.framework import BaseAgent, AgentRole, AgentTask, AgentResult, AgentStatus


class TechnicalDebtAgent(BaseAgent):
    """
    Identifies and quantifies technical debt.

    Capabilities:
    - Calculate debt principal (cost to fix)
    - Estimate interest (ongoing cost)
    - Priority scoring
    - Debt categorization
    - ROI analysis for fixes
    - Payoff strategies
    """

    def __init__(self, agent_id: str = "tech-debt"):
        """Initialize technical debt agent."""
        super().__init__(agent_id, AgentRole.ANALYSIS)

        self.debt_categories = [
            "code_quality",
            "architecture",
            "documentation",
            "testing",
            "security",
            "performance",
            "dependencies",
        ]

    def get_capabilities(self) -> List[str]:
        """Get agent capabilities."""
        return [
            "calculate_debt",
            "estimate_interest",
            "prioritize_debt",
            "recommend_payoff",
            "track_debt",
            "forecast_impact",
        ]

    async def execute(self, task: AgentTask) -> AgentResult:
        """Execute technical debt analysis."""
        self.status = AgentStatus.WORKING

        try:
            analysis = await self._analyze_technical_debt(task.input_data)

            result = AgentResult(
                task_id=task.id,
                agent_id=self.agent_id,
                status=AgentStatus.COMPLETED,
                output=analysis,
                confidence=0.85,
                reasoning="Comprehensive technical debt analysis completed",
                recommendations=analysis.get("recommendations", []),
                next_steps=analysis.get("next_steps", []),
            )

            self.status = AgentStatus.IDLE
            return result

        except Exception as e:
            logger.error(f"Technical debt analysis failed: {e}")
            self.status = AgentStatus.FAILED

            return AgentResult(
                task_id=task.id,
                agent_id=self.agent_id,
                status=AgentStatus.FAILED,
                output={"error": str(e)},
            )

    async def _analyze_technical_debt(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze technical debt."""

        code_metrics = input_data.get("code_metrics", {})
        quality_assessment = input_data.get("quality_assessment", {})
        age_years = input_data.get("age_years", 5)

        analysis = {
            "debt_items": [],
            "total_debt_hours": 0,
            "total_debt_cost": 0,
            "monthly_interest": 0,
            "categories": {},
            "priority_matrix": [],
            "recommendations": [],
            "next_steps": [],
        }

        # Identify debt items
        debt_items = self._identify_debt_items(code_metrics, quality_assessment)
        analysis["debt_items"] = debt_items

        # Calculate debt principal
        total_hours = sum(item["hours_to_fix"] for item in debt_items)
        hourly_rate = input_data.get("hourly_rate", 150)  # Developer hourly rate
        analysis["total_debt_hours"] = total_hours
        analysis["total_debt_cost"] = total_hours * hourly_rate

        # Calculate interest (ongoing cost)
        analysis["monthly_interest"] = self._calculate_interest(debt_items, hourly_rate)

        # Categorize debt
        for item in debt_items:
            category = item["category"]
            if category not in analysis["categories"]:
                analysis["categories"][category] = {
                    "count": 0,
                    "total_hours": 0,
                    "total_cost": 0,
                }

            analysis["categories"][category]["count"] += 1
            analysis["categories"][category]["total_hours"] += item["hours_to_fix"]
            analysis["categories"][category]["total_cost"] += item["hours_to_fix"] * hourly_rate

        # Prioritize debt
        analysis["priority_matrix"] = self._prioritize_debt(debt_items)

        # AI-powered insights
        ai_insights = await self._ai_debt_analysis(analysis, age_years)
        analysis["ai_insights"] = ai_insights

        # Generate recommendations
        analysis["recommendations"] = self._generate_debt_recommendations(analysis)
        analysis["next_steps"] = self._generate_next_steps(analysis)

        return analysis

    def _identify_debt_items(
        self,
        code_metrics: Dict[str, Any],
        quality_assessment: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """Identify specific debt items."""
        items = []

        # From code smells
        code_smells = quality_assessment.get("code_smells", [])
        for smell in code_smells:
            items.append({
                "type": "code_smell",
                "category": "code_quality",
                "description": smell.get("description", ""),
                "severity": smell.get("severity", "medium"),
                "hours_to_fix": self._estimate_fix_time(smell),
                "interest_per_month": self._estimate_ongoing_cost(smell),
            })

        # From security issues
        security_issues = quality_assessment.get("issues", [])
        for issue in security_issues:
            if issue.get("type") == "security":
                items.append({
                    "type": "security_issue",
                    "category": "security",
                    "description": issue.get("description", ""),
                    "severity": issue.get("severity", "high"),
                    "hours_to_fix": self._estimate_fix_time(issue) * 1.5,  # Security takes longer
                    "interest_per_month": self._estimate_ongoing_cost(issue) * 2,  # Higher ongoing risk
                })

        # From complexity
        complexity = code_metrics.get("complexity", 0)
        if complexity > 30:
            items.append({
                "type": "high_complexity",
                "category": "architecture",
                "description": f"High complexity ({complexity}) needs refactoring",
                "severity": "high",
                "hours_to_fix": complexity * 2,  # 2 hours per complexity point
                "interest_per_month": 20,  # Ongoing maintenance overhead
            })

        # From lack of tests
        test_coverage = code_metrics.get("test_coverage", 0)
        if test_coverage < 50:
            gap = 50 - test_coverage
            items.append({
                "type": "insufficient_tests",
                "category": "testing",
                "description": f"Test coverage at {test_coverage}% (target: 50%+)",
                "severity": "medium",
                "hours_to_fix": gap * 2,  # 2 hours per percentage point
                "interest_per_month": 30,  # Risk of bugs
            })

        # From documentation
        doc_score = quality_assessment.get("metrics", {}).get("documentation_score", 0)
        if doc_score < 0.5:
            items.append({
                "type": "poor_documentation",
                "category": "documentation",
                "description": f"Documentation score: {doc_score}/1.0",
                "severity": "low",
                "hours_to_fix": 40,  # Estimate for doc improvement
                "interest_per_month": 15,  # Onboarding overhead
            })

        return items

    def _estimate_fix_time(self, item: Dict[str, Any]) -> float:
        """Estimate hours to fix an item."""
        severity = item.get("severity", "medium")

        severity_multipliers = {
            "critical": 20,
            "high": 10,
            "medium": 5,
            "low": 2,
        }

        return severity_multipliers.get(severity, 5)

    def _estimate_ongoing_cost(self, item: Dict[str, Any]) -> float:
        """Estimate monthly ongoing cost (interest) of an item."""
        severity = item.get("severity", "medium")

        interest_rates = {
            "critical": 50,  # $50/month in overhead
            "high": 20,
            "medium": 10,
            "low": 5,
        }

        return interest_rates.get(severity, 10)

    def _calculate_interest(self, debt_items: List[Dict[str, Any]], hourly_rate: float) -> float:
        """Calculate total monthly interest."""
        return sum(item.get("interest_per_month", 0) for item in debt_items)

    def _prioritize_debt(self, debt_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prioritize debt items using effort/impact matrix."""
        priority_matrix = []

        for item in debt_items:
            effort = item["hours_to_fix"]
            impact = item["interest_per_month"]

            # Calculate priority score (higher is more urgent)
            priority_score = impact / max(effort, 1)  # ROI-based

            # Categorize into matrix
            if effort < 10 and impact > 20:
                quadrant = "quick_win"  # Low effort, high impact
            elif effort < 10 and impact <= 20:
                quadrant = "fill_in"  # Low effort, low impact
            elif effort >= 10 and impact > 20:
                quadrant = "major_project"  # High effort, high impact
            else:
                quadrant = "thankless_task"  # High effort, low impact

            priority_matrix.append({
                "item": item,
                "priority_score": priority_score,
                "quadrant": quadrant,
                "effort": "low" if effort < 10 else "high",
                "impact": "high" if impact > 20 else "low",
            })

        # Sort by priority score (descending)
        priority_matrix.sort(key=lambda x: x["priority_score"], reverse=True)

        return priority_matrix

    async def _ai_debt_analysis(self, analysis: Dict[str, Any], age_years: int) -> str:
        """Use AI for debt analysis insights."""

        prompt = f"""Analyze this technical debt situation:

System age: {age_years} years
Total debt: {analysis['total_debt_hours']} hours (${analysis['total_debt_cost']:,.2f})
Monthly interest: ${analysis['monthly_interest']}/month

Debt categories:
{chr(10).join(f"- {cat}: {info['count']} items, {info['total_hours']} hours" for cat, info in analysis['categories'].items())}

Top priority items:
{chr(10).join(f"- {p['item']['description']} (ROI: {p['priority_score']:.2f})" for p in analysis['priority_matrix'][:3])}

Provide:
1. Overall debt health assessment
2. Biggest concern
3. Recommended payoff strategy (big bang vs incremental)
4. Timeline estimate

Keep under 200 words."""

        response = await self.analyze_with_llm(
            prompt,
            context="You are a technical debt expert helping plan debt reduction.",
        )

        return response

    def _generate_debt_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate debt reduction recommendations."""
        recommendations = []

        # Based on total debt
        total_hours = analysis["total_debt_hours"]
        if total_hours > 500:
            recommendations.append("⚠️ CRITICAL: Over 500 hours of technical debt - immediate action required")
            recommendations.append("Consider dedicating 20% of sprint capacity to debt reduction")
        elif total_hours > 200:
            recommendations.append("High technical debt - allocate 1-2 days per sprint for debt paydown")

        # Based on interest
        monthly_interest = analysis["monthly_interest"]
        if monthly_interest > 100:
            recommendations.append(f"High monthly overhead (${monthly_interest}/mo) - prioritize quick wins")

        # Based on priority matrix
        quick_wins = [p for p in analysis["priority_matrix"] if p["quadrant"] == "quick_win"]
        if quick_wins:
            recommendations.append(f"Start with {len(quick_wins)} quick win items for fast ROI")

        # Category-specific
        categories = analysis["categories"]
        if "security" in categories and categories["security"]["count"] > 0:
            recommendations.append("🔒 Address security debt immediately - highest business risk")

        if "testing" in categories:
            recommendations.append("Implement 'boy scout rule': add tests when touching code")

        return recommendations

    def _generate_next_steps(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate concrete next steps."""
        steps = []

        # Top 3 priorities
        top_items = analysis["priority_matrix"][:3]
        for i, priority_item in enumerate(top_items, 1):
            item = priority_item["item"]
            steps.append(
                f"{i}. Fix {item['type']}: {item['description'][:60]}... "
                f"(Est: {item['hours_to_fix']}h, ROI: {priority_item['priority_score']:.1f})"
            )

        # Strategic steps
        steps.append("4. Create debt reduction backlog and track progress")
        steps.append("5. Set up automated code quality monitoring")
        steps.append("6. Schedule monthly debt review meetings")

        return steps
