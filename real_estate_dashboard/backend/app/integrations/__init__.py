"""
Third-Party Integrations Module

This module provides integrations with external services for:
- Property data
- Market data
- Accounting
- Banking
- Tools and automation

All integrations gracefully handle missing API keys and skip functionality when not configured.
"""

from .base import BaseIntegration, IntegrationStatus, IntegrationConfig
from .manager import IntegrationManager

__all__ = [
    "BaseIntegration",
    "IntegrationStatus",
    "IntegrationConfig",
    "IntegrationManager",
]
