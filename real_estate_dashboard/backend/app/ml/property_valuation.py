"""
Property Valuation Predictor using Machine Learning

Uses XGBoost and Random Forest for accurate property valuations based on:
- Location features
- Property characteristics
- Market conditions
- Historical sales data
"""

import logging
from typing import Dict, List, Optional, Any
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import xgboost as xgb
import joblib
from pathlib import Path

logger = logging.getLogger(__name__)


class PropertyValuationPredictor:
    """
    ML-based property valuation predictor.

    Uses ensemble methods (XGBoost + Random Forest) for robust predictions.
    """

    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize the property valuation predictor.

        Args:
            model_path: Path to saved model, if None creates new model
        """
        self.model_path = model_path
        self.xgb_model = None
        self.rf_model = None
        self.scaler = StandardScaler()
        self.feature_names = []
        self.is_trained = False

        if model_path and Path(model_path).exists():
            self.load_model(model_path)

    def prepare_features(self, properties: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Prepare features from property data.

        Args:
            properties: List of property dictionaries with features

        Returns:
            DataFrame with prepared features
        """
        df = pd.DataFrame(properties)

        # Core features
        feature_columns = [
            'square_feet',
            'bedrooms',
            'bathrooms',
            'year_built',
            'lot_size',
            'garage_spaces',
            'stories'
        ]

        # Location features (simplified - in production use proper geocoding)
        if 'zip_code' in df.columns:
            df['zip_code_encoded'] = pd.Categorical(df['zip_code']).codes
            feature_columns.append('zip_code_encoded')

        # Property type encoding
        if 'property_type' in df.columns:
            df['property_type_encoded'] = pd.Categorical(df['property_type']).codes
            feature_columns.append('property_type_encoded')

        # Condition encoding
        if 'condition' in df.columns:
            condition_map = {
                'poor': 1, 'fair': 2, 'average': 3, 'good': 4, 'excellent': 5
            }
            df['condition_score'] = df['condition'].map(condition_map).fillna(3)
            feature_columns.append('condition_score')

        # Derived features
        if 'square_feet' in df.columns and 'lot_size' in df.columns:
            df['building_to_lot_ratio'] = df['square_feet'] / (df['lot_size'] + 1)
            feature_columns.append('building_to_lot_ratio')

        if 'year_built' in df.columns:
            current_year = 2025
            df['age'] = current_year - df['year_built']
            feature_columns.append('age')

        # Select only available features
        available_features = [col for col in feature_columns if col in df.columns]
        self.feature_names = available_features

        return df[available_features].fillna(df[available_features].median())

    def train(
        self,
        properties: List[Dict[str, Any]],
        prices: List[float],
        test_size: float = 0.2,
        save_path: Optional[str] = None
    ) -> Dict[str, float]:
        """
        Train the valuation models.

        Args:
            properties: List of property feature dictionaries
            prices: List of corresponding prices
            test_size: Fraction of data for testing
            save_path: Path to save trained model

        Returns:
            Dictionary with training metrics
        """
        logger.info(f"Training property valuation model on {len(properties)} samples")

        # Prepare features
        X = self.prepare_features(properties)
        y = np.array(prices)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )

        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        # Train XGBoost
        logger.info("Training XGBoost model...")
        self.xgb_model = xgb.XGBRegressor(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42,
            n_jobs=-1
        )
        self.xgb_model.fit(X_train_scaled, y_train)

        # Train Random Forest
        logger.info("Training Random Forest model...")
        self.rf_model = RandomForestRegressor(
            n_estimators=100,
            max_depth=15,
            random_state=42,
            n_jobs=-1
        )
        self.rf_model.fit(X_train_scaled, y_train)

        # Evaluate
        xgb_score = self.xgb_model.score(X_test_scaled, y_test)
        rf_score = self.rf_model.score(X_test_scaled, y_test)

        # Ensemble predictions
        xgb_pred = self.xgb_model.predict(X_test_scaled)
        rf_pred = self.rf_model.predict(X_test_scaled)
        ensemble_pred = (xgb_pred + rf_pred) / 2

        # Calculate MAPE (Mean Absolute Percentage Error)
        mape = np.mean(np.abs((y_test - ensemble_pred) / y_test)) * 100

        self.is_trained = True

        metrics = {
            'xgb_r2': float(xgb_score),
            'rf_r2': float(rf_score),
            'ensemble_mape': float(mape),
            'n_features': len(self.feature_names),
            'n_samples': len(properties)
        }

        logger.info(f"Training complete: XGBoost R²={xgb_score:.3f}, RF R²={rf_score:.3f}, MAPE={mape:.2f}%")

        # Save model
        if save_path:
            self.save_model(save_path)

        return metrics

    def predict(
        self,
        properties: List[Dict[str, Any]],
        return_confidence: bool = True
    ) -> List[Dict[str, float]]:
        """
        Predict property values.

        Args:
            properties: List of property feature dictionaries
            return_confidence: Whether to return confidence intervals

        Returns:
            List of predictions with confidence intervals
        """
        if not self.is_trained:
            raise ValueError("Model not trained. Call train() first or load a trained model.")

        # Prepare features
        X = self.prepare_features(properties)
        X_scaled = self.scaler.transform(X)

        # Get predictions from both models
        xgb_pred = self.xgb_model.predict(X_scaled)
        rf_pred = self.rf_model.predict(X_scaled)

        # Ensemble prediction (average)
        ensemble_pred = (xgb_pred + rf_pred) / 2

        results = []
        for i, pred in enumerate(ensemble_pred):
            result = {
                'predicted_value': float(pred),
                'xgb_prediction': float(xgb_pred[i]),
                'rf_prediction': float(rf_pred[i])
            }

            if return_confidence:
                # Use model disagreement as confidence indicator
                disagreement = abs(xgb_pred[i] - rf_pred[i])
                confidence_interval = disagreement * 1.5  # Simple heuristic

                result.update({
                    'lower_bound': float(pred - confidence_interval),
                    'upper_bound': float(pred + confidence_interval),
                    'confidence_score': float(1.0 / (1.0 + disagreement / pred))  # 0-1 scale
                })

            results.append(result)

        return results

    def get_feature_importance(self) -> Dict[str, float]:
        """
        Get feature importance scores.

        Returns:
            Dictionary mapping feature names to importance scores
        """
        if not self.is_trained:
            raise ValueError("Model not trained.")

        # Average importance from both models
        xgb_importance = self.xgb_model.feature_importances_
        rf_importance = self.rf_model.feature_importances_
        avg_importance = (xgb_importance + rf_importance) / 2

        return dict(zip(self.feature_names, avg_importance.tolist()))

    def save_model(self, path: str):
        """Save trained model to disk."""
        model_data = {
            'xgb_model': self.xgb_model,
            'rf_model': self.rf_model,
            'scaler': self.scaler,
            'feature_names': self.feature_names,
            'is_trained': self.is_trained
        }
        joblib.dump(model_data, path)
        logger.info(f"Model saved to {path}")

    def load_model(self, path: str):
        """Load trained model from disk."""
        model_data = joblib.load(path)
        self.xgb_model = model_data['xgb_model']
        self.rf_model = model_data['rf_model']
        self.scaler = model_data['scaler']
        self.feature_names = model_data['feature_names']
        self.is_trained = model_data['is_trained']
        logger.info(f"Model loaded from {path}")


def generate_sample_training_data(n_samples: int = 1000) -> tuple:
    """
    Generate synthetic training data for demonstration.

    In production, this would be replaced with real MLS data.

    Args:
        n_samples: Number of samples to generate

    Returns:
        Tuple of (properties, prices)
    """
    np.random.seed(42)

    properties = []
    prices = []

    for _ in range(n_samples):
        # Generate property features
        square_feet = np.random.randint(800, 5000)
        bedrooms = np.random.randint(1, 6)
        bathrooms = np.random.randint(1, 5)
        year_built = np.random.randint(1950, 2024)
        lot_size = np.random.randint(2000, 20000)
        garage_spaces = np.random.randint(0, 4)
        stories = np.random.randint(1, 4)

        # Base price calculation with realistic factors
        base_price = 100  # price per sq ft
        location_factor = np.random.uniform(0.7, 2.5)  # Location premium/discount
        age_factor = 1.0 - (2024 - year_built) * 0.002  # Depreciation
        condition_factor = np.random.uniform(0.85, 1.15)

        price = (
            square_feet * base_price * location_factor * age_factor * condition_factor +
            bedrooms * 10000 +
            bathrooms * 8000 +
            garage_spaces * 5000
        )

        # Add some noise
        price *= np.random.uniform(0.95, 1.05)

        properties.append({
            'square_feet': square_feet,
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'year_built': year_built,
            'lot_size': lot_size,
            'garage_spaces': garage_spaces,
            'stories': stories,
            'property_type': np.random.choice(['single_family', 'condo', 'townhouse']),
            'condition': np.random.choice(['fair', 'average', 'good', 'excellent']),
            'zip_code': np.random.choice(['90210', '10001', '60601', '75201', '33139'])
        })
        prices.append(price)

    return properties, prices
