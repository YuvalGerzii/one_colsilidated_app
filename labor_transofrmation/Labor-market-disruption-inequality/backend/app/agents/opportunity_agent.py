"""
Opportunity Discovery Agent
Proactively identifies opportunities, hidden job markets, and career paths
"""
from typing import Dict, List
from datetime import datetime, timedelta
import numpy as np
from .base_agent import BaseAgent, AgentResponse

class OpportunityDiscoveryAgent(BaseAgent):
    """
    Discovers opportunities that workers might miss
    - Hidden job markets
    - Emerging roles
    - Alternative career paths
    - Networking opportunities
    - Skill monetization options
    """

    def __init__(self, agent_id: str = "opportunity_scout_01"):
        super().__init__(agent_id, "OpportunityDiscovery")
        self.capabilities = [
            'hidden_job_discovery',
            'emerging_role_identification',
            'alternative_path_finding',
            'networking_opportunity_matching',
            'freelance_opportunity_discovery'
        ]

    def process_task(self, task: Dict) -> AgentResponse:
        """Process opportunity discovery task"""
        start_time = datetime.now()

        task_type = task.get('type', 'unknown')

        if task_type == 'discover_opportunities':
            result = self.discover_all_opportunities(
                task.get('worker_profile'),
                task.get('constraints', {})
            )
            status = 'success'
        elif task_type == 'find_hidden_jobs':
            result = self.find_hidden_job_market(
                task.get('worker_profile'),
                task.get('target_role')
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
            confidence=0.80,
            recommendations=result.get('recommendations', []),
            next_steps=result.get('action_items', []),
            timestamp=datetime.now(),
            metadata={'response_time': response_time}
        )

    def analyze(self, data: Dict) -> Dict:
        """Analyze for opportunities"""
        return self.discover_all_opportunities(
            data.get('worker_profile'),
            data.get('constraints', {})
        )

    def discover_all_opportunities(self, worker_profile: Dict, constraints: Dict) -> Dict:
        """
        Comprehensive opportunity discovery across multiple dimensions
        """
        opportunities = {
            'traditional_jobs': self._find_traditional_jobs(worker_profile),
            'hidden_market': self._discover_hidden_market(worker_profile),
            'emerging_roles': self._identify_emerging_roles(worker_profile),
            'freelance': self._find_freelance_opportunities(worker_profile),
            'entrepreneurial': self._identify_entrepreneurial_paths(worker_profile),
            'networking': self._find_networking_opportunities(worker_profile),
            'skill_monetization': self._find_skill_monetization(worker_profile),
            'alternative_careers': self._discover_alternative_paths(worker_profile)
        }

        # Aggregate and prioritize
        all_opps = []
        for category, opps in opportunities.items():
            for opp in opps:
                opp['category'] = category
                all_opps.append(opp)

        prioritized = self._prioritize_opportunities(all_opps, worker_profile)

        return {
            'total_opportunities_found': len(all_opps),
            'by_category': {k: len(v) for k, v in opportunities.items()},
            'top_opportunities': prioritized[:10],
            'opportunities_breakdown': opportunities,
            'recommendations': self._generate_opportunity_recommendations(prioritized),
            'action_items': self._generate_action_items(prioritized[:5])
        }

    def _find_traditional_jobs(self, profile: Dict) -> List[Dict]:
        """Find traditional job postings"""
        # Simulate job discovery
        jobs = []
        skills = profile.get('skills', [])

        # Generate mock opportunities based on skills
        if 'python' in skills:
            jobs.append({
                'title': 'Python Developer',
                'company': 'Tech Corp',
                'match_score': 85,
                'salary_range': '$80K-$120K',
                'source': 'LinkedIn',
                'discovery_method': 'skill_match'
            })

        jobs.append({
            'title': f"{profile.get('current_role', 'Professional')} - Senior Level",
            'company': 'Growing Startup',
            'match_score': 78,
            'salary_range': '$90K-$130K',
            'source': 'Indeed',
            'discovery_method': 'experience_match'
        })

        return jobs

    def _discover_hidden_market(self, profile: Dict) -> List[Dict]:
        """
        Discover hidden job market opportunities
        - Unadvertised positions
        - Direct hiring
        - Referral opportunities
        """
        hidden_opps = []

        hidden_opps.append({
            'title': 'Unadvertised Position via Referral',
            'company': 'Network Connection Company',
            'description': 'Position not publicly posted, accessible through professional network',
            'access_method': 'Contact John Doe in your network',
            'match_score': 82,
            'discovery_method': 'network_analysis',
            'effort_required': 'Medium - requires networking outreach'
        })

        hidden_opps.append({
            'title': 'Direct Company Outreach',
            'company': 'Target Company in Your Field',
            'description': 'Companies often hire before posting publicly',
            'access_method': 'Direct email to hiring manager',
            'match_score': 75,
            'discovery_method': 'proactive_targeting',
            'effort_required': 'High - cold outreach required'
        })

        return hidden_opps

    def _identify_emerging_roles(self, profile: Dict) -> List[Dict]:
        """Identify new/emerging roles that didn't exist 2-3 years ago"""
        emerging = []

        emerging.append({
            'title': 'AI Prompt Engineer',
            'description': 'New role focusing on optimizing AI interactions',
            'market_size': 'Growing rapidly',
            'avg_salary': '$95K-$140K',
            'skills_needed': ['LLMs', 'AI', 'Communication'],
            'current_match': 65,
            'discovery_method': 'trend_analysis',
            'opportunity_score': 90  # High opportunity, low competition
        })

        emerging.append({
            'title': 'Automation Specialist',
            'description': 'Help companies implement workflow automation',
            'market_size': 'High demand',
            'avg_salary': '$85K-$125K',
            'skills_needed': ['Python', 'RPA', 'Business Analysis'],
            'current_match': 72,
            'discovery_method': 'market_gap_analysis',
            'opportunity_score': 85
        })

        return emerging

    def _find_freelance_opportunities(self, profile: Dict) -> List[Dict]:
        """Find freelance and contract opportunities"""
        freelance = []

        skills = profile.get('skills', [])

        if 'python' in skills or 'programming' in str(skills).lower():
            freelance.append({
                'platform': 'Upwork',
                'opportunity_type': 'Freelance Projects',
                'description': 'Python development projects',
                'earning_potential': '$50-$150/hour',
                'flexibility': 'High',
                'discovery_method': 'skill_marketplace_analysis'
            })

        freelance.append({
            'platform': 'Toptal',
            'opportunity_type': 'High-end Consulting',
            'description': 'Elite freelance network',
            'earning_potential': '$100-$200/hour',
            'flexibility': 'Medium',
            'entry_barrier': 'Selective screening process',
            'discovery_method': 'premium_marketplace_analysis'
        })

        return freelance

    def _identify_entrepreneurial_paths(self, profile: Dict) -> List[Dict]:
        """Identify entrepreneurial opportunities"""
        entrepreneur = []

        skills = profile.get('skills', [])

        entrepreneur.append({
            'idea': 'Consulting in Your Domain',
            'description': f"Leverage {profile.get('years_experience', 5)}+ years experience",
            'startup_cost': 'Low ($500-$2000)',
            'earning_potential': '$75K-$150K annually',
            'risk_level': 'Medium',
            'time_to_revenue': '3-6 months',
            'discovery_method': 'experience_monetization_analysis'
        })

        if len(skills) > 3:
            entrepreneur.append({
                'idea': 'Online Course Creation',
                'description': 'Create courses teaching your skills',
                'startup_cost': 'Very Low ($100-$500)',
                'earning_potential': '$2K-$20K annually (passive)',
                'risk_level': 'Low',
                'time_to_revenue': '4-8 months',
                'discovery_method': 'skill_packaging_analysis'
            })

        return entrepreneur

    def _find_networking_opportunities(self, profile: Dict) -> List[Dict]:
        """Find networking events and opportunities"""
        industry = profile.get('current_industry', 'technology')

        networking = []

        networking.append({
            'event': f'{industry.title()} Professional Meetup',
            'type': 'Local Networking',
            'frequency': 'Monthly',
            'benefit': 'Build local industry connections',
            'discovery_method': 'event_scraping',
            'next_date': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        })

        networking.append({
            'event': f'{industry.title()} Virtual Conference',
            'type': 'Online Event',
            'frequency': 'Quarterly',
            'benefit': 'Learn trends, meet leaders',
            'discovery_method': 'online_event_discovery',
            'next_date': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        })

        return networking

    def _find_skill_monetization(self, profile: Dict) -> List[Dict]:
        """Find ways to monetize existing skills immediately"""
        monetization = []

        skills = profile.get('skills', [])

        for skill in skills[:3]:  # Top 3 skills
            monetization.append({
                'skill': skill,
                'method': 'Teaching/Tutoring',
                'platform': 'Wyzant, Tutor.com',
                'earning_potential': '$30-$60/hour',
                'time_investment': '5-10 hours/week',
                'discovery_method': 'skill_demand_matching'
            })

        return monetization

    def _discover_alternative_paths(self, profile: Dict) -> List[Dict]:
        """Discover alternative career paths using transferable skills"""
        current_role = profile.get('current_role', 'Professional')
        skills = profile.get('skills', [])

        alternatives = []

        # Find adjacent roles
        alternatives.append({
            'new_role': 'Technical Project Manager',
            'transfer_match': 85,
            'description': 'Use technical knowledge in leadership role',
            'transition_difficulty': 'Medium',
            'salary_change': '+15%',
            'discovery_method': 'transferable_skill_analysis',
            'rationale': 'Technical skills + communication = strong PM candidate'
        })

        alternatives.append({
            'new_role': 'Solutions Architect',
            'transfer_match': 78,
            'description': 'Design technical solutions for clients',
            'transition_difficulty': 'Medium',
            'salary_change': '+25%',
            'discovery_method': 'career_lattice_analysis',
            'rationale': 'Technical depth + business context = architect path'
        })

        return alternatives

    def _prioritize_opportunities(self, opportunities: List[Dict], profile: Dict) -> List[Dict]:
        """Prioritize opportunities by fit, effort, and reward"""
        def opportunity_score(opp):
            match_score = opp.get('match_score', opp.get('current_match', opp.get('transfer_match', 50)))
            opportunity_rating = opp.get('opportunity_score', 70)

            # Effort penalty
            effort = opp.get('effort_required', 'Medium')
            effort_scores = {'Low': 1.0, 'Medium': 0.8, 'High': 0.6}
            effort_multiplier = effort_scores.get(effort, 0.8)

            score = (match_score * 0.6 + opportunity_rating * 0.4) * effort_multiplier

            return score

        return sorted(opportunities, key=opportunity_score, reverse=True)

    def _generate_opportunity_recommendations(self, opportunities: List[Dict]) -> List[str]:
        """Generate recommendations based on discovered opportunities"""
        if not opportunities:
            return ["Keep building skills - opportunities will emerge"]

        recs = []

        top_opp = opportunities[0]
        recs.append(f"PRIORITY: Pursue {top_opp.get('title', 'top opportunity')} - highest match and opportunity score")

        hidden_market = [o for o in opportunities if o.get('category') == 'hidden_market']
        if hidden_market:
            recs.append(f"Tap into hidden job market - {len(hidden_market)} unadvertised opportunities found")

        emerging = [o for o in opportunities if o.get('category') == 'emerging_roles']
        if emerging:
            recs.append(f"Consider emerging roles with low competition: {emerging[0].get('title')}")

        return recs

    def _generate_action_items(self, top_opportunities: List[Dict]) -> List[str]:
        """Generate specific action items for top opportunities"""
        actions = []

        for opp in top_opportunities[:3]:
            if opp.get('access_method'):
                actions.append(f"{opp.get('title')}: {opp.get('access_method')}")
            elif opp.get('platform'):
                actions.append(f"Create profile on {opp.get('platform')} for {opp.get('opportunity_type')}")
            else:
                actions.append(f"Research and apply for {opp.get('title', 'opportunity')}")

        return actions

    def find_hidden_job_market(self, worker_profile: Dict, target_role: Dict) -> Dict:
        """
        Specifically focus on hidden job market opportunities
        """
        hidden_opps = self._discover_hidden_market(worker_profile)

        # Enhance with specific tactics
        tactics = [
            {
                'tactic': 'LinkedIn Warm Introductions',
                'description': 'Reach out to 2nd connections who work at target companies',
                'success_rate': 0.35,
                'effort': 'Medium',
                'timeline': '2-4 weeks'
            },
            {
                'tactic': 'Direct Hiring Manager Outreach',
                'description': 'Email hiring managers directly before jobs are posted',
                'success_rate': 0.15,
                'effort': 'High',
                'timeline': '1-3 months'
            },
            {
                'tactic': 'Company Career Pages',
                'description': 'Monitor target company career pages for early postings',
                'success_rate': 0.45,
                'effort': 'Low',
                'timeline': 'Ongoing'
            },
            {
                'tactic': 'Industry Events',
                'description': 'Attend conferences to meet hiring managers in person',
                'success_rate': 0.40,
                'effort': 'High',
                'timeline': 'Quarterly'
            }
        ]

        return {
            'hidden_opportunities': hidden_opps,
            'access_tactics': tactics,
            'estimated_hidden_market_size': 'up to 80% of jobs',
            'recommendations': [
                'Focus on networking - most hidden jobs filled through referrals',
                'Be proactive - don't wait for public postings',
                'Build relationships before you need them'
            ]
        }

    def get_recommendations(self, context: Dict) -> List[str]:
        """Get agent-specific recommendations"""
        return [
            "Explore hidden job market through networking",
            "Consider emerging roles with less competition",
            "Diversify opportunities across multiple channels"
        ]
