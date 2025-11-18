"""
RAG Engine with Self-Improving Learning

Core RAG (Retrieval-Augmented Generation) engine that:
- Processes and indexes documents
- Retrieves relevant context for queries
- Generates responses with citations
- Learns and improves from feedback using reinforcement learning
"""

import os
import uuid
import hashlib
import logging
import time
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime
import json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

logger = logging.getLogger(__name__)


class RAGEngine:
    """
    Self-improving RAG engine with reinforcement learning

    Features:
    - Document chunking and indexing
    - Hybrid search (vector + keyword)
    - Query expansion and rewriting
    - Response generation with citations
    - Feedback-based learning
    - RL policy for retrieval optimization
    """

    def __init__(self):
        self.collection_name = "rag_documents"
        self.chunk_size = int(os.getenv("RAG_CHUNK_SIZE", "512"))
        self.chunk_overlap = int(os.getenv("RAG_CHUNK_OVERLAP", "128"))
        self.top_k = int(os.getenv("RAG_TOP_K", "5"))
        self.learning_enabled = os.getenv("RAG_LEARNING_ENABLED", "true").lower() == "true"

        self._embedding_service = None
        self._vector_db = None
        self._llm_service = None
        self._rl_optimizer = None
        self._initialized = False

    async def initialize(self, db: AsyncSession):
        """Initialize all services"""
        if self._initialized:
            return

        from app.services.embedding_service import get_embedding_service
        from app.services.vector_db_service import get_vector_db_service

        # Initialize services
        self._embedding_service = await get_embedding_service()
        self._vector_db = await get_vector_db_service()

        # Create collection
        embedding_dim = self._embedding_service.get_embedding_dimension()
        await self._vector_db.create_collection(
            self.collection_name,
            vector_size=embedding_dim
        )

        # Initialize RL optimizer if learning is enabled
        if self.learning_enabled:
            from app.services.rl_optimizer import get_rl_optimizer
            self._rl_optimizer = await get_rl_optimizer(db)

        self._initialized = True
        logger.info("RAG Engine initialized")

    async def index_document(
        self,
        db: AsyncSession,
        content: str,
        title: str,
        source_type: str,
        source_id: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Index a document for RAG retrieval

        Args:
            db: Database session
            content: Document content
            title: Document title
            source_type: Type of source (pdf, property, etc.)
            source_id: Optional reference ID
            metadata: Additional metadata

        Returns:
            Indexing result with document_id and chunk_count
        """
        from app.models.rag_learning import RAGDocument, RAGDocumentChunk

        await self.initialize(db)

        # Create document record
        content_hash = hashlib.sha256(content.encode()).hexdigest()

        # Check for existing document with same hash
        existing = await db.execute(
            select(RAGDocument).where(RAGDocument.content_hash == content_hash)
        )
        existing_doc = existing.scalar_one_or_none()

        if existing_doc:
            logger.info(f"Document already indexed: {existing_doc.id}")
            return {
                "document_id": existing_doc.id,
                "chunk_count": existing_doc.chunk_count,
                "status": "already_indexed"
            }

        # Create new document
        document = RAGDocument(
            title=title,
            source_type=source_type,
            source_id=source_id,
            content=content,
            content_hash=content_hash,
            metadata=metadata or {},
            embedding_model=self._embedding_service.model_name
        )
        db.add(document)
        await db.flush()

        # Chunk the document
        chunks = self._chunk_text(content)

        # Generate embeddings for chunks
        chunk_texts = [c["text"] for c in chunks]
        embeddings = await self._embedding_service.embed_batch(chunk_texts)

        # Store chunks in database and vector DB
        vector_ids = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            vector_id = str(uuid.uuid4())

            # Create chunk record
            chunk_record = RAGDocumentChunk(
                document_id=document.id,
                content=chunk["text"],
                chunk_index=i,
                vector_id=vector_id,
                start_char=chunk["start"],
                end_char=chunk["end"],
                metadata={
                    "title": title,
                    "source_type": source_type,
                    "source_id": source_id
                }
            )
            db.add(chunk_record)
            vector_ids.append(vector_id)

        await db.flush()

        # Store in vector database
        vectors = []
        for i, (chunk, embedding, vector_id) in enumerate(zip(chunks, embeddings, vector_ids)):
            vectors.append({
                "id": vector_id,
                "vector": embedding,
                "payload": {
                    "document_id": document.id,
                    "chunk_index": i,
                    "content": chunk["text"],
                    "title": title,
                    "source_type": source_type,
                    "source_id": source_id
                }
            })

        await self._vector_db.upsert_vectors(self.collection_name, vectors)

        # Update document status
        document.is_indexed = True
        document.chunk_count = len(chunks)
        document.indexed_at = datetime.utcnow()

        await db.commit()

        logger.info(f"Indexed document {document.id} with {len(chunks)} chunks")

        return {
            "document_id": document.id,
            "chunk_count": len(chunks),
            "status": "indexed"
        }

    def _chunk_text(self, text: str) -> List[Dict[str, Any]]:
        """
        Split text into overlapping chunks

        Returns list of dicts with text, start, end positions
        """
        chunks = []
        words = text.split()

        if not words:
            return []

        # Estimate tokens (rough approximation)
        chars_per_token = 4
        chunk_chars = self.chunk_size * chars_per_token
        overlap_chars = self.chunk_overlap * chars_per_token

        start = 0
        while start < len(text):
            end = min(start + chunk_chars, len(text))

            # Find word boundary
            if end < len(text):
                # Look for space to break at
                while end > start and text[end] not in " \n\t":
                    end -= 1
                if end == start:
                    end = min(start + chunk_chars, len(text))

            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append({
                    "text": chunk_text,
                    "start": start,
                    "end": end
                })

            # Move start with overlap
            start = end - overlap_chars
            if start >= end:
                start = end

        return chunks

    async def query(
        self,
        db: AsyncSession,
        query: str,
        user_id: Optional[int] = None,
        session_id: Optional[str] = None,
        top_k: Optional[int] = None,
        include_sources: bool = True,
        generate_response: bool = True
    ) -> Dict[str, Any]:
        """
        Query the RAG system

        Args:
            db: Database session
            query: User query
            user_id: Optional user ID for personalization
            session_id: Session ID for context
            top_k: Number of results to retrieve
            include_sources: Include source documents in response
            generate_response: Generate LLM response

        Returns:
            Query result with response, sources, and metadata
        """
        from app.models.rag_learning import RAGQuery

        await self.initialize(db)

        start_time = time.time()
        top_k = top_k or self.top_k

        # Apply query expansion if learned rules exist
        expanded_query = await self._expand_query(db, query)

        # Get RL policy decision
        policy_action = "FETCH"
        policy_state = {}
        if self._rl_optimizer:
            state = self._build_state(query, session_id)
            policy_action, policy_state = await self._rl_optimizer.get_action(state)

        # Embed the query
        retrieval_start = time.time()
        query_embedding = await self._embedding_service.embed_text(expanded_query)

        # Search vector database
        if policy_action == "FETCH":
            results = await self._vector_db.hybrid_search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                keyword_query=query,
                top_k=top_k,
                alpha=0.7  # Favor semantic search
            )
        else:
            results = []

        retrieval_time = (time.time() - retrieval_start) * 1000

        # Extract retrieved chunks
        retrieved_chunks = []
        retrieved_chunk_ids = []
        retrieval_scores = []

        for result in results:
            payload = result.get("payload", {})
            retrieved_chunks.append({
                "content": payload.get("content", ""),
                "title": payload.get("title", ""),
                "source_type": payload.get("source_type", ""),
                "source_id": payload.get("source_id", ""),
                "score": result["score"]
            })
            retrieved_chunk_ids.append(int(payload.get("document_id", 0)))
            retrieval_scores.append(result["score"])

        # Generate response
        response = ""
        response_confidence = 0.0
        generation_time = 0.0

        if generate_response and retrieved_chunks:
            gen_start = time.time()
            response, response_confidence = await self._generate_response(
                query, retrieved_chunks
            )
            generation_time = (time.time() - gen_start) * 1000

        total_time = (time.time() - start_time) * 1000

        # Store query record for learning
        query_record = RAGQuery(
            user_id=user_id,
            session_id=session_id,
            original_query=query,
            expanded_query=expanded_query if expanded_query != query else None,
            retrieved_chunk_ids=retrieved_chunk_ids,
            retrieval_scores=retrieval_scores,
            generated_response=response,
            response_confidence=response_confidence,
            retrieval_time_ms=retrieval_time,
            generation_time_ms=generation_time,
            total_time_ms=total_time,
            policy_action=policy_action,
            policy_state=policy_state
        )
        db.add(query_record)
        await db.commit()

        # Build response
        result = {
            "query_id": query_record.id,
            "response": response,
            "confidence": response_confidence,
            "sources": retrieved_chunks if include_sources else [],
            "metrics": {
                "retrieval_time_ms": retrieval_time,
                "generation_time_ms": generation_time,
                "total_time_ms": total_time,
                "num_sources": len(retrieved_chunks)
            },
            "policy_action": policy_action
        }

        return result

    async def _expand_query(self, db: AsyncSession, query: str) -> str:
        """Apply learned query expansion rules"""
        from app.models.rag_learning import QueryRewriteRule

        # Check for matching rewrite rules
        result = await db.execute(
            select(QueryRewriteRule).where(
                QueryRewriteRule.is_active == True
            ).order_by(QueryRewriteRule.success_rate.desc()).limit(10)
        )
        rules = result.scalars().all()

        expanded = query
        for rule in rules:
            if rule.original_pattern.lower() in query.lower():
                expanded = query.replace(
                    rule.original_pattern,
                    rule.rewritten_pattern
                )
                # Update usage count
                await db.execute(
                    update(QueryRewriteRule)
                    .where(QueryRewriteRule.id == rule.id)
                    .values(usage_count=QueryRewriteRule.usage_count + 1)
                )
                break

        return expanded

    def _build_state(self, query: str, session_id: Optional[str]) -> Dict[str, Any]:
        """Build state representation for RL policy"""
        return {
            "query_length": len(query.split()),
            "has_session": session_id is not None,
            "query_type": self._classify_query(query)
        }

    def _classify_query(self, query: str) -> str:
        """Simple query classification"""
        query_lower = query.lower()
        if any(w in query_lower for w in ["what", "who", "when", "where", "why", "how"]):
            return "question"
        elif any(w in query_lower for w in ["find", "search", "show", "list"]):
            return "search"
        elif any(w in query_lower for w in ["calculate", "compute", "estimate"]):
            return "calculation"
        else:
            return "general"

    async def _generate_response(
        self,
        query: str,
        chunks: List[Dict]
    ) -> Tuple[str, float]:
        """Generate response using LLM with retrieved context"""
        try:
            import httpx

            # Build context from chunks
            context_parts = []
            for i, chunk in enumerate(chunks, 1):
                context_parts.append(f"[Source {i}: {chunk['title']}]\n{chunk['content']}")

            context = "\n\n".join(context_parts)

            # Build prompt
            prompt = f"""Based on the following context, answer the question.
If the answer is not in the context, say so clearly.
Always cite your sources using [Source N] format.

Context:
{context}

Question: {query}

Answer:"""

            # Call LLM
            ollama_url = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
            model = os.getenv("OLLAMA_MODEL", "gemma:2b")

            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{ollama_url}/api/generate",
                    json={
                        "model": model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.3,
                            "num_predict": 500
                        }
                    }
                )

                if response.status_code == 200:
                    data = response.json()
                    generated_text = data.get("response", "")

                    # Estimate confidence based on response characteristics
                    confidence = self._estimate_confidence(generated_text, chunks)

                    return generated_text, confidence
                else:
                    logger.error(f"LLM request failed: {response.status_code}")
                    return "Unable to generate response.", 0.0

        except Exception as e:
            logger.error(f"Response generation failed: {e}")
            return f"Error generating response: {str(e)}", 0.0

    def _estimate_confidence(self, response: str, chunks: List[Dict]) -> float:
        """Estimate response confidence"""
        confidence = 0.5  # Base confidence

        # Higher confidence if sources are cited
        if "[Source" in response:
            confidence += 0.2

        # Higher confidence if response is substantial
        if len(response.split()) > 50:
            confidence += 0.1

        # Higher confidence if retrieval scores are high
        if chunks:
            avg_score = sum(c["score"] for c in chunks) / len(chunks)
            confidence += avg_score * 0.2

        return min(confidence, 1.0)

    async def record_feedback(
        self,
        db: AsyncSession,
        query_id: int,
        feedback_type: str,
        rating: Optional[float] = None,
        is_helpful: Optional[bool] = None,
        correction: Optional[str] = None,
        relevant_sources: Optional[List[int]] = None,
        irrelevant_sources: Optional[List[int]] = None
    ) -> Dict[str, Any]:
        """
        Record feedback for a RAG query result

        This feedback is used to train the RL optimizer and improve retrieval.
        """
        from app.models.rag_learning import RAGFeedback, RAGQuery, FeedbackType

        # Get the query
        result = await db.execute(
            select(RAGQuery).where(RAGQuery.id == query_id)
        )
        query = result.scalar_one_or_none()

        if not query:
            return {"error": "Query not found"}

        # Compute reward for RL
        reward = self._compute_reward(
            feedback_type, rating, is_helpful
        )

        # Create feedback record
        feedback = RAGFeedback(
            query_id=query_id,
            feedback_type=FeedbackType(feedback_type),
            rating=rating,
            is_helpful=is_helpful,
            correction_text=correction,
            relevant_sources=relevant_sources or [],
            irrelevant_sources=irrelevant_sources or [],
            computed_reward=reward
        )
        db.add(feedback)

        # Update RL optimizer with feedback
        if self._rl_optimizer and self.learning_enabled:
            await self._rl_optimizer.update_policy(
                state=query.policy_state,
                action=query.policy_action,
                reward=reward,
                next_state=None  # Terminal state
            )

        await db.commit()

        return {
            "feedback_id": feedback.id,
            "reward": reward,
            "learning_updated": self.learning_enabled
        }

    def _compute_reward(
        self,
        feedback_type: str,
        rating: Optional[float],
        is_helpful: Optional[bool]
    ) -> float:
        """Compute reward for RL from feedback"""
        reward = 0.0

        if feedback_type == "thumbs_up":
            reward = 1.0
        elif feedback_type == "thumbs_down":
            reward = -1.0
        elif feedback_type == "rating" and rating is not None:
            # Normalize rating to [-1, 1]
            reward = (rating - 2.5) / 2.5
        elif is_helpful is not None:
            reward = 1.0 if is_helpful else -0.5

        return reward

    async def get_knowledge_gaps(self, db: AsyncSession) -> List[Dict[str, Any]]:
        """Identify knowledge gaps based on failed queries"""
        from app.models.rag_learning import KnowledgeGap

        result = await db.execute(
            select(KnowledgeGap)
            .where(KnowledgeGap.is_resolved == False)
            .order_by(KnowledgeGap.priority_score.desc())
            .limit(20)
        )
        gaps = result.scalars().all()

        return [
            {
                "id": gap.id,
                "topic": gap.topic,
                "description": gap.description,
                "priority": gap.priority_score,
                "frequency": gap.frequency,
                "first_detected": gap.first_detected_at.isoformat()
            }
            for gap in gaps
        ]

    async def get_stats(self, db: AsyncSession) -> Dict[str, Any]:
        """Get RAG engine statistics"""
        from app.models.rag_learning import (
            RAGDocument, RAGDocumentChunk, RAGQuery, RAGFeedback
        )
        from sqlalchemy import func

        # Count documents
        doc_count = await db.scalar(select(func.count(RAGDocument.id)))
        chunk_count = await db.scalar(select(func.count(RAGDocumentChunk.id)))
        query_count = await db.scalar(select(func.count(RAGQuery.id)))
        feedback_count = await db.scalar(select(func.count(RAGFeedback.id)))

        # Get collection info
        collection_info = await self._vector_db.get_collection_info(self.collection_name)

        return {
            "documents": doc_count,
            "chunks": chunk_count,
            "queries": query_count,
            "feedback_records": feedback_count,
            "vector_collection": collection_info,
            "learning_enabled": self.learning_enabled,
            "embedding_model": self._embedding_service.model_name if self._embedding_service else None
        }


# Global instance
_rag_engine: Optional[RAGEngine] = None


async def get_rag_engine() -> RAGEngine:
    """Get or create the global RAG engine instance"""
    global _rag_engine

    if _rag_engine is None:
        _rag_engine = RAGEngine()

    return _rag_engine
