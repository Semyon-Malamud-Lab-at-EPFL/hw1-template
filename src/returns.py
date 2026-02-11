"""Return calculation utilities."""

import pandas as pd


def calculate_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate daily simple returns from a price DataFrame.

    The simple return for day t is defined as:
        r_t = (P_t / P_{t-1}) - 1

    The first row of the output will contain NaN values since there is
    no previous price to compute a return from.

    Parameters
    ----------
    prices : pd.DataFrame
        DataFrame with a DatetimeIndex and one or more columns of
        daily closing prices.

    Returns
    -------
    pd.DataFrame
        DataFrame of daily simple returns with the same shape, index,
        and columns as the input. The first row will be NaN.

    Notes
    -----
    Use vectorized pandas operations. Do NOT use explicit loops.
    """
    
    # TODO: Implement this function (vectorized, no loops)
    raise NotImplementedError("Implement calculate_returns")
