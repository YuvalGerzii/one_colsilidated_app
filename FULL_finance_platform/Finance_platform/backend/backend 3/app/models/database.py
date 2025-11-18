"""
Base Database Models and Mixins

This module contains base classes and mixins used by all database models.
"""

import uuid
from datetime import datetime
from typing import Any, Dict

from sqlalchemy import Column, DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr

from app.core.database import Base


class UUIDMixin:
    """Mixin to add UUID primary key to models."""
    
    @declared_attr
    def id(cls):
        """UUID primary key column."""
        return Column(
            UUID(as_uuid=True),
            primary_key=True,
            default=uuid.uuid4,
            unique=True,
            nullable=False
        )


class TimestampMixin:
    """Mixin to add created_at and updated_at timestamps to models."""
    
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Record creation timestamp"
    )
    
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Record last update timestamp"
    )


class AuditMixin:
    """Mixin to add audit fields (created_by, updated_by) to models."""
    
    @declared_attr
    def created_by(cls):
        """User ID who created the record."""
        return Column(
            UUID(as_uuid=True),
            nullable=True,
            comment="User who created this record"
        )
    
    @declared_attr
    def updated_by(cls):
        """User ID who last updated the record."""
        return Column(
            UUID(as_uuid=True),
            nullable=True,
            comment="User who last updated this record"
        )


class SoftDeleteMixin:
    """Mixin to add soft delete capability to models."""
    
    deleted_at = Column(
        DateTime(timezone=True),
        nullable=True,
        comment="Record deletion timestamp (NULL if not deleted)"
    )
    
    deleted_by = Column(
        UUID(as_uuid=True),
        nullable=True,
        comment="User who deleted this record"
    )
    
    @property
    def is_deleted(self) -> bool:
        """Check if record is soft-deleted."""
        return self.deleted_at is not None
    
    def soft_delete(self, user_id: uuid.UUID = None):
        """Soft delete the record."""
        self.deleted_at = datetime.utcnow()
        self.deleted_by = user_id
    
    def restore(self):
        """Restore a soft-deleted record."""
        self.deleted_at = None
        self.deleted_by = None


class BaseModel(Base, UUIDMixin, TimestampMixin):
    """
    Base model class that all models should inherit from.
    
    Provides:
    - UUID primary key (id)
    - Timestamps (created_at, updated_at)
    - Common utility methods
    """
    
    __abstract__ = True
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert model instance to dictionary.
        
        Returns:
            Dict containing all column values
        """
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
    
    def update_from_dict(self, data: Dict[str, Any]) -> None:
        """
        Update model instance from dictionary.
        
        Args:
            data: Dictionary of field names and values
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def __repr__(self) -> str:
        """String representation of model instance."""
        return f"<{self.__class__.__name__}(id={self.id})>"


# Export all
__all__ = [
    "Base",
    "UUIDMixin",
    "TimestampMixin",
    "AuditMixin",
    "SoftDeleteMixin",
    "BaseModel",
]
