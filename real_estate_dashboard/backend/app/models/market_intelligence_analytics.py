"""
Enhanced Market Intelligence Models for Analytics

Additional models for storing analytical data, trends, correlations,
and derived metrics for deeper market intelligence analysis.
"""

from datetime import datetime, date
from typing import Optional
from decimal import Decimal

from sqlalchemy import Column, Integer, String, Float, DateTime, Date, Text, Boolean, JSON, Numeric, Index, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class MarketTrend(Base):
    """
    Time-series trends and moving averages for market indicators
    Tracks momentum, volatility, and directional changes
    """
    __tablename__ = "market_trends"

    id = Column(Integer, primary_key=True, index=True)

    # Indicator identification
    indicator_type = Column(String(50), nullable=False, index=True)  # stock, reit, index, rate, economic
    indicator_symbol = Column(String(50), nullable=False, index=True)  # Ticker or indicator code
    indicator_name = Column(String(200))

    # Time period
    analysis_date = Column(Date, nullable=False, index=True)
    period_type = Column(String(20), nullable=False, index=True)  # daily, weekly, monthly, quarterly

    # Current value
    current_value = Column(Numeric(20, 6))
    previous_value = Column(Numeric(20, 6))

    # Moving averages
    ma_5_day = Column(Numeric(20, 6))
    ma_10_day = Column(Numeric(20, 6))
    ma_20_day = Column(Numeric(20, 6))
    ma_50_day = Column(Numeric(20, 6))
    ma_200_day = Column(Numeric(20, 6))

    # Percentage changes
    change_1_day_pct = Column(Numeric(10, 4))
    change_5_day_pct = Column(Numeric(10, 4))
    change_1_month_pct = Column(Numeric(10, 4))
    change_3_month_pct = Column(Numeric(10, 4))
    change_6_month_pct = Column(Numeric(10, 4))
    change_1_year_pct = Column(Numeric(10, 4))
    change_ytd_pct = Column(Numeric(10, 4))

    # Volatility measures
    volatility_daily = Column(Numeric(10, 6))  # Standard deviation
    volatility_weekly = Column(Numeric(10, 6))
    volatility_monthly = Column(Numeric(10, 6))

    # Momentum indicators
    rsi_14 = Column(Numeric(10, 4))  # Relative Strength Index
    momentum_score = Column(Numeric(10, 4))  # -100 to +100
    trend_direction = Column(String(20))  # bullish, bearish, neutral, choppy

    # Statistical measures
    z_score = Column(Numeric(10, 4))  # Standard deviations from mean
    percentile_rank = Column(Numeric(5, 2))  # 0-100

    # Anomaly detection
    is_anomaly = Column(Boolean, default=False)
    anomaly_score = Column(Numeric(10, 4))  # Severity of anomaly
    anomaly_reason = Column(Text)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index('idx_trend_symbol_date', 'indicator_symbol', 'analysis_date'),
        Index('idx_trend_type_date', 'indicator_type', 'analysis_date'),
    )


class MarketCorrelation(Base):
    """
    Correlation tracking between different market indicators
    Helps identify relationships and leading indicators
    """
    __tablename__ = "market_correlations"

    id = Column(Integer, primary_key=True, index=True)

    # Indicator pair
    indicator_1_type = Column(String(50), nullable=False)
    indicator_1_symbol = Column(String(50), nullable=False)
    indicator_1_name = Column(String(200))

    indicator_2_type = Column(String(50), nullable=False)
    indicator_2_symbol = Column(String(50), nullable=False)
    indicator_2_name = Column(String(200))

    # Time period
    analysis_start_date = Column(Date, nullable=False)
    analysis_end_date = Column(Date, nullable=False, index=True)
    period_days = Column(Integer)

    # Correlation metrics
    pearson_correlation = Column(Numeric(10, 6))  # -1 to +1
    spearman_correlation = Column(Numeric(10, 6))
    kendall_tau = Column(Numeric(10, 6))

    # Statistical significance
    p_value = Column(Numeric(10, 6))
    is_significant = Column(Boolean)  # p < 0.05
    confidence_level = Column(Numeric(5, 2))

    # Relationship strength
    correlation_strength = Column(String(20))  # strong, moderate, weak, none
    correlation_direction = Column(String(20))  # positive, negative, none

    # Lag analysis
    optimal_lag_days = Column(Integer)  # Best lag for maximum correlation
    lagged_correlation = Column(Numeric(10, 6))

    # Interpretation
    interpretation = Column(Text)
    trading_signal = Column(String(20))  # leading, lagging, coincident

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index('idx_corr_pair', 'indicator_1_symbol', 'indicator_2_symbol'),
        Index('idx_corr_date', 'analysis_end_date'),
    )


class MarketInsight(Base):
    """
    AI-generated and rule-based market insights
    Stores actionable intelligence and alerts
    """
    __tablename__ = "market_insights"

    id = Column(Integer, primary_key=True, index=True)

    # Insight classification
    insight_type = Column(String(50), nullable=False, index=True)  # trend, anomaly, opportunity, risk, alert
    severity = Column(String(20), index=True)  # critical, high, medium, low, info
    category = Column(String(50), index=True)  # housing, rates, employment, reits, general

    # Content
    title = Column(String(500), nullable=False)
    summary = Column(Text)
    detailed_analysis = Column(Text)

    # Related indicators
    primary_indicator = Column(String(50))
    related_indicators = Column(JSON)  # Array of related symbols

    # Metrics that triggered insight
    trigger_metrics = Column(JSON)  # Key metrics that generated this insight
    confidence_score = Column(Numeric(5, 2))  # 0-100

    # Actionability
    is_actionable = Column(Boolean, default=False)
    suggested_actions = Column(JSON)  # Array of suggested actions
    impact_assessment = Column(Text)

    # Time relevance
    insight_date = Column(Date, nullable=False, index=True)
    expires_at = Column(Date)  # When insight becomes stale
    is_active = Column(Boolean, default=True)

    # Source
    generation_method = Column(String(50))  # rule_based, ml_model, llm, manual
    data_sources = Column(JSON)  # Sources used to generate insight

    # User interaction
    view_count = Column(Integer, default=0)
    is_starred = Column(Boolean, default=False)
    user_notes = Column(Text)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index('idx_insight_date_type', 'insight_date', 'insight_type'),
        Index('idx_insight_severity', 'severity', 'is_active'),
    )


class DataQualityMetric(Base):
    """
    Track data quality, completeness, and reliability over time
    """
    __tablename__ = "data_quality_metrics"

    id = Column(Integer, primary_key=True, index=True)

    # Source identification
    data_source = Column(String(50), nullable=False, index=True)  # yfinance, economics_api, etc.
    data_category = Column(String(50), index=True)  # reits, indices, economic, etc.

    # Time period
    measurement_date = Column(Date, nullable=False, index=True)
    measurement_time = Column(DateTime(timezone=True), nullable=False)

    # Availability metrics
    expected_data_points = Column(Integer)
    received_data_points = Column(Integer)
    missing_data_points = Column(Integer)
    completeness_pct = Column(Numeric(5, 2))

    # Quality scores (0-100)
    accuracy_score = Column(Numeric(5, 2))
    timeliness_score = Column(Numeric(5, 2))
    consistency_score = Column(Numeric(5, 2))
    overall_quality_score = Column(Numeric(5, 2))

    # Latency
    fetch_duration_ms = Column(Integer)
    api_response_time_ms = Column(Integer)

    # Error tracking
    error_count = Column(Integer, default=0)
    warning_count = Column(Integer, default=0)
    error_rate_pct = Column(Numeric(5, 2))

    # Reliability
    uptime_pct = Column(Numeric(5, 2))
    success_rate_pct = Column(Numeric(5, 2))

    # Issues
    issues_detected = Column(JSON)  # Array of issue descriptions
    data_anomalies = Column(JSON)  # Detected anomalies

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index('idx_quality_source_date', 'data_source', 'measurement_date'),
    )


class MarketAnalyticsCache(Base):
    """
    Pre-calculated analytics for fast query performance
    Updated daily or on-demand
    """
    __tablename__ = "market_analytics_cache"

    id = Column(Integer, primary_key=True, index=True)

    # Cache key
    cache_key = Column(String(200), nullable=False, unique=True, index=True)
    cache_category = Column(String(50), index=True)

    # Analysis type
    analysis_type = Column(String(50), nullable=False)  # summary, comparison, ranking, forecast
    time_period = Column(String(20))  # daily, weekly, monthly, ytd, 1y, 3y, 5y

    # Cached results
    result_data = Column(JSON, nullable=False)  # The pre-calculated results
    result_metadata = Column(JSON)  # Metadata about the calculation

    # Freshness
    calculated_at = Column(DateTime(timezone=True), nullable=False)
    data_as_of = Column(Date)
    expires_at = Column(DateTime(timezone=True))
    is_valid = Column(Boolean, default=True)

    # Performance
    calculation_duration_ms = Column(Integer)
    source_records_count = Column(Integer)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index('idx_cache_category_valid', 'cache_category', 'is_valid'),
        Index('idx_cache_expires', 'expires_at'),
    )


class MarketScenarioAnalysis(Base):
    """
    Store scenario analyses and what-if projections
    """
    __tablename__ = "market_scenario_analyses"

    id = Column(Integer, primary_key=True, index=True)

    # Scenario identification
    scenario_name = Column(String(200), nullable=False)
    scenario_type = Column(String(50), index=True)  # base, optimistic, pessimistic, stress
    category = Column(String(50))  # interest_rates, economic_growth, housing_market

    # Base assumptions
    base_date = Column(Date, nullable=False)
    projection_period_months = Column(Integer)
    key_assumptions = Column(JSON)  # Dict of assumption variables

    # Input parameters
    interest_rate_change_bps = Column(Integer)
    gdp_growth_pct = Column(Numeric(10, 4))
    inflation_rate_pct = Column(Numeric(10, 4))
    unemployment_change_pct = Column(Numeric(10, 4))
    custom_parameters = Column(JSON)

    # Projected outcomes
    projected_home_price_change_pct = Column(Numeric(10, 4))
    projected_rent_change_pct = Column(Numeric(10, 4))
    projected_reit_performance_pct = Column(Numeric(10, 4))
    projected_cap_rate_change_bps = Column(Integer)

    # Detailed projections
    monthly_projections = Column(JSON)  # Array of monthly forecast values
    confidence_intervals = Column(JSON)  # 95%, 80%, 50% bands

    # Risk assessment
    risk_level = Column(String(20))  # low, medium, high, extreme
    risk_factors = Column(JSON)  # Array of risk descriptions
    probability_pct = Column(Numeric(5, 2))  # Likelihood of scenario

    # Metadata
    created_by = Column(String(50))
    analysis_method = Column(String(50))  # model, expert, hybrid
    notes = Column(Text)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index('idx_scenario_date_type', 'base_date', 'scenario_type'),
    )


class MarketComparison(Base):
    """
    Store comparative analyses between markets, time periods, or metrics
    """
    __tablename__ = "market_comparisons"

    id = Column(Integer, primary_key=True, index=True)

    # Comparison identification
    comparison_type = Column(String(50), nullable=False, index=True)  # market_vs_market, period_vs_period, metric_vs_metric
    comparison_name = Column(String(200))

    # Entities being compared
    entity_a_type = Column(String(50))
    entity_a_identifier = Column(String(100))
    entity_a_data = Column(JSON)

    entity_b_type = Column(String(50))
    entity_b_identifier = Column(String(100))
    entity_b_data = Column(JSON)

    # Comparison date
    comparison_date = Column(Date, nullable=False, index=True)
    comparison_period = Column(String(50))  # current, mtd, qtd, ytd, 1y, 3y, 5y

    # Comparison results
    difference_absolute = Column(Numeric(20, 6))
    difference_percentage = Column(Numeric(10, 4))
    relative_performance = Column(String(20))  # outperform, underperform, inline

    # Statistical comparison
    correlation = Column(Numeric(10, 6))
    beta = Column(Numeric(10, 6))  # If comparing to benchmark
    alpha = Column(Numeric(10, 6))

    # Rankings
    rank_a = Column(Integer)
    rank_b = Column(Integer)
    total_entities = Column(Integer)

    # Detailed metrics
    comparison_metrics = Column(JSON)  # Dict of all compared metrics
    statistical_tests = Column(JSON)  # Results of statistical tests

    # Interpretation
    summary = Column(Text)
    key_differences = Column(JSON)  # Array of key difference descriptions

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index('idx_comparison_type_date', 'comparison_type', 'comparison_date'),
    )


class MarketAlert(Base):
    """
    Automated alerts for significant market events
    """
    __tablename__ = "market_alerts"

    id = Column(Integer, primary_key=True, index=True)

    # Alert classification
    alert_type = Column(String(50), nullable=False, index=True)  # threshold, trend, anomaly, correlation
    severity = Column(String(20), index=True)  # critical, high, medium, low
    priority = Column(Integer, default=3)  # 1=highest, 5=lowest

    # Alert content
    title = Column(String(500), nullable=False)
    message = Column(Text)

    # Triggering condition
    trigger_condition = Column(String(200))
    threshold_value = Column(Numeric(20, 6))
    actual_value = Column(Numeric(20, 6))
    threshold_exceeded_by = Column(Numeric(20, 6))

    # Related data
    indicator_symbol = Column(String(50), index=True)
    indicator_name = Column(String(200))
    indicator_current_value = Column(Numeric(20, 6))

    # Status
    alert_status = Column(String(20), default='active', index=True)  # active, acknowledged, resolved, dismissed
    acknowledged_at = Column(DateTime(timezone=True))
    resolved_at = Column(DateTime(timezone=True))

    # Time
    alert_date = Column(Date, nullable=False, index=True)
    alert_time = Column(DateTime(timezone=True), nullable=False)

    # Notification
    notification_sent = Column(Boolean, default=False)
    notification_channels = Column(JSON)  # email, slack, sms, etc.
    notification_sent_at = Column(DateTime(timezone=True))

    # Action items
    recommended_actions = Column(JSON)
    user_actions_taken = Column(JSON)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index('idx_alert_status_severity', 'alert_status', 'severity'),
        Index('idx_alert_date_type', 'alert_date', 'alert_type'),
    )
