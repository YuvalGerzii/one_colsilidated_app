"""
Motivation Profile Agent for Bond.AI

Analyzes what drives individuals - intrinsic motivators (autonomy, mastery, purpose),
extrinsic motivators (money, status, recognition), values hierarchy, and career
stage motivations.

Based on Self-Determination Theory (Deci & Ryan) and motivational psychology research.

Key Features:
- Intrinsic motivation assessment
- Extrinsic motivation analysis
- Values hierarchy mapping
- Career stage motivation profiling
- Goal alignment scoring
- Motivation archetype classification
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from typing import Any, Dict, List, Optional
from loguru import logger

from multi_agent_system.agents.base import BaseAgent
from multi_agent_system.core.types import Task, Result, AgentCapability


class MotivationProfileAgent(BaseAgent):
    """
    Advanced agent specialized in motivation analysis and matching.

    Analyzes what drives individuals to optimize partnerships based on
    aligned motivations and complementary goals.

    Capabilities:
    - Intrinsic motivation assessment
    - Extrinsic motivation analysis
    - Values hierarchy profiling
    - Career motivation mapping
    - Goal alignment scoring
    - Motivation compatibility matching
    """

    def __init__(self, agent_id: str = "motivation_profile_1", message_bus=None):
        capabilities = [
            AgentCapability("intrinsic_motivation", "Assess intrinsic motivators", 0.89),
            AgentCapability("extrinsic_motivation", "Assess extrinsic motivators", 0.87),
            AgentCapability("values_hierarchy", "Map values hierarchy", 0.90),
            AgentCapability("career_stage", "Profile career stage motivations", 0.86),
            AgentCapability("goal_alignment", "Score goal alignment", 0.88),
            AgentCapability("motivation_compatibility", "Match motivation profiles", 0.85),
        ]
        super().__init__(agent_id, capabilities, message_bus)

    async def process_task(self, task: Task) -> Result:
        """
        Process a motivation profile analysis task.

        Args:
            task: Motivation analysis task to process

        Returns:
            Comprehensive motivation profile analysis results
        """
        logger.info(f"{self.agent_id} analyzing motivation profile: {task.description}")

        # Simulate comprehensive motivation analysis
        motivation_analysis = {
            "task": task.description,

            "motivation_profile_summary": {
                "archetype": "Impact-Driven Builder",
                "description": "Motivated by creating meaningful impact through entrepreneurship",
                "primary_motivators": ["Purpose", "Autonomy", "Mastery"],
                "secondary_motivators": ["Financial Security", "Recognition"],
                "motivational_balance": "Intrinsic-dominant with practical extrinsic goals"
            },

            "intrinsic_motivation": {
                "overall_score": 0.84,  # 0-1 scale
                "level": "Very High",

                "dimensions": {
                    "autonomy": {
                        "score": 0.91,
                        "description": "Strong desire for independence and self-direction",
                        "manifestations": [
                            "Prefers setting own goals and strategies",
                            "Values freedom in how work is done",
                            "Uncomfortable with micromanagement",
                            "Entrepreneurial mindset"
                        ],
                        "career_implications": "Best in founder, leadership, or autonomous roles"
                    },
                    "mastery": {
                        "score": 0.87,
                        "description": "Driven to continuously improve and develop expertise",
                        "manifestations": [
                            "Invests heavily in learning and skill development",
                            "Seeks challenging problems",
                            "Values becoming world-class at craft",
                            "Growth mindset orientation"
                        ],
                        "career_implications": "Needs intellectually stimulating work"
                    },
                    "purpose": {
                        "score": 0.89,
                        "description": "Motivated by meaningful impact and contribution",
                        "manifestations": [
                            "Wants work to matter beyond profits",
                            "Driven by mission and vision",
                            "Values positive societal impact",
                            "Purpose before prestige"
                        ],
                        "career_implications": "Mission-driven companies, social impact work"
                    },
                    "curiosity": {
                        "score": 0.82,
                        "description": "Intrinsic interest in learning and discovery",
                        "manifestations": [
                            "Enjoys exploring new ideas and domains",
                            "Asks deep questions",
                            "Reads broadly across fields",
                            "Experimental mindset"
                        ],
                        "career_implications": "Research, innovation, cross-domain work"
                    },
                    "creativity": {
                        "score": 0.76,
                        "description": "Motivated by creating and building new things",
                        "manifestations": [
                            "Energized by creative problem-solving",
                            "Enjoys building from scratch",
                            "Values original thinking",
                            "Innovation-oriented"
                        ],
                        "career_implications": "Startup founding, product creation, R&D"
                    }
                }
            },

            "extrinsic_motivation": {
                "overall_score": 0.62,  # 0-1 scale
                "level": "Moderate",
                "note": "Present but secondary to intrinsic motivators",

                "dimensions": {
                    "financial_rewards": {
                        "score": 0.68,
                        "description": "Money matters for security and freedom, not primary driver",
                        "manifestations": [
                            "Values financial security and stability",
                            "Sees money as enabler of autonomy",
                            "Not purely profit-driven",
                            "Willing to sacrifice for mission"
                        ],
                        "threshold": "Needs $X for security, then diminishing returns"
                    },
                    "status_prestige": {
                        "score": 0.54,
                        "description": "Moderate interest in status and titles",
                        "manifestations": [
                            "Values respect but not titles for their own sake",
                            "Reputation matters in professional circles",
                            "Not driven by prestige alone",
                            "Substance over appearances"
                        ],
                        "professional_impact": "Modest motivation from status"
                    },
                    "recognition": {
                        "score": 0.71,
                        "description": "Appreciates recognition for good work",
                        "manifestations": [
                            "Values acknowledgment of contributions",
                            "Enjoys peer recognition",
                            "Not seeking spotlight constantly",
                            "Recognition validates impact"
                        ],
                        "professional_impact": "Positive reinforcement important"
                    },
                    "competition": {
                        "score": 0.58,
                        "description": "Moderately competitive, more focused on personal excellence",
                        "manifestations": [
                            "Competes with self more than others",
                            "Enjoys friendly competition",
                            "Not zero-sum mentality",
                            "Collaborative over cutthroat"
                        ],
                        "professional_impact": "Drives performance but not primary motivator"
                    },
                    "security": {
                        "score": 0.61,
                        "description": "Values stability but willing to take calculated risks",
                        "manifestations": [
                            "Wants baseline security",
                            "Comfortable with entrepreneurial risk",
                            "Not risk-averse",
                            "Balances security and opportunity"
                        ],
                        "professional_impact": "Entrepreneurial with safety nets"
                    },
                    "power_influence": {
                        "score": 0.49,
                        "description": "Low power motivation, prefers influence through ideas",
                        "manifestations": [
                            "Not seeking power for its own sake",
                            "Influences through expertise and ideas",
                            "Collaborative leadership style",
                            "Impact over control"
                        ],
                        "professional_impact": "Leadership through expertise, not authority"
                    }
                }
            },

            "values_hierarchy": {
                "description": "What matters most, in priority order",

                "top_values": [
                    {
                        "rank": 1,
                        "value": "Impact & Purpose",
                        "score": 0.94,
                        "description": "Making meaningful difference in the world",
                        "tradeoffs": "Would sacrifice compensation for impact"
                    },
                    {
                        "rank": 2,
                        "value": "Autonomy & Freedom",
                        "score": 0.91,
                        "description": "Independence and self-direction",
                        "tradeoffs": "Would leave high-paying job if not autonomous"
                    },
                    {
                        "rank": 3,
                        "value": "Growth & Learning",
                        "score": 0.87,
                        "description": "Continuous development and mastery",
                        "tradeoffs": "Invests significant time/money in learning"
                    },
                    {
                        "rank": 4,
                        "value": "Integrity & Authenticity",
                        "score": 0.84,
                        "description": "Being true to values and principles",
                        "tradeoffs": "Won't compromise ethics for profit"
                    },
                    {
                        "rank": 5,
                        "value": "Innovation & Creativity",
                        "score": 0.79,
                        "description": "Creating new solutions and ideas",
                        "tradeoffs": "Prefers novel challenges over routine"
                    },
                    {
                        "rank": 6,
                        "value": "Financial Security",
                        "score": 0.71,
                        "description": "Stability and economic freedom",
                        "tradeoffs": "Important but not primary driver"
                    },
                    {
                        "rank": 7,
                        "value": "Work-Life Balance",
                        "score": 0.68,
                        "description": "Time for personal life and relationships",
                        "tradeoffs": "Will work hard on meaningful work, needs boundaries"
                    },
                    {
                        "rank": 8,
                        "value": "Recognition & Status",
                        "score": 0.58,
                        "description": "Acknowledgment and respect",
                        "tradeoffs": "Nice to have, not essential"
                    }
                ],

                "value_conflicts": [
                    {
                        "conflict": "Autonomy vs. Collaboration",
                        "resolution": "Values autonomy within collaborative context",
                        "severity": "low"
                    },
                    {
                        "conflict": "Impact vs. Financial Returns",
                        "resolution": "Prioritizes impact with sustainable financial model",
                        "severity": "low-moderate"
                    }
                ]
            },

            "career_stage_motivations": {
                "current_career_stage": "Growth & Impact Stage",
                "years_in_career": 12,
                "typical_stage": "Mid-career professional / Early-stage entrepreneur",

                "stage_specific_motivations": {
                    "early_career": {
                        "relevance": 0.15,
                        "past_motivations": ["Learning", "Proving myself", "Building foundation"]
                    },
                    "growth_impact_stage": {
                        "relevance": 1.00,
                        "current_motivations": [
                            "Building something meaningful",
                            "Leveraging expertise for impact",
                            "Creating value and wealth",
                            "Establishing reputation",
                            "Growing team and organization"
                        ]
                    },
                    "legacy_stage": {
                        "relevance": 0.32,
                        "emerging_motivations": [
                            "Long-term impact thinking",
                            "Mentoring next generation",
                            "Building lasting institutions"
                        ]
                    }
                },

                "motivational_evolution": {
                    "past_5_years": "Shifted from pure learning to impact-driven building",
                    "next_5_years": "Likely to increase focus on legacy and scale of impact",
                    "trend": "Increasingly purpose-driven, less concerned with status"
                }
            },

            "goal_hierarchy": {
                "1_year_goals": {
                    "primary": "Scale startup to Series A",
                    "motivation_drivers": ["Autonomy", "Mastery", "Impact"],
                    "alignment_with_values": 0.93
                },
                "3_year_goals": {
                    "primary": "Build market-leading product with meaningful impact",
                    "motivation_drivers": ["Purpose", "Creativity", "Recognition"],
                    "alignment_with_values": 0.91
                },
                "10_year_goals": {
                    "primary": "Create lasting positive impact on industry/society",
                    "motivation_drivers": ["Purpose", "Legacy", "Autonomy"],
                    "alignment_with_values": 0.96
                },
                "lifetime_aspirations": {
                    "primary": "Leave world better than found it through innovation",
                    "motivation_drivers": ["Purpose", "Impact", "Creativity"],
                    "alignment_with_values": 0.98
                }
            },

            "motivation_compatibility_matching": {
                "ideal_partner_motivations": {
                    "co_founder": {
                        "essential_shared_motivations": [
                            "High purpose/impact orientation",
                            "High autonomy need",
                            "Growth mindset"
                        ],
                        "complementary_motivations": [
                            "Financial focus (to balance your mission focus)",
                            "Competitive drive (to push for wins)",
                            "Recognition seeking (to champion company)"
                        ],
                        "incompatible_motivations": [
                            "Pure profit maximization at any cost",
                            "Need for constant oversight/control",
                            "Status-only driven"
                        ]
                    },
                    "team_members": {
                        "cultural_fit_motivations": [
                            "Purpose-driven",
                            "Learning-oriented",
                            "Collaborative over competitive"
                        ],
                        "desired_diversity": [
                            "Mix of intrinsic/extrinsic motivations",
                            "Variety of value hierarchies",
                            "Different goal timelines"
                        ]
                    },
                    "investors": {
                        "alignment_needed": [
                            "Patient capital (long-term thinking)",
                            "Mission-aligned",
                            "Support for autonomy"
                        ],
                        "red_flags": [
                            "Purely financial return focus",
                            "Short-term profit pressure",
                            "Micromanagement style"
                        ]
                    }
                },

                "motivation_archetype_compatibility": {
                    "impact_driven_builder": {
                        "compatibility": 0.96,
                        "synergy": "Perfect alignment - same core motivations",
                        "partnership_strength": "Very High"
                    },
                    "wealth_maximizer": {
                        "compatibility": 0.48,
                        "friction": "Fundamental values mismatch",
                        "partnership_strength": "Low - requires clear boundaries"
                    },
                    "stability_seeker": {
                        "compatibility": 0.61,
                        "friction": "Risk tolerance mismatch",
                        "partnership_strength": "Moderate - complementary in some contexts"
                    },
                    "achievement_oriented": {
                        "compatibility": 0.79,
                        "synergy": "Shared drive, different focus (mastery vs achievement)",
                        "partnership_strength": "High"
                    },
                    "creative_explorer": {
                        "compatibility": 0.84,
                        "synergy": "Shared innovation and creativity values",
                        "partnership_strength": "High"
                    }
                }
            },

            "motivational_strengths_weaknesses": {
                "strengths": [
                    "Highly self-motivated - doesn't need external push",
                    "Purpose-driven - attracts aligned talent and partners",
                    "Growth-oriented - continuous improvement",
                    "Balanced - not purely idealistic or materialistic",
                    "Resilient - intrinsic motivation sustains through challenges"
                ],
                "potential_weaknesses": [
                    "May undervalue financial aspects",
                    "Could struggle in purely transactional environments",
                    "Might be too idealistic for some partnerships",
                    "Low power motivation may limit political navigation"
                ],
                "development_areas": [
                    "Strengthen financial/business acumen to match purpose",
                    "Develop comfort with some hierarchy/power dynamics",
                    "Balance idealism with pragmatism"
                ]
            },

            "career_recommendations": {
                "best_fit_roles": [
                    "Startup Founder - High autonomy, impact, mastery",
                    "Mission-Driven CEO - Purpose + leadership",
                    "Social Enterprise Leader - Impact + financial sustainability",
                    "Innovation Lead - Creativity + autonomy",
                    "Head of Impact/Purpose - Alignment with values"
                ],
                "roles_to_avoid": [
                    "Corporate middle management - Low autonomy, bureaucratic",
                    "Pure sales (commission only) - Extrinsic focus",
                    "High-control hierarchies - Conflicts with autonomy",
                    "Unethical industries - Values conflict"
                ],
                "company_culture_fit": {
                    "best_fit": [
                        "Mission-driven startups",
                        "B-corps and social enterprises",
                        "Innovative tech companies",
                        "Research institutions",
                        "Purpose-driven organizations"
                    ],
                    "poor_fit": [
                        "Highly bureaucratic organizations",
                        "Pure profit-maximization cultures",
                        "Unethical industries",
                        "Low-autonomy environments"
                    ]
                }
            },

            "metadata": {
                "assessment_model": "Self-Determination Theory + Motivational Hierarchy v2.0",
                "confidence_score": 0.89,
                "last_updated": "2025-01-16"
            }
        }

        return Result(
            success=True,
            data=motivation_analysis,
            quality_score=0.89,
            metadata={
                "agent_id": self.agent_id,
                "analysis_type": "motivation_profile",
                "processing_time_ms": 267,
                "model_version": "motivation_v2.0",
            }
        )


def create_motivation_profile_agent(agent_id: str = "motivation_profile_1") -> MotivationProfileAgent:
    """Factory function to create a MotivationProfileAgent."""
    return MotivationProfileAgent(agent_id)


if __name__ == "__main__":
    # Demo usage
    import asyncio

    async def demo():
        agent = create_motivation_profile_agent()

        task = Task(
            task_id="motivation_001",
            description="Analyze motivation profile for career and partnership alignment",
            required_capabilities=["intrinsic_motivation", "values_hierarchy"],
            priority=1
        )

        result = await agent.process_task(task)

        print(f"\n{'='*70}")
        print(f"Motivation Profile Analysis Results")
        print(f"{'='*70}\n")

        print(f"Motivation Archetype: {result.data['motivation_profile_summary']['archetype']}")
        print(f"Description: {result.data['motivation_profile_summary']['description']}\n")

        print(f"Intrinsic Motivation: {result.data['intrinsic_motivation']['level']} ({result.data['intrinsic_motivation']['overall_score']:.0%})")
        print(f"Extrinsic Motivation: {result.data['extrinsic_motivation']['level']} ({result.data['extrinsic_motivation']['overall_score']:.0%})\n")

        print(f"Top 3 Values:")
        for value in result.data['values_hierarchy']['top_values'][:3]:
            print(f"  {value['rank']}. {value['value']}: {value['score']:.0%}")

        print(f"\nCareer Stage: {result.data['career_stage_motivations']['current_career_stage']}")
        print(f"Primary Motivators: {', '.join(result.data['motivation_profile_summary']['primary_motivators'])}")

        print(f"\n{'='*70}\n")

    asyncio.run(demo())
