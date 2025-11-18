"""
Citizen-Level Economic Copilot

Integrates personal finance with career decisions to provide holistic life planning.
Helps workers make informed decisions about job offers, career transitions, debt,
retirement, and family financial planning.
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import random


class JobDecisionEngine:
    """
    Comprehensive job offer analysis engine.
    Analyzes job offers holistically including salary, benefits, career growth,
    quality of life, and long-term financial impact.
    """

    def analyze_job_offer(
        self,
        current_situation: Dict,
        job_offer: Dict,
        personal_priorities: Optional[Dict] = None
    ) -> Dict:
        """
        Comprehensive analysis of whether to take a job offer.

        Args:
            current_situation: Current job and financial situation
            job_offer: Details of the job offer
            personal_priorities: Weights for different factors (salary, growth, wlb, etc.)

        Returns:
            Detailed analysis with recommendation and scores across multiple dimensions
        """
        personal_priorities = personal_priorities or {}

        # Default priority weights (can be customized)
        weights = {
            "compensation": personal_priorities.get("compensation", 30),
            "career_growth": personal_priorities.get("career_growth", 25),
            "work_life_balance": personal_priorities.get("work_life_balance", 20),
            "job_security": personal_priorities.get("job_security", 15),
            "company_culture": personal_priorities.get("company_culture", 10)
        }

        # Analyze compensation
        comp_analysis = self._analyze_compensation(
            current_situation.get("compensation", {}),
            job_offer.get("compensation", {})
        )

        # Analyze career growth potential
        growth_analysis = self._analyze_career_growth(
            current_situation.get("role", {}),
            job_offer.get("role", {})
        )

        # Analyze work-life balance
        wlb_analysis = self._analyze_work_life_balance(
            current_situation.get("work_conditions", {}),
            job_offer.get("work_conditions", {})
        )

        # Analyze job security
        security_analysis = self._analyze_job_security(
            current_situation.get("company", {}),
            job_offer.get("company", {})
        )

        # Analyze culture fit
        culture_analysis = self._analyze_culture_fit(
            current_situation.get("culture", {}),
            job_offer.get("culture", {}),
            personal_priorities.get("culture_preferences", {})
        )

        # Calculate weighted overall score
        overall_score = (
            comp_analysis["score"] * weights["compensation"] / 100 +
            growth_analysis["score"] * weights["career_growth"] / 100 +
            wlb_analysis["score"] * weights["work_life_balance"] / 100 +
            security_analysis["score"] * weights["job_security"] / 100 +
            culture_analysis["score"] * weights["company_culture"] / 100
        )

        # Generate recommendation
        recommendation = self._generate_job_recommendation(
            overall_score, comp_analysis, growth_analysis, wlb_analysis
        )

        # Calculate financial impact over 5 years
        financial_projection = self._project_5year_financial_impact(
            current_situation.get("compensation", {}),
            job_offer.get("compensation", {}),
            growth_analysis
        )

        return {
            "overall_score": round(overall_score, 1),
            "recommendation": recommendation,
            "compensation_analysis": comp_analysis,
            "career_growth_analysis": growth_analysis,
            "work_life_balance_analysis": wlb_analysis,
            "job_security_analysis": security_analysis,
            "culture_fit_analysis": culture_analysis,
            "financial_projection_5_years": financial_projection,
            "decision_factors": {
                "pros": self._extract_pros(comp_analysis, growth_analysis, wlb_analysis, security_analysis, culture_analysis),
                "cons": self._extract_cons(comp_analysis, growth_analysis, wlb_analysis, security_analysis, culture_analysis),
                "risks": self._identify_risks(job_offer, security_analysis)
            },
            "priority_weights": weights
        }

    def _analyze_compensation(self, current: Dict, offer: Dict) -> Dict:
        """Analyze total compensation package"""
        current_base = current.get("base_salary", 0)
        current_bonus = current.get("bonus", 0)
        current_equity = current.get("equity_value_annual", 0)
        current_benefits_value = current.get("benefits_value", 0)
        current_total = current_base + current_bonus + current_equity + current_benefits_value

        offer_base = offer.get("base_salary", 0)
        offer_bonus = offer.get("bonus", 0)
        offer_equity = offer.get("equity_value_annual", 0)
        offer_benefits_value = offer.get("benefits_value", 0)
        offer_total = offer_base + offer_bonus + offer_equity + offer_benefits_value

        difference = offer_total - current_total
        percent_change = (difference / current_total * 100) if current_total > 0 else 0

        # Score based on compensation change
        if percent_change >= 20:
            score = 100
        elif percent_change >= 10:
            score = 80
        elif percent_change >= 5:
            score = 60
        elif percent_change >= 0:
            score = 50
        elif percent_change >= -5:
            score = 30
        else:
            score = 10

        return {
            "score": score,
            "current_total_comp": round(current_total, 2),
            "offer_total_comp": round(offer_total, 2),
            "difference": round(difference, 2),
            "percent_change": round(percent_change, 1),
            "breakdown": {
                "base_salary_change": round(offer_base - current_base, 2),
                "bonus_change": round(offer_bonus - current_bonus, 2),
                "equity_change": round(offer_equity - current_equity, 2),
                "benefits_change": round(offer_benefits_value - current_benefits_value, 2)
            },
            "assessment": "significant_increase" if percent_change >= 15 else
                         "moderate_increase" if percent_change >= 5 else
                         "minor_increase" if percent_change > 0 else
                         "decrease"
        }

    def _analyze_career_growth(self, current_role: Dict, offer_role: Dict) -> Dict:
        """Analyze career growth potential"""
        # Seniority level scoring
        seniority_levels = {
            "junior": 1, "mid": 2, "senior": 3, "lead": 4, "principal": 5,
            "manager": 4, "senior_manager": 5, "director": 6, "vp": 7, "c_level": 8
        }

        current_level = seniority_levels.get(current_role.get("seniority", "mid"), 2)
        offer_level = seniority_levels.get(offer_role.get("seniority", "mid"), 2)
        level_change = offer_level - current_level

        # Learning opportunities
        current_learning = current_role.get("learning_score", 50)
        offer_learning = offer_role.get("learning_score", 50)

        # Industry growth potential
        current_industry_growth = current_role.get("industry_growth_rate", 3)
        offer_industry_growth = offer_role.get("industry_growth_rate", 3)

        # Calculate growth score
        score = 50  # baseline

        # Seniority change impact
        if level_change >= 2:
            score += 30
        elif level_change == 1:
            score += 20
        elif level_change == 0:
            score += 0
        else:
            score -= 20

        # Learning opportunities impact
        if offer_learning > current_learning + 20:
            score += 20
        elif offer_learning > current_learning:
            score += 10

        # Industry growth impact
        if offer_industry_growth > current_industry_growth + 2:
            score += 10

        score = max(0, min(100, score))

        return {
            "score": score,
            "seniority_change": level_change,
            "current_level": current_role.get("seniority", "mid"),
            "offer_level": offer_role.get("seniority", "mid"),
            "learning_opportunity_score": offer_learning,
            "industry_growth_rate": offer_industry_growth,
            "promotion_timeline_estimate": self._estimate_promotion_timeline(offer_role),
            "skill_development": offer_role.get("skills_to_gain", []),
            "assessment": "excellent_growth" if score >= 80 else
                         "good_growth" if score >= 60 else
                         "moderate_growth" if score >= 40 else
                         "limited_growth"
        }

    def _analyze_work_life_balance(self, current: Dict, offer: Dict) -> Dict:
        """Analyze work-life balance factors"""
        # Hours per week
        current_hours = current.get("hours_per_week", 40)
        offer_hours = offer.get("hours_per_week", 40)

        # Commute time
        current_commute = current.get("commute_minutes_daily", 0)
        offer_commute = offer.get("commute_minutes_daily", 0)

        # Flexibility
        current_flexibility = current.get("flexibility_score", 50)
        offer_flexibility = offer.get("flexibility_score", 50)

        # Remote work
        current_remote = current.get("remote_days_per_week", 0)
        offer_remote = offer.get("remote_days_per_week", 0)

        # PTO
        current_pto = current.get("pto_days", 15)
        offer_pto = offer.get("pto_days", 15)

        # Calculate score
        score = 50

        # Hours impact
        hours_diff = offer_hours - current_hours
        if hours_diff <= -5:
            score += 20
        elif hours_diff < 0:
            score += 10
        elif hours_diff > 5:
            score -= 20
        elif hours_diff > 0:
            score -= 10

        # Commute impact
        commute_diff = offer_commute - current_commute
        if commute_diff <= -30:
            score += 15
        elif commute_diff < 0:
            score += 8
        elif commute_diff > 30:
            score -= 15
        elif commute_diff > 0:
            score -= 8

        # Flexibility impact
        if offer_flexibility > current_flexibility + 20:
            score += 15
        elif offer_flexibility > current_flexibility:
            score += 8

        # Remote work impact
        remote_diff = offer_remote - current_remote
        if remote_diff >= 3:
            score += 15
        elif remote_diff > 0:
            score += 8 * remote_diff

        # PTO impact
        pto_diff = offer_pto - current_pto
        if pto_diff >= 5:
            score += 10
        elif pto_diff > 0:
            score += 5

        score = max(0, min(100, score))

        # Calculate total weekly time commitment (work + commute)
        current_total_time = current_hours + (current_commute * 5 / 60)
        offer_total_time = offer_hours + (offer_commute * 5 / 60)

        return {
            "score": score,
            "hours_per_week_change": offer_hours - current_hours,
            "commute_time_change_minutes": commute_diff,
            "flexibility_change": offer_flexibility - current_flexibility,
            "remote_days_change": remote_diff,
            "pto_days_change": pto_diff,
            "current_total_weekly_hours": round(current_total_time, 1),
            "offer_total_weekly_hours": round(offer_total_time, 1),
            "assessment": "much_better" if score >= 75 else
                         "better" if score >= 55 else
                         "similar" if score >= 45 else
                         "worse"
        }

    def _analyze_job_security(self, current_company: Dict, offer_company: Dict) -> Dict:
        """Analyze job security factors"""
        # Company size and stability
        current_size = current_company.get("employee_count", 100)
        offer_size = offer_company.get("employee_count", 100)

        # Financial health
        current_health = current_company.get("financial_health_score", 70)
        offer_health = offer_company.get("financial_health_score", 70)

        # Industry stability
        current_stability = current_company.get("industry_stability", 60)
        offer_stability = offer_company.get("industry_stability", 60)

        # Funding/revenue
        current_funded = current_company.get("well_funded", True)
        offer_funded = offer_company.get("well_funded", True)

        # Calculate score
        score = 50

        # Size impact (generally larger = more stable, but not always)
        if offer_size > 1000 and current_size < 500:
            score += 15
        elif offer_size < 50 and current_size > 500:
            score -= 15

        # Financial health impact
        health_diff = offer_health - current_health
        if health_diff >= 20:
            score += 20
        elif health_diff >= 10:
            score += 10
        elif health_diff <= -20:
            score -= 20
        elif health_diff <= -10:
            score -= 10

        # Industry stability impact
        stability_diff = offer_stability - current_stability
        if stability_diff >= 15:
            score += 15
        elif stability_diff > 0:
            score += 8
        elif stability_diff <= -15:
            score -= 15

        # Funding impact
        if offer_funded and not current_funded:
            score += 15
        elif not offer_funded and current_funded:
            score -= 15

        score = max(0, min(100, score))

        return {
            "score": score,
            "company_size": offer_size,
            "financial_health": offer_health,
            "industry_stability": offer_stability,
            "funding_status": "well_funded" if offer_funded else "uncertain",
            "risk_level": "low" if score >= 70 else "moderate" if score >= 40 else "high",
            "assessment": "more_secure" if score >= 60 else "similar" if score >= 45 else "less_secure"
        }

    def _analyze_culture_fit(self, current_culture: Dict, offer_culture: Dict, preferences: Dict) -> Dict:
        """Analyze culture fit"""
        # Culture attributes scoring
        attributes = ["collaborative", "innovative", "fast_paced", "structured", "diverse"]

        current_scores = {attr: current_culture.get(attr, 50) for attr in attributes}
        offer_scores = {attr: offer_culture.get(attr, 50) for attr in attributes}
        preference_weights = {attr: preferences.get(attr, 1.0) for attr in attributes}

        # Calculate weighted fit score
        total_fit = 0
        total_weight = 0

        for attr in attributes:
            # How well does offer match preference (0-100)
            preference_target = preferences.get(f"{attr}_target", 70)
            fit = 100 - abs(offer_scores[attr] - preference_target)
            weight = preference_weights[attr]

            total_fit += fit * weight
            total_weight += weight

        score = total_fit / total_weight if total_weight > 0 else 50

        return {
            "score": round(score, 1),
            "culture_attributes": offer_scores,
            "fit_assessment": "excellent" if score >= 80 else
                            "good" if score >= 60 else
                            "moderate" if score >= 40 else
                            "poor",
            "top_strengths": self._get_top_culture_strengths(offer_scores),
            "potential_concerns": self._get_culture_concerns(offer_scores, preferences)
        }

    def _get_top_culture_strengths(self, scores: Dict) -> List[str]:
        """Get top 3 culture strengths"""
        sorted_attrs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [attr for attr, score in sorted_attrs[:3] if score >= 70]

    def _get_culture_concerns(self, scores: Dict, preferences: Dict) -> List[str]:
        """Identify potential culture mismatches"""
        concerns = []
        for attr, score in scores.items():
            target = preferences.get(f"{attr}_target", 70)
            if abs(score - target) > 30:
                concerns.append(f"{attr}: {score}/100 (you prefer {target}/100)")
        return concerns

    def _estimate_promotion_timeline(self, role: Dict) -> str:
        """Estimate time to next promotion"""
        seniority = role.get("seniority", "mid")
        growth_rate = role.get("company_growth_rate", "moderate")

        timelines = {
            "junior": {"fast": "12-18 months", "moderate": "18-24 months", "slow": "24-36 months"},
            "mid": {"fast": "18-24 months", "moderate": "24-36 months", "slow": "36-48 months"},
            "senior": {"fast": "24-36 months", "moderate": "36-48 months", "slow": "48-60 months"},
            "lead": {"fast": "36-48 months", "moderate": "48-60 months", "slow": "60+ months"}
        }

        return timelines.get(seniority, {}).get(growth_rate, "36-48 months")

    def _project_5year_financial_impact(self, current_comp: Dict, offer_comp: Dict, growth: Dict) -> Dict:
        """Project financial impact over 5 years"""
        current_base = current_comp.get("base_salary", 0)
        offer_base = offer_comp.get("base_salary", 0)

        # Estimate annual raises
        current_raise_rate = 0.03  # 3% typical
        offer_raise_rate = 0.05 if growth["score"] >= 70 else 0.04 if growth["score"] >= 50 else 0.03

        current_projections = []
        offer_projections = []
        current_total = 0
        offer_total = 0

        for year in range(1, 6):
            current_year_comp = current_base * (1 + current_raise_rate) ** year
            offer_year_comp = offer_base * (1 + offer_raise_rate) ** year

            current_projections.append(round(current_year_comp, 2))
            offer_projections.append(round(offer_year_comp, 2))

            current_total += current_year_comp
            offer_total += offer_year_comp

        return {
            "current_job_5_year_total": round(current_total, 2),
            "offer_job_5_year_total": round(offer_total, 2),
            "difference_over_5_years": round(offer_total - current_total, 2),
            "year_by_year_offer": offer_projections,
            "estimated_annual_raise_rate": f"{offer_raise_rate * 100}%"
        }

    def _generate_job_recommendation(self, score: float, comp: Dict, growth: Dict, wlb: Dict) -> Dict:
        """Generate final recommendation"""
        if score >= 75:
            decision = "strongly_recommend"
            explanation = "This opportunity scores highly across multiple dimensions and represents a significant positive change."
        elif score >= 60:
            decision = "recommend"
            explanation = "This is a good opportunity with notable improvements over your current situation."
        elif score >= 45:
            decision = "neutral"
            explanation = "This opportunity has both pros and cons. Consider your personal priorities carefully."
        elif score >= 30:
            decision = "not_recommended"
            explanation = "This opportunity may not represent an improvement over your current situation."
        else:
            decision = "strongly_not_recommended"
            explanation = "This opportunity scores poorly across multiple important dimensions."

        # Add specific guidance
        key_considerations = []
        if comp["percent_change"] < 0:
            key_considerations.append("⚠️ Compensation decrease - ensure other factors compensate")
        if growth["score"] >= 80:
            key_considerations.append("✓ Excellent career growth potential")
        if wlb["score"] <= 30:
            key_considerations.append("⚠️ Work-life balance may be significantly worse")

        return {
            "decision": decision,
            "confidence": "high" if abs(score - 50) > 25 else "moderate",
            "explanation": explanation,
            "key_considerations": key_considerations
        }

    def _extract_pros(self, comp: Dict, growth: Dict, wlb: Dict, security: Dict, culture: Dict) -> List[str]:
        """Extract pros from analysis"""
        pros = []

        if comp["percent_change"] >= 10:
            pros.append(f"Compensation increase of {comp['percent_change']:.1f}%")
        if growth["score"] >= 70:
            pros.append(f"Strong career growth potential ({growth['assessment']})")
        if wlb["score"] >= 60:
            pros.append(f"Improved work-life balance")
        if wlb.get("remote_days_change", 0) > 0:
            pros.append(f"{wlb['remote_days_change']} more remote days per week")
        if security["score"] >= 70:
            pros.append("High job security")
        if culture["score"] >= 75:
            pros.append("Excellent culture fit")

        return pros if pros else ["Opportunity for change"]

    def _extract_cons(self, comp: Dict, growth: Dict, wlb: Dict, security: Dict, culture: Dict) -> List[str]:
        """Extract cons from analysis"""
        cons = []

        if comp["percent_change"] < 0:
            cons.append(f"Compensation decrease of {abs(comp['percent_change']):.1f}%")
        if growth["score"] < 40:
            cons.append("Limited career growth potential")
        if wlb["score"] < 40:
            cons.append("Worse work-life balance")
        if wlb.get("hours_per_week_change", 0) > 5:
            cons.append(f"{wlb['hours_per_week_change']} more hours per week")
        if security["score"] < 40:
            cons.append("Lower job security")
        if culture["score"] < 50:
            cons.append("Questionable culture fit")

        return cons if cons else ["Risk of change"]

    def _identify_risks(self, offer: Dict, security: Dict) -> List[str]:
        """Identify specific risks"""
        risks = []

        if security["risk_level"] == "high":
            risks.append("High financial instability risk")

        company = offer.get("company", {})
        if company.get("employee_count", 1000) < 50:
            risks.append("Startup risk - higher uncertainty but potential upside")

        if company.get("recent_layoffs", False):
            risks.append("Company had recent layoffs - proceed with caution")

        role = offer.get("role", {})
        if role.get("new_team", False):
            risks.append("New team/product - success not guaranteed")

        return risks if risks else ["Standard career change risks"]


class RetirementImpactAnalyzer:
    """
    Analyzes how career changes impact long-term retirement planning.
    """

    def analyze_retirement_impact(
        self,
        current_age: int,
        target_retirement_age: int,
        current_situation: Dict,
        career_change: Dict,
        retirement_goals: Dict
    ) -> Dict:
        """
        Analyze impact of career change on retirement.

        Args:
            current_age: Current age
            target_retirement_age: Target retirement age
            current_situation: Current job and savings
            career_change: Proposed career change (salary change, time out of work, etc.)
            retirement_goals: Retirement savings goals and spending needs

        Returns:
            Comprehensive retirement impact analysis
        """
        years_to_retirement = target_retirement_age - current_age

        # Current trajectory
        current_trajectory = self._project_retirement_savings(
            starting_age=current_age,
            retirement_age=target_retirement_age,
            current_salary=current_situation.get("salary", 0),
            current_savings=current_situation.get("retirement_savings", 0),
            contribution_rate=current_situation.get("retirement_contribution_pct", 10),
            salary_growth_rate=0.03,
            return_rate=0.07
        )

        # New trajectory with career change
        new_trajectory = self._project_retirement_with_change(
            starting_age=current_age,
            retirement_age=target_retirement_age,
            current_savings=current_situation.get("retirement_savings", 0),
            career_change=career_change,
            return_rate=0.07
        )

        # Calculate retirement readiness
        retirement_goal = retirement_goals.get("target_savings", 1000000)
        annual_spending_need = retirement_goals.get("annual_spending", 60000)

        current_readiness = self._calculate_retirement_readiness(
            projected_savings=current_trajectory["final_balance"],
            target_savings=retirement_goal,
            annual_spending=annual_spending_need
        )

        new_readiness = self._calculate_retirement_readiness(
            projected_savings=new_trajectory["final_balance"],
            target_savings=retirement_goal,
            annual_spending=annual_spending_need
        )

        # Impact analysis
        impact_amount = new_trajectory["final_balance"] - current_trajectory["final_balance"]
        impact_percent = (impact_amount / current_trajectory["final_balance"] * 100) if current_trajectory["final_balance"] > 0 else 0

        # Mitigation strategies
        mitigation = self._generate_mitigation_strategies(
            impact_amount=impact_amount,
            years_remaining=years_to_retirement,
            new_situation=career_change
        )

        return {
            "current_trajectory": current_trajectory,
            "new_trajectory": new_trajectory,
            "impact": {
                "difference_at_retirement": round(impact_amount, 2),
                "percent_impact": round(impact_percent, 1),
                "severity": "critical" if impact_percent < -30 else
                           "significant" if impact_percent < -15 else
                           "moderate" if impact_percent < -5 else
                           "minimal" if abs(impact_percent) <= 5 else
                           "positive"
            },
            "retirement_readiness": {
                "current_path": current_readiness,
                "new_path": new_readiness,
                "change": {
                    "years_sustainable_change": new_readiness["years_sustainable"] - current_readiness["years_sustainable"],
                    "goal_achievement_change": new_readiness["percent_of_goal"] - current_readiness["percent_of_goal"]
                }
            },
            "mitigation_strategies": mitigation,
            "recommendation": self._generate_retirement_recommendation(
                impact_percent, new_readiness, years_to_retirement
            )
        }

    def _project_retirement_savings(
        self,
        starting_age: int,
        retirement_age: int,
        current_salary: float,
        current_savings: float,
        contribution_rate: float,
        salary_growth_rate: float,
        return_rate: float
    ) -> Dict:
        """Project retirement savings with compound interest"""
        years = retirement_age - starting_age
        balance = current_savings
        total_contributions = 0
        year_by_year = []

        salary = current_salary

        for year in range(years):
            # Annual contribution
            contribution = salary * (contribution_rate / 100)
            total_contributions += contribution

            # Add contribution and apply returns
            balance = (balance + contribution) * (1 + return_rate)

            # Increase salary
            salary *= (1 + salary_growth_rate)

            year_by_year.append({
                "year": starting_age + year + 1,
                "balance": round(balance, 2),
                "contribution": round(contribution, 2)
            })

        return {
            "final_balance": round(balance, 2),
            "total_contributions": round(total_contributions, 2),
            "investment_gains": round(balance - current_savings - total_contributions, 2),
            "year_by_year": year_by_year[-5:] if len(year_by_year) > 5 else year_by_year  # Last 5 years
        }

    def _project_retirement_with_change(
        self,
        starting_age: int,
        retirement_age: int,
        current_savings: float,
        career_change: Dict,
        return_rate: float
    ) -> Dict:
        """Project retirement savings accounting for career change"""
        years = retirement_age - starting_age
        balance = current_savings
        total_contributions = 0

        # Career change parameters
        time_out_of_work_months = career_change.get("time_out_of_work_months", 0)
        new_salary = career_change.get("new_salary", 0)
        new_contribution_rate = career_change.get("new_contribution_rate", 10)
        reskilling_cost = career_change.get("reskilling_cost", 0)

        # Deduct reskilling cost from savings
        balance -= reskilling_cost

        year_by_year = []
        salary = new_salary

        for year in range(years):
            # Account for time out of work in first year
            if year == 0 and time_out_of_work_months > 0:
                months_working = 12 - time_out_of_work_months
                contribution = salary * (new_contribution_rate / 100) * (months_working / 12)
            else:
                contribution = salary * (new_contribution_rate / 100)

            total_contributions += contribution

            # Add contribution and apply returns
            balance = (balance + contribution) * (1 + return_rate)

            # Increase salary (3% typical)
            salary *= 1.03

            year_by_year.append({
                "year": starting_age + year + 1,
                "balance": round(balance, 2),
                "contribution": round(contribution, 2)
            })

        return {
            "final_balance": round(balance, 2),
            "total_contributions": round(total_contributions, 2),
            "investment_gains": round(balance - current_savings - total_contributions + reskilling_cost, 2),
            "reskilling_cost_impact": round(reskilling_cost, 2),
            "time_out_of_work_impact_months": time_out_of_work_months
        }

    def _calculate_retirement_readiness(
        self,
        projected_savings: float,
        target_savings: float,
        annual_spending: float
    ) -> Dict:
        """Calculate retirement readiness metrics"""
        # 4% rule: can withdraw 4% annually
        annual_withdrawal_sustainable = projected_savings * 0.04

        # Years the money will last
        years_sustainable = round(projected_savings / annual_spending, 1) if annual_spending > 0 else 999

        # Percent of goal achieved
        percent_of_goal = (projected_savings / target_savings * 100) if target_savings > 0 else 100

        return {
            "projected_savings": round(projected_savings, 2),
            "target_savings": round(target_savings, 2),
            "percent_of_goal": round(percent_of_goal, 1),
            "annual_withdrawal_sustainable": round(annual_withdrawal_sustainable, 2),
            "annual_spending_need": round(annual_spending, 2),
            "spending_coverage": round(annual_withdrawal_sustainable / annual_spending * 100, 1) if annual_spending > 0 else 100,
            "years_sustainable": years_sustainable,
            "readiness_level": "on_track" if percent_of_goal >= 90 else
                            "needs_improvement" if percent_of_goal >= 70 else
                            "concerning" if percent_of_goal >= 50 else
                            "critical"
        }

    def _generate_mitigation_strategies(
        self,
        impact_amount: float,
        years_remaining: int,
        new_situation: Dict
    ) -> List[Dict]:
        """Generate strategies to mitigate retirement impact"""
        strategies = []

        if impact_amount < 0:
            # Need to make up for shortfall
            annual_makeup_needed = abs(impact_amount) / years_remaining if years_remaining > 0 else 0

            strategies.append({
                "strategy": "Increase retirement contributions",
                "action": f"Contribute an additional ${round(annual_makeup_needed / 12, 0)}/month",
                "impact": f"Would fully offset retirement shortfall over {years_remaining} years",
                "difficulty": "moderate"
            })

            strategies.append({
                "strategy": "Delay retirement",
                "action": f"Work {round(abs(impact_amount) / 50000, 1)} additional years",
                "impact": "Gives more time to save and reduces withdrawal period",
                "difficulty": "moderate"
            })

            strategies.append({
                "strategy": "Reduce retirement expenses",
                "action": "Lower annual spending in retirement by 10-20%",
                "impact": "Reduces savings needed by similar percentage",
                "difficulty": "easy"
            })

        new_salary = new_situation.get("new_salary", 0)
        if new_salary > 0:
            strategies.append({
                "strategy": "Maximize new employer 401(k) match",
                "action": "Contribute at least enough to get full match",
                "impact": "Free money that compounds over time",
                "difficulty": "easy"
            })

        return strategies

    def _generate_retirement_recommendation(
        self,
        impact_percent: float,
        new_readiness: Dict,
        years_remaining: int
    ) -> Dict:
        """Generate retirement-focused recommendation"""
        if impact_percent < -30:
            return {
                "recommendation": "reconsider",
                "explanation": "This career change significantly jeopardizes your retirement goals. Consider if non-financial benefits justify the impact.",
                "action_required": "Develop concrete plan to offset retirement impact before proceeding"
            }
        elif impact_percent < -15:
            return {
                "recommendation": "proceed_with_caution",
                "explanation": "This career change will impact retirement, but may be manageable with adjustments.",
                "action_required": "Implement at least one mitigation strategy immediately"
            }
        elif impact_percent < -5:
            return {
                "recommendation": "acceptable",
                "explanation": "Minor retirement impact that can likely be offset with small adjustments.",
                "action_required": "Monitor and slightly increase contributions if possible"
            }
        else:
            return {
                "recommendation": "positive",
                "explanation": "This career change maintains or improves your retirement trajectory.",
                "action_required": "Stay on track with current savings plan"
            }


class DebtReskillingOptimizer:
    """
    Optimizes the decision between paying off debt vs investing in reskilling/education.
    """

    def optimize_debt_vs_reskilling(
        self,
        current_situation: Dict,
        debt_details: Dict,
        reskilling_options: List[Dict]
    ) -> Dict:
        """
        Analyze whether to prioritize debt payoff or reskilling investment.

        Args:
            current_situation: Current income and financial state
            debt_details: Debt amounts, interest rates, minimum payments
            reskilling_options: Different reskilling/education options with costs and income potential

        Returns:
            Optimized recommendation with financial projections
        """
        current_income = current_situation.get("annual_income", 0)
        monthly_discretionary = current_situation.get("monthly_discretionary", 0)

        # Analyze debt situation
        debt_analysis = self._analyze_debt_burden(debt_details, current_income, monthly_discretionary)

        # Analyze each reskilling option
        reskilling_analyses = []
        for option in reskilling_options:
            analysis = self._analyze_reskilling_roi(
                option=option,
                current_income=current_income,
                debt_burden=debt_analysis
            )
            reskilling_analyses.append(analysis)

        # Sort by ROI
        reskilling_analyses.sort(key=lambda x: x["10_year_roi"], reverse=True)

        # Generate optimization strategies
        strategies = self._generate_optimization_strategies(
            debt_analysis=debt_analysis,
            best_reskilling=reskilling_analyses[0] if reskilling_analyses else None,
            monthly_discretionary=monthly_discretionary
        )

        # Pick optimal strategy
        optimal_strategy = self._select_optimal_strategy(
            strategies=strategies,
            debt_analysis=debt_analysis,
            reskilling_analyses=reskilling_analyses
        )

        return {
            "debt_analysis": debt_analysis,
            "reskilling_options": reskilling_analyses,
            "optimization_strategies": strategies,
            "optimal_strategy": optimal_strategy,
            "recommendation": self._generate_debt_reskilling_recommendation(
                optimal_strategy, debt_analysis
            )
        }

    def _analyze_debt_burden(self, debt_details: Dict, annual_income: float, monthly_discretionary: float) -> Dict:
        """Analyze overall debt burden"""
        total_debt = debt_details.get("total_debt", 0)
        monthly_minimum = debt_details.get("monthly_minimum_payment", 0)
        weighted_interest_rate = debt_details.get("weighted_avg_interest_rate", 0)

        # Debt-to-income ratio
        debt_to_income_ratio = (total_debt / annual_income * 100) if annual_income > 0 else 0

        # Payment-to-discretionary ratio
        payment_ratio = (monthly_minimum / monthly_discretionary * 100) if monthly_discretionary > 0 else 0

        # Time to payoff at minimum payments
        if weighted_interest_rate > 0:
            monthly_rate = weighted_interest_rate / 12 / 100
            if monthly_minimum > total_debt * monthly_rate:
                months_to_payoff = -(1 / monthly_rate) * (total_debt * monthly_rate / monthly_minimum - 1)
                months_to_payoff = round(months_to_payoff, 0)
            else:
                months_to_payoff = 9999  # Never pays off
        else:
            months_to_payoff = round(total_debt / monthly_minimum, 0) if monthly_minimum > 0 else 9999

        # Total interest paid
        total_interest = (monthly_minimum * months_to_payoff) - total_debt if months_to_payoff < 9999 else total_debt

        severity = "critical" if debt_to_income_ratio > 100 or payment_ratio > 50 else \
                  "high" if debt_to_income_ratio > 50 or payment_ratio > 30 else \
                  "moderate" if debt_to_income_ratio > 20 or payment_ratio > 15 else \
                  "low"

        return {
            "total_debt": round(total_debt, 2),
            "monthly_minimum_payment": round(monthly_minimum, 2),
            "weighted_interest_rate": weighted_interest_rate,
            "debt_to_income_ratio": round(debt_to_income_ratio, 1),
            "payment_to_discretionary_ratio": round(payment_ratio, 1),
            "months_to_payoff_minimum": int(months_to_payoff) if months_to_payoff < 9999 else "Never",
            "total_interest_at_minimum": round(total_interest, 2),
            "severity": severity,
            "high_interest_debt": total_debt if weighted_interest_rate > 7 else 0
        }

    def _analyze_reskilling_roi(self, option: Dict, current_income: float, debt_burden: Dict) -> Dict:
        """Analyze ROI of a reskilling option"""
        cost = option.get("total_cost", 0)
        duration_months = option.get("duration_months", 12)
        expected_new_income = option.get("expected_income_after", 0)
        time_to_new_job_months = option.get("time_to_new_job_months", 3)

        # Income opportunity cost during training
        income_lost = 0
        if option.get("full_time", False):
            income_lost = (current_income / 12) * duration_months

        # Total investment
        total_investment = cost + income_lost

        # Annual income increase
        annual_increase = expected_new_income - current_income

        # Breakeven time (months)
        if annual_increase > 0:
            breakeven_months = (total_investment / (annual_increase / 12))
        else:
            breakeven_months = 9999

        # 10-year ROI
        years_earning = 10 - (duration_months + time_to_new_job_months) / 12
        ten_year_gain = (annual_increase * years_earning) - total_investment
        roi_10_year = (ten_year_gain / total_investment * 100) if total_investment > 0 else 0

        return {
            "option_name": option.get("name", "Reskilling Program"),
            "total_cost": round(cost, 2),
            "duration_months": duration_months,
            "income_opportunity_cost": round(income_lost, 2),
            "total_investment": round(total_investment, 2),
            "expected_new_income": round(expected_new_income, 2),
            "annual_income_increase": round(annual_increase, 2),
            "breakeven_months": round(breakeven_months, 1) if breakeven_months < 9999 else "Never",
            "10_year_total_gain": round(ten_year_gain, 2),
            "10_year_roi": round(roi_10_year, 1),
            "financing_available": option.get("financing_available", False),
            "value_rating": "excellent" if roi_10_year > 300 else
                          "good" if roi_10_year > 150 else
                          "moderate" if roi_10_year > 50 else
                          "poor"
        }

    def _generate_optimization_strategies(
        self,
        debt_analysis: Dict,
        best_reskilling: Optional[Dict],
        monthly_discretionary: float
    ) -> List[Dict]:
        """Generate different optimization strategies"""
        strategies = []

        # Strategy 1: Debt-first
        if debt_analysis["total_debt"] > 0:
            aggressive_payment = monthly_discretionary * 0.8
            months_to_clear = debt_analysis["total_debt"] / aggressive_payment if aggressive_payment > 0 else 9999

            strategies.append({
                "name": "Debt-First Strategy",
                "approach": "Pay off debt aggressively before reskilling",
                "monthly_debt_payment": round(aggressive_payment, 2),
                "months_to_debt_free": round(months_to_clear, 0),
                "then": "Start reskilling after debt-free",
                "pros": ["Lower stress", "Better credit", "No debt burden during training"],
                "cons": ["Delayed income increase", "Market opportunity may pass"],
                "timeline_to_higher_income_months": round(months_to_clear + (best_reskilling["duration_months"] if best_reskilling else 12), 0),
                "total_10_year_outcome": "Calculate based on delayed reskilling"
            })

        # Strategy 2: Reskilling-first
        if best_reskilling:
            strategies.append({
                "name": "Reskilling-First Strategy",
                "approach": "Invest in reskilling now, maintain minimum debt payments",
                "upfront_cost": best_reskilling["total_investment"],
                "months_to_higher_income": best_reskilling["duration_months"],
                "pros": ["Faster income increase", "Better long-term earnings", "High ROI"],
                "cons": ["Debt lingers", "Financial stress during training", "Risk if doesn't work out"],
                "timeline_to_higher_income_months": best_reskilling["duration_months"],
                "total_10_year_outcome": best_reskilling["10_year_total_gain"]
            })

        # Strategy 3: Balanced approach
        if best_reskilling and debt_analysis["total_debt"] > 0:
            strategies.append({
                "name": "Balanced Strategy",
                "approach": "Part-time reskilling while making above-minimum debt payments",
                "monthly_debt_payment": round(monthly_discretionary * 0.5, 2),
                "monthly_reskilling_budget": round(monthly_discretionary * 0.3, 2),
                "pros": ["Progress on both fronts", "Lower risk", "Maintains momentum"],
                "cons": ["Slower on both fronts", "Potentially more stressful"],
                "timeline_to_higher_income_months": "18-24 (part-time program)",
                "total_10_year_outcome": "Moderate between debt-first and reskilling-first"
            })

        return strategies

    def _select_optimal_strategy(
        self,
        strategies: List[Dict],
        debt_analysis: Dict,
        reskilling_analyses: List[Dict]
    ) -> Dict:
        """Select the optimal strategy based on situation"""
        # Decision logic
        if debt_analysis["severity"] == "critical":
            # High debt burden - prioritize debt
            optimal = next((s for s in strategies if "Debt-First" in s["name"]), strategies[0])
            optimal["reason"] = "Critical debt burden requires immediate attention"

        elif debt_analysis["severity"] == "low" and reskilling_analyses and reskilling_analyses[0]["10_year_roi"] > 200:
            # Low debt and high ROI reskilling - prioritize reskilling
            optimal = next((s for s in strategies if "Reskilling-First" in s["name"]), strategies[0])
            optimal["reason"] = "Low debt burden and excellent reskilling ROI make this the clear choice"

        elif debt_analysis.get("high_interest_debt", 0) > 10000:
            # High-interest debt - prioritize paying it down
            optimal = next((s for s in strategies if "Debt-First" in s["name"]), strategies[0])
            optimal["reason"] = "High-interest debt should be eliminated before taking on reskilling costs"

        else:
            # Balanced approach makes sense
            optimal = next((s for s in strategies if "Balanced" in s["name"]), strategies[0])
            optimal["reason"] = "Your situation allows for a balanced approach to both debt and career growth"

        return optimal

    def _generate_debt_reskilling_recommendation(self, optimal_strategy: Dict, debt_analysis: Dict) -> Dict:
        """Generate final recommendation"""
        return {
            "primary_recommendation": optimal_strategy["name"],
            "explanation": optimal_strategy["reason"],
            "immediate_actions": [
                "Create detailed budget to maximize discretionary income",
                "Research financing options for reskilling if pursuing education",
                "Calculate exact debt payoff timeline with current strategy",
                "Ensure emergency fund of 3-6 months expenses before major investments"
            ],
            "warnings": self._generate_warnings(debt_analysis, optimal_strategy)
        }

    def _generate_warnings(self, debt_analysis: Dict, strategy: Dict) -> List[str]:
        """Generate specific warnings"""
        warnings = []

        if debt_analysis["severity"] in ["critical", "high"]:
            warnings.append("⚠️ High debt burden - ensure basic needs covered before pursuing reskilling")

        if "Reskilling-First" in strategy["name"] and debt_analysis["weighted_interest_rate"] > 10:
            warnings.append("⚠️ High-interest debt will compound while reskilling - consider paying down first")

        if debt_analysis.get("months_to_payoff_minimum") == "Never":
            warnings.append("⚠️ CRITICAL: Current minimum payments won't eliminate debt - must increase payments")

        return warnings


class FamilyFinancialPlanner:
    """
    Comprehensive family financial planning integrated with career decisions.
    Accounts for spouse income, children, housing, and major life events.
    """

    def analyze_family_financial_impact(
        self,
        family_situation: Dict,
        career_decision: Dict,
        planning_horizon_years: int = 10
    ) -> Dict:
        """
        Analyze how career decision impacts entire family financially.

        Args:
            family_situation: Family details (spouse, kids, expenses, etc.)
            career_decision: Career change details
            planning_horizon_years: Years to project into future

        Returns:
            Comprehensive family financial analysis
        """
        # Extract family details
        marital_status = family_situation.get("marital_status", "single")
        num_children = family_situation.get("num_children", 0)
        children_ages = family_situation.get("children_ages", [])
        spouse_income = family_situation.get("spouse_income", 0)
        monthly_family_expenses = family_situation.get("monthly_expenses", 5000)
        mortgage_payment = family_situation.get("mortgage_payment", 0)

        # Project baseline (staying at current job)
        baseline_projection = self._project_family_finances(
            years=planning_horizon_years,
            primary_income=family_situation.get("primary_income", 0),
            spouse_income=spouse_income,
            monthly_expenses=monthly_family_expenses,
            children_ages=children_ages,
            career_change=None
        )

        # Project with career change
        change_projection = self._project_family_finances(
            years=planning_horizon_years,
            primary_income=family_situation.get("primary_income", 0),
            spouse_income=spouse_income,
            monthly_expenses=monthly_family_expenses,
            children_ages=children_ages,
            career_change=career_decision
        )

        # Calculate impact
        impact_analysis = self._calculate_family_impact(
            baseline=baseline_projection,
            with_change=change_projection,
            family_situation=family_situation
        )

        # Children-specific considerations
        children_impact = self._analyze_children_impact(
            children_ages=children_ages,
            financial_change=impact_analysis,
            planning_horizon=planning_horizon_years
        )

        # Spouse considerations
        spouse_impact = self._analyze_spouse_impact(
            spouse_income=spouse_income,
            primary_income_change=career_decision.get("income_change", 0),
            marital_status=marital_status
        )

        # Risk assessment
        family_risk = self._assess_family_financial_risk(
            family_situation=family_situation,
            impact_analysis=impact_analysis
        )

        return {
            "baseline_projection": baseline_projection,
            "with_change_projection": change_projection,
            "impact_analysis": impact_analysis,
            "children_considerations": children_impact,
            "spouse_considerations": spouse_impact,
            "family_risk_assessment": family_risk,
            "recommendation": self._generate_family_recommendation(
                impact_analysis, family_risk, family_situation
            )
        }

    def _project_family_finances(
        self,
        years: int,
        primary_income: float,
        spouse_income: float,
        monthly_expenses: float,
        children_ages: List[int],
        career_change: Optional[Dict]
    ) -> Dict:
        """Project family finances over time"""
        annual_savings = []
        cumulative_savings = 0

        for year in range(years):
            # Calculate income for this year
            if career_change and year == 0:
                # First year with career change
                primary_annual = career_change.get("new_income", primary_income)
                months_earning = 12 - career_change.get("months_without_income", 0)
                primary_annual = primary_annual * (months_earning / 12)
                # Subtract reskilling cost
                primary_annual -= career_change.get("reskilling_cost", 0)
            else:
                primary_annual = primary_income * (1.03 ** year)  # 3% annual raise

            spouse_annual = spouse_income * (1.03 ** year)
            total_annual_income = primary_annual + spouse_annual

            # Calculate expenses for this year
            base_expenses = monthly_expenses * 12 * (1.02 ** year)  # 2% inflation

            # Add child-related expenses
            child_expenses = sum(
                self._calculate_child_expenses(age + year)
                for age in children_ages
            )

            total_expenses = base_expenses + child_expenses

            # Annual savings
            year_savings = total_annual_income - total_expenses
            cumulative_savings += year_savings

            annual_savings.append({
                "year": year + 1,
                "total_income": round(total_annual_income, 2),
                "total_expenses": round(total_expenses, 2),
                "annual_savings": round(year_savings, 2),
                "cumulative_savings": round(cumulative_savings, 2)
            })

        return {
            "total_10_year_income": round(sum(y["total_income"] for y in annual_savings), 2),
            "total_10_year_expenses": round(sum(y["total_expenses"] for y in annual_savings), 2),
            "total_10_year_savings": round(sum(y["annual_savings"] for y in annual_savings), 2),
            "final_cumulative_savings": round(cumulative_savings, 2),
            "year_by_year": annual_savings
        }

    def _calculate_child_expenses(self, age: int) -> float:
        """Calculate annual expenses for a child of given age"""
        if age < 5:
            return 15000  # Daycare, diapers, etc.
        elif age < 12:
            return 12000  # School, activities
        elif age < 18:
            return 15000  # Teenager expenses, driving
        elif age < 22:
            return 25000  # College expenses
        else:
            return 0  # Adult

    def _calculate_family_impact(self, baseline: Dict, with_change: Dict, family_situation: Dict) -> Dict:
        """Calculate impact of career change on family"""
        savings_difference = with_change["total_10_year_savings"] - baseline["total_10_year_savings"]

        return {
            "10_year_savings_impact": round(savings_difference, 2),
            "average_annual_impact": round(savings_difference / 10, 2),
            "severity": "positive" if savings_difference >= 0 else
                       "manageable" if savings_difference > -50000 else
                       "concerning" if savings_difference > -150000 else
                       "severe"
        }

    def _analyze_children_impact(self, children_ages: List[int], financial_change: Dict, planning_horizon: int) -> Dict:
        """Analyze how career change affects children"""
        if not children_ages:
            return {"applicable": False}

        # Identify children approaching college
        college_bound = [age for age in children_ages if 18 - age <= planning_horizon and age < 18]

        considerations = []

        if college_bound:
            years_to_first_college = min(18 - age for age in college_bound)
            considerations.append(f"First child starts college in {years_to_first_college} years - ensure adequate savings")

        if financial_change["severity"] in ["concerning", "severe"] and college_bound:
            considerations.append("⚠️ Reduced savings may impact college funding - consider 529 plan adjustments")

        if any(age < 5 for age in children_ages):
            considerations.append("Young children provide flexibility for career change but also highest childcare costs")

        return {
            "applicable": True,
            "num_children": len(children_ages),
            "college_bound_in_horizon": len(college_bound),
            "considerations": considerations
        }

    def _analyze_spouse_impact(self, spouse_income: float, primary_income_change: float, marital_status: str) -> Dict:
        """Analyze impact on spouse/partner"""
        if marital_status == "single":
            return {"applicable": False}

        # Income dependency
        if spouse_income == 0:
            dependency = "full"
            risk_level = "high"
        elif spouse_income < primary_income_change:
            dependency = "significant"
            risk_level = "moderate"
        else:
            dependency = "low"
            risk_level = "low"

        return {
            "applicable": True,
            "spouse_income": round(spouse_income, 2),
            "income_dependency": dependency,
            "risk_level": risk_level,
            "recommendation": "Ensure spouse is aligned on career change" if dependency != "low" else
                            "Dual income provides buffer for career change"
        }

    def _assess_family_financial_risk(self, family_situation: Dict, impact_analysis: Dict) -> Dict:
        """Assess overall family financial risk"""
        risk_factors = []
        risk_score = 0

        # Single income household
        if family_situation.get("spouse_income", 0) == 0 and family_situation.get("marital_status") != "single":
            risk_factors.append("Single income household - no backup if career change fails")
            risk_score += 25

        # Multiple dependents
        num_children = family_situation.get("num_children", 0)
        if num_children >= 3:
            risk_factors.append(f"{num_children} children - significant financial responsibility")
            risk_score += 20
        elif num_children >= 1:
            risk_score += 10

        # Mortgage burden
        mortgage = family_situation.get("mortgage_payment", 0)
        if mortgage > 3000:
            risk_factors.append("High mortgage payment - limited financial flexibility")
            risk_score += 15

        # Emergency fund
        emergency_fund = family_situation.get("emergency_fund_months", 3)
        if emergency_fund < 6:
            risk_factors.append(f"Only {emergency_fund} months emergency fund - below recommended 6+ months")
            risk_score += 20

        # Financial impact severity
        if impact_analysis["severity"] in ["concerning", "severe"]:
            risk_factors.append("Career change has significant negative financial impact")
            risk_score += 30

        risk_level = "critical" if risk_score >= 70 else \
                    "high" if risk_score >= 50 else \
                    "moderate" if risk_score >= 30 else \
                    "low"

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "mitigation_required": risk_level in ["critical", "high"]
        }

    def _generate_family_recommendation(
        self,
        impact_analysis: Dict,
        risk_assessment: Dict,
        family_situation: Dict
    ) -> Dict:
        """Generate family-focused recommendation"""
        if risk_assessment["risk_level"] == "critical":
            decision = "not_recommended"
            explanation = "This career change poses critical financial risk to your family. Reconsider or significantly de-risk before proceeding."
        elif risk_assessment["risk_level"] == "high":
            decision = "proceed_with_caution"
            explanation = "Significant family financial risk. Only proceed if you can mitigate key risk factors."
        elif risk_assessment["risk_level"] == "moderate":
            decision = "acceptable_with_planning"
            explanation = "Manageable family impact with proper planning and communication."
        else:
            decision = "recommended"
            explanation = "Low family financial risk. Good opportunity for career growth."

        family_discussion_points = [
            "Discuss timeline and financial impact with spouse/partner",
            f"Ensure {family_situation.get('emergency_fund_months', 3)}+ months emergency fund before proceeding",
            "Create backup plan if career change doesn't work out",
            "Consider spouse increasing income or reducing expenses as buffer"
        ]

        return {
            "decision": decision,
            "explanation": explanation,
            "family_discussion_points": family_discussion_points,
            "critical_next_steps": risk_assessment["risk_factors"][:3] if risk_assessment["risk_factors"] else []
        }
