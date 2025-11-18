"""
Vector Database Service for RAG System

Provides interface to Qdrant vector database for storing and retrieving embeddings.
Supports collection management, vector operations, and hybrid search.
"""

import os
import uuid
import logging
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)


class VectorDBService:
    """Service for vector database operations using Qdrant"""

    def __init__(self):
        self.host = os.getenv("QDRANT_HOST", "localhost")
        self.port = int(os.getenv("QDRANT_PORT", "6333"))
        self.client = None
        self.collections: Dict[str, bool] = {}

    async def initialize(self):
        """Initialize connection to Qdrant"""
        try:
            from qdrant_client import QdrantClient
            from qdrant_client.http.models import Distance, VectorParams

            self.client = QdrantClient(host=self.host, port=self.port)
            logger.info(f"Connected to Qdrant at {self.host}:{self.port}")

            # Verify connection
            collections = self.client.get_collections()
            logger.info(f"Found {len(collections.collections)} existing collections")

        except ImportError:
            logger.warning("qdrant-client not available, using in-memory fallback")
            self._use_fallback()
        except Exception as e:
            logger.error(f"Failed to connect to Qdrant: {e}")
            self._use_fallback()

    def _use_fallback(self):
        """Set up in-memory fallback for development"""
        self._fallback_storage: Dict[str, Dict[str, Any]] = {}
        self.client = None
        logger.info("Using in-memory vector storage fallback")

    async def create_collection(
        self,
        collection_name: str,
        vector_size: int,
        distance: str = "Cosine"
    ) -> bool:
        """
        Create a new vector collection

        Args:
            collection_name: Name of the collection
            vector_size: Dimension of vectors
            distance: Distance metric (Cosine, Euclid, Dot)

        Returns:
            True if created successfully
        """
        try:
            if self.client:
                from qdrant_client.http.models import Distance as QDistance, VectorParams

                distance_map = {
                    "Cosine": QDistance.COSINE,
                    "Euclid": QDistance.EUCLID,
                    "Dot": QDistance.DOT
                }

                # Check if collection exists
                collections = self.client.get_collections()
                existing = [c.name for c in collections.collections]

                if collection_name not in existing:
                    self.client.create_collection(
                        collection_name=collection_name,
                        vectors_config=VectorParams(
                            size=vector_size,
                            distance=distance_map.get(distance, QDistance.COSINE)
                        )
                    )
                    logger.info(f"Created collection: {collection_name}")
                else:
                    logger.info(f"Collection already exists: {collection_name}")

                self.collections[collection_name] = True
                return True
            else:
                # Fallback
                if collection_name not in self._fallback_storage:
                    self._fallback_storage[collection_name] = {
                        "vectors": {},
                        "vector_size": vector_size
                    }
                return True

        except Exception as e:
            logger.error(f"Failed to create collection: {e}")
            return False

    async def upsert_vectors(
        self,
        collection_name: str,
        vectors: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Insert or update vectors in collection

        Args:
            collection_name: Target collection
            vectors: List of dicts with 'id', 'vector', 'payload'

        Returns:
            List of vector IDs
        """
        if not vectors:
            return []

        try:
            if self.client:
                from qdrant_client.http.models import PointStruct

                points = []
                ids = []

                for v in vectors:
                    vector_id = v.get("id") or str(uuid.uuid4())
                    ids.append(vector_id)

                    points.append(PointStruct(
                        id=vector_id,
                        vector=v["vector"],
                        payload=v.get("payload", {})
                    ))

                self.client.upsert(
                    collection_name=collection_name,
                    points=points
                )

                logger.debug(f"Upserted {len(points)} vectors to {collection_name}")
                return ids
            else:
                # Fallback
                ids = []
                for v in vectors:
                    vector_id = v.get("id") or str(uuid.uuid4())
                    ids.append(vector_id)

                    if collection_name not in self._fallback_storage:
                        self._fallback_storage[collection_name] = {"vectors": {}}

                    self._fallback_storage[collection_name]["vectors"][vector_id] = {
                        "vector": v["vector"],
                        "payload": v.get("payload", {})
                    }
                return ids

        except Exception as e:
            logger.error(f"Failed to upsert vectors: {e}")
            return []

    async def search(
        self,
        collection_name: str,
        query_vector: List[float],
        top_k: int = 5,
        score_threshold: float = 0.0,
        filter_conditions: Optional[Dict] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar vectors

        Args:
            collection_name: Collection to search
            query_vector: Query embedding
            top_k: Number of results
            score_threshold: Minimum similarity score
            filter_conditions: Qdrant filter conditions

        Returns:
            List of results with id, score, and payload
        """
        try:
            if self.client:
                from qdrant_client.http.models import Filter, FieldCondition, MatchValue

                # Build filter if provided
                query_filter = None
                if filter_conditions:
                    conditions = []
                    for key, value in filter_conditions.items():
                        conditions.append(
                            FieldCondition(
                                key=key,
                                match=MatchValue(value=value)
                            )
                        )
                    query_filter = Filter(must=conditions)

                results = self.client.search(
                    collection_name=collection_name,
                    query_vector=query_vector,
                    limit=top_k,
                    score_threshold=score_threshold,
                    query_filter=query_filter
                )

                return [
                    {
                        "id": str(r.id),
                        "score": r.score,
                        "payload": r.payload
                    }
                    for r in results
                ]
            else:
                # Fallback with brute-force search
                return self._fallback_search(
                    collection_name, query_vector, top_k, score_threshold
                )

        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

    def _fallback_search(
        self,
        collection_name: str,
        query_vector: List[float],
        top_k: int,
        score_threshold: float
    ) -> List[Dict[str, Any]]:
        """Fallback brute-force search"""
        import numpy as np

        if collection_name not in self._fallback_storage:
            return []

        results = []
        query = np.array(query_vector)

        for vector_id, data in self._fallback_storage[collection_name]["vectors"].items():
            vec = np.array(data["vector"])
            # Cosine similarity
            score = float(np.dot(query, vec) / (np.linalg.norm(query) * np.linalg.norm(vec) + 1e-9))

            if score >= score_threshold:
                results.append({
                    "id": vector_id,
                    "score": score,
                    "payload": data["payload"]
                })

        # Sort by score and return top_k
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    async def delete_vectors(
        self,
        collection_name: str,
        vector_ids: List[str]
    ) -> bool:
        """
        Delete vectors by IDs

        Args:
            collection_name: Target collection
            vector_ids: List of vector IDs to delete

        Returns:
            True if successful
        """
        try:
            if self.client:
                self.client.delete(
                    collection_name=collection_name,
                    points_selector=vector_ids
                )
                logger.debug(f"Deleted {len(vector_ids)} vectors from {collection_name}")
                return True
            else:
                # Fallback
                if collection_name in self._fallback_storage:
                    for vid in vector_ids:
                        self._fallback_storage[collection_name]["vectors"].pop(vid, None)
                return True

        except Exception as e:
            logger.error(f"Failed to delete vectors: {e}")
            return False

    async def get_collection_info(self, collection_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a collection"""
        try:
            if self.client:
                info = self.client.get_collection(collection_name)
                return {
                    "name": collection_name,
                    "vectors_count": info.vectors_count,
                    "points_count": info.points_count,
                    "status": info.status.value
                }
            else:
                if collection_name in self._fallback_storage:
                    return {
                        "name": collection_name,
                        "vectors_count": len(self._fallback_storage[collection_name]["vectors"]),
                        "status": "green"
                    }
                return None

        except Exception as e:
            logger.error(f"Failed to get collection info: {e}")
            return None

    async def delete_collection(self, collection_name: str) -> bool:
        """Delete a collection"""
        try:
            if self.client:
                self.client.delete_collection(collection_name)
                self.collections.pop(collection_name, None)
                logger.info(f"Deleted collection: {collection_name}")
                return True
            else:
                self._fallback_storage.pop(collection_name, None)
                return True

        except Exception as e:
            logger.error(f"Failed to delete collection: {e}")
            return False

    async def hybrid_search(
        self,
        collection_name: str,
        query_vector: List[float],
        keyword_query: Optional[str] = None,
        top_k: int = 5,
        alpha: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Perform hybrid search combining vector and keyword search

        Args:
            collection_name: Collection to search
            query_vector: Query embedding
            keyword_query: Optional keyword query
            top_k: Number of results
            alpha: Weight for vector search (0=keyword only, 1=vector only)

        Returns:
            Combined search results
        """
        # Get vector search results
        vector_results = await self.search(
            collection_name=collection_name,
            query_vector=query_vector,
            top_k=top_k * 2  # Get more for reranking
        )

        if not keyword_query or alpha >= 1.0:
            return vector_results[:top_k]

        # Combine with keyword matching
        combined_results = []
        for result in vector_results:
            payload = result.get("payload", {})
            content = payload.get("content", "")

            # Simple keyword scoring
            keyword_score = 0.0
            if keyword_query.lower() in content.lower():
                keyword_score = 1.0

            # Combine scores
            final_score = alpha * result["score"] + (1 - alpha) * keyword_score
            result["score"] = final_score
            combined_results.append(result)

        # Re-sort and return
        combined_results.sort(key=lambda x: x["score"], reverse=True)
        return combined_results[:top_k]


# Global instance
_vector_db_service: Optional[VectorDBService] = None


async def get_vector_db_service() -> VectorDBService:
    """Get or create the global vector DB service instance"""
    global _vector_db_service

    if _vector_db_service is None:
        _vector_db_service = VectorDBService()
        await _vector_db_service.initialize()

    return _vector_db_service
