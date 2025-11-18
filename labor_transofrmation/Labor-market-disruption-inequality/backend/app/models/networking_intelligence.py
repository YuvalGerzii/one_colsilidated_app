"""
Networking Intelligence Engine
Analyzes professional networks, identifies gaps, and provides strategic networking recommendations
"""

from typing import Dict, List, Any, Optional, Set
from datetime import datetime, timedelta
from enum import Enum
import math


class ConnectionStrength(str, Enum):
    WEAK = "weak"
    MODERATE = "moderate"
    STRONG = "strong"
    CHAMPION = "champion"


class NetworkingStrategy(str, Enum):
    BREADTH = "breadth"  # Expand to new industries/roles
    DEPTH = "depth"  # Deepen existing connections
    STRATEGIC = "strategic"  # Target specific influencers
    MAINTENANCE = "maintenance"  # Nurture current network


class IndustryTier(str, Enum):
    TARGET = "target"  # Primary industry of interest
    ADJACENT = "adjacent"  # Related industries
    ASPIRATIONAL = "aspirational"  # Desired future industries
    UNRELATED = "unrelated"


class NetworkingIntelligence:
    """Comprehensive networking analysis and strategy engine"""

    def __init__(self):
        # Network scoring weights
        self.network_weights = {
            "size": 0.15,
            "diversity": 0.20,
            "strength": 0.25,
            "strategic_alignment": 0.25,
            "activity_level": 0.15
        }

        # Connection value multipliers
        self.connection_multipliers = {
            "hiring_manager": 3.0,
            "recruiter": 2.5,
            "executive": 2.0,
            "senior_professional": 1.5,
            "peer": 1.0,
            "junior": 0.7
        }

    def analyze_network(self, network_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive network analysis

        Args:
            network_data: Network information including connections, industries, roles

        Returns:
            Detailed network analysis with scores, gaps, and recommendations
        """
        connections = network_data.get("connections", [])
        target_industry = network_data.get("target_industry", "")
        target_role = network_data.get("target_role", "")
        current_role = network_data.get("current_role", "")

        # Calculate network metrics
        network_size = len(connections)

        # Industry diversity
        industries = [c.get("industry", "") for c in connections]
        unique_industries = len(set(industries))
        industry_diversity_score = min(100, (unique_industries / max(1, network_size)) * 200)

        # Role diversity
        roles = [c.get("role", "") for c in connections]
        unique_roles = len(set(roles))
        role_diversity_score = min(100, (unique_roles / max(1, network_size)) * 200)

        # Overall diversity score
        diversity_score = (industry_diversity_score + role_diversity_score) / 2

        # Connection strength analysis
        strength_scores = []
        for conn in connections:
            last_interaction_days = conn.get("days_since_last_interaction", 365)
            interaction_frequency = conn.get("interactions_per_month", 0)

            if last_interaction_days <= 30 and interaction_frequency >= 2:
                strength = ConnectionStrength.STRONG
                score = 100
            elif last_interaction_days <= 90 and interaction_frequency >= 1:
                strength = ConnectionStrength.MODERATE
                score = 70
            elif last_interaction_days <= 180:
                strength = ConnectionStrength.WEAK
                score = 40
            else:
                strength = ConnectionStrength.WEAK
                score = 20

            strength_scores.append(score)

        avg_strength_score = sum(strength_scores) / len(strength_scores) if strength_scores else 0

        # Strategic alignment (connections in target industry/role)
        target_industry_connections = sum(
            1 for c in connections if c.get("industry") == target_industry
        )
        target_role_connections = sum(
            1 for c in connections if c.get("role") == target_role
        )

        strategic_alignment_score = 0
        if network_size > 0:
            industry_alignment = (target_industry_connections / network_size) * 100
            role_alignment = (target_role_connections / network_size) * 100
            strategic_alignment_score = (industry_alignment + role_alignment) / 2

        # Activity level (recent networking)
        recent_adds = sum(
            1 for c in connections if c.get("days_since_connection", 365) <= 30
        )
        recent_interactions = sum(
            1 for c in connections if c.get("days_since_last_interaction", 365) <= 30
        )
        activity_score = min(100, ((recent_adds * 10) + (recent_interactions * 5)))

        # Overall network health score
        size_score = min(100, (network_size / 5))  # 500 connections = 100 score

        overall_score = (
            size_score * self.network_weights["size"] +
            diversity_score * self.network_weights["diversity"] +
            avg_strength_score * self.network_weights["strength"] +
            strategic_alignment_score * self.network_weights["strategic_alignment"] +
            activity_score * self.network_weights["activity_level"]
        )

        # Identify network gaps
        gaps = self._identify_network_gaps(
            connections, target_industry, target_role, current_role
        )

        # Get networking recommendations
        recommendations = self._generate_networking_strategy(
            overall_score, gaps, network_size, target_industry, target_role
        )

        # Identify key connectors (high-value connections)
        key_connectors = self._identify_key_connectors(connections, target_industry)

        # Get dormant relationships to revive
        dormant_connections = [
            {
                "name": c.get("name", "Unknown"),
                "role": c.get("role", ""),
                "company": c.get("company", ""),
                "days_inactive": c.get("days_since_last_interaction", 0),
                "last_topic": c.get("last_interaction_topic", ""),
                "revival_strategy": self._get_revival_strategy(c)
            }
            for c in connections
            if c.get("days_since_last_interaction", 0) > 90
        ][:10]  # Top 10 dormant connections

        return {
            "overall_network_score": round(overall_score, 1),
            "network_health": self._get_health_rating(overall_score),
            "network_size": network_size,
            "metrics": {
                "size_score": round(size_score, 1),
                "diversity_score": round(diversity_score, 1),
                "strength_score": round(avg_strength_score, 1),
                "strategic_alignment": round(strategic_alignment_score, 1),
                "activity_level": round(activity_score, 1)
            },
            "industry_breakdown": self._get_industry_breakdown(connections),
            "role_breakdown": self._get_role_breakdown(connections),
            "connection_strength_distribution": self._get_strength_distribution(connections),
            "target_industry_coverage": {
                "count": target_industry_connections,
                "percentage": round((target_industry_connections / max(1, network_size)) * 100, 1),
                "gap": max(0, 20 - target_industry_connections)  # Target: 20 connections minimum
            },
            "gaps": gaps,
            "key_connectors": key_connectors,
            "dormant_connections_to_revive": dormant_connections,
            "networking_strategy": recommendations,
            "quick_wins": self._get_quick_wins(connections, gaps)
        }

    def connection_value_score(self, connection: Dict[str, Any],
                              target_industry: str,
                              target_role: str) -> Dict[str, Any]:
        """
        Calculate the strategic value of a specific connection

        Args:
            connection: Connection details
            target_industry: User's target industry
            target_role: User's target role

        Returns:
            Value score and breakdown
        """
        base_score = 50

        # Industry alignment
        if connection.get("industry") == target_industry:
            industry_boost = 30
        elif self._is_adjacent_industry(connection.get("industry", ""), target_industry):
            industry_boost = 15
        else:
            industry_boost = 0

        # Role alignment
        conn_role = connection.get("role", "")
        role_type = self._classify_role_type(conn_role)
        role_boost = (self.connection_multipliers.get(role_type, 1.0) - 1.0) * 20

        # Connection strength
        days_since_interaction = connection.get("days_since_last_interaction", 365)
        if days_since_interaction <= 30:
            strength_boost = 20
        elif days_since_interaction <= 90:
            strength_boost = 10
        else:
            strength_boost = 0

        # Influence level
        if connection.get("is_hiring_authority", False):
            influence_boost = 25
        elif connection.get("company_size", "") == "large":
            influence_boost = 15
        else:
            influence_boost = 5

        total_score = base_score + industry_boost + role_boost + strength_boost + influence_boost
        total_score = min(100, total_score)

        # Determine value tier
        if total_score >= 80:
            value_tier = "critical"
        elif total_score >= 60:
            value_tier = "high"
        elif total_score >= 40:
            value_tier = "moderate"
        else:
            value_tier = "low"

        # Engagement recommendations
        engagement_rec = self._get_engagement_recommendation(
            connection, days_since_interaction, value_tier
        )

        return {
            "connection_name": connection.get("name", "Unknown"),
            "value_score": round(total_score, 1),
            "value_tier": value_tier,
            "score_breakdown": {
                "industry_alignment": industry_boost,
                "role_value": round(role_boost, 1),
                "relationship_strength": strength_boost,
                "influence_level": influence_boost
            },
            "engagement_recommendation": engagement_rec,
            "next_action": self._get_next_action(connection, value_tier),
            "conversation_starters": self._get_conversation_starters(connection)
        }

    def networking_event_recommendations(self, worker_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recommend networking events and opportunities

        Args:
            worker_data: Worker profile and target information

        Returns:
            Event recommendations prioritized by value
        """
        target_industry = worker_data.get("target_industry", "")
        target_role = worker_data.get("target_role", "")
        location = worker_data.get("location", "")
        availability = worker_data.get("weekly_networking_hours", 2)

        # Event types with priorities
        event_types = [
            {
                "type": "Industry Conference",
                "value_score": 90,
                "time_commitment": "8-16 hours (1-2 days)",
                "cost": "$200-1000",
                "frequency": "Quarterly",
                "benefit": "Meet industry leaders, learn trends, hiring managers present",
                "recommended": target_industry in ["tech", "finance", "healthcare"]
            },
            {
                "type": "Professional Association Meetup",
                "value_score": 85,
                "time_commitment": "2-3 hours",
                "cost": "$0-50",
                "frequency": "Monthly",
                "benefit": "Build local network, volunteer opportunities, referrals",
                "recommended": True
            },
            {
                "type": "Alumni Events",
                "value_score": 80,
                "time_commitment": "2-4 hours",
                "cost": "$0-100",
                "frequency": "Quarterly",
                "benefit": "Strong common bond, mentorship opportunities, job leads",
                "recommended": True
            },
            {
                "type": "Industry Workshops/Webinars",
                "value_score": 75,
                "time_commitment": "1-2 hours",
                "cost": "$0-100",
                "frequency": "Weekly",
                "benefit": "Learn + network, low commitment, ask questions to presenters",
                "recommended": True
            },
            {
                "type": "Coffee Chats (1-on-1)",
                "value_score": 85,
                "time_commitment": "1 hour",
                "cost": "$5-10",
                "frequency": "Weekly",
                "benefit": "Deep relationship building, personalized advice, referral potential",
                "recommended": True
            },
            {
                "type": "Virtual Networking Events",
                "value_score": 65,
                "time_commitment": "1-2 hours",
                "cost": "$0",
                "frequency": "Weekly",
                "benefit": "No travel, global reach, lower pressure",
                "recommended": availability < 3
            },
            {
                "type": "Hackathons/Competitions",
                "value_score": 70,
                "time_commitment": "8-48 hours",
                "cost": "$0-50",
                "frequency": "Monthly",
                "benefit": "Showcase skills, team building, recruiter presence",
                "recommended": target_role in ["software_engineer", "data_scientist", "designer"]
            },
            {
                "type": "Career Fairs",
                "value_score": 75,
                "time_commitment": "4-6 hours",
                "cost": "$0",
                "frequency": "Quarterly",
                "benefit": "Direct recruiter access, on-site interviews, entry-level friendly",
                "recommended": True
            }
        ]

        # Filter and rank recommendations
        recommended_events = [e for e in event_types if e.get("recommended", False)]
        recommended_events.sort(key=lambda x: x["value_score"], reverse=True)

        # Create weekly networking plan
        weekly_plan = self._create_networking_plan(availability, recommended_events)

        # Platform-specific strategies
        platform_strategies = self._get_platform_strategies(target_industry, target_role)

        return {
            "recommended_events": recommended_events[:5],  # Top 5
            "weekly_networking_plan": weekly_plan,
            "monthly_networking_budget": self._calculate_networking_budget(recommended_events),
            "platform_strategies": platform_strategies,
            "networking_goals": {
                "new_connections_per_month": max(10, availability * 2),
                "meaningful_conversations_per_week": max(2, availability // 2),
                "events_to_attend_per_month": max(2, availability // 2)
            },
            "success_metrics": [
                "Track connections made at each event",
                "Follow up within 48 hours with new contacts",
                "Convert 20% of new connections to coffee chats",
                "Get at least 3 referrals per month from network"
            ]
        }

    def linkedin_optimization_audit(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Audit LinkedIn profile and provide optimization recommendations

        Args:
            profile_data: LinkedIn profile information

        Returns:
            Audit results and actionable improvements
        """
        score = 0
        max_score = 100
        improvements = []

        # Profile photo (10 points)
        if profile_data.get("has_photo"):
            score += 10
        else:
            improvements.append({
                "area": "Profile Photo",
                "priority": "high",
                "current": "Missing",
                "recommendation": "Add professional headshot (increases profile views by 14x)",
                "impact": 10
            })

        # Headline (15 points)
        headline = profile_data.get("headline", "")
        if len(headline) > 50 and any(keyword in headline.lower() for keyword in ["engineer", "manager", "analyst", "specialist"]):
            score += 15
        elif headline:
            score += 7
            improvements.append({
                "area": "Headline",
                "priority": "high",
                "current": headline,
                "recommendation": "Include role, key skills, value proposition (e.g., 'Data Scientist | ML & Python | Turning Data into Business Impact')",
                "impact": 8
            })
        else:
            improvements.append({
                "area": "Headline",
                "priority": "critical",
                "current": "Missing",
                "recommendation": "Create compelling headline with role and key skills",
                "impact": 15
            })

        # About section (15 points)
        about = profile_data.get("about", "")
        if len(about) > 300:
            score += 15
        elif len(about) > 100:
            score += 8
            improvements.append({
                "area": "About Section",
                "priority": "medium",
                "current": f"{len(about)} characters",
                "recommendation": "Expand to 300-500 characters. Include story, expertise, what you're looking for",
                "impact": 7
            })
        else:
            improvements.append({
                "area": "About Section",
                "priority": "high",
                "current": "Too short or missing",
                "recommendation": "Write 300-500 character summary with your story and goals",
                "impact": 15
            })

        # Experience entries (20 points)
        experience_count = profile_data.get("experience_count", 0)
        experiences_with_bullets = profile_data.get("experiences_with_bullets", 0)

        if experience_count >= 3 and experiences_with_bullets >= 2:
            score += 20
        elif experience_count >= 2:
            score += 10
            improvements.append({
                "area": "Experience Descriptions",
                "priority": "high",
                "current": f"{experiences_with_bullets} entries have bullets",
                "recommendation": "Add 3-5 bullet points per role with quantified achievements",
                "impact": 10
            })
        else:
            improvements.append({
                "area": "Work Experience",
                "priority": "critical",
                "current": f"{experience_count} entries",
                "recommendation": "Add all relevant work experience with detailed descriptions",
                "impact": 20
            })

        # Skills (10 points)
        skills_count = profile_data.get("skills_count", 0)
        if skills_count >= 15:
            score += 10
        elif skills_count >= 5:
            score += 5
            improvements.append({
                "area": "Skills",
                "priority": "medium",
                "current": f"{skills_count} skills",
                "recommendation": "Add more skills (target: 15-50). Prioritize in-demand skills for your field",
                "impact": 5
            })
        else:
            improvements.append({
                "area": "Skills",
                "priority": "high",
                "current": f"{skills_count} skills",
                "recommendation": "Add 15-20 relevant skills. Get endorsements from connections",
                "impact": 10
            })

        # Recommendations (10 points)
        recommendations_count = profile_data.get("recommendations_count", 0)
        if recommendations_count >= 3:
            score += 10
        elif recommendations_count >= 1:
            score += 5
            improvements.append({
                "area": "Recommendations",
                "priority": "medium",
                "current": f"{recommendations_count} recommendation(s)",
                "recommendation": "Request 2-3 more recommendations from managers or colleagues",
                "impact": 5
            })
        else:
            improvements.append({
                "area": "Recommendations",
                "priority": "medium",
                "current": "None",
                "recommendation": "Request 3-5 recommendations from past managers/colleagues",
                "impact": 10
            })

        # Activity (10 points)
        posts_per_month = profile_data.get("posts_per_month", 0)
        if posts_per_month >= 4:
            score += 10
        elif posts_per_month >= 1:
            score += 5
            improvements.append({
                "area": "Activity/Engagement",
                "priority": "low",
                "current": f"{posts_per_month} posts/month",
                "recommendation": "Post 1-2x per week (share insights, comment on industry news)",
                "impact": 5
            })
        else:
            improvements.append({
                "area": "Activity/Engagement",
                "priority": "medium",
                "current": "Inactive",
                "recommendation": "Post weekly, engage with others' content, share valuable insights",
                "impact": 10
            })

        # Custom URL (5 points)
        if profile_data.get("has_custom_url"):
            score += 5
        else:
            improvements.append({
                "area": "Custom URL",
                "priority": "low",
                "current": "Default URL",
                "recommendation": "Set custom URL (linkedin.com/in/yourname) for professionalism",
                "impact": 5
            })

        # Certifications (5 points)
        certifications_count = profile_data.get("certifications_count", 0)
        if certifications_count >= 2:
            score += 5
        elif certifications_count >= 1:
            score += 3
        else:
            improvements.append({
                "area": "Certifications",
                "priority": "low",
                "current": "None listed",
                "recommendation": "Add relevant certifications or complete LinkedIn Learning courses",
                "impact": 5
            })

        # Determine profile grade
        if score >= 90:
            grade = "A"
            level = "Excellent"
        elif score >= 75:
            grade = "B"
            level = "Good"
        elif score >= 60:
            grade = "C"
            level = "Needs Improvement"
        elif score >= 40:
            grade = "D"
            level = "Poor"
        else:
            grade = "F"
            level = "Critical - Immediate Action Needed"

        # Sort improvements by priority and impact
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        improvements.sort(key=lambda x: (priority_order[x["priority"]], -x["impact"]))

        return {
            "overall_score": score,
            "max_score": max_score,
            "percentage": round((score / max_score) * 100, 1),
            "grade": grade,
            "level": level,
            "improvements_needed": improvements,
            "quick_wins": [imp for imp in improvements if imp["priority"] in ["critical", "high"]][:3],
            "estimated_time_to_optimize": f"{len(improvements) * 15} minutes",
            "profile_strength": "All-Star" if score >= 90 else "Advanced" if score >= 75 else "Intermediate" if score >= 50 else "Beginner"
        }

    def _identify_network_gaps(self, connections: List[Dict[str, Any]],
                               target_industry: str,
                               target_role: str,
                               current_role: str) -> List[Dict[str, Any]]:
        """Identify gaps in professional network"""
        gaps = []

        # Industry gap
        industry_connections = [c for c in connections if c.get("industry") == target_industry]
        if len(industry_connections) < 20:
            gaps.append({
                "gap_type": "industry_coverage",
                "severity": "high" if len(industry_connections) < 10 else "medium",
                "description": f"Only {len(industry_connections)} connections in target industry ({target_industry})",
                "target": "20+ connections in target industry",
                "action": f"Join {target_industry} groups on LinkedIn, attend industry events"
            })

        # Role diversity gap
        role_types = set(self._classify_role_type(c.get("role", "")) for c in connections)
        if "hiring_manager" not in [self._classify_role_type(c.get("role", "")) for c in connections]:
            gaps.append({
                "gap_type": "hiring_authority",
                "severity": "high",
                "description": "No connections with hiring authority",
                "target": "5+ hiring managers or executives",
                "action": "Reach out to hiring managers on LinkedIn, attend leadership events"
            })

        # Recruiter gap
        recruiter_connections = [c for c in connections if "recruiter" in c.get("role", "").lower()]
        if len(recruiter_connections) < 5:
            gaps.append({
                "gap_type": "recruiter_network",
                "severity": "medium",
                "description": f"Only {len(recruiter_connections)} recruiter connections",
                "target": "10+ recruiters in your field",
                "action": "Connect with recruiters specializing in your industry"
            })

        # Dormant connection gap
        dormant = [c for c in connections if c.get("days_since_last_interaction", 0) > 180]
        if len(dormant) > len(connections) * 0.5:
            gaps.append({
                "gap_type": "relationship_maintenance",
                "severity": "high",
                "description": f"{len(dormant)} dormant connections (>6 months inactive)",
                "target": "Keep 70%+ of network active",
                "action": "Revive 2-3 key dormant connections per week"
            })

        # Geographic gap (if relevant)
        if len(connections) > 0:
            target_location = "local"  # This would come from user data
            local_connections = [c for c in connections if c.get("location", "").lower() == target_location]
            if len(local_connections) < len(connections) * 0.3:
                gaps.append({
                    "gap_type": "geographic_coverage",
                    "severity": "low",
                    "description": "Limited local network",
                    "target": "30%+ local connections",
                    "action": "Attend local meetups and networking events"
                })

        return gaps

    def _generate_networking_strategy(self, overall_score: float,
                                     gaps: List[Dict[str, Any]],
                                     network_size: int,
                                     target_industry: str,
                                     target_role: str) -> Dict[str, Any]:
        """Generate personalized networking strategy"""

        # Determine primary strategy
        if network_size < 100:
            primary_strategy = NetworkingStrategy.BREADTH
            strategy_desc = "Focus on expanding network size across industries and roles"
        elif overall_score < 60:
            primary_strategy = NetworkingStrategy.DEPTH
            strategy_desc = "Strengthen existing connections and increase engagement"
        elif any(gap["gap_type"] == "industry_coverage" for gap in gaps):
            primary_strategy = NetworkingStrategy.STRATEGIC
            strategy_desc = f"Target {target_industry} professionals and hiring managers"
        else:
            primary_strategy = NetworkingStrategy.MAINTENANCE
            strategy_desc = "Maintain strong network and nurture key relationships"

        # Weekly action plan
        weekly_actions = []
        if primary_strategy == NetworkingStrategy.BREADTH:
            weekly_actions = [
                "Send 15-20 connection requests to relevant professionals",
                "Personalize each request with common interest/background",
                "Join 2-3 new industry groups on LinkedIn",
                "Attend 1 networking event or webinar"
            ]
        elif primary_strategy == NetworkingStrategy.STRATEGIC:
            weekly_actions = [
                f"Connect with 10 {target_industry} professionals",
                "Send 5 messages to hiring managers with thoughtful questions",
                "Engage with content from target companies",
                "Schedule 2 coffee chats with industry insiders"
            ]
        elif primary_strategy == NetworkingStrategy.DEPTH:
            weekly_actions = [
                "Reach out to 10 existing connections with value (article, introduction)",
                "Comment meaningfully on 15-20 posts from connections",
                "Schedule 2-3 catch-up calls with dormant connections",
                "Send congratulations/endorsements to 5 connections"
            ]
        else:  # Maintenance
            weekly_actions = [
                "Share 1-2 valuable posts per week",
                "Engage with top 20 connections' content",
                "Maintain 2 meaningful conversations per week",
                "Make 3-5 quality introductions between connections"
            ]

        # Monthly goals
        monthly_goals = {
            "new_connections": 40 if primary_strategy == NetworkingStrategy.BREADTH else 20,
            "meaningful_conversations": 8,
            "coffee_chats": 4,
            "events_attended": 2,
            "value_provided_to_network": "Share 4 helpful resources or make 3 introductions"
        }

        # Success metrics
        success_metrics = [
            f"Grow network by {monthly_goals['new_connections']} quality connections/month",
            "Maintain 30%+ response rate on outreach",
            "Get 2+ referrals per month from network",
            "Move 20% of weak ties to moderate strength"
        ]

        return {
            "primary_strategy": primary_strategy.value,
            "strategy_description": strategy_desc,
            "weekly_action_plan": weekly_actions,
            "monthly_goals": monthly_goals,
            "success_metrics": success_metrics,
            "estimated_time_commitment": "3-5 hours per week",
            "priority_gaps_to_address": [gap for gap in gaps if gap["severity"] == "high"]
        }

    def _identify_key_connectors(self, connections: List[Dict[str, Any]],
                                target_industry: str) -> List[Dict[str, Any]]:
        """Identify most valuable connections"""
        scored_connections = []

        for conn in connections:
            # Calculate value score
            score = 50  # Base score

            if conn.get("industry") == target_industry:
                score += 20
            if conn.get("is_hiring_authority"):
                score += 25
            if conn.get("days_since_last_interaction", 365) <= 30:
                score += 15
            if conn.get("company_size") == "large":
                score += 10

            role_type = self._classify_role_type(conn.get("role", ""))
            score += (self.connection_multipliers.get(role_type, 1.0) - 1.0) * 20

            scored_connections.append({
                "name": conn.get("name", "Unknown"),
                "role": conn.get("role", ""),
                "company": conn.get("company", ""),
                "industry": conn.get("industry", ""),
                "value_score": round(score, 1),
                "why_valuable": self._explain_value(conn, target_industry),
                "engagement_strategy": self._get_engagement_recommendation(conn, conn.get("days_since_last_interaction", 0), "high")
            })

        # Return top 10
        scored_connections.sort(key=lambda x: x["value_score"], reverse=True)
        return scored_connections[:10]

    def _get_revival_strategy(self, connection: Dict[str, Any]) -> str:
        """Get strategy for reviving dormant connection"""
        last_topic = connection.get("last_interaction_topic", "")
        role = connection.get("role", "")

        strategies = [
            f"Share article related to {last_topic} with personal note",
            f"Congratulate on recent job change or company milestone",
            f"Ask for advice on {role}-related question",
            "Offer to make introduction to someone in your network",
            "Invite to virtual coffee to catch up"
        ]

        return strategies[hash(connection.get("name", "")) % len(strategies)]

    def _classify_role_type(self, role: str) -> str:
        """Classify role into type for value calculation"""
        role_lower = role.lower()
        if any(title in role_lower for title in ["ceo", "vp", "director", "head of"]):
            return "executive"
        elif any(title in role_lower for title in ["hiring manager", "engineering manager", "manager"]):
            return "hiring_manager"
        elif "recruiter" in role_lower or "talent" in role_lower:
            return "recruiter"
        elif any(title in role_lower for title in ["senior", "lead", "principal", "staff"]):
            return "senior_professional"
        elif any(title in role_lower for title in ["junior", "associate", "intern"]):
            return "junior"
        else:
            return "peer"

    def _is_adjacent_industry(self, industry1: str, industry2: str) -> bool:
        """Check if industries are adjacent/related"""
        adjacent_map = {
            "tech": ["software", "saas", "cloud", "ai", "cybersecurity"],
            "finance": ["fintech", "banking", "insurance", "investment"],
            "healthcare": ["biotech", "pharmaceuticals", "medical devices"],
            "consulting": ["strategy", "management", "advisory"]
        }

        for key, values in adjacent_map.items():
            if industry1.lower() in values and industry2.lower() in values:
                return True
        return False

    def _get_engagement_recommendation(self, connection: Dict[str, Any],
                                      days_inactive: int,
                                      value_tier: str) -> str:
        """Get engagement recommendation for connection"""
        if value_tier == "critical" and days_inactive > 30:
            return "Priority: Reach out this week with valuable insight or question"
        elif value_tier == "high" and days_inactive > 60:
            return "Reach out within 2 weeks - share article or schedule coffee chat"
        elif days_inactive > 90:
            return "Revival needed: Send personalized message referencing past conversation"
        elif days_inactive <= 30:
            return "Maintain momentum: Continue regular engagement"
        else:
            return "Check in monthly with value-add message"

    def _get_next_action(self, connection: Dict[str, Any], value_tier: str) -> str:
        """Get specific next action for connection"""
        actions = [
            f"Send message: Share relevant article about {connection.get('industry', 'their industry')}",
            f"Request: 15-minute call to learn about their career path",
            f"Offer: Introduction to someone in my network who could help them",
            f"Engage: Comment thoughtfully on their recent LinkedIn post",
            f"Appreciate: Send thank you note for past advice/help"
        ]
        return actions[hash(connection.get("name", "")) % len(actions)]

    def _get_conversation_starters(self, connection: Dict[str, Any]) -> List[str]:
        """Get conversation starters for connection"""
        role = connection.get("role", "professional")
        industry = connection.get("industry", "your field")

        return [
            f"I saw that {industry} is trending toward [X]. What's your take on this?",
            f"As a {role}, what skills do you think are most critical right now?",
            "I'm exploring opportunities in [X area]. Any advice for someone transitioning?",
            "What's the most interesting project you're working on right now?",
            "I'd love to learn from your experience in [X]. Could we schedule a brief call?"
        ]

    def _get_industry_breakdown(self, connections: List[Dict[str, Any]]) -> Dict[str, int]:
        """Get breakdown of connections by industry"""
        industries = {}
        for conn in connections:
            industry = conn.get("industry", "Unknown")
            industries[industry] = industries.get(industry, 0) + 1
        return dict(sorted(industries.items(), key=lambda x: x[1], reverse=True)[:10])

    def _get_role_breakdown(self, connections: List[Dict[str, Any]]) -> Dict[str, int]:
        """Get breakdown of connections by role type"""
        roles = {}
        for conn in connections:
            role_type = self._classify_role_type(conn.get("role", ""))
            roles[role_type] = roles.get(role_type, 0) + 1
        return roles

    def _get_strength_distribution(self, connections: List[Dict[str, Any]]) -> Dict[str, int]:
        """Get distribution of connection strengths"""
        distribution = {"strong": 0, "moderate": 0, "weak": 0}

        for conn in connections:
            days_inactive = conn.get("days_since_last_interaction", 365)
            if days_inactive <= 30:
                distribution["strong"] += 1
            elif days_inactive <= 90:
                distribution["moderate"] += 1
            else:
                distribution["weak"] += 1

        return distribution

    def _get_quick_wins(self, connections: List[Dict[str, Any]],
                       gaps: List[Dict[str, Any]]) -> List[str]:
        """Get quick networking wins"""
        wins = [
            "Send 5 personalized connection requests today",
            "Comment on 10 posts from your network",
            "Reach out to 3 dormant connections with value",
            "Join 2 relevant LinkedIn groups",
            "Update your LinkedIn headline and about section"
        ]

        # Add gap-specific quick wins
        for gap in gaps:
            if gap["gap_type"] == "industry_coverage":
                wins.append(f"Connect with 5 {gap.get('target_industry', 'target industry')} professionals")
            elif gap["gap_type"] == "hiring_authority":
                wins.append("Follow 10 hiring managers at target companies")

        return wins[:5]

    def _create_networking_plan(self, weekly_hours: float,
                               events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create weekly networking plan based on available hours"""
        plan = {
            "total_hours_available": weekly_hours,
            "activities": []
        }

        remaining_hours = weekly_hours

        # Always include digital networking (low time investment, high ROI)
        if remaining_hours >= 1:
            plan["activities"].append({
                "activity": "LinkedIn Engagement",
                "time": "1-2 hours",
                "tasks": [
                    "Send 15 connection requests",
                    "Comment on 20 posts",
                    "Send 5 messages to connections",
                    "Share 1 valuable post"
                ]
            })
            remaining_hours -= 1.5

        # Add 1-on-1 coffee chats if time allows
        if remaining_hours >= 1:
            plan["activities"].append({
                "activity": "Coffee Chats",
                "time": "1-2 hours",
                "tasks": [
                    "Schedule 2 virtual or in-person coffee meetings",
                    "Prepare questions about their career path",
                    "Ask for advice and insights"
                ]
            })
            remaining_hours -= 1.5

        # Add events if time allows
        if remaining_hours >= 2:
            plan["activities"].append({
                "activity": "Networking Event",
                "time": "2-3 hours",
                "tasks": [
                    "Attend 1 industry event or webinar",
                    "Set goal to talk to 5 new people",
                    "Follow up within 48 hours"
                ]
            })

        return plan

    def _calculate_networking_budget(self, events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate monthly networking budget"""
        return {
            "low_budget": "$20-50/month",
            "breakdown": {
                "coffee_chats": "$20 (4 chats @ $5)",
                "meetup_fees": "$0-20",
                "professional_association": "$0-50/year",
                "conference_savings": "$50-100/month (for annual conferences)"
            },
            "medium_budget": "$100-200/month",
            "high_budget": "$300-500/month (includes conferences)",
            "free_options": [
                "LinkedIn networking (free)",
                "Virtual events (free)",
                "Alumni associations (often free)",
                "Informational interviews (free)",
                "LinkedIn groups (free)"
            ]
        }

    def _get_platform_strategies(self, target_industry: str,
                                target_role: str) -> List[Dict[str, Any]]:
        """Get platform-specific networking strategies"""
        return [
            {
                "platform": "LinkedIn",
                "priority": "highest",
                "strategies": [
                    "Post weekly insights about your industry",
                    "Engage with content from target companies",
                    "Use 'Open to Work' badge",
                    "Join industry-specific groups",
                    "Follow hiring managers at target companies"
                ],
                "time_investment": "30-60 min/day"
            },
            {
                "platform": "Twitter/X",
                "priority": "medium",
                "strategies": [
                    "Follow industry leaders and companies",
                    "Share insights and engage in discussions",
                    "Use relevant hashtags",
                    "Participate in Twitter chats"
                ],
                "time_investment": "15-30 min/day",
                "best_for": "Tech, media, startup industries"
            },
            {
                "platform": "Industry Slack/Discord Communities",
                "priority": "high",
                "strategies": [
                    "Join relevant communities",
                    "Offer help and expertise",
                    "Ask thoughtful questions",
                    "Build reputation as helpful member"
                ],
                "time_investment": "20-40 min/day",
                "best_for": "Tech, design, startup roles"
            },
            {
                "platform": "In-Person Events",
                "priority": "high",
                "strategies": [
                    "Attend monthly meetups",
                    "Volunteer at conferences",
                    "Join professional associations",
                    "Alumni events"
                ],
                "time_investment": "4-8 hours/month",
                "best_for": "All industries - strongest connections"
            }
        ]

    def _get_health_rating(self, score: float) -> str:
        """Get health rating for network"""
        if score >= 80:
            return "Excellent - Strong, strategic network"
        elif score >= 60:
            return "Good - Solid network with room for growth"
        elif score >= 40:
            return "Fair - Network needs strengthening"
        else:
            return "Poor - Urgent network building needed"

    def _explain_value(self, connection: Dict[str, Any], target_industry: str) -> str:
        """Explain why connection is valuable"""
        reasons = []

        if connection.get("industry") == target_industry:
            reasons.append("In your target industry")
        if connection.get("is_hiring_authority"):
            reasons.append("Has hiring authority")
        if connection.get("company_size") == "large":
            reasons.append("Works at large company")

        role_type = self._classify_role_type(connection.get("role", ""))
        if role_type in ["executive", "hiring_manager"]:
            reasons.append(f"{role_type.replace('_', ' ').title()} role")

        return ", ".join(reasons) if reasons else "Professional contact"
