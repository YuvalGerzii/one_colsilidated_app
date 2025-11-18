"""Report generation endpoints for professional investment reports."""

from datetime import date, datetime
from typing import List, Optional, Dict, Any
from uuid import UUID
import tempfile
import os

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
import io

from app.core.database import get_db
from app.core.auth import get_current_user_with_company
from app.models.user import User
from app.models.company import Company
from app.models.reports import GeneratedReport, ReportType, ReportStatus, ExportFormat
from app.services.report_generator_service import ReportGeneratorService
from app.core.document_generator import PDFGenerator, PowerPointGenerator


router = APIRouter()


# ===== Pydantic Schemas =====

class ReportGenerateRequest(BaseModel):
    """Request to generate a report."""
    report_type: ReportType
    report_name: str
    deal_id: Optional[UUID] = None
    fund_id: Optional[UUID] = None
    market: Optional[str] = None
    property_type: Optional[str] = None
    quarter: Optional[int] = None
    year: Optional[int] = None
    include_charts: bool = True
    include_appendix: bool = True


class ReportExportRequest(BaseModel):
    """Request to export a report."""
    export_format: ExportFormat
    include_charts: bool = True


class ReportResponse(BaseModel):
    """Response for report generation."""
    id: UUID
    report_type: str
    report_name: str
    status: str
    data: Optional[Dict[str, Any]] = None
    generated_at: Optional[datetime] = None
    error_message: Optional[str] = None

    class Config:
        from_attributes = True


# ===== Endpoints =====

@router.post("/generate", response_model=ReportResponse)
async def generate_report(
    request: ReportGenerateRequest,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> ReportResponse:
    """
    Generate a professional investment report.

    Supports:
    - Investment Committee Memos
    - Quarterly Portfolio Reports
    - Market Research Reports
    - Due Diligence Summary Reports
    """
    current_user, company = user_company

    try:
        # Create report record
        report = GeneratedReport(
            company_id=company.id if company else None,
            report_type=request.report_type,
            report_name=request.report_name,
            status=ReportStatus.GENERATING,
            deal_id=request.deal_id,
            fund_id=request.fund_id,
            include_charts=request.include_charts,
            include_appendix=request.include_appendix
        )
        db.add(report)
        db.commit()
        db.refresh(report)

        # Initialize report generator service
        company_id_str = str(company.id) if company else None
        generator = ReportGeneratorService(db, company_id_str)

        # Generate report based on type
        report_data = None

        if request.report_type == ReportType.INVESTMENT_COMMITTEE_MEMO:
            if not request.deal_id:
                raise HTTPException(status_code=400, detail="deal_id required for Investment Committee Memo")
            report_data = generator.generate_investment_committee_memo(
                str(request.deal_id),
                include_charts=request.include_charts
            )

        elif request.report_type == ReportType.QUARTERLY_PORTFOLIO:
            report_data = generator.generate_quarterly_portfolio_report(
                fund_id=str(request.fund_id) if request.fund_id else None,
                quarter=request.quarter,
                year=request.year,
                include_charts=request.include_charts
            )

        elif request.report_type == ReportType.MARKET_RESEARCH:
            if not request.market:
                raise HTTPException(status_code=400, detail="market required for Market Research Report")
            report_data = generator.generate_market_research_report(
                market=request.market,
                property_type=request.property_type,
                include_charts=request.include_charts
            )

        elif request.report_type == ReportType.DUE_DILIGENCE_SUMMARY:
            if not request.deal_id:
                raise HTTPException(status_code=400, detail="deal_id required for Due Diligence Report")
            report_data = generator.generate_due_diligence_report(
                str(request.deal_id),
                include_charts=request.include_charts
            )

        else:
            raise HTTPException(status_code=400, detail=f"Unsupported report type: {request.report_type}")

        # Update report with generated data
        report.report_data = report_data["data"]
        report.status = ReportStatus.COMPLETED
        report.generated_at = datetime.utcnow()

        db.commit()
        db.refresh(report)

        return ReportResponse(
            id=report.id,
            report_type=report.report_type.value,
            report_name=report.report_name,
            status=report.status.value,
            data=report.report_data,
            generated_at=report.generated_at
        )

    except Exception as e:
        # Update report status to failed
        if 'report' in locals():
            report.status = ReportStatus.FAILED
            report.error_message = str(e)
            db.commit()

        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")


@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(
    report_id: UUID,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> ReportResponse:
    """Get a generated report by ID."""
    current_user, company = user_company

    filters = [GeneratedReport.id == report_id]

    if company:
        filters.append(GeneratedReport.company_id == company.id)

    report = db.query(GeneratedReport).filter(*filters).first()

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    return ReportResponse(
        id=report.id,
        report_type=report.report_type.value,
        report_name=report.report_name,
        status=report.status.value,
        data=report.report_data,
        generated_at=report.generated_at,
        error_message=report.error_message
    )


@router.get("/", response_model=List[ReportResponse])
async def list_reports(
    report_type: Optional[ReportType] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> List[ReportResponse]:
    """List all generated reports."""
    current_user, company = user_company

    query = db.query(GeneratedReport)

    # Filter by company_id if user has a company
    if company:
        query = query.filter(GeneratedReport.company_id == company.id)

    if report_type:
        query = query.filter(GeneratedReport.report_type == report_type)

    reports = query.order_by(GeneratedReport.created_at.desc()).offset(skip).limit(limit).all()

    return [
        ReportResponse(
            id=report.id,
            report_type=report.report_type.value,
            report_name=report.report_name,
            status=report.status.value,
            data=None,  # Don't return full data in list
            generated_at=report.generated_at,
            error_message=report.error_message
        )
        for report in reports
    ]


@router.post("/{report_id}/export/pdf")
async def export_report_pdf(
    report_id: UUID,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """Export report as PDF."""
    current_user, company = user_company

    # Fetch report
    filters = [GeneratedReport.id == report_id]

    if company:
        filters.append(GeneratedReport.company_id == company.id)

    report = db.query(GeneratedReport).filter(*filters).first()

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    if report.status != ReportStatus.COMPLETED:
        raise HTTPException(status_code=400, detail="Report generation not completed")

    try:
        # Re-generate report to get sections
        company_id_str = str(company.id) if company else None
        generator = ReportGeneratorService(db, company_id_str)

        sections = []
        if report.report_type == ReportType.INVESTMENT_COMMITTEE_MEMO:
            result = generator.generate_investment_committee_memo(
                str(report.deal_id),
                include_charts=report.include_charts
            )
            sections = result["sections"]

        elif report.report_type == ReportType.QUARTERLY_PORTFOLIO:
            result = generator.generate_quarterly_portfolio_report(
                fund_id=str(report.fund_id) if report.fund_id else None,
                include_charts=report.include_charts
            )
            sections = result["sections"]

        elif report.report_type == ReportType.MARKET_RESEARCH:
            # Extract market from report_data
            market = report.report_data.get("market", "Unknown")
            result = generator.generate_market_research_report(
                market=market,
                include_charts=report.include_charts
            )
            sections = result["sections"]

        elif report.report_type == ReportType.DUE_DILIGENCE_SUMMARY:
            result = generator.generate_due_diligence_report(
                str(report.deal_id),
                include_charts=report.include_charts
            )
            sections = result["sections"]

        # Generate PDF
        pdf_gen = PDFGenerator(title=report.report_name)
        pdf_bytes = pdf_gen.generate(sections)

        # Return PDF as streaming response
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={report.report_name.replace(' ', '_')}.pdf"
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF export failed: {str(e)}")


@router.post("/{report_id}/export/powerpoint")
async def export_report_powerpoint(
    report_id: UUID,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """Export report as PowerPoint presentation."""
    current_user, company = user_company

    # Fetch report
    filters = [GeneratedReport.id == report_id]

    if company:
        filters.append(GeneratedReport.company_id == company.id)

    report = db.query(GeneratedReport).filter(*filters).first()

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    if report.status != ReportStatus.COMPLETED:
        raise HTTPException(status_code=400, detail="Report generation not completed")

    try:
        # Create PowerPoint presentation
        ppt_gen = PowerPointGenerator(
            title=report.report_name,
            subtitle=f"Generated on {datetime.now().strftime('%B %d, %Y')}"
        )

        # Add title slide
        ppt_gen.add_title_slide()

        # Add content based on report type
        report_data = report.report_data

        if report.report_type == ReportType.INVESTMENT_COMMITTEE_MEMO:
            # Executive Summary slide
            exec_sum = report_data.get("executive_summary", {})
            ppt_gen.add_content_slide(
                title="Executive Summary",
                content=[
                    f"Property: {exec_sum.get('property_name', 'N/A')}",
                    f"Type: {exec_sum.get('property_type', 'N/A')}",
                    f"Location: {exec_sum.get('location', 'N/A')}",
                    f"Asking Price: ${exec_sum.get('asking_price', 0):,.0f}",
                    f"Cap Rate: {exec_sum.get('cap_rate', 0):.2f}%",
                    f"IRR Target: {exec_sum.get('irr_target', 0):.2f}%"
                ]
            )

            # Investment Overview slide
            inv_overview = report_data.get("investment_overview", {})
            metrics = inv_overview.get("key_metrics", {})
            ppt_gen.add_content_slide(
                title="Key Metrics",
                table_data=[
                    ["Metric", "Value"],
                    ["Cap Rate", f"{metrics.get('cap_rate', 0):.2f}%" if metrics.get('cap_rate') else "N/A"],
                    ["NOI", f"${metrics.get('noi', 0):,.0f}" if metrics.get('noi') else "N/A"],
                    ["IRR Target", f"{metrics.get('irr_target', 0):.2f}%" if metrics.get('irr_target') else "N/A"],
                ]
            )

            # Recommendation slide
            rec = report_data.get("recommendation", {})
            ppt_gen.add_content_slide(
                title="Recommendation",
                content=[
                    f"Recommendation: {rec.get('recommendation', 'N/A')}",
                    f"Confidence Level: {rec.get('confidence', 0)}%",
                    f"Vote Requested: {rec.get('vote_requested', 'N/A')}"
                ]
            )

        elif report.report_type == ReportType.QUARTERLY_PORTFOLIO:
            # Fund performance slides
            funds = report_data.get("funds", [])
            for fund_data in funds:
                ppt_gen.add_content_slide(
                    title=fund_data.get("fund_name", "Fund Performance"),
                    table_data=[
                        ["Metric", "Value"],
                        ["Fund Type", fund_data.get("fund_type", "N/A")],
                        ["Total Commitments", f"${fund_data.get('total_commitments', 0):,.0f}"],
                        ["Total Invested", f"${fund_data.get('total_invested', 0):,.0f}"],
                        ["Current Value", f"${fund_data.get('current_value', 0):,.0f}"],
                        ["Unrealized Gain/Loss", f"${fund_data.get('unrealized_gain', 0):,.0f}"],
                    ]
                )

        # Generate PowerPoint bytes
        ppt_bytes = ppt_gen.to_bytes()

        # Return PowerPoint as streaming response
        return StreamingResponse(
            io.BytesIO(ppt_bytes),
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            headers={
                "Content-Disposition": f"attachment; filename={report.report_name.replace(' ', '_')}.pptx"
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PowerPoint export failed: {str(e)}")


@router.delete("/{report_id}")
async def delete_report(
    report_id: UUID,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """Delete a generated report."""
    current_user, company = user_company

    filters = [GeneratedReport.id == report_id]

    if company:
        filters.append(GeneratedReport.company_id == company.id)

    report = db.query(GeneratedReport).filter(*filters).first()

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    db.delete(report)
    db.commit()

    return {"success": True, "message": "Report deleted successfully"}


# ===== Quick Generate Endpoints =====

@router.post("/quick/investment-memo/{deal_id}")
async def quick_generate_investment_memo(
    deal_id: UUID,
    export_format: ExportFormat = Query(ExportFormat.PDF),
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """
    Quick generate and export Investment Committee Memo.

    Returns the PDF/PowerPoint directly without saving to database.
    """
    current_user, company = user_company

    try:
        company_id_str = str(company.id) if company else None
        generator = ReportGeneratorService(db, company_id_str)
        result = generator.generate_investment_committee_memo(
            str(deal_id),
            include_charts=True
        )

        if export_format == ExportFormat.PDF:
            pdf_gen = PDFGenerator(title=f"Investment Memo - {result['data']['deal_name']}")
            pdf_bytes = pdf_gen.generate(result["sections"])

            return StreamingResponse(
                io.BytesIO(pdf_bytes),
                media_type="application/pdf",
                headers={
                    "Content-Disposition": f"attachment; filename=Investment_Memo_{deal_id}.pdf"
                }
            )

        elif export_format == ExportFormat.POWERPOINT:
            ppt_gen = PowerPointGenerator(
                title=f"Investment Memo - {result['data']['deal_name']}",
                subtitle=datetime.now().strftime("%B %d, %Y")
            )
            ppt_gen.add_title_slide()

            # Add key slides
            exec_sum = result['data'].get("executive_summary", {})
            ppt_gen.add_content_slide(
                title="Executive Summary",
                content=[
                    f"Property: {exec_sum.get('property_name', 'N/A')}",
                    f"Price: ${exec_sum.get('asking_price', 0):,.0f}",
                    f"Cap Rate: {exec_sum.get('cap_rate', 0):.2f}%"
                ]
            )

            ppt_bytes = ppt_gen.to_bytes()

            return StreamingResponse(
                io.BytesIO(ppt_bytes),
                media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                headers={
                    "Content-Disposition": f"attachment; filename=Investment_Memo_{deal_id}.pptx"
                }
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")
