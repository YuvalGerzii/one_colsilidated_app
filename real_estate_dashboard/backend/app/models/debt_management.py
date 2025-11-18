"""
Debt Management Models

This module contains database models for debt/financing management including:
- Loans
- Debt Covenants
- Amortization Schedules
- Loan Comparisons
"""

from sqlalchemy import Column, String, Text, Numeric, Date, Boolean, ForeignKey, Enum as SQLEnum, JSON
from sqlalchemy.dialects.postgresql import UUID as GUID
from sqlalchemy.orm import relationship
from decimal import Decimal
from datetime import date
import enum

from app.models.database import Base, UUIDMixin, TimestampMixin, SoftDeleteMixin


class LoanType(str, enum.Enum):
    """Loan type enumeration"""
    CONVENTIONAL = "Conventional"
    BRIDGE = "Bridge"
    CONSTRUCTION = "Construction"
    MEZZANINE = "Mezzanine"
    HARD_MONEY = "Hard Money"
    SBA = "SBA"
    CMBS = "CMBS"
    LINE_OF_CREDIT = "Line of Credit"
    OTHER = "Other"


class LoanStatus(str, enum.Enum):
    """Loan status enumeration"""
    ACTIVE = "Active"
    PENDING = "Pending"
    PAID_OFF = "Paid Off"
    REFINANCED = "Refinanced"
    DEFAULT = "Default"
    FORECLOSURE = "Foreclosure"


class InterestRateType(str, enum.Enum):
    """Interest rate type enumeration"""
    FIXED = "Fixed"
    VARIABLE = "Variable"
    HYBRID = "Hybrid"


class AmortizationType(str, enum.Enum):
    """Amortization type enumeration"""
    FULLY_AMORTIZING = "Fully Amortizing"
    INTEREST_ONLY = "Interest Only"
    BALLOON = "Balloon"
    NEGATIVE_AMORTIZATION = "Negative Amortization"


class CovenantType(str, enum.Enum):
    """Covenant type enumeration"""
    DSCR = "Debt Service Coverage Ratio"
    LTV = "Loan to Value"
    DEBT_YIELD = "Debt Yield"
    CASH_RESERVE = "Cash Reserve"
    OCCUPANCY = "Occupancy Rate"
    FINANCIAL_REPORTING = "Financial Reporting"
    OTHER = "Other"


class Loan(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    Loan/Debt Instrument Model
    """
    __tablename__ = "loans"

    # Basic Information
    loan_name = Column(
        String(200),
        nullable=False,
        index=True,
        comment="Loan identifier/name"
    )

    loan_number = Column(
        String(100),
        nullable=True,
        unique=True,
        index=True,
        comment="Lender's loan number"
    )

    loan_type = Column(
        SQLEnum(LoanType),
        nullable=False,
        default=LoanType.CONVENTIONAL,
        comment="Type of loan"
    )

    status = Column(
        SQLEnum(LoanStatus),
        nullable=False,
        default=LoanStatus.PENDING,
        comment="Current loan status"
    )

    # Multi-Tenancy
    company_id = Column(
        GUID(as_uuid=True),
        ForeignKey('companies.id', ondelete='CASCADE'),
        nullable=True,
        index=True,
        comment="Company this loan belongs to (for multi-tenancy)"
    )

    # Lender Information
    lender_name = Column(
        String(200),
        nullable=False,
        comment="Name of lending institution"
    )

    lender_contact = Column(
        String(200),
        nullable=True,
        comment="Primary lender contact"
    )

    lender_phone = Column(
        String(50),
        nullable=True,
        comment="Lender phone number"
    )

    lender_email = Column(
        String(255),
        nullable=True,
        comment="Lender email"
    )

    # Property/Collateral
    property_address = Column(
        Text,
        nullable=True,
        comment="Collateral property address"
    )

    property_value = Column(
        Numeric(20, 2),
        nullable=True,
        comment="Current property value"
    )

    # Loan Terms
    original_loan_amount = Column(
        Numeric(20, 2),
        nullable=False,
        comment="Original principal amount"
    )

    current_balance = Column(
        Numeric(20, 2),
        nullable=False,
        comment="Current outstanding balance"
    )

    interest_rate = Column(
        Numeric(8, 4),
        nullable=False,
        comment="Annual interest rate (e.g., 0.0425 for 4.25%)"
    )

    interest_rate_type = Column(
        SQLEnum(InterestRateType),
        nullable=False,
        default=InterestRateType.FIXED,
        comment="Fixed or variable rate"
    )

    # Variable rate details
    index_rate = Column(
        String(50),
        nullable=True,
        comment="Index for variable rate (e.g., SOFR, Prime)"
    )

    margin = Column(
        Numeric(8, 4),
        nullable=True,
        comment="Margin over index for variable rate"
    )

    rate_floor = Column(
        Numeric(8, 4),
        nullable=True,
        comment="Minimum interest rate floor"
    )

    rate_cap = Column(
        Numeric(8, 4),
        nullable=True,
        comment="Maximum interest rate cap"
    )

    # Term Details
    origination_date = Column(
        Date,
        nullable=False,
        comment="Loan origination date"
    )

    maturity_date = Column(
        Date,
        nullable=False,
        comment="Loan maturity date"
    )

    term_months = Column(
        Numeric(10, 0),
        nullable=False,
        comment="Loan term in months"
    )

    amortization_type = Column(
        SQLEnum(AmortizationType),
        nullable=False,
        default=AmortizationType.FULLY_AMORTIZING,
        comment="Type of amortization"
    )

    amortization_months = Column(
        Numeric(10, 0),
        nullable=True,
        comment="Amortization period in months"
    )

    interest_only_months = Column(
        Numeric(10, 0),
        nullable=True,
        default=0,
        comment="Number of interest-only months"
    )

    balloon_payment = Column(
        Numeric(20, 2),
        nullable=True,
        comment="Balloon payment amount at maturity"
    )

    # Payment Details
    monthly_payment = Column(
        Numeric(20, 2),
        nullable=True,
        comment="Regular monthly payment"
    )

    payment_frequency = Column(
        String(50),
        nullable=False,
        default="Monthly",
        comment="Payment frequency (Monthly, Quarterly, etc.)"
    )

    next_payment_date = Column(
        Date,
        nullable=True,
        comment="Next payment due date"
    )

    # Fees and Costs
    origination_fee = Column(
        Numeric(20, 2),
        nullable=True,
        default=0,
        comment="Origination fee paid"
    )

    closing_costs = Column(
        Numeric(20, 2),
        nullable=True,
        default=0,
        comment="Total closing costs"
    )

    prepayment_penalty = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="Has prepayment penalty"
    )

    prepayment_penalty_details = Column(
        Text,
        nullable=True,
        comment="Prepayment penalty terms"
    )

    # Calculated Metrics
    ltv_ratio = Column(
        Numeric(8, 4),
        nullable=True,
        comment="Loan to Value ratio"
    )

    dscr = Column(
        Numeric(8, 4),
        nullable=True,
        comment="Debt Service Coverage Ratio"
    )

    debt_yield = Column(
        Numeric(8, 4),
        nullable=True,
        comment="Debt Yield percentage"
    )

    # Additional Information
    purpose = Column(
        Text,
        nullable=True,
        comment="Loan purpose description"
    )

    notes = Column(
        Text,
        nullable=True,
        comment="Additional notes"
    )

    documents = Column(
        JSON,
        nullable=True,
        comment="Document references"
    )

    # Relationships
    covenants = relationship("DebtCovenant", back_populates="loan", cascade="all, delete-orphan")
    amortization_schedule = relationship("AmortizationScheduleEntry", back_populates="loan", cascade="all, delete-orphan")


class DebtCovenant(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    Debt Covenant Tracking
    """
    __tablename__ = "debt_covenants"

    # Foreign Key
    loan_id = Column(
        GUID,
        ForeignKey("loans.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Reference to loan"
    )

    # Covenant Details
    covenant_type = Column(
        SQLEnum(CovenantType),
        nullable=False,
        comment="Type of covenant"
    )

    covenant_name = Column(
        String(200),
        nullable=False,
        comment="Covenant name/description"
    )

    required_value = Column(
        Numeric(20, 4),
        nullable=False,
        comment="Required covenant value/threshold"
    )

    current_value = Column(
        Numeric(20, 4),
        nullable=True,
        comment="Current actual value"
    )

    measurement_frequency = Column(
        String(50),
        nullable=False,
        default="Quarterly",
        comment="How often measured (Monthly, Quarterly, Annually)"
    )

    next_measurement_date = Column(
        Date,
        nullable=True,
        comment="Next measurement date"
    )

    last_measurement_date = Column(
        Date,
        nullable=True,
        comment="Last measurement date"
    )

    in_compliance = Column(
        Boolean,
        nullable=False,
        default=True,
        comment="Currently in compliance"
    )

    breach_consequences = Column(
        Text,
        nullable=True,
        comment="Consequences of breach"
    )

    notes = Column(
        Text,
        nullable=True,
        comment="Additional notes"
    )

    # Relationship
    loan = relationship("Loan", back_populates="covenants")


class AmortizationScheduleEntry(Base, UUIDMixin, TimestampMixin):
    """
    Amortization Schedule Entry
    """
    __tablename__ = "amortization_schedule_entries"

    # Foreign Key
    loan_id = Column(
        GUID,
        ForeignKey("loans.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Reference to loan"
    )

    # Payment Details
    payment_number = Column(
        Numeric(10, 0),
        nullable=False,
        comment="Payment sequence number"
    )

    payment_date = Column(
        Date,
        nullable=False,
        comment="Payment due date"
    )

    beginning_balance = Column(
        Numeric(20, 2),
        nullable=False,
        comment="Balance at start of period"
    )

    payment_amount = Column(
        Numeric(20, 2),
        nullable=False,
        comment="Total payment amount"
    )

    principal_payment = Column(
        Numeric(20, 2),
        nullable=False,
        comment="Principal portion of payment"
    )

    interest_payment = Column(
        Numeric(20, 2),
        nullable=False,
        comment="Interest portion of payment"
    )

    ending_balance = Column(
        Numeric(20, 2),
        nullable=False,
        comment="Balance at end of period"
    )

    cumulative_principal = Column(
        Numeric(20, 2),
        nullable=False,
        comment="Cumulative principal paid"
    )

    cumulative_interest = Column(
        Numeric(20, 2),
        nullable=False,
        comment="Cumulative interest paid"
    )

    # Relationship
    loan = relationship("Loan", back_populates="amortization_schedule")


class LoanComparison(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    Loan Comparison Analysis
    """
    __tablename__ = "loan_comparisons"

    comparison_name = Column(
        String(200),
        nullable=False,
        comment="Name/title of comparison"
    )

    description = Column(
        Text,
        nullable=True,
        comment="Comparison description"
    )

    # Multi-Tenancy
    company_id = Column(
        GUID(as_uuid=True),
        ForeignKey('companies.id', ondelete='CASCADE'),
        nullable=True,
        index=True,
        comment="Company this comparison belongs to (for multi-tenancy)"
    )

    loan_scenarios = Column(
        JSON,
        nullable=False,
        comment="Array of loan scenarios to compare"
    )

    analysis_results = Column(
        JSON,
        nullable=True,
        comment="Comparison analysis results"
    )

    notes = Column(
        Text,
        nullable=True,
        comment="Additional notes"
    )
