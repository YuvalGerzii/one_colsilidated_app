"""
Cross-Platform Intelligence System

Unified intelligence layer that connects 104+ AI agents across all platforms:
- Finance Platform (39 agents)
- Labor Transformation (15 agents)
- Real Estate Dashboard (6 agents)
- Bond.AI (35+ agents)
- Legacy Systems (10 agents)

Enables cross-platform queries like:
- "Find investors in my network for this real estate deal"
- "Match my career skills to opportunities in my professional network"
- "Predict market impact on my real estate portfolio"
"""

__version__ = "1.0.0"

from .orchestrator import CrossPlatformOrchestrator
from .entity_resolver import UnifiedEntityResolver
from .query_router import IntelligentQueryRouter
from .knowledge_graph import CrossPlatformKnowledgeGraph

__all__ = [
    "CrossPlatformOrchestrator",
    "UnifiedEntityResolver",
    "IntelligentQueryRouter",
    "CrossPlatformKnowledgeGraph"
]
