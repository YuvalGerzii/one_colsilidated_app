"""
Configuration settings for Extreme Events Platform
"""

# Risk Thresholds
VAR_CONFIDENCE_LEVELS = [0.95, 0.99, 0.995]  # 95%, 99%, 99.5%
EXTREME_EVENT_THRESHOLD = 3.0  # Standard deviations
IMPACT_SEVERITY_LEVELS = {
    'low': 1,
    'medium': 2,
    'high': 3,
    'critical': 4,
    'catastrophic': 5
}

# Event Categories
EVENT_TYPES = {
    'pandemic': {
        'description': 'Disease outbreaks and health crises',
        'historical_examples': ['COVID-19', 'SARS', 'Spanish Flu'],
        'avg_market_impact': -15.0,  # percent
        'recovery_time_months': 12
    },
    'terrorism': {
        'description': 'Terror attacks and security events',
        'historical_examples': ['9/11', 'London Bombings', 'Paris Attacks'],
        'avg_market_impact': -7.5,
        'recovery_time_months': 3
    },
    'natural_disaster': {
        'description': 'Storms, earthquakes, floods, wildfires',
        'historical_examples': ['Hurricane Katrina', 'Fukushima', 'California Fires'],
        'avg_market_impact': -5.0,
        'recovery_time_months': 6
    },
    'economic_crisis': {
        'description': 'Financial system stress and collapse',
        'historical_examples': ['2008 Crisis', 'Dot-com Bubble', '1987 Crash'],
        'avg_market_impact': -30.0,
        'recovery_time_months': 24
    },
    'geopolitical': {
        'description': 'War, sanctions, political instability',
        'historical_examples': ['Russia-Ukraine War', 'Gulf War', 'Brexit'],
        'avg_market_impact': -10.0,
        'recovery_time_months': 9
    }
}

# Market Sectors (sensitivity to different events)
SECTOR_SENSITIVITY = {
    'healthcare': {'pandemic': 0.5, 'terrorism': 1.0, 'natural_disaster': 1.0, 'economic_crisis': 1.2, 'geopolitical': 1.1},
    'travel': {'pandemic': 2.5, 'terrorism': 2.0, 'natural_disaster': 1.5, 'economic_crisis': 1.8, 'geopolitical': 1.7},
    'finance': {'pandemic': 1.5, 'terrorism': 1.3, 'natural_disaster': 1.1, 'economic_crisis': 3.0, 'geopolitical': 1.5},
    'energy': {'pandemic': 1.2, 'terrorism': 1.8, 'natural_disaster': 1.6, 'economic_crisis': 1.4, 'geopolitical': 2.5},
    'technology': {'pandemic': 0.8, 'terrorism': 1.0, 'natural_disaster': 0.9, 'economic_crisis': 1.3, 'geopolitical': 1.2},
    'consumer': {'pandemic': 1.3, 'terrorism': 1.2, 'natural_disaster': 1.2, 'economic_crisis': 1.8, 'geopolitical': 1.3},
    'utilities': {'pandemic': 0.7, 'terrorism': 1.1, 'natural_disaster': 1.8, 'economic_crisis': 0.9, 'geopolitical': 1.0},
    'real_estate': {'pandemic': 1.4, 'terrorism': 1.5, 'natural_disaster': 2.0, 'economic_crisis': 2.2, 'geopolitical': 1.2}
}

# Machine Learning Model Parameters
ML_CONFIG = {
    'neural_network': {
        'hidden_layers': [128, 64, 32],
        'activation': 'relu',
        'dropout_rate': 0.3,
        'epochs': 100,
        'batch_size': 32
    },
    'svm': {
        'kernel': 'rbf',
        'C': 1.0,
        'gamma': 'scale'
    },
    'random_forest': {
        'n_estimators': 200,
        'max_depth': 20,
        'min_samples_split': 5
    }
}

# Extreme Value Theory Parameters
EVT_CONFIG = {
    'threshold_percentile': 0.95,  # Use top 5% of losses
    'block_size': 20,  # For block maxima method
    'confidence_interval': 0.95
}

# Economic Impact Factors
ECONOMIC_FACTORS = {
    'gdp_impact': {
        'weight': 0.25,
        'unit': 'percentage_points'
    },
    'unemployment': {
        'weight': 0.20,
        'unit': 'percentage_points'
    },
    'inflation': {
        'weight': 0.15,
        'unit': 'percentage_points'
    },
    'trade_disruption': {
        'weight': 0.15,
        'unit': 'percentage_decline'
    },
    'consumer_confidence': {
        'weight': 0.10,
        'unit': 'index_points'
    },
    'investment_decline': {
        'weight': 0.15,
        'unit': 'percentage_decline'
    }
}

# Regional Impact Multipliers
REGIONAL_MULTIPLIERS = {
    'local': 1.0,
    'regional': 2.5,
    'national': 5.0,
    'continental': 8.0,
    'global': 10.0
}

# Time Decay Function (how impact diminishes over time)
TIME_DECAY_PARAMS = {
    'initial_shock_days': 5,      # First shock period
    'acute_phase_days': 30,        # Acute reaction phase
    'recovery_phase_months': 6,    # Recovery period
    'long_term_years': 2          # Long-term effects
}

# API and Data Source Configuration
DATA_SOURCES = {
    'market_data': 'yahoo_finance',  # or 'alpha_vantage', 'bloomberg'
    'news_api': 'gdelt',             # Global Database of Events, Language, and Tone
    'economic_data': 'fred',         # Federal Reserve Economic Data
    'disaster_db': 'em_dat'          # Emergency Events Database
}

# Alert Thresholds
ALERT_LEVELS = {
    'information': {'var_breach': 1.0, 'confidence_drop': 5},
    'warning': {'var_breach': 2.0, 'confidence_drop': 10},
    'critical': {'var_breach': 3.0, 'confidence_drop': 20},
    'emergency': {'var_breach': 5.0, 'confidence_drop': 30}
}
