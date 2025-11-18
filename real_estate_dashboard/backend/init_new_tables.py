"""
Script to initialize new database tables for Portfolio Analytics and Interactive Dashboards.
"""
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import init_db, check_db_connection

def main():
    """Initialize new database tables."""
    print("=" * 60)
    print("Database Table Initialization")
    print("=" * 60)

    # Check database connection
    print("\n1. Checking database connection...")
    if not check_db_connection():
        print("❌ Database connection failed!")
        print("Please check your database settings in .env file")
        return 1

    print("✅ Database connection successful")

    # Initialize tables
    print("\n2. Creating new database tables...")
    print("   - Portfolio Analytics tables:")
    print("     * portfolio_snapshots")
    print("     * portfolio_performance_metrics")
    print("     * cash_flow_projections")
    print("     * portfolio_risk_metrics")
    print("     * geographic_performance")
    print("   - Interactive Dashboards tables:")
    print("     * dashboards")
    print("     * dashboard_widgets")
    print("     * custom_kpis")
    print("     * benchmarks")
    print("     * performance_attribution")
    print("     * dashboard_filters")

    try:
        init_db()
        print("\n✅ Database tables created successfully!")
        print("\nThe following features are now available:")
        print("  • Portfolio Analytics API: /api/v1/portfolio-analytics/*")
        print("  • Interactive Dashboards API: /api/v1/dashboards/*")

    except Exception as e:
        print(f"\n❌ Error creating tables: {e}")
        import traceback
        traceback.print_exc()
        return 1

    print("\n" + "=" * 60)
    print("Initialization Complete!")
    print("=" * 60)
    return 0

if __name__ == "__main__":
    exit(main())
