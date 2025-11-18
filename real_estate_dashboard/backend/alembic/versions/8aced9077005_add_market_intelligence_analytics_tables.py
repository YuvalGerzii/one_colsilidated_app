"""Add market intelligence analytics tables

Revision ID: 8aced9077005
Revises:
Create Date: 2025-11-13 11:52:11.664674

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '8aced9077005'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create market_trends table
    op.create_table(
        'market_trends',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('indicator_type', sa.String(length=50), nullable=False),
        sa.Column('indicator_symbol', sa.String(length=50), nullable=False),
        sa.Column('indicator_name', sa.String(length=200), nullable=True),
        sa.Column('analysis_date', sa.Date(), nullable=False),
        sa.Column('period_type', sa.String(length=20), nullable=False),
        sa.Column('current_value', sa.Numeric(precision=20, scale=6), nullable=True),
        sa.Column('previous_value', sa.Numeric(precision=20, scale=6), nullable=True),
        sa.Column('ma_5_day', sa.Numeric(precision=20, scale=6), nullable=True),
        sa.Column('ma_10_day', sa.Numeric(precision=20, scale=6), nullable=True),
        sa.Column('ma_20_day', sa.Numeric(precision=20, scale=6), nullable=True),
        sa.Column('ma_50_day', sa.Numeric(precision=20, scale=6), nullable=True),
        sa.Column('ma_200_day', sa.Numeric(precision=20, scale=6), nullable=True),
        sa.Column('change_1_day_pct', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('change_5_day_pct', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('change_1_month_pct', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('change_3_month_pct', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('change_6_month_pct', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('change_1_year_pct', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('change_ytd_pct', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('volatility_daily', sa.Numeric(precision=10, scale=6), nullable=True),
        sa.Column('volatility_weekly', sa.Numeric(precision=10, scale=6), nullable=True),
        sa.Column('volatility_monthly', sa.Numeric(precision=10, scale=6), nullable=True),
        sa.Column('rsi_14', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('momentum_score', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('trend_direction', sa.String(length=20), nullable=True),
        sa.Column('z_score', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('percentile_rank', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('is_anomaly', sa.Boolean(), nullable=True),
        sa.Column('anomaly_score', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('anomaly_reason', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_market_trends_id'), 'market_trends', ['id'], unique=False)
    op.create_index(op.f('ix_market_trends_indicator_type'), 'market_trends', ['indicator_type'], unique=False)
    op.create_index(op.f('ix_market_trends_indicator_symbol'), 'market_trends', ['indicator_symbol'], unique=False)
    op.create_index(op.f('ix_market_trends_analysis_date'), 'market_trends', ['analysis_date'], unique=False)
    op.create_index(op.f('ix_market_trends_period_type'), 'market_trends', ['period_type'], unique=False)
    op.create_index('idx_trend_symbol_date', 'market_trends', ['indicator_symbol', 'analysis_date'], unique=False)
    op.create_index('idx_trend_type_date', 'market_trends', ['indicator_type', 'analysis_date'], unique=False)

    # Create market_correlations table
    op.create_table(
        'market_correlations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('indicator_1_type', sa.String(length=50), nullable=False),
        sa.Column('indicator_1_symbol', sa.String(length=50), nullable=False),
        sa.Column('indicator_1_name', sa.String(length=200), nullable=True),
        sa.Column('indicator_2_type', sa.String(length=50), nullable=False),
        sa.Column('indicator_2_symbol', sa.String(length=50), nullable=False),
        sa.Column('indicator_2_name', sa.String(length=200), nullable=True),
        sa.Column('analysis_start_date', sa.Date(), nullable=False),
        sa.Column('analysis_end_date', sa.Date(), nullable=False),
        sa.Column('period_days', sa.Integer(), nullable=True),
        sa.Column('pearson_correlation', sa.Numeric(precision=10, scale=6), nullable=True),
        sa.Column('spearman_correlation', sa.Numeric(precision=10, scale=6), nullable=True),
        sa.Column('kendall_tau', sa.Numeric(precision=10, scale=6), nullable=True),
        sa.Column('p_value', sa.Numeric(precision=10, scale=6), nullable=True),
        sa.Column('is_significant', sa.Boolean(), nullable=True),
        sa.Column('confidence_level', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('correlation_strength', sa.String(length=20), nullable=True),
        sa.Column('correlation_direction', sa.String(length=20), nullable=True),
        sa.Column('optimal_lag_days', sa.Integer(), nullable=True),
        sa.Column('lagged_correlation', sa.Numeric(precision=10, scale=6), nullable=True),
        sa.Column('interpretation', sa.Text(), nullable=True),
        sa.Column('trading_signal', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_market_correlations_id'), 'market_correlations', ['id'], unique=False)
    op.create_index(op.f('ix_market_correlations_analysis_end_date'), 'market_correlations', ['analysis_end_date'], unique=False)
    op.create_index('idx_corr_pair', 'market_correlations', ['indicator_1_symbol', 'indicator_2_symbol'], unique=False)
    op.create_index('idx_corr_date', 'market_correlations', ['analysis_end_date'], unique=False)

    # Create market_insights table
    op.create_table(
        'market_insights',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('insight_type', sa.String(length=50), nullable=False),
        sa.Column('severity', sa.String(length=20), nullable=True),
        sa.Column('category', sa.String(length=50), nullable=True),
        sa.Column('title', sa.String(length=500), nullable=False),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('detailed_analysis', sa.Text(), nullable=True),
        sa.Column('primary_indicator', sa.String(length=50), nullable=True),
        sa.Column('related_indicators', sa.JSON(), nullable=True),
        sa.Column('trigger_metrics', sa.JSON(), nullable=True),
        sa.Column('confidence_score', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('is_actionable', sa.Boolean(), nullable=True),
        sa.Column('suggested_actions', sa.JSON(), nullable=True),
        sa.Column('impact_assessment', sa.Text(), nullable=True),
        sa.Column('insight_date', sa.Date(), nullable=False),
        sa.Column('expires_at', sa.Date(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('generation_method', sa.String(length=50), nullable=True),
        sa.Column('data_sources', sa.JSON(), nullable=True),
        sa.Column('view_count', sa.Integer(), nullable=True),
        sa.Column('is_starred', sa.Boolean(), nullable=True),
        sa.Column('user_notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_market_insights_id'), 'market_insights', ['id'], unique=False)
    op.create_index(op.f('ix_market_insights_insight_type'), 'market_insights', ['insight_type'], unique=False)
    op.create_index(op.f('ix_market_insights_severity'), 'market_insights', ['severity'], unique=False)
    op.create_index(op.f('ix_market_insights_category'), 'market_insights', ['category'], unique=False)
    op.create_index(op.f('ix_market_insights_insight_date'), 'market_insights', ['insight_date'], unique=False)
    op.create_index('idx_insight_date_type', 'market_insights', ['insight_date', 'insight_type'], unique=False)
    op.create_index('idx_insight_severity', 'market_insights', ['severity', 'is_active'], unique=False)

    # Create data_quality_metrics table
    op.create_table(
        'data_quality_metrics',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('data_source', sa.String(length=50), nullable=False),
        sa.Column('data_category', sa.String(length=50), nullable=True),
        sa.Column('measurement_date', sa.Date(), nullable=False),
        sa.Column('measurement_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('expected_data_points', sa.Integer(), nullable=True),
        sa.Column('received_data_points', sa.Integer(), nullable=True),
        sa.Column('missing_data_points', sa.Integer(), nullable=True),
        sa.Column('completeness_pct', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('accuracy_score', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('timeliness_score', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('consistency_score', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('overall_quality_score', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('fetch_duration_ms', sa.Integer(), nullable=True),
        sa.Column('api_response_time_ms', sa.Integer(), nullable=True),
        sa.Column('error_count', sa.Integer(), nullable=True),
        sa.Column('warning_count', sa.Integer(), nullable=True),
        sa.Column('error_rate_pct', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('uptime_pct', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('success_rate_pct', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('issues_detected', sa.JSON(), nullable=True),
        sa.Column('data_anomalies', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_data_quality_metrics_id'), 'data_quality_metrics', ['id'], unique=False)
    op.create_index(op.f('ix_data_quality_metrics_data_source'), 'data_quality_metrics', ['data_source'], unique=False)
    op.create_index(op.f('ix_data_quality_metrics_data_category'), 'data_quality_metrics', ['data_category'], unique=False)
    op.create_index(op.f('ix_data_quality_metrics_measurement_date'), 'data_quality_metrics', ['measurement_date'], unique=False)
    op.create_index('idx_quality_source_date', 'data_quality_metrics', ['data_source', 'measurement_date'], unique=False)

    # Create market_analytics_cache table
    op.create_table(
        'market_analytics_cache',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('cache_key', sa.String(length=200), nullable=False),
        sa.Column('cache_category', sa.String(length=50), nullable=True),
        sa.Column('analysis_type', sa.String(length=50), nullable=False),
        sa.Column('time_period', sa.String(length=20), nullable=True),
        sa.Column('result_data', sa.JSON(), nullable=False),
        sa.Column('result_metadata', sa.JSON(), nullable=True),
        sa.Column('calculated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('data_as_of', sa.Date(), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_valid', sa.Boolean(), nullable=True),
        sa.Column('calculation_duration_ms', sa.Integer(), nullable=True),
        sa.Column('source_records_count', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('cache_key')
    )
    op.create_index(op.f('ix_market_analytics_cache_id'), 'market_analytics_cache', ['id'], unique=False)
    op.create_index(op.f('ix_market_analytics_cache_cache_key'), 'market_analytics_cache', ['cache_key'], unique=True)
    op.create_index(op.f('ix_market_analytics_cache_cache_category'), 'market_analytics_cache', ['cache_category'], unique=False)
    op.create_index('idx_cache_category_valid', 'market_analytics_cache', ['cache_category', 'is_valid'], unique=False)
    op.create_index('idx_cache_expires', 'market_analytics_cache', ['expires_at'], unique=False)

    # Create market_scenario_analyses table
    op.create_table(
        'market_scenario_analyses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('scenario_name', sa.String(length=200), nullable=False),
        sa.Column('scenario_type', sa.String(length=50), nullable=True),
        sa.Column('category', sa.String(length=50), nullable=True),
        sa.Column('base_date', sa.Date(), nullable=False),
        sa.Column('projection_period_months', sa.Integer(), nullable=True),
        sa.Column('key_assumptions', sa.JSON(), nullable=True),
        sa.Column('interest_rate_change_bps', sa.Integer(), nullable=True),
        sa.Column('gdp_growth_pct', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('inflation_rate_pct', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('unemployment_change_pct', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('custom_parameters', sa.JSON(), nullable=True),
        sa.Column('projected_home_price_change_pct', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('projected_rent_change_pct', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('projected_reit_performance_pct', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('projected_cap_rate_change_bps', sa.Integer(), nullable=True),
        sa.Column('monthly_projections', sa.JSON(), nullable=True),
        sa.Column('confidence_intervals', sa.JSON(), nullable=True),
        sa.Column('risk_level', sa.String(length=20), nullable=True),
        sa.Column('risk_factors', sa.JSON(), nullable=True),
        sa.Column('probability_pct', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('created_by', sa.String(length=50), nullable=True),
        sa.Column('analysis_method', sa.String(length=50), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_market_scenario_analyses_id'), 'market_scenario_analyses', ['id'], unique=False)
    op.create_index(op.f('ix_market_scenario_analyses_scenario_type'), 'market_scenario_analyses', ['scenario_type'], unique=False)
    op.create_index('idx_scenario_date_type', 'market_scenario_analyses', ['base_date', 'scenario_type'], unique=False)

    # Create market_comparisons table
    op.create_table(
        'market_comparisons',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('comparison_type', sa.String(length=50), nullable=False),
        sa.Column('comparison_name', sa.String(length=200), nullable=True),
        sa.Column('entity_a_type', sa.String(length=50), nullable=True),
        sa.Column('entity_a_identifier', sa.String(length=100), nullable=True),
        sa.Column('entity_a_data', sa.JSON(), nullable=True),
        sa.Column('entity_b_type', sa.String(length=50), nullable=True),
        sa.Column('entity_b_identifier', sa.String(length=100), nullable=True),
        sa.Column('entity_b_data', sa.JSON(), nullable=True),
        sa.Column('comparison_date', sa.Date(), nullable=False),
        sa.Column('comparison_period', sa.String(length=50), nullable=True),
        sa.Column('difference_absolute', sa.Numeric(precision=20, scale=6), nullable=True),
        sa.Column('difference_percentage', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('relative_performance', sa.String(length=20), nullable=True),
        sa.Column('correlation', sa.Numeric(precision=10, scale=6), nullable=True),
        sa.Column('beta', sa.Numeric(precision=10, scale=6), nullable=True),
        sa.Column('alpha', sa.Numeric(precision=10, scale=6), nullable=True),
        sa.Column('rank_a', sa.Integer(), nullable=True),
        sa.Column('rank_b', sa.Integer(), nullable=True),
        sa.Column('total_entities', sa.Integer(), nullable=True),
        sa.Column('comparison_metrics', sa.JSON(), nullable=True),
        sa.Column('statistical_tests', sa.JSON(), nullable=True),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('key_differences', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_market_comparisons_id'), 'market_comparisons', ['id'], unique=False)
    op.create_index(op.f('ix_market_comparisons_comparison_type'), 'market_comparisons', ['comparison_type'], unique=False)
    op.create_index(op.f('ix_market_comparisons_comparison_date'), 'market_comparisons', ['comparison_date'], unique=False)
    op.create_index('idx_comparison_type_date', 'market_comparisons', ['comparison_type', 'comparison_date'], unique=False)

    # Create market_alerts table
    op.create_table(
        'market_alerts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('alert_type', sa.String(length=50), nullable=False),
        sa.Column('severity', sa.String(length=20), nullable=True),
        sa.Column('priority', sa.Integer(), nullable=True),
        sa.Column('title', sa.String(length=500), nullable=False),
        sa.Column('message', sa.Text(), nullable=True),
        sa.Column('trigger_condition', sa.String(length=200), nullable=True),
        sa.Column('threshold_value', sa.Numeric(precision=20, scale=6), nullable=True),
        sa.Column('actual_value', sa.Numeric(precision=20, scale=6), nullable=True),
        sa.Column('threshold_exceeded_by', sa.Numeric(precision=20, scale=6), nullable=True),
        sa.Column('indicator_symbol', sa.String(length=50), nullable=True),
        sa.Column('indicator_name', sa.String(length=200), nullable=True),
        sa.Column('indicator_current_value', sa.Numeric(precision=20, scale=6), nullable=True),
        sa.Column('alert_status', sa.String(length=20), nullable=True),
        sa.Column('acknowledged_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('resolved_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('alert_date', sa.Date(), nullable=False),
        sa.Column('alert_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('notification_sent', sa.Boolean(), nullable=True),
        sa.Column('notification_channels', sa.JSON(), nullable=True),
        sa.Column('notification_sent_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('recommended_actions', sa.JSON(), nullable=True),
        sa.Column('user_actions_taken', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_market_alerts_id'), 'market_alerts', ['id'], unique=False)
    op.create_index(op.f('ix_market_alerts_alert_type'), 'market_alerts', ['alert_type'], unique=False)
    op.create_index(op.f('ix_market_alerts_severity'), 'market_alerts', ['severity'], unique=False)
    op.create_index(op.f('ix_market_alerts_indicator_symbol'), 'market_alerts', ['indicator_symbol'], unique=False)
    op.create_index(op.f('ix_market_alerts_alert_status'), 'market_alerts', ['alert_status'], unique=False)
    op.create_index(op.f('ix_market_alerts_alert_date'), 'market_alerts', ['alert_date'], unique=False)
    op.create_index('idx_alert_status_severity', 'market_alerts', ['alert_status', 'severity'], unique=False)
    op.create_index('idx_alert_date_type', 'market_alerts', ['alert_date', 'alert_type'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('market_alerts')
    op.drop_table('market_comparisons')
    op.drop_table('market_scenario_analyses')
    op.drop_table('market_analytics_cache')
    op.drop_table('data_quality_metrics')
    op.drop_table('market_insights')
    op.drop_table('market_correlations')
    op.drop_table('market_trends')
