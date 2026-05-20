"""Command-line entry point for the risk analysis project."""

from pathlib import Path

from src.config import AdverseSelectionConfig, RiskReturnConfig
from src.risk_analysis.adverse_selection import build_adverse_selection_result
from src.risk_analysis.risk_return import build_risk_return_result
from src.risk_analysis.visualization import (
    create_adverse_selection_plot,
    create_risk_return_figure,
)


def main() -> None:
    """Run both notebook analyses and save their visual outputs."""

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    risk_return_result = build_risk_return_result(RiskReturnConfig())
    risk_return_figure = create_risk_return_figure(risk_return_result)
    risk_return_figure.write_html(output_dir / "risk_return.html")

    adverse_selection_result = build_adverse_selection_result(
        AdverseSelectionConfig()
    )
    create_adverse_selection_plot(
        adverse_selection_result,
        output_dir / "adverse_selection.png",
    )

    print("Risk analysis complete.")
    print(f"Portfolio return: {risk_return_result.single_portfolio.expected_return:.6f}")
    print(
        "Portfolio standard deviation: "
        f"{risk_return_result.single_portfolio.standard_deviation:.6f}"
    )
    print(f"Outputs saved to: {output_dir.resolve()}")


if __name__ == "__main__":
    main()
