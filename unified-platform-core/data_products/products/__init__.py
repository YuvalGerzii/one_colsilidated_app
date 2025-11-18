"""
Data Products

Monetizable data products from all platforms.
"""

from .finance_data_products import (
    ExtremeEventsAlertsAPI,
    MarketRegimeIndicators,
    ArbitrageSignalsFeed,
    create_finance_data_products_router
)

from .real_estate_data_products import (
    PropertyValuationAPI,
    MarketIntelligenceFeed,
    DealFlowAlertsAPI,
    create_real_estate_data_products_router
)

from .labor_data_products import (
    SkillDemandForecastsAPI,
    SalaryIntelligenceAPI,
    WorkforceAnalyticsAPI,
    create_labor_data_products_router
)

__all__ = [
    # Finance
    "ExtremeEventsAlertsAPI",
    "MarketRegimeIndicators",
    "ArbitrageSignalsFeed",
    "create_finance_data_products_router",

    # Real Estate
    "PropertyValuationAPI",
    "MarketIntelligenceFeed",
    "DealFlowAlertsAPI",
    "create_real_estate_data_products_router",

    # Labor
    "SkillDemandForecastsAPI",
    "SalaryIntelligenceAPI",
    "WorkforceAnalyticsAPI",
    "create_labor_data_products_router",
]
