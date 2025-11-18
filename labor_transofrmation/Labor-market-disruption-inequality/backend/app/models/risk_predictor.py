import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
import joblib
from typing import Dict, List
import os

class JobLossRiskPredictor:
    """
    ML model to predict job loss risk based on:
    - Industry automation trends
    - Skill obsolescence
    - Market demand shifts
    - Worker adaptability factors
    """

    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = [
            'years_experience',
            'education_level_encoded',
            'industry_automation_risk',
            'skill_demand_avg',
            'skill_automation_risk_avg',
            'skill_diversity_score',
            'recent_skill_acquisition',
            'age_category',
            'remote_capability'
        ]

    def _encode_education(self, education_level: str) -> int:
        """Encode education level to numeric"""
        education_mapping = {
            'high_school': 1,
            'associate': 2,
            'bachelor': 3,
            'master': 4,
            'phd': 5
        }
        return education_mapping.get(education_level.lower(), 2)

    def _get_industry_automation_risk(self, industry: str) -> float:
        """Get automation risk score for industry (0-100)"""
        # Based on research data - these are example values
        industry_risks = {
            'manufacturing': 85,
            'retail': 75,
            'transportation': 80,
            'food_service': 70,
            'administrative': 65,
            'healthcare': 30,
            'education': 25,
            'technology': 20,
            'creative': 15,
            'management': 35
        }
        return industry_risks.get(industry.lower(), 50)

    def prepare_features(self, worker_data: Dict) -> np.ndarray:
        """
        Prepare features from worker data

        Args:
            worker_data: Dictionary containing worker information

        Returns:
            Feature array for prediction
        """
        features = [
            worker_data.get('years_experience', 0),
            self._encode_education(worker_data.get('education_level', 'bachelor')),
            self._get_industry_automation_risk(worker_data.get('current_industry', 'technology')),
            worker_data.get('skill_demand_avg', 50),
            worker_data.get('skill_automation_risk_avg', 50),
            worker_data.get('skill_diversity_score', 5),
            worker_data.get('recent_skill_acquisition', 0),
            worker_data.get('age_category', 2),
            worker_data.get('remote_capability', 0.5)
        ]

        return np.array([features])

    def train(self, training_data: List[Dict], labels: List[float]):
        """
        Train the risk prediction model

        Args:
            training_data: List of worker data dictionaries
            labels: Risk scores (0-100)
        """
        X = np.array([self.prepare_features(data).flatten() for data in training_data])
        y = np.array(labels)

        X_scaled = self.scaler.fit_transform(X)

        self.model = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        self.model.fit(X_scaled, y)

    def predict_risk(self, worker_data: Dict) -> Dict[str, float]:
        """
        Predict job loss risk for a worker

        Args:
            worker_data: Worker information dictionary

        Returns:
            Dictionary with risk score and confidence
        """
        if self.model is None:
            # If model not trained, use rule-based estimation
            return self._rule_based_prediction(worker_data)

        features = self.prepare_features(worker_data)
        features_scaled = self.scaler.transform(features)

        risk_score = float(self.model.predict(features_scaled)[0])
        risk_score = max(0, min(100, risk_score))  # Clamp to 0-100

        return {
            'risk_score': round(risk_score, 2),
            'risk_level': self._categorize_risk(risk_score),
            'confidence': 0.85,
            'factors': self._identify_risk_factors(worker_data, risk_score)
        }

    def _rule_based_prediction(self, worker_data: Dict) -> Dict[str, float]:
        """Fallback rule-based prediction when model is not trained"""
        industry_risk = self._get_industry_automation_risk(
            worker_data.get('current_industry', 'technology')
        )
        skill_risk = worker_data.get('skill_automation_risk_avg', 50)
        skill_demand = worker_data.get('skill_demand_avg', 50)

        # Weighted calculation
        risk_score = (
            industry_risk * 0.4 +
            skill_risk * 0.3 +
            (100 - skill_demand) * 0.3
        )

        return {
            'risk_score': round(risk_score, 2),
            'risk_level': self._categorize_risk(risk_score),
            'confidence': 0.65,
            'factors': self._identify_risk_factors(worker_data, risk_score)
        }

    def _categorize_risk(self, score: float) -> str:
        """Categorize risk score into levels"""
        if score < 30:
            return 'low'
        elif score < 60:
            return 'medium'
        else:
            return 'high'

    def _identify_risk_factors(self, worker_data: Dict, risk_score: float) -> List[Dict]:
        """Identify key risk factors contributing to the score"""
        factors = []

        industry_risk = self._get_industry_automation_risk(
            worker_data.get('current_industry', 'technology')
        )
        if industry_risk > 60:
            factors.append({
                'factor': 'industry_automation',
                'impact': 'high',
                'description': 'Industry has high automation risk'
            })

        skill_risk = worker_data.get('skill_automation_risk_avg', 50)
        if skill_risk > 60:
            factors.append({
                'factor': 'skill_obsolescence',
                'impact': 'high',
                'description': 'Current skills at risk of automation'
            })

        skill_diversity = worker_data.get('skill_diversity_score', 5)
        if skill_diversity < 3:
            factors.append({
                'factor': 'low_skill_diversity',
                'impact': 'medium',
                'description': 'Limited skill portfolio reduces adaptability'
            })

        return factors

    def save_model(self, path: str = 'models/risk_predictor.pkl'):
        """Save trained model to disk"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler
        }, path)

    def load_model(self, path: str = 'models/risk_predictor.pkl'):
        """Load trained model from disk"""
        if os.path.exists(path):
            data = joblib.load(path)
            self.model = data['model']
            self.scaler = data['scaler']
            return True
        return False
