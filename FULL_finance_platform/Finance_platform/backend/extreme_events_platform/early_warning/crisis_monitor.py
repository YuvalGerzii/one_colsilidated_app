"""
Real-Time Crisis Monitoring System (V6.0)

Continuously monitors markets for early warning signals.
Aggregates data from multiple sources and triggers alerts.

Usage:
    monitor = CrisisMonitor()
    monitor.update_data(current_market_data)
    alerts = monitor.get_current_alerts()
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from .early_warning_system import EarlyWarningSystem, AlertLevel
from .anomaly_detector import ComprehensiveAnomalyDetector


class CrisisMonitor:
    """
    Real-time monitoring system that combines:
    - Leading indicators tracking
    - Anomaly detection
    - Alert generation
    - Historical pattern matching
    """

    def __init__(self, check_frequency_hours: int = 24):
        """
        Initialize monitor

        Args:
            check_frequency_hours: How often to check (default: daily)
        """
        self.ews = EarlyWarningSystem()
        self.anomaly_detector = ComprehensiveAnomalyDetector()

        self.check_frequency = check_frequency_hours
        self.last_check = None
        self.alert_history = []
        self.current_alerts = []

    def update_and_check(
        self,
        market_data: Dict,
        force_check: bool = False
    ) -> Dict:
        """
        Update data and check for alerts

        Args:
            market_data: Current market indicators
            force_check: Force check even if not time yet

        Returns:
            Alert summary
        """

        now = datetime.now()

        # Check if it's time to run
        if not force_check and self.last_check:
            time_since_last = (now - self.last_check).total_seconds() / 3600
            if time_since_last < self.check_frequency:
                return {
                    'status': 'not_time_yet',
                    'next_check_in_hours': self.check_frequency - time_since_last
                }

        # Run early warning system
        ews_warnings = self.ews.analyze_current_conditions(
            current_data=market_data,
            region=market_data.get('region', 'US')
        )

        # Run anomaly detection
        anomalies = self.anomaly_detector.detect_all_anomalies(
            market_data=market_data,
            historical_data=market_data.get('historical', {})
        )

        # Aggregate alerts
        self.current_alerts = self._aggregate_alerts(ews_warnings, anomalies)

        # Store in history
        self.alert_history.append({
            'timestamp': now,
            'alerts': self.current_alerts
        })

        self.last_check = now

        return {
            'status': 'checked',
            'timestamp': now,
            'num_alerts': len(self.current_alerts),
            'highest_severity': self._get_highest_severity(self.current_alerts),
            'alerts': self.current_alerts
        }

    def _aggregate_alerts(self, ews_warnings, anomalies) -> List[Dict]:
        """Combine EWS warnings and anomalies into unified alerts"""

        alerts = []

        # Add EWS warnings
        for warning in ews_warnings:
            alerts.append({
                'type': 'early_warning',
                'source': 'ews',
                'crisis_type': warning.crisis_type.value,
                'alert_level': warning.alert_level.value,
                'probability': warning.probability,
                'months_until': warning.estimated_months_until,
                'confidence': warning.confidence,
                'key_indicators': [i.name for i in warning.key_indicators],
                'recommendations': warning.recommended_actions
            })

        # Add anomalies
        for anomaly in anomalies:
            alerts.append({
                'type': 'anomaly',
                'source': 'anomaly_detector',
                'anomaly_type': anomaly.type.value,
                'severity': anomaly.severity,
                'crisis_probability': anomaly.crisis_probability,
                'description': anomaly.description,
                'precedent': anomaly.historical_precedent
            })

        return alerts

    def _get_highest_severity(self, alerts: List[Dict]) -> str:
        """Get highest alert level"""

        if not alerts:
            return 'green'

        # Check EWS alerts
        ews_alerts = [a for a in alerts if a['type'] == 'early_warning']
        if ews_alerts:
            levels = [a['alert_level'] for a in ews_alerts]
            if 'black' in levels:
                return 'black'
            if 'red' in levels:
                return 'red'
            if 'orange' in levels:
                return 'orange'
            if 'yellow' in levels:
                return 'yellow'

        # Check anomaly severity
        anomaly_alerts = [a for a in alerts if a['type'] == 'anomaly']
        if anomaly_alerts:
            max_severity = max([a['severity'] for a in anomaly_alerts])
            if max_severity > 0.8:
                return 'red'
            elif max_severity > 0.6:
                return 'orange'
            elif max_severity > 0.4:
                return 'yellow'

        return 'green'

    def get_summary(self) -> str:
        """Get human-readable summary"""

        if not self.current_alerts:
            return "✅ No alerts - Markets normal"

        severity = self._get_highest_severity(self.current_alerts)

        summary = []
        summary.append(f"🚨 ALERT LEVEL: {severity.upper()}")
        summary.append(f"Total alerts: {len(self.current_alerts)}")

        # Group by type
        ews_count = len([a for a in self.current_alerts if a['type'] == 'early_warning'])
        anomaly_count = len([a for a in self.current_alerts if a['type'] == 'anomaly'])

        summary.append(f"Early warnings: {ews_count}, Anomalies: {anomaly_count}")

        # Top 3 alerts
        summary.append("\nTop concerns:")
        for alert in self.current_alerts[:3]:
            if alert['type'] == 'early_warning':
                summary.append(f"  - {alert['crisis_type']}: {alert['probability']:.0%} probability in {alert['months_until']} months")
            else:
                summary.append(f"  - {alert['anomaly_type']}: {alert['description']}")

        return "\n".join(summary)


def main():
    """Example usage"""

    monitor = CrisisMonitor(check_frequency_hours=24)

    # Example: Pre-2008 conditions
    market_data = {
        'credit_to_gdp_gap': 12.0,
        'bank_leverage': 32.0,
        'ted_spread': 0.85,
        'housing_price_to_income': 6.3,
        'vix': 13.5,
        'volatility': 0.12,
        'credit_spreads': 60,
        'leverage': 32.0,
        'region': 'US'
    }

    result = monitor.update_and_check(market_data, force_check=True)

    print("=== Crisis Monitor Summary ===")
    print(f"Status: {result['status']}")
    print(f"Alerts: {result['num_alerts']}")
    print(f"Severity: {result['highest_severity'].upper()}")
    print(f"\n{monitor.get_summary()}")


if __name__ == "__main__":
    main()
