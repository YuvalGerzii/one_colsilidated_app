"""
Users API Endpoints - User management and authentication

Supports user CRUD operations, role management, and profile updates.
"""

from typing import List, Optional
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field, EmailStr
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from passlib.context import CryptContext

from app.api.deps import get_db
from app.models.user import User


router = APIRouter()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Pydantic Schemas

class UserBase(BaseModel):
    """Base user schema with common fields."""
    email: EmailStr = Field(..., description="User email address")
    username: str = Field(..., min_length=3, max_length=100, description="Username")
    first_name: Optional[str] = Field(None, max_length=100, description="First name")
    last_name: Optional[str] = Field(None, max_length=100, description="Last name")
    company_id: Optional[UUID] = Field(None, description="Associated company ID")
    is_active: bool = Field(True, description="User account is active")
    is_verified: bool = Field(False, description="Email is verified")
    is_superuser: bool = Field(False, description="User has admin privileges")


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str = Field(..., min_length=8, description="User password (min 8 characters)")


class UserUpdate(BaseModel):
    """Schema for updating an existing user."""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company_id: Optional[UUID] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    is_superuser: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=8, description="New password")


class UserResponse(BaseModel):
    """Schema for user response (excludes password)."""
    id: UUID
    email: str
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    company_id: Optional[UUID]
    is_active: bool
    is_verified: bool
    is_superuser: bool
    last_login: Optional[datetime]
    email_verified_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserSummary(BaseModel):
    """Lightweight user summary."""
    id: UUID
    email: str
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True


class PasswordChange(BaseModel):
    """Schema for changing password."""
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, description="New password (min 8 characters)")


# Helper Functions

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


# API Endpoints

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new user account.

    - **email**: Valid email address (must be unique)
    - **username**: Username (must be unique)
    - **password**: Password (min 8 characters)
    - **company_id**: Optional company association
    """
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Check if username already exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    # Create new user with hashed password
    user_dict = user_data.model_dump(exclude={'password'})
    user_dict['hashed_password'] = hash_password(user_data.password)

    user = User(**user_dict)
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.get("/", response_model=List[UserResponse])
async def list_users(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records"),
    company_id: Optional[UUID] = Query(None, description="Filter by company"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    is_superuser: Optional[bool] = Query(None, description="Filter by admin status"),
    search: Optional[str] = Query(None, description="Search by email, username, or name"),
    db: Session = Depends(get_db),
):
    """
    List all users with optional filtering.

    Filters:
    - company_id: Filter by associated company
    - is_active: Filter by active/inactive status
    - is_superuser: Filter by admin status
    - search: Search across email, username, first_name, last_name
    """
    query = db.query(User)

    # Apply filters
    if company_id:
        query = query.filter(User.company_id == company_id)

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    if is_superuser is not None:
        query = query.filter(User.is_superuser == is_superuser)

    if search:
        search_filter = or_(
            User.email.ilike(f"%{search}%"),
            User.username.ilike(f"%{search}%"),
            User.first_name.ilike(f"%{search}%"),
            User.last_name.ilike(f"%{search}%"),
        )
        query = query.filter(search_filter)

    # Order by created date (newest first)
    users = query.order_by(User.created_at.desc()).offset(skip).limit(limit).all()

    return users


@router.get("/summary", response_model=List[UserSummary])
async def list_users_summary(
    db: Session = Depends(get_db),
):
    """
    Get lightweight list of all users for dropdown/selector UI.

    Returns only essential fields for optimal performance.
    """
    users = db.query(User).order_by(User.username).all()
    return users


@router.get("/stats")
async def get_user_statistics(
    db: Session = Depends(get_db),
):
    """
    Get user statistics.

    Returns counts by status and role.
    """
    # Count by active status
    active_count = db.query(User).filter(User.is_active == True).count()
    inactive_count = db.query(User).filter(User.is_active == False).count()

    # Count by role
    admin_count = db.query(User).filter(User.is_superuser == True).count()
    regular_count = db.query(User).filter(User.is_superuser == False).count()

    # Count by verification status
    verified_count = db.query(User).filter(User.is_verified == True).count()
    unverified_count = db.query(User).filter(User.is_verified == False).count()

    # Count by company
    company_counts = db.query(
        User.company_id,
        func.count(User.id).label('count')
    ).group_by(User.company_id).all()

    return {
        "total_users": db.query(User).count(),
        "active_users": active_count,
        "inactive_users": inactive_count,
        "admin_users": admin_count,
        "regular_users": regular_count,
        "verified_users": verified_count,
        "unverified_users": unverified_count,
        "by_company": {str(c): count for c, count in company_counts if c is not None},
    }


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Get a specific user by ID.

    - **user_id**: UUID of the user to retrieve
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )

    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an existing user.

    - **user_id**: UUID of the user to update
    - Only provided fields will be updated
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )

    # Check for email uniqueness if email is being changed
    if user_data.email and user_data.email != user.email:
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

    # Check for username uniqueness if username is being changed
    if user_data.username and user_data.username != user.username:
        existing_user = db.query(User).filter(User.username == user_data.username).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )

    # Update user fields
    update_data = user_data.model_dump(exclude_unset=True)

    # Handle password update separately
    if 'password' in update_data:
        update_data['hashed_password'] = hash_password(update_data.pop('password'))

    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Delete a user.

    - **user_id**: UUID of the user to delete
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )

    db.delete(user)
    db.commit()

    return None


@router.patch("/{user_id}/activate")
async def activate_user(
    user_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Activate a user account.

    - **user_id**: UUID of the user to activate
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )

    user.is_active = True
    db.commit()
    db.refresh(user)

    return {"id": user.id, "is_active": user.is_active, "message": "User activated successfully"}


@router.patch("/{user_id}/deactivate")
async def deactivate_user(
    user_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Deactivate a user account.

    - **user_id**: UUID of the user to deactivate
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )

    user.is_active = False
    db.commit()
    db.refresh(user)

    return {"id": user.id, "is_active": user.is_active, "message": "User deactivated successfully"}


@router.patch("/{user_id}/verify-email")
async def verify_email(
    user_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Mark user email as verified.

    - **user_id**: UUID of the user
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )

    user.is_verified = True
    user.email_verified_at = datetime.utcnow()
    db.commit()
    db.refresh(user)

    return {"id": user.id, "is_verified": user.is_verified, "message": "Email verified successfully"}


@router.patch("/{user_id}/make-admin")
async def make_admin(
    user_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Grant admin privileges to a user.

    - **user_id**: UUID of the user
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )

    user.is_superuser = True
    db.commit()
    db.refresh(user)

    return {"id": user.id, "is_superuser": user.is_superuser, "message": "Admin privileges granted"}


@router.patch("/{user_id}/remove-admin")
async def remove_admin(
    user_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Remove admin privileges from a user.

    - **user_id**: UUID of the user
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )

    user.is_superuser = False
    db.commit()
    db.refresh(user)

    return {"id": user.id, "is_superuser": user.is_superuser, "message": "Admin privileges removed"}


@router.post("/{user_id}/change-password")
async def change_password(
    user_id: UUID,
    password_data: PasswordChange,
    db: Session = Depends(get_db),
):
    """
    Change user password.

    - **user_id**: UUID of the user
    - **current_password**: Current password for verification
    - **new_password**: New password
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )

    # Verify current password
    if not verify_password(password_data.current_password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )

    # Update to new password
    user.hashed_password = hash_password(password_data.new_password)
    db.commit()
    db.refresh(user)

    return {"message": "Password changed successfully"}
