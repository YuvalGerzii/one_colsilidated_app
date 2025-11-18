"""Financial metric schemas."""

from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class FinancialMetricBase(BaseModel):
    """Base financial metric schema."""
    company_id: UUID
    period_date: date
    period_type: str = Field(..., pattern="^(Monthly|Quarterly|Annual|LTM)$")
    fiscal_year: int
    fiscal_quarter: Optional[int] = Field(None, ge=1, le=4)
    fiscal_month: Optional[int] = Field(None, ge=1, le=12)
    
    # Income Statement
    revenue: Optional[Decimal] = None
    cogs: Optional[Decimal] = None
    gross_profit: Optional[Decimal] = None
    gross_margin: Optional[Decimal] = None
    operating_expenses: Optional[Decimal] = None
    sales_marketing: Optional[Decimal] = None
    research_development: Optional[Decimal] = None
    general_admin: Optional[Decimal] = None
    ebitda: Optional[Decimal] = None
    ebitda_margin: Optional[Decimal] = None
    adjusted_ebitda: Optional[Decimal] = None
    adjusted_ebitda_margin: Optional[Decimal] = None
    depreciation: Optional[Decimal] = None
    amortization: Optional[Decimal] = None
    ebit: Optional[Decimal] = None
    interest_expense: Optional[Decimal] = None
    interest_income: Optional[Decimal] = None
    other_income: Optional[Decimal] = None
    ebt: Optional[Decimal] = None
    tax_expense: Optional[Decimal] = None
    tax_rate: Optional[Decimal] = None
    net_income: Optional[Decimal] = None
    net_margin: Optional[Decimal] = None
    
    # Balance Sheet
    cash: Optional[Decimal] = None
    accounts_receivable: Optional[Decimal] = None
    inventory: Optional[Decimal] = None
    prepaid_expenses: Optional[Decimal] = None
    other_current_assets: Optional[Decimal] = None
    total_current_assets: Optional[Decimal] = None
    ppe_gross: Optional[Decimal] = None
    accumulated_depreciation: Optional[Decimal] = None
    ppe_net: Optional[Decimal] = None
    intangible_assets: Optional[Decimal] = None
    goodwill: Optional[Decimal] = None
    other_longterm_assets: Optional[Decimal] = None
    total_assets: Optional[Decimal] = None
    accounts_payable: Optional[Decimal] = None
    accrued_expenses: Optional[Decimal] = None
    current_portion_debt: Optional[Decimal] = None
    other_current_liabilities: Optional[Decimal] = None
    total_current_liabilities: Optional[Decimal] = None
    long_term_debt: Optional[Decimal] = None
    deferred_taxes: Optional[Decimal] = None
    other_longterm_liabilities: Optional[Decimal] = None
    total_liabilities: Optional[Decimal] = None
    shareholders_equity: Optional[Decimal] = None
    retained_earnings: Optional[Decimal] = None
    
    # Cash Flow Statement
    operating_cash_flow: Optional[Decimal] = None
    capex: Optional[Decimal] = None
    investing_cash_flow: Optional[Decimal] = None
    financing_cash_flow: Optional[Decimal] = None
    net_cash_flow: Optional[Decimal] = None
    free_cash_flow: Optional[Decimal] = None
    
    # Calculated Metrics
    working_capital: Optional[Decimal] = None
    net_working_capital: Optional[Decimal] = None
    nwc_percent_revenue: Optional[Decimal] = None
    
    # Data Source
    data_source: Optional[str] = Field(None, max_length=100)
    verified: bool = False
    notes: Optional[str] = None


class FinancialMetricCreate(FinancialMetricBase):
    """Schema for creating a financial metric."""
    pass


class FinancialMetricUpdate(BaseModel):
    """Schema for updating a financial metric."""
    period_date: Optional[date] = None
    period_type: Optional[str] = Field(None, pattern="^(Monthly|Quarterly|Annual|LTM)$")
    fiscal_year: Optional[int] = None
    fiscal_quarter: Optional[int] = Field(None, ge=1, le=4)
    fiscal_month: Optional[int] = Field(None, ge=1, le=12)
    revenue: Optional[Decimal] = None
    ebitda: Optional[Decimal] = None
    net_income: Optional[Decimal] = None
    verified: Optional[bool] = None
    notes: Optional[str] = None


class FinancialMetricResponse(FinancialMetricBase):
    """Schema for financial metric response."""
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
