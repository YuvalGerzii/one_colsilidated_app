"""
Machine Learning & AI Analytics API Endpoints

Provides endpoints for:
- Property valuation predictions
- Market trend forecasting
- Deal success probability
- Automated comparable selection
- Financial anomaly detection
- Natural language queries
"""

import logging
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Query, Body
from pydantic import BaseModel, Field

from app.ml.property_valuation import PropertyValuationPredictor, generate_sample_training_data
from app.ml.market_trends import MarketTrendForecaster, generate_sample_market_data
from app.ml.deal_success import DealSuccessPredictor, generate_sample_deal_data
from app.ml.comparable_selector import ComparableSelector, generate_sample_property_database
from app.ml.anomaly_detection import AnomalyDetector, generate_sample_transaction_data
from app.ml.natural_language_query import NaturalLanguageQueryEngine, generate_sample_property_data

logger = logging.getLogger(__name__)

router = APIRouter()


# ================================
# REQUEST/RESPONSE MODELS
# ================================

class PropertyFeatures(BaseModel):
    """Property features for valuation."""
    square_feet: float
    bedrooms: int
    bathrooms: float
    year_built: int
    lot_size: Optional[float] = None
    garage_spaces: Optional[int] = 0
    stories: Optional[int] = 1
    property_type: Optional[str] = "single_family"
    condition: Optional[str] = "average"
    zip_code: Optional[str] = None


class ValuationRequest(BaseModel):
    """Request for property valuation."""
    properties: List[PropertyFeatures] = Field(..., description="List of properties to value")
    return_confidence: bool = Field(True, description="Include confidence intervals")


class ValuationResponse(BaseModel):
    """Response for property valuation."""
    success: bool
    predictions: List[Dict[str, Any]]
    model_info: Optional[Dict[str, Any]] = None


class MarketTrendRequest(BaseModel):
    """Request for market trend forecast."""
    historical_data: List[Dict[str, Any]] = Field(..., description="Historical market data")
    periods: int = Field(12, description="Number of periods to forecast")
    date_column: str = Field("date", description="Date column name")
    value_column: str = Field("median_price", description="Value column name")
    methods: List[str] = Field(
        ["arima", "exponential_smoothing", "gradient_boosting"],
        description="Forecasting methods to use"
    )


class DealSuccessRequest(BaseModel):
    """Request for deal success prediction."""
    deals: List[Dict[str, Any]] = Field(..., description="Deal information")
    return_factors: bool = Field(True, description="Include contributing factors")


class ComparableRequest(BaseModel):
    """Request for comparable property selection."""
    subject_property: Dict[str, Any] = Field(..., description="Subject property")
    n_comps: int = Field(10, description="Number of comparables")
    filters: Optional[Dict[str, Any]] = Field(None, description="Filter criteria")
    weights: Optional[Dict[str, float]] = Field(None, description="Feature weights")


class AnomalyDetectionRequest(BaseModel):
    """Request for anomaly detection."""
    data: List[Dict[str, Any]] = Field(..., description="Data to analyze")
    method: str = Field("multivariate", description="Detection method")
    feature: Optional[str] = Field(None, description="Feature for univariate detection")
    date_column: Optional[str] = Field("date", description="Date column for time series")
    value_column: Optional[str] = Field("value", description="Value column for time series")


class NLQueryRequest(BaseModel):
    """Request for natural language query."""
    query: str = Field(..., description="Natural language query")
    data: Optional[List[Dict[str, Any]]] = Field(None, description="Data to query (optional)")
    use_sample_data: bool = Field(True, description="Use sample data if no data provided")


# ================================
# PROPERTY VALUATION ENDPOINTS
# ================================

@router.post("/valuation/predict", response_model=ValuationResponse)
async def predict_property_valuation(request: ValuationRequest):
    """
    Predict property values using ML models.

    Uses ensemble of XGBoost and Random Forest for accurate predictions.
    """
    try:
        logger.info(f"Predicting valuation for {len(request.properties)} properties")

        # Initialize and train predictor with sample data
        predictor = PropertyValuationPredictor()

        # Generate sample training data (in production, use real MLS data)
        sample_props, sample_prices = generate_sample_training_data(1000)
        predictor.train(sample_props, sample_prices)

        # Prepare input properties
        properties_dict = [prop.model_dump() for prop in request.properties]

        # Make predictions
        predictions = predictor.predict(
            properties_dict,
            return_confidence=request.return_confidence
        )

        # Get feature importance
        feature_importance = predictor.get_feature_importance()

        return ValuationResponse(
            success=True,
            predictions=predictions,
            model_info={
                "feature_importance": feature_importance,
                "n_features": len(feature_importance)
            }
        )

    except Exception as e:
        logger.error(f"Valuation prediction failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/valuation/demo")
async def demo_property_valuation():
    """
    Demo endpoint showing property valuation on sample data.
    """
    try:
        # Generate sample data
        predictor = PropertyValuationPredictor()
        sample_props, sample_prices = generate_sample_training_data(1000)

        # Train model
        metrics = predictor.train(sample_props, sample_prices)

        # Test on a few examples
        test_props = sample_props[:5]
        predictions = predictor.predict(test_props, return_confidence=True)

        return {
            "success": True,
            "training_metrics": metrics,
            "sample_predictions": predictions,
            "feature_importance": predictor.get_feature_importance()
        }

    except Exception as e:
        logger.error(f"Demo valuation failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ================================
# MARKET TRENDS ENDPOINTS
# ================================

@router.post("/market-trends/forecast")
async def forecast_market_trends(request: MarketTrendRequest):
    """
    Forecast market trends using time series analysis.

    Combines ARIMA, Exponential Smoothing, and Gradient Boosting.
    """
    try:
        logger.info(f"Forecasting {request.periods} periods")

        forecaster = MarketTrendForecaster()

        # Generate forecast
        forecast = forecaster.forecast(
            data=request.historical_data,
            periods=request.periods,
            date_column=request.date_column,
            value_column=request.value_column,
            methods=request.methods
        )

        # Add trend analysis
        trend_analysis = forecaster.analyze_trend(
            data=request.historical_data,
            date_column=request.date_column,
            value_column=request.value_column
        )

        return {
            "success": True,
            "forecast": forecast,
            "trend_analysis": trend_analysis
        }

    except Exception as e:
        logger.error(f"Market forecast failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/market-trends/demo")
async def demo_market_trends():
    """
    Demo endpoint showing market trend forecasting on sample data.
    """
    try:
        # Generate sample market data
        sample_data = generate_sample_market_data(48)  # 4 years of monthly data

        forecaster = MarketTrendForecaster()

        # Forecast next 12 months
        forecast = forecaster.forecast(sample_data, periods=12)

        # Analyze trends
        analysis = forecaster.analyze_trend(sample_data)

        return {
            "success": True,
            "sample_data": sample_data[-12:],  # Last 12 months
            "forecast": forecast,
            "trend_analysis": analysis
        }

    except Exception as e:
        logger.error(f"Demo forecast failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ================================
# DEAL SUCCESS ENDPOINTS
# ================================

@router.post("/deal-success/predict")
async def predict_deal_success(request: DealSuccessRequest):
    """
    Predict probability of deal success.

    Uses ensemble classification to predict deal closure likelihood.
    """
    try:
        logger.info(f"Predicting success for {len(request.deals)} deals")

        # Initialize and train predictor
        predictor = DealSuccessPredictor()

        # Generate sample training data
        sample_deals, sample_outcomes = generate_sample_deal_data(1000)
        metrics = predictor.train(sample_deals, sample_outcomes)

        # Make predictions
        predictions = predictor.predict(
            request.deals,
            return_factors=request.return_factors
        )

        return {
            "success": True,
            "predictions": predictions,
            "model_metrics": metrics
        }

    except Exception as e:
        logger.error(f"Deal success prediction failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/deal-success/demo")
async def demo_deal_success():
    """
    Demo endpoint showing deal success prediction on sample data.
    """
    try:
        # Generate sample data
        predictor = DealSuccessPredictor()
        sample_deals, sample_outcomes = generate_sample_deal_data(1000)

        # Train model
        metrics = predictor.train(sample_deals, sample_outcomes)

        # Test predictions
        test_deals = sample_deals[:5]
        predictions = predictor.predict(test_deals, return_factors=True)

        return {
            "success": True,
            "training_metrics": metrics,
            "sample_predictions": predictions,
            "feature_importance": predictor.get_feature_importance()
        }

    except Exception as e:
        logger.error(f"Demo deal prediction failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ================================
# COMPARABLE SELECTION ENDPOINTS
# ================================

@router.post("/comparables/find")
async def find_comparable_properties(request: ComparableRequest):
    """
    Find comparable properties for valuation.

    Uses ML-based similarity scoring to find best comps.
    """
    try:
        logger.info("Finding comparable properties")

        # Initialize selector
        selector = ComparableSelector()

        # Build database with sample properties
        sample_database = generate_sample_property_database(500)
        selector.build_database(sample_database)

        # Find comparables
        comparables = selector.find_comparables(
            subject_property=request.subject_property,
            n_comps=request.n_comps,
            filters=request.filters,
            weights=request.weights
        )

        # Calculate indicated value
        indicated_value = selector.calculate_indicated_value(
            request.subject_property,
            comparables
        )

        return {
            "success": True,
            "comparables": comparables,
            "indicated_value": indicated_value
        }

    except Exception as e:
        logger.error(f"Comparable selection failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/comparables/demo")
async def demo_comparable_selection():
    """
    Demo endpoint showing comparable selection on sample data.
    """
    try:
        # Generate sample database
        selector = ComparableSelector()
        sample_database = generate_sample_property_database(500)
        selector.build_database(sample_database)

        # Create subject property
        subject = sample_database[0]

        # Find comparables
        comparables = selector.find_comparables(subject, n_comps=10)

        # Calculate indicated value
        indicated_value = selector.calculate_indicated_value(subject, comparables)

        return {
            "success": True,
            "subject_property": subject,
            "comparables": comparables[:5],  # Top 5
            "indicated_value": indicated_value
        }

    except Exception as e:
        logger.error(f"Demo comparable selection failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ================================
# ANOMALY DETECTION ENDPOINTS
# ================================

@router.post("/anomaly-detection/detect")
async def detect_anomalies(request: AnomalyDetectionRequest):
    """
    Detect anomalies in financial data.

    Supports multivariate, univariate, and time series detection.
    """
    try:
        logger.info(f"Detecting anomalies using {request.method} method")

        detector = AnomalyDetector()

        if request.method == "multivariate":
            results = detector.detect_multivariate_anomalies(request.data)

        elif request.method == "univariate":
            if not request.feature:
                raise HTTPException(
                    status_code=400,
                    detail="Feature required for univariate detection"
                )
            results = detector.detect_univariate_anomalies(
                request.data,
                request.feature
            )

        elif request.method == "time_series":
            results = detector.detect_time_series_anomalies(
                request.data,
                request.date_column,
                request.value_column
            )

        elif request.method == "financial":
            results = detector.detect_financial_anomalies(request.data)

        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown method: {request.method}"
            )

        return {
            "success": True,
            "method": request.method,
            "results": results
        }

    except Exception as e:
        logger.error(f"Anomaly detection failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/anomaly-detection/demo")
async def demo_anomaly_detection():
    """
    Demo endpoint showing anomaly detection on sample data.
    """
    try:
        # Generate sample transaction data with anomalies
        sample_data = generate_sample_transaction_data(500, with_anomalies=True)

        detector = AnomalyDetector()

        # Run financial anomaly detection
        results = detector.detect_financial_anomalies(sample_data)

        return {
            "success": True,
            "sample_data_count": len(sample_data),
            "anomaly_results": results
        }

    except Exception as e:
        logger.error(f"Demo anomaly detection failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ================================
# NATURAL LANGUAGE QUERY ENDPOINTS
# ================================

@router.post("/nl-query/execute")
async def execute_natural_language_query(request: NLQueryRequest):
    """
    Execute natural language query on property data.

    Examples:
    - "Show me multifamily deals in Miami under $5M"
    - "What's the average ROI for properties in ZIP 90210?"
    - "Find all single family homes with NOI over $50k"
    """
    try:
        logger.info(f"Executing NL query: {request.query}")

        engine = NaturalLanguageQueryEngine(use_embeddings=False)

        # Use provided data or generate sample data
        if request.data:
            data = request.data
        elif request.use_sample_data:
            data = generate_sample_property_data(100)
        else:
            raise HTTPException(
                status_code=400,
                detail="Either provide data or set use_sample_data=true"
            )

        # Execute query
        results = engine.execute_query(request.query, data, return_metadata=True)

        return {
            "success": True,
            **results
        }

    except Exception as e:
        logger.error(f"NL query execution failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/nl-query/suggestions")
async def get_query_suggestions(
    partial_query: str = Query("", description="Partial query for suggestions")
):
    """
    Get query suggestions based on partial input.
    """
    try:
        engine = NaturalLanguageQueryEngine()
        suggestions = engine.suggest_queries(partial_query)

        return {
            "success": True,
            "suggestions": suggestions
        }

    except Exception as e:
        logger.error(f"Query suggestions failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/nl-query/demo")
async def demo_natural_language_query():
    """
    Demo endpoint showing natural language query capabilities.
    """
    try:
        # Generate sample data
        sample_data = generate_sample_property_data(100)

        engine = NaturalLanguageQueryEngine()

        # Example queries
        example_queries = [
            "Show me multifamily deals in Miami under $5M",
            "Find single family homes with ROI over 15%",
            "What's the average price in California?"
        ]

        results = []
        for query in example_queries:
            result = engine.execute_query(query, sample_data)
            results.append({
                "query": query,
                "count": result['count'],
                "sample_results": result['results'][:3] if result['results'] else []
            })

        return {
            "success": True,
            "example_queries": results,
            "total_properties": len(sample_data)
        }

    except Exception as e:
        logger.error(f"Demo NL query failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ================================
# HEALTH CHECK
# ================================

@router.get("/health")
async def ml_health_check():
    """
    Health check for ML/AI services.
    """
    return {
        "success": True,
        "status": "operational",
        "services": {
            "property_valuation": "available",
            "market_trends": "available",
            "deal_success": "available",
            "comparable_selection": "available",
            "anomaly_detection": "available",
            "natural_language_query": "available"
        }
    }
