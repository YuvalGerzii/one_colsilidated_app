"""
Automation Fairness Engine
Policy-level tool to ensure automation doesn't worsen inequality
"""
from typing import Dict, List, Any, Optional
from datetime import datetime
import random


class AutomationFairnessEngine:
    """
    Ensures automation adoption doesn't worsen socioeconomic inequality
    Provides fairness scoring, impact modeling, and policy recommendations
    """

    def __init__(self):
        self.name = "Automation Fairness Engine"

    def calculate_fairness_score(
        self,
        automation_plan: Dict,
        affected_demographics: Dict
    ) -> Dict:
        """
        Score automation plan on fairness dimensions
        Returns overall fairness score (0-100)
        """
        # Analyze multiple fairness dimensions
        income_impact = self._assess_income_inequality_impact(automation_plan, affected_demographics)
        demographic_impact = self._assess_demographic_fairness(automation_plan, affected_demographics)
        geographic_impact = self._assess_geographic_fairness(automation_plan, affected_demographics)
        retraining_access = self._assess_retraining_accessibility(automation_plan, affected_demographics)
        transition_support = self._assess_transition_support(automation_plan)

        # Calculate weighted fairness score
        fairness_score = (
            income_impact['score'] * 0.3 +
            demographic_impact['score'] * 0.25 +
            geographic_impact['score'] * 0.2 +
            retraining_access['score'] * 0.15 +
            transition_support['score'] * 0.1
        )

        # Determine fairness grade
        if fairness_score >= 80:
            grade = 'A - Highly Fair'
            recommendation = 'Approve with commendation'
        elif fairness_score >= 65:
            grade = 'B - Fair'
            recommendation = 'Approve with minor improvements'
        elif fairness_score >= 50:
            grade = 'C - Needs Improvement'
            recommendation = 'Conditional approval pending improvements'
        else:
            grade = 'D - Unfair'
            recommendation = 'Require substantial fairness improvements'

        return {
            'overall_fairness_score': round(fairness_score, 1),
            'fairness_grade': grade,
            'recommendation': recommendation,
            'dimension_scores': {
                'income_inequality_impact': income_impact,
                'demographic_fairness': demographic_impact,
                'geographic_fairness': geographic_impact,
                'retraining_accessibility': retraining_access,
                'transition_support': transition_support
            },
            'required_improvements': self._generate_fairness_improvements(
                fairness_score,
                income_impact,
                demographic_impact,
                geographic_impact,
                retraining_access,
                transition_support
            ),
            'approval_conditions': self._generate_approval_conditions(fairness_score)
        }

    def model_aggregate_impact(
        self,
        automation_scenarios: List[Dict],
        geography: str,  # city, state, national
        population_data: Dict
    ) -> Dict:
        """
        Model aggregate impact of automation at city/state/national level
        """
        total_population = population_data.get('total_population', 0)
        workforce_size = population_data.get('workforce_size', 0)
        median_income = population_data.get('median_income', 50000)

        # Aggregate all scenarios
        total_jobs_impacted = sum(s.get('jobs_impacted', 0) for s in automation_scenarios)
        total_jobs_created = sum(s.get('jobs_created', 0) for s in automation_scenarios)
        net_job_change = total_jobs_created - total_jobs_impacted

        # Calculate impact rate
        impact_rate = (total_jobs_impacted / workforce_size) * 100 if workforce_size > 0 else 0

        # Project income changes
        avg_displaced_income = median_income * 0.8  # Displaced workers typically earn less
        avg_new_job_income = median_income * 1.2    # New jobs typically higher skill/pay
        income_redistribution = (total_jobs_created * avg_new_job_income) - (total_jobs_impacted * avg_displaced_income)

        # Calculate inequality metrics
        gini_coefficient = population_data.get('current_gini', 0.41)
        projected_gini = self._project_gini_coefficient(
            gini_coefficient,
            total_jobs_impacted,
            total_jobs_created,
            workforce_size
        )

        return {
            'geography': geography,
            'geography_type': self._classify_geography_type(geography),
            'population_metrics': {
                'total_population': total_population,
                'workforce_size': workforce_size,
                'median_income': median_income
            },
            'automation_impact': {
                'total_jobs_impacted': total_jobs_impacted,
                'total_jobs_created': total_jobs_created,
                'net_job_change': net_job_change,
                'impact_rate_percentage': round(impact_rate, 2),
                'severity': self._classify_impact_severity(impact_rate)
            },
            'economic_impact': {
                'income_redistribution': income_redistribution,
                'per_capita_impact': income_redistribution / total_population if total_population > 0 else 0,
                'current_gini_coefficient': gini_coefficient,
                'projected_gini_coefficient': projected_gini,
                'inequality_change': projected_gini - gini_coefficient
            },
            'demographic_breakdown': self._model_demographic_impact(automation_scenarios, population_data),
            'timeline_projection': self._project_impact_timeline(automation_scenarios),
            'policy_recommendations': self._generate_policy_recommendations(impact_rate, projected_gini)
        }

    def suggest_policies(
        self,
        impact_analysis: Dict,
        budget_available: float
    ) -> Dict:
        """
        Suggest specific policies based on impact analysis
        """
        impact_rate = impact_analysis.get('automation_impact', {}).get('impact_rate_percentage', 0)
        inequality_change = impact_analysis.get('economic_impact', {}).get('inequality_change', 0)

        policies = {
            'immediate_action': [],
            'short_term': [],
            'long_term': [],
            'budget_allocation': {}
        }

        # Retraining programs (always needed)
        if impact_rate > 0:
            retraining_budget = min(budget_available * 0.4, impact_analysis['automation_impact']['total_jobs_impacted'] * 15000)
            policies['immediate_action'].append({
                'policy': 'Universal Reskilling Program',
                'description': 'Free training for displaced workers',
                'budget': retraining_budget,
                'expected_impact': f"Retrain {int(retraining_budget / 15000)} workers",
                'timeframe': '6-12 months'
            })
            policies['budget_allocation']['retraining'] = retraining_budget

        # Job creation subsidies
        if impact_rate > 10:
            job_subsidy_budget = min(budget_available * 0.3, impact_analysis['automation_impact']['total_jobs_impacted'] * 10000)
            policies['short_term'].append({
                'policy': 'Job Creation Tax Credits',
                'description': '$10k tax credit per new job created',
                'budget': job_subsidy_budget,
                'expected_impact': f"Incentivize creation of {int(job_subsidy_budget / 10000)} jobs",
                'timeframe': '1-2 years'
            })
            policies['budget_allocation']['job_creation'] = job_subsidy_budget

        # UBI pilot if severe impact
        if impact_rate > 15:
            ubi_budget = min(budget_available * 0.25, 500000000)  # Cap at $500M
            policies['immediate_action'].append({
                'policy': 'Universal Basic Income Pilot',
                'description': '$1000/month for displaced workers during transition',
                'budget': ubi_budget,
                'expected_impact': f"Support {int(ubi_budget / 12000)} workers for 1 year",
                'timeframe': '1-2 years'
            })
            policies['budget_allocation']['ubi_pilot'] = ubi_budget

        # Automation tax if inequality worsening
        if inequality_change > 0.02:  # Gini increases by 0.02
            automation_tax_revenue = impact_analysis['automation_impact']['total_jobs_impacted'] * 5000
            policies['long_term'].append({
                'policy': 'Automation Impact Tax',
                'description': '$5k annual tax per job automated',
                'budget': -automation_tax_revenue,  # Negative = revenue generation
                'expected_impact': f"Generate ${automation_tax_revenue:,} for worker transition fund",
                'timeframe': 'Ongoing'
            })
            policies['budget_allocation']['automation_tax'] = -automation_tax_revenue

        # Education investment
        education_budget = min(budget_available * 0.15, 200000000)
        policies['long_term'].append({
            'policy': 'Future Skills Education Initiative',
            'description': 'K-12 and community college AI/automation curriculum',
            'budget': education_budget,
            'expected_impact': 'Prepare next generation for AI economy',
            'timeframe': '5-10 years'
        })
        policies['budget_allocation']['education'] = education_budget

        # Calculate total cost
        total_cost = sum(p['budget'] for p in policies['immediate_action'] + policies['short_term'] + policies['long_term'])
        total_revenue = abs(sum(p['budget'] for p in policies['long_term'] if p['budget'] < 0))

        policies['financial_summary'] = {
            'total_program_cost': total_cost,
            'total_revenue_generated': total_revenue,
            'net_budget_required': total_cost - total_revenue,
            'budget_available': budget_available,
            'budget_utilization_percent': (abs(total_cost) / budget_available) * 100 if budget_available > 0 else 0
        }

        policies['implementation_priority'] = self._prioritize_policies(
            policies['immediate_action'] + policies['short_term'] + policies['long_term'],
            impact_rate,
            budget_available
        )

        return policies

    def simulate_ubi_scenario(
        self,
        ubi_amount_monthly: float,
        coverage_percentage: float,
        population: int,
        duration_months: int
    ) -> Dict:
        """
        Simulate Universal Basic Income scenario
        """
        eligible_population = int(population * (coverage_percentage / 100))
        monthly_cost = eligible_population * ubi_amount_monthly
        total_cost = monthly_cost * duration_months

        # Estimate economic multiplier effect
        multiplier = 1.6  # $1 of UBI generates $1.60 in economic activity
        economic_stimulus = total_cost * multiplier

        # Estimate poverty reduction
        poverty_line = 12880  # Annual US poverty line (2020)
        people_lifted_above_poverty = int(eligible_population * 0.3)  # 30% lifted above poverty

        # Calculate funding sources
        funding_sources = {
            'automation_tax': total_cost * 0.4,
            'progressive_income_tax': total_cost * 0.3,
            'vat_on_luxury_goods': total_cost * 0.2,
            'budget_reallocation': total_cost * 0.1
        }

        simulation = {
            'parameters': {
                'ubi_amount_monthly': ubi_amount_monthly,
                'coverage_percentage': coverage_percentage,
                'eligible_population': eligible_population,
                'duration_months': duration_months
            },
            'costs': {
                'monthly_cost': monthly_cost,
                'total_cost': total_cost,
                'per_capita_cost': total_cost / population
            },
            'economic_effects': {
                'direct_spending': total_cost,
                'multiplier_effect': multiplier,
                'total_economic_stimulus': economic_stimulus,
                'gdp_impact_percent': (economic_stimulus / (population * 55000)) * 100  # Assume $55k GDP per capita
            },
            'social_effects': {
                'people_lifted_above_poverty': people_lifted_above_poverty,
                'poverty_reduction_percent': (people_lifted_above_poverty / eligible_population) * 100,
                'estimated_health_improvement': 'Moderate',
                'estimated_education_improvement': 'Moderate',
                'estimated_crime_reduction': 'Low to Moderate'
            },
            'funding_sources': funding_sources,
            'feasibility': {
                'political_feasibility': 'Low' if coverage_percentage > 50 else 'Medium',
                'economic_feasibility': 'Medium' if total_cost < population * 5000 else 'Low',
                'implementation_complexity': 'High',
                'timeframe_to_implement': '2-3 years'
            },
            'recommendations': [
                'Start with pilot program in 2-3 cities',
                f"Consider phased rollout over {max(duration_months // 6, 1)} phases",
                'Implement strong evaluation metrics',
                'Combine with job training programs for maximum effect'
            ]
        }

        return simulation

    def calculate_inequality_index(
        self,
        current_data: Dict,
        automation_adoption_rate: float
    ) -> Dict:
        """
        Calculate real-time inequality index influenced by automation
        """
        # Current metrics
        current_gini = current_data.get('gini_coefficient', 0.41)
        current_unemployment = current_data.get('unemployment_rate', 5.0)
        median_income = current_data.get('median_income', 50000)

        # Calculate automation impact on inequality
        automation_inequality_factor = automation_adoption_rate * 0.02  # 2% increase in Gini per 100% automation
        projected_gini = min(current_gini + automation_inequality_factor, 1.0)

        # Calculate composite inequality index (0-100, higher = more inequality)
        inequality_index = (
            (projected_gini * 100) * 0.4 +  # 40% weight
            (current_unemployment * 5) * 0.3 +  # 30% weight
            ((100000 - median_income) / 1000) * 0.3  # 30% weight
        )

        # Historical comparison
        historical_trend = 'worsening' if projected_gini > current_gini else 'improving'

        # Breakdown by demographic
        demographic_breakdown = {
            'high_income_top_10_percent': {
                'share_of_wealth': 70 + (automation_adoption_rate * 0.1),
                'automation_benefit': 'high'
            },
            'middle_income_40_60_percentile': {
                'share_of_wealth': 20 - (automation_adoption_rate * 0.05),
                'automation_impact': 'mixed'
            },
            'low_income_bottom_40_percent': {
                'share_of_wealth': 10 - (automation_adoption_rate * 0.05),
                'automation_impact': 'negative'
            }
        }

        return {
            'inequality_index': round(inequality_index, 1),
            'gini_coefficient': {
                'current': current_gini,
                'projected': round(projected_gini, 3),
                'change': round(projected_gini - current_gini, 3),
                'trend': historical_trend
            },
            'income_distribution': demographic_breakdown,
            'severity_rating': self._rate_inequality_severity(inequality_index),
            'contributing_factors': {
                'automation_adoption': f"{automation_adoption_rate:.1f}%",
                'unemployment': f"{current_unemployment:.1f}%",
                'median_income': f"${median_income:,}"
            },
            'recommendations': self._generate_inequality_recommendations(inequality_index, projected_gini),
            'comparison': {
                'vs_national_average': 'above' if inequality_index > 45 else 'below',
                'vs_oecd_average': 'above' if projected_gini > 0.35 else 'below'
            }
        }

    def _assess_income_inequality_impact(self, plan: Dict, demographics: Dict) -> Dict:
        """Assess impact on income inequality"""
        jobs_impacted = plan.get('jobs_impacted', 0)
        avg_impacted_income = demographics.get('avg_impacted_income', 40000)
        new_jobs_income = demographics.get('avg_new_job_income', 60000)

        # Lower income workers typically more impacted
        low_income_impact_rate = demographics.get('low_income_impact_percent', 60)

        # Score (100 = no negative impact, 0 = severe negative impact)
        if low_income_impact_rate < 30:
            score = 90
        elif low_income_impact_rate < 50:
            score = 70
        elif low_income_impact_rate < 70:
            score = 50
        else:
            score = 30

        return {
            'score': score,
            'details': f"{low_income_impact_rate}% of displaced workers are low-income",
            'concern_level': 'low' if score > 70 else 'high'
        }

    def _assess_demographic_fairness(self, plan: Dict, demographics: Dict) -> Dict:
        """Assess fairness across demographic groups"""
        # Check if any group disproportionately impacted
        groups = demographics.get('groups', {})
        disparities = []

        for group, data in groups.items():
            impact_rate = data.get('impact_rate', 0)
            population_percentage = data.get('population_percent', 0)
            disparity = impact_rate - population_percentage

            if disparity > 15:  # >15% overrepresentation
                disparities.append((group, disparity))

        if not disparities:
            score = 95
        elif len(disparities) == 1:
            score = 70
        else:
            score = 40

        return {
            'score': score,
            'details': f"{len(disparities)} groups disproportionately impacted" if disparities else "Impacts distributed fairly",
            'disparities': disparities
        }

    def _assess_geographic_fairness(self, plan: Dict, demographics: Dict) -> Dict:
        """Assess geographic distribution of impacts"""
        regions = demographics.get('regions', {})

        if not regions:
            return {'score': 75, 'details': 'Limited geographic data'}

        # Check if impacts concentrated in specific regions
        max_impact = max(r.get('impact_rate', 0) for r in regions.values())
        min_impact = min(r.get('impact_rate', 0) for r in regions.values())
        concentration = max_impact - min_impact

        if concentration < 10:
            score = 90
        elif concentration < 25:
            score = 70
        else:
            score = 45

        return {
            'score': score,
            'details': f"Impact concentration variance: {concentration:.1f}%",
            'high_impact_regions': [r for r, data in regions.items() if data.get('impact_rate', 0) > 15]
        }

    def _assess_retraining_accessibility(self, plan: Dict, demographics: Dict) -> Dict:
        """Assess accessibility of retraining programs"""
        retraining_budget = plan.get('retraining_budget', 0)
        jobs_impacted = plan.get('jobs_impacted', 1)
        budget_per_worker = retraining_budget / jobs_impacted if jobs_impacted > 0 else 0

        if budget_per_worker > 12000:
            score = 95
        elif budget_per_worker > 8000:
            score = 75
        elif budget_per_worker > 4000:
            score = 55
        else:
            score = 30

        return {
            'score': score,
            'details': f"${budget_per_worker:,.0f} per impacted worker",
            'adequacy': 'strong' if score > 75 else 'insufficient'
        }

    def _assess_transition_support(self, plan: Dict) -> Dict:
        """Assess support during transition period"""
        has_income_support = plan.get('income_support', False)
        has_job_placement = plan.get('job_placement_service', False)
        transition_duration = plan.get('transition_support_months', 0)

        score = 50  # Base score
        if has_income_support:
            score += 20
        if has_job_placement:
            score += 15
        score += min(transition_duration * 2, 15)  # Up to 15 points for duration

        return {
            'score': min(score, 100),
            'details': f"{transition_duration} months support, income_support={has_income_support}",
            'components': {
                'income_support': has_income_support,
                'job_placement': has_job_placement,
                'duration_months': transition_duration
            }
        }

    def _generate_fairness_improvements(self, overall_score, *dimension_scores) -> List[Dict]:
        """Generate required improvements based on scores"""
        improvements = []

        if overall_score < 65:
            improvements.append({
                'priority': 'critical',
                'improvement': 'Increase retraining budget to $12k+ per worker',
                'expected_impact': '+15 fairness points'
            })

        for i, dim in enumerate(dimension_scores):
            if dim['score'] < 60:
                improvements.append({
                    'priority': 'high',
                    'improvement': f"Address low score in: {list(dim.keys())[0]}",
                    'expected_impact': '+10 fairness points'
                })

        return improvements

    def _generate_approval_conditions(self, fairness_score: float) -> List[str]:
        """Generate approval conditions"""
        if fairness_score >= 80:
            return ['Approved - no conditions']

        conditions = []
        if fairness_score < 65:
            conditions.append('Increase retraining investment by 50%')
        if fairness_score < 60:
            conditions.append('Implement transition income support program')
        if fairness_score < 55:
            conditions.append('Create job placement guarantee for retrained workers')

        return conditions

    def _classify_geography_type(self, geography: str) -> str:
        """Classify geography level"""
        if any(word in geography.lower() for word in ['city', 'town', 'county']):
            return 'local'
        elif any(word in geography.lower() for word in ['state', 'province']):
            return 'regional'
        else:
            return 'national'

    def _classify_impact_severity(self, impact_rate: float) -> str:
        """Classify severity of automation impact"""
        if impact_rate > 20:
            return 'severe'
        elif impact_rate > 10:
            return 'significant'
        elif impact_rate > 5:
            return 'moderate'
        else:
            return 'low'

    def _project_gini_coefficient(self, current_gini, jobs_lost, jobs_created, workforce_size) -> float:
        """Project future Gini coefficient"""
        net_job_loss = jobs_lost - jobs_created
        workforce_impact = (net_job_loss / workforce_size) if workforce_size > 0 else 0

        # Automation tends to increase inequality
        gini_change = workforce_impact * 0.05  # 5% increase in Gini per 100% workforce turnover

        return min(current_gini + gini_change, 1.0)

    def _model_demographic_impact(self, scenarios, population_data) -> Dict:
        """Model impact across demographic groups"""
        return {
            'by_age': {
                '18-35': {'impact_rate': 12, 'resilience': 'high'},
                '36-55': {'impact_rate': 18, 'resilience': 'medium'},
                '56+': {'impact_rate': 25, 'resilience': 'low'}
            },
            'by_education': {
                'high_school': {'impact_rate': 22, 'resilience': 'low'},
                'bachelors': {'impact_rate': 12, 'resilience': 'medium'},
                'advanced': {'impact_rate': 5, 'resilience': 'high'}
            }
        }

    def _project_impact_timeline(self, scenarios) -> Dict:
        """Project when impacts will materialize"""
        return {
            'immediate_6_months': '15% of impacts',
            '6_12_months': '35% of impacts',
            '1_2_years': '30% of impacts',
            '2_5_years': '20% of impacts'
        }

    def _generate_policy_recommendations(self, impact_rate, projected_gini) -> List[str]:
        """Generate policy recommendations"""
        recs = []

        if impact_rate > 15:
            recs.append('Implement emergency worker transition fund')
        if impact_rate > 10:
            recs.append('Create job creation tax incentives')
        if projected_gini > 0.45:
            recs.append('Consider automation impact tax')
        if impact_rate > 5:
            recs.append('Expand retraining programs')

        recs.append('Monitor inequality metrics monthly')

        return recs

    def _rate_inequality_severity(self, index: float) -> str:
        """Rate severity of inequality"""
        if index > 60:
            return 'Critical'
        elif index > 50:
            return 'High'
        elif index > 40:
            return 'Moderate'
        else:
            return 'Low'

    def _generate_inequality_recommendations(self, index, gini) -> List[str]:
        """Generate recommendations to reduce inequality"""
        recs = []

        if index > 55:
            recs.append('Urgent: Implement progressive automation tax')
        if gini > 0.45:
            recs.append('Strengthen social safety net programs')
        if index > 45:
            recs.append('Expand access to education and reskilling')

        recs.append('Monitor wealth concentration in top 10%')

        return recs

    def _prioritize_policies(self, policies, impact_rate, budget) -> List[Dict]:
        """Prioritize policies by impact and cost-effectiveness"""
        scored_policies = []

        for policy in policies:
            cost_effectiveness = abs(policy['budget']) / 1000000 if policy['budget'] != 0 else 999  # Lower is better
            urgency = 10 if 'immediate' in policy.get('timeframe', '') else 5

            priority_score = urgency / (cost_effectiveness + 0.1)

            scored_policies.append({
                **policy,
                'priority_score': priority_score,
                'implementation_order': 0
            })

        # Sort by priority score
        scored_policies.sort(key=lambda x: x['priority_score'], reverse=True)

        # Assign implementation order
        for i, policy in enumerate(scored_policies):
            policy['implementation_order'] = i + 1

        return scored_policies[:5]  # Top 5 priorities
