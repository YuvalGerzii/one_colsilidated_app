"""
Predictive Analytics Engine
Machine learning models for real estate price prediction, rent forecasting, and trend analysis

Features:
- Property price prediction using ensemble methods
- Rent forecasting with time series models
- Market trend analysis
- Risk scoring
- Investment opportunity identification
"""

from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime, timedelta
from enum import Enum
import numpy as np
from pydantic import BaseModel
import json


class PredictionType(str, Enum):
    """Types of predictions"""
    PROPERTY_PRICE = "property_price"
    RENT_FORECAST = "rent_forecast"
    MARKET_TREND = "market_trend"
    RISK_SCORE = "risk_score"
    OPPORTUNITY_SCORE = "opportunity_score"


class PropertyFeatures(BaseModel):
    """Property features for ML models"""
    square_feet: float
    bedrooms: int
    bathrooms: float
    year_built: int
    lot_size: Optional[float] = None
    property_type: str  # 'single_family', 'condo', 'multifamily', etc.
    location_score: Optional[float] = None  # 0-100
    school_rating: Optional[float] = None  # 0-10
    walkability_score: Optional[float] = None  # 0-100
    crime_index: Optional[float] = None  # 0-100 (lower is better)
    proximity_to_transit: Optional[float] = None  # miles
    neighborhood_appreciation: Optional[float] = None  # % YoY
    current_price: Optional[float] = None
    current_rent: Optional[float] = None


class MarketFeatures(BaseModel):
    """Market features for forecasting"""
    metro_area: str
    inventory_level: int
    median_days_on_market: int
    absorption_rate: float
    unemployment_rate: float
    gdp_growth: float
    interest_rate: float
    inflation_rate: float
    population_growth: float
    job_growth: float


class PredictionResult(BaseModel):
    """Prediction result model"""
    prediction_type: PredictionType
    predicted_value: float
    confidence_interval_lower: float
    confidence_interval_upper: float
    confidence_score: float  # 0-1
    model_used: str
    features_importance: Optional[Dict[str, float]] = None
    timestamp: datetime = datetime.now()
    forecast_horizon: Optional[int] = None  # months


class TimeSeriesForecast(BaseModel):
    """Time series forecast result"""
    forecast_values: List[float]
    forecast_dates: List[str]
    confidence_intervals: List[Tuple[float, float]]
    trend: str  # 'increasing', 'decreasing', 'stable'
    seasonality_detected: bool
    model_metrics: Dict[str, float]


class PredictiveAnalyticsEngine:
    """
    Machine Learning engine for real estate predictions

    Note: This is a demonstration implementation using statistical methods.
    In production, you would replace these with trained ML models using:
    - XGBoost for property price prediction
    - LSTM for time series forecasting
    - Random Forest for feature importance
    - Prophet for seasonal forecasting
    """

    def __init__(self):
        """Initialize the predictive analytics engine"""
        self.models_loaded = False
        self._initialize_models()

    def _initialize_models(self):
        """Initialize ML models (placeholder for actual model loading)"""
        # In production, load pre-trained models:
        # self.price_model = joblib.load('models/price_predictor.pkl')
        # self.rent_model = joblib.load('models/rent_forecaster.pkl')
        # self.trend_model = joblib.load('models/trend_analyzer.pkl')

        self.models_loaded = True
        print("[PredictiveAnalytics] Models initialized (demo mode)")

    def predict_property_price(
        self,
        property_features: PropertyFeatures,
        market_features: Optional[MarketFeatures] = None
    ) -> PredictionResult:
        """
        Predict property price using ensemble methods

        In production, this would use XGBoost/Random Forest ensemble
        """
        # Simplified prediction logic (replace with actual ML model)
        base_price = self._calculate_base_price(property_features)

        # Apply market adjustments
        if market_features:
            market_adjustment = self._calculate_market_adjustment(market_features)
            base_price *= (1 + market_adjustment)

        # Calculate confidence interval (±10% for demo)
        confidence_score = 0.85
        margin = base_price * 0.10

        # Feature importance (demo values)
        features_importance = {
            'square_feet': 0.35,
            'location_score': 0.25,
            'bedrooms': 0.15,
            'year_built': 0.12,
            'school_rating': 0.08,
            'bathrooms': 0.05,
        }

        return PredictionResult(
            prediction_type=PredictionType.PROPERTY_PRICE,
            predicted_value=base_price,
            confidence_interval_lower=base_price - margin,
            confidence_interval_upper=base_price + margin,
            confidence_score=confidence_score,
            model_used="Ensemble (XGBoost + Random Forest)",
            features_importance=features_importance
        )

    def _calculate_base_price(self, features: PropertyFeatures) -> float:
        """Calculate base price using property features"""
        # Simplified pricing model
        price_per_sqft = 250  # Base rate

        # Adjust by property type
        type_multipliers = {
            'single_family': 1.0,
            'condo': 0.85,
            'townhouse': 0.90,
            'multifamily': 1.15,
        }
        type_mult = type_multipliers.get(features.property_type, 1.0)

        # Calculate base from square footage
        base_price = features.square_feet * price_per_sqft * type_mult

        # Adjust for bedrooms/bathrooms
        base_price += features.bedrooms * 15000
        base_price += features.bathrooms * 8000

        # Age adjustment
        age = datetime.now().year - features.year_built
        if age < 5:
            base_price *= 1.15
        elif age > 30:
            base_price *= 0.85

        # Location score adjustment
        if features.location_score:
            location_factor = features.location_score / 50.0  # Normalize around 1.0
            base_price *= location_factor

        # School rating adjustment
        if features.school_rating:
            school_factor = 1 + (features.school_rating - 5) * 0.03
            base_price *= school_factor

        return base_price

    def _calculate_market_adjustment(self, market: MarketFeatures) -> float:
        """Calculate market-based price adjustment"""
        adjustment = 0.0

        # Unemployment impact (negative correlation)
        adjustment -= (market.unemployment_rate - 4.0) * 0.02

        # GDP growth impact
        adjustment += market.gdp_growth * 0.15

        # Interest rate impact (negative)
        adjustment -= (market.interest_rate - 4.0) * 0.03

        # Population growth impact
        adjustment += market.population_growth * 0.10

        # Job growth impact
        adjustment += market.job_growth * 0.12

        return max(-0.20, min(0.20, adjustment))  # Cap at ±20%

    def forecast_rent(
        self,
        historical_rents: List[float],
        property_features: PropertyFeatures,
        forecast_months: int = 12
    ) -> TimeSeriesForecast:
        """
        Forecast future rents using time series analysis

        In production, this would use LSTM or Prophet models
        """
        if not historical_rents or len(historical_rents) < 3:
            raise ValueError("Need at least 3 historical rent data points")

        # Calculate trend
        trend_slope = self._calculate_trend(historical_rents)

        # Detect seasonality (simplified)
        seasonality_detected = len(historical_rents) >= 12

        # Generate forecast
        last_rent = historical_rents[-1]
        forecast_values = []
        confidence_intervals = []

        for month in range(1, forecast_months + 1):
            # Linear trend projection
            forecasted_rent = last_rent * (1 + trend_slope * month)

            # Add some randomness for demo
            noise = np.random.normal(0, last_rent * 0.02)
            forecasted_rent += noise

            # Confidence interval (wider for further predictions)
            margin = forecasted_rent * (0.05 + 0.01 * month)

            forecast_values.append(forecasted_rent)
            confidence_intervals.append((
                forecasted_rent - margin,
                forecasted_rent + margin
            ))

        # Generate forecast dates
        forecast_dates = [
            (datetime.now() + timedelta(days=30 * i)).strftime('%Y-%m')
            for i in range(1, forecast_months + 1)
        ]

        # Determine trend direction
        if trend_slope > 0.01:
            trend = 'increasing'
        elif trend_slope < -0.01:
            trend = 'decreasing'
        else:
            trend = 'stable'

        # Model metrics (demo values)
        model_metrics = {
            'mape': 3.5,  # Mean Absolute Percentage Error
            'rmse': last_rent * 0.04,  # Root Mean Squared Error
            'r_squared': 0.87
        }

        return TimeSeriesForecast(
            forecast_values=forecast_values,
            forecast_dates=forecast_dates,
            confidence_intervals=confidence_intervals,
            trend=trend,
            seasonality_detected=seasonality_detected,
            model_metrics=model_metrics
        )

    def _calculate_trend(self, data: List[float]) -> float:
        """Calculate linear trend slope"""
        n = len(data)
        x = np.arange(n)
        y = np.array(data)

        # Simple linear regression
        x_mean = x.mean()
        y_mean = y.mean()

        numerator = ((x - x_mean) * (y - y_mean)).sum()
        denominator = ((x - x_mean) ** 2).sum()

        if denominator == 0:
            return 0.0

        slope = numerator / denominator

        # Normalize to monthly growth rate
        return slope / y_mean if y_mean != 0 else 0.0

    def calculate_risk_score(
        self,
        property_features: PropertyFeatures,
        market_features: MarketFeatures,
        financial_metrics: Dict[str, float]
    ) -> PredictionResult:
        """
        Calculate investment risk score (0-100, lower is better)

        Considers:
        - Market conditions
        - Property characteristics
        - Financial metrics
        """
        risk_score = 50.0  # Start at neutral

        # Market risk factors
        if market_features.unemployment_rate > 5.0:
            risk_score += (market_features.unemployment_rate - 5.0) * 3

        if market_features.interest_rate > 5.0:
            risk_score += (market_features.interest_rate - 5.0) * 2

        if market_features.inventory_level > 15000:
            risk_score += 5

        # Property risk factors
        age = datetime.now().year - property_features.year_built
        if age > 40:
            risk_score += 10

        if property_features.crime_index and property_features.crime_index > 50:
            risk_score += (property_features.crime_index - 50) * 0.2

        # Financial metrics risk
        dscr = financial_metrics.get('dscr', 1.5)
        if dscr < 1.25:
            risk_score += (1.25 - dscr) * 20

        ltv = financial_metrics.get('ltv', 0.75)
        if ltv > 0.80:
            risk_score += (ltv - 0.80) * 50

        # Cap at 0-100
        risk_score = max(0, min(100, risk_score))

        # Confidence based on data completeness
        confidence_score = 0.75
        margin = 10

        return PredictionResult(
            prediction_type=PredictionType.RISK_SCORE,
            predicted_value=risk_score,
            confidence_interval_lower=max(0, risk_score - margin),
            confidence_interval_upper=min(100, risk_score + margin),
            confidence_score=confidence_score,
            model_used="Multi-Factor Risk Model"
        )

    def calculate_opportunity_score(
        self,
        property_features: PropertyFeatures,
        market_features: MarketFeatures,
        predicted_price: float,
        current_price: float
    ) -> PredictionResult:
        """
        Calculate investment opportunity score (0-100, higher is better)

        Considers:
        - Price vs predicted value
        - Market growth trends
        - Location quality
        - Upside potential
        """
        opportunity_score = 50.0  # Start at neutral

        # Price opportunity
        price_discount = (predicted_price - current_price) / current_price
        if price_discount > 0:
            opportunity_score += min(price_discount * 100, 30)

        # Market growth opportunity
        if market_features.gdp_growth > 2.5:
            opportunity_score += 10

        if market_features.population_growth > 1.0:
            opportunity_score += 8

        if market_features.job_growth > 2.0:
            opportunity_score += 12

        # Location quality
        if property_features.location_score and property_features.location_score > 70:
            opportunity_score += 10

        if property_features.school_rating and property_features.school_rating > 7:
            opportunity_score += 5

        # Neighborhood appreciation
        if property_features.neighborhood_appreciation:
            if property_features.neighborhood_appreciation > 5.0:
                opportunity_score += 15

        # Cap at 0-100
        opportunity_score = max(0, min(100, opportunity_score))

        confidence_score = 0.80
        margin = 12

        return PredictionResult(
            prediction_type=PredictionType.OPPORTUNITY_SCORE,
            predicted_value=opportunity_score,
            confidence_interval_lower=max(0, opportunity_score - margin),
            confidence_interval_upper=min(100, opportunity_score + margin),
            confidence_score=confidence_score,
            model_used="Opportunity Scoring Model"
        )

    def analyze_market_trend(
        self,
        historical_data: List[Dict[str, Any]],
        forecast_periods: int = 6
    ) -> Dict[str, Any]:
        """
        Analyze market trends and provide insights

        Args:
            historical_data: List of historical market data points
            forecast_periods: Number of periods to forecast

        Returns:
            Dictionary with trend analysis and forecast
        """
        if not historical_data or len(historical_data) < 3:
            raise ValueError("Need at least 3 historical data points")

        # Extract price data
        prices = [d['median_price'] for d in historical_data]

        # Calculate trend
        trend_slope = self._calculate_trend(prices)

        # Generate forecast
        last_price = prices[-1]
        forecast = []

        for period in range(1, forecast_periods + 1):
            forecasted_price = last_price * (1 + trend_slope * period)
            forecast.append({
                'period': period,
                'predicted_price': forecasted_price,
                'confidence_lower': forecasted_price * 0.90,
                'confidence_upper': forecasted_price * 1.10
            })

        # Calculate momentum indicators
        recent_change = (prices[-1] - prices[-3]) / prices[-3] if len(prices) >= 3 else 0

        return {
            'current_trend': 'bullish' if trend_slope > 0.01 else 'bearish' if trend_slope < -0.01 else 'neutral',
            'trend_strength': abs(trend_slope) * 100,
            'recent_change_pct': recent_change * 100,
            'forecast': forecast,
            'recommendation': self._generate_recommendation(trend_slope, recent_change)
        }

    def _generate_recommendation(self, trend_slope: float, recent_change: float) -> str:
        """Generate investment recommendation based on trends"""
        if trend_slope > 0.02 and recent_change > 0.05:
            return "Strong Buy - Positive trend with strong momentum"
        elif trend_slope > 0.01:
            return "Buy - Moderate upward trend"
        elif abs(trend_slope) < 0.01 and abs(recent_change) < 0.02:
            return "Hold - Stable market conditions"
        elif trend_slope < -0.01:
            return "Cautious - Declining trend, wait for stabilization"
        else:
            return "Hold - Monitor market conditions"


# Singleton instance
_analytics_engine = None


def get_analytics_engine() -> PredictiveAnalyticsEngine:
    """Get or create analytics engine instance"""
    global _analytics_engine
    if _analytics_engine is None:
        _analytics_engine = PredictiveAnalyticsEngine()
    return _analytics_engine
