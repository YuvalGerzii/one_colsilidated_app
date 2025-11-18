"""Value Creation Model"""
from sqlalchemy import Column, String, Date, Numeric, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.database import BaseModel, AuditMixin

class ValueCreationInitiative(BaseModel, AuditMixin):
    __tablename__ = "value_creation_initiatives"
    company_id = Column(UUID(as_uuid=True), ForeignKey("portfolio_companies.id", ondelete="CASCADE"), nullable=False, index=True)
    initiative_name = Column(String(255), nullable=False)
    category = Column(String(100))
    status = Column(String(50), default='Planned')
    target_value_impact = Column(Numeric(15, 2))
    start_date = Column(Date)
    completion_date = Column(Date)
    owner = Column(String(255))
    description = Column(Text)
    company = relationship("PortfolioCompany", back_populates="value_creation_initiatives")
