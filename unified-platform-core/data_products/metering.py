"""
Usage Metering and Pricing

Tracks API usage and enforces pricing tiers for data products.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class PricingTier(Enum):
    """Pricing tiers for data products"""
    FREE = "free"              # Limited access
    STARTER = "starter"        # $99/month
    PROFESSIONAL = "professional"  # $499/month
    ENTERPRISE = "enterprise"  # Custom pricing
    UNLIMITED = "unlimited"    # Volume discount


@dataclass
class TierLimits:
    """Limits for each pricing tier"""
    tier: PricingTier
    monthly_requests: int
    requests_per_minute: int
    data_points_per_request: int
    historical_days: int
    real_time_access: bool
    bulk_export: bool
    webhook_alerts: bool
    dedicated_support: bool
    sla_uptime: float
    price_per_month_usd: float


# Define tier limits
TIER_LIMITS: Dict[PricingTier, TierLimits] = {
    PricingTier.FREE: TierLimits(
        tier=PricingTier.FREE,
        monthly_requests=100,
        requests_per_minute=1,
        data_points_per_request=10,
        historical_days=7,
        real_time_access=False,
        bulk_export=False,
        webhook_alerts=False,
        dedicated_support=False,
        sla_uptime=0.95,
        price_per_month_usd=0
    ),
    PricingTier.STARTER: TierLimits(
        tier=PricingTier.STARTER,
        monthly_requests=10000,
        requests_per_minute=10,
        data_points_per_request=100,
        historical_days=30,
        real_time_access=False,
        bulk_export=False,
        webhook_alerts=True,
        dedicated_support=False,
        sla_uptime=0.99,
        price_per_month_usd=99
    ),
    PricingTier.PROFESSIONAL: TierLimits(
        tier=PricingTier.PROFESSIONAL,
        monthly_requests=100000,
        requests_per_minute=60,
        data_points_per_request=1000,
        historical_days=365,
        real_time_access=True,
        bulk_export=True,
        webhook_alerts=True,
        dedicated_support=False,
        sla_uptime=0.995,
        price_per_month_usd=499
    ),
    PricingTier.ENTERPRISE: TierLimits(
        tier=PricingTier.ENTERPRISE,
        monthly_requests=1000000,
        requests_per_minute=1000,
        data_points_per_request=10000,
        historical_days=3650,  # 10 years
        real_time_access=True,
        bulk_export=True,
        webhook_alerts=True,
        dedicated_support=True,
        sla_uptime=0.999,
        price_per_month_usd=2999
    ),
    PricingTier.UNLIMITED: TierLimits(
        tier=PricingTier.UNLIMITED,
        monthly_requests=-1,  # Unlimited
        requests_per_minute=10000,
        data_points_per_request=100000,
        historical_days=3650,
        real_time_access=True,
        bulk_export=True,
        webhook_alerts=True,
        dedicated_support=True,
        sla_uptime=0.9999,
        price_per_month_usd=9999
    )
}


@dataclass
class UsageRecord:
    """Record of API usage"""
    timestamp: datetime
    api_key: str
    endpoint: str
    method: str
    data_points_returned: int
    response_time_ms: int
    status_code: int
    cost_usd: float = 0.0


@dataclass
class CustomerSubscription:
    """Customer subscription details"""
    customer_id: str
    api_key: str
    tier: PricingTier
    products: List[str]
    start_date: datetime
    end_date: Optional[datetime]
    monthly_spend_limit: Optional[float]
    custom_limits: Optional[Dict[str, Any]] = None


class UsageMetering:
    """
    Tracks and enforces API usage limits.

    Features:
    - Real-time usage tracking
    - Rate limiting
    - Overage billing
    - Usage analytics
    """

    def __init__(self):
        self.usage_records: List[UsageRecord] = []
        self.subscriptions: Dict[str, CustomerSubscription] = {}
        self.minute_counters: Dict[str, List[datetime]] = {}

    def register_subscription(
        self,
        subscription: CustomerSubscription
    ) -> bool:
        """Register a customer subscription"""
        self.subscriptions[subscription.api_key] = subscription
        logger.info(f"Registered subscription for customer {subscription.customer_id}")
        return True

    async def check_limits(
        self,
        api_key: str,
        endpoint: str,
        requested_data_points: int = 1
    ) -> Dict[str, Any]:
        """
        Check if request is within limits.

        Returns:
        - allowed: bool
        - reason: str if not allowed
        - remaining: usage stats
        """

        if api_key not in self.subscriptions:
            return {
                "allowed": False,
                "reason": "Invalid API key",
                "remaining": {}
            }

        subscription = self.subscriptions[api_key]
        limits = TIER_LIMITS[subscription.tier]

        # Check rate limit (requests per minute)
        if not self._check_rate_limit(api_key, limits.requests_per_minute):
            return {
                "allowed": False,
                "reason": f"Rate limit exceeded: {limits.requests_per_minute}/minute",
                "remaining": {"requests_this_minute": 0}
            }

        # Check monthly limit
        monthly_usage = self._get_monthly_usage(api_key)
        if limits.monthly_requests > 0 and monthly_usage >= limits.monthly_requests:
            return {
                "allowed": False,
                "reason": f"Monthly limit exceeded: {limits.monthly_requests}",
                "remaining": {"monthly_requests": 0}
            }

        # Check data points per request
        if requested_data_points > limits.data_points_per_request:
            return {
                "allowed": False,
                "reason": f"Data points limit: {limits.data_points_per_request}/request",
                "remaining": {"max_data_points": limits.data_points_per_request}
            }

        return {
            "allowed": True,
            "remaining": {
                "monthly_requests": limits.monthly_requests - monthly_usage - 1,
                "max_data_points": limits.data_points_per_request
            }
        }

    def _check_rate_limit(self, api_key: str, limit: int) -> bool:
        """Check if within rate limit"""
        now = datetime.now()
        one_minute_ago = now - timedelta(minutes=1)

        if api_key not in self.minute_counters:
            self.minute_counters[api_key] = []

        # Clean old records
        self.minute_counters[api_key] = [
            t for t in self.minute_counters[api_key]
            if t > one_minute_ago
        ]

        # Check limit
        if len(self.minute_counters[api_key]) >= limit:
            return False

        # Record this request
        self.minute_counters[api_key].append(now)
        return True

    def _get_monthly_usage(self, api_key: str) -> int:
        """Get total requests this month"""
        now = datetime.now()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        return len([
            r for r in self.usage_records
            if r.api_key == api_key and r.timestamp >= month_start
        ])

    def record_usage(
        self,
        api_key: str,
        endpoint: str,
        method: str,
        data_points: int,
        response_time_ms: int,
        status_code: int
    ) -> UsageRecord:
        """Record API usage"""

        # Calculate cost (for overage billing)
        cost = self._calculate_cost(api_key, data_points)

        record = UsageRecord(
            timestamp=datetime.now(),
            api_key=api_key,
            endpoint=endpoint,
            method=method,
            data_points_returned=data_points,
            response_time_ms=response_time_ms,
            status_code=status_code,
            cost_usd=cost
        )

        self.usage_records.append(record)
        return record

    def _calculate_cost(self, api_key: str, data_points: int) -> float:
        """Calculate cost for usage-based billing"""
        if api_key not in self.subscriptions:
            return 0.0

        subscription = self.subscriptions[api_key]

        # Simple pricing: $0.001 per data point for overages
        limits = TIER_LIMITS[subscription.tier]
        monthly_usage = self._get_monthly_usage(api_key)

        if limits.monthly_requests > 0 and monthly_usage > limits.monthly_requests:
            # Overage pricing
            return data_points * 0.001

        return 0.0

    def get_usage_stats(
        self,
        api_key: str,
        period_days: int = 30
    ) -> Dict[str, Any]:
        """Get usage statistics for a customer"""

        cutoff = datetime.now() - timedelta(days=period_days)

        records = [
            r for r in self.usage_records
            if r.api_key == api_key and r.timestamp >= cutoff
        ]

        if not records:
            return {
                "total_requests": 0,
                "total_data_points": 0,
                "total_cost": 0.0,
                "avg_response_time_ms": 0,
                "error_rate": 0.0
            }

        total_requests = len(records)
        total_data_points = sum(r.data_points_returned for r in records)
        total_cost = sum(r.cost_usd for r in records)
        avg_response_time = sum(r.response_time_ms for r in records) / total_requests
        errors = len([r for r in records if r.status_code >= 400])
        error_rate = errors / total_requests if total_requests > 0 else 0

        return {
            "total_requests": total_requests,
            "total_data_points": total_data_points,
            "total_cost": total_cost,
            "avg_response_time_ms": avg_response_time,
            "error_rate": error_rate,
            "by_endpoint": self._group_by_endpoint(records)
        }

    def _group_by_endpoint(
        self,
        records: List[UsageRecord]
    ) -> Dict[str, int]:
        """Group usage by endpoint"""
        by_endpoint = {}
        for record in records:
            endpoint = record.endpoint
            by_endpoint[endpoint] = by_endpoint.get(endpoint, 0) + 1
        return by_endpoint

    def generate_invoice(
        self,
        api_key: str,
        month: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Generate invoice for a billing period"""

        if api_key not in self.subscriptions:
            return {"error": "Subscription not found"}

        subscription = self.subscriptions[api_key]
        limits = TIER_LIMITS[subscription.tier]

        if month is None:
            month = datetime.now()

        month_start = month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if month.month == 12:
            month_end = month.replace(year=month.year + 1, month=1, day=1) - timedelta(seconds=1)
        else:
            month_end = month.replace(month=month.month + 1, day=1) - timedelta(seconds=1)

        records = [
            r for r in self.usage_records
            if r.api_key == api_key and month_start <= r.timestamp <= month_end
        ]

        base_charge = limits.price_per_month_usd
        overage_charge = sum(r.cost_usd for r in records)
        total_charge = base_charge + overage_charge

        return {
            "customer_id": subscription.customer_id,
            "period": f"{month_start.strftime('%Y-%m')}",
            "tier": subscription.tier.value,
            "base_charge": base_charge,
            "total_requests": len(records),
            "total_data_points": sum(r.data_points_returned for r in records),
            "overage_charge": overage_charge,
            "total_charge": total_charge,
            "generated_at": datetime.now().isoformat()
        }
