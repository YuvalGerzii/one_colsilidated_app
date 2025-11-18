"""API routes for Document OS."""

from typing import List
from fastapi import APIRouter, UploadFile
from src.document_os.models import Document, DocumentSearchResult, EntityGraph

router = APIRouter()


@router.post("/parse", response_model=Document)
async def parse_document(file: UploadFile) -> Document:
    """Parse and extract document structure."""
    return Document(
        title=file.filename or "Untitled",
        content="Parsed content",
        doc_type="pdf",
        metadata={"size": 0},
    )


@router.get("/search", response_model=List[DocumentSearchResult])
async def search_documents(query: str) -> List[DocumentSearchResult]:
    """Semantic document search."""
    return []


@router.get("/graph", response_model=EntityGraph)
async def get_entity_graph() -> EntityGraph:
    """Get entity relationship graph."""
    return EntityGraph(entities=[], relationships=[])


@router.get("/health")
async def health_check() -> dict:
    """Health check."""
    return {"status": "healthy", "module": "document_os"}
