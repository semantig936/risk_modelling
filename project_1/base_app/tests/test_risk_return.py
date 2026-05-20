import numpy as np
import pytest

from src.config import RiskReturnConfig
from src.risk_analysis.risk_return import (
    build_risk_return_result,
    calculate_portfolio_metrics,
    generate_asset_returns,
    generate_weights,
)


def test_generate_weights_sum_to_one() -> None:
    rng = np.random.default_rng(1)
    weights = generate_weights(5, rng)

    assert len(weights) == 5
    assert np.isclose(weights.sum(), 1.0)


def test_generate_asset_returns_shape() -> None:
    rng = np.random.default_rng(1)
    returns = generate_asset_returns(5, 100, rng)

    assert returns.shape == (5, 100)


def test_calculate_portfolio_metrics_validates_weights() -> None:
    returns = np.ones((2, 10))
    weights = np.array([0.2, 0.2])

    with pytest.raises(ValueError):
        calculate_portfolio_metrics(returns, weights)


def test_build_risk_return_result_shapes() -> None:
    config = RiskReturnConfig(
        n_assets=5,
        n_simulations=100,
        portfolio_sizes=tuple(range(2, 10)),
        random_seed=1,
    )
    result = build_risk_return_result(config)

    assert result.simulated_portfolios.shape == (8, 2)
    assert result.best_fit.shape == (8,)
    assert len(result.weights) == 5
