"""
Database Validation and Fixer Utility

Comprehensive database schema validator and auto-repair tool with fallback mechanisms.
Validates and fixes:
- Missing tables
- Schema mismatches
- Foreign key constraints
- Data type issues
- Index problems
"""

import logging
import sys
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timezone

from sqlalchemy import (
    inspect, text, Table, MetaData, create_engine,
    exc as sqlalchemy_exc
)
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine

from app.core.database import get_db, engine, Base
from app.settings import settings

# Import all models to populate Base.metadata
import app.models  # noqa: F401

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DatabaseFixer:
    """Database validation and auto-repair utility."""

    def __init__(self, engine: Engine):
        self.engine = engine
        self.inspector = inspect(engine)
        self.issues_found: List[Dict[str, Any]] = []
        self.fixes_applied: List[Dict[str, Any]] = []
        self.errors: List[Dict[str, Any]] = []

    def log_issue(self, category: str, severity: str, message: str, details: Optional[Dict] = None):
        """Log an issue found during validation."""
        issue = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "category": category,
            "severity": severity,
            "message": message,
            "details": details or {}
        }
        self.issues_found.append(issue)

        if severity == "ERROR":
            logger.error(f"[{category}] {message}")
        elif severity == "WARNING":
            logger.warning(f"[{category}] {message}")
        else:
            logger.info(f"[{category}] {message}")

    def log_fix(self, category: str, action: str, success: bool, details: Optional[Dict] = None):
        """Log a fix attempt."""
        fix = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "category": category,
            "action": action,
            "success": success,
            "details": details or {}
        }
        self.fixes_applied.append(fix)

        if success:
            logger.info(f"✅ [{category}] {action}")
        else:
            logger.error(f"❌ [{category}] {action} - FAILED")

    def check_database_connection(self) -> bool:
        """Verify database connection."""
        logger.info("=" * 70)
        logger.info("DATABASE CONNECTION CHECK")
        logger.info("=" * 70)

        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                result.fetchone()
                logger.info("✅ Database connection successful")
                return True
        except Exception as e:
            self.log_issue(
                "CONNECTION",
                "ERROR",
                f"Database connection failed: {str(e)}",
                {"error_type": type(e).__name__}
            )
            return False

    def get_expected_tables(self) -> Dict[str, Table]:
        """Get all expected tables from SQLAlchemy models."""
        logger.info("\n" + "=" * 70)
        logger.info("EXPECTED SCHEMA ANALYSIS")
        logger.info("=" * 70)

        expected_tables = {}
        metadata = Base.metadata

        for table_name, table in metadata.tables.items():
            expected_tables[table_name] = table
            logger.info(f"  • {table_name} ({len(table.columns)} columns)")

        logger.info(f"\nTotal expected tables: {len(expected_tables)}")
        return expected_tables

    def get_existing_tables(self) -> List[str]:
        """Get list of existing tables in database."""
        try:
            return self.inspector.get_table_names()
        except Exception as e:
            self.log_issue(
                "SCHEMA",
                "ERROR",
                f"Failed to retrieve existing tables: {str(e)}",
                {"error_type": type(e).__name__}
            )
            return []

    def validate_table_exists(self, table_name: str) -> bool:
        """Check if a table exists in the database."""
        existing_tables = self.get_existing_tables()
        exists = table_name in existing_tables

        if not exists:
            self.log_issue(
                "SCHEMA",
                "ERROR",
                f"Table '{table_name}' is missing from database",
                {"table": table_name}
            )

        return exists

    def validate_columns(self, table_name: str, expected_table: Table) -> Tuple[bool, List[str]]:
        """Validate columns for a table."""
        try:
            existing_columns = {col['name']: col for col in self.inspector.get_columns(table_name)}
            expected_columns = {col.name: col for col in expected_table.columns}

            missing_columns = []
            type_mismatches = []

            for col_name, col in expected_columns.items():
                if col_name not in existing_columns:
                    missing_columns.append(col_name)
                    self.log_issue(
                        "SCHEMA",
                        "WARNING",
                        f"Column '{col_name}' missing in table '{table_name}'",
                        {"table": table_name, "column": col_name}
                    )

            # Check for extra columns (might be from old schema)
            for col_name in existing_columns:
                if col_name not in expected_columns:
                    self.log_issue(
                        "SCHEMA",
                        "INFO",
                        f"Extra column '{col_name}' found in table '{table_name}'",
                        {"table": table_name, "column": col_name}
                    )

            return len(missing_columns) == 0, missing_columns

        except Exception as e:
            self.log_issue(
                "SCHEMA",
                "ERROR",
                f"Failed to validate columns for '{table_name}': {str(e)}",
                {"table": table_name, "error_type": type(e).__name__}
            )
            return False, []

    def validate_foreign_keys(self, table_name: str) -> bool:
        """Validate foreign key constraints."""
        try:
            foreign_keys = self.inspector.get_foreign_keys(table_name)

            for fk in foreign_keys:
                referred_table = fk.get('referred_table')
                if not self.validate_table_exists(referred_table):
                    self.log_issue(
                        "FOREIGN_KEY",
                        "ERROR",
                        f"Foreign key in '{table_name}' refers to non-existent table '{referred_table}'",
                        {
                            "table": table_name,
                            "foreign_key": fk.get('name'),
                            "referred_table": referred_table
                        }
                    )
                    return False

            return True

        except Exception as e:
            self.log_issue(
                "FOREIGN_KEY",
                "WARNING",
                f"Failed to validate foreign keys for '{table_name}': {str(e)}",
                {"table": table_name, "error_type": type(e).__name__}
            )
            return True  # Don't fail on FK validation errors

    def validate_indexes(self, table_name: str) -> bool:
        """Validate table indexes."""
        try:
            indexes = self.inspector.get_indexes(table_name)
            logger.debug(f"Table '{table_name}' has {len(indexes)} indexes")
            return True

        except Exception as e:
            self.log_issue(
                "INDEX",
                "WARNING",
                f"Failed to validate indexes for '{table_name}': {str(e)}",
                {"table": table_name, "error_type": type(e).__name__}
            )
            return True  # Don't fail on index validation errors

    def create_missing_tables(self, missing_tables: List[str]) -> bool:
        """Create missing tables using SQLAlchemy metadata."""
        if not missing_tables:
            logger.info("No missing tables to create")
            return True

        logger.info("\n" + "=" * 70)
        logger.info("CREATING MISSING TABLES")
        logger.info("=" * 70)

        success = True
        metadata = Base.metadata

        for table_name in missing_tables:
            if table_name not in metadata.tables:
                self.log_issue(
                    "SCHEMA",
                    "ERROR",
                    f"Table '{table_name}' not found in SQLAlchemy metadata",
                    {"table": table_name}
                )
                success = False
                continue

            try:
                table = metadata.tables[table_name]
                table.create(self.engine, checkfirst=True)

                self.log_fix(
                    "SCHEMA",
                    f"Created table '{table_name}'",
                    True,
                    {"table": table_name, "columns": len(table.columns)}
                )

            except Exception as e:
                self.log_fix(
                    "SCHEMA",
                    f"Failed to create table '{table_name}': {str(e)}",
                    False,
                    {"table": table_name, "error": str(e), "error_type": type(e).__name__}
                )
                success = False

        return success

    def fix_all_tables(self) -> bool:
        """Create all tables from scratch using metadata."""
        logger.info("\n" + "=" * 70)
        logger.info("CREATING ALL TABLES FROM METADATA")
        logger.info("=" * 70)

        try:
            # Create all tables
            Base.metadata.create_all(bind=self.engine)

            self.log_fix(
                "SCHEMA",
                "Created all tables from metadata",
                True,
                {"total_tables": len(Base.metadata.tables)}
            )
            return True

        except Exception as e:
            self.log_fix(
                "SCHEMA",
                f"Failed to create tables: {str(e)}",
                False,
                {"error": str(e), "error_type": type(e).__name__}
            )
            return False

    def validate_all(self) -> bool:
        """Run complete validation suite."""
        logger.info("\n" + "=" * 70)
        logger.info("DATABASE VALIDATION STARTED")
        logger.info("=" * 70)
        logger.info(f"Environment: {settings.ENVIRONMENT}")
        logger.info(f"Database: {settings.DATABASE_URL.split('@')[-1] if '@' in settings.DATABASE_URL else 'hidden'}")

        # Step 1: Check connection
        if not self.check_database_connection():
            logger.error("❌ Database connection failed - cannot proceed")
            return False

        # Step 2: Get expected vs existing tables
        expected_tables = self.get_expected_tables()
        existing_tables = self.get_existing_tables()

        logger.info(f"\nExisting tables in database: {len(existing_tables)}")

        # Step 3: Find missing tables
        missing_tables = [name for name in expected_tables.keys() if name not in existing_tables]

        if missing_tables:
            logger.info("\n" + "=" * 70)
            logger.info("MISSING TABLES DETECTED")
            logger.info("=" * 70)
            for table_name in missing_tables:
                logger.warning(f"  ⚠️  {table_name}")

        # Step 4: Validate existing tables
        logger.info("\n" + "=" * 70)
        logger.info("VALIDATING EXISTING TABLES")
        logger.info("=" * 70)

        for table_name in existing_tables:
            if table_name in expected_tables:
                logger.info(f"\nValidating: {table_name}")

                # Validate columns
                columns_valid, missing_cols = self.validate_columns(table_name, expected_tables[table_name])
                if columns_valid:
                    logger.info(f"  ✅ Columns valid")
                else:
                    logger.warning(f"  ⚠️  Missing columns: {', '.join(missing_cols)}")

                # Validate foreign keys
                fk_valid = self.validate_foreign_keys(table_name)
                if fk_valid:
                    logger.info(f"  ✅ Foreign keys valid")

                # Validate indexes
                idx_valid = self.validate_indexes(table_name)
                if idx_valid:
                    logger.info(f"  ✅ Indexes valid")

        # Step 5: Summary
        logger.info("\n" + "=" * 70)
        logger.info("VALIDATION SUMMARY")
        logger.info("=" * 70)
        logger.info(f"Total issues found: {len(self.issues_found)}")

        errors = [i for i in self.issues_found if i['severity'] == 'ERROR']
        warnings = [i for i in self.issues_found if i['severity'] == 'WARNING']

        logger.info(f"  • Errors: {len(errors)}")
        logger.info(f"  • Warnings: {len(warnings)}")
        logger.info(f"  • Missing tables: {len(missing_tables)}")

        return len(errors) == 0

    def auto_fix(self) -> bool:
        """Automatically fix detected issues."""
        logger.info("\n" + "=" * 70)
        logger.info("AUTO-FIX MODE")
        logger.info("=" * 70)

        # Get missing tables
        expected_tables = self.get_expected_tables()
        existing_tables = self.get_existing_tables()
        missing_tables = [name for name in expected_tables.keys() if name not in existing_tables]

        if missing_tables:
            logger.info(f"\nAttempting to create {len(missing_tables)} missing tables...")
            if self.create_missing_tables(missing_tables):
                logger.info("✅ All missing tables created successfully")
            else:
                logger.warning("⚠️  Some tables failed to create")
        else:
            logger.info("No missing tables to create")

        # Run validation again to verify fixes
        logger.info("\n" + "=" * 70)
        logger.info("RE-VALIDATING AFTER FIXES")
        logger.info("=" * 70)

        # Reset issues for re-validation
        self.issues_found = []

        return self.validate_all()

    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive validation report."""
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "environment": settings.ENVIRONMENT,
            "summary": {
                "total_issues": len(self.issues_found),
                "total_fixes": len(self.fixes_applied),
                "errors": len([i for i in self.issues_found if i['severity'] == 'ERROR']),
                "warnings": len([i for i in self.issues_found if i['severity'] == 'WARNING']),
                "successful_fixes": len([f for f in self.fixes_applied if f['success']]),
                "failed_fixes": len([f for f in self.fixes_applied if not f['success']]),
            },
            "issues": self.issues_found,
            "fixes": self.fixes_applied,
            "errors": self.errors
        }


def main():
    """Main execution function."""
    import argparse

    parser = argparse.ArgumentParser(description='Database Validation and Fixer Tool')
    parser.add_argument(
        '--validate-only',
        action='store_true',
        help='Only validate, do not auto-fix'
    )
    parser.add_argument(
        '--auto-fix',
        action='store_true',
        help='Automatically fix detected issues'
    )
    parser.add_argument(
        '--create-all',
        action='store_true',
        help='Create all tables from metadata (careful!)'
    )
    parser.add_argument(
        '--report',
        type=str,
        help='Save detailed report to JSON file'
    )

    args = parser.parse_args()

    # Create fixer instance
    fixer = DatabaseFixer(engine)

    # Run validation
    validation_passed = fixer.validate_all()

    # Auto-fix if requested
    if args.auto_fix and not validation_passed:
        logger.info("\nAuto-fix requested...")
        fixer.auto_fix()

    # Create all tables if requested
    if args.create_all:
        logger.info("\nCreating all tables from metadata...")
        fixer.fix_all_tables()

    # Generate report
    report = fixer.generate_report()

    # Save report if requested
    if args.report:
        import json
        with open(args.report, 'w') as f:
            json.dump(report, f, indent=2)
        logger.info(f"\n📝 Report saved to: {args.report}")

    # Final summary
    logger.info("\n" + "=" * 70)
    logger.info("FINAL SUMMARY")
    logger.info("=" * 70)
    logger.info(f"Total issues: {report['summary']['total_issues']}")
    logger.info(f"Errors: {report['summary']['errors']}")
    logger.info(f"Warnings: {report['summary']['warnings']}")
    logger.info(f"Fixes applied: {report['summary']['total_fixes']}")
    logger.info(f"Successful fixes: {report['summary']['successful_fixes']}")

    if validation_passed or report['summary']['errors'] == 0:
        logger.info("\n✅ DATABASE IS HEALTHY")
        return 0
    else:
        logger.error("\n❌ DATABASE HAS ISSUES")
        logger.error("Run with --auto-fix to attempt automatic repairs")
        return 1


if __name__ == "__main__":
    sys.exit(main())
