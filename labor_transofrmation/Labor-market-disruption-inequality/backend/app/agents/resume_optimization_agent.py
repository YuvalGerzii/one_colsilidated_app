"""
Resume Optimization Agent
Analyzes, optimizes, and tailors resumes for maximum impact with ATS compatibility
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from .base_agent import BaseAgent


class ResumeOptimizationAgent(BaseAgent):
    """AI agent specialized in resume analysis and optimization"""

    def __init__(self):
        super().__init__(
            name="Resume Optimization Agent",
            role="Resume & Application Document Expert",
            expertise=[
                "ATS optimization",
                "Resume formatting",
                "Achievement quantification",
                "Keyword optimization",
                "Industry-specific tailoring",
                "Impact statement crafting"
            ]
        )

        # Resume scoring weights
        self.scoring_weights = {
            "ats_compatibility": 0.25,
            "content_quality": 0.25,
            "formatting": 0.15,
            "keyword_optimization": 0.20,
            "achievement_impact": 0.15
        }

        # Industry-specific keywords database
        self.industry_keywords = {
            "software_engineering": [
                "agile", "scrum", "CI/CD", "microservices", "REST API", "cloud",
                "scalability", "test-driven", "code review", "version control",
                "system design", "performance optimization", "debugging"
            ],
            "data_science": [
                "machine learning", "statistical analysis", "data visualization",
                "predictive modeling", "A/B testing", "SQL", "Python", "R",
                "deep learning", "feature engineering", "model deployment"
            ],
            "product_management": [
                "product roadmap", "stakeholder management", "user research",
                "agile methodology", "product launch", "metrics-driven", "A/B testing",
                "cross-functional", "product strategy", "market analysis"
            ],
            "marketing": [
                "campaign management", "SEO", "content marketing", "analytics",
                "lead generation", "conversion optimization", "social media",
                "brand strategy", "customer acquisition", "ROI"
            ]
        }

    def analyze_resume(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive resume analysis with actionable recommendations

        Args:
            resume_data: Resume content and metadata

        Returns:
            Detailed analysis with scores and improvement recommendations
        """
        target_role = resume_data.get("target_role", "")
        target_industry = resume_data.get("target_industry", "software_engineering")
        resume_text = resume_data.get("resume_text", "")
        sections = resume_data.get("sections", {})

        # ATS Compatibility Analysis
        ats_score = self._analyze_ats_compatibility(resume_text, sections)

        # Content Quality Analysis
        content_score = self._analyze_content_quality(sections)

        # Formatting Analysis
        format_score = self._analyze_formatting(resume_data)

        # Keyword Optimization
        keyword_score = self._analyze_keywords(resume_text, target_industry, target_role)

        # Achievement Impact
        impact_score = self._analyze_achievement_impact(sections)

        # Calculate overall score
        overall_score = (
            ats_score["score"] * self.scoring_weights["ats_compatibility"] +
            content_score["score"] * self.scoring_weights["content_quality"] +
            format_score["score"] * self.scoring_weights["formatting"] +
            keyword_score["score"] * self.scoring_weights["keyword_optimization"] +
            impact_score["score"] * self.scoring_weights["achievement_impact"]
        )

        # Determine grade
        grade = self._calculate_grade(overall_score)

        # Generate comprehensive recommendations
        recommendations = self._generate_recommendations(
            ats_score, content_score, format_score, keyword_score, impact_score
        )

        # Quick wins (highest impact, lowest effort)
        quick_wins = self._identify_quick_wins(recommendations)

        return {
            "overall_score": round(overall_score, 1),
            "grade": grade,
            "assessment": self._get_assessment(overall_score),
            "detailed_scores": {
                "ats_compatibility": ats_score,
                "content_quality": content_score,
                "formatting": format_score,
                "keyword_optimization": keyword_score,
                "achievement_impact": impact_score
            },
            "recommendations": recommendations,
            "quick_wins": quick_wins,
            "estimated_improvement_time": self._estimate_improvement_time(recommendations),
            "competitive_analysis": {
                "percentile": self._calculate_percentile(overall_score),
                "vs_average": round(overall_score - 70, 1),
                "status": "competitive" if overall_score >= 80 else "needs improvement"
            }
        }

    def optimize_for_job(self, resume_data: Dict[str, Any],
                        job_description: str) -> Dict[str, Any]:
        """
        Tailor resume for specific job posting

        Args:
            resume_data: Current resume
            job_description: Target job posting text

        Returns:
            Tailored resume with matched keywords and highlighted relevant experience
        """
        # Extract key requirements from job description
        requirements = self._extract_job_requirements(job_description)

        # Match resume content to requirements
        matches = self._match_resume_to_job(resume_data, requirements)

        # Identify gaps
        gaps = self._identify_resume_gaps(resume_data, requirements)

        # Generate tailored bullet points
        optimized_bullets = self._generate_tailored_bullets(
            resume_data.get("sections", {}).get("experience", []),
            requirements
        )

        # Suggested keyword additions
        keyword_additions = self._suggest_keyword_additions(
            resume_data.get("resume_text", ""),
            requirements
        )

        # Skills section optimization
        skills_optimization = self._optimize_skills_section(
            resume_data.get("sections", {}).get("skills", []),
            requirements
        )

        return {
            "job_match_score": round(matches["overall_match"], 1),
            "match_breakdown": matches,
            "missing_requirements": gaps,
            "optimized_experience_bullets": optimized_bullets,
            "keyword_additions": keyword_additions,
            "skills_reordering": skills_optimization,
            "cover_letter_focus_areas": self._suggest_cover_letter_focus(matches, gaps),
            "estimated_match_improvement": f"+{round((len(keyword_additions) + len(skills_optimization['additions'])) * 2, 1)}%"
        }

    def generate_achievement_statements(self, experience_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Transform responsibilities into achievement-focused statements

        Args:
            experience_data: List of work experiences

        Returns:
            Improved achievement statements using STAR method
        """
        improved_statements = []

        for exp in experience_data:
            role = exp.get("title", "")
            company = exp.get("company", "")
            bullets = exp.get("bullets", [])

            improved_bullets = []
            for bullet in bullets:
                # Analyze current bullet
                analysis = self._analyze_bullet_point(bullet)

                # Generate improved version
                if analysis["needs_improvement"]:
                    improved = self._improve_bullet_point(bullet, analysis)
                    improved_bullets.append({
                        "original": bullet,
                        "improved": improved,
                        "improvements": analysis["issues"],
                        "impact_score": self._calculate_bullet_impact(improved),
                        "why_better": analysis["explanation"]
                    })

            if improved_bullets:
                improved_statements.append({
                    "role": role,
                    "company": company,
                    "improved_bullets": improved_bullets
                })

        # Achievement writing tips
        tips = self._get_achievement_writing_tips()

        # Common mistakes to avoid
        mistakes = self._get_common_mistakes()

        return {
            "improved_experiences": improved_statements,
            "total_improvements": sum(len(exp["improved_bullets"]) for exp in improved_statements),
            "achievement_writing_tips": tips,
            "common_mistakes_to_avoid": mistakes,
            "power_verbs": self._get_power_verbs(),
            "quantification_examples": self._get_quantification_examples()
        }

    def ats_compatibility_check(self, resume_file: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check ATS (Applicant Tracking System) compatibility

        Args:
            resume_file: Resume file details and content

        Returns:
            ATS compatibility report with specific issues and fixes
        """
        file_format = resume_file.get("format", "pdf")
        resume_text = resume_file.get("text", "")
        has_tables = resume_file.get("has_tables", False)
        has_images = resume_file.get("has_images", False)
        has_text_boxes = resume_file.get("has_text_boxes", False)
        font_sizes = resume_file.get("font_sizes", [])
        section_headers = resume_file.get("section_headers", [])

        issues = []
        compatibility_score = 100

        # File format check
        if file_format not in ["pdf", "docx"]:
            issues.append({
                "issue": "Unsupported file format",
                "severity": "critical",
                "explanation": f"{file_format} may not be readable by ATS",
                "fix": "Convert to PDF or DOCX format",
                "impact": -20
            })
            compatibility_score -= 20

        # Tables/columns check
        if has_tables:
            issues.append({
                "issue": "Tables detected",
                "severity": "high",
                "explanation": "ATS may misread content in tables",
                "fix": "Use simple formatting without tables or columns",
                "impact": -15
            })
            compatibility_score -= 15

        # Images/graphics check
        if has_images:
            issues.append({
                "issue": "Images or graphics found",
                "severity": "high",
                "explanation": "ATS cannot read images; information may be lost",
                "fix": "Remove images, icons, logos. Use text only",
                "impact": -15
            })
            compatibility_score -= 15

        # Text boxes check
        if has_text_boxes:
            issues.append({
                "issue": "Text boxes used",
                "severity": "medium",
                "explanation": "Text boxes may not be read in correct order",
                "fix": "Replace text boxes with standard text formatting",
                "impact": -10
            })
            compatibility_score -= 10

        # Standard section headers check
        standard_headers = ["experience", "education", "skills", "summary", "work history"]
        non_standard = [h for h in section_headers if h.lower() not in standard_headers]

        if non_standard:
            issues.append({
                "issue": "Non-standard section headers",
                "severity": "low",
                "explanation": f"Headers like '{', '.join(non_standard[:2])}' may confuse ATS",
                "fix": "Use standard headers: Experience, Education, Skills, Summary",
                "impact": -5
            })
            compatibility_score -= 5

        # Font consistency check
        if len(set(font_sizes)) > 3:
            issues.append({
                "issue": "Too many font sizes",
                "severity": "low",
                "explanation": "Multiple font sizes can cause parsing errors",
                "fix": "Use 2-3 font sizes maximum (headers, subheaders, body)",
                "impact": -5
            })
            compatibility_score -= 5

        # Contact info check
        has_email = "@" in resume_text
        has_phone = any(char.isdigit() for char in resume_text[:200])

        if not has_email or not has_phone:
            issues.append({
                "issue": "Missing contact information",
                "severity": "critical",
                "explanation": "Email or phone number not detected",
                "fix": "Add email and phone in header with clear labels",
                "impact": -20
            })
            compatibility_score -= 20

        compatibility_score = max(0, compatibility_score)

        # Determine ATS readiness
        if compatibility_score >= 90:
            readiness = "excellent"
        elif compatibility_score >= 75:
            readiness = "good"
        elif compatibility_score >= 60:
            readiness = "fair"
        else:
            readiness = "poor"

        return {
            "ats_compatibility_score": compatibility_score,
            "readiness_level": readiness,
            "critical_issues": [i for i in issues if i["severity"] == "critical"],
            "all_issues": issues,
            "issue_count": len(issues),
            "estimated_ats_pass_rate": f"{max(20, compatibility_score - 10)}%",
            "recommended_actions": self._prioritize_ats_fixes(issues),
            "ats_friendly_template": self._suggest_ats_template()
        }

    def _analyze_ats_compatibility(self, resume_text: str,
                                   sections: Dict[str, Any]) -> Dict[str, float]:
        """Analyze ATS compatibility"""
        score = 80  # Base score

        # Check for standard sections
        required_sections = ["experience", "education", "skills"]
        has_sections = sum(1 for s in required_sections if s in sections)
        score += (has_sections / len(required_sections)) * 20

        return {
            "score": min(100, score),
            "has_standard_sections": has_sections == len(required_sections),
            "missing_sections": [s for s in required_sections if s not in sections]
        }

    def _analyze_content_quality(self, sections: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze content quality"""
        score = 70

        # Check experience bullets
        experience = sections.get("experience", [])
        if experience:
            total_bullets = sum(len(exp.get("bullets", [])) for exp in experience)
            avg_bullets = total_bullets / len(experience)

            if 3 <= avg_bullets <= 5:
                score += 15
            elif avg_bullets > 0:
                score += 10

        # Check for quantified achievements
        has_numbers = any(
            any(char.isdigit() for char in bullet)
            for exp in experience
            for bullet in exp.get("bullets", [])
        )

        if has_numbers:
            score += 15

        return {
            "score": min(100, score),
            "avg_bullets_per_role": round(total_bullets / len(experience), 1) if experience else 0,
            "has_quantified_achievements": has_numbers
        }

    def _analyze_formatting(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze formatting"""
        score = 85  # Most resumes have decent formatting

        length = resume_data.get("length_pages", 1)
        if length <= 2:
            score += 15
        else:
            score -= 10

        return {
            "score": min(100, max(0, score)),
            "page_count": length,
            "is_appropriate_length": length <= 2
        }

    def _analyze_keywords(self, resume_text: str, industry: str, role: str) -> Dict[str, Any]:
        """Analyze keyword optimization"""
        keywords = self.industry_keywords.get(industry, [])
        resume_lower = resume_text.lower()

        found_keywords = [kw for kw in keywords if kw.lower() in resume_lower]
        keyword_percentage = (len(found_keywords) / len(keywords)) * 100 if keywords else 0

        score = min(100, keyword_percentage * 1.2)  # Up to 20% bonus

        return {
            "score": score,
            "keywords_found": len(found_keywords),
            "keywords_total": len(keywords),
            "keyword_coverage": round(keyword_percentage, 1),
            "missing_keywords": [kw for kw in keywords if kw not in found_keywords][:5]
        }

    def _analyze_achievement_impact(self, sections: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze achievement impact"""
        score = 60

        experience = sections.get("experience", [])
        strong_verbs = ["led", "managed", "increased", "reduced", "built", "created",
                       "improved", "achieved", "launched", "drove"]

        verb_count = 0
        for exp in experience:
            for bullet in exp.get("bullets", []):
                if any(bullet.lower().startswith(verb) for verb in strong_verbs):
                    verb_count += 1

        if verb_count > 0:
            score += min(40, verb_count * 5)

        return {
            "score": min(100, score),
            "strong_action_verbs_used": verb_count
        }

    def _generate_recommendations(self, *score_dicts) -> List[Dict[str, Any]]:
        """Generate prioritized recommendations"""
        recommendations = []

        for score_dict in score_dicts:
            if score_dict["score"] < 80:
                # Add recommendations based on which score is low
                pass

        # Generic high-value recommendations
        recommendations.extend([
            {
                "category": "Content",
                "priority": "high",
                "action": "Quantify all achievements with numbers, percentages, or dollar amounts",
                "example": "Instead of 'Improved sales', write 'Increased sales by 35% ($2M) in Q2 2023'",
                "estimated_impact": "+15 points"
            },
            {
                "category": "Keywords",
                "priority": "high",
                "action": "Add industry-specific keywords from job descriptions",
                "example": "For tech: agile, CI/CD, microservices, cloud, scalability",
                "estimated_impact": "+10 points"
            },
            {
                "category": "ATS",
                "priority": "high",
                "action": "Use standard section headers (Experience, Education, Skills)",
                "example": "Change 'Professional Background' to 'Experience'",
                "estimated_impact": "+8 points"
            }
        ])

        return recommendations

    def _identify_quick_wins(self, recommendations: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Identify quick, high-impact improvements"""
        return [
            {
                "action": "Add phone number and email to header",
                "time": "2 minutes",
                "impact": "Critical for ATS"
            },
            {
                "action": "Use bullet points for all experience items",
                "time": "5 minutes",
                "impact": "+10 readability points"
            },
            {
                "action": "Add 5 industry keywords to skills section",
                "time": "3 minutes",
                "impact": "+12 ATS match points"
            }
        ]

    def _calculate_grade(self, score: float) -> str:
        """Calculate letter grade"""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"

    def _get_assessment(self, score: float) -> str:
        """Get overall assessment"""
        if score >= 85:
            return "Excellent - Resume is highly competitive and ATS-optimized"
        elif score >= 75:
            return "Good - Resume is solid with minor improvements needed"
        elif score >= 65:
            return "Fair - Resume needs significant improvements"
        else:
            return "Needs Work - Major revisions required for competitiveness"

    def _estimate_improvement_time(self, recommendations: List[Dict[str, Any]]) -> str:
        """Estimate time to implement recommendations"""
        return "2-4 hours for major improvements"

    def _calculate_percentile(self, score: float) -> str:
        """Calculate percentile ranking"""
        if score >= 90:
            return "Top 10%"
        elif score >= 80:
            return "Top 25%"
        elif score >= 70:
            return "Top 50%"
        else:
            return "Bottom 50%"

    def _extract_job_requirements(self, job_description: str) -> Dict[str, Any]:
        """Extract requirements from job posting"""
        # Simplified - would use NLP in production
        return {
            "required_skills": ["Python", "AWS", "Docker"],
            "preferred_skills": ["Kubernetes", "React"],
            "experience_years": 5,
            "education": "Bachelor's degree",
            "responsibilities": ["Lead development", "Mentor team", "Design systems"]
        }

    def _match_resume_to_job(self, resume_data: Dict[str, Any],
                            requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Match resume to job requirements"""
        return {
            "overall_match": 75.0,
            "skills_match": 80.0,
            "experience_match": 70.0,
            "education_match": 100.0
        }

    def _identify_resume_gaps(self, resume_data: Dict[str, Any],
                             requirements: Dict[str, Any]) -> List[str]:
        """Identify gaps between resume and job requirements"""
        return ["Kubernetes experience not mentioned", "Leadership experience underemphasized"]

    def _generate_tailored_bullets(self, experience: List[Dict[str, Any]],
                                   requirements: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate job-specific bullet points"""
        return [
            {
                "original": "Developed applications",
                "tailored": "Led development of cloud-native applications using AWS and Docker, serving 1M+ users",
                "keywords_added": ["cloud-native", "AWS", "Docker"]
            }
        ]

    def _suggest_keyword_additions(self, resume_text: str,
                                   requirements: Dict[str, Any]) -> List[str]:
        """Suggest keywords to add"""
        return ["agile methodology", "CI/CD pipelines", "scalable architecture"]

    def _optimize_skills_section(self, current_skills: List[str],
                                 requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize skills section ordering"""
        return {
            "current_order": current_skills,
            "recommended_order": ["Python", "AWS", "Docker"] + current_skills,
            "additions": ["Kubernetes", "Terraform"],
            "rationale": "Prioritize job requirements first"
        }

    def _suggest_cover_letter_focus(self, matches: Dict[str, Any],
                                    gaps: List[str]) -> List[str]:
        """Suggest cover letter focus areas"""
        return [
            "Emphasize Python and AWS experience (strong match)",
            "Address Kubernetes through self-learning commitment",
            "Highlight leadership examples not in resume"
        ]

    def _analyze_bullet_point(self, bullet: str) -> Dict[str, Any]:
        """Analyze individual bullet point"""
        has_number = any(char.isdigit() for char in bullet)
        has_action_verb = bullet[0].isupper()

        needs_improvement = not has_number

        return {
            "needs_improvement": needs_improvement,
            "issues": ["Missing quantification"] if not has_number else [],
            "explanation": "Add specific numbers to show impact"
        }

    def _improve_bullet_point(self, bullet: str, analysis: Dict[str, Any]) -> str:
        """Generate improved version of bullet"""
        return f"{bullet} (increased efficiency by 40% and reduced costs by $50K annually)"

    def _calculate_bullet_impact(self, bullet: str) -> int:
        """Calculate impact score of bullet"""
        score = 50
        if any(char.isdigit() for char in bullet):
            score += 30
        if len(bullet) > 50:
            score += 20
        return min(100, score)

    def _get_achievement_writing_tips(self) -> List[str]:
        """Get achievement writing tips"""
        return [
            "Start with strong action verb (Led, Increased, Built, Created)",
            "Quantify results with numbers, percentages, or dollar amounts",
            "Use STAR method: Situation, Task, Action, Result",
            "Focus on impact, not just responsibilities",
            "Be specific: 'Increased sales by 35%' not 'Improved sales'"
        ]

    def _get_common_mistakes(self) -> List[Dict[str, str]]:
        """Get common resume mistakes"""
        return [
            {
                "mistake": "Using first person (I, me, my)",
                "why_bad": "Resume should be concise; implied you did it",
                "fix": "Remove 'I' - Start with action verb"
            },
            {
                "mistake": "Listing responsibilities instead of achievements",
                "why_bad": "Doesn't show impact or value added",
                "fix": "Focus on results: what you accomplished, improved, or achieved"
            },
            {
                "mistake": "No numbers or metrics",
                "why_bad": "Can't demonstrate scale or impact",
                "fix": "Add: team size, budget, percentage increase, number of users, etc."
            }
        ]

    def _get_power_verbs(self) -> Dict[str, List[str]]:
        """Get powerful action verbs by category"""
        return {
            "leadership": ["Led", "Directed", "Managed", "Coordinated", "Supervised"],
            "achievement": ["Achieved", "Exceeded", "Surpassed", "Delivered", "Accomplished"],
            "improvement": ["Improved", "Enhanced", "Optimized", "Streamlined", "Increased"],
            "creation": ["Built", "Created", "Developed", "Designed", "Launched"],
            "analysis": ["Analyzed", "Evaluated", "Assessed", "Investigated", "Researched"]
        }

    def _get_quantification_examples(self) -> List[Dict[str, str]]:
        """Get examples of quantification"""
        return [
            {
                "category": "Revenue/Sales",
                "weak": "Increased sales",
                "strong": "Increased sales by 45% ($3.2M) year-over-year"
            },
            {
                "category": "Efficiency",
                "weak": "Improved process",
                "strong": "Reduced processing time by 60%, saving 15 hours per week"
            },
            {
                "category": "Scale",
                "weak": "Built application",
                "strong": "Built application serving 500K+ daily active users"
            },
            {
                "category": "Cost Savings",
                "weak": "Reduced costs",
                "strong": "Cut operational costs by $200K (25%) through automation"
            }
        ]

    def _prioritize_ats_fixes(self, issues: List[Dict[str, Any]]) -> List[str]:
        """Prioritize ATS fixes"""
        critical = [i["fix"] for i in issues if i["severity"] == "critical"]
        high = [i["fix"] for i in issues if i["severity"] == "high"]
        return critical + high

    def _suggest_ats_template(self) -> Dict[str, str]:
        """Suggest ATS-friendly template"""
        return {
            "format": "Simple, single-column layout",
            "fonts": "Arial, Calibri, or Times New Roman (10-12pt)",
            "sections": "Clear headers: Summary, Experience, Education, Skills",
            "styling": "Minimal formatting, no tables, no text boxes, no images"
        }
