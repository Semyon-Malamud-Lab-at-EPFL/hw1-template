"""Performance metrics calculation."""

import pandas as pd
import numpy as np


def calculate_performance(daily_returns: pd.Series) -> dict:
    """
    Calculate key performance metrics for a daily return series.

    The following metrics should be computed:

    1. Annualized Return:
        annualized_return = mean(r) * 252

    2. Annualized Volatility:
        annualized_volatility = std(r) * sqrt(252)

    3. Sharpe Ratio (assuming zero risk-free rate):
        sharpe_ratio = annualized_return / annualized_volatility

    Parameters
    ----------
    daily_returns : pd.Series
        Series of daily simple returns. May contain NaN values,
        which should be dropped before computation.

    Returns
    -------
    dict
        Dictionary with the following keys:
            - 'annualized_return'     : float
            - 'annualized_volatility' : float
            - 'sharpe_ratio'          : float

    Notes
    -----
    Use vectorized pandas/numpy operations. Do NOT use explicit loops.
    Drop NaN values before performing calculations.
    """
    
    # TODO: Implement this function (vectorized, no loops)
    raise NotImplementedError("Implement calculate_performance")
