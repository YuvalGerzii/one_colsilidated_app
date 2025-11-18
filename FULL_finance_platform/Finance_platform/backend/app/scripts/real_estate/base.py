"""Shared helpers for interactive real estate CLI tools."""

from __future__ import annotations

from contextlib import contextmanager
from decimal import Decimal
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from rich.console import Console
from rich.prompt import Confirm, FloatPrompt, IntPrompt, Prompt
from rich.table import Table

from app.core.database import Base, SessionLocal, engine


console = Console()


def ensure_database() -> None:
    """Ensure the real estate tables exist before persisting data."""

    from app.models import real_estate  # noqa: F401 - import registers models with metadata

    Base.metadata.create_all(bind=engine)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""

    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def prompt_text(message: str, default: Optional[str] = None, allow_blank: bool = False) -> str:
    """Prompt for textual input with validation."""

    while True:
        response = Prompt.ask(message, default=default).strip()
        if response or allow_blank:
            return response
        console.print("[red]A value is required.[/red]")


def prompt_choice(message: str, choices: Iterable[str], default: Optional[str] = None) -> str:
    """Prompt the user to choose one option from a list."""

    choice_list = list(choices)
    choice_str = ", ".join(choice_list)
    while True:
        response = Prompt.ask(f"{message} ([{choice_str}])", default=default)
        if response in choice_list:
            return response
        console.print(f"[red]Please choose one of: {choice_str}[/red]")


def prompt_float(
    message: str,
    default: Optional[float] = None,
    minimum: Optional[float] = None,
    maximum: Optional[float] = None,
) -> float:
    """Prompt for a floating point value with optional bounds."""

    while True:
        response = FloatPrompt.ask(message, default=default)
        if minimum is not None and response < minimum:
            console.print(f"[red]Value must be >= {minimum}[/red]")
            continue
        if maximum is not None and response > maximum:
            console.print(f"[red]Value must be <= {maximum}[/red]")
            continue
        return float(response)


def prompt_int(
    message: str,
    default: Optional[int] = None,
    minimum: Optional[int] = None,
    maximum: Optional[int] = None,
) -> int:
    """Prompt for an integer with optional bounds."""

    while True:
        response = IntPrompt.ask(message, default=default)
        if minimum is not None and response < minimum:
            console.print(f"[red]Value must be >= {minimum}[/red]")
            continue
        if maximum is not None and response > maximum:
            console.print(f"[red]Value must be <= {maximum}[/red]")
            continue
        return int(response)


def prompt_percentage(
    message: str,
    default: Optional[float] = None,
    minimum: float = 0.0,
    maximum: float = 1.0,
) -> float:
    """Prompt for a percentage value and return it as a decimal."""

    default_percentage = None if default is None else default * 100
    while True:
        response = FloatPrompt.ask(f"{message} (%)", default=default_percentage)
        decimal_value = float(response) / 100.0
        if decimal_value < minimum:
            console.print(f"[red]Value must be at least {minimum * 100:.2f}%[/red]")
            continue
        if decimal_value > maximum:
            console.print(f"[red]Value must be at most {maximum * 100:.2f}%[/red]")
            continue
        return decimal_value


def confirm(message: str, default: bool = True) -> bool:
    """Prompt the user for a yes/no confirmation."""

    return Confirm.ask(message, default=default)


def format_currency(value: float) -> str:
    """Format a numeric value as USD currency."""

    return f"${value:,.2f}"


def format_percentage(value: float) -> str:
    """Format a decimal as a percentage string."""

    return f"{value * 100:.2f}%"


def render_metrics_table(title: str, metrics: Dict[str, Any]) -> None:
    """Render a name/value table for model outputs."""

    table = Table(title=title, title_style="bold cyan", box=None, show_header=False)
    table.add_column("Metric", style="bold")
    table.add_column("Value", style="green")
    for key, value in metrics.items():
        if isinstance(value, float):
            display = f"{value:,.4f}" if abs(value) < 1 else f"{value:,.2f}"
        else:
            display = str(value)
        table.add_row(key, display)
    console.print(table)


def render_projection_table(title: str, columns: List[str], rows: List[Dict[str, Any]]) -> None:
    """Render a projection table with the provided columns and rows."""

    table = Table(title=title, title_style="bold magenta")
    for column in columns:
        table.add_column(column, justify="right")
    for row in rows:
        table.add_row(*(row.get(column, "") for column in columns))
    console.print(table)


def decimal_default(obj: Any) -> Any:
    """Convert Decimal objects to floats for JSON serialization."""

    if isinstance(obj, Decimal):
        return float(obj)
    return obj


def _slugify(value: str) -> str:
    """Create a filesystem friendly slug from a label."""

    cleaned = "".join(ch if ch.isalnum() else "-" for ch in value.lower())
    return "-".join(filter(None, cleaned.split("-"))) or "report"


def ensure_report_dir(model_slug: str, project_name: str) -> Path:
    """Create (or reuse) a directory for generated charts."""

    base_dir = Path(__file__).resolve().parent / "reports" / model_slug / _slugify(project_name)
    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir


def save_bar_chart(
    output_dir: Path,
    filename: str,
    title: str,
    labels: Sequence[str],
    datasets: Sequence[Dict[str, Sequence[float]]],
    xlabel: str,
    ylabel: str,
) -> Path:
    """Persist a bar chart to disk and return the file path."""

    path = output_dir / filename
    fig, ax = plt.subplots(figsize=(8, 5))
    num_series = max(1, len(datasets))
    bar_width = 0.8 / num_series
    x_positions = range(len(labels))

    palette = [
        "#1f77b4",
        "#ff7f0e",
        "#2ca02c",
        "#d62728",
        "#9467bd",
        "#8c564b",
        "#e377c2",
        "#7f7f7f",
        "#bcbd22",
        "#17becf",
    ]

    for idx, dataset in enumerate(datasets):
        offsets = [x + (idx - (num_series - 1) / 2) * bar_width for x in x_positions]
        color = palette[idx % len(palette)]
        ax.bar(
            offsets,
            dataset.get("data", []),
            width=bar_width,
            label=dataset.get("label"),
            color=color,
        )

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xticks(list(x_positions))
    ax.set_xticklabels(labels, rotation=15, ha="right")
    if any(dataset.get("label") for dataset in datasets):
        ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    return path


def save_line_chart(
    output_dir: Path,
    filename: str,
    title: str,
    x_values: Sequence[float],
    series: Dict[str, Sequence[float]],
    xlabel: str,
    ylabel: str,
) -> Path:
    """Persist a multi-series line chart to disk and return the file path."""

    path = output_dir / filename
    fig, ax = plt.subplots(figsize=(8, 5))
    palette = [
        "#1f77b4",
        "#ff7f0e",
        "#2ca02c",
        "#d62728",
        "#9467bd",
        "#8c564b",
        "#e377c2",
        "#7f7f7f",
        "#bcbd22",
        "#17becf",
    ]

    for idx, (label, values) in enumerate(series.items()):
        color = palette[idx % len(palette)]
        ax.plot(x_values, values, marker="o", label=label, color=color)

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if series:
        ax.legend()
    ax.grid(True, linestyle="--", alpha=0.4)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    return path


def annuity_payment(principal: float, annual_rate: float, years: int, payments_per_year: int = 12) -> float:
    """Calculate the recurring payment for an amortizing loan."""

    if principal <= 0:
        return 0.0
    periodic_rate = annual_rate / payments_per_year
    total_payments = years * payments_per_year
    if periodic_rate == 0:
        return principal / total_payments
    factor = (1 + periodic_rate) ** total_payments
    return principal * periodic_rate * factor / (factor - 1)


def remaining_balance(
    principal: float,
    annual_rate: float,
    years: int,
    payments_made: int,
    payments_per_year: int = 12,
) -> float:
    """Calculate the remaining balance on an amortizing loan."""

    if principal <= 0:
        return 0.0
    payment = annuity_payment(principal, annual_rate, years, payments_per_year)
    periodic_rate = annual_rate / payments_per_year
    total_payments = years * payments_per_year
    if periodic_rate == 0:
        return max(principal - payment * payments_made, 0.0)
    factor = (1 + periodic_rate) ** total_payments
    remaining_factor = (1 + periodic_rate) ** payments_made
    balance = principal * factor - payment * ((remaining_factor - 1) / periodic_rate)
    balance /= factor
    return max(balance, 0.0)
