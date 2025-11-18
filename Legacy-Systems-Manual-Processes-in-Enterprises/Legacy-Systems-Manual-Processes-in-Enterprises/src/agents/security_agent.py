"""
Security Auditor Agent
Identifies security vulnerabilities and compliance issues in legacy systems
"""

import re
from typing import Dict, Any, List

from loguru import logger

from src.agents.framework import BaseAgent, AgentRole, AgentTask, AgentResult, AgentStatus


class SecurityAuditorAgent(BaseAgent):
    """
    Audits code and systems for security vulnerabilities.

    Capabilities:
    - Identify common vulnerabilities (OWASP Top 10)
    - Detect hardcoded credentials
    - Find SQL injection risks
    - Identify XSS vulnerabilities
    - Check for outdated dependencies
    - Assess encryption practices
    """

    def __init__(self, agent_id: str = "security-auditor"):
        """Initialize security auditor."""
        super().__init__(agent_id, AgentRole.ASSESSMENT)

        self.vulnerability_patterns = {
            "sql_injection": [
                r"SELECT.*\+.*FROM",
                r"INSERT.*\+.*VALUES",
                r"UPDATE.*\+.*SET",
                r"DELETE.*\+.*WHERE",
                r"execute\(.*\+.*\)",
            ],
            "xss": [
                r"innerHTML\s*=",
                r"document\.write\(",
                r"eval\(",
                r"\.html\(.*\+",
            ],
            "command_injection": [
                r"os\.system\(",
                r"subprocess\.call\(.*shell=True",
                r"exec\(",
                r"eval\(",
            ],
            "hardcoded_credentials": [
                r"password\s*=\s*['\"][^'\"]{3,}['\"]",
                r"api[_-]?key\s*=\s*['\"][^'\"]{10,}['\"]",
                r"secret\s*=\s*['\"][^'\"]{10,}['\"]",
                r"token\s*=\s*['\"][^'\"]{10,}['\"]",
            ],
            "weak_crypto": [
                r"MD5\(",
                r"SHA1\(",
                r"DES\(",
                r"ECB",
            ],
            "insecure_deserialization": [
                r"pickle\.loads\(",
                r"yaml\.load\(",
                r"__reduce__",
            ],
        }

        self.owasp_categories = [
            "A01:2021-Broken Access Control",
            "A02:2021-Cryptographic Failures",
            "A03:2021-Injection",
            "A04:2021-Insecure Design",
            "A05:2021-Security Misconfiguration",
            "A06:2021-Vulnerable Components",
            "A07:2021-Identification and Authentication Failures",
            "A08:2021-Software and Data Integrity Failures",
            "A09:2021-Security Logging and Monitoring Failures",
            "A10:2021-Server-Side Request Forgery",
        ]

    def get_capabilities(self) -> List[str]:
        """Get agent capabilities."""
        return [
            "scan_vulnerabilities",
            "audit_security",
            "check_compliance",
            "assess_risk",
            "generate_report",
            "recommend_fixes",
        ]

    async def execute(self, task: AgentTask) -> AgentResult:
        """Execute security audit."""
        self.status = AgentStatus.WORKING

        try:
            audit_report = await self._perform_security_audit(task.input_data)

            # Calculate confidence based on thoroughness
            confidence = 0.95 if len(audit_report["vulnerabilities"]) > 0 else 0.80

            result = AgentResult(
                task_id=task.id,
                agent_id=self.agent_id,
                status=AgentStatus.COMPLETED,
                output=audit_report,
                confidence=confidence,
                reasoning="Comprehensive security audit completed",
                recommendations=audit_report.get("recommendations", []),
                next_steps=audit_report.get("remediation_steps", []),
            )

            self.status = AgentStatus.IDLE
            return result

        except Exception as e:
            logger.error(f"Security audit failed: {e}")
            self.status = AgentStatus.FAILED

            return AgentResult(
                task_id=task.id,
                agent_id=self.agent_id,
                status=AgentStatus.FAILED,
                output={"error": str(e)},
            )

    async def _perform_security_audit(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive security audit."""

        code = input_data.get("code", "")
        dependencies = input_data.get("dependencies", [])
        system_config = input_data.get("configuration", {})

        audit_report = {
            "vulnerabilities": [],
            "severity_summary": {
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0,
            },
            "owasp_mapping": {},
            "compliance_issues": [],
            "recommendations": [],
            "remediation_steps": [],
            "risk_score": 0.0,
        }

        # Scan for vulnerabilities
        vulns = self._scan_for_vulnerabilities(code)
        audit_report["vulnerabilities"] = vulns

        # Count by severity
        for vuln in vulns:
            severity = vuln["severity"]
            audit_report["severity_summary"][severity] += 1

        # Map to OWASP categories
        audit_report["owasp_mapping"] = self._map_to_owasp(vulns)

        # Check dependencies for known vulnerabilities
        dep_issues = self._check_dependencies(dependencies)
        audit_report["vulnerabilities"].extend(dep_issues)

        # Check configuration
        config_issues = self._check_configuration(system_config)
        audit_report["compliance_issues"] = config_issues

        # Calculate risk score
        audit_report["risk_score"] = self._calculate_risk_score(audit_report)

        # AI-powered analysis
        ai_analysis = await self._ai_security_analysis(audit_report)
        audit_report["ai_analysis"] = ai_analysis

        # Generate recommendations
        audit_report["recommendations"] = self._generate_security_recommendations(audit_report)
        audit_report["remediation_steps"] = self._generate_remediation_steps(audit_report)

        return audit_report

    def _scan_for_vulnerabilities(self, code: str) -> List[Dict[str, Any]]:
        """Scan code for security vulnerabilities."""

        vulnerabilities = []

        for vuln_type, patterns in self.vulnerability_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, code, re.IGNORECASE)

                for match in matches:
                    # Get line number
                    line_num = code[:match.start()].count('\n') + 1

                    # Get surrounding context
                    lines = code.split('\n')
                    context_start = max(0, line_num - 2)
                    context_end = min(len(lines), line_num + 2)
                    context = '\n'.join(lines[context_start:context_end])

                    # Determine severity
                    severity = self._determine_severity(vuln_type)

                    vulnerabilities.append({
                        "type": vuln_type,
                        "severity": severity,
                        "line": line_num,
                        "pattern": pattern,
                        "code_snippet": match.group(0),
                        "context": context,
                        "description": self._get_vulnerability_description(vuln_type),
                        "cwe": self._get_cwe(vuln_type),
                    })

        return vulnerabilities

    def _determine_severity(self, vuln_type: str) -> str:
        """Determine vulnerability severity."""

        severity_map = {
            "sql_injection": "critical",
            "command_injection": "critical",
            "hardcoded_credentials": "critical",
            "xss": "high",
            "insecure_deserialization": "high",
            "weak_crypto": "medium",
        }

        return severity_map.get(vuln_type, "medium")

    def _get_vulnerability_description(self, vuln_type: str) -> str:
        """Get description of vulnerability."""

        descriptions = {
            "sql_injection": "SQL injection vulnerability - user input not properly sanitized in database queries",
            "xss": "Cross-site scripting (XSS) vulnerability - user input rendered without encoding",
            "command_injection": "Command injection vulnerability - user input executed as system commands",
            "hardcoded_credentials": "Hardcoded credentials found - secrets should be stored in secure vault",
            "weak_crypto": "Weak cryptographic algorithm - use modern algorithms (SHA-256, AES-256)",
            "insecure_deserialization": "Insecure deserialization - untrusted data being deserialized",
        }

        return descriptions.get(vuln_type, "Security vulnerability detected")

    def _get_cwe(self, vuln_type: str) -> str:
        """Get CWE (Common Weakness Enumeration) number."""

        cwe_map = {
            "sql_injection": "CWE-89",
            "xss": "CWE-79",
            "command_injection": "CWE-78",
            "hardcoded_credentials": "CWE-798",
            "weak_crypto": "CWE-327",
            "insecure_deserialization": "CWE-502",
        }

        return cwe_map.get(vuln_type, "CWE-unknown")

    def _map_to_owasp(self, vulnerabilities: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Map vulnerabilities to OWASP Top 10 categories."""

        owasp_mapping = {}

        owasp_map = {
            "sql_injection": "A03:2021-Injection",
            "xss": "A03:2021-Injection",
            "command_injection": "A03:2021-Injection",
            "hardcoded_credentials": "A07:2021-Identification and Authentication Failures",
            "weak_crypto": "A02:2021-Cryptographic Failures",
            "insecure_deserialization": "A08:2021-Software and Data Integrity Failures",
        }

        for vuln in vulnerabilities:
            vuln_type = vuln["type"]
            owasp_cat = owasp_map.get(vuln_type, "Other")

            if owasp_cat not in owasp_mapping:
                owasp_mapping[owasp_cat] = []

            owasp_mapping[owasp_cat].append(vuln_type)

        return owasp_mapping

    def _check_dependencies(self, dependencies: List[str]) -> List[Dict[str, Any]]:
        """Check dependencies for known vulnerabilities."""

        issues = []

        # Known vulnerable versions (simplified - in production, use CVE database)
        known_vulns = {
            "django==1.11": {"severity": "critical", "cve": "CVE-2019-19844"},
            "flask<1.0": {"severity": "high", "cve": "CVE-2018-1000656"},
            "requests<2.20.0": {"severity": "medium", "cve": "CVE-2018-18074"},
            "pyyaml<5.4": {"severity": "high", "cve": "CVE-2020-14343"},
        }

        for dep in dependencies:
            for vuln_dep, vuln_info in known_vulns.items():
                if vuln_dep in dep.lower():
                    issues.append({
                        "type": "vulnerable_dependency",
                        "severity": vuln_info["severity"],
                        "dependency": dep,
                        "cve": vuln_info["cve"],
                        "description": f"Vulnerable dependency: {dep}",
                    })

        return issues

    def _check_configuration(self, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check configuration for security issues."""

        issues = []

        # Check for insecure configurations
        if config.get("debug", False):
            issues.append({
                "type": "debug_mode_enabled",
                "severity": "high",
                "description": "Debug mode enabled in production - exposes sensitive information",
            })

        if not config.get("ssl_enabled", True):
            issues.append({
                "type": "ssl_disabled",
                "severity": "critical",
                "description": "SSL/TLS not enforced - data transmitted in cleartext",
            })

        if config.get("allow_all_cors", False):
            issues.append({
                "type": "permissive_cors",
                "severity": "medium",
                "description": "CORS allows all origins - potential security risk",
            })

        return issues

    def _calculate_risk_score(self, audit_report: Dict[str, Any]) -> float:
        """Calculate overall security risk score (0-10, higher is worse)."""

        severity_weights = {
            "critical": 10.0,
            "high": 5.0,
            "medium": 2.0,
            "low": 0.5,
        }

        score = 0.0
        for severity, count in audit_report["severity_summary"].items():
            score += severity_weights[severity] * count

        # Normalize to 0-10 scale
        return min(10.0, score / 5)

    async def _ai_security_analysis(self, audit_report: Dict[str, Any]) -> str:
        """Use AI for security analysis insights."""

        vulns = audit_report["vulnerabilities"][:5]  # Top 5

        prompt = f"""Security audit analysis:

Vulnerabilities found: {len(audit_report['vulnerabilities'])}
- Critical: {audit_report['severity_summary']['critical']}
- High: {audit_report['severity_summary']['high']}
- Medium: {audit_report['severity_summary']['medium']}

Top issues:
{chr(10).join(f"- {v['type']}: {v['description']}" for v in vulns)}

Risk score: {audit_report['risk_score']}/10

Provide:
1. Overall security posture assessment
2. Most critical issue to fix first
3. Long-term security strategy recommendation

Keep under 150 words."""

        response = await self.analyze_with_llm(
            prompt,
            context="You are a cybersecurity expert analyzing application security.",
        )

        return response

    def _generate_security_recommendations(self, audit_report: Dict[str, Any]) -> List[str]:
        """Generate security recommendations."""

        recommendations = []

        # Based on risk score
        risk_score = audit_report["risk_score"]
        if risk_score >= 7:
            recommendations.append("🔴 CRITICAL: Severe security issues detected - immediate action required")
            recommendations.append("Do not deploy to production until critical issues are resolved")
        elif risk_score >= 4:
            recommendations.append("⚠️ HIGH RISK: Significant security concerns - prioritize remediation")

        # Based on vulnerabilities
        critical_count = audit_report["severity_summary"]["critical"]
        if critical_count > 0:
            recommendations.append(f"Fix {critical_count} critical vulnerabilities immediately")

        # Specific recommendations
        vuln_types = {v["type"] for v in audit_report["vulnerabilities"]}

        if "sql_injection" in vuln_types:
            recommendations.append("Use parameterized queries or ORM to prevent SQL injection")

        if "hardcoded_credentials" in vuln_types:
            recommendations.append("Move credentials to environment variables or secure vault (e.g., HashiCorp Vault)")

        if "weak_crypto" in vuln_types:
            recommendations.append("Upgrade to modern cryptographic algorithms (SHA-256+, AES-256)")

        if "xss" in vuln_types:
            recommendations.append("Implement proper output encoding and Content Security Policy (CSP)")

        # General recommendations
        recommendations.extend([
            "Implement automated security scanning in CI/CD pipeline",
            "Regular dependency updates to patch known vulnerabilities",
            "Security training for development team",
            "Implement Web Application Firewall (WAF)",
        ])

        return recommendations

    def _generate_remediation_steps(self, audit_report: Dict[str, Any]) -> List[str]:
        """Generate specific remediation steps."""

        steps = []

        # Prioritize critical issues
        critical_vulns = [
            v for v in audit_report["vulnerabilities"]
            if v["severity"] == "critical"
        ]

        for i, vuln in enumerate(critical_vulns[:3], 1):  # Top 3
            steps.append(
                f"{i}. Fix {vuln['type']} at line {vuln.get('line', 'unknown')}: {vuln['description']}"
            )

        # Add systematic steps
        steps.extend([
            f"{len(critical_vulns[:3]) + 1}. Review and update all dependencies",
            f"{len(critical_vulns[:3]) + 2}. Enable security headers (CSP, HSTS, X-Frame-Options)",
            f"{len(critical_vulns[:3]) + 3}. Implement security logging and monitoring",
            f"{len(critical_vulns[:3]) + 4}. Schedule penetration testing",
        ])

        return steps
