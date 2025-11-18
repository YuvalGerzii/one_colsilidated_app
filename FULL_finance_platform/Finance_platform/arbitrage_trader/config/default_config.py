"""
Default configuration for the arbitrage trading system.
"""

DEFAULT_CONFIG = {
    # Logging configuration
    "log_level": "INFO",

    # Market data configuration
    "market_data": {
        "update_interval_ms": 1000,  # Update every 1 second
    },

    # Exchanges and symbols to monitor
    "exchanges": {
        "binance": [
            "BTC/USDT",
            "ETH/USDT",
            "BTC/ETH",
            "SOL/USDT",
            "ETH/BTC"
        ],
        "coinbase": [
            "BTC/USD",
            "ETH/USD",
            "SOL/USD"
        ],
        "kraken": [
            "BTC/USD",
            "ETH/USD",
            "BTC/EUR",
            "ETH/EUR"
        ]
    },

    # Execution configuration
    "execution": {
        "fee_rate": "0.001",  # 0.1% trading fee
        "exchanges": ["binance", "coinbase", "kraken"]
    },

    # Agent configurations
    "agents": {
        # Risk manager configuration
        "risk_manager": {
            "max_position_size": "10000",
            "max_daily_loss": "1000",
            "max_total_exposure": "50000",
            "max_risk_score": "0.7"
        },

        # Cross-exchange arbitrage agent
        "cross_exchange": {
            "enabled": True,
            "min_spread_threshold": "0.001",  # 0.1% minimum spread
            "min_profit_threshold": "0.002",  # 0.2% minimum profit
            "min_confidence": "0.7",
            "max_risk": "0.5"
        },

        # Statistical arbitrage agent
        "statistical": {
            "enabled": True,
            "lookback_period": 20,  # Number of data points for calculations
            "z_score_entry_threshold": 2.0,  # Enter trade when z-score exceeds this
            "z_score_exit_threshold": 0.5,  # Exit when z-score returns to this level
            "correlation_threshold": 0.7,  # Minimum correlation for pairs
            "min_profit_threshold": "0.005",  # 0.5% minimum expected profit
            "min_confidence": "0.6",
            "max_risk": "0.6"
        },

        # Triangular arbitrage agent
        "triangular": {
            "enabled": True,
            "min_profit_threshold": "0.001",  # 0.1% minimum profit
            "min_confidence": "0.7",
            "max_risk": "0.5"
        }
    }
}


def get_config(custom_config: dict = None) -> dict:
    """
    Get configuration with optional custom overrides.

    Args:
        custom_config: Custom configuration to merge with defaults

    Returns:
        Merged configuration dictionary
    """
    config = DEFAULT_CONFIG.copy()

    if custom_config:
        # Deep merge custom config
        _deep_merge(config, custom_config)

    return config


def _deep_merge(base: dict, override: dict):
    """
    Deep merge override dictionary into base dictionary.

    Args:
        base: Base dictionary to merge into
        override: Override dictionary
    """
    for key, value in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value
