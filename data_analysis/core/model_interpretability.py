"""
Model Interpretability Module
==============================

Tools for understanding and explaining model predictions.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Union
import warnings

warnings.filterwarnings('ignore')


class ModelInterpreter:
    """
    Model interpretation using permutation importance and partial dependence.
    """

    def __init__(self, model, X: pd.DataFrame, y: pd.Series):
        """
        Initialize interpreter.

        Args:
            model: Fitted model with predict method
            X: Feature DataFrame
            y: Target series
        """
        self.model = model
        self.X = X
        self.y = y
        self.feature_names = X.columns.tolist()
        self.baseline_score = None

    def permutation_importance(
        self,
        n_repeats: int = 10,
        scoring: str = 'mse'
    ) -> pd.DataFrame:
        """
        Calculate permutation feature importance.

        More reliable than built-in importance for understanding
        actual contribution to predictions.

        Args:
            n_repeats: Number of permutation repeats
            scoring: Scoring function ('mse', 'mae', 'r2')

        Returns:
            DataFrame with importance scores
        """
        X_array = self.X.values
        y_array = self.y.values

        # Baseline score
        baseline_pred = self.model.predict(X_array)
        self.baseline_score = self._calculate_score(y_array, baseline_pred, scoring)

        importances = []

        for col_idx, col_name in enumerate(self.feature_names):
            scores = []

            for _ in range(n_repeats):
                X_permuted = X_array.copy()
                np.random.shuffle(X_permuted[:, col_idx])

                permuted_pred = self.model.predict(X_permuted)
                permuted_score = self._calculate_score(y_array, permuted_pred, scoring)

                # Importance = decrease in performance
                importance = permuted_score - self.baseline_score
                scores.append(importance)

            importances.append({
                'feature': col_name,
                'importance_mean': np.mean(scores),
                'importance_std': np.std(scores)
            })

        df = pd.DataFrame(importances)
        df = df.sort_values('importance_mean', ascending=False)
        df['importance_mean'] = df['importance_mean'].round(6)
        df['importance_std'] = df['importance_std'].round(6)

        return df

    def _calculate_score(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        scoring: str
    ) -> float:
        """Calculate scoring metric."""
        if scoring == 'mse':
            return np.mean((y_true - y_pred) ** 2)
        elif scoring == 'mae':
            return np.mean(np.abs(y_true - y_pred))
        elif scoring == 'r2':
            ss_res = np.sum((y_true - y_pred) ** 2)
            ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
            return 1 - (ss_res / ss_tot)
        else:
            return np.mean((y_true - y_pred) ** 2)

    def partial_dependence(
        self,
        feature: str,
        grid_resolution: int = 50
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate partial dependence for a feature.

        Shows marginal effect of feature on prediction.

        Args:
            feature: Feature name
            grid_resolution: Number of points to evaluate

        Returns:
            Tuple of (grid values, partial dependence values)
        """
        col_idx = self.feature_names.index(feature)
        X_array = self.X.values

        # Create grid
        feature_values = X_array[:, col_idx]
        grid = np.linspace(
            np.percentile(feature_values, 5),
            np.percentile(feature_values, 95),
            grid_resolution
        )

        # Calculate PD
        pd_values = []
        for value in grid:
            X_modified = X_array.copy()
            X_modified[:, col_idx] = value
            predictions = self.model.predict(X_modified)
            pd_values.append(np.mean(predictions))

        return grid, np.array(pd_values)

    def interaction_strength(
        self,
        feature1: str,
        feature2: str,
        grid_resolution: int = 20
    ) -> Dict:
        """
        Calculate interaction strength between two features.

        Args:
            feature1: First feature
            feature2: Second feature
            grid_resolution: Grid resolution

        Returns:
            Dictionary with interaction data
        """
        idx1 = self.feature_names.index(feature1)
        idx2 = self.feature_names.index(feature2)
        X_array = self.X.values

        # Create grids
        grid1 = np.linspace(
            np.percentile(X_array[:, idx1], 5),
            np.percentile(X_array[:, idx1], 95),
            grid_resolution
        )
        grid2 = np.linspace(
            np.percentile(X_array[:, idx2], 5),
            np.percentile(X_array[:, idx2], 95),
            grid_resolution
        )

        # Calculate 2D PD
        pd_2d = np.zeros((grid_resolution, grid_resolution))

        for i, val1 in enumerate(grid1):
            for j, val2 in enumerate(grid2):
                X_modified = X_array.copy()
                X_modified[:, idx1] = val1
                X_modified[:, idx2] = val2
                predictions = self.model.predict(X_modified)
                pd_2d[i, j] = np.mean(predictions)

        # Calculate individual PDs
        pd1 = np.mean(pd_2d, axis=1)
        pd2 = np.mean(pd_2d, axis=0)

        # Calculate interaction
        interaction = pd_2d - np.outer(pd1, np.ones(grid_resolution)) - \
                     np.outer(np.ones(grid_resolution), pd2) + np.mean(pd_2d)

        interaction_strength = np.std(interaction)

        return {
            'feature1': feature1,
            'feature2': feature2,
            'interaction_strength': round(interaction_strength, 6),
            'grid1': grid1,
            'grid2': grid2,
            'pd_2d': pd_2d
        }

    def feature_contributions(
        self,
        instance_idx: int
    ) -> pd.DataFrame:
        """
        Calculate feature contributions for a single prediction.

        Simple approximation of SHAP values.

        Args:
            instance_idx: Index of instance to explain

        Returns:
            DataFrame with feature contributions
        """
        X_array = self.X.values
        instance = X_array[instance_idx]
        baseline = X_array.mean(axis=0)

        # Prediction for instance
        instance_pred = self.model.predict(instance.reshape(1, -1))[0]

        # Baseline prediction
        baseline_pred = self.model.predict(baseline.reshape(1, -1))[0]

        # Calculate contributions
        contributions = []
        remaining = instance_pred - baseline_pred

        for col_idx, col_name in enumerate(self.feature_names):
            # Create instance with one feature at baseline
            modified = instance.copy()
            modified[col_idx] = baseline[col_idx]
            modified_pred = self.model.predict(modified.reshape(1, -1))[0]

            # Contribution = difference
            contribution = instance_pred - modified_pred

            contributions.append({
                'feature': col_name,
                'value': round(instance[col_idx], 4),
                'baseline': round(baseline[col_idx], 4),
                'contribution': round(contribution, 6)
            })

        df = pd.DataFrame(contributions)
        df = df.sort_values('contribution', key=abs, ascending=False)

        return df

    def get_top_features(
        self,
        n: int = 10,
        method: str = 'permutation'
    ) -> List[str]:
        """
        Get top N important features.

        Args:
            n: Number of features
            method: 'permutation' or 'builtin'

        Returns:
            List of feature names
        """
        if method == 'permutation':
            importance_df = self.permutation_importance(n_repeats=5)
            return importance_df['feature'].head(n).tolist()
        elif method == 'builtin' and hasattr(self.model, 'feature_importances_'):
            importance = self.model.feature_importances_
            indices = np.argsort(importance)[::-1][:n]
            return [self.feature_names[i] for i in indices]
        else:
            return self.feature_names[:n]


class PredictionExplainer:
    """
    Explain individual predictions.
    """

    def __init__(self, model, feature_names: List[str]):
        self.model = model
        self.feature_names = feature_names

    def explain_prediction(
        self,
        instance: np.ndarray,
        reference: np.ndarray = None,
        top_n: int = 5
    ) -> Dict:
        """
        Explain a single prediction.

        Args:
            instance: Feature values for instance
            reference: Reference point (default: zeros)
            top_n: Number of top features to show

        Returns:
            Explanation dictionary
        """
        if reference is None:
            reference = np.zeros_like(instance)

        prediction = self.model.predict(instance.reshape(1, -1))[0]
        ref_prediction = self.model.predict(reference.reshape(1, -1))[0]

        # Calculate contributions using forward differences
        contributions = []
        current = reference.copy()

        for i, name in enumerate(self.feature_names):
            current_pred = self.model.predict(current.reshape(1, -1))[0]
            current[i] = instance[i]
            new_pred = self.model.predict(current.reshape(1, -1))[0]

            contributions.append({
                'feature': name,
                'value': instance[i],
                'contribution': new_pred - current_pred
            })

        # Sort by absolute contribution
        contributions.sort(key=lambda x: abs(x['contribution']), reverse=True)

        return {
            'prediction': round(prediction, 4),
            'reference_prediction': round(ref_prediction, 4),
            'top_contributors': contributions[:top_n],
            'total_contribution': round(prediction - ref_prediction, 4)
        }

    def counterfactual(
        self,
        instance: np.ndarray,
        target_value: float,
        feature_ranges: Dict[str, Tuple[float, float]] = None,
        n_iterations: int = 100
    ) -> Dict:
        """
        Find counterfactual explanation.

        What minimal changes would change the prediction?

        Args:
            instance: Current instance
            target_value: Desired prediction
            feature_ranges: Allowed ranges for features
            n_iterations: Search iterations

        Returns:
            Counterfactual instance and changes
        """
        current = instance.copy()
        current_pred = self.model.predict(current.reshape(1, -1))[0]

        best_instance = current.copy()
        best_distance = np.inf

        for _ in range(n_iterations):
            # Random perturbation
            candidate = current.copy()
            for i in range(len(candidate)):
                if feature_ranges and self.feature_names[i] in feature_ranges:
                    low, high = feature_ranges[self.feature_names[i]]
                    candidate[i] = np.random.uniform(low, high)
                else:
                    candidate[i] += np.random.normal(0, np.abs(current[i]) * 0.1 + 0.1)

            # Check prediction
            pred = self.model.predict(candidate.reshape(1, -1))[0]

            if abs(pred - target_value) < abs(best_distance):
                best_distance = pred - target_value
                best_instance = candidate.copy()

            if abs(pred - target_value) < 0.01 * abs(target_value):
                break

        # Calculate changes
        changes = {}
        for i, name in enumerate(self.feature_names):
            if abs(best_instance[i] - instance[i]) > 1e-6:
                changes[name] = {
                    'from': round(instance[i], 4),
                    'to': round(best_instance[i], 4),
                    'change': round(best_instance[i] - instance[i], 4)
                }

        return {
            'original_prediction': round(current_pred, 4),
            'target': target_value,
            'achieved_prediction': round(
                self.model.predict(best_instance.reshape(1, -1))[0], 4
            ),
            'changes': changes,
            'n_features_changed': len(changes)
        }
