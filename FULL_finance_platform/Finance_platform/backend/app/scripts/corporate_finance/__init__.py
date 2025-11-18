"""Interactive corporate finance modeling utilities."""

from .dcf_model import DEFAULT_INPUTS as DCF_DEFAULTS, FORM_FIELDS as DCF_FIELDS
from .dcf_model import build_chart_specs as dcf_chart_specs
from .dcf_model import build_projection as dcf_build_projection
from .dcf_model import build_report_tables as dcf_tables
from .dcf_model import compute_valuation as dcf_compute_valuation
from .dcf_model import prepare_inputs as dcf_prepare_inputs

from .lbo_model import DEFAULT_INPUTS as LBO_DEFAULTS, FORM_FIELDS as LBO_FIELDS
from .lbo_model import build_chart_specs as lbo_chart_specs
from .lbo_model import build_projection as lbo_build_projection
from .lbo_model import build_report_tables as lbo_tables
from .lbo_model import compute_valuation as lbo_compute_valuation
from .lbo_model import prepare_inputs as lbo_prepare_inputs

from .comparative_analysis import (
    DEFAULT_INPUTS as COMPARISON_DEFAULTS,
    FORM_FIELDS as COMPARISON_FIELDS,
    build_chart_specs as comparison_chart_specs,
    build_report_tables as comparison_tables,
    run_comparison as comparison_run,
)

__all__ = [
    "DCF_DEFAULTS",
    "DCF_FIELDS",
    "dcf_prepare_inputs",
    "dcf_build_projection",
    "dcf_compute_valuation",
    "dcf_tables",
    "dcf_chart_specs",
    "LBO_DEFAULTS",
    "LBO_FIELDS",
    "lbo_prepare_inputs",
    "lbo_build_projection",
    "lbo_compute_valuation",
    "lbo_tables",
    "lbo_chart_specs",
    "COMPARISON_DEFAULTS",
    "COMPARISON_FIELDS",
    "comparison_run",
    "comparison_tables",
    "comparison_chart_specs",
]
