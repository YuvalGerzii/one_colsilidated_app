"""
Database Connection and Session Management

This module provides database connectivity using SQLAlchemy.
Supports both sync and async database operations.
"""

from typing import Generator, AsyncGenerator
from sqlalchemy import create_engine, event
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool

from app.config import settings


# ================================
# SYNC DATABASE ENGINE
# ================================

engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT,
    pool_recycle=settings.DB_POOL_RECYCLE,
    echo=settings.DEBUG,  # Log SQL queries in debug mode
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# ================================
# ASYNC DATABASE ENGINE (Optional)
# ================================

async_engine = create_async_engine(
    settings.database_url_async,
    poolclass=QueuePool,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT,
    pool_recycle=settings.DB_POOL_RECYCLE,
    echo=settings.DEBUG,
)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


# ================================
# BASE MODEL
# ================================

Base = declarative_base()


# ================================
# DATABASE CONNECTION EVENTS
# ================================

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    """Set pragmas for SQLite (if used in development)."""
    if "sqlite" in settings.DATABASE_URL:
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


@event.listens_for(engine, "before_cursor_execute")
def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
    """Log slow queries (optional)."""
    if settings.DEBUG:
        conn.info.setdefault('query_start_time', []).append(None)
        # You can add timing logic here


# ================================
# DEPENDENCY INJECTION FUNCTIONS
# ================================

def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get database session.
    
    Usage in FastAPI endpoint:
        @app.get("/items")
        def read_items(db: Session = Depends(get_db)):
            ...
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Async dependency function to get database session.
    
    Usage in FastAPI endpoint:
        @app.get("/items")
        async def read_items(db: AsyncSession = Depends(get_async_db)):
            ...
    
    Yields:
        AsyncSession: SQLAlchemy async database session
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


# ================================
# DATABASE UTILITIES
# ================================

def init_db() -> None:
    """
    Initialize database by creating all tables.
    
    Note: In production, use Alembic migrations instead.
    This is useful for development and testing.
    """
    # Import all models here to ensure they're registered
    from app.models import (
        fund, company, financial_metric, company_kpi,
        valuation, document, due_diligence, value_creation,
        user, audit_log
    )
    
    Base.metadata.create_all(bind=engine)


def drop_db() -> None:
    """
    Drop all database tables.
    
    WARNING: This will delete all data! Use only for testing.
    """
    Base.metadata.drop_all(bind=engine)


def check_db_connection() -> bool:
    """
    Check if database connection is working.
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False


async def check_async_db_connection() -> bool:
    """
    Async check if database connection is working.
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        async with AsyncSessionLocal() as session:
            await session.execute("SELECT 1")
        return True
    except Exception as e:
        print(f"Async database connection failed: {e}")
        return False


# ================================
# TRANSACTION CONTEXT MANAGERS
# ================================

class DatabaseTransaction:
    """
    Context manager for database transactions.
    
    Usage:
        with DatabaseTransaction() as db:
            db.add(new_item)
            # Automatically commits on success, rolls back on error
    """
    
    def __init__(self):
        self.db = SessionLocal()
    
    def __enter__(self) -> Session:
        return self.db
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.db.rollback()
        else:
            self.db.commit()
        self.db.close()


class AsyncDatabaseTransaction:
    """
    Async context manager for database transactions.
    
    Usage:
        async with AsyncDatabaseTransaction() as db:
            db.add(new_item)
            # Automatically commits on success, rolls back on error
    """
    
    def __init__(self):
        self.db = None
    
    async def __aenter__(self) -> AsyncSession:
        self.db = AsyncSessionLocal()
        return self.db
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.db.rollback()
        else:
            await self.db.commit()
        await self.db.close()


# ================================
# EXPORT
# ================================

__all__ = [
    "engine",
    "async_engine",
    "SessionLocal",
    "AsyncSessionLocal",
    "Base",
    "get_db",
    "get_async_db",
    "init_db",
    "drop_db",
    "check_db_connection",
    "check_async_db_connection",
    "DatabaseTransaction",
    "AsyncDatabaseTransaction",
]
