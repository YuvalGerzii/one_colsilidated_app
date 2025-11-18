"""
Configuration for Bond.AI Python Agents
"""

import os
from typing import Optional

class Config:
    """Python Agents Configuration"""

    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:3005",
        "http://localhost:3006",
        os.getenv("CORS_ORIGIN", ""),
    ]

    # Model Configuration
    SENTENCE_TRANSFORMER_MODEL: str = "all-MiniLM-L6-v2"
    ENABLE_GPU: bool = os.getenv("ENABLE_GPU", "false").lower() == "true"

    # Cache Configuration
    ENABLE_EMBEDDING_CACHE: bool = True
    CACHE_SIZE: int = 10000

    # Agent Configuration
    DEFAULT_CONFIDENCE_THRESHOLD: float = 0.6
    MIN_MATCH_SCORE: float = 0.5

    # Matching Weights
    SEMANTIC_WEIGHT: float = 0.15
    PERSONALITY_WEIGHT: float = 0.20
    COMMUNICATION_WEIGHT: float = 0.15
    INTEREST_WEIGHT: float = 0.12
    SKILLS_WEIGHT: float = 0.18
    VALUES_WEIGHT: float = 0.20

config = Config()
