"""
Accounting Models

This module contains comprehensive accounting models for:
- Small businesses and companies
- Individuals and high net worth individuals
- Financial institutions
- Property management accounting
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional
from enum import Enum

from sqlalchemy import Column, String, Text, Numeric, Boolean, Enum as SQLEnum, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.models.database import Base, UUIDMixin, TimestampMixin, SoftDeleteMixin


class AccountingEntityType(str, Enum):
    """Types of accounting entities"""
    SMALL_BUSINESS = "small_business"
    INDIVIDUAL = "individual"
    HIGH_NET_WORTH = "high_net_worth"
    FINANCIAL_INSTITUTION = "financial_institution"
    PROPERTY_MANAGEMENT = "property_management"


class AccountType(str, Enum):
    """Chart of Accounts - Account Types"""
    ASSET = "asset"
    LIABILITY = "liability"
    EQUITY = "equity"
    REVENUE = "revenue"
    EXPENSE = "expense"


class AccountSubType(str, Enum):
    """Detailed account classifications"""
    # Assets
    CURRENT_ASSET = "current_asset"
    FIXED_ASSET = "fixed_asset"
    CASH = "cash"
    ACCOUNTS_RECEIVABLE = "accounts_receivable"
    INVENTORY = "inventory"
    PREPAID_EXPENSES = "prepaid_expenses"
    SECURITY_DEPOSITS = "security_deposits"

    # Liabilities
    CURRENT_LIABILITY = "current_liability"
    LONG_TERM_LIABILITY = "long_term_liability"
    ACCOUNTS_PAYABLE = "accounts_payable"
    LOANS_PAYABLE = "loans_payable"
    MORTGAGE_PAYABLE = "mortgage_payable"
    TENANT_DEPOSITS = "tenant_deposits"

    # Equity
    OWNER_EQUITY = "owner_equity"
    RETAINED_EARNINGS = "retained_earnings"

    # Revenue
    RENTAL_INCOME = "rental_income"
    SERVICE_REVENUE = "service_revenue"
    LATE_FEES = "late_fees"
    OTHER_INCOME = "other_income"

    # Expenses
    OPERATING_EXPENSE = "operating_expense"
    COST_OF_GOODS_SOLD = "cost_of_goods_sold"
    MAINTENANCE = "maintenance"
    UTILITIES = "utilities"
    PROPERTY_TAX = "property_tax"
    INSURANCE = "insurance"
    MANAGEMENT_FEES = "management_fees"
    REPAIRS = "repairs"
    LANDSCAPING = "landscaping"
    ADVERTISING = "advertising"
    LEGAL_PROFESSIONAL = "legal_professional"
    DEPRECIATION = "depreciation"


class TransactionType(str, Enum):
    """Transaction types"""
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"
    ADJUSTMENT = "adjustment"


class TaxBenefitType(str, Enum):
    """Types of tax benefits"""
    DEPRECIATION = "depreciation"
    MORTGAGE_INTEREST = "mortgage_interest"
    PROPERTY_TAX_DEDUCTION = "property_tax_deduction"
    REPAIR_DEDUCTION = "repair_deduction"
    HOME_OFFICE_DEDUCTION = "home_office_deduction"
    TRAVEL_DEDUCTION = "travel_deduction"
    CHARITABLE_CONTRIBUTION = "charitable_contribution"
    MUNICIPAL_BONDS = "municipal_bonds"
    HSA_CONTRIBUTION = "hsa_contribution"
    RETIREMENT_CONTRIBUTION = "retirement_contribution"
    TAX_LOSS_HARVESTING = "tax_loss_harvesting"
    ESTATE_PLANNING = "estate_planning"
    SECTION_1031_EXCHANGE = "section_1031_exchange"
    COST_SEGREGATION = "cost_segregation"


class IntegrationType(str, Enum):
    """Third-party integration types"""
    QUICKBOOKS = "quickbooks"
    XERO = "xero"
    YARDI = "yardi"
    APPFOLIO = "appfolio"
    DOCUSIGN = "docusign"
    DROPBOX = "dropbox"
    BOX = "box"
    GOOGLE_CALENDAR = "google_calendar"
    OUTLOOK_CALENDAR = "outlook_calendar"


class AccountingProfile(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    Accounting Profile - Main accounting setup for a company or individual
    """

    __tablename__ = "accounting_profiles"

    # Foreign Keys
    company_id = Column(
        UUID(as_uuid=True),
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Company this accounting profile belongs to"
    )

    # Basic Information
    entity_type = Column(
        SQLEnum(AccountingEntityType),
        nullable=False,
        default=AccountingEntityType.SMALL_BUSINESS,
        comment="Type of accounting entity"
    )

    fiscal_year_end = Column(
        String(5),
        nullable=False,
        default="12-31",
        comment="Fiscal year end (MM-DD format)"
    )

    accounting_method = Column(
        String(20),
        nullable=False,
        default="accrual",
        comment="Accounting method: accrual or cash"
    )

    base_currency = Column(
        String(3),
        nullable=False,
        default="USD",
        comment="Base currency code (ISO 4217)"
    )

    # Tax Information
    tax_id = Column(
        String(50),
        nullable=True,
        comment="Tax ID / EIN"
    )

    tax_jurisdiction = Column(
        String(100),
        nullable=True,
        comment="Primary tax jurisdiction"
    )

    # Settings
    enable_multi_currency = Column(
        Boolean,
        default=False,
        comment="Enable multi-currency support"
    )

    enable_property_tracking = Column(
        Boolean,
        default=True,
        comment="Enable property-specific tracking"
    )

    enable_trust_accounting = Column(
        Boolean,
        default=False,
        comment="Enable trust accounting for security deposits"
    )

    # Configuration
    settings = Column(
        JSONB,
        nullable=True,
        comment="Additional settings and configurations"
    )

    # Relationships
    company = relationship("Company", back_populates="accounting_profile")
    chart_of_accounts = relationship(
        "ChartOfAccount",
        back_populates="accounting_profile",
        cascade="all, delete-orphan"
    )
    transactions = relationship(
        "AccountingTransaction",
        back_populates="accounting_profile",
        cascade="all, delete-orphan"
    )
    tax_benefits = relationship(
        "TaxBenefit",
        back_populates="accounting_profile",
        cascade="all, delete-orphan"
    )
    integrations = relationship(
        "IntegrationConfig",
        back_populates="accounting_profile",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<AccountingProfile(id={self.id}, company_id={self.company_id}, entity_type={self.entity_type})>"


class ChartOfAccount(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    Chart of Accounts - Individual account definitions
    """

    __tablename__ = "chart_of_accounts"
    __table_args__ = (
        Index('ix_coa_profile_type', 'accounting_profile_id', 'account_type'),
        Index('ix_coa_profile_number', 'accounting_profile_id', 'account_number'),
    )

    # Foreign Keys
    accounting_profile_id = Column(
        UUID(as_uuid=True),
        ForeignKey("accounting_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Accounting profile this account belongs to"
    )

    parent_account_id = Column(
        UUID(as_uuid=True),
        ForeignKey("chart_of_accounts.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="Parent account for sub-accounts"
    )

    # Account Information
    account_number = Column(
        String(20),
        nullable=False,
        comment="Account number (e.g., 1000, 2100)"
    )

    account_name = Column(
        String(200),
        nullable=False,
        comment="Account name"
    )

    account_type = Column(
        SQLEnum(AccountType),
        nullable=False,
        comment="Primary account type"
    )

    account_subtype = Column(
        SQLEnum(AccountSubType),
        nullable=True,
        comment="Detailed account classification"
    )

    description = Column(
        Text,
        nullable=True,
        comment="Account description and usage"
    )

    # Balance Information
    current_balance = Column(
        Numeric(15, 2),
        nullable=False,
        default=0.00,
        comment="Current account balance"
    )

    # Settings
    is_active = Column(
        Boolean,
        default=True,
        comment="Whether account is active"
    )

    is_system_account = Column(
        Boolean,
        default=False,
        comment="System-created account (cannot be deleted)"
    )

    allow_manual_entry = Column(
        Boolean,
        default=True,
        comment="Allow manual transaction entry"
    )

    # Property-specific tracking
    property_id = Column(
        UUID(as_uuid=True),
        ForeignKey("properties.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="Specific property this account tracks (optional)"
    )

    # Metadata
    notes = Column(
        Text,
        nullable=True,
        comment="Additional notes"
    )

    # Relationships
    accounting_profile = relationship("AccountingProfile", back_populates="chart_of_accounts")
    parent_account = relationship("ChartOfAccount", remote_side="ChartOfAccount.id", backref="sub_accounts")
    property = relationship("Property")
    transactions = relationship(
        "TransactionLine",
        back_populates="account",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<ChartOfAccount(id={self.id}, number={self.account_number}, name={self.account_name})>"


class AccountingTransaction(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    Accounting Transactions - Header for double-entry transactions
    """

    __tablename__ = "accounting_transactions"
    __table_args__ = (
        Index('ix_trans_profile_date', 'accounting_profile_id', 'transaction_date'),
        Index('ix_trans_profile_type', 'accounting_profile_id', 'transaction_type'),
    )

    # Foreign Keys
    accounting_profile_id = Column(
        UUID(as_uuid=True),
        ForeignKey("accounting_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Accounting profile this transaction belongs to"
    )

    property_id = Column(
        UUID(as_uuid=True),
        ForeignKey("properties.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="Related property (if applicable)"
    )

    # Transaction Information
    transaction_date = Column(
        String(10),
        nullable=False,
        comment="Transaction date (YYYY-MM-DD)"
    )

    transaction_type = Column(
        SQLEnum(TransactionType),
        nullable=False,
        comment="Type of transaction"
    )

    reference_number = Column(
        String(50),
        nullable=True,
        comment="Reference number (invoice, check, etc.)"
    )

    description = Column(
        Text,
        nullable=False,
        comment="Transaction description"
    )

    # Status
    is_posted = Column(
        Boolean,
        default=False,
        comment="Whether transaction is posted (locked)"
    )

    is_reconciled = Column(
        Boolean,
        default=False,
        comment="Whether transaction is reconciled"
    )

    # Metadata
    notes = Column(
        Text,
        nullable=True,
        comment="Additional notes"
    )

    attachments = Column(
        JSONB,
        nullable=True,
        comment="Document attachments (URLs, metadata)"
    )

    # Relationships
    accounting_profile = relationship("AccountingProfile", back_populates="transactions")
    property = relationship("Property")
    lines = relationship(
        "TransactionLine",
        back_populates="transaction",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<AccountingTransaction(id={self.id}, date={self.transaction_date}, type={self.transaction_type})>"


class TransactionLine(Base, UUIDMixin, TimestampMixin):
    """
    Transaction Lines - Individual debit/credit entries for double-entry bookkeeping
    """

    __tablename__ = "transaction_lines"
    __table_args__ = (
        Index('ix_transline_transaction', 'transaction_id'),
        Index('ix_transline_account', 'account_id'),
    )

    # Foreign Keys
    transaction_id = Column(
        UUID(as_uuid=True),
        ForeignKey("accounting_transactions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Parent transaction"
    )

    account_id = Column(
        UUID(as_uuid=True),
        ForeignKey("chart_of_accounts.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
        comment="Account this line affects"
    )

    # Line Information
    debit = Column(
        Numeric(15, 2),
        nullable=False,
        default=0.00,
        comment="Debit amount"
    )

    credit = Column(
        Numeric(15, 2),
        nullable=False,
        default=0.00,
        comment="Credit amount"
    )

    description = Column(
        Text,
        nullable=True,
        comment="Line item description"
    )

    # Relationships
    transaction = relationship("AccountingTransaction", back_populates="lines")
    account = relationship("ChartOfAccount", back_populates="transactions")

    def __repr__(self) -> str:
        return f"<TransactionLine(id={self.id}, debit={self.debit}, credit={self.credit})>"


class TaxBenefit(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    Tax Benefits - Track tax deductions, credits, and optimization strategies
    """

    __tablename__ = "tax_benefits"
    __table_args__ = (
        Index('ix_tax_profile_year', 'accounting_profile_id', 'tax_year'),
        Index('ix_tax_profile_type', 'accounting_profile_id', 'benefit_type'),
    )

    # Foreign Keys
    accounting_profile_id = Column(
        UUID(as_uuid=True),
        ForeignKey("accounting_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Accounting profile this tax benefit belongs to"
    )

    property_id = Column(
        UUID(as_uuid=True),
        ForeignKey("properties.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="Related property (if applicable)"
    )

    transaction_id = Column(
        UUID(as_uuid=True),
        ForeignKey("accounting_transactions.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="Related transaction (if applicable)"
    )

    # Tax Information
    tax_year = Column(
        String(4),
        nullable=False,
        comment="Tax year (YYYY)"
    )

    benefit_type = Column(
        SQLEnum(TaxBenefitType),
        nullable=False,
        comment="Type of tax benefit"
    )

    benefit_name = Column(
        String(200),
        nullable=False,
        comment="Name of the tax benefit"
    )

    description = Column(
        Text,
        nullable=True,
        comment="Detailed description"
    )

    # Financial Details
    benefit_amount = Column(
        Numeric(15, 2),
        nullable=False,
        comment="Estimated or actual benefit amount"
    )

    estimated_tax_savings = Column(
        Numeric(15, 2),
        nullable=True,
        comment="Estimated tax savings from this benefit"
    )

    # Status
    is_claimed = Column(
        Boolean,
        default=False,
        comment="Whether benefit has been claimed"
    )

    claim_date = Column(
        String(10),
        nullable=True,
        comment="Date benefit was claimed"
    )

    # Documentation
    documentation = Column(
        JSONB,
        nullable=True,
        comment="Supporting documentation and references"
    )

    notes = Column(
        Text,
        nullable=True,
        comment="Additional notes"
    )

    # Relationships
    accounting_profile = relationship("AccountingProfile", back_populates="tax_benefits")
    property = relationship("Property")
    transaction = relationship("AccountingTransaction")

    def __repr__(self) -> str:
        return f"<TaxBenefit(id={self.id}, year={self.tax_year}, type={self.benefit_type}, amount={self.benefit_amount})>"


class IntegrationConfig(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    Integration Configurations - Third-party service integrations
    """

    __tablename__ = "integration_configs"
    __table_args__ = (
        Index('ix_integration_profile_type', 'accounting_profile_id', 'integration_type'),
    )

    # Foreign Keys
    accounting_profile_id = Column(
        UUID(as_uuid=True),
        ForeignKey("accounting_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Accounting profile this integration belongs to"
    )

    # Integration Information
    integration_type = Column(
        SQLEnum(IntegrationType),
        nullable=False,
        comment="Type of integration"
    )

    integration_name = Column(
        String(200),
        nullable=False,
        comment="Display name for this integration"
    )

    # Connection Details
    is_enabled = Column(
        Boolean,
        default=False,
        comment="Whether integration is active"
    )

    is_connected = Column(
        Boolean,
        default=False,
        comment="Whether integration is currently connected"
    )

    last_sync_at = Column(
        String(25),
        nullable=True,
        comment="Last successful sync timestamp"
    )

    # Configuration (encrypted in production)
    api_credentials = Column(
        JSONB,
        nullable=True,
        comment="API credentials and tokens (should be encrypted)"
    )

    sync_settings = Column(
        JSONB,
        nullable=True,
        comment="Sync settings and preferences"
    )

    # Status
    status = Column(
        String(50),
        nullable=True,
        comment="Current status or error message"
    )

    notes = Column(
        Text,
        nullable=True,
        comment="Additional notes"
    )

    # Relationships
    accounting_profile = relationship("AccountingProfile", back_populates="integrations")

    def __repr__(self) -> str:
        return f"<IntegrationConfig(id={self.id}, type={self.integration_type}, enabled={self.is_enabled})>"


# Export all models
__all__ = [
    "AccountingEntityType",
    "AccountType",
    "AccountSubType",
    "TransactionType",
    "TaxBenefitType",
    "IntegrationType",
    "AccountingProfile",
    "ChartOfAccount",
    "AccountingTransaction",
    "TransactionLine",
    "TaxBenefit",
    "IntegrationConfig",
]
