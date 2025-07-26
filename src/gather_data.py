import pandas as pd 
import yfinance as yf

def gather_data(universe: list[str], start_date: str, end_date: str) -> pd.DataFrame:
    """
    Downloads historical adjusted closing prices (adjusted for splits and dividends)
    for a list of tickers using Yahoo Finance. 
    
    Saves the DataFrame to 'results/close_prices.csv'.

    Args:
        universe (list[str]): List of ticker symbols from Yahoo Finance.
        start_date (str): Start date in "YYYY-MM-DD" format.
        end_date (str): End date in "YYYY-MM-DD" format.

    Returns:
        pd.DataFrame: A DataFrame indexed by date with one column per ticker. All rows with missing data are removed.
    """

    close_prices = yf.download(universe, start = start_date, end = end_date, auto_adjust = True)['Close']
    # Remove rows with missing data to ensure time series alignment across all tickers
    close_prices = close_prices.dropna()
    close_prices.to_csv('results/close_prices.csv')
    return close_prices

