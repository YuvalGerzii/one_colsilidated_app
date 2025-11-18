"""
Compliance and Audit API Endpoints

Comprehensive endpoints for regulatory compliance, audit preparation,
and legal compliance tracking.
"""

from typing import List, Optional
from datetime import date, datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from pydantic import BaseModel, Field
from decimal import Decimal

from app.core.database import get_db
from app.models.compliance_audit import (
    Exchange1031Tracking,
    OpportunityZoneInvestment,
    FIRPTACompliance,
    FairHousingCompliance,
    InvestorKYCAML,
    LegalHold,
    StatuteOfLimitationsTracker,
    AuditPreparation,
    SOC2Compliance,
    ClauseComparison,
    Exchange1031Status,
    OpportunityZoneStatus,
    ComplianceStatus,
    AuditStatus,
)


router = APIRouter()


# ================================
# PYDANTIC SCHEMAS
# ================================

# 1031 Exchange Schemas
class Exchange1031Create(BaseModel):
    exchange_name: str
    relinquished_property_address: Optional[str] = None
    relinquished_property_value: Optional[Decimal] = None
    sale_date: Optional[date] = None
    company_id: int

    class Config:
        from_attributes = True


class Exchange1031Response(BaseModel):
    id: int
    exchange_name: str
    status: Exchange1031Status
    relinquished_property_address: Optional[str]
    relinquished_property_value: Optional[Decimal]
    sale_date: Optional[date]
    identification_deadline: Optional[date]
    exchange_deadline: Optional[date]
    deferred_gain: Optional[Decimal]
    estimated_tax_savings: Optional[Decimal]
    company_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Opportunity Zone Schemas
class OpportunityZoneCreate(BaseModel):
    investment_name: str
    property_address: str
    investment_date: date
    investment_amount: Decimal
    capital_gain_invested: Optional[Decimal] = None
    company_id: int

    class Config:
        from_attributes = True


class OpportunityZoneResponse(BaseModel):
    id: int
    investment_name: str
    property_address: str
    status: OpportunityZoneStatus
    investment_date: date
    investment_amount: Decimal
    required_hold_date: Optional[date]
    five_year_milestone: Optional[date]
    seven_year_milestone: Optional[date]
    estimated_tax_free_gain: Optional[Decimal]
    company_id: int

    class Config:
        from_attributes = True


# FIRPTA Schemas
class FIRPTACreate(BaseModel):
    transaction_name: str
    property_address: str
    seller_name: str
    is_foreign_person: bool
    sale_price: Decimal
    sale_date: Optional[date] = None
    company_id: int

    class Config:
        from_attributes = True


class FIRPTAResponse(BaseModel):
    id: int
    transaction_name: str
    property_address: str
    seller_name: str
    is_foreign_person: bool
    sale_price: Decimal
    withholding_rate: Optional[float]
    withholding_amount: Optional[Decimal]
    exemption_claimed: bool
    form_8288_filed: bool
    compliance_status: ComplianceStatus
    company_id: int

    class Config:
        from_attributes = True


# Fair Housing Schemas
class FairHousingCreate(BaseModel):
    property_address: str
    compliance_check_date: date
    company_id: int

    class Config:
        from_attributes = True


class FairHousingResponse(BaseModel):
    id: int
    property_address: str
    compliance_check_date: date
    advertising_compliant: bool
    application_process_compliant: bool
    screening_criteria_compliant: bool
    reasonable_accommodation_policy: bool
    equal_opportunity_posting: bool
    staff_training_completed: bool
    compliance_status: ComplianceStatus
    compliance_score: Optional[int]
    company_id: int

    class Config:
        from_attributes = True


# KYC/AML Schemas
class InvestorKYCCreate(BaseModel):
    investor_name: str
    investor_type: str
    investor_country: str
    company_id: int

    class Config:
        from_attributes = True


class InvestorKYCResponse(BaseModel):
    id: int
    investor_name: str
    investor_type: str
    investor_country: str
    identity_verified: bool
    accredited_investor: Optional[bool]
    pep_screening_completed: bool
    sanctions_screening_completed: bool
    risk_rating: Optional[str]
    kyc_status: ComplianceStatus
    aml_status: ComplianceStatus
    approved_for_investment: bool
    company_id: int

    class Config:
        from_attributes = True


# Legal Hold Schemas
class LegalHoldCreate(BaseModel):
    hold_name: str
    hold_issued_date: date
    hold_reason: str
    custodians: List[dict]
    company_id: int

    class Config:
        from_attributes = True


class LegalHoldResponse(BaseModel):
    id: int
    hold_name: str
    matter_name: Optional[str]
    hold_issued_date: date
    hold_reason: str
    is_active: bool
    notification_sent: bool
    documents_preserved: int
    company_id: int

    class Config:
        from_attributes = True


# Statute of Limitations Schemas
class StatuteLimitationsCreate(BaseModel):
    matter_type: str
    claim_description: str
    incident_date: date
    jurisdiction: str
    statute_period_years: int
    company_id: int

    class Config:
        from_attributes = True


class StatuteLimitationsResponse(BaseModel):
    id: int
    matter_type: str
    claim_description: str
    incident_date: date
    jurisdiction: str
    statute_deadline: date
    is_active: bool
    claim_filed: bool
    company_id: int

    class Config:
        from_attributes = True


# Audit Preparation Schemas
class AuditPreparationCreate(BaseModel):
    audit_name: str
    audit_type: str
    audit_year: int
    company_id: int

    class Config:
        from_attributes = True


class AuditPreparationResponse(BaseModel):
    id: int
    audit_name: str
    audit_type: str
    audit_year: int
    status: AuditStatus
    audit_start_date: Optional[date]
    expected_completion_date: Optional[date]
    collection_progress: int
    checklist_completion: int
    findings_count: int
    company_id: int

    class Config:
        from_attributes = True


# SOC 2 Schemas
class SOC2ComplianceCreate(BaseModel):
    assessment_name: str
    soc2_type: str
    company_id: int

    class Config:
        from_attributes = True


class SOC2ComplianceResponse(BaseModel):
    id: int
    assessment_name: str
    soc2_type: str
    security_compliant: bool
    availability_compliant: bool
    processing_integrity_compliant: bool
    confidentiality_compliant: bool
    privacy_compliant: bool
    overall_readiness_score: Optional[int]
    compliance_status: ComplianceStatus
    gaps_identified: int
    company_id: int

    class Config:
        from_attributes = True


# Clause Comparison Schemas
class ClauseComparisonCreate(BaseModel):
    comparison_name: str
    document_a_name: str
    document_b_name: str
    company_id: int

    class Config:
        from_attributes = True


class ClauseComparisonResponse(BaseModel):
    id: int
    comparison_name: str
    document_a_name: str
    document_b_name: str
    clauses_compared: Optional[int]
    differences_found: Optional[int]
    similarity_score: Optional[float]
    company_id: int
    comparison_date: datetime

    class Config:
        from_attributes = True


# ================================
# 1031 EXCHANGE ENDPOINTS
# ================================

@router.get("/1031-exchanges", response_model=List[Exchange1031Response])
def get_1031_exchanges(
    company_id: int = Query(...),
    status: Optional[Exchange1031Status] = Query(None),
    db: Session = Depends(get_db)
):
    """Get all 1031 exchanges"""
    query = db.query(Exchange1031Tracking).filter(Exchange1031Tracking.company_id == company_id)

    if status:
        query = query.filter(Exchange1031Tracking.status == status)

    exchanges = query.order_by(Exchange1031Tracking.created_at.desc()).all()
    return exchanges


@router.post("/1031-exchanges", response_model=Exchange1031Response)
def create_1031_exchange(
    exchange: Exchange1031Create,
    db: Session = Depends(get_db)
):
    """Create a new 1031 exchange tracking"""
    db_exchange = Exchange1031Tracking(**exchange.model_dump())

    # Calculate deadlines if sale date is provided
    if db_exchange.sale_date:
        db_exchange.identification_deadline = db_exchange.sale_date + timedelta(days=45)
        db_exchange.exchange_deadline = db_exchange.sale_date + timedelta(days=180)

    db.add(db_exchange)
    db.commit()
    db.refresh(db_exchange)
    return db_exchange


@router.get("/1031-exchanges/{exchange_id}", response_model=Exchange1031Response)
def get_1031_exchange(
    exchange_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific 1031 exchange"""
    exchange = db.query(Exchange1031Tracking).filter(Exchange1031Tracking.id == exchange_id).first()
    if not exchange:
        raise HTTPException(status_code=404, detail="1031 exchange not found")
    return exchange


@router.post("/1031-exchanges/{exchange_id}/calculate")
def calculate_1031_savings(
    exchange_id: int,
    db: Session = Depends(get_db)
):
    """Calculate tax savings for 1031 exchange"""
    exchange = db.query(Exchange1031Tracking).filter(Exchange1031Tracking.id == exchange_id).first()
    if not exchange:
        raise HTTPException(status_code=404, detail="1031 exchange not found")

    # Simplified calculation (actual would be more complex)
    if exchange.sale_proceeds and exchange.relinquished_property_value:
        capital_gain = exchange.sale_proceeds - (exchange.relinquished_property_value * Decimal('0.5'))  # Simplified basis
        tax_rate = Decimal('0.20')  # Federal capital gains rate
        exchange.deferred_gain = capital_gain
        exchange.estimated_tax_savings = capital_gain * tax_rate

        db.commit()
        db.refresh(exchange)

    return {
        "deferred_gain": float(exchange.deferred_gain) if exchange.deferred_gain else 0,
        "estimated_tax_savings": float(exchange.estimated_tax_savings) if exchange.estimated_tax_savings else 0,
        "identification_deadline": exchange.identification_deadline.isoformat() if exchange.identification_deadline else None,
        "exchange_deadline": exchange.exchange_deadline.isoformat() if exchange.exchange_deadline else None
    }


# ================================
# OPPORTUNITY ZONE ENDPOINTS
# ================================

@router.get("/opportunity-zones", response_model=List[OpportunityZoneResponse])
def get_opportunity_zones(
    company_id: int = Query(...),
    status: Optional[OpportunityZoneStatus] = Query(None),
    db: Session = Depends(get_db)
):
    """Get all opportunity zone investments"""
    query = db.query(OpportunityZoneInvestment).filter(OpportunityZoneInvestment.company_id == company_id)

    if status:
        query = query.filter(OpportunityZoneInvestment.status == status)

    investments = query.order_by(OpportunityZoneInvestment.investment_date.desc()).all()
    return investments


@router.post("/opportunity-zones", response_model=OpportunityZoneResponse)
def create_opportunity_zone(
    investment: OpportunityZoneCreate,
    db: Session = Depends(get_db)
):
    """Create a new opportunity zone investment"""
    db_investment = OpportunityZoneInvestment(**investment.model_dump())

    # Calculate milestone dates
    if db_investment.investment_date:
        db_investment.required_hold_date = date(db_investment.investment_date.year + 10,
                                                  db_investment.investment_date.month,
                                                  db_investment.investment_date.day)
        db_investment.five_year_milestone = date(db_investment.investment_date.year + 5,
                                                   db_investment.investment_date.month,
                                                   db_investment.investment_date.day)
        db_investment.seven_year_milestone = date(db_investment.investment_date.year + 7,
                                                    db_investment.investment_date.month,
                                                    db_investment.investment_date.day)
        # Deferral expires Dec 31, 2026 or on sale, whichever is earlier
        db_investment.deferral_expiration_date = date(2026, 12, 31)

    db.add(db_investment)
    db.commit()
    db.refresh(db_investment)
    return db_investment


@router.post("/opportunity-zones/{investment_id}/calculate-benefits")
def calculate_oz_benefits(
    investment_id: int,
    db: Session = Depends(get_db)
):
    """Calculate Opportunity Zone tax benefits"""
    investment = db.query(OpportunityZoneInvestment).filter(OpportunityZoneInvestment.id == investment_id).first()
    if not investment:
        raise HTTPException(status_code=404, detail="Investment not found")

    if investment.capital_gain_invested:
        # 10% step-up at 5 years
        investment.basis_step_up_5yr = investment.capital_gain_invested * Decimal('0.10')
        # Additional 5% at 7 years (total 15%)
        investment.basis_step_up_7yr = investment.capital_gain_invested * Decimal('0.05')
        # Potential tax-free gain after 10 years
        investment.estimated_tax_free_gain = investment.investment_amount * Decimal('0.30')  # Estimated appreciation

        db.commit()
        db.refresh(investment)

    return {
        "deferral_amount": float(investment.capital_gain_invested) if investment.capital_gain_invested else 0,
        "basis_step_up_5yr": float(investment.basis_step_up_5yr) if investment.basis_step_up_5yr else 0,
        "basis_step_up_7yr": float(investment.basis_step_up_7yr) if investment.basis_step_up_7yr else 0,
        "estimated_tax_free_gain": float(investment.estimated_tax_free_gain) if investment.estimated_tax_free_gain else 0,
        "hold_requirement_date": investment.required_hold_date.isoformat() if investment.required_hold_date else None
    }


# ================================
# FIRPTA COMPLIANCE ENDPOINTS
# ================================

@router.get("/firpta", response_model=List[FIRPTAResponse])
def get_firpta_records(
    company_id: int = Query(...),
    db: Session = Depends(get_db)
):
    """Get all FIRPTA compliance records"""
    records = db.query(FIRPTACompliance).filter(
        FIRPTACompliance.company_id == company_id
    ).order_by(FIRPTACompliance.created_at.desc()).all()
    return records


@router.post("/firpta", response_model=FIRPTAResponse)
def create_firpta_record(
    record: FIRPTACreate,
    db: Session = Depends(get_db)
):
    """Create a new FIRPTA compliance record"""
    db_record = FIRPTACompliance(**record.model_dump())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


@router.post("/firpta/{record_id}/calculate-withholding")
def calculate_firpta_withholding(
    record_id: int,
    db: Session = Depends(get_db)
):
    """Calculate FIRPTA withholding amount"""
    record = db.query(FIRPTACompliance).filter(FIRPTACompliance.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="FIRPTA record not found")

    # Standard withholding is 15%, but can be 10% for residential under $1M
    if record.property_type == "Residential" and record.sale_price < 1000000:
        record.withholding_rate = 10.0
    else:
        record.withholding_rate = 15.0

    record.withholding_amount = record.sale_price * Decimal(str(record.withholding_rate / 100))

    db.commit()
    db.refresh(record)

    return {
        "sale_price": float(record.sale_price),
        "withholding_rate": record.withholding_rate,
        "withholding_amount": float(record.withholding_amount),
        "exemption_available": record.sale_price < 300000 and record.property_type == "Residential"
    }


# ================================
# FAIR HOUSING ENDPOINTS
# ================================

@router.get("/fair-housing", response_model=List[FairHousingResponse])
def get_fair_housing_records(
    company_id: int = Query(...),
    db: Session = Depends(get_db)
):
    """Get all Fair Housing compliance records"""
    records = db.query(FairHousingCompliance).filter(
        FairHousingCompliance.company_id == company_id
    ).order_by(FairHousingCompliance.compliance_check_date.desc()).all()
    return records


@router.post("/fair-housing", response_model=FairHousingResponse)
def create_fair_housing_record(
    record: FairHousingCreate,
    db: Session = Depends(get_db)
):
    """Create a new Fair Housing compliance record"""
    db_record = FairHousingCompliance(**record.model_dump())

    # Calculate initial compliance score
    score = 0
    if db_record.advertising_compliant: score += 20
    if db_record.application_process_compliant: score += 20
    if db_record.screening_criteria_compliant: score += 20
    if db_record.reasonable_accommodation_policy: score += 20
    if db_record.equal_opportunity_posting: score += 20

    db_record.compliance_score = score
    db_record.compliance_status = ComplianceStatus.COMPLIANT if score == 100 else ComplianceStatus.UNDER_REVIEW

    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


# ================================
# KYC/AML ENDPOINTS
# ================================

@router.get("/kyc-aml", response_model=List[InvestorKYCResponse])
def get_kyc_records(
    company_id: int = Query(...),
    risk_rating: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get all KYC/AML records"""
    query = db.query(InvestorKYCAML).filter(InvestorKYCAML.company_id == company_id)

    if risk_rating:
        query = query.filter(InvestorKYCAML.risk_rating == risk_rating)

    records = query.order_by(InvestorKYCAML.created_at.desc()).all()
    return records


@router.post("/kyc-aml", response_model=InvestorKYCResponse)
def create_kyc_record(
    record: InvestorKYCCreate,
    db: Session = Depends(get_db)
):
    """Create a new KYC/AML record"""
    db_record = InvestorKYCAML(**record.model_dump())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


@router.post("/kyc-aml/{record_id}/screen")
def screen_investor(
    record_id: int,
    db: Session = Depends(get_db)
):
    """Perform PEP and sanctions screening"""
    record = db.query(InvestorKYCAML).filter(InvestorKYCAML.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="KYC record not found")

    # Placeholder for actual screening logic
    record.pep_screening_completed = True
    record.pep_screening_date = date.today()
    record.sanctions_screening_completed = True
    record.sanctions_screening_date = date.today()
    record.sanctions_match_found = False

    # Auto-assign risk rating based on factors
    if record.high_risk_jurisdiction or record.is_pep:
        record.risk_rating = "High"
        record.enhanced_due_diligence_required = True
    else:
        record.risk_rating = "Low"

    db.commit()
    db.refresh(record)

    return {
        "screening_completed": True,
        "pep_screening": "Completed",
        "sanctions_screening": "Completed",
        "risk_rating": record.risk_rating,
        "edd_required": record.enhanced_due_diligence_required
    }


# ================================
# LEGAL HOLD ENDPOINTS
# ================================

@router.get("/legal-holds", response_model=List[LegalHoldResponse])
def get_legal_holds(
    company_id: int = Query(...),
    active_only: bool = Query(True),
    db: Session = Depends(get_db)
):
    """Get all legal holds"""
    query = db.query(LegalHold).filter(LegalHold.company_id == company_id)

    if active_only:
        query = query.filter(LegalHold.is_active == True)

    holds = query.order_by(LegalHold.hold_issued_date.desc()).all()
    return holds


@router.post("/legal-holds", response_model=LegalHoldResponse)
def create_legal_hold(
    hold: LegalHoldCreate,
    db: Session = Depends(get_db)
):
    """Create a new legal hold"""
    db_hold = LegalHold(**hold.model_dump())
    db.add(db_hold)
    db.commit()
    db.refresh(db_hold)
    return db_hold


@router.post("/legal-holds/{hold_id}/release")
def release_legal_hold(
    hold_id: int,
    released_by: str,
    db: Session = Depends(get_db)
):
    """Release a legal hold"""
    hold = db.query(LegalHold).filter(LegalHold.id == hold_id).first()
    if not hold:
        raise HTTPException(status_code=404, detail="Legal hold not found")

    hold.is_active = False
    hold.release_date = date.today()
    hold.release_authorized_by = released_by

    db.commit()
    db.refresh(hold)

    return {"message": "Legal hold released successfully", "hold_id": hold_id}


# ================================
# STATUTE OF LIMITATIONS ENDPOINTS
# ================================

@router.get("/statute-limitations", response_model=List[StatuteLimitationsResponse])
def get_statute_limitations(
    company_id: int = Query(...),
    active_only: bool = Query(True),
    db: Session = Depends(get_db)
):
    """Get all statute of limitations trackers"""
    query = db.query(StatuteOfLimitationsTracker).filter(
        StatuteOfLimitationsTracker.company_id == company_id
    )

    if active_only:
        query = query.filter(
            StatuteOfLimitationsTracker.is_active == True,
            StatuteOfLimitationsTracker.claim_filed == False
        )

    trackers = query.order_by(StatuteOfLimitationsTracker.statute_deadline).all()
    return trackers


@router.post("/statute-limitations", response_model=StatuteLimitationsResponse)
def create_statute_tracker(
    tracker: StatuteLimitationsCreate,
    db: Session = Depends(get_db)
):
    """Create a new statute of limitations tracker"""
    db_tracker = StatuteOfLimitationsTracker(**tracker.model_dump())

    # Calculate statute deadline
    db_tracker.statute_deadline = date(
        db_tracker.incident_date.year + db_tracker.statute_period_years,
        db_tracker.incident_date.month,
        db_tracker.incident_date.day
    )

    db.add(db_tracker)
    db.commit()
    db.refresh(db_tracker)
    return db_tracker


# ================================
# AUDIT PREPARATION ENDPOINTS
# ================================

@router.get("/audit-preparation", response_model=List[AuditPreparationResponse])
def get_audit_preparations(
    company_id: int = Query(...),
    audit_year: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """Get all audit preparations"""
    query = db.query(AuditPreparation).filter(AuditPreparation.company_id == company_id)

    if audit_year:
        query = query.filter(AuditPreparation.audit_year == audit_year)

    audits = query.order_by(AuditPreparation.audit_year.desc()).all()
    return audits


@router.post("/audit-preparation", response_model=AuditPreparationResponse)
def create_audit_preparation(
    audit: AuditPreparationCreate,
    db: Session = Depends(get_db)
):
    """Create a new audit preparation"""
    db_audit = AuditPreparation(**audit.model_dump())
    db.add(db_audit)
    db.commit()
    db.refresh(db_audit)
    return db_audit


@router.post("/audit-preparation/{audit_id}/update-progress")
def update_audit_progress(
    audit_id: int,
    documents_collected: int,
    checklist_completion: int,
    db: Session = Depends(get_db)
):
    """Update audit preparation progress"""
    audit = db.query(AuditPreparation).filter(AuditPreparation.id == audit_id).first()
    if not audit:
        raise HTTPException(status_code=404, detail="Audit preparation not found")

    audit.documents_collected = documents_collected
    audit.checklist_completion = checklist_completion

    if audit.documents_required:
        audit.collection_progress = int((documents_collected / audit.documents_required) * 100)

    db.commit()
    db.refresh(audit)

    return {
        "audit_id": audit_id,
        "collection_progress": audit.collection_progress,
        "checklist_completion": audit.checklist_completion
    }


# ================================
# SOC 2 COMPLIANCE ENDPOINTS
# ================================

@router.get("/soc2-compliance", response_model=List[SOC2ComplianceResponse])
def get_soc2_assessments(
    company_id: int = Query(...),
    db: Session = Depends(get_db)
):
    """Get all SOC 2 compliance assessments"""
    assessments = db.query(SOC2Compliance).filter(
        SOC2Compliance.company_id == company_id
    ).order_by(SOC2Compliance.created_at.desc()).all()
    return assessments


@router.post("/soc2-compliance", response_model=SOC2ComplianceResponse)
def create_soc2_assessment(
    assessment: SOC2ComplianceCreate,
    db: Session = Depends(get_db)
):
    """Create a new SOC 2 compliance assessment"""
    db_assessment = SOC2Compliance(**assessment.model_dump())
    db.add(db_assessment)
    db.commit()
    db.refresh(db_assessment)
    return db_assessment


@router.post("/soc2-compliance/{assessment_id}/calculate-score")
def calculate_soc2_readiness(
    assessment_id: int,
    db: Session = Depends(get_db)
):
    """Calculate SOC 2 readiness score"""
    assessment = db.query(SOC2Compliance).filter(SOC2Compliance.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    # Calculate overall readiness score
    criteria_scores = [
        assessment.security_score or 0,
        assessment.availability_score or 0,
        assessment.processing_integrity_score or 0,
        assessment.confidentiality_score or 0,
        assessment.privacy_score or 0
    ]

    assessment.overall_readiness_score = int(sum(criteria_scores) / len([s for s in criteria_scores if s > 0])) if any(criteria_scores) else 0

    if assessment.overall_readiness_score >= 80:
        assessment.compliance_status = ComplianceStatus.COMPLIANT
    elif assessment.overall_readiness_score >= 60:
        assessment.compliance_status = ComplianceStatus.UNDER_REVIEW
    else:
        assessment.compliance_status = ComplianceStatus.NON_COMPLIANT

    db.commit()
    db.refresh(assessment)

    return {
        "assessment_id": assessment_id,
        "overall_readiness_score": assessment.overall_readiness_score,
        "compliance_status": assessment.compliance_status.value,
        "gaps_identified": assessment.gaps_identified
    }


# ================================
# CLAUSE COMPARISON ENDPOINTS
# ================================

@router.get("/clause-comparisons", response_model=List[ClauseComparisonResponse])
def get_clause_comparisons(
    company_id: int = Query(...),
    db: Session = Depends(get_db)
):
    """Get all clause comparisons"""
    comparisons = db.query(ClauseComparison).filter(
        ClauseComparison.company_id == company_id
    ).order_by(ClauseComparison.comparison_date.desc()).all()
    return comparisons


@router.post("/clause-comparisons", response_model=ClauseComparisonResponse)
def create_clause_comparison(
    comparison: ClauseComparisonCreate,
    db: Session = Depends(get_db)
):
    """Create a new clause comparison"""
    db_comparison = ClauseComparison(**comparison.model_dump())

    # Placeholder for actual comparison logic
    db_comparison.clauses_compared = 25
    db_comparison.differences_found = 8
    db_comparison.similarity_score = 67.5

    db.add(db_comparison)
    db.commit()
    db.refresh(db_comparison)
    return db_comparison


# ================================
# DASHBOARD SUMMARY
# ================================

@router.get("/compliance-dashboard-summary")
def get_compliance_dashboard_summary(
    company_id: int = Query(...),
    db: Session = Depends(get_db)
):
    """Get comprehensive compliance and audit dashboard summary"""

    # 1031 Exchanges
    active_1031_exchanges = db.query(Exchange1031Tracking).filter(
        Exchange1031Tracking.company_id == company_id,
        Exchange1031Tracking.status.in_([Exchange1031Status.IDENTIFICATION_PERIOD, Exchange1031Status.EXCHANGE_PERIOD])
    ).count()

    # Opportunity Zones
    active_oz_investments = db.query(OpportunityZoneInvestment).filter(
        OpportunityZoneInvestment.company_id == company_id,
        OpportunityZoneInvestment.status == OpportunityZoneStatus.INVESTED
    ).count()

    # FIRPTA
    pending_firpta = db.query(FIRPTACompliance).filter(
        FIRPTACompliance.company_id == company_id,
        FIRPTACompliance.form_8288_filed == False
    ).count()

    # Fair Housing
    fair_housing_compliant = db.query(FairHousingCompliance).filter(
        FairHousingCompliance.company_id == company_id,
        FairHousingCompliance.compliance_status == ComplianceStatus.COMPLIANT
    ).count()

    # KYC/AML
    pending_kyc = db.query(InvestorKYCAML).filter(
        InvestorKYCAML.company_id == company_id,
        InvestorKYCAML.approved_for_investment == False
    ).count()

    # Legal Holds
    active_legal_holds = db.query(LegalHold).filter(
        LegalHold.company_id == company_id,
        LegalHold.is_active == True
    ).count()

    # Statute of Limitations
    upcoming_deadlines = db.query(StatuteOfLimitationsTracker).filter(
        StatuteOfLimitationsTracker.company_id == company_id,
        StatuteOfLimitationsTracker.statute_deadline <= date.today() + timedelta(days=90),
        StatuteOfLimitationsTracker.is_active == True
    ).count()

    # Audits
    active_audits = db.query(AuditPreparation).filter(
        AuditPreparation.company_id == company_id,
        AuditPreparation.status == AuditStatus.IN_PROGRESS
    ).count()

    return {
        "regulatory_compliance": {
            "active_1031_exchanges": active_1031_exchanges,
            "opportunity_zone_investments": active_oz_investments,
            "pending_firpta_filings": pending_firpta,
            "fair_housing_properties": fair_housing_compliant
        },
        "investor_compliance": {
            "pending_kyc_approvals": pending_kyc,
            "high_risk_investors": 0  # Could calculate
        },
        "legal_matters": {
            "active_legal_holds": active_legal_holds,
            "upcoming_statute_deadlines": upcoming_deadlines
        },
        "audit_preparation": {
            "active_audits": active_audits,
            "documents_to_collect": 0  # Could calculate
        }
    }
