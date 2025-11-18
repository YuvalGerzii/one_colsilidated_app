"""
Gig Economy & Hybrid Labor Integration Engine

Provides tools for workers to navigate the gig economy, stabilize income,
optimize benefits, and manage hybrid work arrangements.
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import random


class GigEconomyEngine:
    """
    Core engine for gig economy integration and income stabilization.
    Matches skills to gig opportunities, optimizes income streams, and provides
    financial planning for gig workers.
    """

    def __init__(self):
        # Platform databases - in production, integrate with real APIs
        self.gig_platforms = {
            "upwork": {"category": "professional_services", "avg_fee": 0.10, "volume": "high"},
            "fiverr": {"category": "creative_services", "avg_fee": 0.20, "volume": "high"},
            "toptal": {"category": "tech_consulting", "avg_fee": 0.00, "volume": "medium"},
            "freelancer": {"category": "general", "avg_fee": 0.10, "volume": "high"},
            "99designs": {"category": "design", "avg_fee": 0.15, "volume": "medium"},
            "guru": {"category": "professional_services", "avg_fee": 0.09, "volume": "medium"},
            "peopleperhour": {"category": "general", "avg_fee": 0.15, "volume": "medium"},
            "thumbtack": {"category": "local_services", "avg_fee": 0.20, "volume": "high"},
            "taskrabbit": {"category": "local_tasks", "avg_fee": 0.15, "volume": "high"},
            "uber": {"category": "transportation", "avg_fee": 0.25, "volume": "very_high"},
            "doordash": {"category": "delivery", "avg_fee": 0.20, "volume": "very_high"},
            "instacart": {"category": "delivery", "avg_fee": 0.15, "volume": "high"},
        }

        # Skill to gig opportunity mapping
        self.skill_gig_map = {
            "python": ["upwork", "toptal", "freelancer", "guru"],
            "javascript": ["upwork", "toptal", "freelancer", "guru"],
            "web_development": ["upwork", "toptal", "freelancer", "peopleperhour"],
            "data_analysis": ["upwork", "toptal", "freelancer"],
            "machine_learning": ["upwork", "toptal"],
            "graphic_design": ["fiverr", "99designs", "upwork", "freelancer"],
            "writing": ["upwork", "fiverr", "freelancer", "guru"],
            "video_editing": ["fiverr", "upwork", "freelancer"],
            "photography": ["fiverr", "99designs", "upwork"],
            "marketing": ["upwork", "fiverr", "freelancer", "guru"],
            "seo": ["upwork", "fiverr", "freelancer"],
            "social_media": ["upwork", "fiverr", "freelancer"],
            "accounting": ["upwork", "freelancer", "guru"],
            "legal": ["upwork", "freelancer"],
            "translation": ["upwork", "fiverr", "freelancer"],
            "tutoring": ["upwork", "freelancer"],
            "consulting": ["toptal", "upwork", "freelancer"],
            "project_management": ["upwork", "freelancer", "guru"],
            "virtual_assistant": ["upwork", "fiverr", "freelancer"],
            "customer_service": ["upwork", "freelancer"],
            "delivery": ["doordash", "instacart", "uber"],
            "driving": ["uber", "doordash"],
            "handyman": ["thumbtack", "taskrabbit"],
            "cleaning": ["thumbtack", "taskrabbit"],
            "moving": ["thumbtack", "taskrabbit"],
        }

        # Gig task templates with earning potential
        self.gig_tasks = {
            "web_development": [
                {"task": "Build landing page", "avg_rate": 500, "time_hours": 8, "difficulty": "medium"},
                {"task": "Full website development", "avg_rate": 3000, "time_hours": 80, "difficulty": "high"},
                {"task": "Bug fixes", "avg_rate": 100, "time_hours": 2, "difficulty": "low"},
                {"task": "WordPress customization", "avg_rate": 300, "time_hours": 5, "difficulty": "low"},
                {"task": "E-commerce setup", "avg_rate": 1500, "time_hours": 40, "difficulty": "medium"},
            ],
            "graphic_design": [
                {"task": "Logo design", "avg_rate": 300, "time_hours": 5, "difficulty": "medium"},
                {"task": "Social media graphics (10 pack)", "avg_rate": 150, "time_hours": 4, "difficulty": "low"},
                {"task": "Branding package", "avg_rate": 1200, "time_hours": 20, "difficulty": "high"},
                {"task": "Flyer design", "avg_rate": 100, "time_hours": 2, "difficulty": "low"},
                {"task": "Infographic design", "avg_rate": 250, "time_hours": 6, "difficulty": "medium"},
            ],
            "writing": [
                {"task": "Blog post (1000 words)", "avg_rate": 100, "time_hours": 2, "difficulty": "low"},
                {"task": "Technical documentation", "avg_rate": 500, "time_hours": 10, "difficulty": "high"},
                {"task": "Product descriptions (10 pack)", "avg_rate": 150, "time_hours": 3, "difficulty": "low"},
                {"task": "Copywriting for website", "avg_rate": 400, "time_hours": 8, "difficulty": "medium"},
                {"task": "White paper", "avg_rate": 1000, "time_hours": 20, "difficulty": "high"},
            ],
            "data_analysis": [
                {"task": "Data cleaning & analysis", "avg_rate": 400, "time_hours": 8, "difficulty": "medium"},
                {"task": "Dashboard creation", "avg_rate": 600, "time_hours": 12, "difficulty": "medium"},
                {"task": "Statistical analysis report", "avg_rate": 800, "time_hours": 16, "difficulty": "high"},
                {"task": "Excel automation", "avg_rate": 200, "time_hours": 4, "difficulty": "low"},
            ],
            "machine_learning": [
                {"task": "Build prediction model", "avg_rate": 1500, "time_hours": 40, "difficulty": "high"},
                {"task": "Data preprocessing pipeline", "avg_rate": 600, "time_hours": 12, "difficulty": "medium"},
                {"task": "Model fine-tuning", "avg_rate": 800, "time_hours": 16, "difficulty": "high"},
            ],
            "delivery": [
                {"task": "Food delivery (per order)", "avg_rate": 8, "time_hours": 0.5, "difficulty": "low"},
                {"task": "Grocery delivery", "avg_rate": 15, "time_hours": 1, "difficulty": "low"},
                {"task": "Package delivery", "avg_rate": 12, "time_hours": 0.75, "difficulty": "low"},
            ],
            "driving": [
                {"task": "Rideshare (per hour)", "avg_rate": 20, "time_hours": 1, "difficulty": "low"},
                {"task": "Airport trip", "avg_rate": 45, "time_hours": 1.5, "difficulty": "low"},
            ],
            "tutoring": [
                {"task": "Online tutoring session (1 hour)", "avg_rate": 40, "time_hours": 1, "difficulty": "medium"},
                {"task": "Test prep package (10 hours)", "avg_rate": 500, "time_hours": 10, "difficulty": "high"},
            ],
        }

    def match_skills_to_gigs(
        self,
        worker_skills: List[str],
        availability_hours_weekly: int,
        income_target_monthly: float,
        preferences: Optional[Dict] = None
    ) -> Dict:
        """
        Match worker skills to gig opportunities across multiple platforms.

        Args:
            worker_skills: List of worker's skills
            availability_hours_weekly: Hours available per week for gig work
            income_target_monthly: Desired monthly income from gigs
            preferences: Optional preferences (remote_only, local_only, etc.)

        Returns:
            Matched gig opportunities with earning potential and recommendations
        """
        preferences = preferences or {}
        remote_only = preferences.get("remote_only", False)

        # Find matching platforms for each skill
        matched_opportunities = []

        for skill in worker_skills:
            if skill not in self.skill_gig_map:
                continue

            platforms = self.skill_gig_map[skill]

            # Filter local vs remote based on preferences
            filtered_platforms = []
            for platform in platforms:
                platform_info = self.gig_platforms.get(platform, {})
                is_local = platform_info.get("category") in ["local_services", "local_tasks", "transportation", "delivery"]

                if remote_only and is_local:
                    continue

                filtered_platforms.append(platform)

            # Get task opportunities for this skill
            tasks = self.gig_tasks.get(skill, [])

            for platform in filtered_platforms:
                platform_info = self.gig_platforms[platform]

                for task in tasks:
                    # Calculate actual earnings after platform fees
                    platform_fee = platform_info["avg_fee"]
                    net_rate = task["avg_rate"] * (1 - platform_fee)
                    hourly_rate = net_rate / task["time_hours"]

                    # Calculate monthly potential if worker does this regularly
                    # Assume they can do this task multiple times per month based on hours
                    tasks_per_month = min(
                        int(availability_hours_weekly * 4.33 / task["time_hours"]),
                        20  # Cap at 20 tasks per month for variety
                    )
                    monthly_potential = net_rate * tasks_per_month

                    matched_opportunities.append({
                        "skill": skill,
                        "platform": platform,
                        "platform_category": platform_info["category"],
                        "platform_volume": platform_info["volume"],
                        "task": task["task"],
                        "gross_rate": task["avg_rate"],
                        "platform_fee_pct": platform_fee * 100,
                        "net_rate": round(net_rate, 2),
                        "hourly_rate": round(hourly_rate, 2),
                        "time_hours": task["time_hours"],
                        "difficulty": task["difficulty"],
                        "tasks_per_month_potential": tasks_per_month,
                        "monthly_income_potential": round(monthly_potential, 2),
                        "match_score": self._calculate_gig_match_score(
                            task, hourly_rate, platform_info, income_target_monthly
                        )
                    })

        # Sort by match score
        matched_opportunities.sort(key=lambda x: x["match_score"], reverse=True)

        # Create income optimization strategy
        top_opportunities = matched_opportunities[:15]
        income_strategy = self._create_income_optimization_strategy(
            top_opportunities,
            availability_hours_weekly,
            income_target_monthly
        )

        return {
            "total_opportunities": len(matched_opportunities),
            "top_opportunities": top_opportunities,
            "income_optimization_strategy": income_strategy,
            "platforms_to_join": list(set([opp["platform"] for opp in top_opportunities[:10]])),
            "estimated_setup_time_hours": len(set([opp["platform"] for opp in top_opportunities[:10]])) * 2,
            "recommendations": self._generate_gig_recommendations(
                matched_opportunities, income_target_monthly, availability_hours_weekly
            )
        }

    def _calculate_gig_match_score(
        self,
        task: Dict,
        hourly_rate: float,
        platform_info: Dict,
        income_target: float
    ) -> int:
        """Calculate match score (0-100) for a gig opportunity."""
        score = 0

        # Hourly rate scoring (0-40 points)
        if hourly_rate >= 100:
            score += 40
        elif hourly_rate >= 50:
            score += 30
        elif hourly_rate >= 25:
            score += 20
        else:
            score += 10

        # Platform volume scoring (0-20 points)
        volume_scores = {"very_high": 20, "high": 15, "medium": 10, "low": 5}
        score += volume_scores.get(platform_info["volume"], 5)

        # Difficulty scoring - prefer medium difficulty (0-20 points)
        difficulty_scores = {"low": 15, "medium": 20, "high": 10}
        score += difficulty_scores.get(task["difficulty"], 10)

        # Time efficiency scoring (0-20 points)
        if task["time_hours"] <= 5:
            score += 20
        elif task["time_hours"] <= 20:
            score += 15
        else:
            score += 10

        return min(score, 100)

    def _create_income_optimization_strategy(
        self,
        opportunities: List[Dict],
        hours_available: int,
        income_target: float
    ) -> Dict:
        """Create optimized income strategy from multiple gig opportunities."""
        if not opportunities:
            return {"error": "No opportunities available"}

        # Greedy algorithm: select highest hourly rate tasks that fit in time budget
        selected_gigs = []
        total_hours = 0
        total_income = 0
        monthly_hours = hours_available * 4.33

        # Sort by hourly rate
        sorted_opps = sorted(opportunities, key=lambda x: x["hourly_rate"], reverse=True)

        for opp in sorted_opps:
            # Calculate how many times we can do this task
            tasks_possible = int((monthly_hours - total_hours) / opp["time_hours"])

            if tasks_possible > 0:
                # Limit to reasonable number per task type
                tasks_to_add = min(tasks_possible, 8)
                hours_needed = tasks_to_add * opp["time_hours"]
                income_earned = tasks_to_add * opp["net_rate"]

                selected_gigs.append({
                    "task": opp["task"],
                    "platform": opp["platform"],
                    "count_per_month": tasks_to_add,
                    "hours_per_month": round(hours_needed, 1),
                    "income_per_month": round(income_earned, 2),
                    "hourly_rate": opp["hourly_rate"]
                })

                total_hours += hours_needed
                total_income += income_earned

                # If we hit income target, stop
                if total_income >= income_target:
                    break

        gap_to_target = income_target - total_income
        gap_percentage = (gap_to_target / income_target * 100) if income_target > 0 else 0

        return {
            "selected_gigs": selected_gigs,
            "total_monthly_income": round(total_income, 2),
            "total_monthly_hours": round(total_hours, 1),
            "average_hourly_rate": round(total_income / total_hours, 2) if total_hours > 0 else 0,
            "income_target": income_target,
            "gap_to_target": round(gap_to_target, 2),
            "target_achievement_pct": round(min(total_income / income_target * 100, 100), 1) if income_target > 0 else 100,
            "feasibility": "achievable" if gap_percentage <= 0 else "challenging" if gap_percentage <= 30 else "unrealistic"
        }

    def _generate_gig_recommendations(
        self,
        opportunities: List[Dict],
        income_target: float,
        hours_available: int
    ) -> List[str]:
        """Generate personalized recommendations for gig work success."""
        recommendations = []

        if not opportunities:
            recommendations.append("Learn new skills to unlock gig opportunities")
            recommendations.append("Start with delivery/driving gigs for immediate income")
            return recommendations

        avg_hourly = sum(o["hourly_rate"] for o in opportunities[:10]) / min(len(opportunities), 10)

        if avg_hourly < 25:
            recommendations.append("Focus on upskilling to access higher-paying gigs (target $50+/hr)")

        high_value_skills = [o["skill"] for o in opportunities if o["hourly_rate"] > 50]
        if high_value_skills:
            recommendations.append(f"Your high-value skills: {', '.join(set(high_value_skills[:3]))} - prioritize these")

        platform_diversity = len(set(o["platform"] for o in opportunities[:10]))
        if platform_diversity < 3:
            recommendations.append("Diversify across 3-5 platforms to reduce income volatility")

        monthly_potential = hours_available * 4.33 * avg_hourly
        if monthly_potential < income_target:
            shortfall_pct = (income_target - monthly_potential) / income_target * 100
            recommendations.append(f"Income target may be challenging ({shortfall_pct:.0f}% shortfall) - consider increasing hours or rates")

        recommendations.append("Build a strong profile with reviews on top 2-3 platforms first")
        recommendations.append("Start with smaller projects to build reputation, then increase rates")

        return recommendations

    def calculate_income_stabilization_plan(
        self,
        current_income_sources: List[Dict],
        monthly_expenses: float,
        emergency_fund_months: int = 6,
        risk_tolerance: str = "moderate"
    ) -> Dict:
        """
        Create income stabilization plan for gig workers with multiple income streams.

        Args:
            current_income_sources: List of current income sources with amounts and volatility
            monthly_expenses: Monthly expenses
            emergency_fund_months: Target months of expenses in emergency fund
            risk_tolerance: low, moderate, high

        Returns:
            Income stabilization strategy with diversification recommendations
        """
        total_monthly_income = sum(source.get("monthly_avg", 0) for source in current_income_sources)

        # Calculate income volatility (coefficient of variation)
        volatility_scores = []
        for source in current_income_sources:
            volatility = source.get("volatility", "medium")
            volatility_map = {"low": 10, "medium": 30, "high": 60}
            volatility_scores.append(volatility_map.get(volatility, 30))

        avg_volatility = sum(volatility_scores) / len(volatility_scores) if volatility_scores else 30

        # Calculate Herfindahl index for income concentration (0-10000, higher = more concentrated)
        income_shares = [(s.get("monthly_avg", 0) / total_monthly_income * 100) for s in current_income_sources]
        herfindahl = sum(share ** 2 for share in income_shares)

        # Recommendations based on concentration
        diversification_status = "well_diversified" if herfindahl < 3000 else "moderately_concentrated" if herfindahl < 6000 else "highly_concentrated"

        # Emergency fund target
        emergency_fund_target = monthly_expenses * emergency_fund_months

        # Income buffer recommendation based on volatility
        buffer_multiplier = 1.5 if avg_volatility > 40 else 1.3 if avg_volatility > 25 else 1.2
        recommended_monthly_income = monthly_expenses * buffer_multiplier

        income_gap = recommended_monthly_income - total_monthly_income

        # Diversification recommendations
        diversification_recommendations = []

        if herfindahl > 5000:
            diversification_recommendations.append("High income concentration detected - add 2-3 new income streams")

        if len(current_income_sources) < 3:
            diversification_recommendations.append(f"Add {3 - len(current_income_sources)} more income sources for stability")

        if avg_volatility > 40:
            diversification_recommendations.append("High income volatility - prioritize adding stable income sources (part-time W2, retainer clients)")

        # Income stream types to add based on risk tolerance
        risk_profiles = {
            "low": ["part_time_w2", "retainer_clients", "passive_income"],
            "moderate": ["high_value_gigs", "retainer_clients", "project_work"],
            "high": ["high_rate_projects", "speculative_gigs", "commission_work"]
        }

        suggested_stream_types = risk_profiles.get(risk_tolerance, risk_profiles["moderate"])

        return {
            "current_situation": {
                "total_monthly_income": round(total_monthly_income, 2),
                "monthly_expenses": monthly_expenses,
                "surplus_deficit": round(total_monthly_income - monthly_expenses, 2),
                "income_sources_count": len(current_income_sources),
                "avg_volatility_pct": round(avg_volatility, 1),
                "concentration_index": round(herfindahl, 0),
                "diversification_status": diversification_status
            },
            "recommendations": {
                "recommended_monthly_income": round(recommended_monthly_income, 2),
                "income_gap": round(income_gap, 2),
                "emergency_fund_target": round(emergency_fund_target, 2),
                "buffer_multiplier": buffer_multiplier,
                "suggested_new_stream_types": suggested_stream_types,
                "diversification_actions": diversification_recommendations
            },
            "stability_score": self._calculate_stability_score(
                herfindahl, avg_volatility, total_monthly_income, monthly_expenses
            ),
            "risk_assessment": {
                "income_volatility": "high" if avg_volatility > 40 else "moderate" if avg_volatility > 25 else "low",
                "concentration_risk": "high" if herfindahl > 6000 else "moderate" if herfindahl > 3000 else "low",
                "adequacy_risk": "high" if income_gap > monthly_expenses * 0.3 else "moderate" if income_gap > 0 else "low"
            }
        }

    def _calculate_stability_score(
        self,
        herfindahl: float,
        volatility: float,
        income: float,
        expenses: float
    ) -> Dict:
        """Calculate overall income stability score (0-100)."""
        score = 100

        # Deduct for concentration
        if herfindahl > 6000:
            score -= 30
        elif herfindahl > 3000:
            score -= 15

        # Deduct for volatility
        if volatility > 40:
            score -= 25
        elif volatility > 25:
            score -= 15

        # Deduct for income inadequacy
        surplus_ratio = (income - expenses) / expenses if expenses > 0 else 0
        if surplus_ratio < 0.2:
            score -= 20
        elif surplus_ratio < 0.5:
            score -= 10

        score = max(0, score)

        rating = "excellent" if score >= 80 else "good" if score >= 60 else "fair" if score >= 40 else "poor"

        return {
            "score": score,
            "rating": rating,
            "interpretation": f"Your income stability is {rating}. " +
                           ("Focus on diversification and building emergency fund." if score < 60 else
                            "Continue building diverse income streams." if score < 80 else
                            "Well-positioned for income stability.")
        }

    def optimize_gig_portfolio(
        self,
        worker_id: int,
        current_gigs: List[Dict],
        available_hours_weekly: int,
        target_monthly_income: float
    ) -> Dict:
        """
        Analyze current gig portfolio and suggest optimizations.

        Args:
            worker_id: Worker ID
            current_gigs: Current gig engagements
            available_hours_weekly: Available hours per week
            target_monthly_income: Income target

        Returns:
            Portfolio analysis with optimization suggestions
        """
        if not current_gigs:
            return {
                "error": "No current gigs to optimize",
                "recommendation": "Start by matching your skills to gig opportunities"
            }

        # Calculate current performance
        total_monthly_hours = sum(g.get("hours_per_month", 0) for g in current_gigs)
        total_monthly_income = sum(g.get("income_per_month", 0) for g in current_gigs)
        current_avg_hourly = total_monthly_income / total_monthly_hours if total_monthly_hours > 0 else 0

        # Analyze each gig's performance
        gig_analysis = []
        for gig in current_gigs:
            hours = gig.get("hours_per_month", 0)
            income = gig.get("income_per_month", 0)
            hourly = income / hours if hours > 0 else 0

            # Performance vs average
            performance = "above_average" if hourly > current_avg_hourly * 1.2 else "average" if hourly > current_avg_hourly * 0.8 else "below_average"

            gig_analysis.append({
                "gig": gig.get("name", "Unknown"),
                "platform": gig.get("platform", "Unknown"),
                "hours_per_month": hours,
                "income_per_month": income,
                "hourly_rate": round(hourly, 2),
                "performance": performance,
                "recommendation": "keep" if performance != "below_average" else "optimize_or_replace"
            })

        # Identify low performers
        low_performers = [g for g in gig_analysis if g["performance"] == "below_average"]

        # Calculate optimization potential
        monthly_hours_available = available_hours_weekly * 4.33
        unused_hours = monthly_hours_available - total_monthly_hours

        # If we replace low performers with average rate gigs
        low_performer_hours = sum(g["hours_per_month"] for g in low_performers)
        potential_gain = low_performer_hours * current_avg_hourly - sum(g["income_per_month"] for g in low_performers)

        # Additional income from unused hours
        additional_potential = unused_hours * current_avg_hourly

        optimized_income = total_monthly_income + potential_gain + additional_potential

        return {
            "current_portfolio": {
                "total_gigs": len(current_gigs),
                "monthly_hours": round(total_monthly_hours, 1),
                "monthly_income": round(total_monthly_income, 2),
                "average_hourly_rate": round(current_avg_hourly, 2),
                "hours_utilized_pct": round(total_monthly_hours / monthly_hours_available * 100, 1)
            },
            "gig_analysis": gig_analysis,
            "optimization_opportunities": {
                "unused_hours_per_month": round(unused_hours, 1),
                "low_performing_gigs": len(low_performers),
                "potential_gain_from_replacement": round(potential_gain, 2),
                "potential_gain_from_unused_hours": round(additional_potential, 2),
                "total_optimization_potential": round(potential_gain + additional_potential, 2),
                "optimized_monthly_income": round(optimized_income, 2)
            },
            "recommendations": self._generate_portfolio_recommendations(
                gig_analysis, unused_hours, target_monthly_income, optimized_income
            ),
            "action_plan": {
                "immediate": [
                    f"Replace or negotiate higher rates for {len(low_performers)} low-performing gigs",
                    f"Utilize {round(unused_hours, 1)} unused hours per month"
                ],
                "short_term": [
                    "Aim to increase average hourly rate by 20% through rate negotiation",
                    "Focus on platforms with highest volume and best rates"
                ],
                "long_term": [
                    "Build premium client base for retainer work",
                    "Develop passive income streams to reduce time-for-money dependency"
                ]
            }
        }

    def _generate_portfolio_recommendations(
        self,
        gig_analysis: List[Dict],
        unused_hours: float,
        income_target: float,
        optimized_income: float
    ) -> List[str]:
        """Generate portfolio optimization recommendations."""
        recommendations = []

        low_performers = [g for g in gig_analysis if g["performance"] == "below_average"]
        if low_performers:
            recommendations.append(f"Replace {len(low_performers)} low-performing gigs with higher-value opportunities")

        if unused_hours > 20:
            recommendations.append(f"You have {round(unused_hours, 1)} unused hours/month - fill with high-value gigs")

        if optimized_income >= income_target:
            recommendations.append("Income target is achievable with portfolio optimization")
        else:
            gap = income_target - optimized_income
            recommendations.append(f"Even optimized, you're ${round(gap, 0)} short of target - consider upskilling or increasing hours")

        platform_diversity = len(set(g["platform"] for g in gig_analysis))
        if platform_diversity < 3:
            recommendations.append("Diversify across more platforms to reduce dependency risk")

        return recommendations


class GigBenefitsCalculator:
    """
    Calculate benefits costs and tax implications for gig workers.
    Helps gig workers understand total compensation including benefits they need to self-fund.
    """

    def calculate_benefits_package(
        self,
        annual_gig_income: float,
        state: str = "CA",
        age: int = 30,
        dependents: int = 0,
        retirement_contribution_pct: float = 10.0
    ) -> Dict:
        """
        Calculate comprehensive benefits package costs for gig worker.

        Args:
            annual_gig_income: Projected annual income from gig work
            state: State (for tax calculations)
            age: Worker age (for health insurance estimates)
            dependents: Number of dependents
            retirement_contribution_pct: Percentage to contribute to retirement

        Returns:
            Complete benefits cost breakdown and recommendations
        """
        # Health insurance estimates (monthly) - based on marketplace averages
        health_insurance_costs = self._estimate_health_insurance(age, dependents, annual_gig_income)

        # Retirement calculations
        retirement_contribution = annual_gig_income * (retirement_contribution_pct / 100)

        # Tax estimates
        tax_estimates = self._estimate_taxes(annual_gig_income, state)

        # Other benefits
        disability_insurance_monthly = self._estimate_disability_insurance(annual_gig_income, age)
        life_insurance_monthly = self._estimate_life_insurance(age, dependents)

        # Total annual costs
        total_health_annual = health_insurance_costs["monthly_premium"] * 12 + health_insurance_costs["estimated_out_of_pocket"]
        total_retirement_annual = retirement_contribution
        total_disability_annual = disability_insurance_monthly * 12
        total_life_annual = life_insurance_monthly * 12

        total_benefits_cost_annual = (
            total_health_annual +
            total_retirement_annual +
            total_disability_annual +
            total_life_annual
        )

        total_taxes_annual = tax_estimates["total_tax"]

        # Net income after taxes and benefits
        net_annual_income = annual_gig_income - total_taxes_annual - total_benefits_cost_annual
        net_monthly_income = net_annual_income / 12

        # Effective hourly rate (assuming 2080 hours/year)
        effective_hourly_rate = net_annual_income / 2080

        # Comparison with W2 equivalent
        w2_equivalent = self._calculate_w2_equivalent(annual_gig_income, total_benefits_cost_annual)

        return {
            "income": {
                "annual_gig_income": round(annual_gig_income, 2),
                "monthly_gig_income": round(annual_gig_income / 12, 2)
            },
            "health_insurance": {
                "monthly_premium": round(health_insurance_costs["monthly_premium"], 2),
                "annual_premium": round(health_insurance_costs["monthly_premium"] * 12, 2),
                "deductible": health_insurance_costs["deductible"],
                "estimated_out_of_pocket": health_insurance_costs["estimated_out_of_pocket"],
                "total_annual_cost": round(total_health_annual, 2),
                "subsidy_eligible": health_insurance_costs["subsidy_eligible"]
            },
            "retirement": {
                "contribution_pct": retirement_contribution_pct,
                "annual_contribution": round(retirement_contribution, 2),
                "monthly_contribution": round(retirement_contribution / 12, 2),
                "account_type": "Solo 401(k) or SEP IRA",
                "tax_benefit": round(retirement_contribution * 0.25, 2)  # Assuming 25% tax bracket
            },
            "insurance": {
                "disability_insurance_monthly": round(disability_insurance_monthly, 2),
                "disability_insurance_annual": round(total_disability_annual, 2),
                "life_insurance_monthly": round(life_insurance_monthly, 2),
                "life_insurance_annual": round(total_life_annual, 2)
            },
            "taxes": tax_estimates,
            "summary": {
                "gross_annual_income": round(annual_gig_income, 2),
                "total_taxes": round(total_taxes_annual, 2),
                "total_benefits_cost": round(total_benefits_cost_annual, 2),
                "net_annual_income": round(net_annual_income, 2),
                "net_monthly_income": round(net_monthly_income, 2),
                "effective_hourly_rate": round(effective_hourly_rate, 2),
                "total_deductions_pct": round((total_taxes_annual + total_benefits_cost_annual) / annual_gig_income * 100, 1)
            },
            "w2_comparison": w2_equivalent,
            "recommendations": self._generate_benefits_recommendations(
                annual_gig_income, retirement_contribution_pct, health_insurance_costs
            )
        }

    def _estimate_health_insurance(self, age: int, dependents: int, income: float) -> Dict:
        """Estimate health insurance costs based on marketplace averages."""
        # Base premium (rough estimates, vary widely by location)
        base_premium = 450 if age < 30 else 550 if age < 50 else 700

        # Add for dependents
        premium = base_premium + (dependents * 250)

        # Subsidy eligibility (simplified - based on federal poverty level multiples)
        fpl_threshold = 54360 + (dependents * 19720)  # 400% FPL for subsidy cutoff
        subsidy_eligible = income < fpl_threshold

        if subsidy_eligible:
            # Rough subsidy estimate
            premium = premium * 0.6

        return {
            "monthly_premium": premium,
            "deductible": 4500,
            "estimated_out_of_pocket": 2000,
            "subsidy_eligible": subsidy_eligible
        }

    def _estimate_disability_insurance(self, annual_income: float, age: int) -> float:
        """Estimate disability insurance monthly premium."""
        monthly_income = annual_income / 12
        coverage_amount = min(monthly_income * 0.6, 10000)  # Typically 60% of income

        # Rough premium: 1-3% of annual income
        premium_pct = 0.015 if age < 40 else 0.02
        annual_premium = annual_income * premium_pct

        return annual_premium / 12

    def _estimate_life_insurance(self, age: int, dependents: int) -> float:
        """Estimate term life insurance monthly premium."""
        if dependents == 0:
            return 0  # Optional without dependents

        # $500k coverage estimate
        if age < 30:
            monthly = 25
        elif age < 40:
            monthly = 35
        elif age < 50:
            monthly = 60
        else:
            monthly = 100

        return monthly

    def _estimate_taxes(self, annual_income: float, state: str) -> Dict:
        """Estimate federal, state, and self-employment taxes."""
        # Self-employment tax (15.3% on 92.35% of income)
        se_tax_base = annual_income * 0.9235
        se_tax = se_tax_base * 0.153

        # Federal income tax (simplified brackets)
        taxable_income = annual_income - (se_tax / 2)  # Deduct half of SE tax

        if taxable_income <= 11000:
            federal_tax = taxable_income * 0.10
        elif taxable_income <= 44725:
            federal_tax = 1100 + (taxable_income - 11000) * 0.12
        elif taxable_income <= 95375:
            federal_tax = 5147 + (taxable_income - 44725) * 0.22
        elif taxable_income <= 182100:
            federal_tax = 16290 + (taxable_income - 95375) * 0.24
        else:
            federal_tax = 37104 + (taxable_income - 182100) * 0.32

        # State tax (simplified - using CA as example)
        state_tax_rate = 0.08 if state == "CA" else 0.05  # Rough estimates
        state_tax = taxable_income * state_tax_rate

        total_tax = se_tax + federal_tax + state_tax
        effective_rate = total_tax / annual_income * 100

        return {
            "self_employment_tax": round(se_tax, 2),
            "federal_income_tax": round(federal_tax, 2),
            "state_income_tax": round(state_tax, 2),
            "total_tax": round(total_tax, 2),
            "effective_tax_rate_pct": round(effective_rate, 1),
            "quarterly_payment_estimate": round(total_tax / 4, 2)
        }

    def _calculate_w2_equivalent(self, gig_income: float, benefits_cost: float) -> Dict:
        """Calculate what W2 salary would be equivalent to gig income."""
        # W2 employer typically pays:
        # - 7.65% FICA (vs 15.3% self-employment)
        # - ~20-30% benefits (health, retirement, etc.)

        # For equivalent take-home, W2 can be lower
        w2_fica_savings = gig_income * 0.0765
        w2_benefits_savings = benefits_cost

        # Rough equivalent W2 salary
        equivalent_w2 = gig_income - w2_fica_savings - (w2_benefits_savings * 0.7)

        return {
            "gig_income": round(gig_income, 2),
            "equivalent_w2_salary": round(equivalent_w2, 2),
            "difference": round(gig_income - equivalent_w2, 2),
            "explanation": f"Your ${round(gig_income, 0):,.0f} gig income is roughly equivalent to a ${round(equivalent_w2, 0):,.0f} W2 salary when accounting for benefits and taxes"
        }

    def _generate_benefits_recommendations(
        self,
        income: float,
        retirement_pct: float,
        health_info: Dict
    ) -> List[str]:
        """Generate benefits optimization recommendations."""
        recommendations = []

        if retirement_pct < 15:
            recommendations.append("Consider increasing retirement contributions to 15-20% for better long-term security")

        if health_info["subsidy_eligible"]:
            recommendations.append("You may qualify for ACA subsidies - apply at healthcare.gov to reduce premiums")

        recommendations.append("Open a Solo 401(k) or SEP IRA for tax-advantaged retirement savings")
        recommendations.append("Set aside 25-30% of each payment for quarterly tax payments")
        recommendations.append("Consider an HSA (Health Savings Account) if using high-deductible health plan for triple tax advantage")
        recommendations.append("Track all business expenses (home office, equipment, mileage) for tax deductions")

        if income > 100000:
            recommendations.append("Consult with CPA about S-Corp election to potentially reduce self-employment taxes")

        return recommendations


class HybridWorkOptimizer:
    """
    Optimize schedules for workers combining full-time/part-time W2 work with gig work.
    """

    def optimize_hybrid_schedule(
        self,
        w2_job: Dict,
        gig_opportunities: List[Dict],
        weekly_hours_available: int,
        optimization_goal: str = "max_income"
    ) -> Dict:
        """
        Optimize work schedule combining W2 and gig work.

        Args:
            w2_job: Current W2 job details (hours, income, flexibility)
            gig_opportunities: Available gig opportunities
            weekly_hours_available: Total hours available for work per week
            optimization_goal: 'max_income', 'work_life_balance', or 'skill_building'

        Returns:
            Optimized schedule with income projections and recommendations
        """
        w2_hours = w2_job.get("hours_per_week", 40)
        w2_monthly_income = w2_job.get("monthly_income", 0)
        w2_flexibility = w2_job.get("flexibility", "low")  # low, medium, high

        # Available hours for gig work
        gig_hours_available = weekly_hours_available - w2_hours

        if gig_hours_available <= 0:
            return {
                "error": "No hours available for gig work",
                "recommendation": "Consider reducing W2 hours or increasing total available hours"
            }

        # Sort gigs based on optimization goal
        if optimization_goal == "max_income":
            sorted_gigs = sorted(gig_opportunities, key=lambda x: x.get("hourly_rate", 0), reverse=True)
        elif optimization_goal == "skill_building":
            sorted_gigs = sorted(gig_opportunities, key=lambda x: (x.get("skill_value", 0), x.get("hourly_rate", 0)), reverse=True)
        else:  # work_life_balance
            sorted_gigs = sorted(gig_opportunities, key=lambda x: x.get("flexibility_score", 0), reverse=True)

        # Select gigs to fill available hours
        selected_gigs = []
        total_gig_hours = 0
        total_gig_income = 0

        for gig in sorted_gigs:
            gig_hours = gig.get("hours_per_week", 0)

            if total_gig_hours + gig_hours <= gig_hours_available:
                selected_gigs.append(gig)
                total_gig_hours += gig_hours
                total_gig_income += gig.get("weekly_income", 0)

        monthly_gig_income = total_gig_income * 4.33
        total_monthly_income = w2_monthly_income + monthly_gig_income

        # Calculate burnout risk
        total_work_hours = w2_hours + total_gig_hours
        burnout_risk = self._calculate_burnout_risk(total_work_hours, w2_flexibility, len(selected_gigs))

        return {
            "schedule": {
                "w2_hours_per_week": w2_hours,
                "gig_hours_per_week": round(total_gig_hours, 1),
                "total_work_hours_per_week": round(total_work_hours, 1),
                "free_hours_per_week": round(weekly_hours_available - total_work_hours, 1)
            },
            "income": {
                "w2_monthly_income": round(w2_monthly_income, 2),
                "gig_monthly_income": round(monthly_gig_income, 2),
                "total_monthly_income": round(total_monthly_income, 2),
                "gig_income_percentage": round(monthly_gig_income / total_monthly_income * 100, 1) if total_monthly_income > 0 else 0
            },
            "selected_gigs": selected_gigs,
            "burnout_assessment": burnout_risk,
            "sustainability_score": self._calculate_sustainability_score(
                total_work_hours, w2_flexibility, monthly_gig_income, total_monthly_income
            ),
            "recommendations": self._generate_hybrid_recommendations(
                total_work_hours, burnout_risk, w2_flexibility, len(selected_gigs)
            )
        }

    def _calculate_burnout_risk(self, total_hours: float, flexibility: str, num_gigs: int) -> Dict:
        """Calculate burnout risk based on work hours and schedule complexity."""
        risk_score = 0

        # Hours-based risk
        if total_hours > 60:
            risk_score += 40
        elif total_hours > 50:
            risk_score += 25
        elif total_hours > 40:
            risk_score += 10

        # Flexibility helps reduce risk
        flexibility_reduction = {"high": 15, "medium": 5, "low": 0}
        risk_score -= flexibility_reduction.get(flexibility, 0)

        # Multiple gigs increase complexity
        if num_gigs > 3:
            risk_score += 20
        elif num_gigs > 1:
            risk_score += 10

        risk_score = max(0, min(100, risk_score))

        risk_level = "high" if risk_score > 60 else "moderate" if risk_score > 30 else "low"

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "warning": "Unsustainable workload - burnout likely" if risk_score > 60 else
                      "Manageable but monitor stress levels" if risk_score > 30 else
                      "Sustainable workload"
        }

    def _calculate_sustainability_score(
        self,
        total_hours: float,
        flexibility: str,
        gig_income: float,
        total_income: float
    ) -> Dict:
        """Calculate long-term sustainability score (0-100)."""
        score = 100

        # Deduct for excessive hours
        if total_hours > 55:
            score -= 30
        elif total_hours > 45:
            score -= 15

        # Add for flexibility
        flexibility_bonus = {"high": 15, "medium": 5, "low": 0}
        score += flexibility_bonus.get(flexibility, 0)

        # Deduct if too dependent on gig income
        gig_dependency = gig_income / total_income if total_income > 0 else 0
        if gig_dependency > 0.5:
            score -= 20
        elif gig_dependency > 0.3:
            score -= 10

        score = max(0, min(100, score))

        rating = "excellent" if score >= 80 else "good" if score >= 60 else "concerning" if score >= 40 else "unsustainable"

        return {
            "score": score,
            "rating": rating
        }

    def _generate_hybrid_recommendations(
        self,
        total_hours: float,
        burnout_risk: Dict,
        flexibility: str,
        num_gigs: int
    ) -> List[str]:
        """Generate recommendations for hybrid work arrangement."""
        recommendations = []

        if burnout_risk["risk_level"] == "high":
            recommendations.append("CRITICAL: Reduce total hours to below 55/week to prevent burnout")
            recommendations.append("Consider replacing low-value gigs with rest time")

        if total_hours > 50:
            recommendations.append("Schedule at least 1-2 full rest days per week")
            recommendations.append("Use time-blocking to separate W2 and gig work")

        if flexibility == "low":
            recommendations.append("Seek to increase W2 flexibility (remote work, flex hours) to reduce stress")

        if num_gigs > 3:
            recommendations.append("Consolidate gigs - focus on top 2-3 highest-value opportunities")

        recommendations.append("Build 3-month emergency fund to reduce pressure from gig income dependency")
        recommendations.append("Track time and income weekly to identify inefficiencies")

        return recommendations
