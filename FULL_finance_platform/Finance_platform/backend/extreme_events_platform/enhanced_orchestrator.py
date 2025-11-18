"""
Enhanced Orchestrator for Extreme Events Platform V5.0
Integrates all advanced components: generalized framework, behavior prediction,
market direction, multi-agent LLM system, NLP/news analysis, economic events,
cross-sector contagion analysis, and advanced trading strategies
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import json

# Core components
from .core.generalized_framework import GeneralizedEventFramework, EventCharacteristics, PredictionOutput
from .behavioral.human_behavior_predictor import HumanBehaviorPredictor
from .market.direction_predictor import MarketDirectionPredictor
from .multi_agent.multi_agent_orchestrator import MultiAgentOrchestrator

# NLP and News Analysis (V3.0)
from .nlp.sentiment_analyzer import FinancialNLPAnalyzer
from .nlp.news_analyzer import RealTimeNewsAnalyzer
from .nlp.mcp_context_manager import MCPContextManager

# All agents
from .agents import (
    PandemicAgent,
    TerrorismAgent,
    NaturalDisasterAgent,
    EconomicCrisisAgent,
    GeopoliticalAgent
)
from .agents.cyber_attack_agent import CyberAttackAgent
from .agents.climate_crisis_agent import ClimateCrisisAgent
from .agents.compound_event_agent import CompoundEventAgent

# Economic event agents (V3.0)
from .agents.recession_agent import RecessionAgent
from .agents.inflation_agent import InflationAgent
from .agents.interest_rate_agent import InterestRateAgent

# Cross-sector event agents (V5.0)
from .agents.weather_event_agent import WeatherEventAgent
from .agents.energy_event_agent import EnergyEventAgent

# Advanced strategies (V5.0)
from .strategies.cross_sector_contagion import CrossSectorContagionAnalyzer
from .strategies.supply_chain_disruption import SupplyChainDisruptionAnalyzer
from .strategies.commodity_arbitrage import CommodityArbitrageAnalyzer
from .strategies.sector_rotation import SectorRotationOptimizer

from .config.config import EVENT_TYPES
from .config.extended_config import EXTENDED_EVENT_TYPES


class EnhancedExtremeEventsOrchestrator:
    """
    Enhanced orchestrator V5.0 with:
    - Generalized event handling
    - Human behavior prediction
    - Market direction prediction (winners/losers)
    - Multi-agent LLM analysis
    - NLP and sentiment analysis
    - Real-time news monitoring
    - MCP (Model Context Protocol) integration
    - Economic event prediction (recession, inflation, interest rates)
    - Cross-sector contagion analysis (V5.0)
    - Supply chain disruption strategies (V5.0)
    - Commodity arbitrage opportunities (V5.0)
    - Advanced sector rotation optimization (V5.0)
    - Weather and energy event analysis (V5.0)
    - 17+ event types
    """

    def __init__(self, config: Optional[Dict] = None, enable_llm: bool = True, enable_nlp: bool = True, enable_v5_strategies: bool = True):
        """
        Initialize enhanced orchestrator V5.0

        Args:
            config: Optional configuration
            enable_llm: Enable LLM-based multi-agent system
            enable_nlp: Enable NLP and news analysis
            enable_v5_strategies: Enable V5.0 cross-sector strategies
        """
        from .config import config as default_config

        self.config = config or default_config
        self.enable_llm = enable_llm
        self.enable_nlp = enable_nlp
        self.enable_v5_strategies = enable_v5_strategies

        # Initialize core frameworks
        self.generalized_framework = GeneralizedEventFramework()
        self.behavior_predictor = HumanBehaviorPredictor()
        self.direction_predictor = MarketDirectionPredictor()

        # Initialize V5.0 strategy modules
        if self.enable_v5_strategies:
            try:
                self.contagion_analyzer = CrossSectorContagionAnalyzer()
                self.supply_chain_analyzer = SupplyChainDisruptionAnalyzer()
                self.commodity_arbitrage = CommodityArbitrageAnalyzer()
                self.sector_rotation = SectorRotationOptimizer()
                print("✓ V5.0 Cross-Sector Strategies Enabled")
            except Exception as e:
                print(f"⚠ V5.0 Strategies unavailable ({e}), continuing without advanced strategies")
                self.enable_v5_strategies = False

        # Initialize NLP and news analysis (V3.0)
        if self.enable_nlp:
            try:
                self.nlp_analyzer = FinancialNLPAnalyzer()
                self.news_analyzer = RealTimeNewsAnalyzer(self.nlp_analyzer)
                self.mcp_manager = MCPContextManager()
                print("✓ NLP and News Analysis Enabled")
            except Exception as e:
                print(f"⚠ NLP System unavailable ({e}), continuing without news analysis")
                self.enable_nlp = False

        # Initialize multi-agent system
        if self.enable_llm:
            try:
                self.llm_orchestrator = MultiAgentOrchestrator()
                print("✓ LLM Multi-Agent System Enabled")
            except Exception as e:
                print(f"⚠ LLM System unavailable ({e}), continuing with standard analysis")
                self.enable_llm = False

        # Initialize all specialized agents
        self.agents = self._initialize_all_agents()

        # Register all event types and agents with framework
        self._register_with_framework()

        self.analysis_history = []

    def _initialize_all_agents(self) -> Dict:
        """Initialize all 17+ specialized agents"""
        agents = {
            # Original 5 agents
            'pandemic': PandemicAgent(self.config),
            'terrorism': TerrorismAgent(self.config),
            'natural_disaster': NaturalDisasterAgent(self.config),
            'economic_crisis': EconomicCrisisAgent(self.config),
            'geopolitical': GeopoliticalAgent(self.config),

            # Extended agents (V2.0)
            'cyber_attack': CyberAttackAgent(self.config),
            'climate_crisis': ClimateCrisisAgent(self.config),
            'compound_event': CompoundEventAgent(self.config),

            # Economic event agents (V3.0)
            'recession': RecessionAgent(self.config),
            'inflation': InflationAgent(self.config),
            'interest_rate_change': InterestRateAgent(self.config),

            # Cross-sector event agents (V5.0)
            'weather_event': WeatherEventAgent(self.config),
            'energy_event': EnergyEventAgent(self.config),

            # Generic handler for unlisted events
            'generic': None  # Will use generalized framework
        }

        return agents

    def _register_with_framework(self):
        """Register event types and agents with generalized framework"""
        # Register original event types
        for event_type, characteristics in EVENT_TYPES.items():
            self.generalized_framework.register_event_type(event_type, characteristics)

        # Register extended event types
        for event_type, characteristics in EXTENDED_EVENT_TYPES.items():
            self.generalized_framework.register_event_type(event_type, characteristics)

        # Register agents
        for event_type, agent in self.agents.items():
            if agent is not None:
                self.generalized_framework.register_agent(event_type, agent)

    def comprehensive_analysis(
        self,
        event_type: str,
        event_data: Dict,
        news_items: Optional[List[str]] = None,
        use_llm_agents: bool = True,
        use_v5_strategies: bool = True
    ) -> Dict:
        """
        Perform comprehensive analysis with all systems (V5.0)

        Args:
            event_type: Type of extreme event
            event_data: Event data dictionary
            news_items: Optional list of news headlines/articles for NLP analysis
            use_llm_agents: Whether to use LLM multi-agent system
            use_v5_strategies: Whether to use V5.0 cross-sector strategies

        Returns:
            Comprehensive analysis with all components
        """
        print("\n" + "="*80)
        print(f"COMPREHENSIVE EXTREME EVENT ANALYSIS V5.0: {event_type.upper()}")
        print("="*80)

        # Phase 1: Normalize event data using generalized framework
        print("\n[Phase 1] Event Normalization...")
        event_data['event_type'] = event_type
        normalized_event = self.generalized_framework.normalize_event_data(event_data)

        # Phase 2: NLP and News Analysis (V3.0)
        news_analysis = None
        event_warnings = None
        mcp_context = None
        if self.enable_nlp and news_items:
            print("\n[Phase 2] NLP and News Analysis...")
            try:
                news_analysis = self.news_analyzer.analyze_news_stream(news_items)
                event_warnings = news_analysis.get('warnings', [])

                # Create MCP context for LLM agents
                mcp_context = self.mcp_manager.create_context_for_event(
                    event_type=event_type,
                    event_data=event_data,
                    news_items=news_items,
                    historical_data={}  # Can be populated with historical data
                )
                print(f"  ✓ Analyzed {len(news_items)} news items")
                print(f"  ✓ Detected {len(event_warnings)} event warnings")
            except Exception as e:
                print(f"  ⚠ News analysis failed: {e}")

        # Phase 3: Specialized agent analysis
        print(f"\n[Phase 3] Specialized Agent Analysis...")
        agent_analysis = self._run_specialized_agent(event_type, event_data, normalized_event)

        # Phase 4: Human behavior prediction
        print("\n[Phase 4] Human Behavior Prediction...")
        behavior_prediction = self.behavior_predictor.predict_behavior(event_data)
        crowd_psychology = self.behavior_predictor.predict_crowd_psychology(event_data)
        market_participation = self.behavior_predictor.predict_market_participation(event_data)

        # Phase 5: Market direction prediction (what goes up/down)
        print("\n[Phase 5] Market Direction Analysis (Winners/Losers)...")
        market_directions = self.direction_predictor.predict_directions(event_type, event_data)
        trading_opportunities = self.direction_predictor.get_trading_opportunities(event_type, event_data)
        hedging_strategies = self.direction_predictor.get_hedging_strategies({}, event_type, event_data)

        # Phase 6: Multi-agent LLM analysis (if enabled) with MCP context
        llm_analysis = None
        if self.enable_llm and use_llm_agents:
            print("\n[Phase 6] Multi-Agent LLM Analysis...")
            try:
                # Enrich event_data with MCP context if available
                if mcp_context:
                    event_data['mcp_context'] = self.mcp_manager.get_context_for_llm(mcp_context)
                llm_analysis = self.llm_orchestrator.analyze_event_multi_agent(event_data)
            except Exception as e:
                print(f"  ⚠ LLM analysis failed: {e}")

        # Phase 6.5: V5.0 Cross-Sector Strategy Analysis
        v5_analysis = None
        if self.enable_v5_strategies and use_v5_strategies:
            print("\n[Phase 6.5] V5.0 Cross-Sector Strategy Analysis...")
            try:
                v5_analysis = self._run_v5_strategies(event_type, event_data, normalized_event)
                print(f"  ✓ Contagion paths analyzed: {len(v5_analysis.get('contagion_analysis', {}).get('contagion_paths', []))}")
                print(f"  ✓ Arbitrage opportunities: {len(v5_analysis.get('arbitrage_opportunities', []))}")
            except Exception as e:
                print(f"  ⚠ V5.0 strategy analysis failed: {e}")

        # Phase 7: Synthesis
        print("\n[Phase 7] Synthesizing Results...")
        synthesis = self._synthesize_all_results(
            normalized_event,
            agent_analysis,
            behavior_prediction,
            market_directions,
            llm_analysis,
            news_analysis
        )

        print("\n[Complete] Comprehensive Analysis V5.0 Complete")
        print("="*80 + "\n")

        # Compile comprehensive report
        comprehensive_report = {
            'analysis_id': f"{event_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'event_category': normalized_event.category.value,

            # Core analysis
            'normalized_event': self._event_to_dict(normalized_event),
            'agent_analysis': agent_analysis,

            # NLP and News Analysis (V3.0)
            'news_analysis': news_analysis,
            'event_warnings': event_warnings,

            # Behavioral analysis
            'human_behavior': {
                'individual_behavior': self._behavior_to_dict(behavior_prediction),
                'crowd_psychology': crowd_psychology,
                'market_participation': market_participation
            },

            # Market direction analysis
            'market_directions': {
                'winners': [self._direction_to_dict(w) for w in market_directions['winners']],
                'losers': [self._direction_to_dict(l) for l in market_directions['losers']],
                'safe_havens': [self._direction_to_dict(s) for s in market_directions['safe_havens']],
                'summary': market_directions['summary']
            },

            # Trading intelligence
            'trading_opportunities': trading_opportunities,
            'hedging_strategies': hedging_strategies,

            # LLM analysis (with MCP context)
            'llm_multi_agent_analysis': llm_analysis,
            'mcp_context_used': mcp_context is not None,

            # V5.0 Cross-Sector Strategy Analysis
            'v5_cross_sector_analysis': v5_analysis,

            # Synthesis
            'synthesis': synthesis,

            # Actionable intelligence
            'actionable_intelligence': self._generate_actionable_intelligence(
                normalized_event,
                behavior_prediction,
                market_directions,
                synthesis
            )
        }

        # Store in history
        self.analysis_history.append(comprehensive_report)

        return comprehensive_report

    def _run_specialized_agent(
        self,
        event_type: str,
        event_data: Dict,
        normalized_event: EventCharacteristics
    ) -> Dict:
        """Run specialized agent analysis"""
        if event_type in self.agents and self.agents[event_type] is not None:
            agent = self.agents[event_type]
            return agent.analyze_event(event_data)
        else:
            # Use generalized framework for unknown event types
            print(f"  Using generalized analysis for {event_type}")
            return {
                'method': 'generalized',
                'severity_assessment': normalized_event.severity,
                'predictions': {
                    'market_impact': -10.0 * (normalized_event.severity / 3.0),
                    'recovery_days': 90 * (normalized_event.severity / 3.0)
                }
            }

    def _run_v5_strategies(
        self,
        event_type: str,
        event_data: Dict,
        normalized_event: EventCharacteristics
    ) -> Dict:
        """Run V5.0 cross-sector strategy analysis"""

        v5_analysis = {
            'contagion_analysis': None,
            'supply_chain_analysis': None,
            'arbitrage_opportunities': [],
            'sector_rotation': None
        }

        # Determine source sector and shock magnitude
        source_sector = event_data.get('source_sector', self._infer_source_sector(event_type))
        shock_magnitude = event_data.get('shock_magnitude', -10.0 * (normalized_event.severity / 3.0))

        # Run contagion analysis
        if source_sector:
            try:
                contagion = self.contagion_analyzer.analyze_contagion(
                    source_sector=source_sector,
                    shock_magnitude=shock_magnitude,
                    event_description=event_type
                )
                v5_analysis['contagion_analysis'] = contagion
            except Exception as e:
                print(f"    ⚠ Contagion analysis failed: {e}")

        # Run supply chain disruption analysis if relevant
        if event_type in ['supply_shock', 'energy_event', 'weather_event', 'geopolitical']:
            try:
                # Identify relevant bottleneck
                bottleneck = self._identify_bottleneck(event_type, event_data)
                if bottleneck:
                    duration = event_data.get('estimated_duration_days', 60)
                    supply_chain = self.supply_chain_analyzer.analyze_disruption(
                        bottleneck_name=bottleneck,
                        trigger_event=event_type,
                        estimated_duration_days=duration
                    )
                    v5_analysis['supply_chain_analysis'] = {
                        'bottleneck': supply_chain.bottleneck,
                        'severity': supply_chain.severity.value,
                        'probability': supply_chain.probability,
                        'affected_sectors': supply_chain.affected_sectors,
                        'trading_strategy': supply_chain.trading_strategy
                    }
            except Exception as e:
                print(f"    ⚠ Supply chain analysis failed: {e}")

        # Run commodity arbitrage analysis for relevant events
        if event_type in ['energy_event', 'inflation', 'supply_shock']:
            try:
                affected_commodities = self._identify_affected_commodities(event_type)
                price_impacts = {c: shock_magnitude for c in affected_commodities}

                arbitrage = self.commodity_arbitrage.identify_arbitrage(
                    event_type=event_type,
                    affected_commodities=affected_commodities,
                    price_changes=price_impacts
                )

                v5_analysis['arbitrage_opportunities'] = [
                    {
                        'name': opp.name,
                        'type': opp.type.value,
                        'long': opp.long_leg,
                        'short': opp.short_leg,
                        'dislocation': f"{opp.spread_z_score:.1f} std devs",
                        'catalyst': opp.catalyst
                    }
                    for opp in arbitrage[:5]  # Top 5
                ]
            except Exception as e:
                print(f"    ⚠ Arbitrage analysis failed: {e}")

        # Run sector rotation optimization
        try:
            from .strategies.sector_rotation import EventCategory, RotationPhase

            # Map event_type to EventCategory
            event_category = self._map_to_event_category(event_type)
            rotation_phase = RotationPhase.PANIC  # Default to panic phase

            rotation = self.sector_rotation.optimize_allocation(
                event_type=event_category,
                phase=rotation_phase,
                conviction=0.85
            )

            v5_analysis['sector_rotation'] = {
                'overweights': rotation.overweights,
                'underweights': rotation.underweights,
                'hedges': rotation.hedges,
                'expected_sharpe': rotation.expected_sharpe,
                'allocations': [
                    {
                        'sector': alloc.sector,
                        'weight': alloc.target_weight,
                        'conviction': alloc.conviction,
                        'expected_alpha': alloc.expected_alpha
                    }
                    for alloc in rotation.allocations[:10]  # Top 10
                ]
            }
        except Exception as e:
            print(f"    ⚠ Sector rotation analysis failed: {e}")

        return v5_analysis

    def _infer_source_sector(self, event_type: str) -> str:
        """Infer source sector from event type"""
        mappings = {
            'energy_event': 'energy',
            'weather_event': 'agriculture',
            'pandemic': 'healthcare',
            'cyber_attack': 'technology',
            'financial_crisis': 'financials',
            'inflation': 'energy',
            'recession': 'financials',
            'supply_shock': 'semiconductors'
        }
        return mappings.get(event_type, 'energy')

    def _identify_bottleneck(self, event_type: str, event_data: Dict) -> Optional[str]:
        """Identify relevant supply chain bottleneck"""
        mappings = {
            'energy_event': 'strait_hormuz',
            'weather_event': 'panama_canal',
            'supply_shock': 'taiwan_semiconductors',
            'geopolitical': 'suez_canal'
        }
        return mappings.get(event_type)

    def _identify_affected_commodities(self, event_type: str) -> List[str]:
        """Identify affected commodities"""
        mappings = {
            'energy_event': ['oil', 'natural_gas', 'power'],
            'inflation': ['gold', 'oil', 'natural_gas'],
            'supply_shock': ['oil', 'copper']
        }
        return mappings.get(event_type, ['oil'])

    def _map_to_event_category(self, event_type: str):
        """Map event_type string to EventCategory enum"""
        from .strategies.sector_rotation import EventCategory

        mappings = {
            'recession': EventCategory.RECESSION,
            'inflation': EventCategory.INFLATION,
            'energy_event': EventCategory.ENERGY_CRISIS,
            'supply_shock': EventCategory.SUPPLY_SHOCK,
            'financial_crisis': EventCategory.FINANCIAL_CRISIS,
            'geopolitical': EventCategory.GEOPOLITICAL,
            'pandemic': EventCategory.PANDEMIC,
            'cyber_attack': EventCategory.TECH_DISRUPTION
        }
        return mappings.get(event_type, EventCategory.RECESSION)

    def _synthesize_all_results(
        self,
        normalized_event: EventCharacteristics,
        agent_analysis: Dict,
        behavior: Any,
        directions: Dict,
        llm_analysis: Optional[Dict],
        news_analysis: Optional[Dict] = None
    ) -> Dict:
        """Synthesize results from all analysis components (V3.0)"""

        # Extract key metrics
        market_impact = agent_analysis.get('predictions', {}).get('market_predictions', {}).get('overall_market_impact', -10.0)
        dominant_emotion = behavior.dominant_emotion
        top_winner = directions['winners'][0] if directions['winners'] else None
        top_loser = directions['losers'][0] if directions['losers'] else None

        # Determine overall sentiment (adjust based on news if available)
        if market_impact < -15:
            overall_sentiment = 'very_bearish'
        elif market_impact < -5:
            overall_sentiment = 'bearish'
        elif market_impact < 5:
            overall_sentiment = 'neutral'
        else:
            overall_sentiment = 'bullish'

        # Adjust sentiment based on news analysis
        if news_analysis and 'aggregate_sentiment' in news_analysis:
            news_sentiment = news_analysis['aggregate_sentiment']
            if news_sentiment['sentiment'] == 'negative' and news_sentiment['average_score'] < -0.5:
                # News is very negative, make sentiment more bearish
                if overall_sentiment == 'neutral':
                    overall_sentiment = 'bearish'
                elif overall_sentiment == 'bearish':
                    overall_sentiment = 'very_bearish'

        # Key insights
        key_insights = []
        key_insights.append(f"Market expected to decline {abs(market_impact):.1f}%")
        key_insights.append(f"Dominant emotion: {dominant_emotion}")

        # Add news insights
        if news_analysis and 'aggregate_sentiment' in news_analysis:
            news_sent = news_analysis['aggregate_sentiment']
            key_insights.append(f"News sentiment: {news_sent['sentiment']} (score: {news_sent['average_score']:.2f})")

        if top_winner:
            key_insights.append(f"Top opportunity: {top_winner.name} (+{top_winner.expected_change_pct:.0f}%)")
        if top_loser:
            key_insights.append(f"Most vulnerable: {top_loser.name} ({top_loser.expected_change_pct:.0f}%)")

        # Add LLM insights if available
        if llm_analysis:
            confidence = llm_analysis.get('confidence_metrics', {}).get('overall_confidence', 0.7)
            key_insights.append(f"Multi-agent consensus confidence: {confidence*100:.0f}%")

        # List components used
        components_used = [
            'specialized_agent',
            'behavior_prediction',
            'market_direction'
        ]
        if news_analysis:
            components_used.append('nlp_news_analysis')
        if llm_analysis:
            components_used.append('llm_multi_agent')

        return {
            'overall_sentiment': overall_sentiment,
            'market_impact_estimate': market_impact,
            'severity_score': normalized_event.severity,
            'dominant_human_response': dominant_emotion,
            'risk_level': normalized_event.category.value,
            'key_insights': key_insights,
            'analysis_completeness': 'comprehensive_v3',
            'components_used': components_used
        }

    def _generate_actionable_intelligence(
        self,
        normalized_event: EventCharacteristics,
        behavior: Any,
        directions: Dict,
        synthesis: Dict
    ) -> Dict:
        """Generate actionable intelligence for decision-makers"""

        severity = normalized_event.severity

        # Risk level determination
        if severity >= 5:
            action_urgency = 'IMMEDIATE'
        elif severity >= 4:
            action_urgency = 'URGENT'
        elif severity >= 3:
            action_urgency = 'HIGH'
        else:
            action_urgency = 'MODERATE'

        # Portfolio actions
        portfolio_actions = []
        if severity >= 4:
            portfolio_actions.extend([
                'Reduce equity exposure by 30-50%',
                'Raise cash to 25%+',
                'Implement tail risk hedges'
            ])
        elif severity >= 3:
            portfolio_actions.extend([
                'Increase defensive positioning',
                'Add gold and safe havens',
                'Reduce leverage'
            ])

        # Specific opportunities from directions
        long_opportunities = [
            f"{w.name} ({w.rationale})"
            for w in directions['winners'][:3]
        ]

        short_opportunities = [
            f"{l.name} ({l.rationale})"
            for l in directions['losers'][:3]
        ]

        return {
            'action_urgency': action_urgency,
            'immediate_actions': portfolio_actions,
            'long_opportunities': long_opportunities,
            'short_opportunities': short_opportunities,
            'behavioral_caution': f"Expect {behavior.dominant_emotion} to drive irrational decisions",
            'time_horizon': behavior.time_horizon_shift,
            'monitoring_priorities': [
                'Policy response announcements',
                'Behavioral indicators (VIX, put/call ratio)',
                'Sector rotation signals'
            ]
        }

    # Helper methods to convert dataclasses to dict
    def _event_to_dict(self, event: EventCharacteristics) -> Dict:
        """Convert EventCharacteristics to dict"""
        return {
            'event_type': event.event_type,
            'category': event.category.value,
            'severity': event.severity,
            'geographic_scope': event.geographic_scope,
            'fear_factor': event.fear_factor,
            'anger_factor': event.anger_factor,
            'uncertainty_factor': event.uncertainty_factor
        }

    def _behavior_to_dict(self, behavior) -> Dict:
        """Convert BehavioralPrediction to dict"""
        return {
            'dominant_emotion': behavior.dominant_emotion,
            'emotion_intensity': behavior.emotion_intensity,
            'behavioral_patterns': behavior.behavioral_patterns,
            'risk_tolerance_change': behavior.risk_tolerance_change,
            'time_horizon_shift': behavior.time_horizon_shift,
            'social_behaviors': behavior.social_behaviors,
            'economic_behaviors': behavior.economic_behaviors
        }

    def _direction_to_dict(self, direction) -> Dict:
        """Convert MarketDirection to dict"""
        return {
            'name': direction.name,
            'category': direction.category,
            'direction': direction.direction,
            'expected_change_pct': direction.expected_change_pct,
            'confidence': direction.confidence,
            'rationale': direction.rationale,
            'time_horizon': direction.time_horizon
        }

    def export_comprehensive_report(
        self,
        analysis_result: Dict,
        format: str = 'json',
        filepath: str = None
    ) -> str:
        """
        Export comprehensive analysis report

        Args:
            analysis_result: Analysis result
            format: Export format ('json', 'text', 'summary')
            filepath: Optional filepath

        Returns:
            Formatted report
        """
        if format == 'json':
            report = json.dumps(analysis_result, indent=2, default=str)
        elif format == 'summary':
            report = self._format_summary_report(analysis_result)
        else:
            report = self._format_detailed_text_report(analysis_result)

        if filepath:
            with open(filepath, 'w') as f:
                f.write(report)
            print(f"Report saved to: {filepath}")

        return report

    def _format_summary_report(self, analysis: Dict) -> str:
        """Format executive summary report"""
        synthesis = analysis['synthesis']
        intel = analysis['actionable_intelligence']

        report = []
        report.append("="*80)
        report.append("EXECUTIVE SUMMARY - EXTREME EVENT ANALYSIS")
        report.append("="*80)
        report.append(f"\nEvent: {analysis['event_type'].upper()}")
        report.append(f"Severity: {synthesis['severity_score']}/5 ({intel['action_urgency']})")
        report.append(f"Market Impact: {synthesis['market_impact_estimate']:.1f}%")
        report.append(f"Overall Sentiment: {synthesis['overall_sentiment'].upper()}")

        report.append("\n" + "-"*80)
        report.append("KEY INSIGHTS")
        report.append("-"*80)
        for insight in synthesis['key_insights']:
            report.append(f"• {insight}")

        report.append("\n" + "-"*80)
        report.append("IMMEDIATE ACTIONS")
        report.append("-"*80)
        for action in intel['immediate_actions']:
            report.append(f"→ {action}")

        report.append("\n" + "-"*80)
        report.append("OPPORTUNITIES")
        report.append("-"*80)
        report.append("LONG:")
        for opp in intel['long_opportunities'][:3]:
            report.append(f"  + {opp}")

        report.append("\n" + "="*80 + "\n")

        return "\n".join(report)

    def _format_detailed_text_report(self, analysis: Dict) -> str:
        """Format detailed text report"""
        # Similar to summary but with more detail
        return self._format_summary_report(analysis)  # Placeholder

    def query_llm_agent(
        self,
        agent_role: str,
        question: str,
        context: Dict
    ) -> str:
        """
        Query a specific LLM agent directly

        Args:
            agent_role: Role of agent to query
            question: Question to ask
            context: Context data

        Returns:
            Agent's response
        """
        if not self.enable_llm:
            return "LLM system not enabled"

        return self.llm_orchestrator.query_agent(agent_role, question, context)

    # V6.0 Early Warning System Methods
    def run_early_warning_check(self, market_data: Dict) -> Dict:
        """
        Run early warning crisis detection (V6.0)

        Args:
            market_data: Current market indicators

        Returns:
            Early warning analysis with crisis predictions
        """
        try:
            from .early_warning import EarlyWarningSystem
            from .early_warning.crisis_monitor import CrisisMonitor
            from .agents.crisis_detection import BankingCrisisAgent, HousingBubbleAgent

            ews = EarlyWarningSystem()
            monitor = CrisisMonitor()

            # Run comprehensive check
            result = monitor.update_and_check(market_data, force_check=True)

            # Run specialized agents if relevant
            banking_result = None
            housing_result = None

            if 'bank_leverage' in market_data or 'credit_to_gdp_gap' in market_data:
                banking_agent = BankingCrisisAgent()
                banking_result = banking_agent.analyze_event(market_data)

            if 'price_to_income_ratio' in market_data:
                housing_agent = HousingBubbleAgent()
                housing_result = housing_agent.analyze_event(market_data)

            return {
                'monitor_status': result,
                'banking_crisis_analysis': banking_result,
                'housing_bubble_analysis': housing_result,
                'summary': monitor.get_summary()
            }

        except Exception as e:
            return {
                'error': str(e),
                'message': 'Early warning system unavailable. Install dependencies or check module.'
            }

    # V7.0 Market Reading Methods
    def run_market_reading_analysis(self, market_data: Dict) -> Dict:
        """
        Run comprehensive market reading analysis (V7.0)

        Analyzes:
        - Order flow and tape reading
        - Market microstructure (dark pools, institutional flow)
        - Market breadth (McClellan, TRIN, A/D line)
        - Intermarket relationships

        Args:
            market_data: Market data including:
                - trades: List of trade data
                - dark_prints: Dark pool prints
                - order_book: Current order book
                - breadth_data: Daily breadth data
                - asset_prices: Prices for stocks, bonds, commodities, dollar

        Returns:
            Comprehensive market reading analysis
        """
        try:
            from .market_reading import (
                OrderFlowAnalyzer,
                MicrostructureAnalyzer,
                BreadthAnalyzer,
                IntermarketAnalyzer,
                Trade,
                TradeAggressor,
                DarkPoolPrint,
                DailyBreadthData,
                AssetClassData,
                OrderBookLevel
            )

            results = {}

            # Order Flow Analysis
            if 'trades' in market_data:
                order_flow = OrderFlowAnalyzer()
                trades = []
                for t in market_data['trades']:
                    trades.append(Trade(
                        timestamp=t.get('timestamp', datetime.now()),
                        price=t.get('price', 0),
                        size=t.get('size', 0),
                        aggressor=TradeAggressor.BUYER if t.get('side') == 'buy' else TradeAggressor.SELLER,
                        is_block=t.get('size', 0) > 10000,
                        is_odd_lot=t.get('size', 0) % 100 != 0
                    ))
                
                price_history = market_data.get('price_history', [])
                flow_analysis = order_flow.analyze_tape(trades, price_history)
                
                results['order_flow'] = {
                    'cumulative_delta': flow_analysis.cumulative_delta,
                    'signal': flow_analysis.signal.value,
                    'confidence': flow_analysis.confidence,
                    'absorption_detected': flow_analysis.absorption_detected,
                    'exhaustion_detected': flow_analysis.exhaustion_detected,
                    'institutional_activity': flow_analysis.institutional_activity,
                    'key_levels': flow_analysis.key_levels,
                    'recommendation': flow_analysis.trading_recommendation
                }

            # Microstructure Analysis
            if 'dark_prints' in market_data or 'order_book' in market_data:
                microstructure = MicrostructureAnalyzer()
                
                dark_prints = []
                for dp in market_data.get('dark_prints', []):
                    dark_prints.append(DarkPoolPrint(
                        timestamp=dp.get('timestamp', datetime.now()),
                        price=dp.get('price', 0),
                        size=dp.get('size', 0),
                        venue=dp.get('venue', 'UNKNOWN'),
                        is_block=dp.get('size', 0) > 10000,
                        price_improvement=dp.get('price_improvement', 0)
                    ))
                
                # Process order book
                order_book = {'bids': [], 'asks': []}
                raw_book = market_data.get('order_book', {})
                for side in ['bids', 'asks']:
                    for level in raw_book.get(side, []):
                        order_book[side].append(OrderBookLevel(
                            price=level.get('price', 0),
                            size=level.get('size', 0),
                            num_orders=level.get('num_orders', 1)
                        ))
                
                lit_trades = market_data.get('lit_trades', [])
                nbbo = market_data.get('nbbo', {'bid': 0, 'ask': 0})
                
                micro_analysis = microstructure.analyze_microstructure(
                    lit_trades, dark_prints, order_book, nbbo
                )
                
                results['microstructure'] = {
                    'dark_pool_percentage': micro_analysis.dark_pool_percentage,
                    'institutional_flow_score': micro_analysis.institutional_flow_score,
                    'hft_activity': micro_analysis.hft_activity_score,
                    'hidden_liquidity': micro_analysis.hidden_liquidity_detected,
                    'order_book_imbalance': micro_analysis.order_book_imbalance,
                    'smart_money_direction': micro_analysis.smart_money_direction,
                    'participant_breakdown': micro_analysis.participant_breakdown,
                    'signals': micro_analysis.trading_signals,
                    'warnings': micro_analysis.risk_warnings,
                    'recommendations': micro_analysis.recommendations
                }

            # Breadth Analysis
            if 'breadth_data' in market_data:
                breadth = BreadthAnalyzer()
                
                breadth_data = []
                for bd in market_data['breadth_data']:
                    from datetime import date
                    breadth_data.append(DailyBreadthData(
                        date=bd.get('date', date.today()),
                        advances=bd.get('advances', 0),
                        declines=bd.get('declines', 0),
                        unchanged=bd.get('unchanged', 0),
                        advancing_volume=bd.get('advancing_volume', 0),
                        declining_volume=bd.get('declining_volume', 0),
                        new_highs=bd.get('new_highs', 0),
                        new_lows=bd.get('new_lows', 0),
                        total_issues=bd.get('total_issues', 3000)
                    ))
                
                index_prices = market_data.get('index_prices', [])
                breadth_analysis = breadth.analyze_breadth(breadth_data, index_prices)
                
                results['breadth'] = {
                    'ad_line': breadth_analysis.ad_line,
                    'ad_trend': breadth_analysis.ad_line_trend,
                    'ad_divergence': breadth_analysis.ad_divergence,
                    'mcclellan_oscillator': breadth_analysis.mcclellan_oscillator,
                    'mcclellan_summation': breadth_analysis.mcclellan_summation,
                    'trin': breadth_analysis.trin,
                    'trin_signal': breadth_analysis.trin_signal,
                    'new_highs_lows_ratio': breadth_analysis.new_highs_lows_ratio,
                    'percent_above_50ma': breadth_analysis.percent_above_50ma,
                    'overall_signal': breadth_analysis.overall_signal.value,
                    'breadth_thrust': breadth_analysis.breadth_thrust_detected,
                    'hindenburg_omen': breadth_analysis.hindenburg_omen_detected,
                    'confidence': breadth_analysis.confidence,
                    'signals': breadth_analysis.trading_signals,
                    'recommendations': breadth_analysis.recommendations
                }

            # Intermarket Analysis
            if 'asset_prices' in market_data:
                intermarket = IntermarketAnalyzer()
                
                assets = market_data['asset_prices']
                stocks = AssetClassData(name='stocks', prices=assets.get('stocks', []))
                bonds = AssetClassData(name='bonds', prices=assets.get('bonds', []))
                commodities = AssetClassData(name='commodities', prices=assets.get('commodities', []))
                dollar = AssetClassData(name='dollar', prices=assets.get('dollar', []))
                
                inter_analysis = intermarket.analyze_intermarket(
                    stocks, bonds, commodities, dollar
                )
                
                results['intermarket'] = {
                    'business_cycle_stage': inter_analysis.business_cycle_stage.value,
                    'market_regime': inter_analysis.market_regime.value,
                    'correlations': inter_analysis.correlations,
                    'correlation_changes': inter_analysis.correlation_changes,
                    'leading_indicators': inter_analysis.leading_indicators,
                    'asset_rankings': inter_analysis.asset_class_rankings,
                    'sector_recommendations': inter_analysis.sector_recommendations,
                    'risk_level': inter_analysis.risk_level,
                    'signals': inter_analysis.trading_signals,
                    'warnings': inter_analysis.warnings
                }

            # Generate combined summary
            results['summary'] = self._generate_market_reading_summary(results)

            return results

        except Exception as e:
            return {
                'error': str(e),
                'message': 'Market reading analysis failed. Check market_reading module.'
            }

    def _generate_market_reading_summary(self, results: Dict) -> Dict:
        """Generate combined summary from all market reading analyses"""
        summary = {
            'overall_bias': 'neutral',
            'confidence': 0.5,
            'key_signals': [],
            'immediate_actions': [],
            'warnings': []
        }

        bullish_signals = 0
        bearish_signals = 0

        # Order flow signals
        if 'order_flow' in results:
            flow = results['order_flow']
            if 'buying' in flow.get('signal', ''):
                bullish_signals += 1
                summary['key_signals'].append(f"Order flow: {flow['signal']}")
            elif 'selling' in flow.get('signal', ''):
                bearish_signals += 1
                summary['key_signals'].append(f"Order flow: {flow['signal']}")

        # Microstructure signals
        if 'microstructure' in results:
            micro = results['microstructure']
            if micro.get('smart_money_direction') == 'buying':
                bullish_signals += 1
                summary['key_signals'].append("Smart money accumulating")
            elif micro.get('smart_money_direction') == 'selling':
                bearish_signals += 1
                summary['key_signals'].append("Smart money distributing")
            summary['warnings'].extend(micro.get('warnings', []))

        # Breadth signals
        if 'breadth' in results:
            breadth = results['breadth']
            signal = breadth.get('overall_signal', '')
            if 'bullish' in signal:
                bullish_signals += 1
            elif 'bearish' in signal:
                bearish_signals += 1
            
            if breadth.get('breadth_thrust'):
                summary['key_signals'].append("BREADTH THRUST - highly bullish")
                bullish_signals += 2
            if breadth.get('hindenburg_omen'):
                summary['warnings'].append("HINDENBURG OMEN - crash risk elevated")
                bearish_signals += 2

        # Intermarket signals
        if 'intermarket' in results:
            inter = results['intermarket']
            summary['key_signals'].append(f"Cycle: {inter.get('business_cycle_stage')}")
            summary['key_signals'].append(f"Regime: {inter.get('market_regime')}")
            summary['warnings'].extend(inter.get('warnings', []))

        # Determine overall bias
        if bullish_signals > bearish_signals + 1:
            summary['overall_bias'] = 'bullish'
            summary['confidence'] = min(0.5 + (bullish_signals - bearish_signals) * 0.1, 0.9)
            summary['immediate_actions'].append("Consider adding long exposure")
        elif bearish_signals > bullish_signals + 1:
            summary['overall_bias'] = 'bearish'
            summary['confidence'] = min(0.5 + (bearish_signals - bullish_signals) * 0.1, 0.9)
            summary['immediate_actions'].append("Consider reducing exposure or hedging")
        else:
            summary['overall_bias'] = 'neutral'
            summary['immediate_actions'].append("Wait for clearer signals")

        return summary
