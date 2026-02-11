# HW1: Time Series Momentum Strategy

## Overview

In this assignment you will implement a **time series momentum** trading
strategy from scratch using Python. The strategy examines
each asset's own past returns to decide whether to go long or short,
then sizes positions using a volatility-scaling approach.

You are provided with a CSV file of daily index prices for three major
equity indices (S&P 500, NASDAQ, Dow Jones) spanning multiple decades.
Your task is to build a modular, end-to-end pipeline that reads the
data, computes returns, generates trading signals, constructs a
portfolio, and reports key performance metrics.

> **Important:** All implementations must be **vectorized** (using
> pandas/numpy operations). Explicit Python `for` loops over rows or
> dates are **not allowed** and will result in zero credit for the
> affected function.

## Repository Structure

```
├── data/
│   └── price_data.csv          # Daily price data (provided)
├── src/
│   ├── __init__.py
│   ├── io.py                   # read_data
│   ├── returns.py              # calculate_returns
│   ├── momentum.py             # calculate_momentum
│   ├── signals.py              # generate_signals
│   ├── strategy.py             # calculate_volatility, calculate_strategy_returns
│   └── performance.py          # calculate_performance
├── tests/
│   ├── test_public_basic.py    # Type and structure checks
│   └── test_public_shapes.py   # Shape consistency and NaN pattern checks
├── hw1.py                      # Main entry point (do not modify)
├── requirements.txt            # Dependencies
└── README.md                   # This file
```

## Getting Started

```bash
# Clone your repository
git clone <your-repo-url>
cd hw1-<your-username>

# Install dependencies
pip install -r requirements.txt

# Run the pipeline (once you have implemented the functions)
python hw1.py --lookback_days 126
```

## Local Testing

Public tests are provided in the `tests/` directory so you can check
your work **before** pushing. These tests verify types, shapes, and
basic properties — they do **not** check numerical correctness (that
is done by the autograder on push).

```bash
# Run all public tests
pytest tests/ -v

# Run only the basic type/structure checks
pytest tests/test_public_basic.py -v

# Run only the shape consistency checks
pytest tests/test_public_shapes.py -v

# Run tests for a single function (e.g., momentum)
pytest tests/test_public_basic.py::TestCalculateMomentum -v
```

If a test is skipped or fails with `NotImplementedError`, it means
you haven't implemented that function yet — this is expected.

## What to Implement

Open each file under `src/` and implement the functions marked with
`raise NotImplementedError`. Every function has a detailed docstring
that specifies inputs, outputs, and the exact computation required.

| File | Function(s) | Description |
|------|-------------|-------------|
| `src/io.py` | `read_data` | Load CSV, parse dates, set index |
| `src/returns.py` | `calculate_returns` | Simple daily returns from prices |
| `src/momentum.py` | `calculate_momentum` | Cumulative return over past *k* days |
| `src/signals.py` | `generate_signals` | +1 / −1 from momentum sign |
| `src/strategy.py` | `calculate_volatility` | Rolling annualized std dev (252 days) |
| `src/strategy.py` | `calculate_strategy_returns` | Vol-scaled strategy returns + TSMOM |
| `src/performance.py` | `calculate_performance` | Sharpe, drawdown, etc. |

## Grading

Your submission is graded **automatically**. The autograder runs via GitHub Actions and tests each
function independently, awarding **partial credit** on a 100-point
scale.

### Grading Breakdown

| Component | Points |
|-----------|--------|
| `read_data` | 10 |
| `calculate_returns` | 15 |
| `calculate_momentum` | 20 |
| `generate_signals` | 10 |
| `calculate_volatility` | 10 |
| `calculate_strategy_returns` | 25 |
| `calculate_performance` | 10 |
| **Total** | **100** |

> **Note:** Each student is assigned a unique look-back period **in
> trading days** derived from their GitHub username. The autograder
> evaluates your code using your assigned parameter. Make sure your
> functions work correctly for **any** valid look-back value, not just
> a hard-coded one.

## Rules

- Do **not** modify `hw1.py`.
- Do **not** modify or remove `data/price_data.csv`.
- Do **not** modify or remove the `.github/` directory.
- Do **not** add any additional dependencies beyond what is listed in
  `requirements.txt`.
- All implementations must be **vectorized** — no explicit `for` /
  `while` loops over data rows.

## Tips

- Read the docstrings carefully — they specify the exact computation.
- Test incrementally: implement and verify one function at a time.
- You can run `python hw1.py --lookback_days 63` locally with any
  look-back value to check your pipeline end to end.
- Use `pandas.DataFrame.pct_change()`, `.rolling()`, `.shift()`,
  `.cumprod()`, and `numpy.sign()` to keep your code
  concise and fast.
