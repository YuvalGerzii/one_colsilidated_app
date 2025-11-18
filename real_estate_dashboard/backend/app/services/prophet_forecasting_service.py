"""
Prophet Forecasting Service

Provides time-series forecasting capabilities using Facebook's Prophet library.
Generates forecasts for economic indicators with confidence intervals and trend analysis.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import pandas as pd
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

# Prophet import with fallback
try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False
    logger.warning("Prophet library not installed. Forecasting features disabled.")


class ProphetForecastingService:
    """Service for generating time-series forecasts using Prophet"""

    def __init__(self, db: Session):
        self.db = db
        if not PROPHET_AVAILABLE:
            raise ImportError(
                "Prophet library is not installed. "
                "Install with: pip install prophet"
            )

    def generate_forecast(
        self,
        country: str,
        indicator_name: str,
        forecast_periods: int = 365,
        historical_days: int = 730,
        seasonality_mode: str = 'additive',
        include_holidays: bool = False,
        changepoint_prior_scale: float = 0.05,
        seasonality_prior_scale: float = 10.0,
        confidence_interval: float = 0.95
    ) -> Dict[str, Any]:
        """
        Generate forecast for an economic indicator using Prophet.

        Args:
            country: Country name (e.g., "United States")
            indicator_name: Name of the indicator to forecast
            forecast_periods: Number of days to forecast (default: 365 = 1 year)
            historical_days: Days of historical data to use (default: 730 = 2 years)
            seasonality_mode: 'additive' or 'multiplicative'
            include_holidays: Whether to include US holidays
            changepoint_prior_scale: Flexibility of trend (0.001-0.5, default 0.05)
            seasonality_prior_scale: Flexibility of seasonality (0.01-10, default 10)
            confidence_interval: Confidence interval width (0.8-0.99, default 0.95)

        Returns:
            Dict with forecast data, components, and metrics
        """
        try:
            # Get historical data
            from app.services.economics_db_service import EconomicsDBService
            from app.models.economics import EconomicIndicatorHistory

            service = EconomicsDBService(self.db)

            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=historical_days)

            history = service.get_indicator_history(
                country=country,
                indicator_name=indicator_name,
                start_date=start_date,
                end_date=end_date,
                limit=historical_days
            )

            if not history or len(history) < 10:
                raise ValueError(
                    f"Insufficient historical data for {indicator_name}. "
                    f"Need at least 10 data points, found {len(history) if history else 0}"
                )

            # Prepare data for Prophet
            # Prophet requires columns: 'ds' (date) and 'y' (value)
            df = pd.DataFrame([
                {
                    'ds': h.observation_date,
                    'y': h.value_numeric
                }
                for h in reversed(history)  # Oldest to newest
                if h.value_numeric is not None
            ])

            if df.empty or len(df) < 10:
                raise ValueError(f"No valid numeric data for {indicator_name}")

            # Initialize Prophet model
            model = Prophet(
                seasonality_mode=seasonality_mode,
                changepoint_prior_scale=changepoint_prior_scale,
                seasonality_prior_scale=seasonality_prior_scale,
                interval_width=confidence_interval,
                daily_seasonality=False,
                weekly_seasonality=False,
                yearly_seasonality=True
            )

            # Add US holidays if requested
            if include_holidays:
                model.add_country_holidays(country_name='US')

            # Fit model
            logger.info(f"Fitting Prophet model for {indicator_name} with {len(df)} data points")
            model.fit(df)

            # Create future dataframe
            future = model.make_future_dataframe(periods=forecast_periods, freq='D')

            # Generate forecast
            forecast = model.predict(future)

            # Extract components
            components = self._extract_components(model, forecast)

            # Calculate forecast metrics
            metrics = self._calculate_forecast_metrics(df, forecast, forecast_periods)

            # Prepare response
            result = {
                "indicator_name": indicator_name,
                "country": country,
                "forecast_start": (end_date + timedelta(days=1)).isoformat(),
                "forecast_end": (end_date + timedelta(days=forecast_periods)).isoformat(),
                "forecast_periods": forecast_periods,
                "historical_periods": len(df),
                "historical_start": df['ds'].min().isoformat(),
                "historical_end": df['ds'].max().isoformat(),

                # Forecast data
                "forecast": self._format_forecast(forecast, len(df)),

                # Components (trend, seasonality)
                "components": components,

                # Model metrics
                "metrics": metrics,

                # Model parameters
                "parameters": {
                    "seasonality_mode": seasonality_mode,
                    "changepoint_prior_scale": changepoint_prior_scale,
                    "seasonality_prior_scale": seasonality_prior_scale,
                    "confidence_interval": confidence_interval,
                    "include_holidays": include_holidays
                },

                "timestamp": datetime.now().isoformat()
            }

            return result

        except Exception as e:
            logger.error(f"Error generating forecast for {indicator_name}: {str(e)}")
            raise

    def generate_multiple_forecasts(
        self,
        country: str,
        indicator_names: List[str],
        forecast_periods: int = 365,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate forecasts for multiple indicators.

        Args:
            country: Country name
            indicator_names: List of indicator names
            forecast_periods: Number of days to forecast
            **kwargs: Additional parameters for generate_forecast

        Returns:
            Dict with forecasts for each indicator
        """
        results = []
        errors = []

        for indicator_name in indicator_names:
            try:
                forecast = self.generate_forecast(
                    country=country,
                    indicator_name=indicator_name,
                    forecast_periods=forecast_periods,
                    **kwargs
                )
                results.append(forecast)
            except Exception as e:
                errors.append({
                    "indicator_name": indicator_name,
                    "error": str(e)
                })
                logger.error(f"Failed to forecast {indicator_name}: {str(e)}")

        return {
            "forecasts": results,
            "count": len(results),
            "errors": errors,
            "timestamp": datetime.now().isoformat()
        }

    def _format_forecast(self, forecast: pd.DataFrame, historical_count: int) -> List[Dict]:
        """Format forecast data for API response"""

        # Separate historical fit vs future forecast
        forecast_data = []

        for idx, row in forecast.iterrows():
            is_forecast = idx >= historical_count

            data_point = {
                "date": row['ds'].isoformat(),
                "value": float(row['yhat']),
                "lower_bound": float(row['yhat_lower']),
                "upper_bound": float(row['yhat_upper']),
                "is_forecast": is_forecast
            }

            # Add trend and seasonal components if available
            if 'trend' in row:
                data_point['trend'] = float(row['trend'])
            if 'yearly' in row:
                data_point['yearly_seasonality'] = float(row['yearly'])

            forecast_data.append(data_point)

        return forecast_data

    def _extract_components(self, model: 'Prophet', forecast: pd.DataFrame) -> Dict:
        """Extract trend and seasonality components"""

        components = {}

        # Overall trend
        if 'trend' in forecast.columns:
            trend_data = forecast[['ds', 'trend']].tail(365).to_dict('records')
            components['trend'] = [
                {
                    'date': row['ds'].isoformat(),
                    'value': float(row['trend'])
                }
                for row in trend_data
            ]

            # Trend direction
            recent_trend = forecast['trend'].tail(30).mean()
            previous_trend = forecast['trend'].tail(60).head(30).mean()
            components['trend_direction'] = 'increasing' if recent_trend > previous_trend else 'decreasing'
            components['trend_strength'] = abs((recent_trend - previous_trend) / previous_trend * 100) if previous_trend != 0 else 0

        # Yearly seasonality
        if 'yearly' in forecast.columns:
            seasonal_data = forecast[['ds', 'yearly']].tail(365).to_dict('records')
            components['yearly_seasonality'] = [
                {
                    'date': row['ds'].isoformat(),
                    'value': float(row['yearly'])
                }
                for row in seasonal_data
            ]

            components['seasonality_strength'] = float(forecast['yearly'].std())

        # Changepoints (where trend changes)
        if hasattr(model, 'changepoints'):
            changepoints = model.changepoints
            if len(changepoints) > 0:
                components['changepoints'] = [
                    cp.isoformat() for cp in changepoints[-10:]  # Last 10 changepoints
                ]

        return components

    def _calculate_forecast_metrics(
        self,
        historical_df: pd.DataFrame,
        forecast: pd.DataFrame,
        forecast_periods: int
    ) -> Dict:
        """Calculate metrics for forecast quality and insights"""

        metrics = {}

        # Historical fit metrics (on training data)
        historical_actual = historical_df['y'].values
        historical_predicted = forecast['yhat'].iloc[:len(historical_df)].values

        # Mean Absolute Error (MAE)
        mae = abs(historical_actual - historical_predicted).mean()
        metrics['mae'] = float(mae)

        # Mean Absolute Percentage Error (MAPE)
        mape = (abs((historical_actual - historical_predicted) / historical_actual) * 100).mean()
        metrics['mape'] = float(mape)

        # Root Mean Squared Error (RMSE)
        rmse = ((historical_actual - historical_predicted) ** 2).mean() ** 0.5
        metrics['rmse'] = float(rmse)

        # R-squared (coefficient of determination)
        ss_res = ((historical_actual - historical_predicted) ** 2).sum()
        ss_tot = ((historical_actual - historical_actual.mean()) ** 2).sum()
        r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        metrics['r_squared'] = float(r2)

        # Forecast insights
        forecast_values = forecast['yhat'].iloc[-forecast_periods:].values

        metrics['forecast_mean'] = float(forecast_values.mean())
        metrics['forecast_min'] = float(forecast_values.min())
        metrics['forecast_max'] = float(forecast_values.max())
        metrics['forecast_std'] = float(forecast_values.std())

        # Trend analysis
        last_historical = historical_df['y'].iloc[-1]
        last_forecast = forecast_values[-1]

        metrics['total_change'] = float(last_forecast - last_historical)
        metrics['total_change_percent'] = float((last_forecast - last_historical) / last_historical * 100) if last_historical != 0 else 0

        # Confidence interval width
        ci_width = (forecast['yhat_upper'].iloc[-forecast_periods:] - forecast['yhat_lower'].iloc[-forecast_periods:]).mean()
        metrics['avg_confidence_interval_width'] = float(ci_width)

        # Model quality assessment
        if mape < 10:
            metrics['forecast_quality'] = 'excellent'
        elif mape < 20:
            metrics['forecast_quality'] = 'good'
        elif mape < 30:
            metrics['forecast_quality'] = 'fair'
        else:
            metrics['forecast_quality'] = 'poor'

        return metrics

    def get_forecast_recommendations(
        self,
        forecast_result: Dict
    ) -> Dict[str, Any]:
        """
        Generate actionable recommendations based on forecast.

        Args:
            forecast_result: Output from generate_forecast

        Returns:
            Dict with recommendations and insights
        """
        metrics = forecast_result.get('metrics', {})
        components = forecast_result.get('components', {})

        recommendations = []
        risk_level = 'medium'

        # Trend-based recommendations
        trend_direction = components.get('trend_direction')
        trend_strength = components.get('trend_strength', 0)

        if trend_direction == 'increasing':
            if trend_strength > 5:
                recommendations.append({
                    'type': 'trend',
                    'severity': 'high',
                    'message': f"Strong upward trend detected ({trend_strength:.1f}% increase). Consider timing for investments."
                })
                risk_level = 'low'
            else:
                recommendations.append({
                    'type': 'trend',
                    'severity': 'medium',
                    'message': "Moderate upward trend. Monitor for acceleration."
                })
        elif trend_direction == 'decreasing':
            if trend_strength > 5:
                recommendations.append({
                    'type': 'trend',
                    'severity': 'high',
                    'message': f"Strong downward trend detected ({trend_strength:.1f}% decrease). Exercise caution."
                })
                risk_level = 'high'
            else:
                recommendations.append({
                    'type': 'trend',
                    'severity': 'medium',
                    'message': "Moderate downward trend. Monitor closely."
                })

        # Volatility-based recommendations
        forecast_std = metrics.get('forecast_std', 0)
        forecast_mean = metrics.get('forecast_mean', 1)
        coefficient_of_variation = (forecast_std / forecast_mean * 100) if forecast_mean != 0 else 0

        if coefficient_of_variation > 15:
            recommendations.append({
                'type': 'volatility',
                'severity': 'high',
                'message': f"High volatility expected (CV: {coefficient_of_variation:.1f}%). Increased uncertainty in forecast."
            })
            risk_level = 'high' if risk_level != 'high' else risk_level
        elif coefficient_of_variation > 10:
            recommendations.append({
                'type': 'volatility',
                'severity': 'medium',
                'message': f"Moderate volatility (CV: {coefficient_of_variation:.1f}%). Normal market fluctuations expected."
            })

        # Forecast quality recommendations
        forecast_quality = metrics.get('forecast_quality')
        mape = metrics.get('mape', 0)

        if forecast_quality in ['poor', 'fair']:
            recommendations.append({
                'type': 'data_quality',
                'severity': 'medium',
                'message': f"Forecast quality is {forecast_quality} (MAPE: {mape:.1f}%). Consider using more historical data or checking data quality."
            })

        # Change magnitude recommendations
        total_change_percent = metrics.get('total_change_percent', 0)

        if abs(total_change_percent) > 20:
            direction = 'increase' if total_change_percent > 0 else 'decrease'
            recommendations.append({
                'type': 'magnitude',
                'severity': 'high',
                'message': f"Significant {direction} forecasted ({abs(total_change_percent):.1f}%). Major market shift expected."
            })

        return {
            'recommendations': recommendations,
            'risk_level': risk_level,
            'confidence': forecast_quality,
            'key_insights': {
                'trend_direction': trend_direction,
                'trend_strength_pct': round(trend_strength, 2),
                'expected_change_pct': round(total_change_percent, 2),
                'volatility_cv': round(coefficient_of_variation, 2),
                'forecast_quality': forecast_quality,
                'mape': round(mape, 2)
            }
        }


def check_prophet_availability() -> Dict[str, Any]:
    """Check if Prophet is installed and return version info"""

    if not PROPHET_AVAILABLE:
        return {
            "available": False,
            "message": "Prophet library not installed",
            "install_command": "pip install prophet"
        }

    try:
        import prophet
        return {
            "available": True,
            "version": getattr(prophet, '__version__', 'unknown'),
            "message": "Prophet is ready to use"
        }
    except Exception as e:
        return {
            "available": False,
            "message": f"Error checking Prophet: {str(e)}",
            "install_command": "pip install prophet"
        }
