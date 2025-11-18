"""
Legal Services Database Models

Handles legal documents, compliance tracking, and legal calendar items.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text, Date, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.core.database import Base


class ComplianceStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"
    OVERDUE = "overdue"


class CompliancePriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class DocumentCategory(str, enum.Enum):
    ACQUISITION = "acquisition"
    LEASING = "leasing"
    TRANSFER = "transfer"
    GENERAL = "general"
    PARTNERSHIP = "partnership"
    DEVELOPMENT = "development"
    MANAGEMENT = "management"
    RIGHTS = "rights"


class RiskLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class LegalDocument(Base):
    """Legal documents and templates"""
    __tablename__ = "legal_documents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    category = Column(Enum(DocumentCategory), nullable=False)
    description = Column(Text)
    file_path = Column(String(500))
    version = Column(String(50), default="1.0")
    template_url = Column(String(500))
    is_template = Column(Boolean, default=True)
    created_by = Column(String(255))
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    company = relationship("Company", back_populates="legal_documents")


class ComplianceItem(Base):
    """Legal compliance checklist items"""
    __tablename__ = "compliance_items"

    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(Enum(ComplianceStatus), default=ComplianceStatus.PENDING)
    priority = Column(Enum(CompliancePriority), default=CompliancePriority.MEDIUM)
    due_date = Column(Date)
    completed_date = Column(Date, nullable=True)
    property_address = Column(String(500), nullable=True)
    assigned_to = Column(String(255), nullable=True)
    notes = Column(Text)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    company = relationship("Company", back_populates="compliance_items")


class LegalDeadline(Base):
    """Legal calendar and deadline tracking"""
    __tablename__ = "legal_deadlines"

    id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String(255), nullable=False)
    description = Column(Text)
    deadline_date = Column(Date, nullable=False)
    priority = Column(Enum(CompliancePriority), default=CompliancePriority.MEDIUM)
    category = Column(String(100))
    property_address = Column(String(500), nullable=True)
    reminder_sent = Column(Boolean, default=False)
    completed = Column(Boolean, default=False)
    notes = Column(Text)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    company = relationship("Company", back_populates="legal_deadlines")


class RiskAssessment(Base):
    """Property legal risk assessments"""
    __tablename__ = "risk_assessments"

    id = Column(Integer, primary_key=True, index=True)
    property_name = Column(String(255), nullable=False)
    property_address = Column(String(500))
    risk_level = Column(Enum(RiskLevel), default=RiskLevel.MEDIUM)
    risk_score = Column(Integer, default=50)  # 0-100
    assessment_date = Column(Date, nullable=False)
    legal_issues = Column(Text)  # JSON array of issues
    recommendations = Column(Text)
    assessed_by = Column(String(255))
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    company = relationship("Company", back_populates="risk_assessments")


class ContractReview(Base):
    """Contract review tracking and AI analysis results"""
    __tablename__ = "contract_reviews"

    id = Column(Integer, primary_key=True, index=True)
    contract_name = Column(String(255), nullable=False)
    contract_type = Column(String(100))
    file_path = Column(String(500))
    status = Column(String(50), default="under_review")  # under_review, approved, needs_revision
    review_date = Column(Date)
    reviewer = Column(String(255))
    high_risk_clauses = Column(Integer, default=0)
    ai_analysis = Column(Text)  # JSON with AI findings
    notes = Column(Text)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    company = relationship("Company", back_populates="contract_reviews")
