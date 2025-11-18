"""
Unit Tests for LLM Service

Tests graceful degradation, caching, rate limiting, and core functionality.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, Mock, patch
from datetime import datetime

from app.services.llm_service import LLMService, llm_service
from app.services.llm_advanced import (
    ConversationManager,
    RateLimiter,
    RequestQueue,
    conversation_manager,
    rate_limiter
)


# ================================
# LLM SERVICE TESTS
# ================================

@pytest.mark.asyncio
async def test_llm_service_initialization():
    """Test LLM service initializes correctly"""
    service = LLMService()

    assert service.enabled is True
    assert service.model == "gemma:2b"
    assert service.timeout == 30
    assert service.max_retries == 2
    assert service.metrics["total_requests"] == 0


@pytest.mark.asyncio
async def test_llm_health_check_disabled():
    """Test health check when LLM is disabled"""
    service = LLMService()
    service.enabled = False

    health = await service.health_check()

    assert health["status"] == "disabled"
    assert health["available"] is False


@pytest.mark.asyncio
@patch("httpx.AsyncClient.get")
async def test_llm_health_check_healthy(mock_get):
    """Test health check when LLM is healthy"""
    # Mock successful health check
    mock_response = Mock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    service = LLMService()
    health = await service.health_check()

    assert health["status"] == "healthy"
    assert health["available"] is True


@pytest.mark.asyncio
async def test_llm_graceful_degradation_when_disabled():
    """Test graceful degradation when LLM is disabled"""
    service = LLMService()
    service.enabled = False

    result = await service.generate(
        prompt="Test prompt"
    )

    assert result is None
    assert service.metrics["failed_requests"] > 0


@pytest.mark.asyncio
async def test_llm_cache_key_generation():
    """Test cache key is generated consistently"""
    service = LLMService()

    key1 = service._generate_cache_key(
        "test prompt",
        system_prompt="system",
        temperature=0.7
    )

    key2 = service._generate_cache_key(
        "test prompt",
        system_prompt="system",
        temperature=0.7
    )

    # Same inputs should generate same cache key
    assert key1 == key2

    # Different inputs should generate different keys
    key3 = service._generate_cache_key(
        "different prompt",
        system_prompt="system",
        temperature=0.7
    )

    assert key1 != key3


@pytest.mark.asyncio
async def test_llm_metrics_tracking():
    """Test metrics are tracked correctly"""
    service = LLMService()
    service.enabled = False

    initial_requests = service.metrics["total_requests"]

    await service.generate("test")

    assert service.metrics["total_requests"] == initial_requests + 1


@pytest.mark.asyncio
async def test_llm_get_metrics():
    """Test get_metrics returns calculated fields"""
    service = LLMService()
    service.metrics["total_requests"] = 100
    service.metrics["successful_requests"] = 95
    service.metrics["cache_hits"] = 40

    metrics = service.get_metrics()

    assert metrics["success_rate"] == 0.95
    assert metrics["cache_hit_rate"] == 0.4


# ================================
# CONVERSATION MANAGER TESTS
# ================================

def test_create_conversation():
    """Test conversation creation"""
    manager = ConversationManager()
    conv_id = manager.create_conversation(user_id="test_user")

    assert conv_id is not None
    assert conv_id in manager.conversations
    assert manager.conversations[conv_id]["user_id"] == "test_user"


def test_add_message_to_conversation():
    """Test adding messages to conversation"""
    manager = ConversationManager()
    conv_id = manager.create_conversation()

    success = manager.add_message(
        conv_id,
        role="user",
        content="Hello"
    )

    assert success is True
    messages = manager.get_messages(conv_id)
    assert len(messages) == 1
    assert messages[0]["content"] == "Hello"


def test_conversation_history_trimming():
    """Test conversation history is trimmed when too long"""
    manager = ConversationManager(max_history=5)
    conv_id = manager.create_conversation()

    # Add 10 messages
    for i in range(10):
        manager.add_message(conv_id, "user", f"Message {i}")

    messages = manager.get_messages(conv_id)

    # Should only keep last 5
    assert len(messages) == 5
    assert messages[0]["content"] == "Message 5"
    assert messages[-1]["content"] == "Message 9"


def test_delete_conversation():
    """Test conversation deletion"""
    manager = ConversationManager()
    conv_id = manager.create_conversation()

    assert manager.delete_conversation(conv_id) is True
    assert conv_id not in manager.conversations


def test_get_nonexistent_conversation():
    """Test getting non-existent conversation returns None"""
    manager = ConversationManager()
    result = manager.get_conversation("nonexistent_id")

    assert result is None


# ================================
# RATE LIMITER TESTS
# ================================

def test_rate_limiter_allows_within_limits():
    """Test rate limiter allows requests within limits"""
    limiter = RateLimiter(requests_per_minute=10)

    # First request should be allowed
    allowed, reason = limiter.check_rate_limit("user1")

    assert allowed is True
    assert reason is None


def test_rate_limiter_blocks_exceeding_minute_limit():
    """Test rate limiter blocks when minute limit exceeded"""
    limiter = RateLimiter(requests_per_minute=3)

    user_id = "test_user"

    # Make 3 requests (at limit)
    for _ in range(3):
        limiter.record_request(user_id)

    # 4th request should be blocked
    allowed, reason = limiter.check_rate_limit(user_id)

    assert allowed is False
    assert "per minute" in reason


def test_rate_limiter_blocks_exceeding_hour_limit():
    """Test rate limiter blocks when hour limit exceeded"""
    limiter = RateLimiter(
        requests_per_minute=100,  # High minute limit
        requests_per_hour=5  # Low hour limit
    )

    user_id = "test_user"

    # Make 5 requests
    for _ in range(5):
        limiter.record_request(user_id)

    # 6th request should be blocked by hour limit
    allowed, reason = limiter.check_rate_limit(user_id)

    assert allowed is False
    assert "per hour" in reason


def test_rate_limiter_usage_stats():
    """Test rate limiter provides usage statistics"""
    limiter = RateLimiter(requests_per_minute=10, requests_per_hour=50)

    user_id = "test_user"

    # Make 3 requests
    for _ in range(3):
        limiter.record_request(user_id)

    stats = limiter.get_usage_stats(user_id)

    assert stats["requests_last_minute"] == 3
    assert stats["remaining_minute"] == 7
    assert stats["limit_per_minute"] == 10


def test_rate_limiter_global_limit():
    """Test global rate limit applies across all users"""
    limiter = RateLimiter(
        requests_per_minute=100,
        global_requests_per_minute=5
    )

    # Different users make requests
    for i in range(5):
        limiter.record_request(f"user{i}")

    # Next request from any user should be blocked by global limit
    allowed, reason = limiter.check_rate_limit("new_user")

    assert allowed is False
    assert "Global rate limit" in reason


# ================================
# REQUEST QUEUE TESTS
# ================================

@pytest.mark.asyncio
async def test_request_queue_limits_concurrency():
    """Test request queue limits concurrent requests"""
    queue = RequestQueue(max_concurrent=2)

    async def slow_task():
        await asyncio.sleep(0.1)
        return "done"

    # Start 3 tasks concurrently
    tasks = [
        queue.enqueue(slow_task)
        for _ in range(3)
    ]

    # While running, check that only 2 are active
    await asyncio.sleep(0.05)  # Give time for tasks to start

    stats = queue.get_stats()
    assert stats["active_requests"] <= 2

    # Wait for completion
    results = await asyncio.gather(*tasks)
    assert len(results) == 3


@pytest.mark.asyncio
async def test_request_queue_timeout():
    """Test request queue handles timeouts"""
    queue = RequestQueue()

    async def timeout_task():
        await asyncio.sleep(10)  # Long sleep
        return "done"

    # Should timeout after 1 second
    result = await queue.enqueue(timeout_task, timeout=1)

    assert result is None  # Returns None on timeout


@pytest.mark.asyncio
async def test_request_queue_stats():
    """Test request queue provides statistics"""
    queue = RequestQueue(max_concurrent=2)

    async def quick_task():
        await asyncio.sleep(0.01)
        return "done"

    # Enqueue multiple tasks
    tasks = [queue.enqueue(quick_task) for _ in range(3)]

    # Check stats while running
    await asyncio.sleep(0.005)
    stats = queue.get_stats()

    assert stats["max_concurrent"] == 2
    assert "active_requests" in stats
    assert "queued_requests" in stats

    # Wait for completion
    await asyncio.gather(*tasks)


# ================================
# INTEGRATION TESTS
# ================================

@pytest.mark.asyncio
@patch("app.services.llm_service.llm_service.generate")
async def test_conversation_with_context(mock_generate):
    """Test conversation with context management"""
    # Mock LLM response
    mock_generate.return_value = {
        "text": "Hello! How can I help you?",
        "model": "gemma:2b",
        "timestamp": datetime.utcnow().isoformat()
    }

    manager = ConversationManager()
    conv_id = manager.create_conversation()

    # Generate response with context
    result = await manager.generate_with_context(
        conv_id,
        "Hello, I need help"
    )

    assert result is not None
    assert result["text"] == "Hello! How can I help you?"

    # Check messages were added to history
    messages = manager.get_messages(conv_id)
    assert len(messages) == 2  # User message + assistant response


@pytest.mark.asyncio
async def test_graceful_degradation_in_conversation():
    """Test conversation handles LLM unavailability"""
    manager = ConversationManager()
    conv_id = manager.create_conversation()

    # Mock LLM to return None (unavailable)
    with patch("app.services.llm_service.llm_service.generate", return_value=None):
        result = await manager.generate_with_context(
            conv_id,
            "Test message"
        )

        assert result is None

        # Message should not be added if LLM failed
        messages = manager.get_messages(conv_id)
        assert len(messages) == 0


# ================================
# MOCK HELPERS
# ================================

@pytest.fixture
def mock_llm_response():
    """Fixture for mocking LLM responses"""
    return {
        "text": "This is a test response",
        "model": "gemma:2b",
        "source": "local_llm",
        "timestamp": datetime.utcnow().isoformat(),
        "metadata": {
            "prompt_tokens": 10,
            "completion_tokens": 20,
            "total_tokens": 30
        }
    }


@pytest.fixture
def mock_cache_service():
    """Fixture for mocking cache service"""
    with patch("app.services.llm_service.cache_service") as mock:
        mock.get = AsyncMock(return_value=None)
        mock.set = AsyncMock(return_value=True)
        yield mock


# Run all tests with: pytest backend/tests/test_llm_service.py -v
