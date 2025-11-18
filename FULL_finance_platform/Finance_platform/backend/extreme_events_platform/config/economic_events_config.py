"""
Configuration for economic event types (recession, inflation, interest rates)
"""

# Economic Event Types
ECONOMIC_EVENT_TYPES = {
    'recession': {
        'description': 'Economic recession or contraction',
        'historical_examples': ['2008 Financial Crisis', '2020 COVID Recession', '2001 Dot-com Recession'],
        'avg_market_impact': -25.0,
        'recovery_time_months': 18,
        'key_indicators': [
            'yield_curve_inversion',
            'unemployment_rate',
            'gdp_growth',
            'consumer_confidence',
            'manufacturing_pmi'
        ]
    },
    'inflation': {
        'description': 'Inflation surge above Fed target',
        'historical_examples': ['1970s Stagflation', '2021-2023 Inflation Surge'],
        'avg_market_impact': -12.0,
        'recovery_time_months': 24,
        'key_indicators': [
            'cpi',
            'pce',
            'core_pce',
            'wage_growth',
            'commodity_prices'
        ]
    },
    'interest_rate_change': {
        'description': 'Federal Reserve rate hike or cut',
        'historical_examples': ['2022-2023 Hiking Cycle', '2020 Emergency Cuts', '2008 Crisis Cuts'],
        'avg_market_impact': -5.0,  # Depends on direction
        'recovery_time_months': 3,
        'key_indicators': [
            'fed_funds_rate',
            'forward_guidance',
            'inflation',
            'unemployment'
        ]
    },
    'stagflation': {
        'description': 'High inflation with economic stagnation',
        'historical_examples': ['1970s Oil Crisis'],
        'avg_market_impact': -30.0,
        'recovery_time_months': 36
    },
    'deflation': {
        'description': 'Sustained price decline',
        'historical_examples': ['Japan Lost Decades', 'Great Depression'],
        'avg_market_impact': -35.0,
        'recovery_time_months': 48
    }
}

# Recession Indicators and Thresholds
RECESSION_INDICATORS = {
    'yield_curve': {
        'threshold': 0.0,  # Inversion = negative spread
        'weight': 0.30,
        'lead_time_months': 12
    },
    'sahm_rule': {
        'threshold': 0.5,  # Unemployment rise of 0.5pp
        'weight': 0.25,
        'lead_time_months': 0  # Coincident
    },
    'gdp': {
        'threshold': 0.0,  # Two consecutive negative quarters
        'weight': 0.20,
        'lead_time_months': 0
    },
    'consumer_confidence': {
        'threshold': 80,  # Index below 80
        'weight': 0.15,
        'lead_time_months': 3
    },
    'pmi': {
        'threshold': 50,  # Below 50 = contraction
        'weight': 0.10,
        'lead_time_months': 3
    }
}

# Inflation Breakpoints
INFLATION_LEVELS = {
    'target': 2.0,
    'elevated': 3.0,
    'high': 4.5,
    'very_high': 6.0,
    'hyperinflation': 10.0
}

# Fed Rate Response Matrix
FED_RATE_RESPONSE = {
    'inflation_above_target': {
        'small_gap': (0.0, 0.5),  # 0-0.5pp above target
        'medium_gap': (0.5, 1.5),  # 0.5-1.5pp above target
        'large_gap': (1.5, float('inf')),  # >1.5pp above target
        'hikes_needed': {
            'small_gap': 1,
            'medium_gap': 3,
            'large_gap': 6
        }
    }
}

# Economic Cycle Phases
ECONOMIC_CYCLE_PHASES = {
    'expansion': {
        'gdp_growth': '>2%',
        'unemployment': 'declining',
        'inflation': 'stable',
        'policy': 'neutral'
    },
    'peak': {
        'gdp_growth': 'decelerating',
        'unemployment': 'at lows',
        'inflation': 'rising',
        'policy': 'tightening'
    },
    'contraction': {
        'gdp_growth': 'negative',
        'unemployment': 'rising',
        'inflation': 'declining',
        'policy': 'easing'
    },
    'trough': {
        'gdp_growth': 'stabilizing',
        'unemployment': 'at highs',
        'inflation': 'low',
        'policy': 'accommodative'
    }
}
