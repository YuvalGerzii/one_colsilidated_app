"""
Job Application Strategist Agent
Develops comprehensive job application strategies and tracks application campaigns
"""

from typing import Dict, List, Any
from datetime import datetime, timedelta
from .base_agent import BaseAgent


class JobApplicationStrategistAgent(BaseAgent):
    """AI agent specialized in job application strategy and campaign management"""

    def __init__(self):
        super().__init__(
            agent_id="job_application_strategist",
            agent_type="Application Campaign Manager"
        )
        self.capabilities = [
            "Application strategy",
            "Job board optimization",
            "Application tracking",
            "Follow-up timing",
            "Multi-channel job search",
            "Application conversion optimization"
        ]

    def process_task(self, task: Dict) -> 'AgentResponse':
        """Process a task assigned to this agent"""
        from datetime import datetime
        from .base_agent import AgentResponse

        task_type = task.get('type', 'create_strategy')

        if task_type == 'create_strategy':
            result = self.create_application_strategy(task.get('worker_data', task))
        elif task_type == 'track_campaign':
            result = self.track_application_campaign(task.get('applications', []))
        elif task_type == 'optimize_timing':
            result = self.optimize_application_timing(task.get('target_companies', []))
        else:
            result = self.create_application_strategy(task)

        return AgentResponse(
            agent_id=self.agent_id,
            agent_type=self.agent_type,
            status='success',
            data=result,
            confidence=0.85,
            recommendations=result.get('optimization_tips', []) if isinstance(result, dict) else [],
            next_steps=[],
            timestamp=datetime.now(),
            metadata={'task_type': task_type}
        )

    def analyze(self, data: Dict) -> Dict:
        """Analyze provided data according to agent's specialization"""
        return self.create_application_strategy(data)

    def create_application_strategy(self, worker_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create comprehensive job application strategy

        Returns:
            Multi-channel strategy with daily/weekly action plans
        """
        target_role = worker_data.get("target_role", "")
        experience_level = worker_data.get("experience_level", "mid")
        available_hours_weekly = worker_data.get("available_hours_weekly", 10)
        urgency = worker_data.get("urgency", "moderate")  # low, moderate, high, urgent

        # Calculate application targets
        if urgency == "urgent":
            weekly_apps = 25
            network_hours = 3
        elif urgency == "high":
            weekly_apps = 15
            network_hours = 4
        elif urgency == "moderate":
            weekly_apps = 10
            network_hours = 5
        else:
            weekly_apps = 5
            network_hours = 5

        # Multi-channel strategy
        channels = self._define_channels(target_role, experience_level)

        # Weekly schedule
        schedule = self._create_weekly_schedule(available_hours_weekly, weekly_apps, network_hours)

        # Application quality tiers
        tiers = {
            "tier_1_dream_jobs": {
                "count_per_week": max(2, int(weekly_apps * 0.20)),
                "time_per_app": "60-90 minutes",
                "customization": "Fully customized resume, tailored cover letter, company research",
                "follow_up": "LinkedIn connect with hiring manager, email after 1 week"
            },
            "tier_2_target_companies": {
                "count_per_week": max(5, int(weekly_apps * 0.50)),
                "time_per_app": "30-45 minutes",
                "customization": "Tailored resume, standard cover letter with customization",
                "follow_up": "Email follow-up after 1 week"
            },
            "tier_3_volume_applications": {
                "count_per_week": int(weekly_apps * 0.30),
                "time_per_app": "10-15 minutes",
                "customization": "Standard resume and cover letter",
                "follow_up": "None (volume play)"
            }
        }

        return {
            "strategy_overview": {
                "total_weekly_applications": weekly_apps,
                "total_weekly_hours": available_hours_weekly,
                "networking_hours": network_hours,
                "urgency_level": urgency
            },
            "application_tiers": tiers,
            "channels": channels,
            "weekly_schedule": schedule,
            "success_metrics": {
                "target_response_rate": "15-20%",
                "target_interview_rate": "8-12%",
                "estimated_offers_per_month": max(1, weekly_apps // 20)
            },
            "optimization_tips": self._get_optimization_tips()
        }

    def track_application_campaign(self, applications: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Track and analyze application campaign performance

        Returns:
            Campaign analytics with conversion funnel and recommendations
        """
        total_apps = len(applications)

        # Conversion funnel
        screened = sum(1 for app in applications if app.get("status") in ["screening", "interview", "offer"])
        interviewed = sum(1 for app in applications if app.get("status") in ["interview", "offer"])
        offered = sum(1 for app in applications if app.get("status") == "offer")

        # Calculate rates
        response_rate = (screened / total_apps * 100) if total_apps > 0 else 0
        interview_rate = (interviewed / total_apps * 100) if total_apps > 0 else 0
        offer_rate = (offered / total_apps * 100) if total_apps > 0 else 0

        # Channel performance
        channel_performance = {}
        for app in applications:
            channel = app.get("source", "other")
            if channel not in channel_performance:
                channel_performance[channel] = {"total": 0, "responses": 0}
            channel_performance[channel]["total"] += 1
            if app.get("status") != "applied":
                channel_performance[channel]["responses"] += 1

        # Best performing channels
        best_channels = sorted(
            channel_performance.items(),
            key=lambda x: x[1]["responses"] / max(1, x[1]["total"]),
            reverse=True
        )[:3]

        # Time analysis
        avg_response_time = self._calculate_avg_response_time(applications)

        # Recommendations
        recommendations = self._generate_campaign_recommendations(
            response_rate, interview_rate, channel_performance
        )

        return {
            "campaign_summary": {
                "total_applications": total_apps,
                "response_rate": round(response_rate, 1),
                "interview_rate": round(interview_rate, 1),
                "offer_rate": round(offer_rate, 1)
            },
            "conversion_funnel": {
                "applied": total_apps,
                "screening": screened,
                "interview": interviewed,
                "offer": offered
            },
            "channel_performance": channel_performance,
            "best_channels": [{"channel": ch[0], "response_rate": round(ch[1]["responses"]/max(1,ch[1]["total"])*100, 1)} for ch in best_channels],
            "avg_response_time_days": avg_response_time,
            "recommendations": recommendations,
            "next_actions": self._get_next_campaign_actions(response_rate, interview_rate)
        }

    def optimize_application_timing(self, target_companies: List[str]) -> Dict[str, Any]:
        """
        Optimize application timing for maximum visibility

        Returns:
            Best times to apply with day/time recommendations
        """
        return {
            "best_days": ["Tuesday", "Wednesday", "Thursday"],
            "best_times": "8-10 AM in company's timezone",
            "avoid": {
                "monday_mornings": "Hiring managers catching up on emails",
                "friday_afternoons": "Applications may sit until Monday",
                "weekends": "Lower visibility, processed later"
            },
            "optimal_strategy": "Apply Tuesday-Thursday, 8-10 AM company time",
            "follow_up_timing": {
                "first_follow_up": "7-10 days after application",
                "second_follow_up": "2 weeks after first follow-up",
                "connect_on_linkedin": "Within 24 hours of applying"
            }
        }

    def _define_channels(self, role: str, level: str) -> List[Dict[str, Any]]:
        """Define job search channels"""
        return [
            {
                "channel": "LinkedIn",
                "priority": "high",
                "allocation": "40%",
                "strategy": "Use Easy Apply + direct applications, set job alerts",
                "unique_value": "Networking + visibility to recruiters"
            },
            {
                "channel": "Company Websites",
                "priority": "high",
                "allocation": "30%",
                "strategy": "Apply directly to dream companies",
                "unique_value": "Shows genuine interest, bypass ATS sometimes"
            },
            {
                "channel": "Referrals/Network",
                "priority": "critical",
                "allocation": "20%",
                "strategy": "Request referrals from connections",
                "unique_value": "10x higher success rate"
            },
            {
                "channel": "Job Boards (Indeed, Glassdoor)",
                "priority": "medium",
                "allocation": "10%",
                "strategy": "Volume applications for standard roles",
                "unique_value": "High volume, lower competition for some roles"
            }
        ]

    def _create_weekly_schedule(self, hours: float, apps: int, network_hours: float) -> Dict[str, List[str]]:
        """Create weekly application schedule"""
        return {
            "Monday": ["Research 10 companies (1 hr)", "Prepare applications for dream jobs (1 hr)"],
            "Tuesday": ["Submit 3-4 tier 1 applications (2 hrs)", "Network on LinkedIn (1 hr)"],
            "Wednesday": ["Submit 5-6 tier 2 applications (2 hrs)", "Follow up on applications (30 min)"],
            "Thursday": ["Submit remaining tier 2/3 applications (2 hrs)", "Company research (1 hr)"],
            "Friday": ["Networking coffee chats (2 hrs)", "Track applications & plan next week (30 min)"],
            "Weekend": ["Optional: LinkedIn engagement, skill building"]
        }

    def _get_optimization_tips(self) -> List[str]:
        """Get application optimization tips"""
        return [
            "Apply within 48 hours of posting (3x higher response rate)",
            "Tailor resume keywords to job description (use exact phrases)",
            "Follow companies you're interested in on LinkedIn",
            "Set up job alerts to be first applicant",
            "Quality > Quantity: 10 tailored apps beat 50 generic ones",
            "Track all applications in spreadsheet (company, date, status, follow-up)"
        ]

    def _calculate_avg_response_time(self, applications: List[Dict[str, Any]]) -> float:
        """Calculate average response time"""
        response_times = []
        for app in applications:
            if app.get("response_date") and app.get("application_date"):
                # Simplified - would calculate actual days
                response_times.append(7)  # Default 7 days

        return sum(response_times) / len(response_times) if response_times else 10

    def _generate_campaign_recommendations(self, response_rate: float,
                                          interview_rate: float,
                                          channels: Dict) -> List[str]:
        """Generate campaign optimization recommendations"""
        recs = []

        if response_rate < 10:
            recs.append("Response rate is low (<10%). Focus on tailoring applications more carefully.")

        if interview_rate < 5:
            recs.append("Interview rate is low (<5%). Improve resume and cover letter quality.")

        recs.append("Double down on best-performing channels")
        recs.append("Request more referrals from network (10x better success rate)")

        return recs

    def _get_next_campaign_actions(self, response_rate: float, interview_rate: float) -> List[str]:
        """Get next campaign actions"""
        return [
            "Follow up on applications from 1-2 weeks ago",
            "Reach out to hiring managers on LinkedIn",
            "Request referrals for 3-5 target companies",
            "Optimize resume based on rejections"
        ]
