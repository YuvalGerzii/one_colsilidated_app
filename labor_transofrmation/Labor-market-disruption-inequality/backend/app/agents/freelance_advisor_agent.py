"""
Freelance Advisor Agent

Specialized agent for providing intelligent guidance to freelancers on:
- Job selection and bidding strategy
- Pricing optimization
- Profile enhancement
- Career growth in the freelance marketplace
"""

from typing import Dict, List
from datetime import datetime
from .base_agent import BaseAgent, AgentResponse
from ..models.freelance_hub import FreelanceHub


class FreelanceAdvisorAgent(BaseAgent):
    """
    Agent that provides personalized freelance career guidance
    """

    def __init__(self):
        super().__init__(
            agent_id="freelance_advisor_01",
            agent_type="FreelanceAdvisor"
        )

        # Define capabilities
        self.capabilities = [
            'profile_optimization',
            'job_recommendation',
            'pricing_strategy',
            'proposal_assistance',
            'competition_analysis',
            'earnings_optimization',
            'skill_gap_identification',
            'client_acquisition_strategy'
        ]

        # Initialize the freelance hub engine
        self.hub_engine = FreelanceHub()

    def process_task(self, task: Dict) -> AgentResponse:
        """
        Process freelance advisory tasks

        Task types:
        - optimize_profile: Analyze and improve freelancer profile
        - recommend_jobs: Find best job opportunities
        - optimize_pricing: Analyze and recommend pricing strategy
        - analyze_competition: Evaluate competition for a job
        - create_proposal: Help create winning proposal
        - growth_strategy: Long-term career planning
        """
        start_time = datetime.now()
        task_type = task.get('type', 'unknown')

        try:
            if task_type == 'optimize_profile':
                result = self._optimize_profile(task)
            elif task_type == 'recommend_jobs':
                result = self._recommend_jobs(task)
            elif task_type == 'optimize_pricing':
                result = self._optimize_pricing(task)
            elif task_type == 'analyze_competition':
                result = self._analyze_competition(task)
            elif task_type == 'create_proposal':
                result = self._create_proposal(task)
            elif task_type == 'growth_strategy':
                result = self._growth_strategy(task)
            else:
                result = {
                    'error': f'Unknown task type: {task_type}',
                    'supported_types': [
                        'optimize_profile',
                        'recommend_jobs',
                        'optimize_pricing',
                        'analyze_competition',
                        'create_proposal',
                        'growth_strategy'
                    ]
                }

            # Calculate response time
            response_time = (datetime.now() - start_time).total_seconds()
            success = 'error' not in result

            # Update metrics
            self.update_metrics(success, response_time)

            return AgentResponse(
                agent_id=self.agent_id,
                agent_type=self.agent_type,
                status='success' if success else 'failed',
                data=result,
                confidence=result.get('confidence', 0.85) if success else 0.0,
                recommendations=result.get('recommendations', []),
                next_steps=result.get('next_steps', []),
                timestamp=datetime.now(),
                metadata={
                    'task_type': task_type,
                    'response_time_seconds': response_time
                }
            )

        except Exception as e:
            response_time = (datetime.now() - start_time).total_seconds()
            self.update_metrics(False, response_time)

            return AgentResponse(
                agent_id=self.agent_id,
                agent_type=self.agent_type,
                status='failed',
                data={'error': str(e)},
                confidence=0.0,
                recommendations=[],
                next_steps=['Check error details and retry'],
                timestamp=datetime.now(),
                metadata={'error': str(e)}
            )

    def analyze(self, data: Dict) -> Dict:
        """
        Analyze freelancer data and provide insights

        Args:
            data: Freelancer profile and performance data

        Returns:
            Comprehensive analysis and recommendations
        """
        freelancer = data.get('freelancer', {})
        contracts = data.get('contracts', [])
        market_data = data.get('market_data', {})

        # Calculate performance metrics
        metrics = self.hub_engine.calculate_freelancer_metrics(
            freelancer.get('id'),
            contracts
        )

        # Get pricing recommendations
        pricing = self.hub_engine.optimize_pricing_strategy(
            freelancer,
            market_data
        )

        # Identify areas for improvement
        improvement_areas = self._identify_improvement_areas(freelancer, metrics)

        # Generate action plan
        action_plan = self._generate_action_plan(freelancer, metrics, pricing)

        return {
            'performance_metrics': metrics,
            'pricing_analysis': pricing,
            'improvement_areas': improvement_areas,
            'action_plan': action_plan,
            'overall_health_score': self._calculate_health_score(metrics, pricing),
            'confidence': 0.9
        }

    def _optimize_profile(self, task: Dict) -> Dict:
        """Analyze profile and suggest optimizations"""
        freelancer = task.get('freelancer', {})
        market_data = task.get('market_data', {})

        suggestions = []
        priority_actions = []

        # Check profile completeness
        bio = freelancer.get('bio', '')
        if not bio or len(bio) < 100:
            suggestions.append({
                'area': 'bio',
                'issue': 'Bio is missing or too short',
                'recommendation': 'Write a compelling bio (200-400 words) highlighting your expertise and value proposition',
                'impact': 'high',
                'priority': 1
            })
            priority_actions.append('Complete your professional bio')

        # Check hourly rate
        hourly_rate = freelancer.get('hourly_rate', 0)
        if hourly_rate == 0:
            suggestions.append({
                'area': 'pricing',
                'issue': 'No hourly rate set',
                'recommendation': 'Set competitive hourly rate based on your skills and experience',
                'impact': 'critical',
                'priority': 1
            })
            priority_actions.append('Set your hourly rate')

        # Check skills
        skills = freelancer.get('skills', [])
        if len(skills) < 5:
            suggestions.append({
                'area': 'skills',
                'issue': 'Too few skills listed',
                'recommendation': 'Add more relevant skills (aim for 8-12) to improve discoverability',
                'impact': 'high',
                'priority': 2
            })
            priority_actions.append('Add more skills to your profile')

        # Check portfolio
        portfolio_count = len(freelancer.get('portfolio_items', []))
        if portfolio_count < 3:
            suggestions.append({
                'area': 'portfolio',
                'issue': 'Insufficient portfolio items',
                'recommendation': 'Add at least 3-5 portfolio pieces showcasing your best work',
                'impact': 'high',
                'priority': 2
            })
            priority_actions.append('Build your portfolio (minimum 3 items)')

        # Check availability
        if not freelancer.get('is_available', False):
            suggestions.append({
                'area': 'availability',
                'issue': 'Profile marked as unavailable',
                'recommendation': 'Update availability status to receive job recommendations',
                'impact': 'medium',
                'priority': 3
            })

        # Profile strength score
        strength_score = self._calculate_profile_strength(freelancer)

        return {
            'profile_strength_score': strength_score,
            'suggestions': suggestions,
            'priority_actions': priority_actions,
            'estimated_improvement': f"{min(100 - strength_score, 30)}% increase in job matches",
            'next_steps': priority_actions[:3],
            'recommendations': [
                'Complete high-priority actions first',
                'Update profile regularly to stay competitive',
                'Ask satisfied clients for reviews'
            ],
            'confidence': 0.9
        }

    def _recommend_jobs(self, task: Dict) -> Dict:
        """Recommend best jobs for freelancer"""
        freelancer = task.get('freelancer', {})
        available_jobs = task.get('available_jobs', [])
        limit = task.get('limit', 10)

        # Get recommendations from engine
        recommendations = self.hub_engine.recommend_jobs_for_freelancer(
            freelancer,
            available_jobs,
            limit
        )

        # Add strategic advice for each recommendation
        for rec in recommendations:
            rec['bidding_advice'] = self._generate_bidding_advice(rec, freelancer)

        # Categorize recommendations
        high_value = [r for r in recommendations if r['recommendation_score'] >= 80]
        good_fit = [r for r in recommendations if 60 <= r['recommendation_score'] < 80]
        backup_options = [r for r in recommendations if r['recommendation_score'] < 60]

        return {
            'total_opportunities': len(recommendations),
            'high_value_opportunities': high_value,
            'good_fit_opportunities': good_fit,
            'backup_options': backup_options,
            'recommendations': [
                'Focus on high-value opportunities first',
                'Submit proposals within 24 hours for best results',
                'Customize each proposal to the specific job'
            ],
            'next_steps': [
                f'Review top {min(3, len(high_value))} high-value opportunities',
                'Prepare customized proposals',
                'Set aside time for client communication'
            ],
            'confidence': 0.88
        }

    def _optimize_pricing(self, task: Dict) -> Dict:
        """Analyze and optimize pricing strategy"""
        freelancer = task.get('freelancer', {})
        market_data = task.get('market_data', {})
        contracts = task.get('contracts', [])

        # Get pricing optimization from engine
        pricing_analysis = self.hub_engine.optimize_pricing_strategy(
            freelancer,
            market_data
        )

        # Calculate earnings potential
        current_rate = freelancer.get('hourly_rate', 0)
        recommended_rate = pricing_analysis['recommended_rate']
        monthly_hours = 160  # Full-time equivalent

        current_monthly = current_rate * monthly_hours
        optimized_monthly = recommended_rate * monthly_hours
        annual_increase = (optimized_monthly - current_monthly) * 12

        # Rate implementation strategy
        implementation_strategy = self._generate_rate_change_strategy(
            current_rate,
            recommended_rate
        )

        return {
            **pricing_analysis,
            'earnings_potential': {
                'current_monthly': round(current_monthly, 2),
                'optimized_monthly': round(optimized_monthly, 2),
                'monthly_increase': round(optimized_monthly - current_monthly, 2),
                'annual_increase': round(annual_increase, 2)
            },
            'implementation_strategy': implementation_strategy,
            'next_steps': [
                'Test new rate on next 3-5 projects',
                'Monitor client response and acceptance rate',
                'Adjust based on market feedback'
            ],
            'confidence': 0.85
        }

    def _analyze_competition(self, task: Dict) -> Dict:
        """Analyze competition for a specific job"""
        job_posting = task.get('job_posting', {})
        proposals = task.get('proposals', [])
        freelancer = task.get('freelancer', {})

        # Get competition analysis from engine
        competition = self.hub_engine.analyze_competition(job_posting, proposals)

        # Generate competitive strategy
        strategy = self._generate_competitive_strategy(
            job_posting,
            competition,
            freelancer
        )

        return {
            **competition,
            'competitive_strategy': strategy,
            'win_probability': self._estimate_win_probability(
                freelancer,
                competition
            ),
            'next_steps': strategy['action_items'],
            'recommendations': strategy['key_recommendations'],
            'confidence': 0.82
        }

    def _create_proposal(self, task: Dict) -> Dict:
        """Help create a winning proposal"""
        freelancer = task.get('freelancer', {})
        job_posting = task.get('job_posting', {})

        # Generate proposal template
        template = self.hub_engine.generate_proposal_template(
            freelancer,
            job_posting
        )

        # Add enhancement tips
        enhancement_tips = [
            'Personalize the introduction with specific details from the job posting',
            'Include 2-3 relevant examples from your portfolio',
            'Address potential client concerns proactively',
            'End with a clear call-to-action',
            'Proofread carefully for grammar and spelling'
        ]

        # Identify key selling points
        selling_points = self._identify_selling_points(freelancer, job_posting)

        return {
            **template,
            'enhancement_tips': enhancement_tips,
            'selling_points': selling_points,
            'do_list': [
                'Customize template for this specific job',
                'Highlight relevant experience',
                'Show enthusiasm and interest',
                'Be specific about deliverables'
            ],
            'dont_list': [
                "Don't use generic templates",
                "Don't overpromise on timeline",
                "Don't focus only on price",
                "Don't write overly long proposals (keep under 300 words)"
            ],
            'next_steps': [
                'Customize the template sections',
                'Add portfolio links',
                'Review and submit within 24 hours'
            ],
            'confidence': 0.87
        }

    def _growth_strategy(self, task: Dict) -> Dict:
        """Develop long-term growth strategy"""
        freelancer = task.get('freelancer', {})
        contracts = task.get('contracts', [])
        goals = task.get('goals', {})

        # Calculate current performance
        metrics = self.hub_engine.calculate_freelancer_metrics(
            freelancer.get('id'),
            contracts
        )

        # Define growth targets
        growth_targets = self._define_growth_targets(freelancer, metrics, goals)

        # Create growth roadmap
        roadmap = self._create_growth_roadmap(freelancer, metrics, growth_targets)

        # Identify skill gaps for premium services
        skill_gaps = self._identify_premium_skill_gaps(freelancer)

        return {
            'current_performance': metrics,
            'growth_targets': growth_targets,
            'roadmap': roadmap,
            'skill_development_plan': skill_gaps,
            'milestones': roadmap['milestones'],
            'recommendations': roadmap['key_strategies'],
            'next_steps': roadmap['immediate_actions'],
            'confidence': 0.83
        }

    # ==================== HELPER METHODS ====================

    def _calculate_profile_strength(self, freelancer: Dict) -> float:
        """Calculate profile completeness/strength score (0-100)"""
        score = 0

        # Bio (20 points)
        bio = freelancer.get('bio', '')
        if bio:
            score += min(20, len(bio) / 10)  # Max 20 points for 200+ chars

        # Hourly rate (10 points)
        if freelancer.get('hourly_rate', 0) > 0:
            score += 10

        # Skills (20 points)
        skills_count = len(freelancer.get('skills', []))
        score += min(20, skills_count * 2)  # Max 20 points for 10+ skills

        # Portfolio (20 points)
        portfolio_count = len(freelancer.get('portfolio_items', []))
        score += min(20, portfolio_count * 5)  # Max 20 points for 4+ items

        # Rating (15 points)
        rating = freelancer.get('rating_average', 0)
        score += (rating / 5.0) * 15

        # Jobs completed (15 points)
        jobs = freelancer.get('total_jobs_completed', 0)
        score += min(15, jobs)

        return round(min(100, score), 1)

    def _identify_improvement_areas(self, freelancer: Dict, metrics: Dict) -> List[Dict]:
        """Identify specific areas for improvement"""
        areas = []

        # Check success rate
        if metrics['success_rate'] < 90:
            areas.append({
                'area': 'Project Completion',
                'current': f"{metrics['success_rate']}%",
                'target': '95%+',
                'actions': [
                    'Set realistic deadlines',
                    'Improve project scoping',
                    'Communicate proactively with clients'
                ]
            })

        # Check rating
        if metrics['avg_rating'] < 4.5:
            areas.append({
                'area': 'Client Satisfaction',
                'current': f"{metrics['avg_rating']:.1f}/5",
                'target': '4.7+/5',
                'actions': [
                    'Exceed client expectations',
                    'Request feedback mid-project',
                    'Provide exceptional customer service'
                ]
            })

        # Check on-time delivery
        if metrics['on_time_delivery_rate'] < 95:
            areas.append({
                'area': 'On-Time Delivery',
                'current': f"{metrics['on_time_delivery_rate']}%",
                'target': '98%+',
                'actions': [
                    'Build in buffer time',
                    'Use project management tools',
                    'Communicate early if delays occur'
                ]
            })

        return areas

    def _calculate_health_score(self, metrics: Dict, pricing: Dict) -> float:
        """Calculate overall freelance career health score"""
        # Component scores
        performance_score = (
            metrics['success_rate'] +
            (metrics['avg_rating'] / 5.0 * 100) +
            metrics['on_time_delivery_rate']
        ) / 3

        # Pricing score (how close to market rate)
        current = pricing['current_hourly_rate']
        recommended = pricing['recommended_rate']
        pricing_score = min(100, (current / recommended) * 100) if recommended > 0 else 50

        # Volume score
        jobs = metrics['jobs_completed']
        volume_score = min(100, jobs * 2)  # Max at 50 jobs

        # Overall health
        health = (performance_score * 0.5 + pricing_score * 0.3 + volume_score * 0.2)

        return round(health, 1)

    def _generate_action_plan(
        self,
        freelancer: Dict,
        metrics: Dict,
        pricing: Dict
    ) -> List[Dict]:
        """Generate prioritized action plan"""
        actions = []

        # Pricing action
        if pricing['positioning'] == 'underpriced':
            actions.append({
                'priority': 1,
                'action': 'Increase hourly rate',
                'details': f"Raise rate from ${pricing['current_hourly_rate']} to ${pricing['recommended_rate']}",
                'timeline': '1-2 weeks',
                'impact': 'High'
            })

        # Profile action
        if not freelancer.get('bio'):
            actions.append({
                'priority': 1,
                'action': 'Complete profile bio',
                'details': 'Write 200-400 word professional bio',
                'timeline': '1 day',
                'impact': 'High'
            })

        # Portfolio action
        if len(freelancer.get('portfolio_items', [])) < 3:
            actions.append({
                'priority': 2,
                'action': 'Build portfolio',
                'details': 'Add 3-5 high-quality portfolio pieces',
                'timeline': '1 week',
                'impact': 'High'
            })

        return sorted(actions, key=lambda x: x['priority'])

    def _generate_bidding_advice(self, job_rec: Dict, freelancer: Dict) -> str:
        """Generate specific bidding advice for a job"""
        competition = job_rec.get('competition', 'medium')
        match_score = job_rec.get('recommendation_score', 0)

        if match_score >= 80 and competition == 'low':
            return "Strong opportunity - bid confidently at your standard rate"
        elif match_score >= 80 and competition == 'high':
            return "Great fit but competitive - emphasize unique value proposition"
        elif match_score >= 60:
            return "Good match - competitive pricing with strong proposal"
        else:
            return "Lower priority - bid only if capacity allows"

    def _generate_rate_change_strategy(self, current: float, target: float) -> Dict:
        """Generate strategy for implementing rate changes"""
        if target <= current:
            return {
                'approach': 'maintain',
                'steps': ['Your current rate is competitive', 'Monitor market trends quarterly'],
                'timeline': 'N/A'
            }

        increase_pct = ((target - current) / current) * 100

        if increase_pct <= 10:
            return {
                'approach': 'immediate',
                'steps': [
                    'Update rate for all new proposals immediately',
                    'Notify existing clients of upcoming rate change'
                ],
                'timeline': '1 week'
            }
        else:
            return {
                'approach': 'gradual',
                'steps': [
                    f'Increase rate by 50% of target ({((target - current) / 2 + current):.2f}) initially',
                    'Test market acceptance for 4-6 weeks',
                    'Complete increase to target rate',
                    'Apply new rate to new clients first'
                ],
                'timeline': '2-3 months'
            }

    def _generate_competitive_strategy(
        self,
        job: Dict,
        competition: Dict,
        freelancer: Dict
    ) -> Dict:
        """Generate strategy for winning in competitive environment"""
        comp_level = competition['competition_level']
        avg_rate = competition['avg_proposed_rate']

        if comp_level == 'low':
            strategy = {
                'positioning': 'value',
                'pricing_approach': 'Standard rate',
                'key_recommendations': [
                    'Submit proposal quickly (low competition)',
                    'Focus on quality and expertise',
                    'Include relevant portfolio samples'
                ],
                'action_items': [
                    'Submit within 24 hours',
                    'Emphasize unique qualifications',
                    'Attach 2-3 portfolio pieces'
                ]
            }
        elif comp_level == 'medium':
            strategy = {
                'positioning': 'differentiated',
                'pricing_approach': 'Competitive but not lowest',
                'key_recommendations': [
                    'Differentiate with unique approach',
                    'Highlight relevant experience',
                    'Offer added value (e.g., faster delivery, revisions)'
                ],
                'action_items': [
                    'Craft customized proposal',
                    'Address job requirements specifically',
                    'Include satisfaction guarantee'
                ]
            }
        else:  # high competition
            strategy = {
                'positioning': 'exceptional',
                'pricing_approach': 'Value-focused, not price-focused',
                'key_recommendations': [
                    'Stand out with exceptional proposal quality',
                    'Demonstrate deep understanding of requirements',
                    'Showcase highly relevant past work',
                    'Consider video proposal for extra impact'
                ],
                'action_items': [
                    'Research client background thoroughly',
                    'Create custom proposal (no template)',
                    'Provide detailed project approach',
                    'Follow up professionally'
                ]
            }

        return strategy

    def _estimate_win_probability(self, freelancer: Dict, competition: Dict) -> float:
        """Estimate probability of winning the job"""
        base_prob = 0.5

        # Adjust for rating
        rating = freelancer.get('rating_average', 0)
        if rating >= 4.8:
            base_prob += 0.15
        elif rating >= 4.5:
            base_prob += 0.08

        # Adjust for competition
        comp_level = competition['competition_level']
        if comp_level == 'low':
            base_prob += 0.2
        elif comp_level == 'high':
            base_prob -= 0.15

        # Adjust for experience
        jobs = freelancer.get('total_jobs_completed', 0)
        if jobs >= 50:
            base_prob += 0.1
        elif jobs < 5:
            base_prob -= 0.1

        return round(min(0.95, max(0.05, base_prob)), 2)

    def _identify_selling_points(self, freelancer: Dict, job: Dict) -> List[str]:
        """Identify key selling points for this freelancer/job combo"""
        points = []

        # Rating
        rating = freelancer.get('rating_average', 0)
        if rating >= 4.7:
            points.append(f"Top-rated professional ({rating:.1f}/5 stars)")

        # Experience
        jobs = freelancer.get('total_jobs_completed', 0)
        if jobs >= 50:
            points.append(f"Proven track record ({jobs} completed projects)")

        # Success rate
        success_rate = freelancer.get('success_rate', 0)
        if success_rate >= 95:
            points.append(f"{success_rate}% project success rate")

        # Skills match
        freelancer_skills = set(freelancer.get('skills', []))
        job_skills = set(job.get('required_skills', []))
        if len(freelancer_skills & job_skills) >= 3:
            points.append("Perfect skill match for this project")

        # Response time
        if freelancer.get('response_time_hours', 24) <= 6:
            points.append("Fast communication (typically responds within 6 hours)")

        return points

    def _define_growth_targets(
        self,
        freelancer: Dict,
        metrics: Dict,
        goals: Dict
    ) -> Dict:
        """Define growth targets based on current state and goals"""
        current_earnings = metrics['total_earnings']
        current_rate = freelancer.get('hourly_rate', 0)

        # Default to 50% growth if no goals specified
        target_annual_income = goals.get('annual_income', current_earnings * 1.5)
        target_rate = goals.get('hourly_rate', current_rate * 1.3)

        return {
            '6_months': {
                'monthly_income': target_annual_income / 12 * 0.5,
                'hourly_rate': current_rate * 1.15,
                'jobs_per_month': 8,
                'rating_target': max(4.5, metrics['avg_rating'])
            },
            '12_months': {
                'monthly_income': target_annual_income / 12,
                'hourly_rate': target_rate,
                'jobs_per_month': 10,
                'rating_target': 4.7
            },
            '24_months': {
                'monthly_income': target_annual_income / 12 * 1.5,
                'hourly_rate': target_rate * 1.3,
                'jobs_per_month': 12,
                'rating_target': 4.8
            }
        }

    def _create_growth_roadmap(
        self,
        freelancer: Dict,
        metrics: Dict,
        targets: Dict
    ) -> Dict:
        """Create detailed growth roadmap"""
        return {
            'phases': [
                {
                    'name': 'Foundation (Months 1-3)',
                    'focus': 'Build reputation and client base',
                    'goals': [
                        'Complete 15-20 successful projects',
                        'Achieve 4.5+ rating',
                        'Build portfolio with 5+ pieces'
                    ]
                },
                {
                    'name': 'Growth (Months 4-9)',
                    'focus': 'Scale income and increase rates',
                    'goals': [
                        'Increase hourly rate by 20%',
                        'Develop 3-5 repeat clients',
                        'Specialize in high-value services'
                    ]
                },
                {
                    'name': 'Optimization (Months 10-12)',
                    'focus': 'Premium positioning and efficiency',
                    'goals': [
                        'Position as premium provider',
                        'Optimize for high-value projects only',
                        'Develop passive income streams'
                    ]
                }
            ],
            'milestones': [
                {'month': 3, 'milestone': 'First 20 projects completed'},
                {'month': 6, 'milestone': 'Rate increased to target level'},
                {'month': 9, 'milestone': '50% of income from repeat clients'},
                {'month': 12, 'milestone': 'Top-rated status achieved'}
            ],
            'key_strategies': [
                'Focus on quality over quantity',
                'Build long-term client relationships',
                'Continuously upgrade skills',
                'Develop signature service offering',
                'Optimize for recurring revenue'
            ],
            'immediate_actions': [
                'Complete profile optimization',
                'Apply to 3-5 high-value jobs this week',
                'Request reviews from recent satisfied clients'
            ]
        }

    def _identify_premium_skill_gaps(self, freelancer: Dict) -> Dict:
        """Identify skills needed to command premium rates"""
        current_skills = set(freelancer.get('skills', []))
        category = freelancer.get('primary_category', 'web_development')

        # Premium skills by category
        premium_skills_map = {
            'web_development': ['react', 'vue', 'node', 'aws', 'docker', 'typescript'],
            'mobile_development': ['swift', 'kotlin', 'react_native', 'flutter'],
            'graphic_design': ['figma', 'adobe_xd', 'ui_ux', 'brand_strategy'],
            'data_analysis': ['machine_learning', 'python', 'r', 'tableau', 'sql'],
            'writing': ['seo', 'content_strategy', 'copywriting', 'technical_writing']
        }

        premium_skills = set(premium_skills_map.get(category, []))
        missing_skills = premium_skills - current_skills

        return {
            'current_premium_skills': list(current_skills & premium_skills),
            'missing_premium_skills': list(missing_skills),
            'priority_learning': list(missing_skills)[:3],
            'estimated_rate_increase': f"{len(missing_skills) * 5}% potential increase",
            'learning_resources': [
                'Online courses (Udemy, Coursera)',
                'Practice projects for portfolio',
                'Industry certifications'
            ]
        }
