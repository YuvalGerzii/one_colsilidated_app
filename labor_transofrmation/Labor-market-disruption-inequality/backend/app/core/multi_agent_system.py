"""
Multi-Agent System (MAS) Core
Advanced agent coordination with shared environment and distributed control

Features:
- Shared environment (blackboard pattern) for agent state
- Agent-to-agent communication and negotiation
- Distributed task distribution and workflow management
- Collective intelligence through collaboration
- Competition and consensus mechanisms
"""
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
import uuid
import json
from collections import defaultdict
import threading
from queue import PriorityQueue


class MessageType(Enum):
    """Types of inter-agent messages"""
    REQUEST = "request"
    RESPONSE = "response"
    INFORM = "inform"
    QUERY = "query"
    PROPOSE = "propose"
    ACCEPT = "accept"
    REJECT = "reject"
    DELEGATE = "delegate"
    COMPLETE = "complete"
    NEGOTIATE = "negotiate"


class TaskStatus(Enum):
    """Status of distributed tasks"""
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class AgentMessage:
    """Enhanced message format for inter-agent communication"""
    id: str
    from_agent: str
    to_agent: str
    message_type: MessageType
    payload: Dict
    timestamp: datetime
    priority: int = 5  # 1=highest, 10=lowest
    requires_response: bool = False
    conversation_id: Optional[str] = None
    in_reply_to: Optional[str] = None
    deadline: Optional[datetime] = None

    def to_dict(self):
        return {
            'id': self.id,
            'from_agent': self.from_agent,
            'to_agent': self.to_agent,
            'message_type': self.message_type.value,
            'payload': self.payload,
            'timestamp': self.timestamp.isoformat(),
            'priority': self.priority,
            'requires_response': self.requires_response,
            'conversation_id': self.conversation_id,
            'in_reply_to': self.in_reply_to,
            'deadline': self.deadline.isoformat() if self.deadline else None,
        }


@dataclass
class DistributedTask:
    """Task in multi-agent workflow"""
    task_id: str
    name: str
    description: str
    required_capabilities: List[str]
    input_data: Dict
    output_data: Optional[Dict] = None
    status: TaskStatus = TaskStatus.PENDING
    assigned_agent: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    priority: int = 5
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Any] = None
    error: Optional[str] = None


class SharedEnvironment:
    """
    Blackboard pattern - shared knowledge base for all agents

    Agents can:
    - Read shared state
    - Write updates
    - Subscribe to changes
    - Publish events
    - Lock resources
    """

    def __init__(self):
        self.knowledge_base: Dict[str, Any] = {}
        self.subscribers: Dict[str, List[Callable]] = defaultdict(list)
        self.locks: Dict[str, str] = {}  # resource_id -> agent_id
        self.event_log: List[Dict] = []
        self.metrics: Dict[str, Any] = defaultdict(int)
        self._lock = threading.Lock()

    def read(self, key: str, default: Any = None) -> Any:
        """Read from shared knowledge base"""
        return self.knowledge_base.get(key, default)

    def write(self, key: str, value: Any, agent_id: str) -> bool:
        """Write to shared knowledge base"""
        with self._lock:
            old_value = self.knowledge_base.get(key)
            self.knowledge_base[key] = value

            # Log the change
            self.event_log.append({
                'timestamp': datetime.now().isoformat(),
                'agent_id': agent_id,
                'action': 'write',
                'key': key,
                'old_value': old_value,
                'new_value': value,
            })

            # Notify subscribers
            self._notify_subscribers(key, value, agent_id)

            # Update metrics
            self.metrics['total_writes'] += 1
            self.metrics[f'writes_by_{agent_id}'] += 1

            return True

    def update(self, updates: Dict[str, Any], agent_id: str) -> bool:
        """Batch update multiple keys"""
        with self._lock:
            for key, value in updates.items():
                self.write(key, value, agent_id)
            return True

    def subscribe(self, key: str, callback: Callable):
        """Subscribe to changes on a key"""
        self.subscribers[key].append(callback)

    def _notify_subscribers(self, key: str, value: Any, agent_id: str):
        """Notify all subscribers of a change"""
        for callback in self.subscribers.get(key, []):
            try:
                callback(key, value, agent_id)
            except Exception as e:
                print(f"Error in subscriber callback: {e}")

    def acquire_lock(self, resource_id: str, agent_id: str, timeout: int = 30) -> bool:
        """Acquire exclusive lock on a resource"""
        with self._lock:
            if resource_id not in self.locks:
                self.locks[resource_id] = agent_id
                self.event_log.append({
                    'timestamp': datetime.now().isoformat(),
                    'agent_id': agent_id,
                    'action': 'lock_acquired',
                    'resource_id': resource_id,
                })
                return True
            return False

    def release_lock(self, resource_id: str, agent_id: str) -> bool:
        """Release lock on a resource"""
        with self._lock:
            if self.locks.get(resource_id) == agent_id:
                del self.locks[resource_id]
                self.event_log.append({
                    'timestamp': datetime.now().isoformat(),
                    'agent_id': agent_id,
                    'action': 'lock_released',
                    'resource_id': resource_id,
                })
                return True
            return False

    def publish_event(self, event_type: str, data: Dict, agent_id: str):
        """Publish event to shared environment"""
        event = {
            'id': str(uuid.uuid4()),
            'timestamp': datetime.now().isoformat(),
            'agent_id': agent_id,
            'event_type': event_type,
            'data': data,
        }
        self.event_log.append(event)
        self._notify_subscribers(f'event:{event_type}', event, agent_id)

    def get_recent_events(self, limit: int = 100, event_type: Optional[str] = None) -> List[Dict]:
        """Get recent events from log"""
        events = self.event_log[-limit:]
        if event_type:
            events = [e for e in events if e.get('event_type') == event_type]
        return events

    def get_metrics(self) -> Dict[str, Any]:
        """Get environment metrics"""
        return dict(self.metrics)

    def clear(self):
        """Clear all shared state (use with caution)"""
        with self._lock:
            self.knowledge_base.clear()
            self.locks.clear()
            self.event_log.clear()
            self.metrics.clear()


class MultiAgentCoordinator:
    """
    Advanced coordinator for multi-agent systems

    Features:
    - Task distribution and workflow management
    - Agent communication routing
    - Collective decision-making
    - Competition and negotiation
    - Performance monitoring
    """

    def __init__(self, shared_env: Optional[SharedEnvironment] = None):
        self.agents: Dict[str, Any] = {}  # agent_id -> agent instance
        self.shared_env = shared_env or SharedEnvironment()
        self.message_queue = PriorityQueue()
        self.conversations: Dict[str, List[AgentMessage]] = defaultdict(list)
        self.tasks: Dict[str, DistributedTask] = {}
        self.workflows: Dict[str, List[str]] = {}  # workflow_id -> task_ids
        self.performance_metrics: Dict[str, Dict] = defaultdict(dict)
        self._lock = threading.Lock()

    def register_agent(self, agent: Any):
        """Register agent with coordinator"""
        self.agents[agent.agent_id] = agent

        # Give agent access to shared environment
        agent.shared_env = self.shared_env
        agent.coordinator = self

        # Initialize performance metrics
        self.performance_metrics[agent.agent_id] = {
            'tasks_completed': 0,
            'messages_sent': 0,
            'messages_received': 0,
            'collaborations': 0,
            'success_rate': 0.0,
            'avg_response_time': 0.0,
        }

        # Publish agent registration event
        self.shared_env.publish_event('agent_registered', {
            'agent_id': agent.agent_id,
            'agent_type': agent.agent_type,
            'capabilities': agent.capabilities,
        }, 'coordinator')

    def send_message(self, message: AgentMessage):
        """Send message between agents"""
        # Add to priority queue
        self.message_queue.put((message.priority, message.timestamp, message))

        # Store in conversation
        if message.conversation_id:
            self.conversations[message.conversation_id].append(message)

        # Update metrics
        self.performance_metrics[message.from_agent]['messages_sent'] += 1
        if message.to_agent in self.agents:
            self.performance_metrics[message.to_agent]['messages_received'] += 1

        # Publish event
        self.shared_env.publish_event('message_sent', {
            'from': message.from_agent,
            'to': message.to_agent,
            'type': message.message_type.value,
        }, message.from_agent)

    def process_messages(self, max_messages: int = 10):
        """Process pending messages"""
        processed = 0
        while not self.message_queue.empty() and processed < max_messages:
            _, _, message = self.message_queue.get()

            # Deliver to recipient agent
            if message.to_agent in self.agents:
                agent = self.agents[message.to_agent]
                if hasattr(agent, 'receive_message'):
                    agent.receive_message(message)

            processed += 1

    def distribute_task(self, task: DistributedTask) -> bool:
        """
        Distribute task to best available agent

        Uses capability matching and performance scoring
        """
        with self._lock:
            # Store task
            self.tasks[task.task_id] = task

            # Find capable agents
            capable_agents = []
            for agent_id, agent in self.agents.items():
                agent_caps = set(agent.capabilities)
                required_caps = set(task.required_capabilities)
                if required_caps.issubset(agent_caps):
                    capable_agents.append(agent_id)

            if not capable_agents:
                task.status = TaskStatus.FAILED
                task.error = "No capable agents available"
                return False

            # Score agents based on performance
            best_agent = max(capable_agents, key=lambda a: (
                self.performance_metrics[a]['success_rate'],
                -self.performance_metrics[a]['avg_response_time'],
            ))

            # Assign task
            task.assigned_agent = best_agent
            task.status = TaskStatus.ASSIGNED

            # Send task to agent
            message = AgentMessage(
                id=str(uuid.uuid4()),
                from_agent='coordinator',
                to_agent=best_agent,
                message_type=MessageType.REQUEST,
                payload={
                    'task_id': task.task_id,
                    'action': 'execute_task',
                    'task': {
                        'name': task.name,
                        'description': task.description,
                        'input_data': task.input_data,
                    },
                },
                timestamp=datetime.now(),
                priority=task.priority,
                requires_response=True,
            )
            self.send_message(message)

            # Publish event
            self.shared_env.publish_event('task_assigned', {
                'task_id': task.task_id,
                'agent_id': best_agent,
            }, 'coordinator')

            return True

    def create_workflow(self, workflow_id: str, tasks: List[DistributedTask]) -> bool:
        """
        Create multi-task workflow with dependencies

        Tasks are executed based on dependency graph
        """
        with self._lock:
            task_ids = []

            for task in tasks:
                self.tasks[task.task_id] = task
                task_ids.append(task.task_id)

            self.workflows[workflow_id] = task_ids

            # Start executing tasks without dependencies
            for task in tasks:
                if not task.dependencies:
                    self.distribute_task(task)

            return True

    def check_workflow_progress(self, workflow_id: str) -> Dict:
        """Check progress of a workflow"""
        if workflow_id not in self.workflows:
            return {'error': 'Workflow not found'}

        task_ids = self.workflows[workflow_id]
        tasks = [self.tasks[tid] for tid in task_ids]

        total = len(tasks)
        completed = sum(1 for t in tasks if t.status == TaskStatus.COMPLETED)
        failed = sum(1 for t in tasks if t.status == TaskStatus.FAILED)
        in_progress = sum(1 for t in tasks if t.status == TaskStatus.IN_PROGRESS)

        return {
            'workflow_id': workflow_id,
            'total_tasks': total,
            'completed': completed,
            'failed': failed,
            'in_progress': in_progress,
            'progress_percentage': (completed / total * 100) if total > 0 else 0,
            'status': 'completed' if completed == total else 'failed' if failed > 0 else 'in_progress',
            'tasks': [
                {
                    'task_id': t.task_id,
                    'name': t.name,
                    'status': t.status.value,
                    'assigned_agent': t.assigned_agent,
                }
                for t in tasks
            ],
        }

    def request_collaboration(self, requester_id: str, task_description: str,
                            required_agents: List[str]) -> str:
        """
        Request collaboration between multiple agents

        Returns conversation_id for tracking
        """
        conversation_id = str(uuid.uuid4())

        # Send collaboration request to all required agents
        for agent_id in required_agents:
            if agent_id in self.agents:
                message = AgentMessage(
                    id=str(uuid.uuid4()),
                    from_agent=requester_id,
                    to_agent=agent_id,
                    message_type=MessageType.REQUEST,
                    payload={
                        'action': 'collaborate',
                        'task_description': task_description,
                        'collaborators': required_agents,
                    },
                    timestamp=datetime.now(),
                    conversation_id=conversation_id,
                    requires_response=True,
                )
                self.send_message(message)

        # Update collaboration metrics
        for agent_id in required_agents:
            if agent_id in self.performance_metrics:
                self.performance_metrics[agent_id]['collaborations'] += 1

        return conversation_id

    def negotiate(self, agent_ids: List[str], negotiation_topic: str,
                 proposals: Dict[str, Any]) -> Dict:
        """
        Facilitate negotiation between agents

        Agents can propose, counter-propose, accept, or reject
        """
        conversation_id = str(uuid.uuid4())

        # Initiate negotiation
        for agent_id in agent_ids:
            message = AgentMessage(
                id=str(uuid.uuid4()),
                from_agent='coordinator',
                to_agent=agent_id,
                message_type=MessageType.NEGOTIATE,
                payload={
                    'topic': negotiation_topic,
                    'participants': agent_ids,
                    'initial_proposals': proposals,
                },
                timestamp=datetime.now(),
                conversation_id=conversation_id,
                requires_response=True,
            )
            self.send_message(message)

        return {
            'conversation_id': conversation_id,
            'status': 'initiated',
            'participants': agent_ids,
        }

    def vote(self, agent_ids: List[str], question: str, options: List[str]) -> Dict:
        """
        Collective decision through voting

        Returns winning option based on agent votes
        """
        conversation_id = str(uuid.uuid4())
        votes: Dict[str, str] = {}

        # Request votes from all agents
        for agent_id in agent_ids:
            message = AgentMessage(
                id=str(uuid.uuid4()),
                from_agent='coordinator',
                to_agent=agent_id,
                message_type=MessageType.QUERY,
                payload={
                    'action': 'vote',
                    'question': question,
                    'options': options,
                },
                timestamp=datetime.now(),
                conversation_id=conversation_id,
                requires_response=True,
            )
            self.send_message(message)

        # In practice, collect votes asynchronously
        # For now, return structure
        return {
            'conversation_id': conversation_id,
            'question': question,
            'options': options,
            'participants': agent_ids,
            'status': 'voting_in_progress',
        }

    def get_consensus(self, agent_ids: List[str], topic: str,
                     initial_proposals: Dict[str, Any]) -> Dict:
        """
        Reach consensus through iterative discussion

        Agents exchange proposals until agreement or timeout
        """
        conversation_id = str(uuid.uuid4())

        # Write initial state to shared environment
        consensus_key = f'consensus:{conversation_id}'
        self.shared_env.write(consensus_key, {
            'topic': topic,
            'proposals': initial_proposals,
            'participants': agent_ids,
            'round': 1,
            'status': 'in_progress',
        }, 'coordinator')

        # Notify all agents
        for agent_id in agent_ids:
            message = AgentMessage(
                id=str(uuid.uuid4()),
                from_agent='coordinator',
                to_agent=agent_id,
                message_type=MessageType.INFORM,
                payload={
                    'action': 'consensus_building',
                    'consensus_key': consensus_key,
                },
                timestamp=datetime.now(),
                conversation_id=conversation_id,
            )
            self.send_message(message)

        return {
            'conversation_id': conversation_id,
            'consensus_key': consensus_key,
            'status': 'initiated',
        }

    def get_system_status(self) -> Dict:
        """Get comprehensive system status"""
        return {
            'timestamp': datetime.now().isoformat(),
            'agents': {
                'total': len(self.agents),
                'active': sum(1 for a in self.agents.values() if a.active),
                'by_type': self._count_by_type(),
            },
            'tasks': {
                'total': len(self.tasks),
                'by_status': self._count_tasks_by_status(),
            },
            'workflows': {
                'total': len(self.workflows),
                'active': sum(1 for wid in self.workflows if self._is_workflow_active(wid)),
            },
            'messages': {
                'pending': self.message_queue.qsize(),
                'conversations': len(self.conversations),
            },
            'shared_environment': self.shared_env.get_metrics(),
            'performance': {
                agent_id: metrics
                for agent_id, metrics in self.performance_metrics.items()
            },
        }

    def _count_by_type(self) -> Dict[str, int]:
        """Count agents by type"""
        counts = defaultdict(int)
        for agent in self.agents.values():
            counts[agent.agent_type] += 1
        return dict(counts)

    def _count_tasks_by_status(self) -> Dict[str, int]:
        """Count tasks by status"""
        counts = defaultdict(int)
        for task in self.tasks.values():
            counts[task.status.value] += 1
        return dict(counts)

    def _is_workflow_active(self, workflow_id: str) -> bool:
        """Check if workflow is still active"""
        task_ids = self.workflows.get(workflow_id, [])
        tasks = [self.tasks[tid] for tid in task_ids if tid in self.tasks]
        return any(t.status in [TaskStatus.PENDING, TaskStatus.ASSIGNED, TaskStatus.IN_PROGRESS]
                  for t in tasks)

    def visualize_agent_network(self) -> Dict:
        """
        Generate network visualization data

        Shows agent interactions and collaborations
        """
        nodes = []
        edges = []

        # Create nodes for each agent
        for agent_id, agent in self.agents.items():
            nodes.append({
                'id': agent_id,
                'type': agent.agent_type,
                'capabilities': agent.capabilities,
                'active': agent.active,
                'metrics': self.performance_metrics[agent_id],
            })

        # Create edges from message history
        message_counts = defaultdict(int)
        for messages in self.conversations.values():
            for msg in messages:
                key = (msg.from_agent, msg.to_agent)
                message_counts[key] += 1

        for (from_agent, to_agent), count in message_counts.items():
            edges.append({
                'from': from_agent,
                'to': to_agent,
                'weight': count,
                'type': 'communication',
            })

        return {
            'nodes': nodes,
            'edges': edges,
            'timestamp': datetime.now().isoformat(),
        }
