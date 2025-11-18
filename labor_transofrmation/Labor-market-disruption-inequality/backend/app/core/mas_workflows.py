"""
Multi-Agent System Workflows
Demonstrates collective intelligence through agent collaboration

Examples:
1. Career Transition Workflow - Complex problem broken down across multiple agents
2. Learning Strategy Consensus - Agents negotiate optimal learning path
3. Distributed Job Market Analysis - Parallel analysis by specialized agents
"""
from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid

from backend.app.core.multi_agent_system import (
    SharedEnvironment,
    MultiAgentCoordinator,
    DistributedTask,
    TaskStatus,
    MessageType,
    AgentMessage
)


class CareerTransitionWorkflow:
    """
    Complex career transition workflow demonstrating MAS capabilities

    Flow:
    1. Gap Analyzer analyzes skills gap → writes to shared env
    2. Opportunity Scout reads gap → finds matching jobs → writes opportunities
    3. Learning Strategist reads both → creates learning path → writes to shared env
    4. Teaching Coach reads learning path → prepares materials
    5. Career Navigator reads all data → creates comprehensive transition plan

    This demonstrates:
    - Task distribution across specialized agents
    - Sequential data flow through shared environment
    - Collective intelligence emerges from agent interactions
    """

    def __init__(self, coordinator: MultiAgentCoordinator):
        self.coordinator = coordinator
        self.shared_env = coordinator.shared_env
        self.workflow_id = str(uuid.uuid4())

    def execute(self, worker_id: int, target_role: str) -> Dict:
        """
        Execute complete career transition workflow

        Args:
            worker_id: ID of worker seeking transition
            target_role: Target job title/role

        Returns:
            Comprehensive transition plan from all agents
        """
        workflow_key = f"workflow:{self.workflow_id}"

        # Write initial context to shared environment
        self.shared_env.write(workflow_key, {
            'worker_id': worker_id,
            'target_role': target_role,
            'status': 'initiated',
            'started_at': datetime.now().isoformat(),
        }, 'workflow_orchestrator')

        # Task 1: Skill Gap Analysis
        gap_analysis_task = DistributedTask(
            task_id=str(uuid.uuid4()),
            name="Skill Gap Analysis",
            description="Analyze skills gap between current and target role",
            required_capabilities=['skill_gap_analysis'],
            input_data={
                'worker_id': worker_id,
                'target_role': target_role,
                'result_key': f"{workflow_key}:gap_analysis"
            },
            priority=1
        )

        # Task 2: Opportunity Discovery (depends on Task 1)
        opportunity_task = DistributedTask(
            task_id=str(uuid.uuid4()),
            name="Job Opportunity Discovery",
            description="Find matching job opportunities based on skills gap",
            required_capabilities=['opportunity_scouting'],
            input_data={
                'worker_id': worker_id,
                'target_role': target_role,
                'gap_analysis_key': f"{workflow_key}:gap_analysis",
                'result_key': f"{workflow_key}:opportunities"
            },
            dependencies=[gap_analysis_task.task_id],
            priority=2
        )

        # Task 3: Learning Path Creation (depends on Tasks 1 & 2)
        learning_path_task = DistributedTask(
            task_id=str(uuid.uuid4()),
            name="Learning Path Creation",
            description="Create optimized learning path based on gap and opportunities",
            required_capabilities=['learning_path_optimization'],
            input_data={
                'worker_id': worker_id,
                'gap_analysis_key': f"{workflow_key}:gap_analysis",
                'opportunities_key': f"{workflow_key}:opportunities",
                'result_key': f"{workflow_key}:learning_path"
            },
            dependencies=[gap_analysis_task.task_id, opportunity_task.task_id],
            priority=3
        )

        # Task 4: Teaching Material Preparation (depends on Task 3)
        teaching_prep_task = DistributedTask(
            task_id=str(uuid.uuid4()),
            name="Teaching Material Preparation",
            description="Prepare teaching materials and study resources",
            required_capabilities=['teaching_preparation'],
            input_data={
                'worker_id': worker_id,
                'learning_path_key': f"{workflow_key}:learning_path",
                'result_key': f"{workflow_key}:teaching_materials"
            },
            dependencies=[learning_path_task.task_id],
            priority=4
        )

        # Task 5: Comprehensive Transition Plan (depends on all previous)
        transition_plan_task = DistributedTask(
            task_id=str(uuid.uuid4()),
            name="Comprehensive Transition Plan",
            description="Create complete career transition roadmap",
            required_capabilities=['career_navigation'],
            input_data={
                'worker_id': worker_id,
                'workflow_key': workflow_key,
                'result_key': f"{workflow_key}:final_plan"
            },
            dependencies=[
                gap_analysis_task.task_id,
                opportunity_task.task_id,
                learning_path_task.task_id,
                teaching_prep_task.task_id
            ],
            priority=5
        )

        # Create workflow with all tasks
        tasks = [
            gap_analysis_task,
            opportunity_task,
            learning_path_task,
            teaching_prep_task,
            transition_plan_task
        ]

        self.coordinator.create_workflow(self.workflow_id, tasks)

        return {
            'workflow_id': self.workflow_id,
            'workflow_key': workflow_key,
            'status': 'executing',
            'total_tasks': len(tasks),
            'task_ids': [t.task_id for t in tasks]
        }

    def get_progress(self) -> Dict:
        """Get current workflow progress"""
        return self.coordinator.check_workflow_progress(self.workflow_id)

    def get_results(self) -> Dict:
        """Get final results from shared environment"""
        workflow_key = f"workflow:{self.workflow_id}"
        return {
            'gap_analysis': self.shared_env.read(f"{workflow_key}:gap_analysis"),
            'opportunities': self.shared_env.read(f"{workflow_key}:opportunities"),
            'learning_path': self.shared_env.read(f"{workflow_key}:learning_path"),
            'teaching_materials': self.shared_env.read(f"{workflow_key}:teaching_materials"),
            'final_plan': self.shared_env.read(f"{workflow_key}:final_plan"),
        }


class LearningStrategyConsensus:
    """
    Multiple agents negotiate optimal learning strategy

    Demonstrates:
    - Agent negotiation and voting
    - Consensus building through discussion
    - Competitive proposal evaluation
    """

    def __init__(self, coordinator: MultiAgentCoordinator):
        self.coordinator = coordinator
        self.shared_env = coordinator.shared_env

    def build_consensus(self, worker_id: int, target_skills: List[str],
                       time_constraint_hours: int) -> Dict:
        """
        Multiple agents propose learning strategies, then vote for best approach

        Args:
            worker_id: Worker ID
            target_skills: Skills to learn
            time_constraint_hours: Available time

        Returns:
            Consensus learning strategy
        """
        # Find all agents capable of learning strategy
        strategy_agents = [
            agent_id for agent_id, agent in self.coordinator.agents.items()
            if 'learning_strategy' in agent.capabilities
        ]

        if len(strategy_agents) < 2:
            return {'error': 'Need at least 2 agents for consensus'}

        # Each agent proposes a strategy
        proposals = {}
        for agent_id in strategy_agents:
            message = AgentMessage(
                id=str(uuid.uuid4()),
                from_agent='consensus_coordinator',
                to_agent=agent_id,
                message_type=MessageType.REQUEST,
                payload={
                    'action': 'propose_learning_strategy',
                    'worker_id': worker_id,
                    'target_skills': target_skills,
                    'time_constraint_hours': time_constraint_hours,
                },
                timestamp=datetime.now(),
                requires_response=True,
                priority=1
            )
            self.coordinator.send_message(message)

            # In real implementation, wait for response
            # For now, we'll simulate proposals
            proposals[agent_id] = {
                'estimated_hours': time_constraint_hours * 0.8,
                'path_length': len(target_skills) * 2,
                'confidence': 0.85,
            }

        # Agents vote on best strategy
        vote_result = self.coordinator.vote(
            agent_ids=strategy_agents,
            question="Which learning strategy is most effective?",
            options=list(proposals.keys())
        )

        # Build consensus
        consensus = self.coordinator.get_consensus(
            agent_ids=strategy_agents,
            topic="optimal_learning_strategy",
            initial_proposals=proposals
        )

        return {
            'proposals': proposals,
            'vote': vote_result,
            'consensus': consensus,
            'participating_agents': strategy_agents,
        }


class DistributedJobMarketAnalysis:
    """
    Parallel job market analysis by multiple agents

    Demonstrates:
    - Parallel task execution
    - Distributed data collection
    - Result aggregation from multiple sources
    """

    def __init__(self, coordinator: MultiAgentCoordinator):
        self.coordinator = coordinator
        self.shared_env = coordinator.shared_env
        self.analysis_id = str(uuid.uuid4())

    def analyze_market(self, industry: str, region: str, skills: List[str]) -> Dict:
        """
        Multiple agents analyze job market in parallel

        Tasks distributed:
        - Trend analysis agent: Market trends
        - Salary analysis agent: Compensation data
        - Demand analysis agent: Skill demand
        - Competition analysis agent: Job competition level

        Args:
            industry: Industry to analyze
            region: Geographic region
            skills: Skills to analyze

        Returns:
            Aggregated market analysis
        """
        analysis_key = f"market_analysis:{self.analysis_id}"

        # Create parallel tasks for different aspects
        tasks = []

        # Task 1: Trend Analysis
        tasks.append(DistributedTask(
            task_id=str(uuid.uuid4()),
            name="Market Trend Analysis",
            description="Analyze job market trends and growth",
            required_capabilities=['trend_analysis'],
            input_data={
                'industry': industry,
                'region': region,
                'result_key': f"{analysis_key}:trends"
            },
            priority=1
        ))

        # Task 2: Salary Analysis
        tasks.append(DistributedTask(
            task_id=str(uuid.uuid4()),
            name="Salary Analysis",
            description="Analyze compensation and salary ranges",
            required_capabilities=['salary_analysis'],
            input_data={
                'industry': industry,
                'region': region,
                'skills': skills,
                'result_key': f"{analysis_key}:salaries"
            },
            priority=1
        ))

        # Task 3: Skill Demand Analysis
        tasks.append(DistributedTask(
            task_id=str(uuid.uuid4()),
            name="Skill Demand Analysis",
            description="Analyze demand for specific skills",
            required_capabilities=['demand_analysis'],
            input_data={
                'skills': skills,
                'region': region,
                'result_key': f"{analysis_key}:demand"
            },
            priority=1
        ))

        # Task 4: Competition Analysis
        tasks.append(DistributedTask(
            task_id=str(uuid.uuid4()),
            name="Competition Analysis",
            description="Analyze job market competition level",
            required_capabilities=['competition_analysis'],
            input_data={
                'industry': industry,
                'region': region,
                'result_key': f"{analysis_key}:competition"
            },
            priority=1
        ))

        # Execute all tasks in parallel (no dependencies)
        for task in tasks:
            self.coordinator.distribute_task(task)

        return {
            'analysis_id': self.analysis_id,
            'analysis_key': analysis_key,
            'status': 'executing',
            'parallel_tasks': len(tasks),
            'task_ids': [t.task_id for t in tasks]
        }

    def get_results(self) -> Dict:
        """Aggregate results from all parallel analyses"""
        analysis_key = f"market_analysis:{self.analysis_id}"

        return {
            'analysis_id': self.analysis_id,
            'trends': self.shared_env.read(f"{analysis_key}:trends"),
            'salaries': self.shared_env.read(f"{analysis_key}:salaries"),
            'demand': self.shared_env.read(f"{analysis_key}:demand"),
            'competition': self.shared_env.read(f"{analysis_key}:competition"),
            'timestamp': datetime.now().isoformat(),
        }


class CollaborativeResourceCuration:
    """
    Multiple agents collaborate to curate learning resources

    Demonstrates:
    - Agent collaboration requests
    - Resource sharing through shared environment
    - Quality scoring through multi-agent consensus
    """

    def __init__(self, coordinator: MultiAgentCoordinator):
        self.coordinator = coordinator
        self.shared_env = coordinator.shared_env

    def curate_resources(self, topic: str, difficulty_level: str,
                        learner_preferences: Dict) -> Dict:
        """
        Multiple agents collaborate to find and curate best resources

        Args:
            topic: Learning topic
            difficulty_level: beginner/intermediate/advanced
            learner_preferences: Learning style preferences

        Returns:
            Curated resource collection with quality scores
        """
        conversation_id = str(uuid.uuid4())

        # Find content curator agents
        curator_agents = [
            agent_id for agent_id, agent in self.coordinator.agents.items()
            if 'content_curation' in agent.capabilities
        ]

        if not curator_agents:
            return {'error': 'No curator agents available'}

        # Request collaboration
        collab_id = self.coordinator.request_collaboration(
            requester_id='resource_orchestrator',
            task_description=f"Curate high-quality resources for {topic}",
            required_agents=curator_agents
        )

        # Each agent contributes resources to shared environment
        resources_key = f"curation:{conversation_id}:resources"
        self.shared_env.write(resources_key, {
            'topic': topic,
            'difficulty': difficulty_level,
            'preferences': learner_preferences,
            'resources': [],
            'contributors': [],
        }, 'resource_orchestrator')

        # Agents can subscribe to updates and add their findings
        for agent_id in curator_agents:
            message = AgentMessage(
                id=str(uuid.uuid4()),
                from_agent='resource_orchestrator',
                to_agent=agent_id,
                message_type=MessageType.REQUEST,
                payload={
                    'action': 'contribute_resources',
                    'resources_key': resources_key,
                    'topic': topic,
                    'difficulty': difficulty_level,
                },
                timestamp=datetime.now(),
                conversation_id=collab_id,
                priority=2
            )
            self.coordinator.send_message(message)

        return {
            'collaboration_id': collab_id,
            'resources_key': resources_key,
            'participating_agents': curator_agents,
            'status': 'in_progress',
        }

    def get_curated_resources(self, resources_key: str) -> Dict:
        """Get final curated resources"""
        return self.shared_env.read(resources_key, {})


# ===== Workflow Factory =====

class WorkflowFactory:
    """Factory for creating and executing MAS workflows"""

    @staticmethod
    def create_career_transition_workflow(coordinator: MultiAgentCoordinator,
                                         worker_id: int,
                                         target_role: str) -> Dict:
        """Create and execute career transition workflow"""
        workflow = CareerTransitionWorkflow(coordinator)
        return workflow.execute(worker_id, target_role)

    @staticmethod
    def create_learning_consensus(coordinator: MultiAgentCoordinator,
                                  worker_id: int,
                                  target_skills: List[str],
                                  time_hours: int) -> Dict:
        """Create learning strategy consensus workflow"""
        workflow = LearningStrategyConsensus(coordinator)
        return workflow.build_consensus(worker_id, target_skills, time_hours)

    @staticmethod
    def create_market_analysis(coordinator: MultiAgentCoordinator,
                              industry: str,
                              region: str,
                              skills: List[str]) -> Dict:
        """Create distributed job market analysis"""
        workflow = DistributedJobMarketAnalysis(coordinator)
        return workflow.analyze_market(industry, region, skills)

    @staticmethod
    def create_resource_curation(coordinator: MultiAgentCoordinator,
                                topic: str,
                                difficulty: str,
                                preferences: Dict) -> Dict:
        """Create collaborative resource curation"""
        workflow = CollaborativeResourceCuration(coordinator)
        return workflow.curate_resources(topic, difficulty, preferences)
