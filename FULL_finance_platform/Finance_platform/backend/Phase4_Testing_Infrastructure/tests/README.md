# Portfolio Dashboard Testing Suite

**Complete testing infrastructure for the Portfolio Dashboard project.**

## 📦 What's Included

- **110+ Tests**: Unit, Integration, and Service tests
- **7 Files**: 2,300+ lines of production-quality test code
- **15+ Fixtures**: Reusable test data and setup
- **Complete Documentation**: TESTING_GUIDE.md (850+ lines)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install pytest pytest-asyncio httpx
```

### 2. Run Tests

```bash
# Run all tests
pytest

# Run with comprehensive runner
python tests/run_all_tests.py

# Run specific category
pytest -m unit           # Unit tests
pytest -m integration    # Integration tests
pytest -m service        # Service tests
```

### 3. View Results

Expected output:
```
================================================================================
  PORTFOLIO DASHBOARD - COMPREHENSIVE TEST SUITE
================================================================================

✓ PASSED 1. Unit Tests - CRUD Operations
  Tests: 40 passed, 0 failed, 0 skipped (40 total)

✓ PASSED 2. Integration Tests - Core API Endpoints
  Tests: 50 passed, 0 failed, 0 skipped (50 total)

✓ ALL TEST SUITES PASSED!
```

## 📁 File Structure

```
tests/
├── conftest.py              # Fixtures and configuration
├── pytest.ini               # Pytest settings
├── run_all_tests.py         # Comprehensive test runner
├── unit/
│   └── test_crud.py         # Database CRUD tests (40+ tests)
└── integration/
    ├── test_api_endpoints.py    # Core API tests (50+ tests)
    └── test_service_endpoints.py # Service tests (30+ tests)
```

## 🧪 Test Categories

### Unit Tests (40+ tests)
Test database operations directly without HTTP layer.

```bash
pytest tests/unit/test_crud.py -v
```

Tests include:
- Fund CRUD operations
- Company CRUD operations
- Financial Metrics CRUD
- Valuation CRUD
- KPI CRUD
- Model relationships
- Query performance

### Integration Tests (50+ tests)
Test API endpoints with HTTP requests.

```bash
pytest tests/integration/test_api_endpoints.py -v
```

Tests include:
- Fund API endpoints
- Company API endpoints
- Financial Metrics API
- Valuation API
- KPI API
- Dashboard API
- Complete workflows
- Error handling

### Service Tests (30+ tests)
Test business logic services.

```bash
pytest tests/integration/test_service_endpoints.py -v
```

Tests include:
- Model generation (DCF, LBO, Merger)
- PDF extraction and processing
- Batch operations
- Integrated workflows

## 🔧 Key Features

### Fast Execution
- In-memory SQLite database
- Complete suite runs in < 30 seconds
- No database setup required

### Test Isolation
- Each test gets fresh database
- Automatic cleanup
- No test interdependencies

### Comprehensive Fixtures
- Database fixtures (engine, session, client)
- Sample data (fund, company, financials, etc.)
- Request payloads
- Batch test data

### Multiple Run Options
```bash
pytest                    # All tests
pytest -v                 # Verbose output
pytest -m unit            # Unit tests only
pytest -m integration     # Integration tests only
pytest -k "fund"          # Tests matching pattern
pytest --maxfail=1        # Stop on first failure
pytest -s                 # Show print statements
python run_all_tests.py   # Comprehensive runner
```

## 📚 Documentation

See **TESTING_GUIDE.md** for:
- Complete testing guide
- Fixture documentation
- Writing new tests
- Best practices
- Troubleshooting
- CI/CD integration

## ✅ Quick Commands

```bash
# Basic
pytest                          # Run all tests
pytest -v                       # Verbose output
pytest -s                       # Show print statements

# By Category
pytest -m unit                  # Unit tests
pytest -m integration           # Integration tests
pytest -m service               # Service tests
pytest -m "not slow"            # Exclude slow tests

# Specific Tests
pytest tests/unit/test_crud.py                           # File
pytest tests/unit/test_crud.py::TestFundCRUD            # Class
pytest tests/unit/test_crud.py::TestFundCRUD::test_create_fund  # Function

# Debugging
pytest --pdb                    # Enter debugger on failure
pytest -l                       # Show local variables
pytest --lf                     # Run last failed
pytest --tb=short               # Short traceback

# Reporting
pytest --html=report.html       # HTML report
pytest --cov=app                # Coverage report
```

## 🎯 Common Tasks

### Test a Specific Feature

```bash
# Test fund operations
pytest -k "fund" -v

# Test company API
pytest tests/integration/test_api_endpoints.py::TestCompanyAPI -v

# Test model generation
pytest tests/integration/test_service_endpoints.py::TestModelGenerationEndpoints -v
```

### Run Tests Before Commit

```bash
# Quick test (exclude slow tests)
pytest -m "not slow"

# Stop on first failure
pytest --maxfail=1
```

### Generate Coverage Report

```bash
pytest --cov=app --cov-report=html
open htmlcov/index.html
```

## 🔍 Troubleshooting

### Import Errors
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest
```

### Fixture Not Found
```bash
# List available fixtures
pytest --fixtures
```

### Tests Not Discovered
```bash
# List what will be collected
pytest --collect-only
```

## 📈 CI/CD Integration

### GitHub Actions

```yaml
- name: Run tests
  run: |
    pip install pytest pytest-asyncio httpx
    python tests/run_all_tests.py
```

### Pre-commit Hook

```bash
#!/bin/bash
pytest --maxfail=1 -m "not slow"
```

## 🎓 Writing New Tests

```python
import pytest
from sqlalchemy.orm import Session

@pytest.mark.unit
def test_my_feature(db_session: Session):
    """Test description."""
    # Arrange
    data = create_test_data()
    
    # Act
    result = perform_action(data)
    
    # Assert
    assert result == expected
```

## 💡 Best Practices

1. **Use descriptive test names**
2. **Follow AAA pattern** (Arrange, Act, Assert)
3. **Test one thing per test**
4. **Use fixtures for setup**
5. **Test edge cases**
6. **Keep tests fast**
7. **Make tests independent**

## 📞 Help

- **Full Documentation**: See TESTING_GUIDE.md
- **Pytest Docs**: https://docs.pytest.org/
- **FastAPI Testing**: https://fastapi.tiangolo.com/tutorial/testing/

---

**Ready to test!** Run `pytest` to get started.
