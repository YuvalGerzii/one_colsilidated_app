"""
Partner Billing System

Revenue sharing and billing management for white-label partners.
Handles subscriptions, usage billing, and payouts.

Features:
- Subscription management
- Usage-based billing
- Revenue share calculation
- Partner payouts
- Invoice generation
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class BillingPlan(Enum):
    """Partner billing plans"""
    STARTER = "starter"
    GROWTH = "growth"
    ENTERPRISE = "enterprise"
    CUSTOM = "custom"


class BillingCycle(Enum):
    """Billing cycles"""
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUAL = "annual"


class PayoutStatus(Enum):
    """Payout statuses"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class PartnerPlan:
    """Partner billing plan configuration"""
    plan_type: BillingPlan
    base_fee_monthly: float
    revenue_share_percent: float
    included_users: int
    per_user_fee: float
    included_api_calls: int
    per_api_call_fee: float
    support_level: str
    custom_terms: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Subscription:
    """Partner subscription"""
    subscription_id: str
    tenant_id: str
    plan: PartnerPlan
    billing_cycle: BillingCycle

    # Dates
    start_date: datetime
    current_period_start: datetime
    current_period_end: datetime

    # Status
    status: str = "active"  # active, paused, cancelled

    # Usage
    users_count: int = 0
    api_calls_count: int = 0

    # Payment
    payment_method_id: Optional[str] = None
    auto_renew: bool = True


@dataclass
class Invoice:
    """Billing invoice"""
    invoice_id: str
    tenant_id: str
    subscription_id: str

    # Period
    period_start: datetime
    period_end: datetime
    created_at: datetime = field(default_factory=datetime.now)
    due_date: datetime = field(default_factory=lambda: datetime.now() + timedelta(days=30))

    # Amounts
    subtotal: float = 0.0
    tax: float = 0.0
    total: float = 0.0

    # Line items
    line_items: List[Dict[str, Any]] = field(default_factory=list)

    # Status
    status: str = "pending"  # pending, paid, overdue, void
    paid_at: Optional[datetime] = None


@dataclass
class Payout:
    """Partner payout"""
    payout_id: str
    tenant_id: str
    amount: float
    currency: str = "USD"

    # Period
    period_start: datetime
    period_end: datetime

    # Details
    revenue_generated: float = 0.0
    platform_fee: float = 0.0
    net_payout: float = 0.0

    # Status
    status: PayoutStatus = PayoutStatus.PENDING
    scheduled_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    # Payment details
    payout_method: str = "bank_transfer"
    transaction_id: Optional[str] = None


class PartnerBillingManager:
    """
    Manages partner billing and revenue sharing.

    Features:
    - Subscription lifecycle
    - Usage tracking
    - Invoice generation
    - Revenue share calculation
    - Payout processing
    """

    def __init__(self):
        self.plans = self._initialize_plans()
        self.subscriptions: Dict[str, Subscription] = {}
        self.invoices: List[Invoice] = []
        self.payouts: List[Payout] = []

    def _initialize_plans(self) -> Dict[BillingPlan, PartnerPlan]:
        """Initialize partner plans"""

        return {
            BillingPlan.STARTER: PartnerPlan(
                plan_type=BillingPlan.STARTER,
                base_fee_monthly=499,
                revenue_share_percent=70,  # Partner keeps 70%
                included_users=50,
                per_user_fee=5,
                included_api_calls=10000,
                per_api_call_fee=0.001,
                support_level="email"
            ),
            BillingPlan.GROWTH: PartnerPlan(
                plan_type=BillingPlan.GROWTH,
                base_fee_monthly=1499,
                revenue_share_percent=75,
                included_users=200,
                per_user_fee=4,
                included_api_calls=50000,
                per_api_call_fee=0.0008,
                support_level="priority"
            ),
            BillingPlan.ENTERPRISE: PartnerPlan(
                plan_type=BillingPlan.ENTERPRISE,
                base_fee_monthly=4999,
                revenue_share_percent=80,
                included_users=1000,
                per_user_fee=3,
                included_api_calls=500000,
                per_api_call_fee=0.0005,
                support_level="dedicated"
            )
        }

    async def create_subscription(
        self,
        tenant_id: str,
        plan_type: BillingPlan,
        billing_cycle: BillingCycle = BillingCycle.MONTHLY,
        payment_method_id: Optional[str] = None
    ) -> Subscription:
        """Create a new subscription"""

        plan = self.plans.get(plan_type)
        if not plan:
            raise ValueError(f"Invalid plan type: {plan_type}")

        now = datetime.now()

        # Calculate period end based on billing cycle
        if billing_cycle == BillingCycle.MONTHLY:
            period_end = now + timedelta(days=30)
        elif billing_cycle == BillingCycle.QUARTERLY:
            period_end = now + timedelta(days=90)
        else:  # Annual
            period_end = now + timedelta(days=365)

        subscription_id = f"sub_{tenant_id}_{now.timestamp()}"

        subscription = Subscription(
            subscription_id=subscription_id,
            tenant_id=tenant_id,
            plan=plan,
            billing_cycle=billing_cycle,
            start_date=now,
            current_period_start=now,
            current_period_end=period_end,
            payment_method_id=payment_method_id
        )

        self.subscriptions[subscription_id] = subscription
        logger.info(f"Created subscription {subscription_id} for tenant {tenant_id}")

        return subscription

    async def update_usage(
        self,
        subscription_id: str,
        users: Optional[int] = None,
        api_calls: Optional[int] = None
    ):
        """Update usage for a subscription"""

        if subscription_id not in self.subscriptions:
            raise ValueError(f"Subscription {subscription_id} not found")

        subscription = self.subscriptions[subscription_id]

        if users is not None:
            subscription.users_count = users

        if api_calls is not None:
            subscription.api_calls_count = api_calls

    async def generate_invoice(
        self,
        subscription_id: str
    ) -> Invoice:
        """Generate invoice for a subscription"""

        if subscription_id not in self.subscriptions:
            raise ValueError(f"Subscription {subscription_id} not found")

        subscription = self.subscriptions[subscription_id]
        plan = subscription.plan

        # Calculate line items
        line_items = []

        # Base fee
        base_fee = plan.base_fee_monthly
        if subscription.billing_cycle == BillingCycle.QUARTERLY:
            base_fee *= 3
        elif subscription.billing_cycle == BillingCycle.ANNUAL:
            base_fee *= 12 * 0.9  # 10% annual discount

        line_items.append({
            "description": f"Platform Fee ({subscription.billing_cycle.value})",
            "quantity": 1,
            "unit_price": base_fee,
            "amount": base_fee
        })

        # Overage users
        extra_users = max(0, subscription.users_count - plan.included_users)
        if extra_users > 0:
            user_fee = extra_users * plan.per_user_fee
            line_items.append({
                "description": f"Additional Users ({extra_users})",
                "quantity": extra_users,
                "unit_price": plan.per_user_fee,
                "amount": user_fee
            })

        # Overage API calls
        extra_api_calls = max(0, subscription.api_calls_count - plan.included_api_calls)
        if extra_api_calls > 0:
            api_fee = extra_api_calls * plan.per_api_call_fee
            line_items.append({
                "description": f"Additional API Calls ({extra_api_calls:,})",
                "quantity": extra_api_calls,
                "unit_price": plan.per_api_call_fee,
                "amount": api_fee
            })

        subtotal = sum(item["amount"] for item in line_items)
        tax = subtotal * 0.0  # Assuming no tax for B2B SaaS
        total = subtotal + tax

        invoice = Invoice(
            invoice_id=f"inv_{datetime.now().timestamp()}",
            tenant_id=subscription.tenant_id,
            subscription_id=subscription_id,
            period_start=subscription.current_period_start,
            period_end=subscription.current_period_end,
            subtotal=subtotal,
            tax=tax,
            total=total,
            line_items=line_items
        )

        self.invoices.append(invoice)
        logger.info(f"Generated invoice {invoice.invoice_id} for ${total:.2f}")

        return invoice

    async def calculate_revenue_share(
        self,
        tenant_id: str,
        period_start: datetime,
        period_end: datetime
    ) -> Dict[str, Any]:
        """Calculate revenue share for a tenant"""

        # Find tenant's subscription
        subscription = None
        for sub in self.subscriptions.values():
            if sub.tenant_id == tenant_id:
                subscription = sub
                break

        if not subscription:
            return {"error": "No subscription found"}

        # Get invoices for the period
        period_invoices = [
            inv for inv in self.invoices
            if inv.tenant_id == tenant_id
            and inv.period_start >= period_start
            and inv.period_end <= period_end
            and inv.status == "paid"
        ]

        # Calculate revenue
        total_revenue = sum(inv.total for inv in period_invoices)

        # Calculate revenue share
        partner_share_percent = subscription.plan.revenue_share_percent / 100
        platform_share_percent = 1 - partner_share_percent

        partner_revenue = total_revenue * partner_share_percent
        platform_revenue = total_revenue * platform_share_percent

        return {
            "tenant_id": tenant_id,
            "period": {
                "start": period_start.isoformat(),
                "end": period_end.isoformat()
            },
            "total_revenue": total_revenue,
            "revenue_share_percent": subscription.plan.revenue_share_percent,
            "partner_revenue": partner_revenue,
            "platform_revenue": platform_revenue,
            "invoices_count": len(period_invoices)
        }

    async def create_payout(
        self,
        tenant_id: str,
        period_start: datetime,
        period_end: datetime
    ) -> Payout:
        """Create a payout for partner revenue share"""

        # Calculate revenue share
        share = await self.calculate_revenue_share(tenant_id, period_start, period_end)

        if "error" in share:
            raise ValueError(share["error"])

        payout = Payout(
            payout_id=f"payout_{datetime.now().timestamp()}",
            tenant_id=tenant_id,
            amount=share["partner_revenue"],
            period_start=period_start,
            period_end=period_end,
            revenue_generated=share["total_revenue"],
            platform_fee=share["platform_revenue"],
            net_payout=share["partner_revenue"],
            scheduled_date=datetime.now() + timedelta(days=7)
        )

        self.payouts.append(payout)
        logger.info(f"Created payout {payout.payout_id} for ${payout.amount:.2f}")

        return payout

    async def process_payout(self, payout_id: str) -> bool:
        """Process a payout"""

        for payout in self.payouts:
            if payout.payout_id == payout_id:
                # In production, integrate with payment processor
                payout.status = PayoutStatus.PROCESSING

                # Simulate processing
                payout.status = PayoutStatus.COMPLETED
                payout.completed_at = datetime.now()
                payout.transaction_id = f"txn_{datetime.now().timestamp()}"

                logger.info(f"Processed payout {payout_id}")
                return True

        return False

    def get_billing_summary(self, tenant_id: str) -> Dict[str, Any]:
        """Get billing summary for a tenant"""

        # Find subscription
        subscription = None
        for sub in self.subscriptions.values():
            if sub.tenant_id == tenant_id:
                subscription = sub
                break

        if not subscription:
            return {"error": "No subscription found"}

        # Get recent invoices
        recent_invoices = [
            inv for inv in self.invoices
            if inv.tenant_id == tenant_id
        ][-5:]  # Last 5

        # Get pending payouts
        pending_payouts = [
            p for p in self.payouts
            if p.tenant_id == tenant_id and p.status == PayoutStatus.PENDING
        ]

        return {
            "tenant_id": tenant_id,
            "subscription": {
                "id": subscription.subscription_id,
                "plan": subscription.plan.plan_type.value,
                "status": subscription.status,
                "billing_cycle": subscription.billing_cycle.value,
                "current_period_end": subscription.current_period_end.isoformat(),
                "users": subscription.users_count,
                "api_calls": subscription.api_calls_count
            },
            "recent_invoices": [
                {
                    "id": inv.invoice_id,
                    "total": inv.total,
                    "status": inv.status,
                    "date": inv.created_at.isoformat()
                }
                for inv in recent_invoices
            ],
            "pending_payouts": [
                {
                    "id": p.payout_id,
                    "amount": p.amount,
                    "scheduled_date": p.scheduled_date.isoformat() if p.scheduled_date else None
                }
                for p in pending_payouts
            ],
            "total_pending_payout": sum(p.amount for p in pending_payouts)
        }

    async def cancel_subscription(
        self,
        subscription_id: str,
        immediate: bool = False
    ):
        """Cancel a subscription"""

        if subscription_id not in self.subscriptions:
            raise ValueError(f"Subscription {subscription_id} not found")

        subscription = self.subscriptions[subscription_id]

        if immediate:
            subscription.status = "cancelled"
        else:
            # Cancel at end of period
            subscription.auto_renew = False
            subscription.status = "cancelling"

        logger.info(f"Cancelled subscription {subscription_id}")

    def get_revenue_report(
        self,
        period_start: datetime,
        period_end: datetime
    ) -> Dict[str, Any]:
        """Get revenue report for period"""

        period_invoices = [
            inv for inv in self.invoices
            if period_start <= inv.created_at <= period_end
        ]

        paid_invoices = [inv for inv in period_invoices if inv.status == "paid"]

        total_billed = sum(inv.total for inv in period_invoices)
        total_collected = sum(inv.total for inv in paid_invoices)

        return {
            "period": {
                "start": period_start.isoformat(),
                "end": period_end.isoformat()
            },
            "total_invoices": len(period_invoices),
            "paid_invoices": len(paid_invoices),
            "total_billed": total_billed,
            "total_collected": total_collected,
            "collection_rate": (total_collected / total_billed * 100) if total_billed > 0 else 0,
            "by_plan": self._revenue_by_plan(period_invoices)
        }

    def _revenue_by_plan(self, invoices: List[Invoice]) -> Dict[str, float]:
        """Calculate revenue by plan"""
        by_plan = {}
        for inv in invoices:
            sub = self.subscriptions.get(inv.subscription_id)
            if sub:
                plan = sub.plan.plan_type.value
                by_plan[plan] = by_plan.get(plan, 0) + inv.total
        return by_plan
