"""
Add database indexes for performance optimization.

This script adds missing indexes to improve query performance across all tables.
Indexes are added for:
- Foreign keys (if not already indexed)
- Commonly filtered fields (status, dates, types)
- Composite indexes for common query patterns
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text, Index
from app.settings import settings


def main():
    """Add performance indexes to database."""
    engine = create_engine(settings.DATABASE_URL)

    print("=" * 60)
    print("Adding Performance Indexes")
    print("=" * 60)

    # List of indexes to create
    # Format: (table_name, index_name, columns, is_unique)
    indexes_to_create = [
        # Properties table (note: no company_id in this table)
        ("properties", "idx_properties_type_status", ["property_type", "status"], False),
        ("properties", "idx_properties_created_at", ["created_at"], False),
        ("properties", "idx_properties_address", ["city", "state"], False),
        ("properties", "idx_properties_purchase_date", ["purchase_date"], False),

        # Units table
        ("units", "idx_units_property_status", ["property_id", "status"], False),
        ("units", "idx_units_rent", ["monthly_rent"], False),

        # Leases table
        ("leases", "idx_leases_unit_dates", ["unit_id", "start_date", "end_date"], False),
        ("leases", "idx_leases_status", ["status"], False),
        ("leases", "idx_leases_end_date", ["end_date"], False),

        # Property financials
        ("property_financials", "idx_propfin_property_year", ["property_id", "year"], False),
        ("property_financials", "idx_propfin_year", ["year"], False),

        # Maintenance requests
        ("maintenance_requests", "idx_maint_property_status", ["property_id", "status"], False),
        ("maintenance_requests", "idx_maint_priority", ["priority"], False),
        ("maintenance_requests", "idx_maint_created", ["created_at"], False),

        # Deals (CRM)
        ("deals", "idx_deals_company_stage", ["company_id", "stage"], False),
        ("deals", "idx_deals_status", ["status"], False),
        ("deals", "idx_deals_close_date", ["expected_close_date"], False),

        # Funds
        ("funds", "idx_funds_company_status", ["company_id", "status"], False),
        ("funds", "idx_funds_vintage", ["vintage_year"], False),

        # Capital calls
        ("capital_calls", "idx_capcalls_fund_status", ["fund_id", "status"], False),
        ("capital_calls", "idx_capcalls_due_date", ["due_date"], False),

        # Distributions
        ("distributions", "idx_dist_fund_date", ["fund_id", "distribution_date"], False),

        # Portfolio investments
        ("portfolio_investments", "idx_portinv_fund_status", ["fund_id", "status"], False),
        ("portfolio_investments", "idx_portinv_company", ["company_id"], False),

        # Loans
        ("loans", "idx_loans_property_status", ["property_id", "status"], False),
        ("loans", "idx_loans_maturity", ["maturity_date"], False),
        ("loans", "idx_loans_lender", ["lender_name"], False),

        # Projects
        ("projects", "idx_projects_company_status", ["company_id", "status"], False),
        ("projects", "idx_projects_dates", ["start_date", "target_end_date"], False),

        # Tasks
        ("tasks", "idx_tasks_project_status", ["project_id", "status"], False),
        ("tasks", "idx_tasks_priority", ["priority"], False),
        ("tasks", "idx_tasks_due_date", ["due_date"], False),
        ("tasks", "idx_tasks_assigned", ["assigned_to_user_id"], False),

        # Saved calculations
        ("saved_calculations", "idx_savedcalc_user_created", ["user_id", "created_at"], False),
        ("saved_calculations", "idx_savedcalc_type", ["model_type"], False),

        # Financial models
        ("hotel_financial_models", "idx_hotel_company", ["company_id"], False),
        ("single_family_rental_models", "idx_sfr_company", ["company_id"], False),
        ("fix_and_flip_models", "idx_faf_company", ["company_id"], False),
        ("small_multifamily_models", "idx_smf_company", ["company_id"], False),
        ("highrise_multifamily_models", "idx_hmf_company", ["company_id"], False),
        ("mixed_use_development_models", "idx_mud_company", ["company_id"], False),

        # Model templates
        ("model_templates", "idx_templates_type_public", ["model_type", "is_public"], False),
        ("model_templates", "idx_templates_created", ["created_by_user_id"], False),

        # Portfolio analytics
        ("portfolio_snapshots", "idx_portsnap_company_date", ["company_id", "snapshot_date"], False),
        ("portfolio_performance_metrics", "idx_portperf_snap_type", ["snapshot_id", "metric_type"], False),
        ("cash_flow_projections", "idx_cashflow_snap_month", ["snapshot_id", "projection_month"], False),
        ("portfolio_risk_metrics", "idx_portrisk_snap_type", ["snapshot_id", "risk_type"], False),
        ("geographic_performance", "idx_geoperf_snap_region", ["snapshot_id", "region"], False),

        # Interactive dashboards
        ("dashboards", "idx_dashboards_user_type", ["user_id", "dashboard_type"], False),
        ("dashboard_widgets", "idx_widgets_dashboard", ["dashboard_id"], False),
        ("custom_kpis", "idx_kpis_company", ["company_id"], False),
        ("benchmarks", "idx_benchmarks_type_source", ["benchmark_type", "data_source"], False),

        # Market intelligence
        ("census_data", "idx_census_location_year", ["state", "county", "year"], False),
        ("bls_employment", "idx_bls_location_date", ["state", "metro_area", "date"], False),
        ("hud_fair_market_rents", "idx_hud_location_year", ["state", "county_name", "year"], False),

        # Accounting
        ("accounting_profiles", "idx_accprof_company", ["company_id"], False),
        ("chart_of_accounts", "idx_coa_profile_code", ["accounting_profile_id", "account_code"], False),
        ("accounting_transactions", "idx_acctrans_profile_date", ["accounting_profile_id", "transaction_date"], False),
        ("accounting_transactions", "idx_acctrans_type", ["transaction_type"], False),

        # PDF documents
        ("pdf_documents", "idx_pdfdocs_company_type", ["company_id", "document_type"], False),
        ("pdf_documents", "idx_pdfdocs_uploaded", ["uploaded_at"], False),

        # Reports
        ("reports", "idx_reports_company_type", ["company_id", "report_type"], False),
        ("reports", "idx_reports_generated", ["generated_at"], False),
    ]

    created_count = 0
    skipped_count = 0
    error_count = 0

    for table_name, index_name, columns, is_unique in indexes_to_create:
        # Use a new connection for each index to avoid transaction issues
        with engine.connect() as conn:
            try:
                # Check if index already exists
                check_sql = text("""
                    SELECT 1 FROM pg_indexes
                    WHERE tablename = :table_name
                    AND indexname = :index_name
                """)
                result = conn.execute(check_sql, {"table_name": table_name, "index_name": index_name}).fetchone()

                if result:
                    print(f"✓ Index '{index_name}' already exists, skipping...")
                    skipped_count += 1
                    continue

                # Check if table exists
                table_check = text(f"SELECT to_regclass('{table_name}')")
                table_exists = conn.execute(table_check).scalar()

                if not table_exists:
                    print(f"⚠️  Table '{table_name}' doesn't exist, skipping index '{index_name}'")
                    skipped_count += 1
                    continue

                # Create index
                columns_str = ", ".join(columns)
                unique_str = "UNIQUE " if is_unique else ""
                create_sql = text(f"""
                    CREATE {unique_str}INDEX {index_name}
                    ON {table_name} ({columns_str})
                """)

                conn.execute(create_sql)
                conn.commit()
                print(f"✅ Created index: {index_name} on {table_name}({columns_str})")
                created_count += 1

            except Exception as e:
                error_count += 1
                # Try to get the specific error from the exception
                error_msg = str(e).split('\n')[0] if '\n' in str(e) else str(e)
                print(f"❌ Error creating {index_name}: {error_msg}")
                conn.rollback()
                continue

    print("\n" + "=" * 60)
    print("Index Creation Summary")
    print("=" * 60)
    print(f"✅ Created: {created_count}")
    print(f"✓ Skipped (already exists): {skipped_count}")
    print(f"❌ Errors: {error_count}")
    print("=" * 60)

    return 0 if error_count == 0 else 1


if __name__ == "__main__":
    exit(main())
