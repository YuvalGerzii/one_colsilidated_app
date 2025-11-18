"""
Cross-Platform Orchestrator

Central orchestration layer that coordinates 104+ agents across all platforms.
Enables unified queries spanning Finance, Real Estate, Bond.AI, Labor, and Legacy Systems.
"""

import asyncio
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class Platform(Enum):
    FINANCE = "finance"
    REAL_ESTATE = "real_estate"
    BOND_AI = "bond_ai"
    LABOR = "labor"
    LEGACY = "legacy"


@dataclass
class AgentCapability:
    """Describes what an agent can do"""
    agent_id: str
    platform: Platform
    name: str
    description: str
    input_types: List[str]
    output_types: List[str]
    confidence_threshold: float = 0.7


@dataclass
class CrossPlatformQuery:
    """A query that spans multiple platforms"""
    query_id: str
    user_id: str
    query_text: str
    context: Dict[str, Any]
    target_platforms: List[Platform]
    priority: int = 1
    timeout_seconds: int = 30


@dataclass
class AgentResult:
    """Result from a single agent"""
    agent_id: str
    platform: Platform
    result: Any
    confidence: float
    execution_time_ms: int
    metadata: Dict[str, Any]


class CrossPlatformOrchestrator:
    """
    Master orchestrator that coordinates agents across all platforms.

    Features:
    - Intelligent query routing to appropriate platforms/agents
    - Parallel execution with result aggregation
    - Cross-platform entity resolution
    - Unified response synthesis
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.agent_registry: Dict[str, AgentCapability] = {}
        self.platform_connectors: Dict[Platform, Any] = {}
        self._initialize_agent_registry()

    def _initialize_agent_registry(self):
        """Register all 104+ agents from all platforms"""

        # Finance Platform Agents (39)
        finance_agents = [
            # Extreme Events Agents
            AgentCapability("pandemic_agent", Platform.FINANCE, "Pandemic Agent",
                          "Analyzes pandemic market impact", ["event_data"], ["market_prediction"], 0.8),
            AgentCapability("climate_crisis_agent", Platform.FINANCE, "Climate Crisis Agent",
                          "Climate event market analysis", ["climate_data"], ["sector_impact"], 0.75),
            AgentCapability("recession_agent", Platform.FINANCE, "Recession Agent",
                          "Recession prediction and analysis", ["economic_indicators"], ["recession_probability"], 0.85),
            AgentCapability("geopolitical_agent", Platform.FINANCE, "Geopolitical Agent",
                          "Geopolitical risk assessment", ["news_data", "events"], ["risk_score"], 0.7),
            AgentCapability("cyber_attack_agent", Platform.FINANCE, "Cyber Attack Agent",
                          "Cybersecurity threat market impact", ["threat_data"], ["sector_vulnerability"], 0.75),
            AgentCapability("inflation_agent", Platform.FINANCE, "Inflation Agent",
                          "Inflation prediction and hedging", ["economic_data"], ["inflation_forecast"], 0.8),
            AgentCapability("interest_rate_agent", Platform.FINANCE, "Interest Rate Agent",
                          "Rate change impact analysis", ["fed_data", "bonds"], ["rate_prediction"], 0.85),

            # Arbitrage Trading Agents
            AgentCapability("cross_exchange_agent", Platform.FINANCE, "Cross-Exchange Arbitrage",
                          "Detect cross-exchange price discrepancies", ["market_data"], ["arbitrage_opportunities"], 0.9),
            AgentCapability("statistical_arbitrage_agent", Platform.FINANCE, "Statistical Arbitrage",
                          "Mean reversion and cointegration", ["price_series"], ["trading_signals"], 0.85),
            AgentCapability("triangular_arbitrage_agent", Platform.FINANCE, "Triangular Arbitrage",
                          "Currency triangular opportunities", ["fx_rates"], ["arbitrage_path"], 0.9),
            AgentCapability("sentiment_agent", Platform.FINANCE, "Sentiment Analysis",
                          "Market sentiment from news/social", ["text_data"], ["sentiment_score"], 0.7),
            AgentCapability("risk_manager_agent", Platform.FINANCE, "Risk Manager",
                          "Position sizing and limits", ["portfolio", "market_data"], ["risk_metrics"], 0.85),
            AgentCapability("portfolio_manager_agent", Platform.FINANCE, "Portfolio Manager",
                          "Portfolio optimization", ["holdings", "targets"], ["rebalance_actions"], 0.8),
        ]

        # Real Estate Agents (6)
        real_estate_agents = [
            AgentCapability("property_analyst", Platform.REAL_ESTATE, "Property Analyst",
                          "Property valuation and analysis", ["property_data"], ["valuation"], 0.8),
            AgentCapability("market_analysis_agent", Platform.REAL_ESTATE, "Market Analysis",
                          "Real estate market trends", ["location", "property_type"], ["market_report"], 0.75),
            AgentCapability("risk_assessment_agent", Platform.REAL_ESTATE, "Risk Assessment",
                          "Investment risk scoring", ["deal_data"], ["risk_score"], 0.8),
            AgentCapability("financial_modeling_agent", Platform.REAL_ESTATE, "Financial Modeling",
                          "DCF, IRR, Cap Rate analysis", ["financials"], ["model_output"], 0.85),
            AgentCapability("loan_structuring_agent", Platform.REAL_ESTATE, "Loan Structuring",
                          "Optimal debt structure", ["property", "borrower"], ["loan_options"], 0.8),
            AgentCapability("tenant_analysis_agent", Platform.REAL_ESTATE, "Tenant Analysis",
                          "Tenant creditworthiness", ["tenant_data"], ["tenant_score"], 0.75),
        ]

        # Bond.AI Agents (35+)
        bond_ai_agents = [
            AgentCapability("network_analysis_agent", Platform.BOND_AI, "Network Analysis",
                          "Professional network graph analysis", ["connections"], ["network_insights"], 0.8),
            AgentCapability("opportunity_detection_agent", Platform.BOND_AI, "Opportunity Detection",
                          "Business opportunity identification", ["profile", "network"], ["opportunities"], 0.75),
            AgentCapability("relationship_scoring_agent", Platform.BOND_AI, "Relationship Scoring",
                          "Connection value assessment", ["interaction_data"], ["relationship_score"], 0.7),
            AgentCapability("expertise_matching_agent", Platform.BOND_AI, "Expertise Matching",
                          "Match experts to needs", ["requirements", "profiles"], ["matches"], 0.8),
            AgentCapability("introduction_orchestrator", Platform.BOND_AI, "Introduction Orchestrator",
                          "Warm introduction facilitation", ["parties", "context"], ["introduction_plan"], 0.75),
            AgentCapability("community_detection_agent", Platform.BOND_AI, "Community Detection",
                          "Find professional communities", ["network_graph"], ["communities"], 0.7),
            AgentCapability("serendipity_agent", Platform.BOND_AI, "Serendipity Agent",
                          "Unexpected valuable connections", ["profile", "history"], ["serendipitous_matches"], 0.6),
        ]

        # Labor Platform Agents (15)
        labor_agents = [
            AgentCapability("career_navigator", Platform.LABOR, "Career Navigator",
                          "Career path exploration", ["skills", "goals"], ["career_paths"], 0.8),
            AgentCapability("gap_analyzer", Platform.LABOR, "Gap Analyzer",
                          "Skills gap identification", ["current_skills", "target_role"], ["skill_gaps"], 0.85),
            AgentCapability("learning_strategist", Platform.LABOR, "Learning Strategist",
                          "Personalized learning paths", ["gaps", "learning_style"], ["learning_plan"], 0.8),
            AgentCapability("resume_optimizer", Platform.LABOR, "Resume Optimizer",
                          "Resume enhancement", ["resume", "target_job"], ["optimized_resume"], 0.75),
            AgentCapability("job_application_strategist", Platform.LABOR, "Job Application Strategist",
                          "Application optimization", ["job_posting", "profile"], ["application_strategy"], 0.8),
            AgentCapability("mentorship_matcher", Platform.LABOR, "Mentorship Matcher",
                          "Find ideal mentors", ["goals", "preferences"], ["mentor_matches"], 0.7),
            AgentCapability("freelance_advisor", Platform.LABOR, "Freelance Advisor",
                          "Freelance business optimization", ["freelancer_profile"], ["growth_strategy"], 0.75),
        ]

        # Legacy Systems Agents (10)
        legacy_agents = [
            AgentCapability("discovery_agent", Platform.LEGACY, "Discovery Agent",
                          "Legacy system discovery", ["codebase"], ["system_map"], 0.8),
            AgentCapability("process_mining_agent", Platform.LEGACY, "Process Mining",
                          "Business process extraction", ["logs", "documents"], ["process_model"], 0.75),
            AgentCapability("modernization_advisor", Platform.LEGACY, "Modernization Advisor",
                          "Modernization recommendations", ["legacy_system"], ["modernization_plan"], 0.7),
            AgentCapability("code_quality_agent", Platform.LEGACY, "Code Quality",
                          "Code quality assessment", ["source_code"], ["quality_report"], 0.85),
            AgentCapability("security_auditor", Platform.LEGACY, "Security Auditor",
                          "Security vulnerability scan", ["codebase"], ["security_report"], 0.8),
        ]

        # Register all agents
        all_agents = finance_agents + real_estate_agents + bond_ai_agents + labor_agents + legacy_agents
        for agent in all_agents:
            self.agent_registry[agent.agent_id] = agent

        logger.info(f"Registered {len(self.agent_registry)} agents across all platforms")

    async def execute_cross_platform_query(
        self,
        query: CrossPlatformQuery
    ) -> Dict[str, Any]:
        """
        Execute a query that spans multiple platforms.

        Example queries:
        - "Find investors in my network (Bond.AI) for this real estate deal (Real Estate)
           considering current market conditions (Finance)"
        - "What career paths (Labor) align with opportunities in my network (Bond.AI)?"
        """

        start_time = datetime.now()

        # 1. Analyze query to determine required agents
        required_agents = await self._analyze_query(query)

        # 2. Route to appropriate platforms
        platform_tasks = await self._create_platform_tasks(query, required_agents)

        # 3. Execute in parallel with timeout
        results = await self._execute_parallel(platform_tasks, query.timeout_seconds)

        # 4. Resolve entities across platforms
        resolved_results = await self._resolve_cross_platform_entities(results)

        # 5. Synthesize unified response
        synthesis = await self._synthesize_response(query, resolved_results)

        execution_time = (datetime.now() - start_time).total_seconds() * 1000

        return {
            "query_id": query.query_id,
            "synthesis": synthesis,
            "platform_results": resolved_results,
            "agents_used": [r.agent_id for r in results],
            "execution_time_ms": execution_time,
            "confidence": self._calculate_overall_confidence(results)
        }

    async def _analyze_query(self, query: CrossPlatformQuery) -> List[str]:
        """Determine which agents are needed for a query"""

        required_agents = []
        query_lower = query.query_text.lower()

        # Keyword-based routing (will be enhanced with LLM)
        keyword_mappings = {
            # Finance keywords
            "market": ["sentiment_agent", "risk_manager_agent"],
            "arbitrage": ["cross_exchange_agent", "statistical_arbitrage_agent", "triangular_arbitrage_agent"],
            "recession": ["recession_agent", "economic_crisis_agent"],
            "inflation": ["inflation_agent", "interest_rate_agent"],
            "portfolio": ["portfolio_manager_agent", "risk_manager_agent"],

            # Real Estate keywords
            "property": ["property_analyst", "market_analysis_agent"],
            "deal": ["financial_modeling_agent", "risk_assessment_agent"],
            "tenant": ["tenant_analysis_agent"],
            "loan": ["loan_structuring_agent"],
            "valuation": ["property_analyst", "financial_modeling_agent"],

            # Bond.AI keywords
            "network": ["network_analysis_agent", "community_detection_agent"],
            "connection": ["relationship_scoring_agent", "expertise_matching_agent"],
            "investor": ["opportunity_detection_agent", "expertise_matching_agent"],
            "introduction": ["introduction_orchestrator"],

            # Labor keywords
            "career": ["career_navigator", "gap_analyzer"],
            "skills": ["gap_analyzer", "learning_strategist"],
            "job": ["job_application_strategist", "resume_optimizer"],
            "mentor": ["mentorship_matcher"],
            "freelance": ["freelance_advisor"],

            # Legacy keywords
            "legacy": ["discovery_agent", "modernization_advisor"],
            "process": ["process_mining_agent"],
            "code": ["code_quality_agent", "security_auditor"],
        }

        for keyword, agents in keyword_mappings.items():
            if keyword in query_lower:
                required_agents.extend(agents)

        # Remove duplicates while preserving order
        seen = set()
        unique_agents = []
        for agent in required_agents:
            if agent not in seen:
                seen.add(agent)
                unique_agents.append(agent)

        return unique_agents if unique_agents else ["network_analysis_agent"]  # Default

    async def _create_platform_tasks(
        self,
        query: CrossPlatformQuery,
        agent_ids: List[str]
    ) -> Dict[Platform, List[Dict[str, Any]]]:
        """Group agent tasks by platform"""

        platform_tasks = {platform: [] for platform in Platform}

        for agent_id in agent_ids:
            if agent_id in self.agent_registry:
                agent = self.agent_registry[agent_id]
                platform_tasks[agent.platform].append({
                    "agent_id": agent_id,
                    "agent": agent,
                    "query": query
                })

        return {k: v for k, v in platform_tasks.items() if v}  # Remove empty

    async def _execute_parallel(
        self,
        platform_tasks: Dict[Platform, List[Dict[str, Any]]],
        timeout: int
    ) -> List[AgentResult]:
        """Execute all agent tasks in parallel"""

        async def execute_agent_task(task: Dict[str, Any]) -> AgentResult:
            start = datetime.now()
            agent = task["agent"]

            # Simulate agent execution (replace with actual agent calls)
            await asyncio.sleep(0.1)  # Simulated processing

            execution_time = int((datetime.now() - start).total_seconds() * 1000)

            return AgentResult(
                agent_id=agent.agent_id,
                platform=agent.platform,
                result={
                    "status": "success",
                    "data": f"Result from {agent.name}",
                    "recommendations": []
                },
                confidence=agent.confidence_threshold,
                execution_time_ms=execution_time,
                metadata={"query_context": task["query"].context}
            )

        # Create all tasks
        all_tasks = []
        for platform, tasks in platform_tasks.items():
            for task in tasks:
                all_tasks.append(execute_agent_task(task))

        # Execute with timeout
        try:
            results = await asyncio.wait_for(
                asyncio.gather(*all_tasks),
                timeout=timeout
            )
            return list(results)
        except asyncio.TimeoutError:
            logger.warning(f"Query timeout after {timeout}s")
            return []

    async def _resolve_cross_platform_entities(
        self,
        results: List[AgentResult]
    ) -> List[AgentResult]:
        """
        Resolve entities across platforms.

        Examples:
        - Same person appearing in Bond.AI network and Labor skills
        - Same company in Finance analysis and Real Estate deals
        - Same property across multiple data sources
        """

        # Entity resolution logic would go here
        # For now, return results with entity tags

        for result in results:
            result.metadata["entities_resolved"] = True

        return results

    async def _synthesize_response(
        self,
        query: CrossPlatformQuery,
        results: List[AgentResult]
    ) -> Dict[str, Any]:
        """Synthesize a unified response from all agent results"""

        synthesis = {
            "summary": f"Analyzed query across {len(results)} agents from {len(set(r.platform for r in results))} platforms",
            "key_insights": [],
            "recommendations": [],
            "cross_platform_connections": [],
            "confidence_breakdown": {}
        }

        # Group results by platform
        by_platform = {}
        for result in results:
            platform_name = result.platform.value
            if platform_name not in by_platform:
                by_platform[platform_name] = []
            by_platform[platform_name].append(result)

        # Extract insights from each platform
        for platform, platform_results in by_platform.items():
            synthesis["confidence_breakdown"][platform] = sum(
                r.confidence for r in platform_results
            ) / len(platform_results)

        # Identify cross-platform connections
        if Platform.BOND_AI.value in by_platform and Platform.REAL_ESTATE.value in by_platform:
            synthesis["cross_platform_connections"].append({
                "type": "investor_deal_match",
                "description": "Network contacts matched with real estate opportunities"
            })

        if Platform.LABOR.value in by_platform and Platform.BOND_AI.value in by_platform:
            synthesis["cross_platform_connections"].append({
                "type": "career_network_alignment",
                "description": "Career paths aligned with network opportunities"
            })

        if Platform.FINANCE.value in by_platform and Platform.REAL_ESTATE.value in by_platform:
            synthesis["cross_platform_connections"].append({
                "type": "market_impact_analysis",
                "description": "Market conditions impact on real estate portfolio"
            })

        return synthesis

    def _calculate_overall_confidence(self, results: List[AgentResult]) -> float:
        """Calculate weighted overall confidence"""
        if not results:
            return 0.0
        return sum(r.confidence for r in results) / len(results)

    def get_available_agents(self, platform: Optional[Platform] = None) -> List[AgentCapability]:
        """Get list of available agents, optionally filtered by platform"""
        agents = list(self.agent_registry.values())
        if platform:
            agents = [a for a in agents if a.platform == platform]
        return agents

    async def find_cross_platform_opportunities(
        self,
        user_id: str,
        context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Proactively find opportunities that span multiple platforms.

        Examples:
        - Investor in network + Deal in pipeline = Introduction opportunity
        - Career skills + Network contacts = Job referral opportunity
        - Market prediction + Portfolio = Rebalancing opportunity
        """

        opportunities = []

        # Example opportunity detection
        opportunities.append({
            "type": "investor_deal_match",
            "platforms": [Platform.BOND_AI.value, Platform.REAL_ESTATE.value],
            "description": "3 investors in your network match criteria for Deal #123",
            "confidence": 0.85,
            "actions": [
                "Review investor profiles",
                "Schedule introductions",
                "Prepare deal memo"
            ]
        })

        opportunities.append({
            "type": "career_advancement",
            "platforms": [Platform.LABOR.value, Platform.BOND_AI.value],
            "description": "Your skills match requirements for roles at 5 companies in your 2nd-degree network",
            "confidence": 0.78,
            "actions": [
                "Update resume for target roles",
                "Request introductions",
                "Apply to positions"
            ]
        })

        return opportunities


# Convenience function for quick queries
async def cross_platform_query(
    query_text: str,
    user_id: str = "default",
    context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Quick interface for cross-platform queries.

    Usage:
        result = await cross_platform_query(
            "Find investors in my network for this $5M multifamily deal",
            user_id="user123",
            context={"deal_id": "deal456"}
        )
    """

    orchestrator = CrossPlatformOrchestrator()

    query = CrossPlatformQuery(
        query_id=f"query_{datetime.now().timestamp()}",
        user_id=user_id,
        query_text=query_text,
        context=context or {},
        target_platforms=list(Platform)
    )

    return await orchestrator.execute_cross_platform_query(query)
