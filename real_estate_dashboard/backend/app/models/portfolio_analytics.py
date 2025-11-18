"""
Portfolio Analytics Models

Database models for:
- Historical performance tracking
- Portfolio snapshots
- Risk metrics storage
- Cash flow tracking
"""

from datetime import datetime, date
from typing import Optional
from decimal import Decimal

from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Date, Text,
    Boolean, JSON, Numeric, ForeignKey, Index, CheckConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base
from app.models.database import UUIDMixin, TimestampMixin


class PerformanceMetricType(str, enum.Enum):
    """Types of performance metrics"""
    IRR = "irr"
    MOIC = "moic"  # Multiple on Invested Capital
    EQUITY_MULTIPLE = "equity_multiple"
    CASH_ON_CASH = "cash_on_cash"
    CAP_RATE = "cap_rate"
    OCCUPANCY = "occupancy"
    NOI = "noi"
    TOTAL_RETURN = "total_return"


class RiskMetricType(str, enum.Enum):
    """Types of risk metrics"""
    GEOGRAPHIC_CONCENTRATION = "geographic_concentration"
    SECTOR_CONCENTRATION = "sector_concentration"
    TENANT_CONCENTRATION = "tenant_concentration"
    LEVERAGE_RATIO = "leverage_ratio"
    DEBT_SERVICE_COVERAGE = "debt_service_coverage"
    LOAN_TO_VALUE = "loan_to_value"
    INTEREST_COVERAGE = "interest_coverage"


class PortfolioSnapshot(Base, UUIDMixin, TimestampMixin):
    """
    Historical snapshots of portfolio performance.

    Captures point-in-time metrics for tracking performance over time.
    """
    __tablename__ = "portfolio_snapshots"

    # Snapshot metadata
    snapshot_date = Column(Date, nullable=False, index=True)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=True, index=True)
    fund_id = Column(UUID(as_uuid=True), ForeignKey("funds.id"), nullable=True, index=True)

    # Portfolio composition
    total_properties = Column(Integer, default=0)
    total_units = Column(Integer, default=0)
    total_square_feet = Column(Numeric(15, 2), nullable=True)

    # Financial metrics
    total_asset_value = Column(Numeric(20, 2), nullable=False, default=0)
    total_equity = Column(Numeric(20, 2), nullable=False, default=0)
    total_debt = Column(Numeric(20, 2), nullable=False, default=0)
    total_cash = Column(Numeric(20, 2), nullable=False, default=0)

    # Income metrics
    gross_rental_income = Column(Numeric(15, 2), nullable=True)
    operating_expenses = Column(Numeric(15, 2), nullable=True)
    net_operating_income = Column(Numeric(15, 2), nullable=True)

    # Performance metrics
    portfolio_irr = Column(Float, nullable=True, comment="Internal Rate of Return (%)")
    portfolio_moic = Column(Float, nullable=True, comment="Multiple on Invested Capital")
    average_occupancy = Column(Float, nullable=True, comment="Weighted average occupancy (%)")
    average_cap_rate = Column(Float, nullable=True, comment="Weighted average cap rate (%)")

    # Risk metrics
    average_ltv = Column(Float, nullable=True, comment="Loan-to-Value ratio (%)")
    weighted_dscr = Column(Float, nullable=True, comment="Debt Service Coverage Ratio")

    # Geographic and sector breakdown
    geographic_distribution = Column(JSON, nullable=True, comment="{'state': value, ...}")
    sector_distribution = Column(JSON, nullable=True, comment="{'residential': value, ...}")
    property_type_distribution = Column(JSON, nullable=True, comment="{'multifamily': value, ...}")

    # Additional metadata
    notes = Column(Text, nullable=True)
    snapshot_metadata = Column(JSON, nullable=True)

    # Relationships
    company = relationship("Company", foreign_keys=[company_id])
    fund = relationship("Fund", foreign_keys=[fund_id])

    __table_args__ = (
        Index('idx_portfolio_snapshot_date_company', 'snapshot_date', 'company_id'),
        Index('idx_portfolio_snapshot_date_fund', 'snapshot_date', 'fund_id'),
    )


class PortfolioPerformanceMetric(Base, UUIDMixin, TimestampMixin):
    """
    Detailed performance metrics by property, fund, or portfolio level.
    """
    __tablename__ = "portfolio_performance_metrics"

    # Metric metadata
    metric_date = Column(Date, nullable=False, index=True)
    metric_type = Column(String(50), nullable=False, index=True)

    # Scope (what this metric applies to)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=True, index=True)
    fund_id = Column(UUID(as_uuid=True), ForeignKey("funds.id"), nullable=True, index=True)
    property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id"), nullable=True, index=True)

    # Metric value
    value = Column(Float, nullable=False)
    target_value = Column(Float, nullable=True, comment="Target or benchmark value")

    # Context
    period_start = Column(Date, nullable=True)
    period_end = Column(Date, nullable=True)
    calculation_method = Column(String(100), nullable=True)

    # Additional data
    breakdown = Column(JSON, nullable=True, comment="Detailed breakdown of metric calculation")
    notes = Column(Text, nullable=True)

    # Relationships
    company = relationship("Company", foreign_keys=[company_id])
    fund = relationship("Fund", foreign_keys=[fund_id])
    property = relationship("Property", foreign_keys=[property_id])

    __table_args__ = (
        Index('idx_perf_metric_date_type', 'metric_date', 'metric_type'),
        Index('idx_perf_metric_company', 'company_id', 'metric_date'),
        Index('idx_perf_metric_fund', 'fund_id', 'metric_date'),
        Index('idx_perf_metric_property', 'property_id', 'metric_date'),
    )


class CashFlowProjection(Base, UUIDMixin, TimestampMixin):
    """
    Cash flow projections for portfolio planning.

    Tracks projected income, expenses, and capital events.
    """
    __tablename__ = "cash_flow_projections"

    # Projection metadata
    projection_date = Column(Date, nullable=False, index=True)
    projection_month = Column(Integer, nullable=False, comment="Month offset from creation (0-12 for rolling 12)")

    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=True, index=True)
    fund_id = Column(UUID(as_uuid=True), ForeignKey("funds.id"), nullable=True, index=True)
    property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id"), nullable=True, index=True)

    # Income projections
    projected_rental_income = Column(Numeric(15, 2), nullable=True)
    projected_other_income = Column(Numeric(15, 2), nullable=True)
    projected_total_income = Column(Numeric(15, 2), nullable=False)

    # Expense projections
    projected_operating_expenses = Column(Numeric(15, 2), nullable=True)
    projected_capital_expenses = Column(Numeric(15, 2), nullable=True)
    projected_debt_service = Column(Numeric(15, 2), nullable=True)
    projected_total_expenses = Column(Numeric(15, 2), nullable=False)

    # Net cash flow
    projected_net_cash_flow = Column(Numeric(15, 2), nullable=False)

    # Capital events
    projected_acquisitions = Column(Numeric(15, 2), nullable=True)
    projected_dispositions = Column(Numeric(15, 2), nullable=True)
    projected_financing = Column(Numeric(15, 2), nullable=True)
    projected_capital_calls = Column(Numeric(15, 2), nullable=True)
    projected_distributions = Column(Numeric(15, 2), nullable=True)

    # Confidence and assumptions
    confidence_level = Column(String(20), nullable=True, comment="high, medium, low")
    assumptions = Column(JSON, nullable=True)
    scenario = Column(String(50), nullable=True, comment="base, optimistic, pessimistic")

    # Relationships
    company = relationship("Company", foreign_keys=[company_id])
    fund = relationship("Fund", foreign_keys=[fund_id])
    property = relationship("Property", foreign_keys=[property_id])

    __table_args__ = (
        Index('idx_cashflow_proj_date', 'projection_date', 'projection_month'),
        Index('idx_cashflow_proj_company', 'company_id', 'projection_date'),
        CheckConstraint('projection_month >= 0 AND projection_month <= 36', name='check_projection_month_range'),
    )


class PortfolioRiskMetric(Base, UUIDMixin, TimestampMixin):
    """
    Risk metrics and concentration analysis.
    """
    __tablename__ = "portfolio_risk_metrics"

    # Metric metadata
    metric_date = Column(Date, nullable=False, index=True)
    risk_type = Column(String(50), nullable=False, index=True)

    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=True, index=True)
    fund_id = Column(UUID(as_uuid=True), ForeignKey("funds.id"), nullable=True, index=True)

    # Risk metrics
    risk_score = Column(Float, nullable=False, comment="0-100 risk score")
    risk_level = Column(String(20), nullable=True, comment="low, medium, high, critical")

    # Concentration metrics
    concentration_value = Column(Float, nullable=True, comment="Concentration percentage or ratio")
    concentration_limit = Column(Float, nullable=True, comment="Policy limit for concentration")
    is_within_limit = Column(Boolean, default=True)

    # Detailed breakdown
    top_exposures = Column(JSON, nullable=True, comment="Top 5-10 concentrations")
    risk_breakdown = Column(JSON, nullable=True, comment="Detailed risk analysis")

    # Mitigation
    mitigation_strategy = Column(Text, nullable=True)
    action_items = Column(JSON, nullable=True)

    # Relationships
    company = relationship("Company", foreign_keys=[company_id])
    fund = relationship("Fund", foreign_keys=[fund_id])

    __table_args__ = (
        Index('idx_risk_metric_date_type', 'metric_date', 'risk_type'),
        Index('idx_risk_metric_company', 'company_id', 'metric_date'),
    )


class GeographicPerformance(Base, UUIDMixin, TimestampMixin):
    """
    Performance metrics by geographic location for heat maps.
    """
    __tablename__ = "geographic_performance"

    # Location data
    metric_date = Column(Date, nullable=False, index=True)
    country = Column(String(100), nullable=True, index=True)
    state = Column(String(100), nullable=True, index=True)
    city = Column(String(100), nullable=True, index=True)
    zip_code = Column(String(20), nullable=True, index=True)

    # Coordinates for mapping
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=True, index=True)

    # Portfolio composition
    property_count = Column(Integer, default=0)
    total_value = Column(Numeric(20, 2), nullable=True)
    total_square_feet = Column(Numeric(15, 2), nullable=True)

    # Performance metrics
    average_occupancy = Column(Float, nullable=True)
    average_cap_rate = Column(Float, nullable=True)
    total_noi = Column(Numeric(15, 2), nullable=True)
    irr = Column(Float, nullable=True)

    # Risk metrics
    concentration_percentage = Column(Float, nullable=True, comment="% of total portfolio")

    # Additional data
    property_types = Column(JSON, nullable=True, comment="Distribution of property types")
    market_trends = Column(JSON, nullable=True)

    # Relationships
    company = relationship("Company", foreign_keys=[company_id])

    __table_args__ = (
        Index('idx_geo_perf_date_location', 'metric_date', 'state', 'city'),
        Index('idx_geo_perf_company', 'company_id', 'metric_date'),
    )
