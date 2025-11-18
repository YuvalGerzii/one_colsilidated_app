"""
Mental Health & Burnout Prevention System
Monitors stress levels, work-life balance, and provides interventions for job seekers and workers
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from enum import Enum


class StressLevel(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class BurnoutRiskLevel(str, Enum):
    MINIMAL = "minimal"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    SEVERE = "severe"


class InterventionType(str, Enum):
    IMMEDIATE = "immediate"
    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"
    PROFESSIONAL_HELP = "professional_help"


class MentalHealthSystem:
    """Comprehensive mental health and burnout prevention system"""

    def __init__(self):
        # Burnout risk factors and their weights
        self.burnout_factors = {
            "work_hours_weekly": 0.25,
            "job_search_stress": 0.20,
            "financial_pressure": 0.20,
            "social_support": 0.15,
            "sleep_quality": 0.10,
            "exercise_frequency": 0.10
        }

        # Stress indicators
        self.stress_indicators = [
            "difficulty_concentrating",
            "sleep_problems",
            "irritability",
            "physical_symptoms",
            "withdrawal",
            "overwhelmed_feeling",
            "loss_of_motivation",
            "anxiety",
            "depression_symptoms"
        ]

    def assess_burnout_risk(self, worker_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive burnout risk assessment

        Args:
            worker_data: Worker information including work hours, stress levels, etc.

        Returns:
            Burnout risk analysis with score, level, contributing factors, and interventions
        """
        # Calculate burnout score (0-100)
        burnout_score = 0
        factor_scores = {}

        # Work hours assessment (0-100)
        work_hours = worker_data.get("work_hours_weekly", 40)
        if work_hours <= 40:
            hours_score = 0
        elif work_hours <= 50:
            hours_score = (work_hours - 40) * 5  # 0-50
        elif work_hours <= 60:
            hours_score = 50 + (work_hours - 50) * 3  # 50-80
        else:
            hours_score = min(100, 80 + (work_hours - 60) * 2)  # 80-100

        factor_scores["work_hours"] = hours_score
        burnout_score += hours_score * self.burnout_factors["work_hours_weekly"]

        # Job search stress (number of rejections, months unemployed)
        rejections = worker_data.get("recent_rejections", 0)
        months_unemployed = worker_data.get("months_unemployed", 0)
        job_search_score = min(100, (rejections * 5) + (months_unemployed * 10))
        factor_scores["job_search_stress"] = job_search_score
        burnout_score += job_search_score * self.burnout_factors["job_search_stress"]

        # Financial pressure (emergency fund months, debt ratio)
        emergency_fund_months = worker_data.get("emergency_fund_months", 3)
        debt_to_income = worker_data.get("debt_to_income_ratio", 0.3)
        financial_score = max(0, 100 - (emergency_fund_months * 15)) + (debt_to_income * 50)
        financial_score = min(100, financial_score)
        factor_scores["financial_pressure"] = financial_score
        burnout_score += financial_score * self.burnout_factors["financial_pressure"]

        # Social support (0-10 scale, inverted for risk)
        social_support = worker_data.get("social_support_score", 5)
        support_score = max(0, 100 - (social_support * 10))
        factor_scores["social_support"] = support_score
        burnout_score += support_score * self.burnout_factors["social_support"]

        # Sleep quality (hours per night)
        sleep_hours = worker_data.get("sleep_hours_avg", 7)
        if 7 <= sleep_hours <= 9:
            sleep_score = 0
        elif sleep_hours < 7:
            sleep_score = (7 - sleep_hours) * 25  # Less sleep = higher risk
        else:
            sleep_score = (sleep_hours - 9) * 15  # Too much sleep can also indicate issues
        sleep_score = min(100, sleep_score)
        factor_scores["sleep_quality"] = sleep_score
        burnout_score += sleep_score * self.burnout_factors["sleep_quality"]

        # Exercise frequency (days per week)
        exercise_days = worker_data.get("exercise_days_weekly", 3)
        exercise_score = max(0, 100 - (exercise_days * 20))
        factor_scores["exercise"] = exercise_score
        burnout_score += exercise_score * self.burnout_factors["exercise_frequency"]

        # Determine risk level
        if burnout_score < 20:
            risk_level = BurnoutRiskLevel.MINIMAL
        elif burnout_score < 40:
            risk_level = BurnoutRiskLevel.LOW
        elif burnout_score < 60:
            risk_level = BurnoutRiskLevel.MODERATE
        elif burnout_score < 80:
            risk_level = BurnoutRiskLevel.HIGH
        else:
            risk_level = BurnoutRiskLevel.SEVERE

        # Identify top risk contributors
        top_contributors = sorted(
            factor_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]

        # Generate interventions
        interventions = self._generate_interventions(
            burnout_score, risk_level, factor_scores
        )

        # Warning signs specific to this worker
        warning_signs = self._identify_warning_signs(worker_data, factor_scores)

        return {
            "burnout_score": round(burnout_score, 1),
            "risk_level": risk_level.value,
            "risk_category": self._get_risk_category(risk_level),
            "factor_breakdown": {
                k: round(v, 1) for k, v in factor_scores.items()
            },
            "top_risk_contributors": [
                {
                    "factor": contrib[0],
                    "score": round(contrib[1], 1),
                    "impact": "high" if contrib[1] > 70 else "moderate" if contrib[1] > 40 else "low"
                }
                for contrib in top_contributors
            ],
            "warning_signs": warning_signs,
            "interventions": interventions,
            "next_check_in": self._calculate_next_checkin(risk_level),
            "professional_help_recommended": burnout_score >= 70
        }

    def stress_level_assessment(self, stress_indicators: Dict[str, bool]) -> Dict[str, Any]:
        """
        Assess current stress level based on indicators

        Args:
            stress_indicators: Dictionary of stress symptoms (True/False)

        Returns:
            Stress level analysis
        """
        # Count active indicators
        active_indicators = sum(1 for v in stress_indicators.values() if v)
        total_indicators = len(stress_indicators)

        stress_percentage = (active_indicators / total_indicators) * 100

        # Determine stress level
        if stress_percentage < 20:
            level = StressLevel.LOW
            severity = "minimal"
        elif stress_percentage < 40:
            level = StressLevel.MODERATE
            severity = "manageable"
        elif stress_percentage < 60:
            level = StressLevel.HIGH
            severity = "concerning"
        else:
            level = StressLevel.CRITICAL
            severity = "urgent"

        # Get specific active symptoms
        active_symptoms = [k for k, v in stress_indicators.items() if v]

        # Immediate actions based on stress level
        immediate_actions = self._get_stress_relief_actions(level, active_symptoms)

        return {
            "stress_level": level.value,
            "severity": severity,
            "stress_percentage": round(stress_percentage, 1),
            "active_indicators": active_indicators,
            "total_indicators": total_indicators,
            "active_symptoms": active_symptoms,
            "immediate_actions": immediate_actions,
            "coping_strategies": self._get_coping_strategies(active_symptoms),
            "crisis_resources": self._get_crisis_resources() if level == StressLevel.CRITICAL else None
        }

    def work_life_balance_score(self, worker_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate work-life balance score

        Args:
            worker_data: Worker activity and time allocation data

        Returns:
            Work-life balance analysis
        """
        # Time allocation (hours per week)
        work_hours = worker_data.get("work_hours_weekly", 40)
        job_search_hours = worker_data.get("job_search_hours_weekly", 0)
        learning_hours = worker_data.get("learning_hours_weekly", 0)
        family_time = worker_data.get("family_hours_weekly", 0)
        personal_time = worker_data.get("personal_hours_weekly", 0)
        sleep_hours = worker_data.get("sleep_hours_weekly", 49)  # 7 hrs/day

        total_committed = work_hours + job_search_hours + learning_hours + sleep_hours
        total_available = 168  # Hours in a week
        free_time = total_available - total_committed

        # Calculate balance score (0-100)
        balance_score = 100

        # Penalty for overwork
        if total_committed > 100:
            balance_score -= (total_committed - 100) * 2

        # Penalty for insufficient personal/family time
        min_personal_time = 14  # At least 2 hours/day
        if (family_time + personal_time) < min_personal_time:
            balance_score -= (min_personal_time - (family_time + personal_time)) * 3

        # Bonus for good sleep
        if 49 <= sleep_hours <= 63:  # 7-9 hours/day
            balance_score += 10
        else:
            balance_score -= 15

        balance_score = max(0, min(100, balance_score))

        # Determine rating
        if balance_score >= 80:
            rating = "excellent"
            color = "green"
        elif balance_score >= 60:
            rating = "good"
            color = "lightgreen"
        elif balance_score >= 40:
            rating = "fair"
            color = "yellow"
        elif balance_score >= 20:
            rating = "poor"
            color = "orange"
        else:
            rating = "critical"
            color = "red"

        # Time allocation breakdown
        time_breakdown = {
            "work": work_hours,
            "job_search": job_search_hours,
            "learning": learning_hours,
            "family": family_time,
            "personal": personal_time,
            "sleep": sleep_hours,
            "free_time": max(0, free_time)
        }

        # Recommendations
        recommendations = self._get_balance_recommendations(
            time_breakdown, balance_score
        )

        return {
            "balance_score": round(balance_score, 1),
            "rating": rating,
            "color": color,
            "time_breakdown": time_breakdown,
            "total_committed_hours": total_committed,
            "free_time_hours": max(0, round(free_time, 1)),
            "recommendations": recommendations,
            "areas_of_concern": self._identify_balance_concerns(time_breakdown),
            "ideal_allocation": {
                "work": "40-45 hours",
                "job_search": "10-15 hours (if unemployed)",
                "learning": "5-10 hours",
                "family_personal": "20-30 hours",
                "sleep": "49-63 hours (7-9 hrs/day)"
            }
        }

    def wellness_check_in(self, worker_id: int, mood_score: int,
                          energy_level: int, notes: Optional[str] = None) -> Dict[str, Any]:
        """
        Daily/weekly wellness check-in

        Args:
            worker_id: Worker identifier
            mood_score: 1-10 mood rating
            energy_level: 1-10 energy rating
            notes: Optional notes from worker

        Returns:
            Check-in record and trend analysis
        """
        timestamp = datetime.now()

        # Assess current state
        if mood_score >= 8 and energy_level >= 8:
            state = "thriving"
        elif mood_score >= 6 and energy_level >= 6:
            state = "doing_well"
        elif mood_score >= 4 and energy_level >= 4:
            state = "struggling"
        else:
            state = "needs_support"

        # Generate personalized message
        message = self._get_checkin_message(mood_score, energy_level, state)

        # Suggested activities
        activities = self._suggest_wellness_activities(mood_score, energy_level)

        return {
            "check_in_id": f"checkin_{worker_id}_{timestamp.strftime('%Y%m%d_%H%M%S')}",
            "timestamp": timestamp.isoformat(),
            "mood_score": mood_score,
            "energy_level": energy_level,
            "current_state": state,
            "personalized_message": message,
            "suggested_activities": activities,
            "notes": notes,
            "follow_up_recommended": mood_score <= 3 or energy_level <= 3
        }

    def _generate_interventions(self, burnout_score: float,
                                risk_level: BurnoutRiskLevel,
                                factor_scores: Dict[str, float]) -> List[Dict[str, Any]]:
        """Generate personalized interventions based on burnout risk"""
        interventions = []

        # Immediate interventions for high risk
        if burnout_score >= 60:
            interventions.append({
                "type": InterventionType.IMMEDIATE.value,
                "priority": "urgent",
                "action": "Take a break",
                "description": "Step away from job search/work for 24-48 hours",
                "rationale": "Immediate rest needed to prevent burnout escalation"
            })

        # Work hours intervention
        if factor_scores.get("work_hours", 0) > 60:
            interventions.append({
                "type": InterventionType.SHORT_TERM.value,
                "priority": "high",
                "action": "Reduce work hours",
                "description": "Limit total work/job search hours to 50 per week",
                "expected_impact": "Reduce burnout score by 15-20 points"
            })

        # Job search stress intervention
        if factor_scores.get("job_search_stress", 0) > 60:
            interventions.append({
                "type": InterventionType.SHORT_TERM.value,
                "priority": "high",
                "action": "Adjust job search strategy",
                "description": "Focus on quality over quantity. Apply to 3-5 highly targeted positions per week instead of mass applications",
                "expected_impact": "Reduce stress and improve application success rate"
            })

        # Financial pressure intervention
        if factor_scores.get("financial_pressure", 0) > 70:
            interventions.append({
                "type": InterventionType.LONG_TERM.value,
                "priority": "high",
                "action": "Financial counseling",
                "description": "Work with financial advisor to create debt reduction plan and build emergency fund",
                "expected_impact": "Reduce anxiety and improve long-term stability"
            })

        # Social support intervention
        if factor_scores.get("social_support", 0) > 60:
            interventions.append({
                "type": InterventionType.SHORT_TERM.value,
                "priority": "medium",
                "action": "Build support network",
                "description": "Join job seeker support groups, reconnect with friends/family, consider peer mentorship",
                "expected_impact": "Improve emotional resilience and access to opportunities"
            })

        # Sleep intervention
        if factor_scores.get("sleep_quality", 0) > 50:
            interventions.append({
                "type": InterventionType.IMMEDIATE.value,
                "priority": "high",
                "action": "Improve sleep hygiene",
                "description": "Set consistent sleep schedule (11pm-7am), limit screen time before bed, create relaxing bedtime routine",
                "expected_impact": "Better energy, focus, and emotional regulation"
            })

        # Exercise intervention
        if factor_scores.get("exercise", 0) > 60:
            interventions.append({
                "type": InterventionType.SHORT_TERM.value,
                "priority": "medium",
                "action": "Start exercise routine",
                "description": "20-30 minutes of moderate exercise 3-4 days per week (walking, jogging, yoga)",
                "expected_impact": "Reduce stress hormones, improve mood and energy"
            })

        # Professional help for severe cases
        if burnout_score >= 70:
            interventions.append({
                "type": InterventionType.PROFESSIONAL_HELP.value,
                "priority": "urgent",
                "action": "Seek professional support",
                "description": "Consult with therapist or counselor specializing in career transitions and stress management",
                "resources": self._get_professional_resources()
            })

        return interventions

    def _identify_warning_signs(self, worker_data: Dict[str, Any],
                               factor_scores: Dict[str, float]) -> List[str]:
        """Identify specific warning signs for this worker"""
        warnings = []

        if worker_data.get("work_hours_weekly", 40) > 55:
            warnings.append("Working excessive hours (>55/week)")

        if worker_data.get("recent_rejections", 0) > 10:
            warnings.append(f"{worker_data['recent_rejections']} recent job rejections")

        if worker_data.get("months_unemployed", 0) > 6:
            warnings.append("Extended unemployment (>6 months)")

        if worker_data.get("emergency_fund_months", 3) < 1:
            warnings.append("Critical financial situation (<1 month emergency fund)")

        if worker_data.get("sleep_hours_avg", 7) < 6:
            warnings.append("Chronic sleep deprivation (<6 hours/night)")

        if worker_data.get("social_support_score", 5) < 3:
            warnings.append("Low social support network")

        if worker_data.get("exercise_days_weekly", 3) == 0:
            warnings.append("No regular physical activity")

        return warnings

    def _get_stress_relief_actions(self, level: StressLevel,
                                   symptoms: List[str]) -> List[Dict[str, str]]:
        """Get immediate stress relief actions"""
        actions = []

        # Universal actions
        actions.append({
            "action": "Deep breathing",
            "description": "5 minutes of deep breathing (4-7-8 technique)",
            "time": "5 minutes"
        })

        if level in [StressLevel.HIGH, StressLevel.CRITICAL]:
            actions.append({
                "action": "Emergency break",
                "description": "Stop all activities, take 30-minute walk outside",
                "time": "30 minutes"
            })

        if "sleep_problems" in symptoms:
            actions.append({
                "action": "Sleep reset",
                "description": "Go to bed 1 hour earlier tonight, avoid screens 2 hours before",
                "time": "Tonight"
            })

        if "anxiety" in symptoms or "overwhelmed_feeling" in symptoms:
            actions.append({
                "action": "Grounding exercise",
                "description": "5-4-3-2-1 technique: Name 5 things you see, 4 you hear, 3 you feel, 2 you smell, 1 you taste",
                "time": "5 minutes"
            })

        if "physical_symptoms" in symptoms:
            actions.append({
                "action": "Physical release",
                "description": "10-15 minutes of light exercise or stretching",
                "time": "15 minutes"
            })

        return actions

    def _get_coping_strategies(self, symptoms: List[str]) -> List[Dict[str, str]]:
        """Get long-term coping strategies"""
        strategies = [
            {
                "strategy": "Mindfulness meditation",
                "frequency": "Daily, 10-15 minutes",
                "benefit": "Reduces anxiety and improves focus"
            },
            {
                "strategy": "Journaling",
                "frequency": "3-4 times per week",
                "benefit": "Process emotions and identify patterns"
            },
            {
                "strategy": "Social connection",
                "frequency": "Weekly",
                "benefit": "Emotional support and reduced isolation"
            }
        ]

        if "difficulty_concentrating" in symptoms:
            strategies.append({
                "strategy": "Pomodoro Technique",
                "frequency": "Daily during work",
                "benefit": "Improves focus through timed work intervals"
            })

        if "loss_of_motivation" in symptoms:
            strategies.append({
                "strategy": "Small wins tracking",
                "frequency": "Daily",
                "benefit": "Build momentum through achievable daily goals"
            })

        return strategies

    def _get_crisis_resources(self) -> Dict[str, str]:
        """Get crisis and mental health resources"""
        return {
            "crisis_hotline": "988 (Suicide & Crisis Lifeline)",
            "crisis_text": "Text HOME to 741741 (Crisis Text Line)",
            "therapy_platforms": "BetterHelp, Talkspace, Psychology Today directory",
            "free_resources": "NAMI (nami.org), MentalHealth.gov",
            "immediate_help": "If in immediate danger, call 911 or go to nearest ER"
        }

    def _get_professional_resources(self) -> List[Dict[str, str]]:
        """Get professional mental health resources"""
        return [
            {
                "resource": "Online Therapy Platforms",
                "options": "BetterHelp, Talkspace, Cerebral",
                "cost": "$60-100/session",
                "coverage": "Many accept insurance"
            },
            {
                "resource": "Employee Assistance Program (EAP)",
                "options": "Check with employer",
                "cost": "Free (3-6 sessions typically)",
                "coverage": "Confidential counseling"
            },
            {
                "resource": "Community Mental Health Centers",
                "options": "Local CMHC (sliding scale fees)",
                "cost": "Based on income",
                "coverage": "Affordable counseling"
            },
            {
                "resource": "Career Counseling",
                "options": "Career transition specialists",
                "cost": "$75-150/session",
                "coverage": "Job search stress specific"
            }
        ]

    def _get_balance_recommendations(self, time_breakdown: Dict[str, float],
                                    score: float) -> List[str]:
        """Get work-life balance recommendations"""
        recommendations = []

        total_work = time_breakdown["work"] + time_breakdown["job_search"] + time_breakdown["learning"]
        if total_work > 60:
            recommendations.append(
                f"Reduce total work/learning hours from {total_work} to 50-55 hours per week"
            )

        if time_breakdown["sleep"] < 49:
            recommendations.append(
                f"Increase sleep from {time_breakdown['sleep']} to at least 49 hours per week (7 hrs/night)"
            )

        personal_time = time_breakdown["family"] + time_breakdown["personal"]
        if personal_time < 14:
            recommendations.append(
                f"Increase personal/family time from {personal_time} to at least 20 hours per week"
            )

        if time_breakdown["free_time"] < 10:
            recommendations.append(
                "Schedule at least 10-15 hours of unstructured free time for flexibility"
            )

        if score < 60:
            recommendations.append(
                "Consider setting strict work boundaries (e.g., no work after 6pm, weekends off)"
            )

        return recommendations

    def _identify_balance_concerns(self, time_breakdown: Dict[str, float]) -> List[str]:
        """Identify areas of concern in work-life balance"""
        concerns = []

        if time_breakdown["work"] + time_breakdown["job_search"] > 60:
            concerns.append("Overwork risk (>60 hours committed to work/job search)")

        if time_breakdown["sleep"] < 42:
            concerns.append("Sleep deprivation (<6 hours average per night)")

        if time_breakdown["family"] + time_breakdown["personal"] < 10:
            concerns.append("Insufficient personal time (<10 hours per week)")

        if time_breakdown["free_time"] < 5:
            concerns.append("No buffer time for unexpected events or rest")

        return concerns

    def _get_checkin_message(self, mood: int, energy: int, state: str) -> str:
        """Get personalized check-in message"""
        messages = {
            "thriving": "You're doing great! Keep up the positive momentum. Remember to celebrate your wins, both big and small.",
            "doing_well": "You're managing well. Continue with your current routines and don't hesitate to ask for support when needed.",
            "struggling": "It sounds like things are tough right now. That's completely normal during transitions. Consider taking a short break and reaching out to your support network.",
            "needs_support": "I'm concerned about how you're feeling. Please consider talking to someone you trust or a professional. You don't have to go through this alone."
        }
        return messages.get(state, "Thank you for checking in.")

    def _suggest_wellness_activities(self, mood: int, energy: int) -> List[Dict[str, str]]:
        """Suggest activities based on mood and energy"""
        activities = []

        if energy >= 7:
            activities.append({
                "activity": "Exercise",
                "description": "Go for a 30-minute run or workout",
                "benefit": "Release endorphins, boost mood"
            })
        else:
            activities.append({
                "activity": "Gentle movement",
                "description": "15-minute walk or yoga",
                "benefit": "Increase energy without exhaustion"
            })

        if mood < 5:
            activities.append({
                "activity": "Social connection",
                "description": "Call a friend or family member",
                "benefit": "Emotional support and perspective"
            })
            activities.append({
                "activity": "Creative expression",
                "description": "Journal, draw, or play music",
                "benefit": "Process emotions constructively"
            })
        else:
            activities.append({
                "activity": "Gratitude practice",
                "description": "Write down 3 things you're grateful for",
                "benefit": "Boost positive emotions"
            })

        return activities

    def _get_risk_category(self, risk_level: BurnoutRiskLevel) -> str:
        """Get descriptive risk category"""
        categories = {
            BurnoutRiskLevel.MINIMAL: "You're in a healthy state",
            BurnoutRiskLevel.LOW: "Low risk - maintain good habits",
            BurnoutRiskLevel.MODERATE: "Moderate risk - take preventive action",
            BurnoutRiskLevel.HIGH: "High risk - immediate changes needed",
            BurnoutRiskLevel.SEVERE: "Severe risk - seek professional help"
        }
        return categories.get(risk_level, "Unknown")

    def _calculate_next_checkin(self, risk_level: BurnoutRiskLevel) -> str:
        """Calculate when next check-in should be"""
        if risk_level == BurnoutRiskLevel.SEVERE:
            return "24 hours"
        elif risk_level == BurnoutRiskLevel.HIGH:
            return "3 days"
        elif risk_level == BurnoutRiskLevel.MODERATE:
            return "1 week"
        else:
            return "2 weeks"
