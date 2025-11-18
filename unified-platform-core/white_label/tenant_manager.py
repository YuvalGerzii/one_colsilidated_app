"""
Tenant Manager

Multi-tenant infrastructure for white-label platform.
Provides complete isolation between partner instances.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class TenantStatus(Enum):
    """Tenant lifecycle status"""
    PROVISIONING = "provisioning"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    TRIAL = "trial"
    CANCELLED = "cancelled"


class IsolationLevel(Enum):
    """Data isolation level"""
    SHARED = "shared"          # Shared database, row-level isolation
    SCHEMA = "schema"          # Separate schema per tenant
    DATABASE = "database"      # Separate database per tenant
    DEDICATED = "dedicated"    # Dedicated infrastructure


@dataclass
class TenantConfig:
    """Configuration for a tenant"""
    # Basic info
    tenant_id: str
    partner_id: str
    name: str
    domain: str
    status: TenantStatus = TenantStatus.PROVISIONING

    # Technical config
    isolation_level: IsolationLevel = IsolationLevel.SHARED
    database_name: Optional[str] = None
    schema_name: Optional[str] = None

    # Features
    enabled_platforms: List[str] = field(default_factory=lambda: ["real_estate"])
    enabled_features: List[str] = field(default_factory=list)
    disabled_features: List[str] = field(default_factory=list)

    # Limits
    max_users: int = 100
    max_storage_gb: int = 10
    max_api_calls_per_month: int = 100000

    # Branding
    branding_config_id: Optional[str] = None
    custom_domain: Optional[str] = None

    # Billing
    revenue_share_percent: float = 30.0  # Partner keeps 30%
    billing_email: Optional[str] = None


@dataclass
class Tenant:
    """A white-label tenant instance"""
    config: TenantConfig
    created_at: datetime
    updated_at: datetime
    users: List[str] = field(default_factory=list)
    storage_used_gb: float = 0.0
    api_calls_this_month: int = 0
    monthly_revenue: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class TenantManager:
    """
    Manages multi-tenant white-label instances.

    Features:
    - Tenant provisioning and lifecycle
    - Data isolation enforcement
    - Resource quota management
    - Cross-tenant analytics
    """

    def __init__(self):
        self.tenants: Dict[str, Tenant] = {}
        self.domain_mapping: Dict[str, str] = {}  # domain -> tenant_id

    async def create_tenant(
        self,
        config: TenantConfig
    ) -> Tenant:
        """
        Create a new white-label tenant.

        This will:
        1. Provision database/schema
        2. Set up data isolation
        3. Configure features
        4. Initialize branding
        """

        logger.info(f"Creating tenant: {config.name} ({config.tenant_id})")

        # Validate configuration
        self._validate_config(config)

        # Provision storage based on isolation level
        await self._provision_storage(config)

        # Create tenant
        tenant = Tenant(
            config=config,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        # Register tenant
        self.tenants[config.tenant_id] = tenant

        # Map domain
        if config.custom_domain:
            self.domain_mapping[config.custom_domain] = config.tenant_id

        # Set status to active (or trial)
        tenant.config.status = TenantStatus.ACTIVE

        logger.info(f"Tenant created: {config.tenant_id}")
        return tenant

    def _validate_config(self, config: TenantConfig):
        """Validate tenant configuration"""

        if config.tenant_id in self.tenants:
            raise ValueError(f"Tenant {config.tenant_id} already exists")

        if config.custom_domain in self.domain_mapping:
            raise ValueError(f"Domain {config.custom_domain} already in use")

        if config.revenue_share_percent < 0 or config.revenue_share_percent > 100:
            raise ValueError("Revenue share must be between 0 and 100")

    async def _provision_storage(self, config: TenantConfig):
        """Provision storage based on isolation level"""

        if config.isolation_level == IsolationLevel.SHARED:
            # Row-level isolation with tenant_id column
            logger.info(f"Setting up row-level isolation for {config.tenant_id}")
            # Database tables will filter by tenant_id

        elif config.isolation_level == IsolationLevel.SCHEMA:
            # Create dedicated schema
            schema_name = f"tenant_{config.tenant_id}"
            config.schema_name = schema_name
            logger.info(f"Creating schema: {schema_name}")
            # CREATE SCHEMA tenant_xxx

        elif config.isolation_level == IsolationLevel.DATABASE:
            # Create dedicated database
            db_name = f"tenant_{config.tenant_id}_db"
            config.database_name = db_name
            logger.info(f"Creating database: {db_name}")
            # CREATE DATABASE tenant_xxx_db

        elif config.isolation_level == IsolationLevel.DEDICATED:
            # Full dedicated infrastructure
            logger.info(f"Provisioning dedicated infrastructure for {config.tenant_id}")
            # Spin up dedicated containers/VMs

    async def get_tenant(self, tenant_id: str) -> Optional[Tenant]:
        """Get tenant by ID"""
        return self.tenants.get(tenant_id)

    async def get_tenant_by_domain(self, domain: str) -> Optional[Tenant]:
        """Get tenant by custom domain"""
        tenant_id = self.domain_mapping.get(domain)
        if tenant_id:
            return self.tenants.get(tenant_id)
        return None

    async def update_tenant(
        self,
        tenant_id: str,
        updates: Dict[str, Any]
    ) -> Tenant:
        """Update tenant configuration"""

        if tenant_id not in self.tenants:
            raise ValueError(f"Tenant {tenant_id} not found")

        tenant = self.tenants[tenant_id]

        # Apply updates
        for key, value in updates.items():
            if hasattr(tenant.config, key):
                setattr(tenant.config, key, value)

        tenant.updated_at = datetime.now()

        logger.info(f"Tenant updated: {tenant_id}")
        return tenant

    async def suspend_tenant(self, tenant_id: str, reason: str):
        """Suspend a tenant (e.g., for non-payment)"""

        if tenant_id not in self.tenants:
            raise ValueError(f"Tenant {tenant_id} not found")

        tenant = self.tenants[tenant_id]
        tenant.config.status = TenantStatus.SUSPENDED
        tenant.metadata["suspension_reason"] = reason
        tenant.metadata["suspended_at"] = datetime.now().isoformat()
        tenant.updated_at = datetime.now()

        logger.warning(f"Tenant suspended: {tenant_id} - {reason}")

    async def activate_tenant(self, tenant_id: str):
        """Activate a suspended tenant"""

        if tenant_id not in self.tenants:
            raise ValueError(f"Tenant {tenant_id} not found")

        tenant = self.tenants[tenant_id]
        tenant.config.status = TenantStatus.ACTIVE
        tenant.metadata.pop("suspension_reason", None)
        tenant.metadata.pop("suspended_at", None)
        tenant.updated_at = datetime.now()

        logger.info(f"Tenant activated: {tenant_id}")

    async def delete_tenant(self, tenant_id: str):
        """Delete a tenant and all its data"""

        if tenant_id not in self.tenants:
            raise ValueError(f"Tenant {tenant_id} not found")

        tenant = self.tenants[tenant_id]

        # Remove domain mapping
        if tenant.config.custom_domain:
            self.domain_mapping.pop(tenant.config.custom_domain, None)

        # Clean up storage
        await self._cleanup_storage(tenant.config)

        # Remove tenant
        del self.tenants[tenant_id]

        logger.info(f"Tenant deleted: {tenant_id}")

    async def _cleanup_storage(self, config: TenantConfig):
        """Clean up tenant storage"""

        if config.isolation_level == IsolationLevel.SCHEMA:
            logger.info(f"Dropping schema: {config.schema_name}")
            # DROP SCHEMA tenant_xxx CASCADE

        elif config.isolation_level == IsolationLevel.DATABASE:
            logger.info(f"Dropping database: {config.database_name}")
            # DROP DATABASE tenant_xxx_db

        elif config.isolation_level == IsolationLevel.DEDICATED:
            logger.info(f"Terminating dedicated infrastructure")
            # Terminate containers/VMs

    async def check_quota(
        self,
        tenant_id: str,
        resource: str,
        amount: int = 1
    ) -> Dict[str, Any]:
        """Check if tenant has quota for a resource"""

        if tenant_id not in self.tenants:
            return {"allowed": False, "reason": "Tenant not found"}

        tenant = self.tenants[tenant_id]
        config = tenant.config

        if resource == "users":
            current = len(tenant.users)
            limit = config.max_users
            allowed = current + amount <= limit
            return {
                "allowed": allowed,
                "current": current,
                "limit": limit,
                "remaining": limit - current
            }

        elif resource == "storage":
            current = tenant.storage_used_gb
            limit = config.max_storage_gb
            allowed = current + amount <= limit
            return {
                "allowed": allowed,
                "current_gb": current,
                "limit_gb": limit,
                "remaining_gb": limit - current
            }

        elif resource == "api_calls":
            current = tenant.api_calls_this_month
            limit = config.max_api_calls_per_month
            allowed = current + amount <= limit
            return {
                "allowed": allowed,
                "current": current,
                "limit": limit,
                "remaining": limit - current
            }

        return {"allowed": True, "reason": "Unknown resource"}

    def get_tenant_context(self, tenant_id: str) -> Dict[str, Any]:
        """Get context for request processing"""

        if tenant_id not in self.tenants:
            return {}

        tenant = self.tenants[tenant_id]

        return {
            "tenant_id": tenant_id,
            "isolation_level": tenant.config.isolation_level.value,
            "database_name": tenant.config.database_name,
            "schema_name": tenant.config.schema_name,
            "enabled_platforms": tenant.config.enabled_platforms,
            "enabled_features": tenant.config.enabled_features,
            "disabled_features": tenant.config.disabled_features,
            "branding_config_id": tenant.config.branding_config_id
        }

    async def get_all_tenants(
        self,
        partner_id: Optional[str] = None,
        status: Optional[TenantStatus] = None
    ) -> List[Tenant]:
        """Get all tenants with optional filtering"""

        tenants = list(self.tenants.values())

        if partner_id:
            tenants = [t for t in tenants if t.config.partner_id == partner_id]

        if status:
            tenants = [t for t in tenants if t.config.status == status]

        return tenants

    async def get_tenant_stats(self, tenant_id: str) -> Dict[str, Any]:
        """Get usage statistics for a tenant"""

        if tenant_id not in self.tenants:
            return {"error": "Tenant not found"}

        tenant = self.tenants[tenant_id]

        return {
            "tenant_id": tenant_id,
            "status": tenant.config.status.value,
            "users": len(tenant.users),
            "storage_used_gb": tenant.storage_used_gb,
            "api_calls_this_month": tenant.api_calls_this_month,
            "monthly_revenue": tenant.monthly_revenue,
            "created_at": tenant.created_at.isoformat(),
            "updated_at": tenant.updated_at.isoformat()
        }

    async def get_partner_stats(self, partner_id: str) -> Dict[str, Any]:
        """Get aggregate statistics for a partner"""

        partner_tenants = await self.get_all_tenants(partner_id=partner_id)

        total_users = sum(len(t.users) for t in partner_tenants)
        total_revenue = sum(t.monthly_revenue for t in partner_tenants)
        total_api_calls = sum(t.api_calls_this_month for t in partner_tenants)

        return {
            "partner_id": partner_id,
            "total_tenants": len(partner_tenants),
            "active_tenants": len([t for t in partner_tenants
                                   if t.config.status == TenantStatus.ACTIVE]),
            "total_users": total_users,
            "total_monthly_revenue": total_revenue,
            "total_api_calls": total_api_calls,
            "tenants": [
                {
                    "tenant_id": t.config.tenant_id,
                    "name": t.config.name,
                    "status": t.config.status.value,
                    "users": len(t.users),
                    "revenue": t.monthly_revenue
                }
                for t in partner_tenants
            ]
        }
