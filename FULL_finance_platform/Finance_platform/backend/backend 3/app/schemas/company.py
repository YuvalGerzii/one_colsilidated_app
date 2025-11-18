"""Company schemas."""

from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class CompanyBase(BaseModel):
    """Base company schema."""
    fund_id: UUID
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
    headquarters_country: str = Field(default='United States', max_length=100)
    entry_revenue: Optional[Decimal] = None
    entry_ebitda: Optional[Decimal] = None
    entry_multiple: Optional[Decimal] = None
    purchase_price: Optional[Decimal] = None
    equity_invested: Optional[Decimal] = None
    debt_raised: Optional[Decimal] = None
    ownership_percentage: Optional[Decimal] = Field(None, ge=0, le=1)
    company_status: str = Field(default='Active', max_length=50)
    exit_date: Optional[date] = None
    exit_type: Optional[str] = Field(None, max_length=50)
    exit_proceeds: Optional[Decimal] = None
    realized_moic: Optional[Decimal] = None
    realized_irr: Optional[Decimal] = None
    risk_rating: str = Field(default='Medium', max_length=20)
    internal_rating: Optional[str] = Field(None, max_length=10)
    ceo_name: Optional[str] = Field(None, max_length=255)
    cfo_name: Optional[str] = Field(None, max_length=255)
    board_members: Optional[List[str]] = None


class CompanyCreate(CompanyBase):
    """Schema for creating a company."""
    pass


class CompanyUpdate(BaseModel):
    """Schema for updating a company."""
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
    """Schema for company response."""
    id: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
