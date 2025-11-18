"""
Alert and notification service for real-time opportunity and risk alerts.
"""
import asyncio
import logging
from typing import List, Dict, Optional, Callable
from datetime import datetime
from decimal import Decimal
from enum import Enum
from collections import deque

from ..models.types import ArbitrageOpportunity


class AlertLevel(Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class AlertType(Enum):
    """Types of alerts."""
    OPPORTUNITY = "opportunity"
    RISK = "risk"
    EXECUTION = "execution"
    PORTFOLIO = "portfolio"
    SYSTEM = "system"


class Alert:
    """Represents an alert."""

    def __init__(
        self,
        alert_type: AlertType,
        level: AlertLevel,
        message: str,
        details: Dict = None,
        timestamp: datetime = None
    ):
        """Initialize alert."""
        self.alert_type = alert_type
        self.level = level
        self.message = message
        self.details = details or {}
        self.timestamp = timestamp or datetime.now()
        self.acknowledged = False

    def to_dict(self) -> Dict:
        """Convert alert to dictionary."""
        return {
            "type": self.alert_type.value,
            "level": self.level.value,
            "message": self.message,
            "details": self.details,
            "timestamp": self.timestamp.isoformat(),
            "acknowledged": self.acknowledged
        }


class AlertService:
    """Service for managing alerts and notifications."""

    def __init__(self, config: dict = None):
        """
        Initialize alert service.

        Args:
            config: Service configuration
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # Alert storage
        self.alerts: deque = deque(maxlen=self.config.get("max_alerts", 1000))
        self.handlers: Dict[AlertType, List[Callable]] = {}

        # Alert thresholds
        self.thresholds = {
            "min_opportunity_score": Decimal(
                str(self.config.get("min_opportunity_score", "0.7"))
            ),
            "max_risk_score": Decimal(
                str(self.config.get("max_risk_score", "0.5"))
            ),
            "max_drawdown_pct": Decimal(
                str(self.config.get("max_drawdown_pct", "10"))
            ),
            "min_profit_pct": Decimal(
                str(self.config.get("min_profit_pct", "0.5"))
            )
        }

        # Rate limiting
        self.alert_cooldown = self.config.get("alert_cooldown_seconds", 60)
        self.last_alert_time: Dict[str, datetime] = {}

        self.is_running = False

    async def start(self):
        """Start the alert service."""
        self.is_running = True
        self.logger.info("Alert service started")

    async def stop(self):
        """Stop the alert service."""
        self.is_running = False
        self.logger.info("Alert service stopped")

    def register_handler(
        self,
        alert_type: AlertType,
        handler: Callable
    ):
        """
        Register alert handler.

        Args:
            alert_type: Type of alert to handle
            handler: Handler function (async)
        """
        if alert_type not in self.handlers:
            self.handlers[alert_type] = []

        self.handlers[alert_type].append(handler)
        self.logger.info(f"Registered handler for {alert_type.value} alerts")

    async def send_alert(
        self,
        alert_type: AlertType,
        level: AlertLevel,
        message: str,
        details: Dict = None
    ):
        """
        Send an alert.

        Args:
            alert_type: Type of alert
            level: Alert severity
            message: Alert message
            details: Additional details
        """
        if not self.is_running:
            return

        # Check rate limiting
        alert_key = f"{alert_type.value}:{message}"
        if alert_key in self.last_alert_time:
            time_since_last = (datetime.now() - self.last_alert_time[alert_key]).total_seconds()
            if time_since_last < self.alert_cooldown:
                return  # Skip duplicate alert

        # Create alert
        alert = Alert(alert_type, level, message, details)
        self.alerts.append(alert)
        self.last_alert_time[alert_key] = datetime.now()

        # Log alert
        log_method = {
            AlertLevel.INFO: self.logger.info,
            AlertLevel.WARNING: self.logger.warning,
            AlertLevel.CRITICAL: self.logger.critical
        }[level]

        log_method(f"[{alert_type.value.upper()}] {message}")

        # Call handlers
        if alert_type in self.handlers:
            for handler in self.handlers[alert_type]:
                try:
                    await handler(alert)
                except Exception as e:
                    self.logger.error(f"Error in alert handler: {e}", exc_info=True)

    async def alert_opportunity(
        self,
        opportunity: ArbitrageOpportunity
    ):
        """
        Send opportunity alert.

        Args:
            opportunity: Detected opportunity
        """
        # Check thresholds
        if (opportunity.expected_profit_percentage < self.thresholds["min_profit_pct"] or
            opportunity.risk_score > self.thresholds["max_risk_score"]):
            return

        level = AlertLevel.CRITICAL if opportunity.expected_profit_percentage > Decimal(2) else AlertLevel.WARNING

        await self.send_alert(
            alert_type=AlertType.OPPORTUNITY,
            level=level,
            message=f"High-quality {opportunity.arbitrage_type.value} opportunity detected: {opportunity.symbol}",
            details={
                "opportunity_id": opportunity.opportunity_id,
                "symbol": opportunity.symbol,
                "type": opportunity.arbitrage_type.value,
                "expected_profit_pct": float(opportunity.expected_profit_percentage),
                "confidence": float(opportunity.confidence_score),
                "risk": float(opportunity.risk_score)
            }
        )

    async def alert_risk_breach(
        self,
        risk_type: str,
        current_value: Decimal,
        threshold: Decimal,
        details: Dict = None
    ):
        """
        Send risk breach alert.

        Args:
            risk_type: Type of risk
            current_value: Current risk value
            threshold: Risk threshold
            details: Additional details
        """
        await self.send_alert(
            alert_type=AlertType.RISK,
            level=AlertLevel.CRITICAL,
            message=f"Risk threshold breached: {risk_type}",
            details={
                "risk_type": risk_type,
                "current_value": float(current_value),
                "threshold": float(threshold),
                "breach_percentage": float((current_value - threshold) / threshold * 100),
                **(details or {})
            }
        )

    async def alert_execution_issue(
        self,
        issue_type: str,
        message: str,
        details: Dict = None
    ):
        """
        Send execution issue alert.

        Args:
            issue_type: Type of issue
            message: Issue description
            details: Additional details
        """
        await self.send_alert(
            alert_type=AlertType.EXECUTION,
            level=AlertLevel.WARNING,
            message=f"Execution issue: {message}",
            details={
                "issue_type": issue_type,
                **(details or {})
            }
        )

    async def alert_portfolio_event(
        self,
        event_type: str,
        message: str,
        details: Dict = None
    ):
        """
        Send portfolio event alert.

        Args:
            event_type: Type of event
            message: Event description
            details: Additional details
        """
        level = AlertLevel.CRITICAL if "loss" in event_type.lower() else AlertLevel.INFO

        await self.send_alert(
            alert_type=AlertType.PORTFOLIO,
            level=level,
            message=message,
            details={
                "event_type": event_type,
                **(details or {})
            }
        )

    async def alert_system_event(
        self,
        message: str,
        level: AlertLevel = AlertLevel.INFO,
        details: Dict = None
    ):
        """
        Send system event alert.

        Args:
            message: Event description
            level: Alert level
            details: Additional details
        """
        await self.send_alert(
            alert_type=AlertType.SYSTEM,
            level=level,
            message=message,
            details=details
        )

    def get_recent_alerts(
        self,
        count: int = 50,
        alert_type: AlertType = None,
        level: AlertLevel = None
    ) -> List[Dict]:
        """
        Get recent alerts.

        Args:
            count: Number of alerts to return
            alert_type: Filter by alert type
            level: Filter by severity level

        Returns:
            List of alerts
        """
        filtered_alerts = list(self.alerts)

        if alert_type:
            filtered_alerts = [a for a in filtered_alerts if a.alert_type == alert_type]

        if level:
            filtered_alerts = [a for a in filtered_alerts if a.level == level]

        # Return most recent
        return [a.to_dict() for a in filtered_alerts[-count:]]

    def get_alert_statistics(self) -> Dict:
        """
        Get alert statistics.

        Returns:
            Alert statistics
        """
        total_alerts = len(self.alerts)

        if total_alerts == 0:
            return {
                "total_alerts": 0,
                "by_type": {},
                "by_level": {},
                "unacknowledged": 0
            }

        by_type = {}
        by_level = {}
        unacknowledged = 0

        for alert in self.alerts:
            # Count by type
            type_key = alert.alert_type.value
            by_type[type_key] = by_type.get(type_key, 0) + 1

            # Count by level
            level_key = alert.level.value
            by_level[level_key] = by_level.get(level_key, 0) + 1

            # Count unacknowledged
            if not alert.acknowledged:
                unacknowledged += 1

        return {
            "total_alerts": total_alerts,
            "by_type": by_type,
            "by_level": by_level,
            "unacknowledged": unacknowledged,
            "critical_count": by_level.get("critical", 0),
            "warning_count": by_level.get("warning", 0),
            "info_count": by_level.get("info", 0)
        }

    def acknowledge_alerts(
        self,
        alert_type: AlertType = None,
        before_time: datetime = None
    ):
        """
        Acknowledge alerts.

        Args:
            alert_type: Acknowledge specific type
            before_time: Acknowledge alerts before this time
        """
        for alert in self.alerts:
            if alert_type and alert.alert_type != alert_type:
                continue

            if before_time and alert.timestamp > before_time:
                continue

            alert.acknowledged = True

    def clear_alerts(
        self,
        alert_type: AlertType = None,
        acknowledged_only: bool = True
    ):
        """
        Clear alerts.

        Args:
            alert_type: Clear specific type
            acknowledged_only: Only clear acknowledged alerts
        """
        if alert_type is None and not acknowledged_only:
            self.alerts.clear()
            return

        alerts_to_keep = []

        for alert in self.alerts:
            # Keep if doesn't match filters
            keep = False

            if alert_type and alert.alert_type != alert_type:
                keep = True

            if acknowledged_only and not alert.acknowledged:
                keep = True

            if keep:
                alerts_to_keep.append(alert)

        self.alerts.clear()
        self.alerts.extend(alerts_to_keep)


# Example handlers

async def console_alert_handler(alert: Alert):
    """Print alerts to console."""
    print(f"\n{'='*60}")
    print(f"ALERT [{alert.level.value.upper()}]: {alert.message}")
    print(f"Time: {alert.timestamp}")
    if alert.details:
        print(f"Details: {alert.details}")
    print(f"{'='*60}\n")


async def email_alert_handler(alert: Alert):
    """
    Send alerts via email.

    Note: This is a placeholder. In production, implement actual email sending.
    """
    if alert.level == AlertLevel.CRITICAL:
        # Send email for critical alerts
        print(f"[EMAIL] Sending critical alert: {alert.message}")


async def webhook_alert_handler(alert: Alert):
    """
    Send alerts via webhook.

    Note: This is a placeholder. In production, implement actual webhook call.
    """
    # Send to webhook endpoint
    print(f"[WEBHOOK] Posting alert: {alert.message}")


async def slack_alert_handler(alert: Alert):
    """
    Send alerts to Slack.

    Note: This is a placeholder. In production, use Slack API.
    """
    if alert.level in [AlertLevel.WARNING, AlertLevel.CRITICAL]:
        print(f"[SLACK] Posting to channel: {alert.message}")
