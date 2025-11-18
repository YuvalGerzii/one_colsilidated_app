"""
Deal Analysis Framework

Comprehensive framework for analyzing real estate investment deals.
Provides scoring, risk assessment, and investment criteria evaluation.

100% FREE - No API keys required. All calculations performed locally.
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import statistics

logger = logging.getLogger(__name__)


class DealAnalysisService:
    """Comprehensive deal analysis for real estate investments"""

    @staticmethod
    def analyze_deal(
        deal_inputs: Dict[str, float],
        property_type: str = "multifamily",
        investor_criteria: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Perform comprehensive deal analysis

        Args:
            deal_inputs: Deal parameters (purchase price, income, expenses, etc.)
            property_type: Type of property (multifamily, single_family, commercial, etc.)
            investor_criteria: Investor's minimum requirements

        Returns:
            Dict with comprehensive deal analysis
        """
        # Extract inputs
        purchase_price = deal_inputs.get("purchase_price", 0)
        annual_income = deal_inputs.get("annual_income", 0)
        annual_expenses = deal_inputs.get("annual_expenses", 0)
        down_payment_pct = deal_inputs.get("down_payment_pct", 20)
        interest_rate = deal_inputs.get("interest_rate", 6.5)
        loan_term_years = deal_inputs.get("loan_term_years", 30)
        closing_costs = deal_inputs.get("closing_costs", purchase_price * 0.03)
        rehab_costs = deal_inputs.get("rehab_costs", 0)

        # Calculate key metrics
        noi = annual_income - annual_expenses
        down_payment = purchase_price * (down_payment_pct / 100)
        loan_amount = purchase_price - down_payment
        total_cash_invested = down_payment + closing_costs + rehab_costs

        # Monthly payment calculation
        monthly_rate = interest_rate / 100 / 12
        n_payments = loan_term_years * 12
        if monthly_rate > 0:
            monthly_payment = loan_amount * (
                monthly_rate * (1 + monthly_rate) ** n_payments
            ) / ((1 + monthly_rate) ** n_payments - 1)
        else:
            monthly_payment = loan_amount / n_payments

        annual_debt_service = monthly_payment * 12

        # Key Investment Metrics
        cap_rate = (noi / purchase_price) * 100 if purchase_price > 0 else 0
        cash_on_cash = ((noi - annual_debt_service) / total_cash_invested * 100) if total_cash_invested > 0 else 0
        dscr = noi / annual_debt_service if annual_debt_service > 0 else 0

        # Calculate scores
        financial_score = DealAnalysisService._calculate_financial_score(
            cap_rate, cash_on_cash, dscr, property_type
        )

        risk_score = DealAnalysisService._calculate_risk_score(
            dscr, down_payment_pct, deal_inputs
        )

        market_score = DealAnalysisService._calculate_market_score(deal_inputs)

        # Overall deal score (weighted average)
        overall_score = (
            financial_score * 0.50 +  # Financial metrics are most important
            risk_score * 0.30 +        # Risk assessment
            market_score * 0.20        # Market factors
        )

        # Deal rating
        if overall_score >= 80:
            rating = "Excellent"
            recommendation = "Strong Buy"
            emoji = "🟢"
        elif overall_score >= 70:
            rating = "Good"
            recommendation = "Buy"
            emoji = "🟢"
        elif overall_score >= 60:
            rating = "Fair"
            recommendation = "Consider"
            emoji = "🟡"
        elif overall_score >= 50:
            rating = "Below Average"
            recommendation = "Proceed with Caution"
            emoji = "🟡"
        else:
            rating = "Poor"
            recommendation = "Pass"
            emoji = "🔴"

        # Check against investor criteria
        criteria_met = DealAnalysisService._check_investor_criteria(
            {
                "cap_rate": cap_rate,
                "cash_on_cash": cash_on_cash,
                "dscr": dscr,
                "down_payment_pct": down_payment_pct
            },
            investor_criteria or {}
        )

        return {
            "overall_score": round(overall_score, 1),
            "rating": rating,
            "recommendation": recommendation,
            "emoji": emoji,
            "scores": {
                "financial_score": round(financial_score, 1),
                "risk_score": round(risk_score, 1),
                "market_score": round(market_score, 1)
            },
            "key_metrics": {
                "cap_rate": round(cap_rate, 2),
                "cash_on_cash_return": round(cash_on_cash, 2),
                "dscr": round(dscr, 2),
                "noi": round(noi, 2),
                "annual_debt_service": round(annual_debt_service, 2),
                "total_cash_invested": round(total_cash_invested, 2)
            },
            "criteria_check": criteria_met,
            "strengths": DealAnalysisService._identify_strengths(
                cap_rate, cash_on_cash, dscr, property_type
            ),
            "weaknesses": DealAnalysisService._identify_weaknesses(
                cap_rate, cash_on_cash, dscr, property_type
            ),
            "property_type": property_type
        }

    @staticmethod
    def _calculate_financial_score(
        cap_rate: float,
        cash_on_cash: float,
        dscr: float,
        property_type: str
    ) -> float:
        """Calculate financial metrics score (0-100)"""
        score = 0

        # Cap Rate Score (0-35 points)
        if property_type == "multifamily":
            if cap_rate >= 8:
                cap_score = 35
            elif cap_rate >= 6:
                cap_score = 25
            elif cap_rate >= 5:
                cap_score = 15
            else:
                cap_score = 5
        elif property_type == "commercial":
            if cap_rate >= 9:
                cap_score = 35
            elif cap_rate >= 7:
                cap_score = 25
            elif cap_rate >= 6:
                cap_score = 15
            else:
                cap_score = 5
        else:  # single_family, etc.
            if cap_rate >= 7:
                cap_score = 35
            elif cap_rate >= 5:
                cap_score = 25
            elif cap_rate >= 4:
                cap_score = 15
            else:
                cap_score = 5

        score += cap_score

        # Cash-on-Cash Score (0-40 points)
        if cash_on_cash >= 15:
            coc_score = 40
        elif cash_on_cash >= 12:
            coc_score = 30
        elif cash_on_cash >= 10:
            coc_score = 20
        elif cash_on_cash >= 8:
            coc_score = 10
        else:
            coc_score = 0

        score += coc_score

        # DSCR Score (0-25 points)
        if dscr >= 1.5:
            dscr_score = 25
        elif dscr >= 1.3:
            dscr_score = 20
        elif dscr >= 1.2:
            dscr_score = 15
        elif dscr >= 1.1:
            dscr_score = 10
        else:
            dscr_score = 0

        score += dscr_score

        return score

    @staticmethod
    def _calculate_risk_score(
        dscr: float,
        down_payment_pct: float,
        deal_inputs: Dict[str, float]
    ) -> float:
        """Calculate risk score (0-100, higher is less risky)"""
        score = 0

        # DSCR Risk (0-40 points)
        if dscr >= 1.5:
            score += 40
        elif dscr >= 1.3:
            score += 30
        elif dscr >= 1.2:
            score += 20
        elif dscr >= 1.1:
            score += 10

        # Equity Risk (0-30 points)
        if down_payment_pct >= 30:
            score += 30
        elif down_payment_pct >= 25:
            score += 25
        elif down_payment_pct >= 20:
            score += 20
        elif down_payment_pct >= 15:
            score += 15
        elif down_payment_pct >= 10:
            score += 10

        # Vacancy Risk (0-15 points)
        vacancy_rate = deal_inputs.get("vacancy_rate", 5)
        if vacancy_rate <= 5:
            score += 15
        elif vacancy_rate <= 7:
            score += 10
        elif vacancy_rate <= 10:
            score += 5

        # Expense Ratio Risk (0-15 points)
        annual_income = deal_inputs.get("annual_income", 1)
        annual_expenses = deal_inputs.get("annual_expenses", 0)
        expense_ratio = (annual_expenses / annual_income * 100) if annual_income > 0 else 100

        if expense_ratio <= 35:
            score += 15
        elif expense_ratio <= 45:
            score += 10
        elif expense_ratio <= 55:
            score += 5

        return score

    @staticmethod
    def _calculate_market_score(deal_inputs: Dict[str, float]) -> float:
        """Calculate market factors score (0-100)"""
        score = 60  # Base score

        # Location quality (if provided)
        location_score = deal_inputs.get("location_quality", 7) # 1-10 scale
        score += (location_score - 5) * 5  # -20 to +25 points

        # Market growth (if provided)
        market_growth = deal_inputs.get("market_growth_rate", 2)  # % annual growth
        if market_growth >= 3:
            score += 15
        elif market_growth >= 2:
            score += 10
        elif market_growth >= 1:
            score += 5
        elif market_growth < 0:
            score -= 10

        # Cap to 0-100
        return max(0, min(100, score))

    @staticmethod
    def _check_investor_criteria(
        metrics: Dict[str, float],
        criteria: Dict[str, float]
    ) -> Dict[str, Any]:
        """Check if deal meets investor criteria"""
        results = {}
        all_met = True

        checks = {
            "min_cap_rate": "cap_rate",
            "min_cash_on_cash": "cash_on_cash",
            "min_dscr": "dscr",
            "max_down_payment_pct": "down_payment_pct"
        }

        for criterion_key, metric_key in checks.items():
            if criterion_key in criteria and metric_key in metrics:
                criterion_value = criteria[criterion_key]
                metric_value = metrics[metric_key]

                if "min_" in criterion_key:
                    met = metric_value >= criterion_value
                else:  # max_
                    met = metric_value <= criterion_value

                results[criterion_key] = {
                    "required": criterion_value,
                    "actual": round(metric_value, 2),
                    "met": met,
                    "emoji": "✅" if met else "❌"
                }

                if not met:
                    all_met = False

        return {
            "all_criteria_met": all_met,
            "details": results,
            "summary": f"{'✅ All criteria met' if all_met else '❌ Some criteria not met'}"
        }

    @staticmethod
    def _identify_strengths(
        cap_rate: float,
        cash_on_cash: float,
        dscr: float,
        property_type: str
    ) -> List[str]:
        """Identify deal strengths"""
        strengths = []

        # Cap rate strengths
        if property_type == "multifamily" and cap_rate >= 8:
            strengths.append(f"🎯 Excellent cap rate ({cap_rate:.1f}%) for multifamily")
        elif property_type == "commercial" and cap_rate >= 9:
            strengths.append(f"🎯 Excellent cap rate ({cap_rate:.1f}%) for commercial")
        elif cap_rate >= 7:
            strengths.append(f"🎯 Strong cap rate ({cap_rate:.1f}%)")

        # Cash-on-cash strengths
        if cash_on_cash >= 15:
            strengths.append(f"💰 Outstanding cash-on-cash return ({cash_on_cash:.1f}%)")
        elif cash_on_cash >= 12:
            strengths.append(f"💰 Excellent cash-on-cash return ({cash_on_cash:.1f}%)")

        # DSCR strengths
        if dscr >= 1.5:
            strengths.append(f"🛡️ Very healthy debt coverage ({dscr:.2f}x)")
        elif dscr >= 1.3:
            strengths.append(f"🛡️ Strong debt coverage ({dscr:.2f}x)")

        if not strengths:
            strengths.append("⚠️ Limited clear strengths identified")

        return strengths

    @staticmethod
    def _identify_weaknesses(
        cap_rate: float,
        cash_on_cash: float,
        dscr: float,
        property_type: str
    ) -> List[str]:
        """Identify deal weaknesses"""
        weaknesses = []

        # Cap rate weaknesses
        if cap_rate < 5:
            weaknesses.append(f"📉 Low cap rate ({cap_rate:.1f}%) - limited income potential")

        # Cash-on-cash weaknesses
        if cash_on_cash < 8:
            weaknesses.append(f"💸 Low cash-on-cash return ({cash_on_cash:.1f}%)")

        # DSCR weaknesses
        if dscr < 1.2:
            weaknesses.append(f"⚠️ Tight debt coverage ({dscr:.2f}x) - limited safety margin")
        elif dscr < 1.1:
            weaknesses.append(f"🚨 Very tight debt coverage ({dscr:.2f}x) - high risk")

        if not weaknesses:
            weaknesses.append("✅ No significant weaknesses identified")

        return weaknesses

    @staticmethod
    def compare_deals(
        deals: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Compare multiple deals side-by-side

        Args:
            deals: List of deal analysis results

        Returns:
            Dict with comparison analysis
        """
        if not deals:
            return {"error": "No deals to compare"}

        # Extract scores
        scores = [d.get("overall_score", 0) for d in deals]
        cap_rates = [d.get("key_metrics", {}).get("cap_rate", 0) for d in deals]
        coc_returns = [d.get("key_metrics", {}).get("cash_on_cash_return", 0) for d in deals]
        dscrs = [d.get("key_metrics", {}).get("dscr", 0) for d in deals]

        # Find best deal by overall score
        best_idx = scores.index(max(scores))
        best_deal = deals[best_idx]

        # Rankings
        score_rankings = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)

        return {
            "total_deals": len(deals),
            "best_deal": {
                "index": best_idx,
                "score": round(best_deal.get("overall_score", 0), 1),
                "rating": best_deal.get("rating", ""),
                "recommendation": best_deal.get("recommendation", "")
            },
            "statistics": {
                "average_score": round(statistics.mean(scores), 1),
                "highest_score": round(max(scores), 1),
                "lowest_score": round(min(scores), 1),
                "average_cap_rate": round(statistics.mean(cap_rates), 2),
                "average_coc": round(statistics.mean(coc_returns), 2),
                "average_dscr": round(statistics.mean(dscrs), 2)
            },
            "rankings": [
                {
                    "rank": i + 1,
                    "deal_index": score_rankings[i],
                    "score": round(scores[score_rankings[i]], 1),
                    "rating": deals[score_rankings[i]].get("rating", "")
                }
                for i in range(len(deals))
            ]
        }

    @staticmethod
    def calculate_break_even_occupancy(
        annual_income: float,
        annual_expenses: float,
        annual_debt_service: float,
        current_occupancy: float = 95
    ) -> Dict[str, Any]:
        """
        Calculate break-even occupancy rate

        Args:
            annual_income: Annual gross income at full occupancy
            annual_expenses: Annual operating expenses
            annual_debt_service: Annual debt service
            current_occupancy: Current/projected occupancy %

        Returns:
            Dict with break-even analysis
        """
        # Total annual obligations
        total_obligations = annual_expenses + annual_debt_service

        # Break-even occupancy
        break_even_occupancy = (total_obligations / annual_income * 100) if annual_income > 0 else 100

        # Safety margin
        safety_margin = current_occupancy - break_even_occupancy

        # Calculate income needed at break-even
        break_even_income = total_obligations

        # Risk assessment
        if break_even_occupancy <= 70:
            risk_level = "Low"
            emoji = "🟢"
            message = "Excellent safety margin - deal can weather significant vacancy"
        elif break_even_occupancy <= 80:
            risk_level = "Moderate"
            emoji = "🟡"
            message = "Reasonable safety margin - manageable risk"
        elif break_even_occupancy <= 90:
            risk_level = "Elevated"
            emoji = "🟠"
            message = "Limited safety margin - vulnerable to vacancy"
        else:
            risk_level = "High"
            emoji = "🔴"
            message = "Very tight margins - high risk of negative cash flow"

        return {
            "break_even_occupancy": round(break_even_occupancy, 2),
            "current_occupancy": current_occupancy,
            "safety_margin": round(safety_margin, 2),
            "break_even_income": round(break_even_income, 2),
            "risk_level": risk_level,
            "emoji": emoji,
            "interpretation": message,
            "monthly_cushion": round((current_occupancy - break_even_occupancy) / 100 * annual_income / 12, 2)
        }
