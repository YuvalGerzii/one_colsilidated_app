"""
Housing Market Specialized Analyzer

Comprehensive analysis of housing market indicators with real estate-specific insights.

Analyzes:
- Housing affordability (price-to-income ratio, mortgage burden)
- Market momentum (building permits, starts, sales)
- Price trends and appreciation rates
- Mortgage rate impact on affordability
- Housing market health score
- Market cycle identification (expansion, peak, contraction, trough)
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
import statistics

from app.services.economics_db_service import EconomicsDBService
from app.services.economic_analyzer import EconomicAnalyzer
from app.services.trend_analyzer import TrendAnalyzer
from app.services.correlation_analyzer import CorrelationAnalyzer

logger = logging.getLogger(__name__)


class MarketCycle(Enum):
    """Housing market cycle phase"""
    EXPANSION = "expansion"        # Rising prices, high activity
    PEAK = "peak"                  # Maximum prices, slowing activity
    CONTRACTION = "contraction"    # Falling prices, low activity
    TROUGH = "trough"              # Minimum prices, bottoming out
    RECOVERY = "recovery"          # Stabilizing, early growth


class AffordabilityLevel(Enum):
    """Housing affordability classification"""
    EXCELLENT = "excellent"        # Price-to-income < 3
    GOOD = "good"                  # 3-4
    MODERATE = "moderate"          # 4-5
    POOR = "poor"                  # 5-6
    VERY_POOR = "very_poor"        # > 6


class HousingMarketAnalyzer:
    """Specialized analyzer for housing market data"""

    # Key housing indicators
    KEY_INDICATORS = {
        "price": ["House Price", "Home Price", "Housing Price Index"],
        "sales": ["New Home Sales", "Existing Home Sales", "Home Sales"],
        "supply": ["Housing Starts", "Building Permits", "Housing Inventory"],
        "financing": ["Mortgage Rate", "30 Year Mortgage", "15 Year Mortgage"],
        "affordability": ["Affordability Index", "Price to Income"],
    }

    def __init__(self, db_service: EconomicsDBService):
        self.db_service = db_service
        self.economic_analyzer = EconomicAnalyzer(db_service)
        self.trend_analyzer = TrendAnalyzer(db_service)
        self.correlation_analyzer = CorrelationAnalyzer(db_service)

    def analyze_housing_market(
        self,
        country: str
    ) -> Dict[str, Any]:
        """
        Comprehensive housing market analysis

        Args:
            country: Country name

        Returns:
            Dict with complete housing market analysis
        """
        analysis = {
            "country": country,
            "analysis_date": datetime.now().isoformat(),
            "market_overview": {},
            "affordability": {},
            "market_momentum": {},
            "price_trends": {},
            "mortgage_impact": {},
            "market_health_score": 0,
            "market_cycle": None,
            "key_insights": [],
            "recommendations": []
        }

        # Get all housing indicators
        housing_indicators = self.db_service.get_economic_indicators(
            country=country,
            category="housing"
        )

        if not housing_indicators:
            return {"error": "No housing data available for this country"}

        # Market overview
        analysis["market_overview"] = self._analyze_market_overview(
            country,
            housing_indicators
        )

        # Affordability analysis
        analysis["affordability"] = self._analyze_affordability(
            country,
            housing_indicators
        )

        # Market momentum
        analysis["market_momentum"] = self._analyze_momentum(
            country,
            housing_indicators
        )

        # Price trends
        analysis["price_trends"] = self._analyze_price_trends(
            country,
            housing_indicators
        )

        # Mortgage rate impact
        analysis["mortgage_impact"] = self._analyze_mortgage_impact(
            country,
            housing_indicators
        )

        # Calculate health score
        analysis["market_health_score"] = self._calculate_market_health_score(analysis)

        # Identify market cycle
        analysis["market_cycle"] = self._identify_market_cycle(analysis)

        # Generate insights
        analysis["key_insights"] = self._generate_key_insights(analysis)

        # Generate recommendations
        analysis["recommendations"] = self._generate_recommendations(analysis)

        return analysis

    def _analyze_market_overview(
        self,
        country: str,
        indicators: List[Any]
    ) -> Dict[str, Any]:
        """Analyze overall market conditions"""
        overview = {
            "total_indicators": len(indicators),
            "key_metrics": {}
        }

        # Extract key metrics
        for indicator in indicators:
            name_lower = indicator.indicator_name.lower()

            if "house price" in name_lower or "home price" in name_lower:
                overview["key_metrics"]["average_price"] = {
                    "value": indicator.last_value_numeric,
                    "formatted": indicator.last_value,
                    "unit": indicator.unit,
                    "date": indicator.data_date.isoformat() if indicator.data_date else None
                }

            elif "housing start" in name_lower:
                overview["key_metrics"]["housing_starts"] = {
                    "value": indicator.last_value_numeric,
                    "formatted": indicator.last_value,
                    "unit": indicator.unit
                }

            elif "building permit" in name_lower:
                overview["key_metrics"]["building_permits"] = {
                    "value": indicator.last_value_numeric,
                    "formatted": indicator.last_value,
                    "unit": indicator.unit
                }

            elif "mortgage rate" in name_lower and "30" in name_lower:
                overview["key_metrics"]["mortgage_rate_30y"] = {
                    "value": indicator.last_value_numeric,
                    "formatted": indicator.last_value,
                    "unit": indicator.unit
                }

            elif "new home sales" in name_lower:
                overview["key_metrics"]["new_home_sales"] = {
                    "value": indicator.last_value_numeric,
                    "formatted": indicator.last_value,
                    "unit": indicator.unit
                }

        return overview

    def _analyze_affordability(
        self,
        country: str,
        housing_indicators: List[Any]
    ) -> Dict[str, Any]:
        """Analyze housing affordability"""
        affordability = {
            "metrics": {},
            "level": None,
            "interpretation": ""
        }

        # Get house price
        house_price_ind = next(
            (ind for ind in housing_indicators
             if "house price" in ind.indicator_name.lower()
             or "home price" in ind.indicator_name.lower()),
            None
        )

        # Get mortgage rate
        mortgage_rate_ind = next(
            (ind for ind in housing_indicators
             if "mortgage rate" in ind.indicator_name.lower()
             and "30" in ind.indicator_name.lower()),
            None
        )

        # Get GDP per capita for income proxy
        gdp_indicators = self.db_service.get_economic_indicators(
            country=country,
            category="gdp"
        )

        gdp_per_capita_ind = next(
            (ind for ind in gdp_indicators
             if "per capita" in ind.indicator_name.lower()),
            None
        )

        if house_price_ind and gdp_per_capita_ind:
            house_price = house_price_ind.last_value_numeric
            income = gdp_per_capita_ind.last_value_numeric

            if house_price and income and income > 0:
                price_to_income = house_price / income

                affordability["metrics"]["price_to_income_ratio"] = round(price_to_income, 2)
                affordability["metrics"]["house_price"] = house_price
                affordability["metrics"]["annual_income"] = income

                # Classify affordability
                if price_to_income < 3:
                    affordability["level"] = AffordabilityLevel.EXCELLENT.value
                elif price_to_income < 4:
                    affordability["level"] = AffordabilityLevel.GOOD.value
                elif price_to_income < 5:
                    affordability["level"] = AffordabilityLevel.MODERATE.value
                elif price_to_income < 6:
                    affordability["level"] = AffordabilityLevel.POOR.value
                else:
                    affordability["level"] = AffordabilityLevel.VERY_POOR.value

                # Calculate monthly payment burden
                if mortgage_rate_ind and mortgage_rate_ind.last_value_numeric:
                    mortgage_rate = mortgage_rate_ind.last_value_numeric
                    loan_amount = house_price * 0.8  # 20% down
                    monthly_rate = mortgage_rate / 100 / 12
                    n_payments = 360  # 30 years

                    if monthly_rate > 0:
                        monthly_payment = loan_amount * (
                            monthly_rate * (1 + monthly_rate) ** n_payments
                        ) / ((1 + monthly_rate) ** n_payments - 1)

                        monthly_income = income / 12
                        payment_to_income_pct = (monthly_payment / monthly_income) * 100

                        affordability["metrics"]["monthly_payment"] = round(monthly_payment, 2)
                        affordability["metrics"]["monthly_income"] = round(monthly_income, 2)
                        affordability["metrics"]["payment_to_income_pct"] = round(payment_to_income_pct, 1)
                        affordability["metrics"]["mortgage_rate"] = mortgage_rate

                        # Affordability interpretation
                        if payment_to_income_pct < 25:
                            burden = "manageable"
                        elif payment_to_income_pct < 30:
                            burden = "moderate"
                        elif payment_to_income_pct < 35:
                            burden = "high"
                        else:
                            burden = "very high"

                        affordability["metrics"]["burden_level"] = burden

                # Generate interpretation
                affordability["interpretation"] = self._generate_affordability_interpretation(
                    affordability["metrics"],
                    affordability["level"]
                )

        return affordability

    def _analyze_momentum(
        self,
        country: str,
        housing_indicators: List[Any]
    ) -> Dict[str, Any]:
        """Analyze market momentum using leading indicators"""
        momentum = {
            "indicators": {},
            "overall_momentum": None,
            "momentum_score": 0
        }

        # Leading indicators for housing: permits, starts, new sales
        leading_names = ["Building Permits", "Housing Starts", "New Home Sales"]

        momentum_scores = []

        for indicator_name in leading_names:
            # Find matching indicator
            indicator = next(
                (ind for ind in housing_indicators
                 if indicator_name.lower() in ind.indicator_name.lower()),
                None
            )

            if indicator:
                # Analyze trend
                trend_analysis = self.trend_analyzer.analyze_trend(
                    country,
                    indicator.indicator_name,
                    periods=6
                )

                if "error" not in trend_analysis:
                    trend = trend_analysis.get("trend", {})
                    direction = trend.get("direction", "flat")

                    # Score momentum
                    if direction == "upward":
                        score = 75
                    elif direction == "flat":
                        score = 50
                    else:  # downward
                        score = 25

                    momentum_scores.append(score)

                    momentum["indicators"][indicator_name] = {
                        "trend": direction,
                        "momentum_score": score,
                        "current_value": indicator.last_value_numeric
                    }

        # Calculate overall momentum
        if momentum_scores:
            avg_score = statistics.mean(momentum_scores)
            momentum["momentum_score"] = round(avg_score, 1)

            if avg_score > 70:
                momentum["overall_momentum"] = "strong_positive"
            elif avg_score > 55:
                momentum["overall_momentum"] = "positive"
            elif avg_score > 45:
                momentum["overall_momentum"] = "neutral"
            elif avg_score > 30:
                momentum["overall_momentum"] = "negative"
            else:
                momentum["overall_momentum"] = "strong_negative"

        return momentum

    def _analyze_price_trends(
        self,
        country: str,
        housing_indicators: List[Any]
    ) -> Dict[str, Any]:
        """Analyze house price trends"""
        # Find price indicator
        price_indicator = next(
            (ind for ind in housing_indicators
             if "house price" in ind.indicator_name.lower()
             or "home price" in ind.indicator_name.lower()),
            None
        )

        if not price_indicator:
            return {"error": "No price data available"}

        # Analyze trend
        trend_analysis = self.trend_analyzer.analyze_trend(
            country,
            price_indicator.indicator_name,
            periods=12
        )

        return trend_analysis

    def _analyze_mortgage_impact(
        self,
        country: str,
        housing_indicators: List[Any]
    ) -> Dict[str, Any]:
        """Analyze mortgage rate impact on housing market"""
        impact = {}

        # Get mortgage rate
        mortgage_ind = next(
            (ind for ind in housing_indicators
             if "mortgage rate" in ind.indicator_name.lower()
             and "30" in ind.indicator_name.lower()),
            None
        )

        if not mortgage_ind:
            return {"error": "No mortgage rate data"}

        # Analyze mortgage rate trend
        mortgage_trend = self.trend_analyzer.analyze_trend(
            country,
            mortgage_ind.indicator_name,
            periods=12
        )

        impact["mortgage_rate_trend"] = mortgage_trend

        # Correlation with sales
        sales_indicators = [
            ind.indicator_name for ind in housing_indicators
            if "sales" in ind.indicator_name.lower()
        ]

        if sales_indicators:
            # Analyze correlation between mortgage rates and sales
            correlation = self.correlation_analyzer.analyze_correlation(
                country,
                mortgage_ind.indicator_name,
                sales_indicators[0],
                periods=12
            )

            impact["correlation_with_sales"] = correlation

        return impact

    def _calculate_market_health_score(self, analysis: Dict[str, Any]) -> float:
        """Calculate overall housing market health score (0-100)"""
        scores = []

        # Affordability component (30%)
        affordability = analysis.get("affordability", {})
        if affordability.get("level"):
            level = affordability["level"]
            if level == "excellent":
                scores.append(("affordability", 95, 0.30))
            elif level == "good":
                scores.append(("affordability", 80, 0.30))
            elif level == "moderate":
                scores.append(("affordability", 60, 0.30))
            elif level == "poor":
                scores.append(("affordability", 40, 0.30))
            else:
                scores.append(("affordability", 20, 0.30))

        # Momentum component (25%)
        momentum = analysis.get("market_momentum", {})
        if "momentum_score" in momentum:
            scores.append(("momentum", momentum["momentum_score"], 0.25))

        # Price trend component (25%)
        price_trends = analysis.get("price_trends", {})
        trend = price_trends.get("trend", {})
        if trend:
            direction = trend.get("direction", "flat")
            strength = trend.get("strength", "weak")

            if direction == "upward" and strength in ["strong", "very_strong"]:
                trend_score = 75
            elif direction == "upward":
                trend_score = 65
            elif direction == "flat":
                trend_score = 50
            elif direction == "downward" and strength == "weak":
                trend_score = 40
            else:
                trend_score = 25

            scores.append(("price_trend", trend_score, 0.25))

        # Mortgage rate component (20%)
        mortgage_impact = analysis.get("mortgage_impact", {})
        mortgage_trend = mortgage_impact.get("mortgage_rate_trend", {})
        if mortgage_trend and "trend" in mortgage_trend:
            direction = mortgage_trend["trend"].get("direction", "flat")

            # Lower mortgage rates are better for housing
            if direction == "downward":
                mortgage_score = 80
            elif direction == "flat":
                mortgage_score = 50
            else:
                mortgage_score = 30

            scores.append(("mortgage", mortgage_score, 0.20))

        # Calculate weighted average
        if scores:
            total_score = sum(score * weight for _, score, weight in scores)
            total_weight = sum(weight for _, _, weight in scores)

            # Normalize to 100
            health_score = (total_score / total_weight) if total_weight > 0 else 50

            return round(health_score, 1)

        return 50.0

    def _identify_market_cycle(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Identify current market cycle phase"""
        price_trends = analysis.get("price_trends", {})
        momentum = analysis.get("market_momentum", {})

        trend = price_trends.get("trend", {})
        direction = trend.get("direction", "flat")
        strength = trend.get("strength", "weak")

        momentum_status = momentum.get("overall_momentum", "neutral")

        # Determine cycle phase
        if direction == "upward" and momentum_status in ["strong_positive", "positive"]:
            phase = MarketCycle.EXPANSION.value
        elif direction == "upward" and momentum_status in ["neutral", "negative"]:
            phase = MarketCycle.PEAK.value
        elif direction == "downward" and momentum_status in ["negative", "strong_negative"]:
            phase = MarketCycle.CONTRACTION.value
        elif direction == "downward" and momentum_status in ["neutral", "positive"]:
            phase = MarketCycle.TROUGH.value
        else:
            phase = MarketCycle.RECOVERY.value

        return {
            "phase": phase,
            "interpretation": self._get_cycle_interpretation(phase)
        }

    def _get_cycle_interpretation(self, phase: str) -> str:
        """Get interpretation for market cycle phase"""
        interpretations = {
            "expansion": "📈 Market is in expansion phase with rising prices and strong activity. Good time for sellers.",
            "peak": "🔝 Market may be peaking with high prices but slowing momentum. Consider market timing carefully.",
            "contraction": "📉 Market is contracting with falling prices and weak activity. Buyer's market emerging.",
            "trough": "🔻 Market may be bottoming out. Could be approaching buying opportunity.",
            "recovery": "♻️ Market is in early recovery with stabilizing conditions. Transition phase."
        }

        return interpretations.get(phase, "Market phase undetermined")

    def _generate_affordability_interpretation(
        self,
        metrics: Dict[str, Any],
        level: str
    ) -> str:
        """Generate affordability interpretation"""
        texts = []

        price_to_income = metrics.get("price_to_income_ratio")
        if price_to_income:
            texts.append(
                f"Price-to-income ratio is {price_to_income:.1f}x, "
                f"indicating {level} affordability."
            )

        payment_pct = metrics.get("payment_to_income_pct")
        if payment_pct:
            burden = metrics.get("burden_level", "unknown")
            texts.append(
                f"Monthly mortgage payments represent {payment_pct:.1f}% of income, "
                f"which is a {burden} burden."
            )

            if payment_pct < 28:
                texts.append("✅ This meets the traditional 28% rule for housing affordability.")
            else:
                texts.append("⚠️ This exceeds the traditional 28% housing affordability guideline.")

        return " ".join(texts)

    def _generate_key_insights(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate key insights from analysis"""
        insights = []

        # Health score insight
        health_score = analysis.get("market_health_score", 0)
        if health_score > 75:
            insights.append(f"🌟 Market health is strong (score: {health_score}/100)")
        elif health_score > 50:
            insights.append(f"📊 Market health is moderate (score: {health_score}/100)")
        else:
            insights.append(f"⚠️ Market health is weak (score: {health_score}/100)")

        # Cycle insight
        cycle = analysis.get("market_cycle", {})
        if cycle:
            insights.append(cycle.get("interpretation", ""))

        # Affordability insight
        affordability = analysis.get("affordability", {})
        if affordability.get("interpretation"):
            insights.append(f"🏠 {affordability['interpretation']}")

        # Momentum insight
        momentum = analysis.get("market_momentum", {})
        if momentum.get("overall_momentum"):
            momentum_status = momentum["overall_momentum"]
            if momentum_status == "strong_positive":
                insights.append("📈 Market momentum is strongly positive with rising activity")
            elif momentum_status == "negative":
                insights.append("📉 Market momentum is negative with declining activity")

        return insights

    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []

        cycle = analysis.get("market_cycle", {})
        phase = cycle.get("phase")

        affordability = analysis.get("affordability", {})
        level = affordability.get("level")

        # Cycle-based recommendations
        if phase == "expansion":
            recommendations.append("Consider locking in current prices before further appreciation")
            recommendations.append("Good time for sellers to list properties")
        elif phase == "peak":
            recommendations.append("Buyers should exercise caution - prices may have peaked")
            recommendations.append("Sellers may want to capitalize on high prices")
        elif phase == "contraction":
            recommendations.append("Buyers may find better negotiating power")
            recommendations.append("Sellers should price competitively")
        elif phase == "trough":
            recommendations.append("Potential buying opportunity as market bottoms")
            recommendations.append("Watch for signs of recovery before entering")

        # Affordability-based recommendations
        if level in ["poor", "very_poor"]:
            recommendations.append("Consider locations with better affordability")
            recommendations.append("Explore financing options to reduce monthly burden")
        elif level == "excellent":
            recommendations.append("Strong affordability supports market stability")

        return recommendations
