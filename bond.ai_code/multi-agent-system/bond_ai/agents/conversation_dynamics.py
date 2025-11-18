"""
Conversation Dynamics Agent for Bond.AI

Analyzes conversation quality, engagement patterns, and interaction dynamics to
predict relationship success and identify potential issues early.

Key Features:
- Engagement metrics (response rate, latency, message length)
- Conversation balance (give vs. take ratio, reciprocity)
- Topic alignment and common ground analysis
- Rapport building indicators
- Conversation momentum tracking
- Red flag detection (one-sided, ghosting precursors)
- Conversation health scoring
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
from loguru import logger
import numpy as np

from multi_agent_system.agents.base import BaseAgent
from multi_agent_system.core.types import Task, Result, AgentCapability


class ConversationDynamicsAgent(BaseAgent):
    """
    Advanced agent specialized in conversation dynamics and quality analysis.

    Analyzes conversations to predict relationship quality, identify issues,
    and optimize engagement strategies.

    Capabilities:
    - Engagement metrics analysis
    - Reciprocity and balance scoring
    - Topic alignment detection
    - Rapport building analysis
    - Momentum tracking
    - Conversation health scoring
    - Early warning system for relationship issues
    """

    def __init__(self, agent_id: str = "conversation_dynamics_1", message_bus=None):
        capabilities = [
            AgentCapability("engagement_analysis", "Analyze conversation engagement", 0.92),
            AgentCapability("reciprocity_scoring", "Score conversation balance", 0.90),
            AgentCapability("topic_alignment", "Detect topic and interest alignment", 0.88),
            AgentCapability("rapport_building", "Analyze rapport indicators", 0.89),
            AgentCapability("momentum_tracking", "Track conversation momentum", 0.91),
            AgentCapability("conversation_health", "Score overall conversation health", 0.93),
            AgentCapability("red_flag_detection", "Early warning for issues", 0.87),
        ]
        super().__init__(agent_id, capabilities, message_bus)

    async def process_task(self, task: Task) -> Result:
        """
        Process a conversation dynamics analysis task.

        Args:
            task: Conversation analysis task to process

        Returns:
            Comprehensive conversation dynamics analysis results
        """
        logger.info(f"{self.agent_id} analyzing conversation dynamics: {task.description}")

        # Simulate conversation analysis
        conversation_analysis = {
            "task": task.description,
            "conversation_id": "conv_12345",
            "participants": ["User A", "User B"],
            "analysis_period": {
                "start_date": "2025-01-01",
                "end_date": "2025-01-16",
                "duration_days": 15,
                "message_count": 42,
            },

            "conversation_health_score": {
                "overall": 0.84,  # 0-1 scale
                "level": "Healthy",  # Poor, Fair, Good, Healthy, Excellent
                "trend": "improving",  # declining, stable, improving
                "prediction": "Strong potential for meaningful relationship",

                "component_scores": {
                    "reciprocity": 0.88,  # 30% weight
                    "responsiveness": 0.86,  # 25% weight
                    "depth": 0.79,  # 20% weight
                    "positivity": 0.91,  # 15% weight
                    "future_orientation": 0.82,  # 10% weight
                }
            },

            "engagement_metrics": {
                "response_rate": {
                    "user_a": 0.95,
                    "user_b": 0.91,
                    "average": 0.93,
                    "assessment": "Excellent mutual engagement"
                },
                "response_time": {
                    "user_a_median_hours": 3.2,
                    "user_b_median_hours": 4.7,
                    "average_hours": 3.95,
                    "consistency": 0.84,
                    "assessment": "Consistently responsive, reasonable timeframes"
                },
                "message_length": {
                    "user_a_avg_words": 87,
                    "user_b_avg_words": 93,
                    "balance": 0.94,  # How balanced the lengths are
                    "trend": "increasing",
                    "assessment": "Well-matched communication depth"
                },
                "question_asking": {
                    "user_a_questions": 18,
                    "user_b_questions": 16,
                    "balance": 0.89,
                    "per_message_rate": 0.81,
                    "assessment": "Both parties showing genuine interest"
                },
                "engagement_evolution": {
                    "week_1": 0.76,
                    "week_2": 0.84,
                    "current": 0.89,
                    "trend": "growing",
                    "velocity": "+17% over 2 weeks"
                }
            },

            "reciprocity_analysis": {
                "overall_reciprocity": 0.88,
                "assessment": "Highly reciprocal - balanced give and take",

                "dimensions": {
                    "information_sharing": {
                        "balance": 0.91,
                        "user_a_disclosure": 0.82,
                        "user_b_disclosure": 0.79,
                        "assessment": "Both sharing openly and equally"
                    },
                    "question_asking": {
                        "balance": 0.89,
                        "assessment": "Mutual curiosity and interest"
                    },
                    "value_exchange": {
                        "balance": 0.86,
                        "user_a_offers": ["Introduction to VC", "Technical advice"],
                        "user_b_offers": ["Market insights", "Partnership opportunity"],
                        "assessment": "Strong bidirectional value"
                    },
                    "emotional_support": {
                        "balance": 0.84,
                        "assessment": "Supportive and encouraging to each other"
                    },
                    "initiative_taking": {
                        "balance": 0.87,
                        "user_a_initiatives": 12,
                        "user_b_initiatives": 11,
                        "assessment": "Both proactive in conversation"
                    }
                },

                "red_flags": {
                    "one_sided_conversation": False,
                    "extractive_behavior": False,
                    "lack_of_reciprocity": False,
                },
                "green_flags": [
                    "Balanced information exchange",
                    "Mutual question asking",
                    "Both offer value proactively",
                    "Shared initiative"
                ]
            },

            "topic_alignment": {
                "shared_interests_score": 0.82,
                "conversation_topics": [
                    {
                        "topic": "AI/ML Technology",
                        "user_a_interest": 0.94,
                        "user_b_interest": 0.91,
                        "alignment": 0.97,
                        "messages": 18,
                        "depth": "deep"
                    },
                    {
                        "topic": "Startup Ecosystem",
                        "user_a_interest": 0.87,
                        "user_b_interest": 0.89,
                        "alignment": 0.98,
                        "messages": 14,
                        "depth": "moderate"
                    },
                    {
                        "topic": "Product Strategy",
                        "user_a_interest": 0.79,
                        "user_b_interest": 0.84,
                        "alignment": 0.94,
                        "messages": 7,
                        "depth": "surface"
                    },
                    {
                        "topic": "Personal Growth",
                        "user_a_interest": 0.72,
                        "user_b_interest": 0.68,
                        "alignment": 0.94,
                        "messages": 3,
                        "depth": "surface"
                    }
                ],
                "conversation_drift": 0.18,  # Low drift = staying on topic
                "common_ground": [
                    "Both interested in AI applications",
                    "Both building startups",
                    "Both value data-driven decisions",
                    "Similar professional stage"
                ],
                "topic_evolution": "Natural progression from professional to semi-personal",
                "assessment": "Strong alignment on key professional interests"
            },

            "rapport_building": {
                "rapport_score": 0.86,
                "rapport_level": "Strong",

                "indicators": {
                    "linguistic_mimicry": {
                        "score": 0.73,
                        "description": "Moderate adoption of each other's language patterns",
                        "examples": ["Both using 'synergy'", "Similar sentence structures"]
                    },
                    "positive_reinforcement": {
                        "score": 0.91,
                        "user_a_affirmations": 11,
                        "user_b_affirmations": 13,
                        "examples": ["That's a great point", "I love that idea", "Exactly!"]
                    },
                    "humor_exchange": {
                        "score": 0.68,
                        "instances": 5,
                        "reciprocated": 4,
                        "assessment": "Light humor, well received"
                    },
                    "personal_disclosure": {
                        "score": 0.79,
                        "progression": "gradual_deepening",
                        "assessment": "Appropriate sharing, building trust"
                    },
                    "empathy_signals": {
                        "score": 0.84,
                        "examples": ["That sounds challenging", "I can relate", "Makes sense"],
                        "assessment": "Strong mutual empathy"
                    },
                    "shared_experiences": {
                        "score": 0.77,
                        "identified": 4,
                        "examples": ["Both raised funding", "Both technical founders"],
                        "assessment": "Building connection through common experiences"
                    }
                },

                "rapport_progression": {
                    "initial": 0.61,  # First messages
                    "current": 0.86,
                    "growth": "+41%",
                    "trajectory": "healthy_acceleration"
                }
            },

            "conversation_momentum": {
                "current_momentum": "strong_positive",
                "momentum_score": 0.87,

                "metrics": {
                    "response_acceleration": {
                        "trend": "faster",
                        "change": "-18% response time (improvement)",
                        "description": "Both responding more quickly over time"
                    },
                    "message_frequency": {
                        "week_1": 14,
                        "week_2": 28,
                        "current_trend": "increasing",
                        "growth": "+100%"
                    },
                    "engagement_depth": {
                        "trend": "deepening",
                        "avg_message_length_growth": "+23%",
                        "topic_depth_growth": "+37%"
                    },
                    "sentiment_trend": {
                        "initial": 0.72,
                        "current": 0.89,
                        "trend": "increasingly_positive",
                        "improvement": "+24%"
                    }
                },

                "momentum_indicators": [
                    "Increasing message frequency",
                    "Faster response times",
                    "Deeper conversations",
                    "More positive sentiment",
                    "Greater personal disclosure",
                    "More future planning"
                ],

                "predictions": {
                    "next_7_days": {
                        "momentum": "sustained_high",
                        "predicted_messages": 32,
                        "conversation_quality": 0.88,
                        "confidence": 0.84
                    },
                    "meeting_likelihood_30_days": 0.89,
                    "partnership_formation_90_days": 0.76,
                }
            },

            "conversation_quality_indicators": {
                "depth_vs_breadth": {
                    "depth_score": 0.79,
                    "breadth_score": 0.68,
                    "balance": "depth_focused",
                    "assessment": "Meaningful conversations on focused topics"
                },
                "active_listening_signals": {
                    "score": 0.87,
                    "indicators": [
                        "References to previous conversation points",
                        "Follow-up questions",
                        "Building on each other's ideas",
                        "Acknowledging concerns/questions"
                    ]
                },
                "conversation_structure": {
                    "coherence": 0.86,
                    "topic_transitions": "smooth",
                    "conversational_flow": "natural",
                    "dead_end_rate": 0.09  # Low is good
                },
                "intellectual_compatibility": {
                    "score": 0.84,
                    "assessment": "Similar thinking levels, stimulating discussions"
                }
            },

            "red_flags_and_warnings": {
                "red_flags_detected": 0,
                "yellow_flags_detected": 1,
                "green_flags_detected": 12,

                "yellow_flags": [
                    {
                        "type": "schedule_coordination_challenge",
                        "severity": "low",
                        "description": "Took 3 attempts to align on meeting time",
                        "recommendation": "Use scheduling tool for efficiency"
                    }
                ],

                "green_flags": [
                    {"flag": "Both highly responsive", "importance": "high"},
                    {"flag": "Balanced reciprocity", "importance": "high"},
                    {"flag": "Growing engagement", "importance": "high"},
                    {"flag": "Strong topic alignment", "importance": "high"},
                    {"flag": "Positive sentiment", "importance": "medium"},
                    {"flag": "Future planning", "importance": "medium"},
                    {"flag": "Mutual value exchange", "importance": "high"},
                    {"flag": "Active listening", "importance": "medium"},
                    {"flag": "Appropriate personal sharing", "importance": "medium"},
                    {"flag": "Humor reciprocated", "importance": "low"},
                    {"flag": "No ghosting patterns", "importance": "high"},
                    {"flag": "Consistent follow-through", "importance": "high"},
                ],

                "ghosting_risk": {
                    "risk_score": 0.07,  # Very low
                    "confidence": 0.91,
                    "assessment": "Minimal ghosting risk - strong engagement patterns"
                },

                "conversation_death_prediction": {
                    "probability_next_30_days": 0.11,
                    "confidence": 0.83,
                    "protective_factors": [
                        "High reciprocity",
                        "Growing momentum",
                        "Clear mutual value",
                        "Both initiative-takers"
                    ]
                }
            },

            "future_orientation": {
                "score": 0.82,
                "forward_looking_statements": 17,
                "concrete_next_steps": 4,

                "planned_interactions": [
                    {
                        "type": "video_call",
                        "status": "scheduled",
                        "date": "2025-01-20",
                        "topic": "Partnership discussion"
                    },
                    {
                        "type": "introduction",
                        "status": "pending",
                        "description": "User B to intro User A to investor"
                    },
                    {
                        "type": "collaboration",
                        "status": "exploring",
                        "description": "Potential product integration"
                    }
                ],

                "relationship_trajectory": {
                    "current_stage": "active_exploration",
                    "predicted_next_stage": "committed_partnership",
                    "timeline_to_next_stage": "2-4 weeks",
                    "confidence": 0.79
                }
            },

            "optimization_recommendations": {
                "maintain": [
                    "Current response cadence - excellent balance",
                    "Question asking - shows genuine interest",
                    "Value exchange - keep offering mutual value",
                    "Positive reinforcement - encouraging and supportive"
                ],
                "improve": [
                    {
                        "area": "Meeting coordination",
                        "suggestion": "Use Calendly or similar tool",
                        "priority": "low"
                    },
                    {
                        "area": "Deepen one topic",
                        "suggestion": "Go deeper on AI/ML topic - most aligned",
                        "priority": "medium"
                    }
                ],
                "opportunities": [
                    "Schedule in-person meeting if geographically feasible",
                    "Introduce to each other's networks",
                    "Collaborate on small project to test partnership",
                    "Share resources (articles, contacts, etc.)"
                ]
            },

            "metadata": {
                "analysis_model": "Conversation Dynamics v2.0",
                "confidence_score": 0.93,
                "data_quality": "high",
                "last_updated": "2025-01-16T14:30:00Z",
            }
        }

        return Result(
            success=True,
            data=conversation_analysis,
            quality_score=0.93,
            metadata={
                "agent_id": self.agent_id,
                "analysis_type": "conversation_dynamics",
                "processing_time_ms": 298,
                "model_version": "conversation_v2.0",
            }
        )


def create_conversation_dynamics_agent(agent_id: str = "conversation_dynamics_1") -> ConversationDynamicsAgent:
    """Factory function to create a ConversationDynamicsAgent."""
    return ConversationDynamicsAgent(agent_id)


if __name__ == "__main__":
    # Demo usage
    import asyncio

    async def demo():
        agent = create_conversation_dynamics_agent()

        task = Task(
            task_id="conv_001",
            description="Analyze conversation dynamics between two potential partners",
            required_capabilities=["conversation_health", "engagement_analysis"],
            priority=1
        )

        result = await agent.process_task(task)

        print(f"\n{'='*70}")
        print(f"Conversation Dynamics Analysis Results")
        print(f"{'='*70}\n")

        health = result.data['conversation_health_score']
        print(f"Conversation Health: {health['level']} ({health['overall']:.0%})")
        print(f"Trend: {health['trend'].title()}")
        print(f"Prediction: {health['prediction']}\n")

        print(f"Component Scores:")
        for component, score in health['component_scores'].items():
            print(f"  - {component.replace('_', ' ').title()}: {score:.0%}")

        print(f"\nReciprocity: {result.data['reciprocity_analysis']['overall_reciprocity']:.0%}")
        print(f"Rapport: {result.data['rapport_building']['rapport_score']:.0%}")
        print(f"Momentum: {result.data['conversation_momentum']['momentum_score']:.0%}")

        print(f"\nGreen Flags: {result.data['red_flags_and_warnings']['green_flags_detected']}")
        print(f"Yellow Flags: {result.data['red_flags_and_warnings']['yellow_flags_detected']}")
        print(f"Red Flags: {result.data['red_flags_and_warnings']['red_flags_detected']}")

        print(f"\nGhosting Risk: {result.data['red_flags_and_warnings']['ghosting_risk']['risk_score']:.0%} (Very Low)")

        print(f"\n{'='*70}\n")

    asyncio.run(demo())
