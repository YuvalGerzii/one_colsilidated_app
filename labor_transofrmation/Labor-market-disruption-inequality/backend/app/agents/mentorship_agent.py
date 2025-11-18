"""
Mentorship Matching Agent
Connects workers with mentors and builds mentorship relationships
"""

from typing import Dict, List, Any
from .base_agent import BaseAgent


class MentorshipMatchingAgent(BaseAgent):
    """AI agent specialized in mentorship matching and relationship building"""

    def __init__(self):
        super().__init__(
            name="Mentorship Matching Agent",
            role="Mentorship Coordinator",
            expertise=[
                "Mentor matching",
                "Relationship building",
                "Career guidance",
                "Skill development planning",
                "Network leveraging"
            ]
        )

    def find_mentors(self, worker_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Find and rank potential mentors"""
        target_role = worker_profile.get("target_role", "")
        current_role = worker_profile.get("current_role", "")
        skills_to_develop = worker_profile.get("skills_gaps", [])
        industry = worker_profile.get("industry", "")

        # Mock mentor matches
        mentor_matches = [
            {
                "name": "Senior Professional A",
                "current_role": target_role,
                "experience_years": 12,
                "expertise": skills_to_develop[:2],
                "match_score": 92,
                "availability": "Monthly 1-hour sessions",
                "mentorship_style": "Hands-on, project-based guidance",
                "why_good_match": f"Has {target_role} experience you're targeting, expertise in your gap areas"
            },
            {
                "name": "Industry Leader B",
                "current_role": f"Senior {target_role}",
                "experience_years": 8,
                "expertise": [skills_to_develop[0]] if skills_to_develop else [],
                "match_score": 85,
                "availability": "Bi-weekly 30-min calls",
                "mentorship_style": "Strategic career advice, networking",
                "why_good_match": "Recently made similar transition, strong industry network"
            }
        ]

        return {
            "total_matches": len(mentor_matches),
            "top_matches": mentor_matches,
            "matching_criteria": {
                "role_alignment": "60%",
                "skill_overlap": "30%",
                "availability": "10%"
            },
            "next_steps": self._get_mentor_outreach_guide(),
            "relationship_building_tips": self._get_relationship_tips()
        }

    def create_mentorship_plan(self, mentorship_goal: str) -> Dict[str, Any]:
        """Create structured mentorship relationship plan"""
        return {
            "goals": {
                "primary": mentorship_goal,
                "supporting": ["Skill development", "Network expansion", "Career guidance"]
            },
            "meeting_cadence": "Monthly 1-hour sessions + async messaging",
            "session_structure": {
                "check_in": "5 min - Progress since last meeting",
                "deep_dive": "40 min - Main topic/challenge",
                "action_items": "10 min - Next steps and goals",
                "wrap_up": "5 min - Scheduling and thanks"
            },
            "monthly_themes": {
                "month_1": "Current state assessment, goal setting",
                "month_2": "Skill development plan",
                "month_3": "Networking strategy",
                "month_4": "Career path exploration",
                "month_5_6": "Specific skill deep-dives"
            },
            "success_metrics": [
                "Skills acquired or improved",
                "Network connections made",
                "Career decisions clarified",
                "Opportunities created"
            ]
        }

    def _get_mentor_outreach_guide(self) -> List[Dict[str, str]]:
        """Get mentor outreach templates"""
        return [
            {
                "stage": "Initial outreach",
                "message": "Hi [Name], I admire your work in [X]. I'm transitioning to [role] and would value your guidance. Would you be open to a 20-min coffee chat?",
                "timing": "Week 1"
            },
            {
                "stage": "After first meeting",
                "message": "Thank you for the insightful conversation. Your advice on [X] was particularly helpful. Would you be open to a monthly mentorship relationship?",
                "timing": "Within 48 hours"
            }
        ]

    def _get_relationship_tips(self) -> List[str]:
        """Get mentorship relationship tips"""
        return [
            "Always come prepared with specific questions",
            "Respect their time - be punctual and concise",
            "Act on their advice and report back",
            "Offer value in return (insights from your perspective, connections)",
            "Send thank you notes and updates on your progress"
        ]
