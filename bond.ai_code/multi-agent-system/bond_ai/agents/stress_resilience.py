"""
Stress Resilience Agent for Bond.AI

Analyzes how individuals handle pressure, stress response patterns, resilience
factors, coping mechanisms, and burnout risk to optimize partnerships and predict
crisis performance.

Key Features:
- Stress response pattern analysis
- Resilience factor assessment
- Coping mechanism profiling
- Burnout risk scoring
- Pressure performance prediction
- Crisis compatibility matching
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from typing import Any, Dict, List, Optional
from loguru import logger

from multi_agent_system.agents.base import BaseAgent
from multi_agent_system.core.types import Task, Result, AgentCapability


class StressResilienceAgent(BaseAgent):
    """
    Advanced agent specialized in stress resilience and coping analysis.

    Analyzes stress responses, resilience factors, and coping strategies
    to predict performance under pressure and optimize crisis partnerships.

    Capabilities:
    - Stress response pattern analysis
    - Resilience scoring
    - Coping mechanism assessment
    - Burnout risk evaluation
    - Pressure performance prediction
    - Crisis compatibility matching
    """

    def __init__(self, agent_id: str = "stress_resilience_1", message_bus=None):
        capabilities = [
            AgentCapability("stress_response", "Analyze stress response patterns", 0.88),
            AgentCapability("resilience_scoring", "Score resilience factors", 0.90),
            AgentCapability("coping_mechanisms", "Assess coping strategies", 0.87),
            AgentCapability("burnout_risk", "Evaluate burnout risk", 0.89),
            AgentCapability("pressure_performance", "Predict performance under pressure", 0.86),
            AgentCapability("crisis_compatibility", "Match crisis-compatible partners", 0.84),
        ]
        super().__init__(agent_id, capabilities, message_bus)

    async def process_task(self, task: Task) -> Result:
        """
        Process a stress resilience analysis task.

        Args:
            task: Stress resilience task to process

        Returns:
            Comprehensive stress resilience analysis results
        """
        logger.info(f"{self.agent_id} analyzing stress resilience: {task.description}")

        # Simulate comprehensive stress resilience analysis
        resilience_analysis = {
            "task": task.description,

            "resilience_profile_summary": {
                "archetype": "Resilient Performer",
                "overall_resilience_score": 0.83,  # 0-1 scale
                "level": "High",
                "description": "Handles stress well with strong coping mechanisms and recovery capacity",
                "key_strength": "Maintains performance under pressure",
                "development_area": "Work-life balance and prevention of burnout"
            },

            "stress_response_patterns": {
                "primary_response": "Challenge Response",  # Challenge, Threat, Flow, Freeze
                "description": "Views stress as opportunity for growth, activates performance mode",

                "response_types": {
                    "challenge_response": {
                        "frequency": 0.71,
                        "description": "Sees stress as challenge, rises to occasion",
                        "physiological": "Increased focus and energy",
                        "psychological": "Confidence, determination, engagement",
                        "performance_impact": "+18% in challenging situations"
                    },
                    "threat_response": {
                        "frequency": 0.18,
                        "description": "Occasional anxiety when stakes are very high",
                        "triggers": ["Public failure risk", "Team depending heavily"],
                        "management": "Uses preparation and support systems"
                    },
                    "flow_response": {
                        "frequency": 0.09,
                        "description": "Sometimes achieves flow state under optimal pressure",
                        "conditions": ["Meaningful work", "Clear goals", "Immediate feedback"]
                    },
                    "freeze_response": {
                        "frequency": 0.02,
                        "description": "Rare paralysis, usually in unfamiliar high-stakes situations",
                        "recovery_time": "Fast - typically minutes"
                    }
                },

                "stress_indicators": {
                    "early_warning_signs": [
                        "Reduced sleep quality",
                        "Shorter patience",
                        "Increased caffeine consumption",
                        "Less time for relationships"
                    ],
                    "threshold_before_impact": "High - can handle significant stress before performance degrades",
                    "recovery_needs": "Exercise, social connection, strategic breaks"
                }
            },

            "resilience_factors": {
                "overall_score": 0.83,
                "components": {
                    "grit_perseverance": {
                        "score": 0.89,
                        "description": "Exceptional perseverance and determination",
                        "evidence": [
                            "Completes difficult projects despite obstacles",
                            "Maintains focus on long-term goals",
                            "Doesn't quit when things get hard",
                            "Growth from failures"
                        ],
                        "impact": "Sustains effort through adversity"
                    },
                    "adaptability_flexibility": {
                        "score": 0.78,
                        "description": "Good adaptability, some preference for stability",
                        "evidence": [
                            "Adjusts plans when circumstances change",
                            "Handles unexpected challenges well",
                            "Moderate comfort with ambiguity",
                            "Pivots when necessary"
                        ],
                        "impact": "Navigates change effectively"
                    },
                    "optimism_mindset": {
                        "score": 0.81,
                        "description": "Realistic optimism - positive but not naive",
                        "evidence": [
                            "Expects positive outcomes",
                            "Sees failures as temporary",
                            "Focuses on solutions",
                            "Maintains hope during setbacks"
                        ],
                        "impact": "Sustains motivation and morale"
                    },
                    "emotional_regulation": {
                        "score": 0.84,
                        "description": "Strong ability to manage emotions",
                        "evidence": [
                            "Stays calm in crises",
                            "Processes emotions constructively",
                            "Doesn't lash out under stress",
                            "Recovers from setbacks quickly"
                        ],
                        "impact": "Makes good decisions under pressure"
                    },
                    "self_efficacy": {
                        "score": 0.87,
                        "description": "High confidence in ability to handle challenges",
                        "evidence": [
                            "Believes in capacity to succeed",
                            "Takes on difficult challenges",
                            "Not deterred by initial failures",
                            "Strong track record builds confidence"
                        ],
                        "impact": "Approaches challenges confidently"
                    },
                    "social_support": {
                        "score": 0.79,
                        "description": "Strong but could leverage more",
                        "evidence": [
                            "Has supportive relationships",
                            "Asks for help when needed",
                            "Provides support to others",
                            "Could build broader support network"
                        ],
                        "impact": "Buffer against stress, shared problem-solving"
                    },
                    "meaning_purpose": {
                        "score": 0.91,
                        "description": "Very strong sense of purpose",
                        "evidence": [
                            "Work has deep meaning",
                            "Connected to larger mission",
                            "Purpose sustains through difficulty",
                            "Values-driven"
                        ],
                        "impact": "Major resilience factor, sustains through hardship"
                    }
                }
            },

            "coping_mechanisms": {
                "overall_effectiveness": 0.82,
                "approach": "Predominantly problem-focused with healthy emotion-focused strategies",

                "problem_focused_coping": {
                    "score": 0.87,
                    "strategies": [
                        {
                            "strategy": "Active problem-solving",
                            "frequency": "very_high",
                            "effectiveness": 0.91,
                            "description": "Directly addresses stressors with solutions"
                        },
                        {
                            "strategy": "Planning and preparation",
                            "frequency": "high",
                            "effectiveness": 0.88,
                            "description": "Anticipates and prepares for challenges"
                        },
                        {
                            "strategy": "Seeking information",
                            "frequency": "high",
                            "effectiveness": 0.84,
                            "description": "Researches and gathers data to address issues"
                        },
                        {
                            "strategy": "Time management",
                            "frequency": "moderate",
                            "effectiveness": 0.76,
                            "description": "Prioritizes and manages time under pressure"
                        }
                    ]
                },

                "emotion_focused_coping": {
                    "score": 0.78,
                    "strategies": [
                        {
                            "strategy": "Exercise and physical activity",
                            "frequency": "high",
                            "effectiveness": 0.89,
                            "description": "Releases stress through physical exertion"
                        },
                        {
                            "strategy": "Social connection",
                            "frequency": "moderate",
                            "effectiveness": 0.81,
                            "description": "Processes stress with trusted friends/colleagues"
                        },
                        {
                            "strategy": "Mindfulness/meditation",
                            "frequency": "moderate",
                            "effectiveness": 0.73,
                            "description": "Occasional practice, could be more consistent"
                        },
                        {
                            "strategy": "Reframing perspective",
                            "frequency": "high",
                            "effectiveness": 0.84,
                            "description": "Reframes challenges as opportunities"
                        },
                        {
                            "strategy": "Strategic breaks",
                            "frequency": "moderate",
                            "effectiveness": 0.79,
                            "description": "Takes breaks to recharge, though could be more proactive"
                        }
                    ]
                },

                "avoidance_coping": {
                    "score": 0.21,  # Low avoidance is good
                    "note": "Minimal use of unhealthy avoidance strategies",
                    "strategies": [
                        {
                            "strategy": "Denial/avoidance",
                            "frequency": "low",
                            "note": "Rarely avoids problems"
                        },
                        {
                            "strategy": "Substance use",
                            "frequency": "very_low",
                            "note": "Moderate alcohol socially, no problematic use"
                        },
                        {
                            "strategy": "Procrastination",
                            "frequency": "low",
                            "note": "Occasional for unpleasant tasks, not chronic"
                        }
                    ]
                }
            },

            "burnout_risk_assessment": {
                "current_burnout_risk": 0.38,  # 0-1 scale, higher is worse
                "risk_level": "Moderate",
                "trend": "stable",

                "burnout_dimensions": {
                    "exhaustion": {
                        "score": 0.42,
                        "status": "Moderate",
                        "indicators": [
                            "Sometimes tired but manages energy",
                            "Occasional energy depletion",
                            "Good recovery with breaks"
                        ]
                    },
                    "cynicism": {
                        "score": 0.18,
                        "status": "Low",
                        "indicators": [
                            "Maintains positive attitude toward work",
                            "Still finds meaning and purpose",
                            "Engaged with mission"
                        ]
                    },
                    "inefficacy": {
                        "score": 0.14,
                        "status": "Very Low",
                        "indicators": [
                            "High self-efficacy",
                            "Confident in abilities",
                            "Achieves goals effectively"
                        ]
                    }
                },

                "protective_factors": [
                    "Strong sense of purpose (0.91)",
                    "Good emotional regulation (0.84)",
                    "Effective coping strategies (0.82)",
                    "Supportive relationships (0.79)",
                    "Meaningful work"
                ],

                "risk_factors": [
                    {
                        "factor": "High workload",
                        "severity": "moderate",
                        "mitigation": "Needs better delegation and boundaries"
                    },
                    {
                        "factor": "Work-life balance",
                        "severity": "moderate",
                        "mitigation": "Could improve boundaries and personal time"
                    },
                    {
                        "factor": "Perfectionism tendencies",
                        "severity": "low",
                        "mitigation": "Occasional over-commitment, generally manages well"
                    }
                ],

                "recommendations": [
                    "Proactively schedule recovery time",
                    "Delegate more to prevent overload",
                    "Strengthen work-life boundaries",
                    "Maintain regular exercise routine",
                    "Continue mindfulness practice more consistently"
                ]
            },

            "performance_under_pressure": {
                "pressure_performance_score": 0.84,
                "category": "Pressure Performer",
                "description": "Performs at or above baseline under pressure",

                "pressure_scenarios": {
                    "tight_deadlines": {
                        "performance_change": "+12%",
                        "description": "Focuses and accelerates under time pressure",
                        "optimal_pressure_level": "moderate-high"
                    },
                    "high_stakes_decisions": {
                        "performance_change": "+8%",
                        "description": "Maintains clarity and decisiveness",
                        "preparation_important": True
                    },
                    "public_presentations": {
                        "performance_change": "-3%",
                        "description": "Slight nervousness, but manages well",
                        "improves_with_practice": True
                    },
                    "crisis_management": {
                        "performance_change": "+15%",
                        "description": "Excels in crisis - stays calm, leads effectively",
                        "natural_strength": True
                    },
                    "conflict_situations": {
                        "performance_change": "+4%",
                        "description": "Handles conflict constructively",
                        "emotional_regulation_key": True
                    },
                    "resource_constraints": {
                        "performance_change": "+6%",
                        "description": "Creative problem-solving with limitations",
                        "entrepreneurial_advantage": True
                    }
                },

                "optimal_stress_zone": {
                    "description": "Yerkes-Dodson optimal arousal",
                    "current_typical_stress": 0.67,  # 0-1 scale
                    "optimal_stress_level": "0.6-0.75",
                    "assessment": "Operating near optimal zone"
                }
            },

            "crisis_response_profile": {
                "crisis_leadership_score": 0.86,
                "leadership_style_under_pressure": "Decisive Collaborator",

                "crisis_behaviors": {
                    "stays_calm": {
                        "score": 0.91,
                        "impact": "Stabilizes team, enables clear thinking"
                    },
                    "makes_decisions_quickly": {
                        "score": 0.82,
                        "impact": "Prevents paralysis, maintains momentum"
                    },
                    "communicates_clearly": {
                        "score": 0.84,
                        "impact": "Reduces confusion and anxiety"
                    },
                    "delegates_effectively": {
                        "score": 0.74,
                        "impact": "Distributes load, empowers team",
                        "development_area": True
                    },
                    "adapts_plans": {
                        "score": 0.78,
                        "impact": "Pivots when needed"
                    },
                    "maintains_team_morale": {
                        "score": 0.87,
                        "impact": "Keeps team motivated and hopeful"
                    }
                },

                "team_impact_during_crisis": "Stabilizing force - team looks to for leadership and reassurance"
            },

            "stress_compatibility_matching": {
                "ideal_partner_stress_profiles": {
                    "co_founder": {
                        "essential_traits": [
                            "High resilience (0.75+)",
                            "Complementary stress response (calm under pressure)",
                            "Effective coping mechanisms",
                            "Low burnout risk"
                        ],
                        "complementary_traits": [
                            "Different optimal stress levels (one thrives in chaos, one in stability)",
                            "Diverse coping strategies",
                            "Mutual support capability"
                        ],
                        "red_flags": [
                            "High burnout risk",
                            "Panic under pressure",
                            "Unhealthy coping (substance abuse, denial)",
                            "Conflict-avoidant in crises"
                        ]
                    },
                    "team_composition": {
                        "resilience_diversity": "Mix of high-resilience (60%) and moderate (40%)",
                        "stress_response_balance": "Some pressure performers + some stability seekers",
                        "coping_variety": "Diverse strategies for organizational resilience"
                    }
                },

                "partnership_scenarios": {
                    "startup_co_founder": {
                        "compatibility": 0.89,
                        "rationale": "High resilience essential for startup volatility",
                        "stress_alignment": "Both thrive under pressure"
                    },
                    "corporate_partner": {
                        "compatibility": 0.71,
                        "rationale": "May clash if partner prefers stability",
                        "risk": "Different comfort levels with ambiguity"
                    },
                    "crisis_consultant": {
                        "compatibility": 0.94,
                        "rationale": "Perfect fit - excels in crisis situations",
                        "natural_strength": "Crisis performance +15%"
                    }
                }
            },

            "recommendations": {
                "leverage_strengths": [
                    "Take on high-pressure, high-stakes projects",
                    "Lead during crises and turnarounds",
                    "Mentor others on resilience and stress management",
                    "Build ventures in volatile industries (good fit)"
                ],

                "manage_risks": [
                    "Proactively prevent burnout with boundaries",
                    "Schedule regular recovery periods",
                    "Delegate more to prevent overload",
                    "Monitor exhaustion dimension (moderate risk)",
                    "Improve work-life balance sustainability"
                ],

                "optimize_environment": [
                    "Seek high-challenge, high-growth environments",
                    "Partner with equally resilient individuals",
                    "Build supportive team culture",
                    "Maintain purpose-driven work (major protective factor)"
                ],

                "personal_development": [
                    "Strengthen delegation skills",
                    "Formalize mindfulness practice",
                    "Expand support network",
                    "Develop even stronger work-life boundaries"
                ]
            },

            "metadata": {
                "assessment_model": "Resilience & Stress Response v2.0",
                "confidence_score": 0.88,
                "frameworks_used": ["Resilience Scale", "Burnout Inventory", "Stress Response Model"],
                "last_updated": "2025-01-16"
            }
        }

        return Result(
            success=True,
            data=resilience_analysis,
            quality_score=0.88,
            metadata={
                "agent_id": self.agent_id,
                "analysis_type": "stress_resilience",
                "processing_time_ms": 291,
                "model_version": "resilience_v2.0",
            }
        )


def create_stress_resilience_agent(agent_id: str = "stress_resilience_1") -> StressResilienceAgent:
    """Factory function to create a StressResilienceAgent."""
    return StressResilienceAgent(agent_id)


if __name__ == "__main__":
    # Demo usage
    import asyncio

    async def demo():
        agent = create_stress_resilience_agent()

        task = Task(
            task_id="resilience_001",
            description="Analyze stress resilience and burnout risk for high-pressure role",
            required_capabilities=["resilience_scoring", "burnout_risk", "pressure_performance"],
            priority=1
        )

        result = await agent.process_task(task)

        print(f"\n{'='*70}")
        print(f"Stress Resilience Analysis Results")
        print(f"{'='*70}\n")

        print(f"Resilience Archetype: {result.data['resilience_profile_summary']['archetype']}")
        print(f"Overall Resilience: {result.data['resilience_profile_summary']['overall_resilience_score']:.0%} ({result.data['resilience_profile_summary']['level']})\n")

        print(f"Stress Response: {result.data['stress_response_patterns']['primary_response']}")
        print(f"Performance Under Pressure: {result.data['performance_under_pressure']['pressure_performance_score']:.0%}")
        print(f"Category: {result.data['performance_under_pressure']['category']}\n")

        print(f"Burnout Risk: {result.data['burnout_risk_assessment']['risk_level']} ({result.data['burnout_risk_assessment']['current_burnout_risk']:.0%})")
        print(f"Crisis Leadership Score: {result.data['crisis_response_profile']['crisis_leadership_score']:.0%}\n")

        print(f"Top Resilience Factors:")
        factors = result.data['resilience_factors']['components']
        sorted_factors = sorted(factors.items(), key=lambda x: x[1]['score'], reverse=True)[:3]
        for name, data in sorted_factors:
            print(f"  - {name.replace('_', ' ').title()}: {data['score']:.0%}")

        print(f"\n{'='*70}\n")

    asyncio.run(demo())
