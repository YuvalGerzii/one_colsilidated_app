"""
Audit Logging Utilities

Provides easy-to-use functions for logging user actions to the audit log.
"""

from typing import Optional, Dict, Any
from uuid import UUID
from fastapi import Request
from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog, AuditAction


def log_audit_event(
    db: Session,
    action: AuditAction,
    user_id: Optional[UUID] = None,
    user_email: Optional[str] = None,
    resource_type: Optional[str] = None,
    resource_id: Optional[str] = None,
    description: Optional[str] = None,
    changes: Optional[Dict[str, Any]] = None,
    metadata: Optional[Dict[str, Any]] = None,
    request: Optional[Request] = None,
    success: str = "success",
    error_message: Optional[str] = None,
) -> AuditLog:
    """
    Log an audit event.

    Args:
        db: Database session
        action: Type of action performed
        user_id: UUID of user who performed action
        user_email: Email of user
        resource_type: Type of resource (e.g., "property", "deal")
        resource_id: ID of the resource
        description: Human-readable description
        changes: Dict with old/new values for updates
        metadata: Additional context
        request: FastAPI Request object (for IP and user agent)
        success: "success" or "failure"
        error_message: Error message if action failed

    Returns:
        Created AuditLog instance

    Example:
        >>> log_audit_event(
        ...     db,
        ...     action=AuditAction.UPDATE,
        ...     user_id=current_user.id,
        ...     user_email=current_user.email,
        ...     resource_type="property",
        ...     resource_id=str(property.id),
        ...     description="Updated property status",
        ...     changes={"status": {"old": "active", "new": "sold"}},
        ...     request=request
        ... )
    """
    # Extract request context
    ip_address = None
    user_agent = None
    request_id = None

    if request:
        # Get client IP (handle proxies)
        ip_address = request.client.host if request.client else None

        # Check for forwarded IP (behind proxy)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            ip_address = forwarded_for.split(",")[0].strip()

        # Get user agent
        user_agent = request.headers.get("User-Agent")

        # Get request ID (if set by middleware)
        request_id = request.headers.get("X-Request-ID")

    # Create audit log entry
    audit_log = AuditLog(
        user_id=user_id,
        user_email=user_email,
        action=action,
        description=description,
        resource_type=resource_type,
        resource_id=resource_id,
        changes=changes,
        metadata=metadata,
        ip_address=ip_address,
        user_agent=user_agent,
        request_id=request_id,
        success=success,
        error_message=error_message,
    )

    db.add(audit_log)

    # Non-blocking: if audit log fails, don't fail the request
    try:
        db.commit()
    except Exception as e:
        print(f"Warning: Failed to save audit log: {e}")
        db.rollback()

    return audit_log


def log_create(
    db: Session,
    user_id: UUID,
    user_email: str,
    resource_type: str,
    resource_id: str,
    request: Optional[Request] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> AuditLog:
    """
    Log a CREATE action.

    Example:
        >>> log_create(
        ...     db, current_user.id, current_user.email,
        ...     "property", str(property.id), request
        ... )
    """
    return log_audit_event(
        db,
        action=AuditAction.CREATE,
        user_id=user_id,
        user_email=user_email,
        resource_type=resource_type,
        resource_id=resource_id,
        description=f"Created {resource_type} {resource_id}",
        metadata=metadata,
        request=request,
    )


def log_update(
    db: Session,
    user_id: UUID,
    user_email: str,
    resource_type: str,
    resource_id: str,
    changes: Dict[str, Any],
    request: Optional[Request] = None,
) -> AuditLog:
    """
    Log an UPDATE action with changes.

    Example:
        >>> log_update(
        ...     db, current_user.id, current_user.email,
        ...     "property", str(property.id),
        ...     changes={"status": {"old": "active", "new": "sold"}},
        ...     request=request
        ... )
    """
    return log_audit_event(
        db,
        action=AuditAction.UPDATE,
        user_id=user_id,
        user_email=user_email,
        resource_type=resource_type,
        resource_id=resource_id,
        description=f"Updated {resource_type} {resource_id}",
        changes=changes,
        request=request,
    )


def log_delete(
    db: Session,
    user_id: UUID,
    user_email: str,
    resource_type: str,
    resource_id: str,
    request: Optional[Request] = None,
) -> AuditLog:
    """
    Log a DELETE action.

    Example:
        >>> log_delete(
        ...     db, current_user.id, current_user.email,
        ...     "property", str(property.id), request
        ... )
    """
    return log_audit_event(
        db,
        action=AuditAction.DELETE,
        user_id=user_id,
        user_email=user_email,
        resource_type=resource_type,
        resource_id=resource_id,
        description=f"Deleted {resource_type} {resource_id}",
        request=request,
    )


def log_login(
    db: Session,
    user_id: UUID,
    user_email: str,
    request: Request,
    success: bool = True,
    error_message: Optional[str] = None,
) -> AuditLog:
    """
    Log a login attempt.

    Example:
        >>> log_login(db, user.id, user.email, request, success=True)
    """
    return log_audit_event(
        db,
        action=AuditAction.LOGIN if success else AuditAction.LOGIN_FAILED,
        user_id=user_id if success else None,
        user_email=user_email,
        description=f"Login {'successful' if success else 'failed'} for {user_email}",
        request=request,
        success="success" if success else "failure",
        error_message=error_message,
    )


def log_file_upload(
    db: Session,
    user_id: UUID,
    user_email: str,
    filename: str,
    file_size: int,
    request: Optional[Request] = None,
) -> AuditLog:
    """
    Log a file upload.

    Example:
        >>> log_file_upload(
        ...     db, current_user.id, current_user.email,
        ...     "document.pdf", 1024000, request
        ... )
    """
    return log_audit_event(
        db,
        action=AuditAction.FILE_UPLOAD,
        user_id=user_id,
        user_email=user_email,
        description=f"Uploaded file: {filename}",
        metadata={"filename": filename, "size_bytes": file_size},
        request=request,
    )


def log_permission_change(
    db: Session,
    admin_user_id: UUID,
    admin_email: str,
    target_user_id: UUID,
    target_email: str,
    changes: Dict[str, Any],
    request: Optional[Request] = None,
) -> AuditLog:
    """
    Log a permission change.

    Example:
        >>> log_permission_change(
        ...     db, admin.id, admin.email, user.id, user.email,
        ...     changes={"role": {"old": "user", "new": "admin"}},
        ...     request=request
        ... )
    """
    return log_audit_event(
        db,
        action=AuditAction.PERMISSION_CHANGE,
        user_id=admin_user_id,
        user_email=admin_email,
        resource_type="user",
        resource_id=str(target_user_id),
        description=f"Changed permissions for {target_email}",
        changes=changes,
        metadata={"target_user_id": str(target_user_id), "target_email": target_email},
        request=request,
    )


# Export all utilities
__all__ = [
    'log_audit_event',
    'log_create',
    'log_update',
    'log_delete',
    'log_login',
    'log_file_upload',
    'log_permission_change',
]
