"""
Semantic memory with embeddings for context-aware retrieval.

Implements best practices from 2025 research:
- Vector-based semantic search
- Context-aware retrieval
- Embedding-based similarity matching
"""

import numpy as np
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime
from collections import defaultdict
from loguru import logger


class SemanticMemory:
    """
    Semantic memory using embeddings for intelligent retrieval.

    Features:
    - Vector-based storage and retrieval
    - Semantic similarity search
    - Context-aware ranking
    - Automatic relevance scoring
    """

    def __init__(
        self,
        agent_id: str,
        embedding_dim: int = 384,  # Standard embedding dimension
        max_memories: int = 10000,
    ):
        """
        Initialize semantic memory.

        Args:
            agent_id: ID of the agent
            embedding_dim: Dimension of embedding vectors
            max_memories: Maximum number of memories to store
        """
        self.agent_id = agent_id
        self.embedding_dim = embedding_dim
        self.max_memories = max_memories

        # Memory storage
        self.memories: List[Dict[str, Any]] = []
        self.embeddings: List[np.ndarray] = []

        # Index for fast lookup
        self.memory_index: Dict[str, int] = {}

        # Statistics
        self.stats = {
            "total_stored": 0,
            "total_retrieved": 0,
            "cache_hits": 0,
        }

        logger.info(f"SemanticMemory initialized for {agent_id}")

    def _generate_embedding(self, text: str) -> np.ndarray:
        """
        Generate embedding for text.

        For production, use models like:
        - sentence-transformers/all-MiniLM-L6-v2
        - NVIDIA NV-Embed-v2
        - Jina Embeddings v3

        Args:
            text: Text to embed

        Returns:
            Embedding vector
        """
        # Simple hash-based embedding for demo
        # In production, replace with actual embedding model
        np.random.seed(hash(text) % (2**32))
        embedding = np.random.randn(self.embedding_dim)
        # Normalize
        embedding = embedding / (np.linalg.norm(embedding) + 1e-8)
        return embedding

    def store(
        self,
        key: str,
        content: Any,
        context: Optional[Dict[str, Any]] = None,
        importance: float = 0.5,
    ) -> None:
        """
        Store a memory with semantic embedding.

        Args:
            key: Memory identifier
            content: Memory content
            context: Additional context
            importance: Importance score (0.0 to 1.0)
        """
        # Generate embedding from content
        text = f"{key} {str(content)}"
        if context:
            text += f" {str(context)}"

        embedding = self._generate_embedding(text)

        memory = {
            "key": key,
            "content": content,
            "context": context or {},
            "importance": importance,
            "timestamp": datetime.now(),
            "access_count": 0,
        }

        # Check if key exists
        if key in self.memory_index:
            idx = self.memory_index[key]
            self.memories[idx] = memory
            self.embeddings[idx] = embedding
        else:
            # Add new memory
            if len(self.memories) >= self.max_memories:
                # Remove least important memory
                self._evict_memory()

            self.memories.append(memory)
            self.embeddings.append(embedding)
            self.memory_index[key] = len(self.memories) - 1

        self.stats["total_stored"] += 1
        logger.debug(f"Stored semantic memory: {key}")

    def retrieve_by_similarity(
        self,
        query: str,
        top_k: int = 5,
        min_similarity: float = 0.3,
    ) -> List[Tuple[str, Any, float]]:
        """
        Retrieve memories by semantic similarity.

        Args:
            query: Query text
            top_k: Number of results to return
            min_similarity: Minimum similarity threshold

        Returns:
            List of (key, content, similarity_score) tuples
        """
        if not self.memories:
            return []

        # Generate query embedding
        query_embedding = self._generate_embedding(query)

        # Calculate similarities
        similarities = []
        for idx, embedding in enumerate(self.embeddings):
            similarity = np.dot(query_embedding, embedding)
            if similarity >= min_similarity:
                similarities.append((idx, similarity))

        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)

        # Get top-k results
        results = []
        for idx, similarity in similarities[:top_k]:
            memory = self.memories[idx]
            memory["access_count"] += 1
            results.append((memory["key"], memory["content"], float(similarity)))

        self.stats["total_retrieved"] += len(results)
        logger.debug(f"Retrieved {len(results)} memories for query: {query[:50]}...")

        return results

    def retrieve_contextual(
        self,
        query: str,
        context: Dict[str, Any],
        top_k: int = 5,
    ) -> List[Tuple[str, Any, float]]:
        """
        Retrieve memories with context awareness.

        Combines semantic similarity with context matching.

        Args:
            query: Query text
            context: Current context
            top_k: Number of results

        Returns:
            List of (key, content, relevance_score) tuples
        """
        # Get semantic matches
        semantic_matches = self.retrieve_by_similarity(query, top_k * 2, 0.2)

        if not semantic_matches:
            return []

        # Re-rank based on context
        scored_matches = []
        for key, content, similarity in semantic_matches:
            idx = self.memory_index[key]
            memory = self.memories[idx]

            # Calculate context overlap
            context_score = self._calculate_context_overlap(
                memory["context"], context
            )

            # Combine scores (60% semantic, 40% context)
            relevance = 0.6 * similarity + 0.4 * context_score

            # Boost by importance and access frequency
            relevance *= (1.0 + memory["importance"] * 0.2)
            relevance *= (1.0 + min(memory["access_count"] / 10.0, 0.5))

            scored_matches.append((key, content, float(relevance)))

        # Sort by relevance
        scored_matches.sort(key=lambda x: x[2], reverse=True)

        logger.debug(f"Context-aware retrieval: {len(scored_matches[:top_k])} results")

        return scored_matches[:top_k]

    def _calculate_context_overlap(
        self, mem_context: Dict[str, Any], query_context: Dict[str, Any]
    ) -> float:
        """Calculate overlap between contexts."""
        if not mem_context or not query_context:
            return 0.0

        common_keys = set(mem_context.keys()) & set(query_context.keys())
        if not common_keys:
            return 0.0

        matches = sum(
            1 for key in common_keys if mem_context[key] == query_context[key]
        )

        return matches / len(query_context)

    def _evict_memory(self) -> None:
        """Evict least important memory."""
        if not self.memories:
            return

        # Calculate eviction scores (low importance + low access)
        scores = []
        for idx, memory in enumerate(self.memories):
            score = memory["importance"] + memory["access_count"] / 100.0
            scores.append((idx, score))

        # Remove memory with lowest score
        scores.sort(key=lambda x: x[1])
        evict_idx = scores[0][0]

        evicted_key = self.memories[evict_idx]["key"]
        del self.memories[evict_idx]
        del self.embeddings[evict_idx]

        # Rebuild index
        self.memory_index = {
            mem["key"]: idx for idx, mem in enumerate(self.memories)
        }

        logger.debug(f"Evicted memory: {evicted_key}")

    def get_recent_memories(
        self, limit: int = 10, min_importance: float = 0.0
    ) -> List[Dict[str, Any]]:
        """
        Get recent memories.

        Args:
            limit: Maximum number of memories
            min_importance: Minimum importance threshold

        Returns:
            List of memory dictionaries
        """
        filtered = [
            mem for mem in self.memories if mem["importance"] >= min_importance
        ]

        filtered.sort(key=lambda x: x["timestamp"], reverse=True)

        return filtered[:limit]

    def consolidate_memories(self, similarity_threshold: float = 0.9) -> int:
        """
        Consolidate similar memories.

        Args:
            similarity_threshold: Threshold for merging

        Returns:
            Number of memories consolidated
        """
        if len(self.memories) < 2:
            return 0

        consolidated = 0
        to_remove = set()

        for i in range(len(self.embeddings)):
            if i in to_remove:
                continue

            for j in range(i + 1, len(self.embeddings)):
                if j in to_remove:
                    continue

                similarity = np.dot(self.embeddings[i], self.embeddings[j])

                if similarity >= similarity_threshold:
                    # Merge j into i
                    mem_i = self.memories[i]
                    mem_j = self.memories[j]

                    # Keep more important one's content
                    if mem_j["importance"] > mem_i["importance"]:
                        mem_i["content"] = mem_j["content"]

                    # Merge contexts
                    mem_i["context"].update(mem_j["context"])

                    # Update importance (max)
                    mem_i["importance"] = max(
                        mem_i["importance"], mem_j["importance"]
                    )

                    # Update access count (sum)
                    mem_i["access_count"] += mem_j["access_count"]

                    to_remove.add(j)
                    consolidated += 1

        # Remove consolidated memories
        if to_remove:
            self.memories = [
                mem for idx, mem in enumerate(self.memories) if idx not in to_remove
            ]
            self.embeddings = [
                emb for idx, emb in enumerate(self.embeddings) if idx not in to_remove
            ]

            # Rebuild index
            self.memory_index = {
                mem["key"]: idx for idx, mem in enumerate(self.memories)
            }

        if consolidated > 0:
            logger.info(f"Consolidated {consolidated} similar memories")

        return consolidated

    def get_statistics(self) -> Dict[str, Any]:
        """Get semantic memory statistics."""
        return {
            **self.stats,
            "current_memories": len(self.memories),
            "capacity": self.max_memories,
            "utilization": len(self.memories) / self.max_memories,
        }

    def clear(self) -> None:
        """Clear all memories."""
        self.memories.clear()
        self.embeddings.clear()
        self.memory_index.clear()
        logger.info("Cleared semantic memory")
