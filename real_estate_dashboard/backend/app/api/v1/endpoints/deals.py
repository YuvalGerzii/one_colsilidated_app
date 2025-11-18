"""
Deals API Endpoints - Multi-type transaction management

Supports: Real Estate, Company Acquisitions, Shares, Commodities, Debt
"""

from typing import List, Optional
from uuid import UUID
from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from app.api.deps import get_db
from app.models.deal import Deal, DealType, DealStage, DealStatus


router = APIRouter()


# Pydantic Schemas

class DealBase(BaseModel):
    """Base deal schema with common fields."""
    deal_type: str = Field("real_estate", description="Type of deal")
    deal_name: Optional[str] = Field(None, max_length=255, description="General deal name")
    stage: Optional[str] = Field(None, description="Current pipeline stage")
    status: Optional[str] = Field(None, description="Deal status")

    # Financial
    asking_price: Optional[float] = None
    offer_price: Optional[float] = None
    estimated_value: Optional[float] = None
    purchase_price: Optional[float] = None
    currency: str = "USD"

    # Real Estate
    property_name: Optional[str] = None
    property_address: Optional[str] = None
    property_type: Optional[str] = None
    market: Optional[str] = None
    units: Optional[int] = None
    square_feet: Optional[int] = None
    cap_rate: Optional[float] = None
    irr_target: Optional[float] = None

    # Company Acquisition
    target_company: Optional[str] = None
    sector: Optional[str] = None

    # Shares/Equity
    ticker_symbol: Optional[str] = None
    quantity: Optional[float] = None
    asset_class: Optional[str] = None

    # Commodities
    commodity_type: Optional[str] = None

    # Team & Timeline
    broker_id: Optional[UUID] = None
    lead_analyst: Optional[str] = None
    date_identified: Optional[date] = None
    loi_date: Optional[date] = None
    due_diligence_start: Optional[date] = None
    due_diligence_end: Optional[date] = None
    expected_closing: Optional[date] = None
    actual_closing: Optional[date] = None

    # Analysis
    notes: Optional[str] = None
    pros: Optional[str] = None
    cons: Optional[str] = None

    # Metadata
    documents_url: Optional[str] = None
    priority: int = Field(5, ge=1, le=10)
    confidence_level: Optional[int] = Field(None, ge=0, le=100)
    company_id: Optional[UUID] = None


class DealCreate(DealBase):
    """Schema for creating a new deal."""
    pass


class DealUpdate(BaseModel):
    """Schema for updating an existing deal."""
    deal_type: Optional[str] = None
    deal_name: Optional[str] = None
    stage: Optional[str] = None
    status: Optional[str] = None
    asking_price: Optional[float] = None
    offer_price: Optional[float] = None
    estimated_value: Optional[float] = None
    purchase_price: Optional[float] = None
    currency: Optional[str] = None
    property_name: Optional[str] = None
    property_address: Optional[str] = None
    property_type: Optional[str] = None
    market: Optional[str] = None
    units: Optional[int] = None
    square_feet: Optional[int] = None
    cap_rate: Optional[float] = None
    irr_target: Optional[float] = None
    target_company: Optional[str] = None
    sector: Optional[str] = None
    ticker_symbol: Optional[str] = None
    quantity: Optional[float] = None
    asset_class: Optional[str] = None
    commodity_type: Optional[str] = None
    broker_id: Optional[UUID] = None
    lead_analyst: Optional[str] = None
    date_identified: Optional[date] = None
    loi_date: Optional[date] = None
    due_diligence_start: Optional[date] = None
    due_diligence_end: Optional[date] = None
    expected_closing: Optional[date] = None
    actual_closing: Optional[date] = None
    notes: Optional[str] = None
    pros: Optional[str] = None
    cons: Optional[str] = None
    documents_url: Optional[str] = None
    priority: Optional[int] = None
    confidence_level: Optional[int] = None
    company_id: Optional[UUID] = None


class DealResponse(DealBase):
    """Schema for deal response with metadata."""
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DealSummary(BaseModel):
    """Lightweight deal summary."""
    id: UUID
    deal_type: str
    deal_name: Optional[str]
    property_name: Optional[str]
    target_company: Optional[str]
    ticker_symbol: Optional[str]
    stage: Optional[str]
    status: Optional[str]
    asking_price: Optional[float]
    purchase_price: Optional[float]

    class Config:
        from_attributes = True


# API Endpoints

@router.post("/", response_model=DealResponse, status_code=status.HTTP_201_CREATED)
async def create_deal(
    deal_data: DealCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new deal of any type.

    Supported deal types:
    - real_estate: Property acquisitions
    - company_acquisition: M&A transactions
    - shares: Stock/equity purchases
    - commodities: Commodity trading
    - debt: Debt instruments
    - other: Other transaction types
    """
    # Validate deal type
    valid_types = ["real_estate", "company_acquisition", "shares", "commodities", "debt", "other"]
    if deal_data.deal_type not in valid_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid deal_type. Must be one of: {', '.join(valid_types)}"
        )

    # Create new deal
    deal = Deal(**deal_data.model_dump())
    db.add(deal)
    db.commit()
    db.refresh(deal)

    return deal


@router.get("/", response_model=List[DealResponse])
async def list_deals(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records"),
    deal_type: Optional[str] = Query(None, description="Filter by deal type"),
    stage: Optional[str] = Query(None, description="Filter by stage"),
    status: Optional[str] = Query(None, description="Filter by status"),
    company_id: Optional[UUID] = Query(None, description="Filter by company"),
    search: Optional[str] = Query(None, description="Search in deal name, property, or company"),
    db: Session = Depends(get_db),
):
    """
    List all deals with optional filtering.

    Filters:
    - deal_type: Filter by transaction type
    - stage: Filter by pipeline stage
    - status: Filter by deal status
    - company_id: Filter by associated company
    - search: Search across names and descriptions
    """
    query = db.query(Deal)

    # Apply filters
    if deal_type:
        query = query.filter(Deal.deal_type == deal_type)

    if stage:
        query = query.filter(Deal.stage == stage)

    if status:
        query = query.filter(Deal.status == status)

    if company_id:
        query = query.filter(Deal.company_id == company_id)

    if search:
        search_filter = or_(
            Deal.deal_name.ilike(f"%{search}%"),
            Deal.property_name.ilike(f"%{search}%"),
            Deal.target_company.ilike(f"%{search}%"),
            Deal.ticker_symbol.ilike(f"%{search}%"),
            Deal.commodity_type.ilike(f"%{search}%"),
        )
        query = query.filter(search_filter)

    # Order by priority (high first) and then by created date
    deals = query.order_by(Deal.priority.desc(), Deal.created_at.desc()).offset(skip).limit(limit).all()

    return deals


@router.get("/summary", response_model=List[DealSummary])
async def list_deals_summary(
    db: Session = Depends(get_db),
):
    """
    Get lightweight list of all deals for dropdown/selector UI.

    Returns only essential fields for optimal performance.
    """
    deals = db.query(Deal).order_by(Deal.created_at.desc()).all()
    return deals


@router.get("/stats")
async def get_deal_statistics(
    db: Session = Depends(get_db),
):
    """
    Get deal pipeline statistics.

    Returns counts by type, stage, and status.
    """
    # Count by deal type
    type_counts = db.query(
        Deal.deal_type,
        func.count(Deal.id).label('count')
    ).group_by(Deal.deal_type).all()

    # Count by stage
    stage_counts = db.query(
        Deal.stage,
        func.count(Deal.id).label('count')
    ).group_by(Deal.stage).all()

    # Count by status
    status_counts = db.query(
        Deal.status,
        func.count(Deal.id).label('count')
    ).group_by(Deal.status).all()

    # Total deal value
    total_value = db.query(func.sum(Deal.purchase_price)).scalar() or 0
    pipeline_value = db.query(func.sum(Deal.asking_price)).filter(
        Deal.status != "completed"
    ).scalar() or 0

    return {
        "total_deals": db.query(Deal).count(),
        "by_type": {t: c for t, c in type_counts},
        "by_stage": {s: c for s, c in stage_counts},
        "by_status": {st: c for st, c in status_counts},
        "total_value": total_value,
        "pipeline_value": pipeline_value,
    }


@router.get("/{deal_id}", response_model=DealResponse)
async def get_deal(
    deal_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Get a specific deal by ID.

    - **deal_id**: UUID of the deal to retrieve
    """
    deal = db.query(Deal).filter(Deal.id == deal_id).first()

    if not deal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Deal with id {deal_id} not found"
        )

    return deal


@router.put("/{deal_id}", response_model=DealResponse)
async def update_deal(
    deal_id: UUID,
    deal_data: DealUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an existing deal.

    - **deal_id**: UUID of the deal to update
    - Only provided fields will be updated
    """
    deal = db.query(Deal).filter(Deal.id == deal_id).first()

    if not deal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Deal with id {deal_id} not found"
        )

    # Update deal fields
    update_data = deal_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(deal, field, value)

    db.commit()
    db.refresh(deal)

    return deal


@router.delete("/{deal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_deal(
    deal_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Delete a deal.

    - **deal_id**: UUID of the deal to delete
    """
    deal = db.query(Deal).filter(Deal.id == deal_id).first()

    if not deal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Deal with id {deal_id} not found"
        )

    db.delete(deal)
    db.commit()

    return None


@router.patch("/{deal_id}/stage")
async def update_deal_stage(
    deal_id: UUID,
    stage: str = Query(..., description="New stage"),
    db: Session = Depends(get_db),
):
    """
    Update deal stage (for pipeline management).

    - **deal_id**: UUID of the deal
    - **stage**: New stage value
    """
    deal = db.query(Deal).filter(Deal.id == deal_id).first()

    if not deal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Deal with id {deal_id} not found"
        )

    deal.stage = stage
    db.commit()
    db.refresh(deal)

    return {"id": deal.id, "stage": deal.stage}


@router.patch("/{deal_id}/status")
async def update_deal_status(
    deal_id: UUID,
    status: str = Query(..., description="New status"),
    db: Session = Depends(get_db),
):
    """
    Update deal status.

    - **deal_id**: UUID of the deal
    - **status**: New status value
    """
    deal = db.query(Deal).filter(Deal.id == deal_id).first()

    if not deal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Deal with id {deal_id} not found"
        )

    deal.status = status
    db.commit()
    db.refresh(deal)

    return {"id": deal.id, "status": deal.status}
