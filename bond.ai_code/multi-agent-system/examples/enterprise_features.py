"""
Enterprise Features Demonstration.

Showcases production-ready features:
- Advanced fallback chains
- Full MCP server/client
- Database persistence
- Intelligent caching
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from multi_agent_system.core.fallback import (
    FallbackChain,
    FallbackStrategy,
    get_fallback_registry,
)
from multi_agent_system.mcp.server import (
    MCPServer,
    MCPClient,
    ResourceType,
    ToolCategory,
)
from multi_agent_system.persistence.database import DatabaseManager
from multi_agent_system.cache.cache_manager import CacheManager
from multi_agent_system.core.types import Task, Result, TaskStatus


async def demo_fallback_system():
    """Demonstrate advanced fallback system."""
    print("\n" + "=" * 60)
    print("1. ADVANCED FALLBACK SYSTEM")
    print("=" * 60)

    # Create fallback chain with adaptive strategy
    chain = FallbackChain("data_fetch", FallbackStrategy.ADAPTIVE)

    # Add fallback options
    async def primary_fetch():
        """Primary data fetch (simulated failure)."""
        raise Exception("Primary API unavailable")

    async def fallback_cache():
        """Fallback to cache."""
        print("  → Trying cache fallback...")
        return {"source": "cache", "data": "cached_data"}

    async def fallback_backup():
        """Fallback to backup service."""
        print("  → Trying backup service fallback...")
        return {"source": "backup", "data": "backup_data"}

    chain.add_fallback("cache", fallback_cache, priority=2)
    chain.add_fallback("backup", fallback_backup, priority=1)

    # Execute with fallbacks
    print("\nExecuting with fallback chain...")
    result = await chain.execute(primary_fetch)
    print(f"Result: {result}")

    # Show statistics
    print(f"\nFallback statistics:")
    stats = chain.get_statistics()
    for fallback in stats["fallbacks"]:
        print(f"  {fallback['name']}: success_rate={fallback['success_rate']:.2%}")


async def demo_mcp_system():
    """Demonstrate Model Context Protocol."""
    print("\n" + "=" * 60)
    print("2. MODEL CONTEXT PROTOCOL (MCP)")
    print("=" * 60)

    # Create MCP server
    server = MCPServer("knowledge-server")

    # Register a resource
    def get_knowledge():
        return "AI systems use machine learning to improve performance."

    server.register_resource(
        uri="knowledge://ai/overview",
        name="AI Overview",
        description="General AI knowledge",
        resource_type=ResourceType.TEXT,
        handler=get_knowledge,
        mime_type="text/plain",
    )

    # Register a tool
    def analyze_text(text: str, mode: str = "sentiment"):
        return {
            "text": text,
            "mode": mode,
            "result": "positive" if "good" in text.lower() else "neutral",
        }

    server.register_tool(
        name="analyze_text",
        description="Analyze text content",
        category=ToolCategory.DATA_PROCESSING,
        input_schema={
            "type": "object",
            "properties": {
                "text": {"type": "string"},
                "mode": {"type": "string", "enum": ["sentiment", "summary"]},
            },
            "required": ["text"],
        },
        handler=analyze_text,
    )

    # Register a prompt
    server.register_prompt(
        name="task_decomposition",
        description="Decompose a complex task",
        template="Break down this task: {task}\nRequirements: {requirements}",
        arguments=[
            {"name": "task", "type": "string", "required": True},
            {"name": "requirements", "type": "string", "required": False},
        ],
    )

    # Create MCP client
    client = MCPClient("agent-client")
    client.connect_server("knowledge", server)

    # Use MCP resources
    print("\nListing available resources:")
    resources = await client.list_resources()
    for resource in resources:
        print(f"  {resource['name']}: {resource['uri']}")

    print("\nReading resource:")
    content = await client.read_resource("knowledge://ai/overview")
    print(f"  Content: {content['content']}")

    # Use MCP tools
    print("\nCalling MCP tool:")
    result = await client.call_tool("analyze_text", {"text": "This is good news!"})
    print(f"  Analysis result: {result}")

    # Use prompts
    print("\nUsing prompt template:")
    prompt = client.get_prompt(
        "task_decomposition",
        task="Build a web application",
        requirements="authentication, database, API",
    )
    print(f"  Generated prompt:\n  {prompt}")


async def demo_database_persistence():
    """Demonstrate database persistence."""
    print("\n" + "=" * 60)
    print("3. DATABASE PERSISTENCE")
    print("=" * 60)

    # Initialize database
    db = DatabaseManager("./data/demo.db")

    # Create and save a task
    print("\nSaving task to database...")
    task = Task(
        description="Process data analysis",
        requirements=["data_processing", "visualization"],
        priority=5,
        status=TaskStatus.PENDING,
    )
    db.save_task(task)
    print(f"  Saved task: {task.id}")

    # Save a result
    print("\nSaving result...")
    result = Result(
        task_id=task.id,
        success=True,
        data={"analysis": "completed", "charts": 3},
        agent_id="analyst_1",
        execution_time=12.5,
        quality_score=0.92,
    )
    db.save_result(result)

    # Query tasks
    print("\nQuerying pending tasks...")
    tasks = db.query_tasks(status=TaskStatus.PENDING, limit=5)
    print(f"  Found {len(tasks)} pending tasks")
    for t in tasks[:2]:
        print(f"    - {t.description[:50]}...")

    # Get statistics
    print("\nDatabase statistics:")
    stats = db.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")


async def demo_caching_system():
    """Demonstrate intelligent caching."""
    print("\n" + "=" * 60)
    print("4. INTELLIGENT CACHING SYSTEM")
    print("=" * 60)

    cache = CacheManager()

    # Cache a result
    print("\nCaching task result...")
    cache.cache_result("task_123", {"status": "complete", "value": 42})

    # Retrieve from cache
    print("Retrieving from cache...")
    cached = cache.get_cached_result("task_123")
    print(f"  Cached result: {cached}")

    # Cache embeddings
    print("\nCaching embeddings...")
    cache.cache_embedding("machine learning", [0.1, 0.2, 0.3])
    cached_emb = cache.get_cached_embedding("machine learning")
    print(f"  Cached embedding: {cached_emb}")

    # Cached computation
    print("\nCached computation...")

    call_count = [0]

    async def expensive_computation():
        call_count[0] += 1
        await asyncio.sleep(0.1)  # Simulate expensive operation
        return {"computed": True, "value": 100}

    # First call - cache miss
    result1 = await cache.cached_computation("comp_1", expensive_computation)
    print(f"  First call (miss): {result1}, calls={call_count[0]}")

    # Second call - cache hit
    result2 = await cache.cached_computation("comp_1", expensive_computation)
    print(f"  Second call (hit): {result2}, calls={call_count[0]}")

    # Cache warming
    print("\nWarming cache with pre-computed values...")
    cache.warm_cache(
        {
            "config_1": {"setting": "value1"},
            "config_2": {"setting": "value2"},
        },
        cache_type="computation",
    )

    # Get statistics
    print("\nCache statistics:")
    stats = cache.get_statistics()
    print(f"  Overall hit rate: {cache.get_overall_hit_rate():.2%}")
    for cache_name, cache_stats in stats.items():
        print(f"  {cache_name}:")
        print(f"    Size: {cache_stats['size']}/{cache_stats['max_size']}")
        print(f"    Hit rate: {cache_stats['hit_rate']:.2%}")


async def demo_integrated_system():
    """Demonstrate all features working together."""
    print("\n" + "=" * 60)
    print("5. INTEGRATED ENTERPRISE SYSTEM")
    print("=" * 60)

    print("\nInitializing enterprise components...")

    # Initialize all systems
    db = DatabaseManager("./data/enterprise.db")
    cache = CacheManager()
    mcp_server = MCPServer("enterprise-server")
    registry = get_fallback_registry()

    # Register fallback chain
    chain = registry.register_chain("data_pipeline", FallbackStrategy.ADAPTIVE)

    async def primary_pipeline(data):
        # Simulate processing
        return {"processed": data, "source": "primary"}

    async def fallback_simple(data):
        return {"processed": data, "source": "fallback_simple"}

    chain.add_fallback("simple_processing", fallback_simple, priority=1)

    # Setup MCP tool
    def process_data(input_data: str):
        return {"output": input_data.upper(), "processed": True}

    mcp_server.register_tool(
        name="process_data",
        description="Process data",
        category=ToolCategory.DATA_PROCESSING,
        input_schema={"type": "object", "properties": {"input_data": {"type": "string"}}},
        handler=process_data,
    )

    print("\nExecuting integrated workflow...")

    # 1. Create task and save to DB
    task = Task(
        description="Enterprise data processing task",
        requirements=["processing", "validation"],
        priority=8,
    )
    db.save_task(task)
    print(f"  ✓ Task saved to database: {task.id}")

    # 2. Check cache first
    cached_result = cache.get_cached_result(task.id)
    if cached_result:
        print("  ✓ Using cached result")
        result_data = cached_result
    else:
        # 3. Execute with fallback
        try:
            result_data = await chain.execute(primary_pipeline, "test_data")
            print(f"  ✓ Processed with fallback: {result_data['source']}")
        except:
            # 4. Use MCP tool as last resort
            result_data = await mcp_server.call_tool("process_data", {"input_data": "test"})
            print("  ✓ Processed with MCP tool")

        # 5. Cache the result
        cache.cache_result(task.id, result_data)
        print("  ✓ Result cached")

    # 6. Save result to DB
    result = Result(
        task_id=task.id,
        success=True,
        data=result_data,
        agent_id="enterprise_agent",
        execution_time=1.5,
        quality_score=0.95,
    )
    db.save_result(result)
    print("  ✓ Result saved to database")

    # Show final statistics
    print("\nFinal Statistics:")
    print(f"  Database: {db.get_statistics()}")
    print(f"  Cache hit rate: {cache.get_overall_hit_rate():.2%}")
    print(f"  MCP tools: {len(mcp_server.list_tools())}")


async def main():
    """Run all enterprise feature demonstrations."""
    print("\n" + "=" * 60)
    print("ENTERPRISE FEATURES DEMONSTRATION")
    print("=" * 60)

    await demo_fallback_system()
    await demo_mcp_system()
    await demo_database_persistence()
    await demo_caching_system()
    await demo_integrated_system()

    print("\n" + "=" * 60)
    print("All enterprise features demonstrated successfully!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
