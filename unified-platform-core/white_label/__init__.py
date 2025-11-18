"""
White-Label Platform Infrastructure

Enables partners to resell the platform under their own brand:

Features:
- Custom branding (logos, colors, domains)
- Isolated tenant environments
- Custom feature sets per partner
- Revenue sharing/billing
- Partner analytics

Use Cases:
- Real estate brokerages white-labeling property tools
- HR companies white-labeling learning platform
- Financial advisors white-labeling analytics
- Consultancies white-labeling legacy modernization

Revenue Potential: $8M+ ARR from partner channel
"""

__version__ = "1.0.0"

from .tenant_manager import TenantManager, Tenant, TenantConfig
from .branding import BrandingManager, BrandTheme, ColorPalette, Typography
from .feature_flags import FeatureFlagManager, FeatureFlag, create_default_flags
from .partner_billing import PartnerBillingManager, Subscription, Invoice, Payout
from .domain_manager import DomainManager, DomainConfig

__all__ = [
    "TenantManager",
    "Tenant",
    "TenantConfig",
    "BrandingManager",
    "BrandTheme",
    "ColorPalette",
    "Typography",
    "FeatureFlagManager",
    "FeatureFlag",
    "create_default_flags",
    "PartnerBillingManager",
    "Subscription",
    "Invoice",
    "Payout",
    "DomainManager",
    "DomainConfig"
]
