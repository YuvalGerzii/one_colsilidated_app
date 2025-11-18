"""
API Gateway for Data Products

Unified gateway for accessing all monetized data products with:
- Authentication and authorization
- Rate limiting per tier
- Usage tracking
- Billing integration
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging
from functools import wraps

from .metering import UsageMetering, PricingTier

logger = logging.getLogger(__name__)


class ProductType(Enum):
    """Types of data products"""
    FINANCE = "finance"
    REAL_ESTATE = "real_estate"
    BOND_AI = "bond_ai"
    LABOR = "labor"
    CROSS_PLATFORM = "cross_platform"


@dataclass
class APIKey:
    """API key configuration"""
    key_id: str
    customer_id: str
    tier: PricingTier
    products: List[ProductType]
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    is_active: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RateLimitConfig:
    """Rate limit configuration"""
    requests_per_minute: int
    requests_per_hour: int
    requests_per_day: int
    burst_limit: int


class DataProductGateway:
    """
    API Gateway for data product access.

    Features:
    - API key management
    - Rate limiting
    - Usage tracking
    - Product routing
    """

    def __init__(self):
        self.api_keys: Dict[str, APIKey] = {}
        self.metering = UsageMetering()
        self.rate_limits = self._initialize_rate_limits()
        self.request_counts: Dict[str, Dict[str, int]] = {}

    def _initialize_rate_limits(self) -> Dict[PricingTier, RateLimitConfig]:
        """Initialize rate limits per tier"""

        return {
            PricingTier.FREE: RateLimitConfig(
                requests_per_minute=10,
                requests_per_hour=100,
                requests_per_day=500,
                burst_limit=5
            ),
            PricingTier.STARTER: RateLimitConfig(
                requests_per_minute=60,
                requests_per_hour=1000,
                requests_per_day=10000,
                burst_limit=20
            ),
            PricingTier.PROFESSIONAL: RateLimitConfig(
                requests_per_minute=300,
                requests_per_hour=5000,
                requests_per_day=50000,
                burst_limit=50
            ),
            PricingTier.ENTERPRISE: RateLimitConfig(
                requests_per_minute=1000,
                requests_per_hour=20000,
                requests_per_day=200000,
                burst_limit=100
            ),
            PricingTier.UNLIMITED: RateLimitConfig(
                requests_per_minute=10000,
                requests_per_hour=100000,
                requests_per_day=1000000,
                burst_limit=500
            )
        }

    async def create_api_key(
        self,
        customer_id: str,
        tier: PricingTier,
        products: List[ProductType],
        expires_in_days: Optional[int] = None
    ) -> APIKey:
        """Create a new API key"""

        import secrets

        key_id = f"pk_{secrets.token_urlsafe(32)}"

        expires_at = None
        if expires_in_days:
            from datetime import timedelta
            expires_at = datetime.now() + timedelta(days=expires_in_days)

        api_key = APIKey(
            key_id=key_id,
            customer_id=customer_id,
            tier=tier,
            products=products,
            expires_at=expires_at
        )

        self.api_keys[key_id] = api_key
        logger.info(f"Created API key {key_id[:10]}... for customer {customer_id}")

        return api_key

    async def validate_api_key(self, key_id: str) -> Optional[APIKey]:
        """Validate an API key"""

        api_key = self.api_keys.get(key_id)

        if not api_key:
            return None

        if not api_key.is_active:
            return None

        if api_key.expires_at and api_key.expires_at < datetime.now():
            api_key.is_active = False
            return None

        return api_key

    async def check_rate_limit(
        self,
        key_id: str,
        product: ProductType
    ) -> Dict[str, Any]:
        """Check if request is within rate limits"""

        api_key = await self.validate_api_key(key_id)
        if not api_key:
            return {
                "allowed": False,
                "reason": "Invalid API key"
            }

        rate_limit = self.rate_limits[api_key.tier]

        # Initialize request counts
        if key_id not in self.request_counts:
            self.request_counts[key_id] = {
                "minute": 0,
                "hour": 0,
                "day": 0,
                "last_reset_minute": datetime.now(),
                "last_reset_hour": datetime.now(),
                "last_reset_day": datetime.now()
            }

        counts = self.request_counts[key_id]
        now = datetime.now()

        # Reset counters if needed
        if (now - counts["last_reset_minute"]).seconds >= 60:
            counts["minute"] = 0
            counts["last_reset_minute"] = now

        if (now - counts["last_reset_hour"]).seconds >= 3600:
            counts["hour"] = 0
            counts["last_reset_hour"] = now

        if (now - counts["last_reset_day"]).seconds >= 86400:
            counts["day"] = 0
            counts["last_reset_day"] = now

        # Check limits
        if counts["minute"] >= rate_limit.requests_per_minute:
            return {
                "allowed": False,
                "reason": "Rate limit exceeded (per minute)",
                "retry_after_seconds": 60 - (now - counts["last_reset_minute"]).seconds
            }

        if counts["hour"] >= rate_limit.requests_per_hour:
            return {
                "allowed": False,
                "reason": "Rate limit exceeded (per hour)",
                "retry_after_seconds": 3600 - (now - counts["last_reset_hour"]).seconds
            }

        if counts["day"] >= rate_limit.requests_per_day:
            return {
                "allowed": False,
                "reason": "Rate limit exceeded (per day)",
                "retry_after_seconds": 86400 - (now - counts["last_reset_day"]).seconds
            }

        # Increment counters
        counts["minute"] += 1
        counts["hour"] += 1
        counts["day"] += 1

        return {
            "allowed": True,
            "remaining": {
                "minute": rate_limit.requests_per_minute - counts["minute"],
                "hour": rate_limit.requests_per_hour - counts["hour"],
                "day": rate_limit.requests_per_day - counts["day"]
            }
        }

    async def process_request(
        self,
        key_id: str,
        product: ProductType,
        endpoint: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process a data product API request"""

        # Validate API key
        api_key = await self.validate_api_key(key_id)
        if not api_key:
            return {
                "success": False,
                "error": "Invalid or expired API key",
                "code": 401
            }

        # Check product access
        if product not in api_key.products:
            return {
                "success": False,
                "error": f"API key does not have access to {product.value} products",
                "code": 403
            }

        # Check rate limits
        rate_check = await self.check_rate_limit(key_id, product)
        if not rate_check["allowed"]:
            return {
                "success": False,
                "error": rate_check["reason"],
                "code": 429,
                "retry_after": rate_check.get("retry_after_seconds")
            }

        # Track usage
        await self.metering.track_usage(
            customer_id=api_key.customer_id,
            endpoint=f"{product.value}/{endpoint}",
            tier=api_key.tier
        )

        return {
            "success": True,
            "key_id": key_id,
            "customer_id": api_key.customer_id,
            "tier": api_key.tier.value,
            "remaining_requests": rate_check.get("remaining", {})
        }

    async def revoke_api_key(self, key_id: str) -> bool:
        """Revoke an API key"""

        if key_id in self.api_keys:
            self.api_keys[key_id].is_active = False
            logger.info(f"Revoked API key {key_id[:10]}...")
            return True
        return False

    async def get_usage_stats(self, customer_id: str) -> Dict[str, Any]:
        """Get usage statistics for a customer"""

        return await self.metering.get_usage_report(customer_id)

    def get_api_key_stats(self, key_id: str) -> Dict[str, Any]:
        """Get statistics for an API key"""

        api_key = self.api_keys.get(key_id)
        if not api_key:
            return {"error": "API key not found"}

        counts = self.request_counts.get(key_id, {})

        return {
            "key_id": key_id[:10] + "...",
            "customer_id": api_key.customer_id,
            "tier": api_key.tier.value,
            "products": [p.value for p in api_key.products],
            "is_active": api_key.is_active,
            "created_at": api_key.created_at.isoformat(),
            "expires_at": api_key.expires_at.isoformat() if api_key.expires_at else None,
            "requests_today": counts.get("day", 0)
        }


# Decorator for protecting endpoints
def require_api_key(product: ProductType):
    """Decorator to require API key for endpoint"""

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract API key from request (implementation depends on framework)
            api_key = kwargs.get("api_key")
            gateway = kwargs.get("gateway")

            if not api_key or not gateway:
                return {"error": "API key required", "code": 401}

            # Process through gateway
            result = await gateway.process_request(
                key_id=api_key,
                product=product,
                endpoint=func.__name__,
                params=kwargs
            )

            if not result["success"]:
                return result

            # Call the actual function
            return await func(*args, **kwargs)

        return wrapper
    return decorator


# FastAPI integration
def create_gateway_middleware():
    """Create FastAPI middleware for API gateway"""

    from fastapi import Request, HTTPException
    from starlette.middleware.base import BaseHTTPMiddleware

    gateway = DataProductGateway()

    class GatewayMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request: Request, call_next):
            # Check if this is a data product endpoint
            if request.url.path.startswith("/api/data-products/"):
                api_key = request.headers.get("X-API-Key")

                if not api_key:
                    raise HTTPException(status_code=401, detail="API key required")

                # Determine product from path
                path_parts = request.url.path.split("/")
                product_name = path_parts[3] if len(path_parts) > 3 else "unknown"

                try:
                    product = ProductType(product_name)
                except ValueError:
                    product = ProductType.CROSS_PLATFORM

                # Validate and check rate limits
                result = await gateway.process_request(
                    key_id=api_key,
                    product=product,
                    endpoint=request.url.path,
                    params=dict(request.query_params)
                )

                if not result["success"]:
                    raise HTTPException(
                        status_code=result["code"],
                        detail=result["error"]
                    )

                # Add rate limit headers to response
                response = await call_next(request)
                remaining = result.get("remaining_requests", {})
                response.headers["X-RateLimit-Remaining-Minute"] = str(remaining.get("minute", 0))
                response.headers["X-RateLimit-Remaining-Hour"] = str(remaining.get("hour", 0))
                response.headers["X-RateLimit-Remaining-Day"] = str(remaining.get("day", 0))

                return response

            return await call_next(request)

    return GatewayMiddleware, gateway
