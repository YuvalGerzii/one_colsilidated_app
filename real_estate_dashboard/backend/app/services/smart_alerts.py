"""
Smart Alerts Engine
Real-time anomaly detection and intelligent alerting system for real estate portfolio management

Features:
- Anomaly detection for key metrics (vacancy, rent, expenses, NOI)
- Opportunity identification (underperforming assets, market opportunities)
- Risk alerts (financial, operational, compliance)
- Predictive alerts (forecasting-based warnings)
- Customizable thresholds and rules
"""

from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from enum import Enum
import statistics
from pydantic import BaseModel


class AlertSeverity(str, Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class AlertCategory(str, Enum):
    """Alert categories"""
    FINANCIAL = "financial"
    OPERATIONAL = "operational"
    MARKET = "market"
    COMPLIANCE = "compliance"
    OPPORTUNITY = "opportunity"
    PREDICTIVE = "predictive"


class Alert(BaseModel):
    """Alert model"""
    id: Optional[str] = None
    property_id: Optional[int] = None
    property_name: Optional[str] = None
    category: AlertCategory
    severity: AlertSeverity
    title: str
    message: str
    metric_name: Optional[str] = None
    current_value: Optional[float] = None
    expected_value: Optional[float] = None
    threshold: Optional[float] = None
    deviation_percentage: Optional[float] = None
    timestamp: datetime = datetime.now()
    resolved: bool = False
    action_items: List[str] = []

    class Config:
        json_schema_extra = {
            "example": {
                "property_id": 123,
                "property_name": "Oak Street Apartments",
                "category": "operational",
                "severity": "warning",
                "title": "Vacancy Rate Spike Detected",
                "message": "Vacancy rate increased to 15%, which is 50% higher than the 3-month average of 10%",
                "metric_name": "vacancy_rate",
                "current_value": 0.15,
                "expected_value": 0.10,
                "deviation_percentage": 50.0,
            }
        }


class SmartAlertsEngine:
    """
    Intelligent alerting system for real estate portfolio management
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Smart Alerts Engine

        Args:
            config: Configuration dictionary with thresholds and settings
        """
        self.config = config or self._default_config()

    def _default_config(self) -> Dict[str, Any]:
        """Default configuration for alert thresholds"""
        return {
            "vacancy_rate_threshold": 0.10,  # 10%
            "vacancy_spike_percentage": 0.50,  # 50% increase
            "rent_decline_threshold": -0.05,  # -5%
            "expense_spike_percentage": 0.20,  # 20% increase
            "noi_decline_threshold": -0.10,  # -10%
            "dscr_min": 1.25,
            "occupancy_min": 0.85,  # 85%
            "maintenance_cost_max_percentage": 0.15,  # 15% of revenue
            "collection_rate_min": 0.95,  # 95%
        }

    def analyze_property(self, property_data: Dict[str, Any]) -> List[Alert]:
        """
        Analyze a property and generate alerts

        Args:
            property_data: Dictionary containing property metrics

        Returns:
            List of alerts generated
        """
        alerts = []

        # Run all detection methods
        alerts.extend(self._detect_vacancy_anomalies(property_data))
        alerts.extend(self._detect_rent_anomalies(property_data))
        alerts.extend(self._detect_expense_anomalies(property_data))
        alerts.extend(self._detect_noi_anomalies(property_data))
        alerts.extend(self._detect_financial_risks(property_data))
        alerts.extend(self._detect_operational_issues(property_data))
        alerts.extend(self._detect_opportunities(property_data))

        return alerts

    def _detect_vacancy_anomalies(self, data: Dict[str, Any]) -> List[Alert]:
        """Detect vacancy rate anomalies"""
        alerts = []

        current_vacancy = data.get("vacancy_rate", 0)
        avg_vacancy = data.get("avg_vacancy_rate", 0)

        # High vacancy alert
        if current_vacancy > self.config["vacancy_rate_threshold"]:
            alerts.append(Alert(
                property_id=data.get("id"),
                property_name=data.get("name"),
                category=AlertCategory.OPERATIONAL,
                severity=AlertSeverity.WARNING if current_vacancy < 0.15 else AlertSeverity.ERROR,
                title="High Vacancy Rate Detected",
                message=f"Current vacancy rate of {current_vacancy:.1%} exceeds threshold of {self.config['vacancy_rate_threshold']:.1%}",
                metric_name="vacancy_rate",
                current_value=current_vacancy,
                threshold=self.config["vacancy_rate_threshold"],
                action_items=[
                    "Review leasing strategy and marketing efforts",
                    "Analyze competitor pricing and amenities",
                    "Consider rent adjustments or concessions",
                    "Inspect unit conditions and address maintenance issues"
                ]
            ))

        # Vacancy spike alert
        if avg_vacancy > 0 and current_vacancy > avg_vacancy * (1 + self.config["vacancy_spike_percentage"]):
            deviation = ((current_vacancy - avg_vacancy) / avg_vacancy) * 100
            alerts.append(Alert(
                property_id=data.get("id"),
                property_name=data.get("name"),
                category=AlertCategory.OPERATIONAL,
                severity=AlertSeverity.WARNING,
                title="Vacancy Rate Spike Detected",
                message=f"Vacancy rate of {current_vacancy:.1%} is {deviation:.1f}% higher than 3-month average of {avg_vacancy:.1%}",
                metric_name="vacancy_rate",
                current_value=current_vacancy,
                expected_value=avg_vacancy,
                deviation_percentage=deviation,
                action_items=[
                    "Investigate recent tenant turnover patterns",
                    "Review lease renewal strategies",
                    "Conduct market analysis for competitive positioning"
                ]
            ))

        return alerts

    def _detect_rent_anomalies(self, data: Dict[str, Any]) -> List[Alert]:
        """Detect rent-related anomalies"""
        alerts = []

        rent_growth = data.get("rent_growth_rate", 0)
        market_rent_growth = data.get("market_rent_growth", 0.03)

        # Negative rent growth
        if rent_growth < self.config["rent_decline_threshold"]:
            alerts.append(Alert(
                property_id=data.get("id"),
                property_name=data.get("name"),
                category=AlertCategory.FINANCIAL,
                severity=AlertSeverity.ERROR,
                title="Rent Decline Detected",
                message=f"Rent growth of {rent_growth:.1%} indicates declining revenue",
                metric_name="rent_growth_rate",
                current_value=rent_growth,
                threshold=self.config["rent_decline_threshold"],
                action_items=[
                    "Review market conditions and competitive landscape",
                    "Assess property condition and amenity offerings",
                    "Consider capital improvements to justify rent increases",
                    "Analyze tenant demographics and demand patterns"
                ]
            ))

        # Underperforming vs market
        if market_rent_growth > 0 and rent_growth < market_rent_growth * 0.5:
            alerts.append(Alert(
                property_id=data.get("id"),
                property_name=data.get("name"),
                category=AlertCategory.OPPORTUNITY,
                severity=AlertSeverity.INFO,
                title="Below-Market Rent Growth",
                message=f"Property rent growth of {rent_growth:.1%} significantly trails market growth of {market_rent_growth:.1%}",
                metric_name="rent_growth_rate",
                current_value=rent_growth,
                expected_value=market_rent_growth,
                action_items=[
                    "Conduct rent survey to identify pricing opportunities",
                    "Review and update amenities to support higher rents",
                    "Implement value-add renovation program"
                ]
            ))

        return alerts

    def _detect_expense_anomalies(self, data: Dict[str, Any]) -> List[Alert]:
        """Detect expense anomalies"""
        alerts = []

        current_expenses = data.get("operating_expenses", 0)
        avg_expenses = data.get("avg_operating_expenses", 0)
        revenue = data.get("revenue", 1)

        # Expense spike
        if avg_expenses > 0 and current_expenses > avg_expenses * (1 + self.config["expense_spike_percentage"]):
            deviation = ((current_expenses - avg_expenses) / avg_expenses) * 100
            alerts.append(Alert(
                property_id=data.get("id"),
                property_name=data.get("name"),
                category=AlertCategory.FINANCIAL,
                severity=AlertSeverity.WARNING,
                title="Operating Expense Spike",
                message=f"Operating expenses of ${current_expenses:,.0f} are {deviation:.1f}% higher than average of ${avg_expenses:,.0f}",
                metric_name="operating_expenses",
                current_value=current_expenses,
                expected_value=avg_expenses,
                deviation_percentage=deviation,
                action_items=[
                    "Review recent invoices and expense categories",
                    "Identify one-time vs. recurring cost increases",
                    "Renegotiate vendor contracts if needed",
                    "Implement cost-control measures"
                ]
            ))

        # High maintenance costs
        maintenance_costs = data.get("maintenance_costs", 0)
        if revenue > 0:
            maintenance_ratio = maintenance_costs / revenue
            if maintenance_ratio > self.config["maintenance_cost_max_percentage"]:
                alerts.append(Alert(
                    property_id=data.get("id"),
                    property_name=data.get("name"),
                    category=AlertCategory.OPERATIONAL,
                    severity=AlertSeverity.WARNING,
                    title="High Maintenance Costs",
                    message=f"Maintenance costs represent {maintenance_ratio:.1%} of revenue, exceeding {self.config['maintenance_cost_max_percentage']:.1%} threshold",
                    metric_name="maintenance_ratio",
                    current_value=maintenance_ratio,
                    threshold=self.config["maintenance_cost_max_percentage"],
                    action_items=[
                        "Analyze maintenance work orders for patterns",
                        "Consider preventive maintenance program",
                        "Evaluate age of major building systems",
                        "Plan capital improvements if needed"
                    ]
                ))

        return alerts

    def _detect_noi_anomalies(self, data: Dict[str, Any]) -> List[Alert]:
        """Detect NOI (Net Operating Income) anomalies"""
        alerts = []

        current_noi = data.get("noi", 0)
        avg_noi = data.get("avg_noi", 0)

        # NOI decline
        if avg_noi > 0:
            noi_change = (current_noi - avg_noi) / avg_noi
            if noi_change < self.config["noi_decline_threshold"]:
                alerts.append(Alert(
                    property_id=data.get("id"),
                    property_name=data.get("name"),
                    category=AlertCategory.FINANCIAL,
                    severity=AlertSeverity.ERROR,
                    title="Significant NOI Decline",
                    message=f"NOI of ${current_noi:,.0f} has declined {abs(noi_change):.1%} from average of ${avg_noi:,.0f}",
                    metric_name="noi",
                    current_value=current_noi,
                    expected_value=avg_noi,
                    deviation_percentage=noi_change * 100,
                    action_items=[
                        "Conduct detailed income and expense analysis",
                        "Review property management effectiveness",
                        "Develop action plan to restore NOI",
                        "Consider property repositioning strategy"
                    ]
                ))

        return alerts

    def _detect_financial_risks(self, data: Dict[str, Any]) -> List[Alert]:
        """Detect financial risks"""
        alerts = []

        # Low DSCR
        dscr = data.get("dscr", 0)
        if 0 < dscr < self.config["dscr_min"]:
            alerts.append(Alert(
                property_id=data.get("id"),
                property_name=data.get("name"),
                category=AlertCategory.FINANCIAL,
                severity=AlertSeverity.CRITICAL if dscr < 1.0 else AlertSeverity.ERROR,
                title="Low Debt Service Coverage Ratio",
                message=f"DSCR of {dscr:.2f}x is below minimum threshold of {self.config['dscr_min']:.2f}x",
                metric_name="dscr",
                current_value=dscr,
                threshold=self.config["dscr_min"],
                action_items=[
                    "Review debt structure and refinancing options",
                    "Implement revenue enhancement initiatives",
                    "Reduce operating expenses where possible",
                    "Consider additional equity injection if needed"
                ]
            ))

        # Low collection rate
        collection_rate = data.get("collection_rate", 1.0)
        if collection_rate < self.config["collection_rate_min"]:
            alerts.append(Alert(
                property_id=data.get("id"),
                property_name=data.get("name"),
                category=AlertCategory.OPERATIONAL,
                severity=AlertSeverity.WARNING,
                title="Low Rent Collection Rate",
                message=f"Collection rate of {collection_rate:.1%} is below target of {self.config['collection_rate_min']:.1%}",
                metric_name="collection_rate",
                current_value=collection_rate,
                threshold=self.config["collection_rate_min"],
                action_items=[
                    "Review tenant screening procedures",
                    "Strengthen collections process",
                    "Consider rent collection technology/automation",
                    "Evaluate eviction procedures if needed"
                ]
            ))

        return alerts

    def _detect_operational_issues(self, data: Dict[str, Any]) -> List[Alert]:
        """Detect operational issues"""
        alerts = []

        # Low occupancy
        occupancy = data.get("occupancy_rate", 0)
        if occupancy < self.config["occupancy_min"]:
            alerts.append(Alert(
                property_id=data.get("id"),
                property_name=data.get("name"),
                category=AlertCategory.OPERATIONAL,
                severity=AlertSeverity.WARNING,
                title="Low Occupancy Rate",
                message=f"Occupancy rate of {occupancy:.1%} is below target of {self.config['occupancy_min']:.1%}",
                metric_name="occupancy_rate",
                current_value=occupancy,
                threshold=self.config["occupancy_min"],
                action_items=[
                    "Enhance marketing and leasing efforts",
                    "Review pricing strategy",
                    "Offer move-in specials or concessions",
                    "Improve online presence and virtual tours"
                ]
            ))

        # High maintenance backlog
        maintenance_backlog = data.get("maintenance_backlog_days", 0)
        if maintenance_backlog > 7:
            alerts.append(Alert(
                property_id=data.get("id"),
                property_name=data.get("name"),
                category=AlertCategory.OPERATIONAL,
                severity=AlertSeverity.WARNING,
                title="High Maintenance Backlog",
                message=f"Average maintenance backlog of {maintenance_backlog:.0f} days may impact tenant satisfaction",
                metric_name="maintenance_backlog_days",
                current_value=maintenance_backlog,
                threshold=7,
                action_items=[
                    "Increase maintenance staffing or vendor support",
                    "Prioritize work orders by urgency",
                    "Implement preventive maintenance schedule",
                    "Consider maintenance management software"
                ]
            ))

        return alerts

    def _detect_opportunities(self, data: Dict[str, Any]) -> List[Alert]:
        """Detect investment opportunities"""
        alerts = []

        # Value-add opportunity
        market_rent = data.get("market_rent", 0)
        current_rent = data.get("current_rent", 0)

        if market_rent > 0 and current_rent > 0:
            rent_gap = (market_rent - current_rent) / current_rent
            if rent_gap > 0.15:  # 15% upside
                potential_revenue = (market_rent - current_rent) * data.get("units", 0) * 12
                alerts.append(Alert(
                    property_id=data.get("id"),
                    property_name=data.get("name"),
                    category=AlertCategory.OPPORTUNITY,
                    severity=AlertSeverity.INFO,
                    title="Value-Add Opportunity Identified",
                    message=f"Market rent of ${market_rent:,.0f} is {rent_gap:.1%} higher than current rent of ${current_rent:,.0f}. Potential additional revenue: ${potential_revenue:,.0f}/year",
                    metric_name="rent_gap",
                    current_value=current_rent,
                    expected_value=market_rent,
                    deviation_percentage=rent_gap * 100,
                    action_items=[
                        "Conduct unit renovation cost-benefit analysis",
                        "Develop phased renovation plan",
                        "Model pro forma with upgraded units",
                        "Assess financing options for improvements"
                    ]
                ))

        # Refinancing opportunity
        current_rate = data.get("interest_rate", 0)
        market_rate = data.get("market_interest_rate", 0)
        loan_balance = data.get("loan_balance", 0)

        if current_rate > 0 and market_rate > 0 and current_rate > market_rate * 1.25:
            rate_savings = current_rate - market_rate
            annual_savings = loan_balance * rate_savings
            alerts.append(Alert(
                property_id=data.get("id"),
                property_name=data.get("name"),
                category=AlertCategory.OPPORTUNITY,
                severity=AlertSeverity.INFO,
                title="Refinancing Opportunity",
                message=f"Current rate of {current_rate:.2%} significantly exceeds market rate of {market_rate:.2%}. Potential annual savings: ${annual_savings:,.0f}",
                metric_name="interest_rate",
                current_value=current_rate,
                expected_value=market_rate,
                action_items=[
                    "Request rate quotes from lenders",
                    "Analyze refinancing costs vs. savings",
                    "Review prepayment penalties",
                    "Model cash flow impact of refinancing"
                ]
            ))

        return alerts

    def analyze_portfolio(self, portfolio_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze entire portfolio and generate summary

        Args:
            portfolio_data: List of property data dictionaries

        Returns:
            Dictionary with alerts and summary statistics
        """
        all_alerts = []

        for property_data in portfolio_data:
            alerts = self.analyze_property(property_data)
            all_alerts.extend(alerts)

        # Generate summary
        summary = {
            "total_alerts": len(all_alerts),
            "critical_alerts": len([a for a in all_alerts if a.severity == AlertSeverity.CRITICAL]),
            "error_alerts": len([a for a in all_alerts if a.severity == AlertSeverity.ERROR]),
            "warning_alerts": len([a for a in all_alerts if a.severity == AlertSeverity.WARNING]),
            "info_alerts": len([a for a in all_alerts if a.severity == AlertSeverity.INFO]),
            "alerts_by_category": {
                category.value: len([a for a in all_alerts if a.category == category])
                for category in AlertCategory
            },
            "properties_with_alerts": len(set(a.property_id for a in all_alerts if a.property_id)),
            "top_alerts": sorted(
                [a.dict() for a in all_alerts],
                key=lambda x: {"critical": 4, "error": 3, "warning": 2, "info": 1}[x["severity"]],
                reverse=True
            )[:10]
        }

        return {
            "alerts": [a.dict() for a in all_alerts],
            "summary": summary,
            "timestamp": datetime.now().isoformat()
        }


# Singleton instance
_alerts_engine = None


def get_alerts_engine(config: Optional[Dict[str, Any]] = None) -> SmartAlertsEngine:
    """Get or create alerts engine instance"""
    global _alerts_engine
    if _alerts_engine is None:
        _alerts_engine = SmartAlertsEngine(config)
    return _alerts_engine
