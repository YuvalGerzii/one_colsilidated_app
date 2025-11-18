"""
Inflation and Real Value Calculators

Calculate inflation-adjusted values and real returns:
- Historical inflation adjustment
- Real vs nominal returns
- Purchasing power calculator
- Future value projections
- Real wage growth
- Asset appreciation vs inflation
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import statistics

from app.services.economics_db_service import EconomicsDBService

logger = logging.getLogger(__name__)


class InflationCalculator:
    """Calculate inflation-adjusted values and real returns"""

    def __init__(self, db_service: EconomicsDBService):
        self.db_service = db_service

    def adjust_for_inflation(
        self,
        country: str,
        amount: float,
        from_year: int,
        to_year: int,
        annual_inflation_rate: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Adjust amount for inflation between two years

        Args:
            country: Country name
            amount: Original amount
            from_year: Starting year
            to_year: Ending year
            annual_inflation_rate: Optional fixed rate; if None, uses actual data

        Returns:
            Dict with inflation-adjusted value
        """
        if annual_inflation_rate is not None:
            # Use provided rate
            years = to_year - from_year
            adjusted_amount = amount * ((1 + annual_inflation_rate / 100) ** years)
            cumulative_inflation = ((adjusted_amount / amount) - 1) * 100

            return {
                "original_amount": amount,
                "from_year": from_year,
                "to_year": to_year,
                "inflation_rate_used": annual_inflation_rate,
                "adjusted_amount": round(adjusted_amount, 2),
                "cumulative_inflation": round(cumulative_inflation, 1),
                "purchasing_power_change": round(-cumulative_inflation, 1),
                "interpretation": (
                    f"${amount:,.0f} in {from_year} has the same purchasing power as "
                    f"${adjusted_amount:,.0f} in {to_year} (using {annual_inflation_rate}% annual inflation). "
                    f"Purchasing power decreased by {cumulative_inflation:.1f}%."
                )
            }

        else:
            # Use actual historical data
            # For now, use simplified calculation
            # In production, would fetch actual historical inflation data
            return {
                "error": "Historical inflation data lookup not yet implemented",
                "suggestion": "Provide annual_inflation_rate parameter for calculation"
            }

    def calculate_real_vs_nominal(
        self,
        country: str,
        nominal_return: float,
        time_period_years: int = 1
    ) -> Dict[str, Any]:
        """
        Calculate real return after accounting for inflation

        Real Return = ((1 + Nominal Return) / (1 + Inflation)) - 1

        Args:
            country: Country name
            nominal_return: Nominal return rate (e.g., 7 for 7%)
            time_period_years: Period in years

        Returns:
            Dict with real vs nominal comparison
        """
        # Get current inflation rate
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

        inflation_rate = inflation_ind.last_value_numeric

        # Calculate real return
        real_return = ((1 + nominal_return / 100) / (1 + inflation_rate / 100) - 1) * 100

        # Example calculations
        initial_investment = 100000
        nominal_value = initial_investment * ((1 + nominal_return / 100) ** time_period_years)
        real_value = initial_investment * ((1 + real_return / 100) ** time_period_years)
        inflation_erosion = nominal_value - real_value

        return {
            "country": country,
            "time_period_years": time_period_years,
            "nominal_return": nominal_return,
            "inflation_rate": round(inflation_rate, 2),
            "real_return": round(real_return, 2),
            "example_investment": {
                "initial": initial_investment,
                "nominal_value": round(nominal_value, 2),
                "real_value": round(real_value, 2),
                "inflation_erosion": round(inflation_erosion, 2)
            },
            "interpretation": (
                f"A {nominal_return}% nominal return with {inflation_rate:.1f}% inflation "
                f"equals a {real_return:.2f}% real return. "
                f"On ${initial_investment:,.0f}, inflation erodes ${inflation_erosion:,.0f} "
                f"of purchasing power over {time_period_years} year(s)."
            )
        }

    def calculate_purchasing_power(
        self,
        country: str,
        amount: float,
        years_forward: int = 10
    ) -> Dict[str, Any]:
        """
        Calculate future purchasing power of money

        Args:
            country: Country name
            amount: Current amount
            years_forward: Years to project

        Returns:
            Dict with purchasing power projection
        """
        # Get current inflation rate
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

        # Get historical inflation for trend
        history = self.db_service.get_indicator_history(
            country=country,
            indicator_name=inflation_ind.indicator_name,
            limit=12
        )

        if len(history) >= 3:
            historical_rates = [h.value_numeric for h in history if h.value_numeric is not None]
            avg_inflation = statistics.mean(historical_rates)
        else:
            avg_inflation = current_inflation

        # Project purchasing power using both current and average inflation
        projections = []

        for year in range(1, years_forward + 1):
            # Using current inflation
            current_scenario = amount / ((1 + current_inflation / 100) ** year)

            # Using average inflation
            avg_scenario = amount / ((1 + avg_inflation / 100) ** year)

            # Purchasing power loss
            current_loss_pct = ((amount - current_scenario) / amount) * 100
            avg_loss_pct = ((amount - avg_scenario) / amount) * 100

            projections.append({
                "year": year,
                "purchasing_power_current_inflation": round(current_scenario, 2),
                "purchasing_power_avg_inflation": round(avg_scenario, 2),
                "loss_percentage_current": round(current_loss_pct, 1),
                "loss_percentage_avg": round(avg_loss_pct, 1)
            })

        return {
            "country": country,
            "current_amount": amount,
            "current_inflation": round(current_inflation, 2),
            "average_inflation": round(avg_inflation, 2),
            "projections": projections[:5] + projections[-1:] if len(projections) > 6 else projections,
            "key_insights": {
                "year_5_loss_current": round(projections[4]["loss_percentage_current"], 1),
                "year_10_loss_current": round(projections[-1]["loss_percentage_current"], 1),
                "equivalent_buying_power_year_10": round(projections[-1]["purchasing_power_current_inflation"], 2)
            },
            "interpretation": (
                f"${amount:,.0f} today will have the purchasing power of "
                f"${projections[-1]['purchasing_power_current_inflation']:,.0f} in {years_forward} years "
                f"at current {current_inflation:.1f}% inflation rate. "
                f"That's a {projections[-1]['loss_percentage_current']:.1f}% loss in purchasing power."
            )
        }

    def calculate_real_wage_growth(
        self,
        country: str,
        periods: int = 12
    ) -> Dict[str, Any]:
        """
        Calculate real wage growth (wage growth - inflation)

        Args:
            country: Country name
            periods: Number of historical periods to analyze

        Returns:
            Dict with real wage growth analysis
        """
        # Get wage growth data
        labour_indicators = self.db_service.get_economic_indicators(
            country=country,
            category="labour"
        )

        wage_ind = next(
            (ind for ind in labour_indicators
             if "wage" in ind.indicator_name.lower()),
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

        if not wage_ind or not inflation_ind:
            return {"error": "Missing wage or inflation data"}

        # Get historical data
        wage_history = self.db_service.get_indicator_history(
            country=country,
            indicator_name=wage_ind.indicator_name,
            limit=periods
        )

        inflation_history = self.db_service.get_indicator_history(
            country=country,
            indicator_name=inflation_ind.indicator_name,
            limit=periods
        )

        if len(wage_history) < 2 or len(inflation_history) < 2:
            return {"error": "Insufficient historical data"}

        # Calculate real wage growth
        real_wage_data = []

        for wage_point, inflation_point in zip(wage_history, inflation_history):
            if wage_point.value_numeric is not None and inflation_point.value_numeric is not None:
                nominal_wage = wage_point.value_numeric
                inflation = inflation_point.value_numeric

                # Real wage growth ≈ nominal wage growth - inflation
                # (Simplified; exact formula is ((1+nominal)/(1+inflation))-1)
                real_wage_growth = nominal_wage - inflation

                real_wage_data.append({
                    "date": wage_point.observation_date.isoformat() if wage_point.observation_date else None,
                    "nominal_wage_growth": round(nominal_wage, 2),
                    "inflation": round(inflation, 2),
                    "real_wage_growth": round(real_wage_growth, 2),
                    "purchasing_power": "increasing" if real_wage_growth > 0 else "decreasing"
                })

        if not real_wage_data:
            return {"error": "Unable to calculate real wage growth"}

        # Summary statistics
        real_growth_values = [d["real_wage_growth"] for d in real_wage_data]
        avg_real_growth = statistics.mean(real_growth_values)
        current_real_growth = real_growth_values[0]

        # Count periods of positive vs negative real growth
        positive_periods = sum(1 for x in real_growth_values if x > 0)
        negative_periods = len(real_growth_values) - positive_periods

        return {
            "country": country,
            "periods_analyzed": len(real_wage_data),
            "current": {
                "nominal_wage_growth": real_wage_data[0]["nominal_wage_growth"],
                "inflation": real_wage_data[0]["inflation"],
                "real_wage_growth": current_real_growth
            },
            "historical_average": round(avg_real_growth, 2),
            "trend": {
                "positive_periods": positive_periods,
                "negative_periods": negative_periods,
                "percentage_positive": round((positive_periods / len(real_wage_data)) * 100, 1)
            },
            "recent_data": real_wage_data[:6],
            "interpretation": (
                f"Real wage growth is {current_real_growth:+.2f}% (wages growing at "
                f"{real_wage_data[0]['nominal_wage_growth']:.1f}%, inflation at "
                f"{real_wage_data[0]['inflation']:.1f}%). "
                f"{'✅ Workers gaining purchasing power.' if current_real_growth > 0 else '⚠️ Workers losing purchasing power.'} "
                f"Average real growth over period: {avg_real_growth:+.2f}%."
            )
        }

    def calculate_asset_real_return(
        self,
        country: str,
        asset_name: str,
        category: str,
        periods: int = 12
    ) -> Dict[str, Any]:
        """
        Calculate real return of an asset (e.g., house prices) after inflation

        Args:
            country: Country name
            asset_name: Asset indicator name (e.g., "House Prices")
            category: Category (e.g., "housing")
            periods: Periods to analyze

        Returns:
            Dict with real return analysis
        """
        # Get asset data
        asset_indicators = self.db_service.get_economic_indicators(
            country=country,
            category=category
        )

        asset_ind = next(
            (ind for ind in asset_indicators
             if asset_name.lower() in ind.indicator_name.lower()),
            None
        )

        if not asset_ind:
            return {"error": f"Asset '{asset_name}' not found in category '{category}'"}

        # Get asset history
        asset_history = self.db_service.get_indicator_history(
            country=country,
            indicator_name=asset_ind.indicator_name,
            limit=periods
        )

        if len(asset_history) < 2:
            return {"error": "Insufficient asset history"}

        # Get inflation
        price_indicators = self.db_service.get_economic_indicators(
            country=country,
            category="prices"
        )

        inflation_ind = next(
            (ind for ind in price_indicators
             if "inflation" in ind.indicator_name.lower()),
            None
        )

        if not inflation_ind:
            return {"error": "Inflation data not available"}

        inflation_history = self.db_service.get_indicator_history(
            country=country,
            indicator_name=inflation_ind.indicator_name,
            limit=periods
        )

        # Calculate nominal and real returns
        real_returns = []

        for i in range(len(asset_history) - 1):
            current = asset_history[i].value_numeric
            previous = asset_history[i + 1].value_numeric

            if current and previous and previous != 0:
                nominal_return = ((current - previous) / previous) * 100

                # Get corresponding inflation
                if i < len(inflation_history):
                    inflation = inflation_history[i].value_numeric or 0
                else:
                    inflation = 0

                # Real return
                real_return = nominal_return - inflation

                real_returns.append({
                    "date": asset_history[i].observation_date.isoformat() if asset_history[i].observation_date else None,
                    "nominal_return": round(nominal_return, 2),
                    "inflation": round(inflation, 2),
                    "real_return": round(real_return, 2)
                })

        if not real_returns:
            return {"error": "Unable to calculate returns"}

        # Summary
        real_return_values = [r["real_return"] for r in real_returns]
        avg_real_return = statistics.mean(real_return_values)
        avg_nominal_return = statistics.mean([r["nominal_return"] for r in real_returns])

        # Cumulative returns
        cumulative_nominal = 1
        cumulative_real = 1

        for r in reversed(real_returns):
            cumulative_nominal *= (1 + r["nominal_return"] / 100)
            cumulative_real *= (1 + r["real_return"] / 100)

        cumulative_nominal_pct = (cumulative_nominal - 1) * 100
        cumulative_real_pct = (cumulative_real - 1) * 100

        return {
            "country": country,
            "asset": asset_name,
            "category": category,
            "periods_analyzed": len(real_returns),
            "average_returns": {
                "nominal": round(avg_nominal_return, 2),
                "real": round(avg_real_return, 2),
                "inflation_drag": round(avg_nominal_return - avg_real_return, 2)
            },
            "cumulative_returns": {
                "nominal": round(cumulative_nominal_pct, 1),
                "real": round(cumulative_real_pct, 1)
            },
            "recent_data": real_returns[:6],
            "interpretation": (
                f"{asset_name} has returned {avg_nominal_return:+.2f}% nominally but "
                f"{avg_real_return:+.2f}% in real terms (after inflation). "
                f"Over the period, cumulative real return is {cumulative_real_pct:+.1f}% vs "
                f"{cumulative_nominal_pct:+.1f}% nominal."
            )
        }
