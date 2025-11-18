"""Add company_id to properties table for multi-tenant isolation

Revision ID: fix_properties_company_id
Revises: d12ebefd9266
Create Date: 2025-11-16

This migration adds the company_id foreign key to the properties table
to ensure proper multi-tenant data isolation. This aligns the database
schema with the Property model definition.
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'fix_properties_company_id'
down_revision = 'd12ebefd9266'
branch_labels = None
depends_on = None


def upgrade():
    """Add company_id column to properties table."""
    # Add company_id column (nullable initially to allow for data migration)
    op.add_column(
        'properties',
        sa.Column(
            'company_id',
            postgresql.UUID(as_uuid=True),
            nullable=True,  # Temporarily nullable
            comment='Company that owns this property (for multi-tenant isolation)'
        )
    )

    # Add foreign key constraint
    op.create_foreign_key(
        'fk_properties_company_id_companies',
        'properties',
        'companies',
        ['company_id'],
        ['id'],
        ondelete='CASCADE'
    )

    # Add index for performance
    op.create_index(
        'ix_properties_company_id',
        'properties',
        ['company_id']
    )

    # Note: If there are existing properties in the database, you would need to
    # assign them to a company before making the column NOT NULL.
    # Since the database currently has 0 properties, we can safely make it NOT NULL.

    # Make company_id NOT NULL (matches the model definition)
    op.alter_column(
        'properties',
        'company_id',
        nullable=False
    )


def downgrade():
    """Remove company_id column from properties table."""
    op.drop_index('ix_properties_company_id', table_name='properties')
    op.drop_constraint('fk_properties_company_id_companies', 'properties', type_='foreignkey')
    op.drop_column('properties', 'company_id')
