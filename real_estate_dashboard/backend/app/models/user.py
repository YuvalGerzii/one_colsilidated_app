"""User authentication and authorization models."""

from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from app.models.database import BaseModel


class User(BaseModel):
    """
    User model for authentication and multi-tenancy.

    All user data is isolated by user_id for multi-tenant support.
    """

    __tablename__ = "users"

    # Authentication
    email = Column(String(255), unique=True, nullable=False, index=True, comment="User email (login)")
    username = Column(String(100), unique=True, nullable=False, index=True, comment="Username")
    hashed_password = Column(String(255), nullable=False, comment="Bcrypt hashed password")

    # Profile
    first_name = Column(String(100), nullable=True, comment="First name")
    last_name = Column(String(100), nullable=True, comment="Last name")
    company_name = Column(String(255), nullable=True, comment="[DEPRECATED] Use company_id instead")

    # Company Association (Multi-Tenancy)
    company_id = Column(
        UUID(as_uuid=True),
        ForeignKey("companies.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="Company/organization this user belongs to"
    )

    # Status
    is_active = Column(Boolean, default=True, nullable=False, comment="Account is active")
    is_verified = Column(Boolean, default=False, nullable=False, comment="Email verified")
    is_superuser = Column(Boolean, default=False, nullable=False, comment="Admin privileges")

    # Timestamps
    last_login = Column(DateTime, nullable=True, comment="Last login timestamp")
    email_verified_at = Column(DateTime, nullable=True, comment="Email verification timestamp")

    # Relationships
    company = relationship(
        "Company",
        foreign_keys=[company_id],
        backref="users",
        doc="Company this user belongs to"
    )

    # Additional relationships (will be added as we create other models)
    # saved_calculations = relationship("SavedCalculation", back_populates="user", cascade="all, delete-orphan")
    # properties = relationship("Property", back_populates="user", cascade="all, delete-orphan")
    # deals = relationship("Deal", back_populates="user", cascade="all, delete-orphan")

    def to_dict(self):
        """Convert to dictionary (exclude password)."""
        data = super().to_dict()
        data.pop('hashed_password', None)  # Never expose password hash
        return data

    @property
    def full_name(self) -> str:
        """Get full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
