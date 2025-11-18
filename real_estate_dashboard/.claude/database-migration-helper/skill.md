# Database Migration Helper

This skill assists with Alembic migrations for schema changes in the real estate dashboard application.

## Overview

You are a database migration expert specializing in Alembic and SQLAlchemy. Your role is to help developers:
- Initialize and configure Alembic for the first time
- Generate migration scripts for schema changes
- Review migration scripts for correctness and safety
- Troubleshoot migration issues
- Follow best practices for database migrations

## Current Project Context

**Database Setup:**
- Backend: FastAPI with SQLAlchemy ORM
- Database: PostgreSQL
- Current approach: Manual `Base.metadata.create_all()` in `backend/app/core/database.py:136`
- Migration status: Alembic NOT yet initialized (needs setup)

**Base Model Structure:**
Located in `backend/app/models/database.py`:
- `UUIDMixin` - UUID primary key pattern
- `TimestampMixin` - `created_at`, `updated_at` tracking
- `AuditMixin` - `created_by`, `updated_by` tracking
- `SoftDeleteMixin` - Soft delete with `deleted_at`, `deleted_by`
- `BaseModel` - Combines all mixins with utility methods

**SQLAlchemy Naming Convention:**
```python
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
```

## Alembic Best Practices

### 1. Initial Setup

When initializing Alembic for the first time:

```bash
cd backend
alembic init alembic
```

Then configure `alembic.ini`:
```ini
# Update database URL (use environment variable in production)
sqlalchemy.url = postgresql://user:password@localhost/dbname

# Or use config.py approach:
# In env.py, use: config.set_main_option('sqlalchemy.url', settings.DATABASE_URL)
```

Update `alembic/env.py` to import your models:
```python
from app.core.database import Base
from app.models import *  # Import all models

target_metadata = Base.metadata
```

### 2. Naming Convention

**CRITICAL:** Always set up naming conventions to ensure consistent constraint names:

```python
# In alembic/env.py
from sqlalchemy import MetaData

target_metadata = Base.metadata

# Ensure metadata has naming convention
if target_metadata.naming_convention is None:
    target_metadata.naming_convention = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
```

### 3. Creating Migrations

**Autogenerate Feature:**
```bash
# Generate migration from model changes
alembic revision --autogenerate -m "descriptive message"

# Examples:
alembic revision --autogenerate -m "add property financial metrics"
alembic revision --autogenerate -m "add lease payment tracking"
```

**Manual Migrations:**
For data migrations or complex operations:
```bash
alembic revision -m "migrate legacy property data"
```

### 4. Migration Script Structure

A well-formed migration should include:

```python
"""Descriptive message about what changed

Revision ID: abc123
Revises: def456
Create Date: 2025-01-06 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic
revision = 'abc123'
down_revision = 'def456'
branch_labels = None
depends_on = None

def upgrade() -> None:
    """Apply schema changes."""
    # Use batch operations for better compatibility
    with op.batch_alter_table('properties') as batch_op:
        batch_op.add_column(
            sa.Column('purchase_price', sa.Numeric(precision=12, scale=2), nullable=True)
        )
        batch_op.create_index('ix_purchase_price', ['purchase_price'])

def downgrade() -> None:
    """Revert schema changes."""
    with op.batch_alter_table('properties') as batch_op:
        batch_op.drop_index('ix_purchase_price')
        batch_op.drop_column('purchase_price')
```

### 5. Data Migrations

When migrating data, define tables manually to avoid model dependency issues:

```python
def upgrade() -> None:
    # Define table structure at migration time (static schema)
    properties = sa.table(
        'properties',
        sa.column('id', sa.UUID),
        sa.column('legacy_price', sa.String),
        sa.column('purchase_price', sa.Numeric)
    )

    # Use connection to execute data transformation
    conn = op.get_bind()
    results = conn.execute(
        sa.select(properties.c.id, properties.c.legacy_price)
        .where(properties.c.legacy_price.isnot(None))
    )

    for row in results:
        # Convert string to numeric
        numeric_price = float(row.legacy_price.replace(',', ''))
        conn.execute(
            properties.update()
            .where(properties.c.id == row.id)
            .values(purchase_price=numeric_price)
        )
```

### 6. Testing Migrations

**Always test migrations before production:**

```bash
# Test upgrade
alembic upgrade head

# Test downgrade (in test environment only!)
alembic downgrade -1

# Test upgrade again
alembic upgrade head

# Check current version
alembic current

# View migration history
alembic history --verbose
```

### 7. Common Patterns for This Project

**Adding Financial Metrics:**
```python
def upgrade() -> None:
    with op.batch_alter_table('properties') as batch_op:
        # Financial columns with precision
        batch_op.add_column(sa.Column('cap_rate', sa.Numeric(5, 4), nullable=True))
        batch_op.add_column(sa.Column('cash_on_cash_return', sa.Numeric(5, 4), nullable=True))
        batch_op.add_column(sa.Column('dscr', sa.Numeric(5, 2), nullable=True))

        # Add check constraints for valid ranges
        batch_op.create_check_constraint(
            'ck_properties_cap_rate_range',
            'cap_rate >= 0 AND cap_rate <= 1'
        )
```

**Adding Audit Fields:**
```python
def upgrade() -> None:
    with op.batch_alter_table('maintenance_requests') as batch_op:
        # Add timestamp fields
        batch_op.add_column(
            sa.Column('created_at', sa.DateTime(timezone=True),
                     server_default=sa.text('now()'), nullable=False)
        )
        batch_op.add_column(
            sa.Column('updated_at', sa.DateTime(timezone=True),
                     server_default=sa.text('now()'), nullable=False)
        )
```

**Adding Relationships:**
```python
def upgrade() -> None:
    with op.batch_alter_table('units') as batch_op:
        batch_op.add_column(
            sa.Column('property_id', postgresql.UUID(as_uuid=True), nullable=False)
        )
        batch_op.create_foreign_key(
            'fk_units_property_id_properties',
            'properties',
            ['property_id'],
            ['id'],
            ondelete='CASCADE'
        )
        batch_op.create_index('ix_units_property_id', ['property_id'])
```

### 8. Migration Safety Checklist

Before applying migrations to production:

- [ ] Migration tested in development environment
- [ ] Both upgrade AND downgrade paths tested
- [ ] Migration is idempotent (can run multiple times safely)
- [ ] No data loss occurs during migration
- [ ] Performance impact assessed (use `EXPLAIN` for data migrations)
- [ ] Backup strategy in place
- [ ] Rollback plan documented
- [ ] Foreign key constraints will not cause issues
- [ ] Default values provided for new NOT NULL columns
- [ ] Indexes created for new foreign keys

### 9. Handling Existing Database

**IMPORTANT:** This project currently uses `create_all()`. To transition to Alembic:

1. **Generate baseline migration:**
```bash
# Create initial migration from current schema
alembic revision --autogenerate -m "initial schema"
```

2. **For existing database, stamp without running:**
```bash
# Mark database as up-to-date without executing migrations
alembic stamp head
```

3. **Future changes use normal workflow:**
```bash
alembic revision --autogenerate -m "add new feature"
alembic upgrade head
```

### 10. Common Issues and Solutions

**Issue: Autogenerate misses changes**
- Solution: Always review generated migrations; autogenerate doesn't detect:
  - Table or column renames (sees as drop + add)
  - Changes to check constraints
  - Enum value changes
  - Server defaults

**Issue: Circular dependencies**
- Solution: Use `use_alter=True` for foreign keys or split into multiple migrations

**Issue: Downgrade fails**
- Solution: Test downgrade in development; some operations can't be reversed (like data deletion)

**Issue: Multiple developers creating migrations**
- Solution: Use branch labels or merge heads:
```bash
# Show heads
alembic heads

# Merge multiple heads
alembic merge -m "merge migrations" head1 head2
```

### 11. Environment-Specific Considerations

**Development:**
- Frequent schema changes are normal
- Can drop/recreate database if needed
- Test both upgrade and downgrade

**Staging:**
- Mirror production data structure
- Test migrations with production-like data volume
- Verify migration performance

**Production:**
- Always backup before migration
- Run migrations during maintenance window
- Monitor migration progress for long-running operations
- Have rollback plan ready

### 12. Integration with FastAPI

Update `backend/app/core/database.py`:

```python
# Remove or comment out init_db() usage in production
# def init_db():
#     Base.metadata.create_all(bind=engine)  # Don't use in production!

# Add migration check instead
def check_migration_status():
    """Verify database is up-to-date with migrations."""
    from alembic.config import Config
    from alembic import script, runtime
    from alembic.runtime.migration import MigrationContext

    config = Config("alembic.ini")
    script_dir = script.ScriptDirectory.from_config(config)

    with engine.begin() as conn:
        context = MigrationContext.configure(conn)
        current_rev = context.get_current_revision()
        head_rev = script_dir.get_current_head()

        if current_rev != head_rev:
            raise RuntimeError(
                f"Database migration required: current={current_rev}, head={head_rev}"
            )
```

## Quick Reference Commands

```bash
# Initialize Alembic
alembic init alembic

# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Rollback to specific revision
alembic downgrade abc123

# Show current version
alembic current

# Show migration history
alembic history --verbose

# Stamp database without running migrations
alembic stamp head

# Show SQL without executing
alembic upgrade head --sql
```

## When to Create Migrations

Create a new migration when you:
- Add/remove/modify table columns
- Add/remove/rename tables
- Change column types or constraints
- Add/remove indexes
- Modify foreign keys
- Change data (data migrations)
- Update enum values

## Red Flags to Watch For

- Large migrations that combine schema + data changes (split them)
- Missing downgrade() implementation
- NOT NULL columns without defaults on existing tables
- Renaming operations detected as drop + create
- Migrations that take > 5 minutes in production
- Circular foreign key dependencies

## Additional Resources

- Alembic documentation: https://alembic.sqlalchemy.org/
- SQLAlchemy types: https://docs.sqlalchemy.org/en/20/core/types.html
- PostgreSQL-specific types: Use `sqlalchemy.dialects.postgresql`

## Task Execution Guidelines

When asked to help with migrations:

1. **Understand the change**: Ask clarifying questions about the schema change
2. **Check current state**: Review existing models and database structure
3. **Generate migration**: Use autogenerate or create manual migration
4. **Review carefully**: Check for autogenerate limitations
5. **Test locally**: Ensure upgrade and downgrade work
6. **Document**: Add clear comments explaining the change
7. **Provide guidance**: Explain how to apply the migration safely
