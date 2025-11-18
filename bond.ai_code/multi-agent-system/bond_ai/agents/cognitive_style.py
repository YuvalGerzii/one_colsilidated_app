"""
Cognitive Style Agent for Bond.AI

Analyzes thinking patterns, problem-solving approaches, and cognitive preferences
to optimize team composition and predict collaboration success.

Based on cognitive psychology research including:
- Kirton's Adaption-Innovation theory
- Kolb's Learning Styles
- Herrmann Brain Dominance Instrument (HBDI)
- Dual Process Theory (System 1 vs System 2 thinking)

Key Features:
- Thinking style analysis (analytical vs. intuitive, linear vs. systems)
- Problem-solving approach profiling
- Learning style assessment
- Decision-making pattern analysis
- Cognitive diversity scoring for optimal teams
- Innovation index (incremental vs. disruptive)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from typing import Any, Dict, List, Optional
from loguru import logger

from multi_agent_system.agents.base import BaseAgent
from multi_agent_system.core.types import Task, Result, AgentCapability


class CognitiveStyleAgent(BaseAgent):
    """
    Advanced agent specialized in cognitive style analysis and matching.

    Analyzes how people think, learn, solve problems, and make decisions
    to optimize partnerships and team composition.

    Capabilities:
    - Thinking style assessment
    - Problem-solving approach analysis
    - Learning style identification
    - Decision-making pattern recognition
    - Cognitive diversity optimization
    - Innovation potential scoring
    - Complementary thinking partner matching
    """

    def __init__(self, agent_id: str = "cognitive_style_1", message_bus=None):
        capabilities = [
            AgentCapability("thinking_style", "Analyze thinking style patterns", 0.89),
            AgentCapability("problem_solving", "Profile problem-solving approaches", 0.91),
            AgentCapability("learning_style", "Assess learning preferences", 0.87),
            AgentCapability("decision_making", "Analyze decision-making patterns", 0.90),
            AgentCapability("cognitive_diversity", "Optimize cognitive team diversity", 0.88),
            AgentCapability("innovation_index", "Score innovation potential", 0.86),
            AgentCapability("complementary_matching", "Match complementary thinkers", 0.89),
        ]
        super().__init__(agent_id, capabilities, message_bus)

    async def process_task(self, task: Task) -> Result:
        """
        Process a cognitive style analysis task.

        Args:
            task: Cognitive analysis task to process

        Returns:
            Comprehensive cognitive style analysis results
        """
        logger.info(f"{self.agent_id} analyzing cognitive style: {task.description}")

        # Simulate comprehensive cognitive style analysis
        cognitive_analysis = {
            "task": task.description,

            "cognitive_profile_summary": {
                "archetype": "Strategic Systems Thinker",
                "description": "Combines analytical rigor with big-picture systems thinking",
                "cognitive_strengths": [
                    "Complex problem decomposition",
                    "Pattern recognition across domains",
                    "Strategic thinking",
                    "Data-driven decision making"
                ],
                "ideal_roles": [
                    "Strategy Consultant",
                    "Product Manager",
                    "Systems Architect",
                    "Startup CEO",
                    "Research Lead"
                ]
            },

            "thinking_style_dimensions": {
                "analytical_vs_intuitive": {
                    "score": 0.68,  # 0 = pure intuitive, 1 = pure analytical, 0.5 = balanced
                    "classification": "Analytical-leaning balanced",
                    "description": "Prefers data and logic but trusts intuition for complex decisions",
                    "characteristics": {
                        "analytical_traits": [
                            "Breaks down complex problems systematically",
                            "Values data and evidence",
                            "Prefers structured approaches",
                            "Logical reasoning"
                        ],
                        "intuitive_traits": [
                            "Can make gut-feel decisions when needed",
                            "Recognizes patterns quickly",
                            "Comfortable with some ambiguity",
                            "Creative problem-solving"
                        ]
                    },
                    "professional_application": "Excels in roles requiring both rigorous analysis and strategic intuition (e.g., product strategy, investment decisions)"
                },

                "detail_vs_big_picture": {
                    "score": 0.35,  # 0 = pure detail, 1 = pure big picture
                    "classification": "Detail-oriented with strategic awareness",
                    "description": "Focuses on details and execution while maintaining strategic context",
                    "characteristics": {
                        "detail_oriented_traits": [
                            "Thorough and meticulous",
                            "Catches errors and inconsistencies",
                            "Values precision and accuracy",
                            "Strong execution focus"
                        ],
                        "big_picture_traits": [
                            "Understands how details fit into strategy",
                            "Can zoom out when needed",
                            "Sees long-term implications",
                            "Strategic thinker"
                        ]
                    },
                    "professional_application": "Ideal for roles requiring operational excellence with strategic awareness (COO, VP Operations, Technical Lead)"
                },

                "linear_vs_systems": {
                    "score": 0.72,  # 0 = linear, 1 = systems
                    "classification": "Systems thinker",
                    "description": "Thinks in interconnected systems and feedback loops",
                    "characteristics": {
                        "linear_traits": [
                            "Step-by-step problem solving",
                            "Sequential thinking",
                            "Clear cause-effect understanding"
                        ],
                        "systems_traits": [
                            "Sees interconnections and feedback loops",
                            "Understands second-order effects",
                            "Holistic perspective",
                            "Identifies leverage points in complex systems",
                            "Anticipates unintended consequences"
                        ]
                    },
                    "professional_application": "Excellent for complex problem domains (systems design, business strategy, organizational design)"
                },

                "convergent_vs_divergent": {
                    "score": 0.58,  # 0 = convergent (one right answer), 1 = divergent (many possibilities)
                    "classification": "Balanced with slight divergent preference",
                    "description": "Can both generate creative options and converge on optimal solutions",
                    "characteristics": {
                        "convergent_traits": [
                            "Good at narrowing options",
                            "Decisive when needed",
                            "Finds optimal solutions"
                        ],
                        "divergent_traits": [
                            "Generates multiple creative solutions",
                            "Explores alternatives",
                            "Challenges assumptions",
                            "Open to unconventional approaches"
                        ]
                    },
                    "professional_application": "Valuable in innovation roles requiring both ideation and execution"
                },

                "concrete_vs_abstract": {
                    "score": 0.64,  # 0 = concrete, 1 = abstract
                    "classification": "Abstract-leaning balanced",
                    "description": "Comfortable with abstract concepts while staying grounded in reality",
                    "characteristics": {
                        "concrete_traits": [
                            "Values practical, tangible outcomes",
                            "Prefers specific examples",
                            "Action-oriented"
                        ],
                        "abstract_traits": [
                            "Comfortable with theoretical concepts",
                            "Enjoys conceptual discussions",
                            "Can think in frameworks and models",
                            "Philosophical tendencies"
                        ]
                    },
                    "professional_application": "Strong in strategic/conceptual roles with practical grounding (product strategy, consulting)"
                }
            },

            "problem_solving_approach": {
                "primary_style": "Systematic Explorer",
                "description": "Combines structured problem-solving with creative exploration",

                "methodology_preferences": {
                    "trial_and_error": {
                        "preference": 0.42,
                        "usage": "Used for rapid prototyping and experimentation"
                    },
                    "systematic_analysis": {
                        "preference": 0.87,
                        "usage": "Primary approach for complex problems"
                    },
                    "creative_brainstorming": {
                        "preference": 0.73,
                        "usage": "Used for ideation and breakthrough thinking"
                    },
                    "collaborative_problem_solving": {
                        "preference": 0.81,
                        "usage": "Leverages team diversity for better solutions"
                    },
                    "first_principles": {
                        "preference": 0.78,
                        "usage": "Breaks down complex problems to fundamental truths"
                    },
                    "analogical_reasoning": {
                        "preference": 0.69,
                        "usage": "Borrows solutions from other domains"
                    }
                },

                "problem_solving_process": [
                    "1. Define problem clearly and understand root causes",
                    "2. Research and gather relevant data",
                    "3. Break down into components (systems thinking)",
                    "4. Generate multiple solution approaches",
                    "5. Analyze trade-offs systematically",
                    "6. Test assumptions and validate solutions",
                    "7. Implement with monitoring and iteration"
                ],

                "strengths": [
                    "Excellent at complex problem decomposition",
                    "Balances rigor with creativity",
                    "Strong pattern recognition",
                    "Data-driven with strategic intuition"
                ],

                "challenges": [
                    "May over-analyze simple problems",
                    "Can get stuck in analysis paralysis",
                    "Sometimes needs to trust gut more quickly"
                ]
            },

            "learning_style": {
                "primary_style": "Reflective Theorist",
                "kolb_style": "Assimilating",  # Assimilating, Converging, Diverging, Accommodating
                "description": "Learns through theoretical understanding and reflective observation",

                "learning_preferences": {
                    "visual": {
                        "score": 0.81,
                        "description": "Learns well from diagrams, charts, frameworks, whiteboards"
                    },
                    "auditory": {
                        "score": 0.58,
                        "description": "Moderate preference for lectures, podcasts, discussions"
                    },
                    "reading_writing": {
                        "score": 0.89,
                        "description": "Strong preference for reading, writing, documentation"
                    },
                    "kinesthetic": {
                        "score": 0.52,
                        "description": "Moderate learning through doing and hands-on practice"
                    }
                },

                "learning_approach": {
                    "concrete_experience": 0.48,  # Learning by doing
                    "reflective_observation": 0.84,  # Learning by watching and reflecting
                    "abstract_conceptualization": 0.87,  # Learning through theories
                    "active_experimentation": 0.61,  # Learning through testing
                },

                "optimal_learning_conditions": [
                    "Well-structured content with clear frameworks",
                    "Time for reflection and processing",
                    "Visual models and diagrams",
                    "Written materials and documentation",
                    "Logical, coherent presentations",
                    "Opportunities to ask 'why'"
                ],

                "learning_challenges": [
                    "Purely hands-on without theory",
                    "Chaotic, unstructured environments",
                    "Pressure to act before understanding",
                    "Lack of time for reflection"
                ]
            },

            "decision_making_patterns": {
                "decision_style": "Analytical-Adaptive",
                "speed_vs_accuracy": {
                    "score": 0.38,  # 0 = slow/accurate, 1 = fast/approximate
                    "classification": "Deliberate and thorough",
                    "description": "Prefers to gather sufficient information before deciding",
                },

                "risk_tolerance": {
                    "score": 0.64,  # 0 = risk-averse, 1 = risk-seeking
                    "classification": "Calculated risk-taker",
                    "description": "Takes risks when data supports it, but not reckless",
                    "approach": "Evaluates expected value and downside protection"
                },

                "individual_vs_collaborative": {
                    "score": 0.59,  # 0 = individual, 1 = collaborative
                    "classification": "Collaborative with independent analysis",
                    "description": "Values input but makes own assessment",
                },

                "data_vs_intuition": {
                    "score": 0.72,  # 0 = pure intuition, 1 = pure data
                    "classification": "Data-driven with intuition checks",
                    "description": "Heavily relies on data but validates with intuition",
                },

                "decision_factors": {
                    "logic_and_analysis": 0.84,
                    "values_and_ethics": 0.78,
                    "cost_benefit": 0.81,
                    "stakeholder_impact": 0.73,
                    "gut_feeling": 0.47,
                    "precedent": 0.52,
                },

                "under_pressure": "Maintains analytical approach but accelerates, may cut corners on research",
                "with_incomplete_info": "Comfortable making decisions with 70-80% certainty, not perfectionist",
            },

            "innovation_profile": {
                "innovation_index": 0.73,  # 0-1 scale
                "innovation_type": "Adaptive Innovator",  # Kirton: Adaptive vs. Innovative
                "score_breakdown": {
                    "adaptor_score": 0.27,  # Improves existing systems
                    "innovator_score": 0.73,  # Creates new paradigms
                },

                "innovation_style": {
                    "incremental_improvement": {
                        "score": 0.64,
                        "description": "Good at continuous optimization",
                    },
                    "disruptive_innovation": {
                        "score": 0.73,
                        "description": "Capable of paradigm-shifting thinking",
                    },
                    "framework_creation": {
                        "score": 0.79,
                        "description": "Strong at building new conceptual models",
                    },
                    "cross_domain_application": {
                        "score": 0.76,
                        "description": "Borrows ideas across fields effectively",
                    }
                },

                "innovation_characteristics": [
                    "Challenges conventional wisdom",
                    "Asks 'what if' questions",
                    "Comfortable with novel approaches",
                    "Balances creativity with practicality",
                    "Sees opportunities where others see constraints"
                ],

                "best_innovation_environment": [
                    "Autonomy to explore new ideas",
                    "Access to diverse perspectives",
                    "Data and research resources",
                    "Time for deep thinking",
                    "Tolerance for calculated failure"
                ]
            },

            "cognitive_biases_awareness": {
                "self_awareness_score": 0.76,
                "common_biases": [
                    {
                        "bias": "Confirmation bias",
                        "susceptibility": "moderate",
                        "mitigation": "Actively seeks disconfirming evidence"
                    },
                    {
                        "bias": "Analysis paralysis",
                        "susceptibility": "high",
                        "mitigation": "Set decision deadlines, use 80/20 rule"
                    },
                    {
                        "bias": "Overconfidence in models",
                        "susceptibility": "moderate",
                        "mitigation": "Reality-test assumptions, seek feedback"
                    }
                ],
                "debiasing_practices": [
                    "Pre-mortem analysis",
                    "Devil's advocate thinking",
                    "Diverse perspectives consultation",
                    "Data triangulation"
                ]
            },

            "team_role_preferences": {
                "belbin_roles": {
                    "primary": "Specialist / Plant",
                    "secondary": "Monitor Evaluator",
                    "description": "Brings deep expertise and strategic analysis"
                },
                "preferred_contributions": [
                    "Strategic planning and analysis",
                    "Complex problem-solving",
                    "Framework and systems design",
                    "Quality assurance and critical thinking"
                ],
                "team_dynamics": {
                    "works_best_with": [
                        "Action-oriented implementers (Shapers, Implementers)",
                        "People-focused coordinators (Coordinators, Team Workers)",
                        "Creative divergent thinkers (Plants) for balance"
                    ],
                    "potential_friction_with": [
                        "Pure executors who avoid strategy",
                        "Highly impulsive decision-makers",
                        "Anti-intellectual culture"
                    ]
                }
            },

            "cognitive_compatibility_matching": {
                "description": "Cognitive pairing recommendations for optimal partnerships",

                "ideal_co_founder": {
                    "cognitive_profile": {
                        "analytical_vs_intuitive": "0.3-0.5 (more intuitive to balance)",
                        "detail_vs_big_picture": "0.6-0.8 (big picture vision)",
                        "innovation_style": "0.7+ (fellow innovator)",
                        "decision_speed": "0.6-0.8 (faster to complement deliberation)",
                    },
                    "reasoning": "Seek visionary, fast-deciding partner to balance your analytical depth. Both should be innovative.",
                    "example_pairing": "You (Strategic COO) + Visionary CEO"
                },

                "ideal_team_composition": {
                    "cognitive_diversity_score": 0.82,
                    "recommended_mix": {
                        "thinkers_like_you": "20-30%",
                        "action_oriented_executors": "30-40%",
                        "creative_divergent_thinkers": "20-30%",
                        "people_focused_coordinators": "10-20%"
                    },
                    "rationale": "Balance analytical depth with execution and creativity"
                },

                "complementary_partner_profiles": [
                    {
                        "archetype": "Visionary Entrepreneur",
                        "compatibility": 0.87,
                        "synergy": "Your analysis + their vision = powerful combination",
                        "roles": "You: COO/CPO, Them: CEO"
                    },
                    {
                        "archetype": "Execution Machine",
                        "compatibility": 0.81,
                        "synergy": "Your strategy + their execution = results",
                        "roles": "You: Head of Strategy, Them: Head of Operations"
                    },
                    {
                        "archetype": "Creative Innovator",
                        "compatibility": 0.78,
                        "synergy": "Your rigor + their creativity = innovation",
                        "roles": "Co-equal partners with divided domains"
                    }
                ],

                "challenging_pairings": [
                    {
                        "archetype": "Pure Tactician",
                        "compatibility": 0.43,
                        "friction": "Strategy vs. pure execution mindset gap",
                        "workaround": "Clear division of responsibilities"
                    },
                    {
                        "archetype": "Impulsive Executor",
                        "compatibility": 0.38,
                        "friction": "Decision-making speed and process mismatch",
                        "workaround": "Agree on decision framework upfront"
                    }
                ]
            },

            "professional_recommendations": {
                "leverage_your_cognitive_strengths": [
                    "Take on complex strategic problems",
                    "Design systems and frameworks",
                    "Lead analytical projects",
                    "Provide critical evaluation and QA",
                    "Bridge strategy and execution"
                ],

                "compensate_for_cognitive_gaps": [
                    "Partner with fast decision-makers",
                    "Set artificial deadlines to avoid analysis paralysis",
                    "Build in action bias (bias for execution)",
                    "Develop trust in intuition for time-sensitive decisions",
                    "Collaborate with visionaries for big-picture inspiration"
                ],

                "optimal_work_environment": [
                    "Intellectual challenge and complexity",
                    "Access to data and research",
                    "Time for deep thinking",
                    "Collaborative yet independent",
                    "Merit-based culture",
                    "Strategic impact opportunities"
                ],

                "roles_to_avoid": [
                    "Pure execution with no strategy (will be bored)",
                    "High-pressure snap decision roles (stressful)",
                    "Anti-intellectual environments",
                    "Purely tactical/operational (no systems thinking)"
                ]
            },

            "metadata": {
                "assessment_model": "Multi-dimensional cognitive analysis v2.0",
                "confidence_score": 0.89,
                "frameworks_used": ["Kirton KAI", "Kolb Learning Styles", "HBDI", "Belbin Team Roles"],
                "last_updated": "2025-01-16",
            }
        }

        return Result(
            success=True,
            data=cognitive_analysis,
            quality_score=0.89,
            metadata={
                "agent_id": self.agent_id,
                "analysis_type": "cognitive_style",
                "processing_time_ms": 289,
                "model_version": "cognitive_v2.0",
            }
        )


def create_cognitive_style_agent(agent_id: str = "cognitive_style_1") -> CognitiveStyleAgent:
    """Factory function to create a CognitiveStyleAgent."""
    return CognitiveStyleAgent(agent_id)


if __name__ == "__main__":
    # Demo usage
    import asyncio

    async def demo():
        agent = create_cognitive_style_agent()

        task = Task(
            task_id="cognitive_001",
            description="Analyze cognitive style for optimal team pairing",
            required_capabilities=["thinking_style", "cognitive_diversity"],
            priority=1
        )

        result = await agent.process_task(task)

        print(f"\n{'='*70}")
        print(f"Cognitive Style Analysis Results")
        print(f"{'='*70}\n")
        print(f"Cognitive Archetype: {result.data['cognitive_profile_summary']['archetype']}")
        print(f"Description: {result.data['cognitive_profile_summary']['description']}\n")

        print(f"Thinking Style Dimensions:")
        thinking = result.data['thinking_style_dimensions']
        print(f"  - Analytical vs. Intuitive: {thinking['analytical_vs_intuitive']['classification']}")
        print(f"  - Detail vs. Big Picture:   {thinking['detail_vs_big_picture']['classification']}")
        print(f"  - Linear vs. Systems:       {thinking['linear_vs_systems']['classification']}\n")

        print(f"Problem-Solving Style: {result.data['problem_solving_approach']['primary_style']}")
        print(f"Learning Style:        {result.data['learning_style']['primary_style']}")
        print(f"Innovation Type:       {result.data['innovation_profile']['innovation_type']}")
        print(f"Innovation Index:      {result.data['innovation_profile']['innovation_index']:.0%}\n")

        print(f"Ideal Co-Founder:")
        cofounder = result.data['cognitive_compatibility_matching']['ideal_co_founder']
        print(f"  {cofounder['reasoning']}")
        print(f"  Example: {cofounder['example_pairing']}")

        print(f"\n{'='*70}\n")

    asyncio.run(demo())
