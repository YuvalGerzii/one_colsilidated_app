"""
Emotional Intelligence (EQ) Agent for Bond.AI

Assesses and matches professionals based on emotional intelligence competencies.
Uses the Goleman EQ model with four domains: self-awareness, self-management,
social awareness, and relationship management.

Research shows EQ often predicts professional success better than IQ,
especially in leadership, sales, and collaborative roles.

Key Features:
- Self-awareness assessment (emotional self-awareness, accurate self-assessment)
- Self-regulation analysis (emotional self-control, adaptability, achievement orientation)
- Social awareness (empathy, organizational awareness, service orientation)
- Relationship management (influence, conflict management, teamwork, inspiration)
- EQ compatibility scoring for partnerships
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from typing import Any, Dict, List, Optional
from loguru import logger

from multi_agent_system.agents.base import BaseAgent
from multi_agent_system.core.types import Task, Result, AgentCapability


class EmotionalIntelligenceAgent(BaseAgent):
    """
    Advanced agent specialized in emotional intelligence assessment and matching.

    Based on Daniel Goleman's EQ framework with four core domains:
    1. Self-Awareness
    2. Self-Management
    3. Social Awareness
    4. Relationship Management

    Capabilities:
    - Comprehensive EQ assessment
    - EQ-based compatibility matching
    - Leadership potential prediction
    - Team dynamics optimization
    - Conflict resolution style analysis
    - Emotional maturity scoring
    """

    def __init__(self, agent_id: str = "eq_analyst_1", message_bus=None):
        capabilities = [
            AgentCapability("eq_assessment", "Assess overall emotional intelligence", 0.90),
            AgentCapability("self_awareness", "Evaluate self-awareness competencies", 0.89),
            AgentCapability("self_management", "Evaluate self-management competencies", 0.88),
            AgentCapability("social_awareness", "Evaluate social awareness competencies", 0.91),
            AgentCapability("relationship_management", "Evaluate relationship management", 0.90),
            AgentCapability("eq_compatibility", "Match based on EQ compatibility", 0.87),
            AgentCapability("leadership_eq", "Assess leadership EQ", 0.89),
            AgentCapability("team_eq", "Optimize team EQ composition", 0.86),
        ]
        super().__init__(agent_id, capabilities, message_bus)

    async def process_task(self, task: Task) -> Result:
        """
        Process an emotional intelligence assessment task.

        Args:
            task: EQ assessment task to process

        Returns:
            Comprehensive emotional intelligence analysis results
        """
        logger.info(f"{self.agent_id} analyzing emotional intelligence: {task.description}")

        # Simulate comprehensive EQ analysis
        eq_analysis = {
            "task": task.description,

            "overall_eq_profile": {
                "eq_score": 0.82,  # 0-1 scale (0.82 = 82nd percentile)
                "percentile": 82,
                "level": "High",  # Low, Medium, High, Very High, Exceptional
                "description": "Strong emotional intelligence with balanced competencies",
                "professional_suitability": [
                    "Leadership roles",
                    "Client-facing positions",
                    "Team management",
                    "Partnership development",
                    "Conflict mediation"
                ]
            },

            "domain_1_self_awareness": {
                "overall_score": 0.85,
                "percentile": 85,
                "level": "High",
                "description": "Strong understanding of own emotions, strengths, and limitations",

                "competencies": {
                    "emotional_self_awareness": {
                        "score": 0.87,
                        "description": "Recognizes own emotions and their effects",
                        "indicators": [
                            "Accurately identifies own emotional states",
                            "Understands emotional triggers",
                            "Aware of how emotions influence decisions",
                            "Recognizes emotional patterns"
                        ],
                        "professional_impact": "Makes better decisions by understanding emotional biases"
                    },
                    "accurate_self_assessment": {
                        "score": 0.83,
                        "description": "Knows own strengths and weaknesses",
                        "indicators": [
                            "Realistic about capabilities",
                            "Open to feedback and criticism",
                            "Recognizes areas for improvement",
                            "Acknowledges mistakes"
                        ],
                        "professional_impact": "Continuous growth mindset, seeks appropriate help"
                    },
                    "self_confidence": {
                        "score": 0.84,
                        "description": "Strong sense of self-worth and capabilities",
                        "indicators": [
                            "Presents ideas with conviction",
                            "Comfortable taking calculated risks",
                            "Not overly defensive",
                            "Handles setbacks with resilience"
                        ],
                        "professional_impact": "Inspires confidence in others, effective leadership"
                    }
                }
            },

            "domain_2_self_management": {
                "overall_score": 0.79,
                "percentile": 78,
                "level": "Moderately High",
                "description": "Good emotional self-control with room for growth in adaptability",

                "competencies": {
                    "emotional_self_control": {
                        "score": 0.81,
                        "description": "Manages disruptive emotions and impulses",
                        "indicators": [
                            "Stays calm under pressure",
                            "Thinks before acting",
                            "Manages frustration constructively",
                            "Rarely has emotional outbursts"
                        ],
                        "professional_impact": "Trusted in high-stress situations, stable leadership"
                    },
                    "transparency": {
                        "score": 0.83,
                        "description": "Displays honesty and integrity",
                        "indicators": [
                            "Admits mistakes openly",
                            "Confronts unethical behavior",
                            "Builds trust through authenticity",
                            "Values-driven decision making"
                        ],
                        "professional_impact": "High trust, ethical leadership, strong reputation"
                    },
                    "adaptability": {
                        "score": 0.74,
                        "description": "Flexible in handling change",
                        "indicators": [
                            "Adjusts to new situations",
                            "Handles multiple demands",
                            "Adapts strategies when needed",
                            "Moderately comfortable with ambiguity"
                        ],
                        "professional_impact": "Good in evolving environments, some preference for stability",
                        "development_area": True
                    },
                    "achievement_orientation": {
                        "score": 0.86,
                        "description": "Strives to meet/exceed standards of excellence",
                        "indicators": [
                            "Sets challenging goals",
                            "Takes calculated risks for improvement",
                            "Learns from data and feedback",
                            "Continuously seeks improvement"
                        ],
                        "professional_impact": "High performer, drives results, inspires excellence"
                    },
                    "initiative": {
                        "score": 0.78,
                        "description": "Readiness to act on opportunities",
                        "indicators": [
                            "Proactive rather than reactive",
                            "Seizes opportunities",
                            "Goes beyond what's required",
                            "Creates opportunities"
                        ],
                        "professional_impact": "Entrepreneurial mindset, drives innovation"
                    },
                    "optimism": {
                        "score": 0.77,
                        "description": "Persists in pursuing goals despite obstacles",
                        "indicators": [
                            "Sees setbacks as temporary",
                            "Expects positive outcomes",
                            "Focuses on solutions not problems",
                            "Maintains hope during challenges"
                        ],
                        "professional_impact": "Resilient, motivates others, overcomes adversity"
                    }
                }
            },

            "domain_3_social_awareness": {
                "overall_score": 0.84,
                "percentile": 84,
                "level": "High",
                "description": "Highly attuned to others' emotions and organizational dynamics",

                "competencies": {
                    "empathy": {
                        "score": 0.88,
                        "description": "Senses others' feelings and perspectives",
                        "indicators": [
                            "Attentive to emotional cues",
                            "Shows genuine understanding",
                            "Considers others' viewpoints",
                            "Provides emotional support"
                        ],
                        "professional_impact": "Strong relationships, effective mentoring, high trust"
                    },
                    "organizational_awareness": {
                        "score": 0.81,
                        "description": "Reads political currents and decision networks",
                        "indicators": [
                            "Understands organizational politics",
                            "Identifies key influencers",
                            "Navigates hierarchy effectively",
                            "Recognizes underlying power dynamics"
                        ],
                        "professional_impact": "Effective navigation of complex organizations"
                    },
                    "service_orientation": {
                        "score": 0.83,
                        "description": "Anticipates, recognizes, and meets others' needs",
                        "indicators": [
                            "Focuses on serving clients/colleagues",
                            "Seeks ways to increase satisfaction",
                            "Available to help",
                            "Creates value for others"
                        ],
                        "professional_impact": "Excellent client relationships, team support"
                    }
                }
            },

            "domain_4_relationship_management": {
                "overall_score": 0.80,
                "percentile": 80,
                "level": "High",
                "description": "Strong relationship skills with excellent teamwork abilities",

                "competencies": {
                    "developing_others": {
                        "score": 0.82,
                        "description": "Bolsters others' abilities through feedback and guidance",
                        "indicators": [
                            "Provides constructive feedback",
                            "Mentors and coaches effectively",
                            "Identifies developmental needs",
                            "Celebrates others' successes"
                        ],
                        "professional_impact": "Effective mentor, builds strong teams"
                    },
                    "inspirational_leadership": {
                        "score": 0.79,
                        "description": "Inspires and guides individuals and groups",
                        "indicators": [
                            "Articulates compelling vision",
                            "Leads by example",
                            "Brings out best in people",
                            "Makes work exciting"
                        ],
                        "professional_impact": "Motivating leader, high team performance"
                    },
                    "influence": {
                        "score": 0.77,
                        "description": "Wields effective persuasion tactics",
                        "indicators": [
                            "Persuades through logic and emotion",
                            "Builds support for initiatives",
                            "Reads situations and adapts approach",
                            "Creates buy-in"
                        ],
                        "professional_impact": "Effective change agent, drives consensus"
                    },
                    "change_catalyst": {
                        "score": 0.76,
                        "description": "Initiates and manages change",
                        "indicators": [
                            "Recognizes need for change",
                            "Challenges status quo",
                            "Champions new initiatives",
                            "Overcomes resistance"
                        ],
                        "professional_impact": "Drives transformation, innovates"
                    },
                    "conflict_management": {
                        "score": 0.80,
                        "description": "Negotiates and resolves disagreements",
                        "indicators": [
                            "Handles difficult people tactfully",
                            "Finds win-win solutions",
                            "Surfaces and addresses conflicts",
                            "De-escalates tensions"
                        ],
                        "professional_impact": "Maintains team harmony, resolves issues effectively"
                    },
                    "teamwork_collaboration": {
                        "score": 0.89,
                        "description": "Works with others toward shared goals",
                        "indicators": [
                            "Balances focus on task and relationships",
                            "Collaborates and shares information",
                            "Creates team identity",
                            "Builds rapport and trust"
                        ],
                        "professional_impact": "Exceptional team player, creates synergy"
                    }
                }
            },

            "eq_strengths": [
                {
                    "competency": "Empathy",
                    "score": 0.88,
                    "impact": "Builds deep, trusting relationships quickly",
                },
                {
                    "competency": "Teamwork & Collaboration",
                    "score": 0.89,
                    "impact": "Exceptional at working with diverse teams",
                },
                {
                    "competency": "Achievement Orientation",
                    "score": 0.86,
                    "impact": "Drives high performance and results",
                },
                {
                    "competency": "Self-Awareness",
                    "score": 0.85,
                    "impact": "Makes better decisions through self-understanding",
                }
            ],

            "development_areas": [
                {
                    "competency": "Adaptability",
                    "score": 0.74,
                    "recommendation": "Practice embracing ambiguity and rapid change",
                    "priority": "medium"
                },
                {
                    "competency": "Change Catalyst",
                    "score": 0.76,
                    "recommendation": "Take lead on transformation initiatives",
                    "priority": "low"
                },
                {
                    "competency": "Influence",
                    "score": 0.77,
                    "recommendation": "Study persuasion techniques, practice stakeholder management",
                    "priority": "medium"
                }
            ],

            "leadership_potential": {
                "overall_score": 0.81,
                "level": "High",
                "leadership_style": "Collaborative-Achiever",
                "description": "Strong leadership potential with people-first approach",
                "suitable_roles": [
                    "Team Lead / Manager",
                    "Director of People Operations",
                    "VP of Client Success",
                    "Co-founder (COO/CPO)",
                    "Head of Partnerships"
                ],
                "key_strengths": [
                    "Builds cohesive, high-performing teams",
                    "Balances people and results effectively",
                    "High empathy creates psychological safety",
                    "Strong ethical foundation"
                ],
                "watch_areas": [
                    "May struggle with rapid, disruptive change",
                    "Could benefit from more assertive influence tactics"
                ]
            },

            "eq_compatibility_analysis": {
                "description": "EQ-based matching recommendations",
                "ideal_partners": {
                    "co_founder": {
                        "preferred_eq_profile": {
                            "adaptability": "high",  # Complement development area
                            "change_catalyst": "high",  # Complement
                            "teamwork": "high",  # Match strength
                            "achievement_orientation": "high",  # Match strength
                        },
                        "reasoning": "Seek co-founder with high adaptability to balance your preference for stability, while matching on teamwork and drive"
                    },
                    "team_members": {
                        "preferred_mix": "High empathy + varied achievement orientation + diverse conflict styles",
                        "reasoning": "Build psychologically safe teams with complementary approaches to goals and conflict"
                    },
                    "mentor": {
                        "preferred_eq_profile": {
                            "organizational_awareness": "very_high",
                            "influence": "very_high",
                            "adaptability": "high",
                        },
                        "reasoning": "Seek mentors strong in your development areas"
                    },
                    "clients": {
                        "best_fit": "Relationship-oriented, collaborative, value-driven",
                        "challenging_fit": "Highly transactional, low trust, frequent pivots",
                        "reasoning": "Your empathy and teamwork shine with collaborative clients"
                    }
                },
                "compatibility_with_eq_archetypes": {
                    "visionary_leader": {
                        "compatibility": 0.82,
                        "synergy": "Your execution and teamwork complement their vision",
                        "friction": "May struggle with their rapid change pace"
                    },
                    "analytical_achiever": {
                        "compatibility": 0.78,
                        "synergy": "Shared achievement orientation",
                        "friction": "Potential empathy gap"
                    },
                    "people_champion": {
                        "compatibility": 0.91,
                        "synergy": "Aligned values, excellent teamwork",
                        "friction": "Minimal - both may avoid tough decisions"
                    },
                    "strategic_influencer": {
                        "compatibility": 0.85,
                        "synergy": "They provide influence skills, you provide empathy",
                        "friction": "Different approaches to persuasion"
                    }
                }
            },

            "stress_response_eq": {
                "under_pressure": "Maintains emotional control, supports others",
                "coping_mechanisms": ["Problem-solving", "Seeking support", "Optimistic reframing"],
                "resilience_score": 0.83,
                "team_impact_during_stress": "Stabilizing force, provides emotional support",
            },

            "career_recommendations": {
                "best_fit_roles": [
                    "Head of Customer Success - High empathy + service orientation",
                    "VP of People/HR - Developing others + teamwork",
                    "Startup COO - Achievement + collaboration + reliability",
                    "Partnership Lead - Relationship management + influence",
                    "Team Lead/Manager - Leadership + empathy + team building"
                ],
                "roles_to_avoid": [
                    "Cutthroat sales (low empathy required)",
                    "Rapid-pivot startup CEO (requires extreme adaptability)",
                    "Crisis management (unless adaptability improves)"
                ],
                "development_priorities": [
                    "Build comfort with ambiguity and rapid change",
                    "Strengthen influence and persuasion skills",
                    "Practice leading transformational change"
                ]
            },

            "metadata": {
                "assessment_model": "Goleman EQ 2.0",
                "confidence_score": 0.90,
                "assessment_basis": "Communication analysis, behavioral patterns, interaction history",
                "last_updated": "2025-01-16",
            }
        }

        return Result(
            success=True,
            data=eq_analysis,
            quality_score=0.90,
            metadata={
                "agent_id": self.agent_id,
                "analysis_type": "emotional_intelligence",
                "processing_time_ms": 312,
                "model_version": "eq_v2.0",
            }
        )

    async def assess_eq_compatibility(self, profile1_eq: Dict, profile2_eq: Dict) -> Dict:
        """Assess EQ-based compatibility between two profiles."""
        # Weighted compatibility calculation
        weights = {
            "empathy": 0.25,
            "teamwork": 0.20,
            "conflict_management": 0.20,
            "adaptability": 0.15,
            "emotional_control": 0.20,
        }

        # Calculate compatibility score (simplified)
        compatibility = sum(
            weights.get(comp, 0.1) * min(
                profile1_eq.get(comp, 0.5),
                profile2_eq.get(comp, 0.5)
            )
            for comp in weights.keys()
        )

        return {
            "compatibility_score": compatibility,
            "synergies": ["High empathy match", "Complementary strengths"],
            "friction_points": ["Different adaptability levels"],
        }


def create_eq_agent(agent_id: str = "eq_analyst_1") -> EmotionalIntelligenceAgent:
    """Factory function to create an EmotionalIntelligenceAgent."""
    return EmotionalIntelligenceAgent(agent_id)


if __name__ == "__main__":
    # Demo usage
    import asyncio

    async def demo():
        agent = create_eq_agent()

        task = Task(
            task_id="eq_001",
            description="Assess emotional intelligence for leadership role",
            required_capabilities=["eq_assessment", "leadership_eq"],
            priority=1
        )

        result = await agent.process_task(task)

        print(f"\n{'='*70}")
        print(f"Emotional Intelligence Assessment Results")
        print(f"{'='*70}\n")
        print(f"Overall EQ Score: {result.data['overall_eq_profile']['eq_score']:.0%} (Percentile: {result.data['overall_eq_profile']['percentile']})")
        print(f"Level: {result.data['overall_eq_profile']['level']}")
        print(f"\nDomain Scores:")
        print(f"  1. Self-Awareness:          {result.data['domain_1_self_awareness']['overall_score']:.0%}")
        print(f"  2. Self-Management:         {result.data['domain_2_self_management']['overall_score']:.0%}")
        print(f"  3. Social Awareness:        {result.data['domain_3_social_awareness']['overall_score']:.0%}")
        print(f"  4. Relationship Management: {result.data['domain_4_relationship_management']['overall_score']:.0%}")

        print(f"\nTop EQ Strengths:")
        for strength in result.data['eq_strengths'][:3]:
            print(f"  - {strength['competency']}: {strength['score']:.0%} - {strength['impact']}")

        print(f"\nLeadership Potential: {result.data['leadership_potential']['level']}")
        print(f"Leadership Style: {result.data['leadership_potential']['leadership_style']}")
        print(f"\n{'='*70}\n")

    asyncio.run(demo())
