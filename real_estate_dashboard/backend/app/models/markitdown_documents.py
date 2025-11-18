"""
MarkItDown Document Conversion Models

This module contains database models for:
- Document uploads and conversion management using MarkItDown
- Markdown content storage
- Conversion metadata and analytics
- Multi-format document processing tracking
"""

from sqlalchemy import Column, String, Float, Integer, JSON, ForeignKey, Text, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import enum
from datetime import datetime

from app.models.database import BaseModel, SoftDeleteMixin


# Enums
class MarkItDownFileType(str, enum.Enum):
    """Supported file types for MarkItDown conversion"""
    PDF = "PDF"
    WORD = "Word (docx/doc)"
    EXCEL = "Excel (xlsx/xls)"
    POWERPOINT = "PowerPoint (pptx/ppt)"
    IMAGE = "Image (jpg/png/gif/bmp)"
    HTML = "HTML"
    TEXT = "Text"
    AUDIO = "Audio"
    VIDEO = "Video"
    ZIP = "ZIP Archive"
    CSV = "CSV"
    XML = "XML"
    JSON_FILE = "JSON"
    RSS = "RSS Feed"
    IPYNB = "Jupyter Notebook"
    URL = "URL/Web Page"
    OTHER = "Other"


class ConversionStatus(str, enum.Enum):
    """Status of MarkItDown conversion"""
    PENDING = "Pending"
    PROCESSING = "Processing"
    COMPLETED = "Completed"
    FAILED = "Failed"
    PARTIAL = "Partial"  # Some content extracted but with warnings
    NEEDS_REVIEW = "Needs Review"


class ConversionMethod(str, enum.Enum):
    """Method used for conversion"""
    MARKITDOWN = "MarkItDown"
    MARKITDOWN_WITH_LLM = "MarkItDown + LLM"
    AZURE_DOC_INTEL = "Azure Document Intelligence"
    FALLBACK_TEXT = "Fallback Text Extraction"
    HYBRID = "Hybrid Multi-Method"


# Main Models

class MarkItDownDocument(BaseModel, SoftDeleteMixin):
    """
    Stores uploaded documents and MarkItDown conversion metadata

    This is the master record for any document converted using MarkItDown.
    Supports multiple file formats: PDF, Office files, images, HTML, audio, etc.
    """

    __tablename__ = "markitdown_documents"

    # Basic Info
    document_name = Column(String(500), nullable=False, comment="Original filename")
    file_type = Column(SQLEnum(MarkItDownFileType), nullable=False, index=True, comment="Detected file type")
    mime_type = Column(String(100), nullable=True, comment="MIME type from magika")

    # Company/Project Link (optional)
    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.id'), nullable=True, index=True)
    company_name = Column(String(255), nullable=True, comment="Associated company name")
    project_name = Column(String(255), nullable=True, comment="Project/folder name")

    # File Storage
    file_path = Column(String(1000), nullable=False, comment="Storage path (S3/local)")
    file_size_kb = Column(Integer, nullable=True, comment="Original file size in KB")
    file_hash = Column(String(64), nullable=True, index=True, comment="SHA-256 hash for deduplication")

    # Upload Info
    upload_date = Column(DateTime, default=datetime.utcnow, nullable=False, comment="Upload timestamp")
    uploaded_by = Column(UUID(as_uuid=True), nullable=True, comment="User who uploaded")

    # Conversion Status
    conversion_status = Column(
        SQLEnum(ConversionStatus),
        default=ConversionStatus.PENDING,
        nullable=False,
        index=True,
        comment="Current conversion status"
    )
    conversion_method = Column(
        SQLEnum(ConversionMethod),
        nullable=True,
        comment="Method used for conversion"
    )
    conversion_started = Column(DateTime, nullable=True, comment="When conversion started")
    conversion_completed = Column(DateTime, nullable=True, comment="When conversion completed")
    conversion_duration_ms = Column(Integer, nullable=True, comment="Processing time in milliseconds")

    # Conversion Quality
    conversion_confidence = Column(
        Float,
        nullable=True,
        comment="Overall quality score 0-1"
    )
    character_count = Column(Integer, nullable=True, comment="Characters in markdown output")
    word_count = Column(Integer, nullable=True, comment="Words in markdown output")
    page_count = Column(Integer, nullable=True, comment="Pages detected (for paginated docs)")

    # LLM Enhancement (optional)
    llm_enhanced = Column(Boolean, default=False, comment="Whether LLM was used for descriptions")
    llm_model = Column(String(100), nullable=True, comment="LLM model name if used")
    llm_tokens_used = Column(Integer, nullable=True, comment="Total tokens consumed")

    # Validation & Review
    needs_review = Column(Boolean, default=False, index=True, comment="Requires manual review")
    reviewed_by = Column(UUID(as_uuid=True), nullable=True, comment="User who reviewed")
    reviewed_date = Column(DateTime, nullable=True, comment="Review timestamp")
    review_notes = Column(Text, nullable=True, comment="Reviewer notes")

    # Error Tracking
    has_errors = Column(Boolean, default=False, index=True, comment="Whether conversion had errors")
    error_message = Column(Text, nullable=True, comment="Primary error message")
    warnings = Column(JSON, nullable=True, comment="List of warning messages")

    # Metadata & Structure
    detected_language = Column(String(10), nullable=True, comment="Primary language detected")
    detected_structure = Column(JSON, nullable=True, comment="Document structure (headings, tables, images)")
    extracted_metadata = Column(JSON, nullable=True, comment="File metadata (author, created date, etc)")

    # Search & Analysis
    tags = Column(JSON, nullable=True, comment="User-defined tags")
    categories = Column(JSON, nullable=True, comment="Auto-categorization")
    keywords = Column(JSON, nullable=True, comment="Extracted keywords")

    # Usage Tracking
    view_count = Column(Integer, default=0, comment="Number of times viewed")
    last_viewed = Column(DateTime, nullable=True, comment="Last view timestamp")
    export_count = Column(Integer, default=0, comment="Number of exports")

    # Relationships
    content = relationship(
        "MarkItDownContent",
        back_populates="document",
        uselist=False,  # One-to-one
        cascade="all, delete-orphan"
    )
    versions = relationship(
        "MarkItDownVersion",
        back_populates="document",
        cascade="all, delete-orphan"
    )


class MarkItDownContent(BaseModel):
    """
    Stores the actual markdown content from conversion

    Separated from main document table for performance
    (markdown can be large, don't load unless needed)
    """

    __tablename__ = "markitdown_content"

    # Link to document
    document_id = Column(
        UUID(as_uuid=True),
        ForeignKey('markitdown_documents.id', ondelete='CASCADE'),
        nullable=False,
        unique=True,  # One-to-one relationship
        index=True
    )

    # Content Storage
    markdown_text = Column(Text, nullable=False, comment="Full markdown output")

    # Enhanced Content (optional)
    html_preview = Column(Text, nullable=True, comment="Rendered HTML for preview")
    plain_text = Column(Text, nullable=True, comment="Plain text extraction")

    # Content Analysis
    heading_count = Column(Integer, nullable=True, comment="Number of headings")
    table_count = Column(Integer, nullable=True, comment="Number of tables")
    image_count = Column(Integer, nullable=True, comment="Number of images")
    link_count = Column(Integer, nullable=True, comment="Number of links")
    code_block_count = Column(Integer, nullable=True, comment="Number of code blocks")

    # Extracted Elements (for structured access)
    tables_data = Column(JSON, nullable=True, comment="Extracted tables as structured data")
    images_data = Column(JSON, nullable=True, comment="Image metadata and descriptions")
    links_data = Column(JSON, nullable=True, comment="Extracted links")

    # Full-text search vector (PostgreSQL specific - for future use)
    # search_vector = Column(TSVector, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    document = relationship("MarkItDownDocument", back_populates="content")


class MarkItDownVersion(BaseModel):
    """
    Version history for document conversions

    Tracks changes when documents are re-processed with:
    - Different conversion methods
    - Updated MarkItDown versions
    - Different LLM models
    """

    __tablename__ = "markitdown_versions"

    # Link to document
    document_id = Column(
        UUID(as_uuid=True),
        ForeignKey('markitdown_documents.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )

    # Version Info
    version_number = Column(Integer, nullable=False, comment="Sequential version number")
    version_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_by = Column(UUID(as_uuid=True), nullable=True, comment="User who created version")

    # Version Details
    conversion_method = Column(SQLEnum(ConversionMethod), nullable=False)
    markdown_text = Column(Text, nullable=False, comment="Markdown content snapshot")
    conversion_confidence = Column(Float, nullable=True)
    character_count = Column(Integer, nullable=True)

    # Changes from previous version
    change_summary = Column(Text, nullable=True, comment="What changed in this version")
    diff_stats = Column(JSON, nullable=True, comment="Line additions/deletions")

    # Settings used
    settings_used = Column(JSON, nullable=True, comment="Conversion settings/parameters")

    # Relationship
    document = relationship("MarkItDownDocument", back_populates="versions")


class MarkItDownBatch(BaseModel):
    """
    Batch processing records for multiple documents

    Tracks bulk conversions for folders, zip files, or batch uploads
    """

    __tablename__ = "markitdown_batches"

    # Batch Info
    batch_name = Column(String(255), nullable=False, comment="User-defined batch name")
    batch_description = Column(Text, nullable=True, comment="Batch description")

    # Status
    status = Column(
        SQLEnum(ConversionStatus),
        default=ConversionStatus.PENDING,
        nullable=False,
        index=True
    )

    # Progress Tracking
    total_documents = Column(Integer, default=0, comment="Total docs in batch")
    completed_documents = Column(Integer, default=0, comment="Successfully processed")
    failed_documents = Column(Integer, default=0, comment="Failed to process")

    # Timing
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    total_duration_ms = Column(Integer, nullable=True, comment="Total processing time")

    # Configuration
    conversion_settings = Column(JSON, nullable=True, comment="Settings for batch")
    created_by = Column(UUID(as_uuid=True), nullable=True)

    # Statistics
    total_size_kb = Column(Integer, nullable=True, comment="Total size of all files")
    total_characters = Column(Integer, nullable=True, comment="Total markdown output")

    # Relationship (if needed - many documents can belong to one batch)
    # documents = relationship("MarkItDownDocument", secondary="batch_documents")


class MarkItDownAnalytics(BaseModel):
    """
    Analytics and usage statistics for MarkItDown conversions

    Tracks conversion success rates, popular file types, performance metrics
    """

    __tablename__ = "markitdown_analytics"

    # Time period
    date = Column(DateTime, nullable=False, index=True, comment="Analytics date (daily)")

    # Conversion Statistics
    total_conversions = Column(Integer, default=0)
    successful_conversions = Column(Integer, default=0)
    failed_conversions = Column(Integer, default=0)

    # File Type Breakdown
    file_type_stats = Column(JSON, nullable=True, comment="Count by file type")

    # Performance Metrics
    avg_conversion_time_ms = Column(Integer, nullable=True)
    avg_file_size_kb = Column(Integer, nullable=True)
    avg_output_length = Column(Integer, nullable=True)

    # Quality Metrics
    avg_confidence_score = Column(Float, nullable=True)
    documents_needing_review = Column(Integer, default=0)

    # LLM Usage
    llm_enhanced_count = Column(Integer, default=0)
    total_llm_tokens = Column(Integer, default=0)

    # User Activity
    active_users = Column(Integer, default=0)
    total_uploads = Column(Integer, default=0)
