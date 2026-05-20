"""Adverse-selection insurance model logic."""

from dataclasses import dataclass

import numpy as np

from src.config import AdverseSelectionConfig


@dataclass(frozen=True)
class AdverseSelectionResult:
    """Complete adverse-selection model output."""

    loss_probabilities: np.ndarray
    demand_people: np.ndarray
    demand_average_cost: np.ndarray
    supply_people: np.ndarray
    supply_average_cost: np.ndarray


def utility(wealth: float | np.ndarray, gamma: float) -> float | np.ndarray:
    """Calculate utility for a wealth value."""

    return np.exp(np.asarray(wealth) ** gamma)


def generate_loss_probabilities(
    population_size: int,
    rng: np.random.Generator,
) -> np.ndarray:
    """Generate sorted individual loss probabilities."""

    if population_size <= 0:
        raise ValueError("population_size must be positive.")
    return np.sort(rng.uniform(0, 1, population_size))


def supply(quantity: int, probabilities: np.ndarray, loss_cost: float) -> float:
    """Estimate average insurance supply cost for the highest-risk buyers."""

    if quantity <= 0:
        raise ValueError("quantity must be positive.")
    if quantity > len(probabilities):
        raise ValueError("quantity cannot exceed population size.")
    return float(np.mean(probabilities[-quantity:]) * loss_cost)


def demand(
    premium: float,
    probabilities: np.ndarray,
    income: float,
    loss_cost: float,
    gamma: float,
) -> int:
    """Count people whose expected utility is higher with insurance."""

    insured_utility = utility(income - premium, gamma)
    uninsured_utility = (
        probabilities * utility(income - loss_cost, gamma)
        + (1 - probabilities) * utility(income, gamma)
    )
    return int(np.sum(insured_utility > uninsured_utility))


def build_adverse_selection_result(
    config: AdverseSelectionConfig,
) -> AdverseSelectionResult:
    """Run the configured adverse-selection model."""

    rng = np.random.default_rng(config.random_seed)
    probabilities = generate_loss_probabilities(config.population_size, rng)
    premiums = np.arange(config.demand_min, config.demand_max, config.demand_step)
    demand_people = np.array(
        [
            demand(
                premium,
                probabilities,
                config.income,
                config.loss_cost,
                config.utility_gamma,
            )
            for premium in premiums
        ]
    )
    supply_people = np.arange(1, config.population_size + 1)
    supply_average_cost = np.array(
        [supply(quantity, probabilities, config.loss_cost) for quantity in supply_people]
    )

    return AdverseSelectionResult(
        loss_probabilities=probabilities,
        demand_people=demand_people,
        demand_average_cost=premiums,
        supply_people=supply_people,
        supply_average_cost=supply_average_cost,
    )
