"""
Advanced Feature Engineering Module
====================================

Comprehensive feature engineering for creating predictive features
from raw data, including lag features, rolling statistics, and interactions.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Union
from scipy import stats
from sklearn.feature_selection import (
    SelectKBest, f_classif, f_regression,
    mutual_info_classif, mutual_info_regression,
    RFE
)
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import warnings

warnings.filterwarnings('ignore')


class FeatureEngineer:
    """
    Advanced feature engineering class for creating, selecting,
    and transforming features for machine learning models.
    """

    def __init__(self):
        self.feature_importance = {}
        self.selected_features = []
        self.created_features = []

    def create_lag_features(
        self,
        df: pd.DataFrame,
        columns: List[str],
        lags: List[int] = [1, 7, 14, 30],
        group_by: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Create lag features for time series analysis.

        Args:
            df: Input DataFrame
            columns: Columns to create lags for
            lags: List of lag periods
            group_by: Optional column to group by before creating lags

        Returns:
            DataFrame with lag features
        """
        df = df.copy()

        for col in columns:
            for lag in lags:
                new_col = f"{col}_lag_{lag}"
                if group_by:
                    df[new_col] = df.groupby(group_by)[col].shift(lag)
                else:
                    df[new_col] = df[col].shift(lag)
                self.created_features.append(new_col)

        return df

    def create_rolling_features(
        self,
        df: pd.DataFrame,
        columns: List[str],
        windows: List[int] = [7, 14, 30, 90],
        functions: List[str] = ['mean', 'std', 'min', 'max'],
        group_by: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Create rolling window statistics.

        Args:
            df: Input DataFrame
            columns: Columns to calculate rolling stats for
            windows: Window sizes
            functions: Aggregation functions
            group_by: Optional grouping column

        Returns:
            DataFrame with rolling features
        """
        df = df.copy()

        for col in columns:
            for window in windows:
                for func in functions:
                    new_col = f"{col}_rolling_{window}_{func}"

                    if group_by:
                        grouped = df.groupby(group_by)[col]
                        if func == 'mean':
                            df[new_col] = grouped.transform(lambda x: x.rolling(window, min_periods=1).mean())
                        elif func == 'std':
                            df[new_col] = grouped.transform(lambda x: x.rolling(window, min_periods=1).std())
                        elif func == 'min':
                            df[new_col] = grouped.transform(lambda x: x.rolling(window, min_periods=1).min())
                        elif func == 'max':
                            df[new_col] = grouped.transform(lambda x: x.rolling(window, min_periods=1).max())
                        elif func == 'sum':
                            df[new_col] = grouped.transform(lambda x: x.rolling(window, min_periods=1).sum())
                        elif func == 'median':
                            df[new_col] = grouped.transform(lambda x: x.rolling(window, min_periods=1).median())
                    else:
                        rolling = df[col].rolling(window, min_periods=1)
                        df[new_col] = getattr(rolling, func)()

                    self.created_features.append(new_col)

        return df

    def create_expanding_features(
        self,
        df: pd.DataFrame,
        columns: List[str],
        functions: List[str] = ['mean', 'std', 'min', 'max'],
        group_by: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Create expanding window statistics (cumulative).

        Args:
            df: Input DataFrame
            columns: Columns to calculate expanding stats for
            functions: Aggregation functions
            group_by: Optional grouping column

        Returns:
            DataFrame with expanding features
        """
        df = df.copy()

        for col in columns:
            for func in functions:
                new_col = f"{col}_expanding_{func}"

                if group_by:
                    grouped = df.groupby(group_by)[col]
                    df[new_col] = grouped.transform(lambda x: getattr(x.expanding(min_periods=1), func)())
                else:
                    df[new_col] = getattr(df[col].expanding(min_periods=1), func)()

                self.created_features.append(new_col)

        return df

    def create_diff_features(
        self,
        df: pd.DataFrame,
        columns: List[str],
        periods: List[int] = [1, 7, 30],
        pct_change: bool = True
    ) -> pd.DataFrame:
        """
        Create difference and percentage change features.

        Args:
            df: Input DataFrame
            columns: Columns to create diffs for
            periods: Periods for differencing
            pct_change: Whether to include percentage change

        Returns:
            DataFrame with difference features
        """
        df = df.copy()

        for col in columns:
            for period in periods:
                # Absolute difference
                diff_col = f"{col}_diff_{period}"
                df[diff_col] = df[col].diff(period)
                self.created_features.append(diff_col)

                # Percentage change
                if pct_change:
                    pct_col = f"{col}_pct_change_{period}"
                    df[pct_col] = df[col].pct_change(period)
                    self.created_features.append(pct_col)

        return df

    def create_interaction_features(
        self,
        df: pd.DataFrame,
        columns: List[str],
        operations: List[str] = ['multiply', 'divide', 'add', 'subtract']
    ) -> pd.DataFrame:
        """
        Create interaction features between columns.

        Args:
            df: Input DataFrame
            columns: Columns to create interactions for
            operations: Types of interactions

        Returns:
            DataFrame with interaction features
        """
        df = df.copy()

        for i, col1 in enumerate(columns):
            for col2 in columns[i+1:]:
                if 'multiply' in operations:
                    new_col = f"{col1}_x_{col2}"
                    df[new_col] = df[col1] * df[col2]
                    self.created_features.append(new_col)

                if 'divide' in operations:
                    new_col = f"{col1}_div_{col2}"
                    df[new_col] = df[col1] / (df[col2] + 1e-10)
                    self.created_features.append(new_col)

                if 'add' in operations:
                    new_col = f"{col1}_plus_{col2}"
                    df[new_col] = df[col1] + df[col2]
                    self.created_features.append(new_col)

                if 'subtract' in operations:
                    new_col = f"{col1}_minus_{col2}"
                    df[new_col] = df[col1] - df[col2]
                    self.created_features.append(new_col)

        return df

    def create_polynomial_features(
        self,
        df: pd.DataFrame,
        columns: List[str],
        degree: int = 2
    ) -> pd.DataFrame:
        """
        Create polynomial features.

        Args:
            df: Input DataFrame
            columns: Columns for polynomial expansion
            degree: Polynomial degree

        Returns:
            DataFrame with polynomial features
        """
        df = df.copy()

        for col in columns:
            for d in range(2, degree + 1):
                new_col = f"{col}_pow_{d}"
                df[new_col] = df[col] ** d
                self.created_features.append(new_col)

        return df

    def create_cyclical_features(
        self,
        df: pd.DataFrame,
        column: str,
        max_value: int
    ) -> pd.DataFrame:
        """
        Create cyclical encoding for periodic features.

        Args:
            df: Input DataFrame
            column: Column to encode
            max_value: Maximum value in the cycle

        Returns:
            DataFrame with cyclical features
        """
        df = df.copy()

        sin_col = f"{column}_sin"
        cos_col = f"{column}_cos"

        df[sin_col] = np.sin(2 * np.pi * df[column] / max_value)
        df[cos_col] = np.cos(2 * np.pi * df[column] / max_value)

        self.created_features.extend([sin_col, cos_col])

        return df

    def create_target_encoding(
        self,
        df: pd.DataFrame,
        categorical_columns: List[str],
        target_column: str,
        smoothing: float = 1.0
    ) -> pd.DataFrame:
        """
        Create target encoding for categorical variables.

        Args:
            df: Input DataFrame
            categorical_columns: Columns to encode
            target_column: Target variable
            smoothing: Smoothing factor

        Returns:
            DataFrame with target encoded features
        """
        df = df.copy()
        global_mean = df[target_column].mean()

        for col in categorical_columns:
            # Calculate category statistics
            agg = df.groupby(col)[target_column].agg(['mean', 'count'])
            counts = agg['count']
            means = agg['mean']

            # Apply smoothing
            smooth = (counts * means + smoothing * global_mean) / (counts + smoothing)

            # Map to dataframe
            new_col = f"{col}_target_encoded"
            df[new_col] = df[col].map(smooth)
            self.created_features.append(new_col)

        return df

    def create_statistical_features(
        self,
        df: pd.DataFrame,
        columns: List[str]
    ) -> pd.DataFrame:
        """
        Create row-wise statistical features across columns.

        Args:
            df: Input DataFrame
            columns: Columns to aggregate

        Returns:
            DataFrame with statistical features
        """
        df = df.copy()

        prefix = '_'.join(columns[:2]) + '_etc'

        df[f'{prefix}_mean'] = df[columns].mean(axis=1)
        df[f'{prefix}_std'] = df[columns].std(axis=1)
        df[f'{prefix}_min'] = df[columns].min(axis=1)
        df[f'{prefix}_max'] = df[columns].max(axis=1)
        df[f'{prefix}_range'] = df[columns].max(axis=1) - df[columns].min(axis=1)
        df[f'{prefix}_skew'] = df[columns].skew(axis=1)
        df[f'{prefix}_kurtosis'] = df[columns].kurtosis(axis=1)

        new_features = [f'{prefix}_{stat}' for stat in ['mean', 'std', 'min', 'max', 'range', 'skew', 'kurtosis']]
        self.created_features.extend(new_features)

        return df

    def select_features_univariate(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        k: int = 10,
        task: str = 'regression'
    ) -> Tuple[List[str], np.ndarray]:
        """
        Select features using univariate statistical tests.

        Args:
            X: Feature DataFrame
            y: Target variable
            k: Number of features to select
            task: 'regression' or 'classification'

        Returns:
            Tuple of (selected feature names, scores)
        """
        if task == 'regression':
            selector = SelectKBest(score_func=f_regression, k=min(k, len(X.columns)))
        else:
            selector = SelectKBest(score_func=f_classif, k=min(k, len(X.columns)))

        selector.fit(X, y)
        scores = selector.scores_

        # Get selected feature names
        selected_mask = selector.get_support()
        selected_features = X.columns[selected_mask].tolist()

        self.selected_features = selected_features
        self.feature_importance['univariate'] = dict(zip(X.columns, scores))

        return selected_features, scores

    def select_features_mutual_info(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        k: int = 10,
        task: str = 'regression'
    ) -> Tuple[List[str], np.ndarray]:
        """
        Select features using mutual information.

        Args:
            X: Feature DataFrame
            y: Target variable
            k: Number of features to select
            task: 'regression' or 'classification'

        Returns:
            Tuple of (selected feature names, scores)
        """
        if task == 'regression':
            mi_scores = mutual_info_regression(X, y)
        else:
            mi_scores = mutual_info_classif(X, y)

        # Sort features by MI score
        feature_scores = dict(zip(X.columns, mi_scores))
        sorted_features = sorted(feature_scores.items(), key=lambda x: x[1], reverse=True)
        selected_features = [f[0] for f in sorted_features[:k]]

        self.selected_features = selected_features
        self.feature_importance['mutual_info'] = feature_scores

        return selected_features, mi_scores

    def select_features_rfe(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        n_features: int = 10,
        task: str = 'regression'
    ) -> List[str]:
        """
        Select features using Recursive Feature Elimination.

        Args:
            X: Feature DataFrame
            y: Target variable
            n_features: Number of features to select
            task: 'regression' or 'classification'

        Returns:
            List of selected feature names
        """
        if task == 'regression':
            estimator = RandomForestRegressor(n_estimators=50, random_state=42)
        else:
            estimator = RandomForestClassifier(n_estimators=50, random_state=42)

        rfe = RFE(estimator, n_features_to_select=min(n_features, len(X.columns)))
        rfe.fit(X, y)

        selected_features = X.columns[rfe.support_].tolist()
        self.selected_features = selected_features

        return selected_features

    def get_feature_importance_rf(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        task: str = 'regression'
    ) -> Dict[str, float]:
        """
        Get feature importance using Random Forest.

        Args:
            X: Feature DataFrame
            y: Target variable
            task: 'regression' or 'classification'

        Returns:
            Dictionary of feature importances
        """
        if task == 'regression':
            model = RandomForestRegressor(n_estimators=100, random_state=42)
        else:
            model = RandomForestClassifier(n_estimators=100, random_state=42)

        model.fit(X, y)
        importances = dict(zip(X.columns, model.feature_importances_))

        # Sort by importance
        sorted_importances = dict(sorted(importances.items(), key=lambda x: x[1], reverse=True))
        self.feature_importance['random_forest'] = sorted_importances

        return sorted_importances

    def create_time_series_features(
        self,
        df: pd.DataFrame,
        target_column: str,
        date_column: Optional[str] = None,
        lags: List[int] = [1, 7, 14, 30],
        rolling_windows: List[int] = [7, 14, 30],
        include_diff: bool = True
    ) -> pd.DataFrame:
        """
        Comprehensive time series feature engineering.

        Args:
            df: Input DataFrame
            target_column: Target variable
            date_column: Datetime column
            lags: Lag periods
            rolling_windows: Rolling window sizes
            include_diff: Include difference features

        Returns:
            DataFrame with time series features
        """
        df = df.copy()

        # Create lag features
        df = self.create_lag_features(df, [target_column], lags)

        # Create rolling features
        df = self.create_rolling_features(
            df, [target_column], rolling_windows,
            functions=['mean', 'std', 'min', 'max']
        )

        # Create expanding features
        df = self.create_expanding_features(
            df, [target_column],
            functions=['mean', 'std']
        )

        # Create difference features
        if include_diff:
            df = self.create_diff_features(df, [target_column], periods=[1, 7, 30])

        # Add date features if date column provided
        if date_column and date_column in df.columns:
            df[date_column] = pd.to_datetime(df[date_column])

            # Cyclical encoding for month and day of week
            if 'month' not in df.columns:
                df['month'] = df[date_column].dt.month
            if 'dayofweek' not in df.columns:
                df['dayofweek'] = df[date_column].dt.dayofweek

            df = self.create_cyclical_features(df, 'month', 12)
            df = self.create_cyclical_features(df, 'dayofweek', 7)

        return df

    def get_created_features(self) -> List[str]:
        """Get list of all created features."""
        return self.created_features.copy()

    def get_feature_importance_report(self) -> Dict:
        """Get comprehensive feature importance report."""
        return self.feature_importance.copy()
