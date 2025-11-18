"""
Portfolio Company Database Model

Represents a company that a fund has invested in.
"""

from datetime import date
from decimal import Decimal
from typing import List

from sqlalchemy import Column, String, Date, Numeric, Text, ARRAY, CheckConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.database import BaseModel, AuditMixin, SoftDeleteMixin


class PortfolioCompany(BaseModel, AuditMixin, SoftDeleteMixin):
    """
    Portfolio Company Model
    
    Represents a company that a fund has invested in.
    """
    
    __tablename__ = "portfolio_companies"
    __table_args__ = (
        CheckConstraint(
            "ownership_percentage >= 0 AND ownership_percentage <= 1",
            name="ownership_valid"
        ),
        CheckConstraint(
            "company_status IN ('Active', 'Exited', 'Written Off', 'On Hold')",
            name="status_valid"
        ),
    )
    
    # Foreign Keys
    fund_id = Column(
        UUID(as_uuid=True),
        ForeignKey("funds.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Reference to the fund that owns this company"
    )
    
    # Basic Information
    company_name = Column(
        String(255),
        nullable=False,
        index=True,
        comment="Company name (DBA)"
    )
    
    company_legal_name = Column(
        String(255),
        nullable=True,
        comment="Legal entity name"
    )
    
    ticker_symbol = Column(
        String(10),
        nullable=True,
        comment="Stock ticker if public"
    )
    
    website = Column(
        String(255),
        nullable=True,
        comment="Company website URL"
    )
    
    # Investment Details
    investment_date = Column(
        Date,
        nullable=False,
        index=True,
        comment="Date of investment"
    )
    
    deal_type = Column(
        String(50),
        nullable=False,
        comment="Deal type: LBO, Growth, Minority, etc."
    )
    
    # Industry Classification
    sector = Column(
        String(100),
        nullable=False,
        index=True,
        comment="Primary sector (e.g., 'Technology')"
    )
    
    industry = Column(
        String(100),
        nullable=True,
        comment="Industry within sector (e.g., 'SaaS')"
    )
    
    sub_sector = Column(
        String(100),
        nullable=True,
        comment="Sub-sector classification"
    )
    
    business_description = Column(
        Text,
        nullable=True,
        comment="Detailed business description"
    )
    
    # Location
    headquarters_city = Column(
        String(100),
        nullable=True,
        comment="Headquarters city"
    )
    
    headquarters_state = Column(
        String(100),
        nullable=True,
        comment="Headquarters state/province"
    )
    
    headquarters_country = Column(
        String(100),
        default='United States',
        nullable=False,
        comment="Headquarters country"
    )
    
    # Financial Snapshot (at entry)
    entry_revenue = Column(
        Numeric(15, 2),
        nullable=True,
        comment="Revenue at time of investment"
    )
    
    entry_ebitda = Column(
        Numeric(15, 2),
        nullable=True,
        comment="EBITDA at time of investment"
    )
    
    entry_multiple = Column(
        Numeric(10, 2),
        nullable=True,
        comment="Entry valuation multiple (EV/EBITDA)"
    )
    
    purchase_price = Column(
        Numeric(15, 2),
        nullable=True,
        comment="Total purchase price (enterprise value)"
    )
    
    equity_invested = Column(
        Numeric(15, 2),
        nullable=True,
        comment="Equity invested by fund"
    )
    
    debt_raised = Column(
        Numeric(15, 2),
        nullable=True,
        comment="Debt financing raised"
    )
    
    ownership_percentage = Column(
        Numeric(5, 4),
        nullable=True,
        comment="Ownership percentage (decimal, e.g., 0.75 for 75%)"
    )
    
    # Exit Information
    company_status = Column(
        String(50),
        default='Active',
        nullable=False,
        index=True,
        comment="Status: Active, Exited, Written Off, On Hold"
    )
    
    exit_date = Column(
        Date,
        nullable=True,
        comment="Date of exit (if applicable)"
    )
    
    exit_type = Column(
        String(50),
        nullable=True,
        comment="Exit type: IPO, Strategic Sale, Secondary, etc."
    )
    
    exit_proceeds = Column(
        Numeric(15, 2),
        nullable=True,
        comment="Gross proceeds from exit"
    )
    
    realized_moic = Column(
        Numeric(10, 2),
        nullable=True,
        comment="Realized Multiple on Invested Capital"
    )
    
    realized_irr = Column(
        Numeric(10, 4),
        nullable=True,
        comment="Realized Internal Rate of Return (decimal)"
    )
    
    # Risk & Rating
    risk_rating = Column(
        String(20),
        default='Medium',
        nullable=False,
        comment="Risk rating: Low, Medium, High"
    )
    
    internal_rating = Column(
        String(10),
        nullable=True,
        comment="Internal performance rating (A, B, C, D)"
    )
    
    # Team
    ceo_name = Column(
        String(255),
        nullable=True,
        comment="CEO name"
    )
    
    cfo_name = Column(
        String(255),
        nullable=True,
        comment="CFO name"
    )
    
    board_members = Column(
        ARRAY(String),
        nullable=True,
        comment="List of board member names"
    )
    
    # Relationships
    fund = relationship(
        "Fund",
        back_populates="portfolio_companies"
    )
    
    financial_metrics = relationship(
        "FinancialMetric",
        back_populates="company",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    kpis = relationship(
        "CompanyKPI",
        back_populates="company",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    valuations = relationship(
        "Valuation",
        back_populates="company",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    documents = relationship(
        "Document",
        back_populates="company",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    dd_items = relationship(
        "DueDiligenceItem",
        back_populates="company",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    value_creation_initiatives = relationship(
        "ValueCreationInitiative",
        back_populates="company",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )

    # Temporarily disabled - needs foreign key fix in MarketData model
    # market_data = relationship(
    #     "MarketData",
    #     back_populates="company",
    #     cascade="all, delete-orphan",
    #     lazy="dynamic"
    # )

    # Computed Properties
    @property
    def holding_period_days(self) -> int:
        """Calculate holding period in days."""
        end_date = self.exit_date if self.exit_date else date.today()
        return (end_date - self.investment_date).days
    
    @property
    def holding_period_years(self) -> float:
        """Calculate holding period in years."""
        return self.holding_period_days / 365.25
    
    @property
    def is_active(self) -> bool:
        """Check if company is active (not exited or written off)."""
        return self.company_status == 'Active' and not self.is_deleted
    
    @property
    def is_exited(self) -> bool:
        """Check if company has been exited."""
        return self.company_status == 'Exited'
    
    @property
    def entry_leverage_ratio(self) -> Decimal:
        """Calculate entry leverage ratio (Debt/Equity)."""
        if not self.equity_invested or self.equity_invested == 0:
            return Decimal(0)
        return self.debt_raised / self.equity_invested if self.debt_raised else Decimal(0)
    
    def __repr__(self) -> str:
        return f"<PortfolioCompany(name='{self.company_name}', sector='{self.sector}', status='{self.company_status}')>"
