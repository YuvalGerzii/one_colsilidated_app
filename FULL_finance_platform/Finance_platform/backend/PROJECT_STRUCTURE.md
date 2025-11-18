# Portfolio Dashboard Backend - Project Structure

```
backend/
â"œâ"€â"€ app/
â"‚   â"œâ"€â"€ __init__.py
â"‚   â"œâ"€â"€ main.py                    # FastAPI application entry point
â"‚   â"œâ"€â"€ config.py                  # Configuration and environment variables
â"‚   â"‚
â"‚   â"œâ"€â"€ api/
â"‚   â"‚   â"œâ"€â"€ __init__.py
â"‚   â"‚   â"œâ"€â"€ deps.py                 # Dependency injection (DB sessions, auth)
â"‚   â"‚   â"œâ"€â"€ router.py               # Main API router
â"‚   â"‚   â"œâ"€â"€ v1/
â"‚   â"‚       â"œâ"€â"€ __init__.py
â"‚   â"‚       â"œâ"€â"€ endpoints/
â"‚   â"‚           â"œâ"€â"€ __init__.py
â"‚   â"‚           â"œâ"€â"€ funds.py          # Fund CRUD endpoints
â"‚   â"‚           â"œâ"€â"€ companies.py       # Company CRUD endpoints
â"‚   â"‚           â"œâ"€â"€ financials.py      # Financial metrics endpoints
â"‚   â"‚           â"œâ"€â"€ models.py          # Model generation endpoints
â"‚   â"‚           â"œâ"€â"€ pdf.py             # PDF upload/extraction endpoints
â"‚   â"‚           â"œâ"€â"€ reports.py         # Reporting endpoints
â"‚   â"‚           â"œâ"€â"€ dashboard.py       # Dashboard data endpoints
â"‚   â"‚           â""â"€â"€ health.py          # Health check endpoints
â"‚   â"‚
â"‚   â"œâ"€â"€ models/
â"‚   â"‚   â"œâ"€â"€ __init__.py
â"‚   â"‚   â"œâ"€â"€ database.py              # SQLAlchemy models
â"‚   â"‚   â"œâ"€â"€ fund.py
â"‚   â"‚   â"œâ"€â"€ company.py
â"‚   â"‚   â"œâ"€â"€ financial_metric.py
â"‚   â"‚   â"œâ"€â"€ company_kpi.py
â"‚   â"‚   â"œâ"€â"€ valuation.py
â"‚   â"‚   â"œâ"€â"€ document.py
â"‚   â"‚   â"œâ"€â"€ due_diligence.py
â"‚   â"‚   â"œâ"€â"€ value_creation.py
â"‚   â"‚   â"œâ"€â"€ user.py
â"‚   â"‚   â""â"€â"€ audit_log.py
â"‚   â"‚
â"‚   â"œâ"€â"€ schemas/
â"‚   â"‚   â"œâ"€â"€ __init__.py
â"‚   â"‚   â"œâ"€â"€ fund.py                  # Pydantic schemas for validation
â"‚   â"‚   â"œâ"€â"€ company.py
â"‚   â"‚   â"œâ"€â"€ financial_metric.py
â"‚   â"‚   â"œâ"€â"€ model_generation.py
â"‚   â"‚   â"œâ"€â"€ pdf_extraction.py
â"‚   â"‚   â""â"€â"€ response.py
â"‚   â"‚
â"‚   â"œâ"€â"€ crud/
â"‚   â"‚   â"œâ"€â"€ __init__.py
â"‚   â"‚   â"œâ"€â"€ base.py                  # Base CRUD class
â"‚   â"‚   â"œâ"€â"€ fund.py
â"‚   â"‚   â"œâ"€â"€ company.py
â"‚   â"‚   â"œâ"€â"€ financial_metric.py
â"‚   â"‚   â""â"€â"€ valuation.py
â"‚   â"‚
â"‚   â"œâ"€â"€ services/
â"‚   â"‚   â"œâ"€â"€ __init__.py
â"‚   â"‚   â"œâ"€â"€ model_generator.py       # Excel model generation service
â"‚   â"‚   â"œâ"€â"€ pdf_extractor.py         # PDF financial extraction service
â"‚   â"‚   â"œâ"€â"€ kpi_calculator.py        # KPI calculation service
â"‚   â"‚   â"œâ"€â"€ valuation_engine.py      # Valuation calculations
â"‚   â"‚   â""â"€â"€ report_builder.py        # Report generation service
â"‚   â"‚
â"‚   â"œâ"€â"€ core/
â"‚   â"‚   â"œâ"€â"€ __init__.py
â"‚   â"‚   â"œâ"€â"€ database.py              # Database connection and session
â"‚   â"‚   â"œâ"€â"€ security.py              # Authentication/authorization
â"‚   â"‚   â"œâ"€â"€ exceptions.py            # Custom exceptions
â"‚   â"‚   â""â"€â"€ logging.py               # Logging configuration
â"‚   â"‚
â"‚   â""â"€â"€ utils/
â"‚       â"œâ"€â"€ __init__.py
â"‚       â"œâ"€â"€ formatters.py            # Currency/number formatters
â"‚       â"œâ"€â"€ validators.py            # Data validators
â"‚       â""â"€â"€ helpers.py               # Helper functions
â"‚
â"œâ"€â"€ alembic/
â"‚   â"œâ"€â"€ versions/                   # Database migrations
â"‚   â"œâ"€â"€ env.py
â"‚   â""â"€â"€ alembic.ini
â"‚
â"œâ"€â"€ tests/
â"‚   â"œâ"€â"€ __init__.py
â"‚   â"œâ"€â"€ conftest.py                 # Pytest configuration
â"‚   â"œâ"€â"€ test_api/
â"‚   â"œâ"€â"€ test_services/
â"‚   â""â"€â"€ test_crud/
â"‚
â"œâ"€â"€ templates/                      # Excel model templates
â"‚   â"œâ"€â"€ DCF_Model_Comprehensive.xlsx
â"‚   â"œâ"€â"€ LBO_Model_Comprehensive.xlsx
â"‚   â"œâ"€â"€ Merger_Model_Comprehensive.xlsx
â"‚   â"œâ"€â"€ DD_Tracker_Comprehensive.xlsx
â"‚   â""â"€â"€ QoE_Analysis_Comprehensive.xlsx
â"‚
â"œâ"€â"€ storage/
â"‚   â"œâ"€â"€ uploads/                    # Uploaded PDFs
â"‚   â""â"€â"€ generated_models/           # Generated Excel models
â"‚
â"œâ"€â"€ .env.example
â"œâ"€â"€ .env
â"œâ"€â"€ requirements.txt
â"œâ"€â"€ pyproject.toml
â"œâ"€â"€ README.md
â"œâ"€â"€ Dockerfile
â""â"€â"€ docker-compose.yml
```

## Architecture

### Application Flow
```
Client Request
    â†"
FastAPI Router
    â†"
Endpoint Handler
    â†"
Service Layer (business logic)
    â†"
CRUD Layer (database operations)
    â†"
SQLAlchemy Models
    â†"
PostgreSQL Database
```

### Key Design Patterns

1. **Dependency Injection**: Database sessions, current user
2. **Repository Pattern**: CRUD operations abstracted
3. **Service Layer**: Business logic separated from API
4. **Schema Validation**: Pydantic for request/response
5. **Error Handling**: Centralized exception handling
6. **Async/Await**: Non-blocking I/O for performance

## Technology Stack

- **Framework**: FastAPI 0.104+
- **Database ORM**: SQLAlchemy 2.0+
- **Migration Tool**: Alembic
- **Validation**: Pydantic 2.0+
- **Excel Processing**: openpyxl
- **PDF Processing**: pdfplumber, PyPDF2
- **Testing**: pytest, httpx
- **Documentation**: Auto-generated OpenAPI (Swagger)
