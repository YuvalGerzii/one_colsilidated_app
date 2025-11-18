"""
Integration Manager - Central management for all third-party integrations
"""

from typing import Dict, List, Optional
import logging
from .base import BaseIntegration, IntegrationConfig, IntegrationMetadata, IntegrationResponse, IntegrationStatus

logger = logging.getLogger(__name__)


class IntegrationManager:
    """Manages all third-party integrations"""

    def __init__(self):
        self._integrations: Dict[str, BaseIntegration] = {}
        self.logger = logging.getLogger(__name__)

    def register(self, key: str, integration: BaseIntegration):
        """Register an integration"""
        self._integrations[key] = integration
        self.logger.info(f"Registered integration: {key} (Status: {integration.status.value})")

    def get(self, key: str) -> Optional[BaseIntegration]:
        """Get an integration by key"""
        return self._integrations.get(key)

    def get_all(self) -> Dict[str, BaseIntegration]:
        """Get all registered integrations"""
        return self._integrations

    def get_available(self) -> Dict[str, BaseIntegration]:
        """Get only available/active integrations"""
        return {
            key: integration
            for key, integration in self._integrations.items()
            if integration.is_available
        }

    def get_status_summary(self) -> Dict[str, Dict]:
        """Get status summary of all integrations"""
        summary = {}
        for key, integration in self._integrations.items():
            metadata = integration.get_metadata()
            summary[key] = {
                "name": metadata.name,
                "category": metadata.category,
                "status": integration.status.value,
                "is_free": metadata.is_free,
                "available": integration.is_available,
            }
        return summary

    def get_by_category(self, category: str) -> Dict[str, BaseIntegration]:
        """Get integrations by category"""
        return {
            key: integration
            for key, integration in self._integrations.items()
            if integration.get_metadata().category == category
        }

    async def test_all(self) -> Dict[str, IntegrationResponse]:
        """Test all integrations"""
        results = {}
        for key, integration in self._integrations.items():
            if integration.is_available:
                results[key] = await integration.test_connection()
            else:
                results[key] = IntegrationResponse(
                    success=False,
                    error=f"Integration not configured or not available (Status: {integration.status.value})"
                )
        return results


# Global integration manager instance
integration_manager = IntegrationManager()
