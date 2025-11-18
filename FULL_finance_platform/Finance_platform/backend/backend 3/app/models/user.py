"""User Model"""
from sqlalchemy import Column, String, Boolean
from app.models.database import BaseModel

class User(BaseModel):
    __tablename__ = "users"
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255))
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
