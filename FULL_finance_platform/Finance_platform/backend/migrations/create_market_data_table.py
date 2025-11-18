"""
Database migration script for market_data table

Run this script to create the market_data table in your PostgreSQL database.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import engine, Base
from app.models.market_data import MarketData
from app.models.company import PortfolioCompany
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_market_data_table():
    """Create the market_data table."""
    try:
        logger.info("Creating market_data table...")

        # Create all tables (this will only create tables that don't exist)
        Base.metadata.create_all(bind=engine, tables=[MarketData.__table__])

        logger.info("✅ Successfully created market_data table")

        # Print table info
        logger.info("\nTable: market_data")
        logger.info("Columns:")
        for column in MarketData.__table__.columns:
            logger.info(f"  - {column.name}: {column.type}")

        return True

    except Exception as e:
        logger.error(f"❌ Error creating market_data table: {str(e)}")
        return False


def verify_table():
    """Verify the market_data table exists."""
    try:
        from sqlalchemy import inspect

        inspector = inspect(engine)
        tables = inspector.get_table_names()

        if 'market_data' in tables:
            logger.info("✅ market_data table exists")

            # Show columns
            columns = inspector.get_columns('market_data')
            logger.info(f"\nTable has {len(columns)} columns:")
            for col in columns:
                logger.info(f"  - {col['name']}: {col['type']}")

            return True
        else:
            logger.error("❌ market_data table does not exist")
            return False

    except Exception as e:
        logger.error(f"❌ Error verifying table: {str(e)}")
        return False


if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("Market Data Table Migration")
    logger.info("=" * 60)

    # Create table
    if create_market_data_table():
        # Verify table
        verify_table()
        logger.info("\n✅ Migration completed successfully!")
    else:
        logger.error("\n❌ Migration failed!")
        sys.exit(1)
