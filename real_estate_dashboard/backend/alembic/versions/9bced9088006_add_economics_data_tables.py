"""Add economics data tables for Sugra AI API integration

Revision ID: 9bced9088006
Revises: 8aced9077005
Create Date: 2025-11-13 14:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '9bced9088006'
down_revision: Union[str, None] = '8aced9077005'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create economics_country_overview table
    op.create_table(
        'economics_country_overview',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('country_name', sa.String(length=100), nullable=False),
        sa.Column('country_code', sa.String(length=10), nullable=True),
        sa.Column('gdp', sa.Float(), nullable=True),
        sa.Column('gdp_growth', sa.Float(), nullable=True),
        sa.Column('inflation_rate', sa.Float(), nullable=True),
        sa.Column('interest_rate', sa.Float(), nullable=True),
        sa.Column('unemployment_rate', sa.Float(), nullable=True),
        sa.Column('population', sa.Float(), nullable=True),
        sa.Column('current_account', sa.Float(), nullable=True),
        sa.Column('debt_to_gdp', sa.Float(), nullable=True),
        sa.Column('government_budget', sa.Float(), nullable=True),
        sa.Column('data_date', sa.DateTime(), nullable=True),
        sa.Column('data_source', sa.String(length=50), nullable=True),
        sa.Column('raw_data', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_economics_country_overview_country_name'), 'economics_country_overview', ['country_name'], unique=False)
    op.create_index(op.f('ix_economics_country_overview_country_code'), 'economics_country_overview', ['country_code'], unique=False)
    op.create_index(op.f('ix_economics_country_overview_data_date'), 'economics_country_overview', ['data_date'], unique=False)
    op.create_index('ix_country_date', 'economics_country_overview', ['country_name', 'data_date'], unique=False)
    op.create_unique_constraint('uq_country_overview_snapshot', 'economics_country_overview', ['country_name', 'data_date'])

    # Create economics_indicators table
    op.create_table(
        'economics_indicators',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('country_name', sa.String(length=100), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('indicator_name', sa.String(length=255), nullable=False),
        sa.Column('last_value', sa.String(length=50), nullable=True),
        sa.Column('last_value_numeric', sa.Float(), nullable=True),
        sa.Column('previous_value', sa.String(length=50), nullable=True),
        sa.Column('previous_value_numeric', sa.Float(), nullable=True),
        sa.Column('highest_value', sa.String(length=50), nullable=True),
        sa.Column('highest_value_numeric', sa.Float(), nullable=True),
        sa.Column('lowest_value', sa.String(length=50), nullable=True),
        sa.Column('lowest_value_numeric', sa.Float(), nullable=True),
        sa.Column('unit', sa.String(length=100), nullable=True),
        sa.Column('frequency', sa.String(length=50), nullable=True),
        sa.Column('reference_period', sa.String(length=50), nullable=True),
        sa.Column('data_date', sa.DateTime(), nullable=True),
        sa.Column('source', sa.String(length=255), nullable=True),
        sa.Column('raw_data', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('data_source_api', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_economics_indicators_country_name'), 'economics_indicators', ['country_name'], unique=False)
    op.create_index(op.f('ix_economics_indicators_category'), 'economics_indicators', ['category'], unique=False)
    op.create_index(op.f('ix_economics_indicators_indicator_name'), 'economics_indicators', ['indicator_name'], unique=False)
    op.create_index(op.f('ix_economics_indicators_data_date'), 'economics_indicators', ['data_date'], unique=False)
    op.create_index('ix_country_category_indicator', 'economics_indicators', ['country_name', 'category', 'indicator_name'], unique=False)
    op.create_index('ix_category_date', 'economics_indicators', ['category', 'data_date'], unique=False)
    op.create_unique_constraint('uq_indicator_snapshot', 'economics_indicators', ['country_name', 'category', 'indicator_name', 'reference_period'])

    # Create economics_indicator_history table
    op.create_table(
        'economics_indicator_history',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('country_name', sa.String(length=100), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('indicator_name', sa.String(length=255), nullable=False),
        sa.Column('observation_date', sa.DateTime(), nullable=False),
        sa.Column('value', sa.String(length=50), nullable=True),
        sa.Column('value_numeric', sa.Float(), nullable=True),
        sa.Column('unit', sa.String(length=100), nullable=True),
        sa.Column('change_from_previous', sa.Float(), nullable=True),
        sa.Column('change_percent', sa.Float(), nullable=True),
        sa.Column('frequency', sa.String(length=50), nullable=True),
        sa.Column('source', sa.String(length=255), nullable=True),
        sa.Column('data_source_api', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_economics_indicator_history_country_name'), 'economics_indicator_history', ['country_name'], unique=False)
    op.create_index(op.f('ix_economics_indicator_history_category'), 'economics_indicator_history', ['category'], unique=False)
    op.create_index(op.f('ix_economics_indicator_history_indicator_name'), 'economics_indicator_history', ['indicator_name'], unique=False)
    op.create_index(op.f('ix_economics_indicator_history_observation_date'), 'economics_indicator_history', ['observation_date'], unique=False)
    op.create_index('ix_history_country_indicator_date', 'economics_indicator_history', ['country_name', 'indicator_name', 'observation_date'], unique=False)
    op.create_index('ix_history_category_date', 'economics_indicator_history', ['category', 'observation_date'], unique=False)
    op.create_unique_constraint('uq_indicator_history_point', 'economics_indicator_history', ['country_name', 'indicator_name', 'observation_date'])

    # Create economics_fetch_log table
    op.create_table(
        'economics_fetch_log',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('endpoint', sa.String(length=255), nullable=False),
        sa.Column('country', sa.String(length=100), nullable=True),
        sa.Column('category', sa.String(length=50), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('records_fetched', sa.Integer(), nullable=True),
        sa.Column('records_stored', sa.Integer(), nullable=True),
        sa.Column('response_time_ms', sa.Integer(), nullable=True),
        sa.Column('cache_hit', sa.String(length=20), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('error_details', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('fetch_timestamp', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('triggered_by', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_economics_fetch_log_country'), 'economics_fetch_log', ['country'], unique=False)
    op.create_index(op.f('ix_economics_fetch_log_category'), 'economics_fetch_log', ['category'], unique=False)
    op.create_index('ix_fetch_log_timestamp', 'economics_fetch_log', ['fetch_timestamp'], unique=False)
    op.create_index('ix_fetch_log_status', 'economics_fetch_log', ['status', 'fetch_timestamp'], unique=False)

    # Create economics_cache_metadata table
    op.create_table(
        'economics_cache_metadata',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('cache_key', sa.String(length=255), nullable=False),
        sa.Column('country', sa.String(length=100), nullable=True),
        sa.Column('category', sa.String(length=50), nullable=True),
        sa.Column('last_fetched', sa.DateTime(), nullable=True),
        sa.Column('last_accessed', sa.DateTime(), nullable=True),
        sa.Column('access_count', sa.Integer(), nullable=True),
        sa.Column('record_count', sa.Integer(), nullable=True),
        sa.Column('data_quality', sa.String(length=20), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('ttl_seconds', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('cache_key')
    )
    op.create_index(op.f('ix_economics_cache_metadata_cache_key'), 'economics_cache_metadata', ['cache_key'], unique=True)
    op.create_index(op.f('ix_economics_cache_metadata_country'), 'economics_cache_metadata', ['country'], unique=False)
    op.create_index(op.f('ix_economics_cache_metadata_category'), 'economics_cache_metadata', ['category'], unique=False)
    op.create_index('ix_cache_expires', 'economics_cache_metadata', ['expires_at'], unique=False)
    op.create_index('ix_cache_country_category', 'economics_cache_metadata', ['country', 'category'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('economics_cache_metadata')
    op.drop_table('economics_fetch_log')
    op.drop_table('economics_indicator_history')
    op.drop_table('economics_indicators')
    op.drop_table('economics_country_overview')
