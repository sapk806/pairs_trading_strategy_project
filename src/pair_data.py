def pair_data(cointegrated_pairs, close_prices):
    """
    Runs OLS on each cointegrated combination to find the hedge ratios and the spread z-scores.

    Parameters:
        cointegrated_pairs (list of tuples): A list of tuples containing the cointegrated combinations.
        close_prices (pd.DataFrame): Historical adjusted close price data, indexed by dates with assets as columns.

    Returns:
        pd.DataFrame: A DataFrame containing each cointegrated combination and a series of their corresponding z-scores gatheres, indexed by date with combinations as columns.
        dict: A dictionary containing each combination as the key and their corresponding hedge ratio, which was found using OLS.
    """
    import yfinance as yf
    import pandas as pd
    from statsmodels.tsa.stattools import OLS
    from statsmodels.tsa.stattools import add_constant

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

