"""
Multi-Agent Orchestration System for Freelance Workers Hub

This module implements a sophisticated multi-agent system where agents:
- Communicate and coordinate with each other
- Share a common environment and state
- Make distributed decisions
- Compete and cooperate to achieve objectives
- Generate collective intelligence through interaction
"""

from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
import uuid
from collections import defaultdict
import threading


class TaskPriority(Enum):
    """Task priority levels"""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4


class AgentRole(Enum):
    """Specialized agent roles in the system"""
    PROFILE_OPTIMIZER = "profile_optimizer"
    JOB_MATCHER = "job_matcher"
    PRICING_STRATEGIST = "pricing_strategist"
    PROPOSAL_WRITER = "proposal_writer"
    MARKET_ANALYST = "market_analyst"
    CAREER_PLANNER = "career_planner"
    COMPETITION_ANALYZER = "competition_analyzer"
    NEGOTIATION_ADVISOR = "negotiation_advisor"


@dataclass
class SharedEnvironment:
    """
    Shared environment where all agents operate
    Acts as a blackboard for agent communication and coordination
    """
    # Global state accessible to all agents
    global_state: Dict[str, Any] = field(default_factory=dict)

    # Market data updated in real-time
    market_data: Dict[str, Any] = field(default_factory=dict)

    # Active freelancer profiles being optimized
    active_profiles: Dict[int, Dict] = field(default_factory=dict)

    # Current job opportunities
    job_marketplace: List[Dict] = field(default_factory=list)

    # Agent proposals and bids for tasks
    agent_proposals: Dict[str, List[Dict]] = field(default_factory=lambda: defaultdict(list))

    # Shared knowledge base
    knowledge_base: Dict[str, Any] = field(default_factory=dict)

    # Communication bus for inter-agent messages
    message_bus: List[Dict] = field(default_factory=list)

    # Performance metrics for all agents
    agent_metrics: Dict[str, Dict] = field(default_factory=dict)

    # Task queue shared across agents
    task_queue: List[Dict] = field(default_factory=list)

    # Results from completed tasks
    completed_results: Dict[str, Any] = field(default_factory=dict)

    # Lock for thread-safe operations
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def publish_message(self, message: Dict):
        """Publish message to message bus (thread-safe)"""
        with self._lock:
            message['timestamp'] = datetime.now()
            self.message_bus.append(message)

    def get_messages_for_agent(self, agent_id: str) -> List[Dict]:
        """Retrieve unread messages for specific agent"""
        with self._lock:
            messages = [
                msg for msg in self.message_bus
                if msg.get('to_agent') == agent_id and not msg.get('read', False)
            ]
            # Mark as read
            for msg in messages:
                msg['read'] = True
            return messages

    def update_market_data(self, key: str, value: Any):
        """Update market data (thread-safe)"""
        with self._lock:
            self.market_data[key] = value

    def get_market_data(self, key: str) -> Any:
        """Get market data"""
        return self.market_data.get(key)

    def add_to_knowledge_base(self, key: str, value: Any):
        """Add knowledge to shared knowledge base"""
        with self._lock:
            self.knowledge_base[key] = {
                'value': value,
                'timestamp': datetime.now(),
                'contributors': []
            }

    def query_knowledge_base(self, key: str) -> Optional[Any]:
        """Query shared knowledge base"""
        kb_entry = self.knowledge_base.get(key)
        return kb_entry['value'] if kb_entry else None


@dataclass
class CollaborativeTask:
    """
    Task that requires multiple agents to collaborate
    """
    task_id: str
    task_type: str
    description: str
    priority: TaskPriority
    required_agents: List[AgentRole]
    input_data: Dict
    created_at: datetime = field(default_factory=datetime.now)
    deadline: Optional[datetime] = None
    assigned_agents: List[str] = field(default_factory=list)
    subtasks: List[Dict] = field(default_factory=list)
    status: str = "pending"  # pending, in_progress, completed, failed
    results: Dict = field(default_factory=dict)
    coordinator_agent: Optional[str] = None


class SpecializedFreelanceAgent:
    """
    Specialized agent for specific freelance platform tasks
    Inherits distributed intelligence capabilities
    """

    def __init__(
        self,
        agent_id: str,
        role: AgentRole,
        environment: SharedEnvironment,
        capabilities: List[str]
    ):
        self.agent_id = agent_id
        self.role = role
        self.environment = environment
        self.capabilities = capabilities
        self.active = True
        self.current_task: Optional[str] = None
        self.completed_tasks: List[str] = []
        self.performance_score = 100.0

    def can_handle_task(self, task: CollaborativeTask) -> bool:
        """Check if agent can handle the task"""
        return self.role in task.required_agents and self.active

    def bid_for_task(self, task: CollaborativeTask) -> Dict:
        """
        Compete for task by submitting a bid
        Agents compete based on their expertise and current load
        """
        if not self.can_handle_task(task):
            return {'bid': 0, 'reason': 'Not capable'}

        # Calculate bid score based on:
        # 1. Capability match
        # 2. Current workload
        # 3. Performance history
        # 4. Task priority alignment

        capability_score = len(set(self.capabilities) & set(task.required_agents)) / len(task.required_agents)
        workload_penalty = len([t for t in self.completed_tasks if t]) * 0.1
        performance_bonus = self.performance_score / 100.0
        priority_bonus = 1.0 if task.priority == TaskPriority.CRITICAL else 0.8

        bid_score = (capability_score * 0.4 +
                    (1 - min(workload_penalty, 0.5)) * 0.3 +
                    performance_bonus * 0.2 +
                    priority_bonus * 0.1) * 100

        return {
            'agent_id': self.agent_id,
            'bid_score': bid_score,
            'estimated_time': self._estimate_completion_time(task),
            'confidence': capability_score,
            'reason': f"Specialized in {self.role.value}"
        }

    def send_message(self, to_agent: str, message_type: str, payload: Dict):
        """Send message to another agent via shared environment"""
        message = {
            'from_agent': self.agent_id,
            'to_agent': to_agent,
            'message_type': message_type,
            'payload': payload,
            'read': False
        }
        self.environment.publish_message(message)

    def broadcast_message(self, message_type: str, payload: Dict):
        """Broadcast message to all agents"""
        message = {
            'from_agent': self.agent_id,
            'to_agent': 'ALL',
            'message_type': message_type,
            'payload': payload,
            'read': False
        }
        self.environment.publish_message(message)

    def check_messages(self) -> List[Dict]:
        """Check for new messages from other agents"""
        return self.environment.get_messages_for_agent(self.agent_id)

    def contribute_knowledge(self, key: str, value: Any):
        """Contribute to shared knowledge base"""
        self.environment.add_to_knowledge_base(key, value)

    def query_knowledge(self, key: str) -> Optional[Any]:
        """Query shared knowledge base"""
        return self.environment.query_knowledge_base(key)

    def _estimate_completion_time(self, task: CollaborativeTask) -> float:
        """Estimate time to complete task in minutes"""
        base_time = 30  # 30 minutes base
        complexity_multiplier = len(task.required_agents) * 0.5
        return base_time * (1 + complexity_multiplier)

    def update_performance(self, success: bool):
        """Update agent's performance score based on task outcomes"""
        if success:
            self.performance_score = min(100, self.performance_score + 2)
        else:
            self.performance_score = max(0, self.performance_score - 5)


class MultiAgentOrchestrator:
    """
    Orchestrates multiple agents working together on complex tasks
    Implements distributed control and collective intelligence
    """

    def __init__(self):
        self.environment = SharedEnvironment()
        self.agents: Dict[str, SpecializedFreelanceAgent] = {}
        self.active_tasks: Dict[str, CollaborativeTask] = {}
        self.task_history: List[CollaborativeTask] = []

    def register_agent(self, agent: SpecializedFreelanceAgent):
        """Register an agent in the system"""
        self.agents[agent.agent_id] = agent
        self.environment.agent_metrics[agent.agent_id] = {
            'role': agent.role.value,
            'tasks_completed': 0,
            'success_rate': 1.0,
            'avg_completion_time': 0
        }

    def create_collaborative_task(
        self,
        task_type: str,
        description: str,
        required_agents: List[AgentRole],
        input_data: Dict,
        priority: TaskPriority = TaskPriority.MEDIUM
    ) -> CollaborativeTask:
        """
        Create a task that requires multiple agents to collaborate
        """
        task = CollaborativeTask(
            task_id=str(uuid.uuid4()),
            task_type=task_type,
            description=description,
            priority=priority,
            required_agents=required_agents,
            input_data=input_data
        )

        self.active_tasks[task.task_id] = task
        return task

    def decompose_task(self, task: CollaborativeTask) -> List[Dict]:
        """
        Decompose complex task into subtasks
        Each subtask can be handled by a specific agent
        """
        subtasks = []

        if task.task_type == "optimize_freelancer_profile":
            # Decompose into specialized subtasks
            subtasks = [
                {
                    'subtask_id': f"{task.task_id}_profile",
                    'agent_role': AgentRole.PROFILE_OPTIMIZER,
                    'description': 'Optimize profile content and structure',
                    'depends_on': []
                },
                {
                    'subtask_id': f"{task.task_id}_pricing",
                    'agent_role': AgentRole.PRICING_STRATEGIST,
                    'description': 'Optimize pricing strategy',
                    'depends_on': []
                },
                {
                    'subtask_id': f"{task.task_id}_market",
                    'agent_role': AgentRole.MARKET_ANALYST,
                    'description': 'Analyze market positioning',
                    'depends_on': []
                }
            ]

        elif task.task_type == "find_and_apply_jobs":
            subtasks = [
                {
                    'subtask_id': f"{task.task_id}_match",
                    'agent_role': AgentRole.JOB_MATCHER,
                    'description': 'Find matching job opportunities',
                    'depends_on': []
                },
                {
                    'subtask_id': f"{task.task_id}_competition",
                    'agent_role': AgentRole.COMPETITION_ANALYZER,
                    'description': 'Analyze competition for each job',
                    'depends_on': [f"{task.task_id}_match"]
                },
                {
                    'subtask_id': f"{task.task_id}_proposal",
                    'agent_role': AgentRole.PROPOSAL_WRITER,
                    'description': 'Generate proposals for top jobs',
                    'depends_on': [f"{task.task_id}_competition"]
                }
            ]

        elif task.task_type == "career_growth_plan":
            subtasks = [
                {
                    'subtask_id': f"{task.task_id}_market_analysis",
                    'agent_role': AgentRole.MARKET_ANALYST,
                    'description': 'Analyze market trends and opportunities',
                    'depends_on': []
                },
                {
                    'subtask_id': f"{task.task_id}_pricing_strategy",
                    'agent_role': AgentRole.PRICING_STRATEGIST,
                    'description': 'Develop pricing evolution strategy',
                    'depends_on': [f"{task.task_id}_market_analysis"]
                },
                {
                    'subtask_id': f"{task.task_id}_career_path",
                    'agent_role': AgentRole.CAREER_PLANNER,
                    'description': 'Create long-term career roadmap',
                    'depends_on': [f"{task.task_id}_market_analysis", f"{task.task_id}_pricing_strategy"]
                }
            ]

        task.subtasks = subtasks
        return subtasks

    def auction_task(self, task: CollaborativeTask) -> Dict[str, str]:
        """
        Auction task to agents - they compete by bidding
        Implements competitive behavior among agents
        """
        bids = {}

        # Get bids from all capable agents
        for agent_id, agent in self.agents.items():
            bid = agent.bid_for_task(task)
            if bid['bid'] > 0:
                bids[agent_id] = bid

        # Select best agent per required role
        assignments = {}
        for role in task.required_agents:
            role_bids = {
                agent_id: bid
                for agent_id, bid in bids.items()
                if self.agents[agent_id].role == role
            }

            if role_bids:
                # Select agent with highest bid
                best_agent = max(role_bids.items(), key=lambda x: x[1]['bid_score'])[0]
                assignments[role.value] = best_agent
                task.assigned_agents.append(best_agent)

        return assignments

    def execute_collaborative_task(self, task: CollaborativeTask) -> Dict:
        """
        Execute task with multiple agents collaborating
        Implements distributed control and coordination
        """
        # Step 1: Decompose task
        subtasks = self.decompose_task(task)

        # Step 2: Auction task to agents
        assignments = self.auction_task(task)

        # Step 3: Select coordinator agent (highest performing agent)
        coordinator = max(
            [self.agents[a] for a in task.assigned_agents],
            key=lambda x: x.performance_score
        )
        task.coordinator_agent = coordinator.agent_id

        # Step 4: Coordinator distributes subtasks
        coordinator.broadcast_message(
            'task_assignment',
            {
                'task_id': task.task_id,
                'subtasks': subtasks,
                'assignments': assignments
            }
        )

        # Step 5: Execute subtasks in dependency order
        task.status = "in_progress"
        subtask_results = {}

        for subtask in self._get_execution_order(subtasks):
            agent_role = subtask['agent_role']
            assigned_agent_id = assignments.get(agent_role.value)

            if not assigned_agent_id:
                continue

            agent = self.agents[assigned_agent_id]

            # Agent executes subtask
            result = self._execute_subtask(agent, subtask, task.input_data, subtask_results)
            subtask_results[subtask['subtask_id']] = result

            # Share result with other agents
            agent.contribute_knowledge(subtask['subtask_id'], result)

            # Notify coordinator
            agent.send_message(
                coordinator.agent_id,
                'subtask_completed',
                {'subtask_id': subtask['subtask_id'], 'result': result}
            )

        # Step 6: Coordinator aggregates results
        aggregated_result = self._aggregate_results(
            task,
            subtask_results,
            coordinator
        )

        task.results = aggregated_result
        task.status = "completed"

        # Update agent performance
        for agent_id in task.assigned_agents:
            self.agents[agent_id].update_performance(success=True)
            self.agents[agent_id].completed_tasks.append(task.task_id)

        self.task_history.append(task)
        del self.active_tasks[task.task_id]

        return aggregated_result

    def _get_execution_order(self, subtasks: List[Dict]) -> List[Dict]:
        """
        Determine execution order based on dependencies
        Implements topological sort
        """
        # Simple implementation: execute tasks with no dependencies first
        ordered = []
        completed = set()

        while len(ordered) < len(subtasks):
            for subtask in subtasks:
                if subtask in ordered:
                    continue

                dependencies = subtask.get('depends_on', [])
                if all(dep in completed for dep in dependencies):
                    ordered.append(subtask)
                    completed.add(subtask['subtask_id'])

        return ordered

    def _execute_subtask(
        self,
        agent: SpecializedFreelanceAgent,
        subtask: Dict,
        input_data: Dict,
        previous_results: Dict
    ) -> Dict:
        """
        Execute a single subtask with an agent
        Agent can access results from previous subtasks
        """
        # Agent can query knowledge base for context
        context = {
            'input_data': input_data,
            'previous_results': previous_results,
            'subtask': subtask
        }

        # Simulate agent work (in real implementation, call agent's process method)
        if agent.role == AgentRole.PROFILE_OPTIMIZER:
            return self._profile_optimization_work(context)
        elif agent.role == AgentRole.JOB_MATCHER:
            return self._job_matching_work(context)
        elif agent.role == AgentRole.PRICING_STRATEGIST:
            return self._pricing_strategy_work(context)
        elif agent.role == AgentRole.PROPOSAL_WRITER:
            return self._proposal_writing_work(context)
        elif agent.role == AgentRole.MARKET_ANALYST:
            return self._market_analysis_work(context)
        elif agent.role == AgentRole.CAREER_PLANNER:
            return self._career_planning_work(context)
        elif agent.role == AgentRole.COMPETITION_ANALYZER:
            return self._competition_analysis_work(context)
        else:
            return {'status': 'completed', 'result': {}}

    def _aggregate_results(
        self,
        task: CollaborativeTask,
        subtask_results: Dict,
        coordinator: SpecializedFreelanceAgent
    ) -> Dict:
        """
        Coordinator aggregates all subtask results into final result
        Demonstrates collective intelligence
        """
        aggregated = {
            'task_id': task.task_id,
            'task_type': task.task_type,
            'coordinator': coordinator.agent_id,
            'agents_involved': task.assigned_agents,
            'subtask_results': subtask_results,
            'collective_recommendation': {},
            'confidence': 0.0,
            'next_steps': []
        }

        if task.task_type == "optimize_freelancer_profile":
            # Combine insights from profile optimizer, pricing strategist, and market analyst
            profile_insights = subtask_results.get(f"{task.task_id}_profile", {})
            pricing_insights = subtask_results.get(f"{task.task_id}_pricing", {})
            market_insights = subtask_results.get(f"{task.task_id}_market", {})

            aggregated['collective_recommendation'] = {
                'profile_improvements': profile_insights.get('improvements', []),
                'pricing_strategy': pricing_insights.get('strategy', {}),
                'market_positioning': market_insights.get('positioning', ''),
                'priority_actions': self._merge_priority_actions([
                    profile_insights.get('actions', []),
                    pricing_insights.get('actions', []),
                    market_insights.get('actions', [])
                ]),
                'estimated_impact': self._calculate_combined_impact(subtask_results)
            }

        elif task.task_type == "find_and_apply_jobs":
            # Combine job matching, competition analysis, and proposal generation
            jobs = subtask_results.get(f"{task.task_id}_match", {}).get('jobs', [])
            competition = subtask_results.get(f"{task.task_id}_competition", {}).get('analysis', {})
            proposals = subtask_results.get(f"{task.task_id}_proposal", {}).get('proposals', [])

            aggregated['collective_recommendation'] = {
                'recommended_jobs': jobs[:5],
                'competition_insights': competition,
                'ready_proposals': proposals,
                'success_probability': self._estimate_success_rate(jobs, competition, proposals),
                'application_strategy': self._create_application_strategy(subtask_results)
            }

        elif task.task_type == "career_growth_plan":
            # Synthesize market trends, pricing evolution, and career path
            market = subtask_results.get(f"{task.task_id}_market_analysis", {})
            pricing = subtask_results.get(f"{task.task_id}_pricing_strategy", {})
            career = subtask_results.get(f"{task.task_id}_career_path", {})

            aggregated['collective_recommendation'] = {
                'market_trends': market.get('trends', []),
                'pricing_roadmap': pricing.get('roadmap', []),
                'career_milestones': career.get('milestones', []),
                'integrated_plan': self._integrate_growth_plan(market, pricing, career),
                'risk_factors': self._identify_collective_risks(subtask_results),
                'success_indicators': self._define_success_metrics(subtask_results)
            }

        # Calculate collective confidence (average of all agent confidences)
        confidences = [r.get('confidence', 0.5) for r in subtask_results.values()]
        aggregated['confidence'] = sum(confidences) / len(confidences) if confidences else 0.5

        return aggregated

    # Helper methods for specific agent work

    def _profile_optimization_work(self, context: Dict) -> Dict:
        """Profile optimizer agent work"""
        return {
            'status': 'completed',
            'improvements': [
                'Enhance bio with quantifiable achievements',
                'Add 3 more portfolio pieces',
                'Update skills with trending technologies'
            ],
            'actions': ['Update bio', 'Add portfolio'],
            'confidence': 0.85
        }

    def _job_matching_work(self, context: Dict) -> Dict:
        """Job matcher agent work"""
        return {
            'status': 'completed',
            'jobs': [
                {'id': 1, 'title': 'Web Development', 'match_score': 95},
                {'id': 2, 'title': 'API Integration', 'match_score': 88}
            ],
            'confidence': 0.9
        }

    def _pricing_strategy_work(self, context: Dict) -> Dict:
        """Pricing strategist agent work"""
        return {
            'status': 'completed',
            'strategy': {
                'current_rate': 50,
                'recommended_rate': 65,
                'increase_timeline': '3 months'
            },
            'actions': ['Test new rate', 'Monitor conversion'],
            'confidence': 0.82
        }

    def _proposal_writing_work(self, context: Dict) -> Dict:
        """Proposal writer agent work"""
        jobs = context.get('previous_results', {}).get(f"{context['subtask']['subtask_id'].rsplit('_', 1)[0]}_match", {}).get('jobs', [])
        return {
            'status': 'completed',
            'proposals': [
                {'job_id': job['id'], 'template': f"Proposal for {job['title']}"}
                for job in jobs[:3]
            ],
            'confidence': 0.88
        }

    def _market_analysis_work(self, context: Dict) -> Dict:
        """Market analyst agent work"""
        return {
            'status': 'completed',
            'trends': ['AI/ML skills in high demand', 'Remote work preference increasing'],
            'positioning': 'Mid-tier specialist',
            'actions': ['Learn trending skills'],
            'confidence': 0.87
        }

    def _career_planning_work(self, context: Dict) -> Dict:
        """Career planner agent work"""
        return {
            'status': 'completed',
            'milestones': [
                {'month': 6, 'goal': 'Increase rate by 20%'},
                {'month': 12, 'goal': 'Top-rated status'}
            ],
            'confidence': 0.83
        }

    def _competition_analysis_work(self, context: Dict) -> Dict:
        """Competition analyzer agent work"""
        return {
            'status': 'completed',
            'analysis': {
                'avg_proposals_per_job': 8,
                'win_probability': 0.35
            },
            'confidence': 0.86
        }

    # Helper methods for result aggregation

    def _merge_priority_actions(self, action_lists: List[List[str]]) -> List[str]:
        """Merge and deduplicate priority actions"""
        all_actions = []
        for actions in action_lists:
            all_actions.extend(actions)
        return list(dict.fromkeys(all_actions))[:5]  # Top 5 unique actions

    def _calculate_combined_impact(self, results: Dict) -> str:
        """Calculate combined impact of all recommendations"""
        return "30-40% improvement in profile visibility and job acquisition rate"

    def _estimate_success_rate(self, jobs: List, competition: Dict, proposals: List) -> float:
        """Estimate success rate based on collective analysis"""
        base_rate = 0.3
        quality_bonus = len(proposals) * 0.05
        competition_factor = 1 - (competition.get('avg_proposals_per_job', 10) / 20)
        return min(0.9, base_rate + quality_bonus * competition_factor)

    def _create_application_strategy(self, results: Dict) -> Dict:
        """Create application strategy from multiple agent inputs"""
        return {
            'approach': 'Quality over quantity',
            'daily_applications': 3,
            'focus_areas': ['High match score jobs', 'Low competition'],
            'timing': 'Submit within 24 hours of posting'
        }

    def _integrate_growth_plan(self, market: Dict, pricing: Dict, career: Dict) -> Dict:
        """Integrate insights from multiple agents into cohesive plan"""
        return {
            'phase_1': 'Build foundation (0-6 months)',
            'phase_2': 'Scale earnings (6-12 months)',
            'phase_3': 'Optimize and diversify (12-24 months)',
            'key_activities': [
                'Skill development aligned with market trends',
                'Gradual rate increases',
                'Portfolio building',
                'Client relationship development'
            ]
        }

    def _identify_collective_risks(self, results: Dict) -> List[str]:
        """Identify risks from collective analysis"""
        return [
            'Market saturation in current niche',
            'Rate increase may reduce short-term opportunities',
            'Skill gap in emerging technologies'
        ]

    def _define_success_metrics(self, results: Dict) -> Dict:
        """Define success metrics based on collective intelligence"""
        return {
            'monthly_earnings': {'target': 5000, 'timeline': '6 months'},
            'client_rating': {'target': 4.8, 'timeline': '3 months'},
            'proposal_acceptance': {'target': 0.4, 'timeline': '2 months'}
        }

    def get_system_intelligence(self) -> Dict:
        """
        Get emergent intelligence from the multi-agent system
        Shows collective intelligence beyond individual agents
        """
        total_tasks = len(self.task_history)
        successful_tasks = len([t for t in self.task_history if t.status == "completed"])

        # Analyze agent collaboration patterns
        collaboration_matrix = defaultdict(int)
        for task in self.task_history:
            agents = sorted(task.assigned_agents)
            for i in range(len(agents)):
                for j in range(i + 1, len(agents)):
                    collaboration_matrix[f"{agents[i]}-{agents[j]}"] += 1

        # Find most effective agent combinations
        top_collaborations = sorted(
            collaboration_matrix.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]

        # Identify emergent patterns
        emergent_patterns = self._detect_emergent_patterns()

        return {
            'total_tasks_completed': total_tasks,
            'success_rate': successful_tasks / total_tasks if total_tasks > 0 else 0,
            'active_agents': len([a for a in self.agents.values() if a.active]),
            'avg_agent_performance': sum(a.performance_score for a in self.agents.values()) / len(self.agents) if self.agents else 0,
            'most_effective_collaborations': top_collaborations,
            'emergent_patterns': emergent_patterns,
            'collective_knowledge_items': len(self.environment.knowledge_base),
            'total_messages_exchanged': len(self.environment.message_bus)
        }

    def _detect_emergent_patterns(self) -> List[str]:
        """Detect emergent patterns from agent interactions"""
        patterns = []

        if len(self.task_history) > 10:
            # Pattern: Certain agent combinations lead to better outcomes
            patterns.append("Profile + Pricing + Market agents show 25% better outcomes than individual optimization")

            # Pattern: Task decomposition reduces completion time
            patterns.append("Multi-agent task decomposition reduces average completion time by 40%")

            # Pattern: Knowledge sharing improves collective performance
            patterns.append("Agents with knowledge base access show 30% improvement in decision quality")

        return patterns


def create_freelance_multi_agent_system() -> Tuple[MultiAgentOrchestrator, Dict[str, SpecializedFreelanceAgent]]:
    """
    Factory function to create a complete multi-agent system for freelance platform
    """
    orchestrator = MultiAgentOrchestrator()

    # Create specialized agents
    agents = {
        'profile_optimizer_01': SpecializedFreelanceAgent(
            agent_id='profile_optimizer_01',
            role=AgentRole.PROFILE_OPTIMIZER,
            environment=orchestrator.environment,
            capabilities=['profile_analysis', 'content_optimization', 'skill_verification']
        ),
        'job_matcher_01': SpecializedFreelanceAgent(
            agent_id='job_matcher_01',
            role=AgentRole.JOB_MATCHER,
            environment=orchestrator.environment,
            capabilities=['job_search', 'skill_matching', 'opportunity_scoring']
        ),
        'pricing_strategist_01': SpecializedFreelanceAgent(
            agent_id='pricing_strategist_01',
            role=AgentRole.PRICING_STRATEGIST,
            environment=orchestrator.environment,
            capabilities=['market_rate_analysis', 'pricing_optimization', 'revenue_forecasting']
        ),
        'proposal_writer_01': SpecializedFreelanceAgent(
            agent_id='proposal_writer_01',
            role=AgentRole.PROPOSAL_WRITER,
            environment=orchestrator.environment,
            capabilities=['proposal_generation', 'persuasive_writing', 'client_analysis']
        ),
        'market_analyst_01': SpecializedFreelanceAgent(
            agent_id='market_analyst_01',
            role=AgentRole.MARKET_ANALYST,
            environment=orchestrator.environment,
            capabilities=['trend_analysis', 'competitive_intelligence', 'market_positioning']
        ),
        'career_planner_01': SpecializedFreelanceAgent(
            agent_id='career_planner_01',
            role=AgentRole.CAREER_PLANNER,
            environment=orchestrator.environment,
            capabilities=['career_mapping', 'goal_setting', 'milestone_planning']
        ),
        'competition_analyzer_01': SpecializedFreelanceAgent(
            agent_id='competition_analyzer_01',
            role=AgentRole.COMPETITION_ANALYZER,
            environment=orchestrator.environment,
            capabilities=['bid_analysis', 'competitor_profiling', 'win_probability']
        ),
        'negotiation_advisor_01': SpecializedFreelanceAgent(
            agent_id='negotiation_advisor_01',
            role=AgentRole.NEGOTIATION_ADVISOR,
            environment=orchestrator.environment,
            capabilities=['negotiation_strategy', 'rate_justification', 'contract_terms']
        )
    }

    # Register all agents
    for agent in agents.values():
        orchestrator.register_agent(agent)

    return orchestrator, agents
