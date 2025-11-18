"""
Observability and metrics tracking for multi-agent systems.

Provides comprehensive monitoring of:
- Agent performance and efficiency
- Task execution metrics
- Resource utilization
- Quality trends
- System health

Based on best practices: observability is critical for diagnosing root causes.
"""

import asyncio
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from collections import defaultdict, deque
from loguru import logger
import statistics


@dataclass
class TaskExecutionMetrics:
    """Metrics for a single task execution."""
    task_id: str
    agent_id: str
    start_time: datetime
    end_time: datetime
    execution_time: float
    success: bool
    quality_score: float
    complexity_score: float = 0.0
    agents_involved: int = 1
    token_usage: int = 0  # Estimated
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentPerformanceMetrics:
    """Performance metrics for an agent."""
    agent_id: str
    total_tasks: int = 0
    successful_tasks: int = 0
    failed_tasks: int = 0
    total_execution_time: float = 0.0
    average_execution_time: float = 0.0
    average_quality: float = 0.0
    efficiency_score: float = 0.0
    utilization: float = 0.0  # % of time busy
    quality_scores: List[float] = field(default_factory=list)
    last_active: Optional[datetime] = None


class MetricsTracker:
    """
    Tracks and analyzes system-wide metrics.

    Provides insights into:
    - Agent performance trends
    - System efficiency
    - Quality patterns
    - Resource optimization opportunities
    """

    def __init__(
        self,
        history_size: int = 10000,
        aggregation_interval: int = 60  # seconds
    ):
        """
        Initialize the metrics tracker.

        Args:
            history_size: Maximum number of task metrics to keep
            aggregation_interval: Interval for aggregating metrics (seconds)
        """
        self.history_size = history_size
        self.aggregation_interval = aggregation_interval

        # Task execution history
        self.task_metrics: deque = deque(maxlen=history_size)

        # Agent performance
        self.agent_metrics: Dict[str, AgentPerformanceMetrics] = {}

        # System-wide metrics
        self.system_metrics = {
            "total_tasks": 0,
            "successful_tasks": 0,
            "failed_tasks": 0,
            "total_execution_time": 0.0,
            "total_agents": 0,
            "active_agents": 0,
        }

        # Time-series data (for trending)
        self.hourly_metrics: Dict[datetime, Dict[str, Any]] = {}

        # Quality trends
        self.quality_history: deque = deque(maxlen=1000)

        # Alerts
        self.alerts: List[Dict[str, Any]] = []

        logger.info("MetricsTracker initialized")

    def record_task_execution(
        self,
        task_id: str,
        agent_id: str,
        start_time: datetime,
        end_time: datetime,
        success: bool,
        quality_score: float,
        complexity_score: float = 0.0,
        agents_involved: int = 1,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Record metrics for a task execution.

        Args:
            task_id: Task ID
            agent_id: Agent that executed the task
            start_time: Task start time
            end_time: Task end time
            success: Whether task succeeded
            quality_score: Quality score (0-1)
            complexity_score: Task complexity (0-1)
            agents_involved: Number of agents involved
            metadata: Additional metadata
        """
        execution_time = (end_time - start_time).total_seconds()

        # Estimate token usage based on complexity and time
        estimated_tokens = int(complexity_score * 1000 + execution_time * 100)

        task_metric = TaskExecutionMetrics(
            task_id=task_id,
            agent_id=agent_id,
            start_time=start_time,
            end_time=end_time,
            execution_time=execution_time,
            success=success,
            quality_score=quality_score,
            complexity_score=complexity_score,
            agents_involved=agents_involved,
            token_usage=estimated_tokens,
            metadata=metadata or {}
        )

        self.task_metrics.append(task_metric)

        # Update agent metrics
        self._update_agent_metrics(task_metric)

        # Update system metrics
        self._update_system_metrics(task_metric)

        # Record quality trend
        self.quality_history.append({
            "timestamp": end_time,
            "quality_score": quality_score,
            "agent_id": agent_id,
        })

        # Check for alerts
        self._check_alerts(task_metric)

        logger.debug(
            f"Recorded metrics for task {task_id}: "
            f"time={execution_time:.2f}s, quality={quality_score:.2f}, success={success}"
        )

    def _update_agent_metrics(self, task_metric: TaskExecutionMetrics) -> None:
        """Update metrics for an agent."""
        agent_id = task_metric.agent_id

        if agent_id not in self.agent_metrics:
            self.agent_metrics[agent_id] = AgentPerformanceMetrics(agent_id=agent_id)

        metrics = self.agent_metrics[agent_id]

        metrics.total_tasks += 1
        if task_metric.success:
            metrics.successful_tasks += 1
        else:
            metrics.failed_tasks += 1

        metrics.total_execution_time += task_metric.execution_time
        metrics.average_execution_time = (
            metrics.total_execution_time / metrics.total_tasks
        )

        metrics.quality_scores.append(task_metric.quality_score)
        metrics.average_quality = statistics.mean(metrics.quality_scores[-100:])  # Last 100 tasks

        # Calculate efficiency: quality per unit time
        if task_metric.execution_time > 0:
            efficiency = task_metric.quality_score / task_metric.execution_time
            metrics.efficiency_score = (
                metrics.efficiency_score * 0.9 + efficiency * 0.1  # EMA
            )

        metrics.last_active = task_metric.end_time

    def _update_system_metrics(self, task_metric: TaskExecutionMetrics) -> None:
        """Update system-wide metrics."""
        self.system_metrics["total_tasks"] += 1

        if task_metric.success:
            self.system_metrics["successful_tasks"] += 1
        else:
            self.system_metrics["failed_tasks"] += 1

        self.system_metrics["total_execution_time"] += task_metric.execution_time
        self.system_metrics["total_agents"] = len(self.agent_metrics)

        # Count active agents (active in last 5 minutes)
        now = datetime.now()
        active_count = sum(
            1 for m in self.agent_metrics.values()
            if m.last_active and (now - m.last_active).total_seconds() < 300
        )
        self.system_metrics["active_agents"] = active_count

    def _check_alerts(self, task_metric: TaskExecutionMetrics) -> None:
        """Check for alert conditions."""
        # Alert on low quality
        if task_metric.quality_score < 0.5:
            self.alerts.append({
                "timestamp": datetime.now(),
                "severity": "warning",
                "type": "low_quality",
                "message": f"Low quality score ({task_metric.quality_score:.2f}) for task {task_metric.task_id}",
                "agent_id": task_metric.agent_id,
            })

        # Alert on task failure
        if not task_metric.success:
            self.alerts.append({
                "timestamp": datetime.now(),
                "severity": "error",
                "type": "task_failure",
                "message": f"Task {task_metric.task_id} failed",
                "agent_id": task_metric.agent_id,
            })

        # Alert on slow execution
        if task_metric.execution_time > 60.0:  # More than 1 minute
            self.alerts.append({
                "timestamp": datetime.now(),
                "severity": "info",
                "type": "slow_execution",
                "message": f"Slow execution ({task_metric.execution_time:.1f}s) for task {task_metric.task_id}",
                "agent_id": task_metric.agent_id,
            })

        # Keep only recent alerts
        if len(self.alerts) > 1000:
            self.alerts = self.alerts[-1000:]

    def get_agent_metrics(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get metrics for a specific agent."""
        if agent_id not in self.agent_metrics:
            return None

        metrics = self.agent_metrics[agent_id]

        success_rate = (
            metrics.successful_tasks / metrics.total_tasks
            if metrics.total_tasks > 0 else 0
        )

        return {
            "agent_id": agent_id,
            "total_tasks": metrics.total_tasks,
            "successful_tasks": metrics.successful_tasks,
            "failed_tasks": metrics.failed_tasks,
            "success_rate": success_rate,
            "average_execution_time": metrics.average_execution_time,
            "average_quality": metrics.average_quality,
            "efficiency_score": metrics.efficiency_score,
            "last_active": metrics.last_active.isoformat() if metrics.last_active else None,
        }

    def get_system_metrics(self) -> Dict[str, Any]:
        """Get system-wide metrics."""
        success_rate = (
            self.system_metrics["successful_tasks"] / self.system_metrics["total_tasks"]
            if self.system_metrics["total_tasks"] > 0 else 0
        )

        average_quality = (
            statistics.mean([q["quality_score"] for q in self.quality_history])
            if self.quality_history else 0
        )

        return {
            "total_tasks": self.system_metrics["total_tasks"],
            "successful_tasks": self.system_metrics["successful_tasks"],
            "failed_tasks": self.system_metrics["failed_tasks"],
            "success_rate": success_rate,
            "average_quality": average_quality,
            "total_agents": self.system_metrics["total_agents"],
            "active_agents": self.system_metrics["active_agents"],
            "total_execution_time": self.system_metrics["total_execution_time"],
        }

    def get_top_performers(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top performing agents."""
        performers = []

        for agent_id, metrics in self.agent_metrics.items():
            if metrics.total_tasks >= 5:  # Minimum tasks for ranking
                score = (
                    metrics.average_quality * 0.5 +
                    (metrics.successful_tasks / metrics.total_tasks) * 0.3 +
                    metrics.efficiency_score * 0.2
                )

                performers.append({
                    "agent_id": agent_id,
                    "score": score,
                    "total_tasks": metrics.total_tasks,
                    "average_quality": metrics.average_quality,
                    "success_rate": metrics.successful_tasks / metrics.total_tasks,
                })

        performers.sort(key=lambda x: x["score"], reverse=True)

        return performers[:limit]

    def get_quality_trend(self, hours: int = 24) -> Dict[str, Any]:
        """Get quality trend over time."""
        cutoff_time = datetime.now() - timedelta(hours=hours)

        recent_quality = [
            q["quality_score"]
            for q in self.quality_history
            if q["timestamp"] > cutoff_time
        ]

        if not recent_quality:
            return {
                "average": 0,
                "trend": "stable",
                "data_points": 0,
            }

        avg_quality = statistics.mean(recent_quality)

        # Determine trend (compare first half vs second half)
        mid_point = len(recent_quality) // 2
        if mid_point > 0:
            first_half_avg = statistics.mean(recent_quality[:mid_point])
            second_half_avg = statistics.mean(recent_quality[mid_point:])

            if second_half_avg > first_half_avg * 1.05:
                trend = "improving"
            elif second_half_avg < first_half_avg * 0.95:
                trend = "declining"
            else:
                trend = "stable"
        else:
            trend = "insufficient_data"

        return {
            "average": avg_quality,
            "trend": trend,
            "data_points": len(recent_quality),
            "min": min(recent_quality),
            "max": max(recent_quality),
            "std_dev": statistics.stdev(recent_quality) if len(recent_quality) > 1 else 0,
        }

    def get_recent_alerts(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent alerts."""
        return self.alerts[-limit:]

    def get_efficiency_report(self) -> Dict[str, Any]:
        """Generate an efficiency report."""
        if not self.task_metrics:
            return {"error": "No data available"}

        recent_tasks = list(self.task_metrics)[-1000:]  # Last 1000 tasks

        # Calculate metrics
        total_agents_used = sum(t.agents_involved for t in recent_tasks)
        avg_agents_per_task = total_agents_used / len(recent_tasks) if recent_tasks else 0

        # Token usage
        total_tokens = sum(t.token_usage for t in recent_tasks)

        # Complexity vs agents
        complexity_groups = {
            "simple": [],
            "moderate": [],
            "complex": [],
        }

        for task in recent_tasks:
            if task.complexity_score < 0.3:
                complexity_groups["simple"].append(task.agents_involved)
            elif task.complexity_score < 0.6:
                complexity_groups["moderate"].append(task.agents_involved)
            else:
                complexity_groups["complex"].append(task.agents_involved)

        return {
            "total_tasks_analyzed": len(recent_tasks),
            "average_agents_per_task": avg_agents_per_task,
            "estimated_total_tokens": total_tokens,
            "average_tokens_per_task": total_tokens / len(recent_tasks) if recent_tasks else 0,
            "complexity_distribution": {
                category: {
                    "count": len(agents),
                    "avg_agents": statistics.mean(agents) if agents else 0,
                }
                for category, agents in complexity_groups.items()
            },
            "efficiency_score": self._calculate_efficiency_score(recent_tasks),
        }

    def _calculate_efficiency_score(self, tasks: List[TaskExecutionMetrics]) -> float:
        """Calculate overall system efficiency score."""
        if not tasks:
            return 0.0

        # Quality to resource ratio
        total_quality = sum(t.quality_score for t in tasks)
        total_resources = sum(t.agents_involved * t.execution_time for t in tasks)

        if total_resources == 0:
            return 0.0

        efficiency = total_quality / total_resources

        # Normalize to 0-1 range
        return min(1.0, efficiency * 10)  # Rough normalization

    def generate_report(self) -> str:
        """Generate a human-readable metrics report."""
        system_metrics = self.get_system_metrics()
        top_performers = self.get_top_performers(5)
        quality_trend = self.get_quality_trend(24)
        efficiency_report = self.get_efficiency_report()
        recent_alerts = self.get_recent_alerts(10)

        report = []
        report.append("=" * 80)
        report.append("MULTI-AGENT SYSTEM METRICS REPORT")
        report.append("=" * 80)

        # System overview
        report.append("\n📊 SYSTEM OVERVIEW")
        report.append(f"  Total Tasks: {system_metrics['total_tasks']}")
        report.append(f"  Success Rate: {system_metrics['success_rate']:.1%}")
        report.append(f"  Average Quality: {system_metrics['average_quality']:.2f}")
        report.append(f"  Active Agents: {system_metrics['active_agents']}/{system_metrics['total_agents']}")

        # Quality trend
        report.append("\n📈 QUALITY TREND (24 hours)")
        report.append(f"  Average: {quality_trend['average']:.2f}")
        report.append(f"  Trend: {quality_trend['trend']}")
        report.append(f"  Range: {quality_trend['min']:.2f} - {quality_trend['max']:.2f}")

        # Top performers
        report.append("\n🏆 TOP PERFORMING AGENTS")
        for i, agent in enumerate(top_performers, 1):
            report.append(
                f"  {i}. {agent['agent_id']}: "
                f"Score={agent['score']:.2f}, "
                f"Quality={agent['average_quality']:.2f}, "
                f"Success={agent['success_rate']:.1%}"
            )

        # Efficiency
        if "efficiency_score" in efficiency_report:
            report.append("\n⚡ EFFICIENCY METRICS")
            report.append(f"  Efficiency Score: {efficiency_report['efficiency_score']:.2f}")
            report.append(f"  Avg Agents/Task: {efficiency_report['average_agents_per_task']:.1f}")
            report.append(f"  Avg Tokens/Task: {efficiency_report['average_tokens_per_task']:.0f}")

        # Alerts
        if recent_alerts:
            report.append(f"\n⚠️  RECENT ALERTS ({len(recent_alerts)})")
            for alert in recent_alerts[-5:]:
                report.append(f"  [{alert['severity']}] {alert['message']}")

        report.append("\n" + "=" * 80)

        return "\n".join(report)
