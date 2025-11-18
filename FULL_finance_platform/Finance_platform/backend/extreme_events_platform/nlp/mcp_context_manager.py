"""
Model Context Protocol (MCP) Integration
Provides structured context understanding for LLM-based analysis
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class MCPResource:
    """MCP Resource following the protocol specification"""
    uri: str
    name: str
    description: str
    mimeType: str
    text: Optional[str] = None
    blob: Optional[bytes] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MCPContext:
    """Complete context package for LLM"""
    resources: List[MCPResource]
    tools: List[Dict]
    prompts: List[Dict]
    metadata: Dict[str, Any]
    timestamp: datetime


class MCPContextManager:
    """
    Model Context Protocol Manager
    Structures context for optimal LLM understanding and analysis
    """

    def __init__(self):
        """Initialize MCP Context Manager"""
        self.contexts = {}
        self.resources = []

    def create_context_for_event(
        self,
        event_type: str,
        event_data: Dict,
        news_items: Optional[List] = None,
        historical_data: Optional[List] = None
    ) -> MCPContext:
        """
        Create structured MCP context for event analysis

        Args:
            event_type: Type of extreme event
            event_data: Event data dictionary
            news_items: Optional news articles
            historical_data: Optional historical comparisons

        Returns:
            MCPContext object with structured information
        """
        resources = []
        tools = []
        prompts = []

        # 1. Event Data Resource
        event_resource = MCPResource(
            uri=f"event://{event_type}/{datetime.now().isoformat()}",
            name=f"{event_type}_event_data",
            description=f"Core data for {event_type} extreme event",
            mimeType="application/json",
            text=json.dumps(event_data, indent=2),
            metadata={
                'event_type': event_type,
                'timestamp': datetime.now().isoformat()
            }
        )
        resources.append(event_resource)

        # 2. Event Context Resource (domain knowledge)
        context_text = self._generate_domain_context(event_type, event_data)
        context_resource = MCPResource(
            uri=f"context://{event_type}/domain_knowledge",
            name=f"{event_type}_context",
            description=f"Domain knowledge and context for {event_type}",
            mimeType="text/plain",
            text=context_text,
            metadata={'type': 'domain_knowledge'}
        )
        resources.append(context_resource)

        # 3. News Resources (if provided)
        if news_items:
            news_resource = MCPResource(
                uri=f"news://{event_type}/recent",
                name="recent_news_coverage",
                description="Recent news articles about this event",
                mimeType="application/json",
                text=json.dumps(news_items, indent=2),
                metadata={'count': len(news_items), 'type': 'news'}
            )
            resources.append(news_resource)

        # 4. Historical Data Resources
        if historical_data:
            historical_resource = MCPResource(
                uri=f"historical://{event_type}",
                name="historical_comparisons",
                description="Similar historical events for comparison",
                mimeType="application/json",
                text=json.dumps(historical_data, indent=2),
                metadata={'count': len(historical_data), 'type': 'historical'}
            )
            resources.append(historical_resource)

        # 5. Analysis Tools (available to LLM)
        tools = self._define_analysis_tools(event_type)

        # 6. Prompts (structured prompts for different analysis types)
        prompts = self._generate_structured_prompts(event_type, event_data)

        # Create complete context
        context = MCPContext(
            resources=resources,
            tools=tools,
            prompts=prompts,
            metadata={
                'event_type': event_type,
                'context_version': '1.0',
                'created_at': datetime.now().isoformat(),
                'num_resources': len(resources),
                'num_tools': len(tools),
                'num_prompts': len(prompts)
            },
            timestamp=datetime.now()
        )

        # Store context
        context_id = f"{event_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.contexts[context_id] = context

        return context

    def _generate_domain_context(self, event_type: str, event_data: Dict) -> str:
        """Generate domain-specific context text"""
        context_templates = {
            'pandemic': """
DOMAIN CONTEXT: Pandemic Event Analysis

Key Factors to Consider:
- R0 (reproduction number): How contagious is the pathogen?
- Mortality rate: What is the case fatality rate?
- Healthcare capacity: Can hospitals handle the load?
- Containment measures: What interventions are in place?
- Vaccine availability: Is there a vaccine?
- Historical comparisons: COVID-19, SARS, H1N1, Spanish Flu

Market Impact Patterns:
- Immediate: Panic selling, flight to safety
- Short-term: Sector rotation (healthcare up, travel down)
- Medium-term: Policy response impact
- Long-term: Structural economic changes

Behavioral Factors:
- Fear drives initial reaction
- Uncertainty sustains volatility
- Policy confidence aids recovery
""",
            'recession': """
DOMAIN CONTEXT: Recession Analysis

Economic Indicators to Monitor:
- Yield curve inversion (best predictor)
- Unemployment rate trajectory
- GDP growth (negative for 2 quarters = technical recession)
- Consumer confidence indices
- Manufacturing PMI
- Retail sales trends

Recession Phases:
1. Early Warning: Yield curve inverts, confidence drops
2. Initial Decline: Job losses begin, spending falls
3. Contraction Peak: Maximum economic stress
4. Stabilization: Bottom formation
5. Recovery: Growth returns

Market Behavior:
- Lead indicator: Markets decline 6-12 months before recession
- Bottom: Often before economic recovery visible
- Defensive rotation: Utilities, consumer staples outperform
""",
            'inflation': """
DOMAIN CONTEXT: Inflation Analysis

Inflation Drivers:
- Demand-pull: Too much money chasing too few goods
- Cost-push: Supply chain issues, commodity prices
- Monetary: Central bank policy, money supply
- Expectations: Self-fulfilling inflation psychology

Fed Response Framework:
- 2% target inflation (PCE)
- Rate hiking cycle when above target
- 25-50 bps typical moves
- "Higher for longer" if inflation persistent

Market Effects:
- Bonds: Negative (inverse relationship with rates)
- Stocks: Mixed (depends on earnings vs. rates)
- Real Assets: Positive (commodities, TIPS, real estate)
- Cash: Negative (purchasing power erosion)
"""
        }

        # Return specific template or generic
        return context_templates.get(event_type, f"DOMAIN CONTEXT: {event_type.upper()} Analysis")

    def _define_analysis_tools(self, event_type: str) -> List[Dict]:
        """Define tools available for analysis"""
        tools = [
            {
                'name': 'calculate_sentiment',
                'description': 'Calculate sentiment score from text',
                'parameters': {
                    'text': 'string'
                },
                'returns': 'float (-1 to 1)'
            },
            {
                'name': 'identify_affected_sectors',
                'description': 'Identify market sectors affected by event',
                'parameters': {
                    'event_data': 'object'
                },
                'returns': 'array of sector names'
            },
            {
                'name': 'predict_market_direction',
                'description': 'Predict whether market will go up or down',
                'parameters': {
                    'event_severity': 'integer (1-5)',
                    'sentiment': 'float (-1 to 1)'
                },
                'returns': 'string (up/down/neutral)'
            },
            {
                'name': 'assess_behavioral_response',
                'description': 'Assess how people will behaviorally respond',
                'parameters': {
                    'event_type': 'string',
                    'severity': 'integer'
                },
                'returns': 'object with emotion, patterns, risk_tolerance'
            }
        ]

        # Add event-specific tools
        if event_type == 'recession':
            tools.append({
                'name': 'calculate_recession_probability',
                'description': 'Calculate probability of recession from indicators',
                'parameters': {
                    'yield_curve': 'float',
                    'unemployment': 'float',
                    'gdp_growth': 'float'
                },
                'returns': 'float (0 to 1)'
            })

        elif event_type == 'inflation':
            tools.append({
                'name': 'project_rate_path',
                'description': 'Project Federal Reserve interest rate path',
                'parameters': {
                    'current_inflation': 'float',
                    'target_inflation': 'float'
                },
                'returns': 'array of projected rates'
            })

        return tools

    def _generate_structured_prompts(self, event_type: str, event_data: Dict) -> List[Dict]:
        """Generate structured prompts for analysis"""
        prompts = []

        # Core analysis prompt
        severity = event_data.get('severity', 3)
        prompts.append({
            'name': 'analyze_event',
            'description': 'Comprehensive event analysis',
            'prompt': f"""Analyze this {event_type} event with severity {severity}/5.

Consider:
1. What is the likely market impact (direction and magnitude)?
2. Which sectors will be winners and losers?
3. How will human behavior respond (fear, panic, rational)?
4. What is the time horizon (immediate, short, medium, long-term)?
5. What are the key risks and opportunities?
6. What should investors do?

Provide specific, actionable insights with confidence levels."""
        })

        # Sentiment-focused prompt
        prompts.append({
            'name': 'analyze_sentiment',
            'description': 'Sentiment and behavioral analysis',
            'prompt': f"""Analyze the sentiment and behavioral implications of this {event_type} event.

Focus on:
- Dominant emotions (fear, anger, panic, anxiety)
- Crowd psychology and herd behavior
- Risk tolerance changes
- Likely market participant behavior
- Social amplification effects

Explain how sentiment will drive market moves."""
        })

        # Opportunity identification prompt
        prompts.append({
            'name': 'identify_opportunities',
            'description': 'Trading opportunity identification',
            'prompt': f"""Identify specific trading opportunities from this {event_type} event.

For each opportunity, specify:
- Asset/sector name
- Direction (long/short/hedge)
- Expected return
- Risk level
- Time horizon
- Entry/exit points
- Rationale

Prioritize by risk-adjusted return."""
        })

        return prompts

    def get_context_for_llm(self, context: MCPContext) -> str:
        """
        Format context for LLM consumption

        Args:
            context: MCPContext object

        Returns:
            Formatted context string
        """
        output = []

        output.append("="*80)
        output.append("MODEL CONTEXT PROTOCOL (MCP) - STRUCTURED CONTEXT")
        output.append("="*80)
        output.append("")

        # Resources section
        output.append("RESOURCES:")
        output.append("-"*80)
        for resource in context.resources:
            output.append(f"\n[{resource.name}]")
            output.append(f"URI: {resource.uri}")
            output.append(f"Description: {resource.description}")
            output.append(f"Type: {resource.mimeType}")
            if resource.text:
                output.append(f"\nContent:\n{resource.text[:500]}...")
            output.append("")

        # Tools section
        output.append("\nAVAILABLE TOOLS:")
        output.append("-"*80)
        for tool in context.tools:
            output.append(f"\n- {tool['name']}: {tool['description']}")
        output.append("")

        # Prompts section
        output.append("\nANALYSIS PROMPTS:")
        output.append("-"*80)
        for prompt in context.prompts:
            output.append(f"\n{prompt['name']}:")
            output.append(prompt['prompt'])
            output.append("")

        return "\n".join(output)

    def enrich_context_with_news(
        self,
        context: MCPContext,
        news_sentiment: Dict
    ) -> MCPContext:
        """
        Enrich existing context with news sentiment analysis

        Args:
            context: Existing MCPContext
            news_sentiment: News sentiment analysis results

        Returns:
            Enriched MCPContext
        """
        # Add news sentiment resource
        news_resource = MCPResource(
            uri="news://sentiment/analysis",
            name="news_sentiment_analysis",
            description="Aggregated news sentiment analysis",
            mimeType="application/json",
            text=json.dumps(news_sentiment, indent=2),
            metadata={'type': 'sentiment', 'source': 'news_aggregation'}
        )

        context.resources.append(news_resource)
        context.metadata['has_news_sentiment'] = True
        context.metadata['news_sentiment_score'] = news_sentiment.get('sentiment_score', 0.0)

        return context

    def create_chain_of_thought_context(
        self,
        event_type: str,
        event_data: Dict,
        domain_knowledge: str
    ) -> str:
        """
        Create Domain Knowledge Chain-of-Thought (DK-CoT) context
        Based on latest research for improved LLM reasoning

        Args:
            event_type: Event type
            event_data: Event data
            domain_knowledge: Domain-specific knowledge

        Returns:
            Structured CoT prompt
        """
        cot_prompt = f"""DOMAIN KNOWLEDGE CHAIN-OF-THOUGHT ANALYSIS

Event: {event_type.upper()}
Severity: {event_data.get('severity', 3)}/5

STEP 1: DOMAIN KNOWLEDGE APPLICATION
{domain_knowledge}

STEP 2: EVENT CHARACTERISTICS ANALYSIS
- Identify key characteristics of this specific event
- Compare to historical precedents
- Assess unique vs. common factors

STEP 3: CAUSAL REASONING
- What causes this event to impact markets?
- What are the transmission mechanisms?
- What amplifies or dampens the effect?

STEP 4: STAKEHOLDER IMPACT ANALYSIS
- Who is affected? (investors, consumers, businesses, governments)
- How do different stakeholders react?
- What are their incentives and constraints?

STEP 5: MARKET MECHANISM ANALYSIS
- How does this flow through to prices?
- What are the first-order effects?
- What are second and third-order effects?

STEP 6: BEHAVIORAL OVERLAY
- How do emotions affect the above analysis?
- Where does rational analysis diverge from likely reality?
- What behavioral biases are triggered?

STEP 7: SYNTHESIS AND PREDICTION
- Integrate all factors
- Provide probabilistic outcomes
- Specify confidence levels
- Identify key uncertainties

STEP 8: ACTIONABLE RECOMMENDATIONS
- What should be done?
- By whom?
- When?
- With what risk management?

Now, work through each step systematically for this event."""

        return cot_prompt
