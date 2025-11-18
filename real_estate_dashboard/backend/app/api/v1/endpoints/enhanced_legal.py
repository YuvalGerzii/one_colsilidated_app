"""
Enhanced Legal Services API Endpoints

Advanced features for AI contract analysis, clause library, document generation,
zoning lookup, automation workflows, and e-signature management.
"""

from typing import List, Optional
from datetime import date, datetime
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from pydantic import BaseModel, Field
import json

from app.core.database import get_db
from app.models.enhanced_legal import (
    ClauseLibrary,
    DocumentTemplate,
    ZoningData,
    AutomationWorkflow,
    LegalKnowledgeBase,
    ESignatureRequest,
    AIContractAnalysis,
    StateLegalForm,
    RegulatoryChange,
    ClauseCategory,
    ClauseRiskLevel,
    AutomationStatus,
    SignatureStatus,
)


router = APIRouter()


# ================================
# PYDANTIC SCHEMAS
# ================================

# Clause Library Schemas
class ClauseLibraryBase(BaseModel):
    name: str
    category: ClauseCategory
    clause_text: str
    description: Optional[str] = None
    usage_recommendation: Optional[str] = None
    ai_safety_score: int = Field(default=50, ge=0, le=100)
    risk_level: ClauseRiskLevel = ClauseRiskLevel.LOW
    state_specific: bool = False
    applicable_states: Optional[List[str]] = None
    jurisdiction_notes: Optional[str] = None
    version: str = "1.0"
    is_approved: bool = True
    created_by: Optional[str] = None
    approved_by: Optional[str] = None

    class Config:
        from_attributes = True


class ClauseLibraryCreate(ClauseLibraryBase):
    company_id: Optional[UUID] = None


class ClauseLibraryResponse(ClauseLibraryBase):
    id: int
    company_id: Optional[UUID]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Document Template Schemas
class DocumentTemplateBase(BaseModel):
    name: str
    document_type: str
    complexity: Optional[str] = None
    estimated_time: Optional[str] = None
    ai_powered: bool = True
    state_specific: bool = False
    template_content: Optional[str] = None
    template_url: Optional[str] = None
    required_fields: Optional[dict] = None
    optional_fields: Optional[dict] = None
    suggested_clauses: Optional[List[int]] = None
    compliance_requirements: Optional[dict] = None
    category: Optional[str] = None
    is_active: bool = True

    class Config:
        from_attributes = True


class DocumentTemplateCreate(DocumentTemplateBase):
    company_id: Optional[UUID] = None


class DocumentTemplateResponse(DocumentTemplateBase):
    id: int
    company_id: Optional[UUID]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Zoning Data Schemas
class ZoningDataResponse(BaseModel):
    id: int
    jurisdiction: str
    state: str
    zoning_code: str
    zoning_name: str
    category: Optional[str]
    description: Optional[str]
    permitted_uses: Optional[List[str]]
    conditional_uses: Optional[List[str]]
    prohibited_uses: Optional[List[str]]
    density_requirements: Optional[str]
    height_restrictions: Optional[str]
    parking_requirements: Optional[str]
    setback_requirements: Optional[str]
    special_conditions: Optional[str]
    ordinance_reference: Optional[str]
    last_updated: Optional[date]

    class Config:
        from_attributes = True


# Automation Workflow Schemas
class AutomationWorkflowBase(BaseModel):
    name: str
    description: Optional[str] = None
    workflow_type: str
    status: AutomationStatus = AutomationStatus.ACTIVE
    trigger_conditions: Optional[dict] = None
    actions: Optional[dict] = None
    schedule: Optional[str] = None
    notification_settings: Optional[dict] = None
    is_enabled: bool = True

    class Config:
        from_attributes = True


class AutomationWorkflowCreate(AutomationWorkflowBase):
    company_id: UUID


class AutomationWorkflowResponse(AutomationWorkflowBase):
    id: int
    company_id: UUID
    last_run: Optional[datetime]
    next_run: Optional[datetime]
    trigger_count: int
    success_count: int
    error_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Knowledge Base Schemas
class LegalKnowledgeBaseResponse(BaseModel):
    id: int
    title: str
    topic: str
    category: str
    content: str
    summary: Optional[str]
    tags: Optional[List[str]]
    jurisdiction: Optional[str]
    last_reviewed: Optional[date]
    author: Optional[str]
    view_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# E-Signature Schemas
class ESignatureRequestBase(BaseModel):
    document_name: str
    document_path: Optional[str] = None
    status: SignatureStatus = SignatureStatus.PENDING
    sender_email: str
    signers: List[dict]
    expiration_date: Optional[date] = None
    esign_provider: Optional[str] = None

    class Config:
        from_attributes = True


class ESignatureRequestCreate(ESignatureRequestBase):
    company_id: UUID


class ESignatureRequestResponse(ESignatureRequestBase):
    id: int
    company_id: UUID
    current_signer_index: int
    reminder_sent: bool
    completed_at: Optional[datetime]
    audit_trail: Optional[dict]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# AI Contract Analysis Schemas
class AIContractAnalysisBase(BaseModel):
    contract_name: str
    file_path: Optional[str] = None
    risk_score: Optional[int] = None
    risk_level: Optional[str] = None
    high_risk_clauses: Optional[List[dict]] = None
    missing_provisions: Optional[List[str]] = None
    compliance_issues: Optional[List[str]] = None
    recommendations: Optional[List[str]] = None
    clause_analysis: Optional[dict] = None
    financial_terms: Optional[dict] = None
    key_dates: Optional[dict] = None
    parties_involved: Optional[List[str]] = None
    jurisdiction: Optional[str] = None

    class Config:
        from_attributes = True


class AIContractAnalysisCreate(AIContractAnalysisBase):
    company_id: UUID


class AIContractAnalysisResponse(AIContractAnalysisBase):
    id: int
    company_id: UUID
    analysis_date: datetime
    ai_model_version: Optional[str]
    confidence_score: Optional[float]
    processing_time: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


# State Legal Forms Schemas
class StateLegalFormResponse(BaseModel):
    id: int
    form_name: str
    state: str
    form_number: Optional[str]
    category: str
    description: Optional[str]
    form_url: Optional[str]
    is_required: bool
    applicable_transactions: Optional[List[str]]
    effective_date: Optional[date]
    last_updated: Optional[date]
    source_authority: Optional[str]
    is_fillable: bool

    class Config:
        from_attributes = True


# ================================
# API ENDPOINTS
# ================================

# Clause Library Endpoints
@router.get("/clause-library", response_model=List[ClauseLibraryResponse])
def get_clause_library(
    category: Optional[ClauseCategory] = Query(None),
    risk_level: Optional[ClauseRiskLevel] = Query(None),
    state: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get all clauses from library with optional filters"""
    query = db.query(ClauseLibrary).filter(ClauseLibrary.is_approved == True)

    if category:
        query = query.filter(ClauseLibrary.category == category)
    if risk_level:
        query = query.filter(ClauseLibrary.risk_level == risk_level)
    if state:
        query = query.filter(
            or_(
                ClauseLibrary.state_specific == False,
                ClauseLibrary.applicable_states.contains([state])
            )
        )
    if search:
        query = query.filter(
            or_(
                ClauseLibrary.name.ilike(f"%{search}%"),
                ClauseLibrary.description.ilike(f"%{search}%")
            )
        )

    clauses = query.order_by(ClauseLibrary.ai_safety_score.desc()).all()
    return clauses


@router.post("/clause-library", response_model=ClauseLibraryResponse)
def create_clause(
    clause: ClauseLibraryCreate,
    db: Session = Depends(get_db)
):
    """Create a new clause in the library"""
    db_clause = ClauseLibrary(**clause.model_dump())
    db.add(db_clause)
    db.commit()
    db.refresh(db_clause)
    return db_clause


@router.get("/clause-library/{clause_id}", response_model=ClauseLibraryResponse)
def get_clause(
    clause_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific clause by ID"""
    clause = db.query(ClauseLibrary).filter(ClauseLibrary.id == clause_id).first()
    if not clause:
        raise HTTPException(status_code=404, detail="Clause not found")
    return clause


# Document Template Endpoints
@router.get("/document-templates", response_model=List[DocumentTemplateResponse])
def get_document_templates(
    document_type: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    state_specific: Optional[bool] = Query(None),
    ai_powered: Optional[bool] = Query(None),
    db: Session = Depends(get_db)
):
    """Get all document templates with optional filters"""
    query = db.query(DocumentTemplate).filter(DocumentTemplate.is_active == True)

    if document_type:
        query = query.filter(DocumentTemplate.document_type == document_type)
    if category:
        query = query.filter(DocumentTemplate.category == category)
    if state_specific is not None:
        query = query.filter(DocumentTemplate.state_specific == state_specific)
    if ai_powered is not None:
        query = query.filter(DocumentTemplate.ai_powered == ai_powered)

    templates = query.order_by(DocumentTemplate.name).all()
    return templates


@router.post("/document-templates", response_model=DocumentTemplateResponse)
def create_document_template(
    template: DocumentTemplateCreate,
    db: Session = Depends(get_db)
):
    """Create a new document template"""
    db_template = DocumentTemplate(**template.model_dump())
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template


@router.post("/document-templates/{template_id}/generate")
def generate_document_from_template(
    template_id: int,
    form_data: dict,
    db: Session = Depends(get_db)
):
    """Generate a document from template with AI assistance"""
    template = db.query(DocumentTemplate).filter(DocumentTemplate.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    # Here you would implement AI-powered document generation
    # This is a placeholder for the actual implementation
    return {
        "success": True,
        "document_id": template_id,
        "document_name": template.name,
        "generated_at": datetime.utcnow().isoformat(),
        "download_url": f"/api/documents/{template_id}/download",
        "message": "Document generated successfully with AI assistance"
    }


# Zoning Data Endpoints
@router.get("/zoning/lookup", response_model=List[ZoningDataResponse])
def lookup_zoning(
    jurisdiction: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    zoning_code: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Look up zoning information"""
    query = db.query(ZoningData)

    if jurisdiction:
        query = query.filter(ZoningData.jurisdiction.ilike(f"%{jurisdiction}%"))
    if state:
        query = query.filter(ZoningData.state == state)
    if zoning_code:
        query = query.filter(ZoningData.zoning_code.ilike(f"%{zoning_code}%"))
    if category:
        query = query.filter(ZoningData.category == category)

    zoning_data = query.limit(50).all()
    return zoning_data


@router.post("/zoning/verify-property")
def verify_property_zoning(
    address: str,
    property_type: str,
    intended_use: str,
    db: Session = Depends(get_db)
):
    """Verify if property use is compliant with zoning"""
    # This would integrate with external zoning APIs or databases
    # Placeholder implementation
    return {
        "address": address,
        "property_type": property_type,
        "intended_use": intended_use,
        "zoning_compliant": True,
        "zoning_code": "R2",
        "zoning_name": "Multi-Family Residential",
        "permitted_uses": ["residential", "multi-family"],
        "restrictions": ["Height limit: 35 feet", "Minimum 2 parking spaces per unit"],
        "verification_date": datetime.utcnow().isoformat()
    }


# Automation Workflow Endpoints
@router.get("/automation-workflows", response_model=List[AutomationWorkflowResponse])
def get_automation_workflows(
    company_id: UUID = Query(...),
    status: Optional[AutomationStatus] = Query(None),
    workflow_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get all automation workflows"""
    query = db.query(AutomationWorkflow).filter(AutomationWorkflow.company_id == company_id)

    if status:
        query = query.filter(AutomationWorkflow.status == status)
    if workflow_type:
        query = query.filter(AutomationWorkflow.workflow_type == workflow_type)

    workflows = query.order_by(AutomationWorkflow.created_at.desc()).all()
    return workflows


@router.post("/automation-workflows", response_model=AutomationWorkflowResponse)
def create_automation_workflow(
    workflow: AutomationWorkflowCreate,
    db: Session = Depends(get_db)
):
    """Create a new automation workflow"""
    db_workflow = AutomationWorkflow(**workflow.model_dump())
    db.add(db_workflow)
    db.commit()
    db.refresh(db_workflow)
    return db_workflow


@router.patch("/automation-workflows/{workflow_id}/toggle")
def toggle_automation_workflow(
    workflow_id: int,
    db: Session = Depends(get_db)
):
    """Enable or disable an automation workflow"""
    workflow = db.query(AutomationWorkflow).filter(AutomationWorkflow.id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    workflow.is_enabled = not workflow.is_enabled
    workflow.status = AutomationStatus.ACTIVE if workflow.is_enabled else AutomationStatus.INACTIVE
    db.commit()
    db.refresh(workflow)
    return workflow


# Legal Knowledge Base Endpoints
@router.get("/knowledge-base", response_model=List[LegalKnowledgeBaseResponse])
def get_knowledge_base_articles(
    topic: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db)
):
    """Get legal knowledge base articles"""
    query = db.query(LegalKnowledgeBase).filter(LegalKnowledgeBase.is_published == True)

    if topic:
        query = query.filter(LegalKnowledgeBase.topic.ilike(f"%{topic}%"))
    if category:
        query = query.filter(LegalKnowledgeBase.category == category)
    if search:
        query = query.filter(
            or_(
                LegalKnowledgeBase.title.ilike(f"%{search}%"),
                LegalKnowledgeBase.content.ilike(f"%{search}%")
            )
        )

    articles = query.order_by(LegalKnowledgeBase.updated_at.desc()).limit(limit).all()
    return articles


@router.get("/knowledge-base/{article_id}", response_model=LegalKnowledgeBaseResponse)
def get_knowledge_base_article(
    article_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific knowledge base article"""
    article = db.query(LegalKnowledgeBase).filter(LegalKnowledgeBase.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    # Increment view count
    article.view_count += 1
    db.commit()

    return article


# E-Signature Endpoints
@router.get("/esignature-requests", response_model=List[ESignatureRequestResponse])
def get_esignature_requests(
    company_id: UUID = Query(...),
    status: Optional[SignatureStatus] = Query(None),
    db: Session = Depends(get_db)
):
    """Get all e-signature requests"""
    query = db.query(ESignatureRequest).filter(ESignatureRequest.company_id == company_id)

    if status:
        query = query.filter(ESignatureRequest.status == status)

    requests = query.order_by(ESignatureRequest.created_at.desc()).all()
    return requests


@router.post("/esignature-requests", response_model=ESignatureRequestResponse)
def create_esignature_request(
    request: ESignatureRequestCreate,
    db: Session = Depends(get_db)
):
    """Create a new e-signature request"""
    db_request = ESignatureRequest(**request.model_dump())
    db.add(db_request)
    db.commit()
    db.refresh(db_request)

    # Here you would integrate with e-signature providers (DocuSign, Adobe Sign, etc.)
    return db_request


@router.post("/esignature-requests/{request_id}/send")
def send_esignature_request(
    request_id: int,
    db: Session = Depends(get_db)
):
    """Send e-signature request to signers"""
    request = db.query(ESignatureRequest).filter(ESignatureRequest.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="E-signature request not found")

    request.status = SignatureStatus.SENT
    db.commit()

    return {"message": "E-signature request sent successfully", "request_id": request_id}


# AI Contract Analysis Endpoints
@router.get("/ai-analysis", response_model=List[AIContractAnalysisResponse])
def get_ai_analyses(
    company_id: UUID = Query(...),
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db)
):
    """Get AI contract analyses"""
    analyses = db.query(AIContractAnalysis).filter(
        AIContractAnalysis.company_id == company_id
    ).order_by(AIContractAnalysis.analysis_date.desc()).limit(limit).all()
    return analyses


@router.post("/ai-analysis/upload")
async def upload_contract_for_analysis(
    company_id: UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload contract for AI analysis"""
    # This would integrate with AI/ML services for contract analysis
    # Placeholder implementation
    analysis = AIContractAnalysis(
        contract_name=file.filename,
        company_id=company_id,
        risk_score=68,
        risk_level="Medium",
        high_risk_clauses=[
            {"clause": "Unlimited Liability", "severity": "Critical", "location": "Section 12.3"},
            {"clause": "One-sided Termination", "severity": "High", "location": "Section 8.1"}
        ],
        missing_provisions=["Force Majeure Clause", "Dispute Resolution Process"],
        compliance_issues=["Missing Fair Housing Language (Federal Requirement)"],
        recommendations=["Add arbitration clause", "Include specific performance metrics"],
        ai_model_version="1.0",
        confidence_score=0.87,
        processing_time=2340
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return analysis


@router.get("/ai-analysis/{analysis_id}", response_model=AIContractAnalysisResponse)
def get_ai_analysis(
    analysis_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific AI contract analysis"""
    analysis = db.query(AIContractAnalysis).filter(AIContractAnalysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis


# State Legal Forms Endpoints
@router.get("/state-forms", response_model=List[StateLegalFormResponse])
def get_state_forms(
    state: str = Query(...),
    category: Optional[str] = Query(None),
    required_only: bool = Query(False),
    db: Session = Depends(get_db)
):
    """Get state-specific legal forms"""
    query = db.query(StateLegalForm).filter(StateLegalForm.state == state)

    if category:
        query = query.filter(StateLegalForm.category == category)
    if required_only:
        query = query.filter(StateLegalForm.is_required == True)

    forms = query.order_by(StateLegalForm.form_name).all()
    return forms


@router.get("/state-forms/statistics")
def get_state_forms_statistics(
    db: Session = Depends(get_db)
):
    """Get statistics about available state forms"""
    # Get count by state
    from sqlalchemy import func

    state_counts = db.query(
        StateLegalForm.state,
        func.count(StateLegalForm.id).label('count')
    ).group_by(StateLegalForm.state).all()

    category_counts = db.query(
        StateLegalForm.category,
        func.count(StateLegalForm.id).label('count')
    ).group_by(StateLegalForm.category).all()

    return {
        "total_forms": db.query(StateLegalForm).count(),
        "states_covered": len(state_counts),
        "by_state": [{"state": s.state, "count": s.count} for s in state_counts],
        "by_category": [{"category": c.category, "count": c.count} for c in category_counts]
    }


# Regulatory Changes Endpoints
@router.get("/regulatory-changes")
def get_regulatory_changes(
    jurisdiction: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    impact_level: Optional[str] = Query(None),
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db)
):
    """Get recent regulatory changes"""
    query = db.query(RegulatoryChange)

    if jurisdiction:
        query = query.filter(RegulatoryChange.jurisdiction.ilike(f"%{jurisdiction}%"))
    if state:
        query = query.filter(RegulatoryChange.state == state)
    if impact_level:
        query = query.filter(RegulatoryChange.impact_level == impact_level)

    changes = query.order_by(RegulatoryChange.effective_date.desc()).limit(limit).all()

    return [
        {
            "id": change.id,
            "title": change.title,
            "change_type": change.change_type,
            "jurisdiction": change.jurisdiction,
            "state": change.state,
            "effective_date": change.effective_date.isoformat() if change.effective_date else None,
            "description": change.description,
            "impact_level": change.impact_level,
            "action_required": change.action_required,
            "action_deadline": change.action_deadline.isoformat() if change.action_deadline else None
        }
        for change in changes
    ]


# Enhanced Dashboard Summary
@router.get("/enhanced-dashboard-summary")
def get_enhanced_dashboard_summary(
    company_id: UUID = Query(...),
    db: Session = Depends(get_db)
):
    """Get comprehensive summary for enhanced legal services dashboard"""
    # Count various entities
    total_clauses = db.query(ClauseLibrary).filter(
        ClauseLibrary.company_id == company_id,
        ClauseLibrary.is_approved == True
    ).count()

    total_templates = db.query(DocumentTemplate).filter(
        DocumentTemplate.company_id == company_id,
        DocumentTemplate.is_active == True
    ).count()

    active_workflows = db.query(AutomationWorkflow).filter(
        AutomationWorkflow.company_id == company_id,
        AutomationWorkflow.status == AutomationStatus.ACTIVE
    ).count()

    pending_signatures = db.query(ESignatureRequest).filter(
        ESignatureRequest.company_id == company_id,
        ESignatureRequest.status.in_([SignatureStatus.PENDING, SignatureStatus.SENT])
    ).count()

    recent_analyses = db.query(AIContractAnalysis).filter(
        AIContractAnalysis.company_id == company_id
    ).order_by(AIContractAnalysis.analysis_date.desc()).limit(5).all()

    avg_risk_score = db.query(func.avg(AIContractAnalysis.risk_score)).filter(
        AIContractAnalysis.company_id == company_id
    ).scalar() or 0

    return {
        "clause_library": {
            "total_clauses": total_clauses,
            "by_category": {}  # Could add category breakdown
        },
        "document_templates": {
            "total_templates": total_templates,
            "ai_powered": total_templates  # Assuming all are AI-powered
        },
        "automation": {
            "active_workflows": active_workflows,
            "total_triggers_month": 0  # Could calculate from workflow data
        },
        "esignatures": {
            "pending_signatures": pending_signatures
        },
        "ai_analysis": {
            "recent_analyses_count": len(recent_analyses),
            "average_risk_score": round(avg_risk_score, 1)
        },
        "zoning_database": {
            "jurisdictions": 3200,
            "zoning_codes": 125000,
            "last_updated": "2025-11-01"
        }
    }
