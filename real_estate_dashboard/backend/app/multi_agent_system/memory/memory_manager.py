"""
Memory management system for agents.

Provides short-term and long-term memory with consolidation capabilities.
"""

import asyncio
import pickle
from collections import deque
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
from pathlib import Path
from loguru import logger


class MemoryEntry:
    """A single memory entry."""

    def __init__(
        self,
        key: str,
        value: Any,
        importance: float = 0.5,
        metadata: Optional[Dict] = None,
    ):
        self.key = key
        self.value = value
        self.importance = importance  # 0.0 to 1.0
        self.metadata = metadata or {}
        self.created_at = datetime.now()
        self.accessed_at = datetime.now()
        self.access_count = 0

    def access(self) -> None:
        """Mark this memory as accessed."""
        self.accessed_at = datetime.now()
        self.access_count += 1

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "key": self.key,
            "value": self.value,
            "importance": self.importance,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "accessed_at": self.accessed_at.isoformat(),
            "access_count": self.access_count,
        }


class MemoryManager:
    """
    Memory management system for agents.

    Features:
    - Short-term memory (working memory, limited size)
    - Long-term memory (persistent, unlimited)
    - Memory consolidation (important short-term -> long-term)
    - Memory retrieval with relevance scoring
    """

    def __init__(
        self,
        agent_id: str,
        short_term_size: int = 1000,
        long_term_path: Optional[str] = None,
        consolidation_threshold: float = 0.7,
    ):
        """
        Initialize memory manager.

        Args:
            agent_id: ID of the agent this memory belongs to
            short_term_size: Maximum size of short-term memory
            long_term_path: Path to store long-term memory
            consolidation_threshold: Importance threshold for consolidation
        """
        self.agent_id = agent_id
        self.short_term_size = short_term_size
        self.consolidation_threshold = consolidation_threshold

        # Short-term memory (recent, limited)
        self.short_term: deque = deque(maxlen=short_term_size)
        self.short_term_index: Dict[str, MemoryEntry] = {}

        # Long-term memory (persistent, unlimited)
        self.long_term: Dict[str, MemoryEntry] = {}

        # Shared knowledge base (accessible by all agents)
        self.shared_knowledge: Dict[str, Any] = {}

        # Storage path
        if long_term_path:
            self.storage_path = Path(long_term_path) / f"{agent_id}_memory.pkl"
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            self._load_long_term_memory()
        else:
            self.storage_path = None

        logger.info(f"MemoryManager initialized for agent {agent_id}")

    def store_short_term(
        self, key: str, value: Any, importance: float = 0.5, metadata: Optional[Dict] = None
    ) -> None:
        """
        Store a memory in short-term memory.

        Args:
            key: Memory key/identifier
            value: Memory value
            importance: Importance score (0.0 to 1.0)
            metadata: Additional metadata
        """
        entry = MemoryEntry(key, value, importance, metadata)

        # Add to short-term memory
        self.short_term.append(entry)
        self.short_term_index[key] = entry

        logger.debug(f"Stored short-term memory: {key} (importance={importance})")

        # Auto-consolidate if importance is high
        if importance >= self.consolidation_threshold:
            self._consolidate_memory(entry)

    def store_long_term(
        self, key: str, value: Any, importance: float = 1.0, metadata: Optional[Dict] = None
    ) -> None:
        """
        Store a memory directly in long-term memory.

        Args:
            key: Memory key/identifier
            value: Memory value
            importance: Importance score
            metadata: Additional metadata
        """
        entry = MemoryEntry(key, value, importance, metadata)
        self.long_term[key] = entry

        logger.debug(f"Stored long-term memory: {key}")

        # Persist to disk if path is set
        if self.storage_path:
            self._save_long_term_memory()

    def retrieve(self, key: str) -> Optional[Any]:
        """
        Retrieve a memory by key.

        Searches short-term first, then long-term.

        Args:
            key: Memory key

        Returns:
            Memory value, or None if not found
        """
        # Check short-term first
        if key in self.short_term_index:
            entry = self.short_term_index[key]
            entry.access()
            logger.debug(f"Retrieved from short-term: {key}")
            return entry.value

        # Check long-term
        if key in self.long_term:
            entry = self.long_term[key]
            entry.access()
            logger.debug(f"Retrieved from long-term: {key}")
            return entry.value

        logger.debug(f"Memory not found: {key}")
        return None

    def search(
        self,
        query: str,
        limit: int = 10,
        search_long_term: bool = True,
    ) -> List[MemoryEntry]:
        """
        Search memories by query string.

        Args:
            query: Search query
            limit: Maximum number of results
            search_long_term: Whether to search long-term memory

        Returns:
            List of matching memory entries
        """
        results = []

        # Search short-term
        for entry in self.short_term:
            if query.lower() in str(entry.key).lower() or query.lower() in str(entry.value).lower():
                results.append(entry)

        # Search long-term if requested
        if search_long_term:
            for entry in self.long_term.values():
                if query.lower() in str(entry.key).lower() or query.lower() in str(entry.value).lower():
                    results.append(entry)

        # Sort by importance and access count
        results.sort(
            key=lambda e: (e.importance, e.access_count),
            reverse=True,
        )

        return results[:limit]

    def get_recent_memories(self, limit: int = 10) -> List[MemoryEntry]:
        """
        Get recent memories from short-term storage.

        Args:
            limit: Maximum number of memories to return

        Returns:
            List of recent memory entries
        """
        return list(self.short_term)[-limit:]

    def consolidate_memories(self) -> int:
        """
        Consolidate important short-term memories to long-term.

        Returns:
            Number of memories consolidated
        """
        consolidated = 0

        for entry in list(self.short_term):
            if entry.importance >= self.consolidation_threshold:
                if entry.key not in self.long_term:
                    self._consolidate_memory(entry)
                    consolidated += 1

        if consolidated > 0:
            logger.info(f"Consolidated {consolidated} memories to long-term storage")

        return consolidated

    def _consolidate_memory(self, entry: MemoryEntry) -> None:
        """Move a memory entry to long-term storage."""
        self.long_term[entry.key] = entry

        if self.storage_path:
            self._save_long_term_memory()

    def clear_short_term(self) -> None:
        """Clear all short-term memories."""
        self.short_term.clear()
        self.short_term_index.clear()
        logger.info("Cleared short-term memory")

    def clear_long_term(self) -> None:
        """Clear all long-term memories."""
        self.long_term.clear()

        if self.storage_path and self.storage_path.exists():
            self.storage_path.unlink()

        logger.info("Cleared long-term memory")

    def get_statistics(self) -> Dict[str, Any]:
        """Get memory statistics."""
        return {
            "short_term_count": len(self.short_term),
            "short_term_capacity": self.short_term_size,
            "long_term_count": len(self.long_term),
            "total_memories": len(self.short_term) + len(self.long_term),
            "shared_knowledge_count": len(self.shared_knowledge),
        }

    def _save_long_term_memory(self) -> None:
        """Persist long-term memory to disk."""
        if not self.storage_path:
            return

        try:
            with open(self.storage_path, "wb") as f:
                pickle.dump(self.long_term, f)
            logger.debug(f"Saved long-term memory to {self.storage_path}")
        except Exception as e:
            logger.error(f"Failed to save long-term memory: {e}")

    def _load_long_term_memory(self) -> None:
        """Load long-term memory from disk."""
        if not self.storage_path or not self.storage_path.exists():
            return

        try:
            with open(self.storage_path, "rb") as f:
                self.long_term = pickle.load(f)
            logger.info(f"Loaded {len(self.long_term)} long-term memories from disk")
        except Exception as e:
            logger.error(f"Failed to load long-term memory: {e}")

    # Shared knowledge methods
    def share_knowledge(self, key: str, value: Any) -> None:
        """
        Share knowledge with all agents.

        Args:
            key: Knowledge key
            value: Knowledge value
        """
        self.shared_knowledge[key] = value
        logger.debug(f"Shared knowledge: {key}")

    def get_shared_knowledge(self, key: str) -> Optional[Any]:
        """
        Get shared knowledge.

        Args:
            key: Knowledge key

        Returns:
            Knowledge value, or None if not found
        """
        return self.shared_knowledge.get(key)

    def to_dict(self) -> Dict[str, Any]:
        """Convert memory state to dictionary."""
        return {
            "agent_id": self.agent_id,
            "statistics": self.get_statistics(),
            "recent_memories": [
                entry.to_dict() for entry in self.get_recent_memories(5)
            ],
        }
