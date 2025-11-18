"""
Risk Scoring Service - Internal Implementation
Weighted risk scoring algorithms for legal and compliance assessment
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass
from datetime import date, datetime, timedelta
import math


class RiskCategory(str, Enum):
    """Categories of risk"""
    FINANCIAL = "financial"
    LEGAL = "legal"
    REGULATORY = "regulatory"
    OPERATIONAL = "operational"
    REPUTATIONAL = "reputational"
    COMPLIANCE = "compliance"
    CONTRACTUAL = "contractual"
    MARKET = "market"


class RiskLevel(str, Enum):
    """Risk levels"""
    CRITICAL = "critical"  # 80-100
    HIGH = "high"  # 60-79
    MEDIUM = "medium"  # 40-59
    LOW = "low"  # 20-39
    MINIMAL = "minimal"  # 0-19


@dataclass
class RiskFactor:
    """Individual risk factor"""
    name: str
    category: RiskCategory
    score: float  # 0-100
    weight: float  # 0-1
    description: str
    mitigation: Optional[str] = None


@dataclass
class RiskAssessment:
    """Complete risk assessment result"""
    overall_score: float  # 0-100
    risk_level: RiskLevel
    category_scores: Dict[RiskCategory, float]
    risk_factors: List[RiskFactor]
    recommendations: List[str]
    critical_items: List[str]


class RiskScoringService:
    """
    Service for calculating risk scores using weighted algorithms
    No external APIs required
    """

    # Risk factor weights by category
    CATEGORY_WEIGHTS = {
        RiskCategory.LEGAL: 0.25,
        RiskCategory.FINANCIAL: 0.20,
        RiskCategory.REGULATORY: 0.20,
        RiskCategory.COMPLIANCE: 0.15,
        RiskCategory.OPERATIONAL: 0.10,
        RiskCategory.CONTRACTUAL: 0.05,
        RiskCategory.REPUTATIONAL: 0.03,
        RiskCategory.MARKET: 0.02
    }

    def __init__(self):
        """Initialize risk scoring service"""
        pass

    def calculate_overall_risk(self, risk_factors: List[RiskFactor]) -> RiskAssessment:
        """
        Calculate overall risk score from individual factors

        Uses weighted average based on category importance and factor weights
        """
        if not risk_factors:
            return RiskAssessment(
                overall_score=0,
                risk_level=RiskLevel.MINIMAL,
                category_scores={},
                risk_factors=[],
                recommendations=["No risk factors provided for assessment"],
                critical_items=[]
            )

        # Calculate category scores
        category_scores = {}
        for category in RiskCategory:
            category_factors = [f for f in risk_factors if f.category == category]
            if category_factors:
                # Weighted average within category
                total_weight = sum(f.weight for f in category_factors)
                if total_weight > 0:
                    category_scores[category] = sum(
                        f.score * f.weight for f in category_factors
                    ) / total_weight
                else:
                    category_scores[category] = sum(f.score for f in category_factors) / len(category_factors)

        # Calculate overall score using category weights
        overall_score = 0
        total_category_weight = 0

        for category, score in category_scores.items():
            category_weight = self.CATEGORY_WEIGHTS.get(category, 0.05)
            overall_score += score * category_weight
            total_category_weight += category_weight

        if total_category_weight > 0:
            overall_score = overall_score / total_category_weight

        # Determine risk level
        risk_level = self._get_risk_level(overall_score)

        # Generate recommendations
        recommendations = self._generate_risk_recommendations(
            overall_score,
            risk_level,
            category_scores,
            risk_factors
        )

        # Identify critical items
        critical_items = [
            f"{f.name}: {f.description}"
            for f in risk_factors
            if f.score >= 80
        ]

        return RiskAssessment(
            overall_score=overall_score,
            risk_level=risk_level,
            category_scores=category_scores,
            risk_factors=risk_factors,
            recommendations=recommendations,
            critical_items=critical_items
        )

    def _get_risk_level(self, score: float) -> RiskLevel:
        """Convert numeric score to risk level"""
        if score >= 80:
            return RiskLevel.CRITICAL
        elif score >= 60:
            return RiskLevel.HIGH
        elif score >= 40:
            return RiskLevel.MEDIUM
        elif score >= 20:
            return RiskLevel.LOW
        else:
            return RiskLevel.MINIMAL

    def _generate_risk_recommendations(
        self,
        overall_score: float,
        risk_level: RiskLevel,
        category_scores: Dict[RiskCategory, float],
        risk_factors: List[RiskFactor]
    ) -> List[str]:
        """Generate recommendations based on risk assessment"""
        recommendations = []

        # Overall recommendations
        if risk_level == RiskLevel.CRITICAL:
            recommendations.append("CRITICAL RISK LEVEL - Immediate action required")
            recommendations.append("Do not proceed without addressing critical risk factors")
            recommendations.append("Engage legal counsel and executive review")

        elif risk_level == RiskLevel.HIGH:
            recommendations.append("HIGH RISK - Proceed with caution")
            recommendations.append("Implement risk mitigation strategies before proceeding")
            recommendations.append("Obtain legal review and approval")

        elif risk_level == RiskLevel.MEDIUM:
            recommendations.append("MEDIUM RISK - Review and mitigate where possible")
            recommendations.append("Consider additional due diligence")

        # Category-specific recommendations
        for category, score in category_scores.items():
            if score >= 70:
                if category == RiskCategory.LEGAL:
                    recommendations.append("Legal risk is high - engage legal counsel")
                elif category == RiskCategory.FINANCIAL:
                    recommendations.append("Financial risk is high - review with CFO/finance team")
                elif category == RiskCategory.REGULATORY:
                    recommendations.append("Regulatory risk is high - consult compliance officer")
                elif category == RiskCategory.COMPLIANCE:
                    recommendations.append("Compliance risk is high - audit compliance procedures")

        # Factor-specific recommendations
        for factor in risk_factors:
            if factor.score >= 80 and factor.mitigation:
                recommendations.append(f"{factor.name}: {factor.mitigation}")

        return recommendations

    def assess_contract_risk(
        self,
        contract_data: Dict[str, Any]
    ) -> RiskAssessment:
        """
        Assess risk for a contract based on its characteristics

        Args:
            contract_data: Dictionary containing contract information
                - value: contract value in dollars
                - term_months: contract term in months
                - termination_days: notice period for termination
                - liability_cap: liability cap amount (0 if none)
                - indemnification: bool, has broad indemnification
                - arbitration: bool, has arbitration clause
                - governing_law: state governing law
                - missing_clauses: list of missing important clauses
        """
        risk_factors = []

        # Financial value risk
        value = contract_data.get('value', 0)
        if value > 1000000:
            risk_factors.append(RiskFactor(
                name="Contract Value",
                category=RiskCategory.FINANCIAL,
                score=85,
                weight=1.0,
                description=f"High contract value: ${value:,.0f}",
                mitigation="Obtain executive approval and enhanced insurance coverage"
            ))
        elif value > 500000:
            risk_factors.append(RiskFactor(
                name="Contract Value",
                category=RiskCategory.FINANCIAL,
                score=65,
                weight=1.0,
                description=f"Significant contract value: ${value:,.0f}",
                mitigation="Obtain senior management approval"
            ))
        elif value > 100000:
            risk_factors.append(RiskFactor(
                name="Contract Value",
                category=RiskCategory.FINANCIAL,
                score=40,
                weight=0.8,
                description=f"Moderate contract value: ${value:,.0f}"
            ))

        # Term risk
        term_months = contract_data.get('term_months', 0)
        if term_months > 60:
            risk_factors.append(RiskFactor(
                name="Contract Term",
                category=RiskCategory.CONTRACTUAL,
                score=70,
                weight=0.7,
                description=f"Long-term commitment: {term_months} months",
                mitigation="Negotiate break clauses or periodic review terms"
            ))
        elif term_months > 36:
            risk_factors.append(RiskFactor(
                name="Contract Term",
                category=RiskCategory.CONTRACTUAL,
                score=50,
                weight=0.6,
                description=f"Multi-year commitment: {term_months} months"
            ))

        # Termination risk
        termination_days = contract_data.get('termination_days', 30)
        if termination_days == 0:
            risk_factors.append(RiskFactor(
                name="Termination Terms",
                category=RiskCategory.LEGAL,
                score=90,
                weight=0.9,
                description="No termination provision or immediate termination only",
                mitigation="Negotiate for termination for convenience with reasonable notice"
            ))
        elif termination_days > 180:
            risk_factors.append(RiskFactor(
                name="Termination Terms",
                category=RiskCategory.LEGAL,
                score=60,
                weight=0.7,
                description=f"Long termination notice period: {termination_days} days"
            ))

        # Liability cap risk
        liability_cap = contract_data.get('liability_cap', 0)
        if liability_cap == 0:
            risk_factors.append(RiskFactor(
                name="Liability Cap",
                category=RiskCategory.LEGAL,
                score=95,
                weight=1.0,
                description="Unlimited liability - no cap",
                mitigation="CRITICAL: Negotiate for liability cap equal to contract value"
            ))
        elif liability_cap < value:
            cap_ratio = liability_cap / value if value > 0 else 0
            if cap_ratio < 0.5:
                risk_factors.append(RiskFactor(
                    name="Liability Cap",
                    category=RiskCategory.LEGAL,
                    score=35,
                    weight=0.6,
                    description=f"Liability capped at ${liability_cap:,.0f} ({cap_ratio*100:.0f}% of contract value)"
                ))

        # Indemnification risk
        if contract_data.get('indemnification', False):
            risk_factors.append(RiskFactor(
                name="Indemnification",
                category=RiskCategory.LEGAL,
                score=70,
                weight=0.8,
                description="Broad indemnification obligations",
                mitigation="Limit indemnification to own negligence and willful misconduct"
            ))

        # Arbitration risk
        if contract_data.get('arbitration', False):
            risk_factors.append(RiskFactor(
                name="Arbitration Clause",
                category=RiskCategory.LEGAL,
                score=55,
                weight=0.5,
                description="Binding arbitration required",
                mitigation="Ensure arbitration rules and location are acceptable"
            ))

        # Governing law risk
        governing_law = contract_data.get('governing_law', '')
        if governing_law and governing_law not in ['Delaware', 'New York', 'California']:
            risk_factors.append(RiskFactor(
                name="Governing Law",
                category=RiskCategory.LEGAL,
                score=45,
                weight=0.4,
                description=f"Governed by {governing_law} law (less familiar jurisdiction)"
            ))

        # Missing clauses risk
        missing_clauses = contract_data.get('missing_clauses', [])
        if missing_clauses:
            score = min(85, 40 + (len(missing_clauses) * 10))
            risk_factors.append(RiskFactor(
                name="Missing Clauses",
                category=RiskCategory.LEGAL,
                score=score,
                weight=0.9,
                description=f"Missing {len(missing_clauses)} important clauses: {', '.join(missing_clauses)}",
                mitigation="Add standard protective clauses before signing"
            ))

        return self.calculate_overall_risk(risk_factors)

    def assess_compliance_risk(
        self,
        compliance_data: Dict[str, Any]
    ) -> RiskAssessment:
        """
        Assess compliance risk for a transaction or entity

        Args:
            compliance_data: Dictionary containing compliance information
                - overdue_items: number of overdue compliance items
                - pending_items: number of pending items
                - last_audit_days_ago: days since last audit
                - violations: number of past violations
                - high_risk_jurisdictions: number of high-risk jurisdictions
                - kyc_complete: bool, KYC/AML complete
                - licenses_current: bool, all licenses current
        """
        risk_factors = []

        # Overdue compliance items
        overdue = compliance_data.get('overdue_items', 0)
        if overdue > 10:
            risk_factors.append(RiskFactor(
                name="Overdue Compliance Items",
                category=RiskCategory.COMPLIANCE,
                score=90,
                weight=1.0,
                description=f"{overdue} overdue compliance items",
                mitigation="URGENT: Address all overdue items immediately"
            ))
        elif overdue > 5:
            risk_factors.append(RiskFactor(
                name="Overdue Compliance Items",
                category=RiskCategory.COMPLIANCE,
                score=70,
                weight=0.9,
                description=f"{overdue} overdue compliance items",
                mitigation="Create action plan to resolve overdue items"
            ))
        elif overdue > 0:
            risk_factors.append(RiskFactor(
                name="Overdue Compliance Items",
                category=RiskCategory.COMPLIANCE,
                score=50,
                weight=0.7,
                description=f"{overdue} overdue compliance items"
            ))

        # Audit recency
        last_audit = compliance_data.get('last_audit_days_ago', 0)
        if last_audit > 730:  # 2 years
            risk_factors.append(RiskFactor(
                name="Audit History",
                category=RiskCategory.COMPLIANCE,
                score=75,
                weight=0.7,
                description=f"Last audit was {last_audit} days ago (over 2 years)",
                mitigation="Schedule comprehensive compliance audit"
            ))
        elif last_audit > 365:  # 1 year
            risk_factors.append(RiskFactor(
                name="Audit History",
                category=RiskCategory.COMPLIANCE,
                score=50,
                weight=0.6,
                description=f"Last audit was {last_audit} days ago"
            ))

        # Past violations
        violations = compliance_data.get('violations', 0)
        if violations > 0:
            score = min(95, 60 + (violations * 10))
            risk_factors.append(RiskFactor(
                name="Compliance Violations",
                category=RiskCategory.REGULATORY,
                score=score,
                weight=0.95,
                description=f"{violations} compliance violations in history",
                mitigation="Review and remediate root causes of violations"
            ))

        # KYC/AML completion
        if not compliance_data.get('kyc_complete', False):
            risk_factors.append(RiskFactor(
                name="KYC/AML",
                category=RiskCategory.REGULATORY,
                score=85,
                weight=0.9,
                description="KYC/AML procedures not complete",
                mitigation="Complete KYC/AML verification before proceeding"
            ))

        # License status
        if not compliance_data.get('licenses_current', False):
            risk_factors.append(RiskFactor(
                name="Licensing",
                category=RiskCategory.REGULATORY,
                score=80,
                weight=0.85,
                description="Licenses not current or expired",
                mitigation="Renew all required licenses immediately"
            ))

        # High-risk jurisdictions
        high_risk_jurisdictions = compliance_data.get('high_risk_jurisdictions', 0)
        if high_risk_jurisdictions > 0:
            score = min(90, 55 + (high_risk_jurisdictions * 15))
            risk_factors.append(RiskFactor(
                name="Jurisdictional Risk",
                category=RiskCategory.REGULATORY,
                score=score,
                weight=0.8,
                description=f"Operating in {high_risk_jurisdictions} high-risk jurisdictions",
                mitigation="Enhanced due diligence for high-risk jurisdictions"
            ))

        return self.calculate_overall_risk(risk_factors)

    def assess_property_risk(
        self,
        property_data: Dict[str, Any]
    ) -> RiskAssessment:
        """
        Assess risk for a real estate property investment

        Args:
            property_data: Dictionary containing property information
                - age_years: age of property
                - condition_score: 1-10 condition rating
                - location_crime_rate: crime rate per 1000
                - flood_zone: bool, in flood zone
                - environmental_issues: bool, known environmental issues
                - title_issues: bool, title problems
                - zoning_compliant: bool, complies with zoning
                - occupancy_rate: 0-100 percentage
                - deferred_maintenance: estimated cost
        """
        risk_factors = []

        # Property age
        age = property_data.get('age_years', 0)
        if age > 50:
            risk_factors.append(RiskFactor(
                name="Property Age",
                category=RiskCategory.OPERATIONAL,
                score=65,
                weight=0.7,
                description=f"Property is {age} years old",
                mitigation="Obtain thorough property inspection and structural assessment"
            ))
        elif age > 30:
            risk_factors.append(RiskFactor(
                name="Property Age",
                category=RiskCategory.OPERATIONAL,
                score=45,
                weight=0.5,
                description=f"Property is {age} years old"
            ))

        # Property condition
        condition = property_data.get('condition_score', 5)
        if condition <= 3:
            risk_factors.append(RiskFactor(
                name="Property Condition",
                category=RiskCategory.OPERATIONAL,
                score=85,
                weight=0.9,
                description=f"Poor property condition (score: {condition}/10)",
                mitigation="Budget for significant repairs and renovations"
            ))
        elif condition <= 5:
            risk_factors.append(RiskFactor(
                name="Property Condition",
                category=RiskCategory.OPERATIONAL,
                score=55,
                weight=0.7,
                description=f"Fair property condition (score: {condition}/10)"
            ))

        # Flood zone
        if property_data.get('flood_zone', False):
            risk_factors.append(RiskFactor(
                name="Flood Risk",
                category=RiskCategory.OPERATIONAL,
                score=75,
                weight=0.8,
                description="Property in designated flood zone",
                mitigation="Obtain flood insurance and flood mitigation assessment"
            ))

        # Environmental issues
        if property_data.get('environmental_issues', False):
            risk_factors.append(RiskFactor(
                name="Environmental Issues",
                category=RiskCategory.LEGAL,
                score=90,
                weight=1.0,
                description="Known environmental contamination or issues",
                mitigation="CRITICAL: Obtain Phase I/II environmental assessment"
            ))

        # Title issues
        if property_data.get('title_issues', False):
            risk_factors.append(RiskFactor(
                name="Title Issues",
                category=RiskCategory.LEGAL,
                score=95,
                weight=1.0,
                description="Title defects or clouds on title",
                mitigation="CRITICAL: Resolve title issues before closing"
            ))

        # Zoning compliance
        if not property_data.get('zoning_compliant', True):
            risk_factors.append(RiskFactor(
                name="Zoning Compliance",
                category=RiskCategory.REGULATORY,
                score=80,
                weight=0.9,
                description="Property not compliant with current zoning",
                mitigation="Obtain legal opinion on non-conforming use status"
            ))

        # Occupancy rate
        occupancy = property_data.get('occupancy_rate', 100)
        if occupancy < 70:
            risk_factors.append(RiskFactor(
                name="Low Occupancy",
                category=RiskCategory.FINANCIAL,
                score=75,
                weight=0.85,
                description=f"Low occupancy rate: {occupancy}%",
                mitigation="Develop leasing strategy to improve occupancy"
            ))
        elif occupancy < 85:
            risk_factors.append(RiskFactor(
                name="Below-Average Occupancy",
                category=RiskCategory.FINANCIAL,
                score=50,
                weight=0.6,
                description=f"Below-average occupancy: {occupancy}%"
            ))

        # Deferred maintenance
        deferred = property_data.get('deferred_maintenance', 0)
        if deferred > 100000:
            risk_factors.append(RiskFactor(
                name="Deferred Maintenance",
                category=RiskCategory.FINANCIAL,
                score=80,
                weight=0.85,
                description=f"Significant deferred maintenance: ${deferred:,.0f}",
                mitigation="Budget for immediate capital improvements"
            ))
        elif deferred > 50000:
            risk_factors.append(RiskFactor(
                name="Deferred Maintenance",
                category=RiskCategory.FINANCIAL,
                score=55,
                weight=0.6,
                description=f"Deferred maintenance: ${deferred:,.0f}"
            ))

        return self.calculate_overall_risk(risk_factors)


# Singleton instance
risk_scoring_service = RiskScoringService()
