"""
Authentication API Endpoints

Handles user registration, login, token refresh, and profile management.
"""

from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session
import uuid

from app.core.database import get_db
from app.core.auth import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_current_user,
    get_current_active_user
)
from app.models.user import User
from app.models.company import Company

router = APIRouter()


# ===== Request/Response Schemas =====

class UserRegister(BaseModel):
    """
    User registration request.

    Can either join an existing company (via company_id) or create a new one (via company_name).
    """
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company_id: Optional[str] = Field(None, description="UUID of existing company to join")
    company_name: Optional[str] = Field(None, description="Name for new company to create")


class UserLogin(BaseModel):
    """User login request."""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Authentication token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: dict


class TokenRefresh(BaseModel):
    """Token refresh request."""
    refresh_token: str


class UserProfile(BaseModel):
    """User profile response."""
    id: str
    email: str
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    company_name: Optional[str]
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login: Optional[datetime]


class UserProfileUpdate(BaseModel):
    """User profile update request."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company_name: Optional[str] = None


class PasswordChange(BaseModel):
    """Password change request."""
    current_password: str
    new_password: str = Field(..., min_length=8)


# ===== Authentication Endpoints =====

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user account.

    Supports two company association modes:
    1. Join existing company: Provide company_id
    2. Create new company: Provide company_name (will auto-create company)

    Returns access and refresh tokens upon successful registration.
    """
    # Check if email already exists
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Check if username already exists
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    # Handle company association
    company_id_to_set = None
    company_name_to_set = None

    if user_data.company_id:
        # Option 1: Join existing company
        try:
            company_uuid = uuid.UUID(user_data.company_id)
            company = db.query(Company).filter(Company.id == company_uuid).first()
            if not company:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Company not found"
                )
            company_id_to_set = company.id
            company_name_to_set = company.name
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid company_id format"
            )

    elif user_data.company_name:
        # Option 2: Create new company or join existing by name
        existing_company = db.query(Company).filter(
            Company.name == user_data.company_name
        ).first()

        if existing_company:
            # Company with this name already exists, join it
            company_id_to_set = existing_company.id
            company_name_to_set = existing_company.name
        else:
            # Create new company
            new_company = Company(
                name=user_data.company_name,
                details=f"Company created during registration for {user_data.email}"
            )
            db.add(new_company)
            db.flush()  # Get the ID without committing yet
            company_id_to_set = new_company.id
            company_name_to_set = new_company.name

    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        company_id=company_id_to_set,
        company_name=company_name_to_set,  # Keep for backward compatibility
        is_active=True,
        is_verified=False,  # Can implement email verification later
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create tokens
    token_data = {"sub": str(new_user.id), "email": new_user.email}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": new_user.to_dict()
    }


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Login with email and password.

    Returns access and refresh tokens upon successful authentication.
    """
    user = authenticate_user(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated"
        )

    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()

    # Create tokens
    token_data = {"sub": str(user.id), "email": user.email}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": user.to_dict()
    }


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(token_data: TokenRefresh, db: Session = Depends(get_db)):
    """
    Refresh access token using a refresh token.
    """
    try:
        payload = decode_token(token_data.refresh_token)

        # Verify it's a refresh token
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )

        # Create new tokens
        new_token_data = {"sub": str(user.id), "email": user.email}
        new_access_token = create_access_token(new_token_data)
        new_refresh_token = create_refresh_token(new_token_data)

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
            "user": user.to_dict()
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """
    Logout (client-side token removal).

    Since we're using stateless JWT tokens, logout is handled client-side
    by removing the tokens. This endpoint confirms the user is authenticated.
    """
    return {"message": "Successfully logged out"}


# ===== Profile Endpoints =====

@router.get("/me", response_model=UserProfile)
async def get_current_user_profile(current_user: User = Depends(get_current_active_user)):
    """
    Get current user's profile information.
    """
    return current_user.to_dict()


@router.put("/me", response_model=UserProfile)
async def update_profile(
    profile_update: UserProfileUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update current user's profile.
    """
    update_data = profile_update.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(current_user, field, value)

    db.commit()
    db.refresh(current_user)

    return current_user.to_dict()


@router.post("/change-password")
async def change_password(
    password_change: PasswordChange,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Change user's password.
    """
    # Verify current password
    user = authenticate_user(db, current_user.email, password_change.current_password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password"
        )

    # Update password
    current_user.hashed_password = get_password_hash(password_change.new_password)
    db.commit()

    return {"message": "Password updated successfully"}


@router.delete("/me")
async def delete_account(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete current user's account (soft delete - deactivate).
    """
    current_user.is_active = False
    db.commit()

    return {"message": "Account deactivated successfully"}
