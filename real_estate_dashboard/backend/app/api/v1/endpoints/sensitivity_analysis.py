"""
Sensitivity Analysis API Endpoints

Provides REST API for sensitivity analysis calculations.
All calculations are performed server-side using FREE algorithms - no external API keys required.
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.services.sensitivity_analysis_service import (
    SensitivityAnalysisService,
    calculate_cash_on_cash_return,
    calculate_cap_rate,
    calculate_dscr,
    calculate_irr_simple
)

router = APIRouter()
sensitivity_service = SensitivityAnalysisService()


# ========================================
# REQUEST/RESPONSE MODELS
# ========================================

class Variable(BaseModel):
    """Variable definition for sensitivity analysis"""
    name: str
    label: str
    base_value: float
    min: float
    max: float
    unit: Optional[str] = ""


class ScenarioAdjustment(BaseModel):
    """Adjustment for a scenario"""
    variable: str
    value: Optional[float] = None
    multiply_by: Optional[float] = None
    add: Optional[float] = None


class Scenario(BaseModel):
    """Scenario definition"""
    name: str
    description: str
    adjustments: Dict[str, Any]


class SensitivityRequest(BaseModel):
    """Request for sensitivity analysis"""
    base_inputs: Dict[str, float]
    variables: List[Variable]
    metric_type: str = Field(..., description="Type of metric: cash_on_cash, cap_rate, dscr, irr, or custom")
    metric_name: str = "Output"


class MonteCarloRequest(BaseModel):
    """Request for Monte Carlo simulation"""
    base_inputs: Dict[str, float]
    variables: List[Variable]
    metric_type: str
    iterations: int = Field(10000, ge=1000, le=100000)
    distribution: str = Field("normal", description="normal, uniform, or triangular")


class ScenarioAnalysisRequest(BaseModel):
    """Request for scenario analysis"""
    base_inputs: Dict[str, float]
    metric_type: str
    scenarios: List[Scenario]


class BreakEvenRequest(BaseModel):
    """Request for break-even analysis"""
    base_inputs: Dict[str, float]
    variables: List[Variable]
    metric_type: str
    target_metric: float = 0


class TwoWaySensitivityRequest(BaseModel):
    """Request for two-way sensitivity (heat map)"""
    base_inputs: Dict[str, float]
    metric_type: str
    x_variable: Variable
    y_variable: Variable
    steps: int = Field(7, ge=3, le=15)


# ========================================
# HELPER FUNCTIONS
# ========================================

def get_calculator_function(metric_type: str):
    """Get the appropriate calculator function based on metric type"""
    calculators = {
        "cash_on_cash": calculate_cash_on_cash_return,
        "cap_rate": calculate_cap_rate,
        "dscr": calculate_dscr,
        "irr": calculate_irr_simple
    }

    if metric_type not in calculators:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid metric_type. Must be one of: {', '.join(calculators.keys())}"
        )

    return calculators[metric_type]


# ========================================
# ENDPOINTS
# ========================================

@router.post("/one-way")
async def calculate_one_way_sensitivity(request: SensitivityRequest):
    """
    Perform one-way sensitivity analysis (tornado chart)

    **Analyzes how changing each variable individually affects the output metric.**

    Returns results sorted by impact (most sensitive variables first).

    **FREE - No API keys required. All calculations done locally.**
    """
    try:
        calculate_metric = get_calculator_function(request.metric_type)

        # Convert Pydantic models to dicts
        variables_dict = [var.dict() for var in request.variables]

        result = sensitivity_service.one_way_sensitivity(
            base_inputs=request.base_inputs,
            calculate_metric=calculate_metric,
            variables=variables_dict,
            metric_name=request.metric_name
        )

        return {
            "success": True,
            "data": result,
            "metric_type": request.metric_type
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Sensitivity analysis failed: {str(e)}"
        )


@router.post("/two-way")
async def calculate_two_way_sensitivity(request: TwoWaySensitivityRequest):
    """
    Perform two-way sensitivity analysis (heat map)

    **Analyzes how changing two variables simultaneously affects the output.**

    Creates a grid showing all combinations of the two variables.

    **FREE - No API keys required. All calculations done locally.**
    """
    try:
        calculate_metric = get_calculator_function(request.metric_type)

        result = sensitivity_service.two_way_sensitivity(
            base_inputs=request.base_inputs,
            calculate_metric=calculate_metric,
            x_variable=request.x_variable.dict(),
            y_variable=request.y_variable.dict(),
            steps=request.steps
        )

        return {
            "success": True,
            "data": result,
            "metric_type": request.metric_type
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Two-way sensitivity analysis failed: {str(e)}"
        )


@router.post("/monte-carlo")
async def run_monte_carlo_simulation(request: MonteCarloRequest):
    """
    Run Monte Carlo simulation

    **Runs thousands of simulations with random variations to understand probability distribution.**

    Provides statistics, percentiles, histogram data, and risk metrics.

    **FREE - No API keys required. Uses local random number generation.**
    """
    try:
        calculate_metric = get_calculator_function(request.metric_type)

        variables_dict = [var.dict() for var in request.variables]

        result = sensitivity_service.monte_carlo_simulation(
            base_inputs=request.base_inputs,
            calculate_metric=calculate_metric,
            variables=variables_dict,
            iterations=request.iterations,
            distribution=request.distribution
        )

        return {
            "success": True,
            "data": result,
            "metric_type": request.metric_type
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Monte Carlo simulation failed: {str(e)}"
        )


@router.post("/scenarios")
async def analyze_scenarios(request: ScenarioAnalysisRequest):
    """
    Analyze predefined scenarios

    **Compare multiple scenarios (e.g., Base Case, Optimistic, Pessimistic).**

    Shows how the metric changes under different sets of assumptions.

    **FREE - No API keys required. All calculations done locally.**
    """
    try:
        calculate_metric = get_calculator_function(request.metric_type)

        scenarios_dict = [scenario.dict() for scenario in request.scenarios]

        result = sensitivity_service.scenario_analysis(
            base_inputs=request.base_inputs,
            calculate_metric=calculate_metric,
            scenarios=scenarios_dict
        )

        return {
            "success": True,
            "data": result,
            "metric_type": request.metric_type
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Scenario analysis failed: {str(e)}"
        )


@router.post("/break-even")
async def calculate_break_even(request: BreakEvenRequest):
    """
    Calculate break-even values

    **Finds the exact value each variable needs to hit the target metric.**

    Shows which variables are easiest to adjust to reach your goal.

    **FREE - No API keys required. Uses binary search algorithm.**
    """
    try:
        calculate_metric = get_calculator_function(request.metric_type)

        variables_dict = [var.dict() for var in request.variables]

        result = sensitivity_service.break_even_analysis(
            base_inputs=request.base_inputs,
            calculate_metric=calculate_metric,
            variables=variables_dict,
            target_metric=request.target_metric
        )

        return {
            "success": True,
            "data": result,
            "metric_type": request.metric_type
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Break-even analysis failed: {str(e)}"
        )


@router.get("/templates/{property_type}")
async def get_sensitivity_template(property_type: str):
    """
    Get pre-configured sensitivity analysis template for common property types

    **Provides ready-to-use variable configurations for different property types.**

    Available templates:
    - multifamily
    - single_family
    - commercial
    - fix_and_flip

    **FREE - No API keys required.**
    """
    templates = {
        "multifamily": {
            "variables": [
                {
                    "name": "rental_income",
                    "label": "Annual Rental Income",
                    "base_value": 120000,
                    "min": 90000,
                    "max": 150000,
                    "unit": "$"
                },
                {
                    "name": "vacancy_rate",
                    "label": "Vacancy Rate",
                    "base_value": 5,
                    "min": 2,
                    "max": 15,
                    "unit": "%"
                },
                {
                    "name": "operating_expenses",
                    "label": "Annual Operating Expenses",
                    "base_value": 40000,
                    "min": 30000,
                    "max": 55000,
                    "unit": "$"
                },
                {
                    "name": "property_value",
                    "label": "Property Value",
                    "base_value": 1000000,
                    "min": 800000,
                    "max": 1200000,
                    "unit": "$"
                },
                {
                    "name": "appreciation_rate",
                    "label": "Annual Appreciation",
                    "base_value": 3,
                    "min": 0,
                    "max": 8,
                    "unit": "%"
                }
            ],
            "scenarios": [
                {
                    "name": "Optimistic",
                    "description": "Strong market conditions",
                    "adjustments": {
                        "rental_income": {"multiply_by": 1.15},
                        "vacancy_rate": {"multiply_by": 0.5},
                        "appreciation_rate": {"multiply_by": 1.5}
                    }
                },
                {
                    "name": "Pessimistic",
                    "description": "Market downturn",
                    "adjustments": {
                        "rental_income": {"multiply_by": 0.85},
                        "vacancy_rate": {"multiply_by": 2.0},
                        "appreciation_rate": {"multiply_by": 0.3},
                        "operating_expenses": {"multiply_by": 1.2}
                    }
                },
                {
                    "name": "Recession",
                    "description": "Economic recession scenario",
                    "adjustments": {
                        "rental_income": {"multiply_by": 0.75},
                        "vacancy_rate": {"value": 20},
                        "appreciation_rate": {"value": -2},
                        "operating_expenses": {"multiply_by": 1.15}
                    }
                }
            ]
        },
        "single_family": {
            "variables": [
                {
                    "name": "monthly_rent",
                    "label": "Monthly Rent",
                    "base_value": 2500,
                    "min": 2000,
                    "max": 3500,
                    "unit": "$"
                },
                {
                    "name": "purchase_price",
                    "label": "Purchase Price",
                    "base_value": 400000,
                    "min": 350000,
                    "max": 500000,
                    "unit": "$"
                },
                {
                    "name": "down_payment_pct",
                    "label": "Down Payment %",
                    "base_value": 20,
                    "min": 10,
                    "max": 30,
                    "unit": "%"
                },
                {
                    "name": "interest_rate",
                    "label": "Interest Rate",
                    "base_value": 6.5,
                    "min": 4.5,
                    "max": 9.0,
                    "unit": "%"
                },
                {
                    "name": "annual_expenses",
                    "label": "Annual Expenses",
                    "base_value": 8000,
                    "min": 6000,
                    "max": 12000,
                    "unit": "$"
                }
            ]
        },
        "commercial": {
            "variables": [
                {
                    "name": "noi",
                    "label": "Net Operating Income",
                    "base_value": 150000,
                    "min": 100000,
                    "max": 200000,
                    "unit": "$"
                },
                {
                    "name": "cap_rate",
                    "label": "Cap Rate",
                    "base_value": 7.5,
                    "min": 5.0,
                    "max": 10.0,
                    "unit": "%"
                },
                {
                    "name": "tenant_improvement",
                    "label": "Tenant Improvement Costs",
                    "base_value": 50000,
                    "min": 30000,
                    "max": 80000,
                    "unit": "$"
                },
                {
                    "name": "lease_term_years",
                    "label": "Average Lease Term",
                    "base_value": 5,
                    "min": 3,
                    "max": 10,
                    "unit": "years"
                }
            ]
        },
        "fix_and_flip": {
            "variables": [
                {
                    "name": "purchase_price",
                    "label": "Purchase Price",
                    "base_value": 300000,
                    "min": 250000,
                    "max": 350000,
                    "unit": "$"
                },
                {
                    "name": "renovation_cost",
                    "label": "Renovation Cost",
                    "base_value": 75000,
                    "min": 50000,
                    "max": 125000,
                    "unit": "$"
                },
                {
                    "name": "arv",
                    "label": "After Repair Value (ARV)",
                    "base_value": 450000,
                    "min": 400000,
                    "max": 525000,
                    "unit": "$"
                },
                {
                    "name": "holding_months",
                    "label": "Holding Period (Months)",
                    "base_value": 6,
                    "min": 3,
                    "max": 12,
                    "unit": "months"
                },
                {
                    "name": "monthly_costs",
                    "label": "Monthly Holding Costs",
                    "base_value": 3000,
                    "min": 2000,
                    "max": 5000,
                    "unit": "$"
                }
            ]
        }
    }

    if property_type not in templates:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template not found. Available types: {', '.join(templates.keys())}"
        )

    return {
        "success": True,
        "property_type": property_type,
        "template": templates[property_type]
    }
