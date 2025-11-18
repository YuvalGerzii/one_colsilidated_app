"""
PDF Extraction API Endpoints

RESTful API for:
- PDF document upload and extraction
- Financial statement data retrieval
- Historical valuation tracking
- Comparison and analysis
"""

import os
import uuid
import shutil
from typing import List, Optional
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, Query, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.core.database import get_db
from app.services.pdf_extraction_service import PDFExtractionService, get_pdf_service
from app.models.pdf_documents import DocumentType, ExtractionStatus, PeriodType

router = APIRouter()


# =====================================================================
# Pydantic Schemas
# =====================================================================

class DocumentUploadResponse(BaseModel):
    """Response after PDF upload"""
    document_id: str
    status: str
    confidence: float
    needs_review: bool
    statements_extracted: dict
    periods: list
    records_created: int


class DocumentInfo(BaseModel):
    """Document metadata"""
    id: str
    document_name: str
    document_type: str
    company_id: Optional[str]
    company_name: Optional[str]
    extraction_status: str
    extraction_confidence: Optional[float]
    upload_date: str
    needs_review: bool


class ExtractedStatements(BaseModel):
    """All extracted statements for a document"""
    document: dict
    income_statements: List[dict]
    balance_sheets: List[dict]
    cash_flows: List[dict]


class ValuationSnapshotCreate(BaseModel):
    """Create a valuation snapshot"""
    company_id: str
    model_type: str
    enterprise_value: float
    equity_value: float
    dcf_model_id: Optional[str] = None
    lbo_model_id: Optional[str] = None
    key_assumptions: Optional[dict] = None


class ValuationSnapshotResponse(BaseModel):
    """Valuation snapshot response"""
    id: str
    company_id: str
    model_type: str
    enterprise_value: float
    equity_value: float
    snapshot_date: str
    wacc: Optional[float]
    terminal_growth_rate: Optional[float]
    entry_multiple: Optional[float]
    exit_multiple: Optional[float]
    equity_irr: Optional[float]
    moic: Optional[float]


class ValuationComparisonRequest(BaseModel):
    """Request to compare two valuations"""
    baseline_snapshot_id: str
    comparison_snapshot_id: str


class ValuationComparisonResponse(BaseModel):
    """Valuation comparison results"""
    id: str
    company_id: str
    ev_change: float
    ev_change_pct: float
    equity_value_change: float
    equity_value_change_pct: float
    comparison_date: str


# =====================================================================
# PDF UPLOAD AND EXTRACTION ENDPOINTS
# =====================================================================

@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_pdf_document(
    file: UploadFile = File(...),
    document_type: DocumentType = Form(...),
    company_id: Optional[str] = Form(None),
    use_ai: bool = Form(False),
    db: Session = Depends(get_db)
):
    """
    Upload a PDF financial document and extract data

    This endpoint:
    1. Uploads the PDF file
    2. Runs extraction pipeline (pdfplumber or AI-enhanced)
    3. Stores extracted data in database
    4. Returns extraction results

    Args:
        file: PDF file upload
        document_type: Type of document (Quarterly Report, Annual Report, etc.)
        company_id: Optional company UUID
        use_ai: Whether to use AI-enhanced extraction (slower but more accurate)

    Returns:
        Extraction results with document_id and extracted data summary
    """
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    # Save uploaded file temporarily
    upload_dir = "/tmp/pdf_uploads"
    os.makedirs(upload_dir, exist_ok=True)

    file_id = str(uuid.uuid4())
    file_path = os.path.join(upload_dir, f"{file_id}_{file.filename}")

    try:
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract data
        service = get_pdf_service(db)
        result = await service.upload_and_extract(
            file_path=file_path,
            filename=file.filename,
            document_type=document_type,
            company_id=company_id,
            use_ai=use_ai
        )

        return DocumentUploadResponse(**result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")

    finally:
        # Cleanup temporary file
        if os.path.exists(file_path):
            os.remove(file_path)


@router.get("/documents/{document_id}/status")
async def get_document_status(
    document_id: str,
    db: Session = Depends(get_db)
):
    """
    Get extraction status of a document

    Returns current processing status and confidence scores
    """
    service = get_pdf_service(db)
    document = service.get_document(document_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    return {
        'document_id': str(document.id),
        'status': document.extraction_status.value,
        'confidence': document.extraction_confidence,
        'needs_review': document.needs_review,
        'extraction_date': document.extraction_date.isoformat() if document.extraction_date else None,
        'periods_detected': document.periods_detected,
        'statements_found': document.statements_found,
        'errors': document.extraction_errors,
    }


@router.get("/documents/{document_id}/statements", response_model=ExtractedStatements)
async def get_extracted_statements(
    document_id: str,
    db: Session = Depends(get_db)
):
    """
    Get all extracted financial statements from a document

    Returns income statements, balance sheets, and cash flow statements
    """
    service = get_pdf_service(db)
    statements = service.get_extracted_statements(document_id)

    if not statements:
        raise HTTPException(status_code=404, detail="Document not found")

    return ExtractedStatements(**statements)


@router.get("/companies/{company_id}/documents")
async def list_company_documents(
    company_id: str,
    document_type: Optional[DocumentType] = Query(None),
    limit: int = Query(100, le=500),
    db: Session = Depends(get_db)
):
    """
    List all documents for a company

    Args:
        company_id: Company UUID
        document_type: Optional filter by document type
        limit: Maximum number of documents to return

    Returns:
        List of documents with metadata
    """
    service = get_pdf_service(db)
    documents = service.get_company_documents(
        company_id=company_id,
        document_type=document_type,
        limit=limit
    )

    return {
        'company_id': company_id,
        'count': len(documents),
        'documents': [
            {
                'id': str(doc.id),
                'document_name': doc.document_name,
                'document_type': doc.document_type.value,
                'company_name': doc.company_name,
                'extraction_status': doc.extraction_status.value,
                'extraction_confidence': doc.extraction_confidence,
                'upload_date': doc.upload_date.isoformat(),
                'needs_review': doc.needs_review,
                'periods_detected': doc.periods_detected,
                'statements_found': doc.statements_found,
            }
            for doc in documents
        ]
    }


@router.post("/documents/{document_id}/review")
async def mark_document_reviewed(
    document_id: str,
    review_notes: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Mark a document as manually reviewed

    Called after a user has reviewed and potentially corrected extracted data
    """
    service = get_pdf_service(db)
    document = service.get_document(document_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    document.extraction_status = ExtractionStatus.REVIEWED
    document.needs_review = False
    document.review_notes = review_notes

    db.commit()

    return {
        'document_id': str(document.id),
        'status': 'reviewed',
        'review_notes': review_notes
    }


# =====================================================================
# HISTORICAL VALUATION TRACKING ENDPOINTS
# =====================================================================

@router.post("/valuations/snapshots", response_model=ValuationSnapshotResponse)
async def create_valuation_snapshot(
    snapshot: ValuationSnapshotCreate,
    db: Session = Depends(get_db)
):
    """
    Create a historical valuation snapshot

    This saves a point-in-time valuation for future comparison and tracking
    """
    service = get_pdf_service(db)

    snapshot_record = service.create_valuation_snapshot(
        company_id=snapshot.company_id,
        model_type=snapshot.model_type,
        enterprise_value=snapshot.enterprise_value,
        equity_value=snapshot.equity_value,
        dcf_model_id=snapshot.dcf_model_id,
        lbo_model_id=snapshot.lbo_model_id,
        key_assumptions=snapshot.key_assumptions,
    )

    return {
        'id': str(snapshot_record.id),
        'company_id': str(snapshot_record.company_id),
        'model_type': snapshot_record.model_type,
        'enterprise_value': snapshot_record.enterprise_value,
        'equity_value': snapshot_record.equity_value,
        'snapshot_date': snapshot_record.snapshot_date.isoformat(),
        'wacc': snapshot_record.wacc,
        'terminal_growth_rate': snapshot_record.terminal_growth_rate,
        'entry_multiple': snapshot_record.entry_multiple,
        'exit_multiple': snapshot_record.exit_multiple,
        'equity_irr': snapshot_record.equity_irr,
        'moic': snapshot_record.moic,
    }


@router.get("/companies/{company_id}/valuations/history")
async def get_valuation_history(
    company_id: str,
    model_type: Optional[str] = Query(None),
    limit: int = Query(50, le=200),
    db: Session = Depends(get_db)
):
    """
    Get historical valuations for a company

    Returns a timeline of all valuations performed, enabling trend analysis
    """
    service = get_pdf_service(db)
    snapshots = service.get_valuation_history(
        company_id=company_id,
        model_type=model_type,
        limit=limit
    )

    return {
        'company_id': company_id,
        'count': len(snapshots),
        'snapshots': [
            {
                'id': str(snap.id),
                'snapshot_date': snap.snapshot_date.isoformat(),
                'model_type': snap.model_type,
                'enterprise_value': snap.enterprise_value,
                'equity_value': snap.equity_value,
                'equity_value_per_share': snap.equity_value_per_share,
                'implied_ev_ebitda': snap.implied_ev_ebitda,
                'wacc': snap.wacc,
                'terminal_growth_rate': snap.terminal_growth_rate,
                'equity_irr': snap.equity_irr,
                'moic': snap.moic,
            }
            for snap in snapshots
        ]
    }


@router.post("/valuations/compare", response_model=ValuationComparisonResponse)
async def compare_valuations(
    comparison: ValuationComparisonRequest,
    db: Session = Depends(get_db)
):
    """
    Compare two valuation snapshots

    Analyzes what changed between two valuations and quantifies the impact
    of key drivers (revenue, margins, WACC, multiples, etc.)
    """
    service = get_pdf_service(db)

    comparison_record = service.compare_valuations(
        baseline_snapshot_id=comparison.baseline_snapshot_id,
        comparison_snapshot_id=comparison.comparison_snapshot_id
    )

    return {
        'id': str(comparison_record.id),
        'company_id': str(comparison_record.company_id),
        'ev_change': comparison_record.ev_change,
        'ev_change_pct': comparison_record.ev_change_pct,
        'equity_value_change': comparison_record.equity_value_change,
        'equity_value_change_pct': comparison_record.equity_value_change_pct,
        'comparison_date': comparison_record.comparison_date.isoformat(),
    }


@router.get("/valuations/comparisons/{comparison_id}")
async def get_comparison_details(
    comparison_id: str,
    db: Session = Depends(get_db)
):
    """
    Get detailed comparison analysis

    Returns full variance bridge showing which factors drove the change
    """
    from app.models.pdf_documents import ValuationComparison

    comparison = db.query(ValuationComparison).get(uuid.UUID(comparison_id))

    if not comparison:
        raise HTTPException(status_code=404, detail="Comparison not found")

    return {
        'id': str(comparison.id),
        'company_id': str(comparison.company_id),
        'ev_change': comparison.ev_change,
        'ev_change_pct': comparison.ev_change_pct,
        'equity_value_change': comparison.equity_value_change,
        'equity_value_change_pct': comparison.equity_value_change_pct,
        'revenue_impact': comparison.revenue_impact,
        'margin_impact': comparison.margin_impact,
        'wacc_impact': comparison.wacc_impact,
        'terminal_value_impact': comparison.terminal_value_impact,
        'multiple_impact': comparison.multiple_impact,
        'variance_bridge': comparison.variance_bridge,
        'key_changes': comparison.key_changes,
        'commentary': comparison.commentary,
        'comparison_date': comparison.comparison_date.isoformat(),
    }


# Export router
__all__ = ["router"]
