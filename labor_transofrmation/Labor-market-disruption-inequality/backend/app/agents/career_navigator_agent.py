"""
Career Navigator Agent
Provides long-term career planning, transition strategies, and decision support
"""
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from .base_agent import BaseAgent, AgentResponse


class CareerNavigatorAgent(BaseAgent):
    """
    Agent specialized in career navigation and long-term planning
    Explores career lattices, analyzes risk-reward, plans transitions
    """

    def __init__(self, agent_id: str = "career_navigator_01"):
        super().__init__(agent_id, "CareerNavigator")
        self.capabilities = [
            'career_path_exploration',
            'transition_strategy',
            'risk_reward_analysis',
            'decision_support',
            'goal_tracking',
            'career_lattice_mapping'
        ]

    def process_task(self, task: Dict) -> AgentResponse:
        """Process career navigation tasks"""
        import time
        start_time = time.time()

        task_type = task.get('type')

        try:
            if task_type == 'explore_career_paths':
                result = self.explore_career_paths(
                    task.get('current_role'),
                    task.get('worker_profile', {}),
                    task.get('time_horizon_years', 5)
                )
                status = 'success'
                confidence = 0.86

            elif task_type == 'plan_transition':
                result = self.plan_career_transition(
                    task.get('current_role'),
                    task.get('target_role'),
                    task.get('worker_data', {}),
                    task.get('constraints', {})
                )
                status = 'success'
                confidence = 0.88

            elif task_type == 'analyze_risk_reward':
                result = self.analyze_risk_reward(
                    task.get('career_options', []),
                    task.get('worker_profile', {})
                )
                status = 'success'
                confidence = 0.84

            elif task_type == 'track_goals':
                result = self.track_career_goals(
                    task.get('goals', []),
                    task.get('progress_data', {})
                )
                status = 'success'
                confidence = 0.90

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
        """Analyze career options and provide navigation guidance"""
        return self.explore_career_paths(
            data.get('current_role'),
            data.get('worker_profile', {}),
            data.get('time_horizon_years', 5)
        )

    def explore_career_paths(
        self,
        current_role: str,
        worker_profile: Dict,
        time_horizon_years: int
    ) -> Dict:
        """
        Explore possible career paths from current position

        Returns:
            Career lattice with multiple pathways and their viability
        """
        # Build career lattice
        lattice = self._build_career_lattice(current_role)

        # Identify viable paths
        viable_paths = self._identify_viable_paths(
            lattice,
            worker_profile,
            time_horizon_years
        )

        # Analyze each path
        analyzed_paths = []
        for path in viable_paths:
            analysis = self._analyze_career_path(path, worker_profile, time_horizon_years)
            analyzed_paths.append(analysis)

        # Sort by overall score
        analyzed_paths.sort(key=lambda p: p['overall_score'], reverse=True)

        return {
            'current_role': current_role,
            'time_horizon': f"{time_horizon_years} years",
            'total_paths_identified': len(analyzed_paths),
            'career_paths': analyzed_paths[:5],  # Top 5 paths
            'career_lattice': {
                'vertical_moves': lattice['vertical'],
                'lateral_moves': lattice['lateral'],
                'pivot_moves': lattice['pivots']
            },
            'path_categories': {
                'promotion_path': [p for p in analyzed_paths if p['path_type'] == 'vertical'][:2],
                'pivot_path': [p for p in analyzed_paths if p['path_type'] == 'pivot'][:2],
                'specialization_path': [p for p in analyzed_paths if p['path_type'] == 'lateral'][:2]
            },
            'recommendations': [
                f"Top recommended path: {analyzed_paths[0]['target_role']}",
                f"Best for income: {max(analyzed_paths, key=lambda p: p['income_potential'])['target_role']}",
                f"Best for work-life balance: {max(analyzed_paths, key=lambda p: p['work_life_balance'])['target_role']}",
                "Consider both short-term gains and long-term satisfaction"
            ],
            'next_steps': [
                f"Deep dive into top 3 paths",
                "Compare risk-reward profiles",
                "Identify required skill development",
                "Set intermediate milestones"
            ]
        }

    def _build_career_lattice(self, current_role: str) -> Dict:
        """Build career lattice showing possible moves"""
        # Career lattice knowledge base
        lattice_db = {
            'Data Analyst': {
                'vertical': ['Senior Data Analyst', 'Lead Data Analyst', 'Analytics Manager'],
                'lateral': ['Business Analyst', 'Marketing Analyst', 'Product Analyst'],
                'pivots': ['Data Scientist', 'Data Engineer', 'Business Intelligence Developer']
            },
            'Software Engineer': {
                'vertical': ['Senior Software Engineer', 'Staff Engineer', 'Engineering Manager'],
                'lateral': ['DevOps Engineer', 'QA Engineer', 'Technical Writer'],
                'pivots': ['Product Manager', 'Solutions Architect', 'Data Engineer']
            },
            'Project Manager': {
                'vertical': ['Senior Project Manager', 'Program Manager', 'Director of PMO'],
                'lateral': ['Scrum Master', 'Business Analyst', 'Operations Manager'],
                'pivots': ['Product Manager', 'Consultant', 'Change Manager']
            },
            'default': {
                'vertical': ['Senior Role', 'Lead Role', 'Manager Role'],
                'lateral': ['Adjacent Role', 'Related Role'],
                'pivots': ['Career Change', 'Industry Pivot']
            }
        }

        return lattice_db.get(current_role, lattice_db['default'])

    def _identify_viable_paths(
        self,
        lattice: Dict,
        worker_profile: Dict,
        time_horizon: int
    ) -> List[Dict]:
        """Identify which paths are realistically achievable"""
        viable = []
        years_experience = worker_profile.get('years_experience', 0)
        current_skills = worker_profile.get('skills', [])

        # Vertical paths (promotions)
        for role in lattice['vertical']:
            viable.append({
                'target_role': role,
                'path_type': 'vertical',
                'estimated_time_years': 2 if years_experience > 3 else 3,
                'difficulty': 'medium',
                'required_skills': current_skills + ['leadership', 'strategic thinking']
            })

        # Lateral paths (same level, different function)
        for role in lattice['lateral']:
            viable.append({
                'target_role': role,
                'path_type': 'lateral',
                'estimated_time_years': 1,
                'difficulty': 'low',
                'required_skills': current_skills + ['domain knowledge']
            })

        # Pivot paths (career change)
        for role in lattice['pivots']:
            viable.append({
                'target_role': role,
                'path_type': 'pivot',
                'estimated_time_years': 2,
                'difficulty': 'high',
                'required_skills': self._get_pivot_skills(role)
            })

        # Filter by time horizon
        viable = [p for p in viable if p['estimated_time_years'] <= time_horizon]

        return viable

    def _get_pivot_skills(self, role: str) -> List[str]:
        """Get skills needed for pivot role"""
        pivot_skills = {
            'Data Scientist': ['python', 'machine_learning', 'statistics', 'sql'],
            'Data Engineer': ['python', 'sql', 'spark', 'cloud', 'etl'],
            'Product Manager': ['product_strategy', 'user_research', 'roadmapping', 'analytics'],
            'Solutions Architect': ['system_design', 'cloud', 'architecture_patterns', 'consulting']
        }
        return pivot_skills.get(role, ['skill_1', 'skill_2', 'skill_3'])

    def _analyze_career_path(
        self,
        path: Dict,
        worker_profile: Dict,
        time_horizon: int
    ) -> Dict:
        """Analyze a career path with detailed metrics"""
        target_role = path['target_role']
        path_type = path['path_type']

        # Simulate market data (in production, fetch real data)
        income_data = self._get_income_projection(target_role, time_horizon)
        market_demand = self._assess_market_demand(target_role)
        job_satisfaction = self._estimate_satisfaction(target_role, worker_profile)
        transition_difficulty = self._calculate_transition_difficulty(path, worker_profile)

        # Calculate overall score
        overall_score = (
            income_data['growth_potential'] * 0.3 +
            market_demand * 0.3 +
            job_satisfaction * 0.2 +
            (100 - transition_difficulty) * 0.2
        )

        return {
            **path,
            'income_potential': income_data['peak_salary'],
            'income_growth': income_data['growth_rate'],
            'market_demand': market_demand,
            'job_satisfaction': job_satisfaction,
            'work_life_balance': self._estimate_work_life_balance(target_role),
            'automation_risk': self._assess_automation_risk(target_role),
            'transition_difficulty': transition_difficulty,
            'overall_score': round(overall_score, 1),
            'pros': self._identify_pros(target_role, path_type),
            'cons': self._identify_cons(target_role, path_type),
            'salary_trajectory': income_data['trajectory']
        }

    def _get_income_projection(self, role: str, years: int) -> Dict:
        """Project income for role over time horizon"""
        # Salary database (simplified)
        base_salaries = {
            'Data Scientist': 110000,
            'Senior Data Analyst': 95000,
            'Data Engineer': 115000,
            'Product Manager': 120000,
            'Engineering Manager': 140000,
            'Solutions Architect': 130000
        }

        base = base_salaries.get(role, 80000)
        growth_rate = 5  # 5% annual growth

        trajectory = []
        for year in range(years + 1):
            salary = int(base * ((1 + growth_rate/100) ** year))
            trajectory.append({'year': year, 'salary': salary})

        return {
            'base_salary': base,
            'peak_salary': trajectory[-1]['salary'],
            'growth_rate': growth_rate,
            'growth_potential': min((trajectory[-1]['salary'] - base) / base * 100, 100),
            'trajectory': trajectory
        }

    def _assess_market_demand(self, role: str) -> float:
        """Assess market demand for role (0-100)"""
        demand_scores = {
            'Data Scientist': 88,
            'Data Engineer': 92,
            'Product Manager': 85,
            'Software Engineer': 90,
            'Solutions Architect': 82,
            'Engineering Manager': 78
        }
        return demand_scores.get(role, 70)

    def _estimate_satisfaction(self, role: str, worker_profile: Dict) -> float:
        """Estimate job satisfaction (0-100)"""
        # Simplified - in production, use personality matching
        satisfaction_scores = {
            'Data Scientist': 82,
            'Product Manager': 85,
            'Data Engineer': 78,
            'Engineering Manager': 75,
            'Solutions Architect': 80
        }
        return satisfaction_scores.get(role, 75)

    def _estimate_work_life_balance(self, role: str) -> float:
        """Estimate work-life balance (0-100, higher is better)"""
        balance_scores = {
            'Data Scientist': 75,
            'Data Engineer': 70,
            'Product Manager': 65,
            'Engineering Manager': 60,
            'Solutions Architect': 68
        }
        return balance_scores.get(role, 70)

    def _assess_automation_risk(self, role: str) -> float:
        """Assess automation risk (0-100, higher is more risk)"""
        risk_scores = {
            'Data Scientist': 25,
            'Product Manager': 15,
            'Engineering Manager': 10,
            'Data Engineer': 30,
            'Solutions Architect': 20
        }
        return risk_scores.get(role, 40)

    def _calculate_transition_difficulty(self, path: Dict, worker_profile: Dict) -> float:
        """Calculate difficulty of transition (0-100)"""
        base_difficulty = {
            'vertical': 40,
            'lateral': 25,
            'pivot': 70
        }.get(path['path_type'], 50)

        # Adjust based on experience
        years_exp = worker_profile.get('years_experience', 0)
        if years_exp > 5:
            base_difficulty -= 10
        elif years_exp < 2:
            base_difficulty += 15

        return max(0, min(100, base_difficulty))

    def _identify_pros(self, role: str, path_type: str) -> List[str]:
        """Identify advantages of this path"""
        general_pros = {
            'vertical': ['Higher salary', 'More responsibility', 'Leadership experience'],
            'lateral': ['New skills', 'Lower risk', 'Faster transition'],
            'pivot': ['Career fulfillment', 'Market opportunity', 'Skill diversification']
        }

        role_specific = {
            'Data Scientist': ['High demand', 'Interesting problems', 'Cutting-edge tech'],
            'Product Manager': ['Strategic impact', 'Cross-functional work', 'Business acumen'],
            'Data Engineer': ['Strong demand', 'Infrastructure building', 'Scalable systems']
        }

        return general_pros.get(path_type, []) + role_specific.get(role, [])[:2]

    def _identify_cons(self, role: str, path_type: str) -> List[str]:
        """Identify challenges of this path"""
        general_cons = {
            'vertical': ['More stress', 'Longer hours', 'Political navigation'],
            'lateral': ['Similar salary', 'Repetitive work', 'Limited growth'],
            'pivot': ['Skill gaps', 'Starting over', 'Income dip']
        }

        role_specific = {
            'Data Scientist': ['Steep learning curve', 'Math-heavy', 'Tool complexity'],
            'Product Manager': ['Ambiguous metrics', 'Stakeholder management', 'Always on call'],
            'Engineering Manager': ['Less coding', 'People problems', 'Meeting heavy']
        }

        return general_cons.get(path_type, []) + role_specific.get(role, [])[:2]

    def plan_career_transition(
        self,
        current_role: str,
        target_role: str,
        worker_data: Dict,
        constraints: Dict
    ) -> Dict:
        """
        Create detailed transition plan from current to target role

        Returns:
            Comprehensive transition strategy with phases and milestones
        """
        # Analyze gap
        skill_gap = self._analyze_transition_gap(current_role, target_role, worker_data)

        # Create phased plan
        timeline_months = constraints.get('timeline_months', 12)
        budget = constraints.get('budget', 1000)

        phases = self._create_transition_phases(
            skill_gap,
            timeline_months,
            budget
        )

        # Identify risks and mitigation
        risks = self._identify_transition_risks(current_role, target_role, worker_data)

        # Calculate probability of success
        success_probability = self._calculate_success_probability(
            worker_data,
            skill_gap,
            timeline_months
        )

        return {
            'current_role': current_role,
            'target_role': target_role,
            'timeline_months': timeline_months,
            'success_probability': success_probability,
            'skill_gap_analysis': skill_gap,
            'transition_phases': phases,
            'risks': risks,
            'mitigation_strategies': self._create_mitigation_strategies(risks),
            'key_milestones': self._define_milestones(phases),
            'resource_requirements': {
                'time_commitment_hours_per_week': 10 if timeline_months > 6 else 15,
                'estimated_budget': budget,
                'support_needed': ['Mentor', 'Study group', 'Portfolio reviews']
            },
            'decision_points': self._identify_decision_points(timeline_months),
            'recommendations': [
                f"Start with Phase 1: {phases[0]['name']}",
                f"Aim for {success_probability}% probability of success",
                "Build portfolio projects in months 3-6",
                "Start applying in month 9"
            ],
            'next_steps': [
                phases[0]['actions'][0],
                "Set up weekly progress tracking",
                "Find accountability partner",
                "Schedule monthly self-assessments"
            ]
        }

    def _analyze_transition_gap(
        self,
        current_role: str,
        target_role: str,
        worker_data: Dict
    ) -> Dict:
        """Analyze gap between current and target role"""
        current_skills = set(worker_data.get('skills', []))
        target_skills = set(self._get_pivot_skills(target_role))

        missing_skills = target_skills - current_skills
        transferable_skills = current_skills & target_skills

        return {
            'missing_skills': list(missing_skills),
            'transferable_skills': list(transferable_skills),
            'skill_gap_percentage': len(missing_skills) / len(target_skills) * 100 if target_skills else 0,
            'experience_gap_years': max(0, 3 - worker_data.get('years_experience', 0)),
            'readiness_score': 100 - (len(missing_skills) / len(target_skills) * 100 if target_skills else 0)
        }

    def _create_transition_phases(
        self,
        skill_gap: Dict,
        timeline_months: int,
        budget: int
    ) -> List[Dict]:
        """Create phased transition plan"""
        phases = [
            {
                'phase': 1,
                'name': 'Foundation Building',
                'duration_months': int(timeline_months * 0.3),
                'focus': 'Learn core missing skills',
                'actions': [
                    f"Complete courses for: {', '.join(skill_gap['missing_skills'][:3])}",
                    "Build 1-2 small projects",
                    "Join online communities"
                ],
                'success_criteria': 'Completed foundational courses, built demo projects'
            },
            {
                'phase': 2,
                'name': 'Portfolio Development',
                'duration_months': int(timeline_months * 0.3),
                'focus': 'Build impressive portfolio',
                'actions': [
                    "Complete 2-3 substantial projects",
                    "Contribute to open source",
                    "Write blog posts about learnings"
                ],
                'success_criteria': '3 portfolio projects demonstrating target role skills'
            },
            {
                'phase': 3,
                'name': 'Market Preparation',
                'duration_months': int(timeline_months * 0.2),
                'focus': 'Prepare for job search',
                'actions': [
                    "Polish resume and LinkedIn",
                    "Practice interviews",
                    "Activate network for referrals"
                ],
                'success_criteria': 'Interview-ready, strong portfolio, active applications'
            },
            {
                'phase': 4,
                'name': 'Active Transition',
                'duration_months': int(timeline_months * 0.2),
                'focus': 'Land target role',
                'actions': [
                    "Apply to 20+ positions",
                    "Take interviews",
                    "Negotiate offers"
                ],
                'success_criteria': 'Accepted offer in target role'
            }
        ]

        return phases

    def _identify_transition_risks(
        self,
        current_role: str,
        target_role: str,
        worker_data: Dict
    ) -> List[Dict]:
        """Identify risks in career transition"""
        return [
            {
                'risk': 'Skill gaps too large',
                'probability': 'medium',
                'impact': 'high',
                'indicator': 'Unable to complete projects'
            },
            {
                'risk': 'Market saturation',
                'probability': 'low',
                'impact': 'medium',
                'indicator': 'Few job openings'
            },
            {
                'risk': 'Timeline too aggressive',
                'probability': 'medium',
                'impact': 'medium',
                'indicator': 'Falling behind milestones'
            },
            {
                'risk': 'Financial constraints',
                'probability': 'low',
                'impact': 'high',
                'indicator': 'Cannot afford courses/tools'
            }
        ]

    def _create_mitigation_strategies(self, risks: List[Dict]) -> List[Dict]:
        """Create strategies to mitigate risks"""
        return [
            {
                'risk': risk['risk'],
                'mitigation': self._get_mitigation(risk['risk'])
            }
            for risk in risks
        ]

    def _get_mitigation(self, risk: str) -> str:
        """Get mitigation strategy for risk"""
        strategies = {
            'Skill gaps too large': 'Break learning into smaller milestones, get tutor if needed',
            'Market saturation': 'Develop unique specialization, expand geographic search',
            'Timeline too aggressive': 'Add 2-3 month buffer, reduce scope if needed',
            'Financial constraints': 'Use free resources, apply for scholarships'
        }
        return strategies.get(risk, 'Monitor closely and adjust plan as needed')

    def _define_milestones(self, phases: List[Dict]) -> List[Dict]:
        """Define key milestones"""
        milestones = []
        month_counter = 0

        for phase in phases:
            month_counter += phase['duration_months']
            milestones.append({
                'month': month_counter,
                'milestone': f"Complete {phase['name']}",
                'success_criteria': phase['success_criteria']
            })

        return milestones

    def _identify_decision_points(self, timeline_months: int) -> List[Dict]:
        """Identify key decision points in transition"""
        return [
            {
                'month': 3,
                'decision': 'Continue or adjust learning pace',
                'criteria': 'Completed 30% of skill development'
            },
            {
                'month': 6,
                'decision': 'Start applying or continue building',
                'criteria': 'Portfolio has 2+ strong projects'
            },
            {
                'month': timeline_months - 2,
                'decision': 'Accept offer or continue search',
                'criteria': 'Received acceptable offer'
            }
        ]

    def _calculate_success_probability(
        self,
        worker_data: Dict,
        skill_gap: Dict,
        timeline_months: int
    ) -> int:
        """Calculate probability of successful transition"""
        base_probability = 70

        # Adjust for readiness
        readiness = skill_gap['readiness_score']
        if readiness > 70:
            base_probability += 15
        elif readiness < 40:
            base_probability -= 20

        # Adjust for timeline
        if timeline_months >= 12:
            base_probability += 10
        elif timeline_months < 6:
            base_probability -= 15

        # Adjust for experience
        years_exp = worker_data.get('years_experience', 0)
        if years_exp > 5:
            base_probability += 10

        return max(30, min(95, base_probability))

    def analyze_risk_reward(
        self,
        career_options: List[Dict],
        worker_profile: Dict
    ) -> Dict:
        """Analyze risk vs reward for career options"""
        analyzed_options = []

        for option in career_options:
            risk_score = self._calculate_risk_score(option, worker_profile)
            reward_score = self._calculate_reward_score(option, worker_profile)

            analyzed_options.append({
                'option': option['role'],
                'risk_score': risk_score,
                'reward_score': reward_score,
                'risk_reward_ratio': round(reward_score / risk_score, 2) if risk_score > 0 else 0,
                'recommendation': self._get_risk_reward_recommendation(risk_score, reward_score)
            })

        # Sort by risk-reward ratio
        analyzed_options.sort(key=lambda x: x['risk_reward_ratio'], reverse=True)

        return {
            'total_options_analyzed': len(analyzed_options),
            'options': analyzed_options,
            'best_risk_reward': analyzed_options[0] if analyzed_options else None,
            'lowest_risk': min(analyzed_options, key=lambda x: x['risk_score']) if analyzed_options else None,
            'highest_reward': max(analyzed_options, key=lambda x: x['reward_score']) if analyzed_options else None,
            'recommendations': [
                f"Best overall: {analyzed_options[0]['option']}" if analyzed_options else "No options to analyze",
                "Consider risk tolerance and personal goals",
                "Balance short-term safety with long-term growth"
            ],
            'next_steps': [
                "Deep dive into top 2-3 options",
                "Conduct informational interviews",
                "Create detailed transition plan for top choice"
            ]
        }

    def _calculate_risk_score(self, option: Dict, worker_profile: Dict) -> float:
        """Calculate risk score (0-100, higher is more risk)"""
        base_risk = 50
        # Add risk factors
        return min(100, base_risk)

    def _calculate_reward_score(self, option: Dict, worker_profile: Dict) -> float:
        """Calculate reward score (0-100, higher is more reward)"""
        base_reward = 60
        # Add reward factors
        return min(100, base_reward)

    def _get_risk_reward_recommendation(self, risk: float, reward: float) -> str:
        """Get recommendation based on risk-reward profile"""
        ratio = reward / risk if risk > 0 else 0

        if ratio > 1.5:
            return "Highly recommended - excellent risk-reward ratio"
        elif ratio > 1.0:
            return "Recommended - reward outweighs risk"
        elif ratio > 0.7:
            return "Consider carefully - balanced risk-reward"
        else:
            return "High risk - ensure you're comfortable with tradeoffs"

    def track_career_goals(
        self,
        goals: List[Dict],
        progress_data: Dict
    ) -> Dict:
        """Track progress toward career goals"""
        tracked_goals = []

        for goal in goals:
            progress = self._calculate_goal_progress(goal, progress_data)
            tracked_goals.append(progress)

        overall_progress = sum(g['progress_percentage'] for g in tracked_goals) / len(tracked_goals) if tracked_goals else 0

        return {
            'total_goals': len(tracked_goals),
            'overall_progress': round(overall_progress, 1),
            'goals': tracked_goals,
            'on_track_count': len([g for g in tracked_goals if g['status'] == 'on_track']),
            'behind_count': len([g for g in tracked_goals if g['status'] == 'behind']),
            'completed_count': len([g for g in tracked_goals if g['status'] == 'completed']),
            'recommendations': self._generate_goal_recommendations(tracked_goals),
            'next_steps': [
                "Focus on behind-schedule goals",
                "Celebrate completed milestones",
                "Adjust timelines if needed"
            ]
        }

    def _calculate_goal_progress(self, goal: Dict, progress_data: Dict) -> Dict:
        """Calculate progress for individual goal"""
        # Simplified progress calculation
        progress = progress_data.get(goal['id'], {})
        progress_pct = progress.get('percentage', 0)

        if progress_pct >= 100:
            status = 'completed'
        elif progress_pct >= 80:
            status = 'on_track'
        else:
            status = 'behind'

        return {
            **goal,
            'progress_percentage': progress_pct,
            'status': status,
            'days_remaining': goal.get('deadline_days', 30) - progress.get('days_elapsed', 0)
        }

    def _generate_goal_recommendations(self, tracked_goals: List[Dict]) -> List[str]:
        """Generate recommendations based on goal progress"""
        recommendations = []

        behind_goals = [g for g in tracked_goals if g['status'] == 'behind']
        if behind_goals:
            recommendations.append(f"Prioritize {len(behind_goals)} behind-schedule goals")

        completed = [g for g in tracked_goals if g['status'] == 'completed']
        if completed:
            recommendations.append(f"Celebrate {len(completed)} completed goals!")

        return recommendations
