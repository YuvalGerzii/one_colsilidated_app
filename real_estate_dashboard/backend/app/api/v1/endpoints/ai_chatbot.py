"""
AI Chatbot API Endpoints

Provides REST and WebSocket endpoints for AI-powered real estate assistance.
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from loguru import logger
import json

from app.services.ai_chatbot import get_chatbot


router = APIRouter()


# Request/Response Models
class ChatRequest(BaseModel):
    """Chat message request."""
    message: str
    conversation_id: Optional[str] = "default"
    context: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    """Chat message response."""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    agent: str
    agent_name: str
    insights: List[str] = []
    recommendations: List[str] = []
    confidence: Optional[float] = None
    quality_score: Optional[float] = None


class ConversationHistoryResponse(BaseModel):
    """Conversation history response."""
    conversation_id: str
    messages: List[Dict[str, Any]]
    message_count: int


class AgentCapabilitiesResponse(BaseModel):
    """Agent capabilities response."""
    agents: Dict[str, List[Dict[str, Any]]]


# REST Endpoints

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Send a message to the AI chatbot.

    The chatbot uses specialized real estate agents to provide expert analysis:
    - Property Analyst: Valuation, cash flow, investment metrics
    - Market Researcher: Market trends, demographics, competitive analysis
    - Investment Strategist: Portfolio optimization, tax strategy
    - Deal Evaluator: Underwriting, sensitivity analysis, risk assessment
    """
    try:
        chatbot = get_chatbot()
        response = await chatbot.chat(
            user_message=request.message,
            conversation_id=request.conversation_id,
            context=request.context
        )
        return response
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Stream chat response in real-time for better UX.

    Returns Server-Sent Events (SSE) stream with incremental response data.
    """
    try:
        chatbot = get_chatbot()

        async def event_generator():
            async for chunk in chatbot.chat_stream(
                user_message=request.message,
                conversation_id=request.conversation_id,
                context=request.context
            ):
                yield f"data: {chunk}\n\n"

        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",
            }
        )
    except Exception as e:
        logger.error(f"Stream chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversation/{conversation_id}", response_model=ConversationHistoryResponse)
async def get_conversation_history(conversation_id: str):
    """Get full conversation history."""
    chatbot = get_chatbot()
    history = chatbot.get_conversation_history(conversation_id)

    return {
        "conversation_id": conversation_id,
        "messages": history,
        "message_count": len(history)
    }


@router.delete("/conversation/{conversation_id}")
async def clear_conversation(conversation_id: str):
    """Clear conversation history."""
    chatbot = get_chatbot()
    chatbot.clear_conversation(conversation_id)

    return {
        "success": True,
        "message": f"Conversation {conversation_id} cleared"
    }


@router.get("/agents/capabilities", response_model=AgentCapabilitiesResponse)
async def get_agent_capabilities():
    """
    Get capabilities of all available AI agents.

    Returns detailed information about each specialized agent and their expertise.
    """
    chatbot = get_chatbot()
    capabilities = chatbot.get_agent_capabilities()

    return {"agents": capabilities}


@router.get("/agents/info")
async def get_agents_info():
    """Get detailed information about available agents."""
    return {
        "agents": [
            {
                "id": "property_analyst",
                "name": "Property Analyst",
                "description": "Expert in property valuation, cash flow analysis, and investment metrics",
                "capabilities": [
                    "Property valuation (CMA, DCF)",
                    "Cash flow projections",
                    "Investment metrics (Cap Rate, NOI, DSCR, ROI, IRR)",
                    "Rental market analysis",
                    "Risk assessment"
                ],
                "proficiency": 0.93,
                "use_cases": [
                    "How much is this property worth?",
                    "What's the cash flow potential?",
                    "Calculate the cap rate and NOI",
                    "Is this a good investment?"
                ]
            },
            {
                "id": "market_researcher",
                "name": "Market Research Specialist",
                "description": "Expert in market trends, demographics, and competitive analysis",
                "capabilities": [
                    "Market trend analysis",
                    "Demographic research",
                    "Economic indicators tracking",
                    "Competitive landscape analysis",
                    "Neighborhood profiling",
                    "Supply/demand dynamics"
                ],
                "proficiency": 0.91,
                "use_cases": [
                    "What are the market trends in Austin?",
                    "Analyze this neighborhood",
                    "Research the competitive landscape",
                    "What are the demographics?"
                ]
            },
            {
                "id": "investment_strategist",
                "name": "Investment Strategist",
                "description": "Expert in investment strategy, portfolio optimization, and tax planning",
                "capabilities": [
                    "Investment strategy development",
                    "Portfolio optimization",
                    "Risk-adjusted return analysis",
                    "Tax optimization strategies",
                    "Exit planning",
                    "Deal structuring"
                ],
                "proficiency": 0.92,
                "use_cases": [
                    "Create an investment strategy",
                    "Optimize my portfolio",
                    "Tax optimization strategies",
                    "When should I exit this investment?"
                ]
            },
            {
                "id": "deal_evaluator",
                "name": "Deal Evaluation Expert",
                "description": "Expert in deal underwriting, scenario analysis, and risk assessment",
                "capabilities": [
                    "Deal screening and filtering",
                    "Comprehensive underwriting",
                    "Sensitivity analysis",
                    "Scenario modeling (best/base/worst case)",
                    "Deal comparison and ranking",
                    "Investment committee memos"
                ],
                "proficiency": 0.94,
                "use_cases": [
                    "Should I buy this property?",
                    "Evaluate this deal",
                    "Run sensitivity analysis",
                    "Compare multiple deals"
                ]
            }
        ],
        "total_agents": 4,
        "multi_agent_coordination": True,
        "reinforcement_learning_enabled": False,  # Can be enabled for adaptive responses
    }


# WebSocket Endpoint for Real-time Chat

@router.websocket("/ws/chat/{conversation_id}")
async def websocket_chat(websocket: WebSocket, conversation_id: str):
    """
    WebSocket endpoint for real-time bidirectional chat.

    Provides lower latency and better real-time experience than REST.
    """
    await websocket.accept()
    chatbot = get_chatbot()

    logger.info(f"WebSocket connection established for conversation: {conversation_id}")

    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)

            user_message = message_data.get("message")
            context = message_data.get("context")

            if not user_message:
                await websocket.send_json({
                    "type": "error",
                    "message": "No message provided"
                })
                continue

            # Send acknowledgment
            await websocket.send_json({
                "type": "status",
                "message": "Processing your request...",
                "conversation_id": conversation_id
            })

            # Stream response
            async for chunk in chatbot.chat_stream(
                user_message=user_message,
                conversation_id=conversation_id,
                context=context
            ):
                # Parse and send chunk
                chunk_data = json.loads(chunk)
                await websocket.send_json(chunk_data)

    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for conversation: {conversation_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        await websocket.send_json({
            "type": "error",
            "message": f"Error: {str(e)}"
        })


# Demo/Test Endpoints

@router.post("/demo/chat")
async def demo_chat(message: Optional[str] = "Analyze a multifamily property in Austin, TX"):
    """
    Demo endpoint to test chatbot functionality.

    Uses example queries to demonstrate capabilities.
    """
    chatbot = get_chatbot()
    response = await chatbot.chat(
        user_message=message,
        conversation_id="demo"
    )
    return response


@router.get("/health")
async def health_check():
    """Health check for chatbot service."""
    chatbot = get_chatbot()
    agent_count = len(chatbot.agents)

    return {
        "status": "healthy",
        "service": "AI Chatbot",
        "agents_available": agent_count,
        "capabilities": list(chatbot.agents.keys())
    }
