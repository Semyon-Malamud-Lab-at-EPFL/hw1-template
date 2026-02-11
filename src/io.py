"""Data loading utilities."""

import pandas as pd


def read_data(filepath: str) -> pd.DataFrame:
    """
    Read the CSV price data file.

    The CSV file has columns: Date, SP500, NASDAQ, DJIA.
    This function should:
        1. Read the CSV file.
        2. Parse the 'Date' column as datetime and set it as the index.
        3. Ensure all price columns are numeric (float).

    Parameters
    ----------
    filepath : str
        Path to the CSV file containing daily price data.

    Returns
    -------
    pd.DataFrame
        DataFrame with a DatetimeIndex named 'Date' and columns
        ['SP500', 'NASDAQ', 'DJIA'] containing float price values.
    """
    
    # TODO: Implement this function (vectorized, no loops)
    raise NotImplementedError("Implement read_data")
