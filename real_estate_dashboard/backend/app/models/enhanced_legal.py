"""
Enhanced Legal Services Database Models

Advanced features for legal automation, clause library, zoning data, and AI analysis.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text, Date, Boolean, Float, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.core.database import Base


class ClauseCategory(str, enum.Enum):
    PURCHASE_SALE = "purchase_sale"
    LEASING = "leasing"
    RISK_MITIGATION = "risk_mitigation"
    FINANCING = "financing"
    DISCLOSURE = "disclosure"
    TERMINATION = "termination"
    GENERAL = "general"


class ClauseRiskLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AutomationStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PAUSED = "paused"
    ERROR = "error"


class SignatureStatus(str, enum.Enum):
    PENDING = "pending"
    SENT = "sent"
    SIGNED = "signed"
    DECLINED = "declined"
    EXPIRED = "expired"


class ClauseLibrary(Base):
    """Pre-approved legal clauses with AI scoring"""
    __tablename__ = "clause_library"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    category = Column(Enum(ClauseCategory), nullable=False)
    clause_text = Column(Text, nullable=False)
    description = Column(Text)
    usage_recommendation = Column(String(100))  # Standard, Essential, Negotiable, etc.
    ai_safety_score = Column(Integer, default=50)  # 0-100
    risk_level = Column(Enum(ClauseRiskLevel), default=ClauseRiskLevel.LOW)
    state_specific = Column(Boolean, default=False)
    applicable_states = Column(JSON)  # Array of state codes
    jurisdiction_notes = Column(Text)
    version = Column(String(50), default="1.0")
    is_approved = Column(Boolean, default=True)
    created_by = Column(String(255))
    approved_by = Column(String(255))
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    company = relationship("Company", back_populates="clause_library")


class DocumentTemplate(Base):
    """AI-powered document templates"""
    __tablename__ = "document_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    document_type = Column(String(100), nullable=False)
    complexity = Column(String(50))  # Low, Medium, High
    estimated_time = Column(String(50))  # e.g., "5 min"
    ai_powered = Column(Boolean, default=True)
    state_specific = Column(Boolean, default=False)
    template_content = Column(Text)
    template_url = Column(String(500))
    required_fields = Column(JSON)  # Array of required field definitions
    optional_fields = Column(JSON)
    suggested_clauses = Column(JSON)  # Array of clause IDs to suggest
    compliance_requirements = Column(JSON)
    category = Column(String(100))
    is_active = Column(Boolean, default=True)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    company = relationship("Company", back_populates="document_templates")


class ZoningData(Base):
    """Zoning and land use regulations database"""
    __tablename__ = "zoning_data"

    id = Column(Integer, primary_key=True, index=True)
    jurisdiction = Column(String(255), nullable=False, index=True)  # City/County name
    state = Column(String(2), nullable=False, index=True)
    zoning_code = Column(String(50), nullable=False)
    zoning_name = Column(String(255), nullable=False)
    category = Column(String(100))  # Residential, Commercial, Industrial, etc.
    description = Column(Text)
    permitted_uses = Column(JSON)  # Array of permitted uses
    conditional_uses = Column(JSON)
    prohibited_uses = Column(JSON)
    density_requirements = Column(Text)
    height_restrictions = Column(String(255))
    parking_requirements = Column(Text)
    setback_requirements = Column(Text)
    special_conditions = Column(Text)
    ordinance_reference = Column(String(255))
    last_updated = Column(Date)
    data_source = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AutomationWorkflow(Base):
    """Legal automation workflows"""
    __tablename__ = "automation_workflows"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    workflow_type = Column(String(100))  # lease_renewal, compliance, document_expiration, etc.
    status = Column(Enum(AutomationStatus), default=AutomationStatus.ACTIVE)
    trigger_conditions = Column(JSON)  # Conditions that activate the workflow
    actions = Column(JSON)  # Actions to perform
    schedule = Column(String(255))  # Cron expression or schedule
    last_run = Column(DateTime)
    next_run = Column(DateTime)
    trigger_count = Column(Integer, default=0)
    success_count = Column(Integer, default=0)
    error_count = Column(Integer, default=0)
    notification_settings = Column(JSON)
    is_enabled = Column(Boolean, default=True)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    company = relationship("Company", back_populates="automation_workflows")


class LegalKnowledgeBase(Base):
    """Legal knowledge articles and resources"""
    __tablename__ = "legal_knowledge_base"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    topic = Column(String(255), nullable=False, index=True)
    category = Column(String(100), nullable=False)  # Federal Law, State Law, Tax Law, etc.
    content = Column(Text, nullable=False)
    summary = Column(Text)
    tags = Column(JSON)  # Array of tags
    jurisdiction = Column(String(100))  # US, State-specific, etc.
    applicable_states = Column(JSON)
    last_reviewed = Column(Date)
    author = Column(String(255))
    references = Column(JSON)  # Links to external resources
    is_published = Column(Boolean, default=True)
    view_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ESignatureRequest(Base):
    """Electronic signature tracking"""
    __tablename__ = "esignature_requests"

    id = Column(Integer, primary_key=True, index=True)
    document_name = Column(String(255), nullable=False)
    document_path = Column(String(500))
    status = Column(Enum(SignatureStatus), default=SignatureStatus.PENDING)
    sender_email = Column(String(255), nullable=False)
    signers = Column(JSON, nullable=False)  # Array of signer info
    current_signer_index = Column(Integer, default=0)
    expiration_date = Column(Date)
    reminder_sent = Column(Boolean, default=False)
    completed_at = Column(DateTime)
    audit_trail = Column(JSON)  # Complete history of signature events
    ip_addresses = Column(JSON)  # IP addresses of signers
    esign_provider = Column(String(100))  # DocuSign, Adobe Sign, etc.
    provider_reference = Column(String(255))
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    company = relationship("Company", back_populates="esignature_requests")


class AIContractAnalysis(Base):
    """AI contract analysis results"""
    __tablename__ = "ai_contract_analysis"

    id = Column(Integer, primary_key=True, index=True)
    contract_name = Column(String(255), nullable=False)
    file_path = Column(String(500))
    analysis_date = Column(DateTime, default=datetime.utcnow)
    risk_score = Column(Integer)  # 0-100
    risk_level = Column(String(50))  # Low, Medium, High, Critical
    high_risk_clauses = Column(JSON)  # Array of identified risk clauses
    missing_provisions = Column(JSON)  # Array of missing standard provisions
    compliance_issues = Column(JSON)  # Array of compliance problems
    recommendations = Column(JSON)  # Array of AI recommendations
    clause_analysis = Column(JSON)  # Detailed clause-by-clause analysis
    financial_terms = Column(JSON)  # Extracted financial terms
    key_dates = Column(JSON)  # Extracted important dates
    parties_involved = Column(JSON)  # Identified parties
    jurisdiction = Column(String(255))
    ai_model_version = Column(String(50))
    confidence_score = Column(Float)
    processing_time = Column(Integer)  # milliseconds
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    company = relationship("Company", back_populates="ai_contract_analyses")


class StateLegalForm(Base):
    """State-specific legal forms library"""
    __tablename__ = "state_legal_forms"

    id = Column(Integer, primary_key=True, index=True)
    form_name = Column(String(255), nullable=False)
    state = Column(String(2), nullable=False, index=True)
    form_number = Column(String(100))
    category = Column(String(100), nullable=False)  # Residential, Commercial, Disclosure, etc.
    description = Column(Text)
    form_content = Column(Text)
    form_url = Column(String(500))
    is_required = Column(Boolean, default=False)  # Required by state law
    applicable_transactions = Column(JSON)  # Purchase, Lease, etc.
    effective_date = Column(Date)
    expiration_date = Column(Date)
    last_updated = Column(Date)
    source_authority = Column(String(255))  # State bar, realtor association, etc.
    compliance_notes = Column(Text)
    is_fillable = Column(Boolean, default=True)
    required_fields = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class RegulatoryChange(Base):
    """Track regulatory and legal changes"""
    __tablename__ = "regulatory_changes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    change_type = Column(String(100))  # Law, Regulation, Ordinance, Code Update
    jurisdiction = Column(String(255), nullable=False)
    state = Column(String(2))
    effective_date = Column(Date, nullable=False)
    description = Column(Text, nullable=False)
    affected_areas = Column(JSON)  # Areas affected: zoning, fair housing, etc.
    impact_level = Column(String(50))  # Low, Medium, High, Critical
    action_required = Column(Boolean, default=False)
    action_deadline = Column(Date)
    reference_url = Column(String(500))
    notification_sent = Column(Boolean, default=False)
    acknowledged_by = Column(JSON)  # Users who acknowledged the change
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
