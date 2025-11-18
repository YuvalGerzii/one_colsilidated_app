"""
Clause Analysis Service - Internal Implementation
Pattern matching and extraction for contract clauses without external APIs
"""

from typing import Dict, List, Optional, Tuple
from enum import Enum
import re
from dataclasses import dataclass


class ClauseType(str, Enum):
    """Types of clauses commonly found in contracts"""
    GOVERNING_LAW = "governing_law"
    ARBITRATION = "arbitration"
    CONFIDENTIALITY = "confidentiality"
    INDEMNIFICATION = "indemnification"
    TERMINATION = "termination"
    PAYMENT_TERMS = "payment_terms"
    WARRANTY = "warranty"
    LIABILITY_LIMITATION = "liability_limitation"
    FORCE_MAJEURE = "force_majeure"
    ASSIGNMENT = "assignment"
    SEVERABILITY = "severability"
    ENTIRE_AGREEMENT = "entire_agreement"
    AMENDMENT = "amendment"
    NOTICE = "notice"
    WAIVER = "waiver"
    COUNTERPARTS = "counterparts"
    NON_COMPETE = "non_compete"
    NON_SOLICITATION = "non_solicitation"
    INTELLECTUAL_PROPERTY = "intellectual_property"
    DATA_PRIVACY = "data_privacy"


class RiskLevel(str, Enum):
    """Risk levels for clause assessment"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFORMATIONAL = "informational"


@dataclass
class ClausePattern:
    """Pattern definition for identifying clauses"""
    clause_type: ClauseType
    patterns: List[str]  # Regex patterns
    keywords: List[str]  # Keywords that must be present
    risk_indicators: Dict[str, RiskLevel]  # Risk keywords and their levels
    standard_language: str  # Standard/recommended language


@dataclass
class ExtractedClause:
    """Represents an extracted clause from a document"""
    clause_type: ClauseType
    text: str
    start_position: int
    end_position: int
    confidence_score: float  # 0-100
    risk_level: RiskLevel
    risk_factors: List[str]
    recommendations: List[str]


class ClauseAnalysisService:
    """
    Service for analyzing contract clauses using pattern matching
    No external APIs required
    """

    # Clause patterns for identification
    CLAUSE_PATTERNS = {
        ClauseType.GOVERNING_LAW: ClausePattern(
            clause_type=ClauseType.GOVERNING_LAW,
            patterns=[
                r"(?:shall be|is|are)\s+governed\s+(?:by|in accordance with)\s+(?:the\s+)?laws?\s+of\s+(?:the\s+)?(?:State\s+of\s+)?(\w+)",
                r"governing\s+law[:\s]+(?:the\s+)?laws?\s+of\s+(?:the\s+)?(?:State\s+of\s+)?(\w+)",
                r"construction\s+and\s+interpretation.*?laws?\s+of\s+(?:the\s+)?(?:State\s+of\s+)?(\w+)"
            ],
            keywords=["governed", "law", "laws", "jurisdiction"],
            risk_indicators={
                "foreign": RiskLevel.HIGH,
                "international": RiskLevel.HIGH,
                "excluding": RiskLevel.MEDIUM,
                "choice of law": RiskLevel.LOW
            },
            standard_language="This Agreement shall be governed by and construed in accordance with the laws of the State of [STATE], without regard to its conflict of law principles."
        ),

        ClauseType.ARBITRATION: ClausePattern(
            clause_type=ClauseType.ARBITRATION,
            patterns=[
                r"(?:dispute|controversy|claim).*?(?:shall be|will be|must be)\s+(?:resolved|settled|determined)\s+(?:by|through)\s+(?:binding\s+)?arbitration",
                r"arbitration.*?(?:AAA|American Arbitration Association|JAMS)",
                r"(?:agree|agrees)\s+to\s+arbitrate.*?(?:disputes|claims|controversies)"
            ],
            keywords=["arbitration", "arbitrator", "dispute", "resolution"],
            risk_indicators={
                "binding": RiskLevel.HIGH,
                "waive": RiskLevel.CRITICAL,
                "class action": RiskLevel.CRITICAL,
                "jury trial": RiskLevel.HIGH,
                "AAA": RiskLevel.LOW,
                "JAMS": RiskLevel.LOW
            },
            standard_language="Any dispute arising out of or relating to this Agreement shall be resolved through binding arbitration in accordance with the Commercial Arbitration Rules of the American Arbitration Association."
        ),

        ClauseType.INDEMNIFICATION: ClausePattern(
            clause_type=ClauseType.INDEMNIFICATION,
            patterns=[
                r"(?:shall|will|agrees to)\s+(?:indemnify|defend|hold harmless)",
                r"indemnification.*?(?:from|against|for)\s+(?:any|all)",
                r"hold\s+harmless.*?(?:from|against)"
            ],
            keywords=["indemnify", "indemnification", "hold harmless", "defend"],
            risk_indicators={
                "unlimited": RiskLevel.CRITICAL,
                "any and all": RiskLevel.HIGH,
                "gross negligence": RiskLevel.MEDIUM,
                "willful misconduct": RiskLevel.MEDIUM,
                "third party": RiskLevel.HIGH,
                "attorneys' fees": RiskLevel.HIGH
            },
            standard_language="Each party shall indemnify, defend, and hold harmless the other party from and against any claims arising from its own negligence or willful misconduct, excluding claims arising from the other party's actions."
        ),

        ClauseType.LIABILITY_LIMITATION: ClausePattern(
            clause_type=ClauseType.LIABILITY_LIMITATION,
            patterns=[
                r"limitation\s+of\s+liability",
                r"(?:shall not|will not)\s+be\s+liable.*?(?:exceed|more than)",
                r"(?:total|aggregate|maximum)\s+liability.*?(?:limited|shall not exceed)",
                r"in no event.*?(?:liable|responsible).*?(?:indirect|consequential|incidental)"
            ],
            keywords=["liability", "liable", "damages", "limitation"],
            risk_indicators={
                "no liability": RiskLevel.CRITICAL,
                "unlimited": RiskLevel.CRITICAL,
                "consequential": RiskLevel.HIGH,
                "indirect": RiskLevel.HIGH,
                "punitive": RiskLevel.HIGH,
                "incidental": RiskLevel.MEDIUM,
                "special damages": RiskLevel.MEDIUM
            },
            standard_language="IN NO EVENT SHALL EITHER PARTY BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES. TOTAL LIABILITY SHALL NOT EXCEED THE AMOUNTS PAID UNDER THIS AGREEMENT."
        ),

        ClauseType.TERMINATION: ClausePattern(
            clause_type=ClauseType.TERMINATION,
            patterns=[
                r"(?:either party|party)\s+may\s+terminate.*?(?:upon|with|by providing)\s+(\d+)\s+(?:days?|months?)",
                r"termination.*?(?:notice|notification).*?(\d+)\s+(?:days?|months?)",
                r"(?:this agreement|agreement)\s+(?:may be|shall be)\s+terminated"
            ],
            keywords=["terminate", "termination", "notice", "cancel"],
            risk_indicators={
                "immediate": RiskLevel.HIGH,
                "without cause": RiskLevel.MEDIUM,
                "for convenience": RiskLevel.MEDIUM,
                "30 days": RiskLevel.LOW,
                "60 days": RiskLevel.LOW,
                "no notice": RiskLevel.CRITICAL
            },
            standard_language="Either party may terminate this Agreement upon thirty (30) days prior written notice to the other party. Termination for cause may be immediate upon written notice."
        ),

        ClauseType.CONFIDENTIALITY: ClausePattern(
            clause_type=ClauseType.CONFIDENTIALITY,
            patterns=[
                r"confidential(?:ity)?\s+(?:information|data|materials?)",
                r"(?:agrees?|shall)\s+(?:to\s+)?(?:keep|maintain|hold)\s+(?:in\s+)?(?:strict\s+)?confidence",
                r"non-disclosure",
                r"proprietary\s+(?:information|data)"
            ],
            keywords=["confidential", "proprietary", "disclosure", "secret"],
            risk_indicators={
                "perpetual": RiskLevel.HIGH,
                "indefinite": RiskLevel.HIGH,
                "5 years": RiskLevel.MEDIUM,
                "3 years": RiskLevel.LOW,
                "publicly available": RiskLevel.LOW,
                "prior knowledge": RiskLevel.LOW
            },
            standard_language="Receiving Party shall hold all Confidential Information in strict confidence and shall not disclose such information to third parties without prior written consent. This obligation shall survive for three (3) years following termination."
        ),

        ClauseType.NON_COMPETE: ClausePattern(
            clause_type=ClauseType.NON_COMPETE,
            patterns=[
                r"(?:shall not|agrees not to|covenant not to)\s+(?:compete|engage in)",
                r"non-compete|non-competition",
                r"restrictive\s+covenant"
            ],
            keywords=["compete", "competition", "non-compete", "covenant"],
            risk_indicators={
                "worldwide": RiskLevel.CRITICAL,
                "5 years": RiskLevel.CRITICAL,
                "3 years": RiskLevel.HIGH,
                "2 years": RiskLevel.MEDIUM,
                "1 year": RiskLevel.LOW,
                "reasonable": RiskLevel.LOW
            },
            standard_language="Employee agrees not to compete with the Company within [RADIUS] miles of its business locations for a period of [DURATION] following termination of employment."
        ),

        ClauseType.PAYMENT_TERMS: ClausePattern(
            clause_type=ClauseType.PAYMENT_TERMS,
            patterns=[
                r"payment.*?(?:due|payable).*?(\d+)\s+(?:days?|months?)",
                r"(?:shall pay|agrees to pay|will pay)\s+\$?([\d,]+)",
                r"net\s+(\d+)",
                r"invoice.*?(?:payment|due)"
            ],
            keywords=["payment", "pay", "invoice", "due", "net"],
            risk_indicators={
                "advance": RiskLevel.HIGH,
                "prepayment": RiskLevel.HIGH,
                "non-refundable": RiskLevel.HIGH,
                "net 30": RiskLevel.LOW,
                "net 60": RiskLevel.MEDIUM,
                "upon receipt": RiskLevel.HIGH
            },
            standard_language="Payment shall be due within thirty (30) days of invoice date. Late payments shall accrue interest at 1.5% per month."
        ),

        ClauseType.FORCE_MAJEURE: ClausePattern(
            clause_type=ClauseType.FORCE_MAJEURE,
            patterns=[
                r"force\s+majeure",
                r"(?:acts? of god|natural disaster|war|strike|pandemic)",
                r"(?:prevented|hindered|delayed).*?(?:beyond.*?control|unforeseeable)"
            ],
            keywords=["force majeure", "act of god", "beyond control", "unforeseeable"],
            risk_indicators={
                "perpetual": RiskLevel.HIGH,
                "terminate": RiskLevel.MEDIUM,
                "suspend": RiskLevel.MEDIUM,
                "pandemic": RiskLevel.LOW,
                "notice": RiskLevel.LOW
            },
            standard_language="Neither party shall be liable for failure to perform due to causes beyond its reasonable control, including acts of God, war, strikes, or pandemics, provided that notice is given promptly."
        ),

        ClauseType.INTELLECTUAL_PROPERTY: ClausePattern(
            clause_type=ClauseType.INTELLECTUAL_PROPERTY,
            patterns=[
                r"intellectual\s+property",
                r"(?:patent|copyright|trademark|trade secret)s?",
                r"ownership.*?(?:work product|deliverables|materials)",
                r"work(?:s)?\s+(?:for|made for)\s+hire"
            ],
            keywords=["intellectual property", "IP", "copyright", "patent", "trademark"],
            risk_indicators={
                "assigned": RiskLevel.HIGH,
                "irrevocable": RiskLevel.HIGH,
                "worldwide": RiskLevel.MEDIUM,
                "perpetual": RiskLevel.MEDIUM,
                "work for hire": RiskLevel.HIGH,
                "retain": RiskLevel.LOW
            },
            standard_language="All intellectual property rights in work product created under this Agreement shall be owned by [PARTY]. The other party hereby assigns all rights, title, and interest in such work product."
        ),

        ClauseType.ENTIRE_AGREEMENT: ClausePattern(
            clause_type=ClauseType.ENTIRE_AGREEMENT,
            patterns=[
                r"(?:this agreement|agreement)\s+(?:constitutes|represents)\s+the\s+entire",
                r"entire\s+agreement",
                r"supersedes.*?(?:prior|previous|earlier)\s+(?:agreements?|understandings?)"
            ],
            keywords=["entire agreement", "supersedes", "integration"],
            risk_indicators={
                "oral": RiskLevel.MEDIUM,
                "written": RiskLevel.LOW,
                "modification": RiskLevel.LOW
            },
            standard_language="This Agreement constitutes the entire agreement between the parties and supersedes all prior agreements, understandings, and negotiations, whether written or oral."
        ),
    }

    def __init__(self):
        """Initialize clause analysis service"""
        pass

    def extract_clauses(self, document_text: str) -> List[ExtractedClause]:
        """
        Extract and identify clauses from document text

        Args:
            document_text: Full text of the document

        Returns:
            List of extracted clauses with analysis
        """
        extracted_clauses = []

        for clause_type, pattern_def in self.CLAUSE_PATTERNS.items():
            clause = self._find_clause(document_text, pattern_def)
            if clause:
                extracted_clauses.append(clause)

        return extracted_clauses

    def _find_clause(
        self,
        document_text: str,
        pattern_def: ClausePattern
    ) -> Optional[ExtractedClause]:
        """Find a specific clause in document"""

        # Try each pattern
        for pattern in pattern_def.patterns:
            matches = re.finditer(pattern, document_text, re.IGNORECASE | re.DOTALL)

            for match in matches:
                # Extract surrounding context (paragraph)
                start = max(0, document_text.rfind('\n\n', 0, match.start()))
                end = document_text.find('\n\n', match.end())
                if end == -1:
                    end = len(document_text)

                clause_text = document_text[start:end].strip()

                # Calculate confidence based on keyword presence
                confidence = self._calculate_confidence(clause_text, pattern_def.keywords)

                if confidence > 50:  # Minimum confidence threshold
                    # Assess risk
                    risk_level, risk_factors = self._assess_risk(
                        clause_text,
                        pattern_def.risk_indicators
                    )

                    # Generate recommendations
                    recommendations = self._generate_recommendations(
                        pattern_def.clause_type,
                        risk_level,
                        risk_factors,
                        pattern_def.standard_language
                    )

                    return ExtractedClause(
                        clause_type=pattern_def.clause_type,
                        text=clause_text,
                        start_position=start,
                        end_position=end,
                        confidence_score=confidence,
                        risk_level=risk_level,
                        risk_factors=risk_factors,
                        recommendations=recommendations
                    )

        return None

    def _calculate_confidence(self, text: str, keywords: List[str]) -> float:
        """Calculate confidence score based on keyword presence"""
        text_lower = text.lower()
        matches = sum(1 for kw in keywords if kw.lower() in text_lower)
        return min(100, (matches / len(keywords)) * 100 + 20)

    def _assess_risk(
        self,
        clause_text: str,
        risk_indicators: Dict[str, RiskLevel]
    ) -> Tuple[RiskLevel, List[str]]:
        """Assess risk level of a clause"""
        text_lower = clause_text.lower()
        found_risks = []
        highest_risk = RiskLevel.LOW

        risk_values = {
            RiskLevel.INFORMATIONAL: 0,
            RiskLevel.LOW: 1,
            RiskLevel.MEDIUM: 2,
            RiskLevel.HIGH: 3,
            RiskLevel.CRITICAL: 4
        }

        for indicator, risk_level in risk_indicators.items():
            if indicator.lower() in text_lower:
                found_risks.append(indicator)
                if risk_values[risk_level] > risk_values[highest_risk]:
                    highest_risk = risk_level

        return highest_risk, found_risks

    def _generate_recommendations(
        self,
        clause_type: ClauseType,
        risk_level: RiskLevel,
        risk_factors: List[str],
        standard_language: str
    ) -> List[str]:
        """Generate recommendations for clause improvement"""
        recommendations = []

        if risk_level == RiskLevel.CRITICAL:
            recommendations.append("CRITICAL: This clause requires immediate legal review")
            recommendations.append("Consider removing or substantially revising this clause")

        if risk_level == RiskLevel.HIGH:
            recommendations.append("HIGH RISK: Consult with legal counsel before signing")
            recommendations.append("Request modifications to reduce risk exposure")

        if risk_level == RiskLevel.MEDIUM:
            recommendations.append("Review this clause carefully")
            recommendations.append("Consider negotiating for more favorable terms")

        # Add specific recommendations based on risk factors
        if "unlimited" in risk_factors:
            recommendations.append("Negotiate for caps or limitations on liability/obligations")

        if "perpetual" in risk_factors or "indefinite" in risk_factors:
            recommendations.append("Request a defined time period instead of perpetual terms")

        if "binding" in risk_factors and clause_type == ClauseType.ARBITRATION:
            recommendations.append("Understand that binding arbitration waives your right to court")

        if "waive" in risk_factors:
            recommendations.append("Carefully consider what rights you are waiving")

        # Add standard language suggestion
        if risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            recommendations.append(f"Consider standard language: {standard_language}")

        return recommendations

    def compare_clauses(
        self,
        clause1_text: str,
        clause2_text: str,
        clause_type: ClauseType
    ) -> Dict[str, any]:
        """
        Compare two clauses of the same type

        Returns:
            Dictionary with comparison results
        """
        pattern_def = self.CLAUSE_PATTERNS.get(clause_type)
        if not pattern_def:
            raise ValueError(f"Unknown clause type: {clause_type}")

        # Analyze both clauses
        risk1, factors1 = self._assess_risk(clause1_text, pattern_def.risk_indicators)
        risk2, factors2 = self._assess_risk(clause2_text, pattern_def.risk_indicators)

        # Find differences in risk factors
        unique_to_1 = set(factors1) - set(factors2)
        unique_to_2 = set(factors2) - set(factors1)
        common_factors = set(factors1) & set(factors2)

        # Calculate similarity score
        similarity = len(common_factors) / max(len(factors1), len(factors2), 1) * 100

        return {
            "clause_type": clause_type,
            "clause1_risk_level": risk1,
            "clause2_risk_level": risk2,
            "clause1_risk_factors": factors1,
            "clause2_risk_factors": factors2,
            "unique_risks_clause1": list(unique_to_1),
            "unique_risks_clause2": list(unique_to_2),
            "common_risk_factors": list(common_factors),
            "similarity_score": similarity,
            "recommendation": self._get_comparison_recommendation(risk1, risk2)
        }

    def _get_comparison_recommendation(
        self,
        risk1: RiskLevel,
        risk2: RiskLevel
    ) -> str:
        """Get recommendation based on risk comparison"""
        risk_values = {
            RiskLevel.INFORMATIONAL: 0,
            RiskLevel.LOW: 1,
            RiskLevel.MEDIUM: 2,
            RiskLevel.HIGH: 3,
            RiskLevel.CRITICAL: 4
        }

        if risk_values[risk1] < risk_values[risk2]:
            return "Clause 1 has lower risk - prefer this version"
        elif risk_values[risk1] > risk_values[risk2]:
            return "Clause 2 has lower risk - prefer this version"
        else:
            return "Both clauses have similar risk levels - review other factors"

    def find_missing_clauses(
        self,
        document_text: str,
        required_clauses: List[ClauseType]
    ) -> List[ClauseType]:
        """
        Identify clauses that are missing from a document

        Args:
            document_text: Full document text
            required_clauses: List of clause types that should be present

        Returns:
            List of missing clause types
        """
        extracted = self.extract_clauses(document_text)
        found_types = {clause.clause_type for clause in extracted}

        missing = [ct for ct in required_clauses if ct not in found_types]
        return missing

    def generate_clause_summary(self, document_text: str) -> Dict[str, any]:
        """
        Generate a summary of all clauses in a document

        Returns:
            Dictionary with clause analysis summary
        """
        extracted_clauses = self.extract_clauses(document_text)

        # Count by risk level
        risk_counts = {
            RiskLevel.CRITICAL: 0,
            RiskLevel.HIGH: 0,
            RiskLevel.MEDIUM: 0,
            RiskLevel.LOW: 0,
            RiskLevel.INFORMATIONAL: 0
        }

        for clause in extracted_clauses:
            risk_counts[clause.risk_level] += 1

        # Calculate overall risk score (0-100)
        risk_values = {
            RiskLevel.INFORMATIONAL: 0,
            RiskLevel.LOW: 25,
            RiskLevel.MEDIUM: 50,
            RiskLevel.HIGH: 75,
            RiskLevel.CRITICAL: 100
        }

        if extracted_clauses:
            overall_risk = sum(risk_values[c.risk_level] for c in extracted_clauses) / len(extracted_clauses)
        else:
            overall_risk = 0

        return {
            "total_clauses_found": len(extracted_clauses),
            "clause_types": [c.clause_type for c in extracted_clauses],
            "risk_distribution": risk_counts,
            "overall_risk_score": overall_risk,
            "critical_issues": [
                {
                    "clause_type": c.clause_type,
                    "risk_factors": c.risk_factors,
                    "recommendations": c.recommendations
                }
                for c in extracted_clauses
                if c.risk_level in [RiskLevel.CRITICAL, RiskLevel.HIGH]
            ],
            "clauses": [
                {
                    "type": c.clause_type,
                    "risk_level": c.risk_level,
                    "confidence": c.confidence_score,
                    "text_preview": c.text[:200] + "..." if len(c.text) > 200 else c.text
                }
                for c in extracted_clauses
            ]
        }


# Singleton instance
clause_analysis_service = ClauseAnalysisService()
