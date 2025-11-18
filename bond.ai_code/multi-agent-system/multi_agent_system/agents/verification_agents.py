"""
Quality Verification and Delivery Validation Agents.

These agents verify the quality and delivery of work from other agents:
- Quality Verifiers: Check accuracy, completeness, source quality
- Delivery Validators: Ensure proper format, structure, usability

Based on Anthropic's multi-layered evaluation approach.
"""

import asyncio
from typing import Any, Dict, List, Optional
from loguru import logger
import re
import json

from multi_agent_system.agents.base import BaseAgent
from multi_agent_system.core.types import (
    Task,
    Result,
    AgentCapability,
)


class QualityVerifierAgent(BaseAgent):
    """
    Verifies the quality of agent outputs.

    Checks:
    - Factual accuracy (consistency, logic)
    - Completeness (all requirements met)
    - Source quality (if applicable)
    - Confidence appropriateness
    - Data integrity
    """

    def __init__(self, agent_id: str, specialty: str, message_bus=None):
        """
        Initialize quality verifier.

        Args:
            agent_id: Unique agent ID
            specialty: Area of specialization (e.g., "research", "code", "data")
            message_bus: Message bus for communication
        """
        capabilities = [
            AgentCapability("quality_verification", f"Verify quality of {specialty} outputs", 0.95),
            AgentCapability("accuracy_check", "Check factual accuracy", 0.92),
            AgentCapability("completeness_check", "Verify completeness", 0.94),
            AgentCapability("source_validation", "Validate sources", 0.90),
        ]
        super().__init__(agent_id, capabilities, message_bus)

        self.specialty = specialty

        logger.info(f"QualityVerifierAgent initialized for {specialty}")

    async def process_task(self, task: Task) -> Result:
        """
        Verify quality of an agent's output.

        Args:
            task: Task containing the output to verify

        Returns:
            Result with quality scores and findings
        """
        logger.info(f"QualityVerifier verifying {self.specialty} output")

        # Extract the output to verify from task context
        output_to_verify = task.context.get("output_to_verify", {})
        original_task = task.context.get("original_task", {})

        if not output_to_verify:
            return Result(
                task_id=task.id,
                success=False,
                error="No output provided for verification",
            )

        # Perform quality checks
        quality_scores = {}

        # 1. Accuracy check
        accuracy_score = self._check_accuracy(output_to_verify, original_task)
        quality_scores["accuracy"] = accuracy_score

        # 2. Completeness check
        completeness_score = self._check_completeness(output_to_verify, original_task)
        quality_scores["completeness"] = completeness_score

        # 3. Source quality check (if applicable)
        source_score = self._check_sources(output_to_verify)
        quality_scores["source_quality"] = source_score

        # 4. Confidence appropriateness
        confidence_score = self._check_confidence(output_to_verify)
        quality_scores["confidence_appropriateness"] = confidence_score

        # 5. Data integrity
        integrity_score = self._check_data_integrity(output_to_verify)
        quality_scores["data_integrity"] = integrity_score

        # Calculate overall quality
        overall_quality = sum(quality_scores.values()) / len(quality_scores)

        # Generate findings
        findings = self._generate_findings(quality_scores, output_to_verify)

        # Determine if output passes quality threshold
        passes_quality = overall_quality >= 0.7

        logger.info(
            f"Quality verification complete: overall={overall_quality:.2f}, "
            f"passes={'✓' if passes_quality else '✗'}"
        )

        return Result(
            task_id=task.id,
            success=True,
            data={
                "quality_scores": quality_scores,
                "overall_quality": overall_quality,
                "passes_quality_threshold": passes_quality,
                "findings": findings,
                "verified_output": output_to_verify,
            },
            quality_score=overall_quality,
            metadata={
                "verifier_specialty": self.specialty,
                "verification_type": "quality",
            },
        )

    def _check_accuracy(self, output: Dict[str, Any], original_task: Dict[str, Any]) -> float:
        """Check factual accuracy and logical consistency."""
        score = 0.85  # Base score

        # Check for contradictions
        if isinstance(output.get("data"), dict):
            data_str = str(output["data"]).lower()

            # Look for contradictory phrases
            contradictions = [
                ("always", "never"),
                ("all", "none"),
                ("increase", "decrease"),
            ]

            for word1, word2 in contradictions:
                if word1 in data_str and word2 in data_str:
                    # Potential contradiction (might be legitimate comparison)
                    score -= 0.05

        # Check confidence vs quality alignment
        if "quality_score" in output and "confidence" in output:
            alignment = 1 - abs(output["quality_score"] - output.get("confidence", 0.5))
            score = (score + alignment) / 2

        return max(0.0, min(1.0, score))

    def _check_completeness(self, output: Dict[str, Any], original_task: Dict[str, Any]) -> float:
        """Verify all requirements were met."""
        score = 1.0

        # Check if output has data
        if not output.get("data"):
            score -= 0.3

        # Check if success status is provided
        if "success" not in output:
            score -= 0.1

        # Check if quality score is provided
        if "quality_score" not in output:
            score -= 0.1

        # Check against original requirements (if available)
        requirements = original_task.get("requirements", [])
        if requirements:
            met_requirements = 0
            data_str = str(output.get("data", "")).lower()

            for requirement in requirements:
                req_lower = requirement.lower()
                # Simple check: is requirement mentioned in output?
                if any(word in data_str for word in req_lower.split()[:3]):
                    met_requirements += 1

            if requirements:
                requirement_score = met_requirements / len(requirements)
                score = (score + requirement_score) / 2

        return max(0.0, min(1.0, score))

    def _check_sources(self, output: Dict[str, Any]) -> float:
        """Validate source quality (if sources are provided)."""
        score = 0.8  # Default score if no sources

        data = output.get("data", {})

        if isinstance(data, dict):
            # Check for sources/references
            if "sources" in data or "references" in data:
                sources = data.get("sources", data.get("references", []))

                if sources:
                    # Source quality indicators
                    source_score = 0.0
                    count = 0

                    for source in sources if isinstance(sources, list) else [sources]:
                        source_str = str(source).lower()
                        count += 1

                        # Good source indicators
                        if any(ind in source_str for ind in ["https://", "http://", "doi:", "isbn:"]):
                            source_score += 0.3
                        if any(ind in source_str for ind in [".edu", ".gov", ".org"]):
                            source_score += 0.2
                        if len(source_str) > 20:  # Detailed source
                            source_score += 0.1

                    if count > 0:
                        score = min(1.0, source_score / count)

        return score

    def _check_confidence(self, output: Dict[str, Any]) -> float:
        """Check if confidence scores are appropriate."""
        score = 0.9  # Default if no confidence provided

        if "confidence" in output:
            confidence = output["confidence"]

            # Confidence should be between 0 and 1
            if not (0 <= confidence <= 1):
                return 0.0

            # Check if confidence matches output quality
            quality = output.get("quality_score", 0.5)

            # Good alignment between confidence and quality
            alignment = 1 - abs(confidence - quality)
            score = alignment

        return score

    def _check_data_integrity(self, output: Dict[str, Any]) -> float:
        """Check data structure integrity."""
        score = 1.0

        # Check for basic structure
        if not isinstance(output, dict):
            return 0.5

        # Check for required fields
        required_fields = ["success", "data"]
        for field in required_fields:
            if field not in output:
                score -= 0.2

        # Check data is not empty or null
        if output.get("data") is None:
            score -= 0.3
        elif isinstance(output.get("data"), (str, list, dict)) and not output["data"]:
            score -= 0.2

        # Check for error handling
        if not output.get("success") and not output.get("error"):
            score -= 0.2  # Failed but no error message

        return max(0.0, min(1.0, score))

    def _generate_findings(self, quality_scores: Dict[str, float], output: Dict[str, Any]) -> List[str]:
        """Generate human-readable findings."""
        findings = []

        # Check each score
        for check, score in quality_scores.items():
            if score < 0.7:
                findings.append(f"⚠️  {check.replace('_', ' ').title()}: Low score ({score:.2f})")
            elif score < 0.85:
                findings.append(f"ℹ️  {check.replace('_', ' ').title()}: Moderate score ({score:.2f})")
            else:
                findings.append(f"✓ {check.replace('_', ' ').title()}: High score ({score:.2f})")

        # Specific recommendations
        if quality_scores.get("completeness", 1.0) < 0.8:
            findings.append("💡 Recommendation: Ensure all task requirements are addressed")

        if quality_scores.get("source_quality", 1.0) < 0.7:
            findings.append("💡 Recommendation: Include credible sources and references")

        if quality_scores.get("confidence_appropriateness", 1.0) < 0.75:
            findings.append("💡 Recommendation: Align confidence scores with output quality")

        return findings


class DeliveryValidatorAgent(BaseAgent):
    """
    Validates the delivery format and usability of agent outputs.

    Checks:
    - Format compliance (JSON, structure)
    - Usability (clear, actionable)
    - Presentation quality
    - API contract compliance
    - Error handling
    """

    def __init__(self, agent_id: str, specialty: str, message_bus=None):
        """
        Initialize delivery validator.

        Args:
            agent_id: Unique agent ID
            specialty: Area of specialization
            message_bus: Message bus for communication
        """
        capabilities = [
            AgentCapability("delivery_validation", f"Validate {specialty} delivery format", 0.93),
            AgentCapability("format_compliance", "Check format compliance", 0.94),
            AgentCapability("usability_check", "Verify usability", 0.91),
            AgentCapability("contract_validation", "Validate API contracts", 0.92),
        ]
        super().__init__(agent_id, capabilities, message_bus)

        self.specialty = specialty

        logger.info(f"DeliveryValidatorAgent initialized for {specialty}")

    async def process_task(self, task: Task) -> Result:
        """
        Validate delivery format of an agent's output.

        Args:
            task: Task containing the output to validate

        Returns:
            Result with validation scores and findings
        """
        logger.info(f"DeliveryValidator validating {self.specialty} delivery")

        # Extract output to validate
        output_to_validate = task.context.get("output_to_verify", {})

        if not output_to_validate:
            return Result(
                task_id=task.id,
                success=False,
                error="No output provided for validation",
            )

        # Perform delivery validation checks
        validation_scores = {}

        # 1. Format compliance
        format_score = self._check_format_compliance(output_to_validate)
        validation_scores["format_compliance"] = format_score

        # 2. Usability
        usability_score = self._check_usability(output_to_validate)
        validation_scores["usability"] = usability_score

        # 3. Presentation quality
        presentation_score = self._check_presentation(output_to_validate)
        validation_scores["presentation"] = presentation_score

        # 4. API contract compliance
        contract_score = self._check_contract_compliance(output_to_validate)
        validation_scores["contract_compliance"] = contract_score

        # 5. Error handling
        error_handling_score = self._check_error_handling(output_to_validate)
        validation_scores["error_handling"] = error_handling_score

        # Calculate overall validation score
        overall_validation = sum(validation_scores.values()) / len(validation_scores)

        # Generate findings
        findings = self._generate_findings(validation_scores, output_to_validate)

        # Determine if delivery is acceptable
        passes_validation = overall_validation >= 0.75

        logger.info(
            f"Delivery validation complete: overall={overall_validation:.2f}, "
            f"passes={'✓' if passes_validation else '✗'}"
        )

        return Result(
            task_id=task.id,
            success=True,
            data={
                "validation_scores": validation_scores,
                "overall_validation": overall_validation,
                "passes_validation": passes_validation,
                "findings": findings,
                "validated_output": output_to_validate,
            },
            quality_score=overall_validation,
            metadata={
                "validator_specialty": self.specialty,
                "validation_type": "delivery",
            },
        )

    def _check_format_compliance(self, output: Dict[str, Any]) -> float:
        """Check if output follows proper format."""
        score = 1.0

        # Must be a dictionary
        if not isinstance(output, dict):
            return 0.3

        # Should have standard fields
        standard_fields = ["task_id", "success", "data", "agent_id"]
        missing_fields = [f for f in standard_fields if f not in output]

        score -= len(missing_fields) * 0.15

        # Check data type appropriateness
        if "data" in output and output["data"] is not None:
            # Data should be structured (not just a string, unless that's appropriate)
            if isinstance(output["data"], str) and len(output["data"]) > 200:
                score -= 0.1  # Long unstructured strings are less usable

        return max(0.0, min(1.0, score))

    def _check_usability(self, output: Dict[str, Any]) -> float:
        """Check if output is clear and actionable."""
        score = 0.9

        # Check if data is present and useful
        if not output.get("data"):
            score -= 0.3

        # Check for clarity indicators
        data = output.get("data", {})

        if isinstance(data, dict):
            # Structured data is more usable
            score += 0.1

            # Check for clear labels/keys
            keys = list(data.keys())
            if keys:
                # Keys should be descriptive (not single letters)
                descriptive_keys = [k for k in keys if len(str(k)) > 2]
                score += 0.05 * (len(descriptive_keys) / len(keys))

        # Check for actionable information
        if isinstance(data, (dict, str)):
            data_str = str(data).lower()

            # Actionable indicators
            if any(word in data_str for word in ["recommendation", "action", "next steps", "should"]):
                score += 0.1

        return max(0.0, min(1.0, score))

    def _check_presentation(self, output: Dict[str, Any]) -> float:
        """Check presentation quality."""
        score = 0.85

        data = output.get("data", {})

        # Check for well-organized structure
        if isinstance(data, dict):
            # Nested structure indicates organization
            has_nested = any(isinstance(v, (dict, list)) for v in data.values())
            if has_nested:
                score += 0.1

            # Check for metadata/context
            if any(k in data for k in ["metadata", "context", "summary"]):
                score += 0.05

        # Check for quality metrics
        if "quality_score" in output:
            score += 0.05

        if "confidence" in output:
            score += 0.05

        return max(0.0, min(1.0, score))

    def _check_contract_compliance(self, output: Dict[str, Any]) -> float:
        """Check API contract compliance."""
        score = 1.0

        # Required fields for Result contract
        required_fields = {
            "task_id": str,
            "success": bool,
            "data": (dict, list, str, type(None)),
        }

        for field, expected_type in required_fields.items():
            if field not in output:
                score -= 0.2
            elif not isinstance(output[field], expected_type):
                score -= 0.15

        # Optional but recommended fields
        recommended_fields = ["agent_id", "execution_time", "quality_score"]
        present_recommended = sum(1 for f in recommended_fields if f in output)
        score += (present_recommended / len(recommended_fields)) * 0.1

        return max(0.0, min(1.0, score))

    def _check_error_handling(self, output: Dict[str, Any]) -> float:
        """Check error handling quality."""
        score = 1.0

        # If task failed, should have error message
        if not output.get("success", True):
            if not output.get("error"):
                score -= 0.4  # Failed but no error explanation

            # Check error message quality
            elif output.get("error"):
                error_msg = str(output["error"])

                # Error should be descriptive (not just "Error")
                if len(error_msg) < 10:
                    score -= 0.2

                # Should not expose internal details/stack traces in production
                if any(word in error_msg.lower() for word in ["traceback", "exception", "stack"]):
                    score -= 0.1

        return max(0.0, min(1.0, score))

    def _generate_findings(self, validation_scores: Dict[str, float], output: Dict[str, Any]) -> List[str]:
        """Generate validation findings."""
        findings = []

        # Check each validation score
        for check, score in validation_scores.items():
            if score < 0.75:
                findings.append(f"❌ {check.replace('_', ' ').title()}: Failed ({score:.2f})")
            elif score < 0.9:
                findings.append(f"⚠️  {check.replace('_', ' ').title()}: Needs improvement ({score:.2f})")
            else:
                findings.append(f"✓ {check.replace('_', ' ').title()}: Passed ({score:.2f})")

        # Specific recommendations
        if validation_scores.get("format_compliance", 1.0) < 0.8:
            findings.append("💡 Ensure output includes: task_id, success, data, agent_id")

        if validation_scores.get("usability", 1.0) < 0.8:
            findings.append("💡 Structure data clearly with descriptive keys")

        if validation_scores.get("error_handling", 1.0) < 0.9:
            findings.append("💡 Include clear error messages for failed tasks")

        return findings


def create_verification_agents(message_bus=None) -> Dict[str, BaseAgent]:
    """
    Create verification agents for all agent types.

    Returns 2 agents for each type (Quality Verifier + Delivery Validator).

    Args:
        message_bus: Message bus for communication

    Returns:
        Dictionary of verification agents
    """
    agents = {}

    # Core agent types to verify
    agent_types = [
        "research",
        "code",
        "test",
        "data_analysis",
        "general",
    ]

    for agent_type in agent_types:
        # Quality Verifier
        qv_id = f"quality_verifier_{agent_type}"
        agents[qv_id] = QualityVerifierAgent(qv_id, agent_type, message_bus)

        # Delivery Validator
        dv_id = f"delivery_validator_{agent_type}"
        agents[dv_id] = DeliveryValidatorAgent(dv_id, agent_type, message_bus)

    logger.info(f"Created {len(agents)} verification agents ({len(agents)//2} types)")

    return agents
