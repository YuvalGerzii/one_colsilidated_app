"""
Advanced Data Preprocessing Module
==================================

Comprehensive data preprocessing utilities for cleaning, transforming,
and preparing data for analysis and modeling.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Union
from scipy import stats
from sklearn.preprocessing import (
    StandardScaler, MinMaxScaler, RobustScaler,
    LabelEncoder, OneHotEncoder
)
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.decomposition import PCA
import warnings

warnings.filterwarnings('ignore')


class DataPreprocessor:
    """
    Advanced data preprocessing class for comprehensive data cleaning
    and transformation operations.
    """

    def __init__(self):
        self.scalers = {}
        self.encoders = {}
        self.imputers = {}
        self.column_stats = {}
        self.transformations_log = []

    def analyze_data_quality(self, df: pd.DataFrame) -> Dict:
        """
        Comprehensive data quality analysis.

        Args:
            df: Input DataFrame

        Returns:
            Dictionary containing data quality metrics
        """
        quality_report = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024 / 1024,
            'columns': {}
        }

        for col in df.columns:
            col_report = {
                'dtype': str(df[col].dtype),
                'missing_count': int(df[col].isna().sum()),
                'missing_percent': round(df[col].isna().sum() / len(df) * 100, 2),
                'unique_values': int(df[col].nunique()),
                'unique_percent': round(df[col].nunique() / len(df) * 100, 2)
            }

            # Numeric column statistics
            if pd.api.types.is_numeric_dtype(df[col]):
                col_report.update({
                    'mean': round(df[col].mean(), 4) if not df[col].isna().all() else None,
                    'std': round(df[col].std(), 4) if not df[col].isna().all() else None,
                    'min': round(df[col].min(), 4) if not df[col].isna().all() else None,
                    'max': round(df[col].max(), 4) if not df[col].isna().all() else None,
                    'skewness': round(df[col].skew(), 4) if not df[col].isna().all() else None,
                    'kurtosis': round(df[col].kurtosis(), 4) if not df[col].isna().all() else None,
                    'zeros_count': int((df[col] == 0).sum()),
                    'negative_count': int((df[col] < 0).sum())
                })

                # Outlier detection using IQR
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                outliers = ((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))).sum()
                col_report['outliers_iqr'] = int(outliers)

            quality_report['columns'][col] = col_report

        return quality_report

    def handle_missing_values(
        self,
        df: pd.DataFrame,
        strategy: str = 'auto',
        numeric_strategy: str = 'median',
        categorical_strategy: str = 'most_frequent',
        knn_neighbors: int = 5
    ) -> pd.DataFrame:
        """
        Handle missing values with multiple strategies.

        Args:
            df: Input DataFrame
            strategy: 'auto', 'simple', 'knn', or 'interpolate'
            numeric_strategy: Strategy for numeric columns ('mean', 'median', 'most_frequent')
            categorical_strategy: Strategy for categorical columns
            knn_neighbors: Number of neighbors for KNN imputation

        Returns:
            DataFrame with missing values handled
        """
        df = df.copy()

        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

        if strategy == 'auto':
            # Use different strategies based on missing percentage
            for col in df.columns:
                missing_pct = df[col].isna().sum() / len(df) * 100

                if missing_pct == 0:
                    continue
                elif missing_pct > 50:
                    # Drop column if more than 50% missing
                    df = df.drop(columns=[col])
                    self.transformations_log.append(f"Dropped column {col} (>50% missing)")
                elif col in numeric_cols:
                    if missing_pct < 5:
                        df[col] = df[col].fillna(df[col].median())
                    else:
                        # Use interpolation for time series-like data
                        df[col] = df[col].interpolate(method='linear').fillna(method='bfill').fillna(method='ffill')
                else:
                    df[col] = df[col].fillna(df[col].mode().iloc[0] if len(df[col].mode()) > 0 else 'Unknown')

        elif strategy == 'simple':
            # Simple imputation
            if numeric_cols:
                imputer = SimpleImputer(strategy=numeric_strategy)
                df[numeric_cols] = imputer.fit_transform(df[numeric_cols])
                self.imputers['numeric'] = imputer

            if categorical_cols:
                imputer = SimpleImputer(strategy=categorical_strategy)
                df[categorical_cols] = imputer.fit_transform(df[categorical_cols])
                self.imputers['categorical'] = imputer

        elif strategy == 'knn':
            # KNN imputation for numeric columns
            if numeric_cols:
                imputer = KNNImputer(n_neighbors=knn_neighbors)
                df[numeric_cols] = imputer.fit_transform(df[numeric_cols])
                self.imputers['knn'] = imputer

            # Simple imputation for categorical
            if categorical_cols:
                imputer = SimpleImputer(strategy=categorical_strategy)
                df[categorical_cols] = imputer.fit_transform(df[categorical_cols])

        elif strategy == 'interpolate':
            # Time series interpolation
            for col in numeric_cols:
                df[col] = df[col].interpolate(method='time' if isinstance(df.index, pd.DatetimeIndex) else 'linear')
                df[col] = df[col].fillna(method='bfill').fillna(method='ffill')

        self.transformations_log.append(f"Missing values handled using {strategy} strategy")
        return df

    def remove_outliers(
        self,
        df: pd.DataFrame,
        columns: Optional[List[str]] = None,
        method: str = 'iqr',
        threshold: float = 1.5
    ) -> pd.DataFrame:
        """
        Remove or cap outliers using various methods.

        Args:
            df: Input DataFrame
            columns: Columns to process (None for all numeric)
            method: 'iqr', 'zscore', or 'percentile'
            threshold: Threshold for outlier detection

        Returns:
            DataFrame with outliers handled
        """
        df = df.copy()

        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns.tolist()

        removed_count = 0

        for col in columns:
            if method == 'iqr':
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower = Q1 - threshold * IQR
                upper = Q3 + threshold * IQR

            elif method == 'zscore':
                mean = df[col].mean()
                std = df[col].std()
                lower = mean - threshold * std
                upper = mean + threshold * std

            elif method == 'percentile':
                lower = df[col].quantile(threshold / 100)
                upper = df[col].quantile(1 - threshold / 100)

            # Cap outliers instead of removing
            outliers = ((df[col] < lower) | (df[col] > upper)).sum()
            removed_count += outliers
            df[col] = df[col].clip(lower=lower, upper=upper)

        self.transformations_log.append(f"Capped {removed_count} outliers using {method} method")
        return df

    def scale_features(
        self,
        df: pd.DataFrame,
        columns: Optional[List[str]] = None,
        method: str = 'standard'
    ) -> pd.DataFrame:
        """
        Scale numeric features.

        Args:
            df: Input DataFrame
            columns: Columns to scale (None for all numeric)
            method: 'standard', 'minmax', or 'robust'

        Returns:
            Scaled DataFrame
        """
        df = df.copy()

        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns.tolist()

        if method == 'standard':
            scaler = StandardScaler()
        elif method == 'minmax':
            scaler = MinMaxScaler()
        elif method == 'robust':
            scaler = RobustScaler()
        else:
            raise ValueError(f"Unknown scaling method: {method}")

        df[columns] = scaler.fit_transform(df[columns])
        self.scalers[method] = scaler
        self.transformations_log.append(f"Scaled {len(columns)} columns using {method} method")

        return df

    def encode_categorical(
        self,
        df: pd.DataFrame,
        columns: Optional[List[str]] = None,
        method: str = 'auto'
    ) -> pd.DataFrame:
        """
        Encode categorical variables.

        Args:
            df: Input DataFrame
            columns: Columns to encode (None for all categorical)
            method: 'auto', 'label', 'onehot', or 'target'

        Returns:
            DataFrame with encoded categories
        """
        df = df.copy()

        if columns is None:
            columns = df.select_dtypes(include=['object', 'category']).columns.tolist()

        for col in columns:
            unique_count = df[col].nunique()

            if method == 'auto':
                # Use label encoding for high cardinality, one-hot for low
                if unique_count > 10:
                    encoder = LabelEncoder()
                    df[col] = encoder.fit_transform(df[col].astype(str))
                    self.encoders[col] = encoder
                else:
                    dummies = pd.get_dummies(df[col], prefix=col, drop_first=True)
                    df = pd.concat([df.drop(columns=[col]), dummies], axis=1)

            elif method == 'label':
                encoder = LabelEncoder()
                df[col] = encoder.fit_transform(df[col].astype(str))
                self.encoders[col] = encoder

            elif method == 'onehot':
                dummies = pd.get_dummies(df[col], prefix=col, drop_first=True)
                df = pd.concat([df.drop(columns=[col]), dummies], axis=1)

        self.transformations_log.append(f"Encoded {len(columns)} categorical columns using {method} method")
        return df

    def detect_and_convert_dtypes(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Automatically detect and convert column data types.

        Args:
            df: Input DataFrame

        Returns:
            DataFrame with optimized data types
        """
        df = df.copy()

        for col in df.columns:
            # Try to convert to numeric
            if df[col].dtype == 'object':
                try:
                    df[col] = pd.to_numeric(df[col], errors='raise')
                    continue
                except (ValueError, TypeError):
                    pass

                # Try to convert to datetime
                try:
                    df[col] = pd.to_datetime(df[col], errors='raise')
                    continue
                except (ValueError, TypeError):
                    pass

                # Convert to category if low cardinality
                if df[col].nunique() / len(df) < 0.5:
                    df[col] = df[col].astype('category')

            # Downcast numeric types
            elif pd.api.types.is_integer_dtype(df[col]):
                df[col] = pd.to_numeric(df[col], downcast='integer')
            elif pd.api.types.is_float_dtype(df[col]):
                df[col] = pd.to_numeric(df[col], downcast='float')

        self.transformations_log.append("Optimized data types")
        return df

    def create_time_features(
        self,
        df: pd.DataFrame,
        date_column: str,
        features: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Extract time-based features from datetime column.

        Args:
            df: Input DataFrame
            date_column: Name of datetime column
            features: List of features to extract

        Returns:
            DataFrame with time features
        """
        df = df.copy()

        if features is None:
            features = ['year', 'month', 'day', 'dayofweek', 'quarter',
                       'is_weekend', 'is_month_start', 'is_month_end']

        # Ensure datetime type
        df[date_column] = pd.to_datetime(df[date_column])

        if 'year' in features:
            df['year'] = df[date_column].dt.year
        if 'month' in features:
            df['month'] = df[date_column].dt.month
        if 'day' in features:
            df['day'] = df[date_column].dt.day
        if 'dayofweek' in features:
            df['dayofweek'] = df[date_column].dt.dayofweek
        if 'quarter' in features:
            df['quarter'] = df[date_column].dt.quarter
        if 'is_weekend' in features:
            df['is_weekend'] = (df[date_column].dt.dayofweek >= 5).astype(int)
        if 'is_month_start' in features:
            df['is_month_start'] = df[date_column].dt.is_month_start.astype(int)
        if 'is_month_end' in features:
            df['is_month_end'] = df[date_column].dt.is_month_end.astype(int)
        if 'hour' in features:
            df['hour'] = df[date_column].dt.hour
        if 'dayofyear' in features:
            df['dayofyear'] = df[date_column].dt.dayofyear
        if 'weekofyear' in features:
            df['weekofyear'] = df[date_column].dt.isocalendar().week

        self.transformations_log.append(f"Created {len(features)} time features from {date_column}")
        return df

    def apply_log_transform(
        self,
        df: pd.DataFrame,
        columns: Optional[List[str]] = None,
        method: str = 'log1p'
    ) -> pd.DataFrame:
        """
        Apply logarithmic transformation to reduce skewness.

        Args:
            df: Input DataFrame
            columns: Columns to transform
            method: 'log', 'log1p', or 'sqrt'

        Returns:
            Transformed DataFrame
        """
        df = df.copy()

        if columns is None:
            # Auto-detect skewed columns
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            columns = [col for col in numeric_cols
                      if abs(df[col].skew()) > 1 and df[col].min() >= 0]

        for col in columns:
            if method == 'log':
                df[col] = np.log(df[col].clip(lower=1e-10))
            elif method == 'log1p':
                df[col] = np.log1p(df[col].clip(lower=0))
            elif method == 'sqrt':
                df[col] = np.sqrt(df[col].clip(lower=0))

        self.transformations_log.append(f"Applied {method} transform to {len(columns)} columns")
        return df

    def reduce_dimensions(
        self,
        df: pd.DataFrame,
        n_components: int = 10,
        method: str = 'pca'
    ) -> Tuple[pd.DataFrame, object]:
        """
        Reduce dimensionality of dataset.

        Args:
            df: Input DataFrame (numeric only)
            n_components: Number of components to keep
            method: 'pca' or 'svd'

        Returns:
            Tuple of (reduced DataFrame, fitted reducer)
        """
        numeric_df = df.select_dtypes(include=[np.number])

        if method == 'pca':
            reducer = PCA(n_components=min(n_components, len(numeric_df.columns)))
            reduced = reducer.fit_transform(numeric_df)

        columns = [f'PC{i+1}' for i in range(reduced.shape[1])]
        reduced_df = pd.DataFrame(reduced, columns=columns, index=df.index)

        self.transformations_log.append(f"Reduced to {n_components} dimensions using {method}")
        return reduced_df, reducer

    def get_transformation_log(self) -> List[str]:
        """Get log of all transformations applied."""
        return self.transformations_log.copy()

    def full_preprocessing_pipeline(
        self,
        df: pd.DataFrame,
        target_column: Optional[str] = None,
        date_column: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Apply full preprocessing pipeline.

        Args:
            df: Input DataFrame
            target_column: Target variable (to exclude from certain operations)
            date_column: Datetime column for time features

        Returns:
            Fully preprocessed DataFrame
        """
        df = df.copy()

        # 1. Optimize data types
        df = self.detect_and_convert_dtypes(df)

        # 2. Handle missing values
        df = self.handle_missing_values(df, strategy='auto')

        # 3. Create time features if date column provided
        if date_column and date_column in df.columns:
            df = self.create_time_features(df, date_column)

        # 4. Remove outliers from numeric columns
        exclude = [target_column] if target_column else []
        numeric_cols = [c for c in df.select_dtypes(include=[np.number]).columns if c not in exclude]
        df = self.remove_outliers(df, columns=numeric_cols)

        # 5. Encode categorical variables
        df = self.encode_categorical(df, method='auto')

        # 6. Scale numeric features
        scale_cols = [c for c in df.select_dtypes(include=[np.number]).columns if c not in exclude]
        if scale_cols:
            df = self.scale_features(df, columns=scale_cols, method='standard')

        return df
