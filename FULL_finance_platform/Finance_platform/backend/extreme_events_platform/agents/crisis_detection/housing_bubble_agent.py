"""
Housing Bubble Detection Agent (V6.0)

Detects housing bubbles before they crash.

2006-2008 Housing Bubble Warning Signs:
- Price-to-income ratio: 6.5 (historical avg: 4.0) = 63% overvalued
- Price-to-rent ratio: 25 (historical avg: 15-18) = bubble
- Mortgage debt-to-GDP: 70% (normal: 50%)
- Subprime originations: 20% of all mortgages
- Adjustable rate mortgages: 35% of new mortgages (teaser rates)
- Home ownership rate: 69% (pushed beyond natural level)
- Speculative purchases: 40% of new purchases (not primary residence)
- Cash-out refinancing: $300B/year (equity extraction)

Current bubbles to watch (2025):
- Canadian housing (Toronto, Vancouver): Price-to-income >10
- Australian housing: Debt-to-GDP >120%
- Chinese property sector: Evergrande collapse
"""

from typing import Dict, List
from dataclasses import dataclass


@dataclass
class HousingMarketData:
    """Housing market indicators"""
    price_to_income_ratio: float
    price_to_rent_ratio: float
    mortgage_debt_to_gdp: float
    home_ownership_rate: float
    speculative_purchases_pct: float
    adjustable_rate_pct: float
    subprime_pct: float
    price_growth_yoy: float
    months_of_supply: float
    affordability_index: float


class HousingBubbleAgent:
    """Detects housing bubbles"""

    def __init__(self, config: Dict = None):
        self.config = config or {}

        # Historical averages (US)
        self.historical_avg = {
            'price_to_income': 4.0,
            'price_to_rent': 16.0,
            'mortgage_debt_to_gdp': 50.0,
            'home_ownership_rate': 65.0,
            'speculative_purchases': 10.0,
            'months_of_supply': 6.0,
        }

        # Bubble thresholds
        self.thresholds = {
            'price_to_income': {
                'yellow': 5.0,  # 25% overvalued
                'red': 6.0,  # 50% overvalued (2006 level)
                'weight': 0.25
            },
            'price_to_rent': {
                'yellow': 20.0,
                'red': 24.0,  # 2006 level
                'weight': 0.20
            },
            'mortgage_debt_to_gdp': {
                'yellow': 60.0,
                'red': 70.0,  # 2006 level
                'weight': 0.20
            },
            'price_growth_yoy': {
                'yellow': 10.0,  # % per year
                'red': 15.0,  # Unsustainable
                'weight': 0.15
            },
            'speculative_purchases_pct': {
                'yellow': 25.0,  # % of purchases
                'red': 35.0,  # Too much speculation
                'weight': 0.10
            },
            'adjustable_rate_pct': {
                'yellow': 25.0,
                'red': 35.0,  # Lots of rate reset risk
                'weight': 0.10
            }
        }

    def analyze_event(self, event_data: Dict) -> Dict:
        """Analyze housing market for bubble"""

        # Extract data
        data = HousingMarketData(
            price_to_income_ratio=event_data.get('price_to_income_ratio', 4.0),
            price_to_rent_ratio=event_data.get('price_to_rent_ratio', 16.0),
            mortgage_debt_to_gdp=event_data.get('mortgage_debt_to_gdp', 50.0),
            home_ownership_rate=event_data.get('home_ownership_rate', 65.0),
            speculative_purchases_pct=event_data.get('speculative_purchases_pct', 10.0),
            adjustable_rate_pct=event_data.get('adjustable_rate_pct', 15.0),
            subprime_pct=event_data.get('subprime_pct', 5.0),
            price_growth_yoy=event_data.get('price_growth_yoy', 3.0),
            months_of_supply=event_data.get('months_of_supply', 6.0),
            affordability_index=event_data.get('affordability_index', 100.0)
        )

        # Calculate bubble probability
        bubble_prob = self._calculate_bubble_probability(data)

        # Estimate crash timeline
        crash_timeline = self._estimate_crash_timeline(data, bubble_prob)

        # Trading strategies
        trades = self._generate_strategies(bubble_prob, crash_timeline)

        return {
            'bubble_probability': bubble_prob,
            'estimated_months_until_crash': crash_timeline,
            'overvaluation_pct': self._calculate_overvaluation(data),
            'warnings': self._generate_warnings(data, bubble_prob),
            'trading_strategies': trades,
            'historical_comparison': self._compare_to_2006(data),
            'severity': 5 if bubble_prob > 0.8 else (4 if bubble_prob > 0.6 else 3)
        }

    def _calculate_bubble_probability(self, data: HousingMarketData) -> float:
        """Calculate probability this is a bubble"""

        weighted_score = 0.0
        total_weight = 0.0

        # Check each indicator
        indicators = {
            'price_to_income': data.price_to_income_ratio,
            'price_to_rent': data.price_to_rent_ratio,
            'mortgage_debt_to_gdp': data.mortgage_debt_to_gdp,
            'price_growth_yoy': data.price_growth_yoy,
            'speculative_purchases_pct': data.speculative_purchases_pct,
            'adjustable_rate_pct': data.adjustable_rate_pct
        }

        for name, value in indicators.items():
            if name in self.thresholds:
                config = self.thresholds[name]

                if value >= config['red']:
                    score = 1.0
                elif value >= config['yellow']:
                    range_size = config['red'] - config['yellow']
                    score = (value - config['yellow']) / range_size
                else:
                    score = 0.0

                weighted_score += score * config['weight']
                total_weight += config['weight']

        return weighted_score / total_weight

    def _estimate_crash_timeline(self, data: HousingMarketData, prob: float) -> int:
        """Estimate months until crash"""

        # Research shows bubbles can persist 2-5 years after peak valuations
        if prob > 0.8:
            # Severe bubble - likely to crash within 12-18 months
            return 15
        elif prob > 0.6:
            # Moderate bubble - 18-36 months
            return 24
        else:
            # Early stage - 36+ months
            return 36

    def _calculate_overvaluation(self, data: HousingMarketData) -> float:
        """Calculate % overvaluation vs historical avg"""

        price_income_overval = (data.price_to_income_ratio / self.historical_avg['price_to_income'] - 1.0) * 100
        price_rent_overval = (data.price_to_rent_ratio / self.historical_avg['price_to_rent'] - 1.0) * 100

        # Average
        return (price_income_overval + price_rent_overval) / 2

    def _generate_warnings(self, data: HousingMarketData, prob: float) -> List[str]:
        """Generate warnings"""

        warnings = []

        if data.price_to_income_ratio > 6.0:
            warnings.append(f"🚨 Price-to-income at {data.price_to_income_ratio:.1f} (2006: 6.5). Housing severely overvalued.")

        if data.price_to_rent_ratio > 24:
            warnings.append(f"⚠️  Price-to-rent at {data.price_to_rent_ratio:.1f}. Better to rent than buy.")

        if data.speculative_purchases_pct > 30:
            warnings.append(f"📉 {data.speculative_purchases_pct:.0f}% speculative purchases. Bubble behavior.")

        if data.price_growth_yoy > 15:
            warnings.append(f"🔥 Prices growing {data.price_growth_yoy:.0f}%/year. Unsustainable.")

        if not warnings:
            warnings.append("✅ Housing market appears fairly valued.")

        return warnings

    def _generate_strategies(self, prob: float, months: int) -> List[Dict]:
        """Generate trading strategies"""

        strategies = []

        if prob > 0.7:
            strategies.extend([
                {
                    'strategy': 'Short homebuilders',
                    'tickers': 'XHB, DHI, LEN, PHM',
                    'rationale': f'{prob:.0%} bubble probability',
                    'expected_return': '-40% to -70% when bubble pops',
                    'timing': f'Build shorts over next {months//2} months'
                },
                {
                    'strategy': 'Short mortgage lenders',
                    'tickers': 'TREE, RKT, UWM',
                    'rationale': 'Loan originations will collapse',
                    'expected_return': '-50% to -80%'
                },
                {
                    'strategy': 'Buy puts on home improvement',
                    'tickers': 'HD, LOW',
                    'rationale': 'Housing turnover crashes → less renovation',
                    'expected_return': '-20% to -40%'
                }
            ])

        return strategies

    def _compare_to_2006(self, data: HousingMarketData) -> str:
        """Compare current to 2006 peak"""

        comparison = []

        if data.price_to_income_ratio >= 6.0:
            comparison.append("Price-to-income matches 2006 peak")
        if data.price_to_rent_ratio >= 24:
            comparison.append("Price-to-rent matches 2006 peak")
        if data.speculative_purchases_pct >= 35:
            comparison.append("Speculation matches 2006 levels")

        if comparison:
            return "DANGER: " + ", ".join(comparison) + ". This is 2006 all over again."
        else:
            return "Not yet at 2006 bubble extremes."


def main():
    """Example usage"""

    agent = HousingBubbleAgent()

    # 2006 pre-crash conditions
    bubble_2006 = {
        'price_to_income_ratio': 6.5,
        'price_to_rent_ratio': 25.0,
        'mortgage_debt_to_gdp': 72.0,
        'speculative_purchases_pct': 40.0,
        'adjustable_rate_pct': 35.0,
        'price_growth_yoy': 18.0
    }

    result = agent.analyze_event(bubble_2006)

    print("=== 2006 Housing Bubble Analysis ===")
    print(f"Bubble Probability: {result['bubble_probability']:.1%}")
    print(f"Overvaluation: {result['overvaluation_pct']:.0f}%")
    print(f"Months until crash: {result['estimated_months_until_crash']}")
    print(f"\nComparison: {result['historical_comparison']}")
    print(f"\nWarnings:")
    for w in result['warnings']:
        print(f"  {w}")


if __name__ == "__main__":
    main()
