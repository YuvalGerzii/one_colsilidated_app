"""
Financial Anomaly Detection Module

Detects anomalies in financial data using:
- Isolation Forest for outlier detection
- Statistical methods for time series anomalies
- Pattern recognition for unusual transactions
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from scipy import stats

logger = logging.getLogger(__name__)


class AnomalyDetector:
    """
    Detect anomalies in real estate financial data.

    Uses multiple methods:
    - Isolation Forest for multivariate outliers
    - Statistical Z-score for univariate outliers
    - Rolling window analysis for time series anomalies
    """

    def __init__(self, contamination: float = 0.1):
        """
        Initialize the anomaly detector.

        Args:
            contamination: Expected proportion of outliers (0.1 = 10%)
        """
        self.contamination = contamination
        self.isolation_forest = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=100
        )
        self.scaler = StandardScaler()
        self.is_fitted = False

    def detect_multivariate_anomalies(
        self,
        data: List[Dict[str, Any]],
        features: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Detect multivariate anomalies using Isolation Forest.

        Args:
            data: List of data points (e.g., transactions, properties)
            features: List of feature names to use, if None uses all numeric

        Returns:
            List of anomaly detection results
        """
        logger.info(f"Detecting multivariate anomalies in {len(data)} records")

        df = pd.DataFrame(data)

        # Select numeric features
        if features is None:
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        else:
            numeric_cols = [col for col in features if col in df.columns]

        if not numeric_cols:
            raise ValueError("No numeric features found for anomaly detection")

        # Prepare data
        X = df[numeric_cols].fillna(df[numeric_cols].median())

        # Fit and predict
        predictions = self.isolation_forest.fit_predict(X)
        scores = self.isolation_forest.score_samples(X)

        # Normalize scores to 0-1 range (higher = more anomalous)
        anomaly_scores = 1 / (1 + np.exp(scores))

        results = []
        for i, (pred, score) in enumerate(zip(predictions, anomaly_scores)):
            result = {
                'index': i,
                'is_anomaly': bool(pred == -1),
                'anomaly_score': float(score),
                'data_point': data[i]
            }

            # Add feature contributions
            if pred == -1:
                result['anomalous_features'] = self._identify_anomalous_features(
                    X.iloc[i],
                    X,
                    numeric_cols
                )

            results.append(result)

        n_anomalies = sum(1 for r in results if r['is_anomaly'])
        logger.info(f"Detected {n_anomalies} anomalies ({n_anomalies/len(data)*100:.1f}%)")

        return results

    def detect_univariate_anomalies(
        self,
        data: List[Dict[str, Any]],
        feature: str,
        z_threshold: float = 3.0
    ) -> List[Dict[str, Any]]:
        """
        Detect univariate anomalies using Z-score method.

        Args:
            data: List of data points
            feature: Feature name to analyze
            z_threshold: Z-score threshold (typically 2.5-3.0)

        Returns:
            List of anomaly detection results
        """
        logger.info(f"Detecting univariate anomalies in feature '{feature}'")

        df = pd.DataFrame(data)

        if feature not in df.columns:
            raise ValueError(f"Feature '{feature}' not found in data")

        values = df[feature].dropna()

        # Calculate z-scores
        z_scores = np.abs(stats.zscore(values))

        results = []
        for i, (value, z_score) in enumerate(zip(values, z_scores)):
            is_anomaly = z_score > z_threshold

            result = {
                'index': int(values.index[i]),
                'value': float(value),
                'z_score': float(z_score),
                'is_anomaly': bool(is_anomaly),
                'data_point': data[values.index[i]]
            }

            if is_anomaly:
                mean = values.mean()
                std = values.std()
                result['deviation'] = {
                    'from_mean': float(value - mean),
                    'num_std_devs': float(z_score),
                    'percentile': float(stats.percentileofscore(values, value))
                }

            results.append(result)

        n_anomalies = sum(1 for r in results if r['is_anomaly'])
        logger.info(f"Detected {n_anomalies} anomalies in '{feature}'")

        return results

    def detect_time_series_anomalies(
        self,
        data: List[Dict[str, Any]],
        date_column: str,
        value_column: str,
        window_size: int = 12,
        n_std: float = 2.5
    ) -> List[Dict[str, Any]]:
        """
        Detect anomalies in time series data using rolling statistics.

        Args:
            data: Time series data
            date_column: Name of date column
            value_column: Name of value column
            window_size: Rolling window size
            n_std: Number of standard deviations for threshold

        Returns:
            List of anomaly detection results
        """
        logger.info(f"Detecting time series anomalies in '{value_column}'")

        df = pd.DataFrame(data)
        df[date_column] = pd.to_datetime(df[date_column])
        df = df.sort_values(date_column)

        values = df[value_column]

        # Calculate rolling statistics
        rolling_mean = values.rolling(window=window_size, center=True).mean()
        rolling_std = values.rolling(window=window_size, center=True).std()

        # Calculate upper and lower bounds
        upper_bound = rolling_mean + (n_std * rolling_std)
        lower_bound = rolling_mean - (n_std * rolling_std)

        results = []
        for i, (idx, row) in enumerate(df.iterrows()):
            value = row[value_column]
            date = row[date_column]

            # Check if value is outside bounds
            if pd.notna(upper_bound.iloc[i]) and pd.notna(lower_bound.iloc[i]):
                is_anomaly = value > upper_bound.iloc[i] or value < lower_bound.iloc[i]

                result = {
                    'index': i,
                    'date': date.strftime('%Y-%m-%d'),
                    'value': float(value),
                    'rolling_mean': float(rolling_mean.iloc[i]),
                    'rolling_std': float(rolling_std.iloc[i]),
                    'upper_bound': float(upper_bound.iloc[i]),
                    'lower_bound': float(lower_bound.iloc[i]),
                    'is_anomaly': bool(is_anomaly),
                    'data_point': data[i]
                }

                if is_anomaly:
                    deviation = (
                        (value - rolling_mean.iloc[i]) / rolling_std.iloc[i]
                        if rolling_std.iloc[i] > 0 else 0
                    )
                    result['deviation_from_trend'] = float(deviation)
                    result['anomaly_type'] = 'spike' if value > upper_bound.iloc[i] else 'drop'

                results.append(result)

        n_anomalies = sum(1 for r in results if r['is_anomaly'])
        logger.info(f"Detected {n_anomalies} time series anomalies")

        return results

    def detect_financial_anomalies(
        self,
        transactions: List[Dict[str, Any]],
        property_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Comprehensive financial anomaly detection for real estate.

        Detects:
        - Unusual transaction amounts
        - Suspicious payment patterns
        - Abnormal expense ratios
        - Cash flow irregularities

        Args:
            transactions: List of financial transactions
            property_id: Optional property ID to filter by

        Returns:
            Dictionary with anomaly detection results
        """
        logger.info(f"Detecting financial anomalies in {len(transactions)} transactions")

        df = pd.DataFrame(transactions)

        # Filter by property if specified
        if property_id and 'property_id' in df.columns:
            df = df[df['property_id'] == property_id]

        anomalies = {
            'summary': {
                'total_transactions': len(df),
                'total_anomalies': 0
            },
            'amount_anomalies': [],
            'frequency_anomalies': [],
            'pattern_anomalies': []
        }

        # 1. Detect amount anomalies
        if 'amount' in df.columns:
            amount_results = self.detect_univariate_anomalies(
                transactions,
                'amount',
                z_threshold=3.0
            )
            anomalies['amount_anomalies'] = [
                r for r in amount_results if r['is_anomaly']
            ]

        # 2. Detect frequency anomalies (transactions per period)
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            df['month'] = df['date'].dt.to_period('M')

            monthly_counts = df.groupby('month').size().reset_index(name='count')
            monthly_data = [
                {'month': str(row['month']), 'count': row['count']}
                for _, row in monthly_counts.iterrows()
            ]

            if len(monthly_data) > 3:
                freq_results = self.detect_univariate_anomalies(
                    monthly_data,
                    'count',
                    z_threshold=2.5
                )
                anomalies['frequency_anomalies'] = [
                    r for r in freq_results if r['is_anomaly']
                ]

        # 3. Detect pattern anomalies
        if 'category' in df.columns and 'amount' in df.columns:
            # Check for unusual category distributions
            category_stats = df.groupby('category')['amount'].agg(['mean', 'std', 'count'])

            for category in category_stats.index:
                category_df = df[df['category'] == category]
                if len(category_df) > 5:
                    cat_mean = category_stats.loc[category, 'mean']
                    cat_std = category_stats.loc[category, 'std']

                    # Find transactions significantly different from category norm
                    for _, trans in category_df.iterrows():
                        if cat_std > 0:
                            z_score = abs((trans['amount'] - cat_mean) / cat_std)
                            if z_score > 3.0:
                                anomalies['pattern_anomalies'].append({
                                    'transaction': trans.to_dict(),
                                    'category': category,
                                    'expected_amount': float(cat_mean),
                                    'actual_amount': float(trans['amount']),
                                    'z_score': float(z_score)
                                })

        # Update summary
        anomalies['summary']['total_anomalies'] = (
            len(anomalies['amount_anomalies']) +
            len(anomalies['frequency_anomalies']) +
            len(anomalies['pattern_anomalies'])
        )

        return anomalies

    def _identify_anomalous_features(
        self,
        data_point: pd.Series,
        dataset: pd.DataFrame,
        features: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Identify which features contribute to anomaly.

        Args:
            data_point: The anomalous data point
            dataset: Full dataset
            features: Feature names

        Returns:
            List of anomalous features with details
        """
        anomalous_features = []

        for feature in features:
            value = data_point[feature]
            mean = dataset[feature].mean()
            std = dataset[feature].std()

            if std > 0:
                z_score = abs((value - mean) / std)
                if z_score > 2.0:
                    anomalous_features.append({
                        'feature': feature,
                        'value': float(value),
                        'mean': float(mean),
                        'z_score': float(z_score),
                        'percentile': float(stats.percentileofscore(dataset[feature], value))
                    })

        # Sort by z-score
        anomalous_features.sort(key=lambda x: x['z_score'], reverse=True)

        return anomalous_features


def generate_sample_transaction_data(
    n_transactions: int = 500,
    with_anomalies: bool = True
) -> List[Dict[str, Any]]:
    """
    Generate synthetic transaction data for demonstration.

    Args:
        n_transactions: Number of transactions to generate
        with_anomalies: Whether to inject anomalies

    Returns:
        List of transaction dictionaries
    """
    np.random.seed(42)

    categories = ['rent', 'maintenance', 'utilities', 'insurance', 'taxes', 'income']
    normal_amounts = {
        'rent': (2000, 500),
        'maintenance': (500, 200),
        'utilities': (300, 100),
        'insurance': (200, 50),
        'taxes': (800, 200),
        'income': (3000, 800)
    }

    transactions = []
    start_date = pd.Timestamp('2023-01-01')

    for i in range(n_transactions):
        category = np.random.choice(categories)
        mean, std = normal_amounts[category]

        # Normal transaction
        amount = np.random.normal(mean, std)

        # Inject anomalies
        if with_anomalies and np.random.random() < 0.05:
            # 5% anomalies
            amount *= np.random.choice([0.2, 5.0])  # Very low or very high

        date = start_date + pd.Timedelta(days=np.random.randint(0, 730))

        transactions.append({
            'id': f'TXN_{i:05d}',
            'date': date.strftime('%Y-%m-%d'),
            'category': category,
            'amount': max(abs(amount), 10),  # Ensure positive
            'property_id': f'PROP_{np.random.randint(1, 10):03d}',
            'description': f'{category.title()} payment'
        })

    return transactions
