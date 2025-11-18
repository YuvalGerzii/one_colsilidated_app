"""Report models for generating professional investment reports."""

from sqlalchemy import Column, String, Integer, Float, Date, DateTime, Text, ForeignKey, Enum as SQLEnum, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import enum
from datetime import datetime
from typing import Optional

from app.models.database import BaseModel


class ReportType(str, enum.Enum):
    """Report types available for generation."""
    INVESTMENT_COMMITTEE_MEMO = "investment_committee_memo"
    QUARTERLY_PORTFOLIO = "quarterly_portfolio"
    MARKET_RESEARCH = "market_research"
    DUE_DILIGENCE_SUMMARY = "due_diligence_summary"
    DEAL_SUMMARY = "deal_summary"
    FUND_PERFORMANCE = "fund_performance"


class ReportStatus(str, enum.Enum):
    """Report generation status."""
    DRAFT = "draft"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"


class ExportFormat(str, enum.Enum):
    """Export format options."""
    PDF = "pdf"
    POWERPOINT = "pptx"
    WORD = "docx"
    EXCEL = "xlsx"


class GeneratedReport(BaseModel):
    """
    Generated Report model for tracking all report generation requests.

    Stores metadata about reports, links to source data, and export artifacts.
    """

    __tablename__ = "generated_reports"

    # Report Metadata
    report_type = Column(SQLEnum(ReportType), nullable=False, index=True, comment="Type of report")
    report_name = Column(String(255), nullable=False, comment="Custom report name")
    status = Column(SQLEnum(ReportStatus), nullable=False, default=ReportStatus.DRAFT, comment="Report generation status")

    # Multi-Tenancy
    company_id = Column(
        UUID(as_uuid=True),
        ForeignKey('companies.id', ondelete='CASCADE'),
        nullable=True,
        index=True,
        comment="Company this report belongs to (for multi-tenancy)"
    )

    # Source Data References
    deal_id = Column(UUID(as_uuid=True), ForeignKey("deals.id", ondelete="SET NULL"), nullable=True, comment="Related deal (for IC memos, DD summaries)")
    fund_id = Column(UUID(as_uuid=True), ForeignKey("funds.id", ondelete="SET NULL"), nullable=True, comment="Related fund (for portfolio reports)")

    # Report Period (for time-based reports like quarterly)
    report_period_start = Column(Date, nullable=True, comment="Report period start date")
    report_period_end = Column(Date, nullable=True, comment="Report period end date")

    # Generated Content
    report_data = Column(JSON, nullable=True, comment="Structured report data (JSON)")
    generated_html = Column(Text, nullable=True, comment="Generated HTML content")

    # Export Information
    export_formats = Column(JSON, nullable=True, comment="List of exported formats with file paths")
    file_path = Column(String(500), nullable=True, comment="Primary export file path")

    # Configuration
    template_settings = Column(JSON, nullable=True, comment="Custom template settings and parameters")
    include_charts = Column(Boolean, default=True, comment="Whether to include charts")
    include_appendix = Column(Boolean, default=True, comment="Whether to include appendix")

    # Metadata
    generated_at = Column(DateTime, nullable=True, comment="When report was generated")
    generated_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, comment="User who generated report")
    error_message = Column(Text, nullable=True, comment="Error message if generation failed")

    # Relationships
    deal = relationship("Deal", foreign_keys=[deal_id], backref="generated_reports")
    fund = relationship("Fund", foreign_keys=[fund_id], backref="generated_reports")

    def __repr__(self):
        return f"<GeneratedReport(id={self.id}, type={self.report_type}, name={self.report_name}, status={self.status})>"


class ReportTemplate(BaseModel):
    """
    Report Template model for managing custom report templates.

    Allows users to create and save custom report templates with specific formatting.
    """

    __tablename__ = "report_templates"

    # Template Metadata
    template_name = Column(String(255), nullable=False, comment="Template name")
    report_type = Column(SQLEnum(ReportType), nullable=False, index=True, comment="Type of report this template is for")
    description = Column(Text, nullable=True, comment="Template description")

    # Multi-Tenancy
    company_id = Column(
        UUID(as_uuid=True),
        ForeignKey('companies.id', ondelete='CASCADE'),
        nullable=True,
        index=True,
        comment="Company this template belongs to (for multi-tenancy)"
    )

    # Template Content
    html_template = Column(Text, nullable=True, comment="Custom HTML template (Jinja2)")
    css_styles = Column(Text, nullable=True, comment="Custom CSS styles")

    # Template Configuration
    sections = Column(JSON, nullable=True, comment="Report sections configuration")
    default_settings = Column(JSON, nullable=True, comment="Default template settings")

    # Access Control
    is_default = Column(Boolean, default=False, comment="Whether this is a default template")
    is_public = Column(Boolean, default=False, comment="Whether template is shared across company")
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, comment="Template creator")

    def __repr__(self):
        return f"<ReportTemplate(id={self.id}, name={self.template_name}, type={self.report_type})>"
