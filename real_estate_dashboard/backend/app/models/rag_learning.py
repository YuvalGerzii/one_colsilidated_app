"""
RAG Learning and Self-Improving System Database Models

This module defines database models for:
- Document embeddings and vector storage metadata
- RAG query history and feedback
- Reinforcement learning states and policies
- Active learning and knowledge enhancement
"""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, JSON, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
import enum

from app.models.database import Base


class DocumentSourceType(str, enum.Enum):
    """Types of document sources for RAG"""
    PDF = "pdf"
    PROPERTY = "property"
    MARKET_DATA = "market_data"
    DEAL = "deal"
    FINANCIAL_MODEL = "financial_model"
    USER_UPLOAD = "user_upload"
    WEB_SCRAPE = "web_scrape"
    KNOWLEDGE_BASE = "knowledge_base"


class FeedbackType(str, enum.Enum):
    """Types of feedback for learning"""
    THUMBS_UP = "thumbs_up"
    THUMBS_DOWN = "thumbs_down"
    RATING = "rating"
    CORRECTION = "correction"
    IMPLICIT_CLICK = "implicit_click"
    IMPLICIT_DWELL = "implicit_dwell"


class LearningEventType(str, enum.Enum):
    """Types of learning events"""
    RETRIEVAL_SUCCESS = "retrieval_success"
    RETRIEVAL_FAILURE = "retrieval_failure"
    QUERY_REWRITE = "query_rewrite"
    KNOWLEDGE_UPDATE = "knowledge_update"
    POLICY_UPDATE = "policy_update"
    EMBEDDING_REFRESH = "embedding_refresh"


# =============================================================================
# Document and Embedding Models
# =============================================================================

class RAGDocument(Base):
    """Store document metadata for RAG indexing"""
    __tablename__ = "rag_documents"

    id = Column(Integer, primary_key=True, index=True)

    # Document identification
    title = Column(String(500), nullable=False)
    source_type = Column(SQLEnum(DocumentSourceType), nullable=False)
    source_id = Column(String(100), nullable=True)  # Reference to original entity

    # Content
    content = Column(Text, nullable=False)
    content_hash = Column(String(64), nullable=False, index=True)  # SHA256 hash

    # Metadata
    metadata = Column(JSON, default={})
    tags = Column(ARRAY(String), default=[])
    language = Column(String(10), default="en")

    # Processing status
    is_indexed = Column(Boolean, default=False)
    chunk_count = Column(Integer, default=0)
    embedding_model = Column(String(100), nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    indexed_at = Column(DateTime, nullable=True)

    # Relationships
    chunks = relationship("RAGDocumentChunk", back_populates="document", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<RAGDocument(id={self.id}, title={self.title}, source_type={self.source_type})>"


class RAGDocumentChunk(Base):
    """Store document chunks with embedding references"""
    __tablename__ = "rag_document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("rag_documents.id"), nullable=False)

    # Chunk content
    content = Column(Text, nullable=False)
    chunk_index = Column(Integer, nullable=False)

    # Vector reference (stored in Qdrant)
    vector_id = Column(String(100), nullable=False, unique=True, index=True)

    # Position in original document
    start_char = Column(Integer, nullable=True)
    end_char = Column(Integer, nullable=True)

    # Metadata
    metadata = Column(JSON, default={})

    # Quality metrics
    retrieval_count = Column(Integer, default=0)
    avg_relevance_score = Column(Float, default=0.0)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    document = relationship("RAGDocument", back_populates="chunks")

    def __repr__(self):
        return f"<RAGDocumentChunk(id={self.id}, document_id={self.document_id}, chunk_index={self.chunk_index})>"


# =============================================================================
# Query and Retrieval Models
# =============================================================================

class RAGQuery(Base):
    """Store RAG query history for learning"""
    __tablename__ = "rag_queries"

    id = Column(Integer, primary_key=True, index=True)

    # Query details
    user_id = Column(Integer, nullable=True)
    session_id = Column(String(100), nullable=True)
    original_query = Column(Text, nullable=False)
    expanded_query = Column(Text, nullable=True)  # After query expansion

    # Query embedding reference
    query_vector_id = Column(String(100), nullable=True)

    # Retrieval results
    retrieved_chunk_ids = Column(ARRAY(Integer), default=[])
    retrieval_scores = Column(ARRAY(Float), default=[])

    # Generated response
    generated_response = Column(Text, nullable=True)
    response_confidence = Column(Float, nullable=True)
    sources_cited = Column(JSON, default=[])

    # Performance metrics
    retrieval_time_ms = Column(Float, nullable=True)
    generation_time_ms = Column(Float, nullable=True)
    total_time_ms = Column(Float, nullable=True)

    # RL policy decision
    policy_action = Column(String(50), nullable=True)  # FETCH, NO_FETCH, etc.
    policy_state = Column(JSON, default={})

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    feedback = relationship("RAGFeedback", back_populates="query", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<RAGQuery(id={self.id}, query={self.original_query[:50]}...)>"


class RAGFeedback(Base):
    """Store feedback for RAG responses"""
    __tablename__ = "rag_feedback"

    id = Column(Integer, primary_key=True, index=True)
    query_id = Column(Integer, ForeignKey("rag_queries.id"), nullable=False)

    # Feedback details
    feedback_type = Column(SQLEnum(FeedbackType), nullable=False)
    rating = Column(Float, nullable=True)  # 0-5 scale

    # Explicit feedback
    is_helpful = Column(Boolean, nullable=True)
    correction_text = Column(Text, nullable=True)

    # Implicit signals
    click_through = Column(Boolean, default=False)
    dwell_time_seconds = Column(Float, nullable=True)
    reformulated_query = Column(Text, nullable=True)

    # Source-level feedback
    relevant_sources = Column(ARRAY(Integer), default=[])
    irrelevant_sources = Column(ARRAY(Integer), default=[])

    # Computed reward for RL
    computed_reward = Column(Float, nullable=True)

    # User context
    user_id = Column(Integer, nullable=True)
    user_expertise_level = Column(String(20), nullable=True)  # novice, intermediate, expert

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    query = relationship("RAGQuery", back_populates="feedback")

    def __repr__(self):
        return f"<RAGFeedback(id={self.id}, query_id={self.query_id}, type={self.feedback_type})>"


# =============================================================================
# Reinforcement Learning Models
# =============================================================================

class RLPolicy(Base):
    """Store RL policy parameters and states"""
    __tablename__ = "rl_policies"

    id = Column(Integer, primary_key=True, index=True)

    # Policy identification
    policy_name = Column(String(100), nullable=False, unique=True)
    policy_type = Column(String(50), nullable=False)  # q_learning, policy_gradient, ppo

    # Policy parameters
    parameters = Column(JSON, nullable=False, default={})
    hyperparameters = Column(JSON, default={})

    # State
    is_active = Column(Boolean, default=True)
    version = Column(Integer, default=1)

    # Performance metrics
    avg_reward = Column(Float, default=0.0)
    total_episodes = Column(Integer, default=0)
    total_steps = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    episodes = relationship("RLEpisode", back_populates="policy", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<RLPolicy(id={self.id}, name={self.policy_name}, type={self.policy_type})>"


class RLEpisode(Base):
    """Store RL training episodes"""
    __tablename__ = "rl_episodes"

    id = Column(Integer, primary_key=True, index=True)
    policy_id = Column(Integer, ForeignKey("rl_policies.id"), nullable=False)

    # Episode details
    episode_number = Column(Integer, nullable=False)

    # States and actions
    states = Column(JSON, default=[])
    actions = Column(JSON, default=[])
    rewards = Column(ARRAY(Float), default=[])

    # Episode metrics
    total_reward = Column(Float, default=0.0)
    steps = Column(Integer, default=0)

    # Timestamps
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    policy = relationship("RLPolicy", back_populates="episodes")

    def __repr__(self):
        return f"<RLEpisode(id={self.id}, policy_id={self.policy_id}, episode={self.episode_number})>"


class RLStateAction(Base):
    """Store individual state-action pairs for fine-grained learning"""
    __tablename__ = "rl_state_actions"

    id = Column(Integer, primary_key=True, index=True)

    # Context
    query_id = Column(Integer, ForeignKey("rag_queries.id"), nullable=True)
    episode_id = Column(Integer, ForeignKey("rl_episodes.id"), nullable=True)

    # State representation
    state_features = Column(JSON, nullable=False)

    # Action taken
    action = Column(String(50), nullable=False)
    action_params = Column(JSON, default={})

    # Outcome
    reward = Column(Float, nullable=False)
    next_state_features = Column(JSON, nullable=True)
    is_terminal = Column(Boolean, default=False)

    # Q-value (for Q-learning)
    q_value = Column(Float, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<RLStateAction(id={self.id}, action={self.action}, reward={self.reward})>"


# =============================================================================
# Active Learning and Knowledge Enhancement
# =============================================================================

class LearningEvent(Base):
    """Track all learning events in the system"""
    __tablename__ = "learning_events"

    id = Column(Integer, primary_key=True, index=True)

    # Event details
    event_type = Column(SQLEnum(LearningEventType), nullable=False)
    description = Column(Text, nullable=True)

    # Related entities
    query_id = Column(Integer, nullable=True)
    document_id = Column(Integer, nullable=True)
    chunk_id = Column(Integer, nullable=True)

    # Event data
    event_data = Column(JSON, default={})

    # Impact metrics
    improvement_score = Column(Float, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<LearningEvent(id={self.id}, type={self.event_type})>"


class KnowledgeGap(Base):
    """Track identified knowledge gaps for active learning"""
    __tablename__ = "knowledge_gaps"

    id = Column(Integer, primary_key=True, index=True)

    # Gap identification
    topic = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)

    # Evidence
    failed_query_ids = Column(ARRAY(Integer), default=[])
    low_confidence_count = Column(Integer, default=0)

    # Priority
    priority_score = Column(Float, default=0.0)
    frequency = Column(Integer, default=1)

    # Resolution
    is_resolved = Column(Boolean, default=False)
    resolution_document_id = Column(Integer, nullable=True)

    # Timestamps
    first_detected_at = Column(DateTime, default=datetime.utcnow)
    last_detected_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<KnowledgeGap(id={self.id}, topic={self.topic}, priority={self.priority_score})>"


class EnhancedKnowledge(Base):
    """Store enhanced/synthesized knowledge from learning"""
    __tablename__ = "enhanced_knowledge"

    id = Column(Integer, primary_key=True, index=True)

    # Knowledge content
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)

    # Source documents
    source_document_ids = Column(ARRAY(Integer), default=[])

    # Quality metrics
    confidence_score = Column(Float, default=0.0)
    usage_count = Column(Integer, default=0)
    avg_feedback_score = Column(Float, default=0.0)

    # Metadata
    tags = Column(ARRAY(String), default=[])
    metadata = Column(JSON, default={})

    # Vector reference
    vector_id = Column(String(100), nullable=True)

    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<EnhancedKnowledge(id={self.id}, title={self.title})>"


class QueryRewriteRule(Base):
    """Store learned query rewrite rules"""
    __tablename__ = "query_rewrite_rules"

    id = Column(Integer, primary_key=True, index=True)

    # Rule pattern
    original_pattern = Column(String(500), nullable=False)
    rewritten_pattern = Column(String(500), nullable=False)

    # Rule type
    rule_type = Column(String(50), nullable=False)  # synonym, expansion, correction

    # Performance
    success_rate = Column(Float, default=0.0)
    usage_count = Column(Integer, default=0)

    # Status
    is_active = Column(Boolean, default=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<QueryRewriteRule(id={self.id}, pattern={self.original_pattern})>"


class SemanticCache(Base):
    """Cache for frequently asked queries with semantic matching"""
    __tablename__ = "semantic_cache"

    id = Column(Integer, primary_key=True, index=True)

    # Query
    query_text = Column(Text, nullable=False)
    query_vector_id = Column(String(100), nullable=True)

    # Cached response
    cached_response = Column(Text, nullable=False)
    source_chunks = Column(ARRAY(Integer), default=[])

    # Cache metrics
    hit_count = Column(Integer, default=0)
    avg_similarity = Column(Float, default=0.0)

    # Validity
    is_valid = Column(Boolean, default=True)
    expires_at = Column(DateTime, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    last_hit_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<SemanticCache(id={self.id}, hits={self.hit_count})>"
