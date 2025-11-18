"""
Internal Legal Services API Endpoints
All services run internally without external APIs
"""

from typing import List, Optional, Dict, Any
from datetime import date
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from app.services import (
    template_engine,
    TemplateCategory,
    clause_analysis_service,
    ClauseType,
    risk_scoring_service,
    RiskCategory,
    compliance_checklist_service,
    TransactionType,
    deadline_calculator,
    DeadlineType,
    ClaimType
)

router = APIRouter()


# ===== DOCUMENT TEMPLATE GENERATION =====

class DocumentGenerationRequest(BaseModel):
    template_type: str = Field(..., description="Type of document template")
    variables: Dict[str, Any] = Field(..., description="Variables to substitute in template")


class DocumentGenerationResponse(BaseModel):
    document_text: str
    template_type: str
    variables_used: List[str]


class TemplateVariablesResponse(BaseModel):
    template_type: str
    required_variables: List[str]


@router.get("/document-templates/types", response_model=List[str])
def get_available_templates():
    """Get list of available document templates"""
    return [t.value for t in TemplateCategory]


@router.get("/document-templates/{template_type}/variables", response_model=TemplateVariablesResponse)
def get_template_variables(template_type: str):
    """Get required variables for a template"""
    try:
        category = TemplateCategory(template_type)
        variables = template_engine.get_template_variables(category)
        return TemplateVariablesResponse(
            template_type=template_type,
            required_variables=variables
        )
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Template type '{template_type}' not found")


@router.post("/document-templates/generate", response_model=DocumentGenerationResponse)
def generate_document(request: DocumentGenerationRequest):
    """Generate a document from template"""
    try:
        category = TemplateCategory(request.template_type)
        document_text = template_engine.generate_document(category, request.variables)

        return DocumentGenerationResponse(
            document_text=document_text,
            template_type=request.template_type,
            variables_used=list(request.variables.keys())
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/document-templates/validate", response_model=Dict[str, Any])
def validate_template_variables(request: DocumentGenerationRequest):
    """Validate variables for a template"""
    try:
        category = TemplateCategory(request.template_type)
        validation = template_engine.validate_variables(category, request.variables)
        return validation
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ===== CLAUSE ANALYSIS =====

class ClauseAnalysisRequest(BaseModel):
    document_text: str = Field(..., description="Full text of contract or document")


class ClauseAnalysisResponse(BaseModel):
    total_clauses_found: int
    clause_types: List[str]
    risk_distribution: Dict[str, int]
    overall_risk_score: float
    critical_issues: List[Dict[str, Any]]
    clauses: List[Dict[str, Any]]


class ClauseComparisonRequest(BaseModel):
    clause1_text: str
    clause2_text: str
    clause_type: str


class MissingClausesRequest(BaseModel):
    document_text: str
    required_clause_types: List[str]


@router.post("/clause-analysis/analyze", response_model=ClauseAnalysisResponse)
def analyze_contract_clauses(request: ClauseAnalysisRequest):
    """Analyze all clauses in a contract"""
    summary = clause_analysis_service.generate_clause_summary(request.document_text)
    return ClauseAnalysisResponse(**summary)


@router.post("/clause-analysis/compare", response_model=Dict[str, Any])
def compare_clauses(request: ClauseComparisonRequest):
    """Compare two versions of the same clause type"""
    try:
        clause_type = ClauseType(request.clause_type)
        comparison = clause_analysis_service.compare_clauses(
            request.clause1_text,
            request.clause2_text,
            clause_type
        )
        return comparison
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/clause-analysis/missing", response_model=List[str])
def find_missing_clauses(request: MissingClausesRequest):
    """Identify missing required clauses"""
    try:
        required_clauses = [ClauseType(ct) for ct in request.required_clause_types]
        missing = clause_analysis_service.find_missing_clauses(
            request.document_text,
            required_clauses
        )
        return [ct.value for ct in missing]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/clause-analysis/clause-types", response_model=List[str])
def get_supported_clause_types():
    """Get list of supported clause types for analysis"""
    return [ct.value for ct in ClauseType]


# ===== RISK SCORING =====

class ContractRiskRequest(BaseModel):
    value: float = Field(..., description="Contract value in dollars")
    term_months: int = Field(..., description="Contract term in months")
    termination_days: int = Field(default=30, description="Notice period for termination")
    liability_cap: float = Field(default=0, description="Liability cap amount (0 if none)")
    indemnification: bool = Field(default=False, description="Has broad indemnification")
    arbitration: bool = Field(default=False, description="Has arbitration clause")
    governing_law: str = Field(default="", description="State governing law")
    missing_clauses: List[str] = Field(default=[], description="List of missing important clauses")


class ComplianceRiskRequest(BaseModel):
    overdue_items: int = Field(default=0, description="Number of overdue compliance items")
    pending_items: int = Field(default=0, description="Number of pending items")
    last_audit_days_ago: int = Field(default=0, description="Days since last audit")
    violations: int = Field(default=0, description="Number of past violations")
    high_risk_jurisdictions: int = Field(default=0, description="Number of high-risk jurisdictions")
    kyc_complete: bool = Field(default=True, description="KYC/AML complete")
    licenses_current: bool = Field(default=True, description="All licenses current")


class PropertyRiskRequest(BaseModel):
    age_years: int = Field(..., description="Age of property")
    condition_score: int = Field(..., description="1-10 condition rating", ge=1, le=10)
    location_crime_rate: float = Field(default=0, description="Crime rate per 1000")
    flood_zone: bool = Field(default=False, description="In flood zone")
    environmental_issues: bool = Field(default=False, description="Known environmental issues")
    title_issues: bool = Field(default=False, description="Title problems")
    zoning_compliant: bool = Field(default=True, description="Complies with zoning")
    occupancy_rate: float = Field(default=100, description="0-100 percentage", ge=0, le=100)
    deferred_maintenance: float = Field(default=0, description="Estimated cost")


class RiskAssessmentResponse(BaseModel):
    overall_score: float
    risk_level: str
    category_scores: Dict[str, float]
    risk_factors: List[Dict[str, Any]]
    recommendations: List[str]
    critical_items: List[str]


@router.post("/risk-scoring/contract", response_model=RiskAssessmentResponse)
def assess_contract_risk(request: ContractRiskRequest):
    """Assess risk for a contract"""
    assessment = risk_scoring_service.assess_contract_risk(request.dict())

    return RiskAssessmentResponse(
        overall_score=assessment.overall_score,
        risk_level=assessment.risk_level.value,
        category_scores={k.value: v for k, v in assessment.category_scores.items()},
        risk_factors=[
            {
                "name": rf.name,
                "category": rf.category.value,
                "score": rf.score,
                "weight": rf.weight,
                "description": rf.description,
                "mitigation": rf.mitigation
            }
            for rf in assessment.risk_factors
        ],
        recommendations=assessment.recommendations,
        critical_items=assessment.critical_items
    )


@router.post("/risk-scoring/compliance", response_model=RiskAssessmentResponse)
def assess_compliance_risk(request: ComplianceRiskRequest):
    """Assess compliance risk"""
    assessment = risk_scoring_service.assess_compliance_risk(request.dict())

    return RiskAssessmentResponse(
        overall_score=assessment.overall_score,
        risk_level=assessment.risk_level.value,
        category_scores={k.value: v for k, v in assessment.category_scores.items()},
        risk_factors=[
            {
                "name": rf.name,
                "category": rf.category.value,
                "score": rf.score,
                "weight": rf.weight,
                "description": rf.description,
                "mitigation": rf.mitigation
            }
            for rf in assessment.risk_factors
        ],
        recommendations=assessment.recommendations,
        critical_items=assessment.critical_items
    )


@router.post("/risk-scoring/property", response_model=RiskAssessmentResponse)
def assess_property_risk(request: PropertyRiskRequest):
    """Assess risk for a property investment"""
    assessment = risk_scoring_service.assess_property_risk(request.dict())

    return RiskAssessmentResponse(
        overall_score=assessment.overall_score,
        risk_level=assessment.risk_level.value,
        category_scores={k.value: v for k, v in assessment.category_scores.items()},
        risk_factors=[
            {
                "name": rf.name,
                "category": rf.category.value,
                "score": rf.score,
                "weight": rf.weight,
                "description": rf.description,
                "mitigation": rf.mitigation
            }
            for rf in assessment.risk_factors
        ],
        recommendations=assessment.recommendations,
        critical_items=assessment.critical_items
    )


# ===== COMPLIANCE CHECKLISTS =====

class ChecklistGenerationRequest(BaseModel):
    transaction_type: str = Field(..., description="Type of transaction")
    state: str = Field(..., description="State where transaction occurs")
    include_optional: bool = Field(default=False, description="Include optional items")


class ChecklistResponse(BaseModel):
    transaction_type: str
    state: str
    total_items: int
    estimated_total_days: int
    critical_path: List[str]
    items: List[Dict[str, Any]]


@router.post("/compliance-checklists/generate", response_model=ChecklistResponse)
def generate_compliance_checklist(request: ChecklistGenerationRequest):
    """Generate compliance checklist for a transaction"""
    try:
        transaction_type = TransactionType(request.transaction_type)
        checklist = compliance_checklist_service.generate_checklist(
            transaction_type,
            request.state,
            request.include_optional
        )

        return ChecklistResponse(
            transaction_type=request.transaction_type,
            state=request.state,
            total_items=len(checklist.items),
            estimated_total_days=checklist.estimated_total_days,
            critical_path=checklist.critical_path,
            items=[
                {
                    "title": item.title,
                    "description": item.description,
                    "category": item.category,
                    "priority": item.priority.value,
                    "required": item.required,
                    "estimated_days": item.estimated_days,
                    "dependencies": item.dependencies,
                    "state_specific": item.state_specific,
                    "statute_reference": item.statute_reference,
                    "deadline_offset_days": item.deadline_offset_days
                }
                for item in checklist.items
            ]
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/compliance-checklists/transaction-types", response_model=List[str])
def get_transaction_types():
    """Get supported transaction types"""
    return [tt.value for tt in TransactionType]


@router.get("/compliance-checklists/state-requirements/{state}", response_model=List[Dict[str, Any]])
def get_state_requirements(state: str):
    """Get state-specific requirements"""
    items = compliance_checklist_service.get_state_specific_requirements(state)

    return [
        {
            "title": item.title,
            "description": item.description,
            "category": item.category,
            "priority": item.priority.value,
            "statute_reference": item.statute_reference
        }
        for item in items
    ]


# ===== DEADLINE CALCULATOR =====

class StatuteOfLimitationsRequest(BaseModel):
    claim_type: str = Field(..., description="Type of legal claim")
    state: str = Field(..., description="State where claim arises")
    trigger_date: date = Field(..., description="Date when claim accrued")
    trigger_event: str = Field(default="Date of incident", description="Description of triggering event")


class Exchange1031Request(BaseModel):
    relinquished_property_closing_date: date


class OpportunityZoneRequest(BaseModel):
    capital_gain_realization_date: date


class PurchaseContractRequest(BaseModel):
    contract_date: date
    contingencies: Dict[str, int] = Field(..., description="Contingency names and periods in days")


class LeaseNoticeRequest(BaseModel):
    lease_end_date: date
    notice_period_days: int
    notice_type: str = Field(default="Lease Non-Renewal")


class FIRPTARequest(BaseModel):
    closing_date: date


class DeadlineResponse(BaseModel):
    name: str
    deadline_type: str
    deadline_date: date
    trigger_date: date
    trigger_event: str
    days_from_trigger: int
    business_days: bool
    statute_reference: Optional[str]
    consequences_of_missing: str
    reminder_days_before: int
    days_until: int
    status: str


def deadline_to_response(deadline) -> DeadlineResponse:
    """Convert Deadline object to response model"""
    return DeadlineResponse(
        name=deadline.name,
        deadline_type=deadline.deadline_type.value,
        deadline_date=deadline.deadline_date,
        trigger_date=deadline.trigger_date,
        trigger_event=deadline.trigger_event,
        days_from_trigger=deadline.days_from_trigger,
        business_days=deadline.business_days,
        statute_reference=deadline.statute_reference,
        consequences_of_missing=deadline.consequences_of_missing,
        reminder_days_before=deadline.reminder_days_before,
        days_until=deadline_calculator.days_until_deadline(deadline.deadline_date),
        status=deadline_calculator.get_deadline_status(deadline)
    )


@router.post("/deadlines/statute-of-limitations", response_model=DeadlineResponse)
def calculate_statute_of_limitations(request: StatuteOfLimitationsRequest):
    """Calculate statute of limitations deadline"""
    try:
        claim_type = ClaimType(request.claim_type)
        deadline = deadline_calculator.calculate_statute_of_limitations(
            claim_type,
            request.state,
            request.trigger_date,
            request.trigger_event
        )
        return deadline_to_response(deadline)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/deadlines/1031-exchange", response_model=List[DeadlineResponse])
def calculate_1031_deadlines(request: Exchange1031Request):
    """Calculate 1031 exchange deadlines"""
    deadlines = deadline_calculator.calculate_1031_exchange_deadlines(
        request.relinquished_property_closing_date
    )
    return [deadline_to_response(d) for d in deadlines]


@router.post("/deadlines/opportunity-zone", response_model=List[DeadlineResponse])
def calculate_opportunity_zone_deadlines(request: OpportunityZoneRequest):
    """Calculate Opportunity Zone deadlines"""
    deadlines = deadline_calculator.calculate_opportunity_zone_deadlines(
        request.capital_gain_realization_date
    )
    return [deadline_to_response(d) for d in deadlines]


@router.post("/deadlines/purchase-contract", response_model=List[DeadlineResponse])
def calculate_purchase_deadlines(request: PurchaseContractRequest):
    """Calculate purchase contract contingency deadlines"""
    deadlines = deadline_calculator.calculate_purchase_contract_deadlines(
        request.contract_date,
        request.contingencies
    )
    return [deadline_to_response(d) for d in deadlines]


@router.post("/deadlines/lease-notice", response_model=DeadlineResponse)
def calculate_lease_notice_deadline(request: LeaseNoticeRequest):
    """Calculate lease notice deadline"""
    deadline = deadline_calculator.calculate_lease_notice_deadlines(
        request.lease_end_date,
        request.notice_period_days,
        request.notice_type
    )
    return deadline_to_response(deadline)


@router.post("/deadlines/firpta", response_model=DeadlineResponse)
def calculate_firpta_deadline(request: FIRPTARequest):
    """Calculate FIRPTA filing deadline"""
    deadline = deadline_calculator.calculate_firpta_deadline(request.closing_date)
    return deadline_to_response(deadline)


@router.get("/deadlines/claim-types", response_model=List[str])
def get_claim_types():
    """Get supported claim types for statute of limitations"""
    return [ct.value for ct in ClaimType]


# ===== UTILITY ENDPOINTS =====

@router.get("/health")
def health_check():
    """Health check for internal legal services"""
    return {
        "status": "healthy",
        "services": {
            "document_templates": "active",
            "clause_analysis": "active",
            "risk_scoring": "active",
            "compliance_checklists": "active",
            "deadline_calculator": "active"
        },
        "requires_external_apis": False
    }
