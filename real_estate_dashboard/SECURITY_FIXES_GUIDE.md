# Security Fixes Implementation Guide

This guide provides step-by-step instructions to fix all critical and high-severity security vulnerabilities identified in the security audit.

---

## Phase 1: Critical Fixes (Must Complete Before Production)

### Fix 1: Implement Authentication on All Endpoints

**Problem:** 95% of API endpoints lack authentication
**Impact:** Complete data exposure
**Time to Fix:** 2-3 days

#### Step 1: Update Settings to Require SECRET_KEY

```python
# File: backend/app/settings.py
# Change lines 62-65 from:
SECRET_KEY: str = Field(
    default="your-secret-key-replace-in-production",
    description="Secret key for JWT encoding"
)

# To:
SECRET_KEY: str = Field(
    ...,  # Required, no default
    min_length=32,
    description="Secret key for JWT encoding (min 32 chars, use: python -c 'import secrets; print(secrets.token_urlsafe(32))')"
)

@field_validator("SECRET_KEY")
@classmethod
def validate_secret_key(cls, v, info):
    if info.data.get("ENVIRONMENT") == "production":
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters in production")
        if "your-secret-key" in v.lower():
            raise ValueError("Default SECRET_KEY not allowed in production")
    return v
```

#### Step 2: Fix Authentication Dependencies

```python
# File: backend/app/core/auth.py
# Update get_current_user to actually work:

from datetime import datetime, timezone, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.settings import settings

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Validate JWT token and return current user.
    Raises 401 if token is invalid or user not found.
    """
    token = credentials.credentials

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception

    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Verify user is active."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def require_superuser(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """Require superuser privileges."""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Insufficient privileges. Superuser required."
        )
    return current_user
```

#### Step 3: Add Authentication to All Endpoints

Create a helper script to add authentication:

```python
# File: backend/add_auth_to_endpoints.py
"""
Script to add authentication to all endpoints.
Run: python add_auth_to_endpoints.py
"""

import os
import re
from pathlib import Path

ENDPOINTS_DIR = Path("app/api/v1/endpoints")
EXCLUDED_FILES = {"health.py", "auth.py", "__init__.py"}

def add_auth_import(content: str) -> str:
    """Add auth import if not present."""
    if "from app.core.auth import" in content:
        return content

    # Add after other imports
    import_line = "from app.core.auth import get_current_active_user\n"

    # Find last import
    lines = content.split('\n')
    last_import_idx = 0
    for i, line in enumerate(lines):
        if line.startswith('from ') or line.startswith('import '):
            last_import_idx = i

    lines.insert(last_import_idx + 1, import_line)
    return '\n'.join(lines)

def add_auth_dependency(content: str) -> str:
    """Add current_user dependency to endpoints."""

    # Pattern: function with db: Session = Depends(get_db) but no current_user
    pattern = r'(async def \w+\([^)]*)(db: Session = Depends\(get_db\))'

    def replacement(match):
        params = match.group(1)
        db_param = match.group(2)

        # Check if current_user already exists
        if 'current_user' in params:
            return match.group(0)

        # Add current_user before db
        return f'{params}current_user: User = Depends(get_current_active_user),\n    {db_param}'

    return re.sub(pattern, replacement, content)

def process_file(file_path: Path):
    """Process a single endpoint file."""
    print(f"Processing {file_path.name}...")

    with open(file_path, 'r') as f:
        content = f.read()

    # Add imports
    content = add_auth_import(content)

    # Add dependencies
    content = add_auth_dependency(content)

    with open(file_path, 'w') as f:
        f.write(content)

    print(f"  ✅ Updated {file_path.name}")

def main():
    for file_path in ENDPOINTS_DIR.glob("*.py"):
        if file_path.name in EXCLUDED_FILES:
            print(f"Skipping {file_path.name}")
            continue

        process_file(file_path)

    print("\n✅ All endpoints updated!")
    print("\n⚠️  IMPORTANT: Review all changes manually!")
    print("Some endpoints may need special handling (public endpoints, etc.)")

if __name__ == "__main__":
    main()
```

#### Step 4: Manual Review Required

After running the script, manually review these files:
- Public endpoints that should NOT require auth
- Webhook endpoints
- Health check endpoints

---

### Fix 2: Implement Multi-Tenancy Enforcement

**Problem:** Users can access other users' data
**Impact:** Data breach between tenants
**Time to Fix:** 3-4 days

#### Step 1: Add Company Access Control to User Model

```python
# File: backend/app/models/user.py
# Add to User class:

from sqlalchemy.dialects.postgresql import ARRAY
from typing import List

class User(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    # ... existing fields ...

    # Multi-tenancy support
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=True, index=True)
    accessible_company_ids = Column(ARRAY(UUID(as_uuid=True)), default=list)

    # Relationships
    company = relationship("Company", foreign_keys=[company_id])

    def can_access_company(self, company_id: UUID) -> bool:
        """Check if user can access a company."""
        if self.is_superuser:
            return True
        return company_id in self.accessible_company_ids or company_id == self.company_id
```

#### Step 2: Create Access Control Helper

```python
# File: backend/app/core/access_control.py
"""
Multi-tenancy and access control helpers.
"""

from uuid import UUID
from typing import Optional, List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session, Query
from app.models.user import User

def enforce_company_access(
    user: User,
    company_id: Optional[UUID],
    resource_name: str = "resource"
) -> UUID:
    """
    Enforce user can access the specified company.
    Raises 403 if access denied.
    Returns company_id if valid.
    """
    if company_id is None:
        raise HTTPException(
            status_code=400,
            detail=f"company_id required for {resource_name}"
        )

    if not user.can_access_company(company_id):
        raise HTTPException(
            status_code=403,
            detail=f"Access denied to {resource_name} for this company"
        )

    return company_id

def filter_by_company_access(
    query: Query,
    user: User,
    company_id_column,
    company_id: Optional[UUID] = None
) -> Query:
    """
    Filter query by user's accessible companies.

    Args:
        query: SQLAlchemy query object
        user: Current user
        company_id_column: Column to filter on (e.g., Property.company_id)
        company_id: Optional specific company to filter for

    Returns:
        Filtered query
    """
    if user.is_superuser:
        if company_id:
            return query.filter(company_id_column == company_id)
        return query  # Superuser sees all

    # Regular user: filter by accessible companies
    accessible_ids = user.accessible_company_ids + [user.company_id]

    if company_id:
        if company_id not in accessible_ids:
            # Return empty result
            return query.filter(False)
        return query.filter(company_id_column == company_id)

    return query.filter(company_id_column.in_(accessible_ids))

def get_user_companies(user: User) -> List[UUID]:
    """Get list of company IDs user can access."""
    if user.is_superuser:
        return []  # Empty means "all"
    return user.accessible_company_ids + [user.company_id]
```

#### Step 3: Apply Access Control to Endpoints

Example for property_management.py:

```python
# File: backend/app/api/v1/endpoints/property_management.py

from app.core.access_control import filter_by_company_access, enforce_company_access

@router.get("/properties")
async def list_properties(
    company_id: Optional[UUID] = Query(None),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List properties user has access to."""
    query = db.query(Property).filter(Property.deleted_at.is_(None))

    # Apply company access filter
    query = filter_by_company_access(
        query,
        current_user,
        Property.company_id,
        company_id
    )

    properties = query.all()
    return [p.to_dict() for p in properties]

@router.get("/properties/{property_id}")
async def get_property(
    property_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get single property."""
    property_obj = db.query(Property).filter(
        Property.id == property_id,
        Property.deleted_at.is_(None)
    ).first()

    if not property_obj:
        raise HTTPException(404, "Property not found")

    # Verify access
    if not current_user.can_access_company(property_obj.company_id):
        raise HTTPException(403, "Access denied to this property")

    return property_obj.to_dict()

@router.post("/properties")
async def create_property(
    property_data: PropertyCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create new property."""
    # Enforce user can access the company
    enforce_company_access(current_user, property_data.company_id, "property")

    new_property = Property(**property_data.dict())
    db.add(new_property)
    db.commit()
    db.refresh(new_property)

    return new_property.to_dict()
```

---

### Fix 3: Add Rate Limiting

**Problem:** No protection against brute force or DoS
**Impact:** System abuse, credential theft
**Time to Fix:** 1 day

```bash
# Install dependencies
cd backend
pip install slowapi redis
```

```python
# File: backend/app/main.py
# Add after imports:

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import redis

# Initialize limiter
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="redis://localhost:6379"
)

app = FastAPI(...)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# File: backend/app/api/v1/endpoints/auth.py
# Add to endpoints:

from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request

limiter = Limiter(key_func=get_remote_address)

@router.post("/login")
@limiter.limit("5/minute")  # 5 attempts per minute per IP
async def login(
    request: Request,  # Required for limiter
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    ...

@router.post("/register")
@limiter.limit("3/hour")  # 3 registrations per hour per IP
async def register(
    request: Request,
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    ...

@router.post("/forgot-password")
@limiter.limit("3/hour")
async def forgot_password(
    request: Request,
    email: EmailStr,
    db: Session = Depends(get_db)
):
    ...
```

---

### Fix 4: Secure File Uploads

**Problem:** Path traversal, unlimited file sizes
**Impact:** Code execution, DoS
**Time to Fix:** 1 day

```python
# File: backend/app/api/v1/endpoints/pdf_extraction.py

import os
from pathlib import Path
import magic  # pip install python-magic

ALLOWED_EXTENSIONS = {'.pdf'}
MAX_FILENAME_LENGTH = 255

def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent path traversal."""
    # Get basename only (removes path components)
    safe_name = os.path.basename(filename)

    # Remove dangerous characters
    safe_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-")
    safe_name = ''.join(c if c in safe_chars else '_' for c in safe_name)

    # Limit length
    if len(safe_name) > MAX_FILENAME_LENGTH:
        name, ext = os.path.splitext(safe_name)
        safe_name = name[:MAX_FILENAME_LENGTH - len(ext)] + ext

    return safe_name

@router.post("/documents")
async def upload_pdf_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Upload PDF document with security checks."""

    # 1. Check file size FIRST (before reading)
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset

    if file_size > settings.max_upload_size_bytes:
        raise HTTPException(
            413,
            f"File too large. Max size: {settings.MAX_UPLOAD_SIZE_MB}MB"
        )

    # 2. Validate file extension
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, "Only PDF files are allowed")

    # 3. Verify MIME type (don't trust extension)
    file_header = await file.read(1024)
    await file.seek(0)

    mime = magic.from_buffer(file_header, mime=True)
    if mime != 'application/pdf':
        raise HTTPException(400, "File must be a valid PDF")

    # 4. Sanitize filename
    safe_filename = sanitize_filename(file.filename)

    # 5. Generate unique filename
    file_id = str(uuid.uuid4())
    final_filename = f"{file_id}_{safe_filename}"
    file_path = os.path.join(upload_dir, final_filename)

    # 6. Verify path is within upload directory (prevent traversal)
    final_path = Path(file_path).resolve()
    upload_path = Path(upload_dir).resolve()

    if not str(final_path).startswith(str(upload_path)):
        raise HTTPException(400, "Invalid file path")

    # 7. Save file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        logger.error(f"Failed to save file: {e}")
        raise HTTPException(500, "Failed to save file")

    # ... rest of logic
```

---

### Fix 5: Fix Settings Validation

```python
# File: backend/app/settings.py

# Make DATABASE_URL required (no default credentials)
DATABASE_URL: str = Field(
    ...,  # Required
    description="PostgreSQL connection string"
)

# Validate SECRET_KEY (already shown above)

# Fix CORS to be more restrictive
CORS_ALLOW_METHODS: List[str] = '["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]'
CORS_ALLOW_HEADERS: List[str] = '["Authorization", "Content-Type", "Accept", "Origin", "X-Requested-With"]'

# Add production validation
def model_post_init(self, __context):
    """Validate settings on startup."""
    super().model_post_init(__context)

    if self.is_production:
        # Production-specific validations
        if not self.SECRET_KEY or len(self.SECRET_KEY) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters in production")

        if "password@" in self.DATABASE_URL.lower():
            raise ValueError("Weak database password detected in production")

        if not self.SENTRY_DSN:
            logger.warning("SENTRY_DSN not set in production - error tracking disabled")

        # Ensure DEBUG is False
        if self.DEBUG:
            raise ValueError("DEBUG must be False in production")
```

---

## Phase 2: High-Severity Fixes

### Fix 6: Implement RBAC

```python
# File: backend/app/models/user.py

from enum import Enum

class UserRole(str, Enum):
    """User roles with hierarchical permissions."""
    SUPER_ADMIN = "super_admin"      # Full system access
    COMPANY_ADMIN = "company_admin"   # Full company access
    ANALYST = "analyst"               # Read/write company data
    VIEWER = "viewer"                 # Read-only access

class Permission(str, Enum):
    """Fine-grained permissions."""
    # Properties
    PROPERTIES_READ = "properties.read"
    PROPERTIES_CREATE = "properties.create"
    PROPERTIES_UPDATE = "properties.update"
    PROPERTIES_DELETE = "properties.delete"

    # Financial models
    MODELS_READ = "models.read"
    MODELS_CREATE = "models.create"
    MODELS_UPDATE = "models.update"
    MODELS_DELETE = "models.delete"

    # Users
    USERS_READ = "users.read"
    USERS_CREATE = "users.create"
    USERS_UPDATE = "users.update"
    USERS_DELETE = "users.delete"

    # Reports
    REPORTS_GENERATE = "reports.generate"
    REPORTS_EXPORT = "reports.export"

# Role -> Permissions mapping
ROLE_PERMISSIONS = {
    UserRole.SUPER_ADMIN: [p.value for p in Permission],  # All permissions
    UserRole.COMPANY_ADMIN: [
        Permission.PROPERTIES_READ,
        Permission.PROPERTIES_CREATE,
        Permission.PROPERTIES_UPDATE,
        Permission.MODELS_READ,
        Permission.MODELS_CREATE,
        Permission.MODELS_UPDATE,
        Permission.USERS_READ,
        Permission.USERS_CREATE,
        Permission.REPORTS_GENERATE,
        Permission.REPORTS_EXPORT,
    ],
    UserRole.ANALYST: [
        Permission.PROPERTIES_READ,
        Permission.PROPERTIES_UPDATE,
        Permission.MODELS_READ,
        Permission.MODELS_CREATE,
        Permission.MODELS_UPDATE,
        Permission.REPORTS_GENERATE,
    ],
    UserRole.VIEWER: [
        Permission.PROPERTIES_READ,
        Permission.MODELS_READ,
        Permission.REPORTS_GENERATE,
    ],
}

class User(Base, UUIDMixin, TimestampMixin):
    # ... existing fields ...
    role = Column(Enum(UserRole), default=UserRole.VIEWER, nullable=False)
    custom_permissions = Column(ARRAY(String), default=list)  # Additional permissions

    def has_permission(self, permission: str) -> bool:
        """Check if user has a specific permission."""
        if self.is_superuser:
            return True

        role_perms = ROLE_PERMISSIONS.get(self.role, [])
        return permission in role_perms or permission in self.custom_permissions

# File: backend/app/core/auth.py

def require_permission(permission: Permission):
    """Dependency to require specific permission."""
    def permission_checker(current_user: User = Depends(get_current_active_user)):
        if not current_user.has_permission(permission.value):
            raise HTTPException(
                status_code=403,
                detail=f"Missing required permission: {permission.value}"
            )
        return current_user
    return permission_checker

# Use in endpoints:
@router.delete("/properties/{id}")
async def delete_property(
    id: UUID,
    current_user: User = Depends(require_permission(Permission.PROPERTIES_DELETE)),
    db: Session = Depends(get_db)
):
    ...
```

---

## Testing Your Fixes

### 1. Unit Tests

```python
# File: backend/tests/test_auth.py

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_unauthenticated_access_denied():
    """Verify unauthenticated requests are rejected."""
    response = client.get("/api/v1/properties")
    assert response.status_code == 401

def test_authenticated_access_allowed():
    """Verify authenticated requests work."""
    # Login
    login_response = client.post("/api/v1/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Access protected endpoint
    response = client.get(
        "/api/v1/properties",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

def test_multi_tenancy_isolation():
    """Verify users cannot access other tenants' data."""
    # User A's token
    token_a = get_user_token("user_a@company1.com")

    # Try to access User B's property (company 2)
    response = client.get(
        "/api/v1/properties/{user_b_property_id}",
        headers={"Authorization": f"Bearer {token_a}"}
    )
    assert response.status_code == 403  # Access denied

def test_rate_limiting():
    """Verify rate limiting works."""
    for i in range(6):  # Limit is 5/minute
        response = client.post("/api/v1/auth/login", json={
            "email": "test@example.com",
            "password": "wrong"
        })

        if i < 5:
            assert response.status_code == 401  # Invalid credentials
        else:
            assert response.status_code == 429  # Rate limited
```

---

## Deployment Checklist

Before deploying to production, verify:

- [ ] All endpoints require authentication (except public ones)
- [ ] SECRET_KEY is strong and unique (32+ characters)
- [ ] DATABASE_URL has strong password
- [ ] Multi-tenancy enforcement tested
- [ ] Rate limiting configured
- [ ] File upload security implemented
- [ ] RBAC permissions tested
- [ ] CORS properly restricted
- [ ] Security headers enabled
- [ ] HTTPS enforced
- [ ] Database backups configured
- [ ] Monitoring/alerting set up
- [ ] Dependency vulnerabilities scanned
- [ ] Penetration testing completed

---

## Estimated Timeline

- **Phase 1 (Critical):** 5-7 days
- **Phase 2 (High-Severity):** 7-10 days
- **Phase 3 (Medium):** 10-14 days
- **Testing & Validation:** 5-7 days

**Total:** 4-5 weeks to production-ready state

---

## Support

For questions or issues implementing these fixes, review the original security audit report or consult the FastAPI security documentation.
