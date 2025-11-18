"""
Advanced Economic Model Calculators

Implements economic models and theories:
- Taylor Rule (optimal interest rate calculator)
- Phillips Curve analyzer (inflation-unemployment tradeoff)
- Output Gap calculator
- NAIRU estimator (Non-Accelerating Inflation Rate of Unemployment)
- Okun's Law calculator
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import statistics

from app.services.economics_db_service import EconomicsDBService
from app.services.trend_analyzer import TrendAnalyzer
from app.services.correlation_analyzer import CorrelationAnalyzer

logger = logging.getLogger(__name__)


class AdvancedEconomicModels:
    """Advanced economic models and calculators"""

    def __init__(self, db_service: EconomicsDBService):
        self.db_service = db_service
        self.trend_analyzer = TrendAnalyzer(db_service)
        self.correlation_analyzer = CorrelationAnalyzer(db_service)

    def calculate_taylor_rule(
        self,
        country: str,
        target_inflation: float = 2.0,
        equilibrium_real_rate: float = 2.0
    ) -> Dict[str, Any]:
        """
        Calculate optimal interest rate using Taylor Rule

        Taylor Rule: i = r* + π + 0.5(π - π*) + 0.5(y - y*)

        Where:
        - i = nominal federal funds rate
        - r* = equilibrium real interest rate (typically 2%)
        - π = current inflation rate
        - π* = target inflation rate (typically 2%)
        - y - y* = output gap (actual GDP - potential GDP)

        Args:
            country: Country name
            target_inflation: Target inflation rate (default 2%)
            equilibrium_real_rate: Equilibrium real rate (default 2%)

        Returns:
            Dict with Taylor Rule calculation
        """
        # Get current inflation
        price_indicators = self.db_service.get_economic_indicators(
            country=country,
            category="prices"
        )

        inflation_ind = next(
            (ind for ind in price_indicators
             if "inflation" in ind.indicator_name.lower()),
            None
        )

        if not inflation_ind or inflation_ind.last_value_numeric is None:
            return {"error": "Inflation data not available"}

        current_inflation = inflation_ind.last_value_numeric

        # Get GDP growth (proxy for output gap)
        gdp_indicators = self.db_service.get_economic_indicators(
            country=country,
            category="gdp"
        )

        gdp_growth_ind = next(
            (ind for ind in gdp_indicators
             if "growth" in ind.indicator_name.lower()),
            None
        )

        if not gdp_growth_ind or gdp_growth_ind.last_value_numeric is None:
            return {"error": "GDP growth data not available"}

        gdp_growth = gdp_growth_ind.last_value_numeric

        # Estimate output gap (simplified: actual growth - potential growth)
        # Potential growth typically around 2-3% for developed economies
        potential_growth = 2.5
        output_gap = gdp_growth - potential_growth

        # Calculate Taylor Rule rate
        inflation_gap = current_inflation - target_inflation

        # Taylor Rule: i = r* + π + 0.5(π - π*) + 0.5(y - y*)
        taylor_rate = equilibrium_real_rate + current_inflation + 0.5 * inflation_gap + 0.5 * output_gap

        # Get actual policy rate
        money_indicators = self.db_service.get_economic_indicators(
            country=country,
            category="money"
        )

        policy_rate_ind = next(
            (ind for ind in money_indicators
             if "interest rate" in ind.indicator_name.lower() or "policy rate" in ind.indicator_name.lower()),
            None
        )

        actual_policy_rate = None
        if policy_rate_ind and policy_rate_ind.last_value_numeric:
            actual_policy_rate = policy_rate_ind.last_value_numeric

        # Analysis
        if actual_policy_rate:
            rate_deviation = actual_policy_rate - taylor_rate

            if abs(rate_deviation) < 0.5:
                policy_stance = "appropriate"
                emoji = "✅"
                message = f"Policy rate ({actual_policy_rate:.2f}%) is close to Taylor Rule prescription ({taylor_rate:.2f}%)"
            elif rate_deviation > 0:
                policy_stance = "restrictive"
                emoji = "📉"
                message = f"Policy rate ({actual_policy_rate:.2f}%) is {rate_deviation:.2f}pp above Taylor Rule ({taylor_rate:.2f}%) - restrictive stance"
            else:
                policy_stance = "accommodative"
                emoji = "📈"
                message = f"Policy rate ({actual_policy_rate:.2f}%) is {abs(rate_deviation):.2f}pp below Taylor Rule ({taylor_rate:.2f}%) - accommodative stance"
        else:
            policy_stance = "unknown"
            emoji = "❓"
            message = f"Taylor Rule suggests rate of {taylor_rate:.2f}% (actual policy rate not available)"
            rate_deviation = None

        return {
            "country": country,
            "calculation_date": datetime.now().isoformat(),
            "model": "Taylor Rule",
            "inputs": {
                "current_inflation": round(current_inflation, 2),
                "target_inflation": target_inflation,
                "gdp_growth": round(gdp_growth, 2),
                "potential_growth": potential_growth,
                "output_gap": round(output_gap, 2),
                "equilibrium_real_rate": equilibrium_real_rate
            },
            "results": {
                "taylor_rule_rate": round(taylor_rate, 2),
                "actual_policy_rate": round(actual_policy_rate, 2) if actual_policy_rate else None,
                "rate_deviation": round(rate_deviation, 2) if rate_deviation else None,
                "policy_stance": policy_stance,
                "emoji": emoji
            },
            "interpretation": message,
            "recommendation": self._get_taylor_recommendation(policy_stance, rate_deviation)
        }

    def _get_taylor_recommendation(self, stance: str, deviation: Optional[float]) -> str:
        """Get recommendation from Taylor Rule analysis"""
        if stance == "appropriate":
            return "Monetary policy is appropriately calibrated to economic conditions."
        elif stance == "restrictive":
            return "Policy is more restrictive than suggested. This may slow growth but combat inflation."
        elif stance == "accommodative":
            return "Policy is more accommodative than suggested. This supports growth but may risk higher inflation."
        else:
            return "Insufficient data for policy recommendation."

    def analyze_phillips_curve(
        self,
        country: str,
        periods: int = 12
    ) -> Dict[str, Any]:
        """
        Analyze Phillips Curve relationship (unemployment vs inflation)

        Traditional Phillips Curve suggests inverse relationship:
        Lower unemployment → Higher inflation
        Higher unemployment → Lower inflation

        Args:
            country: Country name
            periods: Number of periods to analyze

        Returns:
            Dict with Phillips Curve analysis
        """
        # Get unemployment data
        labour_indicators = self.db_service.get_economic_indicators(
            country=country,
            category="labour"
        )

        unemployment_ind = next(
            (ind for ind in labour_indicators
             if "unemployment" in ind.indicator_name.lower()),
            None
        )

        # Get inflation data
        price_indicators = self.db_service.get_economic_indicators(
            country=country,
            category="prices"
        )

        inflation_ind = next(
            (ind for ind in price_indicators
             if "inflation" in ind.indicator_name.lower()),
            None
        )

        if not unemployment_ind or not inflation_ind:
            return {"error": "Missing unemployment or inflation data"}

        # Analyze correlation
        correlation_result = self.correlation_analyzer.analyze_correlation(
            country,
            unemployment_ind.indicator_name,
            inflation_ind.indicator_name,
            periods=periods
        )

        if "error" in correlation_result:
            return correlation_result

        correlation = correlation_result["correlation_coefficient"]

        # Get historical data for plotting
        unemployment_history = self.db_service.get_indicator_history(
            country=country,
            indicator_name=unemployment_ind.indicator_name,
            limit=periods
        )

        inflation_history = self.db_service.get_indicator_history(
            country=country,
            indicator_name=inflation_ind.indicator_name,
            limit=periods
        )

        # Combine data points
        data_points = []
        for u, i in zip(unemployment_history, inflation_history):
            if u.value_numeric is not None and i.value_numeric is not None:
                data_points.append({
                    "date": u.observation_date.isoformat() if u.observation_date else None,
                    "unemployment": round(u.value_numeric, 2),
                    "inflation": round(i.value_numeric, 2)
                })

        # Theory check
        expected_correlation = "negative"  # Traditional Phillips Curve
        matches_theory = correlation < -0.3

        # Interpretation
        if correlation < -0.5:
            relationship = "strong_inverse"
            message = f"Strong Phillips Curve relationship detected (r={correlation:.2f}). Lower unemployment associated with higher inflation."
        elif correlation < -0.3:
            relationship = "moderate_inverse"
            message = f"Moderate Phillips Curve relationship (r={correlation:.2f}). Traditional tradeoff present but not pronounced."
        elif correlation > 0.3:
            relationship = "positive"
            message = f"⚠️ Positive correlation (r={correlation:.2f}) contradicts traditional Phillips Curve. May indicate supply shocks or structural changes."
        else:
            relationship = "weak"
            message = f"Weak Phillips Curve relationship (r={correlation:.2f}). Tradeoff not evident in recent data."

        return {
            "country": country,
            "calculation_date": datetime.now().isoformat(),
            "model": "Phillips Curve",
            "periods_analyzed": len(data_points),
            "correlation": round(correlation, 3),
            "relationship": relationship,
            "matches_theory": matches_theory,
            "current_conditions": {
                "unemployment": data_points[0]["unemployment"] if data_points else None,
                "inflation": data_points[0]["inflation"] if data_points else None
            },
            "data_points": data_points[:6],  # Recent 6 periods
            "interpretation": message,
            "policy_implications": self._get_phillips_implications(relationship, data_points[0] if data_points else {})
        }

    def _get_phillips_implications(self, relationship: str, current: Dict) -> str:
        """Get policy implications from Phillips Curve analysis"""
        if relationship == "strong_inverse":
            if current.get("unemployment", 5) < 4:
                return "Very low unemployment may fuel inflation. Central bank may need to tighten policy."
            elif current.get("inflation", 2) > 3:
                return "High inflation with low unemployment suggests overheating. Restrictive policy appropriate."
            else:
                return "Traditional Phillips Curve tradeoff active. Policy must balance growth and inflation."

        elif relationship == "positive":
            return "⚠️ Unusual positive relationship suggests supply-side issues. Traditional demand management may be less effective."

        else:
            return "Weak Phillips Curve relationship. Other factors dominating inflation dynamics."

    def calculate_output_gap(
        self,
        country: str,
        potential_growth_rate: float = 2.5
    ) -> Dict[str, Any]:
        """
        Calculate output gap (actual GDP - potential GDP)

        Positive gap = economy above potential (inflationary pressure)
        Negative gap = economy below potential (spare capacity)

        Args:
            country: Country name
            potential_growth_rate: Estimated potential growth rate

        Returns:
            Dict with output gap calculation
        """
        # Get GDP growth
        gdp_indicators = self.db_service.get_economic_indicators(
            country=country,
            category="gdp"
        )

        gdp_growth_ind = next(
            (ind for ind in gdp_indicators
             if "growth" in ind.indicator_name.lower()),
            None
        )

        if not gdp_growth_ind or gdp_growth_ind.last_value_numeric is None:
            return {"error": "GDP growth data not available"}

        actual_growth = gdp_growth_ind.last_value_numeric

        # Calculate output gap (simplified)
        output_gap = actual_growth - potential_growth_rate

        # Get historical data for trend
        gdp_history = self.db_service.get_indicator_history(
            country=country,
            indicator_name=gdp_growth_ind.indicator_name,
            limit=12
        )

        historical_gaps = []
        for h in gdp_history:
            if h.value_numeric is not None:
                gap = h.value_numeric - potential_growth_rate
                historical_gaps.append({
                    "date": h.observation_date.isoformat() if h.observation_date else None,
                    "actual_growth": round(h.value_numeric, 2),
                    "output_gap": round(gap, 2)
                })

        # Average output gap
        if historical_gaps:
            avg_gap = statistics.mean([g["output_gap"] for g in historical_gaps])
        else:
            avg_gap = output_gap

        # Interpretation
        if output_gap > 1.5:
            status = "significant_positive"
            emoji = "🔥"
            message = f"Significant positive output gap ({output_gap:+.1f}pp). Economy overheating - inflation risk high."
        elif output_gap > 0.5:
            status = "moderate_positive"
            emoji = "📈"
            message = f"Moderate positive output gap ({output_gap:+.1f}pp). Economy above potential - some inflation pressure."
        elif output_gap > -0.5:
            status = "neutral"
            emoji = "✅"
            message = f"Output gap near zero ({output_gap:+.1f}pp). Economy operating near potential."
        elif output_gap > -1.5:
            status = "moderate_negative"
            emoji = "📉"
            message = f"Moderate negative output gap ({output_gap:+.1f}pp). Spare capacity exists - room for growth."
        else:
            status = "significant_negative"
            emoji = "⚠️"
            message = f"Significant negative output gap ({output_gap:+.1f}pp). Economy underperforming - policy stimulus may be needed."

        return {
            "country": country,
            "calculation_date": datetime.now().isoformat(),
            "model": "Output Gap",
            "inputs": {
                "actual_growth": round(actual_growth, 2),
                "potential_growth": potential_growth_rate
            },
            "results": {
                "output_gap": round(output_gap, 2),
                "average_gap_12m": round(avg_gap, 2),
                "status": status,
                "emoji": emoji
            },
            "historical_data": historical_gaps[:6],
            "interpretation": message,
            "policy_implication": self._get_output_gap_implications(status)
        }

    def _get_output_gap_implications(self, status: str) -> str:
        """Get policy implications from output gap"""
        if "positive" in status:
            return "Economy above potential - central bank should consider restrictive policy to prevent overheating."
        elif "negative" in status:
            return "Economy below potential - accommodative policy appropriate to close output gap."
        else:
            return "Economy near potential - policy can focus on maintaining balance."

    def calculate_okuns_law(
        self,
        country: str,
        periods: int = 12
    ) -> Dict[str, Any]:
        """
        Calculate Okun's Law relationship (GDP growth vs unemployment)

        Okun's Law: For every 1% increase in unemployment, GDP falls by ~2-3%
        (Empirical relationship varies by country)

        Args:
            country: Country name
            periods: Number of periods to analyze

        Returns:
            Dict with Okun's Law analysis
        """
        # Analyze correlation between GDP growth and unemployment
        gdp_indicators = self.db_service.get_economic_indicators(
            country=country,
            category="gdp"
        )

        gdp_growth_ind = next(
            (ind for ind in gdp_indicators
             if "growth" in ind.indicator_name.lower()),
            None
        )

        labour_indicators = self.db_service.get_economic_indicators(
            country=country,
            category="labour"
        )

        unemployment_ind = next(
            (ind for ind in labour_indicators
             if "unemployment" in ind.indicator_name.lower()),
            None
        )

        if not gdp_growth_ind or not unemployment_ind:
            return {"error": "Missing GDP or unemployment data"}

        # Analyze correlation
        correlation_result = self.correlation_analyzer.analyze_correlation(
            country,
            gdp_growth_ind.indicator_name,
            unemployment_ind.indicator_name,
            periods=periods
        )

        if "error" in correlation_result:
            return correlation_result

        correlation = correlation_result["correlation_coefficient"]

        # Expected: strong negative correlation
        expected_correlation = "negative"
        matches_okuns_law = correlation < -0.3

        # Get data for calculating Okun coefficient
        gdp_history = self.db_service.get_indicator_history(
            country=country,
            indicator_name=gdp_growth_ind.indicator_name,
            limit=periods
        )

        unemployment_history = self.db_service.get_indicator_history(
            country=country,
            indicator_name=unemployment_ind.indicator_name,
            limit=periods
        )

        # Calculate Okun coefficient (simplified linear relationship)
        # Change in unemployment vs change in GDP growth
        unemployment_changes = []
        gdp_changes = []

        for i in range(len(unemployment_history) - 1):
            if unemployment_history[i].value_numeric and unemployment_history[i+1].value_numeric:
                u_change = unemployment_history[i].value_numeric - unemployment_history[i+1].value_numeric
                unemployment_changes.append(u_change)

        for i in range(len(gdp_history) - 1):
            if gdp_history[i].value_numeric and gdp_history[i+1].value_numeric:
                gdp_change = gdp_history[i].value_numeric - gdp_history[i+1].value_numeric
                gdp_changes.append(gdp_change)

        # Estimate Okun coefficient (how much GDP changes per 1% unemployment change)
        if unemployment_changes and gdp_changes:
            min_len = min(len(unemployment_changes), len(gdp_changes))
            unemployment_changes = unemployment_changes[:min_len]
            gdp_changes = gdp_changes[:min_len]

            # Simple average ratio
            ratios = [gdp / u if u != 0 else 0 for gdp, u in zip(gdp_changes, unemployment_changes)]
            okun_coefficient = statistics.mean([r for r in ratios if abs(r) < 10])  # Filter outliers
        else:
            okun_coefficient = -2.0  # Theoretical default

        # Interpretation
        if correlation < -0.6:
            relationship = "strong"
            message = f"Strong Okun's Law relationship (r={correlation:.2f}). Estimated coefficient: {okun_coefficient:.2f}. For every 1% rise in unemployment, GDP falls by ~{abs(okun_coefficient):.1f}%."
        elif correlation < -0.3:
            relationship = "moderate"
            message = f"Moderate Okun's Law relationship (r={correlation:.2f}). GDP-unemployment tradeoff exists but other factors also important."
        else:
            relationship = "weak"
            message = f"Weak Okun's Law relationship (r={correlation:.2f}). GDP growth not strongly linked to unemployment changes in recent period."

        return {
            "country": country,
            "calculation_date": datetime.now().isoformat(),
            "model": "Okun's Law",
            "periods_analyzed": periods,
            "correlation": round(correlation, 3),
            "okun_coefficient": round(okun_coefficient, 2),
            "relationship_strength": relationship,
            "matches_theory": matches_okuns_law,
            "interpretation": message,
            "implication": (
                "Strong GDP-employment link means growth policies will reduce unemployment."
                if relationship == "strong"
                else "Weak link suggests structural unemployment or labor market frictions."
            )
        }
