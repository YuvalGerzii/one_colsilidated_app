"""API routes for Legacy Migrator."""

from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.legacy_migrator.models import (
    MigrationProject,
    CodeAnalysis,
    TranslationResult,
    SourceLanguage,
    TargetLanguage,
)
from src.legacy_migrator.analyzer import LegacyCodeAnalyzer, CodeTranslator
from src.core.logger import logger

router = APIRouter()
analyzer = LegacyCodeAnalyzer()
translator = CodeTranslator()


@router.post("/analyze", response_model=CodeAnalysis)
async def analyze_code(source_code: str, source_language: SourceLanguage) -> CodeAnalysis:
    """Analyze legacy code."""
    try:
        analysis = await analyzer.analyze_code(source_code, source_language)
        return analysis
    except Exception as e:
        logger.error(f"Code analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/translate", response_model=TranslationResult)
async def translate_code(
    source_code: str,
    source_language: SourceLanguage,
    target_language: TargetLanguage,
) -> TranslationResult:
    """Translate legacy code to modern language."""
    try:
        result = await translator.translate_code(source_code, source_language, target_language)
        return result
    except Exception as e:
        logger.error(f"Code translation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/projects", response_model=MigrationProject)
async def create_migration_project(project: MigrationProject) -> MigrationProject:
    """Create a new migration project."""
    logger.info(f"Creating migration project: {project.name}")
    return project


@router.get("/health")
async def health_check() -> dict:
    """Health check for legacy migrator."""
    return {"status": "healthy", "module": "legacy_migrator"}
