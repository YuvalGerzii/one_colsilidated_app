"""
Skills Verification & Certification Tracker
Track, verify, and showcase professional skills, certifications, and credentials
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from enum import Enum


class SkillLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class VerificationStatus(str, Enum):
    UNVERIFIED = "unverified"
    SELF_ASSESSED = "self_assessed"
    PEER_ENDORSED = "peer_endorsed"
    CERTIFIED = "certified"
    PROFESSIONALLY_VERIFIED = "professionally_verified"


class CertificationPriority(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class SkillsCertificationTracker:
    """Comprehensive skills verification and certification tracking system"""

    def __init__(self):
        # Industry-recognized certifications by field
        self.certifications_database = {
            "software_engineering": [
                {
                    "name": "AWS Certified Solutions Architect",
                    "provider": "Amazon Web Services",
                    "cost": 150,
                    "prep_time_hours": 40,
                    "validity_years": 3,
                    "market_value": "high",
                    "salary_impact": "+8-12%",
                    "demand_score": 95
                },
                {
                    "name": "Certified Kubernetes Administrator (CKA)",
                    "provider": "Cloud Native Computing Foundation",
                    "cost": 375,
                    "prep_time_hours": 60,
                    "validity_years": 3,
                    "market_value": "high",
                    "salary_impact": "+10-15%",
                    "demand_score": 88
                },
                {
                    "name": "Google Professional Cloud Architect",
                    "provider": "Google Cloud",
                    "cost": 200,
                    "prep_time_hours": 50,
                    "validity_years": 2,
                    "market_value": "high",
                    "salary_impact": "+8-12%",
                    "demand_score": 85
                }
            ],
            "data_science": [
                {
                    "name": "TensorFlow Developer Certificate",
                    "provider": "Google",
                    "cost": 100,
                    "prep_time_hours": 80,
                    "validity_years": 3,
                    "market_value": "high",
                    "salary_impact": "+10-15%",
                    "demand_score": 92
                },
                {
                    "name": "AWS Certified Machine Learning Specialty",
                    "provider": "Amazon Web Services",
                    "cost": 300,
                    "prep_time_hours": 100,
                    "validity_years": 3,
                    "market_value": "very_high",
                    "salary_impact": "+12-18%",
                    "demand_score": 94
                }
            ],
            "project_management": [
                {
                    "name": "PMP (Project Management Professional)",
                    "provider": "PMI",
                    "cost": 555,
                    "prep_time_hours": 120,
                    "validity_years": 3,
                    "market_value": "very_high",
                    "salary_impact": "+15-20%",
                    "demand_score": 96
                },
                {
                    "name": "Certified ScrumMaster (CSM)",
                    "provider": "Scrum Alliance",
                    "cost": 1000,
                    "prep_time_hours": 16,
                    "validity_years": 2,
                    "market_value": "high",
                    "salary_impact": "+8-12%",
                    "demand_score": 89
                }
            ]
        }

    def track_skill_inventory(self, worker_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive skill inventory tracking

        Args:
            worker_data: Worker's skills and experience

        Returns:
            Detailed skill inventory with verification levels and recommendations
        """
        skills = worker_data.get("skills", [])
        target_role = worker_data.get("target_role", "")

        # Categorize skills
        categorized_skills = {
            "technical_hard_skills": [],
            "soft_skills": [],
            "domain_knowledge": [],
            "tools_platforms": []
        }

        skill_analysis = []
        for skill in skills:
            skill_name = skill.get("name", "")
            level = skill.get("level", SkillLevel.INTERMEDIATE.value)
            years_experience = skill.get("years_experience", 0)
            last_used = skill.get("last_used_date", datetime.now().isoformat())
            verification_status = skill.get("verification_status", VerificationStatus.SELF_ASSESSED.value)

            # Calculate skill strength score (0-100)
            strength_score = self._calculate_skill_strength(
                level, years_experience, verification_status, last_used
            )

            # Market demand for skill
            market_demand = self._get_skill_market_demand(skill_name, target_role)

            # Skill health (is it current or outdated?)
            skill_health = self._assess_skill_health(last_used, market_demand)

            # Verification recommendation
            verification_rec = self._recommend_verification_method(
                skill_name, verification_status, level
            )

            skill_info = {
                "skill_name": skill_name,
                "level": level,
                "years_experience": years_experience,
                "strength_score": strength_score,
                "verification_status": verification_status,
                "market_demand": market_demand,
                "skill_health": skill_health,
                "last_used": last_used,
                "days_since_used": (datetime.now() - datetime.fromisoformat(last_used.replace('Z', '+00:00').replace('+00:00', ''))).days if isinstance(last_used, str) else 0,
                "verification_recommendation": verification_rec,
                "endorsements_count": skill.get("endorsements_count", 0)
            }

            # Categorize
            category = self._categorize_skill(skill_name)
            categorized_skills[category].append(skill_info)
            skill_analysis.append(skill_info)

        # Identify skill gaps
        gaps = self._identify_skill_gaps(skills, target_role)

        # Calculate portfolio strength
        portfolio_strength = self._calculate_portfolio_strength(skill_analysis)

        # Verification priorities
        verification_priorities = self._prioritize_verifications(skill_analysis, target_role)

        return {
            "total_skills": len(skills),
            "categorized_skills": categorized_skills,
            "skill_analysis": sorted(skill_analysis, key=lambda x: x["strength_score"], reverse=True),
            "portfolio_strength": portfolio_strength,
            "skill_gaps": gaps,
            "verification_priorities": verification_priorities,
            "top_skills": sorted(skill_analysis, key=lambda x: x["strength_score"], reverse=True)[:10],
            "outdated_skills": [s for s in skill_analysis if s["skill_health"] == "outdated"],
            "unverified_skills": [s for s in skill_analysis if s["verification_status"] == VerificationStatus.UNVERIFIED.value],
            "recommendations": self._generate_skill_recommendations(skill_analysis, gaps)
        }

    def recommend_certifications(self, worker_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recommend valuable certifications based on career goals

        Args:
            worker_data: Worker profile and goals

        Returns:
            Prioritized certification recommendations with ROI analysis
        """
        role = worker_data.get("target_role", "software_engineer")
        field = worker_data.get("field", "software_engineering")
        current_salary = worker_data.get("current_salary", 100000)
        available_budget = worker_data.get("certification_budget", 1000)
        available_time_hours = worker_data.get("available_study_hours_weekly", 10)

        # Get relevant certifications
        certifications = self.certifications_database.get(field, [])

        # Analyze each certification
        analyzed_certs = []
        for cert in certifications:
            # Calculate ROI
            salary_increase_pct = float(cert["salary_impact"].split("-")[0].replace("+", "").replace("%", "")) / 100
            potential_salary_increase = current_salary * salary_increase_pct
            lifetime_value = potential_salary_increase * 5  # 5-year impact

            roi = (lifetime_value - cert["cost"]) / cert["cost"]

            # Time to complete
            weeks_to_complete = cert["prep_time_hours"] / available_time_hours

            # Feasibility score
            cost_feasible = 100 if cert["cost"] <= available_budget else (available_budget / cert["cost"]) * 100
            time_feasible = 100 if weeks_to_complete <= 12 else (12 / weeks_to_complete) * 100
            feasibility_score = (cost_feasible + time_feasible) / 2

            # Overall priority score
            priority_score = (
                cert["demand_score"] * 0.4 +
                min(100, roi * 5) * 0.35 +
                feasibility_score * 0.25
            )

            # Determine priority level
            if priority_score >= 80:
                priority = CertificationPriority.CRITICAL
            elif priority_score >= 65:
                priority = CertificationPriority.HIGH
            elif priority_score >= 45:
                priority = CertificationPriority.MEDIUM
            else:
                priority = CertificationPriority.LOW

            analyzed_certs.append({
                **cert,
                "priority": priority.value,
                "priority_score": round(priority_score, 1),
                "roi": round(roi, 2),
                "potential_salary_increase": round(potential_salary_increase),
                "5_year_value": round(lifetime_value),
                "weeks_to_complete": round(weeks_to_complete, 1),
                "feasibility_score": round(feasibility_score, 1),
                "cost_feasible": cert["cost"] <= available_budget,
                "time_commitment": f"{weeks_to_complete:.1f} weeks at {available_time_hours} hrs/week"
            })

        # Sort by priority score
        analyzed_certs.sort(key=lambda x: x["priority_score"], reverse=True)

        # Create certification roadmap
        roadmap = self._create_certification_roadmap(
            analyzed_certs, available_budget, available_time_hours
        )

        return {
            "total_recommendations": len(analyzed_certs),
            "high_priority": [c for c in analyzed_certs if c["priority"] in ["critical", "high"]],
            "all_recommendations": analyzed_certs,
            "certification_roadmap": roadmap,
            "budget_analysis": {
                "available_budget": available_budget,
                "recommended_investment": sum(c["cost"] for c in analyzed_certs[:3]),
                "expected_5_year_roi": sum(c["5_year_value"] for c in analyzed_certs[:3])
            },
            "time_analysis": {
                "available_weekly_hours": available_time_hours,
                "total_prep_hours_needed": sum(c["prep_time_hours"] for c in analyzed_certs[:3]),
                "estimated_completion_timeline": f"{sum(c['weeks_to_complete'] for c in analyzed_certs[:3]):.1f} weeks"
            },
            "top_3_recommendations": analyzed_certs[:3]
        }

    def verify_skill(self, skill_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Initiate skill verification process

        Args:
            skill_data: Skill details and verification type

        Returns:
            Verification status and next steps
        """
        skill_name = skill_data.get("skill_name", "")
        verification_type = skill_data.get("verification_type", "self_assessment")
        current_level = skill_data.get("current_level", SkillLevel.INTERMEDIATE.value)

        # Verification methods
        verification_methods = {
            "self_assessment": {
                "name": "Self-Assessment",
                "credibility": 20,
                "cost": 0,
                "time_minutes": 15,
                "description": "Take skill assessment quiz",
                "steps": [
                    "Complete 20-question assessment",
                    "Review results and weak areas",
                    "Update skill level based on score"
                ]
            },
            "peer_endorsement": {
                "name": "Peer Endorsement",
                "credibility": 50,
                "cost": 0,
                "time_minutes": 30,
                "description": "Request endorsements from colleagues",
                "steps": [
                    "Identify 3-5 colleagues who've seen your work",
                    "Send endorsement requests via LinkedIn/email",
                    "Collect endorsements",
                    "Showcase on profile"
                ]
            },
            "certification": {
                "name": "Professional Certification",
                "credibility": 95,
                "cost": "Varies ($100-$500)",
                "time_minutes": "20-100 hours prep",
                "description": "Earn industry-recognized certification",
                "steps": [
                    "Choose relevant certification",
                    "Study and prepare (courses, practice exams)",
                    "Schedule and take exam",
                    "Receive certification",
                    "Add to LinkedIn and resume"
                ]
            },
            "portfolio_project": {
                "name": "Portfolio Demonstration",
                "credibility": 75,
                "cost": 0,
                "time_hours": "10-40 hours",
                "description": "Build project showcasing skill",
                "steps": [
                    "Design project demonstrating skill",
                    "Build and document project",
                    "Deploy and share (GitHub, portfolio site)",
                    "Get feedback from community"
                ]
            },
            "employer_verification": {
                "name": "Employment Verification",
                "credibility": 85,
                "cost": 0,
                "time_minutes": 10,
                "description": "Verify through work history",
                "steps": [
                    "Document projects using this skill",
                    "Get manager/colleague verification",
                    "Add to LinkedIn with endorsements"
                ]
            }
        }

        method = verification_methods.get(verification_type, verification_methods["self_assessment"])

        # Skill assessment questions
        assessment = self._generate_skill_assessment(skill_name, current_level)

        # Recommended verifiers (people to ask for endorsements)
        recommended_verifiers = self._suggest_verifiers(skill_name, skill_data)

        # Portfolio project ideas
        project_ideas = self._suggest_verification_projects(skill_name, current_level)

        return {
            "skill_name": skill_name,
            "verification_method": method,
            "current_verification_status": skill_data.get("verification_status", "unverified"),
            "target_verification_status": self._map_method_to_status(verification_type),
            "credibility_boost": f"+{method['credibility']} credibility points",
            "next_steps": method["steps"],
            "skill_assessment": assessment if verification_type == "self_assessment" else None,
            "recommended_verifiers": recommended_verifiers if verification_type == "peer_endorsement" else None,
            "portfolio_project_ideas": project_ideas if verification_type == "portfolio_project" else None,
            "certification_recommendations": self._get_certification_for_skill(skill_name) if verification_type == "certification" else None,
            "estimated_completion_time": method.get("time_minutes", method.get("time_hours", "varies")),
            "cost": method["cost"]
        }

    def skill_gap_validation(self, current_skills: List[str],
                            target_role: str) -> Dict[str, Any]:
        """
        Validate skill gaps for target role with verification recommendations

        Args:
            current_skills: Current skill set
            target_role: Desired role

        Returns:
            Detailed gap analysis with verification path
        """
        # Required skills for target role
        role_requirements = self._get_role_requirements(target_role)

        # Identify gaps
        missing_skills = []
        weak_skills = []
        sufficient_skills = []

        for req_skill in role_requirements:
            skill_name = req_skill["skill"]
            required_level = req_skill["level"]
            importance = req_skill["importance"]

            # Check if worker has this skill
            current_skill = next((s for s in current_skills if isinstance(s, dict) and s.get("name", "").lower() == skill_name.lower()), None)

            if not current_skill:
                missing_skills.append({
                    "skill": skill_name,
                    "required_level": required_level,
                    "importance": importance,
                    "gap_severity": "critical" if importance == "required" else "high",
                    "learning_path": self._get_learning_path(skill_name, required_level),
                    "time_to_proficiency": self._estimate_learning_time(skill_name, "beginner", required_level),
                    "verification_recommendation": "Complete certification or build portfolio project"
                })
            else:
                current_level = current_skill.get("level", "beginner")
                level_score = {"beginner": 1, "intermediate": 2, "advanced": 3, "expert": 4}

                if level_score.get(current_level, 1) < level_score.get(required_level, 2):
                    weak_skills.append({
                        "skill": skill_name,
                        "current_level": current_level,
                        "required_level": required_level,
                        "gap": f"{current_level} → {required_level}",
                        "improvement_needed": True,
                        "learning_path": self._get_learning_path(skill_name, required_level, current_level),
                        "time_to_proficiency": self._estimate_learning_time(skill_name, current_level, required_level),
                        "verification_status": current_skill.get("verification_status", "unverified"),
                        "verification_recommendation": "Get certified or endorsed by senior professionals"
                    })
                else:
                    sufficient_skills.append({
                        "skill": skill_name,
                        "current_level": current_level,
                        "verification_status": current_skill.get("verification_status", "unverified"),
                        "recommendation": "Maintain and verify through certification or endorsements" if current_skill.get("verification_status") == "unverified" else "Well positioned"
                    })

        # Calculate readiness score
        total_required = len(role_requirements)
        gaps_count = len(missing_skills) + len(weak_skills)
        readiness_score = ((total_required - gaps_count) / total_required) * 100

        # Create improvement plan
        improvement_plan = self._create_improvement_plan(missing_skills, weak_skills)

        return {
            "target_role": target_role,
            "readiness_score": round(readiness_score, 1),
            "readiness_assessment": self._assess_readiness(readiness_score),
            "total_required_skills": total_required,
            "missing_skills_count": len(missing_skills),
            "weak_skills_count": len(weak_skills),
            "sufficient_skills_count": len(sufficient_skills),
            "missing_skills": missing_skills,
            "weak_skills": weak_skills,
            "sufficient_skills": sufficient_skills,
            "improvement_plan": improvement_plan,
            "estimated_time_to_ready": self._calculate_total_prep_time(missing_skills, weak_skills),
            "priority_actions": self._get_priority_actions(missing_skills, weak_skills),
            "verification_roadmap": self._create_verification_roadmap(missing_skills, weak_skills, sufficient_skills)
        }

    def _calculate_skill_strength(self, level: str, years_exp: int,
                                  verification_status: str, last_used: str) -> float:
        """Calculate overall skill strength score"""
        # Base score from level
        level_scores = {
            "beginner": 25,
            "intermediate": 50,
            "advanced": 75,
            "expert": 90
        }
        score = level_scores.get(level, 50)

        # Years of experience boost (up to +20)
        exp_boost = min(20, years_exp * 3)
        score += exp_boost

        # Verification boost
        verification_boost = {
            "unverified": 0,
            "self_assessed": 5,
            "peer_endorsed": 10,
            "certified": 20,
            "professionally_verified": 15
        }
        score += verification_boost.get(verification_status, 0)

        # Recency penalty
        try:
            last_used_date = datetime.fromisoformat(last_used.replace('Z', '+00:00').replace('+00:00', ''))
            days_since = (datetime.now() - last_used_date).days
            if days_since > 365:
                score -= 10
            elif days_since > 180:
                score -= 5
        except:
            pass

        return min(100, max(0, score))

    def _get_skill_market_demand(self, skill_name: str, target_role: str) -> Dict[str, Any]:
        """Get market demand for skill"""
        # Simplified - would query real market data
        demand_score = 75  # Default

        return {
            "demand_score": demand_score,
            "trend": "increasing" if demand_score > 70 else "stable" if demand_score > 50 else "decreasing",
            "job_postings_mentioning": "10,000+",
            "average_salary_boost": "+$8,000"
        }

    def _assess_skill_health(self, last_used: str, market_demand: Dict[str, Any]) -> str:
        """Assess if skill is current or outdated"""
        try:
            last_used_date = datetime.fromisoformat(last_used.replace('Z', '+00:00').replace('+00:00', ''))
            days_since = (datetime.now() - last_used_date).days

            if days_since > 730:  # 2 years
                return "outdated"
            elif days_since > 365:  # 1 year
                return "aging"
            else:
                return "current"
        except:
            return "current"

    def _recommend_verification_method(self, skill_name: str,
                                       current_status: str, level: str) -> str:
        """Recommend verification method for skill"""
        if current_status in ["certified", "professionally_verified"]:
            return "Already well-verified. Maintain certifications."

        if level in ["advanced", "expert"]:
            return "Get professional certification or build impressive portfolio project"
        elif level == "intermediate":
            return "Collect peer endorsements and consider certification"
        else:
            return "Complete self-assessment and build beginner projects"

    def _categorize_skill(self, skill_name: str) -> str:
        """Categorize skill type"""
        technical_keywords = ["python", "java", "javascript", "sql", "aws", "docker", "kubernetes"]
        tools_keywords = ["git", "jira", "figma", "tableau", "excel"]
        soft_keywords = ["communication", "leadership", "teamwork", "problem", "critical thinking"]

        skill_lower = skill_name.lower()

        if any(kw in skill_lower for kw in technical_keywords):
            return "technical_hard_skills"
        elif any(kw in skill_lower for kw in tools_keywords):
            return "tools_platforms"
        elif any(kw in skill_lower for kw in soft_keywords):
            return "soft_skills"
        else:
            return "domain_knowledge"

    def _identify_skill_gaps(self, current_skills: List[Dict[str, Any]],
                            target_role: str) -> List[Dict[str, Any]]:
        """Identify skill gaps for target role"""
        required_skills = self._get_role_requirements(target_role)
        current_skill_names = [s.get("name", "").lower() for s in current_skills if isinstance(s, dict)]

        gaps = []
        for req in required_skills:
            if req["skill"].lower() not in current_skill_names:
                gaps.append({
                    "skill": req["skill"],
                    "required_level": req["level"],
                    "importance": req["importance"],
                    "gap_type": "missing"
                })

        return gaps

    def _calculate_portfolio_strength(self, skills: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate overall portfolio strength"""
        if not skills:
            return {"score": 0, "rating": "weak"}

        avg_strength = sum(s["strength_score"] for s in skills) / len(skills)
        verified_pct = (sum(1 for s in skills if s["verification_status"] != "unverified") / len(skills)) * 100

        # Combined score
        portfolio_score = (avg_strength * 0.6) + (verified_pct * 0.4)

        if portfolio_score >= 80:
            rating = "excellent"
        elif portfolio_score >= 65:
            rating = "strong"
        elif portfolio_score >= 50:
            rating = "good"
        else:
            rating = "needs_improvement"

        return {
            "score": round(portfolio_score, 1),
            "rating": rating,
            "average_skill_strength": round(avg_strength, 1),
            "verification_percentage": round(verified_pct, 1)
        }

    def _prioritize_verifications(self, skills: List[Dict[str, Any]],
                                  target_role: str) -> List[Dict[str, Any]]:
        """Prioritize which skills to verify first"""
        unverified = [s for s in skills if s["verification_status"] in ["unverified", "self_assessed"]]

        # Score each by importance
        for skill in unverified:
            priority_score = (
                skill["strength_score"] * 0.4 +
                skill["market_demand"]["demand_score"] * 0.6
            )
            skill["verification_priority_score"] = priority_score

        # Sort by priority
        prioritized = sorted(unverified, key=lambda x: x["verification_priority_score"], reverse=True)

        return prioritized[:10]  # Top 10

    def _generate_skill_recommendations(self, skills: List[Dict[str, Any]],
                                       gaps: List[Dict[str, Any]]) -> List[str]:
        """Generate skill improvement recommendations"""
        recommendations = []

        # Verify top skills
        top_unverified = [s for s in skills if s["verification_status"] == "unverified"][:3]
        if top_unverified:
            recommendations.append(f"Verify your top skills: {', '.join(s['skill_name'] for s in top_unverified)}")

        # Address outdated skills
        outdated = [s for s in skills if s["skill_health"] == "outdated"]
        if outdated:
            recommendations.append(f"Refresh outdated skills: {', '.join(s['skill_name'] for s in outdated[:2])}")

        # Fill gaps
        if gaps:
            recommendations.append(f"Learn missing critical skills: {', '.join(g['skill'] for g in gaps[:2])}")

        return recommendations

    def _create_certification_roadmap(self, certifications: List[Dict[str, Any]],
                                     budget: float, hours_weekly: float) -> Dict[str, Any]:
        """Create step-by-step certification roadmap"""
        roadmap = []
        cumulative_cost = 0
        cumulative_weeks = 0

        for cert in certifications[:5]:  # Top 5
            if cumulative_cost + cert["cost"] > budget * 1.5:  # Allow slight budget overrun
                break

            cumulative_cost += cert["cost"]
            cumulative_weeks += cert["weeks_to_complete"]

            roadmap.append({
                "order": len(roadmap) + 1,
                "certification": cert["name"],
                "start_week": round(cumulative_weeks - cert["weeks_to_complete"]),
                "duration_weeks": round(cert["weeks_to_complete"], 1),
                "cost": cert["cost"],
                "priority": cert["priority"]
            })

        return {
            "total_certifications": len(roadmap),
            "total_cost": cumulative_cost,
            "total_weeks": round(cumulative_weeks, 1),
            "timeline": roadmap
        }

    def _generate_skill_assessment(self, skill_name: str,
                                   level: str) -> Dict[str, Any]:
        """Generate skill assessment questions"""
        return {
            "skill": skill_name,
            "level": level,
            "question_count": 20,
            "time_limit_minutes": 15,
            "sample_questions": [
                f"Basic {skill_name} concept question",
                f"Intermediate {skill_name} application",
                f"Advanced {skill_name} scenario"
            ],
            "passing_score": 70,
            "certification_available": True
        }

    def _suggest_verifiers(self, skill_name: str,
                          skill_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Suggest people to request endorsements from"""
        return [
            {
                "type": "Manager",
                "recommendation": "Request from current or former manager",
                "message_template": f"Hi [Name], could you endorse my {skill_name} skills on LinkedIn?"
            },
            {
                "type": "Colleague",
                "recommendation": "Request from team members who've worked with you",
                "message_template": f"Hi [Name], we worked together on [project]. Could you endorse my {skill_name}?"
            },
            {
                "type": "Client/Stakeholder",
                "recommendation": "Request from clients who've benefited from your work",
                "message_template": f"Hi [Name], your feedback on my {skill_name} work would be valuable."
            }
        ]

    def _suggest_verification_projects(self, skill_name: str,
                                      level: str) -> List[Dict[str, Any]]:
        """Suggest portfolio projects for skill verification"""
        projects = {
            "python": [
                {
                    "title": "Web Scraper with Data Analysis",
                    "difficulty": "intermediate",
                    "time_hours": 15,
                    "description": "Build scraper + analyze data with pandas",
                    "skills_demonstrated": ["Python", "Web Scraping", "Data Analysis"]
                }
            ],
            "machine_learning": [
                {
                    "title": "Predictive Model Deployment",
                    "difficulty": "advanced",
                    "time_hours": 40,
                    "description": "Train ML model and deploy as API",
                    "skills_demonstrated": ["ML", "Python", "API Development", "Deployment"]
                }
            ]
        }

        return projects.get(skill_name.lower(), [
            {
                "title": f"{skill_name} Demo Project",
                "difficulty": level,
                "time_hours": 20,
                "description": f"Build project showcasing {skill_name} expertise"
            }
        ])

    def _get_certification_for_skill(self, skill_name: str) -> List[Dict[str, Any]]:
        """Get relevant certifications for skill"""
        # Simplified mapping
        cert_map = {
            "python": ["Python Institute PCAP", "Python Institute PCPP"],
            "aws": ["AWS Certified Solutions Architect", "AWS Certified Developer"],
            "kubernetes": ["Certified Kubernetes Administrator (CKA)"]
        }

        cert_names = cert_map.get(skill_name.lower(), [])
        return [{"name": name, "provider": "Varies", "estimated_cost": "$100-$400"} for name in cert_names]

    def _map_method_to_status(self, verification_type: str) -> str:
        """Map verification method to status"""
        mapping = {
            "self_assessment": "self_assessed",
            "peer_endorsement": "peer_endorsed",
            "certification": "certified",
            "portfolio_project": "professionally_verified",
            "employer_verification": "professionally_verified"
        }
        return mapping.get(verification_type, "self_assessed")

    def _get_role_requirements(self, role: str) -> List[Dict[str, Any]]:
        """Get skill requirements for role"""
        # Simplified requirements database
        requirements = {
            "software_engineer": [
                {"skill": "Python", "level": "advanced", "importance": "required"},
                {"skill": "JavaScript", "level": "intermediate", "importance": "required"},
                {"skill": "Git", "level": "intermediate", "importance": "required"},
                {"skill": "SQL", "level": "intermediate", "importance": "required"},
                {"skill": "System Design", "level": "intermediate", "importance": "preferred"}
            ],
            "data_scientist": [
                {"skill": "Python", "level": "advanced", "importance": "required"},
                {"skill": "Machine Learning", "level": "advanced", "importance": "required"},
                {"skill": "Statistics", "level": "advanced", "importance": "required"},
                {"skill": "SQL", "level": "intermediate", "importance": "required"},
                {"skill": "Data Visualization", "level": "intermediate", "importance": "preferred"}
            ]
        }

        return requirements.get(role.lower().replace(" ", "_"), requirements["software_engineer"])

    def _get_learning_path(self, skill_name: str, target_level: str,
                          current_level: str = "beginner") -> List[Dict[str, str]]:
        """Get learning path for skill"""
        return [
            {
                "step": 1,
                "resource": f"Online course: {skill_name} Fundamentals",
                "duration": "2-4 weeks",
                "cost": "$50-$200"
            },
            {
                "step": 2,
                "resource": f"Practice: Build 3-5 projects using {skill_name}",
                "duration": "4-8 weeks",
                "cost": "Free"
            },
            {
                "step": 3,
                "resource": f"Certification: Professional {skill_name} certification",
                "duration": "2-4 weeks prep",
                "cost": "$100-$400"
            }
        ]

    def _estimate_learning_time(self, skill_name: str,
                                current_level: str, target_level: str) -> str:
        """Estimate time to reach target level"""
        level_map = {"beginner": 0, "intermediate": 1, "advanced": 2, "expert": 3}
        gap = level_map.get(target_level, 1) - level_map.get(current_level, 0)

        weeks = gap * 8  # 8 weeks per level
        return f"{weeks} weeks (at 10 hrs/week)"

    def _create_improvement_plan(self, missing_skills: List[Dict[str, Any]],
                                weak_skills: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create comprehensive improvement plan"""
        phases = []

        # Phase 1: Critical missing skills
        critical = [s for s in missing_skills if s["importance"] == "required"][:2]
        if critical:
            phases.append({
                "phase": "Phase 1 (Weeks 1-8)",
                "focus": "Critical Missing Skills",
                "skills": [s["skill"] for s in critical],
                "actions": "Take courses, build projects, get certified"
            })

        # Phase 2: Weak skills improvement
        if weak_skills:
            phases.append({
                "phase": "Phase 2 (Weeks 9-16)",
                "focus": "Skill Enhancement",
                "skills": [s["skill"] for s in weak_skills[:2]],
                "actions": "Advanced courses, complex projects, professional verification"
            })

        # Phase 3: Nice-to-have skills
        preferred = [s for s in missing_skills if s["importance"] == "preferred"][:2]
        if preferred:
            phases.append({
                "phase": "Phase 3 (Weeks 17-24)",
                "focus": "Preferred Skills",
                "skills": [s["skill"] for s in preferred],
                "actions": "Optional but valuable for competitive edge"
            })

        return {
            "total_phases": len(phases),
            "estimated_duration": f"{len(phases) * 8} weeks",
            "phases": phases
        }

    def _calculate_total_prep_time(self, missing_skills: List[Dict[str, Any]],
                                   weak_skills: List[Dict[str, Any]]) -> str:
        """Calculate total preparation time"""
        total_weeks = 0

        for skill in missing_skills[:3]:  # Top 3 critical
            total_weeks += 8  # 8 weeks per missing skill

        for skill in weak_skills[:2]:  # Top 2 weak
            total_weeks += 4  # 4 weeks to improve

        return f"{total_weeks} weeks at 10-15 hours/week"

    def _get_priority_actions(self, missing_skills: List[Dict[str, Any]],
                             weak_skills: List[Dict[str, Any]]) -> List[str]:
        """Get immediate priority actions"""
        actions = []

        if missing_skills:
            top_missing = missing_skills[0]
            actions.append(f"Start learning {top_missing['skill']} immediately (critical gap)")

        if weak_skills:
            top_weak = weak_skills[0]
            actions.append(f"Strengthen {top_weak['skill']}: {top_weak['current_level']} → {top_weak['required_level']}")

        actions.append("Get certifications for top 2 skills to verify proficiency")

        return actions

    def _create_verification_roadmap(self, missing_skills: List[Dict[str, Any]],
                                    weak_skills: List[Dict[str, Any]],
                                    sufficient_skills: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create skill verification roadmap"""
        roadmap = []

        # Verify sufficient skills first (quick wins)
        for skill in sufficient_skills[:2]:
            if skill["verification_status"] == "unverified":
                roadmap.append({
                    "priority": "high",
                    "skill": skill["skill"],
                    "current_level": skill["current_level"],
                    "action": "Get peer endorsements or certification",
                    "timeline": "1-2 weeks",
                    "rationale": "Quick verification of existing strength"
                })

        # Verify as you learn missing skills
        for skill in missing_skills[:2]:
            roadmap.append({
                "priority": "critical",
                "skill": skill["skill"],
                "current_level": "none",
                "action": "Learn skill, then get certified",
                "timeline": "8-12 weeks",
                "rationale": "Critical gap - learn and verify"
            })

        return roadmap

    def _assess_readiness(self, score: float) -> str:
        """Assess readiness based on score"""
        if score >= 90:
            return "Highly qualified - ready to apply"
        elif score >= 75:
            return "Well qualified - minor gaps"
        elif score >= 60:
            return "Moderately qualified - some gaps to address"
        elif score >= 40:
            return "Needs improvement - significant gaps"
        else:
            return "Not ready - major skill development needed"
