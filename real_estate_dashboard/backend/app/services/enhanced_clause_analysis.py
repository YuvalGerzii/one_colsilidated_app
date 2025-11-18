"""
Enhanced Clause Analysis with LLM Support

Combines existing pattern matching with optional LLM analysis.
Falls back gracefully to pattern matching if LLM unavailable.
"""

from typing import Dict, List, Optional, Any
import logging

from app.services.clause_analysis_service import (
    ClauseAnalysisService,
    ClauseType,
    RiskLevel,
    ExtractedClause
)
from app.services.llm_service import llm_service

logger = logging.getLogger(__name__)


class EnhancedClauseAnalysisService(ClauseAnalysisService):
    """
    Enhanced clause analysis with LLM support.

    If LLM is available:
        - Uses LLM for deeper clause interpretation
        - Provides more nuanced risk assessment
        - Generates detailed recommendations

    If LLM is unavailable:
        - Falls back to pattern matching (existing logic)
        - Still provides functional analysis
    """

    async def analyze_clause_with_llm(
        self,
        clause: ExtractedClause
    ) -> Dict[str, Any]:
        """
        Enhance clause analysis with LLM insights.

        Args:
            clause: Extracted clause from pattern matching

        Returns:
            Enhanced analysis with LLM insights or fallback to pattern-based analysis
        """
        system_prompt = """You are a legal expert specializing in contract analysis.
Analyze the provided contract clause and provide:
1. A clear interpretation in plain English
2. Potential risks or concerns
3. Recommendations for improvement

Be concise and practical."""

        prompt = f"""Analyze this {clause.clause_type.value} clause:

"{clause.text}"

Current risk assessment: {clause.risk_level.value}
Identified risk factors: {', '.join(clause.risk_factors) if clause.risk_factors else 'None'}

Provide your analysis."""

        result = await llm_service.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.3,  # Lower temp for more focused analysis
            max_tokens=300
        )

        if result:
            return {
                "clause_type": clause.clause_type.value,
                "text": clause.text,
                "start_position": clause.start_position,
                "end_position": clause.end_position,
                "confidence_score": clause.confidence_score,
                "risk_level": clause.risk_level.value,
                "risk_factors": clause.risk_factors,
                "recommendations": clause.recommendations,
                "llm_analysis": result["text"],
                "llm_used": True,
                "enhanced": True
            }
        else:
            # Fallback to existing analysis
            logger.info(f"LLM unavailable for clause analysis, using pattern-based analysis")
            return {
                "clause_type": clause.clause_type.value,
                "text": clause.text,
                "start_position": clause.start_position,
                "end_position": clause.end_position,
                "confidence_score": clause.confidence_score,
                "risk_level": clause.risk_level.value,
                "risk_factors": clause.risk_factors,
                "recommendations": clause.recommendations,
                "llm_analysis": None,
                "llm_used": False,
                "enhanced": False,
                "message": "LLM unavailable - using pattern-based analysis only"
            }

    async def analyze_document(
        self,
        document_text: str,
        use_llm: bool = True
    ) -> Dict[str, Any]:
        """
        Analyze full document with optional LLM enhancement.

        Args:
            document_text: Full contract text
            use_llm: Whether to use LLM for enhancement

        Returns:
            Complete analysis with all clauses
        """
        # Use existing pattern matching to extract clauses
        extracted_clauses = self.extract_all_clauses(document_text)

        # Enhance with LLM if requested and available
        if use_llm:
            enhanced_clauses = []
            for clause in extracted_clauses:
                enhanced = await self.analyze_clause_with_llm(clause)
                enhanced_clauses.append(enhanced)

            # Generate overall document summary with LLM
            summary = await self._generate_document_summary(
                document_text,
                extracted_clauses
            )

            return {
                "clauses": enhanced_clauses,
                "summary": summary,
                "llm_enhanced": any(c.get("llm_used") for c in enhanced_clauses),
                "total_clauses": len(extracted_clauses),
                "high_risk_count": sum(
                    1 for c in extracted_clauses
                    if c.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]
                )
            }
        else:
            # Return pattern-based analysis only
            return {
                "clauses": [
                    {
                        "clause_type": c.clause_type.value,
                        "text": c.text,
                        "start_position": c.start_position,
                        "end_position": c.end_position,
                        "confidence_score": c.confidence_score,
                        "risk_level": c.risk_level.value,
                        "risk_factors": c.risk_factors,
                        "recommendations": c.recommendations,
                        "llm_used": False
                    }
                    for c in extracted_clauses
                ],
                "llm_enhanced": False,
                "total_clauses": len(extracted_clauses),
                "high_risk_count": sum(
                    1 for c in extracted_clauses
                    if c.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]
                )
            }

    async def _generate_document_summary(
        self,
        document_text: str,
        clauses: List[ExtractedClause]
    ) -> Optional[str]:
        """Generate overall document summary using LLM"""

        # Extract key info about clauses
        high_risk_count = sum(
            1 for c in clauses
            if c.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]
        )

        clause_types = list(set(c.clause_type.value for c in clauses))

        prompt = f"""Summarize this contract document:

Total clauses identified: {len(clauses)}
High-risk clauses: {high_risk_count}
Clause types found: {', '.join(clause_types)}

Provide a brief 2-3 sentence summary of the overall document risk level and key considerations."""

        result = await llm_service.generate(
            prompt=prompt,
            system_prompt="You are a legal expert. Provide concise contract summaries.",
            temperature=0.3,
            max_tokens=150
        )

        return result["text"] if result else None

    async def analyze_single_clause(
        self,
        clause_text: str,
        clause_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze a single clause with LLM assistance.

        Args:
            clause_text: The clause text to analyze
            clause_type: Optional hint about clause type

        Returns:
            Analysis results with LLM insights if available
        """
        system_prompt = """You are a legal expert. Analyze the contract clause and provide:
1. Clause type identification
2. Risk assessment (Critical, High, Medium, Low)
3. Key concerns or red flags
4. Recommendations

Be specific and actionable."""

        prompt = f"""Analyze this contract clause:

"{clause_text}"
"""

        if clause_type:
            prompt += f"\nExpected type: {clause_type}"

        prompt += "\n\nProvide your analysis in a clear, structured format."

        result = await llm_service.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.3,
            max_tokens=400
        )

        if result:
            return {
                "clause_text": clause_text,
                "analysis": result["text"],
                "llm_used": True,
                "model": result["model"],
                "timestamp": result["timestamp"]
            }
        else:
            return {
                "clause_text": clause_text,
                "analysis": "LLM unavailable. Please use pattern-based analysis or try again later.",
                "llm_used": False,
                "message": "LLM service unavailable"
            }

    async def suggest_improvements(
        self,
        clause_text: str,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Suggest improvements to a contract clause.

        Args:
            clause_text: The clause to improve
            context: Optional context about the contract

        Returns:
            Suggested improvements or None if LLM unavailable
        """
        system_prompt = """You are a legal expert specializing in contract drafting.
Suggest specific improvements to make clauses clearer, fairer, and more enforceable."""

        prompt = f"""Review and suggest improvements for this clause:

"{clause_text}"
"""

        if context:
            prompt += f"\n\nContext: {context}"

        prompt += "\n\nProvide 2-3 specific suggestions for improvement."

        result = await llm_service.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.5,  # Medium creativity
            max_tokens=300
        )

        if result:
            return {
                "original_clause": clause_text,
                "suggestions": result["text"],
                "llm_used": True,
                "available": True
            }
        else:
            return {
                "original_clause": clause_text,
                "suggestions": None,
                "llm_used": False,
                "available": False,
                "message": "LLM service unavailable. Cannot generate suggestions."
            }


# Global instance
enhanced_clause_service = EnhancedClauseAnalysisService()
