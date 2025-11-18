"""
Salary Negotiation Coach
AI-powered salary negotiation strategies with market data and personalized tactics
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum


class NegotiationStrategy(str, Enum):
    AGGRESSIVE = "aggressive"
    BALANCED = "balanced"
    CONSERVATIVE = "conservative"


class NegotiationPhase(str, Enum):
    INITIAL_OFFER = "initial_offer"
    COUNTEROFFER = "counteroffer"
    BENEFITS_DISCUSSION = "benefits_discussion"
    FINAL_NEGOTIATION = "final_negotiation"


class LeverageLevel(str, Enum):
    STRONG = "strong"
    MODERATE = "moderate"
    WEAK = "weak"


class SalaryNegotiationCoach:
    """Comprehensive salary negotiation coaching and strategy system"""

    def __init__(self):
        # Industry salary multipliers (relative to baseline)
        self.industry_multipliers = {
            "tech": 1.3,
            "finance": 1.4,
            "consulting": 1.35,
            "healthcare": 1.1,
            "retail": 0.85,
            "education": 0.8,
            "nonprofit": 0.75
        }

        # Location cost of living adjustments
        self.location_multipliers = {
            "san_francisco": 1.35,
            "new_york": 1.30,
            "seattle": 1.20,
            "austin": 1.10,
            "chicago": 1.05,
            "denver": 1.05,
            "atlanta": 0.95,
            "remote": 0.90
        }

    def analyze_offer(self, offer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze job offer and provide negotiation recommendations

        Args:
            offer_data: Offer details including salary, benefits, role, etc.

        Returns:
            Comprehensive offer analysis with negotiation strategies
        """
        # Extract offer components
        base_salary = offer_data.get("base_salary", 0)
        bonus_target = offer_data.get("bonus_target", 0)
        equity_value = offer_data.get("equity_value", 0)
        role = offer_data.get("role", "")
        industry = offer_data.get("industry", "tech")
        location = offer_data.get("location", "")
        years_experience = offer_data.get("years_experience", 0)

        # Calculate market rates
        market_analysis = self._calculate_market_rate(
            role, industry, location, years_experience
        )

        # Total compensation analysis
        total_comp = base_salary + bonus_target + equity_value
        market_median = market_analysis["median"]
        market_p75 = market_analysis["percentile_75"]
        market_p90 = market_analysis["percentile_90"]

        # Determine offer quality
        if total_comp >= market_p90:
            offer_quality = "excellent"
            negotiation_urgency = "low"
        elif total_comp >= market_p75:
            offer_quality = "good"
            negotiation_urgency = "low"
        elif total_comp >= market_median:
            offer_quality = "fair"
            negotiation_urgency = "medium"
        elif total_comp >= market_median * 0.9:
            offer_quality = "below_market"
            negotiation_urgency = "high"
        else:
            offer_quality = "poor"
            negotiation_urgency = "critical"

        # Calculate negotiation targets
        targets = self._calculate_negotiation_targets(
            base_salary, total_comp, market_median, market_p75, market_p90
        )

        # Assess leverage
        leverage = self._assess_leverage(offer_data)

        # Generate negotiation strategy
        strategy = self._generate_strategy(
            offer_quality, leverage, targets, offer_data
        )

        # Calculate potential gains
        potential_gains = self._calculate_potential_gains(
            base_salary, targets, years_experience
        )

        return {
            "offer_summary": {
                "total_compensation": total_comp,
                "base_salary": base_salary,
                "bonus_target": bonus_target,
                "equity_value": equity_value
            },
            "market_analysis": {
                "market_median": market_median,
                "percentile_75": market_p75,
                "percentile_90": market_p90,
                "offer_vs_market": round(((total_comp - market_median) / market_median) * 100, 1)
            },
            "offer_quality": offer_quality,
            "negotiation_urgency": negotiation_urgency,
            "leverage_assessment": leverage,
            "negotiation_targets": targets,
            "recommended_strategy": strategy,
            "potential_lifetime_gains": potential_gains,
            "should_negotiate": offer_quality in ["fair", "below_market", "poor"],
            "negotiation_scripts": self._generate_scripts(targets, leverage, offer_quality),
            "common_mistakes_to_avoid": self._get_common_mistakes()
        }

    def generate_counteroffer(self, current_offer: Dict[str, Any],
                             target_comp: float,
                             leverage_level: str) -> Dict[str, Any]:
        """
        Generate structured counteroffer

        Args:
            current_offer: Current offer details
            target_comp: Desired total compensation
            leverage_level: Your leverage level (strong/moderate/weak)

        Returns:
            Counteroffer structure with justification
        """
        base_salary = current_offer.get("base_salary", 0)
        bonus_target = current_offer.get("bonus_target", 0)

        # Determine counteroffer amount based on leverage
        if leverage_level == LeverageLevel.STRONG.value:
            # Ask for higher amount, expecting negotiation
            counteroffer_base = target_comp * 1.15
        elif leverage_level == LeverageLevel.MODERATE.value:
            # Ask for target plus small buffer
            counteroffer_base = target_comp * 1.08
        else:
            # Ask for target exactly
            counteroffer_base = target_comp * 1.03

        # Allocate between salary and bonus
        suggested_base = base_salary * 1.15 if leverage_level == LeverageLevel.STRONG.value else base_salary * 1.10
        remaining_for_bonus = counteroffer_base - suggested_base

        # Justification points
        justifications = []

        market_data = current_offer.get("market_median", base_salary * 1.1)
        if suggested_base <= market_data:
            justifications.append({
                "point": "Market Rate Alignment",
                "detail": f"Based on market research, the median for this role is ${market_data:,.0f}"
            })

        if current_offer.get("years_experience", 0) > 5:
            justifications.append({
                "point": "Experience Premium",
                "detail": f"{current_offer.get('years_experience')} years of relevant experience with proven track record"
            })

        if current_offer.get("unique_skills", []):
            justifications.append({
                "point": "Specialized Skills",
                "detail": f"Bringing specialized expertise in {', '.join(current_offer.get('unique_skills', [])[:3])}"
            })

        if current_offer.get("competing_offers", False):
            justifications.append({
                "point": "Competitive Offers",
                "detail": "Currently evaluating other opportunities with higher compensation packages"
            })

        # Alternative asks if they can't meet salary
        alternative_asks = [
            {
                "ask": "Signing Bonus",
                "amount": round(base_salary * 0.10),
                "justification": "One-time payment to offset relocation or opportunity cost"
            },
            {
                "ask": "Performance Review Timeline",
                "detail": "6-month review instead of annual, with potential 10-15% raise",
                "value": round(base_salary * 0.12)
            },
            {
                "ask": "Additional Equity",
                "amount": round(current_offer.get("equity_value", 0) * 0.25),
                "justification": "Additional stock options to align with market packages"
            },
            {
                "ask": "Enhanced Benefits",
                "options": ["Additional PTO (5 days)", "Professional development budget ($5k)", "Remote work flexibility"],
                "estimated_value": 10000
            },
            {
                "ask": "Guaranteed Bonus",
                "amount": round(bonus_target * 0.75),
                "justification": "Minimum 75% of target bonus guaranteed first year"
            }
        ]

        # Counteroffer script
        script = self._generate_counteroffer_script(
            suggested_base, remaining_for_bonus, justifications, leverage_level
        )

        return {
            "counteroffer_total": round(counteroffer_base),
            "suggested_base_salary": round(suggested_base),
            "suggested_bonus": round(remaining_for_bonus),
            "increase_over_offer": round(((counteroffer_base - (base_salary + bonus_target)) / (base_salary + bonus_target)) * 100, 1),
            "justifications": justifications,
            "alternative_asks": alternative_asks,
            "counteroffer_script": script,
            "delivery_tips": self._get_delivery_tips(leverage_level),
            "timing_recommendation": self._get_timing_recommendation(),
            "success_probability": self._estimate_success_probability(leverage_level, counteroffer_base, base_salary)
        }

    def benefits_negotiation_guide(self, offer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Guide for negotiating benefits beyond salary

        Args:
            offer_data: Offer details and worker preferences

        Returns:
            Benefits negotiation strategies prioritized by value
        """
        base_salary = offer_data.get("base_salary", 100000)

        # Categorize benefits by negotiability and value
        negotiable_benefits = [
            {
                "benefit": "Signing Bonus",
                "negotiability": "high",
                "typical_value": round(base_salary * 0.10),
                "value_range": f"${base_salary * 0.05:,.0f} - ${base_salary * 0.20:,.0f}",
                "pitch": "To offset relocation costs and opportunity cost of leaving current role",
                "success_rate": "70%"
            },
            {
                "benefit": "Additional PTO",
                "negotiability": "high",
                "typical_value": 5000,  # ~1 week worth
                "value_range": "2-5 extra days",
                "pitch": "Based on years of experience and industry standards for senior professionals",
                "success_rate": "65%"
            },
            {
                "benefit": "Remote Work Flexibility",
                "negotiability": "high",
                "typical_value": 8000,  # Commute + flexibility value
                "value_range": "1-5 days remote per week",
                "pitch": "Demonstrated ability to work effectively remote, improves work-life balance",
                "success_rate": "75%"
            },
            {
                "benefit": "Professional Development Budget",
                "negotiability": "medium",
                "typical_value": 3000,
                "value_range": "$2,000 - $10,000 annually",
                "pitch": "For conferences, courses, certifications to keep skills current",
                "success_rate": "60%"
            },
            {
                "benefit": "Equity/Stock Options",
                "negotiability": "medium",
                "typical_value": round(base_salary * 0.15),
                "value_range": "10-50% more RSUs/options",
                "pitch": "To align compensation with market rate and align incentives",
                "success_rate": "50%"
            },
            {
                "benefit": "Earlier Performance Review",
                "negotiability": "high",
                "typical_value": round(base_salary * 0.10),
                "value_range": "6-month instead of 12-month review",
                "pitch": "Opportunity to prove value quickly and align compensation accordingly",
                "success_rate": "70%"
            },
            {
                "benefit": "Title Upgrade",
                "negotiability": "medium",
                "typical_value": 15000,  # Long-term career value
                "value_range": "One level up",
                "pitch": "Skills and experience align with senior level, important for career trajectory",
                "success_rate": "40%"
            },
            {
                "benefit": "Relocation Package",
                "negotiability": "medium",
                "typical_value": 10000,
                "value_range": "$5,000 - $50,000",
                "pitch": "Cover moving costs, temporary housing, travel",
                "success_rate": "80%",
                "conditional": "Only if relocating"
            },
            {
                "benefit": "Home Office Stipend",
                "negotiability": "high",
                "typical_value": 2000,
                "value_range": "$1,000 - $5,000 one-time",
                "pitch": "For ergonomic setup if working remotely",
                "success_rate": "75%",
                "conditional": "Only if remote"
            },
            {
                "benefit": "Commuter Benefits",
                "negotiability": "low",
                "typical_value": 3000,
                "value_range": "$200-300/month",
                "pitch": "Standard benefit for on-site employees",
                "success_rate": "90%"
            }
        ]

        # Prioritize based on value and success rate
        for benefit in negotiable_benefits:
            value = benefit.get("typical_value", 0)
            success = float(benefit.get("success_rate", "50%").rstrip("%")) / 100
            benefit["expected_value"] = round(value * success)

        negotiable_benefits.sort(key=lambda x: x["expected_value"], reverse=True)

        # Create negotiation package
        package_options = {
            "conservative_package": self._create_benefits_package(
                negotiable_benefits, base_salary * 0.05, "conservative"
            ),
            "balanced_package": self._create_benefits_package(
                negotiable_benefits, base_salary * 0.10, "balanced"
            ),
            "aggressive_package": self._create_benefits_package(
                negotiable_benefits, base_salary * 0.15, "aggressive"
            )
        }

        return {
            "all_negotiable_benefits": negotiable_benefits,
            "top_priorities": negotiable_benefits[:5],
            "negotiation_packages": package_options,
            "benefits_scripts": self._generate_benefits_scripts(),
            "negotiation_sequence": [
                "1. Start with salary negotiation",
                "2. If salary is firm, pivot to signing bonus",
                "3. Negotiate PTO and remote work (high success rate)",
                "4. Ask for professional development budget",
                "5. Request earlier performance review",
                "6. Discuss equity if startup/growth company"
            ],
            "power_phrases": self._get_benefits_power_phrases()
        }

    def leverage_assessment(self, situation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess negotiation leverage

        Args:
            situation: Current situation details

        Returns:
            Leverage analysis and how to maximize it
        """
        leverage_score = 50  # Base score

        # Competing offers
        if situation.get("has_competing_offers", False):
            leverage_score += 25
            competing_boost = "Strong leverage point"
        else:
            competing_boost = "Reduces leverage significantly"

        # Current employment
        if situation.get("currently_employed", False):
            leverage_score += 15
            employment_boost = "Good leverage - not desperate"
        else:
            leverage_score -= 10
            employment_boost = "Weaker position - unemployed"

        # Unique skills
        unique_skills_count = len(situation.get("unique_skills", []))
        if unique_skills_count >= 3:
            leverage_score += 20
            skills_boost = "Strong - brings rare skills"
        elif unique_skills_count >= 1:
            leverage_score += 10
            skills_boost = "Moderate - some unique value"
        else:
            skills_boost = "Weak - no unique differentiation"

        # Market demand for role
        market_demand = situation.get("market_demand", "moderate")
        if market_demand == "high":
            leverage_score += 15
            demand_boost = "High demand for your role"
        elif market_demand == "low":
            leverage_score -= 15
            demand_boost = "Low demand reduces leverage"
        else:
            demand_boost = "Moderate market demand"

        # Company urgency
        if situation.get("company_urgency", "normal") == "urgent":
            leverage_score += 15
            urgency_boost = "Company needs to fill quickly"
        else:
            urgency_boost = "Normal hiring timeline"

        # Interview performance
        if situation.get("interview_feedback", "good") == "excellent":
            leverage_score += 10
            performance_boost = "Strong interview - they want you"
        else:
            performance_boost = "Standard performance"

        leverage_score = max(0, min(100, leverage_score))

        # Determine overall leverage
        if leverage_score >= 75:
            leverage_level = LeverageLevel.STRONG
            recommendation = "Negotiate aggressively - you're in a strong position"
        elif leverage_score >= 50:
            leverage_level = LeverageLevel.MODERATE
            recommendation = "Negotiate tactfully - reasonable asks will likely succeed"
        else:
            leverage_level = LeverageLevel.WEAK
            recommendation = "Negotiate carefully - focus on high-success items like PTO, remote work"

        # How to maximize leverage
        leverage_builders = []
        if not situation.get("has_competing_offers"):
            leverage_builders.append({
                "action": "Get competing offers",
                "impact": "+25 points",
                "how": "Apply to 3-5 similar roles, get to offer stage"
            })

        if unique_skills_count < 2:
            leverage_builders.append({
                "action": "Highlight unique value",
                "impact": "+10-20 points",
                "how": "Document specific skills/achievements they can't easily find elsewhere"
            })

        if situation.get("interview_feedback") != "excellent":
            leverage_builders.append({
                "action": "Strengthen final impression",
                "impact": "+10 points",
                "how": "Send detailed follow-up showing enthusiasm and fit"
            })

        return {
            "leverage_score": round(leverage_score, 1),
            "leverage_level": leverage_level.value,
            "overall_assessment": recommendation,
            "leverage_factors": {
                "competing_offers": {
                    "status": "Yes" if situation.get("has_competing_offers") else "No",
                    "impact": competing_boost
                },
                "employment_status": {
                    "status": "Employed" if situation.get("currently_employed") else "Unemployed",
                    "impact": employment_boost
                },
                "unique_skills": {
                    "status": f"{unique_skills_count} unique skills",
                    "impact": skills_boost
                },
                "market_demand": {
                    "status": market_demand,
                    "impact": demand_boost
                },
                "company_urgency": {
                    "status": situation.get("company_urgency", "normal"),
                    "impact": urgency_boost
                },
                "interview_performance": {
                    "status": situation.get("interview_feedback", "good"),
                    "impact": performance_boost
                }
            },
            "leverage_builders": leverage_builders,
            "negotiation_window": self._calculate_negotiation_window(leverage_score)
        }

    def _calculate_market_rate(self, role: str, industry: str,
                              location: str, years_exp: int) -> Dict[str, float]:
        """Calculate market rate for position"""
        # Base rates by role (simplified - would use real market data)
        base_rates = {
            "software_engineer": 110000,
            "data_scientist": 120000,
            "product_manager": 130000,
            "designer": 95000,
            "marketing_manager": 100000,
            "sales_manager": 110000,
            "default": 85000
        }

        base = base_rates.get(role.lower().replace(" ", "_"), base_rates["default"])

        # Adjust for industry
        industry_mult = self.industry_multipliers.get(industry.lower(), 1.0)
        base *= industry_mult

        # Adjust for location
        location_mult = self.location_multipliers.get(location.lower().replace(" ", "_"), 1.0)
        base *= location_mult

        # Adjust for experience (5% per year after year 2)
        if years_exp > 2:
            base *= (1 + ((years_exp - 2) * 0.05))

        # Calculate percentiles
        median = base
        p75 = base * 1.20
        p90 = base * 1.45

        return {
            "median": round(median),
            "percentile_75": round(p75),
            "percentile_90": round(p90)
        }

    def _calculate_negotiation_targets(self, base_salary: float, total_comp: float,
                                       market_median: float, market_p75: float,
                                       market_p90: float) -> Dict[str, Any]:
        """Calculate negotiation targets"""
        return {
            "minimum_acceptable": round(market_median * 0.95),
            "target": round(market_p75),
            "aspirational": round(market_p90),
            "recommended_ask": round(market_p75 * 1.10),  # Ask for more than target
            "rationale": {
                "minimum": "Should not accept below market median",
                "target": "Fair market rate at 75th percentile",
                "aspirational": "Top tier - justify with unique value",
                "ask": "Start 10% above target to leave negotiation room"
            }
        }

    def _assess_leverage(self, offer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Quick leverage assessment"""
        leverage_score = 50

        if offer_data.get("competing_offers", False):
            leverage_score += 25
        if offer_data.get("currently_employed", False):
            leverage_score += 15
        if len(offer_data.get("unique_skills", [])) >= 2:
            leverage_score += 15

        if leverage_score >= 75:
            level = LeverageLevel.STRONG.value
        elif leverage_score >= 50:
            level = LeverageLevel.MODERATE.value
        else:
            level = LeverageLevel.WEAK.value

        return {
            "level": level,
            "score": leverage_score,
            "summary": f"{level.capitalize()} negotiation position"
        }

    def _generate_strategy(self, offer_quality: str, leverage: Dict[str, Any],
                          targets: Dict[str, Any], offer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate negotiation strategy"""
        strategy_type = NegotiationStrategy.BALANCED

        if leverage["level"] == LeverageLevel.STRONG.value:
            if offer_quality in ["below_market", "poor"]:
                strategy_type = NegotiationStrategy.AGGRESSIVE
            else:
                strategy_type = NegotiationStrategy.BALANCED
        elif leverage["level"] == LeverageLevel.WEAK.value:
            strategy_type = NegotiationStrategy.CONSERVATIVE

        strategies = {
            NegotiationStrategy.AGGRESSIVE.value: {
                "approach": "Direct, confident negotiation",
                "ask_amount": targets["aspirational"],
                "talking_points": [
                    "Emphasize competing offers and market data",
                    "Be willing to walk away if not met",
                    "Ask for top-tier package"
                ],
                "timeline": "Respond within 2-3 days with counteroffer"
            },
            NegotiationStrategy.BALANCED.value: {
                "approach": "Collaborative, data-driven negotiation",
                "ask_amount": targets["recommended_ask"],
                "talking_points": [
                    "Reference market data and experience",
                    "Express enthusiasm while advocating for fair comp",
                    "Open to creative solutions"
                ],
                "timeline": "Respond within 3-5 days after research"
            },
            NegotiationStrategy.CONSERVATIVE.value: {
                "approach": "Gracious negotiation focused on benefits",
                "ask_amount": targets["target"],
                "talking_points": [
                    "Express gratitude for offer",
                    "Gently mention market research",
                    "Focus on non-salary benefits if needed"
                ],
                "timeline": "Respond within 5-7 days, build rapport first"
            }
        }

        return {
            "strategy_type": strategy_type.value,
            "details": strategies[strategy_type.value],
            "success_probability": self._estimate_success_probability(
                leverage["level"],
                strategies[strategy_type.value]["ask_amount"],
                offer_data.get("base_salary", 0)
            )
        }

    def _calculate_potential_gains(self, base_salary: float,
                                   targets: Dict[str, Any],
                                   years_experience: int) -> Dict[str, Any]:
        """Calculate lifetime value of negotiation"""
        # Assume 3-year tenure at company
        years_at_company = 3
        # Assume 3% annual raise
        annual_raise = 0.03

        # Calculate total earnings at current offer
        current_total = 0
        for year in range(years_at_company):
            current_total += base_salary * ((1 + annual_raise) ** year)

        # Calculate total with successful negotiation (to target)
        target_base = targets["target"]
        negotiated_total = 0
        for year in range(years_at_company):
            negotiated_total += target_base * ((1 + annual_raise) ** year)

        gain_3_years = negotiated_total - current_total

        # Future impact (compounding effect on future salaries)
        # New job offers typically based on current salary
        estimated_career_years = max(0, 40 - years_experience)
        # Conservative estimate: 10% of the base increase carries forward
        annual_future_benefit = (target_base - base_salary) * 0.10
        lifetime_future_benefit = annual_future_benefit * estimated_career_years

        return {
            "immediate_gain_3_years": round(gain_3_years),
            "estimated_lifetime_impact": round(lifetime_future_benefit),
            "total_potential_gain": round(gain_3_years + lifetime_future_benefit),
            "explanation": f"A ${round(target_base - base_salary):,} increase now compounds over your career",
            "worth_the_effort": "Absolutely - even modest increases have major long-term impact"
        }

    def _generate_scripts(self, targets: Dict[str, Any],
                         leverage: Dict[str, Any],
                         offer_quality: str) -> Dict[str, str]:
        """Generate negotiation scripts"""
        return {
            "initial_response": f"""
Thank you so much for the offer. I'm excited about the opportunity and the potential to contribute to the team.

I'd like to take a few days to review the details carefully and discuss with my family. Could we schedule a call early next week to discuss the offer?

I appreciate your understanding.
            """.strip(),

            "counteroffer_opening": f"""
Thank you for the opportunity. I'm very enthusiastic about joining the team and contributing to [specific project/goal].

After careful consideration and market research, I was hoping we could discuss the compensation package. Based on my [X years] of experience and the market rate for this role in [location], I was targeting a base salary in the range of ${targets['recommended_ask']:,}.

I'm confident I can deliver significant value, and I'd love to find a package that reflects that. Are you open to discussing this?
            """.strip(),

            "if_they_cant_meet_salary": f"""
I understand there may be constraints on the base salary. I'm still very interested in the role.

Would it be possible to explore alternatives such as:
- A signing bonus
- Additional equity
- An earlier performance review (6 months instead of 12)
- Additional PTO or flexible work arrangements

I'm flexible and want to find a solution that works for both of us.
            """.strip(),

            "accepting_offer": f"""
Thank you so much for working with me on this. I'm thrilled to accept the offer and join the team.

I look forward to starting on [date] and contributing to [specific goal]. Please send over the formal offer letter and any next steps.

Thank you again for this opportunity!
            """.strip(),

            "declining_offer": f"""
Thank you so much for the offer and for the time you've invested in the interview process. I really enjoyed learning about the team and the opportunity.

After careful consideration, I've decided to pursue another opportunity that's a better fit for my career goals at this time.

I have tremendous respect for [company] and hope our paths cross again in the future.
            """.strip()
        }

    def _generate_counteroffer_script(self, target_base: float,
                                     target_bonus: float,
                                     justifications: List[Dict[str, Any]],
                                     leverage_level: str) -> str:
        """Generate detailed counteroffer script"""
        just_text = "\n".join([f"- {j['point']}: {j['detail']}" for j in justifications[:3]])

        return f"""
Subject: Re: Job Offer - [Your Name]

Dear [Hiring Manager],

Thank you again for the offer. I'm genuinely excited about the opportunity to join [Company] and contribute to [specific project/team].

After careful consideration and market research, I was hoping we could discuss the compensation package. I'm targeting a total compensation of approximately ${round(target_base + target_bonus):,}, with a base salary of ${round(target_base):,}.

This is based on several factors:
{just_text}

I'm confident I can deliver exceptional value in this role, and I believe this compensation aligns with the impact I'll make.

I'm flexible and open to discussing creative solutions if there are constraints. I'm also interested in discussing [signing bonus/equity/other benefits] as alternatives.

Would you be open to a brief call to discuss this? I'm excited about joining the team and want to find a package that works for both of us.

Best regards,
[Your Name]
        """.strip()

    def _get_delivery_tips(self, leverage_level: str) -> List[str]:
        """Get tips for delivering counteroffer"""
        tips = [
            "Always express enthusiasm for the role first",
            "Use market data, not personal needs, as justification",
            "Be specific with numbers - shows you've done research",
            "Ask for a conversation, not a demand",
            "Be prepared to explain your value proposition",
            "Stay professional and collaborative",
            "Don't apologize for negotiating - it's expected"
        ]

        if leverage_level == LeverageLevel.STRONG.value:
            tips.append("With strong leverage, you can be more direct and confident")
        elif leverage_level == LeverageLevel.WEAK.value:
            tips.append("With weaker leverage, emphasize gratitude and flexibility")

        return tips

    def _get_timing_recommendation(self) -> Dict[str, str]:
        """Get timing recommendations for negotiation"""
        return {
            "when_to_respond": "3-5 business days after receiving offer",
            "rationale": "Shows you're thoughtful without seeming uninterested",
            "too_fast": "Same day makes you seem desperate",
            "too_slow": "More than 1 week seems like you're not excited",
            "best_practice": "Thank them immediately, then ask for a few days to review"
        }

    def _estimate_success_probability(self, leverage_level: str,
                                     ask_amount: float,
                                     current_offer: float) -> Dict[str, Any]:
        """Estimate probability of successful negotiation"""
        increase_percentage = ((ask_amount - current_offer) / current_offer) * 100

        # Base success rate by leverage
        base_rates = {
            LeverageLevel.STRONG.value: 75,
            LeverageLevel.MODERATE.value: 55,
            LeverageLevel.WEAK.value: 35
        }

        success_rate = base_rates.get(leverage_level, 50)

        # Adjust for ask size
        if increase_percentage <= 5:
            success_rate += 15
        elif increase_percentage <= 10:
            success_rate += 5
        elif increase_percentage <= 20:
            pass  # No adjustment
        elif increase_percentage <= 30:
            success_rate -= 15
        else:
            success_rate -= 30

        success_rate = max(0, min(100, success_rate))

        return {
            "probability": f"{success_rate}%",
            "confidence": "high" if success_rate >= 60 else "moderate" if success_rate >= 40 else "low",
            "recommendation": self._get_probability_recommendation(success_rate)
        }

    def _get_probability_recommendation(self, success_rate: float) -> str:
        """Get recommendation based on success probability"""
        if success_rate >= 70:
            return "Strong chance - proceed with confidence"
        elif success_rate >= 50:
            return "Reasonable chance - negotiate tactfully"
        elif success_rate >= 30:
            return "Lower chance - have backup asks ready"
        else:
            return "Low chance - focus on benefits over salary"

    def _create_benefits_package(self, benefits: List[Dict[str, Any]],
                                target_value: float,
                                style: str) -> Dict[str, Any]:
        """Create benefits negotiation package"""
        package = []
        total_value = 0

        if style == "conservative":
            # High success rate items only
            candidates = [b for b in benefits if float(b.get("success_rate", "0%").rstrip("%")) >= 65]
        elif style == "aggressive":
            # Include lower success items for higher total value
            candidates = benefits
        else:  # balanced
            candidates = [b for b in benefits if float(b.get("success_rate", "0%").rstrip("%")) >= 50]

        for benefit in candidates:
            if total_value >= target_value:
                break
            package.append(benefit["benefit"])
            total_value += benefit.get("typical_value", 0)

        return {
            "benefits": package[:5],  # Top 5
            "estimated_total_value": round(total_value),
            "package_style": style
        }

    def _generate_benefits_scripts(self) -> Dict[str, str]:
        """Generate scripts for benefits negotiation"""
        return {
            "signing_bonus": "Given the opportunity cost of leaving my current role and the transition period, would a signing bonus be possible?",
            "additional_pto": "Based on my [X] years of experience, would it be possible to start with [X] additional PTO days?",
            "remote_work": "I work very effectively in a remote setting. Would there be flexibility for [X] days remote per week?",
            "professional_development": "I'm committed to continuous learning. Does the company offer a professional development budget for courses and conferences?",
            "earlier_review": "I'm confident I can prove my value quickly. Would it be possible to have a performance review at 6 months instead of 12?"
        }

    def _get_benefits_power_phrases(self) -> List[str]:
        """Get powerful phrases for benefits negotiation"""
        return [
            "I'm very excited about this opportunity, and I want to make sure we start our relationship on the right foot...",
            "Based on industry standards for someone with my experience...",
            "I'm confident I can deliver significant value, and I'd love compensation that reflects that...",
            "Is there any flexibility on...?",
            "What would it take to get to [X]?",
            "I'm flexible and open to creative solutions. Could we explore...?",
            "I understand there may be constraints. Would it be possible to...?",
            "This is really important to me because..."
        ]

    def _get_common_mistakes(self) -> List[Dict[str, str]]:
        """Get common negotiation mistakes to avoid"""
        return [
            {
                "mistake": "Accepting the first offer",
                "why_bad": "Companies expect negotiation and often leave room",
                "fix": "Always negotiate - you have nothing to lose"
            },
            {
                "mistake": "Mentioning personal expenses",
                "why_bad": "Companies care about market value, not your rent",
                "fix": "Use market data and your value proposition"
            },
            {
                "mistake": "Giving a range",
                "why_bad": "They'll anchor to the bottom of your range",
                "fix": "Give a specific number based on research"
            },
            {
                "mistake": "Negotiating via email only",
                "why_bad": "Harder to build rapport and read reactions",
                "fix": "Request a call to discuss - more personal"
            },
            {
                "mistake": "Being apologetic",
                "why_bad": "Weakens your position, suggests you don't deserve it",
                "fix": "Be confident - negotiation is expected and professional"
            },
            {
                "mistake": "Revealing your current salary",
                "why_bad": "Anchors negotiation to past, not market value",
                "fix": "Deflect: 'I'm looking for market rate for this role, which is [X]'"
            },
            {
                "mistake": "Making ultimatums",
                "why_bad": "Backs both sides into a corner",
                "fix": "Stay collaborative: 'I'd love to find a solution that works for both of us'"
            },
            {
                "mistake": "Negotiating too many things at once",
                "why_bad": "Overwhelms and can seem greedy",
                "fix": "Prioritize top 2-3 items, save others for later"
            }
        ]

    def _calculate_negotiation_window(self, leverage_score: float) -> Dict[str, str]:
        """Calculate optimal negotiation window"""
        return {
            "best_time": "Between receiving offer and 5 days later",
            "latest": "Within 1 week (7 days) of offer",
            "explanation": "Companies expect you to take time to consider, but waiting too long signals disinterest",
            "your_leverage_allows": "5-7 days" if leverage_score >= 70 else "3-5 days" if leverage_score >= 50 else "2-4 days"
        }
