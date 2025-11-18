"""
API routes for intelligent agent orchestration.
"""

from typing import Dict, Any, List, Optional

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field

from src.agents.framework import (
    AgentOrchestrator,
    AgentTask,
    AgentResult,
    AgentRole,
)
from src.agents.discovery_agent import LegacyDiscoveryAgent
from src.agents.quality_agent import CodeQualityAgent
from src.agents.debt_agent import TechnicalDebtAgent
from src.agents.security_agent import SecurityAuditorAgent
from src.agents.modernization_agent import ModernizationAdvisor
from src.core.logger import logger

router = APIRouter()

# Global orchestrator instance
_orchestrator: Optional[AgentOrchestrator] = None


def get_orchestrator() -> AgentOrchestrator:
    """Get or create agent orchestrator."""
    global _orchestrator

    if _orchestrator is None:
        _orchestrator = AgentOrchestrator()

        # Register all agents
        _orchestrator.register_agent(LegacyDiscoveryAgent())
        _orchestrator.register_agent(CodeQualityAgent())
        _orchestrator.register_agent(TechnicalDebtAgent())
        _orchestrator.register_agent(SecurityAuditorAgent())
        _orchestrator.register_agent(ModernizationAdvisor())

        logger.info("Agent orchestrator initialized with 5 agents")

    return _orchestrator


# ============================================================================
# Request/Response Models
# ============================================================================


class AgentTaskRequest(BaseModel):
    """Agent task request."""

    task_type: str = Field(..., description="Task type (scan, assess, analyze, audit, plan)")
    description: str = Field(..., description="Task description")
    input_data: Dict[str, Any] = Field(..., description="Task input data")
    agent_id: Optional[str] = Field(None, description="Specific agent ID to use")


class AgentTaskResponse(BaseModel):
    """Agent task response."""

    task_id: str
    agent_id: str
    status: str
    output: Dict[str, Any]
    confidence: float
    reasoning: str
    recommendations: List[str]
    next_steps: List[str]


class ComprehensiveAnalysisRequest(BaseModel):
    """Request for comprehensive legacy analysis."""

    codebase_path: Optional[str] = Field(".", description="Path to codebase")
    code_sample: Optional[str] = Field(None, description="Code sample to analyze")
    system_age_years: int = Field(10, description="Estimated system age in years")
    team_size: int = Field(5, description="Development team size")
    budget: float = Field(500000, description="Modernization budget")


class SecurityScanRequest(BaseModel):
    """Request for security scan."""

    code: str = Field(..., description="Code to scan")
    dependencies: List[str] = Field(default_factory=list, description="Dependencies list")
    configuration: Dict[str, Any] = Field(default_factory=dict, description="System configuration")


class ModernizationEstimateRequest(BaseModel):
    """Request for modernization estimate."""

    legacy_technology: str = Field(..., description="Legacy technology (cobol, vb6, etc)")
    lines_of_code: int = Field(..., description="Total lines of code")
    team_size: int = Field(5, description="Development team size")
    budget: float = Field(1000000, description="Available budget")


# ============================================================================
# Agent Endpoints
# ============================================================================


@router.get("/status")
async def get_agent_status() -> Dict[str, Any]:
    """Get agent orchestrator status."""
    orchestrator = get_orchestrator()

    agents_info = []
    for agent in orchestrator.agents.values():
        agents_info.append({
            "id": agent.agent_id,
            "role": agent.role.value,
            "status": agent.status.value,
            "capabilities": agent.get_capabilities(),
            "memory_size": len(agent.memory),
        })

    return {
        "status": "healthy",
        "total_agents": len(orchestrator.agents),
        "agents": agents_info,
        "active_tasks": len(orchestrator.task_results),
    }


@router.get("/agents")
async def list_agents() -> List[Dict[str, Any]]:
    """List all registered agents."""
    orchestrator = get_orchestrator()

    return [
        {
            "id": agent.agent_id,
            "role": agent.role.value,
            "status": agent.status.value,
            "capabilities": agent.get_capabilities(),
        }
        for agent in orchestrator.agents.values()
    ]


@router.post("/task", response_model=AgentTaskResponse)
async def execute_task(request: AgentTaskRequest) -> AgentTaskResponse:
    """
    Execute a single agent task.

    Example:
    ```json
    {
        "task_type": "scan",
        "description": "Scan codebase for legacy systems",
        "input_data": {"path": "/path/to/code"},
        "agent_id": "legacy-discovery"
    }
    ```
    """
    orchestrator = get_orchestrator()

    # Create task
    task = AgentTask(
        id=f"task-{len(orchestrator.task_results) + 1}",
        type=request.task_type,
        description=request.description,
        input_data=request.input_data,
        assigned_to=request.agent_id,
    )

    try:
        result = await orchestrator.execute_task(task)

        return AgentTaskResponse(
            task_id=result.task_id,
            agent_id=result.agent_id,
            status=result.status.value,
            output=result.output,
            confidence=result.confidence,
            reasoning=result.reasoning,
            recommendations=result.recommendations,
            next_steps=result.next_steps,
        )

    except Exception as e:
        logger.error(f"Task execution failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/workflow/comprehensive")
async def comprehensive_analysis(
    request: ComprehensiveAnalysisRequest,
    background_tasks: BackgroundTasks,
) -> Dict[str, Any]:
    """
    Execute comprehensive legacy system analysis workflow.

    Runs all agents in sequence:
    1. Discovery - Scan for legacy patterns
    2. Quality - Assess code quality
    3. Debt - Quantify technical debt
    4. Security - Audit vulnerabilities
    5. Modernization - Create migration plan

    Returns complete analysis with executive summary.
    """
    orchestrator = get_orchestrator()

    try:
        # Phase 1: Discovery
        discovery_task = AgentTask(
            id="discovery-workflow",
            type="scan",
            description="Scan codebase for legacy technologies",
            input_data={"path": request.codebase_path},
            assigned_to="legacy-discovery",
        )

        discovery_result = await orchestrator.execute_task(discovery_task)

        if discovery_result.status.value != "completed":
            raise HTTPException(status_code=500, detail="Discovery phase failed")

        # Phase 2: Quality Assessment
        code_to_analyze = request.code_sample or "# Sample code for analysis"

        quality_task = AgentTask(
            id="quality-workflow",
            type="assess",
            description="Assess code quality",
            input_data={"code": code_to_analyze},
            assigned_to="code-quality",
        )

        quality_result = await orchestrator.execute_task(quality_task)

        # Phase 3: Technical Debt
        total_lines = discovery_result.output.get('total_files', 100) * 500

        debt_task = AgentTask(
            id="debt-workflow",
            type="analyze",
            description="Analyze technical debt",
            input_data={
                "code": code_to_analyze,
                "system_age_years": request.system_age_years,
                "total_lines": total_lines,
                "team_size": request.team_size,
            },
            assigned_to="technical-debt",
        )

        debt_result = await orchestrator.execute_task(debt_task)

        # Phase 4: Security Audit
        security_task = AgentTask(
            id="security-workflow",
            type="audit",
            description="Perform security audit",
            input_data={
                "code": code_to_analyze,
                "dependencies": [],
                "configuration": {"debug": False, "ssl_enabled": True},
            },
            assigned_to="security-auditor",
        )

        security_result = await orchestrator.execute_task(security_task)

        # Phase 5: Modernization Planning
        technologies = discovery_result.output.get('technologies', {})

        modernization_task = AgentTask(
            id="modernization-workflow",
            type="plan",
            description="Create modernization plan",
            input_data={
                "legacy_technologies": technologies,
                "total_lines": total_lines,
                "team_size": request.team_size,
                "budget": request.budget,
            },
            assigned_to="modernization-advisor",
        )

        modernization_result = await orchestrator.execute_task(modernization_task)

        # Compile comprehensive report
        return {
            "status": "success",
            "workflow": "comprehensive_analysis",
            "phases": {
                "discovery": {
                    "status": discovery_result.status.value,
                    "output": discovery_result.output,
                    "recommendations": discovery_result.recommendations,
                },
                "quality": {
                    "status": quality_result.status.value,
                    "output": quality_result.output,
                    "recommendations": quality_result.recommendations,
                },
                "debt": {
                    "status": debt_result.status.value,
                    "output": debt_result.output,
                    "recommendations": debt_result.recommendations,
                },
                "security": {
                    "status": security_result.status.value,
                    "output": security_result.output,
                    "recommendations": security_result.recommendations,
                },
                "modernization": {
                    "status": modernization_result.status.value,
                    "output": modernization_result.output,
                    "recommendations": modernization_result.recommendations,
                },
            },
            "executive_summary": {
                "risk_level": discovery_result.output.get('risk_level', 'unknown'),
                "quality_score": quality_result.output.get('overall_score', 0),
                "technical_debt_hours": debt_result.output.get('total_hours', 0),
                "technical_debt_cost": debt_result.output.get('total_cost', 0),
                "security_risk_score": security_result.output.get('risk_score', 0),
                "critical_vulnerabilities": security_result.output.get('severity_summary', {}).get('critical', 0),
                "modernization_approach": modernization_result.output.get('approach', 'unknown'),
                "modernization_duration_months": modernization_result.output.get('roadmap', {}).get('total_duration_months', 0),
                "modernization_cost": modernization_result.output.get('cost_estimate', {}).get('total', 0),
            },
            "top_recommendations": (
                discovery_result.recommendations[:2] +
                quality_result.recommendations[:2] +
                debt_result.recommendations[:2] +
                security_result.recommendations[:2] +
                modernization_result.recommendations[:2]
            )[:10],
            "cost": {
                "ai_inference_cost": 0,
                "note": "100% FREE - Using local LLMs via Ollama",
            },
        }

    except Exception as e:
        logger.error(f"Comprehensive analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/workflow/security-scan")
async def security_scan(request: SecurityScanRequest) -> Dict[str, Any]:
    """
    Quick security vulnerability scan.

    Scans code for:
    - SQL injection
    - XSS vulnerabilities
    - Command injection
    - Hardcoded credentials
    - Weak cryptography
    - Insecure deserialization

    Maps to OWASP Top 10 2021.
    """
    orchestrator = get_orchestrator()

    task = AgentTask(
        id="security-scan",
        type="audit",
        description="Security vulnerability scan",
        input_data={
            "code": request.code,
            "dependencies": request.dependencies,
            "configuration": request.configuration,
        },
        assigned_to="security-auditor",
    )

    try:
        result = await orchestrator.execute_task(task)

        return {
            "status": "success",
            "vulnerabilities": result.output.get('vulnerabilities', []),
            "severity_summary": result.output.get('severity_summary', {}),
            "owasp_mapping": result.output.get('owasp_mapping', {}),
            "risk_score": result.output.get('risk_score', 0),
            "recommendations": result.recommendations,
            "remediation_steps": result.output.get('remediation_steps', []),
            "ai_analysis": result.output.get('ai_analysis', ''),
        }

    except Exception as e:
        logger.error(f"Security scan failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/workflow/modernization-estimate")
async def modernization_estimate(request: ModernizationEstimateRequest) -> Dict[str, Any]:
    """
    Generate modernization cost and timeline estimate.

    Provides:
    - Recommended technology stack
    - Phased migration roadmap
    - Detailed cost breakdown
    - Risk assessment
    - Success metrics
    """
    orchestrator = get_orchestrator()

    task = AgentTask(
        id="modernization-estimate",
        type="plan",
        description="Modernization cost estimate",
        input_data={
            "legacy_technologies": {request.legacy_technology: request.lines_of_code},
            "total_lines": request.lines_of_code,
            "team_size": request.team_size,
            "budget": request.budget,
        },
        assigned_to="modernization-advisor",
    )

    try:
        result = await orchestrator.execute_task(task)

        return {
            "status": "success",
            "approach": result.output.get('approach', 'unknown'),
            "recommended_stack": result.output.get('recommended_stack', {}),
            "roadmap": result.output.get('roadmap', {}),
            "cost_estimate": result.output.get('cost_estimate', {}),
            "risks": result.output.get('risks', []),
            "success_metrics": result.output.get('success_metrics', []),
            "recommendations": result.recommendations,
            "ai_strategy": result.output.get('ai_strategy', ''),
        }

    except Exception as e:
        logger.error(f"Modernization estimate failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/workflow/discovery")
async def legacy_discovery(codebase_path: str = ".") -> Dict[str, Any]:
    """
    Scan codebase for legacy systems and technologies.

    Detects:
    - Legacy languages (COBOL, Fortran, VB6, Perl, ASP Classic)
    - Obsolete frameworks
    - Old database systems
    - Outdated patterns
    - Risk level assessment
    """
    orchestrator = get_orchestrator()

    task = AgentTask(
        id="discovery-scan",
        type="scan",
        description="Legacy system discovery",
        input_data={"path": codebase_path},
        assigned_to="legacy-discovery",
    )

    try:
        result = await orchestrator.execute_task(task)

        return {
            "status": "success",
            "total_files": result.output.get('total_files', 0),
            "legacy_files": result.output.get('legacy_files', []),
            "technologies": result.output.get('technologies', {}),
            "frameworks": result.output.get('frameworks', {}),
            "obsolete_patterns": result.output.get('obsolete_patterns', []),
            "risk_level": result.output.get('risk_level', 'unknown'),
            "ai_analysis": result.output.get('ai_analysis', ''),
            "recommendations": result.recommendations,
        }

    except Exception as e:
        logger.error(f"Discovery scan failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/workflow/quality-assessment")
async def quality_assessment(code: str) -> Dict[str, Any]:
    """
    Assess code quality metrics.

    Analyzes:
    - Cyclomatic complexity
    - Code smells
    - Security issues
    - Documentation coverage
    - Overall quality score (0-10)
    """
    orchestrator = get_orchestrator()

    task = AgentTask(
        id="quality-assessment",
        type="assess",
        description="Code quality assessment",
        input_data={"code": code},
        assigned_to="code-quality",
    )

    try:
        result = await orchestrator.execute_task(task)

        return {
            "status": "success",
            "overall_score": result.output.get('overall_score', 0),
            "complexity_score": result.output.get('complexity_score', 0),
            "code_smells": result.output.get('code_smells', []),
            "issues": result.output.get('issues', []),
            "metrics": result.output.get('metrics', {}),
            "recommendations": result.recommendations,
            "ai_insights": result.output.get('ai_insights', ''),
        }

    except Exception as e:
        logger.error(f"Quality assessment failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/workflow/debt-analysis")
async def debt_analysis(
    code: str,
    system_age_years: int = 10,
    team_size: int = 5,
) -> Dict[str, Any]:
    """
    Quantify technical debt in hours and dollars.

    Calculates:
    - Total debt hours and cost
    - Monthly interest (ongoing costs)
    - ROI-based prioritization
    - Quick wins vs major projects
    - Payoff strategies
    """
    orchestrator = get_orchestrator()

    # Estimate total lines
    total_lines = len(code.split('\n')) * 100

    task = AgentTask(
        id="debt-analysis",
        type="analyze",
        description="Technical debt analysis",
        input_data={
            "code": code,
            "system_age_years": system_age_years,
            "total_lines": total_lines,
            "team_size": team_size,
        },
        assigned_to="technical-debt",
    )

    try:
        result = await orchestrator.execute_task(task)

        return {
            "status": "success",
            "total_hours": result.output.get('total_hours', 0),
            "total_cost": result.output.get('total_cost', 0),
            "total_interest_monthly": result.output.get('total_interest_monthly', 0),
            "priority_matrix": result.output.get('priority_matrix', {}),
            "debt_categories": result.output.get('debt_categories', {}),
            "payoff_strategy": result.output.get('payoff_strategy', []),
            "recommendations": result.recommendations,
            "ai_analysis": result.output.get('ai_analysis', ''),
        }

    except Exception as e:
        logger.error(f"Debt analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check for agents module."""
    return {"status": "healthy", "module": "agents"}
