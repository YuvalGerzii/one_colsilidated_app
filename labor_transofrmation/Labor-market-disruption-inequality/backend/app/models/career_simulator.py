"""
Career Simulation Engine
Simulates career trajectories with income, burnout, and growth projections
"""
import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class CareerSimulation:
    """Results of career path simulation"""
    career_path: str
    time_horizon_years: int
    income_projection: List[Dict]
    burnout_curve: List[Dict]
    growth_trajectory: List[Dict]
    skill_evolution: List[Dict]
    market_value_projection: List[Dict]
    life_satisfaction: List[Dict]
    summary_metrics: Dict

class CareerSimulator:
    """
    Simulate different career paths with comprehensive projections
    Models income, burnout, growth, and market value over time
    """

    def __init__(self):
        self.career_profiles = self._load_career_profiles()
        self.market_dynamics = self._initialize_market_dynamics()

    def _load_career_profiles(self) -> Dict:
        """Load career profiles with characteristics"""
        return {
            'data_technician': {
                'entry_salary': 55000,
                'salary_growth_rate': 0.06,
                'salary_ceiling': 95000,
                'burnout_baseline': 40,
                'burnout_growth_rate': 0.03,
                'growth_potential': 70,
                'automation_risk': 55,
                'work_life_balance': 65,
                'skill_development_rate': 0.08
            },
            'software_engineer': {
                'entry_salary': 85000,
                'salary_growth_rate': 0.08,
                'salary_ceiling': 180000,
                'burnout_baseline': 55,
                'burnout_growth_rate': 0.04,
                'growth_potential': 85,
                'automation_risk': 30,
                'work_life_balance': 50,
                'skill_development_rate': 0.10
            },
            'data_scientist': {
                'entry_salary': 95000,
                'salary_growth_rate': 0.09,
                'salary_ceiling': 200000,
                'burnout_baseline': 60,
                'burnout_growth_rate': 0.05,
                'growth_potential': 90,
                'automation_risk': 25,
                'work_life_balance': 45,
                'skill_development_rate': 0.12
            },
            'project_manager': {
                'entry_salary': 75000,
                'salary_growth_rate': 0.05,
                'salary_ceiling': 140000,
                'burnout_baseline': 70,
                'burnout_growth_rate': 0.06,
                'growth_potential': 65,
                'automation_risk': 40,
                'work_life_balance': 40,
                'skill_development_rate': 0.05
            },
            'devops_engineer': {
                'entry_salary': 90000,
                'salary_growth_rate': 0.10,
                'salary_ceiling': 175000,
                'burnout_baseline': 65,
                'burnout_growth_rate': 0.05,
                'growth_potential': 80,
                'automation_risk': 35,
                'work_life_balance': 48,
                'skill_development_rate': 0.11
            },
            'ux_designer': {
                'entry_salary': 70000,
                'salary_growth_rate': 0.07,
                'salary_ceiling': 130000,
                'burnout_baseline': 45,
                'burnout_growth_rate': 0.03,
                'growth_potential': 75,
                'automation_risk': 50,
                'work_life_balance': 70,
                'skill_development_rate': 0.09
            }
        }

    def _initialize_market_dynamics(self) -> Dict:
        """Initialize market dynamics factors"""
        return {
            'inflation_rate': 0.03,
            'automation_acceleration': 0.05,  # Annual increase in automation
            'demand_volatility': 0.1,
            'skill_obsolescence_rate': 0.08
        }

    def simulate_career_path(
        self,
        career_path: str,
        worker_profile: Dict,
        time_horizon_years: int = 10
    ) -> CareerSimulation:
        """
        Simulate a career path over time

        Args:
            career_path: Career to simulate
            worker_profile: Worker's current state
            time_horizon_years: Years to simulate

        Returns:
            Complete career simulation
        """
        if career_path not in self.career_profiles:
            raise ValueError(f"Unknown career path: {career_path}")

        profile = self.career_profiles[career_path]

        # Initialize simulation state
        current_salary = profile['entry_salary']
        current_burnout = profile['burnout_baseline']
        current_skills = worker_profile.get('skill_score', 50)
        current_market_value = 50

        # Storage for trajectories
        income_proj = []
        burnout_curve = []
        growth_traj = []
        skill_evol = []
        market_value_proj = []
        life_satisfaction = []

        # Simulate each year
        for year in range(time_horizon_years + 1):
            # Income projection
            salary = self._project_salary(
                current_salary,
                year,
                profile['salary_growth_rate'],
                profile['salary_ceiling']
            )

            # Burnout calculation
            burnout = self._calculate_burnout(
                profile['burnout_baseline'],
                year,
                profile['burnout_growth_rate'],
                profile['work_life_balance']
            )

            # Growth opportunities
            growth = self._calculate_growth_potential(
                profile['growth_potential'],
                year,
                current_skills
            )

            # Skill evolution
            skills = self._evolve_skills(
                current_skills,
                year,
                profile['skill_development_rate'],
                profile['automation_risk']
            )

            # Market value
            market_value = self._calculate_market_value(
                skills,
                salary,
                profile['automation_risk'],
                year
            )

            # Life satisfaction
            satisfaction = self._calculate_life_satisfaction(
                salary,
                burnout,
                growth,
                profile['work_life_balance']
            )

            # Store data points
            income_proj.append({
                'year': year,
                'salary': round(salary, 2),
                'real_salary': round(salary / ((1 + self.market_dynamics['inflation_rate']) ** year), 2),
                'total_compensation': round(salary * 1.15, 2)  # Include benefits
            })

            burnout_curve.append({
                'year': year,
                'burnout_level': round(burnout, 2),
                'burnout_risk': self._categorize_burnout(burnout),
                'recovery_time_weeks': self._calculate_recovery_time(burnout)
            })

            growth_traj.append({
                'year': year,
                'growth_score': round(growth, 2),
                'promotion_probability': self._calculate_promotion_probability(year, growth),
                'leadership_opportunities': year >= 3
            })

            skill_evol.append({
                'year': year,
                'skill_score': round(skills, 2),
                'skills_acquired': int(year * 3),  # ~3 skills per year
                'obsolete_skills': int(year * 1.5)  # ~1.5 skills obsolete per year
            })

            market_value_proj.append({
                'year': year,
                'market_value_index': round(market_value, 2),
                'employability_score': min(100, market_value * 1.1),
                'career_capital': round(salary * skills / 100, 2)
            })

            life_satisfaction.append({
                'year': year,
                'satisfaction_score': round(satisfaction, 2),
                'work_life_balance': profile['work_life_balance'],
                'overall_wellbeing': round((satisfaction + (100 - burnout)) / 2, 2)
            })

            # Update current values
            current_salary = salary
            current_burnout = burnout
            current_skills = skills
            current_market_value = market_value

        # Calculate summary metrics
        summary = self._calculate_summary_metrics(
            income_proj,
            burnout_curve,
            growth_traj,
            skill_evol,
            market_value_proj,
            life_satisfaction,
            profile
        )

        return CareerSimulation(
            career_path=career_path,
            time_horizon_years=time_horizon_years,
            income_projection=income_proj,
            burnout_curve=burnout_curve,
            growth_trajectory=growth_traj,
            skill_evolution=skill_evol,
            market_value_projection=market_value_proj,
            life_satisfaction=life_satisfaction,
            summary_metrics=summary
        )

    def _project_salary(
        self,
        base_salary: float,
        year: int,
        growth_rate: float,
        ceiling: float
    ) -> float:
        """Project salary with growth and ceiling"""
        # Exponential growth with ceiling
        projected = base_salary * ((1 + growth_rate) ** year)

        # Apply diminishing returns as approaching ceiling
        if projected > ceiling * 0.8:
            # Slow down growth near ceiling
            excess = projected - (ceiling * 0.8)
            projected = ceiling * 0.8 + (excess * 0.5)

        return min(projected, ceiling)

    def _calculate_burnout(
        self,
        baseline: float,
        year: int,
        growth_rate: float,
        work_life_balance: float
    ) -> float:
        """Calculate burnout level over time"""
        # Burnout increases over time but is moderated by work-life balance
        burnout = baseline + (year * 5 * growth_rate)

        # Work-life balance reduces burnout
        burnout = burnout * (1 - work_life_balance / 200)

        # Random fluctuations
        burnout += np.random.uniform(-5, 5)

        return max(0, min(100, burnout))

    def _calculate_growth_potential(
        self,
        base_potential: float,
        year: int,
        skill_score: float
    ) -> float:
        """Calculate growth opportunities"""
        # Growth potential starts high and stabilizes
        time_factor = 1 - (year / 20)  # Decreases over time

        growth = base_potential * time_factor * (skill_score / 100)

        return max(20, min(100, growth))

    def _evolve_skills(
        self,
        current_skills: float,
        year: int,
        development_rate: float,
        automation_risk: float
    ) -> float:
        """Evolve skill score over time"""
        # Skills grow but also face obsolescence
        growth = current_skills * (1 + development_rate)

        # Obsolescence factor
        obsolescence = automation_risk / 100 * 2  # Skills lose value

        net_skill_change = growth - obsolescence

        # Ensure skills don't fall too low
        return max(40, min(100, net_skill_change))

    def _calculate_market_value(
        self,
        skill_score: float,
        salary: float,
        automation_risk: float,
        year: int
    ) -> float:
        """Calculate market value index"""
        # Market value = skills + compensation - automation risk
        base_value = (skill_score * 0.6) + (min(100, salary / 2000) * 0.4)

        # Automation risk reduces market value over time
        automation_penalty = automation_risk * (year / 10) * 0.5

        market_value = base_value - automation_penalty

        return max(20, min(100, market_value))

    def _calculate_life_satisfaction(
        self,
        salary: float,
        burnout: float,
        growth: float,
        work_life_balance: float
    ) -> float:
        """Calculate overall life satisfaction"""
        # Multiple factors contribute
        income_satisfaction = min(100, salary / 1500)  # Diminishing returns

        satisfaction = (
            income_satisfaction * 0.3 +
            (100 - burnout) * 0.3 +
            growth * 0.2 +
            work_life_balance * 0.2
        )

        return max(0, min(100, satisfaction))

    def _categorize_burnout(self, burnout: float) -> str:
        """Categorize burnout level"""
        if burnout < 30:
            return 'Low Risk'
        elif burnout < 60:
            return 'Moderate Risk'
        elif burnout < 80:
            return 'High Risk'
        else:
            return 'Critical Risk'

    def _calculate_recovery_time(self, burnout: float) -> int:
        """Calculate weeks needed to recover from burnout"""
        if burnout < 30:
            return 1
        elif burnout < 60:
            return 2
        elif burnout < 80:
            return 4
        else:
            return 8

    def _calculate_promotion_probability(self, year: int, growth: float) -> float:
        """Calculate probability of promotion"""
        # More likely in early-mid career
        if year < 2:
            return 20
        elif year < 5:
            return 40 * (growth / 100)
        elif year < 8:
            return 30 * (growth / 100)
        else:
            return 15 * (growth / 100)

    def _calculate_summary_metrics(
        self,
        income: List[Dict],
        burnout: List[Dict],
        growth: List[Dict],
        skills: List[Dict],
        market_value: List[Dict],
        satisfaction: List[Dict],
        profile: Dict
    ) -> Dict:
        """Calculate summary metrics for simulation"""
        return {
            'total_earnings': sum(i['salary'] for i in income),
            'avg_annual_income': np.mean([i['salary'] for i in income]),
            'peak_income': max(i['salary'] for i in income),
            'income_growth': income[-1]['salary'] - income[0]['salary'],
            'avg_burnout': np.mean([b['burnout_level'] for b in burnout]),
            'peak_burnout': max(b['burnout_level'] for b in burnout),
            'burnout_trajectory': 'Increasing' if burnout[-1]['burnout_level'] > burnout[0]['burnout_level'] else 'Stable',
            'avg_growth_score': np.mean([g['growth_score'] for g in growth]),
            'skill_appreciation': skills[-1]['skill_score'] - skills[0]['skill_score'],
            'final_market_value': market_value[-1]['market_value_index'],
            'avg_life_satisfaction': np.mean([s['satisfaction_score'] for s in satisfaction]),
            'overall_recommendation': self._generate_recommendation(
                income, burnout, growth, market_value, satisfaction
            ),
            'risk_factors': self._identify_risk_factors(profile, burnout, market_value),
            'career_longevity': self._estimate_career_longevity(market_value, burnout)
        }

    def _generate_recommendation(
        self,
        income: List[Dict],
        burnout: List[Dict],
        growth: List[Dict],
        market_value: List[Dict],
        satisfaction: List[Dict]
    ) -> str:
        """Generate overall recommendation"""
        avg_satisfaction = np.mean([s['satisfaction_score'] for s in satisfaction])
        avg_burnout = np.mean([b['burnout_level'] for b in burnout])
        final_market_value = market_value[-1]['market_value_index']

        if avg_satisfaction > 70 and avg_burnout < 50 and final_market_value > 60:
            return "HIGHLY RECOMMENDED - Excellent balance of income, growth, and wellbeing"
        elif avg_satisfaction > 50 and avg_burnout < 65:
            return "RECOMMENDED - Good career path with manageable stress"
        elif avg_burnout > 75:
            return "CAUTION - High burnout risk, consider work-life balance strategies"
        elif final_market_value < 40:
            return "RECONSIDER - Low future market value, high automation risk"
        else:
            return "CONDITIONAL - Viable with proper planning and skill development"

    def _identify_risk_factors(
        self,
        profile: Dict,
        burnout: List[Dict],
        market_value: List[Dict]
    ) -> List[str]:
        """Identify career risk factors"""
        risks = []

        if profile['automation_risk'] > 60:
            risks.append("High automation risk")

        if max(b['burnout_level'] for b in burnout) > 80:
            risks.append("Severe burnout risk")

        if market_value[-1]['market_value_index'] < 50:
            risks.append("Declining market value")

        if profile['salary_ceiling'] < 100000:
            risks.append("Limited income ceiling")

        if profile['work_life_balance'] < 50:
            risks.append("Poor work-life balance")

        return risks if risks else ["No major risks identified"]

    def _estimate_career_longevity(
        self,
        market_value: List[Dict],
        burnout: List[Dict]
    ) -> int:
        """Estimate sustainable career length in years"""
        # Career longevity based on market value trajectory and burnout
        final_mv = market_value[-1]['market_value_index']
        avg_burnout = np.mean([b['burnout_level'] for b in burnout])

        if final_mv > 70 and avg_burnout < 50:
            return 25  # Full career
        elif final_mv > 50 and avg_burnout < 65:
            return 20
        elif final_mv > 40:
            return 15
        else:
            return 10  # Need reskilling

    def compare_career_paths(
        self,
        worker_profile: Dict,
        career_options: List[str],
        time_horizon: int = 10
    ) -> Dict:
        """
        Compare multiple career paths side-by-side

        Returns:
            Comparison matrix with recommendations
        """
        simulations = {}

        for career in career_options:
            if career in self.career_profiles:
                sim = self.simulate_career_path(career, worker_profile, time_horizon)
                simulations[career] = sim

        # Generate comparison
        comparison = {
            'careers_compared': list(simulations.keys()),
            'comparison_matrix': self._build_comparison_matrix(simulations),
            'best_for_income': self._rank_by_metric(simulations, 'total_earnings'),
            'best_for_satisfaction': self._rank_by_metric(simulations, 'avg_life_satisfaction'),
            'best_for_growth': self._rank_by_metric(simulations, 'avg_growth_score'),
            'lowest_burnout': self._rank_by_metric(simulations, 'avg_burnout', reverse=True),
            'overall_best': self._determine_overall_best(simulations)
        }

        return comparison

    def _build_comparison_matrix(self, simulations: Dict[str, CareerSimulation]) -> List[Dict]:
        """Build comparison matrix"""
        matrix = []

        for career, sim in simulations.items():
            matrix.append({
                'career': career,
                'total_earnings': sim.summary_metrics['total_earnings'],
                'avg_income': sim.summary_metrics['avg_annual_income'],
                'peak_income': sim.summary_metrics['peak_income'],
                'avg_burnout': sim.summary_metrics['avg_burnout'],
                'avg_satisfaction': sim.summary_metrics['avg_life_satisfaction'],
                'final_market_value': sim.summary_metrics['final_market_value'],
                'recommendation': sim.summary_metrics['overall_recommendation']
            })

        return matrix

    def _rank_by_metric(
        self,
        simulations: Dict[str, CareerSimulation],
        metric: str,
        reverse: bool = False
    ) -> List[Dict]:
        """Rank careers by specific metric"""
        rankings = []

        for career, sim in simulations.items():
            value = sim.summary_metrics.get(metric, 0)
            rankings.append({
                'career': career,
                'value': value
            })

        rankings.sort(key=lambda x: x['value'], reverse=not reverse)

        return rankings

    def _determine_overall_best(self, simulations: Dict[str, CareerSimulation]) -> Dict:
        """Determine overall best career based on weighted factors"""
        scores = {}

        for career, sim in simulations.items():
            # Weighted scoring
            score = (
                (sim.summary_metrics['avg_annual_income'] / 1000) * 0.30 +
                sim.summary_metrics['avg_life_satisfaction'] * 0.25 +
                (100 - sim.summary_metrics['avg_burnout']) * 0.20 +
                sim.summary_metrics['final_market_value'] * 0.15 +
                sim.summary_metrics['avg_growth_score'] * 0.10
            )

            scores[career] = score

        best_career = max(scores, key=scores.get)

        return {
            'recommended_career': best_career,
            'overall_score': round(scores[best_career], 2),
            'rationale': simulations[best_career].summary_metrics['overall_recommendation']
        }
