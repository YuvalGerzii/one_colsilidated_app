"""
Comprehensive Logging Configuration

Provides structured logging with performance metrics and error tracking.
"""

import logging
import sys
import json
from datetime import datetime
from typing import Any, Dict, Optional
from functools import wraps
import time
import traceback


class JSONFormatter(logging.Formatter):
    """Format logs as JSON for better parsing and analysis"""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": traceback.format_exception(*record.exc_info)
            }

        # Add extra fields
        if hasattr(record, "extra_data"):
            log_data.update(record.extra_data)

        return json.dumps(log_data)


class PerformanceLogger:
    """Logger for performance metrics"""

    def __init__(self, logger_name: str = "performance"):
        self.logger = logging.getLogger(logger_name)

    def log_query(self, query: str, duration_ms: float, rows: int = 0):
        """Log database query performance"""
        self.logger.info(
            "Database Query",
            extra={
                "extra_data": {
                    "type": "db_query",
                    "query": query[:200],  # Limit query length
                    "duration_ms": round(duration_ms, 2),
                    "rows": rows,
                    "slow": duration_ms > 100  # Flag slow queries
                }
            }
        )

    def log_api_call(
        self,
        endpoint: str,
        method: str,
        duration_ms: float,
        status_code: int,
        user_id: Optional[str] = None
    ):
        """Log API call performance"""
        self.logger.info(
            "API Call",
            extra={
                "extra_data": {
                    "type": "api_call",
                    "endpoint": endpoint,
                    "method": method,
                    "duration_ms": round(duration_ms, 2),
                    "status_code": status_code,
                    "user_id": user_id,
                    "slow": duration_ms > 500  # Flag slow API calls
                }
            }
        )

    def log_cache_operation(
        self,
        operation: str,
        key: str,
        hit: bool = False,
        duration_ms: float = 0
    ):
        """Log cache operations"""
        self.logger.debug(
            "Cache Operation",
            extra={
                "extra_data": {
                    "type": "cache",
                    "operation": operation,
                    "key": key,
                    "hit": hit,
                    "duration_ms": round(duration_ms, 2)
                }
            }
        )


def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    json_format: bool = False
):
    """
    Setup application logging

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for log output
        json_format: Use JSON formatting for logs
    """
    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))

    # Remove existing handlers
    root_logger.handlers = []

    # Create formatter
    if json_format:
        formatter = JSONFormatter()
    else:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handler (if specified)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    # Create specialized loggers
    performance_logger = logging.getLogger("performance")
    error_logger = logging.getLogger("errors")
    security_logger = logging.getLogger("security")

    return root_logger


def log_execution_time(logger: Optional[logging.Logger] = None):
    """
    Decorator to log function execution time

    Usage:
        @log_execution_time()
        def my_function():
            ...
    """
    if logger is None:
        logger = logging.getLogger("performance")

    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                duration_ms = (time.time() - start_time) * 1000

                logger.info(
                    f"Function executed: {func.__name__}",
                    extra={
                        "extra_data": {
                            "function": func.__name__,
                            "duration_ms": round(duration_ms, 2),
                            "success": True
                        }
                    }
                )

                return result
            except Exception as e:
                duration_ms = (time.time() - start_time) * 1000
                logger.error(
                    f"Function failed: {func.__name__}",
                    extra={
                        "extra_data": {
                            "function": func.__name__,
                            "duration_ms": round(duration_ms, 2),
                            "success": False,
                            "error": str(e)
                        }
                    },
                    exc_info=True
                )
                raise

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration_ms = (time.time() - start_time) * 1000

                logger.info(
                    f"Function executed: {func.__name__}",
                    extra={
                        "extra_data": {
                            "function": func.__name__,
                            "duration_ms": round(duration_ms, 2),
                            "success": True
                        }
                    }
                )

                return result
            except Exception as e:
                duration_ms = (time.time() - start_time) * 1000
                logger.error(
                    f"Function failed: {func.__name__}",
                    extra={
                        "extra_data": {
                            "function": func.__name__,
                            "duration_ms": round(duration_ms, 2),
                            "success": False,
                            "error": str(e)
                        }
                    },
                    exc_info=True
                )
                raise

        # Check if function is async
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


class ErrorTracker:
    """Track and report errors"""

    def __init__(self):
        self.logger = logging.getLogger("errors")
        self.error_counts = {}

    def log_error(
        self,
        error: Exception,
        context: Optional[Dict[str, Any]] = None,
        severity: str = "ERROR"
    ):
        """Log an error with context"""
        error_type = type(error).__name__
        error_msg = str(error)

        # Track error count
        if error_type not in self.error_counts:
            self.error_counts[error_type] = 0
        self.error_counts[error_type] += 1

        self.logger.log(
            getattr(logging, severity),
            f"{error_type}: {error_msg}",
            extra={
                "extra_data": {
                    "error_type": error_type,
                    "error_message": error_msg,
                    "error_count": self.error_counts[error_type],
                    "context": context or {},
                    "traceback": traceback.format_exc()
                }
            }
        )

    def get_error_stats(self) -> Dict[str, int]:
        """Get error statistics"""
        return self.error_counts.copy()


# Global instances
_performance_logger = PerformanceLogger()
_error_tracker = ErrorTracker()


def get_performance_logger() -> PerformanceLogger:
    """Get the global performance logger"""
    return _performance_logger


def get_error_tracker() -> ErrorTracker:
    """Get the global error tracker"""
    return _error_tracker


# Setup default logging
setup_logging(log_level="INFO", json_format=False)
