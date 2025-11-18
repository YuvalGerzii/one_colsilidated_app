"""
Risk Assessment Calculators

Calculate various economic and investment risks:
- Recession probability calculator
- Housing bubble risk score
- Economic vulnerability index
- Currency risk assessment
- Inflation risk score
- Investment risk metrics
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import statistics

from app.services.economics_db_service import EconomicsDBService
from app.services.economic_analyzer import EconomicAnalyzer
from app.services.trend_analyzer import TrendAnalyzer

logger = logging.getLogger(__name__)


class RiskCalculators:
    """Calculate various economic and investment risk metrics"""

    def __init__(self, db_service: EconomicsDBService):
        self.db_service = db_service
        self.analyzer = EconomicAnalyzer(db_service)
        self.trend_analyzer = TrendAnalyzer(db_service)

    def calculate_recession_probability(
        self,
        country: str
    ) -> Dict[str, Any]:
        """
        Calculate recession probability using leading indicators

        Based on:
        - GDP growth trend
        - Unemployment trend
        - PMI levels
        - Consumer confidence
        - Yield curve (if available)
        - Leading indicators momentum

        Args:
            country: Country name

        Returns:
            Dict with recession probability and risk factors
        """
        risk_factors = []
        risk_score = 0
        max_score = 0

        # 1. GDP Growth (30 points)
        max_score += 30
        gdp_indicators = self.db_service.get_economic_indicators(
            country=country,
            category="gdp"
        )

        gdp_growth_ind = next(
            (ind for ind in gdp_indicators
             if "growth" in ind.indicator_name.lower()),
            None
        )

        if gdp_growth_ind and gdp_growth_ind.last_value_numeric is not None:
            gdp_growth = gdp_growth_ind.last_value_numeric

            # Analyze trend
            gdp_trend = self.trend_analyzer.analyze_trend(
                country,
                gdp_growth_ind.indicator_name,
                periods=6
            )

            if "error" not in gdp_trend:
                direction = gdp_trend.get("trend", {}).get("direction", "flat")
                momentum = gdp_trend.get("momentum", {})

                # Score based on growth level and trend
                if gdp_growth < 0:
                    gdp_risk = 30
                    risk_factors.append("🚨 GDP growth is negative (recession indicator)")
                elif gdp_growth < 1:
                    gdp_risk = 25
                    risk_factors.append("⚠️ GDP growth is very weak (<1%)")
                elif gdp_growth < 2:
                    gdp_risk = 15
                    risk_factors.append("⚠️ GDP growth is below trend (<2%)")
                elif direction == "downward":
                    gdp_risk = 10
                    risk_factors.append("📉 GDP growth is trending downward")
                else:
                    gdp_risk = 0
                    risk_factors.append("✅ GDP growth is healthy")

                risk_score += gdp_risk

        # 2. Unemployment Trend (20 points)
        max_score += 20
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
            unemployment_trend = self.trend_analyzer.analyze_trend(
                country,
                unemployment_ind.indicator_name,
                periods=6
            )

            if "error" not in unemployment_trend:
                direction = unemployment_trend.get("trend", {}).get("direction", "flat")
                growth_rate = unemployment_trend.get("growth_rates", {}).get("period_over_period", 0)

                if direction == "upward" and growth_rate > 5:
                    unemployment_risk = 20
                    risk_factors.append("🚨 Unemployment rising rapidly")
                elif direction == "upward":
                    unemployment_risk = 15
                    risk_factors.append("⚠️ Unemployment trending upward")
                elif unemployment_ind.last_value_numeric > 7:
                    unemployment_risk = 10
                    risk_factors.append("⚠️ Unemployment is elevated")
                else:
                    unemployment_risk = 0
                    risk_factors.append("✅ Unemployment stable or declining")

                risk_score += unemployment_risk

        # 3. PMI / Business Confidence (15 points)
        max_score += 15
        business_indicators = self.db_service.get_economic_indicators(
            country=country,
            category="business"
        )

        pmi_ind = next(
            (ind for ind in business_indicators
             if "pmi" in ind.indicator_name.lower()),
            None
        )

        if pmi_ind and pmi_ind.last_value_numeric is not None:
            pmi = pmi_ind.last_value_numeric

            if pmi < 45:
                pmi_risk = 15
                risk_factors.append("🚨 PMI shows severe contraction (<45)")
            elif pmi < 50:
                pmi_risk = 10
                risk_factors.append("⚠️ PMI shows contraction (<50)")
            elif pmi < 52:
                pmi_risk = 5
                risk_factors.append("⚠️ PMI near contraction threshold")
            else:
                pmi_risk = 0
                risk_factors.append("✅ PMI shows expansion")

            risk_score += pmi_risk

        # 4. Consumer Confidence (15 points)
        max_score += 15
        consumer_indicators = self.db_service.get_economic_indicators(
            country=country,
            category="consumer"
        )

        confidence_ind = next(
            (ind for ind in consumer_indicators
             if "confidence" in ind.indicator_name.lower()),
            None
        )

        if confidence_ind and confidence_ind.last_value_numeric is not None:
            confidence = confidence_ind.last_value_numeric

            if confidence < 80:
                confidence_risk = 15
                risk_factors.append("🚨 Consumer confidence very weak (<80)")
            elif confidence < 90:
                confidence_risk = 10
                risk_factors.append("⚠️ Consumer confidence weak")
            elif confidence < 95:
                confidence_risk = 5
                risk_factors.append("⚠️ Consumer confidence below average")
            else:
                confidence_risk = 0
                risk_factors.append("✅ Consumer confidence strong")

            risk_score += confidence_risk

        # 5. Housing Market (10 points)
        max_score += 10
        housing_indicators = self.db_service.get_economic_indicators(
            country=country,
            category="housing"
        )

        housing_starts_ind = next(
            (ind for ind in housing_indicators
             if "starts" in ind.indicator_name.lower() or "permits" in ind.indicator_name.lower()),
            None
        )

        if housing_starts_ind and housing_starts_ind.last_value_numeric is not None:
            housing_trend = self.trend_analyzer.analyze_trend(
                country,
                housing_starts_ind.indicator_name,
                periods=6
            )

            if "error" not in housing_trend:
                direction = housing_trend.get("trend", {}).get("direction", "flat")

                if direction == "downward":
                    housing_risk = 10
                    risk_factors.append("⚠️ Housing construction declining")
                else:
                    housing_risk = 0
                    risk_factors.append("✅ Housing market stable")

                risk_score += housing_risk

        # 6. Leading Indicators Composite (10 points)
        max_score += 10
        # Check if multiple leading indicators are declining
        leading_declining = sum(1 for factor in risk_factors if "📉" in factor or "🚨" in factor)

        if leading_declining >= 3:
            leading_risk = 10
            risk_factors.append("🚨 Multiple leading indicators declining")
            risk_score += leading_risk
        elif leading_declining >= 2:
            leading_risk = 5
            risk_factors.append("⚠️ Several leading indicators showing weakness")
            risk_score += leading_risk

        # Calculate probability
        if max_score > 0:
            recession_probability = (risk_score / max_score) * 100
        else:
            recession_probability = 0

        # Classification
        if recession_probability < 15:
            risk_level = "low"
            emoji = "✅"
            message = "Low recession risk - economy appears healthy"
        elif recession_probability < 30:
            risk_level = "moderate"
            emoji = "⚠️"
            message = "Moderate recession risk - some warning signs present"
        elif recession_probability < 50:
            risk_level = "elevated"
            emoji = "📊"
            message = "Elevated recession risk - multiple concerning indicators"
        elif recession_probability < 70:
            risk_level = "high"
            emoji = "📉"
            message = "High recession risk - economy showing significant weakness"
        else:
            risk_level = "very_high"
            emoji = "🚨"
            message = "Very high recession risk - recession likely imminent or occurring"

        return {
            "country": country,
            "calculation_date": datetime.now().isoformat(),
            "recession_probability": round(recession_probability, 1),
            "risk_level": risk_level,
            "emoji": emoji,
            "risk_score": risk_score,
            "max_score": max_score,
            "risk_factors": risk_factors,
            "interpretation": message,
            "recommendation": self._get_recession_recommendation(recession_probability)
        }

    def _get_recession_recommendation(self, probability: float) -> str:
        """Get recommendation based on recession probability"""
        if probability < 15:
            return "Continue normal investment activities. Economy is healthy."
        elif probability < 30:
            return "Monitor economic indicators closely. Consider maintaining some cash reserves."
        elif probability < 50:
            return "Exercise caution. Diversify investments and increase emergency savings."
        elif probability < 70:
            return "Reduce risk exposure. Focus on defensive investments and build cash position."
        else:
            return "High risk environment. Prioritize capital preservation and liquidity."

    def calculate_housing_bubble_risk(
        self,
        country: str
    ) -> Dict[str, Any]:
        """
        Calculate housing bubble risk score

        Risk factors:
        - Price-to-income ratio (very high = risky)
        - Price appreciation rate (too fast = risky)
        - Mortgage debt levels
        - Affordability deterioration
        - Speculation indicators

        Args:
            country: Country name

        Returns:
            Dict with bubble risk assessment
        """
        risk_factors = []
        risk_score = 0
        max_score = 0

        # 1. Price-to-Income Ratio (30 points)
        max_score += 30

        housing_indicators = self.db_service.get_economic_indicators(
            country=country,
            category="housing"
        )

        price_ind = next(
            (ind for ind in housing_indicators
             if "price" in ind.indicator_name.lower()),
            None
        )

        gdp_indicators = self.db_service.get_economic_indicators(
            country=country,
            category="gdp"
        )

        gdp_per_capita_ind = next(
            (ind for ind in gdp_indicators
             if "per capita" in ind.indicator_name.lower()),
            None
        )

        if price_ind and gdp_per_capita_ind:
            if price_ind.last_value_numeric and gdp_per_capita_ind.last_value_numeric:
                price_to_income = price_ind.last_value_numeric / gdp_per_capita_ind.last_value_numeric

                if price_to_income > 7:
                    price_risk = 30
                    risk_factors.append(f"🚨 Extreme price-to-income ratio ({price_to_income:.1f}x - severe bubble risk)")
                elif price_to_income > 6:
                    price_risk = 25
                    risk_factors.append(f"⚠️ Very high price-to-income ratio ({price_to_income:.1f}x)")
                elif price_to_income > 5:
                    price_risk = 15
                    risk_factors.append(f"⚠️ High price-to-income ratio ({price_to_income:.1f}x)")
                elif price_to_income > 4:
                    price_risk = 5
                    risk_factors.append(f"📊 Elevated price-to-income ratio ({price_to_income:.1f}x)")
                else:
                    price_risk = 0
                    risk_factors.append(f"✅ Healthy price-to-income ratio ({price_to_income:.1f}x)")

                risk_score += price_risk

        # 2. Price Appreciation Rate (25 points)
        max_score += 25

        if price_ind:
            price_trend = self.trend_analyzer.analyze_trend(
                country,
                price_ind.indicator_name,
                periods=12
            )

            if "error" not in price_trend:
                growth_rates = price_trend.get("growth_rates", {})
                yoy_growth = growth_rates.get("year_over_year", 0)

                if yoy_growth > 15:
                    appreciation_risk = 25
                    risk_factors.append(f"🚨 Extreme price appreciation ({yoy_growth:+.1f}% YoY - bubble warning)")
                elif yoy_growth > 10:
                    appreciation_risk = 20
                    risk_factors.append(f"⚠️ Very rapid price appreciation ({yoy_growth:+.1f}% YoY)")
                elif yoy_growth > 7:
                    appreciation_risk = 10
                    risk_factors.append(f"⚠️ Rapid price appreciation ({yoy_growth:+.1f}% YoY)")
                elif yoy_growth > 4:
                    appreciation_risk = 0
                    risk_factors.append(f"✅ Moderate price appreciation ({yoy_growth:+.1f}% YoY)")
                elif yoy_growth > 0:
                    appreciation_risk = 0
                    risk_factors.append(f"✅ Mild price appreciation ({yoy_growth:+.1f}% YoY)")
                else:
                    appreciation_risk = 0
                    risk_factors.append(f"📉 Prices declining ({yoy_growth:+.1f}% YoY - correction occurring)")

                risk_score += appreciation_risk

        # 3. Mortgage Rates vs Affordability (20 points)
        max_score += 20

        mortgage_ind = next(
            (ind for ind in housing_indicators
             if "mortgage" in ind.indicator_name.lower() and "rate" in ind.indicator_name.lower()),
            None
        )

        if mortgage_ind and mortgage_ind.last_value_numeric:
            mortgage_rate = mortgage_ind.last_value_numeric

            # If rates are low and prices are high, bubble risk increases
            if price_to_income > 5 and mortgage_rate < 4:
                rate_risk = 20
                risk_factors.append("🚨 Low rates fueling price appreciation - correction risk when rates rise")
            elif price_to_income > 5 and mortgage_rate < 5:
                rate_risk = 10
                risk_factors.append("⚠️ Affordable financing supporting high prices")
            else:
                rate_risk = 0
                risk_factors.append("✅ Rate environment appears balanced")

            risk_score += rate_risk

        # 4. Construction Activity (15 points)
        max_score += 15

        permits_ind = next(
            (ind for ind in housing_indicators
             if "permit" in ind.indicator_name.lower() or "starts" in ind.indicator_name.lower()),
            None
        )

        if permits_ind:
            permits_trend = self.trend_analyzer.analyze_trend(
                country,
                permits_ind.indicator_name,
                periods=12
            )

            if "error" not in permits_trend:
                direction = permits_trend.get("trend", {}).get("direction", "flat")
                growth = permits_trend.get("growth_rates", {}).get("year_over_year", 0)

                # Excessive construction can lead to oversupply
                if direction == "upward" and growth > 20:
                    construction_risk = 15
                    risk_factors.append("⚠️ Construction boom - potential oversupply risk")
                elif direction == "downward" and growth < -20:
                    construction_risk = 5
                    risk_factors.append("⚠️ Construction declining sharply - supply concerns")
                else:
                    construction_risk = 0
                    risk_factors.append("✅ Construction activity balanced")

                risk_score += construction_risk

        # 5. Consumer Debt Levels (10 points)
        max_score += 10

        consumer_indicators = self.db_service.get_economic_indicators(
            country=country,
            category="consumer"
        )

        debt_ind = next(
            (ind for ind in consumer_indicators
             if "debt" in ind.indicator_name.lower()),
            None
        )

        if debt_ind and debt_ind.last_value_numeric:
            debt_level = debt_ind.last_value_numeric

            if debt_level > 90:
                debt_risk = 10
                risk_factors.append(f"🚨 Very high consumer debt ({debt_level:.0f}% of income)")
            elif debt_level > 75:
                debt_risk = 5
                risk_factors.append(f"⚠️ Elevated consumer debt ({debt_level:.0f}% of income)")
            else:
                debt_risk = 0
                risk_factors.append(f"✅ Manageable consumer debt ({debt_level:.0f}% of income)")

            risk_score += debt_risk

        # Calculate bubble risk percentage
        if max_score > 0:
            bubble_risk_pct = (risk_score / max_score) * 100
        else:
            bubble_risk_pct = 0

        # Classification
        if bubble_risk_pct < 20:
            risk_level = "low"
            emoji = "✅"
            message = "Low bubble risk - market appears fundamentally sound"
        elif bubble_risk_pct < 40:
            risk_level = "moderate"
            emoji = "⚠️"
            message = "Moderate bubble risk - some froth in market but not extreme"
        elif bubble_risk_pct < 60:
            risk_level = "elevated"
            emoji = "📊"
            message = "Elevated bubble risk - prices detached from fundamentals"
        elif bubble_risk_pct < 80:
            risk_level = "high"
            emoji = "📉"
            message = "High bubble risk - significant correction possible"
        else:
            risk_level = "severe"
            emoji = "🚨"
            message = "Severe bubble risk - market extremely overheated"

        return {
            "country": country,
            "calculation_date": datetime.now().isoformat(),
            "bubble_risk_score": round(bubble_risk_pct, 1),
            "risk_level": risk_level,
            "emoji": emoji,
            "risk_score": risk_score,
            "max_score": max_score,
            "risk_factors": risk_factors,
            "interpretation": message,
            "recommendation": self._get_bubble_recommendation(bubble_risk_pct)
        }

    def _get_bubble_recommendation(self, risk_score: float) -> str:
        """Get recommendation based on bubble risk"""
        if risk_score < 20:
            return "Good time for homebuyers. Market appears healthy."
        elif risk_score < 40:
            return "Exercise normal caution. Market has some risks but not extreme."
        elif risk_score < 60:
            return "Buyers should be cautious. Sellers may want to consider timing."
        elif risk_score < 80:
            return "High risk for buyers. Sellers should seriously consider taking profits."
        else:
            return "Extremely risky for buyers. Sellers strongly advised to consider exiting."

    def calculate_inflation_risk(
        self,
        country: str
    ) -> Dict[str, Any]:
        """
        Calculate inflation risk score

        Args:
            country: Country name

        Returns:
            Dict with inflation risk assessment
        """
        risk_factors = []
        risk_score = 0

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

        if not inflation_ind or inflation_ind.last_value_numeric is None:
            return {"error": "Inflation data not available"}

        current_inflation = inflation_ind.last_value_numeric

        # Analyze inflation trend
        inflation_trend = self.trend_analyzer.analyze_trend(
            country,
            inflation_ind.indicator_name,
            periods=12
        )

        # 1. Current inflation level (40 points)
        if current_inflation > 7:
            level_risk = 40
            risk_factors.append(f"🚨 Very high inflation ({current_inflation:.1f}%)")
        elif current_inflation > 5:
            level_risk = 30
            risk_factors.append(f"⚠️ High inflation ({current_inflation:.1f}%)")
        elif current_inflation > 3.5:
            level_risk = 20
            risk_factors.append(f"⚠️ Elevated inflation ({current_inflation:.1f}%)")
        elif current_inflation > 2.5:
            level_risk = 5
            risk_factors.append(f"📊 Slightly above target ({current_inflation:.1f}%)")
        elif current_inflation > 1.5:
            level_risk = 0
            risk_factors.append(f"✅ Near target ({current_inflation:.1f}%)")
        elif current_inflation > 0:
            level_risk = 10
            risk_factors.append(f"⚠️ Below target ({current_inflation:.1f}%)")
        else:
            level_risk = 30
            risk_factors.append(f"🚨 Deflation ({current_inflation:.1f}%)")

        risk_score += level_risk

        # 2. Inflation trend (30 points)
        if "error" not in inflation_trend:
            direction = inflation_trend.get("trend", {}).get("direction", "flat")
            momentum = inflation_trend.get("momentum", {}).get("classification", "neutral")

            if direction == "upward" and current_inflation > 5:
                trend_risk = 30
                risk_factors.append("🚨 Inflation accelerating from high levels")
            elif direction == "upward" and current_inflation > 3:
                trend_risk = 20
                risk_factors.append("⚠️ Inflation trending upward")
            elif direction == "downward" and current_inflation > 3:
                trend_risk = 10
                risk_factors.append("📊 Inflation declining but still elevated")
            elif direction == "downward":
                trend_risk = 0
                risk_factors.append("✅ Inflation trending downward")
            else:
                trend_risk = 5
                risk_factors.append("📊 Inflation stable")

            risk_score += trend_risk

        # 3. Volatility (15 points)
        if "error" not in inflation_trend:
            volatility = inflation_trend.get("volatility", {}).get("classification", "stable")

            if volatility == "highly_volatile":
                vol_risk = 15
                risk_factors.append("⚠️ Inflation highly volatile - uncertain environment")
            elif volatility == "volatile":
                vol_risk = 10
                risk_factors.append("⚠️ Inflation volatile")
            else:
                vol_risk = 0
                risk_factors.append("✅ Inflation stable")

            risk_score += vol_risk

        # 4. Central bank response (15 points)
        money_indicators = self.db_service.get_economic_indicators(
            country=country,
            category="money"
        )

        interest_rate_ind = next(
            (ind for ind in money_indicators
             if "interest rate" in ind.indicator_name.lower()),
            None
        )

        if interest_rate_ind and interest_rate_ind.last_value_numeric:
            policy_rate = interest_rate_ind.last_value_numeric

            # Real interest rate = nominal rate - inflation
            real_rate = policy_rate - current_inflation

            if real_rate < -2:
                policy_risk = 15
                risk_factors.append(f"🚨 Very negative real rates ({real_rate:.1f}%) - insufficient tightening")
            elif real_rate < 0:
                policy_risk = 10
                risk_factors.append(f"⚠️ Negative real rates ({real_rate:.1f}%)")
            elif real_rate > 2:
                policy_risk = 0
                risk_factors.append(f"✅ Positive real rates ({real_rate:.1f}%) - restrictive policy")
            else:
                policy_risk = 5
                risk_factors.append(f"📊 Slightly positive real rates ({real_rate:.1f}%)")

            risk_score += policy_risk

        # Classify risk
        if risk_score < 20:
            risk_level = "low"
            emoji = "✅"
        elif risk_score < 40:
            risk_level = "moderate"
            emoji = "⚠️"
        elif risk_score < 60:
            risk_level = "elevated"
            emoji = "📊"
        elif risk_score < 80:
            risk_level = "high"
            emoji = "📉"
        else:
            risk_level = "severe"
            emoji = "🚨"

        return {
            "country": country,
            "calculation_date": datetime.now().isoformat(),
            "inflation_risk_score": round(risk_score, 1),
            "risk_level": risk_level,
            "emoji": emoji,
            "current_inflation": round(current_inflation, 2),
            "risk_factors": risk_factors,
            "interpretation": f"Inflation risk is {risk_level} with current inflation at {current_inflation:.1f}%"
        }
