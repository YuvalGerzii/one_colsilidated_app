"""
Financial Data Extractor

Rule-based financial data extraction that works without LLM.
Uses regex patterns, keyword matching, and structural analysis.
"""

import re
from typing import Dict, List, Optional, Any, Tuple
import logging

logger = logging.getLogger(__name__)


class FinancialExtractor:
    """
    Extract financial data from markdown text using rule-based methods.

    This class provides LLM-independent extraction using:
    - Regex patterns for financial metrics
    - Keyword matching
    - Table parsing
    - Structural analysis
    """

    # Financial metric patterns
    REVENUE_PATTERNS = [
        r'(?:total\s+)?revenue[s]?\s*[:=]?\s*\$?\s*([\d,]+\.?\d*)\s*(?:million|m|bn|billion)?',
        r'sales\s*[:=]?\s*\$?\s*([\d,]+\.?\d*)\s*(?:million|m|bn|billion)?',
        r'top\s+line\s*[:=]?\s*\$?\s*([\d,]+\.?\d*)\s*(?:million|m|bn|billion)?',
    ]

    EBITDA_PATTERNS = [
        r'ebitda\s*[:=]?\s*\$?\s*([\d,]+\.?\d*)\s*(?:million|m|bn|billion)?',
        r'adjusted\s+ebitda\s*[:=]?\s*\$?\s*([\d,]+\.?\d*)\s*(?:million|m|bn|billion)?',
    ]

    MARGIN_PATTERNS = [
        r'(?:ebitda|operating|gross|net)\s+margin\s*[:=]?\s*([\d.]+)%?',
        r'margin\s*[:=]?\s*([\d.]+)%',
    ]

    DEBT_PATTERNS = [
        r'(?:total\s+)?debt\s*[:=]?\s*\$?\s*([\d,]+\.?\d*)\s*(?:million|m|bn|billion)?',
        r'borrowings?\s*[:=]?\s*\$?\s*([\d,]+\.?\d*)\s*(?:million|m|bn|billion)?',
        r'leverage\s*[:=]?\s*([\d.]+)x?',
    ]

    CASH_PATTERNS = [
        r'cash(?:\s+and\s+equivalents?)?\s*[:=]?\s*\$?\s*([\d,]+\.?\d*)\s*(?:million|m|bn|billion)?',
        r'liquidity\s*[:=]?\s*\$?\s*([\d,]+\.?\d*)\s*(?:million|m|bn|billion)?',
    ]

    VALUATION_PATTERNS = [
        r'(?:enterprise\s+)?value\s*[:=]?\s*\$?\s*([\d,]+\.?\d*)\s*(?:million|m|bn|billion)?',
        r'valuation\s*[:=]?\s*\$?\s*([\d,]+\.?\d*)\s*(?:million|m|bn|billion)?',
        r'ev[/]ebitda\s*[:=]?\s*([\d.]+)x?',
        r'(?:p[/]e|price[/-]to[/-]earnings)\s*[:=]?\s*([\d.]+)x?',
    ]

    GROWTH_PATTERNS = [
        r'(?:revenue\s+)?growth\s*[:=]?\s*([\d.]+)%?',
        r'cagr\s*[:=]?\s*([\d.]+)%?',
        r'yoy\s+growth\s*[:=]?\s*([\d.]+)%?',
    ]

    def __init__(self):
        self.patterns = {
            'revenue': self.REVENUE_PATTERNS,
            'ebitda': self.EBITDA_PATTERNS,
            'margins': self.MARGIN_PATTERNS,
            'debt': self.DEBT_PATTERNS,
            'cash': self.CASH_PATTERNS,
            'valuation': self.VALUATION_PATTERNS,
            'growth': self.GROWTH_PATTERNS,
        }

    def extract_from_markdown(self, markdown_text: str) -> Dict[str, Any]:
        """
        Extract financial data from markdown text.

        Args:
            markdown_text: Markdown document text

        Returns:
            Dictionary of extracted financial metrics
        """
        text_lower = markdown_text.lower()

        result = {
            'revenue': self._extract_metric(text_lower, 'revenue'),
            'ebitda': self._extract_metric(text_lower, 'ebitda'),
            'margins': self._extract_metric(text_lower, 'margins'),
            'debt': self._extract_metric(text_lower, 'debt'),
            'cash': self._extract_metric(text_lower, 'cash'),
            'valuation': self._extract_metric(text_lower, 'valuation'),
            'growth': self._extract_metric(text_lower, 'growth'),
            'company_name': self._extract_company_name(markdown_text),
            'ticker': self._extract_ticker(markdown_text),
            'metrics_found': 0,
            'confidence': 0.0,
        }

        # Calculate metrics found and confidence
        result['metrics_found'] = sum(1 for k, v in result.items()
                                     if k not in ['metrics_found', 'confidence'] and v)
        result['confidence'] = min(result['metrics_found'] / 7.0, 1.0)

        return result

    def _extract_metric(self, text: str, metric_type: str) -> Optional[List[str]]:
        """Extract a specific metric using regex patterns."""
        patterns = self.patterns.get(metric_type, [])
        matches = []

        for pattern in patterns:
            found = re.findall(pattern, text, re.IGNORECASE)
            matches.extend(found)

        return matches if matches else None

    def _extract_company_name(self, text: str) -> Optional[str]:
        """Extract company name from markdown headers."""
        # Try to find in first few lines or headers
        lines = text.split('\n')[:10]

        for line in lines:
            # Check markdown headers
            if line.startswith('#'):
                name = line.lstrip('#').strip()
                if len(name) > 3 and not any(word in name.lower() for word in ['table', 'figure', 'summary']):
                    return name

        return None

    def _extract_ticker(self, text: str) -> Optional[str]:
        """Extract stock ticker symbol."""
        # Pattern for ticker symbols (3-5 uppercase letters)
        pattern = r'\b([A-Z]{3,5})\b'
        matches = re.findall(pattern, text[:500])  # Search in first 500 chars

        # Filter out common words
        common_words = {'THE', 'AND', 'FOR', 'INC', 'LLC', 'LTD', 'CORP'}
        tickers = [m for m in matches if m not in common_words]

        return tickers[0] if tickers else None

    def extract_tables(self, markdown_text: str) -> List[Dict[str, Any]]:
        """
        Extract tables from markdown.

        Args:
            markdown_text: Markdown text

        Returns:
            List of parsed tables
        """
        tables = []
        table_pattern = r'\|(.+)\|\n\|[-:\s|]+\|\n((?:\|.+\|\n?)+)'

        matches = re.finditer(table_pattern, markdown_text)

        for match in matches:
            header_row = match.group(1)
            data_rows = match.group(2)

            # Parse header
            headers = [h.strip() for h in header_row.split('|') if h.strip()]

            # Parse rows
            rows = []
            for row in data_rows.split('\n'):
                if '|' in row:
                    cells = [c.strip() for c in row.split('|') if c.strip()]
                    if cells:
                        rows.append(cells)

            if headers and rows:
                tables.append({
                    'headers': headers,
                    'rows': rows,
                    'row_count': len(rows),
                    'column_count': len(headers)
                })

        return tables

    def analyze_structure(self, markdown_text: str) -> Dict[str, Any]:
        """
        Analyze document structure.

        Returns:
            Structure analysis
        """
        return {
            'heading_count': markdown_text.count('\n#'),
            'h1_count': markdown_text.count('\n# '),
            'h2_count': markdown_text.count('\n## '),
            'h3_count': markdown_text.count('\n### '),
            'table_count': len(self.extract_tables(markdown_text)),
            'list_count': markdown_text.count('\n- ') + markdown_text.count('\n* '),
            'code_block_count': markdown_text.count('```'),
            'image_count': markdown_text.count('!['),
            'link_count': markdown_text.count(']('),
            'has_tables': '|' in markdown_text,
            'has_financial_terms': self._has_financial_terms(markdown_text),
            'word_count': len(markdown_text.split()),
            'line_count': len(markdown_text.split('\n')),
        }

    def _has_financial_terms(self, text: str) -> bool:
        """Check if text contains financial terminology."""
        financial_terms = [
            'revenue', 'ebitda', 'ebit', 'cash flow', 'debt', 'equity',
            'margin', 'valuation', 'dcf', 'wacc', 'irr', 'multiple',
            'balance sheet', 'income statement', 'p&l', 'assets', 'liabilities'
        ]
        text_lower = text.lower()
        return any(term in text_lower for term in financial_terms)

    def extract_for_dcf_model(self, markdown_text: str) -> Dict[str, Any]:
        """
        Extract data specifically for DCF model.

        Returns:
            DCF model data
        """
        general_data = self.extract_from_markdown(markdown_text)
        text_lower = markdown_text.lower()

        # Extract DCF-specific fields
        wacc_pattern = r'wacc\s*[:=]?\s*([\d.]+)%?'
        wacc_matches = re.findall(wacc_pattern, text_lower)

        terminal_pattern = r'(?:terminal|perpetual)\s+(?:growth|rate)\s*[:=]?\s*([\d.]+)%?'
        terminal_matches = re.findall(terminal_pattern, text_lower)

        tax_pattern = r'tax\s+rate\s*[:=]?\s*([\d.]+)%?'
        tax_matches = re.findall(tax_pattern, text_lower)

        beta_pattern = r'beta\s*[:=]?\s*([\d.]+)'
        beta_matches = re.findall(beta_pattern, text_lower)

        return {
            'company_name': general_data.get('company_name'),
            'ticker': general_data.get('ticker'),
            'revenue': general_data.get('revenue', [None])[0] if general_data.get('revenue') else None,
            'ebitda': general_data.get('ebitda', [None])[0] if general_data.get('ebitda') else None,
            'cash': general_data.get('cash', [None])[0] if general_data.get('cash') else None,
            'total_debt': general_data.get('debt', [None])[0] if general_data.get('debt') else None,
            'wacc': wacc_matches[0] if wacc_matches else None,
            'terminal_growth_rate': terminal_matches[0] if terminal_matches else None,
            'tax_rate': tax_matches[0] if tax_matches else None,
            'beta': beta_matches[0] if beta_matches else None,
            'revenue_growth_rate': general_data.get('growth', [None])[0] if general_data.get('growth') else None,
            'ebitda_margin': general_data.get('margins', [None])[0] if general_data.get('margins') else None,
        }

    def extract_for_lbo_model(self, markdown_text: str) -> Dict[str, Any]:
        """
        Extract data specifically for LBO model.

        Returns:
            LBO model data
        """
        general_data = self.extract_from_markdown(markdown_text)
        text_lower = markdown_text.lower()

        # Extract LBO-specific fields
        entry_multiple_pattern = r'(?:entry|purchase)\s+(?:ev[/]ebitda|multiple)\s*[:=]?\s*([\d.]+)x?'
        entry_matches = re.findall(entry_multiple_pattern, text_lower)

        exit_multiple_pattern = r'exit\s+(?:ev[/]ebitda|multiple)\s*[:=]?\s*([\d.]+)x?'
        exit_matches = re.findall(exit_multiple_pattern, text_lower)

        leverage_pattern = r'(?:total\s+)?leverage\s*[:=]?\s*([\d.]+)x?'
        leverage_matches = re.findall(leverage_pattern, text_lower)

        holding_pattern = r'holding\s+period\s*[:=]?\s*([\d]+)\s*(?:years?|yrs?)'
        holding_matches = re.findall(holding_pattern, text_lower)

        irr_pattern = r'irr\s*[:=]?\s*([\d.]+)%?'
        irr_matches = re.findall(irr_pattern, text_lower)

        return {
            'company_name': general_data.get('company_name'),
            'ltm_revenue': general_data.get('revenue', [None])[0] if general_data.get('revenue') else None,
            'ltm_ebitda': general_data.get('ebitda', [None])[0] if general_data.get('ebitda') else None,
            'purchase_price': general_data.get('valuation', [None])[0] if general_data.get('valuation') else None,
            'entry_ev_ebitda_multiple': entry_matches[0] if entry_matches else None,
            'exit_ev_ebitda_multiple': exit_matches[0] if exit_matches else None,
            'total_leverage': leverage_matches[0] if leverage_matches else None,
            'holding_period': holding_matches[0] if holding_matches else None,
            'target_irr': irr_matches[0] if irr_matches else None,
        }

    def assess_risk_factors(self, markdown_text: str) -> Dict[str, Any]:
        """
        Rule-based risk assessment.

        Returns:
            Risk analysis
        """
        text_lower = markdown_text.lower()

        # Risk keywords by category
        high_risk_keywords = ['bankruptcy', 'default', 'covenant breach', 'going concern',
                            'material weakness', 'significant doubt', 'liquidity crisis']
        medium_risk_keywords = ['challenging', 'headwinds', 'competitive pressure',
                               'market uncertainty', 'regulatory changes']
        financial_risk_keywords = ['leverage', 'debt', 'interest coverage', 'liquidity']
        operational_risk_keywords = ['supply chain', 'operations', 'efficiency', 'capacity']
        market_risk_keywords = ['competition', 'market share', 'pricing pressure']

        # Count keyword occurrences
        high_risk_count = sum(text_lower.count(kw) for kw in high_risk_keywords)
        medium_risk_count = sum(text_lower.count(kw) for kw in medium_risk_keywords)
        financial_risk_count = sum(text_lower.count(kw) for kw in financial_risk_keywords)
        operational_risk_count = sum(text_lower.count(kw) for kw in operational_risk_keywords)
        market_risk_count = sum(text_lower.count(kw) for kw in market_risk_keywords)

        # Determine risk level
        total_risk_score = (high_risk_count * 3) + (medium_risk_count * 1.5)

        if total_risk_score > 10:
            risk_level = "High"
        elif total_risk_score > 5:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        return {
            'risk_level': risk_level,
            'risk_score': min(total_risk_score / 10.0 * 10, 10),
            'high_risk_indicators': high_risk_count,
            'medium_risk_indicators': medium_risk_count,
            'financial_risk_mentions': financial_risk_count,
            'operational_risk_mentions': operational_risk_count,
            'market_risk_mentions': market_risk_count,
            'total_risk_mentions': high_risk_count + medium_risk_count,
        }

    def analyze_sentiment(self, markdown_text: str) -> Dict[str, Any]:
        """
        Rule-based sentiment analysis.

        Returns:
            Sentiment analysis
        """
        text_lower = markdown_text.lower()

        # Sentiment keywords
        positive_keywords = ['strong', 'growth', 'successful', 'improved', 'exceeding',
                           'outperform', 'robust', 'solid', 'momentum', 'optimistic']
        negative_keywords = ['weak', 'decline', 'challenging', 'concern', 'risk',
                           'pressure', 'underperform', 'disappointing', 'deteriorating']

        positive_count = sum(text_lower.count(kw) for kw in positive_keywords)
        negative_count = sum(text_lower.count(kw) for kw in negative_keywords)

        # Calculate sentiment score (1-10)
        net_sentiment = positive_count - negative_count
        sentiment_score = max(1, min(10, 5 + net_sentiment / 2))

        # Determine overall sentiment
        if sentiment_score > 6.5:
            sentiment = "Bullish"
        elif sentiment_score < 4.5:
            sentiment = "Bearish"
        else:
            sentiment = "Neutral"

        return {
            'sentiment': sentiment,
            'sentiment_score': sentiment_score,
            'positive_indicators': positive_count,
            'negative_indicators': negative_count,
            'net_sentiment': net_sentiment,
        }


# Global instance
financial_extractor = FinancialExtractor()
