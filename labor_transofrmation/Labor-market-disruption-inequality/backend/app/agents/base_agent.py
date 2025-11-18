"""
Base Agent Class for Multi-Agent Workforce Transition System
All specialized agents inherit from this base
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass
import uuid

# Import MAS types - will be set by coordinator if using MAS
try:
    from backend.app.core.multi_agent_system import (
        AgentMessage as MASAgentMessage,
        MessageType,
        SharedEnvironment,
        MultiAgentCoordinator
    )
    MAS_AVAILABLE = True
except ImportError:
    MAS_AVAILABLE = False
    MASAgentMessage = None
    MessageType = None
    SharedEnvironment = None
    MultiAgentCoordinator = None

@dataclass
class AgentMessage:
    """Message format for inter-agent communication (legacy)"""
    id: str
    from_agent: str
    to_agent: str
    message_type: str
    payload: Dict
    timestamp: datetime
    priority: int = 5  # 1=highest, 10=lowest
    requires_response: bool = False

@dataclass
class AgentResponse:
    """Standardized agent response format"""
    agent_id: str
    agent_type: str
    status: str  # success, partial, failed
    data: Any
    confidence: float  # 0-1
    recommendations: List[str]
    next_steps: List[str]
    timestamp: datetime
    metadata: Dict

class BaseAgent(ABC):
    """Base class for all agents in the system"""

    def __init__(self, agent_id: str, agent_type: str):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.message_queue: List[AgentMessage] = []
        self.active = True
        self.capabilities: List[str] = []
        self.performance_metrics = {
            'tasks_completed': 0,
            'success_rate': 0.0,
            'avg_response_time': 0.0
        }

        # Multi-Agent System integration (set by coordinator)
        self.shared_env: Optional[Any] = None  # SharedEnvironment instance
        self.coordinator: Optional[Any] = None  # MultiAgentCoordinator instance
        self.mas_enabled = False

    @abstractmethod
    def process_task(self, task: Dict) -> AgentResponse:
        """
        Process a task assigned to this agent

        Args:
            task: Task details and parameters

        Returns:
            AgentResponse with results
        """
        pass

    @abstractmethod
    def analyze(self, data: Dict) -> Dict:
        """
        Analyze provided data according to agent's specialization

        Args:
            data: Input data for analysis

        Returns:
            Analysis results
        """
        pass

    def send_message(self, to_agent: str, message_type: str, payload: Dict,
                    priority: int = 5, requires_response: bool = False) -> AgentMessage:
        """Send message to another agent"""
        message = AgentMessage(
            id=str(uuid.uuid4()),
            from_agent=self.agent_id,
            to_agent=to_agent,
            message_type=message_type,
            payload=payload,
            timestamp=datetime.now(),
            priority=priority,
            requires_response=requires_response
        )
        return message

    def receive_message(self, message: Any):
        """Receive and queue message from another agent (supports both legacy and MAS)"""
        self.message_queue.append(message)
        # Sort by priority
        self.message_queue.sort(key=lambda m: m.priority)

    def process_messages(self) -> List[AgentResponse]:
        """Process all queued messages"""
        responses = []
        while self.message_queue:
            message = self.message_queue.pop(0)
            response = self._handle_message(message)
            if response:
                responses.append(response)
        return responses

    def _handle_message(self, message: AgentMessage) -> Optional[AgentResponse]:
        """Handle individual message (can be overridden by subclasses)"""
        # Default implementation
        return None

    def update_metrics(self, success: bool, response_time: float):
        """Update agent performance metrics"""
        self.performance_metrics['tasks_completed'] += 1

        # Update success rate
        total = self.performance_metrics['tasks_completed']
        current_successes = self.performance_metrics['success_rate'] * (total - 1)
        new_successes = current_successes + (1 if success else 0)
        self.performance_metrics['success_rate'] = new_successes / total

        # Update average response time
        current_avg = self.performance_metrics['avg_response_time']
        self.performance_metrics['avg_response_time'] = (
            (current_avg * (total - 1) + response_time) / total
        )

    def get_capabilities(self) -> List[str]:
        """Return list of agent capabilities"""
        return self.capabilities

    def get_status(self) -> Dict:
        """Return agent status information"""
        return {
            'agent_id': self.agent_id,
            'agent_type': self.agent_type,
            'active': self.active,
            'capabilities': self.capabilities,
            'queued_messages': len(self.message_queue),
            'performance': self.performance_metrics,
            'mas_enabled': self.mas_enabled
        }

    # ===== Multi-Agent System Methods =====

    def enable_mas(self, shared_env: Any, coordinator: Any):
        """Enable Multi-Agent System features for this agent"""
        self.shared_env = shared_env
        self.coordinator = coordinator
        self.mas_enabled = True

    def read_shared_knowledge(self, key: str, default: Any = None) -> Any:
        """Read from shared environment"""
        if not self.mas_enabled or not self.shared_env:
            return default
        return self.shared_env.read(key, default)

    def write_shared_knowledge(self, key: str, value: Any) -> bool:
        """Write to shared environment"""
        if not self.mas_enabled or not self.shared_env:
            return False
        return self.shared_env.write(key, value, self.agent_id)

    def publish_result(self, result_key: str, result_data: Any):
        """Publish task result to shared environment"""
        if self.mas_enabled and self.shared_env:
            self.write_shared_knowledge(result_key, result_data)
            self.shared_env.publish_event('task_completed', {
                'agent_id': self.agent_id,
                'result_key': result_key,
            }, self.agent_id)

    def subscribe_to_changes(self, key: str, callback: callable):
        """Subscribe to changes in shared environment"""
        if self.mas_enabled and self.shared_env:
            self.shared_env.subscribe(key, callback)

    def send_mas_message(self, to_agent: str, message_type: Any, payload: Dict,
                         priority: int = 5, requires_response: bool = False):
        """Send message through MAS coordinator"""
        if not self.mas_enabled or not self.coordinator or not MAS_AVAILABLE:
            return None

        message = MASAgentMessage(
            id=str(uuid.uuid4()),
            from_agent=self.agent_id,
            to_agent=to_agent,
            message_type=message_type,
            payload=payload,
            timestamp=datetime.now(),
            priority=priority,
            requires_response=requires_response
        )
        self.coordinator.send_message(message)
        return message

    def request_collaboration(self, task_description: str, required_agents: List[str]) -> str:
        """Request collaboration with other agents"""
        if not self.mas_enabled or not self.coordinator:
            return ""

        return self.coordinator.request_collaboration(
            self.agent_id,
            task_description,
            required_agents
        )

    def delegate_subtask(self, task_name: str, task_description: str,
                        required_capabilities: List[str], input_data: Dict) -> Optional[str]:
        """Delegate a subtask to another capable agent"""
        if not self.mas_enabled or not self.coordinator or not MAS_AVAILABLE:
            return None

        from backend.app.core.multi_agent_system import DistributedTask, TaskStatus

        task = DistributedTask(
            task_id=str(uuid.uuid4()),
            name=task_name,
            description=task_description,
            required_capabilities=required_capabilities,
            input_data=input_data,
            status=TaskStatus.PENDING
        )

        success = self.coordinator.distribute_task(task)
        return task.task_id if success else None

class AgentCoordinator:
    """
    Coordinates multiple agents and manages inter-agent communication
    """

    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.message_bus: List[AgentMessage] = []
        self.task_queue: List[Dict] = []

    def register_agent(self, agent: BaseAgent):
        """Register a new agent with the coordinator"""
        self.agents[agent.agent_id] = agent

    def unregister_agent(self, agent_id: str):
        """Remove agent from coordination"""
        if agent_id in self.agents:
            del self.agents[agent_id]

    def route_message(self, message: AgentMessage):
        """Route message to appropriate agent"""
        if message.to_agent in self.agents:
            self.agents[message.to_agent].receive_message(message)
        else:
            # Broadcast to all capable agents
            self.message_bus.append(message)

    def assign_task(self, task: Dict, preferred_agent: Optional[str] = None) -> List[AgentResponse]:
        """
        Assign task to appropriate agent(s)

        Args:
            task: Task to be completed
            preferred_agent: Specific agent ID to use, or None for auto-selection

        Returns:
            List of responses from agents
        """
        if preferred_agent and preferred_agent in self.agents:
            # Assign to specific agent
            agent = self.agents[preferred_agent]
            return [agent.process_task(task)]
        else:
            # Find capable agents
            task_type = task.get('type', 'unknown')
            capable_agents = [
                agent for agent in self.agents.values()
                if task_type in agent.get_capabilities()
            ]

            if not capable_agents:
                # No capable agents, queue task
                self.task_queue.append(task)
                return []

            # Assign to best agent (by success rate)
            best_agent = max(
                capable_agents,
                key=lambda a: a.performance_metrics['success_rate']
            )

            return [best_agent.process_task(task)]

    def orchestrate_multi_agent_task(self, task: Dict, agent_sequence: List[str]) -> List[AgentResponse]:
        """
        Orchestrate task that requires multiple agents in sequence

        Args:
            task: Initial task
            agent_sequence: Ordered list of agent IDs to process task

        Returns:
            List of all agent responses
        """
        responses = []
        current_data = task

        for agent_id in agent_sequence:
            if agent_id not in self.agents:
                continue

            agent = self.agents[agent_id]
            response = agent.process_task(current_data)
            responses.append(response)

            # Use output as input for next agent
            if response.status == 'success':
                current_data['previous_results'] = response.data

        return responses

    def get_system_status(self) -> Dict:
        """Get status of entire multi-agent system"""
        return {
            'total_agents': len(self.agents),
            'active_agents': sum(1 for a in self.agents.values() if a.active),
            'queued_tasks': len(self.task_queue),
            'pending_messages': len(self.message_bus),
            'agents': {
                agent_id: agent.get_status()
                for agent_id, agent in self.agents.items()
            }
        }

    def process_all_messages(self):
        """Process all pending messages in the system"""
        for agent in self.agents.values():
            agent.process_messages()

        # Process message bus
        while self.message_bus:
            message = self.message_bus.pop(0)
            self.route_message(message)

    def get_agent_recommendations(self, context: Dict) -> List[str]:
        """
        Get recommendations from all agents about what to do next

        Args:
            context: Current situation context

        Returns:
            Aggregated recommendations from all agents
        """
        recommendations = []

        for agent in self.agents.values():
            if hasattr(agent, 'get_recommendations'):
                agent_recs = agent.get_recommendations(context)
                recommendations.extend(agent_recs)

        return recommendations
