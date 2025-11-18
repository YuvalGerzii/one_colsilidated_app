"""
Correlation Analyzer

Analyzes correlations between economic indicators to identify relationships.

Based on economic research:
- Housing prices correlate with GDP growth, inflation, and mortgage rates
- Unemployment and inflation often have inverse relationships (Phillips Curve)
- Interest rates affect housing, consumer spending, and business investment
- GDP growth correlates with employment, consumer confidence, and business activity
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import statistics

from app.services.economics_db_service import EconomicsDBService

logger = logging.getLogger(__name__)


class CorrelationAnalyzer:
    """Analyze correlations between economic indicators"""

    # Known correlations based on economic theory
    THEORETICAL_CORRELATIONS = {
        ("GDP Growth Rate", "Unemployment Rate"): "negative",  # Okun's Law
        ("GDP Growth Rate", "House Prices"): "positive",
        ("Inflation Rate", "Mortgage Rates"): "positive",
        ("Mortgage Rates", "House Prices"): "negative_complex",  # Complex relationship
        ("Consumer Confidence", "Retail Sales"): "positive",
        ("Interest Rates", "Housing Starts"): "negative",
        ("Unemployment Rate", "Consumer Spending"): "negative",
        ("GDP Growth Rate", "Business Confidence"): "positive",
        ("Inflation Rate", "Purchasing Power"): "negative",
        ("House Prices", "Building Permits"): "positive",
    }

    def __init__(self, db_service: EconomicsDBService):
        self.db_service = db_service

    def calculate_correlation(
        self,
        values_x: List[float],
        values_y: List[float]
    ) -> Optional[float]:
        """
        Calculate Pearson correlation coefficient

        Args:
            values_x: First series of values
            values_y: Second series of values

        Returns:
            Correlation coefficient (-1 to 1) or None
        """
        if len(values_x) != len(values_y) or len(values_x) < 3:
            return None

        # Remove None values
        pairs = [(x, y) for x, y in zip(values_x, values_y) if x is not None and y is not None]

        if len(pairs) < 3:
            return None

        x_vals = [p[0] for p in pairs]
        y_vals = [p[1] for p in pairs]

        # Calculate correlation
        n = len(x_vals)
        x_mean = statistics.mean(x_vals)
        y_mean = statistics.mean(y_vals)

        numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_vals, y_vals))
        denominator_x = sum((x - x_mean) ** 2 for x in x_vals)
        denominator_y = sum((y - y_mean) ** 2 for y in y_vals)

        if denominator_x == 0 or denominator_y == 0:
            return None

        correlation = numerator / (denominator_x * denominator_y) ** 0.5

        return correlation

    def analyze_correlation(
        self,
        country: str,
        indicator_x: str,
        indicator_y: str,
        periods: int = 12
    ) -> Dict[str, Any]:
        """
        Analyze correlation between two indicators

        Args:
            country: Country name
            indicator_x: First indicator
            indicator_y: Second indicator
            periods: Number of periods to analyze

        Returns:
            Dict with correlation analysis
        """
        # Get historical data for both indicators
        history_x = self.db_service.get_indicator_history(
            country=country,
            indicator_name=indicator_x,
            limit=periods
        )

        history_y = self.db_service.get_indicator_history(
            country=country,
            indicator_name=indicator_y,
            limit=periods
        )

        if len(history_x) < 3 or len(history_y) < 3:
            return {
                "error": "Insufficient data for correlation analysis",
                "data_points_x": len(history_x),
                "data_points_y": len(history_y)
            }

        # Extract values
        values_x = [h.value_numeric for h in reversed(history_x) if h.value_numeric is not None]
        values_y = [h.value_numeric for h in reversed(history_y) if h.value_numeric is not None]

        # Ensure same length (use minimum)
        min_len = min(len(values_x), len(values_y))
        values_x = values_x[:min_len]
        values_y = values_y[:min_len]

        # Calculate correlation
        correlation = self.calculate_correlation(values_x, values_y)

        if correlation is None:
            return {"error": "Unable to calculate correlation"}

        analysis = {
            "indicator_x": indicator_x,
            "indicator_y": indicator_y,
            "country": country,
            "data_points": min_len,
            "correlation_coefficient": round(correlation, 3),
            "correlation_strength": self._classify_correlation_strength(correlation),
            "relationship": self._classify_relationship(correlation)
        }

        # Check theoretical expectation
        theoretical = self._get_theoretical_correlation(indicator_x, indicator_y)
        if theoretical:
            analysis["theoretical_expectation"] = theoretical
            analysis["matches_theory"] = self._check_theory_match(correlation, theoretical)

        # Interpretation
        analysis["interpretation"] = self._generate_correlation_interpretation(analysis)

        return analysis

    def _classify_correlation_strength(self, correlation: float) -> str:
        """Classify correlation strength"""
        abs_corr = abs(correlation)

        if abs_corr >= 0.9:
            return "very_strong"
        elif abs_corr >= 0.7:
            return "strong"
        elif abs_corr >= 0.5:
            return "moderate"
        elif abs_corr >= 0.3:
            return "weak"
        else:
            return "very_weak"

    def _classify_relationship(self, correlation: float) -> str:
        """Classify relationship type"""
        if correlation > 0.3:
            return "positive"
        elif correlation < -0.3:
            return "negative"
        else:
            return "negligible"

    def _get_theoretical_correlation(
        self,
        indicator_x: str,
        indicator_y: str
    ) -> Optional[str]:
        """Get theoretical correlation expectation"""
        # Check both orders
        key1 = (indicator_x, indicator_y)
        key2 = (indicator_y, indicator_x)

        if key1 in self.THEORETICAL_CORRELATIONS:
            return self.THEORETICAL_CORRELATIONS[key1]
        elif key2 in self.THEORETICAL_CORRELATIONS:
            return self.THEORETICAL_CORRELATIONS[key2]

        # Check partial matches
        for (ind_a, ind_b), corr_type in self.THEORETICAL_CORRELATIONS.items():
            if (ind_a.lower() in indicator_x.lower() or ind_a.lower() in indicator_y.lower()) and \
               (ind_b.lower() in indicator_x.lower() or ind_b.lower() in indicator_y.lower()):
                return corr_type

        return None

    def _check_theory_match(self, correlation: float, theoretical: str) -> bool:
        """Check if correlation matches theoretical expectation"""
        if theoretical == "positive":
            return correlation > 0.3
        elif theoretical == "negative":
            return correlation < -0.3
        elif theoretical == "negative_complex":
            # Complex relationships may vary
            return True
        return True

    def _generate_correlation_interpretation(self, analysis: Dict[str, Any]) -> str:
        """Generate interpretation text"""
        texts = []

        indicator_x = analysis["indicator_x"]
        indicator_y = analysis["indicator_y"]
        correlation = analysis["correlation_coefficient"]
        strength = analysis["correlation_strength"]
        relationship = analysis["relationship"]

        # Relationship description
        if relationship == "positive":
            texts.append(
                f"📈 {indicator_x} and {indicator_y} have a {strength} positive correlation ({correlation:.2f})."
            )
            texts.append(
                f"When {indicator_x} increases, {indicator_y} tends to increase as well."
            )
        elif relationship == "negative":
            texts.append(
                f"📉 {indicator_x} and {indicator_y} have a {strength} negative correlation ({correlation:.2f})."
            )
            texts.append(
                f"When {indicator_x} increases, {indicator_y} tends to decrease."
            )
        else:
            texts.append(
                f"➡️ {indicator_x} and {indicator_y} show little correlation ({correlation:.2f})."
            )
            texts.append(
                f"Changes in {indicator_x} don't strongly predict changes in {indicator_y}."
            )

        # Theoretical comparison
        if "theoretical_expectation" in analysis:
            theoretical = analysis["theoretical_expectation"]
            matches = analysis.get("matches_theory", False)

            if matches:
                texts.append(
                    f"✅ This matches the expected {theoretical} relationship from economic theory."
                )
            else:
                texts.append(
                    f"⚠️ This differs from the expected {theoretical} relationship, which may indicate unique economic conditions."
                )

        # Strength interpretation
        if strength == "very_strong":
            texts.append(
                "The relationship is very strong and highly predictive."
            )
        elif strength == "strong":
            texts.append(
                "The relationship is strong enough for predictive analysis."
            )
        elif strength == "moderate":
            texts.append(
                "The relationship is moderate - other factors also play significant roles."
            )
        else:
            texts.append(
                "The relationship is weak - many other factors influence these indicators."
            )

        return " ".join(texts)

    def analyze_multiple_correlations(
        self,
        country: str,
        target_indicator: str,
        other_indicators: List[str],
        periods: int = 12
    ) -> Dict[str, Any]:
        """
        Analyze correlations between a target indicator and multiple others

        Args:
            country: Country name
            target_indicator: Main indicator to analyze
            other_indicators: List of indicators to correlate with
            periods: Number of periods

        Returns:
            Dict with multiple correlation analysis
        """
        analysis = {
            "country": country,
            "target_indicator": target_indicator,
            "correlations": [],
            "summary": {}
        }

        correlations = []

        for indicator in other_indicators:
            corr_analysis = self.analyze_correlation(
                country,
                target_indicator,
                indicator,
                periods
            )

            if "error" not in corr_analysis:
                analysis["correlations"].append(corr_analysis)
                correlations.append((
                    indicator,
                    corr_analysis["correlation_coefficient"],
                    corr_analysis["correlation_strength"]
                ))

        # Sort by absolute correlation
        correlations.sort(key=lambda x: abs(x[1]), reverse=True)

        if correlations:
            analysis["summary"] = {
                "total_analyzed": len(correlations),
                "strongest_positive": next(
                    ((ind, corr) for ind, corr, _ in correlations if corr > 0),
                    None
                ),
                "strongest_negative": next(
                    ((ind, corr) for ind, corr, _ in correlations if corr < 0),
                    None
                ),
                "ranked_by_strength": [
                    {
                        "indicator": ind,
                        "correlation": round(corr, 3),
                        "strength": strength
                    }
                    for ind, corr, strength in correlations
                ]
            }

        return analysis

    def find_leading_indicators(
        self,
        country: str,
        target_indicator: str,
        candidate_indicators: List[str],
        periods: int = 12,
        lag_periods: int = 3
    ) -> Dict[str, Any]:
        """
        Find indicators that lead (predict) the target indicator

        Args:
            country: Country name
            target_indicator: Indicator to predict
            candidate_indicators: Potential leading indicators
            periods: Number of periods to analyze
            lag_periods: How many periods to lag the candidate

        Returns:
            Dict with leading indicator analysis
        """
        analysis = {
            "country": country,
            "target_indicator": target_indicator,
            "lag_periods": lag_periods,
            "leading_indicators": []
        }

        # Get target history
        target_history = self.db_service.get_indicator_history(
            country=country,
            indicator_name=target_indicator,
            limit=periods
        )

        if len(target_history) < lag_periods + 3:
            return {"error": "Insufficient data for lag analysis"}

        target_values = [
            h.value_numeric for h in reversed(target_history)
            if h.value_numeric is not None
        ]

        for candidate in candidate_indicators:
            # Get candidate history
            candidate_history = self.db_service.get_indicator_history(
                country=country,
                indicator_name=candidate,
                limit=periods + lag_periods
            )

            if len(candidate_history) < periods + lag_periods:
                continue

            candidate_values = [
                h.value_numeric for h in reversed(candidate_history)
                if h.value_numeric is not None
            ]

            # Shift candidate back by lag_periods
            lagged_candidate = candidate_values[:len(target_values)]

            # Calculate correlation
            correlation = self.calculate_correlation(lagged_candidate, target_values)

            if correlation is not None and abs(correlation) > 0.3:
                analysis["leading_indicators"].append({
                    "indicator": candidate,
                    "correlation_with_lag": round(correlation, 3),
                    "lag_periods": lag_periods,
                    "predictive_strength": self._classify_correlation_strength(correlation),
                    "interpretation": (
                        f"{candidate} shows {self._classify_correlation_strength(correlation)} "
                        f"correlation with {target_indicator} {lag_periods} periods later. "
                        f"This suggests {candidate} may help predict future {target_indicator} values."
                    )
                })

        # Sort by predictive power
        analysis["leading_indicators"].sort(
            key=lambda x: abs(x["correlation_with_lag"]),
            reverse=True
        )

        return analysis
