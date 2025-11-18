"""
Local LLM Client using Ollama
100% FREE - No API keys required!

Enhanced with:
- Response caching for performance
- Streaming support
- Batch processing
- Advanced error handling
- Performance metrics
"""

import hashlib
import time
from typing import List, Dict, Any, Optional, AsyncGenerator
from datetime import datetime, timedelta

import httpx
from loguru import logger

from src.core.config import get_settings

settings = get_settings()


class LLMCache:
    """Simple in-memory cache for LLM responses."""

    def __init__(self, ttl_seconds: int = 3600):
        """Initialize cache with TTL."""
        self.cache: Dict[str, tuple[Any, datetime]] = {}
        self.ttl = timedelta(seconds=ttl_seconds)
        self.hits = 0
        self.misses = 0

    def _make_key(self, prompt: str, **kwargs) -> str:
        """Create cache key from prompt and parameters."""
        key_data = f"{prompt}:{sorted(kwargs.items())}"
        return hashlib.md5(key_data.encode()).hexdigest()

    def get(self, prompt: str, **kwargs) -> Optional[Any]:
        """Get cached response if available and fresh."""
        key = self._make_key(prompt, **kwargs)
        if key in self.cache:
            value, timestamp = self.cache[key]
            if datetime.now() - timestamp < self.ttl:
                self.hits += 1
                logger.debug(f"Cache HIT - Saved LLM call!")
                return value
            else:
                # Expired
                del self.cache[key]

        self.misses += 1
        return None

    def set(self, prompt: str, response: Any, **kwargs) -> None:
        """Cache a response."""
        key = self._make_key(prompt, **kwargs)
        self.cache[key] = (response, datetime.now())

    def clear(self) -> None:
        """Clear all cached responses."""
        self.cache.clear()
        logger.info("LLM cache cleared")

    def stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": f"{hit_rate:.1f}%",
            "size": len(self.cache),
        }


class LLMMetrics:
    """Track LLM usage metrics."""

    def __init__(self):
        """Initialize metrics."""
        self.total_requests = 0
        self.total_tokens = 0
        self.total_time = 0.0
        self.errors = 0
        self.model_usage: Dict[str, int] = {}

    def record_request(
        self, model: str, tokens: int, duration: float, success: bool = True
    ) -> None:
        """Record a request."""
        self.total_requests += 1
        self.total_tokens += tokens
        self.total_time += duration

        if not success:
            self.errors += 1

        self.model_usage[model] = self.model_usage.get(model, 0) + 1

    def get_stats(self) -> Dict[str, Any]:
        """Get usage statistics."""
        avg_time = (
            self.total_time / self.total_requests if self.total_requests > 0 else 0
        )
        error_rate = (
            self.errors / self.total_requests * 100 if self.total_requests > 0 else 0
        )

        return {
            "total_requests": self.total_requests,
            "total_tokens": self.total_tokens,
            "avg_response_time": f"{avg_time:.2f}s",
            "error_rate": f"{error_rate:.1f}%",
            "model_usage": self.model_usage,
            "cost_saved": f"${self.total_tokens * 0.00003:.2f}",  # vs GPT-4
        }


class LocalLLMClient:
    """
    Enhanced client for local LLM inference using Ollama.
    Completely free, no API keys needed!

    Features:
    - Response caching for performance
    - Streaming support
    - Batch processing
    - Advanced error handling
    - Usage metrics
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        enable_cache: bool = True,
    ):
        """
        Initialize local LLM client.

        Args:
            base_url: Ollama server URL (default: from settings)
            model: Model name (default: from settings)
            enable_cache: Enable response caching (default: True)
        """
        self.base_url = base_url or settings.ollama_url
        self.model = model or settings.ollama_model
        self.timeout = httpx.Timeout(settings.ai_timeout, connect=10.0)

        self.cache = LLMCache() if enable_cache else None
        self.metrics = LLMMetrics()

        logger.info(
            f"Initialized Enhanced Local LLM Client - Model: {self.model}, "
            f"Caching: {enable_cache}, URL: {self.base_url}"
        )

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        stream: bool = False,
        use_cache: bool = True,
    ) -> str:
        """
        Generate chat completion using local LLM.

        Args:
            messages: Chat messages in OpenAI format
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            stream: Whether to stream response
            use_cache: Use cached response if available

        Returns:
            str: Generated response
        """
        prompt = self._messages_to_prompt(messages)

        # Check cache
        if use_cache and self.cache:
            cached = self.cache.get(prompt, temp=temperature, max=max_tokens)
            if cached:
                return cached

        start_time = time.time()
        success = True

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": temperature,
                            "num_predict": max_tokens,
                        },
                    },
                )
                response.raise_for_status()
                result = response.json()
                generated_text = result.get("response", "")

                # Record metrics
                tokens = len(generated_text.split())  # Rough estimate
                duration = time.time() - start_time
                self.metrics.record_request(self.model, tokens, duration, True)

                # Cache the result
                if use_cache and self.cache:
                    self.cache.set(prompt, generated_text, temp=temperature, max=max_tokens)

                return generated_text

            except httpx.HTTPError as e:
                success = False
                duration = time.time() - start_time
                self.metrics.record_request(self.model, 0, duration, False)

                logger.error(f"Local LLM request failed: {e}")
                # Fallback to simple response
                return self._fallback_response(messages)

    async def chat_completion_stream(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> AsyncGenerator[str, None]:
        """
        Stream chat completion using local LLM.

        Args:
            messages: Chat messages
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Yields:
            str: Generated text chunks
        """
        prompt = self._messages_to_prompt(messages)

        async with httpx.AsyncClient(timeout=httpx.Timeout(600.0)) as client:
            try:
                async with client.stream(
                    "POST",
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": True,
                        "options": {
                            "temperature": temperature,
                            "num_predict": max_tokens,
                        },
                    },
                ) as response:
                    async for line in response.aiter_lines():
                        if line:
                            try:
                                import json

                                data = json.loads(line)
                                if "response" in data:
                                    yield data["response"]
                            except json.JSONDecodeError:
                                continue

            except httpx.HTTPError as e:
                logger.error(f"Streaming failed: {e}")
                yield "Error: Streaming unavailable"

    async def batch_completion(
        self,
        prompts: List[str],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        max_concurrent: int = 5,
    ) -> List[str]:
        """
        Process multiple prompts in parallel batches.

        Args:
            prompts: List of prompts to process
            temperature: Sampling temperature
            max_tokens: Maximum tokens per response
            max_concurrent: Maximum concurrent requests

        Returns:
            List[str]: Generated responses
        """
        import asyncio

        results = []

        # Process in batches
        for i in range(0, len(prompts), max_concurrent):
            batch = prompts[i : i + max_concurrent]

            tasks = [
                self.chat_completion(
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                for prompt in batch
            ]

            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            results.extend(batch_results)

            logger.info(
                f"Processed batch {i // max_concurrent + 1} "
                f"({len(batch)} prompts)"
            )

        return results

    def _messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """Convert OpenAI-style messages to a single prompt."""
        prompt_parts = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")

            if role == "system":
                prompt_parts.append(f"System: {content}")
            elif role == "user":
                prompt_parts.append(f"User: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")

        prompt_parts.append("Assistant:")
        return "\n\n".join(prompt_parts)

    def _fallback_response(self, messages: List[Dict[str, str]]) -> str:
        """Simple fallback when LLM is unavailable."""
        logger.warning("Using fallback response - LLM unavailable")
        return "# Local LLM is currently unavailable. Using fallback response."

    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embeddings using local model.

        Args:
            text: Text to embed

        Returns:
            List[float]: Embedding vector
        """
        # Check cache
        if self.cache:
            cached = self.cache.get(f"embed:{text}")
            if cached:
                return cached

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/api/embeddings",
                    json={
                        "model": settings.ollama_embedding_model,
                        "prompt": text,
                    },
                )
                response.raise_for_status()
                result = response.json()
                embedding = result.get("embedding", [0.0] * 768)

                # Cache the embedding
                if self.cache:
                    self.cache.set(f"embed:{text}", embedding)

                return embedding

            except httpx.HTTPError as e:
                logger.error(f"Local embedding generation failed: {e}")
                # Return zero vector as fallback
                return [0.0] * 768

    async def batch_embeddings(
        self, texts: List[str], max_concurrent: int = 10
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in parallel.

        Args:
            texts: List of texts to embed
            max_concurrent: Maximum concurrent requests

        Returns:
            List of embedding vectors
        """
        import asyncio

        results = []

        for i in range(0, len(texts), max_concurrent):
            batch = texts[i : i + max_concurrent]
            tasks = [self.generate_embedding(text) for text in batch]
            batch_results = await asyncio.gather(*tasks)
            results.extend(batch_results)

        return results

    async def list_models(self) -> List[str]:
        """
        List available local models.

        Returns:
            List[str]: Available model names
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(f"{self.base_url}/api/tags")
                response.raise_for_status()
                result = response.json()
                models = [m["name"] for m in result.get("models", [])]
                return models

            except httpx.HTTPError as e:
                logger.error(f"Failed to list models: {e}")
                return []

    async def pull_model(self, model_name: str) -> bool:
        """
        Download a model from Ollama library.

        Args:
            model_name: Name of model to download

        Returns:
            bool: Success status
        """
        logger.info(f"Pulling model: {model_name}")

        async with httpx.AsyncClient(timeout=httpx.Timeout(3600.0)) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/api/pull",
                    json={"name": model_name, "stream": False},
                )
                response.raise_for_status()
                logger.info(f"Successfully pulled model: {model_name}")
                return True

            except httpx.HTTPError as e:
                logger.error(f"Failed to pull model {model_name}: {e}")
                return False

    async def delete_model(self, model_name: str) -> bool:
        """
        Delete a local model to free space.

        Args:
            model_name: Name of model to delete

        Returns:
            bool: Success status
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.delete(
                    f"{self.base_url}/api/delete",
                    json={"name": model_name},
                )
                response.raise_for_status()
                logger.info(f"Deleted model: {model_name}")
                return True

            except httpx.HTTPError as e:
                logger.error(f"Failed to delete model {model_name}: {e}")
                return False

    async def is_available(self) -> bool:
        """
        Check if Ollama server is available.

        Returns:
            bool: True if available
        """
        async with httpx.AsyncClient(timeout=httpx.Timeout(5.0)) as client:
            try:
                response = await client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
            except Exception:
                return False

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return self.cache.stats() if self.cache else {"enabled": False}

    def get_metrics(self) -> Dict[str, Any]:
        """Get usage metrics."""
        return self.metrics.get_stats()

    def clear_cache(self) -> None:
        """Clear response cache."""
        if self.cache:
            self.cache.clear()


# Singleton instance
_llm_client: Optional[LocalLLMClient] = None


def get_local_llm() -> LocalLLMClient:
    """Get singleton instance of local LLM client."""
    global _llm_client
    if _llm_client is None:
        _llm_client = LocalLLMClient()
    return _llm_client

