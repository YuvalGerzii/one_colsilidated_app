"""Due Diligence Model"""
from sqlalchemy import Column, String, Text, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.database import BaseModel, AuditMixin

class DueDiligenceItem(BaseModel, AuditMixin):
    __tablename__ = "due_diligence_items"
    company_id = Column(UUID(as_uuid=True), ForeignKey("portfolio_companies.id", ondelete="CASCADE"), nullable=False, index=True)
    category = Column(String(100), nullable=False)
    item_name = Column(String(255), nullable=False)
    status = Column(String(50), default='Not Started')
    risk_level = Column(String(20))
    assigned_to = Column(String(255))
    notes = Column(Text)
    company = relationship("PortfolioCompany", back_populates="dd_items")
