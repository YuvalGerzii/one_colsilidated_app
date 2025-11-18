"""Valuation Model - Stores company valuations"""
from sqlalchemy import Column, String, Date, Numeric, Text, JSONB, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.database import BaseModel, AuditMixin

class Valuation(BaseModel, AuditMixin):
    __tablename__ = "valuations"
    company_id = Column(UUID(as_uuid=True), ForeignKey("portfolio_companies.id", ondelete="CASCADE"), nullable=False, index=True)
    valuation_date = Column(Date, nullable=False, index=True)
    valuation_method = Column(String(50), comment="DCF, Market Comp, Transaction, etc.")
    enterprise_value = Column(Numeric(15, 2))
    equity_value = Column(Numeric(15, 2))
    valuation_assumptions = Column(JSONB, comment="JSON of assumptions")
    notes = Column(Text)
    company = relationship("PortfolioCompany", back_populates="valuations")
