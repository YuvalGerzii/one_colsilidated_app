"""
Internal Legal Services - No External APIs Required

This module provides comprehensive legal and compliance services
without requiring external API integrations.
"""

from app.services.document_template_engine import (
    template_engine,
    DocumentTemplateEngine,
    TemplateCategory,
    ConditionalLogic
)

from app.services.clause_analysis_service import (
    clause_analysis_service,
    ClauseAnalysisService,
    ClauseType,
    RiskLevel,
    ExtractedClause,
    ClausePattern
)

from app.services.risk_scoring_service import (
    risk_scoring_service,
    RiskScoringService,
    RiskCategory,
    RiskLevel as RiskScoreLevel,
    RiskFactor,
    RiskAssessment
)

from app.services.compliance_checklist_service import (
    compliance_checklist_service,
    ComplianceChecklistService,
    TransactionType,
    ChecklistItem,
    ChecklistItemStatus,
    ChecklistItemPriority,
    ComplianceChecklist
)

from app.services.deadline_calculator import (
    deadline_calculator,
    DeadlineCalculator,
    DeadlineType,
    ClaimType,
    Deadline
)

__all__ = [
    # Template Engine
    "template_engine",
    "DocumentTemplateEngine",
    "TemplateCategory",
    "ConditionalLogic",

    # Clause Analysis
    "clause_analysis_service",
    "ClauseAnalysisService",
    "ClauseType",
    "RiskLevel",
    "ExtractedClause",
    "ClausePattern",

    # Risk Scoring
    "risk_scoring_service",
    "RiskScoringService",
    "RiskCategory",
    "RiskScoreLevel",
    "RiskFactor",
    "RiskAssessment",

    # Compliance Checklists
    "compliance_checklist_service",
    "ComplianceChecklistService",
    "TransactionType",
    "ChecklistItem",
    "ChecklistItemStatus",
    "ChecklistItemPriority",
    "ComplianceChecklist",

    # Deadline Calculator
    "deadline_calculator",
    "DeadlineCalculator",
    "DeadlineType",
    "ClaimType",
    "Deadline",
]
