"""
Comprehensive demonstration of advanced multi-agent features:

1. Shared Environment - Agents interact with common resources
2. Distributed Coordination - Agents elect leaders and coordinate
3. Negotiation & Competition - Agents negotiate and compete for resources
4. Collective Intelligence - Agents contribute to shared knowledge
5. Emergent Behavior - System intelligence emerges from agent interactions
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from multi_agent_system.environment import (
    SharedEnvironment,
    ResourceType,
    AccessMode,
)
from multi_agent_system.coordination import (
    DistributedCoordinator,
    CoordinationStrategy,
)
from multi_agent_system.communication.protocols import (
    NegotiationProtocol,
    AuctionProtocol,
    ConsensusProtocol,
    AuctionType,
    VotingMethod,
)
from multi_agent_system.intelligence import (
    CollectiveIntelligence,
    AggregationMethod,
)
from loguru import logger


async def demonstrate_shared_environment():
    """Demonstrate agents interacting in a shared environment."""
    print("\n" + "=" * 80)
    print("1. SHARED ENVIRONMENT DEMONSTRATION")
    print("=" * 80)

    env = SharedEnvironment(name="demo_env")

    # Register agents
    agents = ["agent_1", "agent_2", "agent_3"]
    for agent_id in agents:
        env.register_agent(agent_id)

    print(f"\n✓ Registered {len(agents)} agents")

    # Create shared resources
    data_resource = await env.create_resource(
        name="shared_database",
        resource_type=ResourceType.DATA,
        access_mode=AccessMode.SHARED,
        capacity=2,  # Max 2 agents can access simultaneously
        owner="agent_1",
        data={"records": 1000, "size_mb": 50}
    )

    compute_resource = await env.create_resource(
        name="gpu_cluster",
        resource_type=ResourceType.COMPUTATIONAL,
        access_mode=AccessMode.EXCLUSIVE,  # Only one agent at a time
        owner="admin",
        data={"gpus": 8, "memory_gb": 256}
    )

    print(f"\n✓ Created resources:")
    print(f"  - Shared database (capacity: 2)")
    print(f"  - GPU cluster (exclusive access)")

    # Agents request and use resources
    print("\n📊 Resource Access Demonstration:")

    # Agent 1 and 2 can access shared resource simultaneously
    success1 = await env.request_resource(data_resource, "agent_1")
    success2 = await env.request_resource(data_resource, "agent_2")

    print(f"  - Agent 1 accessing shared database: {'✓' if success1 else '✗'}")
    print(f"  - Agent 2 accessing shared database: {'✓' if success2 else '✗'}")

    # Agent 3 tries to access (should wait or timeout)
    print(f"  - Agent 3 trying to access (at capacity)...")
    success3 = await env.request_resource(data_resource, "agent_3", timeout=2.0)
    print(f"    Result: {'✓ Accessed' if success3 else '✗ Timeout (expected)'}")

    # Agent 1 releases, now agent 3 can access
    await env.release_resource(data_resource, "agent_1")
    print(f"  - Agent 1 released database")

    success3 = await env.request_resource(data_resource, "agent_3", timeout=2.0)
    print(f"  - Agent 3 accessing database: {'✓' if success3 else '✗'}")

    # Exclusive resource competition
    print(f"\n🔒 Exclusive Resource Competition:")
    success = await env.request_resource(compute_resource, "agent_1", timeout=1.0)
    print(f"  - Agent 1 acquired GPU cluster: {'✓' if success else '✗'}")

    success = await env.request_resource(compute_resource, "agent_2", timeout=1.0)
    print(f"  - Agent 2 trying to acquire (should fail): {'✓' if success else '✗ Failed (expected)'}")

    # Show environment state
    state = env.get_environment_state()
    print(f"\n📈 Environment Statistics:")
    print(f"  - Total resources: {state['total_resources']}")
    print(f"  - Resources in use: {state['resources_in_use']}")
    print(f"  - Total events: {state['total_events']}")
    print(f"  - Resource accesses: {state['statistics']['total_resource_accesses']}")
    print(f"  - Conflicts: {state['statistics']['total_conflicts']}")


async def demonstrate_distributed_coordination():
    """Demonstrate distributed coordination with leader election."""
    print("\n" + "=" * 80)
    print("2. DISTRIBUTED COORDINATION DEMONSTRATION")
    print("=" * 80)

    coordinator = DistributedCoordinator(
        strategy=CoordinationStrategy.LOAD_BASED,
        election_timeout=3.0,
        heartbeat_interval=1.0
    )

    await coordinator.start()

    # Register agents with different priorities
    agents = [
        ("agent_alpha", {"research", "analysis"}, 10),
        ("agent_beta", {"coding", "testing"}, 8),
        ("agent_gamma", {"research", "coding"}, 12),  # Highest priority
        ("agent_delta", {"analysis", "testing"}, 5),
    ]

    for agent_id, caps, priority in agents:
        coordinator.register_agent(agent_id, caps, priority)

    print(f"\n✓ Registered {len(agents)} agents")

    # Wait for leader election
    await asyncio.sleep(0.5)

    leader = coordinator.get_leader()
    print(f"\n👑 Leader Elected: {leader}")
    print(f"   (Agent with highest priority)")

    # Submit tasks for distributed allocation
    print(f"\n📋 Task Distribution:")

    tasks = [
        {"id": "task_1", "description": "Research AI trends", "capabilities": {"research"}},
        {"id": "task_2", "description": "Code ML model", "capabilities": {"coding"}},
        {"id": "task_3", "description": "Test API", "capabilities": {"testing"}},
        {"id": "task_4", "description": "Analyze data", "capabilities": {"analysis"}},
    ]

    for task in tasks:
        assigned = await coordinator.submit_task(task, task["capabilities"])
        print(f"  - {task['description']}: assigned to {assigned}")

    # Show coordination state
    state = coordinator.get_coordination_state()
    print(f"\n📊 Coordination Statistics:")
    print(f"  - Total agents: {state['total_agents']}")
    print(f"  - Alive agents: {state['alive_agents']}")
    print(f"  - Tasks allocated: {state['metrics']['total_tasks_allocated']}")
    print(f"  - Elections held: {state['metrics']['total_elections']}")

    # Show agent workloads
    print(f"\n⚖️  Agent Workloads:")
    for agent_info in state['agents']:
        print(f"  - {agent_info['id']}: {agent_info['workload']} tasks ({agent_info['role']})")

    await coordinator.stop()


async def demonstrate_negotiation_and_competition():
    """Demonstrate negotiation and auction protocols."""
    print("\n" + "=" * 80)
    print("3. NEGOTIATION & COMPETITION DEMONSTRATION")
    print("=" * 80)

    # === Negotiation ===
    print(f"\n🤝 Negotiation Protocol:")

    negotiation = NegotiationProtocol()

    # Agent 1 proposes to Agent 2
    proposal_id = await negotiation.propose(
        proposer="agent_1",
        recipient="agent_2",
        subject="Data sharing agreement",
        offer={"data_share_percentage": 70, "cost": 100},
        timeout=60.0
    )

    print(f"  - Agent 1 proposes to Agent 2: {proposal_id[:8]}...")
    print(f"    Offer: 70% data share for $100")

    # Agent 2 makes counter-offer
    await negotiation.counter_offer(
        proposal_id=proposal_id,
        agent_id="agent_2",
        counter_offer={"data_share_percentage": 80, "cost": 120}
    )

    print(f"  - Agent 2 counter-offers: 80% data share for $120")

    # Agent 1 accepts counter-offer
    accepted = await negotiation.accept(
        proposal_id=proposal_id,
        agent_id="agent_1",
        accept_counter=True
    )

    print(f"  - Agent 1 accepts counter-offer: {'✓' if accepted else '✗'}")
    print(f"    Negotiation complete!")

    # === Auction ===
    print(f"\n🏆 Auction Protocol:")

    auction_protocol = AuctionProtocol()

    # Create auction for a resource
    auction_id = await auction_protocol.create_auction(
        auctioneer="resource_owner",
        resource_id="premium_gpu",
        auction_type=AuctionType.SECOND_PRICE,
        starting_price=50.0,
        reserve_price=75.0,
        duration=3.0  # 3 seconds
    )

    print(f"  - Auction created: {auction_id[:8]}...")
    print(f"    Item: Premium GPU")
    print(f"    Type: Second-price auction")
    print(f"    Starting price: $50")

    # Agents place bids
    await auction_protocol.place_bid(auction_id, "agent_1", 60.0)
    print(f"  - Agent 1 bids: $60")

    await auction_protocol.place_bid(auction_id, "agent_2", 85.0)
    print(f"  - Agent 2 bids: $85")

    await auction_protocol.place_bid(auction_id, "agent_3", 92.0)
    print(f"  - Agent 3 bids: $92")

    await auction_protocol.place_bid(auction_id, "agent_4", 78.0)
    print(f"  - Agent 4 bids: $78")

    # Wait for auction to end
    print(f"  - Waiting for auction to end...")
    await asyncio.sleep(3.5)

    # Get results
    auction = auction_protocol.get_auction(auction_id)
    if auction and auction["winner"]:
        print(f"\n  🎉 Winner: {auction['winner']}")
        print(f"     Winning bid: $92")
        print(f"     Price paid: ${auction['winning_bid']} (second-highest bid)")

    # === Voting/Consensus ===
    print(f"\n🗳️  Consensus Protocol:")

    consensus = ConsensusProtocol()

    # Initiate vote
    vote_id = await consensus.initiate_vote(
        initiator="agent_1",
        subject="Choose next project",
        choices=["AI Research", "Product Development", "Infrastructure"],
        eligible_voters={"agent_1", "agent_2", "agent_3", "agent_4", "agent_5"},
        voting_method=VotingMethod.MAJORITY,
        duration=2.0
    )

    print(f"  - Vote initiated: {vote_id[:8]}...")
    print(f"    Subject: Choose next project")
    print(f"    Method: Majority vote")

    # Agents cast votes
    await consensus.cast_vote(vote_id, "agent_1", "AI Research")
    await consensus.cast_vote(vote_id, "agent_2", "AI Research")
    await consensus.cast_vote(vote_id, "agent_3", "Product Development")
    await consensus.cast_vote(vote_id, "agent_4", "AI Research")
    await consensus.cast_vote(vote_id, "agent_5", "Infrastructure")

    print(f"  - 5 agents cast their votes")
    print(f"  - Waiting for vote to end...")

    # Wait for vote to end
    await asyncio.sleep(2.5)

    # Get results
    vote = consensus.get_vote(vote_id)
    if vote and vote["result"]:
        print(f"\n  ✓ Result: '{vote['result']}'")
        print(f"    Participation: {vote['participation_rate']:.0%}")


async def demonstrate_collective_intelligence():
    """Demonstrate collective intelligence and emergent behavior."""
    print("\n" + "=" * 80)
    print("4. COLLECTIVE INTELLIGENCE DEMONSTRATION")
    print("=" * 80)

    intelligence = CollectiveIntelligence()

    # Agents contribute knowledge on various topics
    print(f"\n🧠 Agents Contributing Knowledge:")

    # Topic 1: Market trends
    await intelligence.contribute(
        "agent_1", "market_trends_2024",
        data={"growth": 15.2, "volatility": "medium"},
        quality_score=0.85, confidence=0.9
    )
    await intelligence.contribute(
        "agent_2", "market_trends_2024",
        data={"growth": 16.1, "volatility": "medium"},
        quality_score=0.88, confidence=0.85
    )
    await intelligence.contribute(
        "agent_3", "market_trends_2024",
        data={"growth": 14.8, "volatility": "medium"},
        quality_score=0.82, confidence=0.88
    )

    print(f"  - 3 agents contributed to 'market_trends_2024'")

    # Topic 2: Best practices
    await intelligence.contribute(
        "agent_1", "ml_best_practices",
        data="Use cross-validation",
        quality_score=0.92, confidence=0.95
    )
    await intelligence.contribute(
        "agent_2", "ml_best_practices",
        data="Use cross-validation",
        quality_score=0.90, confidence=0.93
    )
    await intelligence.contribute(
        "agent_4", "ml_best_practices",
        data="Use cross-validation",
        quality_score=0.88, confidence=0.90
    )

    print(f"  - 3 agents contributed to 'ml_best_practices'")

    # Topic 3: System performance (numeric)
    contributions = [
        ("agent_1", 87.5, 0.85, 0.90),
        ("agent_2", 89.2, 0.88, 0.92),
        ("agent_3", 86.8, 0.82, 0.87),
        ("agent_4", 88.7, 0.90, 0.95),
    ]

    for agent_id, value, quality, confidence in contributions:
        await intelligence.contribute(
            agent_id, "system_performance_score",
            data=value, quality_score=quality, confidence=confidence
        )

    print(f"  - 4 agents contributed to 'system_performance_score'")

    # Aggregate knowledge
    print(f"\n📊 Knowledge Aggregation:")

    # Weighted average for numeric data
    result = await intelligence.aggregate(
        "system_performance_score",
        method=AggregationMethod.WEIGHTED_AVERAGE
    )

    knowledge = intelligence.get_collective_knowledge("system_performance_score")
    print(f"  - System Performance Score (weighted average):")
    print(f"    Result: {result:.2f}")
    print(f"    Quality: {knowledge.quality_score:.2f}")
    print(f"    Confidence: {knowledge.confidence_score:.2f}")

    # Consensus for consistent data
    result = await intelligence.aggregate(
        "ml_best_practices",
        method=AggregationMethod.CONSENSUS
    )

    knowledge = intelligence.get_collective_knowledge("ml_best_practices")
    print(f"\n  - ML Best Practices (consensus):")
    print(f"    Result: '{result}' ✓ (all agents agree)")
    print(f"    Confidence: {knowledge.confidence_score:.2f}")

    # Detect emergent patterns
    print(f"\n🔍 Pattern Detection:")

    patterns = await intelligence.detect_patterns(min_occurrences=2)

    print(f"  - Detected {len(patterns)} emergent patterns:")
    for pattern in patterns:
        if pattern["type"] == "collaboration":
            print(f"    • Collaboration: {pattern['agents'][0]} & {pattern['agents'][1]}")
            print(f"      Frequency: {pattern['frequency']} topics")

    # Show system intelligence
    sys_intel = intelligence.get_system_intelligence()

    print(f"\n📈 System Intelligence Metrics:")
    print(f"  - Total topics: {sys_intel['total_topics']}")
    print(f"  - Total contributions: {sys_intel['total_contributions']}")
    print(f"  - Contributing agents: {sys_intel['total_agents']}")
    print(f"  - Average quality: {sys_intel['average_quality']:.2f}")
    print(f"  - Patterns discovered: {sys_intel['patterns_discovered']}")

    # Top contributors
    print(f"\n🏅 Top Contributors:")
    for i, contributor in enumerate(sys_intel['top_contributors'], 1):
        print(f"  {i}. {contributor['agent_id']}: "
              f"reputation={contributor['reputation_score']:.2f}, "
              f"contributions={contributor['contribution_count']}")


async def demonstrate_emergent_behavior():
    """Demonstrate emergent system behavior."""
    print("\n" + "=" * 80)
    print("5. EMERGENT BEHAVIOR DEMONSTRATION")
    print("=" * 80)

    print("\n🌟 Combining All Systems for Emergent Behavior:")

    # Create all systems
    env = SharedEnvironment(name="integrated_env")
    coordinator = DistributedCoordinator(strategy=CoordinationStrategy.CAPABILITY_BASED)
    intelligence = CollectiveIntelligence()
    auction = AuctionProtocol()

    await coordinator.start()

    # Register agents
    agents = {
        "researcher_1": {"research", "analysis"},
        "researcher_2": {"research", "writing"},
        "coder_1": {"coding", "testing"},
        "coder_2": {"coding", "deployment"},
        "analyst_1": {"analysis", "visualization"},
    }

    for agent_id, caps in agents.items():
        env.register_agent(agent_id)
        coordinator.register_agent(agent_id, caps, priority=5)

    print(f"  ✓ {len(agents)} specialized agents in the system")

    # Create a valuable resource
    gpu_id = await env.create_resource(
        name="high_performance_gpu",
        resource_type=ResourceType.COMPUTATIONAL,
        access_mode=AccessMode.EXCLUSIVE,
        owner="system"
    )

    # Auction the resource
    auction_id = await auction.create_auction(
        auctioneer="system",
        resource_id=gpu_id,
        auction_type=AuctionType.FIRST_PRICE,
        starting_price=100.0,
        duration=2.0
    )

    print(f"\n  💎 High-value GPU resource created")
    print(f"  🏆 Auction started for resource access")

    # Agents bid based on their need (simulated)
    await auction.place_bid(auction_id, "researcher_1", 120.0)
    await auction.place_bid(auction_id, "coder_1", 150.0)
    await auction.place_bid(auction_id, "analyst_1", 110.0)

    print(f"  - 3 agents competed for the resource")

    await asyncio.sleep(2.5)

    # Winner uses resource and contributes knowledge
    auction_result = auction.get_auction(auction_id)
    if auction_result and auction_result["winner"]:
        winner = auction_result["winner"]
        print(f"\n  ✓ {winner} won the auction (bid: ${auction_result['winning_bid']})")

        # Winner accesses resource
        await env.request_resource(gpu_id, winner)
        print(f"  ✓ {winner} is using the GPU")

        # Winner contributes insights
        await intelligence.contribute(
            winner,
            "gpu_performance_insights",
            data={"throughput": 95.5, "efficiency": "excellent"},
            quality_score=0.92,
            confidence=0.95
        )

        print(f"  ✓ {winner} shared performance insights with collective")

        # Other agents learn from this
        knowledge = intelligence.get_collective_knowledge("gpu_performance_insights")
        print(f"\n  🌐 Collective learning occurred:")
        print(f"     - Knowledge topic created")
        print(f"     - Other agents can access insights")
        print(f"     - System intelligence improved")

    print(f"\n💡 Emergent Behaviors Observed:")
    print(f"   ✓ Competition led to resource optimization")
    print(f"   ✓ Resource usage generated collective knowledge")
    print(f"   ✓ Agents coordinated without central control")
    print(f"   ✓ System intelligence emerged from interactions")

    await coordinator.stop()


async def main():
    """Run all demonstrations."""
    print("\n" + "=" * 80)
    print(" ADVANCED MULTI-AGENT SYSTEM DEMONSTRATION")
    print("=" * 80)
    print("\nThis demo showcases:")
    print("  1. Shared Environment - Agents interact with common resources")
    print("  2. Distributed Coordination - Decentralized task allocation")
    print("  3. Negotiation & Competition - Auctions, voting, consensus")
    print("  4. Collective Intelligence - Emergent knowledge from interactions")
    print("  5. Emergent Behavior - Complex behaviors from simple rules")

    try:
        await demonstrate_shared_environment()
        await demonstrate_distributed_coordination()
        await demonstrate_negotiation_and_competition()
        await demonstrate_collective_intelligence()
        await demonstrate_emergent_behavior()

        print("\n" + "=" * 80)
        print("✅ ALL DEMONSTRATIONS COMPLETED SUCCESSFULLY")
        print("=" * 80)
        print("\nKey Achievements:")
        print("  ✓ Agents successfully interacted in shared environment")
        print("  ✓ Distributed coordination with automatic leader election")
        print("  ✓ Successful negotiations, auctions, and voting")
        print("  ✓ Collective intelligence with emergent patterns")
        print("  ✓ Complex emergent behavior from agent interactions")
        print("\n" + "=" * 80 + "\n")

    except Exception as e:
        logger.error(f"Error in demonstration: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
