"""
Interview Preparation System
Comprehensive mock interviews, question banks, performance analysis, and coaching
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from enum import Enum
import random


class InterviewType(str, Enum):
    BEHAVIORAL = "behavioral"
    TECHNICAL = "technical"
    SYSTEM_DESIGN = "system_design"
    CASE = "case"
    CODING = "coding"
    CULTURE_FIT = "culture_fit"


class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"


class PerformanceRating(str, Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    NEEDS_IMPROVEMENT = "needs_improvement"
    POOR = "poor"


class InterviewPreparationSystem:
    """Comprehensive interview preparation and coaching system"""

    def __init__(self):
        # Question banks by type
        self.behavioral_questions = self._initialize_behavioral_questions()
        self.technical_questions = self._initialize_technical_questions()
        self.system_design_questions = self._initialize_system_design_questions()
        self.culture_fit_questions = self._initialize_culture_fit_questions()

        # Evaluation criteria
        self.evaluation_criteria = {
            "technical_accuracy": 0.30,
            "communication": 0.25,
            "problem_solving": 0.25,
            "confidence": 0.10,
            "enthusiasm": 0.10
        }

    def generate_mock_interview(self, interview_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate personalized mock interview

        Args:
            interview_data: Interview type, role, difficulty, duration

        Returns:
            Complete mock interview with questions and evaluation criteria
        """
        interview_type = interview_data.get("interview_type", InterviewType.BEHAVIORAL.value)
        role = interview_data.get("role", "software_engineer")
        difficulty = interview_data.get("difficulty", DifficultyLevel.MEDIUM.value)
        duration_minutes = interview_data.get("duration_minutes", 60)

        # Select appropriate questions
        questions = self._select_questions(
            interview_type, role, difficulty, duration_minutes
        )

        # Create interview structure
        interview_structure = self._create_interview_structure(
            questions, duration_minutes, interview_type
        )

        # Evaluation rubric
        rubric = self._create_evaluation_rubric(interview_type)

        # Preparation tips
        prep_tips = self._get_prep_tips(interview_type, difficulty)

        # Common pitfalls
        pitfalls = self._get_common_pitfalls(interview_type)

        return {
            "interview_id": f"mock_{interview_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "interview_type": interview_type,
            "role": role,
            "difficulty": difficulty,
            "estimated_duration": f"{duration_minutes} minutes",
            "interview_structure": interview_structure,
            "evaluation_rubric": rubric,
            "preparation_tips": prep_tips,
            "common_pitfalls_to_avoid": pitfalls,
            "best_practices": self._get_best_practices(interview_type),
            "practice_recommendations": {
                "recommended_practice_sessions": 3,
                "focus_areas": self._identify_focus_areas(interview_data),
                "estimated_prep_time": f"{self._estimate_prep_time(interview_type, difficulty)} hours"
            }
        }

    def evaluate_interview_performance(self, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate mock interview performance

        Args:
            performance_data: Responses, ratings, feedback

        Returns:
            Detailed performance analysis with improvement recommendations
        """
        interview_type = performance_data.get("interview_type", "behavioral")
        responses = performance_data.get("responses", [])

        # Score each dimension
        scores = {}
        for criterion, weight in self.evaluation_criteria.items():
            score = performance_data.get(f"{criterion}_score", 7)  # Default 7/10
            scores[criterion] = {
                "score": score,
                "out_of": 10,
                "percentage": (score / 10) * 100,
                "weight": weight
            }

        # Calculate overall score
        overall_score = sum(
            scores[criterion]["score"] * weight
            for criterion, weight in self.evaluation_criteria.items()
        )
        overall_percentage = (overall_score / 10) * 100

        # Determine performance rating
        if overall_percentage >= 90:
            rating = PerformanceRating.EXCELLENT
        elif overall_percentage >= 75:
            rating = PerformanceRating.GOOD
        elif overall_percentage >= 60:
            rating = PerformanceRating.FAIR
        elif overall_percentage >= 45:
            rating = PerformanceRating.NEEDS_IMPROVEMENT
        else:
            rating = PerformanceRating.POOR

        # Identify strengths and weaknesses
        strengths = [
            criterion for criterion, data in scores.items()
            if data["percentage"] >= 80
        ]
        weaknesses = [
            criterion for criterion, data in scores.items()
            if data["percentage"] < 60
        ]

        # Generate improvement plan
        improvement_plan = self._generate_improvement_plan(
            weaknesses, interview_type, overall_percentage
        )

        # Specific feedback on responses
        response_feedback = self._analyze_responses(responses, interview_type)

        # Compare to benchmarks
        benchmark = self._get_performance_benchmark(interview_type)

        return {
            "overall_score": round(overall_score, 2),
            "overall_percentage": round(overall_percentage, 1),
            "performance_rating": rating.value,
            "rating_explanation": self._explain_rating(rating),
            "dimension_scores": scores,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "response_feedback": response_feedback,
            "improvement_plan": improvement_plan,
            "benchmark_comparison": {
                "your_score": round(overall_percentage, 1),
                "average_score": benchmark["average"],
                "top_10_percent": benchmark["top_10"],
                "vs_average": round(overall_percentage - benchmark["average"], 1)
            },
            "next_steps": self._get_next_steps(rating, weaknesses),
            "estimated_interviews_until_ready": self._estimate_readiness(overall_percentage)
        }

    def get_question_bank(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get curated question bank based on filters

        Args:
            filters: Interview type, role, difficulty, company type

        Returns:
            Filtered question bank with sample answers
        """
        interview_type = filters.get("interview_type", "behavioral")
        role = filters.get("role", "")
        difficulty = filters.get("difficulty", "medium")
        company_type = filters.get("company_type", "")  # startup, big_tech, etc.

        # Select questions based on type
        if interview_type == InterviewType.BEHAVIORAL.value:
            questions = self._filter_behavioral_questions(role, difficulty, company_type)
        elif interview_type == InterviewType.TECHNICAL.value:
            questions = self._filter_technical_questions(role, difficulty)
        elif interview_type == InterviewType.SYSTEM_DESIGN.value:
            questions = self.system_design_questions
        else:
            questions = self.culture_fit_questions

        # Add framework for answering
        for q in questions:
            q["answer_framework"] = self._get_answer_framework(interview_type)
            q["sample_answer"] = self._generate_sample_answer(q, interview_type)
            q["evaluation_criteria"] = self._get_question_criteria(q, interview_type)

        return {
            "interview_type": interview_type,
            "total_questions": len(questions),
            "questions": questions[:20],  # Return top 20
            "answer_frameworks": {
                "STAR": "Situation, Task, Action, Result - for behavioral questions",
                "Problem-Solution-Impact": "For technical/problem-solving questions",
                "Clarify-Plan-Execute-Verify": "For coding questions"
            },
            "practice_schedule": self._create_practice_schedule(len(questions)),
            "mastery_tips": self._get_mastery_tips(interview_type)
        }

    def coach_answer(self, question: str, user_answer: str,
                    interview_type: str) -> Dict[str, Any]:
        """
        Provide coaching on user's answer

        Args:
            question: Interview question
            user_answer: User's response
            interview_type: Type of interview

        Returns:
            Detailed feedback and improvement suggestions
        """
        # Analyze answer components
        analysis = self._analyze_answer(user_answer, interview_type)

        # Score the answer (0-10)
        score = analysis["score"]

        # Generate specific feedback
        feedback = {
            "what_worked_well": analysis["strengths"],
            "what_to_improve": analysis["weaknesses"],
            "missing_elements": analysis["missing"],
            "suggested_improvements": analysis["improvements"]
        }

        # Provide improved version
        improved_answer = self._generate_improved_answer(
            question, user_answer, interview_type, analysis
        )

        # Delivery coaching
        delivery_tips = self._get_delivery_coaching(analysis)

        return {
            "original_question": question,
            "your_answer": user_answer,
            "score": score,
            "out_of": 10,
            "rating": self._score_to_rating(score),
            "detailed_feedback": feedback,
            "improved_answer_example": improved_answer,
            "delivery_coaching": delivery_tips,
            "practice_exercises": self._get_practice_exercises(interview_type, analysis),
            "next_practice_question": self._get_next_practice_question(question, interview_type)
        }

    def company_specific_prep(self, company_name: str,
                             role: str) -> Dict[str, Any]:
        """
        Company-specific interview preparation

        Args:
            company_name: Target company
            role: Target role

        Returns:
            Company-specific interview insights and preparation
        """
        # Company culture and values (would pull from database)
        company_info = self._get_company_info(company_name)

        # Common interview questions for this company
        common_questions = self._get_company_common_questions(company_name, role)

        # Interview process breakdown
        process = self._get_interview_process(company_name, role)

        # Insider tips
        insider_tips = self._get_insider_tips(company_name)

        # Key skills to emphasize
        key_skills = self._get_company_key_skills(company_name, role)

        return {
            "company": company_name,
            "role": role,
            "company_overview": company_info,
            "interview_process": process,
            "commonly_asked_questions": common_questions,
            "key_skills_to_emphasize": key_skills,
            "culture_values_fit": {
                "company_values": company_info.get("values", []),
                "how_to_demonstrate": self._map_values_to_stories(company_info.get("values", []))
            },
            "insider_tips": insider_tips,
            "recent_interview_experiences": self._get_recent_experiences(company_name),
            "preparation_checklist": self._create_company_prep_checklist(company_name, role)
        }

    def track_interview_progress(self, worker_id: int) -> Dict[str, Any]:
        """
        Track interview preparation progress

        Args:
            worker_id: Worker identifier

        Returns:
            Progress tracking and readiness assessment
        """
        # Mock data - would pull from database
        mock_interviews_completed = 8
        questions_practiced = 45
        avg_score = 7.8
        improvement_trend = +1.2  # Points improved over time

        # Calculate readiness score (0-100)
        readiness_score = min(100, (
            (mock_interviews_completed * 8) +
            (questions_practiced * 0.5) +
            (avg_score * 3) +
            (improvement_trend * 10)
        ))

        # Determine readiness level
        if readiness_score >= 85:
            readiness_level = "Interview Ready"
            recommendation = "You're ready! Schedule interviews with confidence."
        elif readiness_score >= 70:
            readiness_level = "Nearly Ready"
            recommendation = "2-3 more practice sessions and you'll be ready."
        elif readiness_score >= 50:
            readiness_level = "Moderate Preparation"
            recommendation = "Continue practicing. Focus on weak areas."
        else:
            readiness_level = "Needs More Practice"
            recommendation = "Invest more time in mock interviews and question practice."

        # Skill breakdown
        skill_scores = {
            "behavioral_questions": 82,
            "technical_questions": 75,
            "communication": 88,
            "problem_solving": 79,
            "confidence": 85
        }

        # Identify gaps
        gaps = [skill for skill, score in skill_scores.items() if score < 75]

        return {
            "readiness_score": round(readiness_score, 1),
            "readiness_level": readiness_level,
            "recommendation": recommendation,
            "statistics": {
                "mock_interviews_completed": mock_interviews_completed,
                "questions_practiced": questions_practiced,
                "average_score": avg_score,
                "improvement_trend": f"+{improvement_trend} points",
                "total_practice_hours": round(mock_interviews_completed * 1.5 + questions_practiced * 0.1, 1)
            },
            "skill_breakdown": skill_scores,
            "skill_gaps": gaps,
            "practice_history": self._get_practice_history(worker_id),
            "upcoming_milestones": [
                {"milestone": "Complete 10 mock interviews", "progress": f"{mock_interviews_completed}/10"},
                {"milestone": "Practice 50 questions", "progress": f"{questions_practiced}/50"},
                {"milestone": "Achieve 8.5 avg score", "progress": f"{avg_score}/8.5"}
            ],
            "recommended_next_practice": self._recommend_next_practice(skill_scores)
        }

    def _initialize_behavioral_questions(self) -> List[Dict[str, Any]]:
        """Initialize behavioral question bank"""
        return [
            {
                "question": "Tell me about a time you faced a significant challenge at work. How did you handle it?",
                "category": "problem_solving",
                "difficulty": "medium",
                "key_elements": ["situation", "challenge", "action", "result"],
                "companies_ask": ["Google", "Amazon", "Meta", "Microsoft"]
            },
            {
                "question": "Describe a situation where you had to work with a difficult team member.",
                "category": "teamwork",
                "difficulty": "medium",
                "key_elements": ["conflict", "resolution", "outcome", "learning"],
                "companies_ask": ["most companies"]
            },
            {
                "question": "Tell me about a time you failed. What did you learn?",
                "category": "growth_mindset",
                "difficulty": "hard",
                "key_elements": ["failure", "reflection", "learning", "application"],
                "companies_ask": ["Google", "Amazon", "Meta"]
            },
            {
                "question": "Describe a time when you had to make a decision without complete information.",
                "category": "decision_making",
                "difficulty": "hard",
                "key_elements": ["ambiguity", "reasoning", "action", "outcome"],
                "companies_ask": ["Amazon", "Meta", "startups"]
            },
            {
                "question": "Tell me about a time you had to persuade someone to see your point of view.",
                "category": "influence",
                "difficulty": "medium",
                "key_elements": ["situation", "approach", "persuasion_tactics", "result"],
                "companies_ask": ["most companies"]
            }
        ]

    def _initialize_technical_questions(self) -> List[Dict[str, Any]]:
        """Initialize technical question bank"""
        return [
            {
                "question": "Explain how you would optimize a slow database query.",
                "category": "performance",
                "difficulty": "medium",
                "topics": ["databases", "optimization", "indexing"],
                "role": "backend_engineer"
            },
            {
                "question": "How would you design a rate limiter?",
                "category": "system_design",
                "difficulty": "hard",
                "topics": ["distributed_systems", "algorithms"],
                "role": "software_engineer"
            },
            {
                "question": "Explain the difference between async/await and promises in JavaScript.",
                "category": "language_specific",
                "difficulty": "easy",
                "topics": ["javascript", "async_programming"],
                "role": "frontend_engineer"
            }
        ]

    def _initialize_system_design_questions(self) -> List[Dict[str, Any]]:
        """Initialize system design question bank"""
        return [
            {
                "question": "Design a URL shortening service like bit.ly",
                "difficulty": "medium",
                "key_components": ["API design", "database schema", "caching", "scalability"],
                "scale": "100M URLs/day"
            },
            {
                "question": "Design Instagram's feed system",
                "difficulty": "hard",
                "key_components": ["feed generation", "ranking", "caching", "real-time updates"],
                "scale": "1B users"
            },
            {
                "question": "Design a distributed task scheduler",
                "difficulty": "hard",
                "key_components": ["task queue", "worker management", "failure handling"],
                "scale": "10K tasks/second"
            }
        ]

    def _initialize_culture_fit_questions(self) -> List[Dict[str, Any]]:
        """Initialize culture fit question bank"""
        return [
            {
                "question": "Why do you want to work here?",
                "category": "motivation",
                "difficulty": "easy",
                "what_theyre_assessing": "Genuine interest, company research, alignment"
            },
            {
                "question": "What are you looking for in your next role?",
                "category": "goals",
                "difficulty": "easy",
                "what_theyre_assessing": "Career goals, job fit, growth mindset"
            },
            {
                "question": "Describe your ideal work environment.",
                "category": "culture_fit",
                "difficulty": "medium",
                "what_theyre_assessing": "Culture alignment, work style, values"
            }
        ]

    def _select_questions(self, interview_type: str, role: str,
                         difficulty: str, duration: int) -> List[Dict[str, Any]]:
        """Select appropriate questions for mock interview"""
        # Calculate number of questions based on duration
        if interview_type == InterviewType.BEHAVIORAL.value:
            questions_count = duration // 15  # 15 min per behavioral question
            pool = self.behavioral_questions
        elif interview_type == InterviewType.TECHNICAL.value:
            questions_count = duration // 20  # 20 min per technical question
            pool = self.technical_questions
        elif interview_type == InterviewType.SYSTEM_DESIGN.value:
            questions_count = 1  # Usually one system design question
            pool = self.system_design_questions
        else:
            questions_count = duration // 10
            pool = self.culture_fit_questions

        # Filter by difficulty
        filtered = [q for q in pool if q.get("difficulty", "medium") == difficulty]
        if not filtered:
            filtered = pool

        # Select random questions
        selected = random.sample(filtered, min(questions_count, len(filtered)))
        return selected

    def _create_interview_structure(self, questions: List[Dict[str, Any]],
                                   duration: int, interview_type: str) -> List[Dict[str, Any]]:
        """Create structured interview timeline"""
        structure = []

        # Introduction (5 min)
        structure.append({
            "phase": "Introduction",
            "duration_minutes": 5,
            "description": "Interviewer introduces themselves, explains interview format",
            "your_task": "Brief self-introduction (2 minutes max)"
        })

        # Questions
        time_per_question = (duration - 10) // len(questions) if questions else 10
        for i, question in enumerate(questions, 1):
            structure.append({
                "phase": f"Question {i}",
                "duration_minutes": time_per_question,
                "question": question.get("question", ""),
                "your_task": "Answer using appropriate framework (STAR for behavioral)",
                "tips": question.get("tips", "Be specific, quantify results")
            })

        # Closing (5 min)
        structure.append({
            "phase": "Your Questions",
            "duration_minutes": 5,
            "description": "Time for you to ask questions",
            "recommended_questions": [
                "What does success look like in this role in the first 6 months?",
                "What are the biggest challenges facing the team right now?",
                "How does the team collaborate and communicate?"
            ]
        })

        return structure

    def _create_evaluation_rubric(self, interview_type: str) -> Dict[str, Any]:
        """Create evaluation rubric for interview"""
        rubrics = {
            "behavioral": {
                "criteria": {
                    "STAR Structure": "Did you use Situation, Task, Action, Result?",
                    "Specificity": "Did you provide concrete details and numbers?",
                    "Impact": "Did you quantify the results?",
                    "Learning": "Did you show growth and reflection?",
                    "Clarity": "Was the story clear and easy to follow?"
                },
                "scoring": "Each criterion scored 1-10"
            },
            "technical": {
                "criteria": {
                    "Technical Accuracy": "Is the solution correct?",
                    "Communication": "Did you explain your thinking?",
                    "Problem Solving": "Did you break down the problem?",
                    "Trade-offs": "Did you discuss alternatives?",
                    "Code Quality": "Clean, readable code?"
                },
                "scoring": "Each criterion scored 1-10"
            }
        }

        return rubrics.get(interview_type, rubrics["behavioral"])

    def _get_prep_tips(self, interview_type: str, difficulty: str) -> List[str]:
        """Get preparation tips for interview type"""
        tips = {
            "behavioral": [
                "Prepare 5-7 STAR stories covering different situations",
                "Practice out loud - timing matters",
                "Quantify results with specific numbers",
                "Show learning and growth from each experience",
                "Be authentic - don't make up stories"
            ],
            "technical": [
                "Review fundamental CS concepts (data structures, algorithms)",
                "Practice coding on whiteboard or paper",
                "Think out loud - explain your reasoning",
                "Ask clarifying questions before jumping in",
                "Test your solution with edge cases"
            ],
            "system_design": [
                "Start with requirements and constraints",
                "Draw diagrams - visualize the system",
                "Discuss trade-offs of different approaches",
                "Consider scalability and failure modes",
                "Don't jump to implementation too quickly"
            ]
        }

        general_tips = tips.get(interview_type, [])

        if difficulty == "hard":
            general_tips.append("Expect follow-up questions that dig deeper")
            general_tips.append("Practice explaining complex topics simply")

        return general_tips

    def _get_common_pitfalls(self, interview_type: str) -> List[Dict[str, str]]:
        """Get common pitfalls to avoid"""
        pitfalls = {
            "behavioral": [
                {
                    "pitfall": "Being too vague",
                    "example": "We improved performance",
                    "fix": "We reduced page load time from 5s to 1.2s, improving conversion by 23%"
                },
                {
                    "pitfall": "Taking too long",
                    "example": "5+ minute rambling answer",
                    "fix": "Keep answers to 2-3 minutes, hit the key points"
                },
                {
                    "pitfall": "Not using STAR framework",
                    "example": "Jumping straight to what you did",
                    "fix": "Set context first: situation and task, then action and result"
                }
            ],
            "technical": [
                {
                    "pitfall": "Jumping to code immediately",
                    "example": "Start coding without understanding problem",
                    "fix": "Ask clarifying questions, discuss approach first"
                },
                {
                    "pitfall": "Staying silent",
                    "example": "Writing code in silence",
                    "fix": "Think out loud, explain your reasoning"
                }
            ]
        }

        return pitfalls.get(interview_type, pitfalls["behavioral"])

    def _get_best_practices(self, interview_type: str) -> List[str]:
        """Get best practices for interview type"""
        practices = [
            "Make eye contact and smile",
            "Take a breath before answering",
            "It's okay to say 'That's a great question, let me think for a moment'",
            "Ask clarifying questions if needed",
            "Be enthusiastic and show genuine interest",
            "End with a strong close: 'I'm very excited about this opportunity'"
        ]

        if interview_type == "technical":
            practices.extend([
                "Draw diagrams to visualize the problem",
                "Test your solution with examples",
                "Discuss time and space complexity"
            ])

        return practices

    def _identify_focus_areas(self, interview_data: Dict[str, Any]) -> List[str]:
        """Identify areas to focus on during prep"""
        role = interview_data.get("role", "")
        weak_areas = interview_data.get("weak_areas", [])

        focus = []
        if "behavioral" in interview_data.get("interview_type", ""):
            focus.append("STAR story preparation")

        if weak_areas:
            focus.extend([f"Improve {area}" for area in weak_areas])

        if not focus:
            focus = ["Overall interview confidence", "Answer structure", "Communication clarity"]

        return focus[:5]

    def _estimate_prep_time(self, interview_type: str, difficulty: str) -> int:
        """Estimate hours needed for preparation"""
        base_hours = {
            "behavioral": 8,
            "technical": 20,
            "system_design": 15,
            "coding": 30
        }

        hours = base_hours.get(interview_type, 10)

        if difficulty == "hard":
            hours = int(hours * 1.5)
        elif difficulty == "easy":
            hours = int(hours * 0.7)

        return hours

    def _generate_improvement_plan(self, weaknesses: List[str],
                                   interview_type: str,
                                   overall_score: float) -> List[Dict[str, Any]]:
        """Generate personalized improvement plan"""
        plan = []

        for weakness in weaknesses:
            if weakness == "technical_accuracy":
                plan.append({
                    "area": "Technical Accuracy",
                    "priority": "high",
                    "action": "Review fundamental concepts and practice coding problems daily",
                    "resources": ["LeetCode", "System Design Primer", "CS fundamentals course"],
                    "time_investment": "1-2 hours/day for 2 weeks"
                })
            elif weakness == "communication":
                plan.append({
                    "area": "Communication",
                    "priority": "high",
                    "action": "Practice explaining technical concepts out loud",
                    "resources": ["Mock interviews with peers", "Record yourself practicing"],
                    "time_investment": "30 min/day for 1 week"
                })
            elif weakness == "problem_solving":
                plan.append({
                    "area": "Problem Solving",
                    "priority": "medium",
                    "action": "Focus on breaking down problems before solving",
                    "resources": ["Practice problems", "Think-aloud protocol"],
                    "time_investment": "1 hour/day for 1 week"
                })

        if overall_score < 60:
            plan.append({
                "area": "Overall Interview Skills",
                "priority": "critical",
                "action": "Complete 3-5 more mock interviews before real interviews",
                "resources": ["Pramp", "Interviewing.io", "Friends/mentors"],
                "time_investment": "3-5 hours over next 2 weeks"
            })

        return plan

    def _analyze_responses(self, responses: List[Dict[str, Any]],
                          interview_type: str) -> List[Dict[str, Any]]:
        """Analyze individual responses"""
        feedback = []

        for i, response in enumerate(responses[:5], 1):  # Top 5 responses
            analysis = {
                "question_number": i,
                "question": response.get("question", ""),
                "your_answer_length": f"{len(response.get('answer', ''))} characters",
                "strengths": response.get("strengths", ["Good structure", "Clear communication"]),
                "improvements": response.get("improvements", ["Add more specific metrics", "Shorten slightly"]),
                "score": response.get("score", 7),
                "interviewer_notes": response.get("notes", "Good answer overall")
            }
            feedback.append(analysis)

        return feedback

    def _get_performance_benchmark(self, interview_type: str) -> Dict[str, float]:
        """Get performance benchmarks"""
        benchmarks = {
            "behavioral": {"average": 72, "top_10": 88},
            "technical": {"average": 68, "top_10": 85},
            "system_design": {"average": 65, "top_10": 82}
        }
        return benchmarks.get(interview_type, {"average": 70, "top_10": 85})

    def _explain_rating(self, rating: PerformanceRating) -> str:
        """Explain performance rating"""
        explanations = {
            PerformanceRating.EXCELLENT: "Outstanding performance. You're ready for interviews!",
            PerformanceRating.GOOD: "Strong performance. A bit more practice and you'll be excellent.",
            PerformanceRating.FAIR: "Decent performance but significant room for improvement.",
            PerformanceRating.NEEDS_IMPROVEMENT: "Below average. Focus on key weaknesses before interviewing.",
            PerformanceRating.POOR: "Needs substantial improvement. Invest more time in preparation."
        }
        return explanations.get(rating, "")

    def _get_next_steps(self, rating: PerformanceRating,
                       weaknesses: List[str]) -> List[str]:
        """Get next steps based on performance"""
        if rating in [PerformanceRating.EXCELLENT, PerformanceRating.GOOD]:
            return [
                "You're ready! Start scheduling real interviews",
                "Do 1-2 more practice sessions to stay sharp",
                "Review company-specific questions before each interview"
            ]
        else:
            steps = [
                f"Focus on improving: {', '.join(weaknesses)}",
                "Complete 3-5 more mock interviews",
                "Practice answers out loud daily"
            ]
            if rating == PerformanceRating.POOR:
                steps.append("Consider working with an interview coach")
            return steps

    def _estimate_readiness(self, overall_percentage: float) -> str:
        """Estimate how many more practice interviews needed"""
        if overall_percentage >= 85:
            return "Ready now! 0-1 more practice sessions recommended"
        elif overall_percentage >= 70:
            return "2-3 more practice sessions"
        elif overall_percentage >= 55:
            return "5-7 more practice sessions"
        else:
            return "10+ practice sessions recommended"

    def _filter_behavioral_questions(self, role: str, difficulty: str,
                                    company_type: str) -> List[Dict[str, Any]]:
        """Filter behavioral questions"""
        return [q for q in self.behavioral_questions
                if q.get("difficulty", "medium") == difficulty]

    def _filter_technical_questions(self, role: str,
                                    difficulty: str) -> List[Dict[str, Any]]:
        """Filter technical questions"""
        return [q for q in self.technical_questions
                if q.get("difficulty", "medium") == difficulty]

    def _get_answer_framework(self, interview_type: str) -> str:
        """Get answer framework for interview type"""
        frameworks = {
            "behavioral": "STAR: Situation, Task, Action, Result",
            "technical": "Clarify → Plan → Execute → Verify",
            "system_design": "Requirements → High-Level Design → Deep Dive → Trade-offs"
        }
        return frameworks.get(interview_type, "Clear structure with examples")

    def _generate_sample_answer(self, question: Dict[str, Any],
                               interview_type: str) -> str:
        """Generate sample answer for question"""
        # Simplified - would have actual sample answers
        return f"[Sample answer would demonstrate the {interview_type} framework with this question]"

    def _get_question_criteria(self, question: Dict[str, Any],
                              interview_type: str) -> List[str]:
        """Get evaluation criteria for specific question"""
        return ["Clarity", "Completeness", "Structure", "Examples/Metrics"]

    def _create_practice_schedule(self, total_questions: int) -> Dict[str, Any]:
        """Create practice schedule"""
        weeks_needed = (total_questions // 5) + 1
        return {
            "total_questions": total_questions,
            "recommended_schedule": f"{weeks_needed} weeks",
            "questions_per_week": 5,
            "daily_practice": "1 question per day (30-45 min)"
        }

    def _get_mastery_tips(self, interview_type: str) -> List[str]:
        """Get mastery tips"""
        return [
            "Practice consistently - daily is better than cramming",
            "Record yourself and watch it back",
            "Get feedback from peers or mentors",
            "Focus on common questions first",
            "Build a library of stories/examples to adapt"
        ]

    def _analyze_answer(self, answer: str, interview_type: str) -> Dict[str, Any]:
        """Analyze user's answer"""
        # Simplified analysis based on answer length and keywords
        word_count = len(answer.split())

        score = 7  # Base score
        strengths = []
        weaknesses = []
        missing = []
        improvements = []

        # Check length
        if word_count < 50:
            weaknesses.append("Answer is too brief")
            score -= 1.5
            improvements.append("Expand with more details and examples")
        elif word_count > 300:
            weaknesses.append("Answer is too long")
            score -= 0.5
            improvements.append("Be more concise, focus on key points")
        else:
            strengths.append("Good answer length")

        # Check for STAR elements (behavioral)
        if interview_type == "behavioral":
            has_situation = any(word in answer.lower() for word in ["situation", "when", "time"])
            has_result = any(word in answer.lower() for word in ["result", "outcome", "achieved", "%", "increased"])

            if has_situation:
                strengths.append("Clear situation/context")
                score += 0.5
            else:
                missing.append("Situation/context")
                score -= 1

            if has_result:
                strengths.append("Quantified results")
                score += 1
            else:
                missing.append("Quantified results")
                improvements.append("Add specific metrics and outcomes")
                score -= 1.5

        # Check for technical terms (technical)
        if interview_type == "technical":
            if any(word in answer.lower() for word in ["algorithm", "complexity", "data structure"]):
                strengths.append("Good technical terminology")
                score += 0.5

        score = max(0, min(10, score))

        return {
            "score": round(score, 1),
            "strengths": strengths,
            "weaknesses": weaknesses,
            "missing": missing,
            "improvements": improvements
        }

    def _generate_improved_answer(self, question: str, user_answer: str,
                                 interview_type: str,
                                 analysis: Dict[str, Any]) -> str:
        """Generate improved version of answer"""
        improvements = analysis.get("improvements", [])

        improved = f"[Improved version incorporating: {', '.join(improvements)}]\n\n"
        improved += f"Based on your answer, here's an enhanced version:\n{user_answer}\n\n"
        improved += "[Additional elements to add: specific metrics, clear STAR structure, stronger conclusion]"

        return improved

    def _get_delivery_coaching(self, analysis: Dict[str, Any]) -> List[Dict[str, str]]:
        """Get coaching on delivery"""
        return [
            {
                "aspect": "Pace",
                "tip": "Speak at moderate pace - not too fast (nervous) or too slow (boring)"
            },
            {
                "aspect": "Energy",
                "tip": "Show enthusiasm! Energy is contagious"
            },
            {
                "aspect": "Eye Contact",
                "tip": "Maintain eye contact 70-80% of the time"
            },
            {
                "aspect": "Pausing",
                "tip": "It's okay to pause and think. Better than 'um' and 'uh'"
            }
        ]

    def _get_practice_exercises(self, interview_type: str,
                               analysis: Dict[str, Any]) -> List[str]:
        """Get practice exercises based on weaknesses"""
        exercises = [
            "Record yourself answering this question again",
            "Practice the improved version out loud 3 times",
            "Get feedback from a friend or mentor"
        ]

        if "missing" in analysis and analysis["missing"]:
            exercises.append(f"Focus on adding: {', '.join(analysis['missing'])}")

        return exercises

    def _get_next_practice_question(self, current_question: str,
                                   interview_type: str) -> str:
        """Get next practice question"""
        # Would use algorithm to pick next question based on performance
        return "Tell me about a time you had to learn a new technology quickly."

    def _score_to_rating(self, score: float) -> str:
        """Convert score to rating"""
        if score >= 9:
            return "Excellent"
        elif score >= 7.5:
            return "Good"
        elif score >= 6:
            return "Fair"
        else:
            return "Needs Improvement"

    def _get_company_info(self, company_name: str) -> Dict[str, Any]:
        """Get company information"""
        # Simplified - would pull from database
        return {
            "name": company_name,
            "size": "Large (10,000+ employees)",
            "culture": "Data-driven, customer-obsessed, innovative",
            "values": ["Customer first", "Innovation", "Integrity", "Teamwork"],
            "interview_style": "Behavioral + Technical + System Design"
        }

    def _get_company_common_questions(self, company_name: str,
                                     role: str) -> List[str]:
        """Get common questions for company"""
        return [
            "Why do you want to work at [company]?",
            "Tell me about a time you failed",
            "Describe a situation where you had to work with a difficult person",
            f"Technical question related to {role}"
        ]

    def _get_interview_process(self, company_name: str, role: str) -> List[Dict[str, Any]]:
        """Get interview process breakdown"""
        return [
            {
                "round": 1,
                "type": "Phone Screen",
                "duration": "30 minutes",
                "focus": "Background, basic fit, salary expectations"
            },
            {
                "round": 2,
                "type": "Technical Phone Screen",
                "duration": "45-60 minutes",
                "focus": "Coding problem or technical discussion"
            },
            {
                "round": 3,
                "type": "On-site (or Virtual)",
                "duration": "4-5 hours",
                "focus": "4-5 interviews covering behavioral, technical, system design"
            }
        ]

    def _get_insider_tips(self, company_name: str) -> List[str]:
        """Get insider tips for company"""
        return [
            f"{company_name} values specific examples and data",
            "They look for ownership and bias for action",
            "Prepare stories that show customer focus",
            "Ask thoughtful questions about the team and projects"
        ]

    def _get_company_key_skills(self, company_name: str, role: str) -> List[str]:
        """Get key skills to emphasize"""
        return [
            "Problem solving",
            "Customer focus",
            "Technical excellence",
            "Communication",
            "Leadership"
        ]

    def _map_values_to_stories(self, values: List[str]) -> Dict[str, str]:
        """Map company values to story types"""
        return {
            value: f"Prepare a story demonstrating {value}"
            for value in values
        }

    def _get_recent_experiences(self, company_name: str) -> List[Dict[str, str]]:
        """Get recent interview experiences"""
        return [
            {
                "role": "Software Engineer",
                "date": "2 months ago",
                "feedback": "5 rounds, heavy on system design and behavioral. Be ready with STAR stories."
            }
        ]

    def _create_company_prep_checklist(self, company_name: str,
                                      role: str) -> List[str]:
        """Create company-specific prep checklist"""
        return [
            f"Research {company_name}'s recent projects and news",
            "Prepare 5-7 STAR stories aligned with company values",
            "Review technical skills for role",
            "Prepare 5 thoughtful questions to ask",
            "Practice company-specific common questions",
            "Understand the interview process and timeline"
        ]

    def _get_practice_history(self, worker_id: int) -> List[Dict[str, Any]]:
        """Get practice history"""
        return [
            {
                "date": "2024-01-15",
                "type": "Behavioral Mock",
                "score": 8.2,
                "duration": "60 minutes"
            },
            {
                "date": "2024-01-10",
                "type": "Technical Mock",
                "score": 7.5,
                "duration": "45 minutes"
            }
        ]

    def _recommend_next_practice(self, skill_scores: Dict[str, float]) -> str:
        """Recommend next practice based on scores"""
        weakest = min(skill_scores.items(), key=lambda x: x[1])
        return f"Focus on {weakest[0]} - your weakest area (score: {weakest[1]})"
