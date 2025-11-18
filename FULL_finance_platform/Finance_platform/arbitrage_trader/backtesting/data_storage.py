"""
Historical data storage system for caching and managing market data.
"""
import json
import os
import logging
import sqlite3
import pickle
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from pathlib import Path
from decimal import Decimal


class DataStorage:
    """Base class for data storage implementations."""

    def save(self, key: str, data: List[Dict], metadata: Dict = None):
        """Save data to storage."""
        raise NotImplementedError

    def load(self, key: str) -> Optional[List[Dict]]:
        """Load data from storage."""
        raise NotImplementedError

    def exists(self, key: str) -> bool:
        """Check if data exists."""
        raise NotImplementedError

    def delete(self, key: str):
        """Delete data from storage."""
        raise NotImplementedError

    def list_keys(self) -> List[str]:
        """List all stored keys."""
        raise NotImplementedError


class FileStorage(DataStorage):
    """File-based data storage using JSON files."""

    def __init__(self, base_path: str = None):
        """
        Initialize file storage.

        Args:
            base_path: Base directory for storing data files
        """
        if base_path is None:
            base_path = os.path.join(os.path.expanduser("~"), ".arbitrage_trader", "data")

        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger(__name__)

    def _get_file_path(self, key: str) -> Path:
        """Get file path for a key."""
        # Sanitize key for filename
        safe_key = key.replace("/", "_").replace("\\", "_").replace(":", "_")
        return self.base_path / f"{safe_key}.json"

    def save(self, key: str, data: List[Dict], metadata: Dict = None):
        """
        Save data to file.

        Args:
            key: Storage key (e.g., "BTCUSDT_binance_1h")
            data: List of OHLCV data points
            metadata: Optional metadata
        """
        file_path = self._get_file_path(key)

        storage_obj = {
            "key": key,
            "timestamp": datetime.now().isoformat(),
            "count": len(data),
            "metadata": metadata or {},
            "data": data
        }

        with open(file_path, "w") as f:
            json.dump(storage_obj, f, indent=2, default=str)

        self.logger.info(f"Saved {len(data)} records to {file_path}")

    def load(self, key: str) -> Optional[List[Dict]]:
        """
        Load data from file.

        Args:
            key: Storage key

        Returns:
            List of data points or None if not found
        """
        file_path = self._get_file_path(key)

        if not file_path.exists():
            return None

        try:
            with open(file_path, "r") as f:
                storage_obj = json.load(f)

            return storage_obj.get("data", [])

        except Exception as e:
            self.logger.error(f"Error loading {key}: {e}")
            return None

    def exists(self, key: str) -> bool:
        """Check if data exists."""
        return self._get_file_path(key).exists()

    def delete(self, key: str):
        """Delete data file."""
        file_path = self._get_file_path(key)
        if file_path.exists():
            file_path.unlink()
            self.logger.info(f"Deleted {file_path}")

    def list_keys(self) -> List[str]:
        """List all stored keys."""
        keys = []
        for file_path in self.base_path.glob("*.json"):
            key = file_path.stem
            keys.append(key)
        return keys

    def get_metadata(self, key: str) -> Optional[Dict]:
        """Get metadata for a key."""
        file_path = self._get_file_path(key)

        if not file_path.exists():
            return None

        try:
            with open(file_path, "r") as f:
                storage_obj = json.load(f)

            return {
                "timestamp": storage_obj.get("timestamp"),
                "count": storage_obj.get("count"),
                **storage_obj.get("metadata", {})
            }

        except Exception as e:
            self.logger.error(f"Error loading metadata for {key}: {e}")
            return None


class SQLiteStorage(DataStorage):
    """SQLite-based data storage for efficient querying."""

    def __init__(self, db_path: str = None):
        """
        Initialize SQLite storage.

        Args:
            db_path: Path to SQLite database file
        """
        if db_path is None:
            base_path = os.path.join(os.path.expanduser("~"), ".arbitrage_trader", "data")
            os.makedirs(base_path, exist_ok=True)
            db_path = os.path.join(base_path, "historical_data.db")

        self.db_path = db_path
        self.logger = logging.getLogger(__name__)

        self._init_db()

    def _init_db(self):
        """Initialize database tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS data_series (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ohlcv_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                series_id INTEGER NOT NULL,
                timestamp INTEGER NOT NULL,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume REAL,
                extra TEXT,
                FOREIGN KEY (series_id) REFERENCES data_series(id),
                UNIQUE(series_id, timestamp)
            )
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_ohlcv_timestamp
            ON ohlcv_data(series_id, timestamp)
        """)

        conn.commit()
        conn.close()

    def save(self, key: str, data: List[Dict], metadata: Dict = None):
        """
        Save data to SQLite.

        Args:
            key: Storage key
            data: List of OHLCV data points
            metadata: Optional metadata
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Insert or update series
            cursor.execute("""
                INSERT INTO data_series (key, metadata, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(key) DO UPDATE SET
                    metadata = excluded.metadata,
                    updated_at = CURRENT_TIMESTAMP
            """, (key, json.dumps(metadata or {})))

            # Get series ID
            cursor.execute("SELECT id FROM data_series WHERE key = ?", (key,))
            series_id = cursor.fetchone()[0]

            # Delete existing data for this series
            cursor.execute("DELETE FROM ohlcv_data WHERE series_id = ?", (series_id,))

            # Insert new data
            for bar in data:
                extra = {k: v for k, v in bar.items()
                        if k not in ["timestamp", "open", "high", "low", "close", "volume"]}

                cursor.execute("""
                    INSERT INTO ohlcv_data (series_id, timestamp, open, high, low, close, volume, extra)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    series_id,
                    bar.get("timestamp", 0),
                    bar.get("open", 0),
                    bar.get("high", 0),
                    bar.get("low", 0),
                    bar.get("close", 0),
                    bar.get("volume", 0),
                    json.dumps(extra) if extra else None
                ))

            conn.commit()
            self.logger.info(f"Saved {len(data)} records to SQLite for {key}")

        except Exception as e:
            conn.rollback()
            self.logger.error(f"Error saving {key}: {e}")
            raise

        finally:
            conn.close()

    def load(self, key: str) -> Optional[List[Dict]]:
        """
        Load data from SQLite.

        Args:
            key: Storage key

        Returns:
            List of data points or None if not found
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Get series ID
            cursor.execute("SELECT id FROM data_series WHERE key = ?", (key,))
            result = cursor.fetchone()

            if not result:
                return None

            series_id = result[0]

            # Load data
            cursor.execute("""
                SELECT timestamp, open, high, low, close, volume, extra
                FROM ohlcv_data
                WHERE series_id = ?
                ORDER BY timestamp
            """, (series_id,))

            data = []
            for row in cursor.fetchall():
                bar = {
                    "timestamp": row[0],
                    "open": row[1],
                    "high": row[2],
                    "low": row[3],
                    "close": row[4],
                    "volume": row[5]
                }

                if row[6]:
                    extra = json.loads(row[6])
                    bar.update(extra)

                data.append(bar)

            return data

        except Exception as e:
            self.logger.error(f"Error loading {key}: {e}")
            return None

        finally:
            conn.close()

    def exists(self, key: str) -> bool:
        """Check if data exists."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM data_series WHERE key = ?", (key,))
        result = cursor.fetchone()

        conn.close()
        return result is not None

    def delete(self, key: str):
        """Delete data series."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT id FROM data_series WHERE key = ?", (key,))
            result = cursor.fetchone()

            if result:
                series_id = result[0]
                cursor.execute("DELETE FROM ohlcv_data WHERE series_id = ?", (series_id,))
                cursor.execute("DELETE FROM data_series WHERE id = ?", (series_id,))
                conn.commit()
                self.logger.info(f"Deleted {key}")

        finally:
            conn.close()

    def list_keys(self) -> List[str]:
        """List all stored keys."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT key FROM data_series ORDER BY key")
        keys = [row[0] for row in cursor.fetchall()]

        conn.close()
        return keys

    def query(
        self,
        key: str,
        start_time: int = None,
        end_time: int = None,
        limit: int = None
    ) -> List[Dict]:
        """
        Query data with filters.

        Args:
            key: Storage key
            start_time: Start timestamp (inclusive)
            end_time: End timestamp (inclusive)
            limit: Maximum records to return

        Returns:
            Filtered data points
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Get series ID
            cursor.execute("SELECT id FROM data_series WHERE key = ?", (key,))
            result = cursor.fetchone()

            if not result:
                return []

            series_id = result[0]

            # Build query
            query = """
                SELECT timestamp, open, high, low, close, volume, extra
                FROM ohlcv_data
                WHERE series_id = ?
            """
            params = [series_id]

            if start_time:
                query += " AND timestamp >= ?"
                params.append(start_time)

            if end_time:
                query += " AND timestamp <= ?"
                params.append(end_time)

            query += " ORDER BY timestamp"

            if limit:
                query += " LIMIT ?"
                params.append(limit)

            cursor.execute(query, params)

            data = []
            for row in cursor.fetchall():
                bar = {
                    "timestamp": row[0],
                    "open": row[1],
                    "high": row[2],
                    "low": row[3],
                    "close": row[4],
                    "volume": row[5]
                }

                if row[6]:
                    extra = json.loads(row[6])
                    bar.update(extra)

                data.append(bar)

            return data

        finally:
            conn.close()


class CachedDataProvider:
    """Data provider with caching layer."""

    def __init__(
        self,
        data_provider,
        storage: DataStorage = None,
        cache_duration_hours: int = 24
    ):
        """
        Initialize cached data provider.

        Args:
            data_provider: Underlying data provider
            storage: Storage backend
            cache_duration_hours: Cache validity duration
        """
        self.provider = data_provider
        self.storage = storage or SQLiteStorage()
        self.cache_duration = timedelta(hours=cache_duration_hours)
        self.logger = logging.getLogger(__name__)

    async def get_crypto_historical(
        self,
        symbol: str,
        days: int = 30,
        provider: str = "binance",
        force_refresh: bool = False
    ) -> List[Dict]:
        """Get crypto historical data with caching."""
        key = f"{symbol}_{provider}_{days}d_crypto"

        # Check cache
        if not force_refresh and self.storage.exists(key):
            metadata = None
            if isinstance(self.storage, FileStorage):
                metadata = self.storage.get_metadata(key)

            if metadata:
                cached_time = datetime.fromisoformat(metadata.get("timestamp", ""))
                if datetime.now() - cached_time < self.cache_duration:
                    self.logger.info(f"Using cached data for {key}")
                    return self.storage.load(key)

        # Fetch fresh data
        self.logger.info(f"Fetching fresh data for {key}")
        data = await self.provider.get_crypto_historical(symbol, days, provider)

        if data:
            self.storage.save(key, data, {"symbol": symbol, "provider": provider, "days": days})

        return data

    async def get_stock_historical(
        self,
        symbol: str,
        period: str = "1y",
        provider: str = "yahoo",
        force_refresh: bool = False
    ) -> List[Dict]:
        """Get stock historical data with caching."""
        key = f"{symbol}_{provider}_{period}_stock"

        # Check cache
        if not force_refresh and self.storage.exists(key):
            metadata = None
            if isinstance(self.storage, FileStorage):
                metadata = self.storage.get_metadata(key)

            if metadata:
                cached_time = datetime.fromisoformat(metadata.get("timestamp", ""))
                if datetime.now() - cached_time < self.cache_duration:
                    self.logger.info(f"Using cached data for {key}")
                    return self.storage.load(key)

        # Fetch fresh data
        self.logger.info(f"Fetching fresh data for {key}")
        data = await self.provider.get_stock_historical(symbol, period, provider)

        if data:
            self.storage.save(key, data, {"symbol": symbol, "provider": provider, "period": period})

        return data

    async def get_forex_historical(
        self,
        from_currency: str,
        to_currency: str,
        days: int = 100,
        force_refresh: bool = False
    ) -> List[Dict]:
        """Get forex historical data with caching."""
        key = f"{from_currency}{to_currency}_{days}d_forex"

        # Check cache
        if not force_refresh and self.storage.exists(key):
            metadata = None
            if isinstance(self.storage, FileStorage):
                metadata = self.storage.get_metadata(key)

            if metadata:
                cached_time = datetime.fromisoformat(metadata.get("timestamp", ""))
                if datetime.now() - cached_time < self.cache_duration:
                    self.logger.info(f"Using cached data for {key}")
                    return self.storage.load(key)

        # Fetch fresh data
        self.logger.info(f"Fetching fresh data for {key}")
        data = await self.provider.get_forex_historical(from_currency, to_currency, days)

        if data:
            self.storage.save(key, data, {
                "from_currency": from_currency,
                "to_currency": to_currency,
                "days": days
            })

        return data

    def clear_cache(self, pattern: str = None):
        """
        Clear cached data.

        Args:
            pattern: Optional pattern to match keys
        """
        keys = self.storage.list_keys()

        for key in keys:
            if pattern is None or pattern in key:
                self.storage.delete(key)
                self.logger.info(f"Cleared cache for {key}")
