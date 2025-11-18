"""Logging configuration for the application."""

import sys
from pathlib import Path

from loguru import logger

from src.core.config import get_settings

settings = get_settings()


def configure_logging() -> None:
    """Configure application logging."""
    # Remove default handler
    logger.remove()

    # Console handler
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=settings.log_level,
        colorize=True,
    )

    # File handler
    log_path = Path("logs")
    log_path.mkdir(exist_ok=True)

    logger.add(
        log_path / "app.log",
        rotation="500 MB",
        retention="30 days",
        level=settings.log_level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        backtrace=True,
        diagnose=True,
    )

    logger.info(f"Logging configured - Level: {settings.log_level}")


# Configure on import
configure_logging()
