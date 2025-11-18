"""
Extended Configuration for Additional Event Types
"""

# Extended Event Types (beyond the original 5)
EXTENDED_EVENT_TYPES = {
    'cyber_attack': {
        'description': 'Cyber attacks, infrastructure hacks, data breaches',
        'historical_examples': ['NotPetya 2017', 'Colonial Pipeline 2021', 'SolarWinds 2020'],
        'avg_market_impact': -8.0,
        'recovery_time_months': 4
    },
    'climate_crisis': {
        'description': 'Climate change events, extreme heat, droughts',
        'historical_examples': ['European Heatwave 2022', 'California Drought', 'Arctic Ice Loss'],
        'avg_market_impact': -6.0,
        'recovery_time_months': 18
    },
    'social_unrest': {
        'description': 'Civil unrest, protests, riots, social movements',
        'historical_examples': ['Arab Spring', 'Hong Kong Protests', 'BLM Movement'],
        'avg_market_impact': -5.5,
        'recovery_time_months': 5
    },
    'technology_disruption': {
        'description': 'AI disruption, automation, tech breakthrough/failure',
        'historical_examples': ['AI Boom 2023', 'Crypto Crash 2022', 'Dotcom Bubble'],
        'avg_market_impact': -12.0,
        'recovery_time_months': 8
    },
    'space_event': {
        'description': 'Solar flares, asteroid threats, satellite disruption',
        'historical_examples': ['Carrington Event 1859', 'Quebec Blackout 1989'],
        'avg_market_impact': -15.0,
        'recovery_time_months': 6
    },
    'supply_chain_collapse': {
        'description': 'Global supply chain breakdown, logistics crisis',
        'historical_examples': ['Suez Canal Block 2021', 'Chip Shortage 2021', 'COVID Supply Chain'],
        'avg_market_impact': -9.0,
        'recovery_time_months': 10
    },
    'resource_crisis': {
        'description': 'Water/food/energy shortage, resource wars',
        'historical_examples': ['1973 Oil Crisis', 'Global Food Crisis 2008'],
        'avg_market_impact': -11.0,
        'recovery_time_months': 12
    },
    'public_health_crisis': {
        'description': 'Antimicrobial resistance, mental health crisis',
        'historical_examples': ['Opioid Crisis', 'AMR Warnings', 'Mental Health Deterioration'],
        'avg_market_impact': -7.0,
        'recovery_time_months': 24
    },
    'infrastructure_failure': {
        'description': 'Grid collapse, internet outage, critical systems failure',
        'historical_examples': ['Texas Grid Failure 2021', 'Facebook Outage 2021'],
        'avg_market_impact': -8.5,
        'recovery_time_months': 3
    },
    'governance_collapse': {
        'description': 'State failure, regime change, institutional breakdown',
        'historical_examples': ['Venezuela Crisis', 'Lebanon Collapse', 'Afghanistan 2021'],
        'avg_market_impact': -13.0,
        'recovery_time_months': 36
    },
    'compound_event': {
        'description': 'Multiple simultaneous crises (polycrisis)',
        'historical_examples': ['2020 Pandemic + Social Unrest', 'Ukraine War + Energy + Food'],
        'avg_market_impact': -20.0,
        'recovery_time_months': 18
    }
}

# Behavioral Response Patterns
BEHAVIORAL_PATTERNS = {
    'fear_response': {
        'triggers': ['high_casualties', 'unknown_threat', 'systemic_risk'],
        'behaviors': [
            'flight_to_safety',
            'panic_selling',
            'herd_behavior',
            'risk_aversion_spike',
            'defensive_positioning'
        ],
        'market_effect': 'sell_off',
        'intensity_multiplier': 1.5
    },
    'anger_response': {
        'triggers': ['injustice', 'corruption', 'inequality'],
        'behaviors': [
            'risk_taking',
            'protest_actions',
            'boycotts',
            'aggressive_trading',
            'contrarian_moves'
        ],
        'market_effect': 'volatility',
        'intensity_multiplier': 1.2
    },
    'panic_buying': {
        'triggers': ['supply_disruption', 'shortage_fears', 'hoarding_signal'],
        'behaviors': [
            'stockpiling',
            'bulk_purchases',
            'commodity_rush',
            'essential_goods_run'
        ],
        'market_effect': 'commodity_spike',
        'intensity_multiplier': 2.0
    },
    'herd_mentality': {
        'triggers': ['market_crash', 'bubble_formation', 'influencer_action'],
        'behaviors': [
            'follow_the_crowd',
            'momentum_trading',
            'meme_stock_behavior',
            'social_media_driven'
        ],
        'market_effect': 'amplification',
        'intensity_multiplier': 1.8
    },
    'learned_helplessness': {
        'triggers': ['prolonged_crisis', 'repeated_shocks', 'policy_failure'],
        'behaviors': [
            'apathy',
            'withdrawal',
            'reduced_participation',
            'pessimism'
        ],
        'market_effect': 'reduced_volume',
        'intensity_multiplier': 0.7
    },
    'optimism_bias': {
        'triggers': ['recovery_signals', 'good_news', 'stimulus_announcement'],
        'behaviors': [
            'excessive_optimism',
            'underestimating_risk',
            'buying_the_dip',
            'denial'
        ],
        'market_effect': 'rally',
        'intensity_multiplier': 1.3
    }
}

# Market Winners and Losers by Event Type
MARKET_DIRECTIONS = {
    'pandemic': {
        'winners': {
            'technology': {'reason': 'Remote work boom', 'expected_gain': 25},
            'e_commerce': {'reason': 'Online shopping surge', 'expected_gain': 40},
            'healthcare': {'reason': 'Medical demand spike', 'expected_gain': 15},
            'streaming': {'reason': 'Home entertainment', 'expected_gain': 30},
            'delivery': {'reason': 'Food/goods delivery', 'expected_gain': 35},
            'biotech': {'reason': 'Vaccine development', 'expected_gain': 50}
        },
        'losers': {
            'travel': {'reason': 'Travel restrictions', 'expected_loss': -60},
            'hospitality': {'reason': 'Lockdowns', 'expected_loss': -55},
            'retail_physical': {'reason': 'Store closures', 'expected_loss': -40},
            'airlines': {'reason': 'Flight cancellations', 'expected_loss': -70},
            'entertainment_venues': {'reason': 'Social distancing', 'expected_loss': -65},
            'oil': {'reason': 'Demand collapse', 'expected_loss': -45}
        }
    },
    'cyber_attack': {
        'winners': {
            'cybersecurity': {'reason': 'Security demand surge', 'expected_gain': 35},
            'cloud_security': {'reason': 'Infrastructure hardening', 'expected_gain': 30},
            'insurance_cyber': {'reason': 'Coverage demand', 'expected_gain': 20},
            'consulting': {'reason': 'Security audits', 'expected_gain': 15}
        },
        'losers': {
            'affected_sector': {'reason': 'Direct impact', 'expected_loss': -25},
            'technology_trust': {'reason': 'Confidence decline', 'expected_loss': -15},
            'data_companies': {'reason': 'Privacy concerns', 'expected_loss': -20},
            'fintech': {'reason': 'Security fears', 'expected_loss': -18}
        }
    },
    'climate_crisis': {
        'winners': {
            'renewable_energy': {'reason': 'Green transition', 'expected_gain': 40},
            'electric_vehicles': {'reason': 'Emission regulations', 'expected_gain': 35},
            'water_tech': {'reason': 'Scarcity solutions', 'expected_gain': 30},
            'sustainable_ag': {'reason': 'Climate-resilient farming', 'expected_gain': 25},
            'carbon_capture': {'reason': 'Decarbonization', 'expected_gain': 45}
        },
        'losers': {
            'fossil_fuels': {'reason': 'Transition away', 'expected_loss': -40},
            'traditional_auto': {'reason': 'EV shift', 'expected_loss': -30},
            'coastal_real_estate': {'reason': 'Sea level rise', 'expected_loss': -35},
            'agriculture_old': {'reason': 'Crop failures', 'expected_loss': -25},
            'insurance': {'reason': 'Disaster claims', 'expected_loss': -20}
        }
    },
    'economic_crisis': {
        'winners': {
            'gold': {'reason': 'Safe haven', 'expected_gain': 20},
            'utilities': {'reason': 'Defensive play', 'expected_gain': 10},
            'consumer_staples': {'reason': 'Essential goods', 'expected_gain': 8},
            'discount_retail': {'reason': 'Budget shopping', 'expected_gain': 15},
            'debt_collection': {'reason': 'Default surge', 'expected_gain': 25},
            'bankruptcy_services': {'reason': 'Business failures', 'expected_gain': 30}
        },
        'losers': {
            'banks': {'reason': 'Loan defaults', 'expected_loss': -45},
            'luxury': {'reason': 'Discretionary cuts', 'expected_loss': -50},
            'construction': {'reason': 'Investment halt', 'expected_loss': -40},
            'automotive': {'reason': 'Purchase delays', 'expected_loss': -35},
            'commercial_real_estate': {'reason': 'Vacancy surge', 'expected_loss': -38}
        }
    },
    'technology_disruption': {
        'winners': {
            'ai_companies': {'reason': 'AI revolution', 'expected_gain': 60},
            'semiconductor': {'reason': 'Chip demand', 'expected_gain': 35},
            'cloud_computing': {'reason': 'Infrastructure need', 'expected_gain': 40},
            'automation': {'reason': 'Labor replacement', 'expected_gain': 30}
        },
        'losers': {
            'legacy_tech': {'reason': 'Obsolescence', 'expected_loss': -40},
            'human_services': {'reason': 'Automation', 'expected_loss': -35},
            'traditional_media': {'reason': 'Digital shift', 'expected_loss': -30},
            'retail_jobs': {'reason': 'Self-checkout', 'expected_loss': -25}
        }
    },
    'supply_chain_collapse': {
        'winners': {
            'logistics_tech': {'reason': 'Efficiency demand', 'expected_gain': 35},
            'regional_manufacturers': {'reason': 'Reshoring', 'expected_gain': 30},
            'inventory_management': {'reason': 'Buffer stock need', 'expected_gain': 25},
            'alternative_suppliers': {'reason': 'Diversification', 'expected_gain': 20}
        },
        'losers': {
            'just_in_time': {'reason': 'Model breakdown', 'expected_loss': -40},
            'global_retailers': {'reason': 'Stock shortages', 'expected_loss': -35},
            'auto_manufacturing': {'reason': 'Parts shortage', 'expected_loss': -45},
            'consumer_electronics': {'reason': 'Component delays', 'expected_loss': -30}
        }
    }
}

# Human Behavior Prediction Factors
BEHAVIORAL_FACTORS = {
    'risk_tolerance': {
        'fear_state': -0.7,  # Risk tolerance multiplier when fearful
        'anger_state': 0.3,   # Risk tolerance when angry
        'neutral_state': 0.0,
        'optimistic_state': 0.5
    },
    'time_horizon': {
        'panic': 'immediate',
        'fear': 'short_term',
        'uncertainty': 'medium_term',
        'confidence': 'long_term'
    },
    'information_seeking': {
        'low_uncertainty': 0.3,
        'medium_uncertainty': 0.6,
        'high_uncertainty': 0.9
    },
    'social_influence': {
        'isolation': 0.2,
        'small_network': 0.5,
        'large_network': 0.8,
        'viral_spread': 1.0
    }
}

# Compound Event Interactions
COMPOUND_EVENT_MULTIPLIERS = {
    ('pandemic', 'economic_crisis'): 1.8,
    ('climate_crisis', 'resource_crisis'): 1.6,
    ('cyber_attack', 'infrastructure_failure'): 1.7,
    ('social_unrest', 'governance_collapse'): 1.9,
    ('supply_chain_collapse', 'resource_crisis'): 1.5,
    ('technology_disruption', 'economic_crisis'): 1.4
}

# Generalized Event Categories
EVENT_CATEGORIES = {
    'physical': ['natural_disaster', 'climate_crisis', 'space_event'],
    'health': ['pandemic', 'public_health_crisis'],
    'security': ['terrorism', 'cyber_attack', 'social_unrest'],
    'economic': ['economic_crisis', 'supply_chain_collapse', 'resource_crisis'],
    'technological': ['technology_disruption', 'infrastructure_failure'],
    'political': ['geopolitical', 'governance_collapse'],
    'compound': ['compound_event']
}

# LLM Agent Roles
LLM_AGENT_ROLES = {
    'analyst': {
        'description': 'Analyzes event data and generates insights',
        'capabilities': ['data_analysis', 'pattern_recognition', 'historical_comparison'],
        'temperature': 0.3  # Lower for analytical tasks
    },
    'predictor': {
        'description': 'Makes predictions about outcomes',
        'capabilities': ['forecasting', 'scenario_generation', 'probability_estimation'],
        'temperature': 0.5
    },
    'psychologist': {
        'description': 'Analyzes human behavior and reactions',
        'capabilities': ['behavioral_analysis', 'sentiment_assessment', 'crowd_psychology'],
        'temperature': 0.6
    },
    'economist': {
        'description': 'Evaluates economic impacts',
        'capabilities': ['market_analysis', 'sector_impact', 'policy_evaluation'],
        'temperature': 0.4
    },
    'strategist': {
        'description': 'Develops response strategies',
        'capabilities': ['strategy_formation', 'risk_mitigation', 'opportunity_identification'],
        'temperature': 0.7
    },
    'coordinator': {
        'description': 'Coordinates multi-agent analysis',
        'capabilities': ['synthesis', 'conflict_resolution', 'consensus_building'],
        'temperature': 0.5
    }
}
