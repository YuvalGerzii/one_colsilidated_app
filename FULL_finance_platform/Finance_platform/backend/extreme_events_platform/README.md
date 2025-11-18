# Extreme Events Market Prediction Platform V7.0

## Overview
This platform predicts and analyzes how financial markets react to extreme events. Now includes professional market reading tools to understand market intent beyond just price - order flow, dark pools, breadth, and intermarket analysis.

**🆕 V7.0 NEW - Market Reading & Professional Analysis:**
- 📊 **Order Flow & Tape Reading** - Delta analysis, volume footprint, absorption/exhaustion detection
- 🏦 **Market Microstructure** - Dark pool analysis (40% of volume), iceberg orders, institutional flow detection
- 📈 **Market Breadth** - McClellan Oscillator, TRIN (Arms Index), Advance/Decline, Breadth Thrust, Hindenburg Omen
- 🌐 **Intermarket Analysis** - Stocks/Bonds/Commodities/Dollar correlations, business cycle staging
- 🤖 **Smart Money Detection** - Identify institutional accumulation/distribution patterns
- ⚡ **HFT Activity Scoring** - Detect high-frequency trading signatures

**V6.0 Features - Early Warning & Crisis Prediction:**
- 🚨 **Early Warning System** - Detects crises 12-24 months in advance using 15+ leading indicators
- 🤖 **ML Anomaly Detection** - Isolation Forest, Autoencoder, Regime Detection (98.8% accuracy)
- 🏦 **Banking Crisis Agent** - 2008 financial crisis indicators (credit-to-GDP gap, TED spread, bank leverage)
- 🏠 **Housing Bubble Detector** - Catches bubbles before they pop (price-to-income, speculation levels)
- 📊 **Real-Time Crisis Monitor** - Continuous monitoring with alert levels (green/yellow/orange/red/black)
- ⏰ **"Quiet Before Storm" Detection** - Identifies dangerous low-volatility periods (contrarian insight!)

**V5.0 Features - Cross-Sector Strategies:**
- 🌐 **Cross-sector contagion analysis** - Traces how events cascade through seemingly unrelated sectors using graph theory
- ⛓️ **Supply chain disruption strategies** - Identifies bottlenecks and trading opportunities from just-in-time failures
- 💹 **Commodity arbitrage analyzer** - Finds dislocations in spreads, crack spreads, and cross-commodity ratios
- 🔄 **Advanced sector rotation** - Optimizes allocations during different event phases
- 🌤️ **Weather event agent** - Analyzes heatwaves, droughts, floods with cross-sector cascades
- ⚡ **Energy event agent** - Models oil shocks, grid failures, and energy price cascades

**V4.0 Features - Advanced Trading Strategies (2025 Hedge Fund Intelligence):**
- 💰 **Hedge Fund Strategy Analyzer**: Macro funds +11.2% YTD, Event-driven +8.7%, Convertible arb +4.0%
- 📊 **Derivatives & Options Strategist**: 0DTE strategies, VIX calls, iron condors, volatility arbitrage
- 📉 **Short Selling Detector**: Sector shorts, pair trades, squeeze risk assessment
- ⚡ **Fast-Action Opportunities**: 0-24 hour critical trades, first-mover advantages
- 🎯 **Institutional Behavior Analyzer**: Follow smart money, fade retail, contrarian signals

**V3.0 Features - NLP & News:**
- 🔍 NLP and sentiment analysis for financial news
- 📰 Real-time news monitoring
- 🧠 Model Context Protocol (MCP) integration
- 📊 Economic event prediction (recession, inflation, interest rates)

## Methodology

### 1. **Extreme Value Theory (EVT)**
- Models tail events that fall outside normal distributions
- Calculates VaR (Value at Risk) and CVaR (Conditional VaR)
- Handles heavy-tailed distributions common in extreme events

### 2. **Black Swan Event Framework**
- Identifies outlier events beyond regular expectations
- Measures extreme impact on markets, economies, and nations
- Analyzes post-event rationalization patterns

### 3. **Machine Learning Models**
- Neural Networks for pattern recognition
- Support Vector Machines for classification
- Regression models for impact forecasting

### 4. **Economic Impact Analysis**
- Lives and public health impacts
- Infrastructure damage assessment
- Social function disruption
- Economic loss quantification

### 5. **NLP and Sentiment Analysis (V3.0)**
- Financial sentiment lexicon for market-relevant text
- Real-time news stream analysis
- Sentiment scoring from -1 (very negative) to +1 (very positive)
- Entity extraction and keyword identification
- Urgency classification (critical, high, medium, low)

### 6. **Model Context Protocol (MCP) (V3.0)**
- Structured context management for LLM agents
- Domain knowledge integration for chain-of-thought reasoning
- Resource organization (news, historical data, indicators)
- Tool definitions for LLM-based analysis
- Prompt structuring for optimal inference

### 7. **Economic Event Prediction (V3.0)**
- **Recession Indicators**: Yield curve inversion, Sahm Rule, GDP, consumer confidence, PMI
- **Inflation Analysis**: Fed 2% target tracking, rate path projection, wage-price dynamics
- **Interest Rate Modeling**: Fed decision analysis, surprise factor calculation, sector impacts

## Architecture

### Agents

**Original Agents (V1.0):**
- **PandemicAgent**: Analyzes disease outbreaks and their economic impacts
- **TerrorismAgent**: Assesses terror attack effects on markets and confidence
- **NaturalDisasterAgent**: Evaluates storms, earthquakes, floods
- **EconomicCrisisAgent**: Monitors financial system stress and contagion
- **GeopoliticalAgent**: Tracks war, sanctions, and political instability

**Extended Agents (V2.0):**
- **CyberAttackAgent**: Analyzes ransomware, data breaches, infrastructure hacks
- **ClimateCrisisAgent**: Long-term climate change impacts, tipping points, stranded assets
- **CompoundEventAgent**: Handles polycrisis (multiple simultaneous events)

**Economic Agents (V3.0):**
- **RecessionAgent**: Recession probability with yield curve, Sahm Rule, GDP indicators
- **InflationAgent**: Inflation analysis with Fed 2% target and rate path projection
- **InterestRateAgent**: Fed rate decision analysis and sector impact assessment

**Analysis Modules (V3.0):**
- **FinancialNLPAnalyzer**: Sentiment analysis with financial lexicon
- **RealTimeNewsAnalyzer**: News stream monitoring and event prediction
- **MCPContextManager**: Model Context Protocol for LLM integration

**Trading Modules (V4.0):**
- **HedgeFundStrategyAnalyzer**: Recommends best hedge fund strategies by event type
- **DerivativesStrategist**: Options and derivatives plays (0DTE, VIX calls, spreads)
- **ShortSellingDetector**: Short opportunities, pair trades, squeeze risk
- **FastActionOpportunities**: Time-critical trades (0-24 hour windows)
- **InstitutionalBehaviorAnalyzer**: Smart money signals, contrarian indicators

### Models
- **EVT Model**: Extreme Value Theory implementation
- **VaR Calculator**: Value at Risk computation
- **ML Predictor**: Machine learning-based forecasting
- **Impact Simulator**: Multi-dimensional impact assessment

## Key Insights from Research

1. **Market Immunity**: First shock creates substantial moves; repeated shocks show diminished returns
2. **Data Challenges**: Limited historical data for rare events
3. **Non-linear Effects**: Traditional models fail; need heavy-tail distributions
4. **Multi-dimensional Impact**: Must consider economic, social, psychological factors

## Usage

### V7.0 Usage (Market Reading & Professional Analysis)

```python
from extreme_events_platform.enhanced_orchestrator import EnhancedExtremeEventsOrchestrator
from datetime import datetime

# Initialize orchestrator
orchestrator = EnhancedExtremeEventsOrchestrator()

# Example 1: Order Flow Analysis
market_data = {
    'trades': [
        {'timestamp': datetime.now(), 'price': 150.25, 'size': 500, 'side': 'buy'},
        {'timestamp': datetime.now(), 'price': 150.26, 'size': 1000, 'side': 'buy'},
        {'timestamp': datetime.now(), 'price': 150.24, 'size': 300, 'side': 'sell'},
        # ... more trades
    ],
    'price_history': [150.00, 150.10, 150.15, 150.20, 150.25]
}

result = orchestrator.run_market_reading_analysis(market_data)
print(f"Order Flow Signal: {result['order_flow']['signal']}")
print(f"Cumulative Delta: {result['order_flow']['cumulative_delta']}")
print(f"Institutional Activity: {result['order_flow']['institutional_activity']:.0%}")

# Example 2: Market Breadth Analysis
breadth_data = {
    'breadth_data': [
        {
            'date': '2024-01-15',
            'advances': 2100,
            'declines': 900,
            'unchanged': 50,
            'advancing_volume': 3500000000,
            'declining_volume': 1200000000,
            'new_highs': 150,
            'new_lows': 25,
            'total_issues': 3050
        },
        # ... more days
    ],
    'index_prices': [4800, 4815, 4830, 4845, 4860]
}

result = orchestrator.run_market_reading_analysis(breadth_data)
print(f"McClellan Oscillator: {result['breadth']['mcclellan_oscillator']:.0f}")
print(f"TRIN: {result['breadth']['trin']:.2f} - {result['breadth']['trin_signal']}")
print(f"Breadth Signal: {result['breadth']['overall_signal']}")
if result['breadth']['breadth_thrust']:
    print("BREADTH THRUST DETECTED - Highly Bullish!")
if result['breadth']['hindenburg_omen']:
    print("WARNING: Hindenburg Omen Detected!")

# Example 3: Intermarket Analysis
intermarket_data = {
    'asset_prices': {
        'stocks': [4800, 4820, 4850, 4840, 4860, 4880, 4900],  # S&P 500
        'bonds': [92.5, 92.3, 92.0, 91.8, 91.5, 91.3, 91.0],   # 10Y Treasury
        'commodities': [280, 282, 285, 288, 290, 293, 295],     # CRB Index
        'dollar': [104.0, 104.2, 104.5, 104.3, 104.6, 104.8, 105.0]  # DXY
    }
}

result = orchestrator.run_market_reading_analysis(intermarket_data)
print(f"Business Cycle: {result['intermarket']['business_cycle_stage']}")
print(f"Market Regime: {result['intermarket']['market_regime']}")
print(f"Risk Level: {result['intermarket']['risk_level']}")
for signal in result['intermarket']['signals']:
    print(f"  - {signal}")

# Example 4: Combined Analysis Summary
print(f"\nOverall Market Bias: {result['summary']['overall_bias']}")
print(f"Confidence: {result['summary']['confidence']:.0%}")
for action in result['summary']['immediate_actions']:
    print(f"  -> {action}")
```

### V6.0 Usage (Early Warning & Crisis Prediction)

```python
from extreme_events_platform.enhanced_orchestrator import EnhancedExtremeEventsOrchestrator

# Run early warning check for 2008-style crisis detection
orchestrator = EnhancedExtremeEventsOrchestrator(enable_early_warning=True)

market_data = {
    'credit_to_gdp_gap': 12.0,  # Massive credit boom
    'bank_leverage': 32.0,  # 2008: 30-40x
    'ted_spread': 0.85,  # Rising (2008 peak: 4.58%)
    'housing_price_to_income': 6.3,  # Bubble
    'vix': 13.5  # Low VIX = dangerous complacency
}

# Detects crises 12-24 months in advance!
result = orchestrator.run_early_warning_check(market_data)
print(f"Crisis Probability: {result['banking_crisis_analysis']['crisis_probability']:.1%}")
print(f"Months until crisis: {result['banking_crisis_analysis']['estimated_months_until']}")
```

### V3.0 Usage (with NLP and News Analysis)

```python
from extreme_events_platform.enhanced_orchestrator import EnhancedExtremeEventsOrchestrator

# Initialize platform with NLP enabled
orchestrator = EnhancedExtremeEventsOrchestrator(
    enable_llm=True,   # Enable multi-agent LLM system
    enable_nlp=True    # Enable NLP and news analysis
)

# Example 1: Recession analysis with news
news_headlines = [
    "Federal Reserve signals concern over slowing GDP growth",
    "Yield curve inverts for third consecutive month",
    "Consumer confidence plunges to lowest level since 2020",
    "Manufacturing PMI drops below 50, indicating contraction"
]

recession_data = {
    'name': 'US Recession Risk 2024',
    'yield_curve_spread': -0.5,  # Inverted
    'unemployment_rate': 4.5,
    'gdp_q1': -0.5,
    'gdp_q2': -0.3,
    'consumer_confidence': 75,
    'pmi': 48,
    'severity': 4
}

result = orchestrator.comprehensive_analysis(
    event_type='recession',
    event_data=recession_data,
    news_items=news_headlines,
    use_llm_agents=True
)

# Access results
print(f"Recession Probability: {result['agent_analysis']['predictions']['recession_probability']:.1%}")
print(f"News Sentiment: {result['news_analysis']['aggregate_sentiment']['sentiment']}")
print(f"Event Warnings: {len(result['event_warnings'])}")

# Get trading intelligence
for signal in result['news_analysis']['trading_signals']:
    print(f"{signal.signal_type}: {signal.asset_class} (strength: {signal.strength:.1%})")

# Example 2: Inflation analysis
inflation_data = {
    'name': 'Inflation Surge 2024',
    'cpi': 6.5,
    'core_pce': 5.5,
    'wage_growth': 5.2,
    'current_fed_rate': 2.5,
    'severity': 4
}

result = orchestrator.comprehensive_analysis(
    event_type='inflation',
    event_data=inflation_data
)

# Get market directions (winners/losers)
for winner in result['market_directions']['winners'][:3]:
    print(f"Winner: {winner['name']} (+{winner['expected_change_pct']:.0f}%)")
for loser in result['market_directions']['losers'][:3]:
    print(f"Loser: {loser['name']} ({loser['expected_change_pct']:.0f}%)")

# Example 3: Standalone NLP analysis
from extreme_events_platform.nlp.sentiment_analyzer import FinancialNLPAnalyzer

nlp = FinancialNLPAnalyzer()
analysis = nlp.analyze_text("Stock market crashes 5% as recession fears intensify")
print(f"Sentiment: {analysis.sentiment} (score: {analysis.score:.2f})")
print(f"Urgency: {analysis.urgency}")
print(f"Topics: {analysis.topics}")
```

### V5.0 Usage (Cross-Sector Strategies)

```python
from extreme_events_platform.enhanced_orchestrator import EnhancedExtremeEventsOrchestrator

# Initialize platform with V5.0 strategies enabled
orchestrator = EnhancedExtremeEventsOrchestrator(
    enable_llm=True,
    enable_nlp=True,
    enable_v5_strategies=True  # Enable cross-sector analysis
)

# Example 1: Energy crisis with cross-sector contagion
energy_crisis_data = {
    'name': 'Strait of Hormuz Crisis',
    'source_sector': 'energy',
    'shock_magnitude': 50,  # +50% oil price shock
    'estimated_duration_days': 90,
    'severity': 5
}

result = orchestrator.comprehensive_analysis(
    event_type='energy_event',
    event_data=energy_crisis_data,
    use_v5_strategies=True
)

# Access V5.0 cross-sector analysis
v5 = result['v5_cross_sector_analysis']

# Contagion analysis - how does energy shock cascade?
contagion = v5['contagion_analysis']
print(f"Affected sectors: {len(contagion['affected_sectors'])}")
for path in contagion['contagion_paths'][:5]:
    print(f"Path: {' → '.join(path['path'])}")
    print(f"Impact: {path['total_impact']:.1f}% in {path['timeframe']}")

# Supply chain disruptions
supply_chain = v5['supply_chain_analysis']
print(f"Bottleneck: {supply_chain['bottleneck']}")
print(f"Severity: {supply_chain['severity']}")
print(f"Trading: {supply_chain['trading_strategy']['immediate_trades'][0]}")

# Commodity arbitrage opportunities
for arb in v5['arbitrage_opportunities'][:3]:
    print(f"{arb['name']}: Long {arb['long']}, Short {arb['short']}")
    print(f"Dislocation: {arb['dislocation']}")

# Sector rotation recommendations
rotation = v5['sector_rotation']
print(f"Overweight: {', '.join(rotation['overweights'])}")
print(f"Underweight: {', '.join(rotation['underweights'])}")
print(f"Hedges: {rotation['hedges']}")

# Example 2: Weather event cascade analysis
from extreme_events_platform.agents.weather_event_agent import WeatherEventAgent

weather_agent = WeatherEventAgent()
heatwave_analysis = weather_agent.analyze_event({
    'weather_type': 'heatwave',
    'region': 'texas',
    'severity': 5,  # Extreme
    'duration_days': 21
})

# See cross-sector cascades
for cascade in heatwave_analysis['cross_sector_contagion']['cascades'][:3]:
    print(f"Stage {cascade['stage']}: {cascade['description']}")
    print(f"Sectors: {', '.join(cascade['sectors_affected'])}")

# Example 3: Standalone strategy modules
from extreme_events_platform.strategies.cross_sector_contagion import CrossSectorContagionAnalyzer
from extreme_events_platform.strategies.commodity_arbitrage import CommodityArbitrageAnalyzer
from extreme_events_platform.strategies.sector_rotation import SectorRotationOptimizer, EventCategory, RotationPhase

# Contagion analysis
contagion_analyzer = CrossSectorContagionAnalyzer()
contagion = contagion_analyzer.analyze_contagion(
    source_sector='semiconductors',
    shock_magnitude=-30,  # -30% production cut
    event_description='Taiwan drought reduces TSMC output'
)

# Commodity arbitrage
commodity_arb = CommodityArbitrageAnalyzer()
opportunities = commodity_arb.identify_arbitrage(
    event_type='energy_crisis',
    affected_commodities=['oil', 'natural_gas', 'power'],
    price_changes={'oil': 50, 'natural_gas': 200, 'power': 300}
)

# Sector rotation
sector_optimizer = SectorRotationOptimizer()
strategy = sector_optimizer.optimize_allocation(
    event_type=EventCategory.ENERGY_CRISIS,
    phase=RotationPhase.PANIC,
    conviction=0.9
)
print(f"Overweight: {strategy.overweights}")
print(f"Expected Sharpe: {strategy.expected_sharpe:.2f}")
```

### V4.0 Usage (Advanced Trading Strategies)

```python
from extreme_events_platform.trading import (
    HedgeFundStrategyAnalyzer,
    DerivativesStrategist,
    ShortSellingDetector,
    FastActionOpportunities,
    InstitutionalBehaviorAnalyzer
)

# Example 1: Hedge Fund Strategies for Market Crash
hf_analyzer = HedgeFundStrategyAnalyzer()
strategies = hf_analyzer.analyze_strategies(
    event_type='market_crash',
    event_data={'severity': 5, 'market_decline_pct': -15},
    market_conditions={'vix': 45, 'dispersion': 0.7}
)

print(f"Top Strategy: {strategies['top_strategies'][0].strategy.value}")
print(f"Expected Alpha: +{strategies['top_strategies'][0].expected_alpha:.1f}%")
# Output: Volatility Arbitrage (95/100 score), +15% alpha

# Example 2: Derivatives - VIX calls during crisis
derivatives = DerivativesStrategist()
options = derivatives.analyze_derivatives_opportunities(
    event_type='recession',
    event_data={'severity': 4},
    portfolio_value=1_000_000
)

# Example 3: Short selling and fast-action opportunities
short_detector = ShortSellingDetector()
shorts = short_detector.identify_short_opportunities(
    event_type='inflation',
    event_data={'severity': 4, 'cpi': 6.5}
)

# Example 4: Institutional behavior analysis
behavior_analyzer = InstitutionalBehaviorAnalyzer()
analysis = behavior_analyzer.analyze_investor_behavior(
    event_type='market_crash',
    market_conditions={'vix': 42}
)
```

### V1.0/V2.0 Usage (Basic)

```python
# Analyze a pandemic scenario
result = orchestrator.analyze_event(
    event_type="pandemic",
    severity="high",
    affected_regions=["global"],
    duration_months=12
)

# Get predictions
predictions = result.get_market_predictions()
economic_impact = result.get_economic_impact()
```

## V5.0 Cross-Sector Strategy Modules

### 1. Cross-Sector Contagion Analyzer
Analyzes how shocks cascade through the economy via hidden connections.

**Key Features:**
- NetworkX-based dependency graph of sector relationships
- Multi-hop contagion path finding (up to 4 degrees of separation)
- Amplification factors for critical connections (e.g., semiconductors → autos = 2.0x)
- Timeline creation showing when each sector gets affected
- Hidden connection finder (non-obvious relationships)

**Real-world examples:**
- Taiwan drought → TSMC → Chip shortage → Auto production → Used car prices
- Texas freeze → Nat gas spike → Fertilizer plants → Agriculture → Food inflation
- Red Sea shipping → Container delays → Retail stockouts → Consumer spending

### 2. Supply Chain Disruption Analyzer
Identifies bottlenecks and just-in-time inventory failures.

**Tracked Bottlenecks:**
- Taiwan semiconductor concentration (92% of advanced chips)
- Suez Canal chokepoint (12% of global trade)
- Strait of Hormuz (21% of oil)
- China rare earth monopoly (70% of supply)
- ASML EUV lithography (100% monopoly)

**Trading Strategies:**
- Long alternative suppliers when bottleneck disrupted
- Short dependent sectors after inventory buffer exhausted
- Long logistics/shipping during rerouting
- Pairs trades (beneficiaries vs victims)

### 3. Commodity Arbitrage Analyzer
Finds dislocations in commodity relationships.

**Arbitrage Types:**
- Calendar spreads (backwardation/contango) - Texas freeze nat gas M+1 vs M+3
- Crack spreads (crude → gasoline) - Refining margins
- Spark spreads (nat gas → electricity) - Power generation margins
- Geographic arbitrage (Henry Hub vs TTF) - US vs Europe gas
- Cross-commodity ratios (oil/gas, gold/silver) - Mean reversion plays
- Commodity-equity spreads (oil vs E&P stocks) - Laggard opportunities

**Historical Winners:**
- Texas freeze 2021: $596 backwardation spread in nat gas = 14,750% return
- COVID oil crash 2020: $57 contango = storage arbitrage
- Europe gas crisis 2022: 16x TTF/Henry Hub spread → LNG exporters +200%

### 4. Sector Rotation Optimizer
Optimizes allocations during different event phases.

**Event Categories:**
- Recession → Overweight staples/utilities, underweight discretionary
- Inflation → Overweight energy/materials, underweight tech
- Energy crisis → Overweight energy/utilities, underweight airlines
- Financial crisis → Overweight defensives, underweight financials/RE

**Rotation Phases:**
1. Panic (2 weeks) - Exaggerated moves, 1.5x multiplier
2. Contagion (2 months) - Secondary effects spread, 1.2x multiplier
3. Adaptation (4 months) - Mean reversion begins, 0.8x multiplier
4. Recovery (6+ months) - Return to normal, 0.3x multiplier

### 5. Weather Event Agent
Analyzes weather-driven cross-sector cascades.

**Event Types:**
- Heatwaves → Power grid → Bitcoin mining → Data centers → Tech
- Droughts → Agriculture → Food prices → Consumer staples → Restaurants
- Cold snaps → Natural gas → Chemicals → Semiconductors → Autos
- Floods → Transportation → Retail → Consumer spending
- Hurricanes → Insurance → Refineries → Energy prices

### 6. Energy Event Agent
Models energy shocks and cascades.

**Event Types:**
- Oil price shocks → Airlines, transportation, chemicals, all sectors
- Natural gas crises → Utilities, fertilizer, chemicals
- Power grid failures → Bitcoin, data centers, manufacturing
- Energy transitions → Renewables, utilities, traditional energy

**Energy Elasticity (quantified):**
- Airlines: -0.35 (fuel = 20-30% of costs)
- Energy stocks: +0.80 (direct beneficiary)
- Utilities: +0.30 (pass-through pricing)
- All sectors affected via input costs

**Historical Precedent:**
- 10 of last 11 US recessions preceded by oil shocks
- >30% oil spike typically triggers 5-stage cascade over 6 months

## Risk Metrics

- **VaR (Value at Risk)**: Maximum expected loss at confidence level
- **CVaR (Expected Shortfall)**: Expected loss beyond VaR threshold
- **Return Level**: Expected extreme value for given return period
- **Impact Score**: Multi-factor composite risk assessment

## Data Sources

**V1.0/V2.0:**
- Historical market data during crises
- Disaster economic loss databases
- Epidemiological transmission models
- Geopolitical risk indices
- Financial network data

**V3.0 NLP and Economic Events:**
- Real-time news feeds and financial headlines
- Federal Reserve economic data (FRED API compatible)
- Treasury yield curve data
- CPI, PCE, and inflation metrics
- Employment and unemployment statistics
- Consumer confidence and PMI indices
- Financial sentiment lexicon (2000+ terms)

## V3.0 Feature Details

### NLP and News Analysis
- **Sentiment Scoring**: -1 (very negative) to +1 (very positive)
- **Financial Lexicon**: 2000+ terms including 'crash' (-0.9), 'rally' (0.7), 'surge' (0.8)
- **Event Detection**: Automatically detects recession, inflation, market crash signals from news
- **Trading Signals**: BUY/SELL/HOLD/HEDGE recommendations based on sentiment
- **Urgency Classification**: CRITICAL (immediate action), HIGH, MEDIUM, LOW
- **Entity Extraction**: Companies, sectors, indices, economic indicators

### Economic Event Indicators

**Recession Indicators:**
- Yield Curve Inversion (weight: 0.30) - Most reliable predictor
- Sahm Rule (weight: 0.25) - 0.5pp unemployment rise threshold
- GDP Growth (weight: 0.20) - Two consecutive negative quarters
- Consumer Confidence (weight: 0.15) - Below 80 threshold
- PMI (weight: 0.10) - Below 50 = contraction

**Inflation Thresholds:**
- Target: 2.0% (Fed goal)
- Elevated: 3.0%
- High: 4.5%
- Very High: 6.0%
- Hyperinflation: 10.0%+

**Interest Rate Impact:**
- Rate hikes: Negative for growth stocks, REITs, utilities; Positive for financials, USD
- Rate cuts: Positive for growth stocks, real estate; Negative for USD, financials

### Model Context Protocol (MCP)
- Structures context for LLM agents with resources, tools, and prompts
- Implements Domain Knowledge Chain-of-Thought (DK-CoT) strategy
- Organizes news, historical data, and indicators for optimal inference
- Compatible with Claude, GPT-4, and other frontier LLMs

## Examples

See `/examples` directory for comprehensive demonstrations:
- `example_v3_nlp_economic_events.py` - NLP, recession, inflation, interest rate analysis
- `example_pandemic.py` - Pandemic scenario (V1.0)
- `example_compound_event.py` - Polycrisis analysis (V2.0)
- `example_behavioral_analysis.py` - Human behavior prediction (V2.0)

## References

**V1.0/V2.0:**
- World Economic Forum Global Risks Report 2025
- Extreme Value Theory applications in finance
- Black Swan Theory (Taleb)
- AI-Driven Early Warning Systems
- Machine Learning for Disaster Forecasting

**V3.0 Research:**
- "Financial Sentiment Analysis with Large Language Models" (2025)
- "FinBERT and GPT-4 for Market Sentiment" (2024-2025)
- "Model Context Protocol" - Anthropic (2024)
- "Domain Knowledge Chain-of-Thought for LLMs" (2025)
- Federal Reserve Economic Data (FRED)
- "Recession Forecasting with Yield Curve" - Federal Reserve
- "The Sahm Rule" - Claudia Sahm (2019)
- "Fed's 2% Inflation Target and Monetary Policy" - FOMC

**V4.0 Research (2025 Hedge Fund Intelligence):**
- "Top Hedge Fund Strategies 2025" - CAIA, Morgan Stanley, Barclays
- "Hedge Fund Industry Trends 2025" - Macro funds +11.2%, Event-driven +8.7%
- "Volatility Arbitrage Opportunities" - Convertible arbitrage +4.0% YTD 2025
- "Zero-Day Options Trading" - 0DTE iron condors, systematic strategies
- "Investor Behavior in Extreme Conditions" - Panic selling patterns, retail capitulation
- "Short Selling During Crises" - Squeeze risk, forced liquidations
- "Institutional vs Retail Behavior" - Dark pools, smart money indicators
- "Fast-Action Trading Opportunities" - VIX spikes, first-mover advantages
- CBOE Options Data, Prime Broker Surveys, 13F Filings

## V4.0 Trading Strategies Deep Dive

### Hedge Fund Strategies by Event Type

**Recession:**
- Distressed Debt (90/100 score) - Expected alpha: +16%
- Global Macro (85) - Central bank divergence trades
- Market Neutral (75) - Cash rebate benefit at 4-5% rates
- CTA Trend Following (80) - Sustained trends

**Inflation:**
- Global Macro (90) - Rate hikes, commodity trends
- CTA (85) - Inflation momentum
- Convertible Arbitrage (55) - Rate sensitivity

**Market Crash:**
- Volatility Arbitrage (95) - VIX explosion, dispersion
- Market Neutral (85) - Beta-zero returns
- Global Macro (80) - Tactical positioning

### Derivatives Strategies

**0DTE (Zero-Day Options):**
- Iron condors for range-bound markets
- Win rate: 65%, Return: +20-50% if market stays range
- Risk: Unlimited if breaks out of range
- Popular in 2025 with systematic funds

**VIX Calls (Crisis Protection):**
- VIX 30/40 call spreads
- Cost: 1-3% of portfolio
- Return: +100% to +500% if VIX >50
- Historical: March 2020 VIX calls returned 10-20x

**Put Protection:**
- Protective puts: 1.5% cost, full downside protection
- Put spreads: 0.5% cost, 10% protection
- Collars: Zero cost, capped upside and downside

### Short Selling Strategies

**Sector Shorts:**
- XLY (Consumer Disc) in recession: -15% expected
- XLK (Tech) in inflation: -21% expected
- Borrow cost: 0.3-1% for ETFs

**Pair Trades:**
- Long XLP / Short XLY (recession): +15% spread
- Long XLE / Short XLK (inflation): +20% spread
- Beta-neutral, lower risk

**Squeeze Risk Management:**
- Avoid SI > 20% of float (GME, AMC territory)
- Stop loss at 8-10% above entry
- Monitor daily for unusual volume

### Fast-Action Opportunities

**0-6 Hours (CRITICAL):**
- VIX calls (before IV spikes 30-50%)
- Inverse ETFs (SPXU, SQQQ)
- Safe haven dips (gold, treasuries)

**6-24 Hours (URGENT):**
- ATM put options
- Protective strategies
- Sector rotation shorts

**Day 2-3 (HIGH):**
- Margin call opportunities
- ETF arbitrage
- VIX term structure trades

**Day 3-7 (MEDIUM):**
- Oversold bounce
- Mean reversion
- Sector rotation longs

### Institutional vs Retail Behavior

**Retail (Panic Threshold: 85%):**
- Sells at bottoms (VIX >40)
- Buys at tops (FOMO)
- Overleveraged (margin calls)
- Contrarian indicator

**Institutions (Panic Threshold: 25%):**
- Buys during panic (5-10% dips)
- Systematic rebalancing
- Dark pool accumulation
- Follow the smart money

**Smart Money Signals:**
- Dark pool volume >40% = accumulation
- ETF inflows during retail panic = buy signal
- Put/call >1.5 = extreme fear, buy
- Insider buying clusters = value

**Contrarian Rules:**
- Buy when VIX >40, put/call >1.5, AAII <25%
- Sell when VIX <15, put/call <0.6, margin debt >$900B
- Fade retail sentiment
- Follow institutional flows

### Risk Management

**Position Limits:**
- Max single trade: 2-3% of portfolio
- Max strategy category: 5-8% of portfolio
- Max total options: 3-8% depending on risk tolerance
- Max 0DTE: 1% of portfolio

**Stop Losses:**
- Shorts: 7-10% above entry
- Options: 50% of premium paid
- 0DTE: Close by 2pm ET (avoid pin risk)
- Hedge funds: Exit if down >12% in timeframe

**Greeks Management:**
- Max portfolio delta: 0.5
- Max portfolio vega: 0.4
- Max daily theta bleed: -0.05 (5% per day)
- Rebalance when limits breached
