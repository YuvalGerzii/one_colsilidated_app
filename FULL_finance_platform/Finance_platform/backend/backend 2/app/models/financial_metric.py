"""
Financial Metric Database Model

Time-series financial data for portfolio companies.
Stores income statement, balance sheet, and cash flow statement data.
"""

from datetime import date
from decimal import Decimal

from sqlalchemy import Column, String, Date, Integer, Numeric, Text, Boolean, CheckConstraint, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.database import BaseModel, AuditMixin


class FinancialMetric(BaseModel, AuditMixin):
    """
    Financial Metrics Model
    
    Stores time-series financial data (monthly, quarterly, annual, LTM).
    """
    
    __tablename__ = "financial_metrics"
    __table_args__ = (
        UniqueConstraint("company_id", "period_date", "period_type", name="unique_company_period"),
        CheckConstraint(
            "period_type IN ('Monthly', 'Quarterly', 'Annual', 'LTM')",
            name="valid_period_type"
        ),
    )
    
    # Foreign Keys
    company_id = Column(
        UUID(as_uuid=True),
        ForeignKey("portfolio_companies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Reference to portfolio company"
    )
    
    # Period Information
    period_date = Column(
        Date,
        nullable=False,
        index=True,
        comment="Period end date"
    )
    
    period_type = Column(
        String(20),
        nullable=False,
        comment="Period type: Monthly, Quarterly, Annual, LTM"
    )
    
    fiscal_year = Column(
        Integer,
        nullable=False,
        index=True,
        comment="Fiscal year"
    )
    
    fiscal_quarter = Column(
        Integer,
        nullable=True,
        comment="Fiscal quarter (1-4), NULL for annual"
    )
    
    fiscal_month = Column(
        Integer,
        nullable=True,
        comment="Fiscal month (1-12), NULL for quarterly/annual"
    )
    
    # ===========================================
    # INCOME STATEMENT
    # ===========================================
    
    # Revenue
    revenue = Column(Numeric(15, 2), comment="Total revenue")
    cogs = Column(Numeric(15, 2), comment="Cost of goods sold")
    gross_profit = Column(Numeric(15, 2), comment="Gross profit")
    gross_margin = Column(Numeric(5, 4), comment="Gross margin %")
    
    # Operating Expenses
    operating_expenses = Column(Numeric(15, 2), comment="Total operating expenses")
    sales_marketing = Column(Numeric(15, 2), comment="Sales & marketing expenses")
    research_development = Column(Numeric(15, 2), comment="R&D expenses")
    general_admin = Column(Numeric(15, 2), comment="G&A expenses")
    
    # EBITDA
    ebitda = Column(Numeric(15, 2), comment="EBITDA")
    ebitda_margin = Column(Numeric(5, 4), comment="EBITDA margin %")
    adjusted_ebitda = Column(Numeric(15, 2), comment="Adjusted EBITDA")
    adjusted_ebitda_margin = Column(Numeric(5, 4), comment="Adjusted EBITDA margin %")
    
    # Depreciation & Amortization
    depreciation = Column(Numeric(15, 2), comment="Depreciation")
    amortization = Column(Numeric(15, 2), comment="Amortization")
    ebit = Column(Numeric(15, 2), comment="EBIT")
    
    # Interest & Taxes
    interest_expense = Column(Numeric(15, 2), comment="Interest expense")
    interest_income = Column(Numeric(15, 2), comment="Interest income")
    other_income = Column(Numeric(15, 2), comment="Other income/(expense)")
    
    ebt = Column(Numeric(15, 2), comment="Earnings before tax")
    tax_expense = Column(Numeric(15, 2), comment="Tax expense")
    tax_rate = Column(Numeric(5, 4), comment="Effective tax rate %")
    net_income = Column(Numeric(15, 2), comment="Net income")
    net_margin = Column(Numeric(5, 4), comment="Net margin %")
    
    # ===========================================
    # BALANCE SHEET
    # ===========================================
    
    # Current Assets
    cash = Column(Numeric(15, 2), comment="Cash & equivalents")
    accounts_receivable = Column(Numeric(15, 2), comment="Accounts receivable")
    inventory = Column(Numeric(15, 2), comment="Inventory")
    prepaid_expenses = Column(Numeric(15, 2), comment="Prepaid expenses")
    other_current_assets = Column(Numeric(15, 2), comment="Other current assets")
    total_current_assets = Column(Numeric(15, 2), comment="Total current assets")
    
    # Long-term Assets
    ppe_gross = Column(Numeric(15, 2), comment="PP&E (gross)")
    accumulated_depreciation = Column(Numeric(15, 2), comment="Accumulated depreciation")
    ppe_net = Column(Numeric(15, 2), comment="PP&E (net)")
    intangible_assets = Column(Numeric(15, 2), comment="Intangible assets")
    goodwill = Column(Numeric(15, 2), comment="Goodwill")
    other_longterm_assets = Column(Numeric(15, 2), comment="Other long-term assets")
    total_assets = Column(Numeric(15, 2), comment="Total assets")
    
    # Current Liabilities
    accounts_payable = Column(Numeric(15, 2), comment="Accounts payable")
    accrued_expenses = Column(Numeric(15, 2), comment="Accrued expenses")
    current_portion_debt = Column(Numeric(15, 2), comment="Current portion of debt")
    other_current_liabilities = Column(Numeric(15, 2), comment="Other current liabilities")
    total_current_liabilities = Column(Numeric(15, 2), comment="Total current liabilities")
    
    # Long-term Liabilities
    long_term_debt = Column(Numeric(15, 2), comment="Long-term debt")
    deferred_taxes = Column(Numeric(15, 2), comment="Deferred taxes")
    other_longterm_liabilities = Column(Numeric(15, 2), comment="Other long-term liabilities")
    total_liabilities = Column(Numeric(15, 2), comment="Total liabilities")
    
    # Equity
    shareholders_equity = Column(Numeric(15, 2), comment="Shareholders equity")
    retained_earnings = Column(Numeric(15, 2), comment="Retained earnings")
    
    # ===========================================
    # CASH FLOW STATEMENT
    # ===========================================
    
    operating_cash_flow = Column(Numeric(15, 2), comment="Operating cash flow")
    capex = Column(Numeric(15, 2), comment="Capital expenditures")
    investing_cash_flow = Column(Numeric(15, 2), comment="Investing cash flow")
    financing_cash_flow = Column(Numeric(15, 2), comment="Financing cash flow")
    net_cash_flow = Column(Numeric(15, 2), comment="Net cash flow")
    free_cash_flow = Column(Numeric(15, 2), comment="Free cash flow")
    
    # ===========================================
    # CALCULATED METRICS
    # ===========================================
    
    working_capital = Column(Numeric(15, 2), comment="Working capital")
    net_working_capital = Column(Numeric(15, 2), comment="Net working capital")
    nwc_percent_revenue = Column(Numeric(5, 4), comment="NWC as % of revenue")
    
    # ===========================================
    # DATA SOURCE & VALIDATION
    # ===========================================
    
    data_source = Column(
        String(100),
        nullable=True,
        comment="Source: Management Report, Audited Financials, etc."
    )
    
    data_source_file_id = Column(
        UUID(as_uuid=True),
        ForeignKey("documents.id"),
        nullable=True,
        comment="Reference to source document"
    )
    
    verified = Column(
        Boolean,
        default=False,
        nullable=False,
        comment="Whether data has been verified"
    )
    
    verified_by = Column(
        UUID(as_uuid=True),
        nullable=True,
        comment="User who verified the data"
    )
    
    verified_at = Column(
        Date,
        nullable=True,
        comment="Verification date"
    )
    
    notes = Column(
        Text,
        nullable=True,
        comment="Additional notes"
    )
    
    # Relationships
    company = relationship(
        "PortfolioCompany",
        back_populates="financial_metrics"
    )
    
    source_document = relationship(
        "Document",
        foreign_keys=[data_source_file_id]
    )
    
    # Computed Properties
    @property
    def total_debt(self) -> Decimal:
        """Calculate total debt."""
        current = self.current_portion_debt or Decimal(0)
        longterm = self.long_term_debt or Decimal(0)
        return current + longterm
    
    @property
    def net_debt(self) -> Decimal:
        """Calculate net debt (total debt - cash)."""
        total_debt = self.total_debt
        cash = self.cash or Decimal(0)
        return total_debt - cash
    
    @property
    def current_ratio(self) -> Decimal:
        """Calculate current ratio."""
        if not self.total_current_liabilities or self.total_current_liabilities == 0:
            return Decimal(0)
        return (self.total_current_assets or Decimal(0)) / self.total_current_liabilities
    
    @property
    def debt_to_equity(self) -> Decimal:
        """Calculate debt-to-equity ratio."""
        if not self.shareholders_equity or self.shareholders_equity == 0:
            return Decimal(0)
        return self.total_debt / self.shareholders_equity
    
    def __repr__(self) -> str:
        return f"<FinancialMetric(company_id={self.company_id}, period={self.period_date}, type={self.period_type})>"
