"""
Personal Reskilling Plan (PRP) Autopilot
Dynamically generates and adapts learning plans based on real-time market data
"""
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
import json

@dataclass
class MicroLesson:
    """5-minute micro-learning unit"""
    lesson_id: str
    skill_target: str
    title: str
    content: str
    duration_minutes: int
    difficulty: str  # beginner, intermediate, advanced
    prerequisites: List[str]
    practice_exercises: List[Dict]
    estimated_mastery_gain: float  # 0-10% mastery per lesson

@dataclass
class PersonalReskillingPlan:
    """Adaptive reskilling plan for individual worker"""
    worker_id: int
    target_role: str
    current_readiness: float
    target_readiness: float
    estimated_completion_weeks: int
    learning_modules: List[Dict]
    weekly_schedule: List[Dict]
    adaptation_triggers: List[str]
    last_updated: datetime

class ReskillingAutopilot:
    """
    AI-powered autopilot that generates and adapts reskilling plans
    Updates weekly based on market trends and learner progress
    """

    def __init__(self):
        self.micro_lesson_library = self._initialize_lesson_library()

    def _initialize_lesson_library(self) -> Dict[str, List[MicroLesson]]:
        """Initialize library of micro-lessons"""
        return {
            'python': self._generate_python_lessons(),
            'machine_learning': self._generate_ml_lessons(),
            'data_analysis': self._generate_data_lessons(),
            'cloud': self._generate_cloud_lessons()
        }

    def generate_personal_reskilling_plan(
        self,
        worker_id: int,
        skill_graph: Dict,
        target_role: Dict,
        market_trends: Dict,
        learning_preferences: Dict = None
    ) -> PersonalReskillingPlan:
        """
        Generate comprehensive Personal Reskilling Plan

        Args:
            worker_id: Worker identifier
            skill_graph: Output from SkillGraphGenerator
            target_role: Target role requirements
            market_trends: Current market data
            learning_preferences: Learning style, time availability, etc.

        Returns:
            Personalized reskilling plan
        """
        if learning_preferences is None:
            learning_preferences = {}

        # Analyze skill gaps
        gaps = self._analyze_skill_gaps(skill_graph, target_role)

        # Prioritize skills based on market trends
        prioritized_skills = self._prioritize_by_market(gaps, market_trends)

        # Generate learning modules
        modules = self._generate_learning_modules(
            prioritized_skills,
            learning_preferences
        )

        # Create weekly schedule
        weekly_schedule = self._create_adaptive_schedule(
            modules,
            learning_preferences.get('hours_per_week', 10)
        )

        # Calculate readiness
        current_readiness = self._calculate_readiness(skill_graph['metrics'], target_role)
        target_readiness = 85.0  # Target 85% readiness

        # Estimate completion time
        estimated_weeks = self._estimate_completion(modules, learning_preferences)

        # Set adaptation triggers
        triggers = [
            'Weekly progress below 70% of target',
            'New high-priority skill emerges in market',
            'Learner consistently struggles with module',
            'Automation threat increases for target role',
            'Better learning path discovered'
        ]

        return PersonalReskillingPlan(
            worker_id=worker_id,
            target_role=target_role['title'],
            current_readiness=current_readiness,
            target_readiness=target_readiness,
            estimated_completion_weeks=estimated_weeks,
            learning_modules=modules,
            weekly_schedule=weekly_schedule,
            adaptation_triggers=triggers,
            last_updated=datetime.now()
        )

    def _analyze_skill_gaps(self, skill_graph: Dict, target_role: Dict) -> List[Dict]:
        """Analyze gaps between current skills and target"""
        current_skills = {s['skill_name']: s for s in skill_graph['nodes']}
        required_skills = target_role.get('required_skills', [])

        gaps = []

        for req_skill in required_skills:
            if req_skill['name'] not in current_skills:
                gaps.append({
                    'skill_name': req_skill['name'],
                    'current_proficiency': 0,
                    'target_proficiency': req_skill.get('required_proficiency', 70),
                    'gap_size': req_skill.get('required_proficiency', 70),
                    'priority': req_skill.get('priority', 'medium')
                })
            else:
                current = current_skills[req_skill['name']]
                target_prof = req_skill.get('required_proficiency', 70)
                if current['proficiency'] < target_prof:
                    gaps.append({
                        'skill_name': req_skill['name'],
                        'current_proficiency': current['proficiency'],
                        'target_proficiency': target_prof,
                        'gap_size': target_prof - current['proficiency'],
                        'priority': req_skill.get('priority', 'medium')
                    })

        return gaps

    def _prioritize_by_market(
        self,
        gaps: List[Dict],
        market_trends: Dict
    ) -> List[Dict]:
        """Prioritize skills based on market demand and trends"""
        skill_demand = market_trends.get('skills_demand', {})

        for gap in gaps:
            demand = skill_demand.get(gap['skill_name'], 50)

            # Calculate priority score
            priority_score = (
                gap['gap_size'] * 0.3 +
                demand * 0.4 +
                (100 if gap['priority'] == 'high' else 50) * 0.3
            )

            gap['market_priority_score'] = priority_score

        # Sort by priority
        return sorted(gaps, key=lambda x: x['market_priority_score'], reverse=True)

    def _generate_learning_modules(
        self,
        prioritized_gaps: List[Dict],
        preferences: Dict
    ) -> List[Dict]:
        """Generate learning modules for each skill gap"""
        modules = []

        for i, gap in enumerate(prioritized_gaps):
            skill_name = gap['skill_name']

            # Get micro-lessons for this skill
            lessons = self._get_lessons_for_skill(skill_name, gap['gap_size'])

            # Generate practice projects
            projects = self._generate_practice_projects(skill_name, gap['target_proficiency'])

            # Create module
            module = {
                'module_id': f"module_{i+1}",
                'skill_target': skill_name,
                'current_proficiency': gap['current_proficiency'],
                'target_proficiency': gap['target_proficiency'],
                'total_micro_lessons': len(lessons),
                'lessons': lessons,
                'practice_projects': projects,
                'estimated_hours': len(lessons) * 0.1 + len(projects) * 2,  # 5min lessons + 2hr projects
                'ai_tutor_available': True,
                'completion_criteria': {
                    'lessons_completed': len(lessons),
                    'projects_passed': len(projects),
                    'proficiency_gained': gap['gap_size']
                }
            }

            modules.append(module)

        return modules

    def _get_lessons_for_skill(self, skill_name: str, gap_size: float) -> List[Dict]:
        """Get appropriate micro-lessons for skill"""
        # Number of lessons based on gap size
        num_lessons = max(10, int(gap_size / 2))  # ~20 lessons for 40 point gap

        lessons = []

        # Progressive difficulty
        for i in range(num_lessons):
            progress = i / num_lessons

            if progress < 0.3:
                difficulty = 'beginner'
            elif progress < 0.7:
                difficulty = 'intermediate'
            else:
                difficulty = 'advanced'

            lessons.append({
                'lesson_id': f"{skill_name}_lesson_{i+1}",
                'title': f"{skill_name.title()} - Part {i+1}",
                'duration_minutes': 5,
                'difficulty': difficulty,
                'topics': self._generate_lesson_topics(skill_name, difficulty),
                'practice_exercises': self._generate_practice_exercises(skill_name, difficulty),
                'estimated_mastery_gain': gap_size / num_lessons
            })

        return lessons

    def _generate_lesson_topics(self, skill_name: str, difficulty: str) -> List[str]:
        """Generate topics for a lesson"""
        topics_map = {
            'python': {
                'beginner': ['Variables', 'Data Types', 'Basic Operations'],
                'intermediate': ['Functions', 'Classes', 'File I/O'],
                'advanced': ['Decorators', 'Generators', 'Async Programming']
            },
            'machine_learning': {
                'beginner': ['ML Concepts', 'Supervised Learning', 'Data Prep'],
                'intermediate': ['Model Training', 'Feature Engineering', 'Validation'],
                'advanced': ['Deep Learning', 'Model Optimization', 'Production ML']
            }
        }

        return topics_map.get(skill_name, {}).get(difficulty, ['Topic 1', 'Topic 2', 'Topic 3'])

    def _generate_practice_exercises(self, skill_name: str, difficulty: str) -> List[Dict]:
        """Generate practice exercises for lesson"""
        return [
            {
                'exercise_id': f"ex_{skill_name}_{difficulty}_1",
                'type': 'code_challenge',
                'auto_graded': True,
                'estimated_minutes': 3
            }
        ]

    def _generate_practice_projects(self, skill_name: str, target_prof: float) -> List[Dict]:
        """Generate hands-on practice projects"""
        num_projects = max(2, int(target_prof / 30))  # 2-3 projects typically

        projects = []

        for i in range(num_projects):
            projects.append({
                'project_id': f"{skill_name}_project_{i+1}",
                'title': f"{skill_name.title()} Capstone {i+1}",
                'description': f"Build a real-world application using {skill_name}",
                'difficulty': 'intermediate' if i == 0 else 'advanced',
                'estimated_hours': 3 + i * 2,
                'auto_grading': True,
                'ai_feedback': True,
                'rubric': {
                    'functionality': 40,
                    'code_quality': 30,
                    'best_practices': 30
                }
            })

        return projects

    def _create_adaptive_schedule(
        self,
        modules: List[Dict],
        hours_per_week: int
    ) -> List[Dict]:
        """Create weekly learning schedule"""
        schedule = []

        # Distribute modules across weeks
        total_hours = sum(m['estimated_hours'] for m in modules)
        total_weeks = max(1, int(np.ceil(total_hours / hours_per_week)))

        hours_allocated = 0
        current_week = 1
        current_week_hours = 0
        current_week_activities = []

        for module in modules:
            module_hours = module['estimated_hours']

            # Check if module fits in current week
            if current_week_hours + module_hours <= hours_per_week:
                current_week_activities.append({
                    'module_id': module['module_id'],
                    'skill_target': module['skill_target'],
                    'activities': [
                        f"Complete {module['total_micro_lessons']} micro-lessons",
                        f"Work on {len(module['practice_projects'])} projects"
                    ],
                    'hours': module_hours
                })
                current_week_hours += module_hours
            else:
                # Save current week and start new one
                if current_week_activities:
                    schedule.append({
                        'week': current_week,
                        'total_hours': current_week_hours,
                        'modules': current_week_activities,
                        'checkpoint': f"Week {current_week} Assessment"
                    })

                current_week += 1
                current_week_hours = module_hours
                current_week_activities = [{
                    'module_id': module['module_id'],
                    'skill_target': module['skill_target'],
                    'activities': [
                        f"Complete {module['total_micro_lessons']} micro-lessons",
                        f"Work on {len(module['practice_projects'])} projects"
                    ],
                    'hours': module_hours
                }]

        # Add last week
        if current_week_activities:
            schedule.append({
                'week': current_week,
                'total_hours': current_week_hours,
                'modules': current_week_activities,
                'checkpoint': f"Week {current_week} Assessment"
            })

        return schedule

    def _calculate_readiness(self, current_metrics: Dict, target_role: Dict) -> float:
        """Calculate current readiness for target role"""
        # Simplified calculation
        skill_match = current_metrics.get('market_alignment_score', 50)
        skill_depth = current_metrics.get('skill_depth_score', 50)

        readiness = (skill_match * 0.6 + skill_depth * 0.4)

        return round(readiness, 2)

    def _estimate_completion(self, modules: List[Dict], preferences: Dict) -> int:
        """Estimate weeks to completion"""
        total_hours = sum(m['estimated_hours'] for m in modules)
        hours_per_week = preferences.get('hours_per_week', 10)

        weeks = int(np.ceil(total_hours / hours_per_week))

        return weeks

    def adapt_plan_weekly(
        self,
        current_plan: PersonalReskillingPlan,
        progress_data: Dict,
        market_updates: Dict
    ) -> PersonalReskillingPlan:
        """
        Adapt plan based on weekly progress and market changes

        Args:
            current_plan: Existing PRP
            progress_data: Learner's progress this week
            market_updates: Latest market trends

        Returns:
            Updated PRP
        """
        # Check if adaptation needed
        needs_adaptation = self._check_adaptation_triggers(
            current_plan,
            progress_data,
            market_updates
        )

        if not needs_adaptation:
            return current_plan

        # Adjust modules based on progress
        updated_modules = self._adjust_modules(
            current_plan.learning_modules,
            progress_data
        )

        # Re-prioritize based on market
        if self._market_shifted(market_updates):
            updated_modules = self._reprioritize_modules(
                updated_modules,
                market_updates
            )

        # Rebuild schedule
        learning_prefs = {'hours_per_week': progress_data.get('avg_hours_per_week', 10)}
        updated_schedule = self._create_adaptive_schedule(updated_modules, learning_prefs['hours_per_week'])

        # Update completion estimate
        updated_weeks = self._estimate_completion(updated_modules, learning_prefs)

        current_plan.learning_modules = updated_modules
        current_plan.weekly_schedule = updated_schedule
        current_plan.estimated_completion_weeks = updated_weeks
        current_plan.last_updated = datetime.now()

        return current_plan

    def _check_adaptation_triggers(
        self,
        plan: PersonalReskillingPlan,
        progress: Dict,
        market: Dict
    ) -> bool:
        """Check if plan needs adaptation"""
        # Progress below target
        if progress.get('completion_rate', 100) < 70:
            return True

        # Market shift
        if self._market_shifted(market):
            return True

        # Learner struggling
        if progress.get('avg_assessment_score', 100) < 60:
            return True

        return False

    def _market_shifted(self, market_updates: Dict) -> bool:
        """Check if market has significantly shifted"""
        # Simplified - check if any skill demand changed >20%
        demand_changes = market_updates.get('demand_changes', {})

        for skill, change_pct in demand_changes.items():
            if abs(change_pct) > 20:
                return True

        return False

    def _adjust_modules(self, modules: List[Dict], progress: Dict) -> List[Dict]:
        """Adjust modules based on learner progress"""
        adjusted = []

        completed_modules = progress.get('completed_modules', [])

        for module in modules:
            if module['module_id'] in completed_modules:
                continue  # Skip completed modules

            # Adjust difficulty if learner struggling
            if progress.get('struggling_with', '') == module['skill_target']:
                # Add more beginner lessons
                module['lessons'] = self._add_remedial_lessons(module)

            adjusted.append(module)

        return adjusted

    def _add_remedial_lessons(self, module: Dict) -> List[Dict]:
        """Add additional beginner lessons for struggling learners"""
        current_lessons = module['lessons']

        # Add 5 more beginner lessons at start
        remedial = []
        for i in range(5):
            remedial.append({
                'lesson_id': f"{module['skill_target']}_remedial_{i+1}",
                'title': f"{module['skill_target']} Fundamentals - Extra {i+1}",
                'duration_minutes': 5,
                'difficulty': 'beginner',
                'topics': ['Review', 'Practice', 'Examples'],
                'practice_exercises': [],
                'estimated_mastery_gain': 2.0
            })

        return remedial + current_lessons

    def _reprioritize_modules(self, modules: List[Dict], market: Dict) -> List[Dict]:
        """Re-prioritize modules based on market changes"""
        demand = market.get('skills_demand', {})

        # Re-score each module
        for module in modules:
            skill = module['skill_target']
            module['market_score'] = demand.get(skill, 50)

        # Sort by market score
        return sorted(modules, key=lambda x: x.get('market_score', 50), reverse=True)

    def _generate_python_lessons(self) -> List[MicroLesson]:
        """Generate Python micro-lessons"""
        return []  # Placeholder

    def _generate_ml_lessons(self) -> List[MicroLesson]:
        """Generate ML micro-lessons"""
        return []  # Placeholder

    def _generate_data_lessons(self) -> List[MicroLesson]:
        """Generate data analysis micro-lessons"""
        return []  # Placeholder

    def _generate_cloud_lessons(self) -> List[MicroLesson]:
        """Generate cloud computing micro-lessons"""
        return []  # Placeholder

    def get_todays_lesson(self, plan: PersonalReskillingPlan, day_of_week: int) -> Dict:
        """Get today's micro-lessons (5-minute units)"""
        current_week = self._get_current_week(plan)

        if current_week >= len(plan.weekly_schedule):
            return {'message': 'Plan completed! Time to apply for jobs.'}

        week_plan = plan.weekly_schedule[current_week]

        # Get lessons for today
        lessons_per_day = 3  # 3x 5-minute lessons per day

        return {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'week': current_week + 1,
            'lessons': self._get_daily_lessons(week_plan, day_of_week, lessons_per_day),
            'total_time_minutes': lessons_per_day * 5,
            'progress_update': f"{current_week + 1} / {len(plan.weekly_schedule)} weeks completed"
        }

    def _get_current_week(self, plan: PersonalReskillingPlan) -> int:
        """Calculate current week of plan"""
        days_since_start = (datetime.now() - plan.last_updated).days
        return min(days_since_start // 7, len(plan.weekly_schedule) - 1)

    def _get_daily_lessons(self, week_plan: Dict, day: int, count: int) -> List[Dict]:
        """Get specific lessons for day"""
        all_modules = week_plan['modules']

        lessons = []
        for module in all_modules:
            # Get first few lessons from module
            module_lessons = module.get('lessons', [])
            lessons.extend(module_lessons[:count])

        return lessons[:count]
