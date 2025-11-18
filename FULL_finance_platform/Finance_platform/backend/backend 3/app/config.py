"""
Configuration Management for Portfolio Dashboard Backend

This module handles all application configuration using Pydantic Settings.
Environment variables are loaded from .env file.
"""

from typing import List, Optional
from pydantic import Field, field_validator, AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
import json


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # ================================
    # APPLICATION SETTINGS
    # ================================
    APP_NAME: str = "Portfolio Dashboard API"
    APP_VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    
    # ================================
    # SERVER CONFIGURATION
    # ================================
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True
    WORKERS: int = 4
    
    # ================================
    # DATABASE
    # ================================
    DATABASE_URL: str = Field(
        default="postgresql://portfolio_user:password@localhost:5432/portfolio_dashboard",
        description="PostgreSQL connection string"
    )
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 3600
    
    # ================================
    # REDIS
    # ================================
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_PASSWORD: Optional[str] = None
    
    # ================================
    # SECURITY
    # ================================
    SECRET_KEY: str = Field(
        default="your-secret-key-replace-in-production",
        description="Secret key for JWT encoding"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # ================================
    # FILE STORAGE
    # ================================
    UPLOAD_DIR: str = "./storage/uploads"
    GENERATED_MODELS_DIR: str = "./storage/generated_models"
    TEMPLATE_DIR: str = "./templates"
    MAX_UPLOAD_SIZE_MB: int = 50
    
    # AWS S3 (Optional)
    USE_S3: bool = False
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    S3_BUCKET_NAME: Optional[str] = None
    
    # ================================
    # PDF EXTRACTION
    # ================================
    OPENAI_API_KEY: Optional[str] = None
    USE_AI_EXTRACTION: bool = False
    EXTRACTION_CONFIDENCE_THRESHOLD: float = 0.85
    TESSERACT_PATH: str = "/usr/bin/tesseract"
    
    # ================================
    # EMAIL
    # ================================
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAIL_FROM: str = "noreply@portfoliodashboard.com"
    EMAIL_FROM_NAME: str = "Portfolio Dashboard"
    
    # ================================
    # CORS
    # ================================
    CORS_ORIGINS: str = '["http://localhost:3000","http://localhost:5173"]'
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: str = '["*"]'
    CORS_ALLOW_HEADERS: str = '["*"]'
    
    @field_validator("CORS_ORIGINS", "CORS_ALLOW_METHODS", "CORS_ALLOW_HEADERS", mode="before")
    @classmethod
    def parse_json_list(cls, v):
        """Parse JSON string to list."""
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [item.strip() for item in v.split(",")]
        return v
    
    # ================================
    # LOGGING
    # ================================
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    LOG_FILE_PATH: str = "./logs/app.log"
    
    # ================================
    # CELERY
    # ================================
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/1"
    
    # ================================
    # MONITORING
    # ================================
    SENTRY_DSN: Optional[str] = None
    ENABLE_METRICS: bool = False
    
    # ================================
    # EXTERNAL SERVICES
    # ================================
    BLOOMBERG_API_KEY: Optional[str] = None
    CAPIQ_USERNAME: Optional[str] = None
    CAPIQ_PASSWORD: Optional[str] = None
    FACTSET_USERNAME: Optional[str] = None
    FACTSET_API_KEY: Optional[str] = None
    
    # ================================
    # TESTING
    # ================================
    TEST_DATABASE_URL: Optional[str] = None
    
    # ================================
    # COMPUTED PROPERTIES
    # ================================
    @property
    def database_url_async(self) -> str:
        """Get async database URL (replace postgresql with postgresql+asyncpg)."""
        return self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.ENVIRONMENT.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.ENVIRONMENT.lower() == "development"
    
    @property
    def max_upload_size_bytes(self) -> int:
        """Get max upload size in bytes."""
        return self.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    
    def get_cors_origins(self) -> List[str]:
        """Get CORS origins as list."""
        if isinstance(self.CORS_ORIGINS, list):
            return self.CORS_ORIGINS
        return json.loads(self.CORS_ORIGINS)
    
    def model_post_init(self, __context):
        """Post-initialization validation and setup."""
        # Create directories if they don't exist
        import os
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)
        os.makedirs(self.GENERATED_MODELS_DIR, exist_ok=True)
        os.makedirs(os.path.dirname(self.LOG_FILE_PATH), exist_ok=True)


# Create global settings instance
settings = Settings()


# Export for easy importing
__all__ = ["settings", "Settings"]
