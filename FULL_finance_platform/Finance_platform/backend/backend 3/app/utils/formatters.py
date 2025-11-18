"""Formatting utilities."""

from decimal import Decimal
from typing import Optional


def format_currency(value: Optional[Decimal], decimals: int = 2) -> str:
    """Format value as currency."""
    if value is None:
        return "$0.00"
    return f"${value:,.{decimals}f}"


def format_percentage(value: Optional[Decimal], decimals: int = 2) -> str:
    """Format value as percentage."""
    if value is None:
        return "0.00%"
    return f"{value * 100:.{decimals}f}%"


def format_number(value: Optional[Decimal], decimals: int = 2) -> str:
    """Format number with thousand separators."""
    if value is None:
        return "0"
    return f"{value:,.{decimals}f}"
