"""Models for Document OS."""

from datetime import datetime
from typing import Dict, List, Optional, Any
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class Document(BaseModel):
    """Document entity."""
    id: UUID = Field(default_factory=uuid4)
    title: str
    content: str
    doc_type: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    entities: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class DocumentSearchResult(BaseModel):
    """Search result."""
    document: Document
    relevance_score: float
    highlighted_snippets: List[str]


class EntityGraph(BaseModel):
    """Entity relationship graph."""
    entities: List[Dict[str, Any]]
    relationships: List[Dict[str, Any]]
