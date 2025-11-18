"""
Learning Path Strategist Agent
Creates optimal, adaptive learning strategies with skill dependency mapping
"""
from typing import Dict, List, Any, Optional
from datetime import datetime
import networkx as nx
from .base_agent import BaseAgent, AgentResponse


class LearningPathStrategistAgent(BaseAgent):
    """
    Agent specialized in creating optimal learning paths
    Analyzes skill dependencies, learning styles, and creates multi-path strategies
    """

    def __init__(self, agent_id: str = "learning_strategist_01"):
        super().__init__(agent_id, "LearningPathStrategist")
        self.capabilities = [
            'create_learning_path',
            'optimize_learning_strategy',
            'analyze_skill_dependencies',
            'learning_style_personalization',
            'time_optimization'
        ]

    def process_task(self, task: Dict) -> AgentResponse:
        """Process learning strategy tasks"""
        import time
        start_time = time.time()

        task_type = task.get('type')

        try:
            if task_type == 'create_learning_path':
                result = self.create_optimal_learning_path(
                    task.get('target_skills', []),
                    task.get('current_skills', []),
                    task.get('time_available_hours', 10),
                    task.get('learning_preferences', {})
                )
                status = 'success'
                confidence = 0.88

            elif task_type == 'optimize_learning_strategy':
                result = self.optimize_strategy(
                    task.get('learning_goals', []),
                    task.get('constraints', {})
                )
                status = 'success'
                confidence = 0.85

            else:
                result = {'error': 'Unknown task type'}
                status = 'failed'
                confidence = 0.0

            response_time = time.time() - start_time
            self.update_metrics(status == 'success', response_time)

            return AgentResponse(
                agent_id=self.agent_id,
                agent_type=self.agent_type,
                status=status,
                data=result,
                confidence=confidence,
                recommendations=result.get('recommendations', []),
                next_steps=result.get('next_steps', []),
                timestamp=datetime.now(),
                metadata={'response_time': response_time}
            )

        except Exception as e:
            return AgentResponse(
                agent_id=self.agent_id,
                agent_type=self.agent_type,
                status='failed',
                data={'error': str(e)},
                confidence=0.0,
                recommendations=[],
                next_steps=['Review task parameters and retry'],
                timestamp=datetime.now(),
                metadata={}
            )

    def analyze(self, data: Dict) -> Dict:
        """Analyze learning requirements and create strategy"""
        return self.create_optimal_learning_path(
            data.get('target_skills', []),
            data.get('current_skills', []),
            data.get('time_available_hours', 10),
            data.get('learning_preferences', {})
        )

    def create_optimal_learning_path(
        self,
        target_skills: List[str],
        current_skills: List[str],
        time_available_hours: int,
        learning_preferences: Dict
    ) -> Dict:
        """
        Create optimal learning path considering dependencies and constraints

        Returns:
            Comprehensive learning strategy with multiple paths
        """
        # Build skill dependency graph
        skill_graph = self._build_skill_dependency_graph(target_skills)

        # Identify skill gaps
        skills_to_learn = [s for s in target_skills if s not in current_skills]

        # Create multiple learning paths
        learning_paths = self._generate_learning_paths(
            skills_to_learn,
            skill_graph,
            time_available_hours
        )

        # Optimize based on learning style
        optimized_path = self._optimize_for_learning_style(
            learning_paths,
            learning_preferences
        )

        # Calculate timeline
        timeline = self._calculate_learning_timeline(
            optimized_path,
            time_available_hours
        )

        # Generate resource recommendations
        resources = self._recommend_learning_resources(skills_to_learn)

        return {
            'optimal_path': optimized_path,
            'alternative_paths': learning_paths[:3],  # Top 3 alternatives
            'timeline': timeline,
            'total_estimated_hours': sum(s['estimated_hours'] for s in optimized_path['skills']),
            'skill_dependencies': self._extract_dependencies(skill_graph),
            'learning_resources': resources,
            'milestones': self._create_milestones(optimized_path),
            'difficulty_curve': self._analyze_difficulty_progression(optimized_path),
            'recommendations': [
                f"Focus on foundational skills first: {', '.join(optimized_path['foundation_skills'])}",
                f"Estimated completion: {timeline['total_weeks']} weeks at {time_available_hours}h/week",
                f"Recommended learning style: {optimized_path['recommended_style']}",
                "Practice each skill with hands-on projects before moving forward"
            ],
            'next_steps': [
                f"Start with: {optimized_path['skills'][0]['name']}",
                f"Complete foundation skills in weeks 1-{timeline['foundation_complete_week']}",
                "Build portfolio project to demonstrate mastery",
                "Join study group or find accountability partner"
            ]
        }

    def _build_skill_dependency_graph(self, skills: List[str]) -> nx.DiGraph:
        """Build directed graph of skill dependencies"""
        G = nx.DiGraph()

        # Skill dependency knowledge base
        dependencies = {
            'machine_learning': ['python', 'statistics', 'linear_algebra'],
            'deep_learning': ['machine_learning', 'python', 'calculus'],
            'data_science': ['python', 'statistics', 'sql'],
            'cloud': ['linux', 'networking'],
            'kubernetes': ['cloud', 'docker', 'linux'],
            'docker': ['linux', 'command_line'],
            'react': ['javascript', 'html', 'css'],
            'node.js': ['javascript'],
            'python': [],
            'javascript': [],
            'sql': [],
            'statistics': ['mathematics'],
            'linear_algebra': ['mathematics'],
            'calculus': ['mathematics'],
            'html': [],
            'css': [],
            'linux': [],
            'networking': [],
            'command_line': [],
            'mathematics': []
        }

        for skill in skills:
            skill_lower = skill.lower().replace(' ', '_')
            G.add_node(skill_lower)

            # Add dependencies
            deps = dependencies.get(skill_lower, [])
            for dep in deps:
                G.add_node(dep)
                G.add_edge(dep, skill_lower)

        return G

    def _generate_learning_paths(
        self,
        skills: List[str],
        graph: nx.DiGraph,
        time_budget: int
    ) -> List[Dict]:
        """Generate multiple optimal learning paths"""
        paths = []

        # Strategy 1: Breadth-first (learn basics of everything)
        breadth_first = self._create_breadth_first_path(skills, graph)
        paths.append({
            'name': 'Breadth-First Strategy',
            'description': 'Learn fundamentals of all skills quickly, then deepen',
            'skills': breadth_first,
            'foundation_skills': self._identify_foundation_skills(graph),
            'recommended_style': 'breadth_first',
            'pros': ['Quick overview', 'Flexible', 'Early wins'],
            'cons': ['Less depth initially', 'May forget basics']
        })

        # Strategy 2: Depth-first (master one skill tree at a time)
        depth_first = self._create_depth_first_path(skills, graph)
        paths.append({
            'name': 'Depth-First Strategy',
            'description': 'Master each skill completely before moving on',
            'skills': depth_first,
            'foundation_skills': self._identify_foundation_skills(graph),
            'recommended_style': 'depth_first',
            'pros': ['Deep mastery', 'Strong foundation', 'Portfolio-ready'],
            'cons': ['Slower to cover all topics', 'Less flexible']
        })

        # Strategy 3: Priority-based (market value optimization)
        priority_based = self._create_priority_path(skills, graph)
        paths.append({
            'name': 'Market-Value Priority',
            'description': 'Prioritize high-demand, high-value skills',
            'skills': priority_based,
            'foundation_skills': self._identify_foundation_skills(graph),
            'recommended_style': 'priority_based',
            'pros': ['Maximize employability', 'ROI-focused', 'Quick wins'],
            'cons': ['May skip interesting topics', 'Less comprehensive']
        })

        return paths

    def _create_breadth_first_path(self, skills: List[str], graph: nx.DiGraph) -> List[Dict]:
        """Create breadth-first learning path"""
        path = []
        foundation = self._identify_foundation_skills(graph)

        # Add foundation skills first
        for skill in foundation:
            path.append({
                'name': skill,
                'level': 'foundation',
                'estimated_hours': 20,
                'priority': 'critical',
                'resources': ['online course', 'documentation']
            })

        # Add intermediate skills
        intermediate = [s for s in skills if s not in foundation]
        for skill in intermediate:
            path.append({
                'name': skill,
                'level': 'intermediate',
                'estimated_hours': 40,
                'priority': 'high',
                'resources': ['project-based course', 'practice problems']
            })

        return path

    def _create_depth_first_path(self, skills: List[str], graph: nx.DiGraph) -> List[Dict]:
        """Create depth-first learning path"""
        path = []

        try:
            # Topological sort for dependency order
            ordered_skills = list(nx.topological_sort(graph))
        except:
            ordered_skills = skills

        for skill in ordered_skills:
            if skill.lower().replace(' ', '_') in [s.lower().replace(' ', '_') for s in skills]:
                depth_level = 'advanced' if graph.out_degree(skill) > 0 else 'foundation'
                path.append({
                    'name': skill,
                    'level': depth_level,
                    'estimated_hours': 60,
                    'priority': 'critical',
                    'resources': ['comprehensive course', 'books', 'projects']
                })

        return path

    def _create_priority_path(self, skills: List[str], graph: nx.DiGraph) -> List[Dict]:
        """Create priority-based path focusing on market value"""
        # Market value scores (simplified)
        market_value = {
            'machine_learning': 95,
            'cloud': 90,
            'python': 88,
            'kubernetes': 85,
            'react': 82,
            'data_science': 88,
            'deep_learning': 87,
            'sql': 75,
            'docker': 78,
            'javascript': 80
        }

        path = []
        foundation = self._identify_foundation_skills(graph)

        # Foundation first
        for skill in foundation:
            path.append({
                'name': skill,
                'level': 'foundation',
                'estimated_hours': 25,
                'priority': 'critical',
                'market_value': market_value.get(skill, 70),
                'resources': ['fast-track course', 'cheat sheets']
            })

        # Sort remaining by market value
        remaining = [s for s in skills if s not in foundation]
        remaining_sorted = sorted(
            remaining,
            key=lambda s: market_value.get(s.lower(), 70),
            reverse=True
        )

        for skill in remaining_sorted:
            path.append({
                'name': skill,
                'level': 'intermediate',
                'estimated_hours': 45,
                'priority': 'high',
                'market_value': market_value.get(skill.lower(), 70),
                'resources': ['bootcamp', 'certification prep']
            })

        return path

    def _identify_foundation_skills(self, graph: nx.DiGraph) -> List[str]:
        """Identify foundational skills (no prerequisites)"""
        foundation = [node for node in graph.nodes() if graph.in_degree(node) == 0]
        return foundation

    def _optimize_for_learning_style(
        self,
        paths: List[Dict],
        preferences: Dict
    ) -> Dict:
        """Select optimal path based on learning style preferences"""
        learning_style = preferences.get('style', 'balanced')

        style_mapping = {
            'fast': 0,  # Breadth-first
            'thorough': 1,  # Depth-first
            'practical': 2,  # Priority-based
            'balanced': 0
        }

        index = style_mapping.get(learning_style, 0)
        return paths[index] if index < len(paths) else paths[0]

    def _calculate_learning_timeline(
        self,
        learning_path: Dict,
        hours_per_week: int
    ) -> Dict:
        """Calculate detailed timeline for learning path"""
        total_hours = sum(s['estimated_hours'] for s in learning_path['skills'])
        total_weeks = int(total_hours / hours_per_week) + 1

        # Foundation completion
        foundation_hours = sum(
            s['estimated_hours']
            for s in learning_path['skills']
            if s.get('level') == 'foundation'
        )
        foundation_weeks = int(foundation_hours / hours_per_week) + 1

        return {
            'total_weeks': total_weeks,
            'total_hours': total_hours,
            'hours_per_week': hours_per_week,
            'foundation_complete_week': foundation_weeks,
            'estimated_completion_date': f"{total_weeks} weeks from start",
            'weekly_breakdown': self._create_weekly_breakdown(
                learning_path['skills'],
                hours_per_week
            )
        }

    def _create_weekly_breakdown(self, skills: List[Dict], hours_per_week: int) -> List[Dict]:
        """Create week-by-week learning breakdown"""
        breakdown = []
        current_week = 1
        hours_accumulated = 0

        for skill in skills:
            skill_hours = skill['estimated_hours']
            weeks_needed = int(skill_hours / hours_per_week) + 1

            breakdown.append({
                'weeks': f"{current_week}-{current_week + weeks_needed - 1}",
                'skill': skill['name'],
                'hours': skill_hours,
                'focus': skill.get('level', 'intermediate')
            })

            current_week += weeks_needed
            hours_accumulated += skill_hours

        return breakdown

    def _recommend_learning_resources(self, skills: List[str]) -> Dict:
        """Recommend specific learning resources for each skill"""
        resources = {}

        resource_db = {
            'machine_learning': {
                'courses': ['Coursera ML Specialization', 'fast.ai'],
                'books': ['Hands-On Machine Learning', 'Pattern Recognition'],
                'practice': ['Kaggle competitions', 'UCI ML Repository'],
                'community': ['r/MachineLearning', 'ML Discord']
            },
            'python': {
                'courses': ['Python for Everybody', 'Automate the Boring Stuff'],
                'books': ['Python Crash Course', 'Fluent Python'],
                'practice': ['LeetCode', 'HackerRank', 'Project Euler'],
                'community': ['r/learnpython', 'Python Discord']
            },
            'default': {
                'courses': ['Udemy', 'Coursera', 'edX'],
                'books': ['O\'Reilly library', 'Manning publications'],
                'practice': ['GitHub projects', 'Tutorial sites'],
                'community': ['Reddit', 'Stack Overflow', 'Discord']
            }
        }

        for skill in skills:
            skill_key = skill.lower().replace(' ', '_')
            resources[skill] = resource_db.get(skill_key, resource_db['default'])

        return resources

    def _create_milestones(self, learning_path: Dict) -> List[Dict]:
        """Create achievement milestones for motivation"""
        skills = learning_path['skills']
        total_skills = len(skills)

        milestones = [
            {
                'name': 'Foundation Complete',
                'description': 'Mastered all prerequisite skills',
                'skills_completed': len([s for s in skills if s.get('level') == 'foundation']),
                'percentage': 25,
                'reward': 'Ready for intermediate topics'
            },
            {
                'name': 'Halfway Point',
                'description': 'Completed 50% of learning path',
                'skills_completed': total_skills // 2,
                'percentage': 50,
                'reward': 'Build your first portfolio project'
            },
            {
                'name': 'Advanced Level',
                'description': 'Completed 75% of learning path',
                'skills_completed': int(total_skills * 0.75),
                'percentage': 75,
                'reward': 'Start applying to jobs'
            },
            {
                'name': 'Path Complete',
                'description': 'Mastered all target skills',
                'skills_completed': total_skills,
                'percentage': 100,
                'reward': 'Career transition ready!'
            }
        ]

        return milestones

    def _analyze_difficulty_progression(self, learning_path: Dict) -> Dict:
        """Analyze how difficulty progresses through the path"""
        skills = learning_path['skills']

        difficulty_scores = []
        for i, skill in enumerate(skills):
            # Difficulty increases with position and level
            base_difficulty = {
                'foundation': 3,
                'intermediate': 6,
                'advanced': 9
            }.get(skill.get('level', 'intermediate'), 5)

            difficulty_scores.append({
                'skill': skill['name'],
                'position': i + 1,
                'difficulty': base_difficulty,
                'cumulative_difficulty': sum(difficulty_scores) + base_difficulty if difficulty_scores else base_difficulty
            })

        return {
            'progression': difficulty_scores,
            'average_difficulty': sum(s['difficulty'] for s in difficulty_scores) / len(difficulty_scores),
            'difficulty_curve': 'gradual' if difficulty_scores[-1]['difficulty'] - difficulty_scores[0]['difficulty'] < 5 else 'steep',
            'recommendation': 'Well-balanced progression' if difficulty_scores[-1]['difficulty'] - difficulty_scores[0]['difficulty'] < 6 else 'Consider more preparation for advanced topics'
        }

    def _extract_dependencies(self, graph: nx.DiGraph) -> List[Dict]:
        """Extract skill dependencies from graph"""
        dependencies = []

        for node in graph.nodes():
            prerequisites = list(graph.predecessors(node))
            if prerequisites:
                dependencies.append({
                    'skill': node,
                    'requires': prerequisites,
                    'enables': list(graph.successors(node))
                })

        return dependencies

    def optimize_strategy(self, learning_goals: List[str], constraints: Dict) -> Dict:
        """Optimize learning strategy based on specific goals and constraints"""
        time_constraint = constraints.get('time_weeks', 12)
        budget_constraint = constraints.get('budget_usd', 500)

        return {
            'optimized_strategy': {
                'focus_areas': learning_goals[:3],  # Top 3 priorities
                'time_allocation': self._allocate_time(learning_goals, time_constraint),
                'budget_allocation': self._allocate_budget(learning_goals, budget_constraint),
                'recommended_intensity': 'moderate' if time_constraint > 12 else 'intensive'
            },
            'trade_offs': {
                'time_vs_depth': 'Favor breadth' if time_constraint < 12 else 'Favor depth',
                'cost_vs_quality': 'Free resources primary' if budget_constraint < 100 else 'Premium courses recommended'
            },
            'recommendations': [
                f"Focus on top 3 skills: {', '.join(learning_goals[:3])}",
                f"Allocate {time_constraint} weeks total",
                "Use free resources for foundation, paid for advanced topics"
            ],
            'next_steps': [
                "Create detailed weekly schedule",
                "Identify accountability partner",
                "Set up progress tracking system"
            ]
        }

    def _allocate_time(self, goals: List[str], total_weeks: int) -> Dict:
        """Allocate time across learning goals"""
        allocation = {}
        weeks_per_goal = total_weeks // len(goals) if goals else 0

        for i, goal in enumerate(goals):
            # First goal gets extra time if there's remainder
            extra = (total_weeks % len(goals)) if i == 0 else 0
            allocation[goal] = weeks_per_goal + extra

        return allocation

    def _allocate_budget(self, goals: List[str], total_budget: int) -> Dict:
        """Allocate budget across learning resources"""
        allocation = {}
        budget_per_goal = total_budget // len(goals) if goals else 0

        for goal in goals:
            allocation[goal] = {
                'courses': budget_per_goal * 0.6,  # 60% on courses
                'books': budget_per_goal * 0.2,    # 20% on books
                'tools': budget_per_goal * 0.2     # 20% on tools/software
            }

        return allocation
