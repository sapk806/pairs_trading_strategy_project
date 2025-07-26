import pandas as pd
import numpy as np

def performance_metrics(portfolio_values: pd.Series):
    """
    Calculates key performance metrics to evaluate the strategy's effectiveness and risk-adjusted returns.

    Metrics Include:
        Cumulative Return
        Volatility
        Sharpe Ratio
        Max_drawdown
        Sortino Ratio
        Highest Values

    Args:
        portfolio_values(pd.Series): Series containing the values of the portfolio, indexed by date.
    
    Returns:
        float: Cumulative return of the portfolio.
        float: Volatility of the portfolio.
        float: Sharpe Ratio of the portoflio.
        float: Max drawdown of the portfolio.
        float: Sortino ratio of the portfolio.
        pd.Series: Series containing the highest value at each index, which is by date.
        float: CAGR of the portfolio.
    """

    initial_portfolio_value = portfolio_values.iloc[0]
    final_portfolio_value = portfolio_values.iloc[-1]

    risk_free_rate = 0 
    daily_returns = portfolio_values.pct_change().dropna()
    
    avg_daily_returns = daily_returns.mean() * 252
    std_daily_returns = daily_returns.std(ddof = 1) * np.sqrt(252)

    current_highest = 0 
    drawdowns = {}
    max_values = {}
    for date in portfolio_values.index:
        value = portfolio_values.loc[date]
        if value > current_highest:
            current_highest = value
        max_values[date] = current_highest
        drawdown = (value / current_highest) - 1
        drawdowns[date] = drawdown
    max_values = pd.Series(max_values)
    
    negative_daily_returns = []
    for daily_return in daily_returns:
        if daily_return < 0:
            negative_daily_returns.append(daily_return)
    negative_daily_returns = pd.Series(negative_daily_returns).dropna()
    std_negative_daily_returns = negative_daily_returns.std(ddof = 1) * np.sqrt(252)

    n_years = 2
    CAGR = (final_portfolio_value / initial_portfolio_value)**(1 / n_years) - 1
    
    sortino_ratio = (avg_daily_returns - risk_free_rate) / std_negative_daily_returns
    sharpe_ratio = (avg_daily_returns - risk_free_rate) / std_daily_returns
    cumulative_return = (final_portfolio_value - initial_portfolio_value) / initial_portfolio_value
    max_drawdown = min(drawdowns.values())
    volatility = std_daily_returns

   
    return cumulative_return, volatility, sharpe_ratio, max_drawdown, sortino_ratio, max_values, CAGR


