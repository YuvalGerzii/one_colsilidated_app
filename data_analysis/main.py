"""
Data Analysis Orchestrator
===========================

Main orchestrator for running comprehensive data analysis pipelines.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Union
from pathlib import Path
from datetime import datetime

from .core.data_preprocessor import DataPreprocessor
from .core.feature_engineering import FeatureEngineer
from .core.utils import DataAnalysisUtils
from .forecasting.time_series_forecaster import TimeSeriesForecaster
from .forecasting.ensemble_forecaster import EnsembleForecaster
from .trends.trend_detector import TrendDetector
from .trends.anomaly_detector import AnomalyDetector
from .predictive.ml_predictor import MLPredictor
from .predictive.neural_predictor import NeuralPredictor
from .visualization.advanced_charts import AdvancedCharts
from .visualization.dashboard_generator import DashboardGenerator
from .projections.scenario_analyzer import ScenarioAnalyzer
from .projections.monte_carlo import MonteCarloSimulator


class DataAnalysisOrchestrator:
    """
    Main orchestrator for comprehensive data analysis workflows.
    """

    def __init__(self, output_dir: str = './analysis_output'):
        """
        Initialize orchestrator.

        Args:
            output_dir: Directory for output files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize components
        self.preprocessor = DataPreprocessor()
        self.feature_engineer = FeatureEngineer()
        self.forecaster = TimeSeriesForecaster()
        self.ensemble = EnsembleForecaster()
        self.trend_detector = TrendDetector()
        self.anomaly_detector = AnomalyDetector()
        self.ml_predictor = MLPredictor()
        self.neural_predictor = NeuralPredictor()
        self.charts = AdvancedCharts()
        self.dashboard = DashboardGenerator()
        self.scenario_analyzer = ScenarioAnalyzer()
        self.monte_carlo = MonteCarloSimulator()

        self.results = {}

    def run_full_analysis(
        self,
        df: pd.DataFrame,
        target_column: str,
        date_column: Optional[str] = None,
        forecast_periods: int = 30,
        generate_report: bool = True
    ) -> Dict:
        """
        Run comprehensive data analysis pipeline.

        Args:
            df: Input DataFrame
            target_column: Target variable column
            date_column: Date column (optional)
            forecast_periods: Number of periods to forecast
            generate_report: Whether to generate HTML report

        Returns:
            Dictionary with all analysis results
        """
        print("=" * 60)
        print("COMPREHENSIVE DATA ANALYSIS PIPELINE")
        print("=" * 60)

        # 1. Data Quality Analysis
        print("\n[1/8] Analyzing data quality...")
        data_quality = self.preprocessor.analyze_data_quality(df)
        self.results['data_quality'] = data_quality
        print(f"  - Total records: {data_quality['total_rows']:,}")
        print(f"  - Total features: {data_quality['total_columns']}")

        # 2. Preprocessing
        print("\n[2/8] Preprocessing data...")
        df_processed = self.preprocessor.full_preprocessing_pipeline(
            df, target_column, date_column
        )
        self.results['preprocessing_log'] = self.preprocessor.get_transformation_log()

        # 3. Trend Analysis
        print("\n[3/8] Detecting trends...")
        if target_column in df.columns:
            series = df[target_column].dropna()
            trend_summary = self.trend_detector.get_trend_summary(series)
            self.results['trend_analysis'] = trend_summary
            print(f"  - Trend: {trend_summary['linear_trend']['trend']}")
            print(f"  - R²: {trend_summary['linear_trend']['r_squared']}")

        # 4. Anomaly Detection
        print("\n[4/8] Detecting anomalies...")
        if target_column in df.columns:
            series = df[target_column].dropna()
            anomaly_summary = self.anomaly_detector.get_anomaly_summary(series)
            self.results['anomaly_detection'] = anomaly_summary
            print(f"  - Total anomalies detected: {anomaly_summary['total_anomalies']}")

        # 5. Time Series Forecasting
        print("\n[5/8] Generating forecasts...")
        if target_column in df.columns:
            series = df[target_column].dropna()

            # ARIMA forecast
            arima_result = self.forecaster.fit_arima(series)
            if 'error' not in arima_result:
                arima_forecast = self.forecaster.forecast('arima', forecast_periods)
                self.ensemble.add_forecast('arima', arima_forecast['forecast'])
                print(f"  - ARIMA: AIC = {arima_result['aic']}")

            # Exponential Smoothing
            try:
                es_result = self.forecaster.fit_exponential_smoothing(series)
                if 'error' not in es_result:
                    es_forecast = self.forecaster.forecast('exp_smoothing', forecast_periods)
                    self.ensemble.add_forecast('exp_smoothing', es_forecast['forecast'])
                    print(f"  - Exp. Smoothing: AIC = {es_result['aic']}")
            except:
                pass

            # Ensemble forecast
            if len(self.ensemble.forecasts) > 0:
                ensemble_forecast = self.ensemble.simple_average()
                self.results['forecast'] = {
                    'ensemble': ensemble_forecast,
                    'weights': self.ensemble.get_weights()
                }
                print(f"  - Ensemble: {len(self.ensemble.forecasts)} models combined")

        # 6. Monte Carlo Simulation
        print("\n[6/8] Running Monte Carlo simulation...")
        if target_column in df.columns:
            series = df[target_column].dropna()
            returns = series.pct_change().dropna()

            if len(returns) > 10:
                drift = returns.mean()
                volatility = returns.std()

                risk_analysis = self.monte_carlo.run_risk_analysis(
                    initial_value=series.iloc[-1],
                    drift=drift,
                    volatility=volatility,
                    periods=forecast_periods
                )
                self.results['risk_analysis'] = risk_analysis
                print(f"  - VaR (95%): {risk_analysis['var']['percentage']:.2f}%")
                print(f"  - CVaR (95%): {risk_analysis['cvar']['percentage']:.2f}%")

        # 7. Scenario Analysis
        print("\n[7/8] Creating scenario projections...")
        if target_column in df.columns:
            series = df[target_column].dropna()
            self.scenario_analyzer.create_baseline_scenario(series)
            self.scenario_analyzer.create_scenario_variants()
            scenario_comparison = self.scenario_analyzer.compare_scenarios(forecast_periods)
            self.results['scenario_analysis'] = scenario_comparison.to_dict()
            print(f"  - Created {len(self.scenario_analyzer.scenarios)} scenarios")

        # 8. Generate Report
        if generate_report:
            print("\n[8/8] Generating report...")
            report_path = self.output_dir / 'analysis_report.html'

            # Add sections to dashboard
            self.dashboard.add_metrics({
                'Records': data_quality['total_rows'],
                'Features': data_quality['total_columns'],
                'Memory (MB)': round(data_quality['memory_usage_mb'], 2)
            }, 'Data Overview')

            if 'trend_analysis' in self.results:
                trend = self.results['trend_analysis']['linear_trend']
                self.dashboard.add_metrics({
                    'Trend': trend['trend'],
                    'Slope': round(trend['slope'], 6),
                    'R²': trend['r_squared']
                }, 'Trend Analysis')

            if 'risk_analysis' in self.results:
                risk = self.results['risk_analysis']
                self.dashboard.add_metrics({
                    'VaR (95%)': f"{risk['var']['percentage']:.2f}%",
                    'CVaR (95%)': f"{risk['cvar']['percentage']:.2f}%",
                    'Prob. of Profit': f"{risk['probabilities']['profit']*100:.1f}%"
                }, 'Risk Metrics')

            self.dashboard.generate_html_dashboard(str(report_path))
            print(f"  - Report saved: {report_path}")

        print("\n" + "=" * 60)
        print("ANALYSIS COMPLETE")
        print("=" * 60)

        return self.results

    def run_forecasting_pipeline(
        self,
        series: pd.Series,
        forecast_periods: int = 30,
        methods: List[str] = None
    ) -> Dict:
        """
        Run focused forecasting pipeline.

        Args:
            series: Time series data
            forecast_periods: Periods to forecast
            methods: Forecasting methods to use

        Returns:
            Forecasting results
        """
        if methods is None:
            methods = ['arima', 'exp_smoothing']

        results = {}

        for method in methods:
            try:
                if method == 'arima':
                    self.forecaster.fit_arima(series)
                    forecast = self.forecaster.forecast('arima', forecast_periods)
                    self.ensemble.add_forecast('arima', forecast['forecast'],
                                             forecast.get('lower'), forecast.get('upper'))
                    results['arima'] = forecast

                elif method == 'exp_smoothing':
                    self.forecaster.fit_exponential_smoothing(series)
                    forecast = self.forecaster.forecast('exp_smoothing', forecast_periods)
                    self.ensemble.add_forecast('exp_smoothing', forecast['forecast'])
                    results['exp_smoothing'] = forecast

            except Exception as e:
                results[method] = {'error': str(e)}

        # Ensemble
        if len(self.ensemble.forecasts) > 0:
            results['ensemble'] = {
                'forecast': self.ensemble.simple_average(),
                'weights': self.ensemble.get_weights()
            }

        return results

    def run_ml_pipeline(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_test: np.ndarray,
        y_test: np.ndarray,
        models: List[str] = None
    ) -> pd.DataFrame:
        """
        Run ML model comparison pipeline.

        Args:
            X_train: Training features
            y_train: Training target
            X_test: Test features
            y_test: Test target
            models: Models to train

        Returns:
            Model comparison DataFrame
        """
        if models is None:
            models = ['xgboost', 'random_forest', 'gradient_boosting']

        for model in models:
            try:
                if model == 'xgboost':
                    self.ml_predictor.train_xgboost(X_train, y_train)
                elif model == 'random_forest':
                    self.ml_predictor.train_random_forest(X_train, y_train)
                elif model == 'gradient_boosting':
                    self.ml_predictor.train_gradient_boosting(X_train, y_train)
            except Exception as e:
                print(f"Error training {model}: {e}")

        return self.ml_predictor.compare_models(X_test, y_test)

    def generate_visualizations(
        self,
        series: pd.Series,
        forecast: np.ndarray = None,
        anomaly_indices: List[int] = None,
        save_dir: str = None
    ) -> List[str]:
        """
        Generate standard visualizations.

        Args:
            series: Time series data
            forecast: Forecast values
            anomaly_indices: Anomaly indices
            save_dir: Directory to save figures

        Returns:
            List of saved file paths
        """
        if save_dir is None:
            save_dir = str(self.output_dir / 'visualizations')

        Path(save_dir).mkdir(parents=True, exist_ok=True)
        saved_files = []

        # Time series plot
        fig = self.charts.plot_time_series(
            series,
            title='Time Series Analysis',
            show_trend=True,
            save_path=f'{save_dir}/time_series.png'
        )
        saved_files.append(f'{save_dir}/time_series.png')

        # Distribution plot
        fig = self.charts.plot_distribution(
            series,
            title='Value Distribution',
            save_path=f'{save_dir}/distribution.png'
        )
        saved_files.append(f'{save_dir}/distribution.png')

        # Anomalies plot
        if anomaly_indices:
            fig = self.charts.plot_anomalies(
                series,
                anomaly_indices,
                save_path=f'{save_dir}/anomalies.png'
            )
            saved_files.append(f'{save_dir}/anomalies.png')

        return saved_files

    def get_results_summary(self) -> Dict:
        """Get summary of all analysis results."""
        return self.results.copy()


def run_quick_analysis(
    data: Union[pd.DataFrame, str],
    target_column: str,
    date_column: str = None
) -> Dict:
    """
    Run quick analysis on data.

    Args:
        data: DataFrame or path to data file
        target_column: Target variable
        date_column: Date column

    Returns:
        Analysis results
    """
    # Load data if path provided
    if isinstance(data, str):
        data = DataAnalysisUtils.load_data(data)

    # Run analysis
    orchestrator = DataAnalysisOrchestrator()
    results = orchestrator.run_full_analysis(
        data,
        target_column,
        date_column,
        forecast_periods=30,
        generate_report=True
    )

    return results


if __name__ == '__main__':
    # Example usage
    print("Data Analysis Package - Example Usage")
    print("-" * 40)

    # Generate sample data
    np.random.seed(42)
    dates = pd.date_range('2020-01-01', periods=500, freq='D')
    values = 100 + np.cumsum(np.random.randn(500) * 2 + 0.05)

    df = pd.DataFrame({
        'date': dates,
        'value': values,
        'volume': np.random.randint(1000, 5000, 500)
    })

    # Run analysis
    results = run_quick_analysis(df, 'value', 'date')

    print("\nAnalysis complete!")
    print(f"Results contain {len(results)} sections")
