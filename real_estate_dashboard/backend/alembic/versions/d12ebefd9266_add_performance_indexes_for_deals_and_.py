"""add_performance_indexes_for_deals_and_users

Revision ID: d12ebefd9266
Revises: e256581b7a09
Create Date: 2025-11-15 17:57:53.673953

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd12ebefd9266'
down_revision: Union[str, None] = 'e256581b7a09'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Deals table indexes - Improve query performance for filtering and searching
    op.create_index('idx_deals_type_stage', 'deals', ['deal_type', 'stage'], unique=False)
    op.create_index('idx_deals_status_priority', 'deals', ['status', 'priority'], unique=False)
    op.create_index('idx_deals_company_id', 'deals', ['company_id'], unique=False)
    op.create_index('idx_deals_stage', 'deals', ['stage'], unique=False)
    op.create_index('idx_deals_status', 'deals', ['status'], unique=False)
    op.create_index('idx_deals_type', 'deals', ['deal_type'], unique=False)
    op.create_index('idx_deals_created_at', 'deals', ['created_at'], unique=False)

    # Users table indexes - Improve login and lookup performance
    op.create_index('idx_users_email', 'users', ['email'], unique=True)
    op.create_index('idx_users_username', 'users', ['username'], unique=True)
    op.create_index('idx_users_company_active', 'users', ['company_id', 'is_active'], unique=False)
    op.create_index('idx_users_is_active', 'users', ['is_active'], unique=False)
    op.create_index('idx_users_is_superuser', 'users', ['is_superuser'], unique=False)


def downgrade() -> None:
    # Remove indexes in reverse order
    op.drop_index('idx_users_is_superuser', table_name='users')
    op.drop_index('idx_users_is_active', table_name='users')
    op.drop_index('idx_users_company_active', table_name='users')
    op.drop_index('idx_users_username', table_name='users')
    op.drop_index('idx_users_email', table_name='users')

    op.drop_index('idx_deals_created_at', table_name='deals')
    op.drop_index('idx_deals_type', table_name='deals')
    op.drop_index('idx_deals_status', table_name='deals')
    op.drop_index('idx_deals_stage', table_name='deals')
    op.drop_index('idx_deals_company_id', table_name='deals')
    op.drop_index('idx_deals_status_priority', table_name='deals')
    op.drop_index('idx_deals_type_stage', table_name='deals')
