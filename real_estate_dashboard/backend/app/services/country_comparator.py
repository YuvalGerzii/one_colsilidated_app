"""
Country Economic Comparator

Enables comprehensive comparison of economic indicators across multiple countries.
Uses Purchasing Power Parity (PPP) adjustments where applicable.

Key comparison metrics:
- GDP per capita (PPP-adjusted)
- Unemployment rates
- Inflation rates
- Housing affordability
- Economic growth trajectories
- Debt levels
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import statistics

from app.database.country_database_manager import country_db_manager
from app.services.economics_db_service import EconomicsDBService
from app.services.economic_analyzer import EconomicAnalyzer

logger = logging.getLogger(__name__)


class CountryComparator:
    """Compare economic indicators across multiple countries"""

    # PPP conversion factors (USD = 1.0 baseline)
    # Source: OECD, IMF - approximate 2025 values
    PPP_FACTORS = {
        "United States": 1.0,
        "China": 0.58,
        "Euro Area": 0.88,
        "Japan": 0.73,
        "Germany": 0.86,
        "India": 0.28,
        "United Kingdom": 0.78,
        "France": 0.87,
        "Russia": 0.45,
        "Canada": 0.82,
        "Italy": 0.85,
        "Brazil": 0.52,
        "Australia": 0.72,
        "South Korea": 0.68,
        "Mexico": 0.53,
        "Spain": 0.83,
        "Indonesia": 0.35,
        "Saudi Arabia": 0.64,
        "Netherlands": 0.84,
        "Turkey": 0.41,
        "Switzerland": 0.67,
        "Taiwan": 0.62,
        "Poland": 0.55,
    }

    def __init__(self):
        """Initialize comparator"""
        self.analyzers: Dict[str, Tuple[EconomicsDBService, EconomicAnalyzer]] = {}

    def _get_country_analyzer(
        self,
        country_slug: str
    ) -> Tuple[EconomicsDBService, EconomicAnalyzer]:
        """Get or create analyzer for a country"""
        if country_slug not in self.analyzers:
            db = country_db_manager.get_session(country_slug)
            db_service = EconomicsDBService(db)
            analyzer = EconomicAnalyzer(db_service)
            self.analyzers[country_slug] = (db_service, analyzer)

        return self.analyzers[country_slug]

    def _get_country_slug(self, country_name: str) -> str:
        """Convert country name to slug"""
        return country_name.lower().replace(" ", "-")

    def compare_indicator(
        self,
        countries: List[str],
        indicator_name: str,
        category: str
    ) -> Dict[str, Any]:
        """
        Compare a specific indicator across countries

        Args:
            countries: List of country names
            indicator_name: Name of the indicator
            category: Category (gdp, labour, housing, etc.)

        Returns:
            Dict with comparison data
        """
        comparison = {
            "indicator": indicator_name,
            "category": category,
            "comparison_date": datetime.now().isoformat(),
            "countries": {},
            "rankings": {},
            "insights": []
        }

        values = {}

        for country in countries:
            country_slug = self._get_country_slug(country)
            db_service, analyzer = self._get_country_analyzer(country_slug)

            # Get indicator data
            indicators = db_service.get_economic_indicators(
                country=country,
                category=category
            )

            # Find matching indicator
            indicator_data = next(
                (ind for ind in indicators if indicator_name.lower() in ind.indicator_name.lower()),
                None
            )

            if indicator_data and indicator_data.last_value_numeric is not None:
                values[country] = {
                    "value": indicator_data.last_value_numeric,
                    "value_string": indicator_data.last_value,
                    "unit": indicator_data.unit,
                    "date": indicator_data.data_date.isoformat() if indicator_data.data_date else None
                }

                # Get interpretation
                interp = analyzer.interpret_indicator(
                    indicator_data.indicator_name,
                    indicator_data.last_value_numeric
                )

                values[country]["interpretation"] = interp

        comparison["countries"] = values

        # Generate rankings
        if values:
            comparison["rankings"] = self._generate_rankings(values, indicator_name)
            comparison["insights"] = self._generate_comparison_insights(
                values,
                indicator_name,
                comparison["rankings"]
            )

        return comparison

    def _generate_rankings(
        self,
        values: Dict[str, Dict],
        indicator_name: str
    ) -> Dict[str, Any]:
        """Generate rankings and statistics"""
        numeric_values = {
            country: data["value"]
            for country, data in values.items()
            if data["value"] is not None
        }

        if not numeric_values:
            return {}

        # Determine if higher is better
        higher_is_better = self._is_higher_better(indicator_name)

        # Sort countries
        sorted_countries = sorted(
            numeric_values.items(),
            key=lambda x: x[1],
            reverse=higher_is_better
        )

        rankings = {
            "ranked_list": [
                {
                    "rank": idx + 1,
                    "country": country,
                    "value": value
                }
                for idx, (country, value) in enumerate(sorted_countries)
            ],
            "highest": {
                "country": sorted_countries[0][0],
                "value": sorted_countries[0][1]
            },
            "lowest": {
                "country": sorted_countries[-1][0],
                "value": sorted_countries[-1][1]
            },
            "average": statistics.mean(numeric_values.values()),
            "median": statistics.median(numeric_values.values()),
            "std_dev": statistics.stdev(numeric_values.values()) if len(numeric_values) > 1 else 0,
            "higher_is_better": higher_is_better
        }

        # Calculate spread
        rankings["spread"] = sorted_countries[0][1] - sorted_countries[-1][1]
        rankings["spread_pct"] = (rankings["spread"] / sorted_countries[-1][1] * 100) if sorted_countries[-1][1] != 0 else 0

        return rankings

    def _is_higher_better(self, indicator_name: str) -> bool:
        """Determine if higher values are better for this indicator"""
        indicator_lower = indicator_name.lower()

        # Lower is better for these
        if any(word in indicator_lower for word in [
            "unemployment", "inflation", "debt", "deficit",
            "mortgage rate", "interest rate", "poverty"
        ]):
            return False

        # Higher is better for most others
        return True

    def _generate_comparison_insights(
        self,
        values: Dict[str, Dict],
        indicator_name: str,
        rankings: Dict[str, Any]
    ) -> List[str]:
        """Generate insights from comparison"""
        insights = []

        if not rankings:
            return insights

        highest = rankings["highest"]
        lowest = rankings["lowest"]
        avg = rankings["average"]
        spread_pct = rankings["spread_pct"]

        # Spread insight
        if spread_pct > 100:
            insights.append(
                f"Large variation: {highest['country']} has {spread_pct:.0f}% higher "
                f"{indicator_name} than {lowest['country']}, indicating significant differences."
            )
        elif spread_pct > 50:
            insights.append(
                f"Moderate variation: {spread_pct:.0f}% spread across countries."
            )
        else:
            insights.append(
                f"Low variation: Countries show similar {indicator_name} levels (±{spread_pct:.0f}%)."
            )

        # Leader insight
        if rankings["higher_is_better"]:
            insights.append(
                f"📊 {highest['country']} leads with the highest {indicator_name} at {highest['value']:.2f}."
            )
        else:
            insights.append(
                f"📊 {lowest['country']} performs best with the lowest {indicator_name} at {lowest['value']:.2f}."
            )

        # Outlier detection
        for country, data in values.items():
            value = data["value"]
            deviation = ((value - avg) / avg) * 100 if avg != 0 else 0

            if abs(deviation) > 50:
                if deviation > 0:
                    insights.append(
                        f"⚠️ {country} is {abs(deviation):.0f}% above average, indicating an outlier."
                    )
                else:
                    insights.append(
                        f"⚠️ {country} is {abs(deviation):.0f}% below average, indicating an outlier."
                    )

        return insights

    def compare_multiple_indicators(
        self,
        countries: List[str],
        indicators: List[Tuple[str, str]]  # [(indicator_name, category), ...]
    ) -> Dict[str, Any]:
        """
        Compare multiple indicators across countries

        Args:
            countries: List of country names
            indicators: List of (indicator_name, category) tuples

        Returns:
            Dict with multi-indicator comparison
        """
        comparison = {
            "countries": countries,
            "indicators": [],
            "comparison_date": datetime.now().isoformat(),
            "country_scores": {}
        }

        # Compare each indicator
        for indicator_name, category in indicators:
            indicator_comp = self.compare_indicator(countries, indicator_name, category)
            comparison["indicators"].append(indicator_comp)

        # Calculate overall scores
        comparison["country_scores"] = self._calculate_country_scores(
            countries,
            comparison["indicators"]
        )

        return comparison

    def _calculate_country_scores(
        self,
        countries: List[str],
        indicator_comparisons: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Calculate overall scores for each country"""
        scores = {country: [] for country in countries}

        for comp in indicator_comparisons:
            rankings = comp.get("rankings", {})
            if not rankings or not rankings.get("ranked_list"):
                continue

            total_countries = len(rankings["ranked_list"])

            # Assign points based on ranking (100 for 1st, decreasing)
            for ranked in rankings["ranked_list"]:
                country = ranked["country"]
                rank = ranked["rank"]

                # Score: 100 * (total - rank + 1) / total
                score = 100 * (total_countries - rank + 1) / total_countries
                scores[country].append(score)

        # Calculate average scores
        result = {}
        for country, country_scores in scores.items():
            if country_scores:
                result[country] = {
                    "average_score": round(statistics.mean(country_scores), 1),
                    "indicators_ranked": len(country_scores),
                    "consistency": round(100 - statistics.stdev(country_scores), 1) if len(country_scores) > 1 else 100
                }

        # Rank countries by score
        sorted_scores = sorted(
            result.items(),
            key=lambda x: x[1]["average_score"],
            reverse=True
        )

        for idx, (country, data) in enumerate(sorted_scores):
            data["overall_rank"] = idx + 1

        return result

    def compare_gdp_per_capita_ppp(
        self,
        countries: List[str]
    ) -> Dict[str, Any]:
        """
        Compare GDP per capita with PPP adjustment

        Args:
            countries: List of country names

        Returns:
            Dict with PPP-adjusted comparison
        """
        comparison = {
            "metric": "GDP per Capita (PPP-adjusted)",
            "comparison_date": datetime.now().isoformat(),
            "countries": {},
            "explanation": (
                "PPP (Purchasing Power Parity) adjusts GDP per capita for price differences "
                "between countries, providing a better comparison of living standards."
            )
        }

        for country in countries:
            country_slug = self._get_country_slug(country)
            db_service, _ = self._get_country_analyzer(country_slug)

            # Get GDP per capita
            indicators = db_service.get_economic_indicators(
                country=country,
                category="gdp"
            )

            gdp_per_capita = next(
                (ind for ind in indicators if "per capita" in ind.indicator_name.lower()),
                None
            )

            if gdp_per_capita and gdp_per_capita.last_value_numeric:
                nominal_value = gdp_per_capita.last_value_numeric

                # Apply PPP adjustment
                ppp_factor = self.PPP_FACTORS.get(country, 1.0)
                ppp_adjusted = nominal_value / ppp_factor

                comparison["countries"][country] = {
                    "nominal_gdp_per_capita": nominal_value,
                    "ppp_factor": ppp_factor,
                    "ppp_adjusted_gdp_per_capita": round(ppp_adjusted, 2),
                    "unit": gdp_per_capita.unit
                }

        # Generate rankings
        if comparison["countries"]:
            ppp_values = {
                country: data["ppp_adjusted_gdp_per_capita"]
                for country, data in comparison["countries"].items()
            }

            sorted_countries = sorted(
                ppp_values.items(),
                key=lambda x: x[1],
                reverse=True
            )

            comparison["rankings"] = [
                {
                    "rank": idx + 1,
                    "country": country,
                    "ppp_adjusted_value": value
                }
                for idx, (country, value) in enumerate(sorted_countries)
            ]

            # Insights
            comparison["insights"] = [
                f"🥇 {sorted_countries[0][0]} has the highest PPP-adjusted GDP per capita at ${sorted_countries[0][1]:,.0f}",
                f"Living standards comparison: {sorted_countries[0][0]} is {((sorted_countries[0][1] / sorted_countries[-1][1]) - 1) * 100:.0f}% higher than {sorted_countries[-1][0]}"
            ]

        return comparison

    def compare_housing_affordability(
        self,
        countries: List[str]
    ) -> Dict[str, Any]:
        """
        Compare housing affordability across countries

        Calculates price-to-income ratio and mortgage burden

        Args:
            countries: List of country names

        Returns:
            Dict with affordability comparison
        """
        comparison = {
            "metric": "Housing Affordability",
            "comparison_date": datetime.now().isoformat(),
            "countries": {},
            "explanation": (
                "Housing affordability is measured by the price-to-income ratio and "
                "mortgage payment as percentage of income. Lower ratios indicate better affordability."
            )
        }

        for country in countries:
            country_slug = self._get_country_slug(country)
            db_service, _ = self._get_country_analyzer(country_slug)

            # Get housing and income data
            housing_indicators = db_service.get_economic_indicators(
                country=country,
                category="housing"
            )

            gdp_indicators = db_service.get_economic_indicators(
                country=country,
                category="gdp"
            )

            # Find house prices
            house_price = next(
                (ind for ind in housing_indicators if "house price" in ind.indicator_name.lower()
                 or "home price" in ind.indicator_name.lower()),
                None
            )

            # Find mortgage rate
            mortgage_rate = next(
                (ind for ind in housing_indicators if "mortgage rate" in ind.indicator_name.lower()),
                None
            )

            # Find GDP per capita (proxy for income)
            gdp_per_capita = next(
                (ind for ind in gdp_indicators if "per capita" in ind.indicator_name.lower()),
                None
            )

            if house_price and gdp_per_capita:
                price_to_income = house_price.last_value_numeric / gdp_per_capita.last_value_numeric

                data = {
                    "average_house_price": house_price.last_value_numeric,
                    "gdp_per_capita": gdp_per_capita.last_value_numeric,
                    "price_to_income_ratio": round(price_to_income, 2)
                }

                if mortgage_rate and mortgage_rate.last_value_numeric:
                    data["mortgage_rate"] = mortgage_rate.last_value_numeric

                    # Estimate monthly payment burden (simplified)
                    # Assumes 30-year mortgage, 20% down payment
                    loan_amount = house_price.last_value_numeric * 0.8
                    monthly_rate = mortgage_rate.last_value_numeric / 100 / 12
                    n_payments = 360  # 30 years

                    if monthly_rate > 0:
                        monthly_payment = loan_amount * (
                            monthly_rate * (1 + monthly_rate) ** n_payments
                        ) / ((1 + monthly_rate) ** n_payments - 1)

                        monthly_income = gdp_per_capita.last_value_numeric / 12
                        payment_to_income = (monthly_payment / monthly_income) * 100

                        data["monthly_payment_estimate"] = round(monthly_payment, 2)
                        data["payment_to_income_pct"] = round(payment_to_income, 1)

                comparison["countries"][country] = data

        # Generate affordability rankings
        if comparison["countries"]:
            # Rank by price-to-income (lower is better)
            affordability_scores = {
                country: data["price_to_income_ratio"]
                for country, data in comparison["countries"].items()
            }

            sorted_countries = sorted(affordability_scores.items(), key=lambda x: x[1])

            comparison["rankings"] = [
                {
                    "rank": idx + 1,
                    "country": country,
                    "price_to_income_ratio": ratio,
                    "affordability": "Excellent" if ratio < 3 else
                                   "Good" if ratio < 4 else
                                   "Moderate" if ratio < 5 else
                                   "Poor" if ratio < 6 else "Very Poor"
                }
                for idx, (country, ratio) in enumerate(sorted_countries)
            ]

            # Insights
            most_affordable = sorted_countries[0]
            least_affordable = sorted_countries[-1]

            comparison["insights"] = [
                f"🏠 Most affordable: {most_affordable[0]} (price-to-income ratio: {most_affordable[1]:.1f})",
                f"💰 Least affordable: {least_affordable[0]} (price-to-income ratio: {least_affordable[1]:.1f})",
            ]

            # Payment burden insight
            payment_data = {
                country: data.get("payment_to_income_pct", 0)
                for country, data in comparison["countries"].items()
                if "payment_to_income_pct" in data
            }

            if payment_data:
                avg_payment_burden = statistics.mean(payment_data.values())
                comparison["insights"].append(
                    f"📊 Average mortgage payment is {avg_payment_burden:.1f}% of monthly income across countries"
                )

        return comparison
