import numpy as np
from typing import Dict, List, Tuple
from sklearn.metrics.pairwise import cosine_similarity

class WorkerJobMatcher:
    """
    ML-based matching algorithm to connect displaced workers with opportunities
    Uses skill matching, location preferences, and adaptability factors
    """

    def __init__(self):
        self.skill_weights = {
            'required': 1.0,
            'preferred': 0.5
        }

    def calculate_skill_match(
        self,
        worker_skills: List[Dict],
        job_skills: List[Dict]
    ) -> Dict[str, float]:
        """
        Calculate skill match score between worker and job

        Args:
            worker_skills: List of {skill_id, proficiency_level}
            job_skills: List of {skill_id, required, importance}

        Returns:
            Match metrics
        """
        worker_skill_map = {s['skill_id']: s['proficiency_level'] for s in worker_skills}

        required_skills = [s for s in job_skills if s.get('required', True)]
        preferred_skills = [s for s in job_skills if not s.get('required', True)]

        # Required skills match
        required_matched = 0
        required_total = len(required_skills)
        required_quality = []

        for skill in required_skills:
            if skill['skill_id'] in worker_skill_map:
                required_matched += 1
                proficiency = worker_skill_map[skill['skill_id']]
                importance = skill.get('importance', 3)
                # Quality score: proficiency weighted by importance
                required_quality.append((proficiency / 5.0) * (importance / 5.0))

        # Preferred skills match
        preferred_matched = 0
        preferred_total = len(preferred_skills)

        for skill in preferred_skills:
            if skill['skill_id'] in worker_skill_map:
                preferred_matched += 1

        # Calculate scores
        required_score = (required_matched / required_total * 100) if required_total > 0 else 100
        preferred_score = (preferred_matched / preferred_total * 100) if preferred_total > 0 else 0
        quality_score = (sum(required_quality) / len(required_quality) * 100) if required_quality else 0

        # Overall match (weighted)
        overall_match = (
            required_score * 0.6 +
            quality_score * 0.3 +
            preferred_score * 0.1
        )

        return {
            'overall_match': round(overall_match, 2),
            'required_skills_match': round(required_score, 2),
            'preferred_skills_match': round(preferred_score, 2),
            'skill_quality_score': round(quality_score, 2),
            'missing_required_skills': required_total - required_matched
        }

    def calculate_location_match(
        self,
        worker_location: str,
        job_location: str,
        remote_friendly: bool
    ) -> float:
        """Calculate location compatibility score"""
        if remote_friendly:
            return 100.0

        # Simple location matching (can be enhanced with geocoding)
        if worker_location.lower() == job_location.lower():
            return 100.0

        # Check if same state/region (basic)
        worker_parts = worker_location.split(',')
        job_parts = job_location.split(',')

        if len(worker_parts) > 1 and len(job_parts) > 1:
            if worker_parts[-1].strip() == job_parts[-1].strip():
                return 60.0  # Same state/region

        return 30.0  # Different locations

    def calculate_salary_match(
        self,
        worker_expected_salary: int,
        job_salary_min: int,
        job_salary_max: int
    ) -> float:
        """Calculate salary compatibility score"""
        if job_salary_min is None or job_salary_max is None:
            return 50.0  # Unknown salary

        if worker_expected_salary is None:
            return 75.0  # Worker flexible on salary

        if job_salary_min <= worker_expected_salary <= job_salary_max:
            return 100.0
        elif worker_expected_salary < job_salary_min:
            return 100.0  # Job pays more than expected
        else:
            # Calculate how far above max the expectation is
            overage = (worker_expected_salary - job_salary_max) / job_salary_max
            if overage < 0.1:
                return 80.0
            elif overage < 0.2:
                return 60.0
            else:
                return 30.0

    def match_worker_to_job(
        self,
        worker: Dict,
        job: Dict,
        worker_skills: List[Dict],
        job_skills: List[Dict]
    ) -> Dict:
        """
        Calculate comprehensive match score between worker and job

        Returns:
            Detailed match analysis
        """
        # Skill matching
        skill_match = self.calculate_skill_match(worker_skills, job_skills)

        # Location matching
        location_score = self.calculate_location_match(
            worker.get('location', ''),
            job.get('location', ''),
            job.get('remote_friendly', False)
        )

        # Salary matching
        salary_score = self.calculate_salary_match(
            worker.get('expected_salary'),
            job.get('salary_min'),
            job.get('salary_max')
        )

        # Experience level match
        experience_match = self._calculate_experience_match(
            worker.get('years_experience', 0),
            job.get('required_experience', 0)
        )

        # Calculate overall match score (weighted)
        overall_score = (
            skill_match['overall_match'] * 0.50 +
            location_score * 0.20 +
            salary_score * 0.15 +
            experience_match * 0.15
        )

        return {
            'match_score': round(overall_score, 2),
            'match_level': self._categorize_match(overall_score),
            'skill_analysis': skill_match,
            'location_score': location_score,
            'salary_score': salary_score,
            'experience_score': experience_match,
            'recommendation': self._generate_recommendation(overall_score, skill_match)
        }

    def _calculate_experience_match(
        self,
        worker_experience: int,
        required_experience: int
    ) -> float:
        """Calculate experience level match"""
        if required_experience == 0:
            return 100.0

        if worker_experience >= required_experience:
            # Has required experience
            overage = worker_experience - required_experience
            if overage > 10:
                return 90.0  # May be overqualified
            return 100.0
        else:
            # Below required experience
            gap = required_experience - worker_experience
            gap_percent = gap / required_experience

            if gap_percent < 0.2:
                return 80.0
            elif gap_percent < 0.4:
                return 60.0
            else:
                return 40.0

    def _categorize_match(self, score: float) -> str:
        """Categorize match score into levels"""
        if score >= 80:
            return 'excellent'
        elif score >= 65:
            return 'good'
        elif score >= 50:
            return 'fair'
        else:
            return 'poor'

    def _generate_recommendation(
        self,
        overall_score: float,
        skill_match: Dict
    ) -> str:
        """Generate recommendation text based on match"""
        if overall_score >= 80:
            return "Strong match - highly recommended to apply"
        elif overall_score >= 65:
            return "Good match - recommended to apply"
        elif overall_score >= 50:
            if skill_match['missing_required_skills'] > 0:
                return f"Consider acquiring {skill_match['missing_required_skills']} missing skills before applying"
            return "Fair match - apply if interested"
        else:
            return "Significant skill gaps - focus on reskilling first"

    def rank_jobs_for_worker(
        self,
        worker: Dict,
        worker_skills: List[Dict],
        jobs: List[Dict],
        jobs_skills: Dict[int, List[Dict]],
        top_n: int = 10
    ) -> List[Dict]:
        """
        Rank all jobs for a worker and return top matches

        Args:
            worker: Worker data
            worker_skills: Worker's skills
            jobs: List of job postings
            jobs_skills: Mapping of job_id to required skills
            top_n: Number of top matches to return

        Returns:
            Ranked list of job matches
        """
        matches = []

        for job in jobs:
            job_id = job['id']
            match_result = self.match_worker_to_job(
                worker,
                job,
                worker_skills,
                jobs_skills.get(job_id, [])
            )

            matches.append({
                'job_id': job_id,
                'job_title': job['title'],
                'company': job['company'],
                'match_score': match_result['match_score'],
                'match_level': match_result['match_level'],
                'recommendation': match_result['recommendation'],
                'details': match_result
            })

        # Sort by match score
        matches.sort(key=lambda x: x['match_score'], reverse=True)

        return matches[:top_n]
