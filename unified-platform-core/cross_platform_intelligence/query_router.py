"""
Intelligent Query Router

Routes queries to the most appropriate agents and platforms based on:
- Query intent classification
- Required data sources
- Agent capabilities
- Historical performance
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import logging
import re

logger = logging.getLogger(__name__)


class QueryIntent(Enum):
    """Types of query intents"""
    FINANCIAL_ANALYSIS = "financial_analysis"
    MARKET_INTELLIGENCE = "market_intelligence"
    PROPERTY_SEARCH = "property_search"
    CAREER_GUIDANCE = "career_guidance"
    NETWORKING = "networking"
    RISK_ASSESSMENT = "risk_assessment"
    INVESTMENT_OPPORTUNITY = "investment_opportunity"
    DOCUMENT_PROCESSING = "document_processing"
    LEARNING = "learning"
    AUTOMATION = "automation"


class Platform(Enum):
    """Available platforms"""
    FINANCE = "finance"
    REAL_ESTATE = "real_estate"
    BOND_AI = "bond_ai"
    LABOR = "labor"
    LEGACY = "legacy"


@dataclass
class RoutingDecision:
    """Routing decision for a query"""
    query_id: str
    primary_platform: Platform
    secondary_platforms: List[Platform]
    required_agents: List[str]
    confidence: float
    reasoning: str
    estimated_latency_ms: int
    fallback_agents: List[str] = field(default_factory=list)


@dataclass
class AgentCapability:
    """Agent capability descriptor"""
    agent_id: str
    platform: Platform
    capabilities: List[str]
    keywords: List[str]
    avg_response_time_ms: int
    success_rate: float
    specializations: List[str]


class IntelligentQueryRouter:
    """
    Routes queries to optimal agents across platforms.

    Features:
    - Intent classification
    - Multi-platform routing
    - Load balancing
    - Performance optimization
    """

    def __init__(self):
        self.agent_registry: Dict[str, AgentCapability] = {}
        self.routing_history: List[Dict[str, Any]] = []
        self._initialize_agent_registry()

    def _initialize_agent_registry(self):
        """Initialize the agent capability registry"""

        # Finance Platform Agents
        finance_agents = [
            AgentCapability(
                agent_id="extreme_events_agent",
                platform=Platform.FINANCE,
                capabilities=["market_prediction", "risk_detection", "alert_generation"],
                keywords=["crash", "crisis", "extreme", "black swan", "pandemic", "recession"],
                avg_response_time_ms=500,
                success_rate=0.92,
                specializations=["market_crisis", "tail_risk"]
            ),
            AgentCapability(
                agent_id="arbitrage_agent",
                platform=Platform.FINANCE,
                capabilities=["opportunity_detection", "trade_execution", "spread_analysis"],
                keywords=["arbitrage", "spread", "price difference", "profit", "exchange"],
                avg_response_time_ms=100,
                success_rate=0.95,
                specializations=["cross_exchange", "triangular", "statistical"]
            ),
            AgentCapability(
                agent_id="portfolio_optimizer",
                platform=Platform.FINANCE,
                capabilities=["allocation", "rebalancing", "risk_optimization"],
                keywords=["portfolio", "allocation", "diversification", "rebalance", "optimize"],
                avg_response_time_ms=800,
                success_rate=0.88,
                specializations=["mean_variance", "risk_parity", "factor_based"]
            ),
            AgentCapability(
                agent_id="sentiment_analyzer",
                platform=Platform.FINANCE,
                capabilities=["news_analysis", "social_sentiment", "market_mood"],
                keywords=["sentiment", "news", "social", "twitter", "reddit", "mood"],
                avg_response_time_ms=300,
                success_rate=0.85,
                specializations=["news_nlp", "social_media", "earnings_calls"]
            ),
        ]

        # Real Estate Platform Agents
        real_estate_agents = [
            AgentCapability(
                agent_id="property_analyzer",
                platform=Platform.REAL_ESTATE,
                capabilities=["valuation", "cash_flow", "roi_calculation"],
                keywords=["property", "valuation", "cap rate", "noi", "cash flow", "roi"],
                avg_response_time_ms=400,
                success_rate=0.90,
                specializations=["residential", "commercial", "multifamily"]
            ),
            AgentCapability(
                agent_id="market_intelligence_agent",
                platform=Platform.REAL_ESTATE,
                capabilities=["market_analysis", "trend_detection", "comparable_search"],
                keywords=["market", "trend", "comparable", "comp", "area", "neighborhood"],
                avg_response_time_ms=600,
                success_rate=0.87,
                specializations=["market_trends", "demographics", "economic_indicators"]
            ),
            AgentCapability(
                agent_id="tax_strategy_agent",
                platform=Platform.REAL_ESTATE,
                capabilities=["tax_optimization", "1031_exchange", "depreciation"],
                keywords=["tax", "1031", "depreciation", "deduction", "cost segregation"],
                avg_response_time_ms=500,
                success_rate=0.93,
                specializations=["cost_seg", "opportunity_zones", "reps_status"]
            ),
        ]

        # Bond.AI Platform Agents
        bond_ai_agents = [
            AgentCapability(
                agent_id="connection_analyzer",
                platform=Platform.BOND_AI,
                capabilities=["network_analysis", "relationship_scoring", "path_finding"],
                keywords=["connection", "network", "relationship", "introduction", "mutual"],
                avg_response_time_ms=200,
                success_rate=0.91,
                specializations=["graph_analysis", "influence_scoring"]
            ),
            AgentCapability(
                agent_id="opportunity_matcher",
                platform=Platform.BOND_AI,
                capabilities=["matching", "recommendation", "compatibility"],
                keywords=["match", "opportunity", "recommendation", "fit", "compatible"],
                avg_response_time_ms=300,
                success_rate=0.86,
                specializations=["job_matching", "investor_matching", "mentor_matching"]
            ),
            AgentCapability(
                agent_id="message_composer",
                platform=Platform.BOND_AI,
                capabilities=["personalization", "template_generation", "tone_adjustment"],
                keywords=["message", "email", "outreach", "template", "personalize"],
                avg_response_time_ms=400,
                success_rate=0.89,
                specializations=["cold_outreach", "follow_up", "introduction"]
            ),
        ]

        # Labor Platform Agents
        labor_agents = [
            AgentCapability(
                agent_id="skill_analyzer",
                platform=Platform.LABOR,
                capabilities=["skill_assessment", "gap_analysis", "learning_path"],
                keywords=["skill", "competency", "gap", "learn", "upskill", "reskill"],
                avg_response_time_ms=350,
                success_rate=0.88,
                specializations=["technical_skills", "soft_skills", "certifications"]
            ),
            AgentCapability(
                agent_id="career_advisor",
                platform=Platform.LABOR,
                capabilities=["career_planning", "job_search", "salary_analysis"],
                keywords=["career", "job", "salary", "promotion", "transition", "growth"],
                avg_response_time_ms=450,
                success_rate=0.84,
                specializations=["career_paths", "market_demand", "compensation"]
            ),
            AgentCapability(
                agent_id="resume_optimizer",
                platform=Platform.LABOR,
                capabilities=["resume_analysis", "ats_optimization", "keyword_extraction"],
                keywords=["resume", "cv", "ats", "keywords", "experience", "achievements"],
                avg_response_time_ms=500,
                success_rate=0.90,
                specializations=["ats_systems", "keyword_density", "impact_statements"]
            ),
        ]

        # Register all agents
        for agent in finance_agents + real_estate_agents + bond_ai_agents + labor_agents:
            self.agent_registry[agent.agent_id] = agent

    async def route_query(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> RoutingDecision:
        """
        Route a query to the appropriate agents.

        Args:
            query: The user's query
            context: Additional context (user preferences, history, etc.)

        Returns:
            RoutingDecision with selected agents and platforms
        """

        # Classify intent
        intent, intent_confidence = self._classify_intent(query)

        # Find matching agents
        matching_agents = self._find_matching_agents(query, intent)

        # Determine primary and secondary platforms
        primary_platform, secondary_platforms = self._determine_platforms(matching_agents)

        # Select optimal agents based on performance
        selected_agents = self._select_optimal_agents(matching_agents, context)

        # Calculate estimated latency
        estimated_latency = self._estimate_latency(selected_agents)

        # Generate reasoning
        reasoning = self._generate_routing_reasoning(
            query, intent, selected_agents, primary_platform
        )

        decision = RoutingDecision(
            query_id=f"route_{datetime.now().timestamp()}",
            primary_platform=primary_platform,
            secondary_platforms=secondary_platforms,
            required_agents=[a.agent_id for a in selected_agents],
            confidence=intent_confidence,
            reasoning=reasoning,
            estimated_latency_ms=estimated_latency,
            fallback_agents=self._get_fallback_agents(selected_agents)
        )

        # Log routing decision
        self.routing_history.append({
            "query": query,
            "decision": decision,
            "timestamp": datetime.now().isoformat()
        })

        return decision

    def _classify_intent(self, query: str) -> Tuple[QueryIntent, float]:
        """Classify query intent"""

        query_lower = query.lower()

        # Intent patterns
        intent_patterns = {
            QueryIntent.FINANCIAL_ANALYSIS: [
                r"portfolio", r"investment", r"stock", r"bond", r"return",
                r"risk", r"allocation", r"performance"
            ],
            QueryIntent.MARKET_INTELLIGENCE: [
                r"market", r"trend", r"forecast", r"predict", r"outlook",
                r"analysis", r"intelligence"
            ],
            QueryIntent.PROPERTY_SEARCH: [
                r"property", r"real estate", r"house", r"apartment",
                r"commercial", r"cap rate", r"roi"
            ],
            QueryIntent.CAREER_GUIDANCE: [
                r"career", r"job", r"skill", r"resume", r"interview",
                r"salary", r"promotion"
            ],
            QueryIntent.NETWORKING: [
                r"connect", r"network", r"introduction", r"relationship",
                r"outreach", r"contact"
            ],
            QueryIntent.RISK_ASSESSMENT: [
                r"risk", r"exposure", r"hedge", r"protect", r"downside",
                r"volatility"
            ],
            QueryIntent.INVESTMENT_OPPORTUNITY: [
                r"opportunity", r"arbitrage", r"deal", r"undervalued",
                r"potential"
            ],
            QueryIntent.DOCUMENT_PROCESSING: [
                r"document", r"contract", r"extract", r"analyze", r"pdf",
                r"report"
            ],
            QueryIntent.LEARNING: [
                r"learn", r"course", r"training", r"education", r"certification"
            ],
            QueryIntent.AUTOMATION: [
                r"automate", r"schedule", r"recurring", r"workflow", r"trigger"
            ]
        }

        # Score each intent
        scores = {}
        for intent, patterns in intent_patterns.items():
            score = sum(1 for p in patterns if re.search(p, query_lower))
            if score > 0:
                scores[intent] = score

        if not scores:
            return QueryIntent.FINANCIAL_ANALYSIS, 0.5

        # Get highest scoring intent
        best_intent = max(scores, key=scores.get)
        confidence = min(scores[best_intent] / 3, 1.0)  # Normalize to 0-1

        return best_intent, confidence

    def _find_matching_agents(
        self,
        query: str,
        intent: QueryIntent
    ) -> List[AgentCapability]:
        """Find agents matching the query"""

        query_lower = query.lower()
        matching = []

        for agent in self.agent_registry.values():
            # Check keyword matches
            keyword_matches = sum(
                1 for kw in agent.keywords
                if kw in query_lower
            )

            if keyword_matches > 0:
                matching.append((agent, keyword_matches))

        # Sort by match count
        matching.sort(key=lambda x: x[1], reverse=True)

        return [agent for agent, _ in matching]

    def _determine_platforms(
        self,
        agents: List[AgentCapability]
    ) -> Tuple[Platform, List[Platform]]:
        """Determine primary and secondary platforms"""

        if not agents:
            return Platform.FINANCE, []

        # Count agents per platform
        platform_counts = {}
        for agent in agents:
            platform_counts[agent.platform] = platform_counts.get(agent.platform, 0) + 1

        # Sort by count
        sorted_platforms = sorted(
            platform_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )

        primary = sorted_platforms[0][0]
        secondary = [p for p, _ in sorted_platforms[1:]]

        return primary, secondary

    def _select_optimal_agents(
        self,
        matching_agents: List[AgentCapability],
        context: Optional[Dict[str, Any]]
    ) -> List[AgentCapability]:
        """Select optimal agents based on performance metrics"""

        if not matching_agents:
            return []

        # Score agents by success rate and response time
        scored = []
        for agent in matching_agents:
            # Higher success rate and lower response time = better score
            score = agent.success_rate * 100 - agent.avg_response_time_ms / 100
            scored.append((agent, score))

        # Sort by score
        scored.sort(key=lambda x: x[1], reverse=True)

        # Return top 5 agents
        return [agent for agent, _ in scored[:5]]

    def _estimate_latency(self, agents: List[AgentCapability]) -> int:
        """Estimate total latency for selected agents"""

        if not agents:
            return 0

        # Parallel execution - take max latency
        return max(agent.avg_response_time_ms for agent in agents)

    def _generate_routing_reasoning(
        self,
        query: str,
        intent: QueryIntent,
        agents: List[AgentCapability],
        primary_platform: Platform
    ) -> str:
        """Generate explanation for routing decision"""

        agent_names = ", ".join(a.agent_id for a in agents[:3])

        return (
            f"Query classified as {intent.value} with primary platform {primary_platform.value}. "
            f"Selected agents: {agent_names}. "
            f"Routing based on keyword matching and historical performance metrics."
        )

    def _get_fallback_agents(
        self,
        selected_agents: List[AgentCapability]
    ) -> List[str]:
        """Get fallback agents if primary agents fail"""

        selected_ids = {a.agent_id for a in selected_agents}
        fallbacks = []

        for agent in self.agent_registry.values():
            if agent.agent_id not in selected_ids:
                fallbacks.append(agent.agent_id)
                if len(fallbacks) >= 3:
                    break

        return fallbacks

    def get_agent_stats(self) -> Dict[str, Any]:
        """Get routing statistics"""

        return {
            "total_agents": len(self.agent_registry),
            "agents_by_platform": self._count_by_platform(),
            "total_routes": len(self.routing_history),
            "avg_confidence": self._avg_confidence()
        }

    def _count_by_platform(self) -> Dict[str, int]:
        """Count agents by platform"""
        counts = {}
        for agent in self.agent_registry.values():
            platform = agent.platform.value
            counts[platform] = counts.get(platform, 0) + 1
        return counts

    def _avg_confidence(self) -> float:
        """Calculate average routing confidence"""
        if not self.routing_history:
            return 0.0
        total = sum(r["decision"].confidence for r in self.routing_history)
        return total / len(self.routing_history)
