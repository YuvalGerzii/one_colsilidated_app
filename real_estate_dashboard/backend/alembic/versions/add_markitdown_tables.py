"""Add MarkItDown document conversion tables

Revision ID: b9cfe8912345
Revises: 8aced9077005
Create Date: 2025-11-13 14:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b9cfe8912345'
down_revision: Union[str, None] = '8aced9077005'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create markitdown_documents table
    op.create_table(
        'markitdown_documents',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('document_name', sa.String(length=500), nullable=False),
        sa.Column('file_type', sa.String(length=50), nullable=False),
        sa.Column('mime_type', sa.String(length=100), nullable=True),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('company_name', sa.String(length=255), nullable=True),
        sa.Column('project_name', sa.String(length=255), nullable=True),
        sa.Column('file_path', sa.String(length=1000), nullable=False),
        sa.Column('file_size_kb', sa.Integer(), nullable=True),
        sa.Column('file_hash', sa.String(length=64), nullable=True),
        sa.Column('upload_date', sa.DateTime(), nullable=False),
        sa.Column('uploaded_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('conversion_status', sa.String(length=50), nullable=False),
        sa.Column('conversion_method', sa.String(length=50), nullable=True),
        sa.Column('conversion_started', sa.DateTime(), nullable=True),
        sa.Column('conversion_completed', sa.DateTime(), nullable=True),
        sa.Column('conversion_duration_ms', sa.Integer(), nullable=True),
        sa.Column('conversion_confidence', sa.Float(), nullable=True),
        sa.Column('character_count', sa.Integer(), nullable=True),
        sa.Column('word_count', sa.Integer(), nullable=True),
        sa.Column('page_count', sa.Integer(), nullable=True),
        sa.Column('llm_enhanced', sa.Boolean(), default=False),
        sa.Column('llm_model', sa.String(length=100), nullable=True),
        sa.Column('llm_tokens_used', sa.Integer(), nullable=True),
        sa.Column('needs_review', sa.Boolean(), default=False),
        sa.Column('reviewed_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('reviewed_date', sa.DateTime(), nullable=True),
        sa.Column('review_notes', sa.Text(), nullable=True),
        sa.Column('has_errors', sa.Boolean(), default=False),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('warnings', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('detected_language', sa.String(length=10), nullable=True),
        sa.Column('detected_structure', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('extracted_metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('tags', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('categories', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('keywords', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('view_count', sa.Integer(), default=0),
        sa.Column('last_viewed', sa.DateTime(), nullable=True),
        sa.Column('export_count', sa.Integer(), default=0),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='SET NULL')
    )
    op.create_index('ix_markitdown_documents_file_type', 'markitdown_documents', ['file_type'])
    op.create_index('ix_markitdown_documents_company_id', 'markitdown_documents', ['company_id'])
    op.create_index('ix_markitdown_documents_conversion_status', 'markitdown_documents', ['conversion_status'])
    op.create_index('ix_markitdown_documents_file_hash', 'markitdown_documents', ['file_hash'])
    op.create_index('ix_markitdown_documents_needs_review', 'markitdown_documents', ['needs_review'])
    op.create_index('ix_markitdown_documents_has_errors', 'markitdown_documents', ['has_errors'])

    # Create markitdown_content table
    op.create_table(
        'markitdown_content',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('document_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('markdown_text', sa.Text(), nullable=False),
        sa.Column('html_preview', sa.Text(), nullable=True),
        sa.Column('plain_text', sa.Text(), nullable=True),
        sa.Column('heading_count', sa.Integer(), nullable=True),
        sa.Column('table_count', sa.Integer(), nullable=True),
        sa.Column('image_count', sa.Integer(), nullable=True),
        sa.Column('link_count', sa.Integer(), nullable=True),
        sa.Column('code_block_count', sa.Integer(), nullable=True),
        sa.Column('tables_data', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('images_data', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('links_data', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['document_id'], ['markitdown_documents.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('document_id')
    )
    op.create_index('ix_markitdown_content_document_id', 'markitdown_content', ['document_id'], unique=True)

    # Create markitdown_versions table
    op.create_table(
        'markitdown_versions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('document_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('version_number', sa.Integer(), nullable=False),
        sa.Column('version_date', sa.DateTime(), nullable=False),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('conversion_method', sa.String(length=50), nullable=False),
        sa.Column('markdown_text', sa.Text(), nullable=False),
        sa.Column('conversion_confidence', sa.Float(), nullable=True),
        sa.Column('character_count', sa.Integer(), nullable=True),
        sa.Column('change_summary', sa.Text(), nullable=True),
        sa.Column('diff_stats', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('settings_used', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['document_id'], ['markitdown_documents.id'], ondelete='CASCADE')
    )
    op.create_index('ix_markitdown_versions_document_id', 'markitdown_versions', ['document_id'])

    # Create markitdown_batches table
    op.create_table(
        'markitdown_batches',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('batch_name', sa.String(length=255), nullable=False),
        sa.Column('batch_description', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('total_documents', sa.Integer(), default=0),
        sa.Column('completed_documents', sa.Integer(), default=0),
        sa.Column('failed_documents', sa.Integer(), default=0),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('total_duration_ms', sa.Integer(), nullable=True),
        sa.Column('conversion_settings', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('total_size_kb', sa.Integer(), nullable=True),
        sa.Column('total_characters', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_markitdown_batches_status', 'markitdown_batches', ['status'])

    # Create markitdown_analytics table
    op.create_table(
        'markitdown_analytics',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('total_conversions', sa.Integer(), default=0),
        sa.Column('successful_conversions', sa.Integer(), default=0),
        sa.Column('failed_conversions', sa.Integer(), default=0),
        sa.Column('file_type_stats', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('avg_conversion_time_ms', sa.Integer(), nullable=True),
        sa.Column('avg_file_size_kb', sa.Integer(), nullable=True),
        sa.Column('avg_output_length', sa.Integer(), nullable=True),
        sa.Column('avg_confidence_score', sa.Float(), nullable=True),
        sa.Column('documents_needing_review', sa.Integer(), default=0),
        sa.Column('llm_enhanced_count', sa.Integer(), default=0),
        sa.Column('total_llm_tokens', sa.Integer(), default=0),
        sa.Column('active_users', sa.Integer(), default=0),
        sa.Column('total_uploads', sa.Integer(), default=0),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_markitdown_analytics_date', 'markitdown_analytics', ['date'])


def downgrade() -> None:
    # Drop tables in reverse order (respecting foreign key constraints)
    op.drop_index('ix_markitdown_analytics_date', table_name='markitdown_analytics')
    op.drop_table('markitdown_analytics')

    op.drop_index('ix_markitdown_batches_status', table_name='markitdown_batches')
    op.drop_table('markitdown_batches')

    op.drop_index('ix_markitdown_versions_document_id', table_name='markitdown_versions')
    op.drop_table('markitdown_versions')

    op.drop_index('ix_markitdown_content_document_id', table_name='markitdown_content')
    op.drop_table('markitdown_content')

    op.drop_index('ix_markitdown_documents_has_errors', table_name='markitdown_documents')
    op.drop_index('ix_markitdown_documents_needs_review', table_name='markitdown_documents')
    op.drop_index('ix_markitdown_documents_file_hash', table_name='markitdown_documents')
    op.drop_index('ix_markitdown_documents_conversion_status', table_name='markitdown_documents')
    op.drop_index('ix_markitdown_documents_company_id', table_name='markitdown_documents')
    op.drop_index('ix_markitdown_documents_file_type', table_name='markitdown_documents')
    op.drop_table('markitdown_documents')
