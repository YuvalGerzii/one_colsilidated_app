"""
Model Context Protocol (MCP) inspired implementation.

Based on 2025 best practices for standardized context management.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, field
from loguru import logger


class ContextType(Enum):
    """Types of context information."""
    TASK = "task"
    CONVERSATION = "conversation"
    SYSTEM = "system"
    DOMAIN = "domain"
    TEMPORAL = "temporal"


class ContextScope(Enum):
    """Scope of context visibility."""
    PRIVATE = "private"  # Agent-specific
    SHARED = "shared"  # Shared with team
    GLOBAL = "global"  # System-wide


@dataclass
class ContextEntry:
    """A single context entry following MCP patterns."""
    id: str
    type: ContextType
    scope: ContextScope
    content: Any
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    importance: float = 0.5
    relevance_score: float = 1.0

    def is_expired(self) -> bool:
        """Check if context entry has expired."""
        if self.expires_at is None:
            return False
        return datetime.now() > self.expires_at

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "type": self.type.value,
            "scope": self.scope.value,
            "content": self.content,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat(),
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "importance": self.importance,
            "relevance_score": self.relevance_score,
        }


class ContextProtocol:
    """
    MCP-inspired context management protocol.

    Provides standardized mechanisms for:
    - Context storage and retrieval
    - Context sharing across agents
    - Relevance-based filtering
    - Automatic context cleanup
    """

    def __init__(self, max_contexts: int = 1000):
        """
        Initialize context protocol.

        Args:
            max_contexts: Maximum number of contexts to store
        """
        self.max_contexts = max_contexts

        # Context storage by scope
        self.private_contexts: Dict[str, List[ContextEntry]] = {}
        self.shared_contexts: List[ContextEntry] = []
        self.global_contexts: List[ContextEntry] = []

        # Context cache for fast retrieval
        self.context_cache: Dict[str, ContextEntry] = {}

        logger.info("ContextProtocol initialized")

    def store_context(
        self,
        agent_id: str,
        context_type: ContextType,
        content: Any,
        scope: ContextScope = ContextScope.PRIVATE,
        importance: float = 0.5,
        ttl_seconds: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Store context following MCP patterns.

        Args:
            agent_id: ID of the agent storing context
            context_type: Type of context
            content: Context content
            scope: Visibility scope
            importance: Importance score
            ttl_seconds: Time to live in seconds
            metadata: Additional metadata

        Returns:
            Context entry ID
        """
        import uuid

        entry_id = f"{agent_id}_{context_type.value}_{uuid.uuid4().hex[:8]}"

        expires_at = None
        if ttl_seconds:
            from datetime import timedelta
            expires_at = datetime.now() + timedelta(seconds=ttl_seconds)

        entry = ContextEntry(
            id=entry_id,
            type=context_type,
            scope=scope,
            content=content,
            metadata=metadata or {},
            importance=importance,
            expires_at=expires_at,
        )

        # Store by scope
        if scope == ContextScope.PRIVATE:
            if agent_id not in self.private_contexts:
                self.private_contexts[agent_id] = []
            self.private_contexts[agent_id].append(entry)

        elif scope == ContextScope.SHARED:
            self.shared_contexts.append(entry)

        else:  # GLOBAL
            self.global_contexts.append(entry)

        # Add to cache
        self.context_cache[entry_id] = entry

        # Cleanup if needed
        self._cleanup_expired()

        logger.debug(f"Stored context: {entry_id} (scope={scope.value})")
        return entry_id

    def retrieve_context(
        self,
        agent_id: str,
        context_type: Optional[ContextType] = None,
        scope: Optional[ContextScope] = None,
        min_importance: float = 0.0,
        limit: int = 10,
    ) -> List[ContextEntry]:
        """
        Retrieve context entries.

        Args:
            agent_id: ID of the requesting agent
            context_type: Filter by context type
            scope: Filter by scope
            min_importance: Minimum importance threshold
            limit: Maximum number of entries

        Returns:
            List of context entries
        """
        contexts = []

        # Collect contexts based on scope
        if scope is None or scope == ContextScope.PRIVATE:
            contexts.extend(self.private_contexts.get(agent_id, []))

        if scope is None or scope == ContextScope.SHARED:
            contexts.extend(self.shared_contexts)

        if scope is None or scope == ContextScope.GLOBAL:
            contexts.extend(self.global_contexts)

        # Filter
        filtered = []
        for entry in contexts:
            if entry.is_expired():
                continue

            if context_type and entry.type != context_type:
                continue

            if entry.importance < min_importance:
                continue

            filtered.append(entry)

        # Sort by relevance and recency
        filtered.sort(
            key=lambda e: (e.relevance_score, e.timestamp),
            reverse=True,
        )

        return filtered[:limit]

    def retrieve_relevant_context(
        self,
        agent_id: str,
        query: str,
        context_type: Optional[ContextType] = None,
        top_k: int = 5,
    ) -> List[ContextEntry]:
        """
        Retrieve context based on relevance to query.

        Uses simple keyword matching. In production, use embeddings.

        Args:
            agent_id: ID of the requesting agent
            query: Query string
            context_type: Filter by type
            top_k: Number of results

        Returns:
            List of relevant context entries
        """
        # Get all accessible contexts
        all_contexts = self.retrieve_context(
            agent_id, context_type=context_type, limit=1000
        )

        # Calculate relevance scores
        query_lower = query.lower()
        for entry in all_contexts:
            # Simple keyword-based scoring
            content_str = str(entry.content).lower()
            metadata_str = str(entry.metadata).lower()

            score = 0.0
            # Check for keyword matches
            for word in query_lower.split():
                if word in content_str:
                    score += 0.5
                if word in metadata_str:
                    score += 0.3

            # Boost recent entries
            age_hours = (datetime.now() - entry.timestamp).total_seconds() / 3600
            recency_boost = max(0, 1.0 - age_hours / 24.0)  # Decay over 24h
            score += recency_boost * 0.2

            # Importance boost
            score += entry.importance * 0.3

            entry.relevance_score = score

        # Sort by relevance
        all_contexts.sort(key=lambda e: e.relevance_score, reverse=True)

        return all_contexts[:top_k]

    def share_context(self, context_id: str, new_scope: ContextScope) -> bool:
        """
        Change the scope of a context entry.

        Args:
            context_id: ID of the context to share
            new_scope: New scope

        Returns:
            True if successful
        """
        if context_id not in self.context_cache:
            return False

        entry = self.context_cache[context_id]
        old_scope = entry.scope

        # Remove from old scope
        if old_scope == ContextScope.PRIVATE:
            for agent_contexts in self.private_contexts.values():
                if entry in agent_contexts:
                    agent_contexts.remove(entry)
                    break
        elif old_scope == ContextScope.SHARED:
            if entry in self.shared_contexts:
                self.shared_contexts.remove(entry)
        else:  # GLOBAL
            if entry in self.global_contexts:
                self.global_contexts.remove(entry)

        # Add to new scope
        entry.scope = new_scope
        if new_scope == ContextScope.SHARED:
            self.shared_contexts.append(entry)
        elif new_scope == ContextScope.GLOBAL:
            self.global_contexts.append(entry)

        logger.debug(f"Changed scope of {context_id}: {old_scope.value} -> {new_scope.value}")
        return True

    def update_context(
        self,
        context_id: str,
        content: Optional[Any] = None,
        importance: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        Update an existing context entry.

        Args:
            context_id: ID of the context
            content: New content
            importance: New importance
            metadata: Metadata to merge

        Returns:
            True if successful
        """
        if context_id not in self.context_cache:
            return False

        entry = self.context_cache[context_id]

        if content is not None:
            entry.content = content

        if importance is not None:
            entry.importance = importance

        if metadata is not None:
            entry.metadata.update(metadata)

        logger.debug(f"Updated context: {context_id}")
        return True

    def delete_context(self, context_id: str) -> bool:
        """
        Delete a context entry.

        Args:
            context_id: ID of the context

        Returns:
            True if successful
        """
        if context_id not in self.context_cache:
            return False

        entry = self.context_cache.pop(context_id)

        # Remove from storage
        if entry.scope == ContextScope.PRIVATE:
            for agent_contexts in self.private_contexts.values():
                if entry in agent_contexts:
                    agent_contexts.remove(entry)
                    break
        elif entry.scope == ContextScope.SHARED:
            if entry in self.shared_contexts:
                self.shared_contexts.remove(entry)
        else:  # GLOBAL
            if entry in self.global_contexts:
                self.global_contexts.remove(entry)

        logger.debug(f"Deleted context: {context_id}")
        return True

    def _cleanup_expired(self) -> int:
        """
        Clean up expired contexts.

        Returns:
            Number of contexts removed
        """
        removed = 0

        # Clean private contexts
        for agent_id in list(self.private_contexts.keys()):
            contexts = self.private_contexts[agent_id]
            before = len(contexts)
            contexts[:] = [c for c in contexts if not c.is_expired()]
            removed += before - len(contexts)

        # Clean shared contexts
        before = len(self.shared_contexts)
        self.shared_contexts[:] = [c for c in self.shared_contexts if not c.is_expired()]
        removed += before - len(self.shared_contexts)

        # Clean global contexts
        before = len(self.global_contexts)
        self.global_contexts[:] = [c for c in self.global_contexts if not c.is_expired()]
        removed += before - len(self.global_contexts)

        # Update cache
        self.context_cache = {
            cid: entry
            for cid, entry in self.context_cache.items()
            if not entry.is_expired()
        }

        if removed > 0:
            logger.debug(f"Cleaned up {removed} expired contexts")

        return removed

    def get_statistics(self) -> Dict[str, Any]:
        """Get context protocol statistics."""
        total_private = sum(len(contexts) for contexts in self.private_contexts.values())

        return {
            "total_contexts": len(self.context_cache),
            "private_contexts": total_private,
            "shared_contexts": len(self.shared_contexts),
            "global_contexts": len(self.global_contexts),
            "agents_with_context": len(self.private_contexts),
            "cache_size": len(self.context_cache),
        }
