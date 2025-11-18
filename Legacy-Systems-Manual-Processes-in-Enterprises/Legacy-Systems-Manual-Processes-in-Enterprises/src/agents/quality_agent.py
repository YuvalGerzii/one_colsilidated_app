"""
Code Quality Assessment Agent
Evaluates code quality, identifies issues, and suggests improvements
"""

import re
from typing import Dict, Any, List

from loguru import logger

from src.agents.framework import BaseAgent, AgentRole, AgentTask, AgentResult, AgentStatus


class CodeQualityAgent(BaseAgent):
    """
    Assesses code quality and identifies improvement opportunities.

    Capabilities:
    - Measure code complexity
    - Detect code smells
    - Identify duplicated code
    - Check naming conventions
    - Evaluate test coverage
    - Assess documentation quality
    """

    def __init__(self, agent_id: str = "code-quality"):
        """Initialize quality agent."""
        super().__init__(agent_id, AgentRole.ASSESSMENT)

        self.quality_metrics = {
            "complexity_thresholds": {
                "low": 10,
                "medium": 20,
                "high": 30,
            },
            "line_count_thresholds": {
                "function": 50,
                "class": 500,
                "file": 1000,
            },
        }

    def get_capabilities(self) -> List[str]:
        """Get agent capabilities."""
        return [
            "assess_quality",
            "measure_complexity",
            "detect_smells",
            "check_conventions",
            "evaluate_tests",
            "analyze_documentation",
        ]

    async def execute(self, task: AgentTask) -> AgentResult:
        """Execute quality assessment task."""
        self.status = AgentStatus.WORKING

        try:
            code = task.input_data.get("code", "")
            language = task.input_data.get("language", "unknown")

            assessment = await self._assess_code_quality(code, language)

            result = AgentResult(
                task_id=task.id,
                agent_id=self.agent_id,
                status=AgentStatus.COMPLETED,
                output=assessment,
                confidence=assessment.get("confidence", 0.8),
                reasoning="Comprehensive code quality analysis completed",
                recommendations=assessment.get("recommendations", []),
            )

            self.status = AgentStatus.IDLE
            return result

        except Exception as e:
            logger.error(f"Quality assessment failed: {e}")
            self.status = AgentStatus.FAILED

            return AgentResult(
                task_id=task.id,
                agent_id=self.agent_id,
                status=AgentStatus.FAILED,
                output={"error": str(e)},
            )

    async def _assess_code_quality(self, code: str, language: str) -> Dict[str, Any]:
        """Comprehensive code quality assessment."""

        assessment = {
            "language": language,
            "metrics": {},
            "issues": [],
            "code_smells": [],
            "recommendations": [],
            "overall_score": 0.0,
            "confidence": 0.85,
        }

        # Basic metrics
        lines = code.split('\n')
        assessment["metrics"]["total_lines"] = len(lines)
        assessment["metrics"]["code_lines"] = len([l for l in lines if l.strip() and not l.strip().startswith('#')])
        assessment["metrics"]["comment_lines"] = len([l for l in lines if l.strip().startswith('#')])
        assessment["metrics"]["blank_lines"] = len([l for l in lines if not l.strip()])

        # Complexity analysis
        complexity = self._calculate_complexity(code)
        assessment["metrics"]["complexity"] = complexity
        assessment["metrics"]["complexity_rating"] = self._rate_complexity(complexity)

        # Code smells detection
        smells = self._detect_code_smells(code, language)
        assessment["code_smells"] = smells

        # Issues detection
        issues = self._detect_issues(code, language)
        assessment["issues"] = issues

        # Documentation check
        doc_score = self._check_documentation(code, language)
        assessment["metrics"]["documentation_score"] = doc_score

        # Calculate overall score
        assessment["overall_score"] = self._calculate_overall_score(assessment)

        # AI-powered analysis
        ai_analysis = await self._ai_quality_analysis(code, assessment)
        assessment["ai_insights"] = ai_analysis

        # Generate recommendations
        assessment["recommendations"] = self._generate_quality_recommendations(assessment)

        return assessment

    def _calculate_complexity(self, code: str) -> int:
        """Calculate cyclomatic complexity."""
        complexity = 1  # Base complexity

        # Count decision points
        decision_keywords = ['if', 'elif', 'else', 'for', 'while', 'case', 'catch', '&&', '||', '?']

        for keyword in decision_keywords:
            complexity += len(re.findall(rf'\b{keyword}\b', code, re.IGNORECASE))

        return complexity

    def _rate_complexity(self, complexity: int) -> str:
        """Rate complexity level."""
        if complexity < self.quality_metrics["complexity_thresholds"]["low"]:
            return "low"
        elif complexity < self.quality_metrics["complexity_thresholds"]["medium"]:
            return "medium"
        elif complexity < self.quality_metrics["complexity_thresholds"]["high"]:
            return "high"
        else:
            return "very_high"

    def _detect_code_smells(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Detect common code smells."""
        smells = []

        # Long function detection
        functions = re.findall(r'(def|function|func)\s+\w+.*?(?=\n(?:def|function|func|class|$))', code, re.DOTALL)
        for i, func in enumerate(functions):
            if func.count('\n') > self.quality_metrics["line_count_thresholds"]["function"]:
                smells.append({
                    "type": "long_function",
                    "severity": "medium",
                    "description": f"Function {i+1} has {func.count(chr(10))} lines (limit: 50)",
                })

        # Magic numbers
        magic_numbers = re.findall(r'\b\d{2,}\b', code)
        if len(magic_numbers) > 10:
            smells.append({
                "type": "magic_numbers",
                "severity": "low",
                "description": f"Found {len(magic_numbers)} magic numbers - consider named constants",
            })

        # Deep nesting
        max_indent = max([len(line) - len(line.lstrip()) for line in code.split('\n')], default=0)
        if max_indent > 20:
            smells.append({
                "type": "deep_nesting",
                "severity": "high",
                "description": f"Maximum nesting level: {max_indent // 4} - consider refactoring",
            })

        # Duplicated code (simple check)
        lines = [l.strip() for l in code.split('\n') if l.strip()]
        duplicates = len(lines) - len(set(lines))
        if duplicates > len(lines) * 0.2:
            smells.append({
                "type": "code_duplication",
                "severity": "medium",
                "description": f"{duplicates} duplicated lines found - consider DRY principle",
            })

        return smells

    def _detect_issues(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Detect code issues."""
        issues = []

        # Security issues
        if 'eval(' in code:
            issues.append({
                "type": "security",
                "severity": "critical",
                "description": "Use of eval() detected - security risk",
            })

        if 'exec(' in code:
            issues.append({
                "type": "security",
                "severity": "critical",
                "description": "Use of exec() detected - security risk",
            })

        # SQL injection risk
        if re.search(r'SELECT.*\+.*FROM', code, re.IGNORECASE):
            issues.append({
                "type": "security",
                "severity": "high",
                "description": "Potential SQL injection vulnerability - use parameterized queries",
            })

        # Poor error handling
        try_blocks = len(re.findall(r'\btry\b', code))
        except_blocks = len(re.findall(r'\bexcept\b', code))
        if try_blocks > 0 and except_blocks == 0:
            issues.append({
                "type": "error_handling",
                "severity": "medium",
                "description": "Try block without except - incomplete error handling",
            })

        # Bare except
        if 'except:' in code:
            issues.append({
                "type": "error_handling",
                "severity": "medium",
                "description": "Bare except clause - catch specific exceptions",
            })

        return issues

    def _check_documentation(self, code: str, language: str) -> float:
        """Check documentation quality."""
        lines = code.split('\n')
        total_lines = len([l for l in lines if l.strip()])

        # Count docstrings and comments
        comment_lines = 0
        if language == "python":
            comment_lines = len(re.findall(r'(""".*?"""|\'\'\'.*?\'\'\'|#.*)', code, re.DOTALL))
        else:
            comment_lines = len(re.findall(r'(//.*|/\*.*?\*/)', code, re.DOTALL))

        doc_ratio = comment_lines / max(total_lines, 1)

        # Score based on documentation ratio
        if doc_ratio >= 0.2:
            return 1.0  # Excellent
        elif doc_ratio >= 0.1:
            return 0.7  # Good
        elif doc_ratio >= 0.05:
            return 0.4  # Fair
        else:
            return 0.1  # Poor

    def _calculate_overall_score(self, assessment: Dict[str, Any]) -> float:
        """Calculate overall quality score (0-10)."""
        score = 10.0

        # Deduct for complexity
        complexity_rating = assessment["metrics"]["complexity_rating"]
        if complexity_rating == "very_high":
            score -= 3.0
        elif complexity_rating == "high":
            score -= 2.0
        elif complexity_rating == "medium":
            score -= 1.0

        # Deduct for code smells
        score -= min(len(assessment["code_smells"]) * 0.5, 3.0)

        # Deduct for issues
        critical_issues = sum(1 for i in assessment["issues"] if i["severity"] == "critical")
        high_issues = sum(1 for i in assessment["issues"] if i["severity"] == "high")

        score -= critical_issues * 2.0
        score -= high_issues * 1.0

        # Add for documentation
        doc_score = assessment["metrics"]["documentation_score"]
        score += doc_score * 2.0

        return max(0.0, min(10.0, score))

    async def _ai_quality_analysis(self, code: str, assessment: Dict[str, Any]) -> str:
        """Use AI for deeper quality analysis."""

        # Limit code size for LLM
        code_snippet = code[:1000] if len(code) > 1000 else code

        prompt = f"""Analyze this code for quality:

```
{code_snippet}
```

Current metrics:
- Complexity: {assessment['metrics']['complexity']} ({assessment['metrics']['complexity_rating']})
- Code smells: {len(assessment['code_smells'])}
- Issues: {len(assessment['issues'])}
- Documentation score: {assessment['metrics']['documentation_score']}
- Overall score: {assessment['overall_score']}/10

Provide 3-5 specific, actionable improvement suggestions."""

        response = await self.analyze_with_llm(
            prompt,
            context="You are a code quality expert reviewing code for improvements.",
            max_tokens=500,
        )

        return response

    def _generate_quality_recommendations(self, assessment: Dict[str, Any]) -> List[str]:
        """Generate quality improvement recommendations."""
        recommendations = []

        # Based on overall score
        score = assessment["overall_score"]
        if score < 5.0:
            recommendations.append("⚠️ Code quality is below acceptable standards - consider major refactoring")
        elif score < 7.0:
            recommendations.append("Code quality needs improvement - address high-priority issues first")

        # Complexity
        if assessment["metrics"]["complexity_rating"] in ["high", "very_high"]:
            recommendations.append("Reduce complexity by breaking down large functions and removing nested conditionals")

        # Documentation
        if assessment["metrics"]["documentation_score"] < 0.5:
            recommendations.append("Improve documentation with docstrings and inline comments")

        # Code smells
        smell_types = {smell["type"] for smell in assessment["code_smells"]}
        if "long_function" in smell_types:
            recommendations.append("Extract long functions into smaller, focused functions")
        if "deep_nesting" in smell_types:
            recommendations.append("Reduce nesting depth using early returns and guard clauses")
        if "code_duplication" in smell_types:
            recommendations.append("Eliminate code duplication by creating reusable functions")

        # Security issues
        if any(issue["type"] == "security" for issue in assessment["issues"]):
            recommendations.append("🔒 Address security issues immediately - eval/exec usage and SQL injection risks")

        return recommendations
