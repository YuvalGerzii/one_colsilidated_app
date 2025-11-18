"""
Automated Comparable Property Selector

Uses ML to automatically select the best comparable properties for valuations:
- Similarity scoring based on property features
- Location-based filtering
- Market timing adjustments
- Quality ranking
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from scipy.spatial.distance import cosine

logger = logging.getLogger(__name__)


class ComparableSelector:
    """
    Automated comparable property selector using ML.

    Uses k-nearest neighbors and custom similarity metrics to find
    the most comparable properties for valuation purposes.
    """

    def __init__(self):
        """Initialize the comparable selector."""
        self.scaler = StandardScaler()
        self.knn_model = None
        self.property_database = None
        self.feature_names = []

    def prepare_features(
        self,
        properties: List[Dict[str, Any]]
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Prepare property features for comparison.

        Args:
            properties: List of property dictionaries

        Returns:
            Tuple of (numeric features DataFrame, metadata DataFrame)
        """
        df = pd.DataFrame(properties)

        # Core comparable features
        numeric_features = []

        # Size features
        if 'square_feet' in df.columns:
            numeric_features.append('square_feet')

        if 'bedrooms' in df.columns:
            numeric_features.append('bedrooms')

        if 'bathrooms' in df.columns:
            numeric_features.append('bathrooms')

        if 'lot_size' in df.columns:
            numeric_features.append('lot_size')

        # Age and condition
        if 'year_built' in df.columns:
            df['age'] = 2025 - df['year_built']
            numeric_features.append('age')

        if 'condition_score' in df.columns:
            numeric_features.append('condition_score')
        elif 'condition' in df.columns:
            condition_map = {
                'poor': 1, 'fair': 2, 'average': 3, 'good': 4, 'excellent': 5
            }
            df['condition_score'] = df['condition'].map(condition_map).fillna(3)
            numeric_features.append('condition_score')

        # Location encoding (simplified - in production use lat/lon)
        if 'zip_code' in df.columns:
            df['zip_code_encoded'] = pd.Categorical(df['zip_code']).codes
            numeric_features.append('zip_code_encoded')

        # Property type
        if 'property_type' in df.columns:
            df['property_type_encoded'] = pd.Categorical(df['property_type']).codes
            numeric_features.append('property_type_encoded')

        # Price (if available)
        if 'sale_price' in df.columns:
            numeric_features.append('sale_price')

        # Sale date recency (if available)
        if 'sale_date' in df.columns:
            df['sale_date'] = pd.to_datetime(df['sale_date'])
            df['days_since_sale'] = (pd.Timestamp.now() - df['sale_date']).dt.days
            numeric_features.append('days_since_sale')

        # Select available features
        available_features = [f for f in numeric_features if f in df.columns]
        self.feature_names = available_features

        # Create metadata DataFrame
        metadata_cols = ['address', 'zip_code', 'sale_price', 'sale_date'] if any(
            col in df.columns for col in ['address', 'zip_code', 'sale_price', 'sale_date']
        ) else []
        metadata_cols = [col for col in metadata_cols if col in df.columns]

        features_df = df[available_features].fillna(df[available_features].median())
        metadata_df = df[metadata_cols] if metadata_cols else pd.DataFrame()

        return features_df, metadata_df

    def build_database(self, properties: List[Dict[str, Any]]):
        """
        Build a database of properties for comparison.

        Args:
            properties: List of property dictionaries to use as comps database
        """
        logger.info(f"Building comparable database with {len(properties)} properties")

        # Prepare features
        features_df, metadata_df = self.prepare_features(properties)

        # Store database
        self.property_database = {
            'features': features_df,
            'metadata': metadata_df,
            'raw_data': properties
        }

        # Fit scaler
        scaled_features = self.scaler.fit_transform(features_df)

        # Build KNN model
        self.knn_model = NearestNeighbors(
            n_neighbors=min(20, len(properties)),
            metric='euclidean',
            algorithm='auto'
        )
        self.knn_model.fit(scaled_features)

        logger.info("Comparable database built successfully")

    def find_comparables(
        self,
        subject_property: Dict[str, Any],
        n_comps: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        weights: Optional[Dict[str, float]] = None
    ) -> List[Dict[str, Any]]:
        """
        Find the most comparable properties to a subject property.

        Args:
            subject_property: Property to find comparables for
            n_comps: Number of comparables to return
            filters: Optional filters (e.g., max distance, property type)
            weights: Optional feature weights for custom scoring

        Returns:
            List of comparable properties with similarity scores
        """
        if self.property_database is None:
            raise ValueError("No property database built. Call build_database() first.")

        logger.info(f"Finding {n_comps} comparables for subject property")

        # Prepare subject property features
        subject_features_df, _ = self.prepare_features([subject_property])

        # Apply filters if provided
        filtered_indices = self._apply_filters(subject_property, filters)

        if len(filtered_indices) == 0:
            logger.warning("No properties match the filters")
            return []

        # Get filtered database
        filtered_features = self.property_database['features'].iloc[filtered_indices]
        filtered_metadata = self.property_database['metadata'].iloc[filtered_indices] if not self.property_database['metadata'].empty else pd.DataFrame()
        filtered_raw = [self.property_database['raw_data'][i] for i in filtered_indices]

        # Scale features
        scaled_subject = self.scaler.transform(subject_features_df)
        scaled_database = self.scaler.transform(filtered_features)

        # Apply custom weights if provided
        if weights:
            weight_vector = np.array([
                weights.get(feature, 1.0) for feature in self.feature_names
            ])
            scaled_subject *= weight_vector
            scaled_database *= weight_vector

        # Calculate distances
        distances = np.linalg.norm(scaled_database - scaled_subject, axis=1)

        # Get top N comparables
        n_comps = min(n_comps, len(distances))
        top_indices = np.argsort(distances)[:n_comps]

        # Build results
        results = []
        for idx in top_indices:
            similarity_score = 1.0 / (1.0 + distances[idx])  # Convert distance to similarity

            comp = {
                'property': filtered_raw[idx],
                'similarity_score': float(similarity_score),
                'distance': float(distances[idx])
            }

            # Add detailed comparison
            comp['feature_comparison'] = self._compare_features(
                subject_features_df.iloc[0],
                filtered_features.iloc[idx]
            )

            # Add adjustments
            comp['suggested_adjustments'] = self._calculate_adjustments(
                subject_property,
                filtered_raw[idx],
                subject_features_df.iloc[0],
                filtered_features.iloc[idx]
            )

            results.append(comp)

        return results

    def _apply_filters(
        self,
        subject_property: Dict[str, Any],
        filters: Optional[Dict[str, Any]]
    ) -> List[int]:
        """
        Apply filters to property database.

        Args:
            subject_property: Subject property
            filters: Filter criteria

        Returns:
            List of indices that pass filters
        """
        if filters is None:
            return list(range(len(self.property_database['raw_data'])))

        indices = []
        db_raw = self.property_database['raw_data']

        for i, prop in enumerate(db_raw):
            # Property type filter
            if 'property_type' in filters:
                if prop.get('property_type') != filters['property_type']:
                    continue

            # Location filter (simplified - in production use geo distance)
            if 'same_zip_code' in filters and filters['same_zip_code']:
                if prop.get('zip_code') != subject_property.get('zip_code'):
                    continue

            # Size filters
            if 'max_size_difference_pct' in filters:
                max_diff = filters['max_size_difference_pct']
                subject_sqft = subject_property.get('square_feet', 0)
                prop_sqft = prop.get('square_feet', 0)

                if subject_sqft > 0:
                    diff_pct = abs(prop_sqft - subject_sqft) / subject_sqft * 100
                    if diff_pct > max_diff:
                        continue

            # Sale date filter
            if 'max_days_since_sale' in filters:
                max_days = filters['max_days_since_sale']
                if 'sale_date' in prop:
                    days_since = (pd.Timestamp.now() - pd.to_datetime(prop['sale_date'])).days
                    if days_since > max_days:
                        continue

            indices.append(i)

        return indices

    def _compare_features(
        self,
        subject_features: pd.Series,
        comp_features: pd.Series
    ) -> Dict[str, Dict[str, float]]:
        """
        Compare features between subject and comparable.

        Args:
            subject_features: Subject property features
            comp_features: Comparable property features

        Returns:
            Dictionary of feature comparisons
        """
        comparison = {}

        for feature in self.feature_names:
            subject_val = subject_features[feature]
            comp_val = comp_features[feature]

            diff = comp_val - subject_val
            pct_diff = (diff / subject_val * 100) if subject_val != 0 else 0

            comparison[feature] = {
                'subject_value': float(subject_val),
                'comp_value': float(comp_val),
                'difference': float(diff),
                'percent_difference': float(pct_diff)
            }

        return comparison

    def _calculate_adjustments(
        self,
        subject_property: Dict[str, Any],
        comp_property: Dict[str, Any],
        subject_features: pd.Series,
        comp_features: pd.Series
    ) -> Dict[str, float]:
        """
        Calculate suggested price adjustments.

        Args:
            subject_property: Subject property
            comp_property: Comparable property
            subject_features: Subject features
            comp_features: Comparable features

        Returns:
            Dictionary of suggested adjustments
        """
        adjustments = {}

        # Size adjustment ($100 per sqft difference)
        if 'square_feet' in subject_features.index:
            sqft_diff = subject_features['square_feet'] - comp_features['square_feet']
            adjustments['size_adjustment'] = float(sqft_diff * 100)

        # Age adjustment (-$1000 per year older)
        if 'age' in subject_features.index:
            age_diff = subject_features['age'] - comp_features['age']
            adjustments['age_adjustment'] = float(-age_diff * 1000)

        # Condition adjustment ($10,000 per point)
        if 'condition_score' in subject_features.index:
            condition_diff = subject_features['condition_score'] - comp_features['condition_score']
            adjustments['condition_adjustment'] = float(condition_diff * 10000)

        # Calculate total adjustment
        adjustments['total_adjustment'] = sum(
            v for k, v in adjustments.items() if k != 'total_adjustment'
        )

        # Adjusted comparable value
        if 'sale_price' in comp_property:
            adjustments['comp_sale_price'] = float(comp_property['sale_price'])
            adjustments['adjusted_comp_value'] = float(
                comp_property['sale_price'] + adjustments['total_adjustment']
            )

        return adjustments

    def calculate_indicated_value(
        self,
        subject_property: Dict[str, Any],
        comparables: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """
        Calculate indicated value from comparables.

        Args:
            subject_property: Subject property
            comparables: List of comparable properties with adjustments

        Returns:
            Dictionary with valuation summary
        """
        adjusted_values = []
        weights = []

        for comp in comparables:
            if 'suggested_adjustments' in comp and 'adjusted_comp_value' in comp['suggested_adjustments']:
                adjusted_value = comp['suggested_adjustments']['adjusted_comp_value']
                weight = comp['similarity_score']

                adjusted_values.append(adjusted_value)
                weights.append(weight)

        if not adjusted_values:
            return {
                'indicated_value': 0,
                'error': 'No comparable values available'
            }

        # Weighted average
        weights_array = np.array(weights)
        weights_array = weights_array / weights_array.sum()  # Normalize

        weighted_value = np.average(adjusted_values, weights=weights_array)

        return {
            'indicated_value': float(weighted_value),
            'min_adjusted_value': float(min(adjusted_values)),
            'max_adjusted_value': float(max(adjusted_values)),
            'mean_adjusted_value': float(np.mean(adjusted_values)),
            'median_adjusted_value': float(np.median(adjusted_values)),
            'std_dev': float(np.std(adjusted_values)),
            'n_comparables': len(adjusted_values)
        }


def generate_sample_property_database(n_properties: int = 500) -> List[Dict[str, Any]]:
    """
    Generate synthetic property database for demonstration.

    Args:
        n_properties: Number of properties to generate

    Returns:
        List of property dictionaries
    """
    np.random.seed(42)

    properties = []
    zip_codes = ['90210', '10001', '60601', '75201', '33139']

    for i in range(n_properties):
        square_feet = np.random.randint(800, 5000)
        bedrooms = np.random.randint(1, 6)
        bathrooms = np.random.randint(1, 5)
        year_built = np.random.randint(1950, 2024)
        lot_size = np.random.randint(2000, 20000)
        zip_code = np.random.choice(zip_codes)

        # Calculate price
        base_price = 150  # per sqft
        location_multiplier = {'90210': 3.0, '10001': 2.5, '60601': 1.5, '75201': 1.2, '33139': 2.0}
        price = square_feet * base_price * location_multiplier[zip_code]

        # Random sale date in last 12 months
        days_ago = np.random.randint(0, 365)
        sale_date = (pd.Timestamp.now() - pd.Timedelta(days=days_ago)).strftime('%Y-%m-%d')

        properties.append({
            'id': f'PROP_{i:04d}',
            'address': f'{np.random.randint(100, 9999)} {np.random.choice(["Main", "Oak", "Elm", "Park"])} St',
            'zip_code': zip_code,
            'square_feet': square_feet,
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'year_built': year_built,
            'lot_size': lot_size,
            'property_type': np.random.choice(['single_family', 'condo', 'townhouse']),
            'condition': np.random.choice(['fair', 'average', 'good', 'excellent']),
            'sale_price': int(price * np.random.uniform(0.9, 1.1)),
            'sale_date': sale_date
        })

    return properties
