"""
Interactive Dashboards Models

Database models for:
- Customizable dashboards with drag-and-drop widgets
- Custom KPI tracking
- Benchmark comparisons
- Performance attribution
- Interactive chart configurations
"""

from datetime import datetime, date
from typing import Optional
from decimal import Decimal
import enum

from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Date, Text,
    Boolean, JSON, Numeric, ForeignKey, Index, CheckConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.database import UUIDMixin, TimestampMixin


class DashboardType(str, enum.Enum):
    """Types of dashboards"""
    PORTFOLIO_OVERVIEW = "portfolio_overview"
    PROPERTY_PERFORMANCE = "property_performance"
    FINANCIAL_ANALYSIS = "financial_analysis"
    RISK_MANAGEMENT = "risk_management"
    MARKET_INTELLIGENCE = "market_intelligence"
    DEAL_PIPELINE = "deal_pipeline"
    FUND_PERFORMANCE = "fund_performance"
    CUSTOM = "custom"


class WidgetType(str, enum.Enum):
    """Types of dashboard widgets"""
    # Charts
    LINE_CHART = "line_chart"
    BAR_CHART = "bar_chart"
    PIE_CHART = "pie_chart"
    AREA_CHART = "area_chart"
    SCATTER_PLOT = "scatter_plot"
    HEATMAP = "heatmap"
    GAUGE = "gauge"

    # Metrics
    KPI_CARD = "kpi_card"
    METRIC_GRID = "metric_grid"
    COMPARISON_TABLE = "comparison_table"

    # Lists and Tables
    DATA_TABLE = "data_table"
    PROPERTY_LIST = "property_list"
    DEAL_LIST = "deal_list"

    # Maps
    GEOGRAPHIC_MAP = "geographic_map"

    # Other
    TEXT_WIDGET = "text_widget"
    IFRAME = "iframe"


class KPICalculationType(str, enum.Enum):
    """Types of KPI calculations"""
    SUM = "sum"
    AVERAGE = "average"
    WEIGHTED_AVERAGE = "weighted_average"
    COUNT = "count"
    PERCENTAGE = "percentage"
    RATIO = "ratio"
    GROWTH_RATE = "growth_rate"
    CUSTOM_FORMULA = "custom_formula"


class BenchmarkType(str, enum.Enum):
    """Types of benchmarks"""
    INDUSTRY_AVERAGE = "industry_average"
    PEER_GROUP = "peer_group"
    HISTORICAL_PERFORMANCE = "historical_performance"
    TARGET = "target"
    MARKET_INDEX = "market_index"


class Dashboard(Base, UUIDMixin, TimestampMixin):
    """
    Customizable dashboard configuration.

    Supports drag-and-drop widget arrangement and
    user-specific dashboard layouts.
    """
    __tablename__ = "dashboards"

    # Dashboard metadata
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    dashboard_type = Column(String(50), nullable=False, index=True)

    # Ownership
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=True, index=True)

    # Visibility and sharing
    is_public = Column(Boolean, default=False, comment="Visible to other users")
    is_default = Column(Boolean, default=False, comment="Default dashboard for this type")
    shared_with_roles = Column(JSON, nullable=True, comment="List of roles that can view this dashboard")

    # Layout configuration
    layout_config = Column(JSON, nullable=True, comment="Grid layout configuration")
    theme_config = Column(JSON, nullable=True, comment="Color scheme and styling")

    # Filters
    default_filters = Column(JSON, nullable=True, comment="Default filter values")
    allowed_filters = Column(JSON, nullable=True, comment="Available filter options")

    # Refresh and caching
    auto_refresh_interval = Column(Integer, nullable=True, comment="Auto-refresh in seconds")
    cache_duration = Column(Integer, nullable=True, comment="Cache duration in seconds")

    # Metadata
    last_viewed_at = Column(DateTime, nullable=True)
    view_count = Column(Integer, default=0)
    is_archived = Column(Boolean, default=False)

    # Relationships
    user = relationship("User", foreign_keys=[user_id])
    company = relationship("Company", foreign_keys=[company_id])
    widgets = relationship("DashboardWidget", back_populates="dashboard", cascade="all, delete-orphan")

    __table_args__ = (
        Index('idx_dashboard_user_type', 'user_id', 'dashboard_type'),
        Index('idx_dashboard_company', 'company_id', 'is_public'),
    )


class DashboardWidget(Base, UUIDMixin, TimestampMixin):
    """
    Individual widget on a dashboard.

    Supports various chart types, metrics, and data visualizations
    with drill-down capabilities.
    """
    __tablename__ = "dashboard_widgets"

    # Widget metadata
    dashboard_id = Column(UUID(as_uuid=True), ForeignKey("dashboards.id"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    widget_type = Column(String(50), nullable=False)

    # Layout and positioning
    position_x = Column(Integer, nullable=False, default=0)
    position_y = Column(Integer, nullable=False, default=0)
    width = Column(Integer, nullable=False, default=4, comment="Grid units")
    height = Column(Integer, nullable=False, default=3, comment="Grid units")

    # Data source
    data_source = Column(String(100), nullable=True, comment="API endpoint or data source")
    data_config = Column(JSON, nullable=True, comment="Query parameters and data configuration")

    # Chart configuration
    chart_config = Column(JSON, nullable=True, comment="Chart.js or visualization config")
    visualization_options = Column(JSON, nullable=True, comment="Color, legend, axes options")

    # Drill-down configuration
    drill_down_enabled = Column(Boolean, default=False)
    drill_down_config = Column(JSON, nullable=True, comment="Drill-down navigation and filters")

    # Interactivity
    clickable = Column(Boolean, default=True)
    on_click_action = Column(JSON, nullable=True, comment="Action to perform on click")

    # Filters
    local_filters = Column(JSON, nullable=True, comment="Widget-specific filters")
    inherit_dashboard_filters = Column(Boolean, default=True)

    # Refresh
    auto_refresh = Column(Boolean, default=False)
    refresh_interval = Column(Integer, nullable=True, comment="Refresh interval in seconds")

    # Metadata
    is_visible = Column(Boolean, default=True)
    order = Column(Integer, default=0, comment="Display order")

    # Relationships
    dashboard = relationship("Dashboard", back_populates="widgets")

    __table_args__ = (
        Index('idx_widget_dashboard_order', 'dashboard_id', 'order'),
        CheckConstraint('width > 0 AND width <= 12', name='check_widget_width'),
        CheckConstraint('height > 0 AND height <= 12', name='check_widget_height'),
    )


class CustomKPI(Base, UUIDMixin, TimestampMixin):
    """
    User-defined custom KPIs for tracking.

    Supports various calculation methods and comparison periods.
    """
    __tablename__ = "custom_kpis"

    # KPI metadata
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=True, index=True)

    # Ownership
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=True, index=True)

    # Calculation configuration
    calculation_type = Column(String(50), nullable=False)
    formula = Column(Text, nullable=True, comment="Custom formula for calculation")
    data_sources = Column(JSON, nullable=False, comment="Data sources for calculation")

    # Aggregation
    aggregation_period = Column(String(20), nullable=True, comment="daily, weekly, monthly, quarterly, yearly")
    calculation_config = Column(JSON, nullable=True, comment="Additional calculation parameters")

    # Target and thresholds
    target_value = Column(Numeric(20, 2), nullable=True)
    warning_threshold = Column(Numeric(20, 2), nullable=True)
    critical_threshold = Column(Numeric(20, 2), nullable=True)

    # Formatting
    unit = Column(String(20), nullable=True, comment="%, $, units, etc.")
    decimal_places = Column(Integer, default=2)
    prefix = Column(String(10), nullable=True, comment="$ or other prefix")
    suffix = Column(String(10), nullable=True, comment="% or other suffix")

    # Comparison
    compare_to_previous_period = Column(Boolean, default=True)
    show_trend = Column(Boolean, default=True)

    # Visibility
    is_public = Column(Boolean, default=False)
    shared_with_users = Column(JSON, nullable=True, comment="List of user IDs")

    # Metadata
    is_active = Column(Boolean, default=True)
    last_calculated_at = Column(DateTime, nullable=True)
    last_calculated_value = Column(Numeric(20, 2), nullable=True)

    # Relationships
    user = relationship("User", foreign_keys=[user_id])
    company = relationship("Company", foreign_keys=[company_id])

    __table_args__ = (
        Index('idx_kpi_user_category', 'user_id', 'category'),
        Index('idx_kpi_company_active', 'company_id', 'is_active'),
    )


class Benchmark(Base, UUIDMixin, TimestampMixin):
    """
    Benchmarks for comparison and performance evaluation.

    Supports industry averages, peer groups, and custom targets.
    """
    __tablename__ = "benchmarks"

    # Benchmark metadata
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    benchmark_type = Column(String(50), nullable=False, index=True)

    # Scope
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=True, index=True)
    metric_name = Column(String(100), nullable=False, index=True, comment="IRR, MOIC, occupancy, etc.")

    # Benchmark data
    value = Column(Numeric(20, 2), nullable=False)
    value_range_min = Column(Numeric(20, 2), nullable=True, comment="Lower bound")
    value_range_max = Column(Numeric(20, 2), nullable=True, comment="Upper bound")

    # Context
    geography = Column(String(100), nullable=True, comment="National, regional, city")
    property_type = Column(String(50), nullable=True, comment="Asset class")
    time_period = Column(String(50), nullable=True, comment="Quarter, year, etc.")
    as_of_date = Column(Date, nullable=False, index=True)

    # Peer group (for peer benchmarks)
    peer_group_definition = Column(JSON, nullable=True, comment="Criteria for peer selection")
    peer_count = Column(Integer, nullable=True, comment="Number of peers in comparison")

    # Data source
    data_source = Column(String(200), nullable=True, comment="NCREIF, NAREIT, custom, etc.")
    data_url = Column(String(500), nullable=True)
    confidence_level = Column(String(20), nullable=True, comment="high, medium, low")

    # Statistics
    percentile_25 = Column(Numeric(20, 2), nullable=True)
    percentile_50 = Column(Numeric(20, 2), nullable=True, comment="Median")
    percentile_75 = Column(Numeric(20, 2), nullable=True)
    mean = Column(Numeric(20, 2), nullable=True)
    standard_deviation = Column(Numeric(20, 2), nullable=True)

    # Metadata
    is_active = Column(Boolean, default=True)
    notes = Column(Text, nullable=True)

    # Relationships
    company = relationship("Company", foreign_keys=[company_id])

    __table_args__ = (
        Index('idx_benchmark_metric_date', 'metric_name', 'as_of_date'),
        Index('idx_benchmark_type_active', 'benchmark_type', 'is_active'),
    )


class PerformanceAttribution(Base, UUIDMixin, TimestampMixin):
    """
    Performance attribution analysis.

    Breaks down portfolio returns into component factors
    (asset allocation, security selection, timing, etc.).
    """
    __tablename__ = "performance_attribution"

    # Attribution metadata
    analysis_date = Column(Date, nullable=False, index=True)
    analysis_period_start = Column(Date, nullable=False)
    analysis_period_end = Column(Date, nullable=False)

    # Scope
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=True, index=True)
    fund_id = Column(UUID(as_uuid=True), ForeignKey("funds.id"), nullable=True, index=True)
    property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id"), nullable=True, index=True)

    # Total return
    total_return = Column(Numeric(10, 4), nullable=False, comment="Total portfolio return (%)")
    benchmark_return = Column(Numeric(10, 4), nullable=True, comment="Benchmark return (%)")
    excess_return = Column(Numeric(10, 4), nullable=True, comment="Return vs benchmark (%)")

    # Attribution components
    asset_allocation_effect = Column(Numeric(10, 4), nullable=True, comment="Return from asset allocation")
    security_selection_effect = Column(Numeric(10, 4), nullable=True, comment="Return from property selection")
    interaction_effect = Column(Numeric(10, 4), nullable=True, comment="Interaction between allocation and selection")

    # Geographic attribution
    geographic_attribution = Column(JSON, nullable=True, comment="Return by geography")

    # Sector attribution
    sector_attribution = Column(JSON, nullable=True, comment="Return by property type/sector")

    # Detailed breakdown
    detailed_attribution = Column(JSON, nullable=True, comment="Granular attribution data")

    # Risk-adjusted metrics
    sharpe_ratio = Column(Numeric(10, 4), nullable=True)
    sortino_ratio = Column(Numeric(10, 4), nullable=True)
    information_ratio = Column(Numeric(10, 4), nullable=True)
    tracking_error = Column(Numeric(10, 4), nullable=True, comment="Volatility of excess returns")

    # Methodology
    attribution_method = Column(String(50), nullable=True, comment="Brinson, BHB, etc.")
    calculation_notes = Column(Text, nullable=True)

    # Relationships
    company = relationship("Company", foreign_keys=[company_id])
    fund = relationship("Fund", foreign_keys=[fund_id])
    property = relationship("Property", foreign_keys=[property_id])

    __table_args__ = (
        Index('idx_perf_attr_company_date', 'company_id', 'analysis_date'),
        Index('idx_perf_attr_fund_date', 'fund_id', 'analysis_date'),
    )


class DashboardFilter(Base, UUIDMixin, TimestampMixin):
    """
    Saved filter configurations for dashboards.

    Allows users to save and quickly apply filter presets.
    """
    __tablename__ = "dashboard_filters"

    # Filter metadata
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)

    # Ownership
    dashboard_id = Column(UUID(as_uuid=True), ForeignKey("dashboards.id"), nullable=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    # Filter configuration
    filter_config = Column(JSON, nullable=False, comment="Filter values and operators")

    # Visibility
    is_public = Column(Boolean, default=False)
    is_default = Column(Boolean, default=False)

    # Usage tracking
    last_used_at = Column(DateTime, nullable=True)
    use_count = Column(Integer, default=0)

    # Relationships
    dashboard = relationship("Dashboard", foreign_keys=[dashboard_id])
    user = relationship("User", foreign_keys=[user_id])

    __table_args__ = (
        Index('idx_filter_dashboard_user', 'dashboard_id', 'user_id'),
    )
