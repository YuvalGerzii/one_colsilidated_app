"""
Helper utilities for the arbitrage trading system.
"""
from decimal import Decimal
from typing import List, Dict, Any
import json


def calculate_profit_percentage(
    buy_price: Decimal,
    sell_price: Decimal,
    fees: Decimal = Decimal(0)
) -> Decimal:
    """
    Calculate profit percentage.

    Args:
        buy_price: Purchase price
        sell_price: Selling price
        fees: Transaction fees

    Returns:
        Profit percentage
    """
    if buy_price == 0:
        return Decimal(0)

    profit = sell_price - buy_price - fees
    return (profit / buy_price) * Decimal(100)


def calculate_sharpe_ratio(
    returns: List[Decimal],
    risk_free_rate: Decimal = Decimal(0)
) -> Decimal:
    """
    Calculate Sharpe ratio.

    Args:
        returns: List of returns
        risk_free_rate: Risk-free rate of return

    Returns:
        Sharpe ratio
    """
    if not returns or len(returns) < 2:
        return Decimal(0)

    # Convert to float for numpy operations
    returns_float = [float(r) for r in returns]

    import numpy as np

    mean_return = Decimal(str(np.mean(returns_float)))
    std_return = Decimal(str(np.std(returns_float)))

    if std_return == 0:
        return Decimal(0)

    return (mean_return - risk_free_rate) / std_return


def format_currency(amount: Decimal, currency: str = "USD") -> str:
    """
    Format amount as currency.

    Args:
        amount: Amount to format
        currency: Currency symbol

    Returns:
        Formatted string
    """
    symbol_map = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥"
    }

    symbol = symbol_map.get(currency, currency)
    return f"{symbol}{float(amount):,.2f}"


def serialize_decimal(obj: Any) -> Any:
    """
    Serialize Decimal objects for JSON.

    Args:
        obj: Object to serialize

    Returns:
        Serializable object
    """
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, dict):
        return {k: serialize_decimal(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [serialize_decimal(item) for item in obj]
    return obj


def to_json(obj: Any, pretty: bool = False) -> str:
    """
    Convert object to JSON string.

    Args:
        obj: Object to convert
        pretty: Pretty print with indentation

    Returns:
        JSON string
    """
    serializable = serialize_decimal(obj)

    if pretty:
        return json.dumps(serializable, indent=2)
    return json.dumps(serializable)


def calculate_max_drawdown(equity_curve: List[Decimal]) -> Decimal:
    """
    Calculate maximum drawdown from equity curve.

    Args:
        equity_curve: List of equity values over time

    Returns:
        Maximum drawdown as percentage
    """
    if not equity_curve or len(equity_curve) < 2:
        return Decimal(0)

    max_drawdown = Decimal(0)
    peak = equity_curve[0]

    for value in equity_curve:
        if value > peak:
            peak = value

        drawdown = (peak - value) / peak if peak > 0 else Decimal(0)
        max_drawdown = max(max_drawdown, drawdown)

    return max_drawdown * Decimal(100)  # Return as percentage
