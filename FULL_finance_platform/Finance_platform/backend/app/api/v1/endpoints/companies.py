"""
Portfolio Companies API Endpoints

Provides CRUD operations for portfolio companies.
"""

from typing import List, Optional
from uuid import UUID
from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import select, and_

from app.core.database import get_db
from app.models.company import PortfolioCompany
from pydantic import BaseModel, Field, ConfigDict, computed_field
from decimal import Decimal


# Pydantic Schemas
class CompanyBase(BaseModel):
    """Base schema for portfolio company data"""
    company_name: str = Field(..., min_length=1, max_length=255)
    company_legal_name: Optional[str] = Field(None, max_length=255)
    ticker_symbol: Optional[str] = Field(None, max_length=10)
    website: Optional[str] = Field(None, max_length=255)
    investment_date: date
    deal_type: str = Field(..., max_length=50)
    sector: str = Field(..., max_length=100)
    industry: Optional[str] = Field(None, max_length=100)
    sub_sector: Optional[str] = Field(None, max_length=100)
    business_description: Optional[str] = None
    headquarters_city: Optional[str] = Field(None, max_length=100)
    headquarters_state: Optional[str] = Field(None, max_length=100)
    headquarters_country: str = Field(default="United States", max_length=100)
    entry_revenue: Optional[Decimal] = None
    entry_ebitda: Optional[Decimal] = None
    entry_multiple: Optional[Decimal] = None
    purchase_price: Optional[Decimal] = None
    equity_invested: Optional[Decimal] = None
    debt_raised: Optional[Decimal] = None
    ownership_percentage: Optional[Decimal] = Field(None, ge=0, le=1)
    company_status: str = Field(default="Active", max_length=50)
    exit_date: Optional[date] = None
    exit_type: Optional[str] = Field(None, max_length=50)
    exit_proceeds: Optional[Decimal] = None
    realized_moic: Optional[Decimal] = None
    realized_irr: Optional[Decimal] = None
    risk_rating: str = Field(default="Medium", max_length=20)
    internal_rating: Optional[str] = Field(None, max_length=10)
    ceo_name: Optional[str] = Field(None, max_length=255)
    cfo_name: Optional[str] = Field(None, max_length=255)
    board_members: Optional[List[str]] = None


class CompanyCreate(CompanyBase):
    """Schema for creating a new company"""
    fund_id: UUID


class CompanyUpdate(BaseModel):
    """Schema for updating a company (all fields optional)"""
    company_name: Optional[str] = Field(None, min_length=1, max_length=255)
    company_legal_name: Optional[str] = Field(None, max_length=255)
    ticker_symbol: Optional[str] = Field(None, max_length=10)
    website: Optional[str] = Field(None, max_length=255)
    investment_date: Optional[date] = None
    deal_type: Optional[str] = Field(None, max_length=50)
    sector: Optional[str] = Field(None, max_length=100)
    industry: Optional[str] = Field(None, max_length=100)
    sub_sector: Optional[str] = Field(None, max_length=100)
    business_description: Optional[str] = None
    headquarters_city: Optional[str] = Field(None, max_length=100)
    headquarters_state: Optional[str] = Field(None, max_length=100)
    headquarters_country: Optional[str] = Field(None, max_length=100)
    entry_revenue: Optional[Decimal] = None
    entry_ebitda: Optional[Decimal] = None
    entry_multiple: Optional[Decimal] = None
    purchase_price: Optional[Decimal] = None
    equity_invested: Optional[Decimal] = None
    debt_raised: Optional[Decimal] = None
    ownership_percentage: Optional[Decimal] = Field(None, ge=0, le=1)
    company_status: Optional[str] = Field(None, max_length=50)
    exit_date: Optional[date] = None
    exit_type: Optional[str] = Field(None, max_length=50)
    exit_proceeds: Optional[Decimal] = None
    realized_moic: Optional[Decimal] = None
    realized_irr: Optional[Decimal] = None
    risk_rating: Optional[str] = Field(None, max_length=20)
    internal_rating: Optional[str] = Field(None, max_length=10)
    ceo_name: Optional[str] = Field(None, max_length=255)
    cfo_name: Optional[str] = Field(None, max_length=255)
    board_members: Optional[List[str]] = None


class CompanyResponse(CompanyBase):
    """Schema for company response"""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    fund_id: UUID
    created_at: datetime
    updated_at: datetime

    @computed_field
    @property
    def company_id(self) -> UUID:
        """Alias for id to match frontend expectations"""
        return self.id


# Create router
router = APIRouter()


@router.get("/", response_model=List[CompanyResponse])
def get_companies(
    fund_id: Optional[UUID] = Query(None, description="Filter by fund ID"),
    status: Optional[str] = Query(None, description="Filter by status"),
    sector: Optional[str] = Query(None, description="Filter by sector"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """
    Get all portfolio companies with optional filters.

    - **fund_id**: Filter companies by fund
    - **status**: Filter by company status (Active, Exited, etc.)
    - **sector**: Filter by sector
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    """
    query = select(PortfolioCompany).where(PortfolioCompany.deleted_at.is_(None))

    if fund_id:
        query = query.where(PortfolioCompany.fund_id == fund_id)
    if status:
        query = query.where(PortfolioCompany.company_status == status)
    if sector:
        query = query.where(PortfolioCompany.sector == sector)

    query = query.offset(skip).limit(limit).order_by(PortfolioCompany.created_at.desc())

    result = db.execute(query)
    companies = result.scalars().all()

    return [CompanyResponse.model_validate(company) for company in companies]


@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(
    company_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Get a specific portfolio company by ID.
    """
    query = select(PortfolioCompany).where(
        and_(
            PortfolioCompany.id == company_id,
            PortfolioCompany.deleted_at.is_(None)
        )
    )
    result = db.execute(query)
    company = result.scalar_one_or_none()

    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with ID {company_id} not found"
        )

    return CompanyResponse.model_validate(company)


@router.post("/", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
def create_company(
    company_data: CompanyCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new portfolio company.
    """
    # Convert Pydantic model to dict and create SQLAlchemy model
    company_dict = company_data.model_dump()
    company = PortfolioCompany(**company_dict)

    db.add(company)
    db.commit()
    db.refresh(company)

    return CompanyResponse.model_validate(company)


@router.put("/{company_id}", response_model=CompanyResponse)
def update_company(
    company_id: UUID,
    company_data: CompanyUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an existing portfolio company.
    """
    # Get existing company
    query = select(PortfolioCompany).where(
        and_(
            PortfolioCompany.id == company_id,
            PortfolioCompany.deleted_at.is_(None)
        )
    )
    result = db.execute(query)
    company = result.scalar_one_or_none()

    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with ID {company_id} not found"
        )

    # Update fields
    update_data = company_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(company, field, value)

    db.commit()
    db.refresh(company)

    return CompanyResponse.model_validate(company)


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(
    company_id: UUID,
    hard_delete: bool = Query(False, description="Permanently delete (true) or soft delete (false)"),
    db: Session = Depends(get_db),
):
    """
    Delete a portfolio company (soft delete by default).
    """
    query = select(PortfolioCompany).where(PortfolioCompany.id == company_id)
    result = db.execute(query)
    company = result.scalar_one_or_none()

    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with ID {company_id} not found"
        )

    if hard_delete:
        db.delete(company)
    else:
        company.soft_delete()

    db.commit()
    return None


@router.get("/{company_id}/summary")
def get_company_summary(
    company_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Get a summary of company financials and performance.
    """
    query = select(PortfolioCompany).where(
        and_(
            PortfolioCompany.id == company_id,
            PortfolioCompany.deleted_at.is_(None)
        )
    )
    result = db.execute(query)
    company = result.scalar_one_or_none()

    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with ID {company_id} not found"
        )

    return {
        "company_id": company.id,
        "company_name": company.company_name,
        "sector": company.sector,
        "status": company.company_status,
        "holding_period_years": company.holding_period_years,
        "entry_revenue": float(company.entry_revenue) if company.entry_revenue else None,
        "entry_ebitda": float(company.entry_ebitda) if company.entry_ebitda else None,
        "entry_multiple": float(company.entry_multiple) if company.entry_multiple else None,
        "equity_invested": float(company.equity_invested) if company.equity_invested else None,
        "ownership_percentage": float(company.ownership_percentage) if company.ownership_percentage else None,
        "realized_moic": float(company.realized_moic) if company.realized_moic else None,
        "realized_irr": float(company.realized_irr) if company.realized_irr else None,
    }
