"""Momentum calculation utilities."""

import pandas as pd


def calculate_momentum(daily_returns: pd.DataFrame, lookback_days: int) -> pd.DataFrame:
    """
    Calculate the momentum signal as the cumulative compounded return
    over the past `lookback_days` trading days.

    For each asset at day t, the momentum signal is defined as the
    compounded return from day (t - lookback_days) to day (t - 1),
    i.e., we skip the current day's return:

        momentum_t = (1 + r_{t-lookback_days}) *
                     (1 + r_{t-lookback_days+1}) *
                     ... *
                     (1 + r_{t-1}) - 1

    Rows where insufficient history exists should be NaN.

    Parameters
    ----------
    daily_returns : pd.DataFrame
        DataFrame of daily simple returns with a DatetimeIndex.
    lookback_days : int
        Number of trading days to look back

    Returns
    -------
    pd.DataFrame
        DataFrame of momentum values with the same columns as input.
        Rows with insufficient history will contain NaN.

    Notes
    -----
    Use vectorized pandas/numpy operations. Do NOT use explicit loops.
    """
    
    # TODO: Implement this function (vectorized, no loops)
    raise NotImplementedError("Implement calculate_momentum")
