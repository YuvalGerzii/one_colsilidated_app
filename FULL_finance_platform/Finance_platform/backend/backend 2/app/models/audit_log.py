"""Audit Log Model"""
from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.models.database import BaseModel

class AuditLog(BaseModel):
    __tablename__ = "audit_logs"
    user_id = Column(UUID(as_uuid=True), index=True)
    action = Column(String(100), nullable=False)
    entity_type = Column(String(100))
    entity_id = Column(UUID(as_uuid=True))
    changes = Column(JSONB)
    ip_address = Column(String(50))
    user_agent = Column(Text)
