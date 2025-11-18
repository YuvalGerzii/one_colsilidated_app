"""Document Model - Tracks uploaded files"""
from sqlalchemy import Column, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.models.database import BaseModel, AuditMixin

class Document(BaseModel, AuditMixin):
    __tablename__ = "documents"
    company_id = Column(UUID(as_uuid=True), ForeignKey("portfolio_companies.id", ondelete="CASCADE"), nullable=True, index=True)
    document_name = Column(String(255), nullable=False)
    document_type = Column(String(100), comment="Financial Statement, Contract, etc.")
    file_path = Column(String(500), nullable=False)
    file_size = Column(String(20))
    mime_type = Column(String(100))
    extraction_status = Column(String(50), default='Pending')
    extracted_data = Column(JSONB)
    extraction_confidence = Column(String(10))
    needs_review = Column(Boolean, default=False)
    company = relationship("PortfolioCompany", back_populates="documents")
