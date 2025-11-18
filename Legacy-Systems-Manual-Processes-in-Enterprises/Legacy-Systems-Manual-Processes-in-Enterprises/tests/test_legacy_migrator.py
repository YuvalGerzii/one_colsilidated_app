"""Tests for Legacy Migrator."""

import pytest

from src.legacy_migrator.models import SourceLanguage, TargetLanguage
from src.legacy_migrator.analyzer import LegacyCodeAnalyzer


@pytest.mark.asyncio
async def test_code_analysis():
    """Test legacy code analysis."""
    analyzer = LegacyCodeAnalyzer()

    cobol_code = """
       IDENTIFICATION DIVISION.
       PROGRAM-ID. TEST.
       PROCEDURE DIVISION.
           DISPLAY 'Test'.
           STOP RUN.
    """

    analysis = await analyzer.analyze_code(cobol_code, SourceLanguage.COBOL)

    assert analysis.source_language == SourceLanguage.COBOL
    assert analysis.total_lines > 0
    assert analysis.complexity_score >= 0
    assert analysis.estimated_effort_hours > 0


@pytest.mark.asyncio
async def test_migration_strategy():
    """Test migration strategy creation."""
    from src.legacy_migrator.models import CodeAnalysis

    analyzer = LegacyCodeAnalyzer()

    analysis = CodeAnalysis(
        source_language=SourceLanguage.COBOL,
        total_lines=1000,
        complexity_score=5.0,
        estimated_effort_hours=500,
        risk_score=5.0,
    )

    strategy = await analyzer.create_migration_strategy(
        analysis, TargetLanguage.PYTHON
    )

    assert strategy.approach in ["big_bang", "strangler_fig", "parallel_run"]
    assert strategy.estimated_duration_days > 0
    assert len(strategy.phases) > 0
