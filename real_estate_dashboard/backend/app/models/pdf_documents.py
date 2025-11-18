"""
PDF Documents and Financial Statement Extraction Models

This module contains database models for:
- PDF document uploads and management
- Extracted financial statements (Income, Balance, Cash Flow)
- Historical valuation tracking
- Data comparison and analysis
"""

from sqlalchemy import Column, String, Float, Integer, JSON, ForeignKey, Text, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import enum
from datetime import datetime

from app.models.database import BaseModel, SoftDeleteMixin


# Enums
class DocumentType(str, enum.Enum):
    """Types of financial documents"""
    QUARTERLY_REPORT = "Quarterly Report"
    ANNUAL_REPORT = "Annual Report"
    INCOME_STATEMENT = "Income Statement"
    BALANCE_SHEET = "Balance Sheet"
    CASH_FLOW = "Cash Flow Statement"
    EARNINGS_RELEASE = "Earnings Release"
    INVESTOR_PRESENTATION = "Investor Presentation"
    OTHER = "Other"


class ExtractionStatus(str, enum.Enum):
    """Status of document extraction"""
    UPLOADED = "Uploaded"
    PROCESSING = "Processing"
    COMPLETED = "Completed"
    NEEDS_REVIEW = "Needs Review"
    REVIEWED = "Reviewed"
    FAILED = "Failed"


class PeriodType(str, enum.Enum):
    """Financial reporting periods"""
    QUARTERLY = "Quarterly"
    ANNUAL = "Annual"
    TTM = "TTM"  # Trailing Twelve Months
    NINE_MONTHS = "Nine Months"
    SIX_MONTHS = "Six Months"
    MONTHLY = "Monthly"


# Main Models

class FinancialDocument(BaseModel, SoftDeleteMixin):
    """
    Stores uploaded PDF documents and extraction metadata

    This is the master record for any financial document uploaded to the system.
    Links to extracted financial statements.
    """

    __tablename__ = "financial_documents"

    # Basic Info
    document_name = Column(String(500), nullable=False, comment="Original filename")
    document_type = Column(SQLEnum(DocumentType), nullable=False, index=True, comment="Type of document")

    # Company Link
    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.id'), nullable=True, index=True)
    company_name = Column(String(255), nullable=True, comment="Company name extracted from doc")
    ticker = Column(String(20), nullable=True, index=True, comment="Stock ticker if applicable")

    # File Storage
    file_path = Column(String(1000), nullable=False, comment="S3 or local file path")
    file_size_kb = Column(Integer, nullable=True, comment="File size in KB")
    page_count = Column(Integer, nullable=True, comment="Number of pages")

    # Upload Info
    upload_date = Column(DateTime, default=datetime.utcnow, comment="When document was uploaded")
    uploaded_by = Column(UUID(as_uuid=True), nullable=True, comment="User who uploaded")

    # Extraction Status
    extraction_status = Column(SQLEnum(ExtractionStatus), default=ExtractionStatus.UPLOADED, index=True)
    extraction_date = Column(DateTime, nullable=True, comment="When extraction completed")
    extraction_method = Column(String(50), nullable=True, comment="pdfplumber, AI, hybrid")
    extraction_confidence = Column(Float, nullable=True, comment="Overall confidence 0-1")

    # Validation
    needs_review = Column(Boolean, default=False, index=True, comment="Requires manual review")
    reviewed_by = Column(UUID(as_uuid=True), nullable=True, comment="User who reviewed")
    reviewed_date = Column(DateTime, nullable=True, comment="When reviewed")
    review_notes = Column(Text, nullable=True, comment="Reviewer's notes")

    # Extracted Data Summary
    periods_detected = Column(JSON, nullable=True, comment="List of periods found in document")
    statements_found = Column(JSON, nullable=True, comment="Which statements were extracted")
    extraction_errors = Column(JSON, nullable=True, comment="List of extraction issues")

    # Metadata
    user_id = Column(UUID(as_uuid=True), nullable=True, comment="Owner of this document")
    tags = Column(JSON, nullable=True, comment="User-defined tags for organization")

    # Relationships
    company = relationship("Company", backref="financial_documents")
    income_statements = relationship("ExtractedIncomeStatement", back_populates="document", cascade="all, delete-orphan")
    balance_sheets = relationship("ExtractedBalanceSheet", back_populates="document", cascade="all, delete-orphan")
    cash_flows = relationship("ExtractedCashFlow", back_populates="document", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<FinancialDocument(id={self.id}, name='{self.document_name}', company='{self.company_name}')>"


class ExtractedIncomeStatement(BaseModel):
    """
    Extracted Income Statement (P&L) data from PDF

    Stores comprehensive income statement line items with period information
    and confidence scoring.
    """

    __tablename__ = "extracted_income_statements"

    # Foreign Keys
    document_id = Column(UUID(as_uuid=True), ForeignKey('financial_documents.id'), nullable=False, index=True)
    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.id'), nullable=True, index=True)

    # Period Information
    period_date = Column(String(50), nullable=False, index=True, comment="YYYY-MM-DD format")
    period_type = Column(SQLEnum(PeriodType), nullable=False, index=True, comment="Quarterly, Annual, etc.")
    fiscal_year = Column(Integer, nullable=False, index=True, comment="Fiscal year")
    fiscal_quarter = Column(Integer, nullable=True, comment="Fiscal quarter (1-4)")

    # Revenue
    revenue = Column(Float, nullable=True, comment="Total revenue ($M)")
    cost_of_revenue = Column(Float, nullable=True, comment="COGS / Cost of revenue ($M)")
    gross_profit = Column(Float, nullable=True, comment="Gross profit ($M)")
    gross_margin_pct = Column(Float, nullable=True, comment="Gross margin %")

    # Operating Expenses
    operating_expenses = Column(Float, nullable=True, comment="Total operating expenses ($M)")
    rd_expense = Column(Float, nullable=True, comment="R&D expense ($M)")
    sga_expense = Column(Float, nullable=True, comment="SG&A expense ($M)")
    marketing_expense = Column(Float, nullable=True, comment="Marketing expense ($M)")
    other_opex = Column(Float, nullable=True, comment="Other operating expenses ($M)")

    # Operating Income
    ebitda = Column(Float, nullable=True, comment="EBITDA ($M)")
    ebitda_margin_pct = Column(Float, nullable=True, comment="EBITDA margin %")
    depreciation_amortization = Column(Float, nullable=True, comment="D&A ($M)")
    ebit = Column(Float, nullable=True, comment="EBIT / Operating income ($M)")
    ebit_margin_pct = Column(Float, nullable=True, comment="EBIT margin %")

    # Non-Operating Items
    interest_expense = Column(Float, nullable=True, comment="Interest expense ($M)")
    interest_income = Column(Float, nullable=True, comment="Interest income ($M)")
    other_income_expense = Column(Float, nullable=True, comment="Other income/(expense) ($M)")

    # Pre-Tax and Taxes
    pretax_income = Column(Float, nullable=True, comment="Income before tax ($M)")
    income_tax_expense = Column(Float, nullable=True, comment="Income tax expense ($M)")
    effective_tax_rate_pct = Column(Float, nullable=True, comment="Effective tax rate %")

    # Net Income
    net_income = Column(Float, nullable=True, comment="Net income ($M)")
    net_margin_pct = Column(Float, nullable=True, comment="Net margin %")

    # Per-Share Data
    shares_outstanding_basic = Column(Float, nullable=True, comment="Basic shares outstanding (M)")
    shares_outstanding_diluted = Column(Float, nullable=True, comment="Diluted shares outstanding (M)")
    eps_basic = Column(Float, nullable=True, comment="Basic EPS ($)")
    eps_diluted = Column(Float, nullable=True, comment="Diluted EPS ($)")

    # Metadata
    source_page = Column(Integer, nullable=True, comment="Page number in PDF")
    confidence_score = Column(Float, nullable=True, comment="Extraction confidence 0-1")
    currency = Column(String(10), default="USD", comment="Currency code")
    unit = Column(String(20), default="millions", comment="millions, thousands, actual")
    extraction_notes = Column(Text, nullable=True, comment="Notes from extraction")

    # Manual Overrides
    is_manually_edited = Column(Boolean, default=False, comment="Has been manually corrected")
    edited_by = Column(UUID(as_uuid=True), nullable=True, comment="User who edited")
    edited_date = Column(DateTime, nullable=True, comment="When edited")

    # Relationships
    document = relationship("FinancialDocument", back_populates="income_statements")
    company = relationship("Company")

    def __repr__(self):
        return f"<ExtractedIncomeStatement(id={self.id}, period='{self.period_date}', revenue={self.revenue})>"


class ExtractedBalanceSheet(BaseModel):
    """
    Extracted Balance Sheet data from PDF

    Stores comprehensive balance sheet line items (Assets, Liabilities, Equity)
    """

    __tablename__ = "extracted_balance_sheets"

    # Foreign Keys
    document_id = Column(UUID(as_uuid=True), ForeignKey('financial_documents.id'), nullable=False, index=True)
    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.id'), nullable=True, index=True)

    # Period Information
    period_date = Column(String(50), nullable=False, index=True, comment="YYYY-MM-DD format")
    period_type = Column(SQLEnum(PeriodType), nullable=False, index=True)
    fiscal_year = Column(Integer, nullable=False, index=True)
    fiscal_quarter = Column(Integer, nullable=True)

    # ASSETS - Current
    cash_and_equivalents = Column(Float, nullable=True, comment="Cash & cash equivalents ($M)")
    marketable_securities = Column(Float, nullable=True, comment="Marketable securities ($M)")
    accounts_receivable = Column(Float, nullable=True, comment="Accounts receivable ($M)")
    inventory = Column(Float, nullable=True, comment="Inventory ($M)")
    prepaid_expenses = Column(Float, nullable=True, comment="Prepaid expenses ($M)")
    other_current_assets = Column(Float, nullable=True, comment="Other current assets ($M)")
    total_current_assets = Column(Float, nullable=True, comment="Total current assets ($M)")

    # ASSETS - Non-Current
    ppe_gross = Column(Float, nullable=True, comment="PP&E gross ($M)")
    accumulated_depreciation = Column(Float, nullable=True, comment="Accumulated depreciation ($M)")
    ppe_net = Column(Float, nullable=True, comment="PP&E net ($M)")
    goodwill = Column(Float, nullable=True, comment="Goodwill ($M)")
    intangible_assets = Column(Float, nullable=True, comment="Intangible assets ($M)")
    long_term_investments = Column(Float, nullable=True, comment="Long-term investments ($M)")
    other_noncurrent_assets = Column(Float, nullable=True, comment="Other non-current assets ($M)")
    total_assets = Column(Float, nullable=True, comment="Total assets ($M)")

    # LIABILITIES - Current
    accounts_payable = Column(Float, nullable=True, comment="Accounts payable ($M)")
    accrued_expenses = Column(Float, nullable=True, comment="Accrued expenses ($M)")
    short_term_debt = Column(Float, nullable=True, comment="Short-term debt ($M)")
    current_portion_long_term_debt = Column(Float, nullable=True, comment="Current portion of LT debt ($M)")
    deferred_revenue_current = Column(Float, nullable=True, comment="Deferred revenue - current ($M)")
    other_current_liabilities = Column(Float, nullable=True, comment="Other current liabilities ($M)")
    total_current_liabilities = Column(Float, nullable=True, comment="Total current liabilities ($M)")

    # LIABILITIES - Non-Current
    long_term_debt = Column(Float, nullable=True, comment="Long-term debt ($M)")
    deferred_revenue_noncurrent = Column(Float, nullable=True, comment="Deferred revenue - non-current ($M)")
    deferred_tax_liabilities = Column(Float, nullable=True, comment="Deferred tax liabilities ($M)")
    pension_liabilities = Column(Float, nullable=True, comment="Pension liabilities ($M)")
    other_noncurrent_liabilities = Column(Float, nullable=True, comment="Other non-current liabilities ($M)")
    total_liabilities = Column(Float, nullable=True, comment="Total liabilities ($M)")

    # EQUITY
    common_stock = Column(Float, nullable=True, comment="Common stock ($M)")
    preferred_stock = Column(Float, nullable=True, comment="Preferred stock ($M)")
    additional_paid_in_capital = Column(Float, nullable=True, comment="Additional paid-in capital ($M)")
    retained_earnings = Column(Float, nullable=True, comment="Retained earnings ($M)")
    treasury_stock = Column(Float, nullable=True, comment="Treasury stock ($M)")
    accumulated_other_comprehensive_income = Column(Float, nullable=True, comment="AOCI ($M)")
    total_equity = Column(Float, nullable=True, comment="Total equity ($M)")

    # Total Liabilities + Equity (should equal Total Assets)
    total_liabilities_and_equity = Column(Float, nullable=True, comment="Total L + E ($M)")

    # Calculated Metrics
    working_capital = Column(Float, nullable=True, comment="Current Assets - Current Liabilities ($M)")
    net_debt = Column(Float, nullable=True, comment="Total Debt - Cash ($M)")
    book_value_per_share = Column(Float, nullable=True, comment="Book value per share ($)")

    # Metadata
    source_page = Column(Integer, nullable=True)
    confidence_score = Column(Float, nullable=True)
    currency = Column(String(10), default="USD")
    unit = Column(String(20), default="millions")
    extraction_notes = Column(Text, nullable=True)

    # Validation Flags
    balance_sheet_balances = Column(Boolean, nullable=True, comment="Does Assets = L + E?")
    balance_difference = Column(Float, nullable=True, comment="Assets - (L + E) if not balanced")

    # Manual Overrides
    is_manually_edited = Column(Boolean, default=False)
    edited_by = Column(UUID(as_uuid=True), nullable=True)
    edited_date = Column(DateTime, nullable=True)

    # Relationships
    document = relationship("FinancialDocument", back_populates="balance_sheets")
    company = relationship("Company")

    def __repr__(self):
        return f"<ExtractedBalanceSheet(id={self.id}, period='{self.period_date}', total_assets={self.total_assets})>"


class ExtractedCashFlow(BaseModel):
    """
    Extracted Cash Flow Statement data from PDF

    Stores comprehensive cash flow data (Operating, Investing, Financing activities)
    """

    __tablename__ = "extracted_cash_flows"

    # Foreign Keys
    document_id = Column(UUID(as_uuid=True), ForeignKey('financial_documents.id'), nullable=False, index=True)
    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.id'), nullable=True, index=True)

    # Period Information
    period_date = Column(String(50), nullable=False, index=True)
    period_type = Column(SQLEnum(PeriodType), nullable=False, index=True)
    fiscal_year = Column(Integer, nullable=False, index=True)
    fiscal_quarter = Column(Integer, nullable=True)

    # OPERATING ACTIVITIES
    net_income = Column(Float, nullable=True, comment="Net income ($M)")
    depreciation_amortization = Column(Float, nullable=True, comment="D&A ($M)")
    stock_based_compensation = Column(Float, nullable=True, comment="Stock-based comp ($M)")
    deferred_taxes = Column(Float, nullable=True, comment="Deferred taxes ($M)")
    change_in_working_capital = Column(Float, nullable=True, comment="Change in NWC ($M)")
    change_in_accounts_receivable = Column(Float, nullable=True, comment="Change in A/R ($M)")
    change_in_inventory = Column(Float, nullable=True, comment="Change in inventory ($M)")
    change_in_accounts_payable = Column(Float, nullable=True, comment="Change in A/P ($M)")
    other_operating_activities = Column(Float, nullable=True, comment="Other operating ($M)")
    cash_from_operations = Column(Float, nullable=True, comment="Net cash from operations ($M)")

    # INVESTING ACTIVITIES
    capex = Column(Float, nullable=True, comment="Capital expenditures ($M)")
    acquisitions = Column(Float, nullable=True, comment="Acquisitions ($M)")
    asset_sales = Column(Float, nullable=True, comment="Proceeds from asset sales ($M)")
    purchases_of_investments = Column(Float, nullable=True, comment="Purchases of investments ($M)")
    sales_of_investments = Column(Float, nullable=True, comment="Sales of investments ($M)")
    other_investing_activities = Column(Float, nullable=True, comment="Other investing ($M)")
    cash_from_investing = Column(Float, nullable=True, comment="Net cash from investing ($M)")

    # FINANCING ACTIVITIES
    debt_issued = Column(Float, nullable=True, comment="Debt issued ($M)")
    debt_repaid = Column(Float, nullable=True, comment="Debt repaid ($M)")
    net_debt_issuance = Column(Float, nullable=True, comment="Net debt issuance ($M)")
    equity_issued = Column(Float, nullable=True, comment="Equity issued ($M)")
    share_repurchases = Column(Float, nullable=True, comment="Share buybacks ($M)")
    dividends_paid = Column(Float, nullable=True, comment="Dividends paid ($M)")
    other_financing_activities = Column(Float, nullable=True, comment="Other financing ($M)")
    cash_from_financing = Column(Float, nullable=True, comment="Net cash from financing ($M)")

    # SUMMARY
    net_change_in_cash = Column(Float, nullable=True, comment="Net change in cash ($M)")
    beginning_cash = Column(Float, nullable=True, comment="Beginning cash balance ($M)")
    ending_cash = Column(Float, nullable=True, comment="Ending cash balance ($M)")

    # CALCULATED METRICS
    free_cash_flow = Column(Float, nullable=True, comment="FCF = CFO - CapEx ($M)")
    fcf_conversion_pct = Column(Float, nullable=True, comment="FCF / Net Income %")
    cash_conversion_cycle = Column(Float, nullable=True, comment="Cash conversion cycle (days)")

    # Metadata
    source_page = Column(Integer, nullable=True)
    confidence_score = Column(Float, nullable=True)
    currency = Column(String(10), default="USD")
    unit = Column(String(20), default="millions")
    extraction_notes = Column(Text, nullable=True)

    # Validation Flags
    cash_flow_reconciles = Column(Boolean, nullable=True, comment="Does sum of activities = net change?")
    reconciliation_difference = Column(Float, nullable=True, comment="Difference if doesn't reconcile")

    # Manual Overrides
    is_manually_edited = Column(Boolean, default=False)
    edited_by = Column(UUID(as_uuid=True), nullable=True)
    edited_date = Column(DateTime, nullable=True)

    # Relationships
    document = relationship("FinancialDocument", back_populates="cash_flows")
    company = relationship("Company")

    def __repr__(self):
        return f"<ExtractedCashFlow(id={self.id}, period='{self.period_date}', fcf={self.free_cash_flow})>"


class ValuationSnapshot(BaseModel):
    """
    Historical Valuation Snapshot

    Stores a point-in-time valuation of a company using DCF or LBO.
    Enables tracking how valuations change over time as new data comes in.
    """

    __tablename__ = "valuation_snapshots"

    # Foreign Keys
    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.id'), nullable=False, index=True)
    dcf_model_id = Column(UUID(as_uuid=True), ForeignKey('dcf_models.id'), nullable=True)
    lbo_model_id = Column(UUID(as_uuid=True), ForeignKey('lbo_models.id'), nullable=True)

    # Snapshot Info
    snapshot_date = Column(DateTime, default=datetime.utcnow, index=True, comment="When valuation was performed")
    valuation_date = Column(String(50), nullable=True, comment="As-of date for the valuation")
    model_type = Column(String(50), nullable=False, index=True, comment="DCF, LBO, Comps, etc.")

    # Key Results
    enterprise_value = Column(Float, nullable=True, comment="Enterprise value ($M)")
    equity_value = Column(Float, nullable=True, comment="Equity value ($M)")
    equity_value_per_share = Column(Float, nullable=True, comment="Value per share ($)")

    # Valuation Metrics
    implied_ev_revenue = Column(Float, nullable=True, comment="Implied EV/Revenue multiple")
    implied_ev_ebitda = Column(Float, nullable=True, comment="Implied EV/EBITDA multiple")
    implied_pe_ratio = Column(Float, nullable=True, comment="Implied P/E ratio")

    # DCF-Specific
    wacc = Column(Float, nullable=True, comment="WACC used (%)")
    terminal_growth_rate = Column(Float, nullable=True, comment="Terminal growth rate (%)")
    terminal_value = Column(Float, nullable=True, comment="Terminal value ($M)")
    terminal_value_pct = Column(Float, nullable=True, comment="Terminal value as % of EV")

    # LBO-Specific
    entry_multiple = Column(Float, nullable=True, comment="Entry EV/EBITDA")
    exit_multiple = Column(Float, nullable=True, comment="Exit EV/EBITDA")
    leverage_ratio = Column(Float, nullable=True, comment="Debt/EBITDA at entry")
    equity_irr = Column(Float, nullable=True, comment="Equity IRR (%)")
    moic = Column(Float, nullable=True, comment="Money-on-invested-capital (x)")

    # Source Data References
    source_documents = Column(JSON, nullable=True, comment="List of document IDs used")
    key_assumptions = Column(JSON, nullable=True, comment="Key assumptions JSON")
    sensitivity_ranges = Column(JSON, nullable=True, comment="Sensitivity analysis ranges")

    # Context
    market_conditions = Column(JSON, nullable=True, comment="Market data at valuation date")
    comparable_trading_multiples = Column(JSON, nullable=True, comment="Peer trading multiples")
    notes = Column(Text, nullable=True, comment="Analyst notes")

    # Metadata
    created_by = Column(UUID(as_uuid=True), nullable=True, comment="User who created")
    version_number = Column(Integer, default=1, comment="Version of this valuation")
    is_published = Column(Boolean, default=False, comment="Published to stakeholders")

    # Relationships
    company = relationship("Company")
    dcf_model = relationship("DCFModel")
    lbo_model = relationship("LBOModel")

    def __repr__(self):
        return f"<ValuationSnapshot(id={self.id}, company_id={self.company_id}, ev={self.enterprise_value}, date='{self.snapshot_date}')>"


class ValuationComparison(BaseModel):
    """
    Valuation Comparison and Variance Analysis

    Tracks changes between valuations over time. Useful for understanding
    what drove changes in valuation estimates.
    """

    __tablename__ = "valuation_comparisons"

    # Snapshots Being Compared
    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.id'), nullable=False, index=True)
    baseline_snapshot_id = Column(UUID(as_uuid=True), ForeignKey('valuation_snapshots.id'), nullable=False)
    comparison_snapshot_id = Column(UUID(as_uuid=True), ForeignKey('valuation_snapshots.id'), nullable=False)

    # Comparison Info
    comparison_date = Column(DateTime, default=datetime.utcnow)
    comparison_type = Column(String(50), nullable=True, comment="Sequential, YoY, Scenario, etc.")

    # Value Changes
    ev_change = Column(Float, nullable=True, comment="Change in EV ($M)")
    ev_change_pct = Column(Float, nullable=True, comment="Change in EV (%)")
    equity_value_change = Column(Float, nullable=True, comment="Change in equity value ($M)")
    equity_value_change_pct = Column(Float, nullable=True, comment="Change in equity value (%)")

    # Driver Analysis (what caused the change)
    revenue_impact = Column(Float, nullable=True, comment="Impact from revenue changes ($M)")
    margin_impact = Column(Float, nullable=True, comment="Impact from margin changes ($M)")
    wacc_impact = Column(Float, nullable=True, comment="Impact from WACC changes ($M)")
    terminal_value_impact = Column(Float, nullable=True, comment="Impact from terminal value ($M)")
    multiple_impact = Column(Float, nullable=True, comment="Impact from multiple changes ($M)")
    other_impact = Column(Float, nullable=True, comment="Other impacts ($M)")

    # Detailed Variance Bridge
    variance_bridge = Column(JSON, nullable=True, comment="Detailed waterfall of changes")
    key_changes = Column(JSON, nullable=True, comment="Summary of key changes")

    # Analysis
    commentary = Column(Text, nullable=True, comment="Analyst commentary on changes")
    prepared_by = Column(UUID(as_uuid=True), nullable=True, comment="User who prepared analysis")

    # Relationships
    company = relationship("Company")
    baseline_snapshot = relationship("ValuationSnapshot", foreign_keys=[baseline_snapshot_id])
    comparison_snapshot = relationship("ValuationSnapshot", foreign_keys=[comparison_snapshot_id])

    def __repr__(self):
        return f"<ValuationComparison(id={self.id}, company_id={self.company_id}, ev_change={self.ev_change})>"


# Export all
__all__ = [
    "DocumentType",
    "ExtractionStatus",
    "PeriodType",
    "FinancialDocument",
    "ExtractedIncomeStatement",
    "ExtractedBalanceSheet",
    "ExtractedCashFlow",
    "ValuationSnapshot",
    "ValuationComparison",
]
