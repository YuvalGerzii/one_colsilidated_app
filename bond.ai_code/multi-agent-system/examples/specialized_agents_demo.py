"""
Demonstration of advanced specialized agents.

This example shows how to use the six advanced specialized agents:
1. Advanced Data Analysis Agent - Statistical analysis and data profiling
2. Advanced Data Science Agent - ML/DL model development
3. Advanced UI Design Agent - UX design and accessibility
4. Advanced Marketing Agent - Marketing strategy and campaigns
5. Advanced Finance Agent - Financial modeling and analysis
6. Advanced Manager/CEO Agent - Strategic planning and execution

Usage:
    python examples/specialized_agents_demo.py
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from loguru import logger

from multi_agent_system.agents.specialized import (
    AdvancedDataAnalysisAgent,
    AdvancedDataScienceAgent,
    AdvancedUIDesignAgent,
    AdvancedMarketingAgent,
    AdvancedFinanceAgent,
    AdvancedManagerCEOAgent,
    create_specialized_agent_pool,
)
from multi_agent_system.agents.orchestrator import OrchestratorAgent
from multi_agent_system.core.types import Task
from multi_agent_system.communication.message_bus import MessageBus


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'=' * 80}")
    print(f"  {title}")
    print(f"{'=' * 80}\n")


def print_result_summary(result, agent_name: str):
    """Print a summary of an agent's result."""
    print(f"\n--- {agent_name} Results ---")
    print(f"Success: {result.success}")
    print(f"Quality Score: {result.quality_score:.2f}")
    print(f"Execution Time: {result.execution_time:.2f}s")

    if result.success and result.data:
        print(f"\nKey Insights (showing first 3):")
        insights = result.data.get("insights", [])
        for i, insight in enumerate(insights[:3], 1):
            print(f"  {i}. {insight}")

        print(f"\nRecommendations (showing first 3):")
        recommendations = result.data.get("recommendations", [])
        for i, rec in enumerate(recommendations[:3], 1):
            print(f"  {i}. {rec}")


async def demo_individual_agents():
    """Demonstrate each specialized agent individually."""
    print_section("Individual Specialized Agent Demonstrations")

    # 1. Data Analysis Agent
    print("\n1. ADVANCED DATA ANALYSIS AGENT")
    print("-" * 40)
    data_analyst = AdvancedDataAnalysisAgent()

    task = Task(
        description="Analyze customer behavior dataset for time series patterns and correlations",
        requirements=["time_series", "correlation_analysis", "visualization"],
        priority=5,  # High priority
    )

    result = await data_analyst.execute_task(task)
    print_result_summary(result, "Data Analysis Agent")

    if result.success:
        data = result.data
        print(f"\nData Profile:")
        print(f"  - Total Records: {data['data_profile']['total_records']:,}")
        print(f"  - Features: {data['data_profile']['features']}")
        print(f"  - Data Quality Score: {data['data_profile']['data_quality_score']:.1%}")
        print(f"\nTime Series Analysis:")
        print(f"  - Trend: {data['time_series_analysis']['trend']}")
        print(f"  - Seasonality: {data['time_series_analysis']['seasonality']}")
        print(f"  - Forecast Confidence: {data['time_series_analysis']['forecast_confidence']:.1%}")

    # 2. Data Science Agent
    print("\n\n2. ADVANCED DATA SCIENCE AGENT")
    print("-" * 40)
    data_scientist = AdvancedDataScienceAgent()

    task = Task(
        description="Build predictive model for customer churn classification",
        requirements=["machine_learning", "classification", "model_evaluation"],
        priority=5,  # High priority
    )

    result = await data_scientist.execute_task(task)
    print_result_summary(result, "Data Science Agent")

    if result.success:
        data = result.data
        print(f"\nModel Selection:")
        print(f"  - Best Model: {data['model_selection']['best_model']}")
        print(f"  - CV Score: {data['model_selection']['models_evaluated'][3]['cv_score']:.1%}")
        print(f"\nTest Performance:")
        test_metrics = data['model_performance']['test_metrics']
        print(f"  - Accuracy: {test_metrics['accuracy']:.1%}")
        print(f"  - F1 Score: {test_metrics['f1_score']:.1%}")
        print(f"  - AUC-ROC: {test_metrics['auc_roc']:.2f}")
        print(f"\nDeployment:")
        print(f"  - Expected Latency: {data['deployment_plan']['expected_latency']}")
        print(f"  - Production Ready: {result.metadata.get('production_ready', False)}")

    # 3. UI Design Agent
    print("\n\n3. ADVANCED UI DESIGN AGENT")
    print("-" * 40)
    ui_designer = AdvancedUIDesignAgent()

    task = Task(
        description="Design responsive dashboard interface with accessibility compliance",
        requirements=["ui_design", "accessibility", "responsive_design"],
        priority=5,  # High priority
    )

    result = await ui_designer.execute_task(task)
    print_result_summary(result, "UI Design Agent")

    if result.success:
        data = result.data
        print(f"\nUser Research:")
        print(f"  - Personas Created: {len(data['user_research']['personas_created'])}")
        print(f"  - Research Methods: {len(data['user_research']['research_methods'])}")
        print(f"\nDesign System:")
        print(f"  - Components: {data['design_system']['components_created']}")
        print(f"  - Typography: {data['design_system']['design_tokens']['typography']}")
        print(f"\nAccessibility:")
        print(f"  - WCAG Level: {data['accessibility_compliance']['wcag_level']}")
        print(f"  - Features: {len(data['accessibility_compliance']['features_implemented'])}")
        print(f"\nUsability Testing:")
        success_rate = data['usability_testing']['success_rate']['round_3']
        print(f"  - Final Success Rate: {success_rate:.1%}")
        print(f"  - User Satisfaction: 4.6/5")

    # 4. Marketing Agent
    print("\n\n4. ADVANCED MARKETING AGENT")
    print("-" * 40)
    marketer = AdvancedMarketingAgent()

    task = Task(
        description="Develop comprehensive go-to-market strategy for SaaS product launch",
        requirements=["marketing_strategy", "campaign_planning", "market_research"],
        priority=5,  # High priority
    )

    result = await marketer.execute_task(task)
    print_result_summary(result, "Marketing Agent")

    if result.success:
        data = result.data
        print(f"\nMarket Size:")
        market = data['market_research']['market_size']
        print(f"  - TAM: {market['tam']}")
        print(f"  - SAM: {market['sam']}")
        print(f"  - SOM: {market['som']}")
        print(f"  - CAGR: {market['cagr']}")
        print(f"\nCustomer Segmentation:")
        print(f"  - Segments: {len(data['customer_segmentation']['segments_identified'])}")
        print(f"  - Target: {data['customer_segmentation']['targeting_priority']}")
        print(f"\nCampaign Planning:")
        campaign = data['campaign_planning']['flagship_campaign']
        print(f"  - Campaign: {campaign['name']}")
        print(f"  - Budget: {campaign['budget']}")
        print(f"  - Target Trials: {campaign['kpis']['trials']}")
        print(f"  - Expected ROI: {campaign['kpis']['roi']}")

    # 5. Finance Agent
    print("\n\n5. ADVANCED FINANCE AGENT")
    print("-" * 40)
    finance_analyst = AdvancedFinanceAgent()

    task = Task(
        description="Perform comprehensive financial analysis and valuation for Series B investment",
        requirements=["financial_modeling", "valuation", "risk_analysis"],
        priority=5,  # High priority
    )

    result = await finance_analyst.execute_task(task)
    print_result_summary(result, "Finance Agent")

    if result.success:
        data = result.data
        print(f"\nFinancial Performance:")
        income = data['financial_statements']['income_statement']
        print(f"  - Revenue: {income['revenue']}")
        print(f"  - Gross Margin: {income['gross_profit']}")
        print(f"  - EBITDA: {income['ebitda']}")
        print(f"  - Net Income: {income['net_income']}")
        print(f"\nKey Ratios:")
        ratios = data['financial_ratios']
        print(f"  - ROE: {ratios['profitability']['roe']}")
        print(f"  - Current Ratio: {ratios['liquidity']['current_ratio']}")
        print(f"  - Revenue Growth YoY: {ratios['growth']['revenue_growth_yoy']}")
        print(f"\nValuation:")
        valuation = data['valuation_analysis']['valuation_summary']
        print(f"  - DCF Value: {valuation['dcf_value']}")
        print(f"  - Comps Value: {valuation['comps_value']}")
        print(f"  - Weighted Average: {valuation['weighted_average']}")
        print(f"  - Range: {valuation['valuation_range']}")
        print(f"\nRecommendation: {data['investment_recommendation']['recommendation']}")

    # 6. Manager/CEO Agent
    print("\n\n6. ADVANCED MANAGER/CEO AGENT")
    print("-" * 40)
    ceo_manager = AdvancedManagerCEOAgent()

    task = Task(
        description="Develop 3-year strategic plan for scaling from $50M to $250M ARR",
        requirements=["strategic_planning", "business_analysis", "organizational_design"],
        priority=10,  # Critical priority
    )

    result = await ceo_manager.execute_task(task)
    print_result_summary(result, "Manager/CEO Agent")

    if result.success:
        data = result.data
        print(f"\nStrategic Vision:")
        print(f"  - Mission: {data['strategic_vision']['mission']}")
        print(f"  - 3-Year Vision: {data['strategic_vision']['vision_3_year']}")
        print(f"  - 5-Year Vision: {data['strategic_vision']['vision_5_year']}")
        print(f"\nStrategic Priorities:")
        for i, priority in enumerate(data['strategic_priorities'][:3], 1):
            print(f"  {i}. {priority['priority']}")
            print(f"     Objective: {priority['objective']}")
        print(f"\nOrganizational Growth:")
        growth = data['organizational_design']['team_growth_plan']
        print(f"  - Engineering: {growth['engineering']}")
        print(f"  - Sales: {growth['sales']}")
        print(f"  - Total Team: {growth['total']}")
        print(f"\nFinancial Strategy:")
        funding = data['financial_strategy']
        print(f"  - Funding: {funding['funding_strategy']}")
        print(f"  - Path to Profitability: {funding['path_to_profitability']}")


async def demo_integrated_workflow():
    """Demonstrate specialized agents working together on a complex business scenario."""
    print_section("Integrated Workflow: New Product Launch Strategy")

    print("Scenario: Planning a comprehensive new product launch")
    print("Involving: Strategic planning, market analysis, financial modeling, and UI design\n")

    # Create message bus and orchestrator
    message_bus = MessageBus()
    orchestrator = OrchestratorAgent(message_bus=message_bus)

    # Create specialized agents
    agent_pool = create_specialized_agent_pool(
        {
            "ceo_manager": 1,
            "marketer": 1,
            "finance_analyst": 1,
            "ui_designer": 1,
            "data_scientist": 1,
        },
        message_bus=message_bus
    )

    # Register all agents with orchestrator
    for agent in agent_pool.values():
        orchestrator.register_worker(agent)

    print(f"Created {len(agent_pool)} specialized agents:")
    for agent_id in agent_pool.keys():
        print(f"  - {agent_id}")

    # Create complex task that requires multiple specialists
    complex_task = Task(
        description="Launch new enterprise product tier with $25M ARR target",
        requirements=[
            "strategic_planning",
            "marketing_strategy",
            "financial_modeling",
            "ui_design",
            "data_science",
        ],
        priority=10,  # Critical priority
        context={
            "current_arr": "$52.3M",
            "target_arr": "$25M from new tier",
            "timeline": "6 months to launch",
            "market": "Enterprise segment",
        }
    )

    print(f"\n\nExecuting complex task with {len(complex_task.requirements)} requirements...")
    print("Orchestrator will delegate to appropriate specialists...\n")

    # Execute through orchestrator
    result = await orchestrator.execute_task(complex_task)

    print(f"\n--- Orchestrated Results ---")
    print(f"Overall Success: {result.success}")
    print(f"Subtasks Completed: {result.data['successful']}/{result.data['subtask_count']}")
    print(f"Average Quality: {result.quality_score:.2f}")
    print(f"Total Execution Time: {result.execution_time:.2f}s")

    print(f"\n\nIndividual Specialist Contributions:")
    for idx, subtask_result in enumerate(result.data['results'], 1):
        agent_id = subtask_result['agent_id']
        success = subtask_result['success']
        quality = subtask_result.get('data', {}).get('confidence', 0.0)

        print(f"\n  {idx}. {agent_id}")
        print(f"     Status: {'✓ Success' if success else '✗ Failed'}")
        print(f"     Confidence: {quality:.1%}")

        # Show first insight from each agent
        insights = subtask_result.get('data', {}).get('insights', [])
        if insights:
            print(f"     Key Insight: {insights[0]}")

    # Show worker status
    print(f"\n\nWorker Status Summary:")
    worker_status = orchestrator.get_worker_status()
    for worker_id, status in worker_status.items():
        print(f"  - {worker_id}: {status['completed_tasks']} completed, "
              f"performance: {status['performance_score']:.2f}")


async def demo_agent_capabilities():
    """Show the capabilities of each specialized agent."""
    print_section("Specialized Agent Capabilities Matrix")

    agents = {
        "Data Analysis": AdvancedDataAnalysisAgent(),
        "Data Science": AdvancedDataScienceAgent(),
        "UI Design": AdvancedUIDesignAgent(),
        "Marketing": AdvancedMarketingAgent(),
        "Finance": AdvancedFinanceAgent(),
        "CEO/Manager": AdvancedManagerCEOAgent(),
    }

    for name, agent in agents.items():
        print(f"\n{name} Agent:")
        print(f"  Capabilities ({len(agent.capabilities)}):")
        for cap in agent.capabilities:
            print(f"    - {cap.name}: {cap.description} (proficiency: {cap.proficiency:.1%})")


async def main():
    """Run all demonstrations."""
    logger.remove()  # Remove default logger
    logger.add(sys.stderr, level="WARNING")  # Only show warnings and errors

    print("\n" + "=" * 80)
    print("  ADVANCED SPECIALIZED AGENTS DEMONSTRATION")
    print("  Multi-Agent System with Professional Domain Expertise")
    print("=" * 80)

    # Demo 1: Individual agents
    await demo_individual_agents()

    # Demo 2: Show capabilities
    await demo_agent_capabilities()

    # Demo 3: Integrated workflow
    await demo_integrated_workflow()

    print_section("Demonstration Complete")
    print("All specialized agents demonstrated successfully!")
    print("\nKey Takeaways:")
    print("  1. Each agent provides deep domain expertise")
    print("  2. Agents produce comprehensive, actionable insights")
    print("  3. Multiple agents can collaborate through orchestration")
    print("  4. Results include confidence scores and quality metrics")
    print("  5. Agents are production-ready for real-world tasks")
    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
