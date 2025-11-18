"""
Audit Log Model

Tracks all user actions for security, compliance, and troubleshooting purposes.
"""

import enum
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Enum as SQLEnum, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.core.database import Base


class AuditAction(str, enum.Enum):
    """Types of auditable actions."""
    # Authentication
    LOGIN = "login"
    LOGOUT = "logout"
    LOGIN_FAILED = "login_failed"
    PASSWORD_CHANGE = "password_change"
    PASSWORD_RESET = "password_reset"

    # CRUD Operations
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"

    # File Operations
    FILE_UPLOAD = "file_upload"
    FILE_DOWNLOAD = "file_download"
    FILE_DELETE = "file_delete"

    # Sensitive Operations
    PERMISSION_CHANGE = "permission_change"
    USER_CREATE = "user_create"
    USER_DELETE = "user_delete"
    DATA_EXPORT = "data_export"

    # System Events
    API_KEY_GENERATED = "api_key_generated"
    API_KEY_REVOKED = "api_key_revoked"
    SETTINGS_CHANGE = "settings_change"


class AuditLog(Base):
    """
    Audit Log Model

    Records all significant user actions for security auditing,
    compliance tracking, and troubleshooting.

    Example audit log entry:
        {
            "user_id": "uuid",
            "action": "update",
            "resource_type": "property",
            "resource_id": "property-uuid",
            "changes": {"status": {"old": "active", "new": "sold"}},
            "ip_address": "192.168.1.1",
            "user_agent": "Mozilla/5.0...",
            "timestamp": "2025-11-10T12:00:00Z"
        }
    """
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Who performed the action
    user_id = Column(UUID(as_uuid=True), nullable=True, index=True,
                     comment="User who performed the action (null for system actions)")
    user_email = Column(String(255), nullable=True, index=True,
                       comment="Email of user (denormalized for faster queries)")

    # What action was performed
    action = Column(SQLEnum(AuditAction), nullable=False, index=True,
                   comment="Type of action performed")
    description = Column(Text, nullable=True,
                        comment="Human-readable description of action")

    # What resource was affected
    resource_type = Column(String(100), nullable=True, index=True,
                          comment="Type of resource (e.g., 'property', 'deal', 'user')")
    resource_id = Column(String(255), nullable=True, index=True,
                        comment="ID of the affected resource")

    # Details about the change
    changes = Column(JSON, nullable=True,
                    comment="JSON object with old/new values for updates")
    extra_metadata = Column(JSON, nullable=True,
                     comment="Additional context (e.g., query parameters, file size)")

    # Request context
    ip_address = Column(String(45), nullable=True, index=True,
                       comment="IP address of the request (supports IPv6)")
    user_agent = Column(Text, nullable=True,
                       comment="User agent string from request")
    request_id = Column(String(255), nullable=True, index=True,
                       comment="Unique request ID for correlating logs")

    # Timing
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow, index=True,
                      comment="When the action occurred")

    # Status
    success = Column(String(10), nullable=False, default="success",
                    comment="Whether action succeeded (success/failure)")
    error_message = Column(Text, nullable=True,
                          comment="Error message if action failed")

    def __repr__(self):
        return (f"<AuditLog(id={self.id}, user={self.user_email}, "
                f"action={self.action}, resource={self.resource_type}:{self.resource_id})>")

    def to_dict(self):
        """Convert audit log to dictionary."""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id) if self.user_id else None,
            "user_email": self.user_email,
            "action": self.action.value if self.action else None,
            "description": self.description,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "changes": self.changes,
            "metadata": self.metadata,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "request_id": self.request_id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "success": self.success,
            "error_message": self.error_message,
        }
