"""
Composite Economic Indices Calculator

Calculates composite economic indices that combine multiple indicators:
- Misery Index (Unemployment + Inflation)
- Economic Freedom Index
- Business Environment Score
- Quality of Life Index
- Consumer Stress Index
- Economic Stability Index
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import statistics

from app.services.economics_db_service import EconomicsDBService

logger = logging.getLogger(__name__)


class CompositeIndicesCalculator:
    """Calculate composite economic indices"""

    def __init__(self, db_service: EconomicsDBService):
        self.db_service = db_service

    def calculate_misery_index(
        self,
        country: str
    ) -> Dict[str, Any]:
        """
        Calculate Misery Index (Unemployment Rate + Inflation Rate)

        Developed by economist Arthur Okun in the 1960s.
        Higher values indicate worse economic conditions.

        Interpretation:
        - < 5: Excellent conditions
        - 5-10: Good conditions
        - 10-15: Moderate distress
        - 15-20: High distress
        - > 20: Severe distress

        Args:
            country: Country name

        Returns:
            Dict with Misery Index calculation
        """
        # Get unemployment rate
        labour_indicators = self.db_service.get_economic_indicators(
            country=country,
            category="labour"
        )

        unemployment_ind = next(
            (ind for ind in labour_indicators
             if "unemployment rate" in ind.indicator_name.lower()),
            None
        )

        # Get inflation rate
        price_indicators = self.db_service.get_economic_indicators(
            country=country,
            category="prices"
        )

        inflation_ind = next(
            (ind for ind in price_indicators
             if "inflation" in ind.indicator_name.lower()
             or "cpi" in ind.indicator_name.lower()),
            None
        )

        if not unemployment_ind or not inflation_ind:
            return {"error": "Missing unemployment or inflation data"}

        unemployment = unemployment_ind.last_value_numeric
        inflation = inflation_ind.last_value_numeric

        if unemployment is None or inflation is None:
            return {"error": "Invalid numeric values"}

        misery_index = unemployment + inflation

        # Classification
        if misery_index < 5:
            level = "excellent"
            emoji = "🌟"
        elif misery_index < 10:
            level = "good"
            emoji = "✅"
        elif misery_index < 15:
            level = "moderate"
            emoji = "⚠️"
        elif misery_index < 20:
            level = "high_distress"
            emoji = "📉"
        else:
            level = "severe_distress"
            emoji = "🚨"

        # Historical context
        history_unemployment = self.db_service.get_indicator_history(
            country=country,
            indicator_name=unemployment_ind.indicator_name,
            limit=12
        )

        history_inflation = self.db_service.get_indicator_history(
            country=country,
            indicator_name=inflation_ind.indicator_name,
            limit=12
        )

        historical_misery = []
        if len(history_unemployment) >= 3 and len(history_inflation) >= 3:
            min_len = min(len(history_unemployment), len(history_inflation))
            for i in range(min_len):
                u = history_unemployment[i].value_numeric
                inf = history_inflation[i].value_numeric
                if u is not None and inf is not None:
                    historical_misery.append(u + inf)

        result = {
            "country": country,
            "calculation_date": datetime.now().isoformat(),
            "misery_index": round(misery_index, 2),
            "components": {
                "unemployment_rate": round(unemployment, 2),
                "inflation_rate": round(inflation, 2)
            },
            "level": level,
            "emoji": emoji,
            "interpretation": self._interpret_misery_index(misery_index, level)
        }

        if historical_misery:
            avg_historical = statistics.mean(historical_misery)
            result["historical_comparison"] = {
                "average": round(avg_historical, 2),
                "current_vs_average": round(misery_index - avg_historical, 2),
                "trend": "improving" if misery_index < avg_historical else "worsening"
            }

        return result

    def _interpret_misery_index(self, index: float, level: str) -> str:
        """Generate interpretation for Misery Index"""
        if level == "excellent":
            return (
                f"Misery Index of {index:.1f} indicates excellent economic conditions. "
                f"Both unemployment and inflation are well-controlled."
            )
        elif level == "good":
            return (
                f"Misery Index of {index:.1f} indicates good economic conditions. "
                f"The economy is performing well with manageable inflation and unemployment."
            )
        elif level == "moderate":
            return (
                f"Misery Index of {index:.1f} indicates moderate economic distress. "
                f"Either unemployment or inflation (or both) are elevated."
            )
        elif level == "high_distress":
            return (
                f"Misery Index of {index:.1f} indicates high economic distress. "
                f"Significant challenges with unemployment and/or inflation."
            )
        else:
            return (
                f"Misery Index of {index:.1f} indicates severe economic distress. "
                f"Both unemployment and inflation are at concerning levels."
            )

    def calculate_economic_stability_index(
        self,
        country: str
    ) -> Dict[str, Any]:
        """
        Calculate Economic Stability Index (0-100)

        Components:
        - Inflation stability (30%)
        - Currency stability (20%)
        - Debt sustainability (20%)
        - Employment stability (15%)
        - Budget balance (15%)

        Args:
            country: Country name

        Returns:
            Dict with stability index
        """
        scores = []
        components = {}

        # 1. Inflation Stability (30%)
        price_indicators = self.db_service.get_economic_indicators(
            country=country,
            category="prices"
        )

        inflation_ind = next(
            (ind for ind in price_indicators
             if "inflation" in ind.indicator_name.lower()),
            None
        )

        if inflation_ind and inflation_ind.last_value_numeric is not None:
            inflation = inflation_ind.last_value_numeric

            # Score based on distance from 2% target
            if 1.5 <= inflation <= 2.5:
                inflation_score = 100
            elif 1.0 <= inflation < 1.5 or 2.5 < inflation <= 3.5:
                inflation_score = 80
            elif 0.5 <= inflation < 1.0 or 3.5 < inflation <= 5.0:
                inflation_score = 60
            elif 0 <= inflation < 0.5 or 5.0 < inflation <= 7.0:
                inflation_score = 40
            else:
                inflation_score = 20

            scores.append(("inflation_stability", inflation_score, 0.30))
            components["inflation_stability"] = {
                "score": inflation_score,
                "value": inflation,
                "weight": 0.30
            }

        # 2. Debt Sustainability (20%)
        gov_indicators = self.db_service.get_economic_indicators(
            country=country,
            category="government"
        )

        debt_ind = next(
            (ind for ind in gov_indicators
             if "debt" in ind.indicator_name.lower() and "gdp" in ind.indicator_name.lower()),
            None
        )

        if debt_ind and debt_ind.last_value_numeric is not None:
            debt_to_gdp = debt_ind.last_value_numeric

            # Score based on Maastricht criteria and debt sustainability
            if debt_to_gdp < 40:
                debt_score = 100
            elif debt_to_gdp < 60:
                debt_score = 80
            elif debt_to_gdp < 80:
                debt_score = 60
            elif debt_to_gdp < 100:
                debt_score = 40
            else:
                debt_score = 20

            scores.append(("debt_sustainability", debt_score, 0.20))
            components["debt_sustainability"] = {
                "score": debt_score,
                "value": debt_to_gdp,
                "weight": 0.20
            }

        # 3. Employment Stability (15%)
        labour_indicators = self.db_service.get_economic_indicators(
            country=country,
            category="labour"
        )

        unemployment_ind = next(
            (ind for ind in labour_indicators
             if "unemployment" in ind.indicator_name.lower()),
            None
        )

        if unemployment_ind and unemployment_ind.last_value_numeric is not None:
            unemployment = unemployment_ind.last_value_numeric

            if unemployment < 4:
                employment_score = 100
            elif unemployment < 5.5:
                employment_score = 80
            elif unemployment < 7:
                employment_score = 60
            elif unemployment < 9:
                employment_score = 40
            else:
                employment_score = 20

            scores.append(("employment_stability", employment_score, 0.15))
            components["employment_stability"] = {
                "score": employment_score,
                "value": unemployment,
                "weight": 0.15
            }

        # 4. Budget Balance (15%)
        budget_ind = next(
            (ind for ind in gov_indicators
             if "budget" in ind.indicator_name.lower() or "deficit" in ind.indicator_name.lower()),
            None
        )

        if budget_ind and budget_ind.last_value_numeric is not None:
            budget = budget_ind.last_value_numeric

            # Surplus is positive, deficit is negative
            if budget > 0:
                budget_score = 100
            elif budget > -3:
                budget_score = 80
            elif budget > -5:
                budget_score = 60
            elif budget > -7:
                budget_score = 40
            else:
                budget_score = 20

            scores.append(("budget_balance", budget_score, 0.15))
            components["budget_balance"] = {
                "score": budget_score,
                "value": budget,
                "weight": 0.15
            }

        # 5. Trade Balance (20%)
        trade_indicators = self.db_service.get_economic_indicators(
            country=country,
            category="trade"
        )

        trade_balance_ind = next(
            (ind for ind in trade_indicators
             if "balance" in ind.indicator_name.lower()),
            None
        )

        if trade_balance_ind and trade_balance_ind.last_value_numeric is not None:
            trade_balance = trade_balance_ind.last_value_numeric

            # Score based on balance (surplus good, but massive deficit bad)
            if trade_balance > 0:
                trade_score = 100
            elif trade_balance > -3:
                trade_score = 80
            elif trade_balance > -5:
                trade_score = 60
            elif trade_balance > -7:
                trade_score = 40
            else:
                trade_score = 20

            scores.append(("trade_balance", trade_score, 0.20))
            components["trade_balance"] = {
                "score": trade_score,
                "value": trade_balance,
                "weight": 0.20
            }

        # Calculate overall stability index
        if scores:
            total_score = sum(score * weight for _, score, weight in scores)
            total_weight = sum(weight for _, _, weight in scores)
            stability_index = (total_score / total_weight) if total_weight > 0 else 50
        else:
            stability_index = 50

        # Classification
        if stability_index >= 80:
            stability_level = "very_stable"
            emoji = "🌟"
        elif stability_index >= 65:
            stability_level = "stable"
            emoji = "✅"
        elif stability_index >= 50:
            stability_level = "moderate"
            emoji = "⚠️"
        elif stability_index >= 35:
            stability_level = "unstable"
            emoji = "📉"
        else:
            stability_level = "very_unstable"
            emoji = "🚨"

        return {
            "country": country,
            "calculation_date": datetime.now().isoformat(),
            "stability_index": round(stability_index, 1),
            "level": stability_level,
            "emoji": emoji,
            "components": components,
            "interpretation": self._interpret_stability(stability_index, stability_level)
        }

    def _interpret_stability(self, index: float, level: str) -> str:
        """Generate interpretation for stability index"""
        if level == "very_stable":
            return (
                f"Stability Index of {index:.1f}/100 indicates very stable economic conditions. "
                f"Low risk environment for investment and business."
            )
        elif level == "stable":
            return (
                f"Stability Index of {index:.1f}/100 indicates stable economic conditions. "
                f"Manageable risks with generally favorable conditions."
            )
        elif level == "moderate":
            return (
                f"Stability Index of {index:.1f}/100 indicates moderate stability. "
                f"Some economic imbalances present requiring monitoring."
            )
        elif level == "unstable":
            return (
                f"Stability Index of {index:.1f}/100 indicates unstable conditions. "
                f"Significant economic imbalances and elevated risks."
            )
        else:
            return (
                f"Stability Index of {index:.1f}/100 indicates very unstable conditions. "
                f"High risk environment with severe economic imbalances."
            )

    def calculate_consumer_stress_index(
        self,
        country: str
    ) -> Dict[str, Any]:
        """
        Calculate Consumer Stress Index

        Measures financial pressure on consumers through:
        - Unemployment rate (40%)
        - Inflation rate (30%)
        - Consumer debt levels (20%)
        - Wage growth vs inflation (10%)

        Higher = more stress

        Args:
            country: Country name

        Returns:
            Dict with consumer stress index
        """
        stress_components = []

        # Get indicators
        labour_indicators = self.db_service.get_economic_indicators(country=country, category="labour")
        price_indicators = self.db_service.get_economic_indicators(country=country, category="prices")
        consumer_indicators = self.db_service.get_economic_indicators(country=country, category="consumer")

        # 1. Unemployment contribution (40%)
        unemployment_ind = next(
            (ind for ind in labour_indicators if "unemployment" in ind.indicator_name.lower()),
            None
        )

        if unemployment_ind and unemployment_ind.last_value_numeric:
            unemployment = unemployment_ind.last_value_numeric
            # Higher unemployment = higher stress
            unemployment_stress = min(unemployment * 10, 100)  # Scale to 0-100
            stress_components.append(("unemployment", unemployment_stress, 0.40, unemployment))

        # 2. Inflation contribution (30%)
        inflation_ind = next(
            (ind for ind in price_indicators if "inflation" in ind.indicator_name.lower()),
            None
        )

        if inflation_ind and inflation_ind.last_value_numeric:
            inflation = inflation_ind.last_value_numeric
            # Optimal at 2%, stress increases as we move away
            inflation_stress = abs(inflation - 2) * 15
            inflation_stress = min(inflation_stress, 100)
            stress_components.append(("inflation", inflation_stress, 0.30, inflation))

        # 3. Consumer debt (20%)
        debt_ind = next(
            (ind for ind in consumer_indicators if "debt" in ind.indicator_name.lower()),
            None
        )

        if debt_ind and debt_ind.last_value_numeric:
            debt = debt_ind.last_value_numeric
            # Higher debt = higher stress
            debt_stress = min((debt / 100) * 100, 100)
            stress_components.append(("consumer_debt", debt_stress, 0.20, debt))

        # 4. Wage growth (10%)
        wage_ind = next(
            (ind for ind in labour_indicators if "wage" in ind.indicator_name.lower()),
            None
        )

        if wage_ind and wage_ind.last_value_numeric and inflation_ind:
            wage_growth = wage_ind.last_value_numeric
            inflation_rate = inflation_ind.last_value_numeric

            # If wage growth < inflation, stress is high
            real_wage_growth = wage_growth - inflation_rate
            if real_wage_growth < 0:
                wage_stress = abs(real_wage_growth) * 20
            else:
                wage_stress = max(0, (2 - real_wage_growth) * 10)

            wage_stress = min(wage_stress, 100)
            stress_components.append(("real_wage_growth", wage_stress, 0.10, real_wage_growth))

        # Calculate overall stress
        if stress_components:
            total_stress = sum(stress * weight for _, stress, weight, _ in stress_components)
            total_weight = sum(weight for _, _, weight, _ in stress_components)
            stress_index = (total_stress / total_weight) if total_weight > 0 else 50
        else:
            stress_index = 50

        # Classification
        if stress_index < 20:
            stress_level = "low"
            emoji = "✅"
        elif stress_index < 40:
            stress_level = "moderate"
            emoji = "⚠️"
        elif stress_index < 60:
            stress_level = "elevated"
            emoji = "📊"
        elif stress_index < 80:
            stress_level = "high"
            emoji = "📉"
        else:
            stress_level = "severe"
            emoji = "🚨"

        return {
            "country": country,
            "calculation_date": datetime.now().isoformat(),
            "consumer_stress_index": round(stress_index, 1),
            "level": stress_level,
            "emoji": emoji,
            "components": {
                name: {
                    "stress_contribution": round(stress, 1),
                    "weight": weight,
                    "actual_value": round(value, 2)
                }
                for name, stress, weight, value in stress_components
            },
            "interpretation": (
                f"Consumer Stress Index of {stress_index:.1f}/100 indicates {stress_level} "
                f"financial pressure on households. "
                f"{'✅ Consumers are generally comfortable.' if stress_index < 40 else ''}"
                f"{'⚠️ Consumers facing moderate financial pressure.' if 40 <= stress_index < 60 else ''}"
                f"{'📉 Consumers under significant financial stress.' if stress_index >= 60 else ''}"
            )
        }

    def calculate_all_indices(self, country: str) -> Dict[str, Any]:
        """
        Calculate all composite indices for a country

        Args:
            country: Country name

        Returns:
            Dict with all indices
        """
        return {
            "country": country,
            "calculation_date": datetime.now().isoformat(),
            "misery_index": self.calculate_misery_index(country),
            "stability_index": self.calculate_economic_stability_index(country),
            "consumer_stress_index": self.calculate_consumer_stress_index(country)
        }
