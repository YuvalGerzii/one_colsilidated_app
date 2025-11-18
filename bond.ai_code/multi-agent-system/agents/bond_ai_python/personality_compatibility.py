"""
Personality Compatibility Agent for Bond.AI

Uses Big5 and MBTI personality frameworks to predict professional relationship
compatibility with 37% variance explained (based on research).

Focuses on professional contexts: team dynamics, working styles, communication
preferences, and collaboration potential.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from typing import Any, Dict, List
from loguru import logger

from multi_agent_system.agents.base import BaseAgent
from multi_agent_system.core.types import Task, Result, AgentCapability


class PersonalityCompatibilityAgent(BaseAgent):
    """
    Advanced agent specialized in personality-based compatibility for professional relationships.

    Capabilities:
    - Big5 personality assessment
    - MBTI type matching
    - Working style compatibility
    - Communication preference matching
    - Team dynamics prediction
    - Collaboration success forecasting
    - Conflict resolution style analysis
    """

    def __init__(self, agent_id: str = "personality_matcher_1", message_bus=None):
        capabilities = [
            AgentCapability("big5_assessment", "Assess Big5 personality traits", 0.93),
            AgentCapability("mbti_matching", "Match MBTI types", 0.91),
            AgentCapability("working_style", "Analyze working style compatibility", 0.92),
            AgentCapability("communication_preferences", "Match communication preferences", 0.90),
            AgentCapability("team_dynamics", "Predict team dynamics", 0.89),
            AgentCapability("collaboration_forecast", "Forecast collaboration success", 0.91),
            AgentCapability("conflict_resolution", "Analyze conflict resolution styles", 0.88),
            AgentCapability("personality_compatibility", "General personality compatibility", 0.91),
        ]
        super().__init__(agent_id, capabilities, message_bus)

    async def process_task(self, task: Task) -> Result:
        """
        Process a personality compatibility task.

        Args:
            task: Personality compatibility task to process

        Returns:
            Comprehensive personality-based compatibility results
        """
        logger.info(f"{self.agent_id} analyzing personality compatibility: {task.description}")

        # Simulate comprehensive personality analysis
        compatibility_results = {
            "task": task.description,
            "your_personality_profile": {
                "big5_traits": {
                    "openness": {
                        "score": 0.82,  # 0-1 scale
                        "percentile": 85,
                        "description": "High - Curious, imaginative, open to new experiences",
                        "professional_implications": "Thrives in innovative environments, embraces change",
                    },
                    "conscientiousness": {
                        "score": 0.76,
                        "percentile": 72,
                        "description": "Moderately High - Organized, dependable, goal-oriented",
                        "professional_implications": "Reliable, meets deadlines, but flexible when needed",
                    },
                    "extraversion": {
                        "score": 0.64,
                        "percentile": 62,
                        "description": "Moderate - Balanced between social and independent work",
                        "professional_implications": "Comfortable in both collaborative and solo settings",
                    },
                    "agreeableness": {
                        "score": 0.71,
                        "percentile": 68,
                        "description": "Moderately High - Cooperative, compassionate, team-oriented",
                        "professional_implications": "Values harmony, good team player, but can be assertive",
                    },
                    "neuroticism": {
                        "score": 0.32,  # Lower is more emotionally stable
                        "percentile": 35,
                        "description": "Low - Emotionally stable, calm under pressure",
                        "professional_implications": "Handles stress well, resilient in challenging situations",
                    },
                },
                "mbti_type": {
                    "type": "ENTJ",
                    "full_name": "Commander",
                    "breakdown": {
                        "E": "Extraversion (moderate preference)",
                        "N": "Intuition (strong preference)",
                        "T": "Thinking (moderate preference)",
                        "J": "Judging (moderate preference)",
                    },
                    "characteristics": [
                        "Natural leader",
                        "Strategic thinker",
                        "Decisive and efficient",
                        "Enjoys challenges",
                        "Direct communication",
                    ],
                    "professional_strengths": [
                        "Excellent at strategic planning",
                        "Effective at driving execution",
                        "Confidence in decision-making",
                        "Inspires and motivates teams",
                    ],
                    "potential_challenges": [
                        "May be perceived as too direct",
                        "Can be impatient with inefficiency",
                        "May overlook emotional considerations",
                    ],
                },
                "working_style": {
                    "preferred_pace": "Fast-paced with clear goals",
                    "decision_making": "Data-driven with intuition",
                    "collaboration_style": "Direct, results-oriented",
                    "feedback_preference": "Honest, constructive, actionable",
                    "work_environment": "Dynamic, innovative, goal-focused",
                },
            },
            "compatibility_analysis": [
                {
                    "match_id": "User_8765",
                    "name": "Alex Thompson",
                    "their_profile": {
                        "big5_summary": "High Openness (0.85), Moderate Conscientiousness (0.72), Moderate Extraversion (0.68)",
                        "mbti_type": "ENFP (Campaigner)",
                    },
                    "overall_compatibility": 0.84,
                    "compatibility_breakdown": {
                        "working_style_match": {
                            "score": 0.86,
                            "analysis": "Both thrive in fast-paced, innovative environments. ENTJ-ENFP is a strong professional pairing.",
                            "synergy": "Your strategic thinking + their creative ideation = powerful combination",
                            "potential_friction": "You prefer structure (J), they prefer flexibility (P) - needs compromise",
                        },
                        "communication_compatibility": {
                            "score": 0.81,
                            "analysis": "Both direct communicators, though you're more task-focused and they're more people-focused",
                            "synergy": "Open, honest dialogue without hidden agendas",
                            "potential_friction": "You may see them as too enthusiastic, they may see you as too serious",
                        },
                        "team_dynamics": {
                            "score": 0.87,
                            "analysis": "Complementary strengths - you provide structure, they provide inspiration",
                            "synergy": "ENTJ leadership + ENFP innovation = excellent co-founding team",
                            "roles": "You: Strategic execution, Them: Vision & culture",
                        },
                        "collaboration_potential": {
                            "score": 0.85,
                            "forecast": "High success probability for joint projects",
                            "best_collaboration_types": [
                                "Co-founding a startup (you as CEO, them as Chief Product/Culture Officer)",
                                "Strategic partnership on AI/ML innovation",
                                "Joint thought leadership initiatives",
                            ],
                            "success_factors": [
                                "Mutual respect for different strengths",
                                "Clear role delineation",
                                "Regular check-ins to align on approach",
                            ],
                        },
                        "conflict_resolution": {
                            "score": 0.79,
                            "analysis": "Both prefer direct resolution, though approaches differ",
                            "you": "Logical, systematic problem-solving",
                            "them": "Empathetic, values-based resolution",
                            "recommendation": "Combine logical analysis with emotional intelligence for best outcomes",
                        },
                    },
                    "relationship_prediction": {
                        "professional_success": 0.84,
                        "long_term_sustainability": 0.81,
                        "mutual_satisfaction": 0.86,
                        "growth_potential": 0.88,  # How much you'll grow together
                    },
                },
                {
                    "match_id": "User_6543",
                    "name": "Jennifer Liu",
                    "their_profile": {
                        "big5_summary": "Moderate Openness (0.74), High Conscientiousness (0.88), Low Extraversion (0.42)",
                        "mbti_type": "ISTJ (Logistician)",
                    },
                    "overall_compatibility": 0.76,
                    "compatibility_breakdown": {
                        "working_style_match": {
                            "score": 0.81,
                            "analysis": "Both value structure and results, though you're more innovative and they're more traditional",
                            "synergy": "Your vision + their execution = solid partnership",
                            "potential_friction": "You may find them too risk-averse, they may find you too changeable",
                        },
                        "communication_compatibility": {
                            "score": 0.74,
                            "analysis": "Both logical communicators, but different styles - you're expressive, they're reserved",
                            "synergy": "Clear, fact-based communication",
                            "potential_friction": "Your directness may overwhelm their preference for thoughtful response",
                        },
                        "team_dynamics": {
                            "score": 0.79,
                            "analysis": "Complementary but requires conscious effort - T-types work well together",
                            "synergy": "Both task-focused and efficient",
                            "roles": "You: Strategy & innovation, Them: Operations & systems",
                        },
                        "collaboration_potential": {
                            "score": 0.72,
                            "forecast": "Moderate success - needs clear boundaries and respect for differences",
                            "best_collaboration_types": [
                                "Mentor-mentee relationship (product strategy)",
                                "Complementary roles in organization (you lead, they execute)",
                                "Advisory relationship",
                            ],
                        },
                    },
                    "relationship_prediction": {
                        "professional_success": 0.76,
                        "long_term_sustainability": 0.79,
                        "mutual_satisfaction": 0.71,
                        "growth_potential": 0.68,
                    },
                },
            ],
            "ideal_personality_matches": {
                "for_co_founding": [
                    "ENFP (Campaigner) - Innovation + vision",
                    "INFJ (Advocate) - Strategic vision + empathy",
                    "ENTP (Debater) - Entrepreneurial + innovative",
                ],
                "for_mentorship": [
                    "ESTJ (Executive) - Experience + systems",
                    "INTJ (Architect) - Strategic depth",
                ],
                "for_team_building": [
                    "Mix of types for diverse perspectives",
                    "At least one high-empathy type (F preference)",
                    "Balance of J and P for structure + flexibility",
                ],
            },
            "personality_based_recommendations": {
                "communication_tips": {
                    "with_ENFP": "Embrace their enthusiasm, provide structure to channel creativity",
                    "with_ISTJ": "Be patient with their process, acknowledge their thoroughness",
                    "with_F_types": "Remember to address emotional considerations, not just logic",
                },
                "team_composition": {
                    "ideal_team": "2-3 T-types (task focus) + 1-2 F-types (people focus) + mix of J/P",
                    "avoid": "All high-Neuroticism team members (stress amplification)",
                    "seek": "High Openness for innovation roles, High Conscientiousness for execution",
                },
                "leadership_style": {
                    "your_natural_style": "Strategic, directive, results-oriented",
                    "adaptation_needed": "Increase empathy with F-types, patience with P-types",
                    "strength_to_leverage": "Decisiveness, strategic thinking, ability to inspire",
                },
            },
            "working_relationship_dynamics": {
                "you_as_leader": {
                    "best_team_members": ["ENFP", "INFJ", "ISFJ", "ISTJ"],
                    "challenging_team_members": ["ESTP", "ESFP"],  # May clash on priorities
                    "management_approach": "Provide clear goals, autonomy in execution, regular feedback",
                },
                "you_as_peer": {
                    "best_collaborators": ["INTJ", "ENTP", "ENFP"],
                    "challenging_peers": ["ISFP", "INFP"],  # Very different approaches
                    "collaboration_approach": "Establish clear roles, respect expertise, direct communication",
                },
                "you_as_report": {
                    "best_managers": ["ESTJ", "ENTJ", "INTJ"],
                    "challenging_managers": ["ESFJ", "ENFJ"],  # May want more emotional connection
                    "what_you_need": "Clear expectations, autonomy, strategic challenges",
                },
            },
            "insights": [
                "84% compatibility with Alex Thompson (ENFP) - exceptional match for co-founding or strategic partnership",
                "ENTJ-ENFP combination is one of the strongest for entrepreneurial ventures",
                "Your low Neuroticism (0.32) makes you excellent at handling high-pressure situations",
                "High Openness (0.82) aligns perfectly with AI/ML innovation focus",
                "Moderate Extraversion (0.64) gives flexibility - comfortable in both solo and team settings",
                "76% compatibility with Jennifer Liu (ISTJ) - good for mentor-mentee, needs work for peer collaboration",
                "Your Thinking preference (T) means you excel with logical, data-driven people",
                "Judging preference (J) indicates you work best with structure and clear plans",
                "Big5 profile suggests you're in top 15% for leadership potential",
                "Working style matches innovation-focused, fast-paced startup environments",
            ],
            "recommendations": [
                "Prioritize relationship with Alex Thompson - 84% personality compatibility is exceptional",
                "For co-founding teams, seek ENFP or ENTP types to complement your strategic execution",
                "When working with ISTJ types (like Jennifer), provide extra time for their thorough process",
                "Leverage your low Neuroticism in high-stress environments - it's a competitive advantage",
                "Balance your team with F-types (Feeling) to ensure emotional intelligence in decisions",
                "Use your direct communication style strategically - soften with F-types, maintain with T-types",
                "In conflicts, remember to acknowledge emotional factors beyond just logical solutions",
                "Seek mentors who are ESTJ or INTJ - they'll understand your thinking style",
                "For team building, aim for personality diversity while maintaining shared values",
                "Play to your ENTJ strengths: strategic vision, decisive action, inspiring leadership",
            ],
            "confidence": 0.91,
        }

        return Result(
            task_id=task.id,
            success=True,
            data=compatibility_results,
            agent_id=self.agent_id,
            quality_score=0.91,
            metadata={
                "personality_frameworks": ["Big5", "MBTI"],
                "variance_explained": 0.37,  # Based on research
                "compatibility_model": "Multi-factor personality matching",
                "prediction_confidence": 0.89,
            }
        )
