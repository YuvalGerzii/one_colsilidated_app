"""
Plaid Integration - Bank Account Linking
Provides bank account connection and transaction data

Note: Plaid has a free development/sandbox environment
Documentation: https://plaid.com/docs/
"""

from typing import Dict, Any, Optional, List
import httpx
from ..base import BaseIntegration, IntegrationConfig, IntegrationMetadata, IntegrationResponse


class PlaidIntegration(BaseIntegration):
    """
    Integration with Plaid API for bank account linking

    Note: Free sandbox environment for development
    Production requires paid plan
    """

    def __init__(self, config: IntegrationConfig):
        config.is_free = True  # Sandbox is free
        config.requires_api_key = True  # Requires client_id and secret
        super().__init__(config)

        # Plaid uses multiple credentials
        self.client_id = config.additional_config.get("client_id")
        self.secret = config.additional_config.get("secret")
        self.environment = config.additional_config.get("environment", "sandbox")

        # Environment URLs
        self.base_urls = {
            "sandbox": "https://sandbox.plaid.com",
            "development": "https://development.plaid.com",
            "production": "https://production.plaid.com"
        }
        self.base_url = self.base_urls.get(self.environment, self.base_urls["sandbox"])

    def get_metadata(self) -> IntegrationMetadata:
        return IntegrationMetadata(
            name="Plaid",
            category="banking",
            description="Bank account linking and financial data access",
            is_free=True,
            requires_api_key=True,
            documentation_url="https://plaid.com/docs/",
            features=[
                "Bank account connection",
                "Account balance checking",
                "Transaction history",
                "Identity verification",
                "Income verification",
                "Assets and liabilities",
                "Free sandbox environment for development"
            ]
        )

    async def test_connection(self) -> IntegrationResponse:
        """Test Plaid API connection"""
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="Plaid integration not configured. Set PLAID_CLIENT_ID and PLAID_SECRET."
            )

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/item/public_token/create",
                    json={
                        "client_id": self.client_id,
                        "secret": self.secret,
                        "institution_id": "ins_3",  # Chase (sandbox)
                        "initial_products": ["auth"]
                    },
                    timeout=10.0
                )

                if response.status_code == 200:
                    return self._success_response({
                        "message": f"Successfully connected to Plaid API ({self.environment} environment)",
                        "environment": self.environment
                    })
                else:
                    return IntegrationResponse(
                        success=False,
                        error=f"Plaid API error: {response.text}"
                    )

        except Exception as e:
            return self._handle_error(e, "Plaid connection test")

    async def create_link_token(
        self,
        user_id: str,
        client_name: str = "Real Estate Dashboard"
    ) -> IntegrationResponse:
        """
        Create a link token for Plaid Link initialization

        Args:
            user_id: Your application's user identifier
            client_name: Name shown in Plaid Link
        """
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="Plaid integration not configured"
            )

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/link/token/create",
                    json={
                        "client_id": self.client_id,
                        "secret": self.secret,
                        "user": {"client_user_id": user_id},
                        "client_name": client_name,
                        "products": ["auth", "transactions"],
                        "country_codes": ["US"],
                        "language": "en"
                    },
                    timeout=10.0
                )
                response.raise_for_status()

                data = response.json()

                return self._success_response({
                    "link_token": data.get("link_token"),
                    "expiration": data.get("expiration")
                })

        except Exception as e:
            return self._handle_error(e, "create_link_token")

    async def exchange_public_token(self, public_token: str) -> IntegrationResponse:
        """
        Exchange public token for access token

        Args:
            public_token: Public token from Plaid Link
        """
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="Plaid integration not configured"
            )

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/item/public_token/exchange",
                    json={
                        "client_id": self.client_id,
                        "secret": self.secret,
                        "public_token": public_token
                    },
                    timeout=10.0
                )
                response.raise_for_status()

                data = response.json()

                return self._success_response({
                    "access_token": data.get("access_token"),
                    "item_id": data.get("item_id")
                })

        except Exception as e:
            return self._handle_error(e, "exchange_public_token")

    async def get_accounts(self, access_token: str) -> IntegrationResponse:
        """
        Get account information

        Args:
            access_token: Plaid access token
        """
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="Plaid integration not configured"
            )

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/accounts/get",
                    json={
                        "client_id": self.client_id,
                        "secret": self.secret,
                        "access_token": access_token
                    },
                    timeout=10.0
                )
                response.raise_for_status()

                data = response.json()

                return self._success_response({
                    "accounts": data.get("accounts", []),
                    "item": data.get("item")
                })

        except Exception as e:
            return self._handle_error(e, "get_accounts")

    async def get_balance(self, access_token: str) -> IntegrationResponse:
        """
        Get account balances

        Args:
            access_token: Plaid access token
        """
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="Plaid integration not configured"
            )

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/accounts/balance/get",
                    json={
                        "client_id": self.client_id,
                        "secret": self.secret,
                        "access_token": access_token
                    },
                    timeout=10.0
                )
                response.raise_for_status()

                data = response.json()

                return self._success_response({
                    "accounts": data.get("accounts", [])
                })

        except Exception as e:
            return self._handle_error(e, "get_balance")
