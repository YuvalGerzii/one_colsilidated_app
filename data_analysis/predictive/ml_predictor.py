"""
Machine Learning Predictive Modeling Module
============================================

Advanced ML models for prediction including XGBoost, Random Forest,
Gradient Boosting, and ensemble methods.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Union
from sklearn.model_selection import (
    cross_val_score, GridSearchCV, RandomizedSearchCV,
    TimeSeriesSplit
)
from sklearn.metrics import (
    mean_absolute_error, mean_squared_error, r2_score,
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, classification_report
)
import warnings

warnings.filterwarnings('ignore')


class MLPredictor:
    """
    Advanced machine learning predictor with multiple algorithms
    and hyperparameter optimization.
    """

    def __init__(self):
        self.models = {}
        self.best_model = None
        self.best_params = {}
        self.feature_importance = {}
        self.metrics = {}

    def train_xgboost(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray = None,
        y_val: np.ndarray = None,
        task: str = 'regression',
        params: Dict = None,
        tune: bool = False
    ) -> Dict:
        """
        Train XGBoost model.

        Args:
            X_train: Training features
            y_train: Training target
            X_val: Validation features
            y_val: Validation target
            task: 'regression' or 'classification'
            params: Model parameters
            tune: Whether to tune hyperparameters

        Returns:
            Training results
        """
        try:
            import xgboost as xgb
        except ImportError:
            return {"error": "xgboost not installed"}

        default_params = {
            'n_estimators': 100,
            'max_depth': 6,
            'learning_rate': 0.1,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'reg_alpha': 0,
            'reg_lambda': 1,
            'random_state': 42
        }

        if params:
            default_params.update(params)

        if task == 'regression':
            model = xgb.XGBRegressor(**default_params)
        else:
            model = xgb.XGBClassifier(**default_params)

        if tune:
            param_grid = {
                'n_estimators': [50, 100, 200],
                'max_depth': [3, 5, 7],
                'learning_rate': [0.01, 0.1, 0.3]
            }
            grid_search = GridSearchCV(model, param_grid, cv=3, scoring='neg_mean_squared_error' if task == 'regression' else 'accuracy')
            grid_search.fit(X_train, y_train)
            model = grid_search.best_estimator_
            self.best_params['xgboost'] = grid_search.best_params_
        else:
            eval_set = [(X_train, y_train)]
            if X_val is not None:
                eval_set.append((X_val, y_val))
            model.fit(X_train, y_train, eval_set=eval_set, verbose=False)

        self.models['xgboost'] = model

        # Feature importance
        importance = dict(zip(range(X_train.shape[1]), model.feature_importances_))
        self.feature_importance['xgboost'] = importance

        return {
            'model': 'XGBoost',
            'params': model.get_params(),
            'n_features': X_train.shape[1],
            'feature_importance': importance
        }

    def train_random_forest(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        task: str = 'regression',
        params: Dict = None,
        tune: bool = False
    ) -> Dict:
        """
        Train Random Forest model.

        Args:
            X_train: Training features
            y_train: Training target
            task: 'regression' or 'classification'
            params: Model parameters
            tune: Whether to tune hyperparameters

        Returns:
            Training results
        """
        from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier

        default_params = {
            'n_estimators': 100,
            'max_depth': None,
            'min_samples_split': 2,
            'min_samples_leaf': 1,
            'random_state': 42
        }

        if params:
            default_params.update(params)

        if task == 'regression':
            model = RandomForestRegressor(**default_params)
        else:
            model = RandomForestClassifier(**default_params)

        if tune:
            param_grid = {
                'n_estimators': [50, 100, 200],
                'max_depth': [5, 10, None],
                'min_samples_split': [2, 5, 10]
            }
            grid_search = GridSearchCV(model, param_grid, cv=3)
            grid_search.fit(X_train, y_train)
            model = grid_search.best_estimator_
            self.best_params['random_forest'] = grid_search.best_params_
        else:
            model.fit(X_train, y_train)

        self.models['random_forest'] = model

        importance = dict(zip(range(X_train.shape[1]), model.feature_importances_))
        self.feature_importance['random_forest'] = importance

        return {
            'model': 'Random Forest',
            'params': model.get_params(),
            'n_estimators': model.n_estimators,
            'feature_importance': importance
        }

    def train_gradient_boosting(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        task: str = 'regression',
        params: Dict = None
    ) -> Dict:
        """
        Train Gradient Boosting model.

        Args:
            X_train: Training features
            y_train: Training target
            task: 'regression' or 'classification'
            params: Model parameters

        Returns:
            Training results
        """
        from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier

        default_params = {
            'n_estimators': 100,
            'max_depth': 3,
            'learning_rate': 0.1,
            'subsample': 0.8,
            'random_state': 42
        }

        if params:
            default_params.update(params)

        if task == 'regression':
            model = GradientBoostingRegressor(**default_params)
        else:
            model = GradientBoostingClassifier(**default_params)

        model.fit(X_train, y_train)
        self.models['gradient_boosting'] = model

        importance = dict(zip(range(X_train.shape[1]), model.feature_importances_))
        self.feature_importance['gradient_boosting'] = importance

        return {
            'model': 'Gradient Boosting',
            'params': model.get_params(),
            'feature_importance': importance
        }

    def train_lightgbm(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray = None,
        y_val: np.ndarray = None,
        task: str = 'regression',
        params: Dict = None
    ) -> Dict:
        """
        Train LightGBM model.

        Args:
            X_train: Training features
            y_train: Training target
            X_val: Validation features
            y_val: Validation target
            task: 'regression' or 'classification'
            params: Model parameters

        Returns:
            Training results
        """
        try:
            import lightgbm as lgb
        except ImportError:
            return {"error": "lightgbm not installed"}

        default_params = {
            'n_estimators': 100,
            'max_depth': -1,
            'learning_rate': 0.1,
            'num_leaves': 31,
            'random_state': 42,
            'verbosity': -1
        }

        if params:
            default_params.update(params)

        if task == 'regression':
            model = lgb.LGBMRegressor(**default_params)
        else:
            model = lgb.LGBMClassifier(**default_params)

        callbacks = []
        eval_set = None
        if X_val is not None:
            eval_set = [(X_val, y_val)]

        model.fit(X_train, y_train, eval_set=eval_set, callbacks=callbacks)
        self.models['lightgbm'] = model

        importance = dict(zip(range(X_train.shape[1]), model.feature_importances_))
        self.feature_importance['lightgbm'] = importance

        return {
            'model': 'LightGBM',
            'params': model.get_params(),
            'feature_importance': importance
        }

    def train_catboost(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        task: str = 'regression',
        params: Dict = None
    ) -> Dict:
        """
        Train CatBoost model.

        Args:
            X_train: Training features
            y_train: Training target
            task: 'regression' or 'classification'
            params: Model parameters

        Returns:
            Training results
        """
        try:
            from catboost import CatBoostRegressor, CatBoostClassifier
        except ImportError:
            return {"error": "catboost not installed"}

        default_params = {
            'iterations': 100,
            'depth': 6,
            'learning_rate': 0.1,
            'random_state': 42,
            'verbose': False
        }

        if params:
            default_params.update(params)

        if task == 'regression':
            model = CatBoostRegressor(**default_params)
        else:
            model = CatBoostClassifier(**default_params)

        model.fit(X_train, y_train)
        self.models['catboost'] = model

        importance = dict(zip(range(X_train.shape[1]), model.feature_importances_))
        self.feature_importance['catboost'] = importance

        return {
            'model': 'CatBoost',
            'params': default_params,
            'feature_importance': importance
        }

    def train_elastic_net(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        alpha: float = 1.0,
        l1_ratio: float = 0.5
    ) -> Dict:
        """
        Train Elastic Net model.

        Args:
            X_train: Training features
            y_train: Training target
            alpha: Regularization strength
            l1_ratio: L1/L2 ratio

        Returns:
            Training results
        """
        from sklearn.linear_model import ElasticNet

        model = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
        model.fit(X_train, y_train)
        self.models['elastic_net'] = model

        return {
            'model': 'Elastic Net',
            'alpha': alpha,
            'l1_ratio': l1_ratio,
            'n_features': X_train.shape[1]
        }

    def train_svr(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        kernel: str = 'rbf',
        C: float = 1.0
    ) -> Dict:
        """
        Train Support Vector Regression.

        Args:
            X_train: Training features
            y_train: Training target
            kernel: Kernel type
            C: Regularization parameter

        Returns:
            Training results
        """
        from sklearn.svm import SVR
        from sklearn.preprocessing import StandardScaler

        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X_train)

        model = SVR(kernel=kernel, C=C)
        model.fit(X_scaled, y_train)

        self.models['svr'] = {'model': model, 'scaler': scaler}

        return {
            'model': 'SVR',
            'kernel': kernel,
            'C': C
        }

    def predict(
        self,
        model_name: str,
        X: np.ndarray
    ) -> np.ndarray:
        """
        Make predictions using trained model.

        Args:
            model_name: Name of model to use
            X: Features for prediction

        Returns:
            Predictions
        """
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not trained")

        model = self.models[model_name]

        if model_name == 'svr':
            X_scaled = model['scaler'].transform(X)
            return model['model'].predict(X_scaled)

        return model.predict(X)

    def predict_proba(
        self,
        model_name: str,
        X: np.ndarray
    ) -> np.ndarray:
        """
        Get prediction probabilities (classification only).

        Args:
            model_name: Name of model to use
            X: Features for prediction

        Returns:
            Probability predictions
        """
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not trained")

        model = self.models[model_name]

        if hasattr(model, 'predict_proba'):
            return model.predict_proba(X)
        else:
            raise ValueError(f"Model {model_name} does not support probability predictions")

    def evaluate(
        self,
        model_name: str,
        X_test: np.ndarray,
        y_test: np.ndarray,
        task: str = 'regression'
    ) -> Dict[str, float]:
        """
        Evaluate model performance.

        Args:
            model_name: Name of model to evaluate
            X_test: Test features
            y_test: Test target
            task: 'regression' or 'classification'

        Returns:
            Dictionary of metrics
        """
        y_pred = self.predict(model_name, X_test)

        if task == 'regression':
            metrics = {
                'MAE': round(mean_absolute_error(y_test, y_pred), 4),
                'MSE': round(mean_squared_error(y_test, y_pred), 4),
                'RMSE': round(np.sqrt(mean_squared_error(y_test, y_pred)), 4),
                'R2': round(r2_score(y_test, y_pred), 4)
            }

            # MAPE
            mask = y_test != 0
            if mask.sum() > 0:
                mape = np.mean(np.abs((y_test[mask] - y_pred[mask]) / y_test[mask])) * 100
                metrics['MAPE'] = round(mape, 2)

        else:
            metrics = {
                'Accuracy': round(accuracy_score(y_test, y_pred), 4),
                'Precision': round(precision_score(y_test, y_pred, average='weighted'), 4),
                'Recall': round(recall_score(y_test, y_pred, average='weighted'), 4),
                'F1': round(f1_score(y_test, y_pred, average='weighted'), 4)
            }

            # AUC for binary classification
            if len(np.unique(y_test)) == 2:
                y_proba = self.predict_proba(model_name, X_test)[:, 1]
                metrics['AUC'] = round(roc_auc_score(y_test, y_proba), 4)

        self.metrics[model_name] = metrics
        return metrics

    def cross_validate(
        self,
        model_name: str,
        X: np.ndarray,
        y: np.ndarray,
        cv: int = 5,
        scoring: str = 'neg_mean_squared_error'
    ) -> Dict:
        """
        Cross-validate model.

        Args:
            model_name: Name of model
            X: Features
            y: Target
            cv: Number of folds
            scoring: Scoring metric

        Returns:
            Cross-validation results
        """
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not trained")

        model = self.models[model_name]
        if isinstance(model, dict):
            model = model['model']

        scores = cross_val_score(model, X, y, cv=cv, scoring=scoring)

        return {
            'mean_score': round(-scores.mean() if 'neg' in scoring else scores.mean(), 4),
            'std_score': round(scores.std(), 4),
            'scores': [-s if 'neg' in scoring else s for s in scores.round(4)]
        }

    def time_series_cv(
        self,
        model_name: str,
        X: np.ndarray,
        y: np.ndarray,
        n_splits: int = 5
    ) -> Dict:
        """
        Time series cross-validation.

        Args:
            model_name: Name of model
            X: Features
            y: Target
            n_splits: Number of splits

        Returns:
            Cross-validation results
        """
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not trained")

        model = self.models[model_name]
        tscv = TimeSeriesSplit(n_splits=n_splits)

        scores = cross_val_score(model, X, y, cv=tscv, scoring='neg_mean_squared_error')

        return {
            'mean_rmse': round(np.sqrt(-scores.mean()), 4),
            'std_rmse': round(np.sqrt(-scores).std(), 4),
            'fold_rmse': [round(np.sqrt(-s), 4) for s in scores]
        }

    def compare_models(
        self,
        X_test: np.ndarray,
        y_test: np.ndarray,
        task: str = 'regression'
    ) -> pd.DataFrame:
        """
        Compare all trained models.

        Args:
            X_test: Test features
            y_test: Test target
            task: 'regression' or 'classification'

        Returns:
            DataFrame with model comparison
        """
        results = []

        for model_name in self.models.keys():
            metrics = self.evaluate(model_name, X_test, y_test, task)
            metrics['Model'] = model_name
            results.append(metrics)

        df = pd.DataFrame(results)

        # Sort by primary metric
        if task == 'regression':
            df = df.sort_values('RMSE')
        else:
            df = df.sort_values('F1', ascending=False)

        return df

    def get_best_model(
        self,
        X_test: np.ndarray,
        y_test: np.ndarray,
        task: str = 'regression',
        metric: str = None
    ) -> str:
        """
        Get the best performing model.

        Args:
            X_test: Test features
            y_test: Test target
            task: 'regression' or 'classification'
            metric: Metric to use for comparison

        Returns:
            Name of best model
        """
        comparison = self.compare_models(X_test, y_test, task)

        if metric is None:
            metric = 'RMSE' if task == 'regression' else 'F1'

        if task == 'regression':
            best_idx = comparison[metric].idxmin()
        else:
            best_idx = comparison[metric].idxmax()

        self.best_model = comparison.loc[best_idx, 'Model']
        return self.best_model

    def ensemble_predict(
        self,
        X: np.ndarray,
        model_names: List[str] = None,
        weights: Dict[str, float] = None,
        method: str = 'average'
    ) -> np.ndarray:
        """
        Ensemble prediction from multiple models.

        Args:
            X: Features
            model_names: Models to include
            weights: Model weights
            method: 'average' or 'weighted'

        Returns:
            Ensemble predictions
        """
        if model_names is None:
            model_names = list(self.models.keys())

        predictions = []
        for name in model_names:
            if name in self.models:
                pred = self.predict(name, X)
                predictions.append(pred)

        predictions = np.array(predictions)

        if method == 'average':
            return np.mean(predictions, axis=0)
        elif method == 'weighted' and weights:
            weighted_preds = np.zeros(predictions.shape[1])
            total_weight = sum(weights.get(name, 1) for name in model_names)
            for i, name in enumerate(model_names):
                weight = weights.get(name, 1) / total_weight
                weighted_preds += weight * predictions[i]
            return weighted_preds

        return np.mean(predictions, axis=0)

    def get_feature_importance_summary(self) -> pd.DataFrame:
        """
        Get feature importance summary across all models.

        Returns:
            DataFrame with feature importances
        """
        if not self.feature_importance:
            return pd.DataFrame()

        # Get all feature indices
        all_features = set()
        for importance in self.feature_importance.values():
            all_features.update(importance.keys())

        # Build summary
        data = []
        for feature in sorted(all_features):
            row = {'Feature': feature}
            for model, importance in self.feature_importance.items():
                row[model] = round(importance.get(feature, 0), 4)
            data.append(row)

        df = pd.DataFrame(data)

        # Add average importance
        importance_cols = [col for col in df.columns if col != 'Feature']
        if importance_cols:
            df['Average'] = df[importance_cols].mean(axis=1)
            df = df.sort_values('Average', ascending=False)

        return df
