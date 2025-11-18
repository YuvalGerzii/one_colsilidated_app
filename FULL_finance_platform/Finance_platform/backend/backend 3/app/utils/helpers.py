"""Helper utility functions."""

from decimal import Decimal
from typing import List, Tuple
from datetime import date


def calculate_moic(invested: Decimal, current_value: Decimal) -> Decimal:
    """Calculate Multiple on Invested Capital."""
    if invested == 0:
        return Decimal(0)
    return current_value / invested


def calculate_irr(cash_flows: List[Tuple[date, Decimal]]) -> float:
    """
    Calculate Internal Rate of Return.
    
    Args:
        cash_flows: List of (date, amount) tuples
        
    Returns:
        IRR as decimal (e.g., 0.25 for 25%)
    """
    # Simplified IRR calculation
    # In production, use numpy.irr or scipy
    return 0.0  # Placeholder
