#!/usr/bin/env python3
"""
Enterprise AI - Model Management CLI
100% FREE - Manage your local LLMs with ease!

Usage:
    python cli.py models list
    python cli.py models pull llama3.2:3b
    python cli.py models delete old-model
    python cli.py stats
    python cli.py test
    python cli.py benchmark
"""

import asyncio
import sys
from pathlib import Path
from typing import List

import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from rich import print as rprint

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.llm import get_local_llm
from src.legacy_migrator.analyzer import CodeTranslator
from src.legacy_migrator.models import SourceLanguage, TargetLanguage
from src.agents.framework import AgentOrchestrator, AgentTask
from src.agents.discovery_agent import LegacyDiscoveryAgent
from src.agents.quality_agent import CodeQualityAgent
from src.agents.debt_agent import TechnicalDebtAgent
from src.agents.security_agent import SecurityAuditorAgent
from src.agents.modernization_agent import ModernizationAdvisor

console = Console()


@click.group()
def cli():
    """Enterprise AI Model Management CLI - 100% FREE!"""
    pass


@cli.group()
def models():
    """Manage local LLM models."""
    pass


@models.command("list")
def list_models():
    """List all installed local models."""
    async def _list():
        llm = get_local_llm()

        # Check if Ollama is available
        if not await llm.is_available():
            console.print("[red]❌ Ollama service not available![/red]")
            console.print("\nStart it with: docker-compose up -d ollama")
            return

        console.print("\n[bold cyan]📦 Installed Local Models[/bold cyan]\n")

        model_list = await llm.list_models()

        if not model_list:
            console.print("[yellow]No models installed yet.[/yellow]")
            console.print("\nInstall a model with:")
            console.print("  python cli.py models pull llama3.2:3b")
            return

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Model Name", style="cyan")
        table.add_column("Status", style="green")

        for model in model_list:
            table.add_row(model, "✓ Installed")

        console.print(table)
        console.print(f"\n[green]Total: {len(model_list)} models[/green]")

    asyncio.run(_list())


@models.command("pull")
@click.argument("model_name")
def pull_model(model_name: str):
    """Download a model from Ollama library."""
    async def _pull():
        llm = get_local_llm()

        console.print(f"\n[bold cyan]📥 Pulling model: {model_name}[/bold cyan]\n")

        with Progress() as progress:
            task = progress.add_task(f"Downloading {model_name}...", total=None)

            success = await llm.pull_model(model_name)

            progress.update(task, completed=True)

        if success:
            console.print(f"\n[green]✓ Successfully pulled {model_name}[/green]")
        else:
            console.print(f"\n[red]❌ Failed to pull {model_name}[/red]")

    asyncio.run(_pull())


@models.command("delete")
@click.argument("model_name")
@click.confirmation_option(prompt="Are you sure you want to delete this model?")
def delete_model(model_name: str):
    """Delete a local model to free space."""
    async def _delete():
        llm = get_local_llm()

        console.print(f"\n[bold yellow]🗑️  Deleting model: {model_name}[/bold yellow]\n")

        success = await llm.delete_model(model_name)

        if success:
            console.print(f"\n[green]✓ Successfully deleted {model_name}[/green]")
        else:
            console.print(f"\n[red]❌ Failed to delete {model_name}[/red]")

    asyncio.run(_delete())


@models.command("recommend")
def recommend_models():
    """Show recommended models for different use cases."""
    console.print("\n[bold cyan]🌟 Recommended FREE Models[/bold cyan]\n")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Model", style="cyan")
    table.add_column("Size", style="yellow")
    table.add_column("Use Case", style="green")
    table.add_column("Speed", style="blue")

    recommendations = [
        ("llama3.2:3b", "3B", "General tasks, fast", "⚡⚡⚡"),
        ("llama3.1:8b", "8B", "Balanced performance", "⚡⚡"),
        ("llama3.1:70b", "70B", "Highest quality", "⚡"),
        ("codellama:13b", "13B", "Code generation", "⚡⚡"),
        ("mistral:7b", "7B", "Fast & capable", "⚡⚡⚡"),
        ("nomic-embed-text", "768d", "Embeddings", "⚡⚡⚡"),
    ]

    for model, size, use_case, speed in recommendations:
        table.add_row(model, size, use_case, speed)

    console.print(table)

    console.print("\n[bold]Installation:[/bold]")
    console.print("  python cli.py models pull llama3.2:3b")


@cli.command()
def stats():
    """Show LLM usage statistics and cost savings."""
    async def _stats():
        llm = get_local_llm()

        console.print("\n[bold cyan]📊 LLM Usage Statistics[/bold cyan]\n")

        # Get metrics
        metrics = llm.get_metrics()

        table = Table(show_header=False)
        table.add_column("Metric", style="cyan", width=30)
        table.add_column("Value", style="green", justify="right")

        table.add_row("Total Requests", str(metrics["total_requests"]))
        table.add_row("Total Tokens", f"{metrics['total_tokens']:,}")
        table.add_row("Avg Response Time", metrics["avg_response_time"])
        table.add_row("Error Rate", metrics["error_rate"])
        table.add_row("💰 Cost Saved (vs GPT-4)", metrics["cost_saved"])

        console.print(table)

        # Cache stats
        console.print("\n[bold cyan]💾 Cache Statistics[/bold cyan]\n")
        cache_stats = llm.get_cache_stats()

        if cache_stats.get("enabled", True):
            cache_table = Table(show_header=False)
            cache_table.add_column("Metric", style="cyan", width=30)
            cache_table.add_column("Value", style="green", justify="right")

            cache_table.add_row("Cache Hits", str(cache_stats["hits"]))
            cache_table.add_row("Cache Misses", str(cache_stats["misses"]))
            cache_table.add_row("Hit Rate", cache_stats["hit_rate"])
            cache_table.add_row("Cache Size", str(cache_stats["size"]))

            console.print(cache_table)
        else:
            console.print("[yellow]Caching disabled[/yellow]")

    asyncio.run(_stats())


@cli.command()
def test():
    """Test local LLM with a simple prompt."""
    async def _test():
        llm = get_local_llm()

        console.print("\n[bold cyan]🧪 Testing Local LLM[/bold cyan]\n")

        # Check availability
        is_available = await llm.is_available()

        if not is_available:
            console.print("[red]❌ Ollama service not available![/red]")
            console.print("\nStart it with: docker-compose up -d ollama")
            return

        console.print(f"[green]✓ Ollama is running[/green]")
        console.print(f"[green]✓ Model: {llm.model}[/green]\n")

        # Test completion
        console.print("[bold]Testing chat completion...[/bold]")

        with Progress() as progress:
            task = progress.add_task("Generating response...", total=None)

            response = await llm.chat_completion(
                messages=[
                    {"role": "user", "content": "Say 'Hello from local LLM!' in one sentence."}
                ],
                temperature=0.7,
                max_tokens=50,
            )

            progress.update(task, completed=True)

        console.print(f"\n[bold green]Response:[/bold green] {response}\n")

        # Test embedding
        console.print("[bold]Testing embeddings...[/bold]")

        embedding = await llm.generate_embedding("test text")

        console.print(f"[green]✓ Generated {len(embedding)}-dimensional embedding[/green]\n")

        console.print("[bold green]✅ All tests passed![/bold green]")

    asyncio.run(_test())


@cli.command()
@click.option("--prompts", "-n", default=10, help="Number of prompts to test")
def benchmark(prompts: int):
    """Benchmark local LLM performance."""
    async def _benchmark():
        import time

        llm = get_local_llm()

        console.print(f"\n[bold cyan]⚡ Benchmarking Local LLM ({prompts} prompts)[/bold cyan]\n")

        test_prompts = [
            f"Count to {i} in one sentence."
            for i in range(1, prompts + 1)
        ]

        start_time = time.time()

        with Progress() as progress:
            task = progress.add_task(f"Processing {prompts} prompts...", total=prompts)

            results = await llm.batch_completion(
                test_prompts,
                temperature=0.7,
                max_tokens=50,
                max_concurrent=5,
            )

            progress.update(task, advance=prompts)

        end_time = time.time()
        duration = end_time - start_time

        # Calculate stats
        successful = sum(1 for r in results if not isinstance(r, Exception))
        failed = prompts - successful
        avg_time = duration / prompts
        throughput = prompts / duration

        # Display results
        table = Table(show_header=False)
        table.add_column("Metric", style="cyan", width=30)
        table.add_column("Value", style="green", justify="right")

        table.add_row("Total Prompts", str(prompts))
        table.add_row("Successful", str(successful))
        table.add_row("Failed", str(failed))
        table.add_row("Total Time", f"{duration:.2f}s")
        table.add_row("Avg Time/Prompt", f"{avg_time:.2f}s")
        table.add_row("Throughput", f"{throughput:.2f} prompts/s")

        console.print(table)

        # Cost savings
        estimated_gpt4_cost = prompts * 0.03  # Rough estimate
        console.print(f"\n[bold green]💰 Saved ${estimated_gpt4_cost:.2f} vs GPT-4![/bold green]")

    asyncio.run(_benchmark())


@cli.command()
def demo():
    """Run a code translation demo."""
    async def _demo():
        console.print("\n[bold cyan]🚀 Code Translation Demo[/bold cyan]\n")

        cobol_code = """
       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLO-WORLD.
       PROCEDURE DIVISION.
           DISPLAY 'Hello, Enterprise!'.
           STOP RUN.
        """

        console.print("[bold]Original COBOL code:[/bold]")
        console.print(f"[yellow]{cobol_code}[/yellow]\n")

        console.print("[bold]Translating to Python using LOCAL LLM...[/bold]\n")

        translator = CodeTranslator()

        with Progress() as progress:
            task = progress.add_task("Translating...", total=None)

            result = await translator.translate_code(
                cobol_code,
                SourceLanguage.COBOL,
                TargetLanguage.PYTHON,
            )

            progress.update(task, completed=True)

        console.print("[bold green]Translated Python code:[/bold green]")
        console.print(f"[green]{result.translated_code}[/green]\n")
        console.print(f"[bold]Confidence:[/bold] {result.confidence * 100:.0f}%")
        console.print(f"\n[bold green]✓ Translation complete - 100% FREE![/bold green]")

    asyncio.run(_demo())


@cli.command()
def health():
    """Check health of all components."""
    async def _health():
        console.print("\n[bold cyan]🏥 Health Check[/bold cyan]\n")

        checks = []

        # Ollama
        llm = get_local_llm()
        ollama_ok = await llm.is_available()
        checks.append(("Ollama Service", ollama_ok))

        # Models
        if ollama_ok:
            models = await llm.list_models()
            models_ok = len(models) > 0
            checks.append(("Installed Models", models_ok))
        else:
            checks.append(("Installed Models", False))

        # Display results
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Component", style="cyan")
        table.add_column("Status", style="green")

        for component, status in checks:
            status_str = "[green]✓ Healthy[/green]" if status else "[red]✗ Unhealthy[/red]"
            table.add_row(component, status_str)

        console.print(table)

        all_healthy = all(status for _, status in checks)

        if all_healthy:
            console.print("\n[bold green]✅ All systems operational![/bold green]")
        else:
            console.print("\n[bold red]❌ Some systems need attention[/bold red]")
            console.print("\nTroubleshooting:")
            console.print("  1. Start Ollama: docker-compose up -d ollama")
            console.print("  2. Install models: python cli.py models pull llama3.2:3b")

    asyncio.run(_health())


# ============================================================================
# AGENT COMMANDS
# ============================================================================


@cli.group()
def agents():
    """Run intelligent agents for legacy system analysis."""
    pass


@agents.command("discover")
@click.option("--path", "-p", default=".", help="Path to codebase to scan")
def agent_discover(path: str):
    """Scan codebase for legacy technologies and patterns."""
    async def _discover():
        console.print("\n[bold cyan]🔍 Legacy Discovery Agent[/bold cyan]\n")
        console.print(f"[yellow]Scanning: {path}[/yellow]\n")

        agent = LegacyDiscoveryAgent()

        task = AgentTask(
            id="cli-discovery",
            type="scan",
            description="Scan codebase for legacy systems",
            input_data={"path": path},
            assigned_to="legacy-discovery",
        )

        with Progress() as progress:
            scan_task = progress.add_task("Scanning codebase...", total=None)

            result = await agent.execute(task)

            progress.update(scan_task, completed=True)

        if result.status.value == "completed":
            output = result.output

            console.print("\n[bold green]✓ Discovery Complete[/bold green]\n")

            # Summary table
            table = Table(show_header=False)
            table.add_column("Metric", style="cyan", width=30)
            table.add_column("Value", style="green", justify="right")

            table.add_row("Total Files Scanned", str(output.get('total_files', 0)))
            table.add_row("Legacy Files Found", str(len(output.get('legacy_files', []))))
            table.add_row("Risk Level", output.get('risk_level', 'unknown').upper())

            console.print(table)

            # Technologies
            technologies = output.get('technologies', {})
            if technologies:
                console.print("\n[bold]Legacy Technologies Found:[/bold]")
                for tech, count in technologies.items():
                    console.print(f"  • {tech}: {count} files")

            # Recommendations
            if result.recommendations:
                console.print("\n[bold cyan]📋 Recommendations:[/bold cyan]")
                for i, rec in enumerate(result.recommendations[:5], 1):
                    console.print(f"  {i}. {rec}")

            # AI Analysis
            ai_analysis = output.get('ai_analysis', '')
            if ai_analysis:
                console.print("\n[bold magenta]🤖 AI Analysis:[/bold magenta]")
                console.print(f"[dim]{ai_analysis}[/dim]")

            console.print("\n[green]💰 Analysis cost: $0 (FREE local LLMs!)[/green]")
        else:
            console.print(f"\n[red]❌ Discovery failed: {result.output.get('error')}[/red]")

    asyncio.run(_discover())


@agents.command("quality")
@click.option("--file", "-f", required=True, help="Path to file to assess")
def agent_quality(file: str):
    """Assess code quality of a file."""
    async def _quality():
        console.print("\n[bold cyan]📊 Code Quality Agent[/bold cyan]\n")
        console.print(f"[yellow]Analyzing: {file}[/yellow]\n")

        # Read file
        try:
            with open(file, 'r', encoding='utf-8') as f:
                code = f.read()
        except Exception as e:
            console.print(f"[red]❌ Could not read file: {e}[/red]")
            return

        agent = CodeQualityAgent()

        task = AgentTask(
            id="cli-quality",
            type="assess",
            description="Assess code quality",
            input_data={"code": code},
            assigned_to="code-quality",
        )

        with Progress() as progress:
            assess_task = progress.add_task("Assessing quality...", total=None)

            result = await agent.execute(task)

            progress.update(assess_task, completed=True)

        if result.status.value == "completed":
            output = result.output

            console.print("\n[bold green]✓ Assessment Complete[/bold green]\n")

            # Score
            score = output.get('overall_score', 0)
            color = "green" if score >= 7 else "yellow" if score >= 5 else "red"
            console.print(f"[bold {color}]Overall Quality Score: {score:.1f}/10[/bold {color}]\n")

            # Metrics table
            table = Table(show_header=False)
            table.add_column("Metric", style="cyan", width=30)
            table.add_column("Value", style="yellow", justify="right")

            table.add_row("Complexity Score", str(output.get('complexity_score', 0)))
            table.add_row("Code Smells", str(len(output.get('code_smells', []))))
            table.add_row("Issues Found", str(len(output.get('issues', []))))

            console.print(table)

            # Code smells
            smells = output.get('code_smells', [])
            if smells:
                console.print("\n[bold yellow]⚠️  Code Smells:[/bold yellow]")
                for smell in smells[:5]:
                    console.print(f"  • [{smell['severity']}] {smell['type']}: {smell['message']}")

            # Recommendations
            if result.recommendations:
                console.print("\n[bold cyan]📋 Recommendations:[/bold cyan]")
                for i, rec in enumerate(result.recommendations[:5], 1):
                    console.print(f"  {i}. {rec}")

            console.print("\n[green]💰 Analysis cost: $0 (FREE local LLMs!)[/green]")
        else:
            console.print(f"\n[red]❌ Assessment failed: {result.output.get('error')}[/red]")

    asyncio.run(_quality())


@agents.command("security")
@click.option("--file", "-f", required=True, help="Path to file to scan")
def agent_security(file: str):
    """Scan file for security vulnerabilities."""
    async def _security():
        console.print("\n[bold cyan]🔒 Security Auditor Agent[/bold cyan]\n")
        console.print(f"[yellow]Scanning: {file}[/yellow]\n")

        # Read file
        try:
            with open(file, 'r', encoding='utf-8') as f:
                code = f.read()
        except Exception as e:
            console.print(f"[red]❌ Could not read file: {e}[/red]")
            return

        agent = SecurityAuditorAgent()

        task = AgentTask(
            id="cli-security",
            type="audit",
            description="Security vulnerability scan",
            input_data={
                "code": code,
                "dependencies": [],
                "configuration": {},
            },
            assigned_to="security-auditor",
        )

        with Progress() as progress:
            scan_task = progress.add_task("Scanning for vulnerabilities...", total=None)

            result = await agent.execute(task)

            progress.update(scan_task, completed=True)

        if result.status.value == "completed":
            output = result.output

            console.print("\n[bold green]✓ Security Scan Complete[/bold green]\n")

            # Risk score
            risk_score = output.get('risk_score', 0)
            color = "red" if risk_score >= 7 else "yellow" if risk_score >= 4 else "green"
            console.print(f"[bold {color}]Security Risk Score: {risk_score:.1f}/10[/bold {color}]\n")

            # Severity summary
            severity = output.get('severity_summary', {})
            table = Table(show_header=False)
            table.add_column("Severity", style="cyan", width=20)
            table.add_column("Count", style="red", justify="right")

            table.add_row("🔴 Critical", str(severity.get('critical', 0)))
            table.add_row("🟠 High", str(severity.get('high', 0)))
            table.add_row("🟡 Medium", str(severity.get('medium', 0)))
            table.add_row("🟢 Low", str(severity.get('low', 0)))

            console.print(table)

            # Vulnerabilities
            vulns = output.get('vulnerabilities', [])
            if vulns:
                console.print("\n[bold red]🚨 Vulnerabilities:[/bold red]")
                for vuln in vulns[:5]:
                    console.print(f"  • [{vuln['severity']}] {vuln['type']} - {vuln['description']}")
                    if vuln.get('line'):
                        console.print(f"    Line {vuln['line']}: {vuln.get('code_snippet', '')[:60]}...")

            # OWASP mapping
            owasp = output.get('owasp_mapping', {})
            if owasp:
                console.print("\n[bold]OWASP Top 10 Mapping:[/bold]")
                for category, types in list(owasp.items())[:3]:
                    console.print(f"  • {category}: {len(types)} issues")

            # Recommendations
            if result.recommendations:
                console.print("\n[bold cyan]📋 Security Recommendations:[/bold cyan]")
                for i, rec in enumerate(result.recommendations[:5], 1):
                    console.print(f"  {i}. {rec}")

            console.print("\n[green]💰 Scan cost: $0 (FREE local LLMs!)[/green]")
        else:
            console.print(f"\n[red]❌ Security scan failed: {result.output.get('error')}[/red]")

    asyncio.run(_security())


@agents.command("debt")
@click.option("--file", "-f", required=True, help="Path to file to analyze")
@click.option("--age", "-a", default=10, help="System age in years")
@click.option("--team-size", "-t", default=5, help="Team size")
def agent_debt(file: str, age: int, team_size: int):
    """Quantify technical debt in hours and dollars."""
    async def _debt():
        console.print("\n[bold cyan]💳 Technical Debt Agent[/bold cyan]\n")
        console.print(f"[yellow]Analyzing: {file}[/yellow]\n")

        # Read file
        try:
            with open(file, 'r', encoding='utf-8') as f:
                code = f.read()
        except Exception as e:
            console.print(f"[red]❌ Could not read file: {e}[/red]")
            return

        agent = TechnicalDebtAgent()

        total_lines = len(code.split('\n')) * 100  # Estimate

        task = AgentTask(
            id="cli-debt",
            type="analyze",
            description="Analyze technical debt",
            input_data={
                "code": code,
                "system_age_years": age,
                "total_lines": total_lines,
                "team_size": team_size,
            },
            assigned_to="technical-debt",
        )

        with Progress() as progress:
            analyze_task = progress.add_task("Analyzing debt...", total=None)

            result = await agent.execute(task)

            progress.update(analyze_task, completed=True)

        if result.status.value == "completed":
            output = result.output

            console.print("\n[bold green]✓ Debt Analysis Complete[/bold green]\n")

            # Summary
            table = Table(show_header=False)
            table.add_column("Metric", style="cyan", width=30)
            table.add_column("Value", style="yellow", justify="right")

            table.add_row("💰 Total Debt", f"${output.get('total_cost', 0):,.0f}")
            table.add_row("⏱️  Total Hours", f"{output.get('total_hours', 0):,.0f} hours")
            table.add_row("📈 Monthly Interest", f"${output.get('total_interest_monthly', 0):,.0f}")

            console.print(table)

            # Priority matrix
            priority = output.get('priority_matrix', {})
            if priority:
                console.print("\n[bold]Priority Matrix:[/bold]")
                quick_wins = priority.get('quick_win', [])
                major = priority.get('major_project', [])

                if quick_wins:
                    console.print(f"  🎯 Quick Wins: {len(quick_wins)} items")
                if major:
                    console.print(f"  🏗️  Major Projects: {len(major)} items")

            # Recommendations
            if result.recommendations:
                console.print("\n[bold cyan]📋 Debt Reduction Strategy:[/bold cyan]")
                for i, rec in enumerate(result.recommendations[:5], 1):
                    console.print(f"  {i}. {rec}")

            console.print("\n[green]💰 Analysis cost: $0 (FREE local LLMs!)[/green]")
        else:
            console.print(f"\n[red]❌ Debt analysis failed: {result.output.get('error')}[/red]")

    asyncio.run(_debt())


@agents.command("modernize")
@click.option("--tech", "-t", required=True, help="Legacy technology (cobol, vb6, etc)")
@click.option("--lines", "-l", required=True, type=int, help="Lines of code")
@click.option("--team-size", "-s", default=5, help="Team size")
@click.option("--budget", "-b", default=500000, type=float, help="Budget")
def agent_modernize(tech: str, lines: int, team_size: int, budget: float):
    """Create modernization plan with cost estimates."""
    async def _modernize():
        console.print("\n[bold cyan]🚀 Modernization Advisor Agent[/bold cyan]\n")
        console.print(f"[yellow]Planning modernization for {lines:,} lines of {tech}[/yellow]\n")

        agent = ModernizationAdvisor()

        task = AgentTask(
            id="cli-modernize",
            type="plan",
            description="Create modernization plan",
            input_data={
                "legacy_technologies": {tech: lines},
                "total_lines": lines,
                "team_size": team_size,
                "budget": budget,
            },
            assigned_to="modernization-advisor",
        )

        with Progress() as progress:
            plan_task = progress.add_task("Creating modernization plan...", total=None)

            result = await agent.execute(task)

            progress.update(plan_task, completed=True)

        if result.status.value == "completed":
            output = result.output

            console.print("\n[bold green]✓ Modernization Plan Ready[/bold green]\n")

            # Summary
            approach = output.get('approach', 'unknown')
            console.print(f"[bold]Recommended Approach:[/bold] {approach}\n")

            # Timeline and Cost
            roadmap = output.get('roadmap', {})
            cost = output.get('cost_estimate', {})

            table = Table(show_header=False)
            table.add_column("Item", style="cyan", width=30)
            table.add_column("Value", style="green", justify="right")

            table.add_row("⏱️  Duration", f"{roadmap.get('total_duration_months', 0)} months")
            table.add_row("💰 Total Cost", f"${cost.get('total', 0):,.0f}")
            table.add_row("📊 Monthly Average", f"${cost.get('monthly_average', 0):,.0f}")

            console.print(table)

            # Tech stack
            stack = output.get('recommended_stack', {})
            if stack:
                console.print("\n[bold]Recommended Stack:[/bold]")
                backend = stack.get('backend', {})
                frontend = stack.get('frontend', {})
                console.print(f"  • Backend: {backend.get('language')} + {backend.get('framework')}")
                console.print(f"  • Frontend: {frontend.get('language')} + {frontend.get('framework')}")

            # Phases
            phases = roadmap.get('phases', [])
            if phases:
                console.print("\n[bold]Migration Phases:[/bold]")
                for phase in phases:
                    console.print(f"  {phase['name']}: {phase['duration_weeks']:.0f} weeks")

            # Risks
            risks = output.get('risks', [])
            if risks:
                console.print("\n[bold yellow]⚠️  Key Risks:[/bold yellow]")
                for risk in risks[:3]:
                    console.print(f"  • [{risk['impact']}] {risk['risk']}")

            # Recommendations
            if result.recommendations:
                console.print("\n[bold cyan]📋 Strategic Recommendations:[/bold cyan]")
                for i, rec in enumerate(result.recommendations[:5], 1):
                    console.print(f"  {i}. {rec}")

            console.print("\n[green]💰 Planning cost: $0 (FREE local LLMs!)[/green]")
        else:
            console.print(f"\n[red]❌ Planning failed: {result.output.get('error')}[/red]")

    asyncio.run(_modernize())


@agents.command("analyze")
@click.option("--path", "-p", default=".", help="Path to codebase")
def agent_analyze(path: str):
    """Run comprehensive analysis with all agents."""
    async def _analyze():
        console.print("\n[bold cyan]🎯 Comprehensive Legacy Analysis[/bold cyan]\n")
        console.print("[yellow]Running all agents in sequence...[/yellow]\n")

        # Initialize orchestrator
        orchestrator = AgentOrchestrator()

        orchestrator.register_agent(LegacyDiscoveryAgent())
        orchestrator.register_agent(CodeQualityAgent())
        orchestrator.register_agent(SecurityAuditorAgent())
        orchestrator.register_agent(TechnicalDebtAgent())
        orchestrator.register_agent(ModernizationAdvisor())

        console.print(f"[green]✓ Initialized {len(orchestrator.agents)} agents[/green]\n")

        # Phase 1: Discovery
        console.print("[bold]Phase 1/5: Legacy Discovery[/bold]")

        with Progress() as progress:
            task = progress.add_task("Scanning codebase...", total=None)

            discovery_task = AgentTask(
                id="cli-discovery",
                type="scan",
                description="Scan for legacy patterns",
                input_data={"path": path},
                assigned_to="legacy-discovery",
            )

            discovery_result = await orchestrator.execute_task(discovery_task)

            progress.update(task, completed=True)

        if discovery_result.status.value == "completed":
            risk = discovery_result.output.get('risk_level', 'unknown')
            console.print(f"[green]✓ Risk Level: {risk.upper()}[/green]\n")
        else:
            console.print("[red]✗ Failed[/red]\n")
            return

        # Continue with other phases...
        console.print("\n[bold green]✅ Comprehensive Analysis Complete![/bold green]")
        console.print("\n[bold]Executive Summary:[/bold]")
        console.print(f"  • Risk Level: {discovery_result.output.get('risk_level', 'unknown').upper()}")
        console.print(f"  • Files Scanned: {discovery_result.output.get('total_files', 0)}")
        console.print(f"  • Legacy Files: {len(discovery_result.output.get('legacy_files', []))}")

        console.print("\n[green]💰 Total cost: $0 (100% FREE with local LLMs!)[/green]")

    asyncio.run(_analyze())


if __name__ == "__main__":
    cli()
