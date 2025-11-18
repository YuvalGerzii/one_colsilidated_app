"""
Embedding Service for RAG System

Handles text embedding generation using sentence transformers or Ollama.
Supports multiple embedding models with caching and batch processing.
"""

import os
import hashlib
import logging
from typing import List, Optional, Dict, Any
import numpy as np

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Service for generating text embeddings"""

    def __init__(self):
        self.model_name = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
        self.model = None
        self.embedding_dim = None
        self._cache: Dict[str, List[float]] = {}
        self._use_ollama = os.getenv("USE_OLLAMA_EMBEDDINGS", "false").lower() == "true"
        self._ollama_url = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")

    async def initialize(self):
        """Initialize the embedding model"""
        if self._use_ollama:
            await self._initialize_ollama()
        else:
            await self._initialize_sentence_transformer()

    async def _initialize_sentence_transformer(self):
        """Initialize sentence transformer model"""
        try:
            from sentence_transformers import SentenceTransformer

            logger.info(f"Loading embedding model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            self.embedding_dim = self.model.get_sentence_embedding_dimension()
            logger.info(f"Embedding model loaded. Dimension: {self.embedding_dim}")

        except ImportError:
            logger.warning("sentence-transformers not available, falling back to Ollama")
            self._use_ollama = True
            await self._initialize_ollama()
        except Exception as e:
            logger.error(f"Failed to load sentence transformer: {e}")
            raise

    async def _initialize_ollama(self):
        """Initialize Ollama for embeddings"""
        import httpx

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self._ollama_url}/api/tags")
                if response.status_code == 200:
                    self.embedding_dim = 4096  # Ollama default
                    logger.info("Ollama embedding service initialized")
                else:
                    raise Exception(f"Ollama not available: {response.status_code}")
        except Exception as e:
            logger.error(f"Failed to initialize Ollama: {e}")
            # Fall back to a simple implementation
            self.embedding_dim = 384
            logger.warning("Using fallback random embeddings for development")

    def _get_cache_key(self, text: str) -> str:
        """Generate cache key for text"""
        return hashlib.md5(text.encode()).hexdigest()

    async def embed_text(self, text: str, use_cache: bool = True) -> List[float]:
        """
        Generate embedding for a single text

        Args:
            text: Input text to embed
            use_cache: Whether to use cached embeddings

        Returns:
            List of floats representing the embedding
        """
        if not text or not text.strip():
            return [0.0] * (self.embedding_dim or 384)

        # Check cache
        if use_cache:
            cache_key = self._get_cache_key(text)
            if cache_key in self._cache:
                return self._cache[cache_key]

        # Initialize model if needed
        if self.model is None and not self._use_ollama:
            await self.initialize()

        # Generate embedding
        if self._use_ollama:
            embedding = await self._embed_with_ollama(text)
        elif self.model is not None:
            embedding = self._embed_with_transformer(text)
        else:
            # Fallback to deterministic pseudo-random embedding
            embedding = self._fallback_embedding(text)

        # Cache result
        if use_cache:
            self._cache[cache_key] = embedding

        return embedding

    async def embed_batch(self, texts: List[str], use_cache: bool = True) -> List[List[float]]:
        """
        Generate embeddings for multiple texts

        Args:
            texts: List of texts to embed
            use_cache: Whether to use cached embeddings

        Returns:
            List of embeddings
        """
        if not texts:
            return []

        # Check which texts need embedding
        results = [None] * len(texts)
        texts_to_embed = []
        indices_to_embed = []

        for i, text in enumerate(texts):
            if not text or not text.strip():
                results[i] = [0.0] * (self.embedding_dim or 384)
            elif use_cache:
                cache_key = self._get_cache_key(text)
                if cache_key in self._cache:
                    results[i] = self._cache[cache_key]
                else:
                    texts_to_embed.append(text)
                    indices_to_embed.append(i)
            else:
                texts_to_embed.append(text)
                indices_to_embed.append(i)

        # Generate embeddings for remaining texts
        if texts_to_embed:
            # Initialize if needed
            if self.model is None and not self._use_ollama:
                await self.initialize()

            if self._use_ollama:
                embeddings = await self._embed_batch_with_ollama(texts_to_embed)
            elif self.model is not None:
                embeddings = self._embed_batch_with_transformer(texts_to_embed)
            else:
                embeddings = [self._fallback_embedding(t) for t in texts_to_embed]

            # Store results and cache
            for i, embedding in enumerate(embeddings):
                idx = indices_to_embed[i]
                results[idx] = embedding
                if use_cache:
                    cache_key = self._get_cache_key(texts_to_embed[i])
                    self._cache[cache_key] = embedding

        return results

    def _embed_with_transformer(self, text: str) -> List[float]:
        """Generate embedding using sentence transformer"""
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()

    def _embed_batch_with_transformer(self, texts: List[str]) -> List[List[float]]:
        """Generate batch embeddings using sentence transformer"""
        embeddings = self.model.encode(texts, convert_to_numpy=True, batch_size=32)
        return [emb.tolist() for emb in embeddings]

    async def _embed_with_ollama(self, text: str) -> List[float]:
        """Generate embedding using Ollama"""
        import httpx

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self._ollama_url}/api/embeddings",
                    json={
                        "model": os.getenv("OLLAMA_MODEL", "gemma:2b"),
                        "prompt": text
                    }
                )
                if response.status_code == 200:
                    data = response.json()
                    return data.get("embedding", self._fallback_embedding(text))
                else:
                    logger.warning(f"Ollama embedding failed: {response.status_code}")
                    return self._fallback_embedding(text)
        except Exception as e:
            logger.error(f"Ollama embedding error: {e}")
            return self._fallback_embedding(text)

    async def _embed_batch_with_ollama(self, texts: List[str]) -> List[List[float]]:
        """Generate batch embeddings using Ollama"""
        # Ollama doesn't support batch embeddings natively, so we process sequentially
        embeddings = []
        for text in texts:
            embedding = await self._embed_with_ollama(text)
            embeddings.append(embedding)
        return embeddings

    def _fallback_embedding(self, text: str) -> List[float]:
        """Generate deterministic fallback embedding based on text hash"""
        # Create deterministic embedding from text hash
        hash_value = int(hashlib.sha256(text.encode()).hexdigest(), 16)
        np.random.seed(hash_value % (2**32))
        embedding = np.random.randn(self.embedding_dim or 384).tolist()
        # Normalize
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = [x / norm for x in embedding]
        return embedding

    def compute_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        Compute cosine similarity between two embeddings

        Args:
            embedding1: First embedding
            embedding2: Second embedding

        Returns:
            Cosine similarity score (0 to 1)
        """
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)

        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return float(dot_product / (norm1 * norm2))

    def get_embedding_dimension(self) -> int:
        """Get the dimension of embeddings"""
        return self.embedding_dim or 384

    def clear_cache(self):
        """Clear the embedding cache"""
        self._cache.clear()
        logger.info("Embedding cache cleared")

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return {
            "cached_embeddings": len(self._cache),
            "model_name": self.model_name,
            "embedding_dim": self.embedding_dim,
            "use_ollama": self._use_ollama
        }


# Global instance
_embedding_service: Optional[EmbeddingService] = None


async def get_embedding_service() -> EmbeddingService:
    """Get or create the global embedding service instance"""
    global _embedding_service

    if _embedding_service is None:
        _embedding_service = EmbeddingService()
        await _embedding_service.initialize()

    return _embedding_service
