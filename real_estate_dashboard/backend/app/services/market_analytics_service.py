"""
Market Analytics Service

Provides data enrichment, trend analysis, correlation calculations,
and insight generation for market intelligence data.
"""

import logging
import numpy as np
import pandas as pd
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Any, Tuple
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from scipy import stats

from app.models.market_intelligence import (
    YFinanceMarketData,
    EconomicIndicator,
    MarketIntelligenceSnapshot
)
from app.models.market_intelligence_analytics import (
    MarketTrend,
    MarketCorrelation,
    MarketInsight,
    DataQualityMetric,
    MarketAlert
)

logger = logging.getLogger(__name__)


class MarketAnalyticsService:
    """Service for advanced market intelligence analytics"""

    def __init__(self, db: Session):
        self.db = db

    # ========================================================================
    # DATA VALIDATION & ENRICHMENT
    # ========================================================================

    def validate_and_enrich_data(
        self,
        data: Dict[str, Any],
        data_type: str
    ) -> Tuple[Dict[str, Any], bool, List[str]]:
        """
        Validate and enrich incoming data

        Args:
            data: Raw data dict
            data_type: Type of data (stock, reit, economic, etc.)

        Returns:
            Tuple of (enriched_data, is_valid, issues)
        """
        enriched = data.copy()
        is_valid = True
        issues = []

        try:
            # Basic validation
            if data_type in ['stock', 'reit', 'index']:
                # Validate price data
                price = data.get('current_price') or data.get('value')
                if price is not None:
                    if price < 0:
                        issues.append(f"Negative price: {price}")
                        is_valid = False
                    elif price == 0:
                        issues.append("Zero price (possibly halted)")

                    # Add price range check (52-week high/low)
                    week_52_high = data.get('52_week_high')
                    week_52_low = data.get('52_week_low')

                    if week_52_high and price:
                        if price > week_52_high * 1.1:  # 10% above 52-week high
                            issues.append(f"Price {price} exceeds 52-week high by >10%")
                            enriched['is_at_52_week_high'] = True

                    if week_52_low and price:
                        if price < week_52_low * 0.9:  # 10% below 52-week low
                            issues.append(f"Price {price} below 52-week low by >10%")
                            enriched['is_at_52_week_low'] = True

                # Validate volume
                volume = data.get('volume')
                if volume and volume < 0:
                    issues.append(f"Negative volume: {volume}")
                    is_valid = False

                # Calculate and add derived metrics
                if 'price_change_pct' in data:
                    change_pct = data['price_change_pct']

                    # Flag large moves (>5% daily)
                    if abs(change_pct) > 5:
                        enriched['is_large_move'] = True
                        enriched['move_magnitude'] = abs(change_pct)

                    # Classify movement
                    if change_pct > 2:
                        enriched['movement_class'] = 'strong_up'
                    elif change_pct > 0.5:
                        enriched['movement_class'] = 'up'
                    elif change_pct < -2:
                        enriched['movement_class'] = 'strong_down'
                    elif change_pct < -0.5:
                        enriched['movement_class'] = 'down'
                    else:
                        enriched['movement_class'] = 'flat'

            elif data_type == 'economic':
                # Validate economic indicator values
                value = data.get('value')
                if value is not None:
                    # Check for unrealistic values based on indicator type
                    indicator_name = data.get('indicator_name', '').lower()

                    if 'rate' in indicator_name or 'unemployment' in indicator_name:
                        if value < 0 or value > 100:
                            issues.append(f"Rate value out of range [0-100]: {value}")
                            is_valid = False

                    if 'growth' in indicator_name:
                        if abs(value) > 50:  # Extreme growth rates
                            issues.append(f"Extreme growth rate: {value}%")

            # Add data quality metadata
            enriched['validation_timestamp'] = datetime.now().isoformat()
            enriched['validation_passed'] = is_valid
            enriched['validation_issues'] = issues if issues else None
            enriched['data_completeness'] = self._calculate_completeness(data)

        except Exception as e:
            logger.error(f"Error validating data: {str(e)}")
            issues.append(f"Validation error: {str(e)}")
            is_valid = False

        return enriched, is_valid, issues

    def _calculate_completeness(self, data: Dict) -> float:
        """Calculate data completeness percentage"""
        total_fields = len(data)
        non_null_fields = sum(1 for v in data.values() if v is not None)
        return (non_null_fields / total_fields * 100) if total_fields > 0 else 0

    # ========================================================================
    # TREND ANALYSIS
    # ========================================================================

    async def calculate_trends(
        self,
        ticker: str,
        indicator_type: str,
        analysis_date: date = None
    ) -> Optional[MarketTrend]:
        """
        Calculate comprehensive trend analysis for an indicator

        Args:
            ticker: Ticker symbol or indicator code
            indicator_type: Type (stock, reit, index, rate, economic)
            analysis_date: Date to analyze (default: today)

        Returns:
            MarketTrend object or None
        """
        if analysis_date is None:
            analysis_date = date.today()

        try:
            # Get historical data (up to 1 year)
            start_date = analysis_date - timedelta(days=365)

            if indicator_type in ['stock', 'reit', 'index']:
                # Query YFinance data
                historical = self.db.query(YFinanceMarketData).filter(
                    YFinanceMarketData.ticker == ticker,
                    YFinanceMarketData.data_timestamp >= start_date,
                    YFinanceMarketData.data_timestamp <= analysis_date
                ).order_by(YFinanceMarketData.data_timestamp).all()

                if not historical:
                    logger.warning(f"No historical data for {ticker}")
                    return None

                # Extract prices
                dates = [h.data_timestamp.date() for h in historical]
                prices = [float(h.current_price) if h.current_price else None for h in historical]

                # Remove None values
                clean_data = [(d, p) for d, p in zip(dates, prices) if p is not None]
                if not clean_data:
                    return None

                dates, prices = zip(*clean_data)
                prices = np.array(prices)

            else:  # economic indicator
                # Query economic data
                historical = self.db.query(EconomicIndicator).filter(
                    EconomicIndicator.indicator_code == ticker,
                    EconomicIndicator.reference_date >= start_date,
                    EconomicIndicator.reference_date <= analysis_date
                ).order_by(EconomicIndicator.reference_date).all()

                if not historical:
                    return None

                dates = [h.reference_date for h in historical]
                prices = np.array([float(h.value) if h.value else None for h in historical])
                prices = prices[~np.isnan(prices)]  # Remove NaN

            if len(prices) < 5:
                logger.warning(f"Insufficient data points for trend analysis: {len(prices)}")
                return None

            # Calculate moving averages
            ma_5 = self._calculate_moving_average(prices, 5)
            ma_10 = self._calculate_moving_average(prices, 10)
            ma_20 = self._calculate_moving_average(prices, 20)
            ma_50 = self._calculate_moving_average(prices, 50)
            ma_200 = self._calculate_moving_average(prices, 200)

            # Calculate percentage changes
            current_price = prices[-1]
            changes = self._calculate_percentage_changes(prices)

            # Calculate volatility
            volatility_daily = float(np.std(np.diff(prices) / prices[:-1]) * 100)

            # Calculate RSI
            rsi = self._calculate_rsi(prices, period=14)

            # Calculate momentum score
            momentum = self._calculate_momentum_score(prices, ma_20, ma_50)

            # Determine trend direction
            trend_direction = self._determine_trend_direction(
                current_price, ma_20, ma_50, ma_200
            )

            # Calculate z-score
            z_score = (current_price - np.mean(prices)) / np.std(prices) if np.std(prices) > 0 else 0

            # Calculate percentile rank
            percentile = stats.percentileofscore(prices, current_price)

            # Anomaly detection
            is_anomaly = abs(z_score) > 2.5  # More than 2.5 std deviations
            anomaly_score = abs(z_score) if is_anomaly else None
            anomaly_reason = f"Value is {abs(z_score):.2f} standard deviations from mean" if is_anomaly else None

            # Create MarketTrend record
            trend = MarketTrend(
                indicator_type=indicator_type,
                indicator_symbol=ticker,
                indicator_name=ticker,  # Could be enriched with full name
                analysis_date=analysis_date,
                period_type='daily',
                current_value=Decimal(str(current_price)),
                previous_value=Decimal(str(prices[-2])) if len(prices) > 1 else None,
                ma_5_day=Decimal(str(ma_5)) if ma_5 else None,
                ma_10_day=Decimal(str(ma_10)) if ma_10 else None,
                ma_20_day=Decimal(str(ma_20)) if ma_20 else None,
                ma_50_day=Decimal(str(ma_50)) if ma_50 else None,
                ma_200_day=Decimal(str(ma_200)) if ma_200 else None,
                change_1_day_pct=Decimal(str(changes.get('1_day', 0))),
                change_5_day_pct=Decimal(str(changes.get('5_day', 0))),
                change_1_month_pct=Decimal(str(changes.get('1_month', 0))),
                change_3_month_pct=Decimal(str(changes.get('3_month', 0))),
                change_6_month_pct=Decimal(str(changes.get('6_month', 0))),
                change_1_year_pct=Decimal(str(changes.get('1_year', 0))),
                change_ytd_pct=Decimal(str(changes.get('ytd', 0))),
                volatility_daily=Decimal(str(volatility_daily)),
                rsi_14=Decimal(str(rsi)) if rsi else None,
                momentum_score=Decimal(str(momentum)),
                trend_direction=trend_direction,
                z_score=Decimal(str(z_score)),
                percentile_rank=Decimal(str(percentile)),
                is_anomaly=is_anomaly,
                anomaly_score=Decimal(str(anomaly_score)) if anomaly_score else None,
                anomaly_reason=anomaly_reason
            )

            self.db.add(trend)
            self.db.commit()

            logger.info(f"✅ Calculated trends for {ticker}: {trend_direction}, RSI={rsi:.1f}")

            return trend

        except Exception as e:
            logger.error(f"Error calculating trends for {ticker}: {str(e)}")
            return None

    def _calculate_moving_average(self, data: np.ndarray, period: int) -> Optional[float]:
        """Calculate simple moving average"""
        if len(data) >= period:
            return float(np.mean(data[-period:]))
        return None

    def _calculate_percentage_changes(self, prices: np.ndarray) -> Dict[str, float]:
        """Calculate percentage changes for various periods"""
        changes = {}
        current = prices[-1]

        try:
            # 1 day
            if len(prices) >= 2:
                changes['1_day'] = ((current - prices[-2]) / prices[-2]) * 100

            # 5 days
            if len(prices) >= 6:
                changes['5_day'] = ((current - prices[-6]) / prices[-6]) * 100

            # 1 month (21 trading days)
            if len(prices) >= 22:
                changes['1_month'] = ((current - prices[-22]) / prices[-22]) * 100

            # 3 months (63 trading days)
            if len(prices) >= 64:
                changes['3_month'] = ((current - prices[-64]) / prices[-64]) * 100

            # 6 months (126 trading days)
            if len(prices) >= 127:
                changes['6_month'] = ((current - prices[-127]) / prices[-127]) * 100

            # 1 year (252 trading days)
            if len(prices) >= 253:
                changes['1_year'] = ((current - prices[-253]) / prices[-253]) * 100

            # YTD (from January 1st to now)
            # Simplified: from first available price this year
            changes['ytd'] = ((current - prices[0]) / prices[0]) * 100

        except Exception as e:
            logger.error(f"Error calculating percentage changes: {str(e)}")

        return changes

    def _calculate_rsi(self, prices: np.ndarray, period: int = 14) -> Optional[float]:
        """Calculate Relative Strength Index"""
        if len(prices) < period + 1:
            return None

        try:
            deltas = np.diff(prices)
            gains = deltas.copy()
            losses = deltas.copy()
            gains[gains < 0] = 0
            losses[losses > 0] = 0
            losses = abs(losses)

            avg_gain = np.mean(gains[-period:])
            avg_loss = np.mean(losses[-period:])

            if avg_loss == 0:
                return 100.0

            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))

            return float(rsi)

        except Exception as e:
            logger.error(f"Error calculating RSI: {str(e)}")
            return None

    def _calculate_momentum_score(
        self,
        price: float,
        ma_20: Optional[float],
        ma_50: Optional[float]
    ) -> float:
        """Calculate momentum score (-100 to +100)"""
        score = 0

        try:
            # Price vs MA20
            if ma_20:
                if price > ma_20:
                    score += 30
                else:
                    score -= 30

            # Price vs MA50
            if ma_50:
                if price > ma_50:
                    score += 30
                else:
                    score -= 30

            # MA20 vs MA50 (golden/death cross)
            if ma_20 and ma_50:
                if ma_20 > ma_50:
                    score += 40
                else:
                    score -= 40

        except Exception as e:
            logger.error(f"Error calculating momentum: {str(e)}")

        return float(score)

    def _determine_trend_direction(
        self,
        price: float,
        ma_20: Optional[float],
        ma_50: Optional[float],
        ma_200: Optional[float]
    ) -> str:
        """Determine overall trend direction"""
        if not ma_20 or not ma_50:
            return "insufficient_data"

        # Strong bullish: price > MA20 > MA50 > MA200
        if price > ma_20 and ma_20 > ma_50:
            if ma_200 and ma_50 > ma_200:
                return "strong_bullish"
            return "bullish"

        # Strong bearish: price < MA20 < MA50 < MA200
        if price < ma_20 and ma_20 < ma_50:
            if ma_200 and ma_50 < ma_200:
                return "strong_bearish"
            return "bearish"

        # Choppy/neutral
        if abs(ma_20 - ma_50) / ma_50 < 0.02:  # Within 2%
            return "choppy"

        return "neutral"

    # ========================================================================
    # CORRELATION ANALYSIS
    # ========================================================================

    async def calculate_correlation(
        self,
        symbol1: str,
        type1: str,
        symbol2: str,
        type2: str,
        period_days: int = 90
    ) -> Optional[MarketCorrelation]:
        """
        Calculate correlation between two market indicators

        Args:
            symbol1: First indicator symbol
            type1: First indicator type
            symbol2: Second indicator symbol
            type2: Second indicator type
            period_days: Number of days to analyze

        Returns:
            MarketCorrelation object or None
        """
        try:
            end_date = date.today()
            start_date = end_date - timedelta(days=period_days)

            # Get data for both indicators
            data1 = self._get_indicator_time_series(symbol1, type1, start_date, end_date)
            data2 = self._get_indicator_time_series(symbol2, type2, start_date, end_date)

            if len(data1) < 10 or len(data2) < 10:
                logger.warning(f"Insufficient data for correlation: {symbol1} vs {symbol2}")
                return None

            # Align data by date
            df1 = pd.DataFrame(data1, columns=['date', 'value1'])
            df2 = pd.DataFrame(data2, columns=['date', 'value2'])
            merged = pd.merge(df1, df2, on='date', how='inner')

            if len(merged) < 10:
                logger.warning(f"Insufficient aligned data: {len(merged)} points")
                return None

            values1 = merged['value1'].values
            values2 = merged['value2'].values

            # Calculate correlations
            pearson_corr, p_value = stats.pearsonr(values1, values2)
            spearman_corr, _ = stats.spearmanr(values1, values2)
            kendall_tau, _ = stats.kendalltau(values1, values2)

            # Determine significance
            is_significant = p_value < 0.05
            confidence = (1 - p_value) * 100

            # Classify correlation strength
            abs_corr = abs(pearson_corr)
            if abs_corr > 0.7:
                strength = "strong"
            elif abs_corr > 0.4:
                strength = "moderate"
            elif abs_corr > 0.2:
                strength = "weak"
            else:
                strength = "none"

            # Direction
            if pearson_corr > 0.2:
                direction = "positive"
            elif pearson_corr < -0.2:
                direction = "negative"
            else:
                direction = "none"

            # Lag analysis (check if one leads the other)
            optimal_lag, lagged_corr = self._find_optimal_lag(values1, values2, max_lag=10)

            # Generate interpretation
            interpretation = self._generate_correlation_interpretation(
                symbol1, symbol2, pearson_corr, strength, direction, optimal_lag
            )

            # Create correlation record
            correlation = MarketCorrelation(
                indicator_1_type=type1,
                indicator_1_symbol=symbol1,
                indicator_1_name=symbol1,
                indicator_2_type=type2,
                indicator_2_symbol=symbol2,
                indicator_2_name=symbol2,
                analysis_start_date=start_date,
                analysis_end_date=end_date,
                period_days=period_days,
                pearson_correlation=Decimal(str(pearson_corr)),
                spearman_correlation=Decimal(str(spearman_corr)),
                kendall_tau=Decimal(str(kendall_tau)),
                p_value=Decimal(str(p_value)),
                is_significant=is_significant,
                confidence_level=Decimal(str(confidence)),
                correlation_strength=strength,
                correlation_direction=direction,
                optimal_lag_days=optimal_lag,
                lagged_correlation=Decimal(str(lagged_corr)),
                interpretation=interpretation,
                trading_signal=self._determine_trading_signal(optimal_lag)
            )

            self.db.add(correlation)
            self.db.commit()

            logger.info(f"✅ Calculated correlation: {symbol1} vs {symbol2} = {pearson_corr:.3f}")

            return correlation

        except Exception as e:
            logger.error(f"Error calculating correlation: {str(e)}")
            return None

    def _get_indicator_time_series(
        self,
        symbol: str,
        indicator_type: str,
        start_date: date,
        end_date: date
    ) -> List[Tuple[date, float]]:
        """Get time series data for an indicator"""
        data = []

        try:
            if indicator_type in ['stock', 'reit', 'index']:
                records = self.db.query(YFinanceMarketData).filter(
                    YFinanceMarketData.ticker == symbol,
                    YFinanceMarketData.data_timestamp >= start_date,
                    YFinanceMarketData.data_timestamp <= end_date
                ).order_by(YFinanceMarketData.data_timestamp).all()

                data = [(r.data_timestamp.date(), float(r.current_price))
                        for r in records if r.current_price]

            else:  # economic
                records = self.db.query(EconomicIndicator).filter(
                    EconomicIndicator.indicator_code == symbol,
                    EconomicIndicator.reference_date >= start_date,
                    EconomicIndicator.reference_date <= end_date
                ).order_by(EconomicIndicator.reference_date).all()

                data = [(r.reference_date, float(r.value))
                        for r in records if r.value]

        except Exception as e:
            logger.error(f"Error getting time series: {str(e)}")

        return data

    def _find_optimal_lag(
        self,
        series1: np.ndarray,
        series2: np.ndarray,
        max_lag: int = 10
    ) -> Tuple[int, float]:
        """Find optimal lag for maximum correlation"""
        best_lag = 0
        best_corr = 0

        try:
            for lag in range(-max_lag, max_lag + 1):
                if lag < 0:
                    # series1 leads series2
                    s1 = series1[:lag]
                    s2 = series2[-lag:]
                elif lag > 0:
                    # series2 leads series1
                    s1 = series1[lag:]
                    s2 = series2[:-lag]
                else:
                    s1 = series1
                    s2 = series2

                if len(s1) >= 10 and len(s2) >= 10:
                    corr, _ = stats.pearsonr(s1, s2)
                    if abs(corr) > abs(best_corr):
                        best_corr = corr
                        best_lag = lag

        except Exception as e:
            logger.error(f"Error finding optimal lag: {str(e)}")

        return best_lag, best_corr

    def _generate_correlation_interpretation(
        self,
        symbol1: str,
        symbol2: str,
        correlation: float,
        strength: str,
        direction: str,
        lag: int
    ) -> str:
        """Generate human-readable interpretation"""
        if strength == "none":
            return f"{symbol1} and {symbol2} show no significant correlation."

        corr_text = f"{strength} {direction} correlation"

        if lag == 0:
            lag_text = "They move together contemporaneously."
        elif lag > 0:
            lag_text = f"{symbol2} leads {symbol1} by approximately {lag} days."
        else:
            lag_text = f"{symbol1} leads {symbol2} by approximately {abs(lag)} days."

        return f"{symbol1} and {symbol2} exhibit a {corr_text} (r={correlation:.3f}). {lag_text}"

    def _determine_trading_signal(self, lag: int) -> str:
        """Determine if indicator is leading, lagging, or coincident"""
        if lag > 2:
            return "leading"
        elif lag < -2:
            return "lagging"
        else:
            return "coincident"

    # ========================================================================
    # DATA QUALITY METRICS
    # ========================================================================

    async def record_data_quality(
        self,
        data_source: str,
        data_category: str,
        expected_points: int,
        received_points: int,
        fetch_duration_ms: int,
        errors: List[str] = None
    ) -> DataQualityMetric:
        """Record data quality metrics for monitoring"""
        try:
            missing = expected_points - received_points
            completeness = (received_points / expected_points * 100) if expected_points > 0 else 0

            # Calculate quality scores
            accuracy_score = 100 - (len(errors or []) * 10)  # -10 per error
            timeliness_score = 100 if fetch_duration_ms < 5000 else max(0, 100 - (fetch_duration_ms - 5000) / 100)
            consistency_score = completeness  # Simple: based on completeness
            overall_score = (accuracy_score + timeliness_score + consistency_score) / 3

            # Error metrics
            error_count = len(errors or [])
            error_rate = (error_count / expected_points * 100) if expected_points > 0 else 0

            quality = DataQualityMetric(
                data_source=data_source,
                data_category=data_category,
                measurement_date=date.today(),
                measurement_time=datetime.now(),
                expected_data_points=expected_points,
                received_data_points=received_points,
                missing_data_points=missing,
                completeness_pct=Decimal(str(completeness)),
                accuracy_score=Decimal(str(accuracy_score)),
                timeliness_score=Decimal(str(timeliness_score)),
                consistency_score=Decimal(str(consistency_score)),
                overall_quality_score=Decimal(str(overall_score)),
                fetch_duration_ms=fetch_duration_ms,
                error_count=error_count,
                error_rate_pct=Decimal(str(error_rate)),
                issues_detected=errors
            )

            self.db.add(quality)
            self.db.commit()

            logger.info(f"✅ Recorded data quality: {data_source}/{data_category} = {overall_score:.1f}/100")

            return quality

        except Exception as e:
            logger.error(f"Error recording data quality: {str(e)}")
            return None

    # ========================================================================
    # INSIGHT GENERATION
    # ========================================================================

    async def generate_insights(self) -> List[MarketInsight]:
        """
        Generate actionable insights from market data

        Returns:
            List of MarketInsight objects
        """
        insights = []

        try:
            # Check for significant REIT movements
            reit_insights = await self._generate_reit_insights()
            insights.extend(reit_insights)

            # Check for interest rate trends
            rate_insights = await self._generate_rate_insights()
            insights.extend(rate_insights)

            # Check for economic anomalies
            economic_insights = await self._generate_economic_insights()
            insights.extend(economic_insights)

            # Check for market correlations
            correlation_insights = await self._generate_correlation_insights()
            insights.extend(correlation_insights)

            logger.info(f"✅ Generated {len(insights)} market insights")

        except Exception as e:
            logger.error(f"Error generating insights: {str(e)}")

        return insights

    async def _generate_reit_insights(self) -> List[MarketInsight]:
        """Generate insights from REIT performance"""
        insights = []

        try:
            # Get recent REIT trends
            recent_trends = self.db.query(MarketTrend).filter(
                MarketTrend.indicator_type == 'reit',
                MarketTrend.analysis_date >= date.today() - timedelta(days=7)
            ).all()

            for trend in recent_trends:
                # Large moves
                if trend.change_1_day_pct and abs(float(trend.change_1_day_pct)) > 3:
                    insight = MarketInsight(
                        insight_type='trend',
                        severity='high' if abs(float(trend.change_1_day_pct)) > 5 else 'medium',
                        category='reits',
                        title=f"{trend.indicator_symbol}: Significant Daily Move",
                        summary=f"{trend.indicator_symbol} moved {trend.change_1_day_pct}% today",
                        detailed_analysis=f"Large move may indicate sector rotation or company-specific news. Monitor for follow-through.",
                        primary_indicator=trend.indicator_symbol,
                        confidence_score=Decimal('85'),
                        insight_date=trend.analysis_date,
                        generation_method='rule_based',
                        is_actionable=True
                    )
                    insights.append(insight)

        except Exception as e:
            logger.error(f"Error generating REIT insights: {str(e)}")

        return insights

    async def _generate_rate_insights(self) -> List[MarketInsight]:
        """Generate insights from interest rate movements"""
        insights = []
        # Implementation similar to REITs
        return insights

    async def _generate_economic_insights(self) -> List[MarketInsight]:
        """Generate insights from economic indicators"""
        insights = []
        # Implementation for economic data analysis
        return insights

    async def _generate_correlation_insights(self) -> List[MarketInsight]:
        """Generate insights from correlations"""
        insights = []
        # Implementation for correlation-based insights
        return insights
