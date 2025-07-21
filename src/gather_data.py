def gather_data(universe, start_date, end_date):
    """
    Gathers historical adjusted close prices for a list of tickers using Yahoo Finance.

    Parameters:
        universe (list of str): List of ticker symbols to download.
        start_date (str): Start date in "YYYY-MM-DD" format.
        end_date (str): End date in "YYYY-MM-DD" format.

    Returns:
        pd.DataFrame: Historical adjusted close price data, indexed by dates with assets as columns.
    """
    import yfinance as yf
    import pandas as pd

    close_prices = yf.download(universe, start = start_date, end = end_date, auto_adjust = True)['Close']
    close_prices = close_prices.dropna()
    close_prices.to_csv('results/close_prices.csv')
    return close_prices

