"""
AI Chatbot Service using Multi-Agent System

Provides intelligent conversation interface powered by specialized real estate agents.
"""

from typing import Any, Dict, List, Optional, AsyncGenerator
from datetime import datetime
from loguru import logger
import asyncio
import json

from app.multi_agent_system.core.types import Task, AgentCapability
from app.multi_agent_system.agents.real_estate_agents import create_real_estate_agents
from app.multi_agent_system.communication.message_bus import MessageBus

# RAG integration flag
RAG_ENABLED = True


class RealEstateChatbot:
    """
    AI Chatbot for real estate investment assistance.

    Powered by specialized agents:
    - Property Analyst: Valuation, cash flow, investment metrics
    - Market Researcher: Market trends, demographics, competitive analysis
    - Investment Strategist: Portfolio optimization, tax strategy, exit planning
    - Deal Evaluator: Underwriting, sensitivity analysis, risk assessment
    """

    def __init__(self):
        """Initialize the chatbot with specialized agents."""
        self.message_bus = MessageBus(max_queue_size=1000)
        self.agents = create_real_estate_agents(message_bus=self.message_bus)

        # Conversation history
        self.conversations: Dict[str, List[Dict[str, Any]]] = {}

        # Agent routing keywords
        self.agent_keywords = {
            "property_analyst": [
                "valuation", "value", "cash flow", "cap rate", "noi", "dscr",
                "rental income", "investment metrics", "property analysis",
                "roi", "return on investment", "property worth", "appraisal"
            ],
            "market_researcher": [
                "market", "trend", "demographic", "neighborhood", "area",
                "competition", "supply", "demand", "economic", "growth",
                "market analysis", "market research", "location", "submarket"
            ],
            "investment_strategist": [
                "strategy", "portfolio", "diversification", "tax", "1031",
                "exit", "sell", "refinance", "leverage", "optimize",
                "risk-adjusted", "allocation", "investment plan"
            ],
            "deal_evaluator": [
                "deal", "underwriting", "evaluate", "analyze deal", "opportunity",
                "screening", "scenario", "sensitivity", "risk assessment",
                "compare", "should i buy", "investment decision"
            ],
        }

        logger.info("RealEstateChatbot initialized with 4 specialized agents")

        # RAG context cache
        self._rag_enabled = RAG_ENABLED

    async def _get_rag_context(self, query: str, session_id: str = None) -> Dict[str, Any]:
        """
        Retrieve relevant context from RAG system.

        Returns context documents and metadata for enhanced responses.
        """
        if not self._rag_enabled:
            return {"context": [], "sources": []}

        try:
            from app.services.rag_engine import get_rag_engine
            from app.core.database import get_async_session

            # Get database session
            async with get_async_session() as db:
                engine = await get_rag_engine()
                result = await engine.query(
                    db=db,
                    query=query,
                    session_id=session_id,
                    top_k=3,
                    include_sources=True,
                    generate_response=False  # Just retrieve, don't generate
                )

                # Extract context
                context = []
                sources = []
                for source in result.get("sources", []):
                    context.append({
                        "content": source.get("content", ""),
                        "title": source.get("title", ""),
                        "score": source.get("score", 0.0)
                    })
                    sources.append({
                        "title": source.get("title", ""),
                        "type": source.get("source_type", ""),
                        "relevance": source.get("score", 0.0)
                    })

                logger.info(f"RAG retrieved {len(context)} relevant documents")

                return {
                    "context": context,
                    "sources": sources,
                    "query_id": result.get("query_id"),
                    "policy_action": result.get("policy_action")
                }

        except Exception as e:
            logger.warning(f"RAG context retrieval failed: {e}")
            return {"context": [], "sources": []}

    def _route_to_agent(self, user_message: str) -> str:
        """
        Route user message to appropriate agent based on keywords.

        Returns:
            Agent ID to handle the query
        """
        message_lower = user_message.lower()

        # Score each agent based on keyword matches
        scores = {}
        for agent_id, keywords in self.agent_keywords.items():
            score = sum(1 for keyword in keywords if keyword in message_lower)
            scores[agent_id] = score

        # Return agent with highest score, default to property_analyst
        best_agent = max(scores, key=scores.get)
        if scores[best_agent] == 0:
            # No keywords matched, use property analyst as default
            best_agent = "property_analyst"

        logger.info(f"Routing query to {best_agent} (scores: {scores})")
        return best_agent

    async def chat(
        self,
        user_message: str,
        conversation_id: str = "default",
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process user message and generate response.

        Args:
            user_message: User's question or request
            conversation_id: Unique conversation identifier
            context: Additional context (property data, user preferences, etc.)

        Returns:
            Dictionary with agent response and metadata
        """
        logger.info(f"[{conversation_id}] Processing: {user_message[:100]}")

        # Initialize conversation if new
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []

        # Add user message to history
        self.conversations[conversation_id].append({
            "role": "user",
            "content": user_message,
            "timestamp": datetime.now().isoformat(),
        })

        # Retrieve RAG context for enhanced responses
        rag_context = await self._get_rag_context(user_message, conversation_id)

        # Route to appropriate agent
        agent_id = self._route_to_agent(user_message)
        agent = self.agents[agent_id]

        # Merge RAG context with provided context
        enhanced_context = context or {}
        if rag_context.get("context"):
            enhanced_context["rag_documents"] = rag_context["context"]
            enhanced_context["rag_sources"] = rag_context["sources"]
            enhanced_context["rag_query_id"] = rag_context.get("query_id")

        # Create task for agent
        task = Task(
            id=f"chat_{conversation_id}_{len(self.conversations[conversation_id])}",
            description=user_message,
            priority=1,
            created_at=datetime.now(),
            metadata=enhanced_context
        )

        # Process with agent
        try:
            result = await agent.process_task(task)

            # Format response
            response = self._format_response(result, agent_id)

            # Add assistant response to history
            self.conversations[conversation_id].append({
                "role": "assistant",
                "content": response["message"],
                "data": response.get("data"),
                "agent": agent_id,
                "timestamp": datetime.now().isoformat(),
                "quality_score": result.quality_score,
            })

            # Include RAG sources in response
            if rag_context.get("sources"):
                response["rag_sources"] = rag_context["sources"]
                response["rag_query_id"] = rag_context.get("query_id")

            return response

        except Exception as e:
            logger.error(f"Error processing chat: {str(e)}")
            return {
                "success": False,
                "message": "I apologize, but I encountered an error processing your request. Please try again or rephrase your question.",
                "error": str(e),
                "agent": agent_id,
            }

    async def chat_stream(
        self,
        user_message: str,
        conversation_id: str = "default",
        context: Optional[Dict[str, Any]] = None
    ) -> AsyncGenerator[str, None]:
        """
        Stream chat response in chunks for real-time UI updates.

        Yields:
            JSON strings with incremental response data
        """
        # Send initial status
        yield json.dumps({
            "type": "status",
            "message": "Processing your request...",
            "timestamp": datetime.now().isoformat()
        }) + "\n"

        # Determine agent
        agent_id = self._route_to_agent(user_message)
        yield json.dumps({
            "type": "agent_selected",
            "agent": agent_id,
            "agent_name": self._get_agent_name(agent_id)
        }) + "\n"

        # Simulate thinking delay (in real implementation, this would be actual processing)
        await asyncio.sleep(0.5)

        yield json.dumps({
            "type": "status",
            "message": "Analyzing your query...",
        }) + "\n"

        # Process with agent
        response = await self.chat(user_message, conversation_id, context)

        # Stream the response
        if response.get("success", True):
            # Send message in chunks for streaming effect
            message = response["message"]
            chunk_size = 50
            for i in range(0, len(message), chunk_size):
                chunk = message[i:i + chunk_size]
                yield json.dumps({
                    "type": "message_chunk",
                    "content": chunk
                }) + "\n"
                await asyncio.sleep(0.05)  # Simulate streaming delay

            # Send complete data
            yield json.dumps({
                "type": "complete",
                "data": response.get("data"),
                "insights": response.get("insights", []),
                "recommendations": response.get("recommendations", []),
                "confidence": response.get("confidence"),
                "agent": agent_id
            }) + "\n"
        else:
            yield json.dumps({
                "type": "error",
                "message": response["message"]
            }) + "\n"

    def _format_response(self, result, agent_id: str) -> Dict[str, Any]:
        """Format agent result into user-friendly response."""
        if not result.success:
            return {
                "success": False,
                "message": "I couldn't complete that analysis. Please provide more details or try a different question.",
                "agent": agent_id,
            }

        data = result.data

        # Extract key information for conversational response
        message_parts = []

        # Add greeting based on agent
        greetings = {
            "property_analyst": "I've completed a comprehensive property analysis. Here's what I found:",
            "market_researcher": "I've researched the market for you. Here are the key insights:",
            "investment_strategist": "I've developed a strategic analysis. Here's my recommendation:",
            "deal_evaluator": "I've evaluated this opportunity. Here's my assessment:",
        }
        message_parts.append(greetings.get(agent_id, "Here's my analysis:"))

        # Add insights
        if "insights" in data:
            message_parts.append("\n\n**Key Insights:**")
            for insight in data["insights"][:5]:  # Top 5 insights
                message_parts.append(f"• {insight}")

        # Add recommendations
        if "recommendations" in data:
            message_parts.append("\n\n**Recommendations:**")
            for rec in data["recommendations"][:5]:  # Top 5 recommendations
                message_parts.append(f"• {rec}")

        # Add confidence
        if "confidence" in data:
            confidence_pct = int(data["confidence"] * 100)
            message_parts.append(f"\n\n*Analysis confidence: {confidence_pct}%*")

        message = "\n".join(message_parts)

        return {
            "success": True,
            "message": message,
            "data": data,
            "agent": agent_id,
            "agent_name": self._get_agent_name(agent_id),
            "insights": data.get("insights", []),
            "recommendations": data.get("recommendations", []),
            "confidence": data.get("confidence"),
            "quality_score": result.quality_score,
        }

    def _get_agent_name(self, agent_id: str) -> str:
        """Get human-friendly agent name."""
        names = {
            "property_analyst": "Property Analyst",
            "market_researcher": "Market Research Specialist",
            "investment_strategist": "Investment Strategist",
            "deal_evaluator": "Deal Evaluation Expert",
        }
        return names.get(agent_id, "AI Assistant")

    def get_conversation_history(self, conversation_id: str) -> List[Dict[str, Any]]:
        """Get full conversation history."""
        return self.conversations.get(conversation_id, [])

    def clear_conversation(self, conversation_id: str) -> None:
        """Clear conversation history."""
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            logger.info(f"Cleared conversation: {conversation_id}")

    def get_agent_capabilities(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get capabilities of all available agents."""
        capabilities = {}
        for agent_id, agent in self.agents.items():
            capabilities[agent_id] = [
                {
                    "name": cap.name,
                    "description": cap.description,
                    "proficiency": cap.proficiency if hasattr(cap, 'proficiency') else 0.9
                }
                for cap in agent.capabilities
            ]
        return capabilities


# Singleton instance
_chatbot_instance: Optional[RealEstateChatbot] = None


def get_chatbot() -> RealEstateChatbot:
    """Get or create chatbot singleton instance."""
    global _chatbot_instance
    if _chatbot_instance is None:
        _chatbot_instance = RealEstateChatbot()
    return _chatbot_instance
