"""
Career and Mentorship Matching Agents for Bond.AI

This module contains specialized agents for career development, mentorship matching,
event recommendations, and skill gap analysis in professional networking contexts.
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import numpy as np


class CareerPathAgent:
    """
    Agent specialized in career trajectory analysis and career path recommendations.

    Capabilities:
    - Analyze career progression patterns
    - Predict future career opportunities
    - Identify career transition pathways
    - Recommend skill development priorities
    - Map career milestones and achievements
    - Benchmark career progress against industry standards
    """

    def __init__(self, agent_id: str = "career_path_agent"):
        self.agent_id = agent_id
        self.proficiency = 0.94
        self.capabilities = [
            "career_trajectory_analysis",
            "opportunity_prediction",
            "transition_pathway_mapping",
            "skill_priority_recommendation",
            "milestone_tracking",
            "industry_benchmarking",
            "growth_potential_assessment"
        ]
        self.career_stages = ["entry_level", "mid_level", "senior", "executive", "c_suite"]

    async def analyze_career_trajectory(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a user's career trajectory and predict future paths.

        Args:
            profile: User profile with work history and skills

        Returns:
            Career trajectory analysis with recommendations
        """
        work_history = profile.get("work_history", [])
        skills = profile.get("skills", [])
        education = profile.get("education", [])

        trajectory_analysis = {
            "current_stage": self._determine_career_stage(work_history),
            "career_velocity": self._calculate_career_velocity(work_history),
            "progression_pattern": self._identify_progression_pattern(work_history),
            "predicted_paths": self._predict_career_paths(work_history, skills),
            "transition_opportunities": self._identify_transition_opportunities(
                work_history, skills
            ),
            "growth_areas": self._identify_growth_areas(work_history, skills),
            "timeline_projections": self._project_career_timeline(work_history)
        }

        return {
            "status": "success",
            "agent": self.agent_id,
            "analysis": trajectory_analysis,
            "proficiency": self.proficiency
        }

    async def recommend_next_steps(
        self,
        profile: Dict[str, Any],
        goals: List[str]
    ) -> Dict[str, Any]:
        """
        Recommend specific next steps for career advancement.

        Args:
            profile: User profile
            goals: Career goals

        Returns:
            Personalized career advancement recommendations
        """
        current_role = profile.get("current_role", {})
        skills = profile.get("skills", [])

        recommendations = {
            "immediate_actions": self._generate_immediate_actions(profile, goals),
            "skill_development": self._recommend_skill_development(skills, goals),
            "networking_priorities": self._recommend_networking_priorities(profile, goals),
            "role_targets": self._identify_target_roles(profile, goals),
            "estimated_timeline": self._estimate_advancement_timeline(profile, goals)
        }

        return {
            "status": "success",
            "agent": self.agent_id,
            "recommendations": recommendations,
            "proficiency": self.proficiency
        }

    def _determine_career_stage(self, work_history: List[Dict[str, Any]]) -> str:
        """Determine current career stage."""
        total_years = sum(h.get("duration_years", 0) for h in work_history)

        if total_years < 3:
            return "entry_level"
        elif total_years < 7:
            return "mid_level"
        elif total_years < 12:
            return "senior"
        elif total_years < 20:
            return "executive"
        else:
            return "c_suite"

    def _calculate_career_velocity(self, work_history: List[Dict[str, Any]]) -> float:
        """Calculate career advancement velocity."""
        if len(work_history) < 2:
            return 0.5

        # Calculate promotions and role changes
        promotions = sum(1 for h in work_history if h.get("was_promotion", False))
        years = sum(h.get("duration_years", 0) for h in work_history)

        velocity = (promotions / max(years, 1)) * 10
        return min(velocity, 1.0)

    def _identify_progression_pattern(self, work_history: List[Dict[str, Any]]) -> str:
        """Identify career progression pattern."""
        if len(work_history) < 2:
            return "early_career"

        # Analyze pattern: linear, accelerating, specialist, generalist
        role_levels = [h.get("seniority_level", 0) for h in work_history]

        if all(role_levels[i] <= role_levels[i+1] for i in range(len(role_levels)-1)):
            return "linear_progression"
        elif any(role_levels[i] < role_levels[i+1] for i in range(len(role_levels)-1)):
            return "accelerating_growth"
        else:
            return "lateral_exploration"

    def _predict_career_paths(
        self,
        work_history: List[Dict[str, Any]],
        skills: List[str]
    ) -> List[Dict[str, Any]]:
        """Predict possible future career paths."""
        paths = [
            {
                "path": "Technical Leadership",
                "probability": 0.75,
                "required_skills": ["leadership", "technical_architecture"],
                "estimated_timeline": "2-3 years"
            },
            {
                "path": "Management Track",
                "probability": 0.65,
                "required_skills": ["people_management", "strategic_planning"],
                "estimated_timeline": "3-5 years"
            },
            {
                "path": "Specialist/Expert",
                "probability": 0.70,
                "required_skills": ["deep_expertise", "thought_leadership"],
                "estimated_timeline": "4-6 years"
            }
        ]
        return paths

    def _identify_transition_opportunities(
        self,
        work_history: List[Dict[str, Any]],
        skills: List[str]
    ) -> List[Dict[str, Any]]:
        """Identify career transition opportunities."""
        return [
            {
                "target_role": "Engineering Manager",
                "feasibility": 0.80,
                "skill_gaps": ["team_leadership", "budget_management"],
                "transition_difficulty": "medium"
            }
        ]

    def _identify_growth_areas(
        self,
        work_history: List[Dict[str, Any]],
        skills: List[str]
    ) -> List[str]:
        """Identify areas for professional growth."""
        return [
            "Leadership and team management",
            "Strategic thinking and planning",
            "Cross-functional collaboration"
        ]

    def _project_career_timeline(self, work_history: List[Dict[str, Any]]) -> Dict[str, str]:
        """Project career milestones timeline."""
        return {
            "next_promotion": "12-18 months",
            "senior_level": "3-4 years",
            "leadership_role": "5-7 years"
        }

    def _generate_immediate_actions(
        self,
        profile: Dict[str, Any],
        goals: List[str]
    ) -> List[str]:
        """Generate immediate actionable steps."""
        return [
            "Complete a leadership training program",
            "Mentor 2-3 junior team members",
            "Lead a cross-functional project"
        ]

    def _recommend_skill_development(
        self,
        current_skills: List[str],
        goals: List[str]
    ) -> List[Dict[str, Any]]:
        """Recommend skills to develop."""
        return [
            {
                "skill": "Strategic Planning",
                "priority": "high",
                "learning_resources": ["courses", "books", "mentorship"]
            }
        ]

    def _recommend_networking_priorities(
        self,
        profile: Dict[str, Any],
        goals: List[str]
    ) -> List[str]:
        """Recommend networking priorities."""
        return [
            "Connect with senior leaders in your industry",
            "Join professional associations",
            "Attend industry conferences"
        ]

    def _identify_target_roles(
        self,
        profile: Dict[str, Any],
        goals: List[str]
    ) -> List[Dict[str, Any]]:
        """Identify target roles to pursue."""
        return [
            {
                "role": "Senior Engineering Manager",
                "fit_score": 0.85,
                "preparation_needed": "6-12 months"
            }
        ]

    def _estimate_advancement_timeline(
        self,
        profile: Dict[str, Any],
        goals: List[str]
    ) -> Dict[str, str]:
        """Estimate timeline for career advancement."""
        return {
            "short_term": "6-12 months",
            "medium_term": "1-3 years",
            "long_term": "3-5 years"
        }


class MentorshipMatchingAgent:
    """
    Agent specialized in matching mentors with mentees based on compatibility,
    expertise alignment, and mutual benefit potential.

    Capabilities:
    - Match mentors and mentees
    - Assess mentorship compatibility
    - Recommend mentorship goals
    - Track mentorship progress
    - Facilitate mentor-mentee introductions
    - Optimize mentorship relationship outcomes
    """

    def __init__(self, agent_id: str = "mentorship_matching_agent"):
        self.agent_id = agent_id
        self.proficiency = 0.93
        self.capabilities = [
            "mentor_mentee_matching",
            "compatibility_assessment",
            "goal_recommendation",
            "progress_tracking",
            "relationship_facilitation",
            "outcome_optimization",
            "expertise_alignment"
        ]

    async def match_mentor_mentee(
        self,
        mentee_profile: Dict[str, Any],
        mentor_candidates: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Match a mentee with the best mentor candidates.

        Args:
            mentee_profile: Profile of the person seeking mentorship
            mentor_candidates: List of potential mentors

        Returns:
            Ranked list of mentor matches with compatibility scores
        """
        mentee_goals = mentee_profile.get("mentorship_goals", [])
        mentee_skills = mentee_profile.get("skills", [])
        mentee_industry = mentee_profile.get("industry", "")

        matches = []
        for mentor in mentor_candidates:
            compatibility = self._calculate_mentorship_compatibility(
                mentee_profile, mentor
            )
            matches.append({
                "mentor": mentor,
                "compatibility_score": compatibility["overall_score"],
                "compatibility_breakdown": compatibility,
                "recommended_focus_areas": self._recommend_focus_areas(
                    mentee_profile, mentor
                )
            })

        # Sort by compatibility score
        matches.sort(key=lambda x: x["compatibility_score"], reverse=True)

        return {
            "status": "success",
            "agent": self.agent_id,
            "top_matches": matches[:5],
            "proficiency": self.proficiency
        }

    async def assess_mentorship_readiness(
        self,
        profile: Dict[str, Any],
        role: str  # "mentor" or "mentee"
    ) -> Dict[str, Any]:
        """
        Assess someone's readiness for mentorship role.

        Args:
            profile: User profile
            role: Either "mentor" or "mentee"

        Returns:
            Readiness assessment with recommendations
        """
        if role == "mentor":
            assessment = self._assess_mentor_readiness(profile)
        else:
            assessment = self._assess_mentee_readiness(profile)

        return {
            "status": "success",
            "agent": self.agent_id,
            "assessment": assessment,
            "proficiency": self.proficiency
        }

    def _calculate_mentorship_compatibility(
        self,
        mentee: Dict[str, Any],
        mentor: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate mentorship compatibility score."""
        # Expertise alignment
        expertise_score = self._calculate_expertise_alignment(
            mentee.get("skills", []),
            mentor.get("expertise", [])
        )

        # Industry alignment
        industry_score = 1.0 if mentee.get("industry") == mentor.get("industry") else 0.6

        # Communication style compatibility
        communication_score = self._calculate_communication_compatibility(mentee, mentor)

        # Availability alignment
        availability_score = self._calculate_availability_alignment(mentee, mentor)

        # Goal alignment
        goal_score = self._calculate_goal_alignment(
            mentee.get("mentorship_goals", []),
            mentor.get("mentoring_strengths", [])
        )

        overall_score = (
            expertise_score * 0.30 +
            industry_score * 0.20 +
            communication_score * 0.20 +
            availability_score * 0.10 +
            goal_score * 0.20
        )

        return {
            "overall_score": overall_score,
            "expertise_alignment": expertise_score,
            "industry_alignment": industry_score,
            "communication_compatibility": communication_score,
            "availability_alignment": availability_score,
            "goal_alignment": goal_score
        }

    def _calculate_expertise_alignment(
        self,
        mentee_skills: List[str],
        mentor_expertise: List[str]
    ) -> float:
        """Calculate expertise alignment between mentee needs and mentor strengths."""
        if not mentee_skills or not mentor_expertise:
            return 0.5

        # Calculate overlap
        mentee_set = set(s.lower() for s in mentee_skills)
        mentor_set = set(e.lower() for e in mentor_expertise)

        overlap = len(mentee_set.intersection(mentor_set))
        total = len(mentee_set)

        return min(overlap / max(total, 1), 1.0)

    def _calculate_communication_compatibility(
        self,
        mentee: Dict[str, Any],
        mentor: Dict[str, Any]
    ) -> float:
        """Calculate communication style compatibility."""
        # Simplified compatibility check
        return 0.85

    def _calculate_availability_alignment(
        self,
        mentee: Dict[str, Any],
        mentor: Dict[str, Any]
    ) -> float:
        """Calculate availability alignment."""
        return 0.90

    def _calculate_goal_alignment(
        self,
        mentee_goals: List[str],
        mentor_strengths: List[str]
    ) -> float:
        """Calculate alignment between mentee goals and mentor strengths."""
        if not mentee_goals or not mentor_strengths:
            return 0.5

        goal_set = set(g.lower() for g in mentee_goals)
        strength_set = set(s.lower() for s in mentor_strengths)

        overlap = len(goal_set.intersection(strength_set))
        return min(overlap / max(len(goal_set), 1) * 1.5, 1.0)

    def _recommend_focus_areas(
        self,
        mentee: Dict[str, Any],
        mentor: Dict[str, Any]
    ) -> List[str]:
        """Recommend focus areas for the mentorship."""
        return [
            "Career advancement strategies",
            "Technical skill development",
            "Leadership skills"
        ]

    def _assess_mentor_readiness(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Assess readiness to be a mentor."""
        experience_years = profile.get("total_experience_years", 0)
        leadership_experience = profile.get("has_leadership_experience", False)

        readiness_score = 0.0
        if experience_years >= 5:
            readiness_score += 0.4
        if leadership_experience:
            readiness_score += 0.3
        if profile.get("has_mentored_before", False):
            readiness_score += 0.3

        return {
            "readiness_score": min(readiness_score, 1.0),
            "strengths": ["Extensive experience", "Leadership background"],
            "areas_to_develop": ["Active listening skills"],
            "recommendations": ["Complete mentor training program"]
        }

    def _assess_mentee_readiness(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Assess readiness to be a mentee."""
        has_clear_goals = len(profile.get("mentorship_goals", [])) > 0
        willing_to_learn = profile.get("learning_mindset", True)

        readiness_score = 0.7 if has_clear_goals and willing_to_learn else 0.4

        return {
            "readiness_score": readiness_score,
            "strengths": ["Clear goals", "Open to feedback"],
            "areas_to_develop": ["Define specific objectives"],
            "recommendations": ["Prepare questions for first meeting"]
        }


class EventRecommendationAgent:
    """
    Agent specialized in recommending networking events, conferences,
    and professional gatherings based on user interests and goals.

    Capabilities:
    - Recommend relevant events
    - Predict event value and ROI
    - Identify networking opportunities at events
    - Track event attendance patterns
    - Suggest optimal event schedule
    - Connect attendees with shared interests
    """

    def __init__(self, agent_id: str = "event_recommendation_agent"):
        self.agent_id = agent_id
        self.proficiency = 0.91
        self.capabilities = [
            "event_recommendation",
            "roi_prediction",
            "networking_opportunity_identification",
            "attendance_tracking",
            "schedule_optimization",
            "attendee_matching"
        ]

    async def recommend_events(
        self,
        profile: Dict[str, Any],
        preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Recommend events based on user profile and preferences.

        Args:
            profile: User profile with interests and goals
            preferences: Event preferences (location, type, etc.)

        Returns:
            Recommended events with relevance scores
        """
        interests = profile.get("interests", [])
        industry = profile.get("industry", "")
        goals = profile.get("goals", [])
        location = preferences.get("location", "")

        # Mock event data
        events = self._fetch_relevant_events(interests, industry, location)
        recommendations = []

        for event in events:
            relevance = self._calculate_event_relevance(profile, event)
            roi_prediction = self._predict_event_roi(profile, event)

            recommendations.append({
                "event": event,
                "relevance_score": relevance,
                "predicted_roi": roi_prediction,
                "networking_potential": self._assess_networking_potential(profile, event),
                "recommended_actions": self._generate_event_actions(event)
            })

        # Sort by relevance
        recommendations.sort(key=lambda x: x["relevance_score"], reverse=True)

        return {
            "status": "success",
            "agent": self.agent_id,
            "recommendations": recommendations[:10],
            "proficiency": self.proficiency
        }

    async def match_event_attendees(
        self,
        user_profile: Dict[str, Any],
        event_attendees: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Match user with other event attendees based on shared interests.

        Args:
            user_profile: User's profile
            event_attendees: List of other attendees

        Returns:
            Matched attendees with connection recommendations
        """
        matches = []

        for attendee in event_attendees:
            compatibility = self._calculate_attendee_compatibility(
                user_profile, attendee
            )

            if compatibility > 0.6:
                matches.append({
                    "attendee": attendee,
                    "compatibility_score": compatibility,
                    "shared_interests": self._identify_shared_interests(
                        user_profile, attendee
                    ),
                    "conversation_starters": self._generate_conversation_starters(
                        user_profile, attendee
                    )
                })

        matches.sort(key=lambda x: x["compatibility_score"], reverse=True)

        return {
            "status": "success",
            "agent": self.agent_id,
            "matches": matches[:15],
            "proficiency": self.proficiency
        }

    def _fetch_relevant_events(
        self,
        interests: List[str],
        industry: str,
        location: str
    ) -> List[Dict[str, Any]]:
        """Fetch events relevant to user's interests."""
        # Mock events
        return [
            {
                "name": "Tech Leadership Summit 2025",
                "type": "conference",
                "industry": "technology",
                "topics": ["leadership", "innovation", "AI"],
                "date": "2025-03-15",
                "location": "San Francisco",
                "attendee_count": 500
            },
            {
                "name": "Startup Networking Mixer",
                "type": "networking",
                "industry": "technology",
                "topics": ["startups", "entrepreneurship"],
                "date": "2025-02-20",
                "location": "San Francisco",
                "attendee_count": 100
            }
        ]

    def _calculate_event_relevance(
        self,
        profile: Dict[str, Any],
        event: Dict[str, Any]
    ) -> float:
        """Calculate how relevant an event is to the user."""
        interests = set(i.lower() for i in profile.get("interests", []))
        event_topics = set(t.lower() for t in event.get("topics", []))

        # Interest overlap
        interest_overlap = len(interests.intersection(event_topics)) / max(len(interests), 1)

        # Industry match
        industry_match = 1.0 if profile.get("industry") == event.get("industry") else 0.5

        # Event size preference (smaller events might be better for networking)
        size_score = min(event.get("attendee_count", 0) / 200, 1.0)

        relevance = (interest_overlap * 0.5 + industry_match * 0.3 + size_score * 0.2)

        return min(relevance, 1.0)

    def _predict_event_roi(
        self,
        profile: Dict[str, Any],
        event: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Predict the ROI of attending an event."""
        return {
            "estimated_valuable_connections": 8,
            "learning_value": "high",
            "career_impact": "medium",
            "time_investment": "8 hours",
            "recommended": True
        }

    def _assess_networking_potential(
        self,
        profile: Dict[str, Any],
        event: Dict[str, Any]
    ) -> float:
        """Assess networking potential at the event."""
        attendee_count = event.get("attendee_count", 0)
        event_type = event.get("type", "")

        if event_type == "networking":
            base_score = 0.9
        elif event_type == "conference":
            base_score = 0.7
        else:
            base_score = 0.5

        # Adjust for size
        if 50 <= attendee_count <= 200:
            base_score += 0.1
        elif attendee_count > 500:
            base_score -= 0.1

        return min(base_score, 1.0)

    def _generate_event_actions(self, event: Dict[str, Any]) -> List[str]:
        """Generate recommended actions for the event."""
        return [
            "Review attendee list in advance",
            "Prepare 30-second elevator pitch",
            "Set goal to connect with 5 people"
        ]

    def _calculate_attendee_compatibility(
        self,
        user: Dict[str, Any],
        attendee: Dict[str, Any]
    ) -> float:
        """Calculate compatibility with another attendee."""
        user_interests = set(i.lower() for i in user.get("interests", []))
        attendee_interests = set(i.lower() for i in attendee.get("interests", []))

        overlap = len(user_interests.intersection(attendee_interests))
        return min(overlap / max(len(user_interests), 1), 1.0)

    def _identify_shared_interests(
        self,
        user: Dict[str, Any],
        attendee: Dict[str, Any]
    ) -> List[str]:
        """Identify shared interests between users."""
        user_interests = set(i.lower() for i in user.get("interests", []))
        attendee_interests = set(i.lower() for i in attendee.get("interests", []))

        return list(user_interests.intersection(attendee_interests))

    def _generate_conversation_starters(
        self,
        user: Dict[str, Any],
        attendee: Dict[str, Any]
    ) -> List[str]:
        """Generate conversation starters."""
        shared = self._identify_shared_interests(user, attendee)

        if shared:
            return [f"I noticed you're also interested in {shared[0]}. What's your experience with it?"]
        return ["What brings you to this event?"]


class SkillGapAnalysisAgent:
    """
    Agent specialized in identifying skill gaps and recommending
    learning paths for professional development.

    Capabilities:
    - Analyze current skill set
    - Identify skill gaps for target roles
    - Recommend learning resources
    - Create personalized learning paths
    - Track skill development progress
    - Benchmark skills against industry standards
    """

    def __init__(self, agent_id: str = "skill_gap_agent"):
        self.agent_id = agent_id
        self.proficiency = 0.92
        self.capabilities = [
            "skill_assessment",
            "gap_identification",
            "learning_path_creation",
            "resource_recommendation",
            "progress_tracking",
            "industry_benchmarking",
            "skill_prioritization"
        ]

    async def analyze_skill_gaps(
        self,
        current_skills: List[Dict[str, Any]],
        target_role: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze skill gaps between current skills and target role requirements.

        Args:
            current_skills: List of current skills with proficiency levels
            target_role: Target role with required skills

        Returns:
            Skill gap analysis with recommendations
        """
        required_skills = target_role.get("required_skills", [])
        current_skill_map = {s["name"]: s.get("proficiency", 0) for s in current_skills}

        gaps = []
        for required in required_skills:
            skill_name = required.get("name", "")
            required_level = required.get("level", 0)
            current_level = current_skill_map.get(skill_name, 0)

            if current_level < required_level:
                gap = {
                    "skill": skill_name,
                    "current_level": current_level,
                    "required_level": required_level,
                    "gap_size": required_level - current_level,
                    "priority": self._calculate_skill_priority(required),
                    "estimated_learning_time": self._estimate_learning_time(
                        current_level, required_level
                    )
                }
                gaps.append(gap)

        # Sort by priority
        gaps.sort(key=lambda x: x["priority"], reverse=True)

        return {
            "status": "success",
            "agent": self.agent_id,
            "skill_gaps": gaps,
            "total_gaps": len(gaps),
            "proficiency": self.proficiency
        }

    async def create_learning_path(
        self,
        skill_gaps: List[Dict[str, Any]],
        time_commitment: str = "10_hours_week"
    ) -> Dict[str, Any]:
        """
        Create a personalized learning path to close skill gaps.

        Args:
            skill_gaps: Identified skill gaps
            time_commitment: Weekly time commitment for learning

        Returns:
            Structured learning path with resources and timeline
        """
        learning_path = {
            "phases": self._create_learning_phases(skill_gaps),
            "estimated_duration": self._calculate_total_duration(skill_gaps, time_commitment),
            "resources": self._recommend_learning_resources(skill_gaps),
            "milestones": self._define_milestones(skill_gaps),
            "practice_projects": self._suggest_practice_projects(skill_gaps)
        }

        return {
            "status": "success",
            "agent": self.agent_id,
            "learning_path": learning_path,
            "proficiency": self.proficiency
        }

    def _calculate_skill_priority(self, skill: Dict[str, Any]) -> float:
        """Calculate priority of acquiring a skill."""
        importance = skill.get("importance", "medium")

        priority_map = {
            "critical": 1.0,
            "high": 0.8,
            "medium": 0.5,
            "low": 0.3
        }

        return priority_map.get(importance, 0.5)

    def _estimate_learning_time(self, current_level: float, target_level: float) -> str:
        """Estimate time needed to reach target skill level."""
        gap = target_level - current_level

        if gap <= 0.2:
            return "1-2 months"
        elif gap <= 0.4:
            return "3-4 months"
        elif gap <= 0.6:
            return "5-6 months"
        else:
            return "6-12 months"

    def _create_learning_phases(self, gaps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create learning phases based on skill gaps."""
        phases = [
            {
                "phase": "Foundation",
                "duration": "1-2 months",
                "skills": [g["skill"] for g in gaps[:2]],
                "goals": ["Build fundamental understanding"]
            },
            {
                "phase": "Application",
                "duration": "2-3 months",
                "skills": [g["skill"] for g in gaps[2:4]],
                "goals": ["Apply skills in practice projects"]
            },
            {
                "phase": "Mastery",
                "duration": "3-4 months",
                "skills": [g["skill"] for g in gaps[4:]],
                "goals": ["Achieve proficiency through real-world application"]
            }
        ]
        return phases

    def _calculate_total_duration(self, gaps: List[Dict[str, Any]], commitment: str) -> str:
        """Calculate total learning path duration."""
        # Simplified calculation
        return "6-9 months"

    def _recommend_learning_resources(self, gaps: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Recommend learning resources for skill gaps."""
        resources = {}

        for gap in gaps:
            skill = gap["skill"]
            resources[skill] = [
                "Online courses (Coursera, Udemy)",
                "Books and documentation",
                "Practice projects",
                "Mentorship"
            ]

        return resources

    def _define_milestones(self, gaps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Define learning milestones."""
        milestones = [
            {
                "milestone": "Complete foundational courses",
                "timeline": "Month 2",
                "criteria": "Pass assessments with 80% score"
            },
            {
                "milestone": "Build first practice project",
                "timeline": "Month 4",
                "criteria": "Deploy working project"
            },
            {
                "milestone": "Contribute to real-world project",
                "timeline": "Month 6",
                "criteria": "Make meaningful contributions"
            }
        ]
        return milestones

    def _suggest_practice_projects(self, gaps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Suggest practice projects for skill development."""
        projects = [
            {
                "project": "Personal Portfolio Website",
                "skills_practiced": ["web_development", "design"],
                "difficulty": "beginner",
                "estimated_time": "2-3 weeks"
            },
            {
                "project": "Data Analysis Dashboard",
                "skills_practiced": ["data_analysis", "visualization"],
                "difficulty": "intermediate",
                "estimated_time": "3-4 weeks"
            }
        ]
        return projects


# Factory function
def create_career_mentorship_agent_pool() -> Dict[str, Any]:
    """
    Create a pool of career and mentorship agents.

    Returns:
        Dictionary mapping agent IDs to agent instances
    """
    return {
        "career_path": CareerPathAgent("career_path_agent"),
        "mentorship_matching": MentorshipMatchingAgent("mentorship_matching_agent"),
        "event_recommendation": EventRecommendationAgent("event_recommendation_agent"),
        "skill_gap_analysis": SkillGapAnalysisAgent("skill_gap_analysis_agent")
    }
