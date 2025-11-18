"""
Base classes for third-party integrations
"""

from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional, List, Callable, Awaitable
from pydantic import BaseModel, Field
import logging
import asyncio
import time

logger = logging.getLogger(__name__)


class IntegrationStatus(str, Enum):
    """Integration status states"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    NOT_CONFIGURED = "not_configured"


class IntegrationConfig(BaseModel):
    """Base configuration for integrations"""
    name: str
    category: str
    is_free: bool = False
    requires_api_key: bool = True
    api_key: Optional[str] = None
    additional_config: Dict[str, Any] = Field(default_factory=dict)
    enabled: bool = False


class IntegrationMetadata(BaseModel):
    """Metadata about an integration"""
    name: str
    category: str
    description: str
    is_free: bool
    requires_api_key: bool
    documentation_url: Optional[str] = None
    features: List[str] = Field(default_factory=list)


class IntegrationResponse(BaseModel):
    """Standard response format for integration operations"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    cached: bool = False


class BaseIntegration(ABC):
    """Abstract base class for all integrations"""

    def __init__(self, config: IntegrationConfig):
        self.config = config
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self._status = IntegrationStatus.NOT_CONFIGURED

        if self._validate_config():
            self._status = IntegrationStatus.ACTIVE
        else:
            self.logger.warning(f"{self.config.name} is not properly configured. Integration will be skipped.")

    def _validate_config(self) -> bool:
        """Validate integration configuration"""
        if not self.config.enabled:
            return False

        if self.config.requires_api_key and not self.config.api_key:
            return False

        return True

    @property
    def is_available(self) -> bool:
        """Check if integration is available for use"""
        return self._status == IntegrationStatus.ACTIVE

    @property
    def status(self) -> IntegrationStatus:
        """Get current integration status"""
        return self._status

    @abstractmethod
    def get_metadata(self) -> IntegrationMetadata:
        """Get integration metadata"""
        pass

    @abstractmethod
    async def test_connection(self) -> IntegrationResponse:
        """Test the integration connection"""
        pass

    def _handle_error(self, error: Exception, operation: str) -> IntegrationResponse:
        """Standard error handling for integrations"""
        error_msg = f"Error in {operation}: {str(error)}"
        self.logger.error(error_msg, exc_info=True)
        self._status = IntegrationStatus.ERROR
        return IntegrationResponse(
            success=False,
            error=error_msg
        )

    def _success_response(self, data: Dict[str, Any], cached: bool = False) -> IntegrationResponse:
        """Create a success response"""
        return IntegrationResponse(
            success=True,
            data=data,
            cached=cached
        )

    async def _retry_with_exponential_backoff(
        self,
        func: Callable[[], Awaitable[IntegrationResponse]],
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        operation_name: str = "operation"
    ) -> IntegrationResponse:
        """
        Retry an async function with exponential backoff

        Args:
            func: Async function to retry
            max_retries: Maximum number of retry attempts
            base_delay: Initial delay between retries (seconds)
            max_delay: Maximum delay between retries (seconds)
            operation_name: Name of operation for logging

        Returns:
            IntegrationResponse from successful call or final failure
        """
        last_error = None

        for attempt in range(max_retries + 1):
            try:
                result = await func()

                # If successful, return immediately
                if result.success:
                    if attempt > 0:
                        self.logger.info(f"{operation_name} succeeded after {attempt} retries")
                    return result

                # If not successful but no exception, this is a controlled failure
                # Don't retry controlled failures
                last_error = result.error
                self.logger.warning(f"{operation_name} returned controlled failure: {result.error}")
                return result

            except Exception as e:
                last_error = str(e)

                if attempt < max_retries:
                    # Calculate exponential backoff delay
                    delay = min(base_delay * (2 ** attempt), max_delay)

                    self.logger.warning(
                        f"{operation_name} failed (attempt {attempt + 1}/{max_retries + 1}): {str(e)}. "
                        f"Retrying in {delay:.1f}s..."
                    )

                    await asyncio.sleep(delay)
                else:
                    # Final attempt failed
                    self.logger.error(
                        f"{operation_name} failed after {max_retries + 1} attempts: {str(e)}"
                    )

        # All retries exhausted
        return self._handle_error(
            Exception(f"Operation failed after {max_retries + 1} attempts. Last error: {last_error}"),
            operation_name
        )
