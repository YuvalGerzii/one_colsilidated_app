"""
Advanced Visualization Module
==============================

Professional data visualization for time series, forecasts,
trends, and model performance.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Union
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')


class AdvancedCharts:
    """
    Advanced charting and visualization for data analysis.
    """

    def __init__(self, style: str = 'seaborn'):
        """
        Initialize with plotting style.

        Args:
            style: Matplotlib style
        """
        self.style = style
        self.figures = {}
        self.color_palette = [
            '#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#3B1F2B',
            '#95C623', '#8C9A9E', '#6E44FF', '#00B4D8', '#FF6B6B'
        ]

    def _setup_matplotlib(self):
        """Setup matplotlib with style."""
        try:
            import matplotlib.pyplot as plt
            import matplotlib.dates as mdates
            plt.style.use(self.style)
            return plt, mdates
        except ImportError:
            raise ImportError("matplotlib not installed")

    def plot_time_series(
        self,
        data: Union[pd.Series, pd.DataFrame],
        title: str = 'Time Series',
        xlabel: str = 'Date',
        ylabel: str = 'Value',
        figsize: Tuple[int, int] = (14, 6),
        show_trend: bool = False,
        save_path: str = None
    ):
        """
        Plot time series data.

        Args:
            data: Time series data
            title: Chart title
            xlabel: X-axis label
            ylabel: Y-axis label
            figsize: Figure size
            show_trend: Show trend line
            save_path: Path to save figure

        Returns:
            Matplotlib figure
        """
        plt, mdates = self._setup_matplotlib()

        fig, ax = plt.subplots(figsize=figsize)

        if isinstance(data, pd.DataFrame):
            for i, col in enumerate(data.columns):
                ax.plot(data.index, data[col], label=col,
                       color=self.color_palette[i % len(self.color_palette)],
                       linewidth=1.5)
            ax.legend(loc='upper left')
        else:
            ax.plot(data.index, data.values, color=self.color_palette[0],
                   linewidth=1.5, label=data.name or 'Value')

            if show_trend:
                # Add trend line
                x = np.arange(len(data))
                z = np.polyfit(x, data.values, 1)
                p = np.poly1d(z)
                ax.plot(data.index, p(x), '--', color=self.color_palette[1],
                       alpha=0.8, label='Trend')
                ax.legend()

        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)

        # Format dates
        if isinstance(data.index, pd.DatetimeIndex):
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            plt.xticks(rotation=45)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        self.figures['time_series'] = fig
        return fig

    def plot_forecast(
        self,
        actual: pd.Series,
        forecast: np.ndarray,
        forecast_index: pd.DatetimeIndex,
        lower: np.ndarray = None,
        upper: np.ndarray = None,
        title: str = 'Forecast',
        figsize: Tuple[int, int] = (14, 6),
        save_path: str = None
    ):
        """
        Plot actual vs forecast with confidence intervals.

        Args:
            actual: Historical actual values
            forecast: Forecast values
            forecast_index: Dates for forecast
            lower: Lower confidence bound
            upper: Upper confidence bound
            title: Chart title
            figsize: Figure size
            save_path: Save path

        Returns:
            Matplotlib figure
        """
        plt, _ = self._setup_matplotlib()

        fig, ax = plt.subplots(figsize=figsize)

        # Plot actual
        ax.plot(actual.index, actual.values, color=self.color_palette[0],
               linewidth=1.5, label='Actual')

        # Plot forecast
        ax.plot(forecast_index, forecast, color=self.color_palette[1],
               linewidth=2, linestyle='--', label='Forecast')

        # Confidence interval
        if lower is not None and upper is not None:
            ax.fill_between(forecast_index, lower, upper,
                          color=self.color_palette[1], alpha=0.2,
                          label='Confidence Interval')

        ax.axvline(x=actual.index[-1], color='gray', linestyle=':', alpha=0.7)
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Value', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend(loc='upper left')
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        self.figures['forecast'] = fig
        return fig

    def plot_decomposition(
        self,
        decomposition: Dict,
        title: str = 'Time Series Decomposition',
        figsize: Tuple[int, int] = (14, 10),
        save_path: str = None
    ):
        """
        Plot time series decomposition.

        Args:
            decomposition: Dict with trend, seasonal, residual components
            title: Chart title
            figsize: Figure size
            save_path: Save path

        Returns:
            Matplotlib figure
        """
        plt, _ = self._setup_matplotlib()

        fig, axes = plt.subplots(4, 1, figsize=figsize)

        components = ['observed', 'trend', 'seasonal', 'residual']
        titles = ['Observed', 'Trend', 'Seasonal', 'Residual']

        for ax, comp, comp_title in zip(axes, components, titles):
            if comp in decomposition:
                data = decomposition[comp]
                ax.plot(data.index, data.values, color=self.color_palette[0])
                ax.set_ylabel(comp_title, fontsize=10)
                ax.grid(True, alpha=0.3)

        axes[0].set_title(title, fontsize=14, fontweight='bold')
        axes[-1].set_xlabel('Date', fontsize=12)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        self.figures['decomposition'] = fig
        return fig

    def plot_anomalies(
        self,
        series: pd.Series,
        anomaly_indices: List[int],
        title: str = 'Anomaly Detection',
        figsize: Tuple[int, int] = (14, 6),
        save_path: str = None
    ):
        """
        Plot time series with anomalies highlighted.

        Args:
            series: Time series data
            anomaly_indices: Indices of anomalies
            title: Chart title
            figsize: Figure size
            save_path: Save path

        Returns:
            Matplotlib figure
        """
        plt, _ = self._setup_matplotlib()

        fig, ax = plt.subplots(figsize=figsize)

        # Plot series
        ax.plot(series.index, series.values, color=self.color_palette[0],
               linewidth=1, label='Data')

        # Highlight anomalies
        if anomaly_indices:
            anomaly_dates = series.index[anomaly_indices]
            anomaly_values = series.iloc[anomaly_indices]
            ax.scatter(anomaly_dates, anomaly_values, color=self.color_palette[2],
                      s=50, zorder=5, label=f'Anomalies ({len(anomaly_indices)})')

        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Value', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        self.figures['anomalies'] = fig
        return fig

    def plot_feature_importance(
        self,
        importance: Dict[str, float],
        title: str = 'Feature Importance',
        top_n: int = 20,
        figsize: Tuple[int, int] = (10, 8),
        save_path: str = None
    ):
        """
        Plot feature importance.

        Args:
            importance: Dictionary of feature importances
            title: Chart title
            top_n: Number of top features
            figsize: Figure size
            save_path: Save path

        Returns:
            Matplotlib figure
        """
        plt, _ = self._setup_matplotlib()

        # Sort and select top features
        sorted_imp = sorted(importance.items(), key=lambda x: x[1], reverse=True)[:top_n]
        features, values = zip(*sorted_imp)

        fig, ax = plt.subplots(figsize=figsize)

        y_pos = np.arange(len(features))
        ax.barh(y_pos, values, color=self.color_palette[0], alpha=0.8)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(features)
        ax.invert_yaxis()
        ax.set_xlabel('Importance', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(True, axis='x', alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        self.figures['feature_importance'] = fig
        return fig

    def plot_model_comparison(
        self,
        metrics_df: pd.DataFrame,
        metric: str = 'RMSE',
        title: str = 'Model Comparison',
        figsize: Tuple[int, int] = (10, 6),
        save_path: str = None
    ):
        """
        Plot model comparison.

        Args:
            metrics_df: DataFrame with model metrics
            metric: Metric to compare
            title: Chart title
            figsize: Figure size
            save_path: Save path

        Returns:
            Matplotlib figure
        """
        plt, _ = self._setup_matplotlib()

        fig, ax = plt.subplots(figsize=figsize)

        models = metrics_df['Model'].values
        values = metrics_df[metric].values
        colors = [self.color_palette[i % len(self.color_palette)]
                 for i in range(len(models))]

        bars = ax.bar(models, values, color=colors, alpha=0.8)

        # Add value labels
        for bar, value in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                   f'{value:.4f}', ha='center', va='bottom', fontsize=10)

        ax.set_xlabel('Model', fontsize=12)
        ax.set_ylabel(metric, fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(True, axis='y', alpha=0.3)
        plt.xticks(rotation=45)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        self.figures['model_comparison'] = fig
        return fig

    def plot_correlation_matrix(
        self,
        df: pd.DataFrame,
        title: str = 'Correlation Matrix',
        figsize: Tuple[int, int] = (12, 10),
        save_path: str = None
    ):
        """
        Plot correlation heatmap.

        Args:
            df: DataFrame with features
            title: Chart title
            figsize: Figure size
            save_path: Save path

        Returns:
            Matplotlib figure
        """
        plt, _ = self._setup_matplotlib()
        try:
            import seaborn as sns
        except ImportError:
            raise ImportError("seaborn not installed")

        corr = df.corr()

        fig, ax = plt.subplots(figsize=figsize)
        mask = np.triu(np.ones_like(corr, dtype=bool))

        sns.heatmap(corr, mask=mask, annot=True, fmt='.2f',
                   cmap='RdBu_r', center=0, ax=ax,
                   square=True, linewidths=0.5)

        ax.set_title(title, fontsize=14, fontweight='bold')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        self.figures['correlation'] = fig
        return fig

    def plot_distribution(
        self,
        series: pd.Series,
        title: str = 'Distribution',
        figsize: Tuple[int, int] = (12, 5),
        save_path: str = None
    ):
        """
        Plot distribution with histogram and box plot.

        Args:
            series: Data series
            title: Chart title
            figsize: Figure size
            save_path: Save path

        Returns:
            Matplotlib figure
        """
        plt, _ = self._setup_matplotlib()

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

        # Histogram
        ax1.hist(series.values, bins=50, color=self.color_palette[0],
                alpha=0.7, edgecolor='black')
        ax1.axvline(series.mean(), color=self.color_palette[1],
                   linestyle='--', label=f'Mean: {series.mean():.2f}')
        ax1.axvline(series.median(), color=self.color_palette[2],
                   linestyle=':', label=f'Median: {series.median():.2f}')
        ax1.set_xlabel('Value', fontsize=10)
        ax1.set_ylabel('Frequency', fontsize=10)
        ax1.set_title('Histogram', fontsize=12)
        ax1.legend()

        # Box plot
        ax2.boxplot(series.values, vert=True)
        ax2.set_ylabel('Value', fontsize=10)
        ax2.set_title('Box Plot', fontsize=12)

        fig.suptitle(title, fontsize=14, fontweight='bold')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        self.figures['distribution'] = fig
        return fig

    def plot_actual_vs_predicted(
        self,
        actual: np.ndarray,
        predicted: np.ndarray,
        title: str = 'Actual vs Predicted',
        figsize: Tuple[int, int] = (10, 8),
        save_path: str = None
    ):
        """
        Plot actual vs predicted scatter plot.

        Args:
            actual: Actual values
            predicted: Predicted values
            title: Chart title
            figsize: Figure size
            save_path: Save path

        Returns:
            Matplotlib figure
        """
        plt, _ = self._setup_matplotlib()

        fig, ax = plt.subplots(figsize=figsize)

        ax.scatter(actual, predicted, alpha=0.5, color=self.color_palette[0])

        # Perfect prediction line
        min_val = min(actual.min(), predicted.min())
        max_val = max(actual.max(), predicted.max())
        ax.plot([min_val, max_val], [min_val, max_val], 'r--',
               linewidth=2, label='Perfect Prediction')

        # Calculate R2
        ss_res = np.sum((actual - predicted) ** 2)
        ss_tot = np.sum((actual - np.mean(actual)) ** 2)
        r2 = 1 - (ss_res / ss_tot)

        ax.set_xlabel('Actual', fontsize=12)
        ax.set_ylabel('Predicted', fontsize=12)
        ax.set_title(f'{title}\nR² = {r2:.4f}', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        self.figures['actual_vs_predicted'] = fig
        return fig

    def plot_residuals(
        self,
        residuals: np.ndarray,
        title: str = 'Residual Analysis',
        figsize: Tuple[int, int] = (14, 5),
        save_path: str = None
    ):
        """
        Plot residual analysis.

        Args:
            residuals: Residual values
            title: Chart title
            figsize: Figure size
            save_path: Save path

        Returns:
            Matplotlib figure
        """
        plt, _ = self._setup_matplotlib()

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

        # Residuals over time
        ax1.plot(residuals, color=self.color_palette[0], alpha=0.7)
        ax1.axhline(y=0, color='r', linestyle='--')
        ax1.set_xlabel('Index', fontsize=10)
        ax1.set_ylabel('Residual', fontsize=10)
        ax1.set_title('Residuals Over Time', fontsize=12)
        ax1.grid(True, alpha=0.3)

        # Residual distribution
        ax2.hist(residuals, bins=50, color=self.color_palette[0],
                alpha=0.7, edgecolor='black')
        ax2.axvline(0, color='r', linestyle='--')
        ax2.set_xlabel('Residual', fontsize=10)
        ax2.set_ylabel('Frequency', fontsize=10)
        ax2.set_title('Residual Distribution', fontsize=12)

        fig.suptitle(title, fontsize=14, fontweight='bold')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        self.figures['residuals'] = fig
        return fig

    def plot_training_history(
        self,
        history: Dict,
        title: str = 'Training History',
        figsize: Tuple[int, int] = (12, 5),
        save_path: str = None
    ):
        """
        Plot neural network training history.

        Args:
            history: Training history dictionary
            title: Chart title
            figsize: Figure size
            save_path: Save path

        Returns:
            Matplotlib figure
        """
        plt, _ = self._setup_matplotlib()

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

        # Loss
        ax1.plot(history.get('loss', []), label='Training',
                color=self.color_palette[0])
        if 'val_loss' in history:
            ax1.plot(history['val_loss'], label='Validation',
                    color=self.color_palette[1])
        ax1.set_xlabel('Epoch', fontsize=10)
        ax1.set_ylabel('Loss', fontsize=10)
        ax1.set_title('Loss', fontsize=12)
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # MAE if available
        if 'mae' in history:
            ax2.plot(history['mae'], label='Training',
                    color=self.color_palette[0])
            if 'val_mae' in history:
                ax2.plot(history['val_mae'], label='Validation',
                        color=self.color_palette[1])
            ax2.set_xlabel('Epoch', fontsize=10)
            ax2.set_ylabel('MAE', fontsize=10)
            ax2.set_title('Mean Absolute Error', fontsize=12)
            ax2.legend()
            ax2.grid(True, alpha=0.3)

        fig.suptitle(title, fontsize=14, fontweight='bold')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        self.figures['training_history'] = fig
        return fig

    def create_interactive_plot(
        self,
        data: pd.DataFrame,
        x: str,
        y: str,
        title: str = 'Interactive Plot',
        save_path: str = None
    ):
        """
        Create interactive plot using Plotly.

        Args:
            data: DataFrame with data
            x: X-axis column
            y: Y-axis column
            title: Chart title
            save_path: Save path (HTML)

        Returns:
            Plotly figure
        """
        try:
            import plotly.express as px
        except ImportError:
            raise ImportError("plotly not installed")

        fig = px.line(data, x=x, y=y, title=title)
        fig.update_layout(
            xaxis_title=x,
            yaxis_title=y,
            template='plotly_white'
        )

        if save_path:
            fig.write_html(save_path)

        return fig

    def save_all_figures(
        self,
        output_dir: str,
        format: str = 'png'
    ) -> List[str]:
        """
        Save all generated figures.

        Args:
            output_dir: Output directory
            format: Image format

        Returns:
            List of saved file paths
        """
        plt, _ = self._setup_matplotlib()

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        saved_files = []
        for name, fig in self.figures.items():
            file_path = output_path / f"{name}.{format}"
            fig.savefig(file_path, dpi=300, bbox_inches='tight')
            saved_files.append(str(file_path))

        return saved_files
