"""
Skill Graph Generator - Converts experience into intelligent skill network
Part of AI Reskilling Autopilot
"""
import numpy as np
from typing import Dict, List, Tuple, Set
from dataclasses import dataclass
from collections import defaultdict
import networkx as nx

@dataclass
class SkillNode:
    """Node in the skill graph"""
    skill_id: int
    skill_name: str
    proficiency: float  # 0-100
    acquisition_date: str
    years_experience: float
    market_demand: float  # 0-100
    transferability: float  # How transferable to other domains
    obsolescence_risk: float  # Risk of becoming obsolete

@dataclass
class SkillEdge:
    """Edge connecting related skills"""
    from_skill: int
    to_skill: int
    relationship_type: str  # 'prerequisite', 'complementary', 'alternative'
    strength: float  # 0-1

class SkillGraphGenerator:
    """
    Converts worker's experience into intelligent skill graph
    Maps relationships, dependencies, and transition paths
    """

    def __init__(self):
        self.graph = nx.DiGraph()
        self.skill_taxonomy = self._load_skill_taxonomy()

    def _load_skill_taxonomy(self) -> Dict:
        """Load standard skill taxonomy and relationships"""
        return {
            'prerequisites': {
                'machine_learning': ['python', 'statistics', 'linear_algebra'],
                'deep_learning': ['machine_learning', 'neural_networks'],
                'data_engineering': ['sql', 'python', 'distributed_systems'],
                'cloud_architecture': ['networking', 'linux', 'security'],
                'frontend_development': ['html', 'css', 'javascript'],
                'backend_development': ['programming', 'databases', 'apis']
            },
            'complementary': {
                'python': ['data_analysis', 'automation', 'web_scraping'],
                'sql': ['database_design', 'data_warehousing'],
                'project_management': ['communication', 'leadership', 'agile'],
                'devops': ['ci_cd', 'containerization', 'monitoring']
            },
            'alternatives': {
                'python': ['r', 'julia'],
                'aws': ['azure', 'gcp'],
                'react': ['vue', 'angular'],
                'mysql': ['postgresql', 'mongodb']
            }
        }

    def generate_skill_graph(
        self,
        worker_experience: Dict,
        worker_skills: List[Dict],
        job_history: List[Dict]
    ) -> Dict:
        """
        Generate comprehensive skill graph from worker's experience

        Args:
            worker_experience: Years, roles, industries
            worker_skills: Current skills with proficiency
            job_history: Previous positions and responsibilities

        Returns:
            Skill graph with nodes, edges, and metadata
        """
        # Clear existing graph
        self.graph.clear()

        # Add skill nodes
        skill_nodes = []
        for skill in worker_skills:
            node = self._create_skill_node(skill, worker_experience, job_history)
            skill_nodes.append(node)
            self.graph.add_node(
                node.skill_id,
                **{
                    'name': node.skill_name,
                    'proficiency': node.proficiency,
                    'market_demand': node.market_demand,
                    'transferability': node.transferability,
                    'obsolescence_risk': node.obsolescence_risk
                }
            )

        # Add edges (relationships)
        edges = self._identify_skill_relationships(skill_nodes)
        for edge in edges:
            self.graph.add_edge(
                edge.from_skill,
                edge.to_skill,
                relationship=edge.relationship_type,
                strength=edge.strength
            )

        # Analyze graph structure
        analysis = self._analyze_graph_structure()

        # Identify skill clusters
        clusters = self._identify_skill_clusters()

        # Calculate graph metrics
        metrics = self._calculate_graph_metrics()

        return {
            'nodes': [self._node_to_dict(n) for n in skill_nodes],
            'edges': [self._edge_to_dict(e) for e in edges],
            'clusters': clusters,
            'analysis': analysis,
            'metrics': metrics,
            'career_profile': self._generate_career_profile(skill_nodes, job_history)
        }

    def _create_skill_node(
        self,
        skill: Dict,
        experience: Dict,
        job_history: List[Dict]
    ) -> SkillNode:
        """Create a skill node with all attributes"""
        # Calculate transferability based on skill type
        transferability = self._calculate_transferability(skill['skill_name'])

        # Calculate obsolescence risk
        obsolescence_risk = self._calculate_obsolescence_risk(skill['skill_name'])

        # Estimate acquisition date from job history
        acquisition_date = self._estimate_acquisition_date(skill, job_history)

        return SkillNode(
            skill_id=skill['skill_id'],
            skill_name=skill['skill_name'],
            proficiency=skill.get('proficiency_level', 50),
            acquisition_date=acquisition_date,
            years_experience=skill.get('years_experience', 1),
            market_demand=skill.get('market_demand', 50),
            transferability=transferability,
            obsolescence_risk=obsolescence_risk
        )

    def _calculate_transferability(self, skill_name: str) -> float:
        """Calculate how transferable skill is across domains"""
        # Soft skills and foundational technical skills = high transferability
        high_transfer = ['communication', 'leadership', 'problem_solving',
                        'programming', 'data_analysis', 'project_management']

        # Very specific technical skills = low transferability
        low_transfer = ['mainframe', 'cobol', 'legacy_systems']

        skill_lower = skill_name.lower()

        for high in high_transfer:
            if high in skill_lower:
                return np.random.uniform(70, 95)

        for low in low_transfer:
            if low in skill_lower:
                return np.random.uniform(10, 30)

        return np.random.uniform(40, 70)  # Medium transferability

    def _calculate_obsolescence_risk(self, skill_name: str) -> float:
        """Calculate risk of skill becoming obsolete"""
        high_risk = ['data_entry', 'manual_testing', 'fax', 'mainframe']
        low_risk = ['machine_learning', 'ai', 'cloud', 'cybersecurity', 'critical_thinking']

        skill_lower = skill_name.lower()

        for high in high_risk:
            if high in skill_lower:
                return np.random.uniform(70, 95)

        for low in low_risk:
            if low in skill_lower:
                return np.random.uniform(5, 25)

        return np.random.uniform(30, 60)

    def _estimate_acquisition_date(self, skill: Dict, job_history: List[Dict]) -> str:
        """Estimate when skill was acquired based on job history"""
        # Simplified - use years_experience
        years_ago = skill.get('years_experience', 1)
        from datetime import datetime, timedelta
        acquisition = datetime.now() - timedelta(days=365 * years_ago)
        return acquisition.strftime('%Y-%m-%d')

    def _identify_skill_relationships(self, nodes: List[SkillNode]) -> List[SkillEdge]:
        """Identify relationships between skills"""
        edges = []

        for i, node1 in enumerate(nodes):
            for node2 in nodes[i+1:]:
                # Check for prerequisite relationships
                if self._is_prerequisite(node1.skill_name, node2.skill_name):
                    edges.append(SkillEdge(
                        from_skill=node1.skill_id,
                        to_skill=node2.skill_id,
                        relationship_type='prerequisite',
                        strength=0.9
                    ))

                # Check for complementary relationships
                elif self._is_complementary(node1.skill_name, node2.skill_name):
                    edges.append(SkillEdge(
                        from_skill=node1.skill_id,
                        to_skill=node2.skill_id,
                        relationship_type='complementary',
                        strength=0.7
                    ))

                # Check for alternative relationships
                elif self._is_alternative(node1.skill_name, node2.skill_name):
                    edges.append(SkillEdge(
                        from_skill=node1.skill_id,
                        to_skill=node2.skill_id,
                        relationship_type='alternative',
                        strength=0.5
                    ))

        return edges

    def _is_prerequisite(self, skill1: str, skill2: str) -> bool:
        """Check if skill1 is prerequisite for skill2"""
        for advanced_skill, prereqs in self.skill_taxonomy['prerequisites'].items():
            if advanced_skill in skill2.lower():
                if any(prereq in skill1.lower() for prereq in prereqs):
                    return True
        return False

    def _is_complementary(self, skill1: str, skill2: str) -> bool:
        """Check if skills are complementary"""
        for base_skill, complements in self.skill_taxonomy['complementary'].items():
            if base_skill in skill1.lower():
                if any(comp in skill2.lower() for comp in complements):
                    return True
        return False

    def _is_alternative(self, skill1: str, skill2: str) -> bool:
        """Check if skills are alternatives"""
        for skill, alternatives in self.skill_taxonomy['alternatives'].items():
            if skill in skill1.lower():
                if any(alt in skill2.lower() for alt in alternatives):
                    return True
        return False

    def _analyze_graph_structure(self) -> Dict:
        """Analyze overall graph structure"""
        if len(self.graph.nodes) == 0:
            return {'error': 'Empty graph'}

        return {
            'total_skills': len(self.graph.nodes),
            'total_connections': len(self.graph.edges),
            'avg_connections_per_skill': len(self.graph.edges) / len(self.graph.nodes) if len(self.graph.nodes) > 0 else 0,
            'graph_density': nx.density(self.graph),
            'strongly_connected': nx.is_strongly_connected(self.graph),
            'central_skills': self._identify_central_skills()
        }

    def _identify_central_skills(self) -> List[Dict]:
        """Identify most central/important skills in graph"""
        if len(self.graph.nodes) == 0:
            return []

        # Calculate centrality
        centrality = nx.degree_centrality(self.graph)

        # Sort by centrality
        sorted_skills = sorted(
            centrality.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]

        return [
            {
                'skill_id': skill_id,
                'skill_name': self.graph.nodes[skill_id].get('name', 'Unknown'),
                'centrality_score': score
            }
            for skill_id, score in sorted_skills
        ]

    def _identify_skill_clusters(self) -> List[Dict]:
        """Identify clusters of related skills"""
        if len(self.graph.nodes) == 0:
            return []

        # Convert to undirected for clustering
        undirected = self.graph.to_undirected()

        # Find connected components (clusters)
        clusters = list(nx.connected_components(undirected))

        return [
            {
                'cluster_id': i,
                'skills': [
                    self.graph.nodes[node].get('name', f'Skill_{node}')
                    for node in cluster
                ],
                'size': len(cluster),
                'avg_proficiency': np.mean([
                    self.graph.nodes[node].get('proficiency', 50)
                    for node in cluster
                ])
            }
            for i, cluster in enumerate(clusters)
        ]

    def _calculate_graph_metrics(self) -> Dict:
        """Calculate various graph metrics"""
        if len(self.graph.nodes) == 0:
            return {}

        return {
            'skill_diversity_score': len(self.graph.nodes),
            'skill_depth_score': np.mean([
                self.graph.nodes[n].get('proficiency', 0)
                for n in self.graph.nodes
            ]),
            'market_alignment_score': np.mean([
                self.graph.nodes[n].get('market_demand', 0)
                for n in self.graph.nodes
            ]),
            'obsolescence_exposure': np.mean([
                self.graph.nodes[n].get('obsolescence_risk', 0)
                for n in self.graph.nodes
            ]),
            'transferability_index': np.mean([
                self.graph.nodes[n].get('transferability', 0)
                for n in self.graph.nodes
            ])
        }

    def _generate_career_profile(
        self,
        skills: List[SkillNode],
        job_history: List[Dict]
    ) -> Dict:
        """Generate career profile summary"""
        return {
            'career_stage': self._determine_career_stage(job_history),
            'primary_domain': self._identify_primary_domain(skills),
            'skill_trajectory': self._analyze_skill_trajectory(skills),
            'strengths': self._identify_strengths(skills),
            'gaps': self._identify_gaps(skills)
        }

    def _determine_career_stage(self, job_history: List[Dict]) -> str:
        """Determine career stage from history"""
        total_years = sum(job.get('years', 0) for job in job_history)

        if total_years < 3:
            return 'Early Career'
        elif total_years < 8:
            return 'Mid Career'
        elif total_years < 15:
            return 'Senior'
        else:
            return 'Expert'

    def _identify_primary_domain(self, skills: List[SkillNode]) -> str:
        """Identify primary skill domain"""
        # Group skills by domain
        tech_count = sum(1 for s in skills if any(
            tech in s.skill_name.lower()
            for tech in ['python', 'java', 'programming', 'development']
        ))

        data_count = sum(1 for s in skills if any(
            data in s.skill_name.lower()
            for data in ['data', 'analytics', 'sql', 'statistics']
        ))

        if tech_count > data_count:
            return 'Software Development'
        elif data_count > 0:
            return 'Data & Analytics'
        else:
            return 'General Business'

    def _analyze_skill_trajectory(self, skills: List[SkillNode]) -> str:
        """Analyze if skills are growing or stagnating"""
        recent_skills = sum(1 for s in skills if s.years_experience < 2)

        if recent_skills > len(skills) * 0.3:
            return 'Actively Growing'
        elif recent_skills > 0:
            return 'Steady Growth'
        else:
            return 'Stagnant - New skills recommended'

    def _identify_strengths(self, skills: List[SkillNode]) -> List[str]:
        """Identify top strengths"""
        strong_skills = sorted(
            skills,
            key=lambda s: s.proficiency * s.market_demand,
            reverse=True
        )[:3]

        return [s.skill_name for s in strong_skills]

    def _identify_gaps(self, skills: List[SkillNode]) -> List[str]:
        """Identify skill gaps"""
        # Simplified - identify high-demand skills worker lacks
        all_high_demand = ['machine_learning', 'cloud_computing', 'cybersecurity',
                          'data_science', 'devops']

        current_skills_lower = [s.skill_name.lower() for s in skills]

        gaps = [
            skill for skill in all_high_demand
            if not any(skill in current for current in current_skills_lower)
        ]

        return gaps[:3]

    def _node_to_dict(self, node: SkillNode) -> Dict:
        """Convert SkillNode to dictionary"""
        return {
            'skill_id': node.skill_id,
            'skill_name': node.skill_name,
            'proficiency': node.proficiency,
            'acquisition_date': node.acquisition_date,
            'years_experience': node.years_experience,
            'market_demand': node.market_demand,
            'transferability': node.transferability,
            'obsolescence_risk': node.obsolescence_risk
        }

    def _edge_to_dict(self, edge: SkillEdge) -> Dict:
        """Convert SkillEdge to dictionary"""
        return {
            'from_skill': edge.from_skill,
            'to_skill': edge.to_skill,
            'relationship_type': edge.relationship_type,
            'strength': edge.strength
        }

    def find_transition_paths(
        self,
        current_skills: List[int],
        target_role_skills: List[int]
    ) -> List[Dict]:
        """
        Find optimal paths from current skills to target role

        Returns:
            List of learning paths with required skills
        """
        paths = []

        for target in target_role_skills:
            if target in current_skills:
                continue  # Already have this skill

            # Find shortest path
            try:
                for current in current_skills:
                    if nx.has_path(self.graph, current, target):
                        path = nx.shortest_path(self.graph, current, target)
                        paths.append({
                            'target_skill_id': target,
                            'from_skill_id': current,
                            'path': path,
                            'steps': len(path) - 1,
                            'estimated_weeks': (len(path) - 1) * 8  # 8 weeks per skill
                        })
                        break
            except nx.NodeNotFound:
                continue

        return sorted(paths, key=lambda x: x['steps'])
