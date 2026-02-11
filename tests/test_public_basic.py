"""
Public tests — basic type and structure checks.

These tests verify that each function:
  - exists and is callable
  - returns the correct type
  - returns reasonable output (not NotImplementedError)

Run with:  pytest tests/ -v
"""

import pytest
import pandas as pd
import numpy as np

DATA_PATH = "data/price_data.csv"
LOOKBACK_DAYS = 63  # arbitrary valid value for local testing


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


# ── 1. read_data ──────────────────────────────────────────────

class TestReadData:
    def test_returns_dataframe(self, prices):
        assert isinstance(prices, pd.DataFrame)

    def test_index_is_datetime(self, prices):
        assert isinstance(prices.index, pd.DatetimeIndex)

    def test_index_name(self, prices):
        assert prices.index.name == "Date"

    def test_has_expected_columns(self, prices):
        assert set(prices.columns) == {"SP500", "NASDAQ", "DJIA"}

    def test_not_empty(self, prices):
        assert len(prices) > 0

    def test_dtypes_are_float(self, prices):
        for col in prices.columns:
            assert np.issubdtype(prices[col].dtype, np.floating), (
                f"Column '{col}' has dtype {prices[col].dtype}, expected float"
            )


# ── 2. calculate_returns ──────────────────────────────────────

class TestCalculateReturns:
    def test_returns_dataframe(self, daily_returns):
        assert isinstance(daily_returns, pd.DataFrame)

    def test_same_columns_as_prices(self, prices, daily_returns):
        assert list(daily_returns.columns) == list(prices.columns)

    def test_same_index_as_prices(self, prices, daily_returns):
        assert daily_returns.index.equals(prices.index)

    def test_first_row_is_nan(self, daily_returns):
        assert daily_returns.iloc[0].isna().all(), (
            "First row should be NaN (no prior price to compute return)"
        )

    def test_no_inf_values(self, daily_returns):
        assert not np.isinf(daily_returns.values[1:]).any(), (
            "Returns should not contain infinite values"
        )


# ── 3. calculate_momentum ────────────────────────────────────

class TestCalculateMomentum:
    def test_returns_dataframe(self, momentum):
        assert isinstance(momentum, pd.DataFrame)

    def test_same_columns_as_returns(self, daily_returns, momentum):
        assert list(momentum.columns) == list(daily_returns.columns)

    def test_early_rows_are_nan(self, momentum):
        # With lookback=63 and shift(1), at least the first 63 rows
        # should be NaN
        first_valid = momentum.first_valid_index()
        assert first_valid is not None, "All values are NaN"
        first_valid_pos = momentum.index.get_loc(first_valid)
        assert first_valid_pos >= LOOKBACK_DAYS, (
            f"First non-NaN at row {first_valid_pos}, "
            f"expected at least {LOOKBACK_DAYS} NaN rows"
        )

    def test_has_some_valid_values(self, momentum):
        assert momentum.notna().any().any(), (
            "Momentum should have some non-NaN values"
        )


# ── 4. generate_signals ──────────────────────────────────────

class TestGenerateSignals:
    def test_returns_dataframe(self, signals):
        assert isinstance(signals, pd.DataFrame)

    def test_same_shape_as_momentum(self, momentum, signals):
        assert signals.shape == momentum.shape

    def test_values_in_valid_set(self, signals):
        unique_vals = set(signals.values.flatten())
        valid = unique_vals - {np.nan}
        assert valid.issubset({-1.0, 0.0, 1.0}), (
            f"Signals should be in {{-1, 0, +1}}, got extra: "
            f"{valid - {-1.0, 0.0, 1.0}}"
        )

    def test_no_nan_in_output(self, signals):
        assert not signals.isna().any().any(), (
            "Signals should not contain NaN — NaN momentum should map to 0"
        )


# ── 5. calculate_volatility ──────────────────────────────────

class TestCalculateVolatility:
    def test_returns_dataframe(self, volatility):
        assert isinstance(volatility, pd.DataFrame)

    def test_same_columns_as_returns(self, daily_returns, volatility):
        assert list(volatility.columns) == list(daily_returns.columns)

    def test_non_negative_values(self, volatility):
        valid = volatility.dropna()
        assert (valid >= 0).all().all(), (
            "Volatility should be non-negative"
        )

    def test_has_some_valid_values(self, volatility):
        assert volatility.notna().any().any(), (
            "Volatility should have some non-NaN values"
        )


# ── 6. calculate_strategy_returns ─────────────────────────────

class TestCalculateStrategyReturns:
    def test_returns_dataframe(self, strategy_returns):
        assert isinstance(strategy_returns, pd.DataFrame)

    def test_has_tsmom_column(self, strategy_returns):
        assert "TSMOM" in strategy_returns.columns, (
            "Output should contain a 'TSMOM' column"
        )

    def test_has_asset_columns(self, strategy_returns):
        for col in ["SP500", "NASDAQ", "DJIA"]:
            assert col in strategy_returns.columns, (
                f"Missing asset column: '{col}'"
            )

    def test_no_inf_values(self, strategy_returns):
        valid = strategy_returns.dropna()
        assert not np.isinf(valid.values).any(), (
            "Strategy returns should not contain infinite values"
        )


# ── 7. calculate_performance ─────────────────────────────────

class TestCalculatePerformance:
    @pytest.fixture(scope="class")
    def performance(self, strategy_returns):
        from src.performance import calculate_performance
        return calculate_performance(strategy_returns["TSMOM"])

    def test_returns_dict(self, performance):
        assert isinstance(performance, dict)

    def test_has_annualized_return(self, performance):
        assert "annualized_return" in performance

    def test_has_annualized_volatility(self, performance):
        assert "annualized_volatility" in performance

    def test_has_sharpe_ratio(self, performance):
        assert "sharpe_ratio" in performance

    def test_values_are_finite(self, performance):
        for key, val in performance.items():
            assert np.isfinite(val), (
                f"'{key}' should be finite, got {val}"
            )

    def test_volatility_is_positive(self, performance):
        assert performance["annualized_volatility"] > 0, (
            "Annualized volatility should be positive"
        )
