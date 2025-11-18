"""
Intelligent Agent Brain

This is the central intelligence system that matches business needs to the right agents.
It acts as a "one-stop-shop" for businesses to describe what they need and get matched
with the most appropriate agents and capabilities.

The brain understands natural language descriptions of business needs and provides:
1. Agent recommendations
2. Workflow suggestions
3. Implementation plans
4. ROI estimates
5. Resource requirements
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import json
import re


class IntelligentAgentBrain:
    """
    Central intelligence system for matching business needs to agents.

    This brain analyzes business requirements and recommends the best agents,
    creates implementation plans, and provides guidance on how to leverage
    the multi-agent ecosystem.

    Capabilities:
    - Natural language understanding of business needs
    - Agent matching and recommendation
    - Workflow design and orchestration
    - Implementation planning
    - ROI estimation
    - Resource requirement assessment
    - Knowledge base management
    """

    def __init__(self, brain_id: str = "intelligent_brain"):
        self.brain_id = brain_id
        self.intelligence_level = 0.95

        # Agent registry with capabilities
        self.agent_registry = self._initialize_agent_registry()

        # Business domain taxonomy
        self.domain_taxonomy = self._initialize_domain_taxonomy()

        # Use case patterns
        self.use_case_patterns = self._initialize_use_case_patterns()

    def _initialize_agent_registry(self) -> Dict[str, Dict[str, Any]]:
        """Initialize comprehensive agent registry."""
        return {
            # Core Agents
            "orchestrator": {
                "category": "core",
                "capabilities": ["task_coordination", "multi_agent_orchestration", "workflow_management"],
                "use_cases": ["complex_workflows", "multi_step_processes"],
                "proficiency": 0.95
            },
            "research_agent": {
                "category": "core",
                "capabilities": ["web_search", "document_analysis", "information_synthesis"],
                "use_cases": ["market_research", "competitor_analysis", "information_gathering"],
                "proficiency": 0.95
            },
            "code_agent": {
                "category": "core",
                "capabilities": ["code_generation", "debugging", "refactoring"],
                "use_cases": ["software_development", "automation", "technical_implementation"],
                "proficiency": 0.90
            },
            "test_agent": {
                "category": "core",
                "capabilities": ["test_generation", "quality_assurance", "validation"],
                "use_cases": ["software_testing", "quality_control"],
                "proficiency": 0.90
            },

            # Utility Agents
            "documentation_agent": {
                "category": "utility",
                "capabilities": ["api_documentation", "readme_generation", "code_commenting"],
                "use_cases": ["documentation", "knowledge_management"],
                "proficiency": 0.91
            },
            "deployment_agent": {
                "category": "utility",
                "capabilities": ["cicd_setup", "docker_deployment", "cloud_deployment"],
                "use_cases": ["devops", "infrastructure", "deployment"],
                "proficiency": 0.89
            },
            "monitoring_agent": {
                "category": "utility",
                "capabilities": ["performance_monitoring", "alerting", "log_analysis"],
                "use_cases": ["system_monitoring", "observability", "incident_management"],
                "proficiency": 0.90
            },
            "security_agent": {
                "category": "utility",
                "capabilities": ["vulnerability_scanning", "security_audit", "compliance"],
                "use_cases": ["security", "compliance", "risk_management"],
                "proficiency": 0.93
            },

            # Domain Specialists
            "legal_compliance_agent": {
                "category": "domain_specialist",
                "capabilities": ["gdpr_compliance", "contract_analysis", "legal_review"],
                "use_cases": ["legal", "compliance", "risk_management"],
                "proficiency": 0.88
            },
            "customer_service_agent": {
                "category": "domain_specialist",
                "capabilities": ["ticket_handling", "sentiment_analysis", "support_automation"],
                "use_cases": ["customer_support", "service_desk", "helpdesk"],
                "proficiency": 0.90
            },
            "content_creation_agent": {
                "category": "domain_specialist",
                "capabilities": ["blog_writing", "social_media", "seo_optimization"],
                "use_cases": ["content_marketing", "seo", "brand_building"],
                "proficiency": 0.91
            },
            "translation_agent": {
                "category": "domain_specialist",
                "capabilities": ["translation", "localization", "multi_language_support"],
                "use_cases": ["internationalization", "global_expansion"],
                "proficiency": 0.89
            },

            # Business Intelligence
            "business_intelligence_agent": {
                "category": "business_intelligence",
                "capabilities": ["kpi_tracking", "dashboard_creation", "business_analytics"],
                "use_cases": ["business_intelligence", "analytics", "reporting"],
                "proficiency": 0.92
            },
            "competitive_analysis_agent": {
                "category": "business_intelligence",
                "capabilities": ["competitor_analysis", "market_intelligence", "swot_analysis"],
                "use_cases": ["competitive_intelligence", "market_analysis", "strategy"],
                "proficiency": 0.90
            },
            "predictive_analytics_agent": {
                "category": "business_intelligence",
                "capabilities": ["forecasting", "prediction", "trend_analysis"],
                "use_cases": ["forecasting", "predictive_analytics", "planning"],
                "proficiency": 0.91
            },

            # Operations & Automation
            "workflow_automation_agent": {
                "category": "operations",
                "capabilities": ["process_automation", "workflow_design", "system_integration"],
                "use_cases": ["automation", "process_improvement", "efficiency"],
                "proficiency": 0.93
            },
            "inventory_management_agent": {
                "category": "operations",
                "capabilities": ["inventory_optimization", "supply_chain", "demand_forecasting"],
                "use_cases": ["inventory", "supply_chain", "logistics"],
                "proficiency": 0.89
            },
            "qa_agent": {
                "category": "operations",
                "capabilities": ["automated_testing", "quality_metrics", "performance_testing"],
                "use_cases": ["quality_assurance", "testing", "reliability"],
                "proficiency": 0.91
            },

            # Sales & Marketing
            "sales_optimization_agent": {
                "category": "sales_marketing",
                "capabilities": ["funnel_optimization", "lead_scoring", "sales_forecasting"],
                "use_cases": ["sales", "revenue_optimization", "pipeline_management"],
                "proficiency": 0.90
            },
            "email_marketing_agent": {
                "category": "sales_marketing",
                "capabilities": ["email_campaigns", "ab_testing", "marketing_automation"],
                "use_cases": ["email_marketing", "lead_nurturing", "customer_engagement"],
                "proficiency": 0.89
            },
            "social_media_agent": {
                "category": "sales_marketing",
                "capabilities": ["social_media_management", "engagement_tracking", "content_scheduling"],
                "use_cases": ["social_media", "brand_awareness", "community_management"],
                "proficiency": 0.88
            },

            # HR & People
            "recruitment_agent": {
                "category": "hr_people",
                "capabilities": ["candidate_screening", "resume_analysis", "recruitment_optimization"],
                "use_cases": ["hiring", "talent_acquisition", "recruitment"],
                "proficiency": 0.91
            },
            "employee_engagement_agent": {
                "category": "hr_people",
                "capabilities": ["engagement_surveys", "culture_assessment", "retention_prediction"],
                "use_cases": ["employee_engagement", "culture", "retention"],
                "proficiency": 0.90
            },
            "performance_review_agent": {
                "category": "hr_people",
                "capabilities": ["performance_reviews", "goal_tracking", "development_planning"],
                "use_cases": ["performance_management", "development", "feedback"],
                "proficiency": 0.89
            },

            # Product & Innovation
            "product_management_agent": {
                "category": "product_innovation",
                "capabilities": ["feature_prioritization", "roadmap_planning", "product_analytics"],
                "use_cases": ["product_management", "product_development", "roadmapping"],
                "proficiency": 0.92
            },
            "innovation_scout_agent": {
                "category": "product_innovation",
                "capabilities": ["trend_tracking", "startup_monitoring", "technology_assessment"],
                "use_cases": ["innovation", "technology_scouting", "rd"],
                "proficiency": 0.90
            },
            "user_feedback_agent": {
                "category": "product_innovation",
                "capabilities": ["feedback_analysis", "sentiment_analysis", "feature_requests"],
                "use_cases": ["user_research", "product_feedback", "voice_of_customer"],
                "proficiency": 0.91
            },

            # Bond.AI Agents
            "career_path_agent": {
                "category": "bond_ai",
                "capabilities": ["career_planning", "path_prediction", "growth_assessment"],
                "use_cases": ["career_development", "professional_growth", "mentorship"],
                "proficiency": 0.94
            },
            "mentorship_matching_agent": {
                "category": "bond_ai",
                "capabilities": ["mentor_matching", "relationship_facilitation", "compatibility_assessment"],
                "use_cases": ["mentorship", "professional_development", "networking"],
                "proficiency": 0.93
            },
            "event_recommendation_agent": {
                "category": "bond_ai",
                "capabilities": ["event_recommendations", "networking_optimization", "roi_prediction"],
                "use_cases": ["networking", "events", "professional_connections"],
                "proficiency": 0.91
            },
            "skill_gap_agent": {
                "category": "bond_ai",
                "capabilities": ["skill_assessment", "learning_paths", "gap_analysis"],
                "use_cases": ["skill_development", "training", "upskilling"],
                "proficiency": 0.92
            }
        }

    def _initialize_domain_taxonomy(self) -> Dict[str, List[str]]:
        """Initialize business domain taxonomy."""
        return {
            "sales": ["lead_generation", "conversion_optimization", "pipeline_management", "forecasting"],
            "marketing": ["content_creation", "email_marketing", "social_media", "seo", "campaigns"],
            "operations": ["automation", "process_improvement", "supply_chain", "inventory", "quality"],
            "hr": ["recruitment", "engagement", "performance", "development", "culture"],
            "product": ["roadmapping", "prioritization", "analytics", "user_research", "innovation"],
            "finance": ["forecasting", "analytics", "risk_management", "compliance"],
            "customer_service": ["support", "ticketing", "satisfaction", "automation"],
            "technology": ["development", "deployment", "monitoring", "security", "testing"],
            "strategy": ["competitive_intelligence", "market_analysis", "planning", "innovation"],
            "analytics": ["business_intelligence", "reporting", "predictive_analytics", "dashboards"]
        }

    def _initialize_use_case_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Initialize common use case patterns."""
        return {
            "improve_sales_conversion": {
                "domain": "sales",
                "agents": ["sales_optimization_agent", "predictive_analytics_agent", "business_intelligence_agent"],
                "workflow": "analyze → optimize → forecast",
                "expected_outcome": "15-25% conversion improvement"
            },
            "automate_customer_support": {
                "domain": "customer_service",
                "agents": ["customer_service_agent", "workflow_automation_agent", "sentiment_analysis"],
                "workflow": "classify → route → respond → escalate",
                "expected_outcome": "50-70% ticket automation"
            },
            "optimize_hiring_process": {
                "domain": "hr",
                "agents": ["recruitment_agent", "workflow_automation_agent"],
                "workflow": "screen → rank → schedule → track",
                "expected_outcome": "40% faster hiring, better candidate quality"
            },
            "improve_product_roadmap": {
                "domain": "product",
                "agents": ["product_management_agent", "user_feedback_agent", "competitive_analysis_agent"],
                "workflow": "gather_feedback → analyze → prioritize → plan",
                "expected_outcome": "Data-driven roadmap, aligned with user needs"
            },
            "automate_marketing_campaigns": {
                "domain": "marketing",
                "agents": ["email_marketing_agent", "social_media_agent", "content_creation_agent"],
                "workflow": "create_content → schedule → distribute → analyze",
                "expected_outcome": "3x campaign velocity, better engagement"
            },
            "enhance_employee_engagement": {
                "domain": "hr",
                "agents": ["employee_engagement_agent", "performance_review_agent"],
                "workflow": "survey → analyze → recommend → implement → track",
                "expected_outcome": "20% engagement improvement, lower churn"
            },
            "accelerate_product_development": {
                "domain": "technology",
                "agents": ["code_agent", "test_agent", "deployment_agent", "qa_agent"],
                "workflow": "develop → test → deploy → monitor",
                "expected_outcome": "50% faster releases, higher quality"
            },
            "business_intelligence_dashboard": {
                "domain": "analytics",
                "agents": ["business_intelligence_agent", "predictive_analytics_agent"],
                "workflow": "collect → analyze → visualize → forecast",
                "expected_outcome": "Real-time insights, data-driven decisions"
            }
        }

    async def match_business_need(self, business_need: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Match a business need description to appropriate agents.

        Args:
            business_need: Natural language description of what the business needs
            context: Optional context about the business (industry, size, etc.)

        Returns:
            Comprehensive recommendation including agents, workflow, and plan
        """
        # Analyze the business need
        analysis = self._analyze_business_need(business_need)

        # Match to use case patterns
        matched_patterns = self._match_use_case_patterns(analysis)

        # Recommend agents
        recommended_agents = self._recommend_agents(analysis, matched_patterns)

        # Design workflow
        workflow = self._design_workflow(recommended_agents, analysis)

        # Create implementation plan
        implementation_plan = self._create_implementation_plan(recommended_agents, workflow, context)

        # Estimate ROI
        roi_estimate = self._estimate_roi(analysis, recommended_agents, context)

        return {
            "status": "success",
            "brain_id": self.brain_id,
            "intelligence_level": self.intelligence_level,
            "analysis": {
                "business_need": business_need,
                "identified_domains": analysis["domains"],
                "key_objectives": analysis["objectives"],
                "complexity": analysis["complexity"]
            },
            "recommendations": {
                "primary_agents": recommended_agents["primary"],
                "supporting_agents": recommended_agents["supporting"],
                "total_agent_count": len(recommended_agents["primary"]) + len(recommended_agents["supporting"]),
                "matched_patterns": matched_patterns
            },
            "workflow": workflow,
            "implementation_plan": implementation_plan,
            "roi_estimate": roi_estimate,
            "next_steps": self._generate_next_steps(recommended_agents, implementation_plan)
        }

    def _analyze_business_need(self, need: str) -> Dict[str, Any]:
        """Analyze and extract key information from business need."""
        need_lower = need.lower()

        # Identify domains
        domains = []
        for domain, keywords in self.domain_taxonomy.items():
            if any(keyword in need_lower for keyword in keywords) or domain in need_lower:
                domains.append(domain)

        # Extract objectives
        objectives = self._extract_objectives(need_lower)

        # Assess complexity
        complexity = self._assess_complexity(need_lower, domains)

        # Extract key terms
        key_terms = self._extract_key_terms(need_lower)

        return {
            "domains": domains if domains else ["general"],
            "objectives": objectives,
            "complexity": complexity,
            "key_terms": key_terms
        }

    def _extract_objectives(self, need: str) -> List[str]:
        """Extract objectives from need description."""
        objectives = []

        # Common objective patterns
        if any(word in need for word in ["improve", "increase", "boost", "enhance", "optimize"]):
            objectives.append("improvement")
        if any(word in need for word in ["automate", "streamline", "efficient"]):
            objectives.append("automation")
        if any(word in need for word in ["analyze", "insight", "understand", "report"]):
            objectives.append("analytics")
        if any(word in need for word in ["reduce", "lower", "decrease", "minimize"]):
            objectives.append("cost_reduction")
        if any(word in need for word in ["scale", "grow", "expand"]):
            objectives.append("scalability")

        return objectives if objectives else ["general_improvement"]

    def _assess_complexity(self, need: str, domains: List[str]) -> str:
        """Assess complexity of the business need."""
        complexity_score = 0

        # Multiple domains increases complexity
        complexity_score += len(domains) * 10

        # Certain keywords indicate complexity
        complex_keywords = ["integrate", "enterprise", "complex", "multiple", "comprehensive", "end-to-end"]
        complexity_score += sum(5 for keyword in complex_keywords if keyword in need)

        if complexity_score >= 40:
            return "high"
        elif complexity_score >= 20:
            return "medium"
        else:
            return "low"

    def _extract_key_terms(self, need: str) -> List[str]:
        """Extract key terms from need description."""
        # Remove common words and extract important terms
        common_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "from", "as", "is", "was", "are", "be", "been", "being", "have", "has", "had", "do", "does", "did", "will", "would", "should", "could", "may", "might", "can", "need", "want", "help", "us", "our", "we", "i"}

        words = re.findall(r'\b\w+\b', need.lower())
        key_terms = [word for word in words if word not in common_words and len(word) > 3]

        return list(set(key_terms))[:10]  # Return top 10 unique terms

    def _match_use_case_patterns(self, analysis: Dict[str, Any]) -> List[str]:
        """Match analysis to known use case patterns."""
        matched = []

        for pattern_name, pattern_info in self.use_case_patterns.items():
            # Check if pattern domain matches
            if pattern_info["domain"] in analysis["domains"]:
                matched.append(pattern_name)

            # Check if key terms match pattern
            pattern_keywords = pattern_name.split("_")
            if any(keyword in analysis["key_terms"] for keyword in pattern_keywords):
                if pattern_name not in matched:
                    matched.append(pattern_name)

        return matched[:3]  # Return top 3 matches

    def _recommend_agents(self, analysis: Dict[str, Any], matched_patterns: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        """Recommend appropriate agents based on analysis."""
        primary_agents = []
        supporting_agents = []

        # Get agents from matched patterns
        pattern_agents = set()
        for pattern_name in matched_patterns:
            if pattern_name in self.use_case_patterns:
                pattern_agents.update(self.use_case_patterns[pattern_name]["agents"])

        # Score all agents based on relevance
        agent_scores = {}
        for agent_id, agent_info in self.agent_registry.items():
            score = 0

            # Check domain match
            if agent_info["category"] in analysis["domains"] or any(d in agent_info["category"] for d in analysis["domains"]):
                score += 30

            # Check use case match
            if any(uc in analysis["key_terms"] for uc in agent_info["use_cases"]):
                score += 20

            # Check capability match
            if any(cap in analysis["key_terms"] for cap in agent_info["capabilities"]):
                score += 15

            # Bonus for pattern matches
            if agent_id in pattern_agents:
                score += 25

            # Proficiency bonus
            score += agent_info["proficiency"] * 10

            if score > 0:
                agent_scores[agent_id] = score

        # Sort by score and categorize
        sorted_agents = sorted(agent_scores.items(), key=lambda x: x[1], reverse=True)

        for agent_id, score in sorted_agents[:5]:
            agent_info = self.agent_registry[agent_id]
            agent_data = {
                "agent_id": agent_id,
                "category": agent_info["category"],
                "capabilities": agent_info["capabilities"],
                "proficiency": agent_info["proficiency"],
                "relevance_score": score
            }

            if score >= 50:
                primary_agents.append(agent_data)
            else:
                supporting_agents.append(agent_data)

        return {
            "primary": primary_agents[:3],  # Top 3 primary agents
            "supporting": supporting_agents[:3]  # Top 3 supporting agents
        }

    def _design_workflow(self, recommended_agents: Dict[str, List[Dict[str, Any]]], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Design a workflow using recommended agents."""
        primary_agents = recommended_agents["primary"]

        # Create workflow steps
        steps = []
        for i, agent in enumerate(primary_agents):
            steps.append({
                "step": i + 1,
                "agent": agent["agent_id"],
                "action": self._determine_agent_action(agent, analysis),
                "inputs": self._determine_step_inputs(i, steps),
                "outputs": self._determine_step_outputs(agent)
            })

        return {
            "workflow_type": "sequential" if analysis["complexity"] == "low" else "parallel",
            "steps": steps,
            "estimated_duration": self._estimate_workflow_duration(steps),
            "orchestration_required": len(steps) > 2
        }

    def _determine_agent_action(self, agent: Dict[str, Any], analysis: Dict[str, Any]) -> str:
        """Determine what action the agent should take."""
        capabilities = agent["capabilities"]
        if "analysis" in capabilities[0] or "analytics" in capabilities[0]:
            return "Analyze and provide insights"
        elif "optimization" in capabilities[0] or "improve" in capabilities[0]:
            return "Optimize and recommend improvements"
        elif "automation" in capabilities[0]:
            return "Automate processes"
        else:
            return f"Execute {capabilities[0]}"

    def _determine_step_inputs(self, step_index: int, previous_steps: List[Dict[str, Any]]) -> List[str]:
        """Determine inputs for a workflow step."""
        if step_index == 0:
            return ["Business requirements", "Current data"]
        else:
            prev_step = previous_steps[-1]
            return [f"Output from {prev_step['agent']}"]

    def _determine_step_outputs(self, agent: Dict[str, Any]) -> List[str]:
        """Determine outputs from a workflow step."""
        return [f"{cap} results" for cap in agent["capabilities"][:2]]

    def _estimate_workflow_duration(self, steps: List[Dict[str, Any]]) -> str:
        """Estimate workflow duration."""
        step_count = len(steps)
        if step_count <= 2:
            return "1-2 weeks"
        elif step_count <= 4:
            return "2-4 weeks"
        else:
            return "1-2 months"

    def _create_implementation_plan(self, recommended_agents: Dict[str, List[Dict[str, Any]]], workflow: Dict[str, Any], context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a detailed implementation plan."""
        return {
            "phases": [
                {
                    "phase": "1. Discovery & Planning",
                    "duration": "1 week",
                    "activities": [
                        "Define detailed requirements",
                        "Configure selected agents",
                        "Set up data connections"
                    ]
                },
                {
                    "phase": "2. Implementation",
                    "duration": workflow["estimated_duration"],
                    "activities": [
                        "Deploy agents",
                        "Implement workflow",
                        "Integrate with existing systems"
                    ]
                },
                {
                    "phase": "3. Testing & Validation",
                    "duration": "1 week",
                    "activities": [
                        "Test agent performance",
                        "Validate outputs",
                        "Optimize configurations"
                    ]
                },
                {
                    "phase": "4. Deployment & Training",
                    "duration": "1 week",
                    "activities": [
                        "Deploy to production",
                        "Train team members",
                        "Set up monitoring"
                    ]
                }
            ],
            "resources_required": {
                "technical": "1 developer/engineer",
                "business": "1 business analyst",
                "time_commitment": "20-40 hours total"
            },
            "success_metrics": self._define_success_metrics(recommended_agents)
        }

    def _define_success_metrics(self, recommended_agents: Dict[str, List[Dict[str, Any]]]) -> List[str]:
        """Define success metrics based on agents."""
        return [
            "Agent accuracy >= 85%",
            "Task completion time reduced by 30%",
            "User satisfaction score >= 4/5",
            "ROI positive within 6 months"
        ]

    def _estimate_roi(self, analysis: Dict[str, Any], recommended_agents: Dict[str, List[Dict[str, Any]]], context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Estimate return on investment."""
        # Simplified ROI calculation
        agent_count = len(recommended_agents["primary"]) + len(recommended_agents["supporting"])

        implementation_cost = agent_count * 5000  # Estimated cost per agent

        # Estimate benefits based on objectives
        annual_benefit = 0
        if "automation" in analysis["objectives"]:
            annual_benefit += 50000  # Time savings
        if "improvement" in analysis["objectives"]:
            annual_benefit += 30000  # Efficiency gains
        if "analytics" in analysis["objectives"]:
            annual_benefit += 40000  # Better decisions

        payback_months = (implementation_cost / (annual_benefit / 12)) if annual_benefit > 0 else 12

        return {
            "estimated_implementation_cost": f"${implementation_cost:,}",
            "estimated_annual_benefit": f"${annual_benefit:,}",
            "payback_period": f"{payback_months:.1f} months",
            "3_year_roi": f"{((annual_benefit * 3 - implementation_cost) / implementation_cost * 100):.0f}%",
            "confidence_level": "medium"
        }

    def _generate_next_steps(self, recommended_agents: Dict[str, List[Dict[str, Any]]], implementation_plan: Dict[str, Any]) -> List[str]:
        """Generate actionable next steps."""
        return [
            f"Review recommended agents: {', '.join([a['agent_id'] for a in recommended_agents['primary']])}",
            "Schedule discovery session with stakeholders",
            "Prepare data sources and integration requirements",
            "Start with Phase 1: Discovery & Planning",
            "Set up monitoring and success metrics"
        ]

    async def get_agent_details(self, agent_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific agent."""
        if agent_id not in self.agent_registry:
            return {
                "status": "error",
                "message": f"Agent '{agent_id}' not found in registry"
            }

        agent = self.agent_registry[agent_id]

        return {
            "status": "success",
            "agent_id": agent_id,
            "details": agent,
            "usage_examples": self._generate_usage_examples(agent_id, agent),
            "integration_guide": self._generate_integration_guide(agent_id)
        }

    def _generate_usage_examples(self, agent_id: str, agent_info: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate usage examples for an agent."""
        return [
            {
                "scenario": f"Using {agent_id} for {agent_info['use_cases'][0]}",
                "example": f"Apply {agent_id} to {agent_info['capabilities'][0]}"
            }
        ]

    def _generate_integration_guide(self, agent_id: str) -> Dict[str, List[str]]:
        """Generate integration guide for an agent."""
        return {
            "prerequisites": ["Configure agent credentials", "Set up data connections"],
            "steps": [
                f"Import {agent_id} from agents library",
                "Configure agent parameters",
                "Execute agent task",
                "Process agent results"
            ]
        }

    async def search_agents_by_capability(self, capability: str) -> Dict[str, Any]:
        """Search for agents by capability."""
        matching_agents = []

        for agent_id, agent_info in self.agent_registry.items():
            if any(capability.lower() in cap.lower() for cap in agent_info["capabilities"]):
                matching_agents.append({
                    "agent_id": agent_id,
                    "category": agent_info["category"],
                    "capabilities": agent_info["capabilities"],
                    "proficiency": agent_info["proficiency"]
                })

        return {
            "status": "success",
            "capability_search": capability,
            "matching_agents": matching_agents,
            "total_matches": len(matching_agents)
        }

    async def list_all_agents(self, category: Optional[str] = None) -> Dict[str, Any]:
        """List all available agents, optionally filtered by category."""
        if category:
            agents = {
                agent_id: info
                for agent_id, info in self.agent_registry.items()
                if info["category"] == category
            }
        else:
            agents = self.agent_registry

        return {
            "status": "success",
            "total_agents": len(agents),
            "agents": agents,
            "categories": list(set(info["category"] for info in agents.values()))
        }


# Convenience function
async def ask_brain(business_need: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Convenience function to ask the Intelligent Agent Brain for recommendations.

    Args:
        business_need: Description of what your business needs
        context: Optional context (industry, company size, etc.)

    Returns:
        Comprehensive recommendations including agents, workflow, and implementation plan

    Example:
        >>> result = await ask_brain("I need to improve my sales conversion rates")
        >>> print(result["recommendations"]["primary_agents"])
    """
    brain = IntelligentAgentBrain()
    return await brain.match_business_need(business_need, context)
