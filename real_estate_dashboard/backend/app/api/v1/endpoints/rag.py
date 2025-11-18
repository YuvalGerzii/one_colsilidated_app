"""
RAG (Retrieval-Augmented Generation) API Endpoints

Provides endpoints for:
- Document indexing and management
- RAG queries with context retrieval
- Feedback collection for learning
- Learning cycle management
- System statistics and monitoring
"""

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional
from loguru import logger

from app.models.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


# =============================================================================
# Request/Response Models
# =============================================================================

class IndexDocumentRequest(BaseModel):
    """Request to index a document"""
    title: str = Field(..., description="Document title")
    content: str = Field(..., description="Document content")
    source_type: str = Field(..., description="Source type: pdf, property, market_data, etc.")
    source_id: Optional[str] = Field(None, description="Reference ID to original entity")
    metadata: Optional[Dict[str, Any]] = Field(default={}, description="Additional metadata")
    tags: Optional[List[str]] = Field(default=[], description="Tags for filtering")


class IndexDocumentResponse(BaseModel):
    """Response from document indexing"""
    success: bool
    document_id: int
    chunk_count: int
    status: str
    message: str


class RAGQueryRequest(BaseModel):
    """Request for RAG query"""
    query: str = Field(..., description="User query")
    top_k: Optional[int] = Field(5, description="Number of results to retrieve")
    include_sources: Optional[bool] = Field(True, description="Include source documents")
    generate_response: Optional[bool] = Field(True, description="Generate LLM response")
    user_id: Optional[int] = Field(None, description="User ID for personalization")
    session_id: Optional[str] = Field(None, description="Session ID for context")


class RAGQueryResponse(BaseModel):
    """Response from RAG query"""
    success: bool
    query_id: int
    response: str
    confidence: float
    sources: List[Dict[str, Any]]
    metrics: Dict[str, Any]
    policy_action: str


class FeedbackRequest(BaseModel):
    """Request to submit feedback"""
    query_id: int = Field(..., description="Query ID to provide feedback for")
    feedback_type: str = Field(..., description="Type: thumbs_up, thumbs_down, rating, correction")
    rating: Optional[float] = Field(None, description="Rating 0-5")
    is_helpful: Optional[bool] = Field(None, description="Was the response helpful")
    correction: Optional[str] = Field(None, description="Correction text if response was wrong")
    relevant_sources: Optional[List[int]] = Field(default=[], description="IDs of relevant sources")
    irrelevant_sources: Optional[List[int]] = Field(default=[], description="IDs of irrelevant sources")


class FeedbackResponse(BaseModel):
    """Response from feedback submission"""
    success: bool
    feedback_id: int
    reward: float
    learning_updated: bool


class LearningCycleResponse(BaseModel):
    """Response from learning cycle"""
    success: bool
    knowledge_gaps: int
    new_patterns: int
    synthesized_knowledge: int
    feedback_stats: Dict[str, Any]


class RAGStatsResponse(BaseModel):
    """RAG system statistics"""
    success: bool
    documents: int
    chunks: int
    queries: int
    feedback_records: int
    vector_collection: Optional[Dict[str, Any]]
    learning_enabled: bool
    embedding_model: Optional[str]
    rl_stats: Optional[Dict[str, Any]]


# =============================================================================
# Document Management Endpoints
# =============================================================================

@router.post("/index", response_model=IndexDocumentResponse)
async def index_document(
    request: IndexDocumentRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Index a document for RAG retrieval.

    The document is:
    1. Chunked into overlapping segments
    2. Embedded using the configured embedding model
    3. Stored in the vector database

    Returns document ID and number of chunks created.
    """
    try:
        from app.services.rag_engine import get_rag_engine

        engine = await get_rag_engine()
        result = await engine.index_document(
            db=db,
            content=request.content,
            title=request.title,
            source_type=request.source_type,
            source_id=request.source_id,
            metadata=request.metadata
        )

        return IndexDocumentResponse(
            success=True,
            document_id=result["document_id"],
            chunk_count=result["chunk_count"],
            status=result["status"],
            message=f"Document indexed with {result['chunk_count']} chunks"
        )

    except Exception as e:
        logger.error(f"Document indexing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/index/file")
async def index_file(
    file: UploadFile = File(...),
    title: Optional[str] = None,
    source_type: str = "user_upload",
    db: AsyncSession = Depends(get_db)
):
    """
    Index a file (PDF, TXT, etc.) for RAG retrieval.

    Supports:
    - PDF files
    - Text files
    - Markdown files
    """
    try:
        from app.services.rag_engine import get_rag_engine

        # Read file content
        content = await file.read()

        # Determine file type and extract text
        filename = file.filename.lower()
        if filename.endswith('.pdf'):
            # Use PDF extraction service
            try:
                from app.services.pdf_extraction_service import extract_text_from_pdf
                text_content = await extract_text_from_pdf(content)
            except ImportError:
                text_content = content.decode('utf-8', errors='ignore')
        else:
            text_content = content.decode('utf-8', errors='ignore')

        # Index the document
        engine = await get_rag_engine()
        result = await engine.index_document(
            db=db,
            content=text_content,
            title=title or file.filename,
            source_type=source_type,
            metadata={"filename": file.filename, "content_type": file.content_type}
        )

        return {
            "success": True,
            "document_id": result["document_id"],
            "chunk_count": result["chunk_count"],
            "filename": file.filename
        }

    except Exception as e:
        logger.error(f"File indexing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/documents/{document_id}")
async def delete_document(
    document_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a document and its chunks from the RAG system.
    """
    try:
        from app.models.rag_learning import RAGDocument, RAGDocumentChunk
        from app.services.vector_db_service import get_vector_db_service
        from sqlalchemy import select, delete

        # Get document chunks
        result = await db.execute(
            select(RAGDocumentChunk).where(RAGDocumentChunk.document_id == document_id)
        )
        chunks = result.scalars().all()

        # Delete from vector DB
        if chunks:
            vector_db = await get_vector_db_service()
            vector_ids = [c.vector_id for c in chunks]
            await vector_db.delete_vectors("rag_documents", vector_ids)

        # Delete from database
        await db.execute(
            delete(RAGDocumentChunk).where(RAGDocumentChunk.document_id == document_id)
        )
        await db.execute(
            delete(RAGDocument).where(RAGDocument.id == document_id)
        )
        await db.commit()

        return {
            "success": True,
            "deleted_document_id": document_id,
            "deleted_chunks": len(chunks)
        }

    except Exception as e:
        logger.error(f"Document deletion error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# Query Endpoints
# =============================================================================

@router.post("/query", response_model=RAGQueryResponse)
async def query_rag(
    request: RAGQueryRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Query the RAG system.

    This endpoint:
    1. Expands the query using learned patterns
    2. Retrieves relevant documents using hybrid search
    3. Generates a response with citations
    4. Records the query for learning

    The RL optimizer decides the retrieval strategy based on learned policies.
    """
    try:
        from app.services.rag_engine import get_rag_engine

        engine = await get_rag_engine()
        result = await engine.query(
            db=db,
            query=request.query,
            user_id=request.user_id,
            session_id=request.session_id,
            top_k=request.top_k,
            include_sources=request.include_sources,
            generate_response=request.generate_response
        )

        return RAGQueryResponse(
            success=True,
            query_id=result["query_id"],
            response=result["response"],
            confidence=result["confidence"],
            sources=result["sources"],
            metrics=result["metrics"],
            policy_action=result["policy_action"]
        )

    except Exception as e:
        logger.error(f"RAG query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/similar")
async def find_similar(
    query: str,
    top_k: int = 5,
    db: AsyncSession = Depends(get_db)
):
    """
    Find similar documents without generating a response.

    Useful for document discovery and exploration.
    """
    try:
        from app.services.rag_engine import get_rag_engine

        engine = await get_rag_engine()
        result = await engine.query(
            db=db,
            query=query,
            top_k=top_k,
            include_sources=True,
            generate_response=False
        )

        return {
            "success": True,
            "query": query,
            "similar_documents": result["sources"],
            "metrics": result["metrics"]
        }

    except Exception as e:
        logger.error(f"Similar search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# Feedback and Learning Endpoints
# =============================================================================

@router.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(
    request: FeedbackRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Submit feedback for a RAG query result.

    Feedback is used to:
    1. Update RL policy for retrieval optimization
    2. Identify knowledge gaps
    3. Train query rewrite rules
    4. Calculate overall system performance
    """
    try:
        from app.services.rag_engine import get_rag_engine

        engine = await get_rag_engine()
        result = await engine.record_feedback(
            db=db,
            query_id=request.query_id,
            feedback_type=request.feedback_type,
            rating=request.rating,
            is_helpful=request.is_helpful,
            correction=request.correction,
            relevant_sources=request.relevant_sources,
            irrelevant_sources=request.irrelevant_sources
        )

        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])

        return FeedbackResponse(
            success=True,
            feedback_id=result["feedback_id"],
            reward=result["reward"],
            learning_updated=result["learning_updated"]
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Feedback submission error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/learning/cycle", response_model=LearningCycleResponse)
async def run_learning_cycle(
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Trigger a learning cycle.

    This runs:
    1. Knowledge gap detection
    2. Query pattern learning
    3. Knowledge synthesis
    4. Feedback aggregation

    Should be run periodically (e.g., daily).
    """
    try:
        from app.services.enhanced_learning_service import get_learning_service

        service = await get_learning_service()
        results = await service.run_learning_cycle(db)

        return LearningCycleResponse(
            success=True,
            knowledge_gaps=results["knowledge_gaps"],
            new_patterns=results["new_patterns"],
            synthesized_knowledge=results["synthesized_knowledge"],
            feedback_stats=results["feedback_stats"]
        )

    except Exception as e:
        logger.error(f"Learning cycle error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/learning/gaps")
async def get_knowledge_gaps(
    db: AsyncSession = Depends(get_db)
):
    """
    Get identified knowledge gaps.

    Knowledge gaps are topics where the system has low confidence or negative feedback.
    These should be addressed by adding more relevant documents.
    """
    try:
        from app.services.rag_engine import get_rag_engine

        engine = await get_rag_engine()
        gaps = await engine.get_knowledge_gaps(db)

        return {
            "success": True,
            "knowledge_gaps": gaps,
            "count": len(gaps)
        }

    except Exception as e:
        logger.error(f"Knowledge gaps error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/learning/train")
async def train_rl_policy(
    batch_size: int = 32,
    db: AsyncSession = Depends(get_db)
):
    """
    Trigger RL policy training on replay buffer.

    This updates the Q-table using experience replay for more stable learning.
    """
    try:
        from app.services.rl_optimizer import get_rl_optimizer

        optimizer = await get_rl_optimizer(db)
        await optimizer.batch_train(db, batch_size)
        await optimizer.save_policy(db)

        stats = optimizer.get_stats()

        return {
            "success": True,
            "message": f"Trained on batch of {batch_size}",
            "stats": stats
        }

    except Exception as e:
        logger.error(f"RL training error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# Statistics and Monitoring Endpoints
# =============================================================================

@router.get("/stats", response_model=RAGStatsResponse)
async def get_rag_stats(
    db: AsyncSession = Depends(get_db)
):
    """
    Get RAG system statistics.

    Returns counts of documents, chunks, queries, and feedback,
    plus RL optimizer statistics.
    """
    try:
        from app.services.rag_engine import get_rag_engine
        from app.services.rl_optimizer import get_rl_optimizer

        engine = await get_rag_engine()
        stats = await engine.get_stats(db)

        # Get RL stats
        optimizer = await get_rl_optimizer(db)
        rl_stats = optimizer.get_stats()

        return RAGStatsResponse(
            success=True,
            documents=stats["documents"],
            chunks=stats["chunks"],
            queries=stats["queries"],
            feedback_records=stats["feedback_records"],
            vector_collection=stats["vector_collection"],
            learning_enabled=stats["learning_enabled"],
            embedding_model=stats["embedding_model"],
            rl_stats=rl_stats
        )

    except Exception as e:
        logger.error(f"Stats error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def rag_health():
    """
    Health check for RAG system.
    """
    try:
        from app.services.embedding_service import get_embedding_service
        from app.services.vector_db_service import get_vector_db_service

        # Check embedding service
        embedding_service = await get_embedding_service()
        embedding_status = "healthy" if embedding_service else "unavailable"

        # Check vector DB
        vector_db = await get_vector_db_service()
        vector_status = "healthy" if vector_db else "unavailable"

        return {
            "status": "healthy",
            "services": {
                "embedding": embedding_status,
                "vector_db": vector_status
            }
        }

    except Exception as e:
        logger.error(f"Health check error: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }
