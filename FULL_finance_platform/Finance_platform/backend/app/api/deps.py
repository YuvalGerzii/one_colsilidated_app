"""
API Dependencies

Common dependencies for API endpoints (database sessions, authentication, etc.)
"""

from typing import Generator, Optional
from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.core.security import decode_access_token


def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Get current authenticated user from JWT token.
    
    Args:
        authorization: Authorization header with Bearer token
        db: Database session
        
    Returns:
        User object if authenticated, None otherwise
        
    Raises:
        HTTPException: If token is invalid
    """
    if not authorization:
        return None
    
    try:
        # Extract token from "Bearer <token>"
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            return None
        
        # Decode token
        payload = decode_access_token(token)
        if not payload:
            return None
        
        user_id = payload.get("sub")
        if not user_id:
            return None
        
        # Get user from database
        user = db.query(User).filter(User.id == user_id).first()
        return user
        
    except Exception:
        return None


def get_current_active_user(
    current_user: Optional[User] = Depends(get_current_user)
) -> User:
    """
    Get current active user (requires authentication).
    
    Args:
        current_user: Current user from token
        
    Returns:
        User object
        
    Raises:
        HTTPException: If not authenticated or user is inactive
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    return current_user


def get_current_superuser(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """
    Get current superuser (requires superuser privileges).
    
    Args:
        current_user: Current active user
        
    Returns:
        User object
        
    Raises:
        HTTPException: If user is not a superuser
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough privileges"
        )
    
    return current_user


# Optional authentication - returns user if authenticated, None otherwise
OptionalUser = Optional[User]
CurrentUser = User

__all__ = [
    "get_current_user",
    "get_current_active_user",
    "get_current_superuser",
    "OptionalUser",
    "CurrentUser",
]
