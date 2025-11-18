"""
Machine Learning Predictions Database Models

Stores ML prediction history and results for:
- Property valuations
- Market forecasts
- Deal success predictions
- Anomaly detections
"""

from sqlalchemy import Column, Integer, Float, String, JSON, Boolean, Text
from app.models.database import Base, TimestampMixin, UUIDMixin


class PropertyValuationPrediction(Base, UUIDMixin, TimestampMixin):
    """Property valuation prediction record."""

    __tablename__ = "ml_property_valuations"

    property_id = Column(String(100), nullable=True, index=True, comment="Reference to property")
    address = Column(String(255), nullable=True, comment="Property address")
    predicted_value = Column(Float, nullable=False, comment="Predicted property value")
    lower_bound = Column(Float, nullable=True, comment="Lower confidence bound")
    upper_bound = Column(Float, nullable=True, comment="Upper confidence bound")
    confidence_score = Column(Float, nullable=True, comment="Prediction confidence (0-1)")

    # Input features
    square_feet = Column(Float, nullable=True)
    bedrooms = Column(Integer, nullable=True)
    bathrooms = Column(Float, nullable=True)
    year_built = Column(Integer, nullable=True)
    property_type = Column(String(50), nullable=True)
    zip_code = Column(String(10), nullable=True)

    # Model metadata
    model_version = Column(String(50), nullable=True, comment="ML model version")
    feature_importance = Column(JSON, nullable=True, comment="Feature importance scores")

    # User info
    analyst = Column(String(255), nullable=True, comment="User who requested prediction")
    notes = Column(Text, nullable=True)


class MarketTrendForecast(Base, UUIDMixin, TimestampMixin):
    """Market trend forecast record."""

    __tablename__ = "ml_market_forecasts"

    market_name = Column(String(255), nullable=False, comment="Market identifier")
    metric_name = Column(String(100), nullable=False, comment="Forecasted metric")

    # Forecast data
    forecast_periods = Column(Integer, nullable=False, comment="Number of periods forecasted")
    forecast_data = Column(JSON, nullable=False, comment="Forecast values and dates")
    ensemble_forecast = Column(JSON, nullable=True, comment="Ensemble forecast results")

    # Methods used
    methods = Column(JSON, nullable=False, comment="Forecasting methods used")

    # Historical data summary
    historical_periods = Column(Integer, nullable=True, comment="Historical data points used")
    trend_direction = Column(String(50), nullable=True, comment="Trend direction")
    volatility = Column(Float, nullable=True, comment="Market volatility measure")

    # User info
    analyst = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)


class DealSuccessPrediction(Base, UUIDMixin, TimestampMixin):
    """Deal success probability prediction record."""

    __tablename__ = "ml_deal_predictions"

    deal_id = Column(String(100), nullable=True, index=True, comment="Reference to deal in CRM")
    deal_name = Column(String(255), nullable=True, comment="Deal name")

    # Prediction
    success_probability = Column(Float, nullable=False, comment="Success probability (0-1)")
    predicted_outcome = Column(String(50), nullable=False, comment="Predicted outcome")
    risk_level = Column(String(50), nullable=False, comment="Risk level (low/medium/high)")
    confidence = Column(Float, nullable=True, comment="Prediction confidence")

    # Deal features
    deal_value = Column(Float, nullable=True)
    offer_to_asking_ratio = Column(Float, nullable=True)
    buyer_credit_score = Column(Integer, nullable=True)
    cash_offer = Column(Boolean, nullable=True)
    pre_approved = Column(Boolean, nullable=True)

    # Top contributing factors
    top_factors = Column(JSON, nullable=True, comment="Top factors affecting prediction")

    # Model metadata
    model_version = Column(String(50), nullable=True)
    model_accuracy = Column(Float, nullable=True, comment="Model accuracy on test set")

    # Actual outcome (filled in later)
    actual_outcome = Column(Boolean, nullable=True, comment="Actual deal outcome")
    outcome_date = Column(String(50), nullable=True)

    # User info
    analyst = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)


class ComparableAnalysis(Base, UUIDMixin, TimestampMixin):
    """Comparable property analysis record."""

    __tablename__ = "ml_comparable_analyses"

    subject_property_id = Column(String(100), nullable=True, index=True)
    subject_address = Column(String(255), nullable=True)

    # Subject property features
    subject_features = Column(JSON, nullable=False, comment="Subject property features")

    # Comparables found
    num_comparables = Column(Integer, nullable=False, comment="Number of comps found")
    comparables_data = Column(JSON, nullable=False, comment="Comparable properties data")

    # Valuation results
    indicated_value = Column(Float, nullable=False, comment="Indicated value from comps")
    min_adjusted_value = Column(Float, nullable=True)
    max_adjusted_value = Column(Float, nullable=True)
    mean_adjusted_value = Column(Float, nullable=True)
    std_dev = Column(Float, nullable=True, comment="Standard deviation of adjusted values")

    # Filters applied
    filters_applied = Column(JSON, nullable=True, comment="Filters used in comp selection")

    # User info
    analyst = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)


class AnomalyDetectionResult(Base, UUIDMixin, TimestampMixin):
    """Anomaly detection result record."""

    __tablename__ = "ml_anomaly_detections"

    entity_type = Column(String(100), nullable=False, comment="Type of entity analyzed")
    entity_id = Column(String(100), nullable=True, index=True, comment="Reference to entity")

    # Detection method
    detection_method = Column(String(100), nullable=False, comment="Detection method used")
    contamination = Column(Float, nullable=True, comment="Expected anomaly rate")

    # Results
    total_records = Column(Integer, nullable=False, comment="Total records analyzed")
    anomalies_found = Column(Integer, nullable=False, comment="Number of anomalies detected")
    anomaly_rate = Column(Float, nullable=False, comment="Actual anomaly rate")

    # Anomaly details
    anomalies = Column(JSON, nullable=False, comment="Detailed anomaly information")

    # Summary statistics
    summary_stats = Column(JSON, nullable=True, comment="Summary statistics of data")

    # User info
    analyst = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)


class NLQueryHistory(Base, UUIDMixin, TimestampMixin):
    """Natural language query history."""

    __tablename__ = "ml_nl_query_history"

    query_text = Column(Text, nullable=False, comment="Natural language query")
    parsed_query = Column(JSON, nullable=False, comment="Parsed query structure")

    # Results
    results_count = Column(Integer, nullable=False, comment="Number of results returned")
    execution_time_ms = Column(Integer, nullable=True, comment="Query execution time")

    # Data source
    data_source = Column(String(100), nullable=True, comment="Data source queried")

    # User info
    user_id = Column(String(100), nullable=True, index=True)
    session_id = Column(String(100), nullable=True, comment="User session identifier")


__all__ = [
    "PropertyValuationPrediction",
    "MarketTrendForecast",
    "DealSuccessPrediction",
    "ComparableAnalysis",
    "AnomalyDetectionResult",
    "NLQueryHistory",
]
