"""
Workforce Digital Twin™ - Real-time AI simulation of the labor market
Tracks, predicts, and simulates workforce dynamics at scale
"""
import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from collections import defaultdict
import json

@dataclass
class MarketSnapshot:
    """Snapshot of labor market state at a point in time"""
    timestamp: datetime
    total_jobs: int
    total_workers: int
    unemployment_rate: float
    avg_salary: float
    skills_demand: Dict[str, float]
    occupation_health: Dict[str, float]
    automation_index: float

class WorkforceDigitalTwin:
    """
    Real-time simulation of entire labor market ecosystem
    Models interactions between workers, jobs, skills, and automation
    """

    def __init__(self):
        self.current_state = None
        self.historical_snapshots = []
        self.occupation_models = {}
        self.region_data = {}

    def initialize_from_data(self, market_data: Dict):
        """Initialize digital twin with current market data"""
        self.current_state = MarketSnapshot(
            timestamp=datetime.now(),
            total_jobs=market_data.get('total_jobs', 0),
            total_workers=market_data.get('total_workers', 0),
            unemployment_rate=market_data.get('unemployment_rate', 0.0),
            avg_salary=market_data.get('avg_salary', 0.0),
            skills_demand=market_data.get('skills_demand', {}),
            occupation_health=market_data.get('occupation_health', {}),
            automation_index=market_data.get('automation_index', 0.0)
        )

    def simulate_market_dynamics(
        self,
        time_horizon_months: int = 12,
        automation_adoption_rate: float = 0.05
    ) -> List[MarketSnapshot]:
        """
        Simulate market evolution over time

        Args:
            time_horizon_months: How far to simulate into future
            automation_adoption_rate: Monthly % increase in automation

        Returns:
            List of market snapshots over time
        """
        simulations = []
        current = self.current_state

        for month in range(time_horizon_months):
            # Apply automation impact
            automation_factor = 1 + (automation_adoption_rate * month)

            # Simulate job displacement
            displaced_jobs = self._calculate_displacement(
                current.total_jobs,
                automation_factor
            )

            # Simulate new job creation (usually < displacement)
            new_jobs = self._calculate_job_creation(
                current.total_jobs,
                automation_factor
            )

            # Update market state
            next_state = MarketSnapshot(
                timestamp=current.timestamp + timedelta(days=30 * (month + 1)),
                total_jobs=int(current.total_jobs - displaced_jobs + new_jobs),
                total_workers=current.total_workers,
                unemployment_rate=self._calculate_unemployment(
                    current.total_workers,
                    current.total_jobs - displaced_jobs + new_jobs
                ),
                avg_salary=self._simulate_salary_movement(
                    current.avg_salary,
                    automation_factor
                ),
                skills_demand=self._evolve_skills_demand(
                    current.skills_demand,
                    automation_factor
                ),
                occupation_health=self._update_occupation_health(
                    current.occupation_health,
                    automation_factor
                ),
                automation_index=current.automation_index * automation_factor
            )

            simulations.append(next_state)
            current = next_state

        return simulations

    def _calculate_displacement(self, total_jobs: int, automation_factor: float) -> int:
        """Calculate jobs displaced by automation"""
        # Higher automation factor = more displacement
        base_displacement_rate = 0.02  # 2% monthly base
        displacement_rate = base_displacement_rate * automation_factor
        return int(total_jobs * displacement_rate)

    def _calculate_job_creation(self, total_jobs: int, automation_factor: float) -> int:
        """Calculate new jobs created (tech, AI, etc.)"""
        # New jobs grow with automation, but slower than displacement
        creation_rate = 0.015 * automation_factor  # 1.5% base
        return int(total_jobs * creation_rate)

    def _calculate_unemployment(self, workers: int, jobs: int) -> float:
        """Calculate unemployment rate"""
        if workers == 0:
            return 0.0
        return max(0.0, (workers - jobs) / workers * 100)

    def _simulate_salary_movement(self, current_avg: float, automation_factor: float) -> float:
        """Simulate average salary changes"""
        # Automation can increase salaries for tech roles, decrease for routine jobs
        # Simplified: slight increase overall but with variance
        growth_rate = 0.002 * automation_factor  # 0.2% monthly
        return current_avg * (1 + growth_rate)

    def _evolve_skills_demand(
        self,
        current_demand: Dict[str, float],
        automation_factor: float
    ) -> Dict[str, float]:
        """Evolve skill demand based on automation trends"""
        evolved = {}

        # Skills that increase with automation
        tech_skills = ['machine_learning', 'ai', 'data_science', 'cloud', 'cybersecurity']

        # Skills that decrease with automation
        routine_skills = ['data_entry', 'manual_assembly', 'basic_bookkeeping']

        for skill, demand in current_demand.items():
            if skill in tech_skills:
                # Increase demand
                evolved[skill] = min(100, demand * (1 + 0.03 * automation_factor))
            elif skill in routine_skills:
                # Decrease demand
                evolved[skill] = max(0, demand * (1 - 0.05 * automation_factor))
            else:
                # Gradual change
                evolved[skill] = demand * (1 + np.random.uniform(-0.01, 0.01))

        return evolved

    def _update_occupation_health(
        self,
        current_health: Dict[str, float],
        automation_factor: float
    ) -> Dict[str, float]:
        """Update health score for each occupation (0-100)"""
        updated = {}

        for occupation, health in current_health.items():
            # Occupations with high automation risk lose health
            if 'entry' in occupation.lower() or 'manual' in occupation.lower():
                updated[occupation] = max(0, health - 2 * automation_factor)
            elif 'engineer' in occupation.lower() or 'scientist' in occupation.lower():
                updated[occupation] = min(100, health + 1.5 * automation_factor)
            else:
                updated[occupation] = health

        return updated

    def predict_occupation_displacement(
        self,
        occupation: str,
        time_horizon_months: int = 18
    ) -> Dict:
        """
        Predict displacement probability for specific occupation

        Returns probability curve over time
        """
        # Get occupation's automation risk score
        base_risk = self._get_occupation_automation_risk(occupation)

        displacement_curve = []
        for month in range(time_horizon_months):
            # Risk increases over time
            monthly_risk = min(100, base_risk * (1 + month * 0.02))
            displacement_curve.append({
                'month': month,
                'displacement_probability': monthly_risk,
                'jobs_at_risk_pct': self._calculate_jobs_at_risk(monthly_risk)
            })

        return {
            'occupation': occupation,
            'current_risk': base_risk,
            'time_horizon_months': time_horizon_months,
            'displacement_curve': displacement_curve,
            'recommended_action': self._get_displacement_recommendation(base_risk)
        }

    def _get_occupation_automation_risk(self, occupation: str) -> float:
        """Get automation risk score for occupation"""
        # Simplified risk mapping
        high_risk = ['data entry', 'telemarketer', 'cashier', 'driver', 'assembler']
        medium_risk = ['accountant', 'paralegal', 'translator', 'customer service']
        low_risk = ['teacher', 'nurse', 'engineer', 'manager', 'therapist']

        occ_lower = occupation.lower()

        for high in high_risk:
            if high in occ_lower:
                return np.random.uniform(70, 95)

        for medium in medium_risk:
            if medium in occ_lower:
                return np.random.uniform(40, 70)

        for low in low_risk:
            if low in occ_lower:
                return np.random.uniform(10, 40)

        return 50  # Default medium risk

    def _calculate_jobs_at_risk(self, risk_score: float) -> float:
        """Convert risk score to % of jobs at risk"""
        # Non-linear relationship
        return min(100, risk_score * 0.8)

    def _get_displacement_recommendation(self, risk: float) -> str:
        """Get recommendation based on displacement risk"""
        if risk > 70:
            return "URGENT: Begin reskilling immediately. High automation risk."
        elif risk > 50:
            return "WARNING: Consider diversifying skills within 12 months."
        elif risk > 30:
            return "MONITOR: Stay updated on industry trends and emerging skills."
        else:
            return "STABLE: Continue developing current expertise."

    def model_automation_scenario(
        self,
        adoption_percentage: float,
        affected_occupations: List[str],
        time_horizon_months: int = 24
    ) -> Dict:
        """
        Model impact of automation adoption scenario

        Args:
            adoption_percentage: % of companies adopting automation (0-100)
            affected_occupations: List of occupations impacted
            time_horizon_months: Simulation period

        Returns:
            Detailed impact analysis
        """
        results = {
            'scenario': {
                'adoption_rate': adoption_percentage,
                'affected_occupations': affected_occupations,
                'time_horizon': time_horizon_months
            },
            'impact': {
                'jobs_displaced': 0,
                'workers_affected': 0,
                'new_jobs_created': 0,
                'unemployment_delta': 0.0,
                'gdp_impact': 0.0
            },
            'timeline': [],
            'occupation_details': []
        }

        # Calculate impact per occupation
        total_displaced = 0
        total_affected = 0

        for occupation in affected_occupations:
            occ_workers = np.random.randint(10000, 100000)  # Mock data
            displacement_rate = (adoption_percentage / 100) * 0.6  # 60% max displacement

            displaced = int(occ_workers * displacement_rate)
            total_displaced += displaced
            total_affected += occ_workers

            results['occupation_details'].append({
                'occupation': occupation,
                'workers': occ_workers,
                'displaced': displaced,
                'displacement_rate': displacement_rate * 100,
                'reskilling_required': displaced
            })

        # Model timeline
        for month in range(0, time_horizon_months, 3):  # Quarterly
            progress = month / time_horizon_months

            results['timeline'].append({
                'month': month,
                'cumulative_displaced': int(total_displaced * progress),
                'unemployment_rate': 5.0 + (progress * adoption_percentage / 10),
                'automation_index': adoption_percentage * progress
            })

        # Overall impact
        results['impact']['jobs_displaced'] = total_displaced
        results['impact']['workers_affected'] = total_affected
        results['impact']['new_jobs_created'] = int(total_displaced * 0.4)  # 40% replacement
        results['impact']['unemployment_delta'] = (total_displaced * 0.6) / 150000000 * 100  # Mock labor force
        results['impact']['gdp_impact'] = -0.5 * (adoption_percentage / 100)  # Negative short-term

        return results

    def calculate_macro_job_risk_index(self, market_data: Dict) -> Dict:
        """
        Calculate overall job market risk index (0-100)
        Updated monthly with latest data
        """
        factors = {
            'automation_adoption': market_data.get('automation_adoption', 0),
            'job_vacancy_rate': market_data.get('job_vacancy_rate', 0),
            'skill_mismatch_index': market_data.get('skill_mismatch', 0),
            'unemployment_trend': market_data.get('unemployment_trend', 0),
            'tech_disruption_rate': market_data.get('tech_disruption', 0)
        }

        # Weighted calculation
        risk_index = (
            factors['automation_adoption'] * 0.30 +
            factors['skill_mismatch_index'] * 0.25 +
            factors['tech_disruption_rate'] * 0.20 +
            factors['unemployment_trend'] * 0.15 +
            (100 - factors['job_vacancy_rate']) * 0.10
        )

        # Determine risk level
        if risk_index > 70:
            level = 'Critical'
            recommendation = 'Major workforce intervention needed'
        elif risk_index > 50:
            level = 'High'
            recommendation = 'Accelerate reskilling programs'
        elif risk_index > 30:
            level = 'Moderate'
            recommendation = 'Monitor trends closely'
        else:
            level = 'Low'
            recommendation = 'Maintain current policies'

        return {
            'index': round(risk_index, 2),
            'level': level,
            'timestamp': datetime.now().isoformat(),
            'factors': factors,
            'recommendation': recommendation,
            'trend': self._calculate_trend(risk_index)
        }

    def _calculate_trend(self, current_index: float) -> str:
        """Calculate if risk is increasing or decreasing"""
        # Simplified - compare to historical
        if len(self.historical_snapshots) > 0:
            prev_index = self.historical_snapshots[-1].automation_index
            if current_index > prev_index * 1.05:
                return 'Increasing'
            elif current_index < prev_index * 0.95:
                return 'Decreasing'
        return 'Stable'

    def generate_region_risk_heatmap(
        self,
        regions: List[str],
        market_data_by_region: Dict[str, Dict]
    ) -> Dict:
        """
        Generate risk heatmap data for geographical regions

        Returns:
            Risk scores and metadata for each region
        """
        heatmap = {
            'regions': [],
            'timestamp': datetime.now().isoformat(),
            'global_avg_risk': 0.0
        }

        total_risk = 0

        for region in regions:
            region_data = market_data_by_region.get(region, {})

            # Calculate region-specific risk
            risk_score = self._calculate_regional_risk(region_data)

            heatmap['regions'].append({
                'name': region,
                'risk_score': risk_score,
                'risk_level': self._categorize_risk(risk_score),
                'primary_industries': region_data.get('industries', []),
                'unemployment_rate': region_data.get('unemployment', 0),
                'automation_adoption': region_data.get('automation_adoption', 0),
                'workers_at_risk': region_data.get('total_workers', 0) * (risk_score / 100),
                'top_threatened_occupations': self._get_top_threatened(region_data)
            })

            total_risk += risk_score

        heatmap['global_avg_risk'] = round(total_risk / len(regions), 2) if regions else 0

        return heatmap

    def _calculate_regional_risk(self, region_data: Dict) -> float:
        """Calculate risk score for a specific region"""
        # Factors: industry composition, automation adoption, unemployment
        industry_risk = region_data.get('industry_automation_exposure', 50)
        unemployment = region_data.get('unemployment', 5)
        automation_rate = region_data.get('automation_adoption', 30)

        risk = (
            industry_risk * 0.5 +
            automation_rate * 0.3 +
            unemployment * 2  # Unemployment is 0-10%, scale to 0-20
        )

        return min(100, risk)

    def _categorize_risk(self, score: float) -> str:
        """Categorize risk score"""
        if score > 70:
            return 'High Risk'
        elif score > 50:
            return 'Elevated Risk'
        elif score > 30:
            return 'Moderate Risk'
        else:
            return 'Low Risk'

    def _get_top_threatened(self, region_data: Dict) -> List[str]:
        """Get top threatened occupations in region"""
        # Simplified - return common high-risk occupations
        return [
            'Retail Salesperson',
            'Office Clerk',
            'Data Entry Specialist',
            'Cashier',
            'Driver'
        ][:3]

    def generate_predictive_alert(
        self,
        occupation: str,
        worker_location: str,
        time_horizon_months: int = 18
    ) -> Dict:
        """
        Generate predictive alert for worker
        Example: "30% of bookkeeping tasks automated in 18 months in your field"
        """
        # Get occupation-specific prediction
        displacement_pred = self.predict_occupation_displacement(occupation, time_horizon_months)

        # Calculate task automation percentage
        task_automation_pct = self._predict_task_automation(occupation, time_horizon_months)

        # Determine urgency
        risk_level = displacement_pred['current_risk']
        if risk_level > 70:
            urgency = 'CRITICAL'
            action = 'Begin transition planning immediately'
        elif risk_level > 50:
            urgency = 'HIGH'
            action = 'Start exploring reskilling options within 3 months'
        elif risk_level > 30:
            urgency = 'MEDIUM'
            action = 'Monitor market trends and prepare for potential changes'
        else:
            urgency = 'LOW'
            action = 'Stay informed about industry developments'

        return {
            'occupation': occupation,
            'location': worker_location,
            'alert': f"{task_automation_pct}% of {occupation} tasks projected to be automated within {time_horizon_months} months in your region",
            'urgency': urgency,
            'displacement_probability': displacement_pred['current_risk'],
            'recommended_action': action,
            'timeline': time_horizon_months,
            'timestamp': datetime.now().isoformat(),
            'similar_workers_affected': np.random.randint(1000, 50000)  # Mock data
        }

    def _predict_task_automation(self, occupation: str, months: int) -> int:
        """Predict % of tasks that will be automated"""
        base_automation = self._get_occupation_automation_risk(occupation)

        # Tasks automate faster than full job displacement
        task_rate = base_automation * (1 + months / 100)

        return min(95, int(task_rate))
