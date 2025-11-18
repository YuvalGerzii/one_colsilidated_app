"""
Observability and monitoring for multi-agent systems.

Implements best practices from 2025 research:
- Distributed tracing
- Centralized logging
- Metrics collection
- Performance monitoring
"""

import time
from typing import Any, Dict, List, Optional, Callable
from datetime import datetime, timedelta
from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum
from loguru import logger


class EventType(Enum):
    """Types of monitoring events."""
    TASK_START = "task_start"
    TASK_COMPLETE = "task_complete"
    TASK_FAIL = "task_fail"
    MESSAGE_SENT = "message_sent"
    MESSAGE_RECEIVED = "message_received"
    AGENT_START = "agent_start"
    AGENT_STOP = "agent_stop"
    LEARNING_UPDATE = "learning_update"
    ERROR = "error"
    CUSTOM = "custom"


@dataclass
class TraceEvent:
    """A single trace event."""
    trace_id: str
    span_id: str
    parent_span_id: Optional[str]
    event_type: EventType
    agent_id: str
    timestamp: datetime
    duration_ms: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    success: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "parent_span_id": self.parent_span_id,
            "event_type": self.event_type.value,
            "agent_id": self.agent_id,
            "timestamp": self.timestamp.isoformat(),
            "duration_ms": self.duration_ms,
            "metadata": self.metadata,
            "success": self.success,
        }


class SystemMonitor:
    """
    Comprehensive monitoring for multi-agent systems.

    Features:
    - Distributed tracing across agents
    - Real-time metrics collection
    - Performance analytics
    - Anomaly detection
    """

    def __init__(self, retention_hours: int = 24):
        """
        Initialize system monitor.

        Args:
            retention_hours: How long to retain events
        """
        self.retention_hours = retention_hours

        # Distributed tracing
        self.traces: Dict[str, List[TraceEvent]] = defaultdict(list)
        self.active_spans: Dict[str, float] = {}  # span_id -> start_time

        # Metrics
        self.metrics: Dict[str, deque] = defaultdict(lambda: deque(maxlen=10000))

        # Agent performance
        self.agent_metrics: Dict[str, Dict[str, Any]] = defaultdict(
            lambda: {
                "task_count": 0,
                "success_count": 0,
                "fail_count": 0,
                "total_duration": 0.0,
                "average_duration": 0.0,
                "last_active": None,
            }
        )

        # System health
        self.health_checks: List[Callable[[], bool]] = []

        # Alerts
        self.alert_thresholds = {
            "error_rate": 0.1,  # 10% error rate
            "avg_duration_ms": 10000,  # 10 seconds
            "queue_size": 1000,
        }
        self.alerts: List[Dict[str, Any]] = []

        logger.info("SystemMonitor initialized")

    def start_span(
        self,
        trace_id: str,
        span_id: str,
        parent_span_id: Optional[str],
        agent_id: str,
        event_type: EventType,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Start a new trace span.

        Args:
            trace_id: Unique trace identifier
            span_id: Unique span identifier
            parent_span_id: Parent span ID for nested operations
            agent_id: ID of the agent
            event_type: Type of event
            metadata: Additional metadata
        """
        self.active_spans[span_id] = time.time()

        event = TraceEvent(
            trace_id=trace_id,
            span_id=span_id,
            parent_span_id=parent_span_id,
            event_type=event_type,
            agent_id=agent_id,
            timestamp=datetime.now(),
            metadata=metadata or {},
        )

        self.traces[trace_id].append(event)

        logger.debug(f"Started span: {span_id} ({event_type.value})")

    def end_span(
        self,
        span_id: str,
        success: bool = True,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        End a trace span.

        Args:
            span_id: Span identifier
            success: Whether operation succeeded
            metadata: Additional metadata
        """
        if span_id not in self.active_spans:
            logger.warning(f"Unknown span: {span_id}")
            return

        start_time = self.active_spans.pop(span_id)
        duration_ms = (time.time() - start_time) * 1000

        # Find and update the event
        for trace_events in self.traces.values():
            for event in trace_events:
                if event.span_id == span_id:
                    event.duration_ms = duration_ms
                    event.success = success
                    if metadata:
                        event.metadata.update(metadata)

                    # Update agent metrics
                    self._update_agent_metrics(
                        event.agent_id, duration_ms, success
                    )

                    logger.debug(
                        f"Ended span: {span_id} "
                        f"(duration={duration_ms:.2f}ms, success={success})"
                    )
                    return

    def record_metric(self, name: str, value: float, tags: Optional[Dict[str, str]] = None) -> None:
        """
        Record a metric value.

        Args:
            name: Metric name
            value: Metric value
            tags: Optional tags for grouping
        """
        metric_entry = {
            "timestamp": datetime.now(),
            "value": value,
            "tags": tags or {},
        }

        self.metrics[name].append(metric_entry)

    def get_trace(self, trace_id: str) -> List[TraceEvent]:
        """
        Get all events for a trace.

        Args:
            trace_id: Trace identifier

        Returns:
            List of trace events
        """
        return self.traces.get(trace_id, [])

    def get_agent_metrics(self, agent_id: str) -> Dict[str, Any]:
        """
        Get performance metrics for an agent.

        Args:
            agent_id: Agent identifier

        Returns:
            Metrics dictionary
        """
        return self.agent_metrics.get(agent_id, {})

    def get_system_metrics(self) -> Dict[str, Any]:
        """Get overall system metrics."""
        total_tasks = sum(
            m["task_count"] for m in self.agent_metrics.values()
        )
        total_success = sum(
            m["success_count"] for m in self.agent_metrics.values()
        )
        total_fail = sum(
            m["fail_count"] for m in self.agent_metrics.values()
        )

        success_rate = total_success / total_tasks if total_tasks > 0 else 0.0

        # Calculate average duration across all agents
        total_duration = sum(
            m["total_duration"] for m in self.agent_metrics.values()
        )
        avg_duration = total_duration / total_tasks if total_tasks > 0 else 0.0

        return {
            "total_tasks": total_tasks,
            "success_count": total_success,
            "fail_count": total_fail,
            "success_rate": success_rate,
            "average_duration_ms": avg_duration,
            "active_agents": len(self.agent_metrics),
            "active_traces": len(self.traces),
            "active_spans": len(self.active_spans),
        }

    def get_metric_stats(
        self, metric_name: str, window_minutes: int = 60
    ) -> Dict[str, float]:
        """
        Get statistics for a metric.

        Args:
            metric_name: Name of the metric
            window_minutes: Time window in minutes

        Returns:
            Statistics dictionary
        """
        if metric_name not in self.metrics:
            return {}

        cutoff = datetime.now() - timedelta(minutes=window_minutes)
        recent_values = [
            entry["value"]
            for entry in self.metrics[metric_name]
            if entry["timestamp"] >= cutoff
        ]

        if not recent_values:
            return {}

        import numpy as np

        return {
            "count": len(recent_values),
            "mean": float(np.mean(recent_values)),
            "median": float(np.median(recent_values)),
            "std": float(np.std(recent_values)),
            "min": float(np.min(recent_values)),
            "max": float(np.max(recent_values)),
            "p95": float(np.percentile(recent_values, 95)),
            "p99": float(np.percentile(recent_values, 99)),
        }

    def check_health(self) -> bool:
        """
        Run health checks.

        Returns:
            True if system is healthy
        """
        for check in self.health_checks:
            try:
                if not check():
                    return False
            except Exception as e:
                logger.error(f"Health check failed: {e}")
                return False

        # Check for anomalies
        metrics = self.get_system_metrics()

        # Check error rate
        if metrics["success_rate"] < (1.0 - self.alert_thresholds["error_rate"]):
            self._create_alert(
                "high_error_rate",
                f"Error rate: {1.0 - metrics['success_rate']:.2%}",
            )

        # Check average duration
        if metrics["average_duration_ms"] > self.alert_thresholds["avg_duration_ms"]:
            self._create_alert(
                "high_latency",
                f"Avg duration: {metrics['average_duration_ms']:.2f}ms",
            )

        return True

    def _update_agent_metrics(
        self, agent_id: str, duration_ms: float, success: bool
    ) -> None:
        """Update metrics for an agent."""
        metrics = self.agent_metrics[agent_id]

        metrics["task_count"] += 1
        if success:
            metrics["success_count"] += 1
        else:
            metrics["fail_count"] += 1

        metrics["total_duration"] += duration_ms
        metrics["average_duration"] = (
            metrics["total_duration"] / metrics["task_count"]
        )
        metrics["last_active"] = datetime.now()

    def _create_alert(self, alert_type: str, message: str) -> None:
        """Create an alert."""
        alert = {
            "type": alert_type,
            "message": message,
            "timestamp": datetime.now(),
        }
        self.alerts.append(alert)
        logger.warning(f"ALERT: {alert_type} - {message}")

    def cleanup_old_data(self) -> int:
        """
        Clean up old monitoring data.

        Returns:
            Number of items removed
        """
        cutoff = datetime.now() - timedelta(hours=self.retention_hours)
        removed = 0

        # Clean traces
        for trace_id in list(self.traces.keys()):
            events = self.traces[trace_id]
            before = len(events)
            events[:] = [e for e in events if e.timestamp >= cutoff]
            removed += before - len(events)

            if not events:
                del self.traces[trace_id]

        # Clean metrics
        for metric_name in self.metrics:
            entries = self.metrics[metric_name]
            before = len(entries)
            # deque doesn't support list comprehension assignment
            while entries and entries[0]["timestamp"] < cutoff:
                entries.popleft()
                removed += 1

        if removed > 0:
            logger.debug(f"Cleaned up {removed} old monitoring entries")

        return removed

    def export_traces(self, trace_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Export traces for external analysis.

        Args:
            trace_id: Specific trace to export, or None for all

        Returns:
            List of trace events as dictionaries
        """
        if trace_id:
            return [event.to_dict() for event in self.get_trace(trace_id)]

        all_traces = []
        for events in self.traces.values():
            all_traces.extend([event.to_dict() for event in events])

        return all_traces

    def get_performance_report(self) -> str:
        """
        Generate a performance report.

        Returns:
            Formatted report string
        """
        metrics = self.get_system_metrics()

        report = ["=" * 60]
        report.append("MULTI-AGENT SYSTEM PERFORMANCE REPORT")
        report.append("=" * 60)
        report.append(f"Total Tasks: {metrics['total_tasks']}")
        report.append(f"Success Rate: {metrics['success_rate']:.2%}")
        report.append(f"Average Duration: {metrics['average_duration_ms']:.2f}ms")
        report.append(f"Active Agents: {metrics['active_agents']}")
        report.append(f"Active Traces: {metrics['active_traces']}")
        report.append("")
        report.append("Top Performing Agents:")

        # Sort agents by performance
        sorted_agents = sorted(
            self.agent_metrics.items(),
            key=lambda x: x[1]["success_count"],
            reverse=True,
        )

        for agent_id, agent_metrics in sorted_agents[:5]:
            success_rate = (
                agent_metrics["success_count"] / agent_metrics["task_count"]
                if agent_metrics["task_count"] > 0
                else 0.0
            )
            report.append(
                f"  {agent_id}: {agent_metrics['task_count']} tasks, "
                f"{success_rate:.2%} success, "
                f"{agent_metrics['average_duration']:.2f}ms avg"
            )

        report.append("=" * 60)

        return "\n".join(report)
