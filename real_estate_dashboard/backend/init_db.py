#!/usr/bin/env python3
"""
Database Initialization Script

This script initializes the database by creating all tables.
Run this script whenever you add new models or need to recreate the database.

Usage:
    python init_db.py
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.database import init_db, check_db_connection

def main():
    """Initialize the database with all tables."""
    print("=" * 60)
    print("🗄️  Database Initialization")
    print("=" * 60)

    print("\n1️⃣  Checking database connection...")
    if not check_db_connection():
        print("❌ Database connection failed!")
        print("   Please check your database configuration in .env")
        sys.exit(1)

    print("✅ Database connection successful!")

    print("\n2️⃣  Creating all tables...")
    try:
        init_db()
        print("✅ All tables created successfully!")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("🎉 Database initialization complete!")
    print("=" * 60)
    print("\nYou can now start your application:")
    print("  uvicorn app.main:app --reload")
    print()

if __name__ == "__main__":
    main()
