"""
Property Data Integrations

Note: Most property data APIs require paid subscriptions.
These integrations provide the framework but will gracefully skip if not configured.
"""

from .attom import AttomDataIntegration
from .realtor import RealtorIntegration

__all__ = [
    "AttomDataIntegration",
    "RealtorIntegration",
]
