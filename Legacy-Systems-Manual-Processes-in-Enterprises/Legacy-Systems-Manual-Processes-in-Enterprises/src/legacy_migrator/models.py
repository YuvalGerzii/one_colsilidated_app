"""Data models for Legacy Migrator."""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class SourceLanguage(str, Enum):
    """Supported source languages."""

    COBOL = "cobol"
    FORTRAN = "fortran"
    AS400 = "as400"
    SAP_ABAP = "sap_abap"
    PL1 = "pl1"
    ASSEMBLY = "assembly"


class TargetLanguage(str, Enum):
    """Supported target languages."""

    PYTHON = "python"
    JAVA = "java"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    GO = "go"
    RUST = "rust"


class MigrationStatus(str, Enum):
    """Migration status."""

    ANALYZING = "analyzing"
    PLANNING = "planning"
    TRANSLATING = "translating"
    TESTING = "testing"
    COMPLETED = "completed"
    FAILED = "failed"


class CodeAnalysis(BaseModel):
    """Analysis result of legacy code."""

    id: UUID = Field(default_factory=uuid4)
    source_language: SourceLanguage
    total_lines: int
    complexity_score: float
    dependencies: List[str] = Field(default_factory=list)
    api_calls: List[str] = Field(default_factory=list)
    data_structures: List[Dict[str, Any]] = Field(default_factory=list)
    estimated_effort_hours: float
    risk_score: float
    recommendations: List[str] = Field(default_factory=list)


class MigrationStrategy(BaseModel):
    """Migration strategy recommendation."""

    approach: str  # "big_bang", "strangler_fig", "parallel_run"
    phases: List[Dict[str, Any]]
    estimated_duration_days: int
    resource_requirements: Dict[str, Any]
    risk_mitigation: List[str]
    rollback_plan: str


class MigrationProject(BaseModel):
    """Migration project."""

    id: UUID = Field(default_factory=uuid4)
    name: str
    description: Optional[str] = None
    source_language: SourceLanguage
    target_language: TargetLanguage
    source_files: List[str]
    status: MigrationStatus = MigrationStatus.ANALYZING
    analysis: Optional[CodeAnalysis] = None
    strategy: Optional[MigrationStrategy] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TranslationResult(BaseModel):
    """Result of code translation."""

    source_file: str
    target_file: str
    source_code: str
    translated_code: str
    confidence: float
    warnings: List[str] = Field(default_factory=list)
    test_coverage: float = 0.0


class PerformanceSimulation(BaseModel):
    """Performance simulation results."""

    metric: str
    legacy_value: float
    modern_value: float
    improvement_percentage: float
    confidence: float
