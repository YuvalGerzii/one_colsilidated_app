"""
Outreach Agent

Autonomous agent for personalized email and message campaigns.
Integrates with Bond.AI for connection intelligence and Labor platform for job applications.

Features:
- Multi-channel outreach (Email, LinkedIn, SMS)
- Personalization using AI
- Sequence management
- Response tracking
- A/B testing
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import asyncio
import logging

from .base_autonomous_agent import (
    BaseAutonomousAgent, AgentAction, ActionResult, AgentConfig,
    ActionType, ActionStatus, RiskLevel
)

logger = logging.getLogger(__name__)


class OutreachAgent(BaseAutonomousAgent):
    """
    Sends personalized outreach messages across channels.

    Use cases:
    - Investor outreach for real estate deals
    - Job application follow-ups
    - Network nurturing sequences
    - Sales campaigns
    """

    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.email_provider = None  # SendGrid, Mailgun, etc.
        self.linkedin_client = None
        self.sms_provider = None
        self.sent_messages: List[Dict[str, Any]] = []
        self.sequences: Dict[str, List[Dict[str, Any]]] = {}

    async def plan_actions(
        self,
        objective: str,
        context: Dict[str, Any]
    ) -> List[AgentAction]:
        """Plan outreach actions based on objective"""

        actions = []

        if "campaign" in objective.lower():
            actions = await self._plan_campaign(context)
        elif "follow_up" in objective.lower():
            actions = await self._plan_follow_ups(context)
        elif "sequence" in objective.lower():
            actions = await self._plan_sequence(context)
        elif "introduction" in objective.lower():
            actions = await self._plan_introduction(context)

        return actions

    async def _plan_campaign(
        self,
        context: Dict[str, Any]
    ) -> List[AgentAction]:
        """Plan a multi-recipient campaign"""

        recipients = context.get("recipients", [])
        template = context.get("template", {})
        channel = context.get("channel", "email")

        actions = []

        for recipient in recipients:
            # Personalize message for each recipient
            personalized_content = await self._personalize_message(
                template, recipient, context
            )

            action = AgentAction(
                action_id=self.create_action_id(),
                action_type=ActionType.SEND_EMAIL if channel == "email" else ActionType.SEND_MESSAGE,
                description=f"Send {channel} to {recipient.get('name', 'Unknown')}",
                parameters={
                    "channel": channel,
                    "recipient": recipient,
                    "subject": personalized_content.get("subject"),
                    "body": personalized_content.get("body"),
                    "from_name": context.get("from_name", "Your Name"),
                    "reply_to": context.get("reply_to"),
                    "track_opens": True,
                    "track_clicks": True
                },
                risk_level=RiskLevel.LOW,
                estimated_impact={
                    "messages_sent": 1,
                    "expected_response_rate": 0.15
                },
                rollback_steps=[
                    "Cannot recall sent message",
                    f"Log sent message to {recipient.get('email')}"
                ]
            )
            actions.append(action)

        return actions

    async def _plan_follow_ups(
        self,
        context: Dict[str, Any]
    ) -> List[AgentAction]:
        """Plan follow-up messages for non-responders"""

        # Get people who haven't responded
        original_campaign_id = context.get("campaign_id")
        days_since = context.get("days_since", 3)

        # Simulated: Get non-responders from database
        non_responders = context.get("non_responders", [])

        actions = []

        for recipient in non_responders:
            follow_up_content = await self._generate_follow_up(
                recipient, context
            )

            action = AgentAction(
                action_id=self.create_action_id(),
                action_type=ActionType.SEND_EMAIL,
                description=f"Follow-up to {recipient.get('name', 'Unknown')}",
                parameters={
                    "channel": "email",
                    "recipient": recipient,
                    "subject": follow_up_content.get("subject"),
                    "body": follow_up_content.get("body"),
                    "is_follow_up": True,
                    "original_campaign_id": original_campaign_id,
                    "follow_up_number": recipient.get("follow_up_count", 0) + 1
                },
                risk_level=RiskLevel.LOW,
                estimated_impact={
                    "messages_sent": 1,
                    "expected_response_rate": 0.10  # Lower for follow-ups
                },
                rollback_steps=["Log follow-up attempt"]
            )
            actions.append(action)

        return actions

    async def _plan_sequence(
        self,
        context: Dict[str, Any]
    ) -> List[AgentAction]:
        """Plan a multi-step outreach sequence"""

        sequence_name = context.get("sequence_name", "default")
        recipients = context.get("recipients", [])
        steps = context.get("steps", [
            {"delay_days": 0, "template": "initial"},
            {"delay_days": 3, "template": "follow_up_1"},
            {"delay_days": 7, "template": "follow_up_2"},
            {"delay_days": 14, "template": "break_up"}
        ])

        actions = []

        for recipient in recipients:
            for i, step in enumerate(steps):
                send_date = datetime.now() + timedelta(days=step.get("delay_days", 0))

                action = AgentAction(
                    action_id=self.create_action_id(),
                    action_type=ActionType.SEND_EMAIL,
                    description=f"Sequence step {i+1} to {recipient.get('name')}",
                    parameters={
                        "channel": "email",
                        "recipient": recipient,
                        "template": step.get("template"),
                        "sequence_name": sequence_name,
                        "step_number": i + 1,
                        "scheduled_time": send_date.isoformat(),
                        "stop_on_reply": True
                    },
                    risk_level=RiskLevel.LOW,
                    estimated_impact={"sequence_step": i + 1},
                    rollback_steps=["Cancel remaining sequence steps"],
                    deadline=send_date
                )
                actions.append(action)

        return actions

    async def _plan_introduction(
        self,
        context: Dict[str, Any]
    ) -> List[AgentAction]:
        """Plan warm introduction between two parties"""

        introducer = context.get("introducer", {})
        party_a = context.get("party_a", {})
        party_b = context.get("party_b", {})
        reason = context.get("reason", "mutual benefit")

        actions = []

        # Step 1: Ask permission from introducer
        permission_action = AgentAction(
            action_id=self.create_action_id(),
            action_type=ActionType.SEND_EMAIL,
            description=f"Request introduction permission from {introducer.get('name')}",
            parameters={
                "channel": "email",
                "recipient": introducer,
                "template": "introduction_permission",
                "context": {
                    "party_a": party_a,
                    "party_b": party_b,
                    "reason": reason
                }
            },
            risk_level=RiskLevel.LOW,
            estimated_impact={"introduction_requested": 1},
            rollback_steps=["Cancel introduction request"]
        )
        actions.append(permission_action)

        # Step 2: Make introduction (conditional on approval)
        intro_action = AgentAction(
            action_id=self.create_action_id(),
            action_type=ActionType.SEND_EMAIL,
            description=f"Introduce {party_a.get('name')} to {party_b.get('name')}",
            parameters={
                "channel": "email",
                "recipients": [party_a, party_b],
                "cc": [introducer],
                "template": "warm_introduction",
                "context": {"reason": reason}
            },
            risk_level=RiskLevel.MEDIUM,
            estimated_impact={"introductions_made": 1},
            rollback_steps=["Send apology for premature introduction"],
            dependencies=[permission_action.action_id],
            requires_approval=True,
            approval_reason="Confirm introduction permission received"
        )
        actions.append(intro_action)

        return actions

    async def _personalize_message(
        self,
        template: Dict[str, Any],
        recipient: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Personalize message template for recipient"""

        # Use LLM for advanced personalization (simulated)
        base_subject = template.get("subject", "Hello {name}")
        base_body = template.get("body", "Dear {name},\n\n{message}")

        # Simple variable replacement
        personalized_subject = base_subject.format(
            name=recipient.get("name", "there"),
            company=recipient.get("company", "your company"),
            title=recipient.get("title", "")
        )

        personalized_body = base_body.format(
            name=recipient.get("name", "there"),
            company=recipient.get("company", "your company"),
            title=recipient.get("title", ""),
            message=context.get("message", "")
        )

        # Add personalization based on recipient data
        if recipient.get("recent_activity"):
            personalized_body = f"I noticed {recipient['recent_activity']}.\n\n" + personalized_body

        return {
            "subject": personalized_subject,
            "body": personalized_body
        }

    async def _generate_follow_up(
        self,
        recipient: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate follow-up message"""

        follow_up_count = recipient.get("follow_up_count", 0)

        if follow_up_count == 0:
            subject = f"Following up - {context.get('topic', 'our conversation')}"
            body = f"Hi {recipient.get('name', 'there')},\n\nI wanted to follow up on my previous message..."
        elif follow_up_count == 1:
            subject = f"Quick follow-up"
            body = f"Hi {recipient.get('name', 'there')},\n\nJust bumping this to the top of your inbox..."
        else:
            subject = f"Last attempt to connect"
            body = f"Hi {recipient.get('name', 'there')},\n\nI don't want to be a pest, so this will be my last message..."

        return {"subject": subject, "body": body}

    async def execute_action(self, action: AgentAction) -> ActionResult:
        """Execute an outreach action"""

        params = action.parameters
        channel = params.get("channel", "email")

        try:
            if channel == "email":
                result = await self._send_email(params)
            elif channel == "linkedin":
                result = await self._send_linkedin_message(params)
            elif channel == "sms":
                result = await self._send_sms(params)
            else:
                raise ValueError(f"Unknown channel: {channel}")

            # Track sent message
            self.sent_messages.append({
                "action_id": action.action_id,
                "channel": channel,
                "recipient": params.get("recipient", {}),
                "sent_at": datetime.now().isoformat(),
                "message_id": result.get("message_id")
            })

            return ActionResult(
                action_id=action.action_id,
                status=ActionStatus.COMPLETED,
                result=result,
                side_effects=[f"Message sent via {channel}"],
                metadata={"channel": channel}
            )

        except Exception as e:
            logger.error(f"Outreach execution error: {e}")
            return ActionResult(
                action_id=action.action_id,
                status=ActionStatus.FAILED,
                result=None,
                error=str(e)
            )

    async def _send_email(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Send email (simulated)"""

        # In production, integrate with SendGrid, Mailgun, etc.
        await asyncio.sleep(0.05)  # Simulate API call

        return {
            "message_id": f"msg_{datetime.now().timestamp()}",
            "status": "sent",
            "recipient": params.get("recipient", {}).get("email"),
            "subject": params.get("subject"),
            "sent_at": datetime.now().isoformat()
        }

    async def _send_linkedin_message(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Send LinkedIn message (simulated)"""

        await asyncio.sleep(0.1)
        return {
            "message_id": f"li_msg_{datetime.now().timestamp()}",
            "status": "sent",
            "platform": "linkedin"
        }

    async def _send_sms(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Send SMS (simulated)"""

        await asyncio.sleep(0.05)
        return {
            "message_id": f"sms_{datetime.now().timestamp()}",
            "status": "sent",
            "platform": "sms"
        }

    async def rollback_action(self, action_id: str) -> bool:
        """Messages cannot be recalled, but we can log the attempt"""
        logger.warning(f"Cannot rollback sent message {action_id}")
        return False

    def get_campaign_stats(self) -> Dict[str, Any]:
        """Get outreach statistics"""

        return {
            "total_sent": len(self.sent_messages),
            "by_channel": self._count_by_channel(),
            "sent_today": self._count_sent_today()
        }

    def _count_by_channel(self) -> Dict[str, int]:
        """Count messages by channel"""
        counts = {}
        for msg in self.sent_messages:
            channel = msg.get("channel", "unknown")
            counts[channel] = counts.get(channel, 0) + 1
        return counts

    def _count_sent_today(self) -> int:
        """Count messages sent today"""
        today = datetime.now().date()
        return len([
            m for m in self.sent_messages
            if datetime.fromisoformat(m["sent_at"]).date() == today
        ])


# Factory function
def create_outreach_agent(
    agent_id: str = "outreach_agent_1",
    daily_limit: int = 100,
    dry_run: bool = True
) -> OutreachAgent:
    """Create a configured outreach agent"""

    config = AgentConfig(
        agent_id=agent_id,
        name="Outreach Agent",
        max_concurrent_actions=10,
        action_timeout_seconds=30,
        auto_approve_risk_levels=[RiskLevel.LOW],
        spending_limit_usd=100.0,  # For paid email services
        daily_action_limit=daily_limit,
        require_human_approval_above=0,  # All messages auto-approved by default
        enabled=True,
        dry_run=dry_run
    )

    return OutreachAgent(config)
