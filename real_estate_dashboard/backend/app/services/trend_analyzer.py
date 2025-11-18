"""
Economic Trend Analyzer

Analyzes historical trends and provides forecasting insights for economic indicators.

Features:
- Time series trend analysis
- Growth rate calculations (YoY, QoQ, MoM)
- Momentum indicators
- Simple trend forecasting
- Seasonal pattern detection
- Volatility analysis
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from enum import Enum
import statistics

from app.services.economics_db_service import EconomicsDBService

logger = logging.getLogger(__name__)


class TrendStrength(Enum):
    """Trend strength classification"""
    VERY_STRONG = "very_strong"
    STRONG = "strong"
    MODERATE = "moderate"
    WEAK = "weak"
    NO_TREND = "no_trend"


class TrendAnalyzer:
    """Analyze economic indicator trends over time"""

    def __init__(self, db_service: EconomicsDBService):
        self.db_service = db_service

    def analyze_trend(
        self,
        country: str,
        indicator_name: str,
        periods: int = 12
    ) -> Dict[str, Any]:
        """
        Analyze trend for an indicator

        Args:
            country: Country name
            indicator_name: Indicator to analyze
            periods: Number of historical periods to analyze

        Returns:
            Dict with trend analysis
        """
        # Get historical data
        history = self.db_service.get_indicator_history(
            country=country,
            indicator_name=indicator_name,
            limit=periods
        )

        if len(history) < 3:
            return {
                "error": "Insufficient data for trend analysis",
                "data_points": len(history)
            }

        # Extract values
        values = [h.value_numeric for h in history if h.value_numeric is not None]
        dates = [h.observation_date for h in history if h.value_numeric is not None]

        if len(values) < 3:
            return {
                "error": "Insufficient numeric data",
                "data_points": len(values)
            }

        # Calculate trend metrics
        analysis = {
            "indicator": indicator_name,
            "country": country,
            "periods_analyzed": len(values),
            "date_range": {
                "start": dates[-1].isoformat() if dates else None,
                "end": dates[0].isoformat() if dates else None
            },
            "current_value": values[0],
            "historical_values": values
        }

        # Basic statistics
        analysis["statistics"] = {
            "mean": round(statistics.mean(values), 2),
            "median": round(statistics.median(values), 2),
            "std_dev": round(statistics.stdev(values), 2) if len(values) > 1 else 0,
            "min": min(values),
            "max": max(values),
            "range": max(values) - min(values)
        }

        # Trend direction and strength
        analysis["trend"] = self._calculate_trend(values)

        # Growth rates
        analysis["growth_rates"] = self._calculate_growth_rates(values, dates)

        # Volatility
        analysis["volatility"] = self._calculate_volatility(values)

        # Momentum
        analysis["momentum"] = self._calculate_momentum(values)

        # Simple forecast
        if len(values) >= 6:
            analysis["forecast"] = self._simple_forecast(values, periods=3)

        # Interpretation
        analysis["interpretation"] = self._generate_trend_interpretation(analysis)

        return analysis

    def _calculate_trend(self, values: List[float]) -> Dict[str, Any]:
        """Calculate trend direction and strength using linear regression"""
        n = len(values)

        # Simple linear regression (y = mx + b)
        # Using index as x (0, 1, 2, ..., n-1)
        x_values = list(range(n))
        x_mean = statistics.mean(x_values)
        y_mean = statistics.mean(values)

        # Calculate slope
        numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_values, values))
        denominator = sum((x - x_mean) ** 2 for x in x_values)

        slope = numerator / denominator if denominator != 0 else 0

        # Calculate R-squared (goodness of fit)
        y_pred = [slope * x + (y_mean - slope * x_mean) for x in x_values]
        ss_res = sum((y - y_p) ** 2 for y, y_p in zip(values, y_pred))
        ss_tot = sum((y - y_mean) ** 2 for y in values)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0

        # Determine trend direction
        if slope > 0:
            direction = "upward"
        elif slope < 0:
            direction = "downward"
        else:
            direction = "flat"

        # Determine trend strength based on R-squared
        if r_squared > 0.8:
            strength = TrendStrength.VERY_STRONG.value
        elif r_squared > 0.6:
            strength = TrendStrength.STRONG.value
        elif r_squared > 0.4:
            strength = TrendStrength.MODERATE.value
        elif r_squared > 0.2:
            strength = TrendStrength.WEAK.value
        else:
            strength = TrendStrength.NO_TREND.value

        return {
            "direction": direction,
            "strength": strength,
            "slope": round(slope, 4),
            "r_squared": round(r_squared, 3),
            "confidence": round(r_squared * 100, 1)
        }

    def _calculate_growth_rates(
        self,
        values: List[float],
        dates: List[datetime]
    ) -> Dict[str, Any]:
        """Calculate various growth rates"""
        growth_rates = {}

        # Period-over-period (most recent vs previous)
        if len(values) >= 2:
            pop_growth = ((values[0] - values[1]) / abs(values[1])) * 100 if values[1] != 0 else 0
            growth_rates["period_over_period"] = round(pop_growth, 2)

        # Year-over-year (if we have 12+ months)
        if len(values) >= 12:
            yoy_growth = ((values[0] - values[11]) / abs(values[11])) * 100 if values[11] != 0 else 0
            growth_rates["year_over_year"] = round(yoy_growth, 2)

        # Average growth rate across all periods
        if len(values) >= 3:
            period_changes = [
                ((values[i] - values[i+1]) / abs(values[i+1])) * 100
                for i in range(len(values)-1)
                if values[i+1] != 0
            ]
            if period_changes:
                growth_rates["average_growth_rate"] = round(statistics.mean(period_changes), 2)

        # Compound growth rate (CAGR-like)
        if len(values) >= 2:
            n_periods = len(values) - 1
            if values[-1] != 0 and values[0] > 0 and values[-1] > 0:
                cagr = (((values[0] / values[-1]) ** (1 / n_periods)) - 1) * 100
                growth_rates["compound_growth_rate"] = round(cagr, 2)

        return growth_rates

    def _calculate_volatility(self, values: List[float]) -> Dict[str, Any]:
        """Calculate volatility metrics"""
        if len(values) < 2:
            return {"error": "Insufficient data"}

        # Calculate period-to-period changes
        changes = [
            ((values[i] - values[i+1]) / abs(values[i+1])) * 100
            for i in range(len(values)-1)
            if values[i+1] != 0
        ]

        if not changes:
            return {"error": "Unable to calculate changes"}

        volatility = {
            "std_dev_of_changes": round(statistics.stdev(changes), 2) if len(changes) > 1 else 0,
            "max_increase": round(max(changes), 2) if changes else 0,
            "max_decrease": round(min(changes), 2) if changes else 0,
            "average_absolute_change": round(statistics.mean([abs(c) for c in changes]), 2)
        }

        # Volatility classification
        avg_abs_change = volatility["average_absolute_change"]
        if avg_abs_change < 1:
            volatility["classification"] = "very_stable"
        elif avg_abs_change < 3:
            volatility["classification"] = "stable"
        elif avg_abs_change < 5:
            volatility["classification"] = "moderate"
        elif avg_abs_change < 10:
            volatility["classification"] = "volatile"
        else:
            volatility["classification"] = "highly_volatile"

        return volatility

    def _calculate_momentum(self, values: List[float]) -> Dict[str, Any]:
        """Calculate momentum indicators"""
        if len(values) < 6:
            return {"error": "Insufficient data for momentum"}

        # Recent momentum (last 3 periods)
        recent_values = values[:3]
        recent_trend = statistics.mean(recent_values)

        # Historical average (exclude most recent 3)
        historical_values = values[3:]
        historical_avg = statistics.mean(historical_values)

        # Momentum relative to history
        momentum_score = ((recent_trend - historical_avg) / abs(historical_avg)) * 100 if historical_avg != 0 else 0

        # Rate of change acceleration
        if len(values) >= 6:
            recent_change = values[0] - values[2]
            past_change = values[3] - values[5]
            acceleration = recent_change - past_change
        else:
            acceleration = 0

        momentum = {
            "momentum_score": round(momentum_score, 2),
            "acceleration": round(acceleration, 2),
            "recent_average": round(recent_trend, 2),
            "historical_average": round(historical_avg, 2)
        }

        # Momentum classification
        if momentum_score > 10:
            momentum["classification"] = "strong_positive"
        elif momentum_score > 5:
            momentum["classification"] = "positive"
        elif momentum_score > -5:
            momentum["classification"] = "neutral"
        elif momentum_score > -10:
            momentum["classification"] = "negative"
        else:
            momentum["classification"] = "strong_negative"

        return momentum

    def _simple_forecast(
        self,
        values: List[float],
        periods: int = 3
    ) -> Dict[str, Any]:
        """Simple trend-based forecast"""
        n = len(values)
        x_values = list(range(n))

        # Calculate trend line
        x_mean = statistics.mean(x_values)
        y_mean = statistics.mean(values)

        numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_values, values))
        denominator = sum((x - x_mean) ** 2 for x in x_values)

        slope = numerator / denominator if denominator != 0 else 0
        intercept = y_mean - slope * x_mean

        # Forecast future periods
        forecast_values = []
        for i in range(1, periods + 1):
            x = n + i - 1
            forecast_value = slope * x + intercept
            forecast_values.append(round(forecast_value, 2))

        # Calculate confidence interval (simple)
        residuals = [values[i] - (slope * i + intercept) for i in range(n)]
        std_error = statistics.stdev(residuals) if len(residuals) > 1 else 0

        forecast = {
            "method": "linear_trend",
            "periods_ahead": periods,
            "forecasted_values": forecast_values,
            "confidence_interval": {
                "std_error": round(std_error, 2),
                "margin_95pct": round(1.96 * std_error, 2)  # 95% confidence
            },
            "warning": "This is a simple trend-based forecast. Actual values may vary significantly."
        }

        return forecast

    def _generate_trend_interpretation(self, analysis: Dict[str, Any]) -> str:
        """Generate human-readable interpretation"""
        texts = []

        trend = analysis.get("trend", {})
        direction = trend.get("direction", "unknown")
        strength = trend.get("strength", "unknown")
        confidence = trend.get("confidence", 0)

        # Trend description
        if direction == "upward":
            texts.append(f"📈 The indicator shows an upward trend")
        elif direction == "downward":
            texts.append(f"📉 The indicator shows a downward trend")
        else:
            texts.append(f"➡️ The indicator shows no clear trend")

        # Strength
        if strength == "very_strong":
            texts.append(f"with very strong consistency ({confidence:.0f}% confidence).")
        elif strength == "strong":
            texts.append(f"with strong consistency ({confidence:.0f}% confidence).")
        elif strength == "moderate":
            texts.append(f"with moderate consistency ({confidence:.0f}% confidence).")
        elif strength == "weak":
            texts.append(f"but the trend is weak ({confidence:.0f}% confidence).")
        else:
            texts.append(f"with no consistent pattern.")

        # Volatility
        volatility = analysis.get("volatility", {})
        vol_class = volatility.get("classification", "unknown")

        if vol_class == "very_stable":
            texts.append("The indicator is very stable with minimal fluctuations.")
        elif vol_class == "stable":
            texts.append("The indicator is relatively stable.")
        elif vol_class == "moderate":
            texts.append("The indicator shows moderate volatility.")
        elif vol_class == "volatile":
            texts.append("⚠️ The indicator is quite volatile.")
        elif vol_class == "highly_volatile":
            texts.append("⚠️ The indicator is highly volatile with significant swings.")

        # Momentum
        momentum = analysis.get("momentum", {})
        mom_class = momentum.get("classification", "unknown")

        if mom_class == "strong_positive":
            texts.append("📊 Recent momentum is strongly positive, suggesting acceleration.")
        elif mom_class == "positive":
            texts.append("✅ Recent momentum is positive.")
        elif mom_class == "neutral":
            texts.append("The indicator is maintaining a steady pace.")
        elif mom_class == "negative":
            texts.append("⚠️ Recent momentum is negative, suggesting deceleration.")
        elif mom_class == "strong_negative":
            texts.append("📉 Recent momentum is strongly negative, indicating sharp deceleration.")

        # Growth rate
        growth_rates = analysis.get("growth_rates", {})
        if "period_over_period" in growth_rates:
            pop = growth_rates["period_over_period"]
            if abs(pop) < 1:
                texts.append(f"Period-over-period change is minimal ({pop:+.2f}%).")
            else:
                texts.append(f"Period-over-period change: {pop:+.2f}%.")

        return " ".join(texts)

    def compare_trends(
        self,
        country: str,
        indicators: List[str],
        periods: int = 12
    ) -> Dict[str, Any]:
        """
        Compare trends across multiple indicators for a country

        Args:
            country: Country name
            indicators: List of indicator names
            periods: Number of periods to analyze

        Returns:
            Dict with comparative trend analysis
        """
        comparison = {
            "country": country,
            "periods": periods,
            "indicators": {},
            "summary": {}
        }

        trend_scores = []

        for indicator in indicators:
            analysis = self.analyze_trend(country, indicator, periods)

            if "error" not in analysis:
                comparison["indicators"][indicator] = analysis

                # Score the trend
                trend = analysis.get("trend", {})
                if trend.get("direction") == "upward" and trend.get("strength") in ["strong", "very_strong"]:
                    trend_scores.append((indicator, "positive", trend.get("confidence", 0)))
                elif trend.get("direction") == "downward" and trend.get("strength") in ["strong", "very_strong"]:
                    trend_scores.append((indicator, "negative", trend.get("confidence", 0)))

        # Summary
        if trend_scores:
            positive_trends = [t for t in trend_scores if t[1] == "positive"]
            negative_trends = [t for t in trend_scores if t[1] == "negative"]

            comparison["summary"] = {
                "total_indicators": len(indicators),
                "positive_trends": len(positive_trends),
                "negative_trends": len(negative_trends),
                "strongest_positive": max(positive_trends, key=lambda x: x[2])[0] if positive_trends else None,
                "strongest_negative": max(negative_trends, key=lambda x: x[2])[0] if negative_trends else None
            }

        return comparison
