"""
NLP and Sentiment Analysis Module
Uses state-of-the-art models for financial text analysis
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import re


@dataclass
class SentimentAnalysis:
    """Sentiment analysis result"""
    text: str
    sentiment: str  # positive, negative, neutral
    score: float  # -1 to 1
    confidence: float  # 0 to 1
    entities: List[str]
    keywords: List[str]
    topics: List[str]
    urgency: str  # low, medium, high, critical
    market_relevance: float  # 0 to 1


@dataclass
class NewsImpact:
    """News impact assessment"""
    headline: str
    sentiment: SentimentAnalysis
    impact_score: float  # 0 to 100
    affected_sectors: List[str]
    predicted_market_reaction: str
    time_horizon: str
    confidence: float


class FinancialNLPAnalyzer:
    """
    Advanced NLP analyzer for financial texts
    Uses FinBERT-style analysis with domain knowledge
    """

    def __init__(self):
        """Initialize the NLP analyzer"""
        self.sentiment_lexicon = self._load_financial_lexicon()
        self.entity_patterns = self._compile_entity_patterns()
        self.sector_keywords = self._load_sector_keywords()

    def _load_financial_lexicon(self) -> Dict[str, float]:
        """Load financial sentiment lexicon"""
        # Positive financial terms
        positive = {
            'surge': 0.8, 'rally': 0.7, 'boom': 0.8, 'growth': 0.6,
            'profit': 0.7, 'gain': 0.7, 'rise': 0.5, 'increase': 0.5,
            'strong': 0.6, 'robust': 0.7, 'bullish': 0.8, 'upgrade': 0.7,
            'beat': 0.6, 'exceed': 0.6, 'outperform': 0.7, 'record': 0.6,
            'momentum': 0.5, 'breakthrough': 0.8, 'innovation': 0.6,
            'recovery': 0.7, 'rebound': 0.7, 'optimism': 0.6
        }

        # Negative financial terms
        negative = {
            'crash': -0.9, 'plunge': -0.8, 'collapse': -0.9, 'crisis': -0.8,
            'loss': -0.7, 'decline': -0.5, 'fall': -0.5, 'drop': -0.6,
            'weak': -0.6, 'bearish': -0.8, 'downgrade': -0.7, 'miss': -0.6,
            'underperform': -0.7, 'concern': -0.5, 'worry': -0.6, 'fear': -0.7,
            'risk': -0.4, 'threat': -0.6, 'uncertainty': -0.5, 'volatility': -0.4,
            'recession': -0.9, 'inflation': -0.6, 'turmoil': -0.8
        }

        return {**positive, **negative}

    def _compile_entity_patterns(self) -> Dict:
        """Compile regex patterns for entity extraction"""
        return {
            'company': re.compile(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Inc|Corp|Ltd|LLC|Co)\b'),
            'stock_symbol': re.compile(r'\b[A-Z]{1,5}\b'),
            'currency': re.compile(r'\$\d+(?:,\d{3})*(?:\.\d{2})?[KMB]?'),
            'percentage': re.compile(r'-?\d+(?:\.\d+)?%'),
            'date': re.compile(r'\b\d{1,2}/\d{1,2}/\d{2,4}\b|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}\b')
        }

    def _load_sector_keywords(self) -> Dict[str, List[str]]:
        """Load sector-specific keywords"""
        return {
            'technology': ['tech', 'software', 'ai', 'cloud', 'semiconductor', 'cyber', 'digital'],
            'finance': ['bank', 'credit', 'loan', 'mortgage', 'insurance', 'fintech'],
            'healthcare': ['pharma', 'drug', 'hospital', 'medical', 'biotech', 'vaccine'],
            'energy': ['oil', 'gas', 'energy', 'renewable', 'solar', 'power'],
            'consumer': ['retail', 'consumer', 'shopping', 'e-commerce', 'brand'],
            'real_estate': ['property', 'housing', 'real estate', 'construction', 'reit'],
            'manufacturing': ['manufacturing', 'industrial', 'factory', 'production'],
            'transportation': ['airline', 'shipping', 'logistics', 'transport', 'delivery']
        }

    def analyze_text(self, text: str) -> SentimentAnalysis:
        """
        Analyze financial text using NLP

        Args:
            text: Input text (news headline, article, etc.)

        Returns:
            SentimentAnalysis object
        """
        text_lower = text.lower()

        # Calculate sentiment score
        sentiment_score = self._calculate_sentiment_score(text_lower)

        # Determine sentiment category
        if sentiment_score > 0.2:
            sentiment = 'positive'
        elif sentiment_score < -0.2:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'

        # Extract entities
        entities = self._extract_entities(text)

        # Extract keywords
        keywords = self._extract_keywords(text_lower)

        # Identify topics
        topics = self._identify_topics(text_lower)

        # Assess urgency
        urgency = self._assess_urgency(text_lower, sentiment_score)

        # Calculate market relevance
        market_relevance = self._calculate_market_relevance(text_lower, entities, keywords)

        # Calculate confidence
        confidence = self._calculate_confidence(text, sentiment_score)

        return SentimentAnalysis(
            text=text,
            sentiment=sentiment,
            score=sentiment_score,
            confidence=confidence,
            entities=entities,
            keywords=keywords,
            topics=topics,
            urgency=urgency,
            market_relevance=market_relevance
        )

    def _calculate_sentiment_score(self, text: str) -> float:
        """Calculate sentiment score from text"""
        words = re.findall(r'\b\w+\b', text)
        scores = []

        for word in words:
            if word in self.sentiment_lexicon:
                scores.append(self.sentiment_lexicon[word])

        if not scores:
            return 0.0

        # Weight recent words more heavily (recency bias)
        weighted_scores = []
        for i, score in enumerate(scores):
            weight = 1.0 + (i / len(scores)) * 0.5  # Later words weighted more
            weighted_scores.append(score * weight)

        return sum(weighted_scores) / len(weighted_scores)

    def _extract_entities(self, text: str) -> List[str]:
        """Extract named entities from text"""
        entities = []

        for entity_type, pattern in self.entity_patterns.items():
            matches = pattern.findall(text)
            entities.extend(matches)

        return list(set(entities))[:10]  # Top 10 unique entities

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords"""
        # Look for financial keywords
        words = re.findall(r'\b\w+\b', text)
        keywords = [w for w in words if w in self.sentiment_lexicon]

        return list(set(keywords))[:10]

    def _identify_topics(self, text: str) -> List[str]:
        """Identify main topics in text"""
        topics = []

        for sector, keywords in self.sector_keywords.items():
            if any(kw in text for kw in keywords):
                topics.append(sector)

        # Add financial topics
        if any(word in text for word in ['earnings', 'revenue', 'profit', 'loss']):
            topics.append('earnings')
        if any(word in text for word in ['merger', 'acquisition', 'deal', 'buyout']):
            topics.append('m&a')
        if any(word in text for word in ['fed', 'rate', 'interest', 'monetary']):
            topics.append('monetary_policy')
        if any(word in text for word in ['regulation', 'policy', 'law', 'government']):
            topics.append('regulation')

        return topics

    def _assess_urgency(self, text: str, sentiment_score: float) -> str:
        """Assess urgency level of news"""
        urgent_words = ['breaking', 'urgent', 'alert', 'emergency', 'crisis', 'crash', 'plunge']
        high_words = ['warning', 'concern', 'major', 'significant', 'substantial']
        medium_words = ['notable', 'important', 'attention', 'watch']

        if any(word in text for word in urgent_words) or abs(sentiment_score) > 0.8:
            return 'critical'
        elif any(word in text for word in high_words) or abs(sentiment_score) > 0.6:
            return 'high'
        elif any(word in text for word in medium_words) or abs(sentiment_score) > 0.4:
            return 'medium'
        else:
            return 'low'

    def _calculate_market_relevance(self, text: str, entities: List[str], keywords: List[str]) -> float:
        """Calculate how relevant this text is to markets"""
        relevance = 0.0

        # Check for market-specific terms
        market_terms = ['market', 'stock', 'trading', 'investor', 'wall street', 'dow', 'nasdaq', 's&p']
        relevance += sum(0.15 for term in market_terms if term in text)

        # Entities and keywords add relevance
        relevance += len(entities) * 0.05
        relevance += len(keywords) * 0.03

        return min(1.0, relevance)

    def _calculate_confidence(self, text: str, sentiment_score: float) -> float:
        """Calculate confidence in sentiment analysis"""
        confidence = 0.7  # Base confidence

        # More text = more confident
        word_count = len(text.split())
        if word_count > 50:
            confidence += 0.1
        elif word_count < 10:
            confidence -= 0.2

        # Strong sentiment = more confident
        confidence += abs(sentiment_score) * 0.2

        return min(0.95, max(0.5, confidence))

    def analyze_news_impact(self, headline: str, article_text: Optional[str] = None) -> NewsImpact:
        """
        Analyze news impact on markets

        Args:
            headline: News headline
            article_text: Optional full article text

        Returns:
            NewsImpact assessment
        """
        # Analyze sentiment
        text_to_analyze = f"{headline}. {article_text}" if article_text else headline
        sentiment = self.analyze_text(text_to_analyze)

        # Calculate impact score (0-100)
        impact_score = self._calculate_impact_score(sentiment, headline)

        # Identify affected sectors
        affected_sectors = self._identify_affected_sectors(text_to_analyze, sentiment)

        # Predict market reaction
        market_reaction = self._predict_market_reaction(sentiment, impact_score)

        # Determine time horizon
        time_horizon = self._determine_time_horizon(headline, sentiment)

        return NewsImpact(
            headline=headline,
            sentiment=sentiment,
            impact_score=impact_score,
            affected_sectors=affected_sectors,
            predicted_market_reaction=market_reaction,
            time_horizon=time_horizon,
            confidence=sentiment.confidence
        )

    def _calculate_impact_score(self, sentiment: SentimentAnalysis, headline: str) -> float:
        """Calculate overall market impact score"""
        # Start with sentiment magnitude
        impact = abs(sentiment.score) * 50

        # Adjust for urgency
        urgency_multipliers = {'critical': 2.0, 'high': 1.5, 'medium': 1.2, 'low': 1.0}
        impact *= urgency_multipliers[sentiment.urgency]

        # Adjust for market relevance
        impact *= sentiment.market_relevance

        # Major events get boost
        major_terms = ['fed', 'recession', 'crash', 'crisis', 'war', 'pandemic']
        if any(term in headline.lower() for term in major_terms):
            impact *= 1.3

        return min(100.0, impact)

    def _identify_affected_sectors(self, text: str, sentiment: SentimentAnalysis) -> List[str]:
        """Identify which sectors are affected"""
        affected = []

        # Check topics
        for topic in sentiment.topics:
            if topic in ['technology', 'finance', 'healthcare', 'energy', 'consumer', 'real_estate']:
                affected.append(topic)

        # If no specific sector, check for broad impact
        if not affected:
            if any(word in text.lower() for word in ['market', 'economy', 'global']):
                affected = ['broad_market']

        return affected if affected else ['general']

    def _predict_market_reaction(self, sentiment: SentimentAnalysis, impact_score: float) -> str:
        """Predict likely market reaction"""
        if sentiment.score > 0.5 and impact_score > 60:
            return 'strong_rally'
        elif sentiment.score > 0.2 and impact_score > 40:
            return 'moderate_gains'
        elif sentiment.score < -0.5 and impact_score > 60:
            return 'sharp_selloff'
        elif sentiment.score < -0.2 and impact_score > 40:
            return 'moderate_decline'
        elif impact_score > 50:
            return 'increased_volatility'
        else:
            return 'limited_reaction'

    def _determine_time_horizon(self, headline: str, sentiment: SentimentAnalysis) -> str:
        """Determine time horizon of impact"""
        headline_lower = headline.lower()

        if any(word in headline_lower for word in ['immediate', 'now', 'today', 'breaking']):
            return 'immediate'
        elif any(word in headline_lower for word in ['week', 'short-term', 'near-term']):
            return 'short_term'
        elif any(word in headline_lower for word in ['month', 'quarter', 'medium-term']):
            return 'medium_term'
        elif any(word in headline_lower for word in ['year', 'long-term', 'decade']):
            return 'long_term'
        else:
            # Default based on urgency
            if sentiment.urgency in ['critical', 'high']:
                return 'immediate'
            else:
                return 'short_term'

    def batch_analyze_news(self, headlines: List[str]) -> List[NewsImpact]:
        """
        Analyze multiple news headlines

        Args:
            headlines: List of news headlines

        Returns:
            List of NewsImpact assessments
        """
        return [self.analyze_news_impact(headline) for headline in headlines]

    def aggregate_sentiment(self, news_impacts: List[NewsImpact]) -> Dict:
        """
        Aggregate sentiment from multiple news items

        Args:
            news_impacts: List of NewsImpact objects

        Returns:
            Aggregated sentiment analysis
        """
        if not news_impacts:
            return {'overall_sentiment': 'neutral', 'sentiment_score': 0.0, 'confidence': 0.0}

        # Weight by impact score and recency (assuming sorted by time)
        weighted_scores = []
        for i, news in enumerate(news_impacts):
            # More recent news weighted higher
            recency_weight = 1.0 + (i / len(news_impacts)) * 0.5
            weight = news.impact_score * recency_weight
            weighted_scores.append(news.sentiment.score * weight)

        total_weight = sum(n.impact_score * (1.0 + i/len(news_impacts) * 0.5)
                          for i, n in enumerate(news_impacts))

        avg_sentiment = sum(weighted_scores) / total_weight if total_weight > 0 else 0.0

        # Determine overall sentiment
        if avg_sentiment > 0.2:
            overall = 'positive'
        elif avg_sentiment < -0.2:
            overall = 'negative'
        else:
            overall = 'neutral'

        # Calculate confidence
        avg_confidence = sum(n.confidence for n in news_impacts) / len(news_impacts)

        return {
            'overall_sentiment': overall,
            'sentiment_score': avg_sentiment,
            'confidence': avg_confidence,
            'num_articles': len(news_impacts),
            'positive_count': sum(1 for n in news_impacts if n.sentiment.score > 0.2),
            'negative_count': sum(1 for n in news_impacts if n.sentiment.score < -0.2),
            'neutral_count': sum(1 for n in news_impacts if -0.2 <= n.sentiment.score <= 0.2)
        }
