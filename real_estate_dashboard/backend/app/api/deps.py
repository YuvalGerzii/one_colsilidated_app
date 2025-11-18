"""
API Dependencies

Common dependencies for API endpoints (database sessions, authentication, etc.)
"""

from typing import Generator, Optional
from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session

from app.core.database import get_db
# from app.models.user import User
# from app.core.security import decode_access_token


def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> Optional[dict]:
    """
    Get current authenticated user from JWT token.

    NOTE: Authentication is not yet implemented. This is a stub.

    Args:
        authorization: Authorization header with Bearer token
        db: Database session

    Returns:
        User object if authenticated, None otherwise

    Raises:
        HTTPException: If token is invalid
    """
    # TODO: Implement authentication when User model and security module are added
    return None


def get_current_active_user(
    current_user: Optional[dict] = Depends(get_current_user)
) -> dict:
    """
    Get current active user (requires authentication).

    NOTE: Authentication is not yet implemented. This is a stub.

    Args:
        current_user: Current user from token

    Returns:
        User object

    Raises:
        HTTPException: If not authenticated or user is inactive
    """
    # TODO: Implement authentication when User model and security module are added
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication not yet implemented",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_superuser(
    current_user: dict = Depends(get_current_active_user)
) -> dict:
    """
    Get current superuser (requires superuser privileges).

    NOTE: Authentication is not yet implemented. This is a stub.

    Args:
        current_user: Current active user

    Returns:
        User object

    Raises:
        HTTPException: If user is not a superuser
    """
    # TODO: Implement authentication when User model and security module are added
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Authentication not yet implemented"
    )


# Optional authentication - returns user if authenticated, None otherwise
OptionalUser = Optional[dict]
CurrentUser = dict

__all__ = [
    "get_current_user",
    "get_current_active_user",
    "get_current_superuser",
    "OptionalUser",
    "CurrentUser",
]
