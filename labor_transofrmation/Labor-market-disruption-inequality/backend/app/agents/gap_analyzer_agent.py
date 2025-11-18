"""
Gap Analysis Agent
Identifies skill gaps, opportunity gaps, and knowledge gaps
"""
from typing import Dict, List
from datetime import datetime
import numpy as np
from .base_agent import BaseAgent, AgentResponse

class GapAnalyzerAgent(BaseAgent):
    """
    Specialized agent for comprehensive gap analysis
    - Identifies skill gaps
    - Discovers hidden opportunity gaps
    - Analyzes knowledge deficits
    - Prioritizes gaps by impact
    """

    def __init__(self, agent_id: str = "gap_analyzer_01"):
        super().__init__(agent_id, "GapAnalyzer")
        self.capabilities = [
            'skill_gap_analysis',
            'opportunity_gap_detection',
            'knowledge_gap_identification',
            'gap_prioritization',
            'market_gap_analysis'
        ]

    def process_task(self, task: Dict) -> AgentResponse:
        """Process gap analysis task"""
        start_time = datetime.now()

        task_type = task.get('type', 'unknown')

        if task_type == 'comprehensive_gap_analysis':
            result = self.comprehensive_gap_analysis(
                task.get('worker_data'),
                task.get('target_role'),
                task.get('market_data')
            )
            status = 'success'
        elif task_type == 'hidden_gap_discovery':
            result = self.discover_hidden_gaps(
                task.get('worker_data'),
                task.get('market_trends')
            )
            status = 'success'
        else:
            result = {'error': 'Unknown task type'}
            status = 'failed'

        response_time = (datetime.now() - start_time).total_seconds()
        self.update_metrics(status == 'success', response_time)

        return AgentResponse(
            agent_id=self.agent_id,
            agent_type=self.agent_type,
            status=status,
            data=result,
            confidence=0.85,
            recommendations=result.get('recommendations', []),
            next_steps=result.get('next_steps', []),
            timestamp=datetime.now(),
            metadata={'response_time': response_time}
        )

    def analyze(self, data: Dict) -> Dict:
        """Analyze data for gaps"""
        return self.comprehensive_gap_analysis(
            data.get('worker_data'),
            data.get('target_role'),
            data.get('market_data')
        )

    def comprehensive_gap_analysis(
        self,
        worker_data: Dict,
        target_role: Dict,
        market_data: Dict
    ) -> Dict:
        """
        Perform comprehensive multi-dimensional gap analysis

        Returns:
            Detailed gap analysis with actionable insights
        """
        # 1. Skill Gaps
        skill_gaps = self._analyze_skill_gaps(worker_data, target_role)

        # 2. Experience Gaps
        experience_gaps = self._analyze_experience_gaps(worker_data, target_role)

        # 3. Network Gaps
        network_gaps = self._analyze_network_gaps(worker_data, target_role)

        # 4. Credential Gaps
        credential_gaps = self._analyze_credential_gaps(worker_data, target_role)

        # 5. Market Readiness Gaps
        market_gaps = self._analyze_market_readiness(worker_data, market_data)

        # 6. Soft Skill Gaps
        soft_skill_gaps = self._analyze_soft_skills(worker_data, target_role)

        # Prioritize all gaps
        all_gaps = (
            skill_gaps['gaps'] +
            experience_gaps['gaps'] +
            network_gaps['gaps'] +
            credential_gaps['gaps'] +
            market_gaps['gaps'] +
            soft_skill_gaps['gaps']
        )

        prioritized = self._prioritize_gaps(all_gaps, market_data)

        # Generate action plan
        action_plan = self._generate_gap_closure_plan(prioritized)

        return {
            'overall_readiness': self._calculate_overall_readiness(prioritized),
            'skill_gaps': skill_gaps,
            'experience_gaps': experience_gaps,
            'network_gaps': network_gaps,
            'credential_gaps': credential_gaps,
            'market_readiness_gaps': market_gaps,
            'soft_skill_gaps': soft_skill_gaps,
            'prioritized_gaps': prioritized,
            'action_plan': action_plan,
            'estimated_closure_time_weeks': sum(g.get('weeks_to_close', 0) for g in prioritized[:10]),
            'recommendations': self._generate_recommendations(prioritized),
            'next_steps': action_plan.get('immediate_actions', [])
        }

    def _analyze_skill_gaps(self, worker: Dict, target: Dict) -> Dict:
        """Analyze technical skill gaps"""
        current_skills = set(worker.get('skills', []))
        required_skills = set(target.get('required_skills', []))
        preferred_skills = set(target.get('preferred_skills', []))

        missing_required = required_skills - current_skills
        missing_preferred = preferred_skills - current_skills

        gaps = []

        for skill in missing_required:
            gaps.append({
                'type': 'skill',
                'gap': skill,
                'severity': 'critical',
                'priority': 1,
                'category': 'technical',
                'weeks_to_close': self._estimate_skill_learning_time(skill),
                'impact': 'Cannot qualify for role without this'
            })

        for skill in missing_preferred:
            gaps.append({
                'type': 'skill',
                'gap': skill,
                'severity': 'moderate',
                'priority': 2,
                'category': 'technical',
                'weeks_to_close': self._estimate_skill_learning_time(skill),
                'impact': 'Improves competitiveness'
            })

        return {
            'total_gaps': len(gaps),
            'critical_gaps': len(missing_required),
            'gaps': gaps,
            'completion_percentage': len(current_skills & required_skills) / len(required_skills) * 100 if required_skills else 100
        }

    def _analyze_experience_gaps(self, worker: Dict, target: Dict) -> Dict:
        """Analyze experience and project gaps"""
        current_exp = worker.get('years_experience', 0)
        required_exp = target.get('required_experience', 0)

        gaps = []

        if current_exp < required_exp:
            gap_years = required_exp - current_exp
            gaps.append({
                'type': 'experience',
                'gap': f'{gap_years} years of experience',
                'severity': 'high',
                'priority': 1,
                'category': 'professional',
                'weeks_to_close': gap_years * 52,  # Can't rush experience
                'impact': 'May limit initial opportunities',
                'mitigation': 'Focus on project work, internships, freelance to accelerate'
            })

        # Project portfolio gap
        current_projects = len(worker.get('portfolio_projects', []))
        expected_projects = target.get('expected_project_count', 5)

        if current_projects < expected_projects:
            gaps.append({
                'type': 'portfolio',
                'gap': f'{expected_projects - current_projects} portfolio projects',
                'severity': 'moderate',
                'priority': 2,
                'category': 'practical',
                'weeks_to_close': (expected_projects - current_projects) * 3,
                'impact': 'Demonstrates practical ability',
                'mitigation': 'Build projects while learning new skills'
            })

        return {
            'total_gaps': len(gaps),
            'gaps': gaps
        }

    def _analyze_network_gaps(self, worker: Dict, target: Dict) -> Dict:
        """Analyze professional network gaps"""
        current_connections = worker.get('professional_network_size', 0)
        industry_connections = worker.get('industry_connections', 0)
        target_industry = target.get('industry', '')

        gaps = []

        # Overall network size
        if current_connections < 100:
            gaps.append({
                'type': 'network',
                'gap': 'Limited professional network',
                'severity': 'moderate',
                'priority': 3,
                'category': 'professional',
                'weeks_to_close': 12,  # Build over time
                'impact': 'Reduces job discovery and referrals',
                'mitigation': 'Join industry groups, attend events, LinkedIn outreach'
            })

        # Industry-specific connections
        if industry_connections < 20:
            gaps.append({
                'type': 'network',
                'gap': f'Few connections in {target_industry}',
                'severity': 'moderate',
                'priority': 3,
                'category': 'professional',
                'weeks_to_close': 8,
                'impact': 'Limited industry insights and opportunities',
                'mitigation': 'Attend industry meetups, join online communities'
            })

        return {
            'total_gaps': len(gaps),
            'gaps': gaps
        }

    def _analyze_credential_gaps(self, worker: Dict, target: Dict) -> Dict:
        """Analyze certification and credential gaps"""
        current_certs = set(worker.get('certifications', []))
        required_certs = set(target.get('required_certifications', []))
        preferred_certs = set(target.get('preferred_certifications', []))

        gaps = []

        for cert in (required_certs - current_certs):
            gaps.append({
                'type': 'credential',
                'gap': cert,
                'severity': 'high',
                'priority': 2,
                'category': 'qualification',
                'weeks_to_close': 12,  # Typical certification time
                'impact': 'May be mandatory for role',
                'mitigation': 'Enroll in certification program'
            })

        for cert in (preferred_certs - current_certs):
            gaps.append({
                'type': 'credential',
                'gap': cert,
                'severity': 'low',
                'priority': 4,
                'category': 'qualification',
                'weeks_to_close': 8,
                'impact': 'Improves credibility',
                'mitigation': 'Consider after essential certifications'
            })

        return {
            'total_gaps': len(gaps),
            'gaps': gaps
        }

    def _analyze_market_readiness(self, worker: Dict, market: Dict) -> Dict:
        """Analyze readiness for current market conditions"""
        gaps = []

        # Emerging skill awareness
        emerging_skills = market.get('emerging_skills', [])
        current_skills = set(worker.get('skills', []))

        missing_emerging = [s for s in emerging_skills if s not in current_skills]

        if missing_emerging:
            gaps.append({
                'type': 'market_trend',
                'gap': f'Missing {len(missing_emerging)} emerging high-demand skills',
                'severity': 'high',
                'priority': 1,
                'category': 'market',
                'weeks_to_close': len(missing_emerging) * 8,
                'impact': 'Missing growing market opportunities',
                'mitigation': f'Focus on: {", ".join(missing_emerging[:3])}'
            })

        return {
            'total_gaps': len(gaps),
            'gaps': gaps
        }

    def _analyze_soft_skills(self, worker: Dict, target: Dict) -> Dict:
        """Analyze soft skill gaps"""
        # Mock soft skill analysis (in production, use assessments)
        required_soft_skills = target.get('soft_skills', [
            'Communication',
            'Leadership',
            'Problem Solving',
            'Teamwork'
        ])

        gaps = []

        for skill in required_soft_skills:
            # Simulate gap detection
            if np.random.random() > 0.7:  # 30% chance of gap
                gaps.append({
                    'type': 'soft_skill',
                    'gap': skill,
                    'severity': 'moderate',
                    'priority': 3,
                    'category': 'interpersonal',
                    'weeks_to_close': 6,
                    'impact': 'Important for role success',
                    'mitigation': 'Practice in team projects, seek feedback'
                })

        return {
            'total_gaps': len(gaps),
            'gaps': gaps
        }

    def _prioritize_gaps(self, gaps: List[Dict], market: Dict) -> List[Dict]:
        """Prioritize gaps by impact, urgency, and market demand"""
        def priority_score(gap):
            # Score based on multiple factors
            severity_scores = {'critical': 100, 'high': 75, 'moderate': 50, 'low': 25}
            priority_scores = {1: 100, 2: 75, 3: 50, 4: 25, 5: 10}

            score = (
                severity_scores.get(gap.get('severity', 'low'), 25) * 0.4 +
                priority_scores.get(gap.get('priority', 5), 10) * 0.4 +
                (1 / max(gap.get('weeks_to_close', 52), 1)) * 100 * 0.2  # Faster to close = higher priority
            )

            return score

        return sorted(gaps, key=priority_score, reverse=True)

    def _calculate_overall_readiness(self, prioritized_gaps: List[Dict]) -> float:
        """Calculate overall readiness score (0-100)"""
        if not prioritized_gaps:
            return 100.0

        # Penalize based on critical gaps
        critical_gaps = len([g for g in prioritized_gaps if g.get('severity') == 'critical'])
        high_gaps = len([g for g in prioritized_gaps if g.get('severity') == 'high'])

        penalty = (critical_gaps * 15) + (high_gaps * 8)

        readiness = max(0, 100 - penalty)

        return round(readiness, 2)

    def _generate_gap_closure_plan(self, prioritized_gaps: List[Dict]) -> Dict:
        """Generate actionable plan to close gaps"""
        immediate = prioritized_gaps[:3]  # Top 3 priorities
        short_term = prioritized_gaps[3:8]  # Next 5
        long_term = prioritized_gaps[8:]  # Rest

        return {
            'immediate_actions': [
                f"Address {gap['gap']}: {gap.get('mitigation', 'Start working on this')}"
                for gap in immediate
            ],
            'short_term_goals': [
                {
                    'gap': gap['gap'],
                    'timeline': f"{gap.get('weeks_to_close', 4)} weeks",
                    'action': gap.get('mitigation', 'Work on this')
                }
                for gap in short_term
            ],
            'long_term_development': [
                {
                    'gap': gap['gap'],
                    'timeline': f"{gap.get('weeks_to_close', 12)} weeks"
                }
                for gap in long_term
            ]
        }

    def _generate_recommendations(self, prioritized_gaps: List[Dict]) -> List[str]:
        """Generate high-level recommendations"""
        if not prioritized_gaps:
            return ["You're well-prepared! Focus on applying for positions."]

        recommendations = []

        critical = [g for g in prioritized_gaps if g.get('severity') == 'critical']
        if critical:
            recommendations.append(
                f"URGENT: Address {len(critical)} critical gaps before applying: " +
                ", ".join(g['gap'] for g in critical[:3])
            )

        skill_gaps = [g for g in prioritized_gaps if g['type'] == 'skill']
        if len(skill_gaps) > 3:
            recommendations.append(
                f"Enroll in comprehensive training program covering: " +
                ", ".join(g['gap'] for g in skill_gaps[:3])
            )

        return recommendations

    def _estimate_skill_learning_time(self, skill: str) -> int:
        """Estimate weeks needed to learn a skill"""
        # Simplified estimation
        if any(x in skill.lower() for x in ['basic', 'intro', 'fundamentals']):
            return 4
        elif any(x in skill.lower() for x in ['advanced', 'expert', 'architect']):
            return 16
        else:
            return 8

    def discover_hidden_gaps(self, worker_data: Dict, market_trends: Dict) -> Dict:
        """
        Discover non-obvious gaps that might not be apparent
        Uses market intelligence to identify future needs
        """
        hidden_gaps = []

        # 1. Future skill needs based on market trends
        emerging_tech = market_trends.get('emerging_technologies', [])
        current_skills = worker_data.get('skills', [])

        for tech in emerging_tech:
            if tech not in current_skills:
                hidden_gaps.append({
                    'gap': f'Future need: {tech}',
                    'type': 'future_skill',
                    'urgency': 'medium',
                    'discovery_method': 'market_trend_analysis',
                    'rationale': f'{tech} is emerging as critical skill',
                    'action': f'Start learning {tech} now to stay ahead'
                })

        # 2. Industry shift gaps
        current_industry = worker_data.get('current_industry', '')
        if current_industry in ['retail', 'manufacturing', 'data_entry']:
            hidden_gaps.append({
                'gap': 'Industry automation exposure',
                'type': 'industry_risk',
                'urgency': 'high',
                'discovery_method': 'industry_analysis',
                'rationale': f'{current_industry} facing high automation pressure',
                'action': 'Consider transition to automation-resistant fields'
            })

        # 3. Complementary skill gaps
        # Find skills that complement existing skills
        if 'python' in current_skills and 'docker' not in current_skills:
            hidden_gaps.append({
                'gap': 'Docker/containerization',
                'type': 'complementary_skill',
                'urgency': 'medium',
                'discovery_method': 'skill_synergy_analysis',
                'rationale': 'Highly complementary to Python development',
                'action': 'Learn Docker to enhance Python capabilities'
            })

        return {
            'hidden_gaps_discovered': len(hidden_gaps),
            'gaps': hidden_gaps,
            'recommendations': [
                'Proactively address these gaps before they become critical',
                'Stay ahead of market trends by continuous learning'
            ]
        }

    def get_recommendations(self, context: Dict) -> List[str]:
        """Get agent-specific recommendations for given context"""
        return [
            "Run comprehensive gap analysis to identify all deficiencies",
            "Prioritize critical gaps that block job opportunities",
            "Create systematic plan to close gaps incrementally"
        ]
