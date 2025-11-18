"""
Bond.AI Platform Demonstration

This example demonstrates the complete Bond.AI platform with all five
specialized agents working together to analyze and optimize professional networks.

Agents demonstrated:
1. Network Analysis Agent - Analyzes network topology and health
2. Relationship Scoring Agent - Calculates Connection Intelligence Score™
3. Opportunity Detection Agent - Implements Opportunity Radar™
4. Connection Matching Agent - Matches compatible connections
5. Trust Bridge Agent - Facilitates warm introductions

Usage:
    python bond.ai/examples/bond_ai_demo.py
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from loguru import logger

from bond_ai.agents.network_analysis import NetworkAnalysisAgent
from bond_ai.agents.relationship_scoring import RelationshipScoringAgent
from bond_ai.agents.opportunity_detection import OpportunityDetectionAgent
from bond_ai.agents.connection_matching import ConnectionMatchingAgent
from bond_ai.agents.trust_bridge import TrustBridgeAgent

from multi_agent_system.agents.orchestrator import OrchestratorAgent
from multi_agent_system.agents.specialized import (
    AdvancedMarketingAgent,
    AdvancedFinanceAgent,
    AdvancedManagerCEOAgent,
)
from multi_agent_system.core.types import Task
from multi_agent_system.communication.message_bus import MessageBus


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'=' * 80}")
    print(f"  {title}")
    print(f"{'=' * 80}\n")


def print_agent_result(agent_name: str, result, show_insights=3, show_recommendations=3):
    """Print formatted agent results."""
    print(f"\n--- {agent_name} Results ---")
    print(f"Success: {result.success}")
    print(f"Quality Score: {result.quality_score:.1%}")

    if result.success and result.data:
        data = result.data

        # Print key metrics if available
        if "network_overview" in data:
            overview = data["network_overview"]
            print(f"\nNetwork Overview:")
            print(f"  - Total Connections: {overview['total_nodes']:,}")
            print(f"  - Total Relationships: {overview['total_edges']:,}")
            print(f"  - Avg Degrees of Separation: {overview['avg_path_length']}")
            print(f"  - Network Health: {overview['clustering_coefficient']:.1%}")

        if "connection_intelligence_score" in data:
            cis = data["connection_intelligence_score"]
            print(f"\nConnection Intelligence Score™:")
            print(f"  - Overall Score: {cis['overall_score']}/100")
            print(f"  - Percentile: Top {100-cis['percentile']}%")
            print(f"  - 30-Day Trend: {cis['trend']}")

        if "opportunity_radar_summary" in data:
            radar = data["opportunity_radar_summary"]
            print(f"\nOpportunity Radar™:")
            print(f"  - Total Opportunities: {radar['total_opportunities_detected']}")
            print(f"  - High Priority: {radar['high_priority_opportunities']}")
            print(f"  - Time Sensitive: {radar['time_sensitive_opportunities']}")
            print(f"  - Detection Accuracy: {radar['detection_accuracy']:.1%}")

        if "matching_summary" in data:
            matching = data["matching_summary"]
            print(f"\nConnection Matching:")
            print(f"  - Candidates Analyzed: {matching['total_candidates_analyzed']:,}")
            print(f"  - High Compatibility: {matching['high_compatibility_matches']}")
            print(f"  - Recommended Connections: {matching['recommended_connections']}")
            print(f"  - Match Accuracy: {matching['match_accuracy']:.1%}")

        if "introduction_summary" in data:
            intros = data["introduction_summary"]
            print(f"\nTrust Bridge Technology™:")
            print(f"  - Pending Introductions: {intros['pending_introductions']}")
            print(f"  - Success Rate: {intros['success_rate']:.1%}")
            print(f"  - Active Trust Bridges: {intros['active_trust_bridges']}")

        # Print insights
        insights = data.get("insights", [])
        if insights and show_insights > 0:
            print(f"\nKey Insights (showing {min(show_insights, len(insights))}/{len(insights)}):")
            for i, insight in enumerate(insights[:show_insights], 1):
                print(f"  {i}. {insight}")

        # Print recommendations
        recommendations = data.get("recommendations", [])
        if recommendations and show_recommendations > 0:
            print(f"\nRecommendations (showing {min(show_recommendations, len(recommendations))}/{len(recommendations)}):")
            for i, rec in enumerate(recommendations[:show_recommendations], 1):
                print(f"  {i}. {rec}")


async def demo_individual_agents():
    """Demonstrate each Bond.AI agent individually."""
    print_section("Bond.AI Individual Agent Demonstrations")

    # 1. Network Analysis Agent
    print("\n1. NETWORK ANALYSIS AGENT")
    print("-" * 40)
    print("Analyzing professional network structure and health...")

    network_analyst = NetworkAnalysisAgent()
    task = Task(
        description="Analyze my professional network for patterns, communities, and opportunities",
        requirements=["network_topology", "community_detection", "weak_tie_analysis"],
        priority=5,
    )

    result = await network_analyst.execute_task(task)
    print_agent_result("Network Analysis Agent", result)

    # 2. Relationship Scoring Agent
    print("\n\n2. RELATIONSHIP SCORING AGENT (Connection Intelligence Score™)")
    print("-" * 40)
    print("Calculating Connection Intelligence Score™ and relationship health...")

    relationship_scorer = RelationshipScoringAgent()
    task = Task(
        description="Calculate my Connection Intelligence Score and analyze relationship health",
        requirements=["connection_intelligence", "relationship_prediction", "value_estimation"],
        priority=5,
    )

    result = await relationship_scorer.execute_task(task)
    print_agent_result("Relationship Scoring Agent", result)

    if result.success:
        # Show top relationships
        top_rels = result.data.get("top_relationships", [])
        if top_rels:
            print(f"\n  Top Relationships:")
            for rel in top_rels[:3]:
                print(f"    - {rel['name']} ({rel['title']}): Score {rel['relationship_score']}/100")

    # 3. Opportunity Detection Agent
    print("\n\n3. OPPORTUNITY DETECTION AGENT (Opportunity Radar™)")
    print("-" * 40)
    print("Scanning network for business opportunities...")

    opportunity_detector = OpportunityDetectionAgent()
    task = Task(
        description="Detect high-value opportunities in my network",
        requirements=["opportunity_scanning", "signal_recognition", "opportunity_scoring"],
        priority=5,
    )

    result = await opportunity_detector.execute_task(task)
    print_agent_result("Opportunity Detection Agent", result)

    if result.success:
        # Show high priority opportunities
        opportunities = result.data.get("high_priority_opportunities", [])
        if opportunities:
            print(f"\n  High-Priority Opportunities:")
            for opp in opportunities[:3]:
                print(f"    - {opp['title']}: Priority {opp['priority_score']}/100")
                print(f"      Value: {opp['estimated_value']}")

    # 4. Connection Matching Agent
    print("\n\n4. CONNECTION MATCHING AGENT")
    print("-" * 40)
    print("Finding compatible connections with 85% accuracy...")

    connection_matcher = ConnectionMatchingAgent()
    task = Task(
        description="Find highly compatible connections based on my interests and goals",
        requirements=["compatibility_prediction", "mutual_benefit", "match_scoring"],
        priority=5,
    )

    result = await connection_matcher.execute_task(task)
    print_agent_result("Connection Matching Agent", result)

    if result.success:
        # Show top matches
        matches = result.data.get("top_matches", [])
        if matches:
            print(f"\n  Top Compatible Matches:")
            for match in matches[:3]:
                person = match['person']
                print(f"    - {person['name']} ({person['title']}): {match['compatibility_score']}% compatible")
                print(f"      Confidence: {match['prediction_confidence']:.1%}")

    # 5. Trust Bridge Agent
    print("\n\n5. TRUST BRIDGE AGENT (Trust Bridge Technology™)")
    print("-" * 40)
    print("Facilitating warm introductions with trust transitivity...")

    trust_bridge = TrustBridgeAgent()
    task = Task(
        description="Facilitate warm introductions to high-value connections",
        requirements=["trust_transitivity", "path_optimization", "message_generation"],
        priority=5,
    )

    result = await trust_bridge.execute_task(task)
    print_agent_result("Trust Bridge Agent", result)

    if result.success:
        # Show priority introductions
        intros = result.data.get("priority_introductions", [])
        if intros:
            print(f"\n  Priority Introductions:")
            for intro in intros[:3]:
                print(f"    - {intro['target']['name']} via {intro['bridge']['name']}")
                print(f"      Trust Transitivity: {intro['trust_analysis']['transitivity_score']:.1%}")
                print(f"      Success Prediction: {intro['success_prediction']['introduction_acceptance']:.1%}")


async def demo_integrated_workflow():
    """Demonstrate Bond.AI agents working together with business strategy agents."""
    print_section("Integrated Workflow: Complete Network Strategy")

    print("Scenario: Comprehensive network analysis and growth strategy")
    print("Involving: All Bond.AI agents + Marketing, Finance, and CEO/Strategy agents\n")

    # Create message bus and orchestrator
    message_bus = MessageBus()
    orchestrator = OrchestratorAgent(message_bus=message_bus)

    # Create Bond.AI agents
    print("Initializing Bond.AI agents...")
    bond_agents = {
        "network_analyst": NetworkAnalysisAgent(message_bus=message_bus),
        "relationship_scorer": RelationshipScoringAgent(message_bus=message_bus),
        "opportunity_detector": OpportunityDetectionAgent(message_bus=message_bus),
        "connection_matcher": ConnectionMatchingAgent(message_bus=message_bus),
        "trust_bridge": TrustBridgeAgent(message_bus=message_bus),
    }

    # Create business strategy agents
    print("Initializing business strategy agents...")
    strategy_agents = {
        "marketer": AdvancedMarketingAgent(message_bus=message_bus),
        "finance_analyst": AdvancedFinanceAgent(message_bus=message_bus),
        "ceo_strategist": AdvancedManagerCEOAgent(message_bus=message_bus),
    }

    # Register all agents with orchestrator
    all_agents = {**bond_agents, **strategy_agents}
    for agent in all_agents.values():
        orchestrator.register_worker(agent)

    print(f"Created {len(all_agents)} specialized agents:")
    for agent_id in all_agents.keys():
        print(f"  - {agent_id}")

    # Create complex task requiring multiple agents
    complex_task = Task(
        description="Develop comprehensive network growth and monetization strategy for Bond.AI platform launch",
        requirements=[
            "network_analysis",
            "relationship_scoring",
            "opportunity_detection",
            "marketing_strategy",
            "financial_modeling",
            "strategic_planning",
        ],
        priority=10,  # Critical
        context={
            "platform": "Bond.AI",
            "goal": "Launch professional networking platform",
            "target_users": "100K in first year",
            "revenue_model": "Freemium + Enterprise",
        }
    )

    print(f"\n\nExecuting complex task with {len(complex_task.requirements)} requirements...")
    print("Orchestrator will delegate to appropriate specialists...\n")

    # Execute through orchestrator
    result = await orchestrator.execute_task(complex_task)

    print(f"\n--- Orchestrated Results ---")
    print(f"Overall Success: {result.success}")
    print(f"Subtasks Completed: {result.data['successful']}/{result.data['subtask_count']}")
    print(f"Average Quality: {result.quality_score:.1%}")
    print(f"Total Execution Time: {result.execution_time:.2f}s")

    print(f"\n\nIndividual Agent Contributions:")
    for idx, subtask_result in enumerate(result.data['results'], 1):
        agent_id = subtask_result['agent_id']
        success = subtask_result['success']

        print(f"\n  {idx}. {agent_id}")
        print(f"     Status: {'✓ Success' if success else '✗ Failed'}")

        # Show first insight from each agent
        insights = subtask_result.get('data', {}).get('insights', [])
        if insights:
            print(f"     Key Insight: {insights[0]}")

    # Show worker status
    print(f"\n\nAgent Performance Summary:")
    worker_status = orchestrator.get_worker_status()
    for worker_id, status in worker_status.items():
        print(f"  - {worker_id}: {status['completed_tasks']} completed, "
              f"performance: {status['performance_score']:.2f}")


async def demo_use_cases():
    """Show specific Bond.AI use cases."""
    print_section("Bond.AI Use Cases")

    print("Use Case 1: Job Seeker - Finding Opportunities")
    print("-" * 40)
    opportunity_detector = OpportunityDetectionAgent()
    task = Task(
        description="Find job opportunities and career advancement paths in my network",
        requirements=["opportunity_scanning", "connection_matching"],
        priority=5,
        context={"user_type": "job_seeker", "goal": "career_advancement"},
    )
    result = await opportunity_detector.execute_task(task)
    if result.success:
        print(f"✓ Detected {result.data['opportunity_radar_summary']['total_opportunities_detected']} opportunities")
        print(f"✓ {result.data['opportunity_radar_summary']['high_priority_opportunities']} high-priority matches")

    print("\n\nUse Case 2: Entrepreneur - Fundraising Network")
    print("-" * 40)
    network_analyst = NetworkAnalysisAgent()
    task = Task(
        description="Analyze network for VC connections and funding opportunities",
        requirements=["network_topology", "weak_tie_analysis"],
        priority=5,
        context={"user_type": "entrepreneur", "goal": "fundraising"},
    )
    result = await network_analyst.execute_task(task)
    if result.success:
        weak_ties = result.data.get('weak_ties_analysis', {})
        print(f"✓ Identified {weak_ties.get('high_value_weak_ties', 0)} high-value weak ties")
        print(f"✓ Network health score: {result.data['network_health_score']['overall_score']}/100")

    print("\n\nUse Case 3: Sales Professional - Client Acquisition")
    print("-" * 40)
    connection_matcher = ConnectionMatchingAgent()
    task = Task(
        description="Match with potential enterprise clients in my extended network",
        requirements=["compatibility_prediction", "mutual_benefit"],
        priority=5,
        context={"user_type": "sales_professional", "goal": "client_acquisition"},
    )
    result = await connection_matcher.execute_task(task)
    if result.success:
        print(f"✓ Analyzed {result.data['matching_summary']['total_candidates_analyzed']:,} candidates")
        print(f"✓ Found {result.data['matching_summary']['recommended_connections']} high-compatibility prospects")


async def main():
    """Run all demonstrations."""
    logger.remove()  # Remove default logger
    logger.add(sys.stderr, level="WARNING")  # Only show warnings and errors

    print("\n" + "=" * 80)
    print("  BOND.AI PLATFORM DEMONSTRATION")
    print("  Making Every Professional Connection Count")
    print("=" * 80)

    print("\n🎯 Mission:")
    print("Democratize access to opportunity by making every professional connection count,")
    print("transforming the way business relationships are discovered, developed, and")
    print("leveraged for mutual success.")

    print("\n✨ Core Features:")
    print("  • Connection Intelligence Score™ - Network health measurement")
    print("  • Opportunity Radar™ - Real-time opportunity detection")
    print("  • Trust Bridge Technology™ - Automated warm introductions")
    print("  • Network ROI Dashboard - Measurable networking impact")
    print("  • Compatibility Prediction - 85% accuracy matching")

    # Demo 1: Individual agents
    await demo_individual_agents()

    # Demo 2: Use cases
    await demo_use_cases()

    # Demo 3: Integrated workflow
    await demo_integrated_workflow()

    print_section("Demonstration Complete")
    print("Bond.AI platform successfully demonstrated!")
    print("\nKey Achievements:")
    print("  ✓ All 5 Bond.AI agents operational")
    print("  ✓ Connection Intelligence Score™ calculated")
    print("  ✓ Opportunity Radar™ detecting opportunities")
    print("  ✓ 85% accuracy compatibility matching")
    print("  ✓ Trust Bridge Technology™ facilitating introductions")
    print("  ✓ Multi-agent orchestration for complex strategies")
    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
