from typing import Dict, List, Tuple
import numpy as np

class ReskillingAdvisor:
    """
    AI-powered reskilling pathway recommendation system
    Analyzes skill gaps and recommends personalized learning paths
    """

    def __init__(self):
        self.skill_learning_times = {}  # skill_id -> estimated weeks

    def analyze_skill_gap(
        self,
        current_skills: List[Dict],
        target_job_skills: List[Dict],
        skill_metadata: Dict[int, Dict]
    ) -> Dict:
        """
        Analyze gap between current skills and target job

        Args:
            current_skills: Worker's current skills with proficiency
            target_job_skills: Required skills for target job
            skill_metadata: Full skill information (name, category, etc.)

        Returns:
            Comprehensive skill gap analysis
        """
        current_skill_map = {s['skill_id']: s['proficiency_level'] for s in current_skills}

        missing_skills = []
        upgrade_skills = []
        matched_skills = []

        for job_skill in target_job_skills:
            skill_id = job_skill['skill_id']
            required = job_skill.get('required', True)
            importance = job_skill.get('importance', 3)

            skill_info = skill_metadata.get(skill_id, {})

            if skill_id not in current_skill_map:
                # Completely missing skill
                missing_skills.append({
                    'skill_id': skill_id,
                    'skill_name': skill_info.get('name', 'Unknown'),
                    'category': skill_info.get('category', 'technical'),
                    'required': required,
                    'importance': importance,
                    'target_proficiency': 3,  # Target intermediate level
                    'estimated_learning_time_weeks': self._estimate_learning_time(skill_info)
                })
            else:
                current_proficiency = current_skill_map[skill_id]
                target_proficiency = 3  # Target intermediate level for job readiness

                if current_proficiency < target_proficiency:
                    # Needs improvement
                    upgrade_skills.append({
                        'skill_id': skill_id,
                        'skill_name': skill_info.get('name', 'Unknown'),
                        'category': skill_info.get('category', 'technical'),
                        'current_proficiency': current_proficiency,
                        'target_proficiency': target_proficiency,
                        'gap': target_proficiency - current_proficiency,
                        'estimated_learning_time_weeks': self._estimate_upgrade_time(
                            current_proficiency,
                            target_proficiency
                        )
                    })
                else:
                    # Already proficient
                    matched_skills.append({
                        'skill_id': skill_id,
                        'skill_name': skill_info.get('name', 'Unknown'),
                        'proficiency': current_proficiency
                    })

        # Calculate overall readiness
        total_required = len([s for s in target_job_skills if s.get('required', True)])
        matched_required = len([s for s in matched_skills
                               if any(js['skill_id'] == s['skill_id'] and js.get('required', True)
                                     for js in target_job_skills)])

        readiness_score = (matched_required / total_required * 100) if total_required > 0 else 0

        return {
            'readiness_score': round(readiness_score, 2),
            'missing_skills': missing_skills,
            'skills_to_upgrade': upgrade_skills,
            'matched_skills': matched_skills,
            'total_estimated_weeks': sum(s['estimated_learning_time_weeks'] for s in missing_skills) +
                                    sum(s['estimated_learning_time_weeks'] for s in upgrade_skills)
        }

    def _estimate_learning_time(self, skill_info: Dict) -> int:
        """Estimate weeks needed to learn a skill from scratch"""
        category = skill_info.get('category', 'technical')

        # Base estimates by category
        base_times = {
            'technical': 12,  # 12 weeks for technical skills
            'soft': 6,        # 6 weeks for soft skills
            'domain': 8       # 8 weeks for domain knowledge
        }

        return base_times.get(category, 10)

    def _estimate_upgrade_time(self, current: int, target: int) -> int:
        """Estimate weeks needed to upgrade proficiency"""
        gap = target - current
        return gap * 4  # 4 weeks per proficiency level

    def recommend_learning_path(
        self,
        skill_gap_analysis: Dict,
        training_programs: List[Dict],
        worker_preferences: Dict = None
    ) -> Dict:
        """
        Recommend personalized learning path with training programs

        Args:
            skill_gap_analysis: Output from analyze_skill_gap
            training_programs: Available training programs
            worker_preferences: Budget, time, format preferences

        Returns:
            Recommended learning path
        """
        if worker_preferences is None:
            worker_preferences = {}

        max_budget = worker_preferences.get('max_budget', 5000)
        max_duration_weeks = worker_preferences.get('max_duration_weeks', 26)
        online_only = worker_preferences.get('online_only', True)

        missing_skills = skill_gap_analysis['missing_skills']
        upgrade_skills = skill_gap_analysis['skills_to_upgrade']

        # Prioritize skills
        priority_skills = self._prioritize_skills(missing_skills, upgrade_skills)

        # Match training programs
        recommended_programs = self._match_training_programs(
            priority_skills,
            training_programs,
            max_budget,
            max_duration_weeks,
            online_only
        )

        # Create learning sequence
        learning_path = self._create_learning_sequence(
            recommended_programs,
            priority_skills
        )

        total_cost = sum(p['cost'] for p in recommended_programs)
        total_duration = sum(p['duration_weeks'] for p in recommended_programs)

        return {
            'recommended_programs': recommended_programs,
            'learning_sequence': learning_path,
            'total_cost': total_cost,
            'total_duration_weeks': total_duration,
            'estimated_completion_date': self._calculate_completion_date(total_duration),
            'budget_fit': total_cost <= max_budget,
            'time_fit': total_duration <= max_duration_weeks,
            'skills_covered': [s['skill_name'] for s in priority_skills]
        }

    def _prioritize_skills(
        self,
        missing_skills: List[Dict],
        upgrade_skills: List[Dict]
    ) -> List[Dict]:
        """Prioritize skills by importance and requirement"""
        all_skills = []

        # Required missing skills - highest priority
        for skill in missing_skills:
            if skill['required']:
                all_skills.append({
                    **skill,
                    'priority': 1,
                    'priority_score': skill['importance'] * 10
                })

        # Skills to upgrade - medium priority
        for skill in upgrade_skills:
            all_skills.append({
                **skill,
                'priority': 2,
                'priority_score': skill.get('gap', 1) * 5
            })

        # Optional missing skills - lower priority
        for skill in missing_skills:
            if not skill['required']:
                all_skills.append({
                    **skill,
                    'priority': 3,
                    'priority_score': skill['importance'] * 3
                })

        # Sort by priority then priority_score
        all_skills.sort(key=lambda x: (x['priority'], -x['priority_score']))

        return all_skills

    def _match_training_programs(
        self,
        priority_skills: List[Dict],
        training_programs: List[Dict],
        max_budget: float,
        max_duration: int,
        online_only: bool
    ) -> List[Dict]:
        """Match training programs to skill needs"""
        recommended = []
        covered_skills = set()
        remaining_budget = max_budget
        remaining_time = max_duration

        # Filter programs by preferences
        filtered_programs = [
            p for p in training_programs
            if (not online_only or p.get('online', True))
        ]

        for skill in priority_skills:
            if skill['skill_id'] in covered_skills:
                continue

            # Find programs that teach this skill
            matching_programs = [
                p for p in filtered_programs
                if skill['skill_id'] in p.get('target_skills', [])
                and p.get('cost', 0) <= remaining_budget
                and p.get('duration_weeks', 0) <= remaining_time
            ]

            if matching_programs:
                # Select best program (by success rate and cost-effectiveness)
                best_program = max(
                    matching_programs,
                    key=lambda p: p.get('success_rate', 0.5) / (p.get('cost', 1) / 1000)
                )

                recommended.append(best_program)
                covered_skills.update(best_program.get('target_skills', []))
                remaining_budget -= best_program.get('cost', 0)
                remaining_time -= best_program.get('duration_weeks', 0)

        return recommended

    def _create_learning_sequence(
        self,
        programs: List[Dict],
        skills: List[Dict]
    ) -> List[Dict]:
        """Create optimal sequence for learning programs"""
        # Simple sequencing by dependencies and difficulty
        sequence = []

        # Group by category: fundamentals first, then advanced
        fundamentals = [p for p in programs if 'fundamental' in p.get('title', '').lower()]
        intermediate = [p for p in programs if 'intermediate' in p.get('title', '').lower()]
        advanced = [p for p in programs if 'advanced' in p.get('title', '').lower()]
        other = [p for p in programs if p not in fundamentals + intermediate + advanced]

        sequence_order = fundamentals + other + intermediate + advanced

        for i, program in enumerate(sequence_order, 1):
            sequence.append({
                'step': i,
                'program_id': program['id'],
                'program_title': program['title'],
                'duration_weeks': program.get('duration_weeks', 0),
                'start_after_weeks': sum(p.get('duration_weeks', 0) for p in sequence_order[:i-1])
            })

        return sequence

    def _calculate_completion_date(self, weeks: int) -> str:
        """Calculate estimated completion date"""
        from datetime import datetime, timedelta
        completion = datetime.now() + timedelta(weeks=weeks)
        return completion.strftime('%Y-%m-%d')

    def track_progress(
        self,
        learning_path: Dict,
        completed_programs: List[int],
        skills_acquired: List[int]
    ) -> Dict:
        """Track learner progress through reskilling path"""
        total_programs = len(learning_path['recommended_programs'])
        completed_count = len(completed_programs)

        progress_percent = (completed_count / total_programs * 100) if total_programs > 0 else 0

        remaining_programs = [
            p for p in learning_path['recommended_programs']
            if p['id'] not in completed_programs
        ]

        return {
            'progress_percent': round(progress_percent, 2),
            'programs_completed': completed_count,
            'programs_total': total_programs,
            'skills_acquired': len(skills_acquired),
            'remaining_programs': remaining_programs,
            'estimated_weeks_remaining': sum(p.get('duration_weeks', 0) for p in remaining_programs)
        }
