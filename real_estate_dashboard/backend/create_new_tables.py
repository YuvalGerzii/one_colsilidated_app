"""
Generate SQL DDL for new Portfolio Analytics and Interactive Dashboards tables.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.schema import CreateTable
from app.settings import settings
from app.models.portfolio_analytics import (
    PortfolioSnapshot,
    PortfolioPerformanceMetric,
    CashFlowProjection,
    PortfolioRiskMetric,
    GeographicPerformance
)
from app.models.interactive_dashboards import (
    Dashboard,
    DashboardWidget,
    CustomKPI,
    Benchmark,
    PerformanceAttribution,
    DashboardFilter
)

def main():
    """Generate and execute SQL for new tables."""
    engine = create_engine(settings.DATABASE_URL)

    print("=" * 60)
    print("Creating Portfolio Analytics & Interactive Dashboards Tables")
    print("=" * 60)

    tables = [
        # Portfolio Analytics
        PortfolioSnapshot.__table__,
        PortfolioPerformanceMetric.__table__,
        CashFlowProjection.__table__,
        PortfolioRiskMetric.__table__,
        GeographicPerformance.__table__,
        # Interactive Dashboards
        Dashboard.__table__,
        DashboardWidget.__table__,
        CustomKPI.__table__,
        Benchmark.__table__,
        PerformanceAttribution.__table__,
        DashboardFilter.__table__,
    ]

    with engine.connect() as conn:
        for table in tables:
            try:
                # Check if table exists
                result = conn.execute(text(f"SELECT to_regclass('{table.name}')")).scalar()
                if result:
                    print(f"✓ Table '{table.name}' already exists, skipping...")
                    continue

                # Create table
                create_stmt = CreateTable(table, if_not_exists=True)
                conn.execute(create_stmt)
                conn.commit()
                print(f"✅ Created table: {table.name}")
            except Exception as e:
                print(f"❌ Error creating {table.name}: {e}")
                import traceback
                traceback.print_exc()
                continue

    print("\n" + "=" * 60)
    print("Table Creation Complete!")
    print("=" * 60)
    return 0

if __name__ == "__main__":
    exit(main())
