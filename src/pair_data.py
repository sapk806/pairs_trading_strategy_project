import yfinance as yf
import pandas as pd
from statsmodels.tsa.stattools import OLS
from statsmodels.tsa.stattools import add_constant

def pair_data(cointegrated_pairs: list[tuple[str, str]], close_prices: pd.DataFrame):
    """
    Performs OLS regression on each cointegrated asset pair to estimate hedge ratios and spread z-scores.

    Args:
        cointegrated_pairs (list[tuple[str, str]]): List of tuples containing the cointegrated combinations that pass the correlation and p-value threshold. 
        close_prices (pd.DataFrame): Historical adjusted close price data, indexed by date (business days) with tickers as columns.

    Returns:
        pd.DataFrame: DataFrame where each column corresponds to a cointegrated pair, and contains the z-score time series of their spread.
        dict[tuple[str, str], float]: Dictionary where each key corresponds to the cointegrated pair and the value corresponds to their corresponding hedge ratio.
    """
    
    zscore_dict = {}
    hedge_ratio_dict = {}
    for combination in cointegrated_pairs:
        assetA = combination[0]
        assetB = combination[1]

        assetA_close_prices = close_prices[assetA]
        assetB_close_prices = close_prices[assetB]
        assetB_close_prices_with_constant = add_constant(assetB_close_prices)

        model = OLS(assetA_close_prices, assetB_close_prices_with_constant)
        result = model.fit()
        hedge_ratio = result.params.iloc[1]
        spread = result.resid
        hedge_ratio_dict[combination] = hedge_ratio
        
        zscore = (spread - spread.mean()) / spread.std()
        zscore_dict[combination] = zscore
    zscore_df = pd.DataFrame(zscore_dict)
    zscore_df.to_csv('results/zscores.csv')
    return zscore_df, hedge_ratio_dict

