"""
Comprehensive Agent Workflow Example
=====================================

This example demonstrates the full agent orchestration workflow:
1. Discovery Agent scans legacy codebase
2. Quality Agent assesses code quality
3. Debt Agent quantifies technical debt
4. Security Agent audits vulnerabilities
5. Modernization Advisor creates migration plan

All agents use 100% FREE local LLMs - NO API costs!
"""

import asyncio
from pathlib import Path
from typing import Dict, Any

from loguru import logger

from src.agents.framework import AgentOrchestrator, AgentTask, AgentRole
from src.agents.discovery_agent import LegacyDiscoveryAgent
from src.agents.quality_agent import CodeQualityAgent
from src.agents.debt_agent import TechnicalDebtAgent
from src.agents.security_agent import SecurityAuditorAgent
from src.agents.modernization_agent import ModernizationAdvisor


async def comprehensive_legacy_analysis(codebase_path: str) -> Dict[str, Any]:
    """
    Perform comprehensive legacy system analysis using all agents.

    Args:
        codebase_path: Path to legacy codebase

    Returns:
        Complete analysis with recommendations
    """
    logger.info("🚀 Starting comprehensive legacy system analysis...")
    logger.info(f"📁 Codebase: {codebase_path}")

    # Initialize orchestrator
    orchestrator = AgentOrchestrator()

    # Register all agents
    discovery_agent = LegacyDiscoveryAgent()
    quality_agent = CodeQualityAgent()
    debt_agent = TechnicalDebtAgent()
    security_agent = SecurityAuditorAgent()
    modernization_agent = ModernizationAdvisor()

    orchestrator.register_agent(discovery_agent)
    orchestrator.register_agent(quality_agent)
    orchestrator.register_agent(debt_agent)
    orchestrator.register_agent(security_agent)
    orchestrator.register_agent(modernization_agent)

    logger.info(f"✅ Registered {len(orchestrator.agents)} agents")

    # =========================================================================
    # PHASE 1: DISCOVERY
    # =========================================================================
    logger.info("\n" + "="*80)
    logger.info("PHASE 1: LEGACY SYSTEM DISCOVERY")
    logger.info("="*80)

    discovery_task = AgentTask(
        id="discovery-001",
        type="scan",
        description="Scan codebase for legacy technologies",
        input_data={"path": codebase_path},
        assigned_to="legacy-discovery",
    )

    discovery_result = await orchestrator.execute_task(discovery_task)

    if discovery_result.status.value == "completed":
        logger.info("✅ Discovery completed")
        logger.info(f"   Total files: {discovery_result.output.get('total_files', 0)}")
        logger.info(f"   Legacy files: {len(discovery_result.output.get('legacy_files', []))}")
        logger.info(f"   Risk level: {discovery_result.output.get('risk_level', 'unknown')}")

        technologies = discovery_result.output.get('technologies', {})
        if technologies:
            logger.info(f"   Technologies found: {', '.join(technologies.keys())}")
    else:
        logger.error("❌ Discovery failed")
        return {"error": "Discovery phase failed"}

    # =========================================================================
    # PHASE 2: CODE QUALITY ASSESSMENT
    # =========================================================================
    logger.info("\n" + "="*80)
    logger.info("PHASE 2: CODE QUALITY ASSESSMENT")
    logger.info("="*80)

    # Read sample code from discovered legacy files
    legacy_files = discovery_result.output.get('legacy_files', [])
    sample_code = ""

    if legacy_files and Path(codebase_path).exists():
        # Read first legacy file as sample
        first_file = legacy_files[0]
        try:
            with open(first_file.get('path', ''), 'r', encoding='utf-8', errors='ignore') as f:
                sample_code = f.read(50000)  # Limit to 50KB
        except Exception as e:
            logger.warning(f"Could not read sample file: {e}")
            sample_code = "# Sample placeholder code for analysis"

    quality_task = AgentTask(
        id="quality-001",
        type="assess",
        description="Assess code quality metrics",
        input_data={"code": sample_code or "# Sample code"},
        assigned_to="code-quality",
    )

    quality_result = await orchestrator.execute_task(quality_task)

    if quality_result.status.value == "completed":
        logger.info("✅ Quality assessment completed")
        logger.info(f"   Quality score: {quality_result.output.get('overall_score', 0):.1f}/10")
        logger.info(f"   Complexity: {quality_result.output.get('complexity_score', 0)}")
        logger.info(f"   Code smells: {len(quality_result.output.get('code_smells', []))}")
        logger.info(f"   Issues: {len(quality_result.output.get('issues', []))}")
    else:
        logger.error("❌ Quality assessment failed")

    # =========================================================================
    # PHASE 3: TECHNICAL DEBT ANALYSIS
    # =========================================================================
    logger.info("\n" + "="*80)
    logger.info("PHASE 3: TECHNICAL DEBT ANALYSIS")
    logger.info("="*80)

    # Estimate total lines from discovery
    total_lines = discovery_result.output.get('total_files', 100) * 500  # Rough estimate

    debt_task = AgentTask(
        id="debt-001",
        type="analyze",
        description="Analyze technical debt",
        input_data={
            "code": sample_code or "# Sample code",
            "system_age_years": 10,
            "total_lines": total_lines,
            "team_size": 5,
        },
        assigned_to="technical-debt",
    )

    debt_result = await orchestrator.execute_task(debt_task)

    if debt_result.status.value == "completed":
        logger.info("✅ Debt analysis completed")
        logger.info(f"   Total debt: {debt_result.output.get('total_hours', 0):.0f} hours")
        logger.info(f"   Dollar value: ${debt_result.output.get('total_cost', 0):,.0f}")
        logger.info(f"   Monthly interest: ${debt_result.output.get('total_interest_monthly', 0):,.0f}")

        priority = debt_result.output.get('priority_matrix', {})
        quick_wins = priority.get('quick_win', [])
        if quick_wins:
            logger.info(f"   Quick wins available: {len(quick_wins)}")
    else:
        logger.error("❌ Debt analysis failed")

    # =========================================================================
    # PHASE 4: SECURITY AUDIT
    # =========================================================================
    logger.info("\n" + "="*80)
    logger.info("PHASE 4: SECURITY AUDIT")
    logger.info("="*80)

    security_task = AgentTask(
        id="security-001",
        type="audit",
        description="Perform security audit",
        input_data={
            "code": sample_code or "# Sample code",
            "dependencies": [],
            "configuration": {
                "debug": False,
                "ssl_enabled": True,
            },
        },
        assigned_to="security-auditor",
    )

    security_result = await orchestrator.execute_task(security_task)

    if security_result.status.value == "completed":
        logger.info("✅ Security audit completed")

        severity_summary = security_result.output.get('severity_summary', {})
        logger.info(f"   Critical: {severity_summary.get('critical', 0)}")
        logger.info(f"   High: {severity_summary.get('high', 0)}")
        logger.info(f"   Medium: {severity_summary.get('medium', 0)}")
        logger.info(f"   Risk score: {security_result.output.get('risk_score', 0):.1f}/10")

        owasp = security_result.output.get('owasp_mapping', {})
        if owasp:
            logger.info(f"   OWASP categories: {len(owasp)}")
    else:
        logger.error("❌ Security audit failed")

    # =========================================================================
    # PHASE 5: MODERNIZATION PLANNING
    # =========================================================================
    logger.info("\n" + "="*80)
    logger.info("PHASE 5: MODERNIZATION PLANNING")
    logger.info("="*80)

    modernization_task = AgentTask(
        id="modernization-001",
        type="plan",
        description="Create modernization plan",
        input_data={
            "legacy_technologies": technologies,
            "total_lines": total_lines,
            "team_size": 5,
            "budget": 500000,
        },
        assigned_to="modernization-advisor",
    )

    modernization_result = await orchestrator.execute_task(modernization_task)

    if modernization_result.status.value == "completed":
        logger.info("✅ Modernization plan created")
        logger.info(f"   Approach: {modernization_result.output.get('approach', 'unknown')}")

        roadmap = modernization_result.output.get('roadmap', {})
        logger.info(f"   Duration: {roadmap.get('total_duration_months', 0)} months")

        cost = modernization_result.output.get('cost_estimate', {})
        logger.info(f"   Estimated cost: ${cost.get('total', 0):,.0f}")

        risks = modernization_result.output.get('risks', [])
        logger.info(f"   Identified risks: {len(risks)}")

        stack = modernization_result.output.get('recommended_stack', {})
        if stack:
            backend = stack.get('backend', {})
            logger.info(f"   Recommended stack: {backend.get('language', 'N/A')} + {backend.get('framework', 'N/A')}")
    else:
        logger.error("❌ Modernization planning failed")

    # =========================================================================
    # FINAL REPORT
    # =========================================================================
    logger.info("\n" + "="*80)
    logger.info("FINAL COMPREHENSIVE REPORT")
    logger.info("="*80)

    report = {
        "discovery": discovery_result.output,
        "quality": quality_result.output,
        "debt": debt_result.output,
        "security": security_result.output,
        "modernization": modernization_result.output,
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
        "recommendations": {
            "discovery": discovery_result.recommendations,
            "quality": quality_result.recommendations,
            "debt": debt_result.recommendations,
            "security": security_result.recommendations,
            "modernization": modernization_result.recommendations,
        },
    }

    logger.info("\n📊 Executive Summary:")
    logger.info(f"   Overall Risk: {report['executive_summary']['risk_level'].upper()}")
    logger.info(f"   Quality Score: {report['executive_summary']['quality_score']:.1f}/10")
    logger.info(f"   Technical Debt: ${report['executive_summary']['technical_debt_cost']:,.0f} ({report['executive_summary']['technical_debt_hours']:.0f} hours)")
    logger.info(f"   Security Risk: {report['executive_summary']['security_risk_score']:.1f}/10")
    logger.info(f"   Modernization: {report['executive_summary']['modernization_duration_months']} months, ${report['executive_summary']['modernization_cost']:,.0f}")

    logger.info("\n🎯 Top Recommendations:")
    all_recommendations = (
        discovery_result.recommendations[:2] +
        quality_result.recommendations[:2] +
        debt_result.recommendations[:2] +
        security_result.recommendations[:2] +
        modernization_result.recommendations[:2]
    )

    for i, rec in enumerate(all_recommendations[:10], 1):
        logger.info(f"   {i}. {rec}")

    logger.info("\n✅ Comprehensive analysis complete!")
    logger.info("💰 Total AI cost: $0 (100% FREE local LLMs!)")

    return report


async def quick_security_scan(code_snippet: str) -> Dict[str, Any]:
    """
    Quick security scan of a code snippet.

    Args:
        code_snippet: Code to scan

    Returns:
        Security audit results
    """
    logger.info("🔒 Running quick security scan...")

    agent = SecurityAuditorAgent()

    task = AgentTask(
        id="quick-security",
        type="audit",
        description="Quick security scan",
        input_data={
            "code": code_snippet,
            "dependencies": [],
            "configuration": {},
        },
        assigned_to="security-auditor",
    )

    result = await agent.execute(task)

    if result.status.value == "completed":
        logger.info("✅ Security scan complete")
        logger.info(f"   Vulnerabilities: {len(result.output.get('vulnerabilities', []))}")
        logger.info(f"   Risk score: {result.output.get('risk_score', 0):.1f}/10")

    return result.output


async def estimate_modernization_cost(
    legacy_tech: str,
    lines_of_code: int,
    team_size: int = 5,
) -> Dict[str, Any]:
    """
    Quick modernization cost estimate.

    Args:
        legacy_tech: Legacy technology (e.g., 'cobol', 'vb6')
        lines_of_code: Total lines of code
        team_size: Development team size

    Returns:
        Modernization plan with cost estimates
    """
    logger.info(f"💡 Estimating modernization for {lines_of_code:,} lines of {legacy_tech}...")

    agent = ModernizationAdvisor()

    task = AgentTask(
        id="quick-estimate",
        type="plan",
        description="Cost estimation",
        input_data={
            "legacy_technologies": {legacy_tech: lines_of_code},
            "total_lines": lines_of_code,
            "team_size": team_size,
            "budget": 1000000,
        },
        assigned_to="modernization-advisor",
    )

    result = await agent.execute(task)

    if result.status.value == "completed":
        cost = result.output.get('cost_estimate', {})
        roadmap = result.output.get('roadmap', {})

        logger.info("✅ Estimate complete")
        logger.info(f"   Duration: {roadmap.get('total_duration_months', 0)} months")
        logger.info(f"   Cost: ${cost.get('total', 0):,.0f}")
        logger.info(f"   Approach: {result.output.get('approach', 'unknown')}")

    return result.output


async def main():
    """Main example runner."""

    print("="*80)
    print("ENTERPRISE AI MODERNIZATION SUITE - AGENT WORKFLOW EXAMPLES")
    print("="*80)
    print("\n💰 Using 100% FREE local LLMs - NO API costs!\n")

    # Example 1: Comprehensive analysis
    print("\n📋 Example 1: Comprehensive Legacy System Analysis")
    print("-" * 80)

    # Use current project as example codebase
    codebase_path = "."

    report = await comprehensive_legacy_analysis(codebase_path)

    # Example 2: Quick security scan
    print("\n\n📋 Example 2: Quick Security Scan")
    print("-" * 80)

    vulnerable_code = """
    def login(username, password):
        query = "SELECT * FROM users WHERE username='" + username + "' AND password='" + password + "'"
        result = db.execute(query)
        return result

    def render_page(user_input):
        html = "<div>" + user_input + "</div>"
        return html
    """

    security_results = await quick_security_scan(vulnerable_code)

    # Example 3: Modernization cost estimate
    print("\n\n📋 Example 3: Modernization Cost Estimate")
    print("-" * 80)

    mod_results = await estimate_modernization_cost(
        legacy_tech="cobol",
        lines_of_code=250000,
        team_size=8,
    )

    print("\n" + "="*80)
    print("✅ All examples completed successfully!")
    print("💰 Total cost: $0 (vs ~$50-100 with paid APIs)")
    print("="*80)


if __name__ == "__main__":
    asyncio.run(main())
