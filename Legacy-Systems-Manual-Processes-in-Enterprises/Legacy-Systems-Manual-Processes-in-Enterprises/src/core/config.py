"""Configuration management for the Enterprise AI suite."""

from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    # Application
    app_name: str = "Enterprise AI Modernization Suite"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = True
    log_level: str = "INFO"

    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_workers: int = 4
    api_reload: bool = True

    # Database
    database_url: str = Field(
        default="postgresql+asyncpg://enterprise_user:enterprise_pass@localhost:5432/enterprise_ai"
    )
    database_pool_size: int = 20
    database_max_overflow: int = 10

    # Redis
    redis_url: str = "redis://localhost:6379/0"
    redis_max_connections: int = 50

    # Vector Database
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str = ""
    qdrant_collection_name: str = "enterprise_vectors"

    # Neo4j
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "enterprise_pass"

    # Elasticsearch
    elasticsearch_url: str = "http://localhost:9200"
    elasticsearch_index_prefix: str = "enterprise_ai"

    # MinIO
    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"
    minio_bucket: str = "enterprise-ai-storage"
    minio_secure: bool = False

    # RabbitMQ & Celery
    rabbitmq_url: str = "amqp://admin:admin@localhost:5672/"
    celery_broker_url: str = "amqp://admin:admin@localhost:5672/"
    celery_result_backend: str = "redis://localhost:6379/1"

    # Local LLM Configuration (FREE - No API keys needed!)
    ollama_url: str = "http://ollama:11434"
    ollama_model: str = "llama3.2:3b"  # Fast, efficient model
    ollama_embedding_model: str = "nomic-embed-text"  # Local embeddings

    # Legacy API support (optional - NOT REQUIRED)
    openai_api_key: str = ""
    openai_model: str = "gpt-4-turbo-preview"
    openai_embedding_model: str = "text-embedding-3-large"

    anthropic_api_key: str = ""
    anthropic_model: str = "claude-3-opus-20240229"

    cohere_api_key: str = ""
    huggingface_api_key: str = ""

    # LLM Mode: "local" (free) or "api" (requires keys)
    llm_mode: str = "local"

    # AI Configuration
    max_tokens: int = 4000
    temperature: float = 0.7
    ai_timeout: int = 300
    embedding_dimension: int = 1536

    # Security
    secret_key: str = "change-this-in-production"
    jwt_secret_key: str = "change-this-jwt-secret-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]

    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_per_minute: int = 60
    rate_limit_per_hour: int = 1000

    # Monitoring
    prometheus_enabled: bool = True
    prometheus_port: int = 9090
    grafana_enabled: bool = True
    jaeger_enabled: bool = True
    jaeger_agent_host: str = "localhost"
    jaeger_agent_port: int = 6831

    # Module Flags
    eaf_enabled: bool = True
    eaf_max_concurrent_agents: int = 10
    eaf_agent_timeout: int = 600

    migrator_enabled: bool = True
    process_miner_enabled: bool = True
    document_os_enabled: bool = True
    governance_enabled: bool = True
    company_brain_enabled: bool = True
    hitl_enabled: bool = True
    infra_orchestrator_enabled: bool = True
    agents_enabled: bool = True
    risk_radar_enabled: bool = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
