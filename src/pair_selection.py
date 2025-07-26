from itertools import combinations
import pandas as pd
from statsmodels.tsa.stattools import coint

def pair_selection(universe: list[str], close_prices: pd.DataFrame) -> list[tuple]:
    """
    Calculates the Pearson correlation coefficient for each unique pair, and filters out any combination with a correlation < 0.89.
    Applies the Engle-Granger cointegration test on any remaining pairs, labeling any combination with a p-value ≤ 0.05 as cointegrated.
    The cointegrated pairs are saved to 'results/cointegrated_pairs.csv'
    
    Args:
        universe (list[str]): List of ticker symbols from Yahoo Finance.
        close_prices (pd.DataFrame): Historical adjusted close price data, indexed by date (business days) with tickers as columns.

    Returns:
        list[tuple[str, str]]: List of tuples containing the cointegrated combinations that pass the correlation and p-value threshold. 
    """

    combinations_list = list(combinations(universe, 2))
    
    correlated_pairs = {}
    for combination in combinations_list:
        assetA = combination[0]
        assetB = combination[1]

        assetA_close_price = close_prices[assetA]
        assetB_close_price = close_prices[assetB]

        correlation = assetA_close_price.corr(assetB_close_price)
        if correlation >=0.89:
            correlated_pairs[combination] = correlation

    cointegrated_pairs = []
    for combination in correlated_pairs:
        assetA = combination[0]
        assetB = combination[1]

        assetA_close_price = close_prices[assetA]
        assetB_close_price = close_prices[assetB]

        pvalue = coint(assetA_close_price, assetB_close_price)[1]
        if pvalue <= 0.05:
            cointegrated_pairs.append((assetA, assetB))
    
    cointegrated_pairs_df = pd.DataFrame(cointegrated_pairs, columns = ['Asset A', 'Asset B'])
    cointegrated_pairs_df.to_csv('results/cointegrated_pairs.csv')
    
    return cointegrated_pairs
    

