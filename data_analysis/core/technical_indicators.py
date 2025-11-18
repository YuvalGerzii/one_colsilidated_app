"""
Technical Indicators and Financial Features
=============================================

Comprehensive technical indicators for financial time series analysis.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional


class TechnicalIndicators:
    """
    Calculate technical indicators for financial analysis.
    """

    @staticmethod
    def sma(series: pd.Series, period: int = 20) -> pd.Series:
        """Simple Moving Average."""
        return series.rolling(window=period).mean()

    @staticmethod
    def ema(series: pd.Series, period: int = 20) -> pd.Series:
        """Exponential Moving Average."""
        return series.ewm(span=period, adjust=False).mean()

    @staticmethod
    def wma(series: pd.Series, period: int = 20) -> pd.Series:
        """Weighted Moving Average."""
        weights = np.arange(1, period + 1)
        return series.rolling(period).apply(
            lambda x: np.sum(weights * x) / weights.sum(), raw=True
        )

    @staticmethod
    def rsi(series: pd.Series, period: int = 14) -> pd.Series:
        """
        Relative Strength Index.

        Measures momentum on a scale of 0-100.
        """
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / (loss + 1e-10)
        return 100 - (100 / (1 + rs))

    @staticmethod
    def macd(
        series: pd.Series,
        fast: int = 12,
        slow: int = 26,
        signal: int = 9
    ) -> pd.DataFrame:
        """
        Moving Average Convergence Divergence.

        Returns MACD line, signal line, and histogram.
        """
        ema_fast = series.ewm(span=fast, adjust=False).mean()
        ema_slow = series.ewm(span=slow, adjust=False).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        histogram = macd_line - signal_line

        return pd.DataFrame({
            'macd': macd_line,
            'signal': signal_line,
            'histogram': histogram
        })

    @staticmethod
    def bollinger_bands(
        series: pd.Series,
        period: int = 20,
        std_dev: float = 2.0
    ) -> pd.DataFrame:
        """
        Bollinger Bands.

        Shows volatility bands around SMA.
        """
        sma = series.rolling(window=period).mean()
        std = series.rolling(window=period).std()
        upper = sma + std_dev * std
        lower = sma - std_dev * std
        bandwidth = (upper - lower) / sma

        return pd.DataFrame({
            'middle': sma,
            'upper': upper,
            'lower': lower,
            'bandwidth': bandwidth
        })

    @staticmethod
    def atr(
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        period: int = 14
    ) -> pd.Series:
        """
        Average True Range.

        Measures volatility.
        """
        prev_close = close.shift(1)
        tr1 = high - low
        tr2 = abs(high - prev_close)
        tr3 = abs(low - prev_close)
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        return tr.rolling(window=period).mean()

    @staticmethod
    def stochastic(
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        k_period: int = 14,
        d_period: int = 3
    ) -> pd.DataFrame:
        """
        Stochastic Oscillator.

        Momentum indicator comparing close to range.
        """
        lowest_low = low.rolling(window=k_period).min()
        highest_high = high.rolling(window=k_period).max()
        k = 100 * (close - lowest_low) / (highest_high - lowest_low + 1e-10)
        d = k.rolling(window=d_period).mean()

        return pd.DataFrame({'k': k, 'd': d})

    @staticmethod
    def cci(
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        period: int = 20
    ) -> pd.Series:
        """
        Commodity Channel Index.

        Measures current price vs average price.
        """
        tp = (high + low + close) / 3
        sma_tp = tp.rolling(window=period).mean()
        mad = tp.rolling(window=period).apply(
            lambda x: np.abs(x - x.mean()).mean(), raw=True
        )
        return (tp - sma_tp) / (0.015 * mad + 1e-10)

    @staticmethod
    def williams_r(
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        period: int = 14
    ) -> pd.Series:
        """Williams %R - momentum indicator."""
        highest_high = high.rolling(window=period).max()
        lowest_low = low.rolling(window=period).min()
        return -100 * (highest_high - close) / (highest_high - lowest_low + 1e-10)

    @staticmethod
    def obv(close: pd.Series, volume: pd.Series) -> pd.Series:
        """
        On-Balance Volume.

        Cumulative volume based on price direction.
        """
        direction = np.sign(close.diff())
        return (direction * volume).cumsum()

    @staticmethod
    def vwap(
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        volume: pd.Series
    ) -> pd.Series:
        """Volume Weighted Average Price."""
        tp = (high + low + close) / 3
        return (tp * volume).cumsum() / volume.cumsum()

    @staticmethod
    def adx(
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        period: int = 14
    ) -> pd.DataFrame:
        """
        Average Directional Index.

        Measures trend strength (not direction).
        """
        plus_dm = high.diff()
        minus_dm = -low.diff()

        plus_dm = plus_dm.where((plus_dm > minus_dm) & (plus_dm > 0), 0)
        minus_dm = minus_dm.where((minus_dm > plus_dm) & (minus_dm > 0), 0)

        # True Range
        prev_close = close.shift(1)
        tr = pd.concat([
            high - low,
            abs(high - prev_close),
            abs(low - prev_close)
        ], axis=1).max(axis=1)

        # Smoothed
        atr = tr.rolling(window=period).mean()
        plus_di = 100 * (plus_dm.rolling(window=period).mean() / (atr + 1e-10))
        minus_di = 100 * (minus_dm.rolling(window=period).mean() / (atr + 1e-10))

        dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di + 1e-10)
        adx = dx.rolling(window=period).mean()

        return pd.DataFrame({
            'adx': adx,
            'plus_di': plus_di,
            'minus_di': minus_di
        })

    @staticmethod
    def ichimoku(
        high: pd.Series,
        low: pd.Series,
        close: pd.Series
    ) -> pd.DataFrame:
        """
        Ichimoku Cloud.

        Comprehensive indicator showing support/resistance, momentum, trend.
        """
        # Tenkan-sen (Conversion Line)
        tenkan = (high.rolling(9).max() + low.rolling(9).min()) / 2

        # Kijun-sen (Base Line)
        kijun = (high.rolling(26).max() + low.rolling(26).min()) / 2

        # Senkou Span A (Leading Span A)
        senkou_a = ((tenkan + kijun) / 2).shift(26)

        # Senkou Span B (Leading Span B)
        senkou_b = ((high.rolling(52).max() + low.rolling(52).min()) / 2).shift(26)

        # Chikou Span (Lagging Span)
        chikou = close.shift(-26)

        return pd.DataFrame({
            'tenkan': tenkan,
            'kijun': kijun,
            'senkou_a': senkou_a,
            'senkou_b': senkou_b,
            'chikou': chikou
        })

    @staticmethod
    def momentum(series: pd.Series, period: int = 10) -> pd.Series:
        """Price momentum."""
        return series - series.shift(period)

    @staticmethod
    def rate_of_change(series: pd.Series, period: int = 10) -> pd.Series:
        """Rate of Change (ROC)."""
        return ((series - series.shift(period)) / series.shift(period)) * 100

    @staticmethod
    def calculate_all(
        df: pd.DataFrame,
        close_col: str = 'close',
        high_col: str = 'high',
        low_col: str = 'low',
        volume_col: str = 'volume'
    ) -> pd.DataFrame:
        """
        Calculate all technical indicators.

        Args:
            df: DataFrame with OHLCV data
            close_col, high_col, low_col, volume_col: Column names

        Returns:
            DataFrame with all indicators
        """
        result = df.copy()
        close = df[close_col]

        # Check available columns
        has_hlv = high_col in df.columns and low_col in df.columns
        has_volume = volume_col in df.columns

        # Moving averages
        for period in [5, 10, 20, 50, 200]:
            result[f'sma_{period}'] = TechnicalIndicators.sma(close, period)
            result[f'ema_{period}'] = TechnicalIndicators.ema(close, period)

        # Momentum indicators
        result['rsi_14'] = TechnicalIndicators.rsi(close, 14)
        result['momentum_10'] = TechnicalIndicators.momentum(close, 10)
        result['roc_10'] = TechnicalIndicators.rate_of_change(close, 10)

        # MACD
        macd = TechnicalIndicators.macd(close)
        result['macd'] = macd['macd']
        result['macd_signal'] = macd['signal']
        result['macd_histogram'] = macd['histogram']

        # Bollinger Bands
        bb = TechnicalIndicators.bollinger_bands(close)
        result['bb_upper'] = bb['upper']
        result['bb_middle'] = bb['middle']
        result['bb_lower'] = bb['lower']
        result['bb_bandwidth'] = bb['bandwidth']

        if has_hlv:
            high = df[high_col]
            low = df[low_col]

            # ATR
            result['atr_14'] = TechnicalIndicators.atr(high, low, close, 14)

            # Stochastic
            stoch = TechnicalIndicators.stochastic(high, low, close)
            result['stoch_k'] = stoch['k']
            result['stoch_d'] = stoch['d']

            # CCI
            result['cci_20'] = TechnicalIndicators.cci(high, low, close, 20)

            # Williams %R
            result['williams_r'] = TechnicalIndicators.williams_r(high, low, close)

            # ADX
            adx = TechnicalIndicators.adx(high, low, close)
            result['adx'] = adx['adx']
            result['plus_di'] = adx['plus_di']
            result['minus_di'] = adx['minus_di']

            # Ichimoku
            ich = TechnicalIndicators.ichimoku(high, low, close)
            for col in ich.columns:
                result[f'ichimoku_{col}'] = ich[col]

            if has_volume:
                volume = df[volume_col]
                result['obv'] = TechnicalIndicators.obv(close, volume)
                result['vwap'] = TechnicalIndicators.vwap(high, low, close, volume)

        return result


def add_technical_features(
    df: pd.DataFrame,
    price_col: str = 'close',
    include_all: bool = True
) -> pd.DataFrame:
    """
    Convenience function to add technical features.

    Args:
        df: DataFrame with price data
        price_col: Price column name
        include_all: Include all indicators or just essential ones

    Returns:
        DataFrame with technical features
    """
    ti = TechnicalIndicators()
    result = df.copy()
    price = df[price_col]

    if include_all and 'high' in df.columns:
        return ti.calculate_all(df)

    # Essential indicators only
    result['sma_20'] = ti.sma(price, 20)
    result['ema_20'] = ti.ema(price, 20)
    result['rsi_14'] = ti.rsi(price, 14)

    macd = ti.macd(price)
    result['macd'] = macd['macd']
    result['macd_signal'] = macd['signal']

    bb = ti.bollinger_bands(price)
    result['bb_upper'] = bb['upper']
    result['bb_lower'] = bb['lower']

    result['momentum'] = ti.momentum(price, 10)
    result['roc'] = ti.rate_of_change(price, 10)

    return result
