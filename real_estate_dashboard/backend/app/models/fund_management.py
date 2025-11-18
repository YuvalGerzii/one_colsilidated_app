"""
Fund Management Models

This module contains database models for PE/VC fund management including:
- Funds
- Limited Partners (LPs)
- Commitments
- Capital Calls
- Distributions
- Portfolio Investments
"""

from sqlalchemy import Column, String, Text, Numeric, Date, ForeignKey, Enum as SQLEnum, JSON
from sqlalchemy.dialects.postgresql import UUID as GUID
from sqlalchemy.orm import relationship
from decimal import Decimal
from datetime import date
import enum

from app.models.database import Base, UUIDMixin, TimestampMixin, SoftDeleteMixin


class FundType(str, enum.Enum):
    """Fund type enumeration"""
    PRIVATE_EQUITY = "Private Equity"
    VENTURE_CAPITAL = "Venture Capital"
    REAL_ESTATE = "Real Estate"
    DEBT = "Debt"
    INFRASTRUCTURE = "Infrastructure"
    HYBRID = "Hybrid"


class FundStatus(str, enum.Enum):
    """Fund status enumeration"""
    FUNDRAISING = "Fundraising"
    INVESTING = "Investing"
    HARVESTING = "Harvesting"
    LIQUIDATING = "Liquidating"
    CLOSED = "Closed"


class CapitalCallStatus(str, enum.Enum):
    """Capital call status enumeration"""
    PENDING = "Pending"
    SENT = "Sent"
    PARTIALLY_FUNDED = "Partially Funded"
    FULLY_FUNDED = "Fully Funded"
    OVERDUE = "Overdue"


class DistributionType(str, enum.Enum):
    """Distribution type enumeration"""
    RETURN_OF_CAPITAL = "Return of Capital"
    CARRIED_INTEREST = "Carried Interest"
    PREFERRED_RETURN = "Preferred Return"
    PROFIT_DISTRIBUTION = "Profit Distribution"


class Fund(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    Fund model representing a PE/VC fund
    """
    __tablename__ = "funds"

    # Basic Information
    name = Column(
        String(200),
        nullable=False,
        index=True,
        comment="Fund name"
    )

    fund_number = Column(
        String(50),
        nullable=True,
        unique=True,
        index=True,
        comment="Fund number/identifier (e.g., Fund I, Fund II)"
    )

    fund_type = Column(
        SQLEnum(FundType),
        nullable=False,
        default=FundType.PRIVATE_EQUITY,
        comment="Type of fund"
    )

    status = Column(
        SQLEnum(FundStatus),
        nullable=False,
        default=FundStatus.FUNDRAISING,
        comment="Current fund status"
    )

    description = Column(
        Text,
        nullable=True,
        comment="Fund description and strategy"
    )

    # Multi-Tenancy
    company_id = Column(
        GUID(as_uuid=True),
        ForeignKey('companies.id', ondelete='CASCADE'),
        nullable=True,
        index=True,
        comment="Company this fund belongs to (for multi-tenancy)"
    )

    # Fund Size and Structure
    target_size = Column(
        Numeric(20, 2),
        nullable=False,
        default=0,
        comment="Target fund size"
    )

    committed_capital = Column(
        Numeric(20, 2),
        nullable=False,
        default=0,
        comment="Total committed capital from LPs"
    )

    currency = Column(
        String(3),
        nullable=False,
        default='USD',
        comment="Fund currency (ISO code)"
    )

    # Dates
    vintage_year = Column(
        String(4),
        nullable=True,
        index=True,
        comment="Fund vintage year"
    )

    inception_date = Column(
        Date,
        nullable=True,
        comment="Fund inception date"
    )

    first_close_date = Column(
        Date,
        nullable=True,
        comment="First close date"
    )

    final_close_date = Column(
        Date,
        nullable=True,
        comment="Final close date"
    )

    investment_period_end = Column(
        Date,
        nullable=True,
        comment="End of investment period"
    )

    termination_date = Column(
        Date,
        nullable=True,
        comment="Expected termination date"
    )

    # Fee Structure
    management_fee_rate = Column(
        Numeric(5, 4),
        nullable=False,
        default=0.0200,
        comment="Management fee rate (e.g., 0.02 for 2%)"
    )

    management_fee_basis = Column(
        String(50),
        nullable=False,
        default='committed_capital',
        comment="Basis for management fee (committed_capital, invested_capital, nav)"
    )

    carried_interest_rate = Column(
        Numeric(5, 4),
        nullable=False,
        default=0.2000,
        comment="Carried interest rate (e.g., 0.20 for 20%)"
    )

    preferred_return_rate = Column(
        Numeric(5, 4),
        nullable=False,
        default=0.0800,
        comment="Preferred return/hurdle rate (e.g., 0.08 for 8%)"
    )

    catch_up_rate = Column(
        Numeric(5, 4),
        nullable=True,
        comment="GP catch-up rate (typically 1.0 for 100%)"
    )

    # Waterfall Structure (JSON)
    waterfall_structure = Column(
        JSON,
        nullable=True,
        comment="Detailed waterfall structure configuration"
    )

    # Performance Metrics (Calculated)
    total_called = Column(
        Numeric(20, 2),
        nullable=False,
        default=0,
        comment="Total capital called from LPs"
    )

    total_distributed = Column(
        Numeric(20, 2),
        nullable=False,
        default=0,
        comment="Total distributions to LPs"
    )

    nav = Column(
        Numeric(20, 2),
        nullable=False,
        default=0,
        comment="Net Asset Value (fair value of remaining investments)"
    )

    irr = Column(
        Numeric(8, 4),
        nullable=True,
        comment="Internal Rate of Return"
    )

    moic = Column(
        Numeric(8, 4),
        nullable=True,
        comment="Multiple on Invested Capital"
    )

    dpi = Column(
        Numeric(8, 4),
        nullable=True,
        comment="Distributions to Paid-In (DPI)"
    )

    rvpi = Column(
        Numeric(8, 4),
        nullable=True,
        comment="Residual Value to Paid-In (RVPI)"
    )

    tvpi = Column(
        Numeric(8, 4),
        nullable=True,
        comment="Total Value to Paid-In (TVPI = DPI + RVPI)"
    )

    # Relationships
    limited_partners = relationship("FundCommitment", back_populates="fund", cascade="all, delete-orphan")
    capital_calls = relationship("CapitalCall", back_populates="fund", cascade="all, delete-orphan")
    distributions = relationship("Distribution", back_populates="fund", cascade="all, delete-orphan")
    investments = relationship("PortfolioInvestment", back_populates="fund", cascade="all, delete-orphan")


class LimitedPartner(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    Limited Partner (Investor) model
    """
    __tablename__ = "limited_partners"

    # Basic Information
    name = Column(
        String(200),
        nullable=False,
        index=True,
        comment="LP name"
    )

    legal_name = Column(
        String(300),
        nullable=True,
        comment="Legal entity name"
    )

    lp_type = Column(
        String(100),
        nullable=True,
        comment="LP type (e.g., Pension Fund, Endowment, Family Office, Corporate)"
    )

    # Multi-Tenancy
    company_id = Column(
        GUID(as_uuid=True),
        ForeignKey('companies.id', ondelete='CASCADE'),
        nullable=True,
        index=True,
        comment="Company this LP belongs to (for multi-tenancy)"
    )

    # Contact Information
    contact_person = Column(
        String(200),
        nullable=True,
        comment="Primary contact person"
    )

    email = Column(
        String(255),
        nullable=True,
        comment="Contact email"
    )

    phone = Column(
        String(50),
        nullable=True,
        comment="Contact phone"
    )

    address = Column(
        Text,
        nullable=True,
        comment="Mailing address"
    )

    # Tax and Legal
    tax_id = Column(
        String(100),
        nullable=True,
        comment="Tax ID / EIN"
    )

    jurisdiction = Column(
        String(100),
        nullable=True,
        comment="Legal jurisdiction"
    )

    # Banking
    bank_name = Column(
        String(200),
        nullable=True,
        comment="Bank name for distributions"
    )

    bank_account = Column(
        String(100),
        nullable=True,
        comment="Bank account number"
    )

    bank_routing = Column(
        String(50),
        nullable=True,
        comment="Bank routing number"
    )

    # Notes
    notes = Column(
        Text,
        nullable=True,
        comment="Additional notes about the LP"
    )

    # Relationships
    commitments = relationship("FundCommitment", back_populates="limited_partner", cascade="all, delete-orphan")


class FundCommitment(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    LP Commitment to a Fund
    """
    __tablename__ = "fund_commitments"

    # Foreign Keys
    fund_id = Column(
        GUID,
        ForeignKey("funds.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Reference to fund"
    )

    lp_id = Column(
        GUID,
        ForeignKey("limited_partners.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Reference to limited partner"
    )

    # Commitment Details
    commitment_amount = Column(
        Numeric(20, 2),
        nullable=False,
        comment="Total commitment amount"
    )

    commitment_date = Column(
        Date,
        nullable=True,
        comment="Date of commitment"
    )

    commitment_percentage = Column(
        Numeric(8, 6),
        nullable=True,
        comment="Percentage of total fund"
    )

    # Tracking
    called_amount = Column(
        Numeric(20, 2),
        nullable=False,
        default=0,
        comment="Total amount called"
    )

    distributed_amount = Column(
        Numeric(20, 2),
        nullable=False,
        default=0,
        comment="Total amount distributed"
    )

    unfunded_commitment = Column(
        Numeric(20, 2),
        nullable=False,
        default=0,
        comment="Remaining uncalled commitment"
    )

    # Notes
    notes = Column(
        Text,
        nullable=True,
        comment="Commitment notes"
    )

    # Relationships
    fund = relationship("Fund", back_populates="limited_partners")
    limited_partner = relationship("LimitedPartner", back_populates="commitments")
    capital_call_items = relationship("CapitalCallItem", back_populates="commitment", cascade="all, delete-orphan")
    distribution_items = relationship("DistributionItem", back_populates="commitment", cascade="all, delete-orphan")


class CapitalCall(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    Capital Call from LPs
    """
    __tablename__ = "capital_calls"

    # Foreign Key
    fund_id = Column(
        GUID,
        ForeignKey("funds.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Reference to fund"
    )

    # Call Details
    call_number = Column(
        String(50),
        nullable=True,
        index=True,
        comment="Capital call number"
    )

    call_date = Column(
        Date,
        nullable=False,
        comment="Date capital call was issued"
    )

    due_date = Column(
        Date,
        nullable=False,
        comment="Date payment is due"
    )

    status = Column(
        SQLEnum(CapitalCallStatus),
        nullable=False,
        default=CapitalCallStatus.PENDING,
        comment="Capital call status"
    )

    total_call_amount = Column(
        Numeric(20, 2),
        nullable=False,
        comment="Total amount being called"
    )

    total_funded_amount = Column(
        Numeric(20, 2),
        nullable=False,
        default=0,
        comment="Total amount funded so far"
    )

    # Purpose
    purpose = Column(
        Text,
        nullable=True,
        comment="Purpose of the capital call"
    )

    investment_description = Column(
        Text,
        nullable=True,
        comment="Description of investments being made"
    )

    # Notes
    notes = Column(
        Text,
        nullable=True,
        comment="Additional notes"
    )

    # Relationships
    fund = relationship("Fund", back_populates="capital_calls")
    items = relationship("CapitalCallItem", back_populates="capital_call", cascade="all, delete-orphan")


class CapitalCallItem(Base, UUIDMixin, TimestampMixin):
    """
    Individual LP's portion of a capital call
    """
    __tablename__ = "capital_call_items"

    # Foreign Keys
    capital_call_id = Column(
        GUID,
        ForeignKey("capital_calls.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Reference to capital call"
    )

    commitment_id = Column(
        GUID,
        ForeignKey("fund_commitments.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Reference to LP commitment"
    )

    # Amounts
    called_amount = Column(
        Numeric(20, 2),
        nullable=False,
        comment="Amount called from this LP"
    )

    funded_amount = Column(
        Numeric(20, 2),
        nullable=False,
        default=0,
        comment="Amount funded by this LP"
    )

    funded_date = Column(
        Date,
        nullable=True,
        comment="Date LP funded the call"
    )

    # Relationships
    capital_call = relationship("CapitalCall", back_populates="items")
    commitment = relationship("FundCommitment", back_populates="capital_call_items")


class Distribution(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    Distribution to LPs
    """
    __tablename__ = "distributions"

    # Foreign Key
    fund_id = Column(
        GUID,
        ForeignKey("funds.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Reference to fund"
    )

    # Distribution Details
    distribution_number = Column(
        String(50),
        nullable=True,
        index=True,
        comment="Distribution number"
    )

    distribution_date = Column(
        Date,
        nullable=False,
        comment="Date of distribution"
    )

    distribution_type = Column(
        SQLEnum(DistributionType),
        nullable=False,
        comment="Type of distribution"
    )

    total_distribution_amount = Column(
        Numeric(20, 2),
        nullable=False,
        comment="Total amount distributed"
    )

    # Source
    source_investment_id = Column(
        GUID,
        ForeignKey("portfolio_investments.id", ondelete="SET NULL"),
        nullable=True,
        comment="Source portfolio investment (if applicable)"
    )

    source_description = Column(
        Text,
        nullable=True,
        comment="Description of distribution source"
    )

    # Notes
    notes = Column(
        Text,
        nullable=True,
        comment="Additional notes"
    )

    # Relationships
    fund = relationship("Fund", back_populates="distributions")
    source_investment = relationship("PortfolioInvestment")
    items = relationship("DistributionItem", back_populates="distribution", cascade="all, delete-orphan")


class DistributionItem(Base, UUIDMixin, TimestampMixin):
    """
    Individual LP's portion of a distribution
    """
    __tablename__ = "distribution_items"

    # Foreign Keys
    distribution_id = Column(
        GUID,
        ForeignKey("distributions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Reference to distribution"
    )

    commitment_id = Column(
        GUID,
        ForeignKey("fund_commitments.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Reference to LP commitment"
    )

    # Waterfall Breakdown
    return_of_capital = Column(
        Numeric(20, 2),
        nullable=False,
        default=0,
        comment="Return of capital portion"
    )

    preferred_return = Column(
        Numeric(20, 2),
        nullable=False,
        default=0,
        comment="Preferred return portion"
    )

    gp_catchup = Column(
        Numeric(20, 2),
        nullable=False,
        default=0,
        comment="GP catch-up portion"
    )

    carried_interest = Column(
        Numeric(20, 2),
        nullable=False,
        default=0,
        comment="Carried interest portion (to GP)"
    )

    remaining_profit = Column(
        Numeric(20, 2),
        nullable=False,
        default=0,
        comment="Remaining profit split"
    )

    total_distribution = Column(
        Numeric(20, 2),
        nullable=False,
        comment="Total distribution to LP"
    )

    # Relationships
    distribution = relationship("Distribution", back_populates="items")
    commitment = relationship("FundCommitment", back_populates="distribution_items")


class PortfolioInvestment(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    Portfolio company investment
    """
    __tablename__ = "portfolio_investments"

    # Foreign Key
    fund_id = Column(
        GUID,
        ForeignKey("funds.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Reference to fund"
    )

    # Company Information
    company_name = Column(
        String(200),
        nullable=False,
        comment="Portfolio company name"
    )

    industry = Column(
        String(100),
        nullable=True,
        comment="Industry/sector"
    )

    description = Column(
        Text,
        nullable=True,
        comment="Company description"
    )

    # Investment Details
    investment_date = Column(
        Date,
        nullable=True,
        comment="Initial investment date"
    )

    initial_investment_amount = Column(
        Numeric(20, 2),
        nullable=False,
        comment="Initial investment amount"
    )

    total_invested = Column(
        Numeric(20, 2),
        nullable=False,
        default=0,
        comment="Total amount invested (including follow-ons)"
    )

    current_value = Column(
        Numeric(20, 2),
        nullable=False,
        default=0,
        comment="Current fair value"
    )

    realized_value = Column(
        Numeric(20, 2),
        nullable=False,
        default=0,
        comment="Realized value from exits/distributions"
    )

    ownership_percentage = Column(
        Numeric(5, 4),
        nullable=True,
        comment="Ownership percentage"
    )

    # Status
    status = Column(
        String(50),
        nullable=True,
        comment="Investment status (Active, Exited, Written Off)"
    )

    exit_date = Column(
        Date,
        nullable=True,
        comment="Exit date (if applicable)"
    )

    exit_type = Column(
        String(100),
        nullable=True,
        comment="Exit type (IPO, M&A, Secondary, etc.)"
    )

    # Metrics
    moic = Column(
        Numeric(8, 4),
        nullable=True,
        comment="Investment-level MOIC"
    )

    irr = Column(
        Numeric(8, 4),
        nullable=True,
        comment="Investment-level IRR"
    )

    # Notes
    notes = Column(
        Text,
        nullable=True,
        comment="Investment notes"
    )

    # Relationships
    fund = relationship("Fund", back_populates="investments")
