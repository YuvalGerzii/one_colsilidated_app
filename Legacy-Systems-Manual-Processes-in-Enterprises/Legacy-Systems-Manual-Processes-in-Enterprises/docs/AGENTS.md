# Intelligent Agent Framework

The Enterprise AI Modernization Suite includes a powerful framework of specialized AI agents that work together to analyze legacy systems, identify modernization opportunities, and create actionable migration plans.

**All agents use 100% FREE local LLMs via Ollama - NO API costs!**

## Overview

The agent framework consists of 5 specialized agents:

| Agent | Role | Purpose |
|-------|------|---------|
| **Legacy Discovery** | Discovery | Scans codebases for legacy technologies and patterns |
| **Code Quality** | Assessment | Evaluates code quality and identifies improvements |
| **Technical Debt** | Analysis | Quantifies technical debt in hours and dollars |
| **Security Auditor** | Assessment | Identifies vulnerabilities and security risks |
| **Modernization Advisor** | Advisory | Creates comprehensive modernization plans |

## Agent Capabilities

### 1. Legacy Discovery Agent

**Purpose**: Systematically discover and catalog legacy systems across your enterprise.

**Capabilities**:
- Scan codebases for legacy language file extensions (COBOL, Fortran, VB6, Perl, ASP Classic)
- Detect obsolete frameworks (Struts 1, Spring 2, jQuery 1.x)
- Identify outdated database systems (Access, FoxPro, Oracle 8)
- Find obsolete code patterns (`eval()`, `goto`, inefficient SQL queries)
- Calculate overall risk level (critical/high/medium/low)
- AI-powered analysis of findings

**Example Output**:
```json
{
  "total_files": 1247,
  "legacy_files": [
    {"path": "/src/legacy/customer.cob", "language": "cobol"},
    {"path": "/app/util.vb", "language": "vb6"}
  ],
  "technologies": {
    "cobol": 45,
    "vb6": 23,
    "asp_classic": 12
  },
  "risk_level": "high",
  "ai_analysis": "The system shows significant legacy footprint with COBOL mainframe code..."
}
```

### 2. Code Quality Agent

**Purpose**: Assess code quality and identify improvement opportunities.

**Capabilities**:
- Calculate cyclomatic complexity
- Detect code smells:
  - Long functions (>50 lines)
  - Magic numbers
  - Deep nesting (>3 levels)
  - Duplicated code
  - Poor documentation
- Identify security issues (eval, exec, SQL injection patterns)
- Generate overall quality score (0-10)
- AI-powered improvement suggestions

**Example Output**:
```json
{
  "overall_score": 4.2,
  "complexity_score": 87,
  "code_smells": [
    {
      "type": "long_function",
      "severity": "medium",
      "message": "Function 'processOrder' has 127 lines",
      "line": 45
    }
  ],
  "issues": [
    {
      "type": "security",
      "severity": "high",
      "description": "Use of eval() detected"
    }
  ]
}
```

### 3. Technical Debt Agent

**Purpose**: Quantify technical debt in measurable terms (hours, dollars, ROI).

**Capabilities**:
- Identify debt categories:
  - Outdated dependencies
  - Code quality issues
  - Architecture problems
  - Documentation gaps
  - Test coverage deficiencies
- Calculate:
  - Total debt hours
  - Dollar value (@$150/hour)
  - Monthly "interest" (ongoing maintenance costs)
- Create priority matrix:
  - Quick Wins (low effort, high impact)
  - Major Projects (high effort, high impact)
  - Nice-to-Have (low effort, low impact)
  - Money Pits (high effort, low impact)
- Generate ROI-based payoff strategy

**Example Output**:
```json
{
  "total_hours": 2400,
  "total_cost": 360000,
  "total_interest_monthly": 12000,
  "priority_matrix": {
    "quick_win": [
      {
        "item": "Update jQuery 1.x to 3.x",
        "hours": 8,
        "impact": "high",
        "roi": 5.25
      }
    ],
    "major_project": [
      {
        "item": "Migrate COBOL to Python",
        "hours": 800,
        "impact": "critical",
        "roi": 1.8
      }
    ]
  }
}
```

### 4. Security Auditor Agent

**Purpose**: Identify security vulnerabilities and compliance issues.

**Capabilities**:
- Scan for OWASP Top 10 2021 vulnerabilities:
  - A03:2021 - Injection (SQL, XSS, Command)
  - A02:2021 - Cryptographic Failures (weak crypto)
  - A07:2021 - Identification and Authentication Failures (hardcoded credentials)
  - A08:2021 - Software and Data Integrity Failures (insecure deserialization)
- Detect specific vulnerability patterns
- Map to CWE (Common Weakness Enumeration)
- Calculate severity (critical/high/medium/low)
- Generate risk score (0-10)
- Provide remediation steps prioritized by severity

**Example Output**:
```json
{
  "vulnerabilities": [
    {
      "type": "sql_injection",
      "severity": "critical",
      "line": 127,
      "code_snippet": "query = 'SELECT * FROM users WHERE id=' + user_id",
      "cwe": "CWE-89",
      "description": "SQL injection vulnerability - user input not sanitized"
    }
  ],
  "severity_summary": {
    "critical": 3,
    "high": 7,
    "medium": 12,
    "low": 5
  },
  "risk_score": 7.8,
  "owasp_mapping": {
    "A03:2021-Injection": ["sql_injection", "xss"],
    "A02:2021-Cryptographic Failures": ["weak_crypto"]
  }
}
```

### 5. Modernization Advisor Agent

**Purpose**: Create comprehensive modernization strategies and plans.

**Capabilities**:
- Recommend modernization approach:
  - Strangler Fig (incremental replacement for large systems)
  - Parallel Run (build new alongside old)
  - Big Bang (complete rewrite for small systems)
- Suggest modern technology stacks:
  - Backend: Python/FastAPI, Java/Spring Boot, C#/.NET Core
  - Frontend: TypeScript/React, Next.js
  - Database: PostgreSQL, Redis
  - AI: Ollama (100% FREE local LLMs!)
- Create phased migration roadmap:
  - Phase 1: Foundation (setup, planning)
  - Phase 2: Core Migration (business logic)
  - Phase 3: Feature Parity (complete features)
  - Phase 4: Go-Live (deployment, cutover)
- Estimate costs:
  - Labor (developers, architects, QA, PM)
  - Infrastructure (dev, staging, production)
  - Tools (licenses, training, CI/CD)
  - 20% contingency buffer
- Identify risks and mitigations
- Define success metrics

**Example Output**:
```json
{
  "approach": "strangler_fig",
  "recommended_stack": {
    "backend": {
      "language": "Python",
      "framework": "FastAPI"
    },
    "frontend": {
      "language": "TypeScript",
      "framework": "React"
    },
    "ai_integration": {
      "llm": "Ollama (Local)",
      "note": "100% free, no API costs"
    }
  },
  "roadmap": {
    "total_duration_months": 18,
    "phases": [
      {
        "name": "Phase 1: Foundation",
        "duration_weeks": 4,
        "objectives": ["Setup environment", "Choose tech stack", "Establish standards"]
      }
    ]
  },
  "cost_estimate": {
    "total": 2250000,
    "labor": 1800000,
    "infrastructure": 126000,
    "tools": 174000,
    "contingency": 450000
  },
  "risks": [
    {
      "category": "Technical",
      "risk": "Data migration complexity",
      "probability": "medium",
      "impact": "high",
      "mitigation": "Extensive testing, dry runs, rollback plan"
    }
  ]
}
```

## Using Agents

### Via CLI

The agents can be invoked directly from the command line:

```bash
# Legacy Discovery
python cli.py agents discover --path /path/to/codebase

# Code Quality Assessment
python cli.py agents quality --file /path/to/file.py

# Security Scan
python cli.py agents security --file /path/to/file.py

# Technical Debt Analysis
python cli.py agents debt --file /path/to/file.py --age 10 --team-size 5

# Modernization Planning
python cli.py agents modernize --tech cobol --lines 250000 --team-size 8 --budget 1000000

# Comprehensive Analysis (all agents)
python cli.py agents analyze --path /path/to/codebase
```

### Via API

All agents are exposed through RESTful API endpoints:

#### Agent Status

```bash
GET /api/v1/agents/status
```

Response:
```json
{
  "status": "healthy",
  "total_agents": 5,
  "agents": [
    {
      "id": "legacy-discovery",
      "role": "discovery",
      "status": "idle",
      "capabilities": ["scan_codebase", "identify_technologies", ...]
    }
  ]
}
```

#### Execute Single Agent Task

```bash
POST /api/v1/agents/task
Content-Type: application/json

{
  "task_type": "scan",
  "description": "Scan codebase for legacy systems",
  "input_data": {"path": "/path/to/code"},
  "agent_id": "legacy-discovery"
}
```

#### Comprehensive Analysis Workflow

```bash
POST /api/v1/agents/workflow/comprehensive
Content-Type: application/json

{
  "codebase_path": "/path/to/code",
  "system_age_years": 10,
  "team_size": 5,
  "budget": 500000
}
```

Response includes results from all 5 agents plus executive summary.

#### Quick Security Scan

```bash
POST /api/v1/agents/workflow/security-scan
Content-Type: application/json

{
  "code": "def login(username, password): ...",
  "dependencies": ["flask==0.10"],
  "configuration": {"debug": false, "ssl_enabled": true}
}
```

#### Modernization Estimate

```bash
POST /api/v1/agents/workflow/modernization-estimate
Content-Type: application/json

{
  "legacy_technology": "cobol",
  "lines_of_code": 250000,
  "team_size": 8,
  "budget": 1000000
}
```

### Via Python Code

```python
import asyncio
from src.agents.framework import AgentTask, AgentOrchestrator
from src.agents.discovery_agent import LegacyDiscoveryAgent
from src.agents.security_agent import SecurityAuditorAgent

async def analyze_system():
    # Single agent
    discovery_agent = LegacyDiscoveryAgent()

    task = AgentTask(
        id="discovery-1",
        type="scan",
        description="Scan for legacy systems",
        input_data={"path": "/path/to/code"},
        assigned_to="legacy-discovery",
    )

    result = await discovery_agent.execute(task)
    print(f"Risk level: {result.output['risk_level']}")

    # Multiple agents with orchestrator
    orchestrator = AgentOrchestrator()
    orchestrator.register_agent(discovery_agent)
    orchestrator.register_agent(SecurityAuditorAgent())

    # Execute tasks in sequence
    discovery_result = await orchestrator.execute_task(discovery_task)
    security_result = await orchestrator.execute_task(security_task)

asyncio.run(analyze_system())
```

## Agent Orchestration

The `AgentOrchestrator` coordinates multiple agents working together:

**Features**:
- Agent registration and lifecycle management
- Task routing to appropriate agents
- Result aggregation
- Shared memory and context
- Error handling and recovery

**Example Workflow**:

```python
from examples.agent_workflow_legacy_analysis import comprehensive_legacy_analysis

# Run full analysis workflow
report = await comprehensive_legacy_analysis("/path/to/codebase")

print(f"Risk Level: {report['executive_summary']['risk_level']}")
print(f"Quality Score: {report['executive_summary']['quality_score']}/10")
print(f"Technical Debt: ${report['executive_summary']['technical_debt_cost']:,}")
print(f"Security Risk: {report['executive_summary']['security_risk_score']}/10")
```

## Cost Comparison

### Traditional Approach (Paid APIs)

- OpenAI GPT-4: $0.03 per 1K tokens input, $0.06 per 1K tokens output
- Typical analysis: ~100K tokens = **$3-5 per analysis**
- 1000 analyses per month = **$3,000-5,000/month**
- **Annual cost: $36,000-60,000**

### Our Approach (Local LLMs)

- Ollama: FREE
- Inference cost: $0
- Unlimited analyses: **$0/month**
- **Annual cost: $0**

**Savings: $36,000-60,000+ per year!**

## Best Practices

### 1. Start with Discovery

Always begin with the Legacy Discovery Agent to understand what you're dealing with:

```bash
python cli.py agents discover --path /path/to/codebase
```

### 2. Assess Quality and Security

After discovery, run quality and security assessments to identify immediate concerns:

```bash
python cli.py agents quality --file critical_module.py
python cli.py agents security --file critical_module.py
```

### 3. Quantify Technical Debt

Use the debt agent to understand the financial impact:

```bash
python cli.py agents debt --file legacy_system.py --age 15
```

### 4. Create Modernization Plan

Finally, create a comprehensive modernization plan:

```bash
python cli.py agents modernize --tech cobol --lines 500000 --team-size 10
```

### 5. Monitor and Iterate

Run agents regularly to track progress:
- Weekly: Security scans on critical modules
- Monthly: Code quality assessments
- Quarterly: Technical debt analysis
- Annually: Comprehensive modernization review

## Advanced Features

### Agent Memory

Agents maintain memory of previous tasks for context-aware analysis:

```python
agent = LegacyDiscoveryAgent()

# First scan
result1 = await agent.execute(task1)

# Second scan - agent remembers first scan
result2 = await agent.execute(task2)

# Access memory
print(agent.memory)  # List of previous tasks and results
```

### Custom Agents

Create your own specialized agents by extending `BaseAgent`:

```python
from src.agents.framework import BaseAgent, AgentRole, AgentTask, AgentResult

class CustomAgent(BaseAgent):
    def __init__(self):
        super().__init__("custom-agent", AgentRole.ANALYSIS)

    def get_capabilities(self) -> List[str]:
        return ["custom_capability_1", "custom_capability_2"]

    async def execute(self, task: AgentTask) -> AgentResult:
        # Your custom logic here
        analysis = await self.analyze_with_llm(
            prompt="Analyze this system...",
            context="You are a specialist in...",
        )

        return AgentResult(
            task_id=task.id,
            agent_id=self.agent_id,
            status=AgentStatus.COMPLETED,
            output={"custom_data": analysis},
            confidence=0.9,
        )
```

## Troubleshooting

### Agent Not Responding

Check Ollama service status:

```bash
python cli.py health
```

If Ollama is not running:

```bash
docker-compose up -d ollama
```

### Out of Memory Errors

Reduce batch size or use smaller models:

```python
llm = get_local_llm(model="llama3.2:3b")  # Smaller, faster model
```

### Slow Performance

Enable caching for repeated analyses:

```python
from src.core.llm import get_local_llm

llm = get_local_llm()
# Caching is enabled by default!

# Clear cache if needed
llm.clear_cache()
```

## Roadmap

Future enhancements:

- [ ] **Compliance Agent**: SOC2, HIPAA, GDPR compliance checking
- [ ] **Performance Agent**: Identify performance bottlenecks
- [ ] **Documentation Agent**: Auto-generate documentation
- [ ] **Test Generation Agent**: Create unit/integration tests
- [ ] **Dependency Agent**: Manage and update dependencies
- [ ] **Migration Executor**: Automated code translation

## Support

For questions or issues:

1. Check this documentation
2. Review examples in `/examples/agent_workflow_legacy_analysis.py`
3. Test agents with `python cli.py agents --help`
4. Create an issue on GitHub

---

**Remember: All agents use 100% FREE local LLMs - unlimited usage with ZERO cost!** 🎉
