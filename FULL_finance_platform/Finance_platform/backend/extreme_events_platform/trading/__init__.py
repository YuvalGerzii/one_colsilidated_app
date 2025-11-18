"""
Trading Module (V4.0)

Advanced trading strategies for extreme events based on 2025 market intelligence.

Modules:
- HedgeFundStrategyAnalyzer: Which hedge fund strategies work best for each event
- DerivativesStrategist: Options and derivatives recommendations
- ShortSellingDetector: Short selling opportunities
- FastActionOpportunities: Time-critical trades (0-24 hour windows)
- InstitutionalBehaviorAnalyzer: Follow smart money, fade retail
"""

from .hedge_fund_strategy_analyzer import (
    HedgeFundStrategyAnalyzer,
    HedgeFundStrategy,
    StrategyRecommendation
)

from .derivatives_strategist import (
    DerivativesStrategist,
    OptionsStrategy,
    OptionsRecommendation
)

from .short_selling_detector import (
    ShortSellingDetector,
    ShortStrategy,
    ShortOpportunity,
    PairTrade
)

from .fast_action_opportunities import (
    FastActionOpportunities,
    FastActionTrade,
    UrgencyLevel
)

from .institutional_behavior_analyzer import (
    InstitutionalBehaviorAnalyzer,
    InvestorType,
    BehaviorProfile,
    SmartMoneySignal
)

__all__ = [
    # Hedge fund strategies
    'HedgeFundStrategyAnalyzer',
    'HedgeFundStrategy',
    'StrategyRecommendation',

    # Derivatives and options
    'DerivativesStrategist',
    'OptionsStrategy',
    'OptionsRecommendation',

    # Short selling
    'ShortSellingDetector',
    'ShortStrategy',
    'ShortOpportunity',
    'PairTrade',

    # Fast action
    'FastActionOpportunities',
    'FastActionTrade',
    'UrgencyLevel',

    # Institutional behavior
    'InstitutionalBehaviorAnalyzer',
    'InvestorType',
    'BehaviorProfile',
    'SmartMoneySignal',
]
