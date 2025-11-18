"""
Enhanced Learning Service for RAG System

Implements advanced learning mechanisms:
- Active learning for identifying knowledge gaps
- Continuous knowledge enhancement
- Query pattern learning
- Feedback-driven optimization
"""

import os
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from collections import Counter
import re

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func, and_, or_

logger = logging.getLogger(__name__)


class EnhancedLearningService:
    """
    Advanced learning service for RAG improvement

    Features:
    - Knowledge gap detection
    - Active learning recommendations
    - Query pattern analysis
    - Automatic knowledge synthesis
    - Feedback aggregation
    """

    def __init__(self):
        self.min_confidence_threshold = 0.4
        self.gap_detection_window_days = 7
        self.pattern_min_frequency = 3

    async def detect_knowledge_gaps(
        self,
        db: AsyncSession,
        days: int = 7
    ) -> List[Dict[str, Any]]:
        """
        Analyze recent queries to identify knowledge gaps

        Knowledge gaps are identified by:
        - Low confidence responses
        - Negative feedback
        - Queries with no retrieval results
        - Repeated similar failed queries
        """
        from app.models.rag_learning import (
            RAGQuery, RAGFeedback, KnowledgeGap, LearningEvent, LearningEventType
        )

        cutoff = datetime.utcnow() - timedelta(days=days)

        # Find low confidence queries
        result = await db.execute(
            select(RAGQuery)
            .where(
                and_(
                    RAGQuery.created_at >= cutoff,
                    or_(
                        RAGQuery.response_confidence < self.min_confidence_threshold,
                        RAGQuery.retrieved_chunk_ids == []
                    )
                )
            )
        )
        low_confidence_queries = result.scalars().all()

        # Find queries with negative feedback
        result = await db.execute(
            select(RAGQuery)
            .join(RAGFeedback)
            .where(
                and_(
                    RAGQuery.created_at >= cutoff,
                    or_(
                        RAGFeedback.is_helpful == False,
                        RAGFeedback.rating < 2.0
                    )
                )
            )
        )
        negative_feedback_queries = result.scalars().all()

        # Combine and analyze
        all_problematic = set(
            [q.id for q in low_confidence_queries] +
            [q.id for q in negative_feedback_queries]
        )

        # Extract topics from problematic queries
        topic_counts = Counter()
        query_texts = {}

        for q in low_confidence_queries + negative_feedback_queries:
            topics = self._extract_topics(q.original_query)
            for topic in topics:
                topic_counts[topic] += 1
                if topic not in query_texts:
                    query_texts[topic] = []
                query_texts[topic].append(q.id)

        # Create or update knowledge gaps
        gaps = []
        for topic, count in topic_counts.most_common(20):
            if count >= 2:  # At least 2 occurrences
                # Check if gap already exists
                result = await db.execute(
                    select(KnowledgeGap)
                    .where(
                        and_(
                            KnowledgeGap.topic == topic,
                            KnowledgeGap.is_resolved == False
                        )
                    )
                )
                existing_gap = result.scalar_one_or_none()

                if existing_gap:
                    # Update existing
                    existing_gap.frequency += count
                    existing_gap.low_confidence_count += count
                    existing_gap.last_detected_at = datetime.utcnow()
                    existing_gap.priority_score = self._calculate_priority(
                        existing_gap.frequency,
                        existing_gap.low_confidence_count
                    )
                    existing_gap.failed_query_ids = list(set(
                        existing_gap.failed_query_ids + query_texts[topic]
                    ))
                else:
                    # Create new gap
                    gap = KnowledgeGap(
                        topic=topic,
                        description=f"Detected from {count} low-confidence queries",
                        failed_query_ids=query_texts[topic],
                        low_confidence_count=count,
                        frequency=count,
                        priority_score=self._calculate_priority(count, count)
                    )
                    db.add(gap)

                gaps.append({
                    "topic": topic,
                    "frequency": count,
                    "query_ids": query_texts[topic]
                })

        # Log learning event
        event = LearningEvent(
            event_type=LearningEventType.RETRIEVAL_FAILURE,
            description=f"Detected {len(gaps)} knowledge gaps",
            event_data={
                "gaps": gaps,
                "total_problematic_queries": len(all_problematic)
            }
        )
        db.add(event)

        await db.commit()

        logger.info(f"Detected {len(gaps)} knowledge gaps from {len(all_problematic)} queries")

        return gaps

    def _extract_topics(self, query: str) -> List[str]:
        """Extract key topics from query"""
        # Simple keyword extraction
        # Remove common words and extract meaningful terms
        stop_words = {
            "the", "a", "an", "is", "are", "was", "were", "be", "been",
            "being", "have", "has", "had", "do", "does", "did", "will",
            "would", "could", "should", "what", "which", "who", "when",
            "where", "why", "how", "can", "may", "might", "must", "shall",
            "i", "you", "he", "she", "it", "we", "they", "this", "that",
            "these", "those", "am", "of", "in", "to", "for", "with", "on",
            "at", "by", "from", "as", "into", "about", "like", "through",
            "after", "over", "between", "out", "against", "during", "without",
            "before", "under", "around", "among", "me", "my", "your", "our"
        }

        # Tokenize and filter
        words = re.findall(r'\b[a-zA-Z]{3,}\b', query.lower())
        topics = [w for w in words if w not in stop_words]

        # Also extract bigrams
        bigrams = []
        for i in range(len(words) - 1):
            if words[i] not in stop_words and words[i+1] not in stop_words:
                bigrams.append(f"{words[i]} {words[i+1]}")

        return topics + bigrams[:3]

    def _calculate_priority(self, frequency: int, low_confidence: int) -> float:
        """Calculate gap priority score"""
        # Simple scoring: frequency * 0.6 + low_confidence * 0.4
        return (frequency * 0.6 + low_confidence * 0.4) / 10.0

    async def learn_query_patterns(
        self,
        db: AsyncSession,
        min_occurrences: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Learn patterns from successful queries

        Creates query rewrite rules based on successful patterns.
        """
        from app.models.rag_learning import (
            RAGQuery, RAGFeedback, QueryRewriteRule, LearningEvent, LearningEventType
        )

        # Find successful queries (high confidence, positive feedback)
        result = await db.execute(
            select(RAGQuery)
            .outerjoin(RAGFeedback)
            .where(
                or_(
                    RAGQuery.response_confidence >= 0.7,
                    RAGFeedback.is_helpful == True,
                    RAGFeedback.rating >= 4.0
                )
            )
            .order_by(RAGQuery.created_at.desc())
            .limit(1000)
        )
        successful_queries = result.scalars().all()

        # Analyze patterns
        patterns = []
        query_pairs = []

        for q in successful_queries:
            if q.expanded_query and q.expanded_query != q.original_query:
                # Successful expansion - learn this pattern
                query_pairs.append({
                    "original": q.original_query,
                    "expanded": q.expanded_query
                })

        # Group similar patterns
        pattern_counts = Counter()
        for pair in query_pairs:
            # Simplified pattern extraction
            pattern_key = (
                pair["original"].lower().split()[0] if pair["original"] else "",
                pair["expanded"].lower().split()[0] if pair["expanded"] else ""
            )
            pattern_counts[pattern_key] += 1

        # Create rules from frequent patterns
        new_rules = []
        for pattern, count in pattern_counts.most_common(10):
            if count >= min_occurrences:
                # Check if rule exists
                result = await db.execute(
                    select(QueryRewriteRule)
                    .where(QueryRewriteRule.original_pattern == pattern[0])
                )
                existing = result.scalar_one_or_none()

                if not existing:
                    rule = QueryRewriteRule(
                        original_pattern=pattern[0],
                        rewritten_pattern=pattern[1],
                        rule_type="expansion",
                        success_rate=0.8,  # Initial estimate
                        usage_count=count
                    )
                    db.add(rule)
                    new_rules.append({
                        "original": pattern[0],
                        "rewritten": pattern[1],
                        "frequency": count
                    })

        # Log learning event
        if new_rules:
            event = LearningEvent(
                event_type=LearningEventType.QUERY_REWRITE,
                description=f"Learned {len(new_rules)} query rewrite rules",
                event_data={"rules": new_rules}
            )
            db.add(event)

        await db.commit()

        logger.info(f"Learned {len(new_rules)} new query rewrite rules")

        return new_rules

    async def synthesize_knowledge(
        self,
        db: AsyncSession
    ) -> List[Dict[str, Any]]:
        """
        Synthesize new knowledge from multiple successful retrievals

        Combines frequently co-retrieved chunks to create enhanced knowledge.
        """
        from app.models.rag_learning import (
            RAGQuery, RAGDocumentChunk, EnhancedKnowledge, LearningEvent, LearningEventType
        )

        # Find frequently co-retrieved chunk pairs
        result = await db.execute(
            select(RAGQuery)
            .where(
                and_(
                    RAGQuery.response_confidence >= 0.6,
                    func.array_length(RAGQuery.retrieved_chunk_ids, 1) >= 2
                )
            )
            .limit(500)
        )
        queries = result.scalars().all()

        # Count co-occurrences
        cooccurrence = Counter()
        for q in queries:
            chunk_ids = q.retrieved_chunk_ids
            for i in range(len(chunk_ids)):
                for j in range(i + 1, len(chunk_ids)):
                    pair = tuple(sorted([chunk_ids[i], chunk_ids[j]]))
                    cooccurrence[pair] += 1

        # Synthesize from frequent pairs
        synthesized = []
        for pair, count in cooccurrence.most_common(10):
            if count >= 5:  # At least 5 co-occurrences
                # Get chunks
                result = await db.execute(
                    select(RAGDocumentChunk)
                    .where(RAGDocumentChunk.id.in_(pair))
                )
                chunks = result.scalars().all()

                if len(chunks) == 2:
                    # Create enhanced knowledge
                    combined_content = f"""
## Combined Knowledge

### Source 1
{chunks[0].content}

### Source 2
{chunks[1].content}

### Key Points
- These sources are frequently used together
- Co-occurrence count: {count}
                    """.strip()

                    enhanced = EnhancedKnowledge(
                        title=f"Synthesized: {chunks[0].metadata.get('title', 'Unknown')} + {chunks[1].metadata.get('title', 'Unknown')}",
                        content=combined_content,
                        source_document_ids=[chunks[0].document_id, chunks[1].document_id],
                        confidence_score=min(chunks[0].avg_relevance_score, chunks[1].avg_relevance_score),
                        tags=["synthesized", "co-occurrence"]
                    )
                    db.add(enhanced)

                    synthesized.append({
                        "chunk_ids": list(pair),
                        "co_occurrence": count
                    })

        # Log event
        if synthesized:
            event = LearningEvent(
                event_type=LearningEventType.KNOWLEDGE_UPDATE,
                description=f"Synthesized {len(synthesized)} enhanced knowledge entries",
                event_data={"synthesized": synthesized}
            )
            db.add(event)

        await db.commit()

        logger.info(f"Synthesized {len(synthesized)} enhanced knowledge entries")

        return synthesized

    async def aggregate_feedback(
        self,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """
        Aggregate feedback to derive insights

        Computes:
        - Overall satisfaction metrics
        - Source quality scores
        - Query type performance
        """
        from app.models.rag_learning import RAGQuery, RAGFeedback, RAGDocumentChunk
        from sqlalchemy import func

        # Get feedback statistics
        result = await db.execute(
            select(
                func.count(RAGFeedback.id).label("total"),
                func.avg(RAGFeedback.rating).label("avg_rating"),
                func.sum(
                    func.cast(RAGFeedback.is_helpful == True, Integer)
                ).label("helpful_count")
            )
            .select_from(RAGFeedback)
        )
        stats = result.first()

        # Get source performance
        result = await db.execute(
            select(
                RAGDocumentChunk.id,
                func.avg(RAGDocumentChunk.avg_relevance_score).label("avg_score"),
                func.sum(RAGDocumentChunk.retrieval_count).label("total_retrievals")
            )
            .group_by(RAGDocumentChunk.id)
            .having(RAGDocumentChunk.retrieval_count > 0)
            .order_by(func.avg(RAGDocumentChunk.avg_relevance_score).desc())
            .limit(10)
        )
        top_sources = result.all()

        return {
            "total_feedback": stats.total if stats else 0,
            "average_rating": float(stats.avg_rating) if stats and stats.avg_rating else 0.0,
            "helpful_percentage": (
                (stats.helpful_count / stats.total * 100)
                if stats and stats.total > 0 else 0.0
            ),
            "top_sources": [
                {
                    "chunk_id": s.id,
                    "avg_score": float(s.avg_score),
                    "retrievals": s.total_retrievals
                }
                for s in top_sources
            ]
        }

    async def run_learning_cycle(self, db: AsyncSession) -> Dict[str, Any]:
        """
        Run a complete learning cycle

        This should be called periodically (e.g., daily) to update the system.
        """
        results = {}

        # 1. Detect knowledge gaps
        gaps = await self.detect_knowledge_gaps(db)
        results["knowledge_gaps"] = len(gaps)

        # 2. Learn query patterns
        patterns = await self.learn_query_patterns(db)
        results["new_patterns"] = len(patterns)

        # 3. Synthesize knowledge
        synthesized = await self.synthesize_knowledge(db)
        results["synthesized_knowledge"] = len(synthesized)

        # 4. Aggregate feedback
        feedback_stats = await self.aggregate_feedback(db)
        results["feedback_stats"] = feedback_stats

        logger.info(f"Learning cycle complete: {results}")

        return results


# Import Integer for SQL cast
from sqlalchemy import Integer


# Global instance
_learning_service: Optional[EnhancedLearningService] = None


async def get_learning_service() -> EnhancedLearningService:
    """Get or create the global learning service instance"""
    global _learning_service

    if _learning_service is None:
        _learning_service = EnhancedLearningService()

    return _learning_service
