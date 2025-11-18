"""
Company Model

This module contains the Company model for multi-tenant property management.
Each company represents an isolated workspace with its own properties and data.
"""

from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from app.models.database import Base, UUIDMixin, TimestampMixin, SoftDeleteMixin


class Company(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    Company table - Represents a company/organization workspace.

    Each company has its own isolated property management space with
    separate properties, units, leases, and financial data.
    """

    __tablename__ = "companies"

    # Basic Information
    name = Column(
        String(200),
        nullable=False,
        unique=True,
        index=True,
        comment="Company name (must be unique)"
    )

    details = Column(
        Text,
        nullable=True,
        comment="Company description and additional details"
    )

    region = Column(
        String(100),
        nullable=True,
        index=True,
        comment="Primary region/location of operations"
    )

    contact_info = Column(
        Text,
        nullable=True,
        comment="Contact information (email, phone, address)"
    )

    logo_url = Column(
        String(500),
        nullable=True,
        comment="URL to company logo image"
    )

    # Relationships
    properties = relationship(
        "Property",
        back_populates="company",
        cascade="all, delete-orphan",
        lazy="dynamic",
        doc="All properties owned by this company"
    )

    accounting_profile = relationship(
        "AccountingProfile",
        back_populates="company",
        uselist=False,
        cascade="all, delete-orphan",
        doc="Accounting profile for this company"
    )

    legal_documents = relationship(
        "LegalDocument",
        back_populates="company",
        cascade="all, delete-orphan",
        lazy="dynamic",
        doc="Legal documents and templates for this company"
    )

    compliance_items = relationship(
        "ComplianceItem",
        back_populates="company",
        cascade="all, delete-orphan",
        lazy="dynamic",
        doc="Compliance tracking items for this company"
    )

    legal_deadlines = relationship(
        "LegalDeadline",
        back_populates="company",
        cascade="all, delete-orphan",
        lazy="dynamic",
        doc="Legal calendar and deadlines for this company"
    )

    risk_assessments = relationship(
        "RiskAssessment",
        back_populates="company",
        cascade="all, delete-orphan",
        lazy="dynamic",
        doc="Property risk assessments for this company"
    )

    contract_reviews = relationship(
        "ContractReview",
        back_populates="company",
        cascade="all, delete-orphan",
        lazy="dynamic",
        doc="Contract reviews for this company"
    )

    # Enhanced Legal Services relationships
    clause_library = relationship(
        "ClauseLibrary",
        back_populates="company",
        cascade="all, delete-orphan",
        lazy="dynamic",
        doc="Clause library for this company"
    )

    document_templates = relationship(
        "DocumentTemplate",
        back_populates="company",
        cascade="all, delete-orphan",
        lazy="dynamic",
        doc="Document templates for this company"
    )

    automation_workflows = relationship(
        "AutomationWorkflow",
        back_populates="company",
        cascade="all, delete-orphan",
        lazy="dynamic",
        doc="Automation workflows for this company"
    )

    esignature_requests = relationship(
        "ESignatureRequest",
        back_populates="company",
        cascade="all, delete-orphan",
        lazy="dynamic",
        doc="E-signature requests for this company"
    )

    ai_contract_analyses = relationship(
        "AIContractAnalysis",
        back_populates="company",
        cascade="all, delete-orphan",
        lazy="dynamic",
        doc="AI contract analyses for this company"
    )

    # Compliance and Audit relationships
    exchange_1031_tracking = relationship(
        "Exchange1031Tracking",
        back_populates="company",
        cascade="all, delete-orphan",
        lazy="dynamic",
        doc="1031 exchange tracking for this company"
    )

    opportunity_zone_investments = relationship(
        "OpportunityZoneInvestment",
        back_populates="company",
        cascade="all, delete-orphan",
        lazy="dynamic",
        doc="Opportunity Zone investments for this company"
    )

    firpta_compliance = relationship(
        "FIRPTACompliance",
        back_populates="company",
        cascade="all, delete-orphan",
        lazy="dynamic",
        doc="FIRPTA compliance tracking for this company"
    )

    fair_housing_compliance = relationship(
        "FairHousingCompliance",
        back_populates="company",
        cascade="all, delete-orphan",
        lazy="dynamic",
        doc="Fair Housing compliance for this company"
    )

    investor_kyc_aml = relationship(
        "InvestorKYCAML",
        back_populates="company",
        cascade="all, delete-orphan",
        lazy="dynamic",
        doc="Investor KYC/AML records for this company"
    )

    legal_holds = relationship(
        "LegalHold",
        back_populates="company",
        cascade="all, delete-orphan",
        lazy="dynamic",
        doc="Legal holds for this company"
    )

    statute_limitations_tracker = relationship(
        "StatuteOfLimitationsTracker",
        back_populates="company",
        cascade="all, delete-orphan",
        lazy="dynamic",
        doc="Statute of limitations tracking for this company"
    )

    audit_preparations = relationship(
        "AuditPreparation",
        back_populates="company",
        cascade="all, delete-orphan",
        lazy="dynamic",
        doc="Audit preparations for this company"
    )

    soc2_compliance = relationship(
        "SOC2Compliance",
        back_populates="company",
        cascade="all, delete-orphan",
        lazy="dynamic",
        doc="SOC 2 compliance tracking for this company"
    )

    clause_comparisons = relationship(
        "ClauseComparison",
        back_populates="company",
        cascade="all, delete-orphan",
        lazy="dynamic",
        doc="Clause comparisons for this company"
    )

    def __repr__(self) -> str:
        """String representation of Company instance."""
        return f"<Company(id={self.id}, name={self.name})>"

    @property
    def property_count(self) -> int:
        """Get the count of active properties for this company."""
        try:
            return self.properties.filter_by(deleted_at=None).count()
        except Exception:
            # Return 0 if the properties table doesn't have company_id column yet
            # This can happen before migrations are run
            return 0
