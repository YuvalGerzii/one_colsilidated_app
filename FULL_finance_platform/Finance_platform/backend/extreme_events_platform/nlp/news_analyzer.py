"""
Real-Time News Analysis System
Monitors and analyzes news for event prediction and market impact
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from .sentiment_analyzer import FinancialNLPAnalyzer, NewsImpact


@dataclass
class NewsSignal:
    """Trading signal derived from news"""
    signal_type: str  # buy, sell, hold, hedge
    strength: float  # 0 to 1
    asset_class: str
    rationale: str
    confidence: float
    time_horizon: str
    timestamp: datetime


@dataclass
class EventWarning:
    """Early warning of potential extreme event"""
    event_type: str
    probability: float  # 0 to 1
    severity_estimate: int  # 1-5
    indicators: List[str]
    news_sources: List[str]
    confidence: float
    timestamp: datetime


class RealTimeNewsAnalyzer:
    """
    Real-time news analysis for event prediction
    Monitors news streams for early warning signals
    """

    def __init__(self):
        """Initialize news analyzer"""
        self.nlp_analyzer = FinancialNLPAnalyzer()
        self.news_buffer = []
        self.event_thresholds = self._define_event_thresholds()
        self.signal_history = []

    def _define_event_thresholds(self) -> Dict:
        """Define thresholds for different event types"""
        return {
            'recession': {
                'keywords': ['recession', 'economic downturn', 'contraction', 'slowdown'],
                'sentiment_threshold': -0.6,
                'frequency_threshold': 5,  # mentions per day
                'urgency_threshold': 'high'
            },
            'inflation': {
                'keywords': ['inflation', 'price surge', 'cpi', 'pce', 'cost increase'],
                'sentiment_threshold': -0.4,
                'frequency_threshold': 3,
                'urgency_threshold': 'medium'
            },
            'interest_rate_hike': {
                'keywords': ['rate hike', 'fed raises', 'interest rate increase', 'monetary tightening'],
                'sentiment_threshold': -0.3,
                'frequency_threshold': 2,
                'urgency_threshold': 'high'
            },
            'market_crash': {
                'keywords': ['crash', 'plunge', 'collapse', 'meltdown', 'panic'],
                'sentiment_threshold': -0.8,
                'frequency_threshold': 2,
                'urgency_threshold': 'critical'
            },
            'cyber_attack': {
                'keywords': ['cyber attack', 'hack', 'data breach', 'ransomware', 'security breach'],
                'sentiment_threshold': -0.5,
                'frequency_threshold': 1,
                'urgency_threshold': 'high'
            },
            'geopolitical_crisis': {
                'keywords': ['war', 'conflict', 'sanctions', 'military', 'tensions'],
                'sentiment_threshold': -0.6,
                'frequency_threshold': 3,
                'urgency_threshold': 'high'
            }
        }

    def analyze_news_stream(self, headlines: List[str], timestamps: Optional[List[datetime]] = None) -> Dict:
        """
        Analyze stream of news headlines

        Args:
            headlines: List of news headlines
            timestamps: Optional timestamps for each headline

        Returns:
            Comprehensive analysis including signals and warnings
        """
        if timestamps is None:
            timestamps = [datetime.now()] * len(headlines)

        # Analyze each headline
        news_impacts = []
        for headline, timestamp in zip(headlines, timestamps):
            impact = self.nlp_analyzer.analyze_news_impact(headline)
            news_impacts.append((impact, timestamp))

        # Aggregate sentiment
        sentiment = self.nlp_analyzer.aggregate_sentiment([ni[0] for ni in news_impacts])

        # Detect potential events
        warnings = self._detect_event_warnings(news_impacts)

        # Generate trading signals
        signals = self._generate_trading_signals(news_impacts, sentiment)

        # Identify trending topics
        trending = self._identify_trending_topics(news_impacts)

        # Assess market sentiment shift
        sentiment_shift = self._assess_sentiment_shift(news_impacts)

        return {
            'timestamp': datetime.now().isoformat(),
            'num_articles': len(headlines),
            'overall_sentiment': sentiment,
            'event_warnings': warnings,
            'trading_signals': signals,
            'trending_topics': trending,
            'sentiment_shift': sentiment_shift,
            'top_impacts': sorted(news_impacts, key=lambda x: x[0].impact_score, reverse=True)[:10]
        }

    def _detect_event_warnings(self, news_impacts: List[Tuple[NewsImpact, datetime]]) -> List[EventWarning]:
        """Detect early warning signals for extreme events"""
        warnings = []

        for event_type, threshold_config in self.event_thresholds.items():
            # Count keyword mentions
            mentions = []
            for impact, timestamp in news_impacts:
                headline_lower = impact.headline.lower()
                if any(kw in headline_lower for kw in threshold_config['keywords']):
                    mentions.append((impact, timestamp))

            if len(mentions) >= threshold_config['frequency_threshold']:
                # Calculate average sentiment of mentions
                avg_sentiment = sum(m[0].sentiment.score for m in mentions) / len(mentions)

                # Check if sentiment crosses threshold
                if avg_sentiment <= threshold_config['sentiment_threshold']:
                    # Estimate severity from sentiment and frequency
                    severity = min(5, int(len(mentions) + abs(avg_sentiment) * 3))

                    # Calculate probability
                    probability = min(0.95, (len(mentions) / 10) + abs(avg_sentiment))

                    # Extract indicators
                    indicators = [m[0].headline for m in mentions[:5]]

                    warning = EventWarning(
                        event_type=event_type,
                        probability=probability,
                        severity_estimate=severity,
                        indicators=indicators,
                        news_sources=[m[0].headline for m in mentions],
                        confidence=0.7,
                        timestamp=datetime.now()
                    )
                    warnings.append(warning)

        return sorted(warnings, key=lambda x: x.probability * x.severity_estimate, reverse=True)

    def _generate_trading_signals(self, news_impacts: List[Tuple[NewsImpact, datetime]], sentiment: Dict) -> List[NewsSignal]:
        """Generate trading signals from news analysis"""
        signals = []

        overall_score = sentiment['sentiment_score']
        confidence = sentiment['confidence']

        # Strong negative sentiment -> defensive signal
        if overall_score < -0.4 and confidence > 0.7:
            signals.append(NewsSignal(
                signal_type='hedge',
                strength=min(1.0, abs(overall_score)),
                asset_class='portfolio',
                rationale=f"Strong negative sentiment ({overall_score:.2f}) suggests market risk",
                confidence=confidence,
                time_horizon='immediate',
                timestamp=datetime.now()
            ))

        # Strong positive sentiment -> bullish signal
        elif overall_score > 0.4 and confidence > 0.7:
            signals.append(NewsSignal(
                signal_type='buy',
                strength=min(1.0, overall_score),
                asset_class='equities',
                rationale=f"Strong positive sentiment ({overall_score:.2f}) suggests upside",
                confidence=confidence,
                time_horizon='short_term',
                timestamp=datetime.now()
            ))

        # Sector-specific signals
        sector_signals = self._generate_sector_signals(news_impacts)
        signals.extend(sector_signals)

        return signals

    def _generate_sector_signals(self, news_impacts: List[Tuple[NewsImpact, datetime]]) -> List[NewsSignal]:
        """Generate sector-specific trading signals"""
        signals = []
        sector_sentiments = {}

        # Aggregate sentiment by sector
        for impact, timestamp in news_impacts:
            for sector in impact.affected_sectors:
                if sector not in sector_sentiments:
                    sector_sentiments[sector] = []
                sector_sentiments[sector].append(impact.sentiment.score)

        # Generate signals for sectors with strong sentiment
        for sector, scores in sector_sentiments.items():
            if len(scores) < 2:
                continue

            avg_score = sum(scores) / len(scores)

            if avg_score > 0.4:
                signals.append(NewsSignal(
                    signal_type='buy',
                    strength=avg_score,
                    asset_class=sector,
                    rationale=f"Positive news flow in {sector}",
                    confidence=0.7,
                    time_horizon='short_term',
                    timestamp=datetime.now()
                ))
            elif avg_score < -0.4:
                signals.append(NewsSignal(
                    signal_type='sell',
                    strength=abs(avg_score),
                    asset_class=sector,
                    rationale=f"Negative news flow in {sector}",
                    confidence=0.7,
                    time_horizon='short_term',
                    timestamp=datetime.now()
                ))

        return signals

    def _identify_trending_topics(self, news_impacts: List[Tuple[NewsImpact, datetime]]) -> List[Dict]:
        """Identify trending topics in news"""
        topic_counts = {}

        for impact, timestamp in news_impacts:
            for topic in impact.sentiment.topics:
                if topic not in topic_counts:
                    topic_counts[topic] = {'count': 0, 'avg_sentiment': 0, 'sentiments': []}

                topic_counts[topic]['count'] += 1
                topic_counts[topic]['sentiments'].append(impact.sentiment.score)

        # Calculate averages
        trending = []
        for topic, data in topic_counts.items():
            if data['count'] >= 2:
                avg_sentiment = sum(data['sentiments']) / len(data['sentiments'])
                trending.append({
                    'topic': topic,
                    'mention_count': data['count'],
                    'avg_sentiment': avg_sentiment,
                    'trend_strength': data['count'] * abs(avg_sentiment)
                })

        return sorted(trending, key=lambda x: x['trend_strength'], reverse=True)[:10]

    def _assess_sentiment_shift(self, news_impacts: List[Tuple[NewsImpact, datetime]]) -> Dict:
        """Assess if sentiment is shifting"""
        if len(news_impacts) < 5:
            return {'shift_detected': False, 'direction': 'stable', 'magnitude': 0.0}

        # Split into recent vs older
        mid_point = len(news_impacts) // 2
        older_impacts = news_impacts[:mid_point]
        recent_impacts = news_impacts[mid_point:]

        # Calculate sentiment for each period
        older_sentiment = sum(i[0].sentiment.score for i in older_impacts) / len(older_impacts)
        recent_sentiment = sum(i[0].sentiment.score for i in recent_impacts) / len(recent_impacts)

        # Detect shift
        shift = recent_sentiment - older_sentiment

        if abs(shift) > 0.3:
            return {
                'shift_detected': True,
                'direction': 'improving' if shift > 0 else 'deteriorating',
                'magnitude': abs(shift),
                'older_sentiment': older_sentiment,
                'recent_sentiment': recent_sentiment,
                'interpretation': 'Significant sentiment shift detected'
            }
        else:
            return {
                'shift_detected': False,
                'direction': 'stable',
                'magnitude': abs(shift),
                'interpretation': 'Sentiment relatively stable'
            }

    def predict_event_from_news(self, headlines: List[str]) -> Dict:
        """
        Predict potential extreme events from news analysis

        Args:
            headlines: Recent news headlines

        Returns:
            Event predictions with probabilities
        """
        # Analyze news stream
        analysis = self.analyze_news_stream(headlines)

        # Extract predictions
        predictions = []

        for warning in analysis['event_warnings']:
            predictions.append({
                'event_type': warning.event_type,
                'probability': warning.probability,
                'severity': warning.severity_estimate,
                'confidence': warning.confidence,
                'evidence': warning.indicators[:3],
                'recommended_action': self._recommend_action(warning)
            })

        # If no explicit warnings, check sentiment for implicit signals
        if not predictions:
            sentiment = analysis['overall_sentiment']
            if sentiment['sentiment_score'] < -0.5:
                predictions.append({
                    'event_type': 'market_stress',
                    'probability': abs(sentiment['sentiment_score']) * 0.7,
                    'severity': 3,
                    'confidence': sentiment['confidence'],
                    'evidence': ['Overall negative sentiment in news'],
                    'recommended_action': 'Increase defensive positioning'
                })

        return {
            'predictions': predictions,
            'analysis': analysis,
            'timestamp': datetime.now().isoformat()
        }

    def _recommend_action(self, warning: EventWarning) -> str:
        """Recommend action based on event warning"""
        if warning.probability > 0.7 and warning.severity_estimate >= 4:
            return 'URGENT: Reduce risk exposure immediately'
        elif warning.probability > 0.5 and warning.severity_estimate >= 3:
            return 'HIGH: Implement hedging strategies'
        elif warning.probability > 0.3:
            return 'MODERATE: Monitor closely and prepare contingencies'
        else:
            return 'LOW: Continue monitoring'

    def create_news_dashboard(self, headlines: List[str]) -> str:
        """
        Create a formatted news dashboard

        Args:
            headlines: Recent headlines

        Returns:
            Formatted dashboard string
        """
        analysis = self.analyze_news_stream(headlines)

        dashboard = []
        dashboard.append("="*80)
        dashboard.append("REAL-TIME NEWS ANALYSIS DASHBOARD")
        dashboard.append("="*80)
        dashboard.append(f"\nTimestamp: {analysis['timestamp']}")
        dashboard.append(f"Articles Analyzed: {analysis['num_articles']}")

        dashboard.append("\n" + "-"*80)
        dashboard.append("OVERALL SENTIMENT")
        dashboard.append("-"*80)
        sentiment = analysis['overall_sentiment']
        dashboard.append(f"Sentiment: {sentiment['overall_sentiment'].upper()}")
        dashboard.append(f"Score: {sentiment['sentiment_score']:.2f}")
        dashboard.append(f"Confidence: {sentiment['confidence']:.0%}")
        dashboard.append(f"Positive: {sentiment['positive_count']} | Negative: {sentiment['negative_count']} | Neutral: {sentiment['neutral_count']}")

        if analysis['event_warnings']:
            dashboard.append("\n" + "-"*80)
            dashboard.append("⚠️  EVENT WARNINGS")
            dashboard.append("-"*80)
            for warning in analysis['event_warnings'][:3]:
                dashboard.append(f"\n{warning.event_type.upper()}")
                dashboard.append(f"  Probability: {warning.probability:.0%}")
                dashboard.append(f"  Severity: {warning.severity_estimate}/5")
                dashboard.append(f"  Evidence: {warning.indicators[0]}")

        if analysis['trading_signals']:
            dashboard.append("\n" + "-"*80)
            dashboard.append("📊 TRADING SIGNALS")
            dashboard.append("-"*80)
            for signal in analysis['trading_signals'][:5]:
                dashboard.append(f"\n{signal.signal_type.upper()}: {signal.asset_class}")
                dashboard.append(f"  Strength: {signal.strength:.0%}")
                dashboard.append(f"  Rationale: {signal.rationale}")

        if analysis['trending_topics']:
            dashboard.append("\n" + "-"*80)
            dashboard.append("🔥 TRENDING TOPICS")
            dashboard.append("-"*80)
            for topic in analysis['trending_topics'][:5]:
                dashboard.append(f"  • {topic['topic']}: {topic['mention_count']} mentions (sentiment: {topic['avg_sentiment']:.2f})")

        dashboard.append("\n" + "="*80)

        return "\n".join(dashboard)
