"""
Country-Specific Database Manager

Manages separate PostgreSQL databases for each country's economic data.
Each country has its own isolated database for better organization and performance.

Database naming: economics_{country_slug}
Example: economics_united_states, economics_china, economics_japan

This provides:
- Complete data isolation per country
- Faster country-specific queries
- Independent scaling per country
- Easier backup/restore per country
"""

import logging
from typing import Dict, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from app.settings import settings

logger = logging.getLogger(__name__)


class CountryDatabaseManager:
    """Manages database connections for country-specific databases"""

    # Country slug to display name mapping
    COUNTRY_NAMES = {
        "united-states": "United States",
        "china": "China",
        "euro-area": "Euro Area",
        "japan": "Japan",
        "germany": "Germany",
        "india": "India",
        "united-kingdom": "United Kingdom",
        "france": "France",
        "russia": "Russia",
        "canada": "Canada",
        "italy": "Italy",
        "brazil": "Brazil",
        "australia": "Australia",
        "south-korea": "South Korea",
        "mexico": "Mexico",
        "spain": "Spain",
        "indonesia": "Indonesia",
        "saudi-arabia": "Saudi Arabia",
        "netherlands": "Netherlands",
        "turkey": "Turkey",
        "switzerland": "Switzerland",
        "taiwan": "Taiwan",
        "poland": "Poland",
    }

    def __init__(self):
        self._engines: Dict[str, any] = {}
        self._session_makers: Dict[str, any] = {}
        self._base_db_url = settings.DATABASE_URL

        # Parse base database URL
        self._parse_base_url()

    def _parse_base_url(self):
        """Parse the base database URL into components"""
        # DATABASE_URL format: postgresql://user:password@host:port/database
        url = self._base_db_url

        # Extract components
        if url.startswith("postgresql://"):
            url = url.replace("postgresql://", "")

        # Split user:password@host:port/database
        if "@" in url:
            auth, rest = url.split("@", 1)
            if ":" in auth:
                self.db_user, self.db_password = auth.split(":", 1)
            else:
                self.db_user = auth
                self.db_password = ""
        else:
            self.db_user = "postgres"
            self.db_password = "postgres"
            rest = url

        # Split host:port/database
        if "/" in rest:
            host_port, _ = rest.split("/", 1)
        else:
            host_port = rest

        if ":" in host_port:
            self.db_host, port_str = host_port.split(":", 1)
            self.db_port = int(port_str)
        else:
            self.db_host = host_port
            self.db_port = 5432

    def get_country_db_name(self, country_slug: str) -> str:
        """Get database name for a country"""
        # Convert country-slug to country_slug for DB name
        clean_slug = country_slug.replace("-", "_")
        return f"economics_{clean_slug}"

    def get_country_db_url(self, country_slug: str) -> str:
        """Get database URL for a specific country"""
        db_name = self.get_country_db_name(country_slug)
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{db_name}"

    def create_country_database(self, country_slug: str) -> bool:
        """
        Create a new database for a country if it doesn't exist

        Args:
            country_slug: Country identifier (e.g., "united-states")

        Returns:
            True if created or already exists, False on error
        """
        db_name = self.get_country_db_name(country_slug)

        try:
            # Connect to PostgreSQL server (not specific database)
            conn = psycopg2.connect(
                host=self.db_host,
                port=self.db_port,
                user=self.db_user,
                password=self.db_password,
                database="postgres"  # Connect to default postgres database
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()

            # Check if database exists
            cursor.execute(
                "SELECT 1 FROM pg_database WHERE datname = %s",
                (db_name,)
            )
            exists = cursor.fetchone()

            if not exists:
                # Create database
                cursor.execute(f'CREATE DATABASE "{db_name}"')
                logger.info(f"✓ Created database: {db_name}")
            else:
                logger.info(f"✓ Database already exists: {db_name}")

            cursor.close()
            conn.close()
            return True

        except Exception as e:
            logger.error(f"Error creating database {db_name}: {str(e)}")
            return False

    def get_engine(self, country_slug: str):
        """
        Get SQLAlchemy engine for a country's database

        Args:
            country_slug: Country identifier

        Returns:
            SQLAlchemy engine instance
        """
        if country_slug not in self._engines:
            db_url = self.get_country_db_url(country_slug)
            self._engines[country_slug] = create_engine(
                db_url,
                poolclass=NullPool,  # Don't pool connections for country DBs
                echo=False
            )

        return self._engines[country_slug]

    def get_session_maker(self, country_slug: str):
        """
        Get SQLAlchemy session maker for a country's database

        Args:
            country_slug: Country identifier

        Returns:
            SQLAlchemy sessionmaker instance
        """
        if country_slug not in self._session_makers:
            engine = self.get_engine(country_slug)
            self._session_makers[country_slug] = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=engine
            )

        return self._session_makers[country_slug]

    def get_session(self, country_slug: str) -> Session:
        """
        Get a database session for a country

        Args:
            country_slug: Country identifier

        Returns:
            SQLAlchemy session
        """
        session_maker = self.get_session_maker(country_slug)
        return session_maker()

    def create_tables(self, country_slug: str) -> bool:
        """
        Create all economics tables in a country's database

        Args:
            country_slug: Country identifier

        Returns:
            True on success, False on error
        """
        try:
            from app.models.economics import Base

            engine = self.get_engine(country_slug)
            Base.metadata.create_all(bind=engine)

            logger.info(f"✓ Created tables in database: {self.get_country_db_name(country_slug)}")
            return True

        except Exception as e:
            logger.error(f"Error creating tables for {country_slug}: {str(e)}")
            return False

    def initialize_country_database(self, country_slug: str) -> bool:
        """
        Complete initialization: create database + create tables

        Args:
            country_slug: Country identifier

        Returns:
            True on success, False on error
        """
        # Step 1: Create database
        if not self.create_country_database(country_slug):
            return False

        # Step 2: Create tables
        if not self.create_tables(country_slug):
            return False

        country_name = self.COUNTRY_NAMES.get(country_slug, country_slug)
        logger.info(f"✅ Initialized database for {country_name}")
        return True

    def initialize_all_databases(self) -> Dict[str, bool]:
        """
        Initialize databases for all countries

        Returns:
            Dict mapping country_slug to success status
        """
        results = {}

        print("\n" + "=" * 80)
        print("INITIALIZING COUNTRY DATABASES")
        print("=" * 80)

        for country_slug, country_name in self.COUNTRY_NAMES.items():
            print(f"\n📊 {country_name} ({country_slug})...")
            success = self.initialize_country_database(country_slug)
            results[country_slug] = success

            if success:
                print(f"   ✅ Database: {self.get_country_db_name(country_slug)}")
            else:
                print(f"   ❌ Failed to initialize")

        print("\n" + "=" * 80)
        successful = sum(1 for v in results.values() if v)
        total = len(results)
        print(f"SUMMARY: {successful}/{total} country databases initialized")
        print("=" * 80 + "\n")

        return results

    def list_country_databases(self) -> list:
        """
        List all country databases that exist

        Returns:
            List of (country_slug, db_name, exists) tuples
        """
        databases = []

        try:
            conn = psycopg2.connect(
                host=self.db_host,
                port=self.db_port,
                user=self.db_user,
                password=self.db_password,
                database="postgres"
            )
            cursor = conn.cursor()

            for country_slug in self.COUNTRY_NAMES.keys():
                db_name = self.get_country_db_name(country_slug)
                cursor.execute(
                    "SELECT 1 FROM pg_database WHERE datname = %s",
                    (db_name,)
                )
                exists = cursor.fetchone() is not None
                databases.append((country_slug, db_name, exists))

            cursor.close()
            conn.close()

        except Exception as e:
            logger.error(f"Error listing databases: {str(e)}")

        return databases

    def drop_country_database(self, country_slug: str) -> bool:
        """
        Drop a country's database (CAUTION: This deletes all data!)

        Args:
            country_slug: Country identifier

        Returns:
            True on success, False on error
        """
        db_name = self.get_country_db_name(country_slug)

        try:
            # Close any existing connections
            if country_slug in self._engines:
                self._engines[country_slug].dispose()
                del self._engines[country_slug]
            if country_slug in self._session_makers:
                del self._session_makers[country_slug]

            # Connect and drop
            conn = psycopg2.connect(
                host=self.db_host,
                port=self.db_port,
                user=self.db_user,
                password=self.db_password,
                database="postgres"
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()

            # Terminate existing connections to the database
            cursor.execute(f"""
                SELECT pg_terminate_backend(pid)
                FROM pg_stat_activity
                WHERE datname = '{db_name}' AND pid <> pg_backend_pid()
            """)

            # Drop database
            cursor.execute(f'DROP DATABASE IF EXISTS "{db_name}"')
            logger.info(f"✓ Dropped database: {db_name}")

            cursor.close()
            conn.close()
            return True

        except Exception as e:
            logger.error(f"Error dropping database {db_name}: {str(e)}")
            return False


# Global instance
country_db_manager = CountryDatabaseManager()
