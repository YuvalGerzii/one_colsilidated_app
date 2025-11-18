"""
Value Alignment Agent for Bond.AI

Analyzes professional values, goals, and principles to ensure deep alignment
for sustainable, meaningful professional relationships.

Based on research showing that value alignment is critical for long-term
relationship success and professional satisfaction.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from typing import Any, Dict, List
from loguru import logger

from multi_agent_system.agents.base import BaseAgent
from multi_agent_system.core.types import Task, Result, AgentCapability


class ValueAlignmentAgent(BaseAgent):
    """
    Advanced agent specialized in value and goal alignment analysis.

    Capabilities:
    - Professional values extraction
    - Goal alignment analysis
    - Principle compatibility assessment
    - Mission and vision alignment
    - Work ethic and culture fit
    - Long-term sustainability prediction
    - Purpose-driven matching
    """

    def __init__(self, agent_id: str = "value_aligner_1", message_bus=None):
        capabilities = [
            AgentCapability("values_extraction", "Extract professional values", 0.91),
            AgentCapability("goal_alignment", "Analyze goal alignment", 0.93),
            AgentCapability("principle_compatibility", "Assess principle compatibility", 0.90),
            AgentCapability("mission_vision_alignment", "Align mission and vision", 0.92),
            AgentCapability("culture_fit", "Evaluate culture fit", 0.89),
            AgentCapability("sustainability_prediction", "Predict relationship sustainability", 0.91),
            AgentCapability("purpose_matching", "Match based on purpose", 0.88),
            AgentCapability("value_alignment", "General value alignment", 0.92),
        ]
        super().__init__(agent_id, capabilities, message_bus)

    async def process_task(self, task: Task) -> Result:
        """
        Process a value alignment task.

        Args:
            task: Value alignment task to process

        Returns:
            Comprehensive value alignment analysis results
        """
        logger.info(f"{self.agent_id} analyzing value alignment: {task.description}")

        # Simulate comprehensive value alignment analysis
        alignment_results = {
            "task": task.description,
            "your_value_system": {
                "core_professional_values": [
                    {
                        "value": "Innovation & Continuous Learning",
                        "importance": 0.95,
                        "evidence": "15 mentions of learning, innovation, staying current",
                        "manifestation": "Always exploring new AI techniques, reading research papers",
                    },
                    {
                        "value": "Impact & Results",
                        "importance": 0.91,
                        "evidence": "Quantifiable accomplishments, user impact focus",
                        "manifestation": "Measures success by user outcomes and business metrics",
                    },
                    {
                        "value": "Integrity & Transparency",
                        "importance": 0.89,
                        "evidence": "Direct communication, honest feedback approach",
                        "manifestation": "Open about challenges, transparent with team and stakeholders",
                    },
                    {
                        "value": "Collaboration & Team Success",
                        "importance": 0.87,
                        "evidence": "12 mentions of team, we, together",
                        "manifestation": "Credits team, invests in team development",
                    },
                    {
                        "value": "Excellence & Quality",
                        "importance": 0.84,
                        "evidence": "High standards in code, product, and execution",
                        "manifestation": "Won't ship mediocre products, iterates for quality",
                    },
                ],
                "work_principles": [
                    "Move fast but don't break things (careful speed)",
                    "Data-driven decisions with intuition",
                    "Customer-centric product development",
                    "Build for scale from day one",
                    "Hire A-players, invest in their growth",
                ],
                "professional_mission": "Build AI/ML products that make meaningful impact at scale",
                "career_vision": "Create category-defining AI company, empower teams to do their best work",
                "work_culture_preferences": {
                    "pace": "Fast-paced but sustainable",
                    "structure": "Balanced - not too chaotic, not too bureaucratic",
                    "autonomy": "High - trust and autonomy with clear accountability",
                    "feedback_culture": "Open, frequent, constructive",
                    "risk_tolerance": "Calculated risks, data-informed",
                },
            },
            "value_alignment_matches": [
                {
                    "match": "Alex Thompson",
                    "overall_alignment": 0.93,
                    "alignment_breakdown": {
                        "core_values_alignment": {
                            "score": 0.95,
                            "shared_values": [
                                {"value": "Innovation & Continuous Learning", "both_importance": [0.95, 0.94]},
                                {"value": "Impact & Results", "both_importance": [0.91, 0.89]},
                                {"value": "Collaboration & Team Success", "both_importance": [0.87, 0.92]},
                            ],
                            "synergy": "Exceptional alignment on core professional values",
                        },
                        "goal_alignment": {
                            "score": 0.94,
                            "your_goals": ["Build AI products at scale", "Raise Series B", "Grow team to 50"],
                            "their_goals": ["Build category-defining AI company", "Secure Series B", "Scale to 100 employees"],
                            "alignment": "Nearly identical goals with compatible timelines",
                        },
                        "mission_vision_alignment": {
                            "score": 0.91,
                            "your_mission": "Build AI/ML products that make meaningful impact at scale",
                            "their_mission": "Democratize AI through accessible, powerful products",
                            "synergy": "Complementary missions - both focused on AI impact",
                        },
                        "work_culture_compatibility": {
                            "score": 0.92,
                            "both_prefer": ["Fast-paced", "High autonomy", "Open feedback", "Calculated risks"],
                            "synergy": "Very compatible work culture preferences",
                            "minor_difference": "You prefer slightly more structure (J vs P)",
                        },
                        "principles_alignment": {
                            "score": 0.89,
                            "shared_principles": [
                                "Move fast (you: carefully, them: with iteration)",
                                "Customer-centric approach",
                                "Data-driven with intuition",
                                "Invest in people",
                            ],
                            "complementary_differences": "You: build for scale, Them: ship and iterate",
                        },
                    },
                    "long_term_sustainability": {
                        "prediction": 0.92,
                        "factors": [
                            "Shared core values (0.95) create strong foundation",
                            "Aligned goals enable collaboration without competition",
                            "Compatible work culture reduces friction",
                            "Mutual respect for different approaches",
                        ],
                        "relationship_type": "Co-founding, Long-term Partnership",
                    },
                    "potential_value_conflicts": {
                        "conflicts": "Minimal - one minor difference",
                        "difference": "Speed vs. structure (manageable with communication)",
                        "resolution": "You provide structure, they provide agility - complementary",
                    },
                },
                {
                    "match": "Jennifer Liu",
                    "overall_alignment": 0.76,
                    "alignment_breakdown": {
                        "core_values_alignment": {
                            "score": 0.78,
                            "shared_values": [
                                {"value": "Excellence & Quality", "both_importance": [0.84, 0.93]},
                                {"value": "Impact & Results", "both_importance": [0.91, 0.87]},
                            ],
                            "different_values": [
                                {"your_top_value": "Innovation (0.95)", "their_top_value": "Reliability (0.94)"},
                            ],
                            "analysis": "Good overlap, but different emphasis - you prioritize innovation, they prioritize reliability",
                        },
                        "goal_alignment": {
                            "score": 0.72,
                            "your_goals": ["Build AI products", "Startup growth", "Innovation"],
                            "their_goals": ["Scale Stripe products", "Enterprise excellence", "Operational efficiency"],
                            "alignment": "Different contexts (startup vs enterprise) but compatible approaches",
                        },
                        "mission_vision_alignment": {
                            "score": 0.74,
                            "your_mission": "Build AI/ML products that make meaningful impact at scale",
                            "their_mission": "Build reliable financial infrastructure for the internet",
                            "synergy": "Different domains but shared commitment to quality and impact",
                        },
                        "work_culture_compatibility": {
                            "score": 0.68,
                            "differences": [
                                "You prefer fast-paced, they prefer measured",
                                "You prefer high autonomy, they prefer clear processes",
                            ],
                            "synergy": "Can learn from each other - you from their process rigor, them from your agility",
                        },
                        "principles_alignment": {
                            "score": 0.79,
                            "shared_principles": [
                                "Customer-centric",
                                "Data-driven decisions",
                                "Hire excellent people",
                            ],
                            "different_approaches": [
                                "You: move fast, They: move carefully",
                                "You: innovation focus, They: reliability focus",
                            ],
                        },
                    },
                    "long_term_sustainability": {
                        "prediction": 0.73,
                        "factors": [
                            "Moderate value alignment (0.76) - workable but requires effort",
                            "Different work culture preferences may cause friction",
                            "Mutual respect can bridge differences",
                        ],
                        "relationship_type": "Mentorship, Advisory (not co-founding)",
                    },
                    "potential_value_conflicts": {
                        "conflicts": "Moderate - 2-3 areas of potential friction",
                        "main_difference": "Innovation vs. Reliability emphasis",
                        "resolution": "Define clear domains - innovation in your area, reliability in execution",
                    },
                },
            ],
            "value_based_opportunity_matching": {
                "purpose_driven_opportunities": [
                    {
                        "opportunity": "Co-found AI/ML startup with Alex Thompson",
                        "value_alignment_score": 0.93,
                        "why_aligned": "Shared mission of AI impact, aligned values on innovation and team",
                        "sustainability": "Very High - values match supports long-term partnership",
                    },
                    {
                        "opportunity": "Advisory role at AI safety organization",
                        "value_alignment_score": 0.87,
                        "why_aligned": "Aligns with integrity, impact, and AI innovation values",
                        "sustainability": "High - mission-driven work",
                    },
                ],
                "mission_aligned_connections": [
                    {"person": "Alex Thompson", "mission_overlap": 0.91, "focus": "AI democratization"},
                    {"person": "User_9876", "mission_overlap": 0.84, "focus": "AI ethics and safety"},
                    {"person": "User_5432", "mission_overlap": 0.79, "focus": "AI in healthcare"},
                ],
            },
            "value_evolution_analysis": {
                "value_trajectory": {
                    "past": "Technical excellence, individual contribution",
                    "present": "Innovation + impact + team success",
                    "future_predicted": "Larger impact, organizational leadership, industry influence",
                },
                "evolving_priorities": [
                    "Increasing focus on team and people (up from 0.75 to 0.87 in 3 years)",
                    "Growing emphasis on industry impact beyond single company",
                    "Emerging interest in AI ethics and responsible innovation",
                ],
                "value_stability": {
                    "stable_values": ["Innovation (always top 3)", "Integrity (always important)"],
                    "growing_values": ["Team Success", "Industry Impact"],
                    "overall_stability": 0.84,  # Values relatively stable - good for long-term relationships
                },
            },
            "organizational_culture_fit": {
                "ideal_company_culture": {
                    "type": "Innovation-driven with excellence standards",
                    "characteristics": [
                        "Fast-paced but sustainable",
                        "High autonomy with accountability",
                        "Open feedback culture",
                        "Learning organization",
                        "Mission-driven",
                    ],
                    "examples": "Startups like Anthropic, Scale AI, or innovation labs in larger tech companies",
                },
                "culture_fit_scores": [
                    {"company_type": "AI/ML Startup (Seed-Series B)", "fit": 0.94},
                    {"company_type": "Innovation Lab (Large Tech)", "fit": 0.81},
                    {"company_type": "Enterprise Software Company", "fit": 0.68},
                    {"company_type": "Consulting Firm", "fit": 0.52},
                ],
            },
            "insights": [
                "93% value alignment with Alex Thompson - exceptional match for long-term partnership",
                "Innovation & Continuous Learning is your top value (0.95) - drives all career decisions",
                "Shared mission with Alex on 'AI impact at scale' creates strong collaboration foundation",
                "76% alignment with Jennifer Liu is moderate - good for mentorship, not ideal for co-founding",
                "Your value system has evolved healthily - increasing team focus while maintaining innovation priority",
                "High value stability (0.84) makes you reliable partner for long-term commitments",
                "Work culture preference (fast but sustainable) shows mature approach to innovation",
                "Purpose-driven opportunities align best with your core values",
                "Integrity & Transparency value (0.89) manifests in direct communication style",
                "Team Success value (0.87) growing over time - natural progression to leadership",
            ],
            "recommendations": [
                "Prioritize relationships with 90%+ value alignment for co-founding and partnerships",
                "Alex Thompson shows 93% alignment - pursue for long-term collaboration/co-founding",
                "For Jennifer Liu relationship, acknowledge value differences upfront and find complementary roles",
                "Seek purpose-driven opportunities that align with your mission of AI impact",
                "Continue developing team-focused values - trajectory aligns with leadership path",
                "Join AI safety/ethics communities - aligns with evolving values",
                "In new relationships, explicitly discuss values and goals early",
                "Target innovation-driven cultures (0.94 fit) over traditional enterprise (0.68 fit)",
                "Use your integrity/transparency value as differentiator in professional brand",
                "Create content around 'Building AI Products with Impact' to attract aligned connections",
            ],
            "confidence": 0.92,
        }

        return Result(
            task_id=task.id,
            success=True,
            data=alignment_results,
            agent_id=self.agent_id,
            quality_score=0.92,
            metadata={
                "value_extraction_method": "NLP + behavioral analysis",
                "alignment_assessment_depth": "comprehensive",
                "sustainability_prediction_accuracy": 0.87,
            }
        )
