"""Risk-return portfolio simulation logic."""

from dataclasses import dataclass

import numpy as np
import statsmodels.api as sm

from src.config import RiskReturnConfig


@dataclass(frozen=True)
class PortfolioMetrics:
    """Expected return and volatility for one simulated portfolio."""

    expected_return: float
    standard_deviation: float


@dataclass(frozen=True)
class RiskReturnResult:
    """Complete risk-return simulation output."""

    single_portfolio: PortfolioMetrics
    simulated_portfolios: np.ndarray
    best_fit: np.ndarray
    weights: np.ndarray


def generate_asset_returns(
    n_assets: int,
    n_periods: int,
    rng: np.random.Generator,
) -> np.ndarray:
    """Generate normally distributed asset returns."""

    if n_assets <= 0:
        raise ValueError("n_assets must be positive.")
    if n_periods <= 1:
        raise ValueError("n_periods must be greater than 1.")
    return rng.standard_normal((n_assets, n_periods))


def generate_weights(n_assets: int, rng: np.random.Generator) -> np.ndarray:
    """Generate random portfolio weights that sum to one."""

    if n_assets <= 0:
        raise ValueError("n_assets must be positive.")
    raw_weights = rng.random(n_assets)
    return raw_weights / raw_weights.sum()


def calculate_portfolio_metrics(
    returns: np.ndarray,
    weights: np.ndarray,
) -> PortfolioMetrics:
    """Calculate portfolio expected return and standard deviation."""

    if returns.ndim != 2:
        raise ValueError("returns must be a two-dimensional array.")
    if returns.shape[0] != len(weights):
        raise ValueError("weights length must match the number of assets.")
    if not np.isclose(weights.sum(), 1.0):
        raise ValueError("weights must sum to one.")

    asset_expected_returns = returns.mean(axis=1)
    covariance = np.cov(returns)
    expected_return = float(np.dot(weights, asset_expected_returns))
    variance = float(weights.T @ covariance @ weights)
    standard_deviation = float(np.sqrt(max(variance, 0.0)))

    return PortfolioMetrics(expected_return, standard_deviation)


def build_risk_return_result(config: RiskReturnConfig) -> RiskReturnResult:
    """Run the configured risk-return simulation."""

    rng = np.random.default_rng(config.random_seed)
    weights = generate_weights(config.n_assets, rng)
    returns = generate_asset_returns(config.n_assets, config.n_simulations, rng)
    single_portfolio = calculate_portfolio_metrics(returns, weights)

    simulated_portfolios = np.array(
        [
            calculate_portfolio_metrics(
                generate_asset_returns(config.n_assets, periods, rng),
                weights,
            )
            for periods in config.portfolio_sizes
        ],
        dtype=object,
    )
    portfolio_points = np.array(
        [
            [item.expected_return, item.standard_deviation]
            for item in simulated_portfolios
        ]
    )
    best_fit = sm.OLS(
        portfolio_points[:, 1],
        sm.add_constant(portfolio_points[:, 0]),
    ).fit().fittedvalues

    return RiskReturnResult(
        single_portfolio=single_portfolio,
        simulated_portfolios=portfolio_points,
        best_fit=best_fit,
        weights=weights,
    )
