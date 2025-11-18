"""
Authentication utilities for JWT tokens and password hashing.
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.settings import settings
from app.core.database import get_db
from app.models.user import User
from app.models.company import Company

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP Bearer token scheme
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.

    Args:
        data: Data to encode in the token (usually user_id, email)
        expires_delta: Token expiration time (defaults to config value)

    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """
    Create a JWT refresh token (longer expiration).

    Args:
        data: Data to encode in the token

    Returns:
        Encoded JWT refresh token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> dict:
    """
    Decode and verify a JWT token.

    Args:
        token: JWT token to decode

    Returns:
        Decoded token payload

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Get the current authenticated user from the JWT token.

    This is a FastAPI dependency that can be used in route handlers.

    Usage:
        @app.get("/protected")
        def protected_route(user: User = Depends(get_current_user)):
            return {"user_id": user.id}

    Args:
        credentials: HTTP Authorization header with Bearer token
        db: Database session

    Returns:
        Current authenticated User

    Raises:
        HTTPException: If authentication fails
    """
    token = credentials.credentials
    payload = decode_token(token)

    # Verify it's an access token
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )

    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Get current user and verify they are active.

    This is a convenience dependency.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_superuser(current_user: User = Depends(get_current_user)) -> User:
    """
    Get current user and verify they are a superuser.

    Use this for admin-only endpoints.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough privileges",
        )
    return current_user


def get_current_user_with_company(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> tuple[User, Optional[Company]]:
    """
    Get current user along with their associated company.

    This is used for multi-company/multi-tenant endpoints where you need
    to enforce company-level data isolation.

    Usage:
        @app.get("/company-data")
        def get_company_data(
            user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company)
        ):
            user, company = user_company
            if not company:
                raise HTTPException(status_code=400, detail="User not associated with a company")
            # Use company.id to filter data
            return {"company_id": company.id}

    Args:
        current_user: Current authenticated user
        db: Database session

    Returns:
        Tuple of (User, Optional[Company])
    """
    # If user has company_id, fetch the company
    if current_user.company_id:
        company = db.query(Company).filter(Company.id == current_user.company_id).first()
        return (current_user, company)

    # User not associated with any company
    return (current_user, None)


def require_company_access(
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company)
) -> tuple[User, Company]:
    """
    Require that the current user is associated with a company.

    This is a stricter version of get_current_user_with_company that raises
    an error if the user doesn't have a company.

    Usage:
        @app.get("/company-only-data")
        def get_data(user_company: tuple[User, Company] = Depends(require_company_access)):
            user, company = user_company
            # company is guaranteed to exist
            return {"company_id": company.id}

    Args:
        user_company: Tuple from get_current_user_with_company

    Returns:
        Tuple of (User, Company) - company is guaranteed to exist

    Raises:
        HTTPException: If user is not associated with a company
    """
    user, company = user_company

    if not company:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must be associated with a company to access this resource",
        )

    return (user, company)


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Authenticate a user by email and password.

    Args:
        db: Database session
        email: User email
        password: Plain text password

    Returns:
        User if authentication succeeds, None otherwise
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
