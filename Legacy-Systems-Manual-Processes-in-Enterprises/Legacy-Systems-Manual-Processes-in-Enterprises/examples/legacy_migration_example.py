"""
Example: Migrating COBOL to Python
"""

import asyncio

from src.legacy_migrator.models import SourceLanguage, TargetLanguage
from src.legacy_migrator.analyzer import LegacyCodeAnalyzer, CodeTranslator


async def main():
    """Example legacy code migration."""

    # Sample COBOL code
    cobol_code = """
       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLO-WORLD.
       PROCEDURE DIVISION.
           DISPLAY 'Hello, World!'.
           STOP RUN.
    """

    # Analyze the code
    analyzer = LegacyCodeAnalyzer()
    print("Analyzing COBOL code...")
    analysis = await analyzer.analyze_code(cobol_code, SourceLanguage.COBOL)

    print(f"Total lines: {analysis.total_lines}")
    print(f"Complexity score: {analysis.complexity_score}")
    print(f"Estimated effort: {analysis.estimated_effort_hours} hours")
    print(f"Risk score: {analysis.risk_score}")
    print(f"Recommendations: {analysis.recommendations}")

    # Create migration strategy
    strategy = await analyzer.create_migration_strategy(analysis, TargetLanguage.PYTHON)
    print(f"\nMigration approach: {strategy.approach}")
    print(f"Estimated duration: {strategy.estimated_duration_days} days")

    # Translate code
    translator = CodeTranslator()
    print("\nTranslating to Python...")
    result = await translator.translate_code(
        cobol_code,
        SourceLanguage.COBOL,
        TargetLanguage.PYTHON,
    )

    print(f"Translation confidence: {result.confidence}")
    print(f"\nTranslated code:\n{result.translated_code}")


if __name__ == "__main__":
    asyncio.run(main())
