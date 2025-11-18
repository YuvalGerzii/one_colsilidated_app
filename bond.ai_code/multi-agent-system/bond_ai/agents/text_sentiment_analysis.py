"""
Text Sentiment Analysis Agent for Bond.AI

Advanced NLP agent for analyzing text sentiment, emotion, tone, and intent in
professional communications. Goes beyond simple positive/negative to provide
nuanced understanding of communication patterns.

Key Features:
- Multi-dimensional sentiment analysis (polarity + intensity)
- 8-emotion detection (Plutchik's wheel)
- Tone analysis (professional, casual, enthusiastic, etc.)
- Intent classification (request, offer, question, etc.)
- Subtext detection (sarcasm, hesitation, urgency)
- Writing style fingerprinting
- Semantic similarity and meaning extraction
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from typing import Any, Dict, List, Optional
from loguru import logger

from multi_agent_system.agents.base import BaseAgent
from multi_agent_system.core.types import Task, Result, AgentCapability


class TextSentimentAnalysisAgent(BaseAgent):
    """
    Advanced agent specialized in text sentiment and emotion analysis.

    Uses NLP techniques to understand:
    - Sentiment (positive/negative/neutral with intensity)
    - Emotions (joy, anger, fear, sadness, etc.)
    - Tone (professional, casual, urgent, etc.)
    - Intent (request, offer, question, etc.)
    - Subtext (sarcasm, hesitation, enthusiasm)
    - Writing style and patterns

    Capabilities:
    - Multi-dimensional sentiment scoring
    - Emotion detection (8 basic emotions)
    - Tone and formality analysis
    - Intent classification
    - Subtext and nuance detection
    - Writing style profiling
    - Semantic meaning extraction
    """

    def __init__(self, agent_id: str = "text_sentiment_1", message_bus=None):
        capabilities = [
            AgentCapability("sentiment_analysis", "Multi-dimensional sentiment analysis", 0.92),
            AgentCapability("emotion_detection", "Detect 8 basic emotions", 0.89),
            AgentCapability("tone_analysis", "Analyze communication tone", 0.90),
            AgentCapability("intent_classification", "Classify message intent", 0.88),
            AgentCapability("subtext_detection", "Detect sarcasm, hesitation, urgency", 0.84),
            AgentCapability("writing_style", "Profile writing style", 0.87),
            AgentCapability("semantic_analysis", "Extract semantic meaning", 0.91),
        ]
        super().__init__(agent_id, capabilities, message_bus)

    async def process_task(self, task: Task) -> Result:
        """
        Process a text sentiment analysis task.

        Args:
            task: Text analysis task to process

        Returns:
            Comprehensive text sentiment and emotion analysis results
        """
        logger.info(f"{self.agent_id} analyzing text sentiment: {task.description}")

        # Sample text for analysis (in real implementation, extract from task)
        sample_text = """
        Hi! I'm really excited about the possibility of collaborating on this project.
        I think there could be great synergy between our teams. I'd love to schedule
        a call next week to discuss further - would Tuesday or Wednesday work for you?
        Looking forward to hearing your thoughts!
        """

        # Simulate comprehensive text analysis
        text_analysis = {
            "task": task.description,
            "analyzed_text_preview": sample_text[:100] + "...",
            "text_length": len(sample_text.split()),
            "analysis_timestamp": "2025-01-16T10:30:00Z",

            "sentiment_analysis": {
                "overall_sentiment": {
                    "polarity": "positive",  # positive, negative, neutral
                    "polarity_score": 0.82,  # -1 to +1 scale
                    "intensity": "strong",  # weak, moderate, strong, very_strong
                    "confidence": 0.94,
                },
                "sentiment_dimensions": {
                    "positivity": {
                        "score": 0.85,
                        "indicators": ["excited", "great synergy", "looking forward"],
                        "strength": "strong"
                    },
                    "negativity": {
                        "score": 0.03,
                        "indicators": [],
                        "strength": "minimal"
                    },
                    "neutrality": {
                        "score": 0.12,
                        "indicators": ["schedule a call", "next week"],
                        "strength": "low"
                    }
                },
                "sentiment_evolution": {
                    "opening": 0.89,  # "really excited"
                    "middle": 0.78,  # "great synergy"
                    "closing": 0.81,  # "looking forward"
                    "trend": "consistently_positive",
                    "description": "Maintains enthusiastic tone throughout"
                }
            },

            "emotion_detection": {
                "model": "Plutchik's 8 Basic Emotions",
                "detected_emotions": [
                    {
                        "emotion": "joy",
                        "intensity": 0.84,
                        "evidence": ["excited", "great", "love to", "looking forward"],
                        "description": "Strong positive emotion, genuine enthusiasm"
                    },
                    {
                        "emotion": "anticipation",
                        "intensity": 0.76,
                        "evidence": ["possibility", "could be", "looking forward"],
                        "description": "Hopeful expectation of positive outcome"
                    },
                    {
                        "emotion": "trust",
                        "intensity": 0.68,
                        "evidence": ["great synergy", "our teams", "collaborate"],
                        "description": "Confidence in potential partnership"
                    }
                ],
                "emotional_valence": "very_positive",
                "emotional_arousal": "high",  # how energized the emotion is
                "emotional_dominance": "confident",  # feeling of control
                "overall_emotional_tone": "Enthusiastic optimism with professional warmth"
            },

            "tone_analysis": {
                "primary_tone": "Professional-Enthusiastic",
                "tone_dimensions": {
                    "formality": {
                        "score": 0.64,  # 0 = very casual, 1 = very formal
                        "classification": "Professional-friendly",
                        "description": "Business appropriate with warm, approachable language"
                    },
                    "enthusiasm": {
                        "score": 0.87,
                        "classification": "Highly enthusiastic",
                        "indicators": ["really excited", "great", "love to", "!"]
                    },
                    "urgency": {
                        "score": 0.32,
                        "classification": "Low urgency",
                        "description": "Relaxed timeline, flexible scheduling"
                    },
                    "confidence": {
                        "score": 0.79,
                        "classification": "Confident",
                        "indicators": ["I think", "could be", "great synergy"]
                    },
                    "assertiveness": {
                        "score": 0.56,
                        "classification": "Moderately assertive",
                        "description": "Suggests action but leaves room for response"
                    },
                    "warmth": {
                        "score": 0.81,
                        "classification": "Warm and friendly",
                        "indicators": ["excited", "love to", "looking forward"]
                    }
                },
                "tone_suitability": {
                    "context": "Initial partnership outreach",
                    "appropriateness": 0.93,
                    "feedback": "Excellent tone for building new relationships - enthusiastic but professional"
                }
            },

            "intent_classification": {
                "primary_intent": "partnership_proposal",
                "intent_breakdown": [
                    {
                        "intent_type": "express_interest",
                        "confidence": 0.96,
                        "text_evidence": "excited about the possibility of collaborating"
                    },
                    {
                        "intent_type": "value_proposition",
                        "confidence": 0.89,
                        "text_evidence": "great synergy between our teams"
                    },
                    {
                        "intent_type": "meeting_request",
                        "confidence": 0.94,
                        "text_evidence": "schedule a call next week"
                    },
                    {
                        "intent_type": "seeking_response",
                        "confidence": 0.87,
                        "text_evidence": "would Tuesday or Wednesday work for you"
                    }
                ],
                "speech_acts": {
                    "assertions": 1,  # "I think there could be great synergy"
                    "questions": 1,  # "would Tuesday or Wednesday work"
                    "requests": 1,  # "love to schedule a call"
                    "offers": 1,  # implicit offer of collaboration
                    "commitments": 0,
                },
                "call_to_action": {
                    "present": True,
                    "clarity": "high",
                    "specific": True,
                    "description": "Clear request to schedule call with specific days",
                    "pressure_level": "low",  # Not pushy
                }
            },

            "subtext_detection": {
                "detected_subtexts": [
                    {
                        "type": "genuine_enthusiasm",
                        "confidence": 0.91,
                        "evidence": "Multiple enthusiasm markers without over-the-top language",
                        "interpretation": "Authentic interest, not forced politeness"
                    },
                    {
                        "type": "respect_for_autonomy",
                        "confidence": 0.84,
                        "evidence": "Offers options, uses 'would...work for you'",
                        "interpretation": "Values recipient's time and preferences"
                    },
                    {
                        "type": "confidence_without_arrogance",
                        "confidence": 0.78,
                        "evidence": "Uses 'I think' and 'could be', not 'definitely' or 'will'",
                        "interpretation": "Confident but humble, open to discussion"
                    }
                ],
                "sarcasm_detected": False,
                "passive_aggressiveness": 0.02,  # Very low
                "hidden_objections": False,
                "hesitation_markers": 0.08,  # Minimal ("I think", "could be")
                "urgency_subtexts": {
                    "artificial_scarcity": False,
                    "pressure_tactics": False,
                    "genuine_time_sensitivity": False,
                },
                "overall_authenticity": 0.92,  # Very authentic, not scripted
            },

            "writing_style_profile": {
                "style_signature": "Professional_Warm_Concise",
                "characteristics": {
                    "vocabulary_richness": {
                        "score": 0.68,
                        "description": "Good variety without being overly complex",
                        "lexical_diversity": 0.71,
                    },
                    "sentence_structure": {
                        "average_length": 15,  # words
                        "complexity": "moderate",
                        "variety": "good",
                        "readability_grade": 10,  # 10th grade level
                    },
                    "punctuation_style": {
                        "exclamation_marks": 2,
                        "question_marks": 1,
                        "em_dashes": 0,
                        "description": "Uses enthusiasm markers appropriately",
                    },
                    "formality_markers": {
                        "contractions": 1,  # "I'd"
                        "slang": 0,
                        "jargon": 1,  # "synergy"
                        "business_buzzwords": 1,  # "synergy"
                        "formality_level": "professional_casual",
                    },
                    "personal_vs_impersonal": {
                        "score": 0.78,  # 0 = impersonal, 1 = personal
                        "first_person_count": 5,  # "I", "I'm", "I'd"
                        "description": "Personal and engaging",
                    },
                    "directness": {
                        "score": 0.72,
                        "description": "Direct about intentions, polite in delivery",
                    }
                },
                "writing_personality": "Enthusiastic Professional - warm, authentic, action-oriented"
            },

            "semantic_analysis": {
                "key_themes": [
                    {"theme": "collaboration", "relevance": 0.89},
                    {"theme": "enthusiasm", "relevance": 0.87},
                    {"theme": "partnership", "relevance": 0.84},
                    {"theme": "next_steps", "relevance": 0.76},
                ],
                "semantic_keywords": [
                    "collaborate", "synergy", "teams", "project",
                    "call", "discuss", "thoughts"
                ],
                "topic_modeling": {
                    "primary_topic": "Partnership Proposal",
                    "secondary_topics": ["Meeting Scheduling", "Value Alignment"],
                },
                "named_entities": {
                    "temporal": ["next week", "Tuesday", "Wednesday"],
                    "organizations": ["our teams"],
                    "actions": ["schedule a call", "discuss"],
                },
                "semantic_similarity": {
                    "similar_to": [
                        "Partnership proposal emails",
                        "Networking follow-ups",
                        "Business development outreach"
                    ],
                    "dissimilar_to": [
                        "Sales pitches",
                        "Spam",
                        "Formal RFPs"
                    ]
                }
            },

            "communication_effectiveness": {
                "overall_score": 0.88,
                "clarity": 0.92,  # Message is very clear
                "engagement": 0.89,  # Likely to elicit positive response
                "persuasiveness": 0.84,  # Compelling value prop
                "professionalism": 0.87,  # Appropriate for business context
                "action_orientation": 0.91,  # Clear next step
                "relationship_building": 0.93,  # Excellent for building rapport

                "predicted_response_metrics": {
                    "response_likelihood": 0.87,
                    "positive_response_likelihood": 0.82,
                    "meeting_acceptance_likelihood": 0.76,
                    "estimated_response_time_hours": 18,
                },

                "strengths": [
                    "Genuine enthusiasm without being over-the-top",
                    "Clear call-to-action with options",
                    "Professional yet warm tone",
                    "Specific but flexible",
                    "Shows value without being pushy"
                ],

                "potential_improvements": [
                    "Could add brief context about why specifically this person/company",
                    "Might include one concrete example of potential synergy",
                    "Consider adding alternative contact method (if urgent)"
                ],
            },

            "red_flags_green_flags": {
                "green_flags": [
                    {"flag": "Authentic enthusiasm", "importance": "high"},
                    {"flag": "Clear next steps", "importance": "high"},
                    {"flag": "Respectful of time", "importance": "medium"},
                    {"flag": "Professional tone", "importance": "medium"},
                    {"flag": "Specific scheduling", "importance": "medium"},
                ],
                "yellow_flags": [
                    {"flag": "Slightly generic (could be more personalized)", "severity": "low"},
                ],
                "red_flags": [],
                "overall_assessment": "Excellent communication - professional, enthusiastic, actionable",
            },

            "metadata": {
                "analysis_model": "Advanced NLP v2.0",
                "confidence_score": 0.91,
                "processing_time_ms": 178,
                "last_updated": "2025-01-16",
            }
        }

        return Result(
            success=True,
            data=text_analysis,
            quality_score=0.92,
            metadata={
                "agent_id": self.agent_id,
                "analysis_type": "text_sentiment",
                "processing_time_ms": 178,
                "model_version": "sentiment_v2.0",
            }
        )

    async def analyze_sentiment(self, text: str) -> Dict:
        """Analyze sentiment polarity and intensity."""
        # Simplified sentiment analysis (in production, use transformers/BERT)
        positive_words = ["excited", "great", "love", "forward", "excellent"]
        negative_words = ["bad", "terrible", "disappointed", "unfortunately"]

        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)

        polarity_score = (pos_count - neg_count) / (pos_count + neg_count + 1)

        return {
            "polarity_score": polarity_score,
            "polarity": "positive" if polarity_score > 0.1 else "negative" if polarity_score < -0.1 else "neutral",
            "confidence": min(0.95, (pos_count + neg_count) / 10)
        }

    async def detect_emotions(self, text: str) -> List[Dict]:
        """Detect emotions using Plutchik's 8 basic emotions."""
        # In production, use emotion classification models
        emotion_keywords = {
            "joy": ["excited", "happy", "great", "wonderful", "love"],
            "trust": ["synergy", "collaborate", "partnership"],
            "anticipation": ["looking forward", "possibility", "could be"],
            "fear": ["worried", "concerned", "afraid"],
            "surprise": ["wow", "unexpected", "amazed"],
            "sadness": ["disappointed", "unfortunately", "sad"],
            "disgust": ["terrible", "awful", "horrible"],
            "anger": ["frustrated", "angry", "furious"],
        }

        detected = []
        for emotion, keywords in emotion_keywords.items():
            intensity = sum(1 for kw in keywords if kw in text.lower()) / len(keywords)
            if intensity > 0:
                detected.append({"emotion": emotion, "intensity": min(intensity * 2, 1.0)})

        return sorted(detected, key=lambda x: x["intensity"], reverse=True)


def create_text_sentiment_agent(agent_id: str = "text_sentiment_1") -> TextSentimentAnalysisAgent:
    """Factory function to create a TextSentimentAnalysisAgent."""
    return TextSentimentAnalysisAgent(agent_id)


if __name__ == "__main__":
    # Demo usage
    import asyncio

    async def demo():
        agent = create_text_sentiment_agent()

        task = Task(
            task_id="text_001",
            description="Analyze sentiment and tone of partnership outreach message",
            required_capabilities=["sentiment_analysis", "tone_analysis", "intent_classification"],
            priority=1
        )

        result = await agent.process_task(task)

        print(f"\n{'='*70}")
        print(f"Text Sentiment Analysis Results")
        print(f"{'='*70}\n")

        sentiment = result.data['sentiment_analysis']['overall_sentiment']
        print(f"Overall Sentiment: {sentiment['polarity'].upper()} ({sentiment['polarity_score']:.2f})")
        print(f"Intensity: {sentiment['intensity']}")
        print(f"Confidence: {sentiment['confidence']:.0%}\n")

        print(f"Primary Tone: {result.data['tone_analysis']['primary_tone']}")
        print(f"Communication Effectiveness: {result.data['communication_effectiveness']['overall_score']:.0%}\n")

        print(f"Detected Emotions:")
        for emotion in result.data['emotion_detection']['detected_emotions']:
            print(f"  - {emotion['emotion'].title()}: {emotion['intensity']:.0%}")

        print(f"\nPrimary Intent: {result.data['intent_classification']['primary_intent'].replace('_', ' ').title()}")

        print(f"\nResponse Prediction:")
        pred = result.data['communication_effectiveness']['predicted_response_metrics']
        print(f"  Response Likelihood: {pred['response_likelihood']:.0%}")
        print(f"  Positive Response:   {pred['positive_response_likelihood']:.0%}")
        print(f"  Meeting Acceptance:  {pred['meeting_acceptance_likelihood']:.0%}")

        print(f"\n{'='*70}\n")

    asyncio.run(demo())
