"""
HW1: Time Series Momentum Strategy
===================================

This is the main entry point for the homework. It orchestrates the
full pipeline from raw daily price data to strategy performance metrics.

Usage:
    python hw1.py [--lookback_days DAYS]
"""

import argparse

from src.io import read_data
from src.returns import calculate_returns
from src.momentum import calculate_momentum
from src.signals import generate_signals
from src.strategy import calculate_volatility, calculate_strategy_returns
from src.performance import calculate_performance


def run_pipeline(
    lookback_days: int = 252, data_path: str = "data/price_data.csv"
) -> dict:
    """
    Run the full time series momentum pipeline.

    Parameters
    ----------
    lookback_days : int
        Number of trading days for the momentum look-back period.
    data_path : str
        Path to the CSV price data file.

    Returns
    -------
    dict
        Dictionary of performance metrics for the TSMOM strategy.
    """
    # Step 1: Load data
    daily_prices = read_data(data_path)

    # Step 2: Calculate daily returns
    daily_returns = calculate_returns(daily_prices)

    # Step 3: Calculate momentum signal
    momentum = calculate_momentum(daily_returns, lookback_days=lookback_days)

    # Step 4: Generate trading signals
    signals = generate_signals(momentum)

    # Step 5: Calculate rolling volatility
    volatility = calculate_volatility(daily_returns, vol_lookback=lookback_days)

    # Step 6: Calculate strategy returns
    strategy_returns = calculate_strategy_returns(
        signals=signals,
        daily_returns=daily_returns,
        volatility=volatility,
        target_vol=0.10,
    )

    # Step 7: Calculate performance metrics for the TSMOM portfolio
    tsmom_returns = strategy_returns["TSMOM"]
    performance = calculate_performance(tsmom_returns)

    return performance


def main():
    parser = argparse.ArgumentParser(description="HW1: Time Series Momentum")
    parser.add_argument(
        "--lookback_days",
        type=int,
        default=252,
        help="Momentum look-back period in trading days (default: 252)",
    )
    parser.add_argument(
        "--data",
        type=str,
        default="data/price_data.csv",
        help="Path to price data CSV",
    )
    args = parser.parse_args()

    print(f"Running Time Series Momentum Strategy (lookback={args.lookback_days} days)")
    print("=" * 60)

    performance = run_pipeline(
        lookback_days=args.lookback_days, data_path=args.data
    )

    print(f"\nPerformance Metrics (TSMOM Portfolio):")
    print(f"  Annualized Return:     {performance['annualized_return']:>10.4f}")
    print(f"  Annualized Volatility: {performance['annualized_volatility']:>10.4f}")
    print(f"  Sharpe Ratio:          {performance['sharpe_ratio']:>10.4f}")


if __name__ == "__main__":
    main()
