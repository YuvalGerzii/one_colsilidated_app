"""
AutoML and Smart Model Selection
=================================

Automated machine learning with intelligent model selection,
hyperparameter optimization, and feature selection.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Union, Any
from sklearn.model_selection import cross_val_score, TimeSeriesSplit
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import warnings
import time

warnings.filterwarnings('ignore')


class AutoML:
    """
    Automated Machine Learning for time series and tabular data.
    """

    def __init__(self, task: str = 'regression', time_budget: int = 300):
        """
        Initialize AutoML.

        Args:
            task: 'regression' or 'classification'
            time_budget: Maximum time in seconds
        """
        self.task = task
        self.time_budget = time_budget
        self.best_model = None
        self.best_params = {}
        self.best_score = None
        self.results = []
        self.feature_importance = {}

    def _get_model_configs(self) -> List[Dict]:
        """Get model configurations to try."""
        from sklearn.linear_model import Ridge, Lasso, ElasticNet
        from sklearn.ensemble import (
            RandomForestRegressor, RandomForestClassifier,
            GradientBoostingRegressor, GradientBoostingClassifier,
            ExtraTreesRegressor, ExtraTreesClassifier
        )
        from sklearn.svm import SVR, SVC

        if self.task == 'regression':
            return [
                {
                    'name': 'Ridge',
                    'model': Ridge,
                    'params': [
                        {'alpha': 0.1},
                        {'alpha': 1.0},
                        {'alpha': 10.0}
                    ]
                },
                {
                    'name': 'Lasso',
                    'model': Lasso,
                    'params': [
                        {'alpha': 0.01},
                        {'alpha': 0.1},
                        {'alpha': 1.0}
                    ]
                },
                {
                    'name': 'ElasticNet',
                    'model': ElasticNet,
                    'params': [
                        {'alpha': 0.1, 'l1_ratio': 0.5},
                        {'alpha': 1.0, 'l1_ratio': 0.5}
                    ]
                },
                {
                    'name': 'RandomForest',
                    'model': RandomForestRegressor,
                    'params': [
                        {'n_estimators': 50, 'max_depth': 5, 'random_state': 42},
                        {'n_estimators': 100, 'max_depth': 10, 'random_state': 42},
                        {'n_estimators': 200, 'max_depth': None, 'random_state': 42}
                    ]
                },
                {
                    'name': 'GradientBoosting',
                    'model': GradientBoostingRegressor,
                    'params': [
                        {'n_estimators': 50, 'max_depth': 3, 'learning_rate': 0.1, 'random_state': 42},
                        {'n_estimators': 100, 'max_depth': 5, 'learning_rate': 0.05, 'random_state': 42}
                    ]
                },
                {
                    'name': 'ExtraTrees',
                    'model': ExtraTreesRegressor,
                    'params': [
                        {'n_estimators': 100, 'max_depth': 10, 'random_state': 42},
                        {'n_estimators': 200, 'max_depth': None, 'random_state': 42}
                    ]
                }
            ]
        else:
            return [
                {
                    'name': 'RandomForest',
                    'model': RandomForestClassifier,
                    'params': [
                        {'n_estimators': 100, 'max_depth': 10, 'random_state': 42},
                        {'n_estimators': 200, 'max_depth': None, 'random_state': 42}
                    ]
                },
                {
                    'name': 'GradientBoosting',
                    'model': GradientBoostingClassifier,
                    'params': [
                        {'n_estimators': 100, 'max_depth': 5, 'learning_rate': 0.1, 'random_state': 42}
                    ]
                }
            ]

    def fit(
        self,
        X: np.ndarray,
        y: np.ndarray,
        cv: int = 5,
        time_series: bool = False
    ) -> Dict:
        """
        Fit AutoML to find best model.

        Args:
            X: Features
            y: Target
            cv: Cross-validation folds
            time_series: Use time series CV

        Returns:
            Results dictionary
        """
        start_time = time.time()
        configs = self._get_model_configs()

        # Determine CV strategy
        if time_series:
            cv_strategy = TimeSeriesSplit(n_splits=cv)
        else:
            cv_strategy = cv

        # Scoring metric
        scoring = 'neg_mean_squared_error' if self.task == 'regression' else 'accuracy'

        best_score = -np.inf
        best_model = None
        best_params = {}
        best_name = ''

        for config in configs:
            if time.time() - start_time > self.time_budget:
                break

            for params in config['params']:
                if time.time() - start_time > self.time_budget:
                    break

                try:
                    model = config['model'](**params)
                    scores = cross_val_score(model, X, y, cv=cv_strategy, scoring=scoring)
                    mean_score = scores.mean()

                    self.results.append({
                        'model': config['name'],
                        'params': params,
                        'score': round(-mean_score if 'neg' in scoring else mean_score, 6),
                        'std': round(scores.std(), 6)
                    })

                    if mean_score > best_score:
                        best_score = mean_score
                        best_model = model
                        best_params = params
                        best_name = config['name']

                except Exception as e:
                    continue

        # Refit best model on full data
        if best_model is not None:
            best_model.fit(X, y)
            self.best_model = best_model
            self.best_params = best_params
            self.best_score = -best_score if 'neg' in scoring else best_score

            # Feature importance
            if hasattr(best_model, 'feature_importances_'):
                self.feature_importance = dict(zip(
                    range(X.shape[1]),
                    best_model.feature_importances_
                ))

        return {
            'best_model': best_name,
            'best_params': best_params,
            'best_score': round(self.best_score, 6) if self.best_score else None,
            'n_models_tried': len(self.results),
            'time_elapsed': round(time.time() - start_time, 2)
        }

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions with best model."""
        if self.best_model is None:
            raise ValueError("Model not fitted yet")
        return self.best_model.predict(X)

    def get_leaderboard(self) -> pd.DataFrame:
        """Get sorted leaderboard of all tried models."""
        df = pd.DataFrame(self.results)
        return df.sort_values('score').head(20)


class SmartFeatureSelector:
    """
    Intelligent feature selection using multiple methods.
    """

    def __init__(self):
        self.selected_features = []
        self.feature_scores = {}
        self.methods_results = {}

    def select_features(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        n_features: int = 20,
        task: str = 'regression'
    ) -> List[str]:
        """
        Smart feature selection combining multiple methods.

        Args:
            X: Feature DataFrame
            y: Target
            n_features: Number of features to select
            task: 'regression' or 'classification'

        Returns:
            List of selected feature names
        """
        from sklearn.feature_selection import (
            mutual_info_regression, mutual_info_classif,
            f_regression, f_classif
        )
        from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier

        feature_names = X.columns.tolist()
        scores = {name: 0 for name in feature_names}

        # 1. Correlation-based (for regression)
        if task == 'regression':
            correlations = X.apply(lambda col: abs(col.corr(y)))
            for name, corr in correlations.items():
                scores[name] += corr if not np.isnan(corr) else 0
            self.methods_results['correlation'] = correlations.to_dict()

        # 2. Mutual Information
        if task == 'regression':
            mi_scores = mutual_info_regression(X, y)
        else:
            mi_scores = mutual_info_classif(X, y)

        mi_normalized = mi_scores / (mi_scores.max() + 1e-10)
        for name, score in zip(feature_names, mi_normalized):
            scores[name] += score
        self.methods_results['mutual_info'] = dict(zip(feature_names, mi_scores))

        # 3. F-statistic
        if task == 'regression':
            f_scores, _ = f_regression(X, y)
        else:
            f_scores, _ = f_classif(X, y)

        f_normalized = f_scores / (np.nanmax(f_scores) + 1e-10)
        for name, score in zip(feature_names, f_normalized):
            if not np.isnan(score):
                scores[name] += score
        self.methods_results['f_statistic'] = dict(zip(feature_names, f_scores))

        # 4. Random Forest importance
        if task == 'regression':
            rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
        else:
            rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)

        rf.fit(X, y)
        rf_scores = rf.feature_importances_
        rf_normalized = rf_scores / (rf_scores.max() + 1e-10)
        for name, score in zip(feature_names, rf_normalized):
            scores[name] += score
        self.methods_results['random_forest'] = dict(zip(feature_names, rf_scores))

        # 5. Variance threshold
        variances = X.var()
        var_normalized = variances / (variances.max() + 1e-10)
        for name, var in var_normalized.items():
            scores[name] += var * 0.5  # Lower weight
        self.methods_results['variance'] = variances.to_dict()

        # Rank and select
        self.feature_scores = scores
        sorted_features = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        self.selected_features = [f[0] for f in sorted_features[:n_features]]

        return self.selected_features

    def get_feature_report(self) -> pd.DataFrame:
        """Get detailed feature selection report."""
        if not self.feature_scores:
            return pd.DataFrame()

        data = []
        for name, score in self.feature_scores.items():
            row = {'Feature': name, 'Total_Score': round(score, 4)}
            for method, method_scores in self.methods_results.items():
                row[method] = round(method_scores.get(name, 0), 4)
            data.append(row)

        df = pd.DataFrame(data)
        return df.sort_values('Total_Score', ascending=False)


class HyperparameterOptimizer:
    """
    Bayesian-style hyperparameter optimization.
    """

    def __init__(self, n_iterations: int = 50):
        self.n_iterations = n_iterations
        self.history = []
        self.best_params = {}
        self.best_score = None

    def optimize(
        self,
        model_class,
        param_space: Dict[str, Tuple],
        X: np.ndarray,
        y: np.ndarray,
        cv: int = 5,
        scoring: str = 'neg_mean_squared_error'
    ) -> Dict:
        """
        Optimize hyperparameters using random search with adaptive sampling.

        Args:
            model_class: Model class to optimize
            param_space: Parameter ranges {name: (min, max, type)}
            X: Features
            y: Target
            cv: Cross-validation folds
            scoring: Scoring metric

        Returns:
            Best parameters and score
        """
        best_score = -np.inf
        best_params = {}

        for i in range(self.n_iterations):
            # Sample parameters
            params = {}
            for name, (min_val, max_val, param_type) in param_space.items():
                if param_type == 'int':
                    params[name] = np.random.randint(min_val, max_val + 1)
                elif param_type == 'float':
                    params[name] = np.random.uniform(min_val, max_val)
                elif param_type == 'log':
                    params[name] = np.exp(np.random.uniform(np.log(min_val), np.log(max_val)))
                elif param_type == 'choice':
                    params[name] = np.random.choice(min_val)  # min_val is list of choices

            try:
                model = model_class(**params)
                scores = cross_val_score(model, X, y, cv=cv, scoring=scoring)
                mean_score = scores.mean()

                self.history.append({
                    'iteration': i,
                    'params': params.copy(),
                    'score': -mean_score if 'neg' in scoring else mean_score
                })

                if mean_score > best_score:
                    best_score = mean_score
                    best_params = params.copy()

            except:
                continue

        self.best_params = best_params
        self.best_score = -best_score if 'neg' in scoring else best_score

        return {
            'best_params': best_params,
            'best_score': round(self.best_score, 6),
            'n_iterations': len(self.history)
        }

    def get_optimization_history(self) -> pd.DataFrame:
        """Get optimization history."""
        return pd.DataFrame(self.history)


class SmartPreprocessor:
    """
    Intelligent preprocessing that adapts to data characteristics.
    """

    def __init__(self):
        self.transformations = []
        self.scalers = {}
        self.recommendations = []

    def analyze_and_preprocess(
        self,
        df: pd.DataFrame,
        target_column: str = None
    ) -> Tuple[pd.DataFrame, List[str]]:
        """
        Analyze data and apply smart preprocessing.

        Args:
            df: Input DataFrame
            target_column: Target variable

        Returns:
            Tuple of (processed DataFrame, recommendations)
        """
        df = df.copy()
        recommendations = []

        # 1. Handle data types
        for col in df.columns:
            if col == target_column:
                continue

            # Convert object to numeric if possible
            if df[col].dtype == 'object':
                try:
                    df[col] = pd.to_numeric(df[col], errors='raise')
                    recommendations.append(f"Converted {col} to numeric")
                except:
                    # Check cardinality for encoding decision
                    cardinality = df[col].nunique()
                    if cardinality <= 10:
                        dummies = pd.get_dummies(df[col], prefix=col, drop_first=True)
                        df = pd.concat([df.drop(columns=[col]), dummies], axis=1)
                        recommendations.append(f"One-hot encoded {col} ({cardinality} categories)")
                    else:
                        # Label encode high cardinality
                        df[col] = df[col].astype('category').cat.codes
                        recommendations.append(f"Label encoded {col} ({cardinality} categories)")

        # 2. Handle missing values intelligently
        for col in df.select_dtypes(include=[np.number]).columns:
            missing_pct = df[col].isna().sum() / len(df) * 100

            if missing_pct > 0:
                if missing_pct > 50:
                    df = df.drop(columns=[col])
                    recommendations.append(f"Dropped {col} ({missing_pct:.1f}% missing)")
                elif missing_pct < 5:
                    df[col] = df[col].fillna(df[col].median())
                    recommendations.append(f"Filled {col} with median ({missing_pct:.1f}% missing)")
                else:
                    # Use interpolation for moderate missing
                    df[col] = df[col].interpolate(method='linear').fillna(method='bfill').fillna(method='ffill')
                    recommendations.append(f"Interpolated {col} ({missing_pct:.1f}% missing)")

        # 3. Handle skewness
        for col in df.select_dtypes(include=[np.number]).columns:
            if col == target_column:
                continue

            skew = df[col].skew()
            if abs(skew) > 2 and df[col].min() >= 0:
                df[col] = np.log1p(df[col])
                recommendations.append(f"Log-transformed {col} (skewness: {skew:.2f})")

        # 4. Handle outliers
        for col in df.select_dtypes(include=[np.number]).columns:
            if col == target_column:
                continue

            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((df[col] < Q1 - 3*IQR) | (df[col] > Q3 + 3*IQR)).sum()

            if outliers > len(df) * 0.01:  # More than 1% outliers
                df[col] = df[col].clip(Q1 - 3*IQR, Q3 + 3*IQR)
                recommendations.append(f"Clipped {outliers} outliers in {col}")

        # 5. Scale features
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if target_column in numeric_cols:
            numeric_cols.remove(target_column)

        if numeric_cols:
            scaler = StandardScaler()
            df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
            self.scalers['standard'] = scaler
            recommendations.append(f"Standardized {len(numeric_cols)} numeric features")

        self.recommendations = recommendations
        return df, recommendations

    def get_recommendations(self) -> List[str]:
        """Get preprocessing recommendations."""
        return self.recommendations.copy()
