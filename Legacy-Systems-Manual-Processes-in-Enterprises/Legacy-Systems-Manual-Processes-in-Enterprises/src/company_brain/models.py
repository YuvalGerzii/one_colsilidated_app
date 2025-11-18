"""Models for Company Brain."""

from typing import List, Dict, Any, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class KnowledgeNode(BaseModel):
    """Knowledge graph node."""
    id: UUID = Field(default_factory=uuid4)
    type: str
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    embeddings: Optional[List[float]] = None


class SearchQuery(BaseModel):
    """Semantic search query."""
    query: str
    context: Optional[str] = None
    limit: int = 10
    filters: Dict[str, Any] = Field(default_factory=dict)


class SearchResult(BaseModel):
    """Search result."""
    node: KnowledgeNode
    score: float
    context: str
