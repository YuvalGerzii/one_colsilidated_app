"""
Feature Flags System

Dynamic feature flag management for white-label tenants.
Control feature rollout, A/B testing, and tenant-specific customization.

Features:
- Tenant-specific flags
- Percentage rollouts
- User targeting
- A/B testing
- Kill switches
"""

from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging
import random

logger = logging.getLogger(__name__)


class FlagType(Enum):
    """Types of feature flags"""
    BOOLEAN = "boolean"
    PERCENTAGE = "percentage"
    USER_LIST = "user_list"
    VARIANT = "variant"


class FlagStatus(Enum):
    """Flag statuses"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    KILLED = "killed"


@dataclass
class FeatureFlag:
    """Feature flag configuration"""
    flag_id: str
    name: str
    description: str
    flag_type: FlagType
    status: FlagStatus = FlagStatus.ACTIVE

    # Targeting
    tenant_ids: List[str] = field(default_factory=list)  # Empty = all tenants
    user_ids: List[str] = field(default_factory=list)    # Specific users
    percentage: float = 100.0  # Rollout percentage

    # Variants (for A/B testing)
    variants: Dict[str, Any] = field(default_factory=dict)
    default_variant: str = "control"

    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    created_by: str = ""
    tags: List[str] = field(default_factory=list)


@dataclass
class FlagEvaluation:
    """Result of flag evaluation"""
    flag_id: str
    enabled: bool
    variant: Optional[str] = None
    reason: str = ""
    evaluated_at: datetime = field(default_factory=datetime.now)


class FeatureFlagManager:
    """
    Manages feature flags for white-label tenants.

    Features:
    - Create and manage flags
    - Evaluate flags for users
    - Track flag usage
    - A/B test analysis
    """

    def __init__(self):
        self.flags: Dict[str, FeatureFlag] = {}
        self.evaluation_history: List[FlagEvaluation] = []
        self.variant_assignments: Dict[str, Dict[str, str]] = {}  # user_id -> {flag_id -> variant}

    def create_flag(
        self,
        name: str,
        description: str,
        flag_type: FlagType = FlagType.BOOLEAN,
        tenant_ids: Optional[List[str]] = None,
        percentage: float = 100.0,
        variants: Optional[Dict[str, Any]] = None
    ) -> FeatureFlag:
        """Create a new feature flag"""

        flag_id = f"flag_{name.lower().replace(' ', '_')}_{datetime.now().timestamp()}"

        flag = FeatureFlag(
            flag_id=flag_id,
            name=name,
            description=description,
            flag_type=flag_type,
            tenant_ids=tenant_ids or [],
            percentage=percentage,
            variants=variants or {"control": {}, "treatment": {}}
        )

        self.flags[flag_id] = flag
        logger.info(f"Created feature flag: {name}")

        return flag

    def evaluate(
        self,
        flag_id: str,
        tenant_id: str,
        user_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> FlagEvaluation:
        """Evaluate a feature flag for a user"""

        flag = self.flags.get(flag_id)

        if not flag:
            return FlagEvaluation(
                flag_id=flag_id,
                enabled=False,
                reason="Flag not found"
            )

        # Check kill switch
        if flag.status == FlagStatus.KILLED:
            return FlagEvaluation(
                flag_id=flag_id,
                enabled=False,
                reason="Flag killed"
            )

        # Check if inactive
        if flag.status == FlagStatus.INACTIVE:
            return FlagEvaluation(
                flag_id=flag_id,
                enabled=False,
                reason="Flag inactive"
            )

        # Check tenant targeting
        if flag.tenant_ids and tenant_id not in flag.tenant_ids:
            return FlagEvaluation(
                flag_id=flag_id,
                enabled=False,
                reason="Tenant not targeted"
            )

        # Check user targeting
        if flag.flag_type == FlagType.USER_LIST:
            if user_id and user_id in flag.user_ids:
                return FlagEvaluation(
                    flag_id=flag_id,
                    enabled=True,
                    reason="User in allowed list"
                )
            return FlagEvaluation(
                flag_id=flag_id,
                enabled=False,
                reason="User not in allowed list"
            )

        # Percentage rollout
        if flag.flag_type == FlagType.PERCENTAGE or flag.percentage < 100:
            # Deterministic based on user_id for consistency
            if user_id:
                hash_value = hash(f"{flag_id}:{user_id}") % 100
            else:
                hash_value = random.randint(0, 99)

            enabled = hash_value < flag.percentage

            return FlagEvaluation(
                flag_id=flag_id,
                enabled=enabled,
                reason=f"Percentage rollout ({flag.percentage}%)"
            )

        # Variant selection for A/B tests
        if flag.flag_type == FlagType.VARIANT:
            variant = self._select_variant(flag, user_id)
            return FlagEvaluation(
                flag_id=flag_id,
                enabled=True,
                variant=variant,
                reason="Variant assignment"
            )

        # Default: enabled
        return FlagEvaluation(
            flag_id=flag_id,
            enabled=True,
            reason="Flag enabled"
        )

    def _select_variant(
        self,
        flag: FeatureFlag,
        user_id: Optional[str]
    ) -> str:
        """Select variant for A/B test"""

        if not user_id:
            return flag.default_variant

        # Check for existing assignment
        user_assignments = self.variant_assignments.get(user_id, {})
        if flag.flag_id in user_assignments:
            return user_assignments[flag.flag_id]

        # Assign variant deterministically
        variants = list(flag.variants.keys())
        if not variants:
            return flag.default_variant

        hash_value = hash(f"{flag.flag_id}:{user_id}") % len(variants)
        variant = variants[hash_value]

        # Store assignment
        if user_id not in self.variant_assignments:
            self.variant_assignments[user_id] = {}
        self.variant_assignments[user_id][flag.flag_id] = variant

        return variant

    def is_enabled(
        self,
        flag_name: str,
        tenant_id: str,
        user_id: Optional[str] = None
    ) -> bool:
        """Quick check if flag is enabled"""

        # Find flag by name
        for flag in self.flags.values():
            if flag.name == flag_name:
                result = self.evaluate(flag.flag_id, tenant_id, user_id)
                return result.enabled

        return False

    def get_variant(
        self,
        flag_name: str,
        tenant_id: str,
        user_id: Optional[str] = None
    ) -> Optional[str]:
        """Get variant for A/B test flag"""

        for flag in self.flags.values():
            if flag.name == flag_name:
                result = self.evaluate(flag.flag_id, tenant_id, user_id)
                return result.variant

        return None

    def update_flag(
        self,
        flag_id: str,
        updates: Dict[str, Any]
    ) -> FeatureFlag:
        """Update a feature flag"""

        if flag_id not in self.flags:
            raise ValueError(f"Flag {flag_id} not found")

        flag = self.flags[flag_id]

        # Apply updates
        for key, value in updates.items():
            if hasattr(flag, key):
                setattr(flag, key, value)

        flag.updated_at = datetime.now()

        logger.info(f"Updated flag {flag.name}")
        return flag

    def kill_flag(self, flag_id: str):
        """Kill switch - immediately disable a flag"""

        if flag_id in self.flags:
            self.flags[flag_id].status = FlagStatus.KILLED
            self.flags[flag_id].updated_at = datetime.now()
            logger.warning(f"Killed flag {self.flags[flag_id].name}")

    def revive_flag(self, flag_id: str):
        """Revive a killed flag"""

        if flag_id in self.flags:
            self.flags[flag_id].status = FlagStatus.ACTIVE
            self.flags[flag_id].updated_at = datetime.now()
            logger.info(f"Revived flag {self.flags[flag_id].name}")

    def get_tenant_flags(
        self,
        tenant_id: str,
        user_id: Optional[str] = None
    ) -> Dict[str, FlagEvaluation]:
        """Get all flag evaluations for a tenant"""

        results = {}

        for flag in self.flags.values():
            result = self.evaluate(flag.flag_id, tenant_id, user_id)
            results[flag.name] = result

        return results

    def get_flag_stats(self, flag_id: str) -> Dict[str, Any]:
        """Get statistics for a flag"""

        flag = self.flags.get(flag_id)
        if not flag:
            return {"error": "Flag not found"}

        # Count variant assignments
        variant_counts = {}
        for user_assignments in self.variant_assignments.values():
            if flag_id in user_assignments:
                variant = user_assignments[flag_id]
                variant_counts[variant] = variant_counts.get(variant, 0) + 1

        return {
            "flag_id": flag_id,
            "name": flag.name,
            "status": flag.status.value,
            "type": flag.flag_type.value,
            "percentage": flag.percentage,
            "tenant_count": len(flag.tenant_ids) if flag.tenant_ids else "all",
            "user_count": len(flag.user_ids),
            "variant_distribution": variant_counts,
            "created_at": flag.created_at.isoformat(),
            "updated_at": flag.updated_at.isoformat()
        }

    def list_flags(
        self,
        status: Optional[FlagStatus] = None,
        tag: Optional[str] = None
    ) -> List[FeatureFlag]:
        """List all flags with optional filtering"""

        flags = list(self.flags.values())

        if status:
            flags = [f for f in flags if f.status == status]

        if tag:
            flags = [f for f in flags if tag in f.tags]

        return flags

    def delete_flag(self, flag_id: str):
        """Delete a feature flag"""

        if flag_id in self.flags:
            name = self.flags[flag_id].name
            del self.flags[flag_id]
            logger.info(f"Deleted flag {name}")


# Pre-built flags for common features
def create_default_flags(manager: FeatureFlagManager):
    """Create default feature flags"""

    # AI features
    manager.create_flag(
        name="ai_chatbot",
        description="Enable AI chatbot assistant",
        flag_type=FlagType.PERCENTAGE,
        percentage=100.0
    )

    manager.create_flag(
        name="predictive_analytics",
        description="Enable ML-powered predictions",
        flag_type=FlagType.PERCENTAGE,
        percentage=50.0
    )

    # Premium features
    manager.create_flag(
        name="advanced_reports",
        description="Enable advanced reporting features",
        flag_type=FlagType.BOOLEAN
    )

    manager.create_flag(
        name="white_label_branding",
        description="Enable custom branding options",
        flag_type=FlagType.BOOLEAN
    )

    # A/B tests
    manager.create_flag(
        name="new_dashboard_layout",
        description="Test new dashboard layout",
        flag_type=FlagType.VARIANT,
        variants={
            "control": {"layout": "classic"},
            "treatment_a": {"layout": "modern"},
            "treatment_b": {"layout": "compact"}
        }
    )

    manager.create_flag(
        name="pricing_experiment",
        description="Test different pricing displays",
        flag_type=FlagType.VARIANT,
        variants={
            "control": {"show_annual_savings": False},
            "treatment": {"show_annual_savings": True}
        }
    )

    return manager
