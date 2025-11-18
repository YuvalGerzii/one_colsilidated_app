"""
Legacy Discovery Agent
Scans, catalogs, and maps legacy systems across the enterprise
"""

import os
from pathlib import Path
from typing import Dict, Any, List
import re

from loguru import logger

from src.agents.framework import BaseAgent, AgentRole, AgentTask, AgentResult, AgentStatus


class LegacyDiscoveryAgent(BaseAgent):
    """
    Discovers and catalogs legacy systems, technologies, and dependencies.

    Capabilities:
    - Scan codebases for legacy patterns
    - Identify technologies and frameworks
    - Map system dependencies
    - Detect obsolete libraries
    - Find hard-coded configurations
    - Identify integration points
    """

    def __init__(self, agent_id: str = "legacy-discovery"):
        """Initialize discovery agent."""
        super().__init__(agent_id, AgentRole.DISCOVERY)

        self.legacy_indicators = {
            "languages": {
                "cobol": [".cob", ".cbl", ".cpy"],
                "fortran": [".f", ".for", ".f90"],
                "vb6": [".vb", ".frm", ".bas"],
                "perl": [".pl", ".pm"],
                "asp_classic": [".asp"],
                "php4": ["<?php", "mysql_query"],
            },
            "frameworks": {
                "struts1": ["org.apache.struts"],
                "spring2": ["org.springframework", "version=\"2."],
                "hibernate3": ["org.hibernate", "version=\"3."],
                "jquery_old": ["jquery-1.", "jquery-2."],
            },
            "databases": {
                "access": [".mdb", ".accdb"],
                "foxpro": [".dbf"],
                "dbase": [".db"],
                "oracle8": ["Oracle8"],
            },
            "obsolete_patterns": [
                "eval(",  # Eval usage
                "document.write(",  # Old JS
                "innerHTML =",  # XSS risk
                "SELECT * FROM",  # Inefficient queries
                "mysql_query",  # Deprecated PHP
                "goto ",  # GOTO statements
            ],
        }

    def get_capabilities(self) -> List[str]:
        """Get agent capabilities."""
        return [
            "scan_codebase",
            "identify_technologies",
            "map_dependencies",
            "detect_legacy",
            "find_configurations",
            "analyze_integrations",
        ]

    async def execute(self, task: AgentTask) -> AgentResult:
        """Execute discovery task."""
        self.status = AgentStatus.WORKING

        try:
            if "scan" in task.type:
                output = await self._scan_codebase(task.input_data)
            elif "analyze" in task.type:
                output = await self._analyze_system(task.input_data)
            else:
                output = {"error": f"Unknown task type: {task.type}"}

            result = AgentResult(
                task_id=task.id,
                agent_id=self.agent_id,
                status=AgentStatus.COMPLETED,
                output=output,
                confidence=0.9,
                reasoning="Systematic codebase scan completed",
                recommendations=self._generate_recommendations(output),
            )

            self.status = AgentStatus.IDLE
            return result

        except Exception as e:
            logger.error(f"Discovery task failed: {e}")
            self.status = AgentStatus.FAILED

            return AgentResult(
                task_id=task.id,
                agent_id=self.agent_id,
                status=AgentStatus.FAILED,
                output={"error": str(e)},
            )

    async def _scan_codebase(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Scan codebase for legacy systems."""
        path = input_data.get("path", ".")

        logger.info(f"Scanning codebase at: {path}")

        findings = {
            "total_files": 0,
            "legacy_files": [],
            "technologies": {},
            "frameworks": {},
            "databases": [],
            "obsolete_patterns": [],
            "risk_level": "unknown",
        }

        # Scan directory
        if os.path.exists(path):
            for root, dirs, files in os.walk(path):
                # Skip common ignore directories
                dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', '__pycache__', 'venv'}]

                for file in files:
                    findings["total_files"] += 1
                    file_path = os.path.join(root, file)

                    # Check for legacy languages
                    for lang, extensions in self.legacy_indicators["languages"].items():
                        if any(file.endswith(ext) for ext in extensions if ext.startswith('.')):
                            findings["legacy_files"].append({
                                "path": file_path,
                                "language": lang,
                                "type": "file_extension",
                            })
                            findings["technologies"][lang] = findings["technologies"].get(lang, 0) + 1

                    # Check file content for patterns
                    if file.endswith(('.py', '.java', '.js', '.php', '.rb')):
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                self._scan_content(content, file_path, findings)
                        except Exception as e:
                            logger.debug(f"Could not read {file_path}: {e}")

        # Calculate risk level
        findings["risk_level"] = self._calculate_risk_level(findings)

        # Use LLM for deeper analysis
        if findings["legacy_files"]:
            summary = await self._ai_analyze_findings(findings)
            findings["ai_analysis"] = summary

        return findings

    def _scan_content(self, content: str, file_path: str, findings: Dict[str, Any]) -> None:
        """Scan file content for legacy patterns."""

        # Check for obsolete patterns
        for pattern in self.legacy_indicators["obsolete_patterns"]:
            if pattern in content:
                findings["obsolete_patterns"].append({
                    "file": file_path,
                    "pattern": pattern,
                })

        # Check for old frameworks
        for framework, indicators in self.legacy_indicators["frameworks"].items():
            if any(indicator in content for indicator in indicators):
                findings["frameworks"][framework] = findings["frameworks"].get(framework, 0) + 1

    def _calculate_risk_level(self, findings: Dict[str, Any]) -> str:
        """Calculate overall risk level."""
        legacy_ratio = len(findings["legacy_files"]) / max(findings["total_files"], 1)
        obsolete_count = len(findings["obsolete_patterns"])

        if legacy_ratio > 0.5 or obsolete_count > 50:
            return "critical"
        elif legacy_ratio > 0.3 or obsolete_count > 20:
            return "high"
        elif legacy_ratio > 0.1 or obsolete_count > 5:
            return "medium"
        else:
            return "low"

    async def _ai_analyze_findings(self, findings: Dict[str, Any]) -> str:
        """Use AI to analyze findings."""
        prompt = f"""Analyze this legacy system discovery report:

Total files scanned: {findings['total_files']}
Legacy files found: {len(findings['legacy_files'])}
Technologies: {findings['technologies']}
Obsolete patterns: {len(findings['obsolete_patterns'])}
Risk level: {findings['risk_level']}

Provide a concise analysis covering:
1. Main legacy concerns
2. Modernization priorities
3. Quick wins
4. Long-term strategy

Keep response under 200 words."""

        response = await self.analyze_with_llm(
            prompt,
            context="You are analyzing legacy systems for modernization.",
        )

        return response

    async def _analyze_system(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detailed system analysis."""
        system_type = input_data.get("type", "unknown")

        analysis = {
            "system_type": system_type,
            "age_estimate": "unknown",
            "modernization_difficulty": "unknown",
            "replacement_options": [],
        }

        # Use AI for analysis
        prompt = f"""Analyze this legacy system:
Type: {system_type}
Description: {input_data.get('description', 'Not provided')}

Provide analysis of:
1. Estimated age and technology generation
2. Modernization difficulty (easy/medium/hard)
3. Top 3 replacement/modernization options
4. Main risks of keeping it as-is"""

        response = await self.analyze_with_llm(prompt)
        analysis["ai_recommendation"] = response

        return analysis

    def _generate_recommendations(self, output: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on findings."""
        recommendations = []

        if output.get("risk_level") == "critical":
            recommendations.append("⚠️ URGENT: Immediate modernization planning required")
            recommendations.append("Consider parallel development of replacement system")

        if output.get("risk_level") in ["critical", "high"]:
            recommendations.append("Prioritize security audit for legacy components")
            recommendations.append("Implement comprehensive monitoring")

        if output.get("obsolete_patterns"):
            recommendations.append(f"Found {len(output['obsolete_patterns'])} obsolete code patterns - review and refactor")

        if output.get("technologies"):
            recommendations.append("Create technology inventory for stakeholders")
            recommendations.append("Estimate licensing and support costs for legacy tech")

        recommendations.append("Schedule knowledge transfer sessions with team members familiar with legacy systems")

        return recommendations
