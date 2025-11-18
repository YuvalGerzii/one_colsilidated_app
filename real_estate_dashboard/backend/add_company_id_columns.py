#!/usr/bin/env python3
"""
Add company_id foreign key columns to all models for multi-tenancy support.

This migration adds company_id columns to:
- Financial Models (DCFModel, LBOModel)
- CRM Models (Deal, Broker, Comp, DealStageRule, EmailTemplate)
- Reports (GeneratedReport, ReportTemplate)
- Debt Management (Loan, LoanComparison)
- Fund Management (Fund, LimitedPartner)

Note: SavedCalculation, Dashboard, CustomKPI already have company_id.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.settings import settings


def check_column_exists(conn, table_name: str, column_name: str) -> bool:
    """Check if a column exists in a table."""
    result = conn.execute(text(f"""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.columns
            WHERE table_name = '{table_name}'
            AND column_name = '{column_name}'
        );
    """))
    return result.scalar()


def add_company_id_column(conn, table_name: str, description: str):
    """Add company_id column to a table."""
    try:
        # Check if column already exists
        if check_column_exists(conn, table_name, 'company_id'):
            print(f"✓ Column company_id already exists in {table_name}, skipping...")
            return True

        # Add the column
        conn.execute(text(f"""
            ALTER TABLE {table_name}
            ADD COLUMN company_id UUID;
        """))

        # Add foreign key constraint
        conn.execute(text(f"""
            ALTER TABLE {table_name}
            ADD CONSTRAINT fk_{table_name}_company_id
            FOREIGN KEY (company_id)
            REFERENCES companies(id)
            ON DELETE CASCADE;
        """))

        # Add index for performance
        conn.execute(text(f"""
            CREATE INDEX IF NOT EXISTS idx_{table_name}_company_id
            ON {table_name}(company_id);
        """))

        # Add comment
        conn.execute(text(f"""
            COMMENT ON COLUMN {table_name}.company_id IS
            'Company this {description} belongs to (for multi-tenancy)';
        """))

        conn.commit()
        print(f"✅ Added company_id to {table_name}")
        return True

    except Exception as e:
        print(f"❌ Error adding company_id to {table_name}: {e}")
        conn.rollback()
        return False


def main():
    """Add company_id columns to all relevant tables."""
    engine = create_engine(settings.DATABASE_URL)

    print("=" * 70)
    print("Adding company_id columns for Multi-Tenancy Support")
    print("=" * 70)

    # Define tables to update with descriptions
    tables_to_update = [
        # Financial Models
        ("dcf_models", "DCF model"),
        ("lbo_models", "LBO model"),

        # CRM Models
        ("deals", "deal"),
        ("brokers", "broker"),
        ("comps", "comparable property"),
        ("deal_stage_rules", "deal stage rule"),
        ("email_templates", "email template"),

        # Reports
        ("generated_reports", "report"),
        ("report_templates", "report template"),

        # Debt Management
        ("loans", "loan"),
        ("loan_comparisons", "loan comparison"),

        # Fund Management
        ("funds", "fund"),
        ("limited_partners", "limited partner"),
    ]

    success_count = 0
    failed_count = 0

    with engine.connect() as conn:
        for table_name, description in tables_to_update:
            # Check if table exists
            result = conn.execute(text(f"SELECT to_regclass('{table_name}')")).scalar()
            if not result:
                print(f"⚠ Table '{table_name}' does not exist, skipping...")
                continue

            if add_company_id_column(conn, table_name, description):
                success_count += 1
            else:
                failed_count += 1

    print("\n" + "=" * 70)
    print(f"Migration Complete!")
    print(f"✅ Successfully updated: {success_count} tables")
    if failed_count > 0:
        print(f"❌ Failed: {failed_count} tables")
    print("=" * 70)

    print("\n📋 Notes:")
    print("  - SavedCalculation, Dashboard, and CustomKPI already had company_id")
    print("  - All new company_id columns are nullable (no default data populated)")
    print("  - Foreign key constraints added with CASCADE delete")
    print("  - Indexes created for query performance")

    return 0 if failed_count == 0 else 1


if __name__ == "__main__":
    exit(main())
