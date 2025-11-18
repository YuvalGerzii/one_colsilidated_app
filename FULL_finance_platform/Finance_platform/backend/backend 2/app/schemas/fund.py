"""Fund schemas."""

from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class FundBase(BaseModel):
    """Base fund schema."""
    fund_name: str = Field(..., min_length=1, max_length=255)
    fund_number: Optional[int] = None
    vintage_year: int = Field(..., ge=1900, le=2100)
    fund_size: Decimal = Field(..., gt=0)
    committed_capital: Decimal = Field(..., gt=0)
    drawn_capital: Decimal = Field(default=Decimal(0), ge=0)
    distributed_capital: Decimal = Field(default=Decimal(0), ge=0)
    target_irr: Optional[Decimal] = None
    fund_strategy: Optional[str] = Field(None, max_length=100)
    sector_focus: Optional[List[str]] = None
    geographic_focus: Optional[List[str]] = None
    fund_status: str = Field(default='Active', max_length=50)
    inception_date: Optional[date] = None
    close_date: Optional[date] = None
    final_close_date: Optional[date] = None


class FundCreate(FundBase):
    """Schema for creating a fund."""
    pass


class FundUpdate(BaseModel):
    """Schema for updating a fund."""
    fund_name: Optional[str] = Field(None, min_length=1, max_length=255)
    fund_number: Optional[int] = None
    vintage_year: Optional[int] = Field(None, ge=1900, le=2100)
    fund_size: Optional[Decimal] = Field(None, gt=0)
    committed_capital: Optional[Decimal] = Field(None, gt=0)
    drawn_capital: Optional[Decimal] = Field(None, ge=0)
    distributed_capital: Optional[Decimal] = Field(None, ge=0)
    target_irr: Optional[Decimal] = None
    fund_strategy: Optional[str] = Field(None, max_length=100)
    sector_focus: Optional[List[str]] = None
    geographic_focus: Optional[List[str]] = None
    fund_status: Optional[str] = Field(None, max_length=50)
    inception_date: Optional[date] = None
    close_date: Optional[date] = None
    final_close_date: Optional[date] = None


class FundResponse(FundBase):
    """Schema for fund response."""
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
