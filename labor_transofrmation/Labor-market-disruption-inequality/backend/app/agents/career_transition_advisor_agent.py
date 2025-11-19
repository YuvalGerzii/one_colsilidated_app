"""
Career Transition Advisor Agent
Specialized guidance for career pivots and major transitions
"""

from typing import Dict, List, Any
from .base_agent import BaseAgent


class CareerTransitionAdvisorAgent(BaseAgent):
    """AI agent specialized in career transition planning and execution"""

    def __init__(self):
        super().__init__(
            agent_id="career_transition_advisor",
            agent_type="Career Pivot Specialist"
        )
        self.capabilities = [
            "Career change planning",
            "Skill transferability",
            "Transition timeline",
            "Risk mitigation",
            "Industry pivots"
        ]

    def process_task(self, task: Dict) -> 'AgentResponse':
        """Process a task assigned to this agent"""
        from datetime import datetime
        from .base_agent import AgentResponse

        task_type = task.get('type', 'assess_feasibility')

        if task_type == 'assess_feasibility':
            result = self.assess_transition_feasibility(task.get('transition_data', task))
        elif task_type == 'create_roadmap':
            result = self.create_transition_roadmap(task.get('transition_goal', task))
        else:
            result = self.assess_transition_feasibility(task)

        return AgentResponse(
            agent_id=self.agent_id,
            agent_type=self.agent_type,
            status='success',
            data=result,
            confidence=0.85,
            recommendations=result.get('risk_mitigation', []) if isinstance(result, dict) else [],
            next_steps=[],
            timestamp=datetime.now(),
            metadata={'task_type': task_type}
        )

    def analyze(self, data: Dict) -> Dict:
        """Analyze provided data according to agent's specialization"""
        return self.assess_transition_feasibility(data)

    def assess_transition_feasibility(self, transition_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess feasibility of career transition"""

        current_role = transition_data.get("current_role", "")
        target_role = transition_data.get("target_role", "")
        current_skills = transition_data.get("current_skills", [])
        target_skills_required = transition_data.get("target_skills", [])
        financial_runway_months = transition_data.get("financial_runway", 6)
        time_available_weekly = transition_data.get("time_weekly", 10)

        # Calculate skill overlap
        transferable_skills = [s for s in current_skills if s in target_skills_required]
        overlap_percentage = (len(transferable_skills) / len(target_skills_required) * 100) if target_skills_required else 0

        # Assess difficulty
        if overlap_percentage >= 70:
            difficulty = "easy"
            estimated_months = 3
        elif overlap_percentage >= 50:
            difficulty = "moderate"
            estimated_months = 6
        elif overlap_percentage >= 30:
            difficulty = "challenging"
            estimated_months = 12
        else:
            difficulty = "very_challenging"
            estimated_months = 18

        # Feasibility assessment
        is_feasible = financial_runway_months >= (estimated_months * 0.7) and time_available_weekly >= 10

        return {
            "feasibility_score": round((overlap_percentage + (financial_runway_months/estimated_months)*30), 1),
            "is_feasible": is_feasible,
            "difficulty_level": difficulty,
            "estimated_timeline_months": estimated_months,
            "skill_analysis": {
                "transferable_skills": transferable_skills,
                "skills_to_learn": [s for s in target_skills_required if s not in current_skills],
                "overlap_percentage": round(overlap_percentage, 1)
            },
            "resource_requirements": {
                "time_commitment": f"{time_available_weekly} hours/week for {estimated_months} months",
                "financial_runway_needed": f"{estimated_months} months",
                "financial_runway_available": f"{financial_runway_months} months",
                "runway_sufficient": financial_runway_months >= estimated_months
            },
            "transition_strategy": self._create_transition_strategy(difficulty, estimated_months),
            "risk_mitigation": self._get_risk_mitigation_strategies(transition_data)
        }

    def create_transition_roadmap(self, transition_goal: Dict[str, Any]) -> Dict[str, Any]:
        """Create detailed transition roadmap"""

        timeline_months = transition_goal.get("timeline_months", 12)

        phases = {
            "phase_1_foundation": {
                "duration": "Months 1-3",
                "focus": "Skill building + Foundation",
                "milestones": [
                    "Complete 2-3 foundational courses",
                    "Build 1-2 beginner projects",
                    "Join professional communities",
                    "Start building network in target field"
                ]
            },
            "phase_2_skill_development": {
                "duration": "Months 4-6",
                "focus": "Advanced skills + Portfolio",
                "milestones": [
                    "Complete advanced training",
                    "Build 2-3 intermediate projects",
                    "Get certified in key technologies",
                    "Contribute to open source or volunteer projects"
                ]
            },
            "phase_3_positioning": {
                "duration": "Months 7-9",
                "focus": "Job market positioning",
                "milestones": [
                    "Build impressive portfolio project",
                    "Tailor resume for new role",
                    "Conduct informational interviews",
                    "Apply to stretch roles"
                ]
            },
            "phase_4_job_search": {
                "duration": "Months 10-12",
                "focus": "Active job search",
                "milestones": [
                    "Apply to 10-15 target roles per week",
                    "Leverage network for referrals",
                    "Prepare for technical interviews",
                    "Negotiate and accept offer"
                ]
            }
        }

        return {
            "total_duration_months": timeline_months,
            "phases": phases,
            "weekly_commitments": {
                "learning": "8-10 hours",
                "projects": "5-7 hours",
                "networking": "2-3 hours",
                "total": "15-20 hours/week"
            },
            "success_checkpoints": self._get_success_checkpoints(),
            "common_pitfalls": self._get_transition_pitfalls()
        }

    def _create_transition_strategy(self, difficulty: str, months: int) -> Dict[str, str]:
        """Create transition strategy based on difficulty"""
        if difficulty == "easy":
            return {
                "approach": "Direct transition",
                "strategy": "Apply to entry-level roles in target field while building portfolio",
                "timeline": f"{months} months"
            }
        elif difficulty in ["moderate", "challenging"]:
            return {
                "approach": "Bridge role strategy",
                "strategy": "Find intermediate role that uses transferable skills + some new ones",
                "timeline": f"{months} months to bridge role, then 6-12 more to target"
            }
        else:
            return {
                "approach": "Complete reskilling",
                "strategy": "Intensive training program or bootcamp + portfolio building",
                "timeline": f"{months} months full preparation"
            }

    def _get_risk_mitigation_strategies(self, transition_data: Dict) -> List[Dict[str, str]]:
        """Get risk mitigation strategies"""
        return [
            {
                "risk": "Financial instability",
                "mitigation": "Build 6-12 month emergency fund before transition",
                "action": "Side hustle or part-time work during transition"
            },
            {
                "risk": "Skill gaps too large",
                "mitigation": "Consider bridge role or internship",
                "action": "Take structured courses with mentorship"
            },
            {
                "risk": "Lack of network",
                "mitigation": "Join communities, attend events, informational interviews",
                "action": "Connect with 3-5 people in target field per week"
            }
        ]

    def _get_success_checkpoints(self) -> List[str]:
        """Get success checkpoints for transition"""
        return [
            "Month 3: Completed foundational courses + 2 projects",
            "Month 6: Portfolio with 4-5 projects + certifications",
            "Month 9: Had 10+ informational interviews + network of 50+ in field",
            "Month 12: Received offer in target role"
        ]

    def _get_transition_pitfalls(self) -> List[Dict[str, str]]:
        """Get common transition pitfalls"""
        return [
            {
                "pitfall": "Moving too fast without foundation",
                "consequence": "Applications rejected, confidence damaged",
                "avoid": "Build solid foundation before applying"
            },
            {
                "pitfall": "Not networking enough",
                "consequence": "Miss hidden opportunities, lack referrals",
                "avoid": "Network from day 1, informational interviews"
            },
            {
                "pitfall": "Insufficient financial runway",
                "consequence": "Forced to take any job, abandon transition",
                "avoid": "Save 6-12 months expenses before full transition"
            }
        ]
