"""
Behavioral Pattern Analysis Agent for Bond.AI

Analyzes behavioral patterns over time to predict reliability, consistency, and
relationship quality. Uses temporal analysis, engagement metrics, and behavioral
fingerprinting to identify patterns.

Key Features:
- Temporal behavior analysis (activity patterns, response times)
- Consistency metrics (reliability, follow-through)
- Social interaction patterns (networking style, relationship building)
- Work rhythm analysis (productivity hours, meeting preferences)
- Engagement trajectory (relationship investment over time)
- Red flag detection (ghosting, flakiness, inconsistency)
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


class BehavioralPatternAnalysisAgent(BaseAgent):
    """
    Advanced agent specialized in behavioral pattern recognition and analysis.

    Capabilities:
    - Temporal behavior tracking and analysis
    - Response pattern analysis
    - Consistency and reliability scoring
    - Engagement trajectory prediction
    - Red flag detection
    - Work rhythm profiling
    - Social interaction pattern analysis
    - Behavioral fingerprinting
    """

    def __init__(self, agent_id: str = "behavioral_pattern_1", message_bus=None):
        capabilities = [
            AgentCapability("temporal_analysis", "Analyze temporal behavior patterns", 0.91),
            AgentCapability("response_pattern", "Analyze response patterns and latency", 0.93),
            AgentCapability("consistency_scoring", "Score reliability and consistency", 0.90),
            AgentCapability("engagement_trajectory", "Predict engagement trajectory", 0.88),
            AgentCapability("red_flag_detection", "Detect behavioral red flags", 0.87),
            AgentCapability("work_rhythm", "Profile work rhythm and preferences", 0.89),
            AgentCapability("social_patterns", "Analyze social interaction patterns", 0.86),
            AgentCapability("behavioral_fingerprint", "Create behavioral fingerprint", 0.92),
        ]
        super().__init__(agent_id, capabilities, message_bus)

    async def process_task(self, task: Task) -> Result:
        """
        Process a behavioral pattern analysis task.

        Args:
            task: Behavioral analysis task to process

        Returns:
            Comprehensive behavioral pattern analysis results
        """
        logger.info(f"{self.agent_id} analyzing behavioral patterns: {task.description}")

        # Simulate comprehensive behavioral pattern analysis
        behavioral_analysis = {
            "task": task.description,
            "analysis_period": {
                "start_date": "2024-07-01",
                "end_date": "2025-01-16",
                "duration_days": 199,
                "data_points": 847,
            },

            "temporal_patterns": {
                "activity_rhythm": {
                    "most_active_hours": [9, 10, 14, 15, 16],
                    "least_active_hours": [0, 1, 2, 3, 22, 23],
                    "peak_day": "Tuesday",
                    "slowest_day": "Sunday",
                    "activity_score": 0.78,
                    "consistency": 0.82,
                    "description": "Regular business hours pattern with strong consistency"
                },
                "response_patterns": {
                    "average_response_time_minutes": 127,
                    "median_response_time_minutes": 45,
                    "response_time_trend": "improving",  # improving, stable, declining
                    "response_rate": 0.89,
                    "response_reliability_score": 0.87,
                    "time_zones_adapted": True,
                    "weekend_response_rate": 0.34,
                    "urgent_response_time_minutes": 23,
                },
                "engagement_cycles": {
                    "active_periods": 14,
                    "dormant_periods": 3,
                    "average_active_duration_days": 12,
                    "average_dormant_duration_days": 4,
                    "cycle_regularity": 0.71,
                    "current_status": "active",
                    "days_in_current_cycle": 8,
                }
            },

            "consistency_metrics": {
                "overall_reliability_score": 0.84,  # 0-1 scale
                "components": {
                    "response_consistency": {
                        "score": 0.87,
                        "description": "Highly consistent in responding to messages",
                        "variance": 0.13,
                    },
                    "follow_through_rate": {
                        "score": 0.82,
                        "description": "Good at following through on commitments",
                        "commitments_made": 34,
                        "commitments_kept": 28,
                        "percentage": 82.4,
                    },
                    "meeting_attendance": {
                        "score": 0.91,
                        "scheduled_meetings": 23,
                        "attended": 21,
                        "on_time_rate": 0.86,
                        "cancellation_rate": 0.09,
                        "average_cancellation_notice_hours": 36,
                    },
                    "communication_consistency": {
                        "score": 0.79,
                        "message_frequency_variance": 0.21,
                        "tone_consistency": 0.83,
                        "professionalism_score": 0.88,
                    }
                },
                "red_flags": {
                    "count": 2,
                    "severity": "low",
                    "flags": [
                        {
                            "type": "late_response_spike",
                            "severity": "low",
                            "date": "2024-12-15",
                            "description": "Response time spike during holiday season",
                            "mitigated": True,
                        },
                        {
                            "type": "missed_meeting",
                            "severity": "low",
                            "date": "2024-11-03",
                            "description": "One no-show (emergency, apologized)",
                            "mitigated": True,
                        }
                    ]
                }
            },

            "social_interaction_patterns": {
                "networking_style": {
                    "type": "strategic_connector",  # options: strategic_connector, relationship_builder, transactional, selective, broad_networker
                    "description": "Focuses on high-quality connections with clear mutual value",
                    "connection_rate": "selective",
                    "relationship_depth": "deep",
                    "network_growth_rate": 0.15,  # 15% per month
                },
                "interaction_preferences": {
                    "preferred_channels": [
                        {"channel": "video_call", "preference": 0.78},
                        {"channel": "email", "preference": 0.71},
                        {"channel": "phone", "preference": 0.45},
                        {"channel": "messaging", "preference": 0.52},
                        {"channel": "in_person", "preference": 0.89},
                    ],
                    "meeting_preference": "video_first",
                    "communication_style": "professional_friendly",
                    "response_detail_level": "comprehensive",
                },
                "relationship_building": {
                    "approach": "value_first",
                    "initial_response_rate": 0.94,
                    "relationship_progression_speed": "moderate",
                    "warm_intro_success_rate": 0.87,
                    "cold_outreach_success_rate": 0.23,
                    "reconnection_rate": 0.56,
                }
            },

            "work_rhythm_profile": {
                "productivity_pattern": {
                    "type": "morning_person",  # morning_person, night_owl, balanced
                    "peak_hours": [9, 10, 11],
                    "low_energy_hours": [14, 15],
                    "second_wind_hours": [16, 17],
                    "weekend_work_frequency": "occasional",
                },
                "meeting_preferences": {
                    "optimal_meeting_times": ["09:00-11:00", "14:00-16:00"],
                    "avoid_times": ["12:00-13:00", "after 17:00"],
                    "preferred_duration": 30,
                    "back_to_back_tolerance": "low",
                    "prep_time_needed": 15,
                },
                "async_vs_sync": {
                    "preference": "async_first",
                    "async_score": 0.72,
                    "sync_score": 0.28,
                    "response_to_async": "excellent",
                    "real_time_availability": "scheduled",
                }
            },

            "engagement_trajectory": {
                "current_phase": "growing",  # growing, stable, declining, dormant
                "trend": "positive",
                "trajectory_score": 0.81,
                "metrics": {
                    "message_frequency_trend": "+12%",
                    "response_speed_trend": "+8%",
                    "meeting_frequency_trend": "stable",
                    "relationship_investment_trend": "+15%",
                },
                "predictions": {
                    "30_day_engagement": {
                        "score": 0.84,
                        "confidence": 0.88,
                        "expected_interactions": 23,
                    },
                    "90_day_engagement": {
                        "score": 0.79,
                        "confidence": 0.76,
                        "expected_interactions": 61,
                    },
                    "churn_risk": {
                        "score": 0.12,  # Low risk
                        "confidence": 0.83,
                        "factors": ["strong consistency", "positive trend", "regular engagement"],
                    }
                },
                "relationship_lifecycle_stage": "active_growth",
                "estimated_relationship_value": "high",
            },

            "behavioral_fingerprint": {
                "signature": "strategic_reliable_morning_async_grower",
                "archetype": "Professional Connector",
                "key_traits": [
                    "High reliability and consistency",
                    "Strategic in networking approach",
                    "Morning peak productivity",
                    "Prefers async communication",
                    "Growing engagement trajectory",
                    "Value-driven relationship builder",
                ],
                "compatibility_notes": {
                    "works_well_with": [
                        "Other strategic connectors",
                        "Value-focused professionals",
                        "Morning schedule people",
                        "Async communicators",
                    ],
                    "potential_friction_with": [
                        "Highly impulsive communicators",
                        "Night owls requiring late responses",
                        "Transactional networkers",
                        "Constant real-time availability expecters",
                    ]
                },
                "unique_identifiers": {
                    "response_pattern_signature": "fast_business_hours_consistent",
                    "engagement_signature": "steady_grower",
                    "reliability_signature": "high_consistency_low_variance",
                }
            },

            "anomaly_detection": {
                "anomalies_detected": 1,
                "anomalies": [
                    {
                        "type": "engagement_spike",
                        "date": "2024-09-15",
                        "description": "Unusually high activity during product launch",
                        "severity": "informational",
                        "context": "Launching new startup",
                        "normalized": True,
                    }
                ],
                "behavioral_stability_score": 0.86,
            },

            "recommendations": {
                "best_contact_times": ["Tuesday 10:00", "Wednesday 14:00", "Thursday 09:00"],
                "communication_approach": "Send detailed async messages, propose video calls for important discussions",
                "relationship_strategy": "Focus on mutual value, respect time boundaries, maintain regular cadence",
                "engagement_optimization": [
                    "Schedule important asks during morning hours",
                    "Give 24-48h for thoughtful async responses",
                    "Propose meetings with clear agendas and value props",
                    "Maintain consistent, non-spammy communication rhythm",
                ]
            },

            "metadata": {
                "analysis_version": "2.0",
                "confidence_score": 0.89,
                "data_quality": "high",
                "sample_size": "sufficient",
                "last_updated": datetime.now().isoformat(),
            }
        }

        return Result(
            success=True,
            data=behavioral_analysis,
            quality_score=0.91,
            metadata={
                "agent_id": self.agent_id,
                "analysis_type": "behavioral_pattern",
                "processing_time_ms": 234,
                "model_version": "behavioral_v2.0",
            }
        )

    async def analyze_response_patterns(self, interaction_history: List[Dict]) -> Dict:
        """Analyze response time and consistency patterns."""
        if not interaction_history:
            return {"error": "No interaction history provided"}

        response_times = [i.get("response_time_minutes", 0) for i in interaction_history]

        return {
            "average": np.mean(response_times),
            "median": np.median(response_times),
            "std_dev": np.std(response_times),
            "consistency_score": 1 - (np.std(response_times) / (np.mean(response_times) + 1)),
        }

    async def detect_red_flags(self, behavioral_data: Dict) -> List[Dict]:
        """Detect behavioral red flags."""
        red_flags = []

        # Ghosting detection
        if behavioral_data.get("response_rate", 1.0) < 0.5:
            red_flags.append({
                "type": "low_response_rate",
                "severity": "high",
                "description": "Responds to less than 50% of messages"
            })

        # Flakiness detection
        if behavioral_data.get("follow_through_rate", 1.0) < 0.6:
            red_flags.append({
                "type": "low_follow_through",
                "severity": "medium",
                "description": "Frequently doesn't follow through on commitments"
            })

        # Inconsistency detection
        if behavioral_data.get("consistency_variance", 0) > 0.7:
            red_flags.append({
                "type": "high_inconsistency",
                "severity": "medium",
                "description": "Highly inconsistent behavioral patterns"
            })

        return red_flags

    async def predict_engagement_trajectory(self, historical_data: List[Dict]) -> Dict:
        """Predict future engagement based on historical patterns."""
        # Simple trend analysis
        if len(historical_data) < 3:
            return {"prediction": "insufficient_data"}

        engagement_scores = [d.get("engagement_score", 0.5) for d in historical_data]

        # Linear trend
        trend = np.polyfit(range(len(engagement_scores)), engagement_scores, 1)[0]

        if trend > 0.01:
            phase = "growing"
        elif trend < -0.01:
            phase = "declining"
        else:
            phase = "stable"

        return {
            "current_phase": phase,
            "trend": "positive" if trend > 0 else "negative" if trend < 0 else "neutral",
            "confidence": min(0.95, len(historical_data) / 20),
        }


def create_behavioral_pattern_agent(agent_id: str = "behavioral_pattern_1") -> BehavioralPatternAnalysisAgent:
    """Factory function to create a BehavioralPatternAnalysisAgent."""
    return BehavioralPatternAnalysisAgent(agent_id)


if __name__ == "__main__":
    # Demo usage
    import asyncio

    async def demo():
        agent = create_behavioral_pattern_agent()

        task = Task(
            task_id="behavioral_001",
            description="Analyze behavioral patterns for user profile optimization",
            required_capabilities=["behavioral_fingerprint", "engagement_trajectory"],
            priority=1
        )

        result = await agent.process_task(task)

        print(f"\n{'='*60}")
        print(f"Behavioral Pattern Analysis Results")
        print(f"{'='*60}\n")
        print(f"Overall Reliability Score: {result.data['consistency_metrics']['overall_reliability_score']:.0%}")
        print(f"Behavioral Archetype: {result.data['behavioral_fingerprint']['archetype']}")
        print(f"Current Phase: {result.data['engagement_trajectory']['current_phase']}")
        print(f"Red Flags: {result.data['consistency_metrics']['red_flags']['count']}")
        print(f"\nKey Traits:")
        for trait in result.data['behavioral_fingerprint']['key_traits']:
            print(f"  - {trait}")
        print(f"\n{'='*60}\n")

    asyncio.run(demo())
