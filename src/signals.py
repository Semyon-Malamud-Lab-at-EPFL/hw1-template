"""Trading signal generation."""

import pandas as pd
import numpy as np


def generate_signals(momentum: pd.DataFrame) -> pd.DataFrame:
    """
    Generate trading signals from momentum values.

    The signal is determined by the sign of the momentum:
        - +1.0 if momentum > 0  (go long)
        - -1.0 if momentum < 0  (go short)
        -  0.0 if momentum is NaN or exactly 0

    Parameters
    ----------
    momentum : pd.DataFrame
        DataFrame of momentum values (output of calculate_momentum).

    Returns
    -------
    pd.DataFrame
        DataFrame of trading signals (+1.0, -1.0, or 0.0) with the
        same shape, index, and columns as the input.

    Notes
    -----
    Use vectorized operations (e.g., numpy.sign). Do NOT use explicit loops.
    """
    
    # TODO: Implement this function (vectorized, no loops)
    raise NotImplementedError("Implement generate_signals")
