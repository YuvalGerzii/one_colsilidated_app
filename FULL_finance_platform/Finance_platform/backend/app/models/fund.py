"""
Fund Database Model

Represents a private equity fund that contains multiple portfolio companies.
"""

from datetime import date
from decimal import Decimal
from typing import List

from sqlalchemy import Column, String, Integer, Date, Numeric, ARRAY, CheckConstraint
from sqlalchemy.orm import relationship

from app.models.database import BaseModel, AuditMixin


class Fund(BaseModel, AuditMixin):
    """
    Private Equity Fund Model
    
    A fund represents a pool of capital that invests in multiple portfolio companies.
    """
    
    __tablename__ = "funds"
    __table_args__ = (
        CheckConstraint("fund_size > 0", name="fund_size_positive"),
        CheckConstraint("committed_capital <= fund_size", name="committed_lte_size"),
        CheckConstraint("drawn_capital <= committed_capital", name="drawn_lte_committed"),
    )
    
    # Basic Information
    fund_name = Column(
        String(255),
        nullable=False,
        index=True,
        comment="Name of the fund (e.g., 'Fund IV')"
    )
    
    fund_number = Column(
        Integer,
        nullable=True,
        comment="Sequential fund number (e.g., 4 for Fund IV)"
    )
    
    vintage_year = Column(
        Integer,
        nullable=False,
        index=True,
        comment="Year the fund was raised"
    )
    
    # Financial Details
    fund_size = Column(
        Numeric(15, 2),
        nullable=False,
        comment="Total fund size in USD"
    )
    
    committed_capital = Column(
        Numeric(15, 2),
        nullable=False,
        comment="Amount committed by LPs"
    )
    
    drawn_capital = Column(
        Numeric(15, 2),
        default=0,
        nullable=False,
        comment="Amount drawn from LPs"
    )
    
    distributed_capital = Column(
        Numeric(15, 2),
        default=0,
        nullable=False,
        comment="Amount distributed back to LPs"
    )
    
    # Investment Strategy
    target_irr = Column(
        Numeric(5, 4),
        nullable=True,
        comment="Target internal rate of return (decimal, e.g., 0.25 for 25%)"
    )
    
    fund_strategy = Column(
        String(100),
        nullable=True,
        comment="Investment strategy (e.g., 'Buyout', 'Growth', 'Venture')"
    )
    
    sector_focus = Column(
        ARRAY(String),
        nullable=True,
        comment="Target sectors (e.g., ['Technology', 'Healthcare'])"
    )
    
    geographic_focus = Column(
        ARRAY(String),
        nullable=True,
        comment="Target geographies (e.g., ['North America', 'Europe'])"
    )
    
    # Status & Dates
    fund_status = Column(
        String(50),
        default='Active',
        nullable=False,
        comment="Status: Active, Closed, Liquidated"
    )
    
    inception_date = Column(
        Date,
        nullable=True,
        comment="Fund inception date"
    )
    
    close_date = Column(
        Date,
        nullable=True,
        comment="First close date"
    )
    
    final_close_date = Column(
        Date,
        nullable=True,
        comment="Final close date"
    )
    
    # Relationships
    portfolio_companies = relationship(
        "PortfolioCompany",
        back_populates="fund",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    # Computed Properties
    @property
    def deployment_rate(self) -> Decimal:
        """Calculate capital deployment rate."""
        if self.committed_capital == 0:
            return Decimal(0)
        return self.drawn_capital / self.committed_capital
    
    @property
    def remaining_capital(self) -> Decimal:
        """Calculate remaining investable capital."""
        return self.committed_capital - self.drawn_capital
    
    @property
    def tvpi(self) -> Decimal:
        """Calculate Total Value to Paid-In (TVPI) multiple."""
        if self.drawn_capital == 0:
            return Decimal(0)
        # This would need to sum NAV + distributions
        # Simplified here - would need portfolio company valuations
        return self.distributed_capital / self.drawn_capital
    
    @property
    def fund_age_years(self) -> int:
        """Calculate fund age in years."""
        if not self.inception_date:
            return 0
        from datetime import date
        return (date.today() - self.inception_date).days // 365
    
    def __repr__(self) -> str:
        return f"<Fund(name='{self.fund_name}', vintage={self.vintage_year}, size=${self.fund_size:,.0f})>"
