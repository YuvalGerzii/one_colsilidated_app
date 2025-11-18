"""
Stripe Integration - Payment Processing
Handles investor payments and subscriptions

Note: Stripe has a free test mode
Documentation: https://stripe.com/docs/api
"""

from typing import Dict, Any, Optional
import httpx
from ..base import BaseIntegration, IntegrationConfig, IntegrationMetadata, IntegrationResponse


class StripeIntegration(BaseIntegration):
    """
    Integration with Stripe API for payment processing

    Note: Free test mode, production charges fees per transaction
    """

    BASE_URL = "https://api.stripe.com/v1"

    def __init__(self, config: IntegrationConfig):
        config.is_free = True  # Test mode is free
        config.requires_api_key = True
        super().__init__(config)

    def get_metadata(self) -> IntegrationMetadata:
        return IntegrationMetadata(
            name="Stripe",
            category="banking",
            description="Payment processing for investor payments and subscriptions",
            is_free=True,
            requires_api_key=True,
            documentation_url="https://stripe.com/docs/api",
            features=[
                "Payment processing",
                "Subscription management",
                "Invoice generation",
                "Customer management",
                "Payout tracking",
                "Free test mode",
                "No monthly fees (pay per transaction)"
            ]
        )

    async def test_connection(self) -> IntegrationResponse:
        """Test Stripe API connection"""
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="Stripe integration not configured. Set STRIPE_API_KEY."
            )

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.BASE_URL}/balance",
                    auth=(self.config.api_key, ""),
                    timeout=10.0
                )
                response.raise_for_status()

                data = response.json()

                is_test_mode = self.config.api_key.startswith("sk_test_")

                return self._success_response({
                    "message": f"Successfully connected to Stripe API ({'Test' if is_test_mode else 'Live'} mode)",
                    "test_mode": is_test_mode,
                    "balance": data
                })

        except Exception as e:
            return self._handle_error(e, "Stripe connection test")

    async def create_payment_intent(
        self,
        amount: int,
        currency: str = "usd",
        customer_id: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None
    ) -> IntegrationResponse:
        """
        Create a payment intent

        Args:
            amount: Amount in cents (e.g., 1000 = $10.00)
            currency: Currency code
            customer_id: Stripe customer ID
            metadata: Additional metadata
        """
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="Stripe integration not configured"
            )

        try:
            data = {
                "amount": amount,
                "currency": currency
            }

            if customer_id:
                data["customer"] = customer_id

            if metadata:
                for key, value in metadata.items():
                    data[f"metadata[{key}]"] = value

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.BASE_URL}/payment_intents",
                    data=data,
                    auth=(self.config.api_key, ""),
                    timeout=10.0
                )
                response.raise_for_status()

                result = response.json()

                return self._success_response({
                    "payment_intent": result
                })

        except Exception as e:
            return self._handle_error(e, "create_payment_intent")

    async def create_customer(
        self,
        email: str,
        name: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None
    ) -> IntegrationResponse:
        """
        Create a Stripe customer

        Args:
            email: Customer email
            name: Customer name
            metadata: Additional metadata
        """
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="Stripe integration not configured"
            )

        try:
            data = {"email": email}

            if name:
                data["name"] = name

            if metadata:
                for key, value in metadata.items():
                    data[f"metadata[{key}]"] = value

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.BASE_URL}/customers",
                    data=data,
                    auth=(self.config.api_key, ""),
                    timeout=10.0
                )
                response.raise_for_status()

                result = response.json()

                return self._success_response({
                    "customer": result
                })

        except Exception as e:
            return self._handle_error(e, "create_customer")

    async def get_balance(self) -> IntegrationResponse:
        """Get account balance"""
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="Stripe integration not configured"
            )

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.BASE_URL}/balance",
                    auth=(self.config.api_key, ""),
                    timeout=10.0
                )
                response.raise_for_status()

                data = response.json()

                return self._success_response({
                    "balance": data
                })

        except Exception as e:
            return self._handle_error(e, "get_balance")
