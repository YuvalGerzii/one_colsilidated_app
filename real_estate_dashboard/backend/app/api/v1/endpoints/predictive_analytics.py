"""
Predictive Analytics API Endpoints
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime

from app.services.predictive_analytics import (
    get_analytics_engine,
    PropertyFeatures,
    MarketFeatures,
    PredictionType,
    PredictionResult,
    TimeSeriesForecast
)

router = APIRouter(
    prefix="/api/v1/predictive-analytics",
    tags=["predictive-analytics"]
)


class PricePredictionRequest(BaseModel):
    """Request model for price prediction"""
    property_features: PropertyFeatures
    market_features: Optional[MarketFeatures] = None


class RentForecastRequest(BaseModel):
    """Request model for rent forecast"""
    historical_rents: List[float]
    property_features: PropertyFeatures
    forecast_months: int = 12


class RiskScoreRequest(BaseModel):
    """Request model for risk score"""
    property_features: PropertyFeatures
    market_features: MarketFeatures
    financial_metrics: Dict[str, float]


class OpportunityScoreRequest(BaseModel):
    """Request model for opportunity score"""
    property_features: PropertyFeatures
    market_features: MarketFeatures
    predicted_price: float
    current_price: float


class MarketTrendRequest(BaseModel):
    """Request model for market trend analysis"""
    historical_data: List[Dict[str, Any]]
    forecast_periods: int = 6


@router.post("/predict-price", response_model=PredictionResult)
async def predict_property_price(request: PricePredictionRequest):
    """
    Predict property price using ML ensemble models

    Returns:
        - Predicted price
        - Confidence intervals
        - Feature importance
        - Model metadata
    """
    try:
        engine = get_analytics_engine()
        result = engine.predict_property_price(
            property_features=request.property_features,
            market_features=request.market_features
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@router.post("/forecast-rent", response_model=TimeSeriesForecast)
async def forecast_rent(request: RentForecastRequest):
    """
    Forecast future rents using time series models

    Returns:
        - Forecasted rent values
        - Confidence intervals
        - Trend analysis
        - Seasonality detection
    """
    try:
        engine = get_analytics_engine()
        result = engine.forecast_rent(
            historical_rents=request.historical_rents,
            property_features=request.property_features,
            forecast_months=request.forecast_months
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Forecast failed: {str(e)}")


@router.post("/risk-score", response_model=PredictionResult)
async def calculate_risk_score(request: RiskScoreRequest):
    """
    Calculate investment risk score (0-100, lower is better)

    Considers:
    - Market conditions
    - Property characteristics
    - Financial metrics
    """
    try:
        engine = get_analytics_engine()
        result = engine.calculate_risk_score(
            property_features=request.property_features,
            market_features=request.market_features,
            financial_metrics=request.financial_metrics
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Risk calculation failed: {str(e)}")


@router.post("/opportunity-score", response_model=PredictionResult)
async def calculate_opportunity_score(request: OpportunityScoreRequest):
    """
    Calculate investment opportunity score (0-100, higher is better)

    Considers:
    - Price vs predicted value
    - Market growth trends
    - Location quality
    - Upside potential
    """
    try:
        engine = get_analytics_engine()
        result = engine.calculate_opportunity_score(
            property_features=request.property_features,
            market_features=request.market_features,
            predicted_price=request.predicted_price,
            current_price=request.current_price
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Opportunity calculation failed: {str(e)}")


@router.post("/market-trend")
async def analyze_market_trend(request: MarketTrendRequest):
    """
    Analyze market trends and provide forecast

    Returns:
        - Current trend (bullish/bearish/neutral)
        - Trend strength
        - Forecast for future periods
        - Investment recommendation
    """
    try:
        engine = get_analytics_engine()
        result = engine.analyze_market_trend(
            historical_data=request.historical_data,
            forecast_periods=request.forecast_periods
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Trend analysis failed: {str(e)}")


@router.get("/demo-prediction")
async def get_demo_prediction():
    """
    Get demo prediction with sample data

    Useful for testing and UI development
    """
    # Sample property features
    sample_property = PropertyFeatures(
        square_feet=2000,
        bedrooms=3,
        bathrooms=2.5,
        year_built=2015,
        lot_size=5000,
        property_type="single_family",
        location_score=75,
        school_rating=8.5,
        walkability_score=65,
        crime_index=25,
        proximity_to_transit=1.5,
        neighborhood_appreciation=6.5,
        current_price=450000
    )

    # Sample market features
    sample_market = MarketFeatures(
        metro_area="Austin, TX",
        inventory_level=12000,
        median_days_on_market=35,
        absorption_rate=0.18,
        unemployment_rate=3.5,
        gdp_growth=2.8,
        interest_rate=4.25,
        inflation_rate=3.2,
        population_growth=2.5,
        job_growth=3.2
    )

    engine = get_analytics_engine()

    # Get price prediction
    price_prediction = engine.predict_property_price(
        property_features=sample_property,
        market_features=sample_market
    )

    # Get rent forecast
    historical_rents = [1800, 1850, 1820, 1900, 1950, 1980, 2000, 2050, 2100, 2150, 2180, 2200]
    rent_forecast = engine.forecast_rent(
        historical_rents=historical_rents,
        property_features=sample_property,
        forecast_months=12
    )

    # Get risk score
    financial_metrics = {
        'dscr': 1.45,
        'ltv': 0.75,
        'cap_rate': 0.055,
        'cash_on_cash': 0.08
    }
    risk_score = engine.calculate_risk_score(
        property_features=sample_property,
        market_features=sample_market,
        financial_metrics=financial_metrics
    )

    # Get opportunity score
    opportunity_score = engine.calculate_opportunity_score(
        property_features=sample_property,
        market_features=sample_market,
        predicted_price=price_prediction.predicted_value,
        current_price=sample_property.current_price
    )

    return {
        "price_prediction": price_prediction.dict(),
        "rent_forecast": {
            "next_12_months": rent_forecast.forecast_values[:12],
            "trend": rent_forecast.trend,
            "confidence": "high" if rent_forecast.model_metrics['r_squared'] > 0.8 else "medium"
        },
        "risk_score": risk_score.dict(),
        "opportunity_score": opportunity_score.dict(),
        "recommendation": "Strong Buy" if opportunity_score.predicted_value > 70 and risk_score.predicted_value < 40 else "Hold"
    }


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    engine = get_analytics_engine()
    return {
        "status": "healthy",
        "models_loaded": engine.models_loaded,
        "timestamp": datetime.now().isoformat()
    }
