"""
Model Templates & Presets System

Provides reusable templates for all financial models:
- Industry-standard assumption sets
- Property type-specific defaults
- Market-based presets
- Company templates by sector
- Model duplication and comparison
"""

from datetime import datetime
from typing import Optional
from decimal import Decimal

from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Date, Text,
    Boolean, JSON, Numeric, ForeignKey, Index, Enum as SQLEnum
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base
from app.models.database import UUIDMixin, TimestampMixin, SoftDeleteMixin


class TemplateCategory(str, enum.Enum):
    """Categories for model templates"""
    REAL_ESTATE = "real_estate"
    FINANCIAL_MODEL = "financial_model"
    FUND_MANAGEMENT = "fund_management"
    DEBT_MANAGEMENT = "debt_management"
    PROPERTY_MANAGEMENT = "property_management"
    ACCOUNTING = "accounting"
    CUSTOM = "custom"


class TemplateType(str, enum.Enum):
    """Specific template types"""
    # Real Estate
    HOTEL = "hotel"
    SINGLE_FAMILY_RENTAL = "single_family_rental"
    FIX_AND_FLIP = "fix_and_flip"
    SMALL_MULTIFAMILY = "small_multifamily"
    HIGH_RISE_MULTIFAMILY = "high_rise_multifamily"
    MIXED_USE = "mixed_use"
    LEASE_ANALYZER = "lease_analyzer"
    RENOVATION_BUDGET = "renovation_budget"

    # Financial Models
    DCF_MODEL = "dcf_model"
    LBO_MODEL = "lbo_model"

    # Fund Management
    PE_FUND = "pe_fund"
    VC_FUND = "vc_fund"
    RE_FUND = "re_fund"

    # Debt Management
    LOAN_ANALYSIS = "loan_analysis"
    REFINANCING = "refinancing"

    # Property Management
    PROPERTY_PORTFOLIO = "property_portfolio"

    # Custom
    CUSTOM = "custom"


class TemplateScope(str, enum.Enum):
    """Visibility and access scope for templates"""
    SYSTEM = "system"  # Built-in, read-only templates
    COMPANY = "company"  # Company-wide templates
    USER = "user"  # User-specific templates
    PUBLIC = "public"  # Publicly shared templates


class ModelTemplate(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    Reusable model templates with preset assumptions and configurations.

    Templates can be:
    - Industry-standard presets
    - Property type-specific defaults
    - Market-based configurations
    - Company sector templates
    """
    __tablename__ = "model_templates"

    # Basic Information
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    category = Column(SQLEnum(TemplateCategory), nullable=False, index=True)
    template_type = Column(SQLEnum(TemplateType), nullable=False, index=True)
    scope = Column(SQLEnum(TemplateScope), nullable=False, default=TemplateScope.USER, index=True)

    # Ownership & Access
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)
    is_default = Column(Boolean, default=False, comment="Default template for this type")

    # Template Data (JSON storage for flexibility)
    assumptions = Column(JSON, nullable=False, comment="Model assumptions and defaults")
    configuration = Column(JSON, nullable=True, comment="Additional configuration settings")

    # Classification & Tags
    property_type = Column(String(100), nullable=True, index=True, comment="Property type (if applicable)")
    market = Column(String(100), nullable=True, index=True, comment="Geographic market")
    industry_sector = Column(String(100), nullable=True, index=True, comment="Industry/sector")
    tags = Column(JSON, nullable=True, comment="Searchable tags")

    # Usage Statistics
    usage_count = Column(Integer, default=0, comment="Times this template has been used")
    last_used_at = Column(DateTime, nullable=True)

    # Metadata
    version = Column(String(20), nullable=True, comment="Template version")
    is_published = Column(Boolean, default=False, comment="Published for others to use")

    # Relationships
    company = relationship("Company", foreign_keys=[company_id])
    user = relationship("User", foreign_keys=[user_id])
    usage_logs = relationship("TemplateUsageLog", back_populates="template", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index("idx_template_category_type", "category", "template_type"),
        Index("idx_template_scope_company", "scope", "company_id"),
        Index("idx_template_property_market", "property_type", "market"),
    )


class TemplateUsageLog(Base, UUIDMixin, TimestampMixin):
    """
    Track template usage for analytics and recommendations.
    """
    __tablename__ = "template_usage_logs"

    template_id = Column(UUID(as_uuid=True), ForeignKey("model_templates.id"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=True, index=True)

    # What was created from this template
    model_type = Column(String(100), nullable=False, comment="Type of model created")
    model_id = Column(String(100), nullable=True, comment="ID of created model")

    # Context
    action = Column(String(50), nullable=False, comment="applied, cloned, compared")
    success = Column(Boolean, default=True)
    error_message = Column(Text, nullable=True)

    # Relationships
    template = relationship("ModelTemplate", back_populates="usage_logs")
    user = relationship("User")
    company = relationship("Company")


class ModelComparison(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    Store model comparison configurations for side-by-side analysis.
    """
    __tablename__ = "model_comparisons"

    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)

    # Ownership
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=True, index=True)

    # Models being compared
    model_type = Column(String(100), nullable=False, comment="Type of models being compared")
    model_ids = Column(JSON, nullable=False, comment="List of model IDs to compare")

    # Comparison Configuration
    comparison_metrics = Column(JSON, nullable=True, comment="Which metrics to compare")
    display_settings = Column(JSON, nullable=True, comment="UI display preferences")

    # Sharing
    is_shared = Column(Boolean, default=False)
    shared_with_users = Column(JSON, nullable=True, comment="List of user IDs with access")

    # Relationships
    user = relationship("User")
    company = relationship("Company")

    # Indexes
    __table_args__ = (
        Index("idx_comparison_user_type", "user_id", "model_type"),
    )


class PresetAssumptionSet(Base, UUIDMixin, TimestampMixin):
    """
    Industry-standard assumption sets that can be applied to models.

    Examples:
    - Cap rates by property type
    - Rent growth assumptions by market
    - Operating expense ratios
    - Financing terms by market conditions
    """
    __tablename__ = "preset_assumption_sets"

    # Basic Information
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    category = Column(SQLEnum(TemplateCategory), nullable=False, index=True)

    # Classification
    property_type = Column(String(100), nullable=True, index=True)
    market = Column(String(100), nullable=True, index=True)
    industry = Column(String(100), nullable=True, index=True)

    # Assumption Data
    assumptions = Column(JSON, nullable=False, comment="Structured assumption data")

    # Source & Credibility
    source = Column(String(200), nullable=True, comment="Data source (e.g., NCREIF, industry report)")
    source_date = Column(Date, nullable=True, comment="When this data was published")
    confidence_level = Column(String(50), nullable=True, comment="high, medium, low")

    # Metadata
    is_active = Column(Boolean, default=True)
    version = Column(String(20), nullable=True)

    # Indexes
    __table_args__ = (
        Index("idx_assumption_category_property", "category", "property_type"),
        Index("idx_assumption_market_industry", "market", "industry"),
    )


class ModelClone(Base, UUIDMixin, TimestampMixin):
    """
    Track model cloning/duplication for audit and lineage.
    """
    __tablename__ = "model_clones"

    # Original Model
    source_model_type = Column(String(100), nullable=False, index=True)
    source_model_id = Column(String(100), nullable=False, index=True)

    # Cloned Model
    cloned_model_type = Column(String(100), nullable=False)
    cloned_model_id = Column(String(100), nullable=False, index=True)

    # Context
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=True, index=True)

    # Cloning Details
    clone_type = Column(String(50), nullable=False, comment="full_copy, template_based, partial")
    modifications = Column(JSON, nullable=True, comment="Changes made during cloning")

    # Relationships
    user = relationship("User")
    company = relationship("Company")

    # Indexes
    __table_args__ = (
        Index("idx_clone_source", "source_model_type", "source_model_id"),
        Index("idx_clone_target", "cloned_model_type", "cloned_model_id"),
    )


# Export all models
__all__ = [
    "TemplateCategory",
    "TemplateType",
    "TemplateScope",
    "ModelTemplate",
    "TemplateUsageLog",
    "ModelComparison",
    "PresetAssumptionSet",
    "ModelClone",
]
