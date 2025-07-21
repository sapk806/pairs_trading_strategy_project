## Pairs Trading Strategy Backtest Using Cointegration and Z-Score Signals

## Overview
My project uses the adjusted close prices of multiple assets to find cointegration between pairs, and generates trading signals using the Z-score of each cointegrated pair.

## Dependencies 
- Python 3.13+
- pandas
- numpy
- matplotlib
- yfinance
- jupyter

## How to Run
- Activate the virtual environment with the required packages and run the script in the main.py file: 

1. Activate the virtual environment.
```bash
source .venv/bin/activate
```
2. Install dependencies.
```bash
pip install -r requirements.txt
```
3. Run the full backtest.
```bash
python main.py
```


## Output
- Plot of the portfolio value over time
- Performance metrics 
    - Cumulative return
    - CAGR
    - Volatility
    - Max drawdown
    - Sharpe ratio
    - Sortino ratio