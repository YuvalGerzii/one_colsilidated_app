"""
Domain Manager

Custom domain management for white-label tenants.
Handles domain verification, SSL certificates, and routing.

Features:
- Custom domain registration
- SSL certificate provisioning
- DNS verification
- Domain routing
- Subdomain management
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class DomainStatus(Enum):
    """Domain statuses"""
    PENDING = "pending"
    VERIFYING = "verifying"
    ACTIVE = "active"
    FAILED = "failed"
    EXPIRED = "expired"


class VerificationMethod(Enum):
    """Domain verification methods"""
    DNS_TXT = "dns_txt"
    DNS_CNAME = "dns_cname"
    FILE = "file"


class SSLStatus(Enum):
    """SSL certificate statuses"""
    PENDING = "pending"
    PROVISIONING = "provisioning"
    ACTIVE = "active"
    EXPIRING = "expiring"
    EXPIRED = "expired"
    FAILED = "failed"


@dataclass
class DomainConfig:
    """Custom domain configuration"""
    domain_id: str
    tenant_id: str
    domain: str
    subdomain: Optional[str] = None

    # Verification
    verification_method: VerificationMethod = VerificationMethod.DNS_TXT
    verification_token: str = ""
    verified: bool = False
    verified_at: Optional[datetime] = None

    # SSL
    ssl_status: SSLStatus = SSLStatus.PENDING
    ssl_expires_at: Optional[datetime] = None
    ssl_auto_renew: bool = True

    # Status
    status: DomainStatus = DomainStatus.PENDING
    primary: bool = False

    # Routing
    target_endpoint: str = ""

    # Timestamps
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class DNSRecord:
    """DNS record configuration"""
    record_type: str  # A, CNAME, TXT
    name: str
    value: str
    ttl: int = 3600
    priority: Optional[int] = None


class DomainManager:
    """
    Manages custom domains for white-label tenants.

    Features:
    - Domain registration
    - Verification workflows
    - SSL provisioning
    - DNS configuration
    """

    def __init__(self):
        self.domains: Dict[str, DomainConfig] = {}
        self.platform_domain = "platform.example.com"

    async def add_domain(
        self,
        tenant_id: str,
        domain: str,
        subdomain: Optional[str] = None,
        primary: bool = False
    ) -> DomainConfig:
        """Add a custom domain for a tenant"""

        import secrets

        # Check if domain already exists
        full_domain = f"{subdomain}.{domain}" if subdomain else domain
        for existing in self.domains.values():
            existing_full = f"{existing.subdomain}.{existing.domain}" if existing.subdomain else existing.domain
            if existing_full == full_domain:
                raise ValueError(f"Domain {full_domain} already registered")

        domain_id = f"dom_{tenant_id}_{datetime.now().timestamp()}"
        verification_token = secrets.token_urlsafe(32)

        config = DomainConfig(
            domain_id=domain_id,
            tenant_id=tenant_id,
            domain=domain,
            subdomain=subdomain,
            verification_token=verification_token,
            primary=primary,
            target_endpoint=f"{tenant_id}.{self.platform_domain}"
        )

        self.domains[domain_id] = config
        logger.info(f"Added domain {full_domain} for tenant {tenant_id}")

        return config

    def get_verification_instructions(
        self,
        domain_id: str
    ) -> Dict[str, Any]:
        """Get domain verification instructions"""

        domain = self.domains.get(domain_id)
        if not domain:
            return {"error": "Domain not found"}

        instructions = {
            "domain_id": domain_id,
            "domain": domain.domain,
            "method": domain.verification_method.value,
            "status": domain.status.value
        }

        if domain.verification_method == VerificationMethod.DNS_TXT:
            instructions["dns_record"] = {
                "type": "TXT",
                "name": f"_platform-verification.{domain.domain}",
                "value": domain.verification_token,
                "ttl": 3600
            }
            instructions["instructions"] = [
                "Log in to your DNS provider",
                f"Add a TXT record for _platform-verification.{domain.domain}",
                f"Set the value to: {domain.verification_token}",
                "Wait for DNS propagation (up to 24 hours)",
                "Click 'Verify' to check the record"
            ]

        elif domain.verification_method == VerificationMethod.DNS_CNAME:
            instructions["dns_record"] = {
                "type": "CNAME",
                "name": domain.subdomain or domain.domain,
                "value": domain.target_endpoint,
                "ttl": 3600
            }
            instructions["instructions"] = [
                "Log in to your DNS provider",
                f"Add a CNAME record for {domain.subdomain or domain.domain}",
                f"Point it to: {domain.target_endpoint}",
                "Wait for DNS propagation (up to 24 hours)",
                "Click 'Verify' to check the record"
            ]

        elif domain.verification_method == VerificationMethod.FILE:
            instructions["file"] = {
                "path": f"/.well-known/platform-verification.txt",
                "content": domain.verification_token
            }
            instructions["instructions"] = [
                "Create a file at /.well-known/platform-verification.txt",
                f"Add the content: {domain.verification_token}",
                "Make sure the file is accessible via HTTP",
                "Click 'Verify' to check the file"
            ]

        return instructions

    async def verify_domain(self, domain_id: str) -> Dict[str, Any]:
        """Verify domain ownership"""

        domain = self.domains.get(domain_id)
        if not domain:
            return {"success": False, "error": "Domain not found"}

        domain.status = DomainStatus.VERIFYING

        # In production, perform actual DNS/file verification
        # For now, simulate verification
        verified = True  # Would check DNS records or file

        if verified:
            domain.verified = True
            domain.verified_at = datetime.now()
            domain.status = DomainStatus.ACTIVE
            domain.updated_at = datetime.now()

            logger.info(f"Domain {domain.domain} verified for tenant {domain.tenant_id}")

            # Provision SSL
            await self.provision_ssl(domain_id)

            return {
                "success": True,
                "domain_id": domain_id,
                "status": "verified"
            }
        else:
            domain.status = DomainStatus.FAILED
            return {
                "success": False,
                "error": "Verification failed - DNS record not found"
            }

    async def provision_ssl(self, domain_id: str) -> Dict[str, Any]:
        """Provision SSL certificate for domain"""

        domain = self.domains.get(domain_id)
        if not domain:
            return {"error": "Domain not found"}

        if not domain.verified:
            return {"error": "Domain must be verified first"}

        domain.ssl_status = SSLStatus.PROVISIONING

        # In production, use Let's Encrypt or similar
        # Simulate SSL provisioning
        domain.ssl_status = SSLStatus.ACTIVE
        domain.ssl_expires_at = datetime.now() + timedelta(days=90)
        domain.updated_at = datetime.now()

        logger.info(f"SSL provisioned for {domain.domain}")

        return {
            "success": True,
            "domain_id": domain_id,
            "ssl_status": "active",
            "expires_at": domain.ssl_expires_at.isoformat()
        }

    async def renew_ssl(self, domain_id: str) -> Dict[str, Any]:
        """Renew SSL certificate"""

        domain = self.domains.get(domain_id)
        if not domain:
            return {"error": "Domain not found"}

        # In production, renew with certificate authority
        domain.ssl_expires_at = datetime.now() + timedelta(days=90)
        domain.ssl_status = SSLStatus.ACTIVE
        domain.updated_at = datetime.now()

        logger.info(f"SSL renewed for {domain.domain}")

        return {
            "success": True,
            "new_expiry": domain.ssl_expires_at.isoformat()
        }

    def get_required_dns_records(
        self,
        domain_id: str
    ) -> List[DNSRecord]:
        """Get all required DNS records for a domain"""

        domain = self.domains.get(domain_id)
        if not domain:
            return []

        records = []

        # Main domain record
        if domain.subdomain:
            records.append(DNSRecord(
                record_type="CNAME",
                name=domain.subdomain,
                value=domain.target_endpoint
            ))
        else:
            # Root domain - use A record
            records.append(DNSRecord(
                record_type="A",
                name="@",
                value="192.0.2.1"  # Platform IP
            ))
            # WWW subdomain
            records.append(DNSRecord(
                record_type="CNAME",
                name="www",
                value=domain.target_endpoint
            ))

        # Verification record
        if not domain.verified:
            records.append(DNSRecord(
                record_type="TXT",
                name=f"_platform-verification",
                value=domain.verification_token
            ))

        return records

    async def remove_domain(self, domain_id: str) -> bool:
        """Remove a custom domain"""

        if domain_id in self.domains:
            domain = self.domains[domain_id]
            logger.info(f"Removed domain {domain.domain}")
            del self.domains[domain_id]
            return True

        return False

    def get_tenant_domains(self, tenant_id: str) -> List[DomainConfig]:
        """Get all domains for a tenant"""

        return [
            d for d in self.domains.values()
            if d.tenant_id == tenant_id
        ]

    def get_primary_domain(self, tenant_id: str) -> Optional[str]:
        """Get primary domain for a tenant"""

        for domain in self.domains.values():
            if domain.tenant_id == tenant_id and domain.primary:
                full = f"{domain.subdomain}.{domain.domain}" if domain.subdomain else domain.domain
                return full

        # Return default subdomain
        return f"{tenant_id}.{self.platform_domain}"

    async def set_primary_domain(
        self,
        tenant_id: str,
        domain_id: str
    ) -> bool:
        """Set primary domain for a tenant"""

        domain = self.domains.get(domain_id)
        if not domain or domain.tenant_id != tenant_id:
            return False

        if not domain.verified:
            return False

        # Unset current primary
        for d in self.domains.values():
            if d.tenant_id == tenant_id:
                d.primary = False

        # Set new primary
        domain.primary = True
        domain.updated_at = datetime.now()

        return True

    def get_domain_status(self, domain_id: str) -> Dict[str, Any]:
        """Get comprehensive domain status"""

        domain = self.domains.get(domain_id)
        if not domain:
            return {"error": "Domain not found"}

        full_domain = f"{domain.subdomain}.{domain.domain}" if domain.subdomain else domain.domain

        # Check SSL expiry
        ssl_warning = None
        if domain.ssl_expires_at:
            days_until_expiry = (domain.ssl_expires_at - datetime.now()).days
            if days_until_expiry < 14:
                ssl_warning = f"SSL expires in {days_until_expiry} days"

        return {
            "domain_id": domain_id,
            "domain": full_domain,
            "tenant_id": domain.tenant_id,
            "status": domain.status.value,
            "verified": domain.verified,
            "verified_at": domain.verified_at.isoformat() if domain.verified_at else None,
            "primary": domain.primary,
            "ssl": {
                "status": domain.ssl_status.value,
                "expires_at": domain.ssl_expires_at.isoformat() if domain.ssl_expires_at else None,
                "auto_renew": domain.ssl_auto_renew,
                "warning": ssl_warning
            },
            "routing": {
                "target": domain.target_endpoint
            },
            "created_at": domain.created_at.isoformat(),
            "updated_at": domain.updated_at.isoformat()
        }

    async def check_expiring_ssl(self, days_threshold: int = 14) -> List[DomainConfig]:
        """Find domains with expiring SSL certificates"""

        expiring = []
        threshold = datetime.now() + timedelta(days=days_threshold)

        for domain in self.domains.values():
            if domain.ssl_expires_at and domain.ssl_expires_at < threshold:
                expiring.append(domain)
                if domain.ssl_auto_renew:
                    await self.renew_ssl(domain.domain_id)

        return expiring

    def get_routing_config(self, hostname: str) -> Optional[Dict[str, Any]]:
        """Get routing configuration for a hostname"""

        for domain in self.domains.values():
            full_domain = f"{domain.subdomain}.{domain.domain}" if domain.subdomain else domain.domain

            if full_domain == hostname:
                if domain.status == DomainStatus.ACTIVE:
                    return {
                        "tenant_id": domain.tenant_id,
                        "target": domain.target_endpoint,
                        "ssl_enabled": domain.ssl_status == SSLStatus.ACTIVE
                    }

        return None
