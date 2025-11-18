"""Legacy code analysis and migration planning."""

import re
from typing import Dict, List, Any

from loguru import logger

from src.legacy_migrator.models import (
    SourceLanguage,
    TargetLanguage,
    CodeAnalysis,
    MigrationStrategy,
    TranslationResult,
)
from src.core.config import get_settings
from src.core.llm import get_local_llm

settings = get_settings()


class LegacyCodeAnalyzer:
    """Analyzes legacy code for migration using FREE local LLMs."""

    def __init__(self) -> None:
        """Initialize analyzer with local LLM."""
        self.llm = get_local_llm()
        logger.info("Using LOCAL LLM - 100% Free, no API keys required!")

    async def analyze_code(
        self, source_code: str, source_language: SourceLanguage
    ) -> CodeAnalysis:
        """
        Analyze legacy code.

        Args:
            source_code: Source code to analyze
            source_language: Programming language

        Returns:
            CodeAnalysis: Analysis results
        """
        logger.info(f"Analyzing {source_language} code")

        # Basic analysis
        lines = source_code.split("\n")
        total_lines = len([l for l in lines if l.strip()])

        # Calculate complexity (simplified)
        complexity_score = self._calculate_complexity(source_code)

        # Extract dependencies
        dependencies = self._extract_dependencies(source_code, source_language)

        # Extract API calls
        api_calls = self._extract_api_calls(source_code)

        analysis = CodeAnalysis(
            source_language=source_language,
            total_lines=total_lines,
            complexity_score=complexity_score,
            dependencies=dependencies,
            api_calls=api_calls,
            estimated_effort_hours=self._estimate_effort(total_lines, complexity_score),
            risk_score=self._calculate_risk(complexity_score, len(dependencies)),
            recommendations=self._generate_recommendations(complexity_score),
        )

        logger.info(f"Analysis complete: {total_lines} lines, complexity: {complexity_score}")
        return analysis

    def _calculate_complexity(self, code: str) -> float:
        """Calculate code complexity."""
        # Simplified cyclomatic complexity
        decision_points = len(re.findall(r"\b(if|while|for|case)\b", code, re.IGNORECASE))
        total_lines = len(code.split("\n"))
        return min(10.0, (decision_points / max(total_lines, 1)) * 100)

    def _extract_dependencies(
        self, code: str, language: SourceLanguage
    ) -> List[str]:
        """Extract code dependencies."""
        dependencies = []

        if language == SourceLanguage.COBOL:
            # Extract COPY statements
            dependencies = re.findall(r"COPY\s+(\S+)", code, re.IGNORECASE)
        elif language == SourceLanguage.PYTHON:
            dependencies = re.findall(r"import\s+(\S+)", code)

        return list(set(dependencies))

    def _extract_api_calls(self, code: str) -> List[str]:
        """Extract API calls."""
        # Simplified API call detection
        api_patterns = [
            r"https?://[^\s]+",
            r"CALL\s+['\"](\S+)['\"]",
        ]

        api_calls = []
        for pattern in api_patterns:
            api_calls.extend(re.findall(pattern, code, re.IGNORECASE))

        return list(set(api_calls))

    def _estimate_effort(self, lines: int, complexity: float) -> float:
        """Estimate migration effort in hours."""
        base_rate = 0.5  # hours per line
        complexity_multiplier = 1 + (complexity / 10)
        return lines * base_rate * complexity_multiplier

    def _calculate_risk(self, complexity: float, dependency_count: int) -> float:
        """Calculate migration risk score (0-10)."""
        risk = (complexity * 0.5) + (dependency_count * 0.2)
        return min(10.0, risk)

    def _generate_recommendations(self, complexity: float) -> List[str]:
        """Generate migration recommendations."""
        recommendations = []

        if complexity > 7:
            recommendations.append("High complexity detected. Consider incremental migration.")
        if complexity < 3:
            recommendations.append("Low complexity. Good candidate for automated translation.")

        recommendations.append("Generate comprehensive test suite before migration.")
        recommendations.append("Set up parallel running environment for validation.")

        return recommendations

    async def create_migration_strategy(
        self, analysis: CodeAnalysis, target_language: TargetLanguage
    ) -> MigrationStrategy:
        """
        Create migration strategy.

        Args:
            analysis: Code analysis results
            target_language: Target programming language

        Returns:
            MigrationStrategy: Recommended strategy
        """
        # Determine approach based on risk
        if analysis.risk_score > 7:
            approach = "strangler_fig"
        elif analysis.risk_score < 3:
            approach = "big_bang"
        else:
            approach = "parallel_run"

        strategy = MigrationStrategy(
            approach=approach,
            phases=[
                {"name": "Analysis", "duration_days": 5},
                {"name": "Translation", "duration_days": 15},
                {"name": "Testing", "duration_days": 10},
                {"name": "Deployment", "duration_days": 5},
            ],
            estimated_duration_days=35,
            resource_requirements={
                "developers": 3,
                "qa_engineers": 2,
                "devops": 1,
            },
            risk_mitigation=[
                "Comprehensive test coverage",
                "Parallel running period",
                "Gradual traffic migration",
            ],
            rollback_plan="Maintain legacy system for 6 months post-migration",
        )

        return strategy


class CodeTranslator:
    """Translates legacy code to modern languages using FREE local LLMs."""

    def __init__(self) -> None:
        """Initialize translator with local LLM."""
        self.llm = get_local_llm()
        logger.info("Code Translator using LOCAL LLM - 100% Free!")

    async def translate_code(
        self,
        source_code: str,
        source_language: SourceLanguage,
        target_language: TargetLanguage,
    ) -> TranslationResult:
        """
        Translate code to modern language.

        Args:
            source_code: Source code
            source_language: Source programming language
            target_language: Target programming language

        Returns:
            TranslationResult: Translation result
        """
        logger.info(f"Translating {source_language} to {target_language} using LOCAL LLM")

        # Always use local LLM (free!)
        is_available = await self.llm.is_available()

        if is_available:
            # Use local AI for translation
            translated_code = await self._local_llm_translation(
                source_code, source_language, target_language
            )
            confidence = 0.85
        else:
            # Fallback: basic translation
            logger.warning("Local LLM unavailable, using rule-based fallback")
            translated_code = self._basic_translation(source_code, target_language)
            confidence = 0.5

        result = TranslationResult(
            source_file="input.source",
            target_file=f"output.{target_language.value}",
            source_code=source_code,
            translated_code=translated_code,
            confidence=confidence,
            warnings=[],
        )

        return result

    def _basic_translation(self, source_code: str, target: TargetLanguage) -> str:
        """Basic rule-based translation."""
        # This is a simplified placeholder
        return f"# Translated to {target.value}\n# Original code:\n# {source_code}\n\n# Translation placeholder"

    async def _local_llm_translation(
        self,
        source_code: str,
        source_language: SourceLanguage,
        target_language: TargetLanguage,
    ) -> str:
        """Local LLM-powered code translation (100% FREE!)."""
        prompt = f"""Translate the following {source_language.value} code to {target_language.value}.
Ensure the translation maintains the same logic and functionality.
Provide clean, idiomatic {target_language.value} code with proper error handling.

Source code:
```{source_language.value}
{source_code}
```

Translated code:"""

        try:
            translated = await self.llm.chat_completion(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=2000,
            )

            # Extract code from markdown if present
            if "```" in translated:
                code_match = re.search(r"```(?:\w+)?\n(.*?)```", translated, re.DOTALL)
                if code_match:
                    translated = code_match.group(1)

            return translated

        except Exception as e:
            logger.error(f"Local LLM translation failed: {e}")
            return self._basic_translation(source_code, target_language)
