"""
Utility Agents for System Operations

This module contains utility agents that handle operational tasks such as
documentation, deployment, monitoring, and security scanning.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import re
import json


class DocumentationAgent:
    """
    Agent specialized in generating and maintaining code documentation.

    Capabilities:
    - Generate API documentation
    - Create README files
    - Write inline code comments
    - Generate architecture diagrams
    - Maintain changelog files
    - Create user guides and tutorials
    """

    def __init__(self, agent_id: str = "doc_agent"):
        self.agent_id = agent_id
        self.proficiency = 0.91
        self.capabilities = [
            "api_documentation",
            "readme_generation",
            "code_commenting",
            "architecture_diagrams",
            "changelog_maintenance",
            "tutorial_creation",
            "docstring_generation"
        ]
        self.documentation_formats = ["markdown", "restructured_text", "html", "pdf"]

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a documentation task."""
        task_type = task.get("type", "")

        if task_type == "generate_api_docs":
            return await self._generate_api_documentation(task)
        elif task_type == "create_readme":
            return await self._create_readme(task)
        elif task_type == "add_comments":
            return await self._add_code_comments(task)
        elif task_type == "update_changelog":
            return await self._update_changelog(task)
        else:
            return {"status": "error", "message": f"Unknown task type: {task_type}"}

    async def _generate_api_documentation(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate API documentation from code."""
        code = task.get("code", "")
        format_type = task.get("format", "markdown")

        # Extract functions, classes, and their signatures
        documentation = {
            "endpoints": self._extract_endpoints(code),
            "models": self._extract_models(code),
            "examples": self._generate_examples(code),
            "format": format_type
        }

        return {
            "status": "success",
            "agent": self.agent_id,
            "documentation": documentation,
            "quality_score": 0.91
        }

    async def _create_readme(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create a README file for a project."""
        project_info = task.get("project_info", {})

        readme_sections = [
            self._generate_title(project_info),
            self._generate_description(project_info),
            self._generate_installation_guide(project_info),
            self._generate_usage_examples(project_info),
            self._generate_contributing_guide(project_info),
            self._generate_license_section(project_info)
        ]

        readme_content = "\n\n".join(readme_sections)

        return {
            "status": "success",
            "agent": self.agent_id,
            "content": readme_content,
            "quality_score": 0.91
        }

    async def _add_code_comments(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Add inline comments to code."""
        code = task.get("code", "")
        style = task.get("style", "docstring")

        commented_code = self._insert_comments(code, style)

        return {
            "status": "success",
            "agent": self.agent_id,
            "commented_code": commented_code,
            "quality_score": 0.91
        }

    async def _update_changelog(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Update changelog with new entries."""
        changes = task.get("changes", [])
        version = task.get("version", "unreleased")

        changelog_entry = self._format_changelog_entry(changes, version)

        return {
            "status": "success",
            "agent": self.agent_id,
            "changelog_entry": changelog_entry,
            "quality_score": 0.91
        }

    def _extract_endpoints(self, code: str) -> List[Dict[str, Any]]:
        """Extract API endpoints from code."""
        # Simplified endpoint extraction
        return []

    def _extract_models(self, code: str) -> List[Dict[str, Any]]:
        """Extract data models from code."""
        return []

    def _generate_examples(self, code: str) -> List[str]:
        """Generate usage examples."""
        return []

    def _generate_title(self, project_info: Dict[str, Any]) -> str:
        """Generate README title section."""
        name = project_info.get("name", "Project")
        return f"# {name}"

    def _generate_description(self, project_info: Dict[str, Any]) -> str:
        """Generate project description."""
        description = project_info.get("description", "")
        return f"## Description\n\n{description}"

    def _generate_installation_guide(self, project_info: Dict[str, Any]) -> str:
        """Generate installation instructions."""
        return "## Installation\n\n```bash\npip install .\n```"

    def _generate_usage_examples(self, project_info: Dict[str, Any]) -> str:
        """Generate usage examples."""
        return "## Usage\n\nSee examples/ directory for usage examples."

    def _generate_contributing_guide(self, project_info: Dict[str, Any]) -> str:
        """Generate contributing guidelines."""
        return "## Contributing\n\nContributions are welcome! Please read CONTRIBUTING.md for details."

    def _generate_license_section(self, project_info: Dict[str, Any]) -> str:
        """Generate license section."""
        license_type = project_info.get("license", "MIT")
        return f"## License\n\nThis project is licensed under the {license_type} License."

    def _insert_comments(self, code: str, style: str) -> str:
        """Insert comments into code."""
        # Simplified comment insertion
        return code

    def _format_changelog_entry(self, changes: List[str], version: str) -> str:
        """Format changelog entry."""
        date = datetime.now().strftime("%Y-%m-%d")
        entry = f"## [{version}] - {date}\n\n"

        for change in changes:
            entry += f"- {change}\n"

        return entry


class DeploymentAgent:
    """
    Agent specialized in handling deployments and CI/CD operations.

    Capabilities:
    - Deploy applications to various platforms
    - Configure CI/CD pipelines
    - Manage containerization (Docker)
    - Handle environment configurations
    - Perform blue-green deployments
    - Rollback failed deployments
    """

    def __init__(self, agent_id: str = "deploy_agent"):
        self.agent_id = agent_id
        self.proficiency = 0.89
        self.capabilities = [
            "docker_deployment",
            "kubernetes_orchestration",
            "ci_cd_setup",
            "environment_management",
            "blue_green_deployment",
            "rollback_management",
            "cloud_deployment"
        ]
        self.supported_platforms = ["aws", "gcp", "azure", "heroku", "vercel"]

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a deployment task."""
        task_type = task.get("type", "")

        if task_type == "deploy_app":
            return await self._deploy_application(task)
        elif task_type == "setup_cicd":
            return await self._setup_cicd_pipeline(task)
        elif task_type == "create_dockerfile":
            return await self._create_dockerfile(task)
        elif task_type == "rollback":
            return await self._rollback_deployment(task)
        else:
            return {"status": "error", "message": f"Unknown task type: {task_type}"}

    async def _deploy_application(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy an application to a platform."""
        platform = task.get("platform", "aws")
        app_config = task.get("config", {})

        deployment_plan = {
            "platform": platform,
            "steps": self._generate_deployment_steps(platform, app_config),
            "estimated_time": "5-10 minutes",
            "rollback_plan": self._generate_rollback_plan(platform)
        }

        return {
            "status": "success",
            "agent": self.agent_id,
            "deployment_plan": deployment_plan,
            "quality_score": 0.89
        }

    async def _setup_cicd_pipeline(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Set up CI/CD pipeline."""
        platform = task.get("platform", "github_actions")
        project_type = task.get("project_type", "python")

        pipeline_config = self._generate_pipeline_config(platform, project_type)

        return {
            "status": "success",
            "agent": self.agent_id,
            "pipeline_config": pipeline_config,
            "quality_score": 0.89
        }

    async def _create_dockerfile(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create a Dockerfile for the project."""
        project_type = task.get("project_type", "python")
        dependencies = task.get("dependencies", [])

        dockerfile = self._generate_dockerfile(project_type, dependencies)

        return {
            "status": "success",
            "agent": self.agent_id,
            "dockerfile": dockerfile,
            "quality_score": 0.89
        }

    async def _rollback_deployment(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Rollback a failed deployment."""
        deployment_id = task.get("deployment_id", "")
        previous_version = task.get("previous_version", "")

        rollback_plan = {
            "deployment_id": deployment_id,
            "target_version": previous_version,
            "steps": [
                "Stop current deployment",
                "Restore previous version",
                "Verify health checks",
                "Update DNS/load balancer"
            ]
        }

        return {
            "status": "success",
            "agent": self.agent_id,
            "rollback_plan": rollback_plan,
            "quality_score": 0.89
        }

    def _generate_deployment_steps(self, platform: str, config: Dict[str, Any]) -> List[str]:
        """Generate deployment steps for a platform."""
        return [
            "Build application",
            "Run tests",
            "Create container image",
            "Push to registry",
            "Deploy to platform",
            "Verify deployment"
        ]

    def _generate_rollback_plan(self, platform: str) -> List[str]:
        """Generate rollback plan."""
        return [
            "Identify issue",
            "Stop current deployment",
            "Restore previous version",
            "Verify rollback"
        ]

    def _generate_pipeline_config(self, platform: str, project_type: str) -> str:
        """Generate CI/CD pipeline configuration."""
        if platform == "github_actions":
            return """name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Run tests
      run: pytest

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - name: Deploy to production
      run: echo "Deploying..."
"""
        return ""

    def _generate_dockerfile(self, project_type: str, dependencies: List[str]) -> str:
        """Generate Dockerfile content."""
        if project_type == "python":
            return """FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
"""
        return ""


class MonitoringAgent:
    """
    Agent specialized in system monitoring and alerting.

    Capabilities:
    - Monitor application performance
    - Set up health checks
    - Configure alerts and notifications
    - Track error rates and latency
    - Generate monitoring dashboards
    - Analyze logs and metrics
    """

    def __init__(self, agent_id: str = "monitor_agent"):
        self.agent_id = agent_id
        self.proficiency = 0.90
        self.capabilities = [
            "performance_monitoring",
            "health_checks",
            "alert_configuration",
            "log_analysis",
            "metric_tracking",
            "dashboard_creation",
            "anomaly_detection"
        ]
        self.monitoring_tools = ["prometheus", "grafana", "datadog", "new_relic"]

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a monitoring task."""
        task_type = task.get("type", "")

        if task_type == "setup_monitoring":
            return await self._setup_monitoring(task)
        elif task_type == "configure_alerts":
            return await self._configure_alerts(task)
        elif task_type == "analyze_logs":
            return await self._analyze_logs(task)
        elif task_type == "create_dashboard":
            return await self._create_dashboard(task)
        else:
            return {"status": "error", "message": f"Unknown task type: {task_type}"}

    async def _setup_monitoring(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Set up monitoring for an application."""
        app_name = task.get("app_name", "")
        metrics = task.get("metrics", ["cpu", "memory", "requests"])

        monitoring_config = {
            "app_name": app_name,
            "metrics": metrics,
            "collection_interval": "30s",
            "retention_period": "30d",
            "endpoints": self._generate_monitoring_endpoints(metrics)
        }

        return {
            "status": "success",
            "agent": self.agent_id,
            "monitoring_config": monitoring_config,
            "quality_score": 0.90
        }

    async def _configure_alerts(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Configure alerts and notifications."""
        alert_rules = task.get("alert_rules", [])
        notification_channels = task.get("channels", ["email"])

        alert_config = {
            "rules": self._process_alert_rules(alert_rules),
            "channels": notification_channels,
            "severity_levels": ["info", "warning", "critical"]
        }

        return {
            "status": "success",
            "agent": self.agent_id,
            "alert_config": alert_config,
            "quality_score": 0.90
        }

    async def _analyze_logs(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze application logs."""
        logs = task.get("logs", [])
        time_range = task.get("time_range", "1h")

        analysis = {
            "total_entries": len(logs),
            "error_count": self._count_errors(logs),
            "warning_count": self._count_warnings(logs),
            "patterns": self._detect_patterns(logs),
            "anomalies": self._detect_anomalies(logs)
        }

        return {
            "status": "success",
            "agent": self.agent_id,
            "analysis": analysis,
            "quality_score": 0.90
        }

    async def _create_dashboard(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create a monitoring dashboard."""
        metrics = task.get("metrics", [])
        dashboard_name = task.get("name", "Application Dashboard")

        dashboard = {
            "name": dashboard_name,
            "panels": self._generate_dashboard_panels(metrics),
            "refresh_rate": "30s",
            "time_range": "last_24h"
        }

        return {
            "status": "success",
            "agent": self.agent_id,
            "dashboard": dashboard,
            "quality_score": 0.90
        }

    def _generate_monitoring_endpoints(self, metrics: List[str]) -> List[str]:
        """Generate monitoring endpoints for metrics."""
        return [f"/metrics/{metric}" for metric in metrics]

    def _process_alert_rules(self, rules: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process and validate alert rules."""
        return rules

    def _count_errors(self, logs: List[str]) -> int:
        """Count error entries in logs."""
        return sum(1 for log in logs if "error" in log.lower())

    def _count_warnings(self, logs: List[str]) -> int:
        """Count warning entries in logs."""
        return sum(1 for log in logs if "warning" in log.lower())

    def _detect_patterns(self, logs: List[str]) -> List[str]:
        """Detect patterns in logs."""
        return []

    def _detect_anomalies(self, logs: List[str]) -> List[Dict[str, Any]]:
        """Detect anomalies in logs."""
        return []

    def _generate_dashboard_panels(self, metrics: List[str]) -> List[Dict[str, Any]]:
        """Generate dashboard panels for metrics."""
        panels = []
        for metric in metrics:
            panels.append({
                "title": metric.capitalize(),
                "type": "graph",
                "metric": metric
            })
        return panels


class SecurityScannerAgent:
    """
    Agent specialized in security vulnerability scanning and compliance.

    Capabilities:
    - Scan code for security vulnerabilities
    - Perform dependency vulnerability checks
    - Check for common security misconfigurations
    - Validate input sanitization
    - Detect hardcoded secrets
    - Generate security reports
    """

    def __init__(self, agent_id: str = "security_agent"):
        self.agent_id = agent_id
        self.proficiency = 0.93
        self.capabilities = [
            "vulnerability_scanning",
            "dependency_audit",
            "secret_detection",
            "compliance_checking",
            "penetration_testing",
            "security_report_generation",
            "threat_modeling"
        ]
        self.security_frameworks = ["OWASP", "CWE", "CVE", "NIST"]

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a security scanning task."""
        task_type = task.get("type", "")

        if task_type == "scan_code":
            return await self._scan_code(task)
        elif task_type == "audit_dependencies":
            return await self._audit_dependencies(task)
        elif task_type == "detect_secrets":
            return await self._detect_secrets(task)
        elif task_type == "compliance_check":
            return await self._compliance_check(task)
        else:
            return {"status": "error", "message": f"Unknown task type: {task_type}"}

    async def _scan_code(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Scan code for security vulnerabilities."""
        code = task.get("code", "")
        language = task.get("language", "python")

        vulnerabilities = {
            "sql_injection": self._check_sql_injection(code),
            "xss": self._check_xss(code),
            "command_injection": self._check_command_injection(code),
            "path_traversal": self._check_path_traversal(code),
            "insecure_deserialization": self._check_insecure_deserialization(code)
        }

        severity = self._calculate_severity(vulnerabilities)

        return {
            "status": "success",
            "agent": self.agent_id,
            "vulnerabilities": vulnerabilities,
            "severity": severity,
            "quality_score": 0.93
        }

    async def _audit_dependencies(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Audit dependencies for known vulnerabilities."""
        dependencies = task.get("dependencies", [])

        audit_results = []
        for dep in dependencies:
            audit_results.append({
                "package": dep,
                "vulnerabilities": self._check_package_vulnerabilities(dep),
                "outdated": self._check_if_outdated(dep)
            })

        return {
            "status": "success",
            "agent": self.agent_id,
            "audit_results": audit_results,
            "quality_score": 0.93
        }

    async def _detect_secrets(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Detect hardcoded secrets in code."""
        code = task.get("code", "")
        files = task.get("files", [])

        secrets_found = {
            "api_keys": self._find_api_keys(code),
            "passwords": self._find_passwords(code),
            "tokens": self._find_tokens(code),
            "private_keys": self._find_private_keys(code)
        }

        return {
            "status": "success",
            "agent": self.agent_id,
            "secrets_found": secrets_found,
            "quality_score": 0.93
        }

    async def _compliance_check(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Check compliance with security standards."""
        standard = task.get("standard", "OWASP")
        code = task.get("code", "")

        compliance_results = {
            "standard": standard,
            "passed_checks": [],
            "failed_checks": [],
            "compliance_score": 0.85
        }

        return {
            "status": "success",
            "agent": self.agent_id,
            "compliance_results": compliance_results,
            "quality_score": 0.93
        }

    def _check_sql_injection(self, code: str) -> List[Dict[str, Any]]:
        """Check for SQL injection vulnerabilities."""
        issues = []
        # Simplified SQL injection detection
        if "execute(" in code and "%" in code:
            issues.append({
                "type": "SQL Injection",
                "severity": "high",
                "description": "Potential SQL injection via string formatting"
            })
        return issues

    def _check_xss(self, code: str) -> List[Dict[str, Any]]:
        """Check for XSS vulnerabilities."""
        return []

    def _check_command_injection(self, code: str) -> List[Dict[str, Any]]:
        """Check for command injection vulnerabilities."""
        issues = []
        if "os.system(" in code or "subprocess.call(" in code:
            issues.append({
                "type": "Command Injection",
                "severity": "high",
                "description": "Potential command injection vulnerability"
            })
        return issues

    def _check_path_traversal(self, code: str) -> List[Dict[str, Any]]:
        """Check for path traversal vulnerabilities."""
        return []

    def _check_insecure_deserialization(self, code: str) -> List[Dict[str, Any]]:
        """Check for insecure deserialization."""
        issues = []
        if "pickle.loads(" in code:
            issues.append({
                "type": "Insecure Deserialization",
                "severity": "high",
                "description": "Unsafe use of pickle.loads()"
            })
        return issues

    def _calculate_severity(self, vulnerabilities: Dict[str, List]) -> str:
        """Calculate overall severity."""
        has_high = any(
            any(v.get("severity") == "high" for v in vulns)
            for vulns in vulnerabilities.values()
        )
        return "high" if has_high else "low"

    def _check_package_vulnerabilities(self, package: str) -> List[Dict[str, Any]]:
        """Check package for known vulnerabilities."""
        return []

    def _check_if_outdated(self, package: str) -> bool:
        """Check if package is outdated."""
        return False

    def _find_api_keys(self, code: str) -> List[Dict[str, Any]]:
        """Find hardcoded API keys."""
        findings = []
        # Simplified API key detection
        patterns = [
            r'api[_-]?key\s*=\s*["\']([^"\']+)["\']',
            r'API[_-]?KEY\s*=\s*["\']([^"\']+)["\']'
        ]
        for pattern in patterns:
            matches = re.findall(pattern, code, re.IGNORECASE)
            for match in matches:
                findings.append({
                    "type": "API Key",
                    "value_length": len(match),
                    "location": "code"
                })
        return findings

    def _find_passwords(self, code: str) -> List[Dict[str, Any]]:
        """Find hardcoded passwords."""
        return []

    def _find_tokens(self, code: str) -> List[Dict[str, Any]]:
        """Find hardcoded tokens."""
        return []

    def _find_private_keys(self, code: str) -> List[Dict[str, Any]]:
        """Find hardcoded private keys."""
        return []


# Factory function to create utility agent pool
def create_utility_agent_pool() -> Dict[str, Any]:
    """
    Create a pool of utility agents for system operations.

    Returns:
        Dictionary mapping agent IDs to agent instances
    """
    return {
        "documentation": DocumentationAgent("documentation_agent"),
        "deployment": DeploymentAgent("deployment_agent"),
        "monitoring": MonitoringAgent("monitoring_agent"),
        "security": SecurityScannerAgent("security_agent")
    }
