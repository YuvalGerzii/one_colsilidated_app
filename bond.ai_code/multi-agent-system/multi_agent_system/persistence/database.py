"""
Database persistence layer using SQLite.

Provides persistent storage for tasks, results, agent states, and memories.
"""

import sqlite3
import json
import pickle
from typing import Any, Dict, List, Optional
from datetime import datetime
from pathlib import Path
from contextlib import contextmanager
from loguru import logger

from multi_agent_system.core.types import Task, Result, TaskStatus


class DatabaseManager:
    """
    Database manager for persistent storage.

    Uses SQLite for local persistence of all system data.
    """

    def __init__(self, db_path: str = "./data/multi_agent_system.db"):
        """
        Initialize database manager.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self._init_database()

        logger.info(f"DatabaseManager initialized with database: {self.db_path}")

    @contextmanager
    def _get_connection(self):
        """Get database connection context manager."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _init_database(self) -> None:
        """Initialize database schema."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Tasks table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id TEXT PRIMARY KEY,
                    description TEXT NOT NULL,
                    requirements TEXT,  -- JSON array
                    context TEXT,  -- JSON object
                    priority INTEGER DEFAULT 1,
                    deadline TEXT,  -- ISO format
                    status TEXT NOT NULL,
                    assigned_to TEXT,
                    parent_task_id TEXT,
                    subtasks TEXT,  -- JSON array
                    created_at TEXT NOT NULL,
                    started_at TEXT,
                    completed_at TEXT,
                    metadata TEXT,  -- JSON object
                    FOREIGN KEY (parent_task_id) REFERENCES tasks(id)
                )
            """)

            # Results table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT NOT NULL,
                    success INTEGER NOT NULL,  -- Boolean as 0/1
                    data TEXT,  -- JSON or pickled
                    error TEXT,
                    agent_id TEXT NOT NULL,
                    execution_time REAL,
                    quality_score REAL,
                    metadata TEXT,  -- JSON object
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (task_id) REFERENCES tasks(id)
                )
            """)

            # Agent states table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS agent_states (
                    agent_id TEXT PRIMARY KEY,
                    status TEXT NOT NULL,
                    current_task TEXT,
                    completed_tasks INTEGER DEFAULT 0,
                    failed_tasks INTEGER DEFAULT 0,
                    average_execution_time REAL DEFAULT 0.0,
                    last_active TEXT,
                    capabilities TEXT,  -- JSON array
                    performance_score REAL DEFAULT 1.0,
                    metadata TEXT,  -- JSON object
                    updated_at TEXT NOT NULL
                )
            """)

            # Memories table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_id TEXT NOT NULL,
                    key TEXT NOT NULL,
                    value TEXT NOT NULL,  -- Pickled
                    importance REAL DEFAULT 0.5,
                    memory_type TEXT NOT NULL,  -- 'short_term' or 'long_term'
                    context TEXT,  -- JSON object
                    created_at TEXT NOT NULL,
                    accessed_at TEXT NOT NULL,
                    access_count INTEGER DEFAULT 0,
                    UNIQUE(agent_id, key, memory_type)
                )
            """)

            # Learning data table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS learning_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_id TEXT NOT NULL,
                    algorithm TEXT NOT NULL,  -- 'q_learning' or 'policy_gradient'
                    episode INTEGER,
                    state TEXT NOT NULL,  -- JSON or pickled
                    action TEXT NOT NULL,
                    reward REAL NOT NULL,
                    next_state TEXT NOT NULL,
                    done INTEGER NOT NULL,  -- Boolean
                    created_at TEXT NOT NULL
                )
            """)

            # System metrics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS system_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_name TEXT NOT NULL,
                    metric_value REAL NOT NULL,
                    tags TEXT,  -- JSON object
                    timestamp TEXT NOT NULL
                )
            """)

            # Create indexes for performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_tasks_status
                ON tasks(status)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_results_task_id
                ON results(task_id)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_memories_agent_id
                ON memories(agent_id)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_learning_agent_id
                ON learning_data(agent_id)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_metrics_name_time
                ON system_metrics(metric_name, timestamp)
            """)

        logger.info("Database schema initialized")

    # ===== Task Persistence =====

    def save_task(self, task: Task) -> None:
        """
        Save a task to database.

        Args:
            task: Task to save
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT OR REPLACE INTO tasks (
                    id, description, requirements, context, priority,
                    deadline, status, assigned_to, parent_task_id, subtasks,
                    created_at, started_at, completed_at, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                task.id,
                task.description,
                json.dumps(task.requirements),
                json.dumps(task.context),
                task.priority,
                task.deadline.isoformat() if task.deadline else None,
                task.status.value,
                task.assigned_to,
                task.parent_task_id,
                json.dumps(task.subtasks),
                task.created_at.isoformat(),
                task.started_at.isoformat() if task.started_at else None,
                task.completed_at.isoformat() if task.completed_at else None,
                json.dumps(task.metadata),
            ))

        logger.debug(f"Saved task: {task.id}")

    def load_task(self, task_id: str) -> Optional[Task]:
        """
        Load a task from database.

        Args:
            task_id: Task ID

        Returns:
            Task instance or None
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()

            if not row:
                return None

            return Task(
                id=row["id"],
                description=row["description"],
                requirements=json.loads(row["requirements"]),
                context=json.loads(row["context"]),
                priority=row["priority"],
                deadline=datetime.fromisoformat(row["deadline"]) if row["deadline"] else None,
                status=TaskStatus(row["status"]),
                assigned_to=row["assigned_to"],
                parent_task_id=row["parent_task_id"],
                subtasks=json.loads(row["subtasks"]),
                created_at=datetime.fromisoformat(row["created_at"]),
                started_at=datetime.fromisoformat(row["started_at"]) if row["started_at"] else None,
                completed_at=datetime.fromisoformat(row["completed_at"]) if row["completed_at"] else None,
                metadata=json.loads(row["metadata"]),
            )

    def query_tasks(
        self,
        status: Optional[TaskStatus] = None,
        assigned_to: Optional[str] = None,
        limit: int = 100,
    ) -> List[Task]:
        """
        Query tasks with filters.

        Args:
            status: Filter by status
            assigned_to: Filter by assigned agent
            limit: Maximum results

        Returns:
            List of tasks
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()

            query = "SELECT * FROM tasks WHERE 1=1"
            params = []

            if status:
                query += " AND status = ?"
                params.append(status.value)

            if assigned_to:
                query += " AND assigned_to = ?"
                params.append(assigned_to)

            query += " ORDER BY created_at DESC LIMIT ?"
            params.append(limit)

            cursor.execute(query, params)
            rows = cursor.fetchall()

            tasks = []
            for row in rows:
                task = Task(
                    id=row["id"],
                    description=row["description"],
                    requirements=json.loads(row["requirements"]),
                    context=json.loads(row["context"]),
                    priority=row["priority"],
                    status=TaskStatus(row["status"]),
                    assigned_to=row["assigned_to"],
                    created_at=datetime.fromisoformat(row["created_at"]),
                )
                tasks.append(task)

            return tasks

    # ===== Result Persistence =====

    def save_result(self, result: Result) -> None:
        """Save a result to database."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Serialize data
            data_str = json.dumps(result.data) if result.data else None

            cursor.execute("""
                INSERT INTO results (
                    task_id, success, data, error, agent_id,
                    execution_time, quality_score, metadata, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                result.task_id,
                1 if result.success else 0,
                data_str,
                result.error,
                result.agent_id,
                result.execution_time,
                result.quality_score,
                json.dumps(result.metadata),
                result.created_at.isoformat(),
            ))

        logger.debug(f"Saved result for task: {result.task_id}")

    def load_results(self, task_id: str) -> List[Result]:
        """Load all results for a task."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT * FROM results WHERE task_id = ? ORDER BY created_at DESC
            """, (task_id,))

            rows = cursor.fetchall()

            results = []
            for row in rows:
                result = Result(
                    task_id=row["task_id"],
                    success=bool(row["success"]),
                    data=json.loads(row["data"]) if row["data"] else None,
                    error=row["error"],
                    agent_id=row["agent_id"],
                    execution_time=row["execution_time"],
                    quality_score=row["quality_score"],
                    metadata=json.loads(row["metadata"]),
                    created_at=datetime.fromisoformat(row["created_at"]),
                )
                results.append(result)

            return results

    # ===== Memory Persistence =====

    def save_memory(
        self,
        agent_id: str,
        key: str,
        value: Any,
        importance: float,
        memory_type: str,
        context: Optional[Dict] = None,
    ) -> None:
        """Save a memory entry."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Serialize value
            value_str = pickle.dumps(value).hex()

            now = datetime.now().isoformat()

            cursor.execute("""
                INSERT OR REPLACE INTO memories (
                    agent_id, key, value, importance, memory_type,
                    context, created_at, accessed_at, access_count
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                agent_id,
                key,
                value_str,
                importance,
                memory_type,
                json.dumps(context or {}),
                now,
                now,
                0,
            ))

        logger.debug(f"Saved memory for {agent_id}: {key}")

    def load_memories(
        self,
        agent_id: str,
        memory_type: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Load memories for an agent."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            query = "SELECT * FROM memories WHERE agent_id = ?"
            params = [agent_id]

            if memory_type:
                query += " AND memory_type = ?"
                params.append(memory_type)

            query += " ORDER BY accessed_at DESC LIMIT ?"
            params.append(limit)

            cursor.execute(query, params)
            rows = cursor.fetchall()

            memories = []
            for row in rows:
                memories.append({
                    "key": row["key"],
                    "value": pickle.loads(bytes.fromhex(row["value"])),
                    "importance": row["importance"],
                    "memory_type": row["memory_type"],
                    "context": json.loads(row["context"]),
                    "created_at": row["created_at"],
                    "access_count": row["access_count"],
                })

            return memories

    # ===== Statistics =====

    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            stats = {}

            # Count tasks by status
            cursor.execute("""
                SELECT status, COUNT(*) as count
                FROM tasks
                GROUP BY status
            """)
            stats["tasks_by_status"] = {
                row["status"]: row["count"] for row in cursor.fetchall()
            }

            # Total results
            cursor.execute("SELECT COUNT(*) as count FROM results")
            stats["total_results"] = cursor.fetchone()["count"]

            # Total memories
            cursor.execute("SELECT COUNT(*) as count FROM memories")
            stats["total_memories"] = cursor.fetchone()["count"]

            # Total learning data
            cursor.execute("SELECT COUNT(*) as count FROM learning_data")
            stats["total_learning_data"] = cursor.fetchone()["count"]

            return stats

    def cleanup_old_data(self, days: int = 30) -> int:
        """
        Clean up old data.

        Args:
            days: Remove data older than this many days

        Returns:
            Number of rows removed
        """
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        removed = 0

        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Remove old completed tasks
            cursor.execute("""
                DELETE FROM tasks
                WHERE status IN ('completed', 'failed', 'cancelled')
                AND completed_at < ?
            """, (cutoff,))
            removed += cursor.rowcount

            # Remove old metrics
            cursor.execute("""
                DELETE FROM system_metrics
                WHERE timestamp < ?
            """, (cutoff,))
            removed += cursor.rowcount

        logger.info(f"Cleaned up {removed} old database records")
        return removed

    def vacuum(self) -> None:
        """Optimize database by running VACUUM."""
        with self._get_connection() as conn:
            conn.execute("VACUUM")
        logger.info("Database vacuumed")
