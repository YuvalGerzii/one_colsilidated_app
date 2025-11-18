"""
Funds API Endpoints

Provides CRUD operations for private equity funds.
"""

from typing import List, Optional
from uuid import UUID
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.database import get_db
from app.models.fund import Fund
from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal


# Pydantic Schemas
class FundBase(BaseModel):
    """Base schema for fund data"""
    fund_name: str = Field(..., min_length=1, max_length=255)
    fund_number: Optional[int] = None
    vintage_year: int = Field(..., ge=1900, le=2100)
    fund_size: Decimal = Field(..., gt=0)
    committed_capital: Decimal = Field(..., ge=0)
    drawn_capital: Decimal = Field(default=Decimal(0), ge=0)
    distributed_capital: Decimal = Field(default=Decimal(0), ge=0)
    target_irr: Optional[Decimal] = Field(None, ge=0, le=1)
    fund_strategy: Optional[str] = Field(None, max_length=100)
    sector_focus: Optional[List[str]] = None
    geographic_focus: Optional[List[str]] = None
    fund_status: str = Field(default="Active", max_length=50)
    inception_date: Optional[date] = None
    close_date: Optional[date] = None
    final_close_date: Optional[date] = None


class FundCreate(FundBase):
    """Schema for creating a new fund"""
    pass


class FundUpdate(BaseModel):
    """Schema for updating a fund (all fields optional)"""
    fund_name: Optional[str] = Field(None, min_length=1, max_length=255)
    fund_number: Optional[int] = None
    vintage_year: Optional[int] = Field(None, ge=1900, le=2100)
    fund_size: Optional[Decimal] = Field(None, gt=0)
    committed_capital: Optional[Decimal] = Field(None, ge=0)
    drawn_capital: Optional[Decimal] = Field(None, ge=0)
    distributed_capital: Optional[Decimal] = Field(None, ge=0)
    target_irr: Optional[Decimal] = Field(None, ge=0, le=1)
    fund_strategy: Optional[str] = Field(None, max_length=100)
    sector_focus: Optional[List[str]] = None
    geographic_focus: Optional[List[str]] = None
    fund_status: Optional[str] = Field(None, max_length=50)
    inception_date: Optional[date] = None
    close_date: Optional[date] = None
    final_close_date: Optional[date] = None


class FundResponse(FundBase):
    """Schema for fund response"""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    fund_id: UUID  # Alias for frontend compatibility
    created_at: date
    updated_at: date

    def __init__(self, **data):
        # Add fund_id as alias for id
        if 'id' in data and 'fund_id' not in data:
            data['fund_id'] = data['id']
        super().__init__(**data)


class FundSummary(BaseModel):
    """Summary statistics for a fund"""
    fund_id: UUID
    fund_name: str
    vintage_year: int
    fund_size: float
    committed_capital: float
    drawn_capital: float
    distributed_capital: float
    deployment_rate: float
    remaining_capital: float
    tvpi: float
    fund_age_years: int
    num_companies: int
    fund_status: str


# Create router
router = APIRouter()


@router.get("/", response_model=List[FundResponse])
def get_funds(
    status: Optional[str] = Query(None, description="Filter by status"),
    vintage_year: Optional[int] = Query(None, description="Filter by vintage year"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """
    Get all funds with optional filters.

    - **status**: Filter by fund status (Active, Closed, etc.)
    - **vintage_year**: Filter by vintage year
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    """
    query = select(Fund)

    if status:
        query = query.where(Fund.fund_status == status)
    if vintage_year:
        query = query.where(Fund.vintage_year == vintage_year)

    query = query.offset(skip).limit(limit).order_by(Fund.vintage_year.desc())

    result = db.execute(query)
    funds = result.scalars().all()

    return [FundResponse.model_validate(fund) for fund in funds]


@router.get("/{fund_id}", response_model=FundResponse)
def get_fund(
    fund_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Get a specific fund by ID.
    """
    query = select(Fund).where(Fund.id == fund_id)
    result = db.execute(query)
    fund = result.scalar_one_or_none()

    if not fund:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fund with ID {fund_id} not found"
        )

    return FundResponse.model_validate(fund)


@router.post("/", response_model=FundResponse, status_code=status.HTTP_201_CREATED)
def create_fund(
    fund_data: FundCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new fund.
    """
    # Convert Pydantic model to dict and create SQLAlchemy model
    fund_dict = fund_data.model_dump()
    fund = Fund(**fund_dict)

    db.add(fund)
    db.commit()
    db.refresh(fund)

    return FundResponse.model_validate(fund)


@router.put("/{fund_id}", response_model=FundResponse)
def update_fund(
    fund_id: UUID,
    fund_data: FundUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an existing fund.
    """
    # Get existing fund
    query = select(Fund).where(Fund.id == fund_id)
    result = db.execute(query)
    fund = result.scalar_one_or_none()

    if not fund:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fund with ID {fund_id} not found"
        )

    # Update fields
    update_data = fund_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(fund, field, value)

    db.commit()
    db.refresh(fund)

    return FundResponse.model_validate(fund)


@router.delete("/{fund_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_fund(
    fund_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Delete a fund (hard delete - use with caution).
    """
    query = select(Fund).where(Fund.id == fund_id)
    result = db.execute(query)
    fund = result.scalar_one_or_none()

    if not fund:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fund with ID {fund_id} not found"
        )

    db.delete(fund)
    db.commit()
    return None


@router.get("/{fund_id}/summary", response_model=FundSummary)
def get_fund_summary(
    fund_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Get a summary of fund performance and portfolio.
    """
    query = select(Fund).where(Fund.id == fund_id)
    result = db.execute(query)
    fund = result.scalar_one_or_none()

    if not fund:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fund with ID {fund_id} not found"
        )

    # Count portfolio companies
    num_companies = fund.portfolio_companies.count()

    return FundSummary(
        fund_id=fund.id,
        fund_name=fund.fund_name,
        vintage_year=fund.vintage_year,
        fund_size=float(fund.fund_size),
        committed_capital=float(fund.committed_capital),
        drawn_capital=float(fund.drawn_capital),
        distributed_capital=float(fund.distributed_capital),
        deployment_rate=float(fund.deployment_rate),
        remaining_capital=float(fund.remaining_capital),
        tvpi=float(fund.tvpi),
        fund_age_years=fund.fund_age_years,
        num_companies=num_companies,
        fund_status=fund.fund_status,
    )


@router.get("/{fund_id}/companies")
def get_fund_companies(
    fund_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Get all portfolio companies for a specific fund.
    """
    query = select(Fund).where(Fund.id == fund_id)
    result = db.execute(query)
    fund = result.scalar_one_or_none()

    if not fund:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fund with ID {fund_id} not found"
        )

    # Get companies (using the relationship)
    companies = fund.portfolio_companies.all()

    return {
        "fund_id": fund.id,
        "fund_name": fund.fund_name,
        "num_companies": len(companies),
        "companies": [
            {
                "company_id": company.id,
                "company_name": company.company_name,
                "sector": company.sector,
                "status": company.company_status,
                "investment_date": company.investment_date,
                "equity_invested": float(company.equity_invested) if company.equity_invested else None,
            }
            for company in companies
        ],
    }
