"""
Communication Style Analysis Agent for Bond.AI

Analyzes communication patterns, preferences, and styles to predict compatibility
and effective interaction strategies for professional relationships.

Based on research showing communication style is critical for team dynamics
and collaboration success.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from typing import Any, Dict, List
from loguru import logger

from multi_agent_system.agents.base import BaseAgent
from multi_agent_system.core.types import Task, Result, AgentCapability


class CommunicationStyleAnalysisAgent(BaseAgent):
    """
    Advanced agent specialized in communication style analysis and matching.

    Capabilities:
    - Communication pattern recognition
    - Response time and frequency analysis
    - Formality level detection
    - Directness vs. indirectness assessment
    - Feedback preference analysis
    - Meeting vs. async communication preference
    - Communication effectiveness prediction
    """

    def __init__(self, agent_id: str = "communication_analyzer_1", message_bus=None):
        capabilities = [
            AgentCapability("pattern_recognition", "Recognize communication patterns", 0.92),
            AgentCapability("response_analysis", "Analyze response behavior", 0.90),
            AgentCapability("formality_detection", "Detect formality levels", 0.89),
            AgentCapability("directness_assessment", "Assess communication directness", 0.91),
            AgentCapability("feedback_preferences", "Analyze feedback preferences", 0.88),
            AgentCapability("channel_preferences", "Determine preferred channels", 0.87),
            AgentCapability("effectiveness_prediction", "Predict communication effectiveness", 0.90),
            AgentCapability("communication_analysis", "General communication analysis", 0.91),
        ]
        super().__init__(agent_id, capabilities, message_bus)

    async def process_task(self, task: Task) -> Result:
        """
        Process a communication style analysis task.

        Args:
            task: Communication analysis task to process

        Returns:
            Comprehensive communication style analysis results
        """
        logger.info(f"{self.agent_id} analyzing communication styles: {task.description}")

        # Simulate comprehensive communication analysis
        analysis_results = {
            "task": task.description,
            "your_communication_profile": {
                "overall_style": "Direct, Clear, Professional-Casual",
                "communication_dimensions": {
                    "directness": {"score": 0.82, "style": "Direct - Says what they mean, gets to the point"},
                    "formality": {"score": 0.54, "style": "Professional-Casual - Adapts to context"},
                    "expressiveness": {"score": 0.71, "style": "Moderately Expressive - Shows enthusiasm appropriately"},
                    "responsiveness": {"score": 0.85, "style": "Very Responsive - Quick to reply"},
                    "detail_orientation": {"score": 0.68, "style": "Balanced - Provides key details without overwhelming"},
                    "empathy_in_communication": {"score": 0.73, "style": "Moderately High - Acknowledges others' perspectives"},
                },
                "preferred_channels": [
                    {"channel": "Video Calls", "preference": 0.89, "use_case": "Important decisions, brainstorming"},
                    {"channel": "Async Messaging (Slack)", "preference": 0.85, "use_case": "Quick updates, collaboration"},
                    {"channel": "Email", "preference": 0.67, "use_case": "Formal communication, documentation"},
                    {"channel": "Phone Calls", "preference": 0.45, "use_case": "Urgent matters only"},
                    {"channel": "In-Person", "preference": 0.78, "use_case": "Relationship building, complex discussions"},
                ],
                "response_patterns": {
                    "avg_response_time": "2.3 hours (work hours)",
                    "response_length": "Medium (100-200 words typical)",
                    "response_thoroughness": "Addresses all points raised",
                    "followup_rate": 0.87,  # Follows up 87% of the time
                },
                "feedback_style": {
                    "giving_feedback": "Direct but constructive, solution-oriented",
                    "receiving_feedback": "Open to feedback, asks clarifying questions",
                    "preferred_feedback_format": "1-on-1, specific examples, actionable suggestions",
                },
            },
            "communication_compatibility": [
                {
                    "match": "Alex Thompson",
                    "compatibility_score": 0.88,
                    "analysis": {
                        "directness_match": {
                            "score": 0.92,
                            "both_styles": "Both direct communicators",
                            "synergy": "Clear, no-BS communication - reduces misunderstandings",
                            "recommendation": "Can be very direct - will appreciate honesty",
                        },
                        "formality_match": {
                            "score": 0.86,
                            "both_styles": "Professional-casual",
                            "synergy": "Comfortable, authentic communication",
                            "recommendation": "Can use informal language while maintaining professionalism",
                        },
                        "channel_preferences": {
                            "score": 0.89,
                            "alignment": "Both prefer video calls and async messaging",
                            "synergy": "Can work efficiently remotely",
                            "recommendation": "Weekly video check-ins + daily Slack updates",
                        },
                        "response_compatibility": {
                            "score": 0.91,
                            "both_patterns": "Quick responders (avg 2-3 hours)",
                            "synergy": "Fast decision-making, momentum maintained",
                            "recommendation": "Leverage speed for rapid iteration",
                        },
                        "feedback_compatibility": {
                            "score": 0.84,
                            "analysis": "Both appreciate direct, constructive feedback",
                            "synergy": "Growth-oriented relationship",
                            "recommendation": "Regular feedback sessions will strengthen collaboration",
                        },
                    },
                    "optimal_communication_strategy": {
                        "meeting_frequency": "Weekly video call + daily async",
                        "meeting_format": "Agenda-driven but allows for creative discussion",
                        "feedback_cadence": "Bi-weekly 1-on-1s for mutual feedback",
                        "decision_making": "Discuss options async, decide synchronously",
                        "conflict_resolution": "Address directly and immediately - both prefer this",
                    },
                    "predicted_effectiveness": 0.88,
                },
                {
                    "match": "Jennifer Liu",
                    "compatibility_score": 0.74,
                    "analysis": {
                        "directness_match": {
                            "score": 0.71,
                            "styles": "You: Direct (0.82), Them: Moderate (0.62)",
                            "friction": "Your directness may feel abrupt to them",
                            "recommendation": "Soften language slightly, provide more context",
                        },
                        "formality_match": {
                            "score": 0.65,
                            "styles": "You: Professional-Casual, Them: More Formal",
                            "friction": "They prefer more formal communication",
                            "recommendation": "Use email for important topics, maintain professionalism",
                        },
                        "channel_preferences": {
                            "score": 0.72,
                            "alignment": "They prefer email/written, you prefer video/async messaging",
                            "friction": "Different channel preferences",
                            "recommendation": "Compromise: structured emails + occasional video calls",
                        },
                        "response_compatibility": {
                            "score": 0.68,
                            "patterns": "You: Quick (2.3h), Them: Thoughtful (1-2 days)",
                            "friction": "Pace mismatch - you may feel impatient",
                            "recommendation": "Set expectations: 24-48h response time for important items",
                        },
                        "feedback_compatibility": {
                            "score": 0.79,
                            "analysis": "Both value feedback, but different delivery preferences",
                            "friction": "They prefer written feedback, you prefer verbal",
                            "recommendation": "Combine: written feedback followed by discussion",
                        },
                    },
                    "optimal_communication_strategy": {
                        "meeting_frequency": "Bi-weekly structured meetings",
                        "meeting_format": "Formal agenda, pre-reads, clear action items",
                        "feedback_cadence": "Monthly written feedback + quarterly discussion",
                        "decision_making": "Provide detailed written proposals, allow processing time",
                        "conflict_resolution": "Schedule dedicated time, prepare written points",
                    },
                    "predicted_effectiveness": 0.74,
                },
            ],
            "communication_insights": {
                "your_strengths": [
                    "Quick response time builds momentum",
                    "Directness reduces ambiguity and wasted time",
                    "Adaptable formality works across contexts",
                    "Strong follow-up rate ensures completion",
                ],
                "your_development_areas": [
                    "Could provide more context for those who prefer detail",
                    "May need to slow down for thoughtful processors",
                    "Could incorporate more written communication for formal contexts",
                ],
                "ideal_communication_partners": [
                    "Direct communicators (avoid misunderstandings)",
                    "Quick responders (maintain momentum)",
                    "Video-call comfortable (your preferred channel)",
                    "Feedback-oriented (mutual growth)",
                ],
                "challenging_communication_partners": [
                    "Very indirect communicators (frustrating for you)",
                    "Slow responders (breaks your rhythm)",
                    "Email-only preferrers (limits your expressiveness)",
                    "Feedback-averse (limits relationship depth)",
                ],
            },
            "team_communication_dynamics": {
                "as_team_leader": {
                    "style": "Clear expectations, regular check-ins, open door",
                    "team_preference": "Mix of direct and moderate communicators",
                    "meeting_approach": "Agenda-driven, time-boxed, action-oriented",
                    "effectiveness": 0.86,
                },
                "in_cross_functional_teams": {
                    "strength": "Bridges technical and business communication",
                    "adaptation_needed": "Adjust directness based on function",
                    "effectiveness": 0.79,
                },
                "in_remote_settings": {
                    "strength": "Comfortable with video and async tools",
                    "preference": "Video-first for important items",
                    "effectiveness": 0.91,
                },
            },
            "communication_optimization": {
                "with_direct_communicators": {
                    "approach": "Be as direct as you naturally are",
                    "channels": "Any - they're flexible",
                    "pace": "Fast - they'll keep up",
                },
                "with_indirect_communicators": {
                    "approach": "Soften language, provide more context",
                    "channels": "Start with written, move to verbal",
                    "pace": "Slower - allow processing time",
                },
                "with_formal_communicators": {
                    "approach": "Increase formality, structure communication",
                    "channels": "Email for official topics",
                    "pace": "Match their rhythm",
                },
                "with_casual_communicators": {
                    "approach": "Your natural professional-casual works",
                    "channels": "Slack, video calls, whatever's efficient",
                    "pace": "Fast and iterative",
                },
            },
            "insights": [
                "88% communication compatibility with Alex Thompson - exceptional match",
                "Direct communication style (0.82) is a strength in professional contexts",
                "Quick response time (2.3h) creates momentum - maintain this",
                "Professional-casual formality (0.54) shows good adaptability",
                "Video call preference (0.89) ideal for remote-first world",
                "74% compatibility with Jennifer Liu requires communication adaptation",
                "High follow-up rate (87%) is above average - demonstrates reliability",
                "Balanced detail orientation (0.68) works for most contexts",
                "Empathy in communication (0.73) could be strengthened slightly",
                "Response length (100-200 words) is optimal - clear and complete",
            ],
            "recommendations": [
                "Prioritize relationships with direct communicators like Alex Thompson (88% compatibility)",
                "With Jennifer Liu, adapt: use email, provide more context, allow 24-48h response time",
                "Maintain quick response time (2.3h) - it's a competitive advantage",
                "For new relationships, start with video calls to build rapport quickly",
                "Explicitly state communication preferences early in relationships",
                "When working with indirect communicators, ask clarifying questions",
                "Leverage your adaptable formality - it works across business and technical audiences",
                "Set up weekly video check-ins + daily async for optimal collaboration rhythm",
                "Use your direct feedback style with those who appreciate it (T-types, direct communicators)",
                "Practice providing more context for detail-oriented communicators",
            ],
            "confidence": 0.91,
        }

        return Result(
            task_id=task.id,
            success=True,
            data=analysis_results,
            agent_id=self.agent_id,
            quality_score=0.91,
            metadata={
                "analysis_dimensions": 6,
                "communication_patterns_analyzed": "directness, formality, expressiveness, responsiveness, detail, empathy",
                "compatibility_predictions": 2,
            }
        )
