"""
Configuration Management for Portfolio Dashboard Backend

This module handles all application configuration using Pydantic Settings.
Environment variables are loaded from .env file.
"""

from typing import List, Optional, Union
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
    # CACHE CONFIGURATION
    # ================================
    ENABLE_REDIS_CACHE: bool = True  # Enable Redis for persistent caching
    CACHE_DEFAULT_TTL: int = 1800  # 30 minutes default TTL
    CACHE_MARKET_DATA_TTL: int = 3600  # 1 hour for market data
    CACHE_INTEGRATION_STATUS_TTL: int = 300  # 5 minutes for integration health
    CACHE_API_RESPONSE_TTL: int = 1800  # 30 minutes for API responses
    CACHE_STATIC_DATA_TTL: int = 86400  # 24 hours for static data
    CACHE_ECONOMIC_INDICATORS_TTL: int = 3600  # 1 hour for economic data
    CACHE_REAL_ESTATE_DATA_TTL: int = 3600  # 1 hour for real estate market data

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
    CORS_ORIGINS: Union[str, List[str]] = '["http://localhost:3000","http://localhost:3001","http://localhost:5173"]'
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: Union[str, List[str]] = '["*"]'
    CORS_ALLOW_HEADERS: Union[str, List[str]] = '["*"]'

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

    # Economics API (Sugra AI)
    ECONOMICS_API_BASE_URL: str = "https://api.sugra.ai"
    ECONOMICS_API_KEY: Optional[str] = None
    ENABLE_ECONOMICS_API: bool = True

    # ================================
    # THIRD-PARTY INTEGRATIONS
    # ================================
    # Market Data (FREE)
    CENSUS_API_KEY: Optional[str] = None  # Optional but recommended
    BLS_API_KEY: Optional[str] = None  # Optional, increases rate limits
    FRED_API_KEY: Optional[str] = None  # Free - required for FRED
    HUD_API_KEY: Optional[str] = None  # Free - requires registration at huduser.gov

    # Property Data (Paid/Limited Free)
    ATTOM_API_KEY: Optional[str] = None  # Paid service
    REALTOR_RAPIDAPI_KEY: Optional[str] = None  # RapidAPI key for Realtor.com

    # Banking & Payments
    PLAID_CLIENT_ID: Optional[str] = None  # Free sandbox
    PLAID_SECRET: Optional[str] = None
    PLAID_ENVIRONMENT: str = "sandbox"  # sandbox, development, production

    STRIPE_API_KEY: Optional[str] = None  # Free test mode

    # Tools & Automation (FREE)
    SLACK_BOT_TOKEN: Optional[str] = None  # Free
    GOOGLE_DRIVE_ACCESS_TOKEN: Optional[str] = None  # Free (15GB)

    # Integration Feature Flags
    ENABLE_INTEGRATIONS: bool = True
    ENABLE_CENSUS_INTEGRATION: bool = False  # Temporarily disabled due to API errors
    ENABLE_BLS_INTEGRATION: bool = True
    ENABLE_FRED_INTEGRATION: bool = True  # ✅ ENABLED - API key configured
    ENABLE_ATTOM_INTEGRATION: bool = False  # DISABLED - paid service, no API key
    ENABLE_REALTOR_INTEGRATION: bool = False  # DISABLED - requires API key
    ENABLE_PLAID_INTEGRATION: bool = False  # DISABLED - requires API key
    ENABLE_STRIPE_INTEGRATION: bool = False  # DISABLED - requires API key
    ENABLE_SLACK_INTEGRATION: bool = False  # DISABLED - requires API key
    ENABLE_GOOGLE_DRIVE_INTEGRATION: bool = False  # DISABLED - requires API key

    # Official Government Data Integrations (FREE)
    ENABLE_DATAGOV_US_INTEGRATION: bool = True  # ✅ Re-enabled - free, no API key required
    ENABLE_DATAGOV_IL_INTEGRATION: bool = False  # Temporarily disabled due to API issues
    ENABLE_BANK_OF_ISRAEL_INTEGRATION: bool = True  # ✅ Enhanced with SDMX API
    ENABLE_HUD_INTEGRATION: bool = True  # ⚠️ Requires HUD_API_KEY for data access
    ENABLE_FHFA_INTEGRATION: bool = True  # ✅ Enhanced with CSV download

    # ================================
    # LLM CONFIGURATION (Local Ollama)
    # ================================
    ENABLE_LLM: bool = Field(
        default=True,
        description="Enable local LLM features (Ollama)"
    )
    OLLAMA_BASE_URL: str = Field(
        default="http://localhost:11434",
        description="Ollama API base URL"
    )
    OLLAMA_MODEL: str = Field(
        default="gemma:2b",
        description="Ollama model to use"
    )
    LLM_TIMEOUT: int = Field(
        default=30,
        description="LLM request timeout in seconds"
    )
    LLM_MAX_RETRIES: int = Field(
        default=2,
        description="Maximum retries for LLM requests"
    )
    LLM_CACHE_TTL: int = Field(
        default=3600,
        description="LLM response cache TTL (seconds)"
    )
    LLM_TEMPERATURE: float = Field(
        default=0.7,
        description="LLM generation temperature (0-1)"
    )
    LLM_MAX_TOKENS: int = Field(
        default=500,
        description="Maximum tokens to generate"
    )

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
