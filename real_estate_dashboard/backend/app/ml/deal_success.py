"""
Deal Success Probability Predictor

Predicts the likelihood of deal success based on:
- Deal characteristics
- Buyer/seller profiles
- Market conditions
- Historical deal outcomes
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
import joblib
from pathlib import Path

logger = logging.getLogger(__name__)


class DealSuccessPredictor:
    """
    ML-based predictor for deal success probability.

    Uses ensemble classification to predict likelihood of deal closing.
    """

    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize the deal success predictor.

        Args:
            model_path: Path to saved model, if None creates new model
        """
        self.model_path = model_path
        self.rf_model = None
        self.gb_model = None
        self.scaler = StandardScaler()
        self.feature_names = []
        self.is_trained = False

        if model_path and Path(model_path).exists():
            self.load_model(model_path)

    def prepare_features(self, deals: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Prepare features from deal data.

        Args:
            deals: List of deal dictionaries with features

        Returns:
            DataFrame with prepared features
        """
        df = pd.DataFrame(deals)

        # Numeric features
        numeric_features = []

        # Deal value metrics
        if 'deal_value' in df.columns:
            numeric_features.append('deal_value')

        if 'asking_price' in df.columns and 'offer_price' in df.columns:
            df['offer_to_asking_ratio'] = df['offer_price'] / df['asking_price']
            numeric_features.append('offer_to_asking_ratio')

        # Financing features
        if 'down_payment_percent' in df.columns:
            numeric_features.append('down_payment_percent')

        if 'loan_to_value' in df.columns:
            numeric_features.append('loan_to_value')

        # Buyer profile
        if 'buyer_credit_score' in df.columns:
            numeric_features.append('buyer_credit_score')

        if 'buyer_previous_purchases' in df.columns:
            numeric_features.append('buyer_previous_purchases')

        # Property features
        if 'property_age' in df.columns:
            numeric_features.append('property_age')

        if 'inspection_issues_count' in df.columns:
            numeric_features.append('inspection_issues_count')

        # Market conditions
        if 'days_on_market' in df.columns:
            numeric_features.append('days_on_market')

        if 'market_inventory' in df.columns:
            numeric_features.append('market_inventory')

        # Deal stage duration
        if 'time_to_offer' in df.columns:
            numeric_features.append('time_to_offer')

        # Categorical encodings
        if 'property_type' in df.columns:
            df['property_type_encoded'] = pd.Categorical(df['property_type']).codes
            numeric_features.append('property_type_encoded')

        if 'financing_type' in df.columns:
            df['financing_type_encoded'] = pd.Categorical(df['financing_type']).codes
            numeric_features.append('financing_type_encoded')

        if 'buyer_type' in df.columns:
            df['buyer_type_encoded'] = pd.Categorical(df['buyer_type']).codes
            numeric_features.append('buyer_type_encoded')

        # Binary flags
        binary_features = [
            'has_contingencies',
            'cash_offer',
            'pre_approved',
            'seller_motivated',
            'competitive_offers'
        ]

        for feature in binary_features:
            if feature in df.columns:
                df[feature] = df[feature].astype(int)
                numeric_features.append(feature)

        # Select available features
        available_features = [f for f in numeric_features if f in df.columns]
        self.feature_names = available_features

        return df[available_features].fillna(df[available_features].median())

    def train(
        self,
        deals: List[Dict[str, Any]],
        outcomes: List[bool],
        test_size: float = 0.2,
        save_path: Optional[str] = None
    ) -> Dict[str, float]:
        """
        Train the deal success prediction models.

        Args:
            deals: List of deal feature dictionaries
            outcomes: List of deal outcomes (True = success, False = failed)
            test_size: Fraction of data for testing
            save_path: Path to save trained model

        Returns:
            Dictionary with training metrics
        """
        logger.info(f"Training deal success model on {len(deals)} samples")

        # Prepare features
        X = self.prepare_features(deals)
        y = np.array(outcomes).astype(int)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )

        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        # Train Random Forest
        logger.info("Training Random Forest classifier...")
        self.rf_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=20,
            random_state=42,
            n_jobs=-1,
            class_weight='balanced'
        )
        self.rf_model.fit(X_train_scaled, y_train)

        # Train Gradient Boosting
        logger.info("Training Gradient Boosting classifier...")
        self.gb_model = GradientBoostingClassifier(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=42
        )
        self.gb_model.fit(X_train_scaled, y_train)

        # Evaluate
        rf_pred = self.rf_model.predict(X_test_scaled)
        gb_pred = self.gb_model.predict(X_test_scaled)

        # Ensemble predictions (voting)
        ensemble_pred = ((rf_pred + gb_pred) >= 1).astype(int)

        # Get probability scores
        rf_proba = self.rf_model.predict_proba(X_test_scaled)[:, 1]
        gb_proba = self.gb_model.predict_proba(X_test_scaled)[:, 1]
        ensemble_proba = (rf_proba + gb_proba) / 2

        metrics = {
            'rf_accuracy': float(accuracy_score(y_test, rf_pred)),
            'gb_accuracy': float(accuracy_score(y_test, gb_pred)),
            'ensemble_accuracy': float(accuracy_score(y_test, ensemble_pred)),
            'ensemble_precision': float(precision_score(y_test, ensemble_pred)),
            'ensemble_recall': float(recall_score(y_test, ensemble_pred)),
            'ensemble_auc': float(roc_auc_score(y_test, ensemble_proba)),
            'n_features': len(self.feature_names),
            'n_samples': len(deals),
            'success_rate': float(y.mean())
        }

        self.is_trained = True

        logger.info(
            f"Training complete: Accuracy={metrics['ensemble_accuracy']:.3f}, "
            f"AUC={metrics['ensemble_auc']:.3f}"
        )

        # Save model
        if save_path:
            self.save_model(save_path)

        return metrics

    def predict(
        self,
        deals: List[Dict[str, Any]],
        return_factors: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Predict deal success probability.

        Args:
            deals: List of deal feature dictionaries
            return_factors: Whether to return contributing factors

        Returns:
            List of predictions with probabilities and factors
        """
        if not self.is_trained:
            raise ValueError("Model not trained. Call train() first or load a trained model.")

        # Prepare features
        X = self.prepare_features(deals)
        X_scaled = self.scaler.transform(X)

        # Get predictions from both models
        rf_proba = self.rf_model.predict_proba(X_scaled)[:, 1]
        gb_proba = self.gb_model.predict_proba(X_scaled)[:, 1]

        # Ensemble probability (average)
        ensemble_proba = (rf_proba + gb_proba) / 2

        results = []
        for i, prob in enumerate(ensemble_proba):
            result = {
                'success_probability': float(prob),
                'predicted_outcome': 'success' if prob >= 0.5 else 'likely_to_fail',
                'confidence': float(abs(prob - 0.5) * 2),  # 0-1 scale
                'rf_probability': float(rf_proba[i]),
                'gb_probability': float(gb_proba[i])
            }

            # Add risk level
            if prob >= 0.75:
                result['risk_level'] = 'low'
            elif prob >= 0.5:
                result['risk_level'] = 'medium'
            else:
                result['risk_level'] = 'high'

            if return_factors:
                # Calculate feature contributions (simplified)
                feature_values = X.iloc[i].to_dict()
                feature_importance = self.get_feature_importance()

                # Top positive and negative factors
                factors = []
                for feature, value in feature_values.items():
                    importance = feature_importance.get(feature, 0)
                    factors.append({
                        'feature': feature,
                        'value': float(value),
                        'importance': float(importance)
                    })

                # Sort by importance
                factors.sort(key=lambda x: x['importance'], reverse=True)
                result['top_factors'] = factors[:5]

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
        rf_importance = self.rf_model.feature_importances_
        gb_importance = self.gb_model.feature_importances_
        avg_importance = (rf_importance + gb_importance) / 2

        return dict(zip(self.feature_names, avg_importance.tolist()))

    def save_model(self, path: str):
        """Save trained model to disk."""
        model_data = {
            'rf_model': self.rf_model,
            'gb_model': self.gb_model,
            'scaler': self.scaler,
            'feature_names': self.feature_names,
            'is_trained': self.is_trained
        }
        joblib.dump(model_data, path)
        logger.info(f"Model saved to {path}")

    def load_model(self, path: str):
        """Load trained model from disk."""
        model_data = joblib.load(path)
        self.rf_model = model_data['rf_model']
        self.gb_model = model_data['gb_model']
        self.scaler = model_data['scaler']
        self.feature_names = model_data['feature_names']
        self.is_trained = model_data['is_trained']
        logger.info(f"Model loaded from {path}")


def generate_sample_deal_data(n_samples: int = 1000) -> Tuple[List[Dict], List[bool]]:
    """
    Generate synthetic deal data for demonstration.

    Args:
        n_samples: Number of samples to generate

    Returns:
        Tuple of (deals, outcomes)
    """
    np.random.seed(42)

    deals = []
    outcomes = []

    for _ in range(n_samples):
        # Generate deal features
        deal_value = np.random.randint(200000, 2000000)
        asking_price = deal_value * np.random.uniform(0.95, 1.05)
        offer_price = asking_price * np.random.uniform(0.85, 1.0)
        down_payment_percent = np.random.uniform(10, 40)
        buyer_credit_score = np.random.randint(550, 850)
        days_on_market = np.random.randint(1, 180)
        inspection_issues = np.random.randint(0, 15)

        # Calculate success probability based on realistic factors
        prob_success = 0.5

        # Strong positive factors
        if offer_price / asking_price > 0.95:
            prob_success += 0.15
        if buyer_credit_score > 750:
            prob_success += 0.15
        if down_payment_percent > 25:
            prob_success += 0.1
        if days_on_market < 30:
            prob_success += 0.05

        # Negative factors
        if inspection_issues > 8:
            prob_success -= 0.15
        if buyer_credit_score < 650:
            prob_success -= 0.2
        if down_payment_percent < 15:
            prob_success -= 0.1

        # Random flags
        cash_offer = np.random.random() < 0.2
        pre_approved = np.random.random() < 0.7
        seller_motivated = np.random.random() < 0.3

        if cash_offer:
            prob_success += 0.2
        if pre_approved:
            prob_success += 0.1
        if seller_motivated:
            prob_success += 0.1

        prob_success = np.clip(prob_success, 0.05, 0.95)
        success = np.random.random() < prob_success

        deals.append({
            'deal_value': deal_value,
            'asking_price': asking_price,
            'offer_price': offer_price,
            'down_payment_percent': down_payment_percent,
            'loan_to_value': 100 - down_payment_percent,
            'buyer_credit_score': buyer_credit_score,
            'buyer_previous_purchases': np.random.randint(0, 5),
            'property_age': np.random.randint(0, 100),
            'inspection_issues_count': inspection_issues,
            'days_on_market': days_on_market,
            'market_inventory': np.random.randint(500, 5000),
            'time_to_offer': np.random.randint(1, 60),
            'property_type': np.random.choice(['single_family', 'condo', 'townhouse', 'multi_family']),
            'financing_type': np.random.choice(['conventional', 'fha', 'va', 'cash']),
            'buyer_type': np.random.choice(['first_time', 'investor', 'upgrading']),
            'has_contingencies': np.random.choice([0, 1]),
            'cash_offer': int(cash_offer),
            'pre_approved': int(pre_approved),
            'seller_motivated': int(seller_motivated),
            'competitive_offers': np.random.choice([0, 1])
        })
        outcomes.append(success)

    return deals, outcomes
