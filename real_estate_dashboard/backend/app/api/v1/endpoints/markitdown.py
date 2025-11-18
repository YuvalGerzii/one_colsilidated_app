"""
MarkItDown API Endpoints

Endpoints for document-to-markdown conversion using MarkItDown.

Supported operations:
- Upload and convert documents (PDF, Office, images, HTML, audio, etc.)
- Retrieve converted markdown content
- List converted documents
- Review and manage conversions
- LLM-enhanced analysis and model integration
"""

import logging
from typing import Optional, List
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from datetime import datetime

logger = logging.getLogger(__name__)

from app.core.database import get_db
from app.services.markitdown_service import MarkItDownService
from app.services.llm_service import llm_service
from app.services.financial_extractor import financial_extractor
from app.models.markitdown_documents import (
    MarkItDownFileType,
    ConversionStatus,
    ConversionMethod
)
from app.models.financial_models import DCFModel, LBOModel

router = APIRouter()


# Pydantic Models

class DocumentConversionRequest(BaseModel):
    """Request model for document conversion"""
    company_id: Optional[str] = Field(None, description="Optional company ID for association")
    use_llm: bool = Field(False, description="Use LLM for enhanced image descriptions")
    project_name: Optional[str] = Field(None, description="Optional project name")


class DocumentConversionResponse(BaseModel):
    """Response model for document conversion"""
    document_id: str
    document_name: str
    file_type: str
    conversion_status: str
    conversion_method: Optional[str]
    conversion_confidence: Optional[float]
    character_count: Optional[int]
    word_count: Optional[int]
    conversion_duration_ms: Optional[int]
    needs_review: bool
    has_errors: bool
    error_message: Optional[str]
    warnings: Optional[List[str]]
    created_at: datetime

    class Config:
        from_attributes = True


class DocumentContentResponse(BaseModel):
    """Response model for document content"""
    document_id: str
    document_name: str
    markdown_text: str
    heading_count: Optional[int]
    table_count: Optional[int]
    image_count: Optional[int]
    link_count: Optional[int]
    code_block_count: Optional[int]


class DocumentListItem(BaseModel):
    """List item for documents"""
    document_id: str
    document_name: str
    file_type: str
    file_size_kb: Optional[int]
    conversion_status: str
    conversion_confidence: Optional[float]
    word_count: Optional[int]
    upload_date: datetime
    needs_review: bool
    company_name: Optional[str]

    class Config:
        from_attributes = True


class ReviewRequest(BaseModel):
    """Request model for reviewing a document"""
    review_notes: Optional[str] = Field(None, description="Optional review notes")


class ConversionStatsResponse(BaseModel):
    """Statistics for conversions"""
    total_documents: int
    completed_conversions: int
    failed_conversions: int
    pending_conversions: int
    needs_review_count: int
    avg_confidence: Optional[float]
    total_words_converted: int
    file_type_distribution: dict


class AnalyzeDocumentRequest(BaseModel):
    """Request model for LLM-enhanced document analysis"""
    analysis_type: str = Field(
        ...,
        description="""Type of analysis: summary, financial_extraction, model_suggestion,
        risk_assessment, valuation_suggestions, sentiment_analysis, competitive_analysis,
        due_diligence, compliance_check, key_metrics_extraction"""
    )
    focus_areas: Optional[List[str]] = Field(None, description="Specific areas to focus on")
    extract_structured_data: bool = Field(False, description="Whether to extract structured financial data")


class AnalyzeDocumentResponse(BaseModel):
    """Response model for document analysis"""
    document_id: str
    document_name: str
    analysis_type: str
    analysis_text: Optional[str]
    structured_data: Optional[dict]
    suggested_model_type: Optional[str]
    confidence: Optional[float]
    llm_available: bool
    extracted_entities: Optional[dict]


class RunInModelRequest(BaseModel):
    """Request model for running extracted data in a financial model"""
    model_type: str = Field(..., description="Type of model: DCF or LBO")
    model_name: Optional[str] = Field(None, description="Name for the new model")
    auto_populate: bool = Field(True, description="Whether to auto-populate fields from extracted data")


class RunInModelResponse(BaseModel):
    """Response model for model creation"""
    success: bool
    model_id: Optional[str]
    model_type: str
    model_name: str
    populated_fields: Optional[List[str]]
    message: str


class AvailableModelsResponse(BaseModel):
    """Response model for available financial models"""
    models: List[dict]


# API Endpoints

@router.post("/convert", response_model=DocumentConversionResponse)
async def convert_document(
    file: UploadFile = File(..., description="Document file to convert"),
    company_id: Optional[str] = Query(None, description="Company ID for association"),
    use_llm: bool = Query(False, description="Use LLM for image descriptions"),
    project_name: Optional[str] = Query(None, description="Project name"),
    db: Session = Depends(get_db)
):
    """
    Convert a document to markdown using MarkItDown.

    Supports multiple file formats:
    - PDF documents
    - Microsoft Office (Word, Excel, PowerPoint)
    - Images (JPG, PNG, GIF, etc.)
    - HTML files
    - Audio files (with transcription)
    - And many more...

    Returns:
        DocumentConversionResponse with conversion results and metadata
    """
    try:
        service = MarkItDownService(db)
        document = await service.convert_document(
            file=file,
            company_id=company_id,
            use_llm=use_llm
        )

        # Update project name if provided
        if project_name:
            document.project_name = project_name
            db.commit()

        return DocumentConversionResponse(
            document_id=str(document.id),
            document_name=document.document_name,
            file_type=document.file_type.value,
            conversion_status=document.conversion_status.value,
            conversion_method=document.conversion_method.value if document.conversion_method else None,
            conversion_confidence=document.conversion_confidence,
            character_count=document.character_count,
            word_count=document.word_count,
            conversion_duration_ms=document.conversion_duration_ms,
            needs_review=document.needs_review,
            has_errors=document.has_errors,
            error_message=document.error_message,
            warnings=document.warnings,
            created_at=document.created_at
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")


@router.get("/documents/{document_id}", response_model=DocumentConversionResponse)
async def get_document(
    document_id: str,
    db: Session = Depends(get_db)
):
    """
    Get document metadata by ID.

    Args:
        document_id: UUID of the document

    Returns:
        DocumentConversionResponse with document metadata
    """
    service = MarkItDownService(db)
    document = service.get_document(document_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    return DocumentConversionResponse(
        document_id=str(document.id),
        document_name=document.document_name,
        file_type=document.file_type.value,
        conversion_status=document.conversion_status.value,
        conversion_method=document.conversion_method.value if document.conversion_method else None,
        conversion_confidence=document.conversion_confidence,
        character_count=document.character_count,
        word_count=document.word_count,
        conversion_duration_ms=document.conversion_duration_ms,
        needs_review=document.needs_review,
        has_errors=document.has_errors,
        error_message=document.error_message,
        warnings=document.warnings,
        created_at=document.created_at
    )


@router.get("/documents/{document_id}/content", response_model=DocumentContentResponse)
async def get_document_content(
    document_id: str,
    db: Session = Depends(get_db)
):
    """
    Get markdown content for a document.

    Args:
        document_id: UUID of the document

    Returns:
        DocumentContentResponse with full markdown text and metrics
    """
    service = MarkItDownService(db)
    document = service.get_document(document_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    markdown_text = service.get_document_content(document_id)

    if not markdown_text:
        raise HTTPException(status_code=404, detail="Document content not found")

    # Get content metrics
    content = document.content

    return DocumentContentResponse(
        document_id=str(document.id),
        document_name=document.document_name,
        markdown_text=markdown_text,
        heading_count=content.heading_count if content else None,
        table_count=content.table_count if content else None,
        image_count=content.image_count if content else None,
        link_count=content.link_count if content else None,
        code_block_count=content.code_block_count if content else None
    )


@router.get("/documents", response_model=List[DocumentListItem])
async def list_documents(
    company_id: Optional[str] = Query(None, description="Filter by company ID"),
    file_type: Optional[MarkItDownFileType] = Query(None, description="Filter by file type"),
    status: Optional[ConversionStatus] = Query(None, description="Filter by status"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """
    List converted documents with optional filtering.

    Query Parameters:
        company_id: Filter by company
        file_type: Filter by file type (PDF, WORD, EXCEL, etc.)
        status: Filter by conversion status
        limit: Maximum results (1-500)

    Returns:
        List of documents with metadata
    """
    service = MarkItDownService(db)
    documents = service.list_documents(
        company_id=company_id,
        file_type=file_type,
        limit=limit
    )

    # Additional status filtering (if needed)
    if status:
        documents = [d for d in documents if d.conversion_status == status]

    return [
        DocumentListItem(
            document_id=str(doc.id),
            document_name=doc.document_name,
            file_type=doc.file_type.value,
            file_size_kb=doc.file_size_kb,
            conversion_status=doc.conversion_status.value,
            conversion_confidence=doc.conversion_confidence,
            word_count=doc.word_count,
            upload_date=doc.upload_date,
            needs_review=doc.needs_review,
            company_name=doc.company_name
        )
        for doc in documents
    ]


@router.post("/documents/{document_id}/review", response_model=DocumentConversionResponse)
async def mark_document_reviewed(
    document_id: str,
    review: ReviewRequest,
    db: Session = Depends(get_db)
):
    """
    Mark a document as reviewed.

    Args:
        document_id: UUID of the document
        review: Review request with optional notes

    Returns:
        Updated document metadata
    """
    service = MarkItDownService(db)

    try:
        # TODO: Get actual user_id from auth
        user_id = "system"

        document = service.mark_reviewed(
            document_id=document_id,
            user_id=user_id,
            review_notes=review.review_notes
        )

        return DocumentConversionResponse(
            document_id=str(document.id),
            document_name=document.document_name,
            file_type=document.file_type.value,
            conversion_status=document.conversion_status.value,
            conversion_method=document.conversion_method.value if document.conversion_method else None,
            conversion_confidence=document.conversion_confidence,
            character_count=document.character_count,
            word_count=document.word_count,
            conversion_duration_ms=document.conversion_duration_ms,
            needs_review=document.needs_review,
            has_errors=document.has_errors,
            error_message=document.error_message,
            warnings=document.warnings,
            created_at=document.created_at
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Review failed: {str(e)}")


@router.get("/stats", response_model=ConversionStatsResponse)
async def get_conversion_stats(
    company_id: Optional[str] = Query(None, description="Filter stats by company"),
    db: Session = Depends(get_db)
):
    """
    Get conversion statistics and analytics.

    Query Parameters:
        company_id: Optional company filter

    Returns:
        Conversion statistics including counts, success rates, and distributions
    """
    from app.models.markitdown_documents import MarkItDownDocument
    from sqlalchemy import func

    query = db.query(MarkItDownDocument)
    if company_id:
        query = query.filter(MarkItDownDocument.company_id == company_id)

    # Total counts
    total_documents = query.count()
    completed = query.filter(MarkItDownDocument.conversion_status == ConversionStatus.COMPLETED).count()
    failed = query.filter(MarkItDownDocument.conversion_status == ConversionStatus.FAILED).count()
    pending = query.filter(MarkItDownDocument.conversion_status == ConversionStatus.PENDING).count()
    needs_review = query.filter(MarkItDownDocument.needs_review == True).count()

    # Average confidence
    avg_confidence_result = query.with_entities(
        func.avg(MarkItDownDocument.conversion_confidence)
    ).filter(
        MarkItDownDocument.conversion_confidence.isnot(None)
    ).scalar()
    avg_confidence = float(avg_confidence_result) if avg_confidence_result else None

    # Total words converted
    total_words_result = query.with_entities(
        func.sum(MarkItDownDocument.word_count)
    ).filter(
        MarkItDownDocument.word_count.isnot(None)
    ).scalar()
    total_words = int(total_words_result) if total_words_result else 0

    # File type distribution
    file_type_counts = db.query(
        MarkItDownDocument.file_type,
        func.count(MarkItDownDocument.id)
    ).group_by(MarkItDownDocument.file_type).all()

    file_type_distribution = {
        file_type.value: count for file_type, count in file_type_counts
    }

    return ConversionStatsResponse(
        total_documents=total_documents,
        completed_conversions=completed,
        failed_conversions=failed,
        pending_conversions=pending,
        needs_review_count=needs_review,
        avg_confidence=avg_confidence,
        total_words_converted=total_words,
        file_type_distribution=file_type_distribution
    )


@router.post("/documents/{document_id}/analyze", response_model=AnalyzeDocumentResponse)
async def analyze_document_with_llm(
    document_id: str,
    request: AnalyzeDocumentRequest,
    db: Session = Depends(get_db)
):
    """
    Analyze a converted document using LLM for intelligent insights.

    **Analysis Types:**

    **Basic Analysis:**
    - `summary`: Generate a concise summary of the document
    - `financial_extraction`: Extract financial data and metrics (revenue, EBITDA, debt, margins)
    - `model_suggestion`: Suggest which financial model to use (DCF/LBO)

    **Advanced Analysis:**
    - `risk_assessment`: Comprehensive risk analysis (financial, operational, market, credit, compliance)
    - `valuation_suggestions`: Recommend valuation methodologies (DCF, Comps, Precedents, LBO)
    - `sentiment_analysis`: Market sentiment and management tone analysis
    - `competitive_analysis`: Competitive positioning and market share analysis
    - `due_diligence`: Full investment due diligence report
    - `compliance_check`: Regulatory compliance and disclosure quality review
    - `key_metrics_extraction`: Extract and organize all financial KPIs and ratios

    **Example:**
    ```json
    {
      "analysis_type": "risk_assessment",
      "focus_areas": ["credit risk", "liquidity", "operational"],
      "extract_structured_data": true
    }
    ```

    **Returns:**
    Analysis results with optional structured data extraction, risk levels, sentiment scores, and recommendations.
    """
    import json

    service = MarkItDownService(db)
    document = service.get_document(document_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Get markdown content
    markdown_text = service.get_document_content(document_id)
    if not markdown_text:
        raise HTTPException(status_code=404, detail="Document content not found")

    # Prepare LLM analysis based on type
    analysis_text = None
    structured_data = None
    suggested_model_type = None
    extracted_entities = None

    if request.analysis_type == "summary":
        system_prompt = "You are a financial document analyst. Provide clear, concise summaries focusing on key information."
        prompt = f"Summarize this document, highlighting key points:\n\n{markdown_text[:3000]}"

        if request.focus_areas:
            prompt += f"\n\nFocus on these areas: {', '.join(request.focus_areas)}"

        result = await llm_service.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.3,
            max_tokens=500
        )

        if result:
            analysis_text = result["text"]

    elif request.analysis_type == "financial_extraction":
        # PRIMARY: Rule-based extraction (works without LLM)
        extracted_data = financial_extractor.extract_from_markdown(markdown_text)

        # Format the rule-based results
        analysis_parts = ["**Financial Data Extraction (Rule-based)**\n"]

        if extracted_data.get('company_name'):
            analysis_parts.append(f"**Company:** {extracted_data['company_name']}")
        if extracted_data.get('ticker'):
            analysis_parts.append(f"**Ticker:** {extracted_data['ticker']}")

        if extracted_data.get('revenue'):
            analysis_parts.append(f"**Revenue:** {', '.join(map(str, extracted_data['revenue']))}")
        if extracted_data.get('ebitda'):
            analysis_parts.append(f"**EBITDA:** {', '.join(map(str, extracted_data['ebitda']))}")
        if extracted_data.get('margins'):
            analysis_parts.append(f"**Margins:** {', '.join(map(str, extracted_data['margins']))}%")
        if extracted_data.get('debt'):
            analysis_parts.append(f"**Debt:** {', '.join(map(str, extracted_data['debt']))}")
        if extracted_data.get('cash'):
            analysis_parts.append(f"**Cash:** {', '.join(map(str, extracted_data['cash']))}")
        if extracted_data.get('valuation'):
            analysis_parts.append(f"**Valuation:** {', '.join(map(str, extracted_data['valuation']))}")
        if extracted_data.get('growth'):
            analysis_parts.append(f"**Growth Rate:** {', '.join(map(str, extracted_data['growth']))}%")

        analysis_parts.append(f"\n**Metrics Found:** {extracted_data['metrics_found']}/7")
        analysis_parts.append(f"**Extraction Confidence:** {extracted_data['confidence']:.2%}")

        analysis_text = "\n".join(analysis_parts)
        structured_data = extracted_data if request.extract_structured_data else None

        # ENHANCEMENT: Use LLM to enhance/validate if available
        llm_result = await llm_service.generate(
            prompt=f"""Enhance and validate this extracted financial data:

{analysis_text}

Original document excerpt:
{markdown_text[:2000]}

Provide additional insights or corrections.""",
            system_prompt="You are a financial data extraction expert. Enhance and validate extracted data.",
            temperature=0.2,
            max_tokens=400
        )

        if llm_result:
            analysis_text += f"\n\n**LLM Enhancement:**\n{llm_result['text']}"

    elif request.analysis_type == "model_suggestion":
        system_prompt = """You are a financial modeling expert. Analyze documents and suggest whether a DCF or LBO model is most appropriate.
- DCF: Best for valuing operating companies, growth companies, public companies
- LBO: Best for leveraged buyouts, private equity deals, highly leveraged transactions"""

        prompt = f"""Analyze this document and suggest which financial model is most appropriate (DCF or LBO):

{markdown_text[:3000]}

Explain your reasoning and identify key factors that influenced your recommendation."""

        result = await llm_service.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.4,
            max_tokens=400
        )

        if result:
            analysis_text = result["text"]

            # Try to extract suggested model type
            text_lower = result["text"].lower()
            if "lbo" in text_lower and text_lower.index("lbo") < text_lower.index("dcf") if "dcf" in text_lower else True:
                suggested_model_type = "LBO"
            elif "dcf" in text_lower:
                suggested_model_type = "DCF"

    elif request.analysis_type == "risk_assessment":
        # PRIMARY: Rule-based risk assessment (works without LLM)
        risk_data = financial_extractor.assess_risk_factors(markdown_text)

        # Format the rule-based results
        analysis_text = f"""**Risk Assessment (Rule-based)**

**Risk Level:** {risk_data['risk_level']}
**Risk Score:** {risk_data['risk_score']:.1f}/10

**Risk Indicators:**
- High-risk indicators: {risk_data['high_risk_indicators']}
- Medium-risk indicators: {risk_data['medium_risk_indicators']}

**Risk Category Mentions:**
- Financial Risk: {risk_data['financial_risk_mentions']} mentions
- Operational Risk: {risk_data['operational_risk_mentions']} mentions
- Market Risk: {risk_data['market_risk_mentions']} mentions

**Total Risk Mentions:** {risk_data['total_risk_mentions']}
"""

        structured_data = risk_data

        # ENHANCEMENT: Use LLM for detailed risk analysis if available
        llm_result = await llm_service.generate(
            prompt=f"""Enhance this rule-based risk assessment with detailed insights:

{analysis_text}

Document excerpt:
{markdown_text[:3000]}

Provide:
1. Specific red flags identified
2. Risk mitigation recommendations
3. Additional risk factors not captured by keywords""",
            system_prompt="You are a financial risk analyst. Provide detailed risk insights.",
            temperature=0.3,
            max_tokens=500
        )

        if llm_result:
            analysis_text += f"\n\n**LLM Enhancement:**\n{llm_result['text']}"

    elif request.analysis_type == "valuation_suggestions":
        system_prompt = """You are a valuation expert with deep knowledge of DCF, LBO, comparable companies, and precedent transactions.
Recommend appropriate valuation methodologies and provide valuation insights."""

        prompt = f"""Analyze this document and provide valuation recommendations:

{markdown_text[:4000]}

Provide:
1. Recommended Valuation Methodologies (DCF, Comparable Companies, Precedent Transactions, LBO)
2. Justification for each methodology
3. Key Value Drivers identified
4. Estimated Valuation Range (if data available)
5. Comparable Companies or Transactions (if mentioned)
6. Critical Assumptions to validate"""

        result = await llm_service.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.3,
            max_tokens=700
        )

        if result:
            analysis_text = result["text"]

    elif request.analysis_type == "sentiment_analysis":
        # PRIMARY: Rule-based sentiment analysis (works without LLM)
        sentiment_data = financial_extractor.analyze_sentiment(markdown_text)

        # Format the rule-based results
        analysis_text = f"""**Sentiment Analysis (Rule-based)**

**Overall Sentiment:** {sentiment_data['sentiment']}
**Sentiment Score:** {sentiment_data['sentiment_score']:.1f}/10

**Sentiment Indicators:**
- Positive indicators: {sentiment_data['positive_indicators']} occurrences
- Negative indicators: {sentiment_data['negative_indicators']} occurrences
- Net sentiment: {sentiment_data['net_sentiment']:+d}

**Interpretation:**
"""
        if sentiment_data['sentiment'] == "Bullish":
            analysis_text += "Document shows positive outlook with optimistic language and growth indicators."
        elif sentiment_data['sentiment'] == "Bearish":
            analysis_text += "Document shows concerning outlook with negative language and risk indicators."
        else:
            analysis_text += "Document shows balanced outlook with mixed positive and negative indicators."

        structured_data = sentiment_data

        # ENHANCEMENT: Use LLM for nuanced sentiment analysis if available
        llm_result = await llm_service.generate(
            prompt=f"""Enhance this rule-based sentiment analysis:

{analysis_text}

Document excerpt:
{markdown_text[:3000]}

Provide:
1. Management tone assessment
2. Market outlook interpretation
3. Forward-looking statement analysis
4. Qualitative insights beyond keyword counting""",
            system_prompt="You are a market sentiment analyst. Provide nuanced sentiment insights.",
            temperature=0.4,
            max_tokens=400
        )

        if llm_result:
            analysis_text += f"\n\n**LLM Enhancement:**\n{llm_result['text']}"

    elif request.analysis_type == "competitive_analysis":
        system_prompt = """You are a competitive strategy analyst with expertise in market positioning and competitive intelligence.
Analyze documents for competitive positioning, market share, and strategic advantages."""

        prompt = f"""Analyze the competitive positioning in this document:

{markdown_text[:4000]}

Provide:
1. Competitive Strengths
2. Competitive Weaknesses
3. Market Position (Leader/Challenger/Follower)
4. Key Competitors Mentioned
5. Competitive Advantages (Moats)
6. Threats from Competition
7. Market Share Insights (if available)
8. Strategic Recommendations"""

        result = await llm_service.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.4,
            max_tokens=700
        )

        if result:
            analysis_text = result["text"]

    elif request.analysis_type == "due_diligence":
        system_prompt = """You are an investment due diligence professional with experience in M&A and private equity.
Conduct a comprehensive due diligence review of financial and business documents."""

        prompt = f"""Conduct an investment due diligence analysis of this document:

{markdown_text[:4000]}

Provide a structured due diligence report covering:
1. Executive Summary
2. Business Overview & Model
3. Financial Health Assessment
4. Key Strengths (Investment Highlights)
5. Key Concerns (Red Flags)
6. Management Quality Indicators
7. Market & Industry Position
8. Valuation Considerations
9. Deal Risks
10. Recommendation (Pass/Further Review/Proceed)"""

        result = await llm_service.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.3,
            max_tokens=900
        )

        if result:
            analysis_text = result["text"]

    elif request.analysis_type == "compliance_check":
        system_prompt = """You are a regulatory compliance expert specializing in financial regulations and reporting standards.
Review documents for compliance issues, regulatory risks, and disclosure quality."""

        prompt = f"""Review this document for compliance and regulatory considerations:

{markdown_text[:4000]}

Provide:
1. Compliance Status (Compliant/Issues Identified/Needs Review)
2. Regulatory Framework (GAAP, IFRS, SEC, etc.)
3. Disclosure Quality Assessment
4. Potential Compliance Risks
5. Missing Required Disclosures
6. Audit Opinion (if financial statements)
7. Recommendations for Compliance Improvements"""

        result = await llm_service.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.2,
            max_tokens=600
        )

        if result:
            analysis_text = result["text"]

    elif request.analysis_type == "key_metrics_extraction":
        system_prompt = """You are a financial metrics analyst. Extract and organize key performance indicators (KPIs) from documents.
Focus on financial ratios, growth metrics, profitability, and efficiency indicators."""

        prompt = f"""Extract all key financial metrics and KPIs from this document:

{markdown_text[:4000]}

Organize metrics by category:
1. Growth Metrics (Revenue growth, User growth, etc.)
2. Profitability Metrics (Gross margin, EBITDA margin, Net margin, ROE, ROA)
3. Efficiency Metrics (Asset turnover, Inventory turnover, etc.)
4. Liquidity Metrics (Current ratio, Quick ratio, Cash ratio)
5. Leverage Metrics (Debt/Equity, Debt/EBITDA, Interest coverage)
6. Valuation Metrics (P/E, EV/EBITDA, EV/Revenue, P/B)
7. Per-Share Metrics (EPS, Book value per share, FCF per share)

Provide values and trends (increasing/decreasing/stable)."""

        if request.extract_structured_data:
            prompt += "\n\nProvide data in JSON format with metric categories as keys."

        result = await llm_service.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.1,
            max_tokens=800
        )

        if result:
            analysis_text = result["text"]

            # Try to extract structured metrics
            if request.extract_structured_data:
                try:
                    text = result["text"].strip()
                    if "```json" in text:
                        json_start = text.index("```json") + 7
                        json_end = text.index("```", json_start)
                        json_text = text[json_start:json_end].strip()
                        structured_data = json.loads(json_text)
                    elif "{" in text and "}" in text:
                        json_start = text.index("{")
                        json_end = text.rindex("}") + 1
                        json_text = text[json_start:json_end]
                        structured_data = json.loads(json_text)
                except:
                    pass

    # Extract entities (basic extraction)
    if markdown_text:
        extracted_entities = {
            "has_tables": "table" in markdown_text.lower() or "|" in markdown_text,
            "has_financial_terms": any(term in markdown_text.lower() for term in ["revenue", "ebitda", "ebit", "cash flow", "debt", "equity"]),
            "has_dates": any(str(year) in markdown_text for year in range(2015, 2030)),
            "has_percentages": "%" in markdown_text,
            "has_currency": "$" in markdown_text or "usd" in markdown_text.lower()
        }

    return AnalyzeDocumentResponse(
        document_id=str(document.id),
        document_name=document.document_name,
        analysis_type=request.analysis_type,
        analysis_text=analysis_text,
        structured_data=structured_data,
        suggested_model_type=suggested_model_type,
        confidence=document.conversion_confidence,
        llm_available=analysis_text is not None,
        extracted_entities=extracted_entities
    )


@router.get("/documents/{document_id}/available-models", response_model=AvailableModelsResponse)
async def get_available_models(
    document_id: str,
    db: Session = Depends(get_db)
):
    """
    Get list of available financial models that can be created from this document.

    Returns:
        List of available model types (DCF, LBO) with descriptions
    """
    service = MarkItDownService(db)
    document = service.get_document(document_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    models = [
        {
            "model_type": "DCF",
            "name": "Discounted Cash Flow Model",
            "description": "Value operating companies using projected cash flows",
            "suitable_for": ["Public companies", "Growth companies", "Operating businesses"],
            "key_inputs": ["Revenue projections", "EBITDA margins", "WACC", "Terminal growth rate"]
        },
        {
            "model_type": "LBO",
            "name": "Leveraged Buyout Model",
            "description": "Analyze PE deals and leveraged transactions",
            "suitable_for": ["Private equity deals", "Leveraged acquisitions", "Sponsor-backed transactions"],
            "key_inputs": ["Purchase price", "Debt structure", "EBITDA", "Exit multiple"]
        }
    ]

    return AvailableModelsResponse(models=models)


@router.post("/documents/{document_id}/run-in-model", response_model=RunInModelResponse)
async def run_document_in_model(
    document_id: str,
    request: RunInModelRequest,
    db: Session = Depends(get_db)
):
    """
    Create a new financial model and populate it with extracted data from the document.

    **Supported Model Types:**
    - `DCF`: Discounted Cash Flow model
    - `LBO`: Leveraged Buyout model

    **Example:**
    ```json
    {
      "model_type": "DCF",
      "model_name": "ACME Corp Valuation",
      "auto_populate": true
    }
    ```

    **Returns:**
    Created model details with populated fields
    """
    import json
    import uuid
    from datetime import datetime

    service = MarkItDownService(db)
    document = service.get_document(document_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Get markdown content
    markdown_text = service.get_document_content(document_id)
    if not markdown_text:
        raise HTTPException(status_code=404, detail="Document content not found")

    model_name = request.model_name or f"{document.document_name} - {request.model_type} Model"
    populated_fields = []

    # Extract structured data - PRIMARY: Rule-based, ENHANCEMENT: LLM
    structured_data = {}

    if request.auto_populate:
        # PRIMARY: Rule-based extraction (works without LLM)
        if request.model_type == "DCF":
            logger.info("Extracting DCF data using rule-based method")
            rule_based_data = financial_extractor.extract_for_dcf_model(markdown_text)

            # Convert to structured format with proper field names
            structured_data = {
                "company_name": rule_based_data.get("company_name"),
                "ticker": rule_based_data.get("ticker"),
                "current_stock_price": None,  # Not extracted by rules
                "shares_outstanding": None,  # Not extracted by rules
                "revenue_current": float(rule_based_data["revenue"].replace(",", "")) if rule_based_data.get("revenue") else None,
                "revenue_growth_rate": float(rule_based_data["revenue_growth_rate"].replace(",", "")) if rule_based_data.get("revenue_growth_rate") else None,
                "ebitda_margin": float(rule_based_data["ebitda_margin"].replace(",", "")) if rule_based_data.get("ebitda_margin") else None,
                "tax_rate": float(rule_based_data["tax_rate"].replace(",", "")) if rule_based_data.get("tax_rate") else None,
                "terminal_growth_rate": float(rule_based_data["terminal_growth_rate"].replace(",", "")) if rule_based_data.get("terminal_growth_rate") else None,
                "cash": float(rule_based_data["cash"].replace(",", "")) if rule_based_data.get("cash") else None,
                "total_debt": float(rule_based_data["total_debt"].replace(",", "")) if rule_based_data.get("total_debt") else None,
                "beta": float(rule_based_data["beta"]) if rule_based_data.get("beta") else None,
                "risk_free_rate": None,  # Not extracted by rules
            }

            logger.info(f"Rule-based extraction found {sum(1 for v in structured_data.values() if v is not None)} fields")

        else:  # LBO
            logger.info("Extracting LBO data using rule-based method")
            rule_based_data = financial_extractor.extract_for_lbo_model(markdown_text)

            structured_data = {
                "company_name": rule_based_data.get("company_name"),
                "industry": None,  # Not extracted by rules
                "ltm_revenue": float(rule_based_data["ltm_revenue"].replace(",", "")) if rule_based_data.get("ltm_revenue") else None,
                "ltm_ebitda": float(rule_based_data["ltm_ebitda"].replace(",", "")) if rule_based_data.get("ltm_ebitda") else None,
                "purchase_price": float(rule_based_data["purchase_price"].replace(",", "")) if rule_based_data.get("purchase_price") else None,
                "entry_ev_ebitda_multiple": float(rule_based_data["entry_ev_ebitda_multiple"]) if rule_based_data.get("entry_ev_ebitda_multiple") else None,
                "exit_ev_ebitda_multiple": float(rule_based_data["exit_ev_ebitda_multiple"]) if rule_based_data.get("exit_ev_ebitda_multiple") else None,
                "total_leverage": float(rule_based_data["total_leverage"]) if rule_based_data.get("total_leverage") else None,
                "holding_period": int(rule_based_data["holding_period"]) if rule_based_data.get("holding_period") else None,
            }

            logger.info(f"Rule-based extraction found {sum(1 for v in structured_data.values() if v is not None)} fields")

        # ENHANCEMENT: Use LLM to fill gaps and enhance if available
        llm_prompt = ""
        if request.model_type == "DCF":
            llm_prompt = f"""Enhance this DCF model data extraction. Fill missing fields if found in document:

Rule-based extraction: {json.dumps(structured_data, indent=2)}

Document:
{markdown_text[:4000]}

Provide enhanced JSON with fields: company_name, ticker, current_stock_price, shares_outstanding, revenue_current, revenue_growth_rate, ebitda_margin, tax_rate, terminal_growth_rate, cash, total_debt, beta, risk_free_rate"""
        else:
            llm_prompt = f"""Enhance this LBO model data extraction. Fill missing fields if found in document:

Rule-based extraction: {json.dumps(structured_data, indent=2)}

Document:
{markdown_text[:4000]}

Provide enhanced JSON with fields: company_name, industry, ltm_revenue, ltm_ebitda, purchase_price, entry_ev_ebitda_multiple, exit_ev_ebitda_multiple, total_leverage, holding_period"""

        llm_result = await llm_service.generate(
            prompt=llm_prompt,
            system_prompt=f"You are a financial data extraction expert. Enhance rule-based extraction for {request.model_type} model.",
            temperature=0.1,
            max_tokens=800
        )

        if llm_result:
            try:
                # Extract JSON from LLM response
                text = llm_result["text"].strip()
                if "```json" in text:
                    json_start = text.index("```json") + 7
                    json_end = text.index("```", json_start)
                    json_text = text[json_start:json_end].strip()
                    llm_data = json.loads(json_text)
                elif "{" in text and "}" in text:
                    json_start = text.index("{")
                    json_end = text.rindex("}") + 1
                    json_text = text[json_start:json_end]
                    llm_data = json.loads(json_text)
                else:
                    llm_data = {}

                # Merge LLM enhancements (prefer LLM data if rule-based is None)
                for key, value in llm_data.items():
                    if key in structured_data and structured_data[key] is None and value is not None:
                        structured_data[key] = value
                        logger.info(f"LLM enhanced field: {key} = {value}")

            except Exception as e:
                logger.warning(f"Failed to parse LLM enhancement: {e}")

    # Create the financial model
    try:
        if request.model_type == "DCF":
            model = DCFModel(
                id=uuid.uuid4(),
                name=model_name,
                company_name=structured_data.get("company_name"),
                ticker=structured_data.get("ticker"),
                description=f"Auto-generated from {document.document_name}",
                current_stock_price=structured_data.get("current_stock_price"),
                shares_outstanding=structured_data.get("shares_outstanding"),
                risk_free_rate=structured_data.get("risk_free_rate"),
                beta=structured_data.get("beta"),
                tax_rate=structured_data.get("tax_rate"),
                terminal_growth_rate=structured_data.get("terminal_growth_rate"),
                cash=structured_data.get("cash"),
                total_debt=structured_data.get("total_debt"),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            # Add revenue projections if available
            if structured_data.get("revenue_current") and structured_data.get("revenue_growth_rate"):
                revenue = structured_data["revenue_current"]
                growth = structured_data["revenue_growth_rate"] / 100
                model.revenue_projections = {
                    "year_1": revenue * (1 + growth),
                    "year_2": revenue * (1 + growth) ** 2,
                    "year_3": revenue * (1 + growth) ** 3,
                    "year_4": revenue * (1 + growth) ** 4,
                    "year_5": revenue * (1 + growth) ** 5,
                }

            # EBITDA margins
            if structured_data.get("ebitda_margin"):
                margin = structured_data["ebitda_margin"]
                model.ebitda_margins = {
                    "year_1": margin,
                    "year_2": margin,
                    "year_3": margin,
                    "year_4": margin,
                    "year_5": margin,
                }

            db.add(model)
            db.commit()
            db.refresh(model)

            populated_fields = [k for k, v in structured_data.items() if v is not None]

            extraction_method = "rule-based extraction"
            if llm_result:
                extraction_method = "rule-based extraction enhanced with LLM"

            return RunInModelResponse(
                success=True,
                model_id=str(model.id),
                model_type="DCF",
                model_name=model.name,
                populated_fields=populated_fields,
                message=f"DCF model created successfully with {len(populated_fields)} populated fields using {extraction_method}"
            )

        elif request.model_type == "LBO":
            model = LBOModel(
                id=uuid.uuid4(),
                name=model_name,
                company_name=structured_data.get("company_name"),
                industry=structured_data.get("industry"),
                description=f"Auto-generated from {document.document_name}",
                ltm_revenue=structured_data.get("ltm_revenue"),
                ltm_ebitda=structured_data.get("ltm_ebitda"),
                purchase_price=structured_data.get("purchase_price"),
                entry_ev_ebitda_multiple=structured_data.get("entry_ev_ebitda_multiple"),
                exit_ev_ebitda_multiple=structured_data.get("exit_ev_ebitda_multiple"),
                total_leverage=structured_data.get("total_leverage"),
                holding_period=structured_data.get("holding_period"),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            db.add(model)
            db.commit()
            db.refresh(model)

            populated_fields = [k for k, v in structured_data.items() if v is not None]

            extraction_method = "rule-based extraction"
            if llm_result:
                extraction_method = "rule-based extraction enhanced with LLM"

            return RunInModelResponse(
                success=True,
                model_id=str(model.id),
                model_type="LBO",
                model_name=model.name,
                populated_fields=populated_fields,
                message=f"LBO model created successfully with {len(populated_fields)} populated fields using {extraction_method}"
            )

        else:
            raise HTTPException(status_code=400, detail=f"Unsupported model type: {request.model_type}")

    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create model: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Model creation failed: {str(e)}")


@router.delete("/documents/{document_id}")
async def delete_document(
    document_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a document and its content.

    Args:
        document_id: UUID of the document

    Returns:
        Success message
    """
    service = MarkItDownService(db)
    document = service.get_document(document_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    try:
        db.delete(document)
        db.commit()
        return {"message": "Document deleted successfully", "document_id": document_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")
