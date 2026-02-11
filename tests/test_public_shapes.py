"""
Public tests — shape consistency and dimensional checks.

These tests verify that outputs have correct dimensions and that
the pipeline is internally consistent (shapes propagate correctly
from one function to the next).

Run with:  pytest tests/ -v
"""

import pytest
import pandas as pd
import numpy as np

DATA_PATH = "data/price_data.csv"
LOOKBACK_DAYS = 63


# ── Fixtures ──────────────────────────────────────────────────

@pytest.fixture(scope="module")
def prices():
    from src.io import read_data
    return read_data(DATA_PATH)


@pytest.fixture(scope="module")
def daily_returns(prices):
    from src.returns import calculate_returns
    return calculate_returns(prices)


@pytest.fixture(scope="module")
def momentum(daily_returns):
    from src.momentum import calculate_momentum
    return calculate_momentum(daily_returns, lookback_days=LOOKBACK_DAYS)


@pytest.fixture(scope="module")
def signals(momentum):
    from src.signals import generate_signals
    return generate_signals(momentum)


@pytest.fixture(scope="module")
def volatility(daily_returns):
    from src.strategy import calculate_volatility
    return calculate_volatility(daily_returns, vol_lookback=LOOKBACK_DAYS)


@pytest.fixture(scope="module")
def strategy_returns(signals, daily_returns, volatility):
    from src.strategy import calculate_strategy_returns
    return calculate_strategy_returns(
        signals=signals,
        daily_returns=daily_returns,
        volatility=volatility,
        target_vol=0.10,
    )


# ── Shape preservation through the pipeline ───────────────────

class TestShapeConsistency:
    """Returns, momentum, signals, and volatility should all share
    the same shape as the price DataFrame (same rows × same columns)."""

    def test_returns_shape_matches_prices(self, prices, daily_returns):
        assert daily_returns.shape == prices.shape, (
            f"Returns shape {daily_returns.shape} != prices shape {prices.shape}"
        )

    def test_momentum_shape_matches_prices(self, prices, momentum):
        assert momentum.shape == prices.shape, (
            f"Momentum shape {momentum.shape} != prices shape {prices.shape}"
        )

    def test_signals_shape_matches_prices(self, prices, signals):
        assert signals.shape == prices.shape, (
            f"Signals shape {signals.shape} != prices shape {prices.shape}"
        )

    def test_volatility_shape_matches_prices(self, prices, volatility):
        assert volatility.shape == prices.shape, (
            f"Volatility shape {volatility.shape} != prices shape {prices.shape}"
        )

    def test_strategy_has_extra_tsmom_column(self, prices, strategy_returns):
        expected_cols = len(prices.columns) + 1  # assets + TSMOM
        assert len(strategy_returns.columns) == expected_cols, (
            f"Strategy should have {expected_cols} columns "
            f"({len(prices.columns)} assets + TSMOM), "
            f"got {len(strategy_returns.columns)}"
        )

    def test_strategy_rows_match_prices(self, prices, strategy_returns):
        assert len(strategy_returns) == len(prices), (
            f"Strategy has {len(strategy_returns)} rows, "
            f"expected {len(prices)}"
        )


# ── Index preservation through the pipeline ───────────────────

class TestIndexConsistency:
    """All DataFrames should share the same DatetimeIndex."""

    def test_returns_index(self, prices, daily_returns):
        assert daily_returns.index.equals(prices.index)

    def test_momentum_index(self, prices, momentum):
        assert momentum.index.equals(prices.index)

    def test_signals_index(self, prices, signals):
        assert signals.index.equals(prices.index)

    def test_volatility_index(self, prices, volatility):
        assert volatility.index.equals(prices.index)

    def test_strategy_index(self, prices, strategy_returns):
        assert strategy_returns.index.equals(prices.index)


# ── NaN pattern checks ────────────────────────────────────────

class TestNaNPatterns:
    """Functions that use rolling windows should produce NaN for
    rows where insufficient history is available."""

    def test_returns_exactly_one_nan_row(self, daily_returns):
        nan_rows = daily_returns.isna().all(axis=1).sum()
        assert nan_rows == 1, (
            f"Returns should have exactly 1 NaN row (first row), "
            f"got {nan_rows}"
        )

    def test_momentum_nan_count(self, momentum):
        # With lookback_days=63 and shift(1), we expect at least 63
        # rows of NaN at the start (plus 1 from the NaN in returns)
        first_col = momentum.iloc[:, 0]
        leading_nans = first_col.isna().cumsum()
        nan_count = (leading_nans == range(1, len(leading_nans) + 1)).sum()
        assert nan_count >= LOOKBACK_DAYS, (
            f"Expected at least {LOOKBACK_DAYS} leading NaN rows "
            f"in momentum, got {nan_count}"
        )

    def test_volatility_nan_count(self, volatility):
        first_col = volatility.iloc[:, 0]
        leading_nans = first_col.isna().cumsum()
        nan_count = (leading_nans == range(1, len(leading_nans) + 1)).sum()
        assert nan_count >= LOOKBACK_DAYS, (
            f"Expected at least {LOOKBACK_DAYS} leading NaN rows "
            f"in volatility, got {nan_count}"
        )


# ── Lookback parameter robustness ─────────────────────────────

class TestLookbackVariation:
    """Verify that functions work with different lookback values."""

    @pytest.mark.parametrize("k", [21, 126, 252])
    def test_momentum_different_lookbacks(self, daily_returns, k):
        from src.momentum import calculate_momentum
        result = calculate_momentum(daily_returns, lookback_days=k)
        assert result.shape == daily_returns.shape
        assert result.notna().any().any(), f"All NaN for lookback={k}"

    @pytest.mark.parametrize("k", [21, 126, 252])
    def test_volatility_different_lookbacks(self, daily_returns, k):
        from src.strategy import calculate_volatility
        result = calculate_volatility(daily_returns, vol_lookback=k)
        assert result.shape == daily_returns.shape
        assert result.notna().any().any(), f"All NaN for lookback={k}"
