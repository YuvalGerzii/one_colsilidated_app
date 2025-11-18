"""
Market Direction Predictor
Predicts which sectors/assets will rise and fall during extreme events
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass
import numpy as np


@dataclass
class MarketDirection:
    """Market direction prediction for a specific asset/sector"""
    name: str
    category: str  # sector, commodity, currency, asset_class
    direction: str  # up, down, neutral
    expected_change_pct: float
    confidence: float  # 0-1
    rationale: str
    time_horizon: str  # immediate, short, medium, long
    volatility_expected: float  # Expected volatility


class MarketDirectionPredictor:
    """
    Predicts what will go up and what will go down during extreme events
    """

    def __init__(self):
        # Load sector mappings from config
        from ..config.extended_config import MARKET_DIRECTIONS
        self.direction_database = MARKET_DIRECTIONS

    def predict_directions(self, event_type: str, event_data: Dict) -> Dict:
        """
        Predict comprehensive market directions

        Args:
            event_type: Type of extreme event
            event_data: Event characteristics

        Returns:
            Dictionary with winners, losers, and neutral assets
        """
        # Get base directions from database
        base_directions = self.direction_database.get(event_type, {})

        # Adjust based on event severity
        severity = event_data.get('severity', 3)
        severity_multiplier = severity / 3.0

        # Get winners
        winners = []
        for sector, info in base_directions.get('winners', {}).items():
            winners.append(MarketDirection(
                name=sector,
                category='sector',
                direction='up',
                expected_change_pct=info['expected_gain'] * severity_multiplier,
                confidence=self._calculate_confidence(event_data),
                rationale=info['reason'],
                time_horizon=self._determine_time_horizon(sector, event_type),
                volatility_expected=abs(info['expected_gain']) * 0.5
            ))

        # Get losers
        losers = []
        for sector, info in base_directions.get('losers', {}).items():
            losers.append(MarketDirection(
                name=sector,
                category='sector',
                direction='down',
                expected_change_pct=info['expected_loss'] * severity_multiplier,
                confidence=self._calculate_confidence(event_data),
                rationale=info['reason'],
                time_horizon=self._determine_time_horizon(sector, event_type),
                volatility_expected=abs(info['expected_loss']) * 0.5
            ))

        # Add general market directions (not event-specific)
        general_directions = self._predict_general_directions(event_data, severity_multiplier)

        return {
            'winners': sorted(winners, key=lambda x: x.expected_change_pct, reverse=True),
            'losers': sorted(losers, key=lambda x: x.expected_change_pct),
            'safe_havens': general_directions['safe_havens'],
            'commodities': general_directions['commodities'],
            'currencies': general_directions['currencies'],
            'asset_classes': general_directions['asset_classes'],
            'summary': self._generate_summary(winners, losers)
        }

    def _predict_general_directions(self, event_data: Dict, severity_mult: float) -> Dict:
        """Predict general market directions (safe havens, commodities, etc.)"""

        # Safe havens (typically benefit during crises)
        safe_havens = [
            MarketDirection(
                name='Gold',
                category='commodity',
                direction='up',
                expected_change_pct=10 * severity_mult,
                confidence=0.85,
                rationale='Traditional safe haven during uncertainty',
                time_horizon='immediate',
                volatility_expected=8
            ),
            MarketDirection(
                name='US Treasury Bonds',
                category='fixed_income',
                direction='up',
                expected_change_pct=5 * severity_mult,
                confidence=0.90,
                rationale='Flight to quality in government bonds',
                time_horizon='immediate',
                volatility_expected=3
            ),
            MarketDirection(
                name='Swiss Franc',
                category='currency',
                direction='up',
                expected_change_pct=3 * severity_mult,
                confidence=0.80,
                rationale='Safe haven currency',
                time_horizon='short',
                volatility_expected=5
            ),
            MarketDirection(
                name='Japanese Yen',
                category='currency',
                direction='up',
                expected_change_pct=4 * severity_mult,
                confidence=0.75,
                rationale='Risk-off currency flows',
                time_horizon='immediate',
                volatility_expected=6
            )
        ]

        # Commodities (varies by event type)
        commodities = self._predict_commodity_directions(event_data, severity_mult)

        # Currencies
        currencies = self._predict_currency_directions(event_data, severity_mult)

        # Asset classes
        asset_classes = [
            MarketDirection(
                name='Equities',
                category='asset_class',
                direction='down',
                expected_change_pct=-15 * severity_mult,
                confidence=0.85,
                rationale='Risk-off environment',
                time_horizon='immediate',
                volatility_expected=25
            ),
            MarketDirection(
                name='Corporate Bonds',
                category='asset_class',
                direction='down',
                expected_change_pct=-8 * severity_mult,
                confidence=0.80,
                rationale='Credit spread widening',
                time_horizon='short',
                volatility_expected=12
            ),
            MarketDirection(
                name='Real Estate',
                category='asset_class',
                direction='down',
                expected_change_pct=-10 * severity_mult,
                confidence=0.70,
                rationale='Economic uncertainty impact',
                time_horizon='medium',
                volatility_expected=15
            ),
            MarketDirection(
                name='Cash',
                category='asset_class',
                direction='neutral',
                expected_change_pct=0,
                confidence=0.95,
                rationale='Capital preservation',
                time_horizon='immediate',
                volatility_expected=1
            )
        ]

        return {
            'safe_havens': safe_havens,
            'commodities': commodities,
            'currencies': currencies,
            'asset_classes': asset_classes
        }

    def _predict_commodity_directions(self, event_data: Dict, severity_mult: float) -> List[MarketDirection]:
        """Predict commodity price directions"""
        commodities = []

        event_type = event_data.get('event_type', '')

        # Oil
        if event_type in ['geopolitical', 'resource_crisis']:
            oil_change = 30 * severity_mult
            oil_direction = 'up'
        elif event_type in ['pandemic', 'economic_crisis']:
            oil_change = -40 * severity_mult
            oil_direction = 'down'
        else:
            oil_change = -10 * severity_mult
            oil_direction = 'down'

        commodities.append(MarketDirection(
            name='Crude Oil',
            category='commodity',
            direction=oil_direction,
            expected_change_pct=oil_change,
            confidence=0.75,
            rationale='Demand disruption' if oil_direction == 'down' else 'Supply disruption',
            time_horizon='immediate',
            volatility_expected=abs(oil_change) * 0.8
        ))

        # Agricultural commodities
        if event_type in ['climate_crisis', 'resource_crisis']:
            commodities.append(MarketDirection(
                name='Agricultural Commodities',
                category='commodity',
                direction='up',
                expected_change_pct=25 * severity_mult,
                confidence=0.80,
                rationale='Climate impact on crops',
                time_horizon='medium',
                volatility_expected=20
            ))

        # Industrial metals
        if event_type in ['economic_crisis']:
            commodities.append(MarketDirection(
                name='Industrial Metals',
                category='commodity',
                direction='down',
                expected_change_pct=-30 * severity_mult,
                confidence=0.85,
                rationale='Industrial demand collapse',
                time_horizon='short',
                volatility_expected=25
            ))

        return commodities

    def _predict_currency_directions(self, event_data: Dict, severity_mult: float) -> List[MarketDirection]:
        """Predict currency movements"""
        currencies = []

        # USD typically strengthens in crises (except US-specific crises)
        if event_data.get('geographic_scope') == 'global':
            currencies.append(MarketDirection(
                name='US Dollar',
                category='currency',
                direction='up',
                expected_change_pct=5 * severity_mult,
                confidence=0.85,
                rationale='Reserve currency status',
                time_horizon='immediate',
                volatility_expected=4
            ))

        # Emerging market currencies typically weaken
        currencies.append(MarketDirection(
            name='Emerging Market Currencies',
            category='currency',
            direction='down',
            expected_change_pct=-10 * severity_mult,
            confidence=0.80,
            rationale='Capital flight to developed markets',
            time_horizon='immediate',
            volatility_expected=15
        ))

        # Euro
        currencies.append(MarketDirection(
            name='Euro',
            category='currency',
            direction='down',
            expected_change_pct=-3 * severity_mult,
            confidence=0.70,
            rationale='Risk aversion',
            time_horizon='short',
            volatility_expected=5
        ))

        return currencies

    def _calculate_confidence(self, event_data: Dict) -> float:
        """Calculate prediction confidence"""
        base_confidence = 0.75

        # Adjust for data quality
        data_quality = event_data.get('data_quality', 'medium')
        quality_adjustment = {'high': 0.15, 'medium': 0, 'low': -0.15}
        base_confidence += quality_adjustment.get(data_quality, 0)

        # Adjust for uncertainty
        uncertainty = event_data.get('uncertainty_level', 0.5)
        base_confidence -= uncertainty * 0.2

        return max(0.5, min(0.95, base_confidence))

    def _determine_time_horizon(self, sector: str, event_type: str) -> str:
        """Determine time horizon for impact"""
        # Immediate impact sectors
        immediate_sectors = ['finance', 'energy', 'technology']
        if sector in immediate_sectors:
            return 'immediate'

        # Short-term impact
        short_term_sectors = ['travel', 'hospitality', 'retail']
        if sector in short_term_sectors:
            return 'short'

        # Medium-term
        medium_term_sectors = ['construction', 'real_estate', 'manufacturing']
        if sector in medium_term_sectors:
            return 'medium'

        # Default
        return 'short'

    def _generate_summary(self, winners: List[MarketDirection], losers: List[MarketDirection]) -> Dict:
        """Generate summary statistics"""
        return {
            'top_winner': winners[0].name if winners else None,
            'top_winner_gain': winners[0].expected_change_pct if winners else 0,
            'top_loser': losers[0].name if losers else None,
            'top_loser_loss': losers[0].expected_change_pct if losers else 0,
            'total_winners': len(winners),
            'total_losers': len(losers),
            'avg_winner_gain': np.mean([w.expected_change_pct for w in winners]) if winners else 0,
            'avg_loser_loss': np.mean([l.expected_change_pct for l in losers]) if losers else 0,
            'overall_market_direction': 'bearish' if len(losers) > len(winners) else 'mixed'
        }

    def get_trading_opportunities(self, event_type: str, event_data: Dict) -> List[Dict]:
        """
        Identify specific trading opportunities

        Args:
            event_type: Type of event
            event_data: Event characteristics

        Returns:
            List of trading opportunity dictionaries
        """
        directions = self.predict_directions(event_type, event_data)
        opportunities = []

        # Long opportunities (winners)
        for winner in directions['winners'][:5]:  # Top 5
            if winner.expected_change_pct > 15 and winner.confidence > 0.7:
                opportunities.append({
                    'type': 'long',
                    'asset': winner.name,
                    'rationale': winner.rationale,
                    'expected_return': winner.expected_change_pct,
                    'confidence': winner.confidence,
                    'risk_level': 'medium' if winner.volatility_expected < 20 else 'high',
                    'time_horizon': winner.time_horizon
                })

        # Short opportunities (losers)
        for loser in directions['losers'][:5]:  # Top 5
            if loser.expected_change_pct < -15 and loser.confidence > 0.7:
                opportunities.append({
                    'type': 'short',
                    'asset': loser.name,
                    'rationale': loser.rationale,
                    'expected_return': abs(loser.expected_change_pct),
                    'confidence': loser.confidence,
                    'risk_level': 'high',  # Shorting is riskier
                    'time_horizon': loser.time_horizon
                })

        # Safe haven opportunities
        for safe_haven in directions['safe_havens']:
            if safe_haven.expected_change_pct > 5:
                opportunities.append({
                    'type': 'defensive_long',
                    'asset': safe_haven.name,
                    'rationale': safe_haven.rationale,
                    'expected_return': safe_haven.expected_change_pct,
                    'confidence': safe_haven.confidence,
                    'risk_level': 'low',
                    'time_horizon': safe_haven.time_horizon
                })

        return sorted(opportunities, key=lambda x: x['expected_return'] * x['confidence'], reverse=True)

    def get_hedging_strategies(self, portfolio: Dict, event_type: str, event_data: Dict) -> List[Dict]:
        """
        Suggest hedging strategies for a portfolio

        Args:
            portfolio: Dictionary of portfolio holdings
            event_type: Type of event
            event_data: Event characteristics

        Returns:
            List of hedging recommendations
        """
        directions = self.predict_directions(event_type, event_data)
        hedges = []

        # VIX/volatility hedge
        hedges.append({
            'strategy': 'Long VIX/Volatility',
            'rationale': 'Hedge against market volatility spike',
            'allocation': '5-10%',
            'effectiveness': 'high',
            'cost': 'medium'
        })

        # Safe haven allocation
        hedges.append({
            'strategy': 'Increase Gold allocation',
            'rationale': 'Safe haven protection',
            'allocation': '10-15%',
            'effectiveness': 'high',
            'cost': 'low'
        })

        # Defensive sectors
        hedges.append({
            'strategy': 'Rotate to defensive sectors (utilities, consumer staples)',
            'rationale': 'Reduce portfolio beta',
            'allocation': '20-30%',
            'effectiveness': 'medium',
            'cost': 'low'
        })

        # Currency hedge
        if event_data.get('geographic_scope') == 'global':
            hedges.append({
                'strategy': 'Currency diversification (CHF, JPY)',
                'rationale': 'Protect against currency risk',
                'allocation': '5-10%',
                'effectiveness': 'medium',
                'cost': 'low'
            })

        # Tail risk hedge
        severity = event_data.get('severity', 3)
        if severity >= 4:
            hedges.append({
                'strategy': 'Out-of-money put options',
                'rationale': 'Tail risk protection',
                'allocation': '2-5%',
                'effectiveness': 'very_high',
                'cost': 'medium'
            })

        return hedges

    def get_sector_rotation_plan(self, event_type: str, event_data: Dict) -> Dict:
        """
        Generate sector rotation plan

        Args:
            event_type: Type of event
            event_data: Event characteristics

        Returns:
            Sector rotation recommendations
        """
        directions = self.predict_directions(event_type, event_data)

        return {
            'exit_sectors': [l.name for l in directions['losers'][:3]],
            'enter_sectors': [w.name for w in directions['winners'][:3]],
            'reduce_exposure': [l.name for l in directions['losers'][3:6]],
            'increase_exposure': [w.name for w in directions['winners'][3:6]],
            'timeline': 'immediate' if event_data.get('severity', 3) >= 4 else 'gradual',
            'rationale': f"Rotating away from crisis-vulnerable sectors toward beneficiaries"
        }
