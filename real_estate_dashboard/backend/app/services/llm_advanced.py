"""
Advanced LLM Features - Conversation Management, Rate Limiting, Streaming

Extends the base LLM service with advanced capabilities for production use.
"""

import logging
import asyncio
from typing import Optional, Dict, Any, List, AsyncGenerator
from datetime import datetime, timedelta
from collections import defaultdict, deque
import uuid

from app.services.llm_service import llm_service
from app.services.cache_service import cache_service

logger = logging.getLogger(__name__)


class ConversationManager:
    """
    Manages multi-turn conversations with context preservation.

    Features:
    - Conversation history tracking
    - Context window management
    - Automatic cleanup of old conversations
    """

    def __init__(self, max_history: int = 10, ttl_minutes: int = 30):
        self.max_history = max_history
        self.ttl_minutes = ttl_minutes
        self.conversations: Dict[str, Dict[str, Any]] = {}
        self._cleanup_task = None

    def create_conversation(self, user_id: Optional[str] = None) -> str:
        """
        Create a new conversation session.

        Args:
            user_id: Optional user identifier

        Returns:
            Conversation ID
        """
        conversation_id = str(uuid.uuid4())

        self.conversations[conversation_id] = {
            "id": conversation_id,
            "user_id": user_id,
            "created_at": datetime.utcnow(),
            "last_activity": datetime.utcnow(),
            "messages": [],
            "metadata": {}
        }

        logger.info(f"Created conversation {conversation_id}")
        return conversation_id

    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        metadata: Optional[Dict] = None
    ) -> bool:
        """
        Add a message to the conversation history.

        Args:
            conversation_id: Conversation identifier
            role: Message role (user, assistant, system)
            content: Message content
            metadata: Optional metadata

        Returns:
            Success status
        """
        if conversation_id not in self.conversations:
            logger.warning(f"Conversation {conversation_id} not found")
            return False

        conversation = self.conversations[conversation_id]

        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": metadata or {}
        }

        conversation["messages"].append(message)
        conversation["last_activity"] = datetime.utcnow()

        # Trim history if too long
        if len(conversation["messages"]) > self.max_history:
            conversation["messages"] = conversation["messages"][-self.max_history:]

        return True

    def get_conversation(self, conversation_id: str) -> Optional[Dict]:
        """Get full conversation history"""
        return self.conversations.get(conversation_id)

    def get_messages(
        self,
        conversation_id: str,
        limit: Optional[int] = None
    ) -> List[Dict]:
        """
        Get conversation messages.

        Args:
            conversation_id: Conversation identifier
            limit: Optional limit on number of messages

        Returns:
            List of messages
        """
        conversation = self.conversations.get(conversation_id)
        if not conversation:
            return []

        messages = conversation["messages"]
        if limit:
            return messages[-limit:]
        return messages

    def delete_conversation(self, conversation_id: str) -> bool:
        """Delete a conversation"""
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            logger.info(f"Deleted conversation {conversation_id}")
            return True
        return False

    def cleanup_old_conversations(self):
        """Remove conversations older than TTL"""
        cutoff = datetime.utcnow() - timedelta(minutes=self.ttl_minutes)
        to_delete = []

        for conv_id, conv in self.conversations.items():
            if conv["last_activity"] < cutoff:
                to_delete.append(conv_id)

        for conv_id in to_delete:
            self.delete_conversation(conv_id)

        if to_delete:
            logger.info(f"Cleaned up {len(to_delete)} old conversations")

    async def generate_with_context(
        self,
        conversation_id: str,
        user_message: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> Optional[Dict[str, Any]]:
        """
        Generate response with conversation context.

        Args:
            conversation_id: Conversation identifier
            user_message: User's message
            system_prompt: Optional system prompt
            **kwargs: Additional parameters for generate()

        Returns:
            LLM response or None
        """
        conversation = self.conversations.get(conversation_id)
        if not conversation:
            logger.warning(f"Conversation {conversation_id} not found")
            return None

        # Build context from conversation history
        messages = conversation["messages"]
        context = "\n".join([
            f"{msg['role']}: {msg['content']}"
            for msg in messages[-5:]  # Last 5 messages
        ])

        # Combine context with current message
        full_prompt = f"""Previous conversation:
{context}

User: {user_message}

Please respond considering the conversation history."""

        # Generate response
        result = await llm_service.generate(
            prompt=full_prompt,
            system_prompt=system_prompt,
            **kwargs
        )

        if result:
            # Add messages to history
            self.add_message(conversation_id, "user", user_message)
            self.add_message(conversation_id, "assistant", result["text"])

        return result


class RateLimiter:
    """
    Rate limiter for LLM requests to prevent abuse and manage resources.

    Features:
    - Per-user rate limiting
    - Global rate limiting
    - Request queue management
    """

    def __init__(
        self,
        requests_per_minute: int = 20,
        requests_per_hour: int = 100,
        global_requests_per_minute: int = 50
    ):
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        self.global_requests_per_minute = global_requests_per_minute

        # Per-user tracking
        self.user_requests: Dict[str, deque] = defaultdict(deque)

        # Global tracking
        self.global_requests: deque = deque()

    def _cleanup_old_requests(self, request_queue: deque, window_seconds: int):
        """Remove requests outside the time window"""
        cutoff = datetime.utcnow() - timedelta(seconds=window_seconds)

        while request_queue and request_queue[0] < cutoff:
            request_queue.popleft()

    def check_rate_limit(self, user_id: str) -> tuple[bool, Optional[str]]:
        """
        Check if user has exceeded rate limits.

        Args:
            user_id: User identifier

        Returns:
            (allowed, reason) tuple
        """
        now = datetime.utcnow()

        # Check global rate limit
        self._cleanup_old_requests(self.global_requests, 60)
        if len(self.global_requests) >= self.global_requests_per_minute:
            return False, "Global rate limit exceeded. Please try again later."

        # Check per-user rate limits
        user_queue = self.user_requests[user_id]

        # Check per-minute limit
        self._cleanup_old_requests(user_queue, 60)
        if len(user_queue) >= self.requests_per_minute:
            return False, f"Rate limit exceeded: {self.requests_per_minute} requests per minute"

        # Check per-hour limit
        hourly_requests = sum(
            1 for req_time in user_queue
            if req_time > now - timedelta(hours=1)
        )
        if hourly_requests >= self.requests_per_hour:
            return False, f"Rate limit exceeded: {self.requests_per_hour} requests per hour"

        # All checks passed
        return True, None

    def record_request(self, user_id: str):
        """Record a request for rate limiting"""
        now = datetime.utcnow()
        self.user_requests[user_id].append(now)
        self.global_requests.append(now)

    def get_usage_stats(self, user_id: str) -> Dict[str, Any]:
        """Get usage statistics for a user"""
        now = datetime.utcnow()
        user_queue = self.user_requests[user_id]

        # Count requests in different windows
        last_minute = sum(
            1 for req_time in user_queue
            if req_time > now - timedelta(minutes=1)
        )
        last_hour = sum(
            1 for req_time in user_queue
            if req_time > now - timedelta(hours=1)
        )

        return {
            "user_id": user_id,
            "requests_last_minute": last_minute,
            "requests_last_hour": last_hour,
            "limit_per_minute": self.requests_per_minute,
            "limit_per_hour": self.requests_per_hour,
            "remaining_minute": max(0, self.requests_per_minute - last_minute),
            "remaining_hour": max(0, self.requests_per_hour - last_hour)
        }


class RequestQueue:
    """
    Queue manager for handling concurrent LLM requests efficiently.

    Features:
    - Priority queue
    - Concurrent request limiting
    - Request timeout handling
    """

    def __init__(self, max_concurrent: int = 3):
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.active_requests = 0
        self.queued_requests = 0

    async def enqueue(
        self,
        func,
        *args,
        priority: int = 5,
        timeout: int = 60,
        **kwargs
    ) -> Any:
        """
        Enqueue a request with priority and timeout.

        Args:
            func: Async function to execute
            *args: Function arguments
            priority: Priority level (1-10, lower = higher priority)
            timeout: Timeout in seconds
            **kwargs: Function keyword arguments

        Returns:
            Function result
        """
        self.queued_requests += 1

        try:
            async with self.semaphore:
                self.queued_requests -= 1
                self.active_requests += 1

                try:
                    result = await asyncio.wait_for(
                        func(*args, **kwargs),
                        timeout=timeout
                    )
                    return result
                finally:
                    self.active_requests -= 1

        except asyncio.TimeoutError:
            logger.warning(f"Request timed out after {timeout}s")
            return None

    def get_stats(self) -> Dict[str, Any]:
        """Get queue statistics"""
        return {
            "active_requests": self.active_requests,
            "queued_requests": self.queued_requests,
            "max_concurrent": self.max_concurrent,
            "available_slots": self.semaphore._value
        }


# Global instances
conversation_manager = ConversationManager()
rate_limiter = RateLimiter()
request_queue = RequestQueue(max_concurrent=3)


# Helper functions for easy integration
async def generate_with_rate_limit(
    user_id: str,
    prompt: str,
    **kwargs
) -> Optional[Dict[str, Any]]:
    """
    Generate text with rate limiting.

    Args:
        user_id: User identifier for rate limiting
        prompt: Text prompt
        **kwargs: Additional parameters

    Returns:
        LLM response or None
    """
    # Check rate limit
    allowed, reason = rate_limiter.check_rate_limit(user_id)
    if not allowed:
        logger.warning(f"Rate limit exceeded for user {user_id}: {reason}")
        return {
            "text": None,
            "available": False,
            "error": reason,
            "rate_limited": True
        }

    # Record request
    rate_limiter.record_request(user_id)

    # Enqueue and execute
    result = await request_queue.enqueue(
        llm_service.generate,
        prompt,
        **kwargs
    )

    return result


async def chat_with_history(
    conversation_id: str,
    user_message: str,
    user_id: Optional[str] = None,
    **kwargs
) -> Optional[Dict[str, Any]]:
    """
    Chat with conversation history and rate limiting.

    Args:
        conversation_id: Conversation identifier
        user_message: User's message
        user_id: Optional user ID for rate limiting
        **kwargs: Additional parameters

    Returns:
        LLM response with conversation context
    """
    # Apply rate limiting if user_id provided
    if user_id:
        allowed, reason = rate_limiter.check_rate_limit(user_id)
        if not allowed:
            return {
                "text": None,
                "available": False,
                "error": reason,
                "rate_limited": True
            }
        rate_limiter.record_request(user_id)

    # Generate with context
    result = await request_queue.enqueue(
        conversation_manager.generate_with_context,
        conversation_id,
        user_message,
        **kwargs
    )

    return result
