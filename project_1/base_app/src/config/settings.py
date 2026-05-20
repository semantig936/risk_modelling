"""Application configuration defaults."""

from dataclasses import dataclass


@dataclass(frozen=True)
class RiskReturnConfig:
    """Configuration for risk-return portfolio simulations."""

    n_assets: int = 5
    n_simulations: int = 500
    portfolio_sizes: tuple[int, ...] = tuple(range(2, 101))
    random_seed: int | None = 42


@dataclass(frozen=True)
class AdverseSelectionConfig:
    """Configuration for the adverse-selection insurance model."""

    population_size: int = 20
    income: float = 2.0
    loss_cost: float = 1.5
    utility_gamma: float = 0.4
    demand_min: float = 0.0
    demand_max: float = 1.9
    demand_step: float = 0.02
    random_seed: int | None = 42
