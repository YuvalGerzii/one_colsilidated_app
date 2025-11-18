"""
LLM Market Intelligence Integration

Enhances market intelligence data with AI-powered insights and analysis.
"""

import logging
from typing import Optional, Dict, Any, List
from datetime import datetime

from app.services.llm_service import llm_service

logger = logging.getLogger(__name__)


class LLMMarketIntelligenceService:
    """
    Service for generating AI-powered market intelligence insights.

    Integrates with existing market intelligence endpoints to provide:
    - Market trend analysis
    - Investment opportunity identification
    - Risk assessment
    - Comparative market analysis
    """

    async def generate_market_summary(
        self,
        market_data: Dict[str, Any],
        location: str,
        time_period: Optional[str] = None
    ) -> Optional[str]:
        """
        Generate comprehensive market summary from data.

        Args:
            market_data: Market statistics and metrics
            location: Market location
            time_period: Optional time period description

        Returns:
            Generated summary or None
        """
        system_prompt = """You are a real estate market analyst. Provide clear, concise market summaries
that highlight key trends, opportunities, and risks for investors."""

        # Extract key metrics
        metrics_summary = self._format_metrics(market_data)

        prompt = f"""Analyze the real estate market for {location}"""

        if time_period:
            prompt += f" ({time_period})"

        prompt += f"""

Market Data:
{metrics_summary}

Provide a concise 3-paragraph summary covering:
1. Current market conditions and trends
2. Key opportunities for investors
3. Risks and considerations"""

        result = await llm_service.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.4,
            max_tokens=400,
            use_cache=True
        )

        return result["text"] if result else None

    async def identify_investment_opportunities(
        self,
        market_data: Dict[str, Any],
        location: str,
        investment_criteria: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        """
        Identify specific investment opportunities based on market data.

        Args:
            market_data: Market statistics
            location: Market location
            investment_criteria: Optional investment preferences

        Returns:
            Investment opportunities analysis
        """
        system_prompt = """You are an investment analyst specializing in real estate.
Identify specific, actionable investment opportunities based on market data."""

        metrics = self._format_metrics(market_data)

        prompt = f"""Based on the following market data for {location}, identify specific investment opportunities:

{metrics}
"""

        if investment_criteria:
            prompt += f"\n\nInvestment Criteria:\n{self._format_dict(investment_criteria)}"

        prompt += """

Provide:
1. Top 3 investment opportunities
2. Rationale for each
3. Entry strategies
4. Expected returns range"""

        result = await llm_service.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.5,
            max_tokens=500,
            use_cache=True
        )

        return result["text"] if result else None

    async def analyze_market_trends(
        self,
        historical_data: List[Dict[str, Any]],
        location: str
    ) -> Optional[str]:
        """
        Analyze market trends from historical data.

        Args:
            historical_data: Time series market data
            location: Market location

        Returns:
            Trend analysis
        """
        system_prompt = """You are a data analyst specializing in real estate market trends.
Identify patterns, inflection points, and forecast future directions."""

        # Format historical data
        timeline = "\n".join([
            f"{item.get('period', i)}: {self._format_metrics(item)}"
            for i, item in enumerate(historical_data[-12:])  # Last 12 periods
        ])

        prompt = f"""Analyze market trends for {location} based on this historical data:

{timeline}

Provide:
1. Key trends identified
2. Inflection points or significant changes
3. Forecast for next 6-12 months
4. Confidence level in forecast"""

        result = await llm_service.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.4,
            max_tokens=450,
            use_cache=True
        )

        return result["text"] if result else None

    async def compare_markets(
        self,
        markets: List[Dict[str, Any]],
        comparison_focus: Optional[str] = None
    ) -> Optional[str]:
        """
        Compare multiple real estate markets.

        Args:
            markets: List of market data dictionaries
            comparison_focus: Optional focus area

        Returns:
            Comparative analysis
        """
        system_prompt = """You are a market analyst comparing real estate markets.
Provide objective comparisons highlighting strengths and trade-offs."""

        markets_summary = "\n\n".join([
            f"{market.get('location', f'Market {i+1}')}:\n{self._format_metrics(market)}"
            for i, market in enumerate(markets)
        ])

        prompt = f"""Compare these real estate markets:

{markets_summary}
"""

        if comparison_focus:
            prompt += f"\n\nFocus on: {comparison_focus}"

        prompt += """

Provide:
1. Comparative ranking with justification
2. Best market for different investor profiles
3. Unique advantages of each market
4. Risk comparison"""

        result = await llm_service.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.4,
            max_tokens=500,
            use_cache=True
        )

        return result["text"] if result else None

    async def assess_market_risk(
        self,
        market_data: Dict[str, Any],
        location: str,
        property_type: Optional[str] = None
    ) -> Optional[str]:
        """
        Assess risks in a specific market.

        Args:
            market_data: Market statistics
            location: Market location
            property_type: Optional property type focus

        Returns:
            Risk assessment
        """
        system_prompt = """You are a real estate risk analyst. Identify and evaluate market risks
objectively, providing actionable mitigation strategies."""

        metrics = self._format_metrics(market_data)

        prompt = f"""Assess investment risks for the {location} real estate market"""

        if property_type:
            prompt += f" ({property_type} properties)"

        prompt += f"""

Market Data:
{metrics}

Provide:
1. Risk level assessment (High/Medium/Low)
2. Top 3-5 risk factors
3. Leading indicators to monitor
4. Risk mitigation strategies"""

        result = await llm_service.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.3,
            max_tokens=450,
            use_cache=True
        )

        return result["text"] if result else None

    async def generate_market_report(
        self,
        market_data: Dict[str, Any],
        location: str,
        report_type: str = "comprehensive"
    ) -> Optional[Dict[str, str]]:
        """
        Generate a complete market report with multiple sections.

        Args:
            market_data: Market statistics
            location: Market location
            report_type: Report type (comprehensive, summary, investment_focus)

        Returns:
            Dictionary with report sections
        """
        logger.info(f"Generating {report_type} market report for {location}")

        report_sections = {}

        # Executive Summary
        summary = await self.generate_market_summary(
            market_data, location
        )
        if summary:
            report_sections["executive_summary"] = summary

        # Investment Opportunities
        opportunities = await self.identify_investment_opportunities(
            market_data, location
        )
        if opportunities:
            report_sections["investment_opportunities"] = opportunities

        # Risk Assessment
        risk = await self.assess_market_risk(
            market_data, location
        )
        if risk:
            report_sections["risk_assessment"] = risk

        report_sections["generated_at"] = datetime.utcnow().isoformat()
        report_sections["location"] = location
        report_sections["llm_generated"] = True

        return report_sections if report_sections else None

    def _format_metrics(self, data: Dict[str, Any]) -> str:
        """Format metrics dictionary for LLM consumption"""
        formatted = []
        for key, value in data.items():
            if isinstance(value, (int, float)):
                formatted.append(f"- {key.replace('_', ' ').title()}: {value:,}")
            elif isinstance(value, str):
                formatted.append(f"- {key.replace('_', ' ').title()}: {value}")
        return "\n".join(formatted)

    def _format_dict(self, data: Dict[str, Any]) -> str:
        """Format dictionary for LLM consumption"""
        import json
        return json.dumps(data, indent=2)


# Global instance
llm_market_intelligence = LLMMarketIntelligenceService()
