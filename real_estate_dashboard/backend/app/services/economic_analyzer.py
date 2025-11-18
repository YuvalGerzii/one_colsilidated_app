"""
Economic Indicators Analyzer

Provides comprehensive analysis of economic indicators including:
- Indicator classification (leading, lagging, coincident)
- Trend analysis and growth rate calculations
- Economic health assessment
- Signal interpretation and insights

Based on established economic theory and analysis methods.
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from enum import Enum
import statistics

from app.services.economics_db_service import EconomicsDBService
from app.models.economics import EconomicIndicator, EconomicIndicatorHistory

logger = logging.getLogger(__name__)


class IndicatorType(Enum):
    """Economic indicator classification"""
    LEADING = "leading"        # Predicts future economic activity (6-12 months ahead)
    COINCIDENT = "coincident"  # Moves with current economic conditions
    LAGGING = "lagging"        # Confirms trends after economic changes


class TrendDirection(Enum):
    """Trend direction classification"""
    STRONG_UP = "strong_upward"      # > 5% growth
    MODERATE_UP = "moderate_upward"  # 2-5% growth
    STABLE = "stable"                # -2% to 2%
    MODERATE_DOWN = "moderate_downward"  # -5% to -2%
    STRONG_DOWN = "strong_downward"      # < -5%


class EconomicSignal(Enum):
    """Economic signal interpretation"""
    VERY_POSITIVE = "very_positive"
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    VERY_NEGATIVE = "very_negative"


class EconomicAnalyzer:
    """Analyzes economic indicators for insights and interpretations"""

    # Indicator classification based on economic theory
    INDICATOR_CLASSIFICATIONS = {
        # LEADING INDICATORS (predict future 6-12 months)
        "Building Permits": IndicatorType.LEADING,
        "Housing Starts": IndicatorType.LEADING,
        "New Home Sales": IndicatorType.LEADING,
        "Consumer Confidence": IndicatorType.LEADING,
        "Business Confidence": IndicatorType.LEADING,
        "Stock Market Index": IndicatorType.LEADING,
        "Manufacturer New Orders": IndicatorType.LEADING,
        "PMI": IndicatorType.LEADING,
        "Average Weekly Hours": IndicatorType.LEADING,
        "Initial Jobless Claims": IndicatorType.LEADING,

        # COINCIDENT INDICATORS (reflect current state)
        "GDP Growth Rate": IndicatorType.COINCIDENT,
        "GDP": IndicatorType.COINCIDENT,
        "Industrial Production": IndicatorType.COINCIDENT,
        "Personal Income": IndicatorType.COINCIDENT,
        "Retail Sales": IndicatorType.COINCIDENT,
        "Manufacturing Sales": IndicatorType.COINCIDENT,
        "Wages": IndicatorType.COINCIDENT,

        # LAGGING INDICATORS (confirm trends)
        "Unemployment Rate": IndicatorType.LAGGING,
        "Inflation Rate": IndicatorType.LAGGING,
        "CPI": IndicatorType.LAGGING,
        "Average House Price": IndicatorType.LAGGING,
        "Existing Home Sales": IndicatorType.LAGGING,
        "Consumer Debt": IndicatorType.LAGGING,
        "Government Debt": IndicatorType.LAGGING,
        "Prime Rate": IndicatorType.LAGGING,
        "Corporate Profits": IndicatorType.LAGGING,
    }

    # Optimal ranges for key indicators (general guidelines)
    OPTIMAL_RANGES = {
        "GDP Growth Rate": (2.0, 3.5, "%"),           # Healthy: 2-3.5%
        "Unemployment Rate": (3.5, 5.0, "%"),         # Healthy: 3.5-5%
        "Inflation Rate": (1.5, 2.5, "%"),            # Target: ~2%
        "Government Debt to GDP": (0, 60, "%"),       # Maastricht: <60%
        "Consumer Confidence": (90, 110, "points"),   # Above 100 is positive
        "PMI": (50, 60, "points"),                    # >50 = expansion
    }

    def __init__(self, db_service: EconomicsDBService):
        self.db_service = db_service

    def classify_indicator(self, indicator_name: str) -> IndicatorType:
        """
        Classify indicator as leading, coincident, or lagging

        Args:
            indicator_name: Name of the indicator

        Returns:
            IndicatorType classification
        """
        # Check exact match
        if indicator_name in self.INDICATOR_CLASSIFICATIONS:
            return self.INDICATOR_CLASSIFICATIONS[indicator_name]

        # Check partial matches
        indicator_lower = indicator_name.lower()

        # Leading indicators (predictive)
        if any(word in indicator_lower for word in [
            "permit", "start", "new", "order", "confidence", "pmi",
            "leading", "initial", "claim"
        ]):
            return IndicatorType.LEADING

        # Lagging indicators (confirmatory)
        if any(word in indicator_lower for word in [
            "unemployment", "inflation", "cpi", "debt", "existing",
            "lagging", "prime rate", "profit"
        ]):
            return IndicatorType.LAGGING

        # Default to coincident
        return IndicatorType.COINCIDENT

    def calculate_growth_rate(
        self,
        current_value: float,
        previous_value: float
    ) -> Optional[float]:
        """
        Calculate percentage growth rate

        Args:
            current_value: Current period value
            previous_value: Previous period value

        Returns:
            Growth rate as percentage
        """
        if previous_value == 0 or previous_value is None:
            return None

        return ((current_value - previous_value) / abs(previous_value)) * 100

    def classify_trend(self, growth_rate: float) -> TrendDirection:
        """
        Classify trend direction based on growth rate

        Args:
            growth_rate: Percentage growth rate

        Returns:
            TrendDirection classification
        """
        if growth_rate > 5:
            return TrendDirection.STRONG_UP
        elif growth_rate > 2:
            return TrendDirection.MODERATE_UP
        elif growth_rate > -2:
            return TrendDirection.STABLE
        elif growth_rate > -5:
            return TrendDirection.MODERATE_DOWN
        else:
            return TrendDirection.STRONG_DOWN

    def interpret_indicator(
        self,
        indicator_name: str,
        current_value: float,
        previous_value: Optional[float] = None,
        historical_avg: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Interpret an economic indicator

        Args:
            indicator_name: Name of the indicator
            current_value: Current value
            previous_value: Previous period value
            historical_avg: Historical average

        Returns:
            Dict with interpretation details
        """
        classification = self.classify_indicator(indicator_name)
        interpretation = {
            "indicator": indicator_name,
            "current_value": current_value,
            "classification": classification.value,
            "time_horizon": self._get_time_horizon(classification),
        }

        # Calculate growth if previous value available
        if previous_value is not None:
            growth_rate = self.calculate_growth_rate(current_value, previous_value)
            if growth_rate is not None:
                interpretation["growth_rate"] = round(growth_rate, 2)
                interpretation["trend"] = self.classify_trend(growth_rate).value

        # Compare to optimal range if available
        if indicator_name in self.OPTIMAL_RANGES:
            min_val, max_val, unit = self.OPTIMAL_RANGES[indicator_name]
            interpretation["optimal_range"] = {
                "min": min_val,
                "max": max_val,
                "unit": unit
            }
            interpretation["in_optimal_range"] = min_val <= current_value <= max_val

        # Compare to historical average
        if historical_avg is not None:
            deviation = ((current_value - historical_avg) / abs(historical_avg)) * 100
            interpretation["vs_historical_avg"] = round(deviation, 2)

        # Generate signal
        interpretation["signal"] = self._generate_signal(
            indicator_name,
            current_value,
            growth_rate if previous_value else None
        )

        # Add interpretation text
        interpretation["interpretation"] = self._generate_interpretation_text(
            indicator_name,
            classification,
            interpretation
        )

        return interpretation

    def _get_time_horizon(self, classification: IndicatorType) -> str:
        """Get time horizon description for indicator type"""
        if classification == IndicatorType.LEADING:
            return "Predicts 6-12 months ahead"
        elif classification == IndicatorType.COINCIDENT:
            return "Reflects current conditions"
        else:  # LAGGING
            return "Confirms past trends"

    def _generate_signal(
        self,
        indicator_name: str,
        current_value: float,
        growth_rate: Optional[float]
    ) -> str:
        """Generate economic signal from indicator"""
        indicator_lower = indicator_name.lower()

        # GDP Growth Rate signals
        if "gdp growth" in indicator_lower or "gdp annual" in indicator_lower:
            if current_value > 3.5:
                return EconomicSignal.VERY_POSITIVE.value
            elif current_value > 2:
                return EconomicSignal.POSITIVE.value
            elif current_value > 0:
                return EconomicSignal.NEUTRAL.value
            elif current_value > -2:
                return EconomicSignal.NEGATIVE.value
            else:
                return EconomicSignal.VERY_NEGATIVE.value

        # Unemployment signals (lower is better)
        elif "unemployment" in indicator_lower:
            if current_value < 4:
                return EconomicSignal.VERY_POSITIVE.value
            elif current_value < 5:
                return EconomicSignal.POSITIVE.value
            elif current_value < 6:
                return EconomicSignal.NEUTRAL.value
            elif current_value < 8:
                return EconomicSignal.NEGATIVE.value
            else:
                return EconomicSignal.VERY_NEGATIVE.value

        # Inflation signals (target ~2%)
        elif "inflation" in indicator_lower or "cpi" in indicator_lower:
            if 1.5 <= current_value <= 2.5:
                return EconomicSignal.VERY_POSITIVE.value
            elif 1 <= current_value < 1.5 or 2.5 < current_value <= 3.5:
                return EconomicSignal.POSITIVE.value
            elif 0 <= current_value < 1 or 3.5 < current_value <= 5:
                return EconomicSignal.NEUTRAL.value
            elif current_value > 5:
                return EconomicSignal.NEGATIVE.value
            else:  # Deflation
                return EconomicSignal.VERY_NEGATIVE.value

        # Consumer/Business Confidence (100 = neutral)
        elif "confidence" in indicator_lower:
            if current_value > 110:
                return EconomicSignal.VERY_POSITIVE.value
            elif current_value > 100:
                return EconomicSignal.POSITIVE.value
            elif current_value > 90:
                return EconomicSignal.NEUTRAL.value
            elif current_value > 80:
                return EconomicSignal.NEGATIVE.value
            else:
                return EconomicSignal.VERY_NEGATIVE.value

        # PMI (50 = expansion/contraction threshold)
        elif "pmi" in indicator_lower:
            if current_value > 55:
                return EconomicSignal.VERY_POSITIVE.value
            elif current_value > 50:
                return EconomicSignal.POSITIVE.value
            elif current_value > 45:
                return EconomicSignal.NEUTRAL.value
            elif current_value > 40:
                return EconomicSignal.NEGATIVE.value
            else:
                return EconomicSignal.VERY_NEGATIVE.value

        # Growth-based signals (for other indicators)
        elif growth_rate is not None:
            if growth_rate > 5:
                return EconomicSignal.VERY_POSITIVE.value
            elif growth_rate > 2:
                return EconomicSignal.POSITIVE.value
            elif growth_rate > -2:
                return EconomicSignal.NEUTRAL.value
            elif growth_rate > -5:
                return EconomicSignal.NEGATIVE.value
            else:
                return EconomicSignal.VERY_NEGATIVE.value

        return EconomicSignal.NEUTRAL.value

    def _generate_interpretation_text(
        self,
        indicator_name: str,
        classification: IndicatorType,
        interpretation: Dict[str, Any]
    ) -> str:
        """Generate human-readable interpretation text"""
        texts = []

        # Classification context
        if classification == IndicatorType.LEADING:
            texts.append(f"{indicator_name} is a leading indicator that helps predict economic activity 6-12 months ahead.")
        elif classification == IndicatorType.COINCIDENT:
            texts.append(f"{indicator_name} is a coincident indicator that reflects current economic conditions.")
        else:
            texts.append(f"{indicator_name} is a lagging indicator that confirms economic trends after they occur.")

        # Trend analysis
        if "growth_rate" in interpretation:
            growth = interpretation["growth_rate"]
            trend = interpretation.get("trend", "stable")

            if abs(growth) < 2:
                texts.append(f"The indicator is stable with minimal change ({growth:+.2f}%).")
            elif growth > 0:
                texts.append(f"The indicator is trending upward with {growth:.2f}% growth.")
            else:
                texts.append(f"The indicator is trending downward with {growth:.2f}% decline.")

        # Optimal range check
        if "in_optimal_range" in interpretation:
            if interpretation["in_optimal_range"]:
                texts.append("The current value is within the optimal range.")
            else:
                optimal = interpretation["optimal_range"]
                texts.append(f"The current value is outside the optimal range of {optimal['min']}-{optimal['max']}{optimal['unit']}.")

        # Signal interpretation
        signal = interpretation.get("signal", "neutral")
        if signal == "very_positive":
            texts.append("📈 This indicates very positive economic conditions.")
        elif signal == "positive":
            texts.append("✅ This indicates positive economic conditions.")
        elif signal == "neutral":
            texts.append("➡️ This indicates neutral economic conditions.")
        elif signal == "negative":
            texts.append("⚠️ This indicates negative economic conditions.")
        elif signal == "very_negative":
            texts.append("📉 This indicates very negative economic conditions.")

        return " ".join(texts)

    def analyze_country(
        self,
        country: str,
        categories: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Comprehensive analysis of a country's economic indicators

        Args:
            country: Country name
            categories: List of categories to analyze (None = all)

        Returns:
            Dict with comprehensive analysis
        """
        if categories is None:
            categories = ["overview", "gdp", "labour", "prices", "housing",
                         "money", "trade", "government", "business", "consumer"]

        analysis = {
            "country": country,
            "analysis_date": datetime.now().isoformat(),
            "categories": {},
            "summary": {},
            "leading_indicators": [],
            "coincident_indicators": [],
            "lagging_indicators": []
        }

        all_signals = []

        for category in categories:
            indicators = self.db_service.get_economic_indicators(
                country=country,
                category=category,
                limit=100
            )

            if not indicators:
                continue

            category_analysis = {
                "indicator_count": len(indicators),
                "indicators": []
            }

            for indicator in indicators:
                # Get historical data for trend analysis
                history = self.db_service.get_indicator_history(
                    country=country,
                    indicator_name=indicator.indicator_name,
                    limit=12
                )

                previous_value = None
                historical_avg = None

                if len(history) > 1:
                    previous_value = history[1].value_numeric
                if len(history) >= 3:
                    historical_avg = statistics.mean([
                        h.value_numeric for h in history
                        if h.value_numeric is not None
                    ])

                if indicator.last_value_numeric is not None:
                    interp = self.interpret_indicator(
                        indicator.indicator_name,
                        indicator.last_value_numeric,
                        previous_value,
                        historical_avg
                    )

                    category_analysis["indicators"].append(interp)

                    # Classify by type
                    classification = self.classify_indicator(indicator.indicator_name)
                    if classification == IndicatorType.LEADING:
                        analysis["leading_indicators"].append(interp)
                    elif classification == IndicatorType.COINCIDENT:
                        analysis["coincident_indicators"].append(interp)
                    else:
                        analysis["lagging_indicators"].append(interp)

                    all_signals.append(interp.get("signal", "neutral"))

            analysis["categories"][category] = category_analysis

        # Generate overall summary
        analysis["summary"] = self._generate_summary(all_signals, analysis)

        return analysis

    def _generate_summary(
        self,
        all_signals: List[str],
        analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate overall economic summary"""
        if not all_signals:
            return {"overall_health": "unknown", "message": "No data available"}

        # Count signals
        signal_counts = {
            "very_positive": all_signals.count("very_positive"),
            "positive": all_signals.count("positive"),
            "neutral": all_signals.count("neutral"),
            "negative": all_signals.count("negative"),
            "very_negative": all_signals.count("very_negative"),
        }

        total = len(all_signals)
        positive_pct = (signal_counts["very_positive"] + signal_counts["positive"]) / total * 100
        negative_pct = (signal_counts["very_negative"] + signal_counts["negative"]) / total * 100

        # Determine overall health
        if positive_pct > 60:
            overall = "strong"
            health_score = 80 + (positive_pct - 60) / 2
        elif positive_pct > 40:
            overall = "good"
            health_score = 60 + (positive_pct - 40)
        elif negative_pct > 60:
            overall = "weak"
            health_score = 20 + (40 - negative_pct)
        elif negative_pct > 40:
            overall = "concerning"
            health_score = 40 - (negative_pct - 40)
        else:
            overall = "mixed"
            health_score = 50

        return {
            "overall_health": overall,
            "health_score": round(health_score, 1),
            "positive_indicators_pct": round(positive_pct, 1),
            "negative_indicators_pct": round(negative_pct, 1),
            "total_indicators_analyzed": total,
            "leading_count": len(analysis["leading_indicators"]),
            "coincident_count": len(analysis["coincident_indicators"]),
            "lagging_count": len(analysis["lagging_indicators"]),
            "message": self._get_health_message(overall, positive_pct, negative_pct)
        }

    def _get_health_message(
        self,
        overall: str,
        positive_pct: float,
        negative_pct: float
    ) -> str:
        """Generate health message"""
        if overall == "strong":
            return f"Economy showing strong performance with {positive_pct:.0f}% of indicators positive."
        elif overall == "good":
            return f"Economy in good shape with {positive_pct:.0f}% of indicators positive."
        elif overall == "weak":
            return f"Economy showing weakness with {negative_pct:.0f}% of indicators negative."
        elif overall == "concerning":
            return f"Economy showing concerning signs with {negative_pct:.0f}% of indicators negative."
        else:
            return "Economy showing mixed signals with balanced positive and negative indicators."
