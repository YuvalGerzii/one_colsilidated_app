"""
Corporate Workforce Transformation OS
Internal tools for companies to reduce layoffs and increase productivity
"""
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import random


class WorkforceTransformationEngine:
    """
    Corporate-level workforce transformation and redeployment system
    Helps companies reduce layoffs by internal job matching and automation planning
    """

    def __init__(self):
        self.name = "Workforce Transformation Engine"

    def analyze_internal_redeployment(
        self,
        company_data: Dict,
        at_risk_employees: List[Dict],
        open_positions: List[Dict]
    ) -> Dict:
        """
        Match at-risk employees to open internal positions
        Reduces layoffs by finding internal opportunities
        """
        matches = []
        redeployment_plan = {
            'total_at_risk': len(at_risk_employees),
            'positions_available': len(open_positions),
            'matches_found': 0,
            'potential_saves': 0,
            'reskilling_needed': [],
            'immediate_fits': [],
            'strategic_moves': []
        }

        for employee in at_risk_employees:
            emp_skills = set(employee.get('skills', []))
            best_match = None
            best_score = 0

            for position in open_positions:
                pos_required = set(position.get('required_skills', []))
                pos_preferred = set(position.get('preferred_skills', []))

                # Calculate match score
                required_match = len(emp_skills & pos_required) / len(pos_required) if pos_required else 0
                preferred_match = len(emp_skills & pos_preferred) / len(pos_preferred) if pos_preferred else 0
                overall_score = (required_match * 0.7) + (preferred_match * 0.3)

                if overall_score > best_score:
                    best_score = overall_score
                    best_match = position

            if best_match and best_score > 0.4:  # 40% threshold
                skill_gap = set(best_match.get('required_skills', [])) - emp_skills
                reskilling_time = len(skill_gap) * 4  # 4 weeks per skill

                match_data = {
                    'employee_id': employee.get('id'),
                    'employee_name': employee.get('name'),
                    'current_role': employee.get('current_role'),
                    'target_position': best_match.get('title'),
                    'target_department': best_match.get('department'),
                    'match_score': round(best_score * 100, 1),
                    'skill_gap': list(skill_gap),
                    'reskilling_weeks': reskilling_time,
                    'estimated_cost': reskilling_time * 1000,  # $1k per week
                    'match_type': 'immediate' if best_score > 0.8 else 'reskilling_needed'
                }

                matches.append(match_data)
                redeployment_plan['matches_found'] += 1
                redeployment_plan['potential_saves'] += 1

                if best_score > 0.8:
                    redeployment_plan['immediate_fits'].append(match_data)
                else:
                    redeployment_plan['reskilling_needed'].append(match_data)

        # Calculate ROI
        avg_layoff_cost = 50000  # severance, unemployment, rehiring
        avg_reskilling_cost = sum(m['estimated_cost'] for m in matches) / len(matches) if matches else 0
        total_savings = (len(matches) * avg_layoff_cost) - (len(matches) * avg_reskilling_cost)

        redeployment_plan['financial_impact'] = {
            'total_layoff_costs_avoided': len(matches) * avg_layoff_cost,
            'total_reskilling_investment': len(matches) * avg_reskilling_cost,
            'net_savings': total_savings,
            'roi_percentage': (total_savings / (len(matches) * avg_reskilling_cost)) * 100 if matches else 0
        }

        redeployment_plan['matches'] = matches
        redeployment_plan['recommendations'] = self._generate_redeployment_recommendations(redeployment_plan)

        return redeployment_plan

    def identify_redundant_workflows(
        self,
        department_data: List[Dict]
    ) -> Dict:
        """
        Identify redundant and automatable workflows
        Suggests automation solutions
        """
        redundancies = {
            'total_departments_analyzed': len(department_data),
            'redundant_workflows': [],
            'automation_opportunities': [],
            'estimated_time_savings_hours_per_week': 0,
            'estimated_cost_savings_annually': 0
        }

        automation_db = {
            'data_entry': {
                'automation_solution': 'RPA with OCR',
                'time_savings_percent': 85,
                'implementation_cost': 25000,
                'annual_savings': 120000
            },
            'report_generation': {
                'automation_solution': 'Automated BI dashboards',
                'time_savings_percent': 70,
                'implementation_cost': 35000,
                'annual_savings': 95000
            },
            'email_processing': {
                'automation_solution': 'AI email classifier and responder',
                'time_savings_percent': 60,
                'implementation_cost': 20000,
                'annual_savings': 75000
            },
            'scheduling': {
                'automation_solution': 'AI scheduling assistant',
                'time_savings_percent': 90,
                'implementation_cost': 15000,
                'annual_savings': 60000
            },
            'invoice_processing': {
                'automation_solution': 'Automated invoice matching',
                'time_savings_percent': 95,
                'implementation_cost': 30000,
                'annual_savings': 110000
            }
        }

        for dept in department_data:
            workflows = dept.get('workflows', [])
            for workflow in workflows:
                workflow_type = workflow.get('type', '').lower()

                # Check if automatable
                if workflow_type in automation_db:
                    auto_solution = automation_db[workflow_type]
                    hours_per_week = workflow.get('hours_per_week', 0)
                    time_saved = hours_per_week * (auto_solution['time_savings_percent'] / 100)

                    opportunity = {
                        'department': dept.get('name'),
                        'workflow': workflow.get('name'),
                        'workflow_type': workflow_type,
                        'current_hours_per_week': hours_per_week,
                        'automation_solution': auto_solution['automation_solution'],
                        'time_savings_percent': auto_solution['time_savings_percent'],
                        'hours_saved_per_week': time_saved,
                        'implementation_cost': auto_solution['implementation_cost'],
                        'annual_savings': auto_solution['annual_savings'],
                        'payback_months': round(auto_solution['implementation_cost'] / (auto_solution['annual_savings'] / 12), 1),
                        'priority': 'high' if auto_solution['payback_months'] < 6 else 'medium'
                    }

                    redundancies['automation_opportunities'].append(opportunity)
                    redundancies['estimated_time_savings_hours_per_week'] += time_saved
                    redundancies['estimated_cost_savings_annually'] += auto_solution['annual_savings']

        # Sort by ROI
        redundancies['automation_opportunities'].sort(
            key=lambda x: x['annual_savings'] / x['implementation_cost'],
            reverse=True
        )

        redundancies['recommendations'] = [
            f"Prioritize {len([o for o in redundancies['automation_opportunities'] if o['priority'] == 'high'])} high-priority automations",
            f"Expected annual savings: ${redundancies['estimated_cost_savings_annually']:,}",
            f"Free up {redundancies['estimated_time_savings_hours_per_week']:.0f} hours/week for strategic work",
            "Implement automations in 3-month sprints to manage change"
        ]

        return redundancies

    def generate_department_productivity_analytics(
        self,
        department_data: Dict
    ) -> Dict:
        """
        Analyze department productivity: manual vs automated hours
        """
        dept_name = department_data.get('name')
        total_employees = department_data.get('employee_count', 0)
        total_hours_per_week = total_employees * 40

        # Simulate current breakdown
        manual_hours = department_data.get('manual_hours_per_week', total_hours_per_week * 0.7)
        automated_hours = department_data.get('automated_hours_per_week', total_hours_per_week * 0.3)

        # Calculate metrics
        automation_rate = (automated_hours / total_hours_per_week) * 100
        productivity_score = min((automation_rate * 0.4) + 60, 100)  # Score 60-100

        # Project improvements
        potential_automation = manual_hours * 0.5  # 50% of manual work is automatable
        projected_productivity = ((automated_hours + potential_automation) / total_hours_per_week) * 100

        analytics = {
            'department': dept_name,
            'current_state': {
                'total_employees': total_employees,
                'total_hours_per_week': total_hours_per_week,
                'manual_hours': manual_hours,
                'automated_hours': automated_hours,
                'automation_rate': round(automation_rate, 1),
                'productivity_score': round(productivity_score, 1)
            },
            'potential_state': {
                'additional_automation_hours': potential_automation,
                'projected_automation_rate': round(projected_productivity, 1),
                'projected_productivity_score': min(round(projected_productivity * 0.4 + 60, 1), 100),
                'hours_freed_for_strategic_work': potential_automation
            },
            'improvement_opportunities': [
                {
                    'opportunity': 'Automate repetitive data tasks',
                    'impact': 'Free 20h/week',
                    'difficulty': 'low'
                },
                {
                    'opportunity': 'Implement AI-assisted reporting',
                    'impact': 'Free 15h/week',
                    'difficulty': 'medium'
                },
                {
                    'opportunity': 'Deploy workflow automation',
                    'impact': 'Free 10h/week',
                    'difficulty': 'medium'
                }
            ],
            'recommendations': [
                f"Current automation rate: {automation_rate:.0f}% - Industry avg: 45%",
                f"Potential to free {potential_automation:.0f}h/week for strategic work",
                f"Focus on low-difficulty, high-impact opportunities first",
                "Track weekly automation metrics"
            ]
        }

        return analytics

    def calculate_employee_risk_scores(
        self,
        employees: List[Dict],
        company_automation_plan: Dict
    ) -> Dict:
        """
        Calculate risk scores for each employee based on automation plans
        """
        risk_analysis = {
            'total_employees': len(employees),
            'high_risk_count': 0,
            'medium_risk_count': 0,
            'low_risk_count': 0,
            'employee_risks': []
        }

        for employee in employees:
            role = employee.get('role', '')
            skills = employee.get('skills', [])
            tenure = employee.get('tenure_years', 0)

            # Calculate base automation risk
            role_automation_risk = self._get_role_automation_risk(role)

            # Adjust for skills
            ai_skills = len([s for s in skills if 'ai' in s.lower() or 'ml' in s.lower() or 'data' in s.lower()])
            skill_protection = min(ai_skills * 10, 30)  # Up to 30% protection

            # Adjust for tenure
            tenure_protection = min(tenure * 2, 20)  # Up to 20% protection

            # Final risk score
            risk_score = max(role_automation_risk - skill_protection - tenure_protection, 0)

            # Categorize
            if risk_score > 70:
                risk_category = 'high'
                risk_analysis['high_risk_count'] += 1
            elif risk_score > 40:
                risk_category = 'medium'
                risk_analysis['medium_risk_count'] += 1
            else:
                risk_category = 'low'
                risk_analysis['low_risk_count'] += 1

            # Reskilling recommendations
            reskilling_path = self._generate_reskilling_path(role, skills, risk_score)

            risk_data = {
                'employee_id': employee.get('id'),
                'name': employee.get('name'),
                'role': role,
                'risk_score': round(risk_score, 1),
                'risk_category': risk_category,
                'automation_risk': role_automation_risk,
                'protective_factors': {
                    'ai_skills': skill_protection,
                    'tenure': tenure_protection
                },
                'reskilling_path': reskilling_path,
                'recommended_actions': self._get_risk_mitigation_actions(risk_category, reskilling_path)
            }

            risk_analysis['employee_risks'].append(risk_data)

        # Sort by risk score
        risk_analysis['employee_risks'].sort(key=lambda x: x['risk_score'], reverse=True)

        risk_analysis['summary'] = {
            'high_risk_percentage': round((risk_analysis['high_risk_count'] / len(employees)) * 100, 1),
            'immediate_action_needed': risk_analysis['high_risk_count'],
            'total_reskilling_budget_needed': risk_analysis['high_risk_count'] * 15000 + risk_analysis['medium_risk_count'] * 8000
        }

        return risk_analysis

    def simulate_union_negotiation(
        self,
        automation_plan: Dict,
        current_workforce: Dict
    ) -> Dict:
        """
        Simulate union reactions to automation plans
        Model cost trade-offs and productivity gains
        """
        total_employees = current_workforce.get('total_count', 0)
        jobs_automated = automation_plan.get('jobs_impacted', 0)
        automation_cost = automation_plan.get('implementation_cost', 0)

        # Simulate union concerns
        job_loss_rate = (jobs_automated / total_employees) * 100

        if job_loss_rate > 20:
            union_stance = 'strong_opposition'
            strike_probability = 75
        elif job_loss_rate > 10:
            union_stance = 'moderate_opposition'
            strike_probability = 35
        else:
            union_stance = 'negotiable'
            strike_probability = 10

        # Calculate negotiation scenarios
        scenarios = {
            'aggressive_automation': {
                'jobs_eliminated': jobs_automated,
                'reskilling_investment': automation_cost * 0.1,
                'union_satisfaction': 20,
                'strike_risk': strike_probability,
                'productivity_gain': 40,
                'timeline_months': 12,
                'net_cost': automation_cost - (jobs_automated * 60000)  # Savings from reduced headcount
            },
            'balanced_approach': {
                'jobs_eliminated': int(jobs_automated * 0.5),
                'reskilling_investment': automation_cost * 0.3,
                'union_satisfaction': 65,
                'strike_risk': strike_probability * 0.3,
                'productivity_gain': 30,
                'timeline_months': 18,
                'net_cost': automation_cost + (jobs_automated * 0.5 * 15000)  # Reskilling cost
            },
            'union_friendly': {
                'jobs_eliminated': 0,
                'reskilling_investment': automation_cost * 0.5,
                'union_satisfaction': 90,
                'strike_risk': 5,
                'productivity_gain': 25,
                'timeline_months': 24,
                'net_cost': automation_cost + (jobs_automated * 20000)  # Full reskilling
            }
        }

        negotiation = {
            'current_situation': {
                'total_workforce': total_employees,
                'jobs_at_risk': jobs_automated,
                'union_stance': union_stance,
                'strike_probability': strike_probability
            },
            'scenarios': scenarios,
            'recommended_approach': 'balanced_approach',
            'negotiation_tactics': [
                'Emphasize reskilling commitment and career growth opportunities',
                'Offer job guarantees for retrained employees',
                'Phase automation gradually over 18-24 months',
                'Create joint labor-management automation committee',
                'Guarantee productivity bonuses shared with workforce'
            ],
            'predicted_outcome': {
                'likely_agreement': True if union_stance != 'strong_opposition' else False,
                'estimated_timeline_to_agreement': '3-6 months',
                'key_demands_expected': [
                    'No involuntary layoffs',
                    'Paid reskilling programs',
                    'Productivity gain sharing',
                    'Consultation on future automation'
                ]
            }
        }

        return negotiation

    def _generate_redeployment_recommendations(self, plan: Dict) -> List[str]:
        """Generate actionable recommendations for redeployment"""
        recs = []

        match_rate = (plan['matches_found'] / plan['total_at_risk']) * 100 if plan['total_at_risk'] > 0 else 0

        if match_rate > 70:
            recs.append(f"Excellent: {match_rate:.0f}% of at-risk employees can be redeployed internally")
        elif match_rate > 40:
            recs.append(f"Good progress: {match_rate:.0f}% redeployable - expand open positions to improve")
        else:
            recs.append(f"Low match rate: {match_rate:.0f}% - consider creating bridge roles or upskilling programs")

        if plan['immediate_fits']:
            recs.append(f"Fast-track {len(plan['immediate_fits'])} high-match employees (>80% fit) immediately")

        if plan['reskilling_needed']:
            recs.append(f"Invest in reskilling {len(plan['reskilling_needed'])} employees - ROI: {plan['financial_impact']['roi_percentage']:.0f}%")

        recs.append(f"Net savings: ${plan['financial_impact']['net_savings']:,.0f} vs traditional layoffs")

        return recs

    def _get_role_automation_risk(self, role: str) -> float:
        """Get base automation risk for a role"""
        risk_db = {
            'data_entry': 95,
            'cashier': 90,
            'telemarketer': 85,
            'assembly_line': 80,
            'customer_service': 70,
            'bookkeeper': 75,
            'admin_assistant': 65,
            'analyst': 50,
            'project_manager': 30,
            'software_engineer': 25,
            'designer': 20,
            'manager': 15,
            'strategist': 10
        }

        role_lower = role.lower()
        for key in risk_db:
            if key in role_lower:
                return risk_db[key]

        return 50  # Default medium risk

    def _generate_reskilling_path(self, role: str, current_skills: List[str], risk_score: float) -> Dict:
        """Generate reskilling path for at-risk employee"""
        if risk_score > 70:
            urgency = 'critical'
            timeline = '3-6 months'
            investment = 15000
        elif risk_score > 40:
            urgency = 'high'
            timeline = '6-12 months'
            investment = 8000
        else:
            urgency = 'moderate'
            timeline = '12-18 months'
            investment = 5000

        # Suggest future-proof skills
        recommended_skills = ['data_analysis', 'ai_tools', 'automation_management', 'digital_literacy']
        skill_gap = [s for s in recommended_skills if s not in current_skills]

        return {
            'urgency': urgency,
            'timeline': timeline,
            'investment_needed': investment,
            'recommended_skills': skill_gap,
            'suggested_programs': [
                'Internal AI tools training',
                'Data analytics bootcamp',
                'Automation management certification'
            ]
        }

    def _get_risk_mitigation_actions(self, risk_category: str, reskilling_path: Dict) -> List[str]:
        """Get specific mitigation actions based on risk level"""
        if risk_category == 'high':
            return [
                'Immediate enrollment in reskilling program',
                'Weekly 1-on-1 with career coach',
                'Shadow employees in target roles',
                'Begin internal job matching process'
            ]
        elif risk_category == 'medium':
            return [
                'Enroll in upskilling program within 30 days',
                'Monthly career development check-ins',
                'Explore internal opportunities',
                'Build portfolio of AI-augmented work'
            ]
        else:
            return [
                'Continue current development plan',
                'Stay updated on automation trends',
                'Quarterly skill assessments',
                'Maintain high performance'
            ]
