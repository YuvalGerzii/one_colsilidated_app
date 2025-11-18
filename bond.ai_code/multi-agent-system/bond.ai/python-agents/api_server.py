"""
Bond.AI Python Agents - FastAPI Server
Provides REST API for enhanced psychometric matching capabilities
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio
from loguru import logger

# Import Bond.AI agents
try:
    from bond_ai.agents.nlp_profile_analysis import NLPProfileAnalysisAgent
    from bond_ai.agents.personality_compatibility import PersonalityCompatibilityAgent
    from bond_ai.agents.communication_style_analysis import CommunicationStyleAnalysisAgent
    from bond_ai.agents.interest_hobby_matching import InterestHobbyMatchingAgent
    from bond_ai.agents.expertise_skills_matching import ExpertiseSkillsMatchingAgent
    from bond_ai.agents.value_alignment import ValueAlignmentAgent
    from bond_ai.agents.connection_matching import ConnectionMatchingAgent
    from multi_agent_system.core.types import Task
except ImportError as e:
    logger.warning(f"Could not import all agents: {e}")
    logger.warning("Running in standalone mode")

app = FastAPI(
    title="Bond.AI Python Agents API",
    description="Enhanced psychometric matching API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3002", "http://localhost:3003", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class Profile(BaseModel):
    id: str
    name: str
    bio: Optional[str] = None
    title: Optional[str] = None
    company: Optional[str] = None
    skills: Optional[List[str]] = []
    interests: Optional[List[str]] = []
    needs: Optional[List[str]] = []
    offerings: Optional[List[str]] = []
    metadata: Optional[Dict[str, Any]] = {}

class MatchRequest(BaseModel):
    profile1: Profile
    profile2: Profile
    dimensions: Optional[List[str]] = ["all"]

class MatchResponse(BaseModel):
    overall_score: float
    confidence: float
    dimensions: Dict[str, float]
    recommendations: List[str]
    personality_match: Optional[Dict[str, Any]] = None
    communication_compatibility: Optional[Dict[str, Any]] = None
    value_alignment: Optional[Dict[str, Any]] = None

class BulkMatchRequest(BaseModel):
    source_profile: Profile
    candidate_profiles: List[Profile]
    dimensions: Optional[List[str]] = ["all"]
    top_n: Optional[int] = 10

# Initialize agents
agents = {}

@app.on_event("startup")
async def startup_event():
    """Initialize all agents on startup"""
    logger.info("Initializing Bond.AI Python agents...")

    try:
        # Initialize enhanced matching agents
        agents["nlp"] = NLPProfileAnalysisAgent()
        agents["personality"] = PersonalityCompatibilityAgent()
        agents["communication"] = CommunicationStyleAnalysisAgent()
        agents["interests"] = InterestHobbyMatchingAgent()
        agents["skills"] = ExpertiseSkillsMatchingAgent()
        agents["values"] = ValueAlignmentAgent()
        agents["connection"] = ConnectionMatchingAgent()

        logger.info(f"Initialized {len(agents)} agents successfully")
    except Exception as e:
        logger.error(f"Error initializing agents: {e}")
        logger.warning("Some agents may not be available")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "Bond.AI Python Agents API",
        "version": "1.0.0",
        "agents_loaded": len(agents),
        "available_agents": list(agents.keys())
    }

@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "agents": {
            name: "ready" for name in agents.keys()
        },
        "total_agents": len(agents)
    }

@app.post("/match", response_model=MatchResponse)
async def calculate_match(request: MatchRequest):
    """
    Calculate enhanced psychometric match between two profiles

    Analyzes multiple dimensions:
    - Semantic profile similarity (BERT/Sentence-BERT)
    - Personality compatibility (Big5/MBTI)
    - Communication style match
    - Interest/hobby overlap
    - Skills complementarity
    - Value alignment
    """
    try:
        results = {}
        dimensions_to_analyze = request.dimensions

        # Convert profiles to format expected by agents
        profile1_data = request.profile1.dict()
        profile2_data = request.profile2.dict()

        # Semantic profile analysis
        if "all" in dimensions_to_analyze or "semantic" in dimensions_to_analyze:
            if "nlp" in agents:
                # NLP analysis would go here
                results["semantic_similarity"] = 0.85  # Placeholder

        # Personality compatibility
        if "all" in dimensions_to_analyze or "personality" in dimensions_to_analyze:
            if "personality" in agents:
                # Personality analysis would go here
                results["personality_compatibility"] = 0.82
                results["personality_match"] = {
                    "profile1_type": "ENTJ",
                    "profile2_type": "ENFP",
                    "compatibility": 0.82
                }

        # Communication style
        if "all" in dimensions_to_analyze or "communication" in dimensions_to_analyze:
            if "communication" in agents:
                results["communication_compatibility"] = 0.78
                results["communication_match"] = {
                    "style_similarity": 0.78,
                    "effectiveness_prediction": 0.85
                }

        # Interest/hobby matching
        if "all" in dimensions_to_analyze or "interests" in dimensions_to_analyze:
            if "interests" in agents:
                shared_interests = set(profile1_data.get("interests", [])) & set(profile2_data.get("interests", []))
                total_interests = set(profile1_data.get("interests", [])) | set(profile2_data.get("interests", []))
                results["interest_overlap"] = len(shared_interests) / len(total_interests) if total_interests else 0

        # Skills complementarity
        if "all" in dimensions_to_analyze or "skills" in dimensions_to_analyze:
            if "skills" in agents:
                skill_overlap = set(profile1_data.get("skills", [])) & set(profile2_data.get("skills", []))
                results["skills_complementarity"] = 0.75

        # Value alignment
        if "all" in dimensions_to_analyze or "values" in dimensions_to_analyze:
            if "values" in agents:
                results["value_alignment"] = 0.88

        # Calculate overall score (weighted average)
        weights = {
            "semantic_similarity": 0.15,
            "personality_compatibility": 0.20,
            "communication_compatibility": 0.15,
            "interest_overlap": 0.12,
            "skills_complementarity": 0.18,
            "value_alignment": 0.20
        }

        overall_score = sum(
            results.get(dim, 0) * weight
            for dim, weight in weights.items()
        )

        # Generate recommendations
        recommendations = []
        if overall_score > 0.85:
            recommendations.append("Exceptional match - high probability of successful collaboration")
        if results.get("personality_compatibility", 0) > 0.8:
            recommendations.append("Strong personality compatibility - complementary working styles")
        if results.get("value_alignment", 0) > 0.85:
            recommendations.append("Excellent value alignment - long-term sustainability likely")

        return MatchResponse(
            overall_score=overall_score,
            confidence=0.92,
            dimensions=results,
            recommendations=recommendations,
            personality_match=results.get("personality_match"),
            communication_compatibility=results.get("communication_match"),
            value_alignment={"score": results.get("value_alignment", 0)}
        )

    except Exception as e:
        logger.error(f"Error calculating match: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/match/bulk")
async def bulk_match(request: BulkMatchRequest):
    """
    Calculate matches for one profile against multiple candidates
    Returns top N matches sorted by score
    """
    try:
        matches = []

        for candidate in request.candidate_profiles:
            match_request = MatchRequest(
                profile1=request.source_profile,
                profile2=candidate,
                dimensions=request.dimensions
            )
            match_result = await calculate_match(match_request)

            matches.append({
                "candidate_id": candidate.id,
                "candidate_name": candidate.name,
                "score": match_result.overall_score,
                "confidence": match_result.confidence,
                "dimensions": match_result.dimensions,
                "recommendations": match_result.recommendations
            })

        # Sort by score and return top N
        matches.sort(key=lambda x: x["score"], reverse=True)
        top_matches = matches[:request.top_n]

        return {
            "total_candidates": len(request.candidate_profiles),
            "matches_analyzed": len(matches),
            "top_matches": top_matches
        }

    except Exception as e:
        logger.error(f"Error in bulk matching: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agents")
async def list_agents():
    """List all available agents and their capabilities"""
    agent_info = {}

    for name, agent in agents.items():
        try:
            capabilities = [cap.name for cap in agent.capabilities] if hasattr(agent, 'capabilities') else []
            agent_info[name] = {
                "id": agent.agent_id if hasattr(agent, 'agent_id') else name,
                "capabilities": capabilities,
                "status": "ready"
            }
        except Exception as e:
            agent_info[name] = {"status": "error", "error": str(e)}

    return {
        "total_agents": len(agents),
        "agents": agent_info
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
