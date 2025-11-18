"""
Unified Platform Core

Enterprise-grade components for cross-platform intelligence,
autonomous agents, data products, and white-label infrastructure.

Revenue Potential: $290M+ ARR
"""

__version__ = "1.0.0"

# Cross-Platform Intelligence
from .cross_platform_intelligence import (
    CrossPlatformOrchestrator,
    UnifiedEntityResolver,
    IntelligentQueryRouter,
    CrossPlatformKnowledgeGraph
)

# Autonomous Agents
from .autonomous_agents import (
    BaseAutonomousAgent,
    AgentAction,
    ActionResult,
    AgentConfig,
    TradingExecutionAgent,
    OutreachAgent,
    PropertyScoutAgent,
    JobApplicationAgent,
    AgentSupervisor,
    create_agent_supervisor
)

# Data Products
from .data_products import (
    UsageMetering,
    PricingTier,
    DataProductGateway,
    # Finance Products
    ExtremeEventsAlertsAPI,
    MarketRegimeIndicators,
    ArbitrageSignalsFeed,
    # Real Estate Products
    PropertyValuationAPI,
    MarketIntelligenceFeed,
    DealFlowAlertsAPI,
    # Labor Products
    SkillDemandForecastsAPI,
    SalaryIntelligenceAPI,
    WorkforceAnalyticsAPI
)

# White-Label Platform
from .white_label import (
    TenantManager,
    TenantConfig,
    BrandingManager,
    BrandTheme,
    FeatureFlagManager,
    PartnerBillingManager,
    DomainManager
)

__all__ = [
    # Version
    "__version__",

    # Cross-Platform Intelligence
    "CrossPlatformOrchestrator",
    "UnifiedEntityResolver",
    "IntelligentQueryRouter",
    "CrossPlatformKnowledgeGraph",

    # Autonomous Agents
    "BaseAutonomousAgent",
    "AgentAction",
    "ActionResult",
    "AgentConfig",
    "TradingExecutionAgent",
    "OutreachAgent",
    "PropertyScoutAgent",
    "JobApplicationAgent",
    "AgentSupervisor",
    "create_agent_supervisor",

    # Data Products
    "UsageMetering",
    "PricingTier",
    "DataProductGateway",
    "ExtremeEventsAlertsAPI",
    "MarketRegimeIndicators",
    "ArbitrageSignalsFeed",
    "PropertyValuationAPI",
    "MarketIntelligenceFeed",
    "DealFlowAlertsAPI",
    "SkillDemandForecastsAPI",
    "SalaryIntelligenceAPI",
    "WorkforceAnalyticsAPI",

    # White-Label Platform
    "TenantManager",
    "TenantConfig",
    "BrandingManager",
    "BrandTheme",
    "FeatureFlagManager",
    "PartnerBillingManager",
    "DomainManager",
]
