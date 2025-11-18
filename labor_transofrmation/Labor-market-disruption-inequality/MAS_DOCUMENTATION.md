# Multi-Agent System (MAS) Documentation

## Overview

The Multi-Agent System is an advanced architecture that enables multiple AI agents to communicate, coordinate, and collaborate to solve complex problems through collective intelligence.

**Key Features:**
- **Distributed Control**: No single point of control; agents make autonomous decisions
- **Shared Environment**: Blackboard pattern for agent state sharing
- **Agent Communication**: Message-based communication with priority queuing
- **Task Distribution**: Intelligent task assignment based on capabilities
- **Collective Intelligence**: Emergent problem-solving through agent interactions

## Architecture

### Core Components

#### 1. SharedEnvironment (Blackboard Pattern)
```python
# Located in: backend/app/core/multi_agent_system.py

class SharedEnvironment:
    """
    Central knowledge base where all agents can:
    - Read shared state
    - Write updates
    - Subscribe to changes
    - Publish events
    - Lock resources
    """
```

**Features:**
- Thread-safe operations with locks
- Event log for audit trail
- Subscriber pattern for reactive updates
- Resource locking mechanism
- Performance metrics tracking

**API Methods:**
- `read(key, default)` - Read from knowledge base
- `write(key, value, agent_id)` - Write to knowledge base
- `subscribe(key, callback)` - Subscribe to changes
- `publish_event(event_type, data, agent_id)` - Publish events
- `acquire_lock(resource_id, agent_id)` - Lock resources
- `release_lock(resource_id, agent_id)` - Release locks

#### 2. MultiAgentCoordinator
```python
class MultiAgentCoordinator:
    """
    Orchestrates multi-agent collaboration:
    - Task distribution with capability matching
    - Message routing with priority
    - Workflow management
    - Performance monitoring
    """
```

**Features:**
- Agent registration and lifecycle management
- Priority-based message queue
- Task capability matching
- Workflow dependency resolution
- Negotiation and voting mechanisms
- Network visualization

**API Methods:**
- `register_agent(agent)` - Register agent
- `send_message(message)` - Send inter-agent message
- `distribute_task(task)` - Assign task to best agent
- `create_workflow(workflow_id, tasks)` - Multi-task workflow
- `request_collaboration(requester_id, task, agents)` - Request collaboration
- `negotiate(agents, topic, proposals)` - Facilitate negotiation
- `vote(agents, question, options)` - Collective voting
- `get_consensus(agents, topic, proposals)` - Build consensus

#### 3. BaseAgent (Extended)
```python
# Located in: backend/app/agents/base_agent.py

class BaseAgent(ABC):
    """
    Enhanced base agent with MAS capabilities:
    - Shared environment access
    - Inter-agent messaging
    - Task delegation
    - Collaboration requests
    """
```

**New MAS Methods:**
- `enable_mas(shared_env, coordinator)` - Enable MAS features
- `read_shared_knowledge(key)` - Read from shared environment
- `write_shared_knowledge(key, value)` - Write to shared environment
- `publish_result(result_key, result_data)` - Publish task results
- `send_mas_message(to_agent, type, payload)` - Send MAS message
- `request_collaboration(task, agents)` - Request collaboration
- `delegate_subtask(name, description, caps, data)` - Delegate work

## Workflows

### 1. Career Transition Workflow

**Description:** Complex 5-agent collaboration for career transition planning

**Flow:**
```
1. Gap Analyzer → Analyzes skills gap → Writes to shared env
2. Opportunity Scout → Reads gap → Finds jobs → Writes opportunities
3. Learning Strategist → Reads gap & opportunities → Creates path → Writes path
4. Teaching Coach → Reads path → Prepares materials → Writes materials
5. Career Navigator → Reads all → Creates final plan → Writes final plan
```

**Demonstrates:**
- Sequential task execution with dependencies
- Data flow through shared environment
- Collective intelligence from agent interactions

**API Endpoint:**
```http
POST /api/v1/mas/workflows/career-transition
{
  "worker_id": 1,
  "target_role": "Data Scientist"
}
```

**Response:**
```json
{
  "success": true,
  "workflow": {
    "workflow_id": "wf_abc123",
    "workflow_key": "workflow:wf_abc123",
    "status": "executing",
    "total_tasks": 5,
    "task_ids": ["task1", "task2", "task3", "task4", "task5"]
  }
}
```

### 2. Learning Consensus Workflow

**Description:** Multiple agents negotiate optimal learning strategy

**Flow:**
```
1. Multiple strategy agents propose learning approaches
2. Agents vote on proposals
3. Consensus building through discussion
4. Final strategy selected
```

**Demonstrates:**
- Agent negotiation
- Voting mechanisms
- Consensus building
- Competitive proposal evaluation

**API Endpoint:**
```http
POST /api/v1/mas/workflows/learning-consensus
{
  "worker_id": 1,
  "target_skills": ["Python", "SQL", "ML"],
  "time_constraint_hours": 100
}
```

### 3. Distributed Market Analysis

**Description:** Parallel job market analysis by specialized agents

**Flow:**
```
Parallel Execution:
- Trend Analyzer → Market trends
- Salary Analyzer → Compensation data
- Demand Analyzer → Skill demand
- Competition Analyzer → Competition level

All results aggregated in shared environment
```

**Demonstrates:**
- Parallel task execution (no dependencies)
- Distributed data collection
- Result aggregation

**API Endpoint:**
```http
POST /api/v1/mas/workflows/market-analysis
{
  "industry": "Technology",
  "region": "US",
  "skills": ["Python", "SQL", "ML"]
}
```

### 4. Resource Curation Workflow

**Description:** Collaborative resource discovery and curation

**Flow:**
```
1. Multiple curator agents search for resources
2. Each contributes findings to shared environment
3. Agents collaboratively rate and filter
4. Quality consensus through multi-agent scoring
```

**Demonstrates:**
- Agent collaboration requests
- Resource sharing through shared environment
- Quality scoring through consensus

**API Endpoint:**
```http
POST /api/v1/mas/workflows/resource-curation
{
  "topic": "Machine Learning",
  "difficulty_level": "intermediate",
  "learner_preferences": {}
}
```

## Message Types

### Inter-Agent Message Types (MessageType Enum)

| Type | Description | Example Use Case |
|------|-------------|------------------|
| REQUEST | Request action from another agent | "Please analyze this skills gap" |
| RESPONSE | Response to request | "Here's the gap analysis result" |
| INFORM | Inform agent of information | "Task completed successfully" |
| QUERY | Query for information | "What's the current market trend?" |
| PROPOSE | Propose a solution/approach | "I propose this learning path" |
| ACCEPT | Accept proposal | "I accept your proposal" |
| REJECT | Reject proposal | "I reject due to time constraints" |
| DELEGATE | Delegate subtask | "Please handle resource curation" |
| COMPLETE | Task completion notification | "Learning path created" |
| NEGOTIATE | Start negotiation | "Let's negotiate the approach" |

### Message Structure

```python
@dataclass
class AgentMessage:
    id: str                           # Unique message ID
    from_agent: str                   # Sender agent ID
    to_agent: str                     # Recipient agent ID
    message_type: MessageType         # Message type enum
    payload: Dict                     # Message data
    timestamp: datetime               # Send timestamp
    priority: int = 5                 # 1=highest, 10=lowest
    requires_response: bool = False   # Needs response?
    conversation_id: Optional[str]    # Conversation tracking
    in_reply_to: Optional[str]        # Reply to message ID
    deadline: Optional[datetime]      # Response deadline
```

## Task System

### Task Status Flow

```
PENDING → ASSIGNED → IN_PROGRESS → COMPLETED
                 ↓                ↓
                 WAITING      FAILED/CANCELLED
```

### Task Distribution Algorithm

1. **Capability Matching**: Find agents with required capabilities
2. **Performance Scoring**: Score agents by success rate & response time
3. **Best Agent Selection**: Assign to highest-scoring agent
4. **Message Dispatch**: Send task request message
5. **Status Tracking**: Monitor task progress

### DistributedTask Structure

```python
@dataclass
class DistributedTask:
    task_id: str                      # Unique task ID
    name: str                         # Task name
    description: str                  # Task description
    required_capabilities: List[str]   # Required agent capabilities
    input_data: Dict                  # Input parameters
    output_data: Optional[Dict]       # Results (when complete)
    status: TaskStatus                # Current status
    assigned_agent: Optional[str]     # Assigned agent ID
    dependencies: List[str]           # Dependency task IDs
    priority: int = 5                 # 1=highest, 10=lowest
    created_at: datetime              # Creation timestamp
    started_at: Optional[datetime]    # Start timestamp
    completed_at: Optional[datetime]  # Completion timestamp
    result: Optional[Any]             # Task result
    error: Optional[str]              # Error message if failed
```

## API Reference

### Base URL
```
http://localhost:8000/api/v1/mas
```

### Workflow Endpoints

#### Start Career Transition
```http
POST /workflows/career-transition
Content-Type: application/json

{
  "worker_id": 1,
  "target_role": "Data Scientist"
}
```

#### Get Workflow Progress
```http
GET /workflows/{workflow_id}/progress
```

**Response:**
```json
{
  "success": true,
  "progress": {
    "workflow_id": "wf_123",
    "total_tasks": 5,
    "completed": 3,
    "failed": 0,
    "in_progress": 2,
    "progress_percentage": 60,
    "status": "in_progress",
    "tasks": [...]
  }
}
```

### Agent Coordination

#### Request Collaboration
```http
POST /collaboration/request
Content-Type: application/json

{
  "requester_id": "gap_analyzer",
  "task_description": "Analyze comprehensive career path",
  "required_agents": ["opportunity_scout", "learning_strategist"]
}
```

#### Distribute Task
```http
POST /tasks/distribute
Content-Type: application/json

{
  "task_name": "Market Analysis",
  "task_description": "Analyze tech job market",
  "required_capabilities": ["trend_analysis"],
  "input_data": {"industry": "Technology"},
  "priority": 3
}
```

### Shared Environment

#### Read Shared Knowledge
```http
GET /shared-environment/knowledge/{key}
```

#### Get Recent Events
```http
GET /shared-environment/events?limit=100&event_type=task_completed
```

#### Get Environment Metrics
```http
GET /shared-environment/metrics
```

**Response:**
```json
{
  "success": true,
  "metrics": {
    "total_writes": 150,
    "writes_by_gap_analyzer": 25,
    "writes_by_opportunity_scout": 30,
    ...
  }
}
```

### System Monitoring

#### Get System Status
```http
GET /status
```

**Response:**
```json
{
  "success": true,
  "system": {
    "timestamp": "2025-11-16T10:30:00Z",
    "agents": {
      "total": 8,
      "active": 7,
      "by_type": {
        "gap_analyzer": 1,
        "opportunity_scout": 1,
        ...
      }
    },
    "tasks": {
      "total": 15,
      "by_status": {
        "completed": 10,
        "in_progress": 3,
        "pending": 2
      }
    },
    "workflows": {
      "total": 3,
      "active": 1
    },
    "messages": {
      "pending": 5,
      "conversations": 8
    },
    "shared_environment": {...},
    "performance": {...}
  }
}
```

#### List All Agents
```http
GET /agents
```

#### Get Agent Details
```http
GET /agents/{agent_id}
```

#### Activate/Deactivate Agent
```http
POST /agents/{agent_id}/activate
POST /agents/{agent_id}/deactivate
```

### Network & Analytics

#### Get Agent Network Visualization
```http
GET /network/visualization
```

**Response:**
```json
{
  "success": true,
  "network": {
    "nodes": [
      {
        "id": "gap_analyzer",
        "type": "gap_analyzer",
        "capabilities": ["skill_gap_analysis"],
        "active": true,
        "metrics": {...}
      },
      ...
    ],
    "edges": [
      {
        "from": "gap_analyzer",
        "to": "opportunity_scout",
        "weight": 15,
        "type": "communication"
      },
      ...
    ],
    "timestamp": "2025-11-16T10:30:00Z"
  }
}
```

#### Get Performance Analytics
```http
GET /analytics/performance
```

#### Get Collaboration Patterns
```http
GET /analytics/collaboration-patterns
```

## Frontend Components

### 1. AgentNetwork Component

**Location:** `frontend/src/pages/MultiAgent/AgentNetwork.jsx`

**Features:**
- Real-time agent status monitoring
- Agent activation/deactivation
- Performance metrics visualization
- Network graph view
- Auto-refresh capability

**Usage:**
```jsx
import AgentNetwork from './pages/MultiAgent/AgentNetwork';

<AgentNetwork />
```

### 2. WorkflowDashboard Component

**Location:** `frontend/src/pages/MultiAgent/WorkflowDashboard.jsx`

**Features:**
- Start new workflows
- Monitor workflow progress
- Task status visualization
- Stepper component for task flow
- Real-time progress updates

**Usage:**
```jsx
import WorkflowDashboard from './pages/MultiAgent/WorkflowDashboard';

<WorkflowDashboard />
```

### 3. API Integration

**Location:** `frontend/src/services/api.js`

```javascript
import { masAPI } from './services/api';

// Start workflow
const result = await masAPI.startCareerTransition({
  worker_id: 1,
  target_role: 'Data Scientist'
});

// Get progress
const progress = await masAPI.getWorkflowProgress(workflowId);

// Get agent network
const network = await masAPI.getAgentNetwork();

// List agents
const agents = await masAPI.listAgents();
```

## Usage Examples

### Example 1: Register Agents and Start Workflow

```python
from backend.app.core.multi_agent_system import MultiAgentCoordinator
from backend.app.agents.gap_analyzer_agent import GapAnalyzerAgent
from backend.app.agents.opportunity_scout_agent import OpportunityScoutAgent
from backend.app.core.mas_workflows import CareerTransitionWorkflow

# Create coordinator
coordinator = MultiAgentCoordinator()

# Register agents
gap_analyzer = GapAnalyzerAgent(agent_id="gap_analyzer", agent_type="gap_analyzer")
opportunity_scout = OpportunityScoutAgent(agent_id="opportunity_scout", agent_type="opportunity_scout")

coordinator.register_agent(gap_analyzer)
coordinator.register_agent(opportunity_scout)

# Start workflow
workflow = CareerTransitionWorkflow(coordinator)
result = workflow.execute(worker_id=1, target_role="Data Scientist")

# Monitor progress
progress = workflow.get_progress()
print(f"Progress: {progress['progress_percentage']}%")

# Get results
results = workflow.get_results()
print(f"Final plan: {results['final_plan']}")
```

### Example 2: Agent Collaboration

```python
# Agent requests collaboration
conversation_id = coordinator.request_collaboration(
    requester_id="learning_strategist",
    task_description="Create comprehensive learning path",
    required_agents=["gap_analyzer", "opportunity_scout", "teaching_coach"]
)

# Agents communicate through shared environment
gap_analyzer.write_shared_knowledge(
    key=f"collab:{conversation_id}:gap_data",
    value={"missing_skills": ["Python", "ML"]}
)

# Other agents read and contribute
gap_data = opportunity_scout.read_shared_knowledge(f"collab:{conversation_id}:gap_data")
```

### Example 3: Task Delegation

```python
# Agent delegates subtask to another agent
task_id = learning_strategist.delegate_subtask(
    task_name="Find Learning Resources",
    task_description="Find best resources for Python and ML",
    required_capabilities=["content_curation"],
    input_data={"skills": ["Python", "ML"], "difficulty": "intermediate"}
)

# Monitor subtask progress
task_status = coordinator.tasks[task_id].status
```

## Performance Metrics

### System Metrics
- Total writes to shared environment
- Writes per agent
- Total events published
- Message queue size
- Active conversations

### Agent Metrics
- Tasks completed
- Success rate (%)
- Average response time (seconds)
- Messages sent/received
- Collaborations participated in

### Workflow Metrics
- Total workflows executed
- Active workflows
- Average completion time
- Failure rate
- Tasks per workflow

## Best Practices

### 1. Agent Design
- ✅ Give agents clear, focused capabilities
- ✅ Make agents stateless when possible
- ✅ Use shared environment for state
- ✅ Handle message timeouts gracefully
- ❌ Don't create circular dependencies
- ❌ Don't block on synchronous operations

### 2. Workflow Design
- ✅ Break complex problems into subtasks
- ✅ Define clear task dependencies
- ✅ Use appropriate task priorities
- ✅ Handle task failures gracefully
- ❌ Don't create deadlocks with circular dependencies
- ❌ Don't use workflows for simple single-agent tasks

### 3. Communication
- ✅ Use appropriate message types
- ✅ Set realistic deadlines
- ✅ Include conversation IDs for tracking
- ✅ Use priority for urgent messages
- ❌ Don't spam messages
- ❌ Don't ignore required_response flag

### 4. Shared Environment
- ✅ Use clear, hierarchical key naming
- ✅ Clean up old data periodically
- ✅ Subscribe to relevant changes only
- ✅ Release locks promptly
- ❌ Don't store large objects
- ❌ Don't hold locks indefinitely

## Troubleshooting

### Common Issues

**Issue: Workflow stuck in "in_progress"**
- Check if all required agents are active
- Verify agents have required capabilities
- Check for circular task dependencies
- Review task failure errors

**Issue: Messages not being delivered**
- Verify agent is registered with coordinator
- Check if agent is active
- Verify message queue is being processed
- Check for message routing errors

**Issue: Shared environment not updating**
- Verify agent has MAS enabled
- Check for thread lock issues
- Verify write permissions
- Check event log for errors

**Issue: Poor agent performance**
- Review agent success rates
- Check average response times
- Monitor message queue sizes
- Analyze collaboration patterns

## Future Enhancements

### Planned Features
1. **Agent Learning**: Agents learn from past interactions
2. **Dynamic Capability Discovery**: Agents advertise new capabilities
3. **Load Balancing**: Distribute tasks across multiple agent instances
4. **Fault Tolerance**: Automatic recovery from agent failures
5. **Real-time Streaming**: WebSocket support for real-time updates
6. **Agent Marketplace**: Discover and register community agents
7. **Visual Workflow Builder**: Drag-and-drop workflow creation
8. **Advanced Negotiations**: Market-based task allocation

## Conclusion

The Multi-Agent System provides a powerful framework for building complex, distributed AI applications. By enabling agents to communicate, coordinate, and collaborate, it allows emergent collective intelligence that can solve problems beyond the capability of any single agent.

**Key Takeaways:**
- Distributed control with no single point of failure
- Shared environment enables seamless data flow
- Message-based communication allows flexible coordination
- Task distribution leverages agent specialization
- Collective intelligence emerges from agent interactions

For more information, see the code files:
- `backend/app/core/multi_agent_system.py` - Core MAS implementation
- `backend/app/core/mas_workflows.py` - Example workflows
- `backend/app/api/multi_agent.py` - API endpoints
- `backend/app/agents/base_agent.py` - Enhanced base agent
- `frontend/src/pages/MultiAgent/` - UI components
