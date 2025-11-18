"""
Real Estate Dashboard Backend - Main Application

FastAPI application entry point with middleware, routers, and configuration.
"""

from contextlib import asynccontextmanager
import logging
import time

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import settings
from app.core.database import check_db_connection, init_db
from app.api.router import api_router

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ================================
# APPLICATION LIFECYCLE
# ================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.

    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting Real Estate Dashboard API...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug Mode: {settings.DEBUG}")

    # Check database connection
    if check_db_connection():
        logger.info("✅ Database connection successful")
    else:
        logger.error("❌ Database connection failed!")
        if not settings.is_development:
            raise Exception("Cannot start application without database connection")

    # Initialize database (only in development)
    if settings.is_development and settings.DEBUG:
        logger.info("Initializing database schema...")
        try:
            init_db()
            logger.info("✅ Database schema initialized")
        except Exception as e:
            logger.warning(f"⚠️ Database initialization failed: {e}")

    logger.info("🚀 Real Estate Dashboard started successfully!")

    yield

    # Shutdown
    logger.info("Shutting down Real Estate Dashboard API...")
    logger.info("✅ Application shut down successfully")


# ================================
# CREATE APPLICATION
# ================================

app = FastAPI(
    title="Real Estate Dashboard API",
    version="1.0.0",
    description="Comprehensive API for Real Estate Property Management and Financial Modeling",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    openapi_url="/openapi.json" if settings.DEBUG else None,
    lifespan=lifespan,
)


# ================================
# MIDDLEWARE
# ================================

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# GZip Compression
app.add_middleware(GZipMiddleware, minimum_size=1000)


# Request Timing Middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add request processing time to response headers."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests."""
    logger.info(f"{request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Status: {response.status_code}")
    return response


# ================================
# EXCEPTION HANDLERS
# ================================

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.status_code,
                "message": exc.detail,
                "type": "http_exception"
            }
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": {
                "code": 422,
                "message": "Validation error",
                "type": "validation_error",
                "details": exc.errors()
            }
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle all other exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)

    # Don't expose internal errors in production
    if settings.is_production:
        message = "Internal server error"
    else:
        message = str(exc)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": 500,
                "message": message,
                "type": "internal_error"
            }
        },
    )


# ================================
# ROOT ENDPOINTS
# ================================

@app.get("/")
async def root():
    """Root endpoint - API information."""
    return {
        "name": "Real Estate Dashboard API",
        "version": "1.0.0",
        "description": "Comprehensive API for Property Management and Real Estate Financial Modeling",
        "environment": settings.ENVIRONMENT,
        "status": "operational",
        "docs_url": "/docs" if settings.DEBUG else "disabled",
        "api_prefix": settings.API_V1_PREFIX,
        "features": [
            "Property Management",
            "Real Estate Financial Models",
            "Portfolio Analytics",
            "ROI Analysis"
        ]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    db_healthy = check_db_connection()

    return {
        "status": "healthy" if db_healthy else "degraded",
        "timestamp": time.time(),
        "checks": {
            "database": "up" if db_healthy else "down",
            "api": "up"
        }
    }


# ================================
# INCLUDE ROUTERS
# ================================

# Include API v1 router
app.include_router(
    api_router,
    prefix=settings.API_V1_PREFIX
)


# ================================
# DEVELOPMENT UTILITIES
# ================================

if settings.DEBUG:
    @app.get("/debug/routes")
    async def list_routes():
        """List all registered routes (debug only)."""
        routes = []
        for route in app.routes:
            routes.append({
                "path": route.path,
                "name": route.name,
                "methods": list(route.methods) if hasattr(route, 'methods') else []
            })
        return routes


# ================================
# APPLICATION INFO
# ================================

@app.on_event("startup")
async def print_startup_info():
    """Print startup information."""
    if settings.DEBUG:
        print("\n" + "="*70)
        print("🏢  REAL ESTATE DASHBOARD API  🏢")
        print("="*70)
        print(f"Version: 1.0.0")
        print(f"Environment: {settings.ENVIRONMENT}")
        print(f"Server: http://{settings.HOST}:{settings.PORT}")
        print(f"API Docs: http://{settings.HOST}:{settings.PORT}/docs")
        print(f"Health Check: http://{settings.HOST}:{settings.PORT}/health")
        print("="*70)
        print("Features:")
        print("  • Property Management System")
        print("  • Real Estate Financial Models (Fix & Flip, SFR, Multifamily, Hotel)")
        print("  • Portfolio Analytics & ROI Analysis")
        print("  • Maintenance Tracking & Lease Management")
        print("="*70 + "\n")


# ================================
# EXPORT
# ================================

__all__ = ["app"]
