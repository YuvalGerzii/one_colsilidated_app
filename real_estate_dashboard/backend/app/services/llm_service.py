"""
LLM Service - Local Language Model Integration with Ollama

Provides LLM capabilities with graceful degradation.
If Ollama is unavailable, returns None without breaking the app.
"""

import logging
import hashlib
import json
from typing import Optional, Dict, Any, List
from datetime import datetime
import httpx
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

from app.settings import settings
from app.services.cache_service import cache_service

logger = logging.getLogger(__name__)


class LLMServiceError(Exception):
    """Base exception for LLM service errors"""
    pass


class LLMUnavailableError(LLMServiceError):
    """Raised when LLM service is unavailable"""
    pass


class LLMService:
    """
    Service for interacting with local Ollama LLM.

    Features:
    - Graceful degradation (returns None on failure)
    - Response caching
    - Retry logic with exponential backoff
    - Request/response logging
    - Health monitoring
    """

    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL
        self.timeout = settings.LLM_TIMEOUT
        self.max_retries = settings.LLM_MAX_RETRIES
        self.cache_ttl = settings.LLM_CACHE_TTL
        self.temperature = settings.LLM_TEMPERATURE
        self.max_tokens = settings.LLM_MAX_TOKENS
        self.enabled = settings.ENABLE_LLM

        # Metrics tracking
        self.metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "cache_hits": 0,
            "total_tokens_generated": 0,
            "avg_response_time": 0.0
        }

        logger.info(
            f"LLM Service initialized - "
            f"Enabled: {self.enabled}, "
            f"Model: {self.model}, "
            f"Base URL: {self.base_url}"
        )

    async def health_check(self) -> Dict[str, Any]:
        """
        Check if Ollama service is healthy.

        Returns:
            Dictionary with health status
        """
        if not self.enabled:
            return {
                "status": "disabled",
                "available": False,
                "message": "LLM service is disabled in settings"
            }

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/api/health")

                if response.status_code == 200:
                    return {
                        "status": "healthy",
                        "available": True,
                        "model": self.model,
                        "metrics": self.metrics
                    }
                else:
                    return {
                        "status": "unhealthy",
                        "available": False,
                        "message": f"Unexpected status code: {response.status_code}"
                    }
        except Exception as e:
            logger.warning(f"LLM health check failed: {e}")
            return {
                "status": "unavailable",
                "available": False,
                "message": str(e)
            }

    def _generate_cache_key(self, prompt: str, **kwargs) -> str:
        """Generate cache key from prompt and parameters"""
        cache_data = {
            "prompt": prompt,
            "model": self.model,
            **kwargs
        }
        cache_str = json.dumps(cache_data, sort_keys=True)
        return f"llm_cache:{hashlib.md5(cache_str.encode()).hexdigest()}"

    @retry(
        stop=stop_after_attempt(2),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(httpx.RequestError),
        reraise=True
    )
    async def _make_ollama_request(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Make request to Ollama API with retry logic.

        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            temperature: Generation temperature (overrides default)
            max_tokens: Max tokens to generate (overrides default)

        Returns:
            Response dictionary from Ollama

        Raises:
            httpx.RequestError: On network/connection errors
            httpx.HTTPStatusError: On HTTP errors
        """
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature or self.temperature,
                "num_predict": max_tokens or self.max_tokens
            }
        }

        start_time = datetime.now()

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/api/chat",
                json=payload
            )
            response.raise_for_status()

        elapsed = (datetime.now() - start_time).total_seconds()

        result = response.json()

        # Update metrics
        self.metrics["avg_response_time"] = (
            (self.metrics["avg_response_time"] * self.metrics["successful_requests"] + elapsed)
            / (self.metrics["successful_requests"] + 1)
        )

        logger.info(f"LLM request completed in {elapsed:.2f}s")

        return result

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        use_cache: bool = True
    ) -> Optional[Dict[str, Any]]:
        """
        Generate text using LLM with graceful degradation.

        Args:
            prompt: User prompt
            system_prompt: Optional system prompt for context
            temperature: Generation temperature (0-1, lower = more focused)
            max_tokens: Maximum tokens to generate
            use_cache: Whether to use cached responses

        Returns:
            Dictionary with generated text and metadata, or None if LLM unavailable

        Example:
            >>> result = await llm_service.generate(
            ...     "Summarize this contract clause",
            ...     system_prompt="You are a legal expert"
            ... )
            >>> if result:
            ...     print(result["text"])
            ... else:
            ...     print("LLM unavailable, using fallback")
        """
        self.metrics["total_requests"] += 1

        if not self.enabled:
            logger.debug("LLM service is disabled")
            self.metrics["failed_requests"] += 1
            return None

        # Check cache
        if use_cache:
            cache_key = self._generate_cache_key(
                prompt,
                system_prompt=system_prompt,
                temperature=temperature,
                max_tokens=max_tokens
            )

            cached = await cache_service.get(cache_key)
            if cached:
                logger.info("LLM cache hit")
                self.metrics["cache_hits"] += 1
                return json.loads(cached)

        try:
            # Make request to Ollama
            response = await self._make_ollama_request(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=temperature,
                max_tokens=max_tokens
            )

            # Extract response
            text = response.get("message", {}).get("content", "")

            result = {
                "text": text,
                "model": self.model,
                "source": "local_llm",
                "timestamp": datetime.utcnow().isoformat(),
                "metadata": {
                    "prompt_tokens": response.get("prompt_eval_count", 0),
                    "completion_tokens": response.get("eval_count", 0),
                    "total_tokens": (
                        response.get("prompt_eval_count", 0) +
                        response.get("eval_count", 0)
                    )
                }
            }

            # Update metrics
            self.metrics["successful_requests"] += 1
            self.metrics["total_tokens_generated"] += result["metadata"]["total_tokens"]

            # Cache result
            if use_cache:
                await cache_service.set(
                    cache_key,
                    json.dumps(result),
                    ttl=self.cache_ttl
                )

            return result

        except httpx.TimeoutException:
            logger.warning(f"LLM request timeout after {self.timeout}s")
            self.metrics["failed_requests"] += 1
            return None

        except httpx.HTTPStatusError as e:
            logger.error(f"LLM HTTP error: {e.response.status_code} - {e.response.text}")
            self.metrics["failed_requests"] += 1
            return None

        except httpx.RequestError as e:
            logger.error(f"LLM request error: {e}")
            self.metrics["failed_requests"] += 1
            return None

        except Exception as e:
            logger.error(f"Unexpected LLM error: {e}", exc_info=True)
            self.metrics["failed_requests"] += 1
            return None

    async def generate_structured(
        self,
        prompt: str,
        output_format: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> Optional[Dict[str, Any]]:
        """
        Generate structured output (JSON) from LLM.

        Args:
            prompt: User prompt
            output_format: Description of expected JSON structure
            system_prompt: Optional system prompt
            **kwargs: Additional arguments for generate()

        Returns:
            Dictionary with parsed JSON or None
        """
        full_system_prompt = (
            f"{system_prompt}\n\n" if system_prompt else ""
        ) + f"You must respond with valid JSON in this format: {output_format}"

        result = await self.generate(
            prompt=prompt,
            system_prompt=full_system_prompt,
            **kwargs
        )

        if not result:
            return None

        # Try to parse JSON from response
        try:
            text = result["text"].strip()
            # Extract JSON if wrapped in markdown code blocks
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]

            parsed = json.loads(text)
            result["parsed"] = parsed
            return result

        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse LLM JSON response: {e}")
            return result  # Return unparsed result

    def get_metrics(self) -> Dict[str, Any]:
        """Get service metrics"""
        return {
            **self.metrics,
            "cache_hit_rate": (
                self.metrics["cache_hits"] / self.metrics["total_requests"]
                if self.metrics["total_requests"] > 0 else 0
            ),
            "success_rate": (
                self.metrics["successful_requests"] / self.metrics["total_requests"]
                if self.metrics["total_requests"] > 0 else 0
            )
        }


# Global instance
llm_service = LLMService()
