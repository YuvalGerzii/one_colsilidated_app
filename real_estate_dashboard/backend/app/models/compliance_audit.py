"""
Compliance and Audit Database Models

Advanced compliance tracking, regulatory requirements, and audit preparation.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text, Date, Boolean, Float, JSON, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from decimal import Decimal

from app.core.database import Base


class Exchange1031Status(str, enum.Enum):
    PLANNING = "planning"
    PROPERTY_SOLD = "property_sold"
    IDENTIFICATION_PERIOD = "identification_period"
    EXCHANGE_PERIOD = "exchange_period"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class OpportunityZoneStatus(str, enum.Enum):
    ELIGIBLE = "eligible"
    INVESTED = "invested"
    HOLDING = "holding"
    EXITED = "exited"


class ComplianceStatus(str, enum.Enum):
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    UNDER_REVIEW = "under_review"
    REMEDIATION = "remediation"


class AuditStatus(str, enum.Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class Exchange1031Tracking(Base):
    """Track 1031 like-kind exchanges"""
    __tablename__ = "exchange_1031_tracking"

    id = Column(Integer, primary_key=True, index=True)
    exchange_name = Column(String(255), nullable=False)
    status = Column(Enum(Exchange1031Status), default=Exchange1031Status.PLANNING)

    # Relinquished Property
    relinquished_property_address = Column(String(500))
    relinquished_property_value = Column(Numeric(15, 2))
    sale_date = Column(Date)
    sale_proceeds = Column(Numeric(15, 2))
    debt_retired = Column(Numeric(15, 2))

    # Timeline Tracking
    identification_deadline = Column(Date)  # 45 days from sale
    exchange_deadline = Column(Date)  # 180 days from sale

    # Replacement Properties
    identified_properties = Column(JSON)  # Array of identified properties
    replacement_property_address = Column(String(500))
    replacement_property_value = Column(Numeric(15, 2))
    replacement_purchase_date = Column(Date)

    # Financial Details
    boot_received = Column(Numeric(15, 2), default=0)  # Taxable portion
    new_loan_amount = Column(Numeric(15, 2))
    qualified_intermediary = Column(String(255))
    qi_contact_info = Column(Text)

    # Tax Calculations
    deferred_gain = Column(Numeric(15, 2))
    basis_in_new_property = Column(Numeric(15, 2))
    estimated_tax_savings = Column(Numeric(15, 2))

    # Compliance
    exchange_agreement_date = Column(Date)
    exchange_agreement_file = Column(String(500))
    compliance_notes = Column(Text)
    cpa_advisor = Column(String(255))

    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    company = relationship("Company", back_populates="exchange_1031_tracking")


class OpportunityZoneInvestment(Base):
    """Track Qualified Opportunity Zone investments"""
    __tablename__ = "opportunity_zone_investments"

    id = Column(Integer, primary_key=True, index=True)
    investment_name = Column(String(255), nullable=False)
    status = Column(Enum(OpportunityZoneStatus), default=OpportunityZoneStatus.ELIGIBLE)

    # Property Details
    property_address = Column(String(500), nullable=False)
    census_tract = Column(String(50))
    opportunity_zone_designation_date = Column(Date)

    # Investment Details
    investment_date = Column(Date, nullable=False)
    investment_amount = Column(Numeric(15, 2), nullable=False)
    capital_gain_invested = Column(Numeric(15, 2))
    capital_gain_date = Column(Date)  # Date of original gain

    # Holding Period Tracking
    required_hold_date = Column(Date)  # 10 years from investment
    five_year_milestone = Column(Date)  # 10% basis step-up
    seven_year_milestone = Column(Date)  # 15% basis step-up

    # Tax Benefits
    deferral_amount = Column(Numeric(15, 2))
    deferral_expiration_date = Column(Date)  # Dec 31, 2026 or sale date
    basis_step_up_5yr = Column(Numeric(15, 2))
    basis_step_up_7yr = Column(Numeric(15, 2))
    estimated_tax_free_gain = Column(Numeric(15, 2))

    # Fund Information
    qozb_fund_name = Column(String(255))  # Qualified Opportunity Zone Business
    qozb_ein = Column(String(20))
    investment_vehicle = Column(String(100))  # Direct, Fund, Partnership

    # Compliance
    form_8949_filed = Column(Boolean, default=False)
    form_8997_filed = Column(Boolean, default=False)
    annual_certification_date = Column(Date)
    compliance_notes = Column(Text)

    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    company = relationship("Company", back_populates="opportunity_zone_investments")


class FIRPTACompliance(Base):
    """Track FIRPTA (Foreign Investment in Real Property Tax Act) compliance"""
    __tablename__ = "firpta_compliance"

    id = Column(Integer, primary_key=True, index=True)
    transaction_name = Column(String(255), nullable=False)
    property_address = Column(String(500), nullable=False)

    # Seller Information
    seller_name = Column(String(255), nullable=False)
    is_foreign_person = Column(Boolean, nullable=False)
    seller_tin = Column(String(50))
    seller_country = Column(String(100))

    # Transaction Details
    sale_price = Column(Numeric(15, 2), nullable=False)
    sale_date = Column(Date)
    property_type = Column(String(100))  # Residential, Commercial, Land

    # FIRPTA Calculations
    withholding_rate = Column(Float, default=15.0)  # 15% standard, 10% if < $1M residential
    withholding_amount = Column(Numeric(15, 2))
    reduced_withholding_approved = Column(Boolean, default=False)
    reduced_withholding_amount = Column(Numeric(15, 2))

    # Exemptions
    exemption_claimed = Column(Boolean, default=False)
    exemption_type = Column(String(100))  # Under $300k personal residence, etc.
    exemption_documentation = Column(String(500))

    # Forms and Filing
    form_8288_filed = Column(Boolean, default=False)
    form_8288_filing_date = Column(Date)
    form_8288a_issued = Column(Boolean, default=False)
    form_8288b_filed = Column(Boolean, default=False)  # Seller's application for withholding certificate

    # Payment
    withholding_payment_date = Column(Date)
    withholding_payment_reference = Column(String(255))
    irs_confirmation_number = Column(String(100))

    # Compliance
    compliance_status = Column(Enum(ComplianceStatus), default=ComplianceStatus.UNDER_REVIEW)
    closing_attorney = Column(String(255))
    notes = Column(Text)

    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    company = relationship("Company", back_populates="firpta_compliance")


class FairHousingCompliance(Base):
    """Track Fair Housing Act compliance"""
    __tablename__ = "fair_housing_compliance"

    id = Column(Integer, primary_key=True, index=True)
    property_address = Column(String(500), nullable=False)
    compliance_check_date = Column(Date, nullable=False)

    # Compliance Areas
    advertising_compliant = Column(Boolean, default=True)
    advertising_notes = Column(Text)

    application_process_compliant = Column(Boolean, default=True)
    application_notes = Column(Text)

    screening_criteria_compliant = Column(Boolean, default=True)
    screening_notes = Column(Text)

    reasonable_accommodation_policy = Column(Boolean, default=True)
    accommodation_notes = Column(Text)

    equal_opportunity_posting = Column(Boolean, default=True)
    posting_location = Column(String(255))

    # Protected Classes Training
    staff_training_completed = Column(Boolean, default=False)
    training_date = Column(Date)
    training_provider = Column(String(255))
    next_training_date = Column(Date)

    # Documentation
    policy_manual_updated = Column(Boolean, default=False)
    policy_manual_version = Column(String(50))
    policy_manual_url = Column(String(500))

    # Violations/Issues
    violations_reported = Column(Boolean, default=False)
    violation_details = Column(JSON)  # Array of violation records
    remediation_plan = Column(Text)
    remediation_completed = Column(Boolean, default=False)

    # Overall Status
    compliance_status = Column(Enum(ComplianceStatus), default=ComplianceStatus.COMPLIANT)
    compliance_score = Column(Integer)  # 0-100
    next_review_date = Column(Date)
    reviewer_name = Column(String(255))

    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    company = relationship("Company", back_populates="fair_housing_compliance")


class InvestorKYCAML(Base):
    """Investor KYC (Know Your Customer) and AML (Anti-Money Laundering) compliance"""
    __tablename__ = "investor_kyc_aml"

    id = Column(Integer, primary_key=True, index=True)
    investor_name = Column(String(255), nullable=False)
    investor_type = Column(String(100))  # Individual, Entity, Trust, Foreign
    investor_country = Column(String(100))

    # Identity Verification
    identity_verified = Column(Boolean, default=False)
    verification_method = Column(String(100))  # Document, Biometric, Third-party
    verification_date = Column(Date)
    verification_provider = Column(String(255))

    # Document Collection
    government_id_collected = Column(Boolean, default=False)
    proof_of_address_collected = Column(Boolean, default=False)
    tax_id_collected = Column(Boolean, default=False)
    entity_documents_collected = Column(Boolean, default=False)  # Articles, bylaws, etc.

    # Accredited Investor Verification
    accredited_investor = Column(Boolean)
    accreditation_method = Column(String(100))  # Income, Net Worth, Professional
    accreditation_date = Column(Date)
    accreditation_expiration = Column(Date)

    # Source of Funds
    source_of_funds_declared = Column(Boolean, default=False)
    source_of_funds = Column(Text)
    high_risk_jurisdiction = Column(Boolean, default=False)

    # PEP Screening (Politically Exposed Person)
    pep_screening_completed = Column(Boolean, default=False)
    pep_screening_date = Column(Date)
    is_pep = Column(Boolean, default=False)
    pep_details = Column(Text)

    # Sanctions Screening
    sanctions_screening_completed = Column(Boolean, default=False)
    sanctions_screening_date = Column(Date)
    sanctions_match_found = Column(Boolean, default=False)
    sanctions_details = Column(Text)

    # Risk Assessment
    risk_rating = Column(String(50))  # Low, Medium, High
    risk_factors = Column(JSON)
    enhanced_due_diligence_required = Column(Boolean, default=False)
    edd_completed = Column(Boolean, default=False)

    # Ongoing Monitoring
    last_review_date = Column(Date)
    next_review_date = Column(Date)
    monitoring_frequency = Column(String(50))  # Annual, Bi-annual, Quarterly

    # Compliance Status
    kyc_status = Column(Enum(ComplianceStatus), default=ComplianceStatus.UNDER_REVIEW)
    aml_status = Column(Enum(ComplianceStatus), default=ComplianceStatus.UNDER_REVIEW)
    approved_for_investment = Column(Boolean, default=False)
    approval_date = Column(Date)
    approved_by = Column(String(255))

    # SAR/CTR
    suspicious_activity_reported = Column(Boolean, default=False)
    sar_filing_date = Column(Date)
    sar_reference_number = Column(String(100))

    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    company = relationship("Company", back_populates="investor_kyc_aml")


class LegalHold(Base):
    """Legal hold management for litigation and investigations"""
    __tablename__ = "legal_holds"

    id = Column(Integer, primary_key=True, index=True)
    hold_name = Column(String(255), nullable=False)
    matter_name = Column(String(255))
    case_number = Column(String(100))

    # Hold Details
    hold_issued_date = Column(Date, nullable=False)
    hold_issued_by = Column(String(255))
    hold_reason = Column(Text, nullable=False)

    # Scope
    custodians = Column(JSON)  # Array of people subject to hold
    properties_affected = Column(JSON)  # Array of property addresses
    document_types = Column(JSON)  # Types of documents to preserve
    date_range_start = Column(Date)
    date_range_end = Column(Date)

    # Status
    is_active = Column(Boolean, default=True)
    release_date = Column(Date)
    release_authorized_by = Column(String(255))

    # Notifications
    notification_sent = Column(Boolean, default=False)
    notification_date = Column(DateTime)
    acknowledgments_required = Column(Boolean, default=True)
    acknowledgments_received = Column(JSON)  # Array of custodian acknowledgments

    # Compliance
    documents_preserved = Column(Integer, default=0)
    last_compliance_check = Column(Date)
    compliance_notes = Column(Text)

    # Legal Counsel
    law_firm = Column(String(255))
    attorney_name = Column(String(255))
    attorney_contact = Column(String(255))

    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    company = relationship("Company", back_populates="legal_holds")


class StatuteOfLimitationsTracker(Base):
    """Track statute of limitations deadlines"""
    __tablename__ = "statute_limitations_tracker"

    id = Column(Integer, primary_key=True, index=True)
    matter_type = Column(String(100), nullable=False)  # Contract, Tort, Property, etc.
    claim_description = Column(Text, nullable=False)

    # Parties
    claimant = Column(String(255))
    respondent = Column(String(255))
    property_address = Column(String(500))

    # Timeline
    incident_date = Column(Date, nullable=False)  # When cause of action accrued
    discovery_date = Column(Date)  # For discovery rule jurisdictions

    # Statute Calculation
    jurisdiction = Column(String(100), nullable=False)
    statute_period_years = Column(Integer)
    statute_deadline = Column(Date, nullable=False)
    tolling_periods = Column(JSON)  # Periods when statute was tolled
    extended_deadline = Column(Date)

    # Status
    is_active = Column(Boolean, default=True)
    claim_filed = Column(Boolean, default=False)
    filing_date = Column(Date)
    case_number = Column(String(100))

    # Alerts
    alert_60_days = Column(Boolean, default=False)
    alert_30_days = Column(Boolean, default=False)
    alert_7_days = Column(Boolean, default=False)
    last_alert_sent = Column(Date)

    # Legal Representation
    attorney_assigned = Column(String(255))
    law_firm = Column(String(255))

    notes = Column(Text)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    company = relationship("Company", back_populates="statute_limitations_tracker")


class AuditPreparation(Base):
    """Audit preparation and document collection"""
    __tablename__ = "audit_preparation"

    id = Column(Integer, primary_key=True, index=True)
    audit_name = Column(String(255), nullable=False)
    audit_type = Column(String(100))  # Financial, Compliance, SOC 2, Tax, etc.
    audit_year = Column(Integer)

    # Auditor Information
    auditor_firm = Column(String(255))
    auditor_contact = Column(String(255))
    engagement_letter_date = Column(Date)

    # Timeline
    audit_start_date = Column(Date)
    fieldwork_start_date = Column(Date)
    fieldwork_end_date = Column(Date)
    expected_completion_date = Column(Date)

    # Status
    status = Column(Enum(AuditStatus), default=AuditStatus.NOT_STARTED)

    # Document Collection
    document_request_list = Column(JSON)  # Array of requested documents
    documents_collected = Column(Integer, default=0)
    documents_required = Column(Integer)
    collection_progress = Column(Integer, default=0)  # Percentage

    # Checklist Items
    checklist = Column(JSON)  # Array of audit checklist items
    checklist_completion = Column(Integer, default=0)  # Percentage

    # Findings
    findings_count = Column(Integer, default=0)
    material_weaknesses = Column(Integer, default=0)
    significant_deficiencies = Column(Integer, default=0)
    findings_details = Column(JSON)

    # Management Response
    management_response_required = Column(Boolean, default=False)
    management_response_submitted = Column(Boolean, default=False)
    management_response_date = Column(Date)

    # Remediation
    remediation_plan = Column(JSON)
    remediation_deadline = Column(Date)
    remediation_completed = Column(Boolean, default=False)

    # Final Report
    draft_report_received = Column(Boolean, default=False)
    draft_report_date = Column(Date)
    final_report_received = Column(Boolean, default=False)
    final_report_date = Column(Date)
    audit_opinion = Column(String(100))  # Unqualified, Qualified, Adverse, Disclaimer

    notes = Column(Text)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    company = relationship("Company", back_populates="audit_preparations")


class SOC2Compliance(Base):
    """SOC 2 readiness and compliance tracking"""
    __tablename__ = "soc2_compliance"

    id = Column(Integer, primary_key=True, index=True)
    assessment_name = Column(String(255), nullable=False)
    soc2_type = Column(String(50))  # Type 1 or Type 2

    # Trust Service Criteria
    security_compliant = Column(Boolean, default=False)
    security_score = Column(Integer)  # 0-100

    availability_compliant = Column(Boolean, default=False)
    availability_score = Column(Integer)

    processing_integrity_compliant = Column(Boolean, default=False)
    processing_integrity_score = Column(Integer)

    confidentiality_compliant = Column(Boolean, default=False)
    confidentiality_score = Column(Integer)

    privacy_compliant = Column(Boolean, default=False)
    privacy_score = Column(Integer)

    # Overall Compliance
    overall_readiness_score = Column(Integer)  # 0-100
    compliance_status = Column(Enum(ComplianceStatus), default=ComplianceStatus.UNDER_REVIEW)

    # Controls Assessment
    total_controls = Column(Integer)
    implemented_controls = Column(Integer)
    controls_list = Column(JSON)  # Detailed control checklist

    # Gap Analysis
    gaps_identified = Column(Integer, default=0)
    critical_gaps = Column(Integer, default=0)
    gaps_details = Column(JSON)

    # Remediation
    remediation_plan = Column(JSON)
    remediation_progress = Column(Integer, default=0)  # Percentage
    target_completion_date = Column(Date)

    # Audit
    audit_scheduled = Column(Boolean, default=False)
    audit_date = Column(Date)
    auditor_firm = Column(String(255))
    audit_completed = Column(Boolean, default=False)
    certification_received = Column(Boolean, default=False)
    certification_date = Column(Date)
    certification_expiration = Column(Date)

    # Continuous Monitoring
    last_assessment_date = Column(Date)
    next_assessment_date = Column(Date)
    monitoring_tools = Column(JSON)

    notes = Column(Text)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    company = relationship("Company", back_populates="soc2_compliance")


class ClauseComparison(Base):
    """Track clause comparisons across contracts"""
    __tablename__ = "clause_comparisons"

    id = Column(Integer, primary_key=True, index=True)
    comparison_name = Column(String(255), nullable=False)
    comparison_date = Column(DateTime, default=datetime.utcnow)

    # Documents Being Compared
    document_a_id = Column(Integer)
    document_a_name = Column(String(255))
    document_a_path = Column(String(500))

    document_b_id = Column(Integer)
    document_b_name = Column(String(255))
    document_b_path = Column(String(500))

    # Comparison Results
    clauses_compared = Column(Integer)
    differences_found = Column(Integer)
    similarity_score = Column(Float)  # 0-100

    # Detailed Analysis
    comparison_results = Column(JSON)  # Clause-by-clause comparison
    key_differences = Column(JSON)  # Important differences highlighted
    risk_differences = Column(JSON)  # Risk-related differences

    # AI Analysis
    ai_summary = Column(Text)
    ai_recommendations = Column(JSON)

    # User Actions
    reviewed_by = Column(String(255))
    review_notes = Column(Text)
    approved_version = Column(String(10))  # A, B, or Custom

    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    company = relationship("Company", back_populates="clause_comparisons")
