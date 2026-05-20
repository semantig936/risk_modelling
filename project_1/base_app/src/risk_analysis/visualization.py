"""Plotting helpers for risk analysis results."""

import os
from pathlib import Path

matplotlib_cache = Path(".cache/matplotlib").resolve()
matplotlib_cache.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(matplotlib_cache))
os.environ.setdefault("XDG_CACHE_HOME", str(Path(".cache").resolve()))

import matplotlib
import plotly.graph_objs as go

from .adverse_selection import AdverseSelectionResult
from .risk_return import RiskReturnResult

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def create_risk_return_figure(result: RiskReturnResult) -> go.Figure:
    """Create a Plotly risk-return scatter plot with best-fit line."""

    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            name="Risk-Return Relationship",
            x=result.simulated_portfolios[:, 0],
            y=result.simulated_portfolios[:, 1],
            mode="markers",
        )
    )
    figure.add_trace(
        go.Scatter(
            name="Best Fit Line",
            x=result.simulated_portfolios[:, 0],
            y=result.best_fit,
            mode="lines",
        )
    )
    figure.update_layout(
        xaxis_title="Return",
        yaxis_title="Standard Deviation",
        width=900,
        height=470,
    )
    return figure


def create_adverse_selection_plot(
    result: AdverseSelectionResult,
    output_path: str | Path | None = None,
) -> None:
    """Create a Matplotlib adverse-selection supply and demand plot."""

    plt.style.use("seaborn-v0_8")
    plt.figure()
    plt.plot(
        result.demand_people,
        result.demand_average_cost,
        "r",
        label="insurance demand",
    )
    plt.plot(
        result.supply_people,
        result.supply_average_cost,
        "g",
        label="insurance supply",
    )
    plt.ylabel("Average Cost")
    plt.xlabel("Number of People")
    plt.legend()

    if output_path is not None:
        plt.savefig(output_path, bbox_inches="tight")
    else:
        plt.show()
    plt.close()
