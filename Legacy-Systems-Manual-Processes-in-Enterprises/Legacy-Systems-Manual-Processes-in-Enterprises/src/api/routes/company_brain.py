"""API routes for Company Brain."""

from typing import List
from fastapi import APIRouter
from src.company_brain.models import KnowledgeNode, SearchQuery, SearchResult

router = APIRouter()


@router.post("/search", response_model=List[SearchResult])
async def search_knowledge(query: SearchQuery) -> List[SearchResult]:
    """Semantic knowledge search."""
    return []


@router.post("/knowledge", response_model=KnowledgeNode)
async def add_knowledge(node: KnowledgeNode) -> KnowledgeNode:
    """Add knowledge to the graph."""
    return node


@router.get("/health")
async def health_check() -> dict:
    """Health check."""
    return {"status": "healthy", "module": "company_brain"}
