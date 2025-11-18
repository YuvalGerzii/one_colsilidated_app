"""
Slack Integration - Team Communication & Notifications
Sends notifications and updates to Slack channels

Note: Free Slack app creation
Documentation: https://api.slack.com/
"""

from typing import Dict, Any, Optional, List
import httpx
from ..base import BaseIntegration, IntegrationConfig, IntegrationMetadata, IntegrationResponse


class SlackIntegration(BaseIntegration):
    """
    Integration with Slack API for notifications

    Note: Free to create Slack apps
    """

    BASE_URL = "https://slack.com/api"

    def __init__(self, config: IntegrationConfig):
        config.is_free = True
        config.requires_api_key = True  # Bot token
        super().__init__(config)

    def get_metadata(self) -> IntegrationMetadata:
        return IntegrationMetadata(
            name="Slack",
            category="tools",
            description="Send notifications and updates to Slack channels",
            is_free=True,
            requires_api_key=True,
            documentation_url="https://api.slack.com/",
            features=[
                "Send messages to channels",
                "Post deal updates",
                "Financial report notifications",
                "Alert on portfolio changes",
                "File sharing",
                "Completely free"
            ]
        )

    async def test_connection(self) -> IntegrationResponse:
        """Test Slack API connection"""
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="Slack integration not configured. Set SLACK_BOT_TOKEN."
            )

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.BASE_URL}/auth.test",
                    headers={"Authorization": f"Bearer {self.config.api_key}"},
                    timeout=10.0
                )
                response.raise_for_status()

                data = response.json()

                if data.get("ok"):
                    return self._success_response({
                        "message": "Successfully connected to Slack API",
                        "team": data.get("team"),
                        "user": data.get("user"),
                        "bot_id": data.get("bot_id")
                    })
                else:
                    return IntegrationResponse(
                        success=False,
                        error=f"Slack API error: {data.get('error')}"
                    )

        except Exception as e:
            return self._handle_error(e, "Slack connection test")

    async def send_message(
        self,
        channel: str,
        text: str,
        blocks: Optional[List[Dict[str, Any]]] = None
    ) -> IntegrationResponse:
        """
        Send a message to a Slack channel

        Args:
            channel: Channel ID or name (e.g., "#general")
            text: Message text
            blocks: Optional rich message blocks
        """
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="Slack integration not configured"
            )

        try:
            payload = {
                "channel": channel,
                "text": text
            }

            if blocks:
                payload["blocks"] = blocks

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.BASE_URL}/chat.postMessage",
                    headers={"Authorization": f"Bearer {self.config.api_key}"},
                    json=payload,
                    timeout=10.0
                )
                response.raise_for_status()

                data = response.json()

                if data.get("ok"):
                    return self._success_response({
                        "message_sent": True,
                        "channel": data.get("channel"),
                        "timestamp": data.get("ts")
                    })
                else:
                    return IntegrationResponse(
                        success=False,
                        error=f"Slack API error: {data.get('error')}"
                    )

        except Exception as e:
            return self._handle_error(e, "send_message")

    async def send_deal_notification(
        self,
        channel: str,
        deal_name: str,
        deal_type: str,
        amount: float,
        status: str,
        details: Optional[Dict[str, Any]] = None
    ) -> IntegrationResponse:
        """
        Send a formatted deal notification

        Args:
            channel: Slack channel
            deal_name: Name of the deal
            deal_type: Type of deal (e.g., "Fix & Flip", "Rental")
            amount: Deal amount
            status: Deal status
            details: Additional details
        """
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="Slack integration not configured"
            )

        # Create rich message blocks
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"🏠 {deal_name}"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Type:*\n{deal_type}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Amount:*\n${amount:,.2f}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Status:*\n{status}"
                    }
                ]
            }
        ]

        if details:
            fields = []
            for key, value in details.items():
                fields.append({
                    "type": "mrkdwn",
                    "text": f"*{key}:*\n{value}"
                })

            if fields:
                blocks.append({
                    "type": "section",
                    "fields": fields
                })

        return await self.send_message(
            channel=channel,
            text=f"New Deal: {deal_name}",
            blocks=blocks
        )

    async def send_report_notification(
        self,
        channel: str,
        report_type: str,
        summary: Dict[str, Any]
    ) -> IntegrationResponse:
        """
        Send a financial report notification

        Args:
            channel: Slack channel
            report_type: Type of report
            summary: Report summary data
        """
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="Slack integration not configured"
            )

        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"📊 {report_type} Report"
                }
            }
        ]

        if summary:
            fields = []
            for key, value in summary.items():
                fields.append({
                    "type": "mrkdwn",
                    "text": f"*{key}:*\n{value}"
                })

            blocks.append({
                "type": "section",
                "fields": fields
            })

        return await self.send_message(
            channel=channel,
            text=f"{report_type} Report Available",
            blocks=blocks
        )
