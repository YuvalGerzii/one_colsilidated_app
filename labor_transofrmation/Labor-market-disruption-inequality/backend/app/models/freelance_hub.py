"""
Freelance Workers Hub - Business Logic Engine

A comprehensive platform for connecting freelancers with day-to-day job opportunities.
Similar to Fiverr but focused on short-term, immediate needs with smart matching.
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import numpy as np
from collections import defaultdict


class FreelanceHub:
    """
    Core engine for the Freelance Workers Hub platform.
    Handles matching, recommendations, pricing, and optimization.
    """

    def __init__(self):
        # Platform categories with typical day rates
        self.categories = {
            "web_development": {
                "name": "Web Development",
                "avg_hourly": 75,
                "typical_duration": "1-7 days",
                "skills": ["html", "css", "javascript", "react", "vue", "angular"],
                "common_tasks": [
                    "Build landing page",
                    "Fix website bugs",
                    "Add new feature",
                    "Redesign UI component"
                ]
            },
            "mobile_development": {
                "name": "Mobile Development",
                "avg_hourly": 80,
                "typical_duration": "3-14 days",
                "skills": ["swift", "kotlin", "react_native", "flutter"],
                "common_tasks": [
                    "Build mobile app",
                    "Fix app bugs",
                    "Add app feature",
                    "Port to another platform"
                ]
            },
            "graphic_design": {
                "name": "Graphic Design",
                "avg_hourly": 60,
                "typical_duration": "1-3 days",
                "skills": ["photoshop", "illustrator", "figma", "canva"],
                "common_tasks": [
                    "Logo design",
                    "Social media graphics",
                    "Brand identity",
                    "Marketing materials"
                ]
            },
            "writing": {
                "name": "Content Writing",
                "avg_hourly": 50,
                "typical_duration": "1-5 days",
                "skills": ["copywriting", "seo", "blogging", "technical_writing"],
                "common_tasks": [
                    "Blog post",
                    "Product description",
                    "SEO article",
                    "Press release"
                ]
            },
            "data_analysis": {
                "name": "Data Analysis",
                "avg_hourly": 70,
                "typical_duration": "2-7 days",
                "skills": ["python", "sql", "excel", "tableau", "power_bi"],
                "common_tasks": [
                    "Data cleaning",
                    "Dashboard creation",
                    "Statistical analysis",
                    "Data visualization"
                ]
            },
            "video_editing": {
                "name": "Video Editing",
                "avg_hourly": 55,
                "typical_duration": "1-5 days",
                "skills": ["premiere_pro", "final_cut", "after_effects"],
                "common_tasks": [
                    "Edit promotional video",
                    "YouTube video editing",
                    "Color grading",
                    "Motion graphics"
                ]
            },
            "virtual_assistant": {
                "name": "Virtual Assistant",
                "avg_hourly": 30,
                "typical_duration": "ongoing",
                "skills": ["email_management", "scheduling", "research", "data_entry"],
                "common_tasks": [
                    "Email management",
                    "Calendar scheduling",
                    "Research tasks",
                    "Data entry"
                ]
            },
            "consulting": {
                "name": "Business Consulting",
                "avg_hourly": 100,
                "typical_duration": "1-30 days",
                "skills": ["strategy", "market_research", "business_analysis"],
                "common_tasks": [
                    "Market research",
                    "Business strategy",
                    "Competitive analysis",
                    "Process optimization"
                ]
            }
        }

        # Quality tier multipliers
        self.tier_multipliers = {
            "beginner": 0.6,
            "intermediate": 1.0,
            "expert": 1.5,
            "top_rated": 2.0
        }

    def match_freelancers_to_job(
        self,
        job_posting: Dict,
        freelancer_profiles: List[Dict]
    ) -> List[Dict]:
        """
        Match freelancers to a job posting based on:
        - Skill alignment
        - Availability
        - Budget compatibility
        - Rating & experience
        - Past success in category

        Returns ranked list of freelancers with match scores
        """
        matches = []

        required_skills = set(job_posting.get("required_skills", []))
        budget_max = job_posting.get("budget_max", 0)
        budget_min = job_posting.get("budget_min", 0)
        experience_level = job_posting.get("experience_level", "intermediate")

        for freelancer in freelancer_profiles:
            # Skip if not available
            if not freelancer.get("is_available", False):
                continue

            # Calculate skill match
            freelancer_skills = set(freelancer.get("skills", []))
            skill_match = len(required_skills & freelancer_skills) / max(len(required_skills), 1)

            # Calculate budget compatibility
            hourly_rate = freelancer.get("hourly_rate", 0)
            estimated_hours = self._estimate_hours_for_job(job_posting)
            estimated_cost = hourly_rate * estimated_hours

            if budget_max > 0:
                if estimated_cost <= budget_max:
                    budget_match = 1.0
                elif estimated_cost <= budget_max * 1.2:  # Within 20% over budget
                    budget_match = 0.7
                else:
                    budget_match = 0.3
            else:
                budget_match = 1.0

            # Rating score
            rating = freelancer.get("rating_average", 0)
            rating_score = rating / 5.0

            # Success rate
            success_rate = freelancer.get("success_rate", 0) / 100.0

            # Experience level match
            freelancer_level = self._determine_experience_level(freelancer)
            level_match = self._calculate_level_match(experience_level, freelancer_level)

            # Response time bonus (faster is better)
            response_hours = freelancer.get("response_time_hours", 24)
            response_score = max(0, 1 - (response_hours / 48))  # Normalize to 0-1

            # Calculate overall match score (weighted average)
            match_score = (
                skill_match * 0.35 +
                budget_match * 0.20 +
                rating_score * 0.20 +
                success_rate * 0.15 +
                level_match * 0.07 +
                response_score * 0.03
            ) * 100  # Convert to 0-100

            # Only include if match is reasonable (>30%)
            if match_score >= 30:
                matches.append({
                    "freelancer_id": freelancer.get("id"),
                    "freelancer_name": freelancer.get("name", "Unknown"),
                    "match_score": round(match_score, 1),
                    "skill_match_pct": round(skill_match * 100, 1),
                    "budget_compatibility": round(budget_match * 100, 1),
                    "rating": rating,
                    "success_rate": freelancer.get("success_rate", 0),
                    "estimated_cost": estimated_cost,
                    "hourly_rate": hourly_rate,
                    "response_time_hours": response_hours,
                    "total_jobs_completed": freelancer.get("total_jobs_completed", 0),
                    "badges": freelancer.get("badges", []),
                    "reason": self._generate_match_reason(skill_match, budget_match, rating_score)
                })

        # Sort by match score (descending)
        matches.sort(key=lambda x: x["match_score"], reverse=True)

        return matches

    def recommend_jobs_for_freelancer(
        self,
        freelancer: Dict,
        available_jobs: List[Dict],
        limit: int = 10
    ) -> List[Dict]:
        """
        Recommend jobs to a freelancer based on their profile
        """
        recommendations = []

        freelancer_skills = set(freelancer.get("skills", []))
        hourly_rate = freelancer.get("hourly_rate", 0)
        min_budget = freelancer.get("min_project_budget", 0)
        preferred_types = freelancer.get("preferred_job_types", [])

        for job in available_jobs:
            # Skip if job is not open
            if job.get("status") != "open":
                continue

            required_skills = set(job.get("required_skills", []))

            # Skill match
            skill_match = len(required_skills & freelancer_skills) / max(len(required_skills), 1)

            # Budget viability
            budget_max = job.get("budget_max", 0)
            estimated_hours = self._estimate_hours_for_job(job)
            expected_earnings = hourly_rate * estimated_hours

            if expected_earnings >= min_budget and expected_earnings <= budget_max * 1.1:
                budget_viable = True
                budget_score = 1.0
            elif expected_earnings < min_budget:
                budget_viable = False
                budget_score = 0.3
            else:
                budget_viable = True
                budget_score = 0.7

            # Competition level
            proposals_count = job.get("proposals_count", 0)
            if proposals_count < 5:
                competition = "low"
                competition_score = 1.0
            elif proposals_count < 15:
                competition = "medium"
                competition_score = 0.7
            else:
                competition = "high"
                competition_score = 0.4

            # Deadline urgency (jobs with sooner deadlines rank higher)
            deadline = job.get("deadline")
            if deadline:
                days_until = (deadline - datetime.utcnow()).days
                if days_until < 3:
                    urgency_score = 1.0
                elif days_until < 7:
                    urgency_score = 0.8
                else:
                    urgency_score = 0.5
            else:
                urgency_score = 0.5

            # Overall recommendation score
            recommendation_score = (
                skill_match * 0.40 +
                budget_score * 0.30 +
                competition_score * 0.20 +
                urgency_score * 0.10
            ) * 100

            if recommendation_score >= 40:  # Only recommend if score is reasonable
                recommendations.append({
                    "job_id": job.get("id"),
                    "job_title": job.get("title"),
                    "recommendation_score": round(recommendation_score, 1),
                    "skill_match_pct": round(skill_match * 100, 1),
                    "estimated_earnings": expected_earnings,
                    "budget_range": f"${budget_max * 0.8:.0f} - ${budget_max:.0f}",
                    "competition": competition,
                    "proposals_count": proposals_count,
                    "deadline": deadline,
                    "client_name": job.get("client_name", "Anonymous"),
                    "reason": self._generate_job_recommendation_reason(
                        skill_match, budget_viable, competition
                    )
                })

        # Sort by recommendation score
        recommendations.sort(key=lambda x: x["recommendation_score"], reverse=True)

        return recommendations[:limit]

    def optimize_pricing_strategy(self, freelancer: Dict, market_data: Dict) -> Dict:
        """
        Analyze market data and recommend optimal pricing for a freelancer
        """
        current_rate = freelancer.get("hourly_rate", 50)
        rating = freelancer.get("rating_average", 0)
        total_jobs = freelancer.get("total_jobs_completed", 0)
        success_rate = freelancer.get("success_rate", 0)

        # Determine experience tier
        tier = self._determine_experience_level(freelancer)

        # Get category data
        primary_category = freelancer.get("primary_category", "web_development")
        category_data = self.categories.get(primary_category, self.categories["web_development"])
        market_avg = category_data["avg_hourly"]

        # Calculate recommended rate based on performance
        base_rate = market_avg * self.tier_multipliers[tier]

        # Adjust for rating
        if rating >= 4.8:
            rating_multiplier = 1.15
        elif rating >= 4.5:
            rating_multiplier = 1.08
        elif rating >= 4.0:
            rating_multiplier = 1.0
        else:
            rating_multiplier = 0.9

        # Adjust for success rate
        if success_rate >= 95:
            success_multiplier = 1.1
        elif success_rate >= 85:
            success_multiplier = 1.0
        else:
            success_multiplier = 0.95

        recommended_rate = base_rate * rating_multiplier * success_multiplier

        # Calculate optimal rate range
        min_rate = recommended_rate * 0.85
        max_rate = recommended_rate * 1.15

        # Competitive positioning
        if current_rate < market_avg * 0.7:
            positioning = "underpriced"
            message = "You're pricing below market - consider raising rates"
        elif current_rate > market_avg * 1.3:
            positioning = "premium"
            message = "You're in premium pricing tier - ensure quality matches"
        else:
            positioning = "competitive"
            message = "Your pricing is competitive with the market"

        return {
            "current_hourly_rate": current_rate,
            "recommended_rate": round(recommended_rate, 2),
            "rate_range": {
                "min": round(min_rate, 2),
                "max": round(max_rate, 2)
            },
            "market_average": market_avg,
            "tier": tier,
            "positioning": positioning,
            "message": message,
            "potential_monthly_increase": round((recommended_rate - current_rate) * 160, 2),  # Assuming 160 hrs/month
            "recommendations": self._generate_pricing_recommendations(
                current_rate, recommended_rate, tier, rating
            )
        }

    def calculate_freelancer_metrics(self, freelancer_id: int, contracts: List[Dict]) -> Dict:
        """
        Calculate comprehensive performance metrics for a freelancer
        """
        if not contracts:
            return {
                "total_earnings": 0,
                "jobs_completed": 0,
                "success_rate": 0,
                "avg_rating": 0,
                "on_time_delivery_rate": 0,
                "avg_response_time_hours": 24,
                "repeat_client_rate": 0,
                "tier": "beginner"
            }

        total_earnings = sum(c.get("total_amount", 0) for c in contracts if c.get("status") == "completed")
        total_contracts = len(contracts)
        completed = [c for c in contracts if c.get("status") == "completed"]
        completed_count = len(completed)

        # Success rate
        success_rate = (completed_count / total_contracts * 100) if total_contracts > 0 else 0

        # Average rating from reviews
        reviews = [c.get("review", {}) for c in completed if c.get("review")]
        if reviews:
            ratings = [r.get("rating", 0) for r in reviews if r.get("rating")]
            avg_rating = sum(ratings) / len(ratings) if ratings else 0
        else:
            avg_rating = 0

        # On-time delivery rate
        on_time = [c for c in completed if c.get("completed_at") and c.get("deadline")
                   and c["completed_at"] <= c["deadline"]]
        on_time_rate = (len(on_time) / completed_count * 100) if completed_count > 0 else 0

        # Repeat client rate
        clients = [c.get("client_id") for c in contracts]
        unique_clients = len(set(clients))
        repeat_rate = ((total_contracts - unique_clients) / total_contracts * 100) if total_contracts > 0 else 0

        # Determine tier
        if avg_rating >= 4.8 and completed_count >= 50:
            tier = "top_rated"
        elif avg_rating >= 4.5 and completed_count >= 20:
            tier = "expert"
        elif completed_count >= 5:
            tier = "intermediate"
        else:
            tier = "beginner"

        return {
            "total_earnings": round(total_earnings, 2),
            "jobs_completed": completed_count,
            "success_rate": round(success_rate, 1),
            "avg_rating": round(avg_rating, 2),
            "total_reviews": len(reviews),
            "on_time_delivery_rate": round(on_time_rate, 1),
            "repeat_client_rate": round(repeat_rate, 1),
            "tier": tier,
            "total_contracts": total_contracts,
            "badges_earned": self._calculate_badges(
                completed_count, avg_rating, on_time_rate, success_rate
            )
        }

    def generate_proposal_template(
        self,
        freelancer: Dict,
        job_posting: Dict
    ) -> Dict:
        """
        Generate a customized proposal template for a freelancer
        """
        freelancer_name = freelancer.get("name", "Freelancer")
        job_title = job_posting.get("title", "this project")
        required_skills = job_posting.get("required_skills", [])

        # Match freelancer skills to job requirements
        freelancer_skills = set(freelancer.get("skills", []))
        matching_skills = list(set(required_skills) & freelancer_skills)

        # Estimate timeline
        estimated_hours = self._estimate_hours_for_job(job_posting)
        hourly_rate = freelancer.get("hourly_rate", 50)
        estimated_cost = hourly_rate * estimated_hours
        estimated_days = max(1, estimated_hours // 8)

        # Generate proposal sections
        introduction = f"Hello! I'm {freelancer_name}, and I'm excited about your project: '{job_title}'."

        skills_paragraph = f"With expertise in {', '.join(matching_skills[:3])}, I'm well-equipped to deliver excellent results on this project."

        experience_paragraph = f"I've successfully completed {freelancer.get('total_jobs_completed', 0)} projects with a {freelancer.get('rating_average', 0):.1f}-star average rating."

        approach = "I propose to approach this project with the following steps:\n1. Initial consultation to understand your specific needs\n2. Development/execution phase with regular updates\n3. Revision rounds based on your feedback\n4. Final delivery with documentation"

        timeline = f"Estimated timeline: {estimated_days} day{'s' if estimated_days > 1 else ''}"

        pricing = f"Proposed rate: ${estimated_cost:.2f} (based on {estimated_hours} hours at ${hourly_rate}/hour)"

        closing = "I'm available to start immediately and would love to discuss this project further. Please feel free to ask any questions!"

        return {
            "template": f"{introduction}\n\n{skills_paragraph}\n\n{experience_paragraph}\n\n{approach}\n\n{timeline}\n\n{pricing}\n\n{closing}",
            "sections": {
                "introduction": introduction,
                "skills": skills_paragraph,
                "experience": experience_paragraph,
                "approach": approach,
                "timeline": timeline,
                "pricing": pricing,
                "closing": closing
            },
            "estimated_hours": estimated_hours,
            "estimated_cost": estimated_cost,
            "suggested_delivery_date": (datetime.utcnow() + timedelta(days=estimated_days)).isoformat()
        }

    def analyze_competition(self, job_posting: Dict, proposals: List[Dict]) -> Dict:
        """
        Analyze competition for a job posting
        """
        if not proposals:
            return {
                "competition_level": "none",
                "total_proposals": 0,
                "avg_proposed_rate": 0,
                "rate_range": {"min": 0, "max": 0},
                "recommendation": "Be the first to propose!"
            }

        rates = [p.get("proposed_rate", 0) for p in proposals]
        avg_rate = sum(rates) / len(rates) if rates else 0
        min_rate = min(rates) if rates else 0
        max_rate = max(rates) if rates else 0

        # Analyze freelancer tiers in proposals
        tiers = [p.get("freelancer", {}).get("tier", "beginner") for p in proposals]
        tier_counts = {tier: tiers.count(tier) for tier in set(tiers)}

        # Determine competition level
        proposal_count = len(proposals)
        if proposal_count < 5:
            competition_level = "low"
            recommendation = "Good opportunity - few competitors"
        elif proposal_count < 15:
            competition_level = "medium"
            recommendation = "Moderate competition - focus on value proposition"
        else:
            competition_level = "high"
            recommendation = "High competition - differentiate with unique skills"

        return {
            "competition_level": competition_level,
            "total_proposals": proposal_count,
            "avg_proposed_rate": round(avg_rate, 2),
            "rate_range": {
                "min": round(min_rate, 2),
                "max": round(max_rate, 2)
            },
            "tier_distribution": tier_counts,
            "recommendation": recommendation,
            "competitive_rate_suggestion": round(avg_rate * 0.95, 2),  # Slightly below average
            "premium_rate_suggestion": round(avg_rate * 1.1, 2)  # Above average
        }

    # ==================== HELPER METHODS ====================

    def _estimate_hours_for_job(self, job_posting: Dict) -> float:
        """Estimate hours required for a job based on description and budget"""
        budget_max = job_posting.get("budget_max", 0)
        budget_min = job_posting.get("budget_min", 0)
        budget_type = job_posting.get("budget_type", "fixed")

        if budget_type == "hourly":
            # For hourly jobs, use duration estimate
            duration = job_posting.get("duration_estimate", "1-3 days")
            if "hour" in duration.lower():
                return float(duration.split("-")[1].split()[0]) if "-" in duration else 8
            elif "day" in duration.lower():
                days = float(duration.split("-")[1].split()[0]) if "-" in duration else 1
                return days * 8
            elif "week" in duration.lower():
                weeks = float(duration.split("-")[1].split()[0]) if "-" in duration else 1
                return weeks * 40

        # For fixed price, estimate based on budget and average rates
        avg_budget = (budget_min + budget_max) / 2 if budget_min and budget_max else budget_max
        avg_market_rate = 65  # Overall platform average

        return max(1, avg_budget / avg_market_rate)

    def _determine_experience_level(self, freelancer: Dict) -> str:
        """Determine freelancer's experience level"""
        rating = freelancer.get("rating_average", 0)
        jobs_completed = freelancer.get("total_jobs_completed", 0)

        if rating >= 4.8 and jobs_completed >= 50:
            return "top_rated"
        elif rating >= 4.5 and jobs_completed >= 20:
            return "expert"
        elif jobs_completed >= 5:
            return "intermediate"
        else:
            return "beginner"

    def _calculate_level_match(self, required: str, freelancer_level: str) -> float:
        """Calculate how well freelancer level matches required level"""
        level_hierarchy = {"beginner": 1, "intermediate": 2, "expert": 3, "top_rated": 4}
        required_rank = level_hierarchy.get(required, 2)
        freelancer_rank = level_hierarchy.get(freelancer_level, 1)

        if freelancer_rank >= required_rank:
            return 1.0  # Perfect match or overqualified
        elif freelancer_rank == required_rank - 1:
            return 0.7  # One level below
        else:
            return 0.4  # Significantly below required level

    def _generate_match_reason(self, skill_match: float, budget_match: float, rating: float) -> str:
        """Generate human-readable match reason"""
        reasons = []

        if skill_match >= 0.8:
            reasons.append("strong skill alignment")
        elif skill_match >= 0.5:
            reasons.append("good skill match")

        if budget_match >= 0.9:
            reasons.append("within budget")

        if rating >= 0.9:
            reasons.append("excellent rating")
        elif rating >= 0.8:
            reasons.append("strong track record")

        return ", ".join(reasons) if reasons else "potential match"

    def _generate_job_recommendation_reason(
        self,
        skill_match: float,
        budget_viable: bool,
        competition: str
    ) -> str:
        """Generate reason for job recommendation"""
        reasons = []

        if skill_match >= 0.8:
            reasons.append("excellent skill fit")
        elif skill_match >= 0.6:
            reasons.append("good skill match")

        if budget_viable:
            reasons.append("meets your rate")

        if competition == "low":
            reasons.append("low competition")

        return ", ".join(reasons) if reasons else "potential opportunity"

    def _generate_pricing_recommendations(
        self,
        current: float,
        recommended: float,
        tier: str,
        rating: float
    ) -> List[str]:
        """Generate actionable pricing recommendations"""
        recommendations = []

        if current < recommended * 0.9:
            recommendations.append("Consider raising your rate to match market value")

        if rating >= 4.8:
            recommendations.append("Your excellent rating justifies premium pricing")

        if tier == "top_rated":
            recommendations.append("As a top-rated freelancer, you can command higher rates")

        recommendations.append("Test higher rates on new clients to gauge market acceptance")
        recommendations.append("Offer package deals to increase perceived value")

        return recommendations

    def _calculate_badges(
        self,
        jobs_completed: int,
        avg_rating: float,
        on_time_rate: float,
        success_rate: float
    ) -> List[str]:
        """Calculate earned badges based on performance"""
        badges = []

        if jobs_completed >= 10:
            badges.append("experienced")
        if jobs_completed >= 50:
            badges.append("veteran")
        if jobs_completed >= 100:
            badges.append("elite")

        if avg_rating >= 4.8:
            badges.append("5_star_rated")

        if on_time_rate >= 95:
            badges.append("reliable_delivery")

        if success_rate >= 98:
            badges.append("high_success_rate")

        return badges
