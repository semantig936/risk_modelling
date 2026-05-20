import numpy as np
import pytest

from src.config import AdverseSelectionConfig
from src.risk_analysis.adverse_selection import (
    build_adverse_selection_result,
    demand,
    generate_loss_probabilities,
    supply,
)


def test_generate_loss_probabilities_are_sorted() -> None:
    rng = np.random.default_rng(1)
    probabilities = generate_loss_probabilities(20, rng)

    assert len(probabilities) == 20
    assert np.all(np.diff(probabilities) >= 0)


def test_supply_rejects_invalid_quantity() -> None:
    probabilities = np.array([0.1, 0.2, 0.3])

    with pytest.raises(ValueError):
        supply(0, probabilities, 1.5)


def test_demand_returns_population_count() -> None:
    probabilities = np.array([0.1, 0.4, 0.8])
    count = demand(0.5, probabilities, income=2.0, loss_cost=1.5, gamma=0.4)

    assert 0 <= count <= len(probabilities)


def test_build_adverse_selection_result_shapes() -> None:
    result = build_adverse_selection_result(AdverseSelectionConfig(random_seed=1))

    assert len(result.loss_probabilities) == 20
    assert len(result.demand_people) == len(result.demand_average_cost)
    assert len(result.supply_people) == 20
    assert len(result.supply_average_cost) == 20
