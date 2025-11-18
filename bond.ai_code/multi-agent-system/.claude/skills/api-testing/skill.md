---
name: FastAPI Testing Expert
description: Creates comprehensive API tests for FastAPI endpoints with proper fixtures, mocking, and test coverage
---

# FastAPI Testing Expert Skill

This skill helps create thorough, maintainable tests for FastAPI applications, specifically tailored for the real estate dashboard API.

## When to Use This Skill

Invoke when:
- Writing new API endpoints
- Refactoring existing endpoints
- Adding test coverage
- Debugging API issues
- Before committing API changes

## Testing Stack

```python
# Required imports for testing
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db
```

## Test Database Setup

### Fixture for Test Database

```python
# conftest.py - Shared fixtures for all tests

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import Base, get_db
from app.models.property_management import Property, Unit, Lease

# Use in-memory SQLite for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Create a test client with database override."""
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_property(db):
    """Create a sample property for testing."""
    property_data = Property(
        address="123 Test Street",
        city="Test City",
        state="TS",
        zip_code="12345",
        property_type="multifamily",
        units_count=4,
        purchase_price=400000,
        purchase_date="2023-01-15"
    )
    db.add(property_data)
    db.commit()
    db.refresh(property_data)
    return property_data


@pytest.fixture
def sample_unit(db, sample_property):
    """Create a sample unit linked to property."""
    unit = Unit(
        property_id=sample_property.id,
        unit_number="101",
        bedrooms=2,
        bathrooms=1,
        square_feet=800,
        monthly_rent=1200
    )
    db.add(unit)
    db.commit()
    db.refresh(unit)
    return unit
```

## Testing Patterns

### 1. Test CRUD Operations

```python
# test_property_endpoints.py

def test_create_property_success(client):
    """Test creating a new property with valid data."""
    property_data = {
        "address": "456 Oak Avenue",
        "city": "Springfield",
        "state": "IL",
        "zip_code": "62701",
        "property_type": "single_family",
        "units_count": 1,
        "purchase_price": 250000,
        "purchase_date": "2024-01-01"
    }

    response = client.post("/api/v1/properties", json=property_data)

    assert response.status_code == 201
    data = response.json()
    assert data["address"] == property_data["address"]
    assert data["purchase_price"] == property_data["purchase_price"]
    assert "id" in data


def test_create_property_invalid_data(client):
    """Test creating property with invalid data returns 422."""
    property_data = {
        "address": "Bad Property",
        "purchase_price": -100000,  # Invalid: negative price
        "units_count": 0  # Invalid: zero units
    }

    response = client.post("/api/v1/properties", json=property_data)

    assert response.status_code == 422
    assert "detail" in response.json()


def test_get_property_success(client, sample_property):
    """Test retrieving an existing property."""
    response = client.get(f"/api/v1/properties/{sample_property.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_property.id
    assert data["address"] == sample_property.address


def test_get_property_not_found(client):
    """Test retrieving non-existent property returns 404."""
    response = client.get("/api/v1/properties/99999")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_property_success(client, sample_property):
    """Test updating property fields."""
    update_data = {
        "address": "789 Updated Street",
        "purchase_price": 450000
    }

    response = client.patch(
        f"/api/v1/properties/{sample_property.id}",
        json=update_data
    )

    assert response.status_code == 200
    data = response.json()
    assert data["address"] == update_data["address"]
    assert data["purchase_price"] == update_data["purchase_price"]


def test_delete_property_success(client, sample_property):
    """Test deleting a property."""
    response = client.delete(f"/api/v1/properties/{sample_property.id}")

    assert response.status_code == 204

    # Verify property is gone
    get_response = client.get(f"/api/v1/properties/{sample_property.id}")
    assert get_response.status_code == 404


def test_list_properties_pagination(client, db):
    """Test listing properties with pagination."""
    # Create multiple properties
    for i in range(15):
        prop = Property(
            address=f"{i} Test St",
            city="Test",
            state="TS",
            zip_code="12345",
            property_type="multifamily",
            units_count=4,
            purchase_price=300000 + (i * 10000),
            purchase_date="2023-01-01"
        )
        db.add(prop)
    db.commit()

    # Test first page
    response = client.get("/api/v1/properties?skip=0&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 10

    # Test second page
    response = client.get("/api/v1/properties?skip=10&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
```

### 2. Test Financial Calculations

```python
# test_financial_calculations.py

def test_calculate_irr_success(client):
    """Test IRR calculation with valid inputs."""
    request_data = {
        "initial_investment": -100000,
        "cash_flows": [10000, 12000, 15000, 18000, 150000],
        "holding_period_years": 5
    }

    response = client.post("/api/v1/calculate/irr", json=request_data)

    assert response.status_code == 200
    data = response.json()
    assert "irr" in data
    assert 0.10 <= data["irr"] <= 0.30  # Reasonable IRR range
    assert data["irr"] > 0  # Positive returns


def test_calculate_irr_negative_returns(client):
    """Test IRR calculation with negative returns."""
    request_data = {
        "initial_investment": -100000,
        "cash_flows": [5000, 5000, 5000, 5000, 5000],  # Total: 25k (loss)
        "holding_period_years": 5
    }

    response = client.post("/api/v1/calculate/irr", json=request_data)

    assert response.status_code == 200
    data = response.json()
    assert data["irr"] < 0  # Negative returns


def test_calculate_cap_rate(client, sample_property):
    """Test cap rate calculation for a property."""
    # Set up income and expenses
    noi = 40000

    response = client.get(
        f"/api/v1/properties/{sample_property.id}/cap_rate",
        params={"annual_noi": noi}
    )

    assert response.status_code == 200
    data = response.json()

    expected_cap_rate = (noi / sample_property.purchase_price) * 100
    assert abs(data["cap_rate"] - expected_cap_rate) < 0.01


def test_calculate_cash_on_cash(client, sample_property):
    """Test cash-on-cash return calculation."""
    request_data = {
        "property_id": sample_property.id,
        "annual_cash_flow": 15000,
        "total_cash_invested": 100000
    }

    response = client.post("/api/v1/calculate/cash_on_cash", json=request_data)

    assert response.status_code == 200
    data = response.json()
    assert data["cash_on_cash_return"] == 15.0  # 15%


def test_calculate_dscr(client):
    """Test debt service coverage ratio calculation."""
    request_data = {
        "noi": 60000,
        "annual_debt_service": 48000
    }

    response = client.post("/api/v1/calculate/dscr", json=request_data)

    assert response.status_code == 200
    data = response.json()
    assert data["dscr"] == 1.25
    assert data["is_sufficient"] is True  # Above 1.20 threshold
```

### 3. Test Input Validation

```python
# test_validation.py

def test_property_negative_price_rejected(client):
    """Test that negative purchase price is rejected."""
    property_data = {
        "address": "123 Test St",
        "city": "Test",
        "state": "TS",
        "zip_code": "12345",
        "property_type": "single_family",
        "units_count": 1,
        "purchase_price": -100000,  # Invalid
        "purchase_date": "2024-01-01"
    }

    response = client.post("/api/v1/properties", json=property_data)
    assert response.status_code == 422


def test_property_invalid_type_rejected(client):
    """Test that invalid property type is rejected."""
    property_data = {
        "address": "123 Test St",
        "property_type": "castle",  # Invalid type
        "purchase_price": 300000
    }

    response = client.post("/api/v1/properties", json=property_data)
    assert response.status_code == 422


def test_unit_rent_below_minimum(client, sample_property):
    """Test that unreasonably low rent is rejected."""
    unit_data = {
        "property_id": sample_property.id,
        "unit_number": "102",
        "monthly_rent": 10  # Too low
    }

    response = client.post("/api/v1/units", json=unit_data)
    assert response.status_code == 422


@pytest.mark.parametrize("invalid_zip", [
    "1234",      # Too short
    "123456",    # Too long
    "abcde",     # Non-numeric
    "12-345",    # Invalid format
])
def test_invalid_zip_codes(client, invalid_zip):
    """Test various invalid zip code formats."""
    property_data = {
        "address": "123 Test St",
        "city": "Test",
        "state": "TS",
        "zip_code": invalid_zip,
        "property_type": "single_family",
        "purchase_price": 250000
    }

    response = client.post("/api/v1/properties", json=property_data)
    assert response.status_code == 422
```

### 4. Test Error Handling

```python
# test_error_handling.py

def test_database_error_handling(client, mocker):
    """Test that database errors are handled gracefully."""
    # Mock database to raise an error
    mocker.patch(
        'app.api.v1.endpoints.property_management.create_property',
        side_effect=Exception("Database connection failed")
    )

    property_data = {
        "address": "123 Test St",
        "purchase_price": 250000
    }

    response = client.post("/api/v1/properties", json=property_data)
    assert response.status_code == 500
    assert "error" in response.json()["detail"].lower()


def test_duplicate_property_address(client, sample_property):
    """Test that duplicate addresses are rejected."""
    duplicate_data = {
        "address": sample_property.address,  # Duplicate
        "city": "Test",
        "state": "TS",
        "zip_code": "12345",
        "property_type": "single_family",
        "purchase_price": 300000,
        "purchase_date": "2024-01-01"
    }

    response = client.post("/api/v1/properties", json=duplicate_data)
    assert response.status_code == 409  # Conflict
    assert "already exists" in response.json()["detail"].lower()


def test_missing_required_fields(client):
    """Test that missing required fields return appropriate error."""
    incomplete_data = {
        "address": "123 Test St"
        # Missing required fields
    }

    response = client.post("/api/v1/properties", json=incomplete_data)
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any("required" in str(error).lower() for error in errors)
```

### 5. Test Relationships & Cascading

```python
# test_relationships.py

def test_delete_property_cascades_to_units(client, db, sample_property):
    """Test that deleting property also deletes associated units."""
    # Create units for the property
    for i in range(3):
        unit = Unit(
            property_id=sample_property.id,
            unit_number=f"10{i}",
            monthly_rent=1000 + (i * 100)
        )
        db.add(unit)
    db.commit()

    # Delete property
    response = client.delete(f"/api/v1/properties/{sample_property.id}")
    assert response.status_code == 204

    # Verify units are also deleted
    units_response = client.get(
        f"/api/v1/properties/{sample_property.id}/units"
    )
    assert units_response.status_code == 404


def test_get_property_with_units(client, db, sample_property):
    """Test retrieving property includes all its units."""
    # Create multiple units
    for i in range(4):
        unit = Unit(
            property_id=sample_property.id,
            unit_number=f"10{i}",
            bedrooms=2,
            monthly_rent=1200
        )
        db.add(unit)
    db.commit()

    response = client.get(f"/api/v1/properties/{sample_property.id}?include_units=true")

    assert response.status_code == 200
    data = response.json()
    assert "units" in data
    assert len(data["units"]) == 4
```

### 6. Test Authentication & Authorization (if implemented)

```python
# test_auth.py

def test_create_property_requires_auth(client):
    """Test that creating property requires authentication."""
    property_data = {
        "address": "123 Test St",
        "purchase_price": 250000
    }

    # Without auth token
    response = client.post("/api/v1/properties", json=property_data)
    assert response.status_code == 401


def test_user_can_only_access_own_properties(client, authenticated_user):
    """Test that users can only access their own properties."""
    # Create property for another user
    other_user_property = create_property_for_user(user_id=999)

    # Try to access with different user
    response = client.get(
        f"/api/v1/properties/{other_user_property.id}",
        headers={"Authorization": f"Bearer {authenticated_user.token}"}
    )

    assert response.status_code == 403  # Forbidden
```

## Test Organization

### File Structure
```
backend/
└── tests/
    ├── conftest.py                    # Shared fixtures
    ├── test_health.py                 # Health check tests
    ├── test_property_endpoints.py     # Property CRUD tests
    ├── test_unit_endpoints.py         # Unit CRUD tests
    ├── test_lease_endpoints.py        # Lease CRUD tests
    ├── test_financial_calculations.py # Calculation tests
    ├── test_validation.py             # Input validation tests
    ├── test_error_handling.py         # Error scenarios
    └── test_integration.py            # End-to-end tests
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_property_endpoints.py

# Run specific test
pytest tests/test_property_endpoints.py::test_create_property_success

# Run tests matching pattern
pytest -k "property"

# Run with verbose output
pytest -v

# Run with print statements visible
pytest -s
```

## Coverage Requirements

Aim for:
- **Overall coverage**: 85%+
- **Critical paths** (financial calculations): 95%+
- **API endpoints**: 90%+
- **Models**: 80%+

## Best Practices

### 1. Use Descriptive Test Names
```python
# ✅ GOOD - Clear what's being tested
def test_create_property_with_negative_price_returns_422():
    pass

# ❌ BAD - Unclear purpose
def test_property():
    pass
```

### 2. Arrange-Act-Assert Pattern
```python
def test_update_property():
    # Arrange - Set up test data
    property_data = {...}
    response = client.post("/api/v1/properties", json=property_data)
    property_id = response.json()["id"]

    # Act - Perform the action being tested
    update_data = {"address": "New Address"}
    update_response = client.patch(
        f"/api/v1/properties/{property_id}",
        json=update_data
    )

    # Assert - Verify results
    assert update_response.status_code == 200
    assert update_response.json()["address"] == "New Address"
```

### 3. Test Edge Cases
- Empty inputs
- Boundary values (0, negative, very large numbers)
- Invalid data types
- Missing required fields
- Duplicate entries
- Null values

### 4. Use Parametrize for Similar Tests
```python
@pytest.mark.parametrize("property_type,expected_response", [
    ("single_family", 201),
    ("multifamily", 201),
    ("commercial", 201),
    ("invalid_type", 422),
])
def test_property_types(client, property_type, expected_response):
    data = {
        "address": "123 Test",
        "property_type": property_type,
        "purchase_price": 250000
    }
    response = client.post("/api/v1/properties", json=data)
    assert response.status_code == expected_response
```

## Execution Instructions

When this skill is invoked:

1. **Identify the endpoint** being tested
2. **Create appropriate fixtures** in conftest.py if needed
3. **Write tests covering**:
   - Happy path (success cases)
   - Error cases (4xx, 5xx)
   - Input validation
   - Edge cases
4. **Ensure tests are isolated** (each test can run independently)
5. **Use meaningful assertions** (check specific fields, not just status codes)
6. **Run tests and verify** they pass
7. **Check coverage** and add tests for uncovered lines

Always write tests that are:
- **Readable**: Clear what they test
- **Reliable**: No flaky tests
- **Fast**: Use in-memory DB, avoid sleeps
- **Isolated**: No dependencies between tests
