from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/workforce_db"

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Enterprise
    STRIPE_API_KEY: Optional[str] = None
    SUBSCRIPTION_TIERS: str = "basic,professional,enterprise"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
